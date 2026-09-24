#!/usr/bin/env python3
"""Independent closure tests for the neutral-invisible ACS scalar couplings."""
import ast
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import qr
import sympy as sp

from canonical_scalar_action import (ROOT, LABELS, load_exact_basis, basis_derivatives,
                                    scalar_gauge_action, scalar_unpack, independent_projector)

OUT = ROOT / 'docs/condensate_energy/hidden_couplings'
SNAP = OUT / 'source-snapshots'
sys.path.insert(0, str(SNAP))
import full_one_loop_rg as archived
from yukawa_model import mass, tensors


def clean(poly):
    return {m: c for m, c in poly.items() if c}


def linear_combination(polys, weights):
    out = defaultdict(Q)
    for p, c in zip(polys, weights):
        if c:
            for m, v in p.items():
                out[m] += Q(c) * Q(v)
    return clean(out)


def square_polynomial(poly):
    out = defaultdict(int)
    items = list(poly.items())
    for i, (a, x) in enumerate(items):
        for j in range(i, len(items)):
            b, y = items[j]
            out[tuple(sorted(a + b))] += x * y * (1 if i == j else 2)
    return clean(out)


def gauge_matrices():
    """Rational real actions and rational squared normalization factors."""
    descriptions = []
    for i, j in combinations(range(4), 2):
        for imaginary in [False, True]:
            t = np.zeros((4, 4), complex)
            t[i, j] = -1j if imaginary else 1
            t[j, i] = 1j if imaginary else 1
            descriptions.append((t, [0.] * 3, [0.] * 3, 0, Q(1, 4)))
    for k in range(1, 4):
        t = np.diag([1.] * k + [-float(k)] + [0.] * (3 - k)).astype(complex)
        descriptions.append((t, [0.] * 3, [0.] * 3, 0, Q(1, 2 * k * (k + 1))))
    for side in [1, 2]:
        for a in range(3):
            left, right = np.zeros(3), np.zeros(3)
            (left if side == 1 else right)[a] = 1
            descriptions.append((np.zeros((4, 4), complex), left, right, side, Q(1)))
    matrices, groups, weights = [], [], []
    for t, left, right, group, weight in descriptions:
        m = np.column_stack([scalar_gauge_action(e, t, left, right) for e in np.eye(68)])
        assert np.array_equal(2 * m, np.round(2 * m))
        matrices.append(m)
        groups.append(group)
        weights.append(weight)
    return matrices, groups, weights


def exact_gauge_polynomials(metric, matrices, groups, weights):
    """3 Tr(Mv^2)^2 by gauge-square pair; every operation after actions is exact."""
    pairs = [tuple(p) for p in archived.G['gauge_square_pairs']]
    out = [defaultdict(Q) for _ in pairs]
    for a in range(21):
        for b in range(a, 21):
            # Twice every raw action is integral; multiplying the Gram by four
            # gives an integral matrix with no floating-point reconstruction.
            ka = (2 * matrices[a]).astype(np.int64)
            kb = (2 * matrices[b]).astype(np.int64)
            matrix = ka.T @ (metric.astype(np.int64)[:, None] * kb)
            polynomial = {}
            for i in range(68):
                for j in range(i, 68):
                    value = int(matrix[i, j] if i == j else matrix[i, j] + matrix[j, i])
                    if value:
                        polynomial[(i, j)] = value
            factor = Q(3, 16) * weights[a] * weights[b] * (1 if a == b else 2)
            dest = out[pairs.index(tuple(sorted((groups[a], groups[b]))))]
            for m, v in square_polynomial(polynomial).items():
                dest[m] += factor * v
    return [clean(p) for p in out]


def project_exact(poly, basis):
    keys = sorted(set(poly).union(*(set(p) for p in basis)))
    array = np.array([[p.get(m, 0) for p in basis] for m in keys], float)
    _, _, pivots = qr(array.T, pivoting=True)
    chosen = [keys[i] for i in pivots[:len(basis)]]
    mat = sp.Matrix([[p.get(m, 0) for p in basis] for m in chosen])
    rhs = sp.Matrix([poly.get(m, 0) for m in chosen])
    coefficients = mat.inv() * rhs
    reconstructed = linear_combination(basis, [Q(str(v)) for v in coefficients])
    assert reconstructed == clean(poly)
    return coefficients


