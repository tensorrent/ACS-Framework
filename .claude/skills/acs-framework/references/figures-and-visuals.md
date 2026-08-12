# Figures and Interactive Visualisations

---

## 1. ⚠️ CRITICAL: every checked-in figure PDF is a placeholder

**Verified independently.** All **27 PDFs** across `papers/figures/` (12) and
`papers/core_trilogy/figures/` (15) are **87,577 bytes each** and reduce to just **two MD5 hashes**:

- `eb258498205fd89e518c1df6e76720d8` — **24 files**
- `78214c6a67347a0ebaadd7f39e284b90` — **3 files** (`fig_flow_field`, `fig_variance_scaling`, `fig_wronskian_heatmap`, core_trilogy only)

Decompressing the content streams shows **all 27 are the same document** — a compiled multi-page
LaTeX *paper*, not a figure. Extracted text fragments read `sl(4,R)`, `⟨2,3⟩`, `h̃/h = 2/3`,
`T_{B−L} = diag(1/3,1/3,1/3,−1)`, `SU(5)`, `SO(10)` — i.e. a build of
**`papers/notes/Pythagorean_Lattice_Limits.tex`**. The two hashes differ in exactly **3,327 bytes**
inside one content stream — two near-identical builds of the same paper.

**Consequences:**
- **No real figure content exists in the repo.** Compiling any paper today would embed the Pythagorean-lattice paper 9–13 times.
- The 12 shared filenames are duplicated **byte-identically** between the two directories; `papers/core_trilogy/figures/` additionally holds the three Paper-B figure names.
- Every paper declares `\graphicspath{{figures/}}`. **Paper C has a graphicspath but no `\includegraphics` at all** — it is genuinely figure-free.
- All generator scripts write to `OUTDIR = "/home/claude/figures"` — an absolute path **outside the repo** — so no script here ever populates `papers/figures/`.

**Partially self-documented:** `docs/PaperB_changelog_extended.md:88` records "some have known empty
boxes — `fig_variance_scaling`, `fig_flow_field`, `fig_wronskian_heatmap` were missing in v2M too",
and lists "Replace placeholder figures" as outstanding work item 1. **The changelog does not note
that the other 12 are also placeholders.**

**If asked to fix figures:** regenerate from `code/acs_codebase/extras/generate_figures.py`,
`ricci_flow.py`, and `colour_geometry.py` after repointing `OUTDIR`; three (`fig_closure_attractor`,
`fig_torsion_tiers`, `fig_hero_nesting`) and the three Paper-B figures have **no generator at all**
and would need writing from scratch.

---

## 2. Figure inventory

| # | Filename | Used by (paper : line, width) | Generator |
|---|---|---|---|
| 1 | `fig_layers_cycle` | Palatini:480 (0.85tw); Form_Function:399 — `fig:layers` | `extras/generate_figures.py` FIG 6 |
| 2 | `fig_ricci_flow` | Palatini:878; Form_Function:793 — `fig:ricci` | `extras/ricci_flow.py:461` |
| 3 | `fig_closure_attractor` | Palatini:1087 (0.75tw) — `fig:selection` | **none** |
| 4 | `fig_selection` | Form_Function:1560 (0.65tw) — `fig:selection` | `generate_figures.py` FIG 2 |
| 5 | `fig_colour_weights` | Palatini:1199; Form_Function:1648 — `fig:colour-weights` | `generate_figures.py` FIG 1 |
| 6 | `fig_nuclear_geometry` | Palatini:1252; Form_Function:1701 — `fig:nuclear` | `extras/colour_geometry.py:344` |
| 7 | `fig_rep_gallery` | Palatini:1265; Form_Function:1714 — `fig:rep-gallery` | `extras/colour_geometry.py:281` |
| 8 | `fig_barbero_immirzi` | Palatini:1642; Form_Function:1994 — `fig:BI` | `generate_figures.py` FIG 4 |
| 9 | `fig_torsion_tiers` | Palatini:2646 (0.75tw) — `fig:torsion-tiers` | **none** |
| 10 | `fig_hero_nesting` | Palatini:2847 (0.92tw) — `fig:hero` | **none** |
| 11 | `fig_chirality` | Form_Function:1232 — `fig:chirality` | `generate_figures.py` FIG 3 |
| 12 | `fig_sign_reversal` | Riemann_Spectral:494; Form_Function:1270 — `fig:sign-reversal` | `generate_figures.py` FIG 5 |
| 13 | `fig_variance_scaling` | Riemann_Spectral:840 — `fig:variance` | **none** (documented placeholder) |
| 14 | `fig_flow_field` | Riemann_Spectral:937 — `fig:flow` | **none** (documented placeholder) |
| 15 | `fig_wronskian_heatmap` | Riemann_Spectral:978 — `fig:wronskian` | **none** (documented placeholder) |

