#!/usr/bin/env python3
"""CP_reg -- simulation Monte-Carlo indépendante (seconde analyse, auteur: opus).

Python 3 standard, sans dépendance. Graine fixée. multiprocessing.

Modèle (un producteur par créneau, tirage public, calendrier connu d'avance) :
  créneau adverse   : prob beta          (l'adversaire est toujours en ligne)
  créneau honnête   : prob (1-beta)*d    (d = fraction du poids honnête en ligne)
  créneau vide      : le reste           (honnête hors ligne ; aucun remplaçant)
Retard : un bloc honnête du créneau s est vu par les honnêtes à partir du
créneau s+D+1 (D créneaux aveugles ; l'adversaire retarde AU MAXIMUM tout bloc
honnête). Longueur d'un bloc honnête : L(s) = 1 + max{L(s') : s' <= s-D-1}.
Vue la plus faible d'un honnête à l'instant t : V(t) = max{L(s') : s' <= t-D}.

Adversaire STRATÉGIQUE (omniscient sur le calendrier, arrêt optimal) :
  - retient TOUS ses blocs (rien de public) ;
  - choisit a posteriori-a priori (calendrier public) le point de départ f de
    sa branche privée parmi TOUS les blocs honnêtes antérieurs à la cible (ou
    genesis) : c'est « attendre la séquence favorable », avance accumulée ;
  - choisit l'instant de révélation t >= cible ;
  - équivoque / départage : mode 'tie' = une égalité de longueur suffit
    (équivoque => ex aequo persistant, ou départage public choisi favorable) ;
    mode 'strict' = il faut dépasser strictement.
  Réussite contre la cible s (coupure de cliché) à l'instant t :
      L(f) + #A(f,t]  >=  V(t)      (tie)    ou  >= V(t)+1 (strict)
Adversaire NAÏF de comparaison (course §15, avance nulle) : part du bout public
juste avant s, sans avance, même règle d'égalité.

Mesures par cible : dernier t de réussite ; profondeur de réorganisation en
créneaux (t-s), en créneaux non vides, en blocs de la vue victime (V(t)-V(s-1)).
eps(K) = P(profondeur >= K) = P(préfixe strictement antérieur à la coupure
divergent pour au moins un honnête, K créneaux / blocs après la coupure).

Usage : python3 cp_sim.py [--quick]
"""
import bisect
import math
import os
import random
import sys
import time
from multiprocessing import Pool

MASTER_SEED = 20260930
GRID = [(b, D, d) for b in (0.10, 0.20, 0.25) for D in (0, 1) for d in (1.0, 0.4)]
GRID += [(0.20, 0, 0.7), (0.20, 1, 0.7)]   # point de référence du mandat
MODES = ("omni_tie", "omni_strict", "naive_tie")
METRICS = ("slots", "blocks", "nonempty")


