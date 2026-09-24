#!/usr/bin/env python3
"""Energy/flux test of an explicitly added 1-D linear throat model.

This does not implement nonlinear Klein foam or derive particle rest mass.
Run with the NumPy/SciPy/Matplotlib scientific environment; outputs are separate
from the source manuscripts and previous audits. See the frozen protocol.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/acs-condensate-energy-mpl')
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.linalg import eigh_tridiagonal
from scipy.sparse import diags
from scipy.sparse.linalg import splu
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy'
CHECKS = []


def check(name, passed, **details):
    row = dict(name=name, passed=bool(passed), **details)
    CHECKS.append(row)
    print(f'{"PASS" if passed else "FAIL"}: {name}', flush=True)
    if not passed:
        (OUT/'failed-checks.json').write_text(json.dumps(CHECKS, indent=2)+'\n')
        raise AssertionError(row)


def propagation(omega, height, width):
    z = height-omega**2
    if abs(z) < 1e-14:
        return np.array([[1., width], [0., 1.]])
    k = math.sqrt(abs(z))
    if z > 0:
        c, s = math.cosh(k*width), math.sinh(k*width)
        return np.array([[c, s/k], [k*s, c]])
    c, s = math.cos(k*width), math.sin(k*width)
    return np.array([[c, s/k], [-k*s, c]])


def scattering(omega, height, width, ode=False):
    if ode and width > 0:
        generator = np.array([[0., 1.], [height-omega**2, 0.]])
        sol = solve_ivp(lambda _, y: (generator@y.reshape(2, 2)).ravel(), (0., width),
                        np.eye(2).ravel(), method='DOP853', rtol=2e-12, atol=2e-13)
        if not sol.success:
            raise RuntimeError(sol.message)
        m = sol.y[:, -1].reshape(2, 2)
    else:
        m = propagation(omega, height, width)
    # y(right)=M y(left), incident amplitude 1, reflected r, transmitted t.
    incoming = np.array([1., 1j*omega])
    backward = np.array([1., -1j*omega])
    r, t = np.linalg.solve(np.column_stack((m@backward, -incoming)), -m@incoming)
    basis = np.column_stack((incoming, backward))
    b = np.linalg.solve(basis, m@basis)
    alpha, beta = b[1, 1], b[1, 0]
    form_t = 4*omega**2/((omega*m[0, 0]+omega*m[1, 1])**2 + (omega**2*m[0, 1]-m[1, 0])**2)
    w = width*math.sqrt(max(height-omega**2, 0.))
    return dict(omega=omega, height=height, width=width, T=float(abs(t)**2), R=float(abs(r)**2),
                alpha_T=float(1/abs(alpha)**2), beta_ratio=float(abs(beta/alpha)**2),
                printed_transfer_T=float(form_t), W=w, exponential=math.exp(-2*w),
                forbidden=height>omega**2)


def stationary_audit():
    rows, errors = [], []
    for w, h, b in itertools.product([.3, .6, 1., 1.7, 2.5, 3.5], [0., .5, 1., 4., 9., 16.], [.25, .5, 1., 2., 3.]):
        row = scattering(w, h, b)
        reference = scattering(w, h, b, ode=True)
        errors.append(abs(row['T']-reference['T']))
        rows.append(row)
    check('180 independent ODE/analytic stationary transmissions agree', max(errors)<1e-8,
          cases=len(rows), max_absolute_error=max(errors))
    flux_error = max(abs(r['T']+r['R']-1) for r in rows)
    check('stationary reflected plus transmitted flux equals incoming flux', flux_error<1e-7,
          max_absolute_error=flux_error)
    identity_error = max(max(abs(r['T']-r['alpha_T']), abs(r['R']-r['beta_ratio']),
                             abs(r['T']-r['printed_transfer_T'])) for r in rows)
    check('explicit spatial convention gives T=1/|alpha|² and R=|beta/alpha|²', identity_error<1e-7,
          max_absolute_error=identity_error)
    controls = [scattering(1., 0., 2.), scattering(1., 4., 0.), scattering(1., 1., 2.)]
    check('free, zero-width and threshold cases have their exact transmissions',
          np.allclose([r['T'] for r in controls], [1., 1., .5], atol=1e-12), controls=controls)
    return dict(cases=rows, controls=controls, max_ode_error=max(errors), max_flux_error=flux_error)


def build_grid(height, width, dx, domain, smooth=0.):
    count = round(domain/dx)
    x = np.arange(count+1)*dx
    if smooth:
        potential = .5*height*(np.tanh((x-4)/smooth)-np.tanh((x-4-width)/smooth))
    else:
        # Cell-average potential resolves a fixed physical step across grid changes.
        overlap = np.maximum(0., np.minimum(x+dx/2, 4+width)-np.maximum(x-dx/2, 4.))
        potential = height*overlap/dx
    potential[[0, -1]] = 0.
    diagonal = 2/dx**2 + potential[1:-1]
    return x, potential, diagonal


def h_action(q, diagonal, dx):
    out = diagonal*q
    out[:-1] -= q[1:]/dx**2
    out[1:] -= q[:-1]/dx**2
    return out


def node_energy(q, p, potential, dx):
    qf, pf = np.pad(q, (1, 1)), np.pad(p, (1, 1))
    e = .5*dx*(abs(pf)**2 + potential*abs(qf)**2)
    spring = abs(np.diff(qf))**2/(2*dx)
    e[:-1] += spring/2
    e[1:] += spring/2
    return e


def region_energy(e, cut):
    return float(e[:cut].sum()+.5*e[cut])


def cut_flux(q, p, cut, dx):
    # Mean of the two edge currents: exact current for the half-node energy cut.
    left = -np.real(np.conj((p[cut-2]+p[cut-1])/2)*(q[cut-1]-q[cut-2])/dx)
    right = -np.real(np.conj((p[cut-1]+p[cut])/2)*(q[cut]-q[cut-1])/dx)
    return float((left+right)/2)


def midpoint_step(q, p, diagonal, dx, dt, factor):
    qm = factor.solve(q+.5*dt*p)
    pn = p-dt*h_action(qm, diagonal, dx)
    qn = 2*qm-q
    return qn, pn, qm, (p+pn)/2


def simulate(height, width, dx=.1, dt=.005, domain=120., end=80., phase=0., perturb=0., smooth=0., initial=None):
    x, potential, diagonal = build_grid(height, width, dx, domain, smooth)
    n = len(diagonal)
    factor = splu(diags([np.full(n-1, -dt**2/(4*dx**2)), 1+dt**2*diagonal/4,
                        np.full(n-1, -dt**2/(4*dx**2))], [-1, 0, 1], dtype=complex, format='csc'))
    if initial is None:
        xi = x[1:-1]
        q = np.where(xi < 4, np.sin(np.pi*xi/4)+1j*perturb*np.sin(2*np.pi*xi/4), 0.).astype(complex)
        q *= np.exp(1j*phase)
        p = -1j*np.pi/4*q
        norm = math.sqrt(node_energy(q, p, potential, dx).sum())
        q, p = q/norm, p/norm
    else:
        q, p = (v.copy() for v in initial)
    q0, p0 = q.copy(), p.copy()
    cut_core, cut_trap = round(4/dx), round((4+width)/dx)
    initial_e = node_energy(q, p, potential, dx)
    energy0 = float(initial_e.sum())
    core0, trap0 = region_energy(initial_e, cut_core), region_energy(initial_e, cut_trap)
    integrated_core = integrated_trap = 0.
    max_drift = max_core_balance = max_trap_balance = 0.
    stride, steps = round(.2/dt), round(end/dt)
    rows = []
    for step in range(steps+1):
        if step % stride == 0 or step == steps:
            e = node_energy(q, p, potential, dx)
            core, trapped = region_energy(e, cut_core), region_energy(e, cut_trap)
            total = float(e.sum())
            max_drift = max(max_drift, abs(total-energy0)/energy0)
            max_core_balance = max(max_core_balance, abs(core-core0+integrated_core)/energy0)
            max_trap_balance = max(max_trap_balance, abs(trapped-trap0+integrated_trap)/energy0)
            rows.append(dict(t=step*dt, core=core/energy0, barrier=(trapped-core)/energy0,
                             trapped=trapped/energy0, exterior=(total-trapped)/energy0, total=total/energy0,
                             outward_flux_integral=integrated_trap/energy0))
        if step == steps:
            break
        q, p, qm, pm = midpoint_step(q, p, diagonal, dx, dt, factor)
        integrated_core += dt*cut_flux(qm, pm, cut_core, dx)
        integrated_trap += dt*cut_flux(qm, pm, cut_trap, dx)
    final_e = node_energy(q, p, potential, dx)
    result = dict(height=height, width=width, dx=dx, dt=dt, domain=domain, end=end, phase=phase,
                  perturb=perturb, smooth=smooth, initial_energy=energy0,
                  energy_drift=max_drift, core_flux_balance=max_core_balance,
                  trap_flux_balance=max_trap_balance,
                  distant_tail_fraction=float(final_e[x>domain-10].sum()/energy0),
                  monochromatic_reference=scattering(np.pi/4, height, width), history=rows)
    return result, (q0, p0), (q, p), (x, final_e)


def time_solver_controls():
    # An independently integrated first-order ODE on a short interval.
    coarse, initial, final_c, _ = simulate(4., 1., dx=.1, dt=.005, domain=30., end=6.)
    fine, _, final_f, _ = simulate(4., 1., dx=.1, dt=.0025, domain=30., end=6.)
    _, _, diagonal = build_grid(4., 1., .1, 30.)
    n = len(diagonal)
    def rhs(_, y):
        return np.concatenate((y[n:], -h_action(y[:n], diagonal, .1)))
    y0 = np.concatenate(initial)
    sol = solve_ivp(rhs, (0., 6.), y0, method='DOP853', rtol=2e-10, atol=2e-12)
    if not sol.success:
        raise RuntimeError(sol.message)
    # Energy norm weights field/velocity consistently; Euclidean norm would hide high-frequency errors.
    _, potential, _ = build_grid(4., 1., .1, 30.)
    def state_error(final):
        return math.sqrt(node_energy(final[0]-sol.y[:n, -1], final[1]-sol.y[n:, -1], potential, .1).sum())
    ec, ef = state_error(final_c), state_error(final_f)
    check('independent DOP853 dynamics and midpoint converge in energy norm', ef<ec and ef<.005,
          coarse_error=ec, fine_error=ef, ode_nfev=sol.nfev)
    # A truly sealed cavity with a discrete eigenfrequency known independently.
    dx, dt, length = .05, .02, 4.
    n = round(length/dx)-1
    diagonal = np.full(n, 2/dx**2)
    ev, vec = eigh_tridiagonal(diagonal, np.full(n-1, -1/dx**2), select='i', select_range=(0, 0))
    omega = math.sqrt(ev[0])
    q = vec[:, 0].astype(complex); p = -1j*omega*q
    q0 = q.copy(); potential = np.zeros(n+2)
    e0 = node_energy(q, p, potential, dx).sum()
    factor = splu(diags([np.full(n-1, -dt**2/(4*dx**2)), 1+dt**2*diagonal/4,
                        np.full(n-1, -dt**2/(4*dx**2))], [-1, 0, 1], dtype=complex, format='csc'))
    steps = 2000
    for _ in range(steps):
        q, p, _, _ = midpoint_step(q, p, diagonal, dx, dt, factor)
    expected = q0*np.exp(-2j*steps*math.atan(omega*dt/2))
    drift = abs(node_energy(q, p, potential, dx).sum()/e0-1)
    error = float(np.linalg.norm(q-expected)/np.linalg.norm(q0))
    check('sealed cavity retains energy and matches independent discrete eigenmode phase',
          drift<1e-8 and error<1e-8, energy_drift=float(drift), phase_error=error)
    return dict(midpoint_coarse_error=ec, midpoint_fine_error=ef, sealed_energy_drift=float(drift),
                sealed_phase_error=error)


def curve_error(a, b):
    at, bt = [r['t'] for r in a['history']], [r['t'] for r in b['history']]
    if not np.allclose(at, bt):
        raise ValueError('Unmatched sampling times')
    return max(abs(x['trapped']-y['trapped']) for x, y in zip(a['history'], b['history']))


def dynamic_audit():
    cases, states, spatial = {}, {}, {}
    choices = [(0., 1.)]+list(itertools.product([1., 4., 9.], [.5, 1., 2.]))
    for h, b in choices:
        key = f'h{h:g}-b{b:g}'
        cases[key], states[key], final, spatial[key] = simulate(h, b)
        print(f'EVOLVED {key}: retained(t=80)={cases[key]["history"][-1]["trapped"]:.8f}', flush=True)
    comparisons = []
    for h, b in [(1., .5), (4., 1.), (9., 2.)]:
        fine, _, _, _ = simulate(h, b, dx=.05, dt=.0025)
        key = f'refined-h{h:g}-b{b:g}'
        cases[key] = fine
        comparisons.append(dict(case=key, max_curve_difference=curve_error(cases[f'h{h:g}-b{b:g}'], fine)))
    check('selected spatial/time refinements meet retained-energy tolerance',
          max(r['max_curve_difference'] for r in comparisons)<.02, comparisons=comparisons)
    base = cases['h4-b1']
    spatial_only, _, _, _ = simulate(4., 1., dx=.05, dt=.005)
    cases['spatial-only-h4-b1'] = spatial_only
    resolution_split = dict(spatial_change=curve_error(base, spatial_only),
                            time_change=curve_error(spatial_only, cases['refined-h4-b1']))
    check('separated central space/time refinements meet tolerance',
          max(resolution_split.values())<.02, **resolution_split)
    larger, _, _, _ = simulate(4., 1., domain=160.)
    cases['larger-domain'] = larger
    larger_error = curve_error(base, larger)
    check('larger exterior domain does not change measured retention', larger_error<1e-6,
          max_curve_difference=larger_error)
    rotated, _, _, _ = simulate(4., 1., phase=.73)
    cases['global-phase'] = rotated
    phase_error = curve_error(base, rotated)
    check('global phase rotation leaves energy observations invariant', phase_error<1e-10,
          max_curve_difference=phase_error)
    perturbed, p_initial, p_final, _ = simulate(4., 1., perturb=.01)
    cases['initial-perturbation'] = perturbed
    difference = tuple(p-b for p,b in zip(p_initial, states['h4-b1']))
    diff, _, diff_final, _ = simulate(4., 1., initial=difference)
    cases['difference-field'] = diff
    check('small initial difference has conserved positive energy', diff['energy_drift']<1e-8,
          initial_difference_energy=diff['initial_energy'], relative_drift=diff['energy_drift'])
    smooth, _, _, _ = simulate(4., 1., smooth=.15)
    cases['smooth-edge'] = smooth
    max_drift = max(c['energy_drift'] for c in cases.values())
    max_balance = max(max(c['core_flux_balance'], c['trap_flux_balance']) for c in cases.values())
    max_tail = max(c['distant_tail_fraction'] for c in cases.values())
    check('all runs conserve total field energy', max_drift<1e-8, max_relative_drift=max_drift)
    check('regional energy loss matches independently integrated net edge flux', max_balance<1e-8,
          max_relative_residual=max_balance)
    check('distant endpoint remains energetically unvisited during measurement', max_tail<1e-8,
          max_tail_fraction=max_tail)
    return dict(cases=cases, refinements=comparisons, resolution_split=resolution_split,
                perturbation_retention_change=curve_error(base, perturbed),
                smooth_edge_retention_change=curve_error(base, smooth)), spatial


def make_figure(results, spatial):
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8), layout='constrained')
    cases = results['dynamics']['cases']
    colors = ['#9dabae', '#6c8992', '#365c70', '#172d3a']
    for h, color in zip([0, 1, 4, 9], colors):
        c = cases[f'h{h}-b1']
        axes[0, 0].plot([r['t'] for r in c['history']], [r['trapped'] for r in c['history']],
                        label=f'U₀={h}', color=color)
    axes[0, 0].set(title='Energy retained inside cavity + barrier', xlabel='Time (c=1 units)', ylabel='E retained / E initial', ylim=(-.025, 1.025))
    axes[0, 0].legend(title='Barrier width b=1', fontsize=8)
    for key, color, label in [('trapped', '#365c70', 'Retained at t=80'), ('T', '#a65e38', 'Single-frequency T'), ('exponential', '#555555', 'exp(−2W)')]:
        values = []
        for b in [.5, 1, 2]:
            c = cases[f'h4-b{b:g}']
            values.append(c['history'][-1]['trapped'] if key=='trapped' else c['monochromatic_reference'][key])
        axes[0, 1].plot([.5, 1, 2], values, 'o-', color=color, label=label)
    axes[0, 1].set(title='Retention and transmission are different observables', xlabel='Barrier width b (length units)', ylabel='Dimensionless fraction', yscale='log')
    axes[0, 1].legend(fontsize=8)
    c = cases['h4-b1']
    ts = [r['t'] for r in c['history']]
    axes[1, 0].plot(ts, [r['trapped'] for r in c['history']], label='Retained', color='#365c70')
    axes[1, 0].plot(ts, [r['exterior'] for r in c['history']], label='Exterior', color='#a65e38')
    axes[1, 0].plot(ts, [r['total'] for r in c['history']], '--', label='Total', color='#555555')
    axes[1, 0].set(title='Energy budget · U₀=4, b=1', xlabel='Time (c=1 units)', ylabel='Energy / E initial')
    axes[1, 0].legend(fontsize=8)
    for name, color, label in [('h4-b1','#9dabae','dx=.1, dt=.005'),('spatial-only-h4-b1','#a65e38','dx=.05, dt=.005'),('refined-h4-b1','#365c70','dx=.05, dt=.0025')]:
        c=cases[name]
        axes[1, 1].plot([r['t'] for r in c['history']], [r['trapped'] for r in c['history']], color=color, label=label)
    axes[1, 1].set(title='Independent resolution changes · same physical barrier', xlabel='Time (c=1 units)', ylabel='E retained / E initial')
    axes[1, 1].legend(fontsize=8)
    fig.suptitle('Condensate energy audit · linear 1-D wave completion, not a full Klein-foam model', fontsize=13)
    fig.savefig(OUT/'energy-comparison.png', dpi=170)
    fig.savefig(OUT/'energy-comparison.svg')
    plt.close(fig)


def main():
    start = time.monotonic()
    sources = ['papers/notes/Klein_Foam_Monad.tex', 'papers/notes/Flag_Condensate_Nuclear_Decay.tex',
               'papers/notes/Density_Engine_Many_Worlds.tex', 'docs/Torsion_Topological_Condensation_Analysis.md',
               'docs/frontier/2026-09-11/Branch_Catalog.json', 'docs/frontier/2026-09-11/workstreams/physical/report.md',
               'code/palpha_overlap/palpha_overlap_gamow.py', 'code/acs_codebase/extras/test_conjecture_condensate_collapse.py',
               'docs/condensate_energy/protocol.md', 'code/condensate_energy/run.py']
    hashes = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}
    stationary = stationary_audit()
    solver = time_solver_controls()
    dynamics, spatial = dynamic_audit()
    legacy = subprocess.run([sys.executable, str(ROOT/'code/acs_codebase/extras/test_conjecture_condensate_collapse.py')],
                            cwd=ROOT, capture_output=True, text=True, timeout=60)
    (OUT/'projective-alignment.log').write_text(legacy.stdout+legacy.stderr)
    check('existing exact projective-alignment script completes', legacy.returncode==0,
          exit_code=legacy.returncode, interpretation='Algebraic projective alignment, not finite-energy localization.')
    results = dict(schema=1, scope='Explicit linear wave completion; no derived quantum mass or autonomous foam dynamics',
                   stationary=stationary, solver_controls=solver, dynamics=dynamics, checks=CHECKS,
                   source_hashes=hashes, versions=dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__, matplotlib=matplotlib.__version__),
                   elapsed_seconds=time.monotonic()-start)
    (OUT/'results.json').write_text(json.dumps(results, indent=2)+'\n')
    make_figure(results, spatial)
    artifacts = ['results.json', 'energy-comparison.png', 'energy-comparison.svg', 'projective-alignment.log']
    (OUT/'checks.json').write_text(json.dumps(dict(checks=CHECKS, source_hashes=hashes,
        artifact_hashes={p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in artifacts}), indent=2)+'\n')
    print(json.dumps(dict(checks_passed=len(CHECKS), elapsed_seconds=time.monotonic()-start,
                         retention_at_80={k:v['history'][-1]['trapped'] for k,v in dynamics['cases'].items()}), indent=2), flush=True)


if __name__ == '__main__':
    main()
