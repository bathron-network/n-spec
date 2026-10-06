# Why N

**Architecture frozen candidate. Not mainnet-qualified. Not production-ready.**

Why BATHRON's base engine is N (voteless, one producer per slot), what it guarantees, and under which conditions. Normative text: **N-SPEC v0.7**. Counterexamples: **ATTACKS.md**. French: `WHY-N.fr.md`.

Status (1 October 2026): frozen **at the architectural level**. Architecture changes require a counterexample, an invariant violation, an implementation impossibility, or a real measurement incompatible with H_N; never a search for elegance. A wrong parameter value is corrected in H_N or a client profile.

---

## 1. What was abandoned, and why

Each candidate below went through kill-tests by at least two independent analyses; several also had blind reviews.

### C: a sequencer plus a ticket-holder quorum (Tendermint-like)

C paired a single sequencer with a quorum of ticket holders that finalised batches (`q > (N+f)/2`, per-height locks, chained certificates, ban on proven equivocation). Its bounded TLA+ model, adapted from a published Tendermint model, found **no safety violation** and caught every deliberately broken variant. No safety bug was found in C. What weighed against it:

- **β cannot be enforced.** The β kill-test showed that "the burn guarantees β" fails: a burn has a cost, but it bounds neither concentration, key rental, corruption, coercion nor attrition. At launch, with a handful of project-managed producers, no β < 1 is defensible.
- **Cost.** Post-quantum votes from thousands of registered identities are expensive. One analysis put N's production signatures at ≈35 MB/day (6 s slots), against ≈49 GB/day for two full C phases every 60 s at 7,000 identities (a factor of ≈1,400).
- **Witness economics.** A blind review of the economics found no remuneration for witnesses.

C is **archived** as a possible future mechanism for irrevocable decisions. Nothing defers to C at genesis. A private C on top of N would be attestation or insurance; it would not make N decisions irrevocable.

### Irrevocable decisions without a quorum: D, D2, D3, Bitcoin barrier

- **D** (irrevocability by convergence): killed. An equivocating owner plus a partition gives two incompatible decisions each claimed to be irrevocable, and silence proves nothing.
- **D2** (mechanical irrevocability): without votes, uniqueness needs a common non-equivocating log, which is Bitcoin. The cost is one Bitcoin transaction per transfer or batch. Not adopted.
- **D3** (single lineage, Bitcoin read-only): killed for free payments. For any local rule, P[double lineage] ≥ 2·(liveness of an honest payment) − 1. Reading Bitcoin proves "after H", never "before H". What survived: clock automata and the **one-hop settlement object**.
- **Bitcoin barrier** (synchronous BFT clocked by Bitcoin): safety rests on Δ. Two tickets plus a partition longer than 2Δ give two silent FINALs.

### Sampled certificates and hybrids: E, E2, two stages, NC

- **E/F**: sampling yields no small committees (≈200 members at β = 0.1, 1,300 to 2,600 at β = 0.2, impossible at β = 0.3), and E still depends on C. Deferred.
- **E2** (faithful SBRB/DPRB): **closed**. It needs 27 to 252 Mbit/s per node at 32 tx/s (≈5 for C), offers probabilistic safety under a static adversary, and has no exportable proof.
- **Two stages** (chain plus C checkpoints) and **NC** (irrevocable C decisions per object): no gain on β. NC's irrevocability requirement does not stay local: it propagates in depth, upstream and to new nodes.

Common thread: irrevocable decisions need an intersecting quorum, Bitcoin writes, or synchrony carrying safety. On 30 September the owner chose to give up that requirement.

## 2. Why N exists

