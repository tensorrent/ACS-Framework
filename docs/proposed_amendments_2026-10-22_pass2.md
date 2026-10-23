# Proposed amendments, 22 October 2026, pass 2

Paste-ready proposals for manifest-bound files. Nothing here has been applied: each target
is listed in `docs/publication/2026-09-24/publication-manifest.json`, so applying it changes
a preserved hash and is the owner's to clear through the integrity gate. The decision each
proposal serves is in [decisions, part 2](decisions_2026-10-22.md). Written by agent session
`dec-science` against `badb0b7`; every `file:line` was re-grepped at that commit.

## 1. Paper A, App. B: the RG-scale sentence and "No free parameters"

**Target.** `papers/core_trilogy/Palatini_Gauge_Attractor.tex` (manifest `grep -c` = 2).
Serves decision 2.1, option 1.

**What it corrects.** `:2454-2456` "This indicates the ACS algebra is realised at the
Pati--Salam scale $\Lambda_{\mathrm{PS}} \sim 10^{15}$~GeV, not $M_P$, or that torsion
partners modify the running above the TeV scale." — the sentence infers a boundary scale
from a mismatch without computing the boundary; the 24 September record
(`docs/condensate_energy/endpoint_audit/README.md:92-98`) records the same running as a
conditional calculation with explicit boundary sensitivity, and a one-loop run with the
boundary at $10^{15}$ GeV (decision 2.1, cheap check) moves $\lambda_{\rm IR}$ from 0.1816
to 0.1849, away from 0.1294. `:2021` "No free parameters, no fitting, no external input."
and `:2469` "No free parameters." are true of the algebraic factors and silent on the
inserted comparison value and the RG inputs.

**Placement.** A new `\section*` immediately after the existing
`\section*{Amendment: scope and evidence, 24 September 2026}` block (`:2979-2988`), before
`\begin{thebibliography}{99}` (`:2990`).

```latex
\section*{Amendment: the quartic running and the parameter count, 22 October 2026}
Appendix~B's statement that the eighteen-percent overshoot of the downward-run quartic
``indicates the ACS algebra is realised at the Pati--Salam scale
$\Lambda_{\mathrm{PS}} \sim 10^{15}$~GeV, not $M_P$'' is withdrawn as an inference. The
running from a boundary value $2\sqrt3/27$ is a conditional calculation: the dated
publication record gives $\lambda_{\rm IR}=0.1806315$ for $\lambda_{\rm UV}=0.1283001$ with
local sensitivity $d\lambda_{\rm IR}/d\lambda_{\rm UV}=0.2088898$, and a one-loop run with
the boundary moved to $10^{15}$~GeV does not bring $\lambda_{\rm IR}$ closer to the
comparison input $0.1294$. No scale at which the algebra fixes the quartic has been
derived, and the companion paper \emph{Complete Scalar Actions and Identifiability
Boundaries in the ACS Framework}, \S6, records that running does not supply the missing
selector. The sentences ``No free parameters, no fitting, no external input'' and ``No free
parameters'' in Appendix~B apply to the algebraic factors $2$, $\sqrt3$, $27$ and $2/3$;
the comparison values $\lambda_{\rm SM}$, $\alpha_s(M_Z)$ and the renormalisation-group
inputs are inserted, and a source expression matched to an inserted value does not derive
that value. The $0.85\%$ algebraic match is retained as a numerical agreement whose
mechanism is underived.
```

## 2. Paper B′, §9.4: "validated chain"

**Target.** `papers/core_trilogy/Spectral_Witness_Refinement.tex` (manifest `grep -c` = 2).
Serves decision 2.1, option 1.

**What it corrects.** `:255` "Through this validated chain, the obstruction's central
content is a *charge*, not a coupling" — "validated" at `:249-255` means the Killing/Koide
chain reproduces the manuscript's inserted $124.7$ GeV; the Action paper's `:306-308`
holds that such agreement does not derive the value. The §12.2 falsification (`:312`) and
the §12.3 split are unaffected and are not amended.

