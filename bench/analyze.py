#!/usr/bin/env python3
"""Analyse du banc réseau N.  analyze.py DATA_DIR [--dval-ms X] > rapport.md ; écrit aussi DATA_DIR/summary.json

DATA_DIR/<phase>/{blocks,clock,events,tx}-<nœud>.csv, DATA_DIR/phases-<nœud>.log (tel que produit par run-host.sh).

Quantités (ms) :
  L_raw   = recv_local − send_local(origine)       # ce que voit le protocole : horloges locales, réseau, files
  D_corr  = L_raw + θ(origine − récepteur)          # retard corrigé de l'offset estimé (incertitude ±δmin/2)
  link    = recv − write du dernier saut (réseau + noyau du lien, non corrigé)
Condition D=0 pour τ : L_h + h·Δ_val ≤ τ − 1000 ms   (signature au plus tard à +2 s, réservation suivante à τ + 1 s)
"""
import csv, glob, json, math, os, random, sys, bisect
from collections import defaultdict

QS = [0.5, 0.95, 0.99, 0.999]
TAUS = [4, 5, 6, 8, 10, 12]


def q(xs, p):
    if not xs:
        return float('nan')
    k = min(len(xs) - 1, max(0, math.ceil(p * len(xs)) - 1))
    return xs[k]


def qci(xs, p, z=1.96):
    """IC ~95 % d'un quantile par statistiques d'ordre (approx. binomiale normale)."""
    n = len(xs)
    if n == 0:
        return (float('nan'),) * 2
    lo = max(0, math.floor(n * p - z * math.sqrt(n * p * (1 - p))) - 1)
    hi = min(n - 1, math.ceil(n * p + z * math.sqrt(n * p * (1 - p))))
    return xs[lo], xs[hi]


