# Physical branches: exact bounds, non-identifiability, and one certified outgoing pole

This workstream continues F04, F05, N02, N03, N04, N06, N07, N08, N09 and M02 from the 11 September 2026 Yukawa certification catalog. It makes five mathematical advances, retains the earlier physical limitations, and does not choose parameters and relabel their agreement as a physical prediction. The old reports, checks and failed attempts remain unchanged.

The strongest new result for the overlap proposal is an explicit family of smooth local potentials with **the same complete confined spectrum and the same node labels but different overlap probabilities**. The strongest numerical certification is a unique complex outgoing benchmark pole enclosed in a disk of radius (10^{-30}) using interval arithmetic. New seesaw inequalities are exact for the stated full mass matrices, while the magnetic-moment bounds expose precisely which distribution assumptions matter.

## Branch dispositions

| Branch | New result | Remaining physical condition |
|---|---|---|
| F04 | Exact continuous positive-mass Koide family; sharp scale-sensitivity bound; conditional monotonic-flow theorem | A predictive mass matrix, its renormalization prescription and matching scale |
| F05 | Exact all-order lower bound on total active-heavy mixing; fixed physical mass spectrum with continuously variable mixing | Full mass texture, observed mixing constraints, channels, abundance history and a current likelihood |
| N02 | Exact partial-width conversion and branch-intensity exclusion thresholds for every frozen node branch | Evaluated channel energies, intensities and angular momenta; the new LNHB route did not return usable tables |
| N03 | Smooth local isospectral counterfamily changes overlap despite identical complete spectrum and nodes; nuisance-rank obstruction | A frozen microscopic or otherwise constrained preformation law and independent branch-aware validation |
| N04 | Exact correlated sensitivity formula and sharp partial-identification interval under explicit independence assumptions | Independently constrained potential/radius distribution and covariance |
| N06 | Rigorous unique-pole disk for the inherited rectangular-barrier outgoing benchmark, checked by independent ODE shooting | Physical potential/channel identification; separate validated enclosures for nuclear poles |
| N07 | Branch-aware feasibility theorem; zero-node exclusion needs only a specified lower bound on the corresponding branch fraction | Pauli-allowed state, physical potential, preformation and branch-resolved inputs |
| N08 | Exact conversion of all 16 frozen node configurations to admissible branch-fraction thresholds; complete-spectrum counterfamily shows nodes do not fix overlap | Physical Pauli/node prescription and channel choice |
| N09 | Explicit observationally equivalent compatible potential pairs and two-point minimax bounds; finite-grid sensitivity slopes | Independent potential constraints; no probability distribution is inferred from the grid |
| M02 | Same framed curve supports different magnetic moments; sharp positive-density support bounds; capacity changes within fixed topology | Charge/current/mass distributions, material and field dynamics, and a quantum spectral model |

## F04: what a Koide relation does and does not fix

For (m_i>0), let (x_i=sqrt{m_i}). The ratio (Q=sum x_i^2/(sum x_i)^2) lies between (1/3) and 1, with the upper endpoint approached if all masses must remain strictly positive. Fixing (Q=2/3), even after fixing an overall mass scale, leaves the continuous positive family

\[
 (x_1,x_2,x_3)\ \propto\
 \left(1,a,2(1+a)+\sqrt{3(a^2+4a+1)}\right),\qquad a>0.
\]

Direct symbolic substitution proves the identity; independently evaluated normalized masses change continuously in the runnable check. A Koide constraint alone therefore does not choose the observed three masses or a physical mixing angle. This supplements, without altering, the newer S20 result that excludes constant (2/3) Yukawa alignment in the declared model.

There is also an exact way to test scale sensitivity without assuming a numerical fit. Define (gamma_i=dlog m_i/dt), (p_i=m_i/sum m), and (q_i=sqrt{m_i}/sumsqrt m). Then

