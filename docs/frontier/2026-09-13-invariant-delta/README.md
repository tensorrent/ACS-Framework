# Global invariant classification delta — 13 September 2026

Degree four and absolute field discriminant 125 already determine Q(zeta_5). A source-reviewed derivation using tame inertia, finite permutation groups and Minkowski's bound identifies all 72 original prime local factors, including the 48 left ambiguous by the earlier local relaxation. No additional zero measurements are used.

The [full derivation and input audit](../../../code/frontier_verification/INVARIANT_README.md) state every arithmetic premise. The complete number-field theorem is not formally mechanized. Its finite components are checked by materially different methods:

- Generator closure and an exhaustive 130817-subset check give the same possible quartic groups. Coset actions independently verify the cubic resolvent step.
- All 32768 subsets containing the identity in C4 x C4 are considered; the four subdirect groups have orders 4,4,8,16, and the latter two force forbidden unramified quotients.
- The frozen [prior-only predictions](Invariant_Predictions.json) match all 604 retained coefficients, including 91 targets. The [independent audit](Invariant_Audit.json) checks 564 polynomial factorizations and lists the selection and missing-square prediction for each of the 48 earlier ambiguities.
- Six actual corrupted transcripts are rejected in the [adversarial replay](Invariant_Adversary.json). A quartic with the same degree and signature but discriminant 256 has a different coefficient at nine, showing why the discriminant input matters.

This changes the interpretation of the benchmark. Earlier spectral bounds, local profiles and uncertainty results remain valid for their declared deduction rules. Their survivor counts are not counts of alternative actual fields compatible with every supplied invariant. Their tested noise thresholds are not unrestricted information-theoretic identification limits.

Branch R15 asks for a benchmark whose permitted global inputs leave multiple actual fields possible. Its first gate is to certify such fields and a differing Euler observable before attributing their distinction to finite zero data. Wider-radius decoder improvements, local feasibility and the other ACS questions continue under their existing scope.

The [research queue](Research_Queue.json) preserves all 116 inherited branches and adds R15. The [event ledger](Branch_Events.jsonl) preserves the 373-event prefix and appends five events, reaching 378. This is an ongoing evidence delta, without a global completion or exhaustion claim.

Evidence and reproduction:

- [Summary](Invariant_Summary.json), [primary sources](Primary_Sources.json), [source acquisition](Source_Acquisition.json) and [visual source checks](Source_Visual_Checks.json).
- [Five command receipts](Execution_Receipts.json) and [exact streams](Execution_Artifacts.zip): four successes and one retained HTTP 406 failure from the first Python download client. Ordinary curl subsequently retrieved all six public references.
- [Source inventory](Source_Inventory.json), [source snapshot](Source_Snapshot.zip), [runtime](Runtime.json), [development notes](Development_Notes.json), [manifest](Manifest.json) and [verification](Verification.json).
- [Initial verification diagnostic](Verification_Development.json): Python tuples and JSON lists caused a direct object comparison to fail. The preserved verifier source was corrected to compare canonical serialization; the mathematical instruments and predictions are unchanged.

Run `python code/frontier_verification/verify_invariant_delta.py` from the repository root with the pinned environment. It verifies preceding checkpoints and freshly replays the new finite audits. Third-party PDFs and rendered pages are retained only in local scratch; the repository records their source URLs, hashes and locators.
