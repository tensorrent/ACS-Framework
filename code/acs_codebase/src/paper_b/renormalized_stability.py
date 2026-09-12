# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Paper B §6 — Finite normalized zero-sum diagnostic
====================================================
For supplied real ordinates gamma_k this module evaluates only

    D_N(u) = -2 Re sum_{k=1}^N exp(i gamma_k u) / (1/2 + i gamma_k).

Every such finite sum is bounded for real u by
2 sum_k 1/sqrt(1/4 + gamma_k^2), including arbitrary synthetic ordinates.
This fact and the finite-grid diagnostic do not test RH. The routine omits
the explicit formula's other terms and any infinite-sum truncation control;
it is not the full arithmetic quantity (psi(exp(u))-exp(u))/exp(u/2).

Under RH the classical von Koch estimate for that full quantity is O(u^2).
For example, Schoenfeld (1976), Theorem 10, (6.2), bounds its absolute value
by u^2/(8*pi) when exp(u) >= 73.2. It does not give the constant bound of
this fixed finite sum. DOI: 10.1090/S0025-5718-1976-0457374-X.

The optional off-critical term has an exponentially growing envelope when
sigma > 1/2. A finite-grid running-maximum comparison of that toy term is
not a proof of an infinite explicit-formula converse.
"""
import numpy as np
from scipy.stats import linregress

from .explicit_formula_resolvent import RIEMANN_ZEROS


def delta_norm(u, gammas=None):
    """
    Evaluate D_N(u), the finite normalized sum over supplied real ordinates.

    Cancel the real exponential analytically before numerical evaluation.
    Forming exp(u) first overflows near u=710 although this sum is bounded.
    """
    if gammas is None:
        gammas = RIEMANN_ZEROS
    gammas = np.asarray(gammas)
    rhos = 0.5 + 1j * gammas
    terms = np.exp(1j * gammas * u) / rhos
    return -2 * np.sum(terms.real)  # standard zero-contribution sign


def boundedness_check(u_min=5.0, u_max=20.0, N_grid=500):
    """
    Summarize a finite normalized sum on a declared log-coordinate grid.

    Returns
    -------
    dict with max, mean, std and a linear-fit slope of running max.
    The slope threshold is a finite-grid diagnostic, not an RH criterion.
    The existing result keys are retained for compatibility.
    """
    u_grid = np.linspace(u_min, u_max, N_grid)
    delta_vals = np.array([delta_norm(u) for u in u_grid])
    abs_vals = np.abs(delta_vals)
    running_max = np.maximum.accumulate(abs_vals)
    slope, intercept, r_val, _, _ = linregress(u_grid, running_max)
    return {
        "u_range": (u_min, u_max),
        "max_abs_delta_norm": float(np.max(abs_vals)),
        "mean_abs_delta_norm": float(np.mean(abs_vals)),
        "std_delta_norm": float(np.std(delta_vals)),
        "running_max_slope": float(slope),
        "running_max_R_squared": float(r_val ** 2),
        "consistent_with_boundedness": bool(abs(slope) < 0.05),
    }


def divergence_test_off_critical(sigma_off=0.7, u_min=5.0, u_max=10.0):
    """
    Hypothetically, if a single zero had real part sigma_off > 0.5,
    its contribution to Delta_norm would grow as e^((sigma - 0.5) u).

    This test demonstrates the divergence by adding ONE off-critical
    zero to the truncated sum.
    """
    u_grid = np.linspace(u_min, u_max, 50)
    on_critical = np.array([delta_norm(u) for u in u_grid])
    # Add a hypothetical off-critical zero at sigma = sigma_off,
    # gamma = 14.134725 (same imaginary part as gamma_1 for clarity)
    extra = []
    for u in u_grid:
        rho = sigma_off + 1j * 14.134725
        contrib = -2 * (np.exp((rho - 0.5) * u) / rho).real
        extra.append(contrib)
    extra = np.array(extra)
    total_off = on_critical + extra

    # Slope of running max
    slope_on, _, _, _, _ = linregress(u_grid, np.maximum.accumulate(np.abs(on_critical)))
    slope_off, _, _, _, _ = linregress(u_grid, np.maximum.accumulate(np.abs(total_off)))
    return {
        "sigma_off": sigma_off,
        "max_with_off_zero": float(np.max(np.abs(total_off))),
        "max_on_critical_only": float(np.max(np.abs(on_critical))),
        "slope_on_critical": float(slope_on),
        "slope_with_off_zero": float(slope_off),
        "off_zero_diverges_faster": bool(slope_off > slope_on),
    }


def main():
    print("Paper B §6 — Finite normalized zero-sum diagnostic")
    print("=" * 60)

    print("\n(1) Finite-grid diagnostic on u in [5, 20] (50 supplied ordinates):")
    b = boundedness_check()
    print(f"    max |Delta_norm|:  {b['max_abs_delta_norm']:.4f}")
    print(f"    mean |Delta_norm|: {b['mean_abs_delta_norm']:.4f}")
    print(f"    std Delta_norm:    {b['std_delta_norm']:.4f}")
    print(f"    running-max slope: {b['running_max_slope']:.5f}")
    print(f"    Consistent with boundedness: {b['consistent_with_boundedness']}")

    print("\n(2) Hypothetical off-critical zero at sigma = 0.7:")
    d = divergence_test_off_critical()
    print(f"    max with off zero:    {d['max_with_off_zero']:.4f}")
    print(f"    max on critical only: {d['max_on_critical_only']:.4f}")
    print(f"    slope on critical:    {d['slope_on_critical']:.5f}")
    print(f"    slope with off zero:  {d['slope_with_off_zero']:.5f}")
    print(f"    Off-zero diverges faster: {d['off_zero_diverges_faster']}")

    print("\nConclusion:")
    print("  Every fixed finite sum over real ordinates is bounded in u.")
    print("  The hypothetical off-critical term has a growing envelope.")
    print("  These diagnostics do not establish RH or an infinite-sum bound.")
    print("  The classical RH estimate for the full normalized error is O(u^2).")
    print("  See Schoenfeld (1976), Theorem 10, (6.2).")


if __name__ == "__main__":
    main()
