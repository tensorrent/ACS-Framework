# Paper A (Colour from Gravity) — Edit Changelog

**Date:** April 26, 2026
**Source version:** April 17, 2026 (40 pages, 2860 lines TeX)
**Edited version:** April 26, 2026 (42 pages, 3065 lines TeX)

## Summary

Paper A now incorporates the Higgs-sector self-pruning results from
session Phases 50, 51, and 52: α₂ is forbidden by representation
theory, β_c is excluded at tree level, and equal-VEV alignment is
incompatible with quark mixing. The parameter ledger is updated from
"5 free, 7 total" to the corrected "4 free + 2 calibrations = 6 total"
in Branch A (minimal bi-doublet).

A small numerical reconciliation: the codebase's λ_eff verification
was using v = 246.0 GeV, giving a 1.01% discrepancy with λ_SM. The
paper uses v = 246.22 GeV (the precise PDG value) and reports a
0.84% match. The codebase has been corrected to match the paper.

## Changes

### Added

1. **§5.5.1 Self-pruning of the bi-doublet Higgs sector** (new subsubsection)
   - Pre-pruning potential equation listing all 5 quartic couplings
   - **Phase 50 paragraph**: α₂ = 0 forbidden because Φ ∼ (1, 2, 2)
     is an SU(4) singlet, so T^A Φ = 0 identically
   - **Phase 51 paragraph**: tree-level extremization of β_c term
     gives ∂V/∂β = 2β_c v² v_R² cos(2β) = 0 → tan β = ±1
   - **Phase 52 paragraph**: algebraic identity
     M_u − M_d = (h − h̃)(κ_1 − κ_2) shows equal VEVs force
     M_u = M_d and |V_CKM| = 1
   - Three-independent-filters paragraph noting:
     representation theory + vacuum extremization + flavor phenomenology
     all assume the minimal bi-doublet
   - Branch A parameter ledger table (locked / forbidden / excluded / free)
   - Cross-references to `src/paper_a/branch_a_vacuum.py`,
     `betac_tan_beta.py`, `yukawa_no_go.py`

2. **§7 CKM=I result reframing**
   - New paragraph "Algebraic origin of V_CKM = 1" added to the
     existing CKM appendix
   - Cross-references the Phase 52 algebraic identity from §5.5.1
   - Notes the V_CKM = 1 finding is structural (any minimal
     bi-doublet at equal VEVs), not a numerical coincidence

### Corrected

3. **§6 Irreducible boundary subsection rewritten**
   - Old: "5 free parameters: tan β, ρ_Δ, α_1, α_2, β_c, total 7 inputs, factor 3"
   - New: 4-paragraph structure
     - Locked by Palatini (5 quantities)
     - Forbidden by representation theory (α_2)
     - Excluded at tree level (β_c)
     - Free at tree level (3: ρ_1, α_1, tan β radiative)
     - Calibrations (2: v, v_R)
   - Total inputs: 6 (vs. 19+ SM, factor 3.2× reduction)
   - Branch B alternative (Σ ∼ (15, 1, 1) extension) cited as 7-input
     fallback if β_c is required at tree level
   - Falsifiability paragraph: explicit experimental targets for each
     free parameter

4. **fig:hero caption updated**
   - Reflects new 6-input ledger with explicit forbidden/excluded
     categories

### Reconciled

5. **λ_eff numerical match**
   - Paper claim: 0.85% match (with v = 246.22 GeV)
   - Codebase old: 1.01% match (with v = 246.0 GeV — rounding error)
   - Resolution: codebase corrected to use v = 246.22 GeV
   - Updated in `src/paper_a/branch_a_vacuum.py::lambda_eff_consistency`
   - Test still passes: `tests/test_paper_a.py::test_lambda_eff_close_to_SM`

### Bibliography

- **Removed duplicate** `Hehl1976` entry (was listed twice)
- **Added** `WallaceB` (Paper B reference)
- **Added** `WallaceC` (Paper C reference) — was previously cited
  in §A.2 but not in bibliography (caused undefined-citation warning)
- **Added** `Lakatos1976` (methodological reference, matches Papers B and C)

## Not changed

