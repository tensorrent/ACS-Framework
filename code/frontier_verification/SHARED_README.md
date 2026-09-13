# Shared ordinate errors in spectral recovery

The [previous uncertainty calculation](ORDINATE_README.md) retained 455 Gaussian measurements and identified 73 of 91 coefficients at additional ordinate radius `0.005`. Optimizing the same independent row ranges with validated dual certificates leaves that count unchanged. Accounting for each ordinate's common effect across measurements identifies 81 coefficients under the same declared uncertainty and inherited analytic assumptions.

## A certified common-variable model

There is one normalized displacement `y_j` per included ordinate, with `|y_j| <= 1`. The same `y_j` appears in every measurement containing that ordinate. Different ordinates have independent displacement coordinates. This is not a single global shift of the entire spectrum.

Let the outward-rounded enlarged box be `I_j = [t_j-r_j, t_j+r_j]`. It encloses the original certified interval plus the declared radius `delta=0.005`. For measurement `m`, write

```
h_m(t) = exp(-a_m t²) cos(u_m t),    u_m = log(m),
C_m = A_m [background_m - 2 sum_{j included at T_m} h_m(t_j)],
J_mj = 2 A_m r_j h'_m(t_j),
T_m = A_m sum_{j included at T_m} r_j² sup_{t in I_j} |h''_m(t)|.
```

Set `J_mj=0` when the ordinate is beyond that measurement's cutoff. The scale `A_m`, nonnegative prime-power weights `W_mn`, and unknown-zero and prime-tail bounds are inherited from the [recovery](RECOVERY_README.md) and [coupled](COUPLED_README.md) derivations. The unknown-zero allowance is recomputed on the enlarged boxes for each cutoff.

Taylor's theorem on the real interval gives

```
2 A_m h_m(t_j+r_j y_j)
  = 2 A_m h_m(t_j) + J_mj y_j + remainder_mj,
|remainder_mj| <= A_m r_j² sup_Ij |h''_m|.
```

The second derivative used in the interval evaluation is

```
h''(t) = exp(-a t²) [(4a²t² - 2a - u²) cos(ut) + 4aut sin(ut)].
```

It is separately obtained by symbolic differentiation and checked numerically with mpmath derivatives. Every term in the finite sum is included in the remainder bound. Defining `E_m = E_zero,m + T_m`, the actual measurements obey the conservative system

```
sum_n W_mn c_n + sum_j J_mj y_j + q_m = C_m + eta_m,
|y_j| <= 1,    |eta_m| <= E_m,    0 <= q_m <= B_m.
```

Here `q_m` is the omitted prime-power contribution, with inherited bound `B_m`. There are 604 coefficient coordinates through 4096, 7602 ordinate coordinates, and 455 rows. Original root counts, cutoff membership and critical-line certificates for the known finite roots are retained. The unobserved-zero bound still permits off-line zeros. No new root-completeness or global RH/GRH assertion is made.

The initial coefficient domains are exactly the previously certified stationary-prefix domains at this uncertainty. Their archived source, audit, measurement and domain hashes are retained. No expected coefficient, polynomial factorization or local power relation is introduced as an inference seed. The experiment still models lost precision around certified data, not arbitrary noisy-center shifts or zeros of a perturbed field.

## Signed combinations retain cancellation

Take any rational signed row vector `alpha`. It need not have positive entries. Put `v_n = sum_m alpha_m W_mn` and `z_j = sum_m alpha_m J_mj`. The common-variable identity implies

```
sum_n v_n c_n <= sum_m alpha_m C_m
                 + sum_j |z_j|
                 + sum_m |alpha_m| E_m
                 + sum_m max(0,-alpha_m) B_m.
```

The first term is evaluated as a signed interval sum. The ordinate allowance is the sum of absolute values **after** combining measurements at each ordinate. This can be much smaller than adding the separate row allowances `sum_m |alpha_m| sum_j |J_mj|`.

For target coordinate `i` and sign `sigma` in `{-1,+1}`, define `d_n = sigma*1(n=i)-v_n`. If a previously certified coefficient domain has endpoints `l_n,u_n`, then

```
sigma c_i <= [the preceding bound]
             + sum_n max(l_n d_n, u_n d_n).
```

Interval endpoint choices bound the residual support conservatively. Every coordinate, including all nuisance prime powers, is retained. A candidate is deleted only when `sigma*candidate` is strictly greater than this complete upper bound. All row, prime-tail, unknown-zero, linearization and coefficient-residual terms remain present.

