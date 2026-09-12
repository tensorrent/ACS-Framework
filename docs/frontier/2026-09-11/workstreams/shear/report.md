# M08/M10: a unique global tanh growth maximum and an independent continuum certificate

The unique global maximizer is now certified for the declared whole-line inviscid tanh Rayleigh model, conditional on the inherited analytic spectral premises listed below. Its location satisfies

\[
0.444918042172<k_*<0.444918042175.
\]

The global growth height satisfies the exact rational enclosure

\[
\frac{667454928885239561257347}{3518437208883200000000000}
<s_*<
\frac{5214491631915934072597903297569}{27487790694400000000000000000000}.
\]

For orientation, a slightly wider decimal enclosure is

\[
0.1897021004666724937969<s_*<0.18970210046667249380691.
\]

The second rigorous implementation independently proves the earlier global upper bound \(s_*<0.19\) with 93 gap-free rational cells. It uses a full-half-line Frobenius expansion and complex-parameter Cauchy bounds. The maximum-location proof uses a separately validated parameter-derivative extension of the earlier Taylor ODE integrator. These are distinct analytic/computational routes; both use Arb arithmetic and the same inherited spectrum/endpoint premises. Neither result is a physical vortex-knot claim.

## Scope and inherited premises

The dimensionless profile is \(U(y)=\tanh y\), with \(V=2\operatorname{sech}^2y\), \(K=-\partial_y^2+k^2\), and weighted state \(q/\sqrt V\in L^2(\mathbb R)\). The Rayleigh equation is

\[
\psi''-k^2\psi-\frac{U''}{U-c}\psi=0.
\]

The previous analytic argument supplies exactly one algebraically simple unstable phase speed \(c=i\eta(k)\), with \(\eta(k)>0\), for each \(0<k<1\). There are no unstable modes for \(k\ge1\). The unstable branch is analytic locally, continuous globally, and \(s(k)=k\eta(k)\) tends to zero at both endpoints. Thus a positive interior global maximum exists. The associated Jost determinant has precisely one simple zero for positive \(\eta\). The unchanged prior spectral discussion is retained in `support/inherited_spectral_premises.md`; this workstream does not claim a new independent proof of that entire spectral theorem or proof-assistant verification.

The endpoint bounds used here are analytic continuum inequalities. Howard's identity gives \(s(k)\le k\). The real Rayleigh energy identity and the Pöschl–Teller comparison give

\[
s(k)^2\le H(k):=\frac{2k}{1+k}-k^2.
\]

