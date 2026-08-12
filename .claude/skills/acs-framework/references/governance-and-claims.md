# Governance — Tiers, the Claim Ledger, the Kills, and the License

Sources: `MANIFEST.md`, `docs/Elimination_Ledger.md`, `docs/ACS_FRAMEWORK_SKILL.md`,
`docs/ACS_Technical_Whitepaper.md`, `docs/ACS_Corpus_Map.md`, `docs/Editorial_Audit_2026-08-07.md`,
`LICENSE`, `CITATION.cff`.

**Canonical sources of truth:** `MANIFEST.md` + `docs/Elimination_Ledger.md`. Where
`key_parameters_ledger.json` disagrees, the JSON is stale (see §9).

---

## 1. The T1–T4 tier system

| Tier | Standard (verbatim from MANIFEST) |
|---|---|
| **T1** | Machine-verified — automated test passes, reproducible by running the code |
| **T2** | Proved in paper — complete mathematical proof, human-verified |
| **T3** | Numerically verified — consistent across runs, not yet theorem-level |
| **T4** | Explicitly falsified — computation shows the claim is false (recorded, not hidden) |

**"Tiers never promote"** is the section heading itself. Enforcement clauses:
- `ACS_FRAMEWORK_SKILL.md` §3: *"When reporting results, always state which tier. **Never let Tier 3 pass as Tier 2.**"*
- Elimination Ledger: the kill criterion may be applied **(a)** numerically by recomputing under an instrument swap (→T1) or **(b)** structurally, arguing from construction where no recomputable pipeline exists (→T2). *"Tier honestly; never let (b) wear (a)'s clothes."*

**Nuance:** the ledger *does* record T2→T1 **upgrades** when a structural verdict is later
machine-confirmed. The no-promotion rule bars **claim-strength** promotion (a T3 result relabelled
T2), not **evidence-strength** re-tiering after new computation.

**Second axis — REFRACTION vs INVARIANT (the "engine kill-criterion", tomographic invariance):**
a quantity is a **REFRACTION** if its value moves under a legitimate change of instrument
(representation / normalization / convention / scale / window); an **INVARIANT (candidate)** if it
does not. Precedent kill: "universal 2π inversion" → representation-specific.

**Tier census across MANIFEST's 54 claim rows:** T1 (pure) 24 · T2 (pure) 14 · T2(known) 2 ·
**T3 (pure) 1** (the SU(3) closure attractor) · T4 (pure) 4 · T2/T3 2 · T1/T3 2 · T1/T2(known) 2 ·
T4/T2 1 · T2/T1 1 · T1(rung1)/T3(rung2) 1 · explicitly not claimed 1.

**Ledger status tags:** `QUEUED / IN-PROGRESS / KILLED / SURVIVED / SPLIT / BLOCKED`.

**Variant definitions flagged by the audit (all now fixed):** Σ redefined T3 as "conjecture" (M28);
`Critical_Line_As_Fibered_Object` labelled R=0.99 fits as T1 where T1 elsewhere means machine
precision (M40); `Three_Layer_Decomposition` §3 labelled a numerical perturbation table T2 (M30).

**Global assembly checks:** `acs_codebase` → **42 passed**; HP suite reproduces session figures
(phase demod R = 0.991; C9 zeros-vs-truth corr = 0.917). **Canonical seed `20260423`**;
**PDG v = 246.22 GeV**; zeros = Odlyzko's first 100,000.

**RC1** = "Release Candidate 1, the bundle's first consolidated claim-discipline pass";
**"RC1-scoped"** marks claims whose stated scope was fixed in that pass.

---

## 2. The MANIFEST claim ledger

### Paper A — Colour from Gravity
| Claim | Tier | Evidence |
|---|---|---|
| SU(3) closure attractor | **T3** | `src/paper_a/`, selection scripts (50k-sample numerical, **not a uniqueness theorem**) |
| Higgs quartic λ_φ = 2√3/27 | T2 | Koide projection; `extras/koide_clebsch_gordan.py` |
| α₂ = 0 (rep theory) | T2 | paper_a |
| β_c = 0 no-go (tree level) | T2 | `src/paper_a/betac_tan_beta.py` |
| tan β gauge-protected (CW 6→5 fails) | **T4** | `extras/phase51_tanbeta.py`, `phase50_vacuum.py` |
| N_gen = 3 (Jacobi truncation at BCH-3) | T1 | paper_a |
| γ = 0.274 (Barbero–Immirzi, Meissner) | T2 | `extras/barbero_immirzi_correct.py` |
| θ_QCD = 0, torsion ratio 0:1:4 | T2 | paper_a |
| θ₁₃ obstruction / TM1 PMNS | T2/T3 | `theta13_obstruction.py`, `tm1_pmns.py` |
| Riemann curvature = Layer-2 bracket; Schwarzschild ∇g=0, R_μν=0, K=48M²/r⁶ | T1 | `extras/riemann_curvature_palatini.py` |

### Paper B + HP knife suite
| Claim | Tier | Evidence |
|---|---|---|
| Wronskian ≠ Poisson (Leibniz fails by −fgh′) | T2 | `src/paper_b/wronskian_leibniz.py` |
| RH ⇒ stationarity | T2 | paper_b |
| von Koch stability | T2 | `renormalized_stability.py` |
| Berry–Keating smooth counting | T2(known) | `berry_keating_counting.py` |
| C5 arithmetic present (real 240 vs GUE ≈1) | T1 | `hp_never_synced.py` |
| Berry–Keating xp carries no arithmetic | T1 | `hp_xp_test.py` (xp-honest 0.71; circular injection labelled) |
| C6 sign + C7 von Mangoldt weights | T1 | `hp_signed_lfunction.py` (sign 100%, weight corr 1.00) |
| C8 character sign, quadratic L (18/18) | T1 | `hp_signed_lfunction.py` |
| C8′ complex-character phase (R = 0.99) | T1 | `hp_phase_test.py` (order-4 mod 5, order-6 mod 7) |
| C9 finite-prime orthogonality (corr 0.92) | T1 | `hp_c9_orthogonality.py` |
| Form/function label is frame-relative | T1 | `hp_form_function_relativity.py` |
| Witness census: ~4.8/5 independent instruments; exactly **TWO** robust FUNCTION faces (arithmetic 830σ, local-order 26σ); **no independent third face** | T1 | `hp_vantage_points.py` |
| Arithmetic-face harmonic ladder obeys p^{−k/2}: slope −0.533 vs −0.5, R²=0.98; abs. weight corr 0.998; GUE null slope +0.20. Necessary HP condition, **constructs no operator** | T1 | `hp_harmonic_ladder.py` |
| HP wall quantified: any H with spectrum {γ} must carry real orbit amplitudes (\|Im W\|/\|Re W\| = 0.0001 → β=1) **and** GUE repulsion (β=2.00 → T-broken) — opposite symmetry classes | T1 | `hp_operator_constraint.py` |
| Wall resolution class: constraints coexist exactly under an **anti-commuting antiunitary** (C H* C⁻¹ = −H, C²=−1); only chiral passes both (β=2.01, \|Im W\|/\|W\| ~1e-12); **β = codim − 1**. Class pinned; arithmetic realisation open | T1 | `hp_wall_resolution_class.py` |
| Repetition tower is 3 deep: rung-3 slope −1.015 (R²=1.00, p≤7); 33-line abs. weight slope +1.002, corr 1.000 | T1 | `hp_ladder_tower.py` |
| Ladder universal across L-functions with a χ^k twist on rung k; diagonal demod table; quadratic χ rung-1 sign flip 12/12 | T1/T3 | `hp_ladder_character_twist.py` |
| Hardened twist (~150 non-circular L-zeros): rung-1 R=0.99; k=3 parity confirmed. **HONEST NEGATIVE: rung-2 phase did NOT harden — stays at the demod floor (~0.26) even at 150 zeros** | T1 (rung1/parity) / **T3 (rung2)** | `hp_twist_hardened.py` |
| Commutator law ‖[ι,T]‖_k = mean_p \|Im χ(p)^k\| = 0 iff order(χ)\|2k — the self-dual locus is the commuting locus. Assembly is a forced topological sort faces≺ladder≺twist≺involution | T1 | `hp_ladder_character_twist.py` Part 3 |

