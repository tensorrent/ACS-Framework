# Prime-gap Compression Law past φ(m) = 24, and F_N stationarity at N = 200 (22 October 2026, pass 2)

Two VERIFY items from the 22 October candidate list: the monograph's planned
F_N run at N = 200 zeros and p ≤ 15×10⁶ (candidate 77), and the prime-gap
note's open question whether the Compression Law continues past φ(m) = 24
(candidate 61). Both were run on 23 October 2026 (UTC) with the pinned Python
(Python 3.12.3, numpy 2.2.6, scipy 1.15.3, mpmath 1.3.0), single-threaded BLAS, from scripts
in the session scratch directory (`scratchpad/actionable2/mpg-run2/`). Nothing
was written into a tracked path; `git status --short` after the runs showed
only this file and the files listed at the end. The cards that interpret these
numbers are in [open problems, monograph section](open_problems_2026-10-22.md#monograph-sigma-synthesis-prime-gap-operator-frontier-branches).
Line numbers refer to commit `5417173`.

## (B) F_N stationarity at N = 200 zeros, p ≤ 15×10⁶ (candidate 77)

**What the monograph says.** `papers/Form_Function_and_Asymmetry.tex:875-879`:
"segment-wise regression of $F_{25}(x)$ on $x \in [\ln 2, \ln(10^4)]$ gives slope
$p$-value consistent with stationarity [...] extension to $N = 200$ is in
progress". `:2309-2314`: "$N = 25$ Riemann zeros computed via
\texttt{mpmath.zetazero} at 50 decimal digits. Evaluation at $x = \ln p$ for all
primes $p \leq 10^4$ (1229 primes). Segment-wise regression over 8 segments.
\emph{Scaling to $N = 200$ zeros and $p \leq 15 \times 10^6$ is planned}". The
monograph prints no slope or p-value.

**The instrument.** `code/acs_codebase/extras/fn_stationarity_fast.py`
(sha256 `8e38341c919cd87a…`; header: "SCALED VERSION: N=25 zeros, primes to
10^4 [...] For M3: change N_ZEROS=200, PRIME_LIMIT=15000000, mp.dps=100"). It
evaluates $F_N(x)=\sum_k A_k(\tfrac12\cos\gamma_k x+\gamma_k\sin\gamma_k x)$,
$A_k = 1/(\tfrac14+\gamma_k^2)$, at $x=\ln p$, splits the primes into 8
equal-*count* segments, and fits an OLS line to the segment means and
population standard deviations against the segment index. It prints slopes,
not p-values. The extras README says the folder is unverified; this is the
only script in `code/` that implements the monograph's parameters.

**Runs.**

| # | Method | N | p ≤ | primes | mean slope (p) | std slope (p) | off-line (σ = 0.55 on γ₁) std slope (p) | wall |
|---|---|---:|---:|---:|---|---|---|---:|
| 1 | archived script, mpmath 50 dps, unmodified copy | 25 | 10⁴ | 1229 | 6.8449e-04 | −3.6058e-03 | ratio printed "1×" | 3.6 s |
| 2 | float64 port, zeros from the 100k table | 25 | 10⁴ | 1229 | 6.8449e-04 (0.897) | −3.6058e-03 (0.244) | −4.2139e-03 (0.301), ratio 1.2 | 0.1 s |
| 3 | archived script with `N_ZEROS = 200` (one-line edit), mpmath | 200 | 10⁴ | 1229 | 2.3730e-04 | −2.0146e-03 | — | 62 s |
| 4 | float64 port | 200 | 10⁴ | 1229 | 2.3730e-04 (0.966) | −2.0146e-03 (0.431) | −2.5397e-03 (0.454), ratio 1.3 | 0.1 s |
| 5 | float64 port | 25 | 15×10⁶ | 970,704 | −1.1397e-03 (0.864) | −6.7575e-03 (0.022) | −1.0688e-02 (0.048), ratio 1.6 | 9.6 s |
| 6 | **float64 port, the planned run** | **200** | **15×10⁶** | **970,704** | **−1.2624e-03 (0.855)** | **−6.2834e-03 (0.026)** | −1.0608e-02 (0.044), ratio 1.7 | 58.7 s |
| 7 | equal-*width* windows (W = 1 in x, x ≥ 5; second method) | 200 | 15×10⁶ | 970,704 | — | +5.9731e-04 per window (0.555) | **+3.4089e-03 (0.003)**, last/first 1.333 | 64 s |

Commands (from `scratchpad/actionable2/mpg-run2/`, `OMP_NUM_THREADS=1`, `Z = code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt`):
1: `acs-venv/bin/python -I -u fn_stationarity_fast.py`;
3: same with `sed 's/^N_ZEROS = 25$/N_ZEROS = 200/'` (the only edit; dps stays 50, primes stay ≤ 10⁴);
2/4/5/6: `fn_stationarity_numpy.py $Z N LIMIT` (same formula, same segmentation, plus `scipy.stats.linregress` p-values, which the archived script never computes);
7: `fn_equalwidth.py $Z 200 15e6`.

**Cross-checks.** The float64 port reproduces all eight segment means and
standard deviations of run 1 to the eight printed digits (e.g. segment 5:
0.03178004 / 0.05548826 in both) and the two N = 200 slopes of run 3 to five
significant figures. So the port is the archived computation at the larger
scale, not a different one. The 100k table carries nine decimals; γ·ln p ≤ 6,550
at p ≤ 15×10⁶, so table rounding moves each phase by at most ~1e-8.

**What the planned run shows.** At N = 200, p ≤ 15×10⁶, the monograph's own
procedure (equal-count segments) gives a standard-deviation slope of
−6.2834e-03 with p = 0.026: not "consistent with stationarity" at the 5% level
by an OLS slope test, which is the reading the monograph's sentence implies.
The same procedure also fails its own counterfactual: an off-line zero
(σ = 0.55) is supposed to make the variance *grow*, but its slope is negative
too (−1.0608e-02). The cause is a segmentation confound, not the zeros: at
p ≤ 15×10⁶ the eight equal-count segments have very unequal widths in x
(segment 1 spans x ∈ [0.6931, 14.2873], width 13.59; segments 4–8 have widths
0.309, 0.240, 0.195, 0.165, 0.143), and a window shorter than the slowest
period (2π/γ₁ = 0.4445) under-samples the dominant mode and reads a smaller
spread. With equal-width windows (run 7) the on-line
slope is +5.97e-04 per window (p = 0.555; max/min of the eleven window
standard deviations 1.313) and the off-line slope is +3.41e-03 (p = 0.003,
last/first 1.333): the discrimination the monograph describes appears, at
N = 200, only after the segmentation is changed. This is one run per method,
not a significance claim about RH; the p-values treat 8 or 11 window
statistics as independent, which overlapping-frequency data are not.

**Also observed in run 1.** The script's Wronskian table prints
`Signs alternate: False` (pairs (6,7) and (7,8) are both positive; (9,10) and
(10,11) both positive), while its RESULTS block prints the hard-coded line
"Wronskians: all non-zero, signs alternate ✓". The monograph does not claim
alternation (grep `alternat` in the .tex: two unrelated hits), so this is a
defect in the extras script's summary, not in the paper. Likewise the RESULTS
line "Off-line zero BREAKS stationarity: σ=0.55 drift: 1× steeper" prints a
ratio of 1.

**The other N = 200 instrument, for completeness.** `code/acs_codebase/extras/fn_n200.py`
(a different statistic: Var of $\sum_k A_k x^{\sigma-1/2}\cos(\gamma_k\log x)$ on
200 points of [X, 2X]) reruns in 55 s and gives the variance ratio
Var(σ = 0.6)/Var(σ = 0.5) = 2.6, 3.4, 4.3, 5.2, 6.8, 8.6 at
X = 10², 3·10², 10³, 3·10³, 10⁴, 3·10⁴. The monograph prints "values 2.6,
4.2, 6.8 at $X = 10^2, 10^3, 10^4$" (`Form_Function_and_Asymmetry.tex:2104-2105`);
the middle value reruns as 4.3, not 4.2.

## (C) The Compression Law past φ(m) = 24 (candidate 61)

**What the note says.** `papers/notes/Prime_Gap_Transition_Operator.tex:162-181`
(table and fits $r_{\rm eff}\approx0.59\,\varphi^{1.61}$,
$r_{\rm eff}/r_{\rm alg}\approx1.23\,\varphi^{-0.64}$ over
φ ∈ {2, 4, 8, 12, 16, 24}); `:185` "Whether the trend continues, saturates,
or reverses for $\varphi(m) > 24$ is an open computational question"; `:344`
"Testing $\varphi(m) > 100$ would constrain extrapolation". Data scale, abstract
`:45`: "$1.27 \times 10^6$ primes up to $2 \times 10^7$ for the full
operator-theoretic analysis".

**The instrument.** No script for $P_m$ is committed under `code/` (grep for
participation / r_eff / compression / totient / transition operator; the
`code/notes_verification/PRIME_GAP_TRANSITION_OPERATOR.md` page is a Markdown
copy of the note). The nearest committed instrument is the frontier's
`los_conditional_limit.py`, inside `docs/frontier/2026-09-11/ACS_Frontier_Evidence.zip`,
which builds the same operator from triple counts but only for m ≤ 30. The runs
here use a RECONSTRUCTED scratch instrument (`prime_gap_compression.py`, 87
lines) that follows the note's Setup literally: states (a, b) ∈ U_m², primes
p > m, $T_m[(b,c),(a,b)] = N(a,b,c)/\sum_c N(a,b,c)$, $T_0 = 1/\varphi(m)$,
$P_m = T_m - T_0$, $r_{\rm eff} = (\sum|\lambda|)^2/\sum|\lambda|^2$ over
eigenvalues with |λ| > 10⁻⁹, $r_{\rm alg}=\varphi^2-\varphi$. A column (a, b)
with no successor is outside the note's definition (the frontier script raises
on it); the instrument counts such columns and sets them to T = 0, and every
row with one is marked *undefined* below. Command:
`acs-venv/bin/python -I -u prime_gap_compression.py 2e7 DEADLINE m… --null`.

**Reproduction (primes ≤ 2×10⁷: 1,270,607 primes).** All six printed values
reproduce to the printed digits: m = 6, 12, 30, 42, 60, 90 give
r_eff = 1.53, 7.07, 15.33, 36.52, 42.98, 100.48 and ratios 0.7674, 0.5890,
0.2738, 0.2767, 0.1791, 0.1820. Numerical rank (tolerance 10⁻⁹) equals φ² − φ and the number of
zero eigenvalues equals φ at every one of the 14 Kernel-Law moduli (run
`r1_repro`, 15 s). The note's own table is not monotone, although `:185` says
"the ratio $r_{\text{eff}}/r_{\text{alg}}$ is monotonically decreasing": 0.274
(φ = 8) → 0.277 (φ = 12) and 0.179 (φ = 16) → 0.182 (φ = 24).

**Past φ = 24, the note's family (composite m, same sample).**

| m | φ | empty columns of (a, b) | r_eff / r_alg (T = 0 convention) | status |
|---:|---:|---:|---:|---|
| 120 | 32 | 22 of 1024 | 0.1791 | undefined by the note |
| 126 | 36 | 72 of 1296 | 0.1938 | undefined |
| 150 | 40 | 291 of 1600 | 0.1497 | undefined |
| 180 | 48 | 757 of 2304 | 0.1282 | undefined |
| 210 | 48 | 955 of 2304 | 0.0924 | undefined |

(run `r3_composite`, 129 s). A self-transition (a, a) needs a prime gap
≡ 0 (mod m), so a gap of at least m; below 2×10⁷ those are too rare to populate
every residue once m passes ~100. At the note's data scale the operator it
defines does not exist for the next composite moduli, and the numbers in the
fourth column are artefacts of whichever empty-column convention is chosen.

**Past φ = 24, prime moduli (the family that stays defined longest).** For
prime m a self-transition needs a gap of 2m.

| m | φ | r_eff | r_eff / r_alg at p ≤ 2×10⁷ | shuffle null r_eff / r_alg | r_eff / r_alg at p ≤ 2×10⁸ |
|---:|---:|---:|---:|---:|---:|
| 5 | 4 | 7.34 | 0.6120 | 0.7954 | |
| 7 | 6 | 15.47 | 0.5158 | 0.8594 | |
| 11 | 10 | 41.73 | 0.4637 | 0.8577 | |
| 13 | 12 | 55.57 | 0.4210 | 0.8802 | |
| 17 | 16 | 88.92 | 0.3705 | 0.8734 | |
| 19 | 18 | 107.86 | 0.3525 | 0.8711 | |
| 23 | 22 | 149.14 | 0.3228 | 0.8787 | 0.2975 |
| 29 | 28 | 226.33 | **0.2994** | 0.8840 | 0.2432 |
| 31 | 30 | 266.49 | 0.3063 | 0.8804 | |
| 37 | 36 | 396.74 | 0.3149 | 0.8838 | |
| 41 | 40 | 495.88 | 0.3179 | 0.8823 | 0.2049 |
| 43 | 42 | 551.52 | 0.3203 | 0.8817 | |
| 47 | 46 | 677.28 | (0.3272; 11 empty columns, undefined) | 0.8824 | |
| 53 | 52 | 831.11 | (0.3134; 83 empty columns, undefined) | 0.8859 | |

(runs `r2_primefam`, 166 s, every listed modulus completed;
`r5_x2e8`: primes ≤ 2×10⁸, 11,078,937 primes, 22 s.) The shuffle null keeps
the residue sequence's multiset and randomises its order (seed 20261023).

**Answer to the note's question, at the scale reached.** At the note's fixed
sample (p ≤ 2×10⁷), within the one family that stays defined, the ratio falls
from 0.612 (φ = 4) to a minimum of 0.299 at φ = 28 and then *rises* slowly
to 0.320 at φ = 42: a reversal. It is not a property of the moduli. With ten
times the primes (p ≤ 2×10⁸) the same three moduli give 0.2975, 0.2432,
0.2049 at φ = 22, 28, 40, monotone decreasing, and the φ = 40 ratio drops by
0.113. So r_eff depends on the sample size as strongly as on φ, the reversal
at 2×10⁷ is a finite-sample effect, and the exponents β ≈ 1.61, δ ≈ 0.64 are
properties of the pair (φ, x), not of φ alone. That is consistent with the
frontier's conditional fixed-modulus limit $r_{\rm eff}\to\varphi-1$ (ratio
→ 1/φ, i.e. 0.025 at φ = 40) under the Lemke Oliver–Soundararajan conjecture
(`docs/frontier/2026-09-11/workstreams/arithmetic/report.md:12`), and does not
test it. The pure-noise null sits at 0.84–0.89 for every φ ≥ 8 (range 0.8368–0.8859 over runs r1 and r2), so the prime
operator is far from noise at every defined row.

