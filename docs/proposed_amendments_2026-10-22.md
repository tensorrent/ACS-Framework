# Proposed amendments to the manifest-bound manuscripts, 22 October 2026

**Date:** 2026-10-22 · **Author:** agent session, item `E-proposals-papers` · **Target repo:**
`tensorrent/acs-framework`, read at `8b9ba94` (branch `claude/surrogate-discriminant-amendments`).

**These are proposals.** Each item carries paste-ready LaTeX in the papers' own
`\section*{Amendment: ...}` convention, so applying one is a copy and not a rewrite.
**Nothing below has been applied to any file under `papers/`.** Every target is listed in
`docs/publication/2026-09-24/publication-manifest.json`
(`grep -c "<path>" docs/publication/2026-09-24/publication-manifest.json` = 2 for each of
`papers/core_trilogy/Palatini_Gauge_Attractor.tex`,
`papers/core_trilogy/Holographic_Spectral_Inversion.tex`,
`papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`,
`papers/Form_Function_and_Asymmetry.tex`, `papers/ACS_Deterministic_AI_Stack_PDR.tex`,
`papers/later_FF06_series/The_Reversible_Flattening.tex`,
`papers/notes/Critical_Line_As_Fibered_Object.tex`, `papers/discrete_geometry_formalism.tex`),
so applying any of them changes a preserved hash; the integrity gate is the owner's to clear.
This file itself is not in the manifest (`grep -c` = 0), nor are `MANIFEST.md` and
`docs/Elimination_Ledger.md` (0 each).

Shape follows the precedent `AISO:docs/research/ACS_PAPER_AMENDMENTS_2026-10-21.md`. The
sibling file `docs/proposed_amendments_2026-10-22_pass2.md` already covers two adjacent
points, cited where they touch an item here: its §1 (Paper A, Appendix B, the RG-scale
sentence) and its second-part §2 (the `docs/witness_perspective/` path).

**How every citation was checked.** Each `file:line` below was read with `sed -n` at
`8b9ba94` and each quoted string re-grepped (`grep -nF`) in the cited file after this
document was written; the verification list is in the item report, not here. Two things
were executed, both outside the tree: `code/acs_codebase/extras/lemma29_verify.py` was run
from a scratch directory with the pinned interpreter (item 12), and one member of
`docs/frontier/2026-09-11/ACS_Frontier_Evidence.zip` was extracted into a scratch directory
and read (items 6, 9, 10). `git status --short` in the worktree was empty after both.
Nothing else was computed; where a claim could not be checked it says so.

Items, keyed to the review list they answer:

| # | key | target |
|---|---|---|
| 1 | E2 | Paper A: the 10 / 6 / 6 counts |
| 2 | E2 | Paper C: "5 quartic couplings to 2 free + 1 radiative" |
| 3 | E3 | Paper B §5: the 0.044 bridge, and the truncated 24 September amendment |
| 4 | E4 | Paper C gap (10): tan β "is open" against MANIFEST T4 |
| 5 | E6 | Form, Function and Asymmetry: fixed points ↔ ΔI = 0 after Q4 was retired |
| 6 | E6 | PDR: the information-balance halting row |
| 7 | E8 | The Reversible Flattening: the two "iff"s |
| 8 | E8 | Fibered-object note: the recalled "iff" |
| 9 | E9 | Discrete geometry formalism: "not a functor" vs "observable functor"; the D03 counter-witnesses |
| 10 | E19 | MANIFEST rows for the PDR and the discrete geometry formalism |
| 11 | D22 | Fibered-object note: the corrected reference for `docs/witness_perspective/` |
| 12 | A3 | Form, Function and Asymmetry, Appendix B: link `lemma29_verify.py` |

---

## 1 · Paper A — the "10 independent quartic couplings" and the two "6 inputs" (E2)

### 1.1 What the paper says

`papers/core_trilogy/Palatini_Gauge_Attractor.tex`:

- `:2778-2782` (§`sec:boundary`, "The irreducible boundary"): "The Pati--Salam Higgs
  potential ($\Phi + \Delta_R$) has approximately 10 independent quartic couplings.  The
  bracket algebra and consistency filters described in \S\ref{sec:self-pruning} together
  fix or exclude seven of them, leaving four free parameters in the minimal bi-doublet
  (Branch~A)."
- `:2825-2828`: "With 2 calibrations and 4 free parameters, the Branch~A model has
  \textbf{6 total inputs} versus the SM's $19+$, a reduction factor of approximately
  $3.2\times$."
- `:2916-2920` (caption of `fig:hero`, `:2921`): "and leaves 3 parameters free ($\rho_1$,
  $\alpha_1$, $\tan\beta$ radiative), for a total of 6 inputs (vs.\ $19{+}$ in the SM)."

Two further observations, recorded because an amendment that restates the counts should not
inherit them. The paragraph headings of §`sec:boundary` tally "Locked by Palatini bracket
structure (5)" (`:2784`), "Forbidden by representation theory (1)" (`:2792`), "Excluded at
tree level by flavor phenomenology (1)" (`:2799`), "Free at tree level (3)" (`:2806`) and
"Calibrations (2)" (`:2823`): the free list names three parameters where `:2826` counts
four, and the five "locked" items include $g_4$, $\tilde h/h$ and $N_{\rm gen}$, which are
not quartic couplings. And `:2060-2061` introduces "five independent quartic couplings
$\{\lambda_\Phi, \rho_1, \rho_2, \alpha_1, \alpha_2, \beta_c\}$": the displayed set has six
members.

### 1.2 What supersedes it

The 24 September audit, `papers/updates/ACS_Action_Identifiability.tex`:

- `:22-25` (abstract): "The calculation retains 68 real scalar coordinates, 17 real quartic
  coefficients, four quadratic coefficients and the trace kinetic metric. Six quartic
  directions are invisible on the neutral background family."
- `:70`: the quartic sum runs over $\lambda_j I_{4j}$, $j=0,\dots,16$.
- `:127-129`: "The entire neutral restriction has quartic rank eleven. The missing six
  directions are $I_6,I_8,I_9,I_{10},\Rea H_\Delta,\Ima H_\Delta$. The first four affect
  transverse masses."

The dated record already states the consequence for *other* papers:
`docs/publication/2026-09-24/amendments.json:7-8` (entry for
`papers/Form_Function_and_Asymmetry.tex`): "The complete scalar sector contains 17 quartic
and four quadratic coefficients; six quartic directions are invisible on the neutral family.
[...] Earlier reduced parameter counts apply only to their stated ansatz." Paper A's own
24 September amendment (`:2979-2988`) says only "The complete scalar action and physical
vacuum still require coefficients, kinetic normalization and a selection rule." and does
not mention the counts, so a reader of Paper A alone still meets 10, 6 and 6 unqualified.
`MANIFEST.md:84` already reads the question "6 → 5 inputs?" as "**superseded as posed, not
open**".

Pass 2's §1 proposes a Paper A amendment at the same place about the RG-scale sentence and
"No free parameters" (`docs/proposed_amendments_2026-10-22_pass2.md:30-47`); it does not
restate the 10 / 6 counts, so the two blocks are complementary and can both be pasted.

### 1.3 Placement and paste-ready block

After the existing `\section*{Amendment: scope and evidence, 24 September 2026}` block
(`:2979-2988`), before `\begin{thebibliography}{99}` (`:2990`).

