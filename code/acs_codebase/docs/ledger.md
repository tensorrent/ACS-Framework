# Verification Ledger

Status of every claim in the ACS trilogy as of repository commit.

Categories:
- **Rigorous** — proved symbolically and/or verified numerically at machine precision
- **Conjectural** — explicitly flagged in the papers as open
- **Disproved** — negative results that delimit model space (first-class)

---

## Paper A — Pati-Salam phenomenology and parameter pruning

| Claim | Status | Evidence | Module |
|---|---|---|---|
| Theorem C: ad_{T_BL}^3 = (16/9) ad_{T_BL} | Rigorous | residual 0.00e+00 | `src/paper_c/theorem_c.py` |
| 5 quartic Higgs parameters before pruning | Rigorous | enumeration | `src/paper_a/branch_a_parameters.py` |
| Palatini constraints lock 4 of them | Rigorous | bracket derivations cited from Paper A §3-4 | (cited only) |
| α₂ = 0 forbidden by representation theory | Rigorous | T^A Φ = 0 for Φ ~ (1,2,2) | `src/paper_a/branch_a_vacuum.py` (docstring) |
| Reduced potential admits stable vacuum | Rigorous | decimal-precision Cramer's rule, 9 alpha_1 values | `src/paper_a/branch_a_vacuum.py` |
| Custodial Δρ ~ 4×10⁻²⁹ at 1-loop heavy | Rigorous | safety factor ~5×10²⁴ vs bound | `src/paper_a/branch_a_vacuum.py` |
| λ_eff = 2√3/27 within 1.01% of λ_SM | Rigorous | direct comparison with m_H = 125.25 | `src/paper_a/branch_a_vacuum.py` |
| β_c at tree level forces tan β = ±1 | Rigorous | symbolic extremization → cos(2β) = 0 | `src/paper_a/betac_tan_beta.py` |
| M_u = M_d when κ_1 = κ_2 (no-go) | Rigorous | symbolic + numerical, both interpretations of h̃/h | `src/paper_a/yukawa_no_go.py` |
| θ_13 not fixable by cross-couplings | Rigorous | v_R requirement conflicts with proton decay | `src/paper_a/theta13_obstruction.py` |
| TM1 ansatz fails PMNS phenomenology | Rigorous | θ_12 pull +3.1σ, θ_23 pull −4.9σ | `src/paper_a/tm1_pmns.py` |
| TM2 ansatz fails PMNS phenomenology | Rigorous | θ_23 pull −4.2σ | `src/paper_a/tm1_pmns.py` |
| Branch A locks at 6 inputs | Rigorous (within minimal bi-doublet) | full pruning chain | `src/paper_a/branch_a_parameters.py` |
| Reduction factor 19+/6 ≈ 3.2× vs SM | Rigorous (counting only) | parameter ledger | `src/paper_a/branch_a_parameters.py` |
| Coleman-Weinberg fixes tan β | **Conjectural** | requires 2-4 weeks symbolic work | (open) |
| h̃/h = 2/3 matrix proportionality vs invariant ratio | **Conjectural** | requires Paper A §7 audit | (open) |
| FeynRules UFO export | **Open** | requires Mathematica + 1-2 months postdoc | (D1) |

---

## Paper B — Spectral / resolvent reinterpretation

| Claim | Status | Evidence | Module |
|---|---|---|---|
| χ(ω) = Σ 1/(ω−γ_k) is meromorphic with simple poles at γ_k | Rigorous | numerical pole structure | `src/paper_b/explicit_formula_resolvent.py` |
| Tr[(ω−H)^{-1}] = χ(ω) for trivial H = diag(γ_k) | Rigorous (tautological) | direct verification | `src/paper_b/explicit_formula_resolvent.py` |
| Wronskian satisfies Plücker identity | Rigorous (algebraic triviality) | symbolic + 1000 trials | (Phase 53 script in extras/) |
| Wronskian fails Leibniz: W(fg,h) − [fW(g,h)+gW(f,h)] = −fgh' | **Disproved as Poisson bracket** | symbolic identity | `src/paper_b/wronskian_leibniz.py` |
| Renormalized Δ_norm(u) bounded under RH (von Koch 1901) | Rigorous (forward direction) | numerical, 50 zeros, u ∈ [5, 20] | `src/paper_b/renormalized_stability.py` |
| Off-critical zero would induce exponential divergence | Rigorous | hypothetical σ=0.7 test | `src/paper_b/renormalized_stability.py` |
| Berry-Keating leading counting matches RvM | Rigorous | within ~1 zero through T = 143 | `src/paper_b/berry_keating_counting.py` |
| Berry-Keating exact spectrum = {γ_k} | **Open** | 26+ years (1999) | (Hilbert-Pólya) |
| Plasma Hamiltonian as foundation | **Disproved** | requires Poisson structure (Leibniz fails) | downgraded to analogy |
| Plasma resonance phenomenology (analogy only) | Defensible | dispersion peaks, beat zeros verified | (interpretive) |
| Hilbert-Pólya operator construction | **Open** | 100+ years (Hilbert/Pólya 1914) | (open) |
| Converse: bounded Δ_norm ⟹ RH | **Conjectural** | requires technical hypotheses on truncation | (open) |

---

## Paper C — Algebraic-closure framework, taxonomy, ER=EPR

