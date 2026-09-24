#!/usr/bin/env python3
"""Targeted mesh refinement and direct outward-energy-flux measurements."""
from concurrent.futures import ProcessPoolExecutor, as_completed
import copy
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from self_binding import ROOT, RadialGrid
from self_binding_polish import polish
from self_binding_dynamics import node_energies
from charge_leakage import half_exit

OUT = ROOT / 'docs/condensate_energy/charge_leakage'


def refined_reference(stationary):
    ref = copy.deepcopy(stationary['reference']['fine'])
    grid = RadialGrid(30., .025)
    ref['dr'] = .025
    ref['profile'] = dict(r=grid.r.tolist(), **{key: np.interp(grid.r, ref['profile']['r'], ref['profile'][key], right=boundary).tolist()
                                               for key, boundary in [('chi', 1.), ('f', 0.)]})
    result = polish(ref)
    assert result['gradient_infinity_norm'] < 1e-5
    return result


def integrate(job, ref):
    started = time.monotonic()
    dr, dt = job['dr'], job['dt']
    grid = RadialGrid(460., dr)
    r, b = grid.r, ref['b']
    epsilon = job['ratio'] * b
    chi = np.interp(r, ref['profile']['r'], ref['profile']['chi'], right=1.)
    q = np.interp(r, ref['profile']['r'], ref['profile']['f'], right=0.).astype(complex)
    omega = ref['charge'] / float(grid.w @ abs(q) ** 2)
    p, u = 1j * omega * q, np.zeros_like(r)
    edge = round(40 / dr) - 1

    def force(c, z):
        z2, abs2 = z * z, abs(z) ** 2
        fc = -grid.gradient(c, 1.) / grid.w - c * (c * c - 1) - c * abs2
        fq = -grid.gradient(z, 0.) / grid.w - c * c * z - b * abs2 * z - epsilon * np.conj(z2 * z)
        return fc, fq, epsilon * float(grid.w @ np.imag(z2 * z2))

    def energy():
        return node_energies(grid, chi, u, q, p, b) + grid.w * epsilon * np.real(q ** 4) / 4

    def flux():
        return -float(grid.k[edge] * ((chi[edge + 1] - chi[edge]) * (u[edge + 1] + u[edge]) / 2 +
                     np.real(np.conj(q[edge + 1] - q[edge]) * (p[edge + 1] + p[edge])) / 2))

    energies = energy()
    e0, e40 = float(energies.sum()), float(energies[:edge + 1].sum())
    q0 = float(grid.w @ np.imag(np.conj(q) * p))
    fc, fq, torque = force(chi, q)
    p40, integral_flux, integral_source = flux(), 0., 0.
    max_e = max_q = max_flux = max_tail = 0.
    steps, stride = round(400 / dt), round(.1 / dt)
    history = []
    for step in range(steps + 1):
        if step % stride == 0:
            en = energy()
            charge = float(grid.w @ np.imag(np.conj(q) * p))
            max_e = max(max_e, abs(float(en.sum()) - e0) / e0)
            max_q = max(max_q, abs(charge - q0 - integral_source) / abs(q0))
            max_flux = max(max_flux, abs(float(en[:edge + 1].sum()) - e40 + integral_flux) / e0)
            max_tail = max(max_tail, float(en[r > 450].sum()) / e0)
            history.append(dict(t=step * dt, charge=charge, local_energy_fraction=float(en[r < 15].sum()) / e0,
                                flux40=p40, integral_flux40=integral_flux,
                                energy_inside40=float(en[:edge + 1].sum()),
                                q40_real=float((q[edge] + q[edge + 1]).real / 2),
                                q40_imag=float((q[edge] + q[edge + 1]).imag / 2),
                                chi40=float((chi[edge] + chi[edge + 1]) / 2 - 1)))
        if step == steps:
            break
        # Equivalent kick-drift-kick form, sharing the original finite-volume Hamiltonian.
        u += .5 * dt * fc
        p += .5 * dt * fq
        chi += dt * u
        q += dt * p
        fcn, fqn, new_torque = force(chi, q)
        u += .5 * dt * fcn
        p += .5 * dt * fqn
        new_flux = flux()
        integral_flux += .5 * dt * (p40 + new_flux)
        integral_source += .5 * dt * (torque + new_torque)
        fc, fq, torque, p40 = fcn, fqn, new_torque, new_flux
    times = np.array([v['t'] for v in history])
    powers = np.array([v['flux40'] for v in history])
    late = times >= 200
    mean_power = float(np.trapezoid(powers[late], times[late]) / 200)
    blocks = []
    for start in [200, 250, 300, 350]:
        select = (times >= start) & (times <= start + 50)
        blocks.append(float(np.trapezoid(powers[select], times[select]) / 50))
    return dict(parameters=job, initial_energy=e0, initial_charge=q0,
                energy_drift=max_e, charge_balance_residual=max_q, energy_flux_balance_residual=max_flux,
                distant_tail=max_tail, final_local_energy_fraction=history[-1]['local_energy_fraction'],
                final_total_charge_fraction=history[-1]['charge'] / q0, half_energy_exit=half_exit(history),
                mean_power_200_400=mean_power, power_per_epsilon_squared=mean_power / epsilon ** 2,
                power_block_means=blocks, history=history, elapsed_seconds=time.monotonic() - started)


