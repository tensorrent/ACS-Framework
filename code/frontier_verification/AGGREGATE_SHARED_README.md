# Shared ordinate errors and local/spectral feedback

This continuation uses exactly the aggregate spectra, 17 Gaussian measurements, 604 coefficient domains and frozen coefficient-seven duals from the [direct aggregate checkpoint](../../docs/frontier/2026-09-13-aggregate-delta/README.md). It computes no new zeros. Both fields have degree four, signature (0,2) and discriminant 576. The decoder is not supplied their Galois group, subfields, defining polynomials, conductor-parity assignments, candidate field list or held-out arithmetic.

There are two advances. Combining signed measurement derivatives before bounding each common root displacement substantially increases the sufficient noise radii of the existing coefficient-seven certificates. Alternating generic local-degree models with the original spectral inequalities recovers all 17 target coefficients in both spectra. These are scoped computational certificates, not a global completion claim.

## Signed common-input error

Write the inherited inequalities as `W_j c <= R_j` and `-W_j c <= -R_j + B_j`, with interval endpoints chosen outward and the omitted prime tail in `[0,B_j]`. Let their nonnegative dual multipliers be `lambda_(2j)` and `lambda_(2j+1)`. Define

```
alpha_j = lambda_(2j) - lambda_(2j+1)
sigma_j = lambda_(2j) + lambda_(2j+1)
H(t) = sum_j alpha_j scale_j exp(-a t^2) cos(u_j t),
a = 1/25, u_j = log(m_j).
```

The same uncertain ordinate occurs in every measurement. If its displacement is `v_i`, the finite contribution to the combined right-hand side changes by `-2 sum_i (H(t_i+v_i)-H(t_i))`. For `|v_i| <= delta`, the mean value theorem gives the sufficient bound

```
E_shared = 2 delta sum_i sup_(t in enlarged I_i) |H'(t)|,
H'(t) = exp(-a t^2) sum_j alpha_j scale_j
        [-2 a t cos(u_j t) - u_j sin(u_j t)].
```

The original bracket already accounts for uncertainty in the base ordinate. We enlarge that bracket by `delta`, preserving each root's index and multiplicity. Enlarged brackets can overlap; this does not invalidate a sum over the fixed population. Every enlarged bracket in the tested grid remains inside `(0,20)`. This assumes the inherited complete finite population and cutoff; a bare list with unknown missing roots does not satisfy the contract.

We retain three ablations with the identical frozen multipliers:

- `global_rows`: the inherited global derivative estimate `sqrt(2a/e)+u_j`, summed by nonnegative row weights over all roots.
- `local_rows`: bound each row derivative near each root before summing its absolute contribution.
- `shared_roots`: add the signed row derivatives first, then bound the absolute combined derivative near each root.

The local bound is capped by the global bound, and the shared bound by the local bound. In the informative duals, each nonzero multiplier belongs to a distinct measurement row; consequently `sigma_j=|alpha_j|`. Zero-radius or zero-multiplier cases serialize empty leaves and zero additional-error derivative placeholders. Those placeholders do not claim that a nonzero function's derivative vanishes at radius zero.

## Unknown zeros and residual support

Finite-error cancellation does not justify cancelling the unknown-zero budgets. The inherited zero-moment constant is

```
C_D = 3/2 + (1/2) log(D) - 2 log(2 pi) + 2 psi(2),
U = C_D - sum_known 3/(9/4 + gamma_i^2).
```

The known contribution is enclosed over the enlarged intervals, so increasing ordinate uncertainty conservatively enlarges the unknown moment budget. For `T=20`, each row retains

```
E_Zj = scale_j U (4+T^2) exp(-a T^2 + a/4) cosh(u_j/2).
```

The combined unknown-zero budget is `sum_j sigma_j E_Zj`. It is added to the nominal dual bound and the chosen finite-input error. The nominal bound uses the inherited unwidened observation intervals, omitted-prime bounds, and the full support of the residual objective over all 604 coefficient boxes. An empty multiplier vector for the positive coefficient objective still gives bound four, not zero. The prior checkpoint derives and audits the analytic identity and unconditional tails; zeros beyond the finite window need not lie on the critical line.

## Tested radii and independent checks

Both 224-bit/32-partition and 320-bit/48-partition runs agree on every candidate set. For field A, the largest successful tested radii for coefficient seven are `0.00001` with global rows, `0.0001` with local rows, and `0.002` with shared roots. For field B they are `0.0001`, `0.01`, and `0.05`. Thus the shared bound improves the tested generic-box radius by factors 200 and 500. Localization accounts for factors 10 and 100; cancellation adds factors 20 and 5. The targets are `c_7(A)=4` and `c_7(B)=0`.

