# Adjudication of the historical indexes against the 24 September 2026 record

**Date:** 22 October 2026. **Scope:** the 35 rows named in the section titles below —
Master Index "explicitly open" items 15–20, Corpus Map open problems O-1–O-8, the Corpus
Map "locked numerical invariants" table, and the MANIFEST Paper A claim table — and
nothing else. **Method:** for each row, quote what the index currently displays, what the
24 September record says, and what the endpoint audit says, each with `file:line`; then
propose the status the row should carry. **This note changes no tier.** The only edits
made alongside it are two dated consistency notes (tan β / Coleman–Weinberg in
`MANIFEST.md` and `docs/ACS_Master_Index.md`, rows A-15 and D-5; the scalar-sector count
in `docs/ACS_Corpus_Map.md:70`) and the link from `docs/README.md`. Everything else here
is a proposal for the owner.

Conventions. Line numbers are those of the tree at commit `174131f`, before this note's
own edits (the two dated notes shift later lines of `MANIFEST.md` and the Master Index by
27). TeX markup is stripped inside quotes; `[...]` marks an elision inside one source
passage. "The record" means `docs/publication/2026-09-24/amendments.json` (the in-paper
copies are the sections headed *Amendment: scope and evidence, 24 September 2026*),
`papers/updates/ACS_Action_Identifiability.tex` (the action paper) and
`docs/publication/2026-09-24/README.md`. "The audit" means
`docs/condensate_energy/endpoint_audit/README.md`. The action paper and the audit are
manifest-bound (`grep -c` against `docs/publication/2026-09-24/publication-manifest.json`:
2 and 1); nothing in them is edited here. The three index files and `docs/README.md` are
not in the manifest (`grep -c` = 0 for each).

Companion, same date: `docs/open_problems_2026-10-22.md` (state-of-the-problem cards,
pass 2) treats several of these rows from the "what would it take" side. The mapping is
Card 1 ↔ A-17/B-O-1, Card 7 ↔ B-O-4, Card P1 ↔ C-2/C-11/D-2, Card P2 ↔ B-O-5,
Card P3 ↔ C-3/D-4/D-9, Card P4 ↔ C-11, Card P5 ↔ A-20/B-O-3/C-8, Card P6 ↔ B-O-7/C-5/D-7,
Card P7 ↔ B-O-8. This note adjudicates what the indexes display against the record; the
cards state the problems. Neither changes a tier.

Proposed-status vocabulary:

| Label | Meaning |
|---|---|
| **Unchanged** | the record neither contradicts nor narrows the row |
| **Scope-annotated** | the claim stands inside a stated ansatz or normalization; the row should say so |
| **Split** | a mathematical statement that stands and a physical reading the record withdraws or conditions; the row should show both |
| **Superseded as posed** | the question's premise was retired by the record |
| **Open (narrowed)** | still open; the record names what it would take |
| **Open (unchanged)** | still open; the record is silent |
| **Contradicted** | the audit states the printed argument fails; a tier change is proposed for the owner, not made |
| **Conditional** | a number the record classes as a conditional calculation, not a prediction |
| **Resolved with caveat** | the Elimination Ledger's own label; the caveat must be displayed |
| **Display stale** | the index label is out of date relative to a later repository record, independent of the 24 September record |

Passages that recur are quoted once here and cited by label below.

- **[REC-COUNT]** `amendments.json:8` (*Form, Function and Asymmetry*): "The complete
  scalar sector contains 17 quartic and four quadratic coefficients; six quartic
  directions are invisible on the neutral family. A scale family changes physical masses
  while preserving dimensionless labels. Earlier reduced parameter counts apply only to
  their stated ansatz."
- **[REC-SELECT]** `amendments.json:88` (Paper A; in-paper copy
  `papers/core_trilogy/Palatini_Gauge_Attractor.tex:2980`): "The algebraic closure
  calculations do not establish a unique microscopic dynamics. For the stated smooth,
  metric-compatible Palatini action, writing the connection as its Levi–Civita part plus
  contortion leaves the added torsion-squared term algebraic in contortion. It supplies no
  independent contortion wave operator. [...] The complete scalar action and physical
  vacuum still require coefficients, kinetic normalization and a selection rule."
- **[REC-ANSATZ]** `amendments.json:96` (Paper C; in-paper copy
  `papers/core_trilogy/Holographic_Spectral_Inversion.tex:1018`): "Reduced
  scalar-potential formulas apply only to their restricted ansatz: the complete invariant
  audit has 17 quartics, hidden transverse directions and nontrivial running."
- **[REC-QUARTIC]** action paper `:267-275`: the one-loop pairs
  "(0.08, 0.1685520), (0.1283001, 0.1806315), (0.18, 0.1898121)", sensitivity
  "dλ_IR/dλ_UV = 0.2088898", "The comparison input is 0.1294. The middle RG output
  corresponds to an approximately 148 GeV tree mass proxy, not a pole-mass prediction."
  Audit `:92-98`: "Setting the upper-scale quartic to 2√3/27 produces a lower-scale
  quartic 0.1806315, not its comparison input 0.1294. The resulting tree mass proxy is
  about 148 GeV; this is not a pole-mass calculation. [...] The independently checked local
  sensitivity dλIR/dλUV is 0.2088898, not zero."
