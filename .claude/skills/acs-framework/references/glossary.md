# Distilled Glossary — the vocabulary you need to read any ACS paper

Replaces the 292 KB `GLOSSARY.md` for working purposes. Organised by cluster.

**About the source file:** 296,920 bytes, 1,961 lines, titled *"Glossary and Index of Key Terms —
ACS Framework."* Eight thematic sections with **126 primary entries** (`###` headings with a fixed
3-field footer: `**Status:**` tier, `**Source:**` file + section + label + line numbers, `**Also:**`
aliases) plus **236 supporting bullets** = 362 canonical entries. Section 9 is an **alphabetical
index**, 675 rows, of which **312 are `X — see Y` alias redirects** — that alias fan-out is why the
file is 292 KB (the `tier map (T1-T4)` entry alone lists ~35 aliases). Stated scope: *"Falsified
claims are retained here deliberately and marked as such: the corpus keeps its negatives."*
Conventions worth knowing: tier labels are per-claim and never promoted; **SPLIT** verdicts are
common (a "locked constant" is routinely recorded as *value = refraction, relation = invariant*);
retracted claims get their own entries as boundary markers; and the glossary **flags internal
inconsistencies in the papers** (e.g. the Tensegrity-atom entry notes "Paper B attributes the
definition to Paper A, which does not contain it").

---

## A. ACS core ontology

**Asymmetric Codependent System (ACS)** — a pair of smooth fields (F, Φ) satisfying codependence,
structural asymmetry, and mutual constraint. The framework's central object.
**ACS-1 Codependence** — each field's evolution equation depends on both; neither is derivable from
the other alone.
**ACS-2 Structural Asymmetry** — coupling operators f and g differ *as operator types* (polynomial
vs absolute value), not merely in parameter values.
**ACS-3 Mutual Constraint** — no admissible state is reachable by varying one field with the other
held arbitrary.
**Form field (F)** — carries *structural* information: boundary conditions, equilibrium geometry,
the space of admissible states. Instances: vierbein e, field strength F_μν, primes, tensegrity cables.
**Function field (Φ)** — carries *dynamic* information: the generator of change. Instances: spin
connection ω, gauge potential A_μ, Riemann zeros, struts. *Form constrains what Functions are
realisable; Function determines which Forms are stable.*
**ΔI (information-asymmetry functional)** — ΔI = TE(F→G) − TE(G→F). A *definition*, not a result
("Link 1"). ΔI>0 Form drives Function; ΔI<0 the reverse; ΔI=0 symmetric/Abelian.
**Information balance** — the condition ΔI = 0; the claimed cross-domain attractor (Ricci-flat
geometry, colour singlets, RH stationarity, Wheeler–DeWitt) and the halting criterion of the AI stack.
**ACS measure** — the ergodic invariant (SRB) measure making TE well-defined. Primes → log-prime
point process; zeros → GUE pair-correlation measure; gauge fields → Liouville measure on the
constraint surface.
**Nested coupling orders** — ΔI(ε) = a₁ε + a₂ε² + a₃ε³ + …: 1st = direct coupling, 2nd = the Lie
bracket [f,g], 3rd = holonomy [[f,g],f] + [[f,g],g]. Mapped to torsion / curvature / Bianchi, and to
the Gauss / diffeo / Hamiltonian constraints in LQG.
**Emergent pattern** — defined *precisely* as the 3rd-order holonomy: the component of ΔI
irreducible to direct or bracketed coupling; the residue of the closed loop Form→Function→Form.
**Layered resolution structure / strict typing rule** — Layer 0 base Forms → Layer 1 Functions on
base Forms (torsion) → Layer 2 brackets producing Forms (curvature) → Layer 3 holonomy (Bianchi).
A layer-n Function acts only on layers < n and produces a **Form, never a Function**. Claimed to
block Gödelian self-reference.
**Constraint-attractor cycle** — Constraint → Solution → Dominance → Inversion → New Constraint.
Canonical instance: T^a = 0 → torsion activation → chiral modes → spinor bundle → 𝔰𝔲(3) → confinement.
**Inversion arc** — a system that solves a constraint becomes the new constraint; Form/Function roles
exchange and ΔI flips sign exactly at leading order. *"The key has become the lock."*
**Holographic resolution (HR-1/2/3)** — (1) boundary completeness I(∂S;C) = H(C); (2) interior
redundancy I(∂S; interior | C) = 0; (3) outward gating ΔI(S→exterior) < 0. Ryu–Takayanagi claimed
recovered at ΔI = 0.
**Self-resolving structure** — carries an intrinsic measure that becomes legible *within its own
record* when its ΔI begins to invert. Prototype: the Bianchi identity.
**Dimensional devolution** — inversion of micro-to-macro: the fundamental object is the 15-dim 𝔰𝔩(4)
fiber; particles are projections onto 3+1D. Compression 𝔰𝔩(4)[15D] → 𝔰𝔲(3)[8D] → Cartan[2D] →
singlet[0D]. Perceived randomness = "resolution bias" of a low-dimensional detector.
**Exact integer automaton** — the float-free verification instrument: a discrete ACS on ℤ₁₆ with
updates from {x², |x−8|}; swapping which function is polynomial reverses ΔI exactly (−1.499 ↔ +1.499).
**Positional duality / three-layer decomposition** — the zeros split into **density** (Riemann–von
Mangoldt, no arithmetic), **local spacings** (GUE universality), **positions** (arithmetic, via the
explicit formula). *All arithmetic content lives in the positions.*
**One mechanism, many forms** — the synthesis claim that the recurring form/function asymmetry is one
mechanism genuinely *expressed* through many substrates — **ontological**, not epistemic (explicitly
not blind-men-and-elephant). ⚠️ Conditional on Link 3, which the ledger retired.
**Form/Function Relativity** — the {form, function} label is a coordinate on (witness × frame), not
intrinsic. *"One witness's form is another witness's function."*
**Role-relativity in nested systems** — the general principle: ascending a nest can only convert the
*marked* role into the *unmarked* one, so each component flips exactly once at a single threshold.

---

## B. Gauge / algebra (Paper A)

**Palatini bracket [e, ω]** — the Lie bracket of vierbein and connection; generates split real
𝔰𝔩(4,ℝ) (rank 15).
**Asymmetry map Φ** — Φ(v) = [e(v), ω(v)]; the image for generic fields is exactly 𝔰𝔩(4), rank 15
by exact symbolic rank over ℚ of a 72×16 matrix.
**Y¹⁴ (bundle of metrics)** — total space over M⁴ with fiber GL(4)/O(4) (dim 10) + base 4 = 14. The
arena of the gravitational ACS.
**BCH–TE morphism** — ΔI(ε) = ε⟨f−g, ∇log dμ/dν⟩ + 2ε²⟨[f,g], ∇log dμ/dν⟩ + O(ε³). The Lie bracket
**is** the exact 2nd-order Taylor coefficient. Proved for compact finite-dim M; **the
infinite-dimensional Palatini extension is explicitly conjectured.**
**Palatini decomposition** — 𝔰𝔩(4) = 6-dim **Lorentz sector** [𝔬(4),𝔬(4)] (curvature) + 9-dim
**torsion sector** [Sym₀(4), 𝔬(4)]. Colour 𝔰𝔩(3,ℝ) distributes 5+3 across both.
**Closure defect D(V)** — Σ‖[Tᵢ,Tⱼ] − Π_V([Tᵢ,Tⱼ])‖ / Σ‖[Tᵢ,Tⱼ]‖: normalised failure to close.
**Closure attractor** — 𝔰𝔩(3,ℝ) is the unique 8-dim subspace of 𝔰𝔩(4,ℝ) achieving numerically exact
closure (D < 1e-14) against 50,000 random samples all > 0.49. **Explicitly a numerical observation,
not a classification theorem (T3).**
**Chirality map J** — J(T) = i·sym(T) + anti(T); by Cartan's classification the unique such map
carrying 𝔰𝔩(3,ℝ) to the compact form 𝔰𝔲(3).
**Two-stage selection mechanism** — 𝔰𝔲(3) emerges by two irreducible steps: algebraic closure
selects 𝔰𝔩(3,ℝ); spinorial chirality completes it to 𝔰𝔲(3). Neither works alone. **The second step
imports unitarity as a physical input.**
**Colour charge gap** — the remaining obstruction: passing from split-real 𝔰𝔩(3,ℝ) to compact
𝔰𝔲(3). Reduced to a single complexification step. **Open.**
**SU(3)-not-in-O(4) theorem** — dim 𝔰𝔲(3) = 8 > 6 and 𝔰𝔲(3) is simple ⟹ only the zero
homomorphism; the strong force cannot arise from the O(4) fiber alone.
**Colour charges as torsion Cartan eigenvalues** — the three QCD colours are eigenvalues of
H₁ = diag(1,−1,0,0) and H₂ = diag(0,1,−1,0), both in the torsion sector; the colourless "White"
state at the origin is the lepton.
**T_{B−L} generator** — diag(1/3, 1/3, 1/3, −1); the minimal Pati–Salam embedding whose bracket
structure produces the framework's native dimensionless ratios.
**Torsion coupling hierarchy (0:1:4)** — all 15 generators classified by ‖[T_{B−L}, X]‖²: 9 Tier-0
(zero coupling), 6 Tier-2 colour-lepton (coupling exactly 32/9). ⚠️ Paper A's body says **two** tiers
while the abstract advertises 0:1:4; see the inconsistency list.
**Active sector** — the nonzero-eigenvalue subspace of ad_T; for T_{B−L} the 6-dim quark-lepton
mixing space split ±4/3, vs a 9-dim kernel.
**Vacuum energy cancellation (Palatini pairing)** — Σ_X ‖[T_{B−L},X]‖²·K(X,X) cancels exactly: each
Tier-2 antisymmetric generator (K = −16) pairs with a symmetric partner (K = +16). **Not
supersymmetry — Form–Function pairing.** Reduces the CC problem from 10¹²¹ to ~10⁵⁵ orders.
**Koide projection** — cos² of the angle between the symmetric channel of the 3rd-order holonomy and
the B−L direction = exactly 2/3 (to 1e-16); normalised through K(T_BL,T_BL) = 32/3 it fixes
λ = 2√3/27 and m_H = 124.7 GeV. Labelled **"partial derivation"** (0.85% residual).
**Koide–Cabibbo relation** — tan θ₀ = λ_W = sin θ_Cabibbo → 12.76° vs 12.73°; RG-invariant at 1 loop.
**Cabibbo chain** — √(m_d/m_s) ≈ λ_W = sin θ_C = tan θ₀^Koide: one bracket projection seen three ways.
**Geometric see-saw** — the RH neutrino couples only through torsion; m_D = m_e²/(3m_τ) ≈ 49 eV,
m_ν × M_R ≈ 2400 eV² ⇒ a falsifiable **49 keV sterile neutrino** with an X-ray line at 24.5 keV.
**(The prediction is the mass and line energy, not the DM abundance.)**
**Self-pruning of the bi-doublet Higgs sector** — three no-fit filters: Phase 50 (α₂ forbidden by rep
theory), Phase 51 (β_c ≠ 0 forces tan β = ±1), Phase 52 (equal VEVs force V_CKM = 𝟙).
**Branch A / Branch B** — A = minimal PS bi-doublet, 6 irreducible inputs after self-pruning (vs SM
19+); B extends with Σ ~ (15,1,1), reopening the exclusions at the cost of a parameter.
**Three generations from Jacobi truncation** — the Jacobi identity closes the BCH algebra at exactly
order 3 (‖Jacobi‖ = 0 exact); each BCH order generates one generation ⟹ N_gen = 3, no fourth.
**Barbero–Immirzi from information balance** — ΔI = 0 at a horizon gives Σ_j (2j+1)e^{−2πγ√(j(j+1))}
= 1, solved by γ = 0.274 (Meissner). The DL value 0.2375 requires SU(2)_k Chern–Simons counting —
**open**.
**tan β gauge-protected flat direction** — tan β *cannot* be fixed perturbatively in the minimal
sector. **"This is NOT 'we couldn't fix it.'"**
**Strong CP θ_QCD = 0** — vanishes exactly because [[f,g],[f,g]] ≡ 0 and all mass matrices are built
from real 𝔰𝔩(4,ℝ) generators; no axion required.
**Gravitational ACS (Ashtekar pair)** — Form = densitised triad Ẽ, Function = Ashtekar connection
A = Γ + γK; the three coupling orders *are* the three LQG constraints.
**Wheeler–DeWitt as ACS quantum attractor** — on a 3-node spin network under Lindblad evolution the
steady state concentrates in ker(Ĥ) (⟨H⟩ = 3e-6, kernel weight 0.507); emergent time = ΔI symmetry
breaking.
**Ricci flow as ACS dynamics** — ∂g/∂t = −2R_μν read as the metric reducing 2nd-order information
asymmetry; verified by 41× curvature-variance reduction.
**Pythagorean lattice ⟨2,3⟩** — the multiplicative subgroup of ℚ^× generated by 2 and 3. Every native
dimensionless ratio of the minimal PS bracket algebra lies in it; SU(5)/SO(10) introduce the prime 5.
**Killing-orthogonality theorem** — tr([X,Y]X) = 0 = tr([X,Y]Y) for any matrix Lie algebra.
**Algebraic non-traversability** — π_X([X,Y]) ≡ 0: no information in a bracket output traverses back
to an input by inner-product reconstruction. Offered as ER=EPR non-traversability from bracket
algebra alone, **with no bulk geometry**.
**Three-class spectral taxonomy** — adjoint flows exp(t·ad_X) are elliptic / hyperbolic / parabolic
via Jordan–Chevalley. Corrective role: ad³ = (16/9)ad is *hyperbolic Cayley–Hamilton saturation*,
not a geometric 2π inversion.
**Grading selection theorem (N2)** — minimising S̃_g[P] = Tr(σ_P·g(ad_T)) is attained at
cluster-coherent partitions and reduces to weighted max-cut. Holds for classical types A, B, C, D;
**fails for G₂** (proved counterexample).
**(3,1) internal grading selection** — for T_{B−L}, the selected grading of the *internal* carrier
space (3 quark colours + 1 lepton) has (3,1) shape. **Explicitly not a derivation of Lorentzian
spacetime signature.**
**Coleman–Mandula bridging mechanisms** — the three routes that could connect the internal (3,1)
grading to spacetime signature: soldering via the Palatini tetrad, a pre-geometric regime, or
explicit CM evasion. **None established. Stating this is never optional.**
**Confinement as ACS attractor** — the only long-distance-observable states sit at ΔI = 0 in the
colour sector.
**Tensegrity-gauge correspondence** — zero eigenvalues of a tensegrity network's rigidity matrix
align with the gauge redundancies of lattice gauge theory on the same graph. Icosahedral tensegrity:
exactly 6 zero modes.
**Banach–Tarski as geometric ACS** — two free-group rotation generators as Form and Function;
non-commutativity is the 2nd-order bracket; the paradoxical second ball is emergent volume.
*(Analogy, no computation.)*

---

## C. Spectral / Riemann (Papers B, B′, methodology)

**Prime-zero ACS** — Form = the primes (multiplicative skeleton of ℤ), Function = the Riemann zeros,
coupled by the explicit formula. RH becomes the statement that this ACS is information-balanced.
**Riemann spectral function F_N(x)** — Σ A_k φ_k(x), A_k = 1/(¼+γ_k²). Its stationarity is the ACS
reformulation of the critical-line condition. ⚠️ Three incompatible φ_k conventions exist in Paper B.
**Stationarity measure S(N,X)** — Var_{x∈[X,2X]}[F_N] / Σ|A_k|². Uniformly stationary if
sup_{X>2} S(N,X) < ∞ for all N.
**T4 / T4′** — T4: RH ⟹ stationarity (proved by AM–GM). T4′: the claimed **equivalence**; the
converse is conditional on an unproved minimum-gap bound δ_N > 0.
**Fourier-dual asymmetric codependent partners** — primes and zeros exchange information through
Fourier transformation (the explicit formula), **never through frequency matching**.
**Tartini tones** — combination frequencies γ_k ± γ_j generated *within* the zero spectrum by
non-commuting (Wronskian) mode brackets. **Intra-spectral (zero-zero) only — explicitly not
prime-zero resonances.**
**Intra-species resonance vs cross-species cancellation** — combination tones arise only within one
spectrum; the prime-zero coupling is a **cancellation identity**. An ACS "closes" across the
Form/Function boundary rather than resonating across it. **RH = balance, not tuning.**
**Wronskian–Lie identification** — W[f,g] = f′g − g′f is a genuine Lie bracket on the zero modes but
**fails Leibniz** by exactly −fgh′, so it is *not* a Poisson bracket. Hamiltonian/plasma readings
are explicitly disallowed.
**Elastodynamic tensor mapping** — a *defined* (not derived) map of the explicit formula onto a
symmetric 2×2 stress tensor: T₁₁ = x (growth), T₁₂ = −Σ Re(x^ρ/ρ) (zero oscillation).
**Unique center manifold** — σ = ½ is the only value at which the tensor flow is purely rotational;
any other σ adds radial drift ∝ (σ − ½).
**Spectral stability ratio ρ_spec** — exactly 0 when all zeros are on the critical line, divergent
in X otherwise.
**Tensegrity atom** — a discrete Form–Function system with stability ratio ρ = αγ/(βκ), stable when
ρ < 1. *(The glossary flags: Paper B attributes this definition to Paper A, which does not contain it.)*
**Resolvent susceptibility χ(ω)** — Σ 1/(ω − γ_ρ) = Tr[(ωI − H)⁻¹]; the rigorous replacement for the
*falsified* plasma-Hamiltonian framing.
**Shuffle knife** — replace a spectrum by its own spacings randomly permuted and re-accumulated, then
ask whether each witness's value survives. Unchanged = reading the universality class (**form**);
collapsed = reading the object (**function**).
**Marginal-matched surrogate** — same one-point spacing distribution by construction; all
object-specific correlations of order ≥2 destroyed.
**Spectral witness** — a scalar functional of a spectrum evaluated on the object and on surrogates.
**True influence z(W)** — |W_real − mean(W_surrogate)| / σ(W_surrogate).
**Form vs Function witnesses** — on 10⁵ zeros with 60 surrogates: arithmetic (~11,500σ) and lag-1
(~97σ) are FUNCTION; spacing, counting, Wigner-shape are FORM (0.4–1.0σ).
**Arithmetic prime-resonance witness** — Σ_{p≤29}⟨cos(γ log p)⟩² on the *actual* (not unfolded)
heights; in content, the explicit-formula coupling. The dominant FUNCTION witness.
**Amplification with N** — the decisive check: a genuine signal *sharpens* as N grows (3,030 →
11,497); an artifact averages down.
**Form-bundle** — the distributional witnesses are *not* independent confirmations: effective rank
~4, **the same on real zeros as on surrogates**.
**Apparatus band** — the ~0.08 disagreement between two legitimate GUE reference constructions. A
candidate signal inside the band is *not claimed* — which is why lag-1 is not claimed beyond-GUE
despite being formally FUNCTION.
**Reference frame ν** — the reference ensemble a witness is scored against; identified with the
dμ/dν slot of the BCH–TE lemma. *"That choice is the perspective."*
**Frame ladder** — Poisson < GUE-marginal < GUE-full bulk < zeta itself (terminal).
**Monotone staircase** — under frame refinement z can only decrease ⟹ each witness has a single
**threshold frame**, and witnesses are totally ordered by the depth of structure they read.
**Reactional vs response-driven definition** — a *reactional* definition names a thing by the
reaction it emits; a *response-driven* one by what it responds to. Defined by outputs, distinct
responders are indistinguishable; defined by inputs, they separate. The shuffle knife is the
operator converting one frame into the other.
**Prime carrier** — the two-point object the prime-resonance functional is a functional of,
identified *positively* as the value-space pair correlation of the **positions**: ρ₂ reconstruction
recovers 100.0%; spacing-preserving surrogates recover ~7%.
**Value-space pair correlation ρ₂** — from differences of *actual positions*. Distinct from the
two-point correlation of the *spacing sequence*.
**Position form factor K(f)** — |Σ_j e^{−ifγ_j}|²/N, the single-realisation form factor. Peaks only
at f = log n for n a prime power, heights tracking (Λ(n)/√n)² at r = 0.9975.
**Retraction: "the primes are not a two-point statistic"** — a formally retracted internal claim: it
had measured the *wrong* two-point object.
**Spacing floor / shuffle floor** — residual prime-resonance power after random permutation; the null
level. Baseline-to-floor separation grows 18× → 474×.
**Measurability wall** — the machine is universal, but for objects with too few resolved zeros the
form factor cannot resolve arithmetic peaks at reachable height.
**Hilbert–Pólya constraint specification (C1–C9)** — an *executable* spec any HP spectrum must pass.
**GUE-necessary-but-not-sufficient** — a GUE spectrum rescaled to the Riemann range is
indistinguishable on pair correlation but fails Fourier-dual prime alignment by ~40×.
**Hilbert–Pólya wall** — any H with spectrum {γ} must carry real orbit amplitudes
(|Im W|/|Re W| = 0.0001 ⟹ T-even, β = 1) **and** GUE repulsion (β = 2.00 ⟹ T-broken) — two
constraints pulling to opposite symmetry classes.
**Wall resolution class** — the two coexist precisely in families with an **anti-commuting
antiunitary** symmetry CH*C⁻¹ = −H (C² = −1). Among GOE/GUE/chiral, only **chiral** passes both.
*"The class is pinned; the primes are not yet in it."*
**Hypercone projection (spectral sense)** — the level-repulsion exponent β is a **dimension counter**,
**β = codim − 1**; the zeros' measured β = 2.019 selects the codim-3 chirality class. ⚠️ Distinct
from the Klein-foam "hypercone."
**Three-number diagnostic** — a structure-group-agnostic test of a transport holonomy D returning
‖D − I‖ (path-dependent?), ‖D − (Tr D/n)I‖ (central?), and mean‖[D,H]‖ (commuting?).
Probe-basis-invariant by Schur.
**Transport obstruction** — D = U₁U₂⁻¹ from two refinement-path orderings. Abelian obstructions are
central scalars; non-abelian ones are conjugacy classes. 𝔰𝔩(4,ℝ) forces non-abelian.
**Mixed obstruction** — decomposed along SU(4) → SU(3)_C × U(1)_{B−L}, the obstruction is *mixed*:
non-abelian on SU(3)_C and the coset, abelian central phase on U(1)_{B−L}.
**Central number** — the projection of the log-holonomy onto B−L; forced (T2) to equal the quark
B−L charge 1/3, because it is an eigenvalue ratio and the path scale cancels.
**Charge/coupling epistemic split** — *charge*-type observables (eigenvalues, charges, ratios) are
forced exactly because they are scale-free; *coupling*-type observables (magnitudes) carry an
irreducible ~1% canonical-normalisation residual. **"The organising result" of B′.**
**Harmonic ladder / repetition tower** — prime periodic orbits appear with r-fold repetitions at the
trace-formula amplitude p^{−k/2}; confirmed 3 rungs deep.
**Functional-equation involution ι and character twist T** — ι: χ → χ̄ from s ↔ 1−s; T paints χ(p)^k
on rung k.
**Commutator order parameter / parity law** — ‖[ι,T]‖_k = 0 ⟺ order(χ) | 2k. *"The self-dual locus
is the commuting locus."*
**Prime face / zero face** — the Euler product (multiplicative, *unique* structure — a factorisation
is a point) vs the Hadamard product (additive, *cardinal* — the size of a cloud), joined by the
explicit formula.
**S(T) counting fluctuation** — N(T) − ⟨N(T)⟩; the framework's claim is that the primes own it
entirely.
**No selection regime** — no arithmetic perturbation of a self-adjoint GUE operator moves spacing
statistics toward the zeros at *any* strength: weak is cosmetic, strong breaks toward Poisson.
**xp as smooth skeleton** — Berry–Keating xp reproduces the smooth staircase to <0.2% but has
continuous spectrum and does not encode S(T). *"xp alone is the operator"* is killed; *"xp as the
smooth skeleton"* survives.
**Kernel Law / Compression Law (N3)** — dim ker(P_m) = φ(m) exactly, kernel = the source sector; and
r_eff ~ φ(m)^1.6 while algebraic rank grows as φ(m)(φ(m)−1). **Explicitly pre-asymptotic.**
**T_min = (2πe)^d/q** — the claimed conditional-uniformity height floor. **T4 in its scaling**: at
d=2 the true floor is 2πe·q^{−1/d} and the framework formula overshoots ~8.5×. The d=1, q=1 value
2πe ≈ 17.08 survives as a genuine analytic invariant.
**Degenerate-case trap** — the named pattern: a claim can pass indefinitely on the degenerate slice
where a wrong dependence coincides with the right one.
**4/3 coincidence** — β = 4/3 vs α(d) = 1 + 1/d at d = 3. **T4**: fails normalisation robustness and
collapses to the identity family n = d + 1.
**Section 9 chain** — the proposed "spectral gap → clustering → cone-sharpness" dependency. **Not
supported** (0/12 exhaustive); "as general theorem: not claimed."
**Resolution unit δ / scaled invariance** — the count of representable points is a coordinate on
(interval × unit), invariant under joint rescaling. "Infinity" and "zero" are two ends of one
staircase in δ. **Explicitly scoped: Cantor is untouched.**

---

## D. Geometry, topology, number representation (FF06 thread)

**Flattening / reversible flattening** — π: R → s from a structured relational object to a scalar.
Reversible iff the producing operation is an **injective homomorphism into a pre-specified,
independently-meaningful structure**.
**Density vs identity** — a homomorphism preserves how parts combine (density); injectivity is the
additional condition that distinct objects have distinct images (identity).
**Convolution seam (the seam)** — the additive/multiplicative boundary, characterised as convolution
— the operation that adds indices while multiplying values. **Crossable by generating functions for
aggregate density; uncrossable for individual identity: convolution yields *how many*, never *which
one*.**
**Unique vs cardinal structure** — the multiplicative side carries *unique* structure (a single
canonical address, by FTA); the additive side carries *cardinal* structure (a cloud with no address,
but an exact count — p(n)). **Addition is not structureless; its structure is the count.**
**p-adic gradient (Wall 6)** — the seam is not a binary void: v_p(a+b) ≥ min(v_p(a), v_p(b)) is
*tight* whenever the valuations differ (~50% of cases). *"The only false wall that made the picture
richer."*
**The 2×2 square / Cantor corner** — classify by (homomorphic?, injective?): homo+inj = reversible;
homo+non-inj = **seam**; non-homo+inj = **Cantor corner** (identity kept, structure scrambled);
neither = noise. On the critical line, s → 1−s occupies the Cantor corner.
**"The critical line is not one seam"** — three distinct maps live there: the reflection is a Cantor
corner; the prime-zero correspondence is granularity-dependent; the genuine convolution seam
(Euler-product convergence edge) sits at **Re = 1, not ½**.
**Cantor pairing counterexample** — π(a,b) = (a+b)(a+b+1)/2 + b is a perfectly reversible bijection
yet not a homomorphism — falsifying the *converse* of the criterion.
**Vacuity guard** — the target structure must be **pre-specified and independently meaningful**;
"injective homomorphism into *some* structure" is empty, since any bijection is an isomorphism onto
the transported operation.
**Three contractions** — biconditional "iff" (falsified) → forward but "into some structure"
(vacuous) → forward, injective, pre-specified. *"The contraction is not the price of the result. The
contraction IS the result."*
**Shape (box)** — {pᵢ : eᵢ} from prime sides to exponent dimensions, volume ∏pᵢ^{eᵢ}. Multiply =
merge, divisibility = containment, gcd/lcm = common/enclosing box, primality = atomic box.
**Geometry Engine** — a 91-line reference implementation computing multiplicative operations from box
geometry without forming the integer value. 12/12 operations verified exact.
**Conservation principle** — an operation on shapes is admissible iff it conserves volume.
**add_exit / GEOMETRY_EXIT** — the named mechanism for addition (which has no shape): compute the
value, refactor, re-enter, emitting a flag. *"Addition is never hidden inside a geometric costume."*
**Additive depth** — the minimal number of primes summing to n: always 1, 2, or 3.
**Relational Representation Principle** — if a computation produces a scalar that is a lossy
projection of a structured object, compute on the object. **Some scalars are shadows.**
**Boundary law** — relational representation beats scalar abstraction iff (i) an exact underlying
relation exists, (ii) it is a product/ratio/non-transitive graph rather than a sum, and (iii) the
scalar projection breaks or the question is exact.
**Dominance engine / non-transitive impossibility** — for cyclic pairwise majority, every total order
contradicts at least one verdict; the relation carries information no scalar can hold.
**Order-dependence / structure-retention axes** — corrected law: non-commutativity measures
*retained order-dependent* structure only; commutative operations (gcd, lcm) can still retain full
order-independent structure. **Two independent axes.**

---

## E. Condensate / particle model (Flag Condensate, Möbius screw)

**Flag Condensate** — the postulated primordial two-component complex scalar Φ = (φ + iπ)/√2 whose
real and imaginary parts are in quadrature; the substrate from which structure is read. Also names
the research programme.
**Klein foam** — reality as a nested, scale-variant dynamic network of self-intersecting
Klein-bottle **hypercones** embedded in the flag condensate.
**Hypercone (Klein-foam sense)** — a self-intersecting Klein-bottle vortex; a Möbius-twisted coring
screw. **Distinct from the spectral "hypercone projection."**
**Monad** — the foam treated as a single indivisible self-reflecting whole (Leibniz), with every
sub-structure a localised reflection.
**Throat** — Nuclear: the colour-confining interior r < R with AdS-like warped metric. Electron: the
high-torsion region of the framed unknot, closest approach ρ_min = R − a. Foam: the hypercone neck.
**Throat sieve** — the set of active cells in a voxel discretisation of the foam.
**Throat weight** — w(r) = √g_rr = R/r, the radial measure factor from the confining metric.
**Phase slip / phase-slip channel** — the geometric defect across the throat linking interior
standing structure to exterior travelling structure; formally the Bogoliubov channel
|β/α|² = e^{−2W}.
**Spectral bifurcation** — the transition from a quadrature-locked confined standing wave to an
in-phase outgoing travelling wave. **The programme's replacement for "the particle tunnels out."**
**Tartini tone (nuclear sense)** — the difference-frequency wave packet produced by nonlinear mode
mixing in the throat; what is conventionally called the emitted alpha particle.
**Slag** — the residual condensate energy trapped in the Casimir cavity of the twisted walls after a
phase slip, **identified with rest mass**: m = δ·E_cond/c², δ ≈ e^{−2W}.
**Standing-wave phase lock** — the interior state: φ and π share a spatial profile but are strictly
quadrature-locked in time. *"No localized physical particle exists within the interior — only a
stationary saturation node."*
**Gamow phase defect W** — W = ∫_R^b κ(r)dr; transmission T = e^{−2W}.
**P_alpha / P_model** — P_α is the standing-wave mode-overlap fraction, **extracted from
Geiger–Nuttall intercepts, not predicted**. P_model is a geometric proxy.
**Spectroscopic factor S** — a multiplicative scale. Variants: global S★, per-isotope S_i
(tautological, diagnostic only), and predictive parametric S(A,Z).
**Four-domain phase-defect unification** — nuclear decay, Hawking radiation, electroweak sphalerons,
and superconducting fluxon nucleation as four lanes of one Bogoliubov transfer-matrix form.
*"Absolute physical identity beyond shared transfer-matrix form is not claimed."*
**Möbius-screw electron / framed unknot** — the electron as a closed loop carrying two full twists of
framing — a (2,1)-torus embedding with self-linking 2. **The knot type is trivial; the physical
content is attributed to framing, not knotting.**
**Self-linking Sl (Călugăreanu)** — Sl = Tw + Wr; under the natural torus framing of a (p,q)-curve,
Sl = p·q = 2. **Only |Sl| and its parity are invariant** — Tw and Wr individually are not.
**Framing Transformer** — the instrument evaluating the chain γ → U → Sl → F:S¹→SO(3) → q:S¹→SU(2),
to locate exactly where spin-½ enters. **It killed the Sl=2 ↔ g=2 identification while confirming
the geometry.**
**Spinorial holonomy σ** — σ = q(4π)/q(0) ∈ {+1, −1}, deciding whether the SU(2) lift closes after
one circuit. σ = −1 ⟹ the nontrivial class of π₁(SO(3)) = ℤ/2.
**Parity law** — σ = (−1)^{p+q} = (−1)^{Sl+1}: **the spin-relevant content of Sl is one parity bit.**
**Sl = 2 ↔ g = 2 identification** — **T4 / KILLED.** Sl = 2 and Sl = 0 lie in the same π₁(SO(3))
class, so the value 2 carries no spin information that 0 does not.
**No-go for geometric g (g = 1)** — for any closed curve with uniform charge-to-mass ratio, μ and
⟨L⟩ are proportional to the same vector area ⟹ **g = 1 exactly**, independent of winding, framing,
twist, or throat. Getting g ≠ 1 requires **decoupling charge and mass distributions**.
**Laplace-eigenspace relocation of spin-½** — the four quaternion coordinates on S³ = SU(2) are
exactly the first nonzero Laplace–Beltrami eigenspace (Δx_i = −3x_i, degeneracy 4), which under
SU(2)_L × SU(2)_R is the (½,½) rep. Spin enters through *representation theory*.
**Capacitance model of α** — assign e/2 per Möbius sheet and match electrostatic self-energy to rest
energy: α⁻¹ = πε₀R/C returns ~137.036 in the annulus baseline. **Deflated**: an output of a tuned
cutoff (a/R ~ 2e-118); moderate aspect ratios give α⁻¹ = O(1).
**Density engine** — the shape of the universe as an inexhaustible geometric constraint source;
geometry routes, compresses, and re-releases phase structure along lanes. **"Density" = structure per
geometric lane on a *stated* manifold** — explicitly not literal infinite energy density in SI units.
**Polymorphic quantum flags / Lisp-deterministic** — the programme's correction to "every
plausibility in parallel" MWI language: one Φ substrate supporting many phase/mode configurations
after spectral bifurcation — **mode polymorphism, not world multiplication**. Counterfactuals read as
*opcodes on a fixed substrate*.
**Scale ladder (micro/meso/macro)** — one phase-defect template recurring: micro (framed unknot),
meso (nuclear colour throat), macro (Schwarzschild horizon).
**Shuman Resonance** — the postulated fundamental torsional standing wave of the Klein foam; a
geometric analogue of Schumann resonances. **The spelling deliberately preserves the programme
name — it is footnoted as intentional, not a typo.**
**Sovereign framing / RC1 claim discipline** — RC1 separates (1) **model claims** (finite statements
on stated manifolds with cited numerics), (2) **structural parallels** (same template, no identity
claim), (3) **metaphor / sovereign framing** (narrative energy, no physics proof).

---

## F. Epistemic / methodology / governance

**Adversarial compression** — CONJECTURE → EXPLICIT COMPUTATION → RESULT. A survivor compresses to a
theorem; a failure is recorded as a **first-class negative** with the killing computation and failure
mechanism; a partial result becomes an observation with a scope boundary. **Overclaiming is the
primary failure mode.**
**Tier map (T1–T4)** — per-claim, never promoted: T1 machine-verified · T2 proved in paper ·
T3 numerically verified, not theorem-level · T4 explicitly falsified (recorded, not hidden). *The
most-aliased term in the glossary (~35 aliases).*
**Engine kill-criterion (tomographic invariance)** — a quantity is a **REFRACTION** if its value
moves under a legitimate change of instrument, an **INVARIANT (candidate)** if it does not. Applied
numerically (→T1) or structurally (→T2). *"Tier honestly; never let (b) wear (a)'s clothes."*
**Refraction** — a quantity whose value moves under legitimate instrument change, therefore not
fundamental. Precedent kills: g₄ = 4/3, γ = 0.274, λ_φ = 0.1283 — all T1 refractions while the
corresponding *relations* survived.
**SPLIT (ledger status)** — the verdict for a claim that divides into an invariant part and a
refraction part. Status tags: QUEUED / IN-PROGRESS / KILLED / SURVIVED / SPLIT / BLOCKED.
**Elimination Ledger / strip-mine discipline** — an append-only catalogue of falsifications,
refractions, and survivals; kill targets ranked by expected-space-collapsed per unit cost, weighted
toward the framework's *own* load-bearing claims. *"One does not prove the gold is present; one
removes everything that is not gold."* Killed dead-ends are "empty tunnels mapped."
**Tomographic invariance engine** — the instrument of the elimination campaign. **Calibrated against
known invariants and refractions first**, with negative controls and decoy targets, "so the engine
could not become its own refraction."
**Pre-registration and the no-tuning rule** — thresholds, kill conditions, and operational
definitions are fixed *before* seeing results.
**Measured, never projected** — a complexity argument or extrapolation is not a measurement.
**False wall** — a **falsified interpretation of a true computation**, distinct from a falsified
conjecture. Six are catalogued.
**Sycophantic mode** — guarded failure mode #1: a result feels validated because a collaborator —
human or machine — agreed, rather than because it was tested.
**False-fit mode** — guarded failure mode #2: a structural resemblance mistaken for an operational
identity.
**Asymmetric instrument** — the division of language models into non-interchangeable roles: an
idea-generator (expansive, fluent, **untrusted by default**), a coder/honest-instrument, and
independent critics. *"A fluent proposal is the most dangerous kind."*
**Adversarial gauntlet / grades** — HIT (relation wins) / SPLIT (multiplicative part wins, additive
is the wall) / DOWNGRADED (existing method already wins) / FALSE FIT (no hidden relation; the scalar
is the datum).
**Scope boundary / scope honesty standards** — an explicit statement of what a result DOES and DOES
NOT claim, required for every result. Five must always be stated: Coleman–Mandula rule,
exceptional-algebra boundary, Barbero–Immirzi gap, neutrino tension, tan β protection.
**Fresh-eyes note** — a *dated* corrective annotation added on re-review so the bundle does not
overstate a result.
**StrickenBy** — an annotation marking a superseded ledger entry with correction ID and date, keeping
the audit trail visible.
**First-class negative** — reporting negative or unresolved measurements with the same prominence as
positive ones. *"Reported as a negative, not spun."*
**Grade hierarchy (AI stack)** — **TheoremGrade** (exact SymPy, closure < 1e-14, exhaustive Jacobi —
citable, admitted to the permanent constraint set) · **VerificationGrade** (mpmath, < 1e-10) ·
**ExploratoryGrade** (NumPy, < 1e-6, advisory only, never admitted).
**Three-tier verification model** — Tier 0 type-level, Tier 1 unit, Tier 2 theorem verification via
the 76-script suite as integration tests. **Distinct from the T1–T4 theorem labels.**
**Canonical seed 20260423** — the fixed seed across all FF06 spectral suites.
**RC1** — Release Candidate 1, the bundle's first consolidated claim-discipline pass.
**SIP License v1.1** — Sovereign Integrity Protocol License, under which every paper declares itself
"co-governed and enforced."
**ΔI ≡ c-function (FF06Σ Link 3)** — the killed conjecture that ΔI *is* the RG c-function. Every
reading closed. **"No reading is both novel and true."**
**Universal-2π overclaim (retracted)** — exp(2π·ad_{T_{B−L}}) has spectral norm ~4348, not 1.
Retained as a boundary marker.
**Predictions on record** — 49 keV sterile neutrino · θ_QCD = 0 exactly · torsion hierarchy 0:1:4 ·
Higgs mass 124.72 GeV · the critical line as the unique center manifold.
**Bracket Engine / Closure Validator / ΔI Monitor / DAG journal** — the AI stack's four components:
the single generative primitive [F,Φ] truncated at BCH order 3; the validator enforcing D < ε; the
convergence detector halting when |ΔI| < ε over 8 steps; and the append-only content-addressed
Merkle DAG.
**Kernel invariant** — three interchangeable arithmetic backends (SymPy exact, mpmath, NumPy fp64)
must produce **bit-identical** results on their common domain.
**Receipt / Reproducibility envelope** — a cryptographic record sufficient for independent replay;
re-execution must produce byte-identical output or the receipt is invalidated.
**Coherence obstruction tensor / scheme dispersion metric / orbit sheaf / de-sublimation** — the
discrete-geometry formalism's vocabulary: exact conjugacy failure between discretisation schemes;
variance over measurement orderings (**not** geometric curvature); the ensemble of all measurement
histories; and the recasting of curvature/RG-flow/holonomy as secondary statistics rather than
intrinsic geometric objects.
