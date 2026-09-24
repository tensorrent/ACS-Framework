#!/usr/bin/env python3
"""Finite one-loop mass/quartic matching in a declared stable ACS branch.

Landau gauge, MS-bar, one light doublet, real diagonal flavor. Full component
spectra cross-check the closed eigenvalues; matching includes the kinetic term.
"""
from dataclasses import dataclass, asdict, replace
import json
import math

import mpmath as mp
import numpy as np
from scipy.integrate import quad
import sympy as s

from canonical_scalar_action import ROOT, load_exact_basis, scalar_pack, scalar_unpack, polynomial_derivatives
from hidden_coupling_audit import gauge_matrices, linear_combination, archived, mass
from radiative_flat_modes import gauge_gram, cw_sum

OUT = ROOT / 'docs/condensate_energy/finite_matching'


@dataclass(frozen=True)
class Parameters:
    lambda0: float = .2
    delta: tuple = (.6, .5, .6, .6, .6)
    portal: float = .2
    d: float = 1.
    second_doublet_mass2: float = .7
    gauges: tuple = (.3, .25, .35)
    majorana: tuple = (.2, .3, .4)
    dirac: tuple = (.07, .11, .16)
    mu: float = 1.

    @property
    def lam7(self):
        return self.delta[1]

    @property
    def shift(self):
        return self.portal ** 2 / (4 * self.lam7)

    @property
    def light(self):
        return self.lambda0 - self.shift

    @property
    def c(self):
        return self.portal / (4 * self.lam7)


def couplings(p):
    lam = np.zeros(17)
    lam[0], lam[6:11], lam[13] = p.lambda0, p.delta, p.portal
    masses = np.array([p.second_doublet_mass2 / 2 - p.portal * p.d ** 2,
                       -p.second_doublet_mass2, 0., -2 * p.lam7 * p.d ** 2])
    # The selected real doublet has y=(Y+Z)/sqrt(2). The orthogonal
    # doublet also couples, through a different explicitly retained combination.
    y = np.array(p.dirac)
    Y, Z, F = np.diag(.7 * np.sqrt(2) * y), np.diag(.3 * np.sqrt(2) * y), np.diag(p.majorana)
    return lam, masses, Y.astype(complex), Z.astype(complex), F.astype(complex)


def delta_sectors(p):
    a, b, c, d, e = p.delta
    return [('bar6_minus', 12, 4 * (d - b) / 3),
            ('bar6_zero', 12, e + 2 * d / 3 - 5 * b / 3),
            ('bar6_plus', 12, (9 * e + 2 * a - 17 * b + 4 * c + 2 * d) / 9),
            ('bar3_zero', 6, e - b), ('bar3_plus', 6, (3 * e + 2 * a - 5 * b) / 3),
            ('singlet_plus', 2, 4 * (a - b) / 3)]


def background(p, h):
    r = math.sqrt(p.d ** 2 - p.c * h ** 2)
    D = np.zeros((3, 4, 4), complex)
    D[:, 3, 3] = r * np.array([1, -1j, 0]) / math.sqrt(2)
    return scalar_pack(h * np.eye(2) / 2, D)


def quadratic_roots(trace, determinant, backend=math):
    heavy = (trace + backend.sqrt(trace ** 2 - 4 * determinant)) / 2
    return heavy, determinant / heavy if heavy else trace * 0


