> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# MANIFEST — ACS Complete Bundle

Core bundle assembled 2026-06-27; sections below the core (Issue #7, Flag
Condensate, framing transformer) were appended later and carry their own dates.
Seed `20260423`. All code referenced was executed at the time its section was
written.

## Verification hierarchy (tiers never promote)

> **T0 added 2026-08-30.** T1 has always meant *a script ran and asserted* — which is
> weaker than "machine-verified" sounds: a sympy assertion is sympy agreeing with itself.
> A kernel-checked proof is categorically different and gets its own, strictly stronger
> tier. **No existing claim changed tier**; T0 is earned by new evidence, not promotion.
> Exactly one proposition holds it so far — see `code/constraint_projection/lean/`.

| Tier | Standard |
|------|----------|
| **T0** | Machine-**checked** — kernel-verified by a proof assistant, axiom dependencies disclosed (added 2026-08-30) |
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
| notes/Adjoint_Clifford_Signature_Selection | N2 | grading-selection theorem |
| notes/Prime_Gap_Transition_Operator | N3 | prime-gap transition operator |
| methodology/Spectral_Rigidity_Shuffle_Knife | — | the discriminant itself |
| methodology/Form_Function_Relativity | FF06g | the form/function label is frame-relative (companion to FF06e) |
| methodology/Scaled_Invariance_of_Infinity_and_Zero | FF06h | ∞/0 as resolution-relative counting labels; joint-scaling invariant is width/δ (companion to FF06g) |
| notes/Critical_Line_As_Fibered_Object | — | the critical line is the two-sided SEAM (prime/Euler face ↔ zero/Hadamard face joined by convolution = explicit formula), NOT a flattening; one object in three verified descriptions — convolution seam law, s↔1−s reflection (commutator [ι,T]), Paper C ER=EPR non-traversability |
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
| Witness vantage-point count: ~4.8/5 independent instruments; exactly TWO robust FUNCTION faces (arithmetic 830σ + local-order 26σ); no independent third face — candidate tones are von-Mangoldt harmonics or the theory-nulled difference-tones | **T1** | `hp_knife_suite/hp_vantage_points.py` (effective-rank + jitter-response independence, seed 20260423) |
| Arithmetic-face harmonic ladder obeys the p^{−k/2} trace-formula weight: k=2/k=1 line ratio = p^{−1/2} (log-log slope −0.533 vs −0.5, R²=0.98; abs. weight corr 0.998; GUE-marginal null slope +0.20) — the prime periodic orbits appear with r-fold repetitions at the standard amplitude (necessary HP-operator condition, constructs no operator) | **T1** | `hp_knife_suite/hp_harmonic_ladder.py` (100k zeros, seed 20260423) |
| Hilbert-Pólya wall quantified (constructs NO operator): any H with spectrum {γ} must carry real orbit amplitudes (|Im W|/|Re W| = 0.0001, T-even → β=1) AND GUE repulsion (measured β=2.00, slope 2.999 → T-broken) simultaneously — the two constraints pull to opposite symmetry classes, which is why the problem is open. Stated as measured numbers, not a slogan | **T1** | `hp_knife_suite/hp_operator_constraint.py` (100k zeros) |
| Wall's resolution class: the two constraints COEXIST exactly under an ANTI-commuting antiunitary (C H* C⁻¹ = −H, C²=−1, verified exact on the hypercone active block) — pairs spectrum γ↔−γ (real witness) while keeping codim-3 degeneracy (β=2); commuting antiunitary forces the real slice (codim 2, β=1). Ensemble discriminator: only chiral passes both (β=2.01, \|Im W\|/\|W\|~1e-12); GOE fails both, GUE fails realness. β = codim − 1 (companion hypercone test): the line is a slice of the cone. Class pinned; arithmetic realisation (orbits log p) remains open | **T1** | `hp_knife_suite/hp_wall_resolution_class.py` (seed 20260423; companion: `test_conjecture_hypercone_projection.py`, torsion branch) |
| Repetition tower is 3 deep: rung k=3 (p³ line at 3 log p) obeys the p^{−(k−1)/2} ratio law at slope −1.015 (R²=1.00) on primes clearing background (p≤7 at 100k zeros); signal-gated absolute weight across 33 prime-power lines (k=1,2,3) gives slope +1.002, corr 1.000. Rung 3 background-limited beyond p≈7 (falsification-first) | **T1** | `hp_knife_suite/hp_ladder_tower.py` (100k zeros, seed 20260423) |
| Ladder is universal across L-functions with a χ^k twist on rung k: complex χ (mod 5 ord 4, mod 7 ord 6) give a DIAGONAL phase-demod table (rung 1 aligns under χ, R=0.99; rung 2 under χ², beats its off-diagonal — rung-2 absolute strength data-limited at ~55 zeros); quadratic χ give rung-1 sign-flip with χ(p) and rung-2 character-blind (12/12 across d=−35,−91,−104). The critical line is one geometry per L-function, χ painted frequency-by-frequency | **T1/T3** | `hp_knife_suite/hp_ladder_character_twist.py` (seed 20260423) |
| Hardened twist (~150 L-zeros, generated non-circularly via `data_zeros/generate_more_lzeros.py`): rung-1 χ-twist decisive at higher N (R=0.99); NEW k=3 parity confirmed — order(χ)\|2k gives commuting rungs (order-6 commutes on rung 3, order-4 not), mod-7 rung-3 phase resolves under χ³ (R=0.59). HONEST NEGATIVE: rung-2 phase did NOT harden — stays at demod floor (~0.26) even at 150 zeros, p²-line phase below the L-zero noise floor (stays T3) | **T1 (rung1/parity) / T3 (rung2)** | `hp_knife_suite/hp_twist_hardened.py` |
| Commutator law: [ι,T] of the functional-equation involution ι(χ)=χ̄ with the twist T is the family's order parameter — ‖[ι,T]‖_k = mean_p\|Im χ(p)^k‖ = 0 iff order(χ)\|2k, so the self-dual locus is the commuting locus (rung parity: order-4 χ commutes on rung 2 not 1; order-6 on neither). Assembly is a forced topological sort faces≺ladder≺twist≺involution | **T1** | `hp_knife_suite/hp_ladder_character_twist.py` (Part 3); `papers/notes/Critical_Line_As_Fibered_Object.tex` §3–§5 |

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
| N3 — transition operator P_m; ker = Dirichlet characters | **T1/T3** | `notes_verification/PRIME_GAP_TRANSITION_OPERATOR.md`, `hp_knife_suite/data_zeros/cyclotomic_*` |
| FF06h — ∞/0 counting label is resolution-relative; joint-scaling invariance N_δ[a,b]=N_λδ[λa,λb] exact (0/2×10⁵), invariant is width/δ | **T1** | `code/notes_verification/test_scaled_invariance.py` (interior of (1,2): 0,9,99,999,9999 as δ→0; A–D all PASS). Scope: counting under resolution, NOT set cardinality — Cantor untouched |

