#!/usr/bin/env python3
"""Full-metric scalar spectrum and exact neutral-slice/source audit."""
import datetime
import hashlib
import json
import math
from pathlib import Path
import shutil

import numpy as np
import sympy as s

from canonical_scalar_action import (ROOT, OUT, SNAP, LABELS, load_exact_basis,
    independent_projector, scalar_pack, scalar_unpack, basis_derivatives, physical_spectrum)


def bracket_and_normalization():
    f = s.diag(s.Rational(1, 3), s.Rational(1, 3), s.Rational(1, 3), -1)
    g = s.zeros(4)
    for i in range(3):
        g[i, 3], g[3, i] = 1 / s.sqrt(3), -1 / s.sqrt(3)
    comm = lambda a, b: a * b - b * a
    norm2 = lambda a: s.simplify(s.trace(a.T * a))
    l2 = comm(f, g)
    l3a, l3s = comm(l2, f), comm(l2, g)
    projection = s.simplify(s.trace(l3s.T * f) ** 2 / (norm2(l3s) * norm2(f)))
    z, c4, scale = s.symbols('Z c4 scale', positive=True)
    lam = 4 * c4 / z ** 2
    changed = lam.subs({z: scale ** 2 * z, c4: scale ** 4 * c4}, simultaneous=True)
    t15 = s.diag(1, 1, 1, -3) / (2 * s.sqrt(6))
    e44 = s.zeros(4)
    e44[3, 3] = 1
    correct = -t15.T * e44 - e44 * t15
    legacy = comm(t15, e44)
    return dict(checks={
        'bracket_is_symmetric_not_original_antisymmetric_generator': l2 == l2.T and l2 != s.Rational(4, 3) * g,
        'third_order_symmetric_piece_nonzero': norm2(l3s) == s.Rational(128, 9),
        'projection_two_thirds_exact': projection == s.Rational(2, 3),
        'projected_norm_256_over_27': projection * norm2(l3s) == s.Rational(256, 27),
        'canonical_quartic_invariant_under_consistent_coordinate_change': s.simplify(changed - lam) == 0,
        'adjoint_commutator_drops_real_Delta_charge': legacy == s.zeros(4) and correct == s.sqrt(s.Rational(3, 2)) * e44},
        norms=dict(f=str(norm2(f)), g=str(norm2(g)), second=str(norm2(l2)), third_antisymmetric=str(norm2(l3a)), third_symmetric=str(norm2(l3s))),
        projection=str(projection), canonical_radial_convention='Lkin=Z/2 (dr)^2, V=c2 r^2+c4 r^4; phi=sqrt(Z)r; lambda_canonical=4 c4/Z^2',
        boundary='This fixes the algebra and the field-redefinition law, not the missing dynamical source-to-canonical kinetic coefficient Z or the complete action.')


def exact_neutral_restriction(polys, quadratics):
    a, u, w, d = s.symbols('a u w d', real=True)
    mapping = {0: a, 6: u, 7: w, 26: d / s.sqrt(2), 47: -d / s.sqrt(2)}
    expressions = []
    for i, poly in enumerate(polys + quadratics):
        value = sum((s.Rational(c, 18 if i < 17 else 1) * s.prod(mapping[j] for j in monomial)
                     for monomial, c in poly.items() if all(j in mapping for j in monomial)), s.S.Zero)
        expressions.append(s.expand(value))
    n, re, im, nd = a * a + u * u + w * w, a * u, a * w, d * d
    expected = [n*n, a*a*(u*u+w*w), a*a*(u*u-w*w), 2*a*a*u*w, n*re, n*im,
                0, d**4, 0, 0, 0, 0, 0, n*nd, re*nd, im*nd, -(a*a-u*u-w*w)*nd/2,
                n, re, im, nd]
    coefficients = s.symbols('l0:17') + s.symbols('m0:4')
    potential = s.expand(sum(c * v for c, v in zip(coefficients, expressions)))
    # u=b cos(alpha), w=b sin(alpha), so at alpha=0 derivative=b d/dw.
    phase = s.factor(u * s.diff(potential, w).subs(w, 0))
    phase_expected = a * u * (coefficients[19] + 2 * coefficients[3] * a * u
                            + coefficients[5] * (a*a+u*u) + coefficients[15] * d*d)
    monomials = sorted(set(m for e in expressions[:17] for m, c in s.Poly(e, a, u, w, d).terms() if c))
    matrix = s.Matrix([[s.Poly(e, a, u, w, d).coeff_monomial(m) for e in expressions[:17]] for m in monomials])
    invisible = [i for i, value in enumerate(expressions[:17]) if value == 0]
    # Direct full-polynomial transverse Hessian response, independent of
    # the restricted polynomial. Retain exact values at the registered VEV.
    vacuum = {0: s.Rational(1, 3), 6: s.Rational(1, 5), 26: 1 / s.sqrt(2), 47: -1 / s.sqrt(2)}
    responses = {}
    for k in invisible:
        entries = {}
        for monomial, coefficient in polys[k].items():
            for i in range(4):
                for j in range(4):
                    if i == j:
                        continue
                    rest = [monomial[t] for t in range(4) if t not in (i, j)]
                    if not all(t in vacuum for t in rest):
                        continue
                    pair = (monomial[i], monomial[j])
                    value = s.Rational(coefficient, 18) * s.prod(vacuum[t] for t in rest)
                    entries[pair] = entries.get(pair, 0) + value
        entries = {pair: s.simplify(v) for pair, v in entries.items() if s.simplify(v) != 0}
        responses[LABELS[k]] = dict(nonzero_hessian_entries=len(entries), examples=[dict(indices=list(pair), raw_hessian=str(v)) for pair, v in sorted(entries.items())[:4]])
    return dict(checks={
        'all_21_restrictions_match_independent_formula': all(s.expand(x-y) == 0 for x,y in zip(expressions, expected)),
        'neutral_quartic_map_rank_11': matrix.rank() == 11,
        'six_coordinate_invariants_invisible': invisible == [6, 8, 9, 10, 11, 12],
        'phase_tadpole_includes_CP_odd_coefficients': s.expand(phase - phase_expected) == 0,
        'four_invisible_norms_change_transverse_hessian': all(responses[LABELS[k]]['nonzero_hessian_entries'] > 0 for k in [6, 8, 9, 10]),
        'holomorphic_terms_invisible_through_Hessian': all(responses[LABELS[k]]['nonzero_hessian_entries'] == 0 for k in [11, 12])},
        variables=['a', 'u=b cos(alpha)', 'w=b sin(alpha)', 'd'], labels=LABELS + ['Nphi', 'Re detPhi', 'Im detPhi', 'NDelta'],
        restrictions=[str(e) for e in expressions], neutral_potential=str(potential),
        phase_tadpole_at_alpha_zero=str(phase), invisible_indices=invisible,
        transverse_hessian_responses=responses,
        neutral_metric='Before quotienting gauge phases: G_(a,b,d,alpha)=diag(2,2,2,2b^2). Full scalar masses use all 68 coordinates and the gauge-orbit projection.')


