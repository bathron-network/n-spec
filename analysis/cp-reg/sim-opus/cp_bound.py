#!/usr/bin/env python3
"""CP_reg -- calcul analytique (seconde analyse, auteur: opus).

Borne de préfixe commun pour une loterie à UN producteur par créneau, calendrier
public, adversaire omniscient (connaît toute la chaîne caractéristique),
rétention, équivoque et départage favorable à l'adversaire.

Méthode : chaîne de Markov exacte sur (horloge, reach rho, marge mu) selon les
récurrences de Blum-Kiayias-Moore-Quader-Russell (SODA 2020) :
    A : rho+1, mu+1
    h : rho <- max(rho-1,0) ; mu <- 0 si (mu==0 et rho>0) sinon mu-1
    vide : inchangé
rho initial = loi stationnaire du reach (avance privée accumulée sur TOUT le
passé : c'est ici qu'entrent rétention + choix du moment) ; mu_0 = rho_0.
eps(k) = P(il existe t >= k : mu_t >= 0)  (violation « pour toujours après »).

Retard Delta : D = créneaux aveugles après un bloc honnête (D=0 si Delta<=5 s
avec les phases §7.2).  Réduction gloutonne : un créneau honnête est « glouton »
(h) s'il arrive > D créneaux après le dernier glouton ; sinon il est
    mode 'pess' : compté A  (borne prouvable, réduction de type Praos)
    mode 'opt'  : ignoré    (estimation : blocs honnêtes non gloutons inutiles
                             à l'adversaire ; PAS une borne)
Deux niveaux : 'slot' (eps en créneaux) et 'sym' (eps en créneaux non vides,
ce qui borne l'erreur d'une règle de confirmation en BLOCS : k blocs au-dessus
de la cible occupent k créneaux non vides distincts, équivoque comprise).

Toutes les troncatures sont conservatrices (masse tronquée = échec).
Usage : python3 cp_bound.py [--out table.json]
"""
import json
import math
import sys
import time
from multiprocessing import Pool

import numpy as np

TARGETS = [1e-6, 1e-9, 1e-12]
STOP_EPS = 1e-13


def rates(beta, d, D, mode):
    a = beta
    h = (1.0 - beta) * d
    g = h / (1.0 + h * D)          # taux des honnêtes gloutons
    q = a + (h - g if mode == "pess" else 0.0)
    return a, h, g, q


def kernel(beta, d, D, mode, level):
    a = beta
    h = (1.0 - beta) * d
    e = 1.0 - a - h
    u = a + h
    F = D + 1
    ng = "A" if mode == "pess" else "n"
    trans = []
    for c in range(D + 2):
        lst = []
        if level == "slot":
            c2 = F if (c == F or c + 1 > D) else c + 1
            if c2 == F:
                lst.append((0, "h", h))
            else:
                lst.append((c2, ng, h))
            lst.append((c2, "A", a))
            lst.append((c2, "n", e))
        else:
            if c == F:
                gaps = [(F, 1.0)]
            else:
                gaps = [(c + g, u * (1 - u) ** (g - 1)) for g in range(1, D - c + 1)]
                gaps.append((F, (1 - u) ** (D - c)))
            for c2, pg in gaps:
                if c2 == F:
                    lst.append((0, "h", pg * h / u))
                else:
                    lst.append((c2, ng, pg * h / u))
                lst.append((c2, "A", pg * a / u))
        # fusion
        m = {}
        for c2, act, p in lst:
            if p > 0:
                m[(c2, act)] = m.get((c2, act), 0.0) + p
        trans.append([(c2, act, p) for (c2, act), p in m.items()])
    return trans


def stationary_reach(trans_slot, C, R):
    """Loi stationnaire de (horloge, rho), rho plafonné à R (masse en R = échec)."""
    n = C * R + C  # rho in 0..R
    T = np.zeros((C * (R + 1), C * (R + 1)))
    idx = lambda c, r: c * (R + 1) + r
    for c in range(C):
        for c2, act, p in trans_slot[c]:
            for r in range(R + 1):
                if act == "A":
                    r2 = min(r + 1, R)
                elif act == "h":
                    r2 = max(r - 1, 0)
                else:
                    r2 = r
                T[idx(c, r), idx(c2, r2)] += p
    # pi (T - I) = 0, sum pi = 1
    A = (T - np.eye(T.shape[0])).T
    A[-1, :] = 1.0
    b = np.zeros(T.shape[0])
    b[-1] = 1.0
    pi = np.linalg.solve(A, b)
    pi = np.clip(pi, 0, None)
    pi /= pi.sum()
    return pi.reshape(C, R + 1)


