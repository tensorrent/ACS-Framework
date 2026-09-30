# Finite coefficient recovery from certified zeros

This continuation recovers all 91 coefficients `Lambda_K(p^k)/log(p)` at prime powers through 361 for the specified field `K=Q(zeta_5)`. The direct spectral method determines 89 at height 2000. A separate inference using general degree-four local constraints determines the remaining two. The computation uses neither the known splitting residues nor actual neighboring coefficients in its estimates or error bounds. It is a resolution audit conditional on the field invariants and analytic identity, not statistical blinding, identification of an unknown field, or an independent natural-operator construction.

The [checkpoint](../../docs/frontier/2026-09-13-recovery-delta/README.md) packages inputs, results, unsuccessful attempts and source identities. All older dated checkpoints and instruments retain their previous bytes.

## Finite certificates through height 2000

The positive counts are 1517 for Riemann zeta, 2028 for Conrey character 2 modulo 5, 2028 for character 4, and 2029 for character 3. The total is 7602, with all intervals disjoint even across factors. All 528 inherited intervals through height 220 overlap the new intervals and retain identical 20-decimal rounding cells.

For a primitive nonprincipal character with parity `a`, use

`Lambda_chi(s)=(5/pi)^((s+a)/2)*Gamma((s+a)/2)*L_chi(s)`.

