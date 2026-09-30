# Quadratic ordinate errors and certified coefficient bounds

The [shared-error checkpoint](SHARED_README.md) identified 81 of 91 prime-power coefficients through 361 after enlarging every certified ordinate interval by radius `0.005`. Retaining second-order terms with a certified cubic remainder identifies 83: coefficients 289 and 359 are both zero. Candidate sets also narrow at 128, 256 and 361. The retained inputs, 455 measurements, 7602 positive ordinates, 604 coefficient coordinates and original cutoff membership are unchanged.

The control that treats a displacement and its square as separate bounded coordinates also identifies 83. Restoring their exact relation tightens individual bounds, but produces no additional singleton on this proposal set. The two-target conic probes likewise add no singleton beyond the linear-program proposals. These limits are retained alongside the improvement.

## Second-order measurement model

Use the notation and inherited zero/prime tail bounds of the [first-order derivation](SHARED_README.md). Each enlarged machine interval has midpoint `t_j` and radius `r_j`; its actual displacement is `r_j y_j`, with `|y_j| <= 1`. For a measurement with `h(t)=exp(-a t²) cos(ut)` and positive normalization `A`, set

```
J_mj = 2 A_m r_j h'_m(t_j),
K_mj = A_m r_j² h''_m(t_j),
H_m = A_m/3 sum_j r_j³ sup_{t in I_j} |h'''_m(t)|.
```

Coordinates outside a row's certified cutoff contribute zero. Taylor's theorem bounds the omitted term in `2 A_m h_m` by `H_m`. The third derivative is

```
h'''(t) = exp(-a t²) [
  (-8a³t³ + 12a²t + 6au²t) cos(ut)
  + (-12a²ut² + 6au + u³) sin(ut)
].
```

The [basis instrument](dedekind_quadratic_ordinate.py) encloses this derivative over each full interval. It retains the original centers, first derivatives, unknown-zero bounds and one-sided prime tails. With `E_m = E_zero,m + H_m`, the rigorous system is

```
Wc + Jy + Kz + q = C + eta,
z_j = y_j², |y_j| <= 1,
|eta_m| <= E_m, 0 <= q_m <= B_m.
```

This models lost precision around the previously certified spectrum. It does not assert that arbitrary allowed displacement vectors are spectra of number fields. The known finite root counts and critical-line certificates are inherited; unobserved zeros still use the unconditional bound that permits off-line zeros.

## Scalar maxima and complete signed bounds

For any rational signed row vector `alpha`, combine coefficients before bounding the ordinate errors:

```
v_n = sum_m alpha_m W_mn,
d_j = sum_m alpha_m J_mj,
e_j = sum_m alpha_m K_mj.
```

For interval values enclosing `d_j,e_j`, choose exact outward dyadics `D_j >= |d_j|` and `E_j <= e_j`. For `|y|<=1`,

```
-d_j y - e_j y² <= D_j |y| - E_j |y|² <= S(D_j,E_j),

S(D,E) = D²/(4E)     if E>0 and D<2E,
         D-E         otherwise.
```

In the first case, completing the square proves the bound, attained at `|y|=D/(2E)`. In the second case, the maximum is attained at `|y|=1`. Equality at `D=2E` is included in the endpoint branch. A zero displacement is allowed in both cases.

For target `i`, sign `sigma=+1` or `-1`, and previously certified coefficient-domain endpoints `l_n,u_n`, the full bound is

```
sigma c_i <= upper(sum_m alpha_m C_m)
   + sum_j S(D_j,E_j)
   + sum_m |alpha_m| E_m
   + sum_m max(0,-alpha_m) B_m
   + sum_n max(l_n (sigma 1[n=i]-v_n),
               u_n (sigma 1[n=i]-v_n)).
```

Interval endpoint choices enclose every residual term, including all nuisance coefficients. A candidate is excluded only by a strict inequality against the complete upper bound. The arithmetic values from polynomial factorization are used only for an audit after inference; the initial domains are exactly the preceding 81-singleton spectral domains.

The independent-square control replaces `S(D,E)` by `D+max(0,-E)`, valid for independent `y in [-1,1]` and `z in [0,1]`. The first-order control reuses the preceding linear error model. All three start from the same preceding domains, use the same retained proposal collection, and iterate synchronous domain exclusions separately.

The [Lean module](proofs/QuadraticSupport.lean) kernel-checks ten real scalar results: vertex and endpoint bounds, the unit-interval upper bound, nonnegativity, signed coefficient reduction, the complete scalar bound, attainment, and two cone identities. Its successful axiom traces contain no `sorryAx`. This module does **not** formalize the Gaussian derivatives, Taylor theorem application, numerical intervals or coefficient inference.

## Proposal methods and their limits

The [LP instrument](dedekind_quadratic_recovery.py) proposes multipliers using separate square coordinates. It records 52 certificates over three rounds: 50 successful HiGHS interior-point solves and two existing opposite box bounds. Multipliers are rounded to the rational grid `1/10^9`; their validity is decided by the complete interval bound, independently of solver status.

The [conic instrument](dedekind_quadratic_conic.py) uses `y² <= z <= 1`, the convex hull of the scalar parabola segment. Its second-order cone contains `(z+1,2y,z-1)`, because