def closed_spectra(p, h, backend=math):
    t = h * h
    r2 = p.d ** 2 - p.c * t
    scalar = [0.] * 9
    for label, count, coefficient in delta_sectors(p):
        scalar += [coefficient * r2] * count
    scalar += [p.second_doublet_mass2 + p.light * t] * 4 + [p.light * t] * 3
    # Full radial/light Hessian, not a heavy-only determinant.
    hll, hrr = (3 * p.lambda0 - p.shift) * t, 4 * p.lam7 * r2
    mixed2 = 2 * p.portal ** 2 * r2 * t
    scalar += list(quadratic_roots(hll + hrr, hll * hrr - mixed2, backend))
    g4, gL, gR = p.gauges
    total = 3 * g4 ** 2 + 2 * gR ** 2
    gy2 = 3 * g4 ** 2 * gR ** 2 / total if total else 0.
    vector = [0.] * 9 + [g4 ** 2 * r2] * 6
    W = quadratic_roots(gR ** 2 * r2 + (gL ** 2 + gR ** 2) * t / 4,
                        gR ** 2 * r2 * gL ** 2 * t / 4, backend)
    Z = quadratic_roots(total * r2 + (gL ** 2 + gR ** 2) * t / 4,
                        total * r2 * (gL ** 2 + gy2) * t / 4, backend)
    vector += [W[0]] * 2 + [W[1]] * 2 + list(Z)
    fermion = []
    for f, y in zip(p.majorana, p.dirac):
        md2, mn2 = y ** 2 * t / 2, 2 * f ** 2 * r2
        fermion += [md2] * 14 + list(quadratic_roots(mn2 + 2 * md2, md2 ** 2, backend))
    return scalar, vector, fermion


def heavy_jets(p):
    rows = []

    def add(label, sector, n, M, a, b=0.):
        if M > 0:
            rows.append(dict(label=label, sector=sector, multiplicity=n, M2=M, a=a, b=b,
                             constant=5 / 6 if sector == 'vector' else 1.5))

    for label, n, coefficient in delta_sectors(p):
        add(label, 'scalar', n, coefficient * p.d ** 2, -coefficient * p.c)
    M = 4 * p.lam7 * p.d ** 2
    add('radial_mixed', 'scalar', 1, M, -p.portal + 2 * p.shift, 6 * p.shift * p.light / M)
    add('second_doublet', 'scalar', 4, p.second_doublet_mass2, p.light)
    g4, gL, gR = p.gauges
    total = 3 * g4 ** 2 + 2 * gR ** 2
    add('color_vectors', 'vector', 18, g4 ** 2 * p.d ** 2, -g4 ** 2 * p.c)
    add('right_vectors', 'vector', 6, gR ** 2 * p.d ** 2,
        gR ** 2 * (1 / 4 - p.c), gL ** 2 / (16 * p.d ** 2))
    if total:
        u = gR ** 4 / (2 * total)
        zlight = (gL ** 2 + gR ** 2) / 4 - u
        add('neutral_vector', 'vector', 3, total * p.d ** 2,
            -total * p.c + u, u * zlight / (total * p.d ** 2))
    for i, (f, y) in enumerate(zip(p.majorana, p.dirac)):
        M = 2 * f ** 2 * p.d ** 2
        add('Majorana_' + str(i), 'fermion', -2, M,
            -2 * f ** 2 * p.c + y ** 2, -y ** 4 / (4 * M))
    return rows


def threshold(p):
    rows = []
    for row in heavy_jets(p):
        M, a, b, n, c = [row[k] for k in ['M2', 'a', 'b', 'multiplicity', 'constant']]
        L = math.log(M / p.mu ** 2)
        dm = n * M * a * (L - c + .5) / (16 * np.pi ** 2)
        dl = n * (2 * M * b * (L - c + .5) + a ** 2 * (L - c + 1.5)) / (16 * np.pi ** 2)
        rows.append(dict(**row, mass_threshold=dm, potential_quartic_threshold=dl))
    g4, gL, gR = p.gauges
    total = 3 * g4 ** 2 + 2 * gR ** 2
    zs = p.shift / (16 * np.pi ** 2)
    zg = 0.
    if gR:
        zg = (gR ** 2 / 2 * (3 * math.log(gR ** 2 * p.d ** 2 / p.mu ** 2) - 2.5)
              + gR ** 4 / (2 * total) * (3 * math.log(total * p.d ** 2 / p.mu ** 2) - 2.5)) / (16 * np.pi ** 2)
    zf = sum(y ** 2 * (.5 - math.log(2 * f ** 2 * p.d ** 2 / p.mu ** 2))
             for f, y in zip(p.majorana, p.dirac)) / (16 * np.pi ** 2)
    dl = sum(r['potential_quartic_threshold'] for r in rows)
    kinetic = -2 * p.light * (zs + zg + zf)
    return dict(rows=rows, tree_quartic=p.light, mass_threshold=sum(r['mass_threshold'] for r in rows),
        potential_quartic_threshold=dl, kinetic=dict(scalar=zs, vector=zg, fermion=zf,
        total=zs + zg + zf), kinetic_quartic_threshold=kinetic,
        canonical_quartic=p.light + dl + kinetic, total_quartic_threshold=dl + kinetic)


