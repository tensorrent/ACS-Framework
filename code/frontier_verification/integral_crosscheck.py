"""Direct complex quadrature and configuration checks for the integral delta.

This uses the two actual complex resolvents, separately and as a paired integrand.
It supplements the universal Lean statements with independent numerical samples;
it is not a general numerical certificate or an assertion about actual zeta data.
"""
import json
import mpmath as mp
import sympy as sp


def closed(gamma, top, eps):
    return 2 * (mp.atan((top - gamma) / eps) + mp.atan(gamma / eps))


def direct(gamma, top, eps):
    low, high = min(0, top), max(0, top)
    points = {mp.mpf(low), mp.mpf(high)}
    for offset in [-1000, -100, -10, -1, 0, 1, 10, 100, 1000]:
        point = gamma + offset * abs(eps)
        if low < point < high:
            points.add(point)
    points = sorted(points)
    if top < 0:
        points.reverse()
    plus = lambda t: 1 / (eps + 1j * (t - gamma))
    minus = lambda t: 1 / (-eps + 1j * (t - gamma))
    paired = mp.quad(lambda t: plus(t) - minus(t), points)
    separate = mp.quad(plus, points) - mp.quad(minus, points)
    return paired, separate


def main():
    mp.mp.dps = 70
    e, u = sp.symbols('e u', real=True)
    plus = 1 / (e + sp.I * u)
    minus = 1 / (-e + sp.I * u)
    assert sp.cancel(plus - minus - 2 * e / (e**2 + u**2)) == 0
    # The sign-flipped mutation has a nonzero imaginary value already at e=u=1.
    assert sp.simplify((plus + minus - 2 * e / (e**2 + u**2)).subs({e: 1, u: 1})) != 0
    cases = []
    for top, gamma in [('1', '.5'), ('1', '0'), ('1', '1'), ('1', '-.2'),
                       ('1', '1.2'), ('-2', '-.7')]:
        top, gamma = mp.mpf(top), mp.mpf(gamma)
        for eps in map(mp.mpf, ['.1', '.000001', '-.1', '-.000001']):
            paired, separate = direct(gamma, top, eps)
            value = closed(gamma, top, eps)
            assert abs(paired - value) < mp.mpf('1e-50')
            assert abs(separate - value) < mp.mpf('1e-50')
            cases.append({'T': str(top), 'gamma': str(gamma), 'epsilon': str(eps),
                          'paired_integral': str(paired), 'separate_integrals_difference': str(separate),
                          'closed_form': str(value), 'maximum_error': str(max(abs(paired-value), abs(separate-value)))})

    configurations = []
    for n in [10, 100, 1000]:
        eps = mp.mpf(1) / n**2
        for name, gamma in [
            ('fixed_interior', [mp.mpf('.5')] * n),
            ('one_resolution_scale_point', [eps] + [mp.mpf('.5')] * (n-1)),
            ('one_subresolution_point', [eps**2] + [mp.mpf('.5')] * (n-1))
        ]:
            ratios = [ratio for g in gamma for ratio in [eps/g, eps/(1-g)]]
            total = mp.fsum(2*mp.pi-closed(g, mp.mpf(1), eps) for g in gamma)
            ratio_sum = mp.fsum(ratios)
            lower = 2 * mp.fsum(x/(1+x*x) for x in ratios)
            assert lower <= total <= 2*ratio_sum
            if total < mp.pi/2:
                assert ratio_sum <= total
            layers = []
            for cutoff in map(mp.mpf, ['.5', '1', '2', '10']):
                fraction = mp.mpf(sum(min(g, 1-g) <= cutoff*eps for g in gamma)) / n
                assert 2*mp.atan(1/cutoff)*fraction <= total/n
                assert total/n <= 2*mp.pi*fraction + 4*mp.atan(1/cutoff)
                layers.append({'L': str(cutoff), 'fraction': str(fraction)})
            configurations.append({'family': name, 'N': n, 'epsilon': str(eps),
                                   'total_error': str(total), 'mean_error': str(total/n),
                                   'ratio_sum': str(ratio_sum), 'boundary_layers': layers})

    x = mp.mpf('.001')
    assert mp.atan(x) > x/2
    assert x-mp.atan(x) > x**3/4
    x = mp.mpf(100)
    assert 2*mp.atan(x) < 4*mp.pi and x > 2*mp.atan(x)
    print(json.dumps({'status': 'passed', 'precision_decimal_digits': mp.mp.dps,
                      'complex_integral_cases': cases, 'configurations': configurations,
                      'explicit_false_mutations': ['resolvent addition', 'arctan half upper bound',
                                                   'cubic coefficient one quarter', 'small-error threshold four pi'],
                      'scope': 'Finite numerical examples complement kernel proofs; no actual-zero dataset is used.'}, indent=2))


if __name__ == '__main__':
    main()
