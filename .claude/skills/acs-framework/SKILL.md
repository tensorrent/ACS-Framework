---
name: acs-framework
description: Working knowledge of the ACS (Asymmetric Codependent Systems) research corpus in this repo — Papers A/B/B′/C, the FF06 methodology thread, the flag-condensate physical models, the T1–T4 claim ledger, the Elimination Ledger of falsifications, the verification code, and the project's history. Use when working on any ACS paper, note, claim, or verification script; when asked what a result means, what tier it sits at, what was falsified, or what is still open; or when editing, citing, reviewing, or extending anything in papers/, code/, docs/, or MANIFEST.md.
---

# ACS Framework

Working knowledge of `tensorrent/ACS-Framework`. This file is the cheatsheet: it should answer most
questions without opening the papers. Load a reference file only for depth.

| Reference | Use when |
|---|---|
| `references/core-trilogy.md` | Papers A, B, B′, C + monograph: theorems, numbers, non-claims, internal inconsistencies |
| `references/methodology-ff06.md` | The shuffle knife, form/function relativity, scaled invariance, Section 9 kill tests, the later_FF06 thread |
| `references/notes-and-models.md` | N1/N2/N3, the Möbius-screw electron, Pα trilogy, capacitance, Klein foam, Paper D |
| `references/governance-and-claims.md` | The full claim ledger, every kill, the audit, the license, open problems |
| `references/code-map.md` | What runs, what the 42 assertions assert, data artifacts, what's broken |
| `references/glossary.md` | Distilled vocabulary, by cluster — replaces the 292 KB GLOSSARY.md |
| `references/figures-and-visuals.md` | Figure inventory, the build script, and the two interactive pages |
| `references/history.md` | How the repo got here: timeline, PRs #1–#12, research arcs, the corruption incident |

---

## The one-paragraph version

Brad Wallace's ACS framework posits that any two mutually-constraining fields — **Form** (structural
information) and **Function** (dynamic information) — generate a net transfer entropy **ΔI**, whose
second-order Taylor coefficient **is** the Lie bracket [f,g] (the **BCH–TE morphism**, the
technical core). Applied to the Palatini pair (vierbein, connection) this generates 𝔰𝔩(4,ℝ), inside
which 𝔰𝔩(3,ℝ) is selected as the unique closure attractor and complexified to colour 𝔰𝔲(3). Applied
to (primes, Riemann zeros) it recasts RH as a stationarity condition. Applied structurally it says
every solution becomes the next constraint (the **inversion arc**). The corpus's real distinguishing
feature is not the physics but the **epistemic discipline**: a four-tier claim ledger that never
promotes, and an append-only Elimination Ledger where the program's own load-bearing claims are
killed and the kills kept.

---

## Non-negotiable rules when working here

1. **State the tier.** T1 machine-verified · T2 proved in paper · T3 numerically verified · T4
   explicitly falsified. **Tiers never promote. Never let T3 pass as T2.** The repo has caught itself
   violating this (audit H1).
2. **Negatives are first-class outputs.** Document the conjecture, the killing computation, the
   mechanism of failure, and the boundary it establishes. Never quietly drop a dead claim.
3. **Every result carries an explicit scope boundary** — what it DOES and DOES NOT claim.
4. **Overclaiming is the named primary failure mode.** When you find one, correct it immediately and
   say why the earlier version was wrong.
5. **Five caveats must always be stated** when their topic comes up: the **Coleman–Mandula rule**
   (the (3,1) grading is *internal*, not spacetime signature — never optional); the
   **exceptional-algebra boundary** (N2 fails for G₂); the **Barbero–Immirzi gap** (0.274 vs 0.2375);
   the **neutrino tension** (resolved by decoupling, killing the keV-DM reading); **tan β protection**
   ("NOT 'we couldn't fix it'").
6. **Canonical seed `20260423`. PDG v = 246.22 GeV.** Zeros = Odlyzko's first 100,000
   (`code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt`, actually 99,999 lines).
