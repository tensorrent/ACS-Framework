# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Common utilities for the ACS codebase.

Provides:
  - Standard sl(n, R) basis construction
  - Bracket and Killing form operations
  - Random traceless matrix generation (seeded)
  - Numerical tolerance constants
"""
import numpy as np
from .seed import default_rng


def sl_n_basis(n):
    """
    Standard traceless basis of sl(n, R), dim = n^2 - 1.

    Layout:
      (n-1) Cartan generators H_i = E_{i,i} - E_{i+1,i+1}
      n(n-1)/2 antisymmetric off-diagonal A_{ij} = E_{ij} - E_{ji}
      n(n-1)/2 symmetric off-diagonal S_{ij} = E_{ij} + E_{ji}

    Returns
    -------
    list of (n, n) ndarray
        Each matrix is traceless. Total length n^2 - 1.

    Examples
    --------
    >>> basis = sl_n_basis(3)
    >>> len(basis)
    8
    >>> all(abs(np.trace(M)) < 1e-12 for M in basis)
    True
    """
    basis = []
    # Cartan
    for a in range(n - 1):
        M = np.zeros((n, n))
        M[a, a] = 1.0
        M[a + 1, a + 1] = -1.0
        basis.append(M)
    # Antisymmetric and symmetric off-diagonal
    for i in range(n):
        for j in range(i + 1, n):
            A = np.zeros((n, n))
            A[i, j] = 1.0
            A[j, i] = -1.0
            basis.append(A)
            S = np.zeros((n, n))
            S[i, j] = 1.0
            S[j, i] = 1.0
            basis.append(S)
    return basis


def bracket(X, Y):
    """Lie bracket [X, Y] = X Y - Y X."""
    return X @ Y - Y @ X


def killing_inner(X, Y, n=None):
    """
    Killing form K(X, Y) = tr(ad_X ad_Y) on sl(n, R).
    Equivalent up to a positive multiplicative constant to 2n tr(X Y).

    Parameters
    ----------
    X, Y : (n, n) ndarray
    n : int, optional
        Defaults to X.shape[0].
    """
    if n is None:
        n = X.shape[0]
    return 2 * n * np.trace(X @ Y)


def random_traceless(n, rng=None):
    """
    Sample a random traceless n x n real matrix.

    Parameters
    ----------
    n : int
    rng : np.random.Generator, optional
        Defaults to the seeded default RNG.
    """
    if rng is None:
        rng = default_rng()
    M = rng.standard_normal((n, n))
    M = M - (np.trace(M) / n) * np.eye(n)
    return M


def to_basis_coords(M, basis):
    """
    Express M as a real linear combination of basis elements.

    Returns (len(basis),) array of coefficients c_i such that
    M = sum_i c_i * basis[i].
    Uses orthogonality of the standard basis under the trace inner product.
    """
    coords = np.zeros(len(basis))
    for i, b in enumerate(basis):
        norm_b = np.trace(b @ b)
        if abs(norm_b) > 1e-12:
            coords[i] = np.trace(M @ b) / norm_b
    return coords


# Numerical tolerances
FLOAT_TOL = 1e-10  # Standard tolerance for "is this zero?"
MACHINE_EPS = 1e-14  # Tightest tolerance after symbolic-then-numerical work
