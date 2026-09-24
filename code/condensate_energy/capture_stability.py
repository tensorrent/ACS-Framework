#!/usr/bin/env python3
"""Externally gated capture and an independently supplied bound-mode control.

This extends the explicitly specified linear wave toy, not full Klein foam.
Every invocation preserves its source, protocol, raw data and check outcomes.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import math
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq
from scipy.sparse import diags
from scipy.sparse.linalg import splu

from run import (ROOT, build_grid, cut_flux, h_action, midpoint_step,
                 node_energy, region_energy)

OUT = ROOT / 'docs/condensate_energy/capture_stability'
CHECKS = []


def gate_value(t, height, start, duration, reopen=None):
    """Return prescribed height and its derivative; start=None means static."""
    if start is None:
        return height, 0.

    def ramp(z):
        if z <= 0:
            return 0., 0.
        if z >= duration:
            return 1., 0.
        return (.5*(1-math.cos(math.pi*z/duration)),
                .5*math.pi/duration*math.sin(math.pi*z/duration))

    value, rate = ramp(t-start)
    if reopen is not None:
        remove, remove_rate = ramp(t-reopen)
        value -= remove
        rate -= remove_rate
    return height*value, height*rate


def initial_pulse(x, potential, dx, center=30., phase=0.):
    xi = x[1:-1]
    q = np.exp(-.5*((xi-center)/4)**2-1j*np.pi/4*xi+1j*phase)
    p = (-(xi-center)/16-1j*np.pi/4)*q
    norm = math.sqrt(node_energy(q, p, potential, dx).sum())
    return q/norm, p/norm


def gated_run(height, start=None, duration=4., reopen=None, dx=.1, dt=.005,
              domain=240., end=160., center=30., phase=0.):
    x, shape, _ = build_grid(1., 1., dx, domain)
    hi, _ = gate_value(0., height, start, duration, reopen)
    potential = hi*shape
    q, p = initial_pulse(x, potential, dx, center, phase)
    n = len(q)
    cut_core, cut_trap = round(4/dx), round(5/dx)
    core_weights = np.zeros(n+2)
    core_weights[:cut_core] = 1.
    core_weights[cut_core] = .5
    trap_weights = np.zeros(n+2)
    trap_weights[:cut_trap] = 1.
    trap_weights[cut_trap] = .5
    active = np.flatnonzero(shape[1:-1])
    active_shape = shape[1:-1][active]
    core_active = core_weights[1:-1][active]
    trap_active = trap_weights[1:-1][active]
    e0 = node_energy(q, p, potential, dx)
    total0 = float(e0.sum())
    core0, trapped0 = region_energy(e0, cut_core), region_energy(e0, cut_trap)
    work = positive = negative = work_core = work_trap = continuum_work = 0.
    flux_core = flux_trap = 0.
    residual = core_residual = trap_residual = tail = 0.
    rows = []
    stride, steps = round(.2/dt), round(end/dt)
    factor = None
    last_mid_height = None
    offdiag = np.full(n-1, -dt**2/(4*dx**2))
    for step in range(steps+1):
        t = step*dt
        if step % stride == 0 or step == steps:
            e = node_energy(q, p, hi*shape, dx)
            total = float(e.sum())
            core = region_energy(e, cut_core)
            trapped = region_energy(e, cut_trap)
            residual = max(residual, abs(total-total0-work))
            core_residual = max(core_residual, abs(core-core0+flux_core-work_core))
            trap_residual = max(trap_residual, abs(trapped-trapped0+flux_trap-work_trap))
            tail = max(tail, float(e[x>domain-10].sum()))
            rows.append(dict(t=t, height=hi, core=core, barrier=trapped-core,
                             trapped=trapped, total=total, work=work,
                             work_positive=positive, work_negative=negative,
                             work_trap=work_trap, continuum_midpoint_work=continuum_work,
                             outward_flux_integral=flux_trap))
        if step == steps:
            break
        hn, _ = gate_value((step+1)*dt, height, start, duration, reopen)
        hm = (hi+hn)/2
        if hm != last_mid_height:
            diagonal = 2/dx**2+hm*shape[1:-1]
            factor = splu(diags([offdiag, 1+dt**2*diagonal/4, offdiag],
                               [-1, 0, 1], dtype=complex, format='csc'))
            last_mid_height = hm
        qn, pn, qm, pm = midpoint_step(q, p, diagonal, dx, dt, factor)
        flux_core += dt*cut_flux(qm, pm, cut_core, dx)
        flux_trap += dt*cut_flux(qm, pm, cut_trap, dx)
        if hn != hi:
            dw_nodes = .25*dx*(hn-hi)*active_shape*(abs(qn[active])**2+abs(q[active])**2)
            dw = float(dw_nodes.sum())
            work += dw
            positive += max(dw, 0.)
            negative += min(dw, 0.)
            work_core += float(dw_nodes@core_active)
            work_trap += float(dw_nodes@trap_active)
            _, rate = gate_value(t+.5*dt, height, start, duration, reopen)
            continuum_work += .5*dt*dx*rate*float(active_shape@abs(qm[active])**2)
        q, p, hi = qn, pn, hn
    summaries = {}
    for requested in [80., 160.]:
        if requested <= end:
            row = min(rows, key=lambda r: abs(r['t']-requested))
            summaries[f'at_{int(requested)}'] = {k: row[k] for k in
                                                ('t', 'trapped', 'core', 'barrier', 'total', 'work')}
    peak = max(rows, key=lambda r: r['trapped'])
    summaries['peak'] = dict(t=peak['t'], trapped=peak['trapped'])
    result = dict(parameters=dict(height=height, start=start, duration=duration,
                                 reopen=reopen, dx=dx, dt=dt, domain=domain,
                                 end=end, center=center, phase=phase),
                  initial_energy=total0, budget_residual=residual,
                  core_budget_residual=core_residual, trap_budget_residual=trap_residual,
                  max_distant_tail=tail, endpoint_vs_midpoint_work=abs(work-continuum_work),
                  summary=summaries, history=rows)
    return result, (q, p)


def assert_check(name, passed, **details):
    row = dict(name=name, passed=bool(passed), **details)
    CHECKS.append(row)
    print(f'{"PASS" if passed else "FAIL"}: {name}', flush=True)


def independent_calibration():
    options = dict(height=16., start=6., duration=2., domain=40., end=12., center=10.)
    coarse, fc = gated_run(**options, dt=.005)
    fine, ff = gated_run(**options, dt=.0025)
    dx = .1
    x, shape, _ = build_grid(1., 1., dx, 40.)
    q0, p0 = initial_pulse(x, np.zeros_like(x), dx, center=10.)
    n = len(q0)

    def rhs(t, y):
        height, rate = gate_value(t, 16., 6., 2.)
        q, p = y[:n], y[n:2*n]
        dw = .5*dx*rate*float(shape[1:-1]@abs(q)**2)
        return np.concatenate((p, -h_action(q, 2/dx**2+height*shape[1:-1], dx), [dw]))

    reference = solve_ivp(rhs, (0., 12.), np.concatenate((q0, p0, [0j])),
                          method='DOP853', rtol=2e-11, atol=2e-13)
    if not reference.success:
        raise RuntimeError(reference.message)
    reference_work = float(reference.y[-1, -1].real)
    errors = [math.sqrt(node_energy(f[0]-reference.y[:n, -1],
                                   f[1]-reference.y[n:2*n, -1], 16*shape, dx).sum())
              for f in [fc, ff]]
    work_errors = [abs(r['history'][-1]['work']-reference_work) for r in [coarse, fine]]
    assert_check('independent time-dependent ODE state convergence',
                 errors[1] < errors[0] and errors[1] < .005,
                 coarse_error=errors[0], fine_error=errors[1], evaluations=reference.nfev)
    assert_check('independent continuum work integral convergence',
                 work_errors[1] < work_errors[0] and work_errors[1] < .005,
                 reference_work=reference_work, coarse_error=work_errors[0], fine_error=work_errors[1])
    return dict(coarse=coarse, fine=fine, ode_energy_norm_errors=errors,
                ode_work_errors=work_errors, reference_work=reference_work,
                ode_evaluations=reference.nfev)


def bound_mode_control():
    length, mu = 4., 2.

    def matching(omega):
        return omega/math.tan(length*omega)+math.sqrt(max(0., mu**2-omega**2))

    roots = []
    for branch in range(math.ceil(length*mu/math.pi)):
        low = (branch+.5)*math.pi/length+1e-12
        high = min((branch+1)*math.pi/length-1e-12, mu)
        if low < high and matching(low)*matching(high) < 0:
            roots.append(brentq(matching, low, high, xtol=1e-14))
    exact = np.array(roots)**2
    assert_check('analytic half-line bound modes satisfy matching',
                 len(roots)>0 and max(abs(matching(r)) for r in roots)<1e-9,
                 omega=roots, eigenvalues=exact.tolist(),
                 decay_rates=[math.sqrt(mu**2-r*r) for r in roots])
    grids = {}
    for domain in [20., 40.]:
        for dx in [.1, .05]:
            x = np.arange(round(domain/dx)+1)*dx
            shape = np.clip((x+dx/2-length)/dx, 0., 1.)
            diagonal = 2/dx**2+mu**2*shape[1:-1]
            ev = eigh_tridiagonal(diagonal, np.full(len(diagonal)-1, -1/dx**2),
                                  select='i', select_range=(0, len(roots)-1), eigvals_only=True)
            grids[f'D{domain:g}-dx{dx:g}'] = ev.tolist()
    coarse = max(abs(np.array(grids['D40-dx0.1'])-exact))
    fine = max(abs(np.array(grids['D40-dx0.05'])-exact))
    domain_error = max(abs(np.array(grids['D40-dx0.05'])-np.array(grids['D20-dx0.05'])))
    assert_check('bound-mode eigenvalues converge to analytic continuum values',
                 fine<coarse and fine<.005, coarse_error=float(coarse), fine_error=float(fine))
    assert_check('bound-mode control is insensitive to remote wall', domain_error<1e-5,
                 domain_error=float(domain_error))
    return dict(length=length, exterior_threshold=mu**2, omega=roots,
                eigenvalues=exact.tolist(), decay_rates=[math.sqrt(mu**2-r*r) for r in roots],
                finite_grid_eigenvalues=grids, coarse_error=float(coarse), fine_error=float(fine),
                domain_error=float(domain_error))


def history_error(a, b, key='trapped'):
    if not np.allclose([r['t'] for r in a['history']], [r['t'] for r in b['history']]):
        raise ValueError('Sampling times differ')
    return max(abs(x[key]-y[key]) for x, y in zip(a['history'], b['history']))


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    attempt = OUT/'attempts'/stamp
    attempt.mkdir(parents=True)
    sources = [Path(__file__).resolve(), Path(__file__).with_name('run.py').resolve(), OUT/'protocol.md']
    source_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    for p in sources:
        shutil.copy2(p, attempt/p.name)
    payload = dict(scope='Externally controlled linear wave capture; not a full Klein-foam model',
                   created_utc=stamp, source_sha256=source_hashes,
                   versions=dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__),
                   cases={}, checks=CHECKS)
    started = time.monotonic()
    payload['calibration'] = independent_calibration()
    payload['bound_mode_control'] = bound_mode_control()
    cases = payload['cases']
    choices = [('open', dict(height=0.))]
    choices += [(f'static-h{h}', dict(height=float(h))) for h in [4, 16]]
    choices += [(f'close-h{h}-t{t}', dict(height=float(h), start=float(t)))
                for h in [4, 16] for t in [16, 20, 24, 28, 32, 36]]
    choices += [('reopen-h16-t28', dict(height=16., start=28., reopen=60.))]
    choices += [(f'refined-h16-t{t}', dict(height=16., start=float(t), dx=.05, dt=.0025))
                for t in [24, 28]]
    choices += [('time-refined-h16-t28', dict(height=16., start=28., dt=.0025)),
                ('domain-h16-t28', dict(height=16., start=28., domain=280.)),
                ('phase-h16-t28', dict(height=16., start=28., phase=1.234)),
                ('duration2-h16-t28', dict(height=16., start=28., duration=2.)),
                ('duration8-h16-t28', dict(height=16., start=28., duration=8.))]
    for name, options in choices:
        cases[name], _ = gated_run(**options)
        last = cases[name]['history'][-1]
        print(f'EVOLVED {name}: trapped160={last["trapped"]:.8f}, gate_work={last["work"]:.8f}', flush=True)
        (attempt/'results.json').write_text(json.dumps(payload, indent=2)+'\n')
    all_cases = list(cases.values())+[payload['calibration'][k] for k in ['coarse', 'fine']]
    budgets = [max(r[key] for r in all_cases) for key in
               ['budget_residual', 'core_budget_residual', 'trap_budget_residual']]
    assert_check('global energy plus signed gate work closes', budgets[0]<1e-8, max_residual=budgets[0])
    assert_check('core and trap energy plus flux and gate work close', max(budgets[1:])<1e-8,
                 core_residual=budgets[1], trap_residual=budgets[2])
    tail = max(r['max_distant_tail'] for r in all_cases)
    assert_check('no sampled outgoing tail reaches distant boundary zone', tail<1e-8, max_tail=tail)
    errors = [history_error(cases[f'close-h16-t{t}'], cases[f'refined-h16-t{t}']) for t in [24, 28]]
    assert_check('combined spatial and temporal refinement', max(errors)<.03, max_trapped_curve_errors=errors)
    base = cases['close-h16-t28']
    de = history_error(base, cases['domain-h16-t28'])
    pe = max(history_error(base, cases['phase-h16-t28'], k) for k in ['trapped', 'work', 'total'])
    assert_check('remote boundary control', de<1e-8, max_trapped_curve_error=de)
    assert_check('global phase leaves observables invariant', pe<1e-8, max_observable_error=pe)
    work_c = base['endpoint_vs_midpoint_work']
    work_f = cases['time-refined-h16-t28']['endpoint_vs_midpoint_work']
    assert_check('discrete work approaches continuum midpoint work under time refinement',
                 work_f<work_c, coarse_difference=work_c, fine_difference=work_f)
    assert_check('all frozen dynamic variants were executed', len(cases)==23, variants=len(cases))
    payload['elapsed_seconds'] = time.monotonic()-started
    payload['all_checks_passed'] = all(c['passed'] for c in CHECKS)
    (attempt/'results.json').write_text(json.dumps(payload, indent=2)+'\n')
    (attempt/'checks.json').write_text(json.dumps(CHECKS, indent=2)+'\n')
    (OUT/'latest-attempt.json').write_text(json.dumps(dict(attempt=str(attempt.relative_to(ROOT)),
                                                       all_checks_passed=payload['all_checks_passed']), indent=2)+'\n')
    if payload['all_checks_passed']:
        shutil.copy2(attempt/'results.json', OUT/'results.json')
        shutil.copy2(attempt/'checks.json', OUT/'checks.json')
    print(f'Attempt saved to {attempt}; elapsed {payload["elapsed_seconds"]:.1f}s', flush=True)
    if not payload['all_checks_passed']:
        raise SystemExit('One or more preregistered numerical checks failed; inspect preserved attempt.')


if __name__ == '__main__':
    main()
