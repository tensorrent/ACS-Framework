# Check coverage of the two update papers

[Repository home](../../README.md) · [Documentation](../README.md) · [Publication record](2026-09-24/README.md) · [Rerun receipt](2026-10-22-rerun.md) · [Reproduction](../REPRODUCTION.md)

**What this is.** Every number printed in the two update papers,
[`ACS_Action_Identifiability.tex`](../../papers/updates/ACS_Action_Identifiability.tex) and
[`ACS_Condensate_Carrier_Boundary.tex`](../../papers/updates/ACS_Condensate_Carrier_Boundary.tex),
mapped to the check in [`code/publication_20260924/verify_science.py`](../../code/publication_20260924/verify_science.py)
that exercises it, or to the archived record it rests on, or to neither. It is a coverage map for
the 58-check verifier, filed beside the 22 October rerun receipt and run against the same pinned
environment on 23 October 2026. It changes nothing manifest-bound and reruns nothing archived.

## Classes

The verifier's own scope string is: "Fresh portable action, normalization, RG, exact-root and
carrier-obstruction checks; archived PDE runs are integrity-checked, not rerun." The
[publication README](2026-09-24/README.md) says the same in prose, and the
[rerun receipt](2026-10-22-rerun.md) lists what was not rerun (the endpoint audit's 95 checks, the
Lean audits, the instruments that write into tracked `docs/` paths). The three classes follow that
boundary:

- **fresh** — a PASS line in `verify_science.py` whose pass/fail depends on the number: it is
  asserted, it is the asserted tolerance, or it is a hard-coded input without which the assertion
  would fail. "(structural)" marks a count the run depends on through array shape rather than
  through an assertion; those rows are counted as fresh but say so.
- **integrity-only** — no PASS line asserts the number; it appears in a file whose SHA-256 is
  checked by `scripts/verify_publication.py` (the 561 manifest entries or the 516 endpoint-receipt
  references), and that file is not rerun. Where a fresh check recomputes a quantity but asserts
  something else about it (the phase6 root digits, the RG λ_IR values), the row is integrity-only
  and says what the fresh check does assert.
- **none** — neither.

Check names are quoted verbatim from the verifier's PASS lines, in backticks. Archived check
names (from the endpoint JSON records) and file paths are also in backticks; the appendix lists
the 58 verifier names so the two can be told apart. Section numbers refer to the current LaTeX
source. The two `.tex` files are themselves among the eight manifest mismatches since `389afe2`:
the manifest hash matches `389afe2~1` for both, and `git diff 389afe2~1 HEAD` on them replaces
only the closing acknowledgments section with the author statement (15 lines each, no numbered
section touched), so every number tabulated here is the number the manifest bound.

## Runs behind this page

| Command (from a clean worktree at `8b9ba94`) | Result |
|---|---|
| `python code/publication_20260924/verify_science.py` (pinned venv: numpy 2.2.6, scipy 1.15.3, sympy 1.14.0) | 58 `PASS` lines, 0 `FAIL`, exit 0, `{"total": 58, "passed": 58}`; 15.0 s wall. Wrote only the ignored `build/publication/science-report.json`; `git status --short` empty. |
| `python scripts/verify_publication.py --integrity-only` | 516 receipt references verified, 16 relocated, 0 archive-only; 8 manifest mismatches, all `papers/**/*.tex` from `389afe2` (the same eight the rerun receipt lists), no evidence file among them. Every file cited below as integrity-only therefore matched its recorded hash in this run. |
| `python scripts/check_navigation.py` | 0 failures (7 pages, 242 local links). |

## Table 1 — `ACS_Action_Identifiability.tex`

The abstract carries five numbers (68, 17, four, six, one-loop); the conclusions carry none.