```
(z+1)² - [(2y)² + (z-1)²] = 4(z-y²).
```

The nonnegative first coordinate and squared cone inequality are equivalent to `y²<=z`. This equivalence is kernel checked separately from the floating solver. The model contains 15,808 variables and 32,526 constraint rows, including 7602 three-dimensional cones. The [Clarabel interface](https://clarabel.org/stable/python/getting_started_py/) and [cone definitions](https://clarabel.org/stable/api_cone_types/) describe the API and sign convention; executed Clarabel 0.11.1 is pinned in [quadratic_requirements.txt](quadratic_requirements.txt).

Two 30-second target probes retain two time-limit statuses and two successful solves. The 120-second continuation records one `AlmostSolved` and three `Solved` statuses. Their finite proposed multipliers receive the same rigorous bound checks. Unverified primal vectors are retained as proposals only. They do not establish feasibility of an integer coefficient assignment or a nonlinear spectrum.

The [union instrument](dedekind_quadratic_union.py) collects 100 proposals, with 15 distinct multiplier combinations, from the frozen, LP and both conic runs. Starting independently from the previous domains, its control counts are 81, 83 and 83. Five candidates are removed in either quadratic control; eight target domains remain:

- 64: 0 or 1; 81: 3 or 4; 125: 0 or 1; 128: 0, 1 or 2.
- 243: 0, 1 or 2; 256: 1, 2, 3 or 4; 343: 0 or 1; 361: 3 or 4.

No fixed-point or solver status proves these survivors jointly feasible.

## Independent checks and reproduction

The [exact audit](dedekind_quadratic_audit.py) rebuilds analytic bases at 160 and 224 bits and replays every retained objective. It separately rounds interval endpoints outward to `2^-192` and uses integers with common denominator `2^192 * 10^9`. For a vertex contribution, an exact integer ceiling of `D²/(4E)` restores that common scale. All residual, ordinate, cubic and omitted-tail contributions remain present. Exact and interval decisions must agree; all 604 independently established arithmetic coefficients must survive.

The [numerical audit](dedekind_quadratic_numeric.py) differentiates symbolically, checks 75 curvature and third-derivative cases with 80-digit mpmath, and computes two complete 7602-term displaced sums. Each gives a strictly positive residual beyond its quadratic prediction, enclosed by the cubic allowance. A retained scalar combination has an interior maximum strictly above both endpoints and zero. Its midpoint maximum is also checked by exact rational arithmetic. These are controls for omitted remainder and vertex terms, with explicitly shared analytic inputs.

The first numerical audit failed because its scalar comparison accidentally evaluated `-d*y-e*y` at the vertex instead of `-d*y-e*y*y`. A preserved diagnostic confirms the certificate bound by exact arithmetic. The corrected audit reruns the full checks. Earlier Lean setup and proof failures, their source versions, and a command-launch failure are retained. Final evidence and execution details are in the [quadratic checkpoint](../../docs/frontier/2026-09-13-quadratic-delta/README.md).

Use the pinned runtime and extract `Quadratic_Audits.zip` into a scratch directory. The exact recorded commands are in the checkpoint receipts. Core reproduction commands are:

```sh
$PYTHON code/frontier_verification/dedekind_quadratic_ordinate.py --prior docs/frontier/2026-09-13-shared-delta --precision 160 --output "$AUDIT/Quadratic_Frozen160.json"
$PYTHON code/frontier_verification/dedekind_quadratic_recovery.py --prior docs/frontier/2026-09-13-shared-delta --precision 160 --time-limit 15 --output "$AUDIT/Quadratic_160.json"
$PYTHON code/frontier_verification/dedekind_quadratic_conic.py --prior docs/frontier/2026-09-13-shared-delta --precision 160 --targets 128 361 --time-limit 30 --output "$AUDIT/Conic_Probe160.json"
$PYTHON code/frontier_verification/dedekind_quadratic_conic.py --prior docs/frontier/2026-09-13-shared-delta --precision 160 --targets 128 361 --time-limit 120 --output "$AUDIT/Conic_Extended160.json"
$PYTHON code/frontier_verification/dedekind_quadratic_union.py --directory "$AUDIT" --prior docs/frontier/2026-09-13-shared-delta --precision 160 --results Quadratic_Frozen160.json Quadratic_160.json Conic_Probe160.json Conic_Extended160.json --output "$AUDIT/Quadratic_Union160.json"
$PYTHON code/frontier_verification/dedekind_quadratic_audit.py --directory "$AUDIT" --prior docs/frontier/2026-09-13-shared-delta --results Quadratic_Frozen160.json Quadratic_160.json Conic_Probe160.json Conic_Extended160.json Quadratic_Union160.json --output "$AUDIT/Quadratic_Audit.json"
$PYTHON code/frontier_verification/dedekind_quadratic_numeric.py --prior docs/frontier/2026-09-13-shared-delta --result "$AUDIT/Quadratic_160.json" --output "$AUDIT/Quadratic_Numeric2.json"
$PYTHON code/frontier_verification/verify_quadratic_delta.py
```

New measurements selected for the declared uncertainty, tighter signed nonlinear error bounds, shared tails, and independently certified feasible or separating models remain active gates. The original unresolved local-factor square powers and all other research branches remain open where their earlier evidence leaves them.
