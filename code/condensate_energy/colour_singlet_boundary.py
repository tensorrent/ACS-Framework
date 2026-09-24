#!/usr/bin/env python3
"""Test the archived RGB/singlet identification by exact representation action."""
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy/endpoint_audit'


def audit_colour_singlet():
    source = Path('/Users/coo-koba42/dev/reports/rh-research-audit-20260923/'
                  'seagate-extension/history-text/'
                  '1c0ad2302178138463e45a6a45bba0ee857d4a85ac4ed0fef07aa1cbf877ff94.txt')
    snapshot = OUT / 'source-snapshots/newton_colour_music-1.py'
    snapshot.write_bytes(source.read_bytes())
    provenance = dict(source=str(source), snapshot=str(snapshot.relative_to(ROOT)),
                      sha256=sha256(snapshot.read_bytes()).hexdigest(),
                      scope='Complete recovered source read; exact claim tested; plot program not replayed')
    (OUT / 'colour-provenance.json').write_text(json.dumps([provenance], indent=2) + '\n')
    generators = []
    for a, b in [(0, 1), (0, 2), (1, 2)]:
        real = s.zeros(3); imag = s.zeros(3)
        real[a, b] = real[b, a] = s.Rational(1, 2)
        imag[a, b] = -s.I / 2; imag[b, a] = s.I / 2
        generators.extend([real, imag])
    generators.extend([s.diag(1, -1, 0) / 2,
                       s.diag(1, 1, -2) / (2 * s.sqrt(3))])
    checks = []

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))

    check('eight normalized traceless Hermitian generators',
          all(t == t.H and s.trace(t) == 0 for t in generators) and
          all(s.simplify(s.trace(a*b) - (s.Rational(1, 2) if i == j else 0)) == 0
              for i, a in enumerate(generators) for j, b in enumerate(generators)))
    state = s.ones(3, 1) / s.sqrt(3)
    check('source equal-superposition state has unit norm', (state.H * state)[0] == 1)
    moved = generators[6] * state
    check('source state is not a singlet', moved != s.zeros(3, 1),
          {'T3_state': [str(v) for v in moved]})
    check('both Cartan expectations nevertheless vanish',
          all(s.simplify((state.H * t * state)[0]) == 0 for t in generators[6:]))
    variance = s.simplify(sum((state.H * t * t * state)[0] for t in generators[6:]))
    check('zero mean charges still have nonzero variance', variance == s.Rational(1, 3), str(variance))
    casimir = sum((t*t for t in generators), s.zeros(3))
    check('fundamental quadratic Casimir is four thirds', casimir == s.Rational(4, 3) * s.eye(3))
    stacked = s.Matrix.vstack(*generators)
    check('no nonzero fundamental vector is invariant', stacked.rank() == 3)
    meson = s.Matrix([int(i == j) for i in range(3) for j in range(3)]) / s.sqrt(3)
    meson_generators = [s.kronecker_product(t, s.eye(3)) - s.kronecker_product(s.eye(3), s.conjugate(t))
                        for t in generators]
    check('triplet times antitriplet has the expected singlet',
          (meson.H * meson)[0] == 1 and all(s.simplify(t*meson) == s.zeros(9, 1) for t in meson_generators))
    baryon = s.zeros(27, 1)
    for p in permutations(range(3)):
        inversions = sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3))
        baryon[9*p[0]+3*p[1]+p[2]] = (-1)**inversions / s.sqrt(6)
    baryon_generators = [s.kronecker_product(t, s.eye(3), s.eye(3))
                         + s.kronecker_product(s.eye(3), t, s.eye(3))
                         + s.kronecker_product(s.eye(3), s.eye(3), t) for t in generators]
    check('three triplets have the expected antisymmetric singlet',
          (baryon.H * baryon)[0] == 1 and all(s.simplify(t*baryon) == s.zeros(27, 1) for t in baryon_generators))
    result = dict(checks_total=len(checks), checks_passed=sum(c['passed'] for c in checks), checks=checks,
                  conclusion='The equal superposition is a triplet, not a singlet. Zero Cartan means do not establish invariance.',
                  limits=['No physical color/optical equivalence is assumed',
                          'No claim about Newton historical attribution or biological color response is tested',
                          'Tensor singlets require a composite representation, not a coordinate relabeling'])
    (OUT / 'colour-singlet.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    if result['checks_passed'] != result['checks_total']:
        raise SystemExit(1)


if __name__ == '__main__':
    audit_colour_singlet()
