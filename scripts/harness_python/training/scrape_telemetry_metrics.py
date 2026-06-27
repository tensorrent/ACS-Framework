#!/usr/bin/env python3
"""Scan a sweep directory for report.json files and print telemetry metric rows."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

# Below this, treat aux_mean and ratio as zero for band labeling (avoids "ghost signal").
EPS_NO_TELEMETRY = 1e-9
# Fewer than this many finite-ratio runs per weight → flag low confidence.
MIN_VALID_CONFIDENCE = 3


def find_reports(root: Path) -> list[Path]:
    return sorted(root.rglob("report.json"))


def safe_metric(fm: dict[str, Any], key: str) -> float:
    if key not in fm:
        return float("nan")
    val = fm.get(key)
    if val is None:
        return float("nan")
    try:
        return float(val)
    except (TypeError, ValueError):
        return float("nan")


def fmt_num(x: float, width: int, prec: int) -> str:
    if not math.isfinite(x):
        return "—".rjust(width)
    return f"{x:>{width}.{prec}f}"


def extract(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        j = json.load(f)
    cfg = j.get("config", {}) or {}
    fm = j.get("final_metrics", {}) or {}
    w = cfg.get("telemetry_aux_weight", "")
    label = cfg.get("run_label") or ""
    row_frac = safe_metric(fm, "telemetry_row_frac")
    aux_mean = safe_metric(fm, "telemetry_aux_mean_abs")
    ratio = safe_metric(fm, "telemetry_aux_to_base_ratio")
    return {
        "run_label": label,
        "weight": w,
        "row_frac": row_frac,
        "aux_mean": aux_mean,
        "ratio": ratio,
        "path": str(path),
        "band": interpret_band(aux_mean, ratio),
    }


def interpret_band(aux_mean: float, ratio: float) -> str:
    if math.isnan(aux_mean) or math.isnan(ratio):
        return "missing"
    if abs(aux_mean) < EPS_NO_TELEMETRY and abs(ratio) < EPS_NO_TELEMETRY:
        return "no telemetry"
    r = ratio
    if r < 0.03:
        return "too weak"
    if r < 0.08:
        return "emerging"
    if r < 0.2:
        return "useful"
    return "strong"


def _group_weight_key(w: Any) -> float | str:
    try:
        return float(w)
    except (TypeError, ValueError):
        return str(w)


def _pstdev_safe(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    return statistics.pstdev(xs)


def _mean_finite(xs: list[float]) -> float:
    xf = [x for x in xs if math.isfinite(x)]
    if not xf:
        return float("nan")
    return statistics.mean(xf)


def _sorted_weight_keys(keys: list[float | str]) -> list[float | str]:
    def k(x: float | str) -> tuple[int, float, str]:
        if isinstance(x, float):
            return (0, x, "")
        return (1, 0.0, str(x))

    return sorted(keys, key=k)


def aggregate(rows: list[dict[str, Any]]) -> list[str]:
    by_w: dict[float | str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_w[_group_weight_key(r["weight"])].append(r)

    low_conf_warnings: list[str] = []

    print()
    print("AGGREGATE (per weight, mean ± std; finite values only)")
    print(f"{'w':>8} {'n (v)':>26} {'row_frac':>10} {'aux_mean':>18} {'ratio':>18}")
    print("-" * 84)
    for wk in _sorted_weight_keys(list(by_w.keys())):
        group = by_w[wk]
        n = len(group)
        valid_ratio = sum(1 for x in group if math.isfinite(float(x["ratio"])))
        rf = [float(x["row_frac"]) for x in group]
        am = [float(x["aux_mean"]) for x in group]
        rr = [float(x["ratio"]) for x in group]
        m_rf = _mean_finite(rf)
        m_am = _mean_finite(am)
        m_rr = _mean_finite(rr)
        am_f = [x for x in am if math.isfinite(x)]
        rr_f = [x for x in rr if math.isfinite(x)]
        s_am = _pstdev_safe(am_f)
        s_rr = _pstdev_safe(rr_f)
        wdisp = f"{wk}" if isinstance(wk, str) else f"{wk:g}"
        rf_s = fmt_num(m_rf, 10, 4)
        am_cell = (
            f"{m_am:9.6f} ±{s_am:.6f}" if math.isfinite(m_am) else "—"
        )
        rr_cell = f"{m_rr:9.4f} ±{s_rr:.4f}" if math.isfinite(m_rr) else "—"
        tag = ""
        if 0 < valid_ratio < MIN_VALID_CONFIDENCE:
            tag = " ⚠ low conf"
            low_conf_warnings.append(
                f"weight {wdisp} has only {valid_ratio} valid run(s) → aggregate may be noisy"
            )
        n_cell = f"{n} (v={valid_ratio}){tag}"
        print(f"{wdisp:>8} {n_cell:>26} {rf_s} {am_cell:>24} {rr_cell:>22}")

    if low_conf_warnings:
        print()
        for msg in low_conf_warnings:
            print(f"[warning] {msg}")

    return low_conf_warnings


def mean_ratio_by_weight(rows: list[dict[str, Any]]) -> dict[float | str, float]:
    by_w: dict[float | str, list[float]] = defaultdict(list)
    for r in rows:
        x = float(r["ratio"])
        if math.isfinite(x):
            by_w[_group_weight_key(r["weight"])].append(x)
    return {w: statistics.mean(v) for w, v in by_w.items() if v}


def valid_ratio_count_by_weight(rows: list[dict[str, Any]]) -> dict[float | str, int]:
    by_w: dict[float | str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_w[_group_weight_key(r["weight"])].append(r)
    return {
        w: sum(1 for x in g if math.isfinite(float(x["ratio"])))
        for w, g in by_w.items()
    }


def suggest_best_weight(rows: list[dict[str, Any]]) -> None:
    mr = mean_ratio_by_weight(rows)
    counts = valid_ratio_count_by_weight(rows)
    if not mr:
        print()
        print("[suggestion] no finite ratio values to compare")
        return
    best = max(mr.items(), key=lambda kv: kv[1])
    print()
    print(
        f"[suggestion] highest mean ratio at weight={best[0]} ({best[1]:.4f})"
    )
    reliable = {
        w: mr[w]
        for w in mr
        if counts.get(w, 0) >= MIN_VALID_CONFIDENCE
    }
    if reliable:
        best_r = max(reliable.items(), key=lambda kv: kv[1])
        v_best = counts.get(best_r[0], 0)
        print(
            f"[suggestion] best reliable weight (v>={MIN_VALID_CONFIDENCE}) = "
            f"{best_r[0]} ({best_r[1]:.4f}) [v={v_best}]"
        )
    else:
        print(
            f"[suggestion] no weight meets minimum confidence (v>={MIN_VALID_CONFIDENCE})"
        )


def print_ratio_trend(mr: dict[float | str, float]) -> None:
    """Mean ratio vs telemetry_aux_weight order (numeric weights sorted ascending)."""
    if len(mr) < 2:
        return
    sorted_w = _sorted_weight_keys(list(mr.keys()))
    ratios = [mr[w] for w in sorted_w]
    if len(ratios) < 2:
        return
    increasing = all(ratios[i] <= ratios[i + 1] for i in range(len(ratios) - 1))
    decreasing = all(ratios[i] >= ratios[i + 1] for i in range(len(ratios) - 1))
    print()
    if increasing and not decreasing:
        print("[trend] ratio increases with weight (expected scaling)")
    elif decreasing and not increasing:
        print("[trend] ratio decreases with weight (unexpected)")
    else:
        print("[trend] non-monotonic ratio (possible noise or saturation)")


def detect_row_frac(rows: list[dict[str, Any]]) -> None:
    vals = [
        float(r["row_frac"])
        for r in rows
        if math.isfinite(r["row_frac"]) and r["row_frac"] > 0
    ]
    if len(vals) < 2:
        return
    span = max(vals) - min(vals)
    if span > 1e-4:
        print()
        print(
            "[diagnostic] row_frac varies across runs → mixed merge volumes (x1 vs x50?)"
        )


def detect_flat_scaling(rows: list[dict[str, Any]]) -> None:
    by_w: dict[float | str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_w[_group_weight_key(r["weight"])].append(r)
    if len(by_w) < 2:
        return

    means_ratio: dict[float | str, float] = {}
    for w, g in by_w.items():
        rr = [float(x["ratio"]) for x in g if math.isfinite(float(x["ratio"]))]
        if not rr:
            continue
        means_ratio[w] = statistics.mean(rr)
    if len(means_ratio) < 2:
        print()
        print(
            "[diagnostic] need ≥2 weights with finite mean ratio to compare scaling "
            "(mixed old/new reports or missing telemetry fields?)"
        )
        return

    vals = list(means_ratio.values())
    span = max(vals) - min(vals)
    if span >= 0.01:
        return

    aux_all = [float(r["aux_mean"]) for r in rows if math.isfinite(float(r["aux_mean"]))]
    if len(aux_all) < 2:
        print()
        print(
            "[diagnostic] aux span not computable (need ≥2 finite aux_mean values across scanned reports)"
        )
        return

    aux_span = max(aux_all) - min(aux_all)
    print()
    if aux_span < 1e-6:
        print(
            "[diagnostic] ratio flat across weights + aux_mean flat "
            f"(mean span {span:.4f}, aux span {aux_span:.2e}) → duplicate telemetry rows dominating"
        )
    else:
        print(
            "[diagnostic] ratio flat across weights but aux_mean varies "
            f"(mean span {span:.4f}, aux span {aux_span:.6f}) → trainer may be saturating or clipping"
        )


def _weight_sort_key(w: Any) -> tuple[int, float, str]:
    try:
        return (0, float(w), "")
    except (TypeError, ValueError):
        return (1, 0.0, str(w))


def _ratio_desc_key(r: dict[str, Any]) -> tuple[int, float]:
    """Descending ratio; NaN last."""
    x = float(r["ratio"])
    if math.isnan(x):
        return (1, 0.0)
    return (0, -x)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Print telemetry_row_frac, telemetry_aux_mean_abs, telemetry_aux_to_base_ratio from sweep report.json files."
    )
    ap.add_argument(
        "sweep_dir",
        type=Path,
        help="Root directory to scan recursively for report.json",
    )
    ap.add_argument(
        "--sort",
        choices=("weight", "ratio"),
        default="weight",
        help="Sort per-run rows by weight (default) or descending ratio.",
    )
    args = ap.parse_args()
    root = args.sweep_dir
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 1

    paths = find_reports(root)
    if not paths:
        print(f"no report.json under {root}", file=sys.stderr)
        return 1

    rows = [extract(p) for p in paths]
    if args.sort == "weight":
        rows.sort(
            key=lambda r: (
                _weight_sort_key(r["weight"]),
                _ratio_desc_key(r),
                str(r["run_label"]),
                r["path"],
            )
        )
    else:
        rows.sort(
            key=lambda r: (
                _ratio_desc_key(r),
                _weight_sort_key(r["weight"]),
                str(r["run_label"]),
                r["path"],
            )
        )

    print(
        f"{'label':22} {'w':>8} {'row_frac':>10} {'aux_mean':>12} {'ratio':>10} {'band':>12}"
    )
    print("-" * 82)
    for r in rows:
        lab = (r["run_label"] or "")[:22]
        wstr = str(r["weight"]) if r["weight"] != "" else ""
        print(
            f"{lab:22} "
            f"{wstr:>8} "
            f"{fmt_num(r['row_frac'], 10, 4)} "
            f"{fmt_num(r['aux_mean'], 12, 6)} "
            f"{fmt_num(r['ratio'], 10, 4)} "
            f"{r['band']:>12}"
        )

    aggregate(rows)
    suggest_best_weight(rows)
    print_ratio_trend(mean_ratio_by_weight(rows))
    detect_row_frac(rows)
    detect_flat_scaling(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
