# N-SPEC — BATHRON consensus engine N

> **N v0.7 — Architecture Frozen Candidate. Not mainnet-qualified. Not production-ready.**
> The current BATHRON Core does **not** implement N yet. Implementation follows the qualification requirements below.
> Network status: <https://bathron.org/docs/status.html>.

N is a mechanical, vote-free consensus engine. It uses **one producer per slot**, drawn from a registry of burned Bitcoin tickets with a
Bitcoin-derived seed, and a deterministic fork-choice by score (most valid production blocks since genesis, then a public tie-break
independent of block content). It has no committee, no quorum and no finality gadget.
- Bitcoin provides roots, facts, time and randomness.
- Objects carry provenance and conservation.
- N only chooses the canonical history when evolutions become incompatible.
- Bitcoin fingerprints can trigger STOP. They never promote a branch.

Start here:
- **[docs/WHY-N.md](docs/WHY-N.md)** (FR: [WHY-N.fr.md](docs/WHY-N.fr.md)) explains why N, what it guarantees under its published domain, and
  what it does not guarantee.
- **[docs/ATTACKS.md](docs/ATTACKS.md)** (FR: [ATTACKS.fr.md](docs/ATTACKS.fr.md)) is the falsification history: what broke, how it was
  found, and what was changed.
- **[spec/N-SPEC-v0.7.md](spec/N-SPEC-v0.7.md)** is the normative specification (in French). Its changes from v0.6 are listed in
  [spec/CHANGELOG-v0.7.md](spec/CHANGELOG-v0.7.md).

## Published domain H_N (summary, §17 of the spec)

| | |
|---|---|
| Slot `τ` | 10 s (derived from a network bench; 6 s was too close to block-propagation limits) |
| Network | W1-class links (RTT ≲ 170 ms, loss ≲ 0.5 %), ≤ 2 relay hops, clocks ≤ 100 ms |
| Adversary / availability | β ≤ 0.30 of total weight, honest availability d ≥ 0.70, so effective honest production h ≥ 0.49 |
| Risk target | ε_H = 10⁻⁹ over 10 years (Bitcoin seed grinding Q_B = 1; Q_B = 256 not qualified) |
| Derived (conditional; reproducible with `analysis/cp-reg/derivation/check_v07_point.py` → ε_H ≈ 4.6·10⁻¹⁰ at Q_B = 1) | `K_reg` = 2 750 slots, `registry_min_blocks` = `maxreorg` = 1 630, delivery density 43/100, default delivery depth K(10⁻⁶) = 739 blocks |
| New or long-absent nodes | Outside the CP_reg claim until they initialise from a recent authenticated origin (weak subjectivity) |

Outside H_N, N makes **no quantitative claim**.

## Layout

| Path | Content |
|---|---|
| `spec/` | Normative spec v0.7 and changelog |
| `docs/` | WHY-N, ATTACKS (EN + FR) |
| `qualification/` | Freeze criteria, qualification requirements QR-1…QR-10, network bench synthesis |
| `analysis/cp-reg/` | Common-prefix analyses (two independent methods), first-divergence lemma, deep pivot, delivery profile, consistency check, `derivation/` (K(ε) and K_reg derivation, reproducible) |
| `formal/` | TLA+ models v0.5 and v0.6, plus extensions (campaign logs, mutations, witnesses). `tla2tools.jar` is not included: download it from the TLA+ project |
| `bench/` | Network bench tools (`nbench.py`, runners, analysis, `plate.py`), results, sanitized raw data of the realistic-load run (hosts anonymised) |

## Provenance and paths

This repository is a curated extract of a private research log. Documents keep their original cross-references:
- `DIRECTION.md`, `MANDAT-*.md`, earlier N-SPEC versions (v0 to v0.6) and the studies of earlier engine candidates (C, D, E, …) are
  **not published here**. References to them record provenance; they are not needed to read or check the published material.
- Research paths map to this repository as follows: `etudes/n-spec/N-SPEC-v0.7.md` → `spec/`; `etudes/n-spec/cp-reg/` → `analysis/cp-reg/`;
  `etudes/n-spec/tla/modele-v0.5/` and `modele-v0.6/` → `formal/`; `etudes/n-spec/banc-reseau/` → `bench/`;
  `CRITERES-GEL`, `EXIGENCES-QUALIFICATION` and `SYNTHESE-BANC-TAU` → `qualification/`. Reproduction commands written with research
  paths must be adapted accordingly.
- Bench hosts are named `vps1`, `vps2`, `mac` (roles only); peer addresses are replaced by `HOST_A/B/C`.

Status vocabulary used throughout: bounded exhaustive PASS, PASS under hypotheses, expected FAIL of a mutation, real normative FAIL,
witness, INCOMPLETE (≠ PASS), NT (not tested), analytic, Monte-Carlo, extrapolation.

## Changing the architecture

The architecture is frozen. It changes only on a **counterexample**, an **invariant violation**, an **implementation impossibility**, or a
**real measurement incompatible with H_N**. A wrong parameter value is corrected in H_N, not by new mechanics.

Issues with a minimal counterexample are welcome.

## License

- **Code** (scripts, simulators, bench tools, TLA+ modules and model configurations, under `analysis/`, `bench/` and `formal/`): MIT, see
  [LICENSE](LICENSE).
- **Documents** (the specification, changelog, docs, qualification, analysis and campaign reports, tables and figures, all `*.md` files):
  Creative Commons Attribution 4.0 International (CC BY 4.0), see [LICENSE-docs](LICENSE-docs).
- Data files produced by the tools (logs, CSV, JSON, archives) follow the license of the documents (CC BY 4.0).

Copyright (c) 2026 The BATHRON developers.

## What is (not) evidence here

Development, preliminary and interrupted runs were removed from this extract. Remaining TLC logs are kept for traceability. Machine-specific
paths in them are replaced by `<JAVA>` / `<TMPDIR>`, and launcher defaults (Homebrew Java path) are overridable by environment variables.
A log is evidence only for the status it records (bounded PASS, witness, INCOMPLETE), within the bounds of its model.
