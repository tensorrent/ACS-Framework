"""
Paper C — Theorem C: minimal polynomial of ad_{T_BL}
=====================================================
Statement:
  ad_{T_BL}^3 = (16/9) ad_{T_BL}    on sl(4, R)

Equivalently the minimal polynomial of ad_{T_BL} is
  m(t) = t (t - 4/3) (t + 4/3) = t^3 - (16/9) t

with eigenvalues {0, +4/3, -4/3} and multiplicities (9, 3, 3).

Run as a script to verify, or import the assertions for tests.
"""
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.common import sl_n_basis, bracket, to_basis_coords, FLOAT_TOL


def build_T_BL():
    """The B-L generator: diag(1/3, 1/3, 1/3, -1) in sl(4, R)."""
    return np.diag([1/3, 1/3, 1/3, -1.0])


def build_ad_matrix(X, basis):
    """
    Build the matrix representation of ad_X on the algebra spanned by basis.

    Returns
    -------
    ad : (d, d) ndarray
        Matrix such that ad[:, i] = coords of [X, basis[i]] in the basis.
    """
    d = len(basis)
    ad = np.zeros((d, d))
    for i, b in enumerate(basis):
        ad[:, i] = to_basis_coords(bracket(X, b), basis)
    return ad


def verify_theorem_c():
    """
    Verify ad_{T_BL}^3 = (16/9) ad_{T_BL} on sl(4, R).

    Returns
    -------
    dict with keys:
      'theorem_c_residual': max element-wise deviation from the identity
      'eigenvalues': sorted unique eigenvalues of ad_{T_BL}
      'multiplicities': dict mapping eigenvalue to multiplicity
      'verified': bool
    """
    T_BL = build_T_BL()
    basis = sl_n_basis(4)
    ad = build_ad_matrix(T_BL, basis)

    # Identity check
    ad3 = ad @ ad @ ad
    target = (16 / 9) * ad
    residual = float(np.max(np.abs(ad3 - target)))

    # Eigenstructure
    eigvals = np.linalg.eigvals(ad)
    rounded = np.round(eigvals.real, 8)
    unique = sorted(set(rounded.tolist()))
    multiplicities = {ev: int(np.sum(np.abs(eigvals - ev) < 1e-6)) for ev in unique}

    return {
        "theorem_c_residual": residual,
        "eigenvalues": unique,
        "multiplicities": multiplicities,
        "verified": bool(residual < FLOAT_TOL),
    }


def main():
    result = verify_theorem_c()
    print("Paper C — Theorem C verification")
    print("=" * 50)
    print(f"  ad^3 = (16/9) ad residual: {result['theorem_c_residual']:.2e}")
    print(f"  Eigenvalues: {result['eigenvalues']}")
    print(f"  Multiplicities: {result['multiplicities']}")
    print(f"  Expected: {{-4/3: 3, 0: 9, +4/3: 3}}")
    print(f"  Verified: {result['verified']}")
    return result


if __name__ == "__main__":
    main()
