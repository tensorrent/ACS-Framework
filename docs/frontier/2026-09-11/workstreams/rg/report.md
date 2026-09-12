# RG frontier: two-loop gauge sector, fixed-point obstructions, and a positive invariant cone

This continuation completes the **two-loop gauge beta functions** of the declared minimal unbroken Pati–Salam theory, proves a **positive invariant region for its full one-loop scalar/gauge/Yukawa flow**, and constrains interacting fixed points of the **2-loop gauge / 1-loop Yukawa / 1-loop scalar truncation**. These are different loop-order statements. Full two-loop Yukawa and scalar beta functions and physical threshold matching remain open.

All calculations retain the previous canonical action, all seventeen real quartics, and arbitrary complex family matrices Y,Z with symmetric F. The main three-family conclusions do not impose diagonal flavor matrices, a vanishing current quartic, CP symmetry, or an O(8)×O(60) restriction.

## 1. Complete two-loop gauge result

Write L=16π², a∈(4,L,R), t=Tr(Y†Y+Z†Z), and f=Tr(F†F). In dimensional regularization with modified minimal subtraction,

\[
\beta_{g_a}=-\frac{g_a^3}{L}b_a+\frac{g_a^3}{L^2}\left[\sum_b B_{ab}g_b^2-D_a\right]+\text{higher loops}.
\]

For n identical chiral families,

\[
b=\left(\frac{35-4n}{3},\;7-\frac{4n}{3},\;\frac{1-4n}{3}\right),\qquad
D=\left(4t+\frac{15}{2}f,\;4t,\;4t+15f\right),
\]

\[
B=\begin{pmatrix}
\frac{205n+28}{6}&\frac{3n}{2}&72+\frac{3n}{2}\\
\frac{15n}{2}&\frac{49n}{3}-41&3\\
360+\frac{15n}{2}&3&\frac{49n+437}{3}
\end{pmatrix}.
\]

In particular,

\[
B_{n=3}=\begin{pmatrix}
643/6&9/2&153/2\\
45/2&8&3\\
765/2&3&584/3
\end{pmatrix},\qquad b_{n=3}=(23/3,3,-11/3).
\]

Scalar quartics do not enter this two-loop gauge sector. `two_loop_gauge.py` evaluates the formula and also exposes `beta_211`, which changes only the gauge derivatives in the retained full one-loop evaluator.

### Derivation and independent checks