| # | Number as printed (section) | What it is | Check name(s) | Class |
|---|---|---|---|---|
| 1 | 68 real scalar coordinates; Φ eight, Δ sixty (abstract; §2) | dimension of the real scalar coordinate vector | `independent finite-difference derivatives`, `identical neutral Hessians across stability counterfamily` (structural: the run draws a size-68 point and pulls H back through a 68×4 tangent; no PASS line asserts 68 by name; observed 68 in this run) | fresh |
| 2 | 17 real quartic coefficients; Table 1 indices 0–16 (abstract; §2) | count and homogeneity of the quartic basis | `17 homogeneous quartics`; `neutral: all_21_restrictions_match_independent_formula` | fresh |
| 3 | four quadratic coefficients (N_Φ, Re d_Φ, Im d_Φ, N_Δ) (abstract; §2) | count and homogeneity of the quadratic basis | `4 homogeneous quadratics`; `neutral: all_21_restrictions_match_independent_formula` | fresh |
| 4 | six quartic directions invisible on the neutral family: I6, I8, I9, I10, Re H_Δ, Im H_Δ (abstract; §3) | the invisible index set | `neutral: six_coordinate_invariants_invisible` (asserts the set is exactly [6, 8, 9, 10, 11, 12]) | fresh |
| 5 | Table 1: projector labels (35,0), (35,2), (20,0), (20,2), (45,1); "the five norms sum to N_Δ²" (§2) | representation labels of the pure-Δ norms and their sum rule | no check asserts the labels or the sum rule; the basis is loaded as data. Archived: `docs/condensate_energy/canonical_vacuum/README.md`, `canonical_vacuum/results.json` check `independent-projector-generic-fields` | integrity-only |
| 6 | G = 2 on Φ and diagonal D_a entries, G = 4 on off-diagonal entries (§2) | trace kinetic metric | loaded and used by `coordinate invariance k=0.2`, `coordinate invariance k=0`, `coordinate invariance k=-0.2` and the dilation checks, but its entries are not asserted (observed {2, 4} over 68 entries in this run). Archived: `canonical_vacuum/qualified-results.json` (`kinetic_metric`, check `kinetic-metric-from-trace`) | integrity-only |
| 7 | λ_can = 4c₄/Z² (§2) | canonical radial quartic convention | `normalization: canonical_quartic_invariant_under_consistent_coordinate_change` (asserts 4c₄/Z² is invariant under Z→s²Z, c₄→s⁴c₄) | fresh |
| 8 | 21 gauge generators (§3); "21 gauge directions" (§5) | dimension of SU(4)×SU(2)_L×SU(2)_R | no PASS line asserts 21; the orbit used by the tadpoles-and-Goldstones and gauge-mass-Gram rows (9, 27) has 21 columns (observed 68×21 in this run). Archived: `docs/condensate_energy/endpoint_audit/README.md` ("the 21-vector Gram"), `endpoint_audit/identifiability.json` | integrity-only |
| 9 | twelve independent orbit directions (§3); twelve Goldstone directions excluded (Table 2 caption) | rank of the gauge orbit at the background | `tadpoles and Goldstones k=0.2`, `tadpoles and Goldstones k=0`, `tadpoles and Goldstones k=-0.2` (assert gauge_orbit_rank == 12) | fresh |
| 10 | 56 physical real scalar directions (§3) | 68 − 12 | `full stationary spectrum k=0.2` asserts (56, 0, 0); the other two rows also sum to 56 | fresh |
| 11 | neutral restriction has quartic rank eleven (§3) | rank of the neutral restriction map | `neutral: neutral_quartic_map_rank_11` | fresh |
| 12 | "the first four affect transverse masses" (§3) | I6, I8, I9, I10 change the transverse Hessian | `neutral: four_invisible_norms_change_transverse_hessian` | fresh |
| 13 | H_Δ has zero value, gradient and Hessian at the rank-one colour background (§3) | holomorphic invariants invisible through second order | `neutral: holomorphic_terms_invisible_through_Hessian`; `neutral: all_21_restrictions_match_independent_formula` (restrictions of I11, I12 are 0) | fresh |
| 14 | H_Δ = 3ABCd/√2 for the specified diagonal perturbation (§3) | nonzero cubic vertex example | no check. Archived: `canonical_vacuum/README.md` | integrity-only |
| 15 | counterfamily coefficients: k on I6+I8+I9+I10; 1/100, 1/50, 1/10, 1/50; V₂ = −2743/7200, −41/240, −1259/625 (§3.1) | the witness potential | hard-coded inputs of `full stationary spectrum k=0.2`, `full stationary spectrum k=0`, `full stationary spectrum k=-0.2` and the three tadpoles-and-Goldstones checks of row 16 (stationarity would fail with different quadratic coefficients) | fresh |
| 16 | background a = 1/3, b = 1/5, d = 1, α = 0 stationary for each tested k (§3.1) | the stationary point | `tadpoles and Goldstones k=0.2`, `tadpoles and Goldstones k=0`, `tadpoles and Goldstones k=-0.2` (tadpole ∞-norm < 1e-10 at that point) | fresh |
| 17 | neutral potential and its four physical neutral masses identical across k (§3.1) | neutral data are blind to k | `identical neutral Hessians across stability counterfamily` (4×4 tangent pullbacks agree to 1e-12) | fresh |
| 18 | Table 2: k = 1/5 → 56 / 0 / 0; k = 0 → 44 / 12 / 0; k = −1/5 → 6 / 0 / 50 | physical mode counts | `full stationary spectrum k=0.2`, `full stationary spectrum k=0`, `full stationary spectrum k=-0.2`; `coordinate invariance k=0.2`, `coordinate invariance k=0`, `coordinate invariance k=-0.2` assert the counts survive a coordinate rescaling | fresh |
| 19 | m² = (5/3)k + 4/5625 for the canonically normalised Re D₃,₀₀; negative at k = −1/5 (§3.1) | exact single-mode witness | no check asserts the formula; the sign at k = −1/5 sits inside the 50 negative modes of `full stationary spectrum k=-0.2` but is not isolated. Archived: `canonical_vacuum/README.md` | integrity-only |
| 20 | minimum physical m² ≈ 0.04321111 at k = 1/5 (§3.1) | smallest eigenvalue of the positive case | no check asserts the value (`full stationary spectrum k=0.2` asserts only the count 56). Archived: `canonical_vacuum/qualified-results.json`, `canonical_vacuum/results.json`, `canonical_vacuum/assessment.json` | integrity-only |
| 21 | gauge source g₄⁴(45, 45, 9, 9, −3) + g₄²g_R²(−72, 36, 72, −36, 12) + g_R⁴(36, 18, 36, 18, 6) (§4) | one-loop gauge contributions to λ₆–λ₁₀ | no check. Archived: `docs/condensate_energy/hidden_couplings/README.md`; `hidden_couplings/exact-witnesses.json` (`scalar_closure_witness.input` = (45, 45, 9, 9, −3)) | integrity-only |
| 22 | "the full five-dimensional Hermitian space" (§4) | scalar loop fills the fifth direction | no check. Archived: `exact-witnesses.json` checks `exact-scalar-loop-adds-fifth-direction` (rank 4 → 5), `exact-scalar-loop-full-polynomial` (5106 monomials) | integrity-only |
| 23 | Bλ_j = [80/3 λ₈ + 64/3 λ₉ − 108g₄² − 48g_R² + 8 Tr F†F] λ_j, j = 11, 12 (§4) | holomorphic beta coefficients | no check. Archived: `hidden_couplings/README.md` | integrity-only |
| 24 | ρ₁ = 8/9, ρ₂ = 0, equal couplings 4/3, zero Yukawas → B(λ₆ − λ₇) = −2560/9 (§4) | two-trace closure counterexample | no check. Archived: `exact-witnesses.json` `historical_counterexample`, check `historical-two-trace-plane-not-RG-invariant` | integrity-only |
| 25 | −K²X²/(4λ₇) (§4) | tree-elimination correction | no check. Archived: `docs/condensate_energy/action_matching/README.md`, `action_matching/tree-matching.json` | integrity-only |
| 26 | "checked against 80-digit limits" (§4) | finite-matching precision | no check. Archived: `docs/condensate_energy/finite_matching/README.md`, `finite_matching/verification.json` | integrity-only |
| 27 | Proposition 1: x→ax, m_i→a²m_i, Ω→a⁴Ω, μ→aμ; V, ∇V, H scale by a⁴, a³, a²; gauge masses by a²; fermion singular masses by a (§5) | the complete-action scale family | `action dilation V, gradient, Hessian a=0.4`, `action dilation V, gradient, Hessian a=2.3`, `gauge mass Gram dilation a=0.4`, `gauge mass Gram dilation a=2.3`, `48-Weyl complex flavor dilation a=0.4`, `48-Weyl complex flavor dilation a=2.3` | fresh |
| 28 | "including complex noncommuting Yukawa matrices" (§5) | the flavour example is genuinely noncommuting | `complex noncommuting flavor witness` (‖YZ − ZY‖ > 0.01) | fresh |
| 29 | "a complex 48-Weyl example" (§5) | fermion mass-matrix dimension | `48-Weyl complex flavor dilation a=0.4`, `48-Weyl complex flavor dilation a=2.3` (structural: the 48×48 shape was observed in this run, not asserted) | fresh |
| 30 | normalised residuals below 10⁻¹⁰ for the component scaling (§5) | tolerance of the dilation checks | the six checks in row 27 assert relative residual < 1e-10 | fresh |
| 31 | the logarithms are unchanged, so V₁ scales by a⁴ (§5) | symbolic invariance of log(M²/μ²) | `one-loop logarithm invariant under simultaneous scale change` | fresh |
| 32 | 10⁻⁹ for the one-loop sum (§5) | numeric a⁴ scaling of the one-loop potential | no check computes the one-loop sum. Archived: `endpoint_audit/identifiability.json` checks `one-loop potential including complex flavor scales to fourth power 0.4` and `… 2.3`; the 1e-9 tolerance is in `code/condensate_energy/endpoint_identifiability.py` | integrity-only |
| 33 | Λ = μ exp[−1/(2bg²(μ))] (§5) | transmutation retains an integration constant | no check. Archived: `identifiability.json` check `one-loop dimensional transmutation still needs its integration scale` | integrity-only |
| 34 | (λ_UV, λ_IR) ≃ (0.08, 0.1685520), (0.1283001, 0.1806315), (0.18, 0.1898121) (§6) | conditional UV→IR pairs of the source's SM truncation | the middle flow is recomputed by `conditional source RG reaches UV`, `perturbed boundary reaches IR -1e-05`, `perturbed boundary reaches IR 1e-05`, `finite running retains sensitivity` (λ_UV = 2√3/27 = 0.12830006), but no PASS line asserts any λ_IR value. Archived: `identifiability.json` `source_RG.alternatives` | integrity-only |
| 35 | dλ_IR/dλ_UV = 0.2088898, variational equation and boundary differences agree (§6) | boundary sensitivity at the middle point | `finite running retains sensitivity` (asserts \|s − 0.2088898\| < 1e-6 and agreement with the variational solution to 1e-5; evidence 0.20888981972361217) | fresh |
| 36 | comparison input 0.1294 (§6) | the source's IR quartic input | hard-coded IR initial value of `conditional source RG reaches UV` | fresh |
| 37 | approximately 148 GeV tree mass proxy (§6) | tree mass from the middle λ_IR | no check. Archived: `identifiability.json` `source_RG.tree_mass_proxy_GeV` = 147.99092… | integrity-only |
| 38 | λ_i = (16/9)(x, y, z, w)_i (§6) | proxy rescaling | every phase6 check (rows 39–44) divides the source equations by (16/9)² before factoring | fresh |
| 39 | 4w(x + y − 3) = 0 (§6) | fourth proxy equation factorises | `phase6: source beta4 factorization` | fresh |
| 40 | 2z² + 2w² + 3 = 0 has no real solution (§6) | nonzero-w branch impossible | `phase6: nonzero w branch impossible over reals` | fresh |
| 41 | z = 0 or z = (3 − x − y)/2 (§6) | third equation splits | `phase6: remaining beta3 factorization` | fresh |
| 42 | "precisely two real solutions" by exact elimination and Sturm counts (§6) | the real solution set | `phase6: zero elimination reconstructs both original equations exactly`, `phase6: zero all real roots isolated by exact Sturm count`, `phase6: nonzero elimination reconstructs both original equations exactly`, `phase6: nonzero all real roots isolated by exact Sturm count`, `exactly two real proxy roots` | fresh |
| 43 | (0.1811535, 0.5106919, 0, 0), (0.6447133, 0.5764245, 0, 0) (§6) | the two root values | the run re-derives both roots and asserts they solve the system (`phase6: zero original residual 0`, `phase6: zero original residual 1`, `phase6: zero independent numerical root 0`, `phase6: zero independent numerical root 1`) but never compares them with the printed digits, which it discards with its temporary directory. Archived: `endpoint_audit/phase6-real-roots.json`. A scratch rerun in this session reproduced all seven printed digits of both roots (residuals 0.0 and 1.1e-16). | integrity-only |
| 44 | neither gives 2√3/27 (§6) | the proposed Higgs number is not a proxy root | `phase6: zero proposed Higgs number is not a proxy root`, `phase6: nonzero proposed Higgs number is not a proxy root` (tests √3/24 in scaled units, which is 2√3/27 · 9/16) | fresh |
| 45 | "the full archived program timed out in its symbolic solve" (§6); 60 s in the record | the incomplete replay | no check, by design. Archived: `endpoint_audit/microscopic.json` check `Phase6 full source replay completes` (passed = false, timeout_seconds 60); `endpoint_audit/attempts/phase6-timeout-60s/` | integrity-only |
| 46 | 95 passing checks and one incomplete source replay (Appendix A) | endpoint tally | no check reruns the endpoint. Archived: `endpoint_audit/assessment.json` (checks_passed 95, checks_total 96) | integrity-only |