At radius `0.005`, the shared A domain is `{3,4}`. Since `7` does not divide `576`, the generic unramified degree-four rule gives `c_7 in {0,1,2,4}`, removing three and retaining four. This separately declared local assumption extends A's tested sufficient radius to `0.005`; it is not part of the generic-box result. At the next shared-only grid points, A has `{3,4}` at `0.005` and B has `{0,1}` at `0.1`. Surviving candidates or failed certificates do not establish feasible alternate spectra, alternate fields, optimal radii or information-theoretic limits.

The independent audit checks all 39,600 stored nonempty leaf midpoints using a complex-exponential derivative representation. It then covers all widened intervals afresh with 47,520 leaves at 384 bits and 96 partitions per root. The new expression is the real part of `sum_j w_j(-2az+i u_j)exp(i u_j z)`, multiplied by `exp(-az^2)`. Exact 192-bit outward integer arithmetic replays the nominal objectives and adds rounded budgets to reproduce all 144 one-sided candidate bounds. These routes use different formulas and partitions but share FLINT as their interval engine.

Separately, mpmath at 85 digits checks 96 finite displaced sums, using uniform positive/negative displacements and positive/negative gradient patterns. These sampled controls do not replace interval coverage. Two constructed controls assign different displacements to the same root in different rows and exceed the shared bound. They demonstrate that common input errors are a necessary premise; they are deliberately inconsistent measurement inputs, not physical alternate spectra. Eight cases shared with the previous radius grid reproduce the old global-row results.

## Generic local rules and feedback

At a prime, enumerate all multisets of positive integer pairs `(e_i,f_i)` satisfying `sum_i e_i f_i=4`. There are eleven generic models. Each implies `c_(p^k)=sum_(f_i divides k) f_i`. The `degree_only` profile permits all eleven models. The `degree_discriminant` profile also requires ramification exactly at primes dividing 576. Neither profile uses a Galois group or a field candidate catalogue.

Start with the intersection of the preceding monotone and dual coefficient domains. At each iteration, retain local models compatible with all current coefficients at their prime, project those models back to every coefficient domain, and apply the spectral row min/max exclusions to the new domains. Every operation only removes candidates, so the process reaches a finite fixed point. Recorded spectral exclusions use the domains after that iteration's complete local step. They may depend on those reductions; resetting to the original domains is not a valid replay.

The baseline recovers 13 of 17 targets in A and 9 in B. One local pass recovers 14 and 11 under degree alone, or 15 and 12 when discriminant ramification is used. Repeating local and spectral deductions recovers all 17 under either profile, at both inherited measurement precisions. The target set is the prime powers through 31; it does not represent all 604 support coefficients.

At the full support through 4096, A has 45 singleton domains under either profile. B has 37 under degree alone and 38 with discriminant ramification; the extra singleton is `n=2401`, changing `{2,4}` to `{4}`. The remaining 559 A domains and 567/566 B domains are conservative unresolved domains. Local compatibility and a monotone fixed point do not prove a jointly realizable number field.

An independent enumeration uses integer partitions of four followed by all divisor pairs, reproducing the eleven models. Exact integer inequalities replay all 3,162 local removals and 190 spectral removals across eight cases. All 604 held-out true coefficients survive every iteration. The arithmetic vectors are inherited from the previous independent polynomial-factorization audit; they are used only to validate results, not to generate the deductions.

## Adversarial scope and replay

Ten actual proof-component mutations test signed multipliers, retained unknown-zero tails, finite population length, complete leaf coverage, false derivative enclosures, residual box support, catalogue completeness, unramified-prime restrictions, elimination of a true coefficient, and omission of local prerequisites. Each targeted predicate accepts its original component and rejects the mutation. These controls supplement the whole independent audit; they do not claim exhaustive fuzzing or that every corrupted component would change the final coefficient.

The [checkpoint](../../docs/frontier/2026-09-13-aggregate-shared-delta/README.md) records seven successful commands, full outputs, exact source hashes and append-only history. Run with the pinned environment:

```
python code/frontier_verification/verify_aggregate_shared_delta.py
```

This recursively verifies the prior checkpoint, extracts its immutable inputs, regenerates both shared-bound and local-closure runs, and freshly executes all three new audits. It verifies the manifest, source snapshot, receipts, 117 preserved branches and 393-event ledger with an unchanged 388-event prefix. The full analytic and number-field arguments are not formalized in Lean.

Next gates are to optimize duals for the actual shared-error bound, compare higher-order or direct nonlinear root enclosures, resolve the remaining support coefficients or construct meaningful ambiguity witnesses, and test additional verified fields under an explicit metadata contract. The wider ACS queue remains active.
