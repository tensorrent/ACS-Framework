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

## Palatini and the Standard Model

**Measurement frame for this section.** Line numbers are against the tree at `58f494c` (`git -C /home/user/acs-framework rev-parse --short HEAD`); the cards were prepared on `01a210e`, and `git diff --stat 01a210e 58f494c` over every file cited here shows one change, `code/capacitance_ribbon/ribbon_capacitance.py` (+10/−1, hunks at lines 17 and 671), which shifts its cited function by one line; all other citations are unchanged. Every number came from a command run on 22 October 2026 with the pinned interpreter (`acs-venv/bin/python`, numpy/scipy/sympy/mpmath); the scratch scripts are named per card and were run from a scratchpad directory, writing to stdout only (`git status --short` in the worktree showed no stray files after each run). "Paper A" is `papers/core_trilogy/Palatini_Gauge_Attractor.tex`; "FF" is `papers/Form_Function_and_Asymmetry.tex`; "SWR" is `papers/core_trilogy/Spectral_Witness_Refinement.tex`; "the queue" is `docs/frontier/2026-09-12-source-delta/Research_Queue.json`; "the ledger" is `docs/Elimination_Ledger.md`. The verifier is `code/publication_20260924/verify_science.py`, whose 18 named checks (58 rows with the parameterised ones expanded) were run through a stdout-only wrapper: `TOTAL 58 PASSED 58 elapsed_s 1.3`. Where a physical formula or input is not in the corpus it is marked **from memory** and is orientation only.

---

### Card P1 — Higgs kinetic normalisation chain and the 0.85% residual (candidate 13)

**(1) Open statement.** Paper A lines 2026–2033: "The remaining step is to derive the precise normalisation chain from the $\mathfrak{sl}(4)$ Killing form to the canonical Higgs kinetic term --- a standard but non-trivial matching that accounts for the $0.85\%$ residual. Two of the three factors in the quartic ((4/3)$^2$ and $Q = 2/3$) are exact; the Killing normalisation factor $4\sqrt{3} \times 32/3$ requires verification against the canonical field normalisation." SWR line 321: "The $0.85\%$ is \emph{not} derived here. What is established is its character: EW-scale, tree/threshold-level, $\sim1\%$, not running, not high-scale. Closing it requires the explicit canonical normalisation of the Higgs kinetic term emerging from the $\mathfrak{sl}(4)$ projection --- an analytic QFT calculation, not a numerical check." SWR line 317: "whose precise mechanism (threshold vs.\ wavefunction normalisation) remains underived"; SWR line 351: "the explicit value of the $\sim1\%$ Higgs-quartic kinetic normalisation (its character is pinned, its value is not derived)". Paper A line 2357: the $m_H$ "pull ($3.2\sigma$) traces to the incomplete normalisation chain".

**(2) Established.** The arithmetic of the chain as stated is internally consistent: Paper A lines 1998–2004 give $\lambda_{\mathrm{proj}} = \tfrac{2}{3}\times\tfrac{128}{9} = \tfrac{256}{27}$ and $K(T_{B-L},T_{B-L}) = 8\,\mathrm{Tr}(T_{B-L}^2) = \tfrac{32}{3}$, and dividing $\lambda_{\mathrm{proj}}$ by the paper's factor $4\sqrt3\times 32/3$ reproduces the boxed $2\sqrt3/27$ exactly (check (5) below). SWR line 312 pins the *character* of the residual: the one-loop SM quartic "crosses $\lambda_{\text{ACS}}=0.1283$ exactly once, at $\mu\approx132$~GeV", so the residual is an EW-scale normalisation offset, not running. The endpoint audit fixes the convention the derivation would have to use: `docs/condensate_energy/endpoint_audit/README.md` lines 88–90, "The correct radial identity is h=√Z r and λcanonical=4c₄/Z² for the convention V=c₄r⁴=λcanonical h⁴/4. Consistent coordinate changes preserve this result; an undetermined common action prefactor remains physically relevant." Verifier checks that pin the surrounding algebra: `17 homogeneous quartics`, `4 homogeneous quadratics`, `one-loop logarithm invariant under simultaneous scale change`, `exactly two real proxy roots` (all PASS in the 58/58 run). The same audit (lines 93–95) shows that a running proxy does not supply the match either: "Setting the upper-scale quartic to 2√3/27 produces a lower-scale quartic **0.1806315**, not its comparison input 0.1294. The resulting tree mass proxy is about **148 GeV**"; and lines 119–121: the two real proxy roots are (λ₁,λ₂) ≈ (0.1811535, 0.5106919), (0.6447133, 0.5764245) and "Neither gives 2√3/27."

**(3) Obstruction.** Queue S06 "Gauge and scalar normalization", status `exact_obstruction`: "Algebraic charge gaps do not fix canonical physical coupling values." Continuation: "Supply a normalized action and a scale-specific matching condition." The Higgs kinetic term whose normalisation $Z$ would convert $\lambda_{\mathrm{proj}}$ into $\lambda_{\mathrm{canonical}}$ is not written anywhere in the tree; the factor $4\sqrt3\times32/3$ is asserted, not derived from a kinetic term.

