# ACS Framework — Master Document Index

**Date:** May 3, 2026
**Status:** All documents final, all cross-references resolved, all compilations clean.

---

## Core Trilogy

| Document | Title | Pages | Lines | Status |
|---|---|---|---|---|
| **TR-2026-FF06a** | Colour from Gravity: Pati-Salam from Palatini Bracket | 44 | 3142 | Final |
| **TR-2026-FF06b** | Information Asymmetry and the Riemann Spectral ACS | 15 | 1151 | Final |
| **TR-2026-FF06c** | The Inversion Arc: Holographic Resolution in ACS | 13 | 1056 | Final |

**Trilogy total: 72 pages, 5349 lines TeX**

## Companion Notes

| Document | Title | Pages | Lines | Status |
|---|---|---|---|---|
| **TR-2026-FF06-N1** | Pythagorean Arithmetic Structure in Minimal PS | 5 | 384 | Final |
| **TR-2026-FF06-N2** | Metric Signature as Minimiser of Adjoint Spectral Activity | 8 | 682 | Final |

**Notes total: 13 pages, 1066 lines TeX**

## Reproducible Code

| File | Purpose | Tests |
|---|---|---|
| `acs_codebase.tar.gz` | Trilogy verification (42 tests) | 42/42 |
| `test_lattice_imprint.py` | N1 IR null test (PDG masses) | Verified |
| `test_signature_selection.py` | N2 verification (4 test blocks) | 4/4 |
| OmniForge `verify_tr2026_ff06.py` | CI pipeline (FF06 + N2) | 32/32 |

## Supporting Documents

| File | Purpose |
|---|---|
| `ACS_CS_Applications.md` | 10 CS use cases with logic schemas |
| `PaperA_changelog.md` | Paper A edit log |
| `PaperB_changelog.md` | Paper B edit log |
| `PaperC_changelog.md` | Paper C edit log |
| `Music_Thread_Closure_Summary.md` | Music-thread compression record |
| `Trilogy_Edit_Summary.md` | Overall edit summary |

---

## Cross-Reference Network

```
Paper A ──cites──→ Paper B (WallaceB)
Paper A ──cites──→ Paper C (WallaceC)
Paper A ──cites──→ N1 (WallaceN1)
Paper A ──cites──→ N2 (WallaceN2)
Paper B ──cites──→ Paper A (Wallace2026a)
Paper C ──cites──→ Paper A (Wallace2026a)
Paper C ──cites──→ Paper B (Wallace2026b)
Paper C ──cites──→ N2 (WallaceN2)
N1 ──cites──→ Paper A (WallaceA)
N2 ──cites──→ Paper A (WallaceA)
N2 ──cites──→ N1 (WallaceN1)
```

All citations resolved: 0 undefined references across all 5 documents.

---

## What Each Document Contains

### Paper A (Colour from Gravity) — 44 pages
- Palatini bracket [e,ω] on sl(4,R) → SU(3) closure attractor
- BCH expansion → Higgs (order 1), gauge bosons (order 2), generations (order 3)
- Higgs quartic λ_φ = 2√3/27 (0.84% match to SM)
- Yukawa ratio h̃/h = 2/3 from Koide projection
- **Phases 50-52**: α₂ forbidden, β_c excluded, M_u = M_d no-go
- **6-input Branch A ledger** (was 5 free / 7 total; now 4 free / 2 calibrations)
- Barbero-Immirzi γ = 0.274 from information balance
- Wheeler-DeWitt as ACS quantum attractor
- **Arithmetic lattice remark** (⟨2,3⟩ structure, cites N1)
- **Signature selection remark** (adjoint spectral minimisation, cites N2)

