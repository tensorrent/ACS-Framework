# Nested uncertainty domains and all-target recovery

All seventeen benchmark targets are now recovered for observation A at radius 0.08 and B at radius 0.05, under both generic local profiles. The certificates also apply to contained smaller noise boxes with the same original intervals and deduction contract. Re-optimizing from the preceding audit-strengthened domains at radius 0.1 makes no additional exclusions. At that radius, the degree/discriminant profile still recovers 15/11 targets for A/B; degree-only recovers 14/11.

The [checkpoint package](../../docs/frontier/2026-09-13-aggregate-nested-delta/README.md) preserves every premise transfer, proposal, interval certificate, exclusion, kernel check and continuation gate. No new zeros, measurement rows, field templates, Galois-group information or arithmetic coefficient seeds are introduced.

## The transfer rule

For fixed original intervals [l_i,h_i], define the uncertainty box B(r) by l_i-r <= t_i <= h_i+r for every root index i. If 0 <= r <= R, then B(r) is a subset of B(R): the two endpoint margins are both R-r >= 0. Any predicate proved for every point in B(R) therefore holds throughout B(r).

The same original root intervals, index correspondence, population, cutoff, measurement family, global metadata and local profile must be retained. A smaller-radius result cannot be transported to a larger radius without further evidence. This pass starts every case with the final independently strengthened radius-0.1 domains from the preceding checkpoint; it never seeds a larger radius with a smaller-radius success.

[NoiseBoxTransfer.lean](proofs/NoiseBoxTransfer.lean) checks four theorems: scalar interval membership, coordinatewise box membership, transfer of an arbitrary universally valid box predicate, and a counterexample to reverse inclusion. The recorded and freshly recompiled proofs use the ordinary Lean axioms propext, Classical.choice and Quot.sound, with no sorryAx. These theorems formalize the geometric transfer step. They do not formalize the explicit formula, arithmetic/local premises, numerical error budgets, optimizer, or file lineage.

The Python producer records all outer and inner rational endpoints. The independent audit reconstructs those endpoints from the fixed input spectra and checks both margins exactly, across 540 root-interval transfers. The producer also checks that the source closure matches its preceding manifest, and records the exact preceding verification artifact as an input. The final verifier recursively validates those earlier deductions.

## Numerical calculation and audit

The tested radii are 0.1, 0.08, 0.06, 0.05, 0.04 and 0.03, for both observations and both local profiles: 24 cases. After the seed transfer, the method repeats the [adaptive multiplier calculation](AGGREGATE_ADAPTIVE_README.md): local projection, domain-aware sampled LP proposals, rationalization, a fresh continuum error certificate for every vector, simultaneous exclusions, then another round. The general-domain support identity remains min(D)*r + (max(D)-min(D))*max(r,0).

There are 470 new vectors, all with successful sampled LP status. Each receives a 224-bit real first-derivative cover with 48 leaves per active root before producer deductions. The independent audit checks 110,832 stored midpoint values/derivatives and computes 221,664 fresh complex quadratic leaves at 384 bits. Exact rational moment endpoints and integer/Fraction domain supports validate all 470 objectives, 132 dual exclusions and 100 consequent local exclusions. Independent local catalogue enumeration and 412 separate 85-digit displaced controls provide complementary checks. All 604 held-out true coefficients survive every round.

Four stronger audit exclusions occur before the producer eventually removes those same candidates. Supplemental exact closure from the producer's final domains adds zero dual or local exclusions. The existing closure instrument is reused unchanged and its exact source hash is preserved. The transcendental interval routes share FLINT; mpmath controls are samples, not completeness proofs.

At radii 0.08 and 0.06, degree/discriminant recovery is 17/13 for A/B. At radii 0.05, 0.04 and 0.03 it is 17/17. Degree-only counts agree on these positive-radius grid points. At radius 0.1, re-optimization reaches the same final domains as its input in one round, preserving the earlier 15/11 and 14/11 results.

These results give a sufficient all-target radius of 0.08 for A and 0.05 for B. The next tested radii where this update stalls short of all targets are 0.1 and 0.06 respectively. Those pairs locate useful next tests; their upper endpoints are not impossibility bounds or proved optimal thresholds. Surviving domains are retained without asserting field realizability or genuine ambiguity. Earlier exact-input full-row results, including stronger support statistics, remain intact.

## Adversarial boundary checks

Ten actual mutations challenge transfer to a larger radius, an outward radius increase lost in binary64 rounding, negative radius, missing roots, permuted root correspondence, changed source centers, an inner endpoint outside its seed, domains borrowed from another observation, smaller-radius singletons, and final domains used as earlier premises.

An exact endpoint witness lies in the radius-0.1 root interval but outside the radius-0.08 interval by 0.02. A predicate valid throughout the smaller interval fails there, demonstrating why unrestricted reverse transfer is invalid. This concerns interval geometry, not a constructed alternate spectrum or number field.

A second displayed witness has destination radius 0.1 + 1e-21. It has the same binary64 value as 0.1 but strictly exceeds it in exact arithmetic, and its upper endpoint lies outside the certified seed interval. This is the same rounded-order mutation listed among the ten controls, not an additional independent experiment.

## Reproduction and next gates

Run from the repository root with the pinned Python environment and inherited Lean/mathlib runtime:

    python code/frontier_verification/verify_aggregate_nested_delta.py

The verifier reruns the preceding checkpoint chain, all new numerical stages, the unchanged supplemental closure, ten mutations, and fresh Lean compilation. It compares the compiled proof artifact, source versions, execution streams, input fingerprints, summary, complete branch catalog and ledger prefix. Five scientific commands succeeded; packaging and final recursive verification are separate.

Next, refine the success/nonclosure test ranges (0.08,0.1) for A and (0.05,0.06) for B. Improve the optimization or propagation method before interpreting stalled updates, compare noisy standalone-row propagation, and investigate constructive feasibility or global-field obstructions. Additional matched-invariant fields and the rest of the ACS queue remain open. The ongoing objective is further verified delta, not global completion.
