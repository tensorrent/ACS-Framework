# Glossary and Index of Key Terms — ACS Framework

Coined and specialized vocabulary used across this repository's manuscripts, notes, and
verification code. Every entry cites its defining location; where a claim has a recorded
verification status it is stated in the framework's tier vocabulary (T1 machine-verified /
T2 proved / T3 numerically verified / T4 explicitly falsified — see
[Verification and governance vocabulary](#verification-and-governance-vocabulary)).
Falsified claims are retained here deliberately and marked as such: the corpus keeps its
negatives.

Each section opens with **primary entries** (subsection headings) for load-bearing terms,
followed by compact supporting vocabulary. The [alphabetical index](#alphabetical-index)
at the end covers every entry.

A companion document, [`docs/Cross_Repo_Glossary_Extract.md`](docs/Cross_Repo_Glossary_Extract.md),
preserves the earlier cross-repository catalogue, which also covers codebases outside this
repository.

## Contents

1. [Framework core](#framework-core)
2. [Verification and governance vocabulary](#verification-and-governance-vocabulary)
3. [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a)
4. [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions)
5. [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions)
6. [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes)
7. [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread)
8. [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d)
9. [Alphabetical index](#alphabetical-index)


## Framework core

The foundational vocabulary of the ACS formalism: the central object, its axioms, and the information-theoretic and Lie-algebraic machinery built on it. Primary sources: `papers/Form_Function_and_Asymmetry.tex` and the core trilogy.

### Adversarial compression

The core methodology: every claim goes through CONJECTURE → EXPLICIT COMPUTATION → RESULT; a survivor compresses to a theorem with proof, a failure is recorded as a first-class negative result with the killing computation and failure mechanism, and a partial result is recorded as an observation with a scope boundary. Rules include never dressing a conjecture in theorem language and treating overclaiming as the primary failure mode.

**Source:** docs/ACS_FRAMEWORK_SKILL.md sec 2; docs/ACS_Corpus_Map.md sec 2 INV-7  
**Also:** INV-7, adversarial compression methodology

### Asymmetric Codependent System (ACS)

A pair of smooth fields (F, Phi) on a manifold satisfying three conditions: codependence (each field's evolution equation depends on both fields), structural asymmetry (the coupling operators f and g differ as operator types, not merely in parameter values), and mutual constraint (neither field's admissible states are reachable while holding the other fixed arbitrarily). The framework's central object, claimed to be realised in gauge theory, number theory, discrete geometry, RG flow, and quantum gravity.

**Source:** papers/Form_Function_and_Asymmetry.tex Definition 2.3 (label def:acs), lines 262-290  
**Also:** ACS, ACS (Asymmetric Codependent Systems), ACS Framework, ACS framework, Algebraic Conductance State (ACS) framework, Asymmetric Codependent Systems, Sovereign-Stack ACS Research Program

### Asymmetry map Phi

The map Phi: T_p Y^14 -> gl(4), Phi(v) = [e(v), omega(v)], sending a tangent vector of the metric bundle to the commutator of its vierbein and connection components. For generic fields its image is all of sl(4) (rank 15, computed by exact symbolic rank over Q).

**Status:** T1/T2: exact symbolic computation  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 4.2, Theorem 'Image of the asymmetry map' (thm:image-phi, ~line 943)

### Constraint-attractor cycle

The dynamical cycle Constraint -> Solution -> Dominance -> Inversion -> New Constraint, in which every ACS attractor is simultaneously the next constraint. Canonical instance: torsion-free Palatini equilibrium T^a = 0 -> torsion activation -> chiral modes -> spinor bundle -> su(3) -> confinement as the new constraint; analogues are tabulated for quantum gravity, Ricci flow, Riemann zeros, and the Higgs sector.

**Status:** framework principle; three instances computationally verified  
**Source:** papers/core_trilogy/Holographic_Spectral_Inversion.tex sec 3.3 (sec:constraint) and sec 6 Table 'inversion arc across domains'  
**Also:** constraint-attractor loop

### Emergent pattern

Defined precisely as the 3rd-order holonomy [[f,g],f] + [[f,g],g]: the component of Delta-I that is irreducible to direct or bracketed coupling, i.e. the residue of the closed loop Form -> Function -> Form. It is the BCH-series term the framework identifies with observable emergent structure (Yang-Mills equation, spin-foam vertex amplitudes, Banach-Tarski volume).

**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 2.2 (def:nested, ~line 414)  
**Also:** 3rd-order holonomy, holonomy term

### Form field

Within an ACS, the field carrying structural information: boundary conditions, equilibrium geometry, the space of admissible states. Instances include the vierbein e in gravity, the field strength F_munu in gauge theory, primes {p_n} in number theory, and cables in tensegrity; in the AI stack it becomes a typed immutable state object.

**Source:** papers/Form_Function_and_Asymmetry.tex Definition def:FF, lines 292-304; papers/ACS_Deterministic_AI_Stack_PDR.tex Glossary  
**Also:** F, Form

### Form/Function Relativity

The principle that the {form, function} label is a coordinate on the product space (witness x frame), not an intrinsic property of the witness: for a fixed witness there exist reference frames in which it is form and frames in which it is function. Slogan: 'one witness's form is another witness's function.'

**Status:** T1 (measured instance on the Riemann spectrum, sec 5; stated in sec 6)  
**Source:** papers/methodology/Form_Function_Relativity.tex Principle 2, sec 2 (lines 82-84); title and abstract  
**Also:** FF06g, frame ladder, frame-relativity of form/function

### Fourier-dual asymmetric codependent partners

The structural claim that the prime sequence and zero sequence exchange information through Fourier transformation (the explicit formula), never through frequency matching: F_N(omega) = (1/N) sum cos(omega gamma_k) peaks precisely at prime-power logarithms log(p^k), while no direct gamma_k-to-prime-frequency alignment exists. Extended empirically to Dirichlet L-functions and the Dedekind zeta of Q(i).

**Status:** T1 measured (top-20 peaks within mean 5e-5; 100% character-sign recovery); rederives classical results in new framing  
**Source:** papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 6.4 (sec:tartini-synthesis) and sec 7 (sec:lfunctions)

### Function field

Within an ACS, the field carrying dynamic information: how the system moves between states, the generator of change. Instances include the spin connection omega, the gauge potential A_mu, Riemann zeros {gamma_k}, and struts in tensegrity; in the AI stack it becomes a typed operator acting on Forms. Form constrains what Functions are realisable; Function determines which Forms are stable.

**Source:** papers/Form_Function_and_Asymmetry.tex Definition def:FF, lines 292-304; papers/ACS_Deterministic_AI_Stack_PDR.tex Glossary  
**Also:** Function, Phi

### Holographic resolution

A system S holographically resolves constraint C if (HR-1) boundary completeness: I(boundary S; C) = H(C); (HR-2) interior redundancy: I(boundary; interior | C) = 0; and (HR-3) outward gating: Delta-I(S -> exterior) < 0. The Ryu-Takayanagi formula is claimed to be recovered at Delta-I = 0; in Paper A the black-hole horizon is conjectured to be an ACS inversion surface with S_BH as a Delta-I saturation integral.

**Status:** definition-only; S_BH identification explicitly a conjecture  
**Source:** papers/core_trilogy/Holographic_Spectral_Inversion.tex sec 3.1, Definition 'Holographic Resolution' (def:holo); used in Palatini_Gauge_Attractor.tex sec 5.5  
**Also:** HR-1/HR-2/HR-3, holographic resolution principle

### Information balance

The condition Delta I = 0, in which Form and Function carry equal mutual information; it is the attractor state across domains (Ricci-flat geometry, colour singlets, RH stationarity, Wheeler-DeWitt) and the halting criterion of the deterministic AI stack.

**Source:** papers/Form_Function_and_Asymmetry.tex def:DI line 321 and passim; papers/ACS_Deterministic_AI_Stack_PDR.tex Glossary  
**Also:** ACS balance condition, Delta I = 0

### Inversion arc

The principle that a system solving a constraint becomes the new constraint: as S becomes the dominant access structure the ACS roles of Form and Function exchange, and by the BCH-TE morphism the sign of Delta-I flips exactly at leading order. Claimed to be instantiated by the Zamolodchikov c-theorem and Komargodski-Schwimmer a-theorem, and verified computationally in three Paper-A instances (Ricci flow, constraint hierarchy, WdW attractor).

**Status:** proved from BCH-TE morphism (conditional on it); instances T3 numerical  
**Source:** papers/core_trilogy/Holographic_Spectral_Inversion.tex sec 3.2, Theorem 'Inversion arc of access systems' (thm:inversion)  
**Also:** INV-5, Paper C: The Inversion Arc, holographic resolution principle, inversion theorem, the key has become the lock

### Nested coupling orders

The power-series expansion Delta-I(eps) = a1*eps + a2*eps^2 + a3*eps^3 + ..., where 1st order is direct coupling, 2nd order is the Lie bracket [f,g] of the coupling operators, and 3rd order is the holonomy term [[f,g],f] + [[f,g],g]. These orders are mapped to torsion, curvature, and the Bianchi identity in gauge theory, and to the Gauss, diffeomorphism, and Hamiltonian constraints in LQG.

**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 2.2, Definition 'Nested Coupling Orders and Emergence' (def:nested, ~line 404)  
**Also:** 1st/2nd/3rd order coupling, ACS coupling orders, BCH orders, coupling orders

### One mechanism, many forms

The synthesis principle that the form/function asymmetry recurring across the ACS corpus is one mechanism genuinely expressed through many substrates - an ontological claim (each form is a faithful instance of the mechanism running, like the wave equation in sound, light, and quantum amplitude), not an epistemic blind-men-and-elephant claim about refracted views of a hidden object. It holds by identity where the identity chain is established and is a falsifiable conjecture where the chain is only gestured (biology, cognition, institutions, language, the theological reading).

**Status:** established within treated domains (T1/T2 forcing); cross-domain identity conditional on Link 3  
**Source:** papers/later_FF06_series/One_Mechanism_Many_Forms_Sigma.tex sec 1 (lines 62-94)  
**Also:** Identity chain, Links 1-3, ontological reading, the singular reading

### Palatini bracket

The Lie bracket [e, ω] obtained by applying the BCH-TE morphism to the vierbein e^a_μ and connection ω^{ab}_μ in Palatini gravity; it generates the split real Lie algebra sl(4,ℝ) (rank 15), which the Palatini decomposition splits into a 6-dimensional Lorentz sector so(3,1) and a 9-dimensional torsion sector.

**Source:** docs/ACS_Technical_Whitepaper.md sec 2.1  
**Also:** [e, ω]

### Positional duality

The three-layer decomposition of Riemann-zero spectral statistics into structurally independent layers: Density (the smooth Riemann–von Mangoldt term, carrying no arithmetic), Local Spacings (GUE universality class), and Positions (arithmetic, governed by the primes via the Weil-Guinand explicit formula). The arithmetic content of the zeros resides entirely in their exact level positions, not in their spacing law.

**Status:** T1 (form/function split at 11,497σ arithmetic vs 0.4-1.0σ form, FF06e)  
**Source:** docs/ACS_Technical_Whitepaper.md sec 3.1; docs/ACS_Corpus_Map.md sec 1 (FF06f)  
**Also:** Density/Spacings/Positions, FF06f decomposition, three-layer decomposition

### role-relativity in nested systems

The general principle of which form/function relativity is the spectral instance: for a component inside a family of systems ordered by nesting (each enclosing system resolving more structure), the two-valued role assigned to the component is a coordinate on (component x system), not a property of the component; ascending the nest can only convert the marked role (recording unresolved structure) into the unmarked one, so each component flips exactly once at a single threshold level. Illustrated by 'one man's trash is another's treasure' and 'one party's security is another's leverage.'

**Status:** framing only — the paper states the folk dualities are cited to locate the principle, not as evidence (sec 6)  
**Source:** papers/methodology/Form_Function_Relativity.tex Principle 1, sec 2 (lines 76-78)

### T1 (ACS generates non-zero information asymmetry)

The theorem that for generic coupling pairs (f,g) with f not identically g, within the BCH convergence radius, Delta I(eps) is non-zero for all but finitely many eps > 0, with sign determined by the dominant BCH order at the late-time attractor.

**Status:** proved for generic case; the non-generic case's inductive argument is admitted informal (sec 11.4)  
**Source:** papers/Form_Function_and_Asymmetry.tex Theorem thm:acs-DI (labels thm:acs-DI, thm:T1-closed), lines 413-457  
**Also:** T1-closed, Theorem 2.9

### T4 (RH implies F_N stationarity)

The one-directional theorem that the Riemann Hypothesis implies stationarity of F_N(x): on the critical line each conjugate zero pair contributes a constant envelope after dividing by sqrt(x), while any off-critical zero adds a strictly positive excess x^sigma + x^(1-sigma) - 2x^(1/2) (AM-GM) that makes F_N non-stationary.

**Status:** proof sketch plus numerical confirmation at N=25 zeros; N=200 extension stated as in progress  
**Source:** papers/Form_Function_and_Asymmetry.tex Theorem thm:FN-acs (label thm:T4), lines 826-869  
**Also:** F_N stationarity theorem, Theorem 4.1

### Torsion as 1st-order ACS coupling (C2)

The lemma that Cartan torsion T^a = de^a + omega wedge e is the 1st-order ACS coupling between Form (vierbein) and Function (spin connection), and that in vacuum Palatini gravity T^a = 0 is the ACS equilibrium state reached dynamically by the field equations rather than imposed externally.

**Status:** proved from the Palatini variation  
**Source:** papers/Form_Function_and_Asymmetry.tex Lemma lem:torsion (label thm:C2-closed), lines 715-751  
**Also:** ACS vacuum equilibrium T^a = 0, C2-closed

#### Supporting vocabulary

- **ACS measure** — The canonical invariant measure equipping a deterministic ACS so transfer entropy is well-defined: the ergodic invariant (SRB) measure mu of the phase flow on X x Y, with marginals given by pushforwards. For primes the measure is the log-prime point process with PNT ergodicity; for zeros the GUE pair-correlation measure; for gauge fields the Liouville measure on the constraint surface. *(papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 2.1, Definition 'ACS measure' (def:acs-measure, ~line 313))*
- **ACS-1 Codependence** — The first ACS axiom: the evolution equations of Form and Function each depend on both fields, so neither field is independent and neither is derivable from the other alone. *(papers/Form_Function_and_Asymmetry.tex def:acs, lines 268-274)*
- **ACS-2 Structural Asymmetry** — The second ACS axiom: the coupling operators f and g satisfy f not-identical-to g as operator types on the respective field spaces, meaning they differ in functional form (e.g. polynomial vs. absolute value), not merely in parameter values. *(papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 2.2 (def:acs, ~line 357))*
- **ACS-3 Mutual Constraint** — The third ACS axiom: the equilibrium set of Form constrains the reachable configurations of Function and vice versa; no admissible state of the pair is accessible by varying one field while holding the other fixed at an arbitrary value. *(papers/Form_Function_and_Asymmetry.tex def:acs, lines 285-289)*
- **Asymmetry map Phi(v) = [e(v), omega(v)]** — The map from tangent vectors of Y^14 to gl(4) given by the commutator of the vierbein and connection values. Its image for generic fields is exactly sl(4) (15-dimensional), established by an exact rank-15 computation of the 72x16 bracket coefficient matrix over Q. *(exact symbolic computation (rank over Q, no floating point); papers/Form_Function_and_Asymmetry.tex Theorem thm:image-phi, lines 1430-1445)*
- **Colour charge gap** — The framework's name for the remaining obstruction in deriving colour: the passage from the split real form sl(3,R) (already present in Palatini geometry) to the compact form su(3), reduced by the paper to a single complexification step via the torsion-induced spinor bundle whose gamma^5 should reproduce the chirality map. *(open (described as ~3 pages of spinor geometry); papers/Form_Function_and_Asymmetry.tex abstract lines 107-118 and sec 11.2 lines 2096-2118)*
- **Conjecture P2: Wheeler-DeWitt as ACS fixed point** — The conjecture that the Wheeler-DeWitt equation H-hat |Psi> = 0 is equivalent to the ACS balance condition Delta I[Psi] = 0 on the kinematic Hilbert space; stated as a theorem classically, open quantumly, with emergent time read as Delta I symmetry breaking by hbar corrections. *(conjecture; papers/Form_Function_and_Asymmetry.tex Conjecture conj:WdW, lines 2026-2035)*
- **Conjecture: geometric fermions from torsion** — The conjecture that in an ACS with non-zero torsion, the torsion-spin coupling produces half-integer angular momentum modes from purely geometric data, with no independent spin structure required (Cartan-Kibble-Sciama mechanism as the 1st-order ACS coupling). *(conjecture; toy-model support from the chirality lattice; papers/Form_Function_and_Asymmetry.tex Conjecture conj:fermions, lines 1129-1135)*
- **Conjecture: Standard Model from GL(4) fiber** — The conjecture that with the ACS coupling (e, omega) on Y^14, the asymmetry bracket generates su(2) + u(1) as the electroweak sub-algebra; refined later into the 'precise GL(4) generation' question of whether a vacuum and symmetry-breaking pattern yields the full SM gauge algebra and fermion representations. *(conjecture; four sub-claims listed open; papers/Form_Function_and_Asymmetry.tex Conjecture conj:SM lines 1113-1127 and conj:gl4-precise lines 1873-1886)*
- **Electroweak Containment** — The argument that su(2)_L x u(1)_Y arises from the O(4) = SU(2)_L x SU(2)_R / Z2 fiber structure of Y^14 after vacuum selection and SU(2)_R -> U(1)_Y breaking, while colour-hypercharge su(3) + u(1)_{B-L} embeds separately in su(4) via the Pati-Salam route; the full SM algebra thus needs two geometric sources. *(partial containment proved; unified single-source derivation open; papers/Form_Function_and_Asymmetry.tex sec 9.5 lines 1717-1750 and Proposition thm:SM-containment lines 1392-1424)*
- **Exact integer automaton** — A floating-point-free verification instrument: a discrete-time ACS on Z_16 (also Z_32, Z_64) with update functions chosen from {x^2, |x-8|}, whose transfer entropies are computed exactly from empirical distributions. Swapping which function is polynomial reverses the sign of Delta-I exactly (-1.499 to +1.499), confirming the ACS asymmetry theorem in exact arithmetic. *(T1 machine-verified exact; papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 2.4 (~line 677); also Riemann_Spectral_Critical_Line.tex sec 'Exact integer automaton')*
- **Geometric chirality from torsion** — The computational result that a spin Hamiltonian on discrete lattices with torsion-free geometry (T^a = 0) has spectral index exactly 0 at every size tested, while activating T^a != 0 produces a chiral spectral index scaling with lattice volume (|index|/N converging to about 0.30), consistent with the Atiyah-Singer index theorem for uniform torsion density. *(T3 numerical (exact integer Hamiltonian; eigenvalues via fp64); papers/Form_Function_and_Asymmetry.tex sec 8.1, lines 1180-1237)*
- **Gravitational ACS (Ashtekar pair)** — The identification of quantum gravity as an ACS with Form = the densitised triad E-tilde (spatial geometry) and Function = the Ashtekar connection A = Gamma + gamma*K (dynamics), whose three coupling orders are the three LQG constraints: Gauss (1st), diffeomorphism (2nd), Hamiltonian (3rd, the holonomy term). *(identification/claim; papers/Form_Function_and_Asymmetry.tex sec 10.1, lines 1898-1922)*
- **Layered resolution structure** — A strict hierarchy induced by the BCH expansion: Layer 0 base Forms (states, boundary data), Layer 1 Functions acting only on base Forms (torsion), Layer 2 brackets of Function pairs producing Forms (curvature), Layer 3 holonomy (Bianchi identity). The strict typing rule (a layer-n Function acts only on layers < n and produces a Form, never a Function) is claimed to block Goedelian self-reference. *(computationally checked (rank growth 2->3->5 in sl(4)); papers/Form_Function_and_Asymmetry.tex Remark rem:layers, lines 353-396)*
- **Predictions on record** — The corpus's list of standing falsifiable predictions: a 49 keV sterile neutrino, θ_QCD = 0 exactly, torsion coupling hierarchy 0:1:4, Higgs mass 124.72 GeV from the λ_φ chain, and the critical line as the unique center manifold (rotational stress-tensor flow at σ = ½). *(docs/ACS_Corpus_Map.md sec 7)*
- **Right locally, wrong globally (glass-box)** — The invariant that each analytical lens is valid in its scope but over-reaches when universalised. Held in FF06c and the newer papers. *(docs/ACS_Corpus_Map.md sec 2 INV-8)*
- **Self-resolving structure** — A structure containing an intrinsic measure mu(t) that becomes nonzero and is legible within the structure's own record whenever its information asymmetry begins to invert - detectable internally, not only by external observers. The Bianchi identity is given as the prototype. *(papers/core_trilogy/Holographic_Spectral_Inversion.tex sec 3.1, Definition 'Self-Resolving Structure' (def:self-resolving))*
- **SU(3)-not-in-O(4) theorem** — The no-go theorem that su(3) cannot embed in o(4): since dim su(3) = 8 > 6 = dim o(4) and su(3) is simple, the only homomorphism is the zero map, so the strong force cannot arise from the O(4) fiber structure alone. *(proved (dimension/simplicity argument); papers/Form_Function_and_Asymmetry.tex Theorem thm:no-su3 (label thm:su3-gap), lines 1754-1768)*
- **Tensegrity / nested codependence** — The invariant that zero modes of the rigidity matrix equal gauge freedoms, together with Menger-sponge-style self-similarity ('each cell carries the whole'). It holds in FF06b, FF06c, and AISO. *(docs/ACS_Corpus_Map.md sec 2 INV-6)*
- **Tensegrity atom** — A discrete Form-Function tensegrity system governed by the dimensionless stability ratio rho = alpha*gamma/(beta*kappa), stable when rho < 1 and unstable when rho > 1; Paper B casts the prime-zero system in this form. Note: Paper B attributes the definition to Paper A, which does not contain it (see presentation issues). *(definition referenced; source citation broken; papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 2.3 'The spectral stability ratio' and sec 'The prime-zero ACS as a tensegrity atom')*
- **Transfer entropy (TE)** — The directed information measure TE_l(X -> Y), a sum over conditional log-probability ratios quantifying how much X's past reduces uncertainty about Y's future beyond Y's own past. Applied to deterministic systems by equipping the ACS with a canonical invariant (SRB) measure; estimated from finite data by the Kraskov k-nearest-neighbour estimator. *(papers/Form_Function_and_Asymmetry.tex def:DI and sec 2.1, lines 222-240, 306-322)*
- **Wronskian bracket analysis** — Evaluation of the Wronskian W[phi_k, phi_j] = phi_k' phi_j - phi_j' phi_k of Riemann zero mode functions, interpreted as the 2nd-order ACS bracket in function space. All tested consecutive-pair Wronskians are non-zero, taken as evidence that the zero modes are non-commuting operators whose bracket implies combination frequencies gamma_k +/- gamma_j. *(T3 numerical; papers/Form_Function_and_Asymmetry.tex sec 4.2 lines 871-882 and sec 8.3 lines 1282-1307)*
- **Yang-Mills Abelian limit theorem (T3)** — The claim that symmetric coupling (f identical to g) gives Delta I = 0 and [f,g] = 0, corresponding to U(1) gauge theory with no self-coupling, while non-Abelian SU(N) gauge theory corresponds to f differing from g with non-zero bracket generating the self-interaction. *(proved (paper's own labelling); papers/Form_Function_and_Asymmetry.tex Theorem thm:YM-abelian lines 675-693; Appendix A 'Proof of Theorem 2.1 (T3)' lines 2181-2218)*


## Verification and governance vocabulary

The tier system, the kill/survive discipline, and the terms the corpus uses to police its own claims. Primary sources: `MANIFEST.md`, `docs/Elimination_Ledger.md`, `papers/later_FF06_series/The_Elimination_Ledger.tex`.

### 76-script ACS verification suite

The integration-test suite of 76 scripts in which each script corresponds to a specific theorem (T1-T21) or derived match (D1-D11); all 76 must pass before a release is cut, and Phase 0's exit criterion is that all pass under the new Form/Function typing.

**Source:** papers/ACS_Deterministic_AI_Stack_PDR.tex sec 5.1 Tier 2 lines 932-935 and sec 8.1  
**Also:** D1-D11, T1-T21, verification suite

### Engine kill-criterion (tomographic invariance)

The ledger's central discriminator: a quantity is a REFRACTION if its value moves under a legitimate change of instrument (representation, normalization, convention, scale, or window), and an INVARIANT (candidate) if it does not. It can be applied numerically by recomputing under an instrument swap (→ T1) or structurally by arguing from the quantity's construction (→ T2); the rule is 'tier honestly; never let (b) wear (a)'s clothes'.

**Source:** docs/Elimination_Ledger.md lines 14-23  
**Also:** collapse, instrument swap, kill condition, kill criteria, kill pass, kill target, kill test, kill-criterion, tomographic invariance

### False wall

A place where a result was asserted that the computation did not support - a falsified interpretation of a true computation, as distinct from a falsified conjecture. The Process Record catalogues six: the Python wall, the 62-orders-of-magnitude attribution, the compression claim, the biconditional (three times), 'FHE is the seam', and the seam as a binary void.

**Status:** definition-only; each wall documented and contracted  
**Source:** papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 5 (lines 198-264)

### Grade hierarchy (Theorem / Verification / Exploratory)

The stack's three-level classification of computational trust: TheoremGrade requires the exact SymPy backend, closure < 1e-14, and exhaustive Jacobi verification and may be cited as a theorem and added to the permanent constraint set; VerificationGrade (mpmath, < 1e-10) is strong numerical evidence and promotion candidate; ExploratoryGrade (NumPy, < 1e-6) is advisory only and never admitted to the constraint set.

**Status:** traced to 'Paper A sec C.2 epistemic tiers'  
**Source:** papers/ACS_Deterministic_AI_Stack_PDR.tex sec 3.6 and 6.2, lines 777-793 and 1007-1042  
**Also:** ExploratoryGrade, TheoremGrade, VerificationGrade, epistemic tiers

### Palatini → Pati-Salam pipeline

The framework's central derivation: the BCH expansion of [e, ω] on sl(4,ℝ) yields, order by order, the frame and connection, the Higgs bi-doublet (with quartic 2√3/27 and Yukawa ratio 2/3), the 12 Pati-Salam gauge bosons via the SU(3) closure attractor, and three generations via Jacobi truncation — deriving the gauge structure SU(4)_C × SU(2)_L × SU(2)_R and reducing the Standard Model's 19+ parameters to 6 inputs.

**Source:** docs/ACS_FRAMEWORK_SKILL.md sec 1 and sec 8  
**Also:** Paper A pipeline, Pati-Salam derivation

### Refraction

A quantity whose value moves under a legitimate change of instrument (representation / normalization / convention / scale / window), and which is therefore not a fundamental invariant. Precedent kill: 'universal 2π inversion' was representation-specific; later the bare values g₄ = 4/3, γ = 0.274, and λ_φ = 0.1283 were all machine-confirmed (T1) as refractions while the corresponding relations/ratios survived.

**Source:** docs/Elimination_Ledger.md lines 14-18 and OOS01 Q1 (lines 350-359)  
**Also:** INVARIANT (candidate), Invariant (candidate), Refraction vs invariant

### Scope boundary

An explicit statement of what a result DOES and DOES NOT claim, required for every result; some kill-test scripts enforce the boundary in-code ('scope boundary enforced in the script'). The skill's Section 5 lists five scope honesty standards that must always be stated (Coleman-Mandula rule, exceptional algebra boundary, Barbero-Immirzi gap, neutrino tension, tan β protection).

**Source:** docs/ACS_FRAMEWORK_SKILL.md sec 2 and sec 5; docs/Elimination_Ledger.md lines 483-487  
**Also:** scope honesty standards

### Strip-mine discipline

The target-selection rule of the Elimination Ledger: rank kill targets by expected-space-collapsed per unit cost, weighted toward kills aimed at the framework's own load-bearing claims. A landed kill credits the survivors by elimination — no proof required. Killed dead-ends are described as 'empty tunnels mapped'.

**Source:** docs/Elimination_Ledger.md lines 5-8, sec 'Continue the strip-mine'  
**Also:** empty-tunnel mapping, strip-mine

### tier map (T1-T4)

The framework's four-tier verification hierarchy, applied per claim and never promoted: T1 machine-verified (automated test passes, reproducible by running the code), T2 proved in paper, T3 numerically verified but not theorem-level, T4 explicitly falsified (recorded, not hidden). The I7 note ends with a per-claim tier map assigning T1 to its measured support rates and T4 to the failed 4/3 mechanism, with 'Section 9 chain as general theorem' marked not claimed.

**Status:** governance convention  
**Source:** papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex 'Tier map (MANIFEST)' (lines 258-274); tier definitions in MANIFEST.md lines 10-17  
**Also:** 4-tier honesty ledger, Epistemic tiers T1/T2/T3/T4, Four-tier verification hierarchy, Four-tier verification hierarchy (T1/T2/T3/T4), MANIFEST tier map, T1, T1 (machine-verified), T1 measured, T1-T4 hierarchy, T2 (proved in paper), T2 forced, T3, T3 (numerically verified), T3 conjecture, T4, T4 (explicitly falsified), T4 falsified, Tier 1, Tier 2, Tier 3, Tier 4, Tier discipline (T1-T4), Tier labels (T1/T3 as used in the seam note), explicitly falsified, four-tier verification hierarchy, four-tier verification ledger, machine-verified, numerically verified, proved in paper, repository tier discipline, result tiers, tier discipline, tier system

#### Supporting vocabulary

- **amplification with N** — The decisive check distinguishing real structure from a finite-size accident: a genuine function signal sharpens as the sample grows (z_arith 3,030 -> 11,497; z_lag1 51 -> 97 from N=2x10^4 to 10^5), whereas an artifact would be averaged down. *(T3 numerical (survived); papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex sec 3 (lines 92-98); also Prime_Carrier_Position_Form_Factor.tex robustness table (lines 118-133))*
- **apparatus band** — The band of disagreement (~0.08 in lag-1 units) between two independent legitimate GUE reference constructions (1/M size-extrapolation vs bulk-concatenation), induced purely by the choice of GUE pipeline. A candidate signal sitting inside the apparatus band is not claimed as a beyond-GUE finding; the lag-1 correlation falls in this band and is therefore explicitly not claimed beyond-GUE despite being formally FUNCTION. *(T3 numerical; papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex sec 5 'Does not establish' (line 124))*
- **Barbero-Immirzi parameter γ** — In ACS, γ ≈ 0.274067 is derived from the information-balance condition ΔI = 0 over the discrete spin area spectrum: Σ_j (2j+1)e^{−2πγ√(j(j+1))} = 1. The framework's scope note states this is the unconstrained (Meissner) value, while the physical value 0.2375 (Domagala-Lewandowski) requires the SU(2) Gauss constraint via Chern-Simons projection; the Elimination Ledger killed the bare value 0.274 as a prescription-dependent refraction (T1: it becomes 0.190206 under SO(3)/integer counting). *(KILLED as bare value (REFRACTION, T1); structural invariant is 'fixed γ once a prescription is fixed'; docs/ACS_Technical_Whitepaper.md sec 2.3; docs/ACS_FRAMEWORK_SKILL.md sec 5.3; docs/Elimination_Ledger.md lines 99-107 and 353)*
- **canonical seed 20260423** — The fixed random seed used across the FF06 spectral suites so that every surrogate ensemble, shuffle, and measurement is reproducible standalone; it is quoted in the reproducibility footers of FF06e, FF06f, FF06g, and FF06h. *(convention; papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex line 71 and footer line 130; Form_Function_Relativity.tex line 118)*
- **Cantor corner** — The cell of the 2x2 square that is non-homomorphic but injective - identity kept, structure scrambled. On the critical line, the reflection s -> 1-s occupies this corner (injective, non-homomorphic, fixed locus Re = 0.5). *(T1 classification; papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 9.1-9.2 (lines 431-440))*
- **chain support decision rule** — The float-suite criterion for declaring the Section 9 chain supported in a tested cell: corr(gap, xi) < -0.2 and corr(gap, leak_proxy) < -0.2 for every required leakage proxy. Support rates against this rule were 0/12 (TFIM exhaustive), 1/12 (cross-model combined), 5/12 (long-range combined, concentrated at the smallest leakage threshold 1e-3). *(T1 (support rates machine-verified); papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex sec 3.1 (lines 108-111) and secs 4.1-4.2)*
- **Closure Validator** — The stack component enforcing the closure attractor principle: every output must satisfy D(output) < epsilon for the closure defect functional, with standard thresholds 1e-14 (exact SymPy), 1e-10 (mpmath), and 1e-6 (NumPy, advisory only). *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 3.4, lines 622-685)*
- **Codependence invariant** — The type-system rule that all data in the stack is classified as either Form (state) or Function (operator) and a value cannot simultaneously inhabit both categories; enforced by Pydantic at runtime and mypy statically. *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 2.2 Layer 1, lines 336-341)*
- **Coleman-Mandula rule (scope standard)** — The mandatory scope note that the N2 grading selection theorem selects a grading of the internal carrier space, NOT of physical spacetime; any discussion connecting the (3,1) grading to Lorentzian signature must include the Coleman-Mandula constraint and the three bridging mechanisms (soldering, pre-geometry, CM evasion). 'This is never optional.' *(docs/ACS_FRAMEWORK_SKILL.md sec 5.1)*
- **DAG journal** — The append-only, content-addressed record of every bracket computation: nodes are immutable Forms, edges are Functions labelled with BCH order, each edge hashed over (source_hash, function_name, order), forming a Merkle DAG with checkpoints every 1024 entries and a two-phase-commit protocol guaranteeing journal-before-return. *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 4.1 lines 800-822 and 5.3 lines 958-982)*
- **Delta I Monitor** — The stack component that detects convergence via information balance: it computes Delta I = TE(F -> Phi) - TE(Phi -> F) over a trailing window of Forms (Kraskov-Stoegbauer-Grassberger estimator) and halts the engine when |Delta I| < epsilon over the last 8 steps, among other halting conditions. *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 3.5, lines 687-733)*
- **Deterministic AI Stack** — The engineering/trust substrate of the framework (whitepaper's 'Paper D'; the corpus map's AISO entry): a deterministic AI governance model run by the constraint-attractor cycle, with routing driven by a bounded ΔI scalar. Related artifacts include the AISO 'Full-Stack Design Invariables + TENT v10' living document and the TENT/CDCL routing scalar delta_i() ∈ [0,1]. *(docs/ACS_Technical_Whitepaper.md sec 5; docs/ACS_Corpus_Map.md sec 1 (AISO row); docs/Elimination_Ledger.md line 228)*
- **False-fit mode** — The second guarded failure mode: a structural resemblance between a mathematical object and a target system mistaken for an operational identity ('we have a Cantor pairing in the build, so the criterion applies'). Four such fits were proposed against the live engineering stack; four were false; the fifth (motif memory) was the first to survive. *(definition-only; instances T4; papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 1 (lines 77-81))*
- **FF06 series** — The corpus's paper-ID scheme: FF06a (Colour from Gravity / Palatini), FF06b (Riemann Spectral ACS) and its refinement FF06b', FF06c (Holographic Spectral Inversion), FF06-N3 (prime-gap transition operator note), FF06e (shuffle knife), FF06f (three-layer decomposition), FF06g (Form/Function relativity), FF06h (scaled invariance of ∞/0), plus a later_FF06_series of eight June methodology/geometry papers and FF06Σ (a linking document whose Link 3 asserted ΔI = c-function). *(docs/ACS_Corpus_Map.md sec 1; MANIFEST.md papers table)*
- **FF06 series designations (FF06e-FF06h)** — The paper-series identifiers for the methodology sequence: FF06e = Spectral Rigidity and Shuffled Spacing Discriminant (shuffle knife), FF06f = Prime Carrier / Position Form Factor, FF06g = Form/Function Relativity, FF06h = Scaled Invariance of Infinity and Zero; each later paper cites its predecessors by these codes. The Issue #7 diagnostic note carries the report ID TR-2026-FF06-I7. *(naming convention; papers/README.md lines 41-44; Form_Function_Relativity.tex line 43; Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex line 37)*
- **First-class negative** — The bundle's discipline of reporting negative or unresolved measurements with the same prominence as positive ones ('negatives first-class', 'Reported as a negative, not spun'); the exemplar is the rung-2 phase magnitude that stayed at the demodulation noise floor and did not improve with more L-zeros. *(papers/notes/Critical_Line_As_Fibered_Object.tex abstract (line 64) and sec 6, lines 250-255)*
- **Fresh-eyes note** — A dated corrective annotation added on re-review so the bundle does not overstate a result. Example: the N3 fresh-eyes note (2026-06-27) records that the transition operator's eigenvalues are bounded dynamical modes, not an unbounded spectrum claimed to be the Riemann zeros, and that its L-function connection is via the kernel (characters), not the eigenvalues. *(MANIFEST.md N3 fresh-eyes note (lines 105-108))*
- **Gauntlet grades (HIT / SPLIT / DOWNGRADED / FALSE FIT)** — The grading scheme of the adversarial gauntlet in When a Number Lies: HIT means the relation wins; SPLIT means the multiplicative part wins while the additive part is the wall; DOWNGRADED means an existing method already wins; FALSE FIT means there is no hidden relation and the scalar is the datum. *(papers/later_FF06_series/When_a_Number_Lies.tex sec 3 (lines 86-107))*
- **Governance Policy Engine** — The stack's policy plane implementing the constraint-attractor cycle: every output is run against declarative, version-controlled policy constraints and attractor tests; outputs satisfying the attractor criteria are promoted to constraints for subsequent computations (the inversion arc as code). *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 3.6 lines 735-793 and sec 6.4)*
- **Grading selection theorem (N2)** — Note N2's general theorem that minimizing adjoint spectral activity (the functional S̃_g[P] = Tr(σ_P · g(ad_T)) with g(0) = 0) selects the (3,1) grading for T_{B−L}, proved via bilinearity in magnetizations and reduction to weighted max-cut. It holds for classical Lie algebra types (A, B, C, D) and fails for exceptional algebras — the G₂ counterexample is proved (multi-length root clusters break the bilinear factorization). *(T2 (theorem + G₂ counterexample); docs/ACS_FRAMEWORK_SKILL.md sec 4.3 item 10, sec 5.2, sec 9 item 4; MANIFEST.md Notes table (lines 100-101))*
- **g₄ = g_L = g_R = 4/3** — The locked gauge-coupling equality from the Palatini bracket (Casimir C₂ = 4/3). The kill test SPLIT it: the bare value 4/3 is a generator-normalization-dependent refraction (T1: it becomes 2/3 under a trace-normalization rescaling), while the equality of the three couplings in one shared normalization survives as the invariant — the Pati-Salam coupling-unification content. *(SPLIT (relation INVARIANT, value REFRACTION, T1); docs/ACS_Corpus_Map.md sec 2; docs/Elimination_Ledger.md lines 88-97 and 352)*
- **Hilbert-Pólya wall** — The quantified obstruction to constructing the Hilbert-Pólya operator: any H with spectrum {γ} must simultaneously carry real orbit amplitudes (|Im W|/|Re W| = 0.0001, T-even → β=1) AND GUE repulsion (measured β=2.00 → T-broken) — two constraints pulling to opposite symmetry classes, which is why the problem is open. Stated as measured numbers, not a slogan. *(T1 (constructs no operator); MANIFEST.md Paper B table (line 75))*
- **HP knife suite** — The falsification/calibration instrument suite (code/hp_knife_suite/) for the Hilbert-Pólya program: it numerically exhibits the explicit formula and its Dirichlet generalization (known theorems), tests witnesses, harmonic ladders, and character twists on 100k Riemann zeros and generated L-function zeros. Its stated scope: it is an instrument, not a source of new theorems, and constructs no operator. *(MANIFEST.md Paper B section and scope note (lines 59-87))*
- **Hypercone projection (hypercone-through-the-slice)** — The survived picture that the 15-dim sl(4) cloud is the object and experience is a slice through which a higher-dimensional cone appears as evolving spheroids/hyperbolae. Its locked content: the level-repulsion exponent β is a dimension counter, β = codim − 1, and the 100k Riemann zeros' measured β = 2.019 selects the codimension-3 chirality class. Scope boundary: the cone is in parameter space, not physical space. *(SURVIVED (C1, C2 T1 exact; C3 T3 measured); docs/Elimination_Ledger.md 2026-07-17 (lines 488-514))*
- **h̃/h = 2/3 (Yukawa ratio)** — The locked Yukawa coupling ratio from the Koide mechanism, a dimensionless, normalization-cancelling, RG-invariant ratio. It is the only one of the four locked constants to fully survive the invariant-or-refraction kill test, upgraded to T1 INVARIANT after machine confirmation that d/d(lnμ)(h̃/h) ≈ 0. *(SURVIVED / INVARIANT (T1); docs/ACS_Corpus_Map.md sec 2; docs/Elimination_Ledger.md lines 109-116 and 355)*
- **Kernel invariant** — The requirement that the three interchangeable arithmetic backends (SymPy exact rationals, mpmath arbitrary precision, NumPy fp64) produce bit-identical results for any computation representable in their common domain, checked at every build. *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 2.2 Layer 0, lines 328-334)*
- **Killing-orthogonality** — Paper C's boundary condition (Thm 4.1): the boundary state space is defined as the orthogonal complement of the bulk gauge orbit under the Lie algebra Killing form, g_boundary = g_bulk^⊥, with B([X,Y], Z) = 0 for all bulk Z. The whitepaper presents this as enforcing the ER=EPR holographic correspondence via the algebra's radical. *(T2 (Thm 4.1); ER=EPR correspondence itself T2/T3 and listed as an open problem; docs/ACS_Technical_Whitepaper.md sec 4.1; MANIFEST.md Paper C table (line 92))*
- **Ledger status tags** — The status vocabulary of Elimination Ledger targets: QUEUED / IN-PROGRESS / KILLED / SURVIVED / SPLIT / BLOCKED. SPLIT records a claim that divides into an invariant part and a refraction part; BLOCKED marks a target waiting on inputs or constructions rather than on swings. *(docs/Elimination_Ledger.md line 12 and REMAINING table (lines 308-317))*
- **N_gen = 3 (Jacobi truncation)** — The prediction that exactly three fermion generations arise because the Jacobi identity truncates the BCH expansion at order 3 (order 4+ vanishes; ‖Jacobi‖ = 0 exact); no fourth generation. *(T1; docs/ACS_Corpus_Map.md sec 2 and sec 4; MANIFEST.md Paper A table (line 53))*
- **OOS01** — The label for an out-of-session batch of results ('OOS01 RESULTS (2026-06-06, Mac via Antigravity)') run on another machine/agent, reviewed and re-tiered in the Elimination Ledger — it upgraded the four framework-constant verdicts to T1, killed the BRA speed claim, and corrected the Q4 ΔI-reading. The label itself is never expanded or defined in the documentation. *(docs/Elimination_Ledger.md line 320)*
- **Parameter ledger** — The bookkeeping table of the gauge sector's inputs: free parameters (tan β, ρ_Δ, α₁, v_R, μ_Δ), two calibrations (m_τ and v = 246.22 GeV), and the locked, algebraically fixed quantities (λ_φ, h̃/h, g₄, 2ρ₁+ρ₂, N_gen, γ, α₂ = 0, β_c = 0) — the claimed reduction from the SM's 19+ parameters. *(docs/ACS_FRAMEWORK_SKILL.md sec 4.2; docs/ACS_Corpus_Map.md sec 3)*
- **PASS_WITH_CAUTION** — The end-to-end verification pipeline status for Issue #7: all scripts exit successfully with zero stdout-vs-JSON consistency errors and zero documentation hash-check failures, with caution retained only because the float NumPy Section 9 scripts remain anchored to a single platform. *(pipeline status label; papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex sec 4.6 (lines 197-201) and Conclusion (line 255))*
- **Prime-gap transition operator P_m (N3)** — The dynamical transition operator over prime gap ensembles on (Z/mZ)* studied in Note N3; its kernel law dim ker(P) = φ(m) holds with no excess across all 14 tested moduli, and the kernel consists of Dirichlet characters. Per the fresh-eyes note, its eigenvalues are bounded dynamical modes (|λ| ≈ 0.01-0.3), not the Riemann zeros. *(T1/T3; the uniform-X conjecture for N3 falsified (F-13); docs/ACS_Corpus_Map.md sec 1 and sec 4 (N3 rows); MANIFEST.md Notes table (line 102) and fresh-eyes note)*
- **RC1 scope** — A recurring remark label in the P_alpha notes marking the claim-discipline boundary of each result: P_model quantities are documented geometric/structural proxies, per-isotope S_i is diagnostic only, and no uniqueness of many-body preformation is claimed. The acronym RC1 is never expanded in these notes. *(scope discipline label; papers/notes/Flag_Condensate_Palpha_Overlap.tex Remark 'RC1 scope' (line 81); papers/notes/Flag_Condensate_Palpha_Refined.tex Remark 'RC1 scope')*
- **Receipt** — A cryptographic record of a computation sufficient for independent replay, carrying input hashes, library hashes, grade, policy version, and timing bounds; re-execution with the same receipt must produce byte-identical output or the receipt is invalidated. *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 4.4 lines 906-909 and Glossary)*
- **Reproducibility envelope** — The explicit conditions under which a stack computation is reproducible: content-addressed inputs, hash-pinned library versions, TheoremGrade or VerificationGrade computation, and completion within the BCH-3 envelope with no unbounded loops. *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 4.4, lines 887-909)*
- **Result hierarchy** — The explicit tier-classification table recording the epistemic status of every claim in the prime-gap note — verified empirical laws, fitted scalings, phenomenological closures, and the three falsified conjectures — used 'to make the epistemic status of the various claims explicit'. *(papers/notes/Prime_Gap_Transition_Operator.tex sec 8.1, lines 299-318)*
- **Seed convention 20260423** — The fixed random seed (20260423) used throughout the corpus for reproducibility of every stochastic computation. *(docs/Elimination_Ledger.md line 10; MANIFEST.md Reproduction notes (line 119))*
- **SIP License v1.1** — The Sovereign Integrity Protocol License under which every paper in the series is 'co-governed and enforced'; cited in each paper's date line and footer with the canonical URL github.com/tensorrent/ACS-Framework/blob/main/LICENSE. *(governance convention; papers/methodology/Form_Function_Relativity.tex lines 1-2; Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex License section (lines 61-64))*
- **Sovereign Integrity Protocol License (SIP License)** — The license under which every trilogy source file declares itself 'co-governed and enforced', pointing to the LICENSE file of the tensorrent/ACS-Framework GitHub repository. *(governance term; papers/core_trilogy/Palatini_Gauge_Attractor.tex line 1 (identical header in all four papers))*
- **spacing floor / shuffle floor** — The residual prime-resonance power measured after a random permutation of the spacings (preserving only the one-point spacing distribution), averaged over hundreds of permutations; the baseline-to-floor separation grows from 18x at N=200 to 474x at N=10^4 and serves as the null level against which the prime signal is scored. *(T3 numerical (noted as O(10)-to-O(100) growth, not last-digit reproducible); papers/methodology/Prime_Carrier_Position_Form_Factor.tex sec 2 (line 64) and robustness table (lines 118-133))*
- **Spectroscopic factor S** — A multiplicative scale on the overlap proxy, P_S = S * P_model. Variants across the P_alpha notes: one global S_star fitted to match mean extracted preformation (~2.7e-2 flat, ~3.18e-2 throat+WS; reduces RMS to ~0.82 without changing correlation); per-isotope S_i (tautological, diagnostic only); and predictive parametric fits log10 S(A,Z) and log10 S(R) evaluated with leave-one-out. *(T3; parametric S(A,Z) LOO RMS = 0.2862 on the original 14, degrading to 1.355 on n=29; papers/notes/Flag_Condensate_Palpha_Overlap.tex sec 2.3; papers/notes/Flag_Condensate_Palpha_Refined.tex sec 3)*
- **StrickenBy** — An annotation convention marking a superseded ledger entry with the correction ID and date (e.g. 'StrickenBy{C1.4-D1, 2026-07-06}'), used when parameters were relocated (α₂ and β_c moved from free to Locked) while keeping the audit trail visible. *(docs/ACS_FRAMEWORK_SKILL.md sec 4.2 note (line 96))*
- **Sycophantic mode** — One of the two guarded failure modes: a result feels validated because a collaborator - human or machine - agreed with it, rather than because it was tested. The program began, fifteen months earlier, in exactly this failure, and naming it was the precondition for everything that followed. *(definition-only; two origin artifacts retested and T4; papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 1 (lines 72-76); Monograph sec 1.2)*
- **T1 upgrade path** — The documented route by which a structural T2 verdict can be promoted to machine-verified T1 — e.g. rerunning the actual ACS derivation under a representation/normalization swap and checking whether the number moves, or integrating RGEs to confirm d/d(lnμ)(h̃/h) ≈ 0. Each structural kill entry states its own upgrade path. *(docs/Elimination_Ledger.md method note (lines 79-86) and h̃/h entry (lines 109-116))*
- **T_min height floor (2πe)^d/q** — The claimed lowest height at which L-function zeros can be resolved, scaling as (2πe)^d/q in degree d and conductor q (the LF01 correction). The floor value 2πe at d=1, q=1 is an analytic invariant (the exact zero of the Riemann-von Mangoldt main term), but the scaling law was falsified (T4) at d=2: the true floor scales as 2πe·q^{−1/d}, and the framework formula overshoots by ~8.5× on the Dedekind zeta of Q(i). *(d=1 floor SURVIVED (T2/T3); scaling law FALSIFIED (T4); docs/Elimination_Ledger.md Q3 entries (lines 141-165, 395-423); docs/ACS_FRAMEWORK_SKILL.md sec 4.4 item 9)*
- **tan β gauge-protected flat direction** — The negative result that the bi-doublet VEV ratio tan β cannot be fixed perturbatively in the minimal sector: the Pati-Salam gauge structure protects it via three independent arguments (h̃/h is an RG invariant, two-loop QCD is multiplicative, thresholds are β-independent). The skill stresses this is NOT 'we couldn't fix it' but a structural protection; the attempted Coleman-Weinberg 6→5 parameter reduction is falsified (T4). *(CW 6→5 reduction T4 (falsified); protection argument T2; docs/ACS_FRAMEWORK_SKILL.md sec 5.5 and sec 4.4 item 8; MANIFEST.md Paper A table (line 52))*
- **Three-tier verification model** — The stack's layered verification: Tier 0 type-level checks (mypy, Pydantic, invariant assertions), Tier 1 unit verification of apply/bracket_with/killing_form against golden values and structure constants, Tier 2 theorem verification via the 76-script suite as integration tests. Note these tiers are distinct from the T1-T4 theorem labels of the physics papers. *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 5.1, lines 916-935)*
- **Vacuity guard** — The requirement that the target structure of the homomorphism criterion be pre-specified and independently meaningful: 'injective homomorphism into some structure' is empty, since any bijection is an isomorphism onto the operation transported through it. This guard was forced when the 'into some structure' form of the criterion was caught as vacuous. *(the unguarded form is T4 (vacuous); papers/later_FF06_series/The_Reversible_Flattening_Monograph.tex sec 3 Criterion 3.1 (lines 127-132))*
- **Witness (spectral witness)** — A test statistic evaluated on the real zero sequence versus surrogate nulls to classify structure as Form or Function — e.g. spacing, counting, shape, lag-1, and arithmetic prime-resonance witnesses. FF06e finds the witness set has effective rank 4, and the vantage-point analysis finds exactly two robust FUNCTION faces (arithmetic ~830σ and local-order ~26σ). *(docs/ACS_Corpus_Map.md sec 4 (FF06e rows); MANIFEST.md Paper B table (line 73))*
- **ΔI ≡ c-function (FF06Σ Link 3)** — The killed conjecture that ΔI is identically the RG c-function (not an analogy). The ledger closed every reading: under the framework's literal transfer-entropy-asymmetry definition the identity is false/ill-defined (sign, fixed-point value, and category mismatches; TE undefined on a static ground state), and under the mutual-information reading it is a restatement of the Casini-Huerta entropic c-theorem — no reading is both novel and true. *(Identity FALSIFIED as stated (T2); monotonicity analogy holds only as the known theorem (T1/T2); target retired; docs/Elimination_Ledger.md Q4 entries (lines 221-267, 333-348, 375-393))*
- **λ_φ = 2√3/27 (Higgs quartic)** — The locked Higgs quartic coupling value ≈ 0.1283 derived by Koide projection (T2 in the MANIFEST claim table), matching experiment (0.129) to 0.84% and chaining to a Higgs mass prediction of 124.72 GeV. The Elimination Ledger later split the claim — the bare number is a refraction under Killing-form normalization (T1), while the Koide-geometric origin is the invariant candidate — and found the physical identification scale-relative (crossing the running quartic near μ ~ 132 GeV). *(T2 derivation; bare value REFRACTION (T1); SPLIT verdict; docs/ACS_Technical_Whitepaper.md sec 2.3; docs/Elimination_Ledger.md lines 118-127 and 354)*


