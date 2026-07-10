# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Paper C — ER=EPR re-reading: algebraic non-traversability
==========================================================
The Maldacena-Susskind ER=EPR conjecture imposes wormhole non-
traversability as an external causality constraint. The ACS bracket
algebra derives the operational content of non-traversability for
free, as a consequence of the Killing-orthogonality theorem.

Operational content of "non-traversable":
  Local Alice operators commute with local Bob operators.
  The bracket [X, Y] is Killing-orthogonal to both X and Y.
  Direct projection of B onto X or Y returns identically zero.

This module verifies the algebraic structure underlying this re-reading.
"""
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.common import bracket, FLOAT_TOL


def bell_state_local_commutativity():
    """
    Verify Alice and Bob's local operators commute on a Bell state,
    illustrating the standard QM tensor-product structure.

    Returns
    -------
    dict with the commutator and its norm.
    """
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    A = np.kron(sigma_x, I2)  # Alice's X on qubit 1
    B = np.kron(I2, sigma_z)  # Bob's Z on qubit 2

    comm = A @ B - B @ A
    return {
        "commutator_norm": float(np.linalg.norm(comm)),
        "commute": bool(np.allclose(comm, 0)),
    }


def bracket_killing_orthogonality():
    """
    For a generic random pair (X, Y) in a matrix algebra, verify
    that [X, Y] is trace-orthogonal to both X and Y.

    Returns
    -------
    dict with both inner products at machine precision.
    """
    rng = np.random.default_rng(42)
    X = rng.standard_normal((4, 4))
    X = X - (np.trace(X) / 4) * np.eye(4)
    Y = rng.standard_normal((4, 4))
    Y = Y - (np.trace(Y) / 4) * np.eye(4)
    B = bracket(X, Y)
    return {
        "tr_B_X": float(np.trace(B @ X)),
        "tr_B_Y": float(np.trace(B @ Y)),
        "both_zero": bool(abs(np.trace(B @ X)) < FLOAT_TOL
                          and abs(np.trace(B @ Y)) < FLOAT_TOL),
    }


def projection_returns_zero():
    """
    The 'reconstruction' projection pi_X(B) = (tr(B X) / tr(X X)) X
    returns identically zero because tr([X,Y] X) = 0 by theorem.

    This is the algebraic statement of "non-traversability": you
    cannot traverse from B back to X by direct projection.
    """
    rng = np.random.default_rng(42)
    X = rng.standard_normal((4, 4))
    X = X - (np.trace(X) / 4) * np.eye(4)
    Y = rng.standard_normal((4, 4))
    Y = Y - (np.trace(Y) / 4) * np.eye(4)
    B = bracket(X, Y)

    coeff = np.trace(B @ X) / np.trace(X @ X)
    pi_X_B = coeff * X
    return {
        "projection_coefficient": float(coeff),
        "projection_norm": float(np.linalg.norm(pi_X_B)),
        "zero_to_machine_precision": bool(abs(coeff) < FLOAT_TOL),
    }


def main():
    print("Paper C — Algebraic non-traversability (ER=EPR re-reading)")
    print("=" * 60)

    print("\n(1) Bell-state local operators commute (standard QM):")
    bell = bell_state_local_commutativity()
    print(f"    [A_Alice, B_Bob] norm: {bell['commutator_norm']:.2e}")
    print(f"    Commute: {bell['commute']}")

    print("\n(2) Killing-orthogonality of bracket output:")
    ko = bracket_killing_orthogonality()
    print(f"    tr([X,Y] · X): {ko['tr_B_X']:.2e}")
    print(f"    tr([X,Y] · Y): {ko['tr_B_Y']:.2e}")
    print(f"    Both zero: {ko['both_zero']}")

    print("\n(3) Direct projection back to X returns zero:")
    pj = projection_returns_zero()
    print(f"    projection coefficient: {pj['projection_coefficient']:.2e}")
    print(f"    pi_X(B) is zero to machine precision: "
          f"{pj['zero_to_machine_precision']}")

    print("\nConclusion:")
    print("  Non-traversability in the ACS bracket algebra is a consequence")
    print("  of trace cyclicity, not an imposed causality postulate.")


if __name__ == "__main__":
    main()
