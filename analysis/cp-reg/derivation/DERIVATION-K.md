# Chaîne de dérivation de K — tables conditionnelles en attente du banc réseau

1ᵉʳ octobre 2026. Autorité : `DIRECTION.md`, lignes « Lemme L1 / CP_reg — décisions (01/10) » et « Mandat orchestrateur — dernier chantier avant gel (01/10) ». **Aucun paramètre de consensus n'est fixé ici.** Ce document fournit une machine de calcul (`derive_k.py`) et des tables conditionnelles. Rien dans N-SPEC, `sim/` ou `sim-opus/` n'a été modifié, et aucune opération git n'a été faite.

## 0. En une page

1. **Entrée attendue du banc : p_late(τ)**, la probabilité qu'un bloc honnête (dépendances comprises) ne soit pas reçu *et validé* par tous les honnêtes avant `start(s+1) + 1 000 ms`. Un créneau honnête en retard est compté **adverse**. Le couple (β, h) devient donc (a, h') = (β + h·p, h·(1−p)), et la condition d'existence de K s'écrit **(1−β)·d·(1−2p_late) > β**.
2. **Cette condition est nécessaire, pas suffisante.** Pour que K(ε) ≤ 13 200 créneaux, il faut d ≥ d_min(β, ε). À ε = 10⁻¹² et p = 0, d_min vaut 0,154 / 0,232 / 0,318 / 0,415 / 0,524 pour β = 0,10 / 0,15 / 0,20 / 0,25 / 0,30, soit θ = a/h' ≤ 0,72 à 0,82 (§4).
3. **Profil A** (β ≤ 0,20 ; d ≥ 0,40) et **profil B** (β ≤ 0,30 ; d ≥ 0,70) ont tous deux un K fini et raisonnable par coupure. p_late ≤ 10⁻³ ne déplace K que de 1 à 3 %.
4. **La contrainte qui dimensionne K_reg n'est pas ε_fix mais le pivot profond** : K_inst ≳ (b + marge)/h' + K_fix(ε/n). K_reg et `registry_min_blocks` sont donc couplés. Avec 7 200 / 2 880 créneaux/blocs, le profil A n'est certifié pour ε_H = 10⁻⁶ sur 10 ans qu'à **τ = 6 s et Q_B = 1** ; il échoue dès τ = 8 s ou Q_B = 256. Le profil B passe partout (§5).
5. **Écarts entre méthodes** : tous sont expliqués, sauf un, qui est structurel (la vraie valeur de N se situe entre l'attaque privée et la borne DP, et aucun des deux calculs ne tranche). Le chiffre de pivot profond d'Opus (L1 §5) était optimiste (§6).

## 1. Ordre de dérivation et entrées

τ → (β_max, d_min) → K(ε) → K_reg → registry_min_blocks → métriques. Le banc (`etudes/n-spec/banc-reseau/PLAN-BANC.md`) mesure, pour chaque τ candidat, la fraction de créneaux qui violent

```text
Δ_net + Δ_val + skew ≤ τ − 1 000 ms      (régime D = 0, §7.2)
```

Cette fraction est p_late(τ). **La valeur publiée doit être une borne supérieure sur toute fenêtre de K créneaux, et non une moyenne.** Le calcul suppose aussi les retards indépendants entre créneaux et non choisis par l'adversaire (hypothèse H_late, §7). Un retard ciblé est une attaque ; il se compte dans β, ou alors on sort du domaine.

Le script s'exécute en une commande, graine 20261001, 4 processus au plus, en `nice` :

```sh
cd etudes/n-spec/cp-reg && nice -n 10 python3 derivation/derive_k.py --procs 4
```

Sorties dans `derivation/results/` : `K-table.csv` (450 lignes), `d-min.csv`, `composition.csv`, `mc.json`, `codex-envelope.csv`, les courbes DP (`dp_curves.npz`, `theta_curves.npz`), `run-log.json` et `TABLES.md`, qui contient toutes les tables. Dès que le banc donne p_late(τ), on lit la ligne correspondante, ou on ajoute la valeur à `PLATES` et on relance (≈ 3 min murales).

## 2. Modèle, réduction p_late et adversaire

**Loterie** (§7.1) : un producteur par créneau, sans remplaçant. On a A avec probabilité β (poids total), H avec probabilité h = (1−β)d (honnête en ligne ; d comprend le DoS ciblé), et un créneau vide sinon.

**Réduction p_late (analytique, sous H_late).** Un créneau honnête en retard devient un symbole A. C'est la réduction « non isolé ⇒ adverse » de Praos, restreinte aux seuls créneaux en retard. Chaque bloc honnête à l'heure a été vu par tous avant la réservation suivante, donc sa profondeur dépasse celle de tous les blocs honnêtes à l'heure qui le précèdent. C'est exactement l'hypothèse du modèle synchrone de Blum–Kiayias–Moore–Quader–Russell. Le bloc en retard, traité comme adverse, peut être placé sur n'importe quelle branche, ce qui donne à l'adversaire strictement plus de pouvoir qu'il n'en a réellement. **Nous n'avons pas trouvé mieux qui soit prouvable.** Traiter un retard de ≤ 2 créneaux comme un D = 1 local ramènerait au régime D ≥ 1, pour lequel aucune borne prouvable n'existe au-delà de β ≈ 0,17 (CONFRONTATION-CP-REG).

**Adversaire du mandat, couvert par la DP d'Opus.** Calendrier public : omniscience sur la chaîne caractéristique. Choix du moment et rétention : avance initiale égale au *reach* stationnaire, P[ρ ≥ r] = θʳ avec θ = a/h', et marge maximisée sur tout t ≥ c + K. Révélation optimale et abstention : maxima sur toutes les fourches. Départage : défavorable aux honnêtes. β est compté sur le poids total.

**Règle d'équivoque (« un créneau équivoqué = une unité de progrès »), vérifiée dans les trois codes :**

| Code | Traitement | Conforme |
|---|---|---|
| `sim-opus/cp_bound.py` (DP) | un symbole A fait +1 sur ρ et +1 sur μ : une unité par branche, utilisable sur plusieurs branches | oui |
| `sim-opus/cp_sim.py` (MC) | branche privée = L(f) + #A(f, t], donc +1 par créneau adverse | oui |
| `sim/model.py` (`strategic_race`, PGF) | « une variante au même créneau a le même tie et n'ajoute AUCUN score » ; au plus un bloc par créneau et par branche | oui |

**Aucune correction n'a été nécessaire.** Nous retenons la lecture conservatrice : une unité *par branche*, et le même créneau peut servir aux deux branches. La lecture « une unité au total » serait optimiste. Conséquence pour la vue victime : **K en blocs = nombre de créneaux non vides**. Si ma chaîne porte k blocs après B, alors k créneaux non vides au moins se sont écoulés, équivoque comprise. Une règle « attendre k blocs sur ma chaîne » hérite donc de la borne en créneaux non vides. Compter les seuls blocs honnêtes visibles, comme la colonne « blocks » de `cp_sim`, ne serait pas sûr.

## 3. Table K(ε) — profils A et B

La table donne la borne DP exacte, en K créneaux / K blocs (créneaux non vides). Entre crochets figure l'attaque privée exacte à dépassement strict, en créneaux : c'est une borne *inférieure* réalisable. Chaque profil est donné à son coin le plus défavorable, car K croît avec β et décroît avec d sur toute la grille.

| Profil (coin) | p_late | ε = 10⁻⁶ | ε = 10⁻⁹ | ε = 10⁻¹² |
|---|---:|---|---|---|
| **A** (β 0,20 ; d 0,40) | 0 | 1 391 / 720 [869] | 2 115 / 1 095 [1 344] | **2 840 / 1 471** [1 823] |
| **A** | 10⁻³ | 1 407 / 729 [879] | 2 140 / 1 108 [1 359] | **2 874 / 1 488** [1 843] |
| **B** (β 0,30 ; d 0,70) | 0 | 835 / 658 [523] | 1 270 / 1 001 [809] | **1 705 / 1 344** [1 098] |
| **B** | 10⁻³ | 844 / 665 [529] | 1 284 / 1 013 [818] | **1 724 / 1 360** [1 109] |

À p = 0, les valeurs sont identiques à celles d'Opus (`CP-REG-opus.md` §3, régression exacte). La grille complète (5 β × 6 d × 5 p_late) se trouve dans `results/TABLES.md`.

**Sensibilité à p_late** : p ≤ 10⁻⁴ déplace K de moins de 0,5 %, p = 10⁻³ de +1 à +3 %, et p = 10⁻² de +7 à +14 % (A : 2 840 → 3 197 ; B : 1 705 → 1 913 à 10⁻¹²). **Le banc a donc peu d'influence sur K par sa valeur, et beaucoup par l'hypothèse qu'il valide** : la réduction n'a de sens que si p_late est petit, borné et non adaptatif. Au-delà de quelques 10⁻², c'est la condition d'existence elle-même qui recule.

**K en créneaux ne dépend pas de τ** (D = 0) ; seule la valeur de p_late(τ) en dépend. En durée, profil A à 10⁻¹² : 2 840 × τ = 4,7 h à 6 s et 9,5 h à 12 s.

## 4. Condition de domaine explicite et cases hors domaine

**Condition nécessaire (H_N, analytique)** : h' > a ⇔ **(1−β)·d·(1−2p_late) > β**. Si elle est violée, l'attaque privée gagne presque sûrement et aucun K n'existe.

**Condition renforcée (analytique + interpolation).** K en blocs ne dépend que de θ = a/h'. Une DP exacte sur une grille de θ ∈ [0,40 ; 0,92], jointe à K_slots ≈ K_blocs/(a+h') (écart ≤ 2 % sur la grille), donne le d minimal pour K(ε) ≤ 13 200 :

