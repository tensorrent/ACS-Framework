#!/usr/bin/env python3
"""
P_alpha refined overlap: isotope-resolved / parametric S (Channel A)
and self-consistent Woods-Saxon + Coulomb radial eigenmode (Channel B).

Extends palpha_overlap_throat.py without deleting it. Flat proxy and
throat+WS baselines are recomputed for side-by-side acceptance metrics.

Channel A — spectroscopic factor structure
-----------------------------------------
  Raw diagnostic:  S_i = P_ext / P_model,i  (equivalently
                   log10 S_i = log10 P_ext - log10 P_model).
  Per-isotope S zeros that isotope's mean residual by construction;
  therefore we also report:
    - global S (mean log residual; existing protocol)
    - parametric log10 S(A,Z) and log10 S(R) fits
    - leave-one-out (LOO) RMS of predicted log10 P vs extracted

Channel B — self-consistent WS + Coulomb eigenmode
-------------------------------------------------
  For each isotope, solve the ell=0 radial Sturm-Liouville problem

      -(hbar^2/2 mu) u'' + [V_WS(r; V0) + V_C(r)] u = E u

  on the confined throat [0, R] with Dirichlet BCs u(0)=u(R)=0.
  Depth V0 is adjusted so the ground eigenvalue equals Q_alpha
  (self-consistency / resonance-in-a-box surrogate).  The resulting
  eigenvector is the alpha trial u_alpha for the throat-weighted overlap
  with the confined flag mode u_in (same measure w=R/r as the throat
  sequel).

Scope (RC1): geometric/structural preformation proxies and a documented
parametric S model — not unique many-body nuclear structure.

Dependencies: numpy, scipy.
"""

from __future__ import annotations

import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import simpson
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

# Local imports (same package directory).
from palpha_overlap import (  # type: ignore
    ISOTOPES,
    IsotopeRow,
    R0_DEFAULT_FM,
    a_alpha_fm,
    best_fit_global_S,
    u_in,
)
from palpha_overlap_throat import (  # type: ignore
    A_WS_DEFAULT_FM,
    KAPPA_TAIL_DEFAULT,
    N_GRID,
    run_analysis as run_throat_analysis,
    summarize_model_rows,
    throat_weight_ads,
)
from palpha_overlap_gamow import evaluate_gamow_isotope  # type: ignore

# Shared harness memo (disk + memory).
_CODE_ROOT = Path(__file__).resolve().parents[1]
if str(_CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(_CODE_ROOT))
from acs_memo import fmt_float, get_npz_solve, put_npz_solve  # noqa: E402

# ---------------------------------------------------------------------------
# Paths / constants
# ---------------------------------------------------------------------------

REPO_DOCS = (
    Path(__file__).resolve().parents[2] / "docs" / "palpha_overlap_refined_results.json"
)

HBARC_MEV_FM = 197.3269718
E2_MEV_FM = 1.439964547  # e^2 / (4 pi epsilon_0) in MeV fm
M_N_MEV = 931.494  # nucleon mass scale (MeV/c^2)

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

N_EIGEN_GRID = 800  # interior FD grid for Channel B (excludes endpoints)
V0_BRACKET_MEV = (1.0, 250.0)


# ---------------------------------------------------------------------------
# Isotope nuclear numbers
# ---------------------------------------------------------------------------


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
    """Alpha–daughter reduced mass in MeV/c^2 (nucleon-mass units)."""
    m_a = 4.0 * M_N_MEV
    m_d = float(A_d) * M_N_MEV
    return (m_a * m_d) / (m_a + m_d)


def hbar2_over_2mu(A_d: int) -> float:
    """ħ²/(2μ) in MeV·fm²."""
    mu = reduced_mass_MeV(A_d)
    return (HBARC_MEV_FM * HBARC_MEV_FM) / (2.0 * mu)


# ---------------------------------------------------------------------------
# Channel B — potentials and eigenmode
# ---------------------------------------------------------------------------


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
    """Uniform-sphere Coulomb for r < R_c; point Coulomb beyond."""
    pref = Z1 * Z2 * E2_MEV_FM
    vc = np.empty_like(r, dtype=float)
    inside = r < R_c_fm
    # Avoid division by zero at r=0: interior formula is regular.
    vc[inside] = (pref / (2.0 * R_c_fm)) * (3.0 - (r[inside] / R_c_fm) ** 2)
    outside = ~inside
    vc[outside] = pref / np.maximum(r[outside], R_c_fm)
    # r=0 exact limit of interior form
    if r.size and r[0] == 0.0:
        vc[0] = (pref / (2.0 * R_c_fm)) * 3.0
    return vc


