> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Bugfix log — Flag Condensate / Density Engine / Pα / capacitance / memo / DAW

**Date:** 2026-07-23  
**Scope:** `code/{palpha_overlap,capacitance_ribbon,acs_memo.py,benchmark_efficiency.py}`, `Aiso_build_artifacts/eigen_path_daw_viz/`, canvases `eigen-path-daw` / `density-engine`, ACS public mirror under `acs-framework-public/code/`.  
**RC1:** Claims limited to this harness run; no aiso/ substrate edits.

**ACS public commit:** `304ff8a` (`304ff8a95ce2c21521c54a3d9a85d4de9c967236`) on `main` (tensorrent/ACS-Framework).

## Procedure executed

1. Ran all Pα / ribbon / efficiency scripts (`ACS_MEMO=0` then memo parity).
2. `npm run typecheck` in the canvases workspace on the authoring machine (outside this repository).
3. Grepped TODO/FIXME/XXX / bare `except: pass` / absolute paths in scope.
4. Spot-checked `ACS_MEMO=0` vs `ACS_MEMO=1` (cold + warm) numerical fingerprints for refined, gamow library path via refined/ribbon.
5. Fixed confirmed bugs; re-ran affected paths.
6. Cross-checked baseline ↔ throat ↔ refined metric consistency on written JSON.

## Bugs found and fixed

| ID | Severity | Status | Description | Fix |
|----|----------|--------|-------------|-----|
| BF-001 | **Correctness** | **FIXED** | `export_daw_profiles.py` set `S_i = P_model_S / P_model`, which equals the single **global** \(S\) for every isotope. `log10_S_i` was already correct → JSON fields were inconsistent. | Compute `log10_S_i = log10_P_extracted − log10_P_model` and `S_i = 10**log10_S_i`. Verified 14/14 isotopes match refined `channel_A_on_eigenmode_base.S_i_table`. |
| BF-002 | **Build** | **FIXED** | `npm run typecheck` failed: `iso.r_fm` is a `readonly` tuple under `as const`, but `DAWLane` / `pathD` required mutable `number[]`. | Accept `readonly number[]` in `_canvas_template.tsx`; rebuild canvas. Typecheck **PASS**. |
| BF-003 | **Portability** | **FIXED** | DAW export wrote an absolute authoring-machine path into `source_json`. | Write the repo-relative path `docs/palpha_overlap_refined_results.json`. |
| BF-004 | **Schema soft** | **FIXED** | Channel A `global_S` only exposed `rms_residual_log10_P` while B/C use `rms_residual_S` (same quantity). | Emit both keys (same float) in `channel_A_from_model_rows`; synced to `acs-framework-public`. |

## Checks that PASS (no bug)

| Check | Result |
|-------|--------|
| `palpha_overlap.py` / `_throat` / `_refined` / `_extended` | exit 0; finite JSON |
| `ribbon_capacitance.py` | exit 0; finite JSON (BIE CODATA miss on scanned window is **documented scope**, not a harness failure) |
| `benchmark_efficiency.py` | `Benchmark status: pass` |
| `export_daw_profiles.py` / `build_canvas.py` | exit 0 after fixes |
| Result JSON NaN/Inf scan | all scoped `*results*.json` finite |
| **ACS_MEMO=0 vs 1** (cold + warm) | **identical** numerics within tolerance |
| Cross-script RMS/S for flat_gaussian & throat_ws | match across baseline / throat / refined |
| ACS public mirror (`acs_memo`, palpha, ribbon) | content **SYNC** after BF-004; `benchmark_efficiency.py` has intentional public path adaptation only |
| Grep TODO/FIXME/`except: pass` in scoped Python | none actionable |

## Remaining known issues (not bugs / out of scope)

1. **`palpha_overlap_gamow.py` has no `__main__`.** It is a library used by refined + DAW export. Running the file alone exits 0 with no stdout/JSON — by design, not a silent failure of Channel C (Channel C is written via refined).
2. **BIE vs CODATA on the scanned aspect window** remains large (as reported in ribbon JSON notes); analytic annulus/conformal CODATA roots sit at extreme \(a/R\) outside BIE-valid mesh — documented model limitation.
3. **GitNexus impact** on these symbols returns not-found / UNKNOWN (index lag for recent harness files); edits were local to new AISO/ACS harness paths.
4. **Canvas README absolute links** point into the authoring machine's local canvases workspace; they are environment-local documentation paths, not runtime code.

## Files changed

- `Aiso_build_artifacts/eigen_path_daw_viz/export_daw_profiles.py` — BF-001, BF-003
- `Aiso_build_artifacts/eigen_path_daw_viz/_canvas_template.tsx` — BF-002
- `Aiso_build_artifacts/eigen_path_daw_viz/eigen_path_daw_data.json` — regenerated
- `Aiso_build_artifacts/eigen_path_daw_viz/eigen_path_daw_data_compact.json` — regenerated
- `eigen-path-daw.canvas.tsx` (canvases workspace on the authoring machine, outside this repository) — regenerated
- `code/palpha_overlap/palpha_overlap_refined.py` — BF-004
- `acs-framework-public/code/palpha_overlap/palpha_overlap_refined.py` — mirror sync
- `docs/palpha_overlap_refined_results.json` — regenerated (alias key)

## Re-verification commands

From the repository root:

```bash
cd code
ACS_MEMO=0 python3 palpha_overlap/palpha_overlap_refined.py
ACS_MEMO=1 python3 capacitance_ribbon/ribbon_capacitance.py
python3 benchmark_efficiency.py
```

The remaining two steps of the original run — `build_canvas.py` under
`Aiso_build_artifacts/eigen_path_daw_viz/` and `npm run typecheck` in the canvases
workspace — operate on trees that are not part of this repository.
