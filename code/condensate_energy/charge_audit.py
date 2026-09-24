#!/usr/bin/env python3
"""Audit continuous scalar charges against the recorded ACS field content.

This adds evidence only: no inherited action, coefficient, or receipt is edited.
"""
import ast
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import sympy as s
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy/charge_audit'
FIELDS = ['Phi', 'Delta', 'psi_L', 'psi_R_physical']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def archive_inputs():
    path = ROOT / 'docs/frontier/2026-09-11/ACS_Frontier_Evidence.zip'
    data = path.read_bytes()
    provenance = [{'path': str(path.relative_to(ROOT)), 'sha256': sha(data)}]
    archive = ZipFile(io.BytesIO(data))
    for _ in range(2):
        member = next(n for n in archive.namelist() if n.endswith('/Prior_Evidence.zip'))
        data = archive.read(member)
        provenance.append({'member': member, 'sha256': sha(data)})
        archive = ZipFile(io.BytesIO(data))
    snapshots = OUT / 'source-snapshots'
    snapshots.mkdir(parents=True, exist_ok=True)
    for suffix in ['/support/scalar_invariant_basis.py', '/checks/full_scalar_basis.py']:
        member = next(n for n in archive.namelist() if n.endswith(suffix))
        data = archive.read(member)
        target = snapshots / Path(member).name
        target.write_bytes(data)
        provenance.append({'member': member, 'sha256': sha(data),
                           'snapshot': str(target.relative_to(ROOT))})
    (OUT / 'archive-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    source = snapshots / 'scalar_invariant_basis.py'
    tree = ast.parse(source.read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'invariants')
    pauli = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]),
             np.diag([1, -1]).astype(complex)]
    env = dict(np=np, itertools=itertools, math=math,
               perms=list(itertools.permutations(range(4))), pauli=pauli)
    # Execute only the inspected evaluator, not the archive's top-level programs.
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), 'exec'), env)
    return env['invariants'], pauli, provenance


def nullspace(rows, columns=4):
    matrix = s.Matrix(rows) if rows else s.zeros(0, columns)
    return dict(rank=matrix.rank(), dimension=len(matrix.nullspace()),
                basis=[[str(x) for x in v] for v in matrix.nullspace()],
                constraints=[[int(x) for x in row] for row in rows])


def family_rows(include_hol):
    rows = []
    # Phi, Delta, L1,L2,L3, R1,R2,R3; every indicated Yukawa entry nonzero.
    for i, j in itertools.product(range(3), repeat=2):
        for sign in [1, -1]:
            row = [0] * 8
            row[0], row[2 + i], row[5 + j] = sign, -1, 1
            rows.append(row)
    for i in range(3):
        for j in range(i, 3):
            row = [0] * 8
            row[1] = 1
            row[5 + i] += 1
            row[5 + j] += 1
            rows.append(row)
    if include_hol:
        rows.append([0, 4, 0, 0, 0, 0, 0, 0])
    return rows


def flavor_generator_check(Y, Z, F, include_hol):
    """Exact equations for both arbitrary Hermitian 3x3 flavor generators."""
    basis = []
    for i in range(3):
        m = s.zeros(3)
        m[i, i] = 1
        basis.append(m)
    for i, j in itertools.combinations(range(3), 2):
        m = s.zeros(3)
        m[i, j] = m[j, i] = 1
        basis.append(m)
        m = s.zeros(3)
        m[i, j], m[j, i] = s.I, -s.I
        basis.append(m)
    variables = s.symbols('p d l0:9 r0:9', real=True)
    p, d = variables[:2]
    left = sum((v * b for v, b in zip(variables[2:11], basis)), s.zeros(3))
    right = sum((v * b for v, b in zip(variables[11:], basis)), s.zeros(3))
    equations = list(-left * Y + Y * right + p * Y)
    equations += list(-left * Z + Z * right - p * Z)
    equations += list(right.T * F + F * right + d * F)
    if include_hol:
        equations.append(4 * d)
    real_equations = [s.expand(part(e)) for e in equations for part in [s.re, s.im]]
    matrix, _ = s.linear_eq_to_matrix(real_equations, variables)
    candidate = s.Matrix([0, -2] + [1, 1, 1, 0, 0, 0, 0, 0, 0] * 2)
    return dict(rank=matrix.rank(), dimension=len(matrix.nullspace()),
                normalized_X_is_symmetry=matrix * candidate == s.zeros(matrix.rows, 1),
                determinants=[str(m.det()) for m in [Y, Z, F]],
                scalar_projections=[[str(v[0]), str(v[1])] for v in matrix.nullspace()])