## The gauge-gravity program (Paper A)

Objects and results of the Palatini-gravity arm: gauge-group selection, the closure attractor, and the derived physical parameters. Primary source: `papers/core_trilogy/Palatini_Gauge_Attractor.tex`.

### Barbero-Immirzi from information balance

The derivation of the Barbero-Immirzi parameter from the ACS balance condition Delta-I = 0 at a black-hole horizon, yielding the partition-function equation Z(gamma) = sum_j (2j+1) exp(-2*pi*gamma*sqrt(j(j+1))) = 1 with solution gamma = 0.274, matching Meissner's value. The Domagala-Lewandowski value 0.2375 is identified as the Gauss-constrained balance; reproducing it exactly requires SU(2)_k Chern-Simons counting and remains open.

**Status:** derived + numerical; exact DL value open  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 5.2, Theorem 'Barbero-Immirzi from information balance' (thm:BI, ~line 1580)  
**Also:** BI balance condition, gamma = 0.274, gamma_ACS = 0.274

### BCH-TE morphism

The lemma that the transfer-entropy asymmetry expands as Delta-I(eps) = eps<f-g, grad log dmu/dnu> + 2 eps^2 <[f,g], grad log dmu/dnu> + O(eps^3), so the Lie bracket [f,g] is the exact second-order Taylor coefficient of Delta-I. Proved for smooth vector fields on compact M via the Cartan formula [L_f, L_g] = L_[f,g]; the extension to infinite-dimensional Palatini field space is explicitly conjectured, not proved.

**Status:** proved for finite-dimensional compact M (symbolically verified); infinite-dimensional case conjecture  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 2.3, Lemma 'BCH-TE morphism' (lem:bch-te, ~line 551)  
**Also:** BCH-transfer-entropy morphism, BCH–Transfer-Entropy morphism, INV-2, Lemma 2.9 (as hardcoded in Appendix B)

### Chirality map J

The linear map J(T) = i*sym(T) + anti(T) on sl(4,R), which multiplies the symmetric (torsion-sector) part of a generator by i while leaving the antisymmetric (Lorentz-sector) part unchanged. By Cartan's classification it is the unique such map (up to scaling and inner automorphisms) carrying sl(3,R) to the compact real form su(3); all 28 output brackets close and all generators are skew-Hermitian.

**Status:** proved via Cartan classification plus grid-scan verification  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 4.3, Proposition 'Chirality uniqueness and complexification' (prop:chirality, ~line 1095)  
**Also:** J(T) = i sym(T) + anti(T), J-map, chirality uniqueness, sl(3,R) → su(3) map

### Closure attractor

The claim that sl(3,R) is the unique 8-dimensional subspace of sl(4,R) achieving numerically exact bracket closure (D < 1e-14), against 50,000 uniformly sampled 8-dimensional subspaces all with D > 0.49. The paper explicitly flags this as a numerical observation, not a classification theorem, though it is consistent with Dynkin's classification of maximal subalgebras.

