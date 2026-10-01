#!/usr/bin/env python3
"""Micro-banc de validation N (Δ_val) : ML-DSA-44 (pqcrypto, liaison Rust/PQClean), SHAKE256 loterie, hachages du corps.
Borne haute d'un bloc : 1 vérification d'en-tête + floor(262144/2420)=108 signatures ML-DSA dans le corps
(une signature par 2 420 octets est le maximum physique) + hachage du corps + loterie. N'inclut PAS l'accès à l'état (UTXO, registre) :
voir la mesure « connect block » du démon actuel, rapportée séparément."""
import hashlib, os, statistics, time, json, platform
from pqcrypto.sign import ml_dsa_44 as m

def bench(f, n):
    ts = []
    for _ in range(n):
        t = time.perf_counter_ns(); f(); ts.append(time.perf_counter_ns() - t)
    ts.sort()
    return {'p50_us': ts[n // 2] / 1e3, 'p99_us': ts[int(n * .99)] / 1e3, 'max_us': ts[-1] / 1e3}

pk, sk = m.keygen()
hdr = os.urandom(400); sig = m.sign(sk, hdr, context=b'N/BLOCK/SIG')
body = os.urandom(262144)
seed = os.urandom(32)
r = {'host': platform.node(), 'cpu': platform.processor() or platform.machine(), 'sig_size': len(sig)}
r['mldsa44_verify'] = bench(lambda: m.verify(pk, hdr, sig, context=b'N/BLOCK/SIG'), 3000)
r['mldsa44_sign'] = bench(lambda: m.sign(sk, hdr, context=b'N/BLOCK/SIG'), 500)
r['shake256_lottery_64B'] = bench(lambda: hashlib.shake_256(b'N/LOTTERY' + seed + os.urandom(8)).digest(64), 20000)
r['sha256_body_256KiB'] = bench(lambda: hashlib.sha256(body).digest(), 500)
r['shake256_body_256KiB'] = bench(lambda: hashlib.shake_256(body).digest(32), 500)
nsig = 262144 // 2420
v = r['mldsa44_verify']['p99_us']
r['block_upper_ms'] = (v * (nsig + 1) + r['sha256_body_256KiB']['p99_us'] * 2 + r['shake256_lottery_64B']['p99_us']) / 1e3
r['note'] = f'borne = (1+{nsig}) vérifs p99 + 2 hachages corps p99 + loterie ; hors accès état'
print(json.dumps(r, indent=1))
