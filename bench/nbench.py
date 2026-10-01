#!/usr/bin/env python3
"""Banc réseau N — propagation de blocs, charge de fond, horloge, rattrapage (v2).

Un processus par nœud. Maillage TCP complet, inondation, dédoublonnage par id.
Sans dépendance. Voir PLAN-BANC.md.

Horodatages (ns, horloge murale locale) :
  send_ns   origine, juste avant mise en file (après construction du bloc)
  write_ns  émetteur du lien, au moment de l'écriture socket (réécrit à chaque saut)
  recv_ns   récepteur, trame complète lue
=> lien = recv − write (réseau + noyau, biaisé par l'offset du lien) ;
   bout-en-bout = recv − send (biaisé par l'offset origine→récepteur).
Émission découplée : une file et une tâche d'écriture par pair ; la production ne bloque jamais.
"""
import argparse, asyncio, os, random, struct, time, json

T_BLOCK, T_TX, T_PING, T_PONG, T_HELLO, T_INV, T_SYNCBLK = 1, 2, 3, 4, 5, 6, 7
HDR = struct.Struct('>IBq')                # longueur, type, write_ns
BLK = struct.Struct('>16sQqHB')            # id, slot, send_ns, origine idx, sauts
TXH = struct.Struct('>16sqH')              # id, send_ns, origine idx
SIZES = [(0.5, 2820), (0.4, 65536), (0.1, 2820 + 262144)]
KEEP_SLOTS = 1800
QUEUE_MAX = 64 * 1024 * 1024               # octets en file par pair avant abandon journalisé


def now_ns():
    return time.time_ns()


class Peer:
    def __init__(self, node, name, w):
        self.node, self.name, self.w = node, name, w
        self.q = asyncio.Queue()
        self.qbytes = 0
        self.task = asyncio.create_task(self.writer())

    def put(self, typ, payload):
        if self.qbytes + len(payload) > QUEUE_MAX:
            self.node.ev('drop', self.name, typ, len(payload))
            return
        self.qbytes += len(payload)
        self.q.put_nowait((typ, payload, time.monotonic()))

    async def writer(self):
        try:
            while True:
                typ, payload, tq = await self.q.get()
                self.qbytes -= len(payload)
                wait = time.monotonic() - tq
                if wait > 0.5:
                    self.node.ev('qwait', self.name, typ, round(wait, 3))
                self.w.write(HDR.pack(len(payload), typ, now_ns()) + payload)
                await asyncio.wait_for(self.w.drain(), 30)
        except Exception:
            self.w.close()


