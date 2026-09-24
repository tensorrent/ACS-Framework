# Klein-cover audit correction — 12 September 2026

This pass corrects a topological interpretation in the archived audit while retaining its valid matrix obstruction. It adds branch C07, 21 Lean theorem declarations, an independent exact affine calculation, and six rejected false mutations. The mean-error work remains in the queue; the newly identified overstatement took priority in this pass.

## The correction

The archived [AxiomIII.lean](../../../code/frontier_verification/proofs/AxiomIII.lean) correctly proves that a matrix commuting with `D = diag(1,-1)`, having determinant ±1 and trace two, must be the identity matrix. Its surrounding comments go further: they identify this with the trivial Klein-bottle mapping class. That implication is false. The archived manuscript audit repeats the same interpretation in its “weaker reading” remark.

The four possible matrices for arbitrary lifts also must not be identified with a faithful four-element representation of the Klein mapping class group. A lift must be specified. For the canonical orientation-preserving lift, the image is `{I,-I}` and the action has a nontrivial kernel. Exact affected statements and source identities are recorded in [Scope_Corrections.json](Scope_Corrections.json). Original sources and earlier receipts remain unchanged.

## An explicit counterexample

Use the stated quotient model `K = T²/<tau>`, where `tau(x,y)=(x+1/2,-y)` modulo the integer lattice. The torus translation

$$F(x,y)=(x,y+\tfrac12)$$

commutes with `tau` on the torus and descends to a diffeomorphism of `K`. Its square is the identity on the torus, and its action on `H₁(T²;Z)` is the identity matrix. Translation is homotopic to identity on the torus; the intermediate translations do not all descend to the Klein bottle.

To distinguish the downstairs class, take universal-cover generators

$$a(x,y)=(x,y+1),\qquad b(x,y)=(x+\tfrac12,-y),\qquad bab^{-1}=a^{-1}.$$

Write group elements as `a^m b^n`, represented by `(m,n)`. Their product is

$$(m,n)(p,q)=(m+(-1)^n p,n+q).$$

Conjugation by `F` fixes `a` and sends `b` to `ab`. On normal forms it is

$$H(m,n)=(m+(n\bmod2),n).$$

It fixes every `(m,2n)` in the torus-cover subgroup. But an inner automorphism, conjugating by any `(m,n)`, sends `b` to `(2m,1)`. The proposed automorphism sends it to `(1,1)`. Parity excludes every possible inner conjugator. Thus the descended diffeomorphism is not isotopic to identity: an isotopy to identity would induce an inner automorphism on the fundamental group. Its square is inner conjugation by `a`, in agreement with an order-two downstairs class.

This also appears in ordinary Klein-bottle homology: `H₁(K;Z)=Z⊕Z/2`, and `b` changes by the nonzero torsion class of `a`. Identity action on the cover's homology therefore loses information that survives downstairs.

The published *Characteristic classes of Klein bottle bundles*, sections 2 and 6, identifies the antipodal map on the circle fibers with the nontrivial Dehn-twist class. In these coordinates that antipodal map is precisely `F`. This supplies an external geometric identification of the explicit witness. [Publisher source](https://doi.org/10.1016/j.topol.2017.01.026)

## What survives and what changes

Every diffeomorphism has a natural lift to the orientation cover, obtained by transporting the local orientation. Choosing this lift gives an orientation-preserving torus map. The construction of the orientation cover and the Klein-bottle covering model are described in Hatcher, section 3.3, page 234, and Example 1.42. [Author's text](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf)

A lift normalizes the two-element deck group and therefore commutes with its nonidentity element. This group implication is now separately kernel-checked. The original centralizer calculation still excludes `[[1,2],[0,1]]`. Requiring determinant one restricts the canonical lift's matrix to `I` or `-I`; identity and `R(x,y)=(-x,-y)` realize these matrices. The exact affine check verifies `RaR⁻¹=a⁻¹` and `RbR⁻¹=b⁻¹`, so `R` also descends. The half-translation and identity give distinct classes with matrix `I`, so this representation is not faithful. Koberda's Proposition 6.1 provides a separate published computation of the four-element outer automorphism group. [Primary paper](https://nyjm.albany.edu/j/2011/17-33p.pdf)

The exact parabolic clause remains obstructed. The weaker condition “a nontrivial class has cover-homology trace two” is possible. Neither that trace nor this counterexample establishes a self-linking number, a coupling constant, or the downstream physical identifications. Those require separate definitions and derivations.

## Verification and remaining scope

- [Formal audit](Formal_Audit.json) checks the unchanged matrix proof and [KleinLiftAudit.lean](../../../code/frontier_verification/proofs/KleinLiftAudit.lean), including the normal-form group laws, automorphism and inverse, non-inner witness, cover-subgroup identity, square-inner relation, and the two matrix/normalizer implications. All 21 new theorem dependencies are printed; none contains `sorryAx`.
- [Audit artifacts](Formal_Audit_Artifacts.zip) retain six altered sources and their compiler rejections. [Development attempts](Development_Attempts.zip) preserve the earlier missing-import and algebraic-normalization failures.
- [Cross-method checks](Cross_Method_Checks.json) verify affine identities symbolically for all four parity combinations, compare 2,401 integer normal-form pairs, and confirm 49 cover elements. Universal claims rest on the symbolic/Lean arguments; finite enumeration supplies additional checks.
- [Sources](Primary_Sources.json), [integrity receipt](Verification.json), [manifest](Manifest.json), [extended event ledger](Branch_Events.jsonl), and [current queue](Research_Queue.json) retain provenance and exact continuation gates. The queue also corrects two inherited branch-reference mistakes: C06's LF parent is C03, and R11's contour parent is C02.

The new Lean file formalizes algebra, not the full surface, orientation-cover, homology, or isotopy constructions. Those geometric steps are explicit analytical arguments with primary references. Reproduction instructions are in [TOPOLOGY_README.md](../../../code/frontier_verification/TOPOLOGY_README.md). The next formal targets remain the mean-error asymptotics and the geometric functorial bridge; source and dataset mapping continues separately.
