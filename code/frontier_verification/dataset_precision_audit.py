"""Audit source-table identity, certified counts, and finite scalar error.

Requires the retained Odlyzko primary tables via --primary. Arb enclosures carry
the publisher's stated ordinate uncertainty; they do not independently certify
all supplied zeros. Selected zeros and endpoint counts are recomputed with Arb.
"""
import argparse
from decimal import Decimal, localcontext
import gzip
import hashlib
import json
from pathlib import Path
import re
import time

from flint import acb, arb, ctx
import mpmath as mp
import numpy as np


EXPECTED = {
    'zeros1': '3436c916a7878261ac183fd7b9448c9a4736b8bbccf1356874a6ce1788541632',
    'zeros2': '0439d90a4c025d1ab3ed25f2241f27afeb6d01e651d95672267783b859ee170f',
    'zeros6.gz': '6acacb4707c429bf368f32823a8eef0e0737b6318d3e144c78975a4986d155da',
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def interval(x):
    return x.str(40)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--primary', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    started = time.time()
    source_sha256 = digest(Path(__file__).read_bytes())
    ctx.prec = 160
    mp.mp.dps = 60
    root = Path(__file__).resolve().parents[2]
    data_path = root / 'code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt'
    for name, expected in EXPECTED.items():
        assert digest((args.primary / name).read_bytes()) == expected, name
    original = (args.primary / 'zeros1').read_bytes()
    repo_data = data_path.read_bytes()
    assert repo_data + b'\n' == original
    text = original.decode().split()
    extended_raw = gzip.decompress((args.primary / 'zeros6.gz').read_bytes())
    extended = extended_raw.decode().split()
    assert len(text) == 100000 and len(extended) == 2001052
    assert text == extended[:len(text)]
    values = np.array(extended, dtype=float)
    assert np.isfinite(values).all() and (np.diff(values) > 0).all()
    high = [''.join(block.split()) for block in
            re.split(r'\n\s*\n', (args.primary / 'zeros2').read_text().strip())]
    assert len(high) == 100 and all(re.fullmatch(r'\d+\.\d+', h) for h in high)
    with localcontext() as context:
        context.prec = 1100
        errors = [abs(Decimal(text[i]) - Decimal(high[i])) for i in range(100)]
        assert max(errors) < Decimal('3e-9')
    source = {
        'repository_path': data_path.relative_to(root).as_posix(),
        'repository_sha256': digest(repo_data),
        'publisher_table_sha256': digest(original),
        'identity': 'All bytes match after appending one final newline to the repository file.',
        'rows': len(text), 'larger_table_rows': len(extended),
        'larger_table_sha256': digest(extended_raw), 'larger_table_prefix_identical': True,
        'publisher_absolute_uncertainty': '3e-9 (zeros1); 4e-9 (zeros6)',
        'first_100_max_difference_from_high_precision_table': str(max(errors)),
        'minimum_gap_in_larger_table_float64': float(np.min(np.diff(values))),
    }
    (args.output / 'Source_Identity.json').write_text(json.dumps(source, indent=2) + '\n')

    selected = []
    for n in [1, 3, 10, 50, 100]:
        computed = acb.zeta_zero(n).imag
        provided = arb(high[n-1], '1e-1000')
        assert computed.overlaps(provided)
        independent = mp.im(mp.zetazero(n))
        assert abs(independent - mp.mpf(high[n-1])) < mp.mpf('1e-45')
        selected.append({'index': n, 'arb_ordinate': interval(computed),
                         'mpmath_ordinate': str(independent), 'matches_primary_high_precision': True})

    configurations = []
    for n in [50, 1000, 10000, 100000]:
        with localcontext() as context:
            context.prec = 40
            endpoint = str((Decimal(extended[n-1]) + Decimal(extended[n])) / 2)
        top = arb(endpoint)
        g = [arb(t, '3e-9') for t in text[:n]]
        assert g[0] > 0 and top - g[-1] > 0
        assert arb(extended[n], '4e-9') - top > 0
        count = top.zeta_nzeros()
        assert count == n
        midpoint_values = np.array(text[:n], dtype=float)
        for eps_text in ['1e-2', '1e-4', '1e-6']:
            eps = arb(eps_text)
            total, ratio = arb(0), arb(0)
            for gamma in g:
                left, right = eps / gamma, eps / (top - gamma)
                total += 2 * (left.atan() + right.atan())
                ratio += left + right
            numerical = 2 * np.sum(np.arctan(float(eps_text) / midpoint_values)
                                   + np.arctan(float(eps_text) / (float(endpoint) - midpoint_values)))
            # Float64 is an independent midpoint computation; its final rounding
            # is enclosed explicitly rather than treated as exact arithmetic.
            assert total.overlaps(arb(float(numerical), abs(float(numerical)) * 1e-11))
            configurations.append({'N': n, 'T_exact_decimal': endpoint, 'epsilon': eps_text,
                                   'certified_zeta_count': str(n),
                                   'total_deficit_enclosure': interval(total),
                                   'mean_deficit_enclosure': interval(total / n),
                                   'endpoint_ratio_sum_enclosure': interval(ratio),
                                   'float64_midpoint_total': float(numerical),
                                   'right_endpoint_distance_enclosure': interval(top - g[-1]),
                                   'input_uncertainty': '3e-9 per supplied ordinate'})
        (args.output / 'Finite_Configurations.json').write_text(json.dumps(configurations, indent=2) + '\n')

    endpoint_cases = []
    for n in [1, 3, 50]:
        true_gamma = acb.zeta_zero(n).imag
        supplied = arb(text[n-1])
        for eps_text in ['1e-6', '1e-8', '1e-10', '1e-12']:
            eps = arb(eps_text)
            # T is the exact table decimal plus the declared exact resolution.
            top = supplied + eps
            uncertain_gamma = arb(text[n-1], '3e-9')
            count = top.zeta_nzeros()
            count_int = count.unique_fmpz()
            assert count_int is not None
            actual = 2 * ((top-true_gamma)/eps).atan() + 2 * (true_gamma/eps).atan()
            rounded = 2 * ((top-supplied)/eps).atan() + 2 * (supplied/eps).atan()
            layer_interval = 2 * ((top-uncertain_gamma)/eps).atan() + 2 * (uncertain_gamma/eps).atan()
            assert layer_interval.contains(actual)
            endpoint_cases.append({'index': n, 'epsilon': eps_text,
                                   'T_construction': text[n-1] + ' + ' + eps_text,
                                   'rounded_table_count': n, 'certified_zeta_count': int(count_int),
                                   'interiority_certified_from_coarse_table': bool(top-uncertain_gamma > 0),
                                   'actual_last_point_is_interior': bool(top-true_gamma > 0),
                                   'coarse_input_contribution_enclosure': interval(layer_interval),
                                   'rounded_point_contribution': interval(rounded),
                                   'recomputed_point_contribution': interval(actual)})
    failure = next(c for c in endpoint_cases if c['index'] == 3 and c['epsilon'] == '1e-10')
    assert failure['rounded_table_count'] == 3 and failure['certified_zeta_count'] == 2
    assert not failure['actual_last_point_is_interior']
    result = {'status': 'passed', 'source_sha256': source_sha256, 'arb_precision_bits': ctx.prec,
              'mpmath_precision_decimal_digits': mp.mp.dps, 'elapsed_seconds': time.time()-started,
              'selected_zeros': selected, 'finite_configurations': configurations,
              'endpoint_precision_cases': endpoint_cases,
              'scope': 'Conditional interval propagation for supplied data; selected zeros and endpoint counts independently recomputed. No all-zero precision recertification or infinite-limit claim.'}
    (args.output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'configurations': len(configurations),
                      'endpoint_cases': len(endpoint_cases), 'selected_zeros': len(selected),
                      'elapsed_seconds': result['elapsed_seconds'], 'count_mismatch_witness': failure}, indent=2))


if __name__ == '__main__':
    main()
