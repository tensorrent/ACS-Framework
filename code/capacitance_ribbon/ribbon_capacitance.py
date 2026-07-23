#!/usr/bin/env python3
"""
Möbius-ribbon capacitance models (sequel to the framed-unknot electron note).

As-implemented numerical estimates only.  Scope:
  - inputs:  R = hbar/(2 m_e c), charge split e/2 per double-cover sheet,
             aspect ratio a/R (or conformal modulus derived from it)
  - outputs: C [F] and alpha^{-1} from self-stress match
             (e/2)^2 / (2 C) = m_e c^2
  - reference: CODATA-style alpha^{-1} approx 137.035999084 (comparison only;
               not a uniqueness proof of alpha or a QED derivation)

Dependencies: stdlib + numpy + scipy.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy import constants as const

_CODE_ROOT = Path(__file__).resolve().parents[1]
if str(_CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(_CODE_ROOT))
from acs_memo import cached_json, fmt_float  # noqa: E402

# ---------------------------------------------------------------------------
# Constants (float64; scipy.constants CODATA set)
# ---------------------------------------------------------------------------

EPS0: float = float(const.epsilon_0)  # F/m
HBAR: float = float(const.hbar)  # J s
M_E: float = float(const.m_e)  # kg
C_LIGHT: float = float(const.c)  # m/s
E_CHARGE: float = float(const.e)  # C
ALPHA_CODATA: float = float(const.alpha)
ALPHA_INV_CODATA: float = 1.0 / ALPHA_CODATA  # ~137.035999...

# Spin-radius input scale from the paper: R = hbar / (2 m_e c)
R_SPIN: float = HBAR / (2.0 * M_E * C_LIGHT)

# Self-stress bookkeeping: Q = e/2 on the double cover
Q_SHEET: float = 0.5 * E_CHARGE

DOC_SCOPE: dict[str, Any] = {
    "claim_discipline": "RC1 as-implemented model outputs; not a uniqueness proof of alpha",
    "inputs": {
        "R": "hbar/(2 m_e c) [spin-radius scale input]",
        "charge_split": "e/2 per double-cover sheet",
        "aspect": "a/R (ribbon half-width / R) or conformal modulus from strip geometry",
    },
    "outputs": {
        "C": "capacitance in farads under stated model",
        "alpha_inv": "from (e/2)^2/(2C) = m_e c^2 combined with alpha = e^2/(4 pi eps0 hbar c)",
    },
    "reference_alpha_inv": ALPHA_INV_CODATA,
}


# ---------------------------------------------------------------------------
# Core matching
# ---------------------------------------------------------------------------

def alpha_from_C(C: float, R: float | None = None) -> float:
    """
    Solve self-stress match for alpha^{-1}.

    (e/2)^2 / (2 C) = m_e c^2
    => e^2 = 8 C m_e c^2
    => alpha = e^2 / (4 pi eps0 hbar c) = 2 C m_e c / (pi eps0 hbar)
    => alpha^{-1} = pi eps0 hbar / (2 C m_e c)

    With R = hbar/(2 m_e c) this is equivalent to alpha^{-1} = pi eps0 R / C.
    """
    if C <= 0.0 or not math.isfinite(C):
        return float("nan")
    if R is None:
        return math.pi * EPS0 * HBAR / (2.0 * C * M_E * C_LIGHT)
    return math.pi * EPS0 * R / C


def C_from_alpha_inv(alpha_inv: float, R: float = R_SPIN) -> float:
    """Invert alpha_from_C at fixed R: C = pi eps0 R / alpha_inv."""
    return math.pi * EPS0 * R / alpha_inv


# ---------------------------------------------------------------------------
# Model 1: paper annulus / thin-ring formula
# ---------------------------------------------------------------------------

def annulus_C(R: float, a: float) -> float:
    """
    Baseline from mobius_screw_electron.tex eq. (C):

        C ≈ 2 pi eps0 R / (ln(8 R / a) + 1)

    Valid in the thin-ring regime R >> a.  Additive +1 is scheme-dependent.
    """
    if a <= 0.0 or R <= 0.0:
        raise ValueError("R and a must be positive")
    return 2.0 * math.pi * EPS0 * R / (math.log(8.0 * R / a) + 1.0)


def annulus_alpha_inv(R: float, a: float) -> float:
    """Closed form: alpha^{-1} = (ln(8R/a) + 1) / 2 under the self-stress match."""
    return 0.5 * (math.log(8.0 * R / a) + 1.0)


def annulus_a_over_R_for_alpha(alpha_inv: float = ALPHA_INV_CODATA) -> float:
    """a/R that makes the annulus model match a target alpha^{-1}."""
    # (ln(8R/a)+1)/2 = alpha_inv  =>  a/R = 8 exp(1 - 2 alpha_inv)
    return 8.0 * math.exp(1.0 - 2.0 * alpha_inv)


# ---------------------------------------------------------------------------
# Model 2: conformal-modulus strip → annulus
# ---------------------------------------------------------------------------

def conformal_annulus_C(R: float, a: float, cover: int = 2) -> float:
    """
    Double-cover rectangular strip mapped to an annulus by the exponential map.

    Geometry (inputs):
      length L = cover * 2 pi R   (cover=2 => full Möbius double cover)
      width  W = 2 a              (ribbon full width)

    Map w = exp(2 pi z / L) sends the strip to an annulus with
      rho = r_out / r_in = exp(2 pi W / L) = exp(2 a / (cover R)).

    Geometric-mean radius (circumference matches strip length):
      R_m = L / (2 pi) = cover * R
      r_in  = R_m / sqrt(rho)
      r_out = R_m * sqrt(rho)
      a_eff = (r_out - r_in) / 2

    Capacitance (thin-annular-plate / thin-ring form, same scheme as annulus_C):
      C = 2 pi eps0 R_m / (ln(8 R_m / a_eff) + 1)

    This keeps the paper's logarithmic scheme and replaces (R, a) by the
    conformally imaged (R_m, a_eff).  Coaxial modulus enters only through rho.
    """
    if a <= 0.0 or R <= 0.0 or cover <= 0:
        raise ValueError("R, a, cover must be positive")
    R_m = float(cover) * R
    # rho = exp(2 a / (cover R)); a_eff = R_m * sinh(a/(cover R)).
    # For x << 1, sinh(x) ~ x; use the linear form to avoid float64 underflow.
    x = a / (float(cover) * R)
    a_eff = R_m * (x if x < 1e-6 else math.sinh(x))
    if a_eff <= 0.0 or not math.isfinite(a_eff):
        raise ValueError("degenerate conformal half-width")
    return 2.0 * math.pi * EPS0 * R_m / (math.log(8.0 * R_m / a_eff) + 1.0)


def conformal_modulus_report(R: float, a: float, cover: int = 2) -> dict[str, float]:
    """Diagnostic conformal quantities (dimensionless where noted)."""
    L = float(cover) * 2.0 * math.pi * R
    W = 2.0 * a
    # ln rho = 2 pi W / L = 2 a / (cover R); avoid underflowing rho-1 at tiny a/R
    ln_rho = 2.0 * a / (float(cover) * R)
    rho = math.exp(ln_rho) if ln_rho < 700.0 else float("inf")
    R_m = L / (2.0 * math.pi)
    x = a / (float(cover) * R)
    a_eff = R_m * (x if x < 1e-6 else math.sinh(x))
    return {
        "L_over_R": L / R,
        "W_over_R": W / R,
        "rho": rho,
        "R_m_over_R": R_m / R,
        "a_eff_over_R": a_eff / R,
        "modulus_ln_rho_over_2pi": ln_rho / (2.0 * math.pi),
    }


# ---------------------------------------------------------------------------
# Model 3: 3D BIE (constant-panel collocation) on a Möbius ribbon
# ---------------------------------------------------------------------------

def _centerline(t: np.ndarray, R: float, a: float) -> np.ndarray:
    """
    (2,1)-torus embedding from mobius_screw_electron.tex eq. (r-t):

      r(t) = ((R + a cos t) cos 2t,
              (R + a cos t) sin 2t,
              a sin t),   t in [0, 2 pi)
    """
    ct, st = np.cos(t), np.sin(t)
    c2, s2 = np.cos(2.0 * t), np.sin(2.0 * t)
    rad = R + a * ct
    return np.stack([rad * c2, rad * s2, a * st], axis=-1)


def _torus_mobius_normal(t: np.ndarray, R: float, a: float, eps: float = 1e-8) -> np.ndarray:
    """
    Unit ribbon normal for a Möbius band about the (2,1) centerline.

    Uses the smooth torus minor-circle direction
        n_minor = (cos t cos 2t, cos t sin 2t, sin t)
    as a continuous reference in the normal plane, then applies a
    half-twist about T so the frame is antiperiodic on [0, 2 pi)
    (Möbius edge closing).  Avoids Frenet-frame flips, which otherwise
    corrupt finite-difference n' and inflate panel areas.
    """
    t = np.asarray(t, dtype=float)
    ct, st = np.cos(t), np.sin(t)
    c2, s2 = np.cos(2.0 * t), np.sin(2.0 * t)
    n_minor = np.stack([ct * c2, ct * s2, st], axis=-1)
    rp = (_centerline(t + eps, R, a) - _centerline(t - eps, R, a)) / (2.0 * eps)
    T = rp / np.linalg.norm(rp, axis=-1, keepdims=True)
    # Project minor normal into the plane ⟂ T (numerical safety)
    n0 = n_minor - np.sum(n_minor * T, axis=-1, keepdims=True) * T
    n0 /= np.linalg.norm(n0, axis=-1, keepdims=True)
    B = np.cross(T, n0)
    B /= np.linalg.norm(B, axis=-1, keepdims=True)
    half = 0.5 * t
    ch, sh = np.cos(half), np.sin(half)
    n_m = ch[:, None] * n0 + sh[:, None] * B
    n_m /= np.linalg.norm(n_m, axis=-1, keepdims=True)
    return n_m


def _rect_self_integral(lx: float, ly: float) -> float:
    """
    Analytic ∫∫_panel 1/|r-r_c| dA for a flat rectangle of sides lx, ly,
    collocation at the centroid (standard closed form).
    """
    a, b = 0.5 * lx, 0.5 * ly
    # 4-corner evaluation of x ln(y+R) + y ln(x+R)
    return 4.0 * (
        a * math.log((b + math.sqrt(a * a + b * b)) / a)
        + b * math.log((a + math.sqrt(a * a + b * b)) / b)
    )


def _ribbon_panels(
    R: float,
    a: float,
    n_u: int,
    n_v: int,
    half_width: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Discretize Möbius ribbon: X(u,v) = r(u) + v n(u), u in [0,2pi), v in [-w,w].

    Returns centroids (N,3), areas (N,), edge lengths (N,2)=(du_arc, dv), normals (N,3).
    """
    w = float(a if half_width is None else half_width)
    # cell centers
    u_edges = np.linspace(0.0, 2.0 * math.pi, n_u + 1)
    v_edges = np.linspace(-w, w, n_v + 1)
    u_c = 0.5 * (u_edges[:-1] + u_edges[1:])
    v_c = 0.5 * (v_edges[:-1] + v_edges[1:])
    du = float(u_edges[1] - u_edges[0])
    dv = float(v_edges[1] - v_edges[0])

    uu, vv = np.meshgrid(u_c, v_c, indexing="ij")
    uu = uu.reshape(-1)
    vv = vv.reshape(-1)

    r0 = _centerline(uu, R, a)
    n = _torus_mobius_normal(uu, R, a)
    centroids = r0 + vv[:, None] * n

    # First fundamental form: r_u = r'(u) + v n'(u), r_v = n
    eps = 1e-8
    rp = (_centerline(uu + eps, R, a) - _centerline(uu - eps, R, a)) / (2.0 * eps)
    n_p = (
        _torus_mobius_normal(uu + eps, R, a) - _torus_mobius_normal(uu - eps, R, a)
    ) / (2.0 * eps)
    r_u = rp + vv[:, None] * n_p
    len_u = np.linalg.norm(r_u, axis=-1) * du
    len_v = np.full_like(len_u, abs(dv))
    areas = np.linalg.norm(np.cross(r_u, n), axis=-1) * du * abs(dv)
    # Guard against rare FD spikes; thin-ribbon fallback: speed * du * dv
    speed = np.linalg.norm(rp, axis=-1)
    fallback = speed * du * abs(dv)
    bad = ~np.isfinite(areas) | (areas <= 0.0) | (areas > 50.0 * fallback)
    areas = np.where(bad, fallback, areas)
    len_u = np.where(bad, speed * du, len_u)
    pnl_n = np.cross(r_u, n)
    pnl_n /= np.linalg.norm(pnl_n, axis=-1, keepdims=True)
    return centroids, areas, np.stack([len_u, len_v], axis=-1), pnl_n