The initial coefficient-32 probe combines 154 signed rows. Its shared ordinate allowance is about 0.7414, versus about 5.6475 if their separate allowances were added. The complete certified objective bound is below one, so coefficient 32 is zero. This demonstrates an improvement from common-error information; the separate-row optimization did not produce that deletion.

## Proposal solvers and independent checks

The [first instrument](dedekind_shared_ordinate.py) records both the marginal optimization and a two-target shared probe. Its probe preserves two 90-second solver limits; those trials contribute only already valid zero-multiplier box bounds. A later [bounded proposal instrument](dedekind_shared_recovery.py) uses the HiGHS interior-point route. All 48 requested solves in that run finish successfully. Eight opposite bounds need no additional solve after a singleton is established; zero multipliers certify the existing opposite box bound.

Solver output only proposes coefficients on the `1/10^9` rational grid. The signed-combination proof is valid for any such coefficients, independent of solver status, floating-point feasibility or optimality. Neither solver success nor a round without new exclusions establishes joint feasibility of the remaining integer candidates.

The [independent audit](dedekind_shared_audit.py) rechecks 36 marginal certificates, recomputes all four probe and 56 main shared certificates at 160 and 224 bits, and validates their decisions with exact integer arithmetic after outward rounding to `2^-192`. Shared certificate quantities then have common denominator `2^192 * 10^9`. All final coefficient domains are checked against the independently established arithmetic values retained from the preceding checkpoint.

Seventy-five 80-digit mpmath cases verify normalized first derivatives and second derivatives at box endpoints and centers. Two complete 7602-term finite center sums are recomputed independently, using the inherited background interval's midpoint. These checks concern the new linearization and recentering; they do not independently recompute the gamma integral or certify the original zero counts.

Three explicit controls show why prerequisite coefficient domains, the Taylor remainder, and separate displacement coordinates cannot be dropped. One allowed scalar displacement produces a finite change strictly larger than its linear support alone. Two independent ordinate displacements produce a linear change strictly larger than the absolute value of their summed coefficients; the correct support is the sum of absolute values.

## Results and continuation

Eight additional target coefficients become singletons: 32, 257, 269, 271, 281, 283, 311 and 313. Additional candidates are removed at 125, 243 and 343. The remaining ten targets are 64, 81, 125, 128, 243, 256, 289, 343, 359 and 361. Their complete domains, each certificate, solver limits and audit results are retained in the [checkpoint](../../docs/frontier/2026-09-13-shared-delta/README.md).

The remainder still adds each row's absolute curvature allowance separately. A next step is to bound the curvature of signed combinations, or to retain common quadratic displacement terms with certified cubic remainders. Noise-aware widths, relations between retained tails, and explicit feasibility or separating certificates are separate continuation gates. No optimum noise threshold, actual-field nonidentifiability or research exhaustion follows from the ten surviving domains.

Use the [pinned dependencies](source_requirements.txt), and extract `Shared_Audits.zip` to a scratch directory for the independent audit. For example:

```sh
$PYTHON code/frontier_verification/dedekind_shared_ordinate.py --prior docs/frontier/2026-09-13-uncertainty-delta --precision 224 --modes marginal --output "$AUDIT/Marginal_224.json"
$PYTHON code/frontier_verification/dedekind_shared_ordinate.py --prior docs/frontier/2026-09-13-uncertainty-delta --precision 160 --modes shared --targets 32 361 --max-rounds 1 --output "$AUDIT/Shared_Probe160.json"
$PYTHON code/frontier_verification/dedekind_shared_recovery.py --prior docs/frontier/2026-09-13-uncertainty-delta --precision 160 --time-limit 15 --output "$AUDIT/Shared_160.json"
$PYTHON code/frontier_verification/dedekind_shared_audit.py --directory "$AUDIT" --prior docs/frontier/2026-09-13-uncertainty-delta --output "$AUDIT/Shared_Audit.json"
$PYTHON code/frontier_verification/verify_shared_delta.py
```

The current [SciPy documentation](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs-ipm.html) describes the interior-point route and result statuses; its online version differs from the pinned runtime. The executed runtime and all exact commands are retained separately. The retained-evidence verifier checks history and transcript integrity; it does not rerun optimizers, numerical bases or the full mathematical audit.