- **[AUD-SCOPE]** audit `:3-5`: "The reviewed ACS assumptions define calculable families
  of models, but do not select a unique physical particle, mass scale or flavor spectrum."
  and `:14`: "It is not a completed theory of matter or a proof of RH."
- **[AUD-FLAVOR]** audit `:257-260`: "Charged partners have a computed spectrum, but no
  source-selected masses or condensate map. Explicit allowed Yukawa choices give opposite
  answers for fermion emission thresholds. This is non-identification, not a calculated
  gauge decay width." Action paper `:33-34`: "They do not select a physical vacuum, a
  unique mass scale or measured flavor data."

---

## A. Master Index, "Explicitly open (flagged in papers)", items 15–20 — `docs/ACS_Master_Index.md:149-155`

### A-15 — `:150` "Coleman-Weinberg analysis (6 → 5 inputs?)"

- **Index displays:** open. Elsewhere: `MANIFEST.md:63` "tan β gauge-protected (CW 6→5
  fails) | **T4**"; `docs/ACS_Corpus_Map.md:67` "gauge-protected flat direction — cannot
  be fixed perturbatively" and `:118` F-11 "CW 6→5 parameter reduction | tan β
  gauge-protected flat direction"; Paper C `Holographic_Spectral_Inversion.tex:852`
  "Radiatively generated: tan β (value pending Coleman–Weinberg)" and `:856-858` "Whether
  one-loop Coleman–Weinberg corrections fix tan β uniquely (reducing the count to 5) is
  open." Paper A `Palatini_Gauge_Attractor.tex:2191-2195`: "tan β is therefore not lifted
  by perturbative corrections in this sector; resolving it requires a non-minimal Higgs
  sector (e.g. Branch B with Σ ∼ (15,1,1)) or non-perturbative effects."
- **Record:** [REC-COUNT]; [REC-ANSATZ]; [REC-SELECT] (last sentence). Action paper
  `:186-190`: "The radial source, gauge sources and a further scalar-loop contraction
  require the full five-dimensional Hermitian space for generic independent gauge
  couplings. This does not preclude a future derived relation among boundary values."
- **Audit:** `:29-32`: "Six quartic directions are invisible to the restricted neutral
  potential but change physical stability. The radiative audit restores the relevant
  couplings; the old reduced potential is generally not closed under running." The
  radiative stage it links, `docs/condensate_energy/radiative_flat_modes/README.md:10`,
  reports "conditional results for specified boundary couplings" and `:223-225` "This
  stage closes the conditional one-loop flat-direction calculation. It does not close
  finite one-loop matching to a selected light doublet, momentum-dependent mass
  corrections, or recovery of an ACS construction that fixes the inputs." It does not name
  tan β (`grep -c -i "tan *\\?beta\|tan β\|tanβ\|vev ratio"` = 0).
- **Proposed:** **Superseded as posed.** The tree-level T4 stands inside the
  minimal-bi-doublet ansatz; the 6-input count is ansatz-bound; the residue — does the
  complete action select tan β — is a different question for which the record supplies no
  selector. *Applied today* as the identical dated note in `MANIFEST.md` (under the Paper A
  table) and `docs/ACS_Master_Index.md` (under item 20). Paper C's `:856-858` is
  manifest-bound; a paste-ready amendment was drafted with this note and is not applied.

### A-16 — `:151` "FeynRules/UFO export"

- **Index displays:** open; `docs/ACS_Corpus_Map.md:139` O-2 "FeynRules/UFO export |
  engineering | LHC-testable predictions".
- **Record:** silent by name (no match for `FeynRules` or `UFO` in `amendments.json`,
  the action paper or the audit). [AUD-FLAVOR], action-paper sentence.
- **Audit:** [AUD-FLAVOR]; `:307` "physical pole masses are not claimed."
- **Proposed:** **Open (narrowed).** An export encodes one Lagrangian with fixed
  coefficients; the record says coefficients, vacuum and flavor data are not selected. The
  row should read "blocked on a selected complete action", not "engineering".

### A-17 — `:152` "Hilbert-Pólya operator construction"

- **Index displays:** open. `docs/ACS_Corpus_Map.md:138` O-1: "**now characterized**:
  self-adjoint (GUE free), arithmetic in positions not spacings, self-duality
  generated-not-imposed → Berry–Keating route survives (FF06f)". `MANIFEST.md:86`
  "Hilbert-Pólya wall quantified (constructs NO operator)"; `:87` "Class pinned;
  arithmetic realisation (orbits log p) remains open".
- **Record:** `amendments.json:92` (Paper B): "A diagonal operator assembled only from
  real ordinates loses the real-part displacement and cannot alone establish the
  Hilbert–Pólya identification." `:72` (N3): "Verification of finite primes and transition
  counts must not be promoted to an exclusion of off-line zeta zeros." `:80` (fibered-line
  note): "The proposed identification of the arithmetic, character and
  algebraic-holographic descriptions remains a conjecture, with no inferred proof of RH".
- **Audit:** `:171` "No actual zeta zero is located or excluded by these checks."
  [AUD-SCOPE] `:14`.
