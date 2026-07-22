#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Issue #7 cross-model exhaustion pass.

Purpose:
  Stress-test the Section 9 toy dependency chain on multiple lattice models
  and multiple outside-cone leakage summaries.

Models:
  - TFIM:   H = -J sum Z_i Z_{i+1} - h sum X_i
  - XXZ+h:  H = Jxy sum (X_iX_{i+1}+Y_iY_{i+1}) + Jz sum Z_iZ_{i+1} - h sum X_i
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from section9_toy_kill_test import (
    corrcoef_safe,
    fit_clustering_length,
    ground_state_correlations,
    heisenberg_evolve_operator,
    local_op,
    tfim_hamiltonian,
)


def xxz_hamiltonian(n_sites: int, jxy: float, jz: float, h: float) -> np.ndarray:
    ident = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    dim = 2**n_sites
    ham = np.zeros((dim, dim), dtype=complex)
    for i in range(n_sites - 1):
        ham += jxy * local_op(i, n_sites, sx, ident) @ local_op(i + 1, n_sites, sx, ident)
        ham += jxy * local_op(i, n_sites, sy, ident) @ local_op(i + 1, n_sites, sy, ident)
        ham += jz * local_op(i, n_sites, sz, ident) @ local_op(i + 1, n_sites, sz, ident)
    for i in range(n_sites):
        ham -= h * local_op(i, n_sites, sx, ident)
    return ham


@dataclass
class PointResult:
    h: float
    gap: float
    xi: float
    v_est: float
    leak_out_max: float
    leak_out_mean: float


def estimate_velocity(
    r_values: list[int], t_values: np.ndarray, leak_grid: np.ndarray, threshold: float
) -> float:
    cross_r = []
    cross_t = []
    for idx, r in enumerate(r_values):
        curve = leak_grid[idx]
        above = np.where(curve > threshold)[0]
        if len(above) == 0:
            continue
        cross_r.append(float(r))
        cross_t.append(float(t_values[int(above[0])]))
    if len(cross_r) < 2:
        return float("nan")
    slope, _ = np.polyfit(cross_t, cross_r, 1)
    return max(0.0, float(slope))


def evaluate_point(
    hamiltonian: np.ndarray, n_sites: int, h: float, t_values: np.ndarray, threshold: float
) -> PointResult:
    ident = np.eye(2, dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    evals, evecs = np.linalg.eigh(hamiltonian)
    gap = float(np.real(evals[1] - evals[0]))
    gs = evecs[:, 0]
    z_ops = [local_op(i, n_sites, sz, ident) for i in range(n_sites)]
    r_values = list(range(1, n_sites))
    corr = ground_state_correlations(gs, z_ops, r_values)
    xi = fit_clustering_length(r_values, corr)

    source = z_ops[0]
    leak_grid = np.zeros((len(r_values), len(t_values)), dtype=float)
    for ti, t in enumerate(t_values):
        source_t = heisenberg_evolve_operator(source, evals, evecs, float(t))
        for ri, r in enumerate(r_values):
            comm = source_t @ z_ops[r] - z_ops[r] @ source_t
            leak_grid[ri, ti] = float(np.linalg.norm(comm, ord=2))

    v_est = estimate_velocity(r_values, t_values, leak_grid, threshold)
    outside_vals = []
    margin = 0.5
    if np.isfinite(v_est):
        for ri, r in enumerate(r_values):
            for ti, t in enumerate(t_values):
                if float(r) > (v_est * float(t) + margin):
                    outside_vals.append(leak_grid[ri, ti])
    leak_out_max = float(max(outside_vals)) if outside_vals else float("nan")
    leak_out_mean = float(np.mean(outside_vals)) if outside_vals else float("nan")
    return PointResult(
        h=h,
        gap=gap,
        xi=xi,
        v_est=v_est,
        leak_out_max=leak_out_max,
        leak_out_mean=leak_out_mean,
    )


def run_model_sweep(model_name: str) -> dict[str, object]:
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
                if model_name == "tfim":
                    ham = tfim_hamiltonian(n_sites=n_sites, j=1.0, h=float(h))
                elif model_name == "xxz":
                    ham = xxz_hamiltonian(n_sites=n_sites, jxy=0.7, jz=1.0, h=float(h))
                else:
                    raise ValueError(f"unknown model: {model_name}")
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
        "model": model_name,
        "settings": {
            "n_sites": n_sites_list,
            "h_values": [float(x) for x in h_values],
            "thresholds": thresholds,
            "t_points": int(len(t_values)),
            "t_max": float(t_values[-1]),
        },
        "summary": {
            "support_cases": support,
            "total_cases": total,
            "support_rate": support / total if total else float("nan"),
        },
        "cases": cases,
    }


def main() -> None:
    tfim = run_model_sweep("tfim")
    xxz = run_model_sweep("xxz")
    combined = {
        "tfim": tfim,
        "xxz": xxz,
        "meta": {
            "combined_support_cases": tfim["summary"]["support_cases"] + xxz["summary"]["support_cases"],
            "combined_total_cases": tfim["summary"]["total_cases"] + xxz["summary"]["total_cases"],
        },
    }

    out_path = (
        Path(__file__).resolve().parents[2] / "docs" / "issue7_cross_model_results.json"
    )
    out_path.write_text(json.dumps(combined, indent=2), encoding="utf-8")

    total_support = combined["meta"]["combined_support_cases"]
    total_cases = combined["meta"]["combined_total_cases"]
    print("Issue #7 cross-model kill pass complete")
    print(f"TFIM support rate: {tfim['summary']['support_rate']:.4f}")
    print(f"XXZ support rate:  {xxz['summary']['support_rate']:.4f}")
    print(f"Combined support:  {total_support}/{total_cases}")
    print(f"artifact: {out_path}")


if __name__ == "__main__":
    main()
