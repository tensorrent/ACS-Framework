"""Measure how certified ordinates change finite character-phase observables."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import numpy as np
from flint import acb, arb, ctx, dirichlet_char

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
CASES = [('chi5', 5, 2, 'cyclotomic_5/zeros_chi_5_order4'),
         ('chi7', 7, 3, 'cyclotomic_7/zeros_chi_7_order6')]


def float_table(words, chi):
    gammas = np.array([float(w) for w in words])
    primes = [p for p in PRIMES if chi(p) != 0]
    chars = np.array([complex(chi(p)) for p in primes])
    phases = np.array([np.exp(1j * k * np.log(primes)[:, None] * gammas).sum(axis=1)
                       for k in [1, 2, 3]])
    phases /= np.abs(phases)
    return [[float(abs(np.mean(phases[k] * np.conj(chars) ** m))) for m in [1, 2, 3]]
            for k in range(3)]


def interval_table(words, chi):
    gammas = [arb(w, '5e-21') for w in words]
    primes = [p for p in PRIMES if chi(p) != 0]
    result = []
    for k in [1, 2, 3]:
        phases = []
        for p in primes:
            u = k * arb(p).log()
            w = sum((acb(0, u * g).exp() for g in gammas), acb(0))
            assert not abs(w).contains(0)
            phases.append(w / abs(w))
        row = []
        for m in [1, 2, 3]:
            mean = sum((phase * chi(p).conjugate() ** m for p, phase in zip(primes, phases)), acb(0)) / len(primes)
            row.append(abs(mean))
        result.append(row)
    return result


def main(baseline, data_root):
    ctx.prec = 160
    result = {'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'precision_bits': ctx.prec, 'cases': [],
              'scope': 'Finite one-sided phase resultants; ordinate rounding is propagated. Statistical significance, infinite tails and operator identification are separate.'}
    with zipfile.ZipFile(baseline) as old:
        for name, q, n, stem in CASES:
            chi = dirichlet_char(q, n)
            for suffix in ['', '_ext']:
                path = stem + suffix + '.txt'
                before = old.read('baseline/code/hp_knife_suite/data_zeros/' + path)
                after = (data_root / path).read_bytes()
                a, b = before.decode().split(), after.decode().split()
                before_R, after_R = float_table(a, chi), float_table(b, chi)
                balls = interval_table(b, chi)
                assert all(abs(float(balls[k][m].mid()) - after_R[k][m]) < 2e-12
                           for k in range(3) for m in range(3))
                threshold = 2 / arb(sum(chi(p) != 0 for p in PRIMES)).sqrt()
                resolved = [balls[k][k] > threshold for k in range(3)]
                result['cases'].append({'character': name, 'file': path,
                    'before_sha256': hashlib.sha256(before).hexdigest(),
                    'after_sha256': hashlib.sha256(after).hexdigest(),
                    'before_rows': len(a), 'after_rows': len(b), 'before_R': before_R,
                    'after_R': after_R, 'after_R_balls': [[x.str(40) for x in row] for row in balls],
                    'twice_heuristic_floor': threshold.str(40), 'own_power_exceeds_twice_floor': resolved})
    result['status'] = 'passed'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--data-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = main(args.baseline, args.data_root)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
