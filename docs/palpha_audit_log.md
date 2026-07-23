# Pα Overlap Audit Log

**UTC:** 2026-07-23  
**Scope (RC1):** JSON canonical (script output); TeX tables rounded to 4 significant decimals. Model claims only — no uniqueness proofs.

## Summary

| Check | Result |
|-------|--------|
| Baseline `palpha_overlap_results.json` vs `flag_condensate_palpha_overlap.tex` | **PASS** |
| Throat `palpha_overlap_throat_results.json` vs `flag_condensate_palpha_throat_overlap.tex` | **PASS** |
| Refined `palpha_overlap_refined_results.json` vs `flag_condensate_palpha_refined.tex` | **PASS** |
| ACS copies under `acs-framework-public/papers/notes/` vs JSON | **PASS** (same rounded values) |
| Per-isotope table spot checks (212Po, 244Cm) | **PASS** |
| `log10 P_ext` vs `t_Gamow/t_meas` on base 14 | **PASS** (|Δ| ≤ 0.005) |

**Overall reality check: PASS**

## Summary statistics (JSON → TeX tolerance ±0.0002)

| Metric | JSON | TeX | Status |
|--------|------|-----|--------|
| Baseline ⟨log10 P⟩ | −0.390487 | −0.3905 | PASS |
| Baseline Pearson r | +0.888210 | +0.8882 | PASS |
| Baseline RMS raw | 1.770480 | 1.7705 | PASS |
| Baseline RMS(global S) | 0.822015 | 0.8220 | PASS |
| Throat ⟨log10 P⟩ | −0.460707 | −0.4607 | PASS |
| Throat Pearson r | +0.887549 | +0.8875 | PASS |
| Throat RMS(global S) | 0.824694 | 0.8247 | PASS |
| Eigenmode Pearson r | +0.967629 | +0.9676 | PASS |
| Eigenmode RMS(global S) | 0.825739 | 0.8257 | PASS |
| LOO S(A,Z) | 0.286229 | 0.2862 | PASS |
| LOO S(R) | 0.469502 | 0.4695 | PASS |

## Channel C (Gamow outgoing) — post-audit extension

| Metric | Dirichlet eigenmode | Gamow outgoing [0,b] | Δ |
|--------|--------------------:|---------------------:|--:|
| Pearson r | +0.967629 | +0.967616 | −0.00001 |
| RMS(global S) | 0.825739 | 0.825730 | −0.000009 |

Gamow Robin BC on [0,b] does **not** improve global-S RMS vs Dirichlet box at R on the stated 14-isotope set (as implemented).

## Extended catalog (29 isotopes)

- Base 14: Nuclear Decay table (canonical).
- +15 from NNDC/NuDat Q and t1/2; R,b,W computed (`isotope_catalog.py`).
- LOO S(A,Z): 0.286 (n=14) → 1.355 (n=29) — parametric fit **degrades** on extended set (expected under mixed extraction protocols).
- Coefficient signs b1>0, b2<0, c1<0 **preserved**; magnitudes shift.

## Artifacts

- Scripts: `code/palpha_overlap/palpha_overlap*.py`, `isotope_catalog.py`
- JSON: `docs/palpha_overlap_*_results.json`, `palpha_overlap_extended_results.json`
- Papers: `flag_condensate_palpha_*.tex` (+ ACS `papers/notes/` copies)
