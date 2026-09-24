#!/usr/bin/env python3
"""Charge-breaking evolution with a measured source and preserved attempts."""
from concurrent.futures import ProcessPoolExecutor, as_completed
import datetime
import hashlib
import json
import math
from pathlib import Path
import shutil
import time

import numpy as np
import sympy as s

from self_binding import ROOT, RadialGrid
from self_binding_dynamics import node_energies

OUT = ROOT / 'docs/condensate_energy/charge_leakage'


def exact_contract():
    x, y, chi, b, epsilon = s.symbols('x y chi b epsilon', real=True)
    q = x + s.I * y
    phi = s.eye(2) * chi / 2
    delta = s.eye(4) * q / (2 * s.sqrt(2))
    nphi = s.trace(phi.conjugate().T * phi)
    ndelta = s.simplify(s.trace(delta.conjugate().T * delta))
    hol = s.simplify(3 * delta.det())
    potential = (nphi - s.Rational(1, 2)) ** 2 + 2 * nphi * ndelta + b * ndelta ** 2
    potential += s.Rational(16, 3) * epsilon * s.re(hol)
    expected = (chi * chi - 1) ** 2 / 4 + chi * chi * (x * x + y * y) / 2
    expected += b * (x * x + y * y) ** 2 / 4 + epsilon * s.re(q ** 4) / 4
    force = -s.diff(potential, x) - s.I * s.diff(potential, y)
    force_expected = -chi * chi * q - b * (x * x + y * y) * q - epsilon * s.conjugate(q) ** 3
    source = s.simplify(y * s.diff(potential, x) - x * s.diff(potential, y))
    kinetic_phi = s.trace(s.diff(phi, chi).conjugate().T * s.diff(phi, chi))
    kinetic_delta = s.trace(s.diff(delta, x).conjugate().T * s.diff(delta, x))
    # Gauge current projections are expectation values of representation generators.
    color_generators = []
    for i in range(3):
        t = s.zeros(4)
        t[i, i], t[i + 1, i + 1] = 1, -1
        color_generators.append(t)
    for i in range(4):
        for j in range(i + 1, 4):
            t = s.zeros(4)
            t[i, j] = t[j, i] = 1
            color_generators.append(t)
            t = s.zeros(4)
            t[i, j], t[j, i] = s.I, -s.I
            color_generators.append(t)
    color_projections = [s.simplify(s.trace(delta.conjugate().T *
                           (-t.conjugate() * delta - delta * t.conjugate().T))) for t in color_generators]
    # Real Cartesian spin-one generators are -i epsilon_abc; all diagonal entries zero.
    spin_generators = [s.Matrix(3, 3, lambda i, j: -s.I * s.LeviCivita(a, i, j)) for a in range(3)]
    pauli = [s.Matrix([[0, 1], [1, 0]]), s.Matrix([[0, -s.I], [s.I, 0]]), s.diag(1, -1)]
    phi_projections = [s.simplify(s.trace(phi.conjugate().T * t * phi)) for t in pauli]
    checks = dict(canonical_Phi_kinetic=kinetic_phi == s.Rational(1, 2),
                  canonical_Delta_kinetic=kinetic_delta == s.Rational(1, 2),
                  gauge_invariant_potential_matches=s.expand(potential - expected) == 0,
                  independent_potential_gradient_matches_force=s.expand(force - force_expected) == 0,
                  exact_charge_source=s.expand(source - epsilon * s.im(q ** 4)) == 0,
                  all_15_color_current_projections_zero=all(v == 0 for v in color_projections),
                  spin_one_current_projections_zero=all(t[2, 2] == 0 for t in spin_generators),
                 _Phi_weak_current_projections_zero=all(v == 0 for v in phi_projections))
    return dict(checks=checks, HDelta=str(hol), charge_source=str(source),
                map='Phi=chi I2/2; D1=D2=0; D3=q I4/(2sqrt(2)); kappa=8epsilon/3',
                boundary='selected classical scalar action/vacuum; not canonical ACS parameter selection or full-field stability')


def half_exit(history, window=10.):
    times = np.array([r['t'] for r in history])
    local = np.array([r['local_energy_fraction'] for r in history])
    count = round(window / (times[1] - times[0])) + 1
    good = np.convolve((local < .5).astype(int), np.ones(count, int), mode='valid')
    indices = np.flatnonzero(good == count)
    return float(times[indices[0]]) if len(indices) else None


