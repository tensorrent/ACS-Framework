#!/usr/bin/env python3
"""Prospective gauged-FLS branch, with Gauss law and exterior field energy."""
import datetime
import hashlib
import json
import math
from pathlib import Path
import shutil

import numpy as np
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp
from scipy.interpolate import CubicSpline

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy/gauge_completion'
B = 2 * math.sqrt(3) / 27


def gauged_bvp(charge, coupling, seed, radius=40., tolerance=1e-7):
    r = np.linspace(0., radius, round(radius * 20) + 1)
    old = seed['profile']
    c = np.interp(r, old['r'], old['chi'], right=1.)
    f = np.interp(r, old['r'], old['f'], right=0.)
    omega = seed['omega']
    om = np.interp(r, old['r'], old.get('Omega', [omega] * len(old['r'])), right=omega)
    fraction = cumulative_trapezoid(4 * math.pi * r * r * om * f * f, r, initial=0.)
    fraction /= fraction[-1]
    y = np.stack((c, np.gradient(c, r), f, np.gradient(f, r), om, np.gradient(om, r), fraction))
    y[[1, 3, 5], 0] = 0.

    def rhs(r, y):
        c, cp, f, fp, om, op, fraction = y
        return np.array([cp, c * (c * c - 1 + f * f), fp,
                         (c * c - om * om) * f + B * f ** 3,
                         op, coupling ** 2 * f * f * om,
                         4 * math.pi * r * r * om * f * f / charge])

    def jacobian(r, y):
        c, cp, f, fp, om, op, fraction = y
        out = np.zeros((7, 7, len(r)))
        out[0, 1] = out[2, 3] = out[4, 5] = 1.
        out[1, 0] = 3 * c * c - 1 + f * f
        out[1, 2] = out[3, 0] = 2 * c * f
        out[3, 2] = c * c - om * om + 3 * B * f * f
        out[3, 4] = -2 * om * f
        out[5, 2], out[5, 4] = 2 * coupling ** 2 * f * om, coupling ** 2 * f * f
        out[6, 2] = 8 * math.pi * r * r * om * f / charge
        out[6, 4] = 4 * math.pi * r * r * f * f / charge
        return out

    def boundary(left, right):
        return np.array([left[1], left[3], left[5], left[6],
                         right[0] - 1, right[2], right[6] - 1])

    solution = solve_bvp(rhs, boundary, r, y, S=np.diag([0., -2., 0., -2., 0., -2., 0.]),
                         fun_jac=jacobian, tol=tolerance, max_nodes=20000)
    x = np.linspace(0., radius, round(radius * 400) + 1)
    c, cp, f, fp, om, op, fraction = solution.sol(x)
    w = 4 * math.pi * x * x
    integral_charge = float(simpson(w * om * f * f, x=x))
    grad = float(simpson(.5 * w * (cp * cp + fp * fp), x=x))
    potential = float(simpson(w * (.25 * (c * c - 1) ** 2 + .5 * c * c * f * f + B / 4 * f ** 4), x=x))
    time = float(simpson(.5 * w * om * om * f * f, x=x))
    inside = float(simpson(.5 * w * op * op / coupling ** 2, x=x)) if coupling else 0.
    outside = 2 * math.pi * radius ** 3 * op[-1] ** 2 / coupling ** 2 if coupling else 0.
    gauss_charge = 4 * math.pi * radius ** 2 * op[-1] / coupling ** 2 if coupling else integral_charge
    omega = float(om[-1] + radius * op[-1])
    energy = grad + potential + time + inside + outside
    tail = float(simpson((w * om * f * f)[x > radius - 5], x=x[x > radius - 5]) / charge)
    radius90 = float(np.interp(.9, fraction, x))
    row = dict(charge=charge, b=B, coupling=coupling, radius=radius, tolerance=tolerance,
               success=bool(solution.success), message=solution.message, nodes=len(solution.x),
               max_rms_residual=float(max(solution.rms_residuals)), omega=omega,
               central_Omega=float(om[0]), integral_charge=integral_charge,
               energy=energy, energy_per_charge=energy / charge,
               gradient_energy=grad, potential_energy=potential, rotation_energy=time,
               electric_inside=inside, electric_outside=float(outside),
               charge_relative=abs(integral_charge / charge - 1),
               gauss_relative=abs(float(gauss_charge) / charge - 1),
               energy_identity_relative=abs(time + inside + outside - .5 * omega * charge) / energy,
               virial_relative=abs(grad + 3 * potential - 3 * time - inside - outside) / energy,
               tail_fraction=tail, radius90=radius90,
               profile=dict(r=x[::10].tolist(), chi=c[::10].tolist(), f=f[::10].tolist(),
                            Omega=om[::10].tolist(), charge_fraction=fraction[::10].tolist()))
    row['localized_candidate'] = bool(solution.success and omega < 1 and tail < 1e-6 and row['virial_relative'] < 1e-4)
    row['scalar_binding_candidate'] = bool(row['localized_candidate'] and energy < charge)
    return row


