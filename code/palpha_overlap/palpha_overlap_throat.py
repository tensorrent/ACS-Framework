#!/usr/bin/env python3
"""
P_alpha throat-geometry overlap (sequel to flat [0,R] standing-wave proxy).

Extends palpha_overlap.py without deleting it. Primary model:

  P = |∫ u_in(r) u_alpha(r) w(r) dr|^2
      / ( ∫ u_in^2 w dr  ·  ∫ u_alpha^2 w dr )

Throat weight (documented choice)
---------------------------------
Companion nuclear note (Flag_Condensate_Nuclear_Decay) gives an AdS-like
confining-throat line element

    ds^2 = (R^2 / r^2) dr^2 + ...

so √g_rr = R/r.  We take the warped radial measure on the interior throat

    w(r) = R / r    on (0, R],

regular at the origin for reduced modes u ~ r near r=0 (integrand ~ R r).
Integration window for the primary overlap remains the confined interior
[0, R] where the Dirichlet flag mode is defined.  The barrier interval
[R, b] enters Gamow W in the companion paper; it is not re-used here as
an overlap support for u_in (which vanishes at R).

Alpha trials
------------
  - Woods-Saxon (primary):  u_WS(r) = r / (1 + exp((r - R_alpha)/a_WS))
      R_alpha = r0 * 4^(1/3),  a_WS = 0.55 fm (input diffuseness)
  - WS × Coulomb-tail matched: C^1-match exponential tail beyond R_match
      = R_alpha + 2 a_WS, with kappa from a shallow binding scale
      kappa = 1 / a_WS (length-matched; phenomenological, not fitted per isotope)
  - Gaussian/HO (comparison baseline): same as palpha_overlap.py

Also recomputes the flat-measure Gaussian proxy for side-by-side deltas.

Scope (RC1): geometric/structural preformation proxy with warped measure
and WS cluster trial — not a unique many-body nuclear-structure claim.

Dependencies: numpy, scipy.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Literal

import numpy as np
from scipy.integrate import simpson
from scipy.special import spherical_jn

# Reuse isotope table from the flat-proxy module (do not duplicate silently).
from palpha_overlap import (  # type: ignore
    ISOTOPES,
    IsotopeRow,
    R0_DEFAULT_FM,
    a_alpha_fm,
    best_fit_global_S,
    pearson_r,
    u_alpha as u_alpha_gaussian,
    u_in,
)

# ---------------------------------------------------------------------------
# Paths / defaults
# ---------------------------------------------------------------------------

REPO_DOCS = (
    Path(__file__).resolve().parents[2] / "docs" / "palpha_overlap_throat_results.json"
)

N_GRID = 4096
A_WS_DEFAULT_FM = 0.55
KAPPA_TAIL_DEFAULT = 1.0 / A_WS_DEFAULT_FM  # fm^-1; length-matched to diffuseness

AlphaKind = Literal["woods_saxon", "ws_coulomb_tail", "gaussian"]
MeasureKind = Literal["throat_ads", "flat"]


# ---------------------------------------------------------------------------
# Throat weight and alpha trials
# ---------------------------------------------------------------------------


def throat_weight_ads(r: np.ndarray, R_fm: float) -> np.ndarray:
    """
    AdS-like radial measure factor w(r) = R/r from √g_rr on
    ds^2 = (R^2/r^2) dr^2 + ...

    At r=0 the weight formally diverges; for u ~ O(r) the products
    u^2 w and u_in u_alpha w remain integrable.  We set w[0] via the
    first interior sample to keep the grid finite (measure-zero point).
    """
    w = np.empty_like(r, dtype=float)
    w[0] = 0.0  # measure-zero endpoint; integrands vanish as O(r)
    w[1:] = R_fm / r[1:]
    return w


def flat_weight(r: np.ndarray, R_fm: float) -> np.ndarray:
    del R_fm
    return np.ones_like(r, dtype=float)


def u_alpha_woods_saxon(
    r: np.ndarray,
    R_alpha_fm: float,
    a_ws_fm: float = A_WS_DEFAULT_FM,
) -> np.ndarray:
    """Woods-Saxon cluster reduced radial trial: u = r / (1 + exp((r-R_a)/a))."""
    return r / (1.0 + np.exp((r - R_alpha_fm) / a_ws_fm))


def u_alpha_ws_coulomb_tail(
    r: np.ndarray,
    R_alpha_fm: float,
    a_ws_fm: float = A_WS_DEFAULT_FM,
    kappa_fm_inv: float = KAPPA_TAIL_DEFAULT,
) -> np.ndarray:
    """
    Woods-Saxon interior glued to an exponential Coulomb-like tail.

    Match radius R_m = R_alpha + 2 a_WS.  For r <= R_m use WS; for r > R_m
    use C * exp(-kappa (r - R_m)) * R_m / r * u_WS(R_m)/R_m scaled so that
    value is continuous at R_m.  Slope continuity is approximate (RC1:
    phenomenological matching, not a full R-matrix eigenmode).
    """
    R_m = R_alpha_fm + 2.0 * a_ws_fm
    u_ws = u_alpha_woods_saxon(r, R_alpha_fm, a_ws_fm)
    u_m = float(R_m / (1.0 + math.exp((R_m - R_alpha_fm) / a_ws_fm)))
    # Tail: same value at R_m, exponential decay with soft 1/r envelope.
    tail = u_m * np.exp(-kappa_fm_inv * (r - R_m)) * (R_m / np.maximum(r, R_m))
    return np.where(r <= R_m, u_ws, tail)


def select_alpha(
    kind: AlphaKind,
    r: np.ndarray,
    r0_fm: float,
    a_ws_fm: float,
    kappa_fm_inv: float,
) -> tuple[np.ndarray, dict[str, float]]:
    R_alpha = a_alpha_fm(r0_fm)  # r0 * 4^(1/3); same length scale as HO a_alpha
    meta = {
        "R_alpha_fm": R_alpha,
        "a_ws_fm": a_ws_fm,
        "kappa_fm_inv": kappa_fm_inv,
        "a_gaussian_fm": R_alpha,
    }
    if kind == "woods_saxon":
        return u_alpha_woods_saxon(r, R_alpha, a_ws_fm), meta
    if kind == "ws_coulomb_tail":
        return u_alpha_ws_coulomb_tail(r, R_alpha, a_ws_fm, kappa_fm_inv), meta
    if kind == "gaussian":
        return u_alpha_gaussian(r, R_alpha), meta
    raise ValueError(f"unknown alpha kind: {kind}")


def select_weight(kind: MeasureKind) -> Callable[[np.ndarray, float], np.ndarray]:
    if kind == "throat_ads":
        return throat_weight_ads
    if kind == "flat":
        return flat_weight
    raise ValueError(f"unknown measure kind: {kind}")


def overlap_P_weighted(
    R_fm: float,
    *,
    alpha_kind: AlphaKind = "woods_saxon",
    measure_kind: MeasureKind = "throat_ads",
    r0_fm: float = R0_DEFAULT_FM,
    a_ws_fm: float = A_WS_DEFAULT_FM,
    kappa_fm_inv: float = KAPPA_TAIL_DEFAULT,
    n_grid: int = N_GRID,
) -> tuple[float, dict[str, float]]:
    if R_fm <= 0.0:
        raise ValueError(f"R_fm must be positive, got {R_fm}")
    r = np.linspace(0.0, R_fm, n_grid)
    ui = u_in(r, R_fm)
    ua, meta = select_alpha(alpha_kind, r, r0_fm, a_ws_fm, kappa_fm_inv)
    w = select_weight(measure_kind)(r, R_fm)
    num = simpson(ui * ua * w, x=r)
    den_in = simpson(ui * ui * w, x=r)
    den_a = simpson(ua * ua * w, x=r)
    if den_in <= 0.0 or den_a <= 0.0:
        raise RuntimeError("non-positive weighted mode norms")
    P = float((num * num) / (den_in * den_a))
    meta = {**meta, "num": float(num), "den_in": float(den_in), "den_a": float(den_a)}
    return P, meta


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ModelSpec:
    label: str
    alpha_kind: AlphaKind
    measure_kind: MeasureKind
    primary: bool = False


MODELS: tuple[ModelSpec, ...] = (
    ModelSpec("throat_ws", "woods_saxon", "throat_ads", primary=True),
    ModelSpec("throat_ws_coulomb", "ws_coulomb_tail", "throat_ads"),
    ModelSpec("throat_gaussian", "gaussian", "throat_ads"),
    ModelSpec("flat_ws", "woods_saxon", "flat"),
    ModelSpec("flat_gaussian", "gaussian", "flat"),  # reproduces baseline proxy
)


def evaluate_isotope_model(
    row: IsotopeRow,
    spec: ModelSpec,
    *,
    r0_fm: float,
    a_ws_fm: float,
    kappa_fm_inv: float,
    n_grid: int,
) -> dict[str, Any]:
    P_raw, meta = overlap_P_weighted(
        row.R_fm,
        alpha_kind=spec.alpha_kind,
        measure_kind=spec.measure_kind,
        r0_fm=r0_fm,
        a_ws_fm=a_ws_fm,
        kappa_fm_inv=kappa_fm_inv,
        n_grid=n_grid,
    )
    log10_P_model = math.log10(P_raw) if P_raw > 0.0 else float("-inf")
    P_ext = row.t12_Gamow_s / row.t12_meas_s
    return {
        "isotope": row.name,
        "Q_alpha_MeV": row.Q_alpha_MeV,
        "R_fm": row.R_fm,
        "b_fm": row.b_fm,
        "W_ana": row.W_ana,
        "t12_Gamow_s": row.t12_Gamow_s,
        "t12_meas_s": row.t12_meas_s,
        "model_label": spec.label,
        "alpha_kind": spec.alpha_kind,
        "measure_kind": spec.measure_kind,
        "P_model": P_raw,
        "log10_P_model": log10_P_model,
        "log10_P_extracted": row.log10_P_extracted,
        "residual_raw": log10_P_model - row.log10_P_extracted,
        "P_ext_halflife": P_ext,
        "alpha_meta": meta,
    }


def summarize_model_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
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

    rms_raw = float(np.sqrt(np.mean(residuals_raw**2)))
    rms_S = float(np.sqrt(np.mean(residuals_S**2)))
    return {
        "n_isotopes": len(rows),
        "mean_log10_P_model": float(np.mean(log10_model)),
        "std_log10_P_model": float(np.std(log10_model, ddof=1)),
        "mean_log10_P_extracted": float(np.mean(log10_ext)),
        "std_log10_P_extracted": float(np.std(log10_ext, ddof=1)),
        "pearson_r_raw": pearson_r(log10_model, log10_ext),
        "pearson_r_with_S": pearson_r(log10_model_S, log10_ext),
        "mean_residual_raw": float(np.mean(residuals_raw)),
        "rms_residual_raw": rms_raw,
        "mean_abs_residual_raw": float(np.mean(np.abs(residuals_raw))),
        "best_fit_global_S": S,
        "log10_S": float(math.log10(S)),
        "mean_residual_S": float(np.mean(residuals_S)),
        "rms_residual_S": rms_S,
        "mean_abs_residual_S": float(np.mean(np.abs(residuals_S))),
        "S_improves_rms": bool(rms_S < rms_raw),
        "rms_improvement": float(rms_raw - rms_S),
    }


def run_analysis(
    *,
    r0_fm: float = R0_DEFAULT_FM,
    a_ws_fm: float = A_WS_DEFAULT_FM,
    kappa_fm_inv: float = KAPPA_TAIL_DEFAULT,
    n_grid: int = N_GRID,
) -> dict[str, Any]:
    models_out: dict[str, Any] = {}
    primary_label = next(m.label for m in MODELS if m.primary)

    for spec in MODELS:
        rows = [
            evaluate_isotope_model(
                iso,
                spec,
                r0_fm=r0_fm,
                a_ws_fm=a_ws_fm,
                kappa_fm_inv=kappa_fm_inv,
                n_grid=n_grid,
            )
            for iso in ISOTOPES
        ]
        summary = summarize_model_rows(rows)
        summary.update(
            {
                "r0_fm": r0_fm,
                "a_ws_fm": a_ws_fm,
                "kappa_fm_inv": kappa_fm_inv,
                "n_grid": n_grid,
                "a_alpha_fm": a_alpha_fm(r0_fm),
                "primary": spec.primary,
                "scope_note": (
                    "Weighted standing-wave overlap on the confined throat [0,R] "
                    "with AdS-like measure w=R/r (companion metric √g_rr) and/or "
                    "flat dr; alpha trial is Woods-Saxon (primary) or Gaussian "
                    "comparison. Not a first-principles many-body uniqueness claim."
                ),
            }
        )
        models_out[spec.label] = {
            "spec": {
                "label": spec.label,
                "alpha_kind": spec.alpha_kind,
                "measure_kind": spec.measure_kind,
                "primary": spec.primary,
            },
            "summary": summary,
            "isotopes": rows,
        }

    # Flat-proxy vs primary throat/WS deltas (mean log10 and RMS after S).
    flat = models_out["flat_gaussian"]["summary"]
    primary = models_out[primary_label]["summary"]
    comparison = {
        "primary_model": primary_label,
        "baseline_model": "flat_gaussian",
        "delta_mean_log10_P_model": float(
            primary["mean_log10_P_model"] - flat["mean_log10_P_model"]
        ),
        "delta_pearson_r": float(primary["pearson_r_raw"] - flat["pearson_r_raw"]),
        "delta_rms_raw": float(primary["rms_residual_raw"] - flat["rms_residual_raw"]),
        "delta_rms_S": float(primary["rms_residual_S"] - flat["rms_residual_S"]),
        "delta_log10_S": float(primary["log10_S"] - flat["log10_S"]),
        "flat_gaussian_mean_log10_P": flat["mean_log10_P_model"],
        "throat_ws_mean_log10_P": primary["mean_log10_P_model"],
        "flat_gaussian_pearson_r": flat["pearson_r_raw"],
        "throat_ws_pearson_r": primary["pearson_r_raw"],
        "flat_gaussian_rms_S": flat["rms_residual_S"],
        "throat_ws_rms_S": primary["rms_residual_S"],
        "flat_gaussian_S": flat["best_fit_global_S"],
        "throat_ws_S": primary["best_fit_global_S"],
    }

    return {
        "model_family": {
            "u_in": "r * j_0(k r), k=pi/R (ell=0 first zero)",
            "throat_weight": (
                "w(r)=R/r on (0,R] from companion AdS-like metric "
                "ds^2=(R^2/r^2)dr^2+... (√g_rr=R/r); flat w=1 for comparison"
            ),
            "u_alpha_primary": (
                f"Woods-Saxon: r/(1+exp((r-R_alpha)/a_WS)), "
                f"R_alpha=r0*4^(1/3), a_WS={a_ws_fm} fm"
            ),
            "u_alpha_ws_coulomb": (
                "WS for r<=R_alpha+2 a_WS; exponential*R_m/r tail beyond, "
                f"kappa={kappa_fm_inv} fm^-1 (phenomenological match)"
            ),
            "u_alpha_gaussian": "r * exp(-r^2/(2 a_alpha^2)), a_alpha=r0*4^(1/3)",
            "P_definition": (
                "|∫ u_in u_alpha w dr|^2 / (∫ u_in^2 w dr · ∫ u_alpha^2 w dr) "
                "on [0,R]; optional P_S = S * P_model"
            ),
            "domain_choice": (
                "Overlap support is the confined interior [0,R] where u_in is "
                "defined. Barrier [R,b] remains the Gamow domain in the nuclear "
                "companion; it is not used as overlap support for the Dirichlet mode."
            ),
            "P_extracted_definition": "P_ext = t_Gamow / t_meas (consistency check)",
        },
        "parameters": {
            "r0_fm": r0_fm,
            "a_ws_fm": a_ws_fm,
            "kappa_fm_inv": kappa_fm_inv,
            "n_grid": n_grid,
            "a_alpha_fm": a_alpha_fm(r0_fm),
        },
        "primary_model": primary_label,
        "comparison_flat_vs_throat_ws": comparison,
        "models": models_out,
        "table_source": (
            "Flag_Condensate_Nuclear_Decay.tex table (14 alpha emitters)"
        ),
        "baseline_proxy_ref": (
            "flag_condensate_palpha_overlap.tex / docs/palpha_overlap_results.json"
        ),
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def format_markdown_table(result: dict[str, Any]) -> str:
    primary = result["primary_model"]
    block = result["models"][primary]
    lines = [
        f"## Primary model: `{primary}` "
        f"(alpha={block['spec']['alpha_kind']}, "
        f"measure={block['spec']['measure_kind']})",
        "",
        "| Isotope | R (fm) | P_model | log10 P_model | log10 P_ext | "
        "resid (raw) | log10 P_model·S | resid (S) |",
        "|---------|-------:|--------:|--------------:|------------:|"
        "------------:|----------------:|----------:|",
    ]
    for r in block["isotopes"]:
        lines.append(
            f"| {r['isotope']} | {r['R_fm']:.2f} | {r['P_model']:.6e} | "
            f"{r['log10_P_model']:+.4f} | {r['log10_P_extracted']:+.2f} | "
            f"{r['residual_raw']:+.4f} | {r['log10_P_model_S']:+.4f} | "
            f"{r['residual_S']:+.4f} |"
        )
    s = block["summary"]
    lines.extend(
        [
            "",
            "### Primary summary",
            f"- mean log10 P_model = {s['mean_log10_P_model']:+.4f} "
            f"(std {s['std_log10_P_model']:.4f})",
            f"- mean log10 P_extracted = {s['mean_log10_P_extracted']:+.4f} "
            f"(std {s['std_log10_P_extracted']:.4f})",
            f"- Pearson r = {s['pearson_r_raw']:+.4f}",
            f"- RMS residual (S=1) = {s['rms_residual_raw']:.4f}",
            f"- best-fit global S = {s['best_fit_global_S']:.6e} "
            f"(log10 S = {s['log10_S']:+.4f})",
            f"- RMS residual (with S) = {s['rms_residual_S']:.4f} "
            f"(improvement {s['rms_improvement']:+.4f})",
            "",
            "### All-model summary",
            "| Model | mean log10 P | Pearson r | RMS raw | S | RMS(S) |",
            "|-------|-------------:|----------:|--------:|--:|-------:|",
        ]
    )
    for label, m in result["models"].items():
        sm = m["summary"]
        marker = " **" if m["spec"]["primary"] else ""
        lines.append(
            f"| {label}{marker} | {sm['mean_log10_P_model']:+.4f} | "
            f"{sm['pearson_r_raw']:+.4f} | {sm['rms_residual_raw']:.4f} | "
            f"{sm['best_fit_global_S']:.4e} | {sm['rms_residual_S']:.4f} |"
        )
    c = result["comparison_flat_vs_throat_ws"]
    lines.extend(
        [
            "",
            "### Flat Gaussian proxy vs throat+WS",
            f"- Δ mean log10 P = {c['delta_mean_log10_P_model']:+.4f}",
            f"- Δ Pearson r = {c['delta_pearson_r']:+.4f}",
            f"- Δ RMS (raw) = {c['delta_rms_raw']:+.4f}",
            f"- Δ RMS (with S) = {c['delta_rms_S']:+.4f}",
            f"- flat S = {c['flat_gaussian_S']:.6e}, "
            f"throat+WS S = {c['throat_ws_S']:.6e}",
            "",
            f"_Scope:_ {s['scope_note']}",
        ]
    )
    return "\n".join(lines)


def write_json(result: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    def _default(obj: Any) -> Any:
        if isinstance(obj, (np.floating, np.integer)):
            return obj.item()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    with path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=_default)
        f.write("\n")


def main() -> int:
    result = run_analysis(
        r0_fm=R0_DEFAULT_FM,
        a_ws_fm=A_WS_DEFAULT_FM,
        kappa_fm_inv=KAPPA_TAIL_DEFAULT,
        n_grid=N_GRID,
    )
    out_path = REPO_DOCS
    write_json(result, out_path)

    log_dir = out_path.parent / "palpha_overlap_throat_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report = format_markdown_table(result)
    header = (
        f"# P_α throat-geometry / Woods-Saxon overlap results\n"
        f"# utc={stamp}  r0_fm={R0_DEFAULT_FM}  a_ws_fm={A_WS_DEFAULT_FM}  "
        f"n_grid={N_GRID}\n\n"
    )
    log_body = header + report + f"\n\nJSON written: {out_path}\n"
    log_path = log_dir / f"run_{stamp}.log"
    log_path.write_text(log_body, encoding="utf-8")

    print(log_body)
    print(f"Log written: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
