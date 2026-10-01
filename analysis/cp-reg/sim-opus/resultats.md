# CP_reg — résultats Monte-Carlo (opus, `cp_sim.py`)

Graine maîtresse `20260930` ; 110 essais × 300000 créneaux par configuration (chauffe 20000, queue 60000) ; cibles = chaque créneau de [chauffe, T−queue) ; 14 processus ; durée murale 100 s.

Les cibles d'un même essai sont corrélées : l'incertitude est donnée par la dispersion entre essais (σ des moyennes par essai). « 0 » = aucun événement ; la résolution est ~1/(nb de cibles) mais l'information effective est bien moindre.

Modes : `omni_tie` = adversaire omniscient (départ + révélation optimaux, égalité gagnée par équivoque/départage) ; `omni_strict` = idem, dépassement strict exigé ; `naive_tie` = course sans avance partant de la cible (référence §15).


## β = 0.1, D = 0 (Δ/τ = 0), densité honnête d = 1.0

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.564 | 10 | 22 (ext 23) | 35 | 47 |
| omni_tie | blocks | -1.12 | 7 | 12 (ext 13) | 19 | 25 |
| omni_tie | nonempty | -0.564 | 11 | 23 (ext 24) | 36 | 48 |
| omni_strict | slots | -0.5855 | 9 | 19 (ext 20) | 32 | 44 |
| omni_strict | blocks | -1.16 | 5 | None (ext 11) | 17 | 23 |
| omni_strict | nonempty | -0.5855 | 10 | 20 (ext 21) | 33 | 45 |
| naive_tie | slots | -0.5747 | 11 | 23 (ext 23) | 35 | 47 |
| naive_tie | blocks | -1.149 | 6 | 12 (ext 12) | 18 | 24 |
| naive_tie | nonempty | -0.5747 | 12 | 24 (ext 24) | 36 | 48 |

Contrôle de dispersion : ε_omni_tie(1000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).


## β = 0.1, D = 0 (Δ/τ = 0), densité honnête d = 0.4

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 5.01e-03 | 5.75e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 2.66e-03 | 3.36e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 3.45e-03 | 3.99e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 1.81e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 7.56e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 8.88e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.07836 | 68 | 156 (ext 154) | 242 | 331 |
| omni_tie | blocks | -0.4095 | 16 | 33 (ext 33) | 50 | 67 |
| omni_tie | nonempty | -0.2069 | 30 | 63 (ext 64) | 97 | 130 |
| omni_strict | slots | -0.07676 | 61 | 151 (ext 149) | 239 | 329 |
| omni_strict | blocks | -0.3966 | 14 | 32 (ext 32) | 49 | 66 |
| omni_strict | nonempty | -0.2032 | 27 | 62 (ext 61) | 95 | 129 |
| naive_tie | slots | -0.07904 | 64 | 156 (ext 149) | 236 | 324 |
| naive_tie | blocks | -0.4046 | 15 | 32 (ext 32) | 49 | 66 |
| naive_tie | nonempty | -0.2023 | 30 | 64 (ext 63) | 97 | 131 |

Contrôle de dispersion : ε_omni_tie(3000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).


## β = 0.1, D = 1 (Δ/τ = 1), densité honnête d = 1.0

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 4.13e-08 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.3032 | 23 | 44 (ext 46) | 68 | 91 |
| omni_tie | blocks | -0.8358 | 10 | 17 (ext 18) | 26 | 34 |
| omni_tie | nonempty | -0.3032 | 24 | 45 (ext 47) | 69 | 92 |
| omni_strict | slots | -0.3116 | 19 | 39 (ext 41) | 63 | 85 |
| omni_strict | blocks | -0.8371 | 8 | 15 (ext 16) | 24 | 33 |
| omni_strict | nonempty | -0.3116 | 20 | 40 (ext 42) | 64 | 86 |
| naive_tie | slots | -0.3069 | 20 | 41 (ext 43) | 65 | 88 |
| naive_tie | blocks | -0.8555 | 8 | 16 (ext 16) | 24 | 32 |
| naive_tie | nonempty | -0.3069 | 21 | 42 (ext 44) | 66 | 89 |

Contrôle de dispersion : ε_omni_tie(1000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).


