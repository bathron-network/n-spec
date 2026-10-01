#!/usr/bin/env python3
"""Chaîne de dérivation conditionnelle de K pour BATHRON N (CP_reg).

Ordre du mandat (DIRECTION.md, 01/10) : tau -> (beta_max, d_min) -> K(eps)
-> K_reg -> registry_min_blocks -> métriques SP/LP.  Ce script NE FIXE AUCUN
paramètre de consensus : il produit des tables conditionnelles à (beta, d,
p_late, tau, horizon, Q_B), à appliquer dès que le banc réseau aura mesuré
p_late(tau).

Réutilise, sans les modifier :
  - ../sim-opus/cp_bound.py  (DP exacte BKMQR : kernel, stationary_reach,
    return_probs, act_A, act_h) ;
  - ../sim/model.py          (enveloppe Codex `derive`, queues de Chernoff).
Copies documentées ici : la boucle `run` d'Opus (pour renvoyer toute la
courbe et descendre à 1e-17), l'attaque privée exacte (tie et strict), et
`strategic_race` de Codex (pour renvoyer les tableaux par départ et mesurer
eps par coupure).  Voir DERIVATION-K.md.

Régime réseau : un créneau honnête est « en retard » avec probabilité p_late
(bloc non reçu ET validé, dépendances comprises, par tous les honnêtes avant
la réservation du créneau suivant).  Réduction conservatrice : un créneau
honnête en retard est un créneau ADVERSE.  D'où
    a  = beta + h*p_late,   h' = h*(1-p_late),   h = (1-beta)*d,
et la condition d'existence de K : h' > a  <=>  (1-beta)*d*(1-2 p_late) > beta.

Usage : nice -n 10 python3 derive_k.py [--quick] [--procs 4]
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "sim-opus"))
sys.path.insert(0, str(HERE.parent / "sim"))
import cp_bound as OB  # noqa: E402  (Opus, non modifié)
import model as CM     # noqa: E402  (Codex, non modifié)

ROOT_SEED = 20261001
BETAS = (0.10, 0.15, 0.20, 0.25, 0.30)
DENS = (0.2, 0.3, 0.4, 0.5, 0.7, 1.0)
PLATES = (0.0, 1e-6, 1e-4, 1e-3, 1e-2)
EPS = (1e-6, 1e-9, 1e-12)
TAUS = (6, 8, 10, 12)
K_LIMIT = 13200          # seuil « K raisonnable » du mandat (créneaux)
TRUNC = 1e-16            # troncature DP (masse tronquée = échec), comme Opus
STOP = 1e-14             # arrêt DP : plancher numérique float64 ~1e-16 (solve
                         # de return_probs) ; au-delà : extrapolation log-linéaire
MAXSTEPS = {"slot": 26000, "sym": 16000}
QUASI = 0.93             # theta = a/h' au-delà : quasi critique (hors domaine)

# Paramètres N-SPEC v0.6 utilisés par la composition (lus, non modifiés).
L_EPOCH = 14400
SEED_GUARD_S = 43200
MTP_MARGIN_S = 7200
HORIZON_YEARS = 10


def eff(beta, d, p):
    h = (1.0 - beta) * d
    a = beta + h * p
    hp = h * (1.0 - p)
    return a, hp


# ---------------------------------------------------------------- DP (Opus)
def dp_curve(job):
    """Copie de cp_bound.run (D=0, mode pess) sur (a, h'), courbe complète."""
    beta, d, p, level = job
    a, hp = eff(beta, d, p)
    out = _dp(a, hp, level)
    out.update(beta=beta, d=d, p=p)
    return out


def dp_theta(job):
    """Niveau 'sym' : ne dépend que de theta = a/h' (créneaux vides retirés)."""
    theta = job
    out = _dp(theta / (1 + theta), 1 / (1 + theta), "sym")
    out["theta_in"] = theta
    return out


def _dp(a, hp, level):
    t0 = time.time()
    out = dict(level=level, a=a, h=hp)
    if a >= hp:
        out.update(status="INFINI", eps=None)
        return out
    theta = a / hp
    out["theta"] = theta
    if theta > QUASI:
        out.update(status="QUASI-CRITIQUE", eps=None)
        return out
    be, de = a, hp / (1.0 - a)   # (1-be)*de = h', be = a : loterie identique
    Mn = int(min(1400, math.ceil(math.log(TRUNC) / math.log(theta)) + 10))
    R, C = Mn, 2
    tslot = OB.kernel(be, de, 0, "pess", "slot")
    trans = tslot if level == "slot" else OB.kernel(be, de, 0, "pess", "sym")
    pi = OB.stationary_reach(tslot, C, R)
    fail = pi[:, R].sum()
    ret = OB.return_probs(trans, C, Mn)
    ret_floor = ret[:, 0].max()
    P = np.zeros((C, R + 1, R + Mn + 1))
    for c in range(C):
        for r in range(R):
            P[c, r, Mn + r] = pi[c, r]
    hist = []
    for _ in range(MAXSTEPS[level]):
        Pn = np.zeros_like(P)
        for c in range(C):
            X = P[c]
            if not X.any():
                continue
            for c2, act, pr in trans[c]:
                if act == "A":
                    Y, f, _k = OB.act_A(X, R)
                elif act == "h":
                    Y, f, _k = OB.act_h(X, Mn)
                else:
                    Y, f = X, 0.0
                Pn[c2] += pr * Y
                fail += pr * f
        P = Pn
        pos = P[:, :, Mn:].sum()
        neg = float((P[:, :, :Mn].sum(axis=1) * ret).sum())
        e = min(1.0, fail + pos + neg + ret_floor)
        hist.append(e)
        if e < STOP:
            break
    out.update(status="OK", eps=np.array(hist), floor=float(fail + ret_floor),
               Mn=Mn, secs=round(time.time() - t0, 2))
    return out


def k_of(curve, target):
    """Plus petit K avec eps(K) <= target ; extrapolation log-linéaire sinon."""
    if curve is None:
        return None, False
    idx = np.flatnonzero(curve <= target)
    if len(idx):
        return int(idx[0]) + 1, False
    n = len(curve)
    lo = int(n * 0.6)
    y1, y2 = math.log(curve[lo]), math.log(curve[-1])
    sl = (y2 - y1) / (n - 1 - lo)
    if sl >= 0:
        return None, True
    return int(math.ceil(n + (math.log(target) - y2) / sl)), True


def eps_of(curve, K):
    if curve is None:
        return 1.0
    if K <= 0:
        return 1.0
    if K <= len(curve):
        return float(curve[K - 1])
    n = len(curve)
    lo = int(n * 0.6)
    y1, y2 = math.log(curve[lo]), math.log(curve[-1])
    sl = (y2 - y1) / (n - 1 - lo)
    return float(math.exp(y2 + sl * (K - n)))


# ------------------------------------------------ attaque privée exacte (Opus)
def private_curve(job):
    """Copie adaptée de cp_bound.private_attack_D0 : avance initiale = reach
    stationnaire, marche libre ; eps(k)=P(exists t>=k : Y_t >= need).
    need=0 : égalité gagnée ; need=1 : dépassement strict (borne INFÉRIEURE
    réalisable du risque, départage public défavorable)."""
    beta, d, p, level, need, kmax = job
    a, hp = eff(beta, d, p)
    if a >= hp:
        return dict(beta=beta, d=d, p=p, level=level, need=need, eps=None)
    th = a / hp
    if level == "slot":
        pA, pH, p0 = a, hp, 1 - a - hp
    else:
        pA, pH, p0 = a / (a + hp), hp / (a + hp), 0.0
    M = int(math.log(1e-18) / math.log(th)) + 5
    off = kmax + M + 5
    size = off + M + kmax + 10
    Y = np.zeros(size)
    for r in range(M):
        Y[off + r] = (1 - th) * th ** r
    fail = th ** M
    ys = np.arange(size) - off
    w = np.where(ys >= need, 1.0, th ** (need - np.minimum(ys, need)).astype(float))
    lo, hi = off, off + M - 1
    hist = []
    for _k in range(kmax):
        Yn = np.zeros(size)
        seg = Y[lo:hi + 1]
        Yn[lo + 1:hi + 2] += pA * seg
        Yn[lo - 1:hi] += pH * seg
        Yn[lo:hi + 1] += p0 * seg
        Y = Yn
        lo -= 1
        hi += 1
        cut = off - M
        if lo < cut:
            Y[lo:cut] = 0.0
            lo = cut
        while hi > off and Y[hi] < 1e-40:
            fail += Y[hi]
            Y[hi] = 0.0
            hi -= 1
        while Y[lo] < 1e-40 and lo < hi:
            Y[lo] = 0.0
            lo += 1
        e = float((Y[lo:hi + 1] * w[lo:hi + 1]).sum()) + fail
        hist.append(e)
        if e < 1e-13:
            break
    return dict(beta=beta, d=d, p=p, level=level, need=need, eps=np.array(hist))


# ------------------------------------------------- Monte-Carlo (Codex, copie)
def race_arrays(labels, ties):
    """Copie de model.strategic_race pour d=0 (groupes d'un créneau,
    producteurs honnêtes distincts), renvoyant les tableaux par départ au lieu
    des seuls témoins max.  Attaque : rétention totale, départ et révélation
    optimaux, départage PUBLIC (tie), une unité de score par créneau adverse
    (l'équivoque n'ajoute rien sur une branche)."""
    n = len(labels)
    hc = (labels == 1).astype(np.int64)
    ac = (labels == 2).astype(np.int64)
    public_slots = np.flatnonzero(labels == 1)
    adverse_slots = np.flatnonzero(labels == 2)
    H = np.r_[0, np.cumsum(hc)]
    A = np.r_[0, np.cumsum(ac)]
    balance = A - H
    idx = np.arange(n + 1)
    fa = np.r_[adverse_slots, n][np.searchsorted(adverse_slots, np.arange(n))]
    fh = np.r_[public_slots, n][np.searchsorted(public_slots, np.arange(n))]
    pt = np.r_[ties, np.inf]
    tie_good = pt[fa] < pt[fh]
    offset = int(-balance.min()) + 2
    maximum = int(balance.max() + offset) + 4
    last_at = np.full(maximum + 1, -1, dtype=np.int64)
    np.maximum.at(last_at, balance + offset, idx)
    last_ge = np.maximum.accumulate(last_at[::-1])[::-1]
    threshold = balance[:-1] + offset + np.where(tie_good, 0, 1)
    release = last_ge[threshold]
    starts = np.arange(n)
    valid = (release > starts) & (fa < n) & (fh < n)
    removed = H[np.maximum(release, 0)] - H[starts]
    valid &= removed > 0
    first_diff = np.minimum(fa, fh)
    return valid, release - 1, first_diff


def mc_cell(job):
    beta, d, p, ib, idd, ip, T, ncal, warm, tail, kgrid = job
    rng = np.random.default_rng(np.random.SeedSequence([ROOT_SEED, 7, ib, idd, ip]))
    h = (1 - beta) * d
    cnt_s = np.zeros(len(kgrid), dtype=np.int64)
    cnt_n = np.zeros(len(kgrid), dtype=np.int64)
    epi = np.zeros(len(kgrid), dtype=np.int64)      # épisodes (runs de coupures)
    percal = []
    ncuts = 0
    censored = 0
    kg = np.array(kgrid)
    for _ in range(ncal):
        u = rng.random(T)
        labels = np.where(u < beta, 2, np.where(u < beta + h, 1, 0)).astype(np.int8)
        late = (labels == 1) & (rng.random(T) < p)
        labels[late] = 2                    # réduction : honnête en retard = adverse
        ties = rng.random(T)
        valid, rel, fd = race_arrays(labels, ties)
        best = np.full(T + 1, -1, dtype=np.int64)
        np.maximum.at(best, fd[valid] + 1, rel[valid])
        best = np.maximum.accumulate(best)       # best[c] = max rel, fd < c
        ne = np.cumsum(labels != 0)
        cuts = np.arange(warm, T - tail)
        r = best[cuts]
        dep_s = np.where(r >= cuts, r - cuts, -1)
        dep_n = np.where(r >= cuts, ne[np.maximum(r, 0)] - ne[cuts - 1], -1)
        censored += int((r >= T - 50).sum())
        v = dep_s[:, None] >= kg[None, :]
        cnt_s += v.sum(axis=0)
        epi += (v[1:] & ~v[:-1]).sum(axis=0) + v[0]
        percal.append(v.sum(axis=0).tolist())
        cnt_n += (dep_n[:, None] >= kg[None, :]).sum(axis=0)
        ncuts += len(cuts)
    return dict(beta=beta, d=d, p=p, ncuts=ncuts, censored=censored,
                kgrid=list(kgrid), slots=cnt_s.tolist(), nonempty=cnt_n.tolist(),
                episodes=epi.tolist(), percal=percal)


# --------------------------------------------------------- composition
_LG = None


def _lg(n):
    global _LG
    if _LG is None or len(_LG) <= n:
        _LG = np.array([math.lgamma(i + 1.0) for i in range(max(n + 1, 250000))])
    return _LG


def pcount_all(m, hp, jmax):
    """Pc[j] = P[Bin(j,h') < m] pour j = 0..jmax, exacte et sans annulation :
    Pc[j] = h' * sum_{i>=j} P[Bin(i,h') = m-1]  (somme de termes positifs)."""
    pc = np.ones(jmax + 1)
    if m <= 0:
        return np.zeros(jmax + 1)
    k = m - 1
    imax = int(max(jmax, (m / hp) * 3 + 20 * math.sqrt(m / hp) + 2000))
    LG = _lg(imax + 1)
    i = np.arange(k, imax + 1)
    lp = LG[i] - LG[k] - LG[i - k] + k * math.log(hp) + (i - k) * math.log1p(-hp)
    pmf = np.exp(lp)
    tail = hp * np.cumsum(pmf[::-1])[::-1]          # tail[t] pour i = k + t
    top = min(jmax, imax)
    js = np.arange(k, top + 1)
    pc[k:top + 1] = np.minimum(1.0, tail[js - k])
    if jmax > imax:
        pc[imax + 1:] = 0.0
    return pc


def binom_lt(n, p, j):
    return float(pcount_all(j, p, n)[n]) if j > 0 else 0.0


def ext_curve(curve, kmax):
    """Courbe eps_fix(K), K=1..kmax, prolongée log-linéairement (extrapolation)."""
    n = len(curve)
    if kmax <= n:
        return curve[:kmax].copy()
    lo = int(n * 0.6)
    y1, y2 = math.log(curve[lo]), math.log(curve[-1])
    sl = min(0.0, (y2 - y1) / (n - 1 - lo))
    extra = np.exp(y2 + sl * np.arange(1, kmax - n + 1))
    return np.r_[curve, extra]


def pivot_terms(ec, b, kin, hp, theta, q):
    """Pivot (voie ii) unifié.  Y bifurque de la chaîne honnête en f = cut + j ;
    compte(Y) >= #H(cut,f] - rho, rho = avance stationnaire.  Si compte(Y) < b :
    #H(j) < b + r ou rho >= r.  Y n'est installable qu'à cut + K_inst au plus
    tôt, donc la fourche a un âge >= K_inst - j (violation CP à coupure f+1).
      T_profond = sum_{j<K_inst} min(P[Bin(j,h')<b+r], eps_fix(K_inst-j))
      T_court   = theta^r + P[Bin(K_inst,h') < b+r]   (j >= K_inst : événements
                  emboîtés ; c'est la condition de robustesse du compte A)."""
    r = max(0, math.ceil(math.log(q / 10) / math.log(theta)))
    pc = pcount_all(b + r, hp, kin)
    js = np.arange(kin)
    ef = ec[np.clip(kin - js - 1, 0, len(ec) - 1)]
    t_prof = float(np.minimum(pc[:kin], ef).sum())
    t_court = theta ** r + float(pc[kin])
    return t_prof, t_court, r


def compose(curves, beta, d, p, tau, eps_h, qb, b=None, kreg=None):
    """Garantie par époque (D1 : ε_post exclu, nœuds nouveaux/de retour hors
    domaine) :
         ε_ep <= T_fix + (T_court + T_profond) + T_CG
       budgets : ε_ep/4, ε_ep/2, ε_ep/4.
       T_fix  = ε_fix(K_inst)                  [voie (i), coupure fixe snapshot_cut]
       T_court, T_profond : pivot_terms        [voie (ii)]
       T_CG   = P[#H(L+K_reg) - rho < b+1]     [synchronisés : maxreorg -> HALT]
       K_inst = K_reg + G(tau), G = ceil((seed_guard - marge MTP)/tau).
       Horizon : ε_H = E(tau) * Q_B * ε_ep  (union sur époques et graines)."""
    a, hp = eff(beta, d, p)
    cs, cn = curves.get((beta, d, p, "slot")), curves.get((beta, d, p, "sym"))
    if cs is None or cn is None:
        return None
    E = math.ceil(HORIZON_YEARS * 365.25 * 86400 / (L_EPOCH * tau))
    G = math.ceil((SEED_GUARD_S - MTP_MARGIN_S) / tau)
    ep = eps_h / (E * qb)
    q = ep / 4
    theta = a / hp
    K1, x1 = k_of(cs, q)
    bmin, xb = k_of(cn, q)            # choix de vivacité : ε_live = ε_ep/4
    if K1 is None or bmin is None:
        return None
    ec = ext_curve(cs, 80000)
    bb = bmin if b is None else b

    def ok_pivot(bv, kin):
        tp, tc, _ = pivot_terms(ec, bv, kin, hp, theta, q)
        return tp + tc <= 2 * q

    lo, hi = K1 - 1, max(K1, int(bb / hp) + 1)
    while not ok_pivot(bb, hi):
        hi *= 2
        if hi > 70000:
            return None
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if ok_pivot(bb, mid):
            hi = mid
        else:
            lo = mid
    Kinst_req = max(K1, hi)
    Kreg_min = max(1, Kinst_req - G)
    kr = Kreg_min if kreg is None else kreg
    kin = kr + G
    rr = max(0, math.ceil(math.log(q / 10) / math.log(theta)))
    t_cg = binom_lt(L_EPOCH + kr, hp, bb + 1 + rr) + theta ** rr
    t_fix = float(ec[kin - 1]) if kin >= 1 else 1.0
    t_prof, t_court, _ = pivot_terms(ec, bb, kin, hp, theta, q)
    # b maximal compatible avec ce K_reg (pivot seul ; T_CG vérifié à part)
    lo_b, hi_b = 0, max(2, int(hp * kin) + 2)
    while lo_b + 1 < hi_b:
        mid = (lo_b + hi_b) // 2
        if ok_pivot(mid, kin):
            lo_b = mid
        else:
            hi_b = mid
    tot = t_fix + t_court + t_prof + t_cg
    return dict(beta=beta, d=d, p=p, tau=tau, eps_H=eps_h, Q_B=qb, E=E, G=G,
                eps_epoch=ep, b=bb, b_min_live=bmin, K_fix_slots=K1,
                K_inst_req=Kinst_req, K_reg_min=Kreg_min,
                K_reg_used=kr, K_reg_hours=round(kr * tau / 3600, 2),
                b_max_given_Kreg=lo_b,
                T_fix=t_fix, T_court=t_court, T_profond=t_prof, T_CG=t_cg,
                eps_epoch_composed=min(1.0, tot),
                eps_H_composed=min(1.0, E * qb * tot),
                sep_5_8_s=kr * tau + SEED_GUARD_S,
                extrapolated=bool(x1 or xb or Kinst_req > len(cs)))


# ----------------------------------------------------------------- rendu
def _f(x):
    return "—" if x in ("", None) else x


def render(res):
    """Écrit results/TABLES.md à partir des CSV/JSON (aucun recalcul)."""
    K = list(csv.DictReader(open(res / "K-table.csv")))
    comp = list(csv.DictReader(open(res / "composition.csv")))
    dmin = list(csv.DictReader(open(res / "d-min.csv")))
    mc = json.load(open(res / "mc.json"))
    L = ["# Tables générées par `derive_k.py` (ne pas éditer)\n",
         "Cellule = K créneaux / K blocs (créneaux non vides), borne DP exacte (analytique). "
         "Entre crochets : attaque privée exacte, dépassement strict (borne inférieure réalisable), créneaux. "
         "`HD` = hors domaine de sûreté N. `*` = extrapolation log-linéaire au-delà de 1e-14.\n"]
    for p in PLATES:
        L.append(f"\n## p_late = {p:g}\n")
        L.append("| β | d | h'−a | ε=1e-6 | ε=1e-9 | ε=1e-12 |")
        L.append("|---:|---:|---:|---|---|---|")
        for beta in BETAS:
            for d in DENS:
                cells = []
                marg = ""
                for e in EPS:
                    r = next(x for x in K if float(x["beta"]) == beta and float(x["d"]) == d
                             and float(x["p_late"]) == p and float(x["eps"]) == e)
                    marg = f"{float(r['cond_margin']):.3f}"
                    star = "*" if r["extrap"] == "True" else ""
                    if r["status"] == "domaine":
                        cells.append(f"{r['K_slots']} / {r['K_blocks']}{star} [{r['K_priv_strict']}]")
                    elif r["K_slots"]:
                        cells.append(f"HD {r['K_slots']} / {r['K_blocks']}{star} [{r['K_priv_strict']}]")
                    elif r["K_priv_strict"]:
                        cells.append(f"HD [attaque ≥ {r['K_priv_strict']}]")
                    else:
                        cells.append("HD (h' ≤ a)")
                L.append(f"| {beta:.2f} | {d:.1f} | {marg} | " + " | ".join(cells) + " |")
    L.append("\n## Condition renforcée : d_min tel que K(ε) ≤ 13 200 créneaux\n")
    L.append("`d_cond` = seuil de (1−β)d(1−2p) > β ; `d_min` = seuil pratique ; θ_max = a/h' maximal.\n")
    L.append("| β | p_late | ε | d_cond | d_min | θ_max | h'−a minimal |")
    L.append("|---:|---:|---:|---:|---:|---:|---:|")
    for r in dmin:
        if float(r["p_late"]) in (0.0, 1e-3, 1e-2):
            L.append(f"| {r['beta']} | {float(r['p_late']):g} | {float(r['eps']):g} | {r['d_cond']} | "
                     f"{_f(r['d_min'])} | {_f(r['theta_max'])} | {_f(r['margin_h_minus_a'])} |")
    L.append("\n## Monte-Carlo (attaque Codex, ε par coupure) contre attaque privée exacte et DP\n")
    L.append("Points retenus : ≥ 30 épisodes indépendants (runs de coupures). Rapport = MC / valeur analytique.\n")
    L.append("| p_late | β | d | points | MC/strict (min–max) | MC/tie (min–max) | MC/DP max | z max vs tie |")
    L.append("|---:|---:|---:|---:|---|---|---:|---:|")
    for m in sorted(mc, key=lambda m: (m["p"], m["beta"], m["d"])):
        n = m["ncuts"]
        pts = []
        for i, (k, s, ep) in enumerate(zip(m["kgrid"], m["slots"], m["episodes"])):
            if ep >= 30 and k > 1:
                pc = np.array([c[i] for c in m["percal"]], float)
                e = s / n
                se = pc.std(ddof=1) / math.sqrt(len(pc)) / (n / len(pc))
                pts.append((e / m["priv_strict"][i], e / m["priv_tie"][i], e / m["dp"][i],
                            (e - m["priv_tie"][i]) / se if se > 0 else 0.0))
        if not pts:
            continue
        a = np.array(pts)
        L.append(f"| {m['p']:g} | {m['beta']} | {m['d']} | {len(pts)} | {a[:,0].min():.2f}–{a[:,0].max():.2f} | "
                 f"{a[:,1].min():.2f}–{a[:,1].max():.2f} | {a[:,2].max():.2f} | {a[:,3].max():.1f} |")
    L.append("\n## Composition conditionnelle (ε_H sur 10 ans, b = b_min de vivacité)\n")
    L.append("Cellule : b_min / K_inst requis / **K_reg min** (h) ; contrôle a posteriori 7 200/2 880 : "
             "b_max(K_reg=7 200) et PASS/FAIL de ε_H composé.\n")
    for eh in (1e-6, 1e-9):
        L.append(f"\n### ε_H = {eh:g}\n")
        L.append("| β | d | p_late | Q_B | τ=6 s | τ=8 s | τ=10 s | τ=12 s |")
        L.append("|---:|---:|---:|---:|---|---|---|---|")
        cells = sorted({(r["beta"], r["d"]) for r in comp}, key=lambda x: (float(x[0]), float(x[1])))
        for beta, d in cells:
            for p in ("0.0", "0.001"):
                for qb in ("1", "256"):
                    line = []
                    for tau in TAUS:
                        r = [x for x in comp if x["beta"] == beta and x["d"] == d and x["p"] == p
                             and x["Q_B"] == qb and x["tau"] == str(tau) and float(x["eps_H"]) == eh]
                        if len(r) < 2:
                            line.append("—")
                            continue
                        a = next(x for x in r if x["mode"].startswith("b="))
                        c = next(x for x in r if x["mode"].startswith("controle"))
                        ok = "PASS" if float(c["eps_H_composed"]) <= eh else "FAIL"
                        line.append(f"{a['b']} / {a['K_inst_req']} / **{a['K_reg_min']}** ({a['K_reg_hours']} h) ; "
                                    f"b_max {c['b_max_given_Kreg']} {ok}")
                    L.append(f"| {beta} | {d} | {float(p):g} | {qb} | " + " | ".join(line) + " |")
    (res / "TABLES.md").write_text("\n".join(L) + "\n")


# ----------------------------------------------------------------- main
def init_worker():
    try:
        os.nice(10)
    except OSError:
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--render-only", action="store_true")
    args = ap.parse_args()
    if args.render_only:
        render(HERE / "results")
        return
    procs = min(4, args.procs)
    init_worker()
    res = HERE / "results"
    res.mkdir(exist_ok=True)
    t0 = time.time()
    cpu0 = time.process_time()
    log = {"seed": ROOT_SEED, "procs": procs, "numpy": np.__version__,
           "python": sys.version.split()[0], "stages": {}}
    pool = Pool(procs, initializer=init_worker)

    # 1. Attaque privée exacte (bornes inférieures) : tri et pré-classement.
    t = time.time()
    pjobs = []
    for beta in BETAS:
        for d in DENS:
            for p in PLATES:
                a, hp = eff(beta, d, p)
                if a >= hp:
                    continue
                pjobs += [(beta, d, p, "slot", 1, 30000), (beta, d, p, "slot", 0, 30000),
                          (beta, d, p, "sym", 0, 20000)]
    if args.quick:
        pjobs = [j for j in pjobs if j[2] in (0.0, 1e-3)]
    priv = {}
    for r in pool.imap_unordered(private_curve, pjobs):
        priv[(r["beta"], r["d"], r["p"], r["level"], r["need"])] = r["eps"]
    log["stages"]["private"] = round(time.time() - t, 1)

    # 2. DP exacte (bornes supérieures), sautée si l'attaque stricte prouve
    #    déjà K(1e-6) > K_LIMIT : hors domaine établi par une attaque
    #    réalisable, pour les trois eps (K croît quand eps décroît).
    t = time.time()
    djobs, skipped = [], []
    for beta in BETAS:
        for d in DENS:
            for p in PLATES:
                if args.quick and p not in (0.0, 1e-3):
                    continue
                c = priv.get((beta, d, p, "slot", 1))
                if c is not None:
                    k6, _ = k_of(c, 1e-6)
                    if k6 is None or k6 > K_LIMIT:
                        skipped.append((beta, d, p))
                        continue
                djobs += [(beta, d, p, "slot"), (beta, d, p, "sym")]
    djobs.sort(key=lambda j: -(eff(j[0], j[1], j[2])[0] / max(1e-9, eff(j[0], j[1], j[2])[1])))
    curves, dpmeta = {}, {}
    for r in pool.imap_unordered(dp_curve, djobs):
        key = (r["beta"], r["d"], r["p"], r["level"])
        curves[key] = r["eps"]
        dpmeta[key] = {k: v for k, v in r.items() if k != "eps"}
        print("DP", key, r["status"], r.get("secs"), flush=True)
    log["stages"]["dp"] = round(time.time() - t, 1)
    np.savez_compressed(res / "dp_curves.npz", **{
        f"{k[0]}_{k[1]}_{k[2]}_{k[3]}": v for k, v in curves.items() if v is not None})

    # 3. Table K(eps) + classement du domaine.
    rows = []
    for beta in BETAS:
        for d in DENS:
            for p in PLATES:
                if args.quick and p not in (0.0, 1e-3):
                    continue
                a, hp = eff(beta, d, p)
                base = dict(beta=beta, d=d, p_late=p, a=round(a, 6), h=round(hp, 6),
                            cond_margin=round(hp - a, 6))
                for e in EPS:
                    row = dict(base, eps=e)
                    cs = curves.get((beta, d, p, "slot"))
                    cn = curves.get((beta, d, p, "sym"))
                    ks, xs = k_of(cs, e)
                    kn, xn = k_of(cn, e)
                    kpt, _ = k_of(priv.get((beta, d, p, "slot", 0)), e)
                    kps, _ = k_of(priv.get((beta, d, p, "slot", 1)), e)
                    kpn, _ = k_of(priv.get((beta, d, p, "sym", 0)), e)
                    if a >= hp:
                        st = "HORS DOMAINE : (1-b)d(1-2p) <= b"
                    elif (beta, d, p) in skipped:
                        st = "HORS DOMAINE : attaque privée stricte > 13200 dès 1e-6"
                    elif dpmeta.get((beta, d, p, "slot"), {}).get("status") == "QUASI-CRITIQUE":
                        st = "HORS DOMAINE : quasi critique"
                    elif ks is None or ks > K_LIMIT:
                        st = "HORS DOMAINE : K > 13200"
                    else:
                        st = "domaine"
                    row.update(K_slots=ks, K_blocks=kn, extrap=bool(xs or xn),
                               K_priv_tie=kpt, K_priv_strict=kps, K_priv_blocks=kpn,
                               status=st)
                    rows.append(row)
    with open(res / "K-table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # 4. Enveloppe Codex (derive) sur les mêmes (a, h').
    t = time.time()
    crow = []
    for beta in BETAS:
        for d in DENS:
            for p in (0.0, 1e-3):
                a, hp = eff(beta, d, p)
                if a >= hp:
                    continue
                for e in EPS:
                    try:
                        r = CM.derive(a, hp / (1 - a), 0.0, e, horizon=14400, q_paths=1)
                    except Exception as ex:  # noqa: BLE001
                        r = dict(conditional_status="ERROR:" + str(ex))
                    crow.append(dict(beta=beta, d=d, p_late=p, eps=e,
                                     status=r.get("conditional_status"),
                                     b=r.get("registry_min_blocks_conditional"),
                                     K_barrier=r.get("K_barrier_slots"),
                                     W=r.get("K_reg_slots_guard0"),
                                     M=r.get("horizon")))
    with open(res / "codex-envelope.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(crow[0].keys()))
        w.writeheader()
        w.writerows(crow)
    log["stages"]["codex_envelope"] = round(time.time() - t, 1)

    # 5. Monte-Carlo (attaque Codex, eps par coupure) sur les cases résolubles.
    t = time.time()
    mjobs = []
    for ib, beta in enumerate(BETAS):
        for idd, d in enumerate(DENS):
            for ip, p in enumerate(PLATES):
                if p not in (0.0, 1e-3):
                    continue
                k6, _ = k_of(curves.get((beta, d, p, "slot")), 1e-6)
                if k6 is None or k6 > 6000:
                    continue
                k5, _ = k_of(priv.get((beta, d, p, "slot", 0)), 1e-5)
                kg = sorted(set(int(x) for x in np.linspace(1, max(12, k5), 12)))
                T = 200000 if not args.quick else 60000
                mjobs.append((beta, d, p, ib, idd, ip, T, 3 if args.quick else 14,
                              20000, min(60000, max(10000, 4 * k6)), kg))
    mc = list(pool.imap_unordered(mc_cell, mjobs))
    log["stages"]["mc"] = round(time.time() - t, 1)
    for m in mc:
        key = (m["beta"], m["d"], m["p"])
        cs = curves.get(key + ("slot",))
        pt, ps = priv.get(key + ("slot", 0)), priv.get(key + ("slot", 1))
        m["dp"] = [eps_of(cs, k) for k in m["kgrid"]]
        m["priv_tie"] = [eps_of(pt, k) for k in m["kgrid"]]
        m["priv_strict"] = [eps_of(ps, k) for k in m["kgrid"]]
    with open(res / "mc.json", "w") as f:
        json.dump(mc, f, indent=1)

    # 6. Composition et dérivation conditionnelle K_reg / registry_min_blocks.
    t = time.time()
    comp = []
    for beta in BETAS:
        for d in DENS:
            for p in (0.0, 1e-6, 1e-4, 1e-3, 1e-2):
                if (beta, d, p, "slot") not in curves or curves[(beta, d, p, "slot")] is None:
                    continue
                ks, _ = k_of(curves[(beta, d, p, "slot")], 1e-12)
                if ks is None or ks > K_LIMIT:
                    continue
                for tau in TAUS:
                    for eh in (1e-6, 1e-9):
                        for qb in (1, 256):
                            c = compose(curves, beta, d, p, tau, eh, qb)
                            if c:
                                c["mode"] = "b=b_min"
                                comp.append(c)
                            c = compose(curves, beta, d, p, tau, eh, qb, b=2880, kreg=7200)
                            if c:
                                c["mode"] = "controle a posteriori 7200/2880"
                                comp.append(c)
    with open(res / "composition.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(comp[0].keys()))
        w.writeheader()
        w.writerows(comp)
    log["stages"]["composition"] = round(time.time() - t, 1)

    # 7. Condition renforcée : d_min(beta, eps, p) tel que K_slots <= K_LIMIT.
    #    K_blocs ne dépend que de theta = a/h' (DP 'sym' exacte sur une grille
    #    de theta) ; K_slots ~= K_blocs/(a+h') (écart <= 2 % sur la grille).
    t = time.time()
    thetas = [round(x, 3) for x in np.arange(0.40, 0.921, 0.02)]
    tcur = {}
    for r in pool.imap_unordered(dp_theta, thetas):
        tcur[r["theta_in"]] = r["eps"]
    np.savez_compressed(res / "theta_curves.npz",
                        **{f"{k}": v for k, v in tcur.items() if v is not None})
    dmin = []
    for e in EPS:
        ths = sorted(tcur)
        ks = [k_of(tcur[th], e)[0] for th in ths]
        lk = np.log(np.array(ks, dtype=float))

        def ksym(th):
            if th < ths[0]:
                return math.exp(lk[0])
            if th > ths[-1]:
                return math.inf
            return math.exp(np.interp(th, ths, lk))
        for beta in BETAS:
            for p in PLATES:
                def kslots(d):
                    a, hp = eff(beta, d, p)
                    if a >= hp:
                        return math.inf
                    return ksym(a / hp) / (a + hp)
                lo, hi = beta / (1 - beta) / (1 - 2 * p) + 1e-9, 1.0
                if kslots(hi) > K_LIMIT:
                    dmin.append(dict(beta=beta, p_late=p, eps=e, d_cond=round(lo, 4),
                                     d_min=None, theta_max=None))
                    continue
                for _ in range(60):
                    mid = (lo + hi) / 2
                    if kslots(mid) > K_LIMIT:
                        lo = mid
                    else:
                        hi = mid
                a, hp = eff(beta, hi, p)
                dmin.append(dict(beta=beta, p_late=p, eps=e,
                                 d_cond=round(beta / (1 - beta) / (1 - 2 * p), 4),
                                 d_min=round(hi, 4), theta_max=round(a / hp, 4),
                                 margin_h_minus_a=round(hp - a, 4)))
    with open(res / "d-min.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["beta", "p_late", "eps", "d_cond", "d_min",
                                          "theta_max", "margin_h_minus_a"])
        w.writeheader()
        w.writerows(dmin)
    log["stages"]["theta"] = round(time.time() - t, 1)

    pool.close()
    pool.join()
    ru = __import__("resource").getrusage(__import__("resource").RUSAGE_CHILDREN)
    log["wall_s"] = round(time.time() - t0, 1)
    log["cpu_parent_s"] = round(time.process_time() - cpu0, 1)
    log["cpu_children_s"] = round(ru.ru_utime + ru.ru_stime, 1)
    log["dp_meta"] = {"|".join(map(str, k)): v for k, v in dpmeta.items()}
    log["skipped_dp"] = skipped
    with open(res / "run-log.json", "w") as f:
        json.dump(log, f, indent=1, default=str)
    render(res)
    print(json.dumps({k: log[k] for k in ("wall_s", "cpu_parent_s", "cpu_children_s", "stages")}))


if __name__ == "__main__":
    main()
