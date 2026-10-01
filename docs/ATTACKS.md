# Attacks and counterexamples: the falsification history of N

**Architecture frozen candidate. Not mainnet-qualified. Not production-ready.**

This document lists the attacks, counterexamples and failed claims that shaped N, from the engine candidates that came before it up to N-SPEC v0.7. Every row comes from a dated study, a model-checking campaign, a numerical derivation, a network bench or a blind review. For the rationale, see **WHY-N.md**. A French version is in `ATTACKS.fr.md`.

## Legend

**Method**
- **TLA+**: bounded model checking with TLC. Every result is bounded and is not a deductive proof.
- **Monte-Carlo**: strategic simulation.
- **Analysis**: an analytic argument or exact dynamic programming (DP), usually produced by two independent analyses and then confronted.
- **Bench**: network measurement on real links, or emulation (netem) on real links.
- **Blind review**: reviewers who were given only the specification text, with no project context.

**Status**
- **REAL FAIL**: the counterexample is reachable under the rules as written, with no mutation. Marked "(analytic)" when it was established by argument rather than by a model checker.
- **MUTATION FAIL**: a deliberately broken variant is caught by the monitor. This is the expected result: it shows the check is sensitive.
- **WITNESS**: a targeted situation is shown to be reachable.
- **BOUNDED PASS**: no violation was found within the stated bounds.
- **INCOMPLETE**: the exploration was interrupted. An INCOMPLETE result is never counted as a PASS.

Rows from N v0.5 onward can be checked against this repository (`spec/`, `formal/`, `analysis/`, `bench/`, `qualification/`). Rows about earlier engine candidates (§1) and early N versions summarise research studies and blind reviews that are not published here.

---

## 1. Engine candidates before N

| Candidate | Attack / counterexample | Method | Status | Fix or decision | Non-regression test |
|---|---|---|---|---|---|
| C (sequencer + ticket quorum) | Safety under equivocation, withholding, broken thresholds or locks | TLA+ (adapted from a published Tendermint model): N=4/F=1/q=3 exhaustive, 28.7 M states; N=7 and N=6 partial | BOUNDED PASS for safety; every deliberately broken variant caught. Liveness: latency issue when q = N−F−U exactly | C is not discarded for safety reasons | Broken variants: threshold too low, no lock, locks erased |
| C | "The burn guarantees β" | Analysis (two independent kill-tests) | REAL FAIL (analytic): a burn bounds neither concentration, key rental, corruption, coercion nor attrition; two honest departures are enough to cross the forging threshold if F tracks N | β becomes a published assumption, never a promise. Later: C archived, pure N chosen | — |
| Quorumless finality (producer + deterministic Core + halt on ambiguity) | Silence is not a detectable ambiguity; Bitcoin does not contain the roots | Analysis (two kill-tests) | REAL FAIL (analytic) | Firm finality needs a quorum, Bitcoin writes or synchrony | — |
| D (finality by convergence) | An equivocating owner plus a partition yields two incompatible "finalities" | Analysis (two kill-tests) | REAL FAIL (analytic): "D without a quorum killed" | D dropped. Retained at no cost: typing of owned vs shared transactions | — |
| D3 (single lineage, Bitcoin read-only) | For any local rule, P[double lineage] ≥ 2·(liveness of an honest payment) − 1 | Analysis | REAL FAIL (analytic) for free payments | Only the one-hop swap object and clock automata survive | — |
| E / F (sampled certificates) | Committee sizes: ≈200 at β=0.1, 1,300–2,600 at β=0.2, impossible at β=0.3; a public committee falls to ≈50 targeted corruptions | Analysis | REAL FAIL (analytic) for F; E deferred | Deferred | — |
| E2 (faithful SBRB/DPRB) | 27–252 Mbit/s per node at 32 tx/s against ≈5 for C; probabilistic safety under a static adversary; no exportable proof | Analysis of the primary papers (two analyses) | REAL FAIL (analytic) against the owner's rule ("if E2 stays more expensive or less safe, close E") | **E closed.** Recovered: per-account parallel execution, validity by (source, seq), freezing of the equivocator | — |
| Bitcoin barrier (synchronous BFT clocked by Bitcoin) | Two tickets plus a partition longer than 2Δ produce two silent FINALs, whatever N is (DLS 1988 bound) | Analysis | REAL FAIL (analytic) | Killed as a finality engine | — |
| Two stages (mechanical chain + C checkpoints) | No gain on β; a public calendar allows on-demand reorgs; a Bitcoin reorg beyond k_seed also halts | Analysis | Deferred | Not adopted | — |
| NC (C finality per object) | Per-object finality propagates in depth, upstream (causal cone) and to new nodes | Analysis | REAL FAIL (analytic) | Pure N at genesis | — |
| N itself (early candidate) | Free, repeatable, non-faulting reorg attempts; reorgs targeted through the public calendar (β=0.2, τ=6 s: depth 6 about every 5.4 days); the minority side erased in a partition; no exportable proof | Analysis | REAL (analytic), accepted as a stated limit | The owner drops firm finality. Vocabulary becomes inclusion → depth → stability; depth policy and exposure caps belong to the SP/LP | K(ε) table (§17.3) |

