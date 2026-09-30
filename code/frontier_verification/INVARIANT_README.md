# Degree and discriminant already determine this field

**Theorem.** A number field of degree four and absolute field discriminant 125 is isomorphic to Q(zeta_5). The conclusion needs no zero measurements, assumed Galois property, or supplied defining polynomial. This is a classical arithmetic derivation with exact finite checks; the complete number-field proof has not been formalized in Lean.

## Arithmetic premises

The degree sum is sum(e_i f_i)=n. A prime ramifies exactly when it divides the field discriminant. In tame ramification its discriminant exponent is sum((e_i−1)f_i). These facts concern the maximal ring of integers, not an arbitrary polynomial order. See [Milne, ANT, Theorems 3.34–3.35](https://www.jmilne.org/math/CourseNotes/ANT.pdf) and [Keith Conrad, The Different Ideal, Theorems 4.8 and 4.13](https://kconrad.math.uconn.edu/blurbs/gradnumthy/different.pdf).

Tame inertia is cyclic. In a permutation representation on n embeddings, a generator has discriminant exponent n minus its number of orbits; this also applies to subfields of a normal closure. See [Jiuya Wang, 2018 dissertation, section 3.1.1, printed page 31](https://asset.library.wisc.edu/1711.dl/6NIAB7DW5X5WN8J/R/file-284b7.pdf). Unramified local extensions remain unramified in composita, so a normal closure introduces no new ramified primes. Inertia maps onto the inertia of a Galois subextension. See [Brian Conrad, Tameness and composite fields](https://math.stanford.edu/~conrad/676Page/handouts/tamecomp.pdf) and [Surjectivity for inertia groups](https://math.stanford.edu/~conrad/676Page/handouts/inertiasurj.pdf).

Minkowski supplies a nonzero integral ideal with norm at most B=(n!/n^n)(4/pi)^r2 sqrt(|D|). Such a norm is at least one. In particular, Q has no nontrivial extension unramified at every finite prime. See [Milne, ANT, Theorems 4.3 and 4.9, printed pages 70 and 72](https://www.jmilne.org/math/CourseNotes/ANT.pdf). The usual Galois correspondence, Lagrange theorem, Eisenstein criterion and polynomial-order index/discriminant identity are also used.

## Derivation

1. Only 5 ramifies in K. Every ramification index is at most four, hence coprime to 5. The tame formula gives 3=4−sum(f_i). Therefore there is exactly one prime above 5, with f=1 and e=4.

2. Let N be the normal closure. Its group embeds transitively in S4, so its order divides 24 and its ramification at 5 is tame. The inertia generator has 4−3=1 orbit on the four embeddings. It is a four-cycle. After conjugating its labels, the only subgroups of S4 containing this cycle are C4, D4 of order eight, and S4. The producer constructs overgroups by adjoining generators. The auditor separately exhausts all 130817 subsets of the possible orders containing C4, and checks multiplication closure.

3. In D4 the cyclic inertia subgroup is normal of index two. Its fixed field would be a quadratic extension of Q unramified at every finite prime. This is impossible by Minkowski. Explicitly, even allowing an imaginary quadratic signature, B<2/3<1 for |D|=1.

4. In S4, act on the three partitions of four letters into two pairs. The image is S3 and the kernel is the four-element subgroup of double transpositions. A four-cycle acts as a transposition. The fixed field of a partition stabilizer is a cubic field E. It is unramified away from 5 and has tame exponent 3−2=1 at 5, hence |D_E|=5. For either cubic signature, pi>3 gives B<=8 sqrt(5)/27<1, since 320<729. This is impossible. The independent auditor obtains the same inertia cycle lengths (1,2) from an explicit coset action. Inertia itself is not normal in S4; no such normality assumption is used.

5. Consequently N=K and Gal(K/Q)=C4. To identify this cyclic quartic, let L=Q(zeta_5). Its polynomial x^4+x^3+x^2+x+1 becomes Eisenstein after x is replaced by x+1. Its four roots lie in L and its automorphism group is C4. The polynomial discriminant is 125, checked independently by a symbolic discriminant and a trace Gram determinant. The possible order indices are 1 and 5. Index 5 would give a quartic field discriminant of absolute value 5, but B<=sqrt(5)/6<1. Thus the index is one and |D_L|=125; the argument in step 1 applies to L too.

6. Form M=KL. The restriction map embeds Gal(M/Q) into C4 x C4, with surjective projections. This group is abelian of exponent four. At 5 its cyclic inertia maps onto the order-four inertia of K and L; it therefore has order exactly four. All primes above 5 have the same inertia because the group is abelian. Its fixed field is unramified at all finite primes, hence equals Q. Thus [M:Q]=4, and K=L inside M. The two finite methods enumerate all four subdirect groups, of orders 4,4,8,16. In the last two cases the forbidden unramified quotient would have degree two or four. No linear-disjointness assumption is made.

This proves uniqueness for every signature compatible with |D|=125. As external corroboration for the originally supplied totally complex signature, [Prasad and Yeung, 2007 preprint, printed page 11, Case (a)](https://archive.mpim-bonn.mpg.de/id/eprint/741/1/preprint_2007_70.pdf) explicitly report the same unique quartic, based on number-field tables. That report is not a premise of the derivation above, and the underlying tables have not been independently enumerated here.

## Euler predictions and what changes

The maximal order is Z[zeta_5]. For p other than 5, Frobenius acts on the nontrivial fifth roots by exponent multiplication by p. Therefore f=ord_5(p), e=1 and g=4/f. At p=5, (e,f,g)=(4,1,1). For every k>=1 the logarithmic Euler coefficient is c_(p^k)=g f if f divides k, and zero otherwise. In particular ramification does not multiply c_5 by e.

The inference producer reads only degree, absolute discriminant and output limits. Its successful source/command receipt predates the independent audit. It emits all 604 coefficients through 4096 and all 72 prime local factors through 361 before loading any retained answers. The auditor then verifies 564 finite-field factorizations, multiplying each factorization back and checking irreducibility. All 604 coefficients match the earlier held-out arithmetic vector, including all 91 targets. The old 48 ambiguous factors are selected individually, including their square coefficients beyond the original target window.

The prior local-profile and spectral programs deliberately restrict inference to explicit-formula bounds and specified local relations. Their remaining alternatives are valid survivors of those relaxations. They are not distinct actual fields with the supplied global invariants. The four prior assumption profiles therefore describe different permitted deductions; they are not four logically independent classes of actual quartic fields once the full discriminant is known. Using it only to label ramified primes leaves global information unused.

Accordingly, the measured ordinate-radius thresholds remain meaningful sufficient bounds for the specified spectral decoder. They are not information-theoretic thresholds for identifying this field from all supplied inputs. Under unrestricted arithmetic deduction, zero spectral observations suffice. This does not claim a noise-independent spectral decoder, verify arbitrary fabricated spectra, or improve any earlier numerical bound.

## Controls and continuation

Q(zeta_8), with polynomial x^4+1, has the same degree and signature (0,2), but field discriminant 256. Its c_9 is four, whereas Q(zeta_5) has c_9=0. The polynomial discriminants, signatures and factorizations are checked independently; the cyclotomic field discriminant formula is [Conrad, Different Ideal, Example 4.10](https://kconrad.math.uconn.edu/blurbs/gradnumthy/different.pdf). Thus degree and signature alone do not justify the new conclusion. A real cubic of discriminant 49 checks that the small-discriminant argument does not incorrectly exclude ordinary cubic fields. Six corrupted transcripts are actually passed through the auditor and rejected, covering group completeness, the resolvent kernel, the compositum quotient, a fabricated bound, ramification weighting and an incorrect formerly ambiguous factor.

The next field-identification experiment must establish that its permitted global inputs leave multiple actual fields possible. Branch R15 now asks for independently certified nonisomorphic examples sharing the declared degree, signature and discriminant, with a differing Euler observable, before assessing information contributed by finite zero data. The existing Q(zeta_5) case remains useful for verified numerical recovery and error analysis. Local-model feasibility, wider-radius method improvement and the rest of the ACS queue remain separate open work.

## Replay

With the pinned Python/SymPy environment, run from the repository root:

```sh
python code/frontier_verification/dedekind_invariant_classification.py --output /tmp/Invariant_Predictions.json
python code/frontier_verification/dedekind_invariant_audit.py --predictions /tmp/Invariant_Predictions.json --root . --output /tmp/Invariant_Audit.json
python code/frontier_verification/dedekind_invariant_adversary.py --predictions /tmp/Invariant_Predictions.json --root . --output /tmp/Invariant_Adversary.json
python code/frontier_verification/verify_invariant_delta.py
```

The [dated checkpoint](../../docs/frontier/2026-09-13-invariant-delta/README.md) retains source hashes, the derivation's premise boundary, receipts, failures, exact predictions, audits and append-only history.
