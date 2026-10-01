# Critères de gel architectural — état au 01/10 (N-SPEC v0.7)

Critères fixés par le mandat orchestrateur (`DIRECTION.md`, 01/10). Statuts : ✅ rempli, ⚠️ rempli avec réserve, ❓ en attente d'une
décision du propriétaire.

| # | Critère | État | Preuve / réserve |
|---|---|---|---|
| 1 | Machine déterministe cohérente sous tests formels | ✅ | TLA+ v0.6 : A on PASS 4/4, C6 8/8, H1 9/9, voie lente PASS — **PASS exhaustifs bornés aux paramètres abstraits des modèles**, pas une preuve pour tous les paramètres. La v0.7 ne change aucune mécanique et les constantes TLA+ sont abstraites |
| 2 | Anciennes variantes cassées toujours cassables | ✅ | A off ⇒ FAIL 4/4 ; 13/13 mutations détectées |
| 3 | Δ et marge d'horloge mesurés | ⚠️ | Banc r1/r2 (`SYNTHESE-BANC-TAU.md`). Réserves : trois points européens, WAN émulé, sauts multiples extrapolés, p_late par fenêtre non certifié |
| 4 | τ dérivé des mesures | ✅ | τ = 10 s (décision du propriétaire fondée sur W1 : 4,7 s au pire contre un budget de 9 s) |
| 5 | H_N publié (β_max, d_min, réseau, exclusions) | ✅ | N-SPEC v0.7 §17 : profil B, W1 ≤ 2 sauts, ε_H = 10⁻⁹ sur 10 ans, exclusions et comportement hors domaine |
| 6 | Analyse analytique et simulation stratégique convergentes pour un K_reg défendable | ⚠️ | La DP exacte borne par le haut, et le MC Codex ne la dépasse jamais (z max 1,6). L'écart DP/MC (facteur 1,3 à 1,8) n'est pas expliqué ; K_reg est pris sur la DP, conservatrice |
| 7 | Pivot profond qualifié | ⚠️ | 4 témoins TLA+ (3 stricts : 2 replays dirigés et 1 exploration semi-dirigée ; 1 en exploration à adversaire restreint) ; couvert en probabilité par T_profond dans la composition (esquisse) ; l'exploration stricte est INCOMPLET |
| 8 | Nœuds nouveaux ou de retour documentés (A′/RELEASE) | ✅ | §12.15 : D1 + **Q1 décidé** (RECOVERY explicite du §12.14 = chemin de réintégration ; réservations de signature conservées, §7.6). Procédure opérationnelle par nœud (dossier signé 3 sur 4) à écrire en phase d'implémentation |
| 9 | Aucune contradiction non expliquée (fork-choice, registre, graine, calendrier, maxreorg) | ⚠️ | `cp-reg/COHERENCE-v0.7.md` : aucune contradiction de sûreté. **Q3 décidé et traité** : profil de livraison H_N `rho_deliv = 43/100`, frein `health_min = 7/10` inchangé ; non-interférence TLA+ **PASS borné** (13 classes, 5 témoins, 3 mutations détectées), revue Codex corrigée. Réserves : frein simplifié dans le modèle ; probabilités à fenêtre fixe ; à la profondeur 77, une vue éclipsée (hors domaine) peut être livrée à tort avec une probabilité d'au plus 5,6·10⁻⁴ |

**Conclusion de l'orchestrateur (mise à jour après Q1/Q3).** Les 9 critères sont remplis, dont 4 avec réserves documentées (3, 6, 7 et 9). **N v0.7 est proposé
comme candidat au gel architectural.** Petites questions restantes, sans effet sur l'architecture : `alpha_budget` et `Delta_nom_ms` à aligner (documentation, QR-10).
Depuis, Q3-bis a été décidé (profondeur de livraison H_N = K(10⁻⁶) = 739 blocs, CHANGELOG n° 45) et β = 3/10 est inscrit dans le profil
de livraison H_N (CHANGELOG n° 43) ; la probabilité de 5,6·10⁻⁴ citée au critère 9 se rapporte à l'ancienne profondeur 77. Les réserves des critères 3, 6 et 7 relèvent de la
suite prévue par le mandat : implémentation → simulation → fuzzing → banc étendu → audit.
