"""Gaussian explicit formula for Q(zeta_5), with unconditional tail bounds.

The finite zero input is certified only through 220. Zeros outside that range
may be off the critical line; the tail bound uses 0 < Re(rho) < 1 and the
positive logarithmic-derivative moment at s=2, not GRH. See EXPLICIT_README.md.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time
from flint import acb, arb, ctx
from sympy import primerange
from dedekind_inputs import load_factors, at_height, NAMES

WIDTHS = ['1/25', '1/100', '1/400']
FREQUENCIES = [('zero', 1, None), ('log2', 2, None), ('log3', 3, None),
               ('log5', 5, None), ('log11', 11, None), ('log19', 19, None),
               ('log139', 139, None), ('log16', 16, None), ('log361', 361, None),
               ('off_peak_2.2', None, '11/5')]
HEIGHTS = [60, 100, 220]
PRIME_LIMITS = [1000, 10000, 100000]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def text(x):
    return x.str(55)


def widen(x, error):
    assert error >= 0
    return x + arb(0, error.upper())


def root_ball(row):
    return arb(row['lo']).union(arb(row['hi']))


def gaussian_pair(a, u):
    normal = 1 / (4 * (arb.pi() * a).sqrt())

    def h(t):
        return (-a * t * t).exp() * (u * t).cos()

    def g(x):
        # Multiplication is valid even when a real interval straddles zero.
        # python-flint 0.9.0 real exponentiation may return nan in that case.
        d, e = x - u, x + u
        return normal * ((-d * d / (4 * a)).exp() + (-e * e / (4 * a)).exp())

    return h, g


def prime_powers(limit):
    rows = []
    for prime in primerange(2, limit + 1):
        p = int(prime)
        f = 1 if p == 5 or p % 5 == 1 else 2 if p % 5 == 4 else 4
        n, k = p**f, f
        while n <= limit:
            rows.append({'n': n, 'prime': p, 'power': k, 'residue_degree': f,
                         'coefficient_divided_by_log_prime': 1 if p == 5 else 4})
            n *= p**f
            k += f
    return sorted(rows, key=lambda r: r['n'])


def moment_bounds(factors, primes):
    constant = arb(3) / 2 + arb(125).log() / 2 - 2 * (2 * arb.pi()).log() + 2 * arb(2).digamma()
    assert 0 < constant < 2
    partial_prime = sum((r['coefficient_divided_by_log_prime'] * arb(r['prime']).log() /
                         (r['n'] * r['n']) for r in primes), arb(0))
    X = PRIME_LIMITS[-1]
    # 0 <= Lambda_K(n) <= 4 log(n), followed by a decreasing integral test.
    prime_tail = 4 * (arb(X).log() + 1) / X
    moment = constant - partial_prime + arb(-prime_tail / 2, prime_tail.upper() / 2)
    upper = constant - partial_prime
    rows = {}
    for top in HEIGHTS:
        selected = at_height(factors, top)
        known = sum((3 / (arb('9/4') + root_ball(r) * root_ball(r))
                     for values in selected.values() for r in values), arb(0))
        assert known < moment
        residual_upper = upper - known
        assert residual_upper > 0 and residual_upper < constant
        rows[str(top)] = {'known_zero_moment': text(known),
                          'unknown_zero_moment_upper': text(residual_upper)}
    return {'constant_upper': text(constant), 'prime_partial_at_2': text(partial_prime),
            'prime_tail_at_2': text(prime_tail), 'full_moment_enclosure': text(moment),
            'cutoffs': rows}


def zero_tail(a, u, top, moment_upper):
    assert a * (4 + top * top) >= 1
    return moment_upper * (4 + top * top) * (-a * top * top + a / 4).exp() * (u / 2).cosh()


def prime_tail(a, u, X):
    b = u + a
    y = arb(X).log() - b
    assert arb(X).log() > 2 and y > 0
    # Integral test after v=log(x), completing the square, and erfc bound.
    return 8 * (a / arb.pi()).sqrt() * (u / 2 + a / 4 - y * y / (4 * a)).exp() * (1 + b / y)


def gamma_poitou(a, u, bits):
    _, g = gaussian_pair(a, u)
    g0 = g(arb(0))
    delta = arb('1e-20')
    end = 180

    def integrand(x, analytic):
        # This is a meromorphic extension, so poles yield non-finite balls.
        if x.abs_upper() < arb('0.01'):
            bx = x * u / (2 * a)
            sh = (bx / 2).sinh()
            numerator = -g0 * ((-x * x / (4 * a)).expm1() * bx.cosh() + 2 * sh * sh)
        else:
            numerator = g0 - g(x)
        return numerator / (2 * (x / 2).sinh())

    cuts = ['1e-20', '0.01', '0.1', '0.5', '1', '2', '3', '4', '5', '6', '8', '12', '20', '40', '80', '180']
    if bits > 160:
        cuts = sorted(set(cuts + ['0.03', '0.3', '1.5', '2.5', '3.5', '4.5', '5.5', '7', '10', '30', '60', '120']), key=F)
    tolerance = arb('1e-32') if bits == 160 else arb('1e-40')
    segments = []
    total = acb(0)
    for lo, hi in zip(cuts, cuts[1:]):
        value = acb.integral(integrand, acb(lo), acb(hi), abs_tol=tolerance, rel_tol=tolerance,
                             eval_limit=100000, depth_limit=50)
        assert value.is_finite() and value.imag.contains(0)
        segments.append({'lo': lo, 'hi': hi, 'integral_real': text(value.real), 'integral_imag': text(value.imag)})
        total += value
    # Global |g''| <= 3/(4*a*sqrt(pi*a)); g'(0)=0, 2*sinh(x/2)>=x.
    second_derivative_bound = 3 / (4 * a * (arb.pi() * a).sqrt())
    lower_tail = second_derivative_bound * delta * delta
    gmax = 1 / (2 * (arb.pi() * a).sqrt())
    upper_tail = 8 * (g0 + gmax) * arb(-end / 2).exp() / (1 - arb(-end).exp())
    constant = -4 * (arb.const_euler() + (8 * arb.pi()).log()) * g0
    value = constant + 4 * total.real
    return {'constant': text(constant), 'segments': segments, 'finite_value': text(value),
            'lower_tail_bound': text(lower_tail), 'upper_tail_bound': text(upper_tail),
            'enclosure': text(widen(value, lower_tail + upper_tail))}


def run(extra, prior, bits):
    ctx.prec = bits
    factors, identity = load_factors(extra, prior)
    powers = prime_powers(PRIME_LIMITS[-1])
    moments = moment_bounds(factors, powers)
    configurations = []
    start = time.monotonic()
    for width in WIDTHS:
        a = arb(width)
        for label, n, rational in FREQUENCIES:
            u = arb(rational) if rational else arb(n).log()
            h, g = gaussian_pair(a, u)
            gamma = gamma_poitou(a, u, bits)
            pole = 2 * (a / 4).exp() * (u / 2).cosh()
            conductor = arb(125).log() * g(arb(0))
            prime_rows = []
            for row in powers:
                term = 2 * row['coefficient_divided_by_log_prime'] * arb(row['prime']).log() / arb(row['n']).sqrt() * g(arb(row['n']).log())
                assert term.is_finite() and term >= 0
                prime_rows.append({**row, 'contribution': text(term)})
            sums = {}
            for X in PRIME_LIMITS:
                partial = sum((arb(r['contribution']) for r in prime_rows if r['n'] <= X), arb(0))
                tail = prime_tail(a, u, X)
                sums[str(X)] = {'partial': text(partial), 'tail_bound': text(tail),
                                'enclosure': text(widen(partial, tail))}
            full_prime = arb(sums[str(PRIME_LIMITS[-1])]['enclosure'])
            rhs = pole + conductor + arb(gamma['enclosure']) - full_prime
            zero_rows = {}
            for top in HEIGHTS:
                selected = at_height(factors, top)
                by_factor = {name: sum((2 * h(root_ball(r)) for r in values), arb(0))
                             for name, values in selected.items()}
                finite = sum(by_factor.values(), arb(0))
                tail = zero_tail(a, u, top, arb(moments['cutoffs'][str(top)]['unknown_zero_moment_upper']))
                enclosure = widen(finite, tail)
                residual = enclosure - rhs
                assert residual.contains(0)
                zero_rows[str(top)] = {'counts': {k: len(v) for k, v in selected.items()},
                                      'factor_sums': {k: text(v) for k, v in by_factor.items()},
                                      'finite_sum': text(finite), 'tail_bound': text(tail),
                                      'enclosure': text(enclosure), 'residual': text(residual)}
            for X in PRIME_LIMITS[:-1]:
                assert arb(sums[str(X)]['enclosure']).overlaps(full_prime)
            row = {'a': width, 'frequency_label': label, 'frequency': text(u), 'frequency_log_integer': n,
                   'frequency_rational': rational, 'pole': text(pole), 'conductor': text(conductor),
                   'gamma': gamma, 'prime_cutoffs': sums, 'prime_terms': prime_rows,
                   'zero_cutoffs': zero_rows, 'arithmetic_enclosure': text(rhs)}
            configurations.append(row)
            print(json.dumps({'a': width, 'frequency': label, 'residual_220': zero_rows['220']['residual'],
                              'zero_tail_220': zero_rows['220']['tail_bound']}), flush=True)
    return {'status': 'passed', 'source_sha256': sha(Path(__file__).read_bytes()), 'input_identity': identity,
            'precision_bits': bits, 'elapsed_seconds': time.monotonic() - start,
            'moment_bounds': moments, 'prime_power_terms': len(powers), 'configurations': configurations,
            'scope': 'Gaussian test functions, full Dedekind factorization, finite certificates through 220 and unconditional off-line zero/prime/gamma tail bounds. No global GRH, statistical or operator claim.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extra', type=Path, required=True)
    parser.add_argument('--prior', type=Path, required=True)
    parser.add_argument('--precision', type=int, choices=[160, 224], required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.extra, args.prior, args.precision)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'configurations': len(result['configurations']),
                      'prime_power_terms': result['prime_power_terms'], 'elapsed_seconds': result['elapsed_seconds']}), flush=True)
