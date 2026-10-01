# CP_reg — seconde analyse indépendante (opus)

30 septembre 2026. Mandat : `MANDAT-CP-REG.md`. Entrées lues : N-SPEC v0.6 §2.5, §3.2, §5.1–5.9, §7.1–7.3, §9.3–9.6, §15, §17, §23.4 ; RAPPORT-TLA v0.6 §4. Analyse conduite **à l'aveugle** de `CP-REG-codex.md` et de `cp-reg/sim/`.
Code : `cp-reg/sim-opus/cp_bound.py` (calcul analytique exact, numpy), `cp-reg/sim-opus/cp_sim.py` (Monte-Carlo, stdlib, graine 20260930), sorties `table_analytique.json` et `resultats.md`.

## 0. Verdict en une page

1. **Si Δ + dérive d'horloge ≤ 5 s** (bloc honnête livré avant la réservation du créneau suivant, §7.2), le modèle de N est exactement le modèle synchrone « un leader par créneau » de Blum–Kiayias–Moore–Quader–Russell. On en tire une borne **exacte** ε(K) contre un adversaire omniscient (calendrier entier connu), qui retient ses blocs, équivoque et gagne les égalités. Dans ce régime, 7 200 créneaux / 2 880 blocs couvrent ε = 10⁻¹² tant que β ≤ 0,30 avec d ≥ 0,7, ou β ≤ 0,20 avec d ≥ 0,4.
2. **La limite dure, c'est la densité honnête.** β est une part du poids **total** du tirage (un créneau d'un honnête hors ligne reste vide, sans remplaçant). La condition nécessaire est donc h = (1−β)·d > β. **À d = 0,2, aucun K n'existe pour β ≥ 0,20. À β = 0,25 et d = 0,4, il faut K ≈ 19 700 créneaux / 10 800 blocs pour 10⁻¹²** : 7 200 / 2 880 sont trop courts (ε ≈ 3·10⁻⁵ et 5·10⁻⁴). Ce n'est pas un artefact de méthode : l'attaque privée simulée atteint ces ordres de grandeur.
3. **Au-delà de Δ ≈ 5 s (Δ/τ ≥ 1), aucune borne prouvable n'est obtenue pour β ≥ 17 %**, quelle que soit la densité. La réduction standard (blocs honnêtes « non gloutons » comptés adverses) échoue. Il ne reste que des estimations, non des bornes. Pour β = 0,20, d = 0,7, Δ/τ = 1 et ε = 10⁻⁹, l'estimation est de **880 créneaux / 672 blocs** ; l'attaque simulée atteint ≈ 600 créneaux.
4. **Le compte de la règle A devient manipulable par l'adversaire à densité ≈ 0,2**, indépendamment de K : dans la fenêtre minimale de 14 400 créneaux, le seuil 2 880 exige h ≥ 0,2. Autour de ce seuil, CP_reg échoue « à volonté » (contre-exemple TLA de fermeture, généralisé).
5. **Un compte de blocs est gonflable par équivoque** (un même créneau adverse sert sur la branche publique et sur la branche privée). Une règle de confirmation en blocs n'est donc saine que si elle compte des **créneaux non vides**. C'est ce que fait la colonne « blocs » ci-dessous. La course idéale du §15 (k = 77 ⇒ 1,3·10⁻¹⁶) compte des blocs honnêtes, que la victime ne peut pas distinguer. Avec équivoque, 77 blocs valent ε ≈ 10⁻⁶ (borne) ou ≈ 10⁻⁸ (attaque privée) : il y a 8 à 10 ordres de grandeur d'écart.

## 1. Modèle formel (a)

### 1.1 Créneaux et loterie

Créneaux de durée τ = 6 s. Chaque créneau a **un** producteur tiré par poids (§7.1), sans remplaçant en cas d'absence. Les tirages sont i.i.d. conditionnellement à la graine. Chaque créneau est :

| symbole | probabilité | sens |
|---|---|---|
| `A` | β | producteur adverse (toujours en ligne, hypothèse pire cas) |
| `H` | h = (1−β)·d | producteur honnête en ligne |
| `⊥` | (1−β)(1−d) | producteur honnête hors ligne : créneau vide |

