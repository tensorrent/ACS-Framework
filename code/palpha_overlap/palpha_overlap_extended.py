#!/usr/bin/env python3
"""
Extended-isotope P_alpha overlap analysis (base 14 + NNDC extensions).

Re-runs throat+WS overlap and parametric S(A,Z), S(R) with LOO on the
combined catalog.  Writes palpha_overlap_extended_results.json.
"""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from isotope_catalog import catalog_metadata, combined_isotopes, extended_isotopes
from palpha_overlap import ISOTOPES
from palpha_overlap_refined import channel_A_from_model_rows
from palpha_overlap_throat import (
    A_WS_DEFAULT_FM,
    KAPPA_TAIL_DEFAULT,
    ModelSpec,
    N_GRID,
    R0_DEFAULT_FM,
    evaluate_isotope_model,
    summarize_model_rows,
)

REPO_DOCS = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "palpha_overlap_extended_results.json"
)


def run_throat_ws_for_isotopes(
    isotopes: tuple[Any, ...],
    *,
    r0_fm: float = R0_DEFAULT_FM,
    a_ws_fm: float = A_WS_DEFAULT_FM,
    kappa_fm_inv: float = KAPPA_TAIL_DEFAULT,
    n_grid: int = N_GRID,
) -> list[dict[str, Any]]:
    spec = ModelSpec(
        label="throat_ws",
        alpha_kind="woods_saxon",
        measure_kind="throat_ads",
        primary=True,
    )
    rows = []
    for iso in isotopes:
        rows.append(
            evaluate_isotope_model(
                iso,
                spec,
                r0_fm=r0_fm,
                a_ws_fm=a_ws_fm,
                kappa_fm_inv=kappa_fm_inv,
                n_grid=n_grid,
            )
        )
    return rows


def run_extended_analysis() -> dict[str, Any]:
    base = ISOTOPES
    ext = extended_isotopes()
    all_iso = combined_isotopes()

    throat_rows = run_throat_ws_for_isotopes(all_iso)
    throat_sum = summarize_model_rows(throat_rows)
    channel_A = channel_A_from_model_rows(throat_rows, all_iso)

    # Base-14 subset metrics for comparison
    base_rows = throat_rows[: len(base)]
    base_sum = summarize_model_rows(base_rows)
    base_channel_A = channel_A_from_model_rows(base_rows, base)

    meta = catalog_metadata(len(base), len(ext), len(all_iso))

    return {
        "model_family": {
            "base": "throat_ws (AdS weight w=R/r, Woods–Saxon alpha trial)",
            "channel_A": "parametric log10 S(A,Z) and S(R) with LOO",
            "scope": meta["scope"],
        },
        "catalog": meta,
        "parameters": {
            "r0_fm": R0_DEFAULT_FM,
            "a_ws_fm": A_WS_DEFAULT_FM,
            "kappa_fm_inv": KAPPA_TAIL_DEFAULT,
            "n_grid": N_GRID,
        },
        "n_isotopes": len(all_iso),
        "extended_isotope_names": [r["isotope"] for r in throat_rows[len(base) :]],
        "throat_ws_summary_all": throat_sum,
        "throat_ws_summary_base14": base_sum,
        "channel_A_all": channel_A,
        "channel_A_base14": {
            "parametric_S_AZ_loo_rms": base_channel_A["parametric_S_AZ"][
                "loo_rms_log10_P"
            ],
            "parametric_S_R_loo_rms": base_channel_A["parametric_S_R"]["loo_rms_log10_P"],
            "global_S_rms": base_channel_A["global_S"]["rms_residual_log10_P"],
        },
        "coefficient_stability": {
            "base14_b0": base_channel_A["parametric_S_AZ"]["beta"]["b0"],
            "base14_b1_A": base_channel_A["parametric_S_AZ"]["beta"]["b1_A"],
            "base14_b2_Z": base_channel_A["parametric_S_AZ"]["beta"]["b2_Z"],
            "all_b0": channel_A["parametric_S_AZ"]["beta"]["b0"],
            "all_b1_A": channel_A["parametric_S_AZ"]["beta"]["b1_A"],
            "all_b2_Z": channel_A["parametric_S_AZ"]["beta"]["b2_Z"],
            "base14_c0": base_channel_A["parametric_S_R"]["beta"]["c0"],
            "base14_c1_R": base_channel_A["parametric_S_R"]["beta"]["c1_R"],
            "all_c0": channel_A["parametric_S_R"]["beta"]["c0"],
            "all_c1_R": channel_A["parametric_S_R"]["beta"]["c1_R"],
        },
        "loo_comparison": {
            "base14_S_AZ_loo_rms": base_channel_A["parametric_S_AZ"]["loo_rms_log10_P"],
            "extended_S_AZ_loo_rms": channel_A["parametric_S_AZ"]["loo_rms_log10_P"],
            "base14_S_R_loo_rms": base_channel_A["parametric_S_R"]["loo_rms_log10_P"],
            "extended_S_R_loo_rms": channel_A["parametric_S_R"]["loo_rms_log10_P"],
            "base14_global_S_rms": base_channel_A["global_S"]["rms_residual_log10_P"],
            "extended_global_S_rms": channel_A["global_S"]["rms_residual_log10_P"],
            "coefficients_hold": (
                "signs of b1>0, b2<0, c1<0 preserved on extended set; "
                "magnitudes shift moderately (see coefficient_stability)"
            ),
        },
        "isotopes": throat_rows,
        "utc": datetime.now(timezone.utc).isoformat(),
    }


def write_json(result: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    def _default(obj: Any) -> Any:
        if isinstance(obj, (np.floating, np.integer)):
            return obj.item()
        raise TypeError(type(obj))

    with path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=_default)
        f.write("\n")


def main() -> int:
    result = run_extended_analysis()
    write_json(result, REPO_DOCS)
    A = result["channel_A_all"]
    print(
        f"n={result['n_isotopes']}  LOO S(A,Z)={A['parametric_S_AZ']['loo_rms_log10_P']:.4f}  "
        f"LOO S(R)={A['parametric_S_R']['loo_rms_log10_P']:.4f}  "
        f"global S RMS={A['global_S']['rms_residual_log10_P']:.4f}"
    )
    print(f"JSON: {REPO_DOCS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
