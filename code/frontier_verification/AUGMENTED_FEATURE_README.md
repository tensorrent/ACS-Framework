# Joint observables, local uniqueness, and measurement precision

The [checkpoint evidence](../../docs/frontier/2026-09-14-aggregate-augmented-feature-delta/README.md) proves three related results. The moment and extra kernels that distinguished the preceding witness can all be matched by a different actual-source witness. Twenty-two selected features are injective on a specific small neighborhood containing a 21-feature collision. Adding a bounded feature-measurement error restores ambiguity even within that neighborhood.

## Source and observation contracts

The inherited complete metadata class consists of A = Q(sqrt(2), sqrt(-3)) and B = Q(sqrt(-2), sqrt(-3)), both degree four, signature (0,2), and absolute discriminant 576. Each complete positive source prefix below 39/2 has 22 entries. Select these entries **before** independent bounded root-coordinate errors; preserve all entries and multiplicities. Source classification, root completeness and both 160/224-bit input versions are inherited and recursively verified. This is a certified benchmark, not an independently acquired anonymous dataset.

The first 17 components are finite sums

`Phi_m(y) = 2 sum_i exp(-y_i^2/25) cos(log(m) y_i)`

at centers 2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29 and 31. Extend this ordered vector by:

1. The finite rational moment `sum_i 3/(9/4+y_i^2)` (18 components).
2. The same-width Gaussian at center 37 (19 components).
3. The center-2 Gaussian with width parameter 1/24 (20 components).
4. The same-width Gaussian at center 41 (21 components).
5. The same-width Gaussian at center 43 (22 components).

No raw root vector, count profile, unknown-tail term or infinite explicit-formula value is released. The finite moment does not implicitly include its infinite tail. Each Gaussian has normalization 2; the moment has numerator 3. All claims use these precisely specified component units.

## Exact collisions survive joint additions

Let c be the preceding rational common midpoint vector. The second positive root is the critical coordinate, index 1. Set A's observed critical coordinate to `c_1+epsilon` and B's to `c_1-epsilon`. Leave all other B coordinates at c. For n in 18, 19, 20 and 21, choose n noncritical A coordinates and solve the n feature-equality equations by adjusting those coordinates.

There are 12 certified constructions: each n at epsilon = 1e-8, 1e-12 and 1e-18. The common root-coordinate error radius is `r=U-epsilon`, where the inherited full-list threshold lies between rational bounds L and U with `U-L=2e-30`. Thus every construction has `r<L`. The largest split gives `r` approximately 0.5732773245123776; its 21-variable correction has maximum magnitude about 0.02022173464. The smallest split gives a strict improvement `1e-18-2e-30`; a binary64 display cannot resolve that radius difference reliably.

Newton at 220 decimal digits proposes centers and inverse matrices. The exported 170-digit entries are thereafter **exact rational numbers**. Numerical convergence alone is not a certificate. For each construction, the correction box has radius rho = 1e-120. Write F(w) for the difference of the released feature vectors and T(w)=w-RF(w). Real Arb interval Jacobians at 640 and 896 bits prove, row by row,

`q_i >= sup_X sum_j |(I-R J_F)_{ij}|`, `q_i<1`,

`|(R F(w0))_i| + rho*q_i < rho`.

The box is convex and complete. The derivative estimate makes T a contraction there, and the center estimate makes it map the box into itself. Banach gives a fixed point; the certified nonsingularity of R then gives F=0. The fixed point is unique within this particular correction box and slice, not globally.

The coordinate checks are uniform over every true root in each inherited source interval and every observation in the correction box. The producer checks the maximum endpoint distance; the independent audit reconstructs the equivalent two inequalities

`source_hi-r <= observed_lo`, `observed_hi <= source_lo+r`.

Across 12 witnesses there are 1,056 root-box checks and 2,112 scalar inequalities. Every observed list stays ordered, and its interior counts at c_1 are A=1 and B=2. The equal finite moment and Gaussian features therefore do not imply equal full observations or counts.

## Independent analytic and arithmetic route

The second route uses `2 Re exp(-a*x^2+i*u*x)`. Its first and second derivatives are reconstructed with complex arithmetic, and symbolic differentiation checks both formulas. The rational moment derivatives are independently checked as

`M'(x)=-6*x/(9/4+x^2)^2`,

`M''(x)=6*(3*x^2-9/4)/(9/4+x^2)^3`.

At the rational center, form J0. Each Jacobian column depends only on its own root coordinate. If M_kj bounds the absolute second derivative on its coordinate interval, scalar loops prove

`q_i <= sum_j |(I-R J0)_ij| + rho * sum_k |R_ik| sum_j M_kj`.

This independently supplies the contraction and self-map bounds at 768 bits. Rational Gaussian elimination modulo the explicitly trial-divided prime 65537 proves nonsingularity, with every denominator invertible modulo that prime. Both analytic routes still share FLINT; they are different formulations, not independent software stacks.

