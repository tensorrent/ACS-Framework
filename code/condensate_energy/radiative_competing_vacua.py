#!/usr/bin/env python3
"""Verify a competing vacuum independently of numerical minimization."""
import json
import math
import mpmath as mp
import numpy as np
from scipy.optimize import minimize_scalar

from canonical_scalar_action import load_exact_basis, scalar_unpack
from hidden_coupling_audit import gauge_matrices, mass
from radiative_flat_modes import OUT, gauge_gram, analytic_curvature, cw_sum
from radiative_vacuum_search import factored_field, effective_potential


def closed_difference(singular, g4=.3, gR=.35, d=1., mu=1.):
    # Independent explicit spectra: rank-four real-spin point versus neutral.
    a, b, total = g4 ** 2 * d ** 2, gR ** 2 * d ** 2, (3 * g4 ** 2 + 2 * gR ** 2) * d ** 2

    def h(x):
        return x ** 2 * (math.log(x / mu ** 2) - 5 / 6)

    gauge = 3 * (3 * h(a) + 2 * h(2 * b) - 2 * h(b) - h(total)) / (64 * np.pi ** 2)
    fermion = sum(f ** 4 * d ** 4 * (7 * math.log(f ** 2 * d ** 2 / mu ** 2) + 10 * math.log(2) - 21 / 2)
                  for f in singular if f) / (64 * np.pi ** 2)
    return dict(gauge=gauge, fermion=fermion, total=gauge + fermion)


def path(u):
    alpha = math.pi * u / 3
    return [math.cos(alpha) ** 2] + [math.sin(alpha) ** 2 / 3] * 3, math.pi * u / 4


def main():
    checks, output = [], {}

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL', flush=True)

    metric = load_exact_basis()[2]
    matrices, groups, weights = gauge_matrices()
    x = factored_field([.25] * 4, np.pi / 4)
    gv = np.linalg.eigvalsh(gauge_gram(x, [.3, .25, .35], metric, matrices, groups, weights))
    expected = np.sort([0.] * 10 + [.3 ** 2] * 9 + [2 * .35 ** 2] * 2)
    check('rank-four-real-spin-explicit-vector-spectrum', max(abs(gv - expected)) < 1e-12)
    check('rank-four-real-spin-ten-massless-vectors', sum(abs(gv) < 1e-12) == 10)
    rows = []
    for singular in [[], [.3], [.5], [.3, .3, .3]]:
        closed = closed_difference(singular)
        direct = effective_potential([.25] * 4, np.pi / 4, singular) - effective_potential([1, 0, 0, 0], 0., singular)
        check('closed-endpoint-energy-' + str(singular), abs(direct - closed['total']) < 1e-15)
        families = max(1, len(singular))
        zeros = np.zeros((families, families), complex)
        F = np.diag(singular if singular else [0.]).astype(complex)
        phi, delta = scalar_unpack(x)
        M = mass(phi, delta, zeros, zeros, F)
        fv = np.linalg.eigvalsh(M.conj().T @ M)
        expected_f = np.sort([0.] * (8 * families) + [f ** 2 / 4 for f in (singular if singular else [0.]) for _ in range(8)])
        check('rank-four-explicit-Weyl-spectrum-' + str(singular), max(abs(fv - expected_f)) < 1e-12)
        endpoint = (3 * cw_sum(gv, 5 / 6, 1.) - 2 * cw_sum(fv, 1.5, 1.)) / (64 * np.pi ** 2)
        base = effective_potential([1, 0, 0, 0], 0., singular)
        check('full-component-endpoint-energy-' + str(singular), abs(endpoint - base - closed['total']) < 1e-15)
        grid = np.linspace(0, 1, 601)
        energy = [effective_potential(*path(u), singular) - base for u in grid]
        imax = int(np.argmax(energy))
        candidates = [(float(grid[imax]), energy[imax])]
        if 0 < imax < len(grid) - 1:
            peak = minimize_scalar(lambda u: -(effective_potential(*path(u), singular) - base),
                bounds=(grid[imax - 1], grid[imax + 1]), method='bounded', options=dict(xatol=1e-12))
            check('path-maximum-optimization-' + str(singular), peak.success)
            candidates.append((float(peak.x), float(-peak.fun)))
        peak_u, peak_energy = max(candidates, key=lambda item: item[1])
        spin = analytic_curvature('spin', .3, .35, singular)['total']
        color = analytic_curvature('color', .3, .35, singular)['total']
        if singular == [.3, .3, .3]:
            check('explicit-local-positive-but-lower-competing-configuration', spin > 0 and color > 0 and closed['total'] < -1e-4,
                  dict(spin=spin, color=color, competing_energy=closed['total']))
            check('explicit-path-positive-barrier-before-lower-endpoint', peak_energy > 1e-7 and 0 < peak_u < 1)
        rows.append(dict(Majorana_singular=singular, closed_energy_difference=closed,
            local_spin_curvature=spin, local_color_curvature=color, path_grid=grid.tolist(), energy_grid=energy,
            path_peak_u=peak_u, path_peak_energy=peak_energy))
    # The counterexample's sign survives high-precision evaluation of its closed expression.
    mp.mp.dps = 70
    a, b, f = mp.mpf('.3') ** 2, mp.mpf('.35') ** 2, mp.mpf('.3')
    h = lambda v: v ** 2 * (mp.log(v) - mp.mpf(5) / 6)
    high = (3 * (3 * h(a) + 2 * h(2 * b) - 2 * h(b) - h(3 * a + 2 * b))
            + 3 * f ** 4 * (7 * mp.log(f ** 2) + 10 * mp.log(2) - mp.mpf(21) / 2)) / (64 * mp.pi ** 2)
    check('70-digit-counterexample-energy', high < 0 and abs(float(high) - rows[-1]['closed_energy_difference']['total']) < 1e-15, str(high))
    output['examples'] = rows
    output['closed_difference_formula'] = ('With a=g4^2 d^2,b=gR^2 d^2,T=3a+2b,h(x)=x^2[log(x/mu^2)-5/6]: '
        'DeltaVg=3[3h(a)+2h(2b)-2h(b)-h(T)]/(64pi^2); '
        'DeltaVf=sum_i f_i^4 d^4[7log(f_i^2 d^2/mu^2)+10log2-21/2]/(64pi^2). '
        'The scalar spectrum and tree potential are equal at these two points for the spin-Gram model.')
    output['scope'] = ('Explicit counterexample to global neutral minimality in the specified leading-one-loop boundary model, '
        'independent of any claim that the rank-four endpoint is the absolute minimum. '
        'The connecting path is not a least-action tunneling path; no decay rate or lifetime is calculated. '
        'For the color-Gram model the rank-four endpoint is not tree-degenerate and this comparison does not apply.')
    output['checks'] = checks
    output['checks_passed'] = sum(c['passed'] for c in checks)
    output['checks_total'] = len(checks)
    (OUT / 'competing-vacua.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=output['checks_passed'], checks_total=len(checks))))
    assert all(c['passed'] for c in checks), 'Failed checks preserved in competing-vacua.json'


if __name__ == '__main__':
    main()
