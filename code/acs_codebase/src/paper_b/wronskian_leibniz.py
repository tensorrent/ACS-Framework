"""
Paper B §6 — Wronskian on scalar functions fails Leibniz
=========================================================
The Wronskian bracket W(f, g) = f g' - f' g is bilinear, antisymmetric,
and satisfies the Plücker identity (a degenerate form of Jacobi for
scalar functions). However, it FAILS the Leibniz rule:

    W(f g, h) - [f W(g, h) + g W(f, h)] = -f g h'

The failure is exact and computable. Therefore W is NOT a Poisson
bracket on the space of scalar functions.

Consequence: the "plasma Hamiltonian" reading of the Riemann spectral
sector — under which W would be the Poisson bracket on zero-mode
amplitudes — does NOT survive scrutiny. The plasma analogy is
phenomenological (resonance peaks, beat frequencies, dispersion);
the Hamiltonian / symplectic claim is not supported by the algebra.

This module verifies the Leibniz failure both symbolically (returning
the exact correction term -f g h') and numerically.
"""
import numpy as np
from sympy import Function, Symbol, diff, simplify


def symbolic_leibniz_check():
    """
    Symbolically compute W(fg, h) - [f W(g,h) + g W(f,h)] and confirm
    it equals -f g h' identically.
    """
    t = Symbol('t', real=True)
    f = Function('f')(t)
    g = Function('g')(t)
    h = Function('h')(t)

    def W(a, b, var):
        return a * diff(b, var) - diff(a, var) * b

    lhs = W(f * g, h, t)
    rhs = f * W(g, h, t) + g * W(f, h, t)
    diff_expr = simplify(lhs - rhs)
    expected = -f * g * diff(h, t)
    is_equal = simplify(diff_expr - expected) == 0

    return {
        "lhs_minus_rhs": diff_expr,
        "expected": expected,
        "matches_minus_fgh_prime": is_equal,
    }


def numerical_leibniz_check(x_test=2.0, eps=1e-6):
    """
    Numerical Leibniz check at a sample point with concrete functions.
    """
    f = lambda x: np.sin(x)
    g = lambda x: np.cos(2 * x)
    h = lambda x: np.exp(-x / 10)

    def W_num(a, b, x):
        da = (a(x + eps) - a(x - eps)) / (2 * eps)
        db = (b(x + eps) - b(x - eps)) / (2 * eps)
        return a(x) * db - da * b(x)

    fg = lambda x: f(x) * g(x)
    W_fg_h = W_num(fg, h, x_test)
    W_g_h = W_num(g, h, x_test)
    W_f_h = W_num(f, h, x_test)
    leibniz_rhs = f(x_test) * W_g_h + g(x_test) * W_f_h
    h_prime = (h(x_test + eps) - h(x_test - eps)) / (2 * eps)
    expected = -f(x_test) * g(x_test) * h_prime

    return {
        "W_fg_h": W_fg_h,
        "leibniz_rhs": leibniz_rhs,
        "difference": W_fg_h - leibniz_rhs,
        "expected_minus_fgh_prime": expected,
        "matches_within_1pct": bool(abs((W_fg_h - leibniz_rhs) - expected) < 1e-3 * abs(expected)),
    }


def main():
    print("Paper B §6 — Wronskian fails Leibniz on scalar functions")
    print("=" * 60)

    print("\n(1) Symbolic check (SymPy):")
    s = symbolic_leibniz_check()
    print(f"    W(fg, h) - [f W(g,h) + g W(f,h)] = {s['lhs_minus_rhs']}")
    print(f"    Expected:                          {s['expected']}")
    print(f"    Identity holds: {s['matches_minus_fgh_prime']}")

    print("\n(2) Numerical check (f=sin, g=cos(2x), h=exp(-x/10), at x=2):")
    n = numerical_leibniz_check()
    print(f"    W(fg, h):            {n['W_fg_h']:+.6f}")
    print(f"    f W(g,h) + g W(f,h): {n['leibniz_rhs']:+.6f}")
    print(f"    Difference:          {n['difference']:+.6f}")
    print(f"    Expected (-f g h'):  {n['expected_minus_fgh_prime']:+.6f}")
    print(f"    Match within 1%: {n['matches_within_1pct']}")

    print("\nConclusion:")
    print("  Leibniz fails. W is not a Poisson bracket on scalar functions.")
    print("  The plasma-Hamiltonian reading of Paper B is not supported.")
    print("  Plasma phenomenology survives only as analogy, not foundation.")


if __name__ == "__main__":
    main()
