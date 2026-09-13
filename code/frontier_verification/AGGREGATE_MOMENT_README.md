# Joint moment uncertainty and noisy target feedback

This pass extends the [coefficient-seven uncertainty study](../../docs/frontier/2026-09-13-aggregate-optimized-delta/README.md) to all seventeen prime-power targets through 31. It uses the same complete aggregate spectra through height 20, seventeen Gaussian measurements, 604 coefficient boxes through 4096, degree four, signature (0,2) and discriminant 576. No new zeros or measurements are computed.

The new continuous bound keeps each root's finite-sum change tied to its known-moment change. A second advance alternates generic local projections with the residual support of the already validated duals. At radius 0.1, the latter process recovers thirteen targets in spectrum A and ten in B when ramification is inferred from the supplied discriminant. The raw spectral certificates recover three and four at that radius. These are scoped noisy-input results; surviving candidates and a finite fixed point do not establish global field realization or information-theoretic ambiguity.

## Combining two effects of the same displacement

For nonnegative inequality multipliers, define the signed Gaussian combination `H(t)` and nonnegative row weights `sigma_j` as in the preceding study. Write

```
m(t) = 3/(9/4+t^2) = 12/(9+4t^2),
kappa = sum_j sigma_j scale_j (4+20^2)
        exp(-a 20^2+a/4) cosh(u_j/2),
U_0 = C_D - sum_i m(gamma_i),   a=1/25.
```

For displaced ordinates `t_i`, the unknown-zero budget is `kappa [C_D-sum_i m(t_i)]`, while the finite-sum contribution changes by `-2 sum_i [H(t_i)-H(gamma_i)]`. Their sum can therefore be written

```
kappa U_0 + sum_i { -2[H(t_i)-H(gamma_i)]
                   -kappa[m(t_i)-m(gamma_i)] }.
```

The two changes inside each brace use the same root displacement. Define `J(t)=-2H(t)-kappa m(t)` and bound `J(t_i)-J(gamma_i)` over the widened bracket. This retains the dependence that was lost when the finite error and the worst widened moment were maximized separately.

The producer also evaluates the independently valid separated budget `kappa U_wide + sum_i sup[-2 delta H_i]`. The reported coupled budget is the minimum of that bound and the joint-increment bound. This explicit fallback prevents numerical overestimation in one enclosure from weakening the result. The original bracket uncertainty, omitted-prime bounds and all 604 residual coefficients remain in the proof. Unknown zeros outside the finite window need not lie on the critical line.

Zero displacement belongs to each increment domain, so increment maxima are capped below by zero. At zero radius, the additional increments are zero and no leaves are needed; the baseline unknown-zero budget remains. Enlarged root brackets can overlap while their indices and multiplicities remain fixed. All tested brackets stay inside `(0,20)`.

## Proposals and continuum verification

A floating LP samples the joint increment at 33 displacements per root. It proposes both signs of all seventeen objectives at radii `0`, `0.005`, `0.02` and `0.1`, giving 272 proposals. Its scores are not continuum bounds or certified optima. Multipliers are rounded to nonnegative rationals on the inherited `10^-9` grid and validated afterward. Sixteen coefficient-seven multiplier vectors from the preceding study are replayed on the common radius grid as additional valid certificates. The producer thus checks 288 objectives.

The 224-bit producer covers every active root interval with 48 rational leaves. At a leaf midpoint it encloses finite and joint changes using first derivatives over the entire leaf. The derivative of the joint expression is `-2H'(t)-kappa m'(t)`; its terms are combined before multiplying by the displacement interval. No unbounded Taylor remainder is discarded.

The independent route uses complex Gaussian derivatives and quadratic Taylor enclosures at 384 bits with 96 leaves. It checks 104,592 stored midpoints and freshly covers 209,184 leaves. The rational moment function receives an additional route: symbolic differentiation verifies

```
m'(t)   = -96t/(9+4t^2)^2,
m''(t)  = (1152t^2-864)/(9+4t^2)^3,
m'''(t) = 4608t(9-4t^2)/(9+4t^2)^4.
```

Every tested interval lies above `3/2`. There, `m` decreases, `m'` increases and `m''` decreases, giving rational endpoint enclosures without transcendental interval evaluation. Exact outward conversion of each rational endpoint to a 192-bit grid supplies integer upper moment budgets. Exact integer products combine those budgets with the nonnegative `kappa` bound and the nominal dual objective. All 576 separated/coupled objective bounds are replayed. The two transcendental interval routes share FLINT.

Mpmath at 85 digits checks 528 displaced sums using uniform and joint-gradient-directed patterns. Samples complement the complete interval covers. The finer independent calculation removes candidate four from A's `c_9` upper domain at radius 0.1 for both budget methods; that change adds no singleton by itself.

