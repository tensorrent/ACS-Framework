"""Compare archived ordinates with complete interval lists and a second library."""
import argparse
from collections import Counter
from decimal import Decimal
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import zipfile

import mpmath as mp
from flint import acb, arb, ctx, dirichlet_char
from sympy import kronecker_symbol

from lfunction_zero_certificate import SPECS

TABLES = {
    'cyclotomic_5/zeros_chi_5_order4.txt': ('chi5', 100),
    'cyclotomic_5/zeros_chi_5_order4_ext.txt': ('chi5', 220),
    'cyclotomic_7/zeros_chi_7_order6.txt': ('chi7', 100),
    'cyclotomic_7/zeros_chi_7_order6_ext.txt': ('chi7', 220),
    'cyclotomic_and_h6/zeros_chi_-104.txt': ('chi_m104', 70),
    'cyclotomic_and_h6/zeros_chi_5_order4.txt': ('chi5', 100),
    'disentangled/zeros_chi_-35.txt': ('chi_m35', 80),
    'disentangled/zeros_chi_-91.txt': ('chi_m91', 60),
}
PREFIX = 'code/hp_knife_suite/data_zeros/'


def mpf(x):
    x = F(x)
    return mp.mpf(x.numerator) / x.denominator


def distance(x, lo, hi):
    return max(F(0), lo - x, x - hi), max(abs(lo - x), abs(hi - x))


def independent_L(name, t):
    q, _, _, d = SPECS[name]
    s = mp.mpc('0.5', t)
    if d:
        chars = [int(kronecker_symbol(d, a)) for a in range(q)]
    else:
        gen = 2 if q == 5 else 3
        direction = -1 if name.endswith('bar') else 1
        chars = [mp.mpc(0)] * q
        for k in range(q - 1):
            chars[pow(gen, k, q)] = mp.exp(2j * mp.pi * direction * k / (q - 1))
    return mp.power(q, -s) * mp.fsum(chars[a] * mp.zeta(s, mp.mpf(a) / q)
                                   for a in range(1, q) if chars[a])


