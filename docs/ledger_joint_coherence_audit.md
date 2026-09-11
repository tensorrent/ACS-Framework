# Elimination Ledger — joint coherence audit

STATUS: complete — Checks A, B, C and D all finished. See the STATUS block at the end.

**Line-number provenance.** Every line number in this report is as of commit `9a09c4e`, i.e.
BEFORE the repairs it prompted. Those repairs inserted supersession markers and so shifted the
file; the current positions are recorded in the ledger's own 2026-09-11 audit entry and are held
by `code/constraint_projection/crossref_check.py`. This report is left at its original addressing
rather than renumbered, because renumbering it would destroy the evidence that the numbers were
correct when observed. One finding of this report is that stale line references are this corpus's
dominant defect shape; rewriting them here would be the same mistake in the other direction.

**One finding of this report corrected the orchestrator's own work**, in flight: `gate_coverage.py`
had classified L413 as a claim-shaped untiered escapee. It is a continuation sub-heading of the
T4 entry at L412. The instrument was corrected and now verifies the inherited tier at runtime.

Scope: `docs/Elimination_Ledger.md` (3,967 lines, 57 entries). Audit of whether the
ledger is internally coherent when read as a joint record: withdrawals recorded at
both ends, direct contradictions between entries, tier discipline, inventory.

Method: entries addressed by line range via a precomputed index; every finding below
quotes the actual text with line numbers. A refinement that was properly recorded at
both ends is not a defect and is reported as such.

---

## CHECK A — withdrawals and corrections recorded at both ends

Six self-corrections were named for verification. Result: **three are clean (recorded at
both ends), two are recorded only at the correcting end, one never reached the ledger at
all.** Details below, each with both ends quoted.

### A1 — R3 (`Sl = 2` forces orientability) withdrawn by R5 · CLEAN, with one naming defect

Both ends are inside the same entry (L2492–2607), and the entry heading itself carries the
withdrawal: L2492 `**OUR OWN FAMILY WAS INCOMPLETE; ONE FINDING WITHDRAWN THE SAME RUN**`.

Original end (L2526–2529):

> **R3 — our own family was incomplete, and this is a correction to us.**
> `twisted_ribbon_capacitance.py` computed `n = 0, 1, 2` and stopped. **`n = 2` is `Sl = 1`.**
> For a planar centreline `Sl = 2` needs `n = 4` — 720°. **The manuscript's own object was
> never in the family we built.** Extended here.

Correcting end (L2573–2575):

> **So `Sl = 2` does not force orientability.** The framework can have both its self-linking
> number and `w₁ ≠ 0`, provided the centreline is non-planar. **R3's second finding is
> withdrawn.**