def bie_mobius_C(
    R: float,
    a: float,
    n_u: int = 64,
    n_v: int = 8,
    half_width: float | None = None,
) -> float:
    """
    Constant-panel collocation BIE capacitance of a Möbius ribbon in R^3.

    Single-layer potential on a thin conducting sheet at unit potential:
      1 = (1/(4 pi eps0)) ∫_S sigma(r') / |r - r'| dA'
    C = Q / V with V=1, Q = ∫ sigma dA.

    Self terms use the analytic rectangular-panel integral; off-diagonal
    nearfield uses 2x2 Gauss quadrature; far field uses centroid rule.
    Lengths are nondimensionalized by R for conditioning, then C is scaled
    back to SI: C = C_hat * eps0 * R.

    Disk/memory memo keyed by (R, a, n_u, n_v, model, half_width).
    """
    if a <= 0.0 or R <= 0.0:
        raise ValueError("R and a must be positive")
    if n_u < 4 or n_v < 2:
        raise ValueError("n_u >= 4 and n_v >= 2 required")

    hw_key = "a" if half_width is None else fmt_float(half_width)
    parts = (
        fmt_float(R),
        fmt_float(a),
        int(n_u),
        int(n_v),
        "bie_mobius_sheet",
        hw_key,
    )

    def _compute() -> float:
        return _bie_mobius_C_uncached(R, a, n_u=n_u, n_v=n_v, half_width=half_width)

    return float(cached_json("bie_capacitance", parts, _compute))


