# Finite coefficient-recovery delta

The certified positive zero union for Q(zeta_5) has expanded from 528 roots through height 220 to **7602 through height 2000**. A recovery calculation using those zeros and explicit error bounds determines 89 of all 91 prime-power coefficients through 361 directly. General degree-four local constraints resolve the remaining two. A separate polynomial-factorization check agrees with all 91.

This is an evidence-backed change in finite resolution. The field invariants and analytic formula are given; the decoder does not infer an unknown field or establish a natural operator. All earlier checkpoints and original imported files are preserved.

## What the new data determine

The direct singleton counts for heights 220,600,1000,1500,2000 are **46,69,79,86,89**. After a separate inference from local degree constraints, the counts are **56,75,84,90,91**. Every target and every unresolved candidate at each height is retained in [Recovery_Audits.zip](Recovery_Audits.zip). The [compact summary](Recovery_Summary.json) includes both inference stages.

The two final direct ambiguities are 256, with candidates 0 through 4, and 361, with candidates 3 and 4. Both become 4 under the general local constraints. Those constraints use only the degree, ramification from the discriminant, and the recovered power coefficients. No specific splitting residue is supplied to the decoder.

Finite coefficient recovery still leaves **48 local splitting types ambiguous**. Their next distinguishing square powers range from 529 to 128881. The [identifiability audit](Local_Identifiability.json) records each one and a general ramification ambiguity that even the full local Euler coefficient sequence cannot distinguish. New branch R14 follows this information boundary.

## Verification and independence

The [certificate archive](Certificates.zip) and [replays](Replays.zip) contain all four factor counts and root intervals. The three Dirichlet factors use a folded completed-function contour, followed by disjoint sign brackets exhausting its count. Every sign and count is replayed at higher precision with different contour partitions; 21 selected roots use separate mpmath Hurwitz sums. The 1517 Riemann roots receive an indexed interval/count replay and three selected 90-digit mpmath comparisons. All 528 older intervals agree with the new prefix, including identical 20-decimal rounded rows. These are finite certificates, without a global GRH claim.

The recovery has 455 cases at 160 bits and 91 final cases at 224 bits. Its unknown-zero bound deliberately omits the earlier prime partial sum; all nuisance coefficients receive the universal degree-four bound. The [derivation](../../../code/frontier_verification/RECOVERY_README.md) details this noncircular dependency and the separate zero, prime, gamma and root errors. All 27 candidate width budgets are retained per case.

The [cross-method audit](Cross_Method.json) freezes the recovery before introducing polynomial-factorization coefficients. All 455 candidate sets retain the independently computed coefficient. A 70-digit mpmath implementation agrees with every final zero sum, gamma integral, finite leakage and unwidened estimate. It uses a separate prime-power inventory and quadrature implementation. Independent ordered compositions reproduce the local-model enumeration. Interval routes share FLINT/Arb; mpmath does not independently prove zero completeness.

Seven deliberate variants produce 3185 comparisons. Six error types exclude the true coefficient somewhere, totaling 1647 exclusions. Omitting the discriminant term is inconclusive in all 455 cases on this width grid; its small size here is not evidence that it can generally be omitted. The other inconclusive comparisons are retained too.

## Preserved attempts and continuation

The [23 execution receipts](Execution_Receipts.json) and [execution archive](Execution_Artifacts.zip) retain 18 successful commands and five unsuccessful attempts. Four task-owned contour attempts were stopped after wide native interval evaluations stalled and a seeded version succeeded. The initial held-out validator encountered SymPy's expression-factor sorting error on FLINT modular values; its polynomial API succeeded. Earlier source versions and planning probes are retained in the [source snapshot](Source_Snapshot.zip) and [development notes](Development_Notes.json).

[Source identities](Source_Inventory.json), [runtime](Runtime.json), [primary references](Primary_Sources.json), [manifest](Manifest.json), and [verification](Verification.json) support reproduction and recursive integrity checks. The verifier recombines recorded enclosures; it does not rerun quadrature or formalize the analytic proof.

The [queue](Research_Queue.json) now has 116 branches. The [ledger](Branch_Events.jsonl) preserves the 350-event prefix and adds five events, reaching 355. Next: coupled coefficient constraints, adaptive resolution/precision budgets, the unresolved square powers and local identifiability, alongside the existing statistical, operator, topology, physical and private-input gates. The investigation remains active, without a global completion or exhaustion claim.