> **Scope note (verbatim intent):** C5–C9 numerically exhibit the explicit formula (Weil–Guinand) and
> its Dirichlet generalization — **known theorems**. The suite is a falsification/calibration
> instrument, not a source of new theorems, and **constructs no operator.** Non-circularity: L-zeros
> are built from L(s,χ) via Hurwitz zeta, **primes never inserted**. "Selberg orthogonality" here is
> a finite-prime proxy.

### Paper C
| Claim | Tier | Evidence |
|---|---|---|
| Killing-orthogonality (Thm 4.1) | T2 | `killing_orthogonality.py` |
| Three-class spectral taxonomy (Thm 4.2) | T2 | `spectral_taxonomy.py` |
| ER=EPR algebraic correspondence | T2/T3 | `er_epr_algebraic.py` |

### Notes
| Claim | Tier | Evidence |
|---|---|---|
| N1 — IR lattice imprint is null vs PDG | **T4** | `test_lattice_imprint.py` |
| N2 — general grading selection theorem | T2 | `test_signature_selection.py` |
| N2 — G₂ exceptional-algebra counterexample | T2 | same |
| N3 — transition operator P_m; ker = Dirichlet characters | T1/T3 | `PRIME_GAP_TRANSITION_OPERATOR.md`, `data_zeros/cyclotomic_*` |
| FF06h — ∞/0 resolution-relative; N_δ[a,b] = N_{λδ}[λa,λb] exact (0/2×10⁵); invariant is width/δ | T1 | `test_scaled_invariance.py`. Scope: counting under resolution, **NOT set cardinality — Cantor untouched** |

### Issue #7
| Claim | Tier |
|---|---|
| TFIM exhaustive chain support 0/12 | T1 |
| Cross-model combined 1/12 | T1 |
| Long-range combined 5/12 | T1 |
| Exact joint chain support false | T1 |
| 4/3 identity family n = d+1 | T1 |
| **4/3 mechanism established under K1/K2** | **T4** |
| Section 9 gap→cone chain as general theorem | **— not claimed** |

### Framing transformer
| Claim | Tier |
|---|---|
| Torus normal is a genuine framing (T·U = 0 to 2.2e-16) | T1 |
| Tw + Wr = Sl, \|Sl\| = pq = 2 (two independent routes) | T1 |
| Frame loop is spinorial: σ = −1, nontrivial in π₁(SO(3)) | T2 |
| Parity law σ = (−1)^{Sl+1} = (−1)^{p+q} | T2/T1 |
| **Sl = 2 as the geometric origin of g = 2** | **T4** |
| Framed-loop geometry yields g ≠ 1 (successor test) | **T4/T2** — `moment_ratio.py`: g = 1 exactly for every closed curve |
| Magnetic helicity of this geometry = Φ²Sl | T2(known) — Moffatt 1969 |
| (2,1) is two Euler angles of one rotation | T1 |
| Framed curve ≡ one quaternion curve on S³ | T1/T2(known) |
| Four quaternion coords span the first Laplace eigenspace on S³, λ = −3, degeneracy 4 = (½,½) | T1/T2(known) |
| Transformer chain requires rational winding | T2 |

---

## 3. The Elimination Ledger

**Governing doctrine (verbatim):** *"**Append-only.** Strip-mine discipline: rank targets by
expected-space-collapsed per unit cost; weight toward kills aimed at our **own** load-bearing
claims. A landed kill credits the survivors by elimination — no proof required. Don't prove the gold
is there; remove everything that isn't."*

**Provenance note (2026-08-07, audit H3):** several kill scripts are cited at `/tmp/…` paths or with
no path; they ran on external session machines and were **not committed**. Those verdicts rest on
logged outputs quoted in the ledger — reproducibility standard **(b) structural/logged**, not (a).
Entries under `code/` are rerunnable.

### Target queue

| Target | Kill target | Verdict | Tier | Date |
|---|---|---|---|---|
| **Q1** | λ_φ, h̃/h, g₄, γ are representation-independent invariants | mixed: 2 KILLED/refraction, 1 SURVIVED, 1 SPLIT | T2 → **T1 upgrade** at OOS01 | 2026-06-06 |
| **Q2** | trinity-wasm BRA kernel beats TF-f32 | **KILLED (measured)** | T1 | 2026-06-06 |
| **Q3** | T_min = (2πe)^d/q as a real invariant | floor value SURVIVED at d=1; **scaling law FALSIFIED** | T2/T3 → **T4** | 2026-06-06 |
| **Q4** | ΔI ≡ RG c-function (FF06Σ Link 3) | **identity FALSIFIED as stated; fully closed** | T1+T2 | 2026-06-06 |
| **Q5** | remaining Hilbert–Pólya candidates | **class kills** (GOE, GSE, bare xp) | T3+T2 | 2026-06-06 |
| **Q6** | residual prime-orbit off-diagonal mechanisms | **KILLED** | T2+T3 | 2026-06-06 |
| **Q7** | PS gauge suppression clears the X-ray bound | **RESOLVED/SURVIVED** with decoupling caveat | T3+T2 | 2026-06-06 |

