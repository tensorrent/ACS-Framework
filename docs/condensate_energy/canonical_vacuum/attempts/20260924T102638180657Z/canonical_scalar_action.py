#!/usr/bin/env python3
"""Complete inherited scalar invariant action in its measured kinetic metric."""
import ast
from collections import defaultdict
from itertools import combinations, permutations, product
import itertools
import math
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy/canonical_vacuum'
SNAP = ROOT / 'docs/condensate_energy/charge_audit/source-snapshots'
LABELS = ['Nphi^2', '|detPhi|^2', 'Re(detPhi^2)', 'Im(detPhi^2)',
          'Nphi Re(detPhi)', 'Nphi Im(detPhi)', 'Delta35_spin0', 'Delta35_spin2',
          'Delta20_spin0', 'Delta20_spin2', 'Delta45_spin1', 'Re HDelta', 'Im HDelta',
          'Nphi NDelta', 'Re(detPhi) NDelta', 'Im(detPhi) NDelta', 'Jphi dot JDelta']


def load_exact_basis():
    path = SNAP / 'full_scalar_basis.py'
    tree = ast.parse(path.read_text())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    env = dict(defaultdict=defaultdict, permutations=permutations, combinations=combinations,
               product=product, math=math, np=np)
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), env)
    polynomials, metric = env['build']()
    quadratics = [{(i, i): 1 for i in range(8)},
                  {(0, 6): 1, (1, 7): -1, (2, 4): -1, (3, 5): 1},
                  {(0, 7): 1, (1, 6): 1, (2, 5): -1, (3, 4): -1},
                  {(i, i): metric[i] // 2 for i in range(8, 68)}]
    return polynomials, quadratics, np.array(metric, float)


def independent_projector():
    path = SNAP / 'scalar_invariant_basis.py'
    tree = ast.parse(path.read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'invariants')
    pauli = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]).astype(complex)]
    env = dict(np=np, itertools=itertools, math=math, perms=list(permutations(range(4))), pauli=pauli)
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(path), 'exec'), env)
    return env['invariants']


def scalar_unpack(x):
    phi = (x[:8:2] + 1j * x[1:8:2]).reshape(2, 2)
    delta = np.zeros((3, 4, 4), complex)
    v = 8
    for a in range(3):
        for i in range(4):
            for j in range(i, 4):
                delta[a, i, j] = delta[a, j, i] = x[v] + 1j * x[v + 1]
                v += 2
    return phi, delta


def scalar_pack(phi, delta):
    values = list(phi.flat)
    values.extend(delta[a, i, j] for a in range(3) for i in range(4) for j in range(i, 4))
    out = np.empty(68)
    out[::2], out[1::2] = np.real(values), np.imag(values)
    return out


def polynomial_derivatives(poly, x, scale=1.):
    monomials = np.array(list(poly), int)
    coefficients = np.array(list(poly.values()), float) / scale
    degree = monomials.shape[1]
    values = x[monomials]
    value = float(coefficients @ np.prod(values, axis=1))
    gradient, hessian = np.zeros(68), np.zeros((68, 68))
    for i in range(degree):
        keep = [j for j in range(degree) if j != i]
        np.add.at(gradient, monomials[:, i], coefficients * np.prod(values[:, keep], axis=1))
        for j in range(degree):
            if i == j:
                continue
            keep = [k for k in range(degree) if k not in (i, j)]
            np.add.at(hessian, (monomials[:, i], monomials[:, j]), coefficients * np.prod(values[:, keep], axis=1))
    return value, gradient, hessian


def basis_derivatives(polys, quadratics, x):
    rows = [polynomial_derivatives(p, x, 18.) for p in polys]
    rows += [polynomial_derivatives(p, x) for p in quadratics]
    return tuple(np.array([r[i] for r in rows]) for i in range(3))


def scalar_gauge_action(x, color, left, right):
    phi, delta = scalar_unpack(x)
    pauli = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]).astype(complex)]
    left_m = sum((left[a] * pauli[a] / 2 for a in range(3)), np.zeros((2, 2), complex))
    right_m = sum((right[a] * pauli[a] / 2 for a in range(3)), np.zeros((2, 2), complex))
    dp = 1j * (left_m @ phi - phi @ right_m)
    dd = np.array([-1j * (color.conj() @ d + d @ color.conj().T) for d in delta])
    for a in range(3):
        dd[(a + 1) % 3] += right[a] * delta[(a + 2) % 3]
        dd[(a + 2) % 3] -= right[a] * delta[(a + 1) % 3]
    return scalar_pack(dp, dd)


