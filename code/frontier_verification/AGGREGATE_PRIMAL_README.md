# Simultaneous cuts, complete target projection and discriminant parity

All seventeen benchmark coefficients through 31 are now necessary consequences of the declared data at ordinate radius **1/10 for A** and **3/50 for B**. The preceding sufficient radii were 2/25 and 1/20. This pass combines freshly certified inequalities, exhaustive finite target branching and a consequence of the supplied signed discriminant. Both inherited seed profiles now use discriminant and its square consequence; the final claim is not degree-only recovery.

The [evidence package](../../docs/frontier/2026-09-14-aggregate-primal-delta/README.md) retains every proposal, certificate, witness, failure and audit. No additional zeros, measurements, defining polynomials, field catalogue, Galois-group label or arithmetic coefficient seed enters inference. Degree four, signature (0,2), absolute field discriminant 576 and the complete finite aggregate critical-line root population through 20 remain the input contract. Earlier wider-to-narrower domain transfer supplies valid seeds at each tested radius. Held-out arithmetic checks the output downstream.

## Keep the whole inequality

Earlier runs used a nonnegative multiplier vector to bound one target after maximizing residuals over current coefficient domains. Here each distinct nonzero vector from the listed earlier records, plus all 34 signed unit rows, receives a new continuum budget at the current radius. The pool has 163 directions for A and 188 for B. A direction's old selection radius is not a premise of its fresh certificate.

Writing the outward rounded nominal rows as A c <= b and their common-displacement error budget as E(lambda), retain

    (lambda A) c <= lambda b + E(lambda).

The nominal rows use the unwidened observation bounds. The finite-root and unknown-tail uncertainty enters the freshly audited budget once. Integer row reconstruction removes the dummy target label and retains all 604 coefficient columns. Common integer scale is 2^384 * 10^9; subsequent normalization divides only by exact powers of two. The audit checks 378,480 stored midpoint values/derivatives, 756,960 fresh complex quadratic leaves and 1,404 displaced mpmath controls. Real and complex interval paths share FLINT; the displaced controls are samples.

At each prime, enumerate generic degree-four local models (e,f) with sum(e*f)=4 and coefficient c_(p^k)=sum_(f|k) f. One nonnegative pattern weight per local coefficient vector, with weights summing to one, represents its convex hull. For nonnegative cut multipliers mu and residual r=s*e_j-mu*A, the exact bound is

    s*c_j <= mu*b + sum_over_primes max_over_allowed_patterns(r dot pattern).

All solver scales are converted back before exact integer and independent Fraction replay. Replacing the maximum by a minimum is unsound; the adversary stores an actual feasible witness contradicting that substitution. Floating solvers propose certificates, not mathematical acceptance decisions.

## What finite branching adds

Eight model-hull cases compare 34 unit rows with the full pool under the same previously mixed-cut seeds. This is not an unseeded unit-only experiment. Fifty-two fresh exact objectives make no new individual-domain exclusions. Of 78 maximum-slack MILP proposals, 66 satisfy their selected cuts and 37 satisfy the entire pool. Twelve solver-status-zero proposals have negative exact slack and remain rejected: optimal slack can be negative.

Fixing all remaining target values simultaneously creates 50, 9, 24 and 16 branches for A/degree-only seed, A/discriminant seed, B/degree-only seed and B/discriminant seed respectively. For each conditional local hull, a phase LP proposes nonnegative cut multipliers. Apply the preceding bound to the constant objective zero. An exact upper bound below zero refutes the entire conditional hull.

All **99** assignments are accounted for: **91** have strict rational separation certificates, **8** have complete integer local-model witnesses, and **0** are unresolved. Independent enumeration verifies Cartesian coverage; Fraction arithmetic replays every separation. Every surviving witness also strictly satisfies fresh unrounded 384-bit inequalities. This proves the exact target projection of the declared finite relaxation, not existence of alternate spectra or fields.

Each seed profile leaves the same two target tuples per observation. A's alternatives differ as (c29,c31)=(0,4) or (2,1), with c25=4. B's differ as (c23,c25,c29,c31)=(0,4,0,0) or (1,0,1,0). All other target coefficients are fixed.

## Derive the missing local restriction