### What each is meant to show

**1. `fig_layers_cycle`** — Two panels. Left: a 4-tier stacked-rectangle ladder with "acts on" arrows
(e^a_μ / T^a = de + ω∧e / R^{ab} / Bianchi) showing the strict resolution hierarchy — each layer acts
only on lower layers and produces a Form, not a Function. Right: a 6-node circular arrow diagram of
the constraint–attractor cycle T^a=0 → torsion activates → chiral modes → spinor bundle → 𝔰𝔲(3) →
confinement.

**2. `fig_ricci_flow`** — Six panels. Top: Ricci scalar R for the sphere (R>0), flat torus (R=0),
Poincaré disk (R<0). Bottom: Ricci flow from a "bumpy sphere" to a uniformised surface, with the
convergence curve showing **curvature variance reduced 41× in 800 steps**. "Ricci flow is the ACS
evolving toward information balance."

**3. `fig_closure_attractor`** — Closure-defect histogram for **2,000** randomly sampled 8-dim
subspaces of 𝔰𝔩(4,ℝ). 𝔰𝔩(3,ℝ) at **D = 1.4×10⁻¹⁶** (red line); minimum random defect **0.50** (gold
dashed). "The gap of 10¹⁵ … is consistent across 50,000 samples (not all shown)."

**4. `fig_selection`** — The monograph's smaller-N version of the same plot: **100** samples, none
below **0.54**. ⚠️ **Both #3 and #4 carry `\label{fig:selection}`** — the same claim at two different
sample counts and thresholds. Worse: the generator draws 100 uniform samples in [0.55, 0.78] with
`np.random.seed(42)` and an axvline at D = 0 — **the histogram is synthetic/illustrative, not the
actual sampled defects.**

**5. `fig_colour_weights`** — Weight diagram of the fundamental **3** of 𝔰𝔲(3): weights at (1,0) red,
(−1,1) blue, (0,−1) green, plus a hollow "White (0,0)" marker at the origin (the lepton). Axes h₁,
h₂ are the Cartan generators, **both in the torsion sector**.

**6. `fig_nuclear_geometry`** — Left: gluon exchange as root-vector displacements in colour weight
space; the three pairs (α₁, α₂, α₁+α₂) are the three torsion–Lorentz gluon pairs. Right:
representations stacked by quadratic Casimir C₂; confinement drives toward the singlet (C₂ = 0,
ΔI = 0).

**7. `fig_rep_gallery`** — Weight diagrams for the six lowest 𝔰𝔲(3) reps: singlet = point, quark
**3** = triangle, gluon **8** = hexagon, decuplet **10** = larger triangle. "The root vectors
connecting adjacent weights are the gluon exchange operators."

**8. `fig_barbero_immirzi`** — The partition function Z(γ) = Σ(2j+1)e^{−2πγ√(j(j+1))}. Z = 1 (dashed)
selects γ_ACS = **0.274** (red); the Domagala–Lewandowski value **0.238** (green, dotted); the 15%
gap. Generator sums half-integer j from 0.5 to 50 over γ ∈ [0.05, 0.8].
⚠️ **The two captions give different mechanisms for the same gap.** Paper A: "the nonlocal
correlations introduced by the **global singlet projection**" (SU(2) Chern–Simons). The monograph:
"a more restrictive counting that excludes integer-j contributions via the horizon **U(1) projection
constraint**." Both texts are in the repo; Paper A explicitly says the monograph's local mechanism
*fails*.

**9. `fig_torsion_tiers`** — All 15 generators of 𝔰𝔩(4,ℝ) under ‖[T_{B−L}, X]‖²: Tier 0 (zero
coupling, 9 generators including the colour 𝔰𝔲(3) block) vs Tier 2 (coupling 32/9, 6 generators
connecting colour and lepton sectors). Each antisymmetric A_{i3} with K = −16 is matched by a
symmetric S_{i3} with K = +16 ⇒ exact vacuum-energy cancellation. ⚠️ `Editorial_Audit:239` flags a
**three-way contradiction**: body text says "exactly three tiers", this caption says "two tiers", the
abstract advertises a 0:1:4 (three-value) hierarchy.