Table 1 counts: **fresh 27, integrity-only 19, none 0** (46 rows).

## Table 2 — `ACS_Condensate_Carrier_Boundary.tex`

The abstract and the conclusions carry no numerals; every number below is in the body or the
appendix.

| # | Number as printed (section) | What it is | Check name(s) | Class |
|---|---|---|---|---|
| 1 | vacuum (χ, q) = (1, 0); exterior charged-wave mass one (§2) | units of the reduced model, v = g = λ_χ = 1 | no check (the square completion is checked with general v, g, λ_χ). Archived: `docs/condensate_energy/self_binding/README.md` | integrity-only |
| 2 | U − g²v²f²/2 = (λ_χ/4)[(χ² − v²) + (g²/λ_χ)f²]² + (1/4)(b − g⁴/λ_χ)f⁴ (§2) | the negative-control identity | `FLS negative control exact square completion` | fresh |
| 3 | b ≥ g⁴/λ_χ ⇒ E ≥ gv\|Q\|; the tested b = 1.2 control cannot bind (§2) | consequence of the identity; the control case | the inequality is not asserted and b = 1.2 is not run. Archived: `self_binding/README.md` (b = 1.2 gives E/Q 1.0066) | integrity-only |
| 4 | b = 2√3/27, Q = 1000: E = 838.163096 (§2.1) | reference binding energy | no check. Archived: `self_binding/README.md`, `self_binding/results.json`, `self_binding/assessment.json` | integrity-only |
| 5 | ω = 0.754888212 (§2.1) | reference frequency | no check. Archived: `self_binding/README.md`, `self_binding/assessment.json`, `charge_leakage/radiation-qualified.json` | integrity-only |
| 6 | √(1 − ω²) = 0.655853480 (§2.1) | predicted tail exponent | no check. Archived: `self_binding/README.md`, `self_binding/assessment.json` | integrity-only |
| 7 | fitted exterior tail exponent 0.655853649 (§2.1) | fit to log(rf) over radii 15–20 | no check. Archived: `self_binding/README.md` only | integrity-only |
| 8 | relative virial residual 2.99×10⁻¹⁰ (§2.1) | stationarity residual | no check. Archived: `self_binding/README.md` | integrity-only |
| 9 | maximum boundary-value RMS residual 9.91×10⁻⁸ (§2.1) | solver residual | no check. Archived: `self_binding/README.md` | integrity-only |
| 10 | spacing 0.1 → 0.05 moves the energy 838.131320 → 838.155154 (§2.1) | finite-volume refinement | no check. Archived: `self_binding/README.md` (838.131320 also in `self_binding/results.json`) | integrity-only |
| 11 | no negative mode in the tested amplitude and phase sectors; dipole mode converges to the translation zero mode (§2.1) | linear stability record (its digits 0.399347, 9.30×10⁻⁶, 0.158962 are in the record, not the paper) | no check. Archived: `self_binding/README.md` | integrity-only |
| 12 | dynamics and formation tests to dimensionless time 80 (§2.1) | evolution horizon | no check. Archived: `self_binding/README.md` ("time 80 on a radius-120 domain") | integrity-only |
| 13 | P ≃ 1.077996267 ε² (§3) | leading radiated power under charge breaking | no check. Archived: `docs/condensate_energy/charge_leakage/README.md`, `charge_leakage/radiation-qualified.json`, `charge_leakage/assessment.json` | integrity-only |
| 14 | Q = 1000, e = 0.12: E/Q = 0.96420948, ω = 0.96932000 (§3) | gauged reference point | no check. Archived: `docs/condensate_energy/gauge_completion/README.md`; ω also in `gauge_completion/results.json`, `gauge_completion/assessment.json` | integrity-only |
| 15 | 14.323945 energy units outside the radius-40 domain; E_outside = e²Q²/(8πR) (§3) | exterior Coulomb energy | no check. Archived: `gauge_completion/README.md`. (The formula evaluates to 14.3239449 in this session; that is arithmetic, not a check.) | integrity-only |
| 16 | finite-volume minimisation, Gauss-law, virial and chemical-potential checks qualify the branch (§3) | qualification of the branch (record tolerances 2.2×10⁻¹⁰, 6.4×10⁻¹¹, 7.6×10⁻¹⁰, 1.9×10⁻⁸ are not printed) | no check. Archived: `gauge_completion/README.md`, `gauge_completion/results.json` | integrity-only |
| 17 | Φ = χI₂/2, D₃ = qE₄₄/√2, T¹⁵ = diag(1, 1, 1, −3)/(2√6); e = √(3/2) g₄ (§3.1) | T¹⁵ weight of the selected Δ component | `normalization: adjoint_commutator_drops_real_Delta_charge` (asserts the T¹⁵ action on E₄₄ in the 10-bar convention is √(3/2)·E₄₄ with exactly that T¹⁵) | fresh |
| 18 | H_Δ and its first derivative vanish on the rank-one slice (§3.1) | no illegal single-component q⁴ was removed | no check on this slice (`neutral: holomorphic_terms_invisible_through_Hessian` is on the companion paper's neutral background, a different rank-one slice). Archived: `gauge_completion/README.md`, `gauge_completion/carrier-contract.json` | integrity-only |
| 19 | at unit gauge couplings the 21-generator mass Gram has eighteen zeros and three eigenvalues 1/2 (§3.1) | exterior gauge spectrum with SU(4) unbroken | no check. Archived: `gauge_completion/README.md` | integrity-only |
| 20 | three massless complex colour–lepton vector pairs with T¹⁵ weight 2/3 of the Δ component's (§3.1) | additional charged carriers | no check. Archived: `gauge_completion/README.md` | integrity-only |
| 21 | the torus curve is a (2,1) embedding and an unknot (§4.1) | knot type of the earlier note's curve | no check; no hash-checked record computes the knot type. The hashed `docs/frontier/2026-09-11/workstreams/physical/report.md` uses the (2,1) centreline without classifying it, and the `code/framed_unknot` outputs under `docs/` are not in the hash set. | none |
| 22 | g = 1 for classical charge and mass on the same curve with uniform charge-to-mass ratio (§4.1) | classical gyromagnetic ratio independent of framing | no check. Archived: `docs/frontier/2026-09-11/workstreams/physical/report.md` §M02 (in the manifest; the `framed_unknot` JSON outputs are not) | integrity-only |
| 23 | C = 2πε₀R/L, q = e/2, R = ħ/(2mc) ⇒ E/mc² = αL/2 (§4.2) | capacitor self-energy in the proposal's own conventions | no check derives αL/2 from C, q, R. Archived: `endpoint_audit/microscopic.json` check `source capacitance and radius imply E over mc2 equals alpha L over two` | integrity-only |
| 24 | E = mc² ⇒ α⁻¹ = L/2, not L (§4.2) | the factor of two | `capacitor factor of two` (solves αL/2 = 1 → α = 2/L) | fresh |
| 25 | K = 137.035999171; 8 exp[−(K − 1)] = 6.65896×10⁻⁵⁹; 8 exp[−(2K − 1)] ≃ 2.03905×10⁻¹¹⁸ (§4.2) | the inserted cutoffs | no check. Archived: `microscopic.json` `CPF_cutoffs` and checks `CPF cutoff is inverse insertion of any desired number`, `CPF displayed approximate cutoff also disagrees numerically`, `self-energy matching requires inverse alpha L over two` | integrity-only |
| 26 | D = diag(1, −1), M = [[1, 2], [0, 1]], MD − DM = [[0, −4], [0, 0]] (§4.3) | deck-commutation failure of the proposed cover map | `cover shear fails necessary deck commutation` | fresh |
| 27 | metric determinant R² + p² cos²(u/2)/(4π²) (§4.3) | glide-compatible metric with free radius and pitch | no check. Archived: `microscopic.json` checks `printed metric respects the glide pullback`, `metric determinant retains an unfixed positive radius and pitch` | integrity-only |
| 28 | unit-integral transverse Gaussian of width ε has squared L² norm 1/(2√π ε) (§4.3) | surface kernel is not an L² volume state | no check. Archived: `microscopic.json` checks `normal Gaussian surface regulator has inverse-width squared norm`, `surface kernel is not an ordinary L2 volume state in zero-width limit` | integrity-only |
| 29 | ψ ↦ iψ preserves \|Dψ\|² (§4.4) | the real/imaginary split is not gauge invariant | no check. Archived: `microscopic.json` check `pi over two phase rotation preserves covariant kinetic density` | integrity-only |
| 30 | the supplied Bell state gives 2√2; a product state gives √2 (§4.4) | CHSH values | no check. Archived: `microscopic.json` checks `chosen Bell settings give two root two`, `same operators with product state do not give same Bell value` | integrity-only |
| 31 | the two-to-three coordinate map has rank two (§4.4) | rank of the hexagonal map | no check. Archived: `microscopic.json` check `hexagonal coordinates are rank two with a linear constraint` | integrity-only |
| 32 | (\|R⟩ + \|G⟩ + \|B⟩)/√3 is a vector in the triplet, not an invariant vector; all eight generators give a trivial common kernel (§4.4) | not a singlet | `triplet Casimir and no invariant vector` (the stacked eight generators have rank 3) | fresh |
| 33 | its two Cartan expectations vanish but the sum of their variances is 1/3 (§4.4) | zero mean charge is not invariance | `balanced triplet has zero means but nonzero variance` (asserts both means 0 and Σ var = 1/3) | fresh |
| 34 | quadratic Casimir 4/3 (§4.4) | fundamental Casimir | `triplet Casimir and no invariant vector` (Σ t² = (4/3)·I) | fresh |
| 35 | the triplet–antitriplet singlet is annihilated by the total generators (§4.4) | positive control | `tensor-product singlet positive control` | fresh |
| 36 | the antisymmetric three-triplet singlet is annihilated (§4.4) | second positive control | no check. Archived: `endpoint_audit/colour-singlet.json` check `three triplets have the expected antisymmetric singlet` | integrity-only |
| 37 | all 24 independent contortion components retained; K∧K and T∧*T algebraic in K (§5) | no independent contortion wave operator | no check. Archived: `microscopic.json` checks `torsion-contortion map has full 24-component rank`, `quadratic torsion term has no connection velocity kinetic matrix`, `quadratic torsion term is algebraic degree two in contortion`, `covariantly constant Palatini coefficient leaves derivative term as boundary` | integrity-only |
| 38 | 2ε/[(1/2 − β)² − ε²] equals −2/ε at β = 1/2, not zero (§6) | the CPF summand on the critical line | `CPF curvature summand is nonzero on the critical line` | fresh |
| 39 | finite-summand integration has a vanishing long-time average on- and off-line (§6) | the countercheck | no check. Archived: `microscopic.json` checks `actual finite critical-line summand time average vanishes`, `finite-summand primitive independently checked (0.5, 20.0)`, `(0.5, 200.0)`, `(0.73, 20.0)`, `(0.73, 200.0)` | integrity-only |
| 40 | "the complete real roots of the historical quartic proxy"; "the 68-component normalization and scale-family proof" (Appendix A) | pointers to the companion paper's results | the phase6 checks of Table 1 rows 39–44 and `exactly two real proxy roots`; Table 1 rows 1, 27–31 | fresh |

Table 2 counts: **fresh 10, integrity-only 29, none 1** (40 rows).

## Totals

| Class | Table 1 | Table 2 | Both |
|---|---|---|---|
| fresh | 27 | 10 | 37 |
| integrity-only | 19 | 29 | 48 |
| none | 0 | 1 | 1 |
| rows | 46 | 40 | 86 |

**Numbers with no coverage at all:** one. Table 2 row 21 — the statement that the torus curve
of the earlier framing note is a (2,1) embedding and an unknot. No verifier check and no
hash-checked record computes the knot type; the hashed physical report uses the (2,1)
centreline but does not classify it, and the `framed_unknot` instrument's outputs are tracked
under `docs/` but not in the manifest or the endpoint receipt.

**What the split means.** Of the 86 printed numbers, 37 would turn a PASS line red if they were
wrong. The other 48 are preserved, not reproduced: the integrity pass proves that the file that
states each one is byte-identical to the file sealed on 24 September, and nothing more. The
binding reference (Table 2 rows 4–12), the gauged point (rows 14–16), the radiated power
(row 13) and the carrier spectrum (rows 19–20) are entirely in that second class, as the
verifier's scope string says they are. Two of the integrity-only rows are recomputed by the
fresh run without being asserted (Table 1 row 34's middle λ_IR and row 43's root digits), so a
fresh assertion for them would cost one comparison each.

## Verifier checks that exercise no number printed in either paper

The two tables cite 53 of the 58 PASS lines. The five they do not cite assert quantities that
neither update paper prints: `normalization: bracket_is_symmetric_not_original_antisymmetric_generator`,
`normalization: third_order_symmetric_piece_nonzero` (the norm 128/9),
`normalization: projection_two_thirds_exact` (the projection 2/3),
`normalization: projected_norm_256_over_27` (256/27) and
`neutral: phase_tadpole_includes_CP_odd_coefficients`. The first four are the bracket algebra
behind the companion papers' normalisation; the fifth is the CP-odd tadpole of the neutral
family. They are evidence for the 24 September record, not for a number on these two pages.

## Appendix — the 58 PASS lines of this run

```
PASS 17 homogeneous quartics
PASS 4 homogeneous quadratics
PASS normalization: bracket_is_symmetric_not_original_antisymmetric_generator
PASS normalization: third_order_symmetric_piece_nonzero
PASS normalization: projection_two_thirds_exact
PASS normalization: projected_norm_256_over_27
PASS normalization: canonical_quartic_invariant_under_consistent_coordinate_change
PASS normalization: adjoint_commutator_drops_real_Delta_charge
PASS neutral: all_21_restrictions_match_independent_formula
PASS neutral: neutral_quartic_map_rank_11
PASS neutral: six_coordinate_invariants_invisible
PASS neutral: phase_tadpole_includes_CP_odd_coefficients
PASS neutral: four_invisible_norms_change_transverse_hessian
PASS neutral: holomorphic_terms_invisible_through_Hessian
PASS full stationary spectrum k=0.2
PASS tadpoles and Goldstones k=0.2
PASS coordinate invariance k=0.2
PASS full stationary spectrum k=0
PASS tadpoles and Goldstones k=0
PASS coordinate invariance k=0
PASS full stationary spectrum k=-0.2
PASS tadpoles and Goldstones k=-0.2
PASS coordinate invariance k=-0.2
PASS identical neutral Hessians across stability counterfamily
PASS independent finite-difference derivatives
PASS complex noncommuting flavor witness
PASS action dilation V, gradient, Hessian a=0.4
PASS gauge mass Gram dilation a=0.4
PASS 48-Weyl complex flavor dilation a=0.4
PASS action dilation V, gradient, Hessian a=2.3
PASS gauge mass Gram dilation a=2.3
PASS 48-Weyl complex flavor dilation a=2.3
PASS one-loop logarithm invariant under simultaneous scale change
PASS conditional source RG reaches UV
PASS perturbed boundary reaches IR -1e-05
PASS perturbed boundary reaches IR 1e-05
PASS finite running retains sensitivity
PASS phase6: source beta4 factorization
PASS phase6: nonzero w branch impossible over reals
PASS phase6: remaining beta3 factorization
PASS phase6: zero elimination reconstructs both original equations exactly
PASS phase6: zero all real roots isolated by exact Sturm count
PASS phase6: zero original residual 0
PASS phase6: zero independent numerical root 0
PASS phase6: zero original residual 1
PASS phase6: zero independent numerical root 1
PASS phase6: zero proposed Higgs number is not a proxy root
PASS phase6: nonzero elimination reconstructs both original equations exactly
PASS phase6: nonzero all real roots isolated by exact Sturm count
PASS phase6: nonzero proposed Higgs number is not a proxy root
PASS exactly two real proxy roots
PASS cover shear fails necessary deck commutation
PASS capacitor factor of two
PASS CPF curvature summand is nonzero on the critical line
PASS balanced triplet has zero means but nonzero variance
PASS triplet Casimir and no invariant vector
PASS tensor-product singlet positive control
PASS FLS negative control exact square completion
```

The archived [`science-report.json`](2026-09-24/science-report.json) lists the same 58 names in
the same order with `passed: true` on every row. The one evidence value it records that is also
printed in a paper, `finite running retains sensitivity`, came out as 0.20888981976663332 in this
run against the archived 0.20888981972361217: the two agree to 4.3×10⁻¹¹, both round to the
printed 0.2088898, and both sit inside the check's 10⁻⁶ tolerance. They are not identical, and
this page does not say they are.