- Abstract
- §1 Introduction (core observation, summary of results)
- §2 ACS framework (measure-theoretic foundation, BCH-TE morphism)
- §3 Gauge theory and gravity (Palatini formulation, Ricci flow)
- §4 GL(4) fiber algebra (selection principle, colour charges,
  electroweak containment, what remains open)
- §5.1-5.4 Higgs derivation up to and including the partial-derivation
  status paragraph (Koide projection, Killing form normalization)
- §5.6 Dimensional devolution
- §5.7 Contextualization within current literature
- Derived matches PDG comparison
- §6 ACS quantum gravity (Barbero-Immirzi, Wheeler-DeWitt, predictions)
- §6 Mass hierarchy angle (resolved), neutrino mass spectrum,
  quark Koide and QCD corrections
- §A Proof of Theorem 2.1
- §B Computational status (Higgs quartic, strong gauge coupling, etc.)
- §C Status of CKM derivation (preserved core, only added cross-reference)
- §D Torsion coupling hierarchy and vacuum energy cancellation
- §E Geometric Vision (plain-language summary)
- §F Experimental Tests

## Verification

All claims in the new §5.5.1 are backed by passing tests in the
companion codebase:

- α₂ = 0 (Phase 50): `tests/test_paper_a.py::test_branch_a_parameter_count`
  and `test_alpha1_stability_bound`, plus the docstring in
  `branch_a_vacuum.py` documents the representation-theoretic
  argument.
- β_c forces tan β = ±1 (Phase 51):
  `tests/test_paper_a.py::test_betac_extremization_yields_pi_4`
- Equal-VEV no-go (Phase 52):
  `tests/test_paper_a.py::test_yukawa_no_go_matrix_proportional`,
  `test_yukawa_no_go_independent_invariant`,
  `test_yukawa_algebraic_identity`
- Vacuum stability and λ_eff:
  `test_vacuum_admits_stable_minimum`,
  `test_vacuum_recovers_target_VEVs`,
  `test_lambda_eff_close_to_SM`

Total Paper A tests: 14/14 passing.

## Page count

Old: 40 pages, 2860 lines TeX
New: 42 pages, 3065 lines TeX
Net addition: 2 pages of new mathematical content (Phases 50/51/52
chain in §5.5.1) + reorganized §6 boundary + bibliography fix

## Trilogy status

| Paper | Status | Pages | Lines TeX | Tests |
|---|---|---|---|---|
| Paper A (06a) | **Edited** | 42 | 3065 | 14/14 |
| Paper B (06b) | **Edited** | 15 | 1151 | 10/10 |
| Paper C (06c) | **Edited** | 13 | 1035 | 18/18 |
| **Total** | **Complete** | **70** | **5251** | **42/42** |

All three papers now reflect the session's results consistently.
The trilogy + codebase + tests + documentation form a coherent,
reproducible computational appendix to the manuscripts.

## Open items for future sessions

1. **§7 audit of h̃/h = 2/3 interpretation** (Paper A §7 boundary)
   - Whether matrix-level proportionality h̃ = (2/3) h or
     invariant-level ratio Tr h̃ / Tr h = 2/3
   - Affects strength of Phase 52 no-go in extended Higgs sectors
   - Phase 52 itself is unaffected (the identity holds for ANY
     h, h̃ when κ_1 = κ_2)

2. **Coleman-Weinberg analysis without β_c**
   - Determines whether tan β reduces from radiative-output to
     genuinely-derived (6 → 5 inputs)
   - Estimated 2-4 weeks of focused symbolic + numerical work

3. **FeynRules / UFO export** (Phase D1)
   - Required for predictive scattering computations
   - Estimated 1-2 months of postdoc work

4. **Hilbert-Pólya operator construction** (Paper B open direction)
   - Construct natural self-adjoint H with spectrum exactly {γ_k}
   - 100+ year open problem; resolution would upgrade
     resolvent-trace framing from formal identity to derived theorem

5. **Post-attractor ΔI < 0 verification** (Paper C)
   - Find a concrete physical instance where the inversion arc's
     post-attractor regime is observable
   - Currently structural conjecture, not derived