The joint budget is selected in 97 nonzero-radius cases: 35 at 0.005, 34 at 0.02 and 28 at 0.1. The largest relative reduction is about 0.7042%, for A's positive `c_8` objective at radius 0.02. No producer candidate domain changes between the two budget methods on this grid. The tighter bound is retained without attributing the later integer-recovery gains to it.

## Local projections and residual feedback

Each noisy calculation starts all 604 coefficients in `{0,1,2,3,4}`, then intersects only certificates for that same radius. It does not reuse zero-noise monotone domains or earlier exact-input local deductions as noisy premises.

The degree-only local profile enumerates all eleven multisets of `(e_i,f_i)` satisfying `sum e_i f_i=4`. The second profile additionally requires ramification exactly at primes dividing 576. That rule follows from the supplied discriminant. Both profiles use `c_(p^k)=sum_(f_i divides k) f_i`; neither uses a Galois group or a candidate-field catalogue.

After projecting compatible local models onto coefficient domains, recompute the residual support of each frozen dual. If the residual coefficient is `r_k` and the current domain is `D_k`, its support is

```
sum_k max_(v in D_k) r_k v,
```

rather than the initial `4 sum_k max(r_k,0)`. The analytic error budget and multipliers remain unchanged. Those budgets depend on the noisy root intervals, not on the coefficient boxes. Each resulting strict objective bound can remove another target candidate. Repeating local projection and residual-support deductions reaches a monotone finite fixed point.

The feedback consumes independently validated analytic budgets and derived noisy candidate domains. It reads no arithmetic coefficient vector. The independent auditor later checks the actual coefficients after each round. The inference boundary is explicit in code and provenance; it is not a claim of formal noninterference or a blinded study.

The independently checked degree/discriminant results are:

- At radius 0: raw spectral counts 12/9, one local pass 14/12, and residual feedback 14/13.
- At radius 0.005: raw counts 10/9, one local pass 13/12, and feedback 13/13.
- At radius 0.02: raw counts 9/9, one local pass 13/11, and feedback 13/13.
- At radius 0.1: raw counts 3/4, one local pass 9/9, and feedback 13/10.

Counts are ordered A/B. The degree-only local profile reaches 11/10 at radius 0.1 and 13/12 at radius 0.02. The stronger profile's full support at radius 0.1 has 33 singleton domains for A and 28 for B out of 604. A's four remaining targets are 23, 25, 29 and 31; B's seven are 13, 17, 19, 23, 25, 29 and 31. Their actual candidate domains are preserved in the result files.

The zero-radius result above belongs to this frozen-dual method. The earlier [full local/spectral row feedback](../../docs/frontier/2026-09-13-aggregate-shared-delta/README.md) already recovers all seventeen exact-input targets in both fields. That stronger baseline remains valid. This pass does not claim optimal deductions from the available inequalities, and its lower exact-input count identifies a limitation of keeping the multiplier family fixed.

An independently enumerated catalogue verifies all 32 one-pass projections and 32 feedback cases. Exact integer residuals and rational error budgets replay 12,326 one-pass local removals, 12,396 local removals within feedback, and 56 new dual removals. These totals count the declared method/profile/radius replicas. Every one of the 604 held-out true coefficients survives every round.

## Failure controls and remaining gates

Ten semantic mutations are rejected after their original components pass. They test moment normalization, complete interval coverage, replacing a joint leaf with its finite-only counterpart, freezing the moment, negative multipliers, eliminating the true coefficient, discarding coefficient-domain prerequisites, reusing zero-noise domains, catalogue completeness and the ramification rule at seven.

A separate one-root diagnostic uses a positive unit measurement multiplier. Both its finite change and its joint change increase over the tested interval. At the positive endpoint, the joint change exceeds the entire finite-only maximum by more than `1.099e-7`. Freezing the known moment therefore omits a positive term in the analytic budget expression. This counterexample does not assert that unknown zeros attain their tail bound, or construct another number field.

Run `python code/frontier_verification/verify_aggregate_moment_delta.py` in the pinned environment to reproduce the proposals, continuum certificates, local projections, feedback, independent audits and mutations, while recursively verifying the earlier checkpoints. The [evidence package](../../docs/frontier/2026-09-13-aggregate-moment-delta/README.md) preserves all seven scientific execution receipts, sources, exact intervals and append-only history.

Next, re-optimize the multiplier family after valid domain reductions, and compare those deductions with noisy standalone-row propagation. Remaining candidate domains need constructive feasibility or global-field analysis before they can be called ambiguity. Further fields, the infinite arithmetic bridge, topology, physical interpretations and the complete ACS queue remain open. The full analytic and number-field proof is not formalized in Lean.