- **Proposed:** **Open (unchanged)**; the Corpus Map O-1 gloss should carry MANIFEST's own
  qualifier "constructs no operator" and the record's: a characterisation of constraints on
  H is not a construction, and "Berry–Keating route survives" is a conjecture, not a result.

### A-18 — `:153` "Multi-cluster weighted proof (N2 Theorem 1(iii))"

- **Index displays:** open. `MANIFEST.md:111` "N2 — general grading selection theorem |
  **T2** | `test_signature_selection.py` (bilinearity + weighted max-cut)"; `:112` "N2 — G₂
  exceptional-algebra counterexample | **T2** | (cluster coherence fails for multi-length
  root clusters)".
- **Current N2 text** (`papers/notes/Adjoint_Clifford_Signature_Selection.tex`): part (ii)
  `:255-265` is the reduction to weighted max-cut "Under cluster-coherent partitions"; part
  (iii) `:266-269` is the binary split; part (iv) `:270-271` "Structural stability —
  numerically supported, not proved here (T3)"; `:293` "We prove parts (i)–(iii); part (iv)
  is verified numerically". `:410-415` Proposition "Failure of cluster coherence in G₂":
  "the interaction weights do not factor through eigenvalue clusters, and the optimal
  grading splits clusters."
- **Record:** `amendments.json:64` (N2): "A signature or grading selection within an
  algebraic construction is distinct from deriving a physical spacetime metric. [...] That
  example cannot independently validate a physical signature-selection claim." — restricts
  the physical reading, not the theorem.
- **Audit:** silent on N2; its soldering remark `:204-209` concerns a recovered
  MacDowell–Mansouri script: "This is a conditional construction, not the missing
  action-to-parameter derivation."
- **Proposed:** **Display stale + Split.** The label "(iii)" no longer matches the current
  theorem numbering; the multi-cluster weighted reduction is proved as part (ii) under the
  cluster-coherence hypothesis, G₂ shows that hypothesis can fail (T2 counterexample), and
  the open residue is part (iv) (T3). The physical reading is scope-annotated by the record.

### A-19 — `:154` "Extension to exceptional algebras (N2)"

- **Index displays:** open. `MANIFEST.md:112` G₂ counterexample at T2. N2 `:691-692`
  "Extension to exceptional algebras (G₂, F₄, E₆,₇,₈) remains open."; `:434-438` "In
  exceptional algebras [...] eigenvalue clusters may contain roots of different lengths
  [...] optimal gradings may split clusters".
- **Record:** `amendments.json:64` as in A-18. **Audit:** silent.
- **Proposed:** **Open (narrowed).** Open in the sense N2 states, with a recorded T2
  obstruction (G₂) the Master Index row omits; propose "open; G₂ counterexample to cluster
  coherence recorded (MANIFEST T2)".

### A-20 — `:155` "Action principle that produces S_f (Route B completion)"

- **Index displays:** open; `docs/ACS_Corpus_Map.md:140` O-3 "Action principle for S̃_g |
  variational theory | first-principles derivation".
- **Record:** [REC-SELECT]. Action paper `:310-314`: "The remaining physical requirements
  are a normalized microscopic condensate-to-field map, a coefficient and flavor selection
  law, and a physical vacuum and matching prescription. The present result is
  underdetermination within the reviewed assumptions, not a no-go theorem against a future
  model that adds justified premises."
- **Audit:** `:195-197` "T² and K∧K are algebraic in K. They provide no independent
  contortion wave operator. Our component check retains all 24 contortion components."
  `:284-289` "The remaining missing physical inputs are a normalized microscopic action
  with its condensate-to-field map, a coefficient/scale and flavor selection law, a
  physical vacuum, and the quantum state/charge sector identifying the proposed particle.
  [...] The evidence does not exclude a future construction that explicitly adds those
  premises."
- **Proposed:** **Open (narrowed).** The record names what the action must supply and
  withdraws one candidate route (propagating torsion from the stated T² term). The row
  should carry that list rather than "variational theory".

---

## B. Corpus Map open problems O-1–O-8 — `docs/ACS_Corpus_Map.md:136-145`

### B-O-1 — `:138` Hilbert–Pólya operator H
See A-17. **Proposed:** **Open (unchanged)**, gloss qualified as there.

### B-O-2 — `:139` FeynRules/UFO export
See A-16. **Proposed:** **Open (narrowed).**

### B-O-3 — `:140` Action principle for S̃_g
See A-20. **Proposed:** **Open (narrowed).**

### B-O-4 — `:141` "L-functions extension | LMFDB zeros | Paper B generality"

- **Index displays:** open. But `MANIFEST.md:89` "Ladder is universal across L-functions
  with a χ^k twist on rung k [...] | **T1/T3**" and `:90` "Hardened twist (~150 L-zeros,
  generated non-circularly via `data_zeros/generate_more_lzeros.py`) [...] HONEST NEGATIVE:
  rung-2 phase did NOT harden [...] | **T1 (rung1/parity) / T3 (rung2)**"; `:96-97`
  "L-zeros built from L(s,χ) via Hurwitz zeta [...] primes never inserted."
