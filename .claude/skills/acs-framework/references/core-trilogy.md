# Core Trilogy — Papers A, B, B′, C + Monograph

Sources: `papers/core_trilogy/{Palatini_Gauge_Attractor, Riemann_Spectral_Critical_Line,
Spectral_Witness_Refinement, Holographic_Spectral_Inversion}.tex`,
`papers/Form_Function_and_Asymmetry.tex`. Author: Bradley Wallace, dated March 2026, SIP v1.1.

**Numbering caution:** A/B/C use `\newtheorem{theorem}{Theorem}[section]` with **one shared
counter** across theorem/lemma/prop/def/remark/corollary/conjecture. Cite by `\label` name, not
by number. B′ uses per-type counters and is cited by section (§3–§13).

---

## 1. The five documents

### Paper A — *Colour from Gravity: SU(3) as a Closure Attractor in the Palatini Bracket*
Subtitle: *The Strong Force Algebra from Vierbein–Connection Geometry and Unitarity*. 3166 lines.

**Claim:** 𝔰𝔲(3) colour is a geometric selection effect inside Palatini gravity, requiring
exactly one non-gravitational input (unitarity/compactness).

**Spine:**
1. Define the ACS: two codependent, structurally asymmetric fields (ACS-1/2/3) with net transfer entropy ΔI.
2. Equip deterministic ACS flows with an SRB/Liouville invariant measure μ so ΔI is well-defined.
3. Prove the **BCH–TE morphism** — the Lie bracket **is** the 2nd-order TE coefficient, via the exact Cartan formula [𝓛_f,𝓛_g] = 𝓛_{[f,g]}. Not an analogy.
4. Therefore ΔI ≠ 0 generically for f ≢ g, confirmed by an exact integer automaton with sign reversal ±1.499.
5. Identify (e^a_μ, ω^{ab}_μ) as an ACS: torsion T^a = 1st-order coupling; curvature R^{ab} = 2nd-order bracket; Bianchi = 3rd-order holonomy. T^a = 0 is the *dynamically reached* vacuum attractor, not an imposed constraint.
6. Compute Im(Φ) where Φ(v) = [e(v), ω(v)]: exactly 𝔰𝔩(4,ℝ), rank 15, splitting 6 (Lorentz) + 9 (torsion).
7. Selection: among 8-dim subspaces of 𝔰𝔩(4,ℝ), only 𝔰𝔩(3,ℝ) has closure defect 𝒟 = 0; it sits 5+3 across torsion/Lorentz — irreducibly distributed across both ACS coupling orders.
8. Complexify: the chirality map J(T) = i·sym(T) + anti(T) is the unique grading-preserving map taking 𝔰𝔩(3,ℝ) → 𝔰𝔲(3). **This step imports unitarity as a physical input.**
9. Read off physics: colour charges = Cartan eigenvalues in the torsion sector; gluons split 5 torsion + 3 Lorentz; confinement = ΔI → 0 attractor.
10. Extend to LQG: (Ẽ, A) is an ACS; the three constraints are the three BCH orders; ACS balance ΔI = 0 at the horizon gives Z(γ) = 1 ⇒ γ = 0.274; WdW is the quantum attractor.
11. Phenomenology: Koide/Cabibbo, Higgs quartic, see-saw, torsion tiers, vacuum-energy cancellation, parameter ledger (6 inputs vs SM's 19+).

### Paper B — *The Riemann Spectral ACS: Stationarity as a Characterisation of the Critical Line*
Subtitle: *Information Asymmetry, Transfer Entropy, and an ACS Approach to the Riemann Hypothesis*.
Cited elsewhere in the repo as *Spectral Susceptibility and Renormalized Stability on the Riemann
Critical Line*. 1959 lines.

**Claim:** primes (Form) and zeros (Function) form an ACS; RH ⇔ stationarity of the spectral
superposition. **⇒ proved; ⇐ conditional** on an unproved minimum-gap bound.

**Spine:** primes as a point process with intensity ~1/log x, zeros with GUE pair-correlation ⇒
ΔI well-defined → define F_N(x) = Σ A_k φ_k(x), A_k = 1/(¼+γ_k²), the explicit formula as ACS
coupling → **RH ⇒ stationarity** by AM–GM (x^σ + x^{1−σ} ≥ 2x^{1/2}, equality iff σ = ½) → the
Wronskian is a genuine Lie bracket but **fails Leibniz** by exactly −fgh′, killing the earlier
plasma-Hamiltonian reading → spectral stability ratio ρ_spec → **converse T4′** via variance
decomposition + sinc bound + Gallagher large sieve → elastodynamic tensor, variance scaling, pure
rotation only at σ=½ ⇒ the critical line is the unique **center manifold** → scale-up to
N = 2,001,052 zeros → Tartini characterisation (R₂ Montgomery, R₃ Rudnick–Sarnak, Fourier dual)
→ L-function generalisation → Hilbert–Pólya constraint spec C1–C9.

### Paper B′ — *Spectral Witness Survival and the Character of the Transport Obstruction*
Subtitle: *A reproducible computational study on the Riemann zeros, with companion results on the
𝔰𝔩(4,ℝ) Palatini transport*. 517 lines. Canonical seed **20260423**; first 10⁵ zeros to 3×10⁻⁹.

**Claim:** separate genuine spectral structure from artifact, and determine the algebraic
character (abelian vs non-abelian) of the transport obstruction. Negatives reported first-class.

**Spine:** unfold by N̄(t) → confirm GUE → SFF ramp/plateau/knee → prime orbits build the ramp,
overshoot past τ_H ⇒ plateau is off-diagonal → Fourier dual = prime-power line spectrum, hardened
by threshold sweep → **falsify two off-diagonal mechanisms** (action-proximity, difference tones)
— the null *is* the content: prime-log incommensurability = unique factorisation, spectrally
expressed → probe-basis-invariant 3-number abelian/non-abelian diagnostic → 𝔰𝔩(4,ℝ) obstruction
forced non-abelian by simplicity → Pati–Salam decomposition ⇒ **mixed**; central number forced to
the quark B−L charge 1/3 via K = 32/3 → height floor T_min = (2πe)^d/q → falsify "same gap" and
the high-scale reading of the Higgs quartic residual ⇒ **charge/coupling epistemic split** →
form/function witness categorisation by surrogate shuffling.

### Paper C — *The Inversion Arc: Holographic Resolution in Asymmetric Coupled Systems*
Subtitle: *Constraint–Attractor Dynamics, Tensegrity, and the Banach–Tarski Connection*. 1068 lines.

**Claim:** the universal structural consequence of the ACS is that a system solving a constraint
becomes the next constraint, with ΔI flipping sign.

**Spine:** tensegrity as discrete ACS (cables = Form, struts = Function; zero modes = gauge
freedoms) → define **holographic resolution** HR-1/2/3 and **self-resolving structure** →
**Inversion theorem**: role exchange f↔g flips the sign of ΔI at 1st and 2nd order (both terms
odd under exchange) → constraint–attractor cycle → algebraic foundations (Killing orthogonality,
three ambiguity numbers, three-class spectral taxonomy, algebraic non-traversability as an ACS
rereading of ER=EPR) → universality table across 5–6 domains → Banach–Tarski as the pure
geometric ACS. **No figures.**

### Monograph — *Form, Function, and the Asymmetry That Generates Both*
2497 lines. The **earlier consolidated version** the trilogy was split out of: contains A+B+C
material with weaker numbers in several places. Unique content: the Einstein–Cartan **torsion
lattice chirality** table, the acoustic-analogy section, and the quantum-ΔI (Lindblad) proposal.

---

## 2. Definitions

- **`def:acs` — Asymmetric Codependent System.** (ACS-1) Codependence: ė = 𝓕(e,ω,ω̇), ω̇ = 𝓖(ω,e,ė). (ACS-2) Structural asymmetry: coupling operators f ≢ g **as operator types** (differ in functional form, e.g. polynomial vs absolute value — not merely parameter values). (ACS-3) Mutual constraint: no admissible state reachable by varying one field with the other held arbitrary.
- **`def:FF` — Form and Function.** Form **e** carries *structural* information (boundary conditions, equilibrium geometry, admissible-state space). Function **ω** carries *dynamic* information (generator of change). "Form constrains what Functions are realisable; Function determines which Forms are stable."
- **`def:DI` — Information asymmetry.** ΔI(F→Φ) = TE(F→Φ) − TE(Φ→F). ΔI>0 Form drives Function; ΔI<0 Function drives Form; ΔI=0 symmetric/Abelian.
- **`def:acs-measure`.** Deterministic phase flow (X×Y, Φ_t) assumed ergodic with invariant measure μ; ΔI computed w.r.t. μ; multiple attractors ⇒ apply per ergodic component. Domain-specific: primes → μ = Σ_n δ(x − log p_n); zeros → GUE pair-correlation measure; gauge fields → Liouville measure on {H=0}∩{G_i=0}∩{H_a=0}.
- **`def:nested` — Nested coupling orders and emergence.** ΔI(ε) = α₁ε + α₂ε² + α₃ε³ + …; 1st = direct coupling; 2nd = Lie bracket [f,g]; 3rd = **holonomy term**. *Emergent pattern is defined precisely as the 3rd-order holonomy* — the part irreducible to direct or bracketed coupling. Valid for ‖ε‖ < r_BCH = π.
- **`def:holo` (C) — Holographic resolution.** (HR-1) Boundary completeness I(∂S;C) = H(C); (HR-2) Interior redundancy I(∂S;int(S)|C) = 0; (HR-3) Outward gating ΔI(S→exterior) < 0. Ryu–Takayanagi recovered at ΔI = 0.
- **`def:self-resolving` (C).** S carries an intrinsic measure μ(t) that becomes nonzero and legible *within S's own record* whenever S begins to invert its ΔI. Prototype: Bianchi identity.
- **`def:stationarity` (B).** 𝒮(N,X) = Var_{x∈[X,2X]}[F_N(x)] / Σ_{k≤N}|A_k|². F_N *uniformly stationary* iff sup_{X>2} 𝒮(N,X) < ∞ for all N.
- **Spectral witness (B′).** A frequency ω at which F_w(ω) = (1/W)Σ_k w(γ_k)e^{−iωγ_k} carries amplitude. **Matrix candidate**: a proposed self-adjoint operator whose spectrum would be {γ_k}.

---

## 3. Named results

| Label | Statement | Depends on |
|---|---|---|
| **`lem:bch-te` — BCH–TE morphism** (the technical core) | ΔI(ε) = ε⟨f−g, ∇log dμ/dν⟩_μ + 2ε²⟨[f,g], ∇log dμ/dν⟩_μ + O(ε³). The factor 2 arises from bracket antisymmetry under X↔Y (contributions add, not cancel). | Schreiber's KL form of TE; first variation of D_KL; **exact Cartan formula**. Symbolically verified on ℝ² polynomial fields. Non-compact M needs integrability of dμ/dν, f, g. |
| **`thm:acs-DI` — ACS generates non-zero ΔI** | For generic (f,g) outside a Lebesgue-null set in C², with f≢g and ε within BCH radius: ΔI(ε) ≠ 0 for all but finitely many ε>0. β₁ = f−g, β₂ = [f,g], β₃ = [[f,g],g]/12 − [[f,g],f]/12. | `lem:bch-te` |
| **`thm:YM-abelian`** | f≡g ⇒ ΔI=0, [f,g]=0 ⇒ U(1). f≢g ⇒ [A_μ,A_ν]≠0 ⇒ SU(N). ACS-2 satisfied geometrically since F is a 2-form and A a 1-form. | `thm:acs-DI` |
| **`thm:gravity-acs`** | (e^a_μ, ω^{ab}_μ) is an ACS: 1st order T^a; 2nd order R^{ab}; self-resolving Bianchi. | `def:acs` |
| **`lem:torsion`** | T^a is the 1st-order coupling; vacuum Palatini δS/δω = 0 ⇒ T^a = 0, **reached dynamically**. Torsion activated three non-circular ways: (a) Einstein–Cartan spin sources; (b) **BKR geometric defects** (disclinations — no matter fields, no action change); (c) Poincaré gauge gravity with βT^a∧*T_a. **Route (b) establishes torsion precedes any spinor field ⇒ no circularity.** | Palatini action |
| **`thm:SM-containment`** | 𝔰𝔲(3)⊕𝔲(1)_{B−L} (dim 9) embeds in 𝔰𝔲(4) via Pati–Salam, Y = diag(⅓,⅓,⅓,−1). The **full** SM algebra does *not* embed as a commuting direct sum: by Schur, Z_{𝔰𝔲(4)}(𝔰𝔲(3)) = 𝔲(1) exactly. 𝔰𝔲(2)_L must come from the O(4) fiber. | Schur; 160 constraint equations solved over ℚ[i] |
| **`thm:image-phi`** | Im(Φ) = 𝔰𝔩(4), 15-dimensional. | Tr([A,B])=0; of 96 pairs, 72 nonzero; the 72×16 matrix has **exact rank 15** over ℚ |
| **`prop:palatini-decomp`** | [𝔬(4),𝔬(4)] = 𝔬(4), dim 6. [Sym₀(4),𝔬(4)] spans 9. Total 15. 𝔰𝔩(3,ℝ) embeds **5 in torsion** (Cartan H₁,H₂ + symmetric root vectors) and **3 in Lorentz** (antisymmetric). With Y in torsion, 𝔰𝔩(3,ℝ)⊕𝔲(1) splits 6+3. **Neither sector alone contains colour.** | exact integer rank over ℚ |
| **`prop:selection` — Closure attractor uniqueness** | 𝒟(V) = Σ_{i<j}‖[T_i,T_j] − Π_V([T_i,T_j])‖ / Σ_{i<j}‖[T_i,T_j]‖. 𝒟(𝔰𝔩(3,ℝ)) = 0 (<10⁻¹⁴). 50,000 uniform Gr(8,15) samples: 𝒟 > 0.49 always. Perturbation stable: 𝒟<0.03 for ε≤0.01. | **Explicitly a numerical observation, not a classification theorem**; cross-checked vs Dynkin 1952 |
| **`prop:chirality`** | Among J(T) = α·sym(T) + β·anti(T), closure preservation *and* skew-Hermiticity hold **iff** α∈iℝ, β∈ℝ. Unique: J(T) = i·sym(T) + anti(T) → compact real form 𝔰𝔲(3); all **28 brackets** close, all skew-Hermitian, all traceless. | Layer 1: Cartan's uniqueness of the compact real form. Layer 2: grid scan. Restriction to sym/anti justified as the eigenspace decomposition of the Cartan involution θ: T ↦ −Tᵀ |
| **`thm:no-su3`** | 𝔰𝔲(3) ↛ 𝔬(4): dim 8 > 6 ⇒ nontrivial kernel; 𝔰𝔲(3) simple ⇒ kernel is 0 or all; injectivity fails ⇒ only the zero map. | simplicity |
| **`thm:BI`** | ΔI = 0 at a horizon with I_Form(j) = log(2j+1), I_Func(j) = 2πγ√(j(j+1)) ⇔ **Z(γ) = Σ_j (2j+1)e^{−2πγ√(j(j+1))} = 1**, solved by γ_ACS = 0.2741. Recovers Meissner (2004). | `lem:bch-te` |
| **`thm:WdW`** | 3-node spin network (dim 8): ‖G‖=7.65 (1st), ‖D‖=6.00 (2nd), ‖Ĥ‖=0.87 (3rd). Lindblad steady state: ⟨Ĥ⟩=3×10⁻⁶; ‖[Ĥ,ρ_∞]‖<10⁻³; Tr(P_{ker Ĥ}ρ_∞)=0.507 > 0.500 baseline. Constraint hierarchy ‖G‖>‖D‖>‖H‖ matches BCH norm ordering. | `spin_network_lindblad.py` |
| **`thm:FN-acs` (T4)** | **RH ⇒ F_N stationary**, via AM–GM. Non-cancellation for finite sums from strict positivity of each excess. Converse = T4′. | explicit formula |
| **`prop:wronski-lie`** | [f,g] = f′g − g′f on C¹((0,∞)) is a Lie bracket (antisymmetry immediate; Jacobi by six terms cancelling in pairs). | — |
| **`rem:not-poisson`** — a **disproof** | W[fg,h] − (f·W[g,h] + g·W[f,h]) = **−fgh′**, exact ⇒ not a Poisson bracket. The prime–zero ACS is *not* a Hamiltonian system with the Wronskian as symplectic form. Any genuine symplectic structure must live on mode-amplitude space (A_k, γ_k). | `src/paper_b/wronskian_leibniz.py` |
| **`thm:vonKoch-acs`** | Δ_norm(u) = (ψ(e^u) − e^u)/e^{u/2} ~ −Σ_ρ e^{(ρ−½)u}/ρ. Bounded under RH; unbounded if any Re ρ₀>½. **Explicitly a restatement of von Koch (1901), not new; forward direction only.** | — |
| **`thm:T4prime` — conditional** | Assuming δ_N = min|γ_k−γ_j| > 0 with induced C<1 (verified to N=200, **not proved**): equivalent are (i) all zeros on Re s=½; (ii) F_N uniformly stationary ∀N; (iii) lim_X 𝒮(N,X)<∞ ∀N. Off-line σ₀>½ ⇒ 𝒮 ≥ c·X^{2(σ₀−½)}. | sinc bound; Weyl density; Gallagher large sieve; diagonal dominance |
| **`thm:variance`** | Var_X[T₁₂] = O(X^{2σ})ΣA_k²; Var/T₁₁² = O(X^{2σ−2}) → 0 for σ<1; **σ=½ gives the fastest diagonalisation, O(X⁻¹)**. | 100 Odlyzko zeros |
| **`thm:sho` (Remark)** | y_k(t) = e^{−σt}φ_k(t) satisfies y_k″ + γ_k²y_k = 0 for **all** σ∈(0,1). Explicitly labelled *definitionally true* — a **self-correction** of an earlier draft that claimed it held only at σ=½. | — |
| **`prop:rotation`** | At σ=½: ω_k = −2√x·cos(γ_k ln x) — pure cosine, zero radial component. At σ≠½ a sin component appears with coefficient γ_k(σ−½) ⇒ spiral. **σ=½ is the unique center manifold.** | `riemann_tensor.py` |
| **`lem:zero-modes` (C)** | Zero eigenvalues of K = RRᵀ are zero-energy deformations aligned with gauge redundancies. Icosahedral tensegrity (12 nodes, 6 struts) gives exactly 6 zero modes = dim SO(3) + translations. | Connelly–Whiteley 1996 |
| **`thm:inversion` (C)** | If S solves C₀ with ΔI>0, then when S becomes the dominant access structure S = C₁ and ΔI < 0. "The key has become the lock." Proof: role reversal f↔g; ΔI is odd at 1st **and** 2nd order since [g,f] = −[f,g]. | `lem:bch-te` |
| **`thm:killing` (C)** | **tr([X,Y]X) = 0 = tr([X,Y]Y)** for any matrix Lie algebra. Bracket output is trace-orthogonal to both inputs. | trace cyclicity |
| **`prop:non-trav` (C)** | π_X(M) = [tr(MX)/tr(X²)]·X satisfies π_X([X,Y]) ≡ 0. No information from B = [X,Y] traverses back to X. The ACS rereading of **ER=EPR** with no bulk geometry invoked. | `thm:killing`; residual <10⁻¹⁶ |
| **`thm:taxonomy` (C)** | Via Jordan–Chevalley X = X_s + X_n: **elliptic** (imaginary eigenvalues, rotational/periodic), **hyperbolic** (real, exponential, no 2π closure), **parabolic** (X_s=0, X_n≠0, polynomial). | Jacobson, Bourbaki |
| **B′ §8.2 (T2)** | 2000 random Palatini connections: [e,ω] central component **8.88×10⁻¹⁶**. 𝔰𝔩(4,ℝ) simple, centre {0}, [e,ω] traceless ⇒ nonzero scalar holonomy algebraically impossible. | simplicity |
| **B′ §9.1 (T2)** | Y restricted to the colour triplet = (⅓)I₃ ⇒ [Y, 𝔰𝔲(3)] = 0 by Schur. **Corrects an earlier mislabelling** of U(1)_{B−L} as non-abelian (a diagonal non-identity matrix fails to commute with generic off-diagonal probes). | Schur |
| **B′ §9.4 (T2)** | K(T_{B−L},T_{B−L}) = 8Tr(T²) = 32/3 ⇒ coupling/K = (32/9)/(32/3) = **1/3** = quark B−L charge; gap²/K = (4/3)²/(32/3) = **1/6**. Because the content is a *charge*, the holonomy path scale θ **cancels**. | — |
| **B′ §12.3 — charge/coupling epistemic split (T2)** | Charge-type observables (eigenvalues, charges, ratios) forced exactly (θ cancels); coupling-type observables (Higgs quartic, masses) carry an **irreducible ~1% EW-scale normalisation residual**. Called "the organising result" of B′. | §12.1–12.2 negatives |

### Conjectures
- **`conj:lepton` (A)** — chiral zero-modes of D_T fall into (1,2)_{−1/2} ⊕ (1,1)_1. "Most tractable next step."
- **`conj:gl4-precise` (A)** — does a vacuum + SSB pattern exist giving residual 𝔰𝔲(3)⊕𝔰𝔲(2)⊕𝔲(1) with correct fermion reps? Claimed **decidable by an explicit ~10-page Lie-theory computation**; either outcome is informative.
- **`conj:SM`, `conj:fermions` (C/monograph)** — SM from GL(4) fiber; geometric fermions from torsion.
- **`conj:WdW`** (monograph P2) — **upgraded to `thm:WdW`** in Paper A (verified on a 3-node toy).
- **B′ §10 (T3)** — height floor T_min(d,q) = (2πe)^d/q, 2πe ≈ 17.08. Degree enters linearly upstairs but exponentially in the floor; conductor lowers it linearly.

---

## 4. Numbers

### Algebra / structural (exact)
| Symbol | Value | Script |
|---|---|---|
| dim Im(Φ) | **15** = dim 𝔰𝔩(4) | — |
| Lorentz / torsion split | **6 + 9** | — |
| 𝔰𝔩(3,ℝ) placement | **5 torsion + 3 Lorentz** (6+3 with Y) | — |
| 𝒟(𝔰𝔩(3,ℝ)) | **1.4×10⁻¹⁶** (fig) / **<10⁻¹⁴** (prop) | `selection_full.py` |
| min random 𝒟 (50k) | **>0.49**; fig: 0.50 (2,000 shown) | `acs_verify_all.py` |
| 𝔰𝔲(3) closures | **28/28**, all skew-Hermitian, all traceless | `chirality_uniqueness.py` |
| ‖Jacobi‖ (3-gen truncation) | **6×10⁻¹⁵** | `three_generations.py` |
| ad³_{T_{B−L}} | **= (16/9)·ad**; spec {0, ±4/3} | `spectral_taxonomy.py` |
| K(T_{B−L},T_{B−L}) | **32/3** = 8Tr(T²) | B′ App. B |
| Tier-0 torsion coupling | **0** (9 generators) | `torsion_higgs_vacuum.py` |
| Tier-2 torsion coupling | **32/9 = 3.5556** (6 generators) | same |
| Killing per Palatini pair | K(A_{i3}) = **−16**, K(S_{i3}) = **+16** | same |
| ρ_vac^(bosonic) | **exactly 0** (+512/3 − 512/3), exact rational SymPy | `acs_vacuum.py` |
| CC reduction | 10¹²¹ → **~10⁵⁵** orders | — |
| ‖[[f,g],f]‖² (gauge-boson) | **512/81** | `higgs_channel_decomp.py` |
| ‖[[f,g],g]‖² (Higgs) | **128/9** | same |
| Koide projection cos²∠ | **2/3 exact to 10⁻¹⁶** | `higgs_derivation.py` |
| Cartan-averaging off-diagonal max | **0.000000 exactly** | — |
| Autocorrelation, ordered geodesic on T¹⁵ | **0.95 in 15D → 0.23 in 3D** | — |

### Physics vs experiment (Paper A PDG table)
| Observable | ACS | PDG | Pull | Mechanism |
|---|---|---|---|---|
| m_H (GeV) | **124.7** | 125.25 ± 0.17 | 3.2σ | Koide projection |
| sin²θ_W(M_Z) | 0.2312 | 0.23121 ± 0.00004 | 0.3σ | PS structure (3/8 run down) |
| α_s (26 GeV) | **0.1415** = (4/3)²/4π | 0.140 ± 0.005 | 0.3σ | g = 4/3 |
| γ_BI | **0.274** | 0.274 ± 0.003 | 0.0σ | TE balance |
| θ₀^Koide (deg) | **12.76** = arctan λ_W | 12.73 ± 0.03 | 1.0σ | Cabibbo chain |
| θ₁₂^PMNS (deg) | **32.4** | 33.41 ± 0.75 | 1.3σ | TBM + Cabibbo |
| θ₁₃^PMNS (deg) | **9.2** | 8.57 ± 0.12 | **5.2σ** (weakest) | λ_W/√2 |
| m_ν M_R (eV²) | **2400** | 2401 ± 50 | 0.0σ | see-saw |
| θ_QCD | **0** | 0 | exact | real 𝔰𝔩(4) |

- **λ_Higgs = 2√3/27 = 0.1283** vs λ_SM = 0.1294 ⇒ **0.85%**. m_H = √(2λ)v = **124.7 GeV**. Factor anatomy: 2 from Frobenius norm of Lorentz generators, √3 from the 𝔰𝔩(4) Killing form (K = 8Tr), 27 = 3³ from three colour-lepton generators cubed, 2/3 from Koide projection. Mexican-hat fraction: **15.9%** of random Palatini directions.
- **Koide Q = 0.666661** vs 2/3; fits charged leptons to 0.001%. A = 17.72 MeV^{1/2}; θ₀ = 12.73°. **tan θ₀ = λ_Wolfenstein = sin θ_Cabibbo**; arctan(0.22650) = 12.76° (0.7σ). Reconstructs m_e to 2.7%, m_μ to 0.24%, m_τ to 0.01%. RG shift of θ₀ over 33 e-folds: **0.002°**.
- **Cabibbo chain:** √(m_d/m_s) = 0.2236 ≈ λ_W = 0.2265 (1.3%) = tan θ₀^Koide.
- **See-saw:** m_D = m_e²/(3m_τ) ≈ **49 eV**; m_ν × M_R ≈ **2400 eV²** (0.1%); m_ν ≈ 0.049 eV ⇒ **M_R ≈ 49 keV**, X-ray line at **24.5 keV**, θ² ~ 10⁻⁶, τ ≈ 2×10¹¹ yr. Suppression ladder: 511,000 eV →(×m_e/m_τ) 147 eV →(×1/3) 49 eV →(×m_D/M_R) 0.049 eV. **Dodelson–Widrow overproduces by ~10⁵ ⇒ not single-component DM.**
- **Quark Koide:** Q_up = 0.85, Q_down = 0.73. Deviation is *not* QCD (1-loop γ₀ = 1/π identical for all quarks ⇒ scale-invariant ratio; 2-loop moves it *away* from 2/3).
- **CKM:** Fritzsch texture gives |V_us| = 0.170 (obs 0.225, 24% off, zero free parameters). **Full BCH texture computation gives V_CKM = 𝟙 exactly** — a negative result kept — with algebraic cause M_u − M_d = (h−h̃)(κ₁−κ₂).
- **Gauge locking:** g₄ = g_L = g_R = **4/3**; h̃/h = **2/3**; N_gen = **3**; 2ρ₁+ρ₂ = **16/9**; α₂ = 0; β_c = 0 (tree). Free: ρ₁ ∈ (0, 8/9), α₁ with |α₁| < 0.81, tan β. Calibrations v, v_R. **Total 6 inputs** vs SM 19+ (≈3.2×). Branch B costs 7.
- **tan β:** ≈30–60 for m_t/m_b ~ 40; B→τν shows a 1.7σ excess consistent with tan β ~ 30–50 at m_{H+} ~ 500 GeV.
- **Integer automaton:** uncoupled −0.000063; symmetric −0.000063; asymmetric (f=x², g=|y−8|) **−1.499**; swapped **+1.499**. ⚠️ Paper A's Computational Addendum: with subsampled ICs, ℤ₁₆ gives −0.855/+1.531; ℤ₃₂ −1.567/+1.060; ℤ₆₄ −2.233/+0.845; dominance ratio R(16)=0.56, R(32)=1.48, R(64)=2.64 — **inverts with N**.
- **Ricci flow:** curvature variance reduced **41×** in 800 steps.
- **Torsion lattice chirality (monograph only):** index 0 at T^a=0 for every size; at T^a≠0: 8×8→21, 12×12→45, 16×16→77, 20×20→121, 24×24→175, 32×32→309; |index|/N → **≈0.30**.

### Paper B numerics
- Wronskian at σ=½, t=1: all 1,225 pairs of the first 50 zeros nonzero, |W| ∈ **[8.6×10⁻⁵, 0.19]**; extended to all **19,900** pairs of 200 zeros, no exceptions. Jacobi verified to **3×10⁻¹⁰** (limited by Δt=10⁻⁶).
- Variance scaling (100 zeros): X=10² ratio 2.73 (pred 2.72); 10³ 4.33 (4.32); 10⁴ 6.92 (6.84); 10⁵ 10.93 (10.84). **<2% over three decades.**
- Cross-term constant C = 0.26 (N=25), 0.28 (N=100), **0.29 (N=200)**.
- y_k″ + γ_k²y_k = 0 verified to **<9×10⁻¹⁴** across 1,000 evaluations.
- **Stationarity exponents** (N = 2,001,052 zeros): α(50) = −0.000200; α(200) = +0.000875; α(10⁵) = +0.001247; α(2×10⁶) = **+0.001259**. Deviation bounded by 1.3×10⁻³.
- **Off-line injection** at γ_fake = 1000, predicted α = 2σ−1: σ=0.40 → −0.197; 0.45 → −0.099; 0.55 → +0.099; 0.60 → +0.199. **All within 1.5%.**
- |C_200| = **0.044**; |C_{2,001,052}| = **7.00×10⁻⁶** vs 4.4×10⁻⁴ expected from N^{−1/2} (63× smaller) ⇒ **|C_N| ~ N^{−0.95}**.
- Arithmetic bridge: mod-6 residue lattice, 5×10⁷ primes to 10⁹, cross-class transition-fraction variance suppressed to **29.2%**, matching R = 1/(1+55×0.044) = **0.292** with N_eff = 56.
- R₂ at N=5,000 (12,497,500 pairs): 0.97 at α≈1, 0.98 at α≈3. R₃ at N=50,000 (606,189 triples): **RMSE 0.051**, max residual 0.182, **Pearson 0.990**.
- **Fourier dual** at N=10⁵: top 20 peaks all align to prime powers within 1.8×10⁻⁴, **mean distance 5×10⁻⁵** vs random baseline 4.3×10⁻² (833× closer), KS p < 10⁻⁴. Rank 10 is ω=4.15888 → **2⁶=64** — the load-bearing prime-power confirmation.
- **L(s,χ₄):** 122 zeros by sign changes of Λ(s,χ₄), bisected to 10⁻¹⁰, range [6.02, 198.79]. Top 19 peaks: **19/19 = 100% sign accuracy** (binomial p = 2×10⁻⁵). Includes 3³=27 (χ₄=−1) and 5²=25 (χ₄=+1).
- **Dirichlet decomposition:** (F_ζ−F_L)/2 top 15 all ≡3 mod 4; (F_ζ+F_L)/2 top 15 all ≡1 mod 4. Both **15/15**. Powers of 2 appear equally (ratio 0.95, 0.99).
- **Dedekind ζ_K, K=ℚ(i):** 19/20 top peaks align within 0.05. Mean |F_K|: split **0.323**, inert at log p **0.057**, inert at log p² **0.144**. **Split/inert ratio 5.7×**.
- **Hilbert–Pólya GUE test:** R₂ RMSE Riemann 0.597 vs GUE 0.600 (indistinguishable); Fourier-dual alignment ratio Riemann 0.012 vs GUE 0.495 — a **40× gap**. Scorecard: Riemann PASS/PASS/PASS/PASS; GUE matrix PASS/PASS/FAIL/FAIL; Poisson PASS/FAIL/FAIL/FAIL.
- Berry–Keating leading semiclassical counting matches Riemann–von Mangoldt to within ~1 zero through T = 143.

### Paper B′ numerics (seed 20260423, 10⁵ zeros)
- Mean spacing **1.0000**, variance **0.16075**. Spacing L² to GUE **2.64×10⁻³**, to Poisson **4.18×10⁻¹**.
- Pair correlation vs Montgomery (r>0.2): 0.988 at M=2×10⁴ → **0.993** at M=6×10⁴ (monotone).
- **SFF:** ramp slope **1.031**, plateau **1.004**, knee at τ_H = 1. **Methodological negative kept:** the untapered estimator gave a spurious +6.83 small-τ excess (pure leakage); Hann tapering collapses it to −0.018.
- **Prime orbits:** cumulative weight tracks the ramp to corr **0.973**; **overshoot 4.33 at τ=2** while true SFF stays at 1 ⇒ plateau held by off-diagonal orbit correlations.
- **Fourier dual: 14/14 on-prime** at threshold 0.12. Sweep 0.30→0.02 gives 10/11/14/15/15/15 peaks, **100% hit rate every time, zero off-prime peaks**; tolerance tightenable 0.035 → **0.005** (7×) with all 14 surviving.
- **Falsified (T4) #1 — action-proximity:** pair-density log–log exponent **−0.01** (flat); mechanism needs ~Δτ⁻¹.
- **Falsified (T4) #2 — difference tones / Tartini:** real contrast **1.136** vs null 1.044 ± 0.074 ⇒ **1.2σ**. Mechanism: prime logs mutually incommensurable — **unique factorisation spectrally expressed**. The real arithmetic off-diagonal is Hardy–Littlewood prime-pair correlation.
- **Diagnostic arms:** abelian U(1) Berry ‖D−I‖=1.372, ‖D−scalar‖=**0.000**, ‖[D,H]‖=**0.000**; non-abelian 𝔰𝔲(2) 0.512/0.486/**2.155**. *Negative kept:* the first abelian attempt was rigged trivial, rebuilt with genuine path-dependent Berry flux.
- **Pati–Salam:** SU(3)_C norm 2.30 non-commuting; coset 3+3̄ norm 1.52; U(1)_{B−L} = diag(0.067i,0.067i,0.067i,−0.202i) with [B−L, SU(3)_C] = 0.00. Real ACS colour sector gives **‖[D,H]‖ = 6.29**.
- **Two-branch signature:** retain B−L ⇒ **mixed**; quotient B−L ⇒ pure non-abelian. Falsifier: B−L testing non-abelian, or any simple sector testing abelian.
- **RGE test of λ:** 0.1294 (m_H), 0.0954 (10³), 0.0381 (10⁶), 0.0159 (10⁹), 0.0085 (10¹²), 0.0091 (10¹⁵). Crosses λ_ACS = 0.1283 **exactly once at μ ≈ 132 GeV** (0.05 e-folds above m_H) then falls monotonically ⇒ **high-scale reading falsified**.
- **Form/function witnesses** (60 surrogates): arithmetic 0.0636 vs 0.00001 ⇒ **z ≈ 11,497 FUNCTION**; lag-1 −0.357 vs −0.0010 ⇒ **z ≈ 97 FUNCTION**; spacing z=1.0, counting z=1.0, Wigner shape z=0.4 — all **FORM**. Scaling: arithmetic 3030σ (N=2×10⁴) → 11,497σ (10⁵); lag-1 51σ → 97σ. **Honest caveat flagged:** the arithmetic *raw* value *decreases* (0.0922 → 0.0636) while significance rises. Effective rank ≈ 4 on both real and surrogate.
- **T_min table:** d=1 → 17.1; d=2 → 291.7; d=3 (S₄) → 4,982.2 (gated); d=5 (A₅) → 1.45×10⁶ (out of reach).

### Paper C numerics
- **Three distinct ambiguity numbers, explicitly warned not to conflate:** (a) passive/subspace dim B^⊥ = n²−2 = **14**; (b) generic active dim ker dμ = **15**; (c) degenerate at (H₁,A₀₁): rank 11, dim ker = **19**.
- [H₁, A₀₁] = **2 S₀₁** (chirality hopping, exact integer); tr(S₀₁H₁) = tr(S₀₁A₀₁) = 0.
- Killing orthogonality residual ~10⁻¹⁵ over 1,000 random pairs in 𝔰𝔩(3,ℝ) and 𝔰𝔩(4,ℝ).
- **‖exp(2π ad_{T_{B−L}})‖ ~ e^{8π/3} ≈ 4,348**, not 1 ⇒ the flow does not close (kills the universal-2π claim).
- Spectral classes: SU(2) quaternion {±i} **elliptic** (2π = −I); Frenet–Serret {0, ±i√(κ²+χ²)} elliptic; 𝔰𝔩(4,ℝ) T_{B−L} {0, ±4/3} **hyperbolic**; core rope ring {−1,0,+1} hyperbolic.

---

## 5. Coinages

**ACS**, **Form/Function fields**, **ΔI**, **BCH–TE morphism**, **emergent pattern** (= the
irreducible 3rd-order holonomy), **closure defect 𝒟 / closure attractor**, **chirality map J**,
**torsion sector / Lorentz sector**, **tier 0/2 torsion hierarchy**, **spectral stability ratio
ρ_spec**, **stationarity measure 𝒮(N,X)**, **inversion arc**, **holographic resolution**,
**self-resolving structure**, **constraint–attractor cycle**, **algebraic non-traversability**,
**spectral witness / matrix candidate**, **charge/coupling epistemic split**.

Two worth stating in full:

- **Layered resolution structure / strict typing rule** (A, `rem:layers`): Layer 0 base Forms; Layer 1 Functions 𝓕₀→𝓕₀ (torsion); Layer 2 bracket 𝓖₁×𝓖₁→𝓕₁ (curvature); Layer 3 holonomy 𝓗₂×𝓖₁→𝓕₂ (Bianchi). **A Function at layer n acts only on objects from layers < n and produces a Form, never a Function.** Verified: cumulative rank 2→3→5 in 𝔰𝔩(4). **Self-reference is blocked** — a Gödelian fixed point would need a Function acting on a Form encoding its own behaviour, which the typing forbids.
- **Dimensional devolution** (A): complexity *decreases* downward; particles are projections of the 15-D 𝔰𝔩(4) fiber onto 3+1D. Compression 𝔰𝔩(4)[15D] → 𝔰𝔲(3)[8D] → Cartan[2D] → singlet[0D]. Testable: any system chaotic in d dimensions gains order when embedded in d+k, saturating at the algebraic dimension of the governing Lie algebra.
- **Tartini tones** — combination frequencies γ_k ± γ_j from the non-vanishing Wronskian; explicitly **intra-spectral (zero–zero) only**, never prime–zero. The ACS signature is **complementary cancellation, not resonance**: "an asymmetric codependent pair does not resonate across the Form/Function boundary, it *closes* across it."
- **Arithmetic lattice structure** (A) — all native dimensionless quantities (1/3, 4/3, 16/9, 2/3, 3, 9) lie in the multiplicative subgroup ⟨2,3⟩ ⊂ ℚ^×; the same lattice as Pythagorean tuning. **Explicitly recorded with no phenomenological consequence claimed** (the companion note's empirical test returns a clean negative).

---

## 6. Key equations

```latex
% BCH–TE morphism (the technical core)
\Delta\mathcal{I}(\varepsilon)=\varepsilon\langle f-g,\nabla\log\tfrac{d\mu}{d\nu}\rangle_\mu
+2\varepsilon^{2}\langle[f,g],\nabla\log\tfrac{d\mu}{d\nu}\rangle_\mu+\mathcal{O}(\varepsilon^{3})
[\mathcal{L}_f,\mathcal{L}_g]=\mathcal{L}_{[f,g]}          % exactness source
\beta_1=f-g,\quad \beta_2=[f,g],\quad \beta_3=\tfrac{1}{12}[[f,g],g]-\tfrac{1}{12}[[f,g],f]

% Palatini ACS
T^a=de^a+\omega^a{}_b\wedge e^b,\qquad R^{ab}=d\omega^{ab}+\omega^a{}_c\wedge\omega^{cb}

% Closure defect / chirality map
\mathcal{D}(V)=\frac{\sum_{i<j}\|[T_i,T_j]-\Pi_V([T_i,T_j])\|}{\sum_{i<j}\|[T_i,T_j]\|}
J(T)=i\,\mathrm{sym}(T)+\mathrm{anti}(T)

% Barbero–Immirzi balance
Z(\gamma)=\sum_{j=1/2,1,3/2,\dots}(2j+1)e^{-2\pi\gamma\sqrt{j(j+1)}}=1\;\Rightarrow\;\gamma_{\rm ACS}=0.2741

% Higgs from BCH
V(r)=r^{2}(\|f-g\|^{2}-\|[f,g]\|^{2})+r^{4}\|[[f,g],\cdot]\|^{2}
\lambda=\frac{2\sqrt3}{27}=0.1283,\qquad m_H=\sqrt{2\lambda}\,v=124.7~\mathrm{GeV}

% Koide + Cabibbo + see-saw
\sqrt{m_i}=A\bigl(1+\sqrt2\cos(\theta_0+2\pi i/3)\bigr),\qquad
\tan\theta_0=\lambda_{\rm W}=\sin\theta_C\approx\sqrt{m_d/m_s}
m_\nu\times M_R=\frac{m_e^{4}}{9m_\tau^{2}}\approx 2400~\mathrm{eV}^2

% Vacuum energy cancellation
\rho_{\rm vac}^{(\rm bos)}=\sum_{X\in\mathfrak{sl}(4)}\|[T_{B-L},X]\|^{2}K(X,X)=0,\quad K(X,X)=8\,\mathrm{Tr}(X^{2})

% Riemann spectral function  (⚠ see §7 item 6 — three incompatible φ_k conventions in B)
F_N(x)=\sum_{k=1}^{N}A_k\varphi_k(x),\quad A_k=\frac{1}{\frac14+\gamma_k^{2}}
\mathcal{S}(N,X)=\frac{\mathrm{Var}_{x\in[X,2X]}[F_N(x)]}{\sum_k|A_k|^2},\qquad \alpha=2\sigma-1

% Wronskian bracket and its Leibniz failure
W[f,g]=f'g-g'f,\qquad W[fg,h]-\bigl(fW[g,h]+gW[f,h]\bigr)=-fgh'

% Renormalised stability / resolvent
\Delta_{\rm norm}(u)=\frac{\psi(e^{u})-e^{u}}{e^{u/2}}\sim-\sum_\rho\frac{e^{(\rho-1/2)u}}{\rho}
\chi(\omega)=\sum_\rho\frac{1}{\omega-\gamma_\rho}=\mathrm{Tr}\bigl[(\omega I-H)^{-1}\bigr]

% Stress tensor; rotation at the critical line
T=\begin{pmatrix}x & -\sum_\rho\mathrm{Re}(x^\rho/\rho)\\ -\sum_\rho\mathrm{Re}(x^\rho/\rho) & 0\end{pmatrix}
\omega_k\big|_{\sigma=1/2}=-2\sqrt{x}\cos(\gamma_k\ln x)

% Fourier dual & unfolding
F_N(\omega)=\frac1N\sum_{k=1}^{N}\cos(\omega\gamma_k),\qquad
\bar N(t)=\frac{t}{2\pi}\log\frac{t}{2\pi}-\frac{t}{2\pi}+\frac78

% GUE forms
R_2(\alpha)=1-\left(\frac{\sin\pi\alpha}{\pi\alpha}\right)^2
R_3(\alpha,\beta)=1-s(\alpha)^2-s(\beta)^2-s(\alpha+\beta)^2+2s(\alpha)s(\beta)s(\alpha+\beta)

% Killing orthogonality / non-traversability / saturation / no-go / floor
\mathrm{tr}([X,Y]X)=\mathrm{tr}([X,Y]Y)=0,\qquad \pi_X([X,Y])=0
\mathrm{ad}_{T_{B-L}}^{3}=\tfrac{16}{9}\,\mathrm{ad}_{T_{B-L}},\qquad \mathrm{spec}=\{0,\pm 4/3\}
M_u-M_d=(h-\tilde h)(\kappa_1-\kappa_2)\;\Rightarrow\;|V_{\rm CKM}|=\mathbb{1}
T_{\min}(d,q)=\frac{(2\pi e)^{d}}{q}
```

---

## 7. What the papers explicitly do NOT claim

**Paper A:**
- Does not derive the electroweak sector or CKM mixing angles. Stated as scope in the Introduction.
- **Unitarity/compactness is an imported physical input** — "the bracket algebra does not derive unitarity; it is imposed as a consistency condition." Two stages, two inputs.
- The BCH–TE morphism's extension to infinite-dimensional Palatini field space is **conjectured, not proved**; all physics uses only finite-dimensional 𝔰𝔩(4,ℝ) where it is exact.
- `prop:selection` uniqueness is a **numerical observation over 50,000 samples, not a classification theorem**.
- The chiral zero-mode / spinor reading is "computational evidence, not a theorem."
- S_BH = ∫|ΔI|dσ is "a conjecture; no derivation has been achieved."
- Exact Domagala–Lewandowski γ = 0.2375 not derived — requires full SU(2)_k Chern–Simons state counting. A naive *local* degeneracy reduction fails; the constraint is a **global** singlet projection.
- Higgs quartic: **"Epistemic status: partial derivation."** Two of three factors exact; the Killing/kinetic normalisation carries the entire 0.85% residual. RG running down gives m_H ≈ 148 GeV (18% overshoot) ⇒ the algebra is realised at Λ_PS ~ 10¹⁵ GeV, or torsion partners modify running. "The RG scale is a separate, open problem."
- θ₀'s **exact** value depends on the physical vacuum direction the framework "does not yet determine."
- tan β cannot be fixed within the minimal bi-doublet at perturbative level (gauge-protected flat direction).
- Vacuum-energy cancellation covers **only** the Planck-scale bosonic term — not Coleman–Weinberg loops, the Higgs minimum (~−10⁸ GeV⁴), or fermionic vacuum energy (~+10⁷ GeV⁴).
- The 49 keV sterile neutrino prediction is **the mass value and X-ray line energy, not the DM abundance**.
- GW 0:1:4 coupling suppressed by (v_R/M_Pl)² ≲ 10⁻⁶ ⇒ **untestable in practice** until Einstein Telescope / Cosmic Explorer (~2035+).
- Four open problems for the SM conjecture: (i) unification of the two geometric sources — "has not been achieved"; (ii) *generation* (the bracket must **span**, not merely be contained in); (iii) fermion representations — **resolved**; (iv) chirality of SU(2)_L.

**Paper B:**
- "No assumption about the truth of RH is made." The converse is **conditional** on δ_N > 0 with C < 1, verified only to N = 200.
- `thm:vonKoch-acs` is a reframing of a classical theorem, forward direction only.
- The stripped-mode ODE is *definitionally true* — labelled a Remark after a **self-correction**.
- The plasma-Hamiltonian framing is **disproved** and retained as a boundary marker.
- The L-function results "are not new mathematical theorems; they re-derive classical results (Dirichlet 1837, Weil 1952, Rudnick–Sarnak 1996)."
- **"We have not constructed the Hilbert–Pólya operator."** The contribution is a constraint specification C1–C9 plus test suite, plus the GUE-not-sufficient demonstration. Three structural hints are "conjectural structural specifications... not operator constructions."
- The stress tensor is a **definition**, not derived from a Lagrangian.
- N = 2×10⁶ scaling "is not a proof of the converse."

**Paper B′ "Not established" list (verbatim scope):** RH; any Hilbert–Pólya operator (the wall is
self-adjointness on a well-defined domain); any explicit formula; the vanishing of off-line /
sub-floor artifacts; the explicit value of the ~1% Higgs-quartic kinetic normalisation ("its
character is pinned, its value is not derived"). Only the *necessary* direction of the height
floor is shown. Above τ_H individual witness elimination is **invalid**.

**Paper C:** the algebraic non-traversability is "a statement about the bracket algebra, not a
derivation of holographic entropy bounds or Ryu–Takayanagi." The universal-2π claim is retracted.
The methodological note on **epistemic compression** (Lakatos) lists three narrowings: the 2π
claim, the Wronskian Leibniz failure, and four-class → three-class taxonomy.

**Monograph open problems:** T4′ converse; the SU(3) dynamical identification ("~3 pages of spinor
geometry", "most tractable remaining problem"); the quantum definition of ΔI via Lindblad steady
states; rigorous non-generic case of T1.

---

## 8. Internal inconsistencies — know these before citing

1. ~~**The 0:1:4 torsion hierarchy contradicts itself across papers.**~~ **RESOLVED 2026-08-12.** Both statements are true about different generator sets, now stated explicitly in Paper A (abstract, §torsion-hierarchy, figure caption, predictions) and Paper C. spec(ad_{T_BL}) = {0⁽⁹⁾, (±4/3)⁽³⁾}, so on **eigenvectors** the coupling takes exactly two values, 0 and 32/9. The electroweak generators J_i, K_i are *not* eigenvectors — each is an equal-weight mixture of one Tier-0 and one Tier-2 generator (e.g. J₁ = (A₀₁+A₂₃)/2) — so each inherits ¼·32/9 = **8/9**, giving 0 : 8/9 : 32/9 = **0:1:4**. 8/9 is not a third eigenvalue. Verified in exact rationals.
2. ~~**γ_BI is listed in the PDG comparison table.**~~ **RESOLVED 2026-08-12.** γ_BI and θ_QCD were both counted as PDG observables; neither is (γ_BI compares to the Meissner *theoretical* value, θ_QCD to an experimental *bound*). They are now in a separate labelled block with footnotes, and the headline is restated as **five of the seven PDG-measured observables within 2σ**, exceptions m_H (3.2σ) and θ₁₃ (5.4σ).
3. **m_H is quoted as both 0.42% and 3.2σ** in the same paper without reconciliation.
4. **`prop:selection` numbers drift across versions:** Paper A prop 50,000 samples / 𝒟 > 0.49 / <10⁻¹⁴; figure caption 2,000 samples / 1.4×10⁻¹⁶ / min 0.50; monograph 100 samples / 𝒟 > 0.54. Three thresholds for one claim.
5. **`rem:uniqueness`'s algebraic argument is confused.** It says 𝔰𝔲(3) "realised over ℝ in dimension 2×8 = 16 > 15." 𝔰𝔲(3) is an 8-dimensional *real* Lie algebra; the correct obstruction is that the maximal compact subalgebra of 𝔰𝔩(4,ℝ) is 𝔰𝔬(4) (dim 6 < 8) — exactly what `thm:no-su3` already uses. The dimension-doubling reasoning is a non sequitur.
6. **Three incompatible definitions of φ_k in Paper B.** §2.1: φ_k(x) = ½cos(γ_k x) + γ_k sin(γ_k x). §2.2/§5: φ_k(x) = cos(γ_k ln x)/√x. Harmonic-oscillator section: φ_k(t) = e^{σt}[σcos + γ_k sin]/(σ²+γ_k²). This is why the same Wronskian appears once at magnitude ~10⁴ and once bounded by 0.19. **Track which convention is live.**
7. **Two different objects named C in `thm:T4prime`.** The cross-term constant C (0.26–0.29) and the cross-correlation bound |C_N| (0.044 → 7×10⁻⁶) are conflated in §"Cross-correlation decay."
8. **Fourier-dual alignment ratio quoted as 0.0012 (833×) in §7 and 0.012 (40× vs GUE) in §9.** Order-of-magnitude discrepancy within one paper.
9. **The ±1.499 integer automaton table is printed unqualified in Paper B and the monograph**, while Paper A's Addendum reports the magnitude symmetry breaks entirely at ℤ₃₂/ℤ₆₄. The trilogy's most-cited "exact, floating-point-free" number is the one the addendum destabilises.
10. **β₃ sign convention conflicts.** `def:nested` uses [[f,g],f] + [[f,g],g]; the `thm:acs-DI` proof uses [[f,g],g]/12 − [[f,g],f]/12; the Higgs section uses the first form again. The 1/12 factors and relative sign are never reconciled.
11. **γ = 0.274 vs 0.2375: the explanation changed between versions.** The monograph blames a **U(1)** Chern–Simons projection suppressing integer-j states (~36%). Paper A blames a **SU(2)** global singlet projection and explicitly says the monograph's local mechanism *fails*. Both texts are in the repo.
12. **`thm:BI`'s "derivation" is a definition-choice.** Z(γ) = 1 is *asserted* to be what ΔI = 0 means; the BCH–TE expansion is never actually evaluated. This is the weakest link in the flagship 0.0σ result.
13. **`thm:acs-DI`'s proof asserts "for generic (f,g), the centraliser is {λ[f,g]}"** — false for generic elements of most Lie algebras (the centraliser of a regular semisimple element is the Cartan subalgebra, dimension = rank). The measure-zero conclusion may survive; the stated reason does not.
14. **`prop:chirality`'s "only if" is weaker than advertised** — uniqueness holds only *within* the ansatz J = α·sym + β·anti; that the ansatz exhausts the candidates is stated, not proved.
15. **Unverifiable inline citations** with no bibliography entries: "Hofseth and Weinstein (2026)", "Contreras (2026)", "Tamburini (2025)", "Goertz et al. 2025", "MDPI Symmetry, Jan. 2026", "Weinstein's Geometric Unity (2021)".

---

## 9. Figures

| Figure | Paper | Content |
|---|---|---|
| `fig_layers_cycle` | A | Left: strict resolution hierarchy. Right: constraint–attractor cycle T^a=0 → chiral modes → spinor bundle → 𝔰𝔩(3,ℝ)→𝔰𝔲(3) → confinement |
| `fig_ricci_flow` | A | Top: R for sphere / flat torus / Poincaré disk. Bottom: bumpy sphere uniformised, variance ↓41× in 800 steps |
| `fig_closure_attractor` | A | Closure-defect histogram, 2,000 random 8-dim subspaces; 𝔰𝔩(3,ℝ) at 1.4×10⁻¹⁶ vs min random 0.50 — a 10¹⁵ gap |
| `fig_colour_weights` | A + monograph | Weight diagram of the fundamental **3**; both Cartan generators in the torsion sector; lepton at the origin |
| `fig_nuclear_geometry` | A + monograph | Left: gluon exchange as root-vector displacements. Right: reps stacked by Casimir C₂; confinement drives to the singlet |
| `fig_rep_gallery` | A + monograph | Six lowest 𝔰𝔲(3) reps: singlet = point, **3** = triangle, **8** = hexagon, **10** = larger triangle |
| `fig_barbero_immirzi` | A + monograph | Z(γ) curve; Z=1 selects 0.274; DL 0.238 dotted; the 15% gap |
| `fig_torsion_tiers` | A | Tier 0 (9 generators, zero coupling) vs Tier 2 (6, 32/9); each A_{i3} with K=−16 matched by S_{i3} with K=+16 ⇒ exact cancellation |
| `fig_hero_nesting` | A App. C | The ACS nesting chain end to end; Branch A input ledger |
| `fig_sign_reversal` | B + monograph | ΔI sign reversal under f↔g on ℤ₁₆, exact integer arithmetic |
| `fig_variance_scaling` | B | Var ratio (σ=0.6)/(σ=0.5), 50 zeros, three decades vs X^{0.2}, <2% |
| `fig_flow_field` | B | γ₁=14.13: left σ=½ closed loop (pure rotation); right σ=0.7 outward spiral |
| `fig_wronskian_heatmap` | B | W[φ_k,φ_j] at t=1, σ=½, first 20 zeros; antisymmetric, no zero entries, checkerboard |
| `fig_chirality` | monograph | Spectral index vs lattice size; ratio → ≈0.30 (Atiyah–Singer) |
| `fig_selection` | monograph | Older closure-defect histogram: 100 samples, none below 0.54 |

**B′ and C contain no figures** (B′ is tables + two embedded reproducible Python drivers).

---

## 10. What is genuinely strong here

1. **The negatives are first-class and load-bearing.** B′ §7.2 falsifies the framework's *own* difference-tone channel and identifies the reason as unique factorisation expressed spectrally. Paper B's Leibniz remark destroys its own earlier plasma-Hamiltonian foundation. The Elimination Ledger discipline is real, not decorative.
2. **The form/function witness split (B′ §13)** is the sharpest empirical result in the trilogy: five witnesses that all "point at the critical line" separated into 0.4–1.0σ generics vs 97σ and 11,497σ ζ-specifics — with the awkward fact (raw value falling while significance rises) reported rather than buried.
3. **The charge/coupling split (B′ §12.3)** is a genuinely structural epistemic claim, and the RGE test that kills the high-scale reading (λ crosses λ_ACS exactly once, at 132 GeV) is clean and decisive.
4. **Paper C's retraction of "universal 2π inversion"** with the ‖exp(2π ad)‖ ≈ 4348 number is unusually honest for this genre.
5. **Y restricted to the colour triplet = (⅓)I₃** makes the abelian/non-abelian verdict a Schur-lemma fact rather than a probe artifact — and B′ explicitly flags that the original probe *mislabelled* it, which "would render the prediction un-falsifiable."
