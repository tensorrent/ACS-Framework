> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# The ACS Corpus — Variables, Invariables, Tests, Results, Failures

*A map of every paper in the folder. Sourced from the extracted texts (FF06a/b/c via embedded page-text; N3 native; FF06b'/e/f from the build). Numbers are as written in the documents.*

---

## 1. The corpus at a glance

| ID | Title | Domain | Pages | Status |
|----|-------|--------|------:|--------|
| FF06a | Colour from Gravity: SU(3) as a Closure Attractor in the Palatini Bracket | Gauge / gravity | 44 | Core |
| FF06b | The Riemann Spectral ACS: Stationarity as a Characterisation of the Critical Line | Number theory | 15 | Core |
| FF06c | Holographic Spectral Inversion and Invariant Kinematic Attractors | QFT / geometry | 14 | Core |
| FF06-N3 | The Prime-Gap Dynamical Dynamical Dynamical Dynamical Dynamical Transition Operators over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembles on (Z/mZ)* | Number theory / operator | 8 | Note |
| FF06b' | Spectral Witness Survival and the Character of the Transport Obstruction | Number theory + bridge | 13 | New |
| FF06e | Spectral Rigidity and Shuffled Spacing Discriminant | Methodology + zeros | 4 | New |
| FF06f | Density, Positions, Spacings (three-layer decomposition) | Number theory | 4 | New |
| FF06g | Form/Function Relativity: The Reference Frame Is the Perspective | Methodology + zeros | 4 | New |
| AISO | Full-Stack Design Invariables + TENT v10 | Engineering / trust | — | Living |

---

## 2. THE INVARIABLES (constant across the whole corpus)

| # | Invariable | Where it holds | Form in the text |
|---|------------|----------------|------------------|
| INV-1 | **The asymmetry ΔI is the primitive** | Every paper | Net transfer entropy between two mutually-constraining fields; sign of ΔI is the generator |
| INV-2 | **ΔI's 2nd-order Taylor coefficient = the Lie bracket [f,g]** | FF06a, carried by all | The BCH–transfer-entropy morphism |
| INV-3 | **Form / Function ontology** | Every paper (Def 2.4 in FF06a) | Form carries structure/admissible states; Function acts within them; ΔI>0 Form drives Function, ΔI<0 Function drives Form |
| INV-4 | **bracket(Function, Function) → Form; holonomy(bracket, Function) → irreducible Form** | FF06a, structural | The operator-type ladder |
| INV-5 | **Inversion arc: a system that solves a constraint becomes the constraint (ΔI flips sign)** | FF06c, echoed everywhere | "Holographic resolution principle" |
| INV-6 | **Tensegrity / nested codependence; self-similarity** | FF06b, FF06c, AISO | zero modes of rigidity matrix = gauge freedoms; Menger-sponge "each cell carries the whole" |
| INV-7 | **Adversarial compression + 4-tier honesty ledger** | Every paper | proven / numerically-verified / conjectured / falsified; negatives are first-class; scope stated |
| INV-8 | **"Right locally, wrong globally"** (glass-box) | FF06c + new papers | each lens valid in scope, over-reaching when universalised |

### Locked numerical invariants (derived, never refit)

| Quantity | Value | Mechanism | Paper |
|----------|-------|-----------|-------|
| g₄ = g_L = g_R | 4/3 | Palatini bracket (C₂ = 4/3) | FF06a |
| λ_φ (Higgs quartic) | 2√3/27 ≈ 0.1283 | Koide projection | FF06a |
| h̃/h (Yukawa ratio) | 2/3 | Koide ratio | FF06a |
| 2ρ₁ + ρ₂ | 16/9 | Palatini pairing | FF06a |
| γ (Barbero–Immirzi) | 0.274 | ACS information balance | FF06a |
| N_gen (generations) | 3 | Jacobi truncation at BCH order 3 | FF06a |
| θ_QCD | 0 exactly | prediction | FF06a |
| torsion coupling hierarchy | 0 : 1 : 4 | prediction | FF06a |
| K(T_BL, T_BL) | 32/3 | Killing form | FF06b' |
| central charge | 1/3 (= quark B−L) | Killing chain | FF06b' |
| m_H (from λ_φ chain) | 124.72 GeV | quartic → mass | FF06b' |

---

## 3. THE VARIABLES (what each paper lets move)

| Variable | Range / values | Notes |
|----------|----------------|-------|
| **Substrate the bracket is applied to** | gravity → primes → QFT → trust | The *only* thing that really changes paper-to-paper |
| ρ₁ (Higgs-triplet self-coupling) | (0, 8/9) | free |
| α₁ (portal coupling) | \|α₁\| < 0.81 | free |
| tan β (bi-doublet VEV ratio) | (0, ∞) | **gauge-protected flat direction** — cannot be fixed perturbatively |
| v_R (right-handed breaking scale) | unconstrained | sets proton decay / heavy boson masses |
| v (EW VEV) | 246.22 GeV | calibration (measured) |
| Free-parameter count | **4 free + 2 calibration = 6** | down from SM's 19+ |
| Claim status | proven / numerical / conjecture / falsified | moves between papers as results sharpen or die |

**The pattern:** framework = Form (constant); each domain = a Function realized within it. The corpus is itself a Form/Function object.

---

## 4. TESTS & NUMERICAL RESULTS (sourced)

| Test | Result | Scale | Tier | Paper |
|------|--------|-------|------|-------|
| sl(3,R) unique 8-dim closure | D < 10⁻¹⁴; >0 for all others | 50,000 random Gr(8,15) samples | 3 (numerical, not classification) | FF06a |
| sl(3,R) → su(3) chirality map | all 28 brackets close; skew-Hermitian | exact symbolic over Q[i] | 1 | FF06a |
| Jacobi closes BCH at order 3 | ‖Jacobi‖ = 0 | exact | 1 | FF06a |
| 8 electric + 8 hypercharges match SM | exact match | fermion_reps.py | 1 | FF06a |
| Full verification suite | 76 scripts | — | 1 | FF06a |
| RH ⇒ stationarity of F_N | confirmed (AM–GM) | 100 Odlyzko zeros | 2 | FF06b |
| Wronskian W[φₖ,φⱼ] ≠ 0 | all pairs non-vanishing | 1,225 pairs (first 50 zeros) | 1 | FF06b |
| Stress-tensor flow rotational at σ=½ | closed loops at ½, spiral else | numerical | 3 | FF06b |
| Rigidity-matrix zero modes = gauge freedoms | 6 = dim SO(3)+translations | exact | 2 | FF06c |
| Prime-gap operator kernel law | dim ker(P) = φ(m), no excess | all 14 moduli | 1 | N3 |
| Prime-gap operator data | — | 1.27×10⁶ primes up to 2×10⁷ | — | N3 |
| GUE pair correlation vs Montgomery | 0.988 (M=20k) → 0.99318 (M=60k) | full 10⁵ | 1 | FF06b' |
| Spacing L2: GUE vs Poisson | 2.64e-3 vs 4.18e-1 | full 10⁵ | 1 | FF06b' |
| Prime-dual line spectrum | 100% on-prime, no off-prime to height 0.015 | 80k block, ω<4.0 | 1 | FF06b' |
| §9 forced values (exact) | K=32/3, charge 1/3, m_H 124.72 | exact SymPy | 1/2 | FF06b' |
| Form/function split | arith 11,497σ, lag1 97σ FUNCTION; spacing/counting/shape 0.4–1.0σ FORM | full 10⁵, 60 seeds | 1 | FF06e |
| Effective rank of witness set | 4 on real AND shuffled | N=20k | 1 | FF06e |
| Form/function **relativity** (frame ladder) | repulsion/shape FUNC vs Poisson (44–50σ) → FORM vs GUE-marginal (0.1–0.2σ); rigidity FORM only vs GUE-full (1.6σ); arith FUNC in every frame (260–832σ) | N=4000, seed 20260423 | 1 | FF06g |
| Position reconstruction (primes) | corr 0.84, expl.var 0.71→0.82, vs random +122σ | full 10⁵, primes<3000 | 1 (verifies known RvM) | FF06f |
| Spacing arithmetic selection | none at any ε (cosmetic, then breaks) | M=400–500 | 1 | FF06f |

---

## 5. FAILURES & FALSIFICATIONS (first-class results)

| # | Claim | How it died | Mechanism | Paper |
|---|-------|-------------|-----------|-------|
| F-1 | ad³ = 2·ad for integers | requires λ = 1/√2 | eigenvalue constraint | framework |
| F-2 | Universal 2π inversion | sl(4) adjoint is hyperbolic | spectral classification | framework |
| F-3 | Wronskian is a Poisson bracket | Leibniz fails by −fgh′ | direct computation | FF06b |
| F-4 | IR lattice imprint on zeros | z-scores null vs PDG | statistical null | framework |
| F-5 | Intrinsic chirality | bias vanishes under covariant conjugation | invariance test | FF06a |
| F-6 | Route A (Killing form selects signature) | Cartan ≠ parity involution | classification | framework |
| F-7 | Route C (stability selects signature) | all signatures equal holonomy norms | computation | framework |
| F-8 | α₂ optional | forbidden by representation theory | T^A Φ = 0 | FF06a |
| F-9 | β_c explanatory | incompatible at tree level (equal-VEV no-go) | mass-matrix rank | FF06a |
| F-10 | Yukawa rescue of tan β | impossible: M_u−M_d = (h−h̃)(κ₁−κ₂) | identity | FF06a |
| F-11 | CW 6→5 parameter reduction | tan β gauge-protected flat direction | RG-invariance + multiplicative QCD + β-indep thresholds | FF06a |
| F-12 | "115-dim subalgebra" | turned out gl(12) on proper saturation | re-computation | framework |
| F-13 | N3 uniform-X conjecture | falsified in tested range | computation | N3 |
| F-14 (this session) | acid-to-water: assembly order selects outcome | greedy jams ~5.5 regardless of order | packing sim | session |
| F-15 (this session) | order-asymmetry as stable signed lever | sign oscillates / decays with N | scaling | session |
| F-16 (this session) | shell-commensuration of the asymmetry | crossings not at centered-hex numbers | computation | session |
| F-17 (this session) | sound & light = two octaves of one EM medium | 4/4 pre-registered tests fail (octave, speed, vacuum, v² law) | physics | session |
| F-18 (this session) | particle/wave = infinite Mandelbrot self-similarity | flower/snowflake are generative w/ characteristic scale | phyllotaxis test | session |
| F-19 (this session) | "same gap": central # residual = Higgs quartic residual | charge (θ cancels) vs coupling (magnitude) | computation | FF06b' |
| F-20 (this session) | quartic residual is high-scale boundary | λ crosses λ_ACS once near EW (~130–180 GeV), runs down | 1-loop RGE | FF06b'/test10 |
| F-21 (this session) | H = symmetrized duality | balanced involutions break GUE; only H-commuting one preserves | involution search | session |
| F-22 (this session) | H via arithmetic diagonal perturbation | cosmetic when weak, breaks GUE when strong; no selection regime | spacing test | FF06f |
| F-23 (this session) | lag-1 beyond-GUE | gap 0.050 inside 0.08 apparatus band (dual-reference) | M=3200 extrapolation | FF06b'/test09 |

---

## 6. OPEN PROBLEMS (live, unrefuted)

| # | Problem | Requires | Impact |
|---|---------|----------|--------|
| O-1 | Hilbert–Pólya operator H | different domain | **now characterized**: self-adjoint (GUE free), arithmetic in positions not spacings, self-duality generated-not-imposed → Berry–Keating route survives (FF06f) |
| O-2 | FeynRules/UFO export | engineering | LHC-testable predictions |
| O-3 | Action principle for S̃_g | variational theory | first-principles derivation |
| O-4 | L-functions extension | LMFDB zeros | Paper B generality |
| O-5 | Full SM from GL(4) fiber | conceptual breakthrough | complete derivation |
| O-6 | ER=EPR correspondence | conceptual breakthrough | holographic interpretation |
| O-7 | Barbero–Immirzi physical value 0.2375 | external Chern–Simons computation | γ from first principles (0.274 is unconstrained value) |
| O-8 | Neutrino tension | PS gauge-sector suppression | naive see-saw sin²2θ ≈ 4×10⁻⁶ vs X-ray < 10⁻¹⁰ |

---

## 7. PREDICTIONS ON RECORD (falsifiable)

| Prediction | Value | Paper |
|------------|-------|-------|
| Sterile neutrino | 49 keV | FF06a |
| θ_QCD | 0 exactly | FF06a |
| Torsion coupling hierarchy | 0 : 1 : 4 | FF06a |
| Higgs mass | 124.72 GeV (from λ_φ chain) | FF06b' |
| Critical line | unique center manifold (rotational flow at σ=½) | FF06b |

---

## 8. THE MAP IN ONE PICTURE

```
                         ΔI  (the asymmetry — INVARIABLE)
                          |
                 [f,g] = 2nd-order Taylor coeff  (INVARIABLE)
                          |
        ┌─────────────────┼─────────────────┬──────────────────┐
        │                 │                 │                  │
   Form/Function     Inversion arc     Tensegrity        Adversarial
   (INVARIABLE)      (INVARIABLE)      (INVARIABLE)      compression
        │                 │                 │            (INVARIABLE)
        └─────────────────┴─────────────────┴──────────────────┘
                          |
         applied to a VARIABLE substrate:
        ┌──────────┬──────────┬──────────┬──────────┐
     gravity     primes      QFT       trust      (each = a Function
     FF06a       FF06b/f    FF06c      AISO         realized in the
        │          │          │          │          constant Form)
   su(3) from   positions  inversion  routing/
   Palatini     = primes   = c/a-thm  qualia
   6 params    spacings              stack
   (4 free)    = GUE
```

**The single sentence:** every paper varies only the substrate; the asymmetry, the Form/Function cut, the inversion principle, the tensegrity geometry, and the honesty method are invariant. The corpus is one object (the framework, Form) pointed at many domains (each a Function).

---

*Map built from the project folder. Tier labels: 1 = machine-verified, 2 = proved in paper, 3 = numerically verified (not theorem), 4 = explicitly falsified. Failures F-14 through F-23 are from the current session; all others are from the manuscripts as written.*