def _bie_mobius_C_uncached(
    R: float,
    a: float,
    n_u: int = 64,
    n_v: int = 8,
    half_width: float | None = None,
) -> float:
    # Work in units of R
    a_hat = a / R
    w_hat = (a if half_width is None else half_width) / R
    cents, areas, edges, _ = _ribbon_panels(1.0, a_hat, n_u, n_v, half_width=w_hat)
    n_pan = cents.shape[0]

    # Dimensionless kernel K = 1/(4 pi |r-r'|); A @ sigma_hat = 1
    A = np.zeros((n_pan, n_pan), dtype=float)
    # Gauss-Legendre nodes on [-1,1]
    g_pts = np.array([-0.5773502691896257, 0.5773502691896257])
    g_wts = np.array([1.0, 1.0])

    for j in range(n_pan):
        cj = cents[j]
        lx, ly = float(edges[j, 0]), float(edges[j, 1])
        # local orthonormal frame for panel j (approximate flat)
        # recover edges along u,v from neighbour structure is costly; use
        # length-based isotropic self term + quadrature with artificial axes
        for i in range(n_pan):
            if i == j:
                # analytic self-panel (rectangle lx x ly)
                A[i, j] = _rect_self_integral(lx, ly) / (4.0 * math.pi)
                continue
            d = cents[i] - cj
            dist = float(np.linalg.norm(d))
            char = 0.5 * (lx + ly)
            if dist > 4.0 * char:
                A[i, j] = areas[j] / (4.0 * math.pi * dist)
            else:
                # 2x2 quadrature in a local tangent plane approx
                # build local axes from a stable complement to panel normal proxy
                # use vector from centroid to collocation projected... simpler:
                # integrate over rectangle in plane spanned by e1,e2
                # Estimate e1 along the longest edge direction via SVD of
                # displacement — use fixed construction from d and a helper.
                helper = np.array([0.0, 0.0, 1.0])
                if abs(d[2]) > 0.9 * dist and dist > 0.0:
                    helper = np.array([1.0, 0.0, 0.0])
                # For near field without true panel axes, use circularized
                # singularity-subtracted centroid: ∫(1/|r-r'| - 1/|r-c|) + area/|r-c|
                # with 2x2 samples on a parallelogram of sides lx, ly.
                e1 = d / dist if dist > 0 else np.array([1.0, 0.0, 0.0])
                e2 = np.cross(helper, e1)
                e2n = np.linalg.norm(e2)
                if e2n < 1e-14:
                    e2 = np.array([0.0, 1.0, 0.0])
                else:
                    e2 /= e2n
                e1p = np.cross(e2, e1)  # not used as normal; need in-plane pair
                # Better in-plane basis at source panel: use world axes projected —
                # approximate panel as rectangle in plane ⟂ connecting line for
                # isotropic nearfield (adequate for capacitance scan accuracy).
                # Use two orthogonal directions perpendicular to an estimated normal.
                n_est = np.cross(e1, e2)
                nn = np.linalg.norm(n_est)
                if nn < 1e-14:
                    n_est = np.array([0.0, 0.0, 1.0])
                else:
                    n_est /= nn
                t1 = np.cross(n_est, helper)
                t1n = np.linalg.norm(t1)
                if t1n < 1e-14:
                    t1 = np.array([1.0, 0.0, 0.0])
                else:
                    t1 /= t1n
                t2 = np.cross(n_est, t1)
                acc = 0.0
                for gu, wu in zip(g_pts, g_wts):
                    for gv, wv in zip(g_pts, g_wts):
                        # map [-1,1]^2 → rectangle
                        p = cj + 0.5 * lx * gu * t1 + 0.5 * ly * gv * t2
                        rij = float(np.linalg.norm(cents[i] - p))
                        if rij < 1e-15:
                            continue
                        acc += wu * wv / rij
                A[i, j] = acc * (0.25 * lx * ly) / (4.0 * math.pi)

    # Solve A sigma_hat = 1
    ones = np.ones(n_pan)
    try:
        sigma_hat = np.linalg.solve(A, ones)
    except np.linalg.LinAlgError:
        sigma_hat, *_ = np.linalg.lstsq(A, ones, rcond=None)
    Q_hat = float(np.sum(sigma_hat * areas))
    if not math.isfinite(Q_hat) or Q_hat <= 0.0:
        # fallback: Tikhonov ridge for ill-conditioned thin-ribbon regimes
        ridge = 1e-10 * np.trace(A) / n_pan
        sigma_hat = np.linalg.solve(A + ridge * np.eye(n_pan), ones)
        Q_hat = float(np.sum(sigma_hat * areas))
    C_hat = Q_hat  # V=1
    return C_hat * EPS0 * R