\[
 \frac{d\log Q}{dt}=\sum_i(p_i-q_i)\gamma_i,
 \qquad
 \left|\frac{d\log Q}{dt}\right|
 \leq\frac{\gamma_{\max}-\gamma_{\min}}2\sum_i|p_i-q_i|.
\]

The range bound is sharp: assign the maximum anomalous dimension to the positive components of (p-q), and the minimum to the negative components. Universal (gamma_i) is sufficient for invariance, but is not necessary; the displayed weighted scalar condition is the actual instantaneous criterion. Forty independent centered-difference checks verify the derivative and bound.

Under the additional, explicit hypothesis (gamma_i=A+B m_i^p), (p>0), the derivative has the sign of (B) for nondegenerate masses. After clearing positive denominators, the numerator is

\[
 B\sum_{i<j}x_i x_j(x_i-x_j)(x_i^{2p}-x_j^{2p}),
\]

which has that sign. This is a conditional theorem about a named beta-function form, **not** an assertion that the generic ACS Yukawa flow has that form. The check independently expands the (p=2) case exactly.

## F05: exact seesaw bounds and an isospectral mixing family

Consider a complex symmetric full mass matrix whose active-active block vanishes. Assume its unitary Takagi matrix has active rows ([A\ B]), with exactly (n_a) designated light columns and any number of heavy columns. Let (d=\mathrm{diag}(m_i)) and (D=\mathrm{diag}(M_I)) be the positive physical masses. The exact block-zero identity and unitarity give

\[
 A d A^T=-B D B^T,\qquad AA^\dagger=I-BB^\dagger.
\]

Put (t=\|B\|_F^2), (eta=\|B\|_2^2), (S=\sum_i m_i), and (M_{\max}=\max_I M_I). Nuclear-norm inequalities yield

\[
 (1-\eta)S\leq\sum_I M_I\|B_I\|^2\leq M_{\max}t,
 \qquad t\geq\frac{S}{M_{\max}+S}.
\]

For (eta<1), the first lower bound follows from the smallest singular value of (A); if (eta=1), it is trivial. For the second bound, (t\geq1) is already sufficient, and otherwise use (eta\leq t). These are exact full-matrix statements, not truncated seesaw formulas. They bound **total** active-heavy mixing; they do not give a positive lower bound for every individual heavy species in a general multifamily model.

This lower bound does not restore uniqueness. With one active state, fix physical masses ((m,M,M)). Take signed eigenvalues ((m,+M,-M)), where the negative sign is absorbed into a Majorana phase. Choose the active row of a real orthogonal matrix to have squared entries

\[
 \left(1-t,\frac{t-(m/M)(1-t)}2,\frac{t+(m/M)(1-t)}2\right),
 \quad\frac{m}{M+m}\leq t\leq1.
\]

Complete that row orthogonally and reconstruct the real symmetric mass matrix. Its active-active entry is exactly zero and its three singular masses stay fixed while total active-heavy mixing runs through the displayed interval. At the left endpoint it saturates the bound. Direct diagonalization and the independent polynomial light projector

\[
 P_{\rm light}=\frac{\mathcal M^2-M^2 I}{m^2-M^2}
\]

recover the same mixing in the checks. Thirty separately generated multi-active block-zero matrices also satisfy the exact bound.

For comparison, a complex-orthogonal boost preserves the leading effective coefficient (-\Theta D\Theta^T) while changing (|\Theta|_F^2). That construction is explicitly recorded as an effective low-energy calculation. Its large-mixing points are not presented as reliable truncated physical eigenvalues. Neither construction supplies a decay abundance or a current X-ray/cosmological likelihood.

## N03: a complete confined spectrum still does not identify overlap

On (0<x<\pi) with Dirichlet endpoints, start with (V=0) and normalized ground mode (u=\sqrt{2/\pi}\sin x). Define

\[
 I(x)=\int_0^x u^2=\frac{x-\tfrac12\sin2x}{\pi},\qquad
 V_t=-2\frac{d^2}{dx^2}\log(1+tI),\quad t>-1.
\]