> **N3 fresh-eyes note (2026-06-27):** the transition operator's eigenvalues are bounded
> dynamical modes (|λ| ≈ 0.01–0.3), **not** an unbounded spectrum claimed to *be* the
> Riemann zeros. Its connection to L-functions is via the kernel (characters), not the
> eigenvalues. Recorded so the bundle does not overstate N3.

---

## Falsified claims ledger
`docs/Elimination_Ledger.md` — the living, append-only kill log. Early entries include
ad³=2·ad, universal 2π inversion, Wronskian-Poisson, IR lattice imprint, intrinsic
chirality, Route A/C signature selection, and CW 6→5; later campaigns added further
kills (T_min scaling, Sl=2↔g=2, EM-as-torsion-annihilator, and others). First-class results.

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
| `papers/notes/Mobius_Screw_Electron.tex` | Framed unknot $(2,1)$; $Sl=2\leftrightarrow g=2$ (model ID); capacitance estimate $\alpha^{-1}\approx 137.036$ | Design / estimate (RC1-scoped*) |
| `papers/notes/Framing_Transformer_Spin_Parity.tex` | Framing transformer of the same curve: CWF decomposition, $SU(2)$ lift of the frame loop, parity law | Computation (see claim table below) |
| `papers/notes/Klein_Foam_Monad.tex` | Klein-foam Monad postulation (TR-2026-FF06-KFM); cites Möbius + nuclear-decay notes; RC1-scoped* | Postulation / ontology |
| `papers/notes/Flag_Condensate_Nuclear_Decay.tex` | Phase-slip / Bogoliubov Gamow channel; Geiger–Nuttall and Hawking transfer-matrix fits as reported in-note | Companion programme note |

\* RC1 = Release Candidate 1, the bundle's first consolidated claim-discipline pass; "RC1-scoped" marks claims whose stated scope was fixed in that pass.

### Framing transformer — claim → evidence → tier

Paper: `papers/notes/Framing_Transformer_Spin_Parity.tex` ·
Code: `code/framed_unknot/` · Artifacts: `docs/framed_unknot_results.json`, `docs/framed_unknot_moment_ratio.json`, `docs/framed_unknot_one_object.json`
Verify: `python3 code/framed_unknot/framing_transformer.py` and `python3 code/framed_unknot/moment_ratio.py`

