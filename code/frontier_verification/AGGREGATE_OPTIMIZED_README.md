# Adapting aggregate-spectrum duals to common ordinate uncertainty

This pass advances the [shared-error checkpoint](../../docs/frontier/2026-09-13-aggregate-shared-delta/README.md). It keeps the same seventeen Gaussian measurements, complete aggregate spectra through height 20, and generic coefficient boxes `0 <= c_n <= 4` for all 604 prime powers through 4096. It studies coefficient seven. It does not claim that the preceding seventeen-target recovery remains valid at the larger noise radii.

The permitted metadata remains degree four, signature (0,2) and discriminant 576. No field catalogue, Galois group, subfields, defining polynomial, conductor-parity assignment, local model or held-out arithmetic is supplied to the new optimizers or certificate producer. The underlying verified benchmark coefficients are `c_7(A)=4` and `c_7(B)=0`; arithmetic enters only the downstream audit.

## Proposal objective and trust boundary

For a coefficient objective `s c_7`, let `A c <= b` be the nominal outward inequalities, with unknown-zero errors removed from the observations and omitted-prime errors retained. For nonnegative dual multipliers `lambda`, let

```
alpha_j = lambda_(2j) - lambda_(2j+1),
sigma_j = lambda_(2j) + lambda_(2j+1),
H(t) = exp(-a t^2) sum_j alpha_j scale_j cos(u_j t),
a = 1/25, u_j = log(m_j).
```

The residual objective has exact box support `4 sum_k max(s 1_(k=7) - (A^T lambda)_k, 0)`. It must be retained even if the solver claims that the residual is zero. With an empty multiplier vector, the positive coefficient objective still has support four.

The proposal LP introduces positive residual variables `z_k`, and nonnegative root-error variables `q_i`. It imposes

```
A^T lambda + z >= s e_7,
q_i >= -2 sum_j alpha_j scale_j [h_j(gamma_i+v)-h_j(gamma_i)]
       for 33 uniformly spaced v in [-delta,delta],
lambda,z,q >= 0.
```

Its objective is `b^T lambda + 4 sum z_k + sum q_i + sum sigma_j E_Zj`, using floating midpoint measurements and widened unknown-zero budgets. This finite floating surrogate proposes useful multipliers. Its score is not a bound over continuous displacements, a rigorously established relaxation optimum, or evidence of information-theoretic optimality. The zero displacement is included.

Multipliers are rounded to exact nonnegative rationals on a `10^-9` grid. Every subsequent certificate is recomputed from those rationals with all residual coefficients and analytic budgets. The proof does not depend on LP optimality or on the numerical feasibility of auxiliary LP variables. An exploratory 36-LP probe and the final 48-proposal run are separately preserved; all solver calls reported success.

## Complete nonlinear error enclosures

Let `I_i` be an inherited root bracket, enlarged by `delta` to `J_i`. A common displacement changes the combined finite contribution by `-2 sum_i [H(gamma_i+v_i)-H(gamma_i)]`. For an upper coefficient bound, it suffices to bound that signed change above. There is no need to bound its absolute value unless using the separate symmetric-derivative ablation.

For each rational leaf `[l,r]` covering `J_i`, let `m=(l+r)/2`, `V=[-(r-l)/2,(r-l)/2]`. The producer encloses

```
-2 [H(t)-H(gamma_i)]
    in -2 [H(m)-H(I_i)] - 2 H'([l,r]) V.
```

This mean-value enclosure includes the nonlinear variation; it is not a Taylor truncation without a remainder. The largest upper endpoint over every leaf, capped below by zero, gives the root's one-sided error budget. Summing those budgets is valid for independent displacements of different roots, with each root's displacement shared by all measurement rows. Taking `H(I_i)` independently from `H(t)` slightly widens the enclosure while preserving the original bracket uncertainty.

The symmetric comparison uses `2 delta sum_i sup_(J_i) |H'|`, with each derivative bound capped by the inherited global row bound. Both methods use the same multiplier vectors, intervals and unknown-zero budgets. We run both the old frozen vectors and the new noise-adapted vectors, separating multiplier choice from the way finite errors are enclosed.

Zero radius or empty multipliers produce zero additional finite error and empty leaves. This does not assert that a nonzero function has zero derivative at radius zero. Enlarged brackets may overlap; indices and multiplicities are preserved. All tested brackets remain inside `(0,20)`. The complete finite population and cutoff are inherited assumptions; these certificates do not apply to a list with unaccounted missing roots.

## Analytic tails remain in the proof

At each tested radius, recompute

```
U = C_D - sum_known 3/(9/4+gamma_i^2)
```

over the enlarged brackets. The inherited explicit-formula and zero-moment derivation gives the combined unknown-zero budget

```
sum_j sigma_j scale_j U (4+20^2)
      exp(-a 20^2+a/4) cosh(u_j/2).
```

