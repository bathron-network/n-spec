#!/usr/bin/env python3
"""Seuils de densité de livraison du profil H_N (N-SPEC v0.7 §14.2).

Calculs binomiaux exacts (log-gamma + fsum ; DP numpy pour la fenêtre
« depuis l'inclusion »). Aucune simulation. Coin du profil B :
beta = 0.30, d = 0.70, p_late = 1e-2 => h = 0.49, h' = h(1-p_late) = 0.4851,
a = beta + h p_late = 0.3049.
"""
import math, json, sys
from fractions import Fraction as F
import numpy as np

BETA, D, PLATE = 0.30, 0.70, 1e-2
H = (1 - BETA) * D
HP = H * (1 - PLATE)          # densité honnête publique (adversaire abstentionniste)
A = BETA + H * PLATE          # densité max d'une branche adverse, retards comptés

def logpmf(n, k, p):
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
            + k * math.log(p) + (n - k) * math.log1p(-p))

def tail_ge(n, k0, p):        # P[Bin(n,p) >= k0]
    k0 = max(k0, 0)
    if k0 > n: return 0.0
    return math.fsum(math.exp(logpmf(n, k, p)) for k in range(k0, n + 1))

def kmin(rho, w):             # plus petit filled tel que den*filled >= num*w
    r = F(rho).limit_denominator(1000)
    return -(-(r.numerator * w) // r.denominator)

def tail_lt(n, k1, p):        # P[Bin(n,p) < k1], somme directe (pas de 1 - x)
    return math.fsum(math.exp(logpmf(n, k, p)) for k in range(0, min(k1, n + 1)))

def fausse_suspension(rho, w, p=HP):   # P[Bin(w,h') < rho w]
    return tail_lt(w, kmin(rho, w), p)

def fausse_livraison(rho, w, p=A):     # P[Bin(w,a) >= rho w]
    return tail_ge(w, kmin(rho, w), p)

def incl_fausse_livraison(rho, depth, p=A, nmax=None):
    """P[exists n : S_n >= depth et den*S_n >= num*n], S_n ~ marche de Bernoulli(p)
    sur les créneaux depuis l'inclusion (créneau d'inclusion rempli : S_1 = 1).
    Borne supérieure de la fausse livraison par la seule fenêtre depuis
    l'inclusion + profondeur (les fenêtres 100/1000 l'abaissent encore)."""
    r = F(rho).limit_denominator(1000)
    if nmax is None:
        nmax = int(depth / rho * 4) + 2000
    dist = np.zeros(nmax + 2); dist[1] = 1.0   # n = 1
    hit = 0.0
    for n in range(1, nmax + 1):
        if n > 1:
            new = dist * (1 - p); new[1:] += dist[:-1] * p; dist = new
        lo = max(depth, -(-(r.numerator * n) // r.denominator))
        if lo <= n:
            hit += dist[lo:].sum(); dist[lo:] = 0.0
    return hit, float(dist.sum())          # (proba, masse restante non absorbée)

def incl_fausse_suspension(rho, depth, p=HP):
    """P[au premier instant de profondeur `depth`, densité depuis l'inclusion < rho]
    = P[T_depth > floor(depth/rho)] = P[Bin(m-1, p) < depth-1], m = floor(depth/rho)
    (le créneau d'inclusion est rempli)."""
    r = F(rho).limit_denominator(1000)
    m = (depth * r.denominator) // r.numerator
    return tail_lt(m - 1, depth - 1, p)

def incl_suspendu_a(rho, n, p=HP):
    """P[densité depuis l'inclusion < rho après n créneaux] (S_1 = 1)."""
    return tail_lt(n - 1, kmin(rho, n) - 1, p)

if __name__ == '__main__':
    out = {'h': H, 'h_prime': HP, 'a': A, 'windows': {}, 'inclusion': {}}
    rhos = [0.30, 0.35, 0.37, 0.38, 0.40, 0.42, 0.43, 0.45, 0.47, 0.70]
    print(f"h={H:.4f} h'={HP:.4f} a={A:.4f}")
    for w in (100, 1000):
        print(f"\nW={w}: rho  kmin  FS(h')  FL(a)  FL(beta=0.30)")
        out['windows'][w] = {}
        for rho in rhos:
            fs, fl, flb = fausse_suspension(rho, w), fausse_livraison(rho, w), fausse_livraison(rho, w, BETA)
            out['windows'][w][rho] = dict(kmin=kmin(rho, w), FS=fs, FL=fl, FL_beta=flb)
            print(f"  {rho:.2f} {kmin(rho,w):5d}  {fs:.3e}  {fl:.3e}  {flb:.3e}")
    for depth in (77, 739, 1123):
        print(f"\nDepuis l'inclusion, profondeur {depth}: rho FS(h') FL(a) reste")
        out['inclusion'][depth] = {}
        for rho in rhos:
            fs = incl_fausse_suspension(rho, depth)
            fl, rest = incl_fausse_livraison(rho, depth)
            out['inclusion'][depth][rho] = dict(FS=fs, FL=fl, unabsorbed=rest)
            print(f"  {rho:.2f}  {fs:.3e}  {fl:.3e}  {rest:.1e}")
    print("\nRetard (honnête, h') : P[densité depuis l'inclusion < rho] après n créneaux")
    out['inclusion_delay'] = {}
    for rho in (0.40, 0.42, 0.43, 0.45):
        row = {n: incl_suspendu_a(rho, n) for n in (159, 200, 300, 500, 1000, 2000)}
        out['inclusion_delay'][rho] = row
        print(f"  {rho:.2f} " + "  ".join(f"n={n}:{v:.2e}" for n, v in row.items()))
    print("\nConvergence FL depuis l'inclusion (nmax doublé)")
    for depth, rho in ((77, 0.40), (77, 0.43), (77, 0.45), (739, 0.43)):
        a1, _ = incl_fausse_livraison(rho, depth)
        a2, _ = incl_fausse_livraison(rho, depth, nmax=2 * (int(depth / rho * 4) + 2000))
        print(f"  N={depth} rho={rho}: {a1:.6e} vs {a2:.6e}")
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'seuils.json', 'w'), indent=1)
