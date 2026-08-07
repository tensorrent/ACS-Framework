# Editorial Audit — 2026-08-07

A full-corpus editorial review (every manuscript and consolidated document read end to
end) surfaced the findings below. They are recorded here in the spirit of the corpus's own
adversarial-compression discipline: **these are editorial-consistency findings, not
scientific verdicts** — each one is a place where two documents disagree, a citation does
not resolve, a tier label is inconsistent with the tier rules, or wording overclaims
relative to the recorded status. Items are retained until fixed in the source documents;
fixes should cite this audit.

Severity: **high** = affects the credibility or reproducibility of a load-bearing claim;
**medium** = inconsistency a careful reader will trip over; **low** = polish.


## High (8)

### H1. `docs/ACS_FRAMEWORK_SKILL.md`

Section 4.3 'Proved Theorems (10)' lists 'SU(3) closure attractor' as theorem #1 with method 'BCH + computational', but MANIFEST tiers it T3 ('numerical, not a uniqueness theorem') — a direct violation of the skill's own rule 'Never let Tier 3 pass as Tier 2' (sec 3).

*Suggested fix:* Move the SU(3) closure attractor out of the Proved Theorems table (or annotate it as T3 numerical selection) so the skill matches the MANIFEST tiering.

### H2. `docs/ACS_Technical_Whitepaper.md`

The whitepaper carries no tier labels and overclaims relative to the framework's own verdicts: sec 2.2 states sl(3,R) 'is the unique subalgebra' (tiered T3 elsewhere, with MANIFEST line 48 explicitly noting '50k-sample numerical, not a uniqueness theorem'), and sec 2.3 presents λ_φ = 2√3/27 and γ ≈ 0.274067 as 'Physical Invariants' although the Elimination Ledger (OOS01 Q1, lines 350-359) machine-confirmed both bare values as REFRACTIONS (T1) and killed γ = 0.274 as prescription-dependent.

*Suggested fix:* Add tier annotations to each whitepaper claim, soften 'unique subalgebra' to the numerical-selection statement, and update sec 2.3 to the ledger's post-kill wording (relations invariant, bare values refractions).

### H3. `docs/Elimination_Ledger.md`

Kill-test code is cited at ephemeral /tmp paths that do not exist in the repository (lines 143 '/tmp/q3_floor.py', 168 '/tmp/q6_offdiag.py', 192 '/tmp/q5_hp.py', 258 '/tmp/q4_largeL.py', 270 '/tmp/q7_neutrino.py', 377 '/tmp/q4_monotonicity.py'), and 'q4_cfunction_testbed.py' (line 223) and 'q3_scaling_test.py' (line 398) are cited with no path and are absent from the repo (verified by find). This breaks the framework's own T1 standard ('reproducible by running the code').

*Suggested fix:* Commit the kill-test scripts into the repo (e.g. code/elimination_ledger/) and update the ledger citations to repo-relative paths; where a script is lost, downgrade the entry's tier note accordingly.

### H4. `papers/core_trilogy/Holographic_Spectral_Inversion.tex`

Order-counting error in the proof of the central inversion theorem (thm:inversion, Step 3): it writes 'The BCH-TE morphism gives Delta-I(f,g) = eps^2 E[f-g] + O(eps^3)' - but per the cited lemma E[f-g] is the FIRST-order (eps^1) coefficient, and the very next sentence says 'The first-order transfer entropy flips sign exactly.' The displayed eps^2 contradicts both the lemma and the surrounding text.

*Suggested fix:* Change the display to Delta-I = eps E[f-g] + O(eps^2) (and note that the bracket term 2 eps^2 <[f,g],.> is invariant under exchange up to sign), keeping the argument consistent with Lemma bch-te.

### H5. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`

Incorrect load-bearing cross-references: line ~833 cites 'the Atiyah-Singer chiral modes of Theorem 3.2 (thm:gravity-acs)' and Conjecture 4.14 (conj:lepton) cites 'the chiral zero-modes of D_T established in Theorem 3.2' - but thm:gravity-acs ('Gauge field pair is an ACS') contains no Atiyah-Singer statement, no operator D_T, and no chiral zero-mode result. Readers are pointed to a theorem that does not establish the claimed result.

*Suggested fix:* Point these citations at the actual source of the chiral-mode evidence (the torsion-lattice computational verification) and reword 'established in' to reflect its computational, not theorem, status.

### H6. `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`

Tier-discipline inconsistency on the central claim: the abstract and Theorem 2.2 (thm:FN-acs) call the converse 'Conjecture T4-prime', but Section 4 states the same claim as 'Theorem T4-prime (stationarity <=> RH)' with a proof whose Steps 2-3 rest on numerically estimated constants (C < 0.29 for N <= 200) and an unproved minimum-gap bound delta_N > 0; the Open Problems section then lists it under 'Confirmed'. A theorem label on a claim the paper itself says is conditional on unproved bounds overclaims relative to the repo's own tier discipline.

*Suggested fix:* Either downgrade thm:T4prime to a conjecture/conditional theorem with the delta_N hypothesis stated in the theorem body, or rename the earlier references so the paper uses one consistent label; move it from 'Confirmed' to a conditional tier in sec:open.

### H7. `papers/later_FF06_series/One_Mechanism_Many_Forms_Sigma.tex`

Status contradiction with The_Elimination_Ledger.tex on the corpus's central claim. One Mechanism (dated June 2026) carries Link 3, the Delta-I = c identification, as the 'central unifying conjecture' (T2/T3, open) on which the whole synthesis is conditional (sec 2, lines 113-134). The Elimination Ledger (also dated June 2026) retires exactly this claim as T4-as-stated: 'no reading is both novel and true. The highest-collapse target is retired' (sec 4.2, lines 280-283). Neither paper acknowledges the other's verdict, so a reader cannot tell which supersedes which - and by the corpus's own tier discipline, carrying a retired claim as an open conjecture without citing its retirement is an overclaim.

*Suggested fix:* Add a dated note to One_Mechanism_Many_Forms_Sigma.tex (or the Elimination Ledger) stating the chronological order and reconciling the two verdicts - e.g. either Link 3 is restated in a form that survives the ledger's three structural objections (sign, fixed-point value, category), or the synthesis's conditional claim is explicitly re-scoped to the retired status.

### H8. `papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex`

Reproduction scripts cited in the Reproduction appendix do not exist anywhere in the repository: verify_ledger.py, predictive_test.py, motif_test_suite.py, check2_gcd_overlap.py, and the Rust shape_engine crate with verify.sh (lines 589-595) are all absent (verified by repo-wide find). The same applies to The_Elimination_Ledger.tex appendix (q3_scaling_test.py, q4_cfunction_testbed.py, lines 477-484) and The_Reversible_Flattening.tex footer (verify_ledger.py, line 249). Only display copies (*_disp.py) of three scripts exist in papers/later_FF06_series/. The reproducibility promise ('all numerical claims reproduce under seed 20260423') cannot be exercised from the repo as shipped.

*Suggested fix:* Add the cited scripts to the repository (e.g. under code/ or harness/) or amend the reproduction appendices to state where the artifacts live; if the *_disp.py listings are the canonical source, rename or note the correspondence explicitly.


## Medium (48)