7. **The Riemann Hypothesis is nowhere claimed proved, and no Hilbert–Pólya operator is
   constructed.** Every hp_knife script says so in its own output. Do not let a summary imply otherwise.
8. **`.tex` is authoritative over `.md`** where they differ. The `Flag_Condensate_Nuclear_Decay`
   and Section 9 mirrors were realigned 2026-08-12; assume drift elsewhere until checked.
9. **Canonical sources of truth: `MANIFEST.md` + `docs/Elimination_Ledger.md`.**
   `key_parameters_ledger.json` was retiered to match them 2026-08-12, but still uses its own
   F-numbering — cite falsifications by claim text, not F-number.
10. **License is SIP v1.1 — not open source.** Reading/citing/reproducing is free; anything touching
    revenue needs a written license and triggers an automatic perpetual 8.4% obligation.

---

## The three core results, honestly stated

**Paper A — colour from gravity.** ΔI's 2nd-order coefficient is [f,g] (proved, finite-dim; the
infinite-dim Palatini extension is **conjectured**). The Palatini bracket image is exactly 𝔰𝔩(4,ℝ),
rank 15 = 6 Lorentz + 9 torsion. Among 8-dim subspaces, 𝔰𝔩(3,ℝ) has closure defect < 10⁻¹⁴ while
50,000 random samples all exceed 0.49 — **T3, a numerical selection, not a uniqueness theorem**.
J(T) = i·sym(T) + anti(T) carries it to 𝔰𝔲(3), **importing unitarity as a physical input**. Colour
sits 5 in torsion + 3 in Lorentz — neither sector alone contains it.

**Paper B — the critical line.** Primes (Form) and zeros (Function) coupled by the explicit formula.
**RH ⇒ stationarity is proved** by AM–GM. The **converse is conditional** on an unproved minimum-gap
bound (verified only to N = 200, C ≤ 0.29). σ = ½ is the unique center manifold (pure rotation; any
other σ spirals). The Wronskian is a genuine Lie bracket but **fails Leibniz by exactly −fgh′**, so
it is *not* a Poisson bracket — this kills the paper's own earlier plasma-Hamiltonian foundation.

**Paper C — the inversion arc.** A system solving a constraint becomes the next constraint; ΔI flips
sign, odd at 1st *and* 2nd order. tr([X,Y]X) = 0 identically ⇒ π_X([X,Y]) ≡ 0: **algebraic
non-traversability**, offered as ER=EPR with no bulk geometry. Three-class taxonomy
(elliptic/hyperbolic/parabolic) — and the correction that **ad³ = (16/9)ad is hyperbolic
Cayley–Hamilton saturation, not a 2π inversion**: ‖exp(2π ad_{T_{B−L}})‖ ≈ 4348, not 1.

---

## Numbers worth having memorised

**Algebra (exact).** dim Im(Φ) = **15** · Lorentz/torsion split **6 + 9** · 𝔰𝔩(3,ℝ) sits **5 + 3** ·
spec(ad_{T_{B−L}}) = **{0(×9), ±4/3(×3)}** · **ad³ = (16/9)·ad** · K(T_{B−L},T_{B−L}) = **32/3** ·
tier-2 torsion coupling **32/9** · torsion-coupling operator spectrum **{4(×9), 6(×6)}** ·
ρ_vac^bosonic = **exactly 0** (+512/3 − 512/3) · Koide projection **2/3 to 1e-16** ·
𝒟(𝔰𝔩(3,ℝ)) < 1e-14 vs min random **0.49** (recomputed at 2,000 samples: 3.2e-16 vs **0.508**).

**Physics.** λ_φ = **2√3/27 = 0.1283** vs λ_SM 0.1294 (**0.84%**) · m_H = **124.7 GeV** vs 125.25
(3.2σ) · g₄ = g_L = g_R = **4/3** · h̃/h = **2/3** (the only full invariant) · N_gen = **3** ·
γ_BI = **0.274067** (SU(2)) / 0.190206 (SO(3)) vs DL **0.2375** · θ_QCD = **0 exactly** ·
θ₁₃ = 9.216° vs 8.57 ± 0.12 → **+5.38σ, the weakest prediction** · PDG table: **5 of 7** measured observables within 2σ · sterile ν **49 keV**, X-ray line
**24.5 keV** · Branch A = **6 inputs** vs SM 19+ (3.2×) · CC reduced 10¹²¹ → ~10⁵⁵.