def low_potential(p, h, backend=math):
    g4, gL, gR = p.gauges
    total = 3 * g4 ** 2 + 2 * gR ** 2
    gy2 = 3 * g4 ** 2 * gR ** 2 / total if total else 0.
    scalars = [3 * p.light * h * h] + [p.light * h * h] * 3
    vectors = [gL ** 2 * h * h / 4] * 2 + [(gL ** 2 + gy2) * h * h / 4]
    fermions = [y ** 2 * h * h / 2 for y in p.dirac for _ in range(14)]
    return loop_potential(p, (scalars, vectors, fermions), backend)


def loop_potential(p, spectra, backend=math):
    pi = backend.pi
    result = 0
    for masses, n, c in zip(spectra, [1, 3, -2], [1.5, 5 / 6, 1.5]):
        for x in masses:
            if x > 0:
                # Exact rational constants in the high-precision path.
                const = (backend.mpf(5) / 6 if n == 3 else backend.mpf(3) / 2) if backend is mp else c
                result += n * x ** 2 * (backend.log(x / p.mu ** 2) - const)
    return result / (64 * pi ** 2)


def rg_check(p):
    lam, masses, Y, Z, F = couplings(p)
    beta = archived.beta(lam, masses, p.gauges, Y, Z, F)
    b = beta['quartics']
    high_derivative = b[0] + (b[1] + b[2]) / 4 + b[4] / 2
    portal_derivative = b[13] + b[14] / 2
    tree_derivative = high_derivative - p.portal * portal_derivative / (2 * p.lam7) + p.portal ** 2 * b[7] / (4 * p.lam7 ** 2)
    d2_derivative = -beta['masses'][3] / (2 * p.lam7) - p.d ** 2 * b[7] / p.lam7
    mass_derivative = beta['masses'][0] + beta['masses'][1] / 2 + p.d ** 2 * portal_derivative + p.portal * d2_derivative
    h = 1e-3
    above, below = threshold(replace(p, mu=p.mu * math.exp(h))), threshold(replace(p, mu=p.mu * math.exp(-h)))
    threshold_derivative = (above['total_quartic_threshold'] - below['total_quartic_threshold']) / (2 * h)
    mass_threshold_derivative = (above['mass_threshold'] - below['mass_threshold']) / (2 * h)
    g4, gL, gR = p.gauges
    total = 3 * g4 ** 2 + 2 * gR ** 2
    gy2 = 3 * g4 ** 2 * gR ** 2 / total if total else 0.
    low_beta = (24 * p.light ** 2 - (9 * gL ** 2 + 3 * gy2) * p.light
                + 3 / 8 * (2 * gL ** 4 + (gL ** 2 + gy2) ** 2)
                + 28 * p.light * sum(y ** 2 for y in p.dirac) - 14 * sum(y ** 4 for y in p.dirac)) / (16 * np.pi ** 2)
    return dict(tree_derivative=tree_derivative, threshold_derivative=threshold_derivative,
        low_beta=low_beta, quartic_residual=tree_derivative + threshold_derivative - low_beta,
        mass_tree_derivative=mass_derivative, mass_threshold_derivative=mass_threshold_derivative,
        mass_residual=mass_derivative + mass_threshold_derivative)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    checks, result = [], {}

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL', flush=True)

    # Exact jets from characteristic equations, without numerical fitting.
    t, L, k, l7, d, g4, gL, gR, f, y = s.symbols('t L k l7 d g4 gL gR f y', positive=True)
    shift, c = k ** 2 / (4 * l7), k / (4 * l7)
    M = 4 * l7 * d ** 2
    x = M + (-k + 2 * shift) * t + 6 * shift * (L - shift) / M * t ** 2
    char = (x - (3 * L - shift) * t) * (x - M + k * t) - 2 * k ** 2 * (d ** 2 - c * t) * t
    check('exact-mixed-radial-heavy-jet', all(s.simplify(s.expand(char).coeff(t, j)) == 0 for j in range(3)))
    for label, M, tr, det, a, b in [
        ('charged-vector', gR ** 2 * d ** 2,
         gR ** 2 * (d ** 2 - c * t) + (gL ** 2 + gR ** 2) * t / 4,
         gR ** 2 * (d ** 2 - c * t) * gL ** 2 * t / 4,
         gR ** 2 * (s.Rational(1, 4) - c), gL ** 2 / (16 * d ** 2)),
        ('Majorana', 2 * f ** 2 * d ** 2, 2 * f ** 2 * (d ** 2 - c * t) + y ** 2 * t,
         y ** 4 * t ** 2 / 4, -2 * f ** 2 * c + y ** 2, -y ** 4 / (8 * f ** 2 * d ** 2))]:
        x = M + a * t + b * t ** 2
        char = s.expand(x ** 2 - tr * x + det)
        check('exact-' + label + '-heavy-jet', all(s.simplify(char.coeff(t, j)) == 0 for j in range(3)))
    T = 3 * g4 ** 2 + 2 * gR ** 2
    u = gR ** 4 / (2 * T)
    zlight = (gL ** 2 + gR ** 2) / 4 - u
    check('hypercharge-matching', s.simplify(zlight - (gL ** 2 + 3 * g4 ** 2 * gR ** 2 / T) / 4) == 0)
    x = T * d ** 2 + (-T * c + u) * t + u * zlight / (T * d ** 2) * t ** 2
    char = s.expand(x ** 2 - (T * (d ** 2 - c * t) + (gL ** 2 + gR ** 2) * t / 4) * x + T * (d ** 2 - c * t) * zlight * t)
    check('exact-neutral-vector-heavy-jet', all(s.simplify(char.coeff(t, j)) == 0 for j in range(3)))
    eps, log, m2 = s.symbols('epsilon logM M2', positive=True)
    regulated = 4 * (1 - 1 / (4 - 2 * eps)) * (1 / eps + 1 - log)
    finite = s.limit(regulated - 3 / eps, eps, 0)
    check('vector-kinetic-evanescent-finite-term', finite == s.Rational(5, 2) - 3 * log)
    z = s.symbols('z', real=True)
    integral = s.integrate((1 - z) / m2, (z, 0, 1))
    check('scalar-heavy-light-two-point-integral', integral == 1 / (2 * m2))
    check('Majorana-two-point-finite-term', s.simplify((1 - log) - m2 * integral - (s.Rational(1, 2) - log)) == 0)
    check('heavy-vector-generator-weight', s.simplify(gR ** 2 / 2 + u - (3 * gR ** 2 / 4 - 3 * g4 ** 2 * gR ** 2 / (4 * T))) == 0)

    polynomials, quadratics, metric = load_exact_basis()
    matrices, groups, weights = gauge_matrices()
    base = Parameters()
    cases = [('full_three_family', base),
        ('one_family', replace(base, majorana=(.31,), dirac=(.14,), portal=.12)),
        ('zero_portal', replace(base, portal=0.)),
        ('scalar_only', replace(base, gauges=(0., 0., 0.), dirac=(0., 0., 0.), majorana=(.2, .3, .4))),
        ('scalar_gauge', replace(base, dirac=(0., 0., 0.))),
        ('scalar_Yukawa', replace(base, gauges=(0., 0., 0.))),
        ('different_full_basis', replace(base, delta=(.71, .43, .82, .64, .79), d=1.27, mu=.83, portal=.17))]
    rows = []
    for label, p in cases:
        check(label + '-tree-gaps-and-positive-light-quartic', min(v for _, _, v in delta_sectors(p)) > 0 and p.light > 0)
        lam, masses, Y, Z, F = couplings(p)
        poly = linear_combination(polynomials, lam / 18)
        qpoly = linear_combination(quadratics, masses)
        errors = []
        for h in [0., .03, .09]:
            field = background(p, h)
            v4, grad4, h4 = polynomial_derivatives(poly, field)
            v2, grad2, h2 = polynomial_derivatives(qpoly, field)
            scalar = np.linalg.eigvalsh((h4 + h2) / np.sqrt(metric[:, None] * metric[None, :]))
            vector = np.linalg.eigvalsh(gauge_gram(field, p.gauges, metric, matrices, groups, weights))
            phi, delta = scalar_unpack(field)
            M = mass(phi, delta, Y, Z, F)
            fermion = np.linalg.eigvalsh(M.conj().T @ M)
            predicted = closed_spectra(p, h)
            residual = [float(max(abs(actual - np.sort(expected)))) for actual, expected in zip([scalar, vector, fermion], predicted)]
            errors.append(residual)
            check(label + '-full-component-spectra-h-' + str(h), max(residual) < 2e-11, residual)
            check(label + '-heavy-radial-EOM-h-' + str(h), max(abs((grad4 + grad2)[8:])) < 1e-12)
            check(label + '-tree-potential-h-' + str(h), abs(v4 + v2 + p.lam7 * p.d ** 4 - p.light * h ** 4 / 4) < 1e-12)
        rg = rg_check(p)
        check(label + '-quartic-RG-cancellation', abs(rg['quartic_residual']) < 1e-10, rg)
        check(label + '-mass-RG-cancellation', abs(rg['mass_residual']) < 1e-10, rg['mass_residual'])
        numerical_integral = quad(lambda x: (1 - x) / (4 * p.lam7 * p.d ** 2), 0, 1, epsabs=1e-13)[0]
        expected_z = 2 * p.portal ** 2 * p.d ** 2 * numerical_integral / (16 * np.pi ** 2)
        th = threshold(p)
        check(label + '-scalar-kinetic-quadrature', abs(expected_z - th['kinetic']['scalar']) < 1e-14)
        rows.append(dict(label=label, parameters=asdict(p), threshold=th, RG=rg, component_errors=errors))
    result['examples'] = rows
    result['formulas'] = dict(jet='x(h)=M2+a*h^2+b*h^4',
        mass='sum n M2 a [log(M2/mu^2)-c+1/2]/(16pi^2)',
        potential_quartic='sum n {2 M2 b [log(M2/mu^2)-c+1/2]+a^2[log(M2/mu^2)-c+3/2]}/(16pi^2)',
        canonical='lambda_EFT=lambda_tree+delta_lambda_potential-2 lambda_tree delta_Z',
        Z_scalar='k^2/(64pi^2 lambda7)',
        Z_vector='{gR^2/2 [3log(MWR2/mu^2)-5/2]+gR^4/(2T)[3log(MZR2/mu^2)-5/2]}/(16pi^2)',
        Z_fermion='sum y_i^2 [1/2-log(MNi2/mu^2)]/(16pi^2)')
    result['checks'] = checks
    result['checks_passed'] = sum(c['passed'] for c in checks)
    result['checks_total'] = len(checks)
    result['scope'] = ('Stable full-basis Delta branch, norm portal, one real selected light doublet, diagonal real flavor. '
        'Dimension-four mass/quartic and finite light kinetic matching in Landau gauge/MS-bar, at zero tree light mass. '
        'No observed mass prediction, arbitrary-boundary/flavor extension or full dimension-six matching.')
    (OUT / 'matching.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=result['checks_passed'], checks_total=len(checks))), flush=True)
    assert all(c['passed'] for c in checks), 'Failed checks retained in matching.json'


if __name__ == '__main__':
    main()
