# Foundations continuation: exact instruments and remaining bridges

This continuation appends results for I01, I05, I07, G04, G05, D03, K01, K02, K03, K05 and C05. It preserves the prior catalog, manuscripts, runtime receipts and access receipts. It does not claim access to private AISO production code or an independent Lean kernel pass.

All three new suites passed in `attempts/20260911T221928192942Z`. An earlier attempt, `20260911T221823239906Z`, failed only because SymPy was missing; its error, successful companion checks and exact program versions remain. The later run used SymPy 1.14.0 and mpmath 1.3.0. The actual Yang–Mills comparison checker is copied byte for byte, with 30 further source/evidence files and SHA-256 identities under `support/`.

## Branch dispositions

| Branch | New disposition | Exact remaining bridge |
|---|---|---|
| I01 | Reference-measure dependence, zero-lag mismatch and the invalid Cartan substitution are explicit; a correct local KL expansion is supplied. | Specify the ACS transition law, observations, lag/history and reference measure, then derive its likelihood. The supplied field split tests the formula's reference dependence; it is not asserted to satisfy every informal ACS condition. |
| I05 | The PDR information-balance halting criterion fails on a four-cycle; a conditional contraction/residual certificate is supplied. | Derive a contraction or coercive Lyapunov inequality for the actual update map and name the convergence target and norm. |
| I07 | A delayed-copy process has current-state TE 0 and full-history TE 1 bit; there is no universal ordering inferred from the prior OU example. | Specify both conditioning sigma-algebras and the temporal law before identifying an ACS information observable. |
| G04 | The Gibbs identity separates a counting normalization from temporal information balance. The zero-magnetic-projection condition admits integer-spin punctures. | Derive the selected physical state counting and its temporal information law; any exclusion of integer spins needs an additional rule. Existing certified roots retain their original scope. |
| G05 | Same internal grading admits different differential symbols and arbitrary mass scales; a solder-map conditional theorem is stated. | Specify spacetime/soldering, full action, normalization, constraints, physical states and continuum limit. |
| D03 | **Correction to the earlier blanket “missing definitions” reading:** the source does specify an O(4) carrier, rewrite maps and observation/variance formulas. Its claimed variance/noncommutativity identification fails directly on that carrier. | Select a faithful observable for ordered compositions, a scheme probability law, and actual topology/restrictions/gluing if a sheaf is intended. A concrete optional sheaf completion is supplied. |
| K01 | An exact, append-only Boolean provenance/replay instrument is implemented and checked by resolution and a separate exhaustive oracle. | Obtain the production constraint semantics, evidence grades, learning/retraction rules and arithmetic/replay format; audit an authorized pinned implementation. |
| K02 | Public benchmark code is recognized and scoped. Private AISO speed/deployment evidence remains unavailable. | Supply the private code, baseline, workload, environment and exact comparison protocol. |
| K03 | The actual available comparison checker has verified negation blindness, a final-window scanning omission, and an unused `--sealed_spec` argument. | Supply the external proof and dependency chain. These checker tests determine nothing about that proof's truth. |
| K05 | Source census, source identities and prior access/runtime gates are preserved without unchanged retries. | Authorized accessible production revision and a working supported proof runtime. |
| C05 | Static source/dependency inventory completed; 24 theorem declarations found across three Lean files, with no `sorry`/`admit` tokens in the comment-stripped census. **Zero new kernel passes.** | Run unchanged files in the supported pinned environment, inspect theorem axioms and reject a separate false-statement mutation. Static token scans cannot replace this gate. |

## I01: repair the statistical object before the bracket bridge

The source defines lagged transfer entropy as conditional mutual information in `papers/Form_Function_and_Asymmetry.tex:306–320`, then gives a different pushforward KL expression at lines 485–493. At zero lag, the former is

\[
I(Y_t;X_t\mid Y_t)=0.
\]