def eigen_ground_energy_and_mode(
    R_fm: float,
    V0_MeV: float,
    *,
    A_d: int,
    Z_d: int,
    r0_fm: float,
    a_ws_fm: float,
    n_interior: int = N_EIGEN_GRID,
) -> tuple[float, np.ndarray, np.ndarray, dict[str, float]]:
    """
    Tridiagonal FD eigenproblem on (0, R) with Dirichlet u(0)=u(R)=0.

    Returns (E0, r_full including endpoints, u_full, meta).
    """
    if R_fm <= 0.0:
        raise ValueError("R_fm must be positive")
    h = R_fm / (n_interior + 1)
    r = h * np.arange(1, n_interior + 1, dtype=float)  # interior nodes
    R_ws = r0_fm * (float(A_d) ** (1.0 / 3.0))
    R_c = R_ws
    V = V_woods_saxon(r, V0_MeV, R_ws, a_ws_fm) + V_coulomb(r, 2, Z_d, R_c)
    coeff = hbar2_over_2mu(A_d)
    # -coeff * (u_{i+1}-2u_i+u_{i-1})/h^2 + V u = E u
    diag = (2.0 * coeff / (h * h)) + V
    off = np.full(n_interior - 1, -coeff / (h * h), dtype=float)
    evals, evecs = eigh_tridiagonal(diag, off, select="i", select_range=(0, 0))
    E0 = float(evals[0])
    u_int = evecs[:, 0].astype(float)
    # Orient positive near origin (first lobe).
    if u_int[0] < 0.0:
        u_int = -u_int
    r_full = np.concatenate(([0.0], r, [R_fm]))
    u_full = np.concatenate(([0.0], u_int, [0.0]))
    # Normalize ∫ u^2 dr = 1 on [0,R] (flat measure; overlap reweights).
    norm = simpson(u_full * u_full, x=r_full)
    if norm > 0.0:
        u_full = u_full / math.sqrt(norm)
    meta = {
        "V0_MeV": float(V0_MeV),
        "E0_MeV": E0,
        "R_ws_fm": float(R_ws),
        "R_c_fm": float(R_c),
        "h_fm": float(h),
        "n_interior": float(n_interior),
        "hbar2_2mu": float(coeff),
        "mu_MeV": float(reduced_mass_MeV(A_d)),
    }
    return E0, r_full, u_full, meta


def _dirichlet_solve_key(
    row: IsotopeRow,
    *,
    r0_fm: float,
    a_ws_fm: float,
    n_interior: int,
) -> tuple[Any, ...]:
    return (
        row.name,
        "dirichlet",
        fmt_float(r0_fm),
        fmt_float(a_ws_fm),
        int(n_interior),
        fmt_float(row.Q_alpha_MeV),
        fmt_float(row.R_fm),
        fmt_float(row.b_fm),
    )


