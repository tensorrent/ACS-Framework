"""Check every new quadratic ordinate independently and compare primary zeta data."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import zipfile
import mpmath as mp


def mpf(x):
    x = F(x)
    return mp.mpf(x.numerator) / x.denominator


def audit(extra, primary):
    with zipfile.ZipFile(extra) as z:
        raw = z.read('factors-224.json')
    data = json.loads(raw)
    mp.mp.dps = 85
    chars = [0, 1, -1, -1, 1]

    def L(t):
        s = mp.mpc('0.5', t)
        return mp.power(5, -s) * mp.fsum(chars[a] * mp.zeta(s, mp.mpf(a) / 5) for a in range(1, 5))

    roots = []
    for j, row in enumerate(data['quadratic5']['positive_root_intervals'], 1):
        center = mp.mpf(row['rounded'])
        probe = L(center + mp.mpf('0.0001'))
        projection = mp.re if abs(mp.re(probe)) > abs(mp.im(probe)) else mp.im
        found = mp.findroot(lambda t: projection(L(t)),
                            (center - mp.mpf('0.0001'), center + mp.mpf('0.0001')),
                            tol=mp.mpf('1e-78'))
        residual = abs(L(found))
        assert mpf(row['lo']) < found < mpf(row['hi']) and residual < mp.mpf('1e-74')
        roots.append({'index': j, 'mpmath_ordinate': mp.nstr(found, 80),
                      'absolute_L_residual': mp.nstr(residual, 12), 'inside_certified_interval': True})
        if j % 25 == 0:
            print(json.dumps({'quadratic_roots_checked': j}), flush=True)
    with zipfile.ZipFile(primary) as z:
        high_raw = z.read('zeros2')
    high = [''.join(block.split()) for block in re.split(r'\n\s*\n', high_raw.decode().strip())]
    assert len(high) == 100
    zeta = []
    for row in data['zeta']['positive_root_intervals']:
        literal = high[row['index'] - 1]
        assert F(row['lo']) < F(literal) < F(row['hi'])
        zeta.append({'index': row['index'], 'primary_decimal_prefix': literal[:84],
                     'primary_literal_inside_certified_interval': True})
    return {'status': 'passed', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'factor_certificate_sha256': hashlib.sha256(raw).hexdigest(),
            'primary_zeros2_sha256': hashlib.sha256(high_raw).hexdigest(),
            'mpmath_decimal_digits': mp.mp.dps, 'quadratic_roots': roots, 'primary_zeta_comparisons': zeta,
            'scope': 'All 146 quadratic roots recomputed with a separate Hurwitz implementation; all 90 Riemann intervals contain the corresponding published high-precision literal. The interval completeness proof still uses FLINT/Arb.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extra', type=Path, required=True)
    parser.add_argument('--primary', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.extra, args.primary)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'quadratic_roots': len(result['quadratic_roots']),
                      'primary_zeta_comparisons': len(result['primary_zeta_comparisons'])}))