### M1. `docs/ACS_Corpus_Map.md`

Line 19 identifies FF06f as 'Density, Positions, Spacings (three-layer decomposition)' while papers/README.md line 42 maps FF06f to Prime_Carrier_Position_Form_Factor.tex (and papers/later_FF06_series/Three_Layer_Decomposition.tex exists as a separate paper), so the FF06f designation is assigned to two different papers in different index documents.

*Suggested fix:* Reconcile the FF06f row in docs/ACS_Corpus_Map.md with papers/README.md, giving the three-layer decomposition paper its own distinct series code if it is a separate work.

### M2. `docs/ACS_Corpus_Map.md`

Failures F-14 through F-23 (sec 5) are attributed to '(this session)' with Paper column 'session', and the footer says 'Failures F-14 through F-23 are from the current session' — session-relative references with no date, author, or artifact links, meaningless to a later reader and unreproducible.

*Suggested fix:* Replace '(this session)' with a date stamp and pointers to the corresponding Elimination Ledger entries or committed test scripts.

### M3. `docs/ACS_FRAMEWORK_SKILL.md`

Internal parameter-count contradiction: sec 4.2 is headed 'Parameter Ledger (7 Inputs)' with 5 free + 2 calibrations, while sec 1 and sec 8 state '19+ (SM) → 6 (ACS Branch A) = 4 free + 2 calibrations', and the corpus map (sec 3) also says '4 free + 2 calibration = 6'. The StrickenBy{C1.4-D1} note changes ledger membership but the counts were never reconciled.

*Suggested fix:* Reconcile the free-parameter count across sec 4.2, sec 1, sec 8, and ACS_Corpus_Map.md sec 3 to a single number, and update the section heading.

### M4. `docs/ACS_FRAMEWORK_SKILL.md`

Open problem 4 (sec 4.5, line 134) grounds its 'Partially closed' status in 'NOTE_landau_identity_transport_20260705.md in the TR-2026-FF06-ACS instrument suite, which is not included in this repository' — a load-bearing status change resting on material readers cannot access.

*Suggested fix:* Either include the note in the repo or downgrade the open-problem status text to what repo-resident evidence supports.

### M5. `docs/ACS_FRAMEWORK_SKILL.md`

Open-problem count mismatch with the corpus map: sec 4.5 lists 'Open Problems (6)' while ACS_Corpus_Map.md sec 6 lists 8 (O-1..O-8, adding the Barbero-Immirzi physical value and the neutrino tension) — and the ledger has since resolved Q7 (neutrino), which neither document reflects.

*Suggested fix:* Synchronize the open-problem lists across the skill, the corpus map, and the ledger's resolutions.

### M6. `docs/ACS_Technical_Whitepaper.md`

Sec 4.1 asserts 'This algebraic orthogonality enforces the ER=EPR holographic correspondence', but the skill (sec 4.5 item 6) and corpus map (O-6) both list the ER=EPR correspondence as an open problem requiring a 'conceptual breakthrough', and MANIFEST tiers it only T2/T3.

*Suggested fix:* Replace 'enforces' with the tiered claim (e.g. 'provides an algebraic correspondence consistent with ER=EPR; full correspondence remains open, T2/T3').

### M7. `docs/Elimination_Ledger.md`

References to private machines/agents and undefined internal labels: 'OOS01 RESULTS (2026-06-06, Mac via Antigravity)' (line 320), 'CORRECTING Antigravity's pin' (line 333), 'logged to W2F record' and 'Category A*' (lines 366-368), and the private 'trinity-wasm' codebase with a withdrawn '489× faster' claim (lines 38, 324-331). None of OOS01, Antigravity, W2F, Category A*, or trinity-wasm is defined anywhere in the repo, and the Q2 bench is not reproducible from repo contents.

*Suggested fix:* Add a short glossary/footnote defining OOS01, Antigravity (the external agent/machine), W2F, and Category A*, and either vendor the trinity-wasm bench inputs or mark Q2 as externally-verified-only.

### M8. `papers/ACS_Deterministic_AI_Stack_PDR.tex`

Section 1 (lines 238-241) asserts 'These are not analogies; they are direct mappings because the ACS governs information flow in any codependent system, whether physical or computational' — a universal claim with no tier-qualified support, exceeding the framework's own graded-evidence discipline (the physics results it maps from are a mix of proved, numerical, and conjectural).

*Suggested fix:* Qualify the claim (e.g. 'we treat these as direct mappings under the ACS hypothesis') or cite the specific tiered results backing each row.

### M9. `papers/ACS_Deterministic_AI_Stack_PDR.tex`

The traceability section and sec 6.1 cite 'Paper A' (secs 2.1, 2.3, 4.3, 5.1, 6.8, C.1, C.2) and 'Paper C (The Inversion Arc)' without ever giving filenames, full titles, or repo paths, so the cross-reference index cannot actually be followed by a newcomer.

*Suggested fix:* Add a key mapping Paper A/B/C/D to the actual files under papers/core_trilogy/.

### M10. `papers/Form_Function_and_Asymmetry.tex`

Line 48 uses \renewcommand{\Form}{\mathbf{e}} but \Form is never previously defined by the document or any loaded package, which is a LaTeX error under normal compilation; the very next line correctly uses \providecommand for \Func, so the asymmetry looks accidental.

*Suggested fix:* Change \renewcommand{\Form} to \providecommand{\Form} (or \newcommand).

### M11. `papers/Form_Function_and_Asymmetry.tex`

Hardcoded cross-reference numbers have drifted from the auto-numbering: Appendix B is titled 'Exact Symbolic Verification of Lemma~2.9' (line 2221) but the BCH-TE lemma auto-numbers as 2.10 (Theorem thm:acs-DI is 2.9) — the PDR's own traceability table cites it as 'Lemma 2.10'; the proof of Theorem 2.9 cites 'Table~1' (line 456) though the automaton table in sec 2.4 is an unnumbered tabular and the numbered copy is Table 1 only via the later sec 8 float.

*Suggested fix:* Replace all hardcoded numbers (Lemma 2.9, Table 1, Theorem 4.1, Proposition 9.x in the appendices) with \ref/\label references.

### M12. `papers/Form_Function_and_Asymmetry.tex`

Appendix C (app:numerics, lines 2255-2265) documents 'Coupled oscillator simulations (Section~2.3)' with omega_1, omega_2, odeint parameters, but Section 2.3 is 'The BCH-transfer-entropy morphism' and no coupled-oscillator section exists anywhere in the paper — a leftover from an earlier draft.

*Suggested fix:* Either restore the coupled-oscillator section or delete/relabel this appendix entry.

### M13. `papers/Form_Function_and_Asymmetry.tex`

Line 1974 refers to 'The previous Postulate~10.2' but no Postulate 10.2 exists in this document (the postulate environment is defined but never used); the reference points to a superseded draft the reader cannot see.

*Suggested fix:* Rewrite as 'an earlier draft's weight-fraction postulate' or cite the archived version explicitly.

### M14. `papers/Form_Function_and_Asymmetry.tex`

Proposition prop:selection (lines 1525-1553) asserts sl(3,R) 'is therefore the unique closure attractor' but the proof is 'All claims verified computationally' over only 100 randomly sampled subspaces; a 100-sample scan supports 'no competing structure was observed', not uniqueness — the Proposition label overstates the T3-numerical evidence.