- **β** = part adverse du poids **total** du tirage, poids inactif compris au dénominateur. C'est la seule lecture compatible avec « aucun remplacement du producteur absent ».
- **d** = densité honnête = 1 − α, où α est la part du poids honnête indisponible, **DoS ciblé compris** (le calendrier est public). α et d sont un seul paramètre.
- La part adverse du poids **actif** vaut β_act = β / (β + h). Par exemple, β = 0,20 avec d = 0,4 donne β_act = 0,385.

### 1.2 Livraison et retard en créneaux

Un bloc du créneau s est signé avant t_s + 2 s et le parent du créneau s + j est choisi à t_s + j·τ + 1 s. Le bloc honnête est donc vu par tous les producteurs honnêtes à partir de s + D + 1, avec :

```
D = ⌈(Δ + 2σ_horloge + 1 s)/τ⌉ − 1       (créneaux « aveugles »)
Δ/τ = 0 ou 0,5  (Δ ≤ 3 s)  ⇒ D = 0
Δ/τ = 1         (Δ = 6 s)  ⇒ D = 1
Δ/τ = 2         (Δ = 12 s) ⇒ D = 2
```

Les phases 1 s / 2 s du §7.2 absorbent donc Δ ≤ 5 s : **Δ/τ = 0,5 donne exactement les mêmes K que Δ/τ = 0.**

### 1.3 Adversaire

Il est omniscient sur la chaîne caractéristique (calendrier public). Il retient ses blocs indéfiniment et les révèle à l'instant de son choix. Il choisit le point de départ de sa branche parmi tout le passé (arrêt optimal) et retarde chaque bloc honnête jusqu'à Δ. Il équivoque (plusieurs blocs par créneau adverse, sur des branches différentes) et gagne les égalités de score. Justification de ce dernier point : deux variantes équivoques d'un même créneau ont le même `tie` (seed, slot, producer, §9.3), donc un ex æquo persistant où chaque nœud garde sa branche (§9.4) ; sinon le départage est public et l'adversaire choisit ses fourches en conséquence.

Les honnêtes produisent à leurs créneaux et suivent Rank (score, puis départage public).

### 1.4 Événement mesuré

Coupure c = `snapshot_cut(e)`. L'échec est que deux vues honnêtes (ou une même vue à deux instants) aient, à un moment quelconque postérieur à c + K, des préfixes `Old_e` différents. Il est inclus dans l'événement « deux branches viables disjointes sur [c, t] » de la théorie des fourches, ce qui rend la borne conservatrice.

K se compte de deux façons :

- **K créneaux**, depuis la coupure ;
- **K blocs** = nombre de **créneaux non vides** depuis la coupure. Si une branche porte k blocs après c, au moins k créneaux non vides se sont écoulés, même si l'adversaire gonfle la branche par équivoque. C'est donc la seule unité de bloc saine.

## 2. Bornes analytiques (b)

### 2.1 Régime D = 0 : borne exacte

Soit w la suite des symboles non vides, x le passé avant c et y le futur. On définit :

```
reach  ρ(ε)=0 ;  ρ(wA)=ρ(w)+1 ;  ρ(wh)=max(ρ(w)−1, 0)
marge  μ_x(ε)=ρ(x) ;  μ_x(yA)=μ_x(y)+1 ;
       μ_x(yh)= 0 si μ_x(y)=0 et ρ(xy)>0,  sinon μ_x(y)−1
```

Théorème (Blum et al., SODA 2020, départage adverse) : la coupure n'est pas stable après y si et seulement si μ_x(y) ≥ 0. D'où :

```
ε(K) = Pr[ ∃ t ≥ K : μ_t ≥ 0 ]
ρ(x) ~ loi stationnaire :  Pr[ρ ≥ r] = (β/h)^r
Condition nécessaire et suffisante d'existence de K :  h > β  ⇔  d > β/(1−β)
```

`cp_bound.py` calcule ε(K) **exactement**, par chaîne de Markov sur (ρ, μ). Les troncatures sont conservatrices (masse tronquée comptée en échec) et la DP a été recoupée par un Monte-Carlo direct des récurrences (écarts < 1 %). La forme lisible est :

```
ε(K) ≈ C · e^(−λ K),  C ∈ [0,3 ; 0,7]
K(ε) ≈ ln(C/ε) / λ
λ_attaque privée = −ln(1 − (√h − √β)²)    par créneau (exact asymptotiquement)
λ_marge ≈ 0,6 à 0,75 × λ_privée           (valeurs exactes ci-dessous)
```

