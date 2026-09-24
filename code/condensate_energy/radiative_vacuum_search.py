#!/usr/bin/env python3
"""Search complete tree-minimum families; numerical candidates, not certificates."""
import json
import math
from fractions import Fraction as Q
from itertools import combinations, permutations

import numpy as np
from scipy.optimize import minimize

from canonical_scalar_action import load_exact_basis, scalar_pack, scalar_unpack, polynomial_derivatives
from hidden_coupling_audit import gauge_matrices, linear_combination, mass
from radiative_flat_modes import (OUT, mapping, gauge_gram, cw_sum, cw_angular)


def factored_field(q, theta, d=1.):
    spin = np.array([math.cos(theta) + math.sin(theta),
                     -1j * (math.cos(theta) - math.sin(theta)), 0]) / math.sqrt(2)
    delta = spin[:, None, None] * np.diag(d * np.sqrt(np.asarray(q, float)))[None, :, :]
    return scalar_pack(np.zeros((2, 2), complex), delta)


def vector_spectrum(q, theta, g4, gR, d=1.):
    q = np.asarray(q, float)
    root = np.sqrt(q)
    values = [0.] * 3
    for i, j in combinations(range(4), 2):
        values += [g4 ** 2 * (root[i] + root[j]) ** 2,
                   g4 ** 2 * (root[i] - root[j]) ** 2]
    values += [gR ** 2 * (1 + math.sin(2 * theta)), gR ** 2 * (1 - math.sin(2 * theta))]
    cartan = np.array([[1, -1, 0, 0], [1, 1, -2, 0], [1, 1, 1, -3]], float)
    cartan /= np.array([2., 2 * np.sqrt(3), 2 * np.sqrt(6)])[:, None]
    neutral = np.zeros((4, 4))
    neutral[:3, :3] = 8 * g4 ** 2 * (cartan * q) @ cartan.T
    neutral[:3, 3] = 4 * g4 * gR * math.cos(2 * theta) * (cartan @ q)
    neutral[3, :3] = neutral[:3, 3]
    neutral[3, 3] = 2 * gR ** 2
    values += list(np.linalg.eigvalsh(neutral))
    return np.sort(np.array(values) * d ** 2)


def fermion_spectrum(q, theta, singular, d=1.):
    values = [0.] * (8 * len(singular))
    for f in singular:
        for probability in q:
            values += [2 * f ** 2 * d ** 2 * probability * math.cos(theta) ** 2,
                       2 * f ** 2 * d ** 2 * probability * math.sin(theta) ** 2]
    return np.sort(values)


def effective_potential(q, theta, singular, g4=.3, gR=.35, d=1., mu=1.):
    return (3 * cw_sum(vector_spectrum(q, theta, g4, gR, d), 5 / 6, mu)
            - 2 * cw_sum(fermion_spectrum(q, theta, singular, d), 1.5, mu)) / (64 * np.pi ** 2)


def probabilities(angles):
    left, q = 1., []
    for angle in angles:
        q.append(left * math.cos(angle) ** 2)
        left *= math.sin(angle) ** 2
    q.append(left)
    return np.array(q + [0.] * (4 - len(q)))


def search_support(rank, singular, starts):
    bounds = [(0., math.pi / 4)] + [(0., math.pi / 2)] * (rank - 1)
    base = effective_potential([1, 0, 0, 0], 0., singular)

    def objective(values):
        return 1e4 * (effective_potential(probabilities(values[1:]), values[0], singular) - base)

    runs = []
    for start in starts:
        result = minimize(objective, start, method='L-BFGS-B', bounds=bounds,
                          options=dict(ftol=1e-13, gtol=1e-8, maxiter=500, maxls=40))
        q = probabilities(result.x[1:])
        runs.append(dict(success=bool(result.success), message=str(result.message),
            theta=float(result.x[0]), q=q.tolist(), energy_relative=float(result.fun / 1e4),
            iterations=int(result.nit), start=list(map(float, start))))
    successful = [r for r in runs if r['success']]
    return dict(rank=rank, successes=len(successful), attempts=len(runs),
                best=min(successful, key=lambda row: row['energy_relative']) if successful else None,
                runs=runs)


