# Efficiency Benchmark Report — Flag Condensate / Pα / Density Engine Harness

**Scope (RC1):** As-implemented **harness performance** on the stated test machine — wall time, throughput, scaling, and **disk/memory memo** speedups. This report does **not** claim physical engine efficiency, alpha-decay accuracy, or uniqueness of the density-engine metaphor.

| Field | Value |
|-------|-------|
| **Date (UTC)** | 2026-07-23 |
| **Platform** | darwin · Python 3.14.6 |
| **Timing tool** | `/usr/bin/time -l` (macOS) + `perf_counter` microbench |
| **Runner** | `rh_papers_may21/acs-framework/code/benchmark_efficiency.py` |
| **Raw JSON** | `rh_papers_may21/acs-framework/docs/efficiency_benchmark_results.json` |
| **Status** | **pass** |
| **Memo root** | `/Users/coo-koba42/dev/rh_papers_may21/acs-framework/.cache` |

---

## Executive summary

Disk/memory memo keyed by BIE `(R, a, n_u, n_v, model)` and eigen/Gamow `(isotope, BC, params)` is enabled (`ACS_MEMO=1`, default). **Ribbon script warm speedup vs before:** **81.01×** (before 12.21 s → warm 0.15071612503379583 s). **Gamow 14-isotope cold→warm:** **14.38×**. **BIE single-point (48×6) cold→warm:** **7284.41×**.

Bottleneck script (post-memo mean): `palpha_overlap_refined`. Bottleneck channel (compute, first-fill): `gamow_outgoing`.

---

## Cache before / after

| Path | Before (s) | After cold (s) | After warm (s) | Speedup cold/warm | vs before (warm) |
|------|----------:|---------------:|---------------:|------------------:|-----------------:|
| Gamow 14 isotopes | (rel flat 23.502×) | 0.1517 | 0.0105 | **14.38×** | — |
| Eigen Dirichlet 14 | — | 0.0909 | 0.0100 | **9.07×** | — |
| BIE single 48×6 | — | 1.1491 | 0.0002 | **7284.41×** | — |
| `ribbon_capacitance.py` | 12.21 | 11.762 | 0.151 | **78.04×** | **81.01×** |

Memo blobs live under `.cache/bie_capacitance/` and `.cache/palpha_eigen/` (gitignored). Disable with `ACS_MEMO=0`.

---

## End-to-end script runs (memo enabled)

| Script | Wall (s) | vs baseline | Peak (MiB) |
|--------|--------:|------------:|-----------:|
| `palpha_overlap_baseline` | 0.243 | 1.00× | 55.25 |
| `palpha_overlap_throat` | 0.273 | 1.12× | 56.77 |
| `palpha_overlap_refined` | 0.350 | 1.44× | 60.03 |
| `palpha_overlap_extended` | 0.273 | 1.12× | 57.2 |
| `ribbon_capacitance` | 0.150 | 0.62× | 39.19 |
| `export_daw_profiles` | 0.270 | 1.11× | 57.1 |
| `build_canvas` | 0.287 | 1.18× | 10.11 |

### Per-channel compute (14 isotopes; may include memo hits on repeats)

| Channel | Per isotope (ms) | vs flat |
|---------|-----------------:|--------:|
| Flat Gaussian | 0.43 | 1.0× |
| Eigenmode Dirichlet | 5.71 | 13.432× |
| Gamow outgoing | 9.71 | 22.854× |

---

## Recommendations

1. Keep `ACS_MEMO=1` for interactive / repeated BIE and Gamow work.
2. Clear `.cache/` when changing mesh parameters or isotope tables.
3. First-fill (cold) cost remains ~O(N^1.37) in BIE panels; warm reads are JSON/NPZ loads.

## Caveats

- Timings are machine-specific; reproduce via `python3 benchmark_efficiency.py`.
- Warm speedups assume identical cache keys; float formatting uses 12 significant digits.
- No claim about numerical accuracy vs experimental alpha-decay data.

## Artifacts

| Path | Description |
|------|-------------|
| `rh_papers_may21/acs-framework/code/acs_memo.py` | Disk + memory memo |
| `rh_papers_may21/acs-framework/code/benchmark_efficiency.py` | Unified runner |
| `rh_papers_may21/acs-framework/docs/efficiency_benchmark_results.json` | JSON |
| `Aiso_build_artifacts/density_engine_many_worlds/EFFICIENCY_BENCHMARK_REPORT.md` | This report |

**Re-run:** `python3 rh_papers_may21/acs-framework/code/benchmark_efficiency.py`
