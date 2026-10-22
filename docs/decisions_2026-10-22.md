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

## Part 2: science and authorship

Decision briefs written 22 October 2026 by an agent session (key `dec-science`) for the
owner. Each brief is a map, not a ruling: the question in one sentence, the evidence with
`file:line` as it stands at `badb0b7` (branch `claude/surrogate-discriminant-amendments`),
the options with their costs, a recommendation labelled as the agent's, and what happens
if nothing is decided. Every `file:line` below was re-grepped before this file was
written; every number carries the command that produced it. Nothing in this part edits a
manifest-bound file; the paste-ready LaTeX for the two manifest-bound amendments that
brief 2.1 proposes is in [proposed amendments, pass 2](proposed_amendments_2026-10-22_pass2.md).
Paths are relative to the repository root unless they begin with `AISO:` (the
`tensorrent/AISO-UI-for-Ai` tree, read at `4fd37e0` on branch
`claude/excel-memory-offloading-9ezwrv`).

---

### 2.1 The Higgs-quartic / m_H / RG-scale chain (candidate 2)

**Question.** Which of the three printed characterisations of the quartic chain
(λ_ACS = 2√3/27 ≈ 0.1283 against λ_SM ≈ 0.1294, and the running that connects them)
does the corpus assert, given that the three manuscripts that carry them are all
manifest-bound and no document arbitrates?

**The three characterisations, verbatim.**

(A) Paper A, `papers/core_trilogy/Palatini_Gauge_Attractor.tex:2450-2459` (App. B,
*Higgs quartic coupling*):

> **RG evolution:** Running the SM couplings to $M_P$ gives $\lambda(M_P) \approx -0.005$
> (the Higgs near-criticality). Running the ACS value downward yields
> $\lambda(M_Z) \approx 0.18$ ($m_H \approx 148$~GeV, 18\% overshoot). This indicates the
> ACS algebra is realised at the Pati--Salam scale $\Lambda_{\mathrm{PS}} \sim 10^{15}$~GeV,
> not $M_P$, or that torsion partners modify the running above the TeV scale. The
> *algebraic* match ($0.85\%$) is the relevant comparison; the RG scale is a separate,
> open problem. (Verified: `four_computations.py`.)

together with `:2021` "No free parameters, no fitting, no external input." (immediately
followed at `:2023` by "**Epistemic status: partial derivation.**") and `:2469` "No free
parameters." (strong coupling subsection).

(B) Paper B′, `papers/core_trilogy/Spectral_Witness_Refinement.tex:312` (§12.2, tier T4):

> The quartic crosses $\lambda_{\text{ACS}}=0.1283$ exactly once, at $\mu\approx132$~GeV ---
> $0.05$ e-folds above $m_H$, essentially at the electroweak scale --- then falls
> monotonically [...] The high-scale reading is thus falsified: were
> $\lambda_{\text{ACS}}$ a high-scale boundary value, it would have to match
> $\lambda_{\text{SM}}$ run *up* to that scale ($\sim0.008$--$0.04$), not the EW-scale
> $0.1283$. The algebraic quartic matches the *physical, electroweak-scale* value directly.
> The $0.85\%$ is therefore an EW-scale normalisation offset [...] not running, and not a
> high-scale boundary condition.

and the same paper's `:255` (§9.4, tier T2): "Through this validated chain, the
obstruction's central content is a *charge*, not a coupling", where "this validated chain"
is the Killing-form/Koide chain of `:249-254` that reproduces $m_H = 124.72$ GeV.

(C) Action paper, `papers/updates/ACS_Action_Identifiability.tex:267-275` (§6, *Running
does not supply the missing selector*):

> The historical source's one-loop SM truncation gives the three conditional pairs
> $(\lambda_{\rm UV},\lambda_{\rm IR})\simeq (0.08,0.1685520),\ (0.1283001,0.1806315),\
> (0.18,0.1898121)$. [...] The comparison input is $0.1294$. The middle RG output
> corresponds to an approximately $148$ GeV tree mass proxy, not a pole-mass prediction.
> Mixed historical input conventions and omitted thresholds preclude a precision
> phenomenological interpretation.

`:287-288`: "Neither gives $2\sqrt3/27$. These are roots of a fixed-gauge proxy, not fixed
points of the complete running action." `:306-308` (§7): "A numerical minimizer cannot
choose which allowed action nature uses, and a source expression matched to an inserted
value does not derive that value."

**What each would require to be true.**

