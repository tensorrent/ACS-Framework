> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Papers

Manuscripts and companion notes. LaTeX sources are canonical; compiled PDFs are
committed alongside them where available. Claim tiers and the claim-to-code
mapping live in [`../MANIFEST.md`](../MANIFEST.md), not here.

## `core_trilogy/` — the foundational papers

| Role | File | Subject |
|------|------|---------|
| A | `Palatini_Gauge_Attractor.tex` | SU(3) as a closure attractor in the Palatini bracket |
| B | `Riemann_Spectral_Critical_Line.tex` | Spectral positional duality; deepest form |
| B′ | `Spectral_Witness_Refinement.tex` | Retitled, tightened witness-survival variant |
| C | `Holographic_Spectral_Inversion.tex` | Holographic resolution / ER=EPR algebraic |

Shared figures are in `core_trilogy/figures/`; `figures/` at this level holds the
subset used by the root monograph.

## `notes/` — companion notes

| Role | File | Subject |
|------|------|---------|
| N1 | `Pythagorean_Lattice_Limits.tex` | Pythagorean structure in the minimal PS algebra |
| N2 | `Adjoint_Clifford_Signature_Selection.tex` | Grading selection from adjoint spectral activity |
| N3 | `Prime_Gap_Transition_Operator.tex` | Prime-gap transition operator on (ℤ/mℤ)* |
| — | `Mobius_Screw_Electron.tex` | Framed-unknot electron model (Flag Condensate) |
| — | `Framing_Transformer_Spin_Parity.tex` | SU(2) lift of that frame loop; parity law; T4 kill |
| — | `Mobius_Ribbon_Capacitance.tex` | Annulus / conformal-modulus / BIE revisions of α |
| — | `Klein_Foam_Monad.tex` | Klein-foam Monad postulation (ontology) |
| — | `Flag_Condensate_Nuclear_Decay.tex` | Phase-slip / Bogoliubov Gamow channel |
| — | `Flag_Condensate_Palpha_{Overlap,Refined,Throat_Overlap}.tex` | Pα overlap trilogy |
| — | `Density_Engine_Many_Worlds.tex` | Density Engine interpretive note |
| — | `Critical_Line_As_Fibered_Object.tex` | The critical line as a two-sided seam (Fork C synthesis) |

## `methodology/` — empirical tools

| Role | File |
|------|------|
| FF06e | `Spectral_Rigidity_Shuffle_Knife.tex` |
| FF06f | `Prime_Carrier_Position_Form_Factor.tex` |
| **FF06g-M** | `Form_Function_Relativity.tex` |
| **FF06h-M** | `Scaled_Invariance_of_Infinity_and_Zero.tex` |
| I7 | `Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex` |

## `later_FF06_series/` — chronological research thread

| Role | File |
|------|------|
| **FF06g-L** | `The_Geometry_Engine.tex` |
| **FF06h-L** | `When_a_Number_Lies.tex` |
| FF06i | `The_Reversible_Flattening.tex` |
| FF06J | `The_Reversible_Flattening_Monograph.tex` |
| FF06K | `The_Reversible_Flattening_Process_Record.tex` |
| K1 | `The_Elimination_Ledger.tex` |
| Σ | `One_Mechanism_Many_Forms_Sigma.tex` |
| — | `Three_Layer_Decomposition.tex` |

The four `*_disp.py` files here are display copies of engine code used in that
thread; the verification code proper lives under [`../code/`](../code).

### ⚠️ The FF06 g/h collision — read before citing by letter

Two independent lettering schemes grew in parallel, and **the bare labels
`FF06g` and `FF06h` each name two different papers**:

| Bare label | In `methodology/` | In `later_FF06_series/` |
|---|---|---|
| `FF06g` | Form/Function Relativity | The Geometry Engine |
| `FF06h` | Scaled Invariance of ∞ and 0 | When a Number Lies |

Both schemes are entrenched in existing documents, so neither is being
retired. Instead, **use the suffixed forms**: `-M` for the `methodology/`
paper, `-L` for the `later_FF06_series/` paper. A bare `FF06g` or `FF06h`
should be read as ambiguous and resolved by looking at the surrounding
subtree. Unsuffixed letters elsewhere in the series (e, f, i, J, K, K1, Σ)
are unambiguous and need no qualifier.

A second, resolved case: `FF06f` designates
`methodology/Prime_Carrier_Position_Form_Factor.tex`. Some older text used it
loosely for the three-layer decomposition, which is the separate
`later_FF06_series/Three_Layer_Decomposition.tex`.

## Root-level

- `Form_Function_and_Asymmetry.tex` — consolidated core monograph
- `ACS_Deterministic_AI_Stack_PDR.tex` — Paper D, Deterministic AI Stack blueprint
- `discrete_geometry_formalism.tex` — Dynamical Epistemic Algebra formalization

## Conventions

- `.md` mirrors accompany the recent Flag Condensate notes for readability; the
  `.tex` is authoritative where the two differ.
- Artifact paths cited inside papers are repo-relative. Where a run log or
  results file was not committed, the paper says so rather than citing a path
  that does not resolve.