# ---------------------------------------------------------------------------
# Scans and reporting
# ---------------------------------------------------------------------------

def scan_aspect_ratios(
    a_over_R: np.ndarray | list[float] | None = None,
    R: float = R_SPIN,
    cover: int = 2,
    n_u: int = 48,
    n_v: int = 6,
    bie_max_a_over_R: float = 0.25,
    bie_min_a_over_R: float = 5e-3,
) -> dict[str, Any]:
    """
    Grid over a/R; report alpha^{-1} for annulus vs conformal vs BIE.

    BIE is restricted to a moderate aspect window where the panel mesh
    resolves the half-width (extreme CODATA-matching a/R for the log-ring
    models are ~1e-118 and are not BIE-resolvable).
    """
    if a_over_R is None:
        # log grid for analytics + denser moderate band for BIE
        a_over_R = np.unique(
            np.concatenate(
                [
                    np.logspace(-4, -0.5, 16),
                    np.logspace(-2.5, -0.6, 12),
                ]
            )
        )
    a_over_R = np.asarray(a_over_R, dtype=float)

    rows: list[dict[str, Any]] = []
    for ar in a_over_R:
        a = ar * R
        C_ann = annulus_C(R, a)
        C_conf = conformal_annulus_C(R, a, cover=cover)
        row: dict[str, Any] = {
            "a_over_R": float(ar),
            "C_annulus_F": C_ann,
            "C_conformal_F": C_conf,
            "alpha_inv_annulus": alpha_from_C(C_ann, R),
            "alpha_inv_conformal": alpha_from_C(C_conf, R),
            "alpha_inv_annulus_closed_form": annulus_alpha_inv(R, a),
            "bie_computed": False,
            "C_bie_F": None,
            "alpha_inv_bie": None,
        }
        if bie_min_a_over_R <= ar <= bie_max_a_over_R:
            try:
                C_bie = bie_mobius_C(R, a, n_u=n_u, n_v=n_v)
                row["bie_computed"] = True
                row["C_bie_F"] = C_bie
                row["alpha_inv_bie"] = alpha_from_C(C_bie, R)
            except Exception as exc:  # noqa: BLE001 — report failure in row
                row["bie_error"] = str(exc)
        rows.append(row)

    def best_match(key: str) -> dict[str, Any]:
        valid = [r for r in rows if r.get(key) is not None and math.isfinite(r[key])]
        if not valid:
            return {"status": "no_samples", "key": key}
        best = min(valid, key=lambda r: abs(r[key] - ALPHA_INV_CODATA))
        return {
            "status": "ok",
            "a_over_R": best["a_over_R"],
            "alpha_inv": best[key],
            "abs_err_vs_codata": abs(best[key] - ALPHA_INV_CODATA),
            "rel_err_vs_codata": abs(best[key] - ALPHA_INV_CODATA) / ALPHA_INV_CODATA,
            "note": (
                "best on scanned grid only; annulus/conformal analytic match "
                "to CODATA requires extreme a/R outside BIE-valid regime"
                if key != "alpha_inv_bie"
                else "best on BIE-valid aspect window only"
            ),
        }

    # Analytic exact match for annulus (closed form)
    aR_exact = annulus_a_over_R_for_alpha(ALPHA_INV_CODATA)
    annulus_exact = {
        "a_over_R": aR_exact,
        "alpha_inv": ALPHA_INV_CODATA,
        "note": (
            "annulus closed form (ln(8R/a)+1)/2 matches CODATA at this "
            f"extreme a/R={aR_exact:.6e}; not a geometric prediction of a"
        ),
    }

    # Conformal: root-find a/R for CODATA on a log bracket
    conf_exact = _conformal_match_codata(R, cover)

    return {
        "R_m": R,
        "R_description": "hbar/(2 m_e c)",
        "cover": cover,
        "bie_mesh": {"n_u": n_u, "n_v": n_v},
        "bie_aspect_window": {"min": bie_min_a_over_R, "max": bie_max_a_over_R},
        "codata_alpha_inv": ALPHA_INV_CODATA,
        "rows": rows,
        "best_on_grid": {
            "annulus": best_match("alpha_inv_annulus"),
            "conformal": best_match("alpha_inv_conformal"),
            "bie": best_match("alpha_inv_bie"),
        },
        "analytic_codata_match": {
            "annulus": annulus_exact,
            "conformal": conf_exact,
        },
    }


