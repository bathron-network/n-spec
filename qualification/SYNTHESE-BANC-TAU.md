# Synthèse — banc réseau, τ, domaine H_N et K (01/10, orchestrateur)

Autorité : DIRECTION.md, mandat orchestrateur du 01/10. Ordre suivi : **mesures → τ → (β_max, d_min) → K(ε) → K_reg → registry_min_blocks**.
Rien n'est figé ici ; les décisions demandées figurent au §6.

Sources :
- banc : `banc-reseau/` (PLAN-BANC, nbench v2, `RESULTATS-r1.md`, `RESULTATS-r2-dval{100,250}.md`, `plate.py`, `data/r{1,2}.tar.gz`, `valbench-vps2.json`) ;
- dérivation : `cp-reg/derivation/` (DERIVATION-K, `K-table.csv`, `composition.csv`) ;
- pivot profond : `cp-reg/PIVOT-PROFOND-TLA.md` ;
- lemme L1 : `cp-reg/CONFRONTATION-LEMME-L1.md`.

## 1. Ce qui a été mesuré (statuts)

| Mesure | Résultat | Statut |
|---|---|---|
| Propagation VPS↔VPS, réseau natif (r1 P0, mélange de tailles, 8 500 blocs par sens) | p50 8 à 11 ms, p99.9 ≈ 30 ms, max 148 ms | mesure directe, 1 saut européen |
| Nœud domestique (Mac) en montant | p50 ≈ 140 ms, p99.9 ≈ 900 ms, max 1,9 s | mesure directe |
| Horloges | VPS↔VPS \|θ\| p99 ≤ 5,5 ms en natif, ≤ 30 ms en W1, ≤ 83 ms en W2 ; Mac (macOS) 85 à 120 ms | mesure directe, estimateur NTP ±δmin/2 |
| Rattrapage après coupure (isolement de 10, 30 ou 60 s) | ≤ 5,2 s après la fin en natif ; ≤ 37 s en W1 | mesure directe |
| Validation Core, cryptographie (ML-DSA-44, vps2) | vérification p50 0,15 ms ; bloc maximal (109 signatures + hachages) ≈ **34 ms** | micro-banc ; accès à l'état **NT** (Δ_val = 100 ms retenu, sensibilité 250) |
| **r2 W1** : ~170 ms d'aller-retour, 0,5 % de perte, **blocs maximaux 256 Ko** espacés de τ | 1 saut : p50 1,3 à 1,7 s, p99 3,5 s, **max 4,7 s** (721 livraisons) | émulation netem sur liens réels |
| **r2 W2** : ~340 ms d'aller-retour, 2 % de perte | 1 saut : p50 4,4 à 4,8 s, p99 ≈ 10 s, **max 14,3 s** (714 livraisons) | émulation |
| r1 P1/P2 (charge de stress 0,5 s) | **saturation** (files de plusieurs secondes à plusieurs minutes) : constat de débit, pas de délai | artefact de charge écarté ; constat physique conservé |