def find_V0_for_Q(
    row: IsotopeRow,
    ids: NuclearIds,
    *,
    r0_fm: float,
    a_ws_fm: float,
    n_interior: int = N_EIGEN_GRID,
    bracket: tuple[float, float] = V0_BRACKET_MEV,
) -> tuple[float, float, np.ndarray, np.ndarray, dict[str, float]]:
    """
    Self-consistent depth: find V0 in bracket such that E0(V0) = Q_alpha.

    Deeper V0 lowers E0.  f(V0) = E0(V0) - Q changes from + to - as V0 grows.
    """
    Q = row.Q_alpha_MeV
    cache_parts = _dirichlet_solve_key(
        row, r0_fm=r0_fm, a_ws_fm=a_ws_fm, n_interior=n_interior
    )
    hit = get_npz_solve("palpha_eigen", cache_parts)
    if hit is not None:
        return hit["V0"], hit["E0"], hit["r"], hit["u"], hit["meta"]

    def f(V0: float) -> float:
        E0, _, _, _ = eigen_ground_energy_and_mode(
            row.R_fm,
            V0,
            A_d=ids.A_d,
            Z_d=ids.Z_d,
            r0_fm=r0_fm,
            a_ws_fm=a_ws_fm,
            n_interior=n_interior,
        )
        return E0 - Q

    f_lo = f(bracket[0])
    f_hi = f(bracket[1])
    # Expand bracket if needed (shallow: E0 > Q; deep: E0 < Q).
    lo, hi = bracket
    if f_lo * f_hi > 0.0:
        # Try widening.
        for hi_try in (300.0, 400.0, 600.0):
            f_hi = f(hi_try)
            if f_lo * f_hi <= 0.0:
                hi = hi_try
                break
        else:
            # Fall back: use V0 that minimizes |E0 - Q| on a coarse grid.
            grid = np.linspace(lo, hi_try, 40)
            vals = [abs(f(float(v))) for v in grid]
            V0 = float(grid[int(np.argmin(vals))])
            E0, r, u, meta = eigen_ground_energy_and_mode(
                row.R_fm,
                V0,
                A_d=ids.A_d,
                Z_d=ids.Z_d,
                r0_fm=r0_fm,
                a_ws_fm=a_ws_fm,
                n_interior=n_interior,
            )
            meta = {
                **meta,
                "V0_fit_status": 0.0,  # 0 = grid fallback
                "Q_alpha_MeV": Q,
                "E0_minus_Q": E0 - Q,
            }
            put_npz_solve(
                "palpha_eigen",
                cache_parts,
                V0=V0,
                E0=E0,
                r=r,
                u=u,
                meta=meta,
            )
            return V0, E0, r, u, meta

    V0 = float(brentq(f, lo, hi, xtol=1e-6, rtol=1e-6, maxiter=80))
    E0, r, u, meta = eigen_ground_energy_and_mode(
        row.R_fm,
        V0,
        A_d=ids.A_d,
        Z_d=ids.Z_d,
        r0_fm=r0_fm,
        a_ws_fm=a_ws_fm,
        n_interior=n_interior,
    )
    meta = {
        **meta,
        "V0_fit_status": 1.0,  # 1 = brentq root
        "Q_alpha_MeV": Q,
        "E0_minus_Q": E0 - Q,
    }
    put_npz_solve(
        "palpha_eigen",
        cache_parts,
        V0=V0,
        E0=E0,
        r=r,
        u=u,
        meta=meta,
    )
    return V0, E0, r, u, meta


def overlap_P_eigenmode(
    row: IsotopeRow,
    ids: NuclearIds,
    *,
    r0_fm: float = R0_DEFAULT_FM,
    a_ws_fm: float = A_WS_DEFAULT_FM,
    n_overlap: int = N_GRID,
    n_interior: int = N_EIGEN_GRID,
) -> tuple[float, dict[str, Any]]:
    """Throat-weighted overlap of u_in with self-consistent WS+Coulomb mode."""
    V0, E0, r_e, u_e, emeta = find_V0_for_Q(
        row, ids, r0_fm=r0_fm, a_ws_fm=a_ws_fm, n_interior=n_interior
    )
    # Interpolate eigenmode onto fine overlap grid on [0, R].
    r = np.linspace(0.0, row.R_fm, n_overlap)
    ua = np.interp(r, r_e, u_e)
    ui = u_in(r, row.R_fm)
    w = throat_weight_ads(r, row.R_fm)
    num = simpson(ui * ua * w, x=r)
    den_in = simpson(ui * ui * w, x=r)
    den_a = simpson(ua * ua * w, x=r)
    if den_in <= 0.0 or den_a <= 0.0:
        raise RuntimeError("non-positive weighted norms in eigenmode overlap")
    P = float((num * num) / (den_in * den_a))
    meta = {
        **emeta,
        "num": float(num),
        "den_in": float(den_in),
        "den_a": float(den_a),
        "bc": "Dirichlet u(0)=u(R)=0; V0 so E0=Q_alpha (box resonance surrogate)",
        "potential": "V_WS(V0,R_ws=r0 A_d^{1/3},a)+V_Coulomb(Z_alpha,Z_d,R_c=R_ws)",
    }
    return P, meta


