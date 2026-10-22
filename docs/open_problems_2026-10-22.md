# Open problems — state-of-the-problem cards (22 October 2026)

These cards are maps, not progress. Each one states an open problem in the
source's own words with a file:line, lists what the corpus has established
toward it and which check pins it, states the obstruction as the record states
it, names the smallest concrete next step, and reports any cheap check that was
run today with its command and number. Nothing on this page claims to advance
the theory. Line numbers refer to the files at commit `c3a383b`.

Cheap checks were run with the pinned Python (`numpy`, `mpmath` only), reading
the committed 100,000-ordinate table (`code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt`,
sha256 `4371e193…0415f8`, identical on `main` and on the PR #16 branch) and the
certified Dirichlet lists from the unmerged PR #16 branch. The scripts live
outside the repository; they write nothing into tracked paths.

## Riemann and spectral

### Card 1 — The Hilbert–Pólya operator (Frontier R06; Elimination Ledger Q5)

Candidate rows 10, 44, 93.

**(1) The open statement, in the source's words.**

- `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:1563`: "We have not constructed the Hilbert--Pólya operator."
- `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:1600-1605` (Open Problems, R06): "A natural operator needs a Hilbert space, domain, self-adjointness proof, and a complete link between its spectrum and $-i(\rho-1/2)$ for actual nontrivial zeros. An explicit full trace identity with justified tails could supply such a link; matching a finite list or its imaginary parts cannot."
- `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:1556-1558`: the Berry–Keating "$xp+px$ heuristic and other published proposals have not yet been tested against the full constraint set; doing so is a tractable open direction."
- `papers/core_trilogy/Spectral_Witness_Refinement.tex:351` (Not established): "any Hilbert--P\'olya operator (the wall is self-adjointness on a well-defined domain)".
- `papers/notes/Critical_Line_As_Fibered_Object.tex:248-250`: "What remains open is a natural operator, its domain and self-adjointness, and a complete identification of its spectral parameter with $-i(\rho-1/2)$ for actual zeta zeros."
- `docs/Elimination_Ledger.md:332`: "Q5 full HP operator | a candidate construction (open problem)"; `:235`: "full-operator search remains open, BLOCKED on a construction, not on data".
- `docs/frontier/2026-09-12-source-delta/Research_Queue.json` R06: `current_status` "open_theorem"; unchanged at the tip of the PR #16 branch (`2026-09-14-aggregate-source-constrained-delta/Research_Queue.json`, "carried_forward_not_newly_audited").

**(2) What the corpus has established toward it, and what pins it.**

- A constraint specification rather than an operator. `Riemann_Spectral_Critical_Line.tex:1540-1555`: the scorecard C1/C3/C5/C6 on four test spectra, in which "Only the actual Riemann zeros pass all constraints."
- Class kills (numerical, T3). `docs/Elimination_Ledger.md:207-235`: unfolded spacing selects the unitary class (GUE L2 distance 7.31e-2 against GSE 1.72e-1, GOE 2.26e-1; fitted repulsion exponent β = 2.12), which kills real-symmetric (GOE) and symplectic (GSE) candidates; bare $xp$ is "killed as sufficient" because its spectrum is continuous, while its smooth count matches the staircase (ratios 0.998 / 1.00001 / 0.99998 at T = 10³ / 10⁴ / 5·10⁴).
- The wall stated as numbers. `MANIFEST.md:86`: "Hilbert-Pólya wall quantified (constructs NO operator): any H with spectrum {γ} must carry real orbit amplitudes … AND GUE repulsion … simultaneously"; `MANIFEST.md:87`: the two constraints coexist under an anti-commuting antiunitary; "Class pinned; arithmetic realisation (orbits log p) remains open". Scripts: `code/hp_knife_suite/hp_operator_constraint.py`, `hp_wall_resolution_class.py`.
- Scoped operator results (R08/R10, both `closed_scoped_result` in the queue): the diagonal ordinate operator with an explicit self-adjoint domain, a trace-class subtracted resolvent and an explicit inverse-square tail. The source-delta README states the limit: the canonical Paper B code "explicitly constructs `diag(gamma)` for its resolvent check. That finite identity holds for any supplied spectrum and does not construct a natural operator or an infinite trace."
- Pytest pins (`code/acs_codebase/tests/test_paper_b.py`): `test_resolvent_identity_at_omega_50` (:29), `test_chi_diverges_near_zeros` (:35), `test_BK_matches_within_two_zeros_through_T_143` (:95), `test_BK_leading_form` (:102), `test_riemann_count_at_known_value` (:109). `code/publication_20260924/verify_science.py` carries no Paper B spectral check (grep for `paper_b|resolvent|delta_norm|riemann` in that file returns only unrelated `np.zeros` lines).

**(3) The obstruction, as the record states it.**

Self-adjointness on a well-defined domain (`Spectral_Witness_Refinement.tex:351`); a construction, not data (`Elimination_Ledger.md:235`); the two measured constraints "pull to opposite symmetry classes, which is why the problem is open" (`MANIFEST.md:86`). The symmetry-class kill itself "rests on RMT universality, not a theorem for ζ" (`Elimination_Ledger.md:221`). A finite spectral match cannot close it (`Riemann_Spectral_Critical_Line.tex:1602-1603`).

**(4) Smallest concrete next step.**

The paper's own unfilled row: run the existing C1/C3/C5/C6 battery (`Riemann_Spectral_Critical_Line.tex:1540-1555`) on the discrete spectrum of a published regularised $xp$ model (Berry–Keating with the $|x|\ge l_x$, $|p|\ge l_p$ cutoffs, or Sierra's boundary-condition version), using its known counting function to generate the first $10^4$ eigenvalues. Inputs: the 100k table for the truth row, the candidate's eigenvalue list; cost: minutes in numpy. Expected output: one more scorecard row (PASS/FAIL per column). This neither constructs nor kills the operator; it discharges the sentence at `:1556-1558`.