def polar_hol(delta):
    result = sum(np.linalg.det(m) for m in delta)
    for a, b in itertools.combinations(range(3), 2):
        result += (np.linalg.det(delta[a] + delta[b]) + np.linalg.det(delta[a] - delta[b])) / 2
    return result


def wick_hol(delta):
    nodes, weights = [-math.sqrt(3), 0, math.sqrt(3)], [1 / 6, 2 / 3, 1 / 6]
    result = 0j
    for inds in itertools.product(range(3), repeat=3):
        matrix = sum(nodes[inds[a]] * delta[a] for a in range(3))
        result += math.prod(weights[i] for i in inds) * np.linalg.det(matrix)
    return result


def invariant_tests(evaluator, pauli):
    rng = np.random.default_rng(20260924)

    def special_unitary(n):
        q = np.linalg.qr(rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)))[0]
        return q * np.exp(-1j * np.angle(np.linalg.det(q)) / n)

    errors = dict(gauge=0., phase=0., wick=0.)
    for _ in range(24):
        phi = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
        delta = rng.normal(size=(3, 4, 4)) + 1j * rng.normal(size=(3, 4, 4))
        delta = (delta + delta.transpose(0, 2, 1)) / 2
        values, quadratic, hol = evaluator(phi, delta)
        scale = max(1., np.max(abs(values)))
        errors['wick'] = max(errors['wick'], abs(wick_hol(delta) - hol) / scale,
                             abs(polar_hol(delta) - hol) / scale)
        for alpha, beta in [(0.271, -0.419), (0.79, 0.31), (-0.4, 0.9)]:
            new_values, new_quad, new_hol = evaluator(np.exp(1j * alpha) * phi,
                                                     np.exp(1j * beta) * delta)
            expected = values.copy()
            for i, j, angle in [(2, 3, 4 * alpha), (4, 5, 2 * alpha),
                                 (11, 12, 4 * beta), (14, 15, 2 * alpha)]:
                expected[i], expected[j] = np.cos(angle) * values[i] - np.sin(angle) * values[j], \
                                           np.sin(angle) * values[i] + np.cos(angle) * values[j]
            qexpected = quadratic.copy()
            qexpected[1], qexpected[2] = np.cos(2 * alpha) * quadratic[1] - np.sin(2 * alpha) * quadratic[2], \
                                        np.sin(2 * alpha) * quadratic[1] + np.cos(2 * alpha) * quadratic[2]
            errors['phase'] = max(errors['phase'], float(np.max(abs(new_values - expected)) / scale),
                                  float(np.max(abs(new_quad - qexpected)) / max(1., np.max(abs(quadratic)))),
                                  abs(new_hol - np.exp(4j * beta) * hol) / scale)
        ul, ur, uc = special_unitary(2), special_unitary(2), special_unitary(4)
        rotation = np.array([[np.trace(a @ ur @ b @ ur.conj().T).real / 2 for b in pauli] for a in pauli])
        transformed = np.einsum('ab,bij->aij', rotation,
                                np.array([uc.conj() @ m @ uc.conj().T for m in delta]))
        transformed_values, _, _ = evaluator(ul @ phi @ ur.conj().T, transformed)
        errors['gauge'] = max(errors['gauge'], float(np.max(abs(values - transformed_values)) / scale))
    return {k: float(v) for k, v in errors.items()}


