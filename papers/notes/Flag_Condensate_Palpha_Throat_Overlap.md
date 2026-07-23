# Throat-Geometry Overlap for Alpha Preformation: Warped Measure and Woods–Saxon Cluster Trial

**ACS Theoretical Physics Working Group**  
Sovereign-Stack ACS Research Program & Flag Condensate Project  
Date: July 22, 2026

---

## Abstract

The flat \([0,R]\) standing-wave overlap proxy uses \(\ell=0\) flag mode vs Gaussian alpha trial with measure \(dr\). This sequel replaces that proxy geometry with (i) the AdS-like throat radial weight \(w(r)=R/r\) implied by the companion nuclear metric \(ds^2=(R^2/r^2)\,dr^2+\cdots\), and (ii) a Woods–Saxon (WS) alpha-cluster radial trial as primary, keeping Gaussian/HO as comparison. Overlap support remains the confined interior \([0,R]\); the barrier \([R,b]\) stays the Gamow domain. On the same 14-isotope set, primary throat+WS yields \(\langle\log_{10} P_{\mathrm{model}}\rangle=-0.4607\), Pearson \(r=+0.8875\) vs extracted \(\log_{10} P_\alpha\), and \(S_\star\approx 3.18\times 10^{-2}\) reducing RMS residual from \(1.7099\) to \(0.8247\). Relative to the flat-Gaussian proxy, \(\Delta r\approx -0.0007\). Still a geometric/structural proxy — not microscopic uniqueness.

---

## Motivation and what moved

Baseline: `flag_condensate_palpha_overlap.tex` (flat \(dr\), Gaussian \(\alpha\)). Nuclear companion: `flag_condensate_nuclear_decay.tex` (AdS-like throat metric; 14-isotope table).

**RC1 scope.** \(P_{\mathrm{model}}\) remains a geometric/structural preformation *proxy*. Warped measure and WS shape are documented mechanism choices, not unique many-body structure. Absolute scale may still need one global \(S\).

### What moved (proxy → throat/WS)

- **Measure:** flat \(dr\) → throat weight \(w(r)=R/r\) from \(\sqrt{g_{rr}}\) on the AdS-like confining metric.
- **Alpha trial:** Gaussian/HO → Woods–Saxon primary \(u_\alpha(r)=r/(1+e^{(r-R_\alpha)/a_{\mathrm{WS}}})\), with optional WS×Coulomb-tail match for comparison.
- **Artifacts:** `palpha_overlap_throat.py`, `palpha_overlap_throat_results.json`; baseline proxy retained.

### What remains open

- Isotope-specific spectroscopic amplitudes beyond one global \(S\).
- Self-consistent bound-state WS+Coulomb (R-matrix / cluster eigenmode).
- Overlap with non-vanishing flag amplitude in the barrier \([R,b]\) (Dirichlet \(u_{\mathrm{in}}\) vanishes at \(R\)).
- Absolute uniqueness of preformation from many-body structure.

**Next.** Parametric isotope-resolved \(S(A,Z)\) (with leave-one-out) and a self-consistent WS+Coulomb interior eigenmode are implemented as comparison channels in `flag_condensate_palpha_refined.tex` / `palpha_overlap_refined.py`. On the stated set, parametric \(S(A,Z)\) reduces LOO residual RMS most among non-tautological protocols.

---

## Throat weight and overlap

Companion metric:
\[
ds^2 = \frac{R^2}{r^2}\,dr^2 + \frac{r^2}{R^2}\eta_{\mu\nu}\,dx^\mu dx^\nu.
\]
Radial measure factor \(\sqrt{g_{rr}}=R/r\):
\[
P_{\mathrm{model}}
=
\frac{\bigl|\int_0^R u_{\mathrm{in}} u_\alpha w\,dr\bigr|^2}
{\bigl(\int_0^R u_{\mathrm{in}}^2 w\,dr\bigr)
 \bigl(\int_0^R u_\alpha^2 w\,dr\bigr)},
\qquad w(r)=\frac{R}{r}.
\]
For \(u\sim O(r)\) near the origin the integrands remain integrable. Flat \(w\equiv 1\) recomputed for comparison (reproduces baseline).

**Domain choice.** Overlap support is \([0,R]\). Barrier \([R,b]\) determines Gamow \(W\) in the nuclear companion; it is not overlap support for the Dirichlet interior mode.

---

## Radial modes

**Flag (\(\ell=0\)):** \(u_{\mathrm{in}}(r)=r\,j_0(\pi r/R)\).

**WS primary** (\(r_0=1.2\,\mathrm{fm}\), \(a_{\mathrm{WS}}=0.55\,\mathrm{fm}\)):
\[
u_\alpha^{\mathrm{WS}}(r)=\frac{r}{1+e^{(r-R_\alpha)/a_{\mathrm{WS}}}},
\qquad R_\alpha=r_0\cdot 4^{1/3}\approx 1.905\,\mathrm{fm}.
\]
Comparison: Gaussian/HO; optional WS with exponential\(\times R_m/r\) tail matched at \(R_m=R_\alpha+2a_{\mathrm{WS}}\) (\(\kappa=1/a_{\mathrm{WS}}\), phenomenological).