**Status:** T3 numerical observation, consistent with algebraic classification  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 4.3 (prop:selection ~line 1038; rem:uniqueness ~line 1069)  
**Also:** 5+3 split, 6+3 split, SU(3) attractor, SU(3) closure attractor, closure attractor uniqueness, colour skeleton, selection principle, sl(3,R) closure, sl(3,R) embedding (colour skeleton)

### Closure defect functional D(V)

For a k-dimensional subspace V of a Lie algebra with basis {T_i}, D(V) is the normalised residual sum ||[T_i,T_j] - Pi_V([T_i,T_j])|| / sum ||[T_i,T_j]||, measuring how far V falls short of closing under the bracket. It is the quantity the AI stack's Closure Validator enforces below threshold.

**Source:** papers/Form_Function_and_Asymmetry.tex Proposition prop:selection, lines 1525-1544; papers/ACS_Deterministic_AI_Stack_PDR.tex sec 3.4 and Glossary  
**Also:** D(V), closure defect

### Colour charges as torsion Cartan eigenvalues

The identification of the three QCD colour charges with the eigenvalues of the Cartan generators H1 = diag(1,-1,0,0) and H2 = diag(0,1,-1,0), both of which sit in the torsion sector of the Palatini decomposition; the fourth, colourless 'White' state at the origin is identified with the lepton. Colour quantum numbers thereby measure how vierbein and spin connection couple at each spacetime point.

**Status:** exact algebra plus interpretation  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 4.4 (~line 1172)  
**Also:** Red/Blue/Green/White geometric colour

### Delta-I (information-asymmetry functional)

For two mutually constraining fields f, g, the net information one carries about the other, defined as the transfer-entropy asymmetry Delta-I = TE(F -> G) - TE(G -> F) (Link 1 of the identity chain, a definition, not a result). A separate reachable definition in the AISO stack is a bounded routing scalar delta_i in [0,1] built from consistency, divergence, late-error, and recomposition weights.

**Status:** definitional (Link 1)  
**Source:** papers/later_FF06_series/One_Mechanism_Many_Forms_Sigma.tex sec 2 Link 1 (lines 102-105); The_Elimination_Ledger.tex sec 4.2 (lines 245-249)  
**Also:** DI, Delta I, INV-1, Information asymmetry (Delta-I), asymmetric transfer entropy, delta I, information asymmetry, net transfer entropy, the asymmetry, transfer-entropy asymmetry, ΔI, ΔI (net transfer entropy)

### Dimensional devolution

The inversion of the micro-to-macro picture: the fundamental object is the full 15-dimensional sl(4) fiber and particles are projections onto 3+1 observation space, via the compression sequence sl(4)[15D] -> su(3)[8D] -> Cartan[2D] -> singlet[0D]. Perceived quantum randomness or chaos is claimed to be the 'resolution bias' of sampling a high-dimensional ordered structure with a low-dimensional detector, with a stated testable consequence (order returns as dimensions are restored).

**Status:** T3 numerical (projection autocorrelation 0.95 -> 0.23) plus conjecture  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 6.7 'Dimensional devolution' (~line 2187); also Holographic_Spectral_Inversion.tex appendix A.3

### Geometric see-saw

The ACS neutrino-mass mechanism: the right-handed neutrino couples only through torsion, an extra BCH order plus the B-L colour-singlet trace gives Dirac mass m_D = m_e^2/(3 m_tau) ~ 49 eV, and the Type-I see-saw yields the product formula m_nu x M_R = m_e^4/(9 m_tau^2) ~ 2400 eV^2 (verified to 0.1%). With observed m_nu ~ 0.049 eV this predicts a falsifiable M_R ~ 49 keV sterile neutrino with X-ray decay line at 24.5 keV; the relic abundance is explicitly excluded from the prediction.

**Status:** falsifiable prediction; three of four suppression factors derived  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 6.3 (~line 1882) and Appendix B  
**Also:** 49 keV sterile neutrino, see-saw product formula

### Koide projection

The result that the squared cosine of the angle between the symmetric channel of the 3rd-order holonomy and the B-L direction equals exactly 2/3 (to 1e-16) - the Koide ratio - and, normalised through the sl(4) Killing form K(T_BL,T_BL)=32/3, fixes the Higgs quartic lambda = 2*sqrt(3)/27 = 0.1283 and m_H = 124.7 GeV (observed 125.25, 0.42%). The paper labels the epistemic status 'partial derivation': the projection factors are exact but the Killing-to-canonical-kinetic normalisation chain carries the 0.85% residual.

**Status:** partial derivation; 0.85% residual unexplained  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 6.5 (eq:koide-projection, eq:higgs-quartic, ~line 1978)  
**Also:** Higgs quartic lambda = 2*sqrt(3)/27, Koide ratio, Q = 2/3 projection

### Koide-Cabibbo relation

The claim that the Koide mass-hierarchy angle of the charged leptons is not free but equals arctan of the Wolfenstein parameter: tan(theta0) = lambda_W = sin(theta_Cabibbo), giving 12.76 degrees vs. observed 12.73 (0.23%, within 0.7 sigma of PDG), and shown to be RG-invariant at 1 loop.

**Status:** numerical match, RG-checked; explicitly falsifiable  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 6.1 (eq:koide-cabibbo, ~line 1806)  
**Also:** tan(theta0) = lambda_Wolfenstein

### Palatini decomposition (torsion sector / Lorentz sector)

The split of the asymmetry-map image sl(4) into a 6-dimensional Lorentz sector [o(4),o(4)] (connection self-bracket = curvature) and a 9-dimensional torsion sector [Sym0(4), o(4)] (metric-connection bracket). The colour algebra sl(3,R) distributes 5+3 across the two sectors, so colour is 'irreducibly distributed across both ACS coupling orders'.

**Status:** exact symbolic computation over Q  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 4.2, Proposition 'Palatini decomposition of the asymmetry map' (prop:palatini-decomp, ~line 962)  
**Also:** 6+9 decomposition, Lorentz sector, Palatini decomposition (Lorentz sector + torsion sector), torsion sector

### Self-pruning of the bi-doublet Higgs sector

Three consistency filters that eliminate couplings of the minimal Pati-Salam bi-doublet Higgs potential without fitting: Phase 50 - alpha_2 is forbidden by representation theory (the bi-doublet is an SU(4) singlet so Tr(Phi-dagger T^A Phi) = 0); Phase 51 - a nonzero beta_c at tree level forces tan(beta) = +/-1; Phase 52 - equal VEVs force M_u = +/-M_d hence V_CKM = 1, contradicting observed mixing, so beta_c = 0 at tree level or the sector must be extended.

**Status:** proved (representation theory / extremisation / no-go identity)  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 6.5.1 'Self-pruning of the bi-doublet Higgs sector' (sec:self-pruning, ~line 2027)  
**Also:** Phase 50, Phase 51, Phase 52, three independent filters

### Three generations from Jacobi truncation

The claim that the Jacobi identity closes the BCH algebra at exactly order 3 (no algebraically independent 4th-order bracket, verified to 6e-15), and each BCH order generates one copy of the fermion representation, giving exactly three Standard Model generations.

**Status:** algebraic truncation verified; field-theoretic mapping to families explicitly not yet derived (Paper C, gaps list)  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 4.7 item (iii-b) (~line 1480)

### Torsion coupling hierarchy

The classification of all 15 sl(4,R) generators by the torsion-VEV coupling ||[T_{B-L}, X]||^2: 9 Tier-0 generators (Cartans and within-colour rotations/boosts) with zero coupling, and 6 Tier-2 colour-lepton generators with coupling exactly 32/9. The abstract states the resulting coupling hierarchy as 0:1:4.

**Status:** exact rational arithmetic (Paper C lists it as theorem)  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex appendix sec 'Torsion coupling hierarchy and vacuum energy cancellation' (sec:torsion-hierarchy, ~line 2610)  
**Also:** 0:1:4 hierarchy, Tier 0, Tier 2

### Two-stage selection mechanism

The claim that su(3) emerges by two irreducible mechanisms: (1) algebraic closure selects sl(3,R) as the unique 8-dimensional attractor in sl(4,R); (2) spinorial chirality completes it to su(3) via the uniquely determined chirality map. Neither works alone: closure without chirality gives only the non-compact split form; chirality without closure gives no algebra.

**Status:** established per the two propositions it cites; final dynamical identification open  
**Source:** papers/Form_Function_and_Asymmetry.tex Remark rem:two-stage, lines 1596-1613

### Vacuum energy cancellation (Palatini pairing)

The theorem that the torsion-weighted bosonic vacuum energy sum over sl(4), sum_X ||[T_{B-L},X]||^2 * K(X,X), cancels exactly: each Tier-2 antisymmetric generator with Killing form -16 is paired with a symmetric partner at +16 and identical torsion coupling. Explicitly not supersymmetry but Form-Function pairing; the paper scopes it as removing only the Planck-scale bosonic contribution, reducing the cosmological-constant problem from 10^121 to ~10^55 orders.

**Status:** proved in exact rational arithmetic; scope limits stated  
**Source:** papers/core_trilogy/Palatini_Gauge_Attractor.tex appendix sec:torsion-hierarchy (~line 2650)

#### Supporting vocabulary

- **Branch A / Branch B** — The two Higgs-sector architectures of the framework: Branch A is the minimal Pati-Salam bi-doublet, whose parameter ledger after self-pruning has 6 irreducible inputs (4 free + 2 calibrations) versus the SM's 19+; Branch B extends the sector with Sigma ~ (15,1,1), reopening the three exclusions at the cost of an extra parameter. *(definition-only / ledger; papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 6.5.1, Table 'Branch A parameter ledger' (tab:branch-A-ledger, ~line 2147))*
- **Cabibbo chain** — The identity chain sqrt(m_d/m_s) ~ lambda_W = sin(theta_C) = tan(theta0_Koide): a down-quark mass ratio, a quark mixing angle, and a lepton mass parameter are claimed to be three manifestations of one bracket projection of T_{B-L} onto the 1st/2nd-generation subspace of SU(4) (match to 1.3%). *(T3 numerical; papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 6.1 (eq:cabibbo-chain, ~line 1833))*
- **Confinement as ACS attractor** — The reading of colour confinement as the statement that the only long-distance-observable states sit at the Delta-I = 0 attractor in the colour sector: the colour singlet has zero eigenvalue under both torsion Cartan generators, and the QCD vacuum screens any Delta-I != 0 (unconfined colour) state by pair creation until a singlet forms. *(interpretation/conjecture; papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 4.4, Remark 'Confinement as ACS attractor' (~line 1233))*
- **Gravitational ACS** — Quantum gravity cast as an ACS with Form = densitised triad E-tilde (spatial geometry) and Function = Ashtekar connection A = Gamma + gamma*K (dynamics), whose three coupling orders map onto the Gauss, diffeomorphism, and Hamiltonian constraints of loop quantum gravity, the Hamiltonian constraint being the 3rd-order holonomy term. *(definition-only plus structural mapping; papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 5.1, Definition 'Gravitational ACS' (~line 1550))*
- **Ricci flow as ACS dynamics** — The interpretation of Hamilton's Ricci flow dg/dt = -2 R_mu-nu as the metric evolving to reduce the 2nd-order information asymmetry, with the Ricci scalar read as the trace of the 2nd-order BCH-TE coefficient; the Einstein-space attractor is the state of uniform Delta-I across the manifold. Verified numerically by a 41x curvature-variance reduction in a bumpy-sphere flow. *(T3 numerical plus interpretation; papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 3.3 (~line 846))*
- **Strong CP theta_QCD = 0** — The claim that theta_QCD vanishes exactly in the ACS because [[f,g],[f,g]] = 0 identically and all fermion mass matrices are built from real sl(4,R) generators, so arg det(Y_u Y_d) = 0 with CP violation entering only through the chirality map; no axion is required. *(stated as theorem, script-verified; papers/core_trilogy/Palatini_Gauge_Attractor.tex appendix B 'Strong CP problem' (~line 2445))*
- **Wheeler-DeWitt as ACS quantum attractor** — The computationally verified theorem that on a 3-node spin network under Lindblad evolution with asymmetric dissipation, the steady state concentrates in the kernel of the Hamiltonian constraint (<H> = 3e-6, kernel weight 0.507), so the WdW equation H|Psi> = 0 is the quantum Delta-I = 0 attractor; time emergence is read as Delta-I symmetry breaking. *(T3 numerical on toy model (paper C classifies it 'derived'); papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 5.3, Theorem 'WdW equation is the ACS quantum attractor' (thm:WdW, ~line 1701))*
- **Y^14 (bundle of metrics)** — The total space of the bundle of metrics over four-dimensional spacetime M^4, with fiber GL(4)/O(4) (dimension 10) and base dimension 4, giving total dimension 14. It is the arena on which the gravitational ACS and the asymmetry map are defined. *(papers/core_trilogy/Palatini_Gauge_Attractor.tex sec 4.1 (~line 893))*


## The spectral-Riemann program (Papers B and B-prime, with companions)

The prime-zero analysis: the explicit-formula instruments, the shuffle-knife methodology (FF06e-h), and the Hilbert-Polya constraint program. Primary sources: `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`, `papers/methodology/`, and the mathematical notes.

### 4/3 coincidence

The numeric coincidence between an ACS-side constant beta = 4/3 and a density-side exponent form alpha(d) = 1 + 1/d at d = 3. Under mechanism-level robustness checks the equality fails normalisation robustness (inferred-dimension spread 74, non-finite values on part of the interval) and collapses to the identity family n = d + 1 on the scanned integer lattice; the mechanism claim is tiered T4 (falsified).

**Status:** T4 (mechanism failed K1/K2); identity family n=d+1 is T1  
**Source:** papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex abstract, RQ-2 (lines 88-90), sec 4.5 (lines 190-195), tier map (lines 269-270)  
**Also:** 4/3 mechanism, the 4/3 equality

### arithmetic prime-resonance witness

The scalar witness sum over p <= 29 of <cos(gamma log p)>^2 computed on the actual (not unfolded) zero heights; in content it is the explicit-formula coupling between zeros and primes. It is the dominant FUNCTION witness (~11,497 sigma at N=10^5), and its significance amplifies with N (3,030 at N=2x10^4 to 11,497 at N=10^5).

**Status:** T1; FUNCTION in every frame tested (survived)  
**Source:** papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex sec 3 (lines 71, 78, 92-98); also Form_Function_Relativity.tex sec 4 (line 114)  
**Also:** arith, prime resonance, prime-resonance power

### Central number

The projection of the log-holonomy onto the retained B-L generator - the discriminating observable of the mixed-obstruction signature. It is forced (T2): normalised through the same Killing form K(T_BL,T_BL) = 32/3 that fixes the Higgs quartic, it equals the quark B-L charge 1/3 (equivalently the coupling invariant 1/6), with the holonomy path scale theta cancelling because the quantity is an eigenvalue ratio.

**Status:** T2 forced  
**Source:** papers/core_trilogy/Spectral_Witness_Refinement.tex sec 9.4

### Charge/coupling epistemic split

The organising T2 classification of the framework's predictions: charge-type observables (eigenvalues, charges, ratios - B-L charges, colour weights, the central number) are forced exactly because they are scale-free, while coupling-type observables (magnitudes - the Higgs quartic, masses) carry an irreducible ~1% electroweak-scale canonical-normalisation residual whose precise mechanism remains underived.

**Status:** T2, supported by two T4 negatives  
**Source:** papers/core_trilogy/Spectral_Witness_Refinement.tex sec 'The charge/coupling epistemic split and the quartic residual' (13.3 as printed)

### Elastodynamic tensor mapping

A defined (not derived) mapping of the explicit formula onto a symmetric 2x2 stress tensor with longitudinal stress T11 = x (growth term) and shear T12 = -sum_rho Re(x^rho/rho) (zero oscillation), from which variance scaling, eigenflow, and center-manifold results are computed with 100 Odlyzko zeros and no RH assumption.

**Status:** definition + T3 numerical (variance ratio matches X^0.2 to <2%)  
**Source:** papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 3.1 (eq:stress-tensor)  
**Also:** stress-tensor mapping T11/T12

### Empirical perturbation P_m

P_m = T_m - T_0, the deviation of the empirical prime-gap transition operator from uniform transport; its column sums vanish and it shares T_m's sparsity pattern. The Kernel Law, Compression Law, and the three falsified conjectures are all statements about P_m.

**Source:** papers/notes/Prime_Gap_Transition_Operator.tex sec 2.2, lines 77-81  
**Also:** prime-gap transition perturbation

### Flattening

A map pi: R -> s from a structured relational object (a factorization, a divisor lattice, a dominance relation) to a scalar or symbol string. It is reversible if there is a relational representation rho(R) with an exact recovery to s such that the operations of interest are computed on rho(R) without forming s.

**Source:** papers/later_FF06_series/The_Reversible_Flattening.tex sec 2 Definition 1 (lines 79-84)  
**Also:** reversible flattening

### Form vs. Function witnesses

An operational discriminant categorising spectral witnesses: a witness is FUNCTION if its value on the real zeros differs from its value on a marginal-matched surrogate (spacings randomly permuted, destroying zeta-specific correlations), and FORM if it does not. On 10^5 zeros with 60 surrogates, the arithmetic prime-resonance and lag-1 witnesses are FUNCTION (~11,500 sigma and ~97 sigma) while spacing, counting, and Wigner-shape witnesses are FORM (0.4-1.0 sigma); the function signal amplifies with N.

**Status:** T1 measured  
**Source:** papers/core_trilogy/Spectral_Witness_Refinement.tex sec 'Form vs. function' (printed 13; renders as sec 13)  
**Also:** FORM, FUNCTION, form (witness label), function (witness label), shuffle-invariant vs shuffle-fragile witnesses

### frame ladder

The four-rung refinement chain of reference frames instantiated on the Riemann zeros, each preserving strictly more structure: Poisson (density only) < GUE-marginal (adds the nearest-neighbour spacing law, via permuted real spacings) < GUE-full bulk (adds the two-point correlation, via random Hermitian eigenvalues) < zeta itself (adds the arithmetic; the terminal frame, against which every witness is trivially form).

**Status:** T1 (exact frames) with GUE-full column approximate (finite-N)  
**Source:** papers/methodology/Form_Function_Relativity.tex sec 3 (lines 96-112)  
**Also:** refinement chain, the nest

### GUE-necessary-but-not-sufficient result

The demonstration that a random GUE matrix spectrum rescaled to the Riemann range is statistically indistinguishable from the real zeros on pair correlation but fails the Fourier-dual prime-alignment constraint by a factor of ~40, ruling out the entire generic-GUE class of Hilbert-Polya candidates.

**Status:** T1 measured  
**Source:** papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 8.2 (sec:hp-gue-not-enough)

### Hilbert-Polya constraint specification (C1-C9)

An executable specification any candidate Hilbert-Polya spectrum must pass: density (C1), variance stationarity (C2), Montgomery R2 (C3), Rudnick-Sarnak R3 (C4), Fourier-dual prime-power peaks (C5), peak signs (C6), von Mangoldt weights (C7), L-function character transfer (C8), and Selberg orthogonality (C9), reduced to pass/fail code with calibrated thresholds. The sharpened target: find self-adjoint H such that Tr(cos(omega H)) reproduces the prime explicit formula AND the statistics are GUE.

**Status:** instrument; operator itself explicitly not constructed  
**Source:** papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 8 (sec:hilbert-polya, sec:hp-constraints)

### Kernel Law

Empirical law: for all 14 tested moduli, dim ker(P_m) = phi(m) exactly, and the kernel equals the source sector (functions f(a,b) = g(a)). The structural inclusion of the source sector is automatic (Proposition on structural source invariance); the empirically nontrivial content is exact dimensional saturation — no excess kernel arises from the arithmetic data.

**Status:** survived — verified across 14 moduli, mechanism-tested at m = 42; presented as an empirical theorem awaiting rigorous proof  
**Source:** papers/notes/Prime_Gap_Transition_Operator.tex sec 3 (Empirical Law thm:kernel), lines 86-97 and sec 3.3

### marginal-matched surrogate

For unfolded zeros with spacings s_i, the sequence obtained by randomly permuting the spacings and re-accumulating. By construction it has the same one-point spacing distribution as the object and destroys all object-specific correlations of order >= 2; it is the null ensemble the shuffle knife compares against.

**Source:** papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex Definition 1, sec 2 (lines 55-57); refined construction (permute-then-reinterpolate) at line 89  
**Also:** GUE-marginal shuffle, gap-shuffle surrogate

### Mixed obstruction (Pati-Salam decomposition)

The verdict that the sl(4) transport obstruction decomposed along SU(4) -> SU(3)_C x U(1)_{B-L} is mixed: non-abelian conjugacy class on SU(3)_C and the coset, abelian central phase on U(1)_{B-L}. Retaining B-L forces a mixed signature with nonzero central number; quotienting it gives pure non-abelian - with a stated falsifier (B-L testing non-abelian, or a simple sector testing abelian, breaks the correspondence).

**Status:** T1 verified on forced manuscript values, with falsifier  
**Source:** papers/core_trilogy/Spectral_Witness_Refinement.tex sec 9 (9.2, 9.3)

### monotone staircase

Proposition that if frames are ordered by refinement (nu_1 nested in nu_2 when every structure nu_1 preserves is also preserved by nu_2), then for a witness reading only structure nu_2 preserves, z decreases under refinement up to sampling noise: refining the frame can turn function into form but never the reverse, so each witness has a single threshold frame and the witnesses are totally ordered by the depth of structure they read. The measured (witness x frame) table on the zeros is such a staircase.

**Status:** T1 (measured on first 4000 zeros; exact-frame columns carry the argument)  
**Source:** papers/methodology/Form_Function_Relativity.tex Proposition 1, sec 2 (lines 88-90); measurement sec 5 (lines 120-137)  
**Also:** staircase

### One property, three dresses

The note's organising conjecture that the seam's defining property has three independently verified statements conjectured to be one structure: arithmetic (convolution crossable for density, uncrossable for identity), symmetric (iota reflects but [iota,T] does not vanish off the self-dual locus), and geometric (the bracket is non-traversable). Explicitly a conjecture, not a theorem — it proves nothing about RH and constructs no Hilbert–Polya operator.

**Status:** conjecture (three verified instances, no proof of identity)  
**Source:** papers/notes/Critical_Line_As_Fibered_Object.tex Principle 2 (prin:one), lines 179-189, and sec 6 scope  
**Also:** one object, three descriptions, three-way identification

### position form factor K(f)

The single-realisation spectral form factor K(f) = |sum_j exp(-i f gamma_j)|^2 / N of the actual zero positions. A fine sweep shows peaks only at f = log n with n a prime power, heights tracking the explicit-formula weight (Lambda(n)/sqrt(n))^2 at Pearson r = 0.9975, and silence (~0.01) at composite n.

**Status:** T3 numerical (r = 0.9975; survived)  
**Source:** papers/methodology/Prime_Carrier_Position_Form_Factor.tex sec 3 (lines 92-116)  
**Also:** single-realisation form factor

### prime carrier

The two-point object that the prime-resonance functional is a functional of, identified positively (not by elimination) as the value-space pair correlation of the zero positions: reconstructing the prime-resonance power from that pair correlation alone recovers 100.0% of the signal to machine precision, while spacing- or index-preserving surrogates recover only ~7%. 'Carrier' is explicitly scoped to mean 'the two-point object the functional is a functional of,' nothing more.

**Status:** T1-style machine-precision identification (reconstruction < 1e-9 of baseline); survived  
**Source:** papers/methodology/Prime_Carrier_Position_Form_Factor.tex abstract (line 31) and sec 4 (lines 140, 148)  
**Also:** the carrier

### Prime face / zero face

The two sides of the Riemann zeta function exhibited by The Geometry Engine: the prime face is the Euler product (multiplicative, unique structure — 'a factorization is a point') and the zero face is the Hadamard product (additive, cardinal structure — 'the size of a cloud'), joined by the explicit formula and verified in both directions on 10^5 zeros.

**Status:** T1 ('Two faces of zeta, T1 both directions', per The Geometry Engine)  
**Source:** papers/notes/Critical_Line_As_Fibered_Object.tex abstract and sec 1 table, lines 80-97  
**Also:** two faces of zeta

### prime-resonance power P

The scalar P = sum over primes p of P(log p), where P(f) = |sum_j exp(-i f gamma_j)|^2 / N over the zero ordinates gamma_j; in FF06f it is summed over p in {2,3,5,7,11,13}. By expansion it is a linear functional of the empirical value-space pair correlation of the positions.

**Source:** papers/methodology/Prime_Carrier_Position_Form_Factor.tex eq. (1), sec 1 (lines 37-42)  
**Also:** prime signal, prime-resonance functional

### Prime-zero ACS

The application of the ACS to number theory: Form = the prime sequence (multiplicative skeleton of Z), Function = the Riemann zero sequence (spectral dynamics of zeta), coupled by the explicit formula; RH becomes the statement that this ACS is information-balanced (stationary superposition, Delta-I = 0).

**Status:** forward direction (RH => stationarity) proved via AM-GM; identification with Delta-I = 0 proposed  
**Source:** papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 2.1, Theorem 'F_N(x) stationarity as ACS consequence' (thm:FN-acs)

### reactional vs response-driven definition

A reactional definition names a thing by the reaction it emits (its output); a response-driven definition names it by what it responds to (its input or purpose). Defined by outputs, distinct responders can be indistinguishable; defined by what they respond to, they separate. The shuffle knife is presented as the operator that converts the reactional frame into the response-driven one.

**Status:** definition-only (epistemological framing)  
**Source:** papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex Principle 1, sec 4 (lines 108-118)

### reference frame (nu)

A reference ensemble on spectra — a distribution from which surrogates are drawn — against which a witness is scored: z_nu(W) = |W_real - E_nu[W]| / sqrt(Var_nu[W]), with W function relative to nu if z_nu > tau (tau = 3) and form otherwise. The frame is a free choice, identified with the reference measure d(mu)/d(nu) of the core monograph's BCH-transfer-entropy lemma; choosing it differently relabels, and 'that choice is the perspective.'

**Source:** papers/methodology/Form_Function_Relativity.tex Definition 2, sec 2 (lines 66-72) and sec 3 (line 112)  
**Also:** frame, reference ensemble, reference measure

### resolution unit (delta)

A freely chosen minimum resolvable step delta > 0 such that the only representable points form the lattice delta-Z = {m delta}; it plays exactly the role of a reference frame for counting, analogous to the surrogate ensemble in FF06g. The 'decimals' reading is the limit delta -> 0 and the 'whole numbers' frame is delta = 1.

**Source:** papers/methodology/Scaled_Invariance_of_Infinity_and_Zero.tex Definition 1, sec 2 (lines 79-88)  
**Also:** counting unit, unit

### Riemann spectral function F_N(x)

The truncated, envelope-stripped explicit-formula sum F_N(x) = sum_{k=1..N} A_k phi_k(x) with spectral weights A_k = 1/(1/4 + gamma_k^2) and modes phi_k(x) = (1/2)cos(gamma_k x) + gamma_k sin(gamma_k x), evaluated at x = ln p for primes p. Its stationarity is the ACS reformulation of the critical-line condition.

**Source:** papers/Form_Function_and_Asymmetry.tex sec 4.1, lines 808-824  
**Also:** F_N(x), Spectral function F_N(x), spectral function

### scaled invariance of the counting label

The principle that the count of representable points in an interval is a coordinate on (interval x unit), invariant under the joint rescaling ([a,b], delta) -> (lambda[a,b], lambda delta) for every lambda > 0 and varying under scaling either factor alone; the labels 'infinity' and 'zero' for the interior of a fixed interval are therefore relative to the unit and are two ends of one staircase in delta. Explicitly scoped as a statement about resolution-relative counting, not set cardinality — Cantor is untouched.

