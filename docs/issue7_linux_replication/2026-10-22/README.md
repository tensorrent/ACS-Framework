# Issue 7 full-pipeline replication on Linux (2026-10-22)

**Environment:** Linux x86_64 (kernel 6.18.44, glibc 2.39), Python 3.12.3, NumPy 2.2.6,
SciPy 1.15.3.
**Reference environment for the committed anchors:** macOS 15.3.2 arm64, Python 3.14.6,
NumPy 2.5.0 (per `../README.md`).
**Source commit:** `badb0b7` plus the `ACS_OUT_DIR` override to the issue7 entry points
(no change to any computation; the override only parameterises where artifacts land).

The 2026-08-07 replication in the parent directory ran the individual kill scripts but
not `verify_issue7_pipeline.py` to completion ("wall-clock bound"). This one runs the
wrapper end to end, into a scratch tree, so the committed anchors were never touched:

```sh
ACS_OUT_DIR=<scratch>/issue7-out python code/issue7/verify_issue7_pipeline.py
```

Files here, both new, neither overwriting anything:

- `issue7_verification_report_linux.json` — the report the pipeline wrote, verbatim
  (sha256 `424a7a1e46be7ba320314f446194721085e95bc6074d81dd3cd5b8555be07fa4`).
- `comparison_vs_macos_anchors.json` — a leaf-by-leaf diff of this run against the
  committed `docs/issue7_verification_report.json`, the four committed JSON artifacts and
  the six committed logs. Every number below is read from it.

## Wall clock

Total 983 s (16 min 23 s). Per stage, from file mtimes in the output tree:

| stage | seconds |
|---|---:|
| section9 + mechanism_4over3 | 12 |
| exhaustive | 611 |
| cross_model | 181 |
| long_range | 179 |
| section9_exact | 0.13 |

## Pipeline verdict

| field | macOS (committed) | Linux (this run) |
|---|---|---|
| `status` | `PASS_WITH_CAUTION` | `NEEDS_WORK` |
| all six runs `exit_code` | 0 | 0 |
| `stdout_lines` per run | 13 / 19 / 5 / 5 / 5 / 13 | identical |
| `consistency_errors` | 0 | 0 |
| `doc_errors` | 0 | 12 |

`NEEDS_WORK` comes from `doc_errors` alone: the two take-up documents quote the macOS
SHA-256 anchors, and six of the ten hashes differ here (below), so the wrapper reports
each of the six as missing from each of the two documents (6 × 2 = 12). Every
stdout-vs-artifact consistency check passed.

## SHA-256 anchors: four transfer, six do not

| anchor | matches macOS | why not |
|---|:-:|---|
| `docs/issue7_section9_exact_results.json` | yes | exact arithmetic |
| `docs/issue7_logs/section9_exact_stdout.txt` | yes | exact arithmetic |
| `docs/issue7_logs/section9_stdout.txt` | yes | float script; byte-identical here anyway |
| `docs/issue7_logs/mechanism_4over3_stdout.txt` | yes | float script; byte-identical here anyway |
| `docs/issue7_logs/exhaustive_stdout.txt` | no | **path echo only**, see below |
| `docs/issue7_logs/cross_model_stdout.txt` | no | **path echo only** |
| `docs/issue7_logs/long_range_stdout.txt` | no | **path echo only** |
| `docs/issue7_exhaustive_results.json` | no | float drift, see below |
| `docs/issue7_cross_model_results.json` | no | float drift |
| `docs/issue7_long_range_results.json` | no | float drift |

**The three log anchors are machine-bound, not platform-bound.** Each of those logs is
five lines, and the only line that differs is line 5, `artifact: <absolute path>`: on
macOS it is `/Users/coo-koba42/dev/rh_papers_may21/acs-framework/docs/…`, here it is the
scratch path. Lines 1–4 — the support rates, the combined counts, the RESULT lines — are
byte-identical. So these three anchors would fail on *any* checkout whose path differs
from the author's, including another Mac, regardless of floating point. (Under the
default output location the echoed path would be `<checkout>/docs/…`, which is still not
the committed string.) The two float logs that do match (`section9`, `mechanism_4over3`)
match because they do not echo a path.

