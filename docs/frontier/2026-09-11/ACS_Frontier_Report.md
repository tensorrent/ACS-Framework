# ACS: open-branch continuation

Research and verification cut-off: 11 September 2026.

Six specialist agents and a coordinating audit worked through a **50-task checklist**: all 36 previously unresolved-status branches, nine further continuations of established results, and five new Navier-Stokes tasks. The previous 105-branch catalog and 256-event history are retained. The work adds proofs, counterexamples, numerical certificates, source corrections, and precise remaining obligations. It does not claim that every open mathematical possibility has been exhausted.

The strongest advances are a unique-maximum certificate for the specified tanh shear model; a positive invariant region for the full one-loop minimal Pati-Salam system; exact restrictions on its two-loop-gauge fixed points; conditional prime-operator asymptotics; trace-class infinite-operator observables; and explicit non-identifiability results for physical inference. The foundations audit tests the actual available definitions and checker. The Navier-Stokes work adds current primary research, exact counterexamples to insufficient regularity arguments, and a nonlinear ideal-MHD energy estimate.

Every result remains attached to its model, hypotheses and verification routes. A failed implication is a mapped path. An unavailable input remains an unavailable input. An unfinished calculation is listed as unfinished computation. No new Lean kernel pass, general RH proof, physical vacuum selection, or general unforced Navier-Stokes theorem is claimed.

## 1. What the checklist now means

`ACS_Frontier_Checklist.md` gives every task a current disposition, evidence, and next admissible step. `Task_Checklist.json` supplies the same information in machine-readable form. A completed investigation is distinguished from a solved parent research program. The seven detailed workstream reports contain the derivations and source-level references; their programs, source snapshots, successful checks and rejected attempts are included in the evidence archive.

| Workstream | Main advance | Remaining boundary |
|---|---|---|
| Shear spectrum | Unique maximum and tight validated height/location bounds | Inherited spectral theorem assumptions; nonlinear evolution and different profiles |
| Renormalization group | Full two-loop gauge sector; full one-loop positivity region; fixed-point restrictions | Full higher-loop system, scalar-compatible interacting zeros, vacuum and thresholds |
| Arithmetic and operators | Uniform norm bounds, conditional spectral law, trace-class subtraction and tails | Unconditional prime errors, joint limits, natural spectral identification |
| Physical inference | Certified model resonance, isospectral obstructions, exact seesaw bounds | Independently constrained potential, channels, mass dynamics and production inputs |
| Foundations and constraints | Source-defined counterexamples, exact replay instrument, actual checker defects | Intended stochastic law, production implementation, external proof, working kernel |
| Navier-Stokes | Current frontier taxonomy, energy/regularity gap, nonlinear MHD estimate | Exact Croft citation, critical-norm bridge, independent full proof verification |
| Projection and integration | Exact all-cutoff Jacobi defect; pinned formalization contract audit | The intended ACS projection and continuum estimates |

Two methods are required where the statement admits them. Exact algebra is checked against a separately assembled representation; differential identities against Fourier evaluation; interval roots against a distinct construction; inference obstructions against explicit alternative models. Shared assumptions are recorded. Re-running one algorithm is reproducibility evidence, not an independent derivation.

The release preserves three particularly important distinctions. The earlier generic Jacobian/BCH counterexamples do not invalidate a restricted ACS model without matching its hypotheses. A finite Fourier projection can fail Jacobi while still yielding a useful energy-stable numerical method. Finally, a checker defect says something about that checker, not about the truth of an unavailable external proof.

## 2. Shear: a formerly open maximum is now certified

The retained model is the inviscid, weighted whole-line Rayleigh problem for the tanh shear profile. Its spectral reduction gives one simple unstable pair for wavenumbers between zero and one. The previous release bounded the global growth height but left uniqueness of the maximizing wavenumber open.

The continuation proves uniqueness conditional on that inherited spectral theorem and its analytic endpoint estimates. It encloses the maximizing wavenumber by

\[
0.444918042172<k_*<0.444918042175.
\]

The growth height lies near 0.18970210046667249380; exact rational endpoints and the final validated intervals are retained in the shear evidence. These digits describe this normalized linear model. They are not universal plasma constants or a nonlinear stability estimate.

The new route compactifies the coordinate using \(z=(1+\tanh y)/2\) and constructs the Jost solution by a Frobenius recurrence. It avoids the spatial cutoff and differential-equation integration used in the earlier certificate. Parameter series and explicit remainder bounds support interval evaluation. An independent derivative calculation controls the Evans determinant along curves of fixed growth.