**Status:** T1 (0 mismatches over 2x10^5 random configurations) and T2 (bijection proof)  
**Source:** papers/methodology/Scaled_Invariance_of_Infinity_and_Zero.tex Principle 1 (lines 93-100), Proposition 1 (lines 102-114), scope sec 6 (lines 206-218)  
**Also:** FF06h, joint-scaling invariance

### Section 9 chain

The proposed dependency direction 'spectral gap -> clustering -> cone-sharpness proxy', motivated by a Little-type dependency statement ('static reduction is meaningful only after observables are rigid enough to support a sharp cone'). Across TFIM, XXZ+h, long-range Ising, and an exact float-free classical Ising analogue it is not supported as a robust monotone relation (float support 0/12 exhaustive; exact joint chain support false); as a general theorem it is explicitly not claimed.

**Status:** not supported on tested windows (T1 support rates); 'as general theorem: not claimed'  
**Source:** papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex abstract, RQ-1 (lines 83-86), results sec 4, tier map (lines 258-274)  
**Also:** Section 9 toy chain, gap-cone dependency chain

### shuffle knife

The discriminant operator that replaces a spectrum by a marginal-matched surrogate (its own spacings randomly permuted and re-accumulated, preserving the one-point spacing distribution while destroying all object-specific correlations) and asks whether each spectral witness's value survives. A witness whose value is unchanged is reading the universality class (form); one whose value collapses is reading the object itself (function), with the size of the collapse measuring its true influence.

**Status:** T1 (form/function split machine-verified per MANIFEST.md claim table)  
**Source:** papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex sec 2 (lines 53-67) and abstract  
**Also:** FF06e, Shuffle knife (marginal-matched surrogate), gap-shuffle, marginal-matched null, shuffle-knife discriminant, shuffle-knife separation, shuffled spacing discriminant, the knife

### spectral witness

A scalar functional of a spectrum (e.g. spacing distribution deviation, counting deviation, Wigner-shape L2, lag-1 correlation, arithmetic prime-resonance), evaluated on the real object and on surrogate ensembles to determine what it responds to. On the Riemann zeros the standard battery of witnesses all 'point at the critical line'.

**Source:** papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex Definition 2, sec 2 (lines 59-65) and sec 1  
**Also:** witness

### Stationarity measure S(N,X) / uniform stationarity

S(N,X) = Var_{x in [X,2X]}[F_N(x)] / sum_k |A_k|^2; F_N is uniformly stationary if sup_{X>2} S(N,X) is finite for all N. This is the quantitative observable through which stationarity is claimed equivalent to RH.

**Source:** papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 4, Definition 'Stationarity measure' (def:stationarity)

### T4-prime (stationarity <=> RH)

The claimed equivalence: all nontrivial zeta zeros have Re(s) = 1/2 iff F_N is uniformly stationary for all N, with an off-line zero forcing S(N,X) >= c X^{2(sigma0-1/2)}. The forward direction is proved (AM-GM); the converse is stated as rigorous for fixed N but conditional on an unproved minimum-gap bound delta_N > 0 and numerically estimated cross-term constants (C < 0.29 for N <= 200). The paper inconsistently labels it both Conjecture and Theorem.

**Status:** forward proved; converse conditional (numerically supported), labeled inconsistently  
**Source:** papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 4, Theorem T4' (thm:T4prime, ~line 678)  
**Also:** Conjecture T4', Conjecture T4-prime, T4', Theorem T4', converse of T4

### Tartini tones

The combination frequencies gamma_k +/- gamma_j generated within the Riemann zero spectrum by the non-commuting (Wronskian) mode brackets - the arithmetic analogue of acoustic difference tones from nonlinear mixing. Crucially they are intra-spectral (zero-zero mixing); the framework insists they are not prime-zero resonances.

**Status:** T1 measured (Wronskian non-vanishing); cross-species resonance version T4 falsified in Paper B-prime  
**Source:** papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 2.2 (~line 334) and sec 6 (sec:tartini)  
**Also:** combination tones, difference-tone spectrum

### Three-number diagnostic

A structure-group-agnostic test returning three numbers for a transport holonomy D: ||D - I|| (path-dependent?), ||D - (Tr D/n)I|| (scalar/central?), and mean ||[D,H]|| over Hermitian probes (commuting?). It cleanly separates a U(1) Berry-flux arm (scalar obstruction) from an su(2) arm (conjugacy-class obstruction), and is shown probe-basis-invariant via Schur's lemma.

**Status:** T1 diagnostic, T2 probe-basis invariance  
**Source:** papers/core_trilogy/Spectral_Witness_Refinement.tex sec 8.1 and sec 9.1  
**Also:** abelian/non-abelian diagnostic

### Transport obstruction

The holonomy D = U1 U2^{-1} built from two refinement-path orderings of a connection, whose algebraic character diagnoses the system: abelian obstructions are central scalars (a number), non-abelian obstructions are conjugacy classes. For sl(4,R) Palatini transport the obstruction is forced non-abelian because the algebra is simple with trivial centre (central component 9e-16 over 2000 trials).

**Status:** diagnostic T1; sl(4) forcing T2  
**Source:** papers/core_trilogy/Spectral_Witness_Refinement.tex sec 8 (8.1 diagnostic, 8.2 forcing)

### Unique center manifold (critical line)

The result that sigma = 1/2 is the only value at which the tensor flow of the explicit formula is purely rotational (closed loops/pinwheel, curl a pure cosine); any other sigma introduces a radial drift proportional to (sigma - 1/2), producing spirals. The critical line is thereby characterised topologically as the unique center manifold of the flow family.

**Status:** proved symbolically for the defined tensor; script-verified  
**Source:** papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 3.4, Proposition 'Pure rotation at sigma = 1/2' (prop:rotation)

### value-space pair correlation of the positions (rho_2)

The empirical two-point object rho_2(s) = (1/N) sum_{j,l} delta(s - (gamma_j - gamma_l)) built from differences of actual zero positions; the form factor P(f) is by construction its Fourier transform. It is distinct from the two-point correlation of the spacing sequence, and it is the object in which the prime signal lives.

**Source:** papers/methodology/Prime_Carrier_Position_Form_Factor.tex eq. (2), sec 1 (lines 44-51)  
**Also:** position pair correlation, rho_2

### Wronskian-Lie identification

The Wronskian [f,g] = f'g - g'f on C^1((0,inf)) is a genuine Lie bracket (bilinear, antisymmetric, Jacobi) on the Riemann zero modes - non-vanishing on all 1,225 pairs of the first 50 zeros (extended to 19,900 pairs of 200 zeros) - but fails the Leibniz rule by the exact correction -fgh', so it is NOT a Poisson bracket; Hamiltonian/plasma readings of the bracket structure are therefore explicitly disallowed.

**Status:** proved + machine-verified; Poisson reading falsified (documented self-correction)  
**Source:** papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 2.2 (prop:wronski-lie, rem:not-poisson)  
**Also:** Leibniz failure -fgh', Wronskian as Lie bracket

#### Supporting vocabulary

- **Action-proximity mechanism (falsified)** — The killed hypothesis that the spectral form factor's plateau is enforced by orbit pairs close in action: the measured near-degenerate pair-density exponent is -0.01 (flat) where the mechanism requires ~ -1. Kept as a first-class negative with killing number. *(T4 falsified; papers/core_trilogy/Spectral_Witness_Refinement.tex sec 7.1)*
- **Adversarial hardening** — The practice of sweeping a result's operating point to show it is not tuned: for the prime-dual witness, detection height was swept over a 15x range and prime-match tolerance tightened 7x (to 0.005), with the hit rate remaining 100% and no off-prime peak ever appearing, at block sizes up to 8e4 zeros. *(T1 measured; papers/core_trilogy/Spectral_Witness_Refinement.tex sec 6, 'Adversarial hardening')*
- **Algebraic non-traversability (ER = EPR)** — Paper C's proposition that for a bracket output B = [X,Y], the trace projection back to an input vanishes identically, pi_X(B) = 0 — no information in B can be traversed back to X by inner-product reconstruction; the ACS bracket is 'opaque from inputs to outputs,' read as an ER=EPR non-traversable bridge derived from the bracket algebra with no bulk geometry invoked. *(T1 (machine-verified at |c| < 10^-16); papers/notes/Critical_Line_As_Fibered_Object.tex sec 4 (sec:bridge), lines 172-177; verified in code/acs_codebase/src/paper_c/er_epr_algebraic.py at |c| < 10^-16)*
- **BCH-transfer-entropy lemma** — Lemma 2.9 of the core monograph, writing the information asymmetry Delta-I(epsilon) as a series in epsilon whose terms are inner products of f - g and the commutator [f,g] against grad log(d(mu)/d(nu)) — i.e. an asymmetry always measured against a chosen reference measure nu. FF06g identifies the knife's surrogate-ensemble slot with this lemma's reference-measure slot: form/function relativity is what that free slot looks like on a spectrum. *(stated as established elsewhere (core monograph); papers/methodology/Form_Function_Relativity.tex sec 5 (line 145); referenced as core monograph Lemma 2.9 (line 112))*
- **Candidate-elimination filter / admissibility class** — A geometric filter scoring each spectral witness by coherence across phase-preserving regaugings, with primes required to be fixed points. Two bracketing failures (an aggressive axis-diffeomorphism destroys primes; a gentle window-x-height regauge passes everything) show the filter's resolution is gated by the 'admissibility class' - the coherent-mesh group lying strictly between the two - which is an observable-algebra condition still to be pinned down. *(T3; threshold deliberately not tuned; papers/core_trilogy/Spectral_Witness_Refinement.tex sec 11 (printed heading 'The candidate-elimination filter and the admissibility coupling'))*
- **Character-product block-diagonalization (falsified conjecture)** — The conjecture that P_m acts block-diagonally in the basis of character products chi_i(a) conj(chi_j(b)); falsified because the left-preserved norm fraction decreases with phi(m), reaching 29% at m = 42 — character structure is exact at the kernel boundary but does not extend globally. *(falsified (T4); papers/notes/Prime_Gap_Transition_Operator.tex sec 7.2, lines 256-274)*
- **Commutator order parameter and parity law** — Principle: with ||[iota,T]||_k = mean over p of |Im chi(p)^k|, one has ||[iota,T]||_k = 0 iff order(chi) divides 2k; the arithmetic face is real on every rung iff chi is self-dual — 'the self-dual locus is the commuting locus,' and off it the commutator equals the phase the zeros carry. Confirmed to rung 3, including the order-6 vs order-4 discrimination. *(T1 (parity law confirmed to rung 3); rung-2 phase magnitude remains a first-class negative (T3); papers/notes/Critical_Line_As_Fibered_Object.tex Principle 1 (prin:comm), lines 140-160)*
- **Compression Law (pre-asymptotic)** — Empirical scaling over the tested range phi(m) in {2,...,24}: the effective dynamical rank satisfies r_eff(m) ~ phi(m)^beta with beta approx 1.6, while algebraic rank grows as phi(m)(phi(m)-1); the ratio decays as a power law with exponent approx -0.64. The note makes no asymptotic claim outside the tested range. *(T3 (empirical fit, explicitly not extrapolated); papers/notes/Prime_Gap_Transition_Operator.tex sec 4 (obs:scaling), lines 140-179)*
- **Conditional-uniformity height floor** — The T3 claim that the implied constant in windowed L-function observables is controlled only above the height floor T_min(d,q) = (2 pi e)^d / q, where degree d enters exponentially and conductor q linearly - the height at which the Riemann-von Mangoldt count becomes asymptotically valid. Only the necessary direction is shown; a falsifiable test (S4 Artin L-zeros to height ~5000) is stated. *(T3 conjecture, correcting an earlier uniformity overclaim; papers/core_trilogy/Spectral_Witness_Refinement.tex sec 10)*
- **Cross-correlation bound C_N** — The observable |C_N| = sup_x |(2/(N(N-1))) sum_{j<k} cos((gamma_j - gamma_k)x)|, measured at 0.044 (N=200) and 7.0e-6 (N=2,001,052), fitting |C_N| ~ N^{-0.95} - 63x below the independent-spacing N^{-1/2} prediction and approaching the deterministic-cancellation bound N^{-1}, attributed to GUE rigidity of zero spacings. *(T1 measured; papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 5, 'Cross-correlation at scale' (~line 1103))*
- **Difference-tone plateau mechanism (falsified)** — The killed hypothesis that the form factor's off-diagonal lives in prime-orbit combination actions |k1 log p1 - k2 log p2| concentrating near zero: the measured contrast is consistent with an incommensurable-frequency null at 1.2 sigma (1338 prime terms, 400 null draws). The structural reason is unique factorisation - prime logarithms are mutually incommensurable, so the resonance channel is empty by arithmetic. *(T4 falsified (null itself is the content); papers/core_trilogy/Spectral_Witness_Refinement.tex sec 7.2)*
- **dimensionless invariant width/delta** — The corollary that N_delta[a,b] depends only on the ratios a/delta and b/delta: the raw width and raw unit are gauge, and the only frame-free content of the count is the dimensionless ratio width/delta. 'Adjacent' means 'one unit apart' — a statement about delta, never about the endpoints. *(T1 (50,000/50,000 ratio-preserving reparametrizations); papers/methodology/Scaled_Invariance_of_Infinity_and_Zero.tex Corollary 1 (lines 116-121); measurement D (lines 166-168))*
- **Effective dynamical rank r_eff** — The participation ratio r_eff(m) = (sum |lambda_i|)^2 / sum |lambda_i|^2 over the nonzero eigenvalues of P_m — the number of modes effectively carrying the dynamics, contrasted with the algebraic rank r_alg = phi(m)^2 - phi(m). *(papers/notes/Prime_Gap_Transition_Operator.tex sec 4, Definition 1, lines 143-149)*
- **Empirical second-order transition operator T_m** — The column-stochastic operator on C^{S_m} built from empirical prime data: T_m[(a',b'),(a,b)] is the normalized count of transitions (a,b) -> (a',b'), nonzero only when b = a' (residue continuity). *(papers/notes/Prime_Gap_Transition_Operator.tex sec 2.1, lines 62-68)*
- **exact float-free kill test** — The Section 9 variant that removes IEEE float entirely from the decision path: integer Ising energies, an integer Boltzmann base B, connected correlators and local-majority influence fractions in exact Fraction arithmetic, with the decision using only signs of Fraction covariances. It also fails the joint chain criterion (cluster covariance sign correct; outside-cone affect identically zero). *(T1 (exact; joint chain support false); papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex sec 3.2 (lines 113-122) and sec 4.3 (lines 177-184))*
- **form-bundle** — The finding that the distributional witnesses (spacing, counting, shape) are not independent confirmations but one generic bundle: their effective rank (~4) is the same on the real zeros as on the surrogate, so the multiplicity is a property of the distribution class. The 'six agreeing witnesses' resolve into one generic form-bundle plus essentially one function witness (the arithmetic one). *(T3 numerical (effective-rank measurement at N=20k); papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex sec 3 (line 102))*
- **Functional-equation involution iota and character twist T** — iota: chi -> conj(chi) is the involution on the family of Dirichlet L-functions induced by the reflection s <-> 1-s; the multiplicative-character twist T paints chi(p)^k on rung k of the harmonic ladder. Their commutator is the family's order parameter. *(papers/notes/Critical_Line_As_Fibered_Object.tex sec 3 (sec:reflect), lines 126-148)*
- **gap two-point surrogate (C)** — A surrogate produced by phase randomisation of the spacing series, which provably preserves the spacing autocovariance (the two-point statistic of the gaps) while destroying all higher-order gap structure. Despite being faithful to the gap two-point object it recovers only ~7% of the prime signal, proving the carrier is not the gap correlation. *(T3 numerical control; papers/methodology/Prime_Carrier_Position_Form_Factor.tex sec 2 (line 65) and 'Coherence and mechanism' (line 136))*
- **GUE-full (bulk) frame** — The frame ladder rung built from eigenvalues of a random Hermitian matrix, bulk unfolded (central 80% trimmed), which preserves the RMT two-point correlation but carries no arithmetic. It is a finite-N approximate ensemble requiring dense diagonalisation (gated behind --full, ~7 min), and its column is explicitly flagged as approximate. *(T3 (approximate; the two exact frames carry the load-bearing flip); papers/methodology/Form_Function_Relativity.tex sec 3 table (line 106), sec 4 (lines 118, 139), sec 6 edge (i) (line 155))*
- **GUE-marginal frame** — The frame ladder rung constructed by permuting the real unfolded spacings and re-accumulating: it restores the exact nearest-neighbour spacing distribution while destroying all correlations of order >= 2 and all arithmetic. It is the same operation as FF06e's marginal-matched surrogate, now named as one rung of the ladder. *(T1 (exact frame); papers/methodology/Form_Function_Relativity.tex sec 3 table (line 105) and line 112)*
- **Harmonic ladder / repetition tower** — The arithmetic-face structure in which prime periodic orbits appear with r-fold repetitions at the standard trace-formula amplitude p^{−k/2}: the k=2/k=1 line ratio follows p^{−1/2} (log-log slope −0.533 vs −0.5, R² = 0.98), and the tower is confirmed 3 rungs deep (p³ lines at 3 log p, slope −1.015). A necessary Hilbert-Pólya operator condition; constructs no operator. *(T1; MANIFEST.md Paper B table (lines 74, 77))*
- **High-scale-boundary reading (falsified)** — The killed rescue hypothesis that lambda_ACS = 2 sqrt(3)/27 is a high-scale boundary value with the 0.85% residual explained by RG running: the full one-loop SM RGE shows the running quartic crosses lambda_ACS exactly once, at mu ~ 132 GeV - essentially the electroweak scale - so the algebraic value matches the physical EW-scale quartic directly and the residual is a tree/threshold-level normalisation offset, not running. *(T4 falsified; papers/core_trilogy/Spectral_Witness_Refinement.tex sec 13.2 (as printed))*
- **Hilbert–Polya wall (quantified obstruction)** — The quantified tension any self-adjoint operator with the zeros as spectrum must resolve: simultaneously real periodic-orbit amplitudes (|Im W|/|Re W| = 0.0001, pulling to time-reversal-invariant beta = 1) and GUE level repulsion (measured beta = 2.00, pulling to time-reversal-broken beta = 2). *(papers/notes/Critical_Line_As_Fibered_Object.tex sec 4, lines 192-197; script hp_operator_constraint.py)*
- **Hypercone projection test (degeneracy cones)** — The companion test establishing that eigenvalue degeneracies of Hermitian families are cones, the repulsion exponent counts the cone's codimension (beta = codim - 1), and the chirality direction supplies the third dimension (measured on the zeros: beta = 2.019, a codim-3 shadow). Note: this 'hypercone' is a spectral-geometry object, distinct from the Klein-foam hypercone vortices of the Flag Condensate notes. *(papers/notes/Critical_Line_As_Fibered_Object.tex sec 4, lines 199-204; code/acs_codebase/extras/test_conjecture_hypercone_projection.py)*
- **identity family n = d + 1** — The bookkeeping-identity explanation of the 4/3 equality: every exact hit in the integer lattice scan of alpha(d) = 1 + 1/d against beta(n) = n/(n-1) satisfies n = d + 1, so the 4/3 match at d = 3, n = 4 is consistent with an identity family rather than a robust physical mechanism. *(T1 (exact lattice scan); papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex sec 4.5 (lines 190-195) and tier map (line 269))*
- **Intra-species resonance vs. cross-species complementary cancellation** — The distinction that combination tones arise only within a single spectrum (zeros with zeros, primes with primes), while the prime-zero coupling is not a resonance but a cancellation identity: psi(x) fluctuations and the zero oscillation sum to a structureless remainder via the explicit formula. An ACS 'closes' across the Form/Function boundary rather than resonating across it. *(structural claim; direct-resonance channel falsified (B-prime sec 7.2); papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 2, 'Acoustic structure' subsection (~line 532))*
- **K1 / K2 robustness checks** — The two 4/3 mechanism tests: K1 (normalisation robustness) scales beta = 4/3 by c and inspects the inferred dimension d-hat = 1/(c beta - 1); K2 scans the integer lattice for alpha(d) = 1 + 1/d against beta(n) = n/(n-1). The 4/3 mechanism failed both, which grounds its T4 entry. *(T1 (exact lattice/identity checks); papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex sec 3.3 (lines 124-133) and tier map (line 270))*
- **Koide ratio h-tilde/h = 2/3** — A derived algebraic relation from the companion paper Colour from Gravity, cited as the single <2,3> quantity that survives into the broken-phase Yukawa structure, and only because it is preserved by tree-level matching; it does not generalize to a lattice-wide structure. *(papers/notes/Pythagorean_Lattice_Limits.tex abstract and sec 4, lines 346-350)*
- **lag-1 spacing correlation witness** — The serial correlation of consecutive unfolded spacings, reading local order. It is formally FUNCTION under the shuffle knife (~97 sigma) but sits within the measured apparatus band of the GUE value, so it is explicitly not claimed as a beyond-GUE finding; in the frame ladder it remains nominally function (6.5 sigma) even against GUE-full, attributed to a finite-N apparatus effect. *(T3; not claimed beyond-GUE (inside apparatus band); papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex sec 3 (line 79) and sec 5 (line 124); Form_Function_Relativity.tex sec 6 edge (i) (line 155))*
- **Matrix candidate** — A proposed self-adjoint operator whose spectrum would be the Riemann zero heights {gamma_k}; the object the witness-survival and constraint-specification machinery is designed to test. *(papers/core_trilogy/Spectral_Witness_Refinement.tex sec 1)*
- **measurability wall** — The data-scarcity boundary named by the programme's signal-to-noise criterion: the identification machine (form factor / explicit formula) is known and universal, but for objects with too few resolved zeros (e.g. the elliptic curve 11a1, with ~10 ordinates in public tables) the form factor cannot resolve its arithmetic peaks at reachable height. *(scope boundary (stated, not measured); papers/methodology/Prime_Carrier_Position_Form_Factor.tex sec 4 'Where the method stops' (line 144))*
- **Mod-6 hexagonal clock** — The residue-class picture at modulus 6 whose three statistical anomalies at 5x10^7 primes motivated the study: a sign-reversed restoring force, a directional asymmetry between the 5->1 and 1->5 transitions, and a variance suppression of cross-class transitions to 0.292 +/- 0.003. *(papers/notes/Prime_Gap_Transition_Operator.tex sec 6, lines 211)*
- **No detectable lattice imprint in the broken phase (negative result)** — Proposition stating that broken-phase Standard Model mass and mixing ratios show no statistically significant preference for the <2,3> lattice: adding primes reduces lattice distance equally for data and null, consistent with the data being lattice-generic. The lattice observation is thereby confined to the unbroken algebraic sector. *(T3 (numerical negative result; survived as stated); papers/notes/Pythagorean_Lattice_Limits.tex sec 4, Proposition (lines 314-325))*
- **Off-line injection test** — A sensitivity control in which a single synthetic zero with envelope factor x^{sigma - 1/2} is injected into F_N; the perturbed variance exponent must follow alpha = 2*sigma - 1. At N = 2,000,000 all four off-line sigmas recover the predicted exponent to within 1.5%, while the unperturbed exponent stays ~0 across six decades of N. *(T1 measured at largest public scale (Odlyzko zeros6); papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 5, 'Off-line injection scaling' (~line 1056))*
- **outside-cone leakage** — The cone-sharpness proxy in the Section 9 kill tests: the commutator norm ||[Z_0(t), Z_r]|| (max and, where stated, mean) measuring influence outside a Lieb-Robinson-type light cone; in the exact classical analogue it is replaced by local-majority influence fractions ('outside-cone affect'), which turn out to be identically zero under local majority. *(T1/T3 observable (proxy; threshold-sensitive); papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex sec 3.1 (lines 104-106) and sec 4.3 (lines 179-184))*
- **pair-correlation sufficiency** — Proposition: the prime-resonance power P is a linear functional of rho_2 alone, hence any transformation of the point set preserving the value-space pair correlation of the positions preserves P exactly. Stated as immediate from the expansion of P(f); the paper's content is measuring which surrogates preserve rho_2. *(T2 (proved, immediate) plus T1-style machine-precision calibration; papers/methodology/Prime_Carrier_Position_Form_Factor.tex Proposition 1, sec 1 (lines 53-57))*
- **Paper B / Paper C (bundle companions)** — Companion papers cited across the notes by letter: Paper B is 'Spectral Susceptibility and Renormalized Stability on the Riemann Critical Line' (source of the |C_N| = 0.044 cross-correlation bound on the first 200 Riemann zeros), and Paper C is 'Holographic Spectral Inversion and Invariant Kinematic Attractors' (source of the algebraic ER=EPR non-traversability result). *(papers/notes/Prime_Gap_Transition_Operator.tex bibliography lines 377-385; papers/notes/Critical_Line_As_Fibered_Object.tex sec 4)*
- **Phenomenological closure ansatz (variance-floor bridge)** — The quarantined mean-field relation R = 1/(1 + (N_eff - 1)|C|) which, with the empirical N_eff = 56 and Paper B's Riemann-zero cross-correlation bound |C_N| = 0.044, reproduces the measured variance floor 0.292 to three significant figures. Presented explicitly as a numerical match, not a derived consequence, and not load-bearing for the Kernel or Compression Laws. *(conjecture (phenomenological closure, numerical match only); papers/notes/Prime_Gap_Transition_Operator.tex sec 6 (sec:bridge), lines 206-228)*
- **Pythagorean lattice <2,3>** — The multiplicative subgroup of Q^x generated by the primes 2 and 3 — the arithmetic lattice of Pythagorean tuning. The note's Observation is that every native dimensionless ratio of the minimal Pati–Salam bracket algebra (charges, adjoint eigenvalues, saturation coefficient, multiplicities) lies in this lattice, whereas SU(5) and SO(10) introduce the prime 5. *(T2; papers/notes/Pythagorean_Lattice_Limits.tex sec 1, Observation (lines 95-101))*
- **Renormalised stability (Delta_norm)** — Delta_norm(u) = (psi(e^u) - e^u)/e^{u/2}, the prime-counting error in logarithmic time rescaled by the natural envelope: bounded under RH, unbounded if any zero has Re(rho) > 1/2. Explicitly presented as a reframing of von Koch's classical bound in ACS stability language, not a new theorem. *(restatement of classical result; T3 numerical check on 50 zeros; papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 2.6 (sec:vonKoch), Theorem 'Renormalised stability under RH' (thm:vonKoch-acs))*
- **repulsion witness** — The witness computing the fraction of spacings below half the mean, reading only the nearest-neighbour spacing law. It is the relativity theorem in miniature: function against Poisson (49.5 sigma) and form against the GUE-marginal frame (0.2 sigma) — the identical scalar functional carrying opposite labels in two frames. *(T1 (measured); papers/methodology/Form_Function_Relativity.tex sec 3 (line 114) and sec 4 table (line 126))*
- **resolution count N_delta[a,b]** — The two-argument count of lattice points of delta-Z in an interval, N_delta[a,b] = floor(b/delta) - ceil(a/delta) + 1 (clamped at 0), with interior variant N_delta-circ(a,b). The note's content is that the second argument (the unit) is load-bearing: the interior of (1,2) carries 0, 9, 99, 999, 9999 points at delta = 1, 1/10, ..., 1/10000. *(T1 (exact rational arithmetic, script exits nonzero on mismatch); papers/methodology/Scaled_Invariance_of_Infinity_and_Zero.tex Definition 1, sec 2 (lines 79-88); measurement A (lines 135-151))*
- **Resolvent susceptibility chi(omega)** — chi(omega) = sum_rho 1/(omega - gamma_rho) = Tr[(omega*I - H)^{-1}] for any operator H with spectrum {gamma_k}: the explicit formula rephrased as a linear-response/resolvent-trace object, adopted as the rigorous replacement for the falsified plasma-Hamiltonian framing. *(tautological identity verified at machine precision; natural-operator construction open; papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 2.5 (sec:resolvent, eq:chi-omega))*
- **retraction: 'the primes are not a two-point statistic'** — A previously entertained internal claim, drawn from spacing-domain surrogate tests, that the prime signal is inaccessible to any two-point statistic and must reside in higher-order phase coherence. FF06f formally retracts it: it measured the wrong two-point object (the spacings), and the surrogate collapse it observed is the destruction of rho_2, not a signature of higher-order structure. *(retracted (falsified internal claim, kept first-class); papers/methodology/Prime_Carrier_Position_Form_Factor.tex abstract (line 31) and sec 4 'Establishes' (line 140))*
- **rigidity witness (number variance)** — The witness computing number variance in fixed windows, reading the two-point correlation of the spectrum. It is function against Poisson and against the spacing-marginal shuffle (both ~10 sigma) and falls to form (1.6 sigma) only once the frame preserves the two-point function (GUE-full) — the one-rung-later step of the staircase. *(T1 (measured); papers/methodology/Form_Function_Relativity.tex sec 3 (line 114) and sec 4 table (line 129))*
- **Same-gap conjecture (falsified)** — The killed hypothesis that the central-number residual and the 0.85% Higgs-quartic residual are the same gap: the central number closed because it is a charge (path scale cancels through the eigenvalue ratio) while the quartic is a coupling with no ratio for the scale to cancel through; the two share only the Killing form 32/3. *(T4 falsified; papers/core_trilogy/Spectral_Witness_Refinement.tex sec 13.1 (as printed))*
- **Source sector** — The phi(m)-dimensional subspace of state-space functions depending only on the source residue class, {f(a,b) = g(a)}; Dirichlet characters furnish a canonical orthogonal basis but the sector itself is the structural object. *(papers/notes/Prime_Gap_Transition_Operator.tex sec 3, lines 92-97)*
- **Sovereign Integrity Protocol License (SIP License v1.1)** — The license under which every note in the bundle is 'co-governed and enforced', cited in the header comment of each .tex file with a pointer to the repository LICENSE file. *(papers/notes/Pythagorean_Lattice_Limits.tex lines 1-2 (identical header in all six files))*
- **Spectral stability ratio (rho_spec)** — rho_spec = max_k |A_k| X^{|sigma_k - 1/2|} / (delta_N^{-1} sum_j |A_j|), the spectral analogue of the tensegrity ratio: rho_spec = 0 exactly when all zeros lie on the critical line (stable, stationary F_N), and diverges as X grows if any zero is off-line. *(papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 2.3 (eq:rho-spec))*
- **Stripped-mode SHO property** — The envelope-stripped mode y_k = e^{-sigma t} phi_k satisfies y_k'' + gamma_k^2 y_k = 0 for ALL sigma - a definitionally true fact (the sigma-dependence lives entirely in the envelope). Its role is corrective: an earlier draft wrongly claimed the SHO property held only at sigma = 1/2; the corrected distinguishing feature of the critical line is stationarity of the superposition. *(proved (tautological); documented self-correction; papers/core_trilogy/Riemann_Spectral_Critical_Line.tex sec 3.3, Remark 'Stripped-mode ODE' (thm:sho) and Remark 'Self-correction from scaling' (rem:self-correction))*
- **Structural source invariance** — Proposition: for any column-stochastic T and uniform reference T_0 both respecting residue continuity, (T - T_0) annihilates every source-only function — the source sector lies in ker(P_m) as a coordinate-level consequence of the construction, delineating what is automatic from what is empirically nontrivial in the Kernel Law. *(T2 (proved, sketch given); papers/notes/Prime_Gap_Transition_Operator.tex sec 3.1 (prop:structural), lines 102-122)*
- **The Geometry Engine / The Reversible Flattening (bundle companions)** — Two companion documents whose vocabulary the seam note inherits: The Reversible Flattening fixes the definitions of flattening and seam; The Geometry Engine exhibits zeta's two faces (Euler product / Hadamard product) with T1 verification in both directions. *(papers/notes/Critical_Line_As_Fibered_Object.tex title page and sec 1, lines 32-49, 77-97)*
- **the scalar was a shadow** — The pattern isolated in the companion note 'When a Number Lies': a single scalar is often a lossy projection (a shadow) of an underlying relation, and the relation, not the scalar, is the faithful object. FF06h reads 'the number of points between 1 and 2' as such a shadow of the relation width/delta. *(framing (established in companion paper When_a_Number_Lies.tex); papers/methodology/Scaled_Invariance_of_Infinity_and_Zero.tex sec 5 (lines 184-189))*
- **threshold frame** — For a given witness, the single rung of the refinement chain at which its label falls from function to form and stays fallen: repulsion and shape at GUE-marginal, rigidity at GUE-full, and the arithmetic witness beyond every frame short of zeta itself. The resulting order of witnesses by depth of structure read is an output of the measurement, not an input. *(T1 (measured); papers/methodology/Form_Function_Relativity.tex Proposition 1 (line 89) and sec 4 (line 137))*
- **Transition state space S_m and transition class** — For modulus m, S_m = {(a,b) : a,b in U_m = (Z/mZ)^*} with |S_m| = phi(m)^2; each consecutive prime pair (p_i, p_{i+1}) coprime to m defines the transition class (p_i mod m, p_{i+1} mod m). *(papers/notes/Prime_Gap_Transition_Operator.tex sec 2 (Setup), lines 56-61)*
- **true influence z(W)** — The z-score z(W) = |W_real - mean(W_surrogate)| / sigma(W_surrogate) of a witness evaluated on the object against an ensemble of marginal-matched surrogates; it quantifies how much of the witness's reading is object-specific rather than class-generic. *(papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex Definition 2, sec 2 (lines 60-64))*
- **Unbiased reference T_0** — The uniform transport operator respecting residue continuity, assigning probability 1/phi(m) to each consistent next state; the baseline from which the empirical perturbation is measured. *(papers/notes/Prime_Gap_Transition_Operator.tex sec 2.2, lines 71-76)*
- **Uniform spectral contraction (falsified conjecture)** — The conjecture that rho(P_m) < 1 uniformly in m with P_m a quasi-nilpotent contraction; falsified by data showing rho(P_m) grows approximately as 0.07 phi(m)^0.75, so contraction holds only in the low-modulus regime and does not extrapolate. *(falsified (T4); papers/notes/Prime_Gap_Transition_Operator.tex sec 7.1, lines 237-254)*
- **Universal renormalized spectral law (falsified conjecture)** — The conjecture that P_m / rho(P_m) has a universal spectral distribution as m grows; falsified because the normalized mean |lambda|/rho decreases monotonically by a factor of 16 across tested moduli — the spectrum concentrates on dominant modes instead of converging to a universal law. *(falsified (T4); papers/notes/Prime_Gap_Transition_Operator.tex sec 7.3, lines 276-294)*
- **Vantage-point census** — The measurement (hp_vantage_points.py) that found two function faces of the zeros over a GUE silhouette: an arithmetic face at ~830 sigma and a local-order face at ~26 sigma, re-read in the note as the two sides of the seam seen from the zero locus. *(papers/notes/Critical_Line_As_Fibered_Object.tex sec 2, lines 100-116; script at code/hp_knife_suite/hp_vantage_points.py)*
- **Wall resolution class** — The result that the two Hilbert–Polya wall constraints coexist precisely in families carrying an anti-commuting antiunitary symmetry C H* C^-1 = -H (verified with C^2 = -1): the anti-commuting C pairs the spectrum gamma <-> -gamma, making the full-spectrum witness machine-real while preserving codim-3 degeneracy (beta = 2). Among GOE/GUE/chiral ensembles only the chiral class passes both constraints; 'the class is pinned; the primes are not yet in it.' *(verified exactly and by ensemble; arithmetic realisation open; papers/notes/Critical_Line_As_Fibered_Object.tex sec 4, lines 205-218; script hp_wall_resolution_class.py)*
- **Wigner-shape witness** — The witness computing the L2 distance of the spacing histogram to the GUE Wigner surmise, reading only the nearest-neighbour spacing law. Like repulsion it is function against Poisson (44.3 sigma) and form against GUE-marginal (0.1 sigma). *(T1 (measured); papers/methodology/Form_Function_Relativity.tex sec 3 (line 114) and sec 4 table (line 127); Spectral_Rigidity_Shuffle_Knife.tex table (line 82))*


