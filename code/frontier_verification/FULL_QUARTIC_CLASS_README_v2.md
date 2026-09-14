# Full quartic classification and the information in a count

Degree four, signature (0,2) and absolute field discriminant 576 determine exactly two isomorphism classes: A=Q(sqrt(2),sqrt(-3)) and B=Q(sqrt(-2),sqrt(-3)). The V4 group is now derived from these inputs. This closes the non-V4 gap left by the earlier conditional classification, while preserving that checkpoint as written.

The [new evidence package](../../docs/frontier/2026-09-14-aggregate-classification-delta/README.md) then identifies the field from a certified aggregate positive-zero count. The exact complete count through height 20 is 23 for A and 22 for B. Alternatively, the count below 7/3 remains distinguishing when each ordinate has error at most 1/3. Selection determines the field and its Euler coefficient formula; all 604 tracked coefficients are checked independently. This exposes an information limit of the present benchmark: precise ordinate locations are unnecessary for a decoder allowed to use the full consequences of the metadata and the derived field class.

## Why the group is derived

Let K be any field satisfying the metadata, N its normal closure and G=Gal(N/Q) acting faithfully on the four embeddings of K. This action is transitive. The signed discriminant is (-1)^2*576=24^2. An integral-basis embedding matrix has determinant Delta with Delta^2=576, so Delta=+24 or -24 is rational and nonzero. G fixes Delta while permuting its rows; every permutation is even. Thus G is contained in A4. Transitivity forces its order to be divisible by four, and the only possibilities are V4 and A4. Embedding discriminants, signs and ramification criteria are recorded in Milne's [Algebraic Number Theory, Propositions 2.26/2.40 and Theorem 3.35](https://www.jmilne.org/math/CourseNotes/ANT.pdf).

Suppose G=A4. Its normal V4 subgroup defines a cyclic cubic field F=N^V4. The normal closure can ramify only at 2 and 3: at any other prime, completions of each conjugate of K are unramified, and finite composita of unramified local extensions stay unramified. Equivalently, inertia has singleton orbits on all four embeddings at an unramified prime of K; the faithful action then forces that inertia to be trivial.

