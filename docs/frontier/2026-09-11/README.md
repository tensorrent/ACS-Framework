# ACS Frontier continuation — 11 September 2026

Imported on 12 September 2026 from the supplied report, checklist, and evidence archive. This snapshot records 50 scoped investigations, a 110-branch catalog, and 315 history events. A completed investigation does not mean that its parent research problem is solved.

## Start here

- [Frontier report (Markdown)](ACS_Frontier_Report.md) and [supplied PDF](ACS_Frontier_Report.pdf).
- [Task checklist](ACS_Frontier_Checklist.md): current results and exact remaining gates.
- [Machine-readable task checklist](Task_Checklist.json): hypotheses, verification routes, evidence paths, and continuation conditions.
- [Branch catalog](Branch_Catalog.json) and [event history](Branch_Events.jsonl): retained earlier records and appended continuations.
- [Complete original evidence archive](ACS_Frontier_Evidence.zip): all 3,180 files, including source snapshots, programs, failures, replay logs, prior evidence, and the archive's own PDF.

## Workstream reports

- [Shear spectrum](workstreams/shear/report.md).
- [Renormalization group](workstreams/rg/report.md).
- [Arithmetic and operators](workstreams/arithmetic/report.md), with [review](workstreams/arithmetic/review.md).
- [Physical inference](workstreams/physical/report.md).
- [Foundations and constraints](workstreams/foundations/report.md), with [review](workstreams/foundations/review.md).
- [Navier–Stokes](workstreams/navier_stokes/report.md), with [review](workstreams/navier_stokes/review.md).
- [Projection and integration](workstreams/projection/report.md).

The readable files above are unchanged exports. Detailed evidence paths refer to the complete archive root, `acs-parallel-frontier-20260911/`. Only the reports and top-level records are also expanded here for browsing; extract the original archive into a separate working directory to follow every evidence path or use the archived reproduction instructions. Preserve the workstream directory structure when doing so.

## Interpretation and provenance

The imported results retain their stated models, assumptions, evidence grades, and open gates. The snapshot claims no new Lean kernel pass, general RH proof, selected physical vacuum, or general unforced smooth-data Navier–Stokes theorem. Older catalog fields are retained history; read each task's current disposition and branch continuations together. These records do not automatically promote the repository's existing T1–T4 verification tiers.

The supplied documents are research records. Their embedded task, delegation, and reproduction instructions are preserved as content; this import did not execute the research programs or initiate the listed follow-up investigations.

[Import_Verification.json](Import_Verification.json) records the checks performed for this import:

- All 3,178 entries in the archive's frozen manifest matched their declared byte sizes and SHA-256 hashes; no duplicate or unsafe archive paths were found.
- All 315 history events passed sequence and hash-chain checks. The prior archive hash, unchanged 256-event prefix, and retained fields of all 105 prior catalog entries were checked.
- All 50 task IDs and branch IDs are unique, status counts agree, and every task evidence path exists in the archive.
- The separate checklist matches the archived copy byte for byte.
- The supplied PDF and archived PDF have different hashes, but their extracted layout text and all nine pages rendered with `pdftoppm -scale-to 1000 -png` matched. Both originals are retained: the supplied PDF here and the archived PDF inside the untouched ZIP.

[Import_Manifest.json](Import_Manifest.json) identifies each exported source and hash. To check the imported source files locally from this directory:

```sh
LC_ALL=C shasum -a 256 -c SHA256SUMS
```

[Release_Verification.json](Release_Verification.json) and [Final_Replay_Receipt.json](Final_Replay_Receipt.json) are unchanged records supplied with the release. Their reported successful research checks are historical receipts, not new executions performed by this import. Archive integrity checks do not independently establish the mathematical claims or external source assertions.