## Holography and algebraic structure (Paper C, with companions)

Killing-form orthogonality, the spectral taxonomy of adjoint flows, and signature selection. Primary sources: `papers/core_trilogy/Holographic_Spectral_Inversion.tex`, `papers/notes/Adjoint_Clifford_Signature_Selection.tex`.

### (3,1) internal grading selection

The headline instance of the selection theorem: for T_{B-L} in sl(4,R) the selected grading of the internal carrier space (B-L charge space: three quark colours plus one lepton) has (3,1) shape. The note stresses this is a grading of the internal space, not a derivation of Lorentzian spacetime signature — identifying the two would require a bridging mechanism not provided, in light of Coleman–Mandula.

**Status:** T2 as internal-grading statement; spacetime-signature interpretation is an open conjecture  
**Source:** papers/notes/Adjoint_Clifford_Signature_Selection.tex abstract and sec 5 (Interpretation and scope), lines 569-644  
**Also:** signature selection

### Algebraic non-traversability

The proposition that the scalar projection of a bracket output B = [X,Y] back onto span{X} vanishes identically (by Killing-orthogonality), so no information from B can be 'traversed' back to X through inner-product reconstruction - offered as the operational content of ER=EPR non-traversability derived from bracket algebra alone, with an explicit disclaimer that it does not derive holographic entropy bounds.

**Status:** proved; correspondence to AdS/CFT flagged as open research direction  
**Source:** papers/core_trilogy/Holographic_Spectral_Inversion.tex sec 4.3, Proposition 'Algebraic non-traversability' (prop:non-trav)  
**Also:** ACS rereading of ER=EPR

### Grading selection theorem

The note's main theorem: for a Cartan element whose adjoint eigenvalue clusters have interaction weights factoring through clusters, minimizing S~_g over involutions (i) is attained at cluster-coherent partitions, (ii) reduces to a weighted max-cut on the complete graph K_m with weights w_ij n_i n_j, (iii) for binary splits uniquely places the minority cluster in the P-negative eigenspace, and (iv) is structurally stable under perturbation. For T_{B-L} the selected grading has (3,1) shape.

**Status:** T2 for parts (i)-(iii) (proved); part (iv) T3 (verified numerically)  
**Source:** papers/notes/Adjoint_Clifford_Signature_Selection.tex sec 3, Theorem 5 (thm:selection), lines 226-268  
**Also:** Grading selection from adjoint activity, selection theorem

### Killing-orthogonality theorem

For any matrix Lie algebra and any X, Y: tr([X,Y]X) = 0 = tr([X,Y]Y) - the bracket output is trace-orthogonal to both inputs. Proved by trace cyclicity, verified symbolically and over 1000 random pairs; presented as the algebraic content of 'non-traversability' in the ACS framework.

**Status:** proved (elementary), machine-verified  
**Source:** papers/core_trilogy/Holographic_Spectral_Inversion.tex sec 4.1, Theorem 'Killing-orthogonality' (thm:killing)

### Minimal Pati–Salam embedding / T_{B-L} generator

The B-L generator T_{B-L} = diag(1/3, 1/3, 1/3, -1) in sl(4,R), normalized to vanishing trace over the fundamental representation, underlying the minimal Pati–Salam embedding whose bracket structure [e, omega] produces the framework's native dimensionless ratios.

**Source:** papers/notes/Pythagorean_Lattice_Limits.tex sec 1, lines 66-71; also papers/notes/Adjoint_Clifford_Signature_Selection.tex sec 2  
**Also:** PS embedding, T_{B-L}

### Three-class spectral taxonomy

The classification of adjoint flows exp(t ad_X) into elliptic (imaginary eigenvalues, rotational/periodic), hyperbolic (real eigenvalues, exponential, no 2-pi closure), and parabolic (nilpotent, polynomial) classes via Jordan-Chevalley decomposition. Its role is corrective: the Palatini ad_{T_{B-L}} saturation ad^3 = (16/9) ad is hyperbolic Cayley-Hamilton saturation, not a geometric 2-pi inversion.

**Status:** mathematically standard, applied as correction of a prior overclaim  
**Source:** papers/core_trilogy/Holographic_Spectral_Inversion.tex sec 4.2, Theorem 'Spectral taxonomy of adjoint flows' (thm:taxonomy)  
**Also:** elliptic/hyperbolic/parabolic adjoint flows

#### Supporting vocabulary

- **Active sector** — The nonzero-eigenvalue subspace of ad_T; for T_{B-L} in sl(4,R) it is the 6-dimensional space of quark–lepton mixing generators split equally between the +4/3 and -4/3 eigenspaces, versus the 9-dimensional kernel of Cartan and quark–quark generators. *(papers/notes/Adjoint_Clifford_Signature_Selection.tex sec 2, Proposition 4 (prop:spectrum), lines 141-155)*
- **Banach-Tarski as geometric ACS** — The reinterpretation of the Banach-Tarski paradox as an ACS: the two free-group rotation generators are Form and Function, their non-commutativity is the 2nd-order bracket, the irreducible non-closure of words is the 3rd-order holonomy, and the paradoxical second ball is the 'emergent volume' quantified by Delta-I. *(illustration/analogy (no computation); papers/core_trilogy/Holographic_Spectral_Inversion.tex appendix B (sec:BT))*
- **Cluster coherence** — The property that the minimizing grading assigns each eigenvalue cluster of ad_T entirely to one parity side — splitting a cluster never reduces the functional. It holds because g(0) = 0 makes the functional bilinear in cluster magnetisations; it holds for all four classical Lie algebra families but can fail in exceptional algebras. *(T2 for classical types (Corollary cor:classical); fails for G_2 (Proposition prop:G2, verified by exhaustive enumeration); papers/notes/Adjoint_Clifford_Signature_Selection.tex Theorem 5(i) and Remark rem:scope, lines 242-245, 416-433)*
- **Coleman–Mandula bridging mechanisms** — The three routes the note identifies that could in principle connect the internal (3,1) grading to spacetime signature without violating Coleman–Mandula: (1) a soldering construction via the Palatini tetrad, (2) a pre-geometric regime where the theorem's hypotheses do not yet apply, (3) explicit evasion of the theorem's hypotheses (massless-only, no mass gap, infinite-dimensional symmetry). None is established in the note. *(conjecture (explicitly open); papers/notes/Adjoint_Clifford_Signature_Selection.tex sec 5, 'What would be needed to bridge the gap', lines 601-628)*
- **Epistemic compression** — The trilogy's stated working discipline: repeated cycles of conjecture, explicit verification, and compression in the Lakatos proofs-and-refutations sense, with disproved hypotheses retained as boundary markers and each correction claimed to tighten the framework. *(methodology statement; papers/core_trilogy/Holographic_Spectral_Inversion.tex sec 1, 'Methodological note on epistemic compression')*
- **Graded spectral functional S~_g[P]** — The functional S~_g[P] = Tr(sigma_P · g(ad_T)) over symmetric involutions P, for any even g >= 0 with g(0) = 0 and g(lambda) > 0 for lambda != 0, where sigma_P is the adjoint representation of X -> PXP^{-1}. The g(0) = 0 condition restricts it to the active (nonzero-eigenvalue) sector of ad_T. *(papers/notes/Adjoint_Clifford_Signature_Selection.tex sec 1, Definition 3 (def:functional), lines 114-129)*
- **Minority-cluster rule** — For a binary eigenvalue split (m = 2, minority cluster of size k < n/2) the unique minimizer places the minority cluster in the P-negative eigenspace I_-, giving minimum value -2k(n-k) g(lambda); for T_{B-L} this selects P = diag(1,1,1,-1), i.e. the (3,1) grading. *(T2; papers/notes/Adjoint_Clifford_Signature_Selection.tex Theorem 5(iii) and Remark (Uniqueness), lines 257-260, 371-378)*
- **Symmetric involution and induced grading** — A matrix P in GL(4,R) with P^2 = I and P = P^T, inducing a Z/2 grading g = g_+ (+) g_- of the Lie algebra via sigma_P(X) = PXP^{-1}; involutions of fixed signature (p,q) form the Grassmannian Gr(q,4). *(papers/notes/Adjoint_Clifford_Signature_Selection.tex sec 1, Definition 2, lines 95-107)*
- **Tensegrity-gauge correspondence** — The lemma that zero eigenvalues of a tensegrity network's rigidity matrix (zero-energy deformations) align with the gauge redundancies of the lattice gauge theory on the same graph — directions in configuration space where Delta I = 0. Numerically verified: the icosahedral tensegrity yields exactly 6 zero modes, matching dim(SO(3)) + translations. *(T3 numerical; papers/Form_Function_and_Asymmetry.tex Lemma lem:zero-modes, lines 912-934)*
- **Universal-2pi overclaim (retracted)** — A withdrawn earlier claim that three-step bracket chains universally produce 2-pi geometric inversions across ACS systems; verification showed exp(2*pi*ad_{T_{B-L}}) has spectral norm ~4348, not 1. Retained explicitly as a boundary marker: what is universal is finite-order Cayley-Hamilton saturation, with geometric content depending on spectral class. *(falsified (self-correction, kept as boundary marker); papers/core_trilogy/Holographic_Spectral_Inversion.tex sec 4.2, Remark 'On the universal-2pi overclaim')*
- **Weight factorisation through eigenvalue clusters** — The hypothesis of the selection theorem that interaction weights w_ab = g(|lambda_a - lambda_b|) depend only on which clusters a and b belong to. It holds for all four classical families (A_n, B_n, C_n, D_n) in their defining representations, but fails for some G_2 Cartan elements whose clusters mix short and long roots. *(T2 for classical types; failure in G_2 verified by exhaustive enumeration over 64 sign assignments; papers/notes/Adjoint_Clifford_Signature_Selection.tex Theorem 5 hypothesis, Corollary cor:classical (lines 380-398), Proposition prop:G2 (lines 400-414))*


## Physical models: the Flag Condensate and electron notes

The speculative physical-model arm — a single scalar condensate as ontological primitive, the framed-unknot electron, and their falsification record. Primary sources: `papers/notes/Flag_Condensate_*.tex`, `papers/notes/Mobius_Screw_Electron.tex`, `papers/notes/Framing_Transformer_Spin_Parity.tex`.

### Capacitance model of alpha (self-stress matching)

Assign charge e/2 to each sheet of the Mobius double cover and match the electrostatic self-energy to the rest energy, (e/2)^2/(2C) = m_e c^2; combined with the spin radius this converts any capacitance C into alpha^-1 = pi*eps0*R/C, returning alpha^-1 ~ 137.036 in the annulus baseline. The sequel shows this figure is an output of the annulus model at a tuned cutoff (a/R ~ 2e-118), not a geometry-unique invariant: moderate aspect ratios give alpha^-1 = O(1).

**Status:** T3 as-implemented estimate; deflated (cutoff-tuned, not geometric) by the ribbon-capacitance sequel  
**Source:** papers/notes/Mobius_Screw_Electron.tex sec 4; papers/notes/Mobius_Ribbon_Capacitance.tex sec 2-4  
**Also:** E_cap = m_e c^2, alpha^-1 = pi eps0 R / C, self-stress match

### Density engine

The reading of the shape of the universe as an inexhaustible geometric constraint source: geometry actively routes, compresses, and re-releases phase structure along lanes. 'Density' means structure per geometric lane on a stated manifold; the term explicitly does not assert literal infinite energy density in SI units.

**Status:** definition-only (metaphor mode) with finite lane-density model mode  
**Source:** papers/notes/Density_Engine_Many_Worlds.tex abstract and sec 2, lines 48-56, 108-154  
**Also:** infinite density engine (metaphor)

### Flag Condensate

Postulate: a primordial condensate field Phi = (phi + i pi)/sqrt(2), a two-component complex scalar whose real and imaginary parts are in quadrature; in the Klein-foam ontology it is the substrate from which structure is read. Also names the research programme and collaboration ('Flag Condensate programme').

**Status:** definition-only (postulate)  
**Source:** papers/notes/Klein_Foam_Monad.tex sec 2, Postulate 2.1, lines 82-87  
**Also:** Phi, Phi substrate, flag condensate field, flag field, flag-condensate field

### Framed unknot

The model electron of the Mobius-screw note: a simple closed loop carrying two full twists of framing, equivalently a (2,1)-torus embedding with self-linking number 2. The knot type is trivial (an unknot) because one winding number equals 1; the physical content is attributed to framing, not knotting.

**Source:** papers/notes/Mobius_Screw_Electron.tex sec 2.3, Definition 1 (lines 124-135)  
**Also:** model electron

### Framing Transformer

The named companion computation and instrument (code/framed_unknot/framing_transformer.py, results in docs/framed_unknot_results.json) that evaluates the full chain gamma -> U -> (Sl = Tw + Wr) -> F: S1 -> SO(3) -> q: S1 -> SU(2) for the Mobius-screw centerline, to locate exactly where spin-1/2 enters. It is the instrument that killed the Sl=2 <-> g=2 identification while confirming the geometry.

**Status:** T2 closed-form + T1/T3 numerical  
**Source:** papers/notes/Framing_Transformer_Spin_Parity.tex title, sec 1-2  
**Also:** framing_transformer.py, parity law, transformer chain

### Klein foam

Postulate: reality modelled as a nested, scale-variant dynamic network of self-intersecting Klein-bottle hypercones (vortex/tornado analogues) embedded in the flag condensate; each hypercone is a Mobius-twisted coring screw that induces phase slips and deposits residual slag, and the foam may be discretised as a voxel grid whose active cells form a throat sieve.

**Status:** definition-only (postulate)  
**Source:** papers/notes/Klein_Foam_Monad.tex sec 2, Postulate 2.2, lines 89-96  
**Also:** KFM, Klein-Foam Monad, Klein-foam Monad, TR-2026-FF06-KFM, the Monad

### Many-worlds self-similarity

The postulate that the same phase-slip / throat / eigen-path pattern recurs across electron, nuclear, and cosmological scales as structural recursion — recurrence of the pattern, not identity of numerical coefficients, and explicitly not a proof of Everett's many-worlds interpretation.

**Status:** conjecture (structural parallel only; 'not a claim that MWI is established physics')  
**Source:** papers/notes/Density_Engine_Many_Worlds.tex abstract and secs 3-4, lines 52-58, 159-194  
**Also:** scale recursion, self-similar phase-defect ladder

### Mobius-screw electron

A geometric model of the electron as a framed unknot: the centerline of a (2,1)-torus embedding on a torus of major radius R and minor radius a, with the spin-1/2 and g=2 content attributed to the framing induced by the torus embedding (self-linking Sl = p*q = 2), plus a separate capacitance estimate for alpha. Explicitly a model design, not a theorem of QED, a measurement, or a uniqueness claim.

**Status:** geometry confirmed (|Sl|=2, spinorial); its g=2 reading is T4 falsified  
**Source:** papers/notes/Mobius_Screw_Electron.tex abstract and sec 1-2  
**Also:** Mobius screw, Mobius-screw electron (framed unknot), Mobius-screw soliton, Möbius-screw electron, Sl = 2 ↔ g = 2, framed (2,1) unknot, framed unknot model, framed-unknot electron model

### P_alpha (alpha preformation factor)

The standing-wave mode-overlap fraction for the alpha configuration entering the decay rate lambda = nu * P_alpha * e^(-2W); in the decay note it is extracted from Geiger-Nuttall intercepts and measured/predicted lifetime ratios (mean log10 P_alpha = -2.03 +/- 0.85), explicitly not predicted from first principles there.

**Status:** extracted from data, not predicted (stated explicitly)  
**Source:** papers/notes/Flag_Condensate_Nuclear_Decay.tex sec 4.2 and Remark 'Status of P_alpha'  
**Also:** P_alpha^ext, alpha preformation amplitude, preformation factor

### P_model (standing-wave overlap proxy)

A geometric/structural proxy for alpha preformation: the normalized squared overlap on [0,R] between the confined l=0 flag reduced radial mode u_in(r) = r j0(pi r/R) (Dirichlet at R) and an alpha-cluster radial trial u_alpha. Flat-Gaussian baseline gives mean log10 P_model = -0.3905, Pearson r = +0.8882 against extracted log10 P_alpha, RMS residual 1.7705 at S=1. Explicitly not a first-principles shell-model or R-matrix spectroscopic factor.

**Status:** T3 on stated set; proxy, no many-body uniqueness claimed  
**Source:** papers/notes/Flag_Condensate_Palpha_Overlap.tex abstract and secs 2-4  
**Also:** P_model = |<u_in|u_alpha>|^2, overlap proxy, standing-wave overlap proxy

### Phase slip / phase-slip channel

The geometric phase defect across the throat that links interior standing structure to exterior travelling structure; quantified by the Gamow integral W and realized as Bogoliubov mode mixing with |beta/alpha|^2 = e^(-2W). The electron note identifies the same formal object in the framed unknot's high-torsion region ('the phase-slip channel is the same formal object'), as a structural identification only.

**Status:** structural link; no new numerical fits claimed in the electron note  
**Source:** papers/notes/Mobius_Screw_Electron.tex sec 5; papers/notes/Flag_Condensate_Nuclear_Decay.tex sec 3-4  
**Also:** geometric phase slip, phase-slip transfer-matrix picture

### Polymorphic quantum flags

The programme's core correction to popular 'every plausibility in parallel' MWI language: one Phi substrate supporting many phase/mode configurations after spectral bifurcation — mode polymorphism on one session, not literal ontological world multiplication; offered as an alternative reading, not a disproof of MWI or string theory.

**Status:** definition-only (RC1 alternative reading)  
**Source:** papers/notes/Density_Engine_Many_Worlds.tex sec 4.1, lines 199-235  
**Also:** polymorphic flags, polymorphic mode lanes

### RC1 claim discipline

The Flag-Condensate programme's scoping regime separating (1) model claims — finite statements on stated manifolds with cited numerics, (2) structural parallels — the same template across domains without identity claims, and (3) metaphor / sovereign framing — narrative energy without physics proof. RC1 remarks mark exactly which layer each passage belongs to.

**Source:** papers/notes/Density_Engine_Many_Worlds.tex sec 1, lines 76-106; papers/notes/Klein_Foam_Monad.tex Remark 1.1 (RC1 scope)  
**Also:** RC1, RC1 scope

### Sl=2 <-> g=2 identification

The Mobius-screw note's proposal to identify the framed unknot's self-linking number 2 with the tree-level Dirac gyromagnetic ratio g=2 as a 'topological bookkeeping statement'. KILLED: the Framing Transformer shows the spin content of Sl is its parity alone (sigma = (-1)^(Sl+1)), so Sl=2 and Sl=0 lie in the same pi_1(SO(3)) class and the value 2 carries no spin information that 0 does not; recorded as falsified in the Elimination Ledger (entry 2026-07-26).

**Status:** T4 falsified (KILLED, T2 structural / T1 numerical per ledger)  
**Source:** papers/notes/Mobius_Screw_Electron.tex sec 3.3 and Remark 'Superseded' (lines 158-196); papers/notes/Framing_Transformer_Spin_Parity.tex Corollary 1 and Remark 'Status change'; docs/Elimination_Ledger.md line 518  
**Also:** g <-> Sl identification, geometric origin of g=2

### Sovereign framing

The RC1 label for the metaphor/narrative layer of the programme (density-engine language, Monad recursion, DAW lanes, RPG quest/karma analogies): 'useful for programme coherence, not a substitute for domain-specific verification,' and never an assertion that the metaphors prove physics.

**Source:** papers/notes/Density_Engine_Many_Worlds.tex sec 1 item 3 and sec 3.2, lines 88-91, 190-194

### Spectral bifurcation

The cluster's reinterpretation of nuclear decay: the transition of the flag field from a confined standing-wave phase lock inside the throat (phi and pi quadrature-locked, energy localized) to an exterior travelling wave (phi and pi propagating together in phase), driven by geometric phase slips across the throat. Replaces particle-based tunneling axioms.

**Status:** T3 on stated 14-isotope set (slope); model claim  
**Source:** papers/notes/Flag_Condensate_Nuclear_Decay.tex abstract and sec 2.2-2.3  
**Also:** decay as spectral bifurcation

### Throat