def exact_hol_witnesses():
    a, b, c, v = s.symbols('a b c v', real=True)
    d = [s.diag(a, b, c, v), s.diag(0, 0, 0, s.I * v), s.zeros(4)]
    hol = sum(m.det() for m in d)
    for i, j in itertools.combinations(range(3), 2):
        hol += ((d[i] + d[j]).det() + (d[i] - d[j]).det()) / 2
    hol = s.expand(hol)
    vacuum = {a: 0, b: 0, c: 0}
    gradient = [s.diff(hol, x).subs(vacuum) for x in [a, b, c]]
    hessian = s.hessian(hol, [a, b, c]).subs(vacuum)
    theta, kr, ki, hr, hi = s.symbols('theta kappa_R kappa_I H_R H_I', real=True)
    product = (kr + s.I * ki) * (hr + s.I * hi)
    # X(Delta)=-2, so X(H)=-8; Qdot=-dV/dtheta for our Noether convention.
    potential = 2 * s.re(s.exp(-8 * s.I * theta) * product)
    source = s.simplify(-s.diff(potential, theta).subs(theta, 0))
    return dict(polynomial=str(hol), zero_through_quadratic=hol.subs(vacuum) == 0 and
                all(x == 0 for x in gradient) and hessian == s.zeros(3),
                third_mixed_derivative=str(s.diff(hol, a, b, c)),
                exact_nonzero_witness=hol.subs({a: 1, b: 1, c: 1, v: 1}) == 3,
                X_charge_source=str(source),
                source_identity=s.simplify(source + 16 * s.im(product)) == 0)


