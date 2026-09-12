# Bounded adversarial review of the shear certificate

**Assessment at this checkpoint:** no remaining defect was found in the inspected final uniqueness and peak-refinement logic, conditional on the inherited unstable-spectrum theorem and analytic endpoint estimates. Exact parsing of recorded outward endpoints confirms the final continuum covers and refined signs. The independent whole-half-line Frobenius method has a different spatial computation and truncation proof. Its final global continuum output was still being produced at this checkpoint; that completed output was not yet accepted by this review.

This is a bounded mathematical/code review, not a full independent rerun of either interval propagator or a proof-assistant verification.

## Evidence examined

The reviewed workstream is the sibling shear directory. Main accepted files inspected:

- checks/uniqueness_certificate_final.py and attempts/uniqueness_certificate_final_20260911T222645920586Z/result.json, plus that attempt's outer_exclusion.json and curvature_cover.json.
- checks/peak_refinement_certificate_final.py and attempts/peak_refinement_certificate_final_20260911T222836459786Z/result.json.
- support/prior_validated_jost_hardened.py, support/curvature_jost_v2.py, support/frobenius_jost_v4.py, support/frobenius_tail_hardened.py, and the evolving final Frobenius/Cauchy audit.

The reviewer's checks/audit_shear_evidence.py parses serialized decimal balls with exact rational arithmetic, independently of Arb's parser. Its first successful checkpoint is outputs/audit_shear_evidence_20260911T223156940712Z.json. That output records SHA-256 hashes of reviewed result files. Earlier failed reviewer attempts remain: one exposed a local snapshot-path mistake in the reviewer, and the next exposed a still-lossy determinant display string.

## Problems found and disposition

1. **Old serialized positivity was not recoverable.** The prior stored global cover includes 557 accepted cells, but many determinants print as "[+/- ...]". These balls contain zero. The old archive cannot itself certify all its signs, regardless of the signs computed before serialization. Shear confirmed this with a failed audit and retained that failure.

2. **More midpoint digits did not completely solve this.** The final uniqueness attempt stores 132 explicit lower and upper endpoints, all adequate for the sign proof. However, one separate D_at_lower_growth display ball still contains zero because its radius has few significant digits. For the cell [1017691/2560000,509897/1280000], the midpoint is approximately 0.001657698 and displayed radius 0.00166; the separately stored lower endpoint is approximately \(3.88966\times10^{-6}>0\). The explicit endpoints are the sign evidence. A standalone gate using full midpoint/radius decimal integers was being added. This display limitation does not invalidate the explicit-endpoint certificate.

3. **The alternative continuum route imported an earlier bound implementation.** frobenius_taylor_v2.py imported frobenius_jost_v2, whose maxima compared overlapping bound balls. The final path uses hardened disk propagation that takes outward upper endpoints before maxima. Earlier runs remain superseded.

4. **The generic Frobenius contraction omitted a diagonal eigenvalue.** The limiting diagonal entries are \(\lambda=1/(1+i\eta)\) and \(1/2\), so the majorant needs \(\max(|\lambda|,1/2)+\epsilon\). The old implementation used \(|\lambda|+\epsilon\), although its general domain did not ensure \(|\lambda|\ge1/2\). The accepted shear range is safe: independently, on its complex disks,
   \[
   |\lambda|=\left|\frac{k}{k+is}\right|
   \ge\frac{c-r}{\sqrt{(c+r)^2+(s+r)^2}}>\frac12
   \]
   for \(c\ge0.19,r=0.02,s=0.19\). The final frobenius_tail_hardened.py nevertheless uses the correct maximum, fixing the generic formula too.

Each issue was sent promptly to shear and the parent. This reviewer changed no shear file.

## Interval rigor and derivative convention

Write \(F(k,s)=D(k,s/k)\), holding growth \(s\) fixed. The rescaled Jost potential is

\[
W(k,s,y)=\frac{kU''(y)}{kU(y)-is}.
\]

Independent symbolic differentiation verifies

\[
W_k=-\frac{isU''}{(kU-is)^2},\qquad
\frac12W_{kk}=\frac{isUU''}{(kU-is)^3}.
\]

These are the normalized coefficients used by curvature_jost_v2.py. Its parameter convolution includes the derivative of \(-2kv\), and its determinant convolution includes the derivative of the explicit factor \(k\). Twice the second normalized coefficient gives \(F_{kk}\). This is not differentiation at fixed phase-speed imaginary part.

The inspected Taylor architecture bounds each entire spatial step, bounds the six-component derivative system by Gronwall, and uses normalized interval jets for the Taylor integral remainder. Tail Cauchy estimates use a complex \(k\)-disk of radius 0.05 with positive real part and a lower bound for \(\Re(s/k)\). The Volterra majorant and Cauchy coefficient bounds are consistent with that domain. Rectangular complex enclosures are conservative.

This checks the formulas and implementation structure. I did not independently rerun every spatial step or verify Arb's arithmetic internals.

## Uniqueness and location

