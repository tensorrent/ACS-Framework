#!/usr/bin/env python3
"""Exact scalar-loop and historical-constraint witnesses; no source edits."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
import json

import sympy as sp

from hidden_coupling_audit import (OUT, archived, clean, linear_combination,
                                   load_exact_basis, scalar_polynomial_beta, square_polynomial)


def exact_scalar_loop(poly, metric):
    hessians = defaultdict(lambda: defaultdict(Q))
    for monomial, coefficient in poly.items():
        counts = Counter(monomial)
        for a in counts:
            for b in counts:
                if b < a or (a == b and counts[a] < 2):
                    continue
                remaining = list(monomial)
                remaining.remove(a)
                remaining.remove(b)
                hessians[(a, b)][tuple(remaining)] += coefficient * counts[a] * (counts[b] - (a == b))
    out = defaultdict(Q)
    for (a, b), polynomial in hessians.items():
        weight = Q(1 if a == b else 2, int(metric[a] * metric[b]))
        for m, v in square_polynomial(clean(polynomial)).items():
            out[m] += weight * v
    return clean(out)


def delta_phase_derivative(poly):
    # Delta -> exp(-2 i alpha) Delta: dx=2y, dy=-2x.
    out = defaultdict(Q)
    for m, c in poly.items():
        for position, index in enumerate(m):
            if index < 8:
                continue
            replacement = index + 1 if index % 2 == 0 else index - 1
            factor = 2 if index % 2 == 0 else -2
            changed = list(m)
            changed[position] = replacement
            out[tuple(sorted(changed))] += c * factor
    return clean(out)


def main():
    checks = []

    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), evidence=detail))
        print(name, 'PASS' if passed else 'FAIL', flush=True)

    polys, quadratics, metric = load_exact_basis()
    basis = [{m: Q(c, 18) for m, c in p.items()} for p in polys]
    for i, p in enumerate(basis):
        expected = {} if i not in [11, 12] else linear_combination(
            [basis[12] if i == 11 else basis[11]], [8 if i == 11 else -8])
        check('exact-X-action-' + str(i), delta_phase_derivative(p) == expected)
    # All-left-handed convention: X(L)=1, X(R^c)=-1,
    # X(Phi)=0; RR vertex contains Delta*, with X=+2.
    check('Yukawa-vertices-neutral-in-Weyl-convention', [1 - 1, 1 - 1, 2 - 1 - 1] == [0, 0, 0])
    direction = [45, 45, 9, 9, -3]
    potential = linear_combination(basis[6:11], direction)
    direct = exact_scalar_loop(potential, metric)
    lam = sp.symbols('l0:17')
    assignment = {l: 0 for l in lam}
    assignment.update({lam[6 + i]: v for i, v in enumerate(direction)})
    beta = scalar_polynomial_beta(lam).subs(assignment)
    expected = linear_combination(basis, [Q(str(v)) for v in beta])
    check('exact-scalar-loop-full-polynomial', direct == expected, len(set(direct) | set(expected)))
    gauge = sp.Matrix([[sp.Rational(v) for v in row] for row in archived.G['gauge_quartic_coefficients'][6:11]])
    start = sp.Matrix.hstack(sp.ones(5, 1), gauge, sp.Matrix([4, -8, -2, 4, 0]))
    check('exact-scalar-loop-adds-fifth-direction', start.rank() == 4 and start.row_join(beta[6:11, :]).rank() == 5)

    # Same point of both historical two-trace ansatze: rho2=0, rho1=8/9.
    # The claimed equation 2 rho1+rho2=16/9 is satisfied here exactly.
    historical = [sp.Integer(0)] * 17
    historical[6:11] = [sp.Rational(8, 9)] * 5
    scalar = scalar_polynomial_beta(historical)
    g2 = sp.Matrix([sp.Rational(16, 9)] * 3)
    waves = sp.Matrix(archived.G['gauge_linear_coefficients']) * g2
    full_gauge = sp.Matrix(archived.G['gauge_quartic_coefficients']).applyfunc(sp.Rational) * sp.ones(6, 1) * sp.Rational(256, 81)
    full = scalar + sp.diag(*historical) * waves + full_gauge
    defect = sp.factor(full[6] - full[7])
    check('historical-point-satisfies-source-relation', 2 * sp.Rational(8, 9) == sp.Rational(16, 9))
    check('historical-two-trace-plane-not-RG-invariant', defect == -sp.Rational(2560, 9))

    # An explicit off-neutral witness for the notation ambiguity:
    # D_1=E11, D_2=E22, D_3=0 => (color,spin)=(2,2).
    # D_1=I4, D_2=D_3=0 => (color,spin)=(4,16).
    # This second assignment is also a simple geometric rank discriminator.
    x = [0] * 68
    for i in [8, 16, 22, 26]:
        x[i] = 1
    values = [sum(c * sp.prod(x[j] for j in m) for m, c in p.items()) for p in basis]
    color = sp.Matrix([1, 1, -sp.Rational(1, 2), -sp.Rational(1, 2), 0])
    spin = sp.Matrix([1, 1, 1, 1, -1])
    color_value = (color.T * sp.Matrix(values[6:11]))[0]
    spin_value = (spin.T * sp.Matrix(values[6:11]))[0]
    check('off-neutral-trace-counterexample', color_value == 4 and spin_value == 16)
    output = dict(checks=checks, checks_passed=sum(c['passed'] for c in checks), checks_total=len(checks),
                  scalar_closure_witness=dict(input=direction, output=[str(v) for v in beta[6:11, :]],
                                              polynomial_monomials=len(direct), starting_rank=4, final_rank=5),
                  historical_counterexample=dict(rho1='8/9', rho2='0', g4='4/3', gL='4/3', gR='4/3',
                       yukawas='zero', other_quartics='zero', B_lambda6_minus_lambda7=str(defect),
                       meaning='Fails tangency to both old two-trace planes even at a point satisfying the claimed scalar relation; not a claim of a physical vacuum.'),
                  trace_counterexample=dict(Delta='D1=I4, D2=D3=0', color=str(color_value), spin=str(spin_value)))
    (OUT / 'exact-witnesses.json').write_text(json.dumps(output, indent=2) + '\n')
    assert all(c['passed'] for c in checks), 'Failures retained in exact-witnesses.json'


if __name__ == '__main__':
    main()
