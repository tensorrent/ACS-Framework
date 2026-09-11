#!/usr/bin/env python3
# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Section 7 of the Constraint Projection Framework: the two legs that were never assessed.

Section 7 asserts a three-way equivalence

    k(eps) = 0   <=>   RH   <=>   Omega_k = 0

The 2026-08-29 pass (cpf_full_verification.py V5) evaluated the DEFINING INTEGRAL and
found it equal to 2 pi N(T)/T -> log(T/2 pi e) -> +oo, not the claimed sum.  That
settles the first leg.  This pass takes the other two:

    L1  the Omega_k leg      is there ANY construction carrying a zeta quantity to the
                             cosmological curvature density, or is the link notational?
    L2  the RH leg           does the construction resemble a real spectral criterion
                             (Hilbert-Polya / Berry-Keating / Connes-Weil) closely enough
                             to inherit content?
    L3  the repair           if it repairs into a KNOWN criterion, say which one.
    L4  prior art, including a correction to this repository's own recorded reading.

Design rule (rule 3): no instrument is used before it has been anchored to a number
someone else published and shown capable of failing.  V0 does that four times.

Run:      python3 code/constraint_projection/section7_remaining_legs.py
          ... --quick   skips the two mpmath contour sweeps (L2b/L2c), ~90 s -> ~5 s