Every (V_t) is a smooth local potential. The normalized ground state becomes

\[
 u_t=\frac{\sqrt{1+t}\,u}{1+tI}.
\]

For each other base eigenfunction (v), its transformed counterpart is

\[
 v_t=v-\frac{tu}{1+tI}\int_0^x uv.
\]

Differentiation verifies that these functions retain their original eigenvalues. The transformed functions satisfy both Dirichlet endpoints. The transformation is invertible: (I_t=(1+t)I/(1+tI)), and the parameter (-t/(1+t)) reverses it. Equivalently the bounded Volterra transformation is invertible on the finite interval. Thus no extra eigenvalues appear and the complete spectrum remains (n^2). The ordered Sturm node counts remain unchanged; in particular the ground state is strictly positive inside the interval.

Nevertheless, its squared overlap with the fixed original ground mode is exactly

\[
 P(t)=|\langle u,u_t\rangle|^2
   =(1+t)\left(\frac{\log(1+t)}t\right)^2,
 \qquad P(0)=1,\quad\lim_{t\to\infty}P(t)=0.
\]

Normalization and overlap are elementary integrals after the substitution (z=I(x)). The check proves the differential intertwining identity symbolically for a general pair of eigenvalues, verifies normalization and overlap by independent quadrature, and independently solves three deformed local potentials on two finite-difference meshes. The first five eigenvalues converge at second order to (n^2).

The obstruction also applies to every fixed normalized cluster trial in L2(0,pi): its scalar product with u_t tends to zero as t tends to infinity. Indeed, I_t(delta) tends to 1 for each delta>0, so normalized probability concentrates near the endpoint. Split the scalar product at delta, apply Cauchy–Schwarz, and first take t to infinity, then delta to zero. The check additionally evaluates a fixed reduced-radial Gaussian proportional to x exp[-x^2/(2 sigma^2)], with sigma=0.65, purely as an instrument demonstration. That scale is not selected as a nuclear parameter.

Rescale (x=\pi r/R) to obtain the same obstruction at any fixed confinement radius. This supplies an exact reason why even energy levels and node labels cannot uniquely specify an overlap proxy without eigenfunction/norming data or a microscopic state law. **It does not assert preservation of all outgoing scattering poles or nuclear observables.** The earlier retrospective overlap validation results retain their original scope.

An additional elementary obstruction concerns freely adjustable preformation. One independent (log P_i) intercept per isotope spans every observed log-width vector. Adding any fixed geometric feature then creates an exact design-matrix null direction. A successful width fit in that saturated model cannot establish the geometric feature's predictive contribution. A shared or otherwise constrained preformation law can instead be tested through frozen branch ratios or held-out widths.

## N02, N04, N07–N09: branch-aware feasibility and identifiable quantities

For a branch fraction (b_i) relative to **all** decays,

\[
 \Gamma_i=\frac{b_i\hbar\log2}{T_{\rm total}},\qquad
 T_{1/2,i}=\frac{T_{\rm total}}{b_i},\qquad
 P_i=\frac{b_i T_{{\rm sp},i}}{T_{\rm total}}.
\]

If (\beta_i) is instead conditional on alpha decay, use (b_i=f_\alpha\beta_i). In the prior provisional alpha-total comparison, (r=T_{\rm sp}/T_\alpha), so (P_i=\beta_i r). A given pole is compatible with (P_i\leq1) exactly when (\beta_i\leq\min(1,1/r)). The new check converts all 16 preserved node configurations and all 18 potential configurations to these thresholds.

For example, the zero-node 212Po and 214Po calculations require the corresponding within-alpha branch fractions to be at most **0.79010%** and **0.41202%**, respectively. Any independently established lower bound above those thresholds excludes those specific branches under (P\leq1). No branch fraction is assumed here. The physical statement remains conditional on the channel actually using that pole and its energy/angular momentum.

