"""
Paper B §6 — Explicit formula as resolvent susceptibility
==========================================================
The Riemann explicit formula

    psi(x) - x = -sum_rho x^rho / rho - log(2 pi) - (1/2) log(1 - x^-2)

can be reformulated in terms of a susceptibility with simple poles at
the imaginary parts of the nontrivial zeros:

    chi(omega) = sum_k 1 / (omega - gamma_k)

This is the trace of the resolvent of any operator H whose spectrum
equals {gamma_k}:

    chi(omega) = Tr[(omega I - H)^-1]

For the trivial choice H = diag(gamma_1, ..., gamma_N) the identity
holds tautologically, verifying the resolvent shape of the explicit
formula. The Hilbert-Polya open problem is to find a NATURAL H
(self-adjoint Schrodinger or similar) whose spectrum equals {gamma_k}
without inputting the values directly.

This module verifies the resolvent shape and reports historical status.
"""
import numpy as np

# First 50 Riemann zero imaginary parts (Odlyzko)
RIEMANN_ZEROS = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
    103.725538, 105.446623, 107.168611, 111.029536, 111.874659,
    114.320221, 116.226680, 118.790783, 121.370125, 122.946829,
    124.256819, 127.516684, 129.578704, 131.087689, 133.497737,
    134.756510, 138.116042, 139.736209, 141.123707, 143.111846,
])


def chi(omega, gammas=None, regularization=1e-10):
    """
    Compute chi(omega) = sum_k 1 / (omega - gamma_k).

    Parameters
    ----------
    omega : float or complex
    gammas : array-like, optional
        Defaults to the first 50 Riemann zeros.
    regularization : float
        Imaginary shift to regularize at poles.
    """
    if gammas is None:
        gammas = RIEMANN_ZEROS
    return np.sum(1.0 / (omega + regularization * 1j - np.asarray(gammas)))


def trace_resolvent(omega, H, regularization=1e-10):
    """
    Compute Tr[(omega I - H)^-1] for a finite-dim operator H.
    """
    n = H.shape[0]
    return np.trace(np.linalg.inv((omega + regularization * 1j) * np.eye(n) - H))


def verify_resolvent_identity(omega_test=50.0, gammas=None):
    """
    Verify Tr[(omega - H)^-1] = chi(omega) for the trivial diagonal H.
    """
    if gammas is None:
        gammas = RIEMANN_ZEROS
    H_trivial = np.diag(gammas).astype(complex)
    chi_val = chi(omega_test, gammas=gammas)
    res_val = trace_resolvent(omega_test, H_trivial)
    return {
        "omega": omega_test,
        "chi_omega": chi_val,
        "trace_resolvent": res_val,
        "match": bool(np.isclose(chi_val, res_val, atol=1e-6)),
    }


def pole_structure_check():
    """
    Verify that |chi(omega)| spikes near each gamma_k (simple poles).
    """
    results = []
    for k in range(5):
        gamma_k = RIEMANN_ZEROS[k]
        # Just below the pole
        chi_below = chi(gamma_k - 0.01)
        # Just above
        chi_above = chi(gamma_k + 0.01)
        results.append({
            "gamma_k": float(gamma_k),
            "abs_chi_minus_eps": float(abs(chi_below)),
            "abs_chi_plus_eps": float(abs(chi_above)),
            "diverges_at_pole": abs(chi_below) > 50 or abs(chi_above) > 50,
        })
    return results


def main():
    print("Paper B §6 — Explicit formula as resolvent susceptibility")
    print("=" * 60)

    print("\n(1) Resolvent identity check (trivial H = diag(gamma_k)):")
    r = verify_resolvent_identity(omega_test=50.0)
    print(f"    chi(50)         = {r['chi_omega']:.6f}")
    print(f"    Tr[(50-H)^-1]   = {r['trace_resolvent']:.6f}")
    print(f"    Identity holds: {r['match']}")

    print("\n(2) Pole structure near first 5 zeros:")
    for p in pole_structure_check():
        print(f"    gamma_k = {p['gamma_k']:.4f}: "
              f"|chi(gamma-eps)| = {p['abs_chi_minus_eps']:.1f}, "
              f"|chi(gamma+eps)| = {p['abs_chi_plus_eps']:.1f}")

    print("\nStatus:")
    print("  Resolvent shape of the explicit formula: VERIFIED (trivially)")
    print("  Hilbert-Polya: a natural self-adjoint H with exact spectrum")
    print("  {gamma_k} not inputted: OPEN since 1914.")


if __name__ == "__main__":
    main()
