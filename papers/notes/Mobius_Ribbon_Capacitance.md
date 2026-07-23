# Möbius-Ribbon Capacitance: Annulus, Conformal Modulus, and BIE Revisions of the α Estimate

**Flag Condensate Collaboration** · Sovereign-Stack ACS Research Program · July 22, 2026  
Sequel to `mobius_screw_electron.tex` · Source: `mobius_ribbon_capacitance.tex`

---

## Abstract

The framed-unknot electron note obtains α⁻¹≈137.036 from an annulus capacitance and self-stress match `(e/2)²/(2C)=m_e c²`, and asks (§4.1) for conformal-map / BIE revision of C. This sequel implements three as-reported models at R=ℏ/(2 m_e c): annulus baseline, double-cover strip→annulus conformal modulus, and constant-panel BIE on a discretized Möbius/(2,1) ribbon. Aspect ratios are scanned; results are written to JSON. Model claims only — comparison uses CODATA-style α⁻¹≈137.035999084; no uniqueness claim for α.

---

## Self-stress match

$$
\frac{(e/2)^2}{2C}=m_e c^2
\quad\Rightarrow\quad
\alpha^{-1}=\frac{\pi\epsilon_0 R}{C}.
$$

---

## Models

1. **Annulus:** `C = 2π ε₀ R / (ln(8R/a)+1)` → `α⁻¹ = (ln(8R/a)+1)/2`.
2. **Conformal (cover=2):** strip L=4πR, W=2a → annulus with `a_eff = R_m sinh(a/(2R))`, `R_m=2R`, same log scheme.
3. **BIE:** single-layer collocation on `X(u,v)=r(u)+v n(u)` with torus-based Möbius frame; moderate aspect window only.

---

## As-implemented numbers (recorded run)

**Demo a/R = 0.05**

| Model | C [F] | α⁻¹ | C/(ε₀ R) |
|-------|-------|-----|----------|
| Annulus | 1.768×10⁻²⁴ | 3.037587 | 1.034 |
| Conformal | 3.174×10⁻²⁴ | 1.692054 | 1.857 |
| BIE Möbius | 1.441×10⁻²³ | 0.372688 | 8.430 |

**CODATA-matching aspect (analytic)**

| Model | a/R | α⁻¹ |
|-------|-----|-----|
| Annulus | ≈2.039×10⁻¹¹⁸ | ≈137.036 |
| Conformal | ≈3.824×10⁻²³⁷ | ≈137.036 |
| BIE | not resolved at that aspect | — |

On the scanned moderate grid: α⁻¹_ann > α⁻¹_conf > α⁻¹_BIE at shared a/R. The companion 137.036 is an annulus-cutoff tuning, not reproduced by conformal/BIE at moderate geometric aspect.

Reference in comparisons: α⁻¹≈137.035999084 (CODATA-style). Runtime `scipy.constants` reciprocal ≈137.035999178.

---

## Files

- Code: `rh_papers_may21/acs-framework/code/capacitance_ribbon/ribbon_capacitance.py`
- Results: `rh_papers_may21/acs-framework/docs/capacitance_ribbon_results.json`
- Logs: `rh_papers_may21/acs-framework/docs/capacitance_ribbon_logs/`
- Formal TeX: `mobius_ribbon_capacitance.tex`
- Parent note: `mobius_screw_electron.tex`