### The kills in detail

**Q1 — framework constants (the four-constant refraction table).**

| Quantity | As carried | Under instrument swap | Verdict |
|---|---|---|---|
| g₄ = g_L = g_R | 4/3 | → **2/3** under Tr(TᵃTᵇ) = ½δ vs δ | **SPLIT** — the *equality* is the invariant |
| γ (Barbero–Immirzi) | 0.274067 (SU(2)/half-integer) | → **0.190206** (SO(3)/integer), \|Δγ\| = 0.0839 | **KILLED / refraction** |
| λ_φ (Higgs quartic) | 2√3/27 ≈ 0.1283 | scales with Killing-form normalisation | **SPLIT** — Koide-projection *geometry* survives; "the physical quartic *is* 2√3/27" is scale-conditioned |
| h̃/h (Yukawa ratio) | 2/3 | d/d(ln μ) ≈ 0; normalisation cancels | **INVARIANT — the only full survivor** |

**Meta-pattern:** *"the relations survive; the bare normalization- or scale-laden numbers mostly
don't."*

**Q6 — residual prime-orbit off-diagonal mechanism, KILLED.** Explicit-formula dual periodogram
power ratios: fundamentals log 2,3,5,7 at ~3–4×10⁸; prime-power harmonics 5×10⁷–4×10⁸ (real,
suppressed by p^{k/2}); composites log 6,10,12,15 at **baseline noise**. **Structural reason, not
merely a null:** the dual carries weight only on Λ(n), supported on prime powers, so a sum-frequency
peak at log(pp′) is **forbidden by the support of Λ**. "Tunnel mapped empty."

**Q5 — Hilbert–Pólya class kills.** Unfolded spacing L²: **GUE 7.31e-2** ≪ GSE 1.72e-1 < GOE
2.26e-1 ≪ Poisson 6.52e-1; fitted β = **2.12**; variance 0.1600. **Kills** (i) any
real-symmetric/T-invariant candidate (GOE, β=1); (ii) any symplectic candidate (GSE, β=4).
**Berry–Keating xp:** reproduces the smooth RvM staircase to **<0.2%**, but has continuous spectrum,
no discrete eigenvalues, and does not encode the prime-driven S(T) → *"xp alone is the operator"*
**killed as sufficient**; "xp as the smooth skeleton" survives. Survivors must satisfy three
conditions **simultaneously**: unitary class (broken T) + the (T/2π)log(T/2πe) smooth count + primes
in the fluctuation spectrum.

**Q4 — ΔI ≡ c-function, FALSIFIED; target fully closed.** The most consequential kill in the repo.
- Instrument built (T1): a provably-monotone Casini–Huerta entropic c-function on TFIM/free-Majorana; critical c = 0.508 (exact ½, <2%); gate-validated to 1e-13–1e-15; M=400 critical fit c = 0.4884.
- **Structural damage (T2):** c is unbounded above (free boson c=1, N bosons c=N, bosonic string c=26), so ΔI ≡ c is dead unless ΔI is both unbounded and canonically normalized.
- **Three ΔI readings exist** and the external agent pinned the wrong one: (a) the AISO routing scalar δᵢ = 0.4·consistency + 0.3·divergence + 0.2·late_error + 0.1·recomposition ∈ [0,1]; (b) the physics ΔI = TE(F→G) − TE(G→F); (c) the mutual-information form.
- Under (b) the identity fails on **three structural mismatches**: (1) **sign** — c ≥ 0 but a TE difference is signed; (2) **fixed-point value** — on a symmetric fixed point TE(F→G) = TE(G→F) so ΔI = 0 while c ≠ 0; (3) **category** — TE is temporal/directed and needs a time series, c is static/spatial (Zamolodchikov; Casini–Huerta) — "not even defined on the same object."
- The only surviving reading (monotonicity) holds **only** under the MI reading, where it *is* the Casini–Huerta entropic c-theorem — established, not novel. The framework's literal TE-asymmetry ΔI is **undefined** on a static, time-translation-invariant ground state and vanishes by symmetry on a symmetric bipartition.
- **Verdict: "No reading is both novel and true."**

**Q2 — BRA speed superiority, KILLED (measured, T1).** Withdrawn projection was **489×**. Measured
(BRA f64 vs TF f32, ns/op): N=16 → 225.6/124.0 (**1.82× slower**); N=64 → 700.9/469.8; N=256 →
2505.5/1638.0; N=1024 → 8326.3/6074.5 (**1.37× slower**). Confound recorded honestly: f64-vs-f32
carries ~1.5–2× the work, so matched-precision parity is untested. **Determinism survives** —
integer and f64 paths bit-identical across runs (T1).

**Q3 — the (d,q) scaling law, FALSIFIED (T4).** The degree-two discriminator:

| L-function | d | q | framework (2πe)^d/q | standard 2πe·q^{−1/d} | N_actual below the framework floor |
|---|---|---|---|---|---|
| L(χ₋₄) | 1 | 4 | 4.27 | 4.27 | 0 (first zero 6.02) |
| L(χ₃) | 1 | 3 | 5.69 | 5.69 | 0 (first zero 8.04) |
| **Dedekind ζ_{ℚ(i)}** | **2** | **4** | **72.93** | **8.54** | **51** |

At d=2 the framework floor sits **above 51 actual zeros**, flatly contradicting T_min's own
definition. Overshoot ~**8.5×**. The two formulas coincide **only at d = 1** — precisely why the ζ
test survived: **the degenerate-case trap.** The floor *value* 2πe ≈ 17.0795 at d=1,q=1 remains an
analytic invariant (it is exactly the zero of the RvM main term).

**Q7 — neutrino/X-ray tension, RESOLVED with a decoupling caveat.** Required suppression
S < 2.5×10⁻⁵ → M_WR ≳ **16 TeV** (v_R ≳ 49 TeV); independent bounds already exceed this (LHC ~5–6
TeV; K_L → μe pushes v_R to hundreds of TeV). **Structural caveat — the real content:** clearing the
bound requires high v_R hence high M_R, so the sterile neutrino is **not keV-scale dark matter**.
*"Not a kill of the framework; a kill of the keV-DM reading."*

**2026-07-17 — EM-as-torsion-annihilator, KILLED both forms (F-6, T1/T4).** Exact rationals, no
floats in any decision. **Strong form:** the torsion sector is exactly Sym₀(4) (dim 9) and its
centralizer in 𝔰𝔩(4) is **{0}** — the full torsion sector annihilates *nothing*. **Weak form:**
Q = J3 + K3 + T_BL/2 is not in ker(ad_{T_BL}); the kernel is the 9-dim 𝔰𝔩(3)⊕𝔲(1) block, so even
the diagonal photon shares "torsion-null" with every colour direction. **Positive residue (new T1
invariant):** C = Σ_a ad†ad has exactly two eigenvalues on 𝔰𝔩(4): **4** (mult 9, symmetric/torsion)
and **6** (mult 6, Lorentz). C is block-scalar ⇒ no algebra-level coupling computation of this form
can single out an EM residue direction.

