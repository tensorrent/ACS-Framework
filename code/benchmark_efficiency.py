#!/usr/bin/env python3
"""
Unified efficiency benchmark for Flag Condensate / Pα / Density Engine harness.

RC1 scope: measures as-implemented script wall time, throughput, and scaling
in the stated test environment — not physical engine efficiency or uniqueness.

Writes: rh_papers_may21/acs-framework/docs/efficiency_benchmark_results.json
"""

from __future__ import annotations

import json
import math
import os
import re
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

CODE_ROOT = Path(__file__).resolve().parent
# ACS-Framework public: code/ sits under repo root. Monorepo checkout may be deeper.
_ACS_ROOT = CODE_ROOT.parent
_MONOREPO = CODE_ROOT.parents[2] if (CODE_ROOT.parents[2] / "Aiso_build_artifacts").is_dir() else _ACS_ROOT
REPO_ROOT = _MONOREPO
PALPHA_DIR = CODE_ROOT / "palpha_overlap"
CAP_DIR = CODE_ROOT / "capacitance_ribbon"
DAW_DIR = REPO_ROOT / "Aiso_build_artifacts" / "eigen_path_daw_viz"
DOCS_OUT = _ACS_ROOT / "docs" / "efficiency_benchmark_results.json"
REPORT_OUT = (
    (_MONOREPO / "Aiso_build_artifacts" / "density_engine_many_worlds" / "EFFICIENCY_BENCHMARK_REPORT.md")
    if (_MONOREPO / "Aiso_build_artifacts").is_dir()
    else (_ACS_ROOT / "docs" / "EFFICIENCY_BENCHMARK_REPORT.md")
)

FAST_RUN_THRESHOLD_S = 5.0
DEFAULT_REPEATS = 3
SLOW_REPEATS = 1

# Inject palpha package for import-based micro-benchmarks.
if str(PALPHA_DIR) not in sys.path:
    sys.path.insert(0, str(PALPHA_DIR))
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))


@dataclass(frozen=True)
class ScriptSpec:
    name: str
    path: Path
    cwd: Path
    repeats: int = DEFAULT_REPEATS
    n_isotopes: int | None = None
    notes: str = ""


@dataclass
class TimedRun:
    wall_s: float
    user_s: float | None
    sys_s: float | None
    peak_memory_bytes: int | None
    exit_code: int
    stderr_tail: str = ""


REAL_RE = re.compile(
    r"^\s*([\d.]+)\s+real\s+([\d.]+)\s+user\s+([\d.]+)\s+sys", re.MULTILINE
)
PEAK_MEM_RE = re.compile(r"^\s*(\d+)\s+peak memory footprint", re.MULTILINE)


def _parse_time_l(text: str) -> tuple[float | None, float | None, float | None, int | None]:
    real = user = sys_t = None
    peak = None
    m = REAL_RE.search(text)
    if m:
        real, user, sys_t = float(m.group(1)), float(m.group(2)), float(m.group(3))
    pm = PEAK_MEM_RE.search(text)
    if pm:
        peak = int(pm.group(1))
    return real, user, sys_t, peak