For multiple independent channels with (0\leq P_i\leq1), the attainable total width is exactly

\[
 0\leq\Gamma_{\rm total}\leq\sum_i\Gamma_{{\rm sp},i}.
\]

Necessity is immediate; sufficiency follows by choosing every (P_i=\Gamma_{\rm total}/\sum_i\Gamma_{{\rm sp},i}). If all branch fractions are supplied, feasibility is instead the collection (b_i\Gamma_{\rm total}\leq\Gamma_{{\rm sp},i}). Forty independent linear programs verify both characterizations. These statements assume channel factors are independently bounded; they do not silently impose a sum-to-one microscopic spectroscopic-factor rule. If a common (P) is imposed, the branch ratios must equal (\Gamma_{{\rm sp},i}/\sum_j\Gamma_{{\rm sp},j}), which supplies a shape test independent of the overall factor.

### A quantitative obstruction using the frozen potential grid

The earlier grid is copied without numerical modification. Each row fits its depth to the same isotope-specific (Q). Restricting to rows compatible with the provisional single-channel (P\leq1) gives:

| Isotope | Compatible grid rows | Compatible (P) range | Ratio of extreme compatible factors | Two-point minimax multiplicative factor |
|---|---:|---:|---:|---:|
| 212Po | 8 of 9 | 0.0712260–0.846764 | 11.8884 | 3.44796 |
| 214Po | 7 of 9 | 0.119073–0.905537 | 7.60488 | 2.75769 |

At each compatible row, choosing (P=\Gamma_{\rm obs}/\Gamma_{\rm sp}) gives exactly the same observed width; their (P\Gamma_{\rm sp}) products agree to the preserved numerical precision. Thus the data pair consisting only of that (Q) and width does not distinguish these potentials. For any estimator based only on these indistinguishable observations, the maximum absolute log-error at two such states is at least half their log-(P) separation. Exponentiating gives the final column. This is a conditional finite-family minimax theorem, **not an empirical uncertainty estimate** and not a claim that the chosen potentials are all physically realistic.

The fixed-(Q) grid's central secants for (log\Gamma_{\rm sp}) are 19.7748 and 20.3917 per fm in the radius coefficient, and 10.2897 and 10.3538 per fm in diffuseness, for 212Po and 214Po respectively. Independent least-squares and normal-equation reconstructions agree. These are finite-grid model sensitivities, not derivatives certified on a continuum or observational error bars.

### Exact uncertainty and fitted-energy identities

For independently attainable intervals (b\in[b_L,b_U]), (T\in[T_L,T_U]) and (g=\Gamma_{\rm sp}\in[g_L,g_U]), the sharp allowed preformation interval is

\[
 \left[\frac{b_L\kappa}{T_U g_U},
       \frac{b_U\kappa}{T_L g_L}\right]\cap[0,1],
 \qquad\kappa=\hbar\log2.
\]

For correlated inputs, these endpoint combinations need not be attainable. The exact differential is (d\log P=d\log b-d\log T-d\log\Gamma_{\rm sp}); its linearized variance uses the full covariance quadratic form with coefficient vector ((1,-1,-1)). Ignoring covariance is an additional assumption.

If a simple matching condition (F(Q,D,p)=0) fits depth (D) at fixed (Q), the implicit-function theorem gives

\[
 D_p=-F_p/F_D,\qquad
 \frac{d\log\Gamma}{dp}
 =\partial_p\log\Gamma-(\partial_D\log\Gamma)F_p/F_D.
\]

The condition (F_D\ne0) is essential. Fixing (Q) removes one degree of freedom; it does not set this remaining width sensitivity to zero. These identities specify the calculation needed when independent potential constraints and covariances become available.

## N06: a rigorous outgoing benchmark pole