```latex
\section*{Amendment: the quartic and input counts, 22 October 2026}
The counts in \S\ref{sec:boundary} and in the caption of Figure~\ref{fig:hero} ---
``approximately 10 independent quartic couplings'', ``\textbf{6 total inputs}'' and
``a total of 6 inputs (vs.\ $19{+}$ in the SM)'' --- are counts taken inside the reduced
minimal-bi-doublet ansatz of \S\ref{sec:self-pruning}. They are not counts of the
Pati--Salam scalar sector. The companion paper \emph{Complete Scalar Actions and
Identifiability Boundaries in the ACS Framework} (\texttt{papers/updates/}) audits the
complete sector and retains 68 real scalar coordinates, 17 real quartic coefficients
$\lambda_0,\dots,\lambda_{16}$ and four quadratic coefficients. Six of the quartic
directions ($I_6,I_8,I_9,I_{10},\operatorname{Re}H_\Delta,\operatorname{Im}H_\Delta$) are
invisible on the neutral background family, on which the quartic rank is eleven, and the
first four of them change transverse masses. The ``reduction factor of approximately
$3.2\times$'' compares an ansatz count with the Standard Model's and is withdrawn as a
statement about the framework. The algebraic results retained in this paper
($\lambda_\Phi=2\sqrt3/27$, $2\rho_1+\rho_2=16/9$, $\alpha_2=0$ by representation theory,
the tree-level $\beta_c$ no-go) keep their stated scope. The list introduced in
\S\ref{sec:self-pruning} as ``five independent quartic couplings'' displays six symbols,
and the ``4 free parameters'' of \S\ref{sec:boundary} are listed there as three; both
tallies are superseded by the audited count above rather than repaired. A parameter count
is a property of the ansatz in which it is taken, not a uniqueness statement about the
physical action.
```

---

## 2 · Paper C — "The reduction from 5 quartic couplings to 2 free + 1 radiative" (E2)

### 2.1 What the paper says

`papers/core_trilogy/Holographic_Spectral_Inversion.tex`, inside
`\subsection{Gaps revealed by formalisation (updated status)}` (`:758`), items (10)–(11) of
the enumerate opened at `:767`:

- `:855-856` (item (10)): "Total inputs: 4 free + 2 calibrations = 6 (vs.\ $19{+}$ in the
  SM, a reduction factor of $\sim 3.2\times$)." The list just above it (`:845-853`) names
  "Free at tree level: $\rho_1$, $\alpha_1$." and "Radiatively generated: $\tan\beta$" —
  three, where the total counts four, as in Paper A (item 1).
- `:861-862` (item (11)): "The reduction from 5 quartic couplings to 2 free + 1 radiative
  proceeds through three independent consistency filters".

### 2.2 What supersedes it

Paper C's own 24 September amendment already carries the audited number, `:1018`:
"Reduced scalar-potential formulas apply only to their restricted ansatz: the complete
invariant audit has 17 quartics, hidden transverse directions and nontrivial running." It
does not say which passages that sentence governs; items (10) and (11) sit 160 lines
earlier under a heading that reads as current status ("updated status"). The audited counts
are those quoted in item 1.2 (`papers/updates/ACS_Action_Identifiability.tex:22-25,
:127-129`).

### 2.3 Placement and paste-ready block

After `:1026` ("historical experiment or a proof of RH."), before
`\section*{Author Statement, ...}` (`:1028`).

```latex
\section*{Amendment: the quartic count in the gap list, 22 October 2026}
Items (10) and (11) of the updated gap list --- ``Total inputs: 4 free + 2 calibrations
= 6'' and ``The reduction from 5 quartic couplings to 2 free + 1 radiative'' --- count
inside the minimal-bi-doublet ansatz. The complete Pati--Salam scalar sector audited in
\emph{Complete Scalar Actions and Identifiability Boundaries in the ACS Framework} has
17 real quartic and four quadratic coefficients, of which six quartic directions are
invisible on the neutral background family and four of those change transverse masses.
``5 quartic couplings'' is the ansatz's count, not the sector's; the three consistency
filters of item (11) retain their stated scope within that ansatz, and the ``reduction
factor of $\sim 3.2\times$'' is withdrawn as a statement about the framework. The
sentence of the 24 September amendment, ``Reduced scalar-potential formulas apply only to
their restricted ansatz'', governs items (10) and (11) specifically.
```

---

## 3 · Paper B §5 — the 0.044 bridge after "not this supremum", and the truncated amendment (E3)

### 3.1 The bridge paragraph

`papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`, `\section{Finite-sample
stability}` (`:958`, `\label{sec:finite-sample}`; §5 in the compiled paper, `pdftotext`
table of contents "5 Finite-sample stability").

First passage, `:978-990`, "Cross-correlation scope correction":
"The previously printed global supremum [...] equals one for $N\ge2$: the triangle
inequality gives the upper bound, and $x=0$ attains it. Thus the reported $0.044$ at
$N=200$ is not this supremum. Any interpretation as a restricted-window statistic requires
the actual window and aggregation convention. It cannot validate the old gap-dependent
converse. The associated numerical values are retained below as historical diagnostics,
not certified global bounds."

Second passage, the next paragraph, `:991-1008`, "Arithmetic consequence: prime gap
transition statistics": "The cross-correlation bound $|C_{200}| = 0.044$ admits a
quantitative bridge to an empirical observable in prime distribution data. [...] This
empirical floor satisfies $R = 1/(1 + (N_{\mathrm{eff}}-1)\cdot|C_N|) = 1/(1 + 55 \times
0.044) = 0.292$ to three significant figures, with $N_{\mathrm{eff}} = 56$ extracted from
the empirical autocorrelation structure of the cross-class indicator. The Wronskian
non-vanishing established here is the spectral-side input; the arithmetic variance floor
is the output."

So within twelve lines the same number is "not this supremum", a "historical diagnostic,
not [a] certified global bound", and then a "bound" that is the "spectral-side input" to a
derivation. `:1052-1057` ("Historical cross-correlation at scale") repeats the first
reading: "These values are not the displayed global supremum, which is one. No universal
cancellation rate or proof of the converse is inferred from this regression."

The cited source is more careful than the paragraph that cites it.
`papers/notes/Prime_Gap_Transition_Operator.tex:234`: "The match is striking but is not a
derivation. The closure formula~\eqref{eq:closure} is not derived from the Wronskian
non-vanishing of \cite{WallaceB}; the identification of $N_{\text{eff}} = 56$ with a
quantity computed from the Riemann zero spectrum is not established; and the appearance of
$|C_N| = 0.044$ on both sides of the match is suggestive but not causal." (`:219` gives the
measured suppression as "$0.292 \pm 0.003$"; `:228-230` the same substitution.) Paper B'
(`papers/core_trilogy/Spectral_Witness_Refinement.tex`) does not carry the bridge
(`grep -n "0\.044\|0\.292\|WallaceN3"` = no lines), so the amendment is for Paper B only.

### 3.2 The truncated 24 September amendment

`:1680-1689`:

```
1687  directory. The dated publication record separates fresh portable checks
1688  from preserved archival results; it does not claim a complete rerun of every
1689  \section*{Author Statement, Neurodiversity Context, and Methodological Note on Assistive Tooling}
```

The sentence stops at "every". The other three papers in `papers/core_trilogy/` finish it:
`Holographic_Spectral_Inversion.tex:1026`, `Palatini_Gauge_Attractor.tex:2988` and
`Spectral_Witness_Refinement.tex:536` each read "historical experiment or a proof of RH."
Across the tree, `grep -rl "complete rerun of every" papers/ --include=*.tex | wc -l` = 33
and `grep -rl "historical experiment or a proof of RH" ... | wc -l` = 32; `comm -3` of the
two sorted lists names exactly `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`.
The compiled PDF therefore carries a sentence fragment immediately before the author
statement.

### 3.3 Placement and paste-ready blocks

(a) The truncation: a one-line completion, inserted between `:1688` and `:1689` so that the
paragraph matches the other 32 files, followed by a blank line as in those files.

```latex
historical experiment or a proof of RH.

```

(b) The bridge: a new `\section*` after the completed sentence and before
`\section*{Author Statement, ...}`.

```latex
\section*{Amendment: the cross-correlation bridge in \S\ref{sec:finite-sample}, 22 October 2026}
The paragraph ``Arithmetic consequence: prime gap transition statistics'' uses the value
$0.044$ at $N=200$ as a ``cross-correlation bound'' and as ``the spectral-side input'' to
the variance floor $R=0.292$. The paragraph immediately before it establishes that this
value is not the displayed supremum (which is one for $N\ge2$), that its window and
aggregation convention are not recorded, and that it is retained as a historical
diagnostic and not a certified bound. A number with that status cannot be an input to a
derivation. The companion note (\cite{WallaceN3}) states the same: the closure formula is
not derived from the Wronskian non-vanishing, the identification of $N_{\mathrm{eff}}=56$
with a spectral quantity is not established, and the appearance of $0.044$ on both sides
is suggestive but not causal. The sentence ``The Wronskian non-vanishing established here
is the spectral-side input; the arithmetic variance floor is the output'' is withdrawn.
What remains is a recorded numerical coincidence between a historical finite-$N$ statistic
and an independently measured suppression $0.292\pm0.003$; it is not an arithmetic
consequence of this paper and carries no weight toward the gap-dependent converse.
```

