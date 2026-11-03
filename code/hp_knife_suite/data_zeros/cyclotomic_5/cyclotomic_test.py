"""Reproduce matched-cutoff Q(zeta_5) finite witness comparisons.

The historical doubled-character, per-factor-normalized implementation is
archived in the Frontier source snapshots. This entry point uses every factor,
compares normalization and sampling choices, and writes a reproducible JSON
record. Its finite statistics are not an infinite explicit-formula theorem.
"""
import argparse
import json
from pathlib import Path
import sys


def main():
    code = Path(__file__).resolve().parents[3]
    root = code.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extra', type=Path, default=root / 'docs/frontier/2026-09-13-dedekind-delta/Factor_Certificates.zip')
    parser.add_argument('--prior', type=Path, default=root / 'docs/frontier/2026-09-13-lfunction-delta/Certificates.zip')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(code / 'frontier_verification'))
    from dedekind_witness_audit import audit
    result = audit(args.extra, args.prior)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'configurations': len(result['configurations']),
                      'independent_checks': len(result['independent_checks'])}))


if __name__ == '__main__':
    main()
