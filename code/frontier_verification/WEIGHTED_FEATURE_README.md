# Larger uniqueness regions and two-sided feature-error bounds

The [checkpoint evidence](../../docs/frontier/2026-09-14-aggregate-weighted-feature-delta/README.md) enlarges the certified 22-feature uniqueness region from radius 1e-10 to radius 0.03. Every preceding joint-feature collision lies in that larger region. More targeted componentwise estimates also give a quantitative identification guarantee, and newly certified feature-space constructions place an ambiguity upper bound only about 13.1% above it under the same restricted observation contract.

## Fixed source and measurement contract

The complete inherited metadata class consists of A=Q(sqrt(2),sqrt(-3)) and B=Q(sqrt(-2),sqrt(-3)), degree four, signature (0,2), absolute discriminant 576. Each complete positive source prefix below 39/2 contains 22 entries. Select the population before independent bounded root-coordinate errors, preserving all entries and multiplicities. All source and classification premises remain linked to their original certificates and are recursively verified.

The 22 finite features are the preceding 17 Gaussians at width parameter 1/25, the finite moment `sum 3/(9/4+y_i^2)`, center 37 at 1/25, center 2 at 1/24, center 41 at 1/25, and center 43 at 1/25. Each Gaussian is `2 sum exp(-a*y_i^2) cos(log(m)*y_i)`. There is no released raw root list, count profile or unknown-tail contribution. In particular the finite moment is not an infinite moment. The feature-error norm uses these stated component units.

Write c for the inherited rational midpoint root vector and L,U for the full-list threshold bounds, with `U-L=2e-30`. This pass fixes root-coordinate error radius `r=U-1e-8<L`. The standard coordinate cubes are `Q_eta={y: max_i |y_i-c_i|<=eta}`, for eta=0.01 and 0.03. They remain positive and strictly ordered. Additional feature errors are independent absolute component errors bounded by tau.

## Retaining cancellation in Taylor bounds

Let J be the Jacobian of the 22-feature map Phi, and let R be the exact rational preconditioner proposed at c. Each Jacobian column depends only on its corresponding root coordinate. For `|h_j|<=eta`, Taylor's theorem applied to the scalar derivative gives

`g'_k(c_j+h_j) = sum_(t=0)^5 g_k^(t+1)(c_j)*h_j^t/t! + remainder`,

`|remainder| <= eta^6/6! * sup_(|x-c_j|<=eta) |g_k^(7)(x)|`.

All kernels are smooth on these real intervals; the moment denominator stays positive. Multiply the center coefficients by R before taking absolute values. A nonnegative matrix majorizing `|I-RJ|` entry by entry is

`B_ij = |(I-RJ(c))_ij| + sum_(t=1)^5 eta^t/t! * |sum_k R_ik g_k^(t+1)(c_j)|`

`       + eta^6/6! * sum_k |R_ik| sup |g_k^(7)|`.

The full uniform remainder is essential. The [primary Mathlib Taylor documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/Calculus/Taylor.html) describes the scalar remainder results; exact pinned reference sources are archived separately from the current web page. The derivative-to-Lipschitz step is the same convex-segment mean-value argument audited in the preceding checkpoint.

Choose positive rational weights w and define `||z||_w=max_i |z_i|/w_i`. A binary64 eigenvector calculation proposes the weights; only the exact exported rational weights and validated row inequalities are proof inputs. The producer proves `sum_j B_ij*w_j/w_i < 1/2` for every row. Thus `G(y)=y-R Phi(y)` is Lipschitz with constant at most 1/2 in this norm on Q_eta. Consequently Phi is injective there.

**The region is still a standard coordinate cube.** It is not the smaller weighted ball. Convexity of Q_eta permits the mean-value argument in the weighted norm. No fixed-point self-map property of the large region is asserted or needed for injectivity.

Complex exponential/Hermite jets at 768 and 1024 bits provide the primary bounds. Independent real sine/cosine polynomial recurrences and exact rational moment numerator recurrences provide scalar bounds at 896 and 1152 bits. SymPy checks derivative orders 0 through 7. Both analytic routes share FLINT. The preceding exploratory radius/order sweeps and their unsuccessful sufficient bounds remain preserved.

At eta=0.03, the weighted bound is about 0.45074. This is a 300-million-fold increase in certified radius over 1e-10, not a global injectivity theorem or an optimal-region claim. All 12 earlier collision boxes fit Q_0.03; 11 fit Q_0.01. Failure of a tested bound at a larger radius does not prove a collision there.

## Exact componentwise stability

Rounding each primary matrix bound upward to a 40-bit dyadic grid gives an exact nonnegative matrix Bbar. Its exact weighted row sums still satisfy the half-defect bound. Set `r_i=sum_k |R_ik|`. Exact rational elimination constructs a positive vector h satisfying

`h_i = r_i + sum_j Bbar_ij*h_j`.

For any y,z in the same cube, the mean-value estimate gives, componentwise,

`|y_i-z_i| <= r_i*||Phi(y)-Phi(z)||_infinity + sum_j Bbar_ij*|y_j-z_j|`.

The weighted maximum principle implies

`|y_i-z_i| <= h_i*||Phi(y)-Phi(z)||_infinity`.

To see why, subtract `h_i*error` from each component bound. If any remainder is positive, choose a coordinate maximizing its ratio to w_i. The nonnegative matrix and its weighted row bound force that positive maximum to be at most half itself, a contradiction. The new Lean proof formalizes this finite maximum principle and the componentwise supersolution consequence.