---

## Numerical protocol

Simpson, \(N=4096\) on \([0,R]\).

- Script: `rh_papers_may21/acs-framework/code/palpha_overlap/palpha_overlap_throat.py`
- JSON: `rh_papers_may21/acs-framework/docs/palpha_overlap_throat_results.json`
- Logs: `rh_papers_may21/acs-framework/docs/palpha_overlap_throat_logs/`

---

## Results (primary: throat + WS)

| Isotope | R (fm) | log10 P_model | log10 P_ext | resid (raw) | log10 (S P) | resid (S) |
|---------|-------:|--------------:|------------:|------------:|------------:|----------:|
| 212Po | 8.99 | -0.4441 | -1.53 | +1.0859 | -1.9419 | -0.4119 |
| 214Po | 9.02 | -0.4465 | -1.19 | +0.7435 | -1.9443 | -0.7543 |
| 216Po | 9.05 | -0.4489 | -1.04 | +0.5911 | -1.9467 | -0.9067 |
| 218Po | 9.07 | -0.4505 | -0.82 | +0.3695 | -1.9483 | -1.1283 |
| 220Rn | 9.10 | -0.4529 | -1.12 | +0.6671 | -1.9507 | -0.8307 |
| 224Ra | 9.16 | -0.4576 | -1.54 | +1.0824 | -1.9555 | -0.4155 |
| 226Ra | 9.18 | -0.4592 | -1.73 | +1.2708 | -1.9571 | -0.2271 |
| 228Th | 9.21 | -0.4616 | -1.87 | +1.4084 | -1.9595 | -0.0895 |
| 232Th | 9.26 | -0.4656 | -2.17 | +1.7044 | -1.9634 | +0.2066 |
| 234U | 9.29 | -0.4679 | -2.64 | +2.1721 | -1.9658 | +0.6742 |
| 238U | 9.34 | -0.4718 | -1.97 | +1.4982 | -1.9697 | +0.0003 |
| 238Pu | 9.34 | -0.4718 | -3.28 | +2.8082 | -1.9697 | +1.3103 |
| 240Pu | 9.36 | -0.4734 | -2.91 | +2.4366 | -1.9713 | +0.9387 |
| 244Cm | 9.42 | -0.4781 | -3.61 | +3.1319 | -1.9760 | +1.6340 |

### Primary summary

- mean log10 P_model = -0.4607 (std 0.0110)
- mean log10 P_extracted = -1.9586 (std 0.8656)
- Pearson r = +0.8875
- RMS (S=1) = 1.7099
- best-fit global S = 3.178×10⁻² (log10 S = -1.4979)
- RMS (with S) = 0.8247 (improvement +0.8852)

### Model comparison

| Model | mean log10 P | Pearson r | RMS raw | RMS(S) |
|-------|-------------:|----------:|--------:|-------:|
| throat + WS (primary) | -0.4607 | +0.8875 | 1.7099 | 0.8247 |
| throat + WS×Coulomb tail | -0.4825 | +0.8875 | 1.6908 | 0.8245 |
| throat + Gaussian | -0.2791 | +0.8881 | 1.8715 | 0.8260 |
| flat + WS | -0.6786 | +0.8876 | 1.5201 | 0.8200 |
| flat + Gaussian (baseline) | -0.3905 | +0.8882 | 1.7705 | 0.8220 |

**Flat Gaussian vs throat+WS:** Δ mean log10 P = -0.0702; Δ r = -0.0007; Δ RMS(S) = +0.0027; S: 0.0270 → 0.0318.

**Interpretation.** Warped measure and WS shape shift absolute scale and slightly compress \(\sigma(\log_{10} P_{\mathrm{model}})\), but do not materially change correlation with extracted \(\log_{10} P_\alpha\). Isotope-specific residual structure remains; one global \(S\) absorbs mean offset only.

---

## Conclusion

Advanced the flat \([0,R]\) proxy to AdS-like throat weight \(w=R/r\) with Woods–Saxon alpha trial on the same 14-isotope set. Primary: \(\langle\log_{10} P\rangle=-0.4607\), \(r=+0.8875\), \(S_\star\approx 0.032\). Correlation essentially unchanged vs flat-Gaussian proxy. Isotope-resolved / parametric \(S\) and self-consistent WS+Coulomb eigenmodes are reported in `flag_condensate_palpha_refined.tex`. Absolute uniqueness not claimed.

---

## Code / artifacts

- Script: `rh_papers_may21/acs-framework/code/palpha_overlap/palpha_overlap_throat.py`
- Results: `rh_papers_may21/acs-framework/docs/palpha_overlap_throat_results.json`
- Logs: `rh_papers_may21/acs-framework/docs/palpha_overlap_throat_logs/`
- Baseline proxy: `flag_condensate_palpha_overlap.tex` / `docs/palpha_overlap_results.json`
- Companion: `flag_condensate_nuclear_decay.tex`
