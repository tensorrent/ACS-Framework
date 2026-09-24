#!/usr/bin/env python3
"""Real formulation of the preserved outgoing linear-response problem."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp
from scipy.interpolate import CubicSpline

from charge_radiation import ROOT, OUT, background, coefficients, observables


def real_solve(fields, omega, b, radius, original):
    r = np.linspace(0, radius, 1201)
    ks = np.sqrt(np.array([(3 * omega) ** 2 - 1, (5 * omega) ** 2 - 1, (4 * omega) ** 2 - 2]))
    profile = original['profile']
    amps = np.array(profile['channels_real']) + 1j * np.array(profile['channels_imag'])
    spline = CubicSpline(profile['r'], amps, axis=1)
    y = np.zeros((6, len(r)), complex)
    y[[0, 2, 4]], y[[1, 3, 5]] = spline(r), spline(r, 1)

    def matrix(r):
        diagonal, uv, uh, _ = coefficients(r, fields, omega, b)
        m = np.zeros((6, 6, len(r)))
        for i in range(3):
            m[2 * i, 2 * i + 1] = 1
            m[2 * i + 1, 2 * i] = diagonal[i]
        m[1, 2] = m[3, 0] = uv
        m[1, 4] = m[3, 4] = m[5, 0] = m[5, 2] = uh
        return m

    def rhs(r, y):
        m = matrix(r)
        out = np.concatenate((np.einsum('ijr,jr->ir', m, y[:6]), np.einsum('ijr,jr->ir', m, y[6:])))
        out[1] += coefficients(r, fields, omega, b)[3]
        return out

    def jacobian(r, y):
        m = matrix(r)
        out = np.zeros((12, 12, len(r)))
        out[:6, :6], out[6:, 6:] = m, m
        return out

    def boundary(left, right):
        l, z = left[:6] + 1j * left[6:], right[:6] + 1j * right[6:]
        value = np.concatenate((l[[0, 2, 4]], z[[1, 3, 5]] - 1j * ks * z[[0, 2, 4]]))
        return np.concatenate((value.real, value.imag))

    sol = solve_bvp(rhs, boundary, r, np.concatenate((y.real, y.imag)), fun_jac=jacobian,
                    tol=1e-8, max_nodes=40000)
    x = np.linspace(0, radius, 16001)
    raw = sol.sol(x)
    values = (raw[:6] + 1j * raw[6:])[[0, 2, 4]]
    row = observables(x, values, fields, omega, f'real-BVP-R{radius:g}')
    row.update(success=bool(sol.success), message=sol.message, nodes=len(sol.x),
               max_rms_residual=float(max(sol.rms_residuals)),
               profile=dict(r=x[::10].tolist(), channels_real=values[:, ::10].real.tolist(),
                            channels_imag=values[:, ::10].imag.tolist()))
    return row


def main():
    raw_path = OUT / 'radiation-results.json'
    original = json.loads(raw_path.read_text())
    assert [r['name'] for r in original['checks'] if not r['passed']] == ['continuum-solver-residual']
    fields, omega, b, energy = background()
    sources = [Path(__file__).resolve(), ROOT / 'code/condensate_energy/charge_radiation.py',
               OUT / 'numerical-amendment.md', raw_path]
    result = dict(original_failure=original['checks'][0], source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}, cases={}, checks=[])
    for radius in [30., 40.]:
        row = real_solve(fields, omega, b, radius, original['cases'][f'BVP-R{radius:g}'])
        result['cases'][row['label']] = row
        print(row['label'], row['success'], row['max_rms_residual'], row['power_per_epsilon_squared'], flush=True)
    ref = result['cases']['real-BVP-R30']
    errors = [abs(original['cases'][f'FD-{dr:g}-R30']['power_per_epsilon_squared'] / ref['power_per_epsilon_squared'] - 1) for dr in [.05, .025, .0125]]
    domain_error = abs(result['cases']['real-BVP-R40']['power_per_epsilon_squared'] / ref['power_per_epsilon_squared'] - 1)
    result['checks'] = [dict(name='real-continuum-solver-residual', passed=all(row['success'] and row['max_rms_residual'] < 1e-6 for row in result['cases'].values())),
                        dict(name='independent-finite-difference-power', errors=errors, passed=errors[-1] < .005),
                        dict(name='finite-difference-errors-decrease', passed=errors[2] < errors[1] < errors[0]),
                        dict(name='domain-enlargement', error=domain_error, passed=domain_error < .001),
                        dict(name='source-flux-identity', error=ref['source_flux_identity_relative'], passed=ref['source_flux_identity_relative'] < .001)]
    result['initial_energy_over_power_coefficient'] = energy / ref['power_per_epsilon_squared']
    result['all_checks_passed'] = all(row['passed'] for row in result['checks'])
    (OUT / 'radiation-qualified.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['checks'], indent=2), flush=True)
    if not result['all_checks_passed']:
        raise SystemExit('Real response still not qualified; preserve results.')


if __name__ == '__main__':
    main()