| Claim | Tier | Evidence |
|-------|------|----------|
| Torus normal is a genuine framing ($T\cdot U=0$ to $2.2\times10^{-16}$) | **T1** | `framing_transformer.py` |
| $Tw+Wr = Sl$, magnitude $\lvert Sl\rvert = pq = 2$ (two independent routes) | **T1** | twist/writhe integrals vs. Gauss linking integral |
| Frame loop is spinorial: $\sigma = -1$, nontrivial in $\pi_1(SO(3))=\mathbb{Z}/2$ | **T2** | closed-form quaternion lift, Prop. 1; confirmed numerically 3 ways |
| Parity law $\sigma = (-1)^{Sl+1} = (-1)^{p+q}$ | **T2/T1** | proved for torus curves; measured on twisted-circle controls $n=-2\ldots4$ |
| $Sl = 2$ as the geometric origin of $g = 2$ | **T4** | parity law: $Sl=2$ and $Sl=0$ are the same $\mathbb{Z}/2$ class, so the magnitude carries no spin information |
| Framed-loop geometry yields $g\neq 1$ (successor test) | **T4/T2** | `code/framed_unknot/moment_ratio.py`: $\mu$ and $\langle L\rangle$ share the vector area $A$, so $g=1$ exactly for every closed curve |
| Magnetic helicity of this geometry $= \Phi^2 Sl$ | **T2(known)** | Moffatt 1969; Moffatt--Ricca 1992 — the dynamo reading supplies the same integer, not a magnitude |
| $(2,1)$ is two Euler angles of one rotation, $A=R_z(\varphi)R_y(-\varphi/2)$ | **T1** | `code/framed_unknot/one_object.py` — matches the direct torus normal to $0.0\times10^{0}$ |
| Framed curve $\equiv$ one quaternion curve on $S^3$ (frame-Hopf) | **T1/T2(known)** | same; framing recovered from $q$ alone to $3.3\times10^{-16}$. Needham arXiv:1708.09124 §2 |
| Four quaternion coords span the first Laplace eigenspace on $S^3$, $\lambda=-3$, degeneracy 4 $=(\tfrac12,\tfrac12)$ | **T1/T2(known)** | same, measured $-3.00000$ per axis — the representation-theoretic home of spin-$\tfrac12$ |
| Transformer chain requires rational winding | **T2** | same — irrational slope never closes, so no $Sl$ and no $\pi_1$ class exists |

> **Scope:** the falsified row retires the *reading* of $Sl=2$ as producing the
> double cover; it does not touch the geometry, the winding numbers, or the
> $\lvert Sl\rvert=2$ computation of the Möbius-screw note, all of which are
> confirmed here. What survives is that the model's double cover comes from the
> odd meridian winding $q=1$ (the $\varphi/2$ half-angle), which is a
> $\mathbb{Z}/2$ statement and cannot by itself yield a magnitude.



---

## Constraint Projection Framework — submitted manuscript & audit (2026-08-29)

Manuscript (archived as submitted): `papers/notes/Constraint_Projection_Framework.tex`
Audit: `papers/notes/Constraint_Projection_Framework_Audit.tex` ·
Code: `code/constraint_projection/` · Artifacts:
`docs/constraint_projection_audit.json`, `docs/constraint_projection_full_verification.json`
Ledger: `docs/Elimination_Ledger.md`, 2026-08-29 (kill + second-pass correction)
Verify: `python3 code/constraint_projection/cpf_audit.py` (first pass, C1–C8)
and `python3 code/constraint_projection/cpf_full_verification.py` (full, V1–V9;
`--deep` recomputes the §7 contour integrals, ~4 min)

> **The manuscript is archived, not endorsed.** Every load-bearing claim is **T4**.
> It is kept because negatives are first-class outputs here, and because two of its
> claims are restatements of kills already in the ledger — which is itself a finding.
> Do not cite any result from it without the audit.

