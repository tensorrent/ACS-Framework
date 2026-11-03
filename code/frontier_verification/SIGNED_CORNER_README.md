# Signed resolvents and a uniform corner bound

The [certificate](../../docs/frontier/2026-09-14-aggregate-signed-corner-delta/Signed_Corner_Certificate.json) improves the uniform feature-error guarantee on the inherited radius-0.01 cube to approximately **1.8011173562984702e-10**. The exact rational upper bound on the critical inverse row norm is approximately **55.5210906442615**. The [independent audit](../../docs/frontier/2026-09-14-aggregate-signed-corner-delta/Independent_Signed_Corner_Audit.json) uses real derivative polynomials, a separately certified majorant and Cramer determinant ratios. The preceding actual ambiguity upper endpoint is approximately **1.831989439894397e-10**, leaving a ratio of approximately **1.0171405175170667**. The exact source-feasible threshold remains open.

All inequalities below refer to exact rational inputs and interval bounds in the reports. Displayed decimals are explanatory. Indices are zero based; the critical coordinate is 1, and the exceptional replacement coordinate is 12.

## Unchanged observation contract

The inherited complete class has two quartic fields of signature (0,2) and absolute discriminant 576: Q(sqrt(2),sqrt(-3)) and Q(sqrt(-2),sqrt(-3)). Their complete positive source prefixes below 39/2 each have 22 entries. Source selection takes place before independent absolute root-coordinate errors, preserving every entry and multiplicity. The rational center c and source threshold enclosure [L,U] are inherited unchanged; U-L=2e-30. Root error is r=U-1e-8<L. The critical coordinates of any two observations from different fields differ by at least 2(L-r).

The ordered map Phi has 22 additive finite features. The first 17 are 2 sum_i exp(-y_i^2/25) cos(log(m)y_i), for m=2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31. Feature 17 is sum_i 3/(9/4+y_i^2). The last four Gaussian features have (m,a)=(37,1/25),(2,1/24),(41,1/25),(43,1/25). No raw roots, counts, infinite moment or unknown tail is supplied. Additional feature errors have independent absolute component bounds. Main corner conclusions require every observed root in Q={y: |y_j-c_j|<=1/100}; the simpler signed bound also applies to the previously certified radius-3/100 cube.

Write g(t) for the vector of these scalar kernels, so Phi(y)=sum_j g(y_j). Kernels are smooth on the whole real line: the rational denominator is positive and the Gaussian/trigonometric factors are smooth. The rational preconditioner R comes from checkpoint 28. Its determinant is nonzero, also verified modulo 65537.

## The matrix family contains every secant

