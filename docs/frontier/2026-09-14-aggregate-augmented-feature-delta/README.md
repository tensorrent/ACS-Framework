# Joint features, local uniqueness, and measurement noise — 14 September 2026

**Actual-source ambiguity survives the moment and extra kernels jointly.** Twelve certified witnesses match 18 through 21 finite measurements. A selected 22-feature extension is injective on a small neighborhood containing the smallest witnesses, yet an explicit feature error of at most 5e-18 restores ambiguity there.

The [proof and reproduction guide](../../../code/frontier_verification/AUGMENTED_FEATURE_README.md) derives the exact collisions, independent complex Taylor bounds, local injectivity and stability, and the two-stage noise contract. The [preceding checkpoint](../2026-09-14-aggregate-feature-delta/README.md) supplied the original 17-feature collision and showed that the added statistics rejected that particular witness.

- [Results and exact continuation gates](Augmented_Feature_Summary.json).
- Proposals and certificates at critical split [1e-8](Augmented_Proposals_Enlarged.json) / [certificate](Augmented_Certificate_Enlarged_v2.json), [1e-12](Augmented_Proposals_Small.json) / [certificate](Augmented_Certificate_Small_v2.json), and [1e-18](Augmented_Proposals_Local.json) / [certificate](Augmented_Certificate_Local_v2.json).
- [Independent complex Taylor, modular rank and polynomial arithmetic audit](Independent_Augmented_Audit.json).
- [Explicit noisy 22-feature common release](Feature_Noise_Boundary.json), keeping root-coordinate and feature-measurement errors separate.
- [Forty-five adversarial mutations and exact scope controls](Adversary_Audit.json).
- [Six compiled Lean lemmas](Lean_Check_v2.json), [preserved first failure](Lean_Check.json), and [proof sources/compiled artifact](Lean_Artifacts.zip).
- [Primary source acquisition](Source_Acquisition.json), [inherited primary sources](Primary_Sources.json), [runtime](Runtime.json), and [inherited inputs](Inherited_Inputs.json).
- [Thirteen recorded executions](Execution_Receipts.json), [full logs](Execution_Artifacts.zip), [development failures and corrections](Development_Notes.json), [source inventory](Source_Inventory.json), [source snapshot](Source_Snapshot.zip), [manifest](Manifest.json), and [fresh recursive verification](Verification.json).
- [All 117 research branches](Research_Queue.json) and the [443-event append-only ledger](Branch_Events.jsonl), retaining all 438 earlier events byte for byte.

The source population is complete below 19.5, selected before bounded coordinate errors, with all 22 entries and multiplicities preserved. The nested measurements consist of the original 17 finite Gaussians, the finite rational moment, center 37, a changed-width center 2, center 41, and finally center 43. No raw roots, count profile or unknown tail is silently added.

For each of 18, 19, 20 and 21 measurements, closed correction boxes of radius 1e-120 contain exact feature-equation roots at three positive critical splits. Direct real interval Jacobians at 640/896 bits and independent complex Taylor bounds at 768 bits establish self-mapping contraction. All 2,112 independent scalar source-to-observation inequalities pass. The largest split is 1e-8, giving root error radius U-1e-8 strictly below L; U-L=2e-30. Full observed root lists and interior counts still differ.

The selected 22-feature map is injective on the coordinate box of radius 1e-10 about the rational midpoint list. A uniform derivative defect at most 1/2 yields an exact rational inverse stability bound, approximately 65.66 million in the specified units. The local 21-feature witness lies inside this region, and center 43 distinguishes it by about 9.02e-18. The conclusion is local; global injectivity and optimal conditioning remain open.

An additional independent feature error of at most 5e-18 admits a common 22-feature release inside that same region: use the fixed B vector through component 21 and subtract 4.5e-18 from its final component. This is compatible with exact local injectivity because the measurement contracts differ. A 1e-18 error cannot hide this witness pair; no global noise threshold is inferred.

Exactly 456 of 604 tracked coefficients remain fixed and 148 ambiguous for the certified exact collisions and the noisy 22-feature common release. Independent arithmetic performs 1,128 factorizations and 1,208 coefficient comparisons. The six Lean lemmas cover the generic local injectivity/stability logic and scope controls; the complete calculus, interval, modular matrix and field/spectral chain is not entirely formalized in Lean.

The initial Arb/Fraction comparison failure and Lean reserved-keyword failure remain preserved beside separate corrected sources. Thirteen recorded commands include 11 successes and two failures. Eight of 16 exact-zero margin controls would be falsely negative in binary64.

Next: global identification over admissible observations, validated parameter families, sharper root/feature noise tradeoffs and stability bounds, physical acquisition/precision models, and fuller formalization. All wider ACS branches and private-input gates remain active; no global completion is claimed.
