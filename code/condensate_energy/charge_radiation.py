#!/usr/bin/env python3
"""Independent outgoing linear response to the quartic charge-breaking term."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import simpson, solve_bvp
from scipy.interpolate import CubicSpline
from scipy.sparse import bmat, diags
from scipy.sparse.linalg import spsolve

from self_binding import ROOT

OUT = ROOT / 'docs/condensate_energy/charge_leakage'


def background():
    stationary = json.loads((OUT.parent / 'self_binding/results.json').read_text())
    continuum = stationary['reference']['continuum']
    profile = continuum['profile']
    splines = [CubicSpline(profile['r'], profile[key]) for key in ['chi', 'f']]
    cutoff = profile['r'][-1]

    def fields(r):
        return np.where(r <= cutoff, splines[0](r), 1.), np.where(r <= cutoff, splines[1](r), 0.)

    return fields, continuum['omega'], stationary['reference']['fine']['b'], continuum['energy']


def coefficients(r, fields, omega, b):
    c, f = fields(r)
    diagonal = [c * c + 2 * b * f * f - (3 * omega) ** 2,
                c * c + 2 * b * f * f - (5 * omega) ** 2,
                3 * c * c - 1 + f * f - (4 * omega) ** 2]
    return diagonal, b * f * f, math.sqrt(2) * c * f, r * f ** 3


def observables(r, amplitudes, fields, omega, label):
    wave_numbers = np.sqrt(np.array([(3 * omega) ** 2 - 1, (5 * omega) ** 2 - 1, (4 * omega) ** 2 - 2]))
    magnitudes = abs(amplitudes[:, -1]) ** 2
    powers = 4 * math.pi * omega * np.array([3, 5, 4]) * wave_numbers * magnitudes
    charge_flux = 4 * math.pi * np.dot(np.array([-1, 1, 0]) * wave_numbers, magnitudes)
    _, f = fields(r)
    charge_source = 16 * math.pi * simpson(r * f ** 3 * amplitudes[0].imag, x=r)
    identity = charge_source + powers.sum() / omega - charge_flux
    return dict(label=label, radius=float(r[-1]), omega=omega,
                power_per_epsilon_squared=float(powers.sum()),
                power_channels=dict(q_minus3=float(powers[0]), q_plus5=float(powers[1]), chi_4=float(powers[2])),
                charge_flux_per_epsilon_squared=float(charge_flux),
                charge_source_per_epsilon_squared=float(charge_source),
                source_flux_identity_relative=float(abs(identity) / max(1., abs(charge_source))),
                wave_numbers=wave_numbers.tolist(),
                boundary_amplitudes=[[float(z.real), float(z.imag)] for z in amplitudes[:, -1]])


def finite_difference(fields, omega, b, radius, dr):
    r = np.linspace(0, radius, round(radius / dr) + 1)
    n = len(r)
    diagonal, uv, uh, source = coefficients(r, fields, omega, b)
    ks = np.sqrt(np.array([(3 * omega) ** 2 - 1, (5 * omega) ** 2 - 1, (4 * omega) ** 2 - 2]))
    blocks = []
    for d, k in zip(diagonal, ks):
        block = diags([-np.ones(n - 1) / dr ** 2, 2 / dr ** 2 + d, -np.ones(n - 1) / dr ** 2],
                      [-1, 0, 1], dtype=complex, format='lil')
        block[0, :] = 0
        block[0, 0] = 1
        block[-1, :] = 0
        block[-1, -3] = 1 / (2 * dr)
        block[-1, -2] = -2 / dr
        block[-1, -1] = 3 / (2 * dr) - 1j * k
        blocks.append(block)
    uv[[0, -1]], uh[[0, -1]] = 0, 0
    a, z = diags(uv), diags(uh)
    operator = bmat([[blocks[0], a, z], [a, blocks[1], z], [z, z, blocks[2]]], format='csc')
    force = np.zeros(3 * n, complex)
    force[1:n - 1] = -source[1:-1]
    solution = spsolve(operator, force).reshape(3, n)
    row = observables(r, solution, fields, omega, f'FD-{dr:g}-R{radius:g}')
    row['dr'] = dr
    row['linear_residual_relative'] = float(np.max(abs(operator @ solution.ravel() - force)) / max(1., np.max(abs(force))))
    return row


def continuum(fields, omega, b, radius):
    r = np.linspace(0, radius, 601)
    ks = np.sqrt(np.array([(3 * omega) ** 2 - 1, (5 * omega) ** 2 - 1, (4 * omega) ** 2 - 2]))

    def rhs(r, y):
        diagonal, uv, uh, source = coefficients(r, fields, omega, b)
        u, up, v, vp, h, hp = y
        return np.array([up, diagonal[0] * u + uv * v + uh * h + source,
                         vp, diagonal[1] * v + uv * u + uh * h,
                         hp, diagonal[2] * h + uh * (u + v)])

    def boundary(left, right):
        return np.concatenate((left[[0, 2, 4]], right[[1, 3, 5]] - 1j * ks * right[[0, 2, 4]]))

    sol = solve_bvp(rhs, boundary, r, np.zeros((6, len(r)), complex), tol=1e-8, max_nodes=30000)
    x = np.linspace(0, radius, 12001)
    values = sol.sol(x)[[0, 2, 4]]
    row = observables(x, values, fields, omega, f'BVP-R{radius:g}')
    row.update(success=bool(sol.success), message=sol.message, nodes=len(sol.x),
               max_rms_residual=float(max(sol.rms_residuals)),
               profile=dict(r=x[::10].tolist(), channels_real=values[:, ::10].real.tolist(), channels_imag=values[:, ::10].imag.tolist()))
    return row


def main():
    fields, omega, b, energy = background()
    sources = [Path(__file__).resolve(), OUT / 'radiation-protocol.md', OUT.parent / 'self_binding/results.json']
    data = dict(status='running', source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}, cases={}, checks=[])
    for radius in [30., 40.]:
        row = continuum(fields, omega, b, radius)
        data['cases'][row['label']] = row
        (OUT / 'radiation-results.json').write_text(json.dumps(data) + '\n')
        print(f"{row['label']}: P/epsilon^2={row['power_per_epsilon_squared']:.10g}, residual={row['max_rms_residual']:.3g}, identity={row['source_flux_identity_relative']:.3g}", flush=True)
    for dr in [.05, .025, .0125]:
        row = finite_difference(fields, omega, b, 30., dr)
        data['cases'][row['label']] = row
        (OUT / 'radiation-results.json').write_text(json.dumps(data) + '\n')
        print(f"{row['label']}: P/epsilon^2={row['power_per_epsilon_squared']:.10g}, linear residual={row['linear_residual_relative']:.3g}", flush=True)
    ref = data['cases']['BVP-R30']
    errors = [abs(data['cases'][f'FD-{dr:g}-R30']['power_per_epsilon_squared'] / ref['power_per_epsilon_squared'] - 1) for dr in [.05, .025, .0125]]
    domain_error = abs(data['cases']['BVP-R40']['power_per_epsilon_squared'] / ref['power_per_epsilon_squared'] - 1)
    data['checks'] = [dict(name='continuum-solver-residual', passed=all(row['success'] and row['max_rms_residual'] < 1e-6 for key, row in data['cases'].items() if key.startswith('BVP'))),
                     dict(name='independent-finite-difference-power', errors=errors, passed=errors[-1] < .005),
                     dict(name='finite-difference-errors-decrease', passed=errors[2] < errors[1] < errors[0]),
                     dict(name='domain-enlargement', error=domain_error, passed=domain_error < .001),
                     dict(name='source-flux-Ward-identity', error=ref['source_flux_identity_relative'], passed=ref['source_flux_identity_relative'] < .001)]
    data['initial_local_energy_over_power_scale'] = dict(coefficient=energy / ref['power_per_epsilon_squared'],
             formula='coefficient/epsilon^2 in the reference dimensionless units; initial weak-breaking scale, not a derived half-life')
    data['all_checks_passed'] = all(row['passed'] for row in data['checks'])
    data['status'] = 'qualified_linear_response' if data['all_checks_passed'] else 'failed_qualification'
    (OUT / 'radiation-results.json').write_text(json.dumps(data) + '\n')
    print(json.dumps(data['checks'], indent=2), flush=True)
    if not data['all_checks_passed']:
        raise SystemExit('Preserve the failed response before any amendment.')


if __name__ == '__main__':
    main()