For a fixed radius eta, let I_j=[c_j-eta,c_j+eta], H_j be the closed convex hull in R^22 of {g'(t):t in I_j}, and H be the family of matrices with column j in H_j. H is convex and therefore connected; it contains every Jacobian on Q and every independent mixture of its columns. These are column hulls, not arbitrary entrywise mixtures of unrelated bounds.

For y,z in Q, define M_j=integral_0^1 g'(z_j+t(y_j-z_j)) dt. Riemann sums are convex combinations of derivative columns and converge in finite-dimensional space, hence M_j belongs to the closed hull H_j. This remains true when y_j=z_j. The fundamental theorem of calculus component by component gives Phi(y)-Phi(z)=M(y-z). Thus the entire secant matrix belongs to H. No assumption that Phi(Q) is convex is used.

Checkpoint 29 establishes |I-RJ|<=B column by column for all derivative choices on the coordinate intervals. Each map z -> e_j-Rz is affine; its coordinate absolute-value sublevel sets are closed and convex. The same bound therefore holds for every column in H_j, and |I-RM|<=B for every M in H. B is nonnegative, w is strictly positive and Bw<w/2. In the weighted maximum norm this gives ||I-RM||<1/2. The Neumann series proves I-E=RM nonsingular for E=I-RM, hence M nonsingular. The determinant is continuous, never zero on connected H, and has constant sign.

## Exact signed resolvent bounds

Put C=(I-B)^-1=sum_(n>=0) B^n. Absolute convergence follows from Bw<w/2. C and C-I are nonnegative. For every M in H,

    Y=M^-1=(I-E)^-1 R,
    |(I-E)^-1-I| <= C-I.

The critical row of C is computed by exact rational elimination and its residual is checked. The certificate explicitly verifies every entry of its critical row minus the identity row is nonnegative. Define delta_k=sum_i (C_(1,i)-delta_(1,i))*|R_(i,k)|. Then |Y_(1,k)-R_(1,k)|<=delta_k. Let v_k=sign(R_(1,k)), u0=Rv, and h solve (I-B)h=|u0|. Exact residuals, h>0 and the weighted contraction give

    |Yv| <= h,        |Yv-u0| <= B h = h-|u0|.

For a row x and v_k in {-1,+1}, |x_k|=v_k*x_k+2*max(0,-v_k*x_k). The entrywise deviations imply

    ||e_1^T Y||_1 <= h_1 + 2 sum_k max(0,delta_k-|R_(1,k)|).

At eta=0.01 every row sign is strict and equals v, so the penalty is zero and K(M)=e_1^T M^-1 v equals the row norm. The signed bound alone is approximately 56.444509737543164. At eta=0.03 four signs remain unresolved, at indices 0,3,5,19; retaining the explicit penalty gives approximately 79.52254826663243 and a noise guarantee approximately 1.2575049741201502e-10. No corner theorem for that larger cube is claimed.

The independent route uses its own 48-bit B, exact FLINT rational inversion with checked residuals, and a finite nonnegative Neumann sum plus a rigorous weighted tail, producing h>=|u0|+Bh. The weaker inequality suffices: |Yv-u0|<=Bh<=h-|u0|. Its independently derived signed bounds are no larger than the primary claims.

## Uniform curvature factors

The corner argument uses a factor bound valid independently for every M in H and every t in I_j. Let b(t)=R g''(t). Around c_j, expand b through powers 0,...,5 using scalar derivative orders 2,...,7. For each component, bound the sixth-order remainder by eta^6/6! times sum_k |R_(i,k)| sup_(t in I_j)|g_k^(8)(t)|. Multiplication by R precedes absolute values in the Taylor coefficients, preserving cancellation. The entire remainder is bounded without cancellation.

If b_i(c_j) is the constant term and rho_i its variation bound, then

    e_1^T M^-1 g''(t)
      belongs to b_1(c_j) +/- [rho_1 + sum_i (C_(1,i)-delta_(1,i))*(|b_i(c_j)|+rho_i)].

This follows from M^-1 g''=(I-E)^-1 b and the same positive resolvent bound. The interval is uniform over M and t, even when t is unrelated to M's jth column. Complex Hermite recurrences and complex partial fractions at 896/1152 bits certify all 22 curvature signs. Independent real sine/cosine polynomials and exact rational-moment numerator recurrences through order 8 certify the same signs at both precisions. Interval arithmetic encloses full coordinate intervals; signs are not inferred from sample points.

The intervals u0_j +/- (h_j-|u0_j|) certify 21 signs for (M^-1 v)_j throughout H. Only coordinate 12 crosses zero in this global enclosure. Its curvature sign is negative. The resulting directions for coordinates 0,...,21 are

    [+,+,+,+,-,+,-,+,+,-,+,+,?,+,+,+,+,-,+,+,+,+].

## Column replacement proof of the corner maximum

Suppose A is the new matrix, B the old matrix and d is the new column minus the old column in position j, so A-B=d e_j^T. Both lie in H. The exact inverse identity gives

    A^-1-B^-1 = -A^-1 (A-B) B^-1,
    K(A)-K(B) = -(e_1^T A^-1 d)*(B^-1 v)_j.

This is a finite difference identity; replacing the last factor by (A^-1 v)_j would generally be wrong. The matrix version and Cramer's rule are documented in [Mathlib's nonsingular inverse module](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/NonsingularInverse.html); exact pinned local sources are archived separately from current documentation.

Fix the new matrix A and the functional ell=e_1^T A^-1. Its derivative on the scalar column curve is ell*g''(t), with the certified constant sign a_j. Therefore ell*g'(t) is monotone on I_j by the mean value theorem. For either endpoint direction d_j in {-1,+1}, ell*(g'(c_j+d_j*eta)-z) has weak sign a_j*d_j for every derivative column z. Linearity extends the inequality to convex combinations, and continuity extends it to the closed convex hull. This is an endpoint comparison with A held fixed; it does not differentiate A while comparing arbitrary hull columns.