def _conformal_match_codata(R: float, cover: int) -> dict[str, Any]:
    """Find a/R such that conformal_annulus_C yields CODATA alpha^{-1}."""
    target_C = C_from_alpha_inv(ALPHA_INV_CODATA, R)

    def f(log_ar: float) -> float:
        ar = math.exp(log_ar)
        return conformal_annulus_C(R, ar * R, cover=cover) - target_C

    # Bracket: small a => small C => large alpha_inv; large a => large C.
    # Floor above underflow of a_eff = R_m * sinh(a/(cover R)) in float64.
    lo, hi = math.log(1e-300), math.log(0.5)
    try:
        flo, fhi = f(lo), f(hi)
    except ValueError as exc:
        return {
            "status": "bracket_eval_failed",
            "note": str(exc),
        }
    if not (math.isfinite(flo) and math.isfinite(fhi)):
        return {
            "status": "non_finite_bracket",
            "note": "conformal C non-finite on CODATA bracket endpoints",
            "f_lo": flo,
            "f_hi": fhi,
        }
    if flo * fhi > 0:
        return {
            "status": "no_root_in_bracket",
            "note": "conformal model did not cross CODATA C in a/R in (1e-300, 0.5)",
            "f_lo": flo,
            "f_hi": fhi,
        }
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    ar = math.exp(0.5 * (lo + hi))
    C = conformal_annulus_C(R, ar * R, cover=cover)
    return {
        "status": "ok",
        "a_over_R": ar,
        "C_F": C,
        "alpha_inv": alpha_from_C(C, R),
        "note": "root of conformal model vs CODATA; typically extreme a/R",
    }


