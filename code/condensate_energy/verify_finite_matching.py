#!/usr/bin/env python3
"""Independent limits, two-point integrals and matching-scale tests."""
from dataclasses import asdict, replace
import json
import math

import mpmath as mp
import numpy as np
from scipy.integrate import quad

from canonical_scalar_action import load_exact_basis, polynomial_derivatives
from hidden_coupling_audit import gauge_matrices, linear_combination
from radiative_flat_modes import gauge_gram
from finite_light_matching import (OUT, Parameters, couplings, background, heavy_jets,
    threshold, closed_spectra, loop_potential, low_potential, rg_check)


def mp_parameters(p):
    values = asdict(p)
    return Parameters(**{key: tuple(mp.mpf(str(v)) for v in value) if isinstance(value, tuple)
                          else mp.mpf(str(value)) for key, value in values.items()})


def precise_thresholds(p):
    mass, quartic = mp.mpf(0), mp.mpf(0)
    for row in heavy_jets(p):
        M, a, b, n = [row[k] for k in ['M2', 'a', 'b', 'multiplicity']]
        c = mp.mpf(5) / 6 if row['sector'] == 'vector' else mp.mpf(3) / 2
        L = mp.log(M / p.mu ** 2)
        mass += n * M * a * (L - c + mp.mpf(1) / 2) / (16 * mp.pi ** 2)
        quartic += n * (2 * M * b * (L - c + mp.mpf(1) / 2)
                       + a * a * (L - c + mp.mpf(3) / 2)) / (16 * mp.pi ** 2)
    return mass, quartic


