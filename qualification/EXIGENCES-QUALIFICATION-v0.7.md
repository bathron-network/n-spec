# Exigences de qualification — N v0.7 (architecture gelée le 01/10)

**Statut exact : N v0.7 est un candidat gelé au niveau architectural. Ce n'est pas une qualification mainnet.**

Décision du propriétaire du 01/10 (`DIRECTION.md`, ligne « Gel architectural N v0.7 »). Toute modification future de l'architecture doit être
motivée par l'un de ces quatre déclencheurs, et non par la recherche d'une architecture « plus élégante » :
- un **contre-exemple** ;
- une **violation d'invariant** ;
- une **impossibilité d'implémentation** ;
- une **mesure réelle incompatible avec H_N**.

Une valeur de paramètre mal choisie n'est pas un défaut architectural : on la corrige dans H_N ou dans le profil.

Chaque réserve de `CRITERES-GEL-v0.7.md` devient ci-dessous une exigence traçable, avec sa phase, son critère d'acceptation, son statut
actuel et ce qui se passe en cas d'échec.

| ID | Origine (critère / réserve) | Exigence | Phase | Critère d'acceptation | Statut au 01/10 | Si échec |
|---|---|---|---|---|---|---|
| **QR-1** | 3 : banc européen, WAN émulé, sauts multiples extrapolés | Mesurer Δ, l'écart d'horloge et p_late avec un **client N réel** sur au moins 3 continents, à au moins 2 sauts réels, avec des blocs maximaux et la charge prévue | Banc étendu | p_late ≤ 10⁻² sur toute fenêtre de 1 913 créneaux (H_N-4), avec une borne de confiance à 95 % ; pire cas d'un saut ≤ 9 s − Δ_val ; horloges ≤ 100 ms | Mesure européenne + émulation W1/W2 (`SYNTHESE-BANC-TAU.md`) | Mesure réelle incompatible avec H_N : réviser τ ou le domaine (paramètres), ou optimiser la propagation (implémentation) |
| **QR-2** | 3 / H_N-4 : p_late par fenêtre non certifié, H_late (indépendance) supposée | Estimer la corrélation des retards et la borne par fenêtre, y compris sous coupures et sous DoS ciblé d'un producteur | Banc étendu + simulation | Test d'indépendance non rejeté, ou modèle corrélé intégré à `derive_k.py` avec un K recalculé ≤ K_reg | Supposée | Corrélation réelle : la réintégrer dans la dérivation de K ; les retards ciblés comptent dans β |
| **QR-3** | 6 : écart DP/MC d'un facteur 1,3 à 1,8 sur K | Écrire la meilleure stratégie à deux branches sous le départage de N (simulateur exact ou DP restreinte), puis expliquer l'écart | Simulation | Écart expliqué, ou nouvelle borne ≤ DP publiée ; K_reg reste ≥ la valeur requise | Ouvert (on publie la DP, conservatrice) | Si une stratégie dépasse la DP (aucune ne l'a fait jusqu'ici) : **contre-exemple**, réouverture de K_reg |
| **QR-4** | 7 : exploration TLA+ stricte du pivot profond INCOMPLET | Terminer `MC_explore_sync_PivotDeep` (plus de mémoire ou de temps, symétries, Apalache) ou en prouver une abstraction | Simulation (formel) | PASS exhaustif borné des invariants de sûreté, plus les témoins conservés | INCOMPLET (5,2 M états) | Violation d'invariant : réouverture architecturale |
| **QR-5** | 9 / Q3 : frein simplifié dans le modèle de non-interférence | Refaire la non-interférence de `rho_deliv` avec le frein fidèle au §6.6 (trois époques, plafonds pondérés, voie lente réelle), puis sur l'implémentation (traces différentielles) | Implémentation + fuzzing | Traces de consensus identiques pour deux seuils de livraison, sur le modèle fidèle et en fuzzing différentiel | PASS borné sur le modèle simplifié | Une fuite vers le consensus est une violation d'invariant à corriger dans l'implémentation |
| **QR-6** | Composition des pivots (esquisse), `extrapolated=True` | Rédiger la preuve de la composition ε_fix + pivots + T_CG, puis la faire relire par une analyse indépendante | Audit | Preuve relue, et budgets ε_ep respectés aux paramètres v0.7 | Esquisse sous hypothèses | Un trou de preuve : borne révisée, et K_reg / b re-dérivés (paramètres) |
| **QR-7** | Q_B = 256 non qualifié | Qualifier le grinding de graine Bitcoin (MTP, rétention, timestamps), puis décider de Q_B | Audit + simulation | Q_B borné et ε_H ≤ 10⁻⁹ au K_reg retenu, ou K_reg re-dérivé | Q_B = 1 supposé | Paramètre à re-dériver, pas de mécanique |
| **QR-8** | Q1-bis : procédure opérationnelle de RECOVERY par nœud (dossier signé 3 sur 4, ou contexte perdu) | Spécifier et tester la procédure de réintégration d'un nœud de retour | Implémentation | Procédure documentée, testée en bout en bout, réservations de signature conservées (§7.6) | Non spécifiée | Impossibilité d'implémentation : réouverture limitée au §12.14 |
| **QR-9** | A4 (ancres) non requalifiée en v0.7 | Requalifier A4 aux paramètres v0.7 (maxreorg = 1 630, τ = 10 s) | Simulation (formel) | Propriétés A4 PASS sur les modèles mis à l'échelle | Ouvert | Violation d'invariant : réouverture |
| **QR-10** | Documentation : `alpha_budget = 1/20` et `Delta_nom_ms` non alignés sur le coin H_N ; β = 3/10 du profil à harmoniser | Aligner les profils clients sur H_N | Implémentation | Profils cohérents avec §17 | Ouvert | — |

Les phases suivent l'ordre du mandat : **implémentation → simulation → fuzzing → banc réseau étendu → audit externe → testnet**. Cet ordre
signifie que chaque exigence est vérifiée au plus tard dans sa phase, et que le testnet public suppose QR-1 à QR-9 acceptées.
