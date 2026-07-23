#!/usr/bin/env python3
"""
Channel C — Gamow / outgoing Coulomb boundary on [0, b].

Extends the Dirichlet box eigenmode (Channel B) by:
  - integrating the WS+Coulomb radial problem on [0, b] (b = outer turning point)
  - imposing u(0) = 0
  - Robin outgoing match at r = b from WKB slope in the exterior allowed region

RC1: quasistationary outgoing surrogate — not a full complex Gamow pole search.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy.integrate import simpson
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

from palpha_overlap import IsotopeRow, N_GRID, R0_DEFAULT_FM, u_in
from palpha_overlap_throat import throat_weight_ads

HBARC_MEV_FM = 197.3269718
E2_MEV_FM = 1.439964547
M_N_MEV = 931.494
N_EIGEN_GRID = 800
V0_BRACKET_MEV = (1.0, 250.0)
A_WS_DEFAULT_FM = 0.55

ELEMENT_Z: dict[str, int] = {
    "Po": 84,
    "Rn": 86,
    "Ra": 88,
    "Th": 90,
    "U": 92,
    "Pu": 94,
    "Cm": 96,
    "Ac": 89,
    "Pa": 91,
    "Am": 95,
    "Cf": 98,
}


@dataclass(frozen=True)
class NuclearIds:
    name: str
    A: int
    Z: int
    A_d: int
    Z_d: int
    Z_alpha: int = 2
    A_alpha: int = 4


_NAME_RE = re.compile(r"^(\d+)([A-Za-z]+)$")


def parse_nuclear_ids(name: str) -> NuclearIds:
    m = _NAME_RE.match(name)
    if not m:
        raise ValueError(f"cannot parse isotope name: {name}")
    A = int(m.group(1))
    el = m.group(2)
    if el not in ELEMENT_Z:
        raise ValueError(f"unknown element symbol in isotope table: {el}")
    Z = ELEMENT_Z[el]
    return NuclearIds(name=name, A=A, Z=Z, A_d=A - 4, Z_d=Z - 2)


def reduced_mass_MeV(A_d: int) -> float:
    m_a = 4.0 * M_N_MEV
    m_d = float(A_d) * M_N_MEV
    return (m_a * m_d) / (m_a + m_d)


def hbar2_over_2mu(A_d: int) -> float:
    mu = reduced_mass_MeV(A_d)
    return (HBARC_MEV_FM * HBARC_MEV_FM) / (2.0 * mu)


def V_woods_saxon(
    r: np.ndarray,
    V0_MeV: float,
    R_ws_fm: float,
    a_ws_fm: float,
) -> np.ndarray:
    return -V0_MeV / (1.0 + np.exp((r - R_ws_fm) / a_ws_fm))


def V_coulomb(
    r: np.ndarray,
    Z1: int,
    Z2: int,
    R_c_fm: float,
) -> np.ndarray:
    pref = Z1 * Z2 * E2_MEV_FM
    vc = np.empty_like(r, dtype=float)
    inside = r < R_c_fm
    vc[inside] = (pref / (2.0 * R_c_fm)) * (3.0 - (r[inside] / R_c_fm) ** 2)
    outside = ~inside
    vc[outside] = pref / np.maximum(r[outside], R_c_fm)
    if r.size and r[0] == 0.0:
        vc[0] = (pref / (2.0 * R_c_fm)) * 3.0
    return vc


def exterior_wkb_log_deriv(Q_MeV: float, Z_d: int, b_fm: float, mu_MeV: float) -> float:
    """
    Outgoing WKB log-derivative at r=b matched from the allowed side (r > b).

    For r = b + delta, V(r) < Q and k = sqrt(2 mu (Q - V) / hbar^2).
    Robin: u'(b)/u(b) ≈ k (outgoing increasing phase in real surrogate).
    """
    delta = max(0.05, 0.002 * b_fm)
    r_out = b_fm + delta
    v_out = 2.0 * Z_d * E2_MEV_FM / r_out
    k_sq = 2.0 * mu_MeV * max(Q_MeV - v_out, 1e-12) / (HBARC_MEV_FM**2)
    return math.sqrt(k_sq)


def eigen_energy_and_mode_on_b(
    row: IsotopeRow,
    ids: NuclearIds,
    V0_MeV: float,
    *,
    r0_fm: float,
    a_ws_fm: float,
    n_interior: int,
) -> tuple[float, np.ndarray, np.ndarray, dict[str, float]]:
    """FD eigenproblem on (0, b) with Dirichlet at 0 and Robin at b."""
    b_fm = row.b_fm
    if b_fm <= 0.0:
        raise ValueError("b_fm must be positive")
    h = b_fm / (n_interior + 1)
    r = h * np.arange(1, n_interior + 1, dtype=float)
    R_ws = r0_fm * (float(ids.A_d) ** (1.0 / 3.0))
    R_c = R_ws
    V = V_woods_saxon(r, V0_MeV, R_ws, a_ws_fm) + V_coulomb(r, 2, ids.Z_d, R_c)
    coeff = hbar2_over_2mu(ids.A_d)
    diag = (2.0 * coeff / (h * h)) + V
    off = np.full(n_interior - 1, -coeff / (h * h), dtype=float)

    # Robin at r=b: u_N' = alpha_out * u_N  =>  (u_N - u_{N-1})/h = alpha * u_N
    alpha_out = exterior_wkb_log_deriv(row.Q_alpha_MeV, ids.Z_d, b_fm, reduced_mass_MeV(ids.A_d))
    diag[-1] += coeff * alpha_out / h

    evals, evecs = eigh_tridiagonal(diag, off, select="i", select_range=(0, 0))
    E0 = float(evals[0])
    u_int = evecs[:, 0].astype(float)
    if u_int[0] < 0.0:
        u_int = -u_int
    r_full = np.concatenate(([0.0], r, [b_fm]))
    u_full = np.concatenate(([0.0], u_int, [u_int[-1] * (1.0 + alpha_out * h)]))
    norm = simpson(u_full * u_full, x=r_full)
    if norm > 0.0:
        u_full = u_full / math.sqrt(norm)
    meta = {
        "V0_MeV": float(V0_MeV),
        "E0_MeV": E0,
        "R_ws_fm": float(R_ws),
        "R_c_fm": float(R_c),
        "b_fm": float(b_fm),
        "h_fm": float(h),
        "n_interior": float(n_interior),
        "alpha_out_fm_inv": float(alpha_out),
        "bc": (
            "u(0)=0; Robin outgoing WKB at r=b on [0,b] "
            "(exterior allowed Coulomb slope)"
        ),
        "potential": "V_WS(V0,R_ws=r0 A_d^{1/3},a)+V_Coulomb(Z_alpha,Z_d,R_c=R_ws)",
        "domain": "[0,b] with b = Coulomb turning point",
    }
    return E0, r_full, u_full, meta


def find_V0_for_Q_gamow(
    row: IsotopeRow,
    ids: NuclearIds,
    *,
    r0_fm: float,
    a_ws_fm: float,
    n_interior: int = N_EIGEN_GRID,
    bracket: tuple[float, float] = V0_BRACKET_MEV,
) -> tuple[float, float, np.ndarray, np.ndarray, dict[str, float]]:
    Q = row.Q_alpha_MeV

    def f(V0: float) -> float:
        E0, _, _, _ = eigen_energy_and_mode_on_b(
            row, ids, V0, r0_fm=r0_fm, a_ws_fm=a_ws_fm, n_interior=n_interior
        )
        return E0 - Q

    lo, hi = bracket
    f_lo, f_hi = f(lo), f(hi)
    if f_lo * f_hi > 0.0:
        for hi_try in (300.0, 400.0, 600.0, 800.0):
            f_hi = f(hi_try)
            if f_lo * f_hi <= 0.0:
                hi = hi_try
                break
        else:
            grid = np.linspace(lo, hi_try, 48)
            vals = [abs(f(float(v))) for v in grid]
            V0 = float(grid[int(np.argmin(vals))])
            E0, r, u, meta = eigen_energy_and_mode_on_b(
                row, ids, V0, r0_fm=r0_fm, a_ws_fm=a_ws_fm, n_interior=n_interior
            )
            meta = {**meta, "V0_fit_status": 0.0, "Q_alpha_MeV": Q, "E0_minus_Q": E0 - Q}
            return V0, E0, r, u, meta

    V0 = float(brentq(f, lo, hi, xtol=1e-6, rtol=1e-6, maxiter=100))
    E0, r, u, meta = eigen_energy_and_mode_on_b(
        row, ids, V0, r0_fm=r0_fm, a_ws_fm=a_ws_fm, n_interior=n_interior
    )
    meta = {**meta, "V0_fit_status": 1.0, "Q_alpha_MeV": Q, "E0_minus_Q": E0 - Q}
    return V0, E0, r, u, meta


def overlap_P_gamow_eigenmode(
    row: IsotopeRow,
    ids: NuclearIds,
    *,
    r0_fm: float = R0_DEFAULT_FM,
    a_ws_fm: float = A_WS_DEFAULT_FM,
    n_overlap: int = N_GRID,
    n_interior: int = N_EIGEN_GRID,
) -> tuple[float, dict[str, Any]]:
    """Throat-weighted overlap on [0,R] with Gamow eigenmode from [0,b]."""
    V0, E0, r_e, u_e, emeta = find_V0_for_Q_gamow(
        row, ids, r0_fm=r0_fm, a_ws_fm=a_ws_fm, n_interior=n_interior
    )
    r = np.linspace(0.0, row.R_fm, n_overlap)
    ua = np.interp(r, r_e, u_e)
    ui = u_in(r, row.R_fm)
    w = throat_weight_ads(r, row.R_fm)
    num = simpson(ui * ua * w, x=r)
    den_in = simpson(ui * ui * w, x=r)
    den_a = simpson(ua * ua * w, x=r)
    if den_in <= 0.0 or den_a <= 0.0:
        raise RuntimeError("non-positive weighted norms in Gamow overlap")
    P = float((num * num) / (den_in * den_a))
    meta = {
        **emeta,
        "num": float(num),
        "den_in": float(den_in),
        "den_a": float(den_a),
    }
    return P, meta


def evaluate_gamow_isotope(
    row: IsotopeRow,
    *,
    r0_fm: float,
    a_ws_fm: float,
    n_overlap: int,
    n_interior: int,
) -> dict[str, Any]:
    ids = parse_nuclear_ids(row.name)
    P_raw, meta = overlap_P_gamow_eigenmode(
        row,
        ids,
        r0_fm=r0_fm,
        a_ws_fm=a_ws_fm,
        n_overlap=n_overlap,
        n_interior=n_interior,
    )
    log10_P_model = math.log10(P_raw) if P_raw > 0.0 else float("-inf")
    return {
        "isotope": row.name,
        "A": ids.A,
        "Z": ids.Z,
        "A_d": ids.A_d,
        "Z_d": ids.Z_d,
        "Q_alpha_MeV": row.Q_alpha_MeV,
        "R_fm": row.R_fm,
        "b_fm": row.b_fm,
        "model_label": "gamow_outgoing_eigenmode",
        "P_model": P_raw,
        "log10_P_model": log10_P_model,
        "log10_P_extracted": row.log10_P_extracted,
        "residual_raw": log10_P_model - row.log10_P_extracted,
        "alpha_meta": meta,
    }
