# Paper C (The Inversion Arc) — Edit Changelog

**Date:** April 25, 2026
**Source version:** April 17, 2026 (10 pages, 734 lines TeX)
**Edited version:** April 25, 2026 (13 pages, 1035 lines TeX)

## Summary

Paper C now incorporates the algebraic foundations developed in
session Phases 48-55: the Killing-orthogonality theorem, the three-class
spectral taxonomy, and the algebraic non-traversability rereading of
ER=EPR. The parameter ledger has been updated from "5 free" to the
correct "4 free + 2 calibrations = 6 inputs" Branch A status.

## Changes

### Added

1. **§3.1 Methodological note on epistemic compression**
   - New subsection in Introduction
   - References Lakatos's *Proofs and Refutations* (1976)
   - Distinguishes proved theorems / open conjectures / disproved
     hypotheses retained as model-space boundaries

2. **§4 Algebraic Foundations of the Inversion Arc** (entire new section)

   - **§4.1 The Killing-orthogonality theorem**
     - Theorem 4.1: tr([X,Y]·X) = 0 for any matrix Lie algebra
     - Proof via trace cyclicity (3 lines)
     - Chirality hopping example: [H_1, A_01] = 2 S_01 in sl(4,R)
     - Three ambiguity numbers in sl(4,R):
       - Passive (B^perp): dim = 14
       - Generic Jacobian kernel: 15
       - Degenerate kernel at (H_1, A_01): 19
     - Cross-references to `src/paper_c/killing_orthogonality.py`
       and `src/paper_c/orthogonal_complement_probe.py`

   - **§4.2 Three-class spectral taxonomy**
     - Theorem 4.2: Jordan-Chevalley → elliptic / hyperbolic / parabolic
     - Table of four ACS instances classified by spectral type
     - Remark explicitly noting and correcting the earlier
       universal-2π overclaim
     - Cross-reference to `src/paper_c/spectral_taxonomy.py`

   - **§4.3 Algebraic non-traversability (ER=EPR rereading)**
     - Proposition 4.3: π_X([X,Y]) = 0 identically (the algebraic
       content of "non-traversable")
     - Two-line proof from Theorem 4.1
     - Remark flagging the AdS/CFT correspondence as a research
       direction, not a derived consequence
     - Cross-reference to `src/paper_c/er_epr_algebraic.py`

### Corrected

3. **§6 (formerly §5) Gaps revealed by formalisation, item (9)**
   "Corrections from the exploration session" expanded to include:
   - α_2 forbidden by representation theory (T^A Φ = 0 for (1,2,2))
   - β_c excluded at tree level (else V_CKM = I from no-go identity)
   - The no-go identity M_u - M_d = (h - h̃)(κ_1 - κ_2) explicitly stated

4. **§6 (formerly §5) Gaps revealed by formalisation, item (10)**
   - Old: "5 free parameters, total 7 inputs"
   - New: "6 inputs in Branch A (minimal bi-doublet)" with full breakdown:
     - 5 locked by Palatini
     - 1 forbidden (α_2)
     - 1 tree-level excluded (β_c)
     - 2 free (ρ_1, α_1)
     - 1 radiative (tan β)
     - 2 calibrations (v, v_R)
   - Reduction factor 19+ / 6 ≈ 3.2× explicitly noted
   - Coleman-Weinberg uncertainty for tan β explicitly flagged

5. **§6 new item (11): Three-layer self-pruning**
   Notes that the Higgs sector reduction operates through three
   independent consistency filters (representation theory, vacuum
   extremization, flavor phenomenology) — within the minimal
   bi-doublet assumption.

### Bibliography additions

- Jacobson 1979, *Lie Algebras*
- Bourbaki 1989, *Lie Groups and Lie Algebras*
- Maldacena & Susskind 2013, ER=EPR conjecture
- Ryu & Takayanagi 2006, Holographic entanglement entropy
- Lakatos 1976, *Proofs and Refutations*

## Not changed

- Tensegrity-gauge correspondence (§2)
- Holographic resolution definitions HR-1 through HR-3 (§3)
- Inversion theorem (Theorem 3.4, originally 4.1) — proof unchanged
- Constraint-attractor cycle (§3.4)
- Unified domains table (§6.1)
- Standard Model conjecture (Conjecture 6.2)
- Geometric fermions conjecture (Conjecture 6.3)
- c-theorem / a-theorem citations (Theorem 6.4)
- Banach-Tarski appendix
- Newton/Russell historical precursors appendix

## Verification

All claims in the new §4 are backed by passing tests in the
companion codebase (`acs_codebase`):

- Theorem 4.1: `tests/test_paper_c.py::test_killing_orthogonality_*`
  (6 tests, including symbolic SymPy identity and 1000-trial
  scaling in sl(3,R) and sl(4,R))
- Theorem 4.2: `tests/test_paper_c.py::test_*_elliptic|hyperbolic`
  (5 tests across SU(2), Frenet-Serret, sl(4,R), core rope)
- Proposition 4.3: `tests/test_paper_c.py::test_direct_projection_returns_zero`

Total Paper C tests: 18 / 18 passing.

## Page count

Old: 10 pages
New: 13 pages
Net addition: 3 pages of mathematical content + revised parameter ledger

## What remains for next session

- Paper A edits (Phases 50-52 chain into the existing Higgs section,
  parameter ledger update, λ = 0.85% vs 1.01% reconciliation)
- Paper B edits (resolvent reframing of §6, Wronskian Leibniz failure,
  renormalized stability frame as von Koch 1901 in log coordinates)