def main():
    checks, output = [], {}

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL', flush=True)

    polys, quadratics, metric = load_exact_basis()
    matrices, groups, weights = gauge_matrices()
    rng = np.random.default_rng(2026092402)
    lam = mapping('spin_gram', Q(3, 10), Q(-1, 10), Q(1, 10), Q(1, 10))
    potential = linear_combination(polys, [c / 18 for c in lam])
    qpoly = linear_combination(quadratics, [1, 0, 0, Q(-2, 5)])
    scalar_reference = None
    residuals = []
    for i in range(10):
        q = np.r_[rng.dirichlet(np.ones(1 + i % 4)), np.zeros(3 - i % 4)]
        theta = rng.uniform(0, np.pi / 4)
        x = factored_field(q, theta)
        v4, g4, h4 = polynomial_derivatives(potential, x)
        v2, g2, h2 = polynomial_derivatives(qpoly, x)
        scalar = np.linalg.eigvalsh((h4 + h2) / np.sqrt(metric[:, None] * metric[None, :]))
        if scalar_reference is None:
            scalar_reference = scalar
        check(f'general-family-{i}-scalar-stationarity-and-spectrum',
              max(abs(g4 + g2)) < 1e-12 and max(abs(scalar - scalar_reference)) < 1e-11 and abs(v4 + v2 + .2) < 1e-12)
        actual_gauge = np.linalg.eigvalsh(gauge_gram(x, [.3, .25, .35], metric, matrices, groups, weights))
        expected_gauge = vector_spectrum(q, theta, .3, .35)
        check(f'general-family-{i}-component-vector-spectrum', max(abs(actual_gauge - expected_gauge)) < 1e-12)
        families = 1 if i % 2 == 0 else 3
        F = rng.normal(size=(families, families)) + 1j * rng.normal(size=(families, families))
        F = (F + F.T) / 10
        Y = rng.normal(size=(families, families)) / 5
        Z = rng.normal(size=(families, families)) / 5
        phi, delta = scalar_unpack(x)
        M = mass(phi, delta, Y, Z, F)
        actual_fermion = np.linalg.eigvalsh(M.conj().T @ M)
        singular = np.linalg.svd(F, compute_uv=False)
        expected_fermion = fermion_spectrum(q, theta, singular)
        check(f'general-family-{i}-component-Weyl-spectrum', max(abs(actual_fermion - expected_fermion)) < 1e-12)
        actual_potential = (3 * cw_sum(actual_gauge, 5 / 6, 1.) - 2 * cw_sum(actual_fermion, 1.5, 1.)) / (64 * np.pi ** 2)
        expected_potential = effective_potential(q, theta, singular)
        permutation_values = [effective_potential(q[list(p)], theta, singular) for p in permutations(range(4))]
        check(f'general-family-{i}-CW-and-permutation-invariance', abs(actual_potential - expected_potential) < 1e-13 and np.ptp(permutation_values) < 1e-13)
        residuals.append(dict(q=q.tolist(), theta=theta, vector=float(max(abs(actual_gauge - expected_gauge))),
            fermion=float(max(abs(actual_fermion - expected_fermion))), potential=abs(actual_potential - expected_potential)))
    for kind in ['spin', 'color']:
        values = []
        for theta in np.linspace(0, np.pi / 4, 9):
            q, angle = ([1, 0, 0, 0], theta) if kind == 'spin' else ([math.sin(theta) ** 2, 0, 0, math.cos(theta) ** 2], 0.)
            values.append(abs(effective_potential(q, angle, [.12, .31, .47]) - cw_angular(kind, theta, .3, .35, [.12, .31, .47])))
        check(kind + '-previous-orbit-recovered', max(values) < 1e-13, max(values))
    output['component_residuals'] = residuals

    searches = []
    for singular in [[], [.3], [.5], [.3, .3, .3]]:
        supports = []
        for rank in range(1, 5):
            equal_angles = [math.acos(1 / math.sqrt(k)) for k in range(rank, 1, -1)]
            starts = [[angle] + equal_angles for angle in [0., .2, np.pi / 4]]
            starts += [list(rng.uniform(.02, .98, rank) * np.array([np.pi / 4] + [np.pi / 2] * (rank - 1))) for _ in range(13)]
            initial = search_support(rank, singular, starts)
            extra_starts = [list(rng.uniform(.001, .999, rank) * np.array([np.pi / 4] + [np.pi / 2] * (rank - 1))) for _ in range(32)]
            repeated = search_support(rank, singular, extra_starts)
            check(f'search-{singular}-rank-{rank}-has-successful-solves', initial['successes'] > 0 and repeated['successes'] > 0,
                  [initial['successes'], repeated['successes']])
            difference = abs(initial['best']['energy_relative'] - repeated['best']['energy_relative'])
            check(f'search-{singular}-rank-{rank}-denser-restart-agreement', difference < 1e-9, difference)
            best = min([initial['best'], repeated['best']], key=lambda row: row['energy_relative'])
            supports.append(dict(rank=rank, initial=initial, repeated=repeated, best=best))
        best = min([r['best'] for r in supports], key=lambda row: row['energy_relative'])
        searches.append(dict(Majorana_singular=singular, supports=supports, best=best))
        print('candidate', singular, best['q'], best['theta'], best['energy_relative'], flush=True)
    output['searches'] = searches
    output['search_scope'] = ('Complete rank-one spin-Gram tree-minimum family modulo gauge transformations and an overall '
        'phase invisible to the perturbative CW potential; theta in [0,pi/4], four Takagi weights q_i>=0, sum q_i=1. '
        'Every color support rank is searched, 16 starts followed by 32 independent starts per rank and input case. '
        'Agreement of multistart candidates is not a global-minimum certificate. Spin/color independent scalar symmetries '
        'make scalar CW constant. The color-Gram tree-minimum family restricts q to rank one, so its search is rank=1 only.')
    output['fixed_inputs'] = dict(g4=.3, gR=.35, d=1., renormalization_and_boundary_scale=1.,
        rho1=.3, rho2=-.1, Phi_mass_coefficient=1., Phi_norm_portal=.1,
        holomorphic_pair=[0, 0], other_hidden_boundary_differences='zero as in the two explicit trace models')
    output['limitations'] = ['Leading one-loop lifting on a tree-degenerate manifold only; no two-loop or momentum-dependent pole correction',
        'A lower-energy orbit point falsifies global neutral minimality, even without certifying the best candidate',
        'A positive local curvature is not proof of global neutral minimality',
        'Boundary coefficients and scales remain independent inputs; no uniquely selected ACS vacuum']
    output['checks'] = checks
    output['checks_passed'] = sum(c['passed'] for c in checks)
    output['checks_total'] = len(checks)
    (OUT / 'vacuum-search.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=output['checks_passed'], checks_total=len(checks))), flush=True)
    assert all(c['passed'] for c in checks), 'Failed checks preserved in vacuum-search.json'


if __name__ == '__main__':
    main()
