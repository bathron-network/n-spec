# Traces et témoins lisibles

Les traces brutes gardent tous les champs et les actions TLC. Les états du tableau comptent les états imprimés de la trace, et non la taille du graphe exploré. Un témoin est un échec volontaire de NoWitness…, distinct d’un invariant normatif. Les premiers essais de développement sont exclus de cet index, mais conservés sur disque.

| Campagne | Statut | Propriété | États de trace | Lecture brute |
|---|---|---|---:|---|
| MC_anchor_agreement_checked | FAIL | A4 | 3 | [trace](traces/MC_anchor_agreement_checked.txt) |
| MC_audit_cp_k1 | FAIL | CPregGlobal | 11 | [trace](traces/MC_audit_cp_k1.txt) |
| MC_audit_cp_k2 | FAIL | CPregGlobal | 12 | [trace](traces/MC_audit_cp_k2.txt) |
| MC_fast_off_00 | FAIL | RegistryImmutable | 10 | [trace](traces/MC_fast_off_00.txt) |
| MC_fast_off_01 | FAIL | RegistryImmutable | 9 | [trace](traces/MC_fast_off_01.txt) |
| MC_fast_off_10 | FAIL | RegistryImmutable | 10 | [trace](traces/MC_fast_off_10.txt) |
| MC_fast_off_11 | FAIL | RegistryImmutable | 9 | [trace](traces/MC_fast_off_11.txt) |
| MC_general_a_k1_strong | FAIL | RegistryImmutable | 13 | [trace](traces/MC_general_a_k1_strong.txt) |
| MC_general_a_k2_strong | FAIL | RegistryImmutable | 14 | [trace](traces/MC_general_a_k2_strong.txt) |
| MC_min_general_k1 | FAIL | RegistryImmutable | 13 | [trace](traces/MC_min_general_k1.txt) |
| MC_min_general_k2 | FAIL | RegistryImmutable | 14 | [trace](traces/MC_min_general_k2.txt) |
| MC_mut_add_checked | FAIL | AddNoReset | 2 | [trace](traces/MC_mut_add_checked.txt) |
| MC_mut_brake_checked | FAIL | Mechanical | 11 | [trace](traces/MC_mut_brake_checked.txt) |
| MC_mut_forget_seal_checked | FAIL | G0 | 2 | [trace](traces/MC_mut_forget_seal_checked.txt) |
| MC_mut_free_anchor_checked | FAIL | AnchorExact | 2 | [trace](traces/MC_mut_free_anchor_checked.txt) |
| MC_mut_generation_checked | FAIL | S1 | 8 | [trace](traces/MC_mut_generation_checked.txt) |
| MC_mut_h1_adopted_only_checked | FAIL | H1NonVacuity | 4 | [trace](traces/MC_mut_h1_adopted_only_checked.txt) |
| MC_mut_h1_anchor_deep_checked | FAIL | H1Orientation | 4 | [trace](traces/MC_mut_h1_anchor_deep_checked.txt) |
| MC_mut_h1_maintain_checked | FAIL | NoContinuation | 5 | [trace](traces/MC_mut_h1_maintain_checked.txt) |
| MC_mut_h1_promote_checked | FAIL | H1Subset | 4 | [trace](traces/MC_mut_h1_promote_checked.txt) |
| MC_mut_import_checked | FAIL | MON1 | 6 | [trace](traces/MC_mut_import_checked.txt) |
| MC_mut_registry_lock_checked | FAIL | NoJournalVeto | 3 | [trace](traces/MC_mut_registry_lock_checked.txt) |
| MC_mut_registry_no_threshold_checked | FAIL | ARule | 7 | [trace](traces/MC_mut_registry_no_threshold_checked.txt) |
| MC_mut_registry_tip_checked | FAIL | ARule | 6 | [trace](traces/MC_mut_registry_tip_checked.txt) |
| MC_registry_commits_CPreg_checked | FAIL | CPreg | 4 | [trace](traces/MC_registry_commits_CPreg_checked.txt) |
| MC_registry_commits_RegistryImmutable_checked | FAIL | RegistryImmutable | 4 | [trace](traces/MC_registry_commits_RegistryImmutable_checked.txt) |
| MC_replay_anchor_split_checked_fixed | FAIL | A4 | 3 | [trace](traces/MC_replay_anchor_split_checked_fixed.txt) |
| MC_replay_audit_cp | FAIL | CPregGlobal | 12 | [trace](traces/MC_replay_audit_cp.txt) |
| MC_replay_audit_min_k1 | FAIL | CPregGlobal | 11 | [trace](traces/MC_replay_audit_min_k1.txt) |
| MC_replay_closure_checked_fixed | FAIL | RegistryImmutable | 3 | [trace](traces/MC_replay_closure_checked_fixed.txt) |
| MC_replay_general_k1 | FAIL | RegistryImmutable | 13 | [trace](traces/MC_replay_general_k1.txt) |
| MC_replay_general_k2 | FAIL | RegistryImmutable | 14 | [trace](traces/MC_replay_general_k2.txt) |
| MC_replay_ruleA_advance | TÉMOIN | NoWitnessAdvance | 18 | [trace](traces/MC_replay_ruleA_advance.txt) |
| MC_scan_stale_counterexample | FAIL | NoStaleVeto | 7 | [trace](traces/MC_scan_stale_counterexample.txt) |
| MC_tie_reservations | FAIL | ReservationsConverge | 5 | [trace](traces/MC_tie_reservations.txt) |
| MC_v6_mirror_off_00 | FAIL | RegistryImmutable | 10 | [trace](traces/MC_v6_mirror_off_00.txt) |
| MC_v6_mirror_off_01 | FAIL | RegistryImmutable | 9 | [trace](traces/MC_v6_mirror_off_01.txt) |
| MC_v6_mirror_off_10 | FAIL | RegistryImmutable | 10 | [trace](traces/MC_v6_mirror_off_10.txt) |
| MC_v6_mirror_off_11 | FAIL | RegistryImmutable | 9 | [trace](traces/MC_v6_mirror_off_11.txt) |
| MC_v6_replay_spec_adopt_off | FAIL | RegistryImmutable | 13 | [trace](traces/MC_v6_replay_spec_adopt_off.txt) |
| MC_v6_replay_spec_off | FAIL | RegistryImmutable | 9 | [trace](traces/MC_v6_replay_spec_off.txt) |
| MC_witness_068_arithmetic | TÉMOIN | NoWitnessHealth | NP (initial) | [trace](traces/MC_witness_068_arithmetic.txt) |
| MC_witness_bitcoin_slow | TÉMOIN | NoWitnessSlowAnchor | 2 | [trace](traces/MC_witness_bitcoin_slow.txt) |
| MC_witness_brake_068_checked | TÉMOIN | NoWitness068 | 14 | [trace](traces/MC_witness_brake_068_checked.txt) |
| MC_witness_brake_Release_checked | TÉMOIN | NoWitnessRelease | 18 | [trace](traces/MC_witness_brake_Release_checked.txt) |
| MC_witness_brake_Slow_checked | TÉMOIN | NoWitnessSlow | 11 | [trace](traces/MC_witness_brake_Slow_checked.txt) |
| MC_witness_btc_checked | TÉMOIN | NoWitnessBTCStop | 4 | [trace](traces/MC_witness_btc_checked.txt) |
| MC_witness_h1_CommonVeto_checked | TÉMOIN | NoWitnessCommonVeto | 5 | [trace](traces/MC_witness_h1_CommonVeto_checked.txt) |
| MC_witness_h1_Maintain_checked | TÉMOIN | NoWitnessMaintain | 4 | [trace](traces/MC_witness_h1_Maintain_checked.txt) |
| MC_witness_h1_Unknown_checked | TÉMOIN | NoWitnessUnknown | 4 | [trace](traces/MC_witness_h1_Unknown_checked.txt) |
| MC_witness_h1_rank | TÉMOIN | NoWitnessRankExit | 2 | [trace](traces/MC_witness_h1_rank.txt) |
| MC_witness_mirror_advance | TÉMOIN | NoWitnessMirror | 15 | [trace](traces/MC_witness_mirror_advance.txt) |
| MC_witness_mirror_empty | TÉMOIN | NoWitnessMirror | 9 | [trace](traces/MC_witness_mirror_empty.txt) |
| MC_witness_money_checked | TÉMOIN | NoWitnessMoney | 27 | [trace](traces/MC_witness_money_checked.txt) |
| MC_witness_persistence_checked | TÉMOIN | NoWitnessCrash | 7 | [trace](traces/MC_witness_persistence_checked.txt) |
| MC_witness_quota_ban | TÉMOIN | NoWitnessProspective | 3 | [trace](traces/MC_witness_quota_ban.txt) |
| MC_witness_react_checked | TÉMOIN | NoWitnessReact | 3 | [trace](traces/MC_witness_react_checked.txt) |
| MC_witness_react_late_price | TÉMOIN | NoWitnessLatePrice | 4 | [trace](traces/MC_witness_react_late_price.txt) |
| MC_witness_recovery_checked | TÉMOIN | NoWitnessRecovery | 4 | [trace](traces/MC_witness_recovery_checked.txt) |
| MC_witness_registry_Above_checked | TÉMOIN | NoWitnessAbove | 9 | [trace](traces/MC_witness_registry_Above_checked.txt) |
| MC_witness_registry_Below_checked | TÉMOIN | NoWitnessBelow | 7 | [trace](traces/MC_witness_registry_Below_checked.txt) |
| MC_witness_registry_Empty_checked | TÉMOIN | NoWitnessEmpty | 7 | [trace](traces/MC_witness_registry_Empty_checked.txt) |
| MC_witness_registry_Reject_checked | TÉMOIN | NoWitnessReject | 8 | [trace](traces/MC_witness_registry_Reject_checked.txt) |
| MC_witness_registry_Threshold_checked | TÉMOIN | NoWitnessThreshold | 8 | [trace](traces/MC_witness_registry_Threshold_checked.txt) |
| MC_witness_registry_late | TÉMOIN | NoWitnessLate | 8 | [trace](traces/MC_witness_registry_late.txt) |
| MC_witness_scan_Decidable | TÉMOIN | NoWitnessDecidable | 7 | [trace](traces/MC_witness_scan_Decidable.txt) |
| MC_witness_scan_Unknown | TÉMOIN | NoWitnessUnknown | 3 | [trace](traces/MC_witness_scan_Unknown.txt) |
| MC_witness_seal_only_checked | TÉMOIN | NoWitnessSealOnly | 3 | [trace](traces/MC_witness_seal_only_checked.txt) |

