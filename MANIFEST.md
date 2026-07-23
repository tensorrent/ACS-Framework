> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# MANIFEST — ACS Complete Bundle

Assembled 2026-06-27. Seed `20260423`. All code below was executed at assembly time.

## Four-tier verification hierarchy (tiers never promote)

| Tier | Standard |
|------|----------|
| **T1** | Machine-verified — automated test passes, reproducible by running the code |
| **T2** | Proved in paper — complete mathematical proof, human-verified |
| **T3** | Numerically verified — consistent across runs, not yet theorem-level |
| **T4** | Explicitly falsified — computation shows the claim is false (recorded, not hidden) |

Assembly-time checks: `acs_codebase` → **42 passed**; HP suite → reproduces session
figures (phase demod R = 0.991; C9 zeros-vs-truth corr = 0.917).

---

## Papers (latest version of each)

| File | Paper | Notes |
|------|-------|-------|
| core_trilogy/Palatini_Gauge_Attractor | A | Pati-Salam SU(4)×SU(2)×SU(2) from Palatini bracket on sl(4,ℝ) |
| core_trilogy/Riemann_Spectral_Critical_Line | B (May 26) | deepest/longest form |
| core_trilogy/Spectral_Witness_Refinement | B' (May 30) | retitled, tightened |
| core_trilogy/Holographic_Spectral_Inversion | C | holographic resolution / ER=EPR algebraic |
| notes/Pythagorean_Lattice_Limits | N1 | |
| notes/Adjoint_Clifford_Adjoint_Clifford_Adjoint_Clifford_Adjoint_Clifford_Adjoint_Clifford_Signature_Selection | N2 | grading-selection theorem |
| notes/Prime_Gap_Prime_Gap_Prime_Gap_Prime_Gap_Prime_Gap_Transition_Operator | N3 | prime-gap Dynamical Dynamical Dynamical Dynamical Dynamical Transition Operators over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembles |
| methodology/Spectral_Rigidity_Shuffle_Knife | — | the discriminant itself |
| methodology/Form_Function_Relativity | FF06g | the form/function label is frame-relative (companion to FF06e) |
| later_FF06_series/ (8 papers) | — | June methodology/geometry thread; documents only |

---

## Claim → evidence → tier

### Paper A (Colour from Gravity)
| Claim | Tier | Evidence |
|-------|------|----------|
| SU(3) closure attractor | **T3** | `acs_codebase/src/paper_a/`, selection scripts (50k-sample numerical, not a uniqueness theorem) |
| Higgs quartic λ_φ = 2√3/27 | **T2** | Koide projection; `acs_codebase` paper_a + `extras/koide_clebsch_gordan.py` |
| α₂ = 0 (representation theory) | **T2** | paper_a |
| β_c = 0 no-go (tree level) | **T2** | `acs_codebase/src/paper_a/betac_tan_beta.py` |
| tan β gauge-protected (CW 6→5 fails) | **T4** | `extras/phase51_tanbeta.py`, `phase50_vacuum.py` — fermion-dominated, boundary min |
| N_gen = 3 (Jacobi truncation at BCH order 3) | **T1** | paper_a |
| γ = 0.274 (Barbero-Immirzi, Meissner) | **T2** | `extras/barbero_immirzi_correct.py` |
| θ_QCD = 0, torsion ratio 0:1:4 | **T2** | paper_a |
| θ₁₃ obstruction / TM1 PMNS | **T2/T3** | `src/paper_a/theta13_obstruction.py`, `tm1_pmns.py` |
| Riemann curvature = Layer-2 bracket R^{ab}=dω+ω∧ω; Palatini eqs solve ω→Γ→R (Schwarzschild: ∇g=0, R_μν=0, K=48M²/r⁶) | **T1** | `extras/riemann_curvature_palatini.py` |

### Paper B (Riemann Spectral ACS)  +  HP knife suite
| Claim | Tier | Evidence |
|-------|------|----------|
| Wronskian ≠ Poisson (Leibniz fails by −fgh′) | **T2** | `acs_codebase/src/paper_b/wronskian_leibniz.py` |
| RH ⇒ stationarity | **T2** | paper_b (functional analysis) |
| von Koch stability | **T2** | `src/paper_b/renormalized_stability.py` |
| Berry-Keating smooth counting reproduced | **T2(known)** | `src/paper_b/berry_keating_counting.py` |
| C5 arithmetic present (real 240 vs GUE ≈1) | **T1** | `hp_knife_suite/hp_never_synced.py` |
| Berry-Keating xp carries no arithmetic | **T1** | `hp_knife_suite/hp_xp_test.py` (xp-honest 0.71; circular injection labeled) |
| C6 sign + C7 von Mangoldt weights (zeta) | **T1** | `hp_knife_suite/hp_signed_lfunction.py` (sign 100%, weight corr 1.00) |
| C8 character sign, quadratic L (18/18) | **T1** | `hp_signed_lfunction.py` |
| C8′ complex-character phase (R = 0.99) | **T1** | `hp_phase_test.py` (order-4 mod 5, order-6 mod 7) |
| C9 finite-prime orthogonality (corr 0.92) | **T1** | `hp_c9_orthogonality.py` |
| Form/function label is frame-relative (staircase over Poisson ≺ GUE-marginal ≺ GUE-full) | **T1** | `hp_knife_suite/hp_form_function_relativity.py` (repulsion/shape flip FUNC→FORM 44σ→0.1σ; arith FUNC in all frames) |

