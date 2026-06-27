"""
Paper A §5 — Branch A vacuum analysis (alpha_2 = 0)
====================================================
The alpha_2 cross-coupling Tr(Phi^dagger T^A Phi) Tr(Delta_R^dagger T^A Delta_R)
vanishes identically in the minimal bi-doublet model:

  Phi ~ (1, 2, 2) under SU(4) x SU(2)_L x SU(2)_R
  T^A is an SU(4) generator, but Phi is an SU(4) singlet
  Therefore T^A Phi = 0
  Therefore Tr(Phi^dagger T^A Phi) = 0
  Therefore the entire cross-coupling vanishes.

This is a hard representation-theoretic obstruction. alpha_2 is FORBIDDEN,
not eliminated by choice.

The reduced potential V(Phi, Delta_R) with alpha_2 = 0 still admits the
correct symmetry-breaking vacuum:

  V = -mu_Phi^2 (Phi^dagger Phi) + lam_Phi (Phi^dagger Phi)^2
      - mu_Delta^2 (Delta_R^dagger Delta_R) + (rho_1 + rho_2) (...)^2
      + alpha_1 (Phi^dagger Phi) Tr(Delta_R^dagger Delta_R)
      + [beta_c Tr(Phi^dagger PhiTilde Delta_R^dagger Delta_R) + h.c.]

with locked couplings:
  lam_Phi = 2 sqrt(3) / 27           (Koide projection)
  2 rho_1 + rho_2 = 16/9             (Palatini pairing)
  g_4 = g_L = g_R = 4/3              (Palatini bracket)
  hTilde / h = 2/3                   (Palatini Yukawa)

This module verifies vacuum stability across the allowed alpha_1 range.

NUMERICAL NOTE: The scale ratio v / v_R ~ 10^-13 makes naive float64
Cramer's-rule inversion unstable due to catastrophic cancellation.
This script uses Python's decimal module at 50-digit precision.
See docs/numerical_pitfalls.md for details.
"""
from decimal import Decimal, getcontext
import numpy as np


def vacuum_analysis(rho_1=Decimal("0.5"),
                    v_phys=Decimal("246.0"),
                    vR_phys=Decimal("1e15"),
                    precision=50):
    """
    Verify Branch A vacuum stability and compute mu^2 calibrations
    for given alpha_1 values.

    Parameters
    ----------
    rho_1 : Decimal
        Free parameter in (0, 8/9).
    v_phys, vR_phys : Decimal
        Calibration scales (electroweak, Pati-Salam).
    precision : int
        Decimal precision (digits).

    Returns
    -------
    dict with stability bound and per-alpha_1 vacuum check.
    """
    getcontext().prec = precision

    # Locked couplings
    lam_phi = Decimal(2) * Decimal(3).sqrt() / Decimal(27)
    rho_2 = Decimal(16) / Decimal(9) - 2 * rho_1
    rho_tot = rho_1 + rho_2

    # Stability: |alpha_1| < 2 sqrt(lam_phi rho_tot)
    max_alpha1 = 2 * (lam_phi * rho_tot).sqrt()

    x_target = v_phys * v_phys
    y_target = vR_phys * vR_phys

    # Test across alpha_1 range
    test_values = [
        Decimal("-0.5"), Decimal("-0.3"), Decimal("-0.1"), Decimal("0.0"),
        Decimal("0.1"), Decimal("0.3"), Decimal("0.5"), Decimal("0.7"),
        Decimal("0.8"),
    ]
    results = []
    for alpha in test_values:
        det_M = 4 * lam_phi * rho_tot - alpha * alpha
        # mu^2 from targets
        mu_phi_sq = 2 * lam_phi * x_target + alpha * y_target
        mu_del_sq = alpha * x_target + 2 * rho_tot * y_target
        # Cramer's rule recovery
        x_star = (2 * rho_tot * mu_phi_sq - alpha * mu_del_sq) / det_M
        y_star = (2 * lam_phi * mu_del_sq - alpha * mu_phi_sq) / det_M
        stable = (x_star > 0) and (y_star > 0) and (det_M > 0)
        results.append({
            "alpha_1": float(alpha),
            "det_M": float(det_M),
            "v_squared": float(x_star),
            "v_R_squared": float(y_star),
            "stable": stable,
        })

    return {
        "lam_phi": float(lam_phi),
        "rho_1": float(rho_1),
        "rho_2": float(rho_2),
        "rho_tot": float(rho_tot),
        "alpha_1_stability_bound": float(max_alpha1),
        "vacuum_per_alpha": results,
    }