def evolve_case(job, reference):
    started = time.monotonic()
    dr = reference['dr']
    dt = .005 if dr == .1 else .0025
    grid = RadialGrid(460., dr)
    b = reference['b']
    epsilon = job['ratio'] * b
    assert abs(epsilon) < b
    r = grid.r
    chi = np.interp(r, reference['profile']['r'], reference['profile']['chi'], right=1.)
    f = np.interp(r, reference['profile']['r'], reference['profile']['f'], right=0.)
    q = f.astype(complex) * np.exp(1j * job.get('phase', 0.))
    omega = job.get('sign', 1.) * reference['charge'] / float(grid.w @ abs(q) ** 2)
    p = 1j * omega * q
    u = np.zeros_like(r)
    if job.get('vacuum'):
        chi[:] = 1.
        q[:] = p[:] = 0.

    def forces(c, z):
        z2 = z * z
        abs2 = abs(z) ** 2
        fc = -grid.gradient(c, 1.) / grid.w - c * (c * c - 1) - c * abs2
        fq = -grid.gradient(z, 0.) / grid.w - c * c * z - b * abs2 * z - epsilon * np.conj(z2 * z)
        torque = epsilon * float(grid.w @ np.imag(z2 * z2))
        return fc, fq, torque

    def energy(c, v, z, velocity):
        return node_energies(grid, c, v, z, velocity, b) + grid.w * epsilon * np.real(z ** 4) / 4

    energy0 = float(energy(chi, u, q, p).sum())
    charge0 = float(grid.w @ np.imag(np.conj(q) * p))
    escale, qscale = max(1., energy0), max(1., abs(charge0))
    fchi, fq, source = forces(chi, q)
    integrated = 0.
    max_edrift = max_balance = max_tail = 0.
    probe_indices = [int(np.argmin(abs(r - value))) for value in [20., 40., 60.]]
    history = []
    steps, stride = round(400 / dt), round(.1 / dt)
    for step in range(steps + 1):
        if step % stride == 0:
            en = energy(chi, u, q, p)
            qdens = grid.w * np.imag(np.conj(q) * p)
            total, charge = float(en.sum()), float(qdens.sum())
            max_edrift = max(max_edrift, abs(total - energy0) / escale)
            max_balance = max(max_balance, abs(charge - charge0 - integrated) / qscale)
            max_tail = max(max_tail, float(en[r > 450].sum()) / escale)
            history.append(dict(t=step * dt, energy=total, charge=charge, integrated_source=integrated,
                                source=source, local_energy_fraction=float(en[r < 15].sum()) / escale,
                                local_charge_fraction=float(qdens[r < 15].sum()) / qscale,
                                chi0=float(chi[0]), q0_real=float(q[0].real), q0_imag=float(q[0].imag),
                                probes=[[float(q[i].real), float(q[i].imag), float(chi[i] - 1)] for i in probe_indices]))
        if step == steps:
            break
        cn = chi + dt * u + .5 * dt * dt * fchi
        qn = q + dt * p + .5 * dt * dt * fq
        fcn, fqn, new_source = forces(cn, qn)
        u += .5 * dt * (fchi + fcn)
        p += .5 * dt * (fq + fqn)
        integrated += .5 * dt * (source + new_source)
        chi, q, fchi, fq, source = cn, qn, fcn, fqn, new_source
    return dict(parameters=dict(**job, dr=dr, dt=dt, radius=460., end=400., b=b,
                                epsilon=epsilon, omega_initial=omega),
                initial_energy=energy0, initial_charge=charge0,
                energy_drift=max_edrift, charge_balance_residual=max_balance, distant_tail=max_tail,
                final_local_energy_fraction=history[-1]['local_energy_fraction'],
                final_total_charge_fraction=history[-1]['charge'] / qscale,
                max_total_charge_change=max(abs(row['charge'] - charge0) / qscale for row in history),
                half_energy_exit=half_exit(history), observation_end=400.,
                actual_probe_radii=[float(r[i]) for i in probe_indices], history=history,
                elapsed_seconds=time.monotonic() - started)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    attempt = OUT / 'attempts' / stamp
    attempt.mkdir(parents=True)
    sources = [Path(__file__).resolve(), OUT / 'protocol.md',
               ROOT / 'code/condensate_energy/self_binding.py',
               ROOT / 'code/condensate_energy/self_binding_dynamics.py']
    for path in sources:
        shutil.copy2(path, attempt / path.name)
    for parent in ['self_binding', 'charge_audit']:
        receipt = json.loads((OUT.parent / parent / 'receipt.json').read_text())
        for name, digest in receipt['artifact_sha256'].items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    stationary = json.loads((OUT.parent / 'self_binding/results.json').read_text())
    contract = exact_contract()
    data = dict(attempt=stamp, status='running', contract=contract, cases={}, checks=[],
                source_sha256={str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
                stationary_sha256=hashlib.sha256((OUT.parent / 'self_binding/results.json').read_bytes()).hexdigest())
    for name, passed in contract['checks'].items():
        data['checks'].append(dict(name=name, passed=bool(passed)))
    (attempt / 'results.json').write_text(json.dumps(data) + '\n')
    assert all(contract['checks'].values()), contract
    print('All 8 exact field-map, force, current and source checks passed.', flush=True)
    jobs = [dict(name=f'ratio-{ratio:g}', ratio=ratio, reference='coarse')
            for ratio in [0., .001, .01, .05, .1, .25, .5, .9]]
    jobs += [dict(name='phase-pi8', ratio=.5, phase=math.pi / 8, reference='coarse'),
             dict(name='phase-pi4', ratio=.5, phase=math.pi / 4, reference='coarse'),
             dict(name='negative', ratio=-.5, reference='coarse'),
             dict(name='opposite-charge', ratio=.5, sign=-1., reference='coarse'),
             dict(name='vacuum', ratio=.5, vacuum=True, reference='coarse'),
             dict(name='refined-0.1', ratio=.1, reference='fine'),
             dict(name='refined-0.5', ratio=.5, reference='fine')]
    with ProcessPoolExecutor(max_workers=2) as pool:
        future_jobs = {pool.submit(evolve_case, job, stationary['reference'][job['reference']]): job for job in jobs}
        for future in as_completed(future_jobs):
            job = future_jobs[future]
            row = future.result()
            data['cases'][job['name']] = row
            (attempt / 'results.json').write_text(json.dumps(data) + '\n')
            print(f"{job['name']}: local E={row['final_local_energy_fraction']:.8f}, total Q/Q0={row['final_total_charge_fraction']:.8f}, max dQ={row['max_total_charge_change']:.4g}, half-exit={row['half_energy_exit']}, E drift={row['energy_drift']:.3g}, balance={row['charge_balance_residual']:.3g}", flush=True)
    for key, tolerance in [('energy_drift', 1e-3), ('charge_balance_residual', 1e-8), ('distant_tail', 1e-8)]:
        value = max(row[key] for row in data['cases'].values())
        data['checks'].append(dict(name=key, maximum=value, tolerance=tolerance, passed=value < tolerance))
    for ratio in [.1, .5]:
        coarse = data['cases'][f'ratio-{ratio:g}']
        fine = data['cases'][f'refined-{ratio:g}']
        energy_error = max(abs(a['local_energy_fraction'] - b['local_energy_fraction']) for a, b in zip(coarse['history'], fine['history']))
        charge_error = max(abs(a['charge'] - b['charge']) / abs(coarse['initial_charge']) for a, b in zip(coarse['history'], fine['history']))
        data['checks'].append(dict(name=f'refinement-{ratio:g}', energy_error=energy_error, charge_error=charge_error,
                                   tolerance=.02, passed=max(energy_error, charge_error) < .02))
    for a, b, charge_sign in [('negative', 'phase-pi4', 1), ('ratio-0.5', 'opposite-charge', -1)]:
        left, right = data['cases'][a], data['cases'][b]
        energy_error = max(abs(x['local_energy_fraction'] - y['local_energy_fraction']) for x, y in zip(left['history'], right['history']))
        charge_error = max(abs(x['charge'] - charge_sign * y['charge']) / 1000 for x, y in zip(left['history'], right['history']))
        data['checks'].append(dict(name=f'equivalence-{a}-{b}', energy_error=energy_error, charge_error=charge_error,
                                   tolerance=1e-8, passed=max(energy_error, charge_error) < 1e-8))
    data['checks'].append(dict(name='vacuum-remains-vacuum', passed=all(row['energy'] == 0 for row in data['cases']['vacuum']['history'])))
    data['checks'].append(dict(name='all-15-registered-cases-completed', passed=len(data['cases']) == 15))
    data['all_checks_passed'] = all(row['passed'] for row in data['checks'])
    data['status'] = 'qualified_finite_time_run' if data['all_checks_passed'] else 'numerical_qualification_failed'
    (attempt / 'results.json').write_text(json.dumps(data) + '\n')
    (OUT / 'latest-attempt.json').write_text(json.dumps(dict(attempt=stamp, status=data['status']), indent=2) + '\n')
    (OUT / 'results.json').write_text(json.dumps(data) + '\n')
    print(json.dumps(data['checks'], indent=2), flush=True)
    if not data['all_checks_passed']:
        raise SystemExit('Preserved numerical failure; targeted amendment needed before qualification.')


if __name__ == '__main__':
    main()
