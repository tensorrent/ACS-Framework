"""Recompute Q(zeta_5) finite witnesses with all factors and matched weights.

Controlled variants isolate conjugation, per-factor normalization and grid
sampling. None of these finite statistics is asserted to equal an infinite
explicit-formula distribution or a calibrated statistical significance test.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import mpmath as mp
import numpy as np
from flint import arb, ctx
from sympy import primerange
from dedekind_inputs import load_factors, at_height, NAMES

HEIGHTS = [60, 80, 100, 140, 180, 220]
WINDOWS = ['rectangular', 'triangular', 'hann']
VARIANTS = ['historical_doubled_means', 'separate_factor_means', 'union_mean']
PRIMES = list(map(int, primerange(2, 149)))


def window(t, top, name):
    if name == 'rectangular':
        return arb(1)
    if name == 'triangular':
        return 1 - t / top
    return (1 + (arb.pi() * t / top).cos()) / 2


def float_window(t, top, name):
    if name == 'rectangular':
        return np.ones(len(t))
    if name == 'triangular':
        return 1 - t / top
    return (1 + np.cos(np.pi * t / top)) / 2


def combine(sums, counts):
    z, a, b, c = sums
    nz, na, nb, nc = counts
    return [(z / nz + 2 * a / na + b / nb) / 4,
            (z / nz + a / na + b / nb + c / nc) / 4,
            (z + a + b + c) / sum(counts)]


def mean(values):
    return sum(values, arb(0)) / len(values)


def group_metrics(rows, variant, cohort, own_degree=False):
    eligible = []
    for row in rows:
        p = row['prime']
        f = 1 if p == 5 or p % 5 == 1 else 2 if p % 5 == 4 else 4
        if p in cohort and row['power'] == (f if own_degree else 1):
            eligible.append(row)
    groups = {}
    for key, predicate in [('split4', lambda p: p != 5 and p % 5 == 1),
                           ('split2', lambda p: p % 5 == 4),
                           ('inert', lambda p: p % 5 in [2, 3]),
                           ('ramified', lambda p: p == 5),
                           ('other_unramified', lambda p: p != 5 and p % 5 != 1)]:
        values = [abs(row['_balls'][variant]) for row in eligible if predicate(row['prime'])]
        groups[key] = {'count': len(values), 'mean_absolute': mean(values).str(40)}
    numerator = arb(groups['split4']['mean_absolute'])
    denominator = arb(groups['other_unramified']['mean_absolute'])
    assert denominator > 0
    return {'groups': groups, 'split4_to_other_ratio': (numerator / denominator).str(40)}


def independent_point(selected, top, name, p, k):
    mp.mp.dps = 85
    u = k * mp.log(p)
    total = mp.mpf(0)
    for rows in selected.values():
        for row in rows:
            t = mp.mpf(row['rounded'])
            weight = (mp.mpf(1) if name == 'rectangular' else 1 - t / top
                      if name == 'triangular' else (1 + mp.cos(mp.pi * t / top)) / 2)
            total += weight * mp.cos(u * t)
    return total / sum(map(len, selected.values()))


def audit(extra, prior):
    ctx.prec = 192
    factors, identity = load_factors(extra, prior)
    grid = np.linspace(0.5, 5.0, 2000)
    configurations, independent = [], []
    for top in HEIGHTS:
        selected = at_height(factors, top)
        counts = [len(selected[n]) for n in NAMES]
        intervals = [[arb(r['rounded'], '5e-21') for r in selected[n]] for n in NAMES]
        numeric = [np.array([float(r['rounded']) for r in selected[n]]) for n in NAMES]
        for name in WINDOWS:
            weights = [[window(t, top, name) for t in ts] for ts in intervals]
            float_weights = [float_window(ts, top, name) for ts in numeric]
            direct, sampled = [], []
            for p in PRIMES:
                for k in [1, 2, 4]:
                    u = k * arb(p).log()
                    sums = [sum((w * (u * t).cos() for w, t in zip(ws, ts)), arb(0))
                            for ws, ts in zip(weights, intervals)]
                    balls = combine(sums, counts)
                    floats = combine([float(np.sum(ws * np.cos(k * np.log(p) * ts)))
                                      for ws, ts in zip(float_weights, numeric)], counts)
                    assert all(abs(float(b.mid()) - a) < 2e-12 for a, b in zip(floats, balls))
                    row = {'prime': p, 'power': k, 'frequency': u.str(40),
                           'outside_historical_frequency_range': bool(u > 5),
                           'factor_sums': dict(zip(NAMES, [s.str(40) for s in sums])),
                           'variants': dict(zip(VARIANTS, [b.str(40) for b in balls])),
                           'float64_variants': dict(zip(VARIANTS, floats)), '_balls': balls}
                    direct.append(row)
                    if k == 1:
                        idx = int(np.argmin(np.abs(grid - np.log(p))))
                        sample_u = arb(float(grid[idx]))
                        sample_sums = [sum((w * (sample_u * t).cos() for w, t in zip(ws, ts)), arb(0))
                                       for ws, ts in zip(weights, intervals)]
                        sample_balls = combine(sample_sums, counts)
                        sampled.append({'prime': p, 'power': 1, 'grid_index': idx,
                                        'binary64_frequency_hex': float(grid[idx]).hex(),
                                        'frequency_error': (sample_u - u).str(40),
                                        'variants': dict(zip(VARIANTS, [b.str(40) for b in sample_balls])),
                                        'union_mean_change_from_exact': (sample_balls[2] - balls[2]).str(40),
                                        '_balls': sample_balls})
            for p, k in [(11, 1), (19, 2), (2, 4)]:
                expected = independent_point(selected, top, name, p, k)
                row = next(r for r in direct if r['prime'] == p and r['power'] == k)
                assert row['_balls'][2].contains(arb(mp.nstr(expected, 82)))
                independent.append({'height': top, 'window': name, 'prime': p, 'power': k,
                                    'mpmath_union_mean': mp.nstr(expected, 80),
                                    'inside_Arb_enclosure': True})
            metrics = {}
            for cohort_name, cohort in [('first_25_primes', PRIMES[:25]), ('all_primes_below_exp5', PRIMES)]:
                metrics[cohort_name] = {
                    'exact_logp': {v: group_metrics(direct, i, cohort) for i, v in enumerate(VARIANTS)},
                    'legacy_grid_logp': {v: group_metrics(sampled, i, cohort) for i, v in enumerate(VARIANTS)},
                    'own_residue_degree_logp': {v: group_metrics(direct, i, cohort, own_degree=True) for i, v in enumerate(VARIANTS)}}
            for row in direct + sampled:
                del row['_balls']
            configurations.append({'height': top, 'window': name, 'counts': dict(zip(NAMES, counts)),
                                   'union_count': sum(counts), 'direct_points': direct,
                                   'legacy_grid_points': sampled, 'metrics': metrics})
            print(json.dumps({'event': 'configuration', 'height': top, 'window': name,
                              'counts': counts, 'union_ratio_first25': metrics['first_25_primes']['exact_logp']['union_mean']['split4_to_other_ratio']}), flush=True)
    return {'status': 'passed', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'input_identity': identity, 'precision_bits': 192, 'mpmath_decimal_digits': 85,
            'heights': HEIGHTS, 'windows': WINDOWS, 'primes': PRIMES,
            'variants': {'historical_doubled_means': '(S_zeta/N_zeta + 2*S_chi1/N_chi1 + S_chi2/N_chi2)/4',
                         'separate_factor_means': 'sum(S_j/N_j)/4',
                         'union_mean': 'sum(S_j)/sum(N_j)'},
            'window_normalization': 'Every S uses the same window w(gamma/T); N remains the unweighted factor count. Ratios are unchanged by any single common scale.',
            'configurations': configurations, 'independent_checks': independent,
            'scope': 'Fresh declared finite computations. The historical missing quadratic table and NPZ are not recreated. No statistical significance or infinite-tail theorem is claimed.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extra', type=Path, required=True)
    parser.add_argument('--prior', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.extra, args.prior)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'configurations': len(result['configurations']),
                      'independent_checks': len(result['independent_checks'])}))
