# Specialist report — CPF §6's ultralight scalar against the observational bounds

STATUS: in progress

Wave-2 specialist. Mission: take the mass that CPF §6's quantum-pressure rotation-curve
mechanism *requires* and test it against published ultralight/fuzzy dark matter bounds.
The audit's existing result (`Constraint_Projection_Framework_Audit.tex`, §"(iii) The scale.")
is internal/structural (T2). This report attempts the escalation to T3 (measured against
external data) or T4 (falsified).

Instrument: `code/constraint_projection/fuzzy_dm_bounds.py`

## Tier conventions used here
- T0 machine-CHECKED, T1 machine (an instrument ran and printed it), T2 proved,
  T3 measured (against external data), T4 falsified. Tiers never promote.
- **Published bounds quoted below are CITED literature values (T3 data from others), not
  measurements made by me.** Every such number is tagged `[CITED]` with its source.
- Numbers computed by my instrument in this session are tagged `[T1 this run]`.

## Sections
1. Re-derivation of the mass §6 requires — **done**
2. Lyman-alpha forest bounds — (pending)
3. Dwarf spheroidal kinematics — (pending)
4. Black hole superradiance — (pending)
5. Honest synthesis — (pending)
6. What I did not do / assumptions not lifted — (pending)

---

## 1. Re-derivation of the mass §6 requires

Instrument: `code/constraint_projection/fuzzy_dm_bounds.py`, Section 1. Run this session.
Inputs from the audit's own fiducial: `v = 200 km/s`, `L = 1 kpc`. Constants: CODATA 2018,
IAU-2015 parsec. Nothing inherited from the audit; the audit's numbers are regenerated as a
cross-check, not copied.

### 1.1 The four set-ups

| route | relation | m (kg) | m (eV/c²) |
|---|---|---|---|
| (a) standard de Broglie | `λ = h/(mv) = L` | 1.0737e-58 | **6.0229e-23** |
| (b) reduced de Broglie | `ƛ = ħ/(mv) = L` | 1.7088e-59 | **9.5858e-24** |
| (c) soliton core, natural units | `r_c = (mv)⁻¹`, i.e. `ħ/(mv)` | 1.7088e-59 | 9.5858e-24 |
| (d) Schive+2014 core–halo, inverted | `r_c = 1.6 kpc (m/1e-22)⁻¹(M_h/1e9 M_⊙)^(-1/3)` | — | 1.600e-23 (MW-like, r_c=1 kpc) |

All `[T1 this run]` except the *functional form and coefficient* of (d), which is `[CITED]`
(Schive, Chiueh & Broadhurst 2014); the inversion arithmetic is mine.

### 1.2 Finding 1A — the mission's "soliton-core relation" is not an independent check

`r_c ~ (m v)⁻¹` in ħ=c=1 units restores to `r_c = ħ/(m v)`, which is **the same equation** as
route (b). The instrument asserts this (`|m_sol − m_red|/m_red < 1e-12`, passes). So the brief's
items "λ_dB = h/(mv)" and "the soliton-core relation r_c ~ (mv)⁻¹" are one constraint, not two.
The genuinely independent soliton route is (d), the empirical core–halo relation, and it is
reported separately above.

### 1.3 Finding 1B — the audit's `9.6e-24 eV` is the *reduced* de Broglie wavelength

`m_standard / m_reduced = 6.283185…`, asserted equal to 2π to 1e-9. The audit note
(`Constraint_Projection_Framework_Audit.tex`, §"(iii) The scale.") writes "the de Broglie
wavelength" and gives `1.7e-59 kg = 9.6e-24 eV`. That number is reproduced here by the
**reduced** convention `ƛ = ħ/(mv)` (1.7088e-59 kg, 9.5858e-24 eV), not by the standard
convention `λ = h/(mv)` (1.0737e-58 kg, 6.0229e-23 eV).

This is a naming convention, not an arithmetic slip, and the audit is internally consistent in
it — two further checks confirm the same convention is used throughout that paragraph:

- The audit's electron figure, `λ_dB = 5.8e-10 m`: reduced gives 5.788e-10 m ✓; standard gives
  3.637e-09 m ✗.
- The audit's "29 decades": `log10(kpc / 5.788e-10 m) = 28.73` ✓.

So the audit's paragraph is arithmetically sound under its own (unstated) convention. The
correction available is one of labelling: under the standard textbook definition of the
de Broglie wavelength the required mass is **6.0e-23 eV**, a factor 2π heavier than stated.
Recorded because the two numbers straddle the literature's quoted fuzzy-DM window
(1e-23 – 1e-22 eV) differently, and because §6's required mass is about to be compared against
published bounds where a factor 2π is not negligible.

**Both values are carried forward.** The bracket taken to data below is

    m_required ∈ [9.6e-24, 6.0e-23] eV/c²      (convention bracket, v=200 km/s, L=1 kpc)

and the manuscript's own stated `m ~ 1e-23 eV` (CPF L88) sits at the bottom of it.

### 1.4 Finding 1C — sensitivity is mild; this is a robust, not a fragile, requirement

`m = ħ/(vL)` is exactly inverse-linear in both inputs, so `dlog10(m)/dlog10(L) = −1` and
likewise for v. A factor 2 in L moves the mass **0.30 decades**, not two. Over the full grid
`L ∈ [0.5, 10] kpc × v ∈ [100, 300] km/s` the mass spans

    6.391e-25 … 3.834e-23 eV      (1.78 decades)  [T1 this run]

The instrument asserts this span is under 2 decades (passes). Consequence for the mission: §6's
requirement is **not** the kind of claim that can be rescued by a factor-2 argument about what
"galactic scale" means. To lift the required mass by a decade you must shrink L by a decade, to
100 pc — below the scale on which flat rotation curves are the phenomenon being explained.