def audit(certificates, baseline):
    ctx.prec = 192
    mp.mp.dps = 65
    certs = {name: json.loads((certificates / (name + '.json')).read_text()) for name in SPECS}
    result = {'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'baseline_archive_sha256': hashlib.sha256(baseline.read_bytes()).hexdigest(),
              'certificate_hashes': {name: hashlib.sha256((certificates / (name + '.json')).read_bytes()).hexdigest() for name in SPECS},
              'precision_bits': ctx.prec, 'mpmath_decimal_digits': mp.mp.dps,
              'tables': [], 'independent_root_checks': [], 'conjugation_checks': []}
    with zipfile.ZipFile(baseline) as old:
        for path, (name, top) in TABLES.items():
            raw = old.read('baseline/' + PREFIX + path)
            values = raw.decode().split()
            cert = certs[name]
            roots = [r for r in cert['root_intervals'] if F(r['hi']) < top]
            assert all(not (F(r['lo']) <= top <= F(r['hi'])) for r in cert['root_intervals'])
            q, index, _, _ = SPECS[name]
            chi = dirichlet_char(q, index)
            rows, assigned = [], []
            for line, word in enumerate(values, 1):
                center = F(word)
                radius = F(10) ** Decimal(word).as_tuple().exponent / 2
                lo, hi = center - radius, center + radius
                image = chi.l(acb(arb('0.5'), arb(str(center), str(radius))))
                bounds = [distance(center, F(r['lo']), F(r['hi'])) for r in roots]
                j = min(range(len(roots)), key=lambda k: sum(bounds[k]))
                assert all(bounds[j][1] < b[0] for k, b in enumerate(bounds) if k != j), 'Nearest root is ambiguous'
                root = roots[j]
                inside = lo <= F(root['lo']) and F(root['hi']) <= hi
                disjoint = all(hi < F(r['lo']) or F(r['hi']) < lo for r in roots)
                excluded = not image.contains(0)
                assert not (excluded and inside)
                status = ('excluded_by_L_ball' if excluded else 'certified_root_inside_cell' if inside
                          else 'excluded_by_complete_list' if disjoint else 'unresolved')
                assigned.append(j)
                rows.append({'line': line, 'printed': word, 'displayed_rounding_radius': str(radius),
                             'rounding_cell_status': status, 'L_cell': image.str(65),
                             'nearest_certified_index': j + 1, 'nearest_rounded_root': root['rounded'],
                             'absolute_error_lower': str(bounds[j][0]), 'absolute_error_upper': str(bounds[j][1])})
            missing = [dict(index=j + 1, rounded=r['rounded']) for j, r in enumerate(roots) if j not in assigned]
            duplicates = {str(j + 1): count for j, count in Counter(assigned).items() if count > 1}
            result['tables'].append({'path': PREFIX + path, 'character': name, 'height_cutoff': top,
                                    'before_sha256': hashlib.sha256(raw).hexdigest(),
                                    'original_rows': len(values), 'certified_rows': len(roots),
                                    'rounding_cell_counts': dict(Counter(row['rounding_cell_status'] for row in rows)),
                                    'missing_roots': missing, 'duplicate_nearest_roots': duplicates,
                                    'maximum_absolute_error_upper': str(max(F(r['absolute_error_upper']) for r in rows)),
                                    'rows': rows})
            print(json.dumps({'event': 'table', 'path': path, 'missing': missing,
                              'cell_counts': result['tables'][-1]['rounding_cell_counts']}), flush=True)

    # Independent character construction + mpmath Hurwitz-zeta evaluations.
    for name, cert in certs.items():
        for j in [0, len(cert['root_intervals']) - 1]:
            root = cert['root_intervals'][j]
            center = mp.mpf(root['rounded'])
            derivative = mp.diff(lambda t: independent_L(name, t), center)
            projection = mp.re if abs(mp.re(derivative)) > abs(mp.im(derivative)) else mp.im
            found = mp.findroot(lambda t: projection(independent_L(name, t)),
                                (center - mp.mpf('0.0001'), center + mp.mpf('0.0001')),
                                tol=mp.mpf('1e-58'))
            residual = abs(independent_L(name, found))
            assert mpf(root['lo']) < found < mpf(root['hi']) and residual < mp.mpf('1e-54')
            result['independent_root_checks'].append({'character': name, 'index': j + 1,
                'mpmath_root': mp.nstr(found, 62), 'absolute_L_residual': mp.nstr(residual, 10),
                'inside_certified_interval': True})
        print(json.dumps({'event': 'independent_roots', 'character': name}), flush=True)

    for name in ['chi5', 'chi7']:
        first, conjugate = certs[name]['root_intervals'][0], certs[name + 'bar']['root_intervals'][0]
        assert F(conjugate['hi']) < F(first['lo'])
        for word in ['5.25', '99.36']:
            t = mp.mpf(word)
            lhs = independent_L(name + 'bar', t)
            correct = mp.conj(independent_L(name, -t))
            wrong = mp.conj(independent_L(name, t))
            assert abs(lhs - correct) < mp.mpf('1e-54') and abs(lhs - wrong) > mp.mpf('0.01')
            result['conjugation_checks'].append({'character': name, 't': word,
                'correct_identity_error': mp.nstr(abs(lhs - correct), 10),
                'same_positive_height_identity_error': mp.nstr(abs(lhs - wrong), 18)})

    # A concrete point accepted by the historical absolute completed-function tolerance.
    t, q = mp.mpf('99.36'), 7
    s = mp.mpc('0.5', t)
    value = independent_L('chi7', t)
    completed = mp.power(q / mp.pi, s / 2) * mp.gamma((s + 1) / 2) * value
    assert abs(completed) < mp.mpf('1e-8') and abs(value) > mp.mpf('0.1')
    result['premature_absolute_tolerance_witness'] = {'character': 'chi7', 't': '99.36',
        'absolute_L': mp.nstr(abs(value), 40), 'absolute_completed_L': mp.nstr(abs(completed), 40),
        'historical_completed_tolerance': '1e-8', 'scope': 'Unscaled residual and certified positional error establish the accuracy failure.'}
    result['status'] = 'passed'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates', type=Path, required=True)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.certificates, args.baseline)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'tables': len(result['tables']),
                      'independent_roots': len(result['independent_root_checks'])}))