---

## 4 · Paper C gap (10) — tan β "is open" against MANIFEST T4 (E4)

### 4.1 What the paper says

`papers/core_trilogy/Holographic_Spectral_Inversion.tex`, item (10) of the gap list
(`:841-858`; the compiled paper prints "(10) The irreducible boundary: 6 inputs in Branch A
(minimal bi-doublet)"):

- `:852`: "Radiatively generated: $\tan\beta$ (value pending Coleman--Weinberg)."
- `:856-858`: "Whether one-loop Coleman--Weinberg corrections fix $\tan\beta$ uniquely
  (reducing the count to 5) is open."

### 4.2 What the record says

- `MANIFEST.md:63`: "| tan β gauge-protected (CW 6→5 fails) | **T4** |
  `extras/phase51_tanbeta.py`, `phase50_vacuum.py` — fermion-dominated, boundary min. Tree
  level, minimal-bi-doublet ansatz; scope as of 24 Sept 2026 in the note under this table |".
- The note under that table, `MANIFEST.md:71-94`: statement (1) "Tree level,
  minimal-bi-doublet ansatz: tan β is a gauge-protected flat direction, so the proposed
  one-loop reduction of that ansatz's six inputs to five fails — **T4**"; statement (2) the
  count "is retired by the 24 September record"; `:84` "So "6 → 5 inputs?" is **superseded
  as posed, not open**."; `:92-94` "Paper C's "is open" at
  `papers/core_trilogy/Holographic_Spectral_Inversion.tex:856-858` is manifest-bound; a
  dated amendment is proposed, not applied."
- Paper A itself, `papers/core_trilogy/Palatini_Gauge_Attractor.tex:2185-2195` (table
  `tab:branch-A-ledger`): "The $\tan\beta$ direction is perturbatively protected by
  Pati--Salam gauge symmetry in the minimal bi-doublet sector [...] $\tan\beta$ is therefore
  not lifted by perturbative corrections in this sector; resolving it requires a non-minimal
  Higgs sector (e.g.\ Branch~B with $\Sigma \sim (15,1,1)$) or non-perturbative effects."
- The residue is a different question with no selector in the record: `MANIFEST.md:85-91`
  quotes `docs/condensate_energy/radiative_flat_modes/README.md:10,223-226` ("conditional
  results for specified boundary couplings"; does "not close [...] recovery of an ACS
  construction that fixes the inputs").
- `docs/adjudication_2026-10-22.md:87-116` (row A-15) reaches "Superseded as posed" and says
  "a paste-ready amendment was drafted with this note and is not applied". I could not find
  that draft: `grep -rn "section\*{Amendment" docs/*.md docs/proposals/*.md` returns only the
  five blocks of `proposed_amendments_2026-10-22_pass2.md`, none for Paper C. The block
  below supplies it.

### 4.3 Placement and paste-ready block

Same placement as item 2 (after `:1026`, before the author statement); it can be pasted as
the paragraph following item 2's block or as its own section.

```latex
\section*{Amendment: the status of $\tan\beta$ in gap (10), 22 October 2026}
Gap (10) lists $\tan\beta$ as ``Radiatively generated [...] (value pending
Coleman--Weinberg)'' and asks whether one-loop corrections fix it uniquely, ``reducing the
count to 5'', calling this open. Two statements replace that status. First, at tree level
in the minimal-bi-doublet ansatz the $\tan\beta$ direction is a gauge-protected flat
direction (Paper~A, Branch~A ledger): $\tilde h/h$ is a one-loop RG invariant, two-loop QCD
corrections rescale without reshaping the potential, and threshold corrections at $v_R$
are $\beta$-independent at leading order, so the proposed reduction from six inputs to
five fails; this is recorded as explicitly falsified (T4) in the repository manifest. The
item is therefore not ``radiatively generated'' and not open as posed. Second, the count
``6'' on which the question was posed is an ansatz count, superseded by the 17-quartic
audit of \emph{Complete Scalar Actions and Identifiability Boundaries in the ACS
Framework}. Whether the complete action selects $\tan\beta$ is a different question; the
dated record supplies no selector for it, and its radiative audit reports conditional
results for specified boundary couplings only. Gap (10) is accordingly superseded as
posed, with the residual question stated in that form.
```

---

## 5 · Form, Function and Asymmetry — fixed points ↔ ΔI = 0 after Q4 was retired (E6)

### 5.1 What the paper says

`papers/Form_Function_and_Asymmetry.tex`:

- `:1026` (table at `:1020-1032`, columns "Domain & ACS Form & ACS Function"):
  "2D QFT (c-theorem) & UV fixed point & IR RG flow \\".
- `:1149-1151`, `\begin{theorem*}[Zamolodchikov $c$-theorem~\cite{Zamolodchikov1986},
  restated in ACS language]\label{thm:c-theorem}`: "For any unitary 2D QFT, there exists a
  function $C(g)$ on coupling space such that $dC/dt \leq 0$ along RG flow, with equality
  if and only if the theory is at a fixed point.  At fixed points, $C$ equals the Virasoro
  central charge $c$.  In the ACS framework, fixed points correspond to $\DI = 0$
  (information balance between UV Form and IR Function)."

The paper's definition of $\DI$ is a transfer-entropy difference (`:328`: "$\DI = 0$ is the
symmetric (Abelian) case."; `:685`: "When $f \equiv g$ (symmetric coupling), $\DI = 0$ and
$[f,g] = 0$."). Its 24 September amendment (`:2326-2327`) addresses the scalar-sector count
and cross-domain maps; it does not mention the $c$-function reading.

### 5.2 What the ledger says

`docs/Elimination_Ledger.md`:

- `:67`: "**Q4-TARGET — ΔI = c-function (FF06Σ Link 3).**"
- `:360`: "### Q4 ΔI ≡ c — **identity falsified as stated (T2); monotonicity-analogy is
  the survivor**".
- `:366-373`: "Under (b) the *identity* faces three structural mismatches, none about
  boundedness: (1) **sign** — c≥0, but a TE difference is signed; (2) **fixed-point value**
  — at a symmetric fixed point TE(F→G)=TE(G→F) ⟹ ΔI=0, while c=central charge≠0 (e.g.
  1/2); (3) **category** — TE is a temporal directed-info-flow quantity; c is
  static/spatial (Zamolodchikov / Casini–Huerta). Identity dead as stated (T2). What
  *survives* is the **monotonicity analogy** [...] So the defensible content is ΔI *plays
  the role of* c (monotone along flow), not ΔI = c numerically."
- `:402-403` (scorecard): "KILLED: [...] **Q4 identity-as-stated (T2)**." /
  "SURVIVED/INVARIANT: [...] Q4 monotonicity-analogy".
- `:418-420`: "transfer entropy is undefined on a static, time-translation-invariant ground
  state and vanishes by symmetry on a symmetric bipartition."
- `:422-426`: "**Q4 fully closed.** Every reading accounted for: the conjecture ΔI ≡ c is
  FALSE/ill-defined under the framework's own TE-asymmetry definition, or a RESTATEMENT of
  an established theorem (Casini–Huerta) under the MI definition. No reading is both novel
  and true."

The theorem environment at `:1149` presents the ΔI sentence inside a restated theorem; the
ledger's verdict is that the identity is false as stated and the fixed-point value is one
of the three reasons. The table row at `:1026` assigns the fixed point and the flow to
Form and Function, which is the analogy the ledger allows and not the identity it retired;
it needs the label, not a change of content.

### 5.3 Placement and paste-ready block

After the 24 September block (`:2326-2335`), before `\section*{Author Statement, ...}`
(`:2337`).

```latex
\section*{Amendment: the $c$-theorem restatement and $\DI=0$, 22 October 2026}
The sentence in the restated $c$-theorem, ``In the ACS framework, fixed points correspond
to $\DI = 0$ (information balance between UV Form and IR Function)'', and the table row
assigning the $c$-theorem's UV fixed point to Form and its IR flow to Function, are
organising analogies and not part of the theorem. The identification $\DI\equiv c$ was
tested in the repository's Elimination Ledger (target Q4) and retired: with $\DI$ defined
as a transfer-entropy difference, $\DI$ is signed where $c\ge0$, vanishes at a symmetric
fixed point where $c$ is a nonzero central charge, and is a temporal directed quantity
where $c$ is static; transfer entropy is moreover undefined on a static ground state. What
survives is the monotonicity analogy --- $\DI$ decreasing along its flow as $c$ decreases
along RG flow --- which is the content the restatement may carry. The $c$-theorem itself,
its 4D analogue and all cited results stand unchanged; ``fixed points correspond to
$\DI=0$'' is to be read as ``the symmetric case $f\equiv g$ of the ACS has $\DI=0$'', a
statement about the ACS and not about conformal fixed points.
```

---

## 6 · PDR — the information-balance halting row (E6)

### 6.1 What the paper says

`papers/ACS_Deterministic_AI_Stack_PDR.tex`:

- `:281` (layer mapping table): "Information balance \texttt{ΔI\ =\ 0} & Halting criterion \\".
- `:699-703` (`\subsection{The ΔI Monitor}`): "**Purpose.** Detect convergence via
  information balance. A computation that reaches \texttt{ΔI\ →\ 0} has found its attractor
  and should halt." The interface comment at `:717` defines "ΔI = TE(F → Φ) {-} TE(Φ → F)"
  with a k-nearest-neighbour estimator (`:719-720`).
- `:734-736` (halting policy, rule 1): "\texttt{\textbar{}ΔI\textbar{}\ \textless{}\ ε}
  over the last 8 steps --- information-balance attractor".
- `:1494-1495` (traceability table): "Information-balance halting & \texttt{ΔI\ =\ 0}
  attractor & Paper A §2.3 Lemma 2.10 \\".

### 6.2 What the record says

Three things bear on the row.

(a) The cross-reference does not point at an attractor statement. In the compiled Paper A,
Lemma 2.10 is the BCH–TE morphism (`pdftotext papers/core_trilogy/Palatini_Gauge_Attractor.pdf`:
"Lemma 2.10 (BCH–TE morphism). Let f, g be smooth vector fields on a compact Riemannian
manifold M"; source `papers/core_trilogy/Palatini_Gauge_Attractor.tex:561`), a Taylor
expansion of $\DI(\varepsilon)$. The word "attractor" with $\DI=0$ is in §3.3 "Ricci flow
as ACS dynamics" (`:859`; `:877-878`: "$R = 0$ (flat): information balance ($\DI = 0$, the
attractor for Ricci-flat flow)"), a statement about Ricci flow.

(b) The fixed-point reading that would make $\DI=0$ a general convergence signature is the
one retired in item 5 (`docs/Elimination_Ledger.md:360-374, :422-426`).

(c) The frontier record supplies a direct counterexample to the halting rule.
`docs/frontier/2026-09-11/workstreams/foundations/report.md:69-75`: "The PDR explicitly
says to halt when the signed information difference approaches zero [...]. The
deterministic map $(x,y)\mapsto(y,1-x)$ cycles through $(0,0),(0,1),(1,1),(1,0)$. Under its
stationary uniform law both directional current-state TEs equal 1 bit, so their difference
is zero. Successive states remain exactly unit distance apart. [...] This refutes the
general halting implication, while making no claim that this finite map satisfies every
smooth-field ACS hypothesis." The receipt is archived, not loose: the path named in
`Branch_Events.jsonl:283` (`workstreams/foundations/attempts/20260911T221928192942Z/information_geometry/result.json`)
does not exist in the tree (`ls` fails), but the same member is inside
`docs/frontier/2026-09-11/ACS_Frontier_Evidence.zip` under
`acs-parallel-frontier-20260911/fresh_replays/20260911T223024125699Z/extracted/foundations/attempts/20260911T221928192942Z/information_geometry/result.json`
(9242 bytes). Extracted to scratch and read: key `I05.PDR_monitor_counterexample` records
`"TE_X_to_Y": {"entropy_identity_bits": 1.0, "conditional_likelihood_bits": 1.0}`, the same
for `TE_Y_to_X`, `"delta_I_bits": 0`, `"successive_squared_distance": [1, 1, 1, 1]`, and
`"scope": "A counterexample to the PDR generic information-balance halting rule; no claim
that this finite cycle satisfies every smooth ACS definition."` The report's suggested
replacement is a contraction certificate (`report.md:77-83`:
$\|z-z_*\|\le\|z-Tz\|/(1-q)$, test operator with $q=3/8$).

The PDR's own 24 September amendment (`:1684`) says the release checks "do not certify
production security or benchmark generalization"; it does not reach the halting rule.

### 6.3 Placement and paste-ready block

After `:1692` ("historical experiment or a proof of RH."), before
`\section*{Author Statement, ...}` (`:1694`). The PDR is pandoc-generated LaTeX and writes
the symbol as `\texttt{ΔI}`; the block keeps that idiom.

```latex
\section*{Amendment: the information-balance halting rule, 22 October 2026}
The halting rule ``\texttt{|ΔI| < ε} over the last 8 steps --- information-balance
attractor'' and the traceability row ``Information-balance halting / \texttt{ΔI = 0}
attractor / Paper A \S2.3 Lemma 2.10'' rest on reading \texttt{ΔI → 0} as a signature of
convergence. That reading is not supported. Lemma~2.10 of Paper~A is the BCH--TE
expansion of \texttt{ΔI} in the coupling and contains no attractor statement; the
``attractor'' phrase in Paper~A belongs to its Ricci-flow section. The identification of
\texttt{ΔI = 0} with a fixed point was tested as Elimination Ledger target Q4 and retired.
And the frontier foundations record (11 September 2026, items I05/I07) exhibits a
deterministic four-cycle $(x,y)\mapsto(y,1-x)$ on which both directional transfer
entropies equal one bit, so \texttt{ΔI} is exactly zero at every step, while successive
states stay at unit distance: a computation can satisfy the rule and never converge.
The \texttt{ΔI} monitor is retained as one engineering heuristic whose estimator,
window and threshold are implementation choices; it is not a correctness criterion. A
halting decision that is to mean convergence requires a certificate of the kind the
frontier record names --- a declared contraction factor $q$ with the residual bound
$\|z-z_*\|\le\|z-Tz\|/(1-q)$, or an equivalent Lyapunov condition derived from the
actual update map --- and the traceability row should cite that requirement rather than
Lemma~2.10.
```

---

## 7 · The Reversible Flattening — the two "iff"s (E8)

### 7.1 What the paper says

`papers/later_FF06_series/The_Reversible_Flattening.tex`:

- `:75-77` (the thesis, in a `quote`): "The algebraic flattening of a relational object
  into a scalar is \emph{losslessly reversible} if and only if the operation that produces
  the scalar is a homomorphism from the object's structure into a structure the relational
  representation stores directly."
- `:94-96` (`\begin{criterion}[Homomorphism]`): "The flattening of an operation $\star$ is
  reversible exactly when $\star$ is a homomorphism $(\text{objects},\star)\to(\text{stored
  relational structure},\oplus)$."

The paper's 24 September amendment (`:263-264`) adds the injectivity requirement
("Reversibility requires an injective encoding on the stated domain and a defined inverse
on its image. Preservation of one operation alone is insufficient to establish lossless
reconstruction. The later monograph's domain restrictions govern the general reading of
this short paper.") but leaves both "iff"s in the body and does not state that the
converse was falsified or by what.

### 7.2 What the record says

The Process Record, `papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex`:

- `:152-154`: "\textbf{Biconditional (``iff'').} The first form claimed reversibility
  \emph{if and only if} a homomorphism existed. The converse was never supported and was
  eventually \emph{falsified} outright (Cantor pairing, Section~\ref{sec:gauntlet}).
  Contracted to one-way implication."
- `:291-296` ("Round 3 --- counterexample (converse falsified)"): "A direct search for a
  reversible map that is \emph{not} a homomorphism produced the Cantor pairing: a bijection
  $\mathbb{N}^2\to\mathbb{N}$, perfectly reversible, yet $\pi(1,2)=8$, $\pi(2,0)=3$,
  $\pi(3,2)=17$, and $8+3=11\ne 17$ --- it does not carry componentwise addition. The
  converse of the criterion is therefore \emph{false} (\Tf). This forced the
  pre-specified-target qualifier (the vacuity guard)."
- `:334` (table): "Criterion converse (reversible $\Rightarrow$ homomorphism) & Cantor
  pairing: reversible, not a homomorphism. \\"

The Monograph, `papers/later_FF06_series/The_Reversible_Flattening_Monograph.tex:52-54`,
gives the repaired statement: "sharpened by a $30$-domain predictive test to require an
\emph{injective} homomorphism into a \emph{pre-specified} structure (homomorphism carries
density; injectivity carries identity), a one-way implication whose converse is falsified
by the Cantor pairing"; `:373` lists the converse at T4. The arithmetic was re-checked by
hand from $\pi(a,b)=\tfrac{(a+b)(a+b+1)}{2}+b$: $\pi(1,2)=6+2=8$, $\pi(2,0)=3+0=3$,
$\pi(3,2)=15+2=17$, and $8+3=11\neq17$.

### 7.3 Placement and paste-ready block

After the 24 September block (`:263-272`), before `\end{document}` (`:274`).

```latex
\section*{Amendment: the two biconditionals, 22 October 2026}
The thesis (``losslessly reversible if and only if the operation that produces the scalar
is a homomorphism'') and the Homomorphism criterion (``reversible exactly when $\star$ is a
homomorphism'') are each to be read as one-way implications, and the forward direction
is to be read with two qualifiers. Forward: a flattening is losslessly reversible when the
operation that produces the scalar is an \emph{injective} homomorphism into a
\emph{pre-specified} structure that the relational form stores; the homomorphism carries
density and the injectivity carries identity, and the target must be named in advance
because ``into some structure'' is satisfied by any bijection through a transported
operation. Converse: false. The Cantor pairing $\pi(a,b)=\tfrac{(a+b)(a+b+1)}{2}+b$ is a
bijection $\mathbb{N}^2\to\mathbb{N}$, hence perfectly reversible, and is not a
homomorphism into the componentwise structure: $\pi(1,2)+\pi(2,0)=8+3=11\neq17=\pi(3,2)$.
The falsification and the resulting contraction to a one-way implication are recorded in
\emph{The Reversible Flattening: Process Record} (the counterexample round) and the
repaired statement is the one used throughout \emph{The Reversible Flattening}
(monograph); this paper's verifications of the forward direction across applied
mathematics are unaffected.
```

---

## 8 · Fibered-object note — the recalled "iff" (E8)

### 8.1 What the note says

`papers/notes/Critical_Line_As_Fibered_Object.tex:92-96`,
`\begin{definition}[Flattening and its seam, recalled from \textit{The Reversible
Flattening}]`: "A \emph{flattening} projects a relational object (a factorization, a
divisor lattice) onto a scalar; it is \emph{reversible} iff the projecting operation is a
homomorphism into the stored relational structure." The definition is introduced as a
recollection of the short paper, so it reproduces the short paper's biconditional (item 7)
and not the monograph's one-way, injective, pre-specified-target statement.

### 8.2 Placement and paste-ready block

After the 24 September block (`:324-333`), before `\end{document}` (`:335`). It can be
combined with item 11's block for the same note.

```latex
\section*{Amendment: the recalled definition of reversibility, 22 October 2026}
The definition ``Flattening and its seam'' is recalled from the short paper \emph{The
Reversible Flattening} in that paper's original biconditional form. The form that stands
is the monograph's: a flattening is reversible when the projecting operation is an
\emph{injective} homomorphism into a \emph{pre-specified} stored structure, and this is
a one-way implication whose converse is falsified by the Cantor pairing (a reversible
bijection $\mathbb{N}^2\to\mathbb{N}$ that is not a homomorphism into the componentwise
structure). ``iff'' in the recalled definition is accordingly to be read as ``when'',
with the two qualifiers. The seam statement that follows --- convolution crossable for
density and uncrossable for identity --- is unchanged, since it concerns the forward
direction only.
```

---

## 9 · Discrete geometry formalism — "not a functor" vs "observable functor"; the D03 counter-witnesses (E9)

### 9.1 What the paper says

`papers/discrete_geometry_formalism.tex`:

- `:24` (abstract): "the nonlinear observation map (a lossy projection, deliberately not a
  functor --- no categorical structure is assumed)".
- `:62`: "Because the system lacks global functoriality, invariants do not exist as
  intrinsic geometric objects."
- `:83`: "When pushed forward through the observable functor, this yields the scheme
  dispersion metric:" — the same map $\Phi$ (`:56`: "$\Phi : \mathcal{A} \to
  \mathbb{R}^m$"), now called a functor.
- `:86-87`: the metric "rigorously measures the \textit{non-commutativity of measurement
  orderings}."

### 9.2 What the frontier record says

Branch D03, "Variance as noncommutativity and geometric ontology"
(`docs/frontier/2026-09-11/Branch_Events.jsonl:127`, sources include this paper).

- `docs/frontier/2026-09-11/workstreams/foundations/report.md:97-104`: "Lines 71–79
  identify a variance of repeated single-scheme observations with noncommutativity. This
  is directly testable: 1. On a one-point grid at $A=I_4$, let $R_P(A)=PA$,
  $P=\operatorname{diag}(-1,1,1,1)$, and let the other scheme be the identity. They
  commute. With $\Phi(A)=A_{11}^3$, equal scheme weights and $k=1$, the reported variance
  is exactly 1. 2. Take quarter-turn rotations in the 12 and 13 planes. They do not
  commute, but $\Phi(A)=A_{44}^3$ equals 1 on their entire generated orbit. Both the
  reported variance and every observed two-order defect vanish." Then: "The ambient matrix
  commutator can also leave $O(4)$, so applying the stated $\Phi$ [...] to it is generally
  undefined. A well-typed order observable is
  $\delta_{\alpha\beta}(A)=\Phi(R_\alpha R_\beta A)-\Phi(R_\beta R_\alpha A)$" (`:107`) and
  (`:112`) "adjoining an empty word yields a monoid, hence a one-object category."
- `docs/frontier/2026-09-11/ACS_Frontier_Checklist.md:30`: "| D03 | needs definition |
  Correction: the source does specify the O(4) state carrier, rewrite maps and Phi. Its
  variance/noncommutativity identity fails directly on that carrier in both directions.".
- The receipt, in the same archived `result.json` as item 6 (key `D03`, read from the
  scratch extraction): `commuting_positive_variance` with `"P": "Matrix([[-1, 0, 0, 0],
  [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])"`, `"Phi": "A[0,0]^3"`, commutator the zero
  matrix, `"declared_variance": "1"`; `noncommuting_zero_variance` with `"Phi": "A[3,3]^3"`,
  `"squared_Frobenius_commutator": "6"`, `"declared_variance": 0`,
  `"observable_order_defect": 0`, `"commutator_in_O4": false`; and
  `"semigroup_correction": "Actual endomorphisms compose associatively. Adjoining the empty
  word gives the free-word action a monoid and hence a one-object category; [...]"`.

The report cites the source at `:29–51` and `:71–79`; at `8b9ba94` the carrier definitions
are at `:36-56` and the variance identification at `:83-87` (the 24 September status
paragraph at `:26-29` and the amendment moved the lines). The paper's own 24 September
amendment (`:95-96`) concerns reconstruction and scale and does not mention D03.

### 9.3 Placement and paste-ready block

After the 24 September block (`:95-104`), before `\end{document}` (`:106`).

```latex
\section*{Amendment: the observation map and the dispersion metric, 22 October 2026}
Two corrections to the body, both from the frontier foundations review of 11 September
2026 (branch D03). First, the observation map $\Phi:\mathcal A\to\mathbb R^m$ is, as the
abstract states, a nonlinear lossy projection and not a functor; the phrase ``pushed
forward through the observable functor'' is to be read as ``evaluated through the
observation map $\Phi$''. (The word action itself, with the empty word adjoined, is a
monoid and so a one-object category; what is not assumed is any functoriality of
$\Phi$.) Second, the statement that the scheme dispersion metric ``rigorously measures
the non-commutativity of measurement orderings'' is withdrawn as an identity. On the
stated carrier it fails in both directions: on a one-point grid at $A=I_4$, the schemes
$R_P(A)=PA$ with $P=\operatorname{diag}(-1,1,1,1)$ and the identity commute, yet with
$\Phi(A)=A_{11}^3$, equal weights and $k=1$ the declared variance is $1$; and the
quarter-turn rotations in the $12$ and $13$ planes do not commute (squared Frobenius norm
of the commutator $6$), yet with $\Phi(A)=A_{44}^3$ the declared variance and every
observed two-order defect are $0$ on the whole generated orbit. The ambient commutator
need not lie in $O(4)$, so $\Phi$ of it is in general undefined. A well-typed order
observable is $\delta_{\alpha\beta}(A)=\Phi(R_\alpha R_\beta A)-\Phi(R_\beta R_\alpha
A)$, which vanishes exactly when the two ordered states agree whenever $\Phi$ is injective
on the reachable orbit. The dispersion metric is retained as a statistic of
single-scheme orbits under $\Phi$; it is not a commutator metric. The orbit-sheaf
language requires a base, restrictions and gluing to be supplied before it names a sheaf;
none is supplied here.
```

---

## 10 · MANIFEST rows for the PDR and the discrete geometry formalism (E19)

### 10.1 What exists

Neither paper has a row anywhere in the two indexes: `grep -n
"Deterministic_AI_Stack_PDR\|discrete_geometry_formalism\|PDR" MANIFEST.md` and the same
against `docs/ACS_Master_Index.md` return nothing (the MANIFEST "Papers" table, `:35-50`,
ends with "| later_FF06_series/ (8 papers) | — | June methodology/geometry thread;
documents only |"). Both are canonical manuscripts (`publication-manifest.json:5,11`) and
are catalogued at `papers/catalog.json:239-248` under the group "Monographs and
engineering" with the summaries "Engineering blueprint, not a benchmark certification." and
"Dynamical epistemic algebra formalization."; `papers/README.md:64-65` repeats both lines.
Neither `MANIFEST.md` nor `docs/ACS_Master_Index.md` is manifest-bound (`grep -c` = 0), so
these rows can be applied directly if the owner adopts them; they are given here as
Markdown in the table idioms of `MANIFEST.md:37-50` and `:56-68`.

### 10.2 Evidence for each

**Paper D, `papers/ACS_Deterministic_AI_Stack_PDR.tex`.**

- Status lines in the paper: `:191` "\textit{Architectural PDR} \quad|\quad April 2026";
  `:1666` "\textbf{Version.} 1.0 (Initial PDR)"; `:1668` "\textbf{Status.} Design review
  --- open for technical critique"; `:1670` "\textbf{Next review.} After Phase 0 exit
  criterion"; `:226-227` "Phase~1 targets full deployment of the 76-script ACS verification
  suite under the new governance within a six-month horizon." No record in the tree states
  that a Phase 0 exit criterion was met (searched `MANIFEST.md`, `docs/*.md`, the frontier
  indexes for the paper's name: hits only in `publication-manifest.json`,
  `manuscript-baseline.json`, `amendments.json`, `papers/catalog.json`, `papers/README.md`).
- Code: the "76-script" suite exists as `code/acs_codebase/extras/ACS_all_76_scripts.py`
  (`:4` "ACS VERIFICATION SUITE", `:7` "SCRIPT 1/76"), in the directory whose README says
  (`code/acs_codebase/extras/README.md:3,9`) "Heritage exploratory scripts" / "**Status:**
  unverified. Some are superseded". `grep -rl "delta_I\|is_converged\|closure_validator"
  code/` hits that file, `extras/integer_acs.py` and
  `condensate_energy/input_selector_audit.py`; the first two compute `delta_I = te_xy -
  te_yx` (`:10538`, `:234`), the third reads a `delta_I` symbol from a snapshot — none is
  the engine, the ΔI monitor or the closure validator the PDR specifies. No test in
  `code/acs_codebase/src/` names the PDR.
- Falsified element: the generic information-balance halting implication, by the frontier
  I05 counterexample (item 6.2(c), receipt in the evidence archive).
- Amendment: `:1683-1692`; `:1684` "The release checks verify manuscript integrity and
  selected calculations; they do not certify production security or benchmark
  generalization."

**Discrete geometry formalism, `papers/discrete_geometry_formalism.tex`.**

- Status: `\date{2026}` (`:15`); no version or phase line in the paper. Frontier branch D03
  status "needs definition" (`ACS_Frontier_Checklist.md:30`; `Branch_Events.jsonl:128,
  :178, :242, :283` each carry `"status": "definition_required"` or `"parent_path_status":
  "needs_definition"`), continuation condition (`:283`): "Choose source/target typing for
  order defects, a faithful observable and probability law; if using sheaf language specify
  topology, restrictions and gluing."
- Code: none in the tree implements the paper (`grep -rl discrete_geometry_formalism code/`
  = no files); the only computation against it is the archived D03 program whose
  `result.json` is quoted in item 9.2.
- Falsified element: the variance ≡ non-commutativity identification, in both directions
  (item 9.2).
- Amendment: `:95-96`.

### 10.3 Proposed rows

In the "Papers (latest version of each)" table, after the `later_FF06_series/` row
(`MANIFEST.md:50`):

```markdown
| ACS_Deterministic_AI_Stack_PDR | D | Architectural PDR, v1.0, April 2026; status "Design review — open for technical critique", next review after Phase 0 exit criterion (`:1666-1670`); no Phase 0 exit recorded; design document, no engine code in the tree |
| discrete_geometry_formalism | — | dynamical epistemic algebra on O(4)-valued rewrite orbits; document only; Frontier D03 "needs definition" (`docs/frontier/2026-09-11/ACS_Frontier_Checklist.md:30`) |
```

A new claim table after "### Notes" (`MANIFEST.md:133-146`), before the "Falsified claims
ledger" (`:149`):

```markdown
### Paper D (Deterministic AI Stack PDR) and the discrete geometry formalism
| Claim | Tier | Evidence |
|-------|------|----------|
| D — five-layer deterministic stack, replay and provenance as engineering properties | — (design) | `papers/ACS_Deterministic_AI_Stack_PDR.tex`; no implementation or test in `code/acs_codebase/src/`; the "76-script suite" it targets is `code/acs_codebase/extras/ACS_all_76_scripts.py`, heritage and unverified per `code/acs_codebase/extras/README.md:9` |
| D — ΔI → 0 (information balance) implies convergence; halting rule | **T4** | frontier I05: four-cycle (x,y)→(y,1−x), both TEs 1 bit, ΔI = 0, successive distance 1 — `docs/frontier/2026-09-11/workstreams/foundations/report.md:69-75`; receipt in `ACS_Frontier_Evidence.zip` (…/attempts/20260911T221928192942Z/information_geometry/result.json, key I05); a contraction certificate ‖z−z*‖ ≤ ‖z−Tz‖/(1−q) is the named replacement |
| D — phase status | Phase 0 (not exited) | PDR `:1668-1670`: "Design review"; "Next review. After Phase 0 exit criterion"; no exit record in the tree |
| DGF — O(4)^Γ carrier, rewrite endomorphisms, observation Φ, dispersion metric as defined | — (definitions) | `papers/discrete_geometry_formalism.tex:36-56, :83-85`; D03 correction: the definitions are present (`ACS_Frontier_Checklist.md:30`) |
| DGF — dispersion metric "measures the non-commutativity of measurement orderings" | **T4** | D03, both directions: commuting schemes with declared variance 1; non-commuting schemes (‖[R,S]‖²_F = 6) with variance 0 and order defect 0 — `report.md:97-104`, receipt key D03 in the same archived `result.json` |
| DGF — orbit sheaf | needs definition | no base, restrictions or gluing supplied; optional discrete-word completion shown constructible (8/8 finite gluings, arbitrary-cover proof) but not identified with the paper's object — `report.md:114`, receipt `sheaf_completion` |
| DGF — phase status | Frontier D03, "needs definition" | `ACS_Frontier_Checklist.md:30`; continuation condition in `Branch_Events.jsonl:283` |
```

Tier dashes are deliberate: the four-tier hierarchy (`MANIFEST.md:21-29`) has no tier for
a design specification or a definition, and inventing one would promote. The two T4 rows
are the only tiered claims the record supports.

---

## 11 · Fibered-object note — the corrected reference for `docs/witness_perspective/` (D22)

### 11.1 Confirmed

`papers/notes/Critical_Line_As_Fibered_Object.tex:86-88` (in
`\section*{Scope correction: 22 September 2026}`, `:80`): "The observer experiment in
\path{docs/witness_perspective/} shows why linear span, intrinsic dimension, and available
measurement directions must be distinguished. It does not establish such a carrier."

At `8b9ba94`: `ls docs/witness_perspective` → "No such file or directory";
`grep -rn "witness_perspective" . --exclude-dir=.git` hits only the note itself,
`docs/open_problems_2026-10-22.md:155,157` and
`docs/proposed_amendments_2026-10-22_pass2.md:112-124` (both reporting the same absence);
`find . -iname "*witness*"` returns seven unrelated files (two condensate-energy witness
scripts, three of their receipts, the Spectral Witness paper and its PDF);
`git log --all --diff-filter=A -- 'docs/witness_perspective/*'` is empty, so the directory
was never added on any local ref; `git log --all -S witness_perspective` returns only
`a51abfe` (the commit that introduced the sentence) and `58f494c` (the open-problems
file). The reference has been dangling since it was written.

### 11.2 Where the content is

The sentence summarises an argument that exists in the tree under another paper's dated
amendment. `papers/later_FF06_series/The_Geometry_Engine.tex:294-295`
(`\section*{Amendment: scope and evidence, 24 September 2026}`): "The engine computes
features relative to its declared representation and observer. Independent response
directions do not automatically measure the intrinsic dimension of an unknown source. For
example, a one-dimensional curved trajectory can span several linear directions. A physical
application must retain sensor calibration, noise alternatives and the forward map." The
same text is `docs/publication/2026-09-24/amendments.json:123-124`. That is the only place
in the tree where linear span, intrinsic dimension and measurement directions are
distinguished in these terms (`grep -rln "intrinsic dimension" docs/ code/` =
`amendments.json` only; in `papers/` only the Geometry Engine amendment). No script,
figure or data for an "observer experiment" was found.

Pass 2's second-part §2 proposes reading the sentence as an unsupported reference until the
experiment is restored. This item proposes the corrected reference instead, since the
supporting argument is published; the two are alternatives, and the owner may prefer pass 2
if an experiment with receipts is expected to be restored.

### 11.3 Placement and paste-ready blocks

(a) In place, replacing `:86-88` (the owner's choice; manifest-bound):

```latex
The point that linear span, intrinsic dimension, and available measurement directions
must be distinguished is made in the 24 September 2026 amendment of \emph{The Geometry
Engine} (\texttt{papers/later\_FF06\_series/The\_Geometry\_Engine.tex}): independent
response directions do not measure the intrinsic dimension of an unknown source, since a
one-dimensional curved trajectory can span several linear directions. It does not
establish such a carrier.
```

(b) As a dated section, after the 24 September block (`:324-333`), before
`\end{document}` (`:335`), combinable with item 8:

```latex
\section*{Amendment: the cited evidence path, 22 October 2026}
The scope correction of 22 September 2026 cites an observer experiment at
\path{docs/witness_perspective/}. No such directory exists in the published repository,
and none was ever committed. The distinction the sentence draws --- between linear span,
intrinsic dimension and the measurement directions available to an observer --- is
stated in the 24 September 2026 amendment of \emph{The Geometry Engine}
(\texttt{papers/later\_FF06\_series/The\_Geometry\_Engine.tex}): independent response
directions do not automatically measure the intrinsic dimension of an unknown source,
because a one-dimensional curved trajectory can span several linear directions. The
citation is corrected to that amendment. No experiment, script or data set stands behind
the earlier path, and the scope correction's conclusion --- that no carrier, map or proof
is supplied --- does not depend on one.
```

---

## 12 · Form, Function and Asymmetry, Appendix B — link `lemma29_verify.py` (A3)

### 12.1 What the paper says

`papers/Form_Function_and_Asymmetry.tex`, `\appendix` at `:2194`; Appendix B is
`:2235` "\section{Exact Symbolic Verification of the BCH--TE Morphism
(Lemma~\ref{lem:bch-te})}" with `\label{app:exact}` (`:2236`); the lemma is
`:475` "\begin{lemma}[BCH--TE morphism]\label{lem:bch-te}". In the compiled paper the
appendix heading is "B Exact Symbolic Verification of the BCH–TE Morphism (Lemma 2.10)"
and the lemma is "Lemma 2.10 (BCH–TE morphism)" (`pdftotext
papers/Form_Function_and_Asymmetry.pdf`).

- `:2238-2251`: the verification "for generic polynomial vector fields $f,g$ on
  $\mathbb{R}^2$", the first variation, the second variation with "the factor $2$", and
  "All cancellations were checked for generic polynomials of degree $\le 3$".
- `:2254`: "The computation script is available as supplementary material." No path or
  name is given anywhere in the paper (`grep -n "\.py"` finds only `selection_full.py`,
  `acs_verify_all.py` at `:1566` and `chirality_uniqueness.py` at `:1612`).
- Appendix C, `:2316-2321`: "\textbf{BCH--TE morphism symbolic verification
  (Lemma~\ref{lem:bch-te}, Appendix~B):} Generic polynomial vector fields $f = (ax^2,
  by)$, $g = (cx, dy^2)$ on $\mathbb{R}^2$.  Cartan formula, bracket antisymmetry, and
  factor-of-2 cancellation verified symbolically over $\mathbb{Q}[a,b,c,d]$ with all
  residuals identically zero.  Third-order BCH term $\beta_3 = (ac^2x^2/12,\; b^2dy^2/12)
  \neq 0$ for generic parameters."

### 12.2 The script, located and run

`code/acs_codebase/extras/lemma29_verify.py` (9405 bytes). Docstring `:6-9`: "Lemma 2.9
Symbolic Verification [...] Verifies the BCH-TE morphism: ΔI(ε) = ε⟨f-g, ∇log(dμ/dν)⟩ +
2ε²⟨[f,g], ∇log(dμ/dν)⟩ + O(ε³)" — the "2.9" is the lemma's number at the time the script
was written; it is 2.10 in the compiled paper. Fields `:43-46`: `f1 = a * x**2`, `f2 = b *
y`, `g1 = c * x`, `g2 = d * y**2`, i.e. exactly Appendix C's $(ax^2,by)$, $(cx,dy^2)$ and
not a sweep over "generic polynomials of degree $\le 3$". Indexed at
`docs/README_verification_suite.md:30`: "| `lemma29_verify.py` | BCH-TE morphism for
polynomial fields | A §2 |", in a catalog whose header (`:6`) says the extras "are not a
current verification ledger". The script has no file writes (`grep -n "open(\|\.write\|
savefig\|to_csv\|json.dump"` = nothing).

Run from a scratch directory with the pinned interpreter
(`acs-venv/bin/python -I <abs path>/code/acs_codebase/extras/lemma29_verify.py`): exit 0,
88 lines of output. Observed lines: "Cartan formula verified: [L_f, L_g] = L_[f,g] ✓",
"Antisymmetry verified: [f,g] + [g,f] = 0 ✓", "β₃¹ = a*c**2*x**2/12", "β₃² =
b**2*d*y**2/12", "β₃ = 0? False", and the summary "1. Cartan formula [L_f, L_g] = L_[f,g]:
VERIFIED exactly ✓ [...] 5. ALL arithmetic exact (symbolic over Q[a,b,c,d]) ✓ / Lemma 2.9
statement (with 2ε² coefficient) is CORRECT." The third-order term matches Appendix C's
$\beta_3=(ac^2x^2/12,\,b^2dy^2/12)$ exactly. `git status --short` in the worktree was
empty afterwards. What the run does not establish: Appendix B's "degree $\le 3$" scope (the
script tests one pair of degree-2 fields), and the lemma for general smooth fields (the
script is a witness on $\mathbb{R}^2$ with one fixed pair). The 2026-09-11 frontier
foundations report (`report.md:23`, branch I01) separately records reference-measure and
zero-lag obstructions to the smooth-field statement; those are not addressed by this link
and are out of this item's scope.

### 12.3 Placement and paste-ready block

Replace the sentence at `:2254` or, keeping the body untouched, add the section after the
24 September block (`:2326-2335`), before the author statement (`:2337`); it can follow
item 5's block.

```latex
\section*{Amendment: the Appendix~B computation script, 22 October 2026}
The script referred to in Appendix~\ref{app:exact} as ``available as supplementary
material'' is \texttt{code/acs\_codebase/extras/lemma29\_verify.py} in the repository
(its docstring names the lemma by its earlier number, 2.9; it is Lemma~\ref{lem:bch-te}
here). It implements the fields of Appendix~C, $f=(ax^2,by)$ and $g=(cx,dy^2)$ on
$\mathbb{R}^2$, over $\mathbb{Q}[a,b,c,d]$ with \texttt{sympy}, and on 22 October 2026
it ran to completion in a clean environment, reporting the Cartan formula and bracket
antisymmetry verified exactly, the factor $2$ in the $\varepsilon^2$ coefficient, and the
third-order term $\beta_3=(ac^2x^2/12,\,b^2dy^2/12)\neq0$, in agreement with Appendix~C.
The script checks that one pair of degree-two fields; Appendix~B's phrase ``generic
polynomials of degree $\le 3$'' describes the intended scope and is to be read as
``the polynomial pair of Appendix~C''. The script is a witness for Lemma~\ref{lem:bch-te}
on that pair, not a proof for general smooth fields, and the repository's script catalog
classes the directory it lives in as heritage, not a current verification ledger.
```

---

## What this file leaves out

- No proposal for `papers/core_trilogy/Spectral_Witness_Refinement.tex`: it does not carry
  the §5 bridge (item 3) and its amendment sentence is complete.
- No proposal for `papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex`
  or `_Monograph.tex`: they already state the one-way form; item 7 cites them.
- No rerun of the D03 or I05 programs: their receipts were read from the evidence archive,
  not re-executed; the numbers quoted are the archive's. Re-execution would need the
  `program.py` members extracted and their imports audited, which was out of this item's
  time box.
- Nothing in `MANIFEST.md` or `docs/ACS_Master_Index.md` was changed; item 10's rows are
  proposals in the same sense as the LaTeX blocks, left for the owner because the two
  indexes are the owner's adjudication surface (`docs/adjudication_2026-10-22.md`).

## Addenda from other first-pass agents (same date)

### Elimination Ledger agent: why no manifest-bound change was needed

# E12-ledger — proposals for manifest-bound files

None required.

The only manifest-bound file this item touches by reference is
`papers/later_FF06_series/The_Elimination_Ledger.tex` (listed in
`docs/publication/2026-09-24/publication-manifest.json`, line 13; sha at line 549).
It was not edited. Checked before deciding:

- It already carries the 24 September amendment verbatim
  (`\section*{Amendment: scope and evidence, 24 September 2026}`, lines 496–497), whose
  text matches the `amendments.json` entry for that path.
- Its treatment of Q3 is already single-valued: the scaling law
  `T_min = (2 pi e)^d / q` is T4 in the tier table (line 96), in §"The height-floor
  scaling law" (lines 181–238) and in the closing summary (line 469); the d=1,q=1 floor
  value `2 pi e` is kept as an invariant (lines 194–196, 454). That is the same ruling
  the Markdown ledger's Q3-TARGET line now states.
- It names the "SIGPIPE harness artifact that reported a passing test as a failure"
  (line 445) as a methodological self-correction, not as a Q5 result, which is consistent
  with the Markdown rename of "Q5 AISO regression" to a regression gate.

So the Markdown ledger was brought into line with the `.tex`, not the other way round,
and no amendment to the `.tex` is proposed.

### Clerical agent: Form_Function_and_Asymmetry appendix entry (E11)

# E11/E20 proposals for manifest-bound files (not edited)

Prepared 2026-10-22 for the owner to apply. Nothing below was written into the
repository; the publication integrity gate is the owner's to clear.

## E11(2) — `papers/Form_Function_and_Asymmetry.tex`, orphan appendix entry (line 2270)

Manifest check: `grep -c "papers/Form_Function_and_Asymmetry.tex" docs/publication/2026-09-24/publication-manifest.json` → `2` (bound; also a `papers/**/*.tex`).

### What is wrong

Appendix `\section{Numerical Parameters}` (`\label{app:numerics}`, line 2262) opens its
itemize with, at line 2270:

```latex
  \item \textbf{Coupled oscillator simulations (archived earlier-draft experiment; no corresponding section in this version):}
    $\omega_1 = 1.0$, $\omega_2 = \sqrt{2}$,
    initial conditions $(x_0, \dot{x}_0, y_0, \dot{y}_0) = (1, 0, 0.5, 0.3)$,
    integrated via \texttt{scipy.integrate.odeint} with step $\Delta t = 0.01$,
    $T = 2000$.  Transfer entropy: bin count $B = 10$, lag $\ell = 4$ steps,
    computed on late-time series $t \in [T/2, T]$ to exclude transients.
    BCH fit: least-squares regression of $|\DI(\eps)|$ on basis
    $\{\eps, \eps^2, \eps^3\}$ over $\eps \in \{0.05, 0.1, \ldots, 1.0\}$.
    \emph{Note:} this is the one computation using standard floating point;
    it is superseded by the exact integer automaton (Section~2.4) for the
    core sign-reversal result.
```

Evidence that it is orphaned (`grep -n -i 'coupled oscillator\|odeint\|BCH fit' papers/Form_Function_and_Asymmetry.tex`):
the only hits are lines 2270, 2273 and 2276, i.e. the appendix item itself. No section,
figure, table or result in the main text refers to this experiment; the next item in the
same list ("Integer automaton (Section~2.4)") does point at an existing subsection
(`\subsection{Exact integer automaton confirmation}`, line 601, in the section labelled
`sec:acs`). The appendix therefore lists parameters for a computation the paper no longer
reports, directly under the sentence "No standard IEEE~754 double-precision floating
point was used in any result reported in this paper, except where explicitly noted."

### Paste-ready fix, in the paper's own amendment convention

Insert immediately after the existing `\section*{Amendment: scope and evidence,
24 September 2026}` block (which ends at the paragraph "...or a proof of RH.", before
`\section*{Author Statement, ...}` at line 2338):

```latex
\section*{Amendment: Appendix~\ref{app:numerics} archival entry, 22 October 2026}
The first item of Appendix~\ref{app:numerics}, ``Coupled oscillator simulations,''
records the parameters of an earlier-draft floating-point experiment
($\omega_1=1$, $\omega_2=\sqrt2$, \texttt{odeint} integration, a BCH fit of
$|\DI(\eps)|$) for which no section, figure, table or result exists in this
version. It is retained only as an archival record of those parameters. No
result reported in this paper depends on it; the core sign-reversal result
rests on the exact integer automaton of the subsection ``Exact integer automaton
confirmation'' in Section~\ref{sec:acs}, whose parameters are the second item of
the same appendix. The entry should not be read as a reported computation, and
the appendix's statement that no double-precision floating point was used in any
reported result stands without exception.
```

If the owner prefers the in-place repair instead of (or in addition to) the amendment,
replace the eleven lines quoted above (2270–2280) with:

```latex
  \item \textbf{Coupled oscillator simulations:} an earlier-draft
    floating-point experiment ($\omega_1=1$, $\omega_2=\sqrt2$,
    \texttt{scipy.integrate.odeint}, BCH fit of $|\DI(\eps)|$) with no
    corresponding section or result in this version; parameters withdrawn
    from this appendix, see the dated amendment at the end of the main text.
    The core sign-reversal result rests on the exact integer automaton below.
```

Either change leaves `\label{app:numerics}` and all cross-references intact. The
amendment text uses only macros already defined in the file (`\DI`, `\eps`,
`\ref{app:numerics}`, `\ref{sec:acs}`); I did not compile it because the file is
manifest-bound and the paper's build is the owner's gate.