Its entire continuation has exactly the nontrivial L-zeros; the trivial zeros cancel gamma poles. The [primitive functional equation and conjugate-character convention](https://dlmf.nist.gov/25.15) give `Lambda_chi(s)=epsilon_chi*Lambda_chibar(1-s)`. The constant epsilon drops out of argument changes. On `Re(s)=2`, the Dirichlet series bounds `|L(s)-1|<=zeta(2)-1<1`, so a global argument lift is

`V_chi(t)=t/2*log(5/pi)+Im logGamma((2+a+it)/2)+arg L_chi(2+it)`.

Here `logGamma` is the analytic branch, not the principal logarithm of the gamma value. [python-flint documents this distinction](https://python-flint.readthedocs.io/en/latest/acb.html#flint.acb.lgamma). The right-side change for rectangle `[-1,2] x [-1/2,T]` is `V_chi(T)-V_chi(-1/2)`; the left-side change is `V_chibar(1/2)-V_chibar(-T)`.

Fold each horizontal half with real part below 1/2 through the functional equation. This leaves four L-paths with real part between 1/2 and 2: conjugate character from `2+i/2` to `1/2+i/2`; original character from `1/2-i/2` to `2-i/2`; original from `2+iT` to `1/2+iT`; and conjugate from `1/2-iT` to `2-iT`. Add the analytic log-gamma endpoint change on each path; the conductor factor has constant argument there.

Each accepted L-path segment has an interval image excluding zero, with endpoint quotient in the right half-plane. The image lies in a convex rectangle disjoint from zero, so its continuous argument change equals the recorded principal endpoint change. Summing the four horizontal and two vertical changes encloses one integer winding number. The 160-bit run starts with 64 segments per half; the 224-bit replay starts with 96 and independently subdivides. Seeding before native evaluation avoids the pathological wide-interval evaluations retained among the unsuccessful attempts.

The initial 0.1-height Hardy scans match all three finite counts. Disjoint brackets with opposite strict signs account for at least that many zeros; equality with the total contour count proves their simplicity and completeness in the rectangle. The refinement uses a secant proposal only to choose endpoints, then proves opposite interval signs inside the original bracket; unsuccessful proposals fall back to bisection. Every endpoint sign is replayed at 224 bits. Seven selected roots per character use a separate 60-digit mpmath Hurwitz sum, including the closest pair. Riemann indexed interval roots and total counts are replayed at 224 bits, with three selected 90-digit mpmath roots. Interval replays share FLINT/Arb; mpmath location checks do not independently prove completeness. No global RH or GRH is assumed or established.

## A coefficient enclosure without an arithmetic oracle

Use the Fourier pair from the [preceding derivation](EXPLICIT_README.md):

`h(t)=exp(-a*t^2)*cos(u*t)` and
`g(x)=(exp(-(x-u)^2/(4a))+exp(-(x+u)^2/(4a)))/(4*sqrt(pi*a))`.

The full zero sum `S` equals `P+log(125)*g(0)+G-Q`, where `P=2*exp(a/4)*cosh(u/2)` and `Q=2*sum Lambda_K(n)/sqrt(n)*g(log n)`. The identity and unconditional logarithmic-derivative premises are those already sourced in the preceding checkpoint from [Belabas–Friedman](https://arxiv.org/pdf/1305.0035) and [Grenie–Molteni](https://arxiv.org/pdf/1407.1375); the GRH-dependent later bounds in those papers are not used here.

At target `m=p^k`, set `u=log m`, `A=2*sqrt(pi*a*m)/log p`, and `D=1+exp(-u^2/a)`. Then

`A*(P+log(125)*g(0)+G-S)=c_m*D+ell`, with `c_m=Lambda_K(m)/log p` and `ell>=0`.

For every degree-four number field, prime-ideal Euler factors give integer `0<=c_(q^j)<=4`; all non-prime-power coefficients vanish. The decoder generates all 604 rational prime powers through `X=4096` by a sieve and bounds the leakage by

`L_finite=sum_(n=q^j<=X,n!=m) 4*log q/log p*sqrt(m/n)*(exp(-(log n-u)^2/(4a))+exp(-(log n+u)^2/(4a)))`.

The omitted prime tail is at most `A*E_Q`, with `y=log X-u-a>0` and

`E_Q=8*sqrt(a/pi)*exp(u/2+a/4-y^2/(4a))*(1+(u+a)/y)`.

This uses only `0<=Lambda_K(n)<=4 log n` and the decreasing integral comparison derived previously. No actual coefficient is substituted even for a neighbor already expected to vanish.

The unknown-zero moment now uses **no prime partial sum**. With

`C=3/2+log(125)/2-2 log(2*pi)+2 psi(2)` and `M_T=sum_(positive gamma<T) 3/(9/4+gamma^2)`,

set `U_T=C-M_T`. The logarithmic derivative at 2 and nonnegative Euler coefficients imply the unknown positive moment is at most `U_T`. This deliberately forgoes the sharper bound that used known arithmetic in the preceding identity audit. Here `U_220` is about 0.249492 and `U_2000` about 0.207075.

For an unknown zero `beta+i gamma`, the strip condition gives `Re(1/(2-rho))>=1/(4+gamma^2)`. Also `|h((rho-1/2)/i)|<=exp(-a*gamma^2+a/4)*cosh(u/2)`, allowing off-line zeros. Thus

`E_zero=U_T*Phi(a,T)*exp(a/4)*cosh(u/2)`, where

`Phi=(4+T^2)*exp(-a*T^2)` if `a*(4+T^2)>=1`, and `Phi=exp(4a-1)/a` otherwise.

The second case is the maximum at `gamma^2=1/a-4`; it keeps the bound valid when the Gaussian is too narrow for the available height. All finite roots enter as intervals. Both signs of height are supplied by the complete conjugate union, rather than assuming each complex character is symmetric about the real axis.

The gamma term is integrated with interval arithmetic on `[1e-20,180]`, retaining every segment and both omitted-end bounds. Rational breakpoints around the Gaussian peak improve evaluation; float proposals choose those breakpoints but play no role in their certified integrals. Different precision runs use different partitions. The inherited global derivative bound `|g''|<=3/(4a sqrt(pi*a))` bounds the lower omitted interval, while the hyperbolic denominator bounds the upper interval.

Let `R` be the interval estimate `A*(P+log(125)*g(0)+G-S_T)` widened by `A*E_zero`, and let `L>=L_finite+A*E_Q`. Retain `c` in `{0,1,2,3,4}` precisely when `R` overlaps `[cD,cD+L]`. Every true coefficient must survive; a singleton therefore identifies it under the declared premises. Root and quadrature errors are already propagated into R. The largest unwidened-estimate radius over the 455 cases is below `8e-27`.

For each target and height, the program chooses one of 27 declared widths by minimizing the computed conservative bound `2*A*E_zero+L`. Choosing the width uses no coefficient estimate or expected answer. This selection bound omits the separately propagated finite arithmetic radius, so it is a planning criterion, not a proof that the chosen width is globally optimal. All 27 budgets remain in the result. Candidate intersections across heights are logical intersections, not independent statistical trials.

## Local inference and what remains unidentified

[Milne, Theorems 3.34 and 3.35](https://www.jmilne.org/math/CourseNotes/ANT.pdf), supply `sum e_j*f_j=4` and ramification exactly at discriminant divisors. A local factor gives `c_(p^k)=sum_(f_j divides k) f_j`. The second inference stage enumerates all five unramified degree partitions and all six ramified `(e,f)` multisets, then retains those consistent with the direct candidate sets. It does not assume that K is Galois or use a residue modulo 5.

At height 2000, target 256 retains all five direct candidates because the conservative neighboring-prime bound is broad. The independently recovered coefficients at 2 and 4 are zero, forcing the sole degree-four unramified residue degree 4, hence `c_256=4`. Target 361 retains `{3,4}` directly; the local constraints retain `{4}`, compatible with two residue-degree-2 primes above 19. The ramified prime 5 retains `(e,f)=(4,1)` from the inferred power coefficients.

All 91 target coefficients are then singletons, but **48 of 72 rational primes still have two admissible local degree partitions**. Their observed prime coefficient is zero and their square is outside the target range. The alternatives `(2,2)` and `(4)` first differ at the square, with coefficients 4 and 0. The next powers range from 23^2=529 to 359^2=128881. These are model ambiguities remaining after the finite recovery, not failed numeric comparisons.

More generally, write `n_f` for the number of prime ideals with residue degree f. Four coefficients give `n1=c1`, `n2=(c2-c1)/2`, `n3=(c3-c1)/3`, `n4=(c4-c2)/4`, by subtracting the divisor sums. This determines residue-degree multiplicities for degree four. It does not generally determine individual ramification indices: the ramified pairs `(e,f)=[(1,1),(3,1)]` and `[(2,1),(2,1)]` both give local factor `(1-p^-s)^-2` and every coefficient equal to 2. The exact enumeration groups these two models together. The full sequence has period dividing 12 since each possible f divides 12. This generic ambiguity is not a claim that either model occurs at the prime 5 of the present field.

## Cross-method controls and continuation

The 160-bit grid has 455 cases: all 91 targets at heights 220,600,1000,1500,2000. Direct singleton counts are 46,69,79,86,89; after local inference they are 56,75,84,90,91. The 224-bit run repeats all 91 final cases with matching candidates. A separate 70-digit mpmath implementation recomputes every final zero sum, gamma integral, finite leakage and unwidened estimate. Its prime-power inventory uses integer trial division rather than the producer sieve.

Only after the decoder results are frozen does the validator factor the fifth cyclotomic polynomial over each relevant finite field. Multiplying the factors back verifies the decomposition, and the resulting coefficient agrees with every retained set across all 455 cases. Ordered degree compositions independently reproduce the local-model enumeration. A source audit checks the decoder imports and its only modulo expressions: local `discriminant % p` and `k % f`. This establishes the inspected executable dependency boundary, not a proof against arbitrary future changes.

Seven variants are tested on all 455 cases. Omitting pole, gamma, negative zeros, or the zero-tail/leakage allowance, and reversing the zero sign each excludes the true coefficient somewhere. Omitting the discriminant term excludes it nowhere at these selected widths; all 455 such tests remain inconclusive. The narrower prior zero-frequency experiment still supplies its separate discriminant control.

Next gates include coupled interval constraints that use already certified neighboring coefficients, adaptive target/height/precision budgets, and the 48 unresolved local-factor squares. At fixed T, taking a toward zero makes the moment-based scaled tail bound grow like `1/sqrt(a)`; it cannot justify an unsmoothed recovery limit. For a fixed target, the crude C-bound would tend to zero along `T^2=kappa*log(1/a)/a` with `kappa>1/2`, but this observation does not supply the required unbounded certificates. A finite root-radius bound is `2*A*N*delta*(sqrt(2a/e)+u)` when each of N positive roots has radius at most delta; higher cutoffs require adequate root precision as well as height. Formal analytic verification, statistical calibration, field/operator identification and physical links retain their own gates.

## Reproduction

Use the pinned [requirements](source_requirements.txt). In a scratch directory run `dirichlet_extended_certificate.py --character c --top 2000 --precision 160 --output character-c.json` for c=2,3,4, then `dirichlet_strip_replay.py --certificate character-c.json --output replay-c.json`. Run `riemann_recovery_certificate.py --top 2000 --precision 160 --output riemann-160.json` and its `riemann_recovery_replay.py` counterpart. The exact recorded commands identify all paths.

`dedekind_recovery_inputs.py` combines those files and checks both prior archives. `dedekind_coefficient_recovery.py --input Recovery_Inputs.json --precision 160 --output Recovery_160.json` runs all five heights; add `--heights 2000 --precision 224` for the final replay. `dedekind_recovery_audit.py` takes `--input`, `--low`, `--high`, `--decoder`, and `--output`; `dedekind_local_identifiability.py` takes `--recovery` and `--output`. The retained-evidence verifier checks identities and recombines reported enclosures without rerunning root certification, quadrature or mpmath.
