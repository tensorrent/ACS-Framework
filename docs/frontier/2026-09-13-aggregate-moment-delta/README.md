# Joint moment uncertainty and noisy target feedback — 13 September 2026

At ordinate-error radius 0.1, generic local rules and frozen-dual residual feedback recover thirteen of seventeen targets in spectrum A and ten in B when ramification is inferred from discriminant 576. Raw spectral certificates recover three and four. Every held-out true coefficient survives the independent integer replay. The remaining four and seven target domains are preserved as unresolved candidates, without a claim of global realization or ambiguity.

The calculation also combines each root's finite-sum and known-moment changes before maximizing its uncertainty budget. It tightens 97 budgets by at most about 0.7042%, but creates no producer candidate-domain changes on this grid. The larger recovery gains come from extending the objective set and feeding valid local domains back into frozen-dual residual supports. The [derivation and reproduction guide](../../../code/frontier_verification/AGGREGATE_MOMENT_README.md) explains both effects and their limits.

Under the degree/discriminant local profile, feedback recovers 13/13 targets at radii 0.005 and 0.02, and 13/10 at radius 0.1. Degree-only local feedback reaches 11/10 at radius 0.1. This method's 14/13 zero-radius result is weaker than the earlier best exact-input 17/17 row/local closure, which remains valid. The limitation motivates re-optimizing after domain reductions.

- [Results, ablations and remaining domains](Moment_Summary.json).
- [272 joint-moment proposals](Moment_Proposals.json) and [288 complete continuum certificates](Moment_Certificates.zip), including sixteen previous coefficient-seven vectors on the common grid.
- [Independent moment audit](Moment_Audit.json): 104,592 stored midpoint checks, 209,184 fresh complex quadratic interval leaves, 576 exact objective bounds, three symbolic moment derivatives and 528 high-precision displaced sums.
- [One-pass local projections and residual feedback](Local_Feedback.zip), with every domain, model and iteration, and [independent exact replay](Moment_Local_Audit.json) of 12,326 one-pass local removals, 12,396 local removals within feedback and 56 dual removals. Counts include the declared method/profile/radius replicas.
- [Ten semantic mutations and a one-root counterexample](Adversary_Audit.json). Moving that root while freezing its known moment omits a positive analytic-budget term above 1.099e-7; unknown-tail saturation and alternate fields are not asserted.
- [Seven scientific execution receipts](Execution_Receipts.json), [full outputs](Execution_Artifacts.zip), [development notes](Development_Notes.json), [runtime](Runtime.json), [inherited inputs](Inherited_Inputs.json) and [reused primary sources](Primary_Sources.json).
- [Source inventory](Source_Inventory.json), [source snapshot](Source_Snapshot.zip), [manifest](Manifest.json) and [fresh recursive verification](Verification.json).
- [All 117 research branches](Research_Queue.json) and the [403-event ledger](Branch_Events.jsonl), retaining the previous 398 events byte for byte.

No new zeros, measurements, field templates or arithmetic coefficient seeds are supplied to inference. Noisy domains come from certificates for that same radius. The transcendental interval routes share FLINT; rational moment bounds and integer feedback provide additional checks. The complete analytic and number-field proof remains unformalized. All previous failed attempts and stronger scoped results remain intact in the [preceding checkpoint](../2026-09-13-aggregate-optimized-delta/README.md) and its history.

Next, re-optimize multipliers after validated domain reductions and compare noisy standalone-row propagation. Constructive feasibility, global-field ambiguity, additional fields and the wider ACS questions remain open.