For each of the 21 uniformly signed directions u_j=sign((B^-1 v)_j), choose d_j=-a_j*u_j. The preceding identity then gives K(A)>=K(B). Replace these 21 columns in ascending index order, leaving column 12 untouched. Every intermediate matrix remains in H; all bounds continue to apply. The resulting face has those 21 columns fixed at their designated endpoint derivatives.

On this face, Cramer's rule writes (M^-1 v)_12=det(M with column 12 replaced by v)/det(M). The numerator is independent of the varying column 12. The [adjugate module](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/Adjugate.html) supplies this determinant definition. The denominator has the same nonzero sign across H. At the face reference with column 12 equal to g'(c_12), rigorous interval inversion proves the quotient negative; independent Cramer determinant ratios prove it again. Hence it is negative throughout this face, including arbitrary convex mixtures. This argument does not assert a global sign for coordinate 12 on H.

The curvature factor for coordinate 12 is negative. Set its column to the lower endpoint g'(c_12-eta); the same endpoint comparison makes K nondecreasing. All columns now equal the single reported corner Jacobian J*. Consequently K(M)<=K(J*) for every M in H. J* itself belongs to H, so it attains the maximum of this outer matrix-family norm. Primary interval inverses at 1024/1536 bits bound its row norm from above by an exact dyadic rational with denominator 2^80. The independent audit reconstructs all 22 critical inverse-row entries as det(J* with column 1 replaced by e_k)/det(J*) at 896/1152 bits and verifies the same upper bound.

## Finite-difference and field consequence

Every secant M is in H. Therefore

    |y_1-z_1| = |e_1^T M^-1 (Phi(y)-Phi(z))|
               <= K_upper * ||Phi(y)-Phi(z)||_infinity.

Different source fields have |y_1-z_1|>=2(L-r). Thus their features differ by at least 2(L-r)/K_upper in infinity norm. If a common report were within tau of both, their feature difference would be at most 2*tau. This is impossible for tau<(L-r)/K_upper. Equality at the rational lower bound is not settled by this strict guarantee.

The source class, finite populations and 604-column arithmetic map are inherited and recursively verified. A fresh arithmetic route repeats 1128 polynomial factorizations and 1208 coefficient comparisons. Field identity fixes the tracked vector below the guarantee. The previously certified ambiguous midpoint above it retains 456 fixed and 148 ambiguous coefficient domains. The corner matrix need not represent a source-feasible pair; its outer-family maximum does not prove sharpness of the source-constrained ambiguity threshold or implement an arbitrary-report decoder.

## Verification and remaining scope

Run the repository's pinned Python environment with `code/frontier_verification/verify_aggregate_signed_corner_delta.py`. This replays the four preserved exploratory scripts, regenerates both certificates and adversaries, freshly compiles the Lean lemmas, checks source/receipt/ledger integrity, then recursively verifies the preceding checkpoint. See the dated package for runtime and source hashes.

Eight Lean lemmas establish the noncommutative inverse identity, rank-one column action and replacement, Cramer numerator invariance, same-sign denominator transfer, nondecreasing endpoint steps, finite convex combination bounds and a replacement chain. The full Neumann/Taylor/closed-hull/integral/connectedness assembly and concrete ACS conclusion are written or computational, not a wholly Lean-formalized theorem. The independent interval routes share FLINT and source premises; two precision runs alone are not independent methods.

Adversaries check exact certificate premises and finite matrix counterexamples to invalid sign, inverse and convex-family shortcuts. Failed proof compilation and setup attempts are preserved alongside corrected versions and actual logs. The prior failure history is retained by the recursive chain.

Next gates include source-constrained lower bounds beyond the outer-family maximum, improved source-feasible upper pairs, bounded-error inverse-set decoding, global regions or counterexamples, and complete analytic formalization. All 117 ACS branches and private-input gates remain tracked. This checkpoint records a forward delta and makes no global completion claim.