def one_trial(args):
    beta, D, d, seed, T, warm, tail = args
    rng = random.Random(seed)
    h = (1.0 - beta) * d
    lim_h = beta + h
    rnd = rng.random
    typ = [0] * T  # 0 vide, 1 adverse, 2 honnête
    for i in range(T):
        r = rnd()
        typ[i] = 1 if r < beta else (2 if r < lim_h else 0)
    X = [0] * T      # nb de créneaux adverses <= t
    PM = [0] * T     # max L honnête sur créneaux <= t
    NE = [0] * T     # nb de créneaux non vides <= t
    Fv = [0] * T     # max_{f honnête <= t} L(f) - X(f)  (genesis : 0)
    x = pm = ne = 0
    fv = 0
    for t in range(T):
        ty = typ[t]
        if ty == 1:
            x += 1
            ne += 1
        elif ty == 2:
            j = t - D - 1
            L = 1 + (PM[j] if j >= 0 else 0)
            if L > pm:
                pm = L
            v = L - x
            if v > fv:
                fv = v
            ne += 1
        X[t] = x
        PM[t] = pm
        NE[t] = ne
        Fv[t] = fv
    # V(t) = PM[t-D]
    Z = [0] * T
    for t in range(T):
        j = t - D
        Z[t] = X[t] - (PM[j] if j >= 0 else 0)
    # suffixe max de Z, rendu croissant par négation pour bisect
    neg = [0] * T
    m = -10 ** 9
    for t in range(T - 1, -1, -1):
        if Z[t] > m:
            m = Z[t]
        neg[t] = -m
    # neg est croissant en t
    hist = {mo: {me: {} for me in METRICS} for mo in MODES}
    late = 0
    n_targets = 0
    s_end = T - tail
    for s in range(warm, s_end):
        n_targets += 1
        # valeur de départ omnisciente : meilleur point de fork strictement avant s
        mo_val = Fv[s - 1]
        jv = s - 1 - D
        vprev = PM[jv] if jv >= 0 else 0
        naive_val = vprev - X[s - 1]
        for mo, base, need in (("omni_tie", mo_val, 0), ("omni_strict", mo_val, 1),
                               ("naive_tie", naive_val, 0)):
            # plus grand t >= s avec base + Z[t] >= need  <=>  SM[t] >= need-base
            thr = need - base          # on cherche SM[t] >= thr <=> neg[t] <= -thr
            k = bisect.bisect_right(neg, -thr) - 1
            if k < s:
                continue
            if k >= T - 50:
                late += 1
            j = k - D
            vt = PM[j] if j >= 0 else 0
            for me, val in (("slots", k - s), ("blocks", vt - vprev),
                            ("nonempty", NE[k] - NE[s - 1])):
                hh = hist[mo][me]
                hh[val] = hh.get(val, 0) + 1
    return n_targets, hist, late


def merge(acc, part):
    for mo in part:
        for me in part[mo]:
            a = acc[mo][me]
            for k, v in part[mo][me].items():
                a[k] = a.get(k, 0) + v


def tail_counts(h):
    """h: {profondeur: nb} -> liste triée (K, nb de cibles de profondeur >= K)."""
    ks = sorted(h)
    out = []
    c = 0
    for k in reversed(ks):
        c += h[k]
        out.append((k, c))
    return list(reversed(out))


def eps_at(tc, K, n):
    # nb de cibles de profondeur >= K
    for k, c in tc:
        if k >= K:
            return c / n
    return 0.0


def fit_rate(tc, n, lo_eps=3e-3, min_count=30):
    """Pente de log eps(K) sur la queue mesurable (eps <= lo_eps, >= min_count cibles)."""
    pts = [(k, c / n) for k, c in tc if c / n <= lo_eps and c >= min_count]
    if len(pts) < 5:
        return None
    xs = [p[0] for p in pts]
    ys = [math.log(p[1]) for p in pts]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((a - mx) ** 2 for a in xs)
    if sxx == 0:
        return None
    sl = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sxx
    return sl, my - sl * mx


def main():
    quick = "--quick" in sys.argv
    ncpu = min(14, os.cpu_count() or 1)
    T, warm, tail = (60000, 10000, 20000) if quick else (300000, 20000, 60000)
    ntr = 4 if quick else 110  # essais par configuration
    t0 = time.time()
    jobs = []
    for ci, (beta, D, d) in enumerate(GRID):
        for i in range(ntr):
            seed = MASTER_SEED * 1000003 + ci * 10007 + i
            jobs.append((ci, (beta, D, d, seed, T, warm, tail)))
    acc = {ci: {mo: {me: {} for me in METRICS} for mo in MODES} for ci in range(len(GRID))}
    ntar = {ci: 0 for ci in range(len(GRID))}
    per_trial = {ci: [] for ci in range(len(GRID))}
    late = {ci: 0 for ci in range(len(GRID))}
    with Pool(ncpu) as pool:
        for (ci, _), (n, hist, lt) in zip(jobs, pool.imap(one_trial, [j[1] for j in jobs], chunksize=1)):
            merge(acc[ci], hist)
            ntar[ci] += n
            late[ci] += lt
            per_trial[ci].append((n, hist))
    wall = time.time() - t0
    write_md(acc, ntar, per_trial, late, wall, T, warm, tail, ntr, ncpu, quick)


KGRID_SLOTS = [50, 100, 200, 300, 500, 800, 1000, 1500, 2000, 3000, 4000, 5000, 7200]
KGRID_BLOCKS = [20, 50, 100, 150, 200, 300, 500, 800, 1000, 1500, 2000, 2880]