**Placement.** A new `\section*` immediately after the existing
`\section*{Amendment: scope and evidence, 24 September 2026}` block (`:527-536`), before
the Author Statement (`:538`).

```latex
\section*{Amendment: the word ``validated'' in \S9.4, 22 October 2026}
In \S9.4 the Killing-form and Koide chain is called ``validated'' because it reproduces the
Higgs mass quoted by the source manuscript. Reproducing an inserted value is agreement with
that value, not a derivation of it; the companion paper \emph{Complete Scalar Actions and
Identifiability Boundaries in the ACS Framework} records the quartic's running as a
conditional calculation with explicit boundary sensitivity. The chain is therefore
``reproduced'' rather than ``validated'', and the forcing of the central number to the
quark $B\!-\!L$ charge $1/3$ in \S9.4 rests on the Killing normalisation $K=32/3$ alone,
which it shares with the quartic and which carries the quartic's residual (\S12.1). The
tier of \S9.4 (T2) is unchanged; the sentence is rewritten so that its status is not
stronger than the companion paper's.
```

## What this file leaves out

- No proposal for `papers/updates/ACS_Action_Identifiability.tex`: its §6–§7 wording is the
  reading the record supports and needs no change.
- No proposal for the five amendments of `AISO:docs/research/ACS_PAPER_AMENDMENTS_2026-10-21.md`;
  they are already paste-ready in that file and their targets are listed in decision 2.5.

# Proposed amendments — 22 October 2026, pass 2

Paste-ready proposals for manifest-bound files (`docs/publication/2026-09-24/publication-manifest.json`
or `papers/**/*.tex`). Nothing here has been applied; the integrity gate is the owner's to clear.
Each item follows the papers' `\section*{Amendment: ...}` convention and cites the line it amends
at commit `c3a383b`. The open-problem cards these come from are in
[open_problems_2026-10-22.md](open_problems_2026-10-22.md).

## 1. Paper B, Open Problems R04: say that R04 as stated is RH

File: `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:1594-1598`.

Current text: "Classical equivalence, unresolved premise (R04). Theorem~\ref{thm:vonKoch-acs} gives the
corrected RH-equivalent bound. Proving that bound independently of RH remains open."

Reason: Theorem `thm:vonKoch-acs` (`:437-444`) states "RH is equivalent to $\sup_{u\ge u_0}
|\Delta_{\mathrm{norm}}(u)|/(1+u^2)<\infty$". An RH-independent proof of the bound is therefore a proof of
RH, and the branch should not read as a tractable lemma.

```latex
\section*{Amendment: R04 is the Riemann hypothesis}
By Theorem~\ref{thm:vonKoch-acs}, the bound $\sup_{u\ge u_0}|\Delta_{\mathrm{norm}}(u)|/(1+u^2)<\infty$
is equivalent to RH. Open Problem R04 is therefore not a lemma short of RH: proving it independently of
RH is proving RH. The finite-$N$ bound on $D_N(u)$, the grid diagnostics, and any envelope chosen with
$\sigma=1/2$ remain scoped results and are not partial progress on R04.
```

## 2. Fibered-object note: the cited `docs/witness_perspective/` path does not exist

File: `papers/notes/Critical_Line_As_Fibered_Object.tex:86`.

Current text: "The observer experiment in \path{docs/witness_perspective/} shows why linear span, intrinsic
dimension, and available measurement directions must be distinguished."

Observed: `ls docs/witness_perspective` fails at `c3a383b`; no file in the tree matches that name.

```latex
\section*{Amendment: dangling evidence path}
The scope correction of 22 September 2026 cites an observer experiment at
\path{docs/witness_perspective/}. That directory is not in the published repository. Until the
experiment is restored with its receipts, the sentence citing it should be read as an unsupported
reference; the scope correction's conclusion (no carrier, map, or proof is supplied) does not depend on it.
```