Indeed, the real potential depth is at most \(2\operatorname{sech}^2y/(1+\eta^2)\). The comparison ground energy is \(-a^2\), where \(a(a+1)=2/(1+\eta^2)\), so \(k\le a\) yields the stated inequality. On \(k\ge0.98\), \(H'(k)=2/(1+k)^2-2k<0\) and \(H(0.98)<0.1897^2\). These exact rational inequalities are checked in the certificate programs.

## Determinant and its sign

Normalize the left Jost solution by \(\psi=e^{ky}f\), with \(f\to1\) as \(y\to-\infty\), and write \(v=f'\). Then

\[
f'=v,\qquad v'=Wf-2kv,\qquad W=\frac{U''}{U-i\eta}.
\]

Reflection-conjugation matching at zero gives

\[
D(k,\eta)=k|f(0)|^2+\Re[v(0)\overline{f(0)}].
\]

This formulation divides by neither \(f\) nor \(\psi\). Its zeros are the unstable matching modes. Since \(D\to k>0\) as \(\eta\to\infty\), continuity and the inherited single-simple-zero property imply: \(D<0\) below the unstable zero and \(D>0\) above it. No unproved global monotonicity of \(D\) in \(\eta\) or growth is used.

All curvature derivatives below are derivatives of

\[
\mathcal D(k,s):=D(k,s/k)
\]

with **growth \(s\) held fixed**. They are not derivatives at fixed phase speed.

## Proof of a unique global maximizer

Let \(L=0.1897\), \(S=0.19\), and \(I=[0.4,0.5]\).

1. An independent Frobenius sign calculation at \(k=89/200\) gives \(\mathcal D(k,L)<0\), hence the global maximum is strictly above \(L\).
2. There are 132 accepted rational ODE cells covering \([L,0.4]\cup[0.5,0.98]\), with \(\mathcal D(k,L)>0\) on every cell. Together with the endpoint inequalities, every point with growth at least \(L\), and therefore every global maximizer, lies strictly inside \(I\).
3. Fifty width-0.002 rational cells cover \(I\). On each cell the entire growth interval \([L,S]\) is included. The validated derivative system proves \(\mathcal D_{kk}>0\) on this rectangle. A common outward lower bound from the detailed archived balls is \(1.0810159007742356\). The looser rational bound \(\mu=0.18\) is also retained for refinement.
4. Strong convexity gives, for any fixed \(s\in[L,S]\),
   \[
   \mathcal D(k,s)\ge\mathcal D(k_0,s)+\mathcal D_k(k_0,s)(k-k_0)+\tfrac\mu2(k-k_0)^2
   \ge\mathcal D(k_0,s)-\frac{|\mathcal D_k(k_0,s)|^2}{2\mu}.
   \]
   At \(k_0=0.445,s=S\), the right side is positive. Using the tighter recorded curvature lower bound, it exceeds \(0.00029349701531208962395\). Therefore growth is below \(S\) throughout \(I\), and the exterior is already below \(L<S\). This establishes the global upper bound without assuming it beforehand.
5. Suppose two distinct global maximizers existed. They would lie in the interior of \(I\), have the same growth \(s_*\in(L,S)\), and satisfy \(\mathcal D(k_1,s_*)=\mathcal D(k_2,s_*)=0\). Strict convexity in \(k\) forces \(\mathcal D(k,s_*)<0\) between them. The determinant sign rule then gives \(s(k)>s_*\), a contradiction. Hence the global maximizer is unique.

This proves uniqueness of the **global** maximum. It does not assert that every stationary point below growth 0.1897 has been excluded or that the entire branch is globally concave or unimodal.

## Location and height refinement

At the exact rational \(k_0=0.4449180422\), Frobenius bisection encloses its true growth root to width below \(10^{-25}\). The lower endpoint in the displayed global-height enclosure is that fixed-point lower bound. The upper endpoint is the fixed-point upper bound plus \(10^{-20}\).

At this proposed upper growth, the independently enclosed determinant is

\[
\mathcal D(k_0,s_U)=[9.8531169119672\times10^{-21}\ \pm4.41\times10^{-35}],
\]

and the validated fixed-growth derivative is \([3.90\times10^{-11}\ \pm3.16\times10^{-14}]\). The strong-convexity lower bound with \(\mu=0.18\) remains strictly positive, with margin at least \(5.62127093847895\times10^{-21}\). Thus the proposed upper endpoint bounds the **global** growth, rather than just the growth at \(k_0\).

For the entire refined growth interval, the endpoint derivative boxes are

\[
\mathcal D_k(0.444918042172,s)=[-1.8\times10^{-12}\ \pm4.30\times10^{-14}]<0,
\]
\[
\mathcal D_k(0.444918042175,s)=[2.6\times10^{-12}\ \pm1.32\times10^{-14}]>0.
\]

At the interior global maximum, differentiation of \(\mathcal D(k,s(k))=0\) gives \(\mathcal D_k=0\). Since \(\mathcal D_k\) strictly increases with \(k\) on the certified rectangle, these endpoint signs force the maximizing wavenumber into the stated strict interval. No optimizer tolerance or sampled sign scan enters this proof.

## Validated derivative route

At fixed growth, write \(W(k,s)=U''k/(kU-is)\). Its first two normalized parameter coefficients are

\[
W_0=\frac{U''k}{kU-is},\qquad
W_1=\frac{-isU''}{(kU-is)^2},\qquad
W_2=\frac{isUU''}{(kU-is)^3}.
\]

The six-component triangular system consists of \((f_p,v_p)\), \(p=0,1,2\), where coefficients are normalized by \(1/p!\):

\[
f_p'=v_p,\qquad
v_p'=\sum_{q=0}^pW_qf_{p-q}-2kv_p-2v_{p-1},\quad v_{-1}=0.
\]

The order-16 real Taylor integral remainder is bounded by whole-step interval jets of this complete system. The infinity-norm Gronwall constant uses the upper endpoint of \(\max(1,\sum_q|W_q|+2|k|+2)\). The final code explicitly takes outward upper endpoints before comparing bound balls. Fundamental-matrix parameter coefficients are convolved with the solution coefficients.

The infinite left tail is enclosed using a complex \(k\)-disk of radius \(r=0.05\). With \(k_\ell=\inf k-r>0\), \(k_u=\sup k+r\),

\[
\Re(s/k)\ge\eta_{\min}:=s_{\min}k_\ell/(k_u^2+r^2)>0.
\]

Thus \(A_T=4e^{-2T}/\eta_{\min}\) bounds the integral of \(|W|\) on the tail. The Volterra kernel is bounded by \(1/(2k_\ell)\), yielding \(|f(-T)-1|\le e^{A_T/(2k_\ell)}-1\) and \(|v(-T)|\le A_Te^{A_T/(2k_\ell)}\). Cauchy's formula divides these errors by \(r^p\) for normalized derivative coefficients. Curvature uses \(T=18,h=0.025\); refinement uses \(T=24,h=0.02\). All cutoff, rounding, parameter, and Taylor errors are included.

This route extends the previous integrator architecture. It is not labeled an independent spatial implementation.

## Independent full-half-line Frobenius route

Set \(t=1+\tanh y\), so the entire left half-line maps to \(0<t\le1\), and set \(A=1+i\eta\). The rescaled Jost solution obeys the exact polynomial-coefficient equation

\[
t(2-t)(t-A)f_{tt}+2(1+k-t)(t-A)f_t+2(t-1)f=0.
\]

For \(f(t)=\sum_{n\ge0}b_nt^n\), \(b_0=1,b_{-1}=0\), the recurrence is

\[
b_{n+1}=\frac{((A+2)n^2+(A+2k)n-2)b_n+(-n^2+n+2)b_{n-1}}
{2A(n+1)(n+1+k)}.
\]

At \(y=0\), \(t=1\) and \(dt/dy=1\), so \(f(0)=\sum b_n\), \(v(0)=\sum n b_n\). There is no finite spatial cutoff.

For a rigorous infinite tail, diagonalize the limiting recurrence matrix using

\[
\lambda=1/A,\quad g=\lambda-1/2,\quad P=\begin{pmatrix}\lambda&1/2\\1&1\end{pmatrix}.
\]

In the transformed state, the exact transfer matrix is

\[
M_n=\begin{pmatrix}\lambda+e_1&e_2\\-e_1&1/2-e_2\end{pmatrix},
\]

\[
e_1=-\frac2{A(n+1+k)}-\frac{k\lambda}{A(n+1)(n+1+k)g},\qquad
e_2=\frac{1+k}{2(n+1+k)}-\frac{k}{2A(n+1)(n+1+k)g}.
\]

For complex parameter boxes, let \(a=\inf|A|>1\), \(g_0=\inf|g|>0\), \(\ell=\inf\Re k>0\), \(L_\lambda=\sup|\lambda|\). For every \(n\ge N\), the perturbation row sum is at most

\[
\epsilon_N=\frac{2/a+\sup|1+k|/2}{N+1+\ell}
+\frac{\sup|k|(L_\lambda+1/2)}{a g_0(N+1)(N+1+\ell)}.
\]

The final API uses \(\rho=\max(L_\lambda,1/2)+\epsilon_N<1\). If \(T_N\) bounds the transformed state's infinity norm, then \(|b_{N+j}|\le C\rho^j\), \(C=(L_\lambda+1/2)T_N\), and

\[
\left|\sum_{n>N}b_n\right|\le\frac{C\rho}{1-\rho},\qquad
\left|\sum_{n>N}nb_n\right|\le C\left(\frac{N\rho}{1-\rho}+\frac{\rho}{(1-\rho)^2}\right).
\]

Disk-error propagation recenters complex state coefficients and propagates their Euclidean error radii, avoiding exponential rectangular wrapping. The final generalized contraction covers both limiting eigenvalues. Earlier versions omitted the maximum with 1/2; their accepted calls are separately checked to lie in \(|\lambda|>1/2\), while the final API removes this restriction.

To cover a real parameter interval \(k=c+x\), \(|x|\le h\), a larger complex disk of radius \(R>h\) bounds the full solution and spatial tail. The center coefficients are computed through degree 16 with 4096-bit ball arithmetic. For the analytic extension

\[
\mathscr D(k)=kf(k)f^\#(k)+\tfrac12\bigl(v(k)f^\#(k)+v^\#(k)f(k)\bigr),\quad f^\#(k)=\overline{f(\bar k)},
\]

suppose \(M_D\) bounds the entire function on the disk and \(E_D\) bounds the omitted spatial tail there. Cauchy gives the total interval-evaluation error

\[
\frac{E_D}{1-h/R}+M_D\frac{(h/R)^{17}}{1-h/R}.
\]

The determinant series is formed before real interval evaluation so that its cancellations are retained. The 93 final cells cover \([0.19,0.98]\) without gaps. Every saved final determinant reparses strictly positive. Howard and the comparison inequality exclude the remaining wavenumbers.

## Independent checks and corrective audit

Five symbolic checks verify the transformed ODE, scalar recurrence, exact diagonalization for symbolic \(n\), and first/second fixed-growth potential derivatives. Six rigorous point comparisons between Frobenius and Taylor ODE enclosures overlap, including both lower-bound signs and the high-wavenumber end. These supplement the two continuum routes.

The inherited 557-cell archive has a real evidence-format weakness. Only 27 default displayed determinant strings still certify positivity after parsing; the other 530 strings contain zero after decimal display widening. This does **not** refute their original live positivity assertions or the theorem. The original executable checked live balls, but its saved default strings alone cannot recover every sign. This workstream does not describe all 557 original cells as having been freshly replayed individually. It independently recomputes a complete replacement continuum cover and also audits the original cover's rational continuity and supporting formulas.

Even `str(more=True)` retains only a few significant digits of the displayed radius, so detailed midpoint printing alone is insufficient near a sign boundary. Final evidence uses either explicit outward endpoints or the exact integer triple from `mid_rad_10exp(60)`, rendered as `[MID e EXP +/- RAD e EXP]`. The separate serialized-records gate reconstructs all 132 exterior and 50 curvature balls from their outward endpoints and proves that every normalized saved ball reparses strictly positive. The final independent 93-cell cover applies the same roundtrip test directly.

## Preserved failures and their valid boundaries

| Attempt | Observed limitation | Resolution or remaining boundary |
|---|---|---|
| First scalar Frobenius interval propagation | Complex rectangle rotations inflate tiny errors to enormous balls. | Disk-error propagation gives rigorous point and complex-disk enclosures. |
| First parameter-interval Frobenius probe | Direct wide parameter boxes lose useful cancellation. | Centered parameter series plus Cauchy bounds. |
| First curvature probe, step 0.05 | Second-derivative remainder is too wide; no positive curvature result. | Step 0.025 closes all 50 boxes; refinement uses 0.02. |
| First centered Frobenius model | Multiplying separately evaluated solution intervals loses determinant cancellation. | Form the analytic determinant series before evaluating it. |
| Default Arb string audit | Live positive balls can be displayed as intervals containing zero. | Explicit endpoints and full-precision midpoint/radius integer serialization; roundtrip gates. |
| Generic contraction API | `rho=abs(lambda)+epsilon` omits the other eigenvalue when abs(lambda)<1/2. | Final API uses the maximum; every earlier accepted point/disk is independently inside the valid restricted domain. |
| Fixed-radius raw continuum cover | Near k=0.215, repeated k subdivision cannot reduce a fixed complex-disk spatial-tail error floor. 361 raw cells, including all inconclusive descendants, are preserved. | Stopped with receipt; use smaller complex radii near the low endpoint and a fresh complete error. Final cover closes with 93 cells. |

Inconclusive boxes are neither counterexamples nor evidence of a second maximizer. Every attempted source, support snapshot, stdout/stderr, result and receipt is retained. The superseded probes are excluded from the accepted replay list.

## Dispositions and reproducibility

M08, interpreted as a unique **global** maximizing location in the stated model, is closed conditionally on the inherited spectral premises. M10's missing second rigorous continuum implementation is closed with the independent Frobenius/Cauchy certificate. The first certificate's archival serialization weakness is documented and corrected by replacement evidence. A completely independent proof of the inherited spectral theorem, proof-assistant verification, global exclusion of every smaller local extremum, and nonlinear/viscous/three-dimensional or physical knot interpretations are not claimed.

The only runtime dependencies are python-flint 0.9.0 and SymPy 1.14.0. Mathematical inputs needed for portable replay are copied under `support/`; no earlier workspace directory is required. Run accepted checks through `checks/run_receipt.py`, which creates a fresh append-only attempt with source/support snapshots and hashes. `replay_commands.json` is the authoritative final accepted program list. Exploratory and failed programs remain available as evidence, not acceptance gates.


## Final fresh replay and independent review

The standalone `independent_full_replay.py` completed successfully in 223.159 seconds. It recomputed all 93 final cells from only the rational grid and radii, using the final hardened Frobenius/Cauchy implementation. No old determinant, Taylor coefficient, ODE solution or Cauchy bound was reused. All93 saved balls reparsed strictly positive. Its receipt is `attempts/independent_full_replay_20260911T223610315992Z/receipt.json`. The five commands in `replay_commands.json` all have accepted zero-exit receipts.

The arithmetic workstream independently reviewed the mathematical scope and parsed the final evidence:93 Frobenius cells,182 normalized records,132 exterior positive endpoints,50 curvature boxes, exact endpoint comparisons and refined peak bounds. Its bounded review found no remaining defect within the inspected scope; it does not replace the declared analytic premises. See `../arithmetic/review.md`.