### Paper B (Riemann Spectral ACS) — 15 pages
- F_N(x) stationarity ↔ RH
- Wronskian as Lie bracket (Proposition 2.2)
- **Wronskian Leibniz failure** (Remark 2.3: not Poisson, correction −fgh')
- **Resolvent susceptibility** (§2.5: χ(ω) = Tr[(ωI−H)⁻¹])
- **Renormalized stability** (§2.6: von Koch 1901 in log coordinates)
- Variance scaling, Wronskian non-vanishing
- Tensor flow / center manifold
- **Open Problems restructured** with Disproved section

### Paper C (Inversion Arc) — 13 pages
- Tensegrity-gauge correspondence
- Holographic resolution (HR-1 through HR-3)
- Constraint-attractor cycle
- **Killing-orthogonality theorem** (Theorem 4.1)
- **Three-class spectral taxonomy** (Theorem 4.2, corrected from 4-class)
- **Signature selection cross-reference** (Remark after Theorem 4.2)
- **Algebraic non-traversability** (Proposition 4.3, ER=EPR rereading)
- Updated parameter ledger (6 inputs, three-layer self-pruning)

### N1 (Pythagorean Structure) — 5 pages
- ⟨2,3⟩ lattice membership of all PS native ratios
- Comparison with SU(5) (⟨2,3,5⟩) and SO(10)
- **IR null test**: PDG masses show no lattice imprint (z ∈ [-0.7, +0.3])
- Classification: UV algebraic artifact, not phenomenological prediction

### N2 (Signature Selection) — 8 pages
- **Lemma**: index-partition → parity map (with O(n) reduction)
- **Theorem**: binary-split signature selection (6-step proof)
- Reduction to max-cut on complete bipartite graph
- Functional universality (6 functionals)
- Frame invariance (50/50 O(4))
- Generator dependence (9 Cartan elements, sl(3)–sl(6))
- Cross-type observation (A, B, C, D types; compact vs noncompact)
- Perturbation stability (eigenvalue-crossing transitions)
- **Full combinatorial proof** (not sketch)

---

## What's Proved vs What's Open

### Proved (theorem-level, with proof)
1. SU(3) as closure attractor of Palatini bracket (Paper A)
2. λ_φ = 2√3/27 from Koide projection (Paper A)
3. α₂ = 0 by representation theory (Paper A §5.5.1)
4. β_c = 0 at tree level → V_CKM = I no-go (Paper A §5.5.1)
5. Killing-orthogonality tr([X,Y]·X) = 0 (Paper C Theorem 4.1)
6. Three-class spectral taxonomy (Paper C Theorem 4.2)
7. Wronskian is Lie bracket but not Poisson (Paper B Remark 2.3)
8. RH ⇒ stationarity of F_N (Paper B)
9. Renormalized stability under RH (Paper B Theorem 2.4)
10. **Signature selection from adjoint spectral activity (N2 Theorem 1)**

### Numerically verified (not yet theorem-level)
11. Compact → Euclidean, noncompact → nontrivial (N2 Observation)
12. ⟨2,3⟩ lattice membership of PS ratios (N1)
13. IR null test for lattice imprint (N1 §4)
14. 72% parity-odd holonomy under Lorentzian grading (Type IIb)

### Explicitly open (flagged in papers)
15. Coleman-Weinberg analysis (6 → 5 inputs?)
16. FeynRules/UFO export
17. Hilbert-Pólya operator construction
18. Multi-cluster weighted proof (N2 Theorem 1(iii))
19. Extension to exceptional algebras (N2)
20. Action principle that produces S_f (Route B completion)

### Explicitly disproved (negative results retained as boundaries)
21. ad³ = 2·ad for integer matrices (impossible: requires λ = 1/√2)
22. Universal 2π inversion at three steps (sl(4) is hyperbolic)
23. Wronskian as Poisson bracket (Leibniz fails by −fgh')
24. IR lattice imprint of ⟨2,3⟩ structure (z-scores null)
25. Intrinsic algebra chirality (Type I from algebra alone — ruled out)
26. Signature selection from Killing form (Route A — closed)
27. Signature selection from stability (Route C — closed)

---

## Recommended Submission Order

1. **N2 (Signature Selection)** — standalone, highest novelty, smallest attack surface
2. **Paper A** — the main paper, references everything else
3. **Paper C** — algebraic foundations, supports Paper A
4. **Paper B** — most independent, can go separately
5. **N1** — short note, cite from Paper A

N2 first because it's the session's strongest result and stands alone.
Paper A last because it's the most complex and benefits from the
companion notes being available as cited references.

---

## Grand Total

| Category | Documents | Pages | Lines TeX | Tests |
|---|---|---|---|---|
| Trilogy | 3 | 72 | 5349 | 42/42 |
| Notes | 2 | 13 | 1066 | 19/19 |
| CI pipeline | — | — | — | 32/32 |
| **Total** | **5** | **85** | **6415** | **all passing** |
