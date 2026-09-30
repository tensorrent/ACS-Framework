"""Independent numeric routes and deliberate falsifications of the Gaussian audit."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time
import mpmath as mp
from flint import acb, arb, ctx
from dedekind_inputs import load_factors, at_height


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def number(value):
    value = F(value)
    return mp.mpf(value.numerator) / value.denominator


def independent_powers(limit):
    # Sieve and residue of the entire prime power, rather than the producer's
    # residue-degree stepping over prime ideals.
    smallest = list(range(limit + 1))
    for p in range(2, int(limit**0.5) + 1):
        if smallest[p] == p:
            for n in range(p * p, limit + 1, p):
                if smallest[n] == n:
                    smallest[n] = p
    rows = []
    for n in range(2, limit + 1):
        p, remainder, k = smallest[n], n, 0
        while remainder % p == 0:
            remainder //= p
            k += 1
        if remainder == 1 and (p == 5 or n % 5 == 1):
            rows.append((n, p, k, 1 if p == 5 else 4))
    return rows


def mp_gamma(a, u):
    normal = 1 / (4 * mp.sqrt(mp.pi * a))
    g0 = 2 * normal * mp.exp(-u * u / (4 * a))

    def g(x):
        return normal * (mp.exp(-(x - u)**2 / (4 * a)) + mp.exp(-(x + u)**2 / (4 * a)))

    def f(x):
        if x == 0:
            return mp.mpf(0)
        if abs(x) < mp.mpf('0.01'):
            bx = x * u / (2 * a)
            numerator = -g0 * (mp.expm1(-x * x / (4 * a)) * mp.cosh(bx) + 2 * mp.sinh(bx / 2)**2)
        else:
            numerator = g0 - g(x)
        return numerator / (2 * mp.sinh(x / 2))

    integral = mp.quad(f, [0, mp.mpf('0.01'), mp.mpf('0.1'), mp.mpf('0.5')] + list(range(1, 11)) + [20, 60, 180, mp.inf])
    return -4 * (mp.euler + mp.log(8 * mp.pi)) * g0 + 4 * integral


def digamma_route(a, u):
    # A different integral over zero-frequency t, rather than Poitou x.
    end = 60 if a > arb('0.02') else 120 if a > arb('0.005') else 240

    def f(t, analytic):
        z = acb(0, 1) * t
        psi_real_extension = ((acb('0.5') + z).digamma() + (acb('0.5') - z).digamma()) / 2
        return (-a * t * t).exp() * (u * t).cos() * psi_real_extension

    value = acb.integral(f, 0, end, abs_tol=arb('1e-30'), rel_tol=arb('1e-30'),
                         eval_limit=300000, depth_limit=50)
    assert value.is_finite() and value.imag.contains(0)
    digamma_integral = 4 / arb.pi() * value.real
    g0 = (-u * u / (4 * a)).exp() / (2 * (arb.pi() * a).sqrt())
    normalization = -4 * (2 * arb.pi()).log() * g0
    gamma = digamma_integral + normalization
    # |Re psi(1/2+it)| <= 4+2t, proved from the positive digamma series.
    tail = 4 / arb.pi() * (-a * end * end).exp() / a * (1 + arb(2) / end)
    return {'upper_limit': end, 'digamma_integral': digamma_integral.str(55),
            'gamma_normalization': normalization.str(55),
            'finite_value': gamma.str(55), 'tail_bound': tail.str(55),
            'enclosure': (gamma + arb(0, tail.upper())).str(55)}


def audit(audit_path, extra, prior):
    ctx.prec = 224
    mp.mp.dps = 60
    data = json.loads(audit_path.read_text())
    factors, identity = load_factors(extra, prior)
    powers = independent_powers(100000)
    assert len(powers) == data['prime_power_terms']
    finite_rows = at_height(factors, 220)
    results, alternate, mutations = [], [], []
    started = time.monotonic()
    for c in data['configurations']:
        a = number(c['a'])
        u = number(c['frequency_rational']) if c['frequency_rational'] else mp.log(c['frequency_log_integer'])
        expected_powers = [(r['n'], r['prime'], r['power'], r['coefficient_divided_by_log_prime']) for r in c['prime_terms']]
        assert expected_powers == powers
        normal = 1 / (4 * mp.sqrt(mp.pi * a))

        def g(x):
            return normal * (mp.exp(-(x - u)**2 / (4 * a)) + mp.exp(-(x + u)**2 / (4 * a)))

        zero = mp.fsum(2 * mp.exp(-a * t * t) * mp.cos(u * t)
                       for rows in finite_rows.values() for r in rows
                       for t in [(number(r['lo']) + number(r['hi'])) / 2])
        prime = mp.fsum(2 * coeff * mp.log(p) / mp.sqrt(n) * g(mp.log(n)) for n, p, k, coeff in powers)
        gamma = mp_gamma(a, u)
        rhs = 2 * mp.exp(a / 4) * mp.cosh(u / 2) + mp.log(125) * g(0) + gamma - prime
        for expected, actual in [(c['zero_cutoffs']['220']['finite_sum'], zero),
                                 (c['prime_cutoffs']['100000']['partial'], prime),
                                 (c['gamma']['enclosure'], gamma), (c['arithmetic_enclosure'], rhs)]:
            assert arb(expected).contains(arb(mp.nstr(actual, 60))), {
                'a': c['a'], 'frequency': c['frequency_label'], 'expected': expected,
                'mpmath': mp.nstr(actual, 60), 'difference': str(arb(expected) - arb(mp.nstr(actual, 60)))}
        results.append({'a': c['a'], 'frequency_label': c['frequency_label'],
                        'zero_sum': mp.nstr(zero, 60), 'prime_sum': mp.nstr(prime, 60),
                        'gamma': mp.nstr(gamma, 60), 'arithmetic': mp.nstr(rhs, 60),
                        'within_producer_enclosures': True})
        if c['frequency_label'] in ['zero', 'log11', 'log361']:
            alt = digamma_route(arb(c['a']), arb(c['frequency']))
            assert arb(alt['enclosure']).overlaps(arb(c['gamma']['enclosure']))
            alternate.append({'a': c['a'], 'frequency_label': c['frequency_label'], **alt})

        z = arb(c['zero_cutoffs']['220']['enclosure'])
        arithmetic = arb(c['arithmetic_enclosure'])
        factor = {k: arb(v) for k, v in c['zero_cutoffs']['220']['factor_sums'].items()}
        counts = c['zero_cutoffs']['220']['counts']
        ramified = sum((arb(r['contribution']) for r in c['prime_terms'] if r['prime'] == 5), arb(0))
        missing_f = sum((arb(r['contribution']) * (1 - arb(1) / r['residue_degree'])
                         for r in c['prime_terms']), arb(0))
        zero_tail = arb(c['zero_cutoffs']['220']['tail_bound'])
        largest_normalizer = arb(sum(counts.values())) / (4 * min(counts.values()))
        weighted_finite = sum(counts.values()) / arb(4) * sum((factor[k] / counts[k] for k in factor), arb(0))
        g0 = arb(c['conductor']) / arb(125).log()
        mutants = {
            'omit_negative_zeros': z / 2 - arithmetic,
            'double_one_positive_conjugate': z + factor['chi1'] - factor['chi3'] + arb(0, zero_tail.upper()) - arithmetic,
            'separate_factor_normalizers': weighted_finite + arb(0, (largest_normalizer * zero_tail).upper()) - arithmetic,
            'omit_pole': z - (arithmetic - arb(c['pole'])),
            'omit_gamma': z - (arithmetic - arb(c['gamma']['enclosure'])),
            'omit_discriminant': z - (arithmetic - arb(c['conductor'])),
            'omit_gamma_normalization': z - (arithmetic + 4 * (2 * arb.pi()).log() * g0),
            'omit_ramified_prime': z - (arithmetic + ramified),
            'omit_residue_degree_multiplier': z - (arithmetic + missing_f),
            'reverse_prime_sign': z - (arithmetic + 2 * arb(c['prime_cutoffs']['100000']['enclosure']))}
        mutations.append({'a': c['a'], 'frequency_label': c['frequency_label'],
                          'variants': {k: {'residual': v.str(55), 'rejected': not v.contains(0)} for k, v in mutants.items()}})
        print(json.dumps({'a': c['a'], 'frequency': c['frequency_label'], 'independent': 'passed'}), flush=True)
    counts = {name: sum(r['variants'][name]['rejected'] for r in mutations) for name in mutations[0]['variants']}
    assert all(count > 0 for count in counts.values())
    return {'status': 'passed', 'source_sha256': sha(Path(__file__).read_bytes()),
            'producer_result_sha256': sha(audit_path.read_bytes()), 'input_identity': identity,
            'mpmath_decimal_digits': 60, 'digamma_interval_precision_bits': 224,
            'independent_configurations': results, 'digamma_routes': alternate,
            'mutation_results': mutations, 'mutation_rejection_counts': counts,
            'elapsed_seconds': time.monotonic() - started,
            'scope': 'Independent numeric recomputation and alternate gamma integral; this does not independently certify root completeness or formalize the analytic explicit formula.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit', type=Path, required=True)
    parser.add_argument('--extra', type=Path, required=True)
    parser.add_argument('--prior', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.audit, args.extra, args.prior)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'independent_configurations': len(result['independent_configurations']),
                      'digamma_routes': len(result['digamma_routes']), 'mutation_rejection_counts': result['mutation_rejection_counts']}), flush=True)