The field discriminant has sign (-1)^r2. For an integral basis b_j and the four embeddings sigma_i into a Galois closure, put Delta=det(sigma_i(b_j)). Then Delta^2 is the signed field discriminant. These facts and the index-square change of discriminant are given in Milne, [Algebraic Number Theory, Proposition 2.26, Remark 2.25 and Proposition 2.40](https://www.jmilne.org/math/CourseNotes/ANT.pdf). The permutation-discriminant criterion is also stated in [Fields and Galois Theory, Proposition 4.1 and Corollary 4.2](https://www.jmilne.org/math/CourseNotes/FT.pdf).

For the supplied signature, signed D=576=24^2. Consequently Delta=+24 or -24 is rational and nonzero. Every automorphism fixes Delta while permuting its embedding rows. The row permutation must therefore be even: the permutation group lies in A4. This does not identify it as V4.

A second derivation works directly at any p not dividing 576. Reduction of an integral basis gives the finite algebra O_K/p O_K, a product of finite fields F_(p^f), with sum(f)=4. Its embedding determinant d has d^2=576 mod p. Here p is odd and d=+24 or -24 belongs to F_p and is nonzero. Frobenius fixes d, so its row permutation is even. On the embeddings of a factor F_(p^f), Frobenius has an f-cycle. Thus (-1)^(4-number_of_factors)=+1. This uses the actual ring of integers, independently of a chosen power basis. Milne's [Theorem 3.35, Lemma 3.36 and Corollary 8.22](https://www.jmilne.org/math/CourseNotes/ANT.pdf) supply the ramification, reduction and Frobenius ingredients.

The only even unramified partitions of four are 1+1+1+1, 1+3 and 2+2, giving (c_p,c_(p^2))=(4,4),(1,1),(0,4). Independent inversion counts, permutation determinants and orbit enumeration check all 24 permutations and the 12 even ones. A's c29=2 requires the forbidden partition 1+1+2. B's already-fixed c5=0 together with the alternative c25=0 requires the forbidden partition 4. Both unwanted tuples are excluded. Each remaining tuple also has a new full 604-coefficient integer witness obeying the parity rule at every unramified prime, all local ramification conditions and all cuts. These witnesses establish consistency of the strengthened relaxation only.

The source-backed general arithmetic argument above is written mathematics; it is not yet formalized in Lean. Finite permutation checks are not a substitute for that argument.

## Guard the hypotheses

- At ramified primes 2 and 3, the unramified cycle-count rule is not applied. The model (e,f)=(2,2), giving c2=0 and c4=2, must remain possible.
- Absolute square alone is insufficient. The irreducible polynomial x^4-x^2-1 has signed discriminant -400, two real roots and an irreducible reduction modulo 3. It supplies an odd four-cycle despite square absolute discriminant. Signed polynomial and field discriminants have the same square class.
- Square discriminant does not imply V4. The irreducible polynomial x^4-x^3-7*x^2+2*x+9 has discriminant 163^2 and factors modulo 2 as (x+1)(x^3+x+1). Its three-cycle remains allowed. Exact Sylvester determinants, independent irreducibility checks and modular factorizations verify both controls.
- B's original polynomial has discriminant 14400=576*5^2. Its reduction modulo 5 has repeated factors even though 5 is unramified in the field. The alternate generator alpha+2*beta yields x^4-2*x^3+19*x^2-18*x+57, whose discriminant is prime to 5 and whose reduction has two distinct quadratic factors. These polynomials are downstream controls, not decoder inputs.

Ten semantic mutations are rejected. The first source acquisition failed with HTTP 406; a separately preserved version with standard headers succeeded. The first parity auditor hit SymPy/FLINT expression-factor sorting; version two uses the polynomial factor API. Both failed sources and receipts remain frozen. No executed instrument was overwritten.

## Reproduction and next delta

With the inherited pinned Python runtime and libraries, run:

    python code/frontier_verification/verify_aggregate_primal_delta.py

The verifier checks prior checkpoints recursively, extracts archived inputs, freshly regenerates all pool certificates and independent budgets, reruns the model-hull LP deductions, and independently replays every stored integer proposal, all joint-branch separators, coverage, strengthened witnesses, parity controls and mutations. It does not repeat the MILP witness search or joint branch LP search: acceptance depends on the stored points and exact certificates, all rechecked. Download fingerprints are verified against the archived acquisition outputs; network retrieval is not repeated.

The successful radii extend to contained smaller boxes under the same contract. They are sufficient certificates, not optimal noise thresholds. Next test wider radii using the newly derived parity rule, examine what the spectral data contribute beyond that rule, construct further actual-field examples and investigate global compatibility beyond local finite relaxations. The classification of all fields with the metadata, infinite arithmetic bridges, formalization, and the wider ACS queue remain open.