The latter, evaluated at zero flow, is \(D(\mu\Vert\mu_Y\otimes\mu_X)=I(X;Y)\). A binary law with diagonal probabilities \(3/8\) and off-diagonal probabilities \(1/8\) gives a strictly positive value, approximately 0.1887 bits. Both the entropy identity and direct conditional-likelihood summation were evaluated independently. Extra independence assumptions can remove this zero-order discrepancy, but they do not establish the temporal identity.

The reference-measure issue is separate. On \(\mathbb T^2\), take Haar \(\mu\),

\[
f=(\sin x,0),\qquad g=(\sqrt2-\sin x,1).
\]

Their sum is the ergodic irrational translation \((\sqrt2,1)\). For the proposed first coefficient, choosing \(\nu=\mu\) gives zero. Choosing \(d\nu\propto e^{\cos x}d\mu\) gives

\[
\langle f-g,\nabla\log(d\mu/d\nu)\rangle_\mu
=\int(2\sin x-\sqrt2)\sin x\,d\mu=1.
\]

Symbolic integration and the Fourier constant term give the same exact result. TE cannot change merely because an auxiliary reference measure changes. This establishes the need for a fixed, justified reference or a corrected reference-invariant formula. It does not identify this field split as a complete ACS-1/2/3 realization.

The source's second-variation substitution is algebraically wrong:

\[
L_fL_g+L_gL_f-(L_f+L_g)^2=-L_f^2-L_g^2,
\]

which is not \([L_f,L_g]\). The script checks an explicit two-dimensional matrix representation as a separate witness.

A constructive local replacement is available. For normalized smooth discrete densities sharing a strictly positive baseline,

\[
p_\epsilon=p_0+\epsilon a+O(\epsilon^2),\quad
q_\epsilon=p_0+\epsilon b+O(\epsilon^2),\qquad
D(p_\epsilon\Vert q_\epsilon)
=\frac{\epsilon^2}{2}\sum_i\frac{(a_i-b_i)^2}{p_{0i}}+O(\epsilon^3).
\]

Normalization removes the linear term and the second-derivative mass terms. The binary example is independently differentiated symbolically. This is a likelihood/score theorem under named hypotheses; identifying its score difference with an ACS Lie bracket still requires a dynamical derivation.

## I05 and I07: information balance, convergence and history are different conditions

The PDR explicitly says to halt when the signed information difference approaches zero (`papers/ACS_Deterministic_AI_Stack_PDR.tex:692–736`). The deterministic map

\[
(x,y)\mapsto(y,1-x)
\]

cycles through \((0,0),(0,1),(1,1),(1,0)\). Under its stationary uniform law both directional current-state TEs equal 1 bit, so their difference is zero. Successive states remain exactly unit distance apart. Exact conditional-likelihood and entropy calculations establish the information values; direct orbit evaluation establishes nonconvergence. This refutes the general halting implication, while making no claim that this finite map satisfies every smooth-field ACS hypothesis.

For a declared \(q\)-contraction with a fixed point, a usable stopping certificate is

\[
\|z-z_*\|\le\frac{\|z-Tz\|}{1-q}.
\]

The test matrix with diagonal \(1/4\) and off-diagonal \(1/8\) has \(q=3/8\), checked by exact spectral eigenvalues and an independent row-sum norm. This illustrates the missing kind of inequality, not a replacement secretly imposed on the ACS system.

For the history question, let \(X_t\) be independent fair bits and \(Y_t=X_{t-2}\). Then

\[
I(Y_{t+1};X_t\mid Y_t)=0,
\qquad
I(Y_{t+1};X_{\le t}\mid Y_{\le t})=1\text{ bit}.
\]

The current source is independent of the future target; its history contains that target exactly. Older target history gives only older independent bits. Finite exact probability enumeration and this independent conditional-independence argument agree. The earlier OU result comparing particular current and history rates does not imply a universal inequality when both histories change.

## D03: assess the actual O(4) definitions