The withdrawal is real, dated, and its cost is stated (L2576–2580: the repair "costs a
parameter"). Downstream references are consistent and all point at R5 as the withdrawer:
L2755 ("R5's withdrawal"), L3171 ("R5's withdrawal of R3"), L3697 ("'planar' was baked into
R1–R4 before R5 lifted it"), L3897 ("after R3→R5"). No earlier entry was found asserting
that `Sl = 2` forces orientability — `grep -n "orientab"` over the whole ledger returns no
such claim before L2492; the pre-CPF `Sl = 2` entries (L535, L619) and the CPF audit (L677,
L738) discuss `w₁ ≠ 0` as a manuscript axiom, not as a consequence of `Sl = 2`. So the
withdrawn claim is self-contained to this entry and no other text is left standing on it.

**The one defect is naming, not bookkeeping.** R5 withdraws *"R3's second finding"*, but R3
as printed (L2526–2529) states exactly one finding — that the family was incomplete. The
withdrawn proposition is implicit in R3's sentence "For a planar centreline `Sl = 2` needs
`n = 4`" (L2528) plus R4's table row `4  2.0  True` (L2538). A reader who jumps to R3 sees
no second finding to subtract, and R3's text carries no marker that any part of it has been
withdrawn. This is a pointer to an unlabelled target, not a live contradiction.

### A2 — K4's framing restated from a verdict to a corpus fact · CLEAN

Both ends are present and the correction is applied in place. Corrected body (L2003–2008):

> **This is a corpus fact, not a verdict on either entry.** Both are entries. Each records a
> state of the work at its date. Neither is graded here, and neither is retracted — the
> ledger is append-only and that applies to the entries being read, not only to the ones
> being written.

Record of the change (L2038–2048):

> *A framing correction, made after this entry first landed in `bdcb530`.* The first draft of
> this entry read the scope difference as a fault — "regressed", "stripped off", "the better
> document". That imports a judgement the arithmetic does not carry and that this ledger's
> own discipline forbids: **entries record state; they do not indict each other.** … The
> instrument, this entry, MANIFEST and the PR were rewritten to the factual form. `bdcb530`
> stays in history as written.

The superseded wording is not left anywhere in the document (`grep -n "regressed\|stripped
off\|the better document"` finds them only inside this quotation of what was removed), the
new framing is stated in the body, and the old state is preserved by commit reference rather
than by a live sentence. This is the pattern the other five should match.

### A3 — the "odd under β↦1−β" boundary: retired, then found VACUOUS · RECORDED AT ONE END ONLY

Three ends exist, and only the newest is current.

End 1, the origin (L1339–1341), correctly flagged open at the time:

> Our one claimed-new result — *a functional detecting off-line zeros
> must be odd under `beta -> 1-beta`* — was asserted novel on judgement alone. **OPEN: it
> needs a literature search before it stands as ours.**

End 2, the retirement entry (L1359–1406), which closes on novelty and **explicitly affirms
the content** (L1389, L1392–1393):

> **Verdict.** The statement is **true but not ours**. …
> **RETIRED as a novel result (T4 on the novelty claim).** The underlying observation stands
> as a correct reading of the CPF manuscript's §7 — it is simply not a contribution.

End 3, the 2026-09-11 §7 entry (L3937–3955), which removes the content:

> This corpus recorded a constraint that *"a functional detecting off-line zeros
> must be ODD under β↦1−β"*, retired it on prior art (Davenport–Heilbronn, Weil positivity), and
> left it at that. The specialist reports the constraint is **vacuous**.
> … **Zeta's zeros are symmetric under β↦1−β, so an odd functional sums to zero over them
> identically — it detects nothing.** Our constraint did not merely duplicate known work; **it
> forced the functional to vanish.** And the companion claim that a `(½−β)²` form is "blind" is
> refuted: an **even** form separates DH from zeta by 0.190366.

**The defect.** L1389 and L1392–1393 still read as live and are now false as written: the
statement is not "true", and the observation does not "stand as a correct reading" — the
later entry finds it vacuous and refutes its companion clause. The retirement entry carries
no pointer to L3902; its last words (L1401–1403) are the standing-practice method note.
A reader entering at L1359 and stopping at the `---` on L1406 leaves with the superseded
reading.

A fourth mention is in the same state (L2940–2941):

> And the two-sidedness reading was already
> retired in this ledger — the *"odd under β↦1−β"* boundary died to Davenport–Heilbronn (1936) and
> Weil positivity within a week of being logged.

That records the *prior-art* cause of death, which the 2026-09-11 entry supersedes with a
stronger internal one (vacuity). Not false, but incomplete and unpointered.

Checked and clean: `MANIFEST.md` contains no surviving statement of this claim
(`grep -n "odd under\|β↦1−β\|beta -> 1-beta" MANIFEST.md` returns nothing), so the claim
was removed from the index when retired and only the ledger's own two older ends remain.

### A4 — K2's mechanism corrected twice · RECORDED AT THE CORRECTING END ONLY

Original end, still reading as standing (L3707–3718, in the 2026-09-01 Kelvin/Schwartz entry
that begins L3648):

> **K2 — Kelvin–Helmholtz, and the trap is that both theorems hold at once.** …
> No stabilising term, so growth is **unbounded as `λ → 0`**. … A regulator — viscosity, surface
> tension, finite core — is therefore mandatory, **and every one of them breaks the exact
> conservation that motivated the programme** (reconnection at finite viscosity changes knot type).

Correction 1 (L3743 heading, body L3807–3824):

> **CORRECTS K2'S MECHANISM; K3'S ASSESSMENT UNTOUCHED** …
> **V6 — and this CORRECTS K2's mechanism.** … K2's trap is real for a **neutral** fluid and has
> an escape in a **conducting** one.

Correction 2 (L3834 heading, body L3878–3897):

> **K2 CORRECTED A SECOND TIME, BY AN INDEPENDENT ROUTE** …
> **F4 — so K2 fails at two of three links, by independent routes, neither needing dissipation.**
> … **K2's conclusion does not survive as stated.** It asserted a mechanism derived from a singular
> limit and applied it to physical structures.

Both corrections are exemplary at their own end: each names the link it breaks, states what
survives, and the second explicitly tallies the sequence (L3895–3898: *"K2 has now been
corrected from two directions in two consecutive entries … the third finding of ours
withdrawn or narrowed by a later entry (after R3→R5 and K4's framing)"*).

**The defect is at the old end.** L3717's *"A regulator … is therefore mandatory"* is the
exact sentence both later entries falsify, and it carries no marker. The 2026-09-01 entry
containing it runs L3648–3742 and ends on an unrelated in-flight note (L3736–3740); nothing
in that entry tells a reader the mechanism was overturned 90 and 190 lines later. Because
the corrections sit in the two immediately following entries, a linear reader recovers; a
reader arriving by search on "Kelvin–Helmholtz" or "regulator" does not.

### A5 — the "T1 = machine-verified" label corrected by introducing T0 · CLEAN

This one is recorded at both ends, and the old end is the definition site rather than an
entry. Correcting end (L1263, L1286–1292):

> **T0 introduced; our T1 label was overstated** · T0 machine-CHECKED
> … `MANIFEST T1: "Machine-verified -- automated test passes, reproducible by running the code"`
> … When `cpf_triple_check.py` asserts `det M == (2Em - p^2)^2`, that is **sympy agreeing with
> sympy**. It is not a proof. The label is stronger than the thing …

Original end, `MANIFEST.md` L12–21, carries the correction in place at the definition:

> **T0 added 2026-08-30.** T1 has always meant *a script ran and asserted* — which is
> weaker than "machine-verified" sounds: a sympy assertion is sympy agreeing with itself.
> … **No existing claim changed tier**; T0 is earned by new evidence, not promotion.

and the tier table now reads `T0 | Machine-**checked** — kernel-verified by a proof
assistant` (L20) above `T1 | Machine-verified` (L21). Both documents agree that no claim
moved tier, which is also what CHECK C needs. No defect.

### A6 — "`A_Q/Q^x` is malformed" corrected to "defined, but not a group" · NOT RECORDED IN THE LEDGER AT ALL

This is the largest gap found. The correction exists in the repository, but **no ledger entry
records it**, and both ledger ends still read as live.

Old end 1, the CPF audit entry (L834–836):

> **C8 — Axiom I is false; Axiom II is ill-posed; two citations are wrong.**
> `A_Q/Q^x` is malformed (`Q^x` is multiplicative and does not act on the additive
> adeles by translation).

Old end 2, the CPF second-pass entry (L996–999):

> - **V8** — Følner sequences computed on `Z` … Every
>   abelian group is amenable; `A_Q/Q` is compact abelian with a Haar probability
>   measure; the idele class group is abelian; `A_Q/Q^x` as literally written is
>   undefined. **Axiom I false under every reading.**

Old end 3, `MANIFEST.md` L222, still the index entry for this claim:

> | Axiom I: $\mathcal{B}$ non-amenable | **T4** | `cpf_audit.py` C8 — $\mathbb{A}_\mathbb{Q}/\mathbb{Q}^\times$ is malformed; …

The correction, in commit `1ab2545` ("Axiom I amenability: specialist result corrects our own
reasoning twice, verdict direction unchanged") and in `docs/axiom_i_amenability.json` L429–430:

> "'A_Q/Q^x is malformed' does not reproduce: it is Connes' adele class space (Selecta Math. 5
> (1999) 29-106). The accurate statement is that it is defined but is not a group, so
> 'translation-invariant' is undefined on it."
> "'every abelian group is amenable' settles A_Q/Q and A_Q^x/Q^x but not A_Q/Q^x, which is not
> a group; that reading is settled by amenability of the Q^x-action instead."

`grep -n "Connes\|adele class"` over the ledger returns **nothing**, and the only ledger
date on 2026-09-11 is the §7 entry (L3902). The sole trace of the amenability run in the
ledger is a passing reference inside that other entry, L3961:

> *Third specialist correction to our own record*, after the amenability run's two (`1ab2545`).

So the ledger counts the two corrections without containing them. Note also that both
corrections are to *mechanism*, not direction — `docs/axiom_i_amenability.json` records
"0 support Axiom I's assertion 3", so the T4 verdict on Axiom I is unaffected. The defect is
that C8 (L835), V8 (L998) and MANIFEST L222 each still assert "malformed"/"undefined" as the
*reason*, and that reason is the one the specialist run says does not reproduce.

Related: the two tallies of self-corrections disagree in scope rather than in fact. L3897
counts "the third finding of ours withdrawn or narrowed by a later entry (after R3→R5 and
K4's framing)"; L3961 counts the "third specialist correction … after the amenability run's
two". Different series, both internally consistent, but the second series has only one of its
three members written into the ledger.


## CHECK B — direct contradictions between entries

Two genuine contradictions were found (both are the un-updated ends already reported in
CHECK A, restated here as contradictions because in each case two *live* texts assert
incompatible things). Three further areas were probed and came back clean; what was
searched is shown in each case, and one soft tension is reported with its resolution rather
than as a defect.

### B1 — the same constraint is "true" in one entry and "detects nothing" in another

L1389 and L1392–1393:

> **Verdict.** The statement is **true but not ours**. … The underlying observation stands
> as a correct reading of the CPF manuscript's §7 — it is simply not a contribution.

L3947–3952:

> **Zeta's zeros are symmetric under β↦1−β, so an odd functional sums to zero over them
> identically — it detects nothing.** Our constraint did not merely duplicate known work; **it
> forced the functional to vanish.** And the companion claim that a `(½−β)²` form is "blind" is
> refuted: an **even** form separates DH from zeta by 0.190366.

These cannot both stand: a constraint that forces its functional to vanish identically is
not "a correct reading", and the later entry supplies a number (0.190366, and 3.806890 in
the direct check at L3944) for the even form the earlier entry called blind. The later
entry is the one with the computation behind it. The earlier text is unmarked.

### B2 — `A_Q/Q^x` is "malformed" in two ledger entries and "defined but not a group" in the artifact

L835–836 (`C8`) and L998–999 (`V8`) both assert malformed/undefined; `docs/axiom_i_amenability.json`
L429 asserts:

> "'A_Q/Q^x is malformed' does not reproduce: it is Connes' adele class space (Selecta Math. 5
> (1999) 29-106). The accurate statement is that it is defined but is not a group…"

"Malformed" and "is Connes' adele class space, defined" are incompatible characterisations
of the same object. The direction of the verdict on Axiom I is not in dispute — both routes
end at T4 — so this is a contradiction in *mechanism*, and the ledger end is the stale one.

### B3 — the `H₂ = 0` clause: "adds nothing" vs "both clauses are the obstruction" · NOT a contradiction

L980–981 (CPF second pass, V1):

> Minor: `H_2 = 0` holds for every closed non-orientable surface, so that
> clause is implied by `w_1 != 0` and adds nothing.

L2256–2258 (Green's theorem entry):

> And **Axiom II reads `w₁(M) ≠ 0, H₂(M;Z) = 0`.** Both clauses are the obstruction:
> `H₂ = 0` means no fundamental class, so an ordinary 2-form has no integral over `M`;
> `w₁ ≠ 0` means no orientation to give a circulation sense.

These read as opposed but are not. V1 says the clause is *logically redundant as an axiom*
(implied by `w₁ ≠ 0` on closed non-orientable surfaces); the Green's entry says the clause,
as written, *obstructs the integral theorem*. An implied clause still states a true fact, and
a true fact can carry an obstruction. The same entry closes the gap explicitly two lines
later (L2260–2261): *"the same clause does both: `w₁ ≠ 0` killed the spin structure and now
kills the integral theorem"* — i.e. the work is being done by `w₁ ≠ 0`, exactly as V1 said.
Recorded here as checked, not as a defect.

### B4 — a stale summary block: the OOS01 scorecard

L387–390:

> ## SCORECARD UPDATE (post-OOS01)
> KILLED: γ (now T1), Q6, Q5-classes, **Q2 BRA speed (T1)**, **Q4 identity-as-stated (T2)**.
> SURVIVED/INVARIANT: h̃/h (now T1), Q3 floor (scoped), Q4 monotonicity-analogy, Q7 (decoupling).
> REFRACTION (T1): g₄'s 4/3, γ's 0.274, λ_φ's 0.1283. BLOCKED: Q3 (d,q) law, Q5 full HP operator.

Two of its lines are superseded within the next 30 lines and it carries no pointer:

- "SURVIVED/INVARIANT: … Q4 monotonicity-analogy" is narrowed at L392 and L406–410 —
  *"Q4 fully closed. Every reading accounted for: the conjecture ΔI ≡ c is FALSE/
  ill-defined under the framework's own TE-asymmetry definition, or a RESTATEMENT of an
  established theorem (Casini–Huerta) under the MI definition. No reading is both novel
  and true."* The analogy survives only as someone else's theorem.
- "BLOCKED: Q3 (d,q) law" is resolved at L412 — **FALSIFIED (T4)**.

The scorecard is a dated snapshot ("post-OOS01"), which is a legitimate form; the defect is
that it sits inline above the entries that supersede it, in a document whose other
supersessions are marked.

### B5 — the ledger's own tier legend never absorbed T0

L11:

> - Tiers: **T1** machine-verified / **T2** proven-or-by-inspection / **T3** numerical / **T4** falsified

Three entries in the same file carry T0 (L1263, L1471, L1637), and `MANIFEST.md` L12–21 was
updated with the T0 note and the T0 row. The ledger's own legend was not. A reader working
from L11 has no definition for the tier three of its entries use. (Cross-listed to CHECK C;
it is the one incomplete end of the otherwise-clean A5.)

### B6 — one heading/body tier mismatch

L535 heading:

> ### 2026-07-26 — Möbius-screw: *Sl = 2* as the geometric origin of *g = 2* — **KILLED** · T2 structural / T1 numerical

L606 body:

> **Verdict.** `Sl = 2 ↔ g = 2` as a *geometric origin* claim is **FALSIFIED (T4)**.

The heading lists T1 and T2 only. Every other falsification entry carries T4 in the heading
(L412, L444, L677, L1023, L1359). The body's T4 is the operative verdict; the heading
under-reports it.

### What was searched and came back clean

- **The `alpha` numbers.** `grep -n "26\.96\|1\.886\|72\.6\|5\.08\|137\.03"` over the whole
  ledger returns 20 lines across 6 entries (L705–730, L1434–1508, L1552–1627, L1718–1730).
  They are mutually consistent and the arithmetic closes: the parameter-free `τ = i/2` step
  predicts `alpha^-1 = 1.886` (L720, L1507), the observed is `137.036`, and the quoted gap
  `72.648` is exactly `137.036 / 1.88629` (L1582 states this identity itself); the most
  defensible physical cutoff gives `26.96`, quoted as "off by 5.08x" (L1722, L1729), and
  `137.036 / 26.96 = 5.083`. The CODATA-matching row (L722, L1727) requires
  `a/R = 2.04e-118` and is labelled "1.0x" — fitted, not predicted. No entry asserts a
  different value for the same configuration. **No contradiction in the alpha numbers.**
- **Q3, across three entries that look opposed.** L151 "**SURVIVED (scoped)**", L378
  "**NOT-FOUND (still blocked)**", L412 "**FALSIFIED (T4)**". Not a contradiction: L419–420
  restates the earlier scope in the later entry (*"Earlier Q3 was SURVIVED-scoped: only the
  d=1,q=1 point (ζ) was testable"*), and L438 preserves the surviving part exactly
  (*"The floor *value* at d=1,q=1 (2πe) remains an analytic invariant (unchanged)"*). The
  L151 entry had pre-declared its own limit at L165–167 (*"the exponential-in-degree,
  linear-in-conductor scaling (2πe)^d/q is **UNTESTED**"*). This is a refinement recorded at
  both ends and is **not a defect**.
- **Q4 / ΔI ≡ c, across three entries.** L231 (blocked on the definition), L350 (identity
  falsified, monotonicity survives), L392 (monotonicity resolved, target closed). Each later
  entry restates what it inherits (L399: *"The only surviving reading of ΔI ≡ c was the
  monotonicity analogy"*). Chain is coherent; only the L387–390 scorecard lags (B4).
- **The g-factor.** `grep -n "g = 1\|g = 2\|moment_ratio"` returns L535–606 (`Sl = 2 ↔ g = 2`
  falsified), L619–633 and L770 (`g = 1` exactly for every closed curve), L1003 (re-executed:
  `moment_ratio.py` returns `g = 1.000000`), L1023–1069 (`g = 2` derived from `su(2)` alone,
  and shown not to diagnose relativity). Every occurrence agrees on which object carries
  which value. **No contradiction found on the g-factor.**

## CHECK C — tier discipline

### The rule, and where it is stated

Two places, both as a bare assertion:

- `MANIFEST.md` L10: `## Verification hierarchy (tiers never promote)`
- `Elimination_Ledger.md` L1466–1467, in the list of this repo's own methods:
  `` `append-only elimination ledger` · `tiers never promote` ``

Neither states what "promote" means, and the corpus uses two incompatible tier semantics.

### The two semantics, both stated in the corpus

**(i) Strength ordering.** `MANIFEST.md` L14–21 lists T0 > T1 > T2 > T3 > T4 with T0
described in the ledger (L1292) as *"Strictly stronger than T1."* Under this reading, moving
a claim from T2 to T1 is a promotion.

**(ii) Path marker.** `Elimination_Ledger.md` L28–31, the engine kill-criterion:

> The criterion can be applied two
> ways: **(a)** numerically, by recomputing under an instrument swap (→ T1), or
> **(b)** structurally, by arguing from the quantity's construction when no
> recomputable pipeline is reachable (→ T2). Tier honestly; never let (b) wear (a)'s
> clothes.

Under (ii), T1 and T2 record *which route was available*, not how strong the result is, and
switching routes changes the tier by design.

### The one claim whose tier was raised across entries

The framework constants (g₄, γ, λ_φ, h̃/h). First entry, L87 and L146–148:

> ### 2026-06-06 — Target 1: framework constants invariant-or-refraction — **T2 STRUCTURAL**
> … All verdicts T2; T1 upgrades require the ACS derivation code under an
> instrument swap (g₄, γ, λ_φ) or an RGE integration (h̃/h).

Second entry, L367 and L375–377:

> ### Q1 framework constants — **T1 UPGRADE (all four predictions machine-confirmed)**
> … My session T2 verdicts upgrade to T1; my λ_φ "geometry-number invariant" hedge was
> slightly too generous — machine says the value moves under Killing-form normalization.

The same four claims, the same verdicts, tier raised T2 → T1. The corpus's own word is
"upgrade", and the upgrade is **designed in**, not accidental: L94 (*"**T1 upgrade path for
every entry below**"*), L125 (*"**T1 upgrade =** integrate the RGEs"*), L325 (a table row
*"Constant T1-upgrades"*), L146–148.

**This is a violation under semantics (i) and compliant under semantics (ii).** The corpus
never says which is meant, and the two readings are used in the same document.

### The contrast that makes the ambiguity visible

The T0 entry handles the identical situation the other way, and says so explicitly (L1292–1295):

> **T0 INTRODUCED — machine-CHECKED proof.** Strictly stronger than T1. … **No existing claim
> changes tier**: T0 is a new classification earned by new evidence, not a promotion. Exactly
> one proposition holds it so far.

and `MANIFEST.md` L15: *"**No existing claim changed tier**; T0 is earned by new evidence, not
promotion."* So when new and stronger evidence arrived in August, the corpus refused to
re-tier anything and created a new tier instead. In June, new and stronger evidence for the
framework constants was recorded as *"My session T2 verdicts upgrade to T1"* — the verdicts
moving, not a new tier being earned. **The two entries apply opposite conventions to the same
kind of event, and neither cites the other.** The L87 entry still reads `**T2 STRUCTURAL**`
in its heading with no marker that L367 raised it.

Nothing else in the ledger raises a tier. `grep -n "upgrade\|UPGRADE\|promote\|promotion"`
returns 11 lines; the remainder are not tier moves: L116 (*"promotes a documented ambiguity
to an explicit"* — about a scope note), L288 (*"the framework's 'tension, not resolved' flag
upgrades to: **not**…"* — a verdict), L3013 (*"upgrades the spinor identification from loose
analogy to structural match"* — a claim's content, and the same sentence records what it
cost: *"It simultaneously converts the zeta bridge from unsupported to excluded"*).

### T0 is defined in one document and used in the other

Counting the 57 entry headings: T1 appears in 42, T2 in 30, T3 in 7, T4 in 5, **T0 in 3**
(L1263, L1471, L1637). The ledger's own legend (L11) lists only T1–T4:

> - Tiers: **T1** machine-verified / **T2** proven-or-by-inspection / **T3** numerical / **T4** falsified

`MANIFEST.md` L12–21 carries both the T0 row and the note explaining the change; the ledger
legend was never updated. Also note the two legends disagree on T2 — ledger L11
"proven-or-by-inspection", MANIFEST L22 "Proved in paper — complete mathematical proof,
human-verified" — which matters because "by inspection" is exactly the weaker sense the T0
entry objected to for T1.

### The six headings with no tier marker

Confirmed against the index and read individually:

| line | heading | assessment |
|---|---|---|
| 37 | Swing now — cheap, decisive, high collapse | target-queue planning heading (L36 `## TARGET QUEUE`), not an entry; nothing is claimed, so nothing to tier |
| 59 | Build the kill test, then swing | same |
| 68 | Continue the strip-mine — empty-tunnel mapping | same |
| 378 | Q3 (d,q) scaling — **NOT-FOUND (still blocked)** | a status, not a result. The scheme has no tier for "no evidence was obtainable", so tierlessness is the only available encoding; consistent, and the status tag vocabulary at L12 (`BLOCKED`) covers it |
| 413 | (LMFDB unreachable from sandbox; zeros COMPUTED directly instead) | a continuation sub-heading of the L412 entry, which carries **T4**; not a separate untiered entry |
| 2609 | The evidence-chain discipline made canon · **method** | see below |

So the task's framing is right in substance but the arithmetic is slightly different from
"3 planning headings + L2609": three are planning headings, one (L413) is a sub-heading of a
tiered entry, one (L378) is a status with no result, and one is L2609.

### Is "method" consistent as a tier substitute? No — and the ledger itself shows why

L2609 puts `method` in the slot every other entry reserves for tiers:

> ### 2026-08-31 — The evidence-chain discipline made canon · method

The tier standards at `MANIFEST.md` L20–24 are all statements about *a claim's evidence*
("automated test passes", "complete mathematical proof", "consistent across runs",
"computation shows the claim is false"). None applies to adopting a discipline, so marking
the entry as a non-claim is defensible in content. **But the corpus does not do this
consistently.** Two other method entries carry real tiers:

- L3025: `### 2026-09-01 — Method rule 11: correctness, not righteousness — **CORRECTED TWICE FROM MEMORY, SO NOW MACHINE-CHECKED** · T1 machine`
- L3083: `### 2026-09-01 — Method rule 12: a destructive restore, guarded rather than remembered · T1 machine`

Both are method-adoption entries, and both are tiered T1 because the *enforcement* was
machine-checked (a linter, a guard). The L2609 entry is the same shape — a discipline made
canon — and the ledger records for it, at L2649–2655, an equally machine-checkable object
(a toolchain file "corrected to what actually compiles", "Two proofs at…"). So "method" is
not a sixth tier and not a principled exemption; it is one entry using the tier slot for a
category label where two later entries of the same kind used the tier. Three method entries,
two conventions.

## CHECK D — inventory

Counted from the index of all 57 headings, cross-checked against the file.

- **57 headings.** 48 carry a date; 9 do not (the 3 target-queue planning headings at L37,
  L59, L68; the 5 undated OOS01 sub-entries at L339, L350, L367, L378, L382; and the L413
  continuation sub-heading). The undated OOS01 block sits between the dated entries of
  2026-06-06 and inherits their date from the surrounding session.
- **Date range 2026-06-06 → 2026-09-11.** By month: June 9, July 5, August 21, September 13.
  Two thirds of the record is the last six weeks, which is consistent with the CPF audit and
  its successors being the bulk of the corpus.
- **Tier markers in headings:** T0 in 3, T1 in 42, T2 in 30, T3 in 7, T4 in 5; 6 headings
  carry none (itemised in CHECK C). Headings routinely carry two or three tiers, one per
  method used, matching the L28–31 path convention.
- **Verdict words in headings** (a heading may carry more than one): KILLED 7, FALSIFIED 4,
  SURVIVED 3, RESOLVED 2, CORRECTED 4, CLOSED 4, WITHDRAWN 1, RETIRED 1, NOT NEW 1,
  ARTIFACT 1. Self-directed outcomes (CORRECTED / WITHDRAWN / RETIRED = 6 headings) are a
  tenth of the record, which is what makes CHECK A the load-bearing check for this document.
- **Structural note.** All 57 use the same `###` heading form with a `·` tier suffix, so the
  file is machine-indexable as it stands; the only two headings that break the pattern are
  L413 (a parenthetical continuation) and L387 (`##`, the scorecard block flagged in B4).

---

## Summary of defects, in the order they should be fixed

1. **A6 / B2** — the amenability correction (commit `1ab2545`, `docs/axiom_i_amenability.json`
   L429–430) has no ledger entry, and three live texts still carry the superseded mechanism:
   `Elimination_Ledger.md` L835, L998, and `MANIFEST.md` L222. Largest gap found.
2. **A3 / B1** — L1389 and L1392–1393 still read as standing after L3937–3955 found the
   constraint vacuous. L2940–2941 records only the superseded cause of death.
3. **A4** — L3717 (*"A regulator … is therefore mandatory"*) carries no marker after being
   corrected twice, at L3807–3824 and L3878–3897.
4. **B5 / C** — the ledger's tier legend (L11) never absorbed T0, which three of its own
   entries use; and it defines T2 as "proven-or-by-inspection" against `MANIFEST.md` L22's
   "complete mathematical proof, human-verified".
5. **C** — "tiers never promote" (MANIFEST L10, ledger L1467) is undefined against two
   coexisting tier semantics, and L367/L375 raises T2 → T1 in the corpus's own word
   ("upgrade") while L1292–1295 refuses the identical move.
6. **B4** — the L387–390 scorecard is superseded on two of its lines within 30 lines and
   carries no pointer.
7. **C** — "· method" at L2609 sits in the tier slot, while the two other method entries
   (L3025, L3083) carry T1.
8. **B6** — L535's heading omits the T4 its own verdict states at L606.
9. **A1** — R5 (L2574–2575) withdraws "R3's second finding", which R3 (L2526–2529) does not
   label; and R3 carries no marker that part of it was withdrawn.

Not defects, verified and recorded as such: the K4 framing correction (A2), the T0
introduction as recorded in `MANIFEST.md` (A5), the Q3 survived→falsified chain (B),
the Q4 chain (B), the `H₂ = 0` apparent clash (B3), the alpha numbers (B), the g-factor (B).

## STATUS

**Completed:** Check A (all six named withdrawal/correction pairs verified at both ends,
with both ends quoted), Check B (contradiction search, including four clean areas with the
searches shown), Check C (tier discipline, the promotion instance, the T0 legend gap, and
the six untiered headings itemised), Check D (inventory).

**Not reached:** (a) no verification that the ledger's claims match the artifacts in
`docs/*.json` beyond the two files opened for A6 — this audit checks the ledger against
itself and against `MANIFEST.md`, not against the code; (b) no exhaustive pairwise
contradiction sweep — Check B probed the areas where the same object is discussed in
multiple entries (alpha, Q3, Q4, g-factor, the Axiom II clauses, the β↦1−β constraint) and
those where CHECK A had already surfaced a stale end, rather than comparing all 57 entries
against each other; (c) `papers/` and the rest of `docs/` were not audited.
