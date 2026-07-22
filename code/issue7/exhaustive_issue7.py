#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Issue #7 exhaustion runner.

Runs:
1) Section 9 toy kill-test sweeps across chain size, field strength, and
   leakage threshold.
2) 4/3 mechanism robustness scans across normalization scales and integer
   lattices.

Outputs:
- JSON artifact under docs/: issue7_exhaustive_results.json
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from mechanism_4over3_test import alpha_density, beta_acs, implied_dimension_from_beta
from section9_toy_kill_test import (
    corrcoef_safe,
    ground_state_correlations,
    heisenberg_evolve_operator,
    fit_clustering_length,
    local_op,
    tfim_hamiltonian,
)


def estimate_velocity_with_threshold(
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


def one_section9_point(
    n_sites: int, j: float, h: float, t_values: np.ndarray, threshold: float
) -> dict[str, float]:
    ident = np.eye(2, dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    hamiltonian = tfim_hamiltonian(n_sites, j, h)
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

    v_est = estimate_velocity_with_threshold(r_values, t_values, leak_grid, threshold)
    margin = 0.5
    outside_vals: list[float] = []
    if np.isfinite(v_est):
        for ri, r in enumerate(r_values):
            for ti, t in enumerate(t_values):
                if float(r) > (v_est * float(t) + margin):
                    outside_vals.append(leak_grid[ri, ti])
    outside_max = float(max(outside_vals)) if outside_vals else float("nan")
    return {
        "h": float(h),
        "gap": gap,
        "xi": float(xi),
        "v_est": float(v_est),
        "outside_max": outside_max,
    }


def run_section9_exhaustive() -> dict[str, object]:
    n_sites_list = [6, 7, 8]
    h_values = np.linspace(0.4, 2.4, 11)
    t_values = np.linspace(0.0, 2.8, 70)
    thresholds = [1e-2, 3e-3, 1e-3, 3e-4]
    j = 1.0

    per_case = []
    support_cases = 0
    total_cases = 0
    for n_sites in n_sites_list:
        for threshold in thresholds:
            rows = [
                one_section9_point(n_sites, j, float(h), t_values, threshold) for h in h_values
            ]
            gaps = [r["gap"] for r in rows]
            xis = [r["xi"] for r in rows]
            leaks = [r["outside_max"] for r in rows]
            corr_gap_xi = corrcoef_safe(gaps, xis)
            corr_gap_leak = corrcoef_safe(gaps, leaks)
            support = (
                np.isfinite(corr_gap_xi)
                and np.isfinite(corr_gap_leak)
                and corr_gap_xi < -0.2
                and corr_gap_leak < -0.2
            )
            total_cases += 1
            support_cases += int(support)
            per_case.append(
                {
                    "n_sites": n_sites,
                    "threshold": threshold,
                    "corr_gap_xi": corr_gap_xi,
                    "corr_gap_outside_leak": corr_gap_leak,
                    "supports_chain": bool(support),
                }
            )
    return {
        "settings": {
            "n_sites": n_sites_list,
            "h_values": [float(x) for x in h_values],
            "t_points": int(len(t_values)),
            "t_max": float(t_values[-1]),
            "thresholds": thresholds,
            "j": j,
        },
        "summary": {
            "support_cases": support_cases,
            "total_cases": total_cases,
            "support_rate": support_cases / total_cases if total_cases else float("nan"),
        },
        "cases": per_case,
    }


def run_4over3_exhaustive() -> dict[str, object]:
    beta0 = 4.0 / 3.0
    scales = np.linspace(0.5, 1.5, 101)
    d_scaled = [implied_dimension_from_beta(float(c * beta0)) for c in scales]
    finite_d = [d for d in d_scaled if math.isfinite(d)]
    finite_spread = max(finite_d) - min(finite_d) if finite_d else float("inf")
    finite_mean = float(np.mean(finite_d)) if finite_d else float("nan")

    dims = range(2, 101)
    nvals = range(2, 101)
    exact_hits: list[tuple[int, int]] = []
    for d in dims:
        a = alpha_density(float(d))
        for n in nvals:
            b = beta_acs(float(n))
            if abs(a - b) < 1e-12:
                exact_hits.append((d, n))
    all_identity_hits = all(n == d + 1 for d, n in exact_hits)

    # Near-hit density under small perturbation alpha_epsilon = 1 + (1+eps)/d
    epsilons = [-0.05, -0.02, 0.0, 0.02, 0.05]
    near_hit_stats = []
    for eps in epsilons:
        near = 0
        total = 0
        for d in dims:
            a_eps = 1.0 + (1.0 + eps) / float(d)
            for n in nvals:
                total += 1
                if abs(a_eps - beta_acs(float(n))) < 5e-3:
                    near += 1
        near_hit_stats.append({"eps": eps, "near_hits": near, "total_pairs": total})

    return {
        "settings": {
            "beta0": beta0,
            "scale_min": float(scales[0]),
            "scale_max": float(scales[-1]),
            "scale_count": int(len(scales)),
            "integer_scan_max": 100,
        },
        "normalization_robustness": {
            "finite_d_mean": finite_mean,
            "finite_d_spread": finite_spread,
            "non_finite_count": int(sum(0 if math.isfinite(d) else 1 for d in d_scaled)),
        },
        "identity_check": {
            "exact_hit_count": len(exact_hits),
            "all_hits_match_n_eq_d_plus_1": bool(all_identity_hits),
            "first_hits": exact_hits[:12],
        },
        "epsilon_near_hit_scan": near_hit_stats,
    }


def main() -> None:
    section9 = run_section9_exhaustive()
    mech = run_4over3_exhaustive()
    result = {"section9_exhaustive": section9, "mechanism_4over3_exhaustive": mech}

    out_path = (
        Path(__file__).resolve().parents[2] / "docs" / "issue7_exhaustive_results.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    support_rate = section9["summary"]["support_rate"]
    spread = mech["normalization_robustness"]["finite_d_spread"]
    all_identity = mech["identity_check"]["all_hits_match_n_eq_d_plus_1"]
    print("Issue #7 exhaustion run complete")
    print(f"section9 support rate: {support_rate:.4f}")
    print(f"4/3 inferred-d spread under scaling: {spread:.6f}")
    print(f"4/3 exact-hit identity only (n=d+1): {all_identity}")
    print(f"artifact: {out_path}")


if __name__ == "__main__":
    main()