**A second, structured null (discounted).** Permuting the prime *gaps*
(keeping their multiset) and rebuilding a pseudo-prime sequence (`prime_gap_gapnull.py`,
run `r4_gapnull`) gives r_eff/r_alg 0.5103, 0.2715, 0.2174, 0.2120, 0.2408,
0.3434 at m = 6, 12, 30, 42, 60, 90 and 0.3029, 0.3966 at m = 29, 41 (primes:
0.2994, 0.3179). At m = 29 the gap-shuffled sequence compresses as much as the
primes do. The confound: pseudo-primes not coprime to m are dropped (kept
fraction 0.534 at m = 30, 60, 90; 0.965 and 0.975 at m = 29, 41), which shrinks
the sample, and the reversal above shows r_eff rises when the sample shrinks.
Only the m = 29 and m = 41 rows are near-equal in sample size, and they
disagree in direction. So this null shows that much of the low-φ compression
can come from the marginal gap law, without settling how much.

**Not done.** φ(m) > 47 at a defined operator (needs p well beyond 2×10⁸ for
composite m); φ > 100 (a 10⁴ × 10⁴ dense eigenproblem per modulus); the
heavy-tail goodness-of-fit (lognormal / stretched exponential vs power law,
`:210`): quantiles are printed by the instrument but no fit or test was run;
repeat seeds for either null.

## Files

Committed: this page, the cards in `open_problems_2026-10-22.md`, the
paste-ready proposals in `proposed_amendments_2026-10-22_pass2.md`, one
`docs/README.md` bullet. Not committed (scratch; the three new scripts are 41–87 lines, formulas
quoted above): `fn_stationarity_numpy.py`, `fn_equalwidth.py`,
`fn_stationarity_fast_N200_p1e4.py` (the archived script with one line changed), `prime_gap_compression.py`,
`prime_gap_gapnull.py`, and the run logs `fn25_orig.out`, `f1`–`f7`, `r1`–`r5`.
