#!/usr/bin/env python3
"""Tree-level radial matching and source-normalization identifiability."""
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
import sympy as s

from canonical_scalar_action import ROOT, load_exact_basis, basis_derivatives, independent_projector
from hidden_coupling_audit import archived

OUT = ROOT / 'docs/condensate_energy/action_matching'


def restrict_to_phi_and_radial(poly, fields, amplitude):
    values = {i: f for i, f in enumerate(fields)}
    values.update({26: amplitude, 47: -amplitude})
    return s.expand(sum(s.Rational(c, 18) * s.prod(values[i] for i in m)
                        for m, c in poly.items() if all(i in values for i in m)))


def main():
    checks = []

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL', flush=True)

    polys, quadratics, metric = load_exact_basis()
    fields = s.symbols('x0:8', real=True)
    amplitude = s.Symbol('t', real=True)
    phi = s.Matrix(2, 2, [fields[2 * i] + s.I * fields[2 * i + 1] for i in range(4)])
    norm = s.expand(s.trace(phi.conjugate().T * phi))
    determinant = s.expand(phi.det())
    realdet, imagdet = s.re(determinant), s.im(determinant)
    current = s.expand(s.trace(phi.conjugate().T * phi * s.diag(1, -1)) / 2)
    Y = 2 * amplitude ** 2
    expected = [norm ** 2, realdet ** 2 + imagdet ** 2, realdet ** 2 - imagdet ** 2,
                2 * realdet * imagdet, norm * realdet, norm * imagdet,
                0, Y ** 2, 0, 0, 0, 0, 0, norm * Y, realdet * Y, imagdet * Y, -current * Y]
    for i in range(17):
        direct = restrict_to_phi_and_radial(polys[i], fields, amplitude)
        check(f'exact-radial-restriction-{i}', s.expand(direct - expected[i]) == 0)

    lam = s.symbols('l0:17', real=True)
    m0, m1, m2, md, y, K, vphi = s.symbols('m0 m1 m2 mDelta y K Vphi', real=True)
    radial_potential = vphi + md * y + lam[7] * y ** 2 + K * y
    stationary_y = -(md + K) / (2 * lam[7])
    effective = vphi - (md + K) ** 2 / (4 * lam[7])
    check('radial-stationary-equation', s.simplify(s.diff(radial_potential, y).subs(y, stationary_y)) == 0)
    check('exact-tree-potential-matching', s.simplify(radial_potential.subs(y, stationary_y) - effective) == 0)
    d, h = s.symbols('d h', positive=True)
    shifted = s.expand(radial_potential.subs({md: -2 * lam[7] * d ** 2, y: (d + h / s.sqrt(2)) ** 2}))
    heavy_mass2 = s.diff(shifted, h, 2).subs({h: 0, K: 0})
    heavy_source = s.diff(shifted, h).subs(h, 0)
    exchange = s.simplify(-heavy_source ** 2 / (2 * heavy_mass2))
    check('canonical-heavy-radial-mass', heavy_mass2 == 4 * lam[7] * d ** 2)
    check('zero-momentum-exchange-matches-quartic-shift', s.simplify(exchange + K ** 2 / (4 * lam[7])) == 0)

    # General Phi quadratic masses after the first breaking. Convert the first
    # column into a same-hypercharge doublet so that H1^dagger H2=det(Phi).
    A = m0 + d ** 2 * (lam[13] - lam[16] / 2)
    B = m0 + d ** 2 * (lam[13] + lam[16] / 2)
    C = (m1 + d ** 2 * lam[14] - s.I * (m2 + d ** 2 * lam[15])) / 2
    doublet_matrix = s.Matrix([[A, C], [s.conjugate(C), B]])
    radius2 = d ** 4 * lam[16] ** 2 + (m1 + d ** 2 * lam[14]) ** 2 + (m2 + d ** 2 * lam[15]) ** 2
    center = m0 + d ** 2 * lam[13]
    z = s.Symbol('z')
    check('doublet-mass-characteristic-polynomial', s.expand((doublet_matrix - z * s.eye(2)).det() - ((center - z) ** 2 - radius2 / 4)) == 0)
    numerical_lam = np.zeros(17)
    numerical_lam[7], numerical_lam[13:17] = 1., [.1, .02, .03, .06]
    numerical_m = np.array([.2, .03, .04, -8.])
    vacuum = np.zeros(68)
    vacuum[26], vacuum[47] = np.sqrt(2), -np.sqrt(2)
    values, gradients, hessians = basis_derivatives(polys, quadratics, vacuum)
    hphi = np.einsum('i,ijk->jk', np.r_[numerical_lam, numerical_m], hessians)[:8, :8] / 2
    subs = {m0: .2, m1: .03, m2: .04, d: 2, **{l: numerical_lam[i] for i, l in enumerate(lam)}}
    doublet_eigenvalues = np.linalg.eigvalsh(np.array(doublet_matrix.subs(subs), complex))
    check('independent-eight-real-Phi-masses', max(abs(np.linalg.eigvalsh(hphi) - np.repeat(doublet_eigenvalues, 4))) < 1e-12)

    # Verify the general single-doublet projection without choosing beta or phase.
    c, b, aR, aI, r = s.symbols('c b aR aI r', real=True)
    substitutions = dict(zip(fields, [c * r / s.sqrt(2), 0, 0, 0, 0, 0, b * aR * r / s.sqrt(2), b * aI * r / s.sqrt(2)]))
    high = sum(lam[i] * expected[i] for i in range(6))
    kphi = lam[13] * norm + lam[14] * realdet + lam[15] * imagdet - lam[16] * current
    projected_high = s.expand(4 * high.subs(substitutions) / r ** 4)
    projected_k = s.expand(2 * kphi.subs(substitutions) / r ** 2)
    high_formula = lam[0] + c ** 2 * b ** 2 * (lam[1] + lam[2] * (aR ** 2 - aI ** 2) + 2 * lam[3] * aR * aI)
    high_formula += c * b * (lam[4] * aR + lam[5] * aI)
    k_formula = lam[13] + c * b * (lam[14] * aR + lam[15] * aI) - lam[16] * (c ** 2 - b ** 2) / 2
    constraints = s.groebner([aR ** 2 + aI ** 2 - 1, c ** 2 + b ** 2 - 1], aI, b, aR, c,
                             domain=s.QQ.frac_field(*lam))
    check('general-light-direction-quartic', constraints.reduce(s.expand(projected_high - high_formula))[1] == 0)
    check('general-light-direction-portal', constraints.reduce(s.expand(projected_k - k_formula))[1] == 0)

    light, vev, lamH, portal, muH = s.symbols('light vev lambdaH portal muH', real=True)
    twofield = muH * light ** 2 / 2 + lamH * light ** 4 / 4 + md * y + lam[7] * y ** 2 + portal * light ** 2 * y / 2
    canonical = twofield.subs(y, (d + h / s.sqrt(2)) ** 2)
    conditions = {light: vev, h: 0, muH: -lamH * vev ** 2 - portal * d ** 2,
                  md: -2 * lam[7] * d ** 2 - portal * vev ** 2 / 2}
    hess = s.hessian(canonical, [light, h]).subs(conditions)
    schur = s.factor(hess[0, 0] - hess[0, 1] ** 2 / hess[1, 1])
    check('Schur-complement-agrees-with-tree-matching', s.simplify(schur - 2 * vev ** 2 * (lamH - portal ** 2 / (4 * lam[7]))) == 0)

    # Independent numerical minimization of the full invariant projector.
    projector = independent_projector()
    rng = np.random.default_rng(20260925)
    samples = []
    for j in range(5):
        P = (rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))) / 7
        lambdas = np.zeros(17)
        lambdas[:6] = [.2, .1, .02, .03, -.01, .04]
        lambdas[6:11] = [1.2, 1., 1.2, 1.2, 1.2]
        lambdas[13:] = [.1, .02, -.03, .04]
        mDelta = -18.
        npnorm = float(np.vdot(P, P).real)
        det = np.linalg.det(P)
        j3 = float(np.trace(P.conj().T @ P @ np.diag([1, -1])).real / 2)
        kval = .1 * npnorm + .02 * det.real - .03 * det.imag - .04 * j3
        predicted_y = -(mDelta + kval) / 2
        def direct(dval):
            D = np.zeros((3, 4, 4), complex)
            D[0, 3, 3], D[1, 3, 3] = dval / np.sqrt(2), -1j * dval / np.sqrt(2)
            invariants = projector(P, D)[0]
            return float(lambdas @ invariants + mDelta * dval ** 2)
        optimized = minimize_scalar(direct, bounds=(0., 6.), method='bounded', options={'xatol': 1e-12})
        vphi_numeric = direct(0)
        matched_value = vphi_numeric - (mDelta + kval) ** 2 / 4
        samples.append(dict(success=bool(optimized.success), displacement_error=abs(optimized.x ** 2 - predicted_y),
                            energy_error=abs(optimized.fun - matched_value)))
    check('independent-radial-minimization', all(r['success'] and r['displacement_error'] < 2e-6 and r['energy_error'] < 1e-9 for r in samples), samples)

    # Algebraic normalization is not an action normalization.
    projected = s.Rational(256, 27)
    killing = s.Rational(32, 3)
    target = 2 * s.sqrt(3) / 27
    Z, c4, scale, common = s.symbols('Z c4 scale common', positive=True)
    canonical_quartic = 4 * c4 / Z ** 2
    check('canonical-quartic-coordinate-invariance', s.simplify(canonical_quartic.subs({c4: c4 / scale ** 4, Z: Z / scale ** 2}, simultaneous=True) - canonical_quartic) == 0)
    natural_example = s.simplify(canonical_quartic.subs({c4: projected, Z: killing}))
    common_example = s.simplify(canonical_quartic.subs({c4: common * projected, Z: common * killing}))
    check('Killing-kinetic-candidate-does-not-give-claimed-quartic', natural_example == s.Rational(1, 3) and s.simplify(natural_example - target) != 0)
    check('overall-action-coefficient-changes-physical-quartic', common_example == 1 / (3 * common))
    required_Z_squared = s.simplify(4 * projected / target)
    check('target-requires-additional-kinetic-choice', s.simplify(required_Z_squared - 512 / s.sqrt(3)) == 0)
    # A squared information functional always leaves the origin at zero energy.
    aa, bb, cc, p = s.symbols('aa bb cc p', real=True)
    squared_information = (aa * p ** 2 - bb * p ** 4 + cc * p ** 6) ** 2
    check('squared-information-origin-degenerate-minimum', squared_information.subs(p, 0) == 0 and s.diff(squared_information, p, 2).subs(p, 0) == 0 and s.degree(squared_information, p) == 12)
    check('no-direct-SU4-gauge-source-for-Phi-quartics', all(s.Rational(row[j]) == 0 for row in archived.G['gauge_quartic_coefficients'][:6] for j in [0, 1, 2]))
    g4, gR = s.symbols('g4 gR', real=True)
    gauge_cw_log = s.expand(3 * (6 * g4 ** 4 + 2 * gR ** 4 + (3 * g4 ** 2 + 2 * gR ** 2) ** 2))
    check('neutral-gauge-CW-log-agrees-with-beta-lambda7', gauge_cw_log == 45 * g4 ** 4 + 36 * g4 ** 2 * gR ** 2 + 18 * gR ** 4)

    spectrum = json.loads((OUT / 'spectrum.json').read_text())
    for name, coefficient in [('color_gram', -1), ('spin_gram', -2)]:
        mode = next(row for row in spectrum['historical_trace_models'][name]['sectors'] if row['color'] == 'bar3' and row['hypercharge'] == '1/3')
        rr = s.Symbol('rho2')
        check(f'{name}-entire-positive-rho2-range-unstable', s.sympify(mode['mass_squared_over_d2']) == coefficient * rr,
              'At 0<rho1<8/9 and rho2=16/9-2rho1, rho2>0, so this mass is strictly negative.')

    output = dict(checks=checks, checks_passed=sum(c['passed'] for c in checks), checks_total=len(checks),
        matching=dict(K='l13 Nphi + l14 Re(detPhi) + l15 Im(detPhi) - l16 Jphi3',
            heavy_solution=str(stationary_y), V_eff=str(effective), heavy_mass_squared=str(heavy_mass2),
            quartic_shift='-K(Phi)^2/(4 lambda7)',
            branch='lambda7>0 and -(mDelta+K)/(2lambda7)>0; heavy physical modes must also be stable and gapped.',
            outside_branch='The constrained radial minimum is y=0 when the formal solution is nonpositive.',
            light_direction=dict(constraints='c^2+b^2=1, aR^2+aI^2=1; c=cos beta, b=sin beta, aR+i aI=exp(i alpha)',
                  high_quartic=str(high_formula), portal=str(k_formula), low_quartic=str(high_formula - k_formula ** 2 / (4 * lam[7]))),
            doublet_mass_matrix=[[str(v) for v in row] for row in doublet_matrix.tolist()],
            doublet_masses_squared='m0+l13*d^2 +/- sqrt(l16^2*d^4+(m1+l14*d^2)^2+(m2+l15*d^2)^2)/2',
            Schur_complement=str(schur), numerical_minimization=samples,
            limitations='Tree-level potential and zero-momentum exchange; not the full derivative EFT, finite one-loop matching or a pole mass.'),
        normalization=dict(projected_bracket_norm=str(projected), Killing_norm=str(killing),
            canonical_quartic=str(canonical_quartic), candidate_Killing_action_quartic=str(natural_example),
            common_prefactor_family=str(common_example), claimed_value=str(target), required_Z_squared=str(required_Z_squared),
            conclusion='Exact bracket projection does not select the scalar kinetic action or its physical quartic.'),
        source_routes=dict(squared_information='Leaves the origin as a global zero alongside any other zeros; does not uniquely select a nonzero VEV.',
            direct_color_gauge_loop='Phi is an SU4 singlet; a direct SU4-only one-loop Phi quartic source is zero in the full unbroken theory.',
            Delta_gauge_log_coefficient=str(gauge_cw_log),
            CW_limit='The logarithmic coefficient is calculable; a finite quartic and vacuum still require renormalization conditions.'))
    (OUT / 'tree-matching.json').write_text(json.dumps(output, indent=2) + '\n')
    assert all(c['passed'] for c in checks), 'Failures retained in tree-matching.json'


if __name__ == '__main__':
    main()
