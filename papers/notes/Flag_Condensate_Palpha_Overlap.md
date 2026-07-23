> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Standing-Wave Overlap Proxy for Alpha Preformation: \(P_\alpha\) from Confined Flag Mode and Gaussian Cluster Trial

**ACS Theoretical Physics Working Group**  
*Sovereign-Stack ACS Research Program & Flag Condensate Project*  
`research@acs-foundation.org` — July 22, 2026

---

## Abstract

The companion nuclear-decay note extracts \(\log_{10} P_\alpha\) from Geiger–Nuttall intercepts and lifetime ratios on a 14-isotope set (\(^{212}\mathrm{Po}\)–\(^{244}\mathrm{Cm}\)), without predicting preformation from interior structure. This sequel evaluates a geometric/structural standing-wave overlap proxy on \([0,R]\): the \(\ell=0\) confined flag reduced radial mode \(u_{\mathrm{in}}(r)\propto r\,j_0(\pi r/R)\) against an alpha-cluster Gaussian/HO trial \(u_\alpha(r)\propto r\,e^{-r^2/(2a_\alpha^2)}\) with \(a_\alpha=r_0\cdot 4^{1/3}\) and input \(r_0\approx 1.2\,\mathrm{fm}\).

On the stated set: \(\langle\log_{10} P_{\mathrm{model}}\rangle=-0.3905\), Pearson \(r=+0.8882\) vs extracted \(\log_{10} P_\alpha\), RMS residual \(1.7705\) at \(S=1\). One global spectroscopic factor \(S\approx 2.70\times 10^{-2}\) reduces RMS to \(0.8220\) (correlation unchanged). Absolute scale may need global \(S\); not a many-body uniqueness claim.

---

## Motivation and scope

Companion paper: slope of alpha-decay systematics is geometric (\(W\), transfer matrix); \(P_\alpha\) was intercept-extracted. This note asks whether confined standing-wave overlap with an alpha-like packet tracks that extracted column.

**RC1 scope.** \(P_{\mathrm{model}}\) is a geometric/structural preformation *proxy*, not a shell-model spectroscopic factor. Half-lives enter only via the published extracted comparison column.

---

## Radial modes

**Confined flag (\(\ell=0\)).**
\[
u_{\mathrm{in}}(r)=r\,j_0(kr),\qquad k=\pi/R
\]

**Alpha-cluster trial.**
\[
u_\alpha(r)=r\,e^{-r^2/(2a_\alpha^2)},\qquad a_\alpha=r_0\cdot 4^{1/3}
\]
with \(r_0=1.2\,\mathrm{fm}\) \(\Rightarrow\) \(a_\alpha\approx 1.905\,\mathrm{fm}\).

**Overlap.**
\[
P_{\mathrm{model}}=\frac{\bigl|\int_0^R u_{\mathrm{in}}u_\alpha\,\mathrm{d}r\bigr|^2}{\bigl(\int_0^R u_{\mathrm{in}}^2\,\mathrm{d}r\bigr)\bigl(\int_0^R u_\alpha^2\,\mathrm{d}r\bigr)}
\]
Optional: \(P_S=S\,P_{\mathrm{model}}\).

---

## Numerical protocol

Simpson quadrature, \(N=4096\) on \([0,R]\). Code: `rh_papers_may21/acs-framework/code/palpha_overlap/palpha_overlap.py`. JSON: `rh_papers_may21/acs-framework/docs/palpha_overlap_results.json`. Logs: `docs/palpha_overlap_logs/`.

---

## Results (stated 14-isotope set)

