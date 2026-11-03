# Moving feature midpoints tighten the local noise threshold — 14 September 2026

**Four exact variable-noise pairs improve the ambiguity upper endpoint to approximately 1.831989439894397e-10.** Under the unchanged radius-0.01 observation contract, the inherited uniform identification guarantee remains approximately 1.768500052962292e-10. Their ratio is about 1.03590013, leaving roughly a 3.6% gap. The convenient rational budget 1.832e-10 also supports the strongest pair.

The [proof and reproduction guide](../../../code/frontier_verification/VARIABLE_NOISE_README.md) derives the mixed root/noise equations, interval existence proofs, moving midpoint budgets and exact scope. The [preceding checkpoint](../2026-09-14-aggregate-weighted-feature-delta/README.md) established larger uniqueness regions, componentwise stability and the original two-sided noise bounds.

- [Results and continuation gates](Variable_Noise_Summary.json).
- Original [boundary-pair proposals](Boundary_Pair_Proposals.json) and [exploratory interval checks](Boundary_Pair_Checks.json), followed by [shifted proposals with accepted and rejected trials](Shifted_Pair_Proposals.json) and [exploratory checks](Shifted_Pair_Checks.json).
- [Four canonical variable-noise certificates](Variable_Noise_Certificate.json) and [independent complex/source/arithmetic audit](Independent_Variable_Noise_Audit.json).
- [Sixty-four adversarial mutations and exact controls](Adversary_Audit.json).
- [Six compiled Lean lemmas](Lean_Check.json) and [proof source/compiled artifact](Lean_Artifacts.zip).
- [Primary source acquisition](Source_Acquisition.json), [inherited primary sources](Primary_Sources.json), [runtime](Runtime.json) and [inherited inputs](Inherited_Inputs.json).
- [Ten command receipts](Execution_Receipts.json), [full logs](Execution_Artifacts.zip), [preserved failure and rejected trial](Development_Notes.json), [source inventory](Source_Inventory.json), [source snapshot](Source_Snapshot.zip), [manifest](Manifest.json) and [fresh recursive verification](Verification.json).
- [All 117 research branches](Research_Queue.json) and the [453-event append-only ledger](Branch_Events.jsonl), retaining all 448 earlier events byte for byte.

The complete inherited class has two discriminant-576 quartic fields, each with 22 positive source roots below 19.5. Source selection precedes independent root errors and preserves all entries. Root error remains r=U-1e-8<L, observations stay inside the same standard coordinate cube of radius 0.01, and the 22 finite feature definitions and absolute error units are unchanged. No raw roots, counts, infinite moment or unknown tail is added.

Fix both critical roots just inside their source bounds and all B roots as rationals. Solve for 21 A root corrections and alpha=tau/1e-10. The final Jacobian column is the exact constant -2e-10*v with zero variation. Real interval Jacobians at 768/1024 bits and independent complex second derivatives at 896/1152 bits prove self-mapping contraction on variable boxes of radius 1e-120. The tau radius is scaled by 1e-10. Modular nonsingularity and all 704 direct scalar source inequalities pass.

At each exact solution, Phi(A)-Phi(B)=2*tau*v. Its feature midpoint is a common report with each component error exactly tau. Every new midpoint differs certifiably from Phi(c); the strongest differs in component 0 by about -0.0048814. The preceding failures for fixed Phi(c) target pairs therefore do not exclude these constructions. Each fixed pair has a sharp budget tau, while the globally optimal restricted threshold remains open.

The corrected common-shift search accepts eight steps among nine trials. Its last full step has a smaller numerical tau but escapes the certified cube by about 1.4599e-6, so it is rejected. The smaller accepted step is fully certified with cube margin about 2.26229e-9. The first search version's numerically singular Newton failure, source and actual receipt are preserved; a separate v2 adds prediction and backtracking. Ten development commands contain nine successes and one failure.

Independent arithmetic performs 1128 polynomial factorizations and 1208 comparisons: 456 of 604 coefficients remain fixed and 148 ambiguous at each common report. The inherited lower guarantee still identifies the field and tracked vector under its stated conditions. An arbitrary-report decoder and global recovery theorem are not established.

Sixty-four adversaries test scale, mixed-variable dimensions, fixed coordinates, source and region constraints, interval evidence and midpoint claims. Six Lean lemmas prove the generic scaling, midpoint, budget and scope logic. The full analytic/interval/modular and field/spectral chain is not entirely formalized. Both analytic routes share FLINT; no runtime version changed and no new source roots were computed.

Next: source-constrained or subdivided lower bounds, improved upper constructions, validated parameter families, bounded-error inverse decoding and global region extensions or counterexamples. Natural operators, infinite arithmetic and real-part information, topology, physical acquisition and private-input gates remain active. No global completion is claimed.
