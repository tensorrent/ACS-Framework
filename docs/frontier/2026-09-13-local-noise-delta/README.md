# Local information and wider uncertainty — 13 September 2026

General degree-four Euler relations resolve all eight coefficient domains left by the [quadratic checkpoint](../2026-09-13-quadratic-delta/README.md), identifying all 91 targets at additional ordinate radius `0.005`. This step does not require Galois structure or use of the discriminant to label ramified primes.

A separate experiment enlarges the radius to `0.01`, `0.02` and `0.03`. With Galois structure and ramification information explicitly supplied, local relations and spectral feedback identify 91, 82 and 62 targets through height 2000. At radius `0.01`, all 91 are already identified using retained measurements through height 1000. The corresponding spectral-box baselines give 38, 17 and 10 targets. The [derivation](../../../code/frontier_verification/LOCAL_NOISE_README.md) separates all four assumption sets and the contributions of local filtering and spectral feedback.

These coefficient results still leave 48 of the original 72 local factors unresolved. Identifying a finite coefficient cohort is not identification of a number field or its complete local arithmetic.

## Evidence and verification

- [Summary, assumption comparisons and remaining domains](Local_Noise_Summary.json).
- [Producer archive](Noise_Producers.zip): two wider-range runs and two local-inference runs, at 160 and 224 bits.
- [Wider-range audit](Wide_Audit.json): 10,592 exclusion replays, 560,440 strict phase brackets and twelve independent 80-digit extrema sums.
- [Local-information audit](Local_Audit.json): 133,128 local and 598 spectral exclusion replays, 64 minimum-observation certificates, eleven independent local profiles and exact symbolic Euler identities.
- [Elementary non-Galois counterexample](Local_Adversary.json): finite polynomial divisions, seven cubic evaluations, a discriminant determinant and a prime-discriminant index argument.
- [Execution receipts](Execution_Receipts.json), [logs and interruption record](Execution_Artifacts.zip), [development notes](Development_Notes.json), [source inventory](Source_Inventory.json), [source snapshots](Source_Snapshot.zip), [runtime](Runtime.json), [primary sources](Primary_Sources.json), [manifest](Manifest.json) and [integrity verification](Verification.json).

All 30 wider-range cases and all 88 local-inference cases agree across precisions. Every local inference begins with explicit previously certified domains. Every added spectral exclusion includes all 604 coefficient coordinates and all inherited error and tail bounds. Held-out arithmetic values remain in every domain.

The minimum-observation audit tests every smaller subset of the available observations. Several formerly unresolved powers need just one earlier observation; the selected witnesses at 125 and 361 each need two under the weakest profile. Their minimum cardinalities apply to the stated finite catalogue and available domain observations.

The quartic `x^4-x-1` has field discriminant `-283` and unramified residue degrees 1 and 3 at seven. It supplies a concrete counterexample to imposing a Galois profile on a general quartic. Other controls reject multiplying Euler coefficients by ramification indices and omitting prerequisite coefficient-domain restrictions.

Nine recorded commands retain seven successes, one diagnostic failure and one deliberately interrupted attempt. The first audit could not print a rational with more than 4,300 digits. The second was stopped after 453 seconds of costly fraction normalization. The successful audit adds aligned dyadic integers exactly, retaining every term; its largest common denominator is `2^422955`. Earlier source versions and terminal receipts remain available.

## Continuing gates

At radius `0.02` with both additional assumptions, nine targets remain: 269, 271, 281, 283, 289, 311, 313, 359 and 361. At `0.03`, 29 targets remain. These survivors have not been proved jointly feasible.

Noise-aware measurements, linked nonlinear errors and tails, explicit feasible or separating models, and the missing local-factor square observations remain active. No optimal uncertainty threshold, new Lean formalization, alternate-field construction or global exhaustion is claimed.

The [research queue](Research_Queue.json) retains all 116 branches. R12, R13, R14 and K04 receive fresh evidence; other branches are marked as carried forward. The [ledger](Branch_Events.jsonl) preserves the 369-event byte prefix and appends four events, reaching 373. Earlier dated packages and pinned instruments remain unchanged.