## β = 0.1, D = 1 (Δ/τ = 1), densité honnête d = 0.4

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 3.14e-02 | 1.60e-03 | 8.26e-07 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 1.73e-02 | 8.58e-04 | 2.89e-07 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 1.85e-02 | 9.18e-04 | 2.89e-07 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 1.89e-03 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 9.07e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 9.03e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.06744 | 108 | 199 (ext 212) | 314 | 417 |
| omni_tie | blocks | -0.3576 | 23 | 39 (ext 42) | 62 | 81 |
| omni_tie | nonempty | -0.1522 | 51 | 89 (ext 97) | 142 | 188 |
| omni_strict | slots | -0.06808 | 98 | 191 (ext 200) | 302 | 403 |
| omni_strict | blocks | -0.3527 | 20 | 37 (ext 40) | 60 | 79 |
| omni_strict | nonempty | -0.1583 | 46 | 84 (ext 90) | 134 | 178 |
| naive_tie | slots | -0.06808 | 99 | 193 (ext 202) | 303 | 405 |
| naive_tie | blocks | -0.3465 | 20 | 38 (ext 40) | 60 | 80 |
| naive_tie | nonempty | -0.1551 | 47 | 86 (ext 92) | 136 | 181 |

Contrôle de dispersion : ε_omni_tie(3000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).


## β = 0.2, D = 0 (Δ/τ = 0), densité honnête d = 1.0

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 2.48e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 6.61e-07 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 1.40e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 4.82e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 1.64e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 2.49e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.2375 | 25 | 53 (ext 54) | 83 | 112 |
| omni_tie | blocks | -0.474 | 14 | 28 (ext 29) | 43 | 58 |
| omni_tie | nonempty | -0.2375 | 26 | 54 (ext 55) | 84 | 113 |
| omni_strict | slots | -0.2491 | 23 | 49 (ext 50) | 78 | 106 |
| omni_strict | blocks | -0.4968 | 12 | 25 (ext 26) | 40 | 54 |
| omni_strict | nonempty | -0.2491 | 24 | 50 (ext 51) | 79 | 107 |
| naive_tie | slots | -0.2417 | 25 | 53 (ext 53) | 81 | 110 |
| naive_tie | blocks | -0.4834 | 13 | 27 (ext 27) | 41 | 56 |
| naive_tie | nonempty | -0.2417 | 26 | 54 (ext 54) | 82 | 111 |

Contrôle de dispersion : ε_omni_tie(1000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).


## β = 0.2, D = 0 (Δ/τ = 0), densité honnête d = 0.4

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 3.37e-01 | 1.41e-01 | 2.78e-02 | 5.84e-03 | 2.75e-04 | 5.37e-07 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 2.78e-01 | 1.15e-01 | 2.24e-02 | 4.68e-03 | 2.17e-04 | 2.89e-07 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 2.31e-01 | 9.16e-02 | 1.71e-02 | 3.47e-03 | 1.49e-04 | 3.31e-07 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 2.32e-01 | 3.49e-02 | 1.80e-03 | 7.04e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 1.85e-01 | 2.74e-02 | 1.40e-03 | 4.99e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 1.42e-01 | 1.95e-02 | 9.52e-04 | 2.67e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.01696 | 418 | 790 (ext 825) | 1233 | 1640 |
| omni_tie | blocks | -0.06957 | 110 | 194 (ext 210) | 310 | 409 |
| omni_tie | nonempty | -0.03461 | 216 | 384 (ext 417) | 617 | 816 |
| omni_strict | slots | -0.01751 | 404 | 783 (ext 799) | 1193 | 1588 |
| omni_strict | blocks | -0.07241 | 106 | 192 (ext 203) | 298 | 393 |
| omni_strict | nonempty | -0.03613 | 209 | 382 (ext 402) | 593 | 784 |
| naive_tie | slots | -0.01806 | 383 | 766 (ext 766) | 1149 | 1531 |
| naive_tie | blocks | -0.07015 | 100 | 186 (ext 198) | 297 | 395 |
| naive_tie | nonempty | -0.03508 | 200 | 372 (ext 396) | 593 | 790 |

Contrôle de dispersion : ε_omni_tie(3000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).


