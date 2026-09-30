# Q(zeta_5): all-factor and normalization delta

This continuation supplies the two missing factors needed for a declared finite Q(zeta_5) comparison and separates three effects: distinct positive conjugate spectra, relative factor weights, and finite cutoff/window choices. The all-factor calculation is now reproducible. The historical 5–6 ratio remains withdrawn: its original quadratic input is unavailable, and the new ratios vary substantially with the stated experiment. This is an ongoing research delta, with no global exhaustion claim.

## Certified finite inputs

The [factor certificates](Factor_Certificates.zip) add 146 positive roots of the primitive even quadratic character modulo 5 and 90 Riemann roots below height 220. Together with the [previously certified](../2026-09-13-lfunction-delta/README.md) complex character and its conjugate, the four factor counts are `(90,146,146,146)`: 528 pairwise separated positive roots. The [exported interval manifest](../../../code/hp_knife_suite/data_zeros/DEDEKIND_FACTORS.json) binds all four decimal tables to their certificates and a 5e-21 ordinate error bound.

The even character requires an extra count: the contour rectangle Re(s) in [-1/4,5/4], Im(s) in [-1/2,220] contains 147 zeros, including the trivial zero at s=0. The exact Hurwitz value is `sum chi(a)*(1/2-a/5)=0`. Disjoint Hardy Z sign brackets supply 146 positive zeros, and matching these plus the origin to the winding count proves simplicity and absence of extras in this finite rectangle. Separate 160-bit and 224-bit runs construct their own contour partitions and agree. The analytic continuation and trivial-zero premise are stated in [NIST DLMF 25.15](https://dlmf.nist.gov/25.15).

For the Riemann factor, interval root generation, separation, the next root above 220, and a total zero count agree. The installed API's meanings are documented for [indexed zeros](https://python-flint.readthedocs.io/en/latest/acb.html#flint.acb.zeta_zeros) and [total counts](https://python-flint.readthedocs.io/en/latest/arb.html#flint.arb.zeta_nzeros). Both new factors are computed at both precisions. Six selected roots receive an 85-digit mpmath check in each run; these are the same six locations across runs.

The [independent root audit](Independent_Root_Audit.json) additionally recomputes every one of the 146 quadratic roots through mpmath's Hurwitz implementation at 85 digits. Every result lies inside its certified interval with residual below 1e-74. All 90 Riemann intervals contain the corresponding high-precision literal from the [retained primary Odlyzko table](../2026-09-12-source-delta/Primary_Tables.zip), originally published on [Odlyzko's table page](https://www-users.cse.umn.edu/~odlyzko/zeta_tables/). Numerical agreement and literal inclusion are additional checks, not second rigorous completeness proofs. The interval routes share FLINT/Arb; these are executable interval arguments, not Lean formalizations or global zero theorems.

## Euler factors and the missing residue-degree multiplier

For p != 5, write f = ord_5(p) and g = 4/f. There are g prime ideals of norm p^f; the local factor is `(1-X^f)^(-g)` for X = p^(-s). At p = 5 there is one prime of norm 5, ramification index four, and local factor `(1-X)^(-1)`. These premises follow from the cyclotomic prime decomposition in [Stevenhagen, Theorem 3.12, printed page 33](https://kconrad.math.uconn.edu/math5230f08/stevenhagen.pdf) and the prime-ideal Euler product in [Milne, Chapter VI, Example 1.1(b)](https://www.jmilne.org/math/CourseNotes/CFT.pdf).

The [exact Euler audit](Euler_Audit.json) independently matches the product of four character factors to a permutation determinant, checks sixteen coefficients through character powers and matrix traces, and factors the fifth cyclotomic polynomial modulo all 168 primes below 1000. Logarithmic differentiation gives

`-X*P'(X)/P(X) = g*f*X^f/(1-X^f)`.

Thus the coefficient at p^k is `g*f*log(p) = 4*log(p)` when f divides k, and zero otherwise. The factor f comes from the logarithm of the prime-ideal norm. At the ramified prime, the coefficient is log(5), not 4 log(5). This is an exact Euler identity; it does not equate a finite Fourier value to a prime coefficient. Local decomposition also does not by itself prove a prime-density theorem.

## Relative normalization changes the measure

Let S_j be the windowed cosine sum over factor j's positive zeros below the same T, and N_j its unweighted count. The audit compares:

- Historical doubled-means control: `(S_0/N_0 + 2*S_1/N_1 + S_2/N_2)/4`.
- Separate factor means: `(S_0/N_0 + S_1/N_1 + S_2/N_2 + S_3/N_3)/4`.
- Union mean: `(S_0 + S_1 + S_2 + S_3)/(N_0 + N_1 + N_2 + N_3)`.

The first comparison changes the positive conjugate list; the second gives every root the same weight, as required by the product's zero multiplicities. A common scalar does not affect the ratios. Normalizing each factor by a different N_j changes relative weights. The corresponding weighted infinite logarithmic derivative with weights 1/N_j fails the nonsplit first-coefficient cancellations at every tested cutoff. At T=220 its coefficient divided by log(p) is 14/3285, before the common scale, at each nonsplit unramified residue; the genuine character sum is zero. This exact counterexample diagnoses weighting, without claiming to predict a finite Fourier amplitude.

## Finite comparisons and their limits

The [finite audit](Finite_Witness_Audit.json) retains all six heights 60, 80, 100, 140, 180 and 220; rectangular, triangular and Hann windows; 34 primes through 139; and powers 1, 2 and 4. It encloses 1,836 exact-log frequency points and 612 nearest points on the historical 2,000-point grid over [0.5,5], for all three variants: 7,344 interval values. Frequencies beyond the old grid are flagged. Float64 recomputation uses a stated 2e-12 tolerance, and 54 union means are independently checked at 85 digits. All windows are shared across factors and counts remain unweighted.

The ratio is the mean absolute amplitude for p congruent to 1 modulo 5 divided by that for the other unramified residues; p=5 is excluded. Both the first 25 primes and all 34 declared primes are retained. For the first-25 cohort, exact log(p) frequencies and rectangular window:

- At T=100, doubled means / separate means / union mean give 6.88920318 / 8.05729680 / 9.43570104. Sampling the union mean at the nearest old-grid points instead gives 9.16531271.
- At T=220 the three exact-frequency ratios are 10.06440878 / 10.74854229 / 20.13027979. The union ratio changes to 14.79604084 for the triangular window and 13.16325914 for Hann.

These are scoped comparisons, not a universal ratio, p-value, density proof, or spectral-operator identification. The doubled-means control uses the same newly certified inputs as the other variants. It is not a literal replay of the missing historical quadratic file and NPZ; the [historical input gates](Historical_Input_Gates.json) retain those exact missing paths and the original consumer is archived unchanged.

## Reproduction and continuation

The [portable consumer](../../../code/hp_knife_suite/data_zeros/cyclotomic_5/cyclotomic_test.py) now uses repository-relative certified inputs and an explicit output path. It reproduces the finite audit byte for byte. The historical figure script remains identified as an external-NPZ workflow. Synthesis documents carry dated corrections while preserving historical statements as such.

[Reproduction instructions](../../../code/frontier_verification/DEDEKIND_README.md), [runtime](Runtime.json), [source changes](Source_Changes.json), [source archive](Source_Snapshot.zip), [nine execution receipts](Execution_Receipts.json), and [execution archive](Execution_Artifacts.zip) identify what ran. The archive also keeps the initial loader and initial results before ZIP input support was added. The [manifest](Manifest.json) and [verification result](Verification.json) check identities and retained-computation consistency, recursively preserving prior checkpoints; the package verifier does not reevaluate the L-functions.

The [research queue](Research_Queue.json) advances P05, R12, R13, K05 and K04. It retains all 115 branches and extends the unchanged 341-event [history](Branch_Events.jsonl) to 346 events. The next mathematical gate is a specified test-function explicit formula with pole, gamma, prime and zero terms and controlled truncation. Statistical calibration needs a separate declared comparison design. Higher cutoffs, natural-operator and independent real-part bridges, geometric topology, physical identifications and the private benchmark inputs remain open.