def main():
    checks, result = [], {}

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL', flush=True)

    source = json.loads((OUT / 'matching.json').read_text())
    mp.mp.dps = 80
    limits = []
    for example in source['examples']:
        p = Parameters(**{k: tuple(v) if isinstance(v, list) else v for k, v in example['parameters'].items()})
        precise = mp_parameters(p)
        expected_m, expected_l = precise_thresholds(precise)
        vacuum = loop_potential(precise, closed_spectra(precise, mp.mpf(0), mp), mp)
        values = []
        for h in map(mp.mpf, ['.01', '.003', '.001', '.0003', '.0001']):
            full = loop_potential(precise, closed_spectra(precise, h, mp), mp)
            soft = low_potential(precise, h, mp)
            hard = full - soft - vacuum
            measured_m = 2 * hard / h ** 2
            measured_l = 4 * (hard - expected_m * h ** 2 / 2) / h ** 4
            naive_l = 4 * (full - vacuum - expected_m * h ** 2 / 2) / h ** 4
            values.append(dict(h=float(h), mass_estimate=float(measured_m), quartic_estimate=float(measured_l),
                mass_error=float(abs(measured_m - expected_m)), quartic_error=float(abs(measured_l - expected_l)),
                without_light_subtraction=float(naive_l)))
        label = example['label']
        check(label + '-80-digit-mass-limit', values[-1]['mass_error'] < 1e-10,
              [v['mass_error'] for v in values])
        check(label + '-80-digit-subtracted-quartic-limit', values[-1]['quartic_error'] < 1e-8 and
              all(a['quartic_error'] > b['quartic_error'] for a, b in zip(values, values[1:])),
              [v['quartic_error'] for v in values])
        check(label + '-unsubtracted-potential-is-not-a-threshold',
              abs(values[-1]['without_light_subtraction'] - values[-2]['without_light_subtraction']) > 1e-4)
        check(label + '-double-vs-80-digit-coefficients',
              abs(float(expected_m) - example['threshold']['mass_threshold']) < 1e-13 and
              abs(float(expected_l) - example['threshold']['potential_quartic_threshold']) < 1e-13)
        rg, th = rg_check(p), threshold(p)
        scales = []
        for t in [-.7, 0., .7]:
            moved = threshold(replace(p, mu=p.mu * math.exp(t)))
            matched_lambda = p.light + rg['tree_derivative'] * t + moved['total_quartic_threshold']
            expected_lambda = th['canonical_quartic'] + rg['low_beta'] * t
            matched_mass = rg['mass_tree_derivative'] * t + moved['mass_threshold']
            scales.append(dict(log_scale_ratio=t, matched_lambda=matched_lambda,
                EFT_run_lambda=expected_lambda, matched_mass=matched_mass,
                quartic_error=abs(matched_lambda - expected_lambda), mass_error=abs(matched_mass - th['mass_threshold'])))
        check(label + '-fixed-boundary-scale-transport', max(max(r['quartic_error'], r['mass_error']) for r in scales) < 1e-12)
        rescaled = threshold(replace(p, d=2 * p.d, mu=2 * p.mu, second_doublet_mass2=4 * p.second_doublet_mass2))
        check(label + '-dimensionful-unit-rescaling', abs(rescaled['canonical_quartic'] - th['canonical_quartic']) < 1e-13 and
              abs(rescaled['mass_threshold'] - 4 * th['mass_threshold']) < 1e-13)
        limits.append(dict(label=label, limits=values, expected_mass=str(expected_m),
            expected_potential_quartic=str(expected_l), scale_transport=scales))
    result['high_precision_and_scale'] = limits

    p = Parameters()
    polys, quadratics, metric = load_exact_basis()
    matrices, groups, weights = gauge_matrices()
    x0 = background(p, 0.)
    g0 = gauge_gram(x0, p.gauges, metric, matrices, groups, weights)
    eigenvalues, eigenvectors = np.linalg.eigh(g0)
    light = np.zeros(68)
    light[0] = light[6] = .5
    actions = np.column_stack([np.sqrt(metric) * (m @ light) * p.gauges[group] * math.sqrt(float(w))
                               for m, group, w in zip(matrices, groups, weights)])
    g4, gL, gR = p.gauges
    T = 3 * g4 ** 2 + 2 * gR ** 2
    generator_rows = []
    for name, M, target in [('color', g4 ** 2 * p.d ** 2, 0.),
                            ('right', gR ** 2 * p.d ** 2, gR ** 2 / 2),
                            ('neutral', T * p.d ** 2, gR ** 4 / (2 * T))]:
        selected = eigenvectors[:, abs(eigenvalues - M) < 1e-10]
        actual = float(np.sum((actions @ selected) ** 2))
        check(name + '-heavy-vector-light-generator-weight', abs(actual - target) < 1e-13, actual)
        generator_rows.append(dict(group=name, squared_mass=M, component_weight=actual, expected_weight=target))
    result['vector_two_point_weights'] = generator_rows

    lam, masses, _, _, _ = couplings(p)
    poly = linear_combination(polys, lam / 18)
    qpoly = linear_combination(quadratics, masses)
    radial = np.sqrt(metric) * x0 / (math.sqrt(2) * p.d)
    elight = np.sqrt(metric) * light
    small = 1e-5
    hessians = []
    for h in [small, -small]:
        x = background(p, h)
        hessians.append((polynomial_derivatives(poly, x)[2] + polynomial_derivatives(qpoly, x)[2]) /
                        np.sqrt(metric[:, None] * metric[None, :]))
    cubic = float(elight @ ((hessians[0] - hessians[1]) / (2 * small)) @ radial)
    check('component-cubic-for-scalar-kinetic-loop', abs(cubic - math.sqrt(2) * p.portal * p.d) < 1e-10, cubic)
    two_point_rows = []
    for M, a, y, mu in [(4 * p.lam7 * p.d ** 2, cubic, .14, 1.), (.3, .21, .19, .7)]:
        Bzero = 1 - math.log(M / mu ** 2)

        def B(q):
            return Bzero - quad(lambda x: math.log1p((1 - x) * q / M), 0., 1., epsabs=1e-13)[0]

        estimates = []
        for fraction in [1e-2, 1e-3, 1e-4]:
            q = M * fraction
            scalar = -a ** 2 * (B(q) - B(-q)) / (2 * q * 16 * np.pi ** 2)
            fermion = y ** 2 * ((M + q) * B(q) - (M - q) * B(-q)) / (2 * q * 16 * np.pi ** 2)
            estimates.append(dict(fraction=fraction, scalar=scalar, fermion=fermion))
        scalar_exact = a ** 2 / (32 * np.pi ** 2 * M)
        fermion_exact = y ** 2 * (.5 - math.log(M / mu ** 2)) / (16 * np.pi ** 2)
        check('regulated-two-point-quadrature-M-' + str(M),
              abs(estimates[-1]['scalar'] - scalar_exact) < 1e-10 and abs(estimates[-1]['fermion'] - fermion_exact) < 1e-10)
        two_point_rows.append(dict(M2=M, cubic=a, Yukawa=y, mu=mu, estimates=estimates,
                                  scalar_exact=scalar_exact, fermion_exact=fermion_exact))
    result['two_point_integrals'] = two_point_rows

    # Primary-source limits: Haisch et al. (11) uses field rescaling ZH,
    # half the kinetic coefficient delta_Z used here. Zhang-Zhou (90), m^2=0.
    A, M = math.sqrt(2) * p.portal * p.d, 4 * p.lam7 * p.d ** 2
    haisch_kinetic = 2 * A ** 2 / (4 * M) / (16 * np.pi ** 2)
    check('singlet-primary-source-kinetic-convention', abs(haisch_kinetic - threshold(p)['kinetic']['scalar']) < 1e-14)
    zero_portal = replace(p, portal=0.)
    th = threshold(zero_portal)
    primary = sum(-y ** 4 * (1 + math.log(2 * f ** 2 * p.d ** 2 / p.mu ** 2))
                  - p.lambda0 * y ** 2 * (1 - 2 * math.log(2 * f ** 2 * p.d ** 2 / p.mu ** 2))
                  for f, y in zip(p.majorana, p.dirac)) / (16 * np.pi ** 2)
    derived = sum(r['potential_quartic_threshold'] for r in th['rows'] if r['sector'] == 'fermion') - 2 * p.lambda0 * th['kinetic']['fermion']
    check('seesaw-primary-source-diagonal-limit', abs(primary - derived) < 1e-14)
    result['primary_sources'] = ['https://arxiv.org/html/2003.05936v2 (11), field-rescaling convention',
        'https://arxiv.org/html/2107.12133v2 (90), zero-light-mass diagonal-flavor limit']
    result['checks'] = checks
    result['checks_passed'] = sum(c['passed'] for c in checks)
    result['checks_total'] = len(checks)
    (OUT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=result['checks_passed'], checks_total=len(checks))), flush=True)
    assert all(c['passed'] for c in checks), 'Failed checks retained in verification.json'


if __name__ == '__main__':
    main()