- **Record:** `amendments.json:92` (Paper B): "The finite ordinate experiments test the
  declared spectral statistics; they neither locate nor exclude all off-line zeta zeros."
  `:32` (shuffle knife): "Results remain scoped to the stated window, unfolding and
  ensemble. [...] No finite shuffle experiment settles RH." `:72` (N3) as in A-17.
- **Audit:** [AUD-SCOPE] `:14` only.
- **Proposed:** **Display stale (partially addressed).** The row should point at
  `MANIFEST.md:89-91` (finite-window L-function evidence at T1/T3, ~150 zeros, rung 2 not
  hardened) and keep "open" for generality beyond the window, with the record's
  finite-window qualifier.

### B-O-5 — `:142` "Full SM from GL(4) fiber | conceptual breakthrough | complete derivation"

- **Record:** [AUD-SCOPE]. Action paper `:43-45`: "It is a consolidation and correction of
  the repository's calculations, not a claim that an unrestricted theory of matter has
  been completed."; `:312-314` as in A-20.
- **Audit:** `:242-245` "Symmetry alone permits different stable local alignments and both
  stable/unstable transverse spectra at the same restricted neutral data. A unique physical
  vacuum is demonstrably underdetermined."
- **Proposed:** **Open (narrowed).** The record converts "conceptual breakthrough" into a
  named list of missing inputs plus an explicit underdetermination result; the row should
  cite it.

### B-O-6 — `:143` "ER=EPR correspondence | conceptual breakthrough | holographic interpretation"

- **Index displays:** open here; `MANIFEST.md:105` "ER=EPR algebraic correspondence |
  **T2/T3** | `src/paper_c/er_epr_algebraic.py`"; Master Index `:107` "Algebraic
  non-traversability (Proposition 4.3, ER=EPR rereading)".
- **Record:** `amendments.json:96` (Paper C): "Physical holography, confinement and
  particle identification require a state space and dynamics in addition to these
  algebraic maps." `:80`: "remains a conjecture".
- **Audit:** silent on ER=EPR by name; `:172-177` on the recovered Bell identity: "this
  calculation does not derive quantum nonlocality from a new spatial dimension".
- **Proposed:** **Split.** Algebraic non-traversability stays at MANIFEST's T2/T3; the
  physical correspondence (the row's "Impact") is a conjecture by the record. The row should
  show both halves.

### B-O-7 — `:144` "Barbero–Immirzi physical value 0.2375 | external Chern–Simons computation | γ from first principles (0.274 is unconstrained value)"

- **Index displays:** open; locked row `:50` "γ (Barbero–Immirzi) | 0.274 | ACS
  information balance"; `MANIFEST.md:65` "γ = 0.274 (Barbero-Immirzi, Meissner) | **T2**".
  Paper A `:2339-2343`: "The Barbero–Immirzi parameter is not a PDG-measured quantity; the
  comparison is against the Meissner theoretical value under the same (SU(2),
  all-half-integer) counting prescription [...] The Domagala–Lewandowski value is 0.2375".
  `docs/Elimination_Ledger.md:115-123`: "γ = 0.274 → REFRACTION (value). `KILLED` [...] The
  invariant is structural — 'there is a fixed γ once a prescription is fixed' — not the
  number 0.274."
- **Record:** silent (no match for `Immirzi`, `0.274` or `0.2375` in `amendments.json`,
  the action paper, the carrier paper or the audit).
- **Proposed:** **Open (unchanged)** for O-7; **Display stale** for the locked row `:50`
  and `MANIFEST.md:65`, which should carry the ledger's 2026-06-06 verdict (value
  prescription-dependent; the structural statement is the invariant).

### B-O-8 — `:145` "Neutrino tension — RESOLVED (Elimination Ledger Q7 [...] decoupling caveat recorded)"

- **Index displays:** resolved. The same page `:153` lists "Sterile neutrino | 49 keV |
  FF06a" under "Predictions on record"; Paper A `:225-226` "Predictions: a 49 keV sterile
  neutrino". `docs/Elimination_Ledger.md:285` "RESOLVED (survives), decoupling caveat · T3
  estimate / T2 structural"; `:297-303` "Clearing the bound requires high v_R, hence high
  M_R ~ v_R, so the sterile/right-handed neutrino is **not keV-scale dark matter** at that
  scale. [...] Not a kill of the framework; a kill of the keV-DM reading."; `:287` "script
  not committed to this repository".
- **Record:** silent on the 49 keV; [AUD-FLAVOR] action-paper sentence.
- **Audit:** [AUD-FLAVOR].
- **Proposed:** **Resolved with caveat**, and the caveat must reach `:153`: one page cannot
  list "49 keV" as a prediction on record and also "resolved by removing the sterile state
  from the keV role". Propose `:153` read "49 keV (Paper A); keV-DM reading killed by Q7's
  decoupling resolution (ledger :297-303); Q7 script not in repository".

---

## C. "Locked numerical invariants (derived, never refit)" — `docs/ACS_Corpus_Map.md:42-56`

### C-1 — `:46` g₄ = g_L = g_R = 4/3

