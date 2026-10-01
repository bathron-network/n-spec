# Résultats bruts et provenance

Les valeurs `None` sont indisponibles. En timeout, les compteurs peuvent être ceux du dernier point publié, pas ceux de l’arrêt. Un PASS de développement ne qualifie pas la version corrigée. Les constantes, propriétés, empreintes TLC et motifs complets figurent dans RESULTATS.json et les .cfg.

| Run | Résultat | Code | Générés | Distincts | Profondeur | File | Durée s | Propriété violée / motif |
|---|---|---:|---:|---:|---:|---:|---:|---|
| [MC_admissions](logs/MC_admissions.log) | PASS (développement) | 0 | 3840 | 3840 | 4 | 0 | 0.59 | exhausted_bounded_graph |
| [MC_admissions_checked](logs/MC_admissions_checked.log) | PASS | 0 | 8640 | 6720 | 5 | 0 | 0.59 | exhausted_bounded_graph |
| [MC_anchor_1](logs/MC_anchor_1.log) | PASS (développement) | 0 | 11650 | 1172 | 9 | 0 | 0.68 | exhausted_bounded_graph |
| [MC_anchor_1_checked](logs/MC_anchor_1_checked.log) | PASS | 0 | 10594 | 1172 | 9 | 0 | 0.7 | exhausted_bounded_graph |
| [MC_anchor_2](logs/MC_anchor_2.log) | PASS (développement) | 0 | 11650 | 1172 | 9 | 0 | 0.68 | exhausted_bounded_graph |
| [MC_anchor_2_checked](logs/MC_anchor_2_checked.log) | PASS | 0 | 10594 | 1172 | 9 | 0 | 0.7 | exhausted_bounded_graph |
| [MC_anchor_agreement](logs/MC_anchor_agreement.log) | FAIL (développement) | 12 | 93 | 59 | 3 | 46 | 0.54 | A4 |
| [MC_anchor_agreement_checked](logs/MC_anchor_agreement_checked.log) | FAIL | 12 | 91 | 53 | 3 | 41 | 0.58 | A4 |
| [MC_audit_cp_k1](logs/MC_audit_cp_k1.log) | FAIL | 12 | 82493 | 17727 | 11 | 7888 | 10.07 | CPregGlobal |
| [MC_audit_cp_k2](logs/MC_audit_cp_k2.log) | FAIL | 12 | 155271 | 34850 | 12 | 16021 | 22.95 | CPregGlobal |
| [MC_authorities](logs/MC_authorities.log) | PASS (développement) | 0 | 872 | 306 | 8 | 0 | 0.54 | exhausted_bounded_graph |
| [MC_authorities_checked](logs/MC_authorities_checked.log) | PASS | 0 | 788 | 306 | 8 | 0 | 0.54 | exhausted_bounded_graph |
| [MC_bitcoin_equal](logs/MC_bitcoin_equal.log) | PASS | 0 | 10594 | 1172 | 9 | 0 | 0.65 | exhausted_bounded_graph |
| [MC_bitcoin_slow](logs/MC_bitcoin_slow.log) | PASS | 0 | 10594 | 1172 | 9 | 0 | 0.65 | exhausted_bounded_graph |
| [MC_brake_068](logs/MC_brake_068.log) | PASS (développement) | 0 | 21 | 21 | 21 | 0 | 11.63 | exhausted_bounded_graph |
| [MC_brake_068_arithmetic](logs/MC_brake_068_arithmetic.log) | PASS | 0 | 64 | 32 | 1 | 0 | 0.54 | exhausted_bounded_graph |
| [MC_brake_068_checked](logs/MC_brake_068_checked.log) | PASS | 0 | 21 | 21 | 21 | 0 | 12.4 | exhausted_bounded_graph |
| [MC_brake_heavy](logs/MC_brake_heavy.log) | INCOMPLET (développement) | 75 | 14 | 13 | 13 | 1 | 7.05 | tool_or_model_error |
| [MC_brake_heavy_checked](logs/MC_brake_heavy_checked.log) | PASS | 0 | 21 | 21 | 21 | 0 | 33.24 | exhausted_bounded_graph |
| [MC_brake_inherited](logs/MC_brake_inherited.log) | INCOMPLET (développement) | 75 | 15 | 14 | 14 | 1 | 9.05 | tool_or_model_error |
| [MC_brake_inherited_after](logs/MC_brake_inherited_after.log) | PASS | 0 | 21 | 21 | 21 | 0 | 40.42 | exhausted_bounded_graph |
| [MC_brake_inherited_checked](logs/MC_brake_inherited_checked.log) | PASS | 0 | 21 | 21 | 21 | 0 | 28.55 | exhausted_bounded_graph |
| [MC_brake_live](logs/MC_brake_live.log) | INCOMPLET (développement) | 143 | 6 | 6 | 6 | 0 (dernier point publié) | 570.02 | timeout |
| [MC_brake_live_checked](logs/MC_brake_live_checked.log) | INCOMPLET | 143 | 6 | 6 | 6 | 0 (dernier point publié) | 570.04 | timeout |
| [MC_brake_live_mechanical](logs/MC_brake_live_mechanical.log) | PASS | 0 | 21 | 21 | 21 | 0 | 28.76 | exhausted_bounded_graph |
| [MC_brake_rounding](logs/MC_brake_rounding.log) | PASS (développement) | 0 | 21 | 21 | 21 | 0 | 32.77 | exhausted_bounded_graph |
| [MC_brake_rounding_checked](logs/MC_brake_rounding_checked.log) | PASS | 0 | 21 | 21 | 21 | 0 | 37.91 | exhausted_bounded_graph |
| [MC_brake_slow](logs/MC_brake_slow.log) | INCOMPLET (développement) | 75 | 14 | 13 | 13 | 1 | 6.97 | tool_or_model_error |
| [MC_brake_slow_checked](logs/MC_brake_slow_checked.log) | PASS | 0 | 21 | 21 | 21 | 0 | 30.38 | exhausted_bounded_graph |
| [MC_c6_k1_00](logs/MC_c6_k1_00.log) | PASS | 0 | 874447 | 134506 | 25 | 0 | 128.42 | exhausted_bounded_graph |
| [MC_c6_k1_01](logs/MC_c6_k1_01.log) | PASS | 0 | 623667 | 92602 | 24 | 0 | 84.28 | exhausted_bounded_graph |
| [MC_c6_k1_10](logs/MC_c6_k1_10.log) | PASS | 0 | 2251944 | 351938 | 28 | 0 | 321.4 | exhausted_bounded_graph |
| [MC_c6_k1_11](logs/MC_c6_k1_11.log) | PASS | 0 | 1412791 | 213454 | 28 | 0 | 180.41 | exhausted_bounded_graph |
| [MC_c6_k2_00](logs/MC_c6_k2_00.log) | PASS | 0 | 815017 | 124850 | 26 | 0 | 124.06 | exhausted_bounded_graph |
| [MC_c6_k2_01](logs/MC_c6_k2_01.log) | PASS | 0 | 500905 | 73585 | 24 | 0 | 67.9 | exhausted_bounded_graph |
| [MC_c6_k2_10](logs/MC_c6_k2_10.log) | PASS | 0 | 1728952 | 268742 | 27 | 0 | 277.26 | exhausted_bounded_graph |
| [MC_c6_k2_11](logs/MC_c6_k2_11.log) | PASS | 0 | 1084144 | 162853 | 27 | 0 | 150.57 | exhausted_bounded_graph |
| [MC_fast_off_00](logs/MC_fast_off_00.log) | FAIL | 12 | 41399 | 8999 | 10 | 4324 | 1.6 | RegistryImmutable |
| [MC_fast_off_01](logs/MC_fast_off_01.log) | FAIL | 12 | 23040 | 5179 | 9 | 2584 | 1.24 | RegistryImmutable |
| [MC_fast_off_10](logs/MC_fast_off_10.log) | FAIL | 12 | 49306 | 11399 | 10 | 5869 | 1.79 | RegistryImmutable |
| [MC_fast_off_11](logs/MC_fast_off_11.log) | FAIL | 12 | 24143 | 5531 | 9 | 2823 | 1.25 | RegistryImmutable |
| [MC_fast_on_00](logs/MC_fast_on_00.log) | PASS | 0 | 1997645 | 280913 | 25 | 0 | 329.16 | exhausted_bounded_graph |
| [MC_fast_on_01](logs/MC_fast_on_01.log) | PASS | 0 | 1015556 | 141242 | 24 | 0 | 151.17 | exhausted_bounded_graph |
| [MC_fast_on_10](logs/MC_fast_on_10.log) | INCOMPLET | 143 | 3543392 | 549892 | 19 | 72479 (dernier point publié) | 569.12 | timeout |
| [MC_fast_on_11](logs/MC_fast_on_11.log) | PASS | 0 | 1971321 | 278093 | 26 | 0 | 296.37 | exhausted_bounded_graph |
| [MC_general_a_k1_c6](logs/MC_general_a_k1_c6.log) | INCOMPLET | 143 | 4435419 | 719926 | 20 | 59148 (dernier point publié) | 570.09 | timeout |
| [MC_general_a_k1_strong](logs/MC_general_a_k1_strong.log) | FAIL | 12 | 614809 | 123699 | 13 | 46852 | 29.81 | RegistryImmutable |
| [MC_general_a_k2_c6](logs/MC_general_a_k2_c6.log) | INCOMPLET | 143 | 3948521 | 614759 | 21 | 18586 (dernier point publié) | 570.1 | timeout |
| [MC_general_a_k2_strong](logs/MC_general_a_k2_strong.log) | FAIL | 12 | 755583 | 150933 | 14 | 54065 | 44.97 | RegistryImmutable |
| [MC_h1_false](logs/MC_h1_false.log) | PASS (développement) | 0 | 510369 | 26896 | 9 | 0 | 2.6 | exhausted_bounded_graph |
| [MC_h1_false_checked](logs/MC_h1_false_checked.log) | PASS | 0 | 510369 | 26896 | 9 | 0 | 2.59 | exhausted_bounded_graph |
| [MC_h1_foreign](logs/MC_h1_foreign.log) | PASS (développement) | 0 | 510369 | 26896 | 8 | 0 | 2.58 | exhausted_bounded_graph |
| [MC_h1_foreign_checked](logs/MC_h1_foreign_checked.log) | PASS | 0 | 510369 | 26896 | 8 | 0 | 2.56 | exhausted_bounded_graph |
| [MC_h1_forward](logs/MC_h1_forward.log) | PASS (développement) | 0 | 544621 | 30276 | 8 | 0 | 2.44 | exhausted_bounded_graph |
| [MC_h1_forward_checked](logs/MC_h1_forward_checked.log) | PASS | 0 | 544621 | 30276 | 8 | 0 | 2.44 | exhausted_bounded_graph |
| [MC_h1_forward_k2](logs/MC_h1_forward_k2.log) | PASS (développement) | 0 | 504973 | 27556 | 7 | 0 | 6.88 | exhausted_bounded_graph |
| [MC_h1_forward_k2_checked](logs/MC_h1_forward_k2_checked.log) | PASS | 0 | 504973 | 27556 | 8 | 0 | 2.36 | exhausted_bounded_graph |
| [MC_h1_inverse](logs/MC_h1_inverse.log) | PASS (développement) | 0 | 510369 | 26896 | 8 | 0 | 2.6 | exhausted_bounded_graph |
| [MC_h1_inverse_checked](logs/MC_h1_inverse_checked.log) | PASS | 0 | 510369 | 26896 | 9 | 0 | 2.54 | exhausted_bounded_graph |
| [MC_h1_losers](logs/MC_h1_losers.log) | PASS (développement) | 0 | 524833 | 28224 | 8 | 0 | 2.56 | exhausted_bounded_graph |
| [MC_h1_losers_checked](logs/MC_h1_losers_checked.log) | PASS | 0 | 524833 | 28224 | 8 | 0 | 2.58 | exhausted_bounded_graph |
| [MC_h1_mutual](logs/MC_h1_mutual.log) | PASS (développement) | 0 | 815361 | 50176 | 8 | 0 | 3.19 | exhausted_bounded_graph |
| [MC_h1_mutual_checked](logs/MC_h1_mutual_checked.log) | PASS | 0 | 815361 | 50176 | 8 | 0 | 3.24 | exhausted_bounded_graph |
| [MC_h1_reevaluation](logs/MC_h1_reevaluation.log) | PASS | 0 | 85 | 12 | 4 | 0 | 0.54 | exhausted_bounded_graph |
| [MC_h1_shallow](logs/MC_h1_shallow.log) | PASS (développement) | 0 | 356865 | 16384 | 7 | 0 | 2.11 | exhausted_bounded_graph |
| [MC_h1_shallow_checked](logs/MC_h1_shallow_checked.log) | PASS | 0 | 356865 | 16384 | 7 | 0 | 2.05 | exhausted_bounded_graph |
| [MC_h1_stale](logs/MC_h1_stale.log) | PASS (développement) | 0 | 544621 | 30276 | 8 | 0 | 2.44 | exhausted_bounded_graph |
| [MC_h1_stale_checked](logs/MC_h1_stale_checked.log) | PASS | 0 | 544621 | 30276 | 8 | 0 | 2.49 | exhausted_bounded_graph |
| [MC_live_reconnection](logs/MC_live_reconnection.log) | PASS | 0 | 202959 | 6826 | 7 | 0 | 4.19 | exhausted_bounded_graph |
| [MC_min_general_k1](logs/MC_min_general_k1.log) | FAIL | 12 | 562997 | 112263 | 13 | 41537 | 109.37 | RegistryImmutable |
| [MC_min_general_k2](logs/MC_min_general_k2.log) | FAIL | 12 | 874892 | 172268 | 14 | 58655 | 223.73 | RegistryImmutable |
| [MC_mirror_off_00](logs/MC_mirror_off_00.log) | FAIL (développement) | 12 | 42274 | 9175 | 10 | 4403 | 1.66 | RegistryImmutable |
| [MC_mirror_off_01](logs/MC_mirror_off_01.log) | FAIL (développement) | 12 | 19367 | 4362 | 9 | 2186 | 1.23 | RegistryImmutable |
| [MC_mirror_off_10](logs/MC_mirror_off_10.log) | FAIL (développement) | 12 | 45329 | 10605 | 10 | 5519 | 1.71 | RegistryImmutable |
| [MC_mirror_off_11](logs/MC_mirror_off_11.log) | FAIL (développement) | 12 | 20290 | 4668 | 9 | 2385 | 1.24 | RegistryImmutable |
| [MC_mirror_on_00](logs/MC_mirror_on_00.log) | PASS (développement) | 0 | 2669720 | 365904 | 25 | 0 | 307.28 | exhausted_bounded_graph |
| [MC_mirror_on_01](logs/MC_mirror_on_01.log) | PASS (développement) | 0 | 1431628 | 193747 | 24 | 0 | 160.44 | exhausted_bounded_graph |
| [MC_mirror_on_10](logs/MC_mirror_on_10.log) | INCOMPLET (développement) | 143 | 4939203 | 720282 | 20 | 64896 (dernier point publié) | 570.14 | timeout |
| [MC_mirror_on_10_core](logs/MC_mirror_on_10_core.log) | INCOMPLET | 143 | 3457226 | 541514 | 19 | 77780 (dernier point publié) | 570.09 | timeout |
| [MC_mirror_on_11](logs/MC_mirror_on_11.log) | PASS (développement) | 0 | 2620872 | 357724 | 25 | 0 | 302.84 | exhausted_bounded_graph |
| [MC_mirror_on_11_core](logs/MC_mirror_on_11_core.log) | PASS | 0 | 1971321 | 278093 | 26 | 0 | 291.58 | exhausted_bounded_graph |
| [MC_money](logs/MC_money.log) | PASS (développement) | 0 | 9637 | 4128 | 35 | 0 | 0.6 | exhausted_bounded_graph |
| [MC_money_checked](logs/MC_money_checked.log) | PASS | 0 | 9637 | 4128 | 35 | 0 | 0.57 | exhausted_bounded_graph |
| [MC_mut_add](logs/MC_mut_add.log) | PASS (développement) | 0 | 960 | 960 | 1 | 0 | 0.59 | exhausted_bounded_graph |
| [MC_mut_add_checked](logs/MC_mut_add_checked.log) | FAIL | 12 | 964 | 964 | 2 | 956 | 0.52 | AddNoReset |
| [MC_mut_brake](logs/MC_mut_brake.log) | PASS (développement) | 0 | 10 | 10 | 10 | 0 | 0.9 | exhausted_bounded_graph |
| [MC_mut_brake_checked](logs/MC_mut_brake_checked.log) | FAIL | 12 | 11 | 11 | 11 | 0 | 1.17 | Mechanical |
| [MC_mut_forget_seal](logs/MC_mut_forget_seal.log) | FAIL (développement) | 12 | 22 | 20 | 3 | 12 | 0.52 | G0 |
| [MC_mut_forget_seal_checked](logs/MC_mut_forget_seal_checked.log) | FAIL | 12 | 22 | 20 | 3 | 12 | 0.54 | G0 |
| [MC_mut_free_anchor](logs/MC_mut_free_anchor.log) | PASS (développement) | 0 | 1911 | 242 | 7 | 0 | 0.58 | exhausted_bounded_graph |
| [MC_mut_free_anchor_checked](logs/MC_mut_free_anchor_checked.log) | FAIL | 12 | 4 | 4 | 2 | 0 | 0.53 | AnchorExact |
| [MC_mut_generation](logs/MC_mut_generation.log) | INCOMPLET (développement) | 75 | 21 | 15 | 3 | 10 | 0.53 | tool_or_model_error |
| [MC_mut_generation_checked](logs/MC_mut_generation_checked.log) | FAIL | 12 | 4739 | 1531 | 8 | 762 | 0.56 | S1 |
| [MC_mut_h1_adopted_only](logs/MC_mut_h1_adopted_only.log) | FAIL (développement) | 12 | 469 | 314 | 4 | 305 | 0.57 | H1NonVacuity |
| [MC_mut_h1_adopted_only_checked](logs/MC_mut_h1_adopted_only_checked.log) | FAIL | 12 | 469 | 314 | 4 | 305 | 0.59 | H1NonVacuity |
| [MC_mut_h1_anchor_deep](logs/MC_mut_h1_anchor_deep.log) | FAIL (développement) | 12 | 520 | 349 | 5 | 339 | 0.59 | H1Orientation |
| [MC_mut_h1_anchor_deep_checked](logs/MC_mut_h1_anchor_deep_checked.log) | FAIL | 12 | 552 | 380 | 4 | 370 | 0.64 | H1Orientation |
| [MC_mut_h1_maintain](logs/MC_mut_h1_maintain.log) | FAIL (développement) | 12 | 625 | 382 | 5 | 370 | 0.59 | NoContinuation |
| [MC_mut_h1_maintain_checked](logs/MC_mut_h1_maintain_checked.log) | FAIL | 12 | 625 | 382 | 5 | 370 | 0.6 | NoContinuation |
| [MC_mut_h1_promote](logs/MC_mut_h1_promote.log) | PASS (développement) | 0 | 423041 | 25600 | 8 | 0 | 2.38 | exhausted_bounded_graph |
| [MC_mut_h1_promote_checked](logs/MC_mut_h1_promote_checked.log) | FAIL | 12 | 344 | 237 | 4 | 229 | 0.59 | H1Subset |
| [MC_mut_import](logs/MC_mut_import.log) | PASS (développement) | 0 | 1193 | 558 | 21 | 0 | 0.54 | exhausted_bounded_graph |
| [MC_mut_import_checked](logs/MC_mut_import_checked.log) | FAIL | 12 | 211 | 125 | 8 | 45 | 0.53 | MON1 |
| [MC_mut_registry_lock](logs/MC_mut_registry_lock.log) | PASS (développement) | 0 | 24103 | 10609 | 5 | 0 | 0.85 | exhausted_bounded_graph |
| [MC_mut_registry_lock_checked](logs/MC_mut_registry_lock_checked.log) | FAIL | 12 | 68 | 66 | 4 | 58 | 0.52 | NoJournalVeto |
| [MC_mut_registry_no_threshold](logs/MC_mut_registry_no_threshold.log) | INCOMPLET (développement) | 75 | 1 | 1 | None | 1 | 0.53 | tool_or_model_error |
| [MC_mut_registry_no_threshold_checked](logs/MC_mut_registry_no_threshold_checked.log) | FAIL | 12 | 270 | 222 | 9 | 109 | 0.52 | ARule |
| [MC_mut_registry_tip](logs/MC_mut_registry_tip.log) | INCOMPLET (développement) | 75 | 1 | 1 | None | 1 | 0.54 | tool_or_model_error |
| [MC_mut_registry_tip_checked](logs/MC_mut_registry_tip_checked.log) | FAIL | 12 | 94 | 82 | 8 | 37 | 0.55 | ARule |
| [MC_persistence](logs/MC_persistence.log) | INCOMPLET (développement) | 75 | 21 | 15 | 3 | 10 | 0.52 | tool_or_model_error |
| [MC_persistence_checked](logs/MC_persistence_checked.log) | PASS | 0 | 11885 | 2204 | 13 | 0 | 0.57 | exhausted_bounded_graph |
| [MC_quota_ban](logs/MC_quota_ban.log) | PASS | 0 | 30 | 30 | 10 | 0 | 0.54 | exhausted_bounded_graph |
| [MC_registry_commits_C6](logs/MC_registry_commits_C6.log) | PASS (développement) | 0 | 79903 | 37249 | 5 | 0 | 1.18 | exhausted_bounded_graph |
| [MC_registry_commits_C6_checked](logs/MC_registry_commits_C6_checked.log) | PASS | 0 | 92353 | 43264 | 5 | 0 | 1.12 | exhausted_bounded_graph |
| [MC_registry_commits_CPreg](logs/MC_registry_commits_CPreg.log) | FAIL (développement) | 12 | 48 | 47 | 4 | 40 | 0.57 | CPreg |
| [MC_registry_commits_CPreg_checked](logs/MC_registry_commits_CPreg_checked.log) | FAIL | 12 | 49 | 48 | 4 | 41 | 0.53 | CPreg |
| [MC_registry_commits_RegistryImmutable](logs/MC_registry_commits_RegistryImmutable.log) | FAIL (développement) | 12 | 49 | 47 | 3 | 40 | 0.53 | RegistryImmutable |
| [MC_registry_commits_RegistryImmutable_checked](logs/MC_registry_commits_RegistryImmutable_checked.log) | FAIL | 12 | 49 | 48 | 4 | 41 | 0.51 | RegistryImmutable |
| [MC_registry_equivalence_1](logs/MC_registry_equivalence_1.log) | PASS | 0 | 8 | 4 | 1 | 0 | 0.64 | exhausted_bounded_graph |
| [MC_registry_equivalence_2](logs/MC_registry_equivalence_2.log) | PASS | 0 | 8 | 4 | 1 | 0 | 0.62 | exhausted_bounded_graph |
| [MC_registry_equivalence_4](logs/MC_registry_equivalence_4.log) | PASS | 0 | 8 | 4 | 1 | 0 | 0.65 | exhausted_bounded_graph |
| [MC_registry_window_1](logs/MC_registry_window_1.log) | INCOMPLET (développement) | 75 | 1 | 1 | None | 1 | 0.53 | tool_or_model_error |
| [MC_registry_window_1_checked](logs/MC_registry_window_1_checked.log) | PASS | 0 | 1889 | 1388 | 13 | 0 | 0.58 | exhausted_bounded_graph |
| [MC_registry_window_2](logs/MC_registry_window_2.log) | INCOMPLET (développement) | 75 | 1 | 1 | None | 1 | 0.53 | tool_or_model_error |
| [MC_registry_window_2_checked](logs/MC_registry_window_2_checked.log) | PASS | 0 | 1889 | 1388 | 13 | 0 | 0.58 | exhausted_bounded_graph |
| [MC_registry_window_4](logs/MC_registry_window_4.log) | INCOMPLET (développement) | 75 | 1 | 1 | None | 1 | 0.54 | tool_or_model_error |
| [MC_registry_window_4_checked](logs/MC_registry_window_4_checked.log) | PASS | 0 | 1889 | 1388 | 13 | 0 | 0.59 | exhausted_bounded_graph |
| [MC_replay_anchor_split](logs/MC_replay_anchor_split.log) | INCOMPLET (développement) | 75 | 2 | 1 | 1 | 0 | 0.54 | tool_or_model_error |
| [MC_replay_anchor_split_checked](logs/MC_replay_anchor_split_checked.log) | INCOMPLET (développement) | 75 | 2 | 1 | 1 | 0 | 0.54 | tool_or_model_error |
| [MC_replay_anchor_split_checked_fixed](logs/MC_replay_anchor_split_checked_fixed.log) | FAIL | 12 | 3 | 3 | 3 | 0 | 0.57 | A4 |
| [MC_replay_audit_c6](logs/MC_replay_audit_c6.log) | PASS | 0 | 15 | 13 | 13 | 0 | 0.62 | replay_completed |
| [MC_replay_audit_cp](logs/MC_replay_audit_cp.log) | FAIL | 12 | 13 | 12 | 12 | 0 | 0.62 | CPregGlobal |
| [MC_replay_audit_min_k1](logs/MC_replay_audit_min_k1.log) | FAIL | 12 | 11 | 11 | 11 | 0 | 0.64 | CPregGlobal |
| [MC_replay_closure](logs/MC_replay_closure.log) | INCOMPLET (développement) | 75 | 2 | 1 | 1 | 0 | 0.52 | tool_or_model_error |
| [MC_replay_closure_checked](logs/MC_replay_closure_checked.log) | INCOMPLET (développement) | 75 | 2 | 1 | 1 | 0 | 0.52 | tool_or_model_error |
| [MC_replay_closure_checked_fixed](logs/MC_replay_closure_checked_fixed.log) | FAIL | 12 | 3 | 3 | 3 | 0 | 0.51 | RegistryImmutable |
| [MC_replay_general_k1](logs/MC_replay_general_k1.log) | FAIL | 12 | 14 | 13 | 13 | 0 | 0.64 | RegistryImmutable |
| [MC_replay_general_k2](logs/MC_replay_general_k2.log) | FAIL | 12 | 15 | 14 | 14 | 0 | 0.65 | RegistryImmutable |
| [MC_replay_ruleA_advance](logs/MC_replay_ruleA_advance.log) | TÉMOIN | 12 | 22 | 18 | 18 | 0 | 0.68 | NoWitnessAdvance |
| [MC_replay_spec_adopt_off](logs/MC_replay_spec_adopt_off.log) | FAIL (développement) | 12 | 13 | 13 | 13 | 0 | 0.65 | RegistryImmutable |
| [MC_replay_spec_adopt_on](logs/MC_replay_spec_adopt_on.log) | PASS (développement) | 0 | 13 | 13 | 13 | 0 | 0.57 | replay_completed |
| [MC_replay_spec_off](logs/MC_replay_spec_off.log) | FAIL (développement) | 12 | 9 | 9 | 9 | 0 | 0.69 | RegistryImmutable |
| [MC_replay_spec_on](logs/MC_replay_spec_on.log) | PASS (développement) | 0 | 9 | 9 | 9 | 0 | 0.57 | replay_completed |
| [MC_scan_foreign](logs/MC_scan_foreign.log) | PASS | 0 | 8449 | 768 | 10 | 0 | 0.59 | exhausted_bounded_graph |
| [MC_scan_matching](logs/MC_scan_matching.log) | PASS | 0 | 8449 | 768 | 10 | 0 | 0.6 | exhausted_bounded_graph |
| [MC_scan_stale](logs/MC_scan_stale.log) | PASS | 0 | 8449 | 768 | 10 | 0 | 0.59 | exhausted_bounded_graph |
| [MC_scan_stale_counterexample](logs/MC_scan_stale_counterexample.log) | FAIL | 12 | 4503 | 621 | 7 | 209 | 0.58 | NoStaleVeto |
| [MC_support_equivalence_1](logs/MC_support_equivalence_1.log) | PASS | 0 | 8 | 4 | 1 | 0 | 0.64 | exhausted_bounded_graph |
| [MC_support_equivalence_2](logs/MC_support_equivalence_2.log) | PASS | 0 | 8 | 4 | 1 | 0 | 0.64 | exhausted_bounded_graph |
| [MC_support_equivalence_4](logs/MC_support_equivalence_4.log) | PASS | 0 | 8 | 4 | 1 | 0 | 0.63 | exhausted_bounded_graph |
| [MC_support_equivalence_4_off](logs/MC_support_equivalence_4_off.log) | PASS | 0 | 8 | 4 | 1 | 0 | 0.58 | exhausted_bounded_graph |
| [MC_tie_parent](logs/MC_tie_parent.log) | PASS | 0 | 59 | 20 | 5 | 0 | 0.54 | exhausted_bounded_graph |
| [MC_tie_reservations](logs/MC_tie_reservations.log) | FAIL | 12 | 57 | 20 | 5 | 0 | 0.54 | ReservationsConverge |
| [MC_v6_mirror_off_00](logs/MC_v6_mirror_off_00.log) | FAIL | 12 | 48162 | 10537 | 10 | 5098 | 1.84 | RegistryImmutable |
| [MC_v6_mirror_off_01](logs/MC_v6_mirror_off_01.log) | FAIL | 12 | 25475 | 5632 | 9 | 2768 | 1.24 | RegistryImmutable |
| [MC_v6_mirror_off_10](logs/MC_v6_mirror_off_10.log) | FAIL | 12 | 46770 | 10862 | 10 | 5612 | 1.73 | RegistryImmutable |
| [MC_v6_mirror_off_11](logs/MC_v6_mirror_off_11.log) | FAIL | 12 | 19942 | 4582 | 9 | 2338 | 1.08 | RegistryImmutable |
| [MC_v6_mirror_on_00](logs/MC_v6_mirror_on_00.log) | PASS | 0 | 1997645 | 280913 | 25 | 0 | 322.5 | exhausted_bounded_graph |
| [MC_v6_mirror_on_01](logs/MC_v6_mirror_on_01.log) | PASS | 0 | 1015556 | 141242 | 24 | 0 | 152.74 | exhausted_bounded_graph |
| [MC_v6_replay_spec_adopt_off](logs/MC_v6_replay_spec_adopt_off.log) | FAIL | 12 | 13 | 13 | 13 | 0 | 0.65 | RegistryImmutable |
| [MC_v6_replay_spec_adopt_on](logs/MC_v6_replay_spec_adopt_on.log) | PASS | 0 | 13 | 13 | 13 | 0 | 0.64 | replay_completed |
| [MC_v6_replay_spec_off](logs/MC_v6_replay_spec_off.log) | FAIL | 12 | 9 | 9 | 9 | 0 | 0.58 | RegistryImmutable |
| [MC_v6_replay_spec_on](logs/MC_v6_replay_spec_on.log) | PASS | 0 | 9 | 9 | 9 | 0 | 0.57 | replay_completed |
| [MC_witness_068_arithmetic](logs/MC_witness_068_arithmetic.log) | TÉMOIN | 12 | None | None | None | None | 0.53 | NoWitnessHealth |
| [MC_witness_bitcoin_slow](logs/MC_witness_bitcoin_slow.log) | TÉMOIN | 12 | 4 | 4 | 2 | 0 | 0.51 | NoWitnessSlowAnchor |
| [MC_witness_brake_068](logs/MC_witness_brake_068.log) | TÉMOIN (développement) | 12 | 14 | 14 | 14 | 0 | 11.42 | NoWitness068 |
| [MC_witness_brake_068_checked](logs/MC_witness_brake_068_checked.log) | TÉMOIN | 12 | 14 | 14 | 14 | 0 | 11.77 | NoWitness068 |
| [MC_witness_brake_Release](logs/MC_witness_brake_Release.log) | INCOMPLET (développement) | 75 | 14 | 13 | 13 | 1 | 7.16 | tool_or_model_error |
| [MC_witness_brake_Release_checked](logs/MC_witness_brake_Release_checked.log) | TÉMOIN | 12 | 18 | 18 | 18 | 0 | 46.69 | NoWitnessRelease |
| [MC_witness_brake_Slow](logs/MC_witness_brake_Slow.log) | INCOMPLET (développement) | 75 | 14 | 13 | 13 | 1 | 7.13 | tool_or_model_error |
| [MC_witness_brake_Slow_checked](logs/MC_witness_brake_Slow_checked.log) | TÉMOIN | 12 | 11 | 11 | 11 | 0 | 5.13 | NoWitnessSlow |
| [MC_witness_btc](logs/MC_witness_btc.log) | TÉMOIN (développement) | 12 | 402 | 168 | 4 | 123 | 0.59 | NoWitnessBTCStop |
| [MC_witness_btc_checked](logs/MC_witness_btc_checked.log) | TÉMOIN | 12 | 374 | 159 | 4 | 119 | 0.6 | NoWitnessBTCStop |
| [MC_witness_h1_CommonVeto](logs/MC_witness_h1_CommonVeto.log) | TÉMOIN (développement) | 12 | 13669 | 4649 | 6 | 4412 | 0.74 | NoWitnessCommonVeto |
| [MC_witness_h1_CommonVeto_checked](logs/MC_witness_h1_CommonVeto_checked.log) | TÉMOIN | 12 | 13657 | 4656 | 5 | 4420 | 0.75 | NoWitnessCommonVeto |
| [MC_witness_h1_Maintain](logs/MC_witness_h1_Maintain.log) | TÉMOIN (développement) | 12 | 625 | 382 | 5 | 370 | 0.59 | NoWitnessMaintain |
| [MC_witness_h1_Maintain_checked](logs/MC_witness_h1_Maintain_checked.log) | TÉMOIN | 12 | 625 | 382 | 5 | 370 | 0.59 | NoWitnessMaintain |
| [MC_witness_h1_Unknown](logs/MC_witness_h1_Unknown.log) | TÉMOIN (développement) | 12 | 197 | 136 | 4 | 128 | 0.53 | NoWitnessUnknown |
| [MC_witness_h1_Unknown_checked](logs/MC_witness_h1_Unknown_checked.log) | TÉMOIN | 12 | 197 | 136 | 4 | 128 | 0.52 | NoWitnessUnknown |
| [MC_witness_h1_rank](logs/MC_witness_h1_rank.log) | TÉMOIN | 12 | 67 | 12 | 4 | 0 | 0.53 | NoWitnessRankExit |
| [MC_witness_mirror_advance](logs/MC_witness_mirror_advance.log) | TÉMOIN | 12 | 1247432 | 245876 | 15 | 79814 | 104.22 | NoWitnessMirror |
| [MC_witness_mirror_empty](logs/MC_witness_mirror_empty.log) | TÉMOIN | 12 | 79013 | 16927 | 9 | 7807 | 2.49 | NoWitnessMirror |
| [MC_witness_money](logs/MC_witness_money.log) | TÉMOIN (développement) | 12 | 8805 | 3833 | 27 | 118 | 0.59 | NoWitnessMoney |
| [MC_witness_money_checked](logs/MC_witness_money_checked.log) | TÉMOIN | 12 | 8820 | 3847 | 27 | 125 | 0.57 | NoWitnessMoney |
| [MC_witness_persistence](logs/MC_witness_persistence.log) | INCOMPLET (développement) | 75 | 21 | 15 | 3 | 10 | 0.54 | tool_or_model_error |
| [MC_witness_persistence_checked](logs/MC_witness_persistence_checked.log) | TÉMOIN | 12 | 2829 | 816 | 8 | 371 | 0.57 | NoWitnessCrash |
| [MC_witness_quota_ban](logs/MC_witness_quota_ban.log) | TÉMOIN | 12 | 23 | 23 | 10 | 1 | 0.55 | NoWitnessProspective |
| [MC_witness_react](logs/MC_witness_react.log) | TÉMOIN (développement) | 12 | 2531 | 2531 | 3 | 956 | 0.6 | NoWitnessReact |
| [MC_witness_react_checked](logs/MC_witness_react_checked.log) | TÉMOIN | 12 | 3138 | 3138 | 3 | 1563 | 0.59 | NoWitnessReact |
| [MC_witness_react_late_price](logs/MC_witness_react_late_price.log) | TÉMOIN | 12 | 5064 | 5064 | 4 | 1916 | 0.58 | NoWitnessLatePrice |
| [MC_witness_recovery](logs/MC_witness_recovery.log) | TÉMOIN (développement) | 12 | 304 | 162 | 4 | 70 | 0.54 | NoWitnessRecovery |
| [MC_witness_recovery_checked](logs/MC_witness_recovery_checked.log) | TÉMOIN | 12 | 256 | 163 | 4 | 71 | 0.52 | NoWitnessRecovery |
| [MC_witness_registry_Above](logs/MC_witness_registry_Above.log) | INCOMPLET (développement) | 75 | 269 | 159 | 9 | 82 | 0.54 | tool_or_model_error |
| [MC_witness_registry_Above_checked](logs/MC_witness_registry_Above_checked.log) | TÉMOIN | 12 | 479 | 386 | 10 | 189 | 0.54 | NoWitnessAbove |
| [MC_witness_registry_Below](logs/MC_witness_registry_Below.log) | INCOMPLET (développement) | 75 | 290 | 171 | 10 | 87 | 0.54 | tool_or_model_error |
| [MC_witness_registry_Below_checked](logs/MC_witness_registry_Below_checked.log) | TÉMOIN | 12 | 234 | 198 | 9 | 100 | 0.55 | NoWitnessBelow |
| [MC_witness_registry_Empty](logs/MC_witness_registry_Empty.log) | INCOMPLET (développement) | 75 | 280 | 164 | 8 | 84 | 0.53 | tool_or_model_error |
| [MC_witness_registry_Empty_checked](logs/MC_witness_registry_Empty_checked.log) | TÉMOIN | 12 | 207 | 173 | 9 | 83 | 0.54 | NoWitnessEmpty |
| [MC_witness_registry_Reject](logs/MC_witness_registry_Reject.log) | INCOMPLET (développement) | 75 | 327 | 190 | 9 | 97 | 0.54 | tool_or_model_error |
| [MC_witness_registry_Reject_checked](logs/MC_witness_registry_Reject_checked.log) | TÉMOIN | 12 | 330 | 270 | 9 | 130 | 0.54 | NoWitnessReject |
| [MC_witness_registry_Threshold](logs/MC_witness_registry_Threshold.log) | INCOMPLET (développement) | 75 | 236 | 138 | 8 | 70 | 0.62 | tool_or_model_error |
| [MC_witness_registry_Threshold_checked](logs/MC_witness_registry_Threshold_checked.log) | TÉMOIN | 12 | 311 | 253 | 9 | 123 | 0.54 | NoWitnessThreshold |
| [MC_witness_registry_late](logs/MC_witness_registry_late.log) | TÉMOIN | 12 | 434 | 353 | 10 | 175 | 0.57 | NoWitnessLate |
| [MC_witness_scan_Decidable](logs/MC_witness_scan_Decidable.log) | TÉMOIN | 12 | 4899 | 648 | 7 | 200 | 0.61 | NoWitnessDecidable |
| [MC_witness_scan_Unknown](logs/MC_witness_scan_Unknown.log) | TÉMOIN | 12 | 33 | 23 | 3 | 15 | 0.53 | NoWitnessUnknown |
| [MC_witness_seal_only](logs/MC_witness_seal_only.log) | TÉMOIN (développement) | 12 | 58 | 45 | 3 | 37 | 0.59 | NoWitnessSealOnly |
| [MC_witness_seal_only_checked](logs/MC_witness_seal_only_checked.log) | TÉMOIN | 12 | 152 | 85 | 3 | 67 | 0.58 | NoWitnessSealOnly |
