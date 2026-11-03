# Ordinate uncertainty delta

All 91 target prime-power coefficients remain recoverable after each certified ordinate interval is enlarged by **±0.0005**, at every tested height from 600 through 2000. Three sharper finite-sum bounds agree on this result. The preceding global bound recovered only 55 targets at height 2000 with the same declared uncertainty.

At the larger radius **0.005**, retaining measurements from earlier cutoffs gives **73 of 91** target coefficients. The remaining 18 candidate domains are recorded explicitly. These are sufficient recovery bounds for the declared uncertainty model, not optimal noise thresholds.

## What changed

The [derivation and reproduction guide](../../../code/frontier_verification/ORDINATE_README.md) supplies three replacements for the coarse all-roots derivative allowance: individual derivative bounds, direct interval evaluation of each Gaussian, and scalar minimum/maximum bounds from endpoints and all enclosed turning points. A strictly increasing phase identifies every possible turning point. Interval contraction encloses it, and separate strict phase brackets verify its existence and uniqueness.

All methods share the inherited finite root certificates, explicit formula, field invariants and unconditional omitted-zero and prime-tail bounds. The moment bound is recomputed on enlarged intervals. No local arithmetic relation or expected coefficient seeds recovery. Ordinate enlargement models loss of precision around certified data with fixed cutoff membership; it does not assert that arbitrarily shifted ordinates belong to a number field.

The retained-prefix policy shares coefficient domains across all measurements at the tested lower cutoffs. At radius 0.0005, it improves the old global method from 55 to 78 targets at height 2000. At radius 0.005, the stationary method improves from 66 with the final cutoff alone to 73 with retained measurements. Adding constraints preserves every previously justified exclusion.

## Verification and evidence

The [producer archive](Ordinate_Audits.zip) retains the initial 40-case probe and both 160-case grids: four bounds, five cutoffs, four uncertainty radii and two retention policies, at 160 and 224 bits. The two precision runs have identical final coefficient domains. Every exclusion includes its measurement, strict gap and prerequisite-domain hashes.

The [independent audit](Ordinate_Audit.json) replays 119,400 deletions with exact integers after outward rounding to a fixed dyadic grid. Polynomial factorization is held out until the producer results are frozen and checks all 604 coefficient domains in every case. All 57,691 reported Gaussian turning-point enclosures receive strict phase-bracket checks. Twelve independent 80-digit mpmath calculations verify scalar finite-sum extrema for targets 2, 11 and 361, at two heights and two radii. Three controls reject missing prerequisites, a false deletion of the true coefficient, and omission of an interior extremum. All four recorded commands passed.

The [summary](Ordinate_Summary.json) contains every result and unresolved target domain. [Execution receipts](Execution_Receipts.json), [execution artifacts](Execution_Artifacts.zip), [development notes](Development_Notes.json), [source inventory](Source_Inventory.json), [source snapshot](Source_Snapshot.zip), [runtime](Runtime.json), [primary references](Primary_Sources.json), [manifest](Manifest.json) and [retained-evidence verification](Verification.json) preserve provenance. The first integrity check encountered a [packaging-order failure](Verification_Bootstrap_Failure.json): its final output path did not yet exist. Re-running the unchanged verifier with its output at that path resolves the link check. Inputs are byte-identical to the preceding [measurement archive](../2026-09-13-coupled-delta/Measurements.zip); no additional finite root certification is claimed in this pass.

## Next questions

The scalar ranges account for extrema within each independent ordinate box, but different Gaussian measurements depend on the same uncertain ordinates. Combining marginal ranges discards those correlations. The next step is to certify combinations that retain common-ordinate errors and choose widths using the declared uncertainty. The 18 wider-radius survivors are not yet proved jointly feasible, so their existence does not establish nonidentifiability.

The [research queue](Research_Queue.json) retains all 116 branches, advancing R12, R13 and K04. The [ledger](Branch_Events.jsonl) preserves the complete 360-event prefix and adds three scoped events, reaching 363. The original local-factor, statistical, operator, topology, physical and private-input gates remain active. This is an ongoing delta, without global completion or exhaustion.