**Spectral.** Form/function split at 10⁵ zeros, 60 surrogates: arithmetic **z ≈ 11,497**, lag-1 **97**
(FUNCTION); spacing/counting/shape **0.4–1.0σ** (FORM) — and those FORM values are re-interpolation
artifacts, exactly zero on bare permuted spacings. Effective rank **≈4 on real AND surrogate**.
Amplification 3,030 → 11,497 from N = 2×10⁴ → 10⁵. Witness census: exactly **two** robust FUNCTION
faces (arithmetic 830σ, local-order 26σ) — **no third face**. ρ₂ reconstruction recovers **100.0%**;
spacing surrogates **~7%**; peak heights ∝ (Λ(n)/√n)² at **r = 0.9975**. Ladder **3 rungs deep**:
rung-2 slope −0.501, rung-3 −1.015, abs. weight +1.002. Commutator law **‖[ι,T]‖_k = 0 iff
order(χ) | 2k**. HP wall: |Im W|/|Re W| = **0.0001** (β=1) vs measured **β = 2.00** — resolved only
by an **anti-commuting antiunitary** (chiral class). **β = codim − 1**; zeros measure **2.019**.
Stationarity α at 2,001,052 zeros = **+0.001259**; off-line injection recovers α = 2σ−1 to 1.5%.

**Models.** Tw + Wr = **−2.000000** at every aspect ratio · **σ = (−1)^{Sl+1} = (−1)^{p+q}** ·
**g = 1 exactly for every closed curve** · Δ_{S³}x_i = **−3.00000**, degeneracy 4 = (½,½) ·
Pα correlation **0.888** (flat) / 0.888 (throat) / 0.968 (eigenmode) but RMS_{S★} ≈ **0.825 in all
three** · Pα LOO 0.286 (n=14) → **1.355 (n=29)** · α⁻¹ best on grid **6.14 / 3.25 / 0.37** vs 137.036.

---

## What was killed (the part that matters most)

| Killed claim | Mechanism |
|---|---|
| **ΔI ≡ the RG c-function** (FF06Σ Link 3) | Fails on sign, fixed-point value, and category. The only surviving reading *is* the Casini–Huerta theorem. **"No reading is both novel and true."** By Σ's own logic the corpus's cross-domain sameness now reads as **analogy, not identity** |
| **T_min = (2πe)^d/q** | At d=2, the floor 72.93 sits above **51 actual zeros**. True scaling is 2πe·q^{−1/d}; the two coincide only at d=1 — **the degenerate-case trap** |
| **Sl = 2 ↔ g = 2** | σ = (−1)^{Sl+1}: an Sl = 0 round circle is spinorial too. The content is **one parity bit** |
| **Geometric g ≠ 1** (successor test) | μ and ⟨L⟩ share the same vector area ⇒ **g = 1** for every closed curve. T2 no-go |
| **Universal 2π inversion** | 𝔰𝔩(4,ℝ) adjoint is hyperbolic; ‖exp(2π ad)‖ ≈ 4348 |
| **Wronskian = Poisson bracket** | Leibniz fails by exactly −fgh′ |
| **EM as torsion annihilator** (F-6) | Torsion sector = Sym₀(4); centralizer in 𝔰𝔩(4) is **{0}** |
| **Torsion condensation holonomy** | Real spectrum ⇒ hyperbolic, not rotational; node displacement **×4348** at 2π. Verdict: **Topological Dissipation** |
| **Section 9 gap→cone chain** | 0/12 exhaustive; the leakage leg has the **wrong sign** (+0.9636) |
| **4/3 mechanism** | Collapses to the identity family n = d + 1 |
| **IR lattice imprint** (N1) | z ∈ [−0.7, +0.3] vs PDG — a clean null |
| **BRA 489× speedup** | Measured **1.37–1.82× slower**. Determinism survives |
| **Prime–zero acoustic resonance** | Cross-species is **complementary cancellation**, not resonance. Prime logs are incommensurable — unique factorisation, spectrally expressed |
| **The four "locked constants" as invariants** | g₄, γ, λ_φ all **refractions** under instrument swap. Only **h̃/h = 2/3** survives. *"The relations survive; the bare numbers mostly don't"* |

