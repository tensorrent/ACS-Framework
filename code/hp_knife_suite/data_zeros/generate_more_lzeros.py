#!/usr/bin/env python3
# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""Generate mod-5/mod-7 lists with finite interval completeness certificates.

The historical Im(L) scan missed three mod-7 roots. Its implementation and
outputs are preserved in docs/frontier/2026-09-12-source-delta/Source_Snapshot.zip.
This replacement proves the finite count before exporting rounded ordinates.
It supports cutoffs up to 220; larger ranges require a new audit.
An explicit output directory separates research runs from shipped data.
"""
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('height', type=int, nargs='?', default=220)
    parser.add_argument('--output-root', type=Path, required=True)
    args = parser.parse_args()
    if not 0 < args.height <= 220:
        parser.error('The audited range is 0 < height <= 220.')
    code = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(code / 'frontier_verification'))
    from lfunction_zero_certificate import certify
    from lfunction_table_export import export_tables
    certificates = args.output_root / 'certificates'
    for name in ['chi5', 'chi7']:
        certify(name, certificates / (name + '.json'))
    export_tables(certificates, args.output_root, {
        'cyclotomic_5/zeros_chi_5_order4_ext.txt': ('chi5', args.height),
        'cyclotomic_7/zeros_chi_7_order6_ext.txt': ('chi7', args.height)})


if __name__ == '__main__':
    main()
