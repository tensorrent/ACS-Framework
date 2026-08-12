# Code Map — What Runs, What It Proves, What's Broken

Sources: `code/**`, `scripts/`, `harness/training/`, and the run artifacts in `docs/`.
**194 Python files, ~81k lines.** Only a small fraction is the verification surface.

---

## 1. Architecture

```
code/acs_codebase/           ← the ONLY tested surface
  src/common/                seed.py (CANONICAL_SEED=20260423), lie_algebra.py
  src/paper_a/  (6 modules)  src/paper_b/  (4)   src/paper_c/  (5)
  tests/                     conftest.py + test_paper_{a,b,c}.py  — FLAT, no subdirs
  docs/                      ledger.md, numerical_pitfalls.md, citations.md
  extras/                    109 .py, 64,364 lines, 2.8 MB — HERITAGE, not the verification surface
  verify_all.sh, pytest.ini, requirements.txt
code/hp_knife_suite/         14 scripts, 1,709 lines + data_zeros/
code/issue7/                 7 scripts, 1,354 lines
code/palpha_overlap/         6 files, 2,049 lines
code/capacitance_ribbon/     1 script, 713 lines
code/framed_unknot/          3 scripts, 822 lines
code/notes_verification/     3 scripts, 695 lines (stdlib/numpy only)
code/acs_memo.py             disk+memory memoisation
code/benchmark_efficiency.py 1,019-line benchmark harness
scripts/                     prime_carrier_reproduce.py, ym_comparison_checker.py
harness/training/            NOT part of the verification suite; not runnable as shipped
```

`src/` totals ≈1,600 lines. Every module is library + `main()` + `__main__` guard; tests import the
functions, never the CLI.