Shared core term of the cluster: in the nuclear note, the colour-confining interior region r < R where the flag field is bound as a standing-wave lock, endowed with the AdS-like warped metric ds^2 = (R^2/r^2)dr^2 + (r^2/R^2) eta dx dx; in the electron model, the high-torsion region of the framed unknot (closest approach rho_min = R - a, shrinking to zero as a -> R).

**Source:** papers/notes/Flag_Condensate_Nuclear_Decay.tex sec 2.2 and 3.1; papers/notes/Mobius_Screw_Electron.tex sec 5; papers/notes/Framing_Transformer_Spin_Parity.tex sec 6.1  
**Also:** colour-confining throat, high-torsion throat, nuclear throat

#### Supporting vocabulary

- **(2,1)-torus embedding (screw centerline)** — The closed curve r(phi), phi in [0,4pi), with components ((R + a cos(phi/2))cos phi, (R + a cos(phi/2))sin phi, a sin(phi/2)); reparameterised by t = phi/2 it winds p=2 times in longitude and q=1 time in latitude on the (R,a) torus. An earlier draft mislabelled it a '(1,2)-torus knot'; the order matters for reading Sl = p*q. *(T3 numerically confirmed in Framing Transformer; papers/notes/Mobius_Screw_Electron.tex sec 2.1-2.2 (eqs r-phi, r-t) and Remark 'Correction of winding order')*
- **Annulus / thin-ring baseline capacitance C_ann** — The baseline capacitance model C_ann = 2 pi eps0 R / (ln(8R/a) + 1) treating the double-cover geometry as an effective annular conductor; under the self-stress match it collapses to alpha^-1 = (ln(8R/a)+1)/2, so matching CODATA forces the extreme aspect ratio a/R ~ 2.039e-118 (a tuning of the cutoff, not a geometric prediction of a). *(T3; CODATA match only at tuned extreme cutoff; papers/notes/Mobius_Ribbon_Capacitance.tex sec 3.1; papers/notes/Mobius_Screw_Electron.tex eq (C))*
- **BIE Mobius collocation C_BIE** — Constant-panel single-layer boundary-integral-equation collocation at unit potential on a discretized Mobius ribbon X(u,v) = r(u) + v n(u) about the (2,1) centerline, with a torus-based half-twist frame stable against Frenet flips; reported only on the panel-resolved window 5e-3 <= a/R <= 0.25. At moderate aspect it sits near the disk scale C ~ 8 eps0 R, giving alpha^-1 = O(1), not O(137). *(T3; papers/notes/Mobius_Ribbon_Capacitance.tex sec 3.3 and 4.1)*
- **Capacitance estimate of alpha** — Treating the Mobius ribbon as a double-cover annular capacitor with C ~ 2 pi epsilon_0 R / (ln(8R/a) + 1) and self-stress matching E_cap = (e/2)^2/(2C) = m_e c^2 yields alpha^-1 approx 137.036 under stated approximations; reported as cutoff- and charge-split-sensitive, 'as-implemented, not as a uniqueness theorem for alpha.' *(T3-style model estimate (explicitly not a uniqueness claim); papers/notes/Klein_Foam_Monad.tex sec 3.4, lines 173-195)*
- **Channel A (parametric spectroscopic factor)** — Refinement channel that extracts per-isotope S_i = P_ext/P_model as a diagnostic and fits predictive parametric log10 S(A,Z) and log10 S(R) by least squares, evaluated by leave-one-out; on the stated set S(A,Z) achieves LOO RMS 0.2862, the largest residual reduction among non-tautological protocols (vs global-S RMS ~0.82). *(T3; predictive power scoped to the original 14-isotope set; papers/notes/Flag_Condensate_Palpha_Refined.tex secs 3 and 6)*
- **Channel B (self-consistent WS+Coulomb eigenmode)** — Refinement channel replacing the phenomenological alpha trial by the l=0 eigenmode of V_WS + V_C on [0,R] with Dirichlet boundaries (finite-difference Sturm-Liouville), the well depth V_0 adjusted so the ground eigenvalue equals Q_alpha (a box-resonance surrogate, not a complex Gamow eigenphase). Raises Pearson r to +0.9676 but leaves global-S RMS essentially unchanged (0.8257). *(T3; papers/notes/Flag_Condensate_Palpha_Refined.tex sec 4)*
- **Channel C (Gamow outgoing boundary)** — Refinement channel extending the radial domain to [0,b] (outer Coulomb turning point) and replacing the hard wall at R with a Robin outgoing match at r = b from the exterior WKB slope, overlap support still [0,R] with throat weight. On the stated set it does not improve global-S RMS versus Channel B (identical r = +0.9676, RMS = 0.8257). *(T3; no improvement under the documented E0 = Q_alpha protocol; papers/notes/Flag_Condensate_Palpha_Refined.tex sec 8)*
- **Conformal strip-to-annulus model C_conf** — Revision of the cutoff geometry: a rectangular double-cover strip of length L = cover*2piR (default cover = 2) and width 2a is sent by the exponential map to an annulus of modulus rho = exp(2a/(cover R)); the resulting mean radius and effective half-width are inserted into the same logarithmic thin-ring scheme. CODATA match requires a/R ~ 3.8e-237. *(T3; papers/notes/Mobius_Ribbon_Capacitance.tex sec 3.2)*
- **Extended isotope catalog (n=29)** — Robustness check adding fifteen alpha emitters from NNDC/NuDat tabulations to the original 14: throat+WS LOO RMS for parametric S(A,Z) degrades from 0.286 to 1.355; coefficient signs hold but magnitudes shift, so parametric-S predictive power is explicitly scoped to the original stated set under the mixed extraction protocol. *(T3; documented degradation (honest negative); papers/notes/Flag_Condensate_Palpha_Refined.tex sec 9)*
- **Four-domain phase-defect unification** — The claim that nuclear decay, Hawking radiation, electroweak sphaleron transitions, and superconducting fluxon nucleation are structurally parallel geometric limits of one phase-defect mechanism (shared phase defect W, Bogoliubov mode mixing, exponential rate); applying the identical transfer-matrix formulation to a Schwarzschild horizon with kappa = c^4/(4GM) recovers T_H = hbar*kappa/(2 pi k_B). Explicitly a unification of 'mechanism shape', with physical identity beyond the structural parallel not claimed. *(structural parallel only (stated); Hawking recovery shown analytically; papers/notes/Flag_Condensate_Nuclear_Decay.tex sec 6 and Table 2)*
- **Four-domain phase-defect unification table** — The table (reproduced from the nuclear-decay companion) reading nuclear alpha decay, black-hole Hawking radiation, electroweak sphalerons, and superconductor fluxon nucleation as four lanes of the same Bogoliubov transfer-matrix form, each with a stated phase defect W; 'absolute physical identity beyond shared transfer-matrix form is not claimed,' and the sphaleron and fluxon rows are programme placeholders. *(structural parallel only (per its own caption); papers/notes/Density_Engine_Many_Worlds.tex sec 5, Table 4 (tab:unification), lines 337-365)*
- **Frame-Hopf map (one quaternion curve)** — Needham's construction by which a framed curve, naively 3+1 pieces of data, is a single quaternion-valued curve q(phi) on S^3 from which the framing and remaining frame leg are recovered by conjugation alone (U = q e_x q-bar, V = q e_z q-bar); reconstruction verified to 3.3e-16 with |q| = 1 to 2.2e-16. *(T3 verified; papers/notes/Framing_Transformer_Spin_Parity.tex sec 7.2; code/framed_unknot/one_object.py)*
- **Gamow phase defect W** — The cumulative geometric phase mismatch across the barrier, W = integral_R^b kappa(r) dr with kappa = sqrt(2 mu (V - E))/hbar, evaluated analytically as W = eta_S [arccos(sqrt(R/b)) - sqrt((R/b)(1 - R/b))] with Sommerfeld parameter eta_S; the transmission is T = e^(-2W) (Gamow/WKB). *(T3 cross-validated (analytic vs Simpson vs transfer matrix) on 14 isotopes; papers/notes/Flag_Condensate_Nuclear_Decay.tex sec 3.2)*
- **Geiger-Nuttall linearity result** — On the stated 14-isotope set (212Po to 244Cm), regression of ln(lambda) against Z/sqrt(E) gives R^2 = 0.9939 (measured) and a predicted-to-measured slope ratio of 1.0000, documenting that the decay slope is geometric (throat potential curvature) while the intercept encodes the data-extracted preformation amplitude. *(T3 numerical, scoped to the stated set; papers/notes/Flag_Condensate_Nuclear_Decay.tex sec 5.1)*
- **Hypercone (Klein-foam sense)** — A self-intersecting Klein-bottle vortex in the flag condensate — a Mobius-twisted coring screw that induces phase slips at its throat and deposits residual slag; the basic structural unit of the Klein foam. Distinct from the spectral 'hypercone projection' of the critical-line note. *(papers/notes/Klein_Foam_Monad.tex Postulate 2.2, lines 89-96)*
- **Instanton action deformation delta-S(R)** — The deviation of the Euclidean action from the flat-space BPST value S_0 = 8 pi^2/g^2 caused by the throat radius R breaking conformal invariance on the AdS-like warped throat metric: S_E = S_0 + 2 integral_R^b kappa(r) dr, with delta-S(R) >> S_0 dominating in the semiclassical limit R << b. Identifies the Gamow factor as a geometric action deformation. *(model derivation; papers/notes/Flag_Condensate_Nuclear_Decay.tex sec 3.1)*
- **Lane density rho_lane** — On a stated throat or routing manifold, rho_lane(r) = |Phi(r)|^2 / V_eff(r): phase-structure content per unit geometric route, finite on each cited manifold; on the nuclear throat it tracks confined standing-wave content before spectral bifurcation, on the electron annulus it reads stored twist energy per geometric turn. *(papers/notes/Density_Engine_Many_Worlds.tex sec 2.1, Definition 2.1, lines 113-126)*
- **Laplace-eigenspace relocation of spin-1/2** — The note's positive result about where spin-1/2 actually enters: the four quaternion coordinates restricted to S^3 = SU(2) are exactly the first nonzero eigenspace of the Laplace-Beltrami operator (Delta x_i = -3 x_i, degeneracy 4), which under SU(2)_L x SU(2)_R is the (1/2,1/2) representation. Spin enters through representation theory - 'which was never a geometric claim about the electron's shape' - consistent with Levy-Leblond's location of g=2. *(T3 measured (-3.00000, max error 8e-7) + representation theory; papers/notes/Framing_Transformer_Spin_Parity.tex sec 7.3 and Remark 'The relocation')*
- **Lisp-deterministic** — The RC1 reading of counterfactuals in flag ontology: polymorphic flags are deterministic, not parallel-world stochastic — 'would/could have if x' reads as opcodes on a fixed substrate, conditional paths (if/when/unless on phase geometry) in one deterministic evaluation context, an 'opcode table on Phi'. *(papers/notes/Density_Engine_Many_Worlds.tex sec 4.1, lines 208-214)*
- **Nested determinants** — The sovereign-framing picture of branching: one playthrough substrate with a stack of conditional flags (RPG quest/karma/reputation language only), where hierarchical guard predicates gate which opcode paths are admissible and outer layers gate inner ones — deterministic given the guard stack, not parallel save files all running. *(papers/notes/Density_Engine_Many_Worlds.tex sec 4.1, lines 216-229)*
- **No-go for geometric g (g=1 result)** — The successor test run after the T4 kill: for any closed curve traversed by a particle with uniform charge-to-mass ratio, mu and <L> are proportional to the same vector area, so g = 1 exactly, independent of winding, framing, twist, or throat. Obtaining g != 1 requires decoupling the charge and mass distributions - stated as a better-posed target than looking for a 2 in the geometry. *(T2 exact (classical orbital g-factor) + T3 numerics; papers/notes/Framing_Transformer_Spin_Parity.tex sec 6 (eq g1) and Corollary 'No-go for geometric g'; code/framed_unknot/moment_ratio.py)*
- **Parity law** — For (p,q) torus curves with torus framing, sigma = (-1)^(p+q) = (-1)^(Sl+1): the spin-relevant content of the self-linking number is one parity bit. The law is standard in the framed-curve and Kirby-calculus literature (Needham; Gompf-Stipsicz); the note's contribution is its evaluation on this curve. The double cover of the Mobius screw comes from the odd meridian winding q=1 (the phi/2 half-angle), not from the product pq. *(T2 (known result, verified here); control family reproduces it exactly; papers/notes/Framing_Transformer_Spin_Parity.tex sec 5, eqs (parity),(parity2) and sec 9 'Relation to the established literature')*
- **Phase slip** — The defect event at a hypercone throat in which confined condensate structure re-releases: most energy radiates as difference tones (the 'Tartini' channel) and a residual fraction deposits as slag; the phase-slip / throat / eigen-path pattern is the template postulated to recur across electron, nuclear, and cosmological scales. *(papers/notes/Klein_Foam_Monad.tex sec 4.1, lines 200-206; papers/notes/Density_Engine_Many_Worlds.tex sec 3)*
- **Scale ladder (micro / meso / macro)** — The interpretive ladder on which one phase-defect template recurs: micro (framed unknot electron, Sl = 2), meso (nuclear colour throat, Gamow W), macro (Schwarzschild horizon, Hawking T_H) — at each rung, confined standing wave -> phase slip -> Bogoliubov mode mixing -> observable, with numerics scoped per row to companion notes. *(papers/notes/Density_Engine_Many_Worlds.tex sec 3.1, Table 1 (tab:ladder), lines 161-186; also Klein_Foam_Monad.tex sec 6)*
- **Self-linking identification Sl = 2 -> g = 2** — The geometric identification of the electron's magnetic-moment doubling with the natural torus-framing self-linking number Sl = Tw + Wr = p·q = 2, while angular momentum remains single-cycle, yielding g = 2 'at tree-level analogy' — stated as a geometric identification inside the model, not a derivation of the QED vertex. *(model claim (scoped); papers/notes/Klein_Foam_Monad.tex sec 3.3, lines 150-171)*
- **Self-linking number Sl (Calugareanu identity)** — For a closed framed curve, Sl = Tw + Wr (twist plus writhe); under the natural torus framing of a (p,q)-torus curve, Sl = p*q, giving Sl = 2 for the Mobius screw. Numerically confirmed by two independent routes: Tw = -1.0338, Wr = -0.9662, Tw+Wr = -2.000000, and the Gauss linking integral with the framing pushoff returns -2.000000 (the sign records that the parameterised embedding is left-handed). *(T3 confirmed (|Sl| = 2); only |Sl| and its parity are invariant; papers/notes/Mobius_Screw_Electron.tex sec 3; papers/notes/Framing_Transformer_Spin_Parity.tex sec 3)*
- **Shuman Resonance** — The postulated fundamental standing wave (torsional mode) of the Klein foam, named as a universal geometric analogue of terrestrial Schumann resonances; the note states the spelling deliberately preserves the programme name. Conscious beings are characterised as self-sustaining, nitinol-like phase-slip loops resonant with this tone (marked interpretive, not a neuroscience claim). *(definition-only (interpretive ontology); papers/notes/Klein_Foam_Monad.tex sec 5, lines 256-267)*
- **Slag** — Residual condensate energy trapped in the Casimir cavity of a hypercone's twisted walls during phase slips, identified with rest mass: m = delta · E_condensate / c^2 with delta ~ e^{-2W} for a Gamow-like barrier integral W. 'Mass as slag' is the ontology's reading of mass. *(papers/notes/Klein_Foam_Monad.tex sec 4.1, lines 200-212)*
- **Spin radius** — The input scale R = hbar/(2 m_e c) fixed by requiring spin angular momentum hbar/2 for mass m_e circulating at speed c on a circle of radius R; explicitly an order-of-magnitude input to the geometric model, not an independent prediction. *(input scale, not a prediction; papers/notes/Mobius_Screw_Electron.tex sec 3.4, eq (R))*
- **Spinorial holonomy sigma** — The sign sigma = q(4pi)/q(0) in {+1,-1} that decides whether the SU(2) lift of the frame loop closes after one circuit of the curve; sigma = -1 means the frame loop represents the non-trivial class of pi_1(SO(3)) = Z/2 (spinorial, two circuits required). For the Mobius screw sigma = -1, proved in closed form via the quaternion lift and confirmed numerically three independent ways. *(T2 proved, T3 confirmed; survived; papers/notes/Framing_Transformer_Spin_Parity.tex eq (sigma) and Proposition 1 (Spinorial holonomy))*
- **Standing-wave phase lock** — The interior nuclear state: phi_in and pi_in share the spatial profile A j_l(kr) Y_lm but are strictly quadrature-locked in time (90 degrees out of phase), so the energy density is constant and localized; 'no localized physical particle exists within the interior --- only a stationary saturation node of the flag field.' *(papers/notes/Flag_Condensate_Nuclear_Decay.tex sec 2.2 (lines 76-86))*
- **Throat / throat sieve** — The constriction of a hypercone where phase slips occur (nuclear decay reads a 'colour throat' with Gamow action W); the throat sieve is the network of active voxel cells formed when the Klein foam is discretised. *(papers/notes/Klein_Foam_Monad.tex Postulate 2.2 line 95 and sec 4.1; papers/notes/Density_Engine_Many_Worlds.tex Table 1)*
- **Throat weight w(r) = R/r** — The radial measure factor sqrt(g_rr) = R/r taken from the AdS-like throat metric of the nuclear note, replacing the flat dr measure in the preformation overlap integrals; for reduced modes u ~ O(r) near the origin the weighted integrands remain integrable. *(T3; changes absolute scale but correlation essentially unchanged (delta r ~ -0.0007); papers/notes/Flag_Condensate_Palpha_Throat_Overlap.tex sec 2)*
- **Torus framing** — The natural framing of a torus curve given by the torus surface normal U(phi) = (cos(phi/2)cos phi, cos(phi/2)sin phi, sin(phi/2)); because the curve lies in the surface, T.U = 0 holds identically (verified to 2.2e-16). *(T3 verified; papers/notes/Framing_Transformer_Spin_Parity.tex sec 2, eq (framing))*
- **Transfer-matrix Bogoliubov extraction** — The numerically stable instrument for extreme transmissions (T ~ 1e-40): slice the barrier [R,b] into N layers, each with a real 2x2 transfer matrix (cosh/sinh in forbidden regions, cos/sin in allowed ones, det M = 1), compute T from the product's matrix elements, and read the barrier as a Bogoliubov mixer b_k = alpha_k a_k + beta_k a_-k^dagger with T = |beta/alpha|^2 = e^(-2W). *(T3 verified across 14 alpha emitters; papers/notes/Flag_Condensate_Nuclear_Decay.tex sec 4)*
- **Woods-Saxon alpha-cluster trial** — The primary alpha radial trial of the throat-overlap note, u_alpha(r) = r / (1 + e^((r - R_alpha)/a_WS)) with R_alpha = r0 * 4^(1/3) ~ 1.905 fm and a_WS = 0.55 fm, replacing the Gaussian/harmonic-oscillator 0s packet of the baseline proxy (kept for comparison). *(T3 model choice, documented not unique; papers/notes/Flag_Condensate_Palpha_Throat_Overlap.tex sec 3.2)*


## Number representation and the FF06 thread

The relational-representation program: shapes, flattenings, the seam, and the boundary between multiplicative and additive structure. Primary source: `papers/later_FF06_series/`.

### Boundary law

The organizing law of When a Number Lies: relational representation strictly improves on scalar abstraction if and only if (i) an exact underlying relation exists, (ii) it is a product, a ratio, or a non-transitive graph rather than a sum, and (iii) the scalar projection breaks (overflow, underflow, cancellation, nonexistence) or the question is exact and the scalar destroys needed structure. Stated as an empirical-structural characterization, not a formal theorem.

**Status:** empirical-structural; each clause witnessed  
**Source:** papers/later_FF06_series/When_a_Number_Lies.tex sec 4 (lines 144-153)

### Conditional-uniformity height floor T_min = (2 pi e)^d / q

The program's claimed height floor below which 'too few zeros exist to resolve the d-fold denser prime spectrum' for an L-function of degree d and conductor q. The scaling law is falsified (T4) in its degree dependence: at d = 2 (Dedekind zeta of Q(i)) the framework floor 72.93 sits above 51 actual zeros, while the standard analytic-conductor floor 2 pi e q^{-1/d} = 8.54 is correct; the d = 1, q = 1 value 2 pi e ~ 17.08 survives as a genuine analytic invariant - the degenerate case where wrong and right degree dependence coincide.

**Status:** T4 (scaling law falsified); d=1 floor survives  
**Source:** papers/later_FF06_series/The_Elimination_Ledger.tex sec 4.1 (lines 177-237)  
**Also:** T_min, height-floor scaling law

### Convolution seam

