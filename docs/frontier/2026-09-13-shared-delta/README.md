# Shared ordinate error delta

Accounting for each ordinate's common effect across measurements identifies **81 of 91 coefficients** at additional radius **0.005**, up from 73. The eight new singletons are at 32, 257, 269, 271, 281, 283, 311 and 313. No additional arithmetic premise is introduced.

## The new information

The preceding calculation bounded each measurement independently. The new model uses one displacement coordinate for each of the 7602 known positive ordinates, shared across all relevant rows among the 455 retained measurements. Interval Taylor remainders certify the approximation. Signed combinations then allow errors to cancel before their absolute bounds are summed.

The [derivation and reproduction guide](../../../code/frontier_verification/SHARED_README.md) gives the full objective bound, including coefficient residuals, Taylor remainders, omitted zeros and prime tails. The coefficient-32 probe reduces its ordinate allowance from approximately 5.65 with separate row bounds to 0.74 with shared coordinates. The complete objective bound falls below one and identifies the coefficient as zero. Optimizing the old independent ranges still identifies only 73 targets, separating the new information from a change of optimizer.

The [producer archive](Shared_Audits.zip) preserves the marginal control, the two-target probe and the full shared run. The probe contains two solver time limits, each retained as an inconclusive proposal with a valid box-bound certificate. The later interior-point run completes all 48 requested solves; eight opposite box bounds need no further optimization after a singleton is established. Every multiplier is rounded to a rational, and full interval objectives decide every inference.

## Independent checks

The [audit](Shared_Audit.json) validates 36 marginal certificates and replays all 60 shared certificates at both 160 and 224 bits, with exact integer support arithmetic. It obtains identical candidate decisions. All 604 final coefficient domains retain the independently established arithmetic values from the preceding checkpoint. Seventy-five independent 80-digit cases check first and second derivatives; two complete 7602-term finite center sums verify recentering. Symbolic differentiation checks the second-derivative identity.

Three controls reject missing prerequisite coefficient bounds, omission of the Taylor remainder, and treating all ordinate displacements as one common scalar. The new model shares each ordinate's error across measurements while retaining a separate displacement for each ordinate.

The [summary](Shared_Summary.json), [execution receipts](Execution_Receipts.json), [execution artifacts](Execution_Artifacts.zip), [development notes](Development_Notes.json), [source inventory](Source_Inventory.json), [source snapshot](Source_Snapshot.zip), [runtime](Runtime.json), [primary references](Primary_Sources.json), [manifest](Manifest.json) and [verification](Verification.json) preserve the result and its provenance. All four recorded commands pass; the two limited solver trials remain explicit inside their successful probe command.

## Remaining questions

Ten targets remain unresolved: 64, 81, 125, 128, 243, 256, 289, 343, 359 and 361. Their full candidate domains are retained. Solver convergence and a round without new deletions do not prove these domains jointly feasible, an optimal uncertainty threshold or alternative number fields.

The next gate is to combine signed curvature bounds or introduce common quadratic displacements with certified cubic remainders. Noise-aware widths, linked tails, and explicit feasibility or separating certificates remain additional routes. The [queue](Research_Queue.json) retains all 116 branches; the [ledger](Branch_Events.jsonl) preserves the complete 363-event prefix and extends it to 366. Earlier operator, topology, physical, local-factor and private-input gates remain active. No global completion or exhaustion is claimed.