| β | d | λ créneau | λ bloc | λ privée (formule) |
|---:|---:|---:|---:|---:|
| 0,10 | 1,0 | 0,384 | 0,384 | 0,511 |
| 0,20 | 1,0 | 0,165 | 0,165 | 0,223 |
| 0,20 | 0,7 | 0,069 | 0,092 | 0,095 |
| 0,20 | 0,4 | 0,0095 | 0,018 | 0,014 |
| 0,25 | 0,4 | 0,0014 | 0,0025 | 0,0023 |
| 0,30 | 0,7 | 0,016 | 0,020 | 0,023 |

Près du seuil (h → β), λ ≈ (h − β)²/(4h) → 0 : K diverge en (h − β)⁻².

### 2.2 Régime D ≥ 1 : pas de borne prouvable utile

On définit un créneau honnête **glouton** comme le premier créneau honnête situé à plus de D créneaux du glouton précédent. Son bloc est plus long que tous les gloutons antérieurs, ce qui donne un taux de croissance g = h/(1 + hD). Les autres créneaux honnêtes (non gloutons) peuvent être vus sans le dernier glouton.

- **Réduction prouvable** (non glouton ⇒ A, famille Praos) : il faut β + (h − g) < g. Pour D = 1, cela donne β < h(1−h)/(1+h), dont le maximum vaut **0,172** (atteint à h = 0,41). **Aucune borne pour β ≥ 0,172, à toute densité** ; pour β = 0,10, il faut en plus h ∈ ]0,13 ; 0,77[. Pour D = 2, aucune configuration de la grille n'est bornée.
- **Estimation** (non glouton ⇒ ignoré ; ce n'est pas une borne) : condition g > β, même DP. C'est la colonne « est. » de la table.

L'écart entre les deux vient de ce que le retard permet à l'adversaire de récolter les blocs honnêtes non gloutons sur sa branche privée quand elle est à égalité ou en tête (on le montre sur un exemple). La réduction les lui donne tous ; la vérité est entre les deux, et **aucune borne publiable ne la fixe**. La conséquence normative est en H_N-2.

### 2.3 Croissance et qualité de chaîne

- **CG** : sur toute fenêtre de k créneaux, chaque vue honnête croît d'au moins (1 − δ)·g·k blocs, sauf avec une probabilité ≈ e^(−δ²gk/3) (Chernoff sur le renouvellement des gloutons), avec g = h/(1+hD).
- **CQ** : sur un long segment, la fraction honnête est au moins 1 − q/g, où q = β (D = 0 ou estimation) ou q = β + h − g (prouvable).

| β | d | g (D=0) | CQ D=0 | g (D=1) | CQ D=1 (est.) | blocs honnêtes / 14 400 créneaux (D=0) |
|---:|---:|---:|---:|---:|---:|---:|
| 0,10 | 1,0 | 0,90 | 0,89 | 0,47 | 0,79 | 12 960 |
| 0,20 | 0,7 | 0,56 | 0,64 | 0,36 | 0,44 | 8 064 |
| 0,20 | 0,4 | 0,32 | 0,38 | 0,24 | 0,18 | 4 608 |
| 0,25 | 0,4 | 0,30 | 0,17 | 0,23 | — (g<β) | 4 320 |
| 0,20 | 0,2 | 0,16 | — (h<β) | 0,14 | — | 2 304 |

### 2.4 Ce que calendrier public, rétention et équivoque changent par rapport au §15

| Effet | Mécanisme | Ordre de grandeur |
|---|---|---|
| Avance accumulée (rétention, départ choisi) | ρ(x) stationnaire géométrique au lieu de a = 0 | ε × 1,3 à 2 ; K + 3 à 5 % (simulation : `omni_tie` contre `naive_tie`) |
| Calendrier connu pour une coupure **fixée** | la théorie des fourches suppose déjà un adversaire omniscient | aucun effet supplémentaire |
| Équilibre à deux branches, départage adverse | marge μ au lieu de la course privée | K × 1,3 à 1,75 (borne contre attaque) |
| Gonflement du compte par équivoque | un créneau adverse sert aux deux branches | K_blocs : ×2 à ×2,5 face à un compte de blocs honnêtes |
| Choix de l'époque attaquée, grinding de graine | union sur E époques × Q_B chemins | ε_global ≤ E·Q_B·ε(K) ; 10 ans × 256 ⇒ facteur ≈ 10⁶ |
| **DoS ciblé des prochains leaders honnêtes** (calendrier public) | fait baisser d exactement là où l'adversaire attaque | c'est le vrai coût du calendrier public : d doit être un **minimum sous attaque** sur toute fenêtre de longueur K, pas une moyenne |
| Avance acquise avant stabilisation | rétention pendant une asynchronie de durée T_a | avance ≤ β·T_a/τ blocs, résorbée en ≈ β·T_a/(τ(g−β)) créneaux |

**Pour ε_CP = 10⁻⁶ sur 10 ans avec Q_B = 256, il faut ε(K) ≈ 10⁻¹² par coupure : c'est la colonne pertinente.**

## 3. Tables de dérivation (c)

Chaque cellule donne **K créneaux / K blocs** (créneaux non vides). La colonne Δ/τ ∈ {0 ; 0,5} (D = 0) est exacte. « prouv. » est la réduction prouvable, « est. » l'estimation. ∞ signifie qu'aucun K n'existe (condition de 2.1 ou 2.2 violée) ; « q.c. » signifie quasi critique (β/g = 0,98, K > 5·10⁴). Un astérisque marque une valeur extrapolée log-linéairement.

### ε = 10⁻⁶

| β | d | Δ/τ ≤ 0,5 | Δ/τ=1 prouv. | Δ/τ=1 est. | Δ/τ=2 prouv. | Δ/τ=2 est. |
|---:|---:|---:|---:|---:|---:|---:|
| 0,10 | 1,0 | 33 / 33 | ∞ | 73 / 73 | ∞ | 151 / 151 |
| 0,10 | 0,7 | 65 / 46 | 5 482 / 4 048 | 123 / 90 | ∞ | 234 / 173 |
| 0,10 | 0,4 | 206 / 92 | 1 963 / 925 | 350 / 162 | ∞ | 628 / 294 |
| 0,10 | 0,2 | 1 625 / 451 | 14 022 / 3 955* | 3 121 / 876 | ∞ | 7 244 / 2 042 |
| 0,20 | 1,0 | 78 / 78 | ∞ | 243 / 243 | ∞ | 957 / 957 |
| 0,20 | 0,7 | 189 / 142 | ∞ | 579 / 442 | ∞ | 2 835 / 2 165 |
| 0,20 | 0,4 | 1 391 / 720 | ∞ | 8 467 / 4 416 | ∞ | ∞ |
| 0,20 | 0,2 | ∞ | ∞ | ∞ | ∞ | ∞ |
| 0,25 | 1,0 | 124 / 124 | ∞ | 521 / 521 | ∞ | 5 373 / 5 373 |
| 0,25 | 0,7 | 360 / 277 | ∞ | 1 932 / 1 502 | ∞ | q.c. |
| 0,25 | 0,4 | 9 696 / 5 330 | ∞ | ∞ | ∞ | ∞ |
| 0,25 | 0,2 | ∞ | ∞ | ∞ | ∞ | ∞ |
| 0,30 | 1,0 | 211 / 211 | ∞ | 1 520 / 1 520 | ∞ | ∞ |
| 0,30 | 0,7 | 835 / 658 | ∞ | 25 540 / 20 192* | ∞ | ∞ |
| 0,30 | ≤0,4 | ∞ | ∞ | ∞ | ∞ | ∞ |

### ε = 10⁻⁹

| β | d | Δ/τ ≤ 0,5 | Δ/τ=1 prouv. | Δ/τ=1 est. | Δ/τ=2 prouv. | Δ/τ=2 est. |
|---:|---:|---:|---:|---:|---:|---:|
| 0,10 | 1,0 | 51 / 51 | ∞ | 112 / 112 | ∞ | 230 / 230 |
| 0,10 | 0,7 | 100 / 70 | 8 246 / 6 089 | 188 / 137 | ∞ | 356 / 264 |
| 0,10 | 0,4 | 317 / 140 | 2 966 / 1 399 | 535 / 247 | ∞ | 956 / 447 |
| 0,10 | 0,2 | 2 476 / 686 | 21 197 / 5 980* | 4 741 / 1 331 | ∞ | 10 974 / 3 093 |
| 0,20 | 1,0 | 120 / 120 | ∞ | 369 / 369 | ∞ | 1 449 / 1 449 |
| **0,20** | **0,7** | **289 / 217** | **∞** | **880 / 672** | ∞ | 4 288 / 3 275 |
| 0,20 | 0,4 | 2 115 / 1 095 | ∞ | 12 809 / 6 680 | ∞ | ∞ |
| 0,20 | 0,2 | ∞ | ∞ | ∞ | ∞ | ∞ |
| 0,25 | 1,0 | 191 / 191 | ∞ | 791 / 791 | ∞ | 8 111 / 8 111 |
| 0,25 | 0,7 | 549 / 424 | ∞ | 2 927 / 2 276 | ∞ | q.c. |
| 0,25 | 0,4 | 14 676 / 8 067 | ∞ | ∞ | ∞ | ∞ |
| 0,25 | 0,2 | ∞ | ∞ | ∞ | ∞ | ∞ |
| 0,30 | 1,0 | 322 / 322 | ∞ | 2 301 / 2 301 | ∞ | ∞ |
| 0,30 | 0,7 | 1 270 / 1 001 | ∞ | 38 537 / 30 465* | ∞ | ∞ |
| 0,30 | ≤0,4 | ∞ | ∞ | ∞ | ∞ | ∞ |

### ε = 10⁻¹²

| β | d | Δ/τ ≤ 0,5 | Δ/τ=1 prouv. | Δ/τ=1 est. | Δ/τ=2 prouv. | Δ/τ=2 est. |
|---:|---:|---:|---:|---:|---:|---:|
| 0,10 | 1,0 | 69 / 69 | ∞ | 150 / 150 | ∞ | 308 / 308 |
| 0,10 | 0,7 | 135 / 95 | 11 010 / 8 131 | 253 / 185 | ∞ | 478 / 354 |
| 0,10 | 0,4 | 427 / 189 | 3 970 / 1 872 | 720 / 332 | ∞ | 1 284 / 601 |
| 0,10 | 0,2 | 3 328 / 922 | 28 371 / 8 004* | 6 363 / 1 786 | ∞ | 14 706 / 4 145 |
| 0,20 | 1,0 | 162 / 162 | ∞ | 496 / 496 | ∞ | 1 940 / 1 940 |
| 0,20 | 0,7 | 389 / 292 | ∞ | 1 181 / 902 | ∞ | 5 740 / 4 385 |
| 0,20 | 0,4 | 2 840 / 1 471 | ∞ | 17 151 / 8 945 | ∞ | ∞ |
| 0,20 | 0,2 | ∞ | ∞ | ∞ | ∞ | ∞ |
| 0,25 | 1,0 | 257 / 257 | ∞ | 1 061 / 1 061 | ∞ | 10 850 / 10 850 |
| 0,25 | 0,7 | 739 / 570 | ∞ | 3 922 / 3 050 | ∞ | q.c. |
| 0,25 | 0,4 | **19 662 / 10 808** | ∞ | ∞ | ∞ | ∞ |
| 0,25 | 0,2 | ∞ | ∞ | ∞ | ∞ | ∞ |
| 0,30 | 1,0 | 434 / 434 | ∞ | 3 083 / 3 083 | ∞ | ∞ |
| 0,30 | 0,7 | 1 705 / 1 344 | ∞ | 51 533 / 40 738* | ∞ | ∞ |
| 0,30 | ≤0,4 | ∞ | ∞ | ∞ | ∞ | ∞ |

### 3.1 Commentaire sur 7 200 créneaux / 2 880 blocs

- **Profondeur réellement disponible.** Le registre R_e n'est installé qu'au porteur de maturité (§5.2), soit au plus tôt `snapshot_cut + K_reg + seed_guard` = **14 400 créneaux**, plus la maturité Bitcoin (k_seed = 30, en pratique ≈ +3 000 à 3 600). Les 7 200 créneaux ne sont donc pas la marge effective : ce qui protège, c'est K_reg **plus** la garde de 12 h. Le mandat interdit de partir de ces valeurs ; je me contente de les situer.
- **D = 0, d ≥ 0,7** : K(10⁻¹²) ≤ 1 705 créneaux / 1 344 blocs jusqu'à β = 0,30. 7 200 / 2 880 sont **tenables avec une marge de 4 à 100×**.
- **D = 0, d = 0,4** : tenables pour β ≤ 0,20 (2 840 / 1 471). **Trop courts à β = 0,25** : ε(7 200 créneaux) = 3,2·10⁻⁵, ε(2 880 blocs) = 4,8·10⁻⁴, ε(14 400 créneaux) = 1,5·10⁻⁹. Même la profondeur réelle de 14 400 manque la cible 10⁻¹².
- **d = 0,2** : impossible pour β ≥ 0,20 (h < β : l'attaque privée gagne presque sûrement). À β = 0,10, 3 328 / 922 suffisent, mais la règle A est au bord du seuil (§4).
- **Δ/τ ≥ 1** : rien n'est prouvable pour β ≥ 0,17. En estimation, 7 200 suffit pour β ≤ 0,20 avec d ≥ 0,7 (D ≤ 2) ; β = 0,20 avec d = 0,4 et D = 1 demande 17 151 créneaux, au-delà de 14 400.
- **2 880 comme `maxreorg`** : une réorganisation légitime dépassant K_blocs déclenche `HALTED_DEEP_REORG`. C'est une perte de vivacité, pas de sûreté, cohérente dès que K_blocs(ε) ≤ 2 880.

## 4. Limite structurelle : le compte de la règle A (hors K)

A_e dépend du compte de blocs de la branche dans [cut, seed_maturity], soit W ≥ 14 400 créneaux. Deux branches qui ne diffèrent que par leur suffixe récent, près du porteur de maturité (donc **non stabilisé** au moment des premiers engagements), obtiennent le même A_e seulement si leurs deux comptes tombent du même côté de 2 880. Sans l'adversaire, les honnêtes seuls fournissent au moins g·W blocs ; l'adversaire peut en ajouter jusqu'à β·W, ou s'abstenir.

| régime | condition | effet |
|---|---|---|
| sûr (avance toujours) | g·W_min − 6σ > 2 880 | A_e = support brut sur toute branche |
| sûr (hérite toujours) | (g+β)·W < 2 880 | registre figé, mais commun |
| **pilotable par l'adversaire** | g·W < 2 880 ≤ (g+β)·W | il place une branche au-dessus et une au-dessous : **CP_reg échoue, quel que soit K** |

Avec W_min = 14 400, le seuil est g > 0,20. La colonne « blocs honnêtes / 14 400 » du §2.3 montre que **toutes les lignes d = 0,2 sont pilotables** (par exemple 2 304 < 2 880 ≤ 5 184 à β = 0,2). La latence Bitcoin (W ≈ 17 800) ne sauve que β = 0,10 et de justesse (3 204, marge ≈ 6σ). C'est la généralisation probabiliste du contre-exemple TLA de fermeture (⟨0,11,13⟩ / ⟨0,23⟩, comptes 2 et 1) : aucun recul temporel ne l'empêche.

## 5. Confrontation Monte-Carlo (`cp_sim.py`)

Adversaire simulé : retient tout, choisit le point de fourche optimal parmi tous les blocs honnêtes antérieurs et l'instant de révélation (omniscience = arrêt optimal), retarde chaque bloc honnête de D créneaux, gagne les égalités (`omni_tie`). On compare avec la variante `omni_strict` et avec la course sans avance `naive_tie`, analogue au §15. La simulation compte 110 essais × 300 000 créneaux par configuration, soit 24,2 M cibles ; elle a pris 101 s murales et 16,6 min CPU sur 14 cœurs.

K en créneaux (mesuré jusqu'à 10⁻⁶, puis extrapolé par pente log-linéaire) :

| β | D | d | Borne marge ε=10⁻⁶ / 10⁻⁹ | Attaque privée **exacte** 10⁻⁶ / 10⁻⁹ | Simulation `omni_tie` 10⁻⁶ / 10⁻⁹ |
|---:|---:|---:|---:|---:|---:|
| 0,10 | 0 | 1,0 | 33 / 51 | 25 / 37 | 22 / 35 |
| 0,10 | 0 | 0,4 | 206 / 317 | 148 / 228 | 156 / 242 |
| 0,20 | 0 | 1,0 | 78 / 120 | 56 / 86 | 53 / 83 |
| 0,20 | 0 | 0,7 | 189 / 289 | 131 / 202 | 137 / 213 |
| 0,20 | 0 | 0,4 | 1 391 / 2 115 | 885 / 1 360 | 825 / 1 233 |
| 0,25 | 0 | 1,0 | 124 / 191 | 87 / 133 | 89 / 133 |
| 0,25 | 0 | 0,4 | 9 696 / 14 676 | 5 508 / 8 454 | 5 484 / 8 406 |
| 0,10 | 1 | 1,0 | est. 73 / 112 | — | 46 / 68 |
| 0,10 | 1 | 0,4 | est. 350 / 535 (prouv. 1 963 / 2 966) | — | 212 / 314 |
| 0,20 | 1 | 1,0 | est. 243 / 369 | — | 149 / 225 |
| **0,20** | **1** | **0,7** | **est. 579 / 880** | — | **379 / 596** |
| 0,20 | 1 | 0,4 | est. 8 467 / 12 809 | — | 3 909 / 5 597 |
| 0,25 | 1 | 1,0 | est. 521 / 791 | — | 333 / 528 |
| 0,25 | 1 | 0,4 | ∞ | — | **non sûr** (rattrapage dans 100 % des essais) |

Lecture :

1. **La simulation reproduit l'attaque privée exacte** (formule de §2.1 avec ρ₀ géométrique) à 1–10 % près, et l'extrapolation simulée est légèrement optimiste (−10 % à β = 0,2, d = 0,4). Les deux codes, indépendants, se valident mutuellement.
2. **Borne marge contre attaque privée, facteur K × 1,3 à 1,75 (D = 0) : écart expliqué.** La borne couvre aussi l'équilibre à deux branches sous départage adverse, que l'adversaire simulé n'essaie pas. Le départage lexicographique public de N rend cet équilibre difficile à D = 0 (tous les honnêtes préfèrent la même branche à score égal ; seule une équivoque produit un vrai ex æquo). **Je publie la borne, pas l'attaque** : la vraie valeur de N est entre les deux.
3. **`omni` contre `naive`** : le point de départ et l'avance optimaux ne multiplient ε que par ≈ 1,3 à 2. Pour une coupure fixée, la rétention coûte peu ; ce sont la densité, la marge et le gonflement du compte qui coûtent.
4. **Blocs** : la victime ne voit que des blocs honnêtes quand l'adversaire retient tout (`resultats.md`, colonne « blocs ») ; K y est 2 à 2,5 fois plus petit qu'en créneaux non vides. Un adversaire qui équivoque gonfle ce compte gratuitement, d'où l'unité « non vides » (colonne `nonempty`) du §3.
5. **Écart résiduel non expliqué (D = 1)** : le rapport estimation/simulation vaut ≈ 1,5 à 2,3, contre 1,3 à 1,75 à D = 0 pour un θ comparable. Une partie vient du biais d'extrapolation (≈ 10 %), le reste (≈ ×1,3) n'est pas expliqué. Deux hypothèses : soit l'estimation traite trop durement la vue la plus lente, soit la simulation n'implémente pas la récolte des blocs non gloutons (§2.2) — auquel cas la simulation sous-estime l'attaque. **À trancher avant d'utiliser une estimation D ≥ 1** ; cela ne change pas le verdict « aucune borne prouvable ».

## 6. Domaine de validité H_N (d) — texte normatif candidat

« Si H_N-1 à H_N-9 sont satisfaites sur tout l'horizon qualifié, alors Pr[∃ e : ¬CP_reg(e,X)] ≤ E·Q_B·ε(K) + ε_A, avec ε(K) donné par la table D = 0 et ε_A ≈ 10⁻⁹ (écart du compte de règle A au-delà de 6σ). Si l'une d'elles est violée, N ne revendique aucune sûreté de registre : STOP (§9.5) ou RECOVERY explicite. »

| # | Hypothèse | Forme mesurable |
|---|---|---|
| **H_N-1** Origine, stabilisation | contexte X commun ; seules les coupures postérieures à T_GST + T_rec sont couvertes | T_rec ≥ β·T_async/(τ(g−β)) + K ; un préfixe construit avant stabilisation n'a **aucune** garantie |
| **H_N-2** Livraison honnête | tout bloc honnête est reçu par tout honnête avant la réservation du créneau suivant, **sur toutes les fenêtres de l'histoire concernée** (pas seulement après réunion : ancres TLA) | Δ + 2σ_horloge ≤ τ − 1 s = **5 s** (⇒ D = 0) ; au-delà, aucune borne prouvable pour β ≥ 0,17 |
| **H_N-3** Poids adverse | part adverse du **poids total** du tirage (inactif compris au dénominateur), adversaire supposé toujours en ligne, borne sup sur l'horizon (admissions et exclusions §15.6 comprises), corruptions passées incluses | β ≤ β_max publié |
| **H_N-4** Densité honnête sous attaque | fraction minimale des créneaux honnêtes effectivement produits, **DoS ciblé permis par le calendrier public compris**, sur **toute** fenêtre de K créneaux | d ≥ d_min avec (1−β)d_min > β et K pris dans la table (β, d_min) |
| **H_N-5** Robustesse de la règle A | le compte ne peut pas être piloté | g·W_min − 6√(W_min·g(1−g)) > `registry_min_blocks`, soit g ≳ 0,22 pour 2 880 / 14 400 |
| **H_N-6** Grinding | nombre de graines ou registres sélectionnables par époque ≤ Q_B | union explicite E·Q_B ; à défaut, hors domaine |
| **H_N-7** Bitcoin | S_e et sa maturité communs ; aucune réorganisation Bitcoin retirant une graine consommée | sinon `HALTED_BTC` |
| **H_N-8** Tirage | loterie uniforme i.i.d. conditionnellement à la graine (§7.1), clés non compromises hors β | — |
| **H_N-9** Unité de confirmation | toute règle en « blocs » compte des **créneaux non vides** de la branche ; aucune inférence de sûreté par densité observée (§15.7) | K_blocs de la table |

**Hors domaine, donc STOP ou RECOVERY** : partitions ou retards > 5 s prolongés ; β > β_max (y compris par exclusions d'honnêtes) ; densité sous d_min ; compte de règle A dans la zone pilotable ; grinding au-delà de Q_B ; réorganisation Bitcoin profonde ; corruption a posteriori / longue portée (relève de H1 et des checkpoints) ; tout préfixe antérieur à la stabilisation.

## 7. Limites à publier telles quelles (e)

1. **À d = 0,2, N n'a pas de préfixe commun pour β ≥ 0,20**, quel que soit K. C'est une propriété du tirage sans remplaçant, pas de la méthode.
2. **À β = 0,25 et d = 0,4, il faut K ≈ 19 700 créneaux / 10 800 blocs pour 10⁻¹²**, au-delà des 14 400 créneaux effectivement disponibles et de 2 880 blocs.
3. **Sans Δ ≤ 5 s, aucune borne prouvable au-delà de β = 17 %.** Les estimations existent mais ne qualifient rien, et l'écart résiduel du §5.5 est ouvert.
4. **La règle A est pilotable par l'adversaire à densité ≈ 0,2** : CP_reg échoue sans réorganisation profonde.
5. **La densité observée ne prouve rien** : l'adversaire gonfle les comptes par équivoque et le calendrier public lui permet d'abaisser d ponctuellement.

Aucune rustine n'est proposée.

## 8. Questions au propriétaire (pas des règles)

- Accepter H_N-2 (Δ ≤ 5 s) comme hypothèse publiée ? Sinon, soit τ doit croître (D = 0 exige τ ≥ Δ + 1 s + 2σ), soit N reste sans borne prouvable au-delà de β ≈ 0,17. C'est un **paramètre**, pas une mécanique.
- Quel couple (β_max, d_min) publier ? La table montre que (0,20 ; 0,7) est confortable, (0,20 ; 0,4) acceptable et (0,25 ; 0,4) hors de portée des paramètres actuels.
- La zone pilotable de la règle A (§4) : l'accepter comme limite hors domaine (H_N-5 ⇒ STOP), ou la traiter comme défaut de conception à examiner **après** CP_reg.
- Confrontation avec l'analyse codex : si ses K diffèrent de la colonne D = 0 de plus de ≈ 10 %, un des deux calculs a un défaut. La DP est exacte et recoupée par deux Monte-Carlo, mais son modèle (β sur le poids total, départage adverse, blocs = non vides) doit être comparé terme à terme.
