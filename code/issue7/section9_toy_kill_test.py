#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Issue #7: Section 9 toy kill test (gap -> cone leakage proxy).

This script does not claim a theorem. It builds a finite 1D transverse-field
Ising chain and checks whether larger spectral gap correlates with:
  (a) shorter static clustering length, and
  (b) lower outside-cone commutator leakage.

If these trends fail, the proposed dependency chain is not supported even in
this toy setting.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def kron_n(ops: list[np.ndarray]) -> np.ndarray:
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def local_op(site: int, n_sites: int, op: np.ndarray, ident: np.ndarray) -> np.ndarray:
    ops = [ident] * n_sites
    ops[site] = op
    return kron_n(ops)


def tfim_hamiltonian(n_sites: int, j: float, h: float) -> np.ndarray:
    ident = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    dim = 2**n_sites
    ham = np.zeros((dim, dim), dtype=complex)
    for i in range(n_sites - 1):
        ham -= j * local_op(i, n_sites, sz, ident) @ local_op(i + 1, n_sites, sz, ident)
    for i in range(n_sites):
        ham -= h * local_op(i, n_sites, sx, ident)
    return ham


def heisenberg_evolve_operator(
    op: np.ndarray, eigvals: np.ndarray, eigvecs: np.ndarray, t: float
) -> np.ndarray:
    # O(t)_ij (in eigenbasis) = exp(i Ei t) * O_ij * exp(-i Ej t)
    op_eig = eigvecs.conj().T @ op @ eigvecs
    phase = np.exp(1j * eigvals * t)
    evolved_eig = phase[:, None] * op_eig * phase.conj()[None, :]
    return eigvecs @ evolved_eig @ eigvecs.conj().T


def ground_state_correlations(
    gs: np.ndarray, z_ops: list[np.ndarray], r_values: list[int]
) -> list[float]:
    z0 = z_ops[0]
    exp_z0 = float(np.real(gs.conj().T @ (z0 @ gs)))
    corr = []
    for r in r_values:
        zr = z_ops[r]
        exp_zr = float(np.real(gs.conj().T @ (zr @ gs)))
        exp_zz = float(np.real(gs.conj().T @ ((z0 @ zr) @ gs)))
        conn = abs(exp_zz - exp_z0 * exp_zr)
        corr.append(conn)
    return corr


def fit_clustering_length(r_values: list[int], corr: list[float]) -> float:
    xs = []
    ys = []
    for r, c in zip(r_values, corr):
        if c > 1e-12:
            xs.append(float(r))
            ys.append(math.log(c))
    if len(xs) < 2:
        return float("nan")
    slope, _intercept = np.polyfit(xs, ys, 1)
    if slope >= 0:
        return float("inf")
    return -1.0 / slope


def estimate_velocity(r_values: list[int], t_values: np.ndarray, leak_grid: np.ndarray) -> float:
    threshold = 1e-3
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
    slope, _intercept = np.polyfit(cross_t, cross_r, 1)
    return max(0.0, float(slope))


@dataclass
class ToyResult:
    h: float
    gap: float
    xi: float
    v_est: float
    outside_max: float


def run_one(n_sites: int, j: float, h: float, t_values: np.ndarray) -> ToyResult:
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

    v_est = estimate_velocity(r_values, t_values, leak_grid)
    if not np.isfinite(v_est):
        outside_max = float("nan")
    else:
        outside_vals: list[float] = []
        margin = 0.5
        for ri, r in enumerate(r_values):
            for ti, t in enumerate(t_values):
                if float(r) > (v_est * float(t) + margin):
                    outside_vals.append(leak_grid[ri, ti])
        outside_max = float(max(outside_vals)) if outside_vals else float("nan")

    return ToyResult(h=h, gap=gap, xi=xi, v_est=v_est, outside_max=outside_max)


def corrcoef_safe(xs: list[float], ys: list[float]) -> float:
    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    good = np.isfinite(x) & np.isfinite(y)
    if np.count_nonzero(good) < 2:
        return float("nan")
    xg = x[good]
    yg = y[good]
    if np.std(xg) < 1e-14 or np.std(yg) < 1e-14:
        return float("nan")
    return float(np.corrcoef(xg, yg)[0, 1])


def main() -> None:
    n_sites = 7
    j = 1.0
    h_values = [0.5, 0.8, 1.2, 1.5, 2.0]
    t_values = np.linspace(0.0, 2.6, 55)
    results = [run_one(n_sites, j, h, t_values) for h in h_values]

    print("Section 9 toy kill test")
    print("Model: 1D TFIM, open chain, N=7")
    print("Columns: h, gap, xi (cluster length), v_est, outside_cone_max")
    for row in results:
        print(
            f"h={row.h:>4.1f}  gap={row.gap:>8.5f}  xi={row.xi:>8.4f}  "
            f"v={row.v_est:>7.4f}  leak_out_max={row.outside_max:>10.6e}"
        )

    gaps = [r.gap for r in results]
    xis = [r.xi for r in results]
    leak = [r.outside_max for r in results]
    corr_gap_xi = corrcoef_safe(gaps, xis)
    corr_gap_leak = corrcoef_safe(gaps, leak)

    print("\nTrend checks")
    print(f"corr(gap, xi)         = {corr_gap_xi:+.4f}  (expect negative)")
    print(f"corr(gap, leak_out)   = {corr_gap_leak:+.4f}  (expect negative)")

    chain_supported = (
        np.isfinite(corr_gap_xi)
        and np.isfinite(corr_gap_leak)
        and corr_gap_xi < -0.2
        and corr_gap_leak < -0.2
    )
    if chain_supported:
        print("RESULT: toy data supports the chain direction.")
    else:
        print("RESULT: toy data does not support a robust monotone chain.")


if __name__ == "__main__":
    main()