def evaluate_eigenmode_isotope(
    row: IsotopeRow,
    *,
    r0_fm: float,
    a_ws_fm: float,
    n_overlap: int,
    n_interior: int,
) -> dict[str, Any]:
    ids = parse_nuclear_ids(row.name)
    P_raw, meta = overlap_P_eigenmode(
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
        "model_label": "throat_ws_coulomb_eigenmode",
        "P_model": P_raw,
        "log10_P_model": log10_P_model,
        "log10_P_extracted": row.log10_P_extracted,
        "residual_raw": log10_P_model - row.log10_P_extracted,
        "alpha_meta": meta,
    }


# ---------------------------------------------------------------------------
# Channel A — isotope S and parametric / LOO
# ---------------------------------------------------------------------------


def extract_S_i(
    log10_P_model: np.ndarray, log10_P_ext: np.ndarray
) -> np.ndarray:
    """S_i = 10^(log10 P_ext - log10 P_model) = P_ext / P_model."""
    return 10.0 ** (log10_P_ext - log10_P_model)


def fit_linear_logS(
    features: np.ndarray, log10_S: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    Least-squares: log10 S ≈ X @ beta, X = [1 | features].
    Returns (beta, fitted_log10_S).
    """
    n = log10_S.size
    X = np.column_stack([np.ones(n), features])
    beta, _, _, _ = np.linalg.lstsq(X, log10_S, rcond=None)
    return beta, X @ beta


def loo_parametric_logS(
    features: np.ndarray, log10_S: np.ndarray
) -> tuple[np.ndarray, float]:
    """
    Leave-one-out predictions of log10 S from linear model in features.
    Returns (loo_log10_S_pred, loo_rms of (pred - true) on log10 S).
    """
    n = log10_S.size
    preds = np.empty(n, dtype=float)
    for i in range(n):
        mask = np.ones(n, dtype=bool)
        mask[i] = False
        beta, _ = fit_linear_logS(features[mask], log10_S[mask])
        if features.ndim == 1:
            x_i = np.array([1.0, features[i]])
        else:
            x_i = np.concatenate(([1.0], features[i]))
        preds[i] = float(x_i @ beta)
    rms = float(np.sqrt(np.mean((preds - log10_S) ** 2)))
    return preds, rms


def channel_A_from_model_rows(
    rows: list[dict[str, Any]],
    isotopes: tuple[IsotopeRow, ...] = ISOTOPES,
) -> dict[str, Any]:
    """Build raw S_i, global S, parametric S(A,Z)/S(R), and LOO metrics."""
    n = len(rows)
    log10_model = np.array([r["log10_P_model"] for r in rows], dtype=float)
    log10_ext = np.array([r["log10_P_extracted"] for r in rows], dtype=float)
    S_i = extract_S_i(log10_model, log10_ext)
    log10_S_i = np.log10(S_i)

    ids = [parse_nuclear_ids(iso.name) for iso in isotopes]
    A = np.array([d.A for d in ids], dtype=float)
    Z = np.array([d.Z for d in ids], dtype=float)
    R = np.array([iso.R_fm for iso in isotopes], dtype=float)

    S_global = best_fit_global_S(log10_model, log10_ext)
    log10_S_global = math.log10(S_global)
    resid_global = (log10_model + log10_S_global) - log10_ext
    rms_global = float(np.sqrt(np.mean(resid_global**2)))

    # Parametric log10 S(A,Z)
    feat_AZ = np.column_stack([A, Z])
    beta_AZ, fit_AZ = fit_linear_logS(feat_AZ, log10_S_i)
    pred_P_AZ = log10_model + fit_AZ
    resid_AZ = pred_P_AZ - log10_ext
    rms_AZ = float(np.sqrt(np.mean(resid_AZ**2)))
    loo_AZ, loo_rms_logS_AZ = loo_parametric_logS(feat_AZ, log10_S_i)
    loo_resid_AZ = (log10_model + loo_AZ) - log10_ext
    loo_rms_P_AZ = float(np.sqrt(np.mean(loo_resid_AZ**2)))

    # Parametric log10 S(R)
    beta_R, fit_R = fit_linear_logS(R, log10_S_i)
    pred_P_R = log10_model + fit_R
    resid_R = pred_P_R - log10_ext
    rms_R = float(np.sqrt(np.mean(resid_R**2)))
    loo_R, loo_rms_logS_R = loo_parametric_logS(R, log10_S_i)
    loo_resid_R = (log10_model + loo_R) - log10_ext
    loo_rms_P_R = float(np.sqrt(np.mean(loo_resid_R**2)))

    # Choose better parametric by LOO RMS on log10 P
    if loo_rms_P_AZ <= loo_rms_P_R:
        best_param = "S(A,Z)"
        best_loo_rms = loo_rms_P_AZ
    else:
        best_param = "S(R)"
        best_loo_rms = loo_rms_P_R

    per_iso = []
    for i, r in enumerate(rows):
        per_iso.append(
            {
                "isotope": r["isotope"],
                "A": ids[i].A,
                "Z": ids[i].Z,
                "R_fm": float(R[i]),
                "log10_P_model": float(log10_model[i]),
                "log10_P_extracted": float(log10_ext[i]),
                "S_i": float(S_i[i]),
                "log10_S_i": float(log10_S_i[i]),
                "log10_S_AZ_fit": float(fit_AZ[i]),
                "log10_S_AZ_loo": float(loo_AZ[i]),
                "residual_P_AZ_loo": float(loo_resid_AZ[i]),
                "log10_S_R_fit": float(fit_R[i]),
                "log10_S_R_loo": float(loo_R[i]),
                "residual_P_R_loo": float(loo_resid_R[i]),
                "residual_with_global_S": float(resid_global[i]),
            }
        )

    return {
        "base_model_label": rows[0].get("model_label", "unknown"),
        "n_isotopes": n,
        "S_i_table": per_iso,
        "S_i_mean": float(np.mean(S_i)),
        "S_i_std": float(np.std(S_i, ddof=1)),
        "log10_S_i_mean": float(np.mean(log10_S_i)),
        "log10_S_i_std": float(np.std(log10_S_i, ddof=1)),
        "note_tautology": (
            "Per-isotope S_i zeros that isotope's residual on the rate / "
            "log10-P scale by construction; use parametric + LOO for "
            "predictive assessment."
        ),
        "global_S": {
            "S": S_global,
            "log10_S": log10_S_global,
            "rms_residual_log10_P": rms_global,
            "mean_residual": float(np.mean(resid_global)),
        },
        "parametric_S_AZ": {
            "form": "log10 S = b0 + b1 A + b2 Z",
            "beta": {
                "b0": float(beta_AZ[0]),
                "b1_A": float(beta_AZ[1]),
                "b2_Z": float(beta_AZ[2]),
            },
            "rms_in_sample_log10_P": rms_AZ,
            "loo_rms_log10_S": loo_rms_logS_AZ,
            "loo_rms_log10_P": loo_rms_P_AZ,
        },
        "parametric_S_R": {
            "form": "log10 S = c0 + c1 R",
            "beta": {"c0": float(beta_R[0]), "c1_R": float(beta_R[1])},
            "rms_in_sample_log10_P": rms_R,
            "loo_rms_log10_S": loo_rms_logS_R,
            "loo_rms_log10_P": loo_rms_P_R,
        },
        "best_parametric_by_loo_rms": best_param,
        "best_parametric_loo_rms_log10_P": best_loo_rms,
    }


# ---------------------------------------------------------------------------
# Full refined analysis
# ---------------------------------------------------------------------------


def acceptance_row(
    label: str,
    mean_log10: float,
    r: float,
    rms_raw: float,
    rms_S: float,
    loo_rms: float | None = None,
) -> dict[str, Any]:
    return {
        "label": label,
        "mean_log10_P": mean_log10,
        "pearson_r": r,
        "rms_raw": rms_raw,
        "rms_global_S": rms_S,
        "loo_rms_parametric_S": loo_rms,
    }


def run_refined_analysis(
    *,
    r0_fm: float = R0_DEFAULT_FM,
    a_ws_fm: float = A_WS_DEFAULT_FM,
    kappa_fm_inv: float = KAPPA_TAIL_DEFAULT,
    n_grid: int = N_GRID,
    n_interior: int = N_EIGEN_GRID,
) -> dict[str, Any]:
    # --- Baselines: flat Gaussian + throat WS (reuse throat runner) ---
    throat = run_throat_analysis(
        r0_fm=r0_fm,
        a_ws_fm=a_ws_fm,
        kappa_fm_inv=kappa_fm_inv,
        n_grid=n_grid,
    )
    flat_sum = throat["models"]["flat_gaussian"]["summary"]
    throat_ws_sum = throat["models"]["throat_ws"]["summary"]
    throat_ws_rows = throat["models"]["throat_ws"]["isotopes"]

    # --- Channel A on throat+WS base ---
    channel_A = channel_A_from_model_rows(throat_ws_rows, ISOTOPES)

    # --- Channel B: eigenmode ---
    eigen_rows = [
        evaluate_eigenmode_isotope(
            iso,
            r0_fm=r0_fm,
            a_ws_fm=a_ws_fm,
            n_overlap=n_grid,
            n_interior=n_interior,
        )
        for iso in ISOTOPES
    ]
    eigen_sum = summarize_model_rows(eigen_rows)
    eigen_sum.update(
        {
            "r0_fm": r0_fm,
            "a_ws_fm": a_ws_fm,
            "n_grid": n_grid,
            "n_interior_eigen": n_interior,
            "primary": False,
            "scope_note": (
                "Self-consistent WS+Coulomb ell=0 eigenmode on [0,R] with "
                "Dirichlet BCs; V0 fitted so E0=Q_alpha. Throat weight w=R/r. "
                "Box-resonance surrogate — not a complex Gamow eigenphase claim."
            ),
        }
    )
    # Channel A also on eigenmode base (for completeness)
    channel_A_eigen = channel_A_from_model_rows(eigen_rows, ISOTOPES)

    # --- Channel C: Gamow outgoing BC on [0,b] ---
    gamow_rows = [
        evaluate_gamow_isotope(
            iso,
            r0_fm=r0_fm,
            a_ws_fm=a_ws_fm,
            n_overlap=n_grid,
            n_interior=n_interior,
        )
        for iso in ISOTOPES
    ]
    gamow_sum = summarize_model_rows(gamow_rows)
    gamow_sum.update(
        {
            "r0_fm": r0_fm,
            "a_ws_fm": a_ws_fm,
            "n_grid": n_grid,
            "n_interior_eigen": n_interior,
            "primary": False,
            "scope_note": (
                "Self-consistent WS+Coulomb ell=0 eigenmode on [0,b] with "
                "Robin outgoing WKB match at r=b; V0 fitted so E0=Q_alpha. "
                "Overlap support remains [0,R] with throat weight. "
                "Quasistationary outgoing surrogate — not a complex pole search."
            ),
        }
    )

    # Acceptance comparison table
    acceptance = [
        acceptance_row(
            "flat_gaussian",
            flat_sum["mean_log10_P_model"],
            flat_sum["pearson_r_raw"],
            flat_sum["rms_residual_raw"],
            flat_sum["rms_residual_S"],
            None,
        ),
        acceptance_row(
            "throat_ws",
            throat_ws_sum["mean_log10_P_model"],
            throat_ws_sum["pearson_r_raw"],
            throat_ws_sum["rms_residual_raw"],
            throat_ws_sum["rms_residual_S"],
            None,
        ),
        acceptance_row(
            "refined_eigenmode",
            eigen_sum["mean_log10_P_model"],
            eigen_sum["pearson_r_raw"],
            eigen_sum["rms_residual_raw"],
            eigen_sum["rms_residual_S"],
            None,
        ),
        acceptance_row(
            "gamow_outgoing_eigenmode",
            gamow_sum["mean_log10_P_model"],
            gamow_sum["pearson_r_raw"],
            gamow_sum["rms_residual_raw"],
            gamow_sum["rms_residual_S"],
            None,
        ),
        acceptance_row(
            "parametric_S_AZ_on_throat_ws",
            throat_ws_sum["mean_log10_P_model"],
            throat_ws_sum["pearson_r_raw"],
            throat_ws_sum["rms_residual_raw"],
            throat_ws_sum["rms_residual_S"],
            channel_A["parametric_S_AZ"]["loo_rms_log10_P"],
        ),
        acceptance_row(
            "parametric_S_R_on_throat_ws",
            throat_ws_sum["mean_log10_P_model"],
            throat_ws_sum["pearson_r_raw"],
            throat_ws_sum["rms_residual_raw"],
            throat_ws_sum["rms_residual_S"],
            channel_A["parametric_S_R"]["loo_rms_log10_P"],
        ),
    ]

    # Which non-tautological channel reduces RMS most?
    # Compare: eigenmode RMS(S) vs throat RMS(S); parametric LOO vs global S RMS.
    rms_throat_S = throat_ws_sum["rms_residual_S"]
    rms_eigen_S = eigen_sum["rms_residual_S"]
    rms_gamow_S = gamow_sum["rms_residual_S"]
    loo_AZ = channel_A["parametric_S_AZ"]["loo_rms_log10_P"]
    loo_R = channel_A["parametric_S_R"]["loo_rms_log10_P"]
    best_loo = min(loo_AZ, loo_R)
    best_loo_name = "S(A,Z)" if loo_AZ <= loo_R else "S(R)"

    delta_eigen_vs_throat = rms_eigen_S - rms_throat_S
    delta_param_loo_vs_global = best_loo - rms_throat_S

    if best_loo < rms_eigen_S and best_loo < rms_throat_S:
        winner = f"Channel A parametric {best_loo_name} (LOO)"
        winner_rms = best_loo
        winner_metric = "loo_rms_log10_P"
    elif rms_eigen_S < rms_throat_S:
        winner = "Channel B refined eigenmode (global S)"
        winner_rms = rms_eigen_S
        winner_metric = "rms_residual_S"
    else:
        winner = "neither refined channel beats throat+WS global-S RMS"
        winner_rms = rms_throat_S
        winner_metric = "rms_residual_S_throat_ws"

    comparison = {
        "rms_throat_ws_global_S": rms_throat_S,
        "rms_eigenmode_global_S": rms_eigen_S,
        "rms_gamow_outgoing_global_S": rms_gamow_S,
        "delta_eigen_minus_throat_S": delta_eigen_vs_throat,
        "delta_gamow_minus_throat_S": rms_gamow_S - rms_throat_S,
        "delta_gamow_minus_eigen_S": rms_gamow_S - rms_eigen_S,
        "pearson_eigenmode": eigen_sum["pearson_r_raw"],
        "pearson_gamow_outgoing": gamow_sum["pearson_r_raw"],
        "loo_rms_parametric_S_AZ": loo_AZ,
        "loo_rms_parametric_S_R": loo_R,
        "delta_best_loo_minus_throat_S": delta_param_loo_vs_global,
        "winner_non_tautological": winner,
        "winner_rms": winner_rms,
        "winner_metric": winner_metric,
        "note": (
            "Per-isotope S_i is excluded from the winner (tautological). "
            "Parametric S judged by leave-one-out RMS on log10 P; "
            "eigenmode judged by RMS after one global S."
        ),
    }

    return {
        "model_family": {
            "channel_A": (
                "Raw S_i = P_ext/P_model; global S; parametric "
                "log10 S(A,Z) and log10 S(R) with leave-one-out"
            ),
            "channel_B": (
                "Self-consistent V_WS+V_C ell=0 eigenmode on [0,R], "
                "Dirichlet BC, V0 so E0=Q_alpha; throat weight w=R/r; "
                "overlap with u_in = r j_0(pi r/R)"
            ),
            "P_definition": (
                "|∫ u_in u_alpha w dr|^2 / (∫ u_in^2 w · ∫ u_alpha^2 w) on [0,R]"
            ),
            "scope": (
                "RC1 geometric/structural proxies and parametric S — "
                "not uniqueness of many-body preformation"
            ),
        },
        "parameters": {
            "r0_fm": r0_fm,
            "a_ws_fm": a_ws_fm,
            "kappa_fm_inv": kappa_fm_inv,
            "n_grid": n_grid,
            "n_interior_eigen": n_interior,
            "a_alpha_fm": a_alpha_fm(r0_fm),
        },
        "baselines": {
            "flat_gaussian": flat_sum,
            "throat_ws": throat_ws_sum,
            "throat_comparison": throat.get("comparison_flat_vs_throat_ws"),
        },
        "channel_A_isotope_S_on_throat_ws": channel_A,
        "channel_B_eigenmode": {
            "summary": eigen_sum,
            "isotopes": eigen_rows,
        },
        "channel_C_gamow_outgoing": {
            "summary": gamow_sum,
            "isotopes": gamow_rows,
        },
        "channel_A_on_eigenmode_base": channel_A_eigen,
        "acceptance_table": acceptance,
        "comparison_channels": comparison,
        "table_source": "Flag_Condensate_Nuclear_Decay.tex table (14 alpha emitters)",
        "baseline_refs": {
            "flat": "palpha_overlap.py / docs/palpha_overlap_results.json",
            "throat": (
                "palpha_overlap_throat.py / docs/palpha_overlap_throat_results.json"
            ),
        },
        "utc": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def format_refined_markdown(result: dict[str, Any]) -> str:
    lines: list[str] = [
        "## Acceptance comparison",
        "",
        "| Channel | ⟨log10 P⟩ | r | RMS raw | RMS global S | LOO RMS param S |",
        "|---------|----------:|--:|--------:|-------------:|----------------:|",
    ]
    for row in result["acceptance_table"]:
        loo = row["loo_rms_parametric_S"]
        loo_s = f"{loo:.4f}" if loo is not None else "—"
        lines.append(
            f"| {row['label']} | {row['mean_log10_P']:+.4f} | "
            f"{row['pearson_r']:+.4f} | {row['rms_raw']:.4f} | "
            f"{row['rms_global_S']:.4f} | {loo_s} |"
        )
    c = result["comparison_channels"]
    A = result["channel_A_isotope_S_on_throat_ws"]
    B = result["channel_B_eigenmode"]["summary"]
    lines.extend(
        [
            "",
            "### Channel A (on throat+WS base)",
            f"- ⟨S_i⟩ = {A['S_i_mean']:.6e} (std {A['S_i_std']:.6e})",
            f"- ⟨log10 S_i⟩ = {A['log10_S_i_mean']:+.4f} "
            f"(std {A['log10_S_i_std']:.4f})",
            f"- global S = {A['global_S']['S']:.6e}, "
            f"RMS = {A['global_S']['rms_residual_log10_P']:.4f}",
            f"- parametric S(A,Z) LOO RMS(log10 P) = "
            f"{A['parametric_S_AZ']['loo_rms_log10_P']:.4f}",
            f"- parametric S(R) LOO RMS(log10 P) = "
            f"{A['parametric_S_R']['loo_rms_log10_P']:.4f}",
            f"- best parametric by LOO: {A['best_parametric_by_loo_rms']}",
            "",
            "### Channel B (WS+Coulomb eigenmode)",
            f"- ⟨log10 P⟩ = {B['mean_log10_P_model']:+.4f}",
            f"- Pearson r = {B['pearson_r_raw']:+.4f}",
            f"- RMS raw = {B['rms_residual_raw']:.4f}",
            f"- global S = {B['best_fit_global_S']:.6e}, "
            f"RMS(S) = {B['rms_residual_S']:.4f}",
            "",
            "### Winner (non-tautological)",
            f"- {c['winner_non_tautological']}",
            f"- metric `{c['winner_metric']}` = {c['winner_rms']:.4f}",
            f"- Δ(eigen − throat) RMS(S) = {c['delta_eigen_minus_throat_S']:+.4f}",
            f"- Δ(best LOO − throat) = {c['delta_best_loo_minus_throat_S']:+.4f}",
            "",
            f"_Note:_ {c['note']}",
            "",
            "### S_i diagnostic table (throat+WS)",
            "| Isotope | A | Z | S_i | log10 S_i | log10 S_AZ LOO | resid LOO |",
            "|---------|--:|--:|----:|----------:|---------------:|----------:|",
        ]
    )
    for row in A["S_i_table"]:
        lines.append(
            f"| {row['isotope']} | {row['A']} | {row['Z']} | "
            f"{row['S_i']:.4e} | {row['log10_S_i']:+.4f} | "
            f"{row['log10_S_AZ_loo']:+.4f} | {row['residual_P_AZ_loo']:+.4f} |"
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
    result = run_refined_analysis()
    out_path = REPO_DOCS
    write_json(result, out_path)

    log_dir = out_path.parent / "palpha_overlap_refined_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report = format_refined_markdown(result)
    header = (
        f"# P_α refined overlap (Channel A isotopic/parametric S; "
        f"Channel B WS+Coulomb eigenmode)\n"
        f"# utc={stamp}  r0_fm={R0_DEFAULT_FM}  a_ws_fm={A_WS_DEFAULT_FM}\n\n"
    )
    log_body = header + report + f"\n\nJSON written: {out_path}\n"
    log_path = log_dir / f"run_{stamp}.log"
    log_path.write_text(log_body, encoding="utf-8")
    print(log_body)
    print(f"Log written: {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