Constat physique. Une connexion TCP unique avec pertes écoule environ 150 Ko/s (W1) ou environ 37 Ko/s (W2). Ajoutez le
redémarrage lent (slow start) après chaque pause de τ secondes : la transmission d'un bloc maximal complet domine Δ. **On n'a fait aucune
optimisation de propagation** (compact blocks, transactions pré-diffusées, QUIC, plusieurs pairs, codage d'effacement). Ces optimisations
sont une marge future d'implémentation, hors preuve et hors règles.

## 2. p_late(τ) — fraction de blocs honnêtes manquant la condition D = 0

Condition : `L_h + h·Δ_val ≤ τ − 1 s`, où h est le nombre de sauts de relais (stocker, valider, retransmettre) et L est mesuré en horloges
locales brutes, ce qui inclut le décalage d'horloge. Pour h ≥ 2, on somme des tirages indépendants sur un chemin unique, ce qui est
conservateur (pas de minimum entre chemins). Résolution statistique à 1 saut : environ 721 livraisons, donc **0 excès ⇒ borne 95 %
≈ 4·10⁻³**.

| Profil réseau | sauts | τ = 6 s | 8 s | 10 s | 12 s |
|---|---:|---:|---:|---:|---:|
| W1 | 1 | 0 (≤ 4·10⁻³) | 0 (≤ 4·10⁻³) | 0 (≤ 4·10⁻³) | 0 (≤ 4·10⁻³) |
| W1 | 2 | **1,0·10⁻¹** | 2·10⁻³ | **1·10⁻⁵** | ≈ 0 |
| W1 | 3 | 5·10⁻¹ | 1·10⁻¹ | 5·10⁻³ | 7·10⁻⁵ |
| W2 | 1 | 4,4·10⁻¹ | 1,2·10⁻¹ | 3,1·10⁻² | 4·10⁻³ (≤ 1,1·10⁻²) |
| W2 | 2 | 0,96 | 0,81 | 0,55 | 0,29 |

Lecture :
- **τ = 6 s n'est tenable qu'avec un seul saut en W1.** À deux sauts, 10 % des blocs honnêtes arrivent en retard.
- **τ = 10 s tient en W1 jusqu'à deux sauts** (≈ 10⁻⁵) ; à trois sauts, environ 5·10⁻³.
- **τ = 12 s** tient jusqu'à trois sauts.
- **W2, avec des blocs complets de 256 Ko relayés naïvement, est hors domaine pour tout τ ≤ 12 s dès deux sauts.** Ce n'est pas un défaut de
  N. C'est le couple (`max_body`, transport) qui le fixe, et on n'y touche pas ici.

## 3. K(ε) par cible, en créneaux puis en temps (DP exacte, pire coin du profil)

| Profil | p_late | ε = 10⁻⁶ | 10⁻⁹ | 10⁻¹² | 10⁻¹² à 6 s | **10⁻¹² à 10 s** | 10⁻¹² à 12 s |
|---|---|---:|---:|---:|---:|---:|---:|
| A (β ≤ 0,20 ; d ≥ 0,40) | 10⁻³ | 1 407 | 2 140 | 2 874 | 4,8 h | **8,0 h** | 9,6 h |
| A | 10⁻² | 1 566 | 2 382 | 3 197 | 5,3 h | **8,9 h** | 10,7 h |
| B (β ≤ 0,30 ; d ≥ 0,70) | 10⁻³ | 844 | 1 284 | 1 724 | 2,9 h | **4,8 h** | 5,7 h |
| B | 10⁻² | 937 | 1 425 | 1 913 | 3,2 h | **5,3 h** | 6,4 h |

- **Condition fondamentale.** Sous réseau imparfait, elle s'écrit **(1−β)·d·(1−2·p_late) > β**. Pour avoir un K raisonnable
  (≤ 13 200 créneaux), il faut une marge de 0,04 à 0,07, soit d_min(β) = 0,154 / 0,232 / 0,318 / 0,415 / 0,524 pour
  β = 0,10 / 0,15 / 0,20 / 0,25 / 0,30. **Ces seuils valent pour p_late = 0 et ε = 10⁻¹²** ; ils montent quand p_late augmente.
- **Hors domaine de sûreté N** : (β, d) = (0,20 ; 0,2), (0,25 ; ≤ 0,3), (0,30 ; ≤ 0,4), (0,15 ; 0,2), et à 10⁻⁹ (0,20 ; 0,3), (0,25 ; 0,4),
  (0,30 ; 0,5).
- **Profils A et B entièrement dans le domaine.**
- Un écart DP/MC d'un facteur 1,3 à 1,8 sur K reste ouvert ; on publie la DP, conservatrice.

## 4. K_reg et registry_min_blocks — dérivés, et non choisis (ε_H sur 10 ans, Q_B = 1)

Ils se dérivent ensemble, car le pivot profond domine : K_inst ≳ b/h' + K_fix, et la garde de 12 h vaut 4 320 créneaux à τ = 10 s,
soit 3 600 nets après la marge MTP de 2 h (contre 6 000 nets à 6 s). Les valeurs ci-dessous sont lues dans `composition.csv` à p_late = 10⁻², donc conservatrices pour W1 à deux sauts et τ = 10 s.

| Profil | ε_H (10 ans) | τ = 6 s : b / K_reg | 8 s | **10 s** | 12 s | 7 200 / 2 880 actuel à 10 s |
|---|---|---|---|---|---|---|
| A | 10⁻⁶ | 1 398 / 2 540 (4,2 h) | 1 380 / 3 938 | **1 367 / 4 762 (13,2 h)** | 1 355 / 5 296 | **échoue** (b = 2 880 > b_max) |
| A | 10⁻⁹ | 1 820 / 4 953 (8,3 h) | 1 803 / 6 355 | **1 789 / 7 176 (19,9 h)** | 1 778 / 7 712 | **échoue** |
| B | 10⁻⁶ | 1 273 / 1 | 1 257 / 457 | **1 244 / 1 310 (3,6 h)** | 1 234 / 1 872 | passe (3,5·10⁻⁸) |
| B | 10⁻⁹ | 1 658 / 445 | 1 642 / 1 886 | **1 629 / 2 739 (7,6 h)** | 1 619 / 3 301 | passe (3,3·10⁻¹¹) |

- **Le couple actuel 7 200 / 2 880 n'est pas une dérivation.** En profil A, il n'est **certifié qu'à τ = 6 s, p_late = 0 et ε_H = 10⁻⁶**.
  Il est non certifié dès p_late = 10⁻² à 6 s (b_max = 2 784 pour ε_H = 10⁻⁶ et 2 484 pour 10⁻⁹) et dès τ ≥ 8 s. « Non certifié » ne veut
  pas dire « attaqué » : c'est la borne par union qui ne suffit plus.
- La valeur K_reg = 1 en profil B à faible τ signifie que la garde Bitcoin couvre déjà le besoin. Le K_reg retenu relève alors d'autres
  rôles (anti-grinding §5.8), ce qui est une **décision**.
- Q_B = 256 (grinding de graine Bitcoin) n'est **pas qualifié** : il augmente K_reg (profil A, **p_late = 0**, ε_H = 10⁻⁶ : 3 295 à 6 s,
  6 083 à 12 s).
