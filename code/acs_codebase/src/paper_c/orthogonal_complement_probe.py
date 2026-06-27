"""
Paper C §5.4 — Orthogonal-complement reconstruction probe
==========================================================
Given B = [X, Y] in sl(n, R), the Killing-orthogonality theorem
forces both X and Y to lie in the codimension-1 subspace

    B^perp = {Z : tr(B Z) = 0}

This module provides an explicit basis for B^perp via SVD null-space
of the Killing-weighted functional v -> <B, v>.

Reconstruction scope:
  Recovers: dim B^perp = n^2 - 2 subspace + ||B||^2 + spec(ad_B)
  Does not recover: span{X, Y}, individual ||X||, ||Y||, K(X,X), K(Y,Y)

Ambiguity counts (sl(4, R)):
  Passive ambiguity:        dim B^perp = 14
  Generic Jacobian kernel:  15  (rank of bracket map at generic (X, Y))
  Degenerate kernel:        19  (at the specific point (H_1, A_{01}))
"""
import numpy as np
from scipy.linalg import null_space
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.common import sl_n_basis, bracket, to_basis_coords, FLOAT_TOL
from src.common import default_rng, random_traceless


def orthogonal_complement_probe(B, n):
    """
    Compute a basis for B^perp ⊂ sl(n, R).

    Parameters
    ----------
    B : (n, n) ndarray
        The bracket output [X, Y].
    n : int
        Dimension of the algebra: sl(n, R).

    Returns
    -------
    null_basis : (n^2-1, n^2-2) ndarray
        Columns form an orthonormal basis of B^perp expressed in
        coordinates relative to the standard sl(n) basis.
    b_coords : (n^2-1,) ndarray
        Expansion of B in the standard basis.
    """
    basis = sl_n_basis(n)
    d = len(basis)
    K_diag = np.array([np.trace(b @ b) for b in basis])
    b_coords = np.array([np.trace(B @ basis[i]) / K_diag[i] for i in range(d)])
    weights = K_diag * b_coords  # the Killing-weighted form of B
    null_basis = null_space(weights.reshape(1, -1))  # (d, d-1)
    return null_basis, b_coords


def jacobian_kernel_dimension(X, Y, n):
    """
    Compute the dimension of the kernel of d(bracket)|_{(X,Y)}.

    The bracket map is mu : sl(n) x sl(n) -> sl(n), mu(X, Y) = [X, Y].
    Its differential at (X, Y) is
        d(mu)(dX, dY) = [dX, Y] + [X, dY].
    Returns the kernel dimension = 2*(n^2 - 1) - rank(d(mu)).
    """
    basis = sl_n_basis(n)
    d = len(basis)
    J = np.zeros((d, 2 * d))
    for i in range(d):
        J[:, i] = to_basis_coords(bracket(basis[i], Y), basis)
        J[:, d + i] = to_basis_coords(bracket(X, basis[i]), basis)
    rank = int(np.linalg.matrix_rank(J, tol=FLOAT_TOL))
    return {
        "rank_of_dmu": rank,
        "kernel_dim": 2 * d - rank,
        "image_dim": rank,
    }


def verify_probe_at_H1_A01():
    """
    Verify the probe on B_0 = [H_1, A_{01}] = 2 S_{01} in sl(4, R).

    Expected:
      dim B^perp = n^2 - 2 = 14
      X, Y both lie in B^perp (projection error ~ 0)
      Jacobian kernel at this DEGENERATE point is 19 (rank 11)
    """
    n = 4
    H1 = np.zeros((n, n))
    H1[0, 0] = 1
    H1[1, 1] = -1
    A01 = np.zeros((n, n))
    A01[0, 1] = 1
    A01[1, 0] = -1

    B = bracket(H1, A01)
    null_basis, b_coords = orthogonal_complement_probe(B, n)

    basis = sl_n_basis(n)
    K_diag = np.array([np.trace(b @ b) for b in basis])
    H1_coords = np.array([np.trace(H1 @ basis[i]) / K_diag[i] for i in range(len(basis))])
    A01_coords = np.array([np.trace(A01 @ basis[i]) / K_diag[i] for i in range(len(basis))])

    # Project onto B^perp
    H1_proj = null_basis @ null_basis.T @ H1_coords
    A01_proj = null_basis @ null_basis.T @ A01_coords

    H1_in_perp = float(np.linalg.norm(H1_coords - H1_proj))
    A01_in_perp = float(np.linalg.norm(A01_coords - A01_proj))

    jac = jacobian_kernel_dimension(H1, A01, n)

    return {
        "dim_B_perp": null_basis.shape[1],
        "H1_in_B_perp_residual": H1_in_perp,
        "A01_in_B_perp_residual": A01_in_perp,
        "jacobian_kernel_dim_degenerate": jac["kernel_dim"],
        "jacobian_rank_degenerate": jac["rank_of_dmu"],
    }


def verify_probe_at_generic(num_trials=20):
    """
    Verify the generic (random pair) Jacobian kernel dimension is 15
    for sl(4, R) — the regular case where the bracket map is onto.
    """
    n = 4
    rng = default_rng()
    ranks = []
    kernels = []
    for _ in range(num_trials):
        X = random_traceless(n, rng)
        Y = random_traceless(n, rng)
        jac = jacobian_kernel_dimension(X, Y, n)
        ranks.append(jac["rank_of_dmu"])
        kernels.append(jac["kernel_dim"])
    return {
        "ranks": ranks,
        "kernels": kernels,
        "all_rank_15": all(r == 15 for r in ranks),
        "all_kernel_15": all(k == 15 for k in kernels),
    }


def main():
    print("Paper C §5.4 — Orthogonal-complement probe")
    print("=" * 60)

    # Degenerate point (H_1, A_01)
    print("\nDegenerate point (H_1, A_{01}) in sl(4, R):")
    d = verify_probe_at_H1_A01()
    print(f"  dim B^perp:                   {d['dim_B_perp']}  (expected 14)")
    print(f"  ||H_1 - pi_perp(H_1)||:       {d['H1_in_B_perp_residual']:.2e}")
    print(f"  ||A_01 - pi_perp(A_01)||:     {d['A01_in_B_perp_residual']:.2e}")
    print(f"  Jacobian rank:                {d['jacobian_rank_degenerate']} (degenerate)")
    print(f"  Jacobian kernel dim:          {d['jacobian_kernel_dim_degenerate']} (degenerate)")

    # Generic points
    print("\nGeneric (X, Y) in sl(4, R), 20 random trials:")
    g = verify_probe_at_generic(num_trials=20)
    print(f"  All ranks == 15:   {g['all_rank_15']}")
    print(f"  All kernels == 15: {g['all_kernel_15']}")

    print("\nSummary of three ambiguity numbers for sl(4, R):")
    print(f"  Passive (B^perp):           14")
    print(f"  Generic Jacobian kernel:    15")
    print(f"  Degenerate kernel at H1,A01: 19")


if __name__ == "__main__":
    main()
