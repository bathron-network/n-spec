| Sonde | Statut | États distincts | Durée (s) |
|---|---|---:|---:|
| `MC_replay_general_k1_L1` | PASS | 13 | 0.75 |
| `MC_replay_general_k2_L1` | PASS | 14 | 0.65 |
| `MC_replay_ruleA_advance_L1` | PASS | 18 | 0.65 |
| `MC_replay_audit_cp_L1` | TÉMOIN | 12 | 0.64 |
| `MC_replay_audit_min_k1_L1` | TÉMOIN | 11 | 0.62 |
| `MC_replay_closure_checked_fixed_L1` | TÉMOIN | 3 | 0.56 |
| `MC_registry_commits_C6_checked_L1` | PASS | 43264 | 1.18 |
| `MC_fast_off_00_L1` | PASS | 402099 | 358.18 |
| `MC_fast_on_00_L1` | PASS | 280913 | 348.32 |
| `MC_c6_k1_00_L1` | PASS | 134506 | 131.59 |
| `MC_general_a_k1_c6_L1` | INCOMPLET | 693034 | 569.23 |
| `MC_private_return_L1` | TÉMOIN | 15 | 0.71 |

Les PASS des replays sont limités au chemin fixé. Les explorations interrompues restent INCOMPLET, indépendamment des invariants non violés jusque-là. Pour INCOMPLET, les compteurs proviennent du dernier relevé TLC disponible. La première tentative interrompue est conservée en plus de ce tableau.