*Suggested fix:* Downgrade to a conjecture/numerical observation or state uniqueness as 'unique among sampled subspaces' in the proposition text.

### M15. `papers/Form_Function_and_Asymmetry.tex`

Proposition prop:chirality (lines 1566-1594) claims an 'if and only if' uniqueness for the chirality map, but the proof is an 'exhaustive scan over the parameter space ... at resolution 0.5' — a finite grid cannot establish an iff over continuous parameters, so the stated verification tier does not support the biconditional as proved.

*Suggested fix:* Either give the (easy) algebraic argument for the iff or restate the result as grid-scan evidence.

### M16. `papers/Form_Function_and_Asymmetry.tex`

Theorem thm:acs-DI is presented as a Theorem, yet Section 11.4 concedes its non-generic-case induction 'uses the convergence of the BCH-Campbell-Dynkin series in an informal way' — the label claims more than the paper's own stated proof status, a mismatch with the repo's tier discipline.

*Suggested fix:* Mark the non-generic branch as a lemma-with-gap or annotate the theorem statement with the caveat from sec 11.4.

### M17. `papers/core_trilogy/Holographic_Spectral_Inversion.tex`

Hard-coded cross-document references that do not resolve: 'Theorem C of Paper A' (sec:taxonomy) - Paper A has no Theorem C and never states ad^3 = (16/9) ad under that name; 'Paper A, S 6.8' (gaps items 7-8) - the torsion-hierarchy material is an appendix subsection of Paper A, not section 6.8; 'Paper B, Section 5' for the Wronskian Leibniz failure - the Leibniz remark (rem:not-poisson) is in Paper B Section 2. Also 'Lemma 2.5 of [Wallace2026a]' repeats the wrong hard-coded number.

*Suggested fix:* Replace all hard-coded cross-paper numbers with named references (theorem/remark names or labels) and re-verify against the current builds.

### M18. `papers/core_trilogy/Holographic_Spectral_Inversion.tex`

Historical attribution likely wrong and uncited: 'In 1867, Alexander Reina Russell proposed a wavelength-based spiral arrangement of the elements, predating Mendeleev' - the octave-periodicity observation with noble-gas-like nodes is standardly attributed to John Newlands (1865); no citation is given for 'Alexander Reina Russell', and the name does not correspond to a documented figure in the history of the periodic table.

