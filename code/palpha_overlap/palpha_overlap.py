#!/usr/bin/env python3
"""
P_alpha standing-wave overlap (sequel proxy to Flag_Condensate_Nuclear_Decay).

Computes a geometric/structural preformation proxy:

    P_model = |∫_0^R u_in(r) u_alpha(r) dr|^2
              / ( ∫_0^R u_in(r)^2 dr  ·  ∫_0^R u_alpha(r)^2 dr )

where, for ell=0 reduced radial modes on the nuclear throat [0, R]:

  - flag interior mode:  u_in(r) ∝ r j_0(k r),  j_0(k R)=0 ⇒ k=π/R
  - alpha cluster trial: u_alpha(r) ∝ r exp(-r^2 / (2 a_alpha^2)),
                         a_alpha = r0 * 4^(1/3),  r0 ≈ 1.2 fm (input)

Scope (RC1):
  This is a standing-wave overlap proxy, not a first-principles many-body
  nuclear-structure calculation. Absolute scale may require one global
  spectroscopic/angular factor S. Half-lives are not used to build P_model;
  extracted log10 P_alpha from the nuclear-decay table is used only for
  comparison.

Dependencies: numpy, scipy.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import simpson
from scipy.special import spherical_jn

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_DOCS = (
    Path(__file__).resolve().parents[2] / "docs" / "palpha_overlap_results.json"
)

# ---------------------------------------------------------------------------
# Table data (Flag_Condensate_Nuclear_Decay, 14 isotopes)
# ---------------------------------------------------------------------------

R0_DEFAULT_FM = 1.2
N_GRID = 4096


@dataclass(frozen=True)
class IsotopeRow:
    name: str
    Q_alpha_MeV: float
    R_fm: float
    b_fm: float
    W_ana: float
    t12_Gamow_s: float
    t12_meas_s: float
    log10_P_extracted: float


ISOTOPES: tuple[IsotopeRow, ...] = (
    IsotopeRow("212Po", 8.954, 8.99, 26.33, 14.821, 8.74e-9, 2.99e-7, -1.53),
    IsotopeRow("214Po", 7.833, 9.02, 30.10, 18.204, 1.05e-5, 1.64e-4, -1.19),
    IsotopeRow("216Po", 6.906, 9.05, 34.14, 21.720, 0.0132, 0.145, -1.04),
    IsotopeRow("218Po", 6.115, 9.07, 38.56, 25.549, 28.45, 186.0, -0.82),
    IsotopeRow("220Rn", 6.405, 9.10, 37.71, 24.629, 4.18, 55.6, -1.12),
    IsotopeRow("224Ra", 5.789, 9.16, 42.67, 28.514, 9.21e3, 3.16e5, -1.54),
    IsotopeRow("226Ra", 4.871, 9.18, 50.70, 34.341, 9.45e8, 5.05e10, -1.73),
    IsotopeRow("228Th", 5.520, 9.21, 45.72, 30.829, 8.07e5, 6.04e7, -1.87),
    IsotopeRow("232Th", 4.082, 9.26, 61.84, 42.673, 2.98e15, 4.43e17, -2.17),
    IsotopeRow("234U", 4.858, 9.29, 52.92, 35.830, 1.76e10, 7.74e12, -2.64),
    IsotopeRow("238U", 4.270, 9.34, 60.20, 41.517, 1.52e15, 1.41e17, -1.97),
    IsotopeRow("238Pu", 5.593, 9.34, 45.98, 31.066, 1.44e6, 2.77e9, -3.28),
    IsotopeRow("240Pu", 5.256, 9.36, 48.93, 33.626, 2.55e8, 2.07e11, -2.91),
    IsotopeRow("244Cm", 5.902, 9.42, 44.47, 29.832, 1.39e5, 5.72e8, -3.61),
)


# ---------------------------------------------------------------------------
# Radial modes and overlap
# ---------------------------------------------------------------------------


def a_alpha_fm(r0_fm: float = R0_DEFAULT_FM) -> float:
    """Alpha HO/Gaussian length: a_alpha = r0 * A_alpha^(1/3), A_alpha=4."""
    return r0_fm * (4.0 ** (1.0 / 3.0))


def u_in(r: np.ndarray, R_fm: float) -> np.ndarray:
    """
    Interior flag reduced radial mode, ell=0:
      u_in(r) = r * j_0(k r),  k = pi/R  (first Dirichlet zero of j_0).
    Equivalent to sin(k r)/k on (0,R]; zero at r=0 by continuity.
    """
    k = math.pi / R_fm
    # spherical_jn(0, x) = sin(x)/x; at x=0 use limit
    x = k * r
    j0 = spherical_jn(0, x)
    return r * j0


def u_alpha(r: np.ndarray, a_fm: float) -> np.ndarray:
    """Alpha-cluster trial reduced radial mode (HO 0s / Gaussian packet)."""
    return r * np.exp(-(r * r) / (2.0 * a_fm * a_fm))


def overlap_P(
    R_fm: float,
    r0_fm: float = R0_DEFAULT_FM,
    n_grid: int = N_GRID,
) -> float:
    """
    Normalized squared overlap on [0, R]:

      P = |∫ u_in u_alpha dr|^2 / (∫ u_in^2 dr · ∫ u_alpha^2 dr)

    Both modes are truncated/supported on [0, R] and integrated numerically.
    """
    if R_fm <= 0.0:
        raise ValueError(f"R_fm must be positive, got {R_fm}")
    # Exclude exact r=0 endpoint singularity bookkeeping; j0 limit is fine,
    # but start slightly above 0 for uniform grid stability.
    r = np.linspace(0.0, R_fm, n_grid)
    a = a_alpha_fm(r0_fm)
    ui = u_in(r, R_fm)
    ua = u_alpha(r, a)
    num = simpson(ui * ua, x=r)
    den_in = simpson(ui * ui, x=r)
    den_a = simpson(ua * ua, x=r)
    if den_in <= 0.0 or den_a <= 0.0:
        raise RuntimeError("non-positive mode norms")
    return float((num * num) / (den_in * den_a))


def pearson_r(x: np.ndarray, y: np.ndarray) -> float:
    if x.size < 2:
        return float("nan")
    x0 = x - x.mean()
    y0 = y - y.mean()
    denom = float(np.sqrt(np.sum(x0 * x0) * np.sum(y0 * y0)))
    if denom == 0.0:
        return float("nan")
    return float(np.sum(x0 * y0) / denom)


def best_fit_global_S(log10_P_model: np.ndarray, log10_P_ext: np.ndarray) -> float:
    """
    Fit log10(S * P_model) ≈ log10_P_ext in the mean residual sense:

      log10 S = mean(log10_P_ext - log10_P_model)
      S = 10^(log10 S)

    Equivalent to matching geometric means of P.
    """
    return float(10.0 ** np.mean(log10_P_ext - log10_P_model))


# ---------------------------------------------------------------------------
# Per-isotope evaluation
# ---------------------------------------------------------------------------


def evaluate_isotope(
    row: IsotopeRow,
    r0_fm: float = R0_DEFAULT_FM,
    n_grid: int = N_GRID,
) -> dict[str, Any]:
    P_raw = overlap_P(row.R_fm, r0_fm=r0_fm, n_grid=n_grid)
    log10_P_model = math.log10(P_raw) if P_raw > 0.0 else float("-inf")

    P_ext_from_halflife = row.t12_Gamow_s / row.t12_meas_s
    log10_P_ext_check = (
        math.log10(P_ext_from_halflife) if P_ext_from_halflife > 0.0 else float("-inf")
    )
    table_vs_check = row.log10_P_extracted - log10_P_ext_check

    return {
        "isotope": row.name,
        "Q_alpha_MeV": row.Q_alpha_MeV,
        "R_fm": row.R_fm,
        "b_fm": row.b_fm,
        "W_ana": row.W_ana,
        "t12_Gamow_s": row.t12_Gamow_s,
        "t12_meas_s": row.t12_meas_s,
        "a_alpha_fm": a_alpha_fm(r0_fm),
        "P_model": P_raw,
        "log10_P_model": log10_P_model,
        "log10_P_extracted": row.log10_P_extracted,
        "residual_raw": log10_P_model - row.log10_P_extracted,
        "P_ext_halflife": P_ext_from_halflife,
        "log10_P_ext_halflife": log10_P_ext_check,
        "log10_P_table_minus_halflife_check": table_vs_check,
    }


def run_analysis(
    r0_fm: float = R0_DEFAULT_FM,
    n_grid: int = N_GRID,
) -> dict[str, Any]:
    rows = [evaluate_isotope(iso, r0_fm=r0_fm, n_grid=n_grid) for iso in ISOTOPES]

    log10_model = np.array([r["log10_P_model"] for r in rows], dtype=float)
    log10_ext = np.array([r["log10_P_extracted"] for r in rows], dtype=float)
    residuals_raw = log10_model - log10_ext

    S = best_fit_global_S(log10_model, log10_ext)
    log10_model_S = log10_model + math.log10(S)
    residuals_S = log10_model_S - log10_ext

    for r, lmS, resS in zip(rows, log10_model_S, residuals_S):
        r["P_model_S"] = float(r["P_model"] * S)
        r["log10_P_model_S"] = float(lmS)
        r["residual_S"] = float(resS)

    corr_raw = pearson_r(log10_model, log10_ext)
    corr_S = pearson_r(log10_model_S, log10_ext)  # identical to corr_raw (affine)

    rms_raw = float(np.sqrt(np.mean(residuals_raw**2)))
    rms_S = float(np.sqrt(np.mean(residuals_S**2)))
    mean_abs_raw = float(np.mean(np.abs(residuals_raw)))
    mean_abs_S = float(np.mean(np.abs(residuals_S)))

    summary = {
        "n_isotopes": len(rows),
        "r0_fm": r0_fm,
        "a_alpha_fm": a_alpha_fm(r0_fm),
        "n_grid": n_grid,
        "mean_log10_P_model": float(np.mean(log10_model)),
        "std_log10_P_model": float(np.std(log10_model, ddof=1)),
        "mean_log10_P_extracted": float(np.mean(log10_ext)),
        "std_log10_P_extracted": float(np.std(log10_ext, ddof=1)),
        "pearson_r_raw": corr_raw,
        "pearson_r_with_S": corr_S,
        "mean_residual_raw": float(np.mean(residuals_raw)),
        "rms_residual_raw": rms_raw,
        "mean_abs_residual_raw": mean_abs_raw,
        "best_fit_global_S": S,
        "log10_S": float(math.log10(S)),
        "mean_residual_S": float(np.mean(residuals_S)),
        "rms_residual_S": rms_S,
        "mean_abs_residual_S": mean_abs_S,
        "S_improves_rms": bool(rms_S < rms_raw),
        "rms_improvement": float(rms_raw - rms_S),
        "scope_note": (
            "P_model is a geometric/structural standing-wave overlap proxy "
            "between confined flag mode and alpha-like Gaussian packet on [0,R]. "
            "Absolute scale may need one global factor S; this is not a "
            "first-principles many-body nuclear-structure prediction."
        ),
    }

    return {
        "model": {
            "u_in": "r * j_0(k r), k=pi/R (ell=0 first zero)",
            "u_alpha": "r * exp(-r^2/(2 a_alpha^2)), a_alpha=r0*4^(1/3)",
            "P_definition": (
                "|∫ u_in u_alpha dr|^2 / (∫ u_in^2 dr · ∫ u_alpha^2 dr) "
                "on [0,R]; optional P_S = S * P_model"
            ),
            "P_extracted_definition": "P_ext = t_Gamow / t_meas (consistency check)",
        },
        "summary": summary,
        "isotopes": rows,
        "table_source": (
            "Flag_Condensate_Nuclear_Decay.tex table (14 alpha emitters)"
        ),
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def format_markdown_table(result: dict[str, Any]) -> str:
    lines = [
        "| Isotope | R (fm) | P_model | log10 P_model | log10 P_ext | "
        "resid (raw) | log10 P_model·S | resid (S) |",
        "|---------|-------:|--------:|--------------:|------------:|"
        "------------:|----------------:|----------:|",
    ]
    for r in result["isotopes"]:
        lines.append(
            f"| {r['isotope']} | {r['R_fm']:.2f} | {r['P_model']:.6e} | "
            f"{r['log10_P_model']:+.4f} | {r['log10_P_extracted']:+.2f} | "
            f"{r['residual_raw']:+.4f} | {r['log10_P_model_S']:+.4f} | "
            f"{r['residual_S']:+.4f} |"
        )
    s = result["summary"]
    lines.extend(
        [
            "",
            "### Summary",
            f"- mean log10 P_model = {s['mean_log10_P_model']:+.4f} "
            f"(std {s['std_log10_P_model']:.4f})",
            f"- mean log10 P_extracted = {s['mean_log10_P_extracted']:+.4f} "
            f"(std {s['std_log10_P_extracted']:.4f})",
            f"- Pearson r (log10 P_model vs extracted) = {s['pearson_r_raw']:+.4f}",
            f"- RMS residual (S=1) = {s['rms_residual_raw']:.4f}",
            f"- best-fit global S = {s['best_fit_global_S']:.6e} "
            f"(log10 S = {s['log10_S']:+.4f})",
            f"- RMS residual (with S) = {s['rms_residual_S']:.4f} "
            f"(improvement {s['rms_improvement']:+.4f})",
            f"- S improves RMS match: {s['S_improves_rms']}",
            f"- a_alpha = {s['a_alpha_fm']:.4f} fm (r0 = {s['r0_fm']} fm)",
            "",
            f"_Scope:_ {s['scope_note']}",
        ]
    )
    return "\n".join(lines)


def write_json(result: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Convert numpy scalars if any slipped through
    def _default(obj: Any) -> Any:
        if isinstance(obj, (np.floating, np.integer)):
            return obj.item()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    with path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=_default)
        f.write("\n")


def main() -> int:
    result = run_analysis(r0_fm=R0_DEFAULT_FM, n_grid=N_GRID)
    out_path = REPO_DOCS
    write_json(result, out_path)

    log_dir = out_path.parent / "palpha_overlap_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    from datetime import datetime, timezone

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report = format_markdown_table(result)
    header = (
        f"# P_α standing-wave overlap results\n"
        f"# utc={stamp}  r0_fm={R0_DEFAULT_FM}  n_grid={N_GRID}\n\n"
    )
    log_body = header + report + f"\n\nJSON written: {out_path}\n"
    log_path = log_dir / f"run_{stamp}.log"
    log_path.write_text(log_body, encoding="utf-8")

    print(log_body)
    print(f"Log written: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
