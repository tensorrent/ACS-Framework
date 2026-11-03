# Actual field ambiguity after finite Gaussian feature release

Two actual fields with degree 4, signature (0,2), and absolute discriminant 576 can produce **the same 17 finite Gaussian features at a radius strictly below the threshold for sharing a full observed root list**. The fields and their complete 22-entry source prefixes below 19.5 are inherited from the [equal-population checkpoint](../../docs/frontier/2026-09-14-aggregate-equal-population-delta/README.md). The full-list threshold is `delta_* = (a_1-b_1)/2`, with certified bounds `[L,U]` of width `2e-30`.

The new certificate uses `r = U - 10^-6 < L`, approximately `0.5732763345123776`. Its strict improvement below L is exactly `499999999999999999999999 / 500000000000000000000000000000`. This proves a strict loss of identifying information in the stated finite feature vector. It does not determine that vector's optimal ambiguity threshold.

## Observation contract

For each field, select the complete positive source prefix below `39/2` before adding noise. Preserve all 22 entries and their multiplicities, independently perturb each coordinate by at most r, and retain every selected entry even if its noisy coordinate leaves the original window. Release only

`Phi_m(y) = 2 sum_(i=0)^21 exp(-y_i^2/25) cos(log(m) y_i)`

for `m = 2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31`, in this order. These sums are invariant under permutation. The release contains no raw root coordinates, cumulative count profile, rational moment, or contribution from unrecorded source ordinates. The input classification and finite completeness premises are inherited; arbitrary external count or contract declarations do not authenticate those premises.

This is a finite measurement contract. It is not equality of infinite explicit-formula measurements, moment-coupled observations, or tail-corrected arithmetic constraints. No old Gaussian tail budget is transferred to the new cutoff. The examples are known certified sources rather than a blinded external dataset.

## Exact construction and source bounds

Let c be the previous checkpoint's rational common midpoint-hull list. Fix epsilon=`10^-6`. Put B's critical coordinate at `c_1-epsilon` and A's critical coordinate at `c_1+epsilon`. Keep the other B coordinates at c. Choose 17 noncritical A coordinates, with zero-based indices

`0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,18,17`.

Write these A coordinates as `c_j+w_k`; keep the remaining A coordinates fixed at c. Define the 17-dimensional function `F(w)=Phi(A(w))-Phi(B)`. The target vector is explicitly `Phi(B)`, a finite analytic expression at rational B coordinates; certified numerical enclosures of all its components are stored.

High-precision Newton iteration proposes a correction center w0, whose largest absolute entry is approximately 0.1181217389510032, and a numerical inverse Jacobian. The exported 140-digit decimals are then interpreted as **exact rational numbers**, not trusted as already exact solutions. The rational matrix R need only be nonsingular and give the verified bounds below. QR and Newton are proposal methods, not proof steps.

Use the closed correction box `X={w: ||w-w0||_infinity <= rho}`, with `rho=10^-100`. For each observed coordinate box `[olo,ohi]` and certified true source box `[slo,shi]`, the independent audit checks

`shi-r <= olo <= ohi <= slo+r`.

These inequalities guarantee `|observed-true|<=r` for **every** true source value in its enclosure and every observed value in its certified box. Both nominal 160/224 source files are checked: 88 root-box inclusions, or 176 scalar boundary inequalities. Four critical-coordinate margins are exactly zero. Recomputing them in binary64 gives approximately `-1.11e-16`; those apparent violations are rounding artifacts, not reasons to weaken the exact bound. The observed boxes are strictly ordered and preserve all entries.

## Closed-box existence proof

Set `T(w)=w-RF(w)`. For each row i, the producer bounds

`e_i = |(R F(w0))_i|`, and `q_i >= sup_(w in X) sum_j |(I-R J_F(w))_(i,j)|`.

It proves `max_i q_i < 1` and `e_i + rho*q_i < rho` for all 17 rows. The line segment between any two points of X stays in X. The fundamental theorem of calculus applied to each component of T therefore makes T Lipschitz in the supremum norm with constant `q=max_i q_i<1`. Comparing T(w) with T(w0) gives `|T(w)_i-w0_i| <= e_i+rho*q_i < rho`, so T maps X into itself.