**10. `fig_hero_nesting`** — The paper's summary graphic: the ACS nesting chain end to end — gravity
→ curvature via the Palatini bracket → 𝔰𝔲(3) as the unique closure attractor → Koide projection and
Higgs potential → mass spectrum → three generations from Jacobi truncation → falsifiable predictions.
Plus the Branch A ledger: 2 calibrations, 1 forbidden (α₂), 1 tree-excluded (β_c), 3 free, **6 total
inputs** vs 19+.

**11. `fig_chirality`** — Left: spectral index vs lattice size; torsion-free gives index 0 at every
size, non-zero torsion gives a growing index. Right: |index|/N converges to **≈0.30**, consistent
with Atiyah–Singer for uniform torsion density. Generator hard-codes sizes [8,12,16,20,24,32] against
indices [16,40,72,120,176,320].

**12. `fig_sign_reversal`** — Four-bar chart of ΔI under f↔g swap on ℤ₁₆, exact integer arithmetic:
Uncoupled 0.0, Symmetric 0.0, Asymmetric (f=x², g=|x−8|) −1.19, Swapped +1.19. ⚠️ **The generator
plots ±1.19 while the paper text and glossary quote the automaton at ∓1.499.**

**13. `fig_variance_scaling`** *(never generated)* — Variance ratio Var[T₁₂](σ=0.6)/Var[T₁₂](σ=0.5)
with 50 Odlyzko zeros over three decades of X; data vs the predicted X^{0.2} dashed line, matching
to better than 2%.

**14. `fig_flow_field`** *(never generated)* — Tensor flow for γ₁ = 14.13. Left: at σ = ½ a closed
loop (pure rotation, no radial drift). Right: at σ = 0.7 an outward spiral. **This is the missing
visual for the "unique center manifold" result** — arguably the most load-bearing absent figure in
the repo.

**15. `fig_wronskian_heatmap`** *(never generated)* — W[φ_k, φ_j] at t=1, σ=½ for the first 20 zeros;
antisymmetric structure visible, no entry zero, checkerboard from difference-frequency sign
alternation.

### Figures generated by the codebase but referenced by no paper
`fig_russell_spiral`, `fig_quantum_acs`, `fig_devolution`, `fig_koide_rg_flow`, `fig_newton_qcd`,
`fig_mersenne_bridge`, `fig_colour_3d`, `fig_higgs_landscape`, `fig_higgs_sombrero` — all in
`code/acs_codebase/extras/`, none present as PDFs. Separately,
`code/hp_knife_suite/data_zeros/` holds four independent figure scripts (`disentangled_fig.py`,
`cyclo_figure.py`, `cyclotomic_fig.py`, `cyclotomic_7_fig.py`) unconnected to the paper figure set —
and all with the same `/home/claude/` hardcoded OUTDIR problem.

---

## 3. Interactive visualisations

### `visualizations/mobius_screw_framing_transformer.html` (49,590 B, 1,312 lines)

**Title:** "The Framing Transformer — Möbius-Screw Electron." Companion to
`papers/notes/Framing_Transformer_Spin_Parity.tex`, 26 Jul 2026.

An interactive **five-plate walkthrough** of the chain γ → U → Sl = Tw + Wr → F: S¹→SO(3) →
q: S¹→SU(2), built to show "the two separate places where the number 2 turns out to do no work at
all." **Each plate is a live computation, not a static illustration.**

