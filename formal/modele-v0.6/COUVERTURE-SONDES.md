# Inventaire des sondes et de leur portée

Les statuts effectifs et compteurs sont dans `RESULTATS.json` et `RESULTATS-DETAILLES.md`. Utiliser les configurations `_checked` lorsqu'elles existent. Les premiers essais des modules non suffixés sont des essais de développement conservés. Les témoins portent une anti-propriété `NoWitness…` : seul un échec TLC explicite de cette anti-propriété vaut TÉMOIN.

| Sonde du mandat | Campagne finale / preuve à consulter | Réserve de portée |
|---|---|---|
| registry_threshold | `MC_registry_window_{1,2,4}_checked`, témoins Below/Threshold/Above | Portée des bornes, non preuve CP_reg. |
| registry_empty_repeat | `MC_witness_mirror_empty`, `MC_witness_registry_Empty_checked`, `MC_brake_inherited_after` | Deux époques vides de production ; calendrier et contrôle hérités testés dans une autre famille. |
| registry_late_seed | `MC_witness_registry_late` | Premier porteur au slot 5, époque réduite commençant au slot 4. |
| registry_closure_withholding | `MC_registry_commits_CPreg_checked`, `MC_replay_closure_checked_fixed`, RegistryWindow | Deux préfixes avec même support brut et comptes différents ; fixtures déclarées valides, loterie et sélection par Rank non rejouées. |
| registry_reorg_original | `MC_fast_off_*`, `MC_fast_on_*`, `MC_v6_replay_spec{,_adopt}_{off,on}` | Générateur élargi v0.5, nouvelle fermeture à la maturité réduite fixe, autres sous-machines historiques. |
| registry_reorg_general | `MC_general_a_k{1,2}_{strong,c6}`, `MC_registry_commits_RegistryImmutable_checked` | A3 global séparé du vieux moniteur local. |
| h1_bootstrap_orders | `MC_h1_forward_checked`, témoin CommonVeto, seuil 2 | Tous ordres des six événements et groupements simultanés, candidats préconstruits. |
| h1_maintain | témoin Maintain, mutation maintain, `MC_h1_reevaluation` | Ancienne adoption conservée pour inspection ; autorisation positive vide. |
| h1_orientation | inverse/mutual/losers/shallow `_checked` | Maxima avant H1, troisième branche et perdants. |
| h1_unknown_foreign | `MC_scan_foreign`, `MC_scan_matching`, témoins Unknown/Decidable | Scans et dossiers abstraits ; pas de traitement des octets de transactions. |
| h1_cadence_stale_refs | `MC_scan_stale_counterexample` | Test de l'affirmation supplémentaire « cadence ⇒ absence de veto », pas invariant normatif à faire passer. |
| brake_068 | `MC_brake_068_arithmetic`, témoin arithmétique, `MC_brake_068_checked` | Le 0,68 est la campagne arithmétique pondérée ; le calendrier temporel est cyclique. |
| brake_slow | `MC_brake_slow_checked`, `MC_brake_live_mechanical` (direct : `MC_brake_live_checked`), témoins Slow/Release, `logs/brake-reference.json` | WF(Advance), horizon de vingt époques, règles temporelles à faibles attributions. |
| brake_rounding_heavy | `MC_brake_rounding_checked`, `MC_brake_heavy_checked` | W=10/100 ; aucun max(1), queue poursuivie après poids lourd. |
| add_all_states | `MC_admissions_checked`, mutation add | Tous cinq états ; ban/exclusion avant achat, activité conservée, tickets dormants après exclusion. |
| react_first_exam | `MC_admissions_checked`, témoins React et late_price | F_x=59/60/61, x opaque, prix historique 10 vs prix ultérieur 20 ; rollback et réexamen. Authenticité et contenu du dossier abstraits. |
| equivocation_contexts | `MC_persistence_checked`, mutation generation | S1 avec préparation/témoin/export/commit, clones/restauration ; S2 algébrique et contrôle de génération non effective. |
| tie_selective_delivery | `MC_tie_parent`, `MC_tie_reservations` | Parents identiques à données communes ; réservations antérieures peuvent rester différentes. Une seule occasion bornée ne prouve pas L2. |
| anchor_exact_mixed | `MC_anchor_{1,2}_checked`, mutation free_anchor, `MC_anchor_agreement_checked` | Bornes N/BTC exactes ; tous maxima examinés, avant/après réunion. |
| bitcoin_slow_reorg | `MC_bitcoin_slow`, `MC_bitcoin_equal`, `MC_witness_bitcoin_slow`, `MC_witness_btc_checked` | Travail BTC unitaire ; arbres et égalité ; seuil D_btc=3 ou 2, liens N réduits à 3. Pas de qualification des 2880 liens/100 confirmations. |
| genesis_seal_only | `MC_witness_seal_only_checked`, mutation forget_seal | Retrait de a1 seul dans l'inventaire genesis (S0 et repère initial g inchangés), graine non consommée. |
| release_channels | `MC_authorities_checked`, témoin recovery | Deux canaux, contradiction, origine existante, demande exacte fraîche à usage unique ; aucun fair RECOVERY. |
| money_undo_crash | `MC_money_checked`, témoin money, mutation import | Petit noyau à trois pointes ; application complète et conversions NT. |

## Non qualifié / NT

- Composition de toutes les sous-machines dans un même état global : **NT**. Les résultats des familles ne sont pas multipliés ou composés en sûreté globale.
- CP_reg sous un domaine H_N probabiliste propre à N, calendrier public adversarial, grinding, corruptions et exposition sur tout l'horizon : **NT et bloquant**. Les FAIL sous partitions non bornées ne définissent pas un domaine sûr alternatif.
- A4 sous un domaine de réseau et Bitcoin qualifié : **NT et bloquant** ; les contre-exemples de l'abstraction sont publiés.
- Vivacité L2 générale et infinie : **NT**. Un suffixe de réunion avec données équitables et protection compatible est testé séparément ; aucune équité administrative.
- Machine complète à 144/30 attributions, intégration bans/rotations/ADD/REACT et comparaison grand saut/incrémental de **tout** ce contrôle : **NT**. Le rejeu des fenêtres temporelles, les budgets calendaires, la rotation sous frein, les effets ADD/REACT et un ban prospectif sont vérifiés en familles séparées.
- Réservation et disponibilité d'un témoin externe réellement distribué, sécurité cryptographique, anti-rollback sans cet ancrage durable et restauration intégrée à toute la monnaie/au consensus : **NT**.
- BOOTSTRAP cryptographique multi-canaux et indépendance réelle de leurs opérateurs : **NT**, représentés par entrées validées.
- G1–G10 applicatifs, sources monétaires multiples typées, conversions, covenants, swaps, transactions réelles et intégration de MON1–MON5 avec ancre/genesis/H1/REACT : **NT**.

Ces NT font que la livraison ne satisfait pas une qualification intégrale de N v0.6. Le gel reste bloqué indépendamment du résultat borné du §8.