def run_gauge_survey():
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    attempt = OUT / 'attempts' / stamp
    attempt.mkdir(parents=True)
    paths = [Path(__file__).resolve(), OUT / 'protocol.md', OUT.parent / 'self_binding/results.json']
    for path in paths:
        shutil.copy2(path, attempt / ('self-binding-results.json' if path.name == 'results.json' else path.name))
    original = json.loads(paths[-1].read_text())['reference']['continuum']
    results = dict(attempt=stamp, source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                   cases={}, continuations={}, checks=[])

    def save(label, row, section='cases'):
        results[section][label] = row
        (attempt / 'results.json').write_text(json.dumps(results) + '\n')
        print(label, row['success'], 'E/Q', round(row['energy_per_charge'], 8),
              'omega', round(row['omega'], 8), 'tail', round(row['tail_fraction'], 8),
              'virial', row['virial_relative'], flush=True)

    seed_by_charge = {1000.: original}
    for charges in [[600., 300.], [1500., 2200., 3000.]]:
        seed = original
        for charge in charges:
            row = gauged_bvp(charge, 0., seed)
            save(f'Q{charge:g}-e0', row, 'continuations')
            if row['success']:
                seed = row
            seed_by_charge[charge] = seed
    for charge in [1000., 300., 3000.]:
        seed = seed_by_charge[charge]
        for coupling in [0., .02, .04, .06, .08, .10, .12, .14, .16, .18, .20, .25]:
            row = gauged_bvp(charge, coupling, seed)
            save(f'Q{charge:g}-e{coupling:g}', row)
            if row['success'] and row['localized_candidate']:
                seed = row
    for coupling in [.08, .12]:
        seed = results['cases'][f'Q1000-e{coupling:g}']
        for radius, tolerance, suffix in [(60., 1e-7, 'domain'), (40., 1e-9, 'tolerance')]:
            save(f'Q1000-e{coupling:g}-{suffix}', gauged_bvp(1000., coupling, seed, radius, tolerance))
    for coupling in [0., .04, .08]:
        row = results['cases'][f'Q1000-e{coupling:g}']
        passed = row['success'] and row['max_rms_residual'] < 1e-5
        passed &= max(row['gauss_relative'], row['charge_relative']) < 1e-5
        passed &= max(row['energy_identity_relative'], row['virial_relative']) < 1e-4
        results['checks'].append(dict(name=f'reference-e{coupling:g}', passed=bool(passed)))
    for coupling in [.08, .12]:
        base = results['cases'][f'Q1000-e{coupling:g}']
        errors = []
        for suffix in ['domain', 'tolerance']:
            row = results['cases'][f'Q1000-e{coupling:g}-{suffix}']
            errors.append(max(abs(row['energy'] / base['energy'] - 1), abs(row['omega'] / base['omega'] - 1)))
        results['checks'].append(dict(name=f'localization-e{coupling:g}', passed=bool(base['localized_candidate'] and max(errors) < 1e-3),
                                       differences=errors))
    results['all_checks_passed'] = all(row['passed'] for row in results['checks'])
    (attempt / 'results.json').write_text(json.dumps(results) + '\n')
    (OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results['checks'], indent=2), flush=True)


if __name__ == '__main__':
    run_gauge_survey()