> **Scope:** C5–C9 numerically exhibit the explicit formula (Weil–Guinand) and its
> Dirichlet generalization — known theorems. The suite is a falsification/calibration
> instrument, not a source of new theorems, and constructs no operator. Non-circularity:
> L-zeros built from L(s,χ) via Hurwitz zeta (`data_zeros/cyclotomic_*/*.py`), primes never
> inserted. "Selberg orthogonality" here = finite-prime proxy, consistent with the
> asymptotic statement, not it.

### Paper C (Inversion Arc)
| Claim | Tier | Evidence |
|-------|------|----------|
| Killing-orthogonality (Thm 4.1) | **T2** | `acs_codebase/src/paper_c/killing_orthogonality.py` |
| Three-class spectral taxonomy (Thm 4.2) | **T2** | `src/paper_c/spectral_taxonomy.py` (Jordan-Chevalley) |
| ER=EPR algebraic correspondence | **T2/T3** | `src/paper_c/er_epr_algebraic.py` |

### Notes
| Claim | Tier | Evidence |
|-------|------|----------|
| N1 — IR lattice imprint is null vs PDG | **T4** | `code/notes_verification/test_lattice_imprint.py` |
| N2 — general grading selection theorem | **T2** | `code/notes_verification/test_signature_selection.py` (bilinearity + weighted max-cut) |
| N2 — G₂ exceptional-algebra counterexample | **T2** | same (cluster coherence fails for multi-length root clusters) |
| N3 — Dynamical Dynamical Dynamical Dynamical Dynamical Transition Operators over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembles P_m; ker = Dirichlet characters | **T1/T3** | `notes_verification/PRIME_GAP_TRANSITION_OPERATOR.md`, `hp_knife_suite/data_zeros/cyclotomic_*` |

> **N3 fresh-eyes note (2026-06-27):** the Dynamical Dynamical Dynamical Dynamical Dynamical Transition Operators over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembles's eigenvalues are bounded
> dynamical modes (|λ| ≈ 0.01–0.3), **not** an unbounded spectrum claimed to *be* the
> Riemann zeros. Its connection to L-functions is via the kernel (characters), not the
> eigenvalues. Recorded so the bundle does not overstate N3.

---

## Falsified claims ledger
`docs/Elimination_Ledger.md` — the eight explicitly falsified claims
(ad³=2·ad, universal 2π inversion, Wronskian-Poisson, IR lattice imprint, intrinsic
chirality, Route A/C Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Signature Selection in Clifford Algebras in Clifford Algebras in Clifford Algebras in Clifford Algebras in Clifford Algebras, CW 6→5). First-class results.

## Reproduction notes
- Seed `20260423` throughout. PDG v = 246.22 GeV canonical.
- Riemann zeros: Odlyzko first 100,000, `data_zeros/riemann_zeros_100k.txt`.
- Codebase entry point: `code/acs_codebase/` (`pytest -q` → 42 passed).


---

## Issue #7 companion — Section 9 cone chain & 4/3 kill tests (TR-2026-FF06-I7)

Paper: `papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex`  
Code: `code/issue7/` · Artifacts: `docs/issue7_*.json`, `docs/issue7_logs/`  
Verify: `python3 code/issue7/verify_issue7_pipeline.py`

| Claim | Tier | Evidence |
|-------|------|----------|
| TFIM exhaustive chain support rate 0/12 | **T1** | `code/issue7/exhaustive_issue7.py` |
| Cross-model combined support 1/12 | **T1** | `code/issue7/cross_model_kill_pass.py` |
| Long-range combined support 5/12 | **T1** | `code/issue7/long_range_kill_pass.py` |
| Exact joint chain support false | **T1** | `code/issue7/section9_exact_kill_test.py` |
| 4/3 identity family n=d+1 on scanned lattice | **T1** | `code/issue7/mechanism_4over3_test.py` |
| 4/3 mechanism established under K1/K2 | **T4** | failed normalisation robustness + identity bookkeeping |
| Section 9 gap→cone chain as general theorem | — | not claimed |


---

## Flag Condensate notes — Möbius-screw electron & nuclear decay

| File | Notes | Status |
|------|-------|--------|
| `papers/notes/Mobius_Screw_Electron.tex` | Framed unknot $(2,1)$; $Sl=2\leftrightarrow g=2$ (model ID); capacitance estimate $\alpha^{-1}\approx 137.036$ | Design / estimate (RC1-scoped) |
| `papers/notes/Flag_Condensate_Nuclear_Decay.tex` | Phase-slip / Bogoliubov Gamow channel; Geiger–Nuttall and Hawking transfer-matrix fits as reported in-note | Companion programme note |