| Claim (manuscript) | Tier | Evidence |
|-------|------|----------|
| $\alpha^{-1} = \ln(8R/a)+1 = 137.035999171$ | **T4** | `cpf_audit.py` C1 — the stated inputs give $L\alpha=2$, i.e. $\alpha^{-1}=\tfrac12(\ln(8R/a)+1)$; a factor of 2 is dropped. Correction already published in `Mobius_Ribbon_Capacitance.tex` eq. `(alpha_ann)` |
| The cutoff $a$ is not free / zero free parameters | **T4** | `cpf_audit.py` C2 — four mutually exclusive requirements on $a/R$ spanning **117.4 decades** ($5.0\times10^{-1}$, $6.66\times10^{-59}$, $2.04\times10^{-118}$, $1.49\times10^{-39}$). One free parameter, fitted per section |
| Axiom III: $\exists\,\phi\in\mathrm{Diff}(\mathcal{M})$, $\phi_*=\left(\begin{smallmatrix}1&2\\0&1\end{smallmatrix}\right)$ | **T4** | `cpf_audit.py` C3 — clauses (1)–(2) force $\mathcal{M}=$ Klein bottle; $\mathrm{MCG}(K)=\mathbb{Z}/2\oplus\mathbb{Z}/2$ is finite, $\phi_*$ is parabolic of infinite order, and $\phi_*D\phi_*^{-1}\neq D$. **The axiom has no model** |
| $\mathcal{M}\cong$ Klein bottle from clauses (1)–(2) | **T2/T1** | `cpf_full_verification.py` V1 — Euler-characteristic census ($\chi(N_k)=2-k$, cover genus $h=k-1$, so $h=1$ only at $k=2$) + Smith normal form on the CW complex ($H_2=0$, $H_1=\mathbb{Z}\oplus\mathbb{Z}/2$). Correct and unique; the one piece of topology in the paper that does what it claims. ($H_2=0$ is implied by $w_1\neq0$, so that clause adds nothing) |
| $g=Sl=2$, $s=Sl/4=1/2$ | **T4** | `cpf_audit.py` C4 — restates the kills of 2026-07-26: $\sigma=(-1)^{Sl+1}$ (one parity bit) and $g=1$ exactly for every closed curve |
| $k(\varepsilon)=0 \Leftrightarrow$ RH $\Leftrightarrow \Omega_k=0$ | **T4** | `cpf_full_verification.py` V5 — the **defining integral** equals $2\pi N(T)/T \to \log(T/2\pi e) \to +\infty$ (residue theorem; ratio $\to 1$ numerically), real, positive and $\varepsilon$-independent, where the claimed sum is negative and $\varepsilon$-dependent. Separately the claimed sum is invariant under $\beta\mapsto1-\beta$, hence blind |
| $S_{\mathrm{LF}} = 2\sqrt2$ under the stated operators | **T3** | `cpf_audit.py` C6 — **arithmetically confirmed** to machine precision, Tsirelson-saturating |
| That sum is a Local Friendliness inequality / falsifies AOE | **T4** | `cpf_full_verification.py` V6 — the **LF bound on that expression is 4** (LP over all four $(a_1,b_1)$ branches; equals the no-signalling bound, since no $x{=}1$ term appears). $2\sqrt2 < 4$: **no LF violation**, and Tsirelson forbids one. The "$>2$" is the Bell local bound |
| $\rho_{\mathrm{DM}}=\frac{\hbar^2}{2m}\lvert\nabla\psi\rvert^2$ solves rotation curves without exotic particles | **T4** | `cpf_audit.py` C7 + `cpf_full_verification.py` V7 — the split contains $\tfrac12\rho v^2$ (double counted in $T_{00}$); it is **not** the Bohm quantum potential $-\tfrac{\hbar^2}{2m}\nabla^2R/R$, so the named mechanism is not the one used; and it needs $m\sim9.6\times10^{-24}$ eV, an ultralight scalar |
| $L_{\mathrm{IR}}=R^2/a\approx1.3\times10^{26}$ m; UV complete | **T4** | `cpf_audit.py` C2 — 19 decades off on the manuscript's own $a$, 79 on the corrected one; the corrected $a$ is $10^{-96}\,\ell_P$ |
| Axiom I: $\mathcal{B}$ non-amenable | **T4** | `cpf_audit.py` C8 — $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^\times$ is malformed; both standard readings are abelian, hence amenable, and $\mathbb{A}_\mathbb{Q}/\mathbb{Q}$ is compact with a Haar probability measure |

> ~~**New structural boundary established (the one genuinely new output).**~~
> **RETIRED 2026-08-30 — NOT NOVEL.** The statement (a functional detecting off-line
> zeros must be **odd** under $\beta\mapsto1-\beta$; anything factoring through
> $(\tfrac12-\beta)^2$ is blind) is **true but classical**. Davenport–Heilbronn (1936)
> is the standard witness that functional-equation symmetry alone cannot locate zeros;
> Weil's positivity criterion is the standard construction that beats it, with off-line
> zeros appearing as negative eigenvalues. Found in one query on the first use of the
> prior-art step. The reading of the manuscript's §7 stands; the *contribution* does not.

> **Second pass, 2026-08-29 — two of our own verdicts corrected, both understated.**
> The first pass settled three checks by structural argument rather than computation.
> Running them moved two verdicts, both *against* the manuscript: the LF bound is **4**
> (so §5 exhibits no LF violation at all, and Tsirelson forbids one), and §7's
> **defining integral** — never evaluated in the first pass — equals
> $2\pi N(T)/T\to\log(T/2\pi e)\to+\infty$, which is the Riemann–von Mangoldt smooth
> counting term, not the claimed sum. Method rule kept: **evaluate the object the
> target actually defines, not the object it claims that object equals.**
> V9 re-executes `code/framed_unknot/` rather than citing it: $Tw+Wr=-2.000000$,
> $\sigma=-1$ three ways, $g=1.000000$; both artifacts byte-identical.

> **Scope:** the audit assesses §§2–8 against the manuscript's own stated inputs.
> The interpretive material of §§1 and 9 (relational measurement) makes no
> falsifiable claim and is not assessed. Nothing here bears on authorship or priority.


---

