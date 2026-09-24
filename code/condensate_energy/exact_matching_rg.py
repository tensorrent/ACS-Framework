#!/usr/bin/env python3
"""Exact symbolic full-theory/EFT RG identities for the matching branch."""
import json
import sympy as s

from hidden_coupling_audit import archived, scalar_polynomial_beta
from finite_light_matching import OUT


def main():
    checks = []

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL', flush=True)

    H, k, a, b, c, d, e, v, C, g4, gL, gR, f, y, split = s.symbols(
        'H k l6 l7 l8 l9 l10 v Mchi2 g4 gL gR f y split', positive=True)
    lam = [0] * 17
    lam[0], lam[6:11], lam[13] = H, [a, b, c, d, e], k
    masses = [C / 2 - k * v ** 2, -C, 0, -2 * b * v ** 2]
    g2 = [g4 ** 2, gL ** 2, gR ** 2]
    matrices = {'Y': s.sqrt(2) * split * y, 'Z': s.sqrt(2) * (1 - split) * y, 'F': f}

    def flavor(word):
        # One real diagonal family; conjugation and transpose are trivial.
        return s.prod(matrices[label[0]] for label in word)

    B = scalar_polynomial_beta(lam)
    B += s.Matrix([lam[i] * sum(s.Rational(archived.GL[i, j]) * g2[j] for j in range(3)) for i in range(17)])
    B += s.Matrix(archived.G['gauge_quartic_coefficients']).applyfunc(s.Rational) * s.Matrix(
        [g2[i] * g2[j] for i, j in archived.G['gauge_square_pairs']])
    for key in ['fermion_box', 'quartic_wave']:
        for row in archived.YUK[key]:
            multiplier = flavor(row['trace_word']) * (lam[row['input_quartic']] if key == 'quartic_wave' else 1)
            B += multiplier * s.Matrix([s.sympify(x) for x in row['coefficients']])
    BM = s.zeros(4, 1)
    for row in archived.M['entries']:
        BM += lam[row['quartic']] * masses[row['mass']] * s.Matrix([s.Rational(x) for x in row['output']])
    BM += s.Matrix([m * value for m, value in zip(masses,
        [-9 * (gL ** 2 + gR ** 2)] * 3 + [-54 * g4 ** 2 - 24 * gR ** 2])])
    for row in archived.YUK['quadratic_wave']:
        BM += flavor(row['trace_word']) * masses[row['input_mass']] * s.Matrix([s.sympify(x) for x in row['coefficients']])
    B = B.applyfunc(s.expand)
    BM = BM.applyfunc(s.expand)
    low = H - k ** 2 / (4 * b)
    Bhigh = B[0] + (B[1] + B[2]) / 4 + B[4] / 2
    Bk = B[13] + B[14] / 2
    Btree = Bhigh - k * Bk / (2 * b) + k ** 2 * B[7] / (4 * b ** 2)
    Bv2 = -BM[3] / (2 * b) - v ** 2 * B[7] / b
    Bmass = BM[0] + BM[1] / 2 + v ** 2 * Bk + k * Bv2

    # Independent heavy jet assembly; the exact full beta coefficients above
    # come from the archived tensor contractions, not these eigenvalue formulas.
    shift, radial_c = k ** 2 / (4 * b), k / (4 * b)
    sectors = [(12, 4 * (d - b) / 3), (12, e + 2 * d / 3 - 5 * b / 3),
               (12, (9 * e + 2 * a - 17 * b + 4 * c + 2 * d) / 9),
               (6, e - b), (6, (3 * e + 2 * a - 5 * b) / 3), (2, 4 * (a - b) / 3)]
    jets = [(n, coefficient * v ** 2, -coefficient * radial_c, 0) for n, coefficient in sectors]
    jets += [(1, 4 * b * v ** 2, -k + 2 * shift, 6 * shift * low / (4 * b * v ** 2)),
             (4, C, low, 0), (18, g4 ** 2 * v ** 2, -g4 ** 2 * radial_c, 0),
             (6, gR ** 2 * v ** 2, gR ** 2 * (s.Rational(1, 4) - radial_c), gL ** 2 / (16 * v ** 2))]
    T = 3 * g4 ** 2 + 2 * gR ** 2
    u = gR ** 4 / (2 * T)
    zl = (gL ** 2 + gR ** 2) / 4 - u
    jets += [(3, T * v ** 2, -T * radial_c + u, u * zl / (T * v ** 2)),
             (-2, 2 * f ** 2 * v ** 2, -2 * f ** 2 * radial_c + y ** 2, -y ** 4 / (8 * f ** 2 * v ** 2))]
    Dpotential = -4 * sum(n * (2 * M * bb + aa ** 2) for n, M, aa, bb in jets)
    Dmass = -4 * sum(n * M * aa for n, M, aa, bb in jets)
    Cheavy = gR ** 2 / 2 + u
    Dkinetic = 24 * low * Cheavy - 8 * low * y ** 2
    gy2 = 3 * g4 ** 2 * gR ** 2 / T
    Blight = 2 * (24 * low ** 2 - (9 * gL ** 2 + 3 * gy2) * low
                  + s.Rational(3, 8) * (2 * gL ** 4 + (gL ** 2 + gy2) ** 2)
                  + 28 * low * y ** 2 - 14 * y ** 4)
    residual = s.factor(Btree + Dpotential + Dkinetic - Blight)
    mass_residual = s.factor(Bmass + Dmass)
    check('exact-all-coupling-quartic-RG-identity', residual == 0, str(residual))
    check('exact-all-coupling-mass-RG-identity', mass_residual == 0, str(mass_residual))
    check('exact-independence-of-orthogonal-doublet-Yukawa-split', s.simplify(s.diff(Btree, split)) == 0 and s.simplify(s.diff(Bmass, split)) == 0)
    no_wave = s.factor(Btree + Dpotential - Blight)
    check('omitting-wave-function-fails-generic-RG-identity', no_wave != 0 and s.factor(no_wave + Dkinetic) == 0)
    output = dict(checks=checks, checks_passed=sum(c['passed'] for c in checks), checks_total=len(checks),
        scaling='All beta and explicit matching-scale derivatives multiplied by 32 pi^2',
        tree_quartic_beta=str(s.factor(Btree)), tree_mass_beta=str(s.factor(Bmass)),
        missing_wave_residual=str(no_wave), canonical_quartic_residual=str(residual), mass_residual=str(mass_residual),
        domain='Real diagonal flavor, arbitrary stable Delta quartics l6..l10, norm portal and declared determinant mass. '
               'One-family Yukawa identity extends by summing diagonal families: all one-loop flavor terms are single traces.')
    (OUT / 'exact-RG.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=output['checks_passed'], checks_total=len(checks))))
    assert all(c['passed'] for c in checks), 'Failed checks retained in exact-RG.json'


if __name__ == '__main__':
    main()