- **Index displays:** locked, "Palatini bracket (C₂ = 4/3)". Paper A `:2167`, `:2787`.
  `docs/Elimination_Ledger.md:104-113`: "g₄ = g_L = g_R = 4/3 → REFRACTION (value) /
  INVARIANT (relation). `SPLIT` [...] Change the normalization and '4/3' changes. The
  **equality** g₄ = g_L = g_R [...] survives any consistent rescaling"; `:379` "g₄ = 4/3 →
  **2/3** under Tr(TᵃTᵇ)=½δ vs δ rescaling → REFRACTION, **T1**".
- **Record:** action paper `:203-208` uses "equal gauge couplings 4/3" as the source point
  of the closure test and finds "B(λ₆−λ₇) = −2560/9. The reduced ansatz therefore fails a
  direct closure test."
- **Audit:** `:100-103` "Its QCD crossing g=4/3 occurs at **25.6476 GeV**, conditional on
  the inserted MZ and alpha_s(MZ). At that crossing the same diagnostic gives g₂≈0.658857,
  so equating one coupling is not simultaneous gauge matching."
- **Proposed:** **Split.** Equality = the invariant; 4/3 = a normalization-dependent value
  (ledger T1); the single-coupling crossing is not gauge matching (audit). Row label:
  "g₄ = g_L = g_R (relation); 4/3 in the paper's normalization".

### C-2 — `:47` λ_φ = 2√3/27 ≈ 0.1283

- **Index displays:** locked, "Koide projection"; `MANIFEST.md:60` **T2**; Master Index
  `:81` "(0.84% match to SM)". `docs/Elimination_Ledger.md:134-142` `SPLIT`: "(i) 2√3/27
  as a number of the Koide projection geometry [...] INVARIANT. (ii) The identification
  'the physical Higgs quartic *is* 2√3/27' is scale-conditioned".
- **Record:** [REC-QUARTIC]; action paper `:287-288` "Neither gives 2√3/27. These are
  roots of a fixed-gauge proxy, not fixed points of the complete running action."; `:306-308`
  "a source expression matched to an inserted value does not derive that value."
- **Audit:** [REC-QUARTIC] audit half.
- **Proposed:** **Split** — number T2, identification conditional and boundary-sensitive.
  Decision brief 2.1 (`docs/decisions_2026-10-22.md:219-311`) already finds the record
  supports its reading (C) only. Row label: "algebraic constant of the Koide projection;
  identification with the physical quartic conditional (action paper §6)".

### C-3 — `:48` h̃/h = 2/3

- **Index displays:** locked, "Koide ratio". `docs/Elimination_Ledger.md:125-132`
  "INVARIANT (candidate). `SURVIVED`"; `:403` "h̃/h (now T1)". Paper C `:822-823` "tan β =
  1/2 was a misidentification of the Yukawa ratio h̃/h ≈ 2/3 with the VEV ratio."
- **Record:** `docs/condensate_energy/selection_energy/README.md:100`: "If Ỹ=(2/3)Y, both
  Dirac mass matrices are scalar multiples of the same matrix. Their left mass squares
  commute, all generation ratios are identical, and there is no physical mixing among
  nondegenerate masses."; `:102` "A **norm-only** relation between two otherwise independent
  matrices is a different hypothesis. [...] Its matrix orientations and flavor data remain
  inputs."
- **Audit:** `:101-103` "The script's square-root mass texture is rank one, leaving
  degenerate zero-mass subspaces; its eigensolver mixing is not a nondegenerate CKM
  prediction."
- **Proposed:** **Split.** The ratio survives as an invariant of the construction; the
  matrix-level reading forbids CKM mixing at every tan β and is decision brief 2.4
  (`docs/decisions_2026-10-22.md:503`, `:543-544`). Row label: "2/3 (norm-level ratio);
  matrix-level reading excluded (selection_energy :100)".

### C-4 — `:49` 2ρ₁ + ρ₂ = 16/9

- **Index displays:** locked, "Palatini pairing"; Paper A `:2166`, `:2786`.
- **Record:** action paper `:203-208`: "both natural readings of the historical two-trace
  Δ potential require λ₆=λ₇. At the source point ρ₁=8/9, ρ₂=0, equal gauge couplings 4/3
  and zero Yukawas, the complete equations give B(λ₆−λ₇)=−2560/9. The reduced ansatz
  therefore fails a direct closure test." [REC-COUNT].
- **Audit:** `:31-32` "the old reduced potential is generally not closed under running."
- **Proposed:** **Scope-annotated.** A relation in the two-trace ansatz; that ansatz is not
  closed under one-loop running. Row label: "16/9 (two-trace ansatz; not closed under
  running — action paper §4)".

### C-5 — `:50` γ (Barbero–Immirzi) = 0.274
See B-O-7. **Proposed:** **Display stale** (ledger: value `KILLED` as
prescription-dependent; structural invariant only); record silent.

### C-6 — `:51` N_gen = 3

- **Index displays:** locked, "Jacobi truncation at BCH order 3"; `MANIFEST.md:64` **T1**
  "paper_a"; Corpus Map `:83` "Jacobi closes BCH at order 3 | ‖Jacobi‖ = 0 | exact | 1".
- **Record:** silent on N_gen; [AUD-FLAVOR] action-paper sentence (no flavor data
  selected). **Audit:** silent.