**2026-07-17 — Condensate-as-collapse, SURVIVED all four forms (T1 exact).** C1: ad_{T_BL}
semisimple over ℚ, exact spectrum {−4/3(×3), 0(×9), +4/3(×3)}; everything outside V₀⊕V₋ collapses
projectively onto the 3-dim V₊. C2: V₊ abelian, nilpotent of order 2 — terminal, cannot regenerate
structure. C3: in the fundamental **4**, V₊ is EXACTLY the three lepton→quark transition operators,
and the collapse rate +4/3 equals Δ(B−L) per transition (1/3 − (−1) = 4/3). C4: the flow-invariant
sector V₀ is EXACTLY 𝔰𝔩(3) ⊕ 𝔲(1)_{B−L} — *"the gauge structure is the furnace; it is never
slag."* Scope: linear hyperbolic flow on 𝔰𝔩(4,ℝ); "collapse" is **not** decoherence/measurement.

**2026-07-17 — Hypercone-through-the-slice, SURVIVED all three forms.** C1 (exact): the slice
x·D + y·S03 in the fermion **4** has sheets ±√(x²+y²) — a true double cone; codim 2 → β = 1.
C2 (exact): adding z·(i·A03) gives ±√(x²+y²+z²), codim 3 → β = 2. **"The repulsion exponent is a
DIMENSION COUNTER: β = codim − 1."** C3 (measured): the repo's 100k zeros give **β = 2.019**.
Scope: the cone is in *parameter* space, not physical space. **This result became the load-bearing
input to the HP wall resolution in PR #7.**

**2026-07-26 — Sl = 2 ↔ g = 2, KILLED** (T2 structural / T1 numerical). See
`notes-and-models.md` §4 for the full argument, the control table, and the literature.

**2026-07-26 — successor test, KILLED (g = 1).** μ/⟨L⟩ = q/2m ⇒ **g = 1 exactly for every closed
curve**. T2 no-go: no model with charge and mass circulating at uniform q/m gives g ≠ 1 by geometry.
**What it opens:** decouple where the charge sits from where the mass sits.

**Torsion condensation holonomy (T4, `docs/Torsion_Topological_Condensation_Analysis.md`).**
"Gravity as a torsional quantum condensate" → **FLAG: TOPOLOGICAL DISSIPATION**.
spectrum(ad_{T_BL}) = {0(×9), ±4/3(×3)} is real ⇒ exp(t·ad) is hyperbolic, not rotational; upper-node
scale factor at t = 2π is **×4348.5**, not ~1.0. dim(torsion ∩ 𝔰𝔩(3,ℝ)) = 5 of 8. **Integrity note
in that doc:** the prompt's "679-test validation set" does not exist (the machine-verified core is
42 assertions), and the prompt's expected outcome "Structural Coherence" was not reported because
the computed outcome was the opposite — *"Reporting Structural Coherence would have been
overclaiming — the framework's primary named failure mode."*

### The corpus-map failure register F-1 … F-23

| # | Claim | Mechanism |
|---|---|---|
| F-1 | ad³ = 2·ad for integers | requires λ = 1/√2 |
| F-2 | Universal 2π inversion | 𝔰𝔩(4) adjoint is hyperbolic |
| F-3 | Wronskian is a Poisson bracket | Leibniz fails by −fgh′ |
| F-4 | IR lattice imprint on zeros | z-scores null vs PDG |
| F-5 | Intrinsic chirality | bias vanishes under covariant conjugation |
| F-6 | Route A (Killing form selects signature) | Cartan ≠ parity involution |
| F-7 | Route C (stability selects signature) | all signatures give equal holonomy norms |
| F-8 | α₂ optional | forbidden by rep theory, T^AΦ = 0 |
| F-9 | β_c explanatory | tree-level equal-VEV no-go, mass-matrix rank |
| F-10 | Yukawa rescue of tan β | M_u − M_d = (h−h̃)(κ₁−κ₂) |
| F-11 | CW 6→5 parameter reduction | tan β gauge-protected flat direction |
| F-12 | "115-dim subalgebra" | turned out 𝔤𝔩(12) on proper saturation |
| F-13 | N3 uniform-X conjecture | falsified in tested range |
| F-14 | acid-to-water: assembly order selects outcome | greedy jams ~5.5 regardless of order |
| F-15 | order-asymmetry as stable signed lever | sign oscillates / decays with N |
| F-16 | shell-commensuration of the asymmetry | crossings not at centered-hex numbers |
| F-17 | sound & light = two octaves of one EM medium | 4/4 pre-registered tests fail |
| F-18 | particle/wave = infinite Mandelbrot self-similarity | flower/snowflake generative with characteristic scale |
| F-19 | "same gap": central-# residual = Higgs quartic residual | charge (θ cancels) vs coupling (magnitude) |
| F-20 | quartic residual is high-scale boundary | λ crosses λ_ACS once near EW (~130–180 GeV), runs down |
| F-21 | H = symmetrized duality | balanced involutions break GUE |
| F-22 | H via arithmetic diagonal perturbation | cosmetic when weak, breaks GUE when strong; no selection regime |
| F-23 | lag-1 beyond-GUE | gap 0.050 inside a 0.08 apparatus band |

⚠️ **Numbering conflict:** `key_parameters_ledger.json` uses a *different* F-numbering (its F-5 =
"θ₀-not-derivable-from-algebra", F-6 = "EM-as-torsion-annihilator"). The corpus map's F-5/F-6 are
intrinsic chirality / Route A. **Cite by claim text, not by F-number alone.**

### Still BLOCKED (on inputs/constructions, not on effort)
Q2 BRA (needs `bra_*` kernel signatures + the TF op it replaces) · Q3 (d,q) law (needs LMFDB zeros
at d>1, q>1) · Q4 finish (needs the FF06Σ Link-3 ΔI definition — though every reading is now
accounted for) · constant T1-upgrades (ACS derivation code under representation swap; RGEs for
h̃/h) · **Q5 full HP operator (needs a candidate construction).**

### External-label key (defined in-ledger after audit M7)
**OOS01** = the first out-of-session kill campaign (external run, 2026-06-06). **Antigravity** = the
external agent/machine session that executed it (verdicts reviewed and **re-tiered**, not accepted
as-is). **W2F** = that session's working-to-file log (not committed). **Category A\*** = its top
regression-severity class. **trinity-wasm** = a private codebase whose benchmark inputs are not
vendored (Q2 is externally-verified-only).

