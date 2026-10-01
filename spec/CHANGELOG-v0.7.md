# CHANGELOG — N-SPEC v0.7

1er octobre 2026. Statut : **candidate ; non qualifiée mainnet**. Base : `N-SPEC-v0.6.md`, copiée puis modifiée aux seuls endroits ci-dessous. Autorité : `DIRECTION.md`, lignes « Mandat orchestrateur — dernier chantier avant gel (01/10) », « Lemme L1 / CP_reg — décisions (01/10) » et « Domaine H_N — décisions (01/10) ».

> **Aucune mécanique modifiée.** Aucune règle de validation, de sélection, de dérivation du registre, de graine, de loterie, d'ancre, d'arrêt, de récupération ni aucun format n'a changé. Les changements portent sur trois valeurs de paramètres réseau (IDs 4, 49, 54), une valeur de profil client (ID 23), les textes et vecteurs qui en dépendent, la publication du domaine H_N (§17), l'état de l'analyse CP_reg (§5.7.2, §23) et une section descriptive sur les nœuds nouveaux ou de retour (§12.15). Contrôle de cohérence : `cp-reg/COHERENCE-v0.7.md`.

## Paramètres finaux

| Paramètre | v0.6 | v0.7 | Origine |
|---|---:|---:|---|
| `tau_ms` (réseau ID 4) | 6 000 | **10 000** | Décision du propriétaire (01/10), sur banc r1/r2 (`SYNTHESE-BANC-TAU.md`) |
| `K_reg` = `registry_stability_slots` (réseau ID 49) | 7 200 | **2 750** | `composition.csv` : `K_reg_min = 2 739`, arrondi vers le haut |
| `registry_min_blocks` (réseau ID 54) | 2 880 | **1 630** | `composition.csv` : `b = b_min = 1 629`, arrondi vers le haut |
| `maxreorg` (profil client ID 23) | 2 880 | **1 630** | Égalité imposée par le §3.3 |
| `fee_maturity_links` (réseau ID 40) | 2 880 | 2 880 (inchangé) | ≥ maxreorg |
| `reference_protection_links` (profil ID 28) | 2 880 | 2 880 (inchangé) | ≥ maxreorg |
| `L_epoch` (réseau ID 5) | 14 400 | 14 400 (inchangé) | Durée : 24 h → **40 h** (conséquence) |

### Ligne source et arrondi

Ligne de `etudes/n-spec/cp-reg/derivation/results/composition.csv`, vérifiée : `beta=0.3, d=0.7, p=0.01, tau=10, eps_H=1e-09, Q_B=1, mode=b=b_min` → `E=2192, G=3600, eps_epoch=4.562e-13, b=1629, b_min_live=1629, K_fix_slots=2066, K_inst_req=6339, K_reg_min=2739, K_reg_hours=7.61, b_max_given_Kreg=1629, eps_H_composed=5.111e-10, sep_5_8_s=70590, extrapolated=True`.

Arrondi :
1. `b` passe de 1 629 à 1 630. C'est la marge de vivacité, puisque `b ≥ b_min` garde la probabilité d'un HALT forcé sous ε_ep/4.
2. Le couple naïf (2 740 ; 1 630) **ne convient pas** : `b_max(2 740) = 1 629 < 1 630`, et le budget du pivot (ε_ep/2) serait dépassé. Chaque bloc de `b` coûte environ `1/h' ≈ 2,06` créneaux de `K_reg` (`b = 1 630` exige `K_reg ≥ 2 741`).
3. `K_reg` est arrondi à **2 750**, première dizaine compatible : `b_max(2 750) = 1 634 ≥ 1 630`.
4. Le recalcul a été fait avec la fonction existante `derive_k.compose`, sur les courbes DP publiées (`dp_curves.npz`), sans nouvelle simulation. Il donne pour (2 750 ; 1 630) : `T_fix = 5,4e-40`, `T_court = 7,6e-15`, `T_profond = 1,95e-13`, `T_CG = 7,6e-15`. Chaque terme tient dans son budget (ε_ep/4, ε_ep/2 pour les deux pivots ensemble, ε_ep/4). On obtient `ε_ep = 2,10e-13` et **`ε_H = 4,61e-10 ≤ 1e-9`**. À `p_late = 1e-3` : 5,3e-11. À `Q_B = 256` : 1,5e-7, ce qui est **hors cible** (Q_B = 256 non qualifié).

## Liste exhaustive des changements

Les numéros de section sont ceux de la v0.7.

