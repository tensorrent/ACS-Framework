# Coupled finite spectral recovery

The [preceding recovery](RECOVERY_README.md) treated all other prime-power coefficients as independent nuisances when estimating each target. This continuation lets the same unknown coefficient occur in all measurement inequalities. It recovers all 91 targets through 361 at height 600, using only 1822 certified positive roots, coefficient integrality and the universal degree-four bounds. Local power relations are a separate optional inference. All earlier instruments and certificates remain unchanged.

At height 220, the retained inequality model has two distinct feasible integer target assignments. Six other remaining pairs are excluded by explicit separating certificates. This is a proved limitation of this particular relaxation; it is not a statement that another number field has the same zeros. Adding the previously established general local relation at the prime 19 resolves that ambiguity, giving all 91 targets at height 220 under that additional premise.

## Measurement boundary and common unknowns

`dedekind_coupled_inputs.py` extracts only the field invariants, root intervals, measurement labels, widths, pole, discriminant, gamma and finite zero terms from the immutable prior archive. It does not import any candidate set, local model or held-out coefficient. The widths were selected in the previous pass using universal leakage bounds, without using expected coefficient values.

For a measurement centered at `m=p^k`, let `u=log m`, `A=2 sqrt(pi*a*m)/log p`. For each rational prime power `n=q^j<=X=4096`, define the positive weight

`w_mn=log q/log p * sqrt(m/n) * [exp(-(log n-u)^2/(4a))+exp(-(log n+u)^2/(4a))]`.

There are 604 unknown coefficients `c_n` through X, each initially in `{0,1,2,3,4}`. The explicit formula and bounds derived in [RECOVERY_README.md](RECOVERY_README.md) give

`sum_n w_mn*c_n + q_m = r_m`, where `r_m in R_m` and `0<=q_m<=B_m`.

Here R is reconstructed from the recorded background and zero terms, including the unconditional unknown-zero error; B bounds the omitted prime tail. The moment bound is `C-M_T`, with no arithmetic partial sum. Off-line unknown zeros remain allowed. Each true coefficient vector satisfies every row simultaneously. The model relaxes the correlations between omitted tails in different rows, as well as all local Euler power relations.

All critical intervals are serialized as exact dyadic midpoint/radius pairs. Printed broad intervals are not used to decide candidates. The coefficient matrix is deterministically reconstructed and identified by a per-row hash rather than duplicating its dense entries in every result.

## Monotone interval exclusion

In one synchronous round, every coefficient retains its previously justified integer domain. For any target candidate, form the smallest and largest possible contribution from the other domains using positive weight bounds and the prime-tail interval. Exclude the candidate only if that whole row range lies strictly above or below R. Each deletion stores the responsible row, sign of separation, strict interval gap and prior-domain hash.

Synchronous rounds make dependencies explicit. A candidate is removed using the state at the beginning of its round; later rounds may use that removal. The true coefficient vector survives by induction. Finite domains ensure termination, but a surviving candidate need not extend to a jointly feasible integer vector.

Both 160-bit and 224-bit runs give identical final domains. For heights 220,600,1000,1500,2000, the numbers of uniquely recovered target coefficients are **78,91,91,91,91**. Their exclusion-round counts are 12,4,5,2,2. The height-600 measurements also determine the incidental coefficient at 367 as zero; the higher-height grids use different widths and do not automatically preserve that extra observation.

## A different route: continuous dual bounds and integer tightening

Using outward bounds `w^-<=w<=w^+`, each observation supplies

`sum w^-_n*c_n <= R^+` and `-sum w^+_n*c_n <= -R^-+B^+`.