def verify_derivatives(polys, quadratics, coefficients, x, metric, label):
    rng = np.random.default_rng(20260924)
    direction = rng.normal(size=68)
    direction /= np.linalg.norm(direction)
    eps = 1e-4
    vals, grads, hs = basis_derivatives(polys, quadratics, x)
    vp, gp, _ = basis_derivatives(polys, quadratics, x + eps * direction)
    vm, gm, _ = basis_derivatives(polys, quadratics, x - eps * direction)
    grad, hess = coefficients @ grads, np.einsum('i,ijk->jk', coefficients, hs)
    gradient_error = abs(float(coefficients @ (vp-vm)) / (2*eps) - float(grad @ direction)) / max(1., abs(float(grad @ direction)))
    hessian_error = float(np.linalg.norm(coefficients @ (gp-gm) / (2*eps) - hess @ direction) / max(1., np.linalg.norm(hess @ direction)))
    return dict(label=label, gradient_error=gradient_error, hessian_error=hessian_error, passed=max(gradient_error, hessian_error) < 1e-5)


def run_canonical_audit():
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    attempt = OUT / 'attempts' / stamp
    attempt.mkdir(parents=True)
    paths = [Path(__file__).resolve(), ROOT/'code/condensate_energy/canonical_scalar_action.py',
             OUT/'protocol.md', SNAP/'full_scalar_basis.py', SNAP/'scalar_invariant_basis.py',
             ROOT/'code/condensate_energy/gauge_carrier_contract.py',
             ROOT/'code/acs_codebase/extras/phase50_vacuum.py',
             ROOT/'code/acs_codebase/extras/task2_lagrangian.py',
             ROOT/'code/acs_codebase/extras/higgs_derivation.py',
             ROOT/'papers/core_trilogy/Palatini_Gauge_Attractor.tex']
    for path in paths[:3]:
        shutil.copy2(path, attempt/path.name)
    results = dict(attempt=stamp, source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}, cases={}, checks=[])
    polys, quadratics, metric = load_exact_basis()
    print('Built full sparse basis', [len(p) for p in polys], flush=True)
    results['kinetic_metric'] = metric.tolist()
    results['monomial_counts'] = [len(p) for p in polys]
    results['normalization'] = bracket_and_normalization()
    results['neutral'] = exact_neutral_restriction(polys, quadratics)
    for key in ['normalization', 'neutral']:
        results['checks'].extend(dict(name=name, passed=bool(passed)) for name,passed in results[key]['checks'].items())
    evaluator = independent_projector()
    rng = np.random.default_rng(20260924)
    projector_errors, kinetic_errors = [], []
    for _ in range(8):
        x = rng.normal(size=68)
        vals, _, _ = basis_derivatives(polys, quadratics, x)
        phi, delta = scalar_unpack(x)
        expected, masses, hol = evaluator(phi, delta)
        projector_errors.append(float(max(abs(vals[:17]-expected)) / max(1., max(abs(expected)))))
        measured = 2*(np.vdot(phi,phi).real+np.vdot(delta,delta).real)
        kinetic_errors.append(float(abs(x@(metric*x)-measured)/measured))
    results['projector_relative_errors'] = projector_errors
    results['kinetic_relative_errors'] = kinetic_errors
    results['checks'].extend([dict(name='independent-projector-generic-fields', passed=max(projector_errors)<1e-10),
                              dict(name='kinetic-metric-from-trace', passed=max(kinetic_errors)<1e-12)])
    vacuum = np.zeros(68)
    vacuum[0], vacuum[6], vacuum[26], vacuum[47] = 1/3, 1/5, 1/math.sqrt(2), -1/math.sqrt(2)
    vals, grads, hs = basis_derivatives(polys, quadratics, vacuum)
    specs = [('angular-positive', .2, 0., 0.), ('angular-zero', 0., 0., 0.),
             ('angular-negative', -.2, 0., 0.), ('phase-tadpole', .2, .03, 0.),
             ('phase-balanced', .2, .03, -.03)]
    neutral_matrices = []
    for name, extra, phase_quartic, phase_mass in specs:
        coeff = np.zeros(21)
        coeff[0], coeff[1], coeff[6:11] = 1., 1., 1.
        coeff[[6, 8, 9, 10]] += extra
        coeff[11], coeff[12], coeff[13], coeff[15], coeff[16] = .01, .02, .1, phase_quartic, .02
        coeff[19] = phase_mass
        indices = [0, 6, 26]
        unknown = [17, 18, 20]
        coeff[unknown] = np.linalg.solve(grads[unknown][:, indices].T, -(coeff @ grads)[indices])
        gradient = coeff @ grads
        hessian = np.einsum('i,ijk->jk', coeff, hs)
        row = physical_spectrum(hessian, gradient, vacuum, metric)
        row.update(quartic_coefficients=coeff[:17].tolist(), quadratic_coefficients=coeff[17:].tolist(),
                   potential=float(coeff @ vals), phase_derivative=float(vacuum[6]*gradient[7]),
                   full_gradient=gradient.tolist(), name=name, angular_extra=extra)
        results['cases'][name] = row
        print(name, 'tadpole',row['tadpole_infinity_norm'],'physical +/-/0',row['positive'],row['negative'],row['zero'],'min',row['minimum_mass_squared'],flush=True)
        if name.startswith('angular-'):
            neutral_matrices.append(hessian[np.ix_([0,6,7,26,47],[0,6,7,26,47])])
        (attempt/'results.json').write_text(json.dumps(results)+'\n')
    results['neutral_hessian_deformation_max_difference'] = max(float(np.max(abs(m-neutral_matrices[0]))) for m in neutral_matrices)
    results['derivative_checks'] = [verify_derivatives(polys,quadratics,coeff,x,metric,label)
        for x,label in [(rng.normal(scale=.3,size=68),'generic'),(vacuum,'vacuum')]]
    stationary = [r for name,r in results['cases'].items() if name!='phase-tadpole']
    results['checks'].extend([
        dict(name='all-stationary-witness-full-tadpoles',passed=max(r['tadpole_infinity_norm'] for r in stationary)<1e-9),
        dict(name='gauge-Goldstone-Ward-identity',passed=max(r['goldstone_ward_relative'] for r in stationary)<1e-9),
        dict(name='correct-12-Goldstones-and-56-physical-directions',passed=all(r['gauge_orbit_rank']==12 and r['physical_real_modes']==56 for r in stationary)),
        dict(name='canonical-spectrum-coordinate-invariance',passed=max(r['coordinate_rescaling_spectrum_error'] for r in stationary)<1e-9),
        dict(name='electromagnetic-charge-commutes-with-masses',passed=max(r['mass_charge_commutator_relative'] for r in stationary)<1e-9),
        dict(name='electromagnetic-vacuum-invariance',passed=max(r['em_vacuum_invariance'] for r in stationary)<1e-12),
        dict(name='neutral-hessian-unchanged-by-hidden-coefficients',passed=results['neutral_hessian_deformation_max_difference']<1e-12),
        dict(name='generic-and-vacuum-finite-difference-derivatives',passed=all(r['passed'] for r in results['derivative_checks'])),
        dict(name='real-VEV-phase-tadpole-detected',passed=results['cases']['phase-tadpole']['tadpole_infinity_norm']>1e-4),
        dict(name='phase-tadpole-cancelled-only-with-explicit-mass-coefficient',passed=results['cases']['phase-balanced']['tadpole_infinity_norm']<1e-9)])
    # Record the tested outcome, rather than making positive spectrum a gate
    # which could hide a real instability of the chosen witness action.
    results['witness_outcome'] = dict(positive_case_has_no_negative_or_flat_modes=results['cases']['angular-positive']['positive']==56,
                                    negative_case_has_tachyons=results['cases']['angular-negative']['negative']>0)
    results['all_checks_passed'] = all(row['passed'] for row in results['checks'])
    (attempt/'results.json').write_text(json.dumps(results)+'\n')
    (OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(dict(checks=results['checks'],outcome=results['witness_outcome']),indent=2),flush=True)


if __name__=='__main__':
    run_canonical_audit()
