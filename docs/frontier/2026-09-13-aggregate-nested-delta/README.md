# Nested uncertainty and kernel-transfer delta — 13 September 2026

All seventeen benchmark targets are certified for A at ordinate radius 0.08 and B at radius 0.05 under both generic local profiles. The certificates also apply to contained smaller noise boxes with the same input contract. Each case starts from the preceding independently strengthened radius-0.1 domains and transfers them by exact interval inclusion, then re-optimizes and freshly certifies measurement combinations. No new roots, measurements, field templates or arithmetic seeds are supplied.

The [derivation and reproduction guide](../../../code/frontier_verification/AGGREGATE_NESTED_README.md) connects the numerical calculation with the kernel-checked transfer rule. At radius 0.1, re-optimizing from the stronger audit domains makes no further exclusions. The next tested nonclosure radii are 0.1 for A and 0.06 for B; these locate useful next experiments, not proved impossibility or optimality thresholds.

- [Results, domains and next test ranges](Nested_Summary.json).
- [All twenty-four nested recoveries and 470 continuum certificates](Nested_Feedback.zip), including exact premise intervals, local models, proposals and every round.
- [Independent numerical audit](Nested_Audit.json): 540 root-interval transfers, 110,832 stored midpoint checks, 221,664 fresh complex quadratic leaves, 470 exact objectives, 412 displaced controls, 132 dual exclusions and 100 local exclusions. All 604 held-out true coefficients remain after every round.
- [Supplemental exact closure](Nested_Closure.json): four stronger intermediate audit findings are already obtained by the producer later; no additional exclusions result.
- [Four Lean theorem checks](Lean_Check.json) and [compiled/source artifacts](Lean_Artifacts.zip), proving scalar and coordinatewise inclusion, universal-predicate transfer, and failure of the reverse inclusion. The full numerical and arithmetic argument is not formalized by these geometric theorems.
- [Ten transfer mutations and exact endpoint witnesses](Adversary_Audit.json), including an outward radius increase of 1e-21 that has the same binary64 representation as 0.1. The exact check rejects it.
- [Five scientific execution receipts](Execution_Receipts.json), [full outputs](Execution_Artifacts.zip), [development notes](Development_Notes.json), [runtime](Runtime.json), [inherited inputs](Inherited_Inputs.json) and [reused sources](Primary_Sources.json).
- [Source inventory](Source_Inventory.json), [snapshot](Source_Snapshot.zip), [manifest](Manifest.json) and [fresh recursive verification](Verification.json).
- [All 117 research branches](Research_Queue.json) and the [413-event ledger](Branch_Events.jsonl), preserving the prior 408 events byte for byte.

Exact rational differences check both sides of every transferred interval. The same observation, local profile, root indexing, population and global inputs are retained. The transcendental interval methods share FLINT; rational, integer and Lean checks have their stated scopes. No surviving domain is asserted to describe an actual field. Earlier failures and stronger exact-input support results remain in the [preceding checkpoint](../2026-09-13-aggregate-adaptive-delta/README.md) and its history.

Next, refine the A (0.08,0.1) and B (0.05,0.06) success/nonclosure test ranges, improve the optimization or propagation method, compare noisy standalone-row inference and investigate constructive/global feasibility. The wider ACS investigation remains active.