The input general gauge formula and semisimple substitution are equations (30)–(31) and (106)–(110) of [Luo, Wang and Xiao](https://arxiv.org/pdf/hep-ph/0211440). They use real scalars and κ=1/2 for Weyl fermions. Converting to complex scalar representations doubles the scalar index. Our resulting representation sums are:

| Field | Copies | Dimension | (C4,CL,CR) | (T4,TL,TR), including spectator dimensions |
|---|---:|---:|---|---|
| L=(4,2,1), Weyl | n | 8 | (15/8,3/4,0) | (1,2,0) |
| R=(bar4,1,2), Weyl | n | 8 | (15/8,0,3/4) | (1,0,2) |
| Φ=(1,2,2), complex | 1 | 4 | (0,3/4,3/4) | (0,1,1) |
| Δ=(bar10,1,3), complex | 1 | 30 | (9/2,0,2) | (9,0,20) |

The first route inserts these rational invariants into the Weyl/complex-scalar formula. The second route explicitly constructs all normalized fundamental SU(4) and SU(2) generators, induces their symmetric-square representations, and exactly verifies their quadratic Casimir matrices and pairwise generator traces. A separate component-weight sum uses H4=diag(1/2,−1/2,0,0), H2=diag(1/2,−1/2), and the weights hi+hj for i≤j. The symmetric-square indices are 3 and 2, producing the spectator-weighted Δ indices (9,0,20). Reassembling the two-loop matrix in the real-scalar convention agrees identically for symbolic n.

For the Yukawa trace, put \(\widehat T_A=G_{AA}^{-1/2}\partial_A M\). The formula is \(D_a=d(G_a)^{-1}\operatorname{Tr}[C_a(F)\sum_A\widehat T_A\widehat T_A^\dagger]\). The declared vertices give total L and R block traces 16t and 16t+60f. Their Casimirs yield D above; mixed Y/Z and Dirac/Majorana traces cancel or lie in distinct scalar directions. A separate component calculation constructs the entire quadratic Gram matrix on **all 22 real Yukawa coordinates at two families**, including both real and imaginary parts and off-diagonal symmetric F. Every off-diagonal residual and every diagonal coefficient residual is exactly zero in dyadic arithmetic. The family-independent proof is the preceding block trace identity; the finite-family Gram is an independent implementation check.

There is also an external check: after permuting (L,R,4) to our order, the matrix agrees with equation (16) of [Chakrabortty and Raychaudhuri](https://arxiv.org/pdf/0909.3905) and equation (45) of [Dark matter and gauge coupling unification in nonsupersymmetric SO(10) grand unified models](https://link.aps.org/accepted/10.1103/PhysRevD.91.095010). These compare the gauge coefficients; they do not verify our convention-dependent F normalization or new theorems.

## 2. Reopening S21 at 2-loop gauge / 1-loop Yukawa order

Let \(\alpha_a=g_a^2/L\), \(\tau=t/L\), \(\varphi=f/L\). At any simultaneous one-loop Yukawa zero, summing the Y and Z norm equations gives

\[
0=\|YY^\dagger-ZZ^\dagger\|_F^2+\|Y^\dagger Y-Z^\dagger Z\|_F^2
 +4t^2+16|\operatorname{Tr}(Z^\dagger Y)|^2+\frac{15}{4}P-c_Dt,
\]

where \(P=\operatorname{Tr}[(Y^\dagger Y+Z^\dagger Z)F^\dagger F]\ge0\). Hence \(t\le c_D/4\), including t=0. The F norm equation gives

\[
0=2P+\frac{15}{2}\operatorname{Tr}[(F^\dagger F)^2]+f^2-c_Mf.
\]

For three families, \(\operatorname{Tr}[(F^\dagger F)^2]\ge f^2/3\), so \(f\le2c_M/7\). Here

\[
c_D=\frac{45}{4}g_4^2+\frac94(g_L^2+g_R^2),\qquad
c_M=\frac{45}{4}g_4^2+\frac92g_R^2.
\]

Substituting these upper bounds into the R-gauge beta bracket proves

\[
-b_R+(B\alpha)_R-4\tau-15\varphi
\ge\frac{11}{3}+\frac{9045}{28}\alpha_4+\frac34\alpha_L+\frac{14543}{84}\alpha_R>0.
\]

**Every simultaneous 2g/1Y fixed point at three families therefore has gR=0**, without any flavor ansatz or small-coupling assumption. This remains a statement about that truncation: two-loop Yukawa nullclines need not satisfy the inequalities used here.

If g4≠0, its gauge equation further requires

\[
\frac{643}{6}\alpha_4+\frac92\alpha_L\ge\frac{23}{3},
\]

so \(\max(\alpha_4,\alpha_L)\ge23/335\approx0.0686567\). If g4=0 but gL≠0, then \(\alpha_L\ge3/8\). Thus in the explicit cube

\[
\max_a\frac{g_a^2}{16\pi^2}<\frac{23}{335},
\]

the 2g/1Y/1scalar system has only the Gaussian dimensionless fixed point. Once the gauge couplings vanish, the previous positive Yukawa norm identity and scalar Hessian identity eliminate nonzero Yukawa and quartic zeros. This is a rigorous bound for the truncated equations, not an all-orders no-go theorem or a universal definition of perturbativity.

### Explicit surviving algebraic candidates

The invariant flavor ansatz Y=yI3, Z=0, F=f0I3 reduces the gauge/Yukawa equations to linear equations in (α4,αL,u,v), where u=y²/L and v=f0²/L. All fifteen nonempty active-coordinate faces were solved exactly; five nonpositive solutions were retained as rejected faces. Representative accepted candidates are:

| Active couplings | α4 | αL | u | v |
|---|---:|---:|---:|---:|
| g4 | 46/643 | 0 | 0 | 0 |
| gL | 0 | 3/8 | 0 | 0 |
| g4,gL | 574/9073 | 1788/9073 | 0 | 0 |
| g4,Y | 161/2048 | 0 | 1035/16384 | 0 |
| g4,F | 644/6977 | 0 | 0 | 690/6977 |
| g4,Y,F | 713/7334 | 0 | 3105/58672 | 345/3667 |
| g4,gL,Y,F | 3364/39025 | 10617/39025 | 14517/156100 | 2913/39025 |

All ten accepted faces are in `results.json`. They were checked again in the actual matrix Yukawa evaluator and by direct Weyl-vertex traces in the gauge beta function. The largest residual is numerical roundoff below 10⁻¹⁰. These are **gauge/Yukawa candidate zeros**, not complete fixed points: no scalar quartic zero or scalar boundedness condition has been asserted at them. Some pass crude g²/(4π)<1 cuts; that alone does not bound omitted-loop effects. They lie outside the proved small-cube exclusion. Stability, higher-loop shifts, and a full scalar solution remain work.

## 3. S22: a positive invariant region for the full one-loop flow

There is now a nontrivial positive invariant cone allowing all three gauge couplings and arbitrary Y,Z,F. This result uses **one-loop gauge running**, alongside one-loop scalar and Yukawa running.

Use canonical coordinates u=G¹ᐟ²x, let r²=uᵀu, and define

\[
q=\operatorname{Tr}(Y^\dagger Y+Z^\dagger Z+F^\dagger F),\quad
h=g_4^2+g_L^2+g_R^2,\quad Q=q+h.
\]

For three families, the closed set

\[
\boxed{\quad V_4(u)\ge\frac{Q}{2}(u^Tu)^2\quad\text{for every }u\in\mathbb R^{68}\quad}
\]

is forward invariant under the full one-loop equations, for as long as that solution exists. In a physical application the loop truncation must still be used within its validity range. Arbitrarily small nonzero Yukawa and gauge couplings occur inside this cone, so it is not empty near the origin.

### Continuum proof, with all constants

Write \(\mathcal B=32\pi^2d/d\log\mu\). The inherited potential formula in canonical coordinates is

\[
\mathcal B V_4=\operatorname{Tr}H^2+3\operatorname{Tr}(M_V^2)^2
-2\operatorname{Tr}(M^\dagger M)^2
+2(Su)\cdot\nabla V_4-6(C_gu)\cdot\nabla V_4,
\]

where H=∇²V4, \(S_{AB}=\operatorname{ReTr}(\widehat T_A^\dagger\widehat T_B)\succeq0\), and \(C_g\) has eigenvalues \(3(g_L^2+g_R^2)/4\) on Φ and \(9g_4^2/2+2g_R^2\) on Δ. The vector-mass term is nonnegative because MV² is a Gram matrix.

The scalar Yukawa Gram has bidoublet eigenvalues \(4t\pm8|\operatorname{Tr}(Z^\dagger Y)|\) and Δ eigenvalue f. Cauchy–Schwarz gives \(S\preceq8qI\). Consequently

\[
\operatorname{Tr}(M^\dagger M)\le8qr^2,\qquad
2\operatorname{Tr}(M^\dagger M)^2\le128q^2r^4.
\]

Let R0 be the gauge-free Yukawa norm derivative numerator from the previous release. Its positive decomposition also supplies an upper bound:

\[
R_0\le10t^2+\frac{23}{4}tf+\frac{17}{2}f^2\le10(t+f)^2=10q^2.
\]

The last inequality has exact residual \(57tf/4+3f^2/2\ge0\). Each of the two matrix-difference norms is at most t², the mixed-trace term is at most 4t², P≤tf, and Tr[(F†F)²]≤f². Gauge contributions decrease R. Therefore

\[
\mathcal Bq\le40q^2,\qquad
\mathcal Bh=-4\sum_a b_ag_a^4\le\frac{44}{3}h^2,\qquad
\mathcal BQ\le40Q^2.
\]

Consider a first contact point for \(W=V_4-\kappa Qr^4\ge0\), at r>0. Since W is nonnegative in all of R68 and vanishes there, ∇W=0 and ∇²W is positive semidefinite. Thus

\[
\nabla V_4=4\kappa Qr^2u,\quad
H\succeq\kappa Q(8uu^T+4r^2I),\quad
\operatorname{Tr}H^2\ge(144+67\cdot16)\kappa^2Q^2r^4=1216\kappa^2Q^2r^4.
\]

The Yukawa wave term is nonnegative at contact. Since \(C_g\preceq(9h/2)I\), the gauge wave term is at least \(-108\kappa Qh r^4\). Dropping the nonnegative vector-mass term and using q,h≤Q gives

\[
\mathcal BW\ge[1216\kappa^2-148\kappa-128]Q^2r^4.
\]

At κ=1/2 this equals **102Q²r⁴**, strictly positive for Q,r>0. The minimum over the compact unit sphere therefore cannot first cross outward. When Q=0 all gauge and Yukawa couplings remain zero, and the inherited scalar positivity theorem covers that boundary. This proves the claimed invariant cone. For g=0, the stronger same-form bound is 156q²r⁴.

### Independent implementation checks and scope

The scalar polynomial representing r⁴/2 was solved for in the old basis and verified exactly on **all 11,093 field monomials**. The coefficient vector per unit Q is

\[
(2,0,0,0,0,0,2,2,2,2,2,0,0,4,0,0,0).
\]

Thus one explicit boundary potential is 2Q(NΦ+NΔ)². The cone allows adding **any nonnegative gauge-invariant quartic remainder**. It does not assume that the boundary potential's radial symmetry persists under RG flow; angular couplings may be generated while the inequality stays true. This resolves the enhanced-symmetry objection in S11 for this sufficient positivity result.

The analytic proof is checked by exact rational constant identities. An independent component route reconstructs H, fermion mass M, scalar Gram S, and a 21-by-21 gauge-vector Gram from infinitesimal transformations of Φ and Δ. At six general three-family nonzero-gauge assignments, its contact derivative agrees with the assembled seventeen-quartic evaluator to at most 1.5×10⁻¹⁵ relative error. The gauge Gram agrees separately with the quartic gauge table to below 4.1×10⁻¹⁵ absolute error. Nine gauge-free assignments at one, two and three families provide additional checks. These component samples validate the implementation and normalizations; the continuum statement is proved by the inequalities, not inferred from sampling.

The cone is sufficient and conservative. It does not characterize every stable trajectory, specify a physical vacuum, extend the old positivity theorem to arbitrary unrestricted Yukawas, or prove two-loop positivity. The earlier negative fermion-box boundary counterexample remains valid outside this cone.

## 4. S20: what higher loops can and cannot repair

At Z=rY with r=2/3 the one-loop defect is

\[
B_Z-rB_Y=\frac{40}{27}\left[2\operatorname{Tr}(Y^\dagger Y)Y-YY^\dagger Y\right].
\]

Taking the real inner product with Y gives at least \(40[\operatorname{Tr}(Y^\dagger Y)]^2/27>0\) for Y≠0. Now scale gauge and Yukawa couplings by ε and scalar quartics by ε². This defect starts at ε³; two-loop Yukawa contributions start at ε⁵. Therefore higher loops **cannot turn constant 2/3 alignment into an identity of formal perturbation theory** in the same canonical model. An analytic invariant graph whose leading relation is Z=(2/3)Y and whose correction begins at weighted order three has the same obstruction: differentiating that correction first contributes at order five.

This is a leading-order argument, not a calculation of the unknown two-loop Yukawa polynomial. It does not exclude an accidental finite-coupling cancellation, a different leading relation, extra fields, nonanalytic corrections, or a different field parameterization. It sharpens the prior conclusion from a one-loop failure to a failure of formal perturbative protection with that leading alignment.

## 5. S04/S07/S17: threshold work already derivable, and the precise remainder

The unbroken beta coefficients above do not require physical mass inputs. A broken-phase EFT calculation does. For the conventional neutral Δ breaking to SU(3)c×SU(2)L×U(1)Y, use \(Y=T^3_R+(B-L)/2\). The normalized SU(4) generator is \(T^{15}=\sqrt{3/8}(B-L)\), giving the tree matching

\[
g_3=g_4,\quad g_2=g_L,\quad \frac1{g_Y^2}=\frac1{g_R^2}+\frac{2}{3g_4^2},\quad
\frac1{g_1^2}=\frac3{5g_R^2}+\frac2{5g_4^2}\quad(g_1^2=5g_Y^2/3).
\]

This agrees with equation (46) of the [independent SO(10) calculation](https://link.aps.org/accepted/10.1103/PhysRevD.91.095010). It is only the tree relation; finite one-loop threshold terms have not been set to zero.

The actual scalar branching can already be specified:

| Parent component | SU(3)c×SU(2)L | Hypercharges |
|---|---|---|
| Φ | (1,2) | −1/2,+1/2 |
| Δ symmetric anti-color pair | (bar6,1) | −4/3,−1/3,+2/3 |
| Δ anti-color/anti-lepton pair | (bar3,1) | −2/3,+1/3,+4/3 |
| Δ anti-lepton pair | (1,1) | 0,+1,+2 |

These dimensions sum to four and thirty complex scalar components. The neutral last-row component is a possible breaking direction, not a dynamically selected vacuum. Which components remain physical, which are eaten, their mixing, and their threshold scales require the chosen vacuum and its mass matrices.

Concrete remaining tasks are: (i) select and solve the stationary vacuum equations using the seventeen quartics and four masses; (ii) diagonalize the canonical scalar Hessian, gauge Gram and Weyl mass map there, identify Goldstones and a light-field projector; (iii) compute the heavy contributions to background gauge two-point functions and the relevant two-, three- and four-point scalar/Yukawa amplitudes, including finite MS decoupling terms and mass logarithms; (iv) specify whether the low-energy EFT retains one or both Φ doublets and which Δ remnants; (v) match the operator bases and evolve each EFT interval. A mere common threshold scale or a gauge representation list does not determine those finite coefficients or light-field rotations.

Full higher-loop running is executable algebra still outstanding, not missing experimental input: contract the canonical 68 scalar vertices, full quartic tensor, and gauge generators into the two-loop Yukawa tensor of equation (35) and scalar tensor of equation (44) in [Luo–Wang–Xiao](https://arxiv.org/pdf/hep-ph/0211440), with the semisimple substitutions and ordered Weyl indices retained. Then project onto Y,Z,F and all seventeen quartics, checking full tensor/polynomial identities. Dimensionful masses require the corresponding two-loop contractions. A complete fixed-point claim must solve these coupled equations, test scalar boundedness on the actual orbit space, evaluate the stability matrix, and quantify omitted-loop sensitivity.

## 6. Reproduction, attempts, and branch disposition

Run `python derive_and_check.py` with NumPy 2.3.5 and SymPy 1.14.0. All prior model and coefficient inputs needed for this check are copied under `support/`, with SHA-256 provenance; no original workspace path is required by the final script. `results.json` contains exact coefficient strings, all fifteen fixed-point faces, all component-check receipts and dependency hashes. The initial plain-Python attempt failed before calculation because SymPy was absent from its import path; it is retained with its source and stderr. The next completed pass verified the gauge-free cone, and the final completed pass added the full-gauge cone and independent candidate evaluations. No numerical counterexample or nonpositive face was deleted.

| Prior branch | New disposition | Retained boundary |
|---|---|---|
| S04 | Full one-loop retained; complete two-loop gauge sector added | Full two-loop Yukawa/scalar and physical trajectory/vacuum |
| S07 | Tree matching and explicit scalar branching derived | Vacuum, mass spectrum, finite decoupling and EFT choices |
| S11 | Full17 positivity cone permits arbitrary angular remainder | No claim of generic enhanced-symmetry preservation |
| S17 | Gauge beta completed through two loops, arbitrary n | Threshold-specific running remains model dependent |
| S20 | Constant 2/3 also fails as a formally protected leading alignment | Accidental finite-coupling cancellation and different models |
| S21 | gR excluded at all 2g/1Y zeros; explicit small-cube no-go; ten flavor-ansatz candidates catalogued | Full two-loop and scalar-compatible interacting fixed points |
| S22 | Explicit full one-loop positive invariant cone proved | Maximal positivity region and higher-loop persistence |

## 7. Additional proof details and scalar-Gram certificate

The kinetic metric has only diagonal entries 2 and 4, so G is strictly positive and the map u=G¹ᐟ²x is invertible on all 68 real directions. At a contact point, write H=A+P with A=κQ(8uuᵀ+4r²I) positive semidefinite and P=∇²W positive semidefinite. Then Tr(H²)−Tr(A²)=2Tr(AP)+Tr(P²)≥0 even when A and P do not commute. This justifies the Hessian-square comparison used above.

For q=0 but h>0, all Yukawas vanish, Q>0 and the same strict contact inequality applies. For Q=0, both the gauge and Yukawa zero subspaces are invariant; the retained scalar-only positivity result supplies the degenerate boundary. The invariant-cone statement is local-in-time and can be continued over every finite interval on which the polynomial ODE solution exists. It asserts neither global existence beyond a coupling divergence nor control of a nonperturbative regime.

A fourth retained verification pass makes the scalar-Gram bound explicit. Its Φ block has the form 4tI8+8[(Re s)KR+(Im s)KI], s=Tr(Z†Y), where KR and KI are real symmetric matrices with

\[
K_R^2=K_I^2=I_8,\qquad K_RK_I+K_IK_R=0.
\]

These matrices are recorded in `results.json`, and their identities are verified exactly. Squaring the traceless combination gives |s|²I8, establishing the asserted eigenvalue bound without diagonalizing a sampled matrix. All 253 polarized pairs of the two-family, 22-real-coordinate Yukawa space also reproduce the complete scalar-Gram form; the Δ block is fI60 and the mixed blocks vanish. This checks normalization independently of the gauge-trace Gram used in section 1.

## 8. Bounded two-loop Yukawa continuation for S18/S19

The entire pure degree-five Yukawa tensor has now been evaluated at

\[
g_a=0,\qquad \lambda_i=0,\qquad Z=F=0,\qquad Y=yI_n,\quad y\in\mathbb R.
\]

The result, with β=β(1)/L+β(2)/L², is

\[
\beta_Y^{(1)}=(2+4n)y^3I_n,\qquad
\boxed{\beta_Y^{(2)}=(1-24n)y^5I_n},\qquad
\beta_Z^{(2)}=\beta_F^{(2)}=0.
\]

For three families the new coefficient is −71. The seven pure-Yukawa contributions in the ordered tensor formula give, respectively,

\[
(2,\;0,\;-1,\;0,\;0,\;-12n,\;-12n)\,y^5I_n.
\]

Nontrace contractions are family-identity tensors. Each closed family trace contributes precisely n, so this is a symbolic all-n identity on this flavor slice; it is not extrapolated from a numerical fit. One route contracts the one-family gauge tensors with a symbolic family-trace multiplicity; a second reconstructs all actual 16n-dimensional Weyl matrices at n=1,2,3 and verifies every external tensor component. Raw scalar coordinates keep all entries and weights Gaussian dyadic; the complete tensor residuals vanish exactly in the tested arithmetic. Vanishing external Δ tensors make their contributions zero; full proportionality to the original Φ tensors also excludes a generated Z term here.

As an independent known-model regression, the same ordered contraction is applied to the Standard Model top Yukawa action built from a complex Higgs doublet and three colors. It reproduces β(1)=9y³/2 and β(2)=−12y⁵. The latter follows independently from the specialized matrix equation (6) of [Luo and Xiao, Two-loop Renormalization Group Equations in the Standard Model](https://arxiv.org/pdf/hep-ph/0207271): with only top Yukawa, zero gauge couplings and zero quartic, its terms reduce to 3/2−27/4−27/4=−12. This regression checks the Weyl multiplicity, scalar metric, and two-loop coefficient signs. All source conventions and seven contribution values are retained in `two_loop_yukawa_slice.py` and its result JSON.

On this pointwise slice, q=ny² has derivative

\[
\frac{dq}{d\log\mu}=\frac{2n(2+4n)y^4}{L}+\frac{2n(1-24n)y^6}{L^2}+\text{higher loops}.
\]

For n=3 this is 84y⁴/L−426y⁶/L². An isolated zero of this expression would occur at y²/L=14/71, but the scalar quartics have a nonzero fermion-box beta there. **The quartic-free slice is not an invariant full trajectory**, and this zero is not a simultaneous fixed point. No full two-loop Yukawa or scalar completion is claimed. This finite continuation explicitly begins the previously open higher-loop tensor work while retaining its remaining contractions.

## 9. Additional assigned branch dispositions

| Prior branch | New disposition | Remaining concrete gate |
|---|---|---|
| S18 | Complete prior one-loop Yukawa formulas retained; full pure degree-five two-loop sector derived on Y=yI_n,Z=F=g=λ=0 | General noncommuting Y,Z,F two-loop words; gauge-Yukawa, quartic-Yukawa and quartic-squared-Yukawa contractions; full tensor identities |
| S19 | Complete prior one-loop scalar Yukawa corrections retained and independently used in the cone contact reconstruction | Full two-loop seventeen-quartic projection and dimensionful-mass contractions; physical vacuum and matching still separate |
| S23 | Earlier current/CP boundary counterexamples and one-loop holomorphic Δ phase theorem retained; positive cone permits generated angular couplings | At higher loops explicitly compute Im[(λ11−iλ12)(βλ11+iβλ12)] and current/CP-coordinate sources with generic flavor spurions; no higher-loop phase theorem established |

There has been substantial bounded progress, not exhaustion of every executable higher-loop contraction or physical-selection branch.