## Where $g=2$ comes from — Lévy-Leblond run, and the measured anomaly (2026-08-30)

Code: `code/constraint_projection/wave_equation_gfactor.py` ·
Artifact: `docs/wave_equation_gfactor.json` ·
Ledger: `docs/Elimination_Ledger.md`, 2026-08-30
Verify: `python3 code/constraint_projection/wave_equation_gfactor.py` (~5 s)

Successor to the 2026-07-26 `Sl = 2 ↔ g = 2` kill, which closed on Lévy-Leblond
(Comm. Math. Phys. **6** (1967) 286) as its decisive external citation. That citation
had never been *run* here. It is now.

| Claim | Tier | Evidence |
|-------|------|----------|
| $\sigma_i\sigma_j=\delta_{ij}+i\epsilon_{ijk}\sigma_k$ | **T1** | W1, all 9 ordered pairs |
| $(\sigma\!\cdot\!\pi)^2=\pi^2-q\hbar(\sigma\!\cdot\!B)$ | **T1** | W2, symbolic with non-commuting $\pi_i$ |
| Lévy-Leblond linearization reduces to free Schrödinger | **T2(known)** | W3 |
| $g=2$ from $su(2)$ + linearization, **no relativity, no topology** | **T1/T2(known)** | W3 — no $c$, no Lorentz, no metric in the chain |
| $4\pi$ periodicity from $\pi_1(SO(3))=\mathbb{Z}/2$, **no manifold** | **T1/T2(known)** | W4 — $e^{-i(2\pi)\sigma_z/2}=-I$ |
| Tree Dirac gives the same $g=2$ | **T2(known)** | W5 — so $g=2$ diagnoses neither relativity nor topology |
| $a_e = 1.15965218059(13)\times10^{-3}$ | **T3(measured)** | Fan et al., PRL **130**, 071801 (2023) |
| Any "$g=2$ exactly" framework sits $8.92\times10^{9}\sigma$ from the data | **T1** | W6 |
| QED series validated by inversion against a published $\alpha^{-1}$ | **T1** | W7 — recovers 137.03599916622 vs Fan et al. 137.035999166(15), agreeing to 0.015× their uncertainty |
| QED vs independent $\alpha$: Rb 2.1σ, Cs −3.9σ; Rb vs Cs 5.5σ | **T3** | W8 — dominant discrepancy is *experimental*. Crude error propagation; sigmas indicative |
| **CPF completeness claim falsified experimentally** | **T4** | W9 — $Sl$ is an integer and the framework has no expansion parameter, so no route to $1.16\times10^{-3}$ at any order |

> **Scope.** W1–W5 are textbook; the contribution is that they are machine-checked rather
> than cited, and that they need no surface, framing, or self-linking number. The new
> result is W9: an *experimental* kill of the manuscript's completeness claim, independent
> of the 2026-07-26 kill of its geometric-origin claim. Lévy-Leblond and tree Dirac stop
> at $g=2$ too — that is no mark against them, since neither claims to be finished.

> **Method note.** The first run of W7/W8 omitted the mass-dependent QED terms
> ($2.75\times10^{-12}$, ~20× the experimental uncertainty) and compared against CODATA's
> $\alpha$, which is partly determined *by* $a_e$ — circular. Both were caught by
> **inverting the series for $\alpha^{-1}$ against a published anchor**, not by
> re-reading the algebra. Rule added to the ledger: *anchor every series to a number
> someone else published.*


---

## Triple-check — every load-bearing CPF claim by ≥2 independent methods (2026-08-30)

Code: `code/constraint_projection/cpf_triple_check.py` ·
Artifact: `docs/constraint_projection_triple_check.json` ·
Ledger: `docs/Elimination_Ledger.md`, 2026-08-30
Verify: `python3 code/constraint_projection/cpf_triple_check.py`
(`--full` adds the T = 74,000 sweep and the LF quantum search, ~15 min)

Two passes in two days each corrected a verdict that had been *reasoned about rather
than run*. This pass attacks every claim from methods sharing no machinery, validates
the instruments before trusting them, and scales past toy sizes.