- **Proposed:** **Unchanged** as the Jacobi computation (T1); note that the record does
  not extend the count to a flavor spectrum.

### C-7 — `:52` θ_QCD = 0 exactly

- **Index displays:** locked, "prediction"; `:154` prediction on record; `MANIFEST.md:66`
  **T2** "paper_a". Paper A `:2486-2495`: "**Theorem:** θ_QCD = 0 exactly in the ACS.
  *Proof:* (i) [[f,g],[f,g]] = 0 identically (antisymmetry of the Lie bracket: [A,A] = 0 for
  any A). (ii) All fermion mass matrices are constructed from real generators of sl(4,R),
  so det(Y_u Y_d) > 0 and arg(det(Y_u Y_d)) = 0. [...] (Verified: `four_computations.py`.)";
  `:2344-2347` "θ_QCD is bounded, not measured [...] The prediction is consistent with that
  bound, which is a weaker statement than a σ-level match."; `:2953-2954` "θ_QCD = 0
  without axion. The real sl(4) structure gives θ = 0 as a theorem."
- **Record:** `amendments.json:88` (Paper A) does not mention θ; neither does the action
  paper.
- **Audit:** `:105-107`: "Its strong-CP argument also fails: [A,A]=0 does not imply
  Tr(F∧F)=0, and real matrices need not have positive determinant. The bare theta
  coefficient remains a separate action datum". ("Its" is `four_computations.py`, the
  script Paper A cites as the verification at `:2495`.)
- **Proposed:** **Contradicted.** Both steps of the printed proof are denied by the audit.
  The T2 at `MANIFEST.md:66` is not supported by the record; the "locked" and "prediction"
  labels at `:52` and `:154` should become "argument as printed fails (endpoint audit
  :105-107); bare θ is a separate action datum; open". A tier change (T2 → T4 on the
  argument as printed) is proposed, not made. Paper A's passage is manifest-bound; no
  amendment text is drafted here.

### C-8 — `:53` torsion coupling hierarchy 0 : 1 : 4

- **Index displays:** locked, "prediction"; `:155`; `MANIFEST.md:66` **T2** (shared row).
  Paper A `:2676-2680` "The 0:1:4 ratio is thus a real statement about the
  electroweak-adapted generators, not a third eigenvalue [...] Both readings are verified
  in exact rational arithmetic"; `:2968-2972` "GW-spin coupling hierarchy 0:1:4 (long-term)
  [...] The torsion correction to GW-matter coupling is suppressed by (v_R/M_Pl)² ≲ 10⁻⁶".
  Paper C `:824-825` "(b) The W/Z torsion share is a conditional prediction, not a
  theorem."
- **Record:** [REC-SELECT]: "leaves the added torsion-squared term algebraic in contortion.
  It supplies no independent contortion wave operator."
- **Audit:** `:195-202` "T² and K∧K are algebraic in K. They provide no independent
  contortion wave operator. Our component check retains all 24 contortion components. [...]
  Additional curvature-derivative terms or a separately specified defect sector could
  change that conclusion; their coefficients, boundary conditions and mode content must be
  stated. They are not generated by renaming T²."
- **Proposed:** **Split.** The ratio on the generator set (exact rational arithmetic)
  stands as algebra; the physical torsion-coupling prediction has no propagating carrier
  under the stated action. "Prediction" at `:53`/`:155` and T2 at `MANIFEST.md:66` should
  split into "algebraic ratio (exact)" and "physical coupling: carrier withdrawn by the
  24 Sept record; conditional on an added torsion sector".

### C-9 — `:54` K(T_BL, T_BL) = 32/3

- **Index displays:** locked, "Killing form"; `:95` "exact SymPy | 1/2". Paper B′
  `Spectral_Witness_Refinement.tex:249` "Killing form K(T_{B−L},T_{B−L}) = 8 Tr(T²_{B−L}) =
  32/3"; `:300` "the Killing/kinetic normalisation carries the entire residual."
- **Record:** the B′ amendment (`amendments.json:100`, in-paper `:528`) is silent on §9.
  Action paper `:107-116`: "A raw Hessian eigenvalue is consequently not automatically a
  physical mass. [...] Multiplying the entire action by an unspecified constant C instead
  changes the canonically normalized quartic to λ_can/C."
- **Audit:** `:86-90` "an undetermined common action prefactor remains physically
  relevant."
- **Proposed:** **Scope-annotated.** Exact as a Killing-form number in the stated
  normalization; carries no physical normalization by itself. Row label: "32/3 (exact, in
  the paper's normalization; the physical normalization is an open input)".

### C-10 — `:55` central charge 1/3 (= quark B−L)

- **Index displays:** locked, "Killing chain". B′ `:257-261` "coupling/K(T_{B−L},T_{B−L})
  = (32/9)/(32/3) = 1/3 [...] The physically natural invariant is the charge 1/3"; `:263`
  "**Falsifier:** B−L testing non-abelian, or a simple sector testing abelian, breaks the
  correspondence". B′ `:255` "Through this validated chain" is the subject of
  `docs/proposed_amendments_2026-10-22_pass2.md:49-76`.
