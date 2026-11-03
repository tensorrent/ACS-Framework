# Quadratic ordinate-error delta — 13 September 2026

This pass advances the finite spectral coefficient calculation from 81 to **83 of 91 identified coefficients** at additional ordinate radius `0.005`. Coefficients 289 and 359 are now certified zero. Candidate sets narrow from `0..3` to `0..2` at 128, from `0..4` to `1..4` at 256, and from `2..4` to `3..4` at 361.

All 455 previously retained measurements and 7602 certified positive ordinates remain in use. The initial domains are the [preceding shared-error results](../2026-09-13-shared-delta/README.md), without adding arithmetic oracle values to inference. The new model retains a common quadratic term for each ordinate and encloses the omitted terms by an interval cubic remainder.

The [derivation and reproduction guide](../../../code/frontier_verification/QUADRATIC_README.md) gives the full signed-combination inequality, interval endpoint choices, prime and zero tails, residual support over all 604 coefficient coordinates, and the exact scalar maximum. The independent-square control also reaches 83. The exact square relation tightens individual bounds but produces no additional singleton with these proposals. The two conic probes add no singleton beyond the LP run.

## Retained evidence

- [Summary and all remaining target domains](Quadratic_Summary.json).
- [Five producer transcripts](Quadratic_Audits.zip): frozen prior multipliers, optimized LP proposals, 30- and 120-second conic probes, and their combined proposal closure.
- [Exact integer and two-precision audit](Quadratic_Audit.json): 2,392 certificate evaluations across 32 replay stages, including all three error models. Interval and exact integer decisions agree; all 604 independently established arithmetic coefficients survive.
- [Independent numerical audit](Quadratic_Numeric2.json): symbolic third derivative, 75 high-precision curvature/derivative cases, two complete 7602-term displaced sums, and an exact rational scalar-maximum check.
- [Lean kernel result](Lean_Check.json) and [ten scalar theorems](../../../code/frontier_verification/proofs/QuadraticSupport.lean): maximum bounds and attainment, signed interval reduction, and cone geometry. These formal statements do not cover the numerical Taylor calculation or coefficient recovery.
- [Execution receipts](Execution_Receipts.json), [logs, failed attempts and compiled proof artifact](Execution_Artifacts.zip), and [development notes](Development_Notes.json).
- [Runtime versions](Runtime.json), [primary source mapping](Primary_Sources.json), [source inventory](Source_Inventory.json), [source snapshots](Source_Snapshot.zip), [manifest](Manifest.json), and [retained-evidence verification](Verification.json).

The main LP run records 50 successful solves and two existing opposite bounds over three rounds. The two conic probes retain two time-limit statuses, one `AlmostSolved`, and five `Solved` statuses. Any finite proposed multipliers are checked independently; solver status and unverified primal coordinates establish neither feasibility nor optimality.

Four of fourteen recorded commands fail and are preserved. Three Lean attempts expose a project-root problem, an uncached umbrella import, and an unfinished positivity proof. Their corrected successor compiles all ten theorems without `sorryAx`. The first independent numerical audit contains a missing square in its scalar comparison; a retained diagnostic verifies the certificate by exact arithmetic, and the corrected full audit passes. A separate command-launch failure occurs before the program starts and is retained outside the normal receipt set.

Two complete allowed displacement vectors produce strictly positive residuals beyond the quadratic prediction, while remaining inside the certified cubic allowance. This rejects omission of the cubic remainder. A scalar interior vertex exceeds both endpoints and zero, rejecting an endpoints-only maximum. A separate integer control shows why preceding coefficient-domain bounds remain necessary. These counterchecks address the mathematical model; none asserts an alternate number-field spectrum.

An initial packaging attempt named `lakefile.lean` where the existing Lean project uses `lakefile.toml`. The failed packager source and failure record are retained; the corrected package includes the actual project configuration.

## Remaining gates

Eight target domains remain unresolved: 64, 81, 125, 128, 243, 256, 343 and 361. Their survival is not a certificate of joint feasibility. Further measurement widths chosen for this uncertainty, tighter signed nonlinear sums, linked tails and explicit feasible or separating witnesses remain actionable. The conic primal proposals could inform a future witness search only after independent validation of every required constraint.

The [research queue](Research_Queue.json) carries all 116 branches forward. R12, R13 and K04 receive new evidence; the other branches are explicitly marked as carried forward, not freshly audited. The [hash-linked ledger](Branch_Events.jsonl) preserves the preceding 366-event byte prefix and adds three events, reaching 369. Earlier dated packages and their pinned instruments remain unchanged.

This is a scoped research delta. The original unresolved local-factor observations, operator and real-part bridges, calibration, topology, physical identifications and private inputs keep their prior gates. No global completion, optimal uncertainty threshold or exhaustion is asserted.