## 3. Witness paper §10: declare the uniformity statistic $C$ so it can be computed

File: `papers/core_trilogy/Spectral_Witness_Refinement.tex:267-269` and `:290`.

Current text: "For the windowed observable $F_w=K_w[\rho]+E_w$ with $\|E_w\|=O(1/N)$ …" and
"The constant $C(\rho,q,d)=\|E_w\|\cdot N$ is controlled only above a height floor"; falsifier at `:290`:
"$S_4$ Artin-$L$ zeros to height $\sim5000$, test boundedness of $C$."

Reason: $K_w[\rho]$, the window $w$ and its normalisation $W$, the norm $\|\cdot\|$, and the meaning of $N$
are not defined in the paper (grep for `K_w`/`E_w` finds only `:267` and `:269`; the reproducible driver
at `:447-449` computes only $T_{\min}$). The falsifier cannot be run as written. Also, the height target
$\sim5000$ comes from the scaling law $T_{\min}=(2\pi e)^d/q$, falsified at $d=2$
(`docs/Elimination_Ledger.md:428-456`); the corrected floor $2\pi e\,q^{-1/d}$ at $d=3$, $q=229$ is $2.79$.

```latex
\section*{Amendment: definition of the uniformity constant and the corrected height target}
The constant $C$ of \S10 is to be read with the following declarations, absent from the original text.
The window $w$ is the Hann taper of \S2 with $W=\sum_k w(\gamma_k)$; $K_w[\rho](\omega)=\frac1W\int
w(t)\,\bar\rho(t)\,e^{-i\omega t}\,dt$ with $\bar\rho(t)=\frac{d}{2\pi}\log\frac{q^{1/d}t}{2\pi e}$;
$E_w=F_w-K_w[\rho]$; $\|E_w\|=\sup_{0<\omega\le\omega_{\max}}|E_w(\omega)|$ for a declared
$\omega_{\max}$; and $N=N(T)$ is the certified zero count below the cutoff $T$. With these, $C(T)=N(T)\,
\|E_w\|$ is computable from any certified ordinate list. The height target $\sim5000$ for $S_4$ rested
on the scaling law $T_{\min}=(2\pi e)^d/q$, which was falsified at $d=2$; the corrected main-term floor
$2\pi e\,q^{-1/d}$ is $2.79$ for conductor $229$. The falsifier is restated as: for a certified $S_4$
Artin-$L$ list (conductor 229), compute $C(T)$ at increasing $T$ and test whether it stays bounded.
```

# Proposed amendments — 22 October 2026, pass 2 (condensate and carrier)

Paste-ready proposals for manifest-bound files from the condensate and carrier cards
(`docs/open_problems_2026-10-22.md`, section "Condensate and carrier"). Nothing here has been
applied; every target is listed in `docs/publication/2026-09-24/publication-manifest.json` or is a
`papers/**/*.tex`, so the integrity gate is the owner's to clear. Line numbers are at commit
`8b9ba94`. Written by agent session `condensate-carrier`.

## 1. Flag-condensate and T_{B−L} notes: the §3.1 restriction clause (Card C2)

**Targets** (all `papers/notes/*.tex`, manifest `grep -c` ≥ 1 or papers): `Flag_Condensate_Nuclear_Decay.tex`
(after line 294), `Flag_Condensate_Palpha_Overlap.tex` (after line 220), `Flag_Condensate_Palpha_Refined.tex`
(after line 433), `Flag_Condensate_Palpha_Throat_Overlap.tex` (after line 285), `Klein_Foam_Monad.tex`
(after line 336), `Pythagorean_Lattice_Limits.tex` (after line 378),
`Adjoint_Clifford_Signature_Selection.tex` (after line 725). The core trilogy uses of $T_{B-L}$
(`Palatini_Gauge_Attractor.tex` lines 228, 2847–2849; `Holographic_Spectral_Inversion.tex` lines 594–626;
`Spectral_Witness_Refinement.tex` line 243) are algebraic and do not draw a stability conclusion; the
owner may add the same sentence there or not.

