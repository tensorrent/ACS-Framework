#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Issue #7 third-model kill pass: long-range Ising.

Purpose:
  Extend the Section 9 toy dependency-chain diagnostics to a model family
  with power-law couplings, where strict Lieb-Robinson cones are known to
  weaken. This is the hardest tested regime for the cone-sharpness proxy.

Model:
  H = -sum_{i<j} J / |i-j|^alpha  Z_i Z_j  -  h sum_i X_i

Decision rule (same as cross-model pass):
  Support requires corr(gap, xi) < -0.2 AND both leakage-proxy correlations
  (max, mean) < -0.2.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from cross_model_kill_pass import evaluate_point
from section9_toy_kill_test import corrcoef_safe, local_op


def long_range_ising_hamiltonian(
    n_sites: int, j: float, alpha: float, h: float
) -> np.ndarray:
    ident = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    dim = 2**n_sites
    ham = np.zeros((dim, dim), dtype=complex)
    for i in range(n_sites):
        for k in range(i + 1, n_sites):
            coupling = j / float(k - i) ** alpha
            ham -= coupling * local_op(i, n_sites, sz, ident) @ local_op(
                k, n_sites, sz, ident
            )
    for i in range(n_sites):
        ham -= h * local_op(i, n_sites, sx, ident)
    return ham


def run_long_range_sweep(alpha: float) -> dict[str, object]:
    n_sites_list = [6, 7]
    h_values = np.linspace(0.5, 2.3, 10)
    thresholds = [1e-2, 3e-3, 1e-3]
    t_values = np.linspace(0.0, 2.8, 70)
    cases = []
    support = 0
    total = 0

    for n_sites in n_sites_list:
        for threshold in thresholds:
            rows = []
            for h in h_values:
                ham = long_range_ising_hamiltonian(
                    n_sites=n_sites, j=1.0, alpha=alpha, h=float(h)
                )
                rows.append(evaluate_point(ham, n_sites, float(h), t_values, threshold))

            gaps = [r.gap for r in rows]
            xis = [r.xi for r in rows]
            leak_max = [r.leak_out_max for r in rows]
            leak_mean = [r.leak_out_mean for r in rows]
            c_gap_xi = corrcoef_safe(gaps, xis)
            c_gap_lmax = corrcoef_safe(gaps, leak_max)
            c_gap_lmean = corrcoef_safe(gaps, leak_mean)

            chain_supported = (
                np.isfinite(c_gap_xi)
                and np.isfinite(c_gap_lmax)
                and np.isfinite(c_gap_lmean)
                and c_gap_xi < -0.2
                and c_gap_lmax < -0.2
                and c_gap_lmean < -0.2
            )
            total += 1
            support += int(chain_supported)
            cases.append(
                {
                    "n_sites": n_sites,
                    "threshold": threshold,
                    "corr_gap_xi": c_gap_xi,
                    "corr_gap_leak_max": c_gap_lmax,
                    "corr_gap_leak_mean": c_gap_lmean,
                    "supports_chain": bool(chain_supported),
                }
            )

    return {
        "model": "long_range_ising",
        "alpha": alpha,
        "settings": {
            "n_sites": n_sites_list,
            "h_values": [float(x) for x in h_values],
            "thresholds": thresholds,
            "t_points": int(len(t_values)),
            "t_max": float(t_values[-1]),
            "j": 1.0,
        },
        "summary": {
            "support_cases": support,
            "total_cases": total,
            "support_rate": support / total if total else float("nan"),
        },
        "cases": cases,
    }


def main() -> None:
    alphas = [3.0, 2.0]
    sweeps = {f"alpha_{a:g}": run_long_range_sweep(a) for a in alphas}
    combined_support = sum(s["summary"]["support_cases"] for s in sweeps.values())
    combined_total = sum(s["summary"]["total_cases"] for s in sweeps.values())
    result = {
        "sweeps": sweeps,
        "meta": {
            "combined_support_cases": combined_support,
            "combined_total_cases": combined_total,
        },
    }

    out_path = (
        Path(__file__).resolve().parents[2] / "docs" / "issue7_long_range_results.json"
    )
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("Issue #7 long-range kill pass complete")
    for key, sweep in sweeps.items():
        print(f"{key} support rate: {sweep['summary']['support_rate']:.4f}")
    print(f"Combined support:  {combined_support}/{combined_total}")
    print(f"artifact: {out_path}")


if __name__ == "__main__":
    main()