def main():
    raw = json.loads((OUT / 'results.json').read_text())
    assert [v['name'] for v in raw['checks'] if not v['passed']] == ['refinement-0.5']
    stationary = json.loads((OUT.parent / 'self_binding/results.json').read_text())
    finer = refined_reference(stationary)
    print('Refined initial stationary gradient:', finer['gradient_infinity_norm'], flush=True)
    sources = [Path(__file__).resolve(), OUT / 'numerical-amendment.md', OUT / 'results.json',
               ROOT / 'code/condensate_energy/charge_leakage.py', ROOT / 'code/condensate_energy/self_binding_polish.py',
               ROOT / 'code/condensate_energy/self_binding.py', ROOT / 'code/condensate_energy/self_binding_dynamics.py']
    data = dict(original_failures=[v for v in raw['checks'] if not v['passed']], refined_initial_profile=finer,
                source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                cases={}, checks=[], status='running')
    jobs = [dict(name='space-0.025', ratio=.5, dr=.025, dt=.00125, reference='finer'),
            dict(name='time-0.00125', ratio=.5, dr=.05, dt=.00125, reference='fine')]
    jobs += [dict(name=f'flux-{ratio:g}', ratio=ratio, dr=.1, dt=.005, reference='coarse') for ratio in [.001, .01, .05]]
    references = dict(stationary['reference'], finer=finer)
    with ProcessPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(integrate, job, references[job['reference']]): job for job in jobs}
        for future in as_completed(futures):
            job = futures[future]
            row = future.result()
            data['cases'][job['name']] = row
            (OUT / 'refinement-results.json').write_text(json.dumps(data) + '\n')
            print(f"{job['name']}: localE={row['final_local_energy_fraction']:.8f}, half-exit={row['half_energy_exit']}, mean P/epsilon^2={row['power_per_epsilon_squared']:.8g}, E drift={row['energy_drift']:.3g}", flush=True)
    for key, tolerance in [('energy_drift', .001), ('charge_balance_residual', 1e-8), ('energy_flux_balance_residual', .001), ('distant_tail', 1e-8)]:
        value = max(row[key] for row in data['cases'].values())
        data['checks'].append(dict(name=key, maximum=value, tolerance=tolerance, passed=value < tolerance))
    parent = raw['cases']['refined-0.5']
    for name in ['space-0.025', 'time-0.00125']:
        row = data['cases'][name]
        errors = dict(energy=max(abs(a['local_energy_fraction'] - b['local_energy_fraction']) for a, b in zip(parent['history'], row['history'])),
                      charge=max(abs(a['charge'] - b['charge']) / 1000 for a, b in zip(parent['history'], row['history'])))
        data['checks'].append(dict(name=name, errors=errors, tolerance=.02, passed=max(errors.values()) < .02))
    data['all_checks_passed'] = all(v['passed'] for v in data['checks'])
    data['status'] = 'qualified_targeted_refinement' if data['all_checks_passed'] else 'failed_targeted_refinement'
    (OUT / 'refinement-results.json').write_text(json.dumps(data) + '\n')
    print(json.dumps(data['checks'], indent=2), flush=True)
    if not data['all_checks_passed']:
        raise SystemExit('Targeted refinement still fails; preserve the result.')


if __name__ == '__main__':
    main()