---

## 3b. The existing skill module — `docs/ACS_FRAMEWORK_SKILL.md`

**473 lines.** Name `acs-framework`; Version 1.0 (May 2026). Trigger list: "ACS, Palatini bracket,
Pati-Salam, grading selection, sl(4), Lie bracket, adjoint representation, Barbero-Immirzi,
Coleman-Weinberg, signature selection, 'work on the papers', 'what's still open', 'test this idea'."
Closing line: *"Nothing more is assumed. Nothing less is computed."*

**Structure:** 1 What This Skill Is · 2 The Adversarial Compression Methodology · 3 The Four-Tier
Hierarchy · 4 Current Framework State (4.1 Documents, 4.2 Parameter Ledger, 4.3 Proved Theorems,
4.4 Falsified Claims, 4.5 Open Problems) · 5 Scope Honesty Standards · 6 Computation Toolkit ·
7 Document Management · 8 The Palatini → Pati-Salam Pipeline · 9 Key Results in One Sentence Each ·
10 What To Do When Starting a New Session.

**Directives to quote verbatim:**

> **Adversarial compression cycle:** `CONJECTURE → EXPLICIT COMPUTATION → RESULT`. Survives ⇒
> compress to THEOREM (with proof); Fails ⇒ record as NEGATIVE RESULT (with computation); Partial ⇒
> record as OBSERVATION (with scope boundary).

> **Rules (never violate these):**
> - Never dress a conjecture in theorem language until the proof is complete
> - Negative results are first-class outputs, not failures — document the conjecture, the killing computation, the mechanism of failure, and the boundary it establishes
> - Every scope boundary must be explicit: what the result DOES and DOES NOT claim
> - Overclaiming is the primary failure mode — correct it immediately when found
> - When a "115-dimensional subalgebra" turns out to be gl(12) upon proper saturation, say so and explain why the earlier result was wrong

> "When reporting results, always state which tier. **Never let Tier 3 pass as Tier 2.**"

> §5.1 **Coleman-Mandula Rule:** "Any discussion connecting the (3,1) grading to Lorentzian
> signature MUST include the Coleman-Mandula constraint and the three bridging mechanisms
> (soldering, pre-geometry, CM evasion). **This is never optional.**"

> §5.5: "This is NOT 'we couldn't fix it.' It IS 'the PS gauge structure prevents perturbative
> fixing in the minimal sector.'"

> §7.2: "Never mix S_f and S̃_g without specifying which regime."

**§4.2 Parameter Ledger (Branch A).** ⚠️ Counting note: this ledger is **5 free + 2 calibrations =
7**; Paper A's `tab:branch-A-ledger` rolls v_R into calibrations and totals **6 (= 4 free + 2
calib.)**. Physical content identical; the 6-vs-7 discrepancy is audit item M3.
- **Free (5):** tan β (gauge-protected flat direction) · ρ_Δ ∈ (0, 8/9) · α₁ (|α₁| < 0.81) · v_R · μ_Δ
- **Calibrations (2):** m_τ, v = 246.22 GeV
- **Locked:** λ_φ = 2√3/27 · h̃/h = 2/3 · g₄ = g_L = g_R = 4/3 · 2ρ₁+ρ₂ = 16/9 · N_gen = 3 · γ = 0.274 · α₂ = 0 · β_c = 0
- **`StrickenBy{C1.4-D1, 2026-07-06}`** — the strike-annotation convention: α₂ and β_c were previously free; struck and relocated to Locked, replaced in the free table by v_R and μ_Δ.