- (A) requires a scale $\mu^\ast$ at which the SM quartic equals 0.1283 *and* a reason the
  algebra fixes λ at $\mu^\ast$. Its own numbers deny the first half: a boundary of 0.1283
  at $M_P$ lands at 0.18, not 0.1294 (`:2452-2453`), and the "Pati–Salam scale" rescue is
  asserted, not computed. (A)'s "No free parameters" sentences are true of the *algebraic*
  factors (`:2015-2021`) and silent about the inserted comparison value and the RG inputs.
- (B) requires that λ_ACS be identified with λ(μ ≈ m_H), and that the 0.85 % be a
  tree/threshold matching effect. (B)'s own §12.3 (`:314-317`) states the mechanism of that
  offset "remains underived", so (B) is a falsification of (A) plus an identification
  whose derivation is open. (B)'s §9.4 word "validated" means "the chain reproduces the
  manuscript's 124.7 GeV", i.e. agreement with an inserted value.
- (C) requires nothing further: it classes the chain as a conditional calculation whose
  output (0.1806315 at $\lambda_{\rm UV}=0.1283001$) is *not* the comparison input, with
  explicit boundary sensitivity $d\lambda_{\rm IR}/d\lambda_{\rm UV}=0.2088898$
  (`:271-272`), and withholds the word "derive" from the 0.85 % match.

**Which the 24 September record supports.** (C), and only (C).

- `docs/condensate_energy/endpoint_audit/README.md:92-98` (manifest-bound; `grep -c` = 1):
  "Setting the upper-scale quartic to 2√3/27 produces a lower-scale quartic **0.1806315**,
  not its comparison input 0.1294. The resulting tree mass proxy is about **148 GeV**; this
  is not a pole-mass calculation. [...] The independently checked local sensitivity
  dλIR/dλUV is **0.2088898**, not zero."
- `docs/publication/2026-09-24/science-report.json` (58 checks passed, `:4`) pins this
  with the named checks `conditional source RG reaches UV` (`:184`), `perturbed boundary
  reaches IR -1e-05` / `1e-05` (`:189`, `:194`), `finite running retains sensitivity`
  (`:199`), `phase6: zero proposed Higgs number is not a proxy root` (`:249`) and
  `phase6: nonzero proposed Higgs number is not a proxy root` (`:264`).
- `docs/publication/2026-09-24/README.md:14`: "Finite RG flow retains measurable
  dependence on boundary data."
- The record does **not** withdraw (A): `docs/publication/2026-09-24/amendments.json`
  entry [21] (Paper A) and the in-paper copy at
  `Palatini_Gauge_Attractor.tex:2979-2980` withdraw two inferences (torsion wave operator,
  colour singlet) and say nothing about the quartic chain; the governance clause at
  `:190-193` ("That amendment governs earlier physical interpretations") therefore does
  not reach App. B. Nor does the record endorse (B)'s positive identification; it is
  consistent with (B)'s *negative* (the crossing near m_H) because both are the same
  one-loop computation read in opposite directions.

**Cheap check run now** (one-loop SM RGE, $V=\lambda(H^\dagger H)^2$, inputs at $M_Z$:
$g'=0.3576$, $g_2=0.6517$, $g_3=1.2177$, $y_t=0.9369$; no thresholds; script
`scratchpad/actionable2/dec-science-checks/rge_check.py`, command
`acs-venv/bin/python -I rge_check.py`):

