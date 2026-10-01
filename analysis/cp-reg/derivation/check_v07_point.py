#!/usr/bin/env python3
"""Recalcule la garantie composée au point retenu par N-SPEC v0.7 (K_reg = 2 750, b = registry_min_blocks = maxreorg = 1 630),
profil B (β = 0,30 ; d = 0,70), p_late = 10⁻², τ = 10 s, ε_H = 10⁻⁹, Q_B ∈ {1, 256}, avec la fonction `compose` de derive_k.py
et les courbes DP publiées (results/dp_curves.npz). Aucune nouvelle simulation.  Usage : python3 check_v07_point.py"""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import derive_k as dk
z = np.load(Path(__file__).parent / "results" / "dp_curves.npz")
curves = {}
for k in z.files:
    b, d, p, kind = k.split("_")
    curves[(float(b), float(d), float(p), kind)] = z[k]
for qb in (1, 256):
    for kreg, b in ((2739, 1629), (2740, 1630), (2750, 1630)):
        r = dk.compose(curves, 0.3, 0.7, 0.01, 10, 1e-9, qb, b=b, kreg=kreg)
        print(json.dumps({k: r[k] for k in ("Q_B", "K_reg_used", "b", "b_max_given_Kreg", "eps_epoch_composed", "eps_H_composed", "extrapolated")}))