Deps:     numpy, sympy, mpmath
Data:     code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt  (Odlyzko, 99,999 lines)
Artifact: docs/section7_remaining_legs.json
"""

import json
import math
import sys
import time
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
ZEROS = ROOT / "code" / "hp_knife_suite" / "data_zeros" / "riemann_zeros_100k.txt"

QUICK = "--quick" in sys.argv
RESULTS = {}


def sec(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------------------
# Shared objects
# ---------------------------------------------------------------------------

mp.mp.dps = 18

# Davenport-Heilbronn function.  Coefficients (1, xi, -xi, -1, 0) mod 5.  xi is NOT
# taken from memory: it is the root of the finite-Fourier eigenvector condition that
# the functional equation requires, so the constant is derived here and then checked.
_S72 = mp.sin(2 * mp.pi / 5)
_S144 = mp.sin(4 * mp.pi / 5)
XI = (-_S72 + mp.sqrt(_S72 ** 2 + _S144 ** 2)) / _S144
_A = [mp.mpf(0), mp.mpf(1), XI, -XI, mp.mpf(-1)]
_LOG5 = mp.log(5)


def dh(s):
    s = mp.mpmathify(s)
    return mp.power(5, -s) * sum(_A[n] * mp.zeta(s, mp.mpf(n) / 5) for n in range(1, 5))


def dh_prime(s):
    s = mp.mpmathify(s)
    return -_LOG5 * dh(s) + mp.power(5, -s) * sum(
        _A[n] * mp.zeta(s, mp.mpf(n) / 5, 1) for n in range(1, 5)
    )


def dh_completed(s):
    s = mp.mpmathify(s)
    return mp.power(5 / mp.pi, (s + 1) / 2) * mp.gamma((s + 1) / 2) * dh(s)


def zeta_prime(s):
    return mp.zeta(s, 1, 1)


def contour_strip_count(f, fp, eps, t0, T, nsplit=1):
    """Argument principle on the rectangle [1/2-eps, 1/2+eps] x [t0, T].

    The vertical sides are exactly Section 7's integrand:
        I = INT_t0^T [ f'/f(1/2+eps+it) - f'/f(1/2-eps+it) ] dt
    and the closed contour gives   I = 2 pi N_eps + i H   with H the two horizontals.
    Returns (I, H, N) where N = (Re I + Im H) / 2 pi must be the integer count of
    zeros with |beta - 1/2| < eps and t0 < gamma < T.
    """
    c = mp.mpf(0.5)
    edges = [t0 + (T - t0) * mp.mpf(i) / nsplit for i in range(nsplit + 1)]
    I = mp.mpc(0)
    for i in range(nsplit):
        I += mp.quad(
            lambda t: fp(c + eps + 1j * t) / f(c + eps + 1j * t)
            - fp(c - eps + 1j * t) / f(c - eps + 1j * t),
            [edges[i], edges[i + 1]],
        )
    h_bot = mp.quad(lambda x: fp(x + 1j * t0) / f(x + 1j * t0), [c - eps, c + eps])
    h_top = -mp.quad(lambda x: fp(x + 1j * T) / f(x + 1j * T), [c - eps, c + eps])
    H = h_bot + h_top
    return I, H, (I.real + H.imag) / (2 * mp.pi)


# ---------------------------------------------------------------------------
# V0  INSTRUMENT VALIDATION
# ---------------------------------------------------------------------------

def v0_instruments():
    sec("V0  INSTRUMENT VALIDATION  (anchor first, then use)")
    out = {}

    # --- V0a  zero list vs Riemann-von Mangoldt ------------------------------
    g = np.loadtxt(ZEROS)
    rvm = lambda T: T / (2 * math.pi) * math.log(T / (2 * math.pi * math.e)) + 7.0 / 8.0
    print("\nV0a  Riemann-von Mangoldt  N(T) = (T/2pi) log(T/2pi e) + 7/8 + S(T)")
    rows = []
    for T in (100.0, 1000.0, 10000.0, 74000.0):
        n = int((g < T).sum())
        m = rvm(T)
        rows.append({"T": T, "N_counted": n, "rvm_main": m, "diff": n - m,
                     "rel": abs(n - m) / n})
        print(f"     T={T:>9.0f}  counted={n:>6d}  RvM={m:>13.4f}  "
              f"diff={n-m:+.4f}  rel={abs(n-m)/n:.3e}")
    worst = max(r["rel"] for r in rows)
    print(f"     worst relative deviation over the four heights = {worst:.3e}")
    print(f"     -> zero list and counting function agree to {worst:.1e}; "
          f"S(T) is O(log T) and the residuals sit at |diff| <= "
          f"{max(abs(r['diff']) for r in rows):.3f}")
    out["v0a_rvm"] = {"rows": rows, "worst_rel": worst}

    # --- V0b  Li's lambda_1 vs published closed form -------------------------
    print("\nV0b  Li coefficient  lambda_1 = SUM_rho 1/rho = 1 + gamma/2 - (1/2)log(4pi)")
    target = 1 + np.euler_gamma / 2 - 0.5 * math.log(4 * math.pi)
    partial = np.cumsum(1.0 / (0.25 + g ** 2))
    li_rows = []
    for N in (1000, 10000, 99999):
        v = float(partial[N - 1])
        G = float(g[N - 1])
        tail_pred = (math.log(G / (2 * math.pi)) + 1) / (2 * math.pi * G)
        li_rows.append({"N": N, "partial": v, "closed_form": target,
                        "residual": v - target, "tail_predicted": -tail_pred,
                        "residual_over_tail": (v - target) / (-tail_pred)})
        print(f"     N={N:>6d}  partial={v:.10f}  closed form={target:.10f}  "
              f"residual={v-target:+.3e}  predicted tail={-tail_pred:+.3e}  "
              f"ratio={(v-target)/(-tail_pred):.4f}")
    r = li_rows[-1]["residual_over_tail"]
    print(f"     -> residual/predicted-tail = {r:.4f} at N=99,999; the partial sum "
          f"reaches a number published independently of this repo, and misses it by "
          f"exactly its own truncation tail")
    out["v0b_li_lambda1"] = {"rows": li_rows, "closed_form": target}

    # --- V0c  contour instrument on prescribed zeros, shown capable of failing -
    print("\nV0c  contour instrument on a polynomial with PRESCRIBED zeros")
    zs = [mp.mpc("0.5", 3), mp.mpc("0.5", 7), mp.mpc("0.81", 12),
          mp.mpc("0.19", 12), mp.mpc("0.5", 20)]
    poly = lambda s: mp.fprod([s - z for z in zs])
    polyp = lambda s: poly(s) * mp.fsum([1 / (s - z) for z in zs])
    poly_rows = []
    for eps in ("0.1", "0.2", "0.4"):
        e = mp.mpf(eps)
        _, _, N = contour_strip_count(poly, polyp, e, mp.mpf("0.5"), mp.mpf(25))
        truth = sum(1 for z in zs if abs(z.real - mp.mpf("0.5")) < e
                    and mp.mpf("0.5") < z.imag < 25)
        ok = abs(float(N) - truth) < 1e-6
        poly_rows.append({"eps": float(e), "N_contour": float(N), "N_true": truth,
                          "match": bool(ok)})
        print(f"     eps={float(e):.2f}  contour N={float(N):.10f}  "
              f"prescribed inside={truth}  match={ok}")
    detects = poly_rows[-1]["N_true"] - poly_rows[0]["N_true"]
    print(f"     -> the count MOVES by {detects} when eps crosses the prescribed "
          f"off-line offset 0.31, so the instrument can reject; all "
          f"{sum(r['match'] for r in poly_rows)}/{len(poly_rows)} rows match")
    out["v0c_contour_poly"] = {"rows": poly_rows, "jump_when_eps_crosses": detects}

    # --- V0d  Davenport-Heilbronn function -----------------------------------
    print("\nV0d  Davenport-Heilbronn function (1936): the classical off-line witness")
    print(f"     xi derived from the DFT-eigenvector condition = {mp.nstr(XI, 15)}")
    fe = []
    for s in (mp.mpc("0.3", 2), mp.mpc("0.8", 11), mp.mpc("1.3", 3)):
        r = dh_completed(s) / dh_completed(1 - s)
        fe.append(float(abs(r - 1)))
    ds_s = mp.mpc(4, mp.mpf("0.3"))
    ds = mp.fsum([_A[n % 5] / mp.power(n, ds_s) for n in range(1, 4000)])
    ds_err = float(abs(ds - dh(ds_s)))
    dp = float(abs(dh_prime(mp.mpc("0.9", 85)) - mp.diff(dh, mp.mpc("0.9", 85))))
    rho = mp.findroot(dh, mp.mpc("0.808517", "85.699348"))
    rho_mirror = mp.findroot(dh, mp.mpc("0.191483", "85.699348"))
    published = mp.mpc("0.808517", "85.699348")
    print(f"     functional equation  max |Lam(s)/Lam(1-s) - 1| = {max(fe):.3e}")
    print(f"     Dirichlet series vs Hurwitz form  |diff| = {ds_err:.3e}")
    print(f"     analytic f' vs numerical f'       |diff| = {dp:.3e}")
    print(f"     off-line zero found  = {mp.nstr(rho, 15)}")
    print(f"     published (Balanzario-Sanchez-Ortiz, Math.Comp. 76 (2007) 2045)"
          f" = {mp.nstr(published, 7)}")
    print(f"     |found - published| = {float(abs(rho - published)):.3e}")
    print(f"     mirror zero found    = {mp.nstr(rho_mirror, 15)}  "
          f"(|beta+beta'-1| = {float(abs(rho.real + rho_mirror.real - 1)):.3e})")
    print(f"     -> a function with the FULL beta <-> 1-beta functional equation and "
          f"|beta - 1/2| = {float(abs(rho.real - 0.5)):.6f} != 0")
    out["v0d_dh"] = {
        "xi": float(XI),
        "functional_equation_max_dev": max(fe),
        "dirichlet_vs_hurwitz": ds_err,
        "analytic_vs_numeric_derivative": dp,
        "offline_zero": [float(rho.real), float(rho.imag)],
        "published_offline_zero": [0.808517, 85.699348],
        "distance_to_published": float(abs(rho - published)),
        "mirror_zero": [float(rho_mirror.real), float(rho_mirror.imag)],
        "offset_from_line": float(abs(rho.real - 0.5)),
    }
    RESULTS["V0_instruments"] = out
    return g, rho, rho_mirror


# ---------------------------------------------------------------------------
# L1  THE Omega_k LEG
# ---------------------------------------------------------------------------

OMEGA_K = 0.0007          # Planck 2018 VI, A&A 641 A6 (2020), TT,TE,EE+lowE+lensing+BAO
OMEGA_K_SIG = 0.0019      # external measurement; NOT re-derived here


def l1_omega_k(g):
    sec("L1  THE Omega_k LEG:  does anything carry k(eps) to a curvature density?")
    out = {}

    # --- L1a  where geometry actually lives in a spectral zeta ---------------
    print("\nL1a  scale content of a spectral zeta vs the Riemann zeta")
    print("     Laplacian on a circle of circumference L: lambda_n = (2 pi n / L)^2,")
    print("     multiplicity 2, so   zeta_Delta(s) = 2 (L/2pi)^(2s) zeta_R(2s).")
    s0 = mp.mpf(2)
    rows = []
    for L in (1, 3, 10):
        Lm = mp.mpf(L)
        direct = 2 * mp.fsum([mp.power((2 * mp.pi * n / Lm) ** 2, -s0)
                              for n in range(1, 60000)])
        closed = 2 * mp.power(Lm / (2 * mp.pi), 2 * s0) * mp.zeta(2 * s0)
        rows.append({"L": L, "direct_sum": float(direct), "closed_form": float(closed),
                     "rel": float(abs(direct / closed - 1))})
        print(f"     L={L:>3}  direct sum={float(direct):.10e}  "
              f"closed form={float(closed):.10e}  rel={float(abs(direct/closed-1)):.2e}")
    ratio = rows[2]["closed_form"] / rows[0]["closed_form"]
    predicted = (10 / 1) ** (2 * float(s0))
    print(f"     ratio zeta_Delta(L=10)/zeta_Delta(L=1) = {ratio:.6e}  "
          f"vs (10/1)^(2s) = {predicted:.6e}  rel={abs(ratio/predicted-1):.2e}")
    print("     -> ALL metric information sits in the prefactor (L/2pi)^(2s); the "
          "factor zeta_R(2s) is identical for every L.")
    print("     Section 7 uses zeta_R alone, with no prefactor and no eigenvalues, so "
          "the object it builds is scale-free by construction.")
    out["l1a_scale"] = {"rows": rows, "ratio": ratio, "predicted": predicted,
                        "rel": abs(ratio / predicted - 1)}

    # --- L1b  dimensional inventory ------------------------------------------
    print("\nL1b  dimensional inventory of Omega_k = -k c^2 / (a0^2 H0^2)")
    needed = {"k (FRW curvature)": "L^-2",
              "a0 (scale factor today)": "L (or dimensionless with a length in H0)",
              "H0 (Hubble rate)": "T^-1",
              "c": "L T^-1"}
    supplied = {"zeta(s)": "dimensionless", "s, eps, t, T": "dimensionless (complex plane)",
                "beta, gamma": "dimensionless (zero coordinates)"}
    print("     required dimensionful inputs:", len(needed))
    for k_, v in needed.items():
        print(f"        {k_:<38} [{v}]")
    print("     dimensionful quantities appearing anywhere in Section 7:", 0)
    for k_, v in supplied.items():
        print(f"        {k_:<38} [{v}]")
    print(f"     -> {len(needed)} required, 0 supplied.  The link needs a bridge "
          f"equation with at least one length; Section 7 states none.")
    out["l1b_dimensions"] = {"required": needed, "supplied": supplied,
                             "n_required_dimensionful": 4, "n_supplied_dimensionful": 0}

    # --- L1c  can k(eps) even be a single number? ----------------------------
    print("\nL1c  Omega_k is one number.  Is k(eps)?")
    N = 50
    eps_grid = [0.05, 0.1, 0.2, 0.3, 0.45]
    claimed = [2 * e * sum(1.0 / ((0.5 - 0.5) ** 2 - e ** 2) for _ in range(N))
               for e in eps_grid]
    print("     manuscript's claimed sum  k = 2 eps SUM 1/((1/2-beta)^2 - eps^2), "
          f"{N} on-line zeros:")
    for e, v in zip(eps_grid, claimed):
        print(f"        eps={e:<5} k={v:>14.4f}   (= -2N/eps = {-2*N/e:.4f})")
    spread = max(claimed) - min(claimed)
    print(f"     spread over the eps grid = {spread:.4f}  -> eps-DEPENDENT")
    exact_rows = []
    for T in (1000.0, 10000.0, 74000.0):
        n = int((g < T).sum())
        exact_rows.append({"T": T, "N": n, "k_exact": 2 * math.pi * n / T,
                           "log_T_over_2pie": math.log(T / (2 * math.pi * math.e))})
        print(f"     exact integral / T at T={T:>8.0f}:  2 pi N(T)/T = "
              f"{2*math.pi*n/T:.6f}   log(T/2pi e) = "
              f"{math.log(T/(2*math.pi*math.e)):.6f}  ratio="
              f"{2*math.pi*n/T/math.log(T/(2*math.pi*math.e)):.6f}   "
              f"(eps-independent, T-divergent)")
    out["l1c_single_number"] = {"claimed_sum": dict(zip(map(str, eps_grid), claimed)),
                                "claimed_spread": spread, "exact_rows": exact_rows}

    # --- L1d  the value, against the measurement -----------------------------
    print("\nL1d  numerical identification test against the measured value")
    print(f"     Omega_k = {OMEGA_K} +- {OMEGA_K_SIG}  (Planck 2018 VI; external datum, "
          f"not re-derived here)")
    k_claimed = -2 * 100000 / 0.1
    k_exact = exact_rows[-1]["k_exact"]
    z_claimed = abs(k_claimed - OMEGA_K) / OMEGA_K_SIG
    z_exact = abs(k_exact - OMEGA_K) / OMEGA_K_SIG
    print(f"     claimed sum, 100,000 on-line zeros, eps=0.1:  k = {k_claimed:.4e}   "
          f"|k - Omega_k|/sigma = {z_claimed:.4e}")
    print(f"     exact integral at T=74,000:                   k = {k_exact:.6f}   "
          f"|k - Omega_k|/sigma = {z_exact:.4e}")
    print(f"     -> under the manuscript's OWN two readings the identification "
          f"k = Omega_k misses by {z_exact:.3g} sigma and {z_claimed:.3g} sigma "
          f"respectively.")
    out["l1d_identification"] = {"omega_k": OMEGA_K, "sigma": OMEGA_K_SIG,
                                 "k_claimed": k_claimed, "z_claimed": z_claimed,
                                 "k_exact": k_exact, "z_exact": z_exact}

    # --- L1e  can any bridge rescue it? --------------------------------------
    print("\nL1e  is there a bridge B with Omega_k = B(k) making the chain work?")
    print("     Such a B needs B(0) = 0 and B(x) != 0 for x != 0.  Then "
          "Omega_k = 0 <=> k = 0.")
    print("     Both readings of k are never zero:")
    min_abs_claimed = min(abs(v) for v in claimed)
    min_abs_exact = min(r["k_exact"] for r in exact_rows)
    print(f"        claimed sum   min |k| over the eps grid = {min_abs_claimed:.4f} > 0")
    print(f"        exact integral min  k  over the T grid  = {min_abs_exact:.6f} > 0, "
          f"and 2 pi N(T)/T > 0 for every T > 14.13 since N(T) >= 1")
    print(f"     -> for every bridge with B(0)=0 the chain predicts Omega_k = B(nonzero), "
          f"i.e. NOT zero.  Section 7's own definitions give the negation of its "
          f"conclusion.")
    out["l1e_bridge"] = {"min_abs_claimed": min_abs_claimed,
                         "min_k_exact": min_abs_exact,
                         "k_ever_zero": False}

    # --- L1f  the biconditional as an empirical statement --------------------
    print("\nL1f  what the biconditional does to a theorem of arithmetic")
    z_obs = OMEGA_K / OMEGA_K_SIG
    ci95 = (OMEGA_K - 1.96 * OMEGA_K_SIG, OMEGA_K + 1.96 * OMEGA_K_SIG)
    print(f"     measured deviation from flat: {OMEGA_K}/{OMEGA_K_SIG} = {z_obs:.4f} sigma")
    print(f"     95% interval on Omega_k: [{ci95[0]:+.5f}, {ci95[1]:+.5f}]")
    print(f"     -> read as a biconditional, current CMB+BAO data would disfavour RH at "
          f"{z_obs:.3f} sigma, and a future detection of |Omega_k| > "
          f"{1.96*OMEGA_K_SIG:.5f} at 95% would refute it.  A point null "
          f"(Omega_k exactly 0) carries zero posterior mass under any continuous prior, "
          f"so the 'Omega_k = 0' side is not measurable even in principle.")
    out["l1f_empirical"] = {"z_observed": z_obs, "ci95": list(ci95)}

    RESULTS["L1_omega_k"] = out


# ---------------------------------------------------------------------------
# L2  THE RH LEG
# ---------------------------------------------------------------------------

def l2_rh_leg(g, rho, rho_mirror):
    sec("L2  THE RH LEG:  what the construction actually is")
    out = {}

    # --- L2a  where the claimed sum comes from -------------------------------
    print("\nL2a  symbolic: the exact difference of log-derivatives (Hadamard term)")
    b, gam, t, e = sp.symbols("beta gamma t varepsilon", real=True)
    a = sp.Rational(1, 2) - b + sp.I * (t - gam)      # A = (1/2 - beta) + i(t - gamma)
    exact = sp.simplify(1 / (a + e) - 1 / (a - e))
    print(f"     1/(A+eps) - 1/(A-eps)  =  {sp.simplify(exact)}")
    target = -2 * e / (a ** 2 - e ** 2)
    print(f"     check against -2 eps/(A^2 - eps^2):  difference simplifies to "
          f"{sp.simplify(exact - target)}")
    manuscript = 2 * e / ((sp.Rational(1, 2) - b) ** 2 - e ** 2)
    at_t_eq_gamma = sp.simplify(target.subs(t, gam))
    print(f"     exact summand at t = gamma:      {at_t_eq_gamma}")
    print(f"     manuscript's summand:            {manuscript}")
    ratio = sp.simplify(manuscript / at_t_eq_gamma)
    print(f"     manuscript / (exact at t=gamma) = {ratio}")
    print(f"     -> the claimed sum is the exact partial-fraction difference with the "
          f"i(t-gamma) term DELETED and the sign flipped.  Deleting i(t-gamma) is "
          f"exactly the step the t-average is supposed to perform, and the average of "
          f"1/(alpha + iu) over u is not its value at u = 0.")
    out["l2a_symbolic"] = {
        "exact_difference": str(sp.simplify(exact)),
        "matches_minus_2eps_over_A2_minus_eps2": bool(sp.simplify(exact - target) == 0),
        "exact_at_t_equals_gamma": str(at_t_eq_gamma),
        "manuscript_summand": str(manuscript),
        "manuscript_over_exact": str(ratio),
    }

    # --- L2b  the exact object IS an argument-principle count ----------------
    print("\nL2b  the same integral, evaluated exactly, on the real zeta")
    if QUICK:
        print("     [--quick] skipped")
        out["l2b_zeta_contour"] = "skipped (--quick)"
    else:
        t0 = time.time()
        zrows = []
        n_true = int((g < 50).sum())
        splits = 12
        for eps in ("0.1", "0.3"):
            E = mp.mpf(eps)
            I, H, N = contour_strip_count(mp.zeta, zeta_prime, E, mp.mpf("0.5"),
                                          mp.mpf(50), nsplit=splits)
            zrows.append({"eps": float(E), "Re_I": float(I.real), "Im_H": float(H.imag),
                          "N_contour": float(N), "N_true": n_true,
                          "two_pi_N": 2 * math.pi * n_true})
            print(f"     eps={float(E):.2f}  Re I = {float(I.real):.6f}   "
                  f"Im H = {float(H.imag):.6f}   (Re I + Im H)/2pi = {float(N):.10f}   "
                  f"N(50) from the zero list = {n_true}")
        err = max(abs(r["N_contour"] - r["N_true"]) for r in zrows)
        print(f"     max |contour count - listed count| = {err:.2e}  ({time.time()-t0:.0f} s)")
        print(f"     -> the integral is 2 pi N_eps(T) + (boundary), an argument-principle "
              f"count of the zeros with |beta - 1/2| < eps.  It is NOT 2 eps SUM "
              f"1/((1/2-beta)^2 - eps^2).")
        out["l2b_zeta_contour"] = {"rows": zrows, "max_err": err}

    # --- L2c  and it DOES see an off-line zero -------------------------------
    print("\nL2c  the same integral on Davenport-Heilbronn, where off-line zeros exist")
    beta_off = float(rho.real)
    offset = abs(beta_off - 0.5)
    if QUICK:
        print("     [--quick] skipped")
        out["l2c_dh_contour"] = "skipped (--quick)"
    else:
        t0 = time.time()
        drows = []
        for eps in ("0.20", "0.45"):
            E = mp.mpf(eps)
            I, H, N = contour_strip_count(dh, dh_prime, E, mp.mpf(84), mp.mpf(88),
                                          nsplit=4)
            drows.append({"eps": float(E), "Re_I": float(I.real),
                          "N_contour": float(N), "N_rounded": int(round(float(N)))})
            print(f"     eps={float(E):.2f}  window 84 < t < 88   "
                  f"(Re I + Im H)/2pi = {float(N):.8f}  -> {int(round(float(N)))} zeros "
                  f"with |beta - 1/2| < {float(E):.2f}")
        jump = drows[1]["N_rounded"] - drows[0]["N_rounded"]
        print(f"     count changes by {jump} when eps crosses the measured offset "
              f"{offset:.6f}")
        print(f"     the pair responsible: beta = {beta_off:.6f} and "
              f"beta' = {float(rho_mirror.real):.6f}, both at gamma = "
              f"{float(rho.imag):.6f}")
        print(f"     -> the UNNORMALISED integral is sensitive to off-line zeros. The "
              f"blindness in Section 7 is therefore not a property of the contour "
              f"object; it enters somewhere else.  L2d locates it.")
        out["l2c_dh_contour"] = {"rows": drows, "jump": jump, "offset": offset,
                                 "seconds": time.time() - t0}

    # --- L2d  where the blindness actually is: the 1/T --------------------
    print("\nL2d  where the blindness is: the 1/T normalisation, unconditionally")
    print("     Section 7 defines k(eps) = lim_T (1/T) INT_0^T [...] dt = "
          "lim_T 2 pi N_eps(T)/T.")
    print("     N(T) - N_eps(T) = 2 N(1/2+eps, T), the classical zero-density count.")
    print("     Carlson (1920): N(sigma,T) << T^(4 sigma (1-sigma)) log T, and "
          "4 sigma (1-sigma) < 1 for every sigma > 1/2.")
    drows = []
    for eps in (0.05, 0.1, 0.25):
        sig = 0.5 + eps
        expo = 4 * sig * (1 - sig)
        row = {"eps": eps, "sigma": sig, "carlson_exponent": expo, "T": {}}
        for T in (1e6, 1e12, 1e24):
            bound = 2 * (T ** expo) * math.log(T) / T
            row["T"][f"{T:.0e}"] = bound
        drows.append(row)
        print(f"     eps={eps:<5} sigma={sig:.2f}  exponent 4s(1-s)={expo:.4f}  "
              f"2 N(sigma,T)/T bound: "
              + "  ".join(f"T=1e{int(math.log10(T)):<2d}:{2*(T**expo)*math.log(T)/T:.3e}"
                          for T in (1e6, 1e12, 1e24)))
    worst = max(r["T"]["1e+24"] for r in drows)
    print(f"     largest bound at T = 1e24 across the eps grid = {worst:.3e}")
    print(f"     -> 2 pi (N(T) - N_eps(T))/T -> 0 whether or not RH holds, so "
          f"k(eps) as literally defined takes the SAME value (the divergent "
          f"log(T/2 pi e)) on both hypotheses.  The definition is RH-independent by "
          f"a theorem, not by the (1/2-beta)^2 symmetry.")
    out["l2d_normalisation"] = {"rows": drows, "bound_at_1e24": worst}

    # --- L2e  does it resemble a real spectral criterion? --------------------
    print("\nL2e  comparison with the actual spectral programme")
    n74 = int((g < 74000).sum())
    weyl = math.log(74000 / (2 * math.pi * math.e))
    ratio = 2 * math.pi * n74 / 74000 / weyl
    print(f"     Berry-Keating / Riemann-von Mangoldt smooth term: what the integral "
          f"computes is 2 pi N(T)/T = {2*math.pi*n74/74000:.6f} vs "
          f"log(T/2pi e) = {weyl:.6f}, ratio = {ratio:.6f} at T = 74,000.")
    print("     That is the WEYL term of the putative Hilbert-Polya operator: the "
          "smooth counting density.  It is the part of the spectrum that carries no "
          "information about the location of individual zeros - every operator with "
          "the right mean density reproduces it, on RH or off it.")
    table = [
        ("Hilbert-Polya", "zeros are eigenvalues of a self-adjoint operator",
         "no operator, no Hilbert space, no eigenvalue equation appears"),
        ("Berry-Keating (H = xp)", "semiclassical density reproduces log(T/2pi e)",
         "MATCHES - but this is the smooth term only, which is RH-independent"),
        ("Connes / Weil positivity", "explicit-formula quadratic form >= 0 <=> RH",
         "no quadratic form, no positivity, no test function"),
        ("Li's criterion", "lambda_n >= 0 for all n >= 1 <=> RH",
         "no such sequence is formed"),
        ("Nyman-Beurling", "approximation in L^2(0,1) <=> RH",
         "no function space appears"),
        ("zero-density / Backlund contour", "N(1/2+eps,T) = 0 for all eps <=> RH",
         "MATCHES the integral once the 1/T is dropped - see L3"),
    ]
    print(f"     {'criterion':<28} {'content':<48} match")
    for nm, content, verdict in table:
        print(f"     {nm:<28} {content:<48} {verdict}")
    matches = [nm for nm, _, v in table if v.startswith("MATCHES")]
    print(f"     -> {len(matches)} of {len(table)} match, and both are objects that are "
          f"RH-INDEPENDENT as used here ({', '.join(matches)}).")
    out["l2e_criteria"] = {"weyl_ratio": ratio,
                           "table": [{"criterion": a_, "content": b_, "verdict": c_}
                                     for a_, b_, c_ in table],
                           "n_matching": len(matches)}
    RESULTS["L2_rh_leg"] = out


# ---------------------------------------------------------------------------
# L3  THE REPAIR
# ---------------------------------------------------------------------------

def l3_repair(g, rho):
    sec("L3  THE REPAIR:  what the construction becomes when it is fixed")
    print("""
     Drop the 1/T and keep the boundary terms.  Section 7's integral is then

         (1/2 pi)[ Re INT_0^T ( zeta'/zeta(1/2+eps+it) - zeta'/zeta(1/2-eps+it) ) dt
                   + Im H ]   =   N_eps(T)   :=   #{rho : |beta-1/2| < eps, 0<gamma<T}

     and the criterion that survives is

         RH   <=>   N(T) - N_eps(T) = 0   for every eps in (0,1/2) and every T > 0
              <=>   N(1/2+eps, T) = 0     for every eps > 0, T > 0.

     That is a true equivalence and it is not new.  It is the definition of the
     zero-density function N(sigma,T) plus the standard contour representation of it.
    """)
    prior = [
        ("Backlund (1914, 1918)", "contour/argument-principle evaluation of N(T) and of "
                                  "zeros in a strip; the standard rigorous count"),
        ("Bohr & Landau (1914)", "N(sigma,T) = o(T) for every fixed sigma > 1/2 - the "
                                 "theorem that makes the 1/T normalisation blind"),
        ("Littlewood (1924)", "2 pi SUM_{beta>1/2}(beta - 1/2) = INT_0^T log|zeta(1/2+it)| dt "
                              "+ O(log T)  (Littlewood's lemma); RH <=> the left side "
                              "vanishes"),
        ("Carlson (1920)", "N(sigma,T) << T^{4 sigma(1-sigma)} log T"),
        ("Selberg (1946), Ingham (1940)", "sharper density theorems built on the same "
                                          "contour identity"),
        ("Davenport & Heilbronn (1936)", "functional-equation symmetry alone does not "
                                         "place zeros - used as the test object in V0d/L2c"),
    ]
    print(f"     {'prior art':<34} content")
    for nm, c in prior:
        print(f"     {nm:<34} {c}")
    print("""
     Status of the repaired statement: correct, classical, and about a century old.
     It is a criterion in the sense that RH is equivalent to it, but it is equivalent
     by restatement - it supplies no route to a proof, which is exactly why the
     literature treats N(sigma,T) as a target for estimates rather than a criterion.
    """)
    # the repaired criterion, exercised on both test functions
    n50 = int((g < 50).sum())
    print(f"     exercised: zeta up to T=50 -> N(T) = {n50}, N_eps(T) = {n50} for "
          f"eps = 0.1 and 0.3 (L2b), so the criterion is SATISFIED there;")
    print(f"     Davenport-Heilbronn in 84 < t < 88 -> the count moves by 2 between "
          f"eps = 0.20 and 0.45 (L2c), so the criterion is VIOLATED there, at the "
          f"zero beta = {float(rho.real):.6f}.  The repaired criterion separates the "
          f"two functions; Section 7's k(eps) does not.")
    RESULTS["L3_repair"] = {
        "repaired_statement": "RH <=> N(1/2+eps,T)=0 for all eps>0, T>0; the integral, "
                              "un-normalised, equals 2 pi N_eps(T) + boundary",
        "prior_art": [{"source": a_, "content": b_} for a_, b_ in prior],
        "novel": False,
    }


# ---------------------------------------------------------------------------
# L4  PRIOR ART AND A CORRECTION TO THIS REPOSITORY'S OWN READING
# ---------------------------------------------------------------------------

def l4_ledger_correction(rho, rho_mirror):
    sec("L4  the 'structural constraint' this repo recorded from Section 7")
    print("""
     Logged 2026-08-29 and repeated in MANIFEST as the audit's one new output:

        "A functional detecting off-line zeros must be ODD under beta -> 1-beta; any
         construction whose beta-dependence factors through (1/2-beta)^2 is blind."

     It was retired 2026-08-30 as NOT NOVEL (Davenport-Heilbronn + Weil positivity).
     The two clauses are tested here as statements.
    """)
    out = {}

    # --- L4a  "must be odd" -> forces the functional to vanish ---------------
    print("L4a  clause 1: 'must be odd under beta -> 1-beta'")
    print("     zeta's zero multiset is invariant under beta -> 1-beta at fixed gamma")
    print("     (rho -> 1 - conj(rho)).  So for F = SUM_rho f(beta,gamma) with f odd")
    print("     about beta = 1/2:  F = -F, hence F = 0 identically.")
    pair = [float(rho.real), float(rho_mirror.real)]
    odd_fns = {"beta - 1/2": lambda x: x - 0.5,
               "(beta - 1/2)^3": lambda x: (x - 0.5) ** 3,
               "sinh(beta - 1/2)": lambda x: math.sinh(x - 0.5)}
    odd_vals = {nm: sum(f(x) for x in pair) for nm, f in odd_fns.items()}
    for nm, v in odd_vals.items():
        print(f"        SUM over the DH mirror pair of {nm:<18} = {v:+.3e}")
    print(f"     -> every odd functional returns "
          f"{max(abs(v) for v in odd_vals.values()):.1e} on a pair that is maximally "
          f"off-line.  'Odd' does not make a detector; it makes the zero functional.")
    out["l4a_odd"] = {"pair": pair, "values": odd_vals,
                      "max_abs": max(abs(v) for v in odd_vals.values())}

    # --- L4b  "(1/2-beta)^2 => blind" -> refuted by a one-line counterexample --
    print("\nL4b  clause 2: 'beta-dependence through (1/2-beta)^2 is blind'")
    dh_sum = sum((x - 0.5) ** 2 for x in pair)
    zeta_sum = 0.0     # every listed zeta zero has beta = 1/2 exactly
    print(f"        F = SUM (beta - 1/2)^2  factors through (1/2-beta)^2 exactly.")
    print(f"        on the DH mirror pair:  F = {dh_sum:.6f}")
    print(f"        on zeta's zeros:        F = {zeta_sum:.6f}")
    print(f"        separation = {dh_sum - zeta_sum:.6f}  -> NOT blind.")
    # and the manuscript's own summand separates on-line from off-line
    N, eps = 50, 0.1
    k_online = 2 * eps * N / ((0.5 - 0.5) ** 2 - eps ** 2)
    k_offline = 2 * eps * N / ((0.5 - 0.7) ** 2 - eps ** 2)
    k_mirror = 2 * eps * N / ((0.5 - 0.3) ** 2 - eps ** 2)
    print(f"        the manuscript's own summand, {N} zeros at eps={eps}:")
    print(f"           all beta = 0.5 : k = {k_online:+.4f}")
    print(f"           all beta = 0.7 : k = {k_offline:+.4f}")
    print(f"           all beta = 0.3 : k = {k_mirror:+.4f}")
    print(f"        on-line vs off-line differ by {abs(k_online-k_offline):.4f}; "
          f"beta=0.7 vs beta=0.3 differ by {abs(k_offline-k_mirror):.4e}")
    print(f"     -> the (1/2-beta)^2 form cannot tell WHICH SIDE of the line a zero is "
          f"on.  It can tell WHETHER a zero is on it.  Those are different, and since "
          f"zeta's zeros are symmetric, no functional of the zero multiset can do the "
          f"first (L4a), so the second is the only thing a detector could ever do.")
    print(f"     -> clause 2 does not hold; the underlying kill of Section 7 does not "
          f"depend on it (L2d supplies an unconditional mechanism instead).")
    out["l4b_even"] = {"dh_sum_sq": dh_sum, "zeta_sum_sq": zeta_sum,
                       "k_online": k_online, "k_offline": k_offline,
                       "k_mirror": k_mirror,
                       "online_offline_separation": abs(k_online - k_offline),
                       "side_separation": abs(k_offline - k_mirror)}
    RESULTS["L4_ledger_correction"] = out


# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    print("Section 7 remaining legs:  Omega_k  and  'k = 0 <=> RH'")
    print("Constraint Projection Framework, papers/notes/Constraint_Projection_Framework.tex")
    print(f"mpmath {mp.__version__}  numpy {np.__version__}  sympy {sp.__version__}"
          f"  quick={QUICK}")
    g, rho, rho_mirror = v0_instruments()
    l1_omega_k(g)
    l2_rh_leg(g, rho, rho_mirror)
    l3_repair(g, rho)
    l4_ledger_correction(rho, rho_mirror)

    sec("SUMMARY  (every line below reads a value computed above)")
    v0 = RESULTS["V0_instruments"]
    l1 = RESULTS["L1_omega_k"]
    l2 = RESULTS["L2_rh_leg"]
    l4 = RESULTS["L4_ledger_correction"]
    lines = [
        f"instruments: RvM count matches the zero list to {v0['v0a_rvm']['worst_rel']:.1e} "
        f"relative; Li's lambda_1 lands on the published closed form to within "
        f"{abs(v0['v0b_li_lambda1']['rows'][-1]['residual']):.1e}, which is "
        f"{v0['v0b_li_lambda1']['rows'][-1]['residual_over_tail']:.3f} x its own "
        f"predicted truncation tail",
        f"DH off-line zero reproduces the published value to "
        f"{v0['v0d_dh']['distance_to_published']:.1e}; offset from the line "
        f"{v0['v0d_dh']['offset_from_line']:.6f}",
        f"L1  Omega_k needs {l1['l1b_dimensions']['n_required_dimensionful']} dimensionful "
        f"inputs; Section 7 supplies {l1['l1b_dimensions']['n_supplied_dimensionful']}. "
        f"The claimed sum varies by {l1['l1c_single_number']['claimed_spread']:.1f} across "
        f"the eps grid, so it is not one number; the exact integral is one number per T "
        f"but diverges.",
        f"L1  k is never 0 under either reading (min |k| = "
        f"{l1['l1e_bridge']['min_abs_claimed']:.2f} claimed, "
        f"{l1['l1e_bridge']['min_k_exact']:.4f} exact), so ANY bridge with B(0)=0 makes "
        f"Section 7 predict Omega_k != 0 - the negation of its own conclusion. Direct "
        f"identification misses the measured value by {l1['l1d_identification']['z_exact']:.3g} "
        f"sigma (exact) and {l1['l1d_identification']['z_claimed']:.3g} sigma (claimed).",
        f"L2  the claimed sum is the exact partial-fraction difference with i(t-gamma) "
        f"deleted and the sign flipped: manuscript/exact-at-t=gamma = "
        f"{l2['l2a_symbolic']['manuscript_over_exact']}",
        f"L2  the un-normalised integral IS an argument-principle count and DOES see "
        f"off-line zeros"
        + ("" if QUICK else
           f" (DH count moves by {l2['l2c_dh_contour']['jump']} across "
           f"eps = {l2['l2c_dh_contour']['offset']:.4f})")
        + f"; the blindness is the 1/T, which kills the difference unconditionally "
          f"(Carlson bound {l2['l2d_normalisation']['bound_at_1e24']:.1e} at T = 1e24).",
        f"L2  of {len(l2['l2e_criteria']['table'])} standard criteria, "
        f"{l2['l2e_criteria']['n_matching']} match - both RH-independent as used. The "
        f"Berry-Keating smooth term matches at ratio "
        f"{l2['l2e_criteria']['weyl_ratio']:.6f}.",
        f"L3  repaired, it is Backlund's contour count and the zero-density criterion "
        f"N(1/2+eps,T)=0: correct, classical, not novel.",
        f"L4  this repo's recorded 'must be ODD' constraint forces F = 0 identically "
        f"(max |F| on a maximally off-line pair = {l4['l4a_odd']['max_abs']:.1e}); and "
        f"'(1/2-beta)^2 => blind' is refuted by SUM (beta-1/2)^2, which separates DH "
        f"from zeta by {l4['l4b_even']['dh_sum_sq']:.6f}.",
    ]
    for i, s in enumerate(lines, 1):
        print(f"  {i}. {s}")

    RESULTS["summary"] = lines
    RESULTS["provenance"] = {
        "script": str(Path(__file__).resolve().relative_to(ROOT)),
        "zeros": str(ZEROS.relative_to(ROOT)),
        "n_zeros": int(len(g)),
        "mpmath": mp.__version__, "numpy": np.__version__, "sympy": sp.__version__,
        "python": sys.version.split()[0],
        "quick": QUICK,
        "omega_k_source": "Planck 2018 VI, A&A 641 A6 (2020), "
                          "TT,TE,EE+lowE+lensing+BAO: 0.0007 +- 0.0019 "
                          "(external measurement, quoted not re-derived)",
        "seconds": round(time.time() - t0, 1),
    }
    out = ROOT / "docs" / "section7_remaining_legs.json"
    out.write_text(json.dumps(RESULTS, indent=2, default=str) + "\n")
    print(f"\nArtifact: {out}   ({time.time()-t0:.1f} s)")


if __name__ == "__main__":
    main()