| β | d_cond (p = 0) | d_min, ε = 10⁻⁶ | 10⁻⁹ | 10⁻¹² | θ_max à 10⁻¹² |
|---:|---:|---:|---:|---:|---:|
| 0,10 | 0,111 | 0,141 | 0,148 | 0,154 | 0,72 |
| 0,15 | 0,176 | 0,216 | 0,225 | 0,232 | 0,76 |
| 0,20 | 0,250 | 0,298 | 0,309 | 0,318 | 0,79 |
| 0,25 | 0,333 | 0,391 | 0,404 | 0,415 | 0,80 |
| 0,30 | 0,429 | 0,496 | 0,511 | 0,524 | 0,82 |

p_late = 10⁻³ ajoute au plus +0,001 à d_min, et 10⁻² environ +0,01. Forme lisible : **h' − a ≥ 0,04 à 0,07**. La marge de dérive doit être *finie*, pas seulement positive. La composition (§5) ajoute un coût b/h', ce qui rend en pratique la condition plus forte encore.

**Cases hors domaine de sûreté N** (grille du mandat, toutes valeurs de p_late sauf mention contraire) :

| (β ; d) | Motif |
|---|---|
| (0,20 ; 0,2), (0,25 ; 0,2), (0,25 ; 0,3), (0,30 ; 0,2), (0,30 ; 0,3), (0,30 ; 0,4) | h' ≤ a : aucun K |
| (0,15 ; 0,2) | h' > a, mais l'attaque privée *réalisable* exige déjà ≥ 19 994 créneaux à 10⁻⁶ |
| (0,20 ; 0,3), (0,25 ; 0,4), (0,30 ; 0,5) | K > 13 200 à 10⁻⁹ et 10⁻¹² ; à 10⁻⁶ ils passent de justesse (12 122 ; 9 696 ; 11 705), et (0,20 ; 0,3) et (0,30 ; 0,5) sortent aussi à 10⁻⁶ si p_late = 10⁻² (15 911 ; 16 128) |