## Parcours des contre-exemples de production A active

Les numéros de ligne d’action dans la trace renvoient aux sources livrées. Les registres et préfixes complets sont conservés dans chaque état brut.

### MC_replay_general_k1

| État | Action | Slot |
|---:|---|---:|
| 1 | Initial predicate | 0 |
| 2 | ReplayNext | 0 |
| 3 | ReplayNext | 1 |
| 4 | ReplayNext | 2 |
| 5 | ReplayNext | 3 |
| 6 | ReplayNext | 4 |
| 7 | ReplayNext | 4 |
| 8 | ReplayNext | 4 |
| 9 | ReplayNext | 4 |
| 10 | ReplayNext | 4 |
| 11 | ReplayNext | 4 |
| 12 | ReplayNext | 4 |
| 13 | ReplayNext | 4 |

### MC_replay_general_k2

| État | Action | Slot |
|---:|---|---:|
| 1 | Initial predicate | 0 |
| 2 | ReplayNext | 0 |
| 3 | ReplayNext | 1 |
| 4 | ReplayNext | 2 |
| 5 | ReplayNext | 3 |
| 6 | ReplayNext | 3 |
| 7 | ReplayNext | 3 |
| 8 | ReplayNext | 4 |
| 9 | ReplayNext | 4 |
| 10 | ReplayNext | 4 |
| 11 | ReplayNext | 4 |
| 12 | ReplayNext | 4 |
| 13 | ReplayNext | 4 |
| 14 | ReplayNext | 4 |

