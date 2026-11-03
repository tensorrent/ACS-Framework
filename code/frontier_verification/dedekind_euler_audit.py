"""Exact Euler-factor and normalization checks for Q(zeta_5).

Compare character products, permutation determinants, modular factorization,
and logarithmic-derivative coefficients, including the ramified prime.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sympy as sp
from dedekind_inputs import load_factors, at_height, NAMES


def audit(extra, prior):
    factors, identity = load_factors(extra, prior)
    X = sp.Symbol('X')
    units = [1, 2, 3, 4]
    logs = {1: 0, 2: 1, 3: 3, 4: 2}
    rows = []
    for residue in units:
        f = next(k for k in [1, 2, 4] if pow(residue, k, 5) == 1)
        g = 4 // f
        chars = [sp.I ** (j * logs[residue]) for j in range(4)]
        poly = sp.expand(sp.prod(1 - c * X for c in chars))
        expected = sp.expand((1 - X**f)**g)
        M = sp.zeros(4)
        for j, u in enumerate(units):
            M[units.index((residue * u) % 5), j] = 1
        assert sp.expand((sp.eye(4) - X * M).det()) == poly == expected
        log_derivative = sp.cancel(-X * sp.diff(poly, X) / poly)
        assert sp.cancel(log_derivative - g * f * X**f / (1 - X**f)) == 0
        series = sp.series(log_derivative, X, 0, 17).removeO().expand()
        coefficients = []
        for k in range(1, 17):
            by_char = sp.expand(sum(c**k for c in chars))
            by_trace = sp.trace(M**k)
            by_series = series.coeff(X, k)
            exact = 4 if k % f == 0 else 0
            assert by_char == by_trace == by_series == exact
            coefficients.append(int(exact))
        rows.append({'residue': residue, 'residue_degree_f': f, 'prime_ideal_count_g': g,
                     'character_values': list(map(str, chars)), 'permutation_matrix': [list(map(int, M.row(i))) for i in range(4)],
                     'Euler_denominator': str(poly), 'X_log_derivative': str(log_derivative),
                     'first_16_coefficients_divided_by_log_p': coefficients,
                     'leading_coefficient_is_g_times_f': g * f})

    modular = []
    phi = X**4 + X**3 + X**2 + X + 1
    for p in list(sp.primerange(2, 1000)):
        _, decomposition = sp.Poly(phi, X, modulus=p).factor_list()
        degrees = sorted((int(poly.degree()), int(exponent)) for poly, exponent in decomposition)
        if p == 5:
            assert degrees == [(1, 4)]
            expected = [(1, 4)]
        else:
            f = next(k for k in [1, 2, 4] if pow(p, k, 5) == 1)
            expected = [(f, 1)] * (4 // f)
            assert degrees == expected
        modular.append({'prime': int(p), 'factor_degrees_and_multiplicities': degrees})
    # At p=5 only the primitive zeta factor has a nontrivial Euler factor.
    ramified = {'prime': 5, 'Euler_denominator': '1 - X',
                'ramification_index': 4, 'residue_degree': 1, 'prime_ideal_count': 1,
                'first_16_coefficients_divided_by_log_5': [1] * 16}

    normalization = []
    for top in [60, 80, 100, 140, 180, 220]:
        selected = at_height(factors, top)
        counts = [len(selected[n]) for n in NAMES]
        equal_weights = len(set(counts)) == 1
        assert not equal_weights
        defects = {}
        for residue in units:
            chars = [sp.I ** (j * logs[residue]) for j in range(4)]
            coefficient = sp.simplify(sum(chars[j] / sp.Integer(counts[j]) for j in range(4)))
            defects[str(residue)] = str(coefficient)
            if residue != 1:
                # A nonzero coefficient where the genuine unramified factor cancels.
                assert coefficient != 0
        normalization.append({'height': top, 'counts': dict(zip(NAMES, counts)),
                              'per_factor_mean_weights': {n: str(F(1, counts[j])) for j, n in enumerate(NAMES)},
                              'common_union_weight': str(F(1, sum(counts))),
                              'weighted_first_prime_coefficients': defects,
                              'all_three_non_split_cancellations_broken': True})
    return {'status': 'passed', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'input_identity': identity, 'unramified_residue_classes': rows, 'ramified': ramified,
            'modular_polynomial_factorizations': modular, 'normalization_counterexamples': normalization,
            'scope': 'Exact local Euler coefficients and finite spectral weights. This does not identify a finite unsmoothed Fourier value with an Euler coefficient.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extra', type=Path, required=True)
    parser.add_argument('--prior', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.extra, args.prior)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'modular_factorizations': len(result['modular_polynomial_factorizations']),
                      'normalization_counterexamples': result['normalization_counterexamples']}, indent=2))