| Isotope | \(R\) (fm) | \(\log_{10} P_{\mathrm{model}}\) | \(\log_{10} P_\alpha^{\mathrm{ext}}\) | resid (raw) | \(\log_{10}(S P)\) | resid (\(S\)) |
|---------|-----------:|---------------------------------:|---------------------------------------:|------------:|-------------------:|--------------:|
| \(^{212}\mathrm{Po}\) | 8.99 | −0.3692 | −1.53 | +1.1608 | −1.9373 | −0.4073 |
| \(^{214}\mathrm{Po}\) | 9.02 | −0.3722 | −1.19 | +0.8178 | −1.9403 | −0.7503 |
| \(^{216}\mathrm{Po}\) | 9.05 | −0.3753 | −1.04 | +0.6647 | −1.9434 | −0.9034 |
| \(^{218}\mathrm{Po}\) | 9.07 | −0.3773 | −0.82 | +0.4427 | −1.9454 | −1.1254 |
| \(^{220}\mathrm{Rn}\) | 9.10 | −0.3804 | −1.12 | +0.7396 | −1.9485 | −0.8285 |
| \(^{224}\mathrm{Ra}\) | 9.16 | −0.3865 | −1.54 | +1.1535 | −1.9546 | −0.4146 |
| \(^{226}\mathrm{Ra}\) | 9.18 | −0.3885 | −1.73 | +1.3415 | −1.9566 | −0.2266 |
| \(^{228}\mathrm{Th}\) | 9.21 | −0.3916 | −1.87 | +1.4784 | −1.9597 | −0.0897 |
| \(^{232}\mathrm{Th}\) | 9.26 | −0.3967 | −2.17 | +1.7733 | −1.9648 | +0.2052 |
| \(^{234}\mathrm{U}\) | 9.29 | −0.3997 | −2.64 | +2.2403 | −1.9678 | +0.6722 |
| \(^{238}\mathrm{U}\) | 9.34 | −0.4048 | −1.97 | +1.5652 | −1.9729 | −0.0029 |
| \(^{238}\mathrm{Pu}\) | 9.34 | −0.4048 | −3.28 | +2.8752 | −1.9729 | +1.3071 |
| \(^{240}\mathrm{Pu}\) | 9.36 | −0.4068 | −2.91 | +2.5032 | −1.9749 | +0.9351 |
| \(^{244}\mathrm{Cm}\) | 9.42 | −0.4129 | −3.61 | +3.1971 | −1.9810 | +1.6290 |

### Summary statistics

- \(\langle\log_{10} P_{\mathrm{model}}\rangle = -0.3905\) (\(\sigma=0.0142\))
- \(\langle\log_{10} P_\alpha^{\mathrm{ext}}\rangle = -1.9586\) (\(\sigma=0.8656\))
- Pearson \(r = +0.8882\)
- RMS (\(S=1\)) = 1.7705
- Best-fit global \(S = 2.703\times 10^{-2}\) (\(\log_{10} S = -1.5681\))
- RMS (with \(S\)) = 0.8220 (improvement +0.9485)
- \(S\) improves RMS: yes; correlation unchanged (affine shift)

**Interpretation.** With fixed \(a_\alpha\) and weakly varying \(R\), \(\log_{10} P_{\mathrm{model}}\) is nearly flat while extracted \(\log_{10} P_\alpha\) varies more. The proxy tracks a mild geometric trend (\(r\approx 0.89\)); isotope-specific structure remains in residuals. Global \(S\) absorbs mean offset only.

---

## Conclusion

Standing-wave overlap sequel to the nuclear-decay note: confined \(\ell=0\) flag mode vs Gaussian alpha trial on \([0,R]\). On the stated set, correlation \(r=+0.8882\); absolute scale improved by \(S\approx 0.027\). Documents a geometric preformation trend, not a unique many-body prediction.

**Next step.** Flat \([0,R]\) measure and Gaussian trial are a geometric proxy. Sequel: AdS-like throat weight \(w(r)=R/r\) and Woods–Saxon (optional Coulomb-tail) alpha trial — `flag_condensate_palpha_throat_overlap.tex` / `Flag_Condensate_Palpha_Throat_Overlap.tex`. Baseline artifacts retained for comparison.

---

## Code / artifacts

- Script: `rh_papers_may21/acs-framework/code/palpha_overlap/palpha_overlap.py`
- Results: `rh_papers_may21/acs-framework/docs/palpha_overlap_results.json`
- Logs: `rh_papers_may21/acs-framework/docs/palpha_overlap_logs/`
- Companion: `flag_condensate_nuclear_decay.tex` / `acs-framework-public/papers/notes/Flag_Condensate_Nuclear_Decay.tex`
- Throat/WS sequel: `flag_condensate_palpha_throat_overlap.tex` / `acs-framework-public/papers/notes/Flag_Condensate_Palpha_Throat_Overlap.tex`
