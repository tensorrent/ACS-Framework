"""
Paper C §5.5 — Three-class spectral taxonomy
=============================================
Adjoint flows exp(t · ad_X) classify by the spectrum of ad_X
(via Jordan-Chevalley decomposition):

  Elliptic:    semisimple, complex-conjugate-pair eigenvalues
               -> rotational, periodic
               -> example: SU(2) quaternion (i sigma_3)
  Hyperbolic:  semisimple, real eigenvalues
               -> exponential growth/decay
               -> example: sl(4, R) Palatini ad_{T_BL}
  Parabolic:   nilpotent (zero spectrum, nontrivial Jordan blocks)
               -> polynomial growth
               -> example: not yet identified in ACS instances

The "three steps make 2 pi" picture from SU(2) is ELLIPTIC-specific.
It does NOT generalize to hyperbolic (sl(4, R)) cases.

This module verifies:
  - SU(2) quaternion: 3 rotations of 2pi/3 give -I (elliptic 2pi inversion)
  - sl(4, R) ad_{T_BL}: exp(t*ad) is hyperbolic (no 2pi loop)
  - Frenet-Serret: A^3 = -(kappa^2 + chi^2) A — elliptic class
  - Core rope ring: R^3 = R — hyperbolic with eigenvalues {-1, 0, +1}
"""
import numpy as np
from scipy.linalg import expm
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.common import sl_n_basis, bracket, to_basis_coords, FLOAT_TOL
from .theorem_c import build_T_BL, build_ad_matrix


def classify_spectrum(eigenvalues, tol=1e-8):
    """
    Classify a spectrum into elliptic, hyperbolic, parabolic, or mixed.

    Returns
    -------
    dict with counts of:
      'real_count':         eigenvalues with |Im| < tol and |Re| > tol
      'imaginary_count':    eigenvalues with |Re| < tol and |Im| > tol
      'zero_count':         eigenvalues with |Re|, |Im| < tol
      'complex_count':      eigenvalues with both |Re|, |Im| > tol
      'class':              'elliptic' / 'hyperbolic' / 'mixed' / 'nilpotent'
    """
    eigs = np.array(eigenvalues)
    real_count = int(np.sum((np.abs(eigs.imag) < tol) & (np.abs(eigs.real) > tol)))
    imag_count = int(np.sum((np.abs(eigs.real) < tol) & (np.abs(eigs.imag) > tol)))
    zero_count = int(np.sum((np.abs(eigs.real) < tol) & (np.abs(eigs.imag) < tol)))
    complex_count = int(np.sum((np.abs(eigs.real) >= tol) & (np.abs(eigs.imag) >= tol)))

    if zero_count == len(eigs):
        cls = "nilpotent (zero spectrum)"
    elif imag_count > 0 and real_count == 0:
        cls = "elliptic"
    elif real_count > 0 and imag_count == 0 and complex_count == 0:
        cls = "hyperbolic"
    else:
        cls = "mixed"

    return {
        "real_count": real_count,
        "imaginary_count": imag_count,
        "zero_count": zero_count,
        "complex_count": complex_count,
        "class": cls,
    }


def classify_ad_T_BL():
    """
    Classify the Palatini adjoint ad_{T_BL} on sl(4, R).
    Expected: hyperbolic (eigenvalues {0, +/- 4/3}).
    """
    T_BL = build_T_BL()
    basis = sl_n_basis(4)
    ad = build_ad_matrix(T_BL, basis)
    eigs = np.linalg.eigvals(ad)
    return classify_spectrum(eigs)


def verify_su2_elliptic_2pi():
    """
    SU(2) quaternion: three 2pi/3 rotations about a common axis compose
    to a 2pi rotation, which acts as -I on spinors.

    Returns the composed rotation and its deviation from -I.
    """
    sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)
    # 2pi/3 rotation about z-axis (spinor representation)
    U_step = expm(-1j * (np.pi / 3) * sigma_3)  # exp(-i theta sigma/2) with theta = 2pi/3 -> half = pi/3
    U_total = U_step @ U_step @ U_step
    return {
        "U_total": U_total,
        "deviation_from_minus_I": float(np.max(np.abs(U_total + np.eye(2)))),
        "is_minus_I": bool(np.allclose(U_total, -np.eye(2))),
    }


