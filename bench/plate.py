#!/usr/bin/env python3
"""p_late(τ, sauts) à partir des livraisons mesurées (r2, blocs max, VPS↔VPS, horloges locales brutes).
Chemin de h sauts = somme de h tirages indépendants + h·Δ_val (conservateur : un seul chemin, pas de minimum entre chemins).
Borne haute 95 % (Clopper-Pearson) quand le nombre d'excès est faible. Condition D=0 : L_h ≤ τ − 1000 ms."""
import csv, glob, math, random, sys, json
D = sys.argv[1]; DVAL = float(sys.argv[2]) if len(sys.argv) > 2 else 100
def load(prefix):
    xs = []
    for f in glob.glob(f'{D}/{prefix}*/blocks-*.csv'):
        for r in csv.DictReader(open(f)):
            if r['first'] == '1' and r['kind'] == 'live':
                xs.append((int(r['recv_ns']) - int(r['send_ns'])) / 1e6)
    return xs
def cp_upper(k, n, a=0.05):
    # borne supérieure de Clopper-Pearson par bissection sur la binomiale
    if k >= n: return 1.0
    lo, hi = k / n, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        cdf = sum(math.comb(n, i) * m**i * (1 - m)**(n - i) for i in range(k + 1))
        lo, hi = (m, hi) if cdf > a else (lo, m)
    return hi
out = {}
rnd = random.Random(7)
for prof in ['W1', 'W2']:
    xs = load(prof); n = len(xs)
    for h in (1, 2, 3):
        for tau in (6, 8, 10, 12):
            lim = tau * 1000 - 1000
            if h == 1:
                k = sum(1 for x in xs if x + DVAL > lim); p = k / n; ub = cp_upper(k, n); nn = n
            else:
                N = 200000
                s = [sum(rnd.choice(xs) for _ in range(h)) + h * DVAL for _ in range(N)]
                k = sum(1 for x in s if x > lim); p = k / N; ub = None; nn = N
            out[f'{prof} h={h} tau={tau}'] = (p, ub, n)
            print(f'{prof} n={n} h={h} τ={tau:>2}s  p_late={p:.2e}' + (f'  (borne 95 % {ub:.1e}, k={k})' if ub is not None else ''))
json.dump(out, open(f'{D}/plate-dval{int(DVAL)}.json', 'w'), indent=1)