| run | result |
|---|---|
| up from $\lambda(m_H)=0.1294$: crossing of 0.1283 | $\mu = 133.0$ GeV, 0.060 e-folds above $m_H$ (B′ says 132 GeV, 0.05) |
| up: $\lambda(10^{15})$ | 0.0025 (B′'s table: 0.0091; the difference is input choice, both are far below 0.1283) |
| down from 0.1283 at $M_P = 1.22\times10^{19}$ | $\lambda(M_Z)=0.1816$, $\sqrt{2\lambda}\,v = 148.4$ GeV (record: 0.1806315 / ~148) |
| down from 0.1283 at $\Lambda_{\rm PS} = 10^{15}$ | $\lambda(M_Z)=0.1849$, $\sqrt{2\lambda}\,v = 149.7$ GeV |

The last row is the one (A) needed and did not compute: moving the boundary from $M_P$ to
$10^{15}$ GeV moves $\lambda_{\rm IR}$ *away* from 0.1294 in this run, not toward it. This
is one-loop with one input set; it is a check on (A)'s sentence, not a new result.

**Options.**

1. **Amend Paper A and Paper B′ by claim-specific appendices** (both manifest-bound →
   integrity gate): withdraw the Λ_PS sentence at `:2454-2456`, qualify `:2021`/`:2469`
   to "no free parameters in the algebraic factors; the comparison value and the RG inputs
   are inserted", and in B′ replace "validated chain" (`:255`) with "chain that reproduces
   the inserted value". Paste-ready LaTeX: proposed amendments pass 2, §1 and §2. Cost: two
   manifest hashes change, so the owner must re-baseline the preservation record or file a
   dated amendment record alongside it. Breaks nothing computational; `four_computations.py`
   and the endpoint checks are untouched.
2. **Arbitrate outside the manuscripts**: add a 2026-10-22 entry per paper to
   `docs/publication/2026-09-24/amendments.json` (not manifest-bound: `grep -c` = 0) stating
   that (C) governs (A) and (B)'s §9.4 wording. Cost: one JSON edit; the manuscripts keep
   printing (A) and (B) and the reader must find the JSON.
3. **Leave as is.** Three readings stay in print; readers of each paper get a different
   epistemic status for the same number.

**Recommendation (agent's).** Option 2 now, option 1 queued through the integrity gate.
The record already contains the arbitration in numbers; what is missing is one sentence
saying so where the manuscripts' readers look.

**If nothing is decided.** The `.claude/skills/acs-framework/references/core-trilogy.md:330`
summary continues to teach (A) ("⇒ the algebra is realised at Λ_PS ~ 10¹⁵ GeV") to every
future session, which is how this item was regenerated six times (`merged_from` 88, 162,
203, 214, 215, 236).

---

### 2.2 The byline on the two supporting papers (candidates 40, 81)

**Question.** Who is named as author of `docs/surrogate_discriminant_amendments.tex` and
`docs/instrument_floors.tex`, and does the corpus author statement extend to them?

**Evidence.**

- Title blocks. `docs/surrogate_discriminant_amendments.tex:21-24`:
  `\author{Amendments to FF06e\\ \small Instrument: B.\ Wallace (TensorRent). Amendments,
  propositions and measurements: agent record, 21 October 2026.\\ \small Byline unset
  pending the author's decision --- see \textbf{Contributions}, final page.}`.
  `docs/instrument_floors.tex:53-54`: `\author{\small Agent record, 21 October 2026. Byline
  unset --- see \textbf{Contributions}.\\ \small Prior instrument: B.\ Wallace (TensorRent),
  FF06e.}`.
- Contributions footers. Surrogate `:527-535`: the discriminant, vocabulary and framing
  "are due to FF06e"; "The three propositions of §…, the descent recasting of §…, the
  four-tier verdict, both corpora, and the interpolation finding of §… are this record's."
  Floors `:854-861`: criteria I–III, the three-character action, both instruments, all six
  figures and the artifact localisation "are this record's. Byline deliberately unset."
- Status boxes. Surrogate `:62-67` and floors `:93-98`: "Its propositions and measurements
  are not part of the corpus author statement".
- The precedent. `docs/ym_comparison_methodology_paper.tex:13`:
  `\author{\textbf{Bradley Wallace} \\ \textit{TensorRent Research} \and \textbf{Operator-AI}
  \\ \textit{Google DeepMind Pair-Programming Subsystem}}` — an AI co-author line, in the
  same `docs/` placement, outside the inventory (`docs/README.md:50`).
- The corpus author statement. `docs/publication/2026-09-24/README.md:45`: "Brad Wallace's
  sole intellectual authorship [...] All novel theories, models, and hypotheses represent
  approximately 5,000–6,000 hours of independent work by the author"; `papers/README.md:77`
  ("across this 35-paper corpus"); `CITATION.cff` (`authors:` lists Wallace only); in each
  canonical manuscript, e.g. `Palatini_Gauge_Attractor.tex:2389`: "the conceptual genesis,
  physical synthesis, and mathematical architecture originate solely with the human
  author". Introduced by commit `389afe2` (2026-09-29).
- Neither doc is in the manifest (`grep -c docs/surrogate_discriminant_amendments.tex
  publication-manifest.json` = 0; same for `docs/instrument_floors.tex`), so the byline edit
  needs no integrity gate.
- The AISO copies are **not** identical to these (the pass-1 verdict said they were):
  `AISO:docs/research/papers/Surrogate_Discriminant_Amendments.tex:22` reads "Amendments and
  measurements: this record." with no "Byline unset" sentence and no status box
  (`diff` shows `22c22,24` and `59a62,69`); `Instrument_Floors.tex` differs at `:47`
  (`\input{Instrument_Floors_data}`) and lacks the status box (`92a93,101`). Whatever is
  decided has to be applied in both trees or the two copies will carry different authors.
- Building is no longer blocked (pass-1 premise fell): both PDFs were built and committed
  (`f2902c4`, `979596a`); what the unset byline still gates is promotion and citation.

**Options and what each implies for the corpus author statement.**

| option | title block | Contributions footer | corpus statement (`docs/publication/2026-09-24/`) |
|---|---|---|---|
| (a) owner sole author, agent acknowledged | `\author{Bradley Wallace}` + an acknowledgement line naming the agent session as instrument | must be rewritten: "are this record's" becomes "were produced with assistive tooling directed by the author", in the corpus's own words | the statement's "sole intellectual authorship" clause extends to these docs; the status boxes' "not part of the corpus author statement" sentence must be deleted, and the papers move inside the claim the statement makes, though they stay outside the 35-paper inventory |
| (b) AI co-author line, as the precedent | `\author{Bradley Wallace \and <agent designation>}` on the `ym_comparison` pattern | kept as written (it already divides the credit the way the line would) | unchanged: the docs stay outside the statement, which is what their status boxes already say; the statement's "sole" clause keeps its scope at the 35 papers |
| (c) leave unset | as now | as now | unchanged |

Costs. (a): the Contributions footers currently say the propositions and measurements are
the agent record's; (a) replaces an accurate provenance line with the corpus's assistive
framing, and the owner takes on the claims (the surrogate paper itself says at `:57-58`
"None of the three propositions is new as statistics"). (b): keeps provenance as written and
follows the house precedent, but most venues' policies refuse an AI name in an author list,
so (b) is a repository byline, not a submittable one. (c): the PDF title page prints "Byline
unset"; nothing can be cited.

**Recommendation (agent's).** (b) in the repository, because it is the only option under
which every sentence already in the two papers stays true, with (a) as the form to switch
to at submission time, when the Contributions footer would be rewritten in the same edit.
Apply the same line to the AISO copies.

**If nothing is decided.** The two PDFs stay readable from `docs/README.md:51-52`, uncitable,
on a branch with no PR (`docs/BRANCHES.md:13`), and the AISO copies keep a different author
line from the acs copies.

---

### 2.3 Where the reproduction chain lives (candidates 52, 83)

**Question.** Should the TypeScript instruments that reproduce the two supporting papers be
vendored into `code/`, reached through a merged AISO `main`, or left as the present
cross-repository pin?

**Evidence.**

- The pin is now `55088af`, not `3a8e610` (pass-1 verdicts are stale on this): re-pinned
  in `979596a`; `docs/instrument_floors.tex:778-782` and
  `docs/surrogate_discriminant_amendments.tex:461-466` both say "The pin is commit
  `55088af`: the four instrument files, the two zero-and-witness scripts and the lattice
  test are byte-identical from the generating commits (`086a0e3`, `64d9658`) through it",
  followed by `git checkout 55088af96d4a3c282d3c8da44d7827ecbe904ddf`.
- The dependency *is* declared: `docs/REPRODUCTION.md:93` names the repository, the branch,
  the pin, the commands, and says "Promoting those instruments into `code/` here is an open
  owner decision". Pass-1 said REPRODUCTION.md had no mention; it does now.
- Reachability in AISO (commands run in `/home/user/AISO-UI-for-Ai`):
  `git branch -a --contains 55088af` → only `claude/excel-memory-offloading-9ezwrv` (local
  and `origin/`); `git merge-base --is-ancestor 55088af origin/main` → NO.
- AISO PR #17 (`gh api repos/tensorrent/AISO-UI-for-Ai/pulls/17`): open, head
  `claude/excel-memory-offloading-9ezwrv` at `4fd37e0`, base `main`, 640 commits, 922 files,
  +230,877 / −10,158, 0 reviews, 0 requested reviewers, `mergeable: true`,
  `mergeable_state: unstable`. Check-runs on the PR head: 12, all `failure`. Check-runs on
  `origin/main` head `1165230`: 6, all `failure` — so red CI is the repository's state, not
  the PR's.
- Import closure, computed by a script that follows every relative `import`/`export … from`
  and dynamic `import()`/`require()` from the ten files the papers cite (`frontend/` as
  root; sizes from `os.path.getsize`):

  | set | files | bytes |
  |---|---|---|
  | the 10 cited files (`src/{shuffle-knife,riemann-siegel,rotor-field,rotor-dynamics}.ts`, `scripts/{riemann-witnesses,riemann-positions,paper-figures}.mts`, `tests/{rotor-dynamics,shuffle-knife,riemann-siegel}.test.ts`) | 10 | 143,820 |
  | transitive closure | 21 | 292,096 |
  | closure without the three tests | 18 | 221,115 |

  The 11 pulled-in files (148,276 bytes: `telemetry.ts` 50,502, `invariants.ts` 14,935,
  `motif-cas-store.ts` 14,135, `regex-topology.ts` 13,035, `content-cell-grid.ts` 12,570,
  `curriculum.ts` 12,310, `reverse-map.ts` 9,417, `procedure-verify.ts` 8,119,
  `procedure-template.ts` 4,747, `action-sequences.ts` 4,622, `assimilation.ts` 3,884) enter
  through **one** import: `import { pctOf } from "./telemetry.js"` at `rotor-field.ts:55`
  and `rotor-dynamics.ts:75`. `pctOf` is a five-line percentage formatter
  (`telemetry.ts:861-865`). External imports across the 21 files: `fs`, `path`, `url`
  (Node built-ins), `vitest` (tests only), `@noble/hashes/sha2.js` (one substrate file).
  Checked-in output: `docs/instrument_floors_data.tex`, 3,031 bytes.

**Options.**

1. **Vendor into `code/`.** Either the full closure (21 files / 292,096 bytes, 11 of them
   AISO substrate organs with no bearing on the papers) or a trimmed copy: the 10 cited
   files (143,820 bytes) with the two `pctOf` imports replaced by a local five-line helper.
   Cost: a Node toolchain (`tsx`, `vitest`) in a `code/` tree whose checks are Python
   (`scripts/verify_science.py`, `scripts/check_navigation.py`); two copies to keep
   byte-identical; the papers' "byte-identical to the generating runs" sentence must be
   re-stated against the vendored hashes. Gains: acs-framework reproduces itself.
2. **Merge AISO PR #17 and re-pin to `main`.** Cost: merging 640 commits / 922 files
   unreviewed and CI-red for the sake of ten files; nothing I may do. Gain: the SHA
   `55088af` stays valid after a merge (merges keep SHAs), so the papers need no edit —
   only the sentence naming the branch goes stale. A smaller route with the same gain is a
   dedicated PR carrying only the ten files' history.
3. **Keep the cross-repo pin.** Cost: the SHA is reachable only from one unmerged branch;
   if that branch is deleted before merge the pin is still fetchable by SHA for a while but
   no longer advertised. Mitigation at zero edit cost to acs-framework: a tag on AISO
   (`git tag repro/instrument-floors-2026-10-22 55088af && git push origin --tags`), which
   makes the SHA reachable regardless of the branch's fate.

**Recommendation (agent's).** 3 with the tag, now; 2 by a ten-file PR as the durable fix;
1 only if the owner wants `code/` self-contained, and then the trimmed 10-file copy, never
the 21-file closure.

**If nothing is decided.** Reproduction works exactly as the papers say for as long as the
branch exists; `REPRODUCTION.md:93` already tells the reader so.

---

### 2.4 Paper A's h̃/h = 2/3: matrix-level or invariant-level (candidate 73)

**Question.** Which reading of the Yukawa ratio h̃/h = 2/3 does Paper A assert, and what
does the choice change?

**Evidence.**

- `code/acs_codebase/README.md:128` (not manifest-bound; `grep -c` = 0), known limitation 4:
  "**§7 of Paper A (h̃/h = 2/3 interpretation).** Whether this is matrix-level
  proportionality or invariant-level ratio determines whether `paper_a/yukawa_no_go.py` is
  an unconditional theorem or a strong indication. The codebase tests both
  interpretations; see the script docstring." `docs/PaperA_changelog.md:154-157` keeps it
  as open item 1.
- The pointer "§7" does not resolve: Paper A has six numbered sections (`:249`, `:306`,
  `:738`, `:901`, `:1553`, `:1801`) and then appendices; the ratio is stated at `:2168`
  (parameter ledger: "h̃/h & 2/3 & Koide ratio"), `:2187-2188` ("the ratio h̃/h is an RG
  invariant (identical representations ⇒ identical anomalous dimensions)"), `:2621-2623`
  and `:2813`.
- Paper A's own definition is a **norm ratio**, `:2621-2622`: "The Yukawa ratio
  $\tilde{h}/h = \|[f,g]\| / \|[[f,g],g]\| \approx 2/3$ (from bracket norms; [...])".
- The script, `code/acs_codebase/src/paper_a/yukawa_no_go.py` docstring: "NOTE: this
  theorem holds regardless of the precise form of h, hTilde, including the case hTilde =
  (2/3) h (matrix-level Palatini). It does NOT depend on the interpretation of the hTilde /
  h = 2/3 relation." `yukawa_no_go_test` runs both cases.
- `docs/condensate_energy/family_boundary/README.md:63`: "Equal positive VEVs make the
  matrices identical for arbitrary independent Yukawa matrices [...] Matrix proportionality
  is not required for this specific obstruction."
- `docs/condensate_energy/selection_energy/README.md:100-102`: "If Ỹ=(2/3)Y, both Dirac mass
  matrices are scalar multiples of the same matrix. Their left mass squares commute, all
  generation ratios are identical, and there is no physical mixing among nondegenerate
  masses. [...] A **norm-only** relation between two otherwise independent matrices is a
  different hypothesis. An explicit noncommuting example satisfies the same norm ratio, so
  the proportionality obstruction does not exclude it. Its matrix orientations and flavor
  data remain inputs."

**The two readings and what differs.**

| | (M) matrix-level: h̃ = (2/3) h | (I) invariant-level: ‖h̃‖/‖h‖ = 2/3, orientations independent |
|---|---|---|
| equal-VEV no-go (Phase 52, `yukawa_no_go.py`) | holds | holds |
| κ₁ ≠ κ₂ | M_u and M_d are multiples of one matrix for **every** tan β → V_CKM = 1 always (`selection_energy/README.md:100`) | mixing possible; orientations are inputs (`:102`) |
| consequence for Paper A | the minimal bi-doublet sector cannot produce CKM at any tan β, which contradicts the CKM programme of Appendix "Status of the CKM Derivation" (`:2573`) | the CKM programme stays open; the ratio constrains magnitudes only |
| supported by Paper A's wording | no | yes (`:2621-2622`, "from bracket norms") |

So the README's framing is inverted: the theorem is unconditional under both readings (the
script and `family_boundary:63` say so); what the reading decides is whether the *model*
survives beyond the equal-VEV point. (M) is the stronger obstruction and would withdraw
Appendix C; (I) is what the text defines.

**Options.** (1) Rule (I); rewrite README limitation 4 and changelog open item 1 to say
"the theorem is unconditional; the reading fixes whether mixing is possible off the
equal-VEV point; Paper A defines the ratio by bracket norms, i.e. (I)". Both files are
outside the manifest. (2) Rule (M); then Paper A's CKM appendix needs an amendment
(manifest-bound). (3) Leave open; the stale "§7" pointer stays.

**Recommendation (agent's).** (1). Paste-ready replacement for `README.md:128`:

> 4. **Paper A's h̃/h = 2/3 (ledger `:2168`, definition `:2621`).** Paper A defines the
> ratio by bracket norms, an invariant-level relation; `paper_a/yukawa_no_go.py` is
> unconditional under both that reading and matrix-level proportionality (its docstring, and
> `docs/condensate_energy/family_boundary/README.md`). What the reading decides is the model
> off the equal-VEV point: matrix-level proportionality forbids CKM mixing at every tan β
> (`docs/condensate_energy/selection_energy/README.md`), the norm-only reading leaves the
> orientations as inputs.

**If nothing is decided.** Each new session re-opens the item from the README (this one
arrived as candidate 533 → 73).

---

### 2.5 Whether the paste-ready amendments enter the six manuscripts (candidate 80)

**Question.** Do the five paste-ready amendments in
`AISO:docs/research/ACS_PAPER_AMENDMENTS_2026-10-21.md` enter their target manuscripts,
and is FF06e's Definition 2 amended in the canonical paper and `amendments.json`?

**Evidence.** Each amendment, its target, and the manifest check
(`grep -c "<path>" docs/publication/2026-09-24/publication-manifest.json`):

| § in the AISO doc | amendment (its `\section*` title) | target file | manifest |
|---|---|---|---|
| 1.3 (`:104`) | *Condorcet figures and the reported quantity* — 7 %/43 %/78 %/99 % → 8.8/47.2/82.0/98.7 | `papers/later_FF06_series/When_a_Number_Lies.tex` | 2 → bound |
| 2.3 (`:175`) | *a fourth mechanism, and the scope of clause (ii)* | `papers/later_FF06_series/When_a_Number_Lies.tex` | 2 → bound |
| 3.7 (`:313`) | *Definition 2, in three parts* (targets `def:ff`, `Spectral_Rigidity_Shuffle_Knife.tex:67`) | `papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex` (FF06e, `:36`) | 2 → bound |
| 4.3 (`:385`) | *the unconverged-instrument trap* | `papers/later_FF06_series/The_Elimination_Ledger.tex` | 2 → bound |
| 5.5 (`:517`) | *the completeness inference, tested* | `papers/later_FF06_series/Three_Layer_Decomposition.tex` | 2 → bound |
| — | none; read in full (`:38-43`), numbers "not recomputed" (`:600-611`) | `papers/updates/ACS_Action_Identifiability.tex`, `papers/updates/ACS_Condensate_Carrier_Boundary.tex` | 2 each → bound |

Three of the "six target manuscripts" live under `papers/later_FF06_series/`, not
`papers/methodology/` as the candidate text says (`find papers -name …`). All six are
manifest-bound, so **every** application waits on the preservation record.

- The Definition 2 point is already asked for by the canonical paper's own amendment:
  `Spectral_Rigidity_Shuffle_Knife.tex:144` (24 Sept): "a null result must retain power and
  resolution limits"; the AISO doc `:236-238` observes the body's Definition 2 "does not
  encode it", and 3.7's part (ii) (`:334-338`) makes it operative (UNRESOLVED tier).
- `docs/publication/2026-09-24/amendments.json`: 0 mentions of `FF06e`, 0 of `2026-10`
  (`grep -c`); its entry [7] is the 24 Sept text for the Shuffle Knife. The file is **not**
  in the manifest (`grep -c` = 0), so an entry can be added without the gate.
- `code/hp_knife_suite/` last touched `226f519` (2026-07-17): the FF06e Python knife is
  unchanged; the repaired knife exists only as TypeScript in AISO (`frontend/src/shuffle-knife.ts`).
- Nothing in `acs-framework/docs/` links the AISO amendments document
  (`grep -rl ACS_PAPER_AMENDMENTS docs/` → 0 files); the amendments are reachable only from
  the other repository.

**Options.** (A) Apply all five as dated `\section*{Amendment: …, 2026-10-21}` appendices,
add five 2026-10-21 entries to `amendments.json`, and re-baseline the manifest in a dated
record (precedent: `docs/publication/2026-10-22-rerun.md` as a dated receipt beside the
frozen 24 Sept record). Cost: five manifest hashes change; the owner clears the integrity
gate once. (B) Apply none; the content lives in the two supporting papers under `docs/`
(which already carry the three-part Definition 2 repair as propositions). Cost: the six
manuscripts keep printing the figures the amendments measured differently. (C) Apply 3.7
only, as the one the canonical paper's own 24 Sept amendment asks for, plus an
`amendments.json` entry; defer the rest.

**Recommendation (agent's).** (C) first, and in the same edit link the AISO amendments
document (or a copy of it under `docs/`) from `docs/README.md`, so the proposals are
findable from the repository they target; (A) when the owner next re-baselines.

**If nothing is decided.** The 24 Sept amendment's sentence at `:144` stays unapplied by
the paper's own definition, and `When_a_Number_Lies` keeps a Condorcet list computed at an
electorate size it does not record.

---

### 2.6 DEP-076: a scope field on test-run-history rows (candidate 112)

**Question.** Should `TestRunRow` gain a `scope` (or `argv`) field, and how are the 189
rows already in the ledger to be read once it exists?

**Evidence** (all `AISO:`).

- `harness/dead_end_map_guide.md:503-507`, DEP-076 (the last of 80 DEPs). Fix line
  (`:505`): "The structural fix is NOT applied and is proposed rather than disposed, because
  it rewrites how 178 existing rows must be read: add a `scope` (or `argv`) field to the row,
  default it to the gate, and have the reporter refuse to compare rows across scopes [...]
  Until then, record only from `npm test`'s scope." Invariant (`:506`): "Scope carried in the
  invocation instead of the row is scope that is not recorded at all".
- `frontend/scripts/record-test-run.mts`: reads `process.argv[2]` (the vitest JSON path) and
  `--allow-red`; builds the row with
  `parseVitestJson(JSON.parse(...), new Date().toISOString(), 5, testedCommit(), testedTree())`;
  no scope anywhere.
- `frontend/src/test-run-history.ts`: `interface TestRunRow { at; files; tests; failed_tests;
  failed_files; duration_s; slowest; commit?; tree?; skipped? }`. The house rule for optional
  fields is stated twice in that interface: for `commit`, "the 43 rows written before this
  field existed have no commit, and two unstamped rows must NOT be read as the same code";
  for `skipped`, "absent must read as UNKNOWN rather than as zero — a row claiming 0 skipped
  when nobody counted would make every old green look like a full one". `codeStateOf(row)`
  returns `null` for an unstamped row and the flake verdict counts those apart.
- The gate is `vitest run tests` (`frontend/package.json:14`).
- Ledger, `data/test-run-history.jsonl`: 189 rows (`wc -l`), 0 containing `"scope"`
  (`grep -c`); fields present: `commit` on 27, `tree` on 131, `skipped` on 33; first row
  2026-08-07, last 2026-10-22T01:29; `files` ranges 408–495. One-sided inference: 0 of 189
  rows carry a `slowest`/`failed_files` path outside `tests/` (only the top-5 slowest are
  kept, so this can convict an off-scope row and cannot acquit one).
- Readers that compare rows (`grep -rl "readTestRuns\|flakeVerdict\|testRunGap"`):
  `frontend/src/test-run-history.ts`, `frontend/src/morning-report.ts`,
  `frontend/src/self-assessment.ts`, `frontend/scripts/morning-report.mts`,
  `frontend/scripts/record-test-run.mts`, and tests `test-run-history.test.ts`,
  `test-run-tree.test.ts`, `flake-reach.test.ts`, `first-of.test.ts`.

**The schema change.** `scope?: string` on `TestRunRow`, written by `record-test-run.mts`
as the vitest include root(s) the run was made with ("tests" for the gate; the DEP's `argv`
variant would store the literal invocation instead). Comparisons (`testRunGap`, the series
in `morning-report`, `flakeVerdict`) key on scope the way `flakeVerdict` keys on
`codeStateOf`, and decline across differing scopes.

**How the 189 rows would be read.** Two readings, and the DEP's own sentence picks the
one the ledger's conventions forbid:

- *Default absent to the gate* (DEP-076 `:505`). Reads all 189 rows as `tests` scope. The
  178 rows at DEP time are gate-scope by the DEP's own evidence (the one off-scope row was
  dropped before commit); the 11 recorded since are attested only by the procedural rule.
  This is exactly the pattern the `skipped` comment refuses ("a row claiming 0 skipped when
  nobody counted").
- *Absent is UNKNOWN* (the `commit`/`skipped` precedent). Rows without `scope` compare only
  among themselves; the series splits at the first scoped row and the gap line says so. The
  wall-growth narrative DEP-076 caught ("4084→5720") becomes "4084→5720 (unscoped)" until a
  scoped row exists.

**The two options the DEP names.** (1) Structural: the field plus reporter refusal across
scopes, with a test that a row written from a bare `vitest run` is never compared to a gate
row. (2) Procedural (status quo): "record only from `npm test`'s scope"; the scope lives in
the operator's habit and `package.json:14`, and the next bare run reproduces the trap.

**Recommendation (agent's).** (1), with absent = UNKNOWN, not defaulted; `scope` written as
the include root string; nine files to touch (listed above); one tested unit. It is a
row-schema change to a tracked ledger and so waits on the owner under AGENTS.md "Line the
test". Not applied here.

**If nothing is decided.** The ledger keeps recording without scope; the 189-row series
remains readable as gate-scope by stipulation only, and the DEP stays the last entry in the
guide with "proposed rather than disposed".

---

### What this part leaves out

- No manuscript, PDF, `amendments.json` or ledger was edited. The two paste-ready
  amendments for brief 2.1 are in the proposals file; the README/changelog rewrite for
  brief 2.4 is quoted in the brief and not applied.
- The RGE check is one-loop with one input set and no thresholds; its purpose is to test
  one sentence of Paper A, and its 10^15 GeV value (0.0025) differs from Paper B′'s table
  (0.0091) by input choice. Neither number is a result of this part.
- PR #17's CI failures were not diagnosed; only counted.
- The closure script follows relative imports only; a path alias or a `node_modules`
  package re-exporting repository code would be missed. None was seen in the 21 files.