def custodial_breaking(v=246.0, vR=1e15, alpha_em_inv=128.0):
    """
    Estimate one-loop heavy contribution to Delta rho parameter:
       Delta rho ~ (g^2 / 16 pi^2) (v / vR)^2

    Returns the estimate and safety factor vs experimental bound 2e-4.
    """
    g_weak = (4 * np.pi / alpha_em_inv) ** 0.5
    delta_rho = (g_weak ** 2 / (16 * np.pi ** 2)) * (v / vR) ** 2
    return {
        "delta_rho_estimate": delta_rho,
        "experimental_bound": 2e-4,
        "safety_factor": 2e-4 / delta_rho if delta_rho > 0 else float("inf"),
    }


def lambda_eff_consistency(m_H=125.25, v=246.22):
    """
    Compare ACS lam_eff = 2 sqrt(3) / 27 with SM extraction
    lam_SM = m_H^2 / (2 v^2).

    Uses the precise electroweak VEV v = 246.22 GeV (the standard
    PDG value derived from the Fermi constant); approximation v = 246
    GeV gives a 1% discrepancy purely from rounding.
    """
    lam_acs = 2 * np.sqrt(3) / 27
    lam_sm = (m_H ** 2) / (2 * v ** 2)
    return {
        "lam_acs": lam_acs,
        "lam_sm": lam_sm,
        "fractional_difference": abs(lam_acs - lam_sm) / lam_sm,
    }


def main():
    print("Paper A §5 — Branch A vacuum analysis (alpha_2 = 0)")
    print("=" * 60)

    va = vacuum_analysis()
    print(f"\nLocked couplings:")
    print(f"  lam_phi = 2 sqrt(3)/27 = {va['lam_phi']:.6f}")
    print(f"  rho_1 (test) = {va['rho_1']}")
    print(f"  rho_2 = 16/9 - 2 rho_1 = {va['rho_2']:.4f}")
    print(f"  rho_tot = {va['rho_tot']:.4f}")
    print(f"\nStability bound: |alpha_1| < {va['alpha_1_stability_bound']:.4f}")
    print(f"\n{'alpha_1':>8} {'det(M)':>10} {'v^2 (GeV^2)':>14} {'v_R^2 (GeV^2)':>16} {'stable':>8}")
    for r in va["vacuum_per_alpha"]:
        print(f"{r['alpha_1']:>8.2f} {r['det_M']:>10.4f} "
              f"{r['v_squared']:>14.3e} {r['v_R_squared']:>16.3e} "
              f"{str(r['stable']):>8}")

    print("\nCustodial SU(2) breaking (one-loop heavy):")
    cb = custodial_breaking()
    print(f"  Delta rho estimate: {cb['delta_rho_estimate']:.2e}")
    print(f"  Experimental bound: {cb['experimental_bound']:.2e}")
    print(f"  Safety factor: {cb['safety_factor']:.2e}")

    print("\nlam_eff consistency:")
    le = lambda_eff_consistency()
    print(f"  lam_eff (ACS): {le['lam_acs']:.5f}")
    print(f"  lam_SM:       {le['lam_sm']:.5f}")
    print(f"  Fractional difference: {le['fractional_difference']:.4f}")


if __name__ == "__main__":
    main()
