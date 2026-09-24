# Source and data continuation — 12 September 2026

This pass connects the Frontier queue to an accessible source revision and original ordinate tables. It also finds and fixes an overflow bug in the canonical finite normalized sum, corrects its RH interpretation, and records a certified endpoint-count counterexample caused by using rounded ordinates beyond their precision. No new Lean theorem or global RH claim is made.

## Source coverage and retained baseline

The baseline is commit `f75fa752d5b973ca3d4f6ca7e4641c75570e7d26`. [Baseline_Inventory.json](Baseline_Inventory.json) records 325 source, document, and data files, including 195 Python files with parsed top-level functions and imports. The inventory excludes prior Frontier checkpoints, PDFs, images, and other binary files; it is not a claim to have semantically audited every file. [Source_Map.json](Source_Map.json) links inspected implementation areas to research branches and distinguishes source availability from validation.

The canonical appendix lives in `code/acs_codebase/src/`; its original 42 tests all passed in this replay. The HP knife suite separately loads the 100,000-ordinate file. The canonical Paper B code supplies only 50 values rounded to six decimals and explicitly constructs `diag(gamma)` for its resolvent check. That finite identity holds for any supplied spectrum and does not construct a natural operator or an infinite trace.

The historical exploratory index conflicted with the `extras/` README about which scripts were verified. Its title and run instructions now point to the canonical suite, while preserving its historical catalog as such. Training source is present, but the declared corpora, run artifacts, Merkle-memory file, and comparison script are absent from this revision; exact paths are recorded in the source map. The Yang-Mills comparison checker is present, but a keyword checklist does not verify an external proof.

[Source_Snapshot.zip](Source_Snapshot.zip) retains all 325 baseline files, the five corrected files, and the new audit instruments. Future source edits need not overwrite this checkpoint's evidence.

## Primary ordinate provenance and independent checks

The repository's `riemann_zeros_100k.txt` is identical to Odlyzko's `zeros1` after restoring one final newline. All 100,000 values also match the prefix of the retrieved `zeros6` table, which contains 2,001,052 ordinates. The provider states absolute uncertainties of `3e-9` and `4e-9` respectively. The first 100 high-precision ordinates are separately supplied in `zeros2`. [Primary table index](https://www-users.cse.umn.edu/~odlyzko/zeta_tables/)

[Primary_Tables.zip](Primary_Tables.zip) retains the downloaded tables, index, response metadata, and hashes; the larger table is retained in its original gzip form. [Source_Identity.json](Source_Identity.json) records exact comparison results. Five selected zeros, at indices 1, 3, 10, 50 and 100, were independently recomputed with Arb and mpmath and compared to the high-precision source. This is not an independent recertification of every ordinate.

For `N=50, 1000, 10000, 100000`, the endpoint `T` is the exact decimal midpoint of the listed Nth and next ordinate. Arb separately confirms `N(T)=N`. For each endpoint, the finite scalar deficit from the previous Lean checkpoints is evaluated at resolutions `1e-2`, `1e-4`, and `1e-6`, carrying `3e-9` uncertainty on every supplied ordinate. These 12 interval computations are compared with a separate float64 midpoint calculation.

For example, at `N=100000`, `T=74921.378646477`, and `epsilon=1e-4`, the total deficit is enclosed by `[0.00509520994 +/- 3.39e-12]`, and the mean by `[5.09520994e-8 +/- 3.39e-17]`. These are finite data-dependent enclosures conditional on the provider's input uncertainty, not asymptotic estimates. The omitted infinite tail remains a separate obligation. Full results are in [Dataset_Audit.json](Dataset_Audit.json).

## A certified failure of a rounded endpoint count

The third listed ordinate is `25.010857580`. Set the exact endpoint to

$$T=25.010857580+10^{-10}=25.0108575801.$$

Counting the rounded inputs gives three. Arb's zero-count function gives two, and its independently recomputed third ordinate lies above this endpoint. Thus the assumed third point is not interior, so the positive-interior error criterion cannot be applied to that three-point list as an actual zero configuration.

The error affects the scalar integral too. At resolution `1e-10`, the rounded third point gives a paired contribution near `4.71238898037669`; the recomputed point gives approximately `2.28445885500593`. The coarse input interval correctly exposes the uncertainty. [Dataset_Audit.json](Dataset_Audit.json) contains twelve endpoint-precision cases.

This adds branch R12: endpoint counts and finite-resolution observables need an input-precision contract. The counterexample does not invalidate the primary table; its use violated the separation needed for an unambiguous count. A practical gate is that each ordinate interval must lie entirely on one side of the selected endpoint, with finer evaluation when that fails. For shrinking resolution, uncertainty relative to resolution must also be controlled.

## Canonical implementation and interpretation correction

The canonical routine formed `exp(u)` before normalizing. It returned NaN at `u=710` and `1000`, despite representing the finite bounded sum

$$D_N(u)=-2\Re\sum_{k=1}^N\frac{e^{i\gamma_k u}}{1/2+i\gamma_k}.$$

The implementation now cancels the real exponential before evaluation. Four regression cases use an independent real trigonometric expression; when applied to the original code, the two beyond the exponential range fail as expected. The corrected 46-case suite passes. A 70-digit mpmath calculation at five values through `u=1000` agrees with the corrected float64 results to better than `3e-13`. [Test_Receipts.json](Test_Receipts.json), [Normalization_Crosscheck.json](Normalization_Crosscheck.json), and [Execution_Artifacts.zip](Execution_Artifacts.zip) retain the complete evidence.

For every fixed finite real ordinate list,

$$|D_N(u)|\le2\sum_{k=1}^N(1/4+\gamma_k^2)^{-1/2}.$$

This follows from the triangle inequality and holds for synthetic ordinates too. It does not establish a constant bound on the full arithmetic quantity `(psi(exp(u))-exp(u))/exp(u/2)`. Under RH, the classical estimate for that quantity is `O(u²)`; Schoenfeld's Theorem 10, equation (6.2), supplies `u²/(8*pi)` above the stated threshold. The module, canonical README, and ledger now make this distinction explicit. [Schoenfeld's primary paper](https://www.ams.org/mcom/1976-30-134/S0025-5718-1976-0457374-X/S0025-5718-1976-0457374-X.pdf)

## Continuation gates

The [queue](Research_Queue.json) retains all 113 inherited branches and adds R12. Six appended events preserve the prior 329-event prefix and advance source mapping, the actual-data error application, the normalization correction, the training-input gate, and evidence reconciliation. The source map identifies the next concrete inputs: certified L-function zero lists and their completeness/precision records; the truncation-to-arithmetic and natural-operator bridges; missing training corpora and run identities; and the still separate topology and coupled RG obligations.

The [manifest](Manifest.json) and [integrity receipt](Verification.json) validate retained sources, commands, archives, and branch history. Earlier proof checkpoints are checked for integrity, not mathematically rerun in this pass. Reproduction instructions are in [SOURCE_README.md](../../../code/frontier_verification/SOURCE_README.md).
