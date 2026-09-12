"""Recompute the canonical finite normalized sum with 70-digit arithmetic."""
import hashlib
import json
from pathlib import Path
import sys

import mpmath as mp
import numpy as np


def main():
    root = Path(__file__).resolve().parents[2]
    code = root / 'code/acs_codebase'
    sys.path.insert(0, str(code))
    from src.paper_b.renormalized_stability import delta_norm
    from src.paper_b.explicit_formula_resolvent import RIEMANN_ZEROS
    mp.mp.dps = 70
    cases = []
    for u in [5, 20, 700, 710, 1000]:
        expected = -2 * mp.fsum(
            (mp.exp(1j * mp.mpf(str(g)) * u) / (mp.mpf('.5') + 1j * mp.mpf(str(g)))).real
            for g in RIEMANN_ZEROS
        )
        with np.errstate(over='raise', invalid='raise'):
            actual = float(delta_norm(u))
        error = abs(mp.mpf(actual) - expected)
        assert np.isfinite(actual) and error < mp.mpf('5e-11')
        cases.append({'u': u, 'float64_result': actual, 'mpmath_70_digit_result': str(expected),
                      'absolute_difference': str(error)})
    source = code / 'src/paper_b/renormalized_stability.py'
    print(json.dumps({'status': 'passed', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'corrected_source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                      'cases': cases, 'scope': 'Finite supplied spectrum only; no arithmetic RH claim.'}, indent=2))


if __name__ == '__main__':
    main()