`papers/discrete_geometry_formalism.tex:29–51` supplies \(\mathcal A=O(4)^\Gamma\), endomorphisms \(R_\alpha\), and an observation \(\Phi\). Lines 71–79 identify a variance of repeated single-scheme observations with noncommutativity. This is directly testable:

1. On a one-point grid at \(A=I_4\), let \(R_P(A)=PA\), \(P=\operatorname{diag}(-1,1,1,1)\), and let the other scheme be the identity. They commute. With \(\Phi(A)=A_{11}^3\), equal scheme weights and \(k=1\), the reported variance is exactly 1.
2. Take quarter-turn rotations in the 12 and 13 planes. They do not commute, but \(\Phi(A)=A_{44}^3\) equals 1 on their entire generated orbit. Both the reported variance and every observed two-order defect vanish.

Exact matrix products/orthogonality and separate two-point probability/orbit calculations verify both witnesses. The observable in the second witness is nonconstant on the full state space, although it is blind to this reachable orbit.

The ambient matrix commutator can also leave \(O(4)\), so applying the stated \(\Phi:\mathcal A\to\mathbb R^m\) to it is generally undefined. A well-typed order observable is

\[
\delta_{\alpha\beta}(A)=\Phi(R_\alpha R_\beta A)-\Phi(R_\beta R_\alpha A).
\]

If \(\Phi\) is injective on the reachable orbit, this vanishes exactly when the two ordered states agree. A lower Lipschitz bound gives a quantitative lower bound on the observed defect. Neither condition turns variance across \(R_\alpha^k\) into a commutator statistic.

Two further source-level corrections follow from the definitions. Actual endomorphisms always compose associatively, and adjoining an empty word yields a monoid, hence a one-object category. Failure of a proposed composition law for preassigned scheme labels does not prevent that category. Also, a finite grid and finitely many schemes do not make the continuous-valued carrier or its orbit finite.

The source has not supplied sheaf restrictions or gluing. A constructive optional completion takes a discrete set of words through a chosen finite depth, sets \(F(U)\) to all measurement-valued functions on \(U\), and restricts by deleting coordinates. The orbit observations form a distinguished global section. Compatible local functions glue uniquely by pointwise union. The script additionally exhausts all eight compatible Boolean gluings for a three-word cover. This proves that a sheaf can be specified; it does not select a unique intended ontology or physical model.

## G04 and G05: what the internal/statistical data determine

The counting sum in `papers/Form_Function_and_Asymmetry.tex:1941–1970` is mathematically definite once its weights are chosen. Its proposed information interpretation requires another step. If

\[
p_j=\frac{d_j e^{-\gamma a_j}}{Z},
\quad
\mathbb E[\log d_j-\gamma a_j]=-H(p)+\log Z,
\]

then at \(Z=1\) that expectation is strictly negative for a nondegenerate law, not zero. Degeneracies \((2,3)\), costs \((1,2)\), and \(\gamma=\log3\) give the exact probabilities \((2/3,1/3)\) and \(Z=1\). Direct summation matches the entropy identity. This tests one proposed interpretation of the source's “Form information minus Function cost”; temporal TE still requires a process. Independent draws from the normalized distribution have zero TE in both directions for every \(\gamma\), regardless of whether the unnormalized sum equals 1.

The source also describes the U(1) projection as excluding integer spins (lines 1998–2016). The constraint \(\sum_i m_i=0\) alone permits two spin-1 punctures with \((m_1,m_2)=(-1,1),(0,0),(1,-1)\). Enumeration and the constant coefficient of \((z^{-1}+1+z)^2\) both give three. This refutes that exclusion as a consequence of the projection condition alone; it does not choose between all physical counting prescriptions or invalidate the already certified roots.

For G05, keep one internal involution \(J=\operatorname{diag}(1,-1)\). Adding the differential symbol \(-\omega^2+k^2\) or \(\omega^2+k^2\) leaves the internal grading untouched but changes the real characteristic structure. Adding an arbitrary positive \(m\) to the hyperbolic completion changes \(\omega^2=k^2+m^2\). The determinant/inertia check and characteristic/dispersion check are separate routes. Thus the grading by itself cannot select those added data. If an invertible solder map and an internal bilinear form are supplied, \(g=e^T\eta e\) inherits the inertia of \(\eta\); that conditional theorem still does not choose the dynamics or masses.

