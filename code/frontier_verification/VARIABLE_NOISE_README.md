# Moving feature midpoints tighten the local noise threshold

The [checkpoint evidence](../../docs/frontier/2026-09-14-aggregate-variable-noise-delta/README.md) improves the ambiguity upper bound from 2e-10 to an exact rational endpoint approximately 1.831989439894397e-10 under the same radius-0.01 observation contract. The inherited uniform identification guarantee is approximately 1.768500052962292e-10. Their ratio is about 1.03590013, leaving a roughly 3.6% gap. The exact threshold remains open.

## What is held fixed

The inherited complete metadata class consists of A=Q(sqrt(2),sqrt(-3)) and B=Q(sqrt(-2),sqrt(-3)), degree four, signature (0,2), absolute discriminant 576. Each complete positive source prefix below 39/2 has 22 entries. Selection precedes independent absolute root-coordinate errors, preserving every entry and multiplicity. The source and field premises remain linked to their original evidence and are recursively verified.

The root error radius remains `r=U-1e-8<L`, with `U-L=2e-30`. Every observation belongs to the standard coordinate cube `Q={y: max_i |y_i-c_i|<=0.01}` about the same rational midpoint vector c. The feature map Phi contains the preceding ordered 22 finite kernels: 17 Gaussian sums, the finite rational moment, center 37, width-1/24 center 2, center 41, and center 43. Exact definitions and units remain in the certificates. No raw root list, cumulative count, infinite moment or unknown tail is included.

Additional feature errors are independent absolute component errors in these stated units. Both fields must be able to produce the same report within that error budget. The existing lower guarantee applies uniformly over source-feasible observations in Q. This pass changes the search for a feasible common report; it does not enlarge Q, alter the root error or change the features.

## A variable noise equation

Set `epsilon=1e-8+1e-16`. Fix `A_1=c_1+epsilon` and `B_1=c_1-epsilon`, where index 1 is the second positive root. The additional 1e-16 gives strict source-feasibility room. All other B coordinates are fixed exact rationals. Let I list the other 21 indices, and write `A_i=c_i+w_i` for i in I.

The unknown vector has 22 components: 21 A corrections and `alpha=tau/s`, where `s=1e-10`. It does not have 22 root unknowns. Let v be the inherited critical inverse-row sign vector, whose 22 entries are all +1 or -1. Solve

`F_k(w,alpha) = Phi_k(A(w))-Phi_k(B)-2*s*alpha*v_k = 0`.

The first 21 Jacobian columns are the corresponding A kernel derivatives. The final column is the exact constant `-2*s*v`. Its derivative variation is zero. Keeping this scale explicit is essential: a box radius for alpha becomes a radius multiplied by s for tau.

At each rational proposed center, the exact rational preconditioner R is the exported approximate inverse of this mixed Jacobian. The producer uses real interval Jacobians at 768 and 1024 bits on the full variable cube of radius `rho=1e-120`. It proves every row of `I-R DF` has sum less than one, and every component of `R F(center)` plus rho times that row sum is strictly below rho. Thus `T(x)=x-RF(x)` is a strict self-mapping contraction. Banach's theorem gives an exact zero of F; preconditioner nonsingularity is checked by interval determinant and independently modulo 65537.

Only the 21 free A coordinates receive radius rho. A's critical coordinate and every B coordinate remain singletons. The exact positive noise value satisfies

`tau in [s*(alpha_center-rho), s*(alpha_center+rho)]`.

Direct rational checks establish source feasibility for every point in the A box and both source precision variants, as well as positivity, ordering and strict Q containment. A separate auditor reconstructs all 704 scalar source inequalities without using the producer's source-constraint helper.

## Independent analytic route

The independent calculation uses complex exponential derivatives for the Gaussian kernels and exact rational moment derivatives at 896 and 1152 bits. It computes each center residual and Jacobian entry with scalar sums. For the 21 root columns, a supremum second derivative on the whole coordinate interval bounds Jacobian variation; the alpha column contributes zero variation. Multiplication by absolute preconditioner entries produces a uniform row bound and a separate strict self-map certificate.

Both analytic routes share FLINT. Their formulas and contraction calculations differ, while the inherited finite-source and field-class premises remain common. Serialized primary residuals and midpoint enclosures are compared with independently recomputed enclosures. The complete analytic and interval implementation is not entirely formalized in Lean.