## 2. Long range and H1

| Version | Attack / counterexample | Method | Status | Fix or decision | Non-regression test |
|---|---|---|---|---|---|
| Long-range study (N v0.1 era) | The object graph alone proves provenance, not date; with stolen keys, a fake chain reaches 100 % density | Analysis | REAL FAIL (analytic) | Rejected as a long-range defence | — |
| Same | "First anchored wins": a live attacker anchors faster than a passive network and splits new nodes from the network for 0.01 BTC | Analysis | REAL FAIL (analytic) | Rejected | — |
| Same | "Density after divergence" elects the twin or the attacker | Analysis | REAL FAIL (analytic) | Discarded. Replaced by disqualification through proven progress (negative temporal proof, never fork-choice) | — |
| v0.2.1 | The temporal filter turned against a new node: a cheap fingerprinted adversarial branch is adopted during an honest drought | Blind review | REAL FAIL (analytic) | v0.3: the witness must also lead in score; never adoption by the filter alone | — |
| v0.4 | A filter that requires a better score can only eliminate a branch that is already beaten, so it is a detector, not a selection rule | Blind review (two of three reviewers) | Finding | Owner decision: **H1 = detector**. A Bitcoin anteriority proof may shrink the safe set or trigger STOP, never promote | `H1Detector`, `H1Subset` monitors |
| v0.5 | The H1 veto is almost inert for a new node, and the outcome depends on **arrival order** (C first ⇒ adopted without H1; W first ⇒ deep halt) | Blind review | REAL FAIL (analytic) | v0.6: oriented veto pairs (C ∈ maxima, W ∈ validated deep branches) with a complete witness, re-evaluated even after adoption | TLA+ `H1OrdersChecked`: all permutations of six events, **9/9 BOUNDED PASS** |
| v0.5 | Mutation "H1 promoter": an alert re-adopts the losing branch | TLA+ | MUTATION FAIL (11 states) | — | `MC_replay_h1`; v0.6 mutations "H1 promote", "H1 limited to adopted", "MAINTAIN skips H1", "Deep depends on local anchor": all caught |
| v0.6 | Fingerprint frequency alone does not bound the freshness of proven progress (stale references) | TLA+ | REAL FAIL (bounded counterexample) | Published. N-SPEC §18: H1 is not complete long-range protection | `MC_scan_stale_counterexample` |

## 3. Registry and common prefix

