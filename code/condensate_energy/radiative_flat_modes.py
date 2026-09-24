#!/usr/bin/env python3
"""Conditional one-loop lifting of exact tree-stationary ACS flat orbits.

No coefficient fitting. All masses use the inherited canonical kinetic metric.
This file adds a new experiment without modifying any sealed earlier source.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
import json
import math

import mpmath as mp
import numpy as np
from scipy.optimize import brentq, minimize_scalar
import sympy as s

from canonical_scalar_action import (ROOT, load_exact_basis, scalar_pack,
    scalar_unpack, polynomial_derivatives)
from hidden_coupling_audit import (gauge_matrices, linear_combination,
    scalar_polynomial_beta, archived, mass)

OUT = ROOT / 'docs/condensate_energy/radiative_flat_modes'


def orbit(kind, theta, d=1., derivative=False):
    c, t = math.cos(theta), math.sin(theta)
    if derivative:
        c, t = -t, c
    delta = np.zeros((3, 4, 4), complex)
    if kind == 'spin':
        delta[:, 3, 3] = d * np.array([c + t, -1j * (c - t), 0]) / math.sqrt(2)
    else:
        spin = np.array([1, -1j, 0]) / math.sqrt(2)
        delta[:, 0, 0], delta[:, 3, 3] = d * t * spin, d * c * spin
    return scalar_pack(np.zeros((2, 2), complex), delta)


def mapping(model, rho1, rho2, phi=.1, portal=.1):
    lam = [0] * 17
    lam[0], lam[13] = phi, portal
    lam[6:11] = ([rho1 + rho2, rho1 + rho2, rho1 - rho2 / 2,
                 rho1 - rho2 / 2, rho1] if model == 'color_gram' else
                [rho1 + rho2] * 4 + [rho1 - rho2])
    return lam


def symmetry_generator(kind):
    generator = np.zeros((68, 68), int)
    if kind == 'spin':
        for k in range(0, 20, 2):
            a, b = 8 + k, 28 + k
            generator[a, b + 1], generator[a + 1, b] = -1, 1
            generator[b, a + 1], generator[b + 1, a] = -1, 1
    else:
        for a in range(3):
            for phase in range(2):
                i, j = 8 + 20 * a + phase, 26 + 20 * a + phase
                generator[i, j], generator[j, i] = 1, -1
    return generator


def lie_derivative(poly, generator):
    out = defaultdict(Q)
    replacements = {i: [(j, int(generator[i, j])) for j in range(68) if generator[i, j]]
                    for i in range(68)}
    for monomial, coefficient in poly.items():
        for i, multiplicity in Counter(monomial).items():
            reduced = list(monomial)
            reduced.remove(i)
            for j, value in replacements[i]:
                out[tuple(sorted(reduced + [j]))] += coefficient * multiplicity * value
    return {m: v for m, v in out.items() if v}


def gauge_gram(x, gauges, metric, matrices, groups, weights):
    directions = np.column_stack([np.sqrt(metric) * (m @ x) * gauges[group] * math.sqrt(float(w))
                                  for m, group, w in zip(matrices, groups, weights)])
    return directions.T @ directions


def predicted_gauge(kind, theta, g4, gR, d=1.):
    a, b = g4 ** 2, gR ** 2
    total = 3 * a + 2 * b
    determinant = 6 * a * b if kind == 'spin' else 2 * a * (a + 2 * b)
    angle = math.sin(2 * theta)
    root = math.sqrt(max(0., total ** 2 - 4 * determinant * angle ** 2))
    heavy = (total + root) / 2
    # Product-over-heavy avoids cancellation in the light neutral eigenvalue.
    light = determinant * angle ** 2 / heavy if heavy else 0.
    if kind == 'spin':
        values = [0.] * 11 + [a] * 6 + [b * (1 + angle), b * (1 - angle)]
    else:
        values = [0.] * 7 + [a * (1 + angle), a * (1 - angle)]
        values += [a * math.sin(theta) ** 2] * 4 + [a * math.cos(theta) ** 2] * 4 + [b] * 2
    return np.sort(np.array(values + [heavy, light]) * d ** 2)


def predicted_fermion(theta, singular, d=1.):
    values = [0.] * (14 * len(singular))
    for f in singular:
        values += [2 * f ** 2 * d ** 2 * math.cos(theta) ** 2,
                   2 * f ** 2 * d ** 2 * math.sin(theta) ** 2]
    return np.sort(values)


def cw_sum(mass2, constant, mu):
    mass2 = np.asarray(mass2, float)
    if np.min(mass2, initial=0.) < -1e-10:
        raise ValueError('Tachyonic input is not a real stable-orbit CW potential')
    x = mass2[mass2 > 0]
    return float(np.sum(x ** 2 * (np.log(x / mu ** 2) - constant)))


def cw_angular(kind, theta, g4, gR, singular, d=1., mu=1.):
    return (3 * cw_sum(predicted_gauge(kind, theta, g4, gR, d), 5 / 6, mu)
            - 2 * cw_sum(predicted_fermion(theta, singular, d), 1.5, mu)) / (64 * np.pi ** 2)


def analytic_curvature(kind, g4, gR, singular, d=1., mu=1.):
    a, b, total = g4 ** 2, gR ** 2, 3 * g4 ** 2 + 2 * gR ** 2
    if kind == 'spin':
        gauge = b ** 2 * (3 * math.log(b * d ** 2 / mu ** 2) + 2)
        gauge -= 18 * a * b * (math.log(total * d ** 2 / mu ** 2) - 1 / 3)
    else:
        gauge = 3 * a ** 2 - 6 * a * (a + 2 * b) * (math.log(total * d ** 2 / mu ** 2) - 1 / 3)
    gauge *= d ** 2 / (8 * np.pi ** 2)
    fermion = d ** 2 / (4 * np.pi ** 2) * sum(
        f ** 4 * (math.log(2 * f ** 2 * d ** 2 / mu ** 2) - 1) for f in singular if f)
    return dict(gauge=gauge, fermion=fermion, total=gauge + fermion)


def mp_potential(kind, theta, g4, gR, singular, d, mu):
    a, b = g4 ** 2, gR ** 2
    total = 3 * a + 2 * b
    determinant = 6 * a * b if kind == 'spin' else 2 * a * (a + 2 * b)
    angle = mp.sin(2 * theta)
    heavy = (total + mp.sqrt(total ** 2 - 4 * determinant * angle ** 2)) / 2
    light = determinant * angle ** 2 / heavy
    if kind == 'spin':
        vectors = [a] * 6 + [b * (1 + angle), b * (1 - angle)]
    else:
        vectors = [a * (1 + angle), a * (1 - angle)]
        vectors += [a * mp.sin(theta) ** 2] * 4 + [a * mp.cos(theta) ** 2] * 4 + [b] * 2
    vectors += [heavy, light]
    fermions = [2 * f ** 2 * u ** 2 for f in singular for u in [mp.sin(theta), mp.cos(theta)]]

    def term(x, c):
        x *= d ** 2
        return x ** 2 * (mp.log(x / mu ** 2) - c) if x else mp.mpf(0)

    return (3 * sum(term(x, mp.mpf(5) / 6) for x in vectors)
            - 2 * sum(term(x, mp.mpf(3) / 2) for x in fermions)) / (64 * mp.pi ** 2)


def exact_characteristic(kind, matrices, groups, weights, metric):
    a, b, g4, gL, gR, z = s.symbols('a b g4 gL gR z', real=True)
    x = s.zeros(68, 1)
    if kind == 'spin':
        x[26], x[47] = a, -b
        norm = a * a + b * b
        expected = z ** 11 * (z - g4 ** 2 * norm) ** 6
        expected *= (z - 2 * gR ** 2 * a ** 2) * (z - 2 * gR ** 2 * b ** 2)
        product = 6 * g4 ** 2 * gR ** 2 * (a ** 2 - b ** 2) ** 2
    else:
        x[8], x[29], x[26], x[47] = a, -a, b, -b
        norm = 2 * (a * a + b * b)
        expected = z ** 7 * (z - 2 * g4 ** 2 * (a + b) ** 2) * (z - 2 * g4 ** 2 * (a - b) ** 2)
        expected *= (z - 2 * g4 ** 2 * a ** 2) ** 4 * (z - 2 * g4 ** 2 * b ** 2) ** 4
        expected *= (z - gR ** 2 * norm) ** 2
        product = 32 * g4 ** 2 * (g4 ** 2 + 2 * gR ** 2) * a ** 2 * b ** 2
    expected *= z ** 2 - (3 * g4 ** 2 + 2 * gR ** 2) * norm * z + product
    columns = []
    for m, group, weight in zip(matrices, groups, weights):
        exact = s.Matrix((2 * m).astype(int).tolist()) / 2
        columns.append(exact * x * [g4, gL, gR][group] * s.sqrt(s.Rational(weight.numerator, weight.denominator)))
    directions = s.Matrix.hstack(*columns)
    gram = (directions.T * s.diag(*map(int, metric)) * directions).applyfunc(s.factor)
    # Connected Gram blocks are exact; the largest is a small neutral block.
    remaining, blocks, actual = set(range(21)), [], s.Integer(1)
    while remaining:
        block, todo = set(), {min(remaining)}
        while todo:
            i = todo.pop()
            block.add(i)
            todo |= {j for j in remaining - block if gram[i, j] != 0}
        remaining -= block
        indices = sorted(block)
        polynomial = gram.extract(indices, indices).charpoly(z)
        actual *= polynomial.as_expr().subs(polynomial.gen, z)
        blocks.append(indices)
    return dict(passed=s.factor(actual - expected) == 0, characteristic=str(s.factor(expected)),
                variables='spin: D1=a E44,D2=-i b E44; color: (D1,D2)=(S,-i S), S=diag(a,0,0,b)',
                blocks=blocks)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    checks, result = [], {}

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL', flush=True)

    polys, quadratics, metric = load_exact_basis()
    matrices, groups, weights = gauge_matrices()
    result['exact_vector_spectra'] = {}
    for kind in ['spin', 'color']:
        exact = exact_characteristic(kind, matrices, groups, weights, metric)
        check(kind + '-exact-vector-characteristic', exact['passed'])
        result['exact_vector_spectra'][kind] = exact

    # Exact symmetries and scalar beta differences on each whole two-trace plane.
    r1, r2, ph, portal = s.symbols('rho1 rho2 lambda0 lambda13', real=True)
    symmetry_rows = []
    for model, kinds in [('color_gram', ['spin']), ('spin_gram', ['spin', 'color'])]:
        symbolic = mapping(model, r1, r2, ph, portal)
        beta_scalar = scalar_polynomial_beta(symbolic)
        for kind in kinds:
            index = 6 if kind == 'spin' else 9
            check(model + '-' + kind + '-scalar-beta-difference-zero', s.expand(beta_scalar[index] - beta_scalar[7]) == 0)
            gen = symmetry_generator(kind)
            check(model + '-' + kind + '-kinetic-symmetry', np.array_equal(metric[:, None] * gen + gen.T * metric[None, :], np.zeros((68, 68))))
            # Four independent coefficients establish the entire stated plane.
            for label, coeff in [('rho1', r1), ('rho2', r2), ('phi', ph), ('portal', portal)]:
                direction = [Q(str(s.diff(c, coeff))) for c in symbolic]
                polynomial = linear_combination(polys, [c / 18 for c in direction])
                check(model + '-' + kind + '-' + label + '-exact-potential-symmetry', not lie_derivative(polynomial, gen))
            check(model + '-' + kind + '-quadratic-symmetry',
                  not lie_derivative(quadratics[0], gen) and not lie_derivative(quadratics[3], gen))
            lam = mapping(model, Q(3, 10), Q(-1, 10), Q(1, 10), Q(1, 10))
            potential = linear_combination(polys, [c / 18 for c in lam])
            mu = [1, 0, 0, Q(-2, 5)]
            qpoly = linear_combination(quadratics, mu)
            spectra, gradients, energies, speeds = [], [], [], []
            for theta in [0., .12, .31, .65, math.pi / 4]:
                x = orbit(kind, theta)
                v4, grad4, h4 = polynomial_derivatives(potential, x)
                v2, grad2, h2 = polynomial_derivatives(qpoly, x)
                spectra.append(np.linalg.eigvalsh((h4 + h2) / np.sqrt(metric[:, None] * metric[None, :])))
                gradients.append(float(max(abs((grad4 + grad2) / np.sqrt(metric)))))
                energies.append(v4 + v2)
                dx = orbit(kind, theta, derivative=True)
                speeds.append(float(dx @ (metric * dx)))
            error = float(max(np.max(abs(row - spectra[0])) for row in spectra))
            check(model + '-' + kind + '-full-68-scalar-spectrum-constant', error < 1e-11, error)
            check(model + '-' + kind + '-stationary-entire-orbit', max(gradients) < 1e-12 and np.ptp(energies) < 1e-12, max(gradients))
            check(model + '-' + kind + '-canonical-speed-two-d2', max(abs(np.array(speeds) - 2)) < 1e-12)
            check(model + '-' + kind + '-no-negative-tree-scalar-mass', min(spectra[0]) > -1e-11)
            zeros = int(sum(abs(spectra[0]) < 1e-10))
            check(model + '-' + kind + '-expected-flat-count', zeros == (11 if model == 'color_gram' else 23), zeros)
            symmetry_rows.append(dict(model=model, orbit=kind, spectral_error=error, maximum_tadpole=max(gradients),
                tree_scalar_spectrum=spectra[0].tolist(), zeros_including_gauge=zeros))
    result['scalar_symmetry'] = symmetry_rows

    rng = np.random.default_rng(20260924)
    component_rows = []
    for families in [1, 3]:
        F = (rng.normal(size=(families, families)) + 1j * rng.normal(size=(families, families))) / 7
        F = (F + F.T) / 2
        Y = (rng.normal(size=(families, families)) + 1j * rng.normal(size=(families, families))) / 5
        Z = (rng.normal(size=(families, families)) + 1j * rng.normal(size=(families, families))) / 5
        singular = np.linalg.svd(F, compute_uv=False)
        for kind in ['spin', 'color']:
            residual_g, residual_f, residual_v = [], [], []
            for theta in [0., 1e-4, .17, .42, math.pi / 4]:
                d, mu = 1.37, .91
                gauges = [.3, .25, .35]
                x = orbit(kind, theta, d)
                gv = np.linalg.eigvalsh(gauge_gram(x, gauges, metric, matrices, groups, weights))
                phi, delta = scalar_unpack(x)
                fm = mass(phi, delta, Y, Z, F)
                fv = np.linalg.eigvalsh(fm.conj().T @ fm)
                pg = predicted_gauge(kind, theta, gauges[0], gauges[2], d)
                pf = predicted_fermion(theta, singular, d)
                residual_g.append(float(max(abs(gv - pg))))
                residual_f.append(float(max(abs(fv - pf))))
                component_potential = (3 * cw_sum(gv, 5 / 6, mu) - 2 * cw_sum(fv, 1.5, mu)) / (64 * np.pi ** 2)
                residual_v.append(abs(component_potential - cw_angular(kind, theta, gauges[0], gauges[2], singular, d, mu)))
            check(f'{kind}-{families}-family-component-vector-spectrum', max(residual_g) < 1e-12, max(residual_g))
            check(f'{kind}-{families}-family-full-Weyl-spectrum', max(residual_f) < 1e-12, max(residual_f))
            check(f'{kind}-{families}-family-component-CW-potential', max(residual_v) < 1e-12, max(residual_v))
            component_rows.append(dict(orbit=kind, families=families, vector_error=max(residual_g),
                Weyl_error=max(residual_f), potential_error=max(residual_v)))
    result['component_checks'] = component_rows

    # Exact gauge/fermion beta source, wave-term cancellation and scale identity.
    g4, gL, gR, d, mu, tf4 = s.symbols('g4 gL gR d mu TF4', positive=True)
    g2 = [g4 ** 2, gL ** 2, gR ** 2]
    gauge_beta = s.Matrix(archived.G['gauge_quartic_coefficients']).applyfunc(s.Rational) * s.Matrix(
        [g2[a] * g2[b] for a, b in archived.G['gauge_square_pairs']])
    beta_rows = {}
    for kind, index in [('spin', 6), ('color', 9)]:
        expected_g = -108 * g4 ** 2 * gR ** 2 + 18 * gR ** 4 if kind == 'spin' else -36 * g4 ** 4 - 72 * g4 ** 2 * gR ** 2
        check(kind + '-exact-gauge-beta-difference', s.expand(gauge_beta[index] - gauge_beta[7] - expected_g) == 0)
        nonzero_box = [row for row in archived.YUK['fermion_box'] if s.sympify(row['coefficients'][index]) - s.sympify(row['coefficients'][7]) != 0]
        check(kind + '-only-F-fourth-power-box-source', len(nonzero_box) == 1 and
            all(label.startswith('F') for label in nonzero_box[0]['trace_word']) and
            s.sympify(nonzero_box[0]['coefficients'][index]) - s.sympify(nonzero_box[0]['coefficients'][7]) == 12,
            [dict(word=row['trace_word'], difference=str(s.sympify(row['coefficients'][index]) - s.sympify(row['coefficients'][7]))) for row in nonzero_box])
        wave_by_word = defaultdict(lambda: s.Integer(0))
        symbolic = mapping('spin_gram', r1, r2, ph, portal)
        for row in archived.YUK['quartic_wave']:
            wave_by_word[tuple(row['trace_word'])] += symbolic[row['input_quartic']] * (s.sympify(row['coefficients'][index]) - s.sympify(row['coefficients'][7]))
        check(kind + '-Yukawa-wave-cancels-on-flat-boundary', all(s.expand(v) == 0 for v in wave_by_word.values()))
        check(kind + '-gauge-wave-cancels-on-flat-boundary', all(a == b for a, b in zip(archived.GL[index], archived.GL[7])))
        f = s.symbols('f', positive=True)
        log_heavy = s.log((3 * g4 ** 2 + 2 * gR ** 2) * d ** 2 / mu ** 2)
        gauge_mass = (gR ** 4 * (3 * s.log(gR ** 2 * d ** 2 / mu ** 2) + 2) - 18 * g4 ** 2 * gR ** 2 * (log_heavy - s.Rational(1, 3))) if kind == 'spin' else (3 * g4 ** 4 - 6 * g4 ** 2 * (g4 ** 2 + 2 * gR ** 2) * (log_heavy - s.Rational(1, 3)))
        gauge_mass *= d ** 2 / (8 * s.pi ** 2)
        fermion_mass = d ** 2 * f ** 4 * (s.log(2 * f ** 2 * d ** 2 / mu ** 2) - 1) / (4 * s.pi ** 2)
        explicit_derivative = mu * s.diff(gauge_mass + fermion_mass, mu)
        tree_running = s.Rational(4, 3) * d ** 2 * (expected_g + 12 * f ** 4) / (32 * s.pi ** 2)
        check(kind + '-exact-one-loop-scale-cancellation', s.simplify(explicit_derivative + tree_running) == 0)
        beta_rows[kind] = dict(beta_difference_32pi2=str(expected_g + 12 * tf4),
            gauge_curvature=str(gauge_mass), one_family_fermion_curvature=str(fermion_mass),
            tree_curvature='4 d^2 (lambda_index-lambda7)/3', index=index)
    result['analytic_formulas'] = beta_rows

    mp.mp.dps = 70
    mp_rows, component_curvatures = [], []
    for kind in ['spin', 'color']:
        for fvals in [[], [.3], [.12, .31, .47]]:
            g4n, gRn, dn, mun = .3, .35, 1.37, .91
            target = analytic_curvature(kind, g4n, gRn, fvals, dn, mun)['total']
            args = [mp.mpf(str(v)) for v in [g4n, gRn]]
            fs = [mp.mpf(str(v)) for v in fvals]
            dp, mup = mp.mpf(str(dn)), mp.mpf(str(mun))
            base = mp_potential(kind, mp.mpf(0), *args, fs, dp, mup)
            values, errors = [], []
            for step in ['.01', '.001', '.0001', '.00001']:
                h = mp.mpf(step)
                estimate = (mp_potential(kind, h, *args, fs, dp, mup) + mp_potential(kind, -h, *args, fs, dp, mup) - 2 * base) / (2 * dp ** 2 * h ** 2)
                values.append(float(estimate))
                errors.append(abs(float(estimate) - target))
            check(f'{kind}-{len(fs)}-family-70-digit-curvature-limit', errors[-1] < 3e-10 and all(a > b for a, b in zip(errors, errors[1:])), errors)
            mp_rows.append(dict(orbit=kind, singular=fvals, target=target, estimates=values, errors=errors))
        # Independent full matrix diagonalizations, not the predicted spectra.
        F = np.diag([.12, .31, .47]).astype(complex)
        zeros = np.zeros_like(F)

        def component_value(theta):
            x = orbit(kind, theta)
            gv = np.linalg.eigvalsh(gauge_gram(x, [.3, .25, .35], metric, matrices, groups, weights))
            phi, delta = scalar_unpack(x)
            fm = mass(phi, delta, zeros, zeros, F)
            fv = np.linalg.eigvalsh(fm.conj().T @ fm)
            return (3 * cw_sum(gv, 5 / 6, 1.) - 2 * cw_sum(fv, 1.5, 1.)) / (64 * np.pi ** 2)

        base = component_value(0.)
        target = analytic_curvature(kind, .3, .35, [.12, .31, .47])['total']
        errors = []
        for h in [.01, .0025, .000625]:
            estimate = (component_value(h) + component_value(-h) - 2 * base) / (2 * h ** 2)
            errors.append(abs(estimate - target))
        check(kind + '-independent-component-curvature-convergence', errors[-1] < 3e-8 and all(a > b for a, b in zip(errors, errors[1:])), errors)
        component_curvatures.append(dict(orbit=kind, target=target, errors=errors))
    result['high_precision_derivatives'] = mp_rows
    result['component_curvatures'] = component_curvatures

    examples = []
    for fvals in [[], [.3], [.5], [.3, .3, .3]]:
        row = dict(g4=.3, gR=.35, d=1., boundary_scale=1., Majorana_singular=fvals,
                   boundary_differences=dict(lambda6_minus_lambda7=0., lambda9_minus_lambda7=0.))
        for kind in ['spin', 'color']:
            parts = analytic_curvature(kind, .3, .35, fvals)
            beta = (-108 * .3 ** 2 * .35 ** 2 + 18 * .35 ** 4 if kind == 'spin' else -36 * .3 ** 4 - 72 * .3 ** 2 * .35 ** 2) + 12 * sum(f ** 4 for f in fvals)
            scale_values = []
            for scale in [.5, 1., 2.]:
                difference = beta * math.log(scale) / (32 * np.pi ** 2)
                scale_values.append(4 * difference / 3 + analytic_curvature(kind, .3, .35, fvals, mu=scale)['total'])
            check(kind + '-scale-cancel-example-' + str(fvals), np.ptp(scale_values) < 1e-14, scale_values)
            grid = np.linspace(0, np.pi / 4, 401)
            energy0 = cw_angular(kind, 0, .3, .35, fvals)
            energies = [cw_angular(kind, theta, .3, .35, fvals) - energy0 for theta in grid]
            imin = int(np.argmin(energies))
            candidates = [(float(grid[imin]), energies[imin])]
            if 0 < imin < len(grid) - 1:
                minimum = minimize_scalar(lambda theta: cw_angular(kind, theta, .3, .35, fvals) - energy0,
                    bounds=(grid[imin - 1], grid[imin + 1]), method='bounded', options=dict(xatol=1e-12))
                check(kind + '-sampled-minimizer-' + str(fvals), minimum.success)
                candidates.append((float(minimum.x), float(minimum.fun)))
            angle, value = min(candidates, key=lambda item: item[1])
            row[kind] = dict(**parts, scales=scale_values, sampled_minimum_angle=angle,
                sampled_minimum_energy_relative_to_neutral=value, angle_grid=grid.tolist(), energy_grid=energies,
                finite_boundary_difference_for_zero_curvature=-3 * parts['total'] / 4)
        examples.append(row)
    result['conditional_examples'] = examples
    thresholds = {}
    for kind in ['spin', 'color']:
        threshold = brentq(lambda f: analytic_curvature(kind, .3, .35, [f])['total'], .01, .8, xtol=1e-13)
        thresholds[kind] = threshold
        check(kind + '-conditional-one-family-sign-crossing', abs(analytic_curvature(kind, .3, .35, [threshold])['total']) < 1e-14)
    result['conditional_sign_crossings'] = thresholds
    result['representation_coverage'] = dict(spin=dict(SU3='singlet', hypercharge=2, real_modes=2),
        color=dict(SU3='bar6', hypercharge='-4/3', real_modes=12),
        qualification='Unbroken SU(3)xU(1) enforces degeneracy within each complex irrep and forbids their quadratic mixing. Color orbit is tree-flat only in spin-Gram model.')
    result['scope'] = ('Landau-gauge MS-bar one-loop effective-potential angular curvature with radial tadpole subtraction; '
        'rho1=.3,rho2=-.1, norm-only portal=.1, Phi mass coefficient=1 for scalar-spectrum tests. '
        'No momentum-dependent pole mass or full one-loop threshold matching. Boundary quartic differences, '
        'gauge/flavor couplings and boundary scale remain independent inputs; orbit scans are not global-vacuum proofs.')
    result['source'] = 'https://arxiv.org/html/hep-ph/0111209v2 : section 3, one-loop Landau-gauge MS-bar potential'
    result['checks'] = checks
    result['checks_passed'] = sum(c['passed'] for c in checks)
    result['checks_total'] = len(checks)
    (OUT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=result['checks_passed'], checks_total=len(checks))), flush=True)
    assert all(c['passed'] for c in checks), 'Failed checks preserved in results.json'


if __name__ == '__main__':
    main()