## Why a moving midpoint matters

At the exact solution, `Phi(A)-Phi(B)=2*tau*v`. Choose the common report

`z=(Phi(A)+Phi(B))/2`.

Then `z-Phi(A)=-tau*v` and `z-Phi(B)=tau*v`. Each component error is exactly tau. The certified upper endpoint therefore supplies a valid common budget; the convenient rational budget **1.832e-10** is slightly larger than the best endpoint and also works.

For each fixed pair, a smaller budget than its exact tau cannot work: the triangle inequality would bound a component difference by twice the budget, while its actual absolute difference is 2*tau. This is sharpness for that pair, not a globally optimal threshold. The [primary Mathlib absolute-value reference](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/Order/Group/Abs.html) documents the inequalities; exact pinned source files are archived separately from the current web page.

The preceding construction required targets `Phi(c)+/-tau*v`. Its rejected lower-budget target pairs constrain that specific report and direction. Here the report is free to move. Independent interval enclosures prove that component 0 of every new midpoint differs from Phi(c). For the strongest pair the difference is about -0.0048814, so it is not a rounding-scale displacement.

## Four certified pairs and a preserved failed search

The first three pairs scale the preceding B correction vector by 1/2, 1 and 3/2, overriding its critical coordinate with the fixed value above. Newton solves propose noise levels approximately 1.98022794955e-10, 1.97588282703e-10 and 1.97151299235e-10. All three are subsequently certified by both analytic routes.

Starting from the third pair, an implicit derivative proposes common root shifts that lower tau. Trial steps must converge numerically, retain source-feasible centers and strict Q containment, and improve tau. The first implementation encounters a numerically singular Newton matrix and emits no report. Its original source and actual failure receipt remain preserved. A separate v2 adds a predictor that shifts A with B, adjusts tau using the implicit derivative, and handles failed trials by backtracking.

The corrected search accepts eight steps among nine trials. Its final full step proposes approximately 1.83159054465e-10 and has source-feasible centers, but leaves Q by approximately 1.4599e-6. It is rejected. A smaller step gives the certified pair at approximately **1.831989439894397e-10**, with minimum cube margin about 2.26229e-9. Search convergence and rejection are not optimality or impossibility proofs.

The exact upper endpoint divided by the inherited lower guarantee is approximately **1.0359001329**, improving the previous ratio of about 1.1309018604. The lower guarantee is unchanged. It still applies only to observations in Q under the complete class and fixed root/feature contract. Neither global injectivity nor a decoder for arbitrary reports is established.

Independent arithmetic repeats 1,128 polynomial factorizations and 1,208 coefficient comparisons. Each common noisy report leaves 456 of 604 tracked coefficients fixed and 148 ambiguous within the complete two-field class. Below the inherited uniform guarantee, the field and its tracked vector are unique under the same premises.

## Adversaries, formal scope and continuation

Sixty-four independent-auditor mutations reject altered noise scales and columns, root/noise dimensions, fixed coordinates, source geometry, serialized evidence, midpoint claims and threshold bounds. Exact controls show that a singular Newton step can coexist with true roots and that rejection of one report does not exclude another report. Another control checks the scaled tau interval and constant final Jacobian column.

Six Lean lemmas prove positive scaled noise bounds, the affine noise column, exact midpoint errors, a necessary common-report budget, fixed critical-coordinate separation and a counterexample to a global inference from a rejected report. The complete contraction-to-analytic-map application, interval/modular implementation and inherited field/spectral chain remain written or computational.

Ten recorded development commands contain nine successes and one preserved failed search. No runtime version changed and no new source roots were computed. The final recursive verifier has its own later receipt.

Next: tighten the uniform lower bound using the source-constrained observation sets or subdivisions; improve the feasible upper construction; validate continuous parameter families; implement bounded-error inverse decoding; and extend the region or find global counterexamples. Natural operators, infinite arithmetic and real-part information, topology, physical acquisition and private-input gates remain active across all 117 research branches.

## Reproduction

From the repository with the pinned existing runtimes:

```sh
../acs-research/.venv/bin/python code/frontier_verification/verify_aggregate_variable_noise_delta.py
```

The verifier replays every original exploration and the preserved failure, regenerates both certificates and audits, repeats adversaries, recompiles Lean, checks sources and append-only history, and recursively verifies the preceding checkpoints.