It is added to the nominal bound and the finite error. Common finite-root cancellation does not cancel this nonnegative tail sum. Zeros outside the certified finite window need not lie on the critical line. The omitted-prime bounds, normalization, gamma terms and coefficient bounds are inherited from the [direct aggregate audit](../../docs/frontier/2026-09-13-aggregate-delta/README.md); this pass computes no new zeros or measurements.

## Results and ablations

Both direct-enclosure runs, at 224 bits/64 leaves and 320 bits/96 leaves per active root, agree on every direct candidate set. Noise-adapted one-sided certificates recover A's coefficient through tested radius `0.06` and B's through `0.13`. Their upper objective bounds are safely below `-3.029` for `-c_7(A)` and below `0.951` for `c_7(B)`. Integrality yields four and zero. The independently replayed bounds are tighter.

On the same radius grid, frozen multipliers recover through `0.002` and `0.07`, with either direct or symmetric bounds. Thus adapting the multipliers and using the one-sided enclosure increases those tested sufficient radii by factors 30 and `13/7`. The preceding checkpoint's B grid stopped at `0.05` before its next tested value `0.1`; the newly checked `0.07` frozen result is a grid extension, and must not be attributed to multiplier optimization.

With adapted multipliers but symmetric derivative bounds, the two producers recover through `0.02` and `0.07`. A finer independent audit extends B's symmetric certificate to `0.1`. Using that stronger independently checked comparison, A's improvement divides into a factor 10 from multiplier adaptation and a factor 3 from the one-sided method; B's divides into `10/7` and `13/10`. These factors describe successful points on the declared grid, not sharp boundaries.

One producer comparison differs: at A radius `0.14`, the adapted symmetric domain is `{1,2,3,4}` with 64 leaves and `{2,3,4}` with 96 leaves. The direct domain remains `{3,4}` in both. The independent audit strengthens two B symmetric domains: at `0.1`, `{0,1}` becomes `{0}`; at `0.2`, `{0,1,2}` becomes `{0,1}`. Both precision and subdivision change between these routes, so these gains are not attributed to precision alone. Every narrower domain is retained as a separately supported result.

At the next direct grid points, A has `{3,4}` at `0.07` and B has `{0,1}` at `0.14`. Neither survivor set proves an alternate spectrum or a globally realizable field. Applying the separately inherited generic unramified-prime rule `c_7 in {0,1,2,4}` extends A's tested singleton radius to `0.14`; B remains at `0.13`. That supplement uses extra local information and is not part of the generic-box result.

## Independent audit and counterexamples to sampled bounds

The auditor uses the complex expressions

```
H^(0,1,2)(t) = Re sum_j w_j exp(-a t^2+i u_j t)
                         * [1, (-2at+i u_j), (-2at+i u_j)^2-2a].
```

It checks 158,400 stored leaf midpoints. It then covers the enlarged intervals afresh with 126,720 leaves at 384 bits and 128 leaves per active root. A quadratic Taylor enclosure uses `H(m)+H'(m)V+H''([l,r])V^2/2`, with the square enclosed in `[0,((r-l)/2)^2]`. This differs from the producer's real trigonometric first-derivative enclosure. Both routes share FLINT; the audit does not claim an independent interval implementation.

Exact 192-bit outward integer arithmetic replays all 192 nominal-plus-error objective bounds and confirms every producer exclusion. Mpmath at 85 digits checks 192 displaced sums using uniform and gradient-directed shifts. These samples complement the complete interval cover.

For each spectrum, a float search locates an off-grid displacement at radius `0.002`; fresh complex interval evaluation proves that its root error exceeds all 33 proposal-grid errors. Both witnesses use offset `-13/16000`, at root indices 3 and 6 respectively. Their strict gaps exceed `5.20e-9` and `2.48e-9`. These are counterexamples to using the sampled maximum itself as a continuous bound, even though the gaps are small. They do not show that the resulting LP coefficient score changes a recovered integer.

Eight semantic proof-component mutations are rejected after the intact components pass: negative multipliers, reversed signed weights, omitted unknown-zero budget, omitted residual support, a missing cover leaf, midpoint substitution for a whole leaf, and the two sampled-maximum substitutions. The final two tests reuse the audited off-grid witnesses and are not counted as additional independent witnesses.

## Reproduction and continuation

Run `python code/frontier_verification/verify_aggregate_optimized_delta.py` in the pinned environment. It recursively checks the prior checkpoint, regenerates proposals and both producer runs, freshly executes the independent and adversarial audits, and verifies source hashes, command receipts and append-only history. See the [checkpoint package](../../docs/frontier/2026-09-13-aggregate-optimized-delta/README.md) for exact inputs, output archives and results.

The next derivation can combine the known-moment variation and finite Gaussian change for the same displaced root before taking separate maxima; the current bound deliberately retains their separate conservative budgets. Further gates include wider target recovery under uncertainty, constructive ambiguity with global realizability, additional actual fields, and the wider ACS questions. The complete analytic and number-field proof remains unformalized, and no global completion is claimed.
