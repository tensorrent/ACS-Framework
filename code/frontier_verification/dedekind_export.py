"""Export four certified factor tables with a common precision manifest."""
import argparse
import hashlib
import json
from pathlib import Path
from dedekind_inputs import load_factors, at_height

PATHS = {'zeta': 'riemann_zeros_220_certified.txt',
         'chi1': 'cyclotomic_5/zeros_chi_5_order4_ext.txt',
         'chi2': 'cyclotomic_5/zeros_chi_5_quadratic_ext.txt',
         'chi3': 'cyclotomic_5/zeros_chi_5_order4_conjugate_ext.txt'}


def export(extra, prior, output):
    factors, identity = load_factors(extra, prior)
    manifest = {'schema': 1, 'input_identity': identity, 'height_cutoff': 220,
                'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'factors': {}, 'scope': 'Positive-height factors of Q(zeta_5), with multiplicity one per factor root.'}
    for name, rows in factors.items():
        path = output / PATHS[name]
        raw = ''.join(r['rounded'] + '\n' for r in rows).encode()
        if path.exists():
            assert path.read_bytes() == raw, ('Refusing to overwrite a different table', path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        manifest['factors'][name] = {'path': PATHS[name], 'rows': len(rows),
                                    'sha256': hashlib.sha256(raw).hexdigest(),
                                    'absolute_decimal_error_bound': '5e-21',
                                    'root_intervals': [{'lo': r['lo'], 'hi': r['hi']} for r in rows]}
    manifest['counts_by_cutoff'] = {str(t): {n: len(rows) for n, rows in at_height(factors, t).items()}
                                    for t in [60, 80, 100, 140, 180, 220]}
    (output / 'DEDEKIND_FACTORS.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extra', type=Path, required=True)
    parser.add_argument('--prior', type=Path, required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    args = parser.parse_args()
    result = export(args.extra, args.prior, args.output_root)
    print(json.dumps({'status': 'passed', 'factors': {n: {k: v for k, v in x.items() if k != 'root_intervals'}
                                                    for n, x in result['factors'].items()}}, indent=2))