## β = 0.2, D = 1 (Δ/τ = 1), densité honnête d = 1.0

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 6.50e-03 | 7.90e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 3.59e-03 | 4.24e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 3.32e-03 | 4.12e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 6.02e-03 | 4.13e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 3.11e-03 | 2.56e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 2.71e-03 | 2.19e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.09022 | 72 | 149 (ext 148) | 225 | 301 |
| omni_tie | blocks | -0.2436 | 28 | 56 (ext 57) | 85 | 113 |
| omni_tie | nonempty | -0.09022 | 73 | 150 (ext 149) | 226 | 302 |
| omni_strict | slots | -0.08902 | 65 | 145 (ext 142) | 220 | 297 |
| omni_strict | blocks | -0.2413 | 25 | 54 (ext 54) | 83 | 111 |
| omni_strict | nonempty | -0.08902 | 66 | 146 (ext 143) | 221 | 298 |
| naive_tie | slots | -0.08887 | 64 | 146 (ext 142) | 219 | 297 |
| naive_tie | blocks | -0.2377 | 25 | 54 (ext 54) | 83 | 112 |
| naive_tie | nonempty | -0.08887 | 65 | 147 (ext 143) | 220 | 298 |

Contrôle de dispersion : ε_omni_tie(1000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).


## β = 0.2, D = 1 (Δ/τ = 1), densité honnête d = 0.4

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 7.87e-01 | 6.44e-01 | 4.47e-01 | 3.17e-01 | 1.66e-01 | 6.59e-02 | 3.64e-02 | 8.43e-03 | 1.94e-03 | 5.87e-05 | 0 | 0 | 0 |
| omni_strict | 7.31e-01 | 5.93e-01 | 4.07e-01 | 2.88e-01 | 1.49e-01 | 5.90e-02 | 3.27e-02 | 7.50e-03 | 1.72e-03 | 5.06e-05 | 0 | 0 | 0 |
| naive_tie | 5.90e-01 | 4.53e-01 | 2.93e-01 | 2.00e-01 | 9.95e-02 | 3.81e-02 | 2.07e-02 | 4.62e-03 | 1.01e-03 | 2.74e-05 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 6.91e-01 | 4.28e-01 | 2.06e-01 | 1.03e-01 | 5.29e-02 | 1.46e-02 | 9.81e-04 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 6.35e-01 | 3.88e-01 | 1.85e-01 | 9.22e-02 | 4.71e-02 | 1.29e-02 | 8.74e-04 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 4.82e-01 | 2.71e-01 | 1.22e-01 | 5.85e-02 | 2.95e-02 | 7.85e-03 | 5.10e-04 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.004092 | 2195 | 3407 (ext 3909) | 5597 | 7285 |
| omni_tie | blocks | -0.01741 | 499 | 783 (ext 902) | 1299 | 1695 |
| omni_tie | nonempty | -0.007647 | 1148 | 1811 (ext 2066) | 2969 | 3872 |
| omni_strict | slots | -0.004093 | 2160 | 3402 (ext 3877) | 5565 | 7253 |
| omni_strict | blocks | -0.01739 | 491 | 781 (ext 895) | 1292 | 1689 |
| omni_strict | nonempty | -0.007634 | 1130 | 1809 (ext 2051) | 2956 | 3861 |
| naive_tie | slots | -0.003682 | 2004 | 3404 (ext 3905) | 5780 | 7656 |
| naive_tie | blocks | -0.01641 | 453 | 781 (ext 881) | 1302 | 1723 |
| naive_tie | nonempty | -0.007083 | 1048 | 1810 (ext 2038) | 3013 | 3988 |

Contrôle de dispersion : ε_omni_tie(3000 créneaux) = 5.868e-05 ± 3.2e-05 (σ entre essais).


## β = 0.25, D = 0 (Δ/τ = 0), densité honnête d = 1.0

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 1.94e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 1.19e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 1.21e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 1.38e-03 | 1.65e-07 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 7.05e-04 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 7.44e-04 | 8.26e-08 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.1476 | 40 | 89 (ext 86) | 133 | 180 |
| omni_tie | blocks | -0.2948 | 22 | 46 (ext 45) | 68 | 92 |
| omni_tie | nonempty | -0.1476 | 41 | 90 (ext 87) | 134 | 181 |
| omni_strict | slots | -0.1444 | 36 | 87 (ext 84) | 131 | 179 |
| omni_strict | blocks | -0.2877 | 19 | 44 (ext 43) | 67 | 91 |
| omni_strict | nonempty | -0.1444 | 37 | 88 (ext 85) | 132 | 180 |
| naive_tie | slots | -0.1501 | 39 | 89 (ext 83) | 129 | 175 |
| naive_tie | blocks | -0.3002 | 20 | 45 (ext 42) | 65 | 88 |
| naive_tie | nonempty | -0.1501 | 40 | 90 (ext 84) | 130 | 176 |