- **Record:** silent on §9. **Audit:** silent; the "1/3" at audit `:222` is the summed
  Cartan variance of the balanced colour triplet, a different quantity
  (`docs/Elimination_Ledger.md:763-764` warns against this conflation).
- **Proposed:** **Unchanged** (T2 as a charge ratio), with the "validated chain" wording
  pending as proposal pass-2 §2.

### C-11 — `:56` m_H (from λ_φ chain) = 124.72 GeV

- **Index displays:** locked, "quartic → mass"; `:95` "§9 forced values (exact) [...] m_H
  124.72 | exact SymPy | 1/2"; `:156` "Higgs mass | 124.72 GeV (from λ_φ chain)" under
  "Predictions on record". B′ `:253` "m_H = √(2λ) v = 124.72 GeV", with v inserted
  (`MANIFEST.md:130` "PDG v = 246.22 GeV canonical").
- **Record:** [REC-QUARTIC]. Action paper Proposition 1 `:220-232` (the scale family:
  "physical mass-squared eigenvalues scale by a², and their signs and ratios are
  unchanged") and `:242-243` "The statement compares physically different actions. It is
  not a coordinate symmetry of one fixed action."; `:256-257` "A fixed measured Newton
  constant could provide extra dimensional data, but the matter-sector matching relation
  would still have to be derived."
- **Audit:** [REC-QUARTIC] audit half; `:307` "physical pole masses are not claimed."
- **Proposed:** **Conditional, not a prediction.** 124.72 GeV is the tree identity √(2λ)v
  evaluated with λ = 2√3/27 and an inserted v; the record's own one-loop reading of the
  same chain gives a 148 GeV tree proxy, and the scale family leaves the overall mass scale
  undetermined. Rows `:56` and `:156` should read "124.72 GeV (tree identity from λ_φ and
  inserted v; not a pole mass; conditional — action paper §6, decision brief 2.1)".

---

## D. MANIFEST Paper A rows — `MANIFEST.md:56-68`

### D-1 — `:59` SU(3) closure attractor | T3
- **Index displays:** "50k-sample numerical, not a uniqueness theorem".
- **Record:** [REC-SELECT] first sentence: "The algebraic closure calculations do not
  establish a unique microscopic dynamics." **Audit:** silent on the closure sampling.
- **Proposed:** **Unchanged (T3).** The row already disclaims uniqueness.

### D-2 — `:60` Higgs quartic λ_φ = 2√3/27 | T2
See C-2. **Proposed:** **Split** — keep T2 for the Koide-projection constant; append
"identification with the physical quartic conditional (action paper §6; audit :92-98)".

### D-3 — `:61` α₂ = 0 (representation theory) | T2
- **Index displays:** T2 "paper_a". Paper A `:2792-2797` "α₂ = 0 identically [...] because
  Φ ∼ (1,2,2) is an SU(4) singlet."; Paper C `:827-832`.
- **Record:** the complete basis (action paper Table 1, `:82-89`) lists the Φ–Δ cross
  invariants as indices 13–16: N_Φ N_Δ, Re d_Φ N_Δ, Im d_Φ N_Δ, J_Φ·J_Δ — no
  SU(4)-adjoint contraction, consistent with T^A Φ = 0. The record does not otherwise
  discuss the row. **Audit:** silent.
- **Proposed:** **Unchanged (T2).**

### D-4 — `:62` β_c = 0 no-go (tree level) | T2
- **Index displays:** T2, `src/paper_a/betac_tan_beta.py`. Paper A `:2171` "β_c (tree) | 0
  | Phase 51/52: equal-VEV no-go"; Paper C `:833-839` "extremization forces tan β = ±1,
  which by the no-go identity M_u − M_d = (h − h̃)(κ₁ − κ₂) gives V_CKM = I".
- **Record:** `selection_energy/README.md:100` (quoted at C-3): with Ỹ = (2/3)Y there is
  "no physical mixing among nondegenerate masses" at any tan β, so the consequence the no-go
  guards against (V_CKM = I) is reached by a stronger, tan β-independent route.
- **Audit:** `:101-104` (quoted at C-3).
- **Proposed:** **Unchanged (T2) with context.** The tree identity stands; its role has
  changed — decision brief 2.4 (`docs/decisions_2026-10-22.md:543-544`) records that under
  the matrix-level reading the minimal bi-doublet sector cannot produce CKM at any tan β.
  The row should cross-reference that.

### D-5 — `:63` tan β gauge-protected (CW 6→5 fails) | T4
See A-15. **Proposed:** **Scope-annotated** — applied today as the dated note under the
table; tier unchanged.

### D-6 — `:64` N_gen = 3 | T1
See C-6. **Proposed:** **Unchanged.**

### D-7 — `:65` γ = 0.274 (Barbero-Immirzi, Meissner) | T2
See B-O-7 / C-5. **Proposed:** **Display stale.** T2 for the computation under the Meissner
prescription; the ledger's 2026-06-06 verdict (value `KILLED` as prescription-dependent) is
reflected neither here nor in MANIFEST's "Falsified claims ledger" paragraph `:123-127`.
Record silent.

