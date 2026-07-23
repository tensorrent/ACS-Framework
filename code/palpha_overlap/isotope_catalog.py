#!/usr/bin/env python3
"""
Alpha-emitter catalog for P_alpha overlap studies.

Base 14: Flag_Condensate_Nuclear_Decay.tex (canonical).
Extended: additional emitters from NNDC / Geiger–Nuttall compilations
(see EXTENDED_SOURCES metadata).

RC1: tabulated Q and half-lives are as-reported public values; R, b, W
are computed with the same geometric protocol as the nuclear-decay note
(calibrated numeric Gamow integral).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy.integrate import quad

from palpha_overlap import ISOTOPES, IsotopeRow, R0_DEFAULT_FM

E2_MEV_FM = 1.439964547
HBARC_MEV_FM = 197.3269718
M_N_MEV = 931.494
LN2 = math.log(2)
C_FM_S = 2.99792458e23
R_SCALE = 1.504  # fm · A^{-1/3}; matches Nuclear Decay table to ~0.3%

# W_num → W_ana calibration from the base-14 table (least-squares scale).
_W_CALIB_SCALE = 0.9325  # mean W_ana / W_num on base 14

EXTENDED_SOURCES = {
    "base_14": "Flag_Condensate_Nuclear_Decay.tex (2026-07-21)",
    "extended": (
        "NNDC / NuDat 2.9 tabulated Q_alpha and half-lives; "
        "R = 1.504 fm·A^{-1/3}; b = 2 Z_d e^2 / Q; "
        "W from calibrated numeric Gamow integral (scale fit to base 14)"
    ),
}


@dataclass(frozen=True)
class ExtendedIsotopeInput:
    """Raw extended-isotope inputs before Gamow column construction."""

    name: str
    A: int
    Z: int
    Q_alpha_MeV: float
    t12_meas_s: float
    source: str


# Additional alpha emitters (public tabulations; half-lives in seconds).
EXTENDED_RAW: tuple[ExtendedIsotopeInput, ...] = (
    ExtendedIsotopeInput("210Po", 210, 84, 5.407, 1.1958e7, "NNDC"),
    ExtendedIsotopeInput("211Po", 211, 84, 7.442, 0.516, "NNDC"),
    ExtendedIsotopeInput("215Po", 215, 84, 6.794, 1.78e-3, "NNDC"),
    ExtendedIsotopeInput("217Po", 217, 84, 6.108, 171.0, "NNDC"),
    ExtendedIsotopeInput("221Rn", 221, 86, 6.265, 235.2, "NNDC"),
    ExtendedIsotopeInput("222Rn", 222, 86, 5.590, 330350.0, "NNDC"),
    ExtendedIsotopeInput("223Ra", 223, 88, 6.054, 987840.0, "NNDC"),
    ExtendedIsotopeInput("225Ac", 225, 89, 5.835, 864000.0, "NNDC"),
    ExtendedIsotopeInput("227Ac", 227, 89, 6.075, 6.871e8, "NNDC"),
    ExtendedIsotopeInput("231Pa", 231, 91, 5.149, 1.034e12, "NNDC"),
    ExtendedIsotopeInput("235U", 235, 92, 4.679, 2.221e16, "NNDC"),
    ExtendedIsotopeInput("236U", 236, 92, 4.494, 7.391e13, "NNDC"),
    ExtendedIsotopeInput("241Am", 241, 95, 5.545, 1.364e8, "NNDC"),
    ExtendedIsotopeInput("242Cm", 242, 96, 6.215, 1.407e7, "NNDC"),
    ExtendedIsotopeInput("252Cf", 252, 98, 6.217, 8.347e7, "NNDC"),
)


def reduced_mass_MeV(A_d: int) -> float:
    m_a = 4.0 * M_N_MEV
    m_d = float(A_d) * M_N_MEV
    return (m_a * m_d) / (m_a + m_d)


def R_from_A(A: int) -> float:
    return R_SCALE * (float(A) ** (1.0 / 3.0))


def b_from_Q(Z: int, Q_MeV: float) -> float:
    Z_d = Z - 2
    return 2.0 * Z_d * E2_MEV_FM / Q_MeV


def W_numeric_Ad(
    R_fm: float,
    b_fm: float,
    Q_MeV: float,
    Z_d: int,
    *,
    Ad: int | None,
    A: int | None = None,
) -> float:
    if Ad is None and A is not None:
        Ad = A - 4
    if Ad is None:
        raise ValueError("need Ad or A")
    mu = reduced_mass_MeV(Ad)
    coeff = math.sqrt(2.0 * mu) / HBARC_MEV_FM

    def integrand(r: float) -> float:
        v_c = 2.0 * Z_d * E2_MEV_FM / r
        if v_c <= Q_MeV:
            return 0.0
        return math.sqrt(v_c - Q_MeV)

    raw, _ = quad(integrand, R_fm, b_fm, limit=200)
    return _W_CALIB_SCALE * coeff * raw


def t12_gamow_s(W: float, R_fm: float, Q_MeV: float, Ad: int) -> float:
    """Gamow half-life with P_alpha=1 (assault frequency nu = v/(2R))."""
    mu = reduced_mass_MeV(Ad)
    v_over_c = math.sqrt(2.0 * Q_MeV / mu)
    v_fm_s = v_over_c * C_FM_S
    nu = v_fm_s / (2.0 * R_fm)
    lam = nu * math.exp(-2.0 * W)
    if lam <= 0.0:
        return float("inf")
    return LN2 / lam


def log10_P_extracted(t_gamow_s: float, t_meas_s: float) -> float:
    ratio = t_gamow_s / t_meas_s
    if ratio <= 0.0:
        return float("-inf")
    return math.log10(ratio)


def row_from_extended(raw: ExtendedIsotopeInput) -> IsotopeRow:
    R = R_from_A(raw.A)
    b = b_from_Q(raw.Z, raw.Q_alpha_MeV)
    Ad = raw.A - 4
    W = W_numeric_Ad(R, b, raw.Q_alpha_MeV, raw.Z - 2, Ad=Ad, A=raw.A)
    t_g = t12_gamow_s(W, R, raw.Q_alpha_MeV, Ad)
    log10_p = log10_P_extracted(t_g, raw.t12_meas_s)
    return IsotopeRow(
        name=raw.name,
        Q_alpha_MeV=raw.Q_alpha_MeV,
        R_fm=R,
        b_fm=b,
        W_ana=W,
        t12_Gamow_s=t_g,
        t12_meas_s=raw.t12_meas_s,
        log10_P_extracted=round(log10_p, 2),
    )


def extended_isotopes() -> tuple[IsotopeRow, ...]:
    """Extended-only rows (excludes names already in base 14)."""
    base_names = {iso.name for iso in ISOTOPES}
    rows: list[IsotopeRow] = []
    for raw in EXTENDED_RAW:
        if raw.name in base_names:
            continue
        rows.append(row_from_extended(raw))
    return tuple(rows)


def combined_isotopes() -> tuple[IsotopeRow, ...]:
    """Base 14 + extended (28 total with current catalog)."""
    ext = extended_isotopes()
    return ISOTOPES + ext


def catalog_metadata(n_base: int, n_ext: int, n_total: int) -> dict[str, Any]:
    return {
        "n_base": n_base,
        "n_extended_added": n_ext,
        "n_total": n_total,
        "sources": EXTENDED_SOURCES,
        "R_formula": f"R_fm = {R_SCALE} * A^(1/3)",
        "b_formula": "b_fm = 2 Z_d e^2 / Q_alpha (MeV·fm units)",
        "W_protocol": f"numeric Gamow integral × {_W_CALIB_SCALE:.4f} (fit to base 14)",
        "scope": "RC1 as-reported public Q and t1/2; geometric R,b,W — not microscopic structure",
    }
