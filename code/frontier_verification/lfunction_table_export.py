"""Export rounded tables from previously validated finite certificates.

This deterministic exporter does not replace certificate replay. The manifest
retains exact root intervals, character IDs and certificate hashes.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from lfunction_data_audit import TABLES

EXPORT_TABLES = {**TABLES,
    'cyclotomic_5/zeros_chi_5_order4_conjugate_ext.txt': ('chi5bar', 220),
    'cyclotomic_7/zeros_chi_7_order6_conjugate_ext.txt': ('chi7bar', 220)}


def export_tables(certificates, output_root, tables=None):
    tables = EXPORT_TABLES if tables is None else tables
    manifest = {'schema': 1, 'scope': 'Positive-height zeros only; finite certified rectangles.',
                'exporter_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'certificate_replay_required': True, 'files': {}}
    for path, (name, top) in tables.items():
        raw = (certificates / (name + '.json')).read_bytes()
        cert = json.loads(raw)
        assert cert['character'] == name and cert['status'] == 'passed'
        assert cert['top'] >= top > 0
        assert cert['contour']['zero_count'] == len(cert['root_intervals'])
        roots = []
        for root in cert['root_intervals']:
            lo, hi, d, r = map(F, [root['lo'], root['hi'], root['rounded'], root['rounding_cell_radius']])
            assert d - r < lo < hi < d + r and r == F(1, 2 * 10**20)
            assert not lo <= top <= hi, 'Cutoff crosses a root interval'
            if hi < top:
                assert not roots or F(roots[-1]['hi']) < lo
                roots.append(root)
        data = ''.join(r['rounded'] + '\n' for r in roots).encode()
        target = output_root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        manifest['files'][path] = {'character': name, 'modulus': cert['character_check']['modulus'],
            'conrey_number': cert['character_check']['conrey_number'], 'height_cutoff': top,
            'rows': len(roots), 'sha256': hashlib.sha256(data).hexdigest(),
            'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'certificate_file': name + '.json',
            'absolute_rounding_error_bound': '5e-21',
            'root_intervals': [{'lo': r['lo'], 'hi': r['hi']} for r in roots]}
    (output_root / 'LFUNCTION_CERTIFICATES.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates', type=Path, required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    args = parser.parse_args()
    manifest = export_tables(args.certificates, args.output_root)
    print(json.dumps({p: {k: v for k, v in d.items() if k != 'root_intervals'}
                      for p, d in manifest['files'].items()}, indent=2))
