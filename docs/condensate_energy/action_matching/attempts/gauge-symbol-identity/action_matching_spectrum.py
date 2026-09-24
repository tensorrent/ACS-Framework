#!/usr/bin/env python3
"""Exact Delta-breaking spectrum and test of the historical Palatini pairing."""
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

import numpy as np
import sympy as s

from canonical_scalar_action import ROOT, load_exact_basis, basis_derivatives
from hidden_coupling_audit import gauge_matrices

OUT = ROOT / 'docs/condensate_energy/action_matching'


def hessian_at_integer_vacuum(poly, vacuum, divisor=1):
    h = s.zeros(68)
    for monomial, coefficient in poly.items():
        counts = Counter(monomial)
        for a in counts:
            for b in counts:
                multiplier = counts[a] * (counts[b] - (a == b))
                if not multiplier:
                    continue
                remaining = list(monomial)
                remaining.remove(a)
                remaining.remove(b)
                value = s.prod(vacuum[i] for i in remaining)
                if value:
                    h[a, b] += s.Rational(coefficient, divisor) * multiplier * value
    return h


def delta_vector(i, j, spin, phase=1):
    vector = s.zeros(68, 1)
    entries = {'minus': [1, -s.I, 0], 'zero': [0, 0, 1], 'plus': [1, s.I, 0]}[spin]
    cursor = 8
    for a in range(3):
        for k in range(4):
            for l in range(k, 4):
                if (k, l) == (i, j):
                    value = s.expand(phase * entries[a])
                    vector[cursor], vector[cursor + 1] = s.re(value), s.im(value)
                cursor += 2
    return vector


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    checks = []

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL', flush=True)

    polynomials, quadratics, metric = load_exact_basis()
    G = s.diag(*[int(v) for v in metric])
    x = delta_vector(3, 3, 'minus')
    # This exact rational vacuum has NDelta=2, i.e. physical d=sqrt(2).
    # Every quoted mass is divided by d^2=2 below.
    quartic_hessians = [hessian_at_integer_vacuum(p, x, 18) for p in polynomials]
    qh = hessian_at_integer_vacuum(quadratics[3], x)
    delta_hessians = [quartic_hessians[i] - (4 * qh if i == 7 else s.zeros(68)) for i in range(6, 11)]
    check('holomorphic-pair-has-no-quadratic-term', quartic_hessians[11] == quartic_hessians[12] == s.zeros(68))
    check('stationarity-mDelta-equals-minus-two-lambda7-d2', all(h * x == (8 * G * x if i == 1 else s.zeros(68, 1))
          for i, h in enumerate(delta_hessians)))
    couplings = s.symbols('l6:11', real=True)
    sectors, all_vectors, all_eigenvalues = [], [], []
    for color_name, colors, color_charge in [
            ('bar6', [(i, j) for i in range(3) for j in range(i, 3)], -s.Rational(1, 3)),
            ('bar3', [(i, 3) for i in range(3)], s.Rational(1, 3)),
            ('singlet', [(3, 3)], s.Integer(1))]:
        for spin, weight in [('minus', -1), ('zero', 0), ('plus', 1)]:
            for phase_name, phase in [('real', 1), ('imaginary', s.I)]:
                formulas, residuals = [], []
                for i, j in colors:
                    v = delta_vector(i, j, spin, phase)
                    norm = (v.T * G * v)[0]
                    coefficients = [s.factor((v.T * h * v)[0] / norm / 2) for h in delta_hessians]
                    formula = sum(a * b for a, b in zip(coefficients, couplings))
                    formulas.append(formula)
                    residuals += [h * v - 2 * c * G * v for h, c in zip(delta_hessians, coefficients)]
                    all_vectors.append(v[8:, :])
                    all_eigenvalues.append(2 * formula)
                check(f'eigenvectors-{color_name}-{spin}-{phase_name}', all(r == s.zeros(68, 1) for r in residuals)
                      and len(set(formulas)) == 1)
                sectors.append(dict(color=color_name, hypercharge=str(color_charge + weight), spin=spin,
                    phase=phase_name, real_multiplicity=len(colors), mass_squared_over_d2=str(s.factor(formulas[0])),
                    coefficients=[str(s.diff(formulas[0], l)) for l in couplings],
                    zero_identically=formulas[0] == 0))
    vectors = s.Matrix.hstack(*all_vectors)
    check('sixty-complete-independent-Delta-eigenvectors', vectors.shape == (60, 60) and vectors.rank() == 60)
    check('nine-Goldstones-fifty-one-other-modes', sum(row['real_multiplicity'] for row in sectors if row['zero_identically']) == 9)
    radial = next(row for row in sectors if row['color'] == 'singlet' and row['spin'] == 'minus' and row['phase'] == 'real')
    check('radial-mass-four-lambda7-d2', s.sympify(radial['mass_squared_over_d2'], locals=dict(zip(map(str, couplings), couplings))) == 4 * couplings[1])
    transverse = [row for row in sectors if row is not radial]
    check('isotropic-shift-leaves-all-transverse-masses-invariant',
          all(sum(s.Rational(c) for c in row['coefficients']) == 0 for row in transverse))

    g4, gL, gR, z = s.symbols('g4 gL gR z', real=True)
    gauges = [g4, gL, gR]
    matrices, groups, weights = gauge_matrices()
    directions = []
    for m, group, weight in zip(matrices, groups, weights):
        exact = s.Matrix((2 * m).astype(int).tolist()) / 2
        directions.append(exact * x * gauges[group] * s.sqrt(s.Rational(weight.numerator, weight.denominator)))
    orbit = s.Matrix.hstack(*directions)
    gram = orbit.T * G * orbit
    expected = z ** 12 * (z - 2 * g4 ** 2) ** 6 * (z - 2 * gR ** 2) ** 2 * (z - 2 * (3 * g4 ** 2 + 2 * gR ** 2))
    check('exact-gauge-spectrum', s.factor(gram.charpoly(z).as_expr() - expected) == 0)
    ungauged_orbit = orbit.subs({g4: 1, gL: 1, gR: 1})
    check('all-gauge-orbit-directions-are-Hessian-zeros', all(h * ungauged_orbit == s.zeros(68, 21) for h in delta_hessians))
    check('nine-broken-generators', ungauged_orbit.rank() == 9)

    sample = {couplings[0]: s.Rational(6, 5), couplings[1]: 1,
              couplings[2]: s.Rational(6, 5), couplings[3]: s.Rational(6, 5), couplings[4]: s.Rational(6, 5)}
    lam = np.zeros(17)
    lam[6:11] = [float(sample[c]) for c in couplings]
    masses = np.array([0., 0., 0., -4.])
    vals, grads, hess = basis_derivatives(polynomials, quadratics, np.array(x, float).ravel())
    raw = np.einsum('i,ijk->jk', np.r_[lam, masses], hess)[8:, 8:]
    hc = raw / np.sqrt(metric[8:, None] * metric[None, 8:])
    numeric = np.linalg.eigvalsh(hc)
    predicted = np.sort([float(e.subs(sample)) for e in all_eigenvalues])
    check('independent-numerical-spectrum', max(abs(numeric - predicted)) < 1e-11, float(max(abs(numeric - predicted))))
    check('explicit-positive-physical-Delta-example', sum(numeric > 1e-8) == 51 and sum(abs(numeric) < 1e-8) == 9)

    r1, r2 = s.symbols('rho1 rho2', real=True)
    mappings = {'color_gram': [r1 + r2, r1 + r2, r1 - r2 / 2, r1 - r2 / 2, r1],
                'spin_gram': [r1 + r2, r1 + r2, r1 + r2, r1 + r2, r1 - r2]}
    history = {}
    for name, mapping in mappings.items():
        rows = []
        for sector in sectors:
            expr = sum(s.Rational(c) * v for c, v in zip(sector['coefficients'], mapping))
            rows.append(dict(color=sector['color'], hypercharge=sector['hypercharge'], phase=sector['phase'],
                real_multiplicity=sector['real_multiplicity'], mass_squared_over_d2=str(s.factor(expr)),
                on_claimed_relation=str(s.factor(expr.subs(r2, s.Rational(16, 9) - 2 * r1)))))
        check(f'{name}-no-claimed-scalar-mass-identity', all(s.expand(s.sympify(row['mass_squared_over_d2'], locals={'rho1': r1, 'rho2': r2}) - (2 * r1 + r2)) != 0 for row in rows))
        at_half = [float(s.sympify(row['on_claimed_relation'], locals={'rho1': r1}).subs(r1, s.Rational(1, 2))) for row in rows]
        counts = dict(negative=sum(row['real_multiplicity'] for row, m in zip(rows, at_half) if m < -1e-12),
                      zero=sum(row['real_multiplicity'] for row, m in zip(rows, at_half) if abs(m) <= 1e-12),
                      positive=sum(row['real_multiplicity'] for row, m in zip(rows, at_half) if m > 1e-12))
        check(f'{name}-old-positive-rho2-range-has-instability', counts['negative'] > 0)
        history[name] = dict(sectors=rows, at_rho1_half=counts)
    output = dict(checks=checks, checks_passed=sum(c['passed'] for c in checks), checks_total=len(checks),
        convention='Phi=0; Delta=(1,-i,0)d E44/sqrt(2), NDelta=d^2; reported masses divided by d^2; zero-based invariant indices.',
        stationarity='mDelta=-2 lambda7 d^2', sectors=sectors,
        gauge_spectrum_over_d2=[dict(mass='0', multiplicity=12), dict(mass='g4^2', multiplicity=6),
                              dict(mass='gR^2', multiplicity=2), dict(mass='3g4^2+2gR^2', multiplicity=1)],
        generic_stable_example=dict(lambda6_to_lambda10=[str(sample[c]) for c in couplings], positive_physical_modes=51,
             boundedness='V = (NDelta-d^2)^2 + (1/5)(I6+I8+I9+I10), up to a constant; all summands nonnegative; holomorphic pair zero.'),
        historical_trace_models=history,
        scope='Exact tree-level first-stage Delta and gauge spectrum. Phi masses and later electroweak breaking are not included in the count of 51 physical Delta modes.')
    (OUT / 'spectrum.json').write_text(json.dumps(output, indent=2) + '\n')
    assert all(c['passed'] for c in checks), 'Failed checks preserved in spectrum.json'


if __name__ == '__main__':
    main()
