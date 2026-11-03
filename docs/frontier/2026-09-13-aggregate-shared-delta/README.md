# Aggregate shared-error and local-feedback delta — 13 September 2026

The existing aggregate spectra now recover all 17 prime-power targets through 31 when generic local-degree rules and spectral inequalities are alternated. Shared root-error bounds also extend the tested sufficient coefficient-seven radii from 0.00001 to 0.002 for A and from 0.0001 to 0.05 for B. These are scoped advances; the ACS investigation remains ongoing.

No new zeros, field templates, Galois groups or held-out arithmetic are supplied to inference. This pass inherits the [preceding measurements and input contract](../2026-09-13-aggregate-delta/README.md). The [derivation and replay guide](../../../code/frontier_verification/AGGREGATE_SHARED_README.md) explains signed derivative cancellation, retained unknown-zero tails and residual support, local-degree models, and the limits of each result.

The radius comparison holds the dual multipliers fixed. Localizing each row derivative alone improves tested radii by 10x and 100x; adding signed cancellation contributes a further 20x and 5x. The generic unramified-prime rule separately excludes coefficient three and extends A's tested radius to 0.005. These are grid-tested sufficient certificates, not optimal noise thresholds or proofs of alternate fields at larger radii.

The baseline recovers 13/9 targets. One generic local pass reaches 14/11 using degree alone or 15/12 using discriminant ramification. Repeating local projections and spectral exclusions reaches 17/17 in both profiles. Full support remains partly unresolved: A has 45 singleton domains out of 604, B has 37 with degree alone and 38 with ramification. Local and spectral survivors need not describe a globally realizable field.

Evidence is preserved in:

- [Results and ablations](Aggregate_Shared_Summary.json), with all tested radius domains and both local profiles.
- [Shared and local certificates](Shared_Local_Certificates.zip), retaining both precision runs, exact interval leaves and every local/spectral iteration.
- [Independent shared-error audit](Shared_Audit.json): 39,600 stored midpoint checks, 47,520 fresh complex interval leaves, 144 exact integer objective bounds and 96 high-precision displaced sums. Two deliberately inconsistent row-error controls demonstrate the common-input premise.
- [Independent local audit](Local_Audit.json): separately enumerated eleven-model catalogue, 3,162 local and 190 spectral removals across eight cases, with all 604 held-out true coefficients retained.
- [Ten actual proof-component mutations](Adversary_Audit.json), each tested against an intact baseline and a semantic rejection predicate.
- [Seven execution receipts](Execution_Receipts.json), [complete outputs](Execution_Artifacts.zip), [source inventory](Source_Inventory.json), [source snapshot](Source_Snapshot.zip), [runtime](Runtime.json), [inherited inputs](Inherited_Inputs.json), [reused primary sources](Primary_Sources.json), and [development notes](Development_Notes.json).
- [Manifest](Manifest.json) and [fresh recursive verification](Verification.json). The [first verification attempt](Verification_Attempts.json) and [its exact output](Verification_Attempts.zip) preserve an output-file ordering failure at the final link check; the scientific instruments and results were unchanged.
- [All 117 research branches](Research_Queue.json) and the [393-event ledger](Branch_Events.jsonl), preserving the prior 388 events byte for byte.

Both interval routes share FLINT. Different derivative formulas, subdivisions, exact integer arithmetic, independent local enumeration and mpmath controls provide complementary checks. The finite spectrum's completeness and membership remain assumptions, and the complete analytic/number-field argument is not formalized in Lean. Zero-radius derivative placeholders encode zero additional error, not a claim that the derivative vanishes.

The next gate is to optimize multipliers for shared input error and compare higher-order or direct nonlinear enclosures, while addressing the remaining support coefficients and additional verified fields. Branches not advanced in this pass are carried forward with their existing questions and evidence.