**What it corrects.** `papers/updates/ACS_Condensate_Carrier_Boundary.tex` lines 153–160 restrict the
scalar binding result ("These classical modes invalidate using the massive scalar threshold alone as a
full-theory stability certificate"), but no note that cites the binding result or uses the same
$T^{15}$ charge carries the restriction: `Flag_Condensate_Nuclear_Decay.tex` line 294 names "a specified
charge and free-wave threshold" only, and the other six carry only the generic pointer paragraph.

**Placement.** Inside each note's existing `\section*{Amendment: scope and evidence, 24 September 2026}`,
as a new final paragraph before the "For the complete-action and microscopic-carrier audit" pointer.

```latex
\paragraph*{Restriction carried from the carrier audit, 22 October 2026.}
Where this note relies on the conditional scalar binding result, or on the $T^{15}\propto T_{B-L}$
charge of the selected $\Delta$ component, the carrier audit's \S3.1 applies: at the exterior
background $\Phi=I_2/2$, $\Delta=0$ the gauge group $SU(4)$ is unbroken, the 21-generator vector
mass Gram has eighteen zero eigenvalues, and three complex colour--lepton vector pairs are massless
with $T^{15}$ weight $2/3$ of the selected $\Delta$ component's. The massive scalar threshold is
therefore not a full-theory stability certificate at that background. The Lie-algebraic statements
about $\mathrm{ad}_{T_{B-L}}$ used here (spectrum $\{0,\pm4/3\}$, $\mathrm{ad}^3=(16/9)\,\mathrm{ad}$,
charge ratio $1/3$) are vacuum-independent and unaffected; no non-Abelian decay width or confinement
conclusion is drawn.
```

## 2. Framing Transformer note: which branch of the stability–quantisation fork the note takes (Card C5)

**Target.** `papers/notes/Framing_Transformer_Spin_Parity.tex` (manifest `grep -c` = 1 or papers), lines
551–556: "Maximal dynamical stability and topological quantisation pull in opposite directions on a torus.
Any model that wants both owes an account of which it is choosing."

**What it corrects.** The account is owed and not given anywhere in the corpus. The note's own content
answers it: every result (self-linking, the $\mathbb Z/2$ parity, the lift) requires a closed curve and
hence a rational winding, and no result uses KAM stability of the curve. This proposal records that
reading; it is the agent's reading of the mathematics, not an owner decision, and the owner may instead
declare the other branch.

**Placement.** A new sentence at the end of the existing `\section*{Amendment: scope and evidence,
24 September 2026}` paragraph (line 637), before the pointer paragraph.

```latex
\section*{Amendment: the stability--quantisation fork, 22 October 2026}
Section~\ref{sec:lit}'s question of which branch a model chooses is answered for this note by its own
results: every statement here requires a closed centerline and hence a rational winding, so the note
takes the topological-quantisation branch and makes no claim of dynamical (KAM) stability for the
curve. Whether a dynamical model of the same object should prefer the noble windings is left open and
is not addressed by any calculation in this repository.
```

(`\label{sec:lit}` is the label of the "Relation to the established literature" section, lines 559–560.)

## 3. Möbius Ribbon Capacitance note: the BIE row at the CODATA aspect (Card C6)

**Target.** `papers/notes/Mobius_Ribbon_Capacitance.tex` (manifest `grep -c` = 2), line 203: `BIE & ---
& not resolved at that aspect \\`.

**What it corrects.** Nothing false; the row is correct. The audit
(`docs/capacitance_normalization_audit_2026-10-22.md`) measured what the instrument returns outside its
window with the scan mesh ($\alpha^{-1}=0.4219$ at $a/R=5\times10^{-3}$, $0.5636$ at $10^{-10}$,
$1.2941$ at $10^{-50}$, against the annulus closed form $59.10$ at $10^{-50}$) and found the BIE $\hat C$
not converged in the mesh at $a/R=0.05$ (1.1% change from 288 to 512 panels), so the row can say why
it is blank and the printed six digits of $\alpha^{-1}_{\rm BIE}$ can carry their uncertainty.

**Placement.** Replace line 203, and add one sentence after the demo table's paragraph at lines 188–192.

```latex
BIE & --- & not resolvable by this discretisation (see amendment) \\
```

```latex
\section*{Amendment: BIE resolution, 22 October 2026}
The constant-panel BIE value at $a/R=0.05$ is mesh-dependent at the percent level
($\hat C=8.49$, $8.43$, $8.34$ at $200$, $288$ and $512$ panels), so its $\alpha^{-1}$ is quoted to
no better than two significant figures ($0.37$). Run outside its declared window with the scan mesh,
the instrument returns $\alpha^{-1}_{\rm BIE}=1.29$ at $a/R=10^{-50}$ where the annulus closed form
gives $59.1$: the CODATA-matching aspect of the log-ring models is not resolvable by this
discretisation, which is why the table row is blank. This is a statement about the instrument, not
about the ribbon.
```

## 4. Endpoint audit README: the Phase-6 replay rerun at 1,500 seconds (Card C7)

**Target.** `docs/condensate_energy/endpoint_audit/README.md` (manifest `grep -c` = 1), lines 16–19
("The incomplete replay hit a 60-second symbolic-solver limit"), 109–112 ("Its full replay timed out in
the symbolic four-quartic solve") and 298 ("The original failed driver is in `attempts/phase6-timeout-60s/`.").

**What it adds.** A dated execution record, nothing more: the unchanged source replay was rerun on
23 October 2026 with the limit raised from 60 s to 1,500 s and did not complete, and the stage is
identified. Nothing in the existing text is wrong; the 95 passing checks and the exact two-root result
are untouched. The file is Markdown, so the paragraph is in its convention rather than
`\section*{Amendment: ...}`.

**Placement.** A new paragraph after line 121 (the end of the two-root paragraph that begins at line
109), and one sentence appended to line 298.

```markdown
**Replay rerun, 23 October 2026.** The unchanged `source-snapshots/phase6_dynamics.py`
(sha256 `04ebb30b…1a6ee`) was run from a scratch copy with one BLAS thread and a 1,500-second
kill limit (Python 3.12.3, SymPy 1.14.0, NumPy 2.2.6). It was killed at 1,500 s (exit 137) at the
same stage as the 60-second attempt, inside the four-quartic `solve` at source line 361, with 163
lines printed, an empty stderr and resident memory past 2 GB and still growing. A separate probe
of the same four polynomials finds the lex Gröbner basis in 0.01 s and exactly twelve complex
solutions, two of them real; the stage that does not return is the solver's expression of those
roots in radicals. The replay therefore remains incomplete at twenty-five times the original
limit. This is a dated execution record, not a change to the 95 passing checks or to the exact
two-root result.
```

For line 298, one of the two sentences below, which is the owner's choice (Card C7(5)):

```markdown
A 1,500-second rerun on 23 October 2026 reached the same stage and was killed; the unchanged
source will not be rerun again.
```

```markdown
A 1,500-second rerun on 23 October 2026 reached the same stage and was killed; any completing
replay will use a documented one-line edit of the solver call and be labelled a modified replay.
```

## What this block leaves out

- No proposal for `papers/updates/ACS_Action_Identifiability.tex` or
  `papers/updates/ACS_Condensate_Carrier_Boundary.tex`: their replay and §3.1 wording is the reading
  the record supports and needs no change; §1 propagates §3.1 outward, it does not amend it.
- No proposal for `docs/CONDENSATE_EVIDENCE.md` (not manifest-bound): the heading-to-input map of
  Card C4(4) can be applied directly in a later pass.
- No proposal closing the geometric g route in `docs/Elimination_Ledger.md` (not manifest-bound):
  Card C5(4) leaves that as an owner decision, and a ledger entry should follow the decision, not
  precede it.