The characterization of the additive/multiplicative boundary as convolution - the operation that adds indices while multiplying values, ( a x^i )( b x^j ) = ab x^{i+j} - which is the native inhabitant of the seam. The seam is crossed by generating functions (Euler's identity sum p(n) x^n = prod (1-x^k)^{-1}, verified coefficient-wise for n <= 30) for aggregate density, but remains uncrossable for individual identity: convolution yields how many, never which one.

**Status:** components T1; the identification 'the seam is convolution' T3, deliberately not promoted  
**Source:** papers/later_FF06_series/The_Reversible_Flattening.tex sec 6 (lines 165-198); Process_Record sec 4.3  
**Also:** Additive seam, Seam, Seam law, addition has no shape, density-not-identity crossing, multiplicative-additive seam law, seam density law, the additive wall, the seam, the seam is convolution (keystone)

### Delta-I = c identity

The program's stated load-bearing conjecture identifying the information asymmetry Delta-I with the renormalization-group c-function. The Elimination Ledger retires it as stated (T4): with Delta-I as the bounded routing scalar it is falsified for every theory with c > 1; as transfer-entropy asymmetry it fails on sign, fixed-point value, and category (temporal/directed vs static/spatial); and the only surviving reading is a restatement of the Casini-Huerta entropic c-theorem - no reading is both novel and true. One Mechanism, Many Forms nonetheless carries it as Link 3, the central open identification on which the cross-domain unification is conditional.

**Status:** T4 as stated (Elimination Ledger); carried as T2/T3 open conjecture (One Mechanism)  
**Source:** papers/later_FF06_series/The_Elimination_Ledger.tex sec 4.2 (lines 239-283); One_Mechanism_Many_Forms_Sigma.tex sec 2 Link 3  
**Also:** Link 3, information-asymmetry / central-charge identity

### Density vs identity

The split unifying the criterion and the seam: a homomorphism preserves how parts combine (the density side) while injectivity is the additional condition that distinct objects have distinct images (the identity side); a non-injective homomorphism carries density and loses identity. Reversibility = homomorphism (density) + injectivity (identity), and the seam is where injectivity fails.

**Status:** T2 (identity/density split theorem)  
**Source:** papers/later_FF06_series/The_Reversible_Flattening_Monograph.tex sec 6 Theorem (lines 208-216)  
**Also:** identity/density split

### Elimination Ledger

The append-only catalogue of falsifications, refractions, and survivals in the ACS/AISO program: a single elimination campaign of pre-registered kill tests, each with a falsification criterion fixed before running, targeting the program's own load-bearing claims first. It retired the program's two highest-collapse claims (Delta-I = c and the height-floor scaling law) and gathered all prior dead ends into one table.

**Status:** the ledger itself is methodology; individual verdicts T1-T4  
**Source:** papers/later_FF06_series/The_Elimination_Ledger.tex abstract and sec 1 (lines 22-61)  
**Also:** Negative ledger, falsified claims ledger, kill ledger, kill-queue, negative results as first-class outputs

### FF06 series paper labels

The corpus's internal naming scheme for its papers, used for cross-reference: FF06a (Colour from Gravity / Palatini bracket), FF06b and FF06b' (Riemann spectral side; Spectral Witness Survival and the Transport Obstruction), FF06c (the Inversion Arc), FF06e (the Shuffle Knife / Spectral Rigidity and Shuffled Spacing Discriminant), FF06g (The Geometry Engine), FF06h (When a Number Lies), FF06i (The Reversible Flattening), FF06J (the consolidating Monograph), FF06K (the Process Record), plus LF01 (the L-function finite-window localisation note) and N3 (the prime-gap operator).

**Source:** papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex footer (lines 600-607); One_Mechanism_Many_Forms_Sigma.tex footer (lines 270-276)

### Form/function split

The categorisation of spectral statistics into 'form' (spacing, counting, shape - properties of the universality class, shared by every GUE sequence, registering 0.4-1.0 sigma against surrogates) and 'function' (the object-specific arithmetic content - the arithmetic witness at ~11,500 sigma, or positions prime-governed at 122 sigma). The arithmetic content of the zeros lives entirely in where the levels sit, not in how they are spaced.

**Status:** survived; confirmed by two independent routes at 10^5 scale  
**Source:** papers/later_FF06_series/Three_Layer_Decomposition.tex sec 4 (lines 105-120); One_Mechanism_Many_Forms_Sigma.tex sec 3  
**Also:** Form/Function cut, Form/Function ontology, INV-3, form vs function, form/function asymmetry, form/function coupling

### Geometry Engine

A 91-line reference implementation of the shape representation in which multiplicative operations are computed from the box geometry without forming the integer value; all twelve of its operations are verified exact against integer ground truth (12/12, including the round-trip volume(shape(n)) = n). Benchmarked across ten ontologies, it wins where the standard method flattens rich multiplicative structure and loses, flatly reported, elsewhere.

**Status:** T1  
**Source:** papers/later_FF06_series/The_Geometry_Engine.tex abstract and sec 2 (lines 87-110)  
**Also:** FF06g, reference engine, shape engine

### Pre-registration and the no-tuning rule

The rule that thresholds, kill conditions, and the meaning of operational terms are fixed before seeing results, and that tuning a filter or encoding to the known answer is forbidden - where tempting, the rule was stated explicitly in the test harness itself. Every kill test states its falsification criterion before execution, accompanied by negative controls and decoys.

**Source:** papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 2.3 (lines 115-119); The_Elimination_Ledger.tex sec 2.4  
**Also:** kill condition, pre-registered test

### Relational Representation Principle

The principle that if a computation produces a scalar s that is a lossy or non-invertible projection of an underlying structured object R (a product, a ratio, a graph), then computing the desired answer directly on R is more accurate, and often more tractable, than forming s and operating on it. Some scalars are 'shadows': the magnitude lives in the projection, not the object.

**Status:** characterized with predictive boundary; survived gauntlet  
**Source:** papers/later_FF06_series/When_a_Number_Lies.tex sec 1 (lines 57-67)  
**Also:** relational over scalar

### Reversible flattening (the thesis)

The central thesis of the later FF06 series: the algebraic flattening of a relational object to a scalar is losslessly reversible when the operation producing the scalar is an injective homomorphism into a pre-specified, independently-meaningful structure - the homomorphism carries density (how parts combine), the injectivity carries identity (which object), and reversibility requires both. It is a falsifiable empirical principle stated in the forward direction only; the converse was falsified (Cantor pairing).

**Status:** forward direction verified (30/30 predictive test); converse T4; survived after three contractions  
**Source:** papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 3 Principle 1 (lines 132-138); The_Reversible_Flattening_Monograph.tex Criterion 3.1  
**Also:** FF06i (parent paper), the homomorphism criterion

### Shape

A box encoding a positive integer's multiplicative structure as a finite map {p_i : e_i} from prime sides to positive exponent dimensions, with volume prod p_i^{e_i}; the empty box is the unit 1, and zero and negatives are not boxes. Multiplicative questions become geometric: multiply = merge, divisibility = containment, gcd/lcm = common/enclosing box, primality = atomic box.

**Status:** T1 (all operations verified exact)  
**Source:** papers/later_FF06_series/The_Geometry_Engine.tex sec 2 Definition 1 (lines 72-76)  
**Also:** box, prime box, prime-signature representation

### Three-layer decomposition

A decomposition of the first 10^5 Riemann zeros into three structurally independent layers, each with a different governor: the average density is the smooth Riemann-von Mangoldt term (analysis, no arithmetic); the positions (the fluctuation S(T) of the counting function about its mean) are owned by the primes via the explicit formula; and the local spacings are pure GUE, the arithmetic-blind universality class.

**Status:** positions T1 (+122 sigma vs control); spacings labeled T2; survived  
**Source:** papers/later_FF06_series/Three_Layer_Decomposition.tex sec 1 (lines 33-53)  
**Also:** density/positions/spacings decomposition

### Tomographic invariance engine

The central instrument of the elimination campaign: a battery that varies the measuring instrument and asks which quantities move, applied numerically (T1 verdicts) or structurally by argument from a quantity's construction (T2 verdicts). Before use on uncertain calls it was calibrated against known invariants and refractions, with negative controls and decoy targets so the engine could not become its own refraction.

**Status:** calibrated instrument  
**Source:** papers/later_FF06_series/The_Elimination_Ledger.tex sec 2.3 (lines 97-111)  
**Also:** tomographic kill-criterion

### Two faces of zeta

The theorem that the integer engine (prime boxes, the Euler product) and the analysis engine (zero/pole geometry, the Hadamard product) are one engine seen through the two products of the Riemann zeta function, with the explicit formula as the dictionary between them - verified in both directions on the real first 10^5 zeros (positions from primes at +122 sigma; the prime staircase psi(x) from zeros, agreeing at every tested x).

**Status:** T1 both directions  
**Source:** papers/later_FF06_series/The_Geometry_Engine.tex sec 7 Theorem 3 (lines 242-256)  
**Also:** loop closure

#### Supporting vocabulary

- **30-domain predictive test** — A test of whether the homomorphism criterion predicts reversibility outside the examples it was built from: 30 domains were chosen, predictions locked before scoring, then checked against ground truth. The original criterion scored 28/30; the two misses (persistent homology and list-to-multiset) were homomorphic but non-injective, and adding the injectivity qualifier took the score to 30/30 - evidence the criterion picks out a real class rather than being fitted retrospectively. *(T1 (28/30 original, 30/30 corrected); papers/later_FF06_series/The_Reversible_Flattening_Monograph.tex sec 6 (lines 188-216); Process_Record sec 6)*
- **add_exit / GEOMETRY_EXIT** — The explicit, named mechanism by which the shape engine handles addition (which has no shape): it computes the value, refactors, and re-enters geometry, emitting a GEOMETRY_EXIT flag so that every additive step is visible as a departure from the geometric world. Addition is never hidden inside a geometric costume. *(T1 component of engine; papers/later_FF06_series/The_Geometry_Engine.tex sec 2.1 (lines 120-123))*
- **Additive depth** — The unique invariant of a number's additive structure: the minimal number of primes summing to it, which is 1, 2, or 3 (every prime has depth 1; every even >= 4 has depth 2 by Goldbach, verified empirically; every remaining odd has depth 3 by Helfgott's weak Goldbach theorem). Verified over [2, 10^5). *(T1 at tested scale; papers/later_FF06_series/The_Geometry_Engine.tex sec 5 (lines 199-213))*
- **Advantage map** — The measured head-to-head race of the geometry engine against the standard method for each of ten ontologies of applied mathematics and computer science, reporting wins (e.g. multiplicative functions 81x, binomial prime structure 13x) and losses (smoothness 106x slower, sieving 73x slower) flatly, with no advantage at the factoring entry wall by design. *(T1 (measured); papers/later_FF06_series/The_Geometry_Engine.tex sec 3 (lines 124-161))*
- **Adversarial gauntlet** — Four rounds of external attack on the reversible-flattening claim - language critique (3 overclaims), substance audit (5 concessions producing five of the six false walls), counterexample search (converse falsified via Cantor pairing), and final review - with grade trajectory 2/5 -> 4.5/5 -> 5/5. Each round contracted the claim; in no round was the verified core successfully challenged. *(process record; papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 6 (lines 266-302))*
- **AISO / TENT / OmniForge stack** — The program's computational/engineering stack, referenced as the live production source against which architecture-integration hypotheses are tested (four falsified, one - motif memory - survived). Components mentioned include the BRA kernel, a routing/CDCL engine, trust and Merkle layers, and a motif-memory subsystem. *(definition-only (external system); papers/later_FF06_series/The_Elimination_Ledger.tex abstract; When_a_Number_Lies.tex sec 6 (lines 185-191))*
- **AISO motif-memory integration** — The first architecture-integration hypothesis to survive (after an explicit 0-for-4 record): encoding memory 'motifs' as shapes, tested by a pre-registered harness with a discriminating self-test against 45 live motifs and 990 pairs. Composition (write side) matched exponent-addition on 100% of pairs with 0 collisions; retrieval-via-gcd (read side) was falsified at 55.15% accuracy against an 83.13% majority baseline - the homomorphism lives in the event/keyword-count layer, and statistical embedding handles retrieval. *(composition T1 pass; retrieval T4; papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 8.2 (lines 351-391))*
- **Amplitude-matched random-frequency control** — The decisive control for the position reconstruction: the log-prime frequencies log p are replaced by amplitude-matched random incommensurable frequencies, yielding correlation 0.004 +/- 0.019 (nothing), which establishes that specifically the prime frequencies, not any oscillatory sum, reconstruct S(T) at 122 sigma over the matched null. *(T1; papers/later_FF06_series/Three_Layer_Decomposition.tex sec 2 (line 78))*
- **Analysis engine** — The transfer of the shape engine to analytic functions with poles in place of primes: the shape is {pole : order}, free structural questions are radius of convergence and best expansion center (chosen by pure geometry, farthest from all poles), the value (summing the series) remains work, and the wall is entire/lacunary functions with no finite shape. *(T3/T1 (verified on examples); papers/later_FF06_series/The_Geometry_Engine.tex sec 6 (lines 215-238))*
- **Asymmetric instrument** — The division of language models into distinct, non-interchangeable roles: an idea-generator (expansive, fluent, untrusted by default), a coder/aggregator/honest-instrument (the author of the process record), and independent critics. The generator's fluency is treated as a hypothesis, never as evidence, because a fluent proposal is the most dangerous kind. *(papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 2.4 (lines 121-127))*
- **BRA kernel verdicts** — The BRA kernel was advanced as a faster deterministic replacement for a TensorFlow Gabor wave-packet operation, with a withdrawn 489x speedup projection; measured, it is 1.37-1.82x slower (BRA f64 vs TF f32, the precision confound recorded honestly), killing the speed claim (T4). The surviving value is determinism: the integer and f64 paths are bit-identical across runs (T1). *(speed T4; determinism T1; papers/later_FF06_series/The_Elimination_Ledger.tex sec 4.3 (lines 285-315))*
- **Cantor pairing counterexample** — The adversarial counterexample that falsified the converse of the homomorphism criterion: the Cantor pairing pi(a,b) = (a+b)(a+b+1)/2 + b is a perfectly reversible bijection N^2 -> N yet is not a homomorphism into the natural componentwise structure (pi(1,2) + pi(2,0) = 11 != 17 = pi(3,2)). Reversibility therefore does not imply injective homomorphism. *(converse T4 (falsified); papers/later_FF06_series/The_Reversible_Flattening_Monograph.tex sec 3 (lines 125-127); Process_Record sec 6 Round 3)*
- **Conservation principle** — The single correctness criterion of the shape engine: every operation on shapes is admissible if and only if it conserves volume - a reshaping is exact when the volume it produces equals the value the corresponding arithmetic operation would produce. *(papers/later_FF06_series/The_Geometry_Engine.tex sec 2 Principle 1 (lines 78-82))*
- **Degenerate-case trap** — The recurring pattern named in the Elimination Ledger discussion: a claim can pass indefinitely on the degenerate slice of its parameter space where a wrong dependence coincides exactly with the right one (as the height-floor law did at d = 1); the discriminating test lives off that slice, and naming where it lives before testing is what converts a scoped survival into a clean falsification. *(pattern (illustrated at T4); papers/later_FF06_series/The_Elimination_Ledger.tex sec 7 (lines 421-425))*
- **Dominance engine** — The second realization of the relational principle for non-transitive relations: a directed dominance graph, integer and exact, supporting monotone elimination - the only faithful representation when preferences cycle, since a partial order (like box containment) cannot represent a cycle. *(T1 (verified engine); papers/later_FF06_series/When_a_Number_Lies.tex sec 2 and 5; The_Reversible_Flattening_Monograph.tex sec 10.1)*
- **Framework-constant refraction verdicts** — The tomographic classification of four ACS constants carried as 'locked': the bare values g_4 = 4/3 (generator-normalization dependent), the Barbero-Immirzi gamma = 0.274067 (counting-prescription dependent, -> 0.190206 under SO(3) counting), and the Higgs quartic lambda_phi = 2 sqrt(3)/27 (Killing-form-normalization dependent) are refractions, while the relations survive: the unification equality g_4 = g_L = g_R, the Koide-geometric origin of lambda_phi, and the dimensionless RG-invariant Yukawa ratio h-tilde/h = 2/3, the strongest invariant of the four. *(T1 (all four verdicts machine-confirmed); papers/later_FF06_series/The_Elimination_Ledger.tex sec 3 (lines 121-173))*
- **Hilbert-Polya positive specification** — The observation that if a self-adjoint H has the Riemann zeros as spectrum then (i) spacings come for free from self-adjointness, (ii) arithmetic enters through positions (H must reproduce the prime-driven S(T)), and (iii) self-duality is generated by H, not imposable on it. This selects the Berry-Keating-type position/counting route and rules out symmetrisation and diagonal-perturbation routes. *(Observation; does not construct H; papers/later_FF06_series/Three_Layer_Decomposition.tex sec 5 (lines 122-135))*
- **Measured, never projected** — The enforced discipline that a complexity argument or extrapolation is not a measurement and is never reported as one - paired with 'validate the instrument before trusting it' (a new numerical method must reproduce an independent method on a shared case before use at scale). *(papers/later_FF06_series/The_Elimination_Ledger.tex sec 2.4 (lines 115-119))*
- **Necessary spectral signatures** — Three Hilbert-Polya necessary (not sufficient) signatures machine-verified on the real zeros: nearest-neighbour spacing (KS 0.0197 to GUE vs 0.299 to Poisson), number variance / spectral rigidity (GUE log-law on 5/5 windows), and pair correlation (matching Montgomery's 1 - (sin pi r / pi r)^2 to 0.026). Stated with a hard scope wall: they do not construct an operator and do not bear on RH. *(T1, necessary != sufficient; papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 9.4 (lines 455-461))*
- **No selection regime** — The finding that no arithmetic perturbation of a self-adjoint GUE operator moves its spacing statistics toward the zeros at any strength: weak arithmetic (epsilon 0.05-0.2) is cosmetic (indistinguishable from GUE), strong arithmetic (epsilon 0.4-0.8) breaks GUE toward Poisson, and there is no intermediate regime where arithmetic is selected. *(labeled T2 in section heading; papers/later_FF06_series/Three_Layer_Decomposition.tex sec 3 (lines 86-103))*
- **Non-transitive impossibility (Condorcet instance)** — The strongest instance of the relational principle: if the pairwise majority relation contains a cycle A > B > C > A, every total order (every scalar ranking) contradicts at least one majority verdict, so the relation carries information no scalar can hold. Cyclicity is structural, not small-sample: about 7%, 43%, 78%, 99% of random electorates for 3, 5, 7, 10 candidates, and about 48% at 1001 voters with five candidates. *(T1 (exhaustive verification); papers/later_FF06_series/When_a_Number_Lies.tex sec 5 (lines 155-180); The_Reversible_Flattening_Monograph.tex sec 10)*
- **One field, two readouts** — The reading forced by bracketing the zeros with three constructions (generic GUE; a prime field on a rigid lattice; their additive sum - none reaching the zeros' corner): the GUE statistic and the prime peaks are two readouts of one object, the arithmetic fluctuation field S(T), whose local correlations give GUE and whose Fourier content gives the prime peaks - not two separable mechanisms to build and add. Scoped as a sandbox illustration, not a no-go theorem. *(T3 after two T4 framings (tension; cheap add-on); papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 9.7 (lines 508-525))*
- **Orbit observable A(tau)** — The observable A(tau) = sum_k w(gamma_k) cos(tau gamma_k) used throughout the Riemann arc - on rediscovery recognized as one object under several names: LF01's F_w, FF06b-prime's prime-dual (its load-bearing witness), and FF06e's arithmetic witness, all forms of the explicit-formula coupling of primes against zeros. *(T1 (hardened forms live in LF01, FF06b', FF06e); papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 9.8 (lines 528-531))*
- **Order-dependence / structure-retention axes** — The corrected map after the conjecture 'commutativity measures projected-away structure' was falsified: non-commutativity measures retained order-dependent structure only (cross product retains one bit of orientation; matrix products retain the whole arrangement), while commutative operations like gcd and lcm can still retain full order-independent structure. The two axes are independent, and the shape engine lives in the commutative-and-structured cell. *(strong form T4; corrected law survived; papers/later_FF06_series/The_Reversible_Flattening.tex sec 7 (lines 200-211); Monograph sec 7)*
- **Origin falsifications (phi + inverse-silver; FHT consciousness score)** — Two early, unfalsifiable artifacts of the program's fifteen-month-old intuition, re-tested against ground truth and falsified: the claim that a golden-ratio + inverse-silver combination 'structures noise' (the combination's discrepancy 0.02132 is 25x worse than phi alone at 0.00084) and the 'FHT consciousness score' (saturates to 1.0 on random noise and structure alike, discriminating nothing). Each was a real kernel wrapped in an unfalsifiable, sycophancy-reinforced story. *(T4 (both); papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 8 (lines 393-415); Monograph negative ledger)*
- **p-adic gradient (Wall 6)** — The refinement showing the seam is not a binary void: the p-adic valuation obeys the ultrametric bound v_p(a+b) >= min(v_p(a), v_p(b)), which is tight (the valuation determined exactly) whenever the summands' valuations differ (about 50% of cases) and slack only on ties. The seam is therefore a measurable gradient of structural loss, not total irreversibility - the only false wall that made the picture richer rather than smaller. *(T1 (verified 10^4 and 6x10^4 cases); papers/later_FF06_series/The_Reversible_Flattening_Monograph.tex sec 4 (lines 157-165); Process_Record sec 5.6)*
- **Peaked spectrum = diagonal prime powers** — The result that the peaked content of the explicit-formula dual periodogram on the zeros is exactly the diagonal prime-power set {k log p} at 10^7-10^8 contrast over baseline, with composites and decoys at noise level. There is a structural reason, not merely a null: the dual carries weight only on the von Mangoldt function Lambda(n), supported on prime powers, so a sum-frequency peak at log(pp') is forbidden; the off-diagonal tunnel is mapped empty. *(T2 + T3; survived; papers/later_FF06_series/The_Elimination_Ledger.tex sec 4.4 (lines 317-334))*
- **Radius / falsification surface** — The explicitly drawn boundary of the one-mechanism claim: where the identity chain is instantiated the mechanism is earned; in domains where FF06c only maps the inversion (institutions, cognition, language, biology, the theological reading) 'same mechanism' is a sharp conjecture whose test is whether the chain instantiates there - either the form/function coupling is forced or it merely resembles (a false-fit wearing the mechanism's name). *(conjecture beyond treated domains, by design; papers/later_FF06_series/One_Mechanism_Many_Forms_Sigma.tex sec 4 (lines 183-204))*
- **Reductive sweep (decoy ranking)** — Running the spectral signatures against decoys to measure discriminating power: a genuine GUE matrix spectrum remapped to the zeta density passes spacing and rigidity yet is empty of prime orbits (2.4 vs the zeros' 228.8), yielding the ranking prime-orbit peaks (strong, only arithmetic spectra) > GUE spacing/rigidity (medium, all chaotic spectra) > Maslov constant 7/8 (weak, any curve-matched sequence). *(T1; papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 9.6 (lines 476-505))*
- **S(T) counting fluctuation** — The oscillatory part of the exact zero-counting function, S(T) = N(T) - <N(T)>, where <N(T)> is the smooth Riemann-von Mangoldt mean. The explicit formula expresses it as a sum over prime powers, and the framework's claim is that the primes own it entirely (explained variance climbing 0.64 to 0.82 with a white residual, lag-1 autocorrelation 0.057). *(T1; completeness inference T1'; papers/later_FF06_series/Three_Layer_Decomposition.tex sec 1-2 (lines 35-84))*
- **Strip-mining stance** — The methodological posture of the elimination campaign: one does not prove the gold is present; one removes everything that is not gold, and what remains earns credibility by the elimination of alternatives. Destruction is made cheap and routine, and a clean kill is treated as a success. *(papers/later_FF06_series/The_Elimination_Ledger.tex sec 1 (lines 50-54) and sec 8)*
- **The 2x2 square** — The classification lens carried from the relational work to the Riemann arc: is a map homomorphic, and is it injective? Homomorphic+injective is reversible; homomorphic+non-injective is a seam (density crosses, identity is lost); non-homomorphic+injective is the Cantor corner (identity kept, structure scrambled); neither is noise. *(classification tool; cells verified per-map; papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 9.1 (lines 428-434))*
- **The critical line is not one seam** — The finding that the natural conjecture 'Re(s) = 1/2 is the seam' is false as a single label: three distinct maps live there - the reflection s -> 1-s is the Cantor corner; the prime-zero correspondence is granularity-dependent (lossless on the full set, a seam at the individual level, where dropping one zero delocalizes the reconstruction); and the genuine convolution seam, the Euler-product convergence edge, sits at Re = 1, not 1/2. *(T1/T3; single-seam conjecture T4; papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 9.2 (lines 436-444))*
- **Three contractions** — The forced shrinking of the reversible-flattening thesis through three successive forms: (1) biconditional 'iff' (converse never supported, later falsified outright); (2) forward but 'into some structure' (vacuous); (3) forward, injective, pre-specified target (final). 'The contraction is not the price of the result. The contraction is the result.' *(process record; earlier forms T4; papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex sec 3 (lines 143-158))*
- **Unique vs cardinal structure** — The two kinds of structure meeting at the seam: the multiplicative side carries unique structure (the factorization is a single canonical object, a point, an address, by the Fundamental Theorem of Arithmetic), while the additive side carries cardinal structure (the decompositions form a cloud with no canonical address, but the size of the cloud is exact and deep - the partition function p(n), e.g. p(100) = 190,569,292). Addition is not structureless; its structure is the count, not an address. *(T2/T1 components; papers/later_FF06_series/The_Reversible_Flattening.tex sec 6 Theorem 2 (lines 169-175); Monograph sec 4)*
- **Verified-optimal d(n) structure search** — The headline tractability instance: an exact branch-and-bound in exponent space with a provably admissible upper bound (budget all remaining log-room on the cheapest prime; each unit buys at most a factor of two) that finds the integer n <= N maximizing the divisor count d(n) out to N = 10^80 without ever forming n, anchored exact against brute force at four small bounds. Attribution was later corrected: the speed comes from the knapsack-on-exponents structure of highly composite numbers, not from the relational representation, which is a bystander. *(T1, with corrected attribution; two earlier versions T4; papers/later_FF06_series/When_a_Number_Lies.tex sec 3 (lines 110-119); The_Reversible_Flattening_Monograph.tex sec 9; Process_Record sec 5.2)*
- **xp as smooth skeleton** — The class-level verdict on the Berry-Keating xp operator: its semiclassical count reproduces the smooth Riemann-von Mangoldt staircase to < 0.2% (passing the necessary smooth-density condition), but xp has continuous spectrum, no discrete eigenvalues, and does not encode the prime-driven fluctuation S(T) - so 'xp alone is the operator' is killed as sufficient while 'xp as the smooth skeleton' survives. *(T2 + T3; sufficiency killed, skeleton survives; papers/later_FF06_series/The_Elimination_Ledger.tex sec 5 (lines 351-359))*


## The Deterministic AI Stack (Paper D)

The engineering arm: a discrete rewrite formalism and its planned realisation. Primary sources: `papers/ACS_Deterministic_AI_Stack_PDR.tex`, `papers/discrete_geometry_formalism.tex`.

### ACS Deterministic AI Stack

A bracket-governed, byte-reproducible software architecture in which every generative step is a Lie bracket between typed Form and Function fields, outputs are validated by a closure criterion, convergence is detected by information balance (Delta I -> 0), and compositional depth is capped at BCH order 3 via the Jacobi identity. There is no sampling and no temperature; specified in five layers and four deployable services.

**Status:** design specification (PDR v1.0)  
**Source:** papers/ACS_Deterministic_AI_Stack_PDR.tex title page and sec 1-2  
**Also:** Deterministic AI Stack, Paper D

### Bracket Engine

The stack's single generative primitive: takes a Form F and a Function Phi and produces [F, Phi] truncated at BCH order 3, with every composition journaled with cryptographic provenance. It is stateless between brackets and guarantees byte-identical reproduction for byte-identical inputs (invariant I-B1).

**Status:** specified; reference sketch in Appendix A  
**Source:** papers/ACS_Deterministic_AI_Stack_PDR.tex sec 3.3, lines 525-620  
**Also:** Composition Core

### Dynamical Epistemic Algebra

The formal specification of the ACS Deterministic AI stack as a multi-parameter, non-commuting dynamical system on matrix-valued states analyzed through iterated projection-valued observables, given by the tuple (A, S, {R_alpha}, Phi): state space, scheme set, rewrite semigroup, and observation functor. It deliberately avoids asserting a continuum geometric ontology or a strict categorical renormalization group.

**Source:** papers/discrete_geometry_formalism.tex sec 1, lines 20-50  
**Also:** discrete operator geometry stack

### Jacobi truncation

The principle that the Jacobi identity [[A,B],C] + [[B,C],A] + [[C,A],B] = 0 ensures no new independent content is generated beyond BCH order 3, which the stack uses as its bounded-depth guarantee; compositions that would exceed order 3 raise JacobiTruncationError.

**Status:** traced to 'Paper A sec 5.1 Thm' (Jacobi truncation theorem)  
**Source:** papers/ACS_Deterministic_AI_Stack_PDR.tex sec 1 table, invariant I-Phi4 lines 499-506, and Glossary  
**Also:** BCH-3 truncation, bounded-depth guarantee

#### Supporting vocabulary

- **ACS trilogy (Paper A / Paper C)** — The core paper series to which every architectural decision of the AI stack is traced: the PDR cites 'Paper A' for definitions, the Jacobi truncation theorem, closure attractor selection, epistemic tiers and the 0:1:4 hierarchy, and 'Paper C (The Inversion Arc)' for the constraint-attractor cycle and two-phase commit; the repo holds these under papers/core_trilogy/. *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 9 (Traceability), lines 1443-1482)*
- **Coherence obstruction tensor** — The explicit commutator [R_alpha, R_beta]\(A) = R_alpha(R_beta(A)) - R_beta(R_alpha(A)) between two discretization schemes, quantifying their exact conjugacy failure; its pushforward through the observation functor yields the scheme dispersion metric. *(papers/discrete_geometry_formalism.tex sec 3, lines 68-73)*
- **De-sublimation of geometry** — The principle that traditionally geometric quantities are reduced to computable statistics on the orbit sheaf: curvature becomes the commutator defect of local update operators after projection, RG flow becomes iterated composition drift in Phi-space, fixed points become attractors of the discrete dynamics, and holonomy becomes loop compositions in the action semigroup. *(papers/discrete_geometry_formalism.tex sec 2.1, lines 60-66)*
- **Observation functor Phi** — A deliberately lossy, nonlinear projection Phi: A -> R^m extracting structural statistics (such as mean plaquette holonomy curvature) from a state; the sole channel through which information about the non-commuting dynamics is measured. *(papers/discrete_geometry_formalism.tex sec 1.3, lines 45-50)*
- **Orbit sheaf / Spec_S(A)** — The primitive output of the Dynamical Epistemic Algebra: the ensemble of all possible measurement histories Phi(R_{alpha_k} o ... o R_{alpha_1}(A)) under the finite atlas of rewrite rules. All traditional physics-like quantities are recast as secondary statistical functionals on this ensemble. *(papers/discrete_geometry_formalism.tex sec 2, lines 52-58)*
- **Rewrite semigroup {R_alpha}** — A family of nonlinear update endomorphisms on the state space, indexed by discretization schemes (e.g. bilinear interpolation, Procrustes midpoint alignment), that are explicitly not required to compose coherently across schemes: they form a non-commutative semigroup action, not a strict category or groupoid. *(papers/discrete_geometry_formalism.tex sec 1.2, lines 38-43)*
- **Torsion hierarchy 0:1:4** — A coupling hierarchy carried over from the physics framework ('Paper A sec C.1') and mapped in the stack to operator priority tiers; also slated for GW waveform templates in the Phase 4 physics-frontier roadmap. The PDR uses it as a named design input without restating its derivation. *(papers/ACS_Deterministic_AI_Stack_PDR.tex sec 1 table line 273 and sec 9 traceability lines 1477-1478)*


## Alphabetical index

| Term | Section |
|---|---|
| (2,1)-torus embedding (screw centerline) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| (3,1) internal grading selection | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| 0:1:4 hierarchy — see Torsion coupling hierarchy | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| 1st/2nd/3rd order coupling — see Nested coupling orders | [Framework core](#framework-core) |
| 30-domain predictive test | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| 3rd-order holonomy — see Emergent pattern | [Framework core](#framework-core) |
| 4-tier honesty ledger — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| 4/3 coincidence | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| 4/3 mechanism — see 4/3 coincidence | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| 49 keV sterile neutrino — see Geometric see-saw | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| 5+3 split — see Closure attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| 6+3 split — see Closure attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| 6+9 decomposition — see Palatini decomposition (torsion sector / Lorentz sector) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| 76-script ACS verification suite | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| [e, ω] — see Palatini bracket | [Framework core](#framework-core) |
| abelian/non-abelian diagnostic — see Three-number diagnostic | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| ACS (Asymmetric Codependent Systems) — see Asymmetric Codependent System (ACS) | [Framework core](#framework-core) |
| ACS balance condition — see Information balance | [Framework core](#framework-core) |
| ACS coupling orders — see Nested coupling orders | [Framework core](#framework-core) |
| ACS Deterministic AI Stack | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| ACS Framework — see Asymmetric Codependent System (ACS) | [Framework core](#framework-core) |
| ACS framework — see Asymmetric Codependent System (ACS) | [Framework core](#framework-core) |
| ACS measure | [Framework core](#framework-core) |
| ACS rereading of ER=EPR — see Algebraic non-traversability | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| ACS trilogy (Paper A / Paper C) | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| ACS vacuum equilibrium T^a = 0 — see Torsion as 1st-order ACS coupling (C2) | [Framework core](#framework-core) |
| ACS — see Asymmetric Codependent System (ACS) | [Framework core](#framework-core) |
| ACS-1 Codependence | [Framework core](#framework-core) |
| ACS-2 Structural Asymmetry | [Framework core](#framework-core) |
| ACS-3 Mutual Constraint | [Framework core](#framework-core) |
| Action-proximity mechanism (falsified) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Active sector | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| add_exit / GEOMETRY_EXIT | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| addition has no shape — see Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Additive depth | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Additive seam — see Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Advantage map | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Adversarial compression | [Framework core](#framework-core) |
| adversarial compression methodology — see Adversarial compression | [Framework core](#framework-core) |
| Adversarial gauntlet | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Adversarial hardening | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| AISO / TENT / OmniForge stack | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| AISO motif-memory integration | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Algebraic Conductance State (ACS) framework — see Asymmetric Codependent System (ACS) | [Framework core](#framework-core) |
| Algebraic non-traversability | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Algebraic non-traversability (ER = EPR) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| alpha preformation amplitude — see P_alpha (alpha preformation factor) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| alpha^-1 = pi eps0 R / C — see Capacitance model of alpha (self-stress matching) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| amplification with N | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Amplitude-matched random-frequency control | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Analysis engine | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Annulus / thin-ring baseline capacitance C_ann | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| apparatus band | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| arith — see arithmetic prime-resonance witness | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| arithmetic prime-resonance witness | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Asymmetric Codependent System (ACS) | [Framework core](#framework-core) |
| Asymmetric Codependent Systems — see Asymmetric Codependent System (ACS) | [Framework core](#framework-core) |
| Asymmetric instrument | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| asymmetric transfer entropy — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Asymmetry map Phi | [Framework core](#framework-core) |
| Asymmetry map Phi(v) = [e(v), omega(v)] | [Framework core](#framework-core) |
| Banach-Tarski as geometric ACS | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Barbero-Immirzi from information balance | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Barbero-Immirzi parameter γ | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| BCH orders — see Nested coupling orders | [Framework core](#framework-core) |
| BCH-3 truncation — see Jacobi truncation | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| BCH-TE morphism | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| BCH-transfer-entropy lemma | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| BCH-transfer-entropy morphism — see BCH-TE morphism | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| BCH–Transfer-Entropy morphism — see BCH-TE morphism | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| BI balance condition — see Barbero-Immirzi from information balance | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| BIE Mobius collocation C_BIE | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Boundary law | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| bounded-depth guarantee — see Jacobi truncation | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| box — see Shape | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| BRA kernel verdicts | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Bracket Engine | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| Branch A / Branch B | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| C2-closed — see Torsion as 1st-order ACS coupling (C2) | [Framework core](#framework-core) |
| Cabibbo chain | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Candidate-elimination filter / admissibility class | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| canonical seed 20260423 | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Cantor corner | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Cantor pairing counterexample | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Capacitance estimate of alpha | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Capacitance model of alpha (self-stress matching) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Central number | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| chain support decision rule | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Channel A (parametric spectroscopic factor) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Channel B (self-consistent WS+Coulomb eigenmode) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Channel C (Gamow outgoing boundary) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Character-product block-diagonalization (falsified conjecture) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Charge/coupling epistemic split | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Chirality map J | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| chirality uniqueness — see Chirality map J | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Closure attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| closure attractor uniqueness — see Closure attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Closure defect functional D(V) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| closure defect — see Closure defect functional D(V) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Closure Validator | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Cluster coherence | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Codependence invariant | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Coherence obstruction tensor | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| Coleman-Mandula rule (scope standard) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Coleman–Mandula bridging mechanisms | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| collapse — see Engine kill-criterion (tomographic invariance) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Colour charge gap | [Framework core](#framework-core) |
| Colour charges as torsion Cartan eigenvalues | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| colour skeleton — see Closure attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| colour-confining throat — see Throat | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| combination tones — see Tartini tones | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Commutator order parameter and parity law | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Composition Core — see Bracket Engine | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| Compression Law (pre-asymptotic) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Conditional-uniformity height floor | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Conditional-uniformity height floor T_min = (2 pi e)^d / q | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Confinement as ACS attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Conformal strip-to-annulus model C_conf | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Conjecture P2: Wheeler-DeWitt as ACS fixed point | [Framework core](#framework-core) |
| Conjecture T4' — see T4-prime (stationarity <=> RH) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Conjecture T4-prime — see T4-prime (stationarity <=> RH) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Conjecture: geometric fermions from torsion | [Framework core](#framework-core) |
| Conjecture: Standard Model from GL(4) fiber | [Framework core](#framework-core) |
| Conservation principle | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Constraint-attractor cycle | [Framework core](#framework-core) |
| constraint-attractor loop — see Constraint-attractor cycle | [Framework core](#framework-core) |
| converse of T4 — see T4-prime (stationarity <=> RH) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| counting unit — see resolution unit (delta) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| coupling orders — see Nested coupling orders | [Framework core](#framework-core) |
| Cross-correlation bound C_N | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| D(V) — see Closure defect functional D(V) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| D1-D11 — see 76-script ACS verification suite | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| DAG journal | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| De-sublimation of geometry | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| decay as spectral bifurcation — see Spectral bifurcation | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Degenerate-case trap | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Delta I = 0 — see Information balance | [Framework core](#framework-core) |
| Delta I Monitor | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Delta I — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| delta I — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Delta-I = c identity | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Density engine | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Density vs identity | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| density-not-identity crossing — see Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| density/positions/spacings decomposition — see Three-layer decomposition | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Density/Spacings/Positions — see Positional duality | [Framework core](#framework-core) |
| Deterministic AI Stack | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Deterministic AI Stack — see ACS Deterministic AI Stack | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| DI — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Difference-tone plateau mechanism (falsified) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| difference-tone spectrum — see Tartini tones | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Dimensional devolution | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| dimensionless invariant width/delta | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| discrete operator geometry stack — see Dynamical Epistemic Algebra | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| Dominance engine | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Dynamical Epistemic Algebra | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| E_cap = m_e c^2 — see Capacitance model of alpha (self-stress matching) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Effective dynamical rank r_eff | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Elastodynamic tensor mapping | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Electroweak Containment | [Framework core](#framework-core) |
| Elimination Ledger | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| elliptic/hyperbolic/parabolic adjoint flows — see Three-class spectral taxonomy | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Emergent pattern | [Framework core](#framework-core) |
| Empirical perturbation P_m | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Empirical second-order transition operator T_m | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| empty-tunnel mapping — see Strip-mine discipline | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Engine kill-criterion (tomographic invariance) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Epistemic compression | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Epistemic tiers T1/T2/T3/T4 — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| epistemic tiers — see Grade hierarchy (Theorem / Verification / Exploratory) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| exact float-free kill test | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Exact integer automaton | [Framework core](#framework-core) |
| explicitly falsified — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| ExploratoryGrade — see Grade hierarchy (Theorem / Verification / Exploratory) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Extended isotope catalog (n=29) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| F — see Form field | [Framework core](#framework-core) |
| F_N stationarity theorem — see T4 (RH implies F_N stationarity) | [Framework core](#framework-core) |
| F_N(x) — see Riemann spectral function F_N(x) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| False wall | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| False-fit mode | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| falsified claims ledger — see Elimination Ledger | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| FF06 series | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| FF06 series designations (FF06e-FF06h) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| FF06 series paper labels | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| FF06e — see shuffle knife | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| FF06f decomposition — see Positional duality | [Framework core](#framework-core) |
| FF06g — see Form/Function Relativity | [Framework core](#framework-core) |
| FF06g — see Geometry Engine | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| FF06h — see scaled invariance of the counting label | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| FF06i (parent paper) — see Reversible flattening (the thesis) | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| First-class negative | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Flag Condensate | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| flag condensate field — see Flag Condensate | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| flag field — see Flag Condensate | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| flag-condensate field — see Flag Condensate | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Flattening | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| form (witness label) — see Form vs. Function witnesses | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Form field | [Framework core](#framework-core) |
| form vs function — see Form/function split | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Form vs. Function witnesses | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Form — see Form field | [Framework core](#framework-core) |
| FORM — see Form vs. Function witnesses | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| form-bundle | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| form/function asymmetry — see Form/function split | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| form/function coupling — see Form/function split | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Form/Function cut — see Form/function split | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Form/Function ontology — see Form/function split | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Form/Function Relativity | [Framework core](#framework-core) |
| Form/function split | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Four-domain phase-defect unification | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Four-domain phase-defect unification table | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Four-tier verification hierarchy (T1/T2/T3/T4) — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Four-tier verification hierarchy — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| four-tier verification hierarchy — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| four-tier verification ledger — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Fourier-dual asymmetric codependent partners | [Framework core](#framework-core) |
| frame ladder | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| frame ladder — see Form/Function Relativity | [Framework core](#framework-core) |
| frame — see reference frame (nu) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Frame-Hopf map (one quaternion curve) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| frame-relativity of form/function — see Form/Function Relativity | [Framework core](#framework-core) |
| framed (2,1) unknot — see Mobius-screw electron | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Framed unknot | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| framed unknot model — see Mobius-screw electron | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| framed-unknot electron model — see Mobius-screw electron | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Framework-constant refraction verdicts | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Framing Transformer | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| framing_transformer.py — see Framing Transformer | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Fresh-eyes note | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| function (witness label) — see Form vs. Function witnesses | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Function field | [Framework core](#framework-core) |
| FUNCTION — see Form vs. Function witnesses | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Function — see Function field | [Framework core](#framework-core) |
| Functional-equation involution iota and character twist T | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| g <-> Sl identification — see Sl=2 <-> g=2 identification | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| gamma = 0.274 — see Barbero-Immirzi from information balance | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| gamma_ACS = 0.274 — see Barbero-Immirzi from information balance | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Gamow phase defect W | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| gap two-point surrogate (C) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| gap-cone dependency chain — see Section 9 chain | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| gap-shuffle surrogate — see marginal-matched surrogate | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| gap-shuffle — see shuffle knife | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Gauntlet grades (HIT / SPLIT / DOWNGRADED / FALSE FIT) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Geiger-Nuttall linearity result | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Geometric chirality from torsion | [Framework core](#framework-core) |
| geometric origin of g=2 — see Sl=2 <-> g=2 identification | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| geometric phase slip — see Phase slip / phase-slip channel | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Geometric see-saw | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Geometry Engine | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Governance Policy Engine | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Grade hierarchy (Theorem / Verification / Exploratory) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Graded spectral functional S~_g[P] | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Grading selection from adjoint activity — see Grading selection theorem | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Grading selection theorem | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Grading selection theorem (N2) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Gravitational ACS | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Gravitational ACS (Ashtekar pair) | [Framework core](#framework-core) |
| GUE-full (bulk) frame | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| GUE-marginal frame | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| GUE-marginal shuffle — see marginal-matched surrogate | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| GUE-necessary-but-not-sufficient result | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| g₄ = g_L = g_R = 4/3 | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Harmonic ladder / repetition tower | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| height-floor scaling law — see Conditional-uniformity height floor T_min = (2 pi e)^d / q | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Higgs quartic lambda = 2*sqrt(3)/27 — see Koide projection | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| High-scale-boundary reading (falsified) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| high-torsion throat — see Throat | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Hilbert-Polya constraint specification (C1-C9) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Hilbert-Polya positive specification | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Hilbert-Pólya wall | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Hilbert–Polya wall (quantified obstruction) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Holographic resolution | [Framework core](#framework-core) |
| holographic resolution principle — see Holographic resolution | [Framework core](#framework-core) |
| holographic resolution principle — see Inversion arc | [Framework core](#framework-core) |
| holonomy term — see Emergent pattern | [Framework core](#framework-core) |
| HP knife suite | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| HR-1/HR-2/HR-3 — see Holographic resolution | [Framework core](#framework-core) |
| Hypercone (Klein-foam sense) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Hypercone projection (hypercone-through-the-slice) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Hypercone projection test (degeneracy cones) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| h̃/h = 2/3 (Yukawa ratio) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Identity chain — see One mechanism, many forms | [Framework core](#framework-core) |
| identity family n = d + 1 | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| identity/density split — see Density vs identity | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| infinite density engine (metaphor) — see Density engine | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Information asymmetry (Delta-I) — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| information asymmetry — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Information balance | [Framework core](#framework-core) |
| information-asymmetry / central-charge identity — see Delta-I = c identity | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Instanton action deformation delta-S(R) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| instrument swap — see Engine kill-criterion (tomographic invariance) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Intra-species resonance vs. cross-species complementary cancellation | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| INV-1 — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| INV-2 — see BCH-TE morphism | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| INV-3 — see Form/function split | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| INV-5 — see Inversion arc | [Framework core](#framework-core) |
| INV-7 — see Adversarial compression | [Framework core](#framework-core) |
| INVARIANT (candidate) — see Refraction | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Invariant (candidate) — see Refraction | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Inversion arc | [Framework core](#framework-core) |
| inversion theorem — see Inversion arc | [Framework core](#framework-core) |
| J(T) = i sym(T) + anti(T) — see Chirality map J | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| J-map — see Chirality map J | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Jacobi truncation | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| joint-scaling invariance — see scaled invariance of the counting label | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| K1 / K2 robustness checks | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Kernel invariant | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Kernel Law | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| KFM — see Klein foam | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| kill condition — see Engine kill-criterion (tomographic invariance) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| kill condition — see Pre-registration and the no-tuning rule | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| kill criteria — see Engine kill-criterion (tomographic invariance) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| kill ledger — see Elimination Ledger | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| kill pass — see Engine kill-criterion (tomographic invariance) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| kill target — see Engine kill-criterion (tomographic invariance) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| kill test — see Engine kill-criterion (tomographic invariance) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| kill-criterion — see Engine kill-criterion (tomographic invariance) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| kill-queue — see Elimination Ledger | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Killing-orthogonality | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Killing-orthogonality theorem | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Klein foam | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Klein-Foam Monad — see Klein foam | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Klein-foam Monad — see Klein foam | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Koide projection | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Koide ratio h-tilde/h = 2/3 | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Koide ratio — see Koide projection | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Koide-Cabibbo relation | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| lag-1 spacing correlation witness | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Lane density rho_lane | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Laplace-eigenspace relocation of spin-1/2 | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Layered resolution structure | [Framework core](#framework-core) |
| Ledger status tags | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Leibniz failure -fgh' — see Wronskian-Lie identification | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Lemma 2.9 (as hardcoded in Appendix B) — see BCH-TE morphism | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Link 3 — see Delta-I = c identity | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Links 1-3 — see One mechanism, many forms | [Framework core](#framework-core) |
| Lisp-deterministic | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| loop closure — see Two faces of zeta | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Lorentz sector — see Palatini decomposition (torsion sector / Lorentz sector) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| machine-verified — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| MANIFEST tier map — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Many-worlds self-similarity | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| marginal-matched null — see shuffle knife | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| marginal-matched surrogate | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Matrix candidate | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| measurability wall | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Measured, never projected | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Minimal Pati–Salam embedding / T_{B-L} generator | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Minority-cluster rule | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Mixed obstruction (Pati-Salam decomposition) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Mobius screw — see Mobius-screw electron | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Mobius-screw electron | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Mobius-screw electron (framed unknot) — see Mobius-screw electron | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Mobius-screw soliton — see Mobius-screw electron | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Mod-6 hexagonal clock | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| model electron — see Framed unknot | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| monotone staircase | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| multiplicative-additive seam law — see Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Möbius-screw electron — see Mobius-screw electron | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| N_gen = 3 (Jacobi truncation) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Necessary spectral signatures | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Negative ledger — see Elimination Ledger | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| negative results as first-class outputs — see Elimination Ledger | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Nested coupling orders | [Framework core](#framework-core) |
| Nested determinants | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| net transfer entropy — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| No detectable lattice imprint in the broken phase (negative result) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| No selection regime | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| No-go for geometric g (g=1 result) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Non-transitive impossibility (Condorcet instance) | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| nuclear throat — see Throat | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| numerically verified — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Observation functor Phi | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| Off-line injection test | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| One field, two readouts | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| One mechanism, many forms | [Framework core](#framework-core) |
| one object, three descriptions — see One property, three dresses | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| One property, three dresses | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| ontological reading — see One mechanism, many forms | [Framework core](#framework-core) |
| OOS01 | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Orbit observable A(tau) | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Orbit sheaf / Spec_S(A) | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| Order-dependence / structure-retention axes | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Origin falsifications (phi + inverse-silver; FHT consciousness score) | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| outside-cone leakage | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| overlap proxy — see P_model (standing-wave overlap proxy) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| p-adic gradient (Wall 6) | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| P_alpha (alpha preformation factor) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| P_alpha^ext — see P_alpha (alpha preformation factor) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| P_model (standing-wave overlap proxy) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| P_model = \|&lt;u_in\|u_alpha&gt;\|^2 — see P_model (standing-wave overlap proxy) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| pair-correlation sufficiency | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Palatini bracket | [Framework core](#framework-core) |
| Palatini decomposition (Lorentz sector + torsion sector) — see Palatini decomposition (torsion sector / Lorentz sector) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Palatini decomposition (torsion sector / Lorentz sector) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Palatini → Pati-Salam pipeline | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Paper A pipeline — see Palatini → Pati-Salam pipeline | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Paper B / Paper C (bundle companions) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Paper C: The Inversion Arc — see Inversion arc | [Framework core](#framework-core) |
| Paper D — see ACS Deterministic AI Stack | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| Parameter ledger | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Parity law | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| parity law — see Framing Transformer | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| PASS_WITH_CAUTION | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Pati-Salam derivation — see Palatini → Pati-Salam pipeline | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Peaked spectrum = diagonal prime powers | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Phase 50 — see Self-pruning of the bi-doublet Higgs sector | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Phase 51 — see Self-pruning of the bi-doublet Higgs sector | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Phase 52 — see Self-pruning of the bi-doublet Higgs sector | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Phase slip | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Phase slip / phase-slip channel | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| phase-slip transfer-matrix picture — see Phase slip / phase-slip channel | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Phenomenological closure ansatz (variance-floor bridge) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Phi substrate — see Flag Condensate | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Phi — see Flag Condensate | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Phi — see Function field | [Framework core](#framework-core) |
| polymorphic flags — see Polymorphic quantum flags | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| polymorphic mode lanes — see Polymorphic quantum flags | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Polymorphic quantum flags | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| position form factor K(f) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| position pair correlation — see value-space pair correlation of the positions (rho_2) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Positional duality | [Framework core](#framework-core) |
| pre-registered test — see Pre-registration and the no-tuning rule | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Pre-registration and the no-tuning rule | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Predictions on record | [Framework core](#framework-core) |
| preformation factor — see P_alpha (alpha preformation factor) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| prime box — see Shape | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| prime carrier | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Prime face / zero face | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| prime resonance — see arithmetic prime-resonance witness | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| prime signal — see prime-resonance power P | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Prime-gap transition operator P_m (N3) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| prime-gap transition perturbation — see Empirical perturbation P_m | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| prime-resonance functional — see prime-resonance power P | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| prime-resonance power P | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| prime-resonance power — see arithmetic prime-resonance witness | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| prime-signature representation — see Shape | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Prime-zero ACS | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| proved in paper — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| PS embedding — see Minimal Pati–Salam embedding / T_{B-L} generator | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Pythagorean lattice <2,3> | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Q = 2/3 projection — see Koide projection | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Radius / falsification surface | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| RC1 claim discipline | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| RC1 scope | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| RC1 scope — see RC1 claim discipline | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| RC1 — see RC1 claim discipline | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| reactional vs response-driven definition | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Receipt | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Red/Blue/Green/White geometric colour — see Colour charges as torsion Cartan eigenvalues | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Reductive sweep (decoy ranking) | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| reference engine — see Geometry Engine | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| reference ensemble — see reference frame (nu) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| reference frame (nu) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| reference measure — see reference frame (nu) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| refinement chain — see frame ladder | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Refraction | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Refraction vs invariant — see Refraction | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| relational over scalar — see Relational Representation Principle | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Relational Representation Principle | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Renormalised stability (Delta_norm) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| repository tier discipline — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Reproducibility envelope | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| repulsion witness | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| resolution count N_delta[a,b] | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| resolution unit (delta) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Resolvent susceptibility chi(omega) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Result hierarchy | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| result tiers — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| retraction: 'the primes are not a two-point statistic' | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Reversible flattening (the thesis) | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| reversible flattening — see Flattening | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Rewrite semigroup {R_alpha} | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| rho_2 — see value-space pair correlation of the positions (rho_2) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Ricci flow as ACS dynamics | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Riemann spectral function F_N(x) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Right locally, wrong globally (glass-box) | [Framework core](#framework-core) |
| rigidity witness (number variance) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| role-relativity in nested systems | [Framework core](#framework-core) |
| S(T) counting fluctuation | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Same-gap conjecture (falsified) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Scale ladder (micro / meso / macro) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| scale recursion — see Many-worlds self-similarity | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| scaled invariance of the counting label | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Scope boundary | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| scope honesty standards — see Scope boundary | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| seam density law — see Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Seam law — see Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Seam — see Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Section 9 chain | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Section 9 toy chain — see Section 9 chain | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| see-saw product formula — see Geometric see-saw | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Seed convention 20260423 | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| selection principle — see Closure attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| selection theorem — see Grading selection theorem | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Self-linking identification Sl = 2 -> g = 2 | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Self-linking number Sl (Calugareanu identity) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Self-pruning of the bi-doublet Higgs sector | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Self-resolving structure | [Framework core](#framework-core) |
| self-similar phase-defect ladder — see Many-worlds self-similarity | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| self-stress match — see Capacitance model of alpha (self-stress matching) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Shape | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| shape engine — see Geometry Engine | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| shuffle knife | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Shuffle knife (marginal-matched surrogate) — see shuffle knife | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| shuffle-invariant vs shuffle-fragile witnesses — see Form vs. Function witnesses | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| shuffle-knife discriminant — see shuffle knife | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| shuffle-knife separation — see shuffle knife | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| shuffled spacing discriminant — see shuffle knife | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Shuman Resonance | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| signature selection — see (3,1) internal grading selection | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| single-realisation form factor — see position form factor K(f) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| SIP License v1.1 | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Sl = 2 ↔ g = 2 — see Mobius-screw electron | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| sl(3,R) closure — see Closure attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| sl(3,R) embedding (colour skeleton) — see Closure attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| sl(3,R) → su(3) map — see Chirality map J | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Sl=2 <-> g=2 identification | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Slag | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Source sector | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Sovereign framing | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Sovereign Integrity Protocol License (SIP License v1.1) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Sovereign Integrity Protocol License (SIP License) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Sovereign-Stack ACS Research Program — see Asymmetric Codependent System (ACS) | [Framework core](#framework-core) |
| spacing floor / shuffle floor | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Spectral bifurcation | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Spectral function F_N(x) — see Riemann spectral function F_N(x) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| spectral function — see Riemann spectral function F_N(x) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Spectral stability ratio (rho_spec) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| spectral witness | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Spectroscopic factor S | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Spin radius | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Spinorial holonomy sigma | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| staircase — see monotone staircase | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| standing-wave overlap proxy — see P_model (standing-wave overlap proxy) | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Standing-wave phase lock | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Stationarity measure S(N,X) / uniform stationarity | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| stress-tensor mapping T11/T12 — see Elastodynamic tensor mapping | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| StrickenBy | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Strip-mine discipline | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| strip-mine — see Strip-mine discipline | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Strip-mining stance | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Stripped-mode SHO property | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Strong CP theta_QCD = 0 | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Structural source invariance | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| SU(3) attractor — see Closure attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| SU(3) closure attractor — see Closure attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| SU(3)-not-in-O(4) theorem | [Framework core](#framework-core) |
| Sycophantic mode | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Symmetric involution and induced grading | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| T1 (ACS generates non-zero information asymmetry) | [Framework core](#framework-core) |
| T1 (machine-verified) — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T1 measured — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T1 upgrade path | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T1 — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T1-closed — see T1 (ACS generates non-zero information asymmetry) | [Framework core](#framework-core) |
| T1-T21 — see 76-script ACS verification suite | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T1-T4 hierarchy — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T2 (proved in paper) — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T2 forced — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T3 (numerically verified) — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T3 conjecture — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T3 — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T4 (explicitly falsified) — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T4 (RH implies F_N stationarity) | [Framework core](#framework-core) |
| T4 falsified — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T4 — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T4' — see T4-prime (stationarity <=> RH) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| T4-prime (stationarity <=> RH) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| T_min height floor (2πe)^d/q | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| T_min — see Conditional-uniformity height floor T_min = (2 pi e)^d / q | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| T_{B-L} — see Minimal Pati–Salam embedding / T_{B-L} generator | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| tan β gauge-protected flat direction | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| tan(theta0) = lambda_Wolfenstein — see Koide-Cabibbo relation | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Tartini tones | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Tensegrity / nested codependence | [Framework core](#framework-core) |
| Tensegrity atom | [Framework core](#framework-core) |
| Tensegrity-gauge correspondence | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| The 2x2 square | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| the 4/3 equality — see 4/3 coincidence | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| the additive wall — see Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| the asymmetry — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| the carrier — see prime carrier | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| The critical line is not one seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| The Geometry Engine / The Reversible Flattening (bundle companions) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| the homomorphism criterion — see Reversible flattening (the thesis) | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| the key has become the lock — see Inversion arc | [Framework core](#framework-core) |
| the knife — see shuffle knife | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| the Monad — see Klein foam | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| the nest — see frame ladder | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| the scalar was a shadow | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| the seam is convolution (keystone) — see Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| the seam — see Convolution seam | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| the singular reading — see One mechanism, many forms | [Framework core](#framework-core) |
| Theorem 2.9 — see T1 (ACS generates non-zero information asymmetry) | [Framework core](#framework-core) |
| Theorem 4.1 — see T4 (RH implies F_N stationarity) | [Framework core](#framework-core) |
| Theorem T4' — see T4-prime (stationarity <=> RH) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| TheoremGrade — see Grade hierarchy (Theorem / Verification / Exploratory) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Three contractions | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Three generations from Jacobi truncation | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| three independent filters — see Self-pruning of the bi-doublet Higgs sector | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Three-class spectral taxonomy | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Three-layer decomposition | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| three-layer decomposition — see Positional duality | [Framework core](#framework-core) |
| Three-number diagnostic | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Three-tier verification model | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| three-way identification — see One property, three dresses | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| threshold frame | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Throat | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Throat / throat sieve | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Throat weight w(r) = R/r | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Tier 0 — see Torsion coupling hierarchy | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Tier 1 — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Tier 2 — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Tier 2 — see Torsion coupling hierarchy | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Tier 3 — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Tier 4 — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Tier discipline (T1-T4) — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| tier discipline — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Tier labels (T1/T3 as used in the seam note) — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| tier system — see tier map (T1-T4) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Tomographic invariance engine | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| tomographic invariance — see Engine kill-criterion (tomographic invariance) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| tomographic kill-criterion — see Tomographic invariance engine | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Torsion as 1st-order ACS coupling (C2) | [Framework core](#framework-core) |
| Torsion coupling hierarchy | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Torsion hierarchy 0:1:4 | [The Deterministic AI Stack (Paper D)](#the-deterministic-ai-stack-paper-d) |
| torsion sector — see Palatini decomposition (torsion sector / Lorentz sector) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Torus framing | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| TR-2026-FF06-KFM — see Klein foam | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Transfer entropy (TE) | [Framework core](#framework-core) |
| transfer-entropy asymmetry — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Transfer-matrix Bogoliubov extraction | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| transformer chain — see Framing Transformer | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Transition state space S_m and transition class | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Transport obstruction | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| true influence z(W) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Two faces of zeta | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| two faces of zeta — see Prime face / zero face | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Two-stage selection mechanism | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Unbiased reference T_0 | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Uniform spectral contraction (falsified conjecture) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Unique center manifold (critical line) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Unique vs cardinal structure | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| unit — see resolution unit (delta) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Universal renormalized spectral law (falsified conjecture) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Universal-2pi overclaim (retracted) | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Vacuity guard | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Vacuum energy cancellation (Palatini pairing) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| value-space pair correlation of the positions (rho_2) | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Vantage-point census | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| verification suite — see 76-script ACS verification suite | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| VerificationGrade — see Grade hierarchy (Theorem / Verification / Exploratory) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| Verified-optimal d(n) structure search | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Wall resolution class | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Weight factorisation through eigenvalue clusters | [Holography and algebraic structure (Paper C, with companions)](#holography-and-algebraic-structure-paper-c-with-companions) |
| Wheeler-DeWitt as ACS quantum attractor | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Wigner-shape witness | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Witness (spectral witness) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| witness — see spectral witness | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Woods-Saxon alpha-cluster trial | [Physical models: the Flag Condensate and electron notes](#physical-models-the-flag-condensate-and-electron-notes) |
| Wronskian as Lie bracket — see Wronskian-Lie identification | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| Wronskian bracket analysis | [Framework core](#framework-core) |
| Wronskian-Lie identification | [The spectral-Riemann program (Papers B and B-prime, with companions)](#the-spectral-riemann-program-papers-b-and-b-prime-with-companions) |
| xp as smooth skeleton | [Number representation and the FF06 thread](#number-representation-and-the-ff06-thread) |
| Y^14 (bundle of metrics) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| Yang-Mills Abelian limit theorem (T3) | [Framework core](#framework-core) |
| ΔI (net transfer entropy) — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| ΔI — see Delta-I (information-asymmetry functional) | [The gauge-gravity program (Paper A)](#the-gauge-gravity-program-paper-a) |
| ΔI ≡ c-function (FF06Σ Link 3) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
| λ_φ = 2√3/27 (Higgs quartic) | [Verification and governance vocabulary](#verification-and-governance-vocabulary) |
