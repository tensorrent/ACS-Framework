#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Issue #7: 4/3 mechanism test.

Goal:
  Test whether the equality
      ACS value beta = 4/3
      LLT-like exponent alpha(d) = 1 + 1/d
  has a robust mechanism or is a coordinate/normalization coincidence.

Kill criteria:
  K1: If the mapping depends on generator normalization, it is not invariant.
  K2: If equality arises only under a bookkeeping identity (n = d + 1), it is
      not an independent mechanism.
"""

from __future__ import annotations

import math

import numpy as np


def alpha_density(d: float) -> float:
    return 1.0 + 1.0 / d


def beta_acs(n: float) -> float:
    # Charge-gap pattern used in the ACS note: (+1/(n-1)) - (-1) = n/(n-1)
    return n / (n - 1.0)


def implied_dimension_from_beta(beta_value: float) -> float:
    # Solve beta = 1 + 1/d  => d = 1/(beta - 1)
    if beta_value <= 1.0:
        return float("nan")
    return 1.0 / (beta_value - 1.0)


def main() -> None:
    beta0 = 4.0 / 3.0
    d0 = implied_dimension_from_beta(beta0)
    print("4/3 mechanism test")
    print(f"Baseline: beta = 4/3 => implied d = {d0:.6f}")

    print("\nK1: normalization robustness")
    scales = [0.50, 0.75, 1.00, 1.10, 1.25, 1.50]
    print("scale c, beta' = c*beta, implied d' = 1/(beta'-1)")
    d_values = []
    for c in scales:
        beta_scaled = c * beta0
        d_scaled = implied_dimension_from_beta(beta_scaled)
        d_values.append(d_scaled)
        print(f"c={c:>4.2f}  beta'={beta_scaled:>7.4f}  d'={d_scaled:>10.6f}")
    finite_d = [d for d in d_values if math.isfinite(d)]
    spread = max(finite_d) - min(finite_d) if finite_d else float("inf")
    print(f"finite d' spread under scaling = {spread:.6f}")

    print("\nK2: independent-mechanism check (integer lattice scan)")
    dims = list(range(2, 13))
    n_vals = list(range(2, 13))
    exact_hits: list[tuple[int, int]] = []
    for d in dims:
        a = alpha_density(float(d))
        for n in n_vals:
            b = beta_acs(float(n))
            if abs(a - b) < 1e-12:
                exact_hits.append((d, n))
    print(f"exact alpha(d)=beta(n) hits in d,n in [2..12]: {exact_hits}")
    bookkeeping_only = all(n == d + 1 for d, n in exact_hits)
    print(f"all hits satisfy n=d+1: {bookkeeping_only}")

    print("\nDecision")
    k1_fail = (spread > 0.5) or any(not math.isfinite(d) for d in d_values)
    k2_fail = bookkeeping_only
    if k1_fail or k2_fail:
        print("RESULT: mechanism not established; coincidence fails robustness tests.")
    else:
        print("RESULT: mechanism survives these tests (unexpected).")


if __name__ == "__main__":
    main()