| Claim | Methods | Tier | Result |
|-------|---------|------|--------|
| Axiom III clause (3) unsatisfiable | deck-centraliser (390,625 matrices) **+** `Out(π₁(K))` by word algebra | **T1/T2** | both give order 4, `{diag(±1,±1)}`; `φ_*` in neither |
| LF instrument is sound | 3 validations: local ⊆ LF, PR box ∉ LF, **quantum ∉ LF** (slack `3√3−4` at the maximally entangled state) | **T1** | all pass — the construction reproduces Bong et al. |
| LF bound on the manuscript's sum = 4 | LP over 4 branches **+** exact rational certificate (no solver) | **T1/T2** | 4 exactly; `2 < 2√2 < 4`, so Tsirelson forbids any LF violation |
| §7 integral → `2πN(T)/T → log(T/2πe)` | mpmath quadrature **+** exact closed form over 100k Odlyzko zeros | **T1** | ratio `0.999994` at T = 74,000 — **900× the original scale** |
| §7 gap between the two methods | truncation-window sweep | **T1** | converges upward and stabilises: it was quadrature error, not disagreement |
| §7 component decomposition | zero sum / pole / ψ separately | **T1** | only `2πN(T)/T` survives division by T; verified piece by piece |
| `g = 2` | Lévy-Leblond 4×4 (`det M = (2Em−p²)²`, rank 2 on shell) **+** `σ·π` squaring **+** Dirac reduction | **T1/T2(known)** | three routes, all bottoming out in `{σᵢ,σⱼ} = 2δᵢⱼ` |
| `α⁻¹ = ½(ln(8R/a)+1)` | symbolic solve **+** repo's published `eq. (alpha_ann)` **+** repo's BIE instrument re-run | **T1/T2** | agree to `1.2e-9` relative on `a/R = 2.039050e-118` |

> **No verdict moved on this pass** — after two consecutive passes that each corrected
> something, a third built specifically to break the results did not. But three of these
> claims had rested on a **single** method, and X2 on a construction built from a
> definition rather than from the source paper — the most fragile thing in the audit.
> It now carries three validations and an exact certificate.

> **Method rule added (third).** *An instrument is not trusted until it has been shown
> capable of failing.* Validate that it excludes what it must exclude before believing
> what it includes. Companions: *evaluate the object the target actually defines*
> (2026-08-29) and *anchor every series to a number someone else published* (2026-08-30).

> **Reproducibility note.** `ribbon_capacitance.py` was re-run this session and its
> tracked artifact regenerated **byte-identically** (sole diff: a trailing newline),
> independently confirming the repo's byte-reproducibility claim.


---

## Formal verification — first T0 result (2026-08-30)

Code: `code/constraint_projection/lean/LFBound.lean` · `.../lean/README.md`
Ledger: `docs/Elimination_Ledger.md`, 2026-08-30
Verify: `lean code/constraint_projection/lean/LFBound.lean` (~0.8 s, exit 0, **no Mathlib**)

Method adopted from Anthropic's Riemann-zeta pipeline (2026-08-10), which ends in a Lean
formalization passing a standard checker.

| Claim | Tier | Evidence |
|-------|------|----------|
| LF bound on the CPF §5 sum is exactly 4 | **T0** | `lf_bound_is_four` — attained by an explicit LF branch **and** an upper bound |
| `S ≤ 4` on any normalised non-negative behaviour | **T0** | `S_le_four` (needs neither LF nor no-signalling) |
| the witness is a genuine LF branch | **T0** | `star_is_LF` — **depends on no axioms** |
| the witness attains `S = 4` | **T0** | `star_S_eq_four` — **depends on no axioms** |
| the proof can fail | **T1** | 3 mutations, all REJECTED by Lean |

> **Axioms disclosed:** only `propext` and `Quot.sound`; **no `Classical.choice`**, so the
> development is constructive. No `sorry`, no `native_decide`.

> **Not formalised:** Tsirelson (`2√2`) and the Bell bound (2) remain external/numerical.
> The Lean file makes no quantum-mechanical claim.

> **Closed 2026-08-30:** that prior-art search was run. The claim is **not novel** —
> Davenport–Heilbronn and Weil positivity both predate it. Retired; see the ledger.
> The prior-art step is now standing practice: no result is logged as novel until a
> literature search has been run and recorded.


---

## Coherence audit — the CPF work used none of this repo's own methods (2026-08-30)

Ledger: `docs/Elimination_Ledger.md`, 2026-08-30

| Measurement | Tier | Evidence |
|-------------|------|----------|
| 4 CPF instruments, ~1,900 lines, **0 uses** of any repo-native method device | **T1** | grep for refraction / invariant / shuffle / surrogate / decoy / vantage / effective-rank |
| The manuscript's $\alpha^{-1}$ is a **REFRACTION** by this ledger's own criterion | **T2** | moves to $O(1)$ under model swap (annulus→conformal→BIE); the additive constant $+1\to-7/4$ shifts it by exactly $11/8$ |
| Decoy test on the $\alpha$ match — **RUN 2026-08-30** | **T1** | `alpha_decoy_test.py`: **14 of 14** decoy log-forms reproduce CODATA once each is given its own free cutoff. The test does **not** separate, where the T_min precedent did. Bits carried: **0** |
| Shuffle knife / surrogates **do not apply** to the CPF audit | **T2** | the audit is deductive (exact integers, finite group theory, rational certificates, a kernel-checked proof); there is no distribution to permute |

> **Standing correction to practice.** An audit in this corpus should state up front which
> of the program's own devices it applies and which it does not and why. Four instruments
> went by without that. The verdicts were correct; the audit was simply built as though
> the corpus had no methods of its own.

