"""Exact affine and integer-normal-form audit of the Klein cover counterexample.

The affine realization and symbolic identities are separate from the Lean proofs.
Topological interpretation uses the explicitly stated quotient and covering model.
"""
from itertools import product
import json
import sympy as sp


def sign(n):
    return 1 if n % 2 == 0 else -1


def multiply(g, h):
    m, n = g
    p, q = h
    return m + sign(n)*p, n+q


def inverse(g):
    m, n = g
    return -sign(n)*m, -n


def twist(g):
    m, n = g
    return m+n % 2, n


def affine(m, n, parity):
    return sp.Matrix([[1, 0, n/2], [0, (-1)**parity, m], [0, 0, 1]])


def main():
    m, p, k, l = sp.symbols('m p k l', integer=True)
    a = sp.Matrix([[1, 0, 0], [0, 1, 1], [0, 0, 1]])
    b = sp.Matrix([[1, 0, sp.Rational(1, 2)], [0, -1, 0], [0, 0, 1]])
    f = sp.Matrix([[1, 0, 0], [0, 1, sp.Rational(1, 2)], [0, 0, 1]])
    assert b*a*b.inv() == a.inv()
    assert f*a*f.inv() == a
    assert f*b*f.inv() == a*b
    assert f*(b*b) == (b*b)*f
    assert f*f == a
    reversal = sp.diag(-1, -1, 1)
    assert reversal*a*reversal.inv() == a.inv()
    assert reversal*b*reversal.inv() == b.inv()
    assert reversal[:2, :2] == -sp.eye(2)
    symbolic = []
    for r, s in product(range(2), repeat=2):
        n, q = 2*k+r, 2*l+s
        g, h = affine(m, n, r), affine(p, q, s)
        assert sp.simplify(g*h-affine(m+(-1)**r*p, n+q, (r+s) % 2)) == sp.zeros(3)
        assert sp.simplify(f*g*f.inv()-affine(m+r, n, r)) == sp.zeros(3)
        assert sp.simplify(g*b*g.inv()-a**(2*m)*b) == sp.zeros(3)
        symbolic.append({'first_parity': r, 'second_parity': s,
                         'product_identity': True, 'half_translation_conjugacy': True,
                         'inner_b_even_vertical_shift': True})

    elements = list(product(range(-3, 4), repeat=2))
    for g, h in product(elements, repeat=2):
        assert multiply(g, inverse(g)) == (0, 0)
        assert twist(multiply(g, h)) == multiply(twist(g), twist(h))
        assert multiply(multiply(g, (0, 1)), inverse(g))[0] % 2 == 0
    for m0, n0 in elements:
        assert twist((m0, 2*n0)) == (m0, 2*n0)
        assert multiply(multiply((1, 0), (m0, n0)), (-1, 0)) == twist(twist((m0, n0)))
    assert twist((0, 1)) == (1, 1)
    assert twist((0, 1))[0] % 2 == 1
    # Mutating the displacement to an even shift destroys the non-inner witness.
    assert all((g[0]+2*(g[1] % 2), g[1]) ==
               multiply(multiply((1, 0), g), (-1, 0)) for g in elements)

    d = sp.diag(1, -1)
    phi = sp.Matrix([[1, 2], [0, 1]])
    assert phi*d != d*phi
    centraliser = [sp.diag(s, t) for s, t in product([-1, 1], repeat=2)]
    positive = [v for v in centraliser if v.det() == 1]
    assert positive == [-sp.eye(2), sp.eye(2)]
    assert f[:2, :2] == sp.eye(2)
    print(json.dumps({'status': 'passed', 'arithmetic': 'exact integer and symbolic rational',
                      'affine_symbolic_parity_cases': symbolic, 'normal_form_pairs': len(elements)**2,
                      'cover_elements_checked': len(elements),
                      'witness': {'torus_lift': 'F(x,y)=(x,y+1/2)', 'deck': 'tau(x,y)=(x+1/2,-y)',
                                  'cover_homology_matrix': [[1, 0], [0, 1]], 'trace': 2,
                                  'normal_form_action': '(m,n) -> (m + n mod 2, n)',
                                  'twist_b': [1, 1], 'inner_b': '(2*m,1)',
                                  'square': 'inner conjugation by a; F^2 is the vertical deck translation'},
                      'negative_identity_realization': 'R(x,y)=(-x,-y), with R a R^-1=a^-1 and R b R^-1=b^-1',
                      'parabolic_obstruction_retained': True,
                      'canonical_orientation_preserving_matrix_candidates': [matrix.tolist() for matrix in positive],
                      'correction': 'Identity cover homology does not imply an inner automorphism or trivial Klein mapping class.',
                      'scope': 'The algebraic model and affine identities are explicit; full surface topology is not formalized here.'}, indent=2, default=str))


if __name__ == '__main__':
    main()