The uniqueness argument has a concrete shape. First, exterior bounds confine any global maximizer to the interior wavenumber interval. Second, the determinant is strictly convex in wavenumber at a fixed candidate growth height throughout that interval. If two different wavenumbers achieved the same largest height, strict convexity would force a negative determinant between them. The spectral sign rule would then imply a still larger growth rate, contradicting maximality. Derivative signs and root brackets sharpen the location.

The intervals, accepted cover cells, mathematical signs, and parameter derivatives are preserved in `workstreams/shear`. Exploratory failures from interval wrapping and later enclosure hardening remain alongside the final accepted checks. A narrow floating-point peak was not treated as a proof of global uniqueness.

Adversarial review exposed an archival limitation: default Arb display strings could enlarge a positive computed ball enough that the saved string no longer certified its sign. This does not establish that the live inequality was false. It means those display strings alone were insufficient evidence. The final independent Frobenius certificate covers the remaining compact interval with 93 rational cells whose full-precision balls reparse strictly positive. Separate outward-endpoint audits pass all 132 exterior cells and 50 curvature cells. Old records and corrective appendices remain visible.

M04/M07/M08/M10 consequently advance substantially within their declared linear problem. Changes of profile, carrier space, magnetic physics, viscosity or nonlinear dynamics are separate branches. The work does not infer nonlinear vortex-knot persistence from a bounded linear growth curve.

## 3. RG: a positive region with gauge and Yukawa interactions

Use the previously declared minimal unbroken Pati-Salam action, three chiral families, all 68 canonical real scalar coordinates, all seventeen real quartics, general complex Y,Z, and symmetric F. Let

\[
q=\operatorname{Tr}(Y^\dagger Y+Z^\dagger Z+F^\dagger F),\qquad
h=g_4^2+g_L^2+g_R^2,\qquad Q=q+h.
\]

In canonical scalar coordinates u, the closed region

\[
V_4(u)\ge\frac{Q}{2}(u^Tu)^2,\qquad u\in\mathbb R^{68},
\]

is forward invariant under the **full one-loop** scalar, Yukawa and gauge equations, for as long as the truncated solution exists. It is a region with the natural weighted scaling of gauge/Yukawa versus quartic couplings. It is sufficient, conservative, and nonempty arbitrarily near the origin.

The proof works on the full quartic, not on an assumption that radial symmetry remains preserved. Write \(\mathcal B=32\pi^2d/d\log\mu\). At a contact point of \(W=V_4-\kappa Qr^4\), nonnegativity makes the Hessian of W positive semidefinite and its gradient zero. In 68 dimensions,

\[
\operatorname{Tr}(\nabla^2V_4)^2\ge1216\kappa^2Q^2r^4.
\]

The fermion box is bounded below by \(-128q^2r^4\); the gauge wave term by \(-108\kappa Qhr^4\); the Yukawa wave and gauge-vector mass terms are nonnegative at contact.

The norm equations give \(\mathcal BQ\le40Q^2\), and therefore

\[
\mathcal BW\ge(1216\kappa^2-148\kappa-128)Q^2r^4.
\]

At \(\kappa=1/2\), the coefficient is 102, strictly positive when Q and r are nonzero. Compactness of the unit sphere rules out an outward first crossing. The Q=0 boundary reduces to the retained scalar positivity theorem. The detailed proof explains each normalization and inequality.

An independent component calculation rebuilds the scalar Hessian, fermion mass map, Yukawa Gram and 21-dimensional gauge-vector mass Gram. It agrees with the assembled seventeen-quartic evaluator. Exact polynomial checks identify the radial boundary potential across all 11,093 field monomials. These checks support the normalization; the continuum claim comes from the contact proof. A separate agent adversarially reviewed the constants and boundary argument.

The earlier negative fermion-box example remains valid outside this region. The new theorem supplies the missing restricted positive region; it does not make unrestricted Yukawa positivity automatic or establish two-loop positivity.

## 4. Higher-loop running and the remaining fixed-point problem

For \(L=16\pi^2\), the completed two-loop gauge sector is

\[
\beta_{g_a}=-\frac{g_a^3}{L}b_a+\frac{g_a^3}{L^2}\left(\sum_bB_{ab}g_b^2-D_a\right).
\]

At three families, \(b=(23/3,3,-11/3)\). In the order (4,L,R), the coefficient matrix is:

| Row | Column 4 | Column L | Column R |
|---|---:|---:|---:|
| 4 | 643/6 | 9/2 | 153/2 |
| L | 45/2 | 8 | 3 |
| R | 765/2 | 3 | 584/3 |

With \(t=\operatorname{Tr}(Y^\dagger Y+Z^\dagger Z)\) and \(f=\operatorname{Tr}(F^\dagger F)\), the Yukawa subtractions are \(D=(4t+15f/2,4t,4t+15f)\). Representation sums, explicit normalized generators, component weights, and Weyl-vertex traces agree. The gauge matrix also agrees with independent published calculations. The general formula is from [Luo, Wang and Xiao](https://arxiv.org/pdf/hep-ph/0211440); external coefficient comparisons are [Chakrabortty and Raychaudhuri](https://arxiv.org/pdf/0909.3905) and [the SO(10) unification calculation](https://link.aps.org/accepted/10.1103/PhysRevD.91.095010).

This permits a stronger but carefully truncated fixed-point result. At simultaneous one-loop Yukawa zeros, positive norm identities bound t and f. Substituting those bounds into the two-loop R-gauge equation leaves a strictly positive bracket. Thus **every three-family two-loop-gauge/one-loop-Yukawa fixed point has gR=0**. In the explicit cube

\[
\max_a\frac{g_a^2}{16\pi^2}<\frac{23}{335},
\]

the corresponding dimensionless gauge/Yukawa/scalar truncation has only the Gaussian fixed point. This is neither an all-orders statement nor a definition of perturbative validity.

Outside that cube, ten exact gauge/Yukawa candidate faces survive in a specified identity-matrix flavor ansatz; five nonpositive faces are recorded as rejected. The candidates still need compatible scalar zeros, boundedness, stability and omitted-loop analysis. Calling them complete physical fixed points would skip essential work.

The fixed ratio Z=(2/3)Y also fails as a protected leading relation in formal perturbation theory: its nonzero cubic-order defect cannot be canceled identically by fifth-order corrections. Accidental cancellation at particular finite couplings remains a different question.

One further higher-loop branch was worked explicitly. At the pointwise slice Y=yI_n with Z, F, gauge couplings and quartics zero, the complete pure-Yukawa degree-five tensor gives

\[
\beta_Y^{(2)}=(1-24n)y^5I_n.
\]

At three families its coefficient is -71. Symbolic family-trace multiplicities and full Weyl matrices agree; the same contraction independently reproduces the Standard Model top-only coefficient -12 from [Luo and Xiao's equation (6)](https://arxiv.org/pdf/hep-ph/0207271). This slice generates quartic running, so its isolated Yukawa zero is not a full fixed point.

Tree-level broken-phase matching and component branching are now explicit. Finite decoupling coefficients still require a selected vacuum, canonical masses, Goldstones, light-field projector and effective-theory content. General two-loop Yukawa, quartic and mass contractions remain a named computation. Physical trajectory and vacuum selection require actual boundary conditions; neither can be chosen by numerical convenience.

## 5. Prime operators: conditional laws and sharp obstructions

The manuscript's transition matrix has states (a,b) and maps (a,b) to (b,c). Conditional frequencies determine \(P=T-T_0\). Grouping input and output indices separately turns P into blocks \(B_b[c,a]\) for singular-value purposes. This is not an eigenvalue similarity transformation. It gives exact block-rank and norm identities.

If positive triple counts satisfy \(C(a,b,c)=A(1+\epsilon_{abc})\), with \(\max|\epsilon_{abc}|=\delta<1\) and k residue classes, then

\[
\|P\|_{\rm op}\le\frac{\delta}{\sqrt{1-\delta^2}},\qquad
\|P\|_{S_2}\le\frac{\sqrt{k}\delta}{\sqrt{1-\delta^2}},
\]

\[
\|P\|_{S_1}\le\frac{k\sqrt{k-1}\delta}{\sqrt{1-\delta^2}}.
\]

These are uniform in dimension. Operator, Hilbert-Schmidt and trace-norm convergence to zero therefore require different sufficient discrepancy rates. The rates are sharp in order under the stated structural assumptions. Balanced rational Hadamard constructions realize full allowable rank and near-quadratic eigenvalue participation while defeating stronger convergence claims. Euler circuits realize their integer counts as cyclic residue words. They are explicitly **surrogate sequences, not primes**.

A constructive arithmetic prediction is now available under a named conjecture. For a fixed modulus with k reduced residue classes, the triple form of the [Lemke Oliver-Soundararajan Main Conjecture](https://arxiv.org/html/1603.03720v4) implies, with \(h=\log\log x/\log x\),

\[
P/h\longrightarrow L_k,\qquad
(L_k)_{(b,c),(a,b)}=\frac1{2k}-\frac12\mathbf1_{b=c}.
\]

The conditional-frequency quotient cancels the first adjacent-equality bias. A separate factorization of the resulting operator gives nonzero eigenvalues -1/2, repeated k-1 times. Thus the spectral radius divided by h tends to 1/2, and the manuscript's eigenvalue participation rank tends to k-1. This fixed-modulus implication does not justify exchanging the prime-prefix and modulus limits.

Fresh counts through two million were checked at three prefixes and six moduli. Exact denominator-cleared block ranks certify maximal algebraic rank for all eighteen recorded matrices. Their spectral ratios and participation values are still far from the asymptotic predictions. They are retained as finite observations, not evidence sufficient to prove the conjecture.

The unproved arithmetic remainder, universal compression law, and joint-limit spectral law remain open. The initial one-sided Hadamard construction failed the required flow balance; its failure and corrected double-centering construction are preserved.

## 6. Infinite operators: a valid trace and its identification limit

For the explicitly constructed diagonal operator H with eigenvalues equal to the paired positive and negative zeta ordinates, the unpaired resolvent remains non-trace-class. The specified subtraction

\[
A(z)=(H-zI)^{-1}-H^{-1}
\]

is trace class away from the spectrum. Two Hilbert-Schmidt factors prove this; direct absolute summation is an independent route. Its trace is the previously paired scalar observable

\[
\operatorname{Tr}A(z)=\sum_{\gamma>0}\frac{2z}{\gamma^2-z^2}.
\]

The retained explicit inverse-square ordinate-tail estimate now yields trace-norm bounds for A, all its derivatives, and relative errors of the canonical product \(D(z)=\prod_{\gamma>0}(1-z^2/\gamma^2)\). The product identity \(-D'/D=\operatorname{Tr}A\) supplies another analytic check. An integer-spectrum instrument verifies the formulas against sine and cotangent closed forms. The external counting premise is [Bellotti and Wong's explicit zero-count estimate](https://arxiv.org/html/2412.15470v2).

This repaired observable does not identify H with a natural arithmetic operator. The information loss is exact: a doubled pair of central zeros and a reflected off-line quartet can have identical ordinate multisets while their full complex-coordinate products differ. Every ordinate-only construction above is blind to that difference. The example is an abstract symmetry-compatible multiset, not a proposed alternative zeta zero set.

R04's unconditional prime-error bound, the natural-operator branch of R06, and the required real-part spectral identification remain open. Better tail control cannot substitute for those missing statements. This distinguishes a useful analytic continuation from an unsupported RH conclusion.

## 7. Physical branches: what the observables can identify

The resonance instrument now has a rigorous complex-root enclosure for its specified outgoing rectangular barrier. The enclosed energy is approximately

\[
E=6.44103758586326682918-0.00220823702857963427i.
\]

An Arb/Rouche certificate isolates a unique zero in the declared small disk, and a separately integrated outgoing ODE checks the resonance condition. This certifies the model pole. It does not assign a physical isotope, potential, Pauli prescription or branching channel without the corresponding inputs.

A new exact local-potential family shows why spectra alone need not determine overlaps. On the finite Dirichlet interval, an explicit smooth isospectral deformation retains all eigenvalues \(n^2\) and node labels while its overlap with the original ground state is

\[
P(t)=(1+t)\left[\frac{\log(1+t)}{t}\right]^2.
\]

For positive t it ranges from a limit of one toward zero. Symbolic intertwining, exact normalization, independent quadrature and two-mesh spectral calculations agree. This is an exact confined-potential obstruction; it is not a claim that outgoing nuclear poles share that isospectral family.

In the frozen nuclear model grid, different compatible potentials can reproduce the same decay observations after preformation compensation. The corresponding preformation ratios exceed 11 for one retained isotope and 7 for another. These yield explicit two-point inference limits within the declared candidate set. A model grid is not a probability distribution or a calibrated uncertainty interval.

The flavor work likewise separates constraints from selection. An exact seesaw relation supplies an all-order lower bound on active-heavy mixing at fixed physical masses. A fixed-spectrum one-active/two-heavy construction independently shows that the mixing itself is not uniquely determined by the spectrum. Koide geometry and framing identities still require a predictive dynamical mass or charge-distribution model to become physical predictions.

No fresh branch-resolved nuclear data were imported after an unsuccessful primary-source retrieval. Channel energies, intensities, angular momenta, potential constraints and production inputs remain specific evidence gates. The archive retains the attempted route, rather than filling it with invented values.

## 8. Foundations: test the supplied definitions

The information audit exposes several distinct obligations. Zero-lag transfer entropy is zero by conditioning, whereas a joint-versus-product KL divergence is generally mutual information and need not vanish. A proposed reference-measure formula changes when an auxiliary reference changes. The displayed second-variation combination equals the negative sum of squares, not a Lie commutator. Each statement has an explicit exact witness and a separate likelihood, integral or matrix calculation.

A corrected local KL expansion is constructive: for normalized smooth densities with a shared positive baseline, its leading term is a quadratic score-distance. Identifying that score with ACS dynamics still requires a transition law, observations, histories and reference measure. It does not follow from notation.

The PDR's information-balance halting rule has a concrete obstruction. The deterministic update \((x,y)\mapsto(y,1-x)\) cycles through four states. Under the stationary uniform law, both directional transfer entropies equal one bit, so their difference is zero while the state never converges. A separate contraction-residual theorem supplies a valid stopping certificate when its explicit contraction hypothesis is proved. The cycle is not asserted to satisfy every smooth-field ACS condition.

The geometry review corrects an earlier overly broad source reading. `discrete_geometry_formalism.tex` does provide an O(4) carrier, rewrite maps, and observations. Commuting maps on that actual carrier can have positive reported variance; noncommuting maps can be invisible to a nonconstant observable on the reachable orbit. A well-typed ordered-observation difference and an optional explicit word-sheaf construction are supplied. Probability, faithful observation, gluing and physical selection remain distinct obligations.

The counting audit separates Gibbs normalization from temporal information balance. It also shows directly that a zero total magnetic projection does not alone exclude integer-spin punctures. Internal grading is compatible with different spacetime symbols and arbitrary added masses; an explicit solder map can support a conditional inertia theorem, but the grading does not select that map or action.

## 9. Transparent constraints and the actual checker

The source glossary expands ACS CDCL as **Constraint-Driven Consensus Layer** and distinguishes it from SAT conflict-driven clause learning. The new Boolean provenance instrument is therefore a declared reference sublanguage, not an audit of unseen AISO production code.

It has immutable hashed events, typed exact premises, explicit scope, local resolution, ancestry, and append-only retirement. A retired premise invalidates the current use of conclusions that depend on it without deleting their proofs. A second derivation with independent live support can survive. Resolution soundness is checked against an exhaustive truth-assignment oracle; ancestry is independently reconstructed rather than trusting stored support sets. The suite checks 294 admissible resolution instances, an eleven-event trace, and eight invalid mutations.

The supplied Yang-Mills comparison script was tested unchanged. All eight keyword predictions score a full match on both affirmative and explicitly negated fixtures. A separate implementation reproduces the score. The scan also misses an otherwise complete keyword cluster in its final unscanned window, and the parsed sealed-specification option is unused. These are verified software limitations. The unavailable external proof has not thereby been refuted or verified.

The source inventory recognizes public benchmark code while retaining the separate absence of private production evidence. The copied Lean files have a static census and pinned dependencies, but the supported runtime failures remain unresolved. Zero-sorry token counts are not kernel receipts, and topological inputs declared external in the source remain external.

## 10. Navier-Stokes: current work, exact scope, and ACS

The requested Croft citation is still unresolved. Croft Adams is a plausible public candidate, not an established identification. His [February regularity article](https://medium.com/@theadamsfamily1981/navier-stokes-regularity-complete-proof-via-viscosity-maintained-separation-acb7dc8e87f0) uses estimates contradicted by explicit three-dimensional solenoidal examples below. The candidate's displayed proof does not establish its conclusion. This judgment is confined to that text.

The latest primary-source search also found the [8 September OpenAI release](https://openai.com/index/navier-stokes-solution/), which claims smooth-forced positive-viscosity breakdown and supplies a manuscript and Lean project. The repository at pinned commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` labels review self-assessed. This audit verified selected statement/configuration/adapter files and their hashes; it did not run the full proof. The [Clay formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf) separates forced alternatives C/D from unforced A/B, so those hypotheses cannot be silently interchanged.

Other relevant primary work includes the [March 2026 Hou-Wang-Yang revision](https://arxiv.org/html/2509.25116v2) on computer-assisted unforced Leray-Hopf nonuniqueness from singular initial data; [Albritton-Brue-Colombo](https://annals.math.princeton.edu/2022/196-1/p03) on forced Leray nonuniqueness; [Buckmaster-Vicol](https://annals.math.princeton.edu/2019/189-1/p03) in a broader weak-solution class; and [Chen-Hou](https://arxiv.org/abs/2305.05660) on Euler with boundary. These are different solution classes, initial regularities and equations. The detailed survey also distinguishes fractional viscosity and [Tao's averaged equation](https://arxiv.org/abs/1402.0290). It does not turn related breakthroughs into a theorem for the standard unforced smooth-data problem.

The pinned formalization audit checks identical challenge/submission definition tokens and theorem headers, plus independent inspection of convection, viscosity, initial conditions, force decay, uniform energy and periodic pressure. The two placeholders in the reference challenge are not solution proofs. No placeholder occurs in the selected adapters; this does not certify the entire imported dependency graph. Configuration enabling a checker is not evidence that this audit ran it.

For ACS, the missing mathematical bridge is specific. In unforced flow, energy controls an integrated derivative norm, whereas the enstrophy identity includes potentially positive vortex stretching. Smooth shear solutions show that energy and integrated dissipation do not uniformly control pointwise enstrophy. A Gaussian divergence-free scaling family has bounded H1 norm and unbounded maximum velocity, disproving the candidate H1-to-L-infinity estimate.

More strongly, the exact smooth initial field \(u_0=A(\sin y,0,\cos x-\cos(x+y))\) has decreasing energy and initially increasing enstrophy when A exceeds twelve times the viscosity. At A=16 and viscosity one, the energy derivative is -512 and half the enstrophy derivative is +256. Symbolic integration and the full Fourier-projected nonlinear right-hand side agree. This is an initial-growth example, not a singular solution.

An ACS continuation argument would need a specified functional and a proven bridge to a sufficient critical-norm or strain-integrability estimate, uniformly in any cutoff. No such bridge was found in the supplied corpus. A dimensionless algebraic constant or a finite spectral result does not supply it.

The projection check adds an exact test for any proposed algebraic transfer. For the Poisson bracket on the torus and sharp square Fourier cutoff N, retained real functions \(f=\cos Nx\), \(g=\sin Nx\), \(h=\cos(Nx+y)\) have projected Jacobi sum

\[
J_N=\frac{N^2}{2}\sin(Nx+y)\ne0
\]

for every integer N at least one, while the full Jacobi sum vanishes. Exact Fourier convolution and physical-space differentiation agree. The intended ACS projection must therefore prove closure, control the discarded-mode defect, or specify another legitimate bracket. This does not say that every restricted ACS algebra fails.

M03 gains a separate constructive result. In periodic incompressible ideal MHD about a smooth shear and constant aligned magnetic field, the full nonlinear perturbation energy obeys an exact identity and the bound \(H(t)\le H(0)e^{t\|U'\|_\infty}\) while smooth solutions exist. Integration by parts and an independent full nonlinear Fourier calculation verify cancellation. Higher-norm continuation, unequal-density interfaces and nonlinear persistence remain open.

## 11. What remains genuinely open

The current checklist is an append-only map, not a claim of universal completion. The most important remaining paths are:

- **Executable mathematical work:** full two-loop Yukawa/scalar/mass contractions, scalar-compatible interacting fixed points and stability, and verified proof-assistant execution in a supported environment. Partial calculations retain their precise degree and loop order.
- **Unproved analytic bridges:** unconditional prime remainder bounds, the RH-equivalent estimate, natural-operator identification, nonlinear shear/MHD persistence, and an ACS functional controlling a sufficient Navier-Stokes continuation norm.
- **Model choices and physical data:** vacuum and boundary values, light-field content and thresholds, nuclear channels and independently constrained potentials, predictive flavor and charge/current dynamics.
- **Unseen evidence:** the intended Croft reference, authorized production AISO code and benchmark protocol, the external Yang-Mills proof, and independent full verification receipts for newly released formalizations.

There is no quality ranking between a constructive theorem and a rigorously excluded route. What matters is that the exact conclusion, assumptions, evidence and next step are recoverable. The failed attempts, source corrections, previous archive and full ledger prefix are preserved so the same errors need not be rediscovered.

The replay and integrity receipts accompany the final checklist. They distinguish successful mathematical programs from failed exploratory attempts and from source/runtime gates that were never verified. Reproduction establishes that the archived computation can be rerun; it does not upgrade conditional arithmetic premises, metadata, or a selected-file audit into a universal proof.