At 2, a ramified completion of the cyclic cubic F would have decomposition and inertia group C3, ramification degree e=3 and residue degree f=1. Its wild 2-group is trivial. Tame inertia would inject into the multiplicative group of its residue field F2, which has order one. This is impossible. Hence F is unramified at 2. The unramified closure and inertia filtration used here are given by Milne, [Corollaries 7.51–7.52, Lemma 7.57 and Corollary 7.59](https://www.jmilne.org/math/CourseNotes/ANT.pdf).

At 3, assume F ramifies. Inertia I in N has nontrivial image in A4/V4, so I is one of the four C3 subgroups or all of A4. Wild inertia must be a normal 3-subgroup with prime-to-3 quotient. A4 has no normal subgroup of order three, excluding I=A4. Therefore I=C3. Its normalizer in A4 is itself. Since inertia is normal in the local decomposition group D, we obtain D=I=C3.

The action of D on the four embeddings has orbits of sizes one and three. As D=I, the local algebra K tensor Q3 is Q3 times a totally ramified cubic field. For a wildly ramified local factor, the different exponent is at least its ramification degree. Consequently this cubic factor contributes at least three to v3(disc(K)); the remaining linear factor contributes zero. This contradicts v3(576)=2. The different bound and its contribution to the field discriminant are stated and proved in Conrad's [The Different Ideal, Theorem 4.13 and Corollary 4.16](https://kconrad.math.uconn.edu/blurbs/gradnumthy/different.pdf). Because the discriminant is a square, the lower bound could also be sharpened to the next even exponent, four; three already suffices for the contradiction.

F would now be unramified at every finite prime. A cyclic cubic field is totally real: complex conjugation cannot act nontrivially through an odd-order group. If its discriminant were one, the Minkowski ideal bound would be 3!/3^3=2/9, below the smallest positive integer ideal norm. This is impossible, also covered by Milne's [Theorem 4.9](https://www.jmilne.org/math/CourseNotes/ANT.pdf). Thus G cannot be A4. It is V4; its order equals [K:Q], so K=N and K is biquadratic.

The computation does not substitute finite tests for those number-theoretic steps. It checks their finite group content by two methods: generator closure and all 2,048 subsets of A4 containing the identity, using opposite composition conventions and different parity calculations. Both give ten subgroups and precisely the two transitive possibilities. All five inertia candidates with nontrivial cubic quotient image are checked, including their normal wild subgroups, normalizers and embedding orbits. The general arithmetic argument above is written mathematics, not a Lean kernel proof.

## Finish the field enumeration

A quadratic subfield can ramify only where K ramifies. Its squarefree radicand is therefore one of -6,-3,-2,-1,2,3,6. A biquadratic field is determined by its three nontrivial quadratic subfields; these form a two-dimensional plane in the square classes generated by -1,2,3. There are seven such planes. The fundamental quadratic discriminant is d when d=1 modulo four and 4d otherwise. The field discriminant is the product of the three quadratic discriminants, by the abelian conductor-discriminant formula and the quadratic conductor identity: Milne, [Class Field Theory, V.3.27–3.29](https://www.jmilne.org/math/CourseNotes/CFT.pdf).

Exactly two planes have the required discriminant and signature. Their quadratic discriminants are (-24,-3,8) and (-8,-3,24), giving A and B. An independent enumeration tests all 256 sign-valued functions on the units modulo 24, finds eight characters and seven character planes, and obtains the same two fields. The old V4-conditional list is used only as a downstream comparison. The classifier itself reads only the four metadata fields.

## Actual fields test the hypotheses

Two genuine A4 fields prevent an overbroad conclusion:

- x^4-2*x^3+2*x^2+2 has field discriminant 3136=2^6*7^2. It is Eisenstein at two, positive on the real line, and has a distinct 1+3 factorization modulo three. Modulo seven it is (x+2)(x+1)^3: the cubic ramification is tame and the discriminant exponent is two. Allowing an extra ramified prime seven invalidates the obstruction.
- x^4+8*x+12 has field discriminant 5184=2^6*3^4 and power-basis index eight. Its integral basis is 1,x,x^2/2,x/2+x^3/4. It has a distinct 1+3 factorization modulo five and, at the non-index prime three, factors as x*(x-1)^3. It retains prime support {2,3} but has wild cubic ramification and exponent four at three. Dropping the small-exponent hypothesis invalidates the obstruction.

Both discriminants are positive squares and both fields have signature (0,2). Positivity follows from the identities

    x^4-2*x^3+2*x^2+2 = (x^2-x)^2 + x^2 + 2,
    x^4+8*x+12 = (x^2-2)^2 + 4*(x+1)^2 + 4.

For the second polynomial, rational roots and all possible monic quadratic factorizations are excluded. Such factors would require bd=12, a(d-b)=8 and b+d=a^2; the middle equation bounds |a| by eight. Square discriminant, transitivity and a three-cycle give A4; a separate CAS Galois-group calculation agrees.

The proposed orders have integral multiplication matrices and the stated trace discriminants. Maximality is checked by excluding integral elements v/p outside each order for every prime p whose square divides its discriminant. Multiplying a nonzero residue vector by a unit and subtracting an order element reduces it to a representative whose first nonzero coordinate is one. All 470 representatives are checked, covering 2,510 nonzero residue vectors. A nonintegral coefficient in each multiplication characteristic polynomial excludes integrality; Newton trace identities reproduce every polynomial independently. SymPy's round_two algorithm separately returns the same maximal-order lattice. Polynomial index primes are handled explicitly.

## What the count contributes

The decoder rebuilds each derived class's aggregate template from its three quadratic factors and zeta. It generates coefficients from

    c_(p^k) = 1 + sum_D Kronecker(D,p)^k,

including ramified primes, where a ramified quadratic character contributes zero. This is the Euler-factor identity for the biquadratic field. Precise source intervals establish candidate template counts and the observation error contract; the selector receives only a height and a nonnegative integer count, with no field label or individual ordinates.

At zero noise, the first distinguishing integer height is two. The complete count through 20 also distinguishes A's 23 roots from B's 22. At height 7/3 and error radius 1/3, every permitted independent ordinate displacement leaves count one for A and zero for B. This reuses the previously certified gate with a newly derived complete field class, removing its earlier supplied-Galois-group premise.

Twenty cases cover two candidate-spectrum precisions, two observations and five height/radius settings. Sixteen select one field and all 604 coefficients. Four cases at radius 1/2 retain both fields. Independent attainable-count sets replay every decision. Uniform displacements of +1/2 and -1/2 show that each field can produce either count zero or one at that radius; eight interval checks cover both precisions. These witnesses concern this count statistic, not the full spectrum.

Metadata alone fixes 456 of 604 coefficients and 12 of the 17 targets. The distinguishing count resolves the remaining 148 coefficients, including target indices 3,7,19,27,31. Independent polynomial factorization at 564 primes for each field, with alternate generators where needed, reproduces all 1,208 coefficient values. No new roots or Gaussian measurements are computed.

Completeness remains essential. A bare count cannot establish its own completeness or error bound. For a count below h with ordinate error r and certified root completeness through T, the decoder checks T-r>=h so omitted higher roots cannot enter the gate. In particular, completeness through 20 alone does not justify a noisy count at height 20. The exact count at that height and the robust interior gate are distinct contracts.

## Verification and continuation

Thirteen semantic mutations challenge group coverage, normality, wild exponents, the Minkowski bound, class completeness, supplied labels, malformed counts, missing completeness margin and forged predictions. All are rejected; the two actual A4 controls remain allowed when the exact metadata hypotheses are relaxed. Seven recorded scientific/source commands pass. Executed sources and older checkpoints remain unchanged.

Run the inherited pinned Python environment with:

    python code/frontier_verification/verify_aggregate_classification_delta_v2.py

The first verifier completed the prior recursive replay but stopped when comparing integer-key subgroup counts against their saved JSON string-key form. A recorded diagnostic shows that the full audit is identical after JSON normalization. The separate v2 verifier normalizes representations, rejects key collisions and changed values, and retains the failed version and receipts. The seven scientific/source commands remain successful and unchanged.

The verifier recursively checks the preceding checkpoint and freshly regenerates the classification, independent enumeration, actual-field controls, count decoding, polynomial audit and semantic tests. It verifies hashes, acquisition receipts and the append-only research ledger. The new arithmetic proof remains unformalized in Lean.

Earlier Gaussian coefficient-recovery results retain their declared validity and restricted deduction methods. They are not optimal limits for this richer decoder. A sharper benchmark should match degree, signature, discriminant and finite zero counts, or explicitly limit the available prior and decoding method. Constructing such benchmarks, extending arithmetic formalization and investigating the broader operator, infinite arithmetic, topology and private-input questions remain active research gates.