### This program's own methodological inventions (none externally sourced)

`shuffle knife` — marginal-matched surrogate; FORM/FUNCTION split, self-calibrating
because the surrogate inherits the object's own distribution ·
`tomographic invariance` — refraction vs invariant under instrument swap, with numerical
(a) and structural (b) paths and an explicit rule never to let (b) wear (a)'s clothes ·
`vantage-point census` — effective rank of witnesses ·
`decoy discipline` · `strip-mine targeting` — rank by expected-space-collapsed per unit
cost, weighted toward the program's *own* load-bearing claims ·
`append-only elimination ledger` · `tiers never promote`.


---

## Decoy test and the second T0 (2026-08-30)

Code: `code/constraint_projection/alpha_decoy_test.py` ·
`code/constraint_projection/lean/AxiomIII.lean`
Artifacts: `docs/alpha_decoy_test.json` · Ledger: `docs/Elimination_Ledger.md`, 2026-08-30

| Claim | Tier | Evidence |
|-------|------|----------|
| The manuscript's $\alpha$ form is **not privileged** | **T1** | 14 of 14 decoy log-forms hit CODATA to $<10^{-25}$; the test does not separate |
| The match carries **0 bits** | **T2** | 1 parameter fitted to 1 datum, residual DOF 0; the model reproduces every target in its range ($\alpha^{-1}=42$ at $a/R=1.25\times10^{-17}$) |
| The quoted $6\times10^{-9}$ tracks **working precision**, not physics | **T1** | residual falls with `mp.dps`; improvable without limit |
| Parameter-free reading predicts $\alpha^{-1} = 1.886$ | **T1** | from $\tau = ia/R = i/2$; wrong by a factor of **72.6** |
| That 72.6× gap is an **artifact, not a scaling rule** | **T1/T2** | `alpha_scaling_test.py` — ratio runs 61→138 across the $\tau$ sweep; exponents for $\alpha$/$L_{\rm IR}$/$g$ are 1.0 / 20.7 / 0.00027; only $p=0$ reconciles the three instruments; 1 observable vs 2 parameters |
| $\alpha^{-1}$ is a **REFRACTION** by the kill-criterion | **T2** | ~8× across annulus/conformal/BIE; $d(\alpha^{-1})/d(\text{const}) = 1/2$ exactly |
| **Axiom III clause (3) unsatisfiable** | **T0** | `axiom_III_clause3_unsatisfiable` — centraliser is diagonal, $\varphi_*$ is not, its unimodular part is exactly four, $\varphi_*$ has infinite order |
| Both Lean proofs can fail | **T1** | 3 + 4 mutations, all REJECTED |

> **Axioms.** `LFBound.lean` uses only `propext` and `Quot.sound` (constructive).
> `AxiomIII.lean` additionally uses **`Classical.choice`** — not constructive. Disclosed
> because the first file's constructivity was reported, so the second's loss of it must be.

> **Scope of the Axiom III proof.** The *algebraic* obstruction is machine-checked. That a
> diffeomorphism of $K$ induces a matrix commuting with $D$, and that
> $\mathrm{MCG}(K)=\mathbb{Z}/2\oplus\mathbb{Z}/2$ (Lickorish 1963), are **assumed and
> cited**, not formalised — the manuscript's error is algebraic, and that is what is proved.


---

## Third T0 — the per-zero 2π contribution (2026-08-30)

Code: `code/constraint_projection/lean/withMathlib/PerZero.lean` ·
Ledger: `docs/Elimination_Ledger.md`, 2026-08-30
Verify: `cd code/constraint_projection/lean/withMathlib && lake exe cache get && lake env lean PerZero.lean`

| Claim | Tier | Evidence |
|-------|------|----------|
| Imaginary parts of the two lines cancel **exactly** | **T0** | `imag_cancels` — $\alpha$ enters only as $\alpha^2$; no hypothesis needed |
| Real parts combine to $2[\arctan(\tfrac{T-\gamma}{\varepsilon}) + \arctan(\tfrac{\gamma}{\varepsilon})]$ | **T0** | `real_doubles` — $\arctan$ is odd |
| That is **strictly below** $2\pi$ at every finite $\varepsilon$ | **T0** | `contribution_lt_two_pi` |
| …and **tends to** $2\pi$ as $\varepsilon\to0^+$ for $0<\gamma<T$ | **T0** | `contribution_tendsto` |
| The proof can fail | **T1** | 5 mutations, all REJECTED — including `imagPart` made odd in $\alpha$ |

> **Wording corrected by the formalisation.** We had written the contribution "$\to 2\pi$"
> in a way that invited reading it as attained. It is not: $\arctan < \pi/2$ strictly, so
> $2\pi$ is a supremum approached, never reached. Both facts are now separate theorems.
> The numerics were never affected; the prose was looser than the mathematics.