**(4) Smallest next step.** A lemma, not a calculation campaign: write the bi-doublet kinetic term $Z\,\mathrm{Tr}(D_\mu\Phi)^\dagger D^\mu\Phi$ in the *same* generator normalisation that produced $\lambda_{\mathrm{proj}} = 256/27$ (the $T_{B-L}$ and Lorentz-sector generators of `higgs_potential.py`, Killing form $K = 8\,\mathrm{Tr}$), read off $Z$, and compute $\lambda_{\mathrm{canonical}} = \lambda_{\mathrm{proj}}/Z^2$ by the audit's radial identity. Inputs: the explicit $4\times4$ generators already in `code/acs_codebase`; expected cost: one page of algebra plus a 30-line sympy script. The result is decisive either way: either $Z^2 = 4\sqrt3\times32/3$ falls out (closing the "requires verification" sentence) or it does not (and the boxed value loses its "every factor is algebraic" status). The step does *not* decide the 0.85%: that needs the "scale-specific matching condition" S06 asks for.

**(5) Cheap check run now** (`acs-venv/bin/python -I scratchpad/actionable2/higgs_chain_check.py`, sympy):
- $\mathrm{Tr}(T_{B-L}^2) = 4/3$ with $T_{B-L} = \mathrm{diag}(1/3,1/3,1/3,-1)$, so $K = 8\,\mathrm{Tr} = 32/3$ (paper: 32/3). $\lambda_{\mathrm{proj}}/(4\sqrt3\cdot 32/3) = 2\sqrt3/27$ exactly (`True`), $= 0.128300$.
- $\lambda_{\mathrm{SM}} = m_H^2/(2v^2) = 0.129383$ with the paper's inputs (125.25, 246.22); residual $(\lambda_{\mathrm{SM}}-\lambda)/\lambda_{\mathrm{SM}} = 0.837\%$ (the paper rounds to 0.85%).
- $m_H^{\mathrm{pred}} = \sqrt{2\lambda}\,v = 124.724$ GeV (paper: 124.7). Pull against 125.25 ± 0.17 is 3.09σ with the unrounded value (the paper's 3.2σ uses 124.7); against the PDG-2024 value 125.20 ± 0.11 (**from memory**) it is 4.32σ.
- The wavefunction factor that would absorb the whole residual is $Z = \sqrt{\lambda/\lambda_{\mathrm{SM}}} = 0.99580$, i.e. a 0.42% kinetic-term renormalisation. This is the *size* of what step (4) has to produce; it is not evidence that it does.

---

### Card P2 — The Standard Model from GL(4) and Conjecture gl4-precise (candidates 17, 58)

**(1) Open statement.** Paper A lines 1446–1452: "Four further claims are required to complete the SM generation conjecture, and all four remain open: ... (i) Unification of the two sources. The colour and electroweak factors arise from different parts of the geometry. A unified derivation from a single ACS structure on $\mathcal{Y}^{14}$ has not been achieved." Lines 1532–1550 state the replacement conjecture: "\begin{conjecture}[Precise GL(4) generation]\label{conj:gl4-precise} ... Determine whether there exists a vacuum configuration and symmetry-breaking pattern such that the residual gauge algebra equals $\mathfrak{su}(3) \oplus \mathfrak{su}(2) \oplus \mathfrak{u}(1)$ ... This is decidable by an explicit $\sim\!10$-page computation in Lie theory. It constitutes the remaining open problem of the programme, and the answer --- whether a proof or a no-go theorem --- is informative either way." FF carries the identical conjecture at lines 1888–1906. FF lines 2127–2133 state the other open step: "The single remaining open step is the \emph{dynamical identification}: showing that the torsion-induced spinor bundle's $\gamma^5$ operator, when restricted to the fiber algebra via the vierbein soldering form, reproduces the chirality map ... ($\sim\!3$ pages of spinor geometry)". Further inputs the bracket does not derive: Paper A line 556, the BCH–TE morphism on the Palatini field space "is conjectured but not proved"; lines 1173–1176, "compactness itself is a physical input ... The bracket algebra does not derive unitarity; it is imposed"; lines 1328–1331, "The chirality of $\mathrm{SU}(2)_L$ (the $V{-}A$ structure) requires the spinor bundle, which is a physical input (unitarity/compactness), not derived from the bracket alone." `papers/core_trilogy/Holographic_Spectral_Inversion.tex` lines 775–776: "Not yet: a field-theoretic derivation showing that the BCH orders map to distinct fermion families in the quantum theory."

**(2) Established.** Claim (iii) is marked resolved in Paper A lines 1461–1489: one full SM generation with "All 8~electric charges and all 8~hypercharges match the SM exactly (verified: \texttt{fermion\_reps.py})" (line 1485–1486). Lines 1492–1495: Jacobi closes the BCH algebra at order 3 "(verified: $\|\mathrm{Jacobi}\| = 6 \times 10^{-15}$)". Verifier checks on the colour triplet structure: `balanced triplet has zero means but nonzero variance`, `triplet Casimir and no invariant vector`, `tensor-product singlet positive control` (PASS, 58/58 run). Queue G06 (`exact_result`): "The Lorentzian star plus gamma-inverse map is invertible for real nonzero gamma and singular at gamma=+i,-i."

**(3) Obstruction.** Queue A09 "Three directions imply three generations", `exact_obstruction`: "The three Ei4 directions form one color triplet; arbitrary repeated family multiplicity preserves the cubic identity." Continuation: "Supply a generation-counting mechanism independent of color dimension." This is a direct obstruction to claim (iii-b) (Paper A lines 1491–1497, "Each BCH order generates one copy of the fermion representation, giving exactly three generations"). Queue G05 (`needs_definition`): "Identical internal grading is compatible with inequivalent differential principal symbols and arbitrary mass parameters"; continuation: "Supply spacetime/soldering, full action, normalization, constraints, states and continuum limit; internal grading alone does not select them." `docs/publication/2026-09-24/amendments.json` line 88: "The algebraic closure calculations do not establish a unique microscopic dynamics."

**(4) Smallest next step.** The conjecture's own "$\sim$10-page computation" has a zero-th page that is cheap and decisive about *how it must be set up*: over $\mathbb{R}$, $\Phi(v) = [e(v),\omega(v)]$ takes values in $\mathfrak{sl}(4,\mathbb{R})$, whose maximal compact subalgebra is $\mathfrak{so}(4)$ (dimension 6), so the 12-dimensional compact target $\mathfrak{su}(3)\oplus\mathfrak{su}(2)\oplus\mathfrak{u}(1)$ cannot be a subalgebra of the real image; the conjecture is only meaningful after the chirality map $J$ (Paper A Prop. chirality) complexifies. The concrete next step is therefore: (a) fix the complexified target $J(\mathfrak{sl}(3,\mathbb{R}))\oplus\cdots\subset\mathfrak{sl}(4,\mathbb{C})$ explicitly; (b) parametrise $(e,\omega)$ as a pair of linear maps $\mathbb{R}^{14}\to\mathfrak{gl}(4)$ (a $2\times14\times16 = 448$-parameter family modulo $GL(4)$ conjugation) and write the condition "span of $J\Phi$ equals the target" as polynomial equations; (c) compute the dimension of the solution variety with a Gröbner/numerical-algebraic-geometry run. Expected cost: the generic case is a one-line rank computation (done below); the non-generic locus is a polynomial-system computation of moderate size (448 unknowns, equations of degree 2 in $(e,\omega)$) that should be scaled down first to a sub-fiber. A no-go would be: the locus where the image is 12-dimensional and closed has the wrong Lie type for every vacuum.

**(5) Cheap check run now** (`acs-venv/bin/python -I scratchpad/actionable2/gl4_span_check.py`, numpy, seed 0): for 20 random pairs of linear maps $e,\omega:\mathbb{R}^{14}\to\mathfrak{gl}(4,\mathbb{R})$ the span of $\{\Phi(v)\}$ has dimension **15** in every trial (= all of $\mathfrak{sl}(4,\mathbb{R})$). So "the residual gauge algebra equals the SM algebra" is a *non-generic* condition on the vacuum, i.e. the conjecture is a question about a proper subvariety of field configurations, not about the generic point. This does not touch the conjecture's truth value.

---

### Card P3 — Pati–Salam vacuum alignment: CKM, Koide $\theta_0$, PMNS $\theta_{23}$ (candidate 18)

**(1) Open statement.** Paper A lines 2481–2482: "the precise Wolfenstein parameters require the full vacuum alignment in the Pati--Salam sector, which is not yet computed." Lines 1513–1515: "The \emph{exact} value of $\theta_0$ depends on the physical vacuum direction in the $\mathrm{GL}(4)$ fiber (the electroweak symmetry-breaking VEV), which the ACS framework does not yet determine." Lines 2549–2551: "TBM gives $\theta_{23} = 45^\circ$ (obs: $49.2^\circ$, gap $4.2^\circ$); the deviation requires a higher-order correction or renormalisation group running from the PS scale to low energy." Lines 2354–2356: "The $\theta_{13}^{\mathrm{PMNS}}$ prediction ($9.216^\circ$ vs.\ $8.57^\circ$, 5.4$\sigma$) is the weakest match". The App. C attempt, lines 2584–2586: "\subsection*{Result: $V_{\mathrm{CKM}} = \mathbb{1}$} The computation yields an identity CKM matrix and zero CP phase."

**(2) Established.** Koide ratio $Q = 0.666661$ versus $2/3$ (Paper A line 1502) and $\theta_0 = 12.73^\circ$ from the sym/anti ratio across BCH orders (lines 1505–1511); PMNS $\theta_{12} = 32.4^\circ$ vs $33.4^\circ$ and $\theta_{13} = 9.2^\circ$ vs $8.6^\circ$ (summary table lines 2508–2509). Paper A lines 2474–2478 already record that mass-ratio textures undershoot: "a Fritzsch texture gives $|V_{us}| \approx 0.05$ (too small); the empirical Fritzsch formula ... is closer but 19\% off the observed $0.2245$." App. C's own diagnosis of $V_{\mathrm{CKM}}=\mathbb{1}$ (lines 2589–2599): "(ii)~Both up-type and down-type matrices share the \emph{same} BCH texture (same $\varepsilon$, same bracket structure), so their diagonalising matrices are nearly identical". Verifier: `complex noncommuting flavor witness` (PASS). Queue F04 (`needs_definition`): "Exact d log Q/dt and sharp anomalous-dimension range bound are derived".

**(3) Obstruction.** Queue F01 "Yukawa ratio and CKM structure", `exact_obstruction`: "A literal matrix lock h_tilde=(2/3)h aligns Mu and Md; independent matrices reconstruct arbitrary masses." Continuation: "Specify the channel-to-matrix map or a texture-generating mechanism." Queue S20 (`closed_scoped_obstruction`): "Nonzero cubic alignment defect excludes constant 2/3 as a protected leading relation in formal perturbation theory." F04 continuation: "Predictive mass texture, scale and matching prescription remain required; prior S20 exclusion unchanged." Endpoint audit line 103: "square-root mass texture is rank one, leaving degenerate zero-mass subspaces". In short: the alignment that makes the framework predictive forces $V=\mathbb{1}$; relaxing it makes $V$ a fit.

**(4) Smallest next step.** Not the full alignment. The smallest well-posed computation is: take the App. C texture $M_{ij} = m_i\delta_{ij} + \varepsilon^{|i-j|}\sqrt{m_im_j}\,e^{i\varphi_{ij}}$ (line 2581), keep $\varepsilon=\lambda_W$ fixed for both sectors as the paper does, and let the *only* free datum be the vacuum angle $\vartheta$ in the $O(4)$ fiber that rotates the up- and down-type projections of $T_{B-L}$ relative to each other; compute $|V_{us}|(\vartheta)$ and ask whether $0.2245$ is reached for any $\vartheta$ with the $J$-phases of line 2582. Inputs: `ps_yukawa_full.py` (cited at line 2600) and the physical quark masses; cost: a 60-line numpy script. If no $\vartheta$ reaches 0.2245 the texture is excluded as the CKM source regardless of alignment; if one does, that $\vartheta$ is the number the vacuum alignment must produce, which converts F01 from an obstruction into a target.

**(5) Cheap check run now** (`acs-venv/bin/python -I scratchpad/actionable2/ckm_texture_check.py`, numpy; quark masses $m_u,m_c,m_t = 0.0013, 0.63, 172$ and $m_d,m_s,m_b = 0.0027, 0.054, 2.86$ GeV **from memory**, zero phases, $\varepsilon = 0.2265$): with identical mass inputs in both sectors $\max|V-\mathbb{1}| = 1.1\times10^{-15}$ (reproduces App. C's identity result); with the physical masses $|V_{us}| = 0.0429$, $|V_{cb}| = 0.0179$, $|V_{ub}| = 0.00128$ (observed 0.2245, 0.041, 0.0036). So the shared-$\varepsilon$ texture with real masses is *not* identity but gives $|V_{us}|$ a factor 5.2 too small, in line with the paper's own "$\approx0.05$ (too small)" at line 2476. The identity result at line 2586 is therefore specific to equal textures *and* equal mass ratios, not to the texture alone.

---

### Card P4 — The Newton-constant matching relation (candidate 19)

**(1) Open statement.** `papers/updates/ACS_Action_Identifiability.tex` lines 256–260: "A fixed measured Newton constant could provide extra dimensional data, but the matter-sector matching relation would still have to be derived. Dimensional transmutation also retains an integration constant: $\Lambda=\mu\exp[-1/(2bg^2(\mu))]$ for the stated one-loop equation. The beta function alone does not select $\Lambda$ in physical units." Endpoint audit lines 74–77: "The calculation does not choose a preferred a. A fixed measured Newton constant or other physical scale could be an additional input, but needs a derived matching relation to the matter sector."

**(2) Established.** The scaling identity itself: `ACS_Action_Identifiability.tex` lines 250–254, "$V_1$ scales by $a^4$. Two component tests use all 68 scalars, 21 gauge directions and a complex 48-Weyl example; normalized residuals are below $10^{-10}$ for the component scaling and $10^{-9}$ for the one-loop sum." Verifier checks: `17 homogeneous quartics`, `4 homogeneous quadratics`, `one-loop logarithm invariant under simultaneous scale change`, `conditional source RG reaches UV`, `finite running retains sensitivity` (PASS, 58/58). Paper A line 2649 states where the gravitational coefficient would come from: a "variational problem whose coefficients are fixed by the Killing form."

**(3) Obstruction.** Queue S06 (`exact_obstruction`), continuation: "Supply a normalized action and a scale-specific matching condition." The corpus has no expression for $G_N$ in terms of the condensate parameter $a$ and no statement of how the Palatini–Holst coefficient scales under $a$; a grep for Newton, $G_N$ and Planck across `docs/frontier` finds no derivation (the skeptic's verdict for this item records the same null result).

**(4) Smallest next step.** A one-page dimensional lemma, before any computation: under the homogeneity $x\to a x$ that scales $V_1$ by $a^4$, determine the scaling weight $w$ of the coefficient $\kappa$ multiplying the Palatini term $e\wedge e\wedge R$ in the same action. If $w \neq 4$ then the dimensionless ratio $v^2/M_P^2 \propto a^{4-w}$ is *not* scale-free and a measured $G_N$ together with $v = 246.22$ GeV fixes $a$ uniquely; if $w = 4$ the ratio is $a$-independent and $G_N$ cannot fix the scale at all, which would close the item negatively. Inputs: the action's gravitational term as written in Paper A §(Palatini) and the homogeneity test already in the verifier; cost: pencil, then a 20-line extension of the `one-loop logarithm invariant under simultaneous scale change` check. No numerical check was run for this card: there is no action in the tree to scale.

---

### Card P5 — The dynamical torsion action (candidate 20)

**(1) Open statement.** Paper A lines 838–841: "It does not, in this smooth metric-compatible action, supply a propagating torsion mode. A dynamical torsion extension requires additional terms and a separate mode analysis. The earlier description of this term as kinetic is withdrawn." `papers/updates/ACS_Condensate_Carrier_Boundary.tex` lines 262–266: "Curvature-derivative terms, singular defects or constrained teleparallel models require separate actions and mode analyses. They are not ruled out here, but their dynamics do not follow from renaming the algebraic term ``kinetic.'' The recovered soldering example likewise inserts a Lorentzian internal metric, a nondegenerate vierbein and a length scale."

**(2) Established.** The negative result is clean: the parity-preserving quadratic torsion term $\beta\,T^a\wedge{*T_a}$ (Paper A lines 835–838) "changes the algebraic contortion equation" only. Carrier Boundary lines 258–259: "The same algebraic structure is exhibited in the quadratic-torsion decomposition of Ref.~\cite{Torsion}." Queue G06 (`exact_result`) on the Holst map invertibility. `docs/Torsion_Topological_Condensation_Analysis.md` is an algebraic holonomy computation, not a mode analysis. No verifier check names torsion (grep of the 18 check names: none).

**(3) Obstruction.** Carrier Boundary lines 262–266 as quoted; G06 continuation: "Derive the complete spacetime action, source terms and actual evolution." G05 continuation: "Supply spacetime/soldering, full action, normalization, constraints, states and continuum limit". There is no candidate action: the item is open because the object does not exist in the tree, not because a computation failed.

**(4) Smallest next step.** State the action, then do the standard linearised spin-projector analysis; do not invent a new one. The minimal propagating-torsion Lagrangian is the quadratic Poincaré-gauge family $L = e\,[\,R + \beta\,T^a\wedge{*T_a} + \text{(two further } T^2 \text{ irreducibles)} + \sum_{i=1}^{6} a_i (R^2)_i\,]$ (the $R^2$ invariants in the Riemann–Cartan curvature are what make torsion propagate; the ghost- and tachyon-free coefficient windows are a known linearised result in the Poincaré-gauge literature, **from memory**, to be re-derived not cited). The ACS-specific question is the *selection*: which of the six $a_i$ the Killing-form-fixed variational problem (Paper A line 2649) sets to zero or relates. The smallest step is therefore: write the ACS action's curvature-squared sector in the Riemann–Cartan irreducible basis, linearise about flat space with zero torsion, and compute the $0^\pm,1^\pm,2^\pm$ spin-content of the torsion propagator. Cost: a 200-line sympy script using the standard spin projectors, plus the one page that translates the Killing-form coefficients into the $a_i$. Expected outcome: either a massive torsion multiplet with masses in units of the condensate scale (new prediction surface) or a confirmation that the ACS coefficients land outside the healthy window (closing the extension). No cheap check was run: there is nothing to run until the action is written.

---

### Card P6 — Barbero–Immirzi and the SU(2)$_k$ counting (candidate 26)

**(1) Open statement.** Paper A lines 1632–1635: "Reproducing the exact DL value within the ACS framework requires incorporating the full $\mathrm{SU}(2)_k$ Chern--Simons state counting; the mechanism is identified but the exact numerical derivation remains open." Lines 1697–1704: "the constrained value ($0.2375$) requires the additional Chern--Simons topological field theory machinery. The chirality map $J$ ... provides a natural $\mathbb{Z}_2$ grading (integer vs.\ half-integer $j$) that may select the spinorial sector; making this precise remains open." The ledger has moved the target (lines 115–121): "**γ = 0.274 → REFRACTION (value).** `KILLED` The value is counting-prescription-dependent ... Value moves (0.274 → 0.2375) under a change of the state-counting prescription ⇒ kill condition met. The invariant is structural — "there is a fixed γ once a prescription is fixed" — not the number 0.274."

**(2) Established.** The formula is given: Paper A lines 1603–1606, $Z(\gamma) = \sum_{j=1/2,1,3/2,\ldots} (2j+1)\,e^{-2\pi\gamma\sqrt{j(j+1)}} = 1$ (eq. BI-partition), with the stated root $\gamma_{\mathrm{ACS}} = 0.2741$ (line 1623) identified with Meissner's. Frontier T-G04 (`docs/frontier/2026-09-11/Task_Checklist.json` lines 200–219, status `needs_definition`): "Each specified positive counting prescription has one rigorously bracketed positive root, with different values across prescriptions" (scope: "Three explicit state-counting sums"); result: "At Z=1 the expected log degeneracy minus area cost is negative spin entropy, not zero. The U(1) zero-magnetic-projection constraint admits integer-spin punctures." `docs/frontier/2026-09-11/workstreams/foundations/report.md` line 128: "The constraint $\sum_i m_i=0$ alone permits two spin-1 punctures ... Enumeration and the constant coefficient of $(z^{-1}+1+z)^2$ both give three. This refutes that exclusion as a consequence of the projection condition alone".

**(3) Obstruction.** T-G04 continuation: "Derive the physical counting prescription and its temporal information process. Integer-spin exclusion requires an additional rule beyond sum m_i=0." I.e. the ACS condition $\Delta I = 0$ as currently defined does not choose between the $(2j+1)$-per-puncture weighting and the Gauss-constrained dominant weighting; and the $\mathbb{Z}_2$ selection offered at line 1702 is refuted as a consequence of $\sum m_i = 0$ alone.

**(4) Smallest next step.** The Domagala–Lewandowski dominant counting is equivalent to replacing the degeneracy $(2j+1)$ by $2$ (the two extremal magnetic labels $m=\pm j$ per puncture) in the same sum; the full SU(2)$_k$ level cut $j\le k/2$ is numerically irrelevant (check (5)). So the ACS-internal question reduces to a single definitional lemma: *which degeneracy does "Form information" $I_{\mathrm{Form}}(j)=\log(2j+1)$ (Paper A line 1597) count once the Gauss constraint is imposed as $\Delta I = 0$ on the boundary?* If the constraint is imposed before counting, the per-puncture weight is $2$ and the ACS root is $0.2375$; if after, it is $(2j+1)$ and the root is $0.274$. A finite brute-force count for $n\le 8$ punctures with $\sum m_i = 0$ enforced, compared against both exponents, decides which weighting the constrained count actually realises (this is Domagala–Lewandowski's computation restricted to small $n$; cost: minutes). What it cannot decide is whether $\Delta I = 0$ *means* the constrained count, which is the needs_definition in T-G04.

**(5) Cheap check run now** (`acs-venv/bin/python -I scratchpad/actionable2/immirzi_counting.py`, scipy `brentq`, $j_{\max}=2000$, xtol $10^{-12}$):

| prescription | root $\gamma$ | $Z(0.2375)$ | $Z(0.274)$ |
|---|---|---|---|
| (2j+1) per $j$, all half-integers (Paper A eq. BI-partition, Meissner) | **0.274067** | 1.422067 | 1.000614 |
| 2 per $j$, all half-integers (Domagala–Lewandowski dominant counting) | **0.237533** | 1.000273 | 0.747512 |
| (2j+1) per $j$, half-integer $j$ only | 0.222865 | 0.873814 | 0.640842 |
| 2 per $j$, half-integer $j$ only | 0.189138 | 0.691546 | 0.536537 |

Truncation (the SU(2)$_k$ cut $j\le j_{\max}$): the Meissner root is 0.224152, 0.265177, 0.272227, 0.273986, 0.274067 at $j_{\max}=1,2,3,5,10$ and unchanged at 50; the DL root is 0.201784, 0.231430, 0.236271, 0.237472, 0.237533 at the same cuts. Both candidate values are therefore the roots of two different weightings of the *same* sum, each converged to six decimals by $j_{\max}=10$; neither restriction to half-integer $j$ reproduces either value, which is consistent with the frontier's refutation of the $\mathbb{Z}_2$ selection.

---

### Card P7 — Sterile-neutrino production (candidate 28)

**(1) Open statement.** Paper A lines 2556–2570: "The Dodelson--Widrow mechanism overproduces this state by a factor $\sim\! 10^5$, ruling out a single-component DM interpretation. Three alternatives remain: (a)~a smaller effective $\theta$ from additional see-saw structure; (b)~resonant production (Shi--Fuller) requiring a lepton asymmetry; (c)~the sterile neutrino as a \emph{subdominant} DM component ... The ACS prediction is the \emph{mass value} ($M_R \approx 49$~keV) and the X-ray line energy, not the dark matter abundance --- the relic density depends on the production mechanism, which is outside the scope of the bracket algebra." `Holographic_Spectral_Inversion.tex` lines 794–795: "The Dodelson--Widrow mechanism overproduces this state by $\sim\!10^5$, requiring either subdominant DM or an alternative production mechanism."

**(2) Established.** The mass relation: Holographic lines 792–793, "$m_\nu \times M_R = m_e^4/(9m_\tau^2)$ (holds to $0.1\%$), predicting $M_R \sim 49$~keV"; the inputs $\theta \approx m_D/M_R \approx 10^{-3}$, lifetime $\tau\approx2\times10^{11}$ yr and line energy $E_\gamma = 24.5$ keV (Paper A lines 2556–2566). The ledger's Q7 (lines 285–303) finds the X-ray bound clearable at high $v_R$: "Required suppression S < 2.5×10⁻⁵ → M_WR ≳ 16 TeV (v_R ≳ 49 TeV)" (line 291; script `/tmp/q7_neutrino.py`, recorded as not committed). Frontier T-F05 (`Task_Checklist.json` lines 171–190, `needs_definition`): "A fixed physical spectrum (m,M,M) supports a continuum t in [m/(M+m),1]."

**(3) Obstruction.** Two, and they pull against each other. Paper A line 2569: the relic density "is outside the scope of the bracket algebra." Ledger lines 298–303: "Clearing the bound requires high v_R, hence high M_R ~ v_R, so the sterile/right-handed neutrino is **not keV-scale dark matter** at that scale. The resolution is by *decoupling* ... fatal if a keV-sterile-DM candidate was required (that role does not survive)." T-F05 continuation: "Full textures, observed mixing constraints, decay channels, abundance history and current likelihood." The corpus has neither a non-DW mechanism for a subdominant 49 keV state nor a reconciliation of $M_R\approx49$ keV with $M_R\sim v_R$.

**(4) Smallest next step.** Before any mechanism: a two-number consistency table. With the paper's own $(M_R, \theta)$, compute (a) the DW abundance with a stated fit formula and its reference, (b) the mixing the X-ray bound allows at 49 keV, and (c) the subdominant fraction $f$ for which (a) scaled by $f$ and (b) scaled by $1/f$ are simultaneously satisfied. If no $f\in(0,1]$ exists, alternative (c) in Paper A is closed and only (a)/(b) remain; if one exists, it is the number a production mechanism must hit. Cost: one script, one afternoon to pin the formula provenance. The reconciliation with Q7 is a separate, prior question for the owner: is $M_R \approx 49$ keV or $M_R \sim v_R$ the framework's right-handed-neutrino mass? Both cannot be on record.

**(5) Cheap check run now** (`acs-venv/bin/python -I -c ...`, mpmath; **DW fit formula from memory, not in the corpus**: $\Omega_s h^2 \approx 0.3\,(\sin^2 2\theta/10^{-10})(m_s/100\,\mathrm{keV})^2$): with $\sin^22\theta = 4\times10^{-6}$ (the ledger's stated naive value) and $m_s = 49$ keV, $\Omega_s h^2 \approx 2.9\times10^3$, an overproduction factor of $2.4\times10^4$ against 0.12, versus the paper's "$\sim10^5$"; DW would need $\sin^22\theta \approx 1.7\times10^{-10}$ to give $\Omega h^2 = 0.12$ at 49 keV. The factor-of-4 difference from the paper's $10^5$ is a provenance question for step (4), not a finding; the orientation (DW at the stated mixing is excluded by orders of magnitude) agrees with the paper.

---

### Card P8 — The capacitor factor of two (candidate 102)

**(1) Open statement.** `ACS_Condensate_Carrier_Boundary.tex` lines 186–203, "\subsection{Capacitance retains a cutoff and a factor of two}": with $L=\log(8R/a)+1$, "$\frac{E}{mc^2}=\frac{\alpha L}{2},\qquad E=mc^2\ \Longrightarrow\ \alpha^{-1}=L/2.$ The later archived CPF manuscript instead used $\alpha^{-1}=L$ and inserted $a/R=8\exp[-(K-1)]$. This produces any desired $L=K$ by construction. ... Neither cutoff follows from topology. The companion capacitance computations remain conditional model comparisons."

**(2) Established: the verifier.** Run on 22 October 2026 through a stdout-only wrapper (`acs-venv/bin/python scratchpad/actionable2/run_vs_capacitor.py <worktree>/code/publication_20260924`, which imports `verify_science.run()` and never calls its `__main__` writer): the line printed by the check is

```
PASS capacitor factor of two
```

and the check row is `{"name": "capacitor factor of two", "passed": true, "evidence": null}` within `TOTAL 58 PASSED 58 elapsed_s 1.3` (the 22 October rerun receipt `docs/publication/2026-10-22-rerun.md` line 18 records the same `{"total": 58, "passed": 58}` in 3.5 s). What the check proves is exactly its source line (`verify_science.py` line 121): `s.solve(s.Eq(alpha*L/2,1),alpha)==[2/L]`, i.e. that $\alpha L/2 = 1$ has the unique solution $\alpha = 2/L$. The repository instrument encodes the same convention: `code/capacitance_ribbon/ribbon_capacitance.py` lines 110–111, `def annulus_alpha_inv(R, a)`: "Closed form: alpha^{-1} = (ln(8R/a) + 1) / 2 under the self-stress match." The parameter-free reading is withdrawn in `docs/publication/2026-09-24/amendments.json` (line 84: "a chosen cutoff does not derive the fine-structure constant").

**(3) What remains open beyond the verifier.** The verifier settles the algebra of the factor of two and nothing else. Still open: (a) the cutoff — `docs/capacitance_ribbon_results.json` line 333: "annulus closed form (ln(8R/a)+1)/2 matches CODATA at this extreme a/R=2.039050e-118; not a geometric prediction of a"; frontier M02 (`docs/frontier/2026-09-11/workstreams/physical/report.md` line 210, "fixed framing leaves magnetic moments and capacitance free"); (b) the BIE-versus-CODATA mismatch on the scanned aspect window, which the verifier does not touch; (c) the editorial question of whether the $\alpha^{-1}$ self-stress match stays on record as a "conditional model comparison" or is retired. No check in the suite asserts anything about $a/R$ or the mesh validity.

**(4) Smallest next step.** Either supply an independent selection of $a/R$ (M02's continuation: "Charge/current/mass distributions, material and field dynamics, and a quantum spectral model") or retire the match. There is no intermediate computation that helps: the inverse relation reconstructs any target.

**(5) Cheap check run now** (mpmath, `acs-venv/bin/python -I -c ...`): $8\exp[-(K-1)] = 6.65896\times10^{-59}$ and $8\exp[-(2K-1)] = 2.03905\times10^{-118}$ at $K = 137.035999171$, reproducing the two cutoffs quoted at Carrier Boundary lines 198–202 to the six printed figures. This confirms the paper's arithmetic; it is the paper's point that the arithmetic is reversible.

---

### Card P9 — The Higgs mass-ratio closed form (candidate 103)

**(1) Open statement.** `docs/Editorial_Audit_2026-08-07.md` line 963 (C6): "Root README presented `higgs_mass_ratio.py` as a derivation. The winning closed form is **selected by a 17-candidate search**; `higgs_derivation.py` exists to derive it and does not succeed. | Fixed: labelled as numerology pending derivation". `docs/README_verification_suite.md` line 45: "m_H/v = 0.506306 vs 0.508691 (0.47% match, m_H = 124.66 GeV); the closed form is selected by a 17-candidate search, not derived".

**(2) Run and selection statistics.** `acs-venv/bin/python code/acs_codebase/extras/higgs_mass_ratio.py` (stdout only, exit 0, worktree clean afterwards) prints "Target: m_H/v = 0.508691", "Wolfenstein: λ_W = 0.226500", and under "THE RESULT": "Best formula: m_H/v = 4/(3π)×√(2π×λ_W) / Value: 0.506306 / Target: 0.508691 / Match: 0.47%". The script prints only the ten best of its candidates. Re-evaluating all 17 (`code/acs_codebase/extras/higgs_mass_ratio.py` lines 341–357; `acs-venv/bin/python -I scratchpad/actionable2/higgs17_stats.py`): 17 candidates, 14 numerically distinct values (three duplicate pairs); gaps to target: minimum 0.469%, second 0.534% ($\sqrt{2\lambda_W/\sqrt3}$), median 20.84%, mean 42.49%, maximum 252.83%; 1 within 0.5%, 2 within 1%, 3 within 3%, 8 within 10%. Two further facts from the same run: the winner simplifies to $(4/3)\sqrt{2\lambda_W/\pi}$, so the $\pi$ does not cancel, and it is the only one of the 17 containing $\pi$; and the 0.47% depends on the input $\lambda_W = 0.2265$: at $\lambda_W = 0.2245$ (the value Paper A line 2478 calls "the observed $0.2245$") the winner's gap is 0.909%, at 0.2250 it is 0.799%.

**(3) Obstruction.** `docs/condensate_energy/action_matching/README.md` lines 210–216 on `higgs_derivation.py`: "direct SU(4)-only loops generate no Phi quartic in the unbroken canonical theory, because Phi is a color singlet ... That coefficient does not determine a finite quartic or a renormalization condition"; lines 238–239: "No physical coefficient is to be fixed by matching the desired Higgs mass." Endpoint audit line 121: "Neither gives 2√3/27." Queue S06 as in Card P1.

**(4) What lifting "numerology pending derivation" would need.** A pre-registered derivation, in the sense of the repository's own rule, that produces $m_H/v = (4/3)\sqrt{2\lambda_W/\pi}$ *including the $1/\sqrt\pi$* from a normalised action before the number 0.508691 is looked at. No Lie-algebraic normalisation in Paper A produces a $\pi$ (the factors on record are $2$, $\sqrt3$, $27$, $4/3$, $2/3$: lines 2016–2020), so the derivation would have to come from a loop integral or a geometric volume, which is a different calculation from the Killing-form chain of Card P1. Absent that, the two consistent options are: keep the row as labelled (numerology, with the 2-of-17-within-1% statistic beside it) or retire it from the verification suite and the Paper A line 2034 "Verified:" list. Choosing between them is the owner's; the agent's recommendation is to add the full-17 statistic and the $\lambda_W$-sensitivity to the README row, because "0.47% match" without "second candidate at 0.53%; 0.91% at $\lambda_W=0.2245$" overstates the selectivity of the search.

**(5) Cheap check run now.** The statistics in (2) are the check. Left out: a look-elsewhere probability, since the candidate family is not a sample from any stated distribution and any such number would be a choice, not a measurement.

---

**What this section left out.** No manuscript was edited; no instrument was run that writes into tracked paths (`git status --short` in the worktree after all runs: only this file and the one-bullet `docs/README.md` change). Numbers marked **from memory** (PDG $m_H$, quark masses, the Dodelson–Widrow fit) are orientation inputs, not corpus facts, and any card that depends on them says so. The scratch scripts (`higgs_chain_check.py`, `gl4_span_check.py`, `ckm_texture_check.py`, `immirzi_counting.py`, `higgs17_stats.py`, `run_vs_capacitor.py`) are not committed; each is under forty lines and is reproduced in substance by the formulas quoted in its card. Not attempted in the time box: the brute-force small-$n$ Gauss-constrained count of Card P6(4), the vacuum-angle scan of Card P3(4), and any look at the `ps_yukawa_full.py` phases.