The nonempty closed box X is complete. Banach's theorem yields a unique fixed point of T in X. Since R is nonsingular, `w*=T(w*)` implies `F(w*)=0`. This yields exact equality of the 17 features, rather than a merely small residual. Banach's complete-subset form is the theorem used by the [mathlib implementation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Topology/MetricSpace/Contracting.html#ContractingWith.exists_fixedPoint'). The pinned local module is additionally verified against its git object and recorded by hash.

The rational coordinate inclusions apply to w*, so both actual fields realize the common feature vector within radius r. Their full observed point lists differ: the second coordinates are separated by `2*epsilon`, and the lists stay strictly ordered. An interior count at the preceding rational gate is 1 for A and 2 for B. This is consistent with `r<L`, where a full-point-list decoder can distinguish the fields.

## Independent routes and arithmetic consequences

The producer evaluates the real trigonometric Jacobian over the full box with Arb at 512 and 768 bits. The largest derivative-error row bound is approximately `4.63212e-93`. Repeating precision is a useful numerical cross-check but is not an independent implementation.

The independent auditor writes each feature as `2 Re exp(-a*x^2+i*u*x)`. It evaluates F and its first derivatives at the rational center, then bounds Jacobian variation using the second derivative over each coordinate interval. Symbolic differentiation separately verifies

`g''(x)=2 exp(-a*x^2) ((4*a^2*x^2-2*a-u^2) cos(u*x)+4*a*u*x*sin(u*x))`.

If `M_kj` bounds the absolute second derivative of feature k at variable j, the alternate row bound is

`q_i <= sum_j |(I-RJ(w0))_ij| + rho*sum_k |R_ik| sum_j M_kj`.

This suffices because each Jacobian column depends only on its own coordinate. The auditor checks the resulting self-map inequalities using scalar loops and complex ball arithmetic at 640 bits. It proves rational nonsingularity by a different method: all denominators of R are invertible modulo the trial-divided prime 65537, and Gaussian elimination gives determinant **37610 modulo 65537**, which is nonzero. The earlier epsilon=`10^-12` certificate is also independently replayed; its modular determinant is 10497.

Both formulations share FLINT's real/complex ball arithmetic and inherited source spectra. Their formulas, variation bounds, matrix operations and nonsingularity proofs differ. Arithmetic enclosures can widen because of dependency effects, so a failed interval test alone would not prove nonexistence. The [Arb author's usage guide](https://fredrikj.net/arb/using.html) explains enclosure interpretation and that limitation; the actual runtime and source hashes are pinned separately.

The metadata classification admits only these two actual fields. Both realize the fixed common feature vector, so its coefficient domains are exact within that class: **456 of 604 tracked coefficients remain fixed, and 148 are ambiguous**, including targets 3,7,19,27,31. Independent modular polynomial factorization reconstructs both 604-value vectors with 1,128 factorizations away from the chosen order indices. The 17-feature collision is not a sufficient basis for choosing one of those two arithmetic vectors.

## Observables that distinguish this witness

The release contract matters. In addition to the interior counts 1 and 2, three omitted statistics are rigorously different throughout the A correction box versus the fixed B observation:

- The finite rational moment `sum 3/(9/4+y_i^2)` has A-minus-B value approximately `-0.0003169819125874793`.
- The same-width Gaussian feature at center 37 differs by approximately `3.1810488540584535e-5`.
- The center-2 Gaussian feature with width parameter `1/24` differs by approximately `-2.306291393403567e-6`.

All three difference enclosures exclude zero at two precisions. Thus adding one of these measurements rejects **this particular collision witness**. It does not prove that an augmented feature vector identifies the field uniformly: a different collision may satisfy the extra equation. That is an explicit next gate, along with identifying sharper radii and the effect of increasing the number of released features.

## Adversaries, failures and formal scope

Thirty-five semantic mutations reject missing features, wrong widths or critical coordinates, corrupted source data, changed release contracts, singular/inadequate preconditioners, off-root centers, missing coordinate checks and false self-map reports. Exact counterexamples show why a tiny constant residual need not have a root and why a singular preconditioner can create fixed points without zeros of F.

The original local Newton export applied its correction twice when reporting its residual and inverse Jacobian. A separate complex-exponential audit rejects both reported quantities, while accepting the separately corrected source. Both sources and results remain preserved. The larger epsilon=`5e-6` Newton attempt encounters a numerically singular Jacobian; this is a failed local proposal, not evidence of global nonexistence. The uninformative binary64 optimization attempts, with residuals but no certified conclusion, are retained as proposals.

Six lemmas in the [canonical Lean source](proofs/FeatureContraction_v2.lean) cover uniform interval errors, the self-map center criterion, injective preconditioning, Banach root existence on a complete set, strict radius improvement and equality of features. They compile without `sorryAx`. The first attempt lacked a compiled dependency; after acquiring that exact pinned module, the same source exposed an out-of-scope nonnegative-real notation. The separate v2 writes `NNReal` explicitly. A separate launcher typo failed before running an audit; its manual tool-failure record is distinguished from runner-generated receipts.

The numerical Jacobian/row-norm bridge, finite-dimensional calculus, modular-determinant interpretation, complete field classification and analytic source completeness retain their written/computational proof scopes. Those parts are not claimed as a single fully formalized Lean theorem. The successful generic Banach lemma nevertheless checks the central logical step from an injectively preconditioned contraction to an exact zero.

## Reproduction and continuation

The [dated evidence package](../../docs/frontier/2026-09-14-aggregate-feature-delta/README.md) preserves proposals, both existence routes, arithmetic domains, additional-observable boundaries, failed attempts, runtime acquisition, sources, receipts and append-only research history. The canonical verifier freshly repeats the new science and Lean check before recursively verifying the preceding checkpoints:

```sh
../acs-research/.venv/bin/python code/frontier_verification/verify_aggregate_feature_delta.py
```

Next, use validated continuation or different slices to improve the finite-feature radius, test joint release of the moment or additional kernels, and audit how feature count and Jacobian rank affect local information. Keep exact root existence distinct from solver convergence and local uniqueness distinct from global identifiability. The wider ACS questions about natural operators, infinite arithmetic and real-part information, topology, physical interpretation, formalization and private inputs remain active; no global exhaustion is claimed.