def explicit_trace_contractions():
    """Build two different invariant traces in Gaussian-integer arithmetic."""
    src = ROOT / 'docs/condensate_energy/charge_audit/source-snapshots/full_scalar_basis.py'
    tree = ast.parse(src.read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    env = dict(defaultdict=defaultdict, permutations=permutations, combinations=combinations,
               product=product, math=math, np=np)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(src), 'exec'), env)
    entry, mul, conj, norm, sumps = [env[k] for k in ['entry', 'mul', 'conj', 'norm', 'sumps']]
    d = [[[None] * 4 for _ in range(4)] for _ in range(3)]
    v = 8
    for a in range(3):
        for i in range(4):
            for j in range(i, 4):
                d[a][i][j] = d[a][j][i] = entry(v)
                v += 2
    color = [[sumps(mul(conj(d[a][k][i]), d[a][k][j])
                     for a, k in product(range(3), range(4))) for j in range(4)] for i in range(4)]
    spin = [[sumps(mul(conj(d[a][i][j]), d[b][i][j])
                    for i, j in product(range(4), repeat=2)) for b in range(3)] for a in range(3)]
    result = []
    for matrix in [color, spin]:
        p = sumps(norm(value) for row in matrix for value in row)
        assert all(complex(c).imag == 0 and complex(c).real == int(complex(c).real) for c in p.values())
        result.append({m: int(complex(c).real) for m, c in p.items() if c})
    return result


def component_check(polys, quadratics, metric, matrices, groups, weights, rng, families):
    x = rng.normal(size=68) / np.sqrt(metric)
    x /= np.linalg.norm(np.sqrt(metric) * x)
    lam = rng.normal(size=17) / 4
    g = rng.uniform(.1, .7, 3)
    Y = (rng.normal(size=(families, families)) + 1j * rng.normal(size=(families, families))) / 5
    Z = (rng.normal(size=(families, families)) + 1j * rng.normal(size=(families, families))) / 5
    F = (rng.normal(size=(families, families)) + 1j * rng.normal(size=(families, families))) / 10
    F += F.T.copy()
    vals, grads, hess = basis_derivatives(polys, quadratics, x)
    h = np.einsum('i,ijk->jk', lam, hess[:17]) / np.sqrt(metric[:, None] * metric[None, :])
    grad = lam @ grads[:17] / np.sqrt(metric)
    u = x * np.sqrt(metric)
    P, D = scalar_unpack(x)
    fermion = mass(P, D, Y, Z, F)
    t = tensors(Y, Z, F) / np.sqrt(metric)[:, None, None]
    s = np.einsum('aij,bij->ab', t.conj(), t).real
    directions = np.column_stack([g[group] * math.sqrt(float(w)) * np.sqrt(metric) * (m @ x)
                                  for m, group, w in zip(matrices, groups, weights)])
    gram = directions.T @ directions
    c = np.array([.75 * (g[1] ** 2 + g[2] ** 2)] * 8 + [4.5 * g[0] ** 2 + 2 * g[2] ** 2] * 60)
    mm = fermion.conj().T @ fermion
    parts = [float(np.trace(h @ h)), float(3 * np.trace(gram @ gram)),
             float(-2 * np.trace(mm @ mm).real), float(2 * (s @ u) @ grad), float(-6 * (c * u) @ grad)]
    beta = archived.beta(lam, np.zeros(4), g, Y, Z, F)['quartics'] * (32 * np.pi ** 2)
    assembled = float(beta @ vals[:17])
    residual = abs(assembled - sum(parts)) / max(1., sum(abs(v) for v in parts))
    projector = independent_projector()(P, D)[0]
    return dict(families=families, parts=parts, assembled=assembled, residual=residual,
                projector_residual=float(max(abs(projector - vals[:17]))))


def scalar_polynomial_beta(lam):
    return sp.Matrix(archived.S['coefficients']) .applyfunc(sp.Rational) * sp.Matrix(
        [lam[a] * lam[b] for a, b in archived.S['coupling_pairs']])


def integrate_example():
    initial = np.zeros(20)
    initial[0], initial[6:11], initial[13] = .08, .06, .02
    initial[17:] = [.3, .25, .35]
    scalar = archived.SC
    pairs = archived.S['coupling_pairs']
    gpairs = archived.G['gauge_square_pairs']

    def rhs(t, state):
        lam, g = state[:17], state[17:]
        g2 = g * g
        b = scalar @ np.array([lam[a] * lam[b] for a, b in pairs])
        b += lam * (archived.GL @ g2)
        b += archived.GC @ np.array([g2[a] * g2[b] for a, b in gpairs])
        return np.r_[b / (32 * np.pi ** 2), -np.array([23 / 3, 3., -11 / 3]) * g ** 3 / (16 * np.pi ** 2)]

    branches = []
    for end in [-2., 2.]:
        times = np.linspace(0, end, 81)
        normal = solve_ivp(rhs, (0, end), initial, method='DOP853', t_eval=times, rtol=1e-9, atol=1e-12)
        tight = solve_ivp(rhs, (0, end), initial, method='DOP853', t_eval=times, rtol=2e-12, atol=2e-14)
        assert normal.success and tight.success
        back = solve_ivp(rhs, (end, 0), tight.y[:, -1], method='DOP853', rtol=2e-12, atol=2e-14)
        assert back.success
        branches.append(dict(t=times.tolist(), states=tight.y.T.tolist(),
                             tolerance_difference=float(max(abs(normal.y - tight.y).flat)),
                             reversal_error=float(max(abs(back.y[:, -1] - initial)))))
    h = 1e-4
    small = solve_ivp(rhs, (0, h), initial, method='DOP853', rtol=2e-12, atol=2e-14)
    slopes = (small.y[:, -1] - initial) / h
    return dict(initial=initial.tolist(), initial_derivative=rhs(0, initial).tolist(),
                derivative_error=float(max(abs(slopes - rhs(0, initial)))), branches=branches,
                limits='Illustrative mass-independent one-loop running; no physical scale or vacuum selected.')