1. **The shape** — draggable 3D (2,1)-torus curve with its ribbon, faces coloured separately so the strip's two-sidedness is visible; a moving triad shows T, U, V = T×U. An `a/R` slider (default 0.300) and a **Throat** button sweep a/R → 1, carrying the donut continuously into the funnel-with-a-throat of the tornado reading; ρ_min = R − a, so the throat closes as a → R. Live readouts hold **Self-linking −2.000000** ("unchanged across the whole sweep") and **Holonomy σ = −1** ("spinorial, throughout").
2. **Călugăreanu–White–Fuller** — drag the aspect ratio and watch Twist (−1.033761) and Writhe (−0.966239) trade against each other while **Tw + Wr stays pinned at −2.000000** from a fat-hole donut to a closed funnel. Teaching point: Tw and Wr are *geometry* and move; only Sl is *topology*. "Donut and vortex are one framed loop, related by a deformation, and the topology cannot tell them apart." **Honest note on the page:** past a/R ≈ 0.9 the last decimal drifts by a few parts in 10⁶ — quadrature error as the curve crowds the axis, not the invariant moving.
3. **The lift** — plots q(φ) = [cos(φ/2) + k sin(φ/2)]·[cos(φ/4) − j sin(φ/4)] across φ ∈ [0, 4π], landing on q(4π) = (−1,0,0,0). The longitude factor returns to +1 and contributes nothing; the sign is carried entirely by the meridian half-angle.
4. **The parity law (the kill plate)** — a control family of round circles (writhe exactly 0) with n framing twists. Step n and watch σ flip on every increment. **The n = 0 row is the one that kills Sl = 2 ↔ g = 2**: an untwisted circle is spinorial in exactly the same sense as the Möbius screw with |Sl| = 2 — "whatever produces the double cover here, it cannot be the number 2, because 0 does it too." Holonomy is computed by lifting [T, U, T×U] to quaternions with sign continuity, **not** by applying the parity formula: *"the formula is what the measurement produces."*
5. **The successor test / verdict** — computes μ against ⟨L⟩ to get a dimensioned g that *can* fail; both moments are proportional to the same vector area, so g = 1 and "the same 2 cancels again." Closes with what is falsified (T4) and what survives.

**Engineering.** Fully self-contained — **no CDN, no webfonts, no network requests**. Every number is
computed in-browser from the same formulas as `code/framed_unknot/framing_transformer.py` and agrees
to six decimals. The writhe is a **live Gauss double integral over 300 samples**, not a lookup —
*"the invariance you see is computed, not asserted."*

### `visualizations/acs_q_plane_confinement_simulator.html` (105,872 B, 2,249 lines)

**Title:** "ACS Q-Plane Confinement Simulator." A real-time 3D/2D toy dynamical simulator of two qq̄
pairs under a parameterized string-tension law **T(d) = k·d + c/(d+ε)**, with inter-pair coupling
driven by centered neighbour strain and a snap/confinement-break criterion. Its self-description is
blunt: ***"Parameterized toy … Not QCD."***

**Controls:** separation d per pair · tension model k (0.15), c (2.0), ε (0.5) · snap & memory
(d_ref → T_snap = 16.0; two snap modes: `T(d) ≥ T_snap` or strain integral ≥ max; strain max 3.0;
strain decay λ 0.4/s — strain integrates T/T_snap against the **locked** snap value only) · noise
(display vs force) · motion (wobble damping; inertial d, τ = 0.50 s) · **pair interaction** in three
coupling modes — **Amplify** T×(1+α·ñ), **Oppose** T×(1−α·ñ), **Threshold-shift**
T/(T_snap·(1−α·ñ)), where ñ = neighbour strain/max − 0.5, factor clamped to [0.5, 1.5], α = 0.80 ·
phase map / density visualisation (per-pair toggles, halos, difference A−B and symmetric-diff modes,
dominance threshold, contours and contour history, cause attribution tension/strain/both, Freeze
density, Clear frozen, Reset overlays; breaks recorded as causal snapshots with ×/○ markers faded by
id, ~0.5 s replay, click-to-probe) · **presets** Stable (α=0.2, λ=0.8, oppose) / Cascade (α=0.7,
λ=0.2, amplify) / Oscillatory (α=0.5, λ=0.5, amplify) · Pause / Step / Step×10 / Clear ghost with a
live stats panel.

**Two caveats, both documented in `visualizations/README.md`:**
1. ⚠️ **It requires network access.** The page loads three.js 0.128 and OrbitControls from `unpkg.com` via an import map (lines 8–11 and 225), so it renders **blank offline or behind a CSP blocking third-party scripts**. The README gives the fix: vendor `three.module.js` and `OrbitControls.js` locally and rewrite the import map to relative paths. This makes it the one artifact in the repo that would **not** work as a self-contained Artifact without vendoring. (The CDN dependency was disclosed in PR #8.)
2. **It is explicitly non-load-bearing:** "an illustrative visualiser, not a verification artifact: nothing in `MANIFEST.md` depends on it, and it computes no tiered claim." This stands in deliberate contrast to the Möbius page, which *is* pinned to a verification script to six decimals.