def write_md(acc, ntar, per_trial, late, wall, T, warm, tail, ntr, ncpu, quick):
    L = []
    L.append("# CP_reg — résultats Monte-Carlo (opus, `cp_sim.py`)\n")
    L.append(f"Graine maîtresse `{MASTER_SEED}` ; {ntr} essais × {T} créneaux par configuration "
             f"(chauffe {warm}, queue {tail}) ; cibles = chaque créneau de [chauffe, T−queue) ; "
             f"{ncpu} processus ; durée murale {wall:.0f} s.{' MODE RAPIDE.' if quick else ''}\n")
    L.append("Les cibles d'un même essai sont corrélées : l'incertitude est donnée par la "
             "dispersion entre essais (σ des moyennes par essai). « 0 » = aucun événement ; "
             "la résolution est ~1/(nb de cibles) mais l'information effective est bien moindre.\n")
    L.append("Modes : `omni_tie` = adversaire omniscient (départ + révélation optimaux, égalité "
             "gagnée par équivoque/départage) ; `omni_strict` = idem, dépassement strict exigé ; "
             "`naive_tie` = course sans avance partant de la cible (référence §15).\n")
    for ci, (beta, D, d) in enumerate(GRID):
        n = ntar[ci]
        L.append(f"\n## β = {beta}, D = {D} (Δ/τ = {'0' if D == 0 else '1'}), densité honnête d = {d}\n")
        L.append(f"Cibles : {n:,} ; révélations tardives en fin d'essai (biais de troncature) : {late[ci]}.\n")
        if late[ci] > 0.01 * n:
            L.append("**RÉGIME NON SÛR** : la branche privée rattrape la vue honnête jusqu'à la fin de "
                     "presque tous les essais (β ≥ taux de croissance honnête sous retard maximal). "
                     "ε(K) ≈ 1 pour tout K ; aucune profondeur ne suffit.\n")
            continue
        for me, grid in (("slots", KGRID_SLOTS), ("blocks", KGRID_BLOCKS)):
            L.append(f"\nε(K) — K en **{'créneaux' if me == 'slots' else 'blocs (vue victime)'}**\n")
            L.append("| mode | " + " | ".join(str(k) for k in grid) + " |")
            L.append("|---|" + "---|" * len(grid))
            for mo in MODES:
                tc = tail_counts(acc[ci][mo][me])
                L.append(f"| {mo} | " + " | ".join(
                    (f"{eps_at(tc, k, n):.2e}" if eps_at(tc, k, n) > 0 else "0") for k in grid) + " |")
        L.append("\nQueue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :\n")
        L.append("| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |")
        L.append("|---|---|---|---|---|---|---|")
        for mo in MODES:
            for me in ("slots", "blocks", "nonempty"):
                tc = tail_counts(acc[ci][mo][me])
                k3 = next((k for k, c in tc if c / n <= 1e-3), None)
                k6m = next((k for k, c in tc if c / n <= 1e-6), None)
                fr = fit_rate(tc, n)
                if fr:
                    sl, ic = fr
                    ext = lambda e: int(math.ceil((math.log(e) - ic) / sl))
                    L.append(f"| {mo} | {me} | {sl:.4g} | {k3} | {k6m} (ext {ext(1e-6)}) | {ext(1e-9)} | {ext(1e-12)} |")
                else:
                    L.append(f"| {mo} | {me} | — | {k3} | {k6m} | — | — |")
        # dispersion entre essais à un K de référence
        ref = 1000 if d == 1.0 else 3000
        vals = []
        for (nn, hist) in per_trial[ci]:
            tc = tail_counts(hist["omni_tie"]["slots"])
            vals.append(eps_at(tc, ref, nn))
        m = sum(vals) / len(vals)
        sd = (sum((v - m) ** 2 for v in vals) / max(1, len(vals) - 1)) ** 0.5 / len(vals) ** 0.5
        L.append(f"\nContrôle de dispersion : ε_omni_tie({ref} créneaux) = {m:.3e} ± {sd:.1e} (σ entre essais).\n")
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "resultats.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
