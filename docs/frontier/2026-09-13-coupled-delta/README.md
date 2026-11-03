# Coupled spectral-recovery delta

All 91 prime-power coefficients through 361 can now be recovered at **height 600**, using 1822 certified positive zeros and only coefficient integrality and the universal degree-four bounds. A second method using validated linear-programming certificates confirms the result. The previous pass needed height 2000 and a local arithmetic step for its two remaining direct ambiguities.

At height 220, the new bounds identify 89 target coefficients. The two remaining target pairs both have explicit feasible integer models for the retained inequalities. Adding one previously established general prime/square relation resolves this ambiguity and identifies all 91 targets at height 220. These inference scopes are kept separate.

## Evidence and methods

The [measurement archive](Measurements.zip) extracts only observed terms and certified root intervals from the immutable prior checkpoint. Every coefficient through 4096 starts in the same domain 0 through 4. No inferred coefficient, local model or polynomial validation value seeds the main algorithms.

The [coupled audits](Coupled_Audits.zip) retain two precision runs across five heights, every elimination witness, and fourteen added-uncertainty cases. Positive measurement weights allow each newly justified exclusion to constrain other measurements. The [dual archive](Dual_Audits.zip) supplies a separate continuous relaxation, rational multipliers and integer tightening. The [derivation](../../../code/frontier_verification/COUPLED_README.md) explains both proofs and their shared analytic premises.

The [exact audit](Exact_Audit.json) replays 8601 exclusions and 970 dual certificates after outward rounding to a fixed dyadic grid, using integer arithmetic. Independent polynomial factorization checks every retained coefficient domain. Four deliberate errors test prerequisites, true-coefficient deletion, multiplier signs and the residual correction. All are rejected.

## A verified information boundary

At height 220, the interval-exclusion method identifies 78 targets; iterated dual bounds identify 89. [Six separating certificates](Target_Branches.json) eliminate six of the eight remaining target pairs. [Two integer witnesses](Integer_Witnesses.json) satisfy every measurement inequality with different values at 359 and 361, confirmed by the [exact branch audit](Branch_Audit.json). Thus the retained coefficient-box relaxation cannot distinguish `(0,4)` from `(1,1)` at those two targets. These witnesses are not alternative number fields or zero spectra.

The [optional local bridge](Local_Bridge.json) uses the already inferred zero coefficient at 19 and the general degree-four prime/square relation. It forces the square coefficient at 361 to four; the checked pair exclusions force the coefficient at 359 to zero. This yields all 91 targets at height 220 with that additional local information.

## Uncertainty and next gates

At heights 1000 and 2000, all 91 targets remain identified when each certified ordinate interval is enlarged by every tested additional radius from 5e-21 through 5e-6. At 5e-4, the current conservative method identifies 67 and 55 respectively. All unresolved candidates remain recorded. The two heights use different widths and the error estimate grows with the number of included roots; this is not an intrinsic disadvantage of more data or an optimal precision threshold. The [summary](Coupled_Summary.json) records the full comparison.

All eleven recorded computation commands succeeded. Seven preliminary alternative-pair trials with fixed nuisance coefficients failed to certify feasibility and are preserved inside the exact audit; free-nuisance integer witnesses subsequently established the stated ambiguity. [Receipts](Execution_Receipts.json), [execution artifacts](Execution_Artifacts.zip), [sources](Source_Inventory.json), [source snapshot](Source_Snapshot.zip), [runtime](Runtime.json), [primary references](Primary_Sources.json), [manifest](Manifest.json) and [verification](Verification.json) preserve provenance.

The [queue](Research_Queue.json) retains 116 branches and the [ledger](Branch_Events.jsonl) extends the unchanged 355-event prefix to 360. Next: sharper per-root uncertainty bounds, noise-aware measurements, linked tail constraints, and the still unresolved local-factor square powers. The original through-361 cohort retains 48 local-factor ambiguities. Statistical, operator, physical, topology and private-input gates remain active. No global completion or exhaustion is claimed.