## K01: transparent constraints with explicit semantics

The source glossary is decisive: `docs/Cross_Repo_Glossary_Extract.md:51` expands the program's CDCL as **Constraint-Driven Consensus Layer** and explicitly distinguishes it from SAT's Conflict-Driven Clause Learning. The source census found eight relevant mentions but no actual production engine. Therefore the new Boolean instrument is a deliberately narrower reference sublanguage, not a reconstruction or audit of unseen AISO.

The instrument has immutable, scoped, hashed events; explicitly declared premise origins; a distinct exact-Boolean evidence grade; exact integer literals; local two-parent resolution; earlier-node dependencies; and append-only retirement. Every proof carries the set of premise leaves supporting it. It is usable exactly while all those leaves remain active. Different proof nodes may conclude the same clause while retaining different supports. Retraction leaves the earlier proof in the log and invalidates only its current use. A new valid derivation can survive independently.

Soundness follows by induction over appended proof nodes and a two-case argument on the resolution pivot. The independent checker uses complete truth assignments instead of resolution to verify every live conclusion against active root clauses, and recursively traverses ancestry instead of using the support-set algorithm. All ledger prefixes agree. The test also exhausts 294 admissible resolution instances across all 27 tautology-free clauses on three Boolean variables and rejects eight mutations: content tampering, a wrong rehashed resolvent, a forward parent, cross-scope use, changed arithmetic, unsupported evidence grade, floating-point literal, and reuse of a retired premise.

The 11-event trace and independent prefix oracle are preserved. Hashes establish content integrity under their assumptions; they do not authenticate an author or establish a claim's truth. An actual production audit needs a semantic predicate and sound inference rules for each production evidence type. Empirical research dispositions must not silently become Boolean theorems.

## K02, K03, K05 and C05: audit what is present

Two independent source censuses, `rg` and a filesystem traversal, agree on 329 selected text/code files. The source availability note in `papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex:339–342` independently says the production code and private engineering evidence are absent. `code/benchmark_efficiency.py` is present and explicitly measures scoped public script performance; it is not the missing private workload. No private speed claim was rerun or rejected on that basis.

The available `scripts/ym_comparison_checker.py` was imported unchanged. All eight predictions score 1.0/MATCH for both affirmative and explicitly negated fixtures containing the same keywords. A separate implementation of the published keyword score confirms this. A second fixture places a full C4 keyword cluster after 150 neutral words: the actual checker reports MISS/0, while its unscanned final 150-word window scores 1.0. Control-flow inspection identifies the range endpoint that omits that window. AST inspection finds no dereference of the parsed `--sealed_spec` argument. These findings concern the comparison tool only; they determine nothing about the unavailable 600-page proof.

The three copied Lean files contain 24 theorem declarations in a static token census. Their hashes, toolchain and nine locked package revisions are preserved. The pinned Mathlib revision is `be865aa50cc0364be66c3941a6dc0c845a2c2ceb`, with `leanprover/lean4:v4.34.0-rc2`. The source itself states that the Klein-bottle lifting/topology input in `AxiomIII.lean` remains external. Both historical runtime startup failures are retained. No unchanged startup or GitHub 404 retry was made, and no runtime/access restriction was altered.

## Replay

Install the two versions in `requirements.txt` into an appropriate working environment, then run `python run_checks.py` from this directory. The script appends a new timestamped attempt with stdout, stderr, program copies, hashes, receipts and result JSON. No original source or earlier attempt is edited. `source_instruments.py` reads only the portable pinned copies and verifies their hashes before importing the checker. The failed first attempt remains part of the evidence, and runtime/access-blocked branches remain explicitly open.