def main():
    checks, data = [], {}

    def check(name, passed, evidence=None):
        checks.append(dict(name=name, passed=bool(passed), evidence=evidence))
        print(name, 'PASS' if passed else 'FAIL', flush=True)

    polys, quadratics, metric = load_exact_basis()
    basis = [{m: Q(v, 18) for m, v in p.items()} for p in polys]
    archived_basis = json.loads((SNAP / 'quartics.json').read_text())
    check('archived-basis-identical', [{tuple(m): c for m, c in p} for p in archived_basis['quartics']] == polys)
    check('archived-kinetic-metric-identical', np.array_equal(metric, archived_basis['kinetic_metric']))
    provenance = json.loads((SNAP / 'provenance.json').read_text())
    check('source-hashes', all(sha256((SNAP / f).read_bytes()).hexdigest() == row['sha256']
                               for f, row in provenance['members'].items()))
    matrices, groups, weights = gauge_matrices()
    check('all-generators-preserve-kinetic-metric', all(np.array_equal(metric[:, None] * m + m.T * metric[None, :], np.zeros((68, 68))) for m in matrices))
    direct = exact_gauge_polynomials(metric, matrices, groups, weights)
    gauge_columns = []
    for j, pair in enumerate(archived.G['gauge_square_pairs']):
        column = [Q(row[j]) for row in archived.G['gauge_quartic_coefficients']]
        expected = linear_combination(basis, column)
        check('exact-gauge-pair-' + str(pair), direct[j] == expected, len(set(direct[j]) | set(expected)))
        gauge_columns.append([str(v) for v in column])
    data['exact_gauge_columns'] = dict(pairs=archived.G['gauge_square_pairs'], columns=gauge_columns,
                                     monomials=[len(p) for p in direct])

    lam = sp.symbols('l0:17', real=True)
    bscalar = scalar_polynomial_beta(lam)
    hol = {}
    for i in [11, 12]:
        scalar = sp.factor(bscalar[i])
        check(f'holomorphic-{i}-scalar-zero-surface', scalar.subs({lam[11]: 0, lam[12]: 0}) == 0)
        check(f'holomorphic-{i}-gauge-source-zero', all(Q(c) == 0 for c in archived.G['gauge_quartic_coefficients'][i]))
        check(f'holomorphic-{i}-fermion-box-source-zero', all(sp.sympify(row['coefficients'][i]) == 0 for row in archived.YUK['fermion_box']))
        wave = [dict(input=row['input_quartic'], word=row['trace_word'], coefficient=row['coefficients'][i])
                for row in archived.YUK['quartic_wave'] if row['coefficients'][i] != '0']
        check(f'holomorphic-{i}-wave-multiplicative', len(wave) == 1 and wave[0] == dict(input=i, word=['F', 'F^*'], coefficient='8'))
        hol[str(i)] = dict(scalar=str(scalar), gauge=archived.G['gauge_linear_coefficients'][i], wave=wave)
    data['holomorphic_beta'] = hol

    rho = sp.Symbol('rho', real=True)
    radial = [sp.Integer(0)] * 17
    radial[6:11] = [rho] * 5
    bradial = scalar_polynomial_beta(radial)
    check('isotropic-scalar-control', all(sp.expand(bradial[i] - 272 * rho ** 2) == 0 for i in range(6, 11)))
    delta_gauge = sp.Matrix([[sp.Rational(v) for v in row] for row in archived.G['gauge_quartic_coefficients'][6:11]])
    gauge_equal = delta_gauge * sp.ones(6, 1)
    check('gauge-breaks-isotropic-ansatz', len(set(gauge_equal)) > 1)
    hidden = [6, 8, 9, 10]
    check('four-hidden-norm-gauge-sources-nonzero', all(any(Q(v) for v in archived.G['gauge_quartic_coefficients'][i]) for i in hidden))
    box = sp.Matrix([sp.Rational(v) for v in archived.YUK['fermion_box'][0]['coefficients'][6:11]])
    check('majorana-breaks-isotropic-ansatz', len(set(box)) > 1)
    data['isotropic_controls'] = dict(scalar_beta=str(272 * rho ** 2), gauge_equal=[str(v) for v in gauge_equal],
                                      majorana_box=[str(v) for v in box],
                                      gauge_equal_difference_from_index7=[str(gauge_equal[i] - gauge_equal[1]) for i in [0, 2, 3, 4]])

    trace_polys = explicit_trace_contractions()
    trace_coefficients = [project_exact(p, basis[6:11]) for p in trace_polys]
    data['trace_contractions'] = {'color_gram': [str(v) for v in trace_coefficients[0]],
                                 'spin_gram': [str(v) for v in trace_coefficients[1]],
                                 'monomials': [len(p) for p in trace_polys]}
    check('trace-definitions-have-distinct-exact-expansions', trace_coefficients[0] != trace_coefficients[1])
    check('trace-definitions-agree-on-neutral-vacuum', trace_coefficients[0][1] == trace_coefficients[1][1] == 1)
    # The declared source equation in either possible trace convention removes
    # only one linear combination and leaves the rho1 parameter free.
    t = sp.Symbol('rho1', real=True)
    data['source_relation_conditional'] = {
        name: [str(sp.expand(t + (sp.Rational(16, 9) - 2 * t) * c)) for c in vec]
        for name, vec in zip(['color_gram', 'spin_gram'], trace_coefficients)}
    initial_span = sp.Matrix.hstack(sp.ones(5, 1), delta_gauge, box)
    span = sp.Matrix.hstack(*initial_span.columnspace())
    ranks = [span.rank()]
    for step in range(5):
        additions = []
        vectors = list(span.columnspace())
        for a in range(len(vectors)):
            for b in range(a, len(vectors)):
                vector = vectors[a] if a == b else vectors[a] + vectors[b]
                assignment = {l: 0 for l in lam}
                assignment.update({lam[6 + k]: vector[k] for k in range(5)})
                additions.append(bscalar[6:11, :].subs(assignment))
        widened = sp.Matrix.hstack(span, *additions)
        updated = sp.Matrix.hstack(*widened.columnspace())
        ranks.append(updated.rank())
        if updated.cols == span.cols:
            break
        span = updated
    data['delta_counterterm_span'] = dict(ranks=ranks, dimension=span.cols,
        meaning='Linear invariant-operator space generated by radial, independent gauge monomials, Majorana box and scalar contractions; not a count of fitted boundary inputs.')
    check('delta-hermitian-closure-requires-five-operator-directions', span.cols == 5)

    rng = np.random.default_rng(20260924)
    samples = [component_check(polys, quadratics, metric, matrices, groups, weights, rng, n) for n in [1, 1, 2, 2, 3, 3]]
    data['component_samples'] = samples
    for i, sample in enumerate(samples):
        check(f'full-component-beta-{i}', sample['residual'] < 1e-9 and sample['projector_residual'] < 1e-10, sample)
    flow = integrate_example()
    data['flow'] = flow
    check('running-tolerance-convergence', max(b['tolerance_difference'] for b in flow['branches']) < 1e-8)
    check('running-reversal', max(b['reversal_error'] for b in flow['branches']) < 1e-8)
    check('running-initial-derivative', flow['derivative_error'] < 1e-7)
    check('running-holomorphic-zeros-preserved', all(np.max(np.abs(np.array(b['states'])[:, 11:13])) == 0 for b in flow['branches']))
    check('running-hidden-norm-splitting', all(np.ptp(np.array(b['states'])[-1, 6:11]) > 1e-4 for b in flow['branches']))
    prior = ROOT / 'docs/condensate_energy/canonical_vacuum/receipt.json'
    receipt = json.loads(prior.read_text())
    check('previous-canonical-artifacts-unchanged', all(sha256((ROOT / p).read_bytes()).hexdigest() == digest for p, digest in receipt['artifact_sha256'].items()))
    check('previous-ancestral-receipts-unchanged', all(sha256((ROOT / p).read_bytes()).hexdigest() == digest for p, digest in receipt['prior_receipts_verified'].items()))
    data.update(checks=checks, checks_passed=sum(c['passed'] for c in checks), checks_total=len(checks),
                basis_labels=LABELS, prior_receipt_sha256=sha256(prior.read_bytes()).hexdigest(),
                versions=dict(numpy=np.__version__, scipy=__import__('scipy').__version__, sympy=sp.__version__))
    OUT.mkdir(exist_ok=True, parents=True)
    (OUT / 'results.json').write_text(json.dumps(data, indent=2) + '\n')
    assert all(c['passed'] for c in checks), 'Failed checks retained in results.json'


if __name__ == '__main__':
    main()