### MC_min_general_k1

| État | Action | Slot |
|---:|---|---:|
| 1 | Initial predicate | 0 |
| 2 | Produce | 0 |
| 3 | Tick | 1 |
| 4 | Tick | 2 |
| 5 | Tick | 3 |
| 6 | Tick | 4 |
| 7 | Reveal | 4 |
| 8 | Produce | 4 |
| 9 | Heal | 4 |
| 10 | Return | 4 |
| 11 | Fetch | 4 |
| 12 | Produce | 4 |
| 13 | Fetch | 4 |

### MC_min_general_k2

| État | Action | Slot |
|---:|---|---:|
| 1 | Initial predicate | 0 |
| 2 | Produce | 0 |
| 3 | Tick | 1 |
| 4 | Tick | 2 |
| 5 | Tick | 3 |
| 6 | Reveal | 3 |
| 7 | Heal | 3 |
| 8 | Return | 3 |
| 9 | Fetch | 3 |
| 10 | Produce | 3 |
| 11 | Tick | 4 |
| 12 | Produce | 4 |
| 13 | Produce | 4 |
| 14 | Fetch | 4 |

### MC_replay_audit_cp

| État | Action | Slot |
|---:|---|---:|
| 1 | Initial predicate | 0 |
| 2 | Action | 0 |
| 3 | Action | 1 |
| 4 | Action | 2 |
| 5 | Action | 3 |
| 6 | Action | 4 |
| 7 | Action | 4 |
| 8 | Action | 4 |
| 9 | Action | 4 |
| 10 | Action | 4 |
| 11 | Action | 4 |
| 12 | Action | 4 |

### MC_replay_audit_min_k1

| État | Action | Slot |
|---:|---|---:|
| 1 | Initial predicate | 0 |
| 2 | Action | 0 |
| 3 | Action | 1 |
| 4 | Action | 2 |
| 5 | Action | 3 |
| 6 | Action | 4 |
| 7 | Action | 4 |
| 8 | Action | 4 |
| 9 | Action | 4 |
| 10 | Action | 4 |
| 11 | Action | 4 |