Aucune rustine n'est proposée. Les profils A et B sont intégralement dans le domaine.

## 5. Composition par époque, horizon, K_reg et registry_min_blocks

**Formule (D1 : ε_post exclu, nœuds nouveaux ou de retour hors domaine).** Pour chaque époque e :

```text
ε_ep ≤ T_fix + T_court + T_profond + T_CG
T_fix     = ε_fix(K_inst)                                   voie (i), coupure fixe snapshot_cut
T_profond = Σ_{j<K_inst} min( P[Bin(j,h') < b+r], ε_fix(K_inst−j) )      pivot profond
T_court   = θ^r + P[Bin(K_inst,h') < b+r]                   pivot peu profond (robustesse du compte A)
T_CG      = θ^r + P[Bin(L+K_reg,h') < b+1+r]                maxreorg ⇒ HALT pour les synchronisés
K_inst    = K_reg + G(τ),   G(τ) = ⌈(seed_guard − marge MTP)/τ⌉ = ⌈36 000 s/τ⌉
ε_H       = E(τ) · Q_B · ε_ep,  E = ⌈10 ans / (L_epoch·τ)⌉
```

**Le pivot unifié** (esquisse, statut « sous hypothèse ») fonctionne ainsi. Une branche Y qui hérite, c'est-à-dire dont le compte est < b, a bifurqué en f = cut + j avec #H(cut, f] − ρ < b. Elle n'est installable qu'à cut + K_inst au plus tôt ; la fourche a donc un âge ≥ K_inst − j, ce qui est une violation CP de la coupure f+1. L'union porte sur j. Pour j ≥ K_inst, les événements sont emboîtés, et l'on retrouve la condition de robustesse g·W > b de `CP-REG-opus.md` §4, qui correspond au pivot peu profond de Codex. Les deux volets du pivot relèvent ainsi d'une seule somme.