| Version | Attack / counterexample | Method | Status | Fix or decision | Non-regression test |
|---|---|---|---|---|---|
| v0.3 | **Local registry locks** (persisted at the cut, never replaced): two honest nodes lock different registries after a one-block divergence near the cut (exploitable by an adversarial producer); an absence crossing a cut ⇒ HALTED; a BOOTSTRAP older than about one epoch is unusable; permanent block after a low-density epoch | Blind review of v0.4 (three reviewers, common root cause) | REAL FAIL (analytic) | v0.5: locks removed; the registry is a deterministic function of an old snapshot of the candidate chain (stable prefix, Ouroboros-style) | v0.6 mutation "committed registry used as veto" caught (`NoJournalVeto`) |
| v0.5 | **Registry reorg**: the snapshot is dated in slots, reorg protection in blocks. A withheld block A₀ with an ADD, empty slots, then adoption ⇒ two registries in the same epoch and context, with no mutation | TLA+ (`MC_spec_registryreorg`, 9-state trace); confirmed by three blind reviewers who had not seen the model | **REAL FAIL** (no mutation); bounded `MC_safe` PASS (93,112 states) did not cover it | Owner decision **D + A**: C6 conditional stability stated exactly; CP_reg as a separate obligation; rule A: `A_e` advances only if the branch has ≥ maxreorg blocks in the snapshot window, otherwise inherited. No lock | `MC_v6_replay_spec_{off,on}`, `..._adopt_{off,on}` (9 and 13 states) |
| v0.6 | **A off ⇒ RegistryImmutable FAIL** | TLA+, four Bitcoin vectors | A off: **FAIL 4/4** + 2 replays. A on: **BOUNDED PASS 4/4** (exhaustive within the model bounds, abstract constants), 1,331,054 distinct states (one vector finished on an uncapped re-run) | Rule A retained | `MC_fast_off_*` / `MC_fast_on_*`; C6 8/8 BOUNDED PASS; 13/13 mutations caught |
| v0.5 | Mutation "snapshot taken on the tip" | TLA+ | MUTATION FAIL (7 states) | — | `MC_replay_tip`; v0.6 "snapshot on tip", "rule A threshold removed" caught |
| v0.6, A on | **Withheld B₀**: B₀ carries an ADD and is withheld; at slot 4 two honest nodes sign under (2,1,1) and (2,2,1). Two registries in the same epoch and context with **zero disconnections**, so no deep halt is expected | TLA+ (`MC_replay_general_k1/k2`, audit log `MC_audit_cp_k1/k2` in 11–12 states) | **REAL FAIL** of strong immutability and of CP_reg without a network domain; C6 PASS on the same trace | CP_reg made a separate obligation to be analysed under a published domain (no new mechanism) | Same replays; `MC_replay_audit_c6` PASS |
| v0.6 | Incompatible anchors after separate deliveries (A4) | TLA+ (`MC_anchor_agreement_checked`) | REAL FAIL (bounded, no network domain) | Open: the missing assumption is a network bound on construction and delivery | **QR-9** |
| v0.6 | Data convergence does not erase earlier diverging signature reservations | TLA+ (`MC_tie_reservations`) | REAL FAIL (bounded) | Published; no mechanism change | Same configuration |
| v0.6 | Rule A is steerable near d ≈ 0.2 (g·W < b ≤ (g+β)·W) | Analysis (DP) + executable trace (2 disconnections) + Monte-Carlo (0.32 % at β=0.20, d=0.20, K=512; 16 M repetitions) | REAL FAIL in that zone | Zone excluded by the published domain (d ≥ 0.70) | K(ε) table, `d-min` table |
| v0.6 | Old §15 depth k = 77 (no-lead model) underestimates risk by 8 to 10 orders of magnitude under public calendar + withholding + equivocation | Analysis (two independent methods) + blind review of v0.5 | REAL FAIL (analytic) of the earlier claim | k = 77 kept as a laboratory value with no risk bound; DP table K(ε) published; equivocation counted as one unit of progress per branch | Equivocation rule checked in three codes |
| v0.6 | **CP_reg and the changing calendar** (first-divergence lemma L1). L1 and L2 hold, but "the whole race is played under a common calendar" is false: a private branch that forks before the cut, is behind at epoch start, then switches registry and calendar and catches up | Analysis E1 (pre-snapshot content composed after seeing the seed, rotating keys ⇒ many selectable calendars) + TLA+ witness `MC_private_return_L1` (15 states; two signatures at slot 4 under different registries) | WITNESS / REAL FAIL (analytic) of the bound; ε_U UNKNOWN | Synchronised nodes are covered by maxreorg (halt). New or returning nodes declared **out of the CP_reg domain** (D1, weak subjectivity, return via a recent A′/RELEASE origin) | `MC_private_return_L1`; 12 TLA+ probes, `NoOtherStructural` never violated |
| v0.6 → v0.7 | **Deep pivot**: a private branch closes its window early, below the threshold, by **antedating a maturity carrier inside the MTP margin** [MatMin, BtcMat), inherits the registry, then takes the lead. A synchronised node adopts it after 2–3 disconnections, below maxreorg | TLA+ (dedicated mirror): 2 directed replays, 1 semi-directed exploration, 1 restricted exploration; contrast run gives STOP | **WITNESS ×4**; strict full exploration **INCOMPLETE** (5.2 M states) | No new mechanism. Covered in probability by the term `T_profond` when (K_reg, b) are derived together. An earlier optimistic estimate of the pivot depth was corrected (fluctuation tail, lead and union over fork positions) | `MC_replay_{sync,aftersig,stop,shallow}_PivotDeep`; **QR-4** |
| v0.7 | Residual band of ≈370 slots (≈1 h) at the MTP floor where arithmetic does not force STOP for an antedated *installation* | Analysis (coherence check) | Explained; bounded in probability by `T_profond` ≈ 1.95·10⁻¹³ per epoch | Probabilistic coverage accepted as the derived dimensioning | **QR-6** (composition proof) |

## 4. Liveness, network and parameters

