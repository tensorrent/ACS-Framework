# Independent adversarial review of the RG invariant-region argument

Reviewed: `workstreams/rg/report.md`, Sections 2–3, with the retained Weyl mass map, one-loop evaluator, canonical metric, and quartic basis. Source hashes and independent rational-check results are in `evidence/rg_adversarial_review.json`. No RG file was modified.

**Verdict: no substantive mathematical error found within the declared one-loop model.** The Section 3 continuum argument establishes the claimed sufficient forward-invariant region for finite-dimensional RG solutions while they exist. Its positive margin is not inferred from numerical sampling. The Section 2 right-gauge exclusion and small-cube arithmetic also check. This review does not independently rederive every inherited beta coefficient from a quantum-field-theory renormalization calculation.

## Normalization and the norm derivatives

The retained evaluator returns scalar quartic beta coefficients divided by \(32\pi^2\), gauge beta functions divided by \(16\pi^2\), and Yukawa matrix beta functions divided by \(16\pi^2\). Thus, if \(R=\sum\operatorname{ReTr}(Y_i^\dagger B_i)\) is the Yukawa numerator and \(q=\sum\|Y_i\|_F^2\),

\[
(32\pi^2)q'=4R,
\qquad(32\pi^2)h'=-4\sum_a b_ag_a^4.
\]

There is no missing factor of two. The definition counts the full Frobenius norm of symmetric F, including both entries of an off-diagonal pair; the mass-map and beta conventions use the same definition.

The sum of the two matrix-difference squares is at most \(2t^2\), the trace-square contribution is at most \(4t^2\), and the separate \(4t^2\) term gives the stated total \(10t^2\). The mixed contributions are \((15/4+2)P=(23/4)P\), with \(0\le P\le tf\), while the F-only terms are bounded by \((17/2)f^2\). Hence

\[
R\le10t^2+\tfrac{23}{4}tf+\tfrac{17}{2}f^2\le10(t+f)^2.
\]

At three families the only positive contribution to \(\mathcal Bh\) is \((44/3)g_R^4\). Therefore

\[
\mathcal BQ\le40q^2+\tfrac{44}{3}h^2\le40(q+h)^2.
\]

These inequalities use upper bounds because the barrier derivative contains \(-\kappa\mathcal BQ\); the inequality direction is correct.

## Canonical fields and the fermion bound

The kinetic metric has 68 positive real entries. Direct expansion using rational arithmetic independently verifies the reported coefficient vector against \((x^TGx)^2/2\) on **all 11,093 monomials** of the union of the target and retained basis. Thus the factor \(r^4/2=2(N_\Phi+N_\Delta)^2\) is consistent with the stated convention.

For real canonical coordinates, the linear mass map gives

\[
\operatorname{Tr}(M^\dagger M)=u^TSu.
\]

Only the real symmetric part of the scalar Gram contributes to this quadratic form. Cauchy–Schwarz yields \(|\operatorname{Tr}(Z^\dagger Y)|\le t/2\), so the stated bidoublet eigenvalues are between 0 and \(8t\); the Delta eigenvalue is f. Therefore \(0\preceq S\preceq8qI\), and positivity of \(M^\dagger M\) gives

\[
2\operatorname{Tr}[(M^\dagger M)^2]\le2[\operatorname{Tr}(M^\dagger M)]^2\le128q^2r^4.
\]

No alignment or diagonal-flavor assumption enters this estimate.

## Contact, Hessians, and compactness

At a nonzero contact point of a nonnegative homogeneous quartic \(W=V_4-\kappa Qr^4\), its full gradient vanishes and its full Hessian is positive semidefinite. Considering a minimum on the unit sphere is sufficient because homogeneity and \(W=0\) also make the radial derivative vanish; equivalently, W is nonnegative everywhere in the ambient field space.

Let

\[
K=\kappa Q(8uu^T+4r^2I),\qquad H=K+P,\qquad P\succeq0.
\]

Here K is positive semidefinite because \(\kappa,Q\ge0\). Although squaring matrices is not generally operator-monotone, the **trace** comparison used in the report is valid:

\[
\operatorname{Tr}(H^2)-\operatorname{Tr}(K^2)
=2\operatorname{Tr}(KP)+\operatorname{Tr}(P^2)\ge0.
\]

The radial eigenvalue is \(12\kappa Qr^2\), and the 67 transverse eigenvalues are \(4\kappa Qr^2\). Thus \(144+67\cdot16=1216\) is correct. The wave terms have the asserted signs at contact. In particular,

\[
-6(C_gu)\cdot\nabla V_4
\ge-24\kappa Qr^2(9h/2)r^2=-108\kappa Qh r^4.
\]

Combining the bounds produces

\[
\mathcal BW\ge(1216\kappa^2-148\kappa-128)Q^2r^4,
\]

equal to \(102Q^2r^4\) at \(\kappa=1/2\). With h=0, the margin is 156. Both values were checked independently as rational identities.

For Q>0, the strict inward derivative on every active unit-sphere direction and compactness of the sphere exclude a first outward crossing. The coefficient ODE is polynomial and locally Lipschitz. Consequently the statement has its claimed local-existence boundary; it does not assert that the RG coefficients cannot develop a Landau pole.

## The Q=0 boundary

Q is a sum of squared real/complex coupling components. Q=0 means every gauge and Yukawa coupling vanishes. Their beta functions also vanish there, so uniqueness keeps them zero. The remaining potential evolution satisfies

\[
\mathcal BV_4(u)=\operatorname{Tr}[(\nabla^2V_4(u))^2]\ge0
\]

for each fixed real u, throughout its existence interval. Hence a nonnegative initial quartic remains nonnegative. This supplies the required boundary argument directly; no division by Q is needed. It also proves that a scalar fixed point with vanishing gauge/Yukawa couplings has zero quartic: a zero polynomial beta forces every Hessian to vanish, and quartic homogeneity then forces \(V_4=0\).

## Independent 2g/1Y fixed-point arithmetic

The norm identities imply \(t\le c_D/4\) and \(f\le2c_M/7\), including the zero-norm cases. Substitution into the right-gauge bracket gives exactly

\[
\tfrac{11}{3}+\tfrac{9045}{28}\alpha_4
+\tfrac34\alpha_L+\tfrac{14543}{84}\alpha_R>0.
\]

Thus a simultaneous gauge/Yukawa zero has \(g_R=0\). The remaining necessary condition for nonzero \(g_4\) yields

\[
\max(\alpha_4,\alpha_L)\ge
\frac{23/3}{643/6+9/2}=\frac{23}{335}.
\]

When \(g_4=0\) and \(g_L\ne0\), the bound \(\alpha_L\ge3/8\) follows. The strict small-cube exclusion and its restriction to the stated loop truncation are correct. Independent rational substitution also verifies all seven representative candidate faces printed in the report; this does not certify their scalar quartic equations.

## Suggested precision improvement

The word “cone” is accurate under the natural **weighted scaling**

\[
\lambda_i\mapsto a^2\lambda_i,\qquad (Y,Z,F,g)\mapsto a(Y,Z,F,g),\quad a\ge0.
\]

It is not an ordinary cone under uniform scaling of all original coupling coordinates, since V is linear in quartics while Q is quadratic in gauge/Yukawa couplings. Calling it a “forward-invariant region” or a “weighted cone” avoids that minor ambiguity. This terminology point does not affect the positivity theorem or its numerical constants.