Contrôle de dispersion : ε_omni_tie(1000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).


## β = 0.25, D = 0 (Δ/τ = 0), densité honnête d = 0.4

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 8.09e-01 | 6.82e-01 | 4.97e-01 | 3.69e-01 | 2.09e-01 | 9.35e-02 | 5.53e-02 | 1.53e-02 | 4.07e-03 | 3.13e-04 | 5.93e-05 | 0 | 0 |
| omni_strict | 7.70e-01 | 6.44e-01 | 4.65e-01 | 3.44e-01 | 1.94e-01 | 8.64e-02 | 5.10e-02 | 1.41e-02 | 3.71e-03 | 3.05e-04 | 5.43e-05 | 0 | 0 |
| naive_tie | 6.31e-01 | 4.99e-01 | 3.39e-01 | 2.42e-01 | 1.31e-01 | 5.66e-02 | 3.29e-02 | 9.02e-03 | 2.40e-03 | 1.85e-04 | 4.14e-05 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 7.68e-01 | 5.43e-01 | 3.19e-01 | 1.92e-01 | 1.18e-01 | 4.54e-02 | 6.94e-03 | 3.76e-04 | 1.10e-04 | 0 | 0 | 0 |
| omni_strict | 7.25e-01 | 5.07e-01 | 2.96e-01 | 1.77e-01 | 1.09e-01 | 4.16e-02 | 6.32e-03 | 3.69e-04 | 1.06e-04 | 0 | 0 | 0 |
| naive_tie | 5.67e-01 | 3.64e-01 | 1.99e-01 | 1.15e-01 | 6.90e-02 | 2.60e-02 | 3.88e-03 | 2.16e-04 | 6.40e-05 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.002364 | 2544 | 4331 (ext 5484) | 8406 | 11329 |
| omni_tie | blocks | -0.009145 | 707 | 1189 (ext 1468) | 2224 | 2979 |
| omni_tie | nonempty | -0.004556 | 1403 | 2374 (ext 2931) | 4447 | 5964 |
| omni_strict | slots | -0.002337 | 2521 | 4281 (ext 5492) | 8448 | 11404 |
| omni_strict | blocks | -0.009096 | 700 | 1175 (ext 1465) | 2225 | 2984 |
| omni_strict | nonempty | -0.004552 | 1390 | 2349 (ext 2920) | 4438 | 5955 |
| naive_tie | slots | -0.002251 | 2338 | 4289 (ext 5399) | 8469 | 11538 |
| naive_tie | blocks | -0.008721 | 647 | 1176 (ext 1439) | 2231 | 3023 |
| naive_tie | nonempty | -0.00436 | 1294 | 2352 (ext 2878) | 4462 | 6046 |

Contrôle de dispersion : ε_omni_tie(3000 créneaux) = 3.125e-04 ± 1.3e-04 (σ entre essais).


## β = 0.25, D = 1 (Δ/τ = 1), densité honnête d = 1.0

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 7.27e-02 | 7.66e-03 | 8.98e-05 | 3.14e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 4.92e-02 | 5.09e-03 | 5.36e-05 | 2.98e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 3.98e-02 | 4.01e-03 | 4.31e-05 | 1.20e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 7.17e-02 | 2.07e-03 | 8.60e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 4.69e-02 | 1.31e-03 | 8.10e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 3.64e-02 | 9.88e-04 | 5.29e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.03529 | 146 | 350 (ext 333) | 528 | 724 |
| omni_tie | blocks | -0.09343 | 57 | 133 (ext 127) | 201 | 275 |
| omni_tie | nonempty | -0.03529 | 147 | 351 (ext 334) | 529 | 725 |
| omni_strict | slots | -0.0341 | 137 | 346 (ext 329) | 531 | 734 |
| omni_strict | blocks | -0.08981 | 53 | 132 (ext 126) | 203 | 279 |
| omni_strict | nonempty | -0.0341 | 138 | 347 (ext 330) | 532 | 735 |
| naive_tie | slots | -0.04132 | 132 | 325 (ext 296) | 464 | 631 |
| naive_tie | blocks | -0.1091 | 50 | 123 (ext 113) | 176 | 239 |
| naive_tie | nonempty | -0.04132 | 133 | 326 (ext 297) | 465 | 632 |