**Budgets** : ε_ep/4 pour T_fix, ε_ep/2 pour les deux pivots, ε_ep/4 pour T_CG. On choisit ensuite b_min = K_blocs(ε_ep/4). Ce choix est **de vivacité** : l'adversaire ne force un HALT qu'avec une probabilité ≤ ε_ep/4. Tout b ∈ [b_min ; b_max(K_reg)] est admissible.

**Dérivation conditionnelle, ε_H = 10⁻⁶ sur 10 ans, p_late = 0.** Chaque cellule se lit « b_min / K_reg min en créneaux (en heures) ». Le contrôle a posteriori du couple actuel (7 200 / 2 880), fait *après* la dérivation, donne b_max à K_reg = 7 200 et le verdict.

| Coin | Q_B | τ = 6 s | 8 s | 10 s | 12 s |
|---|---:|---|---|---|---|
| A | 1 | 1 241 / 1 574 (2,6 h) — b_max 2 931 **PASS** | 1 225 / 2 985 (6,6 h) — 2 488 FAIL | 1 213 / 3 815 (10,6 h) — FAIL | 1 203 / 4 359 (14,5 h) — FAIL |
| A | 256 | 1 542 / 3 295 (5,5 h) — 2 710 **FAIL** | 1 527 / 4 707 (10,5 h) — FAIL | 1 515 / 5 539 (15,4 h) — FAIL | 1 505 / 6 083 (20,3 h) — FAIL |
| B | 1 | 1 134 / 1* | 1 120 / 1* | 1 109 / 768 (2,1 h) | 1 100 / 1 334 (4,4 h) — tous PASS |
| B | 256 | 1 410 / 1* | 1 396 / 933 (2,1 h) | 1 385 / 1 791 (5,0 h) | 1 376 / 2 358 (7,9 h) — tous PASS |

\* K_reg = 1 signifie que CP_reg seul n'impose rien : la garde Bitcoin (G = 6 000 ou 4 500 créneaux) couvre déjà K_inst. La valeur de K_reg relève alors d'autres rôles (§5.8 anti-grinding), qui sont une décision et non une dérivation.

À p_late = 10⁻³, le profil A demande 1 667 à 6 205 et le profil B 1 à 2 418 (+2 à +5 %). À ε_H = 10⁻⁹ et Q_B = 256, A demande 5 441 / 6 850 / 7 682 / 8 225 et B 758 / 2 206 / 3 064 / 3 631 (`TABLES.md`). Toutes les requêtes sous 10⁻¹⁴ utilisent le prolongement log-linéaire de la courbe DP (extrapolation).