> **Axioms:** `propext`, `Classical.choice`, `Quot.sound` — non-constructive, as Mathlib's
> real analysis is.

> **Cost.** First proof here needing Mathlib (~5 GB cache) rather than a bare `lean`
> binary. Kept in `withMathlib/` with its own `lakefile.toml` so the dependency boundary
> is visible in the tree.

### Formal-verification status

The deductive core of the CPF audit is now machine-checked end to end — **§5 LF bound**,
**Axiom III clause (3)**, **§7 per-zero contribution**. What remains outside the kernel is
in every case either measured data or standard textbook results cited by name, never a
step of our own reasoning.


---

## What the α gap is, and whether it can be corrected (2026-08-30)

Code: `code/constraint_projection/alpha_gap_diagnosis.py` ·
Artifact: `docs/alpha_gap_diagnosis.json` · Ledger: `docs/Elimination_Ledger.md`, 2026-08-30

Follow-on from the scaling test: ruling out a power law ruled out a *species* of
correction, leaving open what the gap actually is.

| Finding | Tier | Evidence |
|---------|------|----------|
| The gap is **additive in the log** ($L \to L+270$), not multiplicative | **T1** | why no power law could fit — wrong shape of correction |
| "72.6×" is an artifact of $a/R=1/2$; the **Planck cutoff gives 26.96** (5.08×) | **T1** | six physical scales tabulated, from 1.54 to 137.04 |
| The CODATA-matching cutoff is $2.4\times10^{-96}$ Planck lengths | **T1** | not a regulator; voids "UV complete" |
| The prefactor **cannot be repaired**: $\alpha^{-1} = (4\pi\eta^2/\kappa)L$ needs $\eta \notin \{1,\tfrac12,\tfrac13,\tfrac23,2\}$ for every natural $\kappa$ | **T2** | four normalisations tried |
| Log-in-scale **is** the shape of RG running — but coefficient off by $3\pi/4$ and **sign opposite** | **T2** | QED $-2/3\pi$ screens; this $+1/2$ anti-screens, backwards for $U(1)$ |
| The general no-go is **standard, not ours** | **T2** | dimensional transmutation; RG boundary conditions; arXiv:1411.4673 survey |

> **Answer: the gap is not correctable.** All three routes close. The correct move is
> reporting, not repair — the framework with its own scale-fixing predicts
> $\alpha^{-1} = 1.886$ and is falsified. Anything that closes the gap adds physics not
> in the manuscript, and must then be tested as a different theory.

> **Wyler 1970 got $\alpha^{-1} = 137.03608$ (rel err $5.9\times10^{-7}$) and was
> debunked. This manuscript is 13,471× closer — and carries zero bits.** Closer agreement
> is not better evidence; more digits only means more digits were fitted. *(An in-flight
> correction: the first draft of the instrument had this comparison backwards.)*


---

## Can a relative boundary condition fix α? (2026-08-30)

Code: `code/constraint_projection/alpha_relational_boundary.py` ·
Artifact: `docs/alpha_relational_boundary.json` · Ledger: `docs/Elimination_Ledger.md`

| Finding | Tier | Evidence |
|---------|------|----------|
| §8's $\lambda_{\rm UV}\lambda_{\rm IR}=1/R^4$ **is** a relational condition: $a\,L_{\rm IR}=R^2$ | **T2** | substituting gives $\alpha^{-1} = \tfrac12(\ln(8L_{\rm IR}/R)+1)$ — Dirac large-number form |
| Using it makes α a **parameter-free prediction**: $\alpha^{-1} = 46.24$ | **T1** | off by 2.96×, beating 72.6× ($\tau=i/2$) and 5.08× (Planck) |
| But it predicts α **drifts** at $2.5\times10^{-13}$/yr | **T1** | $\dot\alpha/\alpha \sim H_0/2\alpha^{-1}$ |
| **Excluded by ~10⁴** against every independent bound | **T3(measured)** | atomic clocks 12,575×; Oklo 20,958×; quasars 2,515× |
| The manuscript has **two** relational conditions giving 1.886 and 46.24 | **T1** | they disagree by **24.5×** |

> **The deep point.** A relative boundary condition does not rescue the framework — it
> makes it **over-determined and inconsistent**, which is strictly worse than
> under-determined. Under-determination is a missing input you can go find;
> over-determination with disagreement means the framework's own conditions contradict
> each other, and there is no free parameter left to absorb the difference.

> **Prior art (rule 4, searched before claiming).** α-constancy as a constraint on
> varying-α models is a standard, well-developed method, and the Oklo / atomic-clock
> bounds are the field's own. The Dirac large-number framing is classical. Only the
> application to this framework is ours.

> **A route that improved things and was killed anyway.** 72.6× → 2.96× and
> parameter-free is a real gain. It died on a test it could have passed: had the drift
> come in below 10⁻¹⁷/yr, the relational reading would have survived as a live option.