Contrôle de dispersion : ε_omni_tie(1000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).


## β = 0.25, D = 1 (Δ/τ = 1), densité honnête d = 0.4

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 72600000.

**RÉGIME NON SÛR** : la branche privée rattrape la vue honnête jusqu'à la fin de presque tous les essais (β ≥ taux de croissance honnête sous retard maximal). ε(K) ≈ 1 pour tout K ; aucune profondeur ne suffit.


## β = 0.2, D = 0 (Δ/τ = 0), densité honnête d = 0.7

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 2.84e-03 | 1.83e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 1.73e-03 | 8.35e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 1.87e-03 | 1.04e-05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 2.86e-03 | 1.82e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 1.53e-03 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 1.55e-03 | 3.72e-07 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.08938 | 61 | 137 (ext 136) | 213 | 291 |
| omni_tie | blocks | -0.2562 | 24 | 52 (ext 51) | 78 | 105 |
| omni_tie | nonempty | -0.1278 | 46 | 101 (ext 100) | 154 | 208 |
| omni_strict | slots | -0.09596 | 56 | 130 (ext 126) | 198 | 270 |
| omni_strict | blocks | -0.288 | 22 | 46 (ext 46) | 70 | 94 |
| omni_strict | nonempty | -0.1423 | 42 | 92 (ext 91) | 140 | 188 |
| naive_tie | slots | -0.09403 | 57 | 131 (ext 129) | 202 | 275 |
| naive_tie | blocks | -0.2759 | 22 | 47 (ext 47) | 72 | 97 |
| naive_tie | nonempty | -0.138 | 44 | 94 (ext 94) | 144 | 194 |

Contrôle de dispersion : ε_omni_tie(3000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).


## β = 0.2, D = 1 (Δ/τ = 1), densité honnête d = 0.7

Cibles : 24,200,000 ; révélations tardives en fin d'essai (biais de troncature) : 0.


ε(K) — K en **créneaux**

| mode | 50 | 100 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 3000 | 4000 | 5000 | 7200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 9.53e-02 | 1.31e-02 | 3.05e-04 | 8.72e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 6.49e-02 | 8.78e-03 | 2.02e-04 | 6.53e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 5.45e-02 | 7.13e-03 | 1.58e-04 | 4.13e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

ε(K) — K en **blocs (vue victime)**

| mode | 20 | 50 | 100 | 150 | 200 | 300 | 500 | 800 | 1000 | 1500 | 2000 | 2880 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omni_tie | 5.83e-02 | 1.38e-03 | 4.34e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| omni_strict | 3.79e-02 | 8.71e-04 | 3.72e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| naive_tie | 2.99e-02 | 6.66e-04 | 1.98e-06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Queue exponentielle ajustée (ε ≤ 3e-3, ≥ 30 cibles) et extrapolation :

| mode | unité | pente ln ε / K | K(1e-3) mesuré | K(1e-6) | K(1e-9) extrap. | K(1e-12) extrap. |
|---|---|---|---|---|---|---|
| omni_tie | slots | -0.03187 | 169 | 387 (ext 379) | 596 | 813 |
| omni_tie | blocks | -0.1098 | 53 | 116 (ext 115) | 178 | 241 |
| omni_tie | nonempty | -0.04225 | 130 | 292 (ext 290) | 453 | 617 |
| omni_strict | slots | -0.03083 | 157 | 382 (ext 374) | 598 | 822 |
| omni_strict | blocks | -0.1062 | 49 | 114 (ext 113) | 178 | 243 |
| omni_strict | nonempty | -0.0409 | 122 | 289 (ext 285) | 454 | 623 |
| naive_tie | slots | -0.03476 | 152 | 377 (ext 348) | 547 | 746 |
| naive_tie | blocks | -0.1154 | 47 | 112 (ext 106) | 166 | 226 |
| naive_tie | nonempty | -0.0452 | 118 | 286 (ext 268) | 421 | 574 |

Contrôle de dispersion : ε_omni_tie(3000 créneaux) = 0.000e+00 ± 0.0e+00 (σ entre essais).

