# Certified ranges for uncertain ordinates

This instrument replaces a coarse error allowance in the [coupled recovery calculation](COUPLED_README.md). It reuses the same immutable finite root certificates, Gaussian measurements, field invariants and unconditional omitted-zero bound. It also retains measurements from smaller cutoffs so that a larger cutoff can add information without discarding previous constraints.

## Four finite-sum bounds

Write `h(t) = exp(-a t²) cos(u t)`, with positive `a` and `u = log(m)`, and `S = 2 sum h(gamma_j)` over the certified positive ordinates. The scale `A`, background terms, positive prime-power weights and prime-tail allowance are inherited from the [recovery derivation](RECOVERY_README.md). Every coefficient through 4096 starts in `{0,1,2,3,4}`. No local-power relation or expected coefficient seeds inference.

The experiment enlarges each original certified ordinate interval by a declared radius `delta`. This is a loss of precision around existing certified data, with the finite zero count and cutoff membership retained. It does not assert that arbitrary shifted ordinates are the zeros of a number field. Moving a noisy observation's center and then expanding it by `delta` is a different experiment and may require a larger enclosure.

The global route is unchanged: `|h'(t)| <= sqrt(2a/e) + u`, so its normalized finite-input allowance is `2 A N delta (sqrt(2a/e) + u)`.

The individual derivative route uses

```
h'(t) = exp(-a t²) [-2at cos(ut) - u sin(ut)].
```

For each enlarged interval `I_j`, interval arithmetic bounds `sup_Ij |h'|`. The mean value theorem gives the allowance `2 A delta sum_j sup_Ij |h'|`, in addition to the original certified finite-sum enclosure. The smaller of its upper endpoint and the old global upper bound is safe. Floating-point interval construction rounds the enlarged boxes outward; these outer boxes are used for derivative evaluation. The declared displacement is the mathematical `delta`, rather than the slightly enlarged machine radius.

The direct route evaluates `2 sum h(I_j)` with ordinary interval arithmetic. The stationary route computes the minimum and maximum of each scalar Gaussian on its enlarged interval from endpoints and every possible enclosed critical point, then sums lower and upper bounds separately. Both range routes operate on the actual outward-rounded machine boxes and therefore also enclose the declared model.

## All turning points are accounted for

Define

```
theta(t) = u t + atan(2 a t / u).
h'(t) = -exp(-a t²) sqrt(u² + 4 a² t²) sin(theta(t)).
theta'(t) = u + (2a/u)/(1 + (2at/u)²) > 0.
```

Thus each positive critical point satisfies `theta(t) = k pi`, with integer `k >= 1`, and is unique. Its initial enclosure is `[(k-1/2)pi/u, k pi/u]`. The map

```
F_k(t) = [k pi - atan(2 a t/u)] / u
```

has derivative of absolute value at most `2a/u²`. This quantity is checked to be below one for every retained measurement. Applying `F_k` to an interval containing the critical point preserves containment; contraction narrows it below the declared radius tolerance. A separate audit checks strict opposite signs of `theta(t)-k pi` at the final enclosure's endpoints, at higher precision. Monotonicity supplies uniqueness without trusting fixed-point convergence alone.

Possible critical indices are obtained by outward bounds on `theta(I_j)/pi`; none can be skipped. At the critical point,

```
h(t) = (-1)^k exp(-a t²) / sqrt(1 + (2at/u)²).
```

The direct and transformed value enclosures are intersected. Endpoint and critical-value candidates bound each scalar minimum and maximum. If a critical-point enclosure straddles an interval edge, including its entire value remains conservative; such cases are counted explicitly. The recorded grid has no such edge cases. The audit also retains an example in which the critical value lies strictly outside the endpoint-value hull, rejecting the shortcut of using endpoints alone.

