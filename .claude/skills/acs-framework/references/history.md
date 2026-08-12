# How the ACS Framework Repo Got Here

Provenance and intellectual history of `tensorrent/ACS-Framework`. Read this when you
need to know *why* something is the way it is, who killed what, or what a branch name means.

**Scope:** 79 commits, 2026-06-27 → 2026-08-07 on `main`, plus one unmerged branch dated
2026-08-10. Owner and merger throughout: Brad Wallace (`wellthatshandy@gmail.com`, GitHub
`tensorrent`).

---

## 1. Timeline in seven phases

| Phase | Dates | What happened |
|---|---|---|
| 0 — Public release | 2026-06-27 | `0d21a04` drops the entire corpus at once. Same day: `7422dbb` strips `TR-2026-FF06*` preprint designations; `f830807` rebuilds README as a scientific index; `b12a675` adds the Technical Whitepaper. |
| 1 — Solo consolidation | 2026-07-02 → 07-10 | Owner commits direct to `main`. Antigravity Feed Package, 7-input parameter ledger, YM sealed release, the mass retitling (`73cc4c2`), FF06f, SIP License v1.1 migration. |
| 2 — Agent-branch research era | 2026-07-11 → 07-17 | Work moves to `claude/*` branches, one per research thread. PRs #1–#6 plus the start of #7. |
| 3 — Cursor-assisted expansion | 2026-07-22 → 07-23 | Owner + `Co-authored-by: Cursor`, direct to `main`. Möbius-screw electron, Klein-Foam Monad, nuclear decay, Pα trilogy, capacitance, BUGFIX_LOG. |
| 4 — Corruption repair + framing parity | 2026-07-23 → 07-26 | `claude/electron-banach-tarski-lduyf6` → PR #8. |
| 5 — Glossary side-branch | 2026-07-30 | `8fdfcfe` on `docs/glossary`. Unrelated FHE branch reaches its final commit, never merged. |
| 6 — Public-cleanup arc | 2026-08-07 | Four PRs (#9–#12) in seven hours. `main` ends at `08abbbd`. |
| 7 — In flight | 2026-08-10 | `claude/public-ip-exposure-audit-6zxyf4`, one commit, no PR. |

At initial release the papers carried different names. The corpus arrived complete:
core trilogy, three notes, FF06e, the later-FF06 series, the root monograph, the AI-stack
PDR, three code trees, and the docs including the Elimination Ledger. Nothing here was
built incrementally from nothing — the July/August work is refinement, falsification and
cleanup on top of a corpus that landed whole.

---

## 2. Pull requests

| PR | Merged | Branch | Size | What it did |
|---|---|---|---|---|
| #1 | 07-11 | `form-function-perspective-trsjjg` | +334/−1 | FF06g: form/function is frame-relative |
| #2 | 07-13 | `tr8g-pythagorean-theorem-4332wx` | +124/−47 | Paper B acoustic reframing |
| #3 | 07-13 | `neiman-tensor-equation-nub8q8` | +260 | Palatini curvature solver |
| #4 | **closed unmerged** 08-07 | `infinity-zero-scaled-invariance-vzm54b` | +493/−2 | FF06h — superseded, content cherry-picked into #7 |
| #5 | 07-17 | `torsion-topological-condensation-h6v40k` | +180 | Torsion holonomy verdict (T4) |
| #6 | 08-07 | same torsion branch | +650/−2 | Three conjecture tests; F-6 kill |
| #7 | 08-07 | `neiman-tensor-equation-nub8q8` | +2227/−4, 14 commits | The spectral witness arc |
| #8 | 07-26 | `electron-banach-tarski-lduyf6` | +1204/−98, 31 files | Corruption fix + Sl=2↔g=2 kill |
| #9 | 08-07 | `repo-cleanup-public-u5wyz8` | +5769/−2260, 29 commits | Consolidate all branches |
| #10 | 08-07 | same | +2959/−299 | Glossary rebuild, CITATION.cff, 107-finding audit |
| #11 | 08-07 | same | +86/−32 | The 8 high-severity fixes |
| #12 | 08-07 | same | +1710/−238, 42 files | All 99 medium/low findings |

### PR detail worth carrying

**#1 — FF06g.** Establishes that the FORM/FUNCTION label is a property of the *pair*
(witness, reference measure), not of the witness. Scores five witnesses against the
refinement ladder Poisson ≺ GUE-marginal ≺ GUE-full ≺ ζ and proves a monotone staircase:
repulsion and Wigner-shape read FUNCTION vs Poisson (44–50σ) and FORM vs GUE-marginal
(0.1–0.2σ) — the identical witness carrying opposite labels. The arithmetic prime-resonance
witness stays FUNCTION in every frame short of ζ (260–832σ). Kills the implicit FF06e claim
that labels were intrinsic. T1.

**#2 — Paper B acoustic reframing.** Paper B's prose asserted a difference-tone/Tartini
*resonance* between primes and zeros, contradicting its own §8 synthesis, Witness Refinement
§7.2, and the Elimination Ledger, all of which report zero–prime frequency alignment as
consistent with the null. Rewritten: intra-species (zero-zero, prime-prime) combination tones
are real; the cross-species relation is complementary cancellation carried by the explicit
formula. RH becomes "in balance, not in tune."

**#3 — Palatini curvature solver.** `riemann_curvature_palatini.py` reads
R^{ab} = dω^{ab} + ω^a_c ∧ ω^{cb} as the second-order ACS (Layer-2) self-coupling of the
connection. Verified on Schwarzschild: ∇g = 0, R_μν = 0, Kretschmann K = 48M²/r⁶, full
algebraic symmetries and first Bianchi. T1.

**#5 — Torsion holonomy.** Tests "mass/gravity is a quantum condensate caught in a torsional
field" by computing holonomy instead of assuming it. `ad_{T_BL}` has exact real spectrum
{0(×9), ±4/3(×3)} ⇒ hyperbolic, not rotational; node displacement ×4348 at t = 2π with no
closure. dim(torsion ∩ sl(3,ℝ)) = 5 of 8; the locked 0:1:4 ratio leaves the photon direction
torsion-decoupled. Verdict **Topological Dissipation**, T4. Commit `f1b80a3` carries an
integrity note: the prompt's claimed "679-test validation set" does not exist in the repo,
so the verdict rests on the 42-assertion suite — "Reporting 'Structural Coherence' would have
been overclaiming."

**#6 — Three conjecture tests**, each stated in kill-able form *before* computing, exact
rational arithmetic:
1. **EM-as-torsion-annihilator — KILLED both forms** → ledger F-6. The torsion sector is
   exactly Sym₀(4); its centralizer in sl(4) is {0}; Q = J3+K3+T_BL/2 isn't even in
   ker ad_{T_BL}. Positive residue: the torsion-coupling operator is block-scalar with exact
   spectrum {4(×9), 6(×6)} — a new T1 locked invariant.
2. **Condensate-as-collapse — SURVIVES all four forms.** The image/ω-limit dual of the killed
   kernel form: every generic direction collapses projectively onto a 3-dim V₊ that is exactly
   the three lepton→quark transition operators; collapse rate 4/3 = Δ(B−L) exactly; invariant
   sector exactly sl(3)⊕u(1)_{B−L}.
3. **Hypercone-through-the-slice — SURVIVES all three forms.** Eigenvalue sheets
   ±√(x²+y²) (codim 2, β=1); with the chirality direction ±√(x²+y²+z²) (codim 3, β=2).
   **β = codim − 1**; measured β = 2.019 on the repo's 100k zeros.

**#7 — The spectral witness arc** (largest research PR). Results, each machine-verified:
- **Witness census** (`hp_vantage_points.py`): ~4.8/5 independent instruments but exactly
  **two** robust FUNCTION faces — arithmetic (830σ) and local-order (26σ). No third face.
- **Harmonic ladder / repetition tower** (`hp_harmonic_ladder.py`, `hp_ladder_tower.py`):
  Weil trace-formula weight |F(k log p)| ~ Λ(p^k)/√(p^k), a tower **3 deep**. Rung-2 slope
  −0.501 (R²=1.00, p≤47); rung-3 slope −1.015 (R²=1.00, p≤7 before background); absolute
  weight slope +1.002.
- **Character twist + commutator law** (`hp_ladder_character_twist.py`, `hp_twist_hardened.py`):
  χ^k on rung k, universal across Dirichlet L. Rung-1 demodulation R = 0.99 on ~150 freshly
  generated non-circular L-zeros; quadratic sign flips 12/12. The law
  **‖[ι,T]‖_k = 0 iff order(χ) | 2k**, confirmed to rung 3.
- **Honest negative kept first-class:** rung-2 phase never hardened, sits at the demodulation
  floor even at 150 zeros, stays T3.
- **HP wall quantified then resolved** (`hp_operator_constraint.py`, `hp_wall_resolution_class.py`):
  any H with spectrum {γ} must carry real orbit amplitudes (|Im W|/|Re W| = 0.0001) *and*
  GUE β = 2.00 — naively opposite classes. Resolved by importing #6's hypercone β = codim − 1:
  they coexist exactly under an **anti-commuting antiunitary** (C H* C⁻¹ = −H, C² = −1).
  Among GOE/GUE/chiral, only chiral passes both.
- Synthesis note: `papers/notes/Critical_Line_As_Fibered_Object.tex`.

**#8 — Corruption fix + framing parity.** The headline fix: `73cc4c2`'s find-replace
replacement string contained its own search string, expanding phrases five-fold ("Adjoint
Spectral Minimization and Bipartite Adjoint Spectral…", "Dynamical Dynamical … over Prime Gap
Ensembless over…") across 11 files including paper sources, MANIFEST, README and a test module.
Also carries the framing-transformer computation and the Sl=2 ↔ g=2 kill, README-tree
regeneration (the tree "failed against `ls` on the first check": a nonexistent Paper B filename,
3-of-11 notes, 3-of-4 methodology papers), `pytest.ini` testpaths pinning (collection
10.8 s → 2.6 s), and the CDN-dependency disclosure for the Q-plane visualizer.
Editorial principle recorded in `62967b6`: captured stdout and run-output JSON showing absolute
paths were *deliberately left untouched* — "rewriting evidence to look tidier is not a fix."

**#9 — Consolidation.** Five branches merged via five descriptive merge commits; two things
explicitly declined: PR #4 (byte-identical duplicate) and the FHE branch ("effectively a
separate project… needs an owner decision"). This is where all the July branch research
actually reached `main`.

**#10 — Glossary, citation, audit.** GLOSSARY.md replaced wholesale (see §5), `CITATION.cff`
added (CFF 1.2.0), and `docs/Editorial_Audit_2026-08-07.md` landed: 107 findings
(8 high / 48 medium / 51 low) from an end-to-end read of every manuscript.

**#11 — The 8 high-severity fixes**, deliberately opened unmerged for author review because
they touch manuscript wording:

| ID | Fix |
|---|---|
| H1 | SU(3) closure attractor annotated T3 numerical selection; skill's "Proved Theorems (10)" → "9 and one numerical selection" |
| H2 | Whitepaper's sl(3,ℝ) "unique subalgebra" scoped to the 50k-sample numerical result; λ_φ/γ marked as refractions per ledger OOS01/Q1 |
| H3 | Provenance note for kill-test scripts cited at `/tmp` or with no path that were never committed |
| H4 | Paper C order-counting fix in `thm:inversion` Step 3 (first-order coefficient displayed at ε²) |
| H5 | Paper A chiral-zero-mode citations repointed from `thm:gravity-acs` (which contains no such result) to §6 |
| H6 | Paper B Theorem T4′ made explicitly conditional on the minimum-gap bound |
| H7 | *One Mechanism Many Forms* gets a dated note that the ledger retired Link 3, so the synthesis "presently reads as analogy, not identity" |
| H8 | Three FF06 reproduction appendices state which artifacts are committed |

**#12 — All 99 medium/low.** Every audit entry gains a **Resolution** line; 4 retained by
design as author's voice. Substance corrections: torsion-tier count reconciled to two tiers;
PDG claim corrected to seven-of-nine; the undocumented "Alexander Reina Russell 1867" Mersenne
attribution replaced with the documented record (de Chancourtois 1862, Newlands 1865);
prime-gap contraction crossing recomputed (φ ≈ 35, not 50); the chirality-map "iff" given a
two-line algebraic proof instead of resting on a grid scan. Two findings closed by *doing work*
rather than editing text: generating and committing the capacitance results JSON, and
replicating the issue7 float suite on Linux x86_64 (`docs/issue7_linux_replication/`) with
decision-level outputs matching and the exact artifact byte-identical.

---

## 3. The research arcs

**A. The spectral-witness arc** — `neiman-tensor-equation-nub8q8`, 07-13 → 07-17, PRs #3 and #7.
Starts almost incidentally with a Palatini curvature solver and becomes the repo's deepest
investigation. Move order: count the faces (exactly two robust FUNCTION faces; third-face
search fails) → find the arithmetic face's internal depth (the p^{−k/2} trace-formula ladder)
→ test universality across Dirichlet L (χ^k on rung k) → discover the commutator law → deepen
the tower to rung 3 → quantify the Hilbert-Pólya wall as two measured numbers rather than a
slogan → harden the twist on ~150 generated L-zeros → resolve the wall as a symmetry-class
selection using the torsion branch's hypercone result. Self-corrects its own framing mid-arc
(see §4). **Resolution: class pinned (anti-commuting antiunitary / chiral ensemble), arithmetic
realisation left open.** Every commit says "proves nothing about RH; constructs no operator."

**B. The torsion condensation conjecture tests** — `torsion-topological-condensation-h6v40k`,
07-17, PRs #5 and #6. Begins from a physical conjecture posed to be computed rather than
asserted. #5 returns Topological Dissipation. #6 then runs three sharper conjectures on the
same algebra: the EM-annihilator dies in both forms, and its *dual* reading — the condensate as
the collapsed terminal output, "the slag of the furnace," rather than the protected base —
survives all four sub-claims. An unusually clean case of a kill directly generating its own
successor. The hypercone test's β = codim − 1 then becomes the load-bearing input to arc A's
wall resolution: the two branches cross-fertilise without merging.

**C. The electron / Banach-Tarski framing-parity thread** — `electron-banach-tarski-lduyf6`,
07-23 → 07-26, PR #8 plus four post-merge commits. Targets the Möbius-screw electron note,
which identified the (2,1) framed-unknot self-linking number Sl = pq = 2 with the Dirac g = 2.
`5973d95` builds the chain γ → U → Sl → F:S¹→SO(3) → q:S¹→SU(2) and confirms the geometry
(T·U = 0 to 2.2e−16; |Sl| = 2 by two independent routes; frame loop spinorial, σ = −1) — then
kills the identification with the parity law **σ = (−1)^(Sl+1) = (−1)^(p+q)**: an Sl = 0 round
circle is spinorial in exactly the same sense, so the magnitude 2 carries no spin information.
What survives is the odd meridian winding q = 1 as the actual source of the double cover.
Post-merge: `26c2005` grounds the parity law in the published literature (Needham
arXiv:1708.09124, Gompf-Stipsicz §5.6–5.7, Dennis-Hannay 2005, Atiyah 1990,
Finkelstein-Rubinstein 1968, Wilczek-Zee 1983, and decisively Lévy-Leblond 1967 — g = 2 comes
from linearizing Schrödinger, so its origin is the spinor representation, neither relativistic
nor topological), making the T4 verdict binding rather than in-house. `62967b6` adds a
self-contained five-plate visual (live Gauss double integral, no CDN) and finds the
tornado/funnel reading is the *same* framed loop under a/R → 1, with Tw + Wr = −2.000000
throughout. `d2d9334` runs the successor test the first kill proposed — compute μ/⟨L⟩ instead
of matching integers — and kills that too: **g = 1 exactly** for every closed curve, the double
winding real (2.09× vector area) but cancelling identically; ends with a T2 no-go: no model with
charge and mass circulating at uniform q/m gives g ≠ 1. `f46ec47` closes constructively by
relocating spin into a Laplace eigenspace on S³ (measured −3.00000 per axis, degeneracy 4, the
(½,½) rep), and flags the KAM-vs-quantization tension (irrational winding ratios have no
self-linking number at all).

**D. The form/function perspective thread** — `form-function-perspective-trsjjg`, 07-11, PR #1
plus post-merge `e6a7625`. Two steps: make frame-relativity operational, then elevate it from a
spectral fact to a general **Principle of role-relativity in nested systems** — a component's
role is conferred by the enclosing system that resolves it — with the monotone-staircase
proposition read as the folk saying ("one man's trash…") made a theorem. Explicitly honest
about the elevation: the general principle and folk dualities are framing, not measurement; the
FF06g table is byte-for-byte unchanged.

**E. The FF06h scaled-invariance thread** — developed *in parallel* on two branches. Resolved
not by picking a winner arbitrarily but by cherry-picking #4's version as canonical into #7 and
closing #4. The only fully-superseded PR in the repo.

**F. The public-cleanup arc** — 08-07, PRs #9–#12. Four stages in one day: consolidate →
document and audit → fix what's dangerous → fix everything else.

**G. The unmerged FHE side-project** — `feature/prime-fhe-homomorphic-primitive`, last commit
2026-07-30. A ~217k-line crypto eprint (Transcript Equivalence Theorem, AKPP nullity proof,
blinded-evaluation handle protocol) that deletes files `main` still uses. Left alone pending an
owner decision. **Do not merge or cherry-pick from it without asking.**

---

## 4. What was falsified, and when

**Pre-history** (in `key_parameters_ledger.json`, dated 2026-06-06, present at initial release):

| ID | Killed claim | Tier / reason |
|---|---|---|
| F-1 | ad³ = 2·ad | T4 — fails for integer eigenvalues |
| F-2 | Universal 2π inversion loop | T4 — sl(4,ℝ) adjoint is hyperbolic; only su(2) quaternion closes |
| F-3 | Wronskian-Poisson equivalence | T4 — Leibniz failure by the −f·g·h′ term |
| F-4 | IR lattice imprint | T4 — no significant ⟨2,3⟩ imprint in PDG masses/CKM |
| F-5 | θ₀ derivable from algebra | T2 — θ₀ = 2/9 is necessarily a fit |

Same 2026-06-06 session block: Q6 residual prime-orbit off-diagonal mechanism KILLED;
Q5 class kills (GOE, GSE, and xp-alone killed as sufficient); Q3 (d,q) scaling law FALSIFIED
(T4); Q4 ΔI ≡ RG c-function identity falsified as stated, monotonicity analogy survives (this
is the kill behind PR #11's H7); Q1 framework constants' bare values confirmed as *refractions*
(the kill behind H2).

**2026-07-09** — FF06f retracts the internal "no two-point statistic carries the primes"
reading; it had measured the wrong two-point object (index/spacing rather than position pair
correlation).

**2026-07-13 (PR #2)** — the prime-zero *acoustic resonance* mechanism, killed by the paper's
own null result.

**2026-07-14** — the "critical line as a flattening" framing killed by the repo's own
vocabulary (`abd1fca`): flattening means compression to a scalar; the correct object is a
**seam**, two-sided and two-dimensional, "crossable for density, uncrossable for identity."
Same day, two first-class negatives recorded: rung-2 character phase never hardens even at 150
zeros; and the non-existence of any known natural operator with the required signature.

**2026-07-17** — torsion-condensation holonomy: T4 Topological Dissipation (#5). Then **F-6**,
EM-as-torsion-annihilator, killed in both strong and weak form (#6).

**2026-07-26** — **Sl = 2 ↔ g = 2 killed** (T2 structural / T1 numerical): the geometric integer
carries no spin information a 0 doesn't. Its successor — the dynamo/moment-ratio route — killed
the same day with **g = 1 exactly**, generalized to a T2 no-go on any uniform-q/m circulating
model. Also recorded: half-integer hopfions/fractional skyrmions in the condensed-matter
literature mean half-integer *topological index*, not angular momentum, and are not precedent.

**2026-08-07 (PR #11)** — not scientific kills but credibility corrections: SU(3) closure
attractor demoted from "proved theorem" to T3 numerical selection; sl(3,ℝ) "uniqueness" scoped
to a 50k-sample numerical result; Theorem T4′ made conditional; Paper C's inversion-proof
order-counting corrected; FF06Σ Link 3 downgraded to analogy.

---

## 5. Deletions, renames, and the corruption incident

**The 2026-07-07 mass retitling (`73cc4c2`, 75 files)** — "Standardize ACS filenames and titles
to scientific consensus":

| Old | New |
|---|---|
| `Colour_from_Gravity` | **`Palatini_Gauge_Attractor`** (Paper A) |
| `Riemann_Spectral_ACS_extended` | **`Riemann_Spectral_Critical_Line`** (Paper B) |
| `Spectral_Witness_Survival` | **`Spectral_Witness_Refinement`** (Paper B′) |
| `Inversion_Arc` | **`Holographic_Spectral_Inversion`** (Paper C) |
| `Form_Function_Shuffle_Knife` | `Spectral_Rigidity_Shuffle_Knife` (FF06e) |
| `Pythagorean_Structure` | `Pythagorean_Lattice_Limits` (N1) |
| `Signature_Selection` | `Adjoint_Clifford_Signature_Selection` (N2) |
| `Transition_Operator` | `Prime_Gap_Transition_Operator` (N3) |

This is the *only* commit in history that deletes paper files, and it is also the commit that
broke the corpus. Not caught until `764200a` (2026-07-23) and PR #8; residual artifacts were
still being cleaned in PR #12. **If you find a five-folded phrase anywhere, this is why.**

**2026-06-27 (`7422dbb`)** — all `TR-2026-FF06*` preprint designations stripped
(`TR-2026-FF06d` → `ACS-PDR-1.0`). Note they partly return later: the Cursor-phase notes
reintroduce `TR-2026-FF06-KFM` and `TR-2026-FF06-I7`.

**2026-07-26 (`62967b6`)** — deletes stale duplicate harness scripts and scrubs authoring-machine
paths (`rh_papers_may21/`, `/Users/…`, `tent_io/`) from source and prose while explicitly
preserving absolute paths inside captured stdout and run-output JSON as true records.

**The glossary replacement (2026-08-07, `18fb3d7`)** — the `docs/glossary`-branch GLOSSARY.md
turned out to be an extract from a *cross-repository* catalogue covering codebases not present
here. Preserved verbatim at `docs/Cross_Repo_Glossary_Extract.md` with a provenance note, and
GLOSSARY.md rebuilt from a complete pass over all 30 papers/notes plus MANIFEST, whitepaper,
corpus map, ledger and skill module: 360+ entries in eight thematic sections, ~670-row
alphabetical index, every one of 51 cited paths verified to resolve, falsified claims retained
and marked. The original's most valuable content was its **vocabulary-hazard section** (three
senses of "scroll"; CDCL redefined as Constraint-Driven Consensus Layer; ζ as a boolean
predicate; three incompatible F369 tables all carrying the EigenCharge name, making cross-repo
charge comparison invalid).

---

## 6. Authorship patterns

- **`Claude <noreply@anthropic.com>` — 44 commits.** All research and cleanup branch work.
  Every commit carries a `Claude-Session:` URL and a model trailer.
- **`tensorrent <wellthatshandy@gmail.com>` — 26 commits.** Direct-to-`main` owner work.
- **`Brad Wallace` — 9 commits.** Exclusively GitHub merge commits. Same human, same email;
  the display name differs because GitHub's web merge uses the profile name.
- **Model trailers mark eras.** Claude Opus 4.8 — 21 commits, 07-09 → 07-17. Claude Fable 5 —
  21 commits, 07-17 → 08-07. Claude Opus 5 — the 08-10 exposure-audit commit only. The
  4.8 → Fable 5 handover happens mid-day on 07-17, in the middle of the torsion branch.
- **`Co-authored-by: Cursor` — 10 commits**, all 2026-07-22/23: a distinct tool-and-phase
  signature covering the Möbius-screw electron, Klein-Foam Monad, nuclear decay, Pα trilogy and
  BUGFIX_LOG work.
- **PR bodies are Claude-written** and unusually structured: summary, per-claim results with
  numbers, an explicit scope-boundary section, and a verification block.
- **No reviews, no review comments, no issues.** Every PR self-merged by the owner within
  seconds to minutes, except #6/#7 (open 21 days) and #11 (15 minutes, held for review).

---

## 7. Current state

- **`origin/main` = `08abbbd`** (2026-08-07, the PR #12 merge). This is the tip.
- **Local `main` is stale** at `5f36688` (the PR #8 merge, 2026-07-26), 37 commits behind.
  Always check which you're on.
- **No open PRs, no open issues.** Eleven of twelve PRs merged; #4 closed as superseded.
- **In flight:** `claude/public-ip-exposure-audit-6zxyf4`, one commit `93c9459` (2026-08-10),
  branched off `08abbbd`, never PR'd. It redacts local developer absolute paths from
  `docs/issue7_verification_report.json`, `docs/issue7_logs/*_stdout.txt`, and
  `docs/ACS_Antigravity_Feed_Package/verification_report.json`, and removes private
  sibling-codebase detail from `docs/Cross_Repo_Glossary_Extract.md`, while deliberately
  retaining author affiliations and the AISO/TENT/OmniForge references. Its own caveat: "this
  does not remove the previously published content from git history, and the repository is
  public."
- **Dormant:** `feature/prime-fhe-homomorphic-primitive`. The eight merged research branches
  still exist on the remote and were never deleted.
- **Standing invariants across all history:** canonical seed `20260423`; the
  `code/acs_codebase` pytest suite at **42 passing** in every verification block from July
  through August; the T1–T4 tier vocabulary; the Elimination Ledger as a living, append-only
  kill log (its description corrected from a fixed "eight falsifications" count in PR #10).