### D-8 — `:66` θ_QCD = 0, torsion ratio 0:1:4 | T2
See C-7 and C-8. **Proposed:** **Contradicted (θ_QCD) / Split (0:1:4).** Split the row:
θ_QCD — printed argument fails (audit `:105-107`), tier change proposed; 0:1:4 — algebraic
ratio stands, physical carrier withdrawn.

### D-9 — `:67` θ₁₃ obstruction / TM1 PMNS | T2/T3
- **Index displays:** T2/T3, `theta13_obstruction.py`, `tm1_pmns.py`. Paper A `:2328`
  "θ₁₃^PMNS (deg) | 9.216 | 8.57 | 0.12 | 5.4σ" — a negative result (obstruction).
- **Record:** silent on PMNS by name; [AUD-FLAVOR] action-paper sentence. **Audit:**
  [AUD-FLAVOR].
- **Proposed:** **Unchanged.** An obstruction is consistent with the record's flavor
  non-identification; nothing in the record promotes or retires it.

### D-10 — `:68` Riemann curvature = Layer-2 bracket; Palatini eqs solve ω→Γ→R (Schwarzschild) | T1
- **Record:** [REC-SELECT] concerns the added torsion-squared term and contortion, not the
  Levi-Civita curvature check. **Audit:** `:193-197` "R(ω)=R(ωLC)+DLC K+K∧K [...] Our
  component check retains all 24 contortion components."
- **Proposed:** **Unchanged (T1)**, noting that the row is a Levi-Civita computation and
  carries no torsion dynamics.

---

## E. Tally — 35 rows

| Row | Proposed status |
|---|---|
| A-15 | Superseded as posed (applied as a dated note; tier T4 unchanged) |
| A-16 | Open (narrowed) |
| A-17 | Open (unchanged); gloss qualified |
| A-18 | Display stale + Split |
| A-19 | Open (narrowed) |
| A-20 | Open (narrowed) |
| B-O-1 | Open (unchanged); gloss qualified |
| B-O-2 | Open (narrowed) |
| B-O-3 | Open (narrowed) |
| B-O-4 | Display stale (partially addressed) |
| B-O-5 | Open (narrowed) |
| B-O-6 | Split |
| B-O-7 | Open (unchanged); locked row display stale |
| B-O-8 | Resolved with caveat; §7 row `:153` inconsistent with it |
| C-1 | Split |
| C-2 | Split |
| C-3 | Split |
| C-4 | Scope-annotated |
| C-5 | Display stale |
| C-6 | Unchanged |
| C-7 | Contradicted (tier change proposed) |
| C-8 | Split |
| C-9 | Scope-annotated |
| C-10 | Unchanged |
| C-11 | Conditional, not a prediction |
| D-1 | Unchanged |
| D-2 | Split |
| D-3 | Unchanged |
| D-4 | Unchanged, with context |
| D-5 | Scope-annotated (applied as a dated note) |
| D-6 | Unchanged |
| D-7 | Display stale |
| D-8 | Contradicted / Split |
| D-9 | Unchanged |
| D-10 | Unchanged |

By label: Unchanged 8 · Open (unchanged) 3 · Open (narrowed) 6 · Superseded as posed 1 ·
Split 8 (A-18, B-O-6, C-1, C-2, C-3, C-8, D-2, D-8) · Scope-annotated 3 · Display stale 3
(B-O-4, C-5, D-7; A-18 and B-O-7 also carry the label) · Contradicted 1 (C-7; D-8 is its
MANIFEST copy) · Conditional 1 · Resolved with caveat 1. Total 35.

The only **tier-change proposal** is θ_QCD (C-7 / D-8): T2 → T4 on the argument as
printed. Every other proposal is a label, scope or cross-reference change.

## F. Display notes outside the 35 rows (observed while adjudicating; not changed)

- `MANIFEST.md:30` and `:132` say `acs_codebase` → "42 passed"; `docs/ACS_Master_Index.md:38`
  and `:186` say "42/42". `docs/publication/2026-09-24/README.md:31` says "The existing
  canonical suite has 46 tests" and `docs/publication/2026-10-22-rerun.md:19` records
  "46 passed". The 42 is the count on the dates those sections were written; a dated
  pointer to the current count would stop readers taking it as current.
- `docs/ACS_Corpus_Map.md:182-183`, the §8 picture, still prints "6 params (4 free)";
  the corrected row at `:70` now says to read the picture with it. Redrawing the picture is
  left to the owner.

## G. What this note changed, and did not

- **Applied** (unbound files only): `docs/ACS_Corpus_Map.md:70` (the audited coefficient
  count, citing the action paper); `MANIFEST.md:63` (scope pointer) plus the dated
  tan β / Coleman–Weinberg note under the Paper A table; `docs/ACS_Master_Index.md:150`
  (pointer) plus the identical dated note under item 20; the link in `docs/README.md`.
- **Not applied:** any tier; any label in the 35 rows beyond the two notes; Paper C's
  `:856-858` wording (manifest-bound — a paste-ready amendment was drafted alongside this
  note and handed to the owner, not committed); Paper A's θ_QCD theorem (manifest-bound; no
  text drafted).
- **Verification:** `python3 -I scripts/check_navigation.py` on the tree with this note
  (reports `failures: []`, 241 local links, of which one is the link added to
  `docs/README.md`) and `git status --short` showing only the five intended files.