| Version | Attack / counterexample | Method | Status | Fix or decision | Non-regression test |
|---|---|---|---|---|---|
| v0 | Taking the Bitcoin reference at the tip makes N reorganise on every Bitcoin orphan (≈100 N blocks lost) and splits N during Bitcoin races | Blind review | REAL FAIL (analytic) | v0.1: Bitcoin reference buried at `d_ref` = 6, bounded progression | — |
| v0 | Tie-break on block id is grindable ⇒ adversary wins every tie ⇒ targeted exclusion of an identity via the public calendar | Blind review | REAL FAIL (analytic) | v0.1: tie-break independent of block content; signed ommers credited for activity | — |
| v0.2.1 | Equivocation tie: two variants with the same tie stall honest nodes on the prefix (≈5 h for 1 M sats, repeatable) | Blind review (three reviewers) | REAL FAIL (analytic) | v0.3 §7.3: a producer may extend any tied tip, and every extension strictly wins | Explicit `EQUIVOCATION_TIE_STALLED` state (N-SPEC §9.4) |
| v0.5 | The density brake at 7/10 is a liveness switch held for free by calibrated adversarial abstention or withholding | Blind review | REAL FAIL (analytic) | v0.6: health measured outside QUEUED identities, plus a slow exclusion lane (1 % over 7 epochs) | TLA+ slow-lane witnesses; mutation "brake cancels all budgets" caught |
| v0.7 | **Delivery at 0.70 blocked by adversarial abstention**: at the domain corner (β = 0.30 abstaining, d = 0.70) expected density is ≈0.49, below the 7/10 laboratory threshold, so delivery is suspended | Analysis (coherence check) | REAL (liveness only; safety needs ≈0.17) | Owner decision Q3: H_N delivery profile `rho_deliv = 43/100`; consensus brake constant unchanged at 7/10; default depth K(10⁻⁶) = 739 blocks | TLA+ non-interference: **13 BOUNDED PASS**, 5 WITNESSES, 3 MUTATION FAILs (threshold leaking into selection, brake, STOP); **QR-5** |
| v0.6 → v0.7 | **τ = 6 s against 256 KB block propagation**: on W1 (≈170 ms RTT, 0.5 % loss), full 256 KB blocks reach a worst case of 4.7 s per hop against a 5 s budget; at 2 hops, 10 % of honest blocks are late. One lossy TCP connection carries ≈150 KB/s | Bench (European measurement + emulation on real links) | REAL FAIL of τ = 6 s beyond one hop | Owner decision: **τ = 10 s** (2-hop W1 ≈ 10⁻⁵, extrapolated); W2 out of domain. No propagation optimisation assumed | **QR-1, QR-2** |
| v0.5 / v0.6 | **The 7,200 / 2,880 pair was never derived**: in profile A it is certified only at τ = 6 s, p_late = 0, ε_H = 10⁻⁶; it fails from τ ≥ 8 s or Q_B = 256 (b > b_max) | Analysis (exact DP + composition) | REAL FAIL (analytic) of the parameter choice | Pair abandoned. Derived under H_N: **K_reg = 2,750, registry_min_blocks = maxreorg = 1,630**, ε_H ≈ 4.6·10⁻¹⁰. The naively rounded pair (2,740; 1,630) is also rejected because b_max(2,740) = 1,629 | Reproducible derivation script and `composition` table |
| v0.7 | DP vs Monte-Carlo gap of a factor 1.3 to 1.8 on K | Analysis + Monte-Carlo (no MC run exceeded the DP: MC/DP ≤ 0.61; no significant excess over the exact private attack with adverse tie-break, max z = +1.6) | Unexplained | DP (conservative) published | **QR-3** |

---

## 5. What remains open

Freezing the architecture leaves ten traceable requirements. A public testnet presupposes QR-1 to QR-9 accepted.

| ID | Open item | If it fails |
|---|---|---|
| QR-1 | Δ, clock skew and p_late measured with a real N client on ≥ 3 continents, ≥ 2 real hops, maximal blocks | Revise τ or the domain, or optimise propagation |
| QR-2 | Delay correlation and per-window bound, including outages and targeted DoS | Feed correlation into the K derivation; targeted delays count in β |
| QR-3 | Explain the DP/MC gap on K | A strategy beating the DP is a counterexample and reopens K_reg |
| QR-4 | Finish the strict deep-pivot exploration, or prove an abstraction | Invariant violation: architectural reopening |
| QR-5 | Delivery non-interference with the faithful brake, then on the implementation | Leak to consensus: fix in the implementation |
| QR-6 | Written, independently reviewed composition proof | Revised bound; K_reg and b re-derived |
| QR-7 | Bitcoin seed grinding qualified; decide Q_B | Parameter re-derived, no mechanism |
| QR-8 | Per-node RECOVERY procedure specified and tested | Reopening limited to the recovery section |
| QR-9 | A4 (anchor compatibility) requalified at v0.7 parameters | Invariant violation: reopening |
| QR-10 | Client profiles aligned with H_N | Documentation |

Also explicitly open or not covered: nothing guarantees that STOP fires outside H_N (in particular on W2); macOS clocks were measured at 85–120 ms, at the edge of H_N-8; Δ_val excludes state access; the TLA+ models use abstract constants and are not composed into one global model.