def discrete_quotient(rows):
    matrix = s.Matrix(rows)
    normal = smith_normal_form(matrix, domain=s.ZZ)
    # Orders divide 8, certified by Smith normal form, so this grid is exhaustive.
    orders = [abs(int(normal[i, i])) for i in range(4)]
    allowed = {v for v in itertools.product(range(8), repeat=4)
               if all(sum(a * b for a, b in zip(row, v)) % 8 == 0 for row in rows)}
    centers = set()
    for a, b, c in itertools.product(range(4), range(2), range(2)):
        centers.add(((4 * (b - c)) % 8, (-4 * a) % 8,
                     (2 * a + 4 * b) % 8, (2 * a + 4 * c) % 8))
    quantum = {v for v in allowed if 12 * v[2] % 8 == 0 and 12 * v[3] % 8 == 0}
    return dict(smith_diagonal=orders, classical_field_actions=len(allowed),
                gauge_center_field_actions=len(centers),
                classical_quotient_order=len(allowed) // len(centers),
                ordinary_instanton_survivors=len(quantum),
                survivors_equal_gauge_center=quantum == centers,
                centers_preserve_all_terms=centers <= allowed,
                scope='family-uniform field phases; ordinary instantons; not line operators or bundle classification')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, expected in json.loads((OUT.parent / 'self_binding/receipt.json').read_text())['artifact_sha256'].items():
        assert sha((ROOT / name).read_bytes()) == expected, name
    evaluate, pauli, provenance = archive_inputs()
    y, yt, maj, hol = [1, 0, -1, 1], [-1, 0, -1, 1], [0, 1, 0, 2], [0, 4, 0, 0]
    full = [y, yt, maj, hol]
    phases = dict(full=nullspace(full), no_holomorphic_Delta=nullspace(full[:-1]),
                  no_Majorana_or_holomorphic_Delta=nullspace([y, yt]),
                  full_three_family=nullspace(family_rows(True), 8),
                  no_holomorphic_three_family=nullspace(family_rows(False), 8))
    basis_terms = [
        ('Nphi^2', 0, 0), ('|detPhi|^2', 0, 0),
        ('Re[(detPhi)^2]', 4, 0), ('Im[(detPhi)^2]', 4, 0),
        ('Nphi Re(detPhi)', 2, 0), ('Nphi Im(detPhi)', 2, 0),
        ('norm(35,spin0)^2', 0, 0), ('norm(35,spin2)^2', 0, 0),
        ('norm(20prime,spin0)^2', 0, 0), ('norm(20prime,spin2)^2', 0, 0),
        ('norm(45,spin1)^2', 0, 0), ('Re H_Delta', 0, 4), ('Im H_Delta', 0, 4),
        ('Nphi NDelta', 0, 0), ('Re(detPhi) NDelta', 2, 0),
        ('Im(detPhi) NDelta', 2, 0), ('Jphi_R dot JDelta_R', 0, 0)]
    quartics = [dict(name=name, underlying_complex_weight=[p, d],
                     X_weight=-2 * d) for name, p, d in basis_terms]
    errors = invariant_tests(evaluate, pauli)
    witnesses = exact_hol_witnesses()
    Y = s.diag(1, 2, 3)
    F = s.Matrix([[2, s.Rational(1, 5), 0], [s.Rational(1, 5), 3, s.I / 7], [0, s.I / 7, 4]])
    Z = s.Matrix([[1, s.I / 3, 0], [s.Rational(1, 4), 3, 1], [0, 1, 2]])
    flavor = {}
    for label, conjugate in [('aligned_2_over_3', 2 * Y / 3), ('nonaligned_complex', Z)]:
        for include in [False, True]:
            flavor[f'{label}_hol_{include}'] = flavor_generator_check(Y, conjugate, F, include)
    # Universal trace conditions for arbitrary invertible Y,Ytilde,F, N_g=3.
    p, d, tL, tR = s.symbols('p d trace_TL trace_TR', real=True)
    trace_solution = s.solve([-tL + tR + 3 * p, -tL + tR - 3 * p, 2 * tR + 3 * d],
                             [p, tL, tR])
    anomaly_at_X = dict(SU4_squared_X=s.Rational(3) * (2 * s.Rational(1, 2) - 2 * s.Rational(1, 2)),
                        SU2L_squared_X=s.Rational(3) * 4 * s.Rational(1, 2),
                        SU2R_squared_X=-s.Rational(3) * 4 * s.Rational(1, 2),
                        gravity_squared_X=3 * (8 - 8), X_cubed=3 * (8 - 8))
    anomaly_trace = [s.simplify((2 * tL).subs(trace_solution)),
                     s.simplify((-2 * tR).subs(trace_solution))]
    finite = discrete_quotient(full)
    bl = [s.Rational(1, 3)] * 3 + [-s.Integer(1)]
    fermion_B = [s.simplify((1 + value) / 4) for value in bl]
    delta_B = {f'{i + 1}{j + 1}': s.simplify((-2 - bl[i] - bl[j]) / 4)
               for i in range(4) for j in range(i, 4)}
    checks = {
        'parent_self_binding_receipt_unchanged': True,
        'full_uniform_phase_constraints_rank_four': phases['full']['rank'] == 4,
        'minimal_obstruction_determinant_nonzero': abs(s.Matrix(full).det()) == 16,
        'classical_X_survives_only_without_holomorphic_Delta': phases['no_holomorphic_Delta']['basis'] == [['0', '-2', '1', '1']],
        'full_three_family_phase_constraints_rank_eight': phases['full_three_family']['rank'] == 8,
        'three_family_no_holomorphic_has_one_phase': phases['no_holomorphic_three_family']['dimension'] == 1,
        '17_quartics_and_nine_independent_phase_invariants': len(quartics) == 17 and sum(p == d == 0 for _, p, d in basis_terms) == 9,
        'exactly_two_real_quartics_break_classical_X': sum(q['X_weight'] != 0 for q in quartics) == 2,
        'full_basis_gauge_covariance': errors['gauge'] < 1e-10,
        'full_basis_phase_covariance': errors['phase'] < 1e-10,
        'independent_Wick_and_polarization_agree': errors['wick'] < 1e-10,
        'holomorphic_term_nonzero_exact_witness': witnesses['exact_nonzero_witness'],
        'vacuum_slice_hides_cubic_transverse_breaker': witnesses['zero_through_quadratic'] and witnesses['third_mixed_derivative'] == '3*v',
        'exact_Noether_source_for_holomorphic_breaking': witnesses['source_identity'],
        'arbitrary_flavor_generators_full_terms_leave_none': all(flavor[f'{k}_hol_True']['dimension'] == 0 for k in ['aligned_2_over_3', 'nonaligned_complex']),
        'arbitrary_flavor_generators_no_hol_leave_X': all(flavor[f'{k}_hol_False']['dimension'] == 1 and flavor[f'{k}_hol_False']['normalized_X_is_symmetry'] for k in ['aligned_2_over_3', 'nonaligned_complex']),
        'trace_conditions_force_zero_Phi_charge': trace_solution[p] == 0,
        'flavor_basis_independent_scalar_anomaly_obstruction': anomaly_trace == [-3 * d, 3 * d],
        'candidate_X_mixed_weak_anomalies_nonzero': anomaly_at_X['SU2L_squared_X'] == 6 and anomaly_at_X['SU2R_squared_X'] == -6,
        'candidate_X_SU4_gravity_cubic_cancel': all(anomaly_at_X[k] == 0 for k in ['SU4_squared_X', 'gravity_squared_X', 'X_cubed']),
        'ordinary_instanton_survivors_are_gauge_centers': finite['survivors_equal_gauge_center'] and finite['centers_preserve_all_terms'],
        'vacuum_preserving_combination_is_baryon_number_on_fermions': fermion_B == [s.Rational(1, 3)] * 3 + [0],
        'neutral_Delta_cannot_carry_this_unbroken_global_charge': delta_B['44'] == 0,
        'colored_Delta_components_do_carry_baryon_charge': delta_B['11'] == -s.Rational(2, 3) and delta_B['14'] == -s.Rational(1, 3),
    }
    result = dict(status='completed_scoped_charge_audit', fields=FIELDS,
                  convention='physical psi_R is (4,1,2), Delta is (bar10,1,3); anomalies use psi_R^c',
                  checks={k: bool(v) for k, v in checks.items()}, all_checks_passed=all(checks.values()),
                  phases=phases, quartic_weights=quartics,
                  quadratic_weights=[{'name': n, 'weight': w} for n, w in
                                     [('Nphi', [0, 0]), ('Re detPhi', [2, 0]), ('Im detPhi', [2, 0]), ('NDelta', [0, 0])]],
                  flavor=flavor, numerical_transform_errors=errors, exact_witnesses=witnesses,
                  universal_invertible_Yukawa_trace_solution={str(k): str(v) for k, v in trace_solution.items()},
                  candidate_X_anomalies={k: str(v) for k, v in anomaly_at_X.items()},
                  anomaly_normalization='sum over left-handed Weyl fermions X*T(rep)*spectator multiplicity, T(fund)=1/2',
                  instanton_delta_X={'SU2L_unit_charge': 12, 'SU2R_unit_charge': -12},
                  arbitrary_flavor_weak_anomalies=list(map(str, anomaly_trace)), discrete=finite,
                  broken_phase=dict(generator='B=(X+(B-L))/4', fermion_charges=list(map(str, fermion_B)),
                                    Delta_symmetric_color_components={k: str(v) for k, v in delta_B.items()},
                                    holomorphic_quartic_B_charge=-2),
                  outcome='No exact independent continuous scalar charge established for the stated complete minimal action; truncation candidate is anomalous and neutral-Delta identification fails.',
                  boundaries=['no assertion excluding other field content or explicitly justified coupling restrictions',
                              'no classification of nonlinear/topological/emergent symmetries',
                              'no soliton lifetime computed', 'no complete gauged soliton solved',
                              'charge-generator trace theorem assumes both Dirac matrices and Majorana matrix invertible'],
                  versions=dict(numpy=np.__version__, sympy=s.__version__))
    sources = [Path(__file__).resolve(), OUT / 'protocol.md', OUT / 'archive-provenance.json',
               ROOT / 'papers/core_trilogy/Palatini_Gauge_Attractor.tex',
               ROOT / 'code/acs_codebase/extras/task2_lagrangian.py',
               ROOT / 'docs/frontier/2026-09-11/Branch_Catalog.json',
               OUT.parent / 'self_binding/receipt.json']
    sources += sorted((OUT / 'source-snapshots').glob('*.py'))
    result['source_sha256'] = {str(path.relative_to(ROOT)): sha(path.read_bytes()) for path in sources}
    (OUT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(all_checks_passed=result['all_checks_passed'], checks=result['checks'],
                          phases=phases, flavor=flavor, errors=errors, discrete=finite,
                          anomalies=result['candidate_X_anomalies'], witness=witnesses), indent=2))
    if not result['all_checks_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