*Suggested fix:* Verify the intended figure (Newlands' law of octaves, 1865?) and add a citation, or remove the historical claim.

### M19. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`

Internal contradiction in the torsion-tier count: line ~2613 says all 15 generators 'fall into exactly three tiers', but only Tier 0 and Tier 2 are then defined; the Figure fig_torsion_tiers caption says they 'fall into two tiers'; and the abstract advertises a '0:1:4' (three-value) coupling hierarchy. Three mutually inconsistent counts of the same result.

*Suggested fix:* Reconcile: either define the missing Tier 1 (the electroweak tier implied by 0:1:4, per Paper C's gaps list item 7) or state two tiers consistently in text, figure caption, and abstract.

### M20. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`

PDG comparison text does not match its own table: the table (sec 'Derived matches: PDG comparison') lists 9 observables, of which 7 are within 2 sigma (m_H at 3.2 sigma and theta13 at 5.2 sigma are not), yet the following sentence claims 'Nine of eleven matches are within 2 sigma of the PDG central value.'

*Suggested fix:* Correct to 'seven of nine' or add the two missing rows the count refers to.

### M21. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`

Search-and-replace artifacts leave garbled prose: '(the computational verification (Section 4))' is used as a noun phrase ~6 times, including the doubled form 'see the computational verification (Section 4) for computational evidence'; 'Four further claims are required for full \n the SM generation conjecture' (~line 1435); 'the precise question replacing the original the SM generation conjecture' (~line 1519); and 'the self-resolving property of the self-resolving property' (~line 838).

*Suggested fix:* Re-edit the replaced phrases by hand: e.g. 'the torsion-lattice verification of Section 4', 'required to complete the SM generation conjecture', 'replacing the original SM generation conjecture', 'the self-resolving property of the gauge system'.

### M22. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`

Verification-suite size is inconsistent across the trilogy: Paper A's abstract says 'a 76-script verification suite', while Paper B sec 1 says 'the full development, including ... the 57-script verification suite, is in the companion paper' and Paper C's intro says 'Paper A ... (57 verification scripts)'.

*Suggested fix:* Pick the current count (or say 'the verification suite' without a number) and align all three papers.

### M23. `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`

Broken companion-paper attributions: 'the tensegrity atom of \cite{Wallace2026a}' (~line 339), 'the tensegrity form of \cite{Wallace2026a}' (~line 615), the ratio rho = alpha*gamma/(beta*kappa) attributed to Wallace2026a, and 'the ACS coupling order definition~\cite{Wallace2026a}' - Wallace2026a is Paper A (Colour from Gravity), which contains no tensegrity atom, no rho = alpha*gamma/beta*kappa, and whose tensegrity content lives in Paper C. Similarly 'Lemma 2.5 of \cite{Wallace2026a}' is hard-coded, but in Paper A the BCH-TE lemma is not numbered 2.5 (the shared counter makes 2.5 the Information Asymmetry definition).

*Suggested fix:* Repoint tensegrity references to Paper C (Wallace2026c) or to wherever the tensegrity atom is actually defined, and replace hard-coded 'Lemma 2.5' with the lemma name ('the BCH-TE morphism lemma') to survive renumbering.

### M24. `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`

Orphaned label and leftover editorial scaffolding: '\label{sec:comp}' (line ~461) sits between a subsection end and the next \subsection with no sectioning command of its own, so '\S\ref{sec:comp}' ('the acoustic-structure subsection of S...') resolves to whatever numbered unit precedes it; and lines ~1129-1132 retain the integration comment '% NEW SECTIONS FOR PAPER B EXTENSION / Insert between current Section 7 ... and Section 8' in the source.

*Suggested fix:* Attach sec:comp to the intended sectioning command and delete the insertion-instruction comment block.

### M25. `papers/core_trilogy/Spectral_Witness_Refinement.tex`

Off-by-one hard-coded section numbers: the charge/coupling section renders as Section 12, but the title-page date line, the abstract, the summary table rows, and the internal bold headings all call it 'S13' / '13.1' / '13.2' / '13.3'; the actual Section 13 is 'Form vs. function'. Readers following '\S13' land in the wrong section.

*Suggested fix:* Use \label/\ref instead of literal section numbers, or renumber the bold paragraph headings to 12.1-12.3 and fix the abstract/date/table references.

### M26. `papers/core_trilogy/Spectral_Witness_Refinement.tex`

The 'Companion documents' section references four files - where_my_hunches_went.md, operator_constraints.md, uniformity_addendum.md, admissibility_note.md - none of which exist anywhere in the repository (verified by find). The casual filename 'where_my_hunches_went.md' is also out of register with the paper's otherwise formal tone.

*Suggested fix:* Either add the companion documents to the repo (e.g. under docs/) with these names, or update the section to point at the files that do exist (docs/Elimination_Ledger.md etc.) and drop the missing ones.

### M27. `papers/discrete_geometry_formalism.tex`

Internal inconsistency: sec 1.2 (line 43) says the rewrite maps 'generate a non-commutative semigroup action', but sec 3 (line 70) says 'Because the rewrite algebra is non-associative, we define the coherence obstruction tensor'; a semigroup is associative by definition, and the obstruction defined is a commutator, which measures non-commutativity, not non-associativity.

*Suggested fix:* Change 'non-associative' to 'non-commutative' (or drop the semigroup claim if associativity genuinely fails).

### M28. `papers/later_FF06_series/One_Mechanism_Many_Forms_Sigma.tex`

The tier legend in the abstract (line 57) redefines T3 as 'conjecture' ('Tiers: T1 measured, T2 proven/forced, T3 conjecture, T4 falsified'), whereas every other paper in the series defines T3 as 'numerically verified, not theorem-level' (e.g. The_Geometry_Engine.tex lines 66-68, Process Record sec 2.2, Elimination Ledger sec 2.2). A newcomer cross-reading the corpus will assign different meanings to the same label.

*Suggested fix:* Use the standard T3 definition and, if a conjecture tier is needed, introduce a distinct label rather than overloading T3.

### M29. `papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex`

Multiple claims are verified only against private, unpublished artifacts a reader cannot inspect: 'live OmniForge/AISO source', 'the kernel whitepaper', 'production source' and the AISO motif-memory production merge path (secs 7-8; also When_a_Number_Lies.tex sec 6 and The_Reversible_Flattening_Monograph.tex sec 11). The falsifications and the surviving integration are therefore unreproducible from the public record, in tension with the papers' reproducibility framing.

*Suggested fix:* State explicitly in each affected section that the engineering-side evidence rests on private source unavailable in this repository, or include redacted excerpts/hashes of the relevant source so the claims are at least auditable.

### M30. `papers/later_FF06_series/Three_Layer_Decomposition.tex`

Section 3 is headed 'Spacings are pure GUE, arithmetic-blind (T2)' (line 86), but the evidence presented is a numerical perturbation table (spacing-histogram distances at various epsilon, with sigma bands) - a finite-scale numerical result. Under the corpus's own tier definitions (T2 = proven or forced by a stated argument; T3 = numerically verified, not theorem-level, which 'cannot stand in for T2' per the Process Record sec 2.2), this appears to be a T3 result labeled T2. The paper also uses tier labels T1/T1'/T2 in headings without ever defining the tier scheme, unlike its companions.

*Suggested fix:* Either relabel the section T3 or add the forcing argument that earns T2; add a one-line definition of the four-tier scheme so the paper is self-contained.

### M31. `papers/later_FF06_series/When_a_Number_Lies.tex`

Line 151-152: 'each violation by a DOWNGRADED or FALSE-FIT or SEAM result above' references a grade 'SEAM' that is not part of the grading scheme defined in sec 3 (HIT, SPLIT, DOWNGRADED, FALSE FIT, lines 86-87), and no table row carries a SEAM grade. Presumably SPLIT is meant.

*Suggested fix:* Change 'SEAM' to 'SPLIT' (or add SEAM to the defined grade list if it is intentionally distinct).

### M32. `papers/methodology/Form_Function_Relativity.tex`

The measurement table (lines 126-127) shows repulsion and shape reverting from FORM at GUE-marginal (0.2 and 0.1 sigma) back to FUNC at GUE-full (5.3 and 6.5 sigma), which on its face contradicts Proposition 1's 'refining the frame can turn function into form but never the reverse' (line 89) and the 'flips once and stays flipped' claim of Principle 1 (line 77); the honest-edges paragraph (line 155) explains only the lag-1 cell as a finite-N apparatus effect and never addresses the repulsion/shape reversal.

*Suggested fix:* Extend edge (i) in section 6 to explicitly cover the repulsion and shape GUE-full cells (5.3/6.5 sigma) as the same finite-N approximation artifact, or annotate those cells in the table, so the staircase claim is not contradicted by its own table.

### M33. `papers/methodology/Prime_Carrier_Position_Form_Factor.tex`

Lines 61 and 148 claim the functional is 'the shuffle-knife prime-resonance witness reused verbatim,' but FF06e's witness is sum over p<=29 of <cos(gamma log p)>^2 (Spectral_Rigidity_Shuffle_Knife.tex line 71) while FF06f's eq. (1) is |sum_j exp(-i f gamma_j)|^2/N summed over p in {2,...,13} — a different functional form and a different prime cutoff, so 'verbatim' overstates the identity.

*Suggested fix:* State the exact relationship between the two functionals (the FF06f power is the complex-exponential generalisation of the FF06e cosine witness) and note the changed prime cutoff, replacing 'verbatim' with an accurate description.

### M34. `papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex`

Line 88 contains a source comment referencing an internal work order ('% STRUCK 2026-07-02 per WO-03 C1.5: naive surrogate spacing definition.') that no reader can resolve, and the correction paragraph at line 89 is spliced mid-flow immediately after 'They are reading the universality class,' declaring the table's 0.4-1.0 sigma FORM deviations 'purely artifacts of this re-interpolation path' while the abstract (line 42) still reports '0.4-1.0 sigma from the surrogate null' without that caveat.

*Suggested fix:* Move the WO-03 change note to a changelog or ledger file, integrate the permute-then-reinterpolate clarification as its own labelled remark, and add the artifact caveat (or the corrected zero-by-construction statement) to the abstract and table caption.

### M35. `papers/notes/Adjoint_Clifford_Signature_Selection.tex`

The filename and the subtitle in the \date field (line 35: 'Adjoint Spectral Minimization and Bipartite Signature Selection in Clifford Algebras') promise Clifford-algebra content, but the word 'Clifford' never appears in the body; the note is entirely about sl(n) Lie-algebra gradings.

*Suggested fix:* Rename the file / subtitle to match the actual content (e.g. 'Grading Selection from Adjoint Spectral Activity in sl(n)') or add the Clifford-algebra connection the title implies.

### M36. `papers/notes/Adjoint_Clifford_Signature_Selection.tex`

Broken internal cross-reference: Test 3 (lines 519-521) says ternary splits 'are correctly handled by the weighted criterion of part (iii)', but Theorem 1 part (iii) is the binary-split case; the weighted max-cut criterion is part (ii). The Table 2 caption repeats a similar attribution.

*Suggested fix:* Change 'part (iii)' to 'part (ii)' in the ternary-split sentences.

### M37. `papers/notes/Adjoint_Clifford_Signature_Selection.tex`

Theorem 1 (thm:selection) includes part (iv) whose proof is deferred entirely to numerics ('part (iv) is verified numerically', line 283-284). Packaging a numerically-verified statement inside a theorem labelled as proved overclaims relative to the corpus's own T2 (proved) vs T3 (numerical) tier discipline.

*Suggested fix:* Demote part (iv) to a separate numerically-supported proposition or observation, matching how Observation obs:compact is handled.

### M38. `papers/notes/Critical_Line_As_Fibered_Object.tex`

No bibliography: companion works are cited only by nicknames ('Paper C', 'Paper B'', 'The Geometry Engine', 'The Reversible Flattening') with no \cite entries or file paths for the documents themselves, unlike every other note in the set. A newcomer cannot resolve which repo files these are.

*Suggested fix:* Add a thebibliography block (or footnote paths) mapping each nickname to its repo file, as the Klein-Foam and Density-Engine notes do.

### M39. `papers/notes/Critical_Line_As_Fibered_Object.tex`

Line 199-200 cites a development branch ('branch claude/torsion-topological-condensation-h6v40k') as the location of test_conjecture_hypercone_projection.py, but the file exists on the current branch at code/acs_codebase/extras/; citing an ephemeral AI-session branch inside a research note is fragile and reads as an internal-machine reference.

*Suggested fix:* Cite the in-tree path code/acs_codebase/extras/test_conjecture_hypercone_projection.py instead of the branch name.

### M40. `papers/notes/Critical_Line_As_Fibered_Object.tex`

Tier-discipline stretch: line 254-255 labels statistical fit results (rung-1 twist R = 0.99, seam density law ~0.99 coupling) as 'decisive (T1)', while elsewhere in the corpus T1 denotes machine-verified exact results (e.g. non-traversability at |c| < 10^-16). Correlation-level evidence labelled with the exactness tier overclaims relative to the bundle's own tier semantics.

*Suggested fix:* Label the statistical results T3 (or define a distinct 'decisive-statistical' tier) and reserve T1 for machine-precision identities.

### M41. `papers/notes/Density_Engine_Many_Worlds.tex`

Unresolvable paths: Appendix A references \texttt{Aiso_build_artifacts/eigen_path_daw_viz/} (line 382) and \texttt{density-engine.canvas.tsx} (line 404), neither of which exists anywhere in the repository — they appear to be artifacts on a private build machine.

*Suggested fix:* Either commit the visualisation harness under code/ or visualizations/ and update the paths, or mark them explicitly as external/unpublished artifacts.

### M42. `papers/notes/Flag_Condensate_Nuclear_Decay.tex`

Inconsistent coupling label: the BPST instanton action is written S_0 = 8pi^2/g_weak^2 (lines 100-102) while the surrounding derivation is explicitly about the colour-confining (strong/Yang-Mills) throat; the 'weak' subscript contradicts the colour setting and is never explained.

*Suggested fix:* Rename the coupling (e.g. g_s or plain g) or add a sentence justifying the electroweak subscript.

### M43. `papers/notes/Flag_Condensate_Nuclear_Decay.tex`

Overclaim relative to the note's own tier discipline: 'The exact transmission coefficient T' (line 140) and 'gives the exact half-life' (lines 154-156) - the half-life formula contains the data-extracted P_alpha (which the note's own Remark says is not predicted from first principles), and T is a numerical transfer-matrix output, so 'exact' overstates both.

*Suggested fix:* Replace 'exact' with 'transfer-matrix' / 'model' in both places, consistent with the P_alpha status remark.

### M44. `papers/notes/Flag_Condensate_Nuclear_Decay.tex`

Unsupported table entries: Table 2 (lines 244-261) lists Sphaleron W = 90.000 and Superconductor (NbTi) W = 17.400 with no derivation, data source, or code reference anywhere in the note, unlike the nuclear column which is fully cross-validated; the round '90.000' especially reads as a placeholder.

*Suggested fix:* Add a derivation or citation for the sphaleron and fluxon W values, or mark them as illustrative order-of-magnitude entries.

### M45. `papers/notes/Mobius_Ribbon_Capacitance.tex`

Broken cross-reference: the abstract (line 40), the Remark at lines 215-221, and the Acknowledgments (lines 239-240) all cite the companion's '\S4.1' for the geometric-fidelity caveat / revision path, but in Mobius_Screw_Electron.tex the geometric-fidelity subsection is \S4.2 (sec:C-fidelity); \S4.1 is 'Double-cover annulus'.

*Suggested fix:* Change the three '\S4.1' citations to '\S4.2' (or cite the label sec:C-fidelity by name).

### M46. `papers/notes/Mobius_Ribbon_Capacitance.tex`

Internal contradiction on artifacts: the abstract promises 'capacitances and alpha^-1 are written to machine-readable results' (line 48), but Section 4 says 'Artifacts: the script's stdout (results JSON and run logs not committed to this repository)' (lines 159-163) - the machine-readable results are not actually in the repo, unlike the other notes in the cluster whose JSONs are committed under docs/.

*Suggested fix:* Commit the results JSON (matching the palpha_overlap pattern) or soften the abstract's 'machine-readable results' claim.

### M47. `papers/notes/Mobius_Screw_Electron.tex`

Bibliography path that does not resolve: the ribboncap2026 entry (lines 358-364) cites 'mobius_ribbon_capacitance.tex / papers/notes/Mobius_Ribbon_Capacitance.tex' - the lowercase alternate filename does not exist anywhere in the repository. The same lowercase-alternate pattern appears in Mobius_Ribbon_Capacitance.tex (line 249), Flag_Condensate_Nuclear_Decay.tex (line 285), Flag_Condensate_Palpha_Overlap.tex (lines 214, 220), Flag_Condensate_Palpha_Throat_Overlap.tex (lines 280-293), and Flag_Condensate_Palpha_Refined.tex (lines 421-431, where only the lowercase names are given).

*Suggested fix:* Drop the lowercase alternates and cite only the real repo paths (papers/notes/Capitalized_Name.tex).

### M48. `papers/notes/Prime_Gap_Transition_Operator.tex`

Arithmetic inconsistency in the falsification of uniform contraction (line 254): the stated fit rho(P_m) ~ 0.07 * phi(m)^0.75 predicts rho = 1 at phi(m) ~ 35 (14.29^(4/3) ~ 34.6), not 'near phi(m) ~ 50' as written.

*Suggested fix:* Recompute the crossing point from the quoted fit (or quote the fit constants that actually give ~50).


## Low (51)

### L1. `MANIFEST.md`

The status label 'RC1-scoped' is used twice in the Flag Condensate table (lines 148, 150) but 'RC1' is never defined anywhere in the five consolidated documents.

*Suggested fix:* Define RC1 (release-candidate scope?) at first use or in a status-label legend.

### L2. `docs/ACS_Corpus_Map.md`

The sec 8 ASCII map uses the undefined cryptic abbreviation 'inversion = c/a-thm' for the QFT column, and casual shorthand throughout the diagram; 'c/a-thm' appears nowhere else in the documentation.

*Suggested fix:* Expand 'c/a-thm' to its full name (presumably the c/a-theorem of Paper C's inversion arc) at first use.

### L3. `docs/ACS_Technical_Whitepaper.md`

The whitepaper (sec 5) attributes the Deterministic AI Stack to 'Paper D', but no Paper D exists in the MANIFEST papers table or the corpus map (the nearest object is the AISO living document) — a dangling cross-reference.

*Suggested fix:* Either map 'Paper D' explicitly to the AISO/PDR document (papers/ACS_Deterministic_AI_Stack_PDR.*) or drop the Paper D label.

### L4. `docs/Elimination_Ledger.md`

Typo 'computatioanal_work_ACS' (line 80) — misspelling of 'computational'; if this is the literal directory name on the external machine it should be flagged as such, otherwise it is a typo in a governance document.

*Suggested fix:* Correct to 'computational_work_ACS' or add '(sic, directory name as-is)'.

### L5. `docs/Elimination_Ledger.md`

The first queue entry is named 'T1-TARGET' (line 30), overloading the tier label 'T1'; the session scorecard then refers to the same target as 'Q1' (line 350), so the target carries two inconsistent names, one colliding with the verification vocabulary.

*Suggested fix:* Rename the entry 'Q1-TARGET' throughout to match the scorecard and avoid collision with Tier 1.

### L6. `docs/Elimination_Ledger.md`

Casual/emphatic wording in results prose: 'Matched op identified at last' and 'The withdrawn 489× faster is obliterated — not faster, slower' (lines 361-364); vivid metaphors like 'the slag of the furnace' and 'the gold' are stylistic choices but sit uneasily in a governance ledger a newcomer must parse.

*Suggested fix:* Keep the metaphors if they are house style, but rephrase result sentences to neutral register ('the withdrawn 489× claim is contradicted by measurement').

### L7. `papers/ACS_Deterministic_AI_Stack_PDR.tex`

Phase 3 exit criterion (line 1369) contains an unresolved placeholder: 'sub-second latency for bracket operations below complexity bound C₁ (tbd)'.

*Suggested fix:* Define C₁ or mark the criterion explicitly as deferred to a later revision.

### L8. `papers/Form_Function_and_Asymmetry.tex`

Line 1328 cites '(cf. \emph{Spectral Witness Refinement} \S7.2; Elimination Ledger)' with no file path, footnote, or bibliography entry; the targets exist only elsewhere in the repo (papers/later_FF06_series/The_Elimination_Ledger.tex, docs/Elimination_Ledger.md), so a reader of the standalone paper cannot resolve the falsification claim.

*Suggested fix:* Add explicit citations or repo-relative pointers for Spectral Witness Refinement and the Elimination Ledger.

### L9. `papers/Form_Function_and_Asymmetry.tex`

Acknowledgements (lines 2170-2176) contain casual/personal wording for a research monograph: 'the KOBA42 Research Collective for inspiration', 'his family for tolerating 365 days of obsession', and 'Special thanks to the sleeping son who made it all matter.'

*Suggested fix:* Trim to a conventional acknowledgements register if the paper is intended for external review.

### L10. `papers/Form_Function_and_Asymmetry.tex`

The author block (line 60) gives \texttt{Form, Function, and Asymmetry} — the paper's own title in typewriter font — where an email or affiliation line normally goes; it reads as an unfilled placeholder.

*Suggested fix:* Replace with a contact address or delete the line.

### L11. `papers/core_trilogy/Holographic_Spectral_Inversion.tex`

Count mismatch in the unified-claims section: the text says 'All five domains (gauge theory, number theory, discrete geometry, renormalisation group, and quantum gravity)' and the table caption repeats 'All five domains', but the table itself lists six rows (adding Gravity as a separate domain from gauge theory).

*Suggested fix:* Say 'six domains' (or merge the gauge theory and gravity rows) so text, caption, and table agree.

### L12. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`

Lemma 3.3 (lem:torsion) proof says 'Torsion becomes non-zero in two ways' and then enumerates three items (a) spin sources, (b) geometric defects, (c) Poincare gauge gravity.

*Suggested fix:* Change 'two ways' to 'three ways' (or restructure (c) as a remark).

### L13. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`

Prediction P4 ends 'matches holographic resolution (D6)' - the label 'D6' is defined nowhere in the paper (it appears to be a definition number from an earlier draft or another document).

*Suggested fix:* Replace '(D6)' with a proper reference to the holographic-resolution definition in Paper C (def:holo).

### L14. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`

Duplicate bibliography entries: the Inversion Arc paper appears twice under two keys (\bibitem{Wallace2026c} at line ~3087 and \bibitem{WallaceC} at line ~3132), so the same work is cited as two different reference numbers in the rendered bibliography.

*Suggested fix:* Keep one key (e.g. Wallace2026c), delete the duplicate, and update the \cite{WallaceC} call sites.

### L15. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`

Casual/unprofessional wording in the Acknowledgements: 'the KOBA42 Research Collective for inspiration, and his family for tolerating 365 days of obsession. Special thanks to the sleeping son who made it all matter.' This register clashes with the technical tone and would draw attention in any formal submission.

*Suggested fix:* Trim to a conventional acknowledgement (tools, collaborators, family) and move personal dedications to a dedication line if desired.

### L16. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`

Cross-paper content bleed: the 'Computational limitations' subsection of Paper A discusses '100 Riemann zeros (Odlyzko tables)' and 'the Jacobi identity for the Wronskian bracket' - both Paper B subject matter with no role in Paper A's Palatini/gauge content - apparently copied from a shared addendum.

*Suggested fix:* Move the Riemann-zero and Wronskian limitations to Paper B's reproducibility section and keep only the Grassmannian-sampling limitation in Paper A.

### L17. `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`

Environment-type mismatch in references: 'Theorem~\ref{thm:sho}' is cited in the Open Problems and Discussion sections, but thm:sho labels a Remark ('Stripped-mode ODE'), so the text will read 'Theorem 5.3' while pointing at Remark 5.3.

*Suggested fix:* Either promote the stripped-mode result to a proposition or change the citing text to 'Remark~\ref{thm:sho}' (and rename the label rem:sho).

### L18. `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`

Stale scope heading: the Open Problems status block is headed 'Confirmed (real data, 100 Odlyzko zeros)' although several of the results listed under it were verified at N=200, N=19,900 pairs, or N=2,000,000 zeros per the paper's own Section 5.

*Suggested fix:* Reword the heading to 'Confirmed (real Odlyzko data)' and give per-item N.

### L19. `papers/core_trilogy/Spectral_Witness_Refinement.tex`

Author affiliation reads 'TensorRent --- geometry / state-field side' - internal project jargon ('state-field side' names one arm of an internal two-track workflow) presented as an institutional affiliation, unexplained to any outside reader.

*Suggested fix:* Use a standard affiliation ('Independent Researcher', matching the other three papers) and explain the two-track structure, if needed, in a footnote.

### L20. `papers/discrete_geometry_formalism.tex`

The filename says 'discrete_geometry_formalism' but the document's title is 'The ACS Deterministic AI Stack: A Dynamical Epistemic Algebra over Finite Rewrite Orbits', and the author field is the placeholder 'Formal Specification' with \date{\today}; the title also collides with ACS_Deterministic_AI_Stack_PDR.tex, inviting confusion between the two documents.

*Suggested fix:* Retitle (e.g. 'A Dynamical Epistemic Algebra over Finite Rewrite Orbits'), credit an author, and fix the date.

### L21. `papers/discrete_geometry_formalism.tex`

Phi is named the 'Observation Functor' (sec 1.3) even though the same document stresses 'the system lacks global functoriality' and that the operations 'do not form a strict category'; with no categories in play, 'functor' is unearned terminology by the paper's own de-sublimation standard.

*Suggested fix:* Rename to 'observation map' or 'observable projection'.

### L22. `papers/later_FF06_series/The_Elimination_Ledger.tex`

LaTeX double-hyphens used where single hyphens are intended, rendering as en dashes inside compound modifiers: 'highest--collapse claims', 'information--asymmetry / central--charge identity', 'conditional--uniformity height floor' (abstract, lines 28-34), and 'four--tier verification hierarchy' (line 38).

*Suggested fix:* Replace the double hyphens with single hyphens in these compounds (en dashes are for ranges, not hyphenation).

### L23. `papers/later_FF06_series/The_Elimination_Ledger.tex`

The Reproducibility appendix (line 484) says 'Verdicts and tiers are recorded in the append-only elimination ledger (The Elimination Ledger)' - a circular self-reference: the paper points to itself as the ledger artifact, and no separate append-only ledger file exists in the repository.

*Suggested fix:* Point to the actual ledger artifact (file path in the repo) or reword to make clear the paper is itself the ledger of record.

### L24. `papers/later_FF06_series/The_Geometry_Engine.tex`

The abstract claims the engine was benchmarked 'across ten ontologies of applied mathematics and computer science' (line 40), but the advantage-map table (lines 129-145) lists 11 task rows spanning only 9 distinct ontology labels (multiplicative functions, combinatorics, exact rationals, content addressing, generality, computer algebra, number theory, cryptography, prime generation). The count 'ten' matches neither.

*Suggested fix:* Reconcile the abstract's count with the table - either 'nine ontologies' / 'eleven tasks', or adjust the table's ontology labels.

### L25. `papers/later_FF06_series/The_Geometry_Engine.tex`

The Scope section (lines 271-272) lists retained falsified claims 'Mersenne-as-prime, single-deletion-as-primality, geometry-beats-division' that appear nowhere else in the paper or in the rest of the FF06 series files surveyed - dangling references with no statement of what the claims were or how they were killed, contrary to the program's own rule that negatives are recorded 'with the killing computation'.

*Suggested fix:* Add one line per claim (statement + killing mechanism), or cite the document where each is recorded.

### L26. `papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex`

The author block uses the paper's filename as an identifier line: '\small \texttt{The Reversible Flattening Process Record}' (line 33); One_Mechanism_Many_Forms_Sigma.tex does the same ('\texttt{One Mechanism Many Forms} (synthesis)', line 33). A typeset monospaced title-as-ID in the author block reads as leftover internal tooling metadata rather than a publication element.

*Suggested fix:* Remove the \texttt filename lines from the author blocks or move them to a footnote identifying the document key in the corpus index.

### L27. `papers/later_FF06_series/Three_Layer_Decomposition.tex`

Running heads are inconsistent: left head 'Three-Layer Decomposition of the Riemann Zeros' (hyphenated) vs right head 'Three Layer Decomposition' (unhyphenated) (lines 14-15); companion papers also cite it unhyphenated ('Three Layer Decomposition', The_Geometry_Engine.tex line 276).

*Suggested fix:* Standardize on 'Three-Layer Decomposition' in both running heads and in companion citations.

### L28. `papers/later_FF06_series/When_a_Number_Lies.tex`

Line 115 (and repeated in The_Reversible_Flattening_Monograph.tex line 301 and Process_Record line 195): the anchor list '$N\le 60,840,720720,2162160$ ($d=12,32,240,320$)' uses bare commas to separate list items inside math, which collide with thousands-separator reading - '840,720720' and '720720,2162160' are ambiguous at a glance.

*Suggested fix:* Typeset the anchors as a spaced list, e.g. $N \in \{60,\ 840,\ 720720,\ 2162160\}$, or use semicolons.

### L29. `papers/methodology/Form_Function_Relativity.tex`

In the same table (line 130) the arith witness's z-values are non-monotone along the refinement chain (259.9 vs Poisson, 832.2 vs GUE-marginal, 479.1 vs GUE-full); this does not violate Proposition 1 (whose hypothesis requires the witness to read only preserved structure), but the text never tells the reader why the monotonicity claim does not apply to that row.

*Suggested fix:* Add a sentence where the table is read (section 4) noting that Proposition 1 constrains only witnesses reading structure the finer frame preserves, so the arith row's z-values may fluctuate while its label stays FUNC.

### L30. `papers/methodology/Prime_Carrier_Position_Form_Factor.tex`

Line 42 references 'an internal strip-mine synthesis' and 'the "converse machine" of the analogous Fan-Wan lesson' — an internal private document and an unexplained allusion that a newcomer cannot resolve from the repo.

*Suggested fix:* Either cite the internal synthesis by an in-repo path (or drop the reference) and add one sentence explaining what the Fan-Wan lesson is or a citation for it.

### L31. `papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex`

Lines 209-211 and the footnote at lines 229-236 anchor the float suite's SHA-256 artefacts to a single private machine environment ('macOS-15.3.2-arm64-arm-64bit-Mach-O', Python 3.14.6, NumPy 2.5.0) with only same-machine byte-identical reruns; readers on any other platform cannot reproduce the anchored hashes, and the pipeline itself retains PASS_WITH_CAUTION for exactly this reason.

*Suggested fix:* Run the float suite on a second public platform (e.g. Linux CI) and record tolerance-based rather than byte-identical anchors for the float scripts, then lift the caution or document the residual drift.

### L32. `papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex`

Line 102 refers to 'the original "six agreeing witnesses"' in quotation marks, but that phrase is never introduced; the measured suite has five witnesses (table, lines 78-83) while section 1 (line 47) lists six statistics, so the five/six count switch is confusing.

*Suggested fix:* Either introduce the six-witness battery explicitly with a count in section 1 and explain which one is absent from the five-witness measurement suite, or change line 102 to 'the original battery of agreeing witnesses'.

### L33. `papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex`

The paper is cited throughout the repo as FF06e (e.g. Form_Function_Relativity.tex line 43, papers/README.md line 41) but never states its own series designation anywhere in the tex, so a newcomer reading it standalone cannot connect the 'FF06e' citations to this document.

*Suggested fix:* Add the FF06e designation to the title block or date line, matching the convention used by FF06g/FF06h and the TR-2026-FF06-I7 header.

### L34. `papers/notes/Adjoint_Clifford_Signature_Selection.tex`

Unbalanced parentheses in Table 2 Cartan-element entries (lines 532-537): '$(1/4)^4, -1)$', '$(1/3)^3, (-1/2)^2)$', '$(1/5)^5, -1)$', etc. are missing their opening parenthesis.

*Suggested fix:* Write '$((1/4)^4, -1)$' and similarly for the other tuple entries; also note the table declares 5 columns ({@{}lllll@{}}, line 525) but uses only 4.

### L35. `papers/notes/Adjoint_Clifford_Signature_Selection.tex`

The abstract switches notation without warning: the functional is defined with g throughout, but line 63 reads 'If $f(0) > 0$' — f is only introduced later in Proposition 2. Also line 557: 'no bifurcation to $\varepsilon = 2$' is unclear wording (presumably 'up to $\varepsilon = 2$').

*Suggested fix:* Use g consistently in the abstract (or introduce f there), and reword the perturbation-stability sentence.

### L36. `papers/notes/Critical_Line_As_Fibered_Object.tex`

Filename mismatch: the file is named Critical_Line_As_Fibered_Object.tex but the note's title and entire argument are 'The Critical Line Is a Seam, Not a Flattening' — 'fibered object' vocabulary appears nowhere in the text, so the filename reflects the superseded framing the note explicitly retracts.

*Suggested fix:* Rename to something like Critical_Line_As_Seam.tex (updating MANIFEST/links) or note the legacy filename in the header.

### L37. `papers/notes/Critical_Line_As_Fibered_Object.tex`

Casual wording in a research note: 'Reported as a negative, not spun' (line 254) and the unattributed 'cumulative folk tale' footnote (lines 229-231) describing the forced assembly order.

*Suggested fix:* Replace with neutral phrasing ('reported as an unresolved negative') and either name the folk-tale reference or drop the footnote.

### L38. `papers/notes/Density_Engine_Many_Worlds.tex`

Bibliography path problems: PalphaRefined2026 (lines 431-436) lists a stale root-level path 'flag_condensate_palpha_refined.tex' alongside the real papers/notes path; PalphaOverlap2026 (lines 438-442) cites 'flag_condensate_palpha_overlap.tex', which does not resolve (actual file is papers/notes/Flag_Condensate_Palpha_Overlap.tex), and that entry is never cited in the text.

*Suggested fix:* Point both entries at the canonical papers/notes/ paths only, and either cite PalphaOverlap2026 or delete the entry.

### L39. `papers/notes/Density_Engine_Many_Worlds.tex`

Pop-culture framing occupies a large share of the note's body: 'Fable karma tiers, Fallout faction reputation, quest flags' (line 221), RPG/DAW tables 2-3, and repeated gaming language in the main sections rather than the appendix. It is RC1-quarantined but its volume in the main text dilutes the two formal contributions (lane density definition, unification-table reading).

*Suggested fix:* Compress the RPG/Lisp analogy material into the existing DAW appendix, keeping one short RC1 remark in the main text.

### L40. `papers/notes/Flag_Condensate_Nuclear_Decay.tex`

Section heading 'Universal Geometric Unification' (line 222) overclaims relative to its own first paragraph, which immediately restricts the result to 'a unification of mechanism shape, not a claim that the four phenomena are physically identical'.

*Suggested fix:* Retitle to match the stated scope, e.g. 'Cross-Domain Structural Parallel' or 'Four-Domain Phase-Defect Pattern'.

### L41. `papers/notes/Flag_Condensate_Nuclear_Decay.tex`

Notation inconsistency: the deformed action is introduced as 'delta S(R, V_C)' (line 107) but written delta S(R) everywhere else in the note, including in the same sentence's displayed equation.

*Suggested fix:* Pick one signature for delta S and use it consistently.

### L42. `papers/notes/Flag_Condensate_Palpha_Overlap.tex`

Unexplained acronym: the recurring remark label 'RC1 scope' (line 81 here, and again in Flag_Condensate_Palpha_Throat_Overlap.tex line 77 and Flag_Condensate_Palpha_Refined.tex line 81) is never expanded or defined in any of the P_alpha notes; a newcomer cannot tell what RC1 stands for.

*Suggested fix:* Expand RC1 at first use (e.g. 'Release Candidate 1' or whatever it denotes) or link to where the term is defined in the repo.

### L43. `papers/notes/Flag_Condensate_Palpha_Refined.tex`

The extended DAW metaphor (Section 2, fig:daw-tracks) - master fader, clip automation, 'Dirichlet mute', 'Gamow send' - plus the disclaimer 'not a claim that alpha decay is literally audio production' reads as casual for a physics research note, and the metaphor vocabulary leaks into the technical Remark on boundary conditions ('routes a Gamow send into [R,b]').

*Suggested fix:* Keep the figure if useful but confine DAW vocabulary to the figure caption; state boundary conditions in standard terms in the body text.

### L44. `papers/notes/Flag_Condensate_Palpha_Refined.tex`

Redundant table row: in Table 2 (Acceptance comparison, lines 346-358) the 'Gamow outgoing' row is numerically identical to 'refined eigenmode' in every column with no annotation in the table itself; only the later Section 8 explains they coincide, so the table alone looks like a copy-paste error.

*Suggested fix:* Add a table footnote noting Channel C reproduces Channel B's metrics by construction under the E0 = Q_alpha protocol.

### L45. `papers/notes/Framing_Transformer_Spin_Parity.tex`

Scope statement contradicted later in the same note: Section 1 says 'Every number below is produced by code/framed_unknot/framing_transformer.py' (lines 75-77), but Section 6 numbers come from code/framed_unknot/moment_ratio.py and Section 7 from code/framed_unknot/one_object.py, as the note itself states.

*Suggested fix:* Amend the scope sentence to list all three scripts (all of which do exist in the repo).

### L46. `papers/notes/Framing_Transformer_Spin_Parity.tex`

Casual/unpolished phrasing in a formal note: 'the difference is $0.000\times10^{0}$ --- not small, but identically zero' (raw machine formatting left in prose, sec 7.1), and conversational lines such as 'This is what isotopy invariance looks like when you watch it' (sec 6.1) and the section title 'What survives, and it is worth keeping' (sec 6).

*Suggested fix:* Replace the machine-formatted number with 'identically zero (0 to machine precision)' and tone the conversational sentences to match the rest of the note's register.

### L47. `papers/notes/Klein_Foam_Monad.tex`

Bibliography entries Wheeler (line 305) and Finkelstein (line 325) are never cited anywhere in the text.

*Suggested fix:* Either cite them where relevant (e.g. geometrodynamics / causal-net lineage in sec 2) or remove them.

### L48. `papers/notes/Klein_Foam_Monad.tex`

'Shuman Resonance' deliberately preserves a misspelling of 'Schumann' (acknowledged at line 261: 'spelling preserves the programme name'), and section 5 characterises conscious beings as 'nitinol-like phase-slip loops'; even with the in-text disclaimers, this naming and the closing incantation ('The screw bores. The bubbles foam. ...', lines 295-296) will read as unserious to newcomers encountering the note cold.

*Suggested fix:* Add a footnote at first use explaining the Shuman/Schumann distinction is intentional, and consider moving the closing incantation into the already-existing 'Interpretive coda' appendix.

### L49. `papers/notes/Mobius_Screw_Electron.tex`

Stale date after revision: the note is dated July 22, 2026 (line 32) yet contains the 'Superseded ... falsified (T4)' Remark (lines 177-196) citing the Framing Transformer companion dated July 26, 2026 - the date was not updated when the post-falsification remark was added.

*Suggested fix:* Update the \date (or add a revision line, e.g. 'revised July 26, 2026') so the document date postdates the material it cites.

### L50. `papers/notes/Pythagorean_Lattice_Limits.tex`

Line break inside a hyphenated word (lines 205-206): 'independent group-\n theoretic reasons' will typeset as 'group- theoretic' with a spurious space.

*Suggested fix:* Add a trailing % after 'group-' or keep 'group-theoretic' on one line.

### L51. `papers/notes/Pythagorean_Lattice_Limits.tex`

Apparent inconsistency between Table 3's caption ('All z-scores fall in [-0.7, +0.3]', line 303-305) and the body text (lines 310-312) citing 'the largest absolute z-score is -0.71 ... at N = 7'. The table is at N = 5 and the text value at N = 7, but that distinction is not flagged, so the two statements read as contradictory.

*Suggested fix:* State explicitly that the caption range refers to N = 5 and that the -0.71 value is from the N = 7 run.
