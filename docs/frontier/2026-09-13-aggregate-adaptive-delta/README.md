# Adaptive multiplier and audit-closure delta — 13 September 2026

Both aggregate spectra now have all seventeen target coefficients recovered at tested ordinate radii 0, 0.005 and 0.02 under either generic local profile. At radius 0.1, recovery rises from 13/10 to 15/11 targets under degree/discriminant rules, and from 11/10 to 14/11 under degree-only rules. The change re-optimizes measurement combinations after valid domain reductions and freshly certifies each changed uncertainty budget. No new zeros, measurement rows, field templates or arithmetic seeds enter inference.

The [derivation and reproduction guide](../../../code/frontier_verification/AGGREGATE_ADAPTIVE_README.md) explains the general-domain support identity, ordered premises, interval certificates and remaining limits. The earlier exact-input full-row result already recovered all seventeen targets and remains stronger on some support statistics. The new result concerns positive-radius recovery; no optimal robustness threshold or global feasibility is asserted.

- [Results and remaining target domains](Adaptive_Summary.json).
- [Adaptive feedback and all 288 continuum certificates](Adaptive_Feedback.zip), including every proposal, premise hash, local model and round.
- [Independent audit](Adaptive_Audit.json): 80,976 stored midpoint checks, 161,952 fresh complex quadratic leaves, 288 exact domain objectives, 356 mpmath displaced controls, 109 dual exclusions and 87 local exclusions. All 604 held-out coefficients survive every round.
- [Supplemental audit closure](Audit_Closure.json): two actual exclusions consume eight repeated audit findings, removing candidate 2 from B's coefficient at 31 at radius 0.1 under both profiles. No further local or singleton gain follows.
- [Ten component mutations and a stale-budget counterexample](Adversary_Audit.json). Permitted displaced roots make a ninefold measurement combination exceed its unscaled old budget by more than 0.383 in the finite-sum change alone. Unknown-tail saturation and alternate fields are not asserted.
- [Four scientific execution receipts](Execution_Receipts.json), [full outputs](Execution_Artifacts.zip), [development notes](Development_Notes.json), [runtime](Runtime.json), [inherited inputs](Inherited_Inputs.json) and [reused sources](Primary_Sources.json).
- [Source inventory](Source_Inventory.json), [snapshot](Source_Snapshot.zip), [manifest](Manifest.json) and [fresh recursive verification](Verification.json).
- [All 117 research branches](Research_Queue.json) and the [408-event ledger](Branch_Events.jsonl), preserving the prior 403 events byte for byte.

At radius 0.1 under the stronger profile, two A targets and six B targets remain unresolved. Their candidate domains are preserved, without a claim that they are globally realizable. The transcendental interval routes share FLINT; exact moment and integer calculations provide additional checks. The full analytic proof is not formalized. Earlier failures, input contracts and stronger scoped results remain intact in the [preceding checkpoint](../2026-09-13-aggregate-moment-delta/README.md) and its history.

Next, re-optimize from audit-strengthened domains, bracket all-target recovery beyond radius 0.02, compare noisy standalone-row propagation and investigate constructive or global feasibility. Additional matched-invariant fields and the wider ACS questions remain open.