class Node:
    def __init__(self, a):
        self.a = a
        self.nodes = a.nodes.split(',')
        self.me = self.nodes.index(a.name)
        self.peers = {}            # nom -> Peer
        self.seen = {}             # id -> slot
        self.store = {}            # slot -> charge bloc (sans en-tête de lien)
        self.txseen = set()
        os.makedirs(a.out, exist_ok=True)
        o = lambda k: open(os.path.join(a.out, f'{k}-{a.name}.csv'), 'x', buffering=1)
        self.fblk, self.ftx, self.fclk, self.fev = o('blocks'), o('tx'), o('clock'), o('events')
        self.fblk.write('slot,origin,size,send_ns,write_ns,recv_ns,hops,from,kind,first\n')
        self.ftx.write('origin,send_ns,write_ns,recv_ns,from\n')
        self.fclk.write('peer,t1,t2,t3,t4\n')
        self.end = a.t0 + a.duration
        self.last_rx = {}

    def ev(self, *f):
        self.fev.write(','.join(str(x) for x in (now_ns(),) + f) + '\n')

    def flood(self, typ, payload, exclude=None):
        for n, p in list(self.peers.items()):
            if n != exclude:
                p.put(typ, payload)

    async def readframe(self, r):
        n, t, wns = HDR.unpack(await r.readexactly(HDR.size))
        return t, wns, await r.readexactly(n)

    async def handle(self, r, w, peer=None):
        me = None
        try:
            if peer is None:                       # entrant : attendre HELLO
                t, _, p = await self.readframe(r)
                peer = p.decode()
            else:
                w.write(HDR.pack(len(self.a.name), T_HELLO, now_ns()) + self.a.name.encode())
            old = self.peers.get(peer)
            if old is not None:
                old.w.close()
            me = self.peers[peer] = Peer(self, peer, w)
            self.last_rx[peer] = time.monotonic()
            self.ev('connect', peer)
            # rattrapage par inventaire : j'annonce les créneaux que je possède dans la fenêtre
            lo = max(0, self.cur_slot() - KEEP_SLOTS)
            have = sorted(s for s in self.store if s >= lo)
            me.put(T_INV, struct.pack(f'>QI{len(have)}Q', lo, len(have), *have))
            while True:
                t, wns, p = await self.readframe(r)
                trecv = now_ns()
                self.last_rx[peer] = time.monotonic()
                if t in (T_BLOCK, T_SYNCBLK):
                    self.on_block(p, wns, trecv, peer, 'sync' if t == T_SYNCBLK else 'live')
                elif t == T_TX:
                    self.on_tx(p, wns, trecv, peer)
                elif t == T_PING:
                    t1, = struct.unpack('>q', p)
                    me.put(T_PONG, struct.pack('>qqq', t1, trecv, now_ns()))
                elif t == T_PONG:
                    t1, t2, t3 = struct.unpack('>qqq', p)
                    self.fclk.write(f'{peer},{t1},{t2},{t3},{trecv}\n')
                elif t == T_INV:
                    lo, k = struct.unpack_from('>QI', p)
                    have = set(struct.unpack_from(f'>{k}Q', p, 12))
                    miss = [s for s in sorted(self.store) if s >= lo and s not in have]
                    self.ev('inv', peer, k, len(miss))
                    for s in miss:
                        me.put(T_SYNCBLK, self.store[s])
        except (asyncio.IncompleteReadError, ConnectionError, OSError):
            pass
        finally:
            if peer and me is not None and self.peers.get(peer) is me:
                del self.peers[peer]
                me.task.cancel()
                self.ev('disconnect', peer)
            w.close()

    def on_block(self, p, wns, trecv, peer, kind):
        bid, slot, sns, org, hops = BLK.unpack_from(p)
        first = bid not in self.seen
        self.fblk.write(f'{slot},{self.nodes[org]},{len(p)},{sns},{wns},{trecv},{hops + 1},{peer},{kind},{int(first)}\n')
        if not first:
            return
        self.seen[bid] = slot
        fwd = bytearray(p)
        BLK.pack_into(fwd, 0, bid, slot, sns, org, min(hops + 1, 255))
        fwd = bytes(fwd)
        self.store[slot] = fwd
        self.flood(T_BLOCK, fwd, exclude=peer)

    def on_tx(self, p, wns, trecv, peer):
        tid, sns, org = TXH.unpack_from(p)
        if tid in self.txseen:
            return
        self.txseen.add(tid)
        if random.random() < 0.05:                 # échantillon
            self.ftx.write(f'{self.nodes[org]},{sns},{wns},{trecv},{peer}\n')
        self.flood(T_TX, p, exclude=peer)

    def cur_slot(self):
        return int((time.time() - self.a.t0) // self.a.cadence)

    async def producer(self):
        rnd = random.Random(self.me * 7919 + int(self.a.t0))
        while time.time() < self.end:
            s = self.cur_slot() + 1
            await asyncio.sleep(max(0, self.a.t0 + s * self.a.cadence - time.time()))
            if s % len(self.nodes) != self.me or s < 0:
                continue
            u, size, acc = rnd.random(), SIZES[-1][1], 0
            for pr, sz in (SIZES if not self.a.max_blocks else [(1.0, SIZES[-1][1])]):
                acc += pr
                if u < acc:
                    size = sz
                    break
            bid = os.urandom(16)
            body = os.urandom(size - BLK.size)
            sns = now_ns()
            p = BLK.pack(bid, s, sns, self.me, 0) + body
            self.seen[bid] = s
            self.store[s] = p
            self.fblk.write(f'{s},{self.a.name},{size},{sns},{sns},{sns},0,self,produced,1\n')
            self.flood(T_BLOCK, p)
            lag = (time.time() - (self.a.t0 + s * self.a.cadence))
            if lag > 0.05:
                self.ev('late_produce', s, round(lag, 3))
            for k in [k for k in self.store if k < s - KEEP_SLOTS]:
                del self.store[k]
            if len(self.seen) > 40000:
                self.seen = {k: v for k, v in self.seen.items() if v >= s - KEEP_SLOTS}

    async def txload(self):
        while time.time() < self.end:
            await asyncio.sleep(random.expovariate(self.a.tx_rate))
            tid = os.urandom(16)
            self.txseen.add(tid)
            self.flood(T_TX, TXH.pack(tid, now_ns(), self.me) + os.urandom(3072 - TXH.size))
            if len(self.txseen) > 400000:
                self.txseen = set()

    async def pinger(self):
        while time.time() < self.end:
            await asyncio.sleep(2)
            for n, p in list(self.peers.items()):
                if time.monotonic() - self.last_rx.get(n, 0) > 10:   # pair muet : couper
                    self.ev('timeout', n)
                    p.w.close()
                    continue
                p.put(T_PING, struct.pack('>q', now_ns()))

    async def dialer(self, name, host, port):
        while time.time() < self.end:
            if name not in self.peers:
                try:
                    r, w = await asyncio.wait_for(asyncio.open_connection(host, port), 5)
                    asyncio.create_task(self.handle(r, w, peer=name))
                except Exception:
                    pass
            await asyncio.sleep(1)

    async def main(self):
        if self.a.listen:
            await asyncio.start_server(lambda r, w: self.handle(r, w), '0.0.0.0', self.a.listen)
        for spec in filter(None, self.a.peers.split(',')):
            name, addr = spec.split('=')
            host, port = addr.rsplit(':', 1)
            asyncio.create_task(self.dialer(name, host, int(port)))
        self.ev('start', json.dumps(vars(self.a)).replace(',', ';'))
        await asyncio.gather(self.producer(), self.txload(), self.pinger())
        self.ev('end')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True)
    ap.add_argument('--nodes', required=True)
    ap.add_argument('--listen', type=int, default=0)
    ap.add_argument('--peers', default='')
    ap.add_argument('--t0', type=float, required=True)
    ap.add_argument('--duration', type=float, required=True)
    ap.add_argument('--cadence', type=float, default=0.5)
    ap.add_argument('--tx-rate', type=float, default=32.0)
    ap.add_argument('--max-blocks', action='store_true', help='tous les blocs à la taille maximale consensus')
    ap.add_argument('--out', required=True)
    asyncio.run(Node(ap.parse_args()).main())