def return_probs(trans, C, Mn):
    """ret[c, j] = P(mu atteint 0 un jour | mu = j - Mn < 0, horloge c), mort sous -Mn."""
    N = C * Mn
    T = np.zeros((N, N))
    b = np.zeros(N)
    for c in range(C):
        for c2, act, p in trans[c]:
            for j in range(Mn):  # mu = j - Mn in [-Mn, -1]
                if act == "A":
                    j2 = j + 1
                    if j2 == Mn:
                        b[c * Mn + j] += p
                    else:
                        T[c * Mn + j, c2 * Mn + j2] += p
                elif act == "h":
                    j2 = j - 1
                    if j2 >= 0:
                        T[c * Mn + j, c2 * Mn + j2] += p
                else:
                    T[c * Mn + j, c2 * Mn + j] += p
    V = np.linalg.solve(np.eye(N) - T, b)
    return np.clip(V.reshape(C, Mn), 0, 1)


def act_A(X, R):
    Y = np.zeros_like(X)
    Y[1:, 1:] = X[:-1, :-1]
    return Y, X[R, :].sum(), 0.0


def act_h(X, Mn):
    Y = np.zeros_like(X)
    # rho >= 1
    Y[:-1, : Mn - 1] += X[1:, 1:Mn]          # mu<0 -> mu-1
    Y[:-1, Mn] += X[1:, Mn]                   # mu=0 collant
    Y[:-1, Mn:-1] += X[1:, Mn + 1 :]          # mu>0 -> mu-1
    killed = X[1:, 0].sum()
    # rho = 0 (mu <= 0)
    Y[0, :-1] += X[0, 1:]
    killed += X[0, 0]
    return Y, 0.0, killed


def run(cfg):
    beta, d, D, mode, level, maxsteps = cfg
    t0 = time.time()
    a, h, g, q = rates(beta, d, D, mode)
    out = dict(beta=beta, d=d, D=D, mode=mode, level=level, g=g, q=q)
    if q >= g:
        out.update(status="INFINI", K={str(x): None for x in TARGETS})
        return out
    # rapport effectif (par symbole utile) pour dimensionner les troncatures
    theta = q / g
    if theta > 0.93:
        # quasi critique : décroissance < 1 %/symbole utile ; K > plusieurs 10^4 créneaux.
        out.update(status="QUASI-CRITIQUE", theta=theta, K={str(x): None for x in TARGETS})
        return out
    Mn = int(min(900, math.ceil(math.log(1e-16) / math.log(theta)) + 10))
    R = Mn
    C = D + 2
    tslot = kernel(beta, d, D, mode, "slot")
    trans = tslot if level == "slot" else kernel(beta, d, D, mode, "sym")
    pi = stationary_reach(tslot, C, R)
    fail0 = pi[:, R].sum()
    ret = return_probs(trans, C, Mn)
    ret_floor = ret[:, 0].max()
    W = R + Mn + 1
    P = np.zeros((C, R + 1, W))
    for c in range(C):
        for r in range(R):
            P[c, r, Mn + r] = pi[c, r]
    fail = fail0
    killed = 0.0
    eps_hist = []
    K = {}
    for step in range(1, maxsteps + 1):
        Pn = np.zeros_like(P)
        for c in range(C):
            X = P[c]
            if not X.any():
                continue
            for c2, act, p in trans[c]:
                if act == "A":
                    Y, f, k = act_A(X, R)
                elif act == "h":
                    Y, f, k = act_h(X, Mn)
                else:
                    Y, f, k = X, 0.0, 0.0
                Pn[c2] += p * Y
                fail += p * f
                killed += p * k
        P = Pn
        pos = P[:, :, Mn:].sum()
        neg = float((P[:, :, :Mn].sum(axis=1) * ret).sum())
        eps = fail + pos + neg + ret_floor  # masse tuée : retour <= ret_floor
        eps = min(1.0, eps)
        eps_hist.append(eps)
        for x in TARGETS:
            if str(x) not in K and eps <= x:
                K[str(x)] = step
        if eps < STOP_EPS:
            break
    # extrapolation log-linéaire si nécessaire
    n = len(eps_hist)
    extrap = False
    for x in TARGETS:
        if str(x) not in K:
            lo = int(n * 0.6)
            y1, y2 = math.log(eps_hist[lo]), math.log(eps_hist[-1])
            slope = (y2 - y1) / (n - 1 - lo)
            if slope >= 0:
                K[str(x)] = None
            else:
                K[str(x)] = int(n + (math.log(x) - y2) / slope)
                extrap = True
    out.update(status="OK", K=K, extrap=extrap, steps=n, R=R, Mn=Mn,
               eps_last=eps_hist[-1], floor=fail0 + ret_floor,
               curve={str(k): eps_hist[k - 1] for k in
                      sorted(set([1, 10, 30, 50, 100, 200, 300, 500, 800, 1000,
                                  1500, 2000, 2880, 3000, 4000, 5000, 7200,
                                  10000, 14400, 20000]))
                      if k <= n},
               secs=round(time.time() - t0, 1))
    return out