def _comparison_table(scan: dict[str, Any]) -> list[dict[str, Any]]:
    """Compact table rows for stdout / JSON."""
    table = []
    for r in scan["rows"]:
        table.append(
            {
                "a_over_R": r["a_over_R"],
                "alpha_inv_annulus": r["alpha_inv_annulus"],
                "alpha_inv_conformal": r["alpha_inv_conformal"],
                "alpha_inv_bie": r["alpha_inv_bie"],
                "C_annulus_F": r["C_annulus_F"],
                "C_conformal_F": r["C_conformal_F"],
                "C_bie_F": r["C_bie_F"],
            }
        )
    return table


def main() -> int:
    R = R_SPIN
    # Representative moderate aspect for a worked example + full scan
    a_demo = 0.05 * R

    C_ann = annulus_C(R, a_demo)
    C_conf = conformal_annulus_C(R, a_demo, cover=2)
    C_bie = bie_mobius_C(R, a_demo, n_u=48, n_v=6)

    scan = scan_aspect_ratios(R=R, cover=2, n_u=40, n_v=5)

    summary: dict[str, Any] = {
        "scope": DOC_SCOPE,
        "constants": {
            "eps0": EPS0,
            "hbar": HBAR,
            "m_e": M_E,
            "c": C_LIGHT,
            "e": E_CHARGE,
            "R_spin_m": R,
            "alpha_inv_codata": ALPHA_INV_CODATA,
            "precision": "float64 / scipy.constants",
        },
        "formulas": {
            "annulus_C": "2*pi*eps0*R / (ln(8R/a) + 1)",
            "conformal_annulus_C": (
                "strip L=cover*2*pi*R, W=2a; rho=exp(2a/(cover*R)); "
                "R_m=cover*R; a_eff=(r_out-r_in)/2; "
                "C=2*pi*eps0*R_m/(ln(8 R_m/a_eff)+1)"
            ),
            "bie_mobius_C": (
                "constant-panel single-layer BIE on Möbius ribbon about (2,1) "
                "centerline; C=Q/V at V=1 with regularized self-panel terms"
            ),
            "alpha_from_C": "pi*eps0*R/C  <=>  (e/2)^2/(2C)=m_e c^2",
            "centerline": (
                "r(t)=((R+a cos t)cos 2t, (R+a cos t)sin 2t, a sin t), t in [0,2pi)"
            ),
        },
        "demo_point": {
            "a_over_R": 0.05,
            "C_annulus_F": C_ann,
            "C_conformal_F": C_conf,
            "C_bie_F": C_bie,
            "alpha_inv_annulus": alpha_from_C(C_ann, R),
            "alpha_inv_conformal": alpha_from_C(C_conf, R),
            "alpha_inv_bie": alpha_from_C(C_bie, R),
            "conformal_diagnostics": conformal_modulus_report(R, a_demo, cover=2),
        },
        "comparison_table": _comparison_table(scan),
        "best_on_grid": scan["best_on_grid"],
        "analytic_codata_match": scan["analytic_codata_match"],
        "scan_meta": {
            "bie_mesh": scan["bie_mesh"],
            "bie_aspect_window": scan["bie_aspect_window"],
        },
    }

    # Sanity: finite positive capacitances
    for name, val in [("annulus", C_ann), ("conformal", C_conf), ("bie", C_bie)]:
        if not (math.isfinite(val) and val > 0.0):
            print(f"ERROR: non-positive C for {name}: {val}", file=sys.stderr)
            return 1

    out_path = Path(__file__).resolve().parents[2] / "docs" / "capacitance_ribbon_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, allow_nan=False)
        fh.write("\n")

    # Human-readable stdout summary (+ full JSON)
    print("Möbius-ribbon capacitance sequel — as-implemented model outputs")
    print(f"R = hbar/(2 m_e c) = {R:.6e} m")
    print(f"CODATA-style alpha^{{-1}} reference = {ALPHA_INV_CODATA:.9f}")
    print()
    print("Demo a/R = 0.05")
    print(f"  annulus:    C={C_ann:.6e} F   alpha^{{-1}}={alpha_from_C(C_ann, R):.6f}")
    print(f"  conformal:  C={C_conf:.6e} F   alpha^{{-1}}={alpha_from_C(C_conf, R):.6f}")
    print(f"  BIE:        C={C_bie:.6e} F   alpha^{{-1}}={alpha_from_C(C_bie, R):.6f}")
    print()
    print("Comparison table (alpha^{-1}):")
    print(f"{'a/R':>12}  {'annulus':>12}  {'conformal':>12}  {'BIE':>12}")
    for row in summary["comparison_table"]:
        bie_s = f"{row['alpha_inv_bie']:.6f}" if row["alpha_inv_bie"] is not None else "—"
        print(
            f"{row['a_over_R']:12.4e}  {row['alpha_inv_annulus']:12.6f}  "
            f"{row['alpha_inv_conformal']:12.6f}  {bie_s:>12}"
        )
    print()
    print("Best on scanned grid vs CODATA:")
    for model, info in summary["best_on_grid"].items():
        print(f"  {model}: {info}")
    print()
    print("Analytic CODATA match (annulus / conformal):")
    for model, info in summary["analytic_codata_match"].items():
        print(f"  {model}: {info}")
    print()
    print(f"Wrote {out_path}")
    print(json.dumps(summary, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