The current application draft defines **M0 as the only settlement asset**. For the application reading of N-SPEC §13, see [APP-SPEC v1 draft, GEN-3](../app/APP-SPEC-v1-draft.md#01-rang-du-document); the frozen engine text is unchanged. SPs and LPs are roles outside consensus and do not require a registered identity; a producer is a registered identity selected to produce a block.

N is the answer to a choice made explicitly by the project owner on 30 September: **pure N at genesis**.

- One producer per slot, drawn mechanically from Bitcoin and the ticket registry.
- A mechanical fork-choice with no vote, quorum, QC, lock, round or certificate.
- Tickets are a production lottery, not voting weight. A burn of `P0 = 1,000,000 sats` buys one unit of weight. The burn makes Sybils costly. It does not guarantee that tickets are independent.
- No block reward. Fees are transferred, never minted.

There is no native finality. N provides no exportable proof of irrevocability and gives up "pause rather than roll back". Client vocabulary: **inclusion → depth → stability under a policy**; there is no native `FINAL`. Atomicity holds **on every branch** (X/M0 delivery-versus-payment is all-or-nothing). For BTC/M0 the Bitcoin leg is irreversible, so the residual risk ε(k) is carried and priced by the settlement or liquidity provider (SP/LP) through its choice of depth.

In exchange: a chain that keeps producing, mechanical "like Bitcoin", with signature bandwidth two to three orders of magnitude below a voting engine.

## 3. The property split

> Bitcoin creates the roots. Objects carry and conserve the rights. N chooses the canonical history when evolutions become incompatible.

| Property | Carried by | Meaning |
|---|---|---|
| **Provenance** | Bitcoin | Every settlement resource has a typed Bitcoin origin. Supply equals the sum of burns. TICKET and REACT create zero M0. |
| **Conservation** | Objects / Core | Transitions are valid inside each history. Native transitions and their undo are atomic. This is an interface obligation (G1–G10), checked jointly with the application specification. N alone does not prove settlement-asset conservation. |
| **Canonicity** | N | Selection of one history among incompatible ones. This is the only thing N decides. |
| **Anteriority** | Bitcoin | A prefix commitment carried in an admissible Bitcoin transaction (M0 burns, NEW/ADD tickets, REACT). There is no dedicated `ANCHOR` transaction. |
| **Origin** (new or returning nodes) | A′ / RELEASE | A `BOOTSTRAP` package distributed with releases and authenticated by 4 keys with a 3-of-4 threshold. Exceptional recovery uses an explicitly accepted `RECOVERY` package. |

A long-range attack under N is therefore a **registry** conflict, never a settlement-asset conflict. Settlement-asset conservation (no creation of M0) holds **only under the application obligations G1–G10 (spec §21), which are not yet qualified**.

## 4. Weak subjectivity

N is weakly subjective, by an explicit owner decision (D1, 1 October).

- A **synchronised** node (one that itself satisfies the network assumptions of H_N) is protected by `maxreorg`. A private branch that changes calendar after the start of an epoch would require a reorganisation deeper than `maxreorg`, and the node goes to `HALTED_DEEP_REORG` instead of adopting it. This is probabilistic, not deterministic: the failure probability is bounded by the term `T_CG` of the composition.
- A **new or returning** node (no local origin, or one whose reception left the D = 0 regime) is **outside the CP_reg domain**. It can adopt a private branch without any forbidden disconnection. That risk is not bounded. It is long-range, resurfacing through the registry.
- Such a node returns to the domain only after initialising from a **recent authenticated origin**, meaning one at least `maxreorg + 1 = 1,631` blocks after any relevant fork. A fresh node uses `BOOTSTRAP`. A returning node that keeps its origin uses the explicit `RECOVERY` path, which preserves its signature reservations and anti-double-signing memory.
- An origin has **zero fork-choice power** over a synchronised node. A `BOOTSTRAP` received by a node that already has a local origin is ignored (`BOOTSTRAP_IGNORED_LOCAL_ORIGIN`). Ordinary operation (restart, absence, catch-up, fork-choice) requires no checkpoint. A bootstrap does not expire because of age alone, and no amount of elapsed time counts as approval of a new origin.

## 5. Bitcoin's role

Bitcoin is read-only for N. N never changes Bitcoin's rules and adds no anchoring transaction. Bitcoin supplies four things:

1. **Roots.** Burns create M0 and tickets. REACT is authenticated by the Bitcoin signature itself.
2. **Facts.** Every node verifies headers, confirmations and payments. The one-hop BTC/M0 settlement is resolved by inclusion of the Bitcoin leg.
3. **Time.** The median time past (MTP), a 12-hour seed guard (43,200 s), a 7,200 s MTP margin, and durations counted in Bitcoin heights (`G_anchor = 26,280`, cadence 13,140, REACT grace 4,032).
4. **Randomness.** The epoch seed hashes the first Bitcoin block whose MTP passes the seed time, buried at `k_seed = 30` confirmations, together with the registry root. No N parent, state, signature or producer nonce enters the seed.

**Fingerprints can trigger STOP but never promote a branch.** The owner's invariant, as stated in N-SPEC (translated):

> A Bitcoin anteriority proof can shrink the set of histories a node considers safe, or trigger a halt. It can never, on its own, make canonical a history that N's fork-choice would not have chosen.

H1, the long-range check, is a **separate veto**. The N base decision stays as it is, or turns into a wait or a halt. H1 never changes score, tie-break, registry, anchor or origin. It assumes at least one valid fingerprint roughly every 13,140 Bitcoin blocks (about 3 months), with a window `G_anchor` of about 6 months. During bootstrap, a real 0.01 BTC ADD per quarter is planned if natural activity does not provide one. H1 does not give complete long-range protection, and it does not protect a new node under eclipse.

## 6. The H_N domain

H_N is **part of the protocol**. N's quantitative guarantees (common prefix, CP_reg, safety depths) hold only inside it. A single profile (profile B) is published, so the boundary stays simple and auditable.

| # | Assumption | Value | Status |
|---|---|---|---|
| H_N-1 | Slot duration | τ = 10 s | Decision, based on bench runs |
| H_N-2 | Adversarial weight, on **total** weight, at every instant of the horizon | β ≤ 0.30 | Decision |
| H_N-3 | Effective honest availability (targeted DoS included) | d ≥ 0.70, so h = (1−β)d ≥ 0.49 | Decision |
| H_N-4 | Late honest blocks over any window of 1,913 slots | p_late ≤ 10⁻² | Conservative assumption, **not certified** |
| H_N-5 | Delays independent and not chosen by the adversary | — | Assumption, not verified |
| H_N-6 | Network class W1 | RTT ≲ 170 ms, loss ≲ 0.5 % | Decision; emulation |
| H_N-7 | Relay hops from producer to every honest node | ≤ 2 | Decision; extrapolated |
| H_N-8 | Clock skew | ≤ 100 ms | Decision; measured |
| H_N-9 | Validation per hop | Δ_val = 100 ms | Crypto micro-bench; state access not tested |
| H_N-10 | Existence condition | (1−β)·d·(1−2p_late) > β; at the corner 0.4802 > 0.30 | Analytic, necessary |
| H_N-11 | Reinforced condition | d ≥ d_min(β, ε); 0.70 against 0.524 needed (≈ 0.53 at p_late = 10⁻²) | Analytic + interpolation |
| H_N-12 | Safety target | ε_H = 10⁻⁹ over 10 years (2,192 epochs of 40 h) | Decision |
| H_N-13 | Selectable Bitcoin seeds per epoch | Q_B = 1 (256 not qualified) | Decision |
| H_N-14 | Common origin | Synchronised in the sense of §4 | Decision D1 |
| H_N-15 | Adversary covered | Public calendar, timing, withholding, optimal reveal, equivocation (one unit of progress per branch), abstention, adverse tie-break | Analytic (DP) |

Derived parameters (dynamic programming bound, composed per epoch, rounded up): **K_reg = 2,750 slots** (7 h 38 min), **registry_min_blocks = maxreorg = 1,630 blocks**. The composed horizon risk is ε_H ≈ 4.6·10⁻¹⁰ ≤ 10⁻⁹. These are conditional derivations, not established guarantees. The DP curve is extrapolated below 10⁻¹⁴, and the composition of the two pivot terms is still a sketch.

**Out of domain:** W2 networks or worse, more than 2 hops, clocks beyond 100 ms, β > 0.30 or d < 0.70 at any instant, correlated or targeted delays, new or returning nodes before re-initialisation, Q_B > 1, and horizons beyond 10 years. Outside H_N, N makes **no quantitative claim**. Only the existing halts and recoveries apply. **Nothing guarantees that a STOP fires outside the domain.**

## 7. Why SPs and LPs choose their own depth

There is no native finality in N. It publishes a table instead. K(ε) is the depth beyond which a common-prefix violation has probability at most ε **per cut**, at the worst corner of the domain (β = 0.30, d = 0.70, p_late = 10⁻²):

| ε per cut | K slots | K blocks | Duration at τ = 10 s | [best exact private attack, slots] |
|---|---:|---:|---:|---:|
| 10⁻⁶ | 937 | 739 | 2 h 36 min | [584] |
| 10⁻⁹ | 1,425 | 1,123 | 3 h 58 min | [903] |
| 10⁻¹² | 1,913 | 1,508 | 5 h 19 min | [1,224] |

"K blocks" counts non-empty slots, equivocations included. Counting only visible honest blocks would not be safe. The default depth of the H_N delivery profile is **K(10⁻⁶) = 739 blocks**. Core exposes the full table, and each SP or LP may require a larger depth for a smaller ε. The risk belongs to the party that delivers outside value, so that party chooses the depth, with an exposure cap. The delivery density threshold (`rho_deliv = 43/100`) only affects liveness. A bounded TLA+ non-interference check (13 threshold classes, on a model with a simplified brake) found no path from this threshold into fork-choice, the anchor, STOP, the registry rule, the brake or production. The check with the faithful brake model, then on the implementation, is still open (QR-5).

## 8. What N guarantees under H_N, and what it does not

**Under H_N, N claims:**
- a common prefix at depth K(ε) per cut, from the published table (analytic DP bound);
- registry agreement (CP_reg) between synchronised nodes, as a conditional derivation (not a closed theorem) with ε_H ≈ 4.6·10⁻¹⁰ ≤ 10⁻⁹ over 10 years;
- for a synchronised node, a deep halt (`HALTED_DEEP_REORG`) rather than adoption of a private branch that changes calendar after the start of an epoch, except with probability at most `T_CG` (the pivot cases below `maxreorg` are counted separately, in `T_court` and `T_profond`, inside ε_H);
- determinism: the same candidate chain, epoch and Bitcoin context give the same registry and seed, whatever a node observed earlier;
- atomicity of native transitions on every branch;
- zero settlement-asset creation by N, and zero fork-choice power for an origin or for H1.

**N does not guarantee:** native finality; convergence between incompatible origins; safe sync under eclipse; an unpredictable calendar; unbiased Bitcoin randomness; complete long-range protection; a universal attack cost; absence of censorship or DoS; BTC/M0 atomicity once the lock is gone; settlement-asset conservation without application qualification. Deep halts persist as long as the conflict does.

## 9. Qualification reserves (QR-1 … QR-10)

Open reserves, each with a phase and acceptance criterion. Order: implementation → simulation → fuzzing → extended bench → external audit → testnet; a public testnet presupposes QR-1 to QR-9 accepted.

| ID | Requirement | Status (1 Oct) |
|---|---|---|
| QR-1 | Measure Δ, clock skew and p_late with a real N client, on at least 3 continents, with at least 2 real hops and maximal blocks | Europe-only measurement plus emulation |
| QR-2 | Estimate delay correlation and the per-window bound, including under outages and targeted DoS | Assumed |
| QR-3 | Explain the factor of 1.3 to 1.8 between the DP bound and Monte-Carlo on K | Open (DP published, conservative) |
| QR-4 | Finish the strict TLA+ exploration of the deep pivot, or prove an abstraction | INCOMPLETE (5.2 M states) |
| QR-5 | Redo delivery non-interference with the faithful brake model, then on the implementation | Bounded PASS on a simplified model |
| QR-6 | Write and independently review the composition proof (ε_fix + pivots + T_CG) | Sketch under assumptions |
| QR-7 | Qualify Bitcoin seed grinding (MTP, withholding, timestamps), then decide Q_B | Q_B = 1 assumed |
| QR-8 | Specify and test the per-node RECOVERY procedure | Not specified |
| QR-9 | Requalify A4 (anchor compatibility) at v0.7 parameters | Open |
| QR-10 | Align client profiles (`alpha_budget`, `Delta_nom_ms`, β) with H_N | Open (documentation) |

N v0.7 is a candidate whose weaknesses are named and whose parameters are derived. It is not a qualified system.