def main():
    outp = "table_analytique.json"
    if "--out" in sys.argv:
        outp = sys.argv[sys.argv.index("--out") + 1]
    cfgs = []
    for beta in [0.10, 0.20, 0.25, 0.30]:
        for d in [1.0, 0.7, 0.4, 0.2]:
            for D in [0, 1, 2]:
                modes = ["pess"] if D == 0 else ["pess", "opt"]
                for mode in modes:
                    for level in ["slot", "sym"]:
                        cfgs.append((beta, d, D, mode, level, 25000 if level == "slot" else 12000))
    cfgs.sort(key=lambda c: -rates(c[0], c[1], c[2], c[3])[3] / max(1e-9, rates(c[0], c[1], c[2], c[3])[2]))
    with Pool(14) as pool:
        res = []
        for r in pool.imap_unordered(run, cfgs):
            res.append(r)
            print(r["beta"], r["d"], r["D"], r["mode"], r["level"], r["status"], r.get("K"),
                  r.get("secs"), "extrap" if r.get("extrap") else "", flush=True)
    with open(outp, "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()


def private_attack_D0(beta, d, level, kmax=40000, targets=TARGETS):
    """Attaque privée seule, D=0, avance initiale = reach stationnaire (géométrique
    de raison theta=q/p par symbole), égalité gagnée. Exact :
        eps(k) = P(Y_k >= 0) + sum_{y<0} P(Y_k=y) * theta^(-y),
    Y_k = rho0 + (#A - #h) sur les k premiers créneaux (ou symboles)."""
    a = beta
    h = (1 - beta) * d
    u = a + h
    if a >= h:
        return None, {}
    theta = a / h
    if level == "slot":
        pA, pH, p0 = a, h, 1 - u
    else:
        pA, pH, p0 = a / u, h / u, 0.0
    M = int(math.log(1e-18) / math.log(theta)) + 5
    off = kmax + M + 5
    size = off + M + kmax + 10
    import numpy as _np
    Y = _np.zeros(size)
    for r in range(M):
        Y[off + r] = (1 - theta) * theta ** r
    fail = theta ** M
    ys = _np.arange(size) - off
    w = _np.where(ys >= 0, 1.0, theta ** (-_np.minimum(ys, 0).astype(float)))
    K = {}
    curve = {}
    lo, hi = off, off + M - 1  # support courant
    for k in range(1, kmax + 1):
        Yn = _np.zeros(size)
        Yn[lo + 1:hi + 2] += pA * Y[lo:hi + 1]
        Yn[lo - 1:hi] += pH * Y[lo:hi + 1]
        Yn[lo:hi + 1] += p0 * Y[lo:hi + 1]
        Y = Yn
        lo -= 1
        hi += 1
        # élaguer très loin sous zéro (retour <= theta^m négligeable)
        cut = off - M
        if lo < cut:
            Y[lo:cut] = 0.0
            lo = cut
        while hi > off and Y[hi] < 1e-40:
            fail += Y[hi]; Y[hi] = 0.0; hi -= 1
        while Y[lo] < 1e-40 and lo < hi:
            Y[lo] = 0.0; lo += 1
        eps = float((Y[lo:hi + 1] * w[lo:hi + 1]).sum()) + fail
        if k in (100, 300, 500, 1000, 2000, 2880, 5000, 7200, 10000, 14400):
            curve[k] = eps
        for x in targets:
            if str(x) not in K and eps <= x:
                K[str(x)] = k
        if eps < 1e-13:
            break
    return K, curve

