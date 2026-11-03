# Reproducing the Q(zeta_5) continuation

The [Dedekind checkpoint](../../docs/frontier/2026-09-13-dedekind-delta/README.md) retains two-precision certificates for the missing quadratic and Riemann factors, exact Euler checks, declared finite witness comparisons and archived source changes. Use the pinned [source requirements](source_requirements.txt). The calculations use python-flint 0.9.0 / FLINT 3.6.0 and mpmath 1.3.0.

From this directory:

```sh
python dedekind_factor_certificate.py --precision 160 --output /path/to/factors-160.json
python dedekind_factor_certificate.py --precision 224 --output /path/to/factors-224.json
python dedekind_independent_roots.py --extra ../../docs/frontier/2026-09-13-dedekind-delta/Factor_Certificates.zip --primary ../../docs/frontier/2026-09-12-source-delta/Primary_Tables.zip --output /path/to/independent-roots.json
python dedekind_euler_audit.py --extra ../../docs/frontier/2026-09-13-dedekind-delta/Factor_Certificates.zip --prior ../../docs/frontier/2026-09-13-lfunction-delta/Certificates.zip --output /path/to/euler-audit.json
python dedekind_witness_audit.py --extra ../../docs/frontier/2026-09-13-dedekind-delta/Factor_Certificates.zip --prior ../../docs/frontier/2026-09-13-lfunction-delta/Certificates.zip --output /path/to/witness-audit.json
python verify_dedekind_delta.py
```

The factor inputs accept either the ZIP above or an extracted `factors-224.json`. Export the four decimal tables and their interval manifest with `dedekind_export.py`, passing the same `--extra` and `--prior` arguments and an explicit `--output-root`. The export refuses to replace a different existing table. It adds the even quadratic and 90-root Riemann files and verifies the two existing complex-character tables.

The portable application entry point is:

```sh
python ../hp_knife_suite/data_zeros/cyclotomic_5/cyclotomic_test.py --output /path/to/witness-audit.json
```

Its default paths refer to the retained checkpoints, and its result matches the direct audit command byte for byte. It produces declared finite comparisons, not the historical NPZ output whose original quadratic input is missing.

## Counting the even character

The quadratic character is the primitive even character modulo 5 with values `[0,1,-1,-1,1]` and Conrey index 4. The prior contour/refinement primitives remain unchanged. There are 146 positive Hardy Z sign-change brackets below 220, but the rectangle from real part -1/4 to 5/4 and height -1/2 to 220 contains 147 zeros. The extra zero is at s=0. The Hurwitz identity gives its exact value as the rational sum of `chi(a)*(1/2-a/5)`, which is zero.

Each disjoint positive bracket gives a zero, and the exact origin value gives one more. Matching that lower count to the whole-contour winding count proves that all 147 are simple and there are no extras in the finite rectangle. Ignoring the trivial zero would incorrectly reject this even-character extension. The two working precisions use separately constructed contour partitions and agree. Their interval kernel is shared. These are executable interval arguments with documented analytic premises, not Lean formalizations.

For the Riemann factor, all 90 zeros below 220 are computed as complex balls and checked against the total zero count and the next zero above 220. All 90 intervals also contain the corresponding primary high-precision literal from Odlyzko's retained table. Six selected new-factor roots are checked at 85 digits in each certificate run, and a separate script recomputes every quadratic root through an independent Hurwitz implementation. This independently checks locations numerically; it does not provide a second rigorous completeness proof.

## What the Euler factors imply

For an unramified rational prime, let f be its order modulo 5 and g=4/f. Cyclotomic factorization gives g prime ideals of norm p^f. Thus the local factor is `(1-X^f)^(-g)`, where `X=p^(-s)`. The four character factors multiply to this denominator; a separate permutation determinant gives the same polynomial. Modular factorizations of the fifth cyclotomic polynomial are checked for all 168 primes below 1000. At p=5 there is one prime of norm 5, with ramification index four, and only the primitive zeta factor supplies the local factor `(1-X)^(-1)`.

Logarithmic differentiation gives coefficients `g*f*log(p)` at powers p^k with f dividing k, and zero otherwise. The factor f comes from `log(norm(P))`; counting prime ideals alone omits it. The rational-function identity proves the whole coefficient pattern, with sixteen initial coefficients also compared through character sums and permutation traces. These Euler identities do not assert equality with a finite Fourier ordinate.

For a fixed finite cutoff, the product's zero measure adds every factor root with the same multiplicity. Dividing factor j by a different count N_j changes those relative weights. As an exact counterexample, at T=220 the counts are `(90,146,146,146)`. The weighted logarithmic-derivative combination with weights `1/N_j` has first-prime coefficient `14/3285` (before the common scale) at every nonsplit unramified residue, where the genuine character sum cancels. This concerns the corresponding weighted infinite logarithmic derivative; it is not an exact prediction for the truncated Fourier values.

## Finite comparison definitions

The audit fixes six heights, three shared windows (rectangular, triangular and Hann), 34 primes below exp(5), and powers 1, 2 and 4. It computes 1,836 exact-log frequency points and 612 nearest-grid points, with three explicitly defined normalization/conjugation variants. All 7,344 variant values have interval enclosures carrying the 5e-21 decimal ordinate uncertainty. A separate float64 calculation is checked with an explicit tolerance, and 54 common-weight values are independently checked at 85 digits.

The historical doubled-means control uses certified current inputs; it is not a reconstruction of the missing historical input files. The separate-means variant replaces only the conjugate list. The union mean then gives every root the same weight. Every factor uses the same window, and count normalizers remain unweighted counts. A common scalar cannot change the reported ratios. Both the first-25-prime cohort and the entire declared frequency-range cohort are retained. Powers outside the old frequency range are marked explicitly.

Ratios of group mean absolute amplitudes depend on height, window, sampling and cohort. They do not supply a p-value, prove a density theorem, or identify a spectral operator. The next step is a specified test-function explicit formula including pole, gamma, prime and zero terms with controlled truncation, alongside a separately justified statistical comparison.