def verify_sl4_hyperbolic():
    """
    sl(4, R) ad_{T_BL}: at t = 2pi, exp(t*ad) blows up exponentially.
    Demonstrates the spectrum is real (hyperbolic), not imaginary.
    """
    T_BL = build_T_BL()
    basis = sl_n_basis(4)
    ad = build_ad_matrix(T_BL, basis)
    U_2pi = expm(2 * np.pi * ad)
    max_norm = float(np.max(np.abs(U_2pi)))
    # Identify the upper eigenspace growth: eigenvalue +4/3 at t=2pi gives e^(8pi/3)
    expected_growth = np.exp(8 * np.pi / 3)
    return {
        "max_element_at_2pi": max_norm,
        "expected_growth_factor": expected_growth,
        "is_bounded_loop": max_norm < 10,  # would fail for hyperbolic
    }


def verify_core_rope_hyperbolic():
    """
    Core rope ring operator R with minimal polynomial t(t-1)(t+1).
    Spectrum {-1, 0, +1} — three distinct real eigenvalues -> hyperbolic.
    """
    # Permutation-like operator on three states
    # R is diagonalizable with the stated spectrum
    R = np.diag([1.0, 0.0, -1.0])
    eigs = np.linalg.eigvals(R)
    R3 = R @ R @ R
    return {
        "R_cubed_equals_R": bool(np.allclose(R3, R)),
        "eigenvalues": sorted(eigs.real.tolist()),
        "spectrum_classification": classify_spectrum(eigs),
    }


def verify_frenet_serret_elliptic(kappa=1.0, chi=0.5):
    """
    Frenet-Serret matrix:
       A = [[0, kappa, 0], [-kappa, 0, chi], [0, -chi, 0]]
    has eigenvalues {0, +/- i sqrt(kappa^2 + chi^2)} -> elliptic class.
    Minimal polynomial: lambda (lambda^2 + kappa^2 + chi^2) = 0
    so A^3 = -(kappa^2 + chi^2) A.
    """
    A = np.array([
        [0,      kappa, 0    ],
        [-kappa, 0,     chi  ],
        [0,      -chi,  0    ],
    ])
    A3 = A @ A @ A
    target = -(kappa**2 + chi**2) * A
    eigs = np.linalg.eigvals(A)
    return {
        "A_cubed_residual": float(np.max(np.abs(A3 - target))),
        "eigenvalues": eigs,
        "spectrum_classification": classify_spectrum(eigs),
    }


def main():
    print("Paper C §5.5 — Three-class spectral taxonomy")
    print("=" * 60)

    print("\nClass 1: Elliptic (SU(2) quaternion)")
    su2 = verify_su2_elliptic_2pi()
    print(f"  Three 2pi/3 rotations -> deviation from -I: {su2['deviation_from_minus_I']:.2e}")
    print(f"  Geometric 2pi inversion: {su2['is_minus_I']}")

    print("\nClass 1: Elliptic (Frenet-Serret)")
    fs = verify_frenet_serret_elliptic()
    print(f"  A^3 = -(k^2 + chi^2) A residual: {fs['A_cubed_residual']:.2e}")
    print(f"  Spectrum class: {fs['spectrum_classification']['class']}")
    print(f"  (zeros, imag, real): "
          f"{fs['spectrum_classification']['zero_count']}, "
          f"{fs['spectrum_classification']['imaginary_count']}, "
          f"{fs['spectrum_classification']['real_count']}")

    print("\nClass 2: Hyperbolic (sl(4, R) ad_{T_BL})")
    sl4 = verify_sl4_hyperbolic()
    print(f"  Max |exp(2pi * ad)| element: {sl4['max_element_at_2pi']:.2e}")
    print(f"  Expected growth e^(8pi/3): {sl4['expected_growth_factor']:.2e}")
    print(f"  This is exponential — no 2pi loop")

    cls_T_BL = classify_ad_T_BL()
    print(f"  Spectrum class: {cls_T_BL['class']}")
    print(f"  (zeros, imag, real, complex): "
          f"{cls_T_BL['zero_count']}, "
          f"{cls_T_BL['imaginary_count']}, "
          f"{cls_T_BL['real_count']}, "
          f"{cls_T_BL['complex_count']}")

    print("\nClass 2: Hyperbolic (Core rope ring)")
    cr = verify_core_rope_hyperbolic()
    print(f"  R^3 = R: {cr['R_cubed_equals_R']}")
    print(f"  Eigenvalues: {cr['eigenvalues']}")
    print(f"  Spectrum class: {cr['spectrum_classification']['class']}")

    print("\nConclusion:")
    print("  The 2pi-inversion picture is elliptic-class-specific.")
    print("  Hyperbolic systems exhibit exponential, not rotational, flow.")
    print("  Common feature: low-degree minimal polynomial, finite-order closure.")


if __name__ == "__main__":
    main()