**Lecture.**
1. **K_reg dépend de τ alors que K n'en dépend pas.** La garde de 12 h et la marge MTP de 2 h sont exprimées en secondes. G tombe donc de 6 000 à 3 000 créneaux entre 6 s et 12 s, et K_reg doit compenser. Si l'on garde 7 200 créneaux, **passer de 6 à 8 s fait échouer le profil A**.
2. **b et K_reg ne se choisissent pas séparément.** Augmenter b de Δb coûte environ Δb/h' créneaux de K_reg : 3,1 créneaux par bloc en A, 2,0 en B. 2 880 est au-dessus de b_max dans le profil A dès que τ ≥ 8 s ou Q_B = 256.
3. **Contraintes N-SPEC qui dépendent de τ**, signalées sans être modifiées :
   - §5.2 « le cliché précède l'époque de 36 h au moins », qui vaut (K_reg + L)·τ ;
   - §5.4/§8.4 : G(τ) = 36 000/τ ;
   - §5.8 : séparation nominale K_reg·τ + 43 200 s = 86 400 s et marge 79 199 s, toutes deux vraies seulement à τ = 6 s avec K_reg = 7 200 (voir `sep_5_8_s` dans `composition.csv`) ;
   - §3.1 : (signature_close − open) + Delta_nom + 2·δ_clock < τ, et la condition D = 0 elle-même ;
   - L_epoch = 14 400 créneaux, soit une époque de 24 h·τ/6 et donc E(τ) ;
   - les fenêtres comptées en époques (activité, exclusions, evidence_horizon), dont la durée réelle change ;
   - `fee_maturity_links` et `reference_protection_links` ≥ maxreorg = b (§3.1), qui suivent b.

## 6. Confrontation des méthodes

| Comparaison | Écart | Statut |
|---|---|---|
| DP (Opus) contre attaque privée exacte | K_DP/K_priv = 1,32 à 1,83 sur toute la grille, y compris à p = 10⁻³ | **Expliqué** : la DP borne toute fourche (équilibre à deux branches, départage adverse) ; l'attaque privée n'en est qu'une |
| MC Codex (`strategic_race`, ε par coupure, 2,38 M coupures par case, 40 cases) contre attaque privée exacte | MC/strict ∈ [0,52 ; 1,75], MC/tie ∈ [0,19 ; 1,37] ; sur les 278 points à ≥ 30 épisodes indépendants, **aucun dépassement significatif du cas tie** (z max = +1,6) ; MC/DP ≤ 0,61 partout | **Expliqué** : le départage public de Codex est favorable à l'adversaire une fois sur deux environ, donc le MC tombe entre strict et tie. Les ratios < 0,5 à haute densité sont un effet de petit K (départ exigeant au moins un bloc honnête déconnecté) |
| MC Codex contre DP | facteur 1,3 à 1,8 en K | **Structurel, non résolu** : aucun code n'exécute l'équilibre à deux branches sous le départage de N (§9.3–9.4 : variantes équivoques ex æquo ⇒ stabilité *suspendue*). La vraie valeur de N se situe entre l'attaque et la DP. **On publie la DP** |
| Enveloppe Codex (`derive`) contre DP | profil A à 10⁻¹² : barrière 17 272 contre K_DP 2 840 (6×) ; W = 62 964 contre K_inst composé 7 400 à 9 300 ; en B : W = 35 857 contre 4 300 à 5 500 | **Expliqué** : ce sont des événements différents. L'absence de barrière catalane contient la marge ≥ 0, et le taux PGF vaut ≈ 0,0048 par créneau actif (singularité imbriquée) contre 0,0184 pour la DP. S'y ajoutent l'union sur M ≈ 77 000 départs et trois fenêtres. Les deux bornes sont valides ; celle de Codex est lâche. Régression exacte sur les chiffres publiés par Codex (β 0,20, d 0,40, 10⁻⁹ : W = 52 225, b = 6 960) |
| Pivot profond, Opus L1 §5, contre T_profond | Opus : K_piv = 13 200 − 2 880/h = 4 200, ε_fix ≈ 2·10⁻¹⁸, « passe de justesse ». Ici, avec 7 200/2 880 à τ = 6 s : T_profond = 3,4·10⁻¹¹ par époque (Q_B = 1) | **Expliqué, et Opus était optimiste.** Opus utilisait le compte *moyen* b/h, sans queue de fluctuation (≈ 7σ, soit +1 000 créneaux), sans avance ρ (+190) et sans union sur les positions de fourche (+≈ 970). K_piv effectif ≈ 2 900 ≈ K_fix(10⁻¹²). Conséquence : A avec 7 200/2 880 est **non certifié** à Q_B = 256 (ε_H = 4·10⁻⁵). « Non certifié » ne veut pas dire « attaquable » : c'est une borne par union, pas une attaque |
| Réduction p_late dans le MC | late → A appliquée dans les labels | Le MC **ne teste pas** la réduction ; il vérifie seulement la cohérence numérique. La réduction est analytique |