| # | Section | Ancien → nouveau | Source de la dérivation |
|---:|---|---|---|
| 1 | Titre | « N-SPEC v0.6 » → « N-SPEC v0.7 » | — |
| 2 | En-tête | Date 30/09 → 01/10 ; « Remplace v0.5 » → « Remplace v0.6 » | — |
| 3 | Préambule, §1 | Ajout de l'objet de la v0.7 (paramètres dérivés + H_N, aucune mécanique), des sources et de l'arrondi | DIRECTION 01/10 |
| 4 | Préambule, §2 | « CP_reg bloquante avant gel » → CP_reg analysée sous H_N, garantie conditionnelle | DERIVATION-K §5, SYNTHESE §4 |
| 5 | Préambule, avant-dernier § | « valeurs de travail de la v0.6 » → valeurs v0.6 inchangées + trois dérivés v0.7 valables dans H_N | DIRECTION 01/10 |
| 6 | §1.3 | « passent en version 6 … règles v0.6 » → « restent en version 6 (formats inchangés) … règles v0.7, qui ne diffèrent que par des valeurs et H_N » | — |
| 7 | §2.5 | `maxreorg = 2880`, `≥ 2880 ⇔ ≥ 2881` → `1630`, `≥ 1630 ⇔ ≥ 1631` | composition.csv (b) |
| 8 | §2.5 | Ajout : frais et références restent à 2 880 liens ≥ maxreorg | §3.3 |
| 9 | §3.2 | En-tête de colonne « Valeur v0.6 » → « Valeur v0.7 » | — |
| 10 | §3.2 ID 4 | `tau_ms` 6 000 → **10 000** | Décision propriétaire |
| 11 | §3.2 ID 49 | `K_reg` 7 200 → **2 750** | composition.csv, arrondi |
| 12 | §3.2 ID 54 | `registry_min_blocks` 2 880 → **1 630** | composition.csv, arrondi |
| 13 | §3.2, note | « valeurs nouvelles en gras = choix de travail » → choix v0.6 inchangés ; IDs 4/49/54 fixés par la v0.7 (décision, dérivation) | — |
| 14 | §3.3 ID 23 | `maxreorg` 2 880 → **1 630** | §3.3 (égalité) |
| 15 | §3.3, contraintes | `client.maxreorg = consensus.registry_min_blocks = 2880` → `= 1630` ; commentaires `2880 ≥ 1630` | §3.3 |
| 16 | §3.3 | Ajout : contrainte de fenêtre vérifiée à τ = 10 s (3 000 < 10 000) ; `Delta_nom_ms` ≠ borne de délai H_N | Calcul |
| 17 | §5.1 | Ajout : époque = 40 h à τ = 10 s (L_epoch inchangé) ; fenêtres en créneaux/époques ×10/6 en durée ; E = 2 192 | Calcul |
| 18 | §5.2 | `K_reg = 7200` → `2750` | composition.csv |
| 19 | §5.2 | « précède … de 36 heures au moins » → `(K_reg + L_epoch)·τ = 171 500 s`, **47 h 38 min** | Calcul |
| 20 | §5.7.2 | « CP_reg bloquante ; tant que l'analyse manque… » → état sous H_N : formule de composition, ε_CP ≈ 4,6e-10 ≤ 1e-9, table des termes et statuts, cinq points ouverts (écart DP/MC 1,3–1,8 ; Q_B = 256 ; TLA+ strict INCOMPLET ; p_late par fenêtre non certifié ; A4 non requalifiée), interdiction de présenter l'immutabilité hors H_N | DERIVATION-K §5–7, SYNTHESE §4 et réserves, PIVOT-PROFOND-TLA §4 |
| 21 | §5.8 | `K_reg × τ + garde = 43200 + 43200 = 86400 s` → `27500 + 43200 = 70700 s` | composition.csv (`sep_5_8_s` recalculé pour 2 750) |
| 22 | §5.8 | Marge `86400 − 7200 − 1 = 79199 s` → `70700 − 7200 − 1 = 63499 s` | Calcul |
| 23 | §5.8 | Ajout : rappel des valeurs v0.6, garde 12 h inchangée | — |
| 24 | §7.2 | Ajout : bornes en ms absolues, cohérentes à τ = 10 s (9 s de budget, condition D = 0) | SYNTHESE §2 |
| 25 | §8.4 | Ajout : marge MTP = 720 créneaux ; `G(τ) = 3 600` ; premier porteur légal ≥ `snapshot_cut + K_inst`, `K_inst = 6 350` | DERIVATION-K §5 |
| 26 | §9.6 | « plus de 2 880 déconnexions » → « plus de `maxreorg` = 1 630 » | §2.5 |
| 27 | §11.5 | « 2 880 liens représentent 4,8 h » → « 1 630 liens représentent 16 300 s ≈ 4,5 h (≈ 9,3 h à h' ≈ 0,485) » ; `4,8h` → `4,5h` dans la formule | Calcul |
| 28 | §12.15 (nouvelle) | Nœuds nouveaux ou de retour : synchronisé / hors domaine / retour par origine récente (≥ maxreorg + 1 = 1 631 blocs après toute fourche) ; seuls chemins existants ; question de réintégration renvoyée au propriétaire | D1 (DIRECTION 01/10), CONFRONTATION-LEMME-L1 §2 et §5 |
| 29 | §15.5 | Ajout : H_N suppose Q_B = 1 ; 256 non qualifié | DIRECTION 01/10 |
| 30 | §17.1–17.6 (nouveaux) | Domaine H_N complet : principe et statuts ; quinze hypothèses H_N-1 à H_N-15 (τ, β_max, d_min, h_min, p_late_max et H_late, W1, ≤ 2 sauts, horloges, Δ_val, condition et marge, d_min renforcé, ε_H, Q_B, origine, adversaire) ; table K(ε) pour 10⁻⁶ / 10⁻⁹ / 10⁻¹² ; dérivation et arrondi de K_reg / b ; exclusions ; comportement hors domaine (aucune prétention quantitative, exposition de l'état, STOP/RECOVERY existants seulement, pas de garantie de STOP) | SYNTHESE-BANC-TAU, K-table.csv, composition.csv, DERIVATION-K §2–8 |
| 31 | §17.7 | Ancien tableau des hypothèses à publier, conservé sous ce titre | — |
| 32 | §19.2 | Budget « à six secondes » : 14 400 blocs/j, 34 848 000, 40 608 000, 3 774 873 600 o/j → « à dix secondes » : **8 640** blocs/j, **20 908 800**, **24 364 800**, **2 264 924 160** o/j | 86 400/τ × (2 420 ; 2 820 ; 262 144) |
| 33 | §19.3 | « reprise sans 2 880 nouveaux blocs » → « sans `maxreorg` = 1 630 » | §2.5 |
| 34 | §19.4 items 7, 8, 9 | Ajout de l'état v0.7 de chaque condition (aucune condition retirée) | §5.7.2, §17 |
| 35 | §20.2 | `snapshot_cut(..., stability=7200)` → `2750` ; asserts `-7200 / 7200` → `-2750 / 11650` (noyau réexécuté : OK) | K_reg |
| 36 | §20.4 | Vecteur d'ancre : `T.height=5000` → `3750` (maxreorg = 1 630), pour garder `Nbound = 2120` et les trois lignes inchangées | §9.6 |
| 37 | §21.10 | « 1440 créneaux = 2,4 heures » → « = 4 heures » ; « partition inférieure à 2,4 heures » → « 4 heures » | τ (ommer_horizon inchangé) |
| 38 | §23.1 | Ajout : état CP_reg sous H_N (conditionnel, pas un théorème, A4 non levée) ; constantes TLA+ v0.6 abstraites | PIVOT-PROFOND-TLA, PORTEE-ET-MAPPING |
| 39 | §23.4 A3 | « ni 2 880 blocs d'une seule branche » → « ni `maxreorg` blocs » | §2.5 |
| 40 | §23.4 H_N | Ajout : le domaine publié est celui du §17 | §17 |
| 41 | §23.10 | Ajout : l'analyse sous H_N fournit unités, horizon, probabilité ; reste conditionnelle ; exploration stricte INCOMPLET | §5.7.2 |
| 42 | §24 | Phrase d'introduction et nouvelle ligne de traçabilité v0.7 | — |

Total : **42 changements**.
- 7 valeurs de paramètres ou égalités : n° 7, 10, 11, 12, 14, 15, 18.
- 12 textes ou vecteurs recalculés : n° 19, 21, 22, 25, 26, 27, 32, 33, 35, 36, 37, 39.
- 3 sections nouvelles ou réécrites : n° 20, 28, 30.
- 20 notes, mises à jour d'état ou changements éditoriaux : les autres numéros.

## Ce qui n'a pas changé (vérifié)

- Toutes les règles et tous les formats. Les versions de format restent : manifeste 6, KEYREG/ROTATE/bloc 3.
- `L_epoch`, `seed_guard_seconds = 43 200`, `btc_slot_mtp_margin_seconds = 7 200` et toutes les valeurs en secondes ou en hauteurs Bitcoin (H1, G_anchor, grâce REACT, D_btc).
- Les fenêtres exprimées en créneaux ou en époques : `ommer_horizon = 1 440`, `evidence_horizon = 14 400`, fenêtres d'activité et de contestation, voie lente. Seule leur durée change (×10/6), et aucune contradiction n'est démontrée (COHERENCE §5).
- `fee_maturity_links = 2 880` et `reference_protection_links = 2 880`. Les vecteurs §20.6 (2 879/2 880 liens) et G7 §21.7 restent valides, puisqu'ils portent sur la maturité des frais et non sur maxreorg.
- `k_default = 77`, `Q_B_work = 256` et `M_work = 14 400` : valeurs de laboratoire du §15.4, hors H_N.
- `delta_clock_ms = 500` et `Delta_nom_ms = 1 000` : tolérances de profil compatibles avec H_N (horloges ≤ 100 ms) ; voir COHERENCE Q4.
- Les mentions historiques « v0.6 » qui désignent l'origine d'une règle (§9.1, §12.1, §12.13, titres des cas §20).

## Propositions non retenues

- Changer `L_epoch` pour garder une époque de 24 h : exclu par la consigne, et ce serait un changement de calendrier.
- Retenir le couple (2 740 ; 1 630) arrondi indépendamment : il viole `b ≤ b_max(K_reg)`.
- Ajouter une règle de réintégration des nœuds de retour, un indicateur de domaine contraignant ou un STOP automatique hors domaine : ce seraient des mécaniques nouvelles, renvoyées au propriétaire (COHERENCE).

## Ajouts après les décisions Q1 et Q3 (01/10)

Autorité : `DIRECTION.md`, ligne « Gel v0.7 — Q1/Q3 (01/10) ». Dérivation et vérification : `cp-reg/LIVRAISON-HN.md`. Ces ajouts ne modifient aucune mécanique : ni le frein (§6.6, `7/10` inchangé), ni la fork-choice, ni la règle A, ni STOP.

| # | Section | Ancien → nouveau | Source |
|---:|---|---|---|
| 43 | §14.2, nouvelle sous-section « Profil de livraison H_N » | Ajout d'une instance du profil client v6, au format inchangé, propre à H_N : `rho_deliv` (IDs 6–7) = **43/100** sur les fenêtres de 100 et 1 000 créneaux et depuis l'inclusion ; `beta_default` = `beta_delivery_max` = 3/10. Le texte ajoute : la table des risques binomiaux au coin du domaine ; la profondeur 77 inchangée, avec renvoi à K(ε) du §17.3 sur décision du propriétaire ; la séparation entre `rho_deliv` (profil) et la constante du frein `health_min = 7/10` (consensus, inchangée) ; la lecture de `rho_min` au §14.3 comme seuil du profil actif ; la non-interférence avec la fork-choice, l'ancre, STOP, la règle A, le frein, la voie lente, H1 et la production | Q3 ; `cp-reg/livraison-hn/seuils.py` ; `tla/modele-v0.6/NonInterference_Deliv.tla` |
| 44 | §12.15 | Le point « chemin de réintégration … question ouverte (Q1) ; la v0.7 n'en active aucun » est remplacé par la décision : la `RECOVERY` explicite du §12.14 est **le** chemin de réintégration d'un nœud de retour qui conserve son origine (KNOWN_CONTEXT ou LOST_CONTEXT, acceptation ponctuelle, réservations de signature et mémoire anti-double-signature conservées, §7.6). La réinstallation en nœud sans origine reste possible (observateur, ou producteur avec rotation) ; l'option (ii) n'est pas retenue ; aucune équité de RECOVERY ; la procédure opérationnelle d'émission du dossier est renvoyée à la politique RELEASE | Q1 |
| 45 | §14.2 profil de livraison H_N | profondeur 77 (laboratoire) → **K(10⁻⁶) = 739 blocs** par défaut, table K(ε) exposée, choix SP/LP | Décision du propriétaire Q3-bis (01/10) ; paramètre de profil, aucune mécanique |

Total après ces ajouts : **45 changements**. Les trois nouveaux sont des textes descriptifs ou des valeurs de profil client ; aucune valeur réseau ni aucun format n'est modifié.