Write this system `G*c<=b`. A continuous linear program proposes lower and upper bounds on each target, starting with the box `[0,4]^604`. [SciPy's HiGHS interface](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html) supplies the numerical solution and inequality marginals; its success status is not accepted as proof. Multipliers are made nonnegative and rounded to exact rationals on a denominator-10^9 grid.

For any nonnegative multiplier vector lambda and sign `s in {-1,1}`, put `d=s*e_i-lambda*G`. If `l_j<=c_j<=u_j`, then

`s*c_i <= lambda*b + sum_j max(l_j*d_j,u_j*d_j)`.

This follows directly by adding weighted valid inequalities and bounding the remaining linear functional on the box. It does not require an optimal, feasible or exact dual solution from the solver. Interval arithmetic encloses the entire right side. A zero multiplier vector simply returns the existing box bound. Integer rounding tightens the domains, and new LP bounds use only boxes justified in previous rounds.

The initial continuous certificates identify **76,90,91,91,91** targets at the five heights. Iterated integer box tightening identifies **89,91,91,91,91**. At height 220 its remaining domains are `c359 in {0,1}` and `c361 in {1,2,3,4}`. At height 600 one further round identifies the last coefficient, 256. This route does not import domains from the interval-exclusion algorithm.

## Exact replay and deliberate certificate errors

The independent replay rounds weight and measurement bounds outward to the fixed grid `2^-192`. All subsequent exclusion arithmetic uses Python integers. Multipliers retain their exact denominator-10^9 grid. This avoids depending on the producer's Arb additions and comparisons, while sharing its analytically justified weight and measurement enclosures.

Across two five-height precision runs and fourteen uncertainty runs, **8601 candidate exclusions** are verified by strictly positive integer gaps. **970 dual certificates** are independently recombined, including integer-tightening rounds. All 604 coefficients in each interval case retain the value obtained by a separate polynomial factorization performed only after inference outputs are frozen.

The audit rejects four deliberately invalid certificate steps: deleting the true coefficient, using a later-round witness without its prerequisite exclusions, allowing a negative dual multiplier, and omitting the residual support correction. The last error would falsely bound a coefficient by zero even when the unchanged box permits four. These are checks of certificate logic, not new claims about the analytic formula or zero completeness.

## The two surviving height-220 target pairs

Enumerate all eight pairs left by the dual refinement. With each pair fixed, a numerical phase-I LP proposes a separating multiplier. The proof is elementary: if

`min_(c in box) lambda*G*c - lambda*b > 0`,

then no point in that box satisfies the inequalities. Nonnegative rational multipliers and outward interval arithmetic prove six exclusions; exact integer replay confirms them. The surviving pairs are `(c359,c361)=(0,4)` and `(1,1)`.

A mixed-integer solver then proposes a full 604-coordinate vector for each surviving pair. Both vectors pass strict interval inclusion in every one of the 91 measurement rows with the permitted prime-tail variable set to zero. Exact integer replay confirms those inclusions. The vectors differ at 359,361,373,379,383,389,397,401. The first vector also differs from actual field arithmetic at some nuisance coordinates; it is a witness for the relaxed inequalities, not a substitute arithmetic table.

Therefore no method using only this exact set of inequalities and integer coefficient boxes can select a unique target pair. More measurements, sharper or linked tail bounds, or additional arithmetic information could change that conclusion. Failure of the earlier probe that held all nuisance coordinates at their true values did not prove infeasibility; its seven unsuccessful trials are retained alongside the successful free-nuisance witnesses.

There is an explicit optional arithmetic bridge. The inferred coefficient at 19 is zero, and `19` does not divide the given discriminant. Among general unramified degree-four partitions, only `(2,2)` or `(4)` has prime coefficient zero. Their square coefficients are 4 and 0. Intersecting this with the inferred square domain `{1,2,3,4}` forces `c361=4`; the checked pair exclusions then force `c359=0`. Thus all 91 targets at height 220 are identified after adding this general local relation. The underlying degree and ramification facts are [Milne, Theorems 3.34–3.35](https://www.jmilne.org/math/CourseNotes/ANT.pdf), as already used in the prior checkpoint. No specific residue modulo 5 or Galois restriction is needed for this bridge.

## Additional ordinate uncertainty

The uncertainty experiment enlarges each already certified root interval by an additional radius delta, retaining its certified membership below the cutoff. It recomputes the zero moment with those enlarged intervals. It also adds the finite-sum bound

`E_input=2*A*N*delta*(sqrt(2a/e)+u)`.

Indeed `|h'(t)|<=2a|t| exp(-a*t^2)+u exp(-a*t^2)<=sqrt(2a/e)+u`; the mean-value theorem and sum over both signs give the bound. This is a conservative loss-of-ordinate-precision model around the certified data, not a claim that perturbed ordinates are zeros of another field.

At both heights 1000 and 2000, every tested radius from `5e-21` through `5e-6` preserves all 91 target singletons. At `5e-4`, 67 and 55 respectively remain singletons. Every retained domain includes the independent arithmetic coefficient, and domains expand monotonically as delta increases at a fixed height and width grid.

The 67-versus-55 comparison does not show that more zero data intrinsically reduces information. The two grids use different widths and the coarse error allowance grows with N; one can always retain a useful lower-cutoff measurement. These are sufficient bounds at declared radii, not optimal precision thresholds. A per-root derivative bound, noise-aware width selection and combined-cutoff measurements are concrete next improvements.

## Remaining scope and reproduction

For the original through-361 cohort, 48 local factors remain ambiguous between residue-degree patterns after all target coefficients are recovered. The earlier [R14 audit](../../docs/frontier/2026-09-13-recovery-delta/Local_Identifiability.json) still applies. If the incidental prime 367 is added to that cohort, its unresolved square is 134689. Residue-degree multiplicities still do not generally identify individual ramification indices.

This pass reuses certified roots and gamma terms rather than claiming new root counts or quadrature. The model remains conditional on the stated field invariants and the sourced explicit formula. It does not establish global RH/GRH, statistical calibration, an unknown-field identification, or a natural operator. The queue carries the other physical, topological and private-input gates forward.

Use the pinned [runtime requirements](source_requirements.txt). `dedekind_coupled_inputs.py` takes `--prior` and `--output`. `dedekind_coupled_recovery.py` takes `--input`, `--precision`, optional `--heights` and `--deltas`, and `--output`. `dedekind_coupled_dual.py` supplies the first dual certificates; `dedekind_coupled_dual_refine.py` takes them via `--initial`. The branch certificate, integer witness and exact audits are separate entry points. All eleven exact computation commands are preserved in the [checkpoint receipts](../../docs/frontier/2026-09-13-coupled-delta/Execution_Receipts.json). The retained-evidence verifier checks hashes and transcript relationships; the recorded exact replay is the computation validating every inequality witness.
