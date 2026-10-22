# Governance decisions awaiting the owner, 22 October 2026

[Repository home](../README.md) · [Documentation](README.md) · [Branches](BRANCHES.md) · [Reproduction](REPRODUCTION.md) · [Publication record](publication/2026-09-24/README.md)

**What this page is.** Seven decision briefs, one per open repository-governance question. Each gives the question in one sentence, the evidence with the command that produced every number, the options with what each costs and breaks, a recommendation that is the preparing agent's and not the owner's, and what happens if nothing is decided. Nothing here is a ruling. Nothing here changes a manifest-bound file.

**Measurement frame.** All counts were taken on 22 October 2026 in a clone where `origin/main` = `389afe2` and the branch `claude/surrogate-discriminant-amendments` is at `badb0b7` (= `origin/claude/surrogate-discriminant-amendments`). "Ahead/behind" is `git rev-list --count origin/main..<ref>` / `<ref>..origin/main`; "three-dot stat" is `git diff --stat origin/main...<ref> | tail -1`; "merge-tree" is `git merge-tree --write-tree origin/main <ref>`. GitHub figures are from `gh api repos/tensorrent/ACS-Framework/pulls/<n>` and are labelled REST; they count against the PR's recorded base and do not always agree with the local three-dot count, and the two are reported side by side rather than reconciled.

**Index.** The 24 September [branch index](BRANCHES.md) lists five unmerged refs and one deleted one. Their dispositions:

| Branch | Status | Brief |
|---|---|---|
| `claude/surrogate-discriminant-amendments` | unmerged, no PR, 10 ahead | [1](#1-the-surrogate-discriminant-branch-merge-pr-and-promotion) |
| (the integrity gate on `main`) | red since `389afe2` | [2](#2-the-integrity-gate-new-preservation-record-or-move-the-author-statement-out) |
| `claude/constraint-projection-framework-010dsu` (PR #14) | open, dirty | [3](#3-pr-14-constraint-projection-framework) |
| `codex/acs-frontier-delta-2026-09-12` (PR #16) | open, clean | [4](#4-pr-16-frontier-delta) |
| `claude/papers-repo-analysis-kce6bn` | unmerged, no PR, 1 ahead | [5](#5-the-exodus-kill-commit-merge-or-drop) |
| `claude/public-ip-exposure-audit-6zxyf4` | unmerged, no PR, 1 ahead | [6](#6-absolute-path-exposure-one-policy-and-the-redaction-branch) |
| `claude/infinity-zero-scaled-invariance-vzm54b` | unmerged, closed PR #4, 1 ahead | [7](#7-the-reconciled-ruling-on-the-infinity-zero-branch) |
| `feature/prime-fhe-homomorphic-primitive` | **decided** — ref deleted 22 October 2026, [BRANCHES.md addendum](BRANCHES.md) | — |

## 1. The surrogate-discriminant branch: merge, PR, and promotion

**Question.** Does `claude/surrogate-discriminant-amendments` merge into `main` as supporting documentation under `docs/`, and do its two papers get a pointer (or an explicit exclusion) in the governing layer, or a promotion into `papers/`?

**Evidence.**

- Branch tip `badb0b7`, pushed (`git log -1 --format=%h origin/claude/surrogate-discriminant-amendments` → `badb0b7`); **10 ahead, 0 behind** `origin/main` (`git rev-list --count origin/main..HEAD` → 10; `HEAD..origin/main` → 0). The ten commits are docs-only by subject (`git log origin/main..HEAD --format='%h %s'`): `65dfb15` and `53f7d95` add the two papers (21 Oct); `48c38b6`, `555b198` the FHE-deletion record; `f2902c4` the built PDFs; `7e17623`, `262a118`, `979596a`, `afbb962`, `badb0b7` the dated rerun receipt and its index entries (22 Oct).
- **`papers/` is untouched**: `git diff --stat origin/main HEAD -- papers/` prints nothing. The integrity verifier on this branch returns the same 8 failures as on `main`, no more (`python scripts/verify_publication.py --integrity-only` → 8 `manifest mismatch` lines, all under `papers/`, exit 1; see brief 2).
- **The governing layer does not mention the papers**: `grep -c -E 'instrument_floors|surrogate_discriminant' MANIFEST.md README.md` → 0 and 0; `grep -rl` over `docs/publication/2026-09-24/` → 0 files; `papers/catalog.json` and `papers/README.md` → 0 each; `find papers -iname '*surrogate*' -o -iname '*instrument_floor*'` → nothing.
- **The papers classify themselves as non-governing**: `docs/instrument_floors.tex:94-97` and `docs/surrogate_discriminant_amendments.tex:63-66`, "Status in this repository. A supporting document under docs/, outside the 35-paper canonical publication inventory and its build job ... Its propositions and measurements are not part of the corpus author statement".
- **Already recorded on the branch**: `docs/README.md:50-51` lists both papers with their PDFs; `docs/BRANCHES.md:13` lists the branch ("opened 21 October 2026, no PR"); `docs/REPRODUCTION.md:91-93` declares the cross-repository dependency on `tensorrent/AISO-UI-for-Ai` and says "Promoting those instruments into `code/` here is an open owner decision recorded in the branch index."
- **No PR**: `gh api 'repos/tensorrent/ACS-Framework/pulls?state=open'` lists #16 and #14 only.
- **No CI on this branch**: `.github/workflows/publication.yml:3-5` triggers on push to `main` and `codex/**`, on `pull_request`, and on dispatch. A `claude/*` push runs nothing; opening a PR would run the gate, which reads red today for the 8 pre-existing mismatches (brief 2), not for anything on this branch.
- **Branch-name convention**: this repository has none to check against (`ls docs | grep -i branch` → `BRANCHES.md`, `branch-audit`; `grep -rn -iE 'branch nam|naming convention'` over `README.md`, `docs/README.md`, `docs/BRANCHES.md`, `.github/` → no hits). Five of the seven remote refs carry the `claude/` prefix. AISO's `docs/BRANCHING.md` rule that `claude/*` is harness scratch governs AISO, not this repository.
- **Promotion into `papers/` is gated twice**: `scripts/check_navigation.py:61-69` requires a `papers/catalog.json` entry and a clickable `papers/README.md` row for every `papers/**/*.tex` that carries `\documentclass`; `scripts/verify_publication.py:24-25` fails with `manuscript inventory changed` whenever that set differs from the manifest's 35. Promotion therefore requires a new preservation record (brief 2) as well as the instruments moving into `code/`.
- **AISO side (REST, `gh api repos/tensorrent/AISO-UI-for-Ai/pulls/17`)**: PR #17 open, head `4fd37e0`, 640 commits, `mergeable_state: unstable`, 0 requested reviewers; `origin/main` there is `1165230`. The two papers pin that branch for reproduction (`docs/instrument_floors.tex:778-780`), so the pin is to an unmerged branch in the other repository too.

**Options.**

| | Costs | Breaks |
|---|---|---|
| **A. Open a PR and merge as docs-only.** | A PR; the CI run will be red for the pre-existing 8, so the merge is by owner judgement, not by a green check. | Nothing in the seal: 0 manifest-bound files touched. |
| **B. A, plus an explicit line in `MANIFEST.md` saying the two papers are outside the inventory and the author statement.** | One paragraph. `MANIFEST.md` is not manifest-bound (`grep -c '"MANIFEST.md"' publication-manifest.json` → 0), nor is the top-level `README.md` (→ 0). | Nothing. |
| **C. Promote into `papers/`.** | Catalog entry, README row, instruments imported into `code/`, and a new preservation record (brief 2); the AISO pin would move from a branch to a merged commit. | The current seal, until re-sealed. |
| **D. Leave unmerged.** | Nothing now. | `main`'s `docs/README.md` and `BRANCHES.md` keep not mentioning the branch; the rerun receipt stays off `main`. |

**Recommendation (the agent's).** B. The branch is docs-only, pushes nothing into the sealed set, and already carries its own exclusion text; what `main` lacks is the pointer. C should wait on brief 2 and on AISO PR #17 reaching a merged commit, because a `papers/` entry that pins an unmerged branch for its reproduction is weaker than a `docs/` entry that says so.

**If nothing is decided.** The branch stays 10 ahead with no CI and no PR; the only reader-facing index of the two papers is on a branch.

## 2. The integrity gate: new preservation record, or move the author statement out

**Question.** Does the owner cut a new dated preservation record that re-seals the 8 manuscripts edited by `389afe2`, or move those 8 edits out of the sealed sources so the 24 September seal holds again?

**Evidence.**

- **Measured red.** In a clean worktree at `badb0b7` (`papers/` identical to `main`): `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python scripts/verify_publication.py --integrity-only` → `manuscripts 35, amended 33, manifest_files 561, receipt_references_verified 516, relocated_references 16, archive_only_references 0`, and exactly 8 failures, all `manifest mismatch:` — `papers/ACS_Deterministic_AI_Stack_PDR.tex`, `papers/Form_Function_and_Asymmetry.tex`, `papers/core_trilogy/Holographic_Spectral_Inversion.tex`, `papers/core_trilogy/Palatini_Gauge_Attractor.tex`, `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex`, `papers/core_trilogy/Spectral_Witness_Refinement.tex`, `papers/updates/ACS_Action_Identifiability.tex`, `papers/updates/ACS_Condensate_Carrier_Boundary.tex`; exit 1. `git status --short` was empty afterwards (the report goes to the ignored `build/`).
- **Cause.** `git show --numstat 389afe2 -- papers/` touches exactly those 8 `.tex` plus `papers/README.md` (which is not bound: `grep -c '"papers/README.md"'` → 0). Five files gained 12 appended lines (`\section*{Author Statement, Neurodiversity Context, and Methodological Note on Assistive Tooling}`); three replaced an existing section (`Palatini_Gauge_Attractor.tex` 15/−8, `ACS_Action_Identifiability.tex` 11/−4, `ACS_Condensate_Carrier_Boundary.tex` 11/−4, each dropping its `\section*{Acknowledgements ...}`); `Riemann_Spectral_Critical_Line.tex` 11/−1. So "moving the edits out" is a restore of the sealed bytes (`git checkout 389afe2^ -- <8 files>`), not a deletion of appended lines.
- **The PDFs did not move.** The verifier names no `.pdf`, so the 8 committed PDFs still match the seal: on `main` today the `.tex` carries the author statement and the published PDF does not.
- **What the tooling has, and lacks, for a new record.** `scripts/verify_publication.py:11` hard-codes `RECORD = ROOT/'docs/publication/2026-09-24'` and `:29` the marker `'% Publication amendment: 2026-09-24'` that each of the 33 amended sources must contain exactly once. The record directory holds `README.md, amendments.json, build-report.json, integrity-report.json, manuscript-baseline.json, provenance/, publication-manifest.json, receipt-relocations.json, science-report.json, style-and-research.md, visual-review.json` (`ls docs/publication/2026-09-24/`). **No script in the repository writes a manifest**: `grep -rl publication-manifest scripts/ code/publication_20260924/` → only the verifier. Both `scripts/verify_publication.py` and `scripts/build_papers.py` are themselves manifest-bound (the manifest's two `scripts/` keys), so re-pointing the verifier at a new record changes a sealed file and the new manifest must bind the new script bytes. `REPRODUCTION.md:44`: "`--update-pdfs` replaces the committed PDF copies and is intended for a reviewed publication update. The dated publication manifest binds source and PDF bytes; changing either requires a deliberate new preservation record, not an automatic rewrite of historical hashes."
- **Exactly what a new record requires**, read from the code: (1) rebuild the 8 PDFs with `python scripts/build_papers.py --paper <each of the 8> --update-pdfs` (`REPRODUCTION.md:38-44`); the 22 October rerun receipt reports all 35 sources building at `389afe2` with Tectonic 0.15.0 in 2 m 34 s ([`publication/2026-10-22-rerun.md`](publication/2026-10-22-rerun.md), row "Manuscript build") — that is the receipt's claim, not re-run for this brief; (2) a new `docs/publication/<date>/` with a `publication-manifest.json` whose `sha256` map (561 entries today: 417 `docs/`, 72 `code/`, 70 `papers/`, 2 `scripts/`) carries the new `.tex` and `.pdf` hashes, written by a sealing step the repository does not ship; (3) `verify_publication.py:11` pointed at the new directory, and `:29` left alone unless the 33 amendments are re-dated; (4) nothing in the 516 receipt references or the 16 relocations, which `389afe2` did not touch. **Re-sealing changes** the 8 `.tex` hashes, the 8 `.pdf` hashes, the two scripts' hashes if edited, and the record's own report files; it does not change the 2026-09-24 record, which stays as the historical seal.
- **Record of the state**: `.claude/skills/acs-framework/references/history.md` §8: "The publication integrity gate is red on main since 389afe2 (2026-09-29) ... REPRODUCTION.md requires a new preservation record for that; none has been made."

**Options.**

| | Costs | Breaks |
|---|---|---|
| **A. New preservation record.** | The four steps above, including writing a sealer; a dated, owner-signed event. | Nothing afterwards; CI green; the PDFs then carry the author statement. |
| **B. Restore the 8 sealed sources; carry the author statement in an unbound file** (`papers/README.md`, which `389afe2` already edited, or a new `docs/` page). | One commit. | Nothing; CI green at once; `.tex` and PDF agree again. The statement is then outside the manuscripts. |
| **C. Do nothing.** | Nothing now. | The gate stays red; every PR's check reads red regardless of its content. Brief 3 shows the cost: PR #14's merge adds a ninth failure (`manuscript inventory changed`) that a red-by-default gate does not surface. |

**Recommendation (the agent's).** B now, as the floor that makes the gate mean something again in one reversible commit; A when the owner wants the statement inside the published PDFs, because A is the only route that puts it there, and the same sealing step is what every later promotion (brief 1 option C, brief 3) will need. Writing the sealer once pays for all of them.

**If nothing is decided.** CI on `main` has been red since 2026-09-29; the signal that the seal exists to give is lost until one of A or B is done.

## 3. PR #14: constraint-projection framework

**Question.** Who reviews `claude/constraint-projection-framework-010dsu`, and does it merge (whole, partial, or archival), close, or stay?

**Evidence.**

- **Local**: 46 ahead, 12 behind (`git rev-list --count`); three-dot stat `83 files changed, 25655 insertions(+), 3 deletions(-)`; tip `eb52629` 2026-09-14 ("Our own fixed-point classification, stress-tested: three of its five claims falsified"); merge-base `29e5740`. **Merge-tree**: `CONFLICT (content)` in `MANIFEST.md` and `papers/README.md`; exit 1.
- **REST**: `state open, mergeable false, mergeable_state dirty, requested_reviewers 0, reviews 0, comments 0, review_comments 0, updated_at 2026-09-14T17:12:50Z, commits 46, changed_files 83, additions 25655`.
- **Content** (`git diff --name-only origin/main...<ref>` grouped): 39 under `code/constraint_projection`, 5 under `papers/notes`, 2 under `code/acs_codebase`, `papers/README.md`, and 8 under `docs/` (`specialist_fuzzy_dm.md`, `specialist_gauge_stress.md`, `specialist_method_prior_art.md`, five result JSONs). By type: 33 `.py`, 28 `.json`, 7 paths under `lean/`. Two new manuscripts with `\documentclass` and their PDFs: `papers/notes/Constraint_Projection_Framework.tex` and `..._Audit.tex`; **no change to `papers/catalog.json`**. 0 manifest-bound files touched.
- **What the gates say on the merged tree** (merge tree `3cd13ea` extracted to scratch with the two conflict markers left in place; not a resolved merge): `check_navigation.py --root <scratch>` → 1 failure, `catalog coverage differs: missing=['papers/notes/Constraint_Projection_Framework.tex', 'papers/notes/Constraint_Projection_Framework_Audit.tex']`; `verify_publication.py --integrity-only` there → `manuscripts 37` and `manuscript inventory changed` in addition to the 8 pre-existing mismatches. The catalog failure comes from `catalog.json` against `papers/**/*.tex` and is independent of the conflict markers.
- **Open verification inside the branch**: `docs/specialist_fuzzy_dm.md:3` "STATUS: complete — sections 1-6 written; instrument runs at exit 0; test gate NOT run, nothing committed"; `:645` "the number itself is unverified"; `:230` cites Hlozek+ 2015/2018 bounds from a figure.
- `docs/BRANCHES.md:27`: "Its findings have not been promoted into the published paper corpus by this cleanup."

**Options.**

| | Costs | Breaks |
|---|---|---|
| **A. Name a reviewer, resolve the two conflicts, merge whole, add catalog entries for the two notes.** | Review of 83 files; `manuscript inventory changed` → needs brief 2's new record. | The seal, until re-sealed. |
| **B. As A, but the two notes move out of `papers/` (e.g. to `docs/`), leaving the inventory at 35.** | Same review; two file moves. | Nothing in either gate: navigation green (no `\documentclass` under `papers/` added), inventory unchanged. |
| **C. Close the PR; retain the branch as BRANCHES.md does.** | Nothing. | Nothing; the branch keeps drifting (12 behind now). |
| **D. Delete.** | Loses the only copies: the two notes and PDFs, 33 instruments and 7 `lean/` paths, 28 result JSONs, three specialist reports. | — |

**Recommendation (the agent's).** B, with the fuzzy-DM report's "NOT run" and "unverified" lines merged as they stand rather than edited to look finished. It is the one option that lands the work on `main` with both gates green and without a seal event.

**If nothing is decided.** The PR stays `dirty`; the conflicts in `MANIFEST.md` and `papers/README.md` grow with every edit to those files on `main`.

## 4. PR #16: frontier delta

**Question.** Who reviews `codex/acs-frontier-delta-2026-09-12`, and does `main` take the whole 500 MB delta, only its README/scripts/proofs, or neither?

**Evidence.**

- **Local**: 27 ahead, 5 behind; three-dot stat `837 files changed, 3209930 insertions(+), 964 deletions(-)`; tip `6234df3` 2026-09-14; merge-base `173398b`. **Merge-tree clean**: exit 0, no `CONFLICT` lines.
- **REST**: `state open, mergeable true, mergeable_state clean, requested_reviewers 0, reviews 0, comments 0, updated_at 2026-09-14T07:40:25Z, commits 32, changed_files 989, additions 3246741, deletions 1031`. The local 27/837 and REST 32/989 differ because they count against different bases; both are given, neither corrected.
- **Content**: 583 files under `docs/frontier`, 231 under `code/frontier_verification`, 23 under `code/hp_knife_suite`; 389 files are not data by extension (filter: not `.json/.txt/.csv/.npy/.npz/.dat/.log/.tsv`); 27 `verify_*_delta.py`; 15 `.lean`; one `riemann_zeros_220_certified` file; it edits `docs/frontier/README.md`, a page the navigation check reads. 0 manifest-bound files, 0 `papers/*.tex`. **Size**: `git ls-tree -r -l` over the 837 changed paths at the tip sums to **500.1 MB**.
- **Not done here**: the merged tree was not extracted and the navigation/integrity checks were not run on it (500 MB, time box). Clean merge-tree is a conflict statement, not a gate statement. The item's "22 checkpoint directories" could not be confirmed by a `checkpoint|ckpt` path pattern (0 matches); the "one diagnostic receipt with an empty source-hash map" was not located by two grep patterns and remains unverified.
- **Open inside the branch**: `code/frontier_verification/SIGNED_CORNER_README.md:3` still contains "remains open" (the source-feasible threshold). `docs/BRANCHES.md:21`: "Review this delta against the current publication before integration."

**Options.**

| | Costs | Breaks |
|---|---|---|
| **A. Name a reviewer; merge whole.** | A 500 MB increment to every clone; the review of 389 non-data files. | Unknown until the two gates are run on the merged tree; no sealed file is touched. |
| **B. Merge README, scripts, proofs and the certified zeros; keep checkpoint data on the branch or as a release asset referenced by hash.** | Splitting the branch; the data's provenance moves to a pointer. | Any receipt that hashes a file left out would fail if it is verified in-tree. |
| **C. Close the PR; retain the branch.** | Nothing. | Nothing; the clean state is not guaranteed to persist (5 behind now). |
| **D. Delete.** | Loses 27 scripts, 15 proofs, the certified zeros table, 583 result files. | — |

**Recommendation (the agent's).** A reviewer first; then run `check_navigation.py` and `verify_publication.py --integrity-only` on the merged tree before any merge, which this brief did not do. Between A and B, B unless the reviewer finds that receipts in the branch hash the data files in-tree, in which case the data must come with them.

**If nothing is decided.** The PR stays open and clean today; nothing on `main` references its 27 scripts or 15 proofs.

## 5. The Exodus kill commit: merge or drop

**Question.** Does `e4bc971` on `claude/papers-repo-analysis-kce6bn` merge so the kill "ACS explains the Exodus electrostatic anomaly" is recorded in the published ledger, or is the route dropped with the branch?

**Evidence.**

- **Local**: 1 ahead, 13 behind; tip `e4bc971` 2026-08-12, `ledger: kill "ACS explains the Exodus electrostatic anomaly" (T2, three grounds)`. `git show --stat`: `.claude/skills/acs-framework/SKILL.md +12`, `MANIFEST.md +10`, `docs/Elimination_Ledger.md +92`, `docs/Exodus_Electrostatic_Anomaly_Analysis.md +272` (new); 4 files, +386/−0. **Merge-tree clean**, exit 0. 0 manifest-bound files.
- **On `main`**: `grep -rniI exodus` hits only `docs/BRANCHES.md:41`; `grep -c 'External-application' MANIFEST.md` → 0; `docs/Elimination_Ledger.md` has no Exodus entry. The branch is the only copy of the analysis and of the ledger entry.
- **The document's own label** (branch copy, lines 1-6): "Verdict: NO — the proposed bridge is KILLED on three independent structural grounds", "Tier: T2 structural (K1–K3) / external experimental evidence (§4)". Its one transferable discriminator, from the same document: "does the force require the leakage current? ... If it is genuinely current-independent, ACS has nothing to say by K2 and the route should be abandoned rather than repaired." Nothing in either repository runs that test.
- `docs/BRANCHES.md:41`: "The merged PR does not justify deleting this branch."

**Options.**

| | Costs | Breaks |
|---|---|---|
| **A. Merge the commit as-is.** | A clean merge; the ledger gains a kill, `MANIFEST.md` a paragraph, the skill 12 lines. | Nothing in the gates. |
| **B. Cherry-pick only the analysis and the ledger entry.** | Dropping the `MANIFEST.md`/skill text means writing the pointer elsewhere. | Nothing. |
| **C. Drop the route; delete the branch.** | The kill is recorded nowhere on `main` but `BRANCHES.md:41`. | The ledger's append-only kill log is incomplete by one entry. |

**Recommendation (the agent's).** A. The ledger exists to keep kills, the commit merges clean, and recording a kill does not close the discriminator; that stays open under either choice and should be said so in the ledger entry.

**If nothing is decided.** The only copy stays on a 13-behind branch protected by one sentence in `BRANCHES.md`.

## 6. Absolute-path exposure: one policy, and the redaction branch

**Question.** Is the repository's policy on local absolute paths (`/Users/<name>/...`) in published receipts "redact" or "map-and-preserve", and accordingly does `claude/public-ip-exposure-audit-6zxyf4` merge or close?

**Evidence.**

- **The branch**: tip `93c9459` 2026-08-10, 1 ahead, 16 behind; merge-tree clean (exit 0); six files, 0 manifest-bound. Names and hunk counts (`git diff origin/main...<ref> -- <file> | grep -c '^@@'`): `docs/ACS_Antigravity_Feed_Package/verification_report.json` 1, `docs/Cross_Repo_Glossary_Extract.md` 3, `docs/issue7_logs/cross_model_stdout.txt` 1, `docs/issue7_logs/exhaustive_stdout.txt` 1, `docs/issue7_logs/long_range_stdout.txt` 1, `docs/issue7_verification_report.json` 1; numstat 2/2, 12/14, 1/1, 1/1, 1/1, 12/12. On `main` those six hold 2, 0, 1, 1, 1, 12 `/Users/` lines (`git show origin/main:<f> | grep -c '/Users/'`); on the branch, 0 each. The glossary change is cross-repository detail, not paths.
- **The corpus today** (`grep -rIc --exclude-dir=.git '/Users/' .`): **688 lines in 56 files** (785 path tokens by `grep -o`). Of those, **440 lines in 25 manifest-bound files** and **248 lines in 31 unbound files**. Top carriers: `docs/condensate_energy/endpoint_audit/archive-rescreen.json` 248 (bound), `docs/frontier/2026-09-12-delta/Lean_Audit_v434.json` 45, `docs/condensate_energy/source-reconciliation-20260924.json` 40 (bound), three `Formal_Audit.json` 38/31/24. The branch's 17 lines are 2.5% of 688; 64% of the exposure sits under the seal.
- **Some paths are load-bearing.** `docs/publication/2026-09-24/receipt-relocations.json` holds 16 absolute paths as keys; `scripts/verify_publication.py:33-37` uses them to relocate 16 receipt references (`relocated_references: 16` in the integrity report). Redacting that file breaks the verifier. Of the 31 unbound carriers, 4 are hash-checked through the endpoint receipt (`finite_matching/.../run.log`, `action_matching/.../acs-action-spectrum-run1.log`, `endpoint_audit/attempts/phase6-timeout-60s/driver.log`, `radiative_flat_modes/.../run.log`), so redacting them fails `archived receipt mismatch`.
- **The branch's own caveat** (`history.md` §7): "this does not remove the previously published content from git history, and the repository is public." `docs/BRANCHES.md:53`: "retained for review against current provenance and preservation requirements; this cleanup does not apply the redactions." No policy text exists in either repository.
- The exposure is a home-directory username and layout, not a credential.

**Options.**

| | Costs | Breaks |
|---|---|---|
| **A. Policy: map-and-preserve.** Paths are provenance; relocation maps resolve them; write the policy in one paragraph (REPRODUCTION.md or BRANCHES.md); close the branch. | A paragraph. | Nothing. |
| **B. Policy: redact going forward.** Apply the branch (17 lines) and a scripted pass over the 27 unbound, un-hashed carriers (248 − the 4 hash-checked files' lines); leave the 25 bound files and the 4 hashed logs until a new record (brief 2). | A tracked-path rewrite; two regimes in the tree until re-sealing. | Nothing in the gates if the 29 load-bearing files are left alone; the first future receipt reintroduces paths unless generators change. |
| **C. Redact everything including history.** | Rewrites every SHA recorded in `BRANCHES.md`, `branch-audit/2026-09-24.json`, and the publication record. | The preservation discipline. |

**Recommendation (the agent's).** A. Two thirds of the exposure is sealed, part of it is load-bearing, and the content is already in public history; the branch's 17 lines buy no privacy. The policy paragraph is what is missing, not the redaction.

**If nothing is decided.** Two policies coexist; each new receipt adds paths (the 24 September record added 16 after the branch was cut), and the branch ages.

## 7. The "reconciled" ruling on the infinity-zero branch

**Question.** Does the owner rule `claude/infinity-zero-scaled-invariance-vzm54b` reconciled with `main` and retire the ref?

**Evidence.**

- **Local**: tip `ef82e58` 2026-07-14, 1 ahead, 73 behind; three-dot: 4 files (`MANIFEST.md +2`, `README.md +12/−2`, `code/notes_verification/test_scaled_invariance.py +247`, `papers/methodology/Scaled_Invariance_of_Infinity_and_Zero.tex +234`).
- **The test is byte-identical on `main`**: `git diff --quiet origin/main <ref> -- code/notes_verification/test_scaled_invariance.py` → exit 0.
- **The paper differs by 29 lines** (`git diff --stat <ref> origin/main -- <paper>` → `29 +++-`): `main`'s copy carries the `% Publication amendment: 2026-09-24` marker (1) and the branch's does not (0). `main`'s copy is manifest-bound (the branch is the only one of the five that touches a sealed file: 1). `MANIFEST.md` and `README.md` have moved 101 and 172 lines past it.
- **Merge-tree**: `CONFLICT (add/add)` on the paper, `CONFLICT (content)` on `MANIFEST.md` and `README.md`; exit 1. Merging would also edit a sealed source and add a ninth mismatch.
- **Already written**: `docs/BRANCHES.md:13` (22 October): "its test file is byte-identical ... and its paper is on `main` in the amended form, so the branch holds nothing `main` lacks; the 'reconciled' ruling this page asks for before retirement is the owner's, and this note is the evidence for it, not the ruling." `docs/BRANCHES.md:47`: "Retain the branch until its surviving differences are explicitly reconciled." The full SHA is recorded at `BRANCHES.md:45` and in `branch-audit/2026-09-24.json` (`disposition: retain_unmerged`).

**Options.**

| | Costs | Breaks |
|---|---|---|
| **A. Rule "reconciled"; delete the ref; one dated line in BRANCHES.md.** | One line. | Nothing; the objects stay reachable by the recorded SHA. |
| **B. Keep.** | Nothing. | Nothing; a 73-behind branch with an add/add conflict stays listed as awaiting a ruling. |
| **C. Merge.** | Conflict resolution. | The seal (one bound source) for no content `main` lacks. |

**Recommendation (the agent's).** A.

**If nothing is decided.** `BRANCHES.md` keeps asking for a ruling its own 22 October note already evidences.

## What this page did not do

It ran no science checks and no builds; it did not extract or gate-check PR #16's merged tree; it did not test the Exodus current-independence discriminator; it did not resolve any conflict; it changed no manifest-bound file. Every number above has its command next to it, and the agent's recommendations are labelled as such throughout.