The finite scalar ranges are sharp up to their certified numerical enclosures for the independent Cartesian boxes. This does not make the full recovery constraints optimal: different Gaussian rows share the same uncertain ordinates, and their marginal ranges forget those correlations. The omitted-zero and prime-tail bounds are also conservative. No optimal noise threshold or alternate number field is inferred from an unresolved candidate.

## Tail bounds and retained measurements

Each declared uncertainty radius also enlarges the moment calculation used in the inherited unconditional omitted-zero bound. Known selected boxes must remain positive and below the cutoff, and known unselected boxes must remain above it. The certificate at the final height still supplies the finite root count; this experiment does not infer the distance to a previously unobserved zero above that height.

For any finite-sum enclosure `S_range`, the row observation is `R = A(background - S_range) + [-E_zero, E_zero]`. The derivative routes use the original `R0` and the respective additional input allowance. Prime-tail variables remain in the inherited interval `[0, B]` and all measurement weights remain nonnegative.

The `single_cutoff` policy keeps 91 rows at one height. The `retained_prefix` policy keeps all 91-row sets at the tested heights up to the current one: 91, 182, 273, 364 or 455 rows. It shares the same 604 integer coefficient domains across them. Every exclusion is valid for any vector satisfying all retained rows. Adding rows cannot invalidate an earlier exclusion, and the monotone finite-domain closure can only shrink domains. The audit checks this property for every tested prefix and separately checks that wider uncertainty does not shrink the resulting domains on this grid. Neither property requires a heuristic ordering of the Gaussian widths.

## Independent checks and reproducibility

The [range producer](dedekind_ordinate_ranges.py) runs four methods, five heights, four radii and two retention policies at both 160 and 224 bits. A prior 160-bit probe is preserved and compared byte-for-byte at the case level with its corresponding full-grid cases.

The [audit](dedekind_ordinate_audit.py) reconstructs the original weight enclosures, verifies all observation metadata links, rounds outward to the `2^-192` grid and replays every coefficient deletion with integer arithmetic. It checks all 604 retained domains against independently multiplied-back polynomial factorizations, introduced only after producer results are frozen. It rejects deletion of a true coefficient and removal of prerequisite exclusions.

All reported turning points receive strict phase-bracket checks. Twelve scalar extrema calculations use a separate 80-decimal-digit mpmath implementation, independent secant solutions and direct cosine evaluations. These checks cover targets 2, 11 and 361 at heights 220 and 2000, at radii `5e-4` and `5e-3`, using the producer's exact dyadic machine-box endpoints. Numerical agreement supports the interval derivation but does not independently certify root completeness or the full explicit formula.

Use the pinned [runtime dependencies](source_requirements.txt). Extract `Measurements.zip` from the preceding checkpoint and `Ordinate_Audits.zip` from the [new checkpoint](../../docs/frontier/2026-09-13-uncertainty-delta/README.md) into a scratch directory. With `PYTHON` naming that environment and `AUDIT` the scratch directory:

```sh
$PYTHON code/frontier_verification/dedekind_ordinate_ranges.py --input "$AUDIT/Measurements.json" --precision 160 --deltas 5e-6 5e-5 5e-4 5e-3 --methods global derivative direct stationary --output "$AUDIT/Ranges_160.json"
$PYTHON code/frontier_verification/dedekind_ordinate_ranges.py --input "$AUDIT/Measurements.json" --precision 224 --deltas 5e-6 5e-5 5e-4 5e-3 --methods global derivative direct stationary --output "$AUDIT/Ranges_224.json"
$PYTHON code/frontier_verification/dedekind_ordinate_audit.py --directory "$AUDIT" --prior docs/frontier/2026-09-13-coupled-delta --output "$AUDIT/Ordinate_Audit.json"
$PYTHON code/frontier_verification/verify_ordinate_delta.py
```

The probe is included in the result archive; its exact command is in the execution receipts. The retained-evidence verifier checks hashes and transcript consistency recursively. It does not rerun the numerical producers or silently upgrade inherited mathematical claims.