**(5) Cheap check run now.**

Smooth-count necessary condition reproduced on the committed table.
Command: `acs-venv/bin/python -I riemann_checks.py riemann_zeros_100k.txt pr16_dirichlet/` (check A) and `riemann_checks2.py` (check A').
With the 7/8 term, N_smooth/N_actual = 0.999409, 1.000095, 0.999997 at T = 10³, 10⁴, 5·10⁴ (N_actual = 649, 10142, 63519). Without the 7/8 term (the convention that reproduces the ledger's figures): 0.998060, 1.000009, 0.999983, matching `Elimination_Ledger.md:224-225` (0.998 / 1.00001 / 0.99998) to the printed digits. This is the necessary condition only.

### Card 2 — The bound $\Delta_{\mathrm{norm}}(u)=O(u^2)$ independent of RH (Frontier R04)

Candidate row 11.

**(1) The open statement.**

- `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:1594-1598`: "Classical equivalence, unresolved premise (R04). Theorem~\ref{thm:vonKoch-acs} gives the corrected RH-equivalent bound. Proving that bound independently of RH remains open. Finite-grid slopes, additional ordinates, and an envelope chosen with $\sigma=1/2$ do not discharge it."
- The theorem itself, `:437-444`: "For any fixed $u_0>0$, RH is equivalent to $\sup_{u\ge u_0}|\Delta_{\mathrm{norm}}(u)|/(1+u^2)<\infty$," with $\Delta_{\mathrm{norm}}(u)=(\psi(e^u)-e^u)/e^{u/2}$ (`:432`).
- Queue R04 (`docs/frontier/2026-09-12-source-delta/Research_Queue.json`): `current_status` "finite_source_overflow_fixed_arithmetic_normalization_bridge_open"; continuation "Specify the full arithmetic quantity, normalization, truncation and summation conventions and prove the bridge. Finite-grid slope tests and fixed-N bounds cannot discharge the infinite claim."

**(2) Established toward it.**

- The equivalence is proved in both directions in the paper (`:437-460`, classical reduction via von Koch and Schoenfeld); the conditional constant is sourced: "$|\Delta_{\mathrm{norm}}(u)|<u^2/(8\pi)$ for $e^u\ge73.2$" (`:472`, Schoenfeld 1976, Theorem 10, (6.2)); `code/acs_codebase/docs/ledger.md:82` records the same source.
- The finite object the code evaluates is separated from the arithmetic one: `:465-466` defines $D_N(u)$ with the fixed-$N$ bound $2\sum_k(1/4+\gamma_k^2)^{-1/2}$; the source-delta README records the overflow fix at $u=710$ and $1000$, the 46-case suite and a 70-digit cross-check agreeing "to better than `3e-13`".
- Pytest pins (`code/acs_codebase/tests/test_paper_b.py`): `test_truncated_delta_norm_grid_diagnostic` (:64), `test_delta_norm_avoids_intermediate_exponential_overflow` (:73, parametrised at u = 5, 700, 710, 1000), `test_off_critical_zero_diverges_faster` (:87).

**(3) The obstruction.**

By the paper's own Theorem (`:437-444`), an RH-independent proof of the bound is a proof of RH: the two statements are equivalent. The record therefore does not name a lemma short of RH; it names what does *not* count (`:1596-1598`). Unconditionally, the best known error term is of Vinogradov–Korobov type, $\psi(x)-x=O(x\exp(-c(\log x)^{3/5}(\log\log x)^{-1/5}))$, which in $u$-coordinates is $\Delta_{\mathrm{norm}}(u)=O(e^{u/2-cu^{3/5}(\log u)^{-1/5}})$, far from $O(u^2)$. (That comparison is this card's, not the paper's; it is the standard state of the art, cited here only to size the gap.)

**(4) Smallest concrete next step.**

There is no partial step toward the theorem that is not RH. The smallest *honest* step is editorial: the Open Problems paragraph could say in one sentence that, by Theorem `thm:vonKoch-acs`, R04 as stated is RH, so that the branch is not read as a tractable lemma. (The file is manifest-bound; this is recorded as a proposal, not an edit — see `docs/proposed_amendments_2026-10-22_pass2.md`, item 1.)

**(5) Cheap check run now (measurement only).**

Command: check C in `riemann_checks.py`. Sieve to $x=10^7$; over 4000 log-spaced $x\ge73.2$, $\max|\Delta_{\mathrm{norm}}(u)|/(u^2/8\pi)=0.8039$, attained at $u=4.564$ ($x\approx96$); at $x=10^7$, $\Delta_{\mathrm{norm}}=-0.4619$ against $u^2/(8\pi)=10.34$. This says only that Schoenfeld's conditional bound is not violated below $10^7$, which is already known at far larger heights; it is not evidence about the limit.

### Card 3 — The finite-to-infinite bridge (Frontier R04 / R05 / R08 / R10)

Candidate row 95.

**(1) The open statement.**

- `docs/frontier/2026-09-12-source-delta/README.md`: "The omitted infinite tail remains a separate obligation." and, under Continuation gates, the next inputs are "the truncation-to-arithmetic and natural-operator bridges".
- Queue R05: `current_status` "exact_obstruction"; "Finite boundedness and finite trace identities do not justify the unregularized infinite objects."; continuation "Prove uniform convergence or use an explicitly regularized observable."
- Queue R08 / R10 continuation: "A natural operator and its full zeta-zero spectral identification remain missing."

**(2) Established toward it.**

- Finite side, certified: at $N=100000$, $T=74921.378646477$, $\epsilon=10^{-4}$ the total deficit is enclosed by `[0.00509520994 +/- 3.39e-12]` (source-delta README; `Dataset_Audit.json`), "finite data-dependent enclosures conditional on the provider's input uncertainty, not asymptotic estimates."
- Regularised side, scoped: R08 and R10 are `closed_scoped_result` (paired observable realised as the trace of an explicitly subtracted trace-class operator; explicit inverse-square tail), on a *declared* diagonal spectrum.
- Smoothed bridge for one Dedekind zeta, unmerged: PR #16 branch `docs/frontier/2026-09-13-explicit-delta/README.md` — "The certified finite Q(zeta_5) spectra now agree with a declared explicit formula … with separate bounds on every omitted tail. … The unknown-zero bound allows zeros off the critical line and does not assume GRH." Largest final zero-tail bound below 6.6e-49; residual enclosures within ±7e-24; the moment beyond height 220 bounded by 0.050037848535216. Its own gate: "Taking a toward zero with fixed height 220 is not justified."
- Pins: `code/frontier_verification/verify_source_delta.py` (integrity only, "performs no downloads and does not rerun the mathematical commands" per `README.md:46`), `normalization_crosscheck.py`; `test_resolvent_identity_at_omega_50`.

**(3) The obstruction.**

The fixed-$N$ bound is not uniform in $N$ and is blind to arithmetic: "This fixed finite bound holds for arbitrary real input ordinates" (`Riemann_Spectral_Critical_Line.tex:468`); "Fixed-$N$ boundedness does not imply an infinite bound" (`:1586`). The PR #16 bridge is Gaussian-smoothed, for Q(ζ₅) only, and unmerged (`docs/BRANCHES.md:19`).

**(4) Smallest concrete next step.**

Apply the PR #16 Gaussian explicit-formula instrument to ζ itself: inputs already in the tree (`riemann_zeros_220_certified.txt`, 90 rows, on the PR #16 branch; prime powers to $10^5$), $h(t)=\exp(-at^2)\cos(ut)$ at the same $a\in\{1/25,1/100,1/400\}$ and frequencies, with the $s=2$ moment argument for the unknown-zero tail. Expected output: residual enclosures containing 0 and an explicit tail bound for ζ at height 220, i.e. the same smoothed bridge the branch has for Q(ζ₅). Cost: the branch reports 30 cases at 160/224 bits in minutes. This does not touch the unsmoothed limit (R05) or the operator (R06).

**(5) Cheap check run now.**

Command: check B in `riemann_checks.py`. The fixed-$N$ bound $2\sum_{k\le N}(1/4+\gamma_k^2)^{-1/2}$ on the committed table: 1.530369 (N=50), 4.641940 (10³), 8.587313 (10⁴), 13.987514 (10⁵) — growing, as expected for a sum of $1/\gamma_k$, so the finite bound cannot be passed to the limit as it stands.

### Card 4 — The arithmetic RH criterion bridge (acs_codebase ledger; FF06f amendment)

Candidate row 74.

**(1) The open statement.**

- `code/acs_codebase/docs/ledger.md:53`: "| Bridge from finite zero sums to a full arithmetic RH criterion | **Open** | Requires correct normalization, summation conventions, and truncation control | (open) |"; `:126`: "Finite-sum to arithmetic RH bridge (Paper B) — correct normalization, truncation control, and converse hypotheses remain open".
- `papers/methodology/Prime_Carrier_Position_Form_Factor.tex:161` (24 Sept amendment): "Extending the result to an infinite zero sum requires convergence control beyond correlation."

**(2) Established toward it.** As Card 3 (2); plus `ledger.md:46-47` (the finite bound "Applies to arbitrary real ordinates; does not establish an RH-wide arithmetic bound"; the σ=0.7 toy term has "no infinite-sum cancellation/converse theorem").

**(3) The obstruction.** The three named conventions (normalisation, summation, truncation) are not written down in one place in the canonical code, and the converse direction (from the finite sum to RH) has no hypothesis under which it holds (`ledger.md:126`).

**(4) Smallest concrete next step.** Write the three conventions as one displayed identity and cite the classical theorem that supplies the truncation control: unconditionally, $\psi(x)=x-\sum_{|\gamma|\le T}x^{\rho}/\rho-\log 2\pi-\tfrac12\log(1-x^{-2})+O\!\left(x\log^2 x/T\right)$ (Davenport, *Multiplicative Number Theory*, ch. 17), so that $\Delta_{\mathrm{norm}}(u)=D_N(u)+R_N(u)$ with the symmetric-in-$\pm\gamma$ convention and $|R_N(u)|\le C\,e^{u/2}u^2/\gamma_N+O(e^{-u/2})$. This makes "truncation control" a cited theorem and shows explicitly why fixed $N$ cannot bound the limit: $N$ must grow with $e^{u/2}u^2$. The converse hypothesis stays open (it is RH, Card 2).

**(5) Cheap check run now.** Command: check F in `riemann_checks2.py` (sieve to $10^6$; $N=100000$, $\gamma_N=74920.8$). $\Delta_{\mathrm{norm}}(u)-D_N(u)$ = −0.0580, −0.0182, −0.0042, −0.0050 at $x=10^3,10^4,10^5,10^6$; the classical scale $e^{u/2}u^2/\gamma_N$ = 0.0201, 0.1132, 0.5595, 2.5476. At $x=10^3$ and $10^4$ the residual equals the omitted constant term $-\log(2\pi)/\sqrt{x}$ (−0.0581, −0.0184) to three decimals, i.e. the term the paper says the routine omits (`:469`); by $x\ge10^5$ the truncation scale dominates the budget. Measurement at one $N$; no inference about the limit.

### Card 5 — Paper B replacement observables and conventions (Frontier R03)

Candidate row 12. Four definitional sub-items, all in `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`.

**(1) The open statements.**

- (a) Stability ratio, `:378-385`: "The earlier claim that this ratio vanishes on the critical line is false (Frontier R03). … A replacement observable must be defined and justified separately; this revision does not silently change the old ratio into an excess-amplitude ratio." Queue R03: `exact_obstruction`, continuation "Choose and justify the intended stability diagnostic."
- (b) Prefactor, `:810-811`: "A fitted prefactor and a precise centered-versus-uncentered observable must be specified before asserting the former $2\%$ agreement."
- (c) Injection convention, `:1020-1029`: "At $\sigma=1/2$ its envelope factor is one, not zero. Also, if $x$ denotes logarithmic coordinate, the actual explicit-formula envelope is $e^{(\sigma-1/2)x}$, not $x^{\sigma-1/2}$. The table preserves the reported numbers without treating this definition mismatch as resolved."
- (d) Transfer entropy, `:390-393`: "Identifying a bounded-variance diagnostic with transfer-entropy balance $\DI=0$ additionally requires a specified stochastic process, history sigma-algebras, lag, and measure; that identification is not proved here."

**(2) Established.** The R03 counterexample (ratio strictly positive on the line, `:375-377`); `docs/Elimination_Ledger.md` Q4 names $\Delta I=\mathrm{TE}(F\to G)-\mathrm{TE}(G\to F)$ but supplies no process for the prime–zero sequences; the historical tables are retained as reported (`:800-806`, `:1030-1036`).

**(3) The obstruction.** Definitional, not computational: each sub-item waits on a declared definition that the paper refuses to introduce silently.

**(4) Smallest concrete next step, per sub-item.** (a) Declare $\rho_{\mathrm{exc}}=\delta_N\max_k|A_k|\,(X^{|\sigma_k-1/2|}-1)/\sum_j|A_j|$ as a *new* observable (zero on the line by construction), and state that it carries no threshold claim. (b) Regress the retained comparator column on $\log X$ and print the fitted prefactor (see (5)). (c) Rerun the injection with the envelope $e^{(\sigma-1/2)x}$ in log coordinates and re-tabulate the four slopes. (d) Declare one process (e.g. unfolded zero spacings and normalised prime gaps as two stationary series, lag 1, Gaussian TE estimator) and compute $\Delta I$ under that declaration only.

**(5) Cheap check run now.** Command: check D in `riemann_checks.py`. The retained comparator column divided by $X^{0.2}$: 1.0829, 1.0851, 1.0841, 1.0840 at $X=10^2..10^5$. The column is consistent with $c\,X^{0.2}$, $c\approx1.084$, constant to the third decimal — i.e. a fitted prefactor, which is what `:810-811` says must be specified.

### Card 6 — The seam reading of the critical line (fibered-object note)

Candidate row 64.

**(1) The open statement.** `papers/notes/Critical_Line_As_Fibered_Object.tex:83-85`: "An additional carrier would need an explicit mathematical definition, a map to the observed coordinates, and a proof that the map preserves the asserted structure."; `:118-121`: "Describing it as a seam of a richer object requires an additional construction; neither a shadow nor a gluing map is supplied here."; `:81`: "This note's seam is an organising conjecture."

**(2) Established.** The two-face table (`:98-108`, Euler product vs Hadamard product, linked by the explicit formula and "tested numerically on a finite zero table", `:116-117`); the vantage-point census (`MANIFEST.md`, `hp_vantage_points.py`: two function faces, arithmetic ~830σ and local-order ~26σ). Nothing beyond the note: a grep for `gluing map|fibered object|seam law` outside the note hits only frontier event logs, the branch catalog, `papers/README.md`, `The_Geometry_Engine.tex` and the August editorial audit (12 files), none of which defines a carrier.

**(3) The obstruction.** No candidate carrier is named anywhere in the tree. The set $\mathrm{Re}(s)=1/2$ "remains one-dimensional" (`:119`). The one cited supporting experiment, `docs/witness_perspective/` (`:86`), does not exist in the repository (`ls` fails).

**(4) Smallest concrete next step.** Two, in order. (i) Clerical: repair or remove the dangling `docs/witness_perspective/` reference (manifest-bound file; proposal in `docs/proposed_amendments_2026-10-22_pass2.md`, item 2). (ii) Mathematical: name the carrier as a definite object — the natural candidate already in the note is the Weil explicit-formula pairing $\langle h,\Lambda\rangle$ between test functions on the zero side and the prime-power measure — and state the lemma to attempt: *the two "seam-law" statistics (arithmetic face, local-order face) are functionals of that pairing alone.* If true, the seam is a restatement of the explicit formula and the note's "richer object" claim reduces to it; if false, the residual is the carrier the note is missing. Inputs: the existing `hp_vantage_points.py` statistics and the explicit formula; cost: a derivation, then one script run.

**(5) Cheap check run now.** Only the greps and the `ls` above; no numeric check applies.

### Card 7 — L-function extension: S₄ Artin-L zeros and "boundedness of C" (Witness §10; Corpus Map O-4; Frontier R12/P05/R07) — VERIFY attempt

Candidate rows 21, 94.

**(1) The statement to verify, in the source's words.**

- `papers/core_trilogy/Spectral_Witness_Refinement.tex:290`: "**Falsifiable:** $S_4$ Artin-$L$ zeros to height $\sim5000$, test boundedness of $C$."
- The object, `:267`: "For the windowed observable $F_w=K_w[\rho]+E_w$ with $\|E_w\|=O(1/N)$, prior work conjectured the implied constant uniform in $(\rho,q,d)$."; `:269`: "The constant $C(\rho,q,d)=\|E_w\|\cdot N$ is controlled only above a height floor" $T_{\min}(d,q)=(2\pi e)^d/q$; `:284`: "$3$ & $S_4$ & $4{,}982$ & open --- gated".
- The windowed observable, `:76-79`: $F_w(\omega)=\frac{1}{W}\sum_k w(\gamma_k)\,e^{-i\omega\gamma_k}$.
- `docs/ACS_Corpus_Map.md:141`: "| O-4 | L-functions extension | LMFDB zeros | Paper B generality |"; `docs/ACS_FRAMEWORK_SKILL.md:147`: O-4 "remains **open with partial repo-resident progress**".
- Rows 94: the R12 contract (source-delta README): "each ordinate interval must lie entirely on one side of the selected endpoint, with finer evaluation when that fails. For shrinking resolution, uncertainty relative to resolution must also be controlled."

**(2) Established toward it.**

- The gate premise is dead. `docs/Elimination_Ledger.md:428-456`: the scaling law $T_{\min}=(2\pi e)^d/q$ is "**FALSIFIED (T4)** in its degree dependence" at $d=2$ (Dedekind ζ of Q(i): framework floor 72.93 "sits **above 51 actual zeros**"); "the floor scales as 2πe·q^(−1/d) (standard), not (2πe)^d/q". For $S_4$, $d=3$, $q=229$ the corrected floor is $2\pi e\cdot229^{-1/3}=2.79$, not 4,982: the "height ∼5000" target is an artefact of the falsified law. Queue R07 (PR #16 tip): "A claimed finite uniformity threshold still needs an independent error theorem."
- Certified degree-1 inputs exist, unmerged. PR #16 branch `docs/frontier/2026-09-13-lfunction-delta/README.md`: "certifies 794 distinct simple zeros for seven specified Dirichlet characters in finite rectangles" by a whole-contour interval count (argument principle; `code/frontier_verification/LFUNCTION_README.md:27-34` on that branch); manifest `code/hp_knife_suite/data_zeros/LFUNCTION_CERTIFICATES.json` (absent on `main`). "No Artin/S₄ zeros anywhere" in the tree; `code/hp_knife_suite/data_zeros/cyclotomic_5/cyclotomic_synthesis.md:121` still names non-abelian Artin L-functions as "the next structural extension".

**(3) Why the statistic could not be computed — and what was found instead.**

*The definition is not precise enough to compute.* The paper gives $C=\|E_w\|\cdot N$ with $E_w=F_w-K_w[\rho]$, but defines neither $K_w[\rho]$ (the smooth kernel applied to the density), nor the window $w$ and its normalisation $W$, nor the norm $\|\cdot\|$ (sup over which $\omega$ range, or $L^2$), nor whether $N$ is the zero count below the cutoff. `K_w` and `E_w` occur nowhere else in the tree (grep over `papers/`, `docs/`, `code/`: only `:267` and `:269`), and the reproducible driver (`:447-449`, "R7 floor") computes only $T_{\min}$, not $C$. Any value of $C$ reported today would be this card's reconstruction, so none is reported.

*LMFDB access, as observed (22 October 2026, through the session proxy).*
- The Artin representation exists: `https://www.lmfdb.org/ArtinRepresentation/3.229.4t5.a.a` — Galois group $S_4$, dimension 3, conductor 229, root number 1, defining polynomial $x^4-x^3+1$ (fetched and read). Its page exposes no L-function link and no zeros.
- `https://www.lmfdb.org/api/` answers JSON and lists `lfunc_lfunctions`, `lfunc_instances`, `artin_reps` collections. Queries `artin_reps/?Dim=i3&Galn=i24`, `lfunc_lfunctions/?degree=i3&conductor=i229` and `lfunc_instances/?url=sArtinRepresentation/3.229.4t5.a.a` all returned `"data": []` — well-formed but empty; the field names were guesses from the API index, so this is inconclusive about the database, not a negative.
- L-function search pages `/L/?degree=3&conductor=229` and `/L/?degree=3&origin=Artin` returned "No matches"; label guesses under `/L/3/229/…` returned 404.
- `/L/download_zeros/<label>` is the documented zero-list route (seen for other labels in search results). Every `curl` to lmfdb.org, and every browser-fetch after the first six, was served a reCAPTCHA interstitial ("Checking your browser before accessing www.lmfdb.org"), so no zero list was downloaded. The folder `scratchpad/actionable2/lmfdb/` therefore holds no LMFDB file.

*Fallback computed on the certified degree-1 lists (PR #16 branch).* Command: check E in `riemann_checks.py`. For each certified list, the count below its certified cutoff against the standard main term $\frac{T}{2\pi}\log\frac{qT}{2\pi e}$: χ₅ (q=5, T=220) 146 vs 145.84; χ̄₅ 146 vs 145.84; χ₇ (q=7, T=220) 157 vs 157.62; χ̄₇ 158 vs 157.62; χ₋₃₅ (T=80) 65 vs 64.93; χ₋₉₁ (T=60) 55 vs 55.07; χ₋₁₀₄ (T=70) 67 vs 67.46. All seven within ±0.62 of the main term. At $d=1$ the framework floor and the standard floor coincide (`Elimination_Ledger.md:448-450`), so these lists cannot test the floor law; the check only confirms the certified counts track the main term at their cutoffs.

**(4) Smallest concrete next step.** Two inputs, in order. (i) Declare the statistic: fix $w$ (the paper's Hann taper, `:88-89`), $K_w[\rho]$ as the windowed transform of the smooth density $\bar\rho(t)=\frac{d}{2\pi}\log\frac{q^{1/d}t}{2\pi e}$, the norm as $\sup_{0<\omega\le\omega_{\max}}$, and $N=N(T)$; then $C(T)=N(T)\sup_\omega|F_w-K_w[\rho]|$ is computable from any certified list. (ii) Obtain a certified $S_4$ list: either the LMFDB zeros for `3.229.4t5.a.a` once the download route is reachable (an interactive browser session, or a request not routed through the agent proxy), or compute them with the PR #16 method extended to degree 3 (needs the Euler factors of $L(s,\rho)$ from Frobenius cycle types, available on the Artin-representation page, and an Arb/FLINT contour count). Given the corrected floor of 2.79, a list to height 100–200 (order $10^2$ zeros) is enough to place the $d=3$ point on the floor-law table; "boundedness of $C$" as $N\to\infty$ additionally needs the scaling in $N$, which no finite list settles.

**(5) Needs line.** Missing: a certified ordinate list for one $S_4$ Artin L-function (conductor 229 is the smallest), from LMFDB (`/L/download_zeros/<label>` for the L-function instance of `ArtinRepresentation/3.229.4t5.a.a`) or from an Arb-based recomputation, with the R12 precision record (interval per ordinate, whole-contour count). And: a one-paragraph declaration of $K_w$, $w$, $\|\cdot\|$ in the Witness paper (manifest-bound; proposal in `docs/proposed_amendments_2026-10-22_pass2.md`, item 3). With both, the $d=3$ row of the floor-law table and a first value of $C(T)$ become computable in minutes.

### What this pass left out

- No Lean, Arb or FLINT runs; the pinned venv has `numpy`, `scipy`, `sympy`, `mpmath` only.
- No recertification of any ordinate; the 100k table and the PR #16 lists were used as supplied.
- No LMFDB file was obtained; the attempt is recorded above with each response as observed.
- Scale reached: sieve to $x=10^7$ (Card 2) and $10^6$ (Card 4); $N=10^5$ zeros; seven certified Dirichlet lists of 55–158 zeros.