Independent integral-polynomial arithmetic performs 1,128 factorizations and 1,208 coefficient comparisons. For each exact collision, precisely 456 of 604 tracked coefficients are fixed and 148 are ambiguous in the complete two-field class. This remains true after jointly including the finite moment and all additions through center 41.

## A local 22-feature uniqueness and stability result

The chosen noncritical Jacobian minors at c have ranks 18 through 21. The full 22-by-22 Jacobian has a rational approximate inverse R, whose modular determinant is 62994 modulo 65537. On the closed coordinate box `Q={x: ||x-c||_infinity <= 1e-10}`, both methods prove the uniform bound

`||I-R J_Phi(x)||_infinity <= 1/2`.

The direct interval bound is about 0.08834; the independent complex Taylor bound is about 0.05680. These are sufficient upper bounds, not exact suprema. Larger tested boxes are retained; failure of a sufficient bound does not establish noninjectivity.

For x,y in Q, their segment remains in Q. Apply the fundamental theorem of calculus to each component of `G(x)=x-R Phi(x)`, then the row-sum bound and triangle inequality. This yields

`||(x-y)-R(Phi(x)-Phi(y))||_infinity <= (1/2)||x-y||_infinity`.

Consequently Phi is injective on Q and

`||x-y||_infinity <= 2||R||_infinity ||Phi(x)-Phi(y)||_infinity`.

The exact rational constant is stored; its value is about 65,659,927.01. This is a bound in the specified feature units. It does not assert good numerical conditioning or a physical instrument's precision. The derivative-to-Lipschitz step is also described by the [primary Mathlib mean-value documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/Calculus/MeanValue.html); exact pinned source files are archived separately from that current web page.

The epsilon=1e-18 witnesses all lie in Q. In particular, the 21-feature witness has maximum distance from c about 1.97e-12, but its center-43 feature differs by approximately -9.01926321168e-18. Thus these particular 21 features are not injective even within Q, while their 22-component extension is injective there. This does not prove a universal feature-count minimum or global identifiability over the full feasible observation region.

## Explicit measurement-noise ambiguity

Now add a second observation stage: each released feature may have an independent absolute measurement error at most tau. This is distinct from the earlier root-coordinate error radius r.

Use the local 21-feature collision, and set tau = 5e-18. Define the common released vector z to equal B's exact first 21 feature values, and set its last component to B's exact center-43 feature minus 4.5e-18. The first 21 feature errors are exactly zero for both fields. Real trigonometric and complex exponential evaluations at 640 and 896 bits bound the final errors strictly below tau for every A observation in the certified correction box. Hence both actual fields admit this same noisy 22-feature release inside Q; 148 tracked arithmetic coefficients remain ambiguous.

There is no conflict with exact injectivity: the exact 22-feature vectors are different. The final-feature separation exceeds 2e-18, so tau=1e-18 cannot hide **this witness pair**, by the triangle inequality. That exclusion does not apply to all possible pairs. For a fixed exact pair with identical first 21 components, the sharp independent component-error threshold is half its last-component difference, as follows from the triangle inequality and the componentwise midpoint construction. The interval evidence encloses that difference; it does not establish the optimal threshold over all admissible field observations.

## Audits, formal scope, and next gates

Forty-five mutations test joint feature definitions, source metadata and multiplicity, coordinate boxes, self-map reports, nonsingularity, rank, local neighborhoods and stability constants. Sixteen exact-zero coordinate margins are retained; eight become falsely negative in binary64. A square-map example has a small derivative defect on [3/4,5/4] but collides at -1 and 1 globally, preventing a local-to-global inference.

Six Lean lemmas check local injectivity from the defect inequality, the half-defect stability consequence, the remaining-feature gap, prefix versus extension equality, and the local/global control. The full vector mean-value/row-norm derivation, interval implementation, modular matrix interpretation and inherited field/spectral premises remain written or computational, rather than entirely formalized in Lean.

The first certificate run failed because Arb does not directly compare to Python Fraction; the separate v2 uses an Arb enclosure for 1/2. The first Lean source used the reserved word `prefix` as a binder; the separate v2 renames it. Both failed sources and their actual receipts are preserved. Thirteen recorded commands comprise 11 successes and two failures; the final recursive verifier has its own subsequent receipt.

Next: prove or refute global injectivity over the admissible observation sets; improve local neighborhoods and quantitative stability bounds; validate parameterized collision families and the tradeoff between root-coordinate and feature-measurement errors; test physical precision/acquisition assumptions; and formalize the remaining calculus and arithmetic bridges. The full 117-branch ACS program and private-input gates remain active.

## Reproduction

From the repository, with the existing pinned Python and Lean runtimes, run:

```sh
../acs-research/.venv/bin/python code/frontier_verification/verify_aggregate_augmented_feature_delta.py
```

The verifier regenerates every proposal and certificate, independently audits all 12 witnesses and the noise boundary, reruns the adversaries, recompiles the canonical Lean source, checks immutable sources and receipts, and recursively verifies preceding checkpoints.
