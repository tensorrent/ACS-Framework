> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Paper B (Riemann Spectral ACS) — Extension Changelog

**From**: v2M (17 pages, May 2026)
**To**: extended (26 pages, May 2026)
**Status**: Compiled, integrated, presented as new artifact

---

## What changed

### Abstract (expanded)

Original abstract covered:
- ACS framework applied to RH
- Stationarity ⇔ RH conjecture
- 2M-zero variance stationarity
- Off-line scaling α = 2σ−1
- Cross-correlation |C_N| ~ N^(-0.95)
- Wronskian non-vanishing on 1225 pairs
- Tensor flow center-manifold

Added to abstract:
- Tartini-tone characterization: R₂ at N=5K, R₃ at N=50K (RMSE 0.051), Fourier-dual peaks at log(p^k) within 5×10⁻⁵ mean distance (including 2⁶ = 64 prime power)
- L-function generalization: χ₄ recovery (19/19 = 100% accuracy), Dirichlet's theorem decomposition (15/15 each direction), Dedekind ζ_K(ℚ(i)) prime-ideal structure (5.7× ratio)
- Hilbert-Pólya constraint specification: GUE necessary but not sufficient, 40× distinction by Fourier-dual alignment

### Three new sections (~9 pages of new material)

**§8 — Tartini-Tone Characterization of the Spectrum** (formerly absent)

- §8.1 Order-2: Montgomery's pair correlation R₂ at N=5K
- §8.2 Order-3: Rudnick-Sarnak R₃ at N=50K (RMSE 0.051, correlation 0.99)
- §8.3 Fourier-dual: explicit-formula peak structure (top 20 peaks within 1.8×10⁻⁴ of prime powers, including 2⁶ = 64)
- §8.4 Synthesis: internal rigidity (R₂, R₃) + external coupling (F(ω) peaks) = complete Tartini-tone fingerprint

Theoretical content:
- Equation for R₂ (Montgomery)
- Equation for R₃ (Rudnick-Sarnak GUE form)
- Equation for F_N(ω) and the explicit formula
- Statement that prime-zero coupling is Fourier-dual, not resonant

**§9 — L-Function Generalisation** (formerly absent)

- §9.1 Dirichlet L(s, χ₄): 100% sign accuracy on 19 peaks recovers χ₄
- §9.2 Cross-correlation Dirichlet's theorem: F_ζ ± F_L decomposes primes by residue class
- §9.3 Dedekind zeta of ℚ(i): split/inert prime-ideal structure recovered
- §9.4 Status: framework's universality empirically confirmed at three L-function classes

Theoretical content:
- Explicit formula for L(s, χ) with character
- Algebraic decomposition F_ζ ± F_L → primes ≡ ±1 mod 4
- Dedekind zeta factorization ζ_K = ζ × L for ℚ(i)
- Prime-ideal norm structure: ramified, split, inert

**§10 — Hilbert-Pólya Constraint Specification** (formerly absent)

- §10.1 The constraints C1–C9 as a precise specification
- §10.2 GUE is necessary but not sufficient: empirical demonstration with random Hermitian matrices
- §10.3 The Selberg trace formula reading: spectral side empirical, geometric side empirical, geometric space unknown
- §10.4 The framework's structural hints: direct sum / tensor product / graded operator
- §10.5 Executable test suite with scorecard
- §10.6 Status: target sharpened from "find H with spec γ_k" to "find H with Tr(cos(ωH)) = prime explicit formula AND GUE statistics"

### Open Problems section updated

**"Extension to L-functions"** — original was a question ("Does it extend?"); now reports the empirical answer (yes, three classes confirmed), with remaining breadth as open work.

**"Hilbert-Pólya operator construction"** — original cited Berry-Keating and Connes as related work; now references §10 for the framework's specific contribution (constraint specification + executable test suite) and sharpens the target statement.

### Bibliography additions

- `RudnickSarnak1996`: Duke Math. J. 81 (1996), 269–322
- `Weil1952`: explicit formulas
- `Dedekind1871`: Vorlesungen Supplement X
- `Selberg1956`: trace formula
- `TartiniMap`: accompanying technical note
- `HPCode`: reference implementation

---

## What did NOT change

- Sections 1–7 preserved exactly. No deletions, no edits to existing proofs or theorems.
- All existing labels, theorem numbers, and equation numbers preserved (new content uses §8/§9/§10).
- Bibliography style and layout preserved.
- Existing figures retained (some have known empty boxes — `fig_variance_scaling`, `fig_flow_field`, `fig_wronskian_heatmap` were missing in v2M too).

---

## Page count

- v2M: 17 pages
- Extended: 26 pages
- Delta: +9 pages (three new sections of ~3 pages each)

---

## Files in the extension package

| File | Description |
|---|---|
| Riemann_Spectral_Critical_Line.tex | Full LaTeX source, 26-page output |
| Riemann_Spectral_Critical_Line.pdf | Compiled output |
| tartini_synthesis/ | R₃, prime-power, Fourier-dual figures + paragraph |
| l_function_test/ | L(s, χ₄) test data + figure |
| l_function_arc/ | Cross-correlation + Dedekind figures + synthesis |
| hilbert_polya/ | Scorecard figure + test code |
| PaperB_changelog_extended.md | This document |

---

## Outstanding work

What still needs to happen before submission:

1. **Replace placeholder figures**: fig_variance_scaling, fig_flow_field, fig_wronskian_heatmap need to be generated (or removed if redundant)
2. **Add figures for new sections**: the empirical content of §8–§10 is currently table-only; figures from tartini_synthesis/, l_function_arc/, hilbert_polya/ should be embedded via \includegraphics
3. **Internal consistency check**: verify cross-references (\ref{sec:...}, \ref{eq:...}) all resolve
4. **External review**: send to Grok or human reviewer for math/structural critique
5. **Submission**: Experimental Mathematics is the appropriate venue per the framework's stated target

These are quality-pass tasks, not blockers. The paper compiles, the content is integrated, and the structural extension is complete.