**Survivors from the same campaign:** condensate-as-collapse (all four forms — V₊ is exactly the
three lepton→quark transition operators, collapse rate 4/3 = Δ(B−L)); hypercone projection
(β = codim − 1, which then resolved the HP wall); the height floor **value** 2πe at d=1.

---

## Traps — things that will bite you

> **Corrected 2026-08-12** (coherence pass; see `docs/Editorial_Audit_2026-08-07.md`, section
> "Coherence pass"): the 27 placeholder figure PDFs are replaced by a real, byte-reproducible
> build (`scripts/generate_paper_figures.py`); the torsion 0:1:4 vs two-tier contradiction is
> resolved by exact computation (different generator sets — 8/9 is not a third eigenvalue); the
> Ricci "41× variance" was a **standard deviation** mislabel (variance ≈1.7×10³); and the PDG
> table's "seven of nine within 2σ" counted two non-PDG rows, now restated as **five of seven**.
> The two items first logged as open (Wronskian normalisation, FF06 lettering) were both closed
> on follow-up — see traps 1 and 6.

1. **The FF06 lettering collided; now disambiguated by suffix.** Bare `FF06g`/`FF06h` each named
   two papers. Use **`-M`** for the `methodology/` paper and **`-L`** for the
   `later_FF06_series/` one: FF06g-M = Form/Function Relativity, FF06g-L = The Geometry Engine;
   FF06h-M = Scaled Invariance of ∞/0, FF06h-L = When a Number Lies. **A bare FF06g/FF06h in any
   older text is ambiguous** — resolve from the subtree. Canonical table: `papers/README.md`.
2. **Paper B uses three φ_k conventions** — now documented in `rem:phi-conventions`: C1
   log-argument, C2 envelope-stripped (all Wronskian tables), C3 general-σ. The normalisation
   cancels in ratios and in every stationarity statement, but not in absolute magnitudes.
3. **`koide_clebsch_gordan.py`'s headline verdict is a logged negative** — θ₀ = 3.86°/3.92° vs the
   observed 12.73°, closing with `CONCESSION CONFIRMED (T2 derived negative)`. The 0.001% belongs
   to Koide's *empirical* relation, not to anything the script derives.
4. **`higgs_mass_ratio.py` is numerology.** It computes a bracket-based ratio, gets a poor answer,
   then searches **17 hand-written closed forms** and reports the winner as "← EXACT";
   `higgs_derivation.py` exists to derive it and does not succeed. Both now labelled as such.
5. **The `.md` mirrors drift from the `.tex`.** `.tex` is authoritative. The nuclear-decay and
   Section 9 mirrors were corrected 2026-08-12; assume drift elsewhere until checked.
6. **Wronskian magnitudes are convention-dependent — the quoted range is C3, not C2.**
   Paper B's |W| ∈ [8.6×10⁻⁵, 0.19] comes from `extras/riemann_tensor.py` under
   φ_k(t) = e^{σt}[σcos(γ_k t) + γ_k sin(γ_k t)]/(σ²+γ_k²) at t = 1, σ = ½, over 1225 pairs of the
   first 50 zeros; recomputed as **8.589×10⁻⁵ / 0.1921**. The 1/(σ²+γ_k²) factor sets the scale and
   enters twice. Under C2 the same bracket spans [6.4×10⁻⁴, 19.2]. **Never compare magnitudes
   across conventions.** The figure build self-checks against the stated range every run.