**§4.3 Proved Theorems:** (1) SU(3) closure attractor — **annotated T3, numerical selection, not a
uniqueness theorem** (this is audit H1's fix) · (2) λ_φ = 2√3/27 · (3) α₂ = 0 · (4) β_c = 0 no-go ·
(5) Killing-orthogonality · (6) three-class taxonomy · (7) Wronskian ≠ Poisson · (8) RH ⇒
stationarity · (9) von Koch stability · (10) general grading selection.

**§4.5 Open Problems (6):** FeynRules/UFO export · Hilbert-Pólya operator · action principle for
S̃_g · L-functions extension (**open with partial repo-resident progress**) · SM from GL(4) fiber ·
ER=EPR correspondence. Corpus map adds O-7 (Barbero-Immirzi physical value) and O-8 (neutrino
tension, **since resolved**).

**§10 session-start protocol:** read the skill → check `ACS_Corpus_Map.md` and
`Elimination_Ledger.md` → ask which cluster to work on → apply adversarial compression → after any
paper edit: compile → check refs → run tests → bundle → after any new result: classify T1–T4 and
update the relevant paper.

---

## 4. The whitepaper's argument spine

`docs/ACS_Technical_Whitepaper.md` (115 lines), post-audit with inline tier annotations.

1. **Core axioms.** The primitive is **asymmetric transfer entropy** ΔI = T_{Y→X} − T_{X→Y}. Sign defines governance: ΔI>0 Form governs Function; ΔI<0 the reverse; ΔI=0 stable balance (attractor). **BCH–TE morphism:** ΔI(τ) = τ²[f,g] + O(τ³), so stable information flow ⇔ algebraic closure.
2. **Gauge sector.** The morphism on (e, ω) generates split real 𝔰𝔩(4,ℝ) (rank 15) = 6-dim Lorentz + 9-dim torsion. Among 50,000 sampled 8-dim subspaces, 𝔰𝔩(3,ℝ) is the only one achieving numerically exact closure — **T3, "a numerical selection result consistent with Dynkin's classification, not a proved uniqueness theorem"** (D < 10⁻¹⁴ vs > 0.49 for every alternative). Post-audit status note (OOS01/Q1, T1): the *relations* survive normalisation changes but the *bare values* are **refractions**.
3. **Spectral sector.** **Positional duality** — density (smooth RvM, no arithmetic) / local spacings (GUE universality) / positions (arithmetic, via Weil–Guinand): ⟨cos(γ log p)⟩ ∝ −ln p/√p. **The shuffle knife:** Form stays within 0.4–1.0σ of the surrogate null; Function collapses (~11,500σ). *The arithmetic content lives entirely in the exact level positions, not the spacing law.*
4. **Holographic resolution.** **Killing-orthogonality** — the boundary state space is the orthogonal complement of the bulk gauge orbit. Post-audit wording: this "provides an algebraic correspondence **consistent with** ER=EPR (T2/T3; the full holographic correspondence **remains an open problem, O-6**)" — it previously read "enforces."
5. **Deterministic AI Stack governance.** The **constraint-attractor cycle**: Constraint Set k —Solve→ Attractor —Promote→ Constraint Set k+1, with feedback via ΔI ≠ 0 corrections.

---

## 5. The corpus map's dependency spine

**The eight INVARIABLES** (constant across the whole corpus):

| # | Invariable |
|---|---|
| INV-1 | **ΔI is the primitive** — net transfer entropy between two mutually-constraining fields; its sign is the generator |
| INV-2 | **ΔI's 2nd-order Taylor coefficient = the Lie bracket [f,g]** — the BCH–TE morphism |
| INV-3 | **Form / Function ontology** |
| INV-4 | **bracket(Function, Function) → Form; holonomy(bracket, Function) → irreducible Form** — the operator-type ladder |
| INV-5 | **Inversion arc**: a system that solves a constraint becomes the constraint (ΔI flips sign) |
| INV-6 | **Tensegrity / nested codependence; self-similarity** — rigidity-matrix zero modes = gauge freedoms |
| INV-7 | **Adversarial compression + 4-tier honesty ledger** — negatives first-class; scope stated |
| INV-8 | **"Right locally, wrong globally"** (glass-box) — each lens valid in scope, over-reaching when universalised |

**Locked numerical invariants (derived, never refit):** g₄ = g_L = g_R = 4/3 · λ_φ = 2√3/27 ·
h̃/h = 2/3 · 2ρ₁+ρ₂ = 16/9 · γ = 0.274 · N_gen = 3 · θ_QCD = 0 exactly · torsion hierarchy 0:1:4 ·
K(T_BL,T_BL) = 32/3 · central charge 1/3 · m_H = 124.72 GeV.

**The VARIABLES — the only real degree of freedom is the substrate.** "The framework = Form
(constant); each domain = a Function realized within it. **The corpus is itself a Form/Function
object.**" Substrate ranges gravity → primes → QFT → trust.

**The single sentence (§8):** *"every paper varies only the substrate; the asymmetry, the
Form/Function cut, the inversion principle, the tensegrity geometry, and the honesty method are
invariant. The corpus is one object (the framework, Form) pointed at many domains (each a
Function)."*

**Predictions on record (falsifiable):** sterile neutrino 49 keV · θ_QCD = 0 exactly · torsion
hierarchy 0:1:4 · Higgs mass 124.72 GeV · the critical line as the unique center manifold.

**`ACS_Master_Index.md` is a historical snapshot (May 3, 2026)** indexing only the five documents
existing then. **MANIFEST supersedes it.** It does contain the recommended submission order: N2
first (standalone, highest novelty, smallest attack surface), then A, C, B, N1.

---

## 6. Changelogs — the substantive edits

**Paper A** (Apr 26, 2026; 40pp → 42pp). Added §5.5.1 **self-pruning of the bi-doublet Higgs
sector** — Phase 50 (α₂ = 0 because Φ ~ (1,2,2) is an SU(4) singlet so T^AΦ ≡ 0), Phase 51
(tree extremization ∂V/∂β = 2β_c v²v_R² cos 2β = 0 → tan β = ±1), Phase 52 (the identity
**M_u − M_d = (h − h̃)(κ₁ − κ₂)** forces M_u = M_d and |V_CKM| = 1 at equal VEVs). Added §7 CKM=I
reframing (structural, not a numerical coincidence). Corrected §6: old "5 free, 7 inputs, factor 3"
→ **6 inputs, 3.2× reduction**. Reconciled λ_eff (codebase used v = 246.0 giving a spurious 1.01%;
paper used PDG 246.22 giving 0.84% — codebase corrected). **Open items:** audit of h̃/h = 2/3
(matrix-level proportionality vs invariant-level trace ratio); CW analysis without β_c (2–4 weeks);
FeynRules/UFO export (1–2 months); HP construction; post-attractor ΔI < 0 in Paper C.

**Paper B** (v2M 17pp → extended 26pp). Three entirely new sections: **§8 Tartini-Tone
Characterization** (Montgomery R₂ at N=5K; Rudnick–Sarnak R₃ at N=50K, RMSE 0.051, corr 0.99;
Fourier-dual peaks incl. 2⁶=64; synthesis — the coupling is **Fourier-dual, not resonant**);
**§9 L-Function Generalisation** (χ₄ 100% sign accuracy on 19 peaks; F_ζ ± F_L decomposes primes by
residue class 15/15; Dedekind ζ split/inert 5.7×); **§10 Hilbert-Pólya Constraint Specification**
(C1–C9; GUE necessary but not sufficient, 40× distinction; **target sharpened** from "find H with
spectrum γ_k" to "find H with Tr(cos(ωH)) = the prime explicit formula AND GUE statistics").
Sections 1–7 preserved exactly. **Outstanding: replace placeholder figures.**

**The July 2026 acoustic-consistency revision** (across Paper B and the monograph): §8.4 already
said Fourier-dual-not-resonant and the cross-species difference-tone channel was falsified, but the
"Acoustic structure" subsection and "Geometric Vision" appendix still described resonance and "in
tune." Reframed: **intra-species** combination tones γ_k ± γ_j are real zero–zero mixing;
**cross-species** the explicit formula is a **cancellation identity**; **RH = balance, not tuning**
("perfectly in tune" → "in perfect balance"). *No numerical claim, theorem, or falsification record
changed.*

**Paper C** (Apr 25, 2026; 10pp → 13pp; Phases 48–55). Added §3.1 methodological note on epistemic
compression (Lakatos). Added §4 Algebraic Foundations — Thm 4.1 tr([X,Y]X) = 0 (3-line proof);
chirality hopping [H₁,A₀₁] = 2S₀₁; the three ambiguity numbers 14/15/19; Thm 4.2 Jordan–Chevalley
taxonomy with a Remark **explicitly correcting the universal-2π overclaim**; Prop 4.3
π_X([X,Y]) = 0 with a Remark flagging AdS/CFT as a research direction, **not** a derived consequence.

**Running logs.** `BUGFIX_LOG.md` (2026-07-23): **BF-001** (correctness) `export_daw_profiles.py`
set S_i = the global S for every isotope; fixed to log₁₀S_i = log₁₀P_extracted − log₁₀P_model,
verified 14/14. BF-002 readonly-tuple typecheck. BF-003 absolute authoring path in `source_json` →
repo-relative. BF-004 schema key alias. Plus a PASS table (`ACS_MEMO=0` vs `1` identical).
`EFFICIENCY_BENCHMARK_REPORT.md`: ribbon warm speedup **81.01×**, Gamow cold→warm **14.38×**, BIE
single-point **7284.41×**; explicit RC1 scope — *"does not claim physical engine efficiency,
alpha-decay accuracy, or uniqueness of the density-engine metaphor."* `palpha_audit_log.md`:
JSON↔TeX reality check **PASS** at ±0.0002 across 11 metrics; the Gamow Robin BC does **not** improve
global-S RMS vs the Dirichlet box (Δr = −0.00001); the extended 29-isotope catalog **degrades** the
fit (LOO 0.286 → 1.355) though coefficient signs are preserved.

---

## 7. The editorial audit (2026-08-07)

887 lines. Full-corpus review. Framing: *"these are editorial-consistency findings, not scientific
verdicts"* — each is a place where two documents disagree, a citation does not resolve, a tier label
is inconsistent with the tier rules, or wording overclaims relative to recorded status. Severity:
**high** = affects credibility/reproducibility of a load-bearing claim; **medium** = an inconsistency
a careful reader will trip over; **low** = polish. Every item carries a **Resolution** line.
Totals: **8 high + 48 medium + 51 low = 107** (the commit message says "99 medium/low" — that's
48 + 51).

### The 8 high-severity findings (fixed in PR #11)

| # | File | Finding |
|---|---|---|
| **H1** | `ACS_FRAMEWORK_SKILL.md` | §4.3 lists the SU(3) closure attractor as proved theorem #1 while MANIFEST tiers it T3 — **a direct violation of the skill's own rule.** *Fixed: annotated T3 numerical selection.* |
| **H2** | `ACS_Technical_Whitepaper.md` | No tier labels; §2.2 says 𝔰𝔩(3,ℝ) "is the unique subalgebra"; §2.3 presents λ_φ and γ as "Physical Invariants" though OOS01/Q1 machine-confirmed both as REFRACTIONS. *Fixed.* |
| **H3** | `Elimination_Ledger.md` | Kill-test code cited at `/tmp` paths absent from the repo — **breaks the framework's own T1 standard.** *Resolved by disclosure.* |
| **H4** | `Holographic_Spectral_Inversion.tex` | Order-counting error in the central inversion theorem (Step 3 displays the first-order coefficient at ε²). *Fixed.* |
| **H5** | `Palatini_Gauge_Attractor.tex` | Load-bearing citations point at `thm:gravity-acs`, which contains no Atiyah-Singer statement, no D_T, no chiral zero-mode result. *Fixed: repointed at §6.* |
| **H6** | `Riemann_Spectral_Critical_Line.tex` | The central claim is called "Conjecture T4-prime" in the abstract and "Theorem T4-prime" in §4, resting on numerically estimated constants and an **unproved minimum-gap bound**; Open Problems then lists it as "Confirmed." *Fixed: made explicitly conditional.* |
| **H7** | `One_Mechanism_Many_Forms_Sigma.tex` | **Status contradiction on the corpus's central claim.** Σ carries Link 3 as the conjecture on which the whole synthesis is conditional; the Elimination Ledger retires exactly that claim as T4-as-stated. Neither cited the other. *Fixed: dated reconciliation note.* |
| **H8** | `The_Reversible_Flattening_Process_Record.tex` | Reproduction-appendix scripts do not exist anywhere in the repo. **"The reproducibility promise ('all numerical claims reproduce under seed 20260423') cannot be exercised from the repo as shipped."** *Resolved by disclosure.* |

### The 48 medium findings — categories
1. **Cross-document count/label contradictions** — free-parameter count 7 vs 6 (M3); open-problem count 6 vs 8 (M5); FF06f assigned to two papers (M1); verification-suite size 76 vs 57 scripts (M22); torsion-tier count three-vs-two-vs-0:1:4 (M19); "nine of eleven" vs a 9-row table with 7 within 2σ (M20).
2. **Tier-discipline stretches** — a theorem part proved "numerically" (M37); `prop:selection` asserting uniqueness on 100 samples (M14); `prop:chirality` claiming "iff" from a 0.5-resolution grid scan (M15); `thm:acs-DI` conceding informal BCH convergence (M16); statistical fits labelled "decisive (T1)" (M40); "the exact half-life" where P_α is data-extracted (M43).
3. **Overclaim relative to recorded status** — "enforces the ER=EPR correspondence" vs O-6 open (M6); "these are not analogies; they are direct mappings" (M8); "reused verbatim" for a different functional (M33).
4. **Broken cross-references** — "Theorem C of Paper A", "Paper A §6.8", "Lemma 2.5 of [Wallace2026a]" (M17); tensegrity content attributed to Paper A when it lives in Paper C (M23); off-by-one section headings (M25).
5. **Unresolvable/private artifacts** — companion `.md` files that don't exist (M26); private OmniForge/AISO source (M29); `Aiso_build_artifacts/…` (M41); undefined labels OOS01/Antigravity/W2F/trinity-wasm (M7).
6. **Session-relative provenance** — F-14…F-23 attributed to "(this session)" with no date or artifact link (M2).
7. **LaTeX/build defects** — `\renewcommand` on an undefined macro (M10); drifted hardcoded numbers (M11); an internal WO-03 work-order comment left in source (M34); a title promising Clifford content the body never contains (M35).
8. **Terminology slips** — "non-associative" where "non-commutative" is meant (M27); a grade "SEAM" not in the defined scheme (M31); `g_weak` in a colour-confining derivation (M42); a fit whose stated crossing (~50) disagrees with its own constants (~35) (M48); a table contradicting the proposition it illustrates (M32).

### Retained by design (not fixed)
L9, L15 — personal acknowledgements kept as the author's voice · L39 — the RPG/DAW framing kept as
the note's declared RC1-quarantined style · L48 — the closing incantation kept as interpretive-coda
style. **Resolved by replication:** L31 — the Issue-7 single-machine SHA anchoring answered by the
Linux x86_64 rerun (`docs/issue7_linux_replication/`).

---

## 8. Licensing — this is NOT open source

**Root `LICENSE` — Sovereign Integrity Protocol License (SIP License v1.1).** © 2026 Brad Wallace,
Independent Researcher. Every doc file carries the banner "Co-governed and enforced under the SIP
License v1.1."

**Permitted, free, perpetual, worldwide, royalty-free:**
- **Personal Use** — any individual or immediate family, non-commercial. *"Individual and family use is always free."*
- **Educational Use** — schools, universities, teachers, students, self-learners, **free when no financial gain is derived from the Work itself**. *"Self-study is always free."*
- Use, study, modify, run; create and distribute derivative works for Personal/Educational Use, **provided the original copyright notice and license are retained**.

**Expressly prohibited without a prior written commercial license:** any Commercial Use, cloud
deployment, SaaS, secondary redistribution, or any use producing Financial Gain. "Commercial Use" is
defined broadly — revenue, profit, or commercial advantage; hosted platforms; redistribution for
fee; **consulting services**; product development; **training courses sold for money**; any
derivative sold or licensed for profit. Schools deriving Financial Gain (paid courses,
certification, consulting) **must** obtain a commercial license.

**Commercial terms:** negotiated per use, plus a **5% default royalty on gross revenue**, payable in
perpetuity to the Licensor and their successors/heirs; survives transfer of rights.

**Automatic penalties for Unlicensed Use** (immediate, non-negotiable, perpetual): a **4.2%
"distrust fee"** of gross profit ("cannot be waived, reduced, or renegotiated") **+ 4.2%** to
public-infrastructure projects "as reparation to the public good." The combined **8.4%** attaches
**to the product itself** and follows it in perpetuity — surviving bankruptcy, sale, transfer, or
dissolution. Any unlicensed commercial use "constitutes a knowing, willful violation," causing
**automatic, immediate, irreversible forfeiture of any defense of good faith, innocent infringement,
or fair use.** Closing note: *"not affiliated with the MIT License or any other standard
open-source license."*

**`papers/LICENSE-PAPERS.md`:** everything under `papers/` — **including all LaTeX source and
compiled PDFs** — is governed by the root SIP License.

**Practical read for downstream agents:** reading, citing, studying, and reproducing the
computations is free; anything touching revenue — including consulting, paid courses, hosted
services, and any derivative product — requires a prior written license, and using it without one
triggers an automatic, product-attached, perpetual 8.4% obligation.

**`CITATION.cff`** (CFF 1.2.0, `type: software`, released 2026-08-07): title "ACS Framework
(Asymmetric Codependent Systems)"; author Wallace, Brad — Independent Researcher; keywords include
**falsification** and **verification**. The abstract advertises the governance system itself.

---

## 9. Open problems the repo flags against itself

### Formal (corpus map O-1…O-8 / skill §4.5)

| ID | Problem | Status |
|---|---|---|
| O-1 | Hilbert–Pólya operator H | **Characterized, not solved.** Must simultaneously be unitary-class (broken T), reproduce (T/2π)log(T/2πe), and carry primes in the fluctuation spectrum. GOE/GSE killed; bare xp killed-as-sufficient. Resolution class pinned to the anti-commuting antiunitary (β = codim − 1); arithmetic realisation open. **BLOCKED on a construction, not on data.** |
| O-2 | FeynRules/UFO export | Engineering, ~1–2 months |
| O-3 | Action principle for S̃_g | Variational theory ("Route B completion") |
| O-4 | L-functions extension | **Open with partial repo-resident progress**; further closure rests on an external note not in this repo |
| O-5 | Full SM from GL(4) fiber | Conceptual breakthrough |
| O-6 | ER=EPR correspondence | Conceptual breakthrough; the whitepaper §4.1 explicitly defers to this |
| O-7 | Barbero–Immirzi physical value 0.2375 | Needs a **global** singlet projection on the multi-puncture tensor product, NOT a local degeneracy removal |
| O-8 | Neutrino tension | **RESOLVED** (Q7) with the decoupling caveat |

### Standing scope-honesty caveats (skill §5 — "Must Always Be Stated")
The Coleman-Mandula rule · the exceptional-algebra boundary (cluster coherence holds for A/B/C/D,
**fails for G₂** — always state the factorization condition) · the Barbero-Immirzi gap · the
neutrino tension · tan β protection.

### Reproducibility gaps the repo flags against itself
- Ledger kill scripts at `/tmp` are not committed → those verdicts are standard **(b)**, not recomputable (H3).
- `later_FF06_series` reproduction-appendix scripts do not exist; only `*_disp.py` display copies (H8).
- Issue-7 float scripts remain **single-platform SHA-anchored** (macOS 15.3.2 arm64 / Python 3.14.6 / NumPy 2.5.0); the pipeline retains **`PASS_WITH_CAUTION`** for exactly this reason. The Linux replication establishes a **tolerance-based** cross-platform anchor (decision-level identical, floats to ~1e-12) but `verify_issue7_pipeline.py` was not exercised to completion there.
- The Antigravity feed package's `verification_report.json` was generated on a private machine (2026-07-02, overall_status PASS, core pytest 42 passed in 1.80s).
- Engineering-side claims (OmniForge/AISO source, trinity-wasm bench) rest on private source.
- `Mobius_Screw_Electron.tex` §4.2 records that the α⁻¹ ≈ 137.036 estimate **does not survive its own revision path**.

### Structurally open successor questions raised by kills
Decouple where the charge sits from where the mass sits (the only route past the g = 1 no-go) · find
the mechanism for "EM as degradation" in the representation where charges act, not the adjoint
algebra · define a static, positive, canonically-normalized ΔI if the c-function identity is to be
revived (the Casini–Huerta instrument stands ready) · supply an arithmetic realisation (orbits at
log p) for the pinned chiral resolution class.

### The sealed Yang–Mills pre-registration
`docs/PARALLEL_YM_SEALED_20260704.md` — a sealed, pre-registered mass-gap construction skeleton to
be scored against a collaborator's construction when it lands. **CLEAN (scoreable) C1–C6:** C1 Step 1
is trivial, all difficulty is transport (toy T1: single-plaquette SU(2), gap = 1.5g² + 0.01% at
strong coupling, truncation-converged 1e-13); C2 the proof is a **survival theorem**; C3 the
massless-gluon obstruction is **projection-class**; C4 **one-channel law** — the bound lives in the
0++ plaquette-plaquette correlation length; C5 the dangerous step is an **exchange of limits**,
explicitly named "the C1.1/T_min failure mode at proof scale"; C6 the result form is
**constructive**. **CONTAMINATED (excluded from scoring):** X1 refinement transport between nested
Wilson-type algebras; X2 the invariant-algebra pivot. *"Negative outcomes are first-class: a MISS
localizes where the two ends of the object disagree, which is joint-paper content either way."*
Checker: `scripts/ym_comparison_checker.py`.

---

## 10. ⚠️ The stale JSON ledger

`docs/ACS_Antigravity_Feed_Package/key_parameters_ledger.json` (last_updated 2026-07-17) still lists
`g_4`, `lambda_phi`, and `gamma_unconstrained` under **`locked_invariants`** at **T2**, which
contradicts the Elimination Ledger's OOS01 **T1 REFRACTION** verdicts on all three bare values. It
also uses a different F-numbering. **Treat the JSON as a partially stale agent-feed artifact;
MANIFEST + Elimination_Ledger are canonical.**

The feed package's `prompt_templates.md` contains three role templates that all instruct "Load the
ACS Framework skill from docs/ACS_FRAMEWORK_SKILL.md", enforce the adversarial compression cycle,
and end with "Do not overclaim or promote Tier 3 results to Tier 2."
