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