7. **`key_parameters_ledger.json` was stale and is now retiered**, but still uses an F-numbering
   that does not match the corpus map's F-1…F-23. Cite falsifications by claim text, not F-number.

8. **Local `main` is stale** at the PR #8 merge, 37 commits behind `origin/main` (`08abbbd`).
9. **Running any artifact script overwrites tracked JSON in `docs/`** (they resolve
   `Path(__file__).parents[2]/"docs"`), and the Pα scripts write to the *wrong* path, creating
   untracked duplicates.
10. **`extras/` is heritage, not the verification surface.** `pytest.ini` pins `testpaths` precisely
    because 9 extras files match pytest's glob and would be *executed* on collection. Never import
    `ACS_all_76_scripts.py` (1.07 MB concatenation).
11. **`exp(2π·ad) ≈ 4348 is correct, not a bug.** A *small* value there would be the bug.
12. **The scale-separated vacuum solve needs `decimal` at 50 digits** — float64 returns v² = 0, a
    spurious "unstable." `extras/phase50_vacuum.py` still has the bug; `src/` fixes it.
13. **Three ambiguity numbers (14 / 15 / 19)** are all correct and different. Citing only the
    degenerate 19 produces a misleading "ambiguity factor." Always report all three.

---

## Running things

```bash
cd code/acs_codebase && python -m pytest -q      # 42 passed, ~2.3 s — the canonical gate
bash verify_all.sh                               # suite + all 15 modules, ~2.5 s
python -m src.paper_c.theorem_c                  # single module (must run as -m from acs_codebase/)

cd code/hp_knife_suite
python3 hp_form_function_relativity.py           # 2.4 s   (--full adds GUE-full, ~7 min)
python3 hp_never_synced.py                       # ~45 s   (dense 6000×6000)
python3 hp_vantage_points.py                     # ~10 min (the witness census)
python3 code/issue7/verify_issue7_pipeline.py    # PASS_WITH_CAUTION by design
python3 scripts/prime_carrier_reproduce.py       # ~2 min, all three FF06f tables
```

Deps: `numpy scipy sympy pytest` (+ `mpmath matplotlib` for some extras, **not** in
requirements.txt). The 42-passing suite is the standing gate cited in every verification block from
July through August.

---

## Still open

**O-1 Hilbert–Pólya operator** — *characterized, not solved*. Must simultaneously be unitary-class
(broken T), reproduce the (T/2π)log(T/2πe) smooth count, and carry primes in the fluctuation
spectrum. GOE and GSE killed; bare xp killed-as-sufficient. Resolution class pinned to the
anti-commuting antiunitary; **arithmetic realisation open**. Blocked on a construction, not on data.
**O-2** FeynRules/UFO export · **O-3** action principle for S̃_g · **O-4** L-functions extension
(needs LMFDB zeros at d>1) · **O-5** full SM from the GL(4) fiber · **O-6** ER=EPR correspondence ·
**O-7** Barbero–Immirzi 0.2375 (needs a *global* singlet projection, not local degeneracy removal) ·
**O-8** neutrino tension — **resolved**, with the decoupling caveat.

**Successor questions the kills opened:** decouple where the charge sits from where the mass sits
(the only route past g = 1) · find "EM as degradation" in the representation where charges act, not
the adjoint algebra · define a static, positive, canonically-normalized ΔI if the c-function identity
is to be revived · supply an arithmetic realisation for the pinned chiral class.

---

## Working conventions

- Cite theorems by `\label` name, not number — A/B/C share **one** counter across
  theorem/lemma/prop/def/remark.
- After any paper edit: compile (3-pass pdflatex) → check refs → run the 42-assertion suite → bundle.
- After any new result: classify T1–T4, update the relevant paper, and if it's a kill, append to
  `docs/Elimination_Ledger.md` with the mechanism.
- The repo's own session protocol lives in `docs/ACS_FRAMEWORK_SKILL.md` (473 lines) — that file is
  the author's in-repo LLM module and remains canonical for the parameter ledger and the computation
  toolkit. This skill summarises and extends it; it does not replace it.
