# Navier–Stokes, the Croft citation, and the ACS continuation gap

Research cut-off: 11 September 2026. This workstream distinguishes mathematical derivation, computation, published results, and newly released proof claims. It does not prove or disprove general unforced three-dimensional Navier–Stokes regularity.

## Main result

The ACS corpus supplies a useful discipline for separating a constraint, a model, a numerical observation, and a theorem. It does not presently supply a bound that converts incompressibility, energy dissipation, or information asymmetry into the norm control needed for global Navier–Stokes regularity. The independent checks here identify exactly where that conversion fails. They also extend M03 to a conditional **nonlinear perturbation-energy estimate** in a specified ideal-MHD model; nonlinear smooth persistence remains open.

A current-source check is essential: on 8 September 2026 OpenAI released a manuscript claiming smooth-forced, positive-viscosity three-dimensional Navier–Stokes blowup, together with Lean formalization. That claim must be assessed on its own hypotheses and proof, rather than omitted by repeating an older blanket description of the subject. It concerns the forced alternatives C/D of the Clay formulation. It is not by itself a counterexample to the unforced assertions A/B. [Announcement](https://openai.com/index/navier-stokes-solution/), [manuscript](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf), [Clay formulation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf).

## 1. What “Croft's reference” could mean

A recursive case-insensitive search of the supplied ACS repository found **no `Croft` or `Navier` match**. The `Stokes` matches primarily concern the differential-form theorem and do not identify a Navier–Stokes citation. Repository revision: `1ab25455b00f384eade0721144052131cc52465d`.

A plausible public candidate exists: **Croft Adams**, *Navier–Stokes Regularity: Complete Proof via Viscosity-Maintained Separation*, 3 February 2026. Its proof invokes the false three-dimensional embedding

\[
\|u\|_\infty\le C(\|u\|_2+\|\nabla u\|_2),
\]

and subsequently assumes a derivative bound from the velocity norm. It also treats integrated dissipation as pointwise gradient control. These steps are not valid estimates for arbitrary three-dimensional smooth divergence-free fields; Sections 4–5 give independently derived counterexamples. The article's claimed global-regularity conclusion therefore does not follow from its displayed proof. [Authored article](https://medium.com/@theadamsfamily1981/navier-stokes-regularity-complete-proof-via-viscosity-maintained-separation-acb7dc8e87f0).

A second candidate, dated 22 February 2026 with an internal 21 February date, claims formal Navier–Stokes and Yang–Mills proofs. Its displayed regularity statement omits convection, and the displayed proof contains `sorry` placeholders. Its trace-free algebra does not establish a PDE continuation estimate. These observations concern this authored Medium text; they must not be confused with challenge placeholders in an unrelated formalization repository. [Second authored article](https://medium.com/@theadamsfamily1981/navier-stokes-existence-and-smoothness-and-yang-mills-existence-and-mass-gap-complete-formal-db37dfa64786).

Neither search establishes that Adams is the person the user intended. A transcription of “cross-reference” is another possibility, not an identification. The exact unresolved request is: **“Please provide the author, title, link, or quoted passage meant by ‘Croft's reference’; did you mean Croft Adams, or ‘cross-reference’?”** The substantive analysis below does not depend on the answer.

## 2. Current advances and their exact scope

| Result/source | What it addresses | What cannot be inferred |
|---|---|---|
| OpenAI, 8 September 2026, Theorem 1.1 | Claims that for every positive viscosity there is a smooth compactly supported space-time force and zero initial data producing a smooth flow before time 1, with bounded kinetic energy and unbounded velocity near time 1. | This is a newly released manuscript and formalization claim, not an independently rerun theorem in this workstream. Its forced construction does not establish unforced blowup. |
| Hou–Wang–Yang, arXiv:2509.25116v2, 19 March 2026 | Claims a computer-assisted construction of infinitely many suitable Leray–Hopf solutions of unforced 3D Navier–Stokes with common compactly supported data, smooth away from the origin and in every spatial Lq below q=3; solutions are smooth at positive times. | Singular initial data are essential to the theorem statement. This is not formation of a singularity from smooth initial data. No journal acceptance or independent replay was established here. |
| Albritton–Brué–Colombo, Annals 2022 | Two distinct Leray solutions starting at zero with identical forcing. | The force belongs to a class allowing an initial-time singularity; it is not a smooth-forcing Clay counterexample. |
| Buckmaster–Vicol, Annals 2019 | Nonuniqueness among finite-energy weak solutions. | Finite-energy weak is a broader class than Leray–Hopf. The result does not establish smooth-data classical nonuniqueness. |
| Chen–Hou, analysis/numerics papers | Computer-assisted smooth-data blowup for axisymmetric Euler with boundary. | Euler has zero viscosity; the boundary and equation matter. It is not the standard unforced positive-viscosity whole-space Navier–Stokes theorem. |
| Córdoba–Martínez-Zoroa–Zheng, arXiv:2407.06776 | Forced fractional-dissipation blowup with dissipation order α below (22−8√7)/9, using the convention \(|\nabla|^\alpha\). | Standard viscosity corresponds to α=2 in this convention, far outside the theorem's range. The force's stated regularity is also different from smooth compact forcing. |
| Tao, arXiv:1402.0290 | An averaged modification of Navier–Stokes retains its energy cancellation but admits blowup. | It is a modified nonlinearity, not the original equation. It is a rigorous obstruction to arguments using only those shared estimates. |

Primary references for the rows: [OpenAI paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf); [Hou–Wang–Yang v2](https://arxiv.org/html/2509.25116v2); [Albritton–Brué–Colombo](https://annals.math.princeton.edu/2022/196-1/p03); [Buckmaster–Vicol](https://annals.math.princeton.edu/2019/189-1/p03); [Chen–Hou I](https://arxiv.org/abs/2210.07191), [II](https://arxiv.org/abs/2305.05660); [fractional result](https://arxiv.org/abs/2407.06776); [averaged equation](https://arxiv.org/abs/1402.0290).

The lesson from computer-assisted PDE is precise: a plausible profile and a small computed residual are only part of the work. Hou–Wang–Yang also address the operator inverse, an unstable eigenpair, infinite-dimensional remainder, and localization to finite-energy data; their [code is public](https://github.com/HouGroup2026/3d-navier-stokes-nonuniqueness). The entire proof or verification suite was not rerun here.

The OpenAI release supplies [formalization files](https://github.com/openai/NavierStokesAndEuler). The parent audit separately inspected the repository at commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, found self-assessed verification metadata and an explicitly convection-containing comparator definition, and distinguished challenge placeholders from the submitted proof. That static audit is stronger than an announcement-only reading, but it is not a fresh Lean/kernel run. Consult the parent evidence for its exact audit boundary.

This is a focused, primary-source survey of the relevant frontier, not an assertion that every September 2026 preprint was validated. Unreviewed broad regularity claims surfaced in searching and were not promoted to established results.

## 3. The rigorous bridge ACS would need

Work with smooth divergence-free fields on \(\mathbb R^3\) with sufficient decay, or on a periodic three-dimensional torus. Let

\[
\partial_tu+(u\cdot\nabla)u+\nabla p=\nu\Delta u+f,
\quad \omega=\nabla\times u,\quad
E=\tfrac12\|u\|_2^2,\quad Y=\|\omega\|_2^2=\|\nabla u\|_2^2.
\]

Multiplication by \(u\), integration, incompressibility, and boundary cancellation give

\[
E'(t)+\nu Y(t)=\langle f,u\rangle.
\]

With no forcing, this controls \(\sup_tE(t)\) and \(\int_0^T Y(t)dt\), not \(\sup_{t<T}Y(t)\). Curling the equation gives

\[
\partial_t\omega+(u\cdot\nabla)\omega
=(\omega\cdot\nabla)u+\nu\Delta\omega+\nabla\times f.
\]

The transport integral vanishes again, leaving

\[
\tfrac12Y'+\nu\|\nabla\omega\|_2^2
=\int\omega\cdot S\omega\,dx+\langle\nabla\times f,\omega\rangle,
\quad S=\tfrac12(\nabla u+\nabla u^\top).
\]

The trace-free condition \(\operatorname{tr}S=0\) does not make this stretching term nonpositive. For a symmetric trace-free \(3\times3\) matrix, the sharp algebraic estimate is

\[
\lambda_{\max}(S)\le\sqrt{2/3}\,|S|_F.
\]

Indeed, \(\lambda_2+\lambda_3=-\lambda_1\) implies \(\lambda_2^2+\lambda_3^2\ge\lambda_1^2/2\). Equality is attained by \(\operatorname{diag}(a,-a/2,-a/2)\). This is a **relative** pointwise bound, not a bound on \(|S|\), and its dimensionless constant is not a critical scaling exponent.

For unforced flow on \(\mathbb R^3\), Hölder, the Riesz-transform bound, Sobolev, and interpolation give

\[
\left|\int\omega\cdot S\omega\right|
\le C\|\omega\|_3^3
\le C\|\omega\|_2^{3/2}\|\nabla\omega\|_2^{3/2}
\le\frac\nu2\|\nabla\omega\|_2^2+C_\nu Y^3,
\quad C_\nu\sim C\nu^{-3}.
\]

Consequently \(Y'\le C\nu^{-3}Y^3\). Comparing to the equality ODE yields only a finite local control interval; it is not a global estimate. A better constant below one in the stretching estimate still leaves the cubic power and does not close this argument.

One sufficient bridge is \(\int_0^T\|S(t)\|_\infty dt<\infty\), which makes the enstrophy estimate a Grönwall inequality. Another is a velocity bound in \(L_t^pL_x^q\), \(q>3\), \(2/p+3/q\le1\). The endpoint \(L_t^\infty L_x^3\) is covered by Escauriaza–Seregin–Šverák. These are continuation criteria; proving their hypotheses for arbitrary smooth initial data remains the substantive missing step for the unforced problem. [Original endpoint publication record](https://experts.umn.edu/en/publications/lsub3sub-solutions-of-the-navier-stokes-equations-and-backward-un/).

The scaling makes the gap visible. For \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t)\),

\[
\|u_\lambda\|_2^2=\lambda^{-1}\|u\|_2^2,
\quad \|\nabla u_\lambda\|_2^2=\lambda\|\nabla u\|_2^2,
\quad \|u_\lambda\|_3=\|u\|_3.
\]

Thus increasingly fine structure can become cheaper in energy while more expensive in derivatives. This calculation is not a construction of a singular solution.

## 4. Independently checked counterexamples to the proposed estimates

### 4.1 Exact unforced shear solutions: energy does not bound enstrophy uniformly

On \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), with volume normalized to one, take

\[
u_N(x,y,z,t)=e^{-\nu N^2t}(\sin Ny,0,0),\quad p=0.
\]

The nonlinear term is exactly zero, and the remaining equation is the heat equation. Therefore

\[
E_N(t)=\tfrac14e^{-2\nu N^2t},\quad
Y_N(t)=\tfrac{N^2}{2}e^{-2\nu N^2t},\quad
\int_0^\infty Y_N(t)dt=\tfrac1{4\nu}.
\]

At \(t_N=(\nu N^2)^{-1}>0\), energy is the same for every N, but enstrophy grows like \(N^2\). Every member is smooth and globally regular. This refutes a uniform estimate using only this energy/dissipation information; it does not refute estimates depending on the initial higher norm or on a fixed positive waiting time.

### 4.2 Bounded H1 does not bound maximum velocity in three dimensions

Let \(\psi=e^{-|x|^2}\) and

\[
v=(\partial_y\psi,-\partial_x\psi,0)=(-2y,2x,0)e^{-|x|^2},
\quad C=\|v\|_2^2=\pi^{3/2}/\sqrt2.
\]

The field is smooth, rapidly decaying, and divergence-free. Direct integration gives \(\|\nabla v\|_2^2=5C\). For

\[
w_\lambda(x)=\lambda^{1/2}v(\lambda x)/\sqrt C,
\]

we obtain \(\|w_\lambda\|_2^2=\lambda^{-2}\), \(\|\nabla w_\lambda\|_2^2=5\), but

\[
\|w_\lambda\|_\infty=\lambda^{1/2}\sqrt{2/e}/\sqrt C\longrightarrow\infty.
\]

This is a direct solenoidal counterexample to the candidate's H1-to-L∞ inequality. Replacing \(\lambda^{1/2}\) by \(\lambda^{3/2}\) gives an L2-normalized family with gradient norm squared \(5\lambda^2\), disproving a reverse derivative estimate. These are initial fields, not purported full solutions with blowup.

### 4.3 Enstrophy can initially increase while energy decreases

Set \(u_0=A(\sin y,0,\cos x-\cos(x+y))\). It is a divergence-free trigonometric polynomial. Exact integrations give

\[
E(0)=\tfrac34A^2,\quad Y(0)=2A^2,\quad
\|\nabla\omega(0)\|_2^2=3A^2,\quad
\int\omega\cdot S\omega=\tfrac14A^3.
\]

Hence

\[
E'(0)=-2\nu A^2<0,\quad
\tfrac12Y'(0)=A^2(A/4-3\nu)>0\quad\hbox{if }A>12\nu.
\]

For A=16 and ν=1, the two derivatives are **−512** and **+256**, respectively (the latter is half the derivative of Y). The independent Fourier evaluation applies the actual projected nonlinear Navier–Stokes right-hand side and reproduces these values. It is an initial-growth counterexample, not a finite-time singularity.

### 4.4 Integrated dissipation does not prohibit an endpoint spike

The scalar pair \(Y(t)=(1-t)^{-1/2}\), \(E(t)=\nu+2\nu\sqrt{1-t}\), \(0\le t<1\), has \(E'+\nu Y=0\), positive bounded energy, and finite \(\int_0^1Y=2\), but unbounded Y. This pair only tests the logical content of the scalar energy identity; it is not claimed to solve Navier–Stokes.

## 5. What M03 gains: a specified nonlinear ideal-MHD estimate

The earlier M03 result concerns linear planar-interface magnetic stabilization. A complete nonlinear model requires more information than its dispersion relation. Here is a finite statement for **constant-density incompressible ideal MHD on the periodic torus**, with the magnetic field expressed in velocity units:

\[
u_t+u\cdot\nabla u+\nabla P=b\cdot\nabla b,
\quad b_t+u\cdot\nabla b=b\cdot\nabla u,
\quad\nabla\cdot u=\nabla\cdot b=0.
\]

The fields \(U=U(y)e_x\), \(B=B_0e_x\) are a steady background. Write \(u=U+v\), \(b=B+h\), and

\[
H=\tfrac12\int(|v|^2+|h|^2)dx.
\]

Multiplying the two perturbation equations by v and h and integrating yields the **full nonlinear identity**

\[
H'=-\int U'(y)(v_xv_y-h_xh_y)dx.
\]

The transport and pressure terms integrate to zero. The cubic self-interactions cancel because

\[
\int v\cdot(h\cdot\nabla h)+h\cdot(h\cdot\nabla v)=\int h\cdot\nabla(v\cdot h)=0;
\]

the remaining advective cubic terms vanish separately. Uniform-background magnetic terms likewise pair into a total derivative. Therefore

\[
|H'|\le\|U'\|_\infty H,
\qquad H(t)\le H(0)e^{t\|U'\|_\infty},
\]

throughout any smooth solution interval. The numerical check constructs independent three-dimensional solenoidal v,h, evaluates the complete nonlinear RHS including Leray pressure elimination, and verifies the identity without linearizing.

This gives conditional finite-time L2 control with a specified norm, domain, data, and dynamics. It does **not** supply a uniform higher-derivative estimate, show decay, or prove nonlinear vortex-knot persistence. The absence of B0 from this coarse energy bound does not contradict magnetic spectral stabilization: its directional phase information is lost in this estimate. Resistive/viscous MHD, unequal-density interfaces, current sheets, boundaries, and observed plasma parameters need their own model and estimates.

## 6. Exact ACS cross-reference and next admissible bridge

| Supplied ACS object | What is actually available | Missing Navier–Stokes link |
|---|---|---|
| Paper A definitions ACS-1/2/3, `Palatini_Gauge_Attractor.tex` | Codependence, operator-type asymmetry, mutual constraints; transfer-entropy asymmetry is defined from a specified joint law. | Specify genuine NS field spaces and a probability/coarse-graining law. Velocity/vorticity are not freely independent: Biot–Savart already relates them. No bound on a critical PDE norm follows from their labels. |
| `One_Mechanism_Many_Forms_Sigma.tex`, identity-chain section and August status update | The manuscript itself retires its literal ΔI=c identification as stated and classifies current cross-domain sameness as analogy. | A new identity or inequality relating a precisely defined ACS functional to strain, enstrophy, or a Serrin norm must be proved, with cutoff-independent constants. |
| Archived `Constraint_Projection_Framework.tex` and its audit | The paper's own status block labels its load-bearing claims T4. Its surface-to-space integral operator is not the solenoidal orthogonal projection. | Define and prove the operator's relationship to the Helmholtz–Leray multiplier; topological language is not this relationship. |
| `finite_thickness_kh.py`, F1–F4 | Linear inviscid Rayleigh analysis around a tanh shear, including a finite growth rate and short-wave cutoff. It explicitly does not make the layer stable. | Linear growth control is not nonlinear NS/MHD continuation. The full evolution can change the shear and its scales. The unique-peak continuation M08 is owned by the separate workstream and is not duplicated here. |

For reference, the genuine Leray projector is \(\widehat{Pq}(k)=(I-k\otimes k/|k|^2)\hat q(k)\) for k≠0, with the zero mode fixed appropriately. It satisfies \(P^2=P=P^*\) and removes gradients. Its energy cancellation follows from incompressibility and integration by parts; it is not an automatic consequence of a generic projection or an information-balance principle. The parent's projection workstream independently examines stronger algebraic obstructions.

An ACS proposal becomes a reviewable PDE contribution if it specifies a functional A[u], proves a uniform a priori estimate, and proves a bridge such as

\[
\int_0^T\|S\|_\infty dt\le C(u_0,\nu,T,A),
\quad\hbox{or}\quad\|u\|_{L_t^pL_x^q}\le C,
\quad2/p+3/q\le1.
\]

The probability law, pressure, nonlinear term, viscosity, boundary conditions, and all infinite-mode remainders must be included. The counterexamples above are mandatory tests for any proposed bridge; a method that fails them cannot certify general regularity. No such complete bridge was located in the supplied corpus.

## Reproduction and audit boundary

`energy_checks.py` checks the trigonometric identities by symbolic integration and independently by Fourier differentiation; it checks Gaussian norms by symbolic integration and independently by Gauss–Hermite quadrature. Assertions compare the actual computed equations and derivatives, not merely two rephrasings of a claimed conclusion. The Fourier grids resolve all products used; these are small exact-mode checks, not turbulence simulations or interval certificates.

Install `requirements.txt`, then run:

```bash
python energy_checks.py --output evidence/checks_replay.json
```

`evidence/checks.json` retains the first successful run; `evidence/checks_v2.json` adds the nonlinear MHD identity. `evidence/attempts.json` records dependency failures and source-retrieval limitations. No failed attempt was silently replaced with a success claim. The successful run used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, and SymPy 1.14.0.

The derivations here are exact mathematical arguments with numerical cross-checks. They do not promote a preprint, a model equation, or a self-assessed formalization to an independently certified resolution of a Millennium problem.