- **Statut** : les lignes de `composition.csv` utilisées portent `extrapolated=True` (DP extrapolée sous 10⁻¹⁴), et la composition des deux
  pivots reste une **esquisse sous hypothèses**. Ces valeurs sont des **dérivations conditionnelles, pas des garanties acquises**.

## 5. Tableau demandé, comparé en temps réel (W1, deux sauts, profil A, ε = 10⁻¹² par cible, ε_H = 10⁻⁹ sur 10 ans)

| τ | p_late (W1, 2 sauts) | K(10⁻¹²) | temps K | K_reg dérivé (b) | pivot profond | marge réseau (1 saut, max observé / budget) |
|---|---:|---:|---:|---|---|---|
| 6 s | 1·10⁻¹ | hors grille (K existe, seuil p < 0,1875, mais il est très grand) | — | — | fenêtre d'antidatage MTP = 1 200 créneaux | **4,7 / 5 s : falaise** |
| 8 s | 2·10⁻³ | ≈ 2 900 | ≈ 6,4 h | ≈ 6 400 (1 800), ≈ 14 h | 900 créneaux | 4,7 / 7 s |
| **10 s** | **1·10⁻⁵** | ≈ 2 870 | **≈ 8 h** | **≈ 7 200 (1 790), ≈ 20 h** | 720 créneaux | **4,7 / 9 s : large** |
| 12 s | ≈ 0 | ≈ 2 870 | ≈ 9,6 h | ≈ 7 700 (1 780), ≈ 26 h | 600 créneaux | 4,7 / 11 s |

