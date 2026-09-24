# Branch index and cleanup audit

[Repository home](../README.md) · [Documentation](README.md) · [Papers](../papers/README.md) · [Reproduction](REPRODUCTION.md)

**Audit snapshot: 24 September 2026.** `main` is the published reading and reproduction branch. The audit began at [b75cf44](https://github.com/tensorrent/ACS-Framework/commit/b75cf44fd1b18ceabce89758d2ae4b26f1606686), after the 35-paper publication merged.

The cleanup removed **nine remote branch refs whose exact tips were already ancestors of `main`**, reducing the audited remote set from **16 to 7**: `main` plus six unmerged research branches. A temporary branch used to deliver this navigation update is outside that snapshot. No unmerged work was discarded, and no open research PR was closed or merged.

[Machine-readable audit and deletion receipt](branch-audit/2026-09-24.json) records every original tip, commit counts, PR association, ancestry result, and the remote snapshot after cleanup. Counts below are relative to the audited `main` revision and will age as work continues. Use the [live branch list](https://github.com/tensorrent/ACS-Framework/branches) and [open PR list](https://github.com/tensorrent/ACS-Framework/pulls) for current status.

## Open research PRs

### Frontier continuation

`codex/acs-frontier-delta-2026-09-12` · [PR #16](https://github.com/tensorrent/ACS-Framework/pull/16) · [audited files](https://github.com/tensorrent/ACS-Framework/tree/6234df3811a635d139e3eeba30cfaa78b1015e2b)

27 commits are not in the audited main, covering later source constraints, joint features, local noise bounds, and mixed observations. Main already contains the five earlier reviewed frontier commits. Review this delta against the current publication before integration.

### Constraint-projection framework

`claude/constraint-projection-framework-010dsu` · [PR #14](https://github.com/tensorrent/ACS-Framework/pull/14) · [audited files](https://github.com/tensorrent/ACS-Framework/tree/eb52629acc6eb6b80ded6e01873acb728fa409c5)

46 commits are not in the audited main. The branch includes self-audits, falsified classification claims, prior-art review, and unfinished reports. Its findings have not been promoted into the published paper corpus by this cleanup.

## Other retained research

### Prime/FHE homomorphic primitive

`feature/prime-fhe-homomorphic-primitive` · [audited files](https://github.com/tensorrent/ACS-Framework/tree/8fea47f4153dcb13287c90d8f2dbb809bed6d9cc)

This is a separate Git history with no common ancestor with main, containing 17 commits. It has no open ACS PR at this snapshot. Its cryptographic manuscript and benchmarks need a deliberate import/review decision; it cannot be treated as an ordinary stale ACS feature branch.

### Post-merge paper analysis

`claude/papers-repo-analysis-kce6bn` · [audited files](https://github.com/tensorrent/ACS-Framework/tree/e4bc97195e2d697dce2aade749d62ea6aff7bc4b)

PR #13 merged the earlier framework knowledge module, but the branch subsequently gained one unmerged commit about the Exodus electrostatic-anomaly claim, including a new analysis and elimination-ledger additions. The merged PR does not justify deleting this branch.

### Scaled-invariance reconciliation

`claude/infinity-zero-scaled-invariance-vzm54b` · [audited files](https://github.com/tensorrent/ACS-Framework/tree/ef82e58eb021d7837889272c8e377ae723bb60b4)

The single branch-only commit belongs to closed PR #4. Its scaled-invariance test is already byte-identical on main; the paper and navigation files differ from the now-amended main versions. Retain the branch until its surviving differences are explicitly reconciled.

### Exposure/redaction proposal

`claude/public-ip-exposure-audit-6zxyf4` · [audited files](https://github.com/tensorrent/ACS-Framework/tree/93c94595ad94a98aba94f9caa77d81e25b361149)

One unmerged commit proposes redacting local paths and cross-repository details in six historical documents/logs. It is retained for review against current provenance and preservation requirements; this cleanup does not apply the redactions.

## Retired merged branches

Each linked commit remains reachable through published `main`. Only the branch name was removed; the work and Git history remain recoverable.

- `claude/electron-banach-tarski-lduyf6` — [preserved tip f46ec47](https://github.com/tensorrent/ACS-Framework/commit/f46ec478ad1f5dbdf4b2d5dedd46d3b027563968).
- `claude/form-function-perspective-trsjjg` — [preserved tip e6a7625](https://github.com/tensorrent/ACS-Framework/commit/e6a7625ba432f6b849b1e05d5707c004ae79618f).
- `claude/neiman-tensor-equation-nub8q8` — [preserved tip b31d1d0](https://github.com/tensorrent/ACS-Framework/commit/b31d1d06481ef487ecadb512b8b9ac80ecb12211).
- `claude/repo-cleanup-public-u5wyz8` — [preserved tip 66b201e](https://github.com/tensorrent/ACS-Framework/commit/66b201ed785283cbe8c9e256b50346c9fe456734).
- `claude/torsion-topological-condensation-h6v40k` — [preserved tip 905ed49](https://github.com/tensorrent/ACS-Framework/commit/905ed4939514c3b69a8f114022bb76ed40a21f79).
- `claude/tr8g-pythagorean-theorem-4332wx` — [preserved tip 558874e](https://github.com/tensorrent/ACS-Framework/commit/558874e8d0ea345b48a937c88aabc536a35193a5).
- `codex/acs-publication-update-2026-09-24` — [preserved tip a51abfe](https://github.com/tensorrent/ACS-Framework/commit/a51abfea189e08104b52f71ecdc0c63732601815).
- `codex/import-acs-frontier-2026-09-11` — [preserved tip 89bbb27](https://github.com/tensorrent/ACS-Framework/commit/89bbb278a5d72791b4104925a83f10758cd22535).
- `docs/glossary` — [preserved tip 8fdfcfe](https://github.com/tensorrent/ACS-Framework/commit/8fdfcfe504fb33e6d97adbe670606eb0095e1930).

The deletion used an atomic push, exact-tip leases, fresh ancestry checks, branch-protection checks, and an open-PR check. A changed tip or newly active PR would have stopped the operation.

## Restore a retired branch if needed

Choose its exact name and full SHA from the JSON audit. From a clone with main's history:

```sh
git fetch origin main
git branch restored-research <recorded-full-sha>
```

This creates a local branch at the preserved tip. Publish it only when that work needs an active remote branch again. A shallow clone may need `git fetch --unshallow origin` first.

## Local worktrees and indexing

The original ACS and threshold-audit worktrees contained uncommitted work and were left untouched. The completed publication worktree was retained as well. Remote branch cleanup does not remove local branches or working files.

The ACS GitNexus index was built locally in index-only mode, without changing standing instruction files. To index your own checkout with the installed GitNexus CLI:

```sh
gitnexus analyze --index-only --name ACS-Framework
```

The local `.gitnexus/` database is ignored by Git. Large data files skipped by the code index remain present in the repository and covered by their publication receipts; this code index is not a substitute for the evidence index.