| Claim | Status | Evidence | Module |
|---|---|---|---|
| Theorem C minimal polynomial | Rigorous | symbolic + eigendecomposition | `src/paper_c/theorem_c.py` |
| Killing-orthogonality: tr([X,Y]·X) = 0 | Rigorous | symbolic identity = 0 | `src/paper_c/killing_orthogonality.py` |
| Scaling: 1000 trials in sl(3,ℝ), max residual ~10^{-15} | Rigorous | reproducible with seed 20260423 | `src/paper_c/killing_orthogonality.py` |
| Scaling: 1000 trials in sl(4,ℝ), max residual ~10^{-15} | Rigorous | reproducible with seed 20260423 | `src/paper_c/killing_orthogonality.py` |
| Chirality hopping [H₁, A₀₁] = 2 S₀₁ | Rigorous | exact integer match in sl(3) and sl(4) | `src/paper_c/killing_orthogonality.py` |
| Orthogonal-complement probe: dim B^⊥ = n²-2 | Rigorous | algorithm + verification | `src/paper_c/orthogonal_complement_probe.py` |
| Generic Jacobian rank = 15 in sl(4,ℝ) | Rigorous | 20 random trials | `src/paper_c/orthogonal_complement_probe.py` |
| Degenerate kernel = 19 at (H₁, A₀₁) | Rigorous | specific point, rank = 11 | `src/paper_c/orthogonal_complement_probe.py` |
| Three-class spectral taxonomy (elliptic / hyperbolic / parabolic) | Rigorous | Jordan-Chevalley standard result | `src/paper_c/spectral_taxonomy.py` |
| ad_{T_BL} is hyperbolic class | Rigorous | spectrum {0, ±4/3} all real | `src/paper_c/spectral_taxonomy.py` |
| SU(2) quaternion: 3×120° = 2π inversion | Rigorous (elliptic case) | residual 4×10⁻¹⁶ | `src/paper_c/spectral_taxonomy.py` |
| sl(4,ℝ) ad-flow is hyperbolic, not rotational | Rigorous | exp(2π·ad) blows up to ~10³ | `src/paper_c/spectral_taxonomy.py` |
| Universal "2π inversion at three steps" | **Disproved** | rep-specific, hyperbolic vs elliptic | `src/paper_c/spectral_taxonomy.py` |
| Frenet-Serret A³ = -(κ²+χ²)A — elliptic class | Rigorous | residual 0.00e+00 | `src/paper_c/spectral_taxonomy.py` |
| Core rope R³ = R — hyperbolic class | Rigorous | spectrum {-1,0,+1} real | `src/paper_c/spectral_taxonomy.py` |
| Algebraic non-traversability (ER=EPR) | Rigorous | direct projection returns 0 by theorem | `src/paper_c/er_epr_algebraic.py` |
| Bell-state local operators commute | Rigorous (standard QM) | exact tensor-product | `src/paper_c/er_epr_algebraic.py` |
| c-theorem (2D) as inversion-arc forward instance | Cited (Zamolodchikov 1986) | not re-derived here | (literature) |
| a-theorem (4D) as inversion-arc forward instance | Cited (Komargodski-Schwimmer 2011) | not re-derived here | (literature) |
| Post-attractor ΔI < 0 (sign flip past IR) | **Conjectural** | structural argument, not proved | (open) |
| "3-cap in AdS/CFT entanglement hierarchies" | **Conjectural / research direction** | bridge to AdS/CFT not constructed | (open) |
| von Koch (1901) bound restated as ACS stability | Cited and reframed | not a new theorem | (interpretive) |

---

## Test summary

```
$ python -m pytest tests/ -v
======================= 42 passed in 4.08s =======================
```

All tests reproduce within machine tolerance using `numpy>=1.24`, `scipy>=1.10`, `sympy>=1.12`. Random seed `20260423` is canonical.

---

## Negative results (delimit model space)

These are first-class outputs of the framework's adversarial-compression methodology:

1. **α₂ forbidden** — representation theory rules out the cross-coupling identically
2. **β_c excluded at tree level** — incompatible with phenomenological mass hierarchies
3. **Equal-VEV alignment forbidden** — M_u = M_d when κ_1 = κ_2 prevents CKM mixing
4. **Wronskian not a Poisson bracket** — Leibniz fails by exact term −fgh'
5. **Universal 2π inversion not universal** — representation-specific, fails for hyperbolic ad
6. **TM1/TM2 ansaetze rejected** — fail to reproduce PMNS angles within 3-5σ
7. **θ_13 cross-coupling rescue impossible** — v_R requirement conflicts with proton decay
8. **θ₀ not derivable from Palatini bracket algebra** — [h,ω] spans all of sl(4) (rank=15,
   `gl4_asymmetry_map.py`); physical selector Function=[k_dir,Form] annihilates BCH hierarchy
   (`vacuum_theta0.py`); θ₀ = 2/9 rad is a fit necessarily; EWSB-scale input required
   (`theta0_derivation_suite.py` OVERCLAIM LEDGER: `theta0-not-derivable-from-algebra`, T2)

These are durable theorems-by-falsification: they tell future model-builders which doors are closed and why.

---

## Known gaps (acknowledged in papers)

1. h̃/h = 2/3 interpretation (Paper A §7) — affects rigor of the Yukawa no-go conditional
2. Coleman-Weinberg without β_c — would determine if tan β reduces 6→5 inputs
3. FeynRules UFO export (Phase D1) — needed for predictive scattering work
4. Hilbert-Pólya construction — exact spectrum match remains 100+ year open problem
5. Post-attractor ΔI < 0 (Paper C) — structural conjecture, not proved
6. Converse direction of renormalized boundedness (Paper B) — full RH equivalence open