**The three JSON anchors are float-bound.** Leaf-by-leaf:

| artifact | leaves | exact | differ ≤1e-12 | ≤1e-9 | ≤1e-6 | >1e-6 | max abs diff | non-float mismatches |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `issue7_exhaustive_results.json` | 133 | 109 | 23 | 0 | 0 | 1 | 0.0831 | 0 |
| `issue7_cross_model_results.json` | 116 | 80 | 29 | 4 | 0 | 3 | 0.0411 | 0 |
| `issue7_long_range_results.json` | 120 | 84 | 20 | 14 | 0 | 2 | 0.0465 | 0 |
| `issue7_section9_exact_results.json` | 63 | 63 | 0 | 0 | 0 | 0 | 0 | 0 (byte-identical) |

Zero non-float mismatches means every `supports_chain` boolean, every support count,
every `n_sites`/threshold label and every integer is the same on both platforms. The
decision-level reading of the 2026-08-07 note holds for the full pipeline.

## What the 2026-08-07 note did not say

That note reported float agreement "to ~1e-12 or better (IEEE last-bit drift only)".
This run does not support that figure as stated. 72 of the 96 differing float leaves are
within 1e-12 and 18 more within 1e-9, but **six leaves move by between 0.007 and 0.083**,
all of them correlation coefficients (`corr_gap_outside_leak`, `corr_gap_leak_max`,
`corr_gap_leak_mean`), listed with both values under `float_diff_over_1e-6` in the
comparison JSON:

| leaf | macOS | Linux | abs diff |
|---|---:|---:|---:|
| exhaustive `section9_exhaustive.cases[6].corr_gap_outside_leak` | 0.4531 | 0.3700 | 0.0831 |
| cross_model `tfim.cases[2].corr_gap_leak_mean` | 0.4941 | 0.5172 | 0.0231 |
| cross_model `tfim.cases[4].corr_gap_leak_max` | 0.7474 | 0.7885 | 0.0411 |
| cross_model `tfim.cases[4].corr_gap_leak_mean` | 0.8684 | 0.8756 | 0.0072 |
| long_range `sweeps.alpha_2.cases[2].corr_gap_leak_max` | −0.6253 | −0.6593 | 0.0340 |
| long_range `sweeps.alpha_2.cases[2].corr_gap_leak_mean` | −0.6459 | −0.6924 | 0.0465 |

None of the six flips a verdict: the `supports_chain` next to each is the same on both
platforms. But they are not last-bit drift, and a tolerance-based anchor for these
artifacts has to be wide enough to hold them, or exclude these diagnostic correlations
and anchor only the decision fields.

A plausible mechanism, **not verified here**: those correlations are taken over per-`h`
values of `outside_max` / leak extrema, which are selected by a threshold crossing of the
leak grid (`estimate_velocity_with_threshold`); a last-bit difference in the grid near
the threshold moves the crossing by one cell, which moves the selected extremum
discontinuously. The committed artifacts store only the per-case correlations, not the
per-`h` rows, so the artifacts alone cannot confirm this; a rerun that dumps `leak_grid`
on both platforms could. It is also unknown how much of the difference is the platform
and how much is NumPy 2.2.6 vs 2.5.0 — the two are confounded in this comparison.

## Absolute paths in the Linux report

The Linux report contains no `/Users` path (`"/Users"` occurs 0 times). It does contain
absolute paths in the `script` and `stdout_file` fields of each run, because the wrapper
writes `str(script)` and `str(out)`; here those are the scratch-tree paths. Making those
two fields repo-relative would make the report itself portable; that is a change to the
report format, not to any computation, and was left out of this change set to keep the
diff to the ask.

## Reproduce the comparison

The comparison was produced by a read-only script (not committed) that loads both reports
and all ten artifact pairs, walks the JSON leaf by leaf, buckets float differences, and
diffs the logs line by line; `comparison_vs_macos_anchors.json` is its unedited output.
`git status --short` in the worktree after the run listed only the edited instruments and
these new files: nothing under the tracked `docs/` was written by the pipeline.
