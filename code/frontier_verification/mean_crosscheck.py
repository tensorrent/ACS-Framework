"""Independent finite and asymptotic checks of the mean-error continuation.

Symbolic series and rational counting supplement, rather than replace, Lean.
Direct complex quadrature reuses the preceding checkpoint's quadrature routine.
All configurations are synthetic; there is no claim about an actual-zero dataset.
"""
from fractions import Fraction
import json
import mpmath as mp
import sympy as sp
from integral_crosscheck import direct


def number(x):
    return mp.mpf(x.numerator) / x.denominator if isinstance(x, Fraction) else mp.mpf(x)


def deficit(g, top, eps):
    return 2 * mp.pi - 2 * (mp.atan((top-g)/eps) + mp.atan(g/eps))


def main():
    mp.mp.dps = 70
    tolerance = mp.mpf('1e-55')
    z = sp.Symbol('z', positive=True)
    expression = sp.pi/2 + 2*sp.atan(z*z/(1-z*z)) + 4*(1/z-1)*sp.atan(2*z*z)
    total_limit = sp.limit(expression, z, 0, dir='+')
    mean_limit = sp.limit(z*expression, z, 0, dir='+')
    assert total_limit == sp.pi/2 and mean_limit == 0
    series = sp.series(expression, z, 0, 5)
    assert sp.expand(series.removeO()).coeff(z, 1) == 8
    assert sp.expand(series.removeO()).coeff(z, 2) == -6

    finite = []
    layers_checked = 0
    for top in [Fraction(1, 7), Fraction(1), Fraction(13)]:
        for relative_eps in [Fraction(1, 10000), Fraction(1, 100), Fraction(1), Fraction(100)]:
            eps = top * relative_eps
            for n in [1, 2, 7, 31]:
                # Distinct deterministic rational ordinates, including thin layers.
                points = [top * Fraction(1 + (k * 997) % 9998, 10000) for k in range(n)]
                total = mp.fsum(deficit(number(g), number(top), number(eps)) for g in points)
                mean = total / n
                layers = []
                for cutoff in [Fraction(1, 4), Fraction(1), Fraction(2), Fraction(10), Fraction(1000)]:
                    count = sum(min(g, top-g) <= cutoff*eps for g in points)
                    fraction = Fraction(count, n)
                    lower = 2*mp.atan(1/number(cutoff))*number(fraction)
                    sharp = 2*mp.pi*number(fraction) + 4*mp.atan(1/number(cutoff))
                    coarse = 2*mp.pi*number(fraction) + 4/number(cutoff)
                    assert lower <= mean+tolerance and mean <= sharp+tolerance and sharp <= coarse+tolerance
                    layers.append({'L':str(cutoff), 'count':count, 'fraction':str(fraction),
                                   'lower':str(lower), 'sharp_upper':str(sharp), 'coarse_upper':str(coarse)})
                    layers_checked += 1
                finite.append({'T':str(top), 'epsilon':str(eps), 'N':n, 'mean_error':str(mean), 'layers':layers})

    family = []
    quadrature = []
    for n in [2, 3, 10, 100, 1000, 10000, 1000000, 100000000]:
        eps = mp.mpf(1)/n**2
        explicit = deficit(eps, 1, eps) + (n-1)*deficit(mp.mpf('.5'), 1, eps)
        formula = mp.pi/2 + 2*mp.atan(mp.mpf(1)/(n*n-1)) + 4*(n-1)*mp.atan(mp.mpf(2)/n**2)
        assert abs(explicit-formula) < mp.mpf('1e-50')
        assert 0 < formula-mp.pi/2 <= 2/mp.mpf(n*n-1)+8/mp.mpf(n)
        family.append({'N':n, 'epsilon':str(eps), 'total_error':str(explicit),
                       'mean_error':str(explicit/n), 'distance_from_pi_over_two':str(formula-mp.pi/2)})
        if n in [2, 10, 100]:
            values = []
            for g in [eps, mp.mpf('.5')]:
                paired, separate = direct(g, mp.mpf(1), eps)
                expected = 2*mp.pi-deficit(g, 1, eps)
                error = max(abs(paired-expected), abs(separate-expected))
                assert error < mp.mpf('1e-50')
                quadrature.append({'N':n, 'gamma':str(g), 'epsilon':str(eps), 'maximum_error':str(error)})
                values.append(2*mp.pi-paired)
            assert abs(values[0]+(n-1)*values[1]-formula) < mp.mpf('1e-48')

    single = []
    for n in [3, 10, 100, 10000]:
        eps = Fraction(1, n*n)
        gamma = 2*eps
        assert min(gamma, 1-gamma) > eps
        observed = deficit(number(gamma), 1, number(eps))
        persistent_lower = 2*mp.atan(mp.mpf(1)/2)
        assert observed > persistent_lower > 0
        single.append({'N':n, 'epsilon':str(eps), 'gamma':str(gamma),
                       'fraction_at_L_1':'0', 'mean_error_singleton':str(observed),
                       'strict_positive_lower_bound':str(persistent_lower)})

    # Concrete witnesses to semantic mutations, independent of proof scripts.
    eps = mp.mpf('.01')
    boundary = deficit(eps, 1, eps)
    midpoint = deficit(mp.mpf('.5'), 1, eps)
    assert boundary < 4*mp.atan(1)  # doubling the lower coefficient is false
    assert midpoint > 0            # deleting the far-layer tail is false
    assert abs(mp.pi/2) > 1        # nonzero total limit is not a zero limit
    print(json.dumps({'status':'passed', 'precision_decimal_digits':mp.mp.dps,
                      'symbolic':{'variable':'z=1/N', 'total_limit':str(total_limit),
                                  'mean_limit':str(mean_limit), 'total_series':str(series)},
                      'finite_configurations':finite, 'layer_inequalities_checked':layers_checked,
                      'counterfamily':family, 'complex_quadrature_cases':quadrature,
                      'single_cutoff_counterexamples':single,
                      'scope':'Synthetic configurations, exact rational layer counts, symbolic limits, and finite numerical quadrature. No actual-zero data.'}, indent=2))


if __name__ == '__main__':
    main()