The independent route rounds its real-polynomial majorant upward on a 48-bit dyadic grid. It uses 33 positive Neumann-series terms and an exact weighted geometric tail, rather than a linear solver. Direct rational inequalities verify its supersolution; its critical-coordinate bound is no larger than the claimed primary bound.

The critical coordinate is index 1, the second positive root. Its primary stability constants are approximately 56.54509302 on Q_0.01 and 79.66539048 on Q_0.03. These are much more useful for field identification than a maximum over all root coordinates. A larger neighborhood alone does not imply better conditioning.

## Uniform identification versus actual ambiguity

For source-feasible observations from A and B, the critical source intervals imply

`y_A,1 - y_B,1 >= 2*(L-r)>0`.

If both observations lie in Q_eta, componentwise stability therefore gives

`||Phi(y_A)-Phi(y_B)||_infinity >= 2*(L-r)/h_1`.

A common released vector with independent feature errors at most tau would make that feature separation at most `2*tau`. Hence field identity is guaranteed whenever

`tau < (L-r)/h_1`.

For Q_0.01 this exact rational guarantee is approximately **1.76850005296e-10**. For Q_0.03 it is approximately **1.25525023352e-10**. These are uniform separation statements over the stated source-feasible observations and complete two-field class. They are not an implemented decoder for arbitrary observations, and they do not cover observations outside the specified cube.

For an actual ambiguity construction, use the exact sign vector of R's critical row as v and propose the targets

`Phi(y_A)=Phi(c)+tau*v`, `Phi(y_B)=Phi(c)-tau*v`.

Eight 22-variable inverse roots, two for each of four tested tau values, are certified by small self-mapping contraction boxes of radius 1e-120. Primary real interval Jacobians and independent complex second-derivative bounds, with modular nonsingularity checks, prove exact target equations. Every inverse root lies in Q_0.01.

At tau=2.1e-10 and **2e-10**, both observations satisfy every source error bound. Their common released vector is exactly Phi(c), using feature errors `-tau*v` and `+tau*v`. Their exact feature distance is `2*tau`, so tau is the sharp component-error threshold for each of these fixed pairs. At tau=1.98e-10 and 1.97e-10, exact source/observation interval separation excludes the specified signed target pair. Local injectivity excludes another local inverse for those exact targets. It does not exclude other directions, common releases or observation pairs at those budgets.

Thus, for fixed r and Q_0.01, the local ambiguity threshold is bounded below by the uniform guarantee and above by the actual construction at 2e-10. The ratio is approximately **1.1309018604**. The exact threshold is still open. The larger Q_0.03 has its own weaker lower bound; the same actual pair supplies an upper bound there.

Independent arithmetic performs 1,128 polynomial factorizations and 1,208 coefficient comparisons. At the common noisy release, 456 of 604 tracked coefficients remain fixed and 148 are ambiguous within the complete class. Below the uniform guarantee, field identity—and therefore its tracked arithmetic vector—is unique under the stated conditions.

The common report Phi(c) illustrates why a noisy decoder cannot simply invert the report and test that single root vector: c itself fails the two source-feasibility requirements at r<L, while noise-consistent observations from both fields exist. A future decoder must examine the bounded-error inverse set.

## Endpoint audit, adversaries and formal scope

The first independent region audit reconstructed serialized Arb balls before comparing endpoints. That operation adds rounding. A controlled 1024-bit diagnosis found 108 false rejections among 1,936 comparisons, while all exact dyadic midpoint-plus-radius endpoint comparisons passed. The [python-flint documentation](https://python-flint.readthedocs.io/en/latest/arb.html) explicitly allows upward rounding of a nonzero constructor radius. The separate v2 auditor compares the exact rational endpoints. The original certificate, failed auditor source and actual failure receipt remain intact; no bound was relaxed.

Fifty-two adversarial mutations reject incorrect weights, geometry, Taylor order/remainder scaling, matrix and supersolution data, acquisition contracts, inverse targets and source-feasibility labels. An exact polynomial control `f(x)=x-(4096/14197)x^7` has equal values at 3/4 and 1. Omitting its order-6 derivative remainder or dividing by 7! instead of 6! would falsely certify a small derivative defect; the correct remainder prevents that conclusion. Separate controls distinguish standard cubes from weighted balls and exact endpoints from reconstructed interval representations.

Six Lean lemmas prove the weighted maximum principle, componentwise supersolution bound, critical source gap, strict noise-identification consequence, signed common-release error and exact midpoint-radius upper bound. The full Taylor/mean-value application, analytic identities, interval implementation, modular interpretation and inherited field/spectral/arithmetic chain remain separately written or computational.

Fourteen recorded commands comprise 12 successes and two preserved failures. The first full verifier passed the decoder record to the proposal generator instead of the midpoint/preconditioner record; its source and KeyError receipt are preserved beside the separate corrected v2 verifier. The scientific certificates are unchanged. No runtime version changed and no new source roots were computed. The final recursive verifier has its own subsequent execution receipt.

Next: tighten the restricted two-sided noise bounds; optimize directions and common releases; implement a verified bounded-error inverse decoder; validate parameter families; extend the admissible region or find global counterexamples; and formalize the remaining analytic bridges. Natural operators, infinite arithmetic/real-part information, topology, physical acquisition/precision models and all private-input gates remain part of the wider active ACS program.

## Reproduction

From the repository with the existing pinned runtimes:

```sh
../acs-research/.venv/bin/python code/frontier_verification/verify_aggregate_weighted_feature_delta_v2.py
```

The verifier regenerates the certificates and proposals, replays both independent methods and the original explorations, repeats the endpoint diagnosis and adversaries, recompiles Lean, checks immutable evidence and append-only history, and recursively verifies preceding checkpoints.