Colonne « pivot profond » : les témoins TLA+ sont confirmés dans le modèle réduit. Aux paramètres réels, un nœud synchronisé fait STOP pour
les engagements d'époque dès h > 0,267. Pour les installations antérieures au début d'époque, le terme T_profond est **absorbé par la
composition** quand (b, K_reg) sont dérivés comme ci-dessus ; il n'est pas absorbé avec 7 200 / 2 880 en profil A à τ ≥ 8 s. Aucune
mécanique nouvelle n'est proposée : le dimensionnement (b, K_reg) le couvre **dans la composition esquissée**, ce qui n'est pas encore
une garantie démontrée.

En profil B, le même tableau donne à τ = 10 s : K(10⁻¹²) ≈ 1 900 créneaux ≈ 5,3 h, et K_reg ≈ 2 740 (b ≈ 1 630) ≈ 7,6 h.

## 6. Recommandation de l'orchestrateur et décisions du propriétaire

**Recommandation :**
- **τ = 10 s.** La marge réseau passe de « falaise » à « large » ; le coût est K ≈ 8 h au lieu de 4,8 h en profil A.
- **Domaine réseau H_N** : liens de classe W1 (aller-retour ≲ 170 ms, perte ≲ 0,5 %), **au plus deux sauts** de relais entre un producteur
  honnête et tout honnête, et horloges ≤ 100 ms. **W2 est hors domaine** ⇒ STOP/RECOVERY, pas de garantie.
- **Profil B** si la disponibilité honnête de 0,7 est crédible au lancement : K_reg ≈ 2 740 et b ≈ 1 630, avec de grandes marges. Sinon,
  profil A avec K_reg ≈ 7 200 et **b ≈ 1 790 (et non 2 880)**.

**Décisions demandées :**
1. τ (6 / 8 / **10** / 12).
2. Domaine réseau : classe de liens et nombre de sauts maximal.
3. Profil (β_max, d_min) : A ou B.
4. ε_H sur 10 ans (10⁻⁶ ou 10⁻⁹) et hypothèse Q_B (1, ou 256 non qualifié).

Ensuite, tout est dérivé : K_reg, registry_min_blocks, et les textes N-SPEC dépendant de τ (§5.2 « 36 h », §5.8 « 86 400 s / 79 199 s »,
L_epoch en heures, fenêtres en créneaux). Ce sont des paramètres, pas des mécaniques.

**Réserves Codex (revue T2, intégrées)** :
- Le 10⁻⁵ de W1 à deux sauts et τ = 10 s correspond à **2 excès sur 200 000 tirages synthétiques**, issus de 721 livraisons qui mélangent
  les phases espacées de 6 et de 10 s. Il n'a pas de borne de confiance multi-sauts.
- `plate.py` ne compte que les livraisons reçues. Il n'établit ni la réception par **tous** les honnêtes, ni une borne sur **toute fenêtre de
  K créneaux**, ni H_late (indépendance des retards), alors que DERIVATION-K les exige.
- « Tient », « large » et « conservateur » sont donc des **lectures de mesures et d'émulation**, pas des certifications.
- **Exclure W2 est un choix de domaine** (à deux sauts, la condition d'existence est violée aux coins A et B). Le banc ne démontre pas que
  STOP/RECOVERY se déclenche dans ce cas.

**Limites** :
- trois points de mesure européens ; les profils mondiaux sont émulés ;
- 45 min par sous-phase : le p99.9 à un saut n'est pas résolu, seulement borné à ≈ 4·10⁻³ ;
- sauts multiples extrapolés par sommation indépendante ;
- Δ_val hors accès à l'état ;
- écart DP/MC non expliqué.

Une campagne étendue (plus de points, durée plus longue, client N réel) fait partie de la phase « banc réseau étendu » après le gel.