def canonical_gauge_orbit(x, metric):
    from gauge_carrier_contract import canonical_color_basis
    color_basis, names = canonical_color_basis()
    cols = [scalar_gauge_action(x, np.array(t, complex), [0.] * 3, [0.] * 3) for t in color_basis]
    for side in range(2):
        for a in range(3):
            left, right = np.zeros(3), np.zeros(3)
            (left if side == 0 else right)[a] = 1.
            cols.append(scalar_gauge_action(x, np.zeros((4, 4), complex), left, right))
    return np.sqrt(metric)[:, None] * np.array(cols).T


def electromagnetic_generator(metric):
    color = np.diag([1 / 6, 1 / 6, 1 / 6, -1 / 2]).astype(complex)
    matrix = np.column_stack([scalar_gauge_action(np.eye(68)[i], color, [0, 0, 1], [0, 0, 1]) for i in range(68)])
    return np.sqrt(metric)[:, None] * matrix / np.sqrt(metric)[None, :]


def physical_spectrum(hessian, gradient, x, metric):
    hc = hessian / np.sqrt(metric[:, None] * metric[None, :])
    orbit = canonical_gauge_orbit(x, metric)
    u, singular, vh = np.linalg.svd(orbit, full_matrices=True)
    rank = int(np.sum(singular > 1e-10))
    physical = u[:, rank:]
    hp = physical.T @ hc @ physical
    mass2, vectors = np.linalg.eigh(hp)
    scale = max(1., float(np.linalg.norm(hc, 2)))
    tol = 1e-8 * scale
    em = electromagnetic_generator(metric)
    cp = physical.T @ (-em @ em) @ physical
    charges2, charge_vectors = np.linalg.eigh(cp)
    sectors = []
    for charge in [0., 1 / 3, 2 / 3, 1., 4 / 3, 2.]:
        mask = abs(charges2 - charge ** 2) < 1e-8
        v = charge_vectors[:, mask]
        if not v.shape[1]:
            continue
        ev = np.linalg.eigvalsh(v.T @ hp @ v)
        sectors.append(dict(abs_electric_charge=charge, real_modes=len(ev), mass_squared=ev.tolist(),
                            negative=int(np.sum(ev < -tol)), zero=int(np.sum(abs(ev) <= tol)), positive=int(np.sum(ev > tol))))
    factors = np.linspace(.3, 2.2, 68)
    changed_h = factors[:, None] * hessian * factors[None, :]
    changed_g = np.diag(factors * factors * metric)
    generalized = eigh(changed_h, changed_g, eigvals_only=True)
    invariant_error = float(np.max(abs(generalized - np.linalg.eigvalsh(hc))) / scale)
    return dict(gauge_orbit_rank=rank, physical_real_modes=len(mass2), mass_squared=mass2.tolist(),
                negative=int(np.sum(mass2 < -tol)), zero=int(np.sum(abs(mass2) <= tol)), positive=int(np.sum(mass2 > tol)),
                minimum_mass_squared=float(mass2[0]), zero_band=tol,
                tadpole_infinity_norm=float(max(abs(gradient / np.sqrt(metric)))),
                goldstone_ward_relative=float(np.linalg.norm(hc @ orbit) / max(1., np.linalg.norm(orbit) * scale)),
                em_antisymmetry=float(np.linalg.norm(em + em.T)),
                mass_charge_commutator_relative=float(np.linalg.norm(hc @ em - em @ hc) / scale),
                em_vacuum_invariance=float(np.linalg.norm(em @ (np.sqrt(metric) * x))),
                coordinate_rescaling_spectrum_error=invariant_error,
                raw_hessian_spectrum_change=float(np.max(abs(np.linalg.eigvalsh(changed_h) - np.linalg.eigvalsh(hessian)))),
                sectors=sectors, canonical_hessian=hc.tolist())
