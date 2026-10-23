# CPF experimental-claims check, 22 October 2026

The endpoint audit closes its review of the recovered **Constraint Projection Framework** (CPF)
article with: "We have not authenticated the article's claimed experimental confirmations; its
algebraic failures are sufficient to reject the claimed zero-input derivation, without making a
claim about those experiments"
([endpoint audit, line 183](condensate_energy/endpoint_audit/README.md#a-recovered-claim-of-complete-closure-does-not-close-the-inputs)).
This note does the authentication it deferred. For each experimental or observational claim in the
article, we located the primary source and checked whether it says what the CPF attributes to it.
It is a citation check, not a re-review of the algebra. The algebraic dispositions in the endpoint
audit (items 1–6) are unchanged and are cited here only where a row depends on them.

The article is
[`CPF-recovered-1.tex`](condensate_energy/endpoint_audit/source-snapshots/CPF-recovered-1.tex)
(byte-identical to `CPF-recovered-0.tex`; dated "August 20, 2026" at its line 29). Line numbers
below refer to that file at commit `5417173`. The snapshot, the endpoint audit README and
`microscopic.json` (which carries the same caveat at line 214) are manifest-bound and were not
edited. A paste-ready replacement for the README sentence was handed to the owner with this check
and is not applied.

## Scope and method

The article has no `\cite` commands. Its bibliography is attached by subject, so we matched each
experimental claim to the entry it names in the text (the "CODATA 2022" table header, "(Nature,
2026)", "(Science, 2026)", "FDM") or, for the Ω_k and Bell rows, to the only entry on that subject.
That matching is ours and is stated per row. The six mathematical references (Finkelstein–Rubinstein,
White, Călugăreanu, Fuller, Guinand, Weil) make no experimental claim and were not checked.

Sources were fetched on 23 October 2026. For each one we resolved the DOI at `doi.org`, read its
Crossref record, and took the quoted text from the arXiv full text where one exists, otherwise
from the Crossref abstract field (Science, Planck, Proietti), the publisher-deposited abstract in the
PolyU repository (Nature), or the Particle Data Group review PDFs (PDG). Publisher landing pages
returned HTTP 403 to this environment for 9 of 10 DOIs, so no paywalled full text was read. The
sigma and voltage figures were computed with mpmath at 30 digits from the printed numbers and the
exact SI values of h and e.

## Result

| # | CPF claim (line) | Quantity and value as printed | Citation as printed | Primary source | Verdict |
|---|---|---|---|---|---|
| 1 | α⁻¹ at zero momentum matches CODATA 2022 (40, 194) | 137.035 999 171 vs 137.035 999 177(21); "6 × 10⁻⁹ (<0.3σ)" | E. Tiesinga et al., *Rev. Mod. Phys.* **94**, 035002 (2023) (530) | Mohr, Newell, Taylor, Tiesinga, *Rev. Mod. Phys.* **97**, 025002 (2025), doi:10.1103/RevModPhys.97.025002, arXiv:2409.03787 | **Cited inaccurately.** The reference value and the 0.286σ arithmetic are right. The locator is wrong: doi:10.1103/RevModPhys.94.035002 is Harilal et al., "Optical diagnostics of laser-produced plasmas" (2022). The agreement is by construction, because the cutoff inserts the target value (endpoint audit item 2). |
| 2 | α⁻¹(M_Z) matches CODATA 2022 (195) | 127.946 vs 127.952(9); "0.43σ" | Same entry, by the column header "CODATA 2022" | Not in CODATA 2022 (no "127." anywhere in its text). The value is the PDG 2020 MS-bar value α̂⁽⁵⁾(M_Z)⁻¹ = 127.952 ± 0.009 (Erler and Freitas, *Review of Particle Physics*, doi:10.1093/ptep/ptaa104). | **Cited inaccurately.** It comes from the wrong source, and the printed discrepancy is wrong: \|127.952 − 127.946\|/0.009 = 0.667σ. The value is also superseded: PDG 2022 gives 127.951 ± 0.009 (doi:10.1093/ptep/ptac097) and PDG 2024 gives 127.930 ± 0.008 (doi:10.1103/PhysRevD.110.030001), which is 2.00σ from 127.946. The article never derives 127.946; it appears only at line 195. |
| 3 | Ω_k = 0 "matches the latest cosmic microwave background observations" (365) | Ω_k = 0.0007 ± 0.0019 | Planck Collaboration, "Planck 2018 results. VI", *A&A* **641**, A6 (2020) (546) | Same paper, doi:10.1051/0004-6361/201833910, arXiv:1807.06209, eq. (47b) | **Cited inaccurately.** The number and the locator are right. The number is a CMB + lensing + BAO combination, not a CMB result. The same paper's constraint from the CMB power spectra alone (TT,TE,EE+lowE) is Ω_K = −0.044 (+0.018/−0.015), which it calls "an apparent detection of curvature at well over 2 σ". |
| 4 | Polar vortex lattices give "direct empirical confirmation of the framework's predictions" (439, 447) | Winding n = ±1 for the "Topological Stitching Operator" | "Nature", "Intrinsic polar vortex crystals in A-site layer-ordered perovskites", *Nature* **616**, 43 (2026) (548) | Xu, Luo, Yue, … , Zhu, *Nature* **653**, 83–89 (published 29 April 2026), doi:10.1038/s41586-026-10470-2 | **Cited inaccurately.** The paper exists and the title is exact. The volume, page and authors are wrong: Crossref lists *Nature* **616** pp. 42–43 (April 2023) as "Blue foods brought to the table to improve fish-policy decisions". The abstract explains the lattice by octahedral rotations and phonon exchange and does not refer to the CPF. The paper appeared before the article's 20 August 2026 date, so it cannot confirm a prediction made in the article. |
| 5 | Ultra-low-voltage switching in α-Bi₂SeO₅ gives "direct empirical confirmation" (440, 447) | V_op = α⁻¹ ħ/(eτ) ≈ 0.8 V | "Science", "Wafer-scale ultrathin van der Waals ferroelectric oxide α-Bi₂SeO₅", *Science* **371**, eabc1234 (2026) (550) | Wu, Li, Han, … , "Wafer-scale ultrathin and uniform van der Waals ferroelectric oxide", *Science* **391**, eadz1655 (29 January 2026), doi:10.1126/science.adz1655 | **Cited inaccurately.** The 0.8 V figure is in the source, as the operating voltage of FeFET arrays. The locator is wrong: doi:10.1126/science.abc1234 returns 404 at both doi.org and Crossref, and the title and authors differ. The article never defines τ. Reaching 0.8 V needs τ = 1.127 × 10⁻¹³ s, while the source's own 20 ns write time gives 4.51 × 10⁻⁶ V. The paper also predates the article. |
| 6 | S_LF = 2√2 "rigorously falsifying" Absoluteness of Observed Events (44, 296–299) | 2√2 ≈ 2.8284 | M. Proietti et al., "Experimental test of local observer independence", *Sci. Adv.* **5**, eaaw9832 (2019) (532). This entry is in the bibliography only; the text does not attribute the claim to it. | Same paper, doi:10.1126/sciadv.aaw9832, arXiv:1902.05080 | **Confirmed as cited**, as a bibliographic entry. It does not support the article's stronger statement. The experiment measured 2.416 ± 0.075, about 5.5σ below 2√2, and its conclusion depends on the assumptions of free choice and locality. |
| 7 | Rotation curves resolved "without exotic particles"; "matches the Ultralight Fuzzy Dark Matter (FDM) phenomenology" (42, 424) | v_rot → constant | L. Hui et al., "Ultralight scalars as cosmological dark matter", *Phys. Rev. D* **95**, 043541 (2017) (552) | Hui, Ostriker, Tremaine, Witten, doi:10.1103/PhysRevD.95.043541, arXiv:1610.08297 | **Source says the opposite** on particle content. FDM is a hypothesised light boson (m ∼ 10⁻²² eV). The source also describes FDM halos as a soliton core inside an envelope that "resembles a CDM halo", whereas the article's own rotation formula tends to zero (endpoint audit item 4). The locator is right. |

The six bibliography entries cover seven rows, because rows 1 and 2 share one entry. Three entries
have correct locators (Planck, Proietti, Hui et al.). Three are wrong: one points to an unrelated
paper (CODATA), one has a wrong volume and page (Nature), and one does not resolve (Science).

Verdicts by row: 1 confirmed as cited (row 6, bibliographic only), 5 cited inaccurately, 1 source
says the opposite, 0 source not found. Both papers in rows 4 and 5 were found by their titles,
although the locators the article prints for them are wrong.

None of the seven rows confirms a CPF derivation:

- Row 1 compares against a value the article inserted.
- Row 2 compares against a number the article does not derive, and the printed σ is wrong.
- Row 3 is a combined measurement consistent with zero curvature. It cannot tell the CPF apart
  from any other flat model.
- Rows 4 and 5 are experiments published before the article, and their sources explain them by
  other mechanisms.
- Row 6 is a conditional measurement below 2√2.
- Row 7 cites a model that is a new particle.

The rows support the endpoint audit's rejection of the zero-input derivation. They do not change its
grounds, which remain algebraic.

## Evidence quotes

Each quotation below is copied verbatim from the cited source. Where the source text came from a
PDF, line breaks and the layout of subscripts are normalised.

**1. CODATA 2022.** The arXiv:2409.03787 constants table reads "inverse fine-structure constant α−1
137.035 999 177(21) 1.6 × 10−10". The NIST value page (physics.nist.gov, `Value?alphinv`) reads
"Concise form 137.035 999 177(21) … Source: 2022 CODATA recommended values". Crossref gives the
title of doi:10.1103/RevModPhys.97.025002 as "CODATA recommended values of the fundamental physical
constants: 2022", with authors Mohr, Newell, Taylor and Tiesinga, issued 2025-04-30. Crossref gives
the title of the printed locator doi:10.1103/RevModPhys.94.035002 as "Optical diagnostics of
laser-produced plasmas", with authors Harilal, Phillips, Froula and others, issued 2022-08-15. The
"E. Tiesinga et al." byline matches the 2018 edition (Tiesinga, Mohr, Newell, Taylor,
doi:10.1103/RevModPhys.93.025010).

**2. α at M_Z.** PDG 2020, review "10. Electroweak Model and Constraints on New Physics", revised
March 2020 by J. Erler and A. Freitas: "In the modified minimal subtraction (MS) scheme … we have
α̂⁽⁴⁾(m_τ)⁻¹ = 133.472 ± 0.007 and α̂⁽⁵⁾(M_Z)⁻¹ = 127.952 ± 0.009." PDG 2022 gives
"α̂⁽⁵⁾(M_Z)⁻¹ = 127.951 ± 0.009". PDG 2024, revised April 2024, gives "α̂⁽⁵⁾(M_Z)⁻¹ = 127.930 ± 0.008". The
CODATA 2022 text has 0 matches for "127.".

**3. Planck 2018 VI**, §7.3:

- "This is a prediction that can be tested to high accuracy by the combination of CMB and BAO data
  (the CMB alone suffers from a geometric degeneracy, which is weakly broken with the addition of
  CMB lensing)."
- "ΩK = −0.044 +0.018 −0.015 (68 %, Planck TT,TE,EE+lowE), (46b) an apparent detection of curvature
  at well over 2 σ."
- "ΩK = 0.0007 ± 0.0019 (68 %, TT,TE,EE+lowE+lensing+BAO). (47b) The joint results suggests our
  Universe is spatially flat to a 1 σ accuracy of 0.2 %."

We did not check whether a later survey superseded this as "the latest" observation by 20 August
2026.

**4. Nature 653, 83–89.** From the abstract deposited in the PolyU repository (handle
10397/119374), which carries the same DOI:

- "Here we show that a two-dimensional polar hedgehog lattice with a period down to 4 nm can
  crystallize spontaneously free from any external boundary constraints in a family of A-site
  layer-ordered perovskites."
- "Theoretical calculations show that the exchange interaction of phonons describing the octahedral
  rotations is the primary driving force of this intriguing dipole topology."

Crossref dates the paper 2026-04-29. The abstract does not state a winding number, and we did not
read the full text.

**5. Science 391, eadz1655.** From the Crossref abstract: "Ultrathin vdW ferroelectric oxides formed
atomically uniform interfaces with two-dimensional semiconductors and yielded ferroelectric
field-effect transistor (FeFET) arrays with a low operating voltage (0.8 volts), exceptional cycling
endurance (>1.5 × 10¹² cycles), fast write speed (20 nanoseconds), …". Crossref dates the paper
2026-01-29. The figures from the CPF formula are α⁻¹ħ/e = 9.0199 × 10⁻¹⁴ V·s, so 0.8 V needs
τ = 1.1275 × 10⁻¹³ s, and τ = 20 ns gives V = 4.5099 × 10⁻⁶ V.

**6. Proietti et al. 2019** (arXiv:1902.05080):

- "We achieve a value of S_exp = 2.416 +0.075 −0.075, thus violating inequality (2) by more than 5
  standard deviations."
- "Modulo the potential loopholes and accepting the photons' status as observers, the violation of
  inequality (2) implies that at least one of the three assumptions of free choice, locality, and
  observer-independent facts must fail."

The abstract states: "If one holds fast to the assumptions of locality and free-choice, this result
implies that quantum theory should be interpreted in an observer-dependent way."

**7. Hui, Ostriker, Tremaine, Witten 2017** (arXiv:1610.08297):

- "An intriguing alternative to cold dark matter (CDM) is that the dark matter is a light
  (m ∼ 10⁻²² eV) boson having a de Broglie wavelength λ ∼ 1 kpc, often called fuzzy dark matter
  (FDM)."
- "(ii) FDM halos are comprised of a core that is a stationary, minimum-energy configuration called
  a "soliton", surrounded by an envelope that resembles a CDM halo."

## Not checked

The article also says the following, but cites no source for it, so there was nothing to
authenticate:

- the "Empirical Verification" table entry g = 2 (line 477), which the article itself says receives
  QED corrections;
- the acknowledgement of "experimental groups at CERN" (line 524), which has no matching
  bibliography entry.

We did not test whether the article's CHSH-form S_LF, which uses settings 2 and 3 only, is a
Local-Friendliness inequality in the sense of the literature. Item 6 of the endpoint audit covers
that calculation within its own assumptions.

## Identifier resolution

All identifiers were resolved from this environment on 23 October 2026.

| Identifier | doi.org | Crossref | Text read from |
|---|---|---|---|
| 10.1103/RevModPhys.97.025002 | 302 | 200 | arXiv:2409.03787 (abs 200, PDF) |
| 10.1103/RevModPhys.94.035002 (printed) | 302 | 200, unrelated title | Crossref title only |
| 10.1093/ptep/ptaa104 (PDG 2020) | 302 | 200 | pdg.lbl.gov 2020 review PDF (200) |
| 10.1093/ptep/ptac097 (PDG 2022) | 302 | 200 | pdg.lbl.gov 2022 review PDF (200) |
| 10.1103/PhysRevD.110.030001 (PDG 2024) | 302 | 200 | pdg.lbl.gov 2024 review PDF (200) |
| 10.1051/0004-6361/201833910 | 302 | 200 | arXiv:1807.06209 (abs 200, PDF) |
| 10.1038/s41586-026-10470-2 | 302 | 200 | nature.com landing (200); abstract via PolyU repository (200) |
| 10.1126/science.adz1655 | 302 | 200 | Crossref abstract |
| 10.1126/science.abc1234 (printed) | 404 | 404 | does not exist |
| 10.1126/sciadv.aaw9832 | 302 | 200 | arXiv:1902.05080 (abs 200, PDF) |
| 10.1103/PhysRevD.95.043541 | 302 | 200 | arXiv:1610.08297 (abs 200) |
| 10.1103/RevModPhys.93.025010 (2018 edition) | 302 | 200 | Crossref record only |

Each `doi.org` 302 redirected to the publisher. Every landing page except nature.com answered 403
to this environment, which is why the text column names a second route.