def load_offsets(ph):
    """θ[(a,b)] : liste triée (t_ns, θ_ms = horloge b − horloge a, δmin_ms) par fenêtre de 60 s, vue depuis a pingant b."""
    out = {}
    for f in glob.glob(os.path.join(ph, 'clock-*.csv')):
        a = os.path.basename(f)[6:-4]
        win = defaultdict(list)
        for r in csv.DictReader(open(f)):
            t1, t2, t3, t4 = (int(r[k]) for k in ('t1', 't2', 't3', 't4'))
            d = ((t4 - t1) - (t3 - t2)) / 1e6
            th = ((t2 - t1) + (t3 - t4)) / 2e6
            win[(r['peer'], t1 // 60_000_000_000)].append((d, th, t1))
        per = defaultdict(list)
        for (b, w), v in win.items():
            d, th, t1 = min(v)
            per[(a, b)].append((t1, th, d))
        for k, v in per.items():
            out[k] = sorted(v)
    return out


def theta(offs, a, b, t):
    """θ = horloge b − horloge a à l'instant t (ms), et demi-δ comme incertitude."""
    if (a, b) in offs:
        v, s = offs[(a, b)], 1
    elif (b, a) in offs:
        v, s = offs[(b, a)], -1
    else:
        return None, None
    i = bisect.bisect_left(v, (t,))
    c = [v[j] for j in (i - 1, i) if 0 <= j < len(v)]
    t1, th, d = min(c, key=lambda x: abs(x[0] - t))
    return s * th, d / 2


def phase_stats(ph, cut_windows):
    offs = load_offsets(ph)
    nodes = [os.path.basename(f)[7:-4] for f in glob.glob(os.path.join(ph, 'blocks-*.csv'))]
    produced = {}
    first = {}                      # (recv, origin, slot) -> row
    for n in nodes:
        for r in csv.DictReader(open(os.path.join(ph, f'blocks-{n}.csv'))):
            key = (r['origin'], int(r['slot']))
            if r['kind'] == 'produced':
                produced[key] = int(r['size'])
            elif r['first'] == '1':
                first[(n,) + key] = r
    raw, corr, link, unc = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    bysize = defaultdict(list)
    in_cut = lambda t: any(a <= t <= b + 120e9 for a, b in cut_windows)
    excluded = 0
    for (n, org, slot), r in first.items():
        send, recv, wr = int(r['send_ns']), int(r['recv_ns']), int(r['write_ns'])
        if r['kind'] == 'sync' or in_cut(recv):
            excluded += 1
            continue
        L = (recv - send) / 1e6
        th, u = theta(offs, n, org, recv)
        d = (org, n)
        raw[d].append(L)
        if th is not None:
            corr[d].append(L + th)
            unc[d].append(u)
        link[d].append((recv - wr) / 1e6)
        bysize[(d, int(r['size']))].append(L)
    # complétude : chaque bloc produit reçu par chaque autre nœud ?
    missing = defaultdict(int)
    for (org, slot) in produced:
        for n in nodes:
            if n != org and (n, org, slot) not in first:
                missing[(org, n)] += 1
    res = {'dirs': {}, 'excluded_cut_or_sync': excluded, 'produced': len(produced)}
    for d in sorted(raw):
        xs, cs, ls = sorted(raw[d]), sorted(corr[d]), sorted(link[d])
        res['dirs'][f'{d[0]}->{d[1]}'] = {
            'n': len(xs), 'missing': missing[d],
            'raw': {f'p{p*100:g}': q(xs, p) for p in QS} | {'max': xs[-1], 'p99.9_ci': qci(xs, 0.999)},
            'corr': ({f'p{p*100:g}': q(cs, p) for p in QS} | {'max': cs[-1]}) if cs else None,
            'offset_unc_ms_median': q(sorted(unc[d]), 0.5) if unc[d] else None,
            'link': {f'p{p*100:g}': q(ls, p) for p in QS} | {'max': ls[-1]},
            'by_size_p99.9': {str(s): q(sorted(v), 0.999) for (dd, s), v in bysize.items() if dd == d},
            'by_size_max': {str(s): max(v) for (dd, s), v in bysize.items() if dd == d},
        }
    # offsets
    res['offsets'] = {}
    for (a, b), v in sorted(offs.items()):
        ths = sorted(abs(x[1]) for x in v)
        res['offsets'][f'{a}~{b}'] = {'windows': len(v), 'abs_theta_p50': q(ths, .5), 'abs_theta_p99': q(ths, .99),
                                      'abs_theta_max': ths[-1], 'theta_drift_ms': v[-1][1] - v[0][1],
                                      'delta_min_p50': q(sorted(x[2] for x in v), .5)}
    res['_raw'] = raw
    return res


def cuts_from_log(path):
    ws, st = [], None
    if not os.path.exists(path):
        return ws
    for line in open(path):
        p = line.split()
        if len(p) >= 2 and p[1] == 'cut_start':
            st = (int(p[0]), p[2], int(p[3]))
        elif len(p) >= 2 and p[1] == 'cut_end' and st:
            ws.append((st[0], int(p[0]), st[1], st[2]))
            st = None
    return ws


def catchup(ph, cuts, node='vps2'):
    """Pour chaque coupure : délai entre fin de coupure et réception du dernier bloc manquant produit pendant la coupure."""
    f = os.path.join(ph, f'blocks-{node}.csv')
    if not os.path.exists(f):
        return []
    rows = [r for r in csv.DictReader(open(f)) if r['first'] == '1' and r['kind'] != 'produced']
    out = []
    for a, b, mode, d in cuts:
        inside = [int(r['recv_ns']) for r in rows if a <= int(r['send_ns']) <= b]
        if inside:
            out.append({'mode': mode, 'dur_s': d, 'blocks': len(inside), 'catchup_s': (max(inside) - b) / 1e9})
    return out


def multihop(raw_all, dval, hmax=6, n=200000, seed=1):
    rnd = random.Random(seed)
    pool = [x for v in raw_all for x in v]
    if not pool:
        return {}
    out = {}
    for h in range(1, hmax + 1):
        s = sorted(sum(rnd.choice(pool) for _ in range(h)) + h * dval for _ in range(n))
        out[h] = {'p99': q(s, .99), 'p99.9': q(s, .999), 'p99.99': q(s, .9999), 'max': s[-1],
                  'viol': {t: sum(1 for x in s if x > t * 1000 - 1000) / n for t in TAUS}}
    return out


def main():
    data = sys.argv[1]
    dval = float(sys.argv[sys.argv.index('--dval-ms') + 1]) if '--dval-ms' in sys.argv else 0.0
    cuts = []
    for lg in glob.glob(os.path.join(data, 'phases-*.log')):
        cuts += cuts_from_log(lg)
    summ = {'dval_ms': dval, 'phases': {}}
    print(f'# Banc réseau N — résultats ({os.path.basename(os.path.abspath(data))})\n')
    print(f'Δ_val par saut utilisé pour la condition : {dval} ms. Quantiles en ms. « raw » = horloges locales (ce que voit le protocole).\n')
    for ph in sorted(os.path.dirname(f) for f in glob.glob(os.path.join(data, '*', 'blocks-vps1.csv'))):
        P = os.path.basename(ph)
        cw = [(a, b) for a, b, *_ in cuts]
        st = phase_stats(ph, cw)
        cu = catchup(ph, [c for c in cuts])
        raw = st.pop('_raw')
        mh = multihop([v for k, v in raw.items() if 'mac' not in k[0] and 'mac' not in k[1]] or list(raw.values()), dval)
        st['catchup'] = cu
        st['multihop_vps'] = mh
        summ['phases'][P] = st
        print(f'## {P}\n\nBlocs produits : {st["produced"]} ; exclus (rattrapage ou ≤ 120 s après coupure) : {st["excluded_cut_or_sync"]}.\n')
        print('| sens | n | manquants | p50 | p95 | p99 | p99.9 [IC95] | max | p99.9 corrigé | ±offset | lien p99.9 |')
        print('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
        for d, v in st['dirs'].items():
            r, c = v['raw'], v['corr'] or {}
            ci = r['p99.9_ci']
            print(f"| {d} | {v['n']} | {v['missing']} | {r['p50']:.1f} | {r['p95']:.1f} | {r['p99']:.1f} | "
                  f"{r['p99.9']:.1f} [{ci[0]:.0f}–{ci[1]:.0f}] | {r['max']:.0f} | {c.get('p99.9', float('nan')):.1f} | "
                  f"{(v['offset_unc_ms_median'] or float('nan')):.2f} | {v['link']['p99.9']:.1f} |")
        print('\n| paire | fenêtres | \\|θ\\| p50 | \\|θ\\| p99 | \\|θ\\| max | dérive θ | δmin p50 |')
        print('|---|---:|---:|---:|---:|---:|---:|')
        for k, v in st['offsets'].items():
            print(f"| {k} | {v['windows']} | {v['abs_theta_p50']:.2f} | {v['abs_theta_p99']:.2f} | {v['abs_theta_max']:.2f} | "
                  f"{v['theta_drift_ms']:.2f} | {v['delta_min_p50']:.1f} |")
        if cu:
            print('\n| coupure | durée (s) | blocs pendant | rattrapage après fin (s) |')
            print('|---|---:|---:|---:|')
            for c in cu:
                print(f"| {c['mode']} | {c['dur_s']} | {c['blocks']} | {c['catchup_s']:.2f} |")
        if mh:
            print(f'\nMulti-sauts (VPS↔VPS, tirages indépendants, + h·Δ_val) — fraction de blocs violant D=0 :\n')
            print('| sauts | p99.9 | p99.99 | ' + ' | '.join(f'τ={t}s' for t in TAUS) + ' |')
            print('|---:|---:|---:|' + '---:|' * len(TAUS))
            for h, v in mh.items():
                print(f"| {h} | {v['p99.9']:.0f} | {v['p99.99']:.0f} | " + ' | '.join(f"{v['viol'][t]:.1e}" for t in TAUS) + ' |')
        print()
    json.dump(summ, open(os.path.join(data, 'summary.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
