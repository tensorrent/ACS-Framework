"""Finite-resolution and moving-boundary checks for the declared PerZero formula.

Exact symbolic integrand algebra and derivative checks are separate from numerical
quadrature. Numerical samples support the analytical inequalities in the report;
they are not a general theorem proof and do not establish RH.
"""
import json
import mpmath as mp
import sympy as sp


def contribution(gamma, top, eps):
    return 2 * (mp.atan((top - gamma) / eps) + mp.atan(gamma / eps))


def direct_quadrature(gamma, top, eps):
    # Resolve the narrow Lorentzian by u=(t-gamma)/eps. No arctangent call.
    lo, hi = -gamma / eps, (top - gamma) / eps
    breaks = sorted({lo, hi, *[mp.mpf(v) for v in [-1000, -100, -10, -1, 0, 1, 10, 100, 1000]
                              if lo < v < hi]})
    return mp.quad(lambda u: 2 / (1 + u * u), breaks)


def main():
    mp.mp.dps = 70
    u, e = sp.symbols('u e', real=True, positive=True)
    paired = 1 / (e + sp.I * u) - 1 / (-e + sp.I * u)
    assert sp.simplify(paired - 2 * e / (e ** 2 + u ** 2)) == 0
    assert sp.simplify(sp.diff(2 * sp.atan(u / e), u) - 2 * e / (e ** 2 + u ** 2)) == 0
    x = sp.symbols('x', positive=True)
    assert sp.simplify(sp.diff(x - sp.atan(x), x) - x ** 2 / (1 + x ** 2)) == 0

    rows = []
    for top, gamma in [('1', '.5'), ('1', '.01'), ('3', '2.99'), ('10', '2')]:
        top, gamma = mp.mpf(top), mp.mpf(gamma)
        for eps in map(mp.mpf, ['.7', '.1', '.001', '.000001']):
            value = contribution(gamma, top, eps)
            integral = direct_quadrature(gamma, top, eps)
            assert abs(value - integral) < mp.mpf('1e-55')
            deficit = 2 * mp.pi - value
            exact_deficit = 2 * (mp.atan(eps / gamma) + mp.atan(eps / (top - gamma)))
            assert abs(deficit - exact_deficit) < mp.mpf('1e-60')
            lower = 2 * eps * (gamma / (gamma ** 2 + eps ** 2)
                              + (top - gamma) / ((top - gamma) ** 2 + eps ** 2))
            first_order = 2 * eps * (1 / gamma + 1 / (top - gamma))
            cubic_bound = 2 * eps ** 3 / 3 * (1 / gamma ** 3 + 1 / (top - gamma) ** 3)
            assert 0 < lower <= deficit <= first_order
            assert 0 <= first_order - deficit <= cubic_bound
            rows.append({'T': str(top), 'gamma': str(gamma), 'epsilon': str(eps),
                         'quadrature_error': str(abs(value - integral)),
                         'deficit': str(deficit), 'lower': str(lower),
                         'linear_upper': str(first_order), 'cubic_remainder_bound': str(cubic_bound)})

    boundary = []
    for c in map(mp.mpf, ['0', '.1', '1', '10']):
        limit = mp.pi + 2 * mp.atan(c)
        values = []
        for eps in map(mp.mpf, ['.001', '.00001', '.0000001']):
            gamma = c * eps
            value = contribution(gamma, mp.mpf(1), eps)
            assert abs(value - limit) <= 2 * eps / (1 - gamma)
            values.append({'epsilon': str(eps), 'contribution': str(value), 'limit_error': str(abs(value - limit))})
        boundary.append({'c': str(c), 'limit': str(limit), 'samples': values})

    aggregate = []
    for n in [10, 100, 1000]:
        eps = mp.mpf(1) / n ** 2
        gamma = [eps] + [mp.mpf('.5')] * (n - 1)
        deficits = [2 * mp.pi - contribution(g, mp.mpf(1), eps) for g in gamma]
        total = mp.fsum(deficits)
        # One boundary point leaves an absolute pi/2 defect as the mean vanishes.
        assert total > mp.pi / 2 and total / n < 10 / mp.mpf(n)
        fraction = mp.mpf(1) / n
        cutoff = mp.mpf(2)
        assert 2 * mp.atan(1 / cutoff) * fraction <= total / n
        assert total / n <= 2 * mp.pi * fraction + 4 * mp.atan(1 / cutoff)
        aggregate.append({'N': n, 'epsilon': str(eps), 'total_deficit': str(total),
                          'mean_deficit': str(total / n), 'boundary_fraction_at_2epsilon': str(fraction)})

    # These proposed strengthenings are false on explicit examples.
    finite_error = 2 * mp.pi - contribution(mp.mpf('.5'), mp.mpf(1), mp.mpf('.1'))
    assert finite_error > 0
    assert abs(contribution(mp.mpf('1e-8'), mp.mpf(1), mp.mpf('1e-8')) - 2 * mp.pi) > 1
    print(json.dumps({'status': 'passed', 'precision_decimal_digits': mp.mp.dps,
                      'symbolic_checks': ['paired_integrand', 'antiderivative', 'cubic_remainder_identity'],
                      'interior_samples': rows, 'moving_boundary': boundary,
                      'mean_vs_total_counterfamily': aggregate,
                      'rejected_strengthenings': ['finite_epsilon_equality', 'uniform_over_all_interior_ordinates',
                                                 'mean_error_convergence_implies_total_error_convergence'],
                      'scope': 'Declared scalar kernel. No assertion that arbitrary ordinates are zeta zeros; no RH identification.'}, indent=2))


if __name__ == '__main__':
    main()