## 7. Statuts

| Élément | Statut |
|---|---|
| Réduction p_late → A | analytique, sous H_late (retards i.i.d., non adaptatifs, borne sur toute fenêtre K) |
| K(ε) DP, créneaux et blocs | analytique exact, troncatures conservatrices ; au-delà de 10⁻¹⁴ (plancher float64 ≈ 10⁻¹⁶) : **extrapolation** |
| Attaque privée exacte | analytique exact (borne inférieure réalisable du modèle) |
| MC Codex par coupure | Monte-Carlo, 40 cases × 14 calendriers × 200 000 créneaux |
| d_min, θ_max | analytique + interpolation (≤ 2 %) |
| Composition, pivot unifié | analytique sous hypothèses (unions, compte ≥ #H − ρ) ; esquisse à relire |
| Pivot profond en TLA+ | **NT** ici (un run TLC `MC_explore_sync_PivotDeep` tournait sur la machine ; résultat non consulté) |
| p_late(τ), Δ, skew | **NT**, en attente du banc |
| Q_B = 256 | hypothèse non qualifiée (Codex §4.6) ; Q_B = 1 publié en parallèle |
| ε_post | exclu par D1 |

## 8. Métriques SP/LP que Core peut exposer (sans rien imposer)

Catégories de l'API §16.1 : O = objectif, L = observation locale, M = résultat de modèle.

1. **Profondeur de sûreté (M)** : pour un bloc B, `k_slots` (créneaux écoulés) et `k_blocks` (blocs de la chaîne locale après B), confrontés à la table publiée du domaine. On en tire le niveau atteint, parmi 10⁻⁶, 10⁻⁹ et 10⁻¹², avec « ou » entre les deux unités. Une seule unité suffit dans le modèle, et `k_blocks` compte des créneaux non vides.
2. **Paramètres du domaine (O)** : β_max, d_min, p_late_max, τ, K_reg, b, horizon E, époque courante, table ε ↔ K.
3. **p_late observé (L)** : fraction des blocs validés après `start(s+1) + 1 000 ms`, sur des fenêtres de 100, 1 000 et K_slots créneaux ; p99,9 de latence ; incertitude d'horloge. Alarme au-delà de p_late_max.
4. **État du domaine (L/O)** : IN / DOUTE / OUT. Signaux : densité non vide observée sous (a+h')_min sur une fenêtre K, p_late au-dessus du seuil, `EQUIVOCATION_TIE_STALLED`, réorganisation observée plus profonde que K_blocs(10⁻⁶), réconciliation Bitcoin. **Le test est unilatéral** : une densité haute ne prouve pas l'appartenance au domaine (rétention, équivoque).
5. **Marge du compte A (O)** : `window_blocks(C,e)` comparé à b, en écarts-types de la production honnête attendue (zone de pivot).
6. **Consommation d'horizon (M)** : époques écoulées rapportées à E, et ε_H consommé.

## 9. Ce qui reste à faire, dans l'ordre

1. Banc : p_late(τ) comme borne par fenêtre, et vérification de H_late (corrélation des retards, coupures).
2. Propriétaire : choisir τ, puis (β_max, d_min) en respectant d ≥ d_min(β, ε) (§4), puis ε_H et Q_B.
3. Relire le pivot unifié (§5) ; témoin TLA+ du pivot profond (Codex).
4. Lire K_reg et b dans `composition.csv`, ou relancer avec la valeur mesurée.

Calcul machine : ≈ 1 400 s CPU au total, pilotes compris (campagne finale : 519 s CPU, 162 s murales), avec 4 processus au plus en `nice`, à côté du banc et d'un TLC. `TABLES.md` a été régénéré par `--render-only`, sans recalcul, après une retouche de mise en forme.