The inherited controlled benchmark is the half-line equation (-u''+Vu=Eu), (u(0)=0), with (V=0) on ((0,1)), (V=20) on ((1,2)), and (V=0) beyond 2, in units (hbar^2/(2\mu)=1). The boundary at 2 is genuinely outgoing: (u'=i\sqrt E\,u).

Exact transfer through the two intervals gives an analytic determinant (D(E)). At the decimal center

\[
 E_0=6.4410375858632668291750820163897948
 -0.0022082370285796342710682308196514037\,i,
\]

Arb arithmetic at 180 bits proves that the disk (|E-E_0|<10^{-30}) contains exactly one zero. The proof compares (D) with the linear function (D'(E_0)(E-E_0)). On the whole enclosing complex box, interval jets bound half the second derivative. The verified Rouché inequality is

\[
 |D(E_0)|+r^2\sup|D''|/2
 < r|D'(E_0)|,
\]

with left side approximately (1.27648\times10^{-34}), right side (1.06499\times10^{-29}), and (r=10^{-30}). The width enclosure printed by Arb is

\[
 \Gamma\in[0.00441647405715926854213646164\ \pm\ 2.70\times10^{-30}].
\]

Independent adaptive complex ODE shooting, starting away from this center, agrees to the check's specified (2\times10^{-10}) energy tolerance. The numerical shooting comparison is corroboration; the interval inequality supplies the actual proof of enclosure and uniqueness.

This also establishes a concrete certification standard for future narrow nuclear poles. A tiny unnormalized residual alone is insufficient: (D_\epsilon(E)=\epsilon(E-2)) has residual (2\epsilon) at zero while its root remains distance 2 away. A validated root disk must be much narrower than half the resonance width before its imaginary part is relatively resolved. No such interval certificate is claimed here for the earlier Woods–Saxon/Coulomb nuclear widths.

## M02: fixed framing leaves magnetic moments and capacitance free

Under classical rigid rotation around (z), with one angular velocity and positive normalized charge and mass distributions,

\[
 \mu_z=\frac\omega2\int s^2\,dq,\quad
 L_z=\omega\int s^2\,dm,\quad
 g=\frac{2M\mu_z}{Q L_z}
   =\frac{\langle s^2\rangle_q}{\langle s^2\rangle_m}.
\]

Here (s) is cylindrical radius. Proportional mass and charge distributions give (g=1) for every embedding and framing. On the manuscript's same ((2,1)) centerline, give charge and mass the positive parameter densities ((1+c\cos t)/(2\pi)) and ((1+d\cos t)/(2\pi)), (|c|,|d|<1). Geometry and framing do not change, but

\[
 g(c,d)=\frac{R^2+a^2/2+Ra c}{R^2+a^2/2+Ra d}
\]

does. Exact integration and direct three-vector moment integrals independently verify the result. More generally, positivity and (R-a\leq s\leq R+a) give sharp bounds

\[
 \left(\frac{R-a}{R+a}\right)^2\leq g\leq
 \left(\frac{R+a}{R-a}\right)^2.
\]

Concentrating positive charge and mass densities near opposite extrema approaches either endpoint. Thus (g=2) within this specific common-rotation model requires (a/R\geq3-2\sqrt2\approx0.171573). Other velocities, signed charge distributions, spin fields or stresses change the hypotheses; framing alone does not supply any of them. This is a kinematic family, not a stable electron or QED model.

Electrostatic capacity also fails to be a topology invariant. For nested conductors (K_1\subset K_2), the Dirichlet energy principle gives (C(K_1)\leq C(K_2)); strictness for nested smooth conductors with positive separation follows from uniqueness and the maximum principle. Independently, the unit-charge energy principle gives the same monotonicity by enlargement of the allowed charge measures. The family of solid tubes (K_a=\{x:\mathrm{dist}(x,\mathrm{circle}_R)\leq a\}), (0<a<R), has fixed torus topology and can retain the same chosen centerline framing while its capacity increases strictly. It is a counterfamily to topology-only capacity selection, not an assertion that a solid tube equals the manuscript ribbon conductor.

Since these tubes contain a ball of radius (a) and lie in a ball of radius (R+a),

\[
 4\pi\epsilon_0 a\leq C(K_a)\leq4\pi\epsilon_0(R+a).
\]

The normalizing sphere formula is checked independently through surface potential and the integrated external field energy. If the charge is (f e), the stipulated self-energy equation and (R=\hbar/(2mc)) imply

\[
 \alpha^{-1}=\frac{4\pi\epsilon_0 f^2 R}{C}
            =\frac{4\pi f^2}{c(\mathrm{shape})},
 \quad C=\epsilon_0 R c(\mathrm{shape}).
\]

Uniform scaling cancels after imposing the Compton-radius input; the aspect ratio and charge split remain. In the manuscript annulus scheme this becomes

\[
 \alpha^{-1}=2f^2[\log(8R/a)+1],\qquad
 \log(a/R)=\log8+1-\alpha^{-1}/(2f^2).
\]

The inverse relation reconstructs arbitrary targets. It is a parameter fit unless (a/R) and (f) are independently selected. The check uses 137.036 only as the manuscript's existing target and does not claim an updated physical constant or a reliable BIE extrapolation at an extreme cutoff.

## Retrieval, verification and replay boundaries

The prior failed IAEA/NNDC endpoints were not retried. A newly identified primary route was the [LNHB nuclear-data portal](https://www.lnhb.fr/home/nuclear-data/), whose indexed description identifies the DDEP recommended-data program. Opening that page and its [recommended-data table](https://www.lnhb.fr/accueil/donnees-nucleaires/donnees-nucleaires-tableau/) both returned fetch timeouts. A targeted follow-up search did not produce a usable relevant primary table. No number from an unrelated result, secondary summary, or missing branch table was imported. `access_attempts.json` records this unsuccessful path. N02 remains open.

The two local nuclear input JSON files are byte-for-byte copies of the previously retained successful node/grid results, with provenance and SHA-256 hashes in `support/provenance.json`. The new sensitivity and identifiability calculations reuse their finite outputs; they do not claim an independent rerun of the expensive nuclear ODE sweeps. Separate exact proofs, linear programs, decimal conversions and least-squares formulations state precisely which inputs they share.

Run the five checks using Python with NumPy, SciPy, SymPy, mpmath and python-flint installed:

```text
python run_check.py flavor_boundaries
python run_check.py nuclear_identifiability
python run_check.py isospectral_overlap
python run_check.py outgoing_certificate
python run_check.py moment_capacitance
```

Every invocation creates a new attempt directory containing stdout, stderr, a JSON result and a hashed receipt, stores the exact check source by its SHA-256, and appends an event. The initial and expanded nuclear-identifiability runs are both retained. All executed mathematical checks passed; the failed external retrieval path remains explicitly recorded. None of the conditional mathematical results closes the full ACS physical-prediction problem.


## Appended adversarial-review clarification

The exact fixed-spectrum seesaw family and its polynomial light-state projector assume **0 < m < M**. This makes the light/heavy designation unambiguous and ensures the projector denominator m^2 - M^2 is nonzero. The checked examples already satisfy this condition.

The N03 saturated-intercept rank statement concerns **unrestricted log preformation intercepts**, or local variations around a solution whose preformation factors lie strictly inside 0 < P_i < 1. It is a local non-identifiability statement within that feasible interior. The physical upper bounds P_i <= 1 can restrict global fits; they do not permit an arbitrary observed width to be absorbed for every potential. The branch-capacity inequalities and feasible-potential restrictions elsewhere in this report remain in force.

This clarification was appended after adversarial review. The complete pre-append report is retained by its SHA-256 in review_snapshots, and all previously checked program sources are unchanged. The reviewer also independently confirmed the same benchmark disk using a hyperbolic transfer representation, an explicit first derivative, and a Cauchy bound on all higher terms; that review is corroboration using the same Arb arithmetic library.
