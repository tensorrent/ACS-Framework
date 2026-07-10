# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Paper C §5.3 — Killing-orthogonality theorem
=============================================
Theorem:
  For any X, Y in a matrix Lie algebra,
      tr([X, Y] · X) = 0
  identically. By trace cyclicity:
      tr(XYX - YX^2) = tr(XYX) - tr(X^2 Y)
                      = tr(YX^2) - tr(X^2 Y)
                      = 0.

This module provides:
  - Symbolic verification (SymPy) returning 0 identically
  - 1000-trial numerical scaling test in sl(3, R) and sl(4, R)
  - Chirality-hopping example: [H_1, A_{01}] = 2 S_{01}

The chirality-hopping example demonstrates that the bracket maps
between symmetric and antisymmetric sectors of the algebra — the
algebraic mechanism underlying the Palatini decomposition.
"""
import numpy as np
import sys
import os
from sympy import Matrix, symbols, simplify, eye

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.common import (
    sl_n_basis, bracket, random_traceless, default_rng, MACHINE_EPS,
)


def symbolic_verification():
    """
    Verify tr([X, Y] · X) = 0 symbolically in sl(3) using generic matrices.

    Returns the simplified expression — should be exactly 0.
    """
    a = symbols('a:9', real=True)
    b = symbols('b:9', real=True)
    X = Matrix(3, 3, a)
    Y = Matrix(3, 3, b)
    # Make traceless
    X = X - (X.trace() / 3) * eye(3)
    Y = Y - (Y.trace() / 3) * eye(3)
    B = X * Y - Y * X
    inner_X = simplify((B * X).trace())
    inner_Y = simplify((B * Y).trace())
    return inner_X, inner_Y


def numerical_scaling_test(n, num_trials=1000, seed=None):
    """
    Test tr([X,Y]·X) = 0 across num_trials random pairs in sl(n, R).

    Returns
    -------
    dict with keys:
      'max_residual_X': max |tr([X,Y]·X)|
      'mean_residual_X': mean |tr([X,Y]·X)|
      'max_residual_Y': max |tr([X,Y]·Y)|
      'mean_residual_Y': mean |tr([X,Y]·Y)|
      'verified': all residuals below MACHINE_EPS
    """
    rng = default_rng(seed=seed)
    res_X = np.empty(num_trials)
    res_Y = np.empty(num_trials)
    for k in range(num_trials):
        X = random_traceless(n, rng)
        Y = random_traceless(n, rng)
        B = bracket(X, Y)
        res_X[k] = np.trace(B @ X)
        res_Y[k] = np.trace(B @ Y)
    return {
        "max_residual_X": float(np.max(np.abs(res_X))),
        "mean_residual_X": float(np.mean(np.abs(res_X))),
        "max_residual_Y": float(np.max(np.abs(res_Y))),
        "mean_residual_Y": float(np.mean(np.abs(res_Y))),
        "verified": bool(np.max(np.abs(res_X)) < MACHINE_EPS * 1e3
                         and np.max(np.abs(res_Y)) < MACHINE_EPS * 1e3),
    }


def chirality_hopping_example(n=4):
    """
    Compute [H_1, A_{01}] in sl(n, R) and verify it equals 2 S_{01}.

    Returns
    -------
    dict with the bracket result, expected 2*S_01, and exact-match flag.
    """
    H1 = np.zeros((n, n))
    H1[0, 0] = 1
    H1[1, 1] = -1
    A01 = np.zeros((n, n))
    A01[0, 1] = 1
    A01[1, 0] = -1
    S01 = np.zeros((n, n))
    S01[0, 1] = 1
    S01[1, 0] = 1

    B = bracket(H1, A01)
    expected = 2 * S01
    return {
        "bracket_H1_A01": B,
        "expected_2_S01": expected,
        "exact_match": bool(np.allclose(B, expected)),
    }


def main():
    print("Paper C §5.3 — Killing-orthogonality verification")
    print("=" * 60)

    # Symbolic
    inner_X, inner_Y = symbolic_verification()
    print(f"\nSymbolic (sl(3, R)):")
    print(f"  tr([X,Y]·X) simplifies to: {inner_X}")
    print(f"  tr([X,Y]·Y) simplifies to: {inner_Y}")
    print(f"  Both identically zero: {inner_X == 0 and inner_Y == 0}")

    # sl(3) scaling
    print(f"\nNumerical scaling — sl(3, R), 1000 trials:")
    r3 = numerical_scaling_test(n=3, num_trials=1000)
    print(f"  max |tr([X,Y]·X)|: {r3['max_residual_X']:.2e}")
    print(f"  max |tr([X,Y]·Y)|: {r3['max_residual_Y']:.2e}")

    # sl(4) scaling
    print(f"\nNumerical scaling — sl(4, R), 1000 trials:")
    r4 = numerical_scaling_test(n=4, num_trials=1000)
    print(f"  max |tr([X,Y]·X)|: {r4['max_residual_X']:.2e}")
    print(f"  max |tr([X,Y]·Y)|: {r4['max_residual_Y']:.2e}")

    # Chirality hopping
    print(f"\nChirality-hopping example: [H_1, A_{{01}}] = 2 S_{{01}} in sl(4, R)")
    ch = chirality_hopping_example(n=4)
    print(f"  Exact match: {ch['exact_match']}")

    print(f"\nAll three identities verified: "
          f"{r3['verified'] and r4['verified'] and ch['exact_match']}")


if __name__ == "__main__":
    main()