**`pytest.ini` sets `testpaths = tests` explicitly** because `extras/` contains 9 files matching
pytest's collection glob with no test functions and no `__main__` guard — collection would *execute*
them. (PR #8 added this; collection went 10.8 s → 2.6 s.)

`requirements.txt`: `numpy>=1.24, scipy>=1.10, sympy>=1.12, pytest>=7.0`. **Extras additionally need
`mpmath` and `matplotlib`, which are not declared.**

---

## 2. The 42 assertions, by test function

### `test_paper_a.py` (14)
| Test | Asserts |
|---|---|
| `test_branch_a_parameter_count` | `total_inputs == 6` |
| `test_alpha1_stability_bound` | 0.80 < 2√(λ_Φ ρ_tot) < 0.82 at ρ₁=0.5 (actual 0.80979) |
| `test_vacuum_admits_stable_minimum` | ≥7 of 9 α₁ values stable (actual 9/9) |
| `test_vacuum_recovers_target_VEVs` | every stable point recovers v² = 246² to <1e-3 rel |
| `test_custodial_breaking_safe` | Δρ < 1e-20, safety > 1e15 (actual 3.76e-29, 5.32e24) |
| `test_lambda_eff_close_to_SM` | \|λ_ACS−λ_SM\|/λ_SM < 0.02 (actual **0.0084** with v=246.22) |
| `test_betac_extremization_yields_pi_4` | SymPy `solve(dV/dβ)` == {π/4, 3π/4} exactly |
| `test_yukawa_no_go_matrix_proportional` | ‖M_u−M_d‖ < 1e-12 and CKM deviation from I < 1e-12 |
| `test_yukawa_no_go_independent_invariant` | same, for independent h, h̃ with norm ratio 2/3 |
| `test_yukawa_algebraic_identity` | `simplify(expand(M_u−M_d) − expand((h−h̃)(κ₁−κ₂))) == 0` |
| `test_theta13_pull_significant` | \|pull\| > 4σ (actual **+5.38σ**) |
| `test_theta13_rescue_incompatible_with_proton_decay` | rescue v_R vs proton bound ratio ≥ 1e10 (actual 1e12) |
| `test_tm1_fails_phenomenology` | TM1 θ₁₂ pull +3.1σ, θ₂₃ pull −4.9σ |
| `test_tm2_fails_phenomenology` | TM2 θ₂₃ pull −4.2σ |

### `test_paper_b.py` (10)
| Test | Asserts |
|---|---|
| `test_resolvent_identity_at_omega_50` | χ(50) = Tr[(50−H)⁻¹] for H = diag(γ_k) (both 3.955088) |
| `test_chi_diverges_near_zeros` | \|χ(γ_k ± 0.01)\| > 50 for the first 5 zeros (≈99–101) |
| `test_leibniz_failure_symbolic` | W(fg,h) − [fW(g,h)+gW(f,h)] ≡ **−f g h′** in SymPy |
| `test_leibniz_failure_numerical` | numeric matches within 1% (−0.048662 both) |
| `test_leibniz_difference_nonzero` | \|−fgh′\| > 1e-3 → W is *not* a Poisson bracket |
| `test_delta_norm_bounded_under_RH` | running-max slope of \|Δ_norm\| on u∈[5,20] < 0.05 (actual 0.00290) |
| `test_off_critical_zero_diverges_faster` | slope with a σ=0.7 zero (0.06648) > on-critical (0.01537) |
| `test_BK_matches_within_two_zeros_through_T_143` | \|N(T) − N_BK(T)\| ≤ 2 at T = 50…143 (max 1.45) |
| `test_BK_leading_form` | N_BK(100) == (100/2π)(ln(100/2π) − 1) |
| `test_riemann_count_at_known_value` | N(50) == 10 (γ₁₀ = 49.773832) |

### `test_paper_c.py` (18)
| Test | Asserts |
|---|---|
| `test_theorem_c_residual_machine_zero` | max\|ad³ − (16/9)ad\| < 1e-12 (actual **0.00e+00**) |
| `test_theorem_c_eigenvalues_correct` | multiplicities {0:9, +4/3:3, −4/3:3} |
| `test_killing_orthogonality_symbolic` | SymPy tr([X,Y]X) and tr([X,Y]Y) both **exactly `0`** |
| `test_killing_orthogonality_sl3_scaling` | 1000 trials 𝔰𝔩(3): max residual 3.55e-15 / 6.66e-15 |
| `test_killing_orthogonality_sl4_scaling` | 1000 trials 𝔰𝔩(4): 6.22e-15 / 7.99e-15 |
| `test_chirality_hopping_exact` | [H₁,A₀₁] == 2 S₀₁ exactly |
| `test_probe_dimension_matches_theory` | dim B⊥ == **14** = n²−2 |
| `test_generators_lie_in_B_perp` | projection residuals 0.00 |
| `test_generic_jacobian_rank` | 20 random pairs → rank **15**, kernel **15** |
| `test_degenerate_kernel_at_H1_A01` | rank **11**, kernel **19** |
| `test_ad_T_BL_is_hyperbolic` | class "hyperbolic", zero_count 9, real 6, imaginary 0 |
| `test_su2_quaternion_elliptic_2pi` | three exp(−iπ/3 σ₃) → −I (deviation 4.14e-16) |
| `test_sl4_hyperbolic_no_2pi_loop` | `is_bounded_loop is False`, max element at 2π > 100 (actual **2.17e3**; e^{8π/3} = 4.35e3) |
| `test_core_rope_R_cubed_equals_R` | R = diag(1,0,−1), R³ = R, hyperbolic |
| `test_frenet_serret_elliptic` | A³ = −(κ²+χ²)A residual 0.00, class "elliptic" |
| `test_bell_state_local_ops_commute` | [σ_x⊗I, I⊗σ_z] == 0 |
| `test_bracket_killing_orthogonal_to_inputs` | tr(BX) = −4.44e-16, tr(BY) = −5.55e-17 |
| `test_direct_projection_returns_zero` | π_X([X,Y]) coefficient −6.33e-17 < FLOAT_TOL |

---

## 3. Module index

### `src/` — canonical
| Path | Computes | Headline |
|---|---|---|
| `common/seed.py` | canonical RNG | `CANONICAL_SEED = 20260423` |
| `common/lie_algebra.py` | 𝔰𝔩(n,ℝ) basis, bracket, Killing form (2n·tr(XY)), coords | dim = n²−1; `FLOAT_TOL=1e-10`, `MACHINE_EPS=1e-14` |
| `paper_a/branch_a_parameters.py` | pruning ledger 9→7→6; α₁ stability bound | λ_Φ = 0.128300, ρ_tot = 1.2778, \|α₁\| < 0.8098 |
| `paper_a/branch_a_vacuum.py` | Decimal(50) Cramer's-rule vacuum over 9 α₁; Δρ; λ_eff | v² = 6.052e4, v_R² = 1.0e30 all stable; Δρ = 3.76e-29; λ_ACS 0.12830 vs λ_SM 0.12938 = **0.84%** |
| `paper_a/betac_tan_beta.py` | symbolic ∂V/∂β = 2β_c v²v_R² cos 2β | critical points [π/4, 3π/4] → tan β = ±1 |
| `paper_a/yukawa_no_go.py` | M_u − M_d = (h−h̃)(κ₁−κ₂); SVD/CKM | ‖M_u−M_d‖ = 0.00e0; CKM deviation 5.55e-16 |
| `paper_a/theta13_obstruction.py` | θ₁₃ = arcsin(λ_W/√2), pull, proton-decay conflict | **9.216° vs 8.57 ± 0.12 → +5.38σ**; JUNO-projected +12.92σ |
| `paper_a/tm1_pmns.py` | TM1/TM2 predicted angles and pulls | TM1 35.72°(+3.1σ)/44.35°(−4.9σ); TM2 45.00°(−4.2σ) |
| `paper_b/explicit_formula_resolvent.py` | χ(ω) = Σ1/(ω−γ_k) = Tr[(ω−H)⁻¹]. Holds `RIEMANN_ZEROS` (50 Odlyzko) | χ(50) = 3.955088 |
| `paper_b/wronskian_leibniz.py` | symbolic + numeric Leibniz defect | defect ≡ **−f g h′** = −0.048662 at x=2 |
| `paper_b/renormalized_stability.py` | Δ_norm(u) = (ψ(eᵘ)−eᵘ)/e^{u/2}; σ=0.7 injection | max 0.5253, slope 0.00290; off-critical slope 0.06648 |
| `paper_b/berry_keating_counting.py` | N_BK(T) = (T/2π)(ln(T/2π) − 1) vs actual | T=50:10/8.55 … T=143:49/48.36 |
| `paper_c/theorem_c.py` | ad_{T_BL} on 𝔰𝔩(4,ℝ) | ad³ = (16/9)ad residual **0.00e+00**; spec {0⁹, ±4/3³} |
| `paper_c/killing_orthogonality.py` | symbolic identity + 2000 trials + [H₁,A₀₁]=2S₀₁ | symbolic `0`; residuals ≤ 8e-15 |
| `paper_c/orthogonal_complement_probe.py` | SVD null space of B⊥; Jacobian rank of dμ | **14 / 15 / 19** |
| `paper_c/spectral_taxonomy.py` | elliptic/hyperbolic/parabolic classifier + 4 instances | SU(2) → −I (4.14e-16); exp(2π·ad) max 2.17e3 |
| `paper_c/er_epr_algebraic.py` | Bell commutation, tr([X,Y]X)=0, π_X(B)=0 | coefficient −6.33e-17 |

### `hp_knife_suite/` — 14 scripts
All load `data_zeros/riemann_zeros_100k.txt`, seed 20260423, and **end with an explicit "proves
nothing about RH / constructs no operator" disclaimer.**

| Script | Computes | Headline |
|---|---|---|
| `hp_knife.py` | witness S(u) at u = log n, n = 2..40; 300 surrogates, N=30k | mean z at prime powers **+54.59**, composites −1.28 |
| `hp_never_synced.py` | real vs GUE (dense 6000×6000) vs lattice at matched density | ratio pp/comp **real 239.7, GUE 0.977, lattice 0.685**. ~44 s |
| `hp_xp_test.py` | Berry–Keating levels vs primes-injected trace-formula levels | xp-honest carries **no** arithmetic (ratio ≈0.71); the circular version is labelled `xp+orbits(CIRC)` |
| `hp_signed_lfunction.py` | C6 sign, C7 weight, C8 quadratic-χ sign flip | C6 1.00; C7 corr 1.00; **C8 18/18** (d = −35, −91, −104) |
| `hp_phase_test.py` | complex witness, χ̄-demodulation resultant | **R(χ) = 0.991** vs trivial 0.085, χ² 0.196 → "PHASE CARRIES χ" |
| `hp_c9_orthogonality.py` | 6×6 Selberg orthogonality from zeros vs from characters | diag 1.00; **corr 0.917**, mean \|Δ\| 0.033 |
| `hp_operator_constraint.py` | the HP wall as two measured numbers | mean \|Im W\|/\|Re W\| = **0.000**; small-spacing slope 2.999 → **β = 2.00** |
| `hp_wall_resolution_class.py` | sympy proof that C = σ_y∘K reconciles the two; GOE/GUE/chGUE discriminator | only **chGUE** passes both (β=2.01, \|Im W\|/\|W\| = 9.9e-13) |
| `hp_vantage_points.py` | 10 witnesses × 300 surrogates + jitter-response independence | **arith 830σ, phasepow 566σ, arith2 42σ, lag1 26σ, rigidity 9σ, lag2 6σ, difftone 5σ, sumtone 4σ**; effective rank 4.8/5; **no third face**. ~10 min |
| `hp_harmonic_ladder.py` | k=2/k=1 line ratio law = p^{−1/2} | slope **−0.533** (pred −0.5), R² = 0.982; GUE null +0.200 |
| `hp_ladder_tower.py` | extends to rung k=3 | rung 2 slope **−0.501** (R²=1.000); rung 3 **−1.015** (p ≤ 7); 33-line abs. weight slope **+1.002** |
| `hp_ladder_character_twist.py` | χ^k twist; demod table; commutator ‖[ι,T]‖_k | quadratic 0 both rungs; mod-5 ord-4 0.643/0.000; mod-7 ord-6 0.619/0.619 |
| `hp_twist_hardened.py` | 3×3 demod on ~150 regenerated L-zeros | rung 1 R=0.995 RESOLVED; **rung 2 R=0.220 at floor — honest negative**; rung 3 R=0.591 |
| `hp_form_function_relativity.py` | witnesses vs Poisson ≺ GUE-marginal (≺ GUE-full with `--full`) | repulsion 49.5σ→**0.2σ**; arith 259.9→**832.2**. 2.4 s / ~7 min |

### `issue7/` — 7 scripts
| Script | Headline |
|---|---|
| `section9_toy_kill_test.py` | corr(gap,ξ) = −0.6375 (expected) but corr(gap,leak) = **+0.9636 (wrong sign)** → chain not supported |
| `exhaustive_issue7.py` | **support 0/12**; 4/3 finite-d spread 74.0; all exact hits satisfy n = d+1 |
| `cross_model_kill_pass.py` | TFIM 0/6, XXZ 1/6 → **1/12** |
| `long_range_kill_pass.py` | α=3 2/6, α=2 3/6 → **5/12** |
| `section9_exact_kill_test.py` | sign cov(gap,cluster) = −1 ✓ but sign cov(gap,outside) = **0** → `supports_chain: false` |
| `mechanism_4over3_test.py` | hits (2,3)…(11,12) all n = d+1 → **"mechanism not established"** |
| `verify_issue7_pipeline.py` | runs all 6, SHA-256s, cross-checks JSON ↔ docs → `PASS_WITH_CAUTION` |

### `palpha_overlap/`, `capacitance_ribbon/`, `framed_unknot/`, `notes_verification/`
| Script | Headline |
|---|---|
| `isotope_catalog.py` | 14 base emitters + 15 NNDC = 29; R = 1.504·A^{1/3} fm, b = 2Z_d e²/Q |
| `palpha_overlap.py` | flat j₀ × Gaussian → **r = 0.8882**, RMS 1.7705, S★ = 2.70e-2, RMS_{S★} = 0.8220 |
| `palpha_overlap_throat.py` | AdS weight w=R/r + Woods–Saxon → r = 0.8875, RMS_{S★} = 0.8247 |
| `palpha_overlap_refined.py` (953 L) | Channel A (S(A,Z), LOO), Channel B (self-consistent eigenmode) → **r = 0.9676** |
| `palpha_overlap_gamow.py` | Channel C, Robin outgoing WKB. **Library only, no `__main__`** (documented) |
| `palpha_overlap_extended.py` | 29-isotope re-run → base-14 LOO 0.286 vs extended **1.355**; r drops 0.888 → **0.199** |
| `ribbon_capacitance.py` (713 L) | three models. Best α⁻¹: annulus 6.14, conformal 3.25, BIE 0.37 vs 137.036 (rel err 0.955). Analytic CODATA roots at a/R ≈ 2.04e-118 and 3.82e-237. **A documented negative.** ~32 s cold |
| `framing_transformer.py` | Tw −1.0338 + Wr −0.9662 = **−2.0000**, σ = −1 three ways; measured rule **σ = (−1)^{Sl+1}** |
| `moment_ratio.py` | **g = 1.000000 exactly, shape-independent** |
| `one_object.py` | S³ Laplace eigenvalue **−3.0000000, degeneracy 4**, errors ≤ 8e-7; irrational slope never closes |
| `test_lattice_imprint.py` (N1) | **clean negative**: 0.6–1.2× null mean, z ∈ [−0.7, +0.3] |
| `test_signature_selection.py` (N2) | uniquely minimised at diag(1,1,1,−1); 6 functionals, 5000 samples, 50 rotations → **ALL PASS** |
| `test_scaled_invariance.py` (FF06h) | A–D all PASS; only width/δ is physical |

### `scripts/`
`prime_carrier_reproduce.py` reproduces every FF06f table. **Table 1** (N=200, 300 trials): ordered
baseline 51.988 (100%), spacing shuffle 2.770 (5.3%), gap 2-point 3.773 (7.3%), index 2-point 3.729
(7.2%), **value-space pair-correlation 51.988 (100.0% exact)**, Poisson null 5.869. **Table 2**
(N=4000): Pearson r = **0.9975**; prime-power mean 36.15 vs composite 0.01. **Table 3:** separation
grows **18.4× → 474.2×** (N = 200 → 10,000). Mechanism: gap autocovariance preserved yet prime power
collapses 216.4 → 1.258. ~2 min.
`ym_comparison_checker.py` diffs a target document against the sealed YM predictions C1–C6, X1–X2.

### `extras/` — heritage, 109 scripts
Naming: `phase##_*` chronological phases · `acs_*` early framework · `task_*` paper-section tasks ·
`paper_b_*` · `test_conjecture_*` adversarial tests. Several carry inline `StrickenBy{rule: …}`
self-retraction annotations and append-only `OVERCLAIM_LEDGER` structures.

**The three MANIFEST-cited scripts (expected to run clean):**
- `barbero_immirzi_correct.py` — brentq + mpmath(50 dps) on Z(γ)=1. **γ_ACS = 0.274067** (SU(2)); SO(3)-only 0.190206; DL leading ln2/(π√3) = 0.127384.
- `koide_clebsch_gordan.py` — chirality map, BCH orders, Nelder–Mead Koide fit, 10,000-sample scan. **Best θ₀ = 3.86° / 3.92° vs target 12.73° — a documented FAILURE**, self-annotated as a T2 derived-negative. ⚠️ See §7.
- `higgs_mass_ratio.py` — m_H/v from the bracket potential, then a 17-candidate numerology search. Winner 4/(3π)√(2πλ_W) = 0.506306 vs 0.508691 → **0.47%** (m_H = 124.66 GeV).

**Thematic index (one line each):** *Algebra/selection* — `lemma29_verify.py` (BCH-TE morphism),
`gl4_exact.py`, `gl4_asymmetry_map.py` (rank 15 ⇒ the θ₀ no-go), `selection_principle.py` /
`selection_full.py`, `chirality_test.py` / `chirality_uniqueness.py`, `su3_decomposition.py`,
`su3_torsion_intersection.py`, `colour_charges.py`, `colour_geometry.py`, `integer_acs.py`,
`layered_resolution.py`. *Fermions* — `fermion_reps.py`, `fermion_reps_full.py`, `acs_fermions.py`,
`three_generations.py`, `and_gate_test.py`. *Flavour/θ₀/CKM (mostly negatives)* —
`theta0_derivation_suite.py` (**VERDICT T2 DERIVED NEGATIVE**), `theta0_cabibbo.py`,
`koide_rg_flow.py`, `vacuum_theta0.py`, `bl_vev_projection.py`, `quark_koide_gut.py`,
`ckm_derivation.py`, `pati_salam_ckm.py`, `ps_yukawa_full.py` (all → V_CKM = I),
`phase12_task1_pmns.py`, `task_B_theta13.py`, `phase52_yukawa.py`. *Higgs/vacuum/RG* —
`higgs_potential.py`, `higgs_derivation.py`, `acs_higgs_wall.py`, `acs_final_wall.py`,
`phase50_vacuum.py` (**superseded — has the float64 cancellation bug**), `phase51_tanbeta.py` (T4),
`phase7_qfp_yukawa.py`, `phase8_full_qfp.py`, `phase9_final.py` (CC: 66 orders removed, 55 remain),
`phase10_multiangle.py` (12 ideas, 2 survive), `task_D_lagrangian.py`. *Neutrinos* —
`neutrino_seesaw_v2.py`, `neutrino_exact.py`, `neutrino_honest.py`. *Gravity/torsion/LQG* —
`riemann_curvature_palatini.py` (T1: Schwarzschild ∇g=0, R_μν=0, K=48M²/r⁶), `ricci_flow.py`,
`gw_torsion.py`, `torsion_hierarchy.py` (0:1:4 — photon 0, W/Z 0.889, gluon 3.556),
`torsion_higgs_vacuum.py`, `torsion_condensation_holonomy.py`, `gamma_discrepancy.py`,
`chern_simons_projection.py`, `horizon_puncture_saddle.py`, `spin_network_lindblad.py`,
`acs_vacuum.py`, `phase55_holonomy_corrected.py` (corrects the ad-as-rotation error: ‖U−I‖ → 2174 at
t=2π). *ER=EPR* — `acs_ads_cft_er_epr.py`, `er_epr_audit.py`, `acs_vs_er_epr_test.py`
(reconstruction error = 1 was a **theorem, not a bug**). *Riemann in extras* — `paper_b_plasma.py`,
`paper_b_resolvent.py`, `fn_n200.py`, `t4_converse.py`, `eml_vs_acs_test.py`, `mersenne_bridge.py`.
*Conjecture kills* — `test_conjecture_condensate_collapse.py`,
`test_conjecture_em_torsion_annihilator.py`, `test_conjecture_hypercone_projection.py` (β = codim−1).
*Summaries* — `acs_complete_sm.py`, `acs_verify_all.py`, `four_computations.py`,
`phase11_tests.py`, `generate_figures.py`.

**`ACS_all_76_scripts.py`** — 1.07 MB / 26,575 lines. **Not a program:** a flat concatenation of 76
of the above separated by `# SCRIPT n/76: <name>.py` banners. Redundant. **Never import or execute.**

---

## 4. How to run everything

```bash
pip install numpy scipy sympy pytest           # + mpmath matplotlib for some extras
cd code/acs_codebase && python -m pytest -q    # 42 passed in ~2.3 s
bash verify_all.sh                             # all 15 modules + suite, ~2.5 s
python -m src.paper_c.theorem_c                # any single module

cd code/hp_knife_suite
python3 hp_knife.py                     # ~20 s
python3 hp_never_synced.py              # ~45 s (dense 6000×6000 diagonalisation)
python3 hp_xp_test.py                   # ~30 s
python3 hp_signed_lfunction.py; python3 hp_phase_test.py; python3 hp_c9_orthogonality.py
python3 hp_operator_constraint.py       # ~5 s
python3 hp_vantage_points.py            # ~10 min
python3 hp_harmonic_ladder.py; python3 hp_ladder_tower.py; python3 hp_twist_hardened.py
python3 hp_form_function_relativity.py         # 2.4 s
python3 hp_form_function_relativity.py --full  # ~7 min

python3 code/issue7/verify_issue7_pipeline.py
python3 scripts/prime_carrier_reproduce.py      # ~2 min
python3 code/notes_verification/test_*.py       # <1 s each, stdlib only
python3 code/palpha_overlap/palpha_overlap.py   # 0.7 s
python3 code/capacitance_ribbon/ribbon_capacitance.py   # ~32 s cold, ~0.15 s warm (memo)
```

**Canonical seed `20260423`.** Two documented deviations:
`src/paper_a/yukawa_no_go.py::yukawa_no_go_test(seed=42)` and `src/paper_c/er_epr_algebraic.py`
(`default_rng(42)` hardcoded twice). Both contradict pitfall #6's claim of universal canonical
seeding, but are harmless — the results are seed-independent theorems.

**Environment gotchas.** Modules must run as `python -m src.<pkg>.<mod>` from `code/acs_codebase/`
(they mutate `sys.path`). `paper_b/__init__.py` re-exports `RIEMANN_ZEROS`, triggering a benign
`RuntimeWarning: found in sys.modules after import of package`. **PDG v = 246.22 GeV is canonical**
(246 gives a spurious 1% λ discrepancy). **All artifact writers resolve `Path(__file__).parents[2]/"docs"`
— running them overwrites tracked JSON in `docs/`.**

`code/acs_memo.py`: disk + in-memory memo, `.cache/` at repo root, `ACS_MEMO=0` disables,
`ACS_MEMO_DIR` overrides, exposes `STATS{hits,misses,writes}`.

---

## 5. The seven numerical pitfalls (`code/acs_codebase/docs/numerical_pitfalls.md`)

1. **Catastrophic cancellation in scale-separated Cramer's rule.** v² = (2ρ_tot μ²_φ − α₁ μ²_Δ)/(4λ_φρ_tot − α₁²): with v ≈ 246 and v_R ≈ 1e15, both numerator terms are ~1e29 GeV² but must differ by ~1e4 — a 25-order ratio exceeding float64's ~16 digits, so naive evaluation returns **v² = 0** (a spurious "unstable"). Fix: `decimal` at 50 digits.
2. **`numpy.bool_` vs Python `bool`.** `np.allclose(...) is True` → `False`. Fix: wrap every returned numpy boolean in `bool(...)` at the return site; tests deliberately use `is True` so leaks fail loudly.
3. **Bracket-map Jacobian rank is point-dependent.** Generic: rank 15, kernel 15. Degenerate at (H₁,A₀₁): rank 11, kernel 19. Passive dim B⊥ = 14. **Citing only one — especially the degenerate 19 — produces a misleading "ambiguity factor"; always report all three.**
4. **SymPy `MatrixSymbol` does not auto-distribute scalars.** Fix: commutative scalar symbols + explicit `expand()`; the matrix-level proof is carried numerically. MatrixSymbol is for shape tracking, not distributivity.
5. **exp(2π·ad_{T_BL}) ≈ e^{8π/3} ≈ 4348 is correct, not a bug.** Real spectrum ±4/3 ⇒ hyperbolic flow; the 2π loop does not close. **A *small* value at 2π would be the actual bug.**
6. **Random seed discipline.** Canonical 20260423; cross-NumPy-version reproducibility is a known limitation.
7. **Implicit `np.float64` default.** Fine for everything shipped; would matter only for explicit-formula work at thousands of zeros (needs mpmath).

---

## 6. Data artifacts

- **`data_zeros/riemann_zeros_100k.txt`** — 1.8 MB, **99,999 lines** (not exactly 100k), Odlyzko, 9-decimal, 14.134725142 → 74920.827498994.
- **L-function zeros** (imaginary parts, ascending): `cyclotomic_5/zeros_chi_5_order4.txt` 54 zeros and `_ext` **146**; `cyclotomic_7/zeros_chi_7_order6.txt` 59 and `_ext` **154**; `cyclotomic_and_h6/zeros_chi_-104.txt` 67 (ℚ(√−26), h=6); `disentangled/zeros_chi_-35.txt` 65 and `zeros_chi_-91.txt` 55 ("the decisive sample").
- **The non-circularity mechanism** — `generate_more_lzeros.py` builds L(s,χ) = q^{−s} Σ χ(a) ζ(s, a/q) from the **Hurwitz zeta** at mp.dps=20, so **primes are never inserted** into the object whose prime structure is then read out. The root finder needs no root number: at a simple zero both Re L and Im L change sign, so it brackets Im-L sign changes (step 0.04), refines with `findroot(solver='anderson')`, and accepts only where |L| < 1e-6 collapses. Deterministic, seed-free; validated against pre-existing files to ~5 digits. **This is what makes the C8/C9/twist results non-circular** — and exactly what `hp_xp_test.py` contrasts against (injecting the prime trace-formula fluctuation into Berry–Keating levels *is* circular and is labelled `xp+orbits(CIRC)`).
- **Four synthesis `.md` files** (768 lines): `cyclotomic_synthesis.md` — ℚ(ζ₅) 4-tier splitting recovered, split_4 mean |F_K| **0.696** vs split_2 0.099, inert 0.107 (ratio 2.15× vs ℚ(i)'s 0.323, predicted 2×). `cyclotomic_7_synthesis.md` — "the cleanest single result": six order-6 character classes at 60° in the (F_cos, F_sin) plane, **mean absolute phase error 6.7°**. `final_synthesis.md` — the h=6 plateau plus the first complex-character channel split. `disentangled_synthesis.md` — the decisive fixed-h varying-conductor experiment: h=2 ratios 3.96/3.39/3.13/3.03 at conductors 15/20/24/35 but **1.30 at conductor 91** → **"0.52 + 5.82/h" is FALSIFIED**; what survives is "split mean roughly constant (~0.30), inert mean grows monotonically with conductor (0.041 → 0.206)." All four adopt an explicit Track A (publishable empirical) / Track B (speculative) split with reviewer-driven tightening ("law" → "empirical scaling phenomenon", "proves" → "operational recovery").

---

## 7. ⚠️ Broken, stale, or contradicting

### Stale README references (`code/acs_codebase/README.md`) — **all fixed 2026-08-12**
- Lists `paper_c/holonomy_representation.py`, `frenet_serret.py`, `core_rope_ring.py` — **none exist**; those checks are functions inside `spectral_taxonomy.py`.
- Quick-start says `python -m src.paper_b.resolvent_renormalized` — **no such module** (it's `renormalized_stability`).
- Shows `tests/paper_a/`, `tests/paper_b/`, `tests/paper_c/` subdirectories — tests are **flat files**.
- Cites `src/paper_a/lagrangian_specification.md` — **does not exist**.
- Says extras is "~100 scripts"; actual **109**. The top-level README says "~130" — also off.

### Numbers that disagree with their own docs
- ~~`theta13_obstruction.py` docstring "≈9.18 degrees, a 5.2σ pull"~~ **fixed 2026-08-12** to 9.216° / 5.38σ (matching the code); Paper A's table likewise updated to 5.4σ.
- ~~`ledger.md` "λ_eff within 1.01%"~~ **fixed 2026-08-12** to **0.84%** (canonical v = 246.22); the row now records that 1.01% was the v = 246 value.
- ~~`README_verification_suite.md` "0.42% match"~~ **fixed 2026-08-12** to **0.47%**, with the 17-candidate search disclosed in the same row.
- `barbero_immirzi_correct.py` claims γ = 0.274067 "matches the Meissner partition function approach" three lines after printing "Commonly cited Meissner value: γ ≈ 0.2375" and "Discrepancy: 0.036567."
- ~~The top-level README billed `koide_clebsch_gordan.py` as a clean "0.001% fit"~~ **fixed 2026-08-12**: it now states both the confirmed part (Koide's *empirical* relation at 0.001%) and the logged negative (θ₀ = 3.86°/3.92° vs 12.73°, `CONCESSION CONFIRMED (T2 derived negative)`).

### Selection-by-search dressed as derivation
- `higgs_mass_ratio.py` computes a bracket-based m_H/v, gets a poor answer, then searches **17 hand-written closed forms** in λ_W and 4/3 and reports the winner as "THE RESULT / ← EXACT". `higgs_derivation.py` exists specifically to try (and fail) to derive that formula. **Treat as numerology, not derivation.**
- `koide_clebsch_gordan.py` scans 10,000 random pairs for the one closest to a target angle — the script now says outright that a random scan cannot select a vacuum direction.

### Non-runnable / dead code
- `data_zeros/*/{cyclo_figure, cyclotomic_test, cyclotomic_v2, cyclotomic_zeros, cyclotomic_7*, do_m104, do_h2_disentangle, disentangled_fig}.py` — hardcoded `OUTDIR = "/home/claude/..."` and load `.npz` files **not shipped**. Provenance only; the `.txt` zeros and `.md` syntheses are the durable outputs.
- `palpha_overlap_gamow.py` has no `__main__` (documented, by design).
- `harness/training/run_phase1_tune_batch.sh` calls `compare_runs.py`, **not in the repo**; the phase-D sweep needs `harness/reports/training/gsm_merged_telemetry_x50.jsonl`, also absent. Use `--disable-merkle-memory` and `SKIP_COMPARE=1`. Both documented in `harness/training/README.md`.
- `extras/.chialisp/**/*.hex` — three compiled Chialisp blobs with an authoring-machine path baked into the directory name; unrelated to ACS.

### Output-path drift
`palpha_overlap*.py` write to `docs/palpha_overlap_results.json` but the **committed** artifacts live
in `docs/palpha_overlap/` — running them creates untracked top-level duplicates. Same class:
`ribbon_capacitance.py`, `framed_unknot/`, `issue7/` overwrite tracked `docs/*.json` in place.
`issue7_verification_report.json`, `issue7_logs/*.txt`, and the Antigravity `verification_report.json`
embed macOS absolute paths. Only `issue7_linux_replication/` is path-clean.

### Superseded in place (flagged in `extras/README.md`, not corrected)
`phase50_vacuum.py` still has the float64 cancellation bug that `branch_a_vacuum.py` fixes ·
`acs_vs_er_epr_test.py` still reports "reconstruction error = 1" as an anomaly when it is the
Killing-orthogonality theorem · `task1_tm1_redo.py` builds a non-unitary symbolic TM1 matrix.

### Easy to misread, not a defect
`ledger.md` itself labels the Paper B resolvent identity **"Rigorous (tautological)"** — H is
literally `diag(γ_k)`, so `test_resolvent_identity_at_omega_50` verifies a *definition*, not a
construction. The hp_knife suite is the honest counterweight: all 14 scripts end by stating they
construct no operator and prove nothing about RH.

---

## 8. Run artifacts in `docs/`

| Artifact | Headline |
|---|---|
| `issue7_exhaustive_results.json` | **support 0/12**; finite-d spread 74.0; 98 exact hits, all n = d+1 |
| `issue7_cross_model_results.json` | **1/12** |
| `issue7_long_range_results.json` | **5/12** |
| `issue7_section9_exact_results.json` | `sign_cov_gap_outside_affect: 0`, **`supports_chain: false`**, `float_free: true` |
| `issue7_verification_report.json` | **`PASS_WITH_CAUTION`**, 0 consistency errors, 3 warnings ("finite-model diagnostics, not universal no-go proofs") |
| `issue7_linux_replication/` | reproduces macOS numbers to ~1e-14 (corr −0.6129301583028085 vs …076) |
| `capacitance_ribbon_results.json` | best α⁻¹ **6.14 / 3.25 / 0.37** vs 137.036 |
| `framed_unknot_results.json` | Tw + Wr = −2.0000, σ = −1 ×3 → **σ = (−1)^{Sl+1}** |
| `framed_unknot_moment_ratio.json` | **g = 1.0 exact, shape-independent** |
| `framed_unknot_one_object.json` | S³ Laplace eigenvalue **−3.0, degeneracy 4** |
| `palpha_overlap/*.json` | flat 0.8882 / throat 0.8875 / eigenmode 0.9676 / gamow 0.9676; global-S RMS all ≈0.825 (**Δ ≈1e-3 — the upgrades barely move the metric**) |
| `efficiency_benchmark_results.json` | `status: pass`; Gamow cold→warm **14.38×**, BIE **7284×**, ribbon warm **81×** |
| `ACS_Antigravity_Feed_Package/verification_report.json` | 2026-07-02, `overall_status: PASS`, core pytest **42 passed in 1.80 s** |

`docs/README_verification_suite.md` claims 21 theorems / 11 derived matches (<5%) / 9 predictions /
0 contradictions / 2 calibrations / 5 free params / **7 total inputs** vs 19+ SM — note the 7-vs-6
discrepancy with Paper A's ledger (audit M3).

---

## 9. `code/acs_codebase/docs/ledger.md`

Three-category ledger (Rigorous / Conjectural / Disproved), one row per claim.

- **Paper A (17 rows).** Rigorous: Theorem C (residual 0.00e+00); 5 quartics pre-pruning; Palatini locks (cited, not re-derived); α₂ = 0 (docstring-level evidence only); stable vacuum over 9 α₁; Δρ ~4e-29; λ_eff within 0.84% (corrected 2026-08-12; see §7); β_c ⇒ tan β = ±1; M_u = M_d no-go; θ₁₃ not rescuable; TM1/TM2 fail; Branch A locks at 6 inputs. Conjectural: CW fixing tan β (2–4 weeks); h̃/h = 2/3 matrix-vs-invariant interpretation; FeynRules export.
- **Paper B (12 rows).** Rigorous: simple poles at γ_k; the resolvent identity **explicitly labelled "tautological"**; Δ_norm bounded under RH (forward direction, von Koch 1901); off-critical divergence; BK counting. **Disproved:** Wronskian as Poisson bracket, and consequently the **plasma-Hamiltonian foundation** (demoted to analogy). Open: BK exact spectrum (26+ yrs), HP construction (100+ yrs), the converse.
- **Paper C (18 rows).** All the taxonomy/orthogonality results. **Disproved:** universal "2π inversion at three steps" — representation-specific.
- **8 first-class negative results:** α₂ forbidden; β_c excluded at tree level; equal-VEV forbidden; Wronskian ≠ Poisson; 2π inversion not universal; TM1/TM2 rejected; θ₁₃ rescue impossible; **θ₀ not derivable from the Palatini bracket algebra** ([h,ω] spans all of 𝔰𝔩(4), rank 15).

`docs/citations.md` maps results to literature — **von Koch 1901 flagged CRITICAL CITATION** for the
boundedness claim ("the framing is new; the underlying inequality is von Koch's") — plus
Berry-Keating 1999, Pati-Salam 1974, Zamolodchikov 1986, Komargodski-Schwimmer 2011,
Maldacena-Susskind 2013, Odlyzko, and Lakatos/Popper for methodology.