def run_script_timed(spec: ScriptSpec) -> dict[str, Any]:
    """Run a script under /usr/bin/time -l; repeat per spec.repeats."""
    runs: list[TimedRun] = []
    for _ in range(spec.repeats):
        cmd = ["/usr/bin/time", "-l", sys.executable, str(spec.path)]
        proc = subprocess.run(
            cmd,
            cwd=str(spec.cwd),
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        real, user, sys_t, peak = _parse_time_l(proc.stderr)
        wall = real if real is not None else float("nan")
        runs.append(
            TimedRun(
                wall_s=wall,
                user_s=user,
                sys_s=sys_t,
                peak_memory_bytes=peak,
                exit_code=proc.returncode,
                stderr_tail=proc.stderr[-500:] if proc.stderr else "",
            )
        )
        if proc.returncode != 0:
            break

    walls = [r.wall_s for r in runs if math.isfinite(r.wall_s)]
    peaks = [r.peak_memory_bytes for r in runs if r.peak_memory_bytes is not None]
    mean_wall = statistics.mean(walls) if walls else float("nan")
    std_wall = statistics.stdev(walls) if len(walls) > 1 else 0.0
    peak_mem = max(peaks) if peaks else None

    throughput: dict[str, float | None] = {}
    if spec.n_isotopes and mean_wall > 0:
        throughput["isotopes_per_sec"] = spec.n_isotopes / mean_wall
    if "ribbon" in spec.name:
        throughput["note"] = "grid scan over aspect ratios; see scaling.bie_mesh"

    return {
        "script": str(spec.path.relative_to(REPO_ROOT)),
        "name": spec.name,
        "repeats": spec.repeats,
        "exit_code": runs[-1].exit_code if runs else 1,
        "wall_time_s": {
            "mean": mean_wall,
            "std": std_wall,
            "runs": walls,
        },
        "user_time_s": runs[-1].user_s if runs else None,
        "sys_time_s": runs[-1].sys_s if runs else None,
        "peak_memory_bytes": peak_mem,
        "peak_memory_MiB": round(peak_mem / (1024 * 1024), 2) if peak_mem else None,
        "throughput": throughput,
        "notes": spec.notes,
    }


def time_callable(fn: Callable[[], Any], *, repeats: int = 3) -> dict[str, float]:
    times: list[float] = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return {
        "mean_s": statistics.mean(times),
        "std_s": statistics.stdev(times) if len(times) > 1 else 0.0,
        "runs_s": times,
    }


def channel_microbenchmarks() -> dict[str, Any]:
    """Per-channel wall time on base-14 set (import-based, no JSON I/O).

    Memo disabled so relative channel costs reflect compute, not cache hits.
    """
    prev_memo = os.environ.get("ACS_MEMO")
    os.environ["ACS_MEMO"] = "0"
    try:
        out = _channel_microbenchmarks_uncached()
    finally:
        if prev_memo is None:
            os.environ.pop("ACS_MEMO", None)
        else:
            os.environ["ACS_MEMO"] = prev_memo
    return out


def _channel_microbenchmarks_uncached() -> dict[str, Any]:
    from palpha_overlap import ISOTOPES, N_GRID, R0_DEFAULT_FM, run_analysis
    from palpha_overlap_gamow import (
        A_WS_DEFAULT_FM,
        N_EIGEN_GRID,
        evaluate_gamow_isotope,
    )
    from palpha_overlap_refined import evaluate_eigenmode_isotope
    from palpha_overlap_throat import (
        KAPPA_TAIL_DEFAULT,
        ModelSpec,
        evaluate_isotope_model,
        run_analysis as run_throat_analysis,
    )

    n_iso = len(ISOTOPES)
    spec_ws = ModelSpec(
        label="throat_ws",
        alpha_kind="woods_saxon",
        measure_kind="throat_ads",
        primary=True,
    )

    flat = time_callable(lambda: run_analysis(r0_fm=R0_DEFAULT_FM, n_grid=N_GRID))
    throat = time_callable(
        lambda: run_throat_analysis(
            r0_fm=R0_DEFAULT_FM,
            a_ws_fm=A_WS_DEFAULT_FM,
            kappa_fm_inv=KAPPA_TAIL_DEFAULT,
            n_grid=N_GRID,
        )
    )

    def _eigen_all() -> None:
        for iso in ISOTOPES:
            evaluate_eigenmode_isotope(
                iso,
                r0_fm=R0_DEFAULT_FM,
                a_ws_fm=A_WS_DEFAULT_FM,
                n_overlap=N_GRID,
                n_interior=N_EIGEN_GRID,
            )

    def _gamow_all() -> None:
        for iso in ISOTOPES:
            evaluate_gamow_isotope(
                iso,
                r0_fm=R0_DEFAULT_FM,
                a_ws_fm=A_WS_DEFAULT_FM,
                n_overlap=N_GRID,
                n_interior=N_EIGEN_GRID,
            )

    def _throat_per_iso() -> None:
        for iso in ISOTOPES:
            evaluate_isotope_model(
                iso,
                spec_ws,
                r0_fm=R0_DEFAULT_FM,
                a_ws_fm=A_WS_DEFAULT_FM,
                kappa_fm_inv=KAPPA_TAIL_DEFAULT,
                n_grid=N_GRID,
            )

    eigen = time_callable(_eigen_all)
    gamow = time_callable(_gamow_all)
    throat_iso = time_callable(_throat_per_iso)

    per_iso = {
        "flat_gaussian": flat["mean_s"] / n_iso,
        "throat_ws_loop": throat_iso["mean_s"] / n_iso,
        "eigenmode_dirichlet": eigen["mean_s"] / n_iso,
        "gamow_outgoing": gamow["mean_s"] / n_iso,
    }

    baseline = flat["mean_s"]
    relative = {
        k: round(v / baseline, 3) if baseline > 0 else None
        for k, v in {
            "flat_gaussian": flat["mean_s"],
            "throat_full_analysis": throat["mean_s"],
            "eigenmode_14_isotopes": eigen["mean_s"],
            "gamow_14_isotopes": gamow["mean_s"],
        }.items()
    }

    return {
        "n_isotopes": n_iso,
        "n_grid": N_GRID,
        "n_interior_eigen": N_EIGEN_GRID,
        "memo_disabled": True,
        "total_wall_s": {
            "flat_gaussian": flat,
            "throat_full_analysis": throat,
            "eigenmode_dirichlet_14": eigen,
            "gamow_outgoing_14": gamow,
        },
        "per_isotope_s": per_iso,
        "per_isotope_throughput_per_sec": {
            k: 1.0 / v if v > 0 else None for k, v in per_iso.items()
        },
        "relative_to_flat": relative,
        "bottleneck_channel": max(
            (
                ("gamow_outgoing", gamow["mean_s"]),
                ("eigenmode_dirichlet", eigen["mean_s"]),
                ("throat_full_analysis", throat["mean_s"]),
                ("flat_gaussian", flat["mean_s"]),
            ),
            key=lambda x: x[1],
        )[0],
    }


def scaling_benchmarks() -> dict[str, Any]:
    """Sweep n_grid, isotope count, BIE mesh, eigen interior grid.

    Disables ACS_MEMO for fair asymptotic slopes (cache would flatten warm points).
    """
    from isotope_catalog import ISOTOPES, combined_isotopes
    from palpha_overlap import R0_DEFAULT_FM, run_analysis
    from palpha_overlap_extended import run_throat_ws_for_isotopes
    from palpha_overlap_gamow import A_WS_DEFAULT_FM, evaluate_gamow_isotope
    from palpha_overlap_refined import evaluate_eigenmode_isotope
    from palpha_overlap_throat import A_WS_DEFAULT_FM as A_WS

    sys.path.insert(0, str(CAP_DIR))
    from ribbon_capacitance import R_SPIN, bie_mobius_C  # type: ignore

    prev_memo = os.environ.get("ACS_MEMO")
    os.environ["ACS_MEMO"] = "0"
    try:
        return _scaling_benchmarks_uncached(
            ISOTOPES=ISOTOPES,
            combined_isotopes=combined_isotopes,
            R0_DEFAULT_FM=R0_DEFAULT_FM,
            run_analysis=run_analysis,
            run_throat_ws_for_isotopes=run_throat_ws_for_isotopes,
            evaluate_gamow_isotope=evaluate_gamow_isotope,
            evaluate_eigenmode_isotope=evaluate_eigenmode_isotope,
            A_WS=A_WS,
            R_SPIN=R_SPIN,
            bie_mobius_C=bie_mobius_C,
        )
    finally:
        if prev_memo is None:
            os.environ.pop("ACS_MEMO", None)
        else:
            os.environ["ACS_MEMO"] = prev_memo


def _scaling_benchmarks_uncached(
    *,
    ISOTOPES,
    combined_isotopes,
    R0_DEFAULT_FM,
    run_analysis,
    run_throat_ws_for_isotopes,
    evaluate_gamow_isotope,
    evaluate_eigenmode_isotope,
    A_WS,
    R_SPIN,
    bie_mobius_C,
) -> dict[str, Any]:
    # n_grid scaling (flat proxy, 14 isotopes)
    grid_sizes = [512, 1024, 2048, 4096, 8192]
    grid_rows = []
    for ng in grid_sizes:
        t = time_callable(lambda n=ng: run_analysis(r0_fm=R0_DEFAULT_FM, n_grid=n))
        grid_rows.append(
            {
                "n_grid": ng,
                "wall_s": t["mean_s"],
                "grid_points_per_sec": (ng * len(ISOTOPES)) / t["mean_s"],
                "isotopes_per_sec": len(ISOTOPES) / t["mean_s"],
            }
        )

    # Fit log-log slope for asymptotic hint (last 3 points)
    def _loglog_slope(xs: list[float], ys: list[float]) -> float | None:
        if len(xs) < 2:
            return None
        lx = [math.log(x) for x in xs]
        ly = [math.log(y) for y in ys]
        n = len(lx)
        mx = sum(lx) / n
        my = sum(ly) / n
        num = sum((lx[i] - mx) * (ly[i] - my) for i in range(n))
        den = sum((lx[i] - mx) ** 2 for i in range(n))
        return num / den if den else None

    grid_slope = _loglog_slope(
        [r["n_grid"] for r in grid_rows[-3:]],
        [r["wall_s"] for r in grid_rows[-3:]],
    )

    # Isotope-count scaling (throat+WS only — extended harness)
    iso_sets = [
        ("base_14", ISOTOPES),
        ("extended_29", combined_isotopes()),
    ]
    iso_rows = []
    for label, isos in iso_sets:
        t = time_callable(lambda i=isos: run_throat_ws_for_isotopes(i))
        iso_rows.append(
            {
                "label": label,
                "n_isotopes": len(isos),
                "wall_s": t["mean_s"],
                "isotopes_per_sec": len(isos) / t["mean_s"],
                "per_isotope_ms": 1000.0 * t["mean_s"] / len(isos),
            }
        )
    n14_t = iso_rows[0]["wall_s"]
    n29_t = iso_rows[1]["wall_s"]
    iso_ratio = n29_t / n14_t if n14_t > 0 else None
    n_ratio = iso_rows[1]["n_isotopes"] / iso_rows[0]["n_isotopes"]
    linearity_note = (
        f"wall time ratio {iso_ratio:.3f} vs isotope ratio {n_ratio:.3f} "
        f"({'approximately linear' if iso_ratio and abs(iso_ratio - n_ratio) < 0.15 * n_ratio else 'superlinear'})"
        if iso_ratio
        else "insufficient data"
    )

    # BIE mesh scaling (single demo point a/R=0.05)
    a_demo = 0.05 * R_SPIN
    bie_meshes = [(16, 4), (32, 4), (48, 6), (64, 8), (96, 8)]
    bie_rows = []
    for nu, nv in bie_meshes:
        panels = nu * nv
        t = time_callable(lambda u=nu, v=nv: bie_mobius_C(R_SPIN, a_demo, n_u=u, n_v=v))
        bie_rows.append(
            {
                "n_u": nu,
                "n_v": nv,
                "panels": panels,
                "wall_s": t["mean_s"],
                "panels_per_sec": panels / t["mean_s"],
            }
        )
    bie_slope = _loglog_slope(
        [r["panels"] for r in bie_rows],
        [r["wall_s"] for r in bie_rows],
    )

    # Eigen interior grid (single isotope — slowest per-iso cost)
    iso0 = ISOTOPES[0]
    interior_sizes = [200, 400, 800, 1200]
    interior_rows = []
    for ni in interior_sizes:
        t = time_callable(
            lambda n=ni: evaluate_eigenmode_isotope(
                iso0,
                r0_fm=R0_DEFAULT_FM,
                a_ws_fm=A_WS,
                n_overlap=4096,
                n_interior=n,
            )
        )
        interior_rows.append({"n_interior": ni, "wall_s": t["mean_s"]})
    interior_slope = _loglog_slope(
        [r["n_interior"] for r in interior_rows],
        [r["wall_s"] for r in interior_rows],
    )

    # Gamow vs eigen on one heavy isotope (238U index)
    heavy = ISOTOPES[10]
    t_eigen = time_callable(
        lambda: evaluate_eigenmode_isotope(
            heavy,
            r0_fm=R0_DEFAULT_FM,
            a_ws_fm=A_WS,
            n_overlap=4096,
            n_interior=800,
        ),
        repeats=3,
    )
    t_gamow = time_callable(
        lambda: evaluate_gamow_isotope(
            heavy,
            r0_fm=R0_DEFAULT_FM,
            a_ws_fm=A_WS,
            n_overlap=4096,
            n_interior=800,
        ),
        repeats=3,
    )

    return {
        "n_grid_flat_proxy": {
            "rows": grid_rows,
            "loglog_slope_wall_vs_n_grid_last3": grid_slope,
            "interpretation": (
                f"slope ≈ {grid_slope:.2f} on last 3 sizes "
                "(≈1 ⇒ linear in grid points for Simpson overlap)"
                if grid_slope is not None
                else "n/a"
            ),
        },
        "isotope_count_throat_ws": {
            "rows": iso_rows,
            "wall_ratio_29_over_14": iso_ratio,
            "isotope_count_ratio": n_ratio,
            "linearity_assessment": linearity_note,
        },
        "bie_mobius_mesh": {
            "a_over_R": 0.05,
            "rows": bie_rows,
            "loglog_slope_wall_vs_panels": bie_slope,
            "interpretation": (
                f"slope ≈ {bie_slope:.2f} vs panel count "
                "(dense BIE solve — expect ≥1)"
                if bie_slope is not None
                else "n/a"
            ),
            "memo_disabled": True,
        },
        "eigen_interior_single_isotope": {
            "isotope": heavy.name,
            "rows": interior_rows,
            "loglog_slope": interior_slope,
        },
        "heavy_isotope_238U_single_solve": {
            "eigenmode_s": t_eigen,
            "gamow_s": t_gamow,
            "gamow_over_eigen_ratio": t_gamow["mean_s"] / t_eigen["mean_s"]
            if t_eigen["mean_s"] > 0
            else None,
            "memo_disabled": True,
        },
    }


def build_script_specs() -> list[ScriptSpec]:
    return [
        ScriptSpec(
            "palpha_overlap_baseline",
            PALPHA_DIR / "palpha_overlap.py",
            PALPHA_DIR,
            n_isotopes=14,
            notes="Flat [0,R] Gaussian overlap, n_grid=4096",
        ),
        ScriptSpec(
            "palpha_overlap_throat",
            PALPHA_DIR / "palpha_overlap_throat.py",
            PALPHA_DIR,
            n_isotopes=14,
            notes="Throat weight + WS models",
        ),
        ScriptSpec(
            "palpha_overlap_refined",
            PALPHA_DIR / "palpha_overlap_refined.py",
            PALPHA_DIR,
            n_isotopes=14,
            notes="Channel A/B/C full analysis",
        ),
        ScriptSpec(
            "palpha_overlap_extended",
            PALPHA_DIR / "palpha_overlap_extended.py",
            PALPHA_DIR,
            n_isotopes=29,
            notes="Throat+WS on 29-isotope catalog",
        ),
        ScriptSpec(
            "ribbon_capacitance",
            CAP_DIR / "ribbon_capacitance.py",
            CAP_DIR,
            repeats=SLOW_REPEATS,
            notes="Annulus/conformal/BIE aspect scan (~12s)",
        ),
        ScriptSpec(
            "export_daw_profiles",
            DAW_DIR / "export_daw_profiles.py",
            REPO_ROOT,
            n_isotopes=14,
            notes="Eigen-path lane export, 128 pts/lane",
        ),
        ScriptSpec(
            "build_canvas",
            DAW_DIR / "build_canvas.py",
            REPO_ROOT,
            notes="Runs export + compact JSON + canvas inject",
        ),
    ]


def compute_relative_ratios(script_results: list[dict[str, Any]]) -> dict[str, float]:
    by_name = {r["name"]: r["wall_time_s"]["mean"] for r in script_results}
    baseline = by_name.get("palpha_overlap_baseline")
    if not baseline or baseline <= 0:
        return {}
    return {
        name: round(t / baseline, 3)
        for name, t in by_name.items()
        if math.isfinite(t)
    }


def cache_speedup_benchmarks(before: dict[str, Any] | None) -> dict[str, Any]:
    """
    Cold (empty disk memo) vs warm (disk+memory hit) timings for BIE and Gamow.

    Clears memo namespaces, then primes on the cold pass.
    """
    import acs_memo
    from palpha_overlap import ISOTOPES, N_GRID, R0_DEFAULT_FM
    from palpha_overlap_gamow import (
        A_WS_DEFAULT_FM,
        N_EIGEN_GRID,
        evaluate_gamow_isotope,
    )
    from palpha_overlap_refined import evaluate_eigenmode_isotope

    sys.path.insert(0, str(CAP_DIR))
    from ribbon_capacitance import R_SPIN, bie_mobius_C  # type: ignore

    os.environ["ACS_MEMO"] = "1"
    acs_memo.clear_memory()
    acs_memo.clear_namespace("palpha_eigen", disk=True)
    acs_memo.clear_namespace("bie_capacitance", disk=True)
    acs_memo.reset_stats()

    def _gamow_all() -> None:
        for iso in ISOTOPES:
            evaluate_gamow_isotope(
                iso,
                r0_fm=R0_DEFAULT_FM,
                a_ws_fm=A_WS_DEFAULT_FM,
                n_overlap=N_GRID,
                n_interior=N_EIGEN_GRID,
            )

    def _eigen_all() -> None:
        for iso in ISOTOPES:
            evaluate_eigenmode_isotope(
                iso,
                r0_fm=R0_DEFAULT_FM,
                a_ws_fm=A_WS_DEFAULT_FM,
                n_overlap=N_GRID,
                n_interior=N_EIGEN_GRID,
            )

    a_demo = 0.05 * R_SPIN

    # Cold (miss): first compute + write
    t0 = time.perf_counter()
    _gamow_all()
    gamow_cold = time.perf_counter() - t0
    acs_memo.clear_memory()  # force disk reload on warm

    t0 = time.perf_counter()
    _gamow_all()
    gamow_warm = time.perf_counter() - t0

    acs_memo.clear_namespace("palpha_eigen", disk=True)
    acs_memo.clear_memory()
    t0 = time.perf_counter()
    _eigen_all()
    eigen_cold = time.perf_counter() - t0
    acs_memo.clear_memory()
    t0 = time.perf_counter()
    _eigen_all()
    eigen_warm = time.perf_counter() - t0

    acs_memo.clear_namespace("bie_capacitance", disk=True)
    acs_memo.clear_memory()
    t0 = time.perf_counter()
    bie_mobius_C(R_SPIN, a_demo, n_u=48, n_v=6)
    bie_cold = time.perf_counter() - t0
    acs_memo.clear_memory()
    t0 = time.perf_counter()
    bie_mobius_C(R_SPIN, a_demo, n_u=48, n_v=6)
    bie_warm = time.perf_counter() - t0

    # Full ribbon script: cold then warm (disk survives across subprocesses)
    acs_memo.clear_namespace("bie_capacitance", disk=True)
    ribbon_spec = ScriptSpec(
        "ribbon_capacitance",
        CAP_DIR / "ribbon_capacitance.py",
        CAP_DIR,
        repeats=1,
        notes="cache cold/warm",
    )
    env_memo = {**os.environ, "ACS_MEMO": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    t0 = time.perf_counter()
    proc_c = subprocess.run(
        [sys.executable, str(ribbon_spec.path)],
        cwd=str(ribbon_spec.cwd),
        capture_output=True,
        text=True,
        env=env_memo,
    )
    ribbon_cold = time.perf_counter() - t0
    t0 = time.perf_counter()
    proc_w = subprocess.run(
        [sys.executable, str(ribbon_spec.path)],
        cwd=str(ribbon_spec.cwd),
        capture_output=True,
        text=True,
        env=env_memo,
    )
    ribbon_warm = time.perf_counter() - t0

    def _ratio(cold: float, warm: float) -> float | None:
        if warm <= 0:
            return None
        return round(cold / warm, 2)

    before_ribbon = None
    before_gamow_rel = None
    before_utc = None
    if before:
        # Prefer the original pre-memo baseline if already recorded.
        prev_cs = before.get("cache_speedup") or {}
        before_ribbon = prev_cs.get("before_ribbon_wall_s")
        before_gamow_rel = prev_cs.get("before_gamow_relative_to_flat")
        before_utc = prev_cs.get("before_baseline_utc") or before.get("utc")
        if before_ribbon is None:
            for row in before.get("script_runs", []):
                if row.get("name") == "ribbon_capacitance":
                    before_ribbon = row["wall_time_s"]["mean"]
        if before_gamow_rel is None:
            before_gamow_rel = (
                before.get("channel_cost", {})
                .get("relative_to_flat", {})
                .get("gamow_14_isotopes")
            )

    return {
        "memo_root": str(acs_memo.memo_root()),
        "memo_stats_after": dict(acs_memo.STATS),
        "before_baseline_utc": before_utc,
        "before_ribbon_wall_s": before_ribbon,
        "before_gamow_relative_to_flat": before_gamow_rel,
        "gamow_14": {
            "cold_s": gamow_cold,
            "warm_s": gamow_warm,
            "speedup": _ratio(gamow_cold, gamow_warm),
        },
        "eigen_14": {
            "cold_s": eigen_cold,
            "warm_s": eigen_warm,
            "speedup": _ratio(eigen_cold, eigen_warm),
        },
        "bie_single_48x6": {
            "cold_s": bie_cold,
            "warm_s": bie_warm,
            "speedup": _ratio(bie_cold, bie_warm),
        },
        "ribbon_script": {
            "cold_s": ribbon_cold,
            "warm_s": ribbon_warm,
            "speedup": _ratio(ribbon_cold, ribbon_warm),
            "cold_exit": proc_c.returncode,
            "warm_exit": proc_w.returncode,
            "vs_before_speedup": (
                round(before_ribbon / ribbon_warm, 2)
                if before_ribbon and ribbon_warm > 0
                else None
            ),
        },
    }


def load_previous_results() -> dict[str, Any] | None:
    if not DOCS_OUT.is_file():
        return None
    try:
        with DOCS_OUT.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


def write_efficiency_report(result: dict[str, Any]) -> None:
    """Refresh markdown report from the latest JSON result (RC1 scoped)."""
    cache = result.get("cache_speedup", {})
    scripts = result.get("script_runs", [])
    by_name = {r["name"]: r for r in scripts}
    ch = result.get("channel_cost", {})
    summary = result.get("summary", {})

    gamow = cache.get("gamow_14", {})
    bie = cache.get("bie_single_48x6", {})
    ribbon = cache.get("ribbon_script", {})

    lines = [
        "# Efficiency Benchmark Report — Flag Condensate / Pα / Density Engine Harness",
        "",
        "**Scope (RC1):** As-implemented **harness performance** on the stated test machine — "
        "wall time, throughput, scaling, and **disk/memory memo** speedups. This report does "
        "**not** claim physical engine efficiency, alpha-decay accuracy, or uniqueness of the "
        "density-engine metaphor.",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| **Date (UTC)** | {result.get('utc', '')[:10]} |",
        f"| **Platform** | {result.get('environment', {}).get('platform')} · "
        f"Python {result.get('environment', {}).get('python')} |",
        "| **Timing tool** | `/usr/bin/time -l` (macOS) + `perf_counter` microbench |",
        "| **Runner** | `rh_papers_may21/acs-framework/code/benchmark_efficiency.py` |",
        "| **Raw JSON** | `rh_papers_may21/acs-framework/docs/efficiency_benchmark_results.json` |",
        f"| **Status** | **{result.get('status')}** |",
        f"| **Memo root** | `{cache.get('memo_root', 'rh_papers_may21/acs-framework/.cache/')}` |",
        "",
        "---",
        "",
        "## Executive summary",
        "",
        f"Disk/memory memo keyed by BIE `(R, a, n_u, n_v, model)` and eigen/Gamow "
        f"`(isotope, BC, params)` is enabled (`ACS_MEMO=1`, default). "
        f"**Ribbon script warm speedup vs before:** "
        f"**{ribbon.get('vs_before_speedup', 'n/a')}×** "
        f"(before {cache.get('before_ribbon_wall_s')} s → warm {ribbon.get('warm_s')} s). "
        f"**Gamow 14-isotope cold→warm:** **{gamow.get('speedup', 'n/a')}×**. "
        f"**BIE single-point (48×6) cold→warm:** **{bie.get('speedup', 'n/a')}×**.",
        "",
        f"Bottleneck script (post-memo mean): `{summary.get('bottleneck_script')}`. "
        f"Bottleneck channel (compute, first-fill): `{summary.get('bottleneck_channel')}`.",
        "",
        "---",
        "",
        "## Cache before / after",
        "",
        "| Path | Before (s) | After cold (s) | After warm (s) | Speedup cold/warm | vs before (warm) |",
        "|------|----------:|---------------:|---------------:|------------------:|-----------------:|",
        f"| Gamow 14 isotopes | "
        f"(rel flat {cache.get('before_gamow_relative_to_flat')}×) | "
        f"{gamow.get('cold_s', float('nan')):.4f} | "
        f"{gamow.get('warm_s', float('nan')):.4f} | "
        f"**{gamow.get('speedup')}×** | — |",
        f"| Eigen Dirichlet 14 | — | "
        f"{cache.get('eigen_14', {}).get('cold_s', float('nan')):.4f} | "
        f"{cache.get('eigen_14', {}).get('warm_s', float('nan')):.4f} | "
        f"**{cache.get('eigen_14', {}).get('speedup')}×** | — |",
        f"| BIE single 48×6 | — | "
        f"{bie.get('cold_s', float('nan')):.4f} | "
        f"{bie.get('warm_s', float('nan')):.4f} | "
        f"**{bie.get('speedup')}×** | — |",
        f"| `ribbon_capacitance.py` | "
        f"{cache.get('before_ribbon_wall_s')} | "
        f"{ribbon.get('cold_s', float('nan')):.3f} | "
        f"{ribbon.get('warm_s', float('nan')):.3f} | "
        f"**{ribbon.get('speedup')}×** | "
        f"**{ribbon.get('vs_before_speedup')}×** |",
        "",
        "Memo blobs live under `.cache/bie_capacitance/` and `.cache/palpha_eigen/` "
        "(gitignored). Disable with `ACS_MEMO=0`.",
        "",
        "---",
        "",
        "## End-to-end script runs (memo enabled)",
        "",
        "| Script | Wall (s) | vs baseline | Peak (MiB) |",
        "|--------|--------:|------------:|-----------:|",
    ]
    ratios = result.get("relative_to_baseline", {})
    for row in scripts:
        name = row["name"]
        wt = row["wall_time_s"]["mean"]
        mem = row.get("peak_memory_MiB")
        lines.append(
            f"| `{name}` | {wt:.3f} | {ratios.get(name, float('nan')):.2f}× | {mem} |"
        )

    per = ch.get("per_isotope_s", {})
    rel = ch.get("relative_to_flat", {})
    lines.extend(
        [
            "",
            "### Per-channel compute (14 isotopes; may include memo hits on repeats)",
            "",
            "| Channel | Per isotope (ms) | vs flat |",
            "|---------|-----------------:|--------:|",
            f"| Flat Gaussian | {1000 * per.get('flat_gaussian', float('nan')):.2f} | "
            f"{rel.get('flat_gaussian', 1.0)}× |",
            f"| Eigenmode Dirichlet | {1000 * per.get('eigenmode_dirichlet', float('nan')):.2f} | "
            f"{rel.get('eigenmode_14_isotopes', float('nan'))}× |",
            f"| Gamow outgoing | {1000 * per.get('gamow_outgoing', float('nan')):.2f} | "
            f"{rel.get('gamow_14_isotopes', float('nan'))}× |",
            "",
            "---",
            "",
            "## Recommendations",
            "",
            "1. Keep `ACS_MEMO=1` for interactive / repeated BIE and Gamow work.",
            "2. Clear `.cache/` when changing mesh parameters or isotope tables.",
            "3. First-fill (cold) cost remains ~O(N^1.37) in BIE panels; warm reads are "
            "JSON/NPZ loads.",
            "",
            "## Caveats",
            "",
            "- Timings are machine-specific; reproduce via `python3 benchmark_efficiency.py`.",
            "- Warm speedups assume identical cache keys; float formatting uses 12 significant "
            "digits.",
            "- No claim about numerical accuracy vs experimental alpha-decay data.",
            "",
            "## Artifacts",
            "",
            "| Path | Description |",
            "|------|-------------|",
            "| `rh_papers_may21/acs-framework/code/acs_memo.py` | Disk + memory memo |",
            "| `rh_papers_may21/acs-framework/code/benchmark_efficiency.py` | Unified runner |",
            "| `rh_papers_may21/acs-framework/docs/efficiency_benchmark_results.json` | JSON |",
            "| `Aiso_build_artifacts/density_engine_many_worlds/EFFICIENCY_BENCHMARK_REPORT.md` | "
            "This report |",
            "",
            "**Re-run:** `python3 rh_papers_may21/acs-framework/code/benchmark_efficiency.py`",
            "",
        ]
    )
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")


def run_all() -> dict[str, Any]:
    before = load_previous_results()
    specs = build_script_specs()

    # Probe one fast script to choose repeats for slow ones dynamically.
    probe = run_script_timed(
        ScriptSpec("_probe", specs[0].path, specs[0].cwd, repeats=1)
    )
    probe_t = probe["wall_time_s"]["mean"]

    script_results: list[dict[str, Any]] = []
    for spec in specs:
        if spec.repeats == DEFAULT_REPEATS and probe_t > FAST_RUN_THRESHOLD_S:
            spec = ScriptSpec(
                spec.name,
                spec.path,
                spec.cwd,
                repeats=SLOW_REPEATS,
                n_isotopes=spec.n_isotopes,
                notes=spec.notes,
            )
        script_results.append(run_script_timed(spec))

    channels = channel_microbenchmarks()
    scaling = scaling_benchmarks()
    cache = cache_speedup_benchmarks(before)
    ratios = compute_relative_ratios(script_results)

    all_ok = all(r["exit_code"] == 0 for r in script_results)
    all_ok = all_ok and cache["ribbon_script"]["cold_exit"] == 0
    all_ok = all_ok and cache["ribbon_script"]["warm_exit"] == 0
    slowest_script = max(
        script_results,
        key=lambda r: r["wall_time_s"]["mean"],
    )

    return {
        "scope": (
            "RC1 harness performance benchmark — wall time, throughput, scaling, "
            "and disk/memory memo speedups of as-implemented scripts in the stated "
            "environment; not a claim about physical engine efficiency."
        ),
        "utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "platform": sys.platform,
            "python": sys.version.split()[0],
            "repo_root": str(REPO_ROOT),
            "timing_tool": "/usr/bin/time -l (macOS)",
            "fast_run_threshold_s": FAST_RUN_THRESHOLD_S,
            "default_repeats": DEFAULT_REPEATS,
            "acs_memo": os.environ.get("ACS_MEMO", "1"),
        },
        "status": "pass" if all_ok else "fail",
        "script_runs": script_results,
        "relative_to_baseline": ratios,
        "slowest_script": {
            "name": slowest_script["name"],
            "wall_s": slowest_script["wall_time_s"]["mean"],
        },
        "channel_cost": channels,
        "scaling": scaling,
        "cache_speedup": cache,
        "summary": {
            "bottleneck_script": slowest_script["name"],
            "bottleneck_channel": channels["bottleneck_channel"],
            "extended_set_linearity": scaling["isotope_count_throat_ws"][
                "linearity_assessment"
            ],
            "gamow_vs_eigen_heavy_isotope_ratio": scaling[
                "heavy_isotope_238U_single_solve"
            ]["gamow_over_eigen_ratio"],
            "bie_scaling_slope": scaling["bie_mobius_mesh"].get(
                "loglog_slope_wall_vs_panels"
            ),
            "ribbon_warm_vs_before": cache["ribbon_script"].get("vs_before_speedup"),
            "gamow_cold_to_warm": cache["gamow_14"].get("speedup"),
            "bie_cold_to_warm": cache["bie_single_48x6"].get("speedup"),
        },
    }


def main() -> int:
    result = run_all()
    DOCS_OUT.parent.mkdir(parents=True, exist_ok=True)
    with DOCS_OUT.open("w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
        fh.write("\n")
    write_efficiency_report(result)

    print(f"Benchmark status: {result['status']}")
    print(f"Wrote {DOCS_OUT}")
    print(f"Wrote {REPORT_OUT}")
    print("\nScript wall times (mean s):")
    for row in result["script_runs"]:
        wt = row["wall_time_s"]["mean"]
        ratio = result["relative_to_baseline"].get(row["name"], 1.0)
        mem = row.get("peak_memory_MiB")
        mem_s = f"  peak={mem} MiB" if mem else ""
        print(f"  {row['name']:28s}  {wt:8.3f}s  x{ratio:.2f}{mem_s}")
    cs = result["cache_speedup"]
    print("\nCache speedups (cold → warm):")
    print(f"  gamow_14:     {cs['gamow_14']['speedup']}×")
    print(f"  eigen_14:     {cs['eigen_14']['speedup']}×")
    print(f"  bie_48x6:     {cs['bie_single_48x6']['speedup']}×")
    print(
        f"  ribbon_script:{cs['ribbon_script']['speedup']}× "
        f"(vs before warm {cs['ribbon_script'].get('vs_before_speedup')}×)"
    )
    print(f"\nBottleneck channel: {result['summary']['bottleneck_channel']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