The inherited premises are substantial: one simple unstable eigenvalue for every \(0<k<1\); purely imaginary unstable phase speed for this symmetric profile; exact equivalence between the eigenvalue condition and the Jost zero; determinant continuity and positivity at large positive phase-speed imaginary part; and the endpoint estimates. They are accepted as named inputs here, not proved by the new cover.

Under those premises, uniqueness follows correctly. Two maximizing wavenumbers at the same growth \(s\) would be two zeros of \(F(k,s)\). Strict convexity makes \(F\) negative between them. A negative determinant lies below its unique simple zero, so an intermediate wavenumber would have greater growth: a contradiction.

The strong-convexity estimate

\[
F(k,s)\ge F(k_0,s)-\frac{|F_k(k_0,s)|^2}{2\mu}
\]

holds when \(F_{kk}\ge\mu>0\) and establishes the global growth upper bound. Differentiating the smooth simple-root branch \(F(k,g(k))=0\) gives \(g'=-F_k/F_s\); hence a stationary point satisfies \(F_k=0\). Opposite endpoint signs of \(F_k\), certified for every growth in the enclosure, localize the unique maximum. These derivative boxes are not just evaluations at estimated peak growth.

The exact-Fraction audit verifies:

- All 132 exterior cells have positive explicit lower endpoints and cover [0.1897,0.4] and [0.5,0.98] without gaps.
- All 50 curvature cells cover [0.4,0.5] × [0.1897,0.19] without gaps and have lower endpoints exceeding 0.18.
- Recorded strong-convexity margins are positive.
- Both final fixed-\(k\) root-bracket endpoints occur in the bisection history with the required opposite signs. The audit does not rely on the initial guessed bracket.
- Final derivative boxes have strict opposite signs.
- Decimal growth enclosures contain their exact rational bounds; wavenumber decimal endpoints equal the rational endpoints.

At the upper analytic endpoint,

\[
\frac{2(0.98)}{1+0.98}-0.98^2=\frac{7301}{247500}<0.1897^2.
\]

Its derivative is negative there and decreases thereafter. Howard's \(s\le k\) handles the low-\(k\) region; the inherited stable range handles \(k\ge1\). These analytic exclusions join the interval cover; the code does not numerically cover all \(k>0\).

## Independence of the Frobenius route

The coordinate \(t=1+\tanh y\) maps the entire left half-line to \(0<t\le1\). The recurrence computes its full-half-line Jost series, and a diagonal-basis transfer contraction bounds all omitted coefficients. The derivative tail correctly includes the weight \(n+\ell\). At \(t=1\), \(dt/dy=1\), so its derivative series gives the derivative required for matching.

The continuum enclosure first forms determinant Taylor coefficients, preserving cancellation, then adds a complex-disk Cauchy remainder. Conjugating coefficients is legitimate for the real-analytic determinant's holomorphic extension on a conjugation-symmetric disk. Spatial-tail error and parameter truncation are separate. The bound \(|k|\le c+r\) is appropriate on the Cauchy circle even though solution bounds use a containing square.

This shares the differential equation, spectral premises and Arb arithmetic with the Taylor-ODE route, but not its spatial cutoff, step propagation or truncation proof. The six point overlaps are finite consistency checks; by themselves they are not an independent global bound. A completed positive Frobenius/Cauchy continuum cover is required for that stronger claim.

## Remaining review boundary

The first checkpoint accepts the inspected conditional uniqueness/refinement chain and explicit-endpoint data. A finished independent global Frobenius cover was not yet present. The review does not reprove the inherited spectral classification, prove nonlinear instability, or interpret the nondimensional peak as a physical prediction without the original scaling assumptions.

## Completed-cover addendum, 2026-09-11 22:36 UTC

The pending final outputs arrived and passed the reviewer's exact rational parser. This addendum supersedes the pending-output limitation above.

- attempts/independent_global_certificate_final_20260911T223339581000Z/result.json contains 93 gap-free cells covering [0.19,0.98], each with a strictly positive full-precision serialized determinant and lower bound. The final code uses frobenius_jost_v4 and the generalized contraction formula. It reuses 68 finite-polynomial enclosure balls only after adding a complete newly computed hardened spatial/parameter remainder, and performs 25 full fresh evaluations. Reusing a ball enclosing the finite polynomial is valid even if its old extra error was insufficient: the added new full error establishes the required enclosure independently of that old error.
- attempts/serialized_records_gate_20260911T223339579146Z/result.json reconstructs all 132 exterior and 50 curvature records from their outward endpoints and serializes them with full midpoint/radius precision. All 182 normalized balls and lower bounds parse strictly positive under the independent Fraction-based parser. The earlier single loose display ball is therefore no longer the final standalone sign record.
- The completed reviewer evidence is outputs/audit_shear_evidence_20260911T223601327726Z.json. It retains SHA-256 hashes of all four reviewed result files.

**Final bounded disposition:** the inspected final artifacts support a conditional unique global maximum and its refined enclosure, plus a second continuum proof of the coarser growth upper bound 0.19 by a spatially independent Frobenius/Cauchy method. No unresolved mathematical defect was found within the reviewed scope. This acceptance continues to rely on the named inherited spectrum/endpoint theorems, the interval implementations and Arb; it is not an independent rerun of the full propagations.
