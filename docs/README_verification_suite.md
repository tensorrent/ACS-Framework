# ACS Verification Suite — 72 Scripts
## TR-2026-FF06a/b/c (Wallace, 2026)

All scripts require Python 3.8+ with NumPy and SciPy.
SymPy is required for the exact-arithmetic scripts.
No proprietary software needed.

### How to run everything:
```bash
pip install numpy scipy sympy
for f in *.py; do python3 "$f"; done
```

---

## Phases 1–3 (Trilogy core — 57 scripts)

### Algebra and Selection
| Script | Verifies | Paper |
|--------|----------|-------|
| `lemma29_verify.py` | BCH-TE morphism for polynomial fields | A §2 |
| `gl4_exact.py` | Im(Φ) = sl(4), rank 15, over Q | A §4.2 |
| `selection_principle.py` | Closure defect: sl(3,R) = 0, 100 random > 0.54 | A §4.4 |
| `chirality_uniqueness.py` | J(T) = i·sym + anti, 28 brackets close | A §4.7 |
| `su3_decomposition.py` | su(3) generators from sl(3,R) + J | A §4.5 |
| `fermion_reps.py` | 8 electric charges, 8 hypercharges correct | A §4.6 |
| `three_generations.py` | BCH truncation at order 3 (Jacobi) | A §6.1 |
| `barbero_immirzi_correct.py` | γ = 0.274 from Z(γ) = 1 | A §5 |

### Mass and Mixing
| Script | Verifies | Paper |
|--------|----------|-------|
| `theta0_cabibbo.py` | tan θ₀ = λ_W to 0.23% | A §6.1 |
| `koide_rg_flow.py` | Koide ratio stable under 1-loop RG | A §6.5 |
| `higgs_potential.py` | Sombrero potential from ΔI landscape | A §6.6 |
| `higgs_mass_ratio.py` | m_H = 124.7 GeV (0.42% match) | A §6.6 |
| `higgs_derivation.py` | λ = 2√3/27 Koide projection | A §6.6 |
| `higgs_channel_decomp.py` | L3 symmetric/antisymmetric channels | A §6.6 |
| `neutrino_honest.py` | See-saw product formula (0.1%) | A §6.3 |
| `neutrino_seesaw_v2.py` | M_R ≈ 49 keV prediction | A §6.3 |
| `spin_network_lindblad.py` | WdW attractor ⟨H⟩ = 3×10⁻⁶ | A §5 |

### CKM Attempts (negative results)
| Script | Verifies | Paper |
|--------|----------|-------|
| `pati_salam_ckm.py` | BCH off-diagonals → V_CKM = I | A App C |
| `phase5_ckm.py` | Bi-doublet h+h̃ mechanism | A App C |
| `phase5_1_ckm.py` | Δ_R enhancement attempt | A App C |
| `ps_yukawa_full.py` | Full PS Yukawa texture | A App C |

### Stress Tests
| Script | Verifies | Paper |
|--------|----------|-------|
| `seven_tests.py` | 7 independent stress tests | A §B |
| `four_computations.py` | λ, α_s, sin²θ_W, CKM | A §C |
| `three_fruit.py` | PMNS angles, sterile ν, DW | A §C |

---

## Phases 4–10 (Exploration — 15 scripts)

### Riemann Tensor Analysis (NEW — this session)
| Script | Verifies | Paper B section |
|--------|----------|----------------|
| `riemann_tensor.py` | Tensor mapping, variance, curl, Wronskian, SHO | B §5 (all) |
| `riemann_scaled_final.py` | 100 Odlyzko zeros, 50k closure samples, scaled variance | B §5.2-5.5 |

### Torsion and Causal Structure
| Script | Verifies | New theorem? |
|--------|----------|-------------|
| `torsion_causal.py` | Photon massless (Cartan), c exact (contortion antisym) | T15, T16 |
| `torsion_hierarchy.py` | Full 0:1:4 tier classification of all 15 generators | T19 |

### Vacuum Energy and Higgs
| Script | Verifies | New theorem? |
|--------|----------|-------------|
| `acs_vacuum.py` | Bosonic vacuum cancellation Σ(tc×K)=0 | T14 |
| `torsion_higgs_vacuum.py` | Symbolic verification (exact rational) + W/Z share | T14 (symbolic) |

### Quantisation and Spectra
| Script | Verifies | New result? |
|--------|----------|------------|
| `acs_quantisation.py` | Discrete spectra, 2 polarisations, zero-point energy | Structural |

### Gravitational Waves
| Script | Verifies | New theorem? |
|--------|----------|-------------|
| `gw_torsion.py` | 2 GW pols, c exact, no birefringence, vacuum protected | T17, T18, T20 |

### Fermions
| Script | Verifies | New result? |
|--------|----------|------------|
| `acs_fermions.py` | Chirality, 3 generations (Jacobi dim=3), 48 Weyl | T21 |

### Complete SM and Boundaries
| Script | Verifies | Status |
|--------|----------|--------|
| `acs_complete_sm.py` | Full SM ledger: 13T + 11D + 4P | Summary |
| `acs_higgs_wall.py` | 5-parameter irreducible boundary | Boundary |

### RG and Dynamics (Phases 6–9)
| Script | Verifies | Status |
|--------|----------|--------|
| `phase6_dynamics.py` | Classical field eqns: 0 new constraints | Negative |
| `phase7_qfp_yukawa.py` | QFP with Yukawas: no crossing with bracket λ | Negative |
| `phase8_full_qfp.py` | Full 10-quartic QFP: no stable solution | Negative |
| `phase9_final.py` | CC: 66 orders removed, 55 remain | Partial |
| `phase10_multiangle.py` | 12 ideas evaluated, 2 survive | Strategic |

---

## Result Summary

| Category | Count |
|----------|-------|
| Theorems (exact, no input) | 21 |
| Derived matches (< 5%) | 11 |
| Falsifiable predictions | 9 |
| Contradictions with experiment | 0 |
| Calibration inputs | 2 (m_τ, v) |
| Free parameters | 5 |
| Total inputs | 7 (vs 19+ in SM) |
