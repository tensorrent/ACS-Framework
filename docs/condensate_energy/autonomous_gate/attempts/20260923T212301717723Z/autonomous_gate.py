#!/usr/bin/env python3
"""Hamiltonian wave/gate candidate: no external closure schedule or damping."""
from __future__ import annotations

import datetime
import hashlib
import itertools
import json
import math
from pathlib import Path
import shutil
import sys
import time

import numpy as np
import scipy
from scipy.integrate import solve_ivp

from run import ROOT, build_grid, cut_flux, node_energy, region_energy

OUT = ROOT/'docs/condensate_energy/autonomous_gate'
CHECKS = []


def verify(name, passed, **details):
    CHECKS.append(dict(name=name, passed=bool(passed), **details))
    print(f'{"PASS" if passed else "FAIL"}: {name}', flush=True)


def pulse_state(x, shape, dx, g, carrier, energy, center, sigma, phase):
    xi = x[1:-1]
    q = np.exp(-.5*((xi-center)/sigma)**2-1j*carrier*xi+1j*phase)
    p = (-(xi-center)/sigma**2-1j*carrier)*q
    norm = math.sqrt(energy/node_energy(q, p, g*shape, dx).sum()) if energy else 0.
    return q*norm, p*norm, 1., 0.


def evolve(g=16., mass=1., spring=1., carrier=math.pi/4, coupled=True,
           energy=1., dx=.1, dt=.005, domain=240., end=160., center=30.,
           sigma=4., phase=0., initial=None):
    x, shape, _ = build_grid(1., 1., dx, domain)
    active = np.flatnonzero(shape[1:-1])
    b = shape[1:-1][active]
    cut = round(5/dx)
    core_cut = round(4/dx)
    weights = np.ones(len(active))
    weights[active+1>cut] = 0.
    weights[active+1==cut] = .5
    bt = b*weights
    if initial is None:
        q, p, a, v = pulse_state(x, shape, dx, g, carrier, energy, center, sigma, phase)
    else:
        q, p, a, v = initial[0].copy(), initial[1].copy(), initial[2], initial[3]
    start_state = (q.copy(), p.copy(), float(a), float(v))
    e0 = node_energy(q, p, g*a*a*shape, dx)
    field0, trap0 = float(e0.sum()), region_energy(e0, cut)
    gate0 = .5*mass*v*v+.5*spring*(a-1)**2
    total0 = field0+gate0
    scale = total0 if total0>0 else 1.
    invdx2 = 1/dx**2

    def forces(q, a):
        f = -2*invdx2*q
        f[1:] += invdx2*q[:-1]
        f[:-1] += invdx2*q[1:]
        f[active] -= g*a*a*b*q[active]
        intensity = dx*float(b@abs(q[active])**2)
        av = -(spring*(a-1)+g*a*intensity)/mass if coupled else 0.
        return f, av, intensity

    f, av, intensity = forces(q, a)
    power = g*a*v*intensity
    trap_power = g*a*v*dx*float(bt@abs(q[active])**2)
    flux = cut_flux(q, p, cut, dx)
    work = positive_work = negative_work = trap_work = integrated_flux = 0.
    max_drift = max_field_residual = max_gate_residual = max_trap_residual = max_tail = 0.
    steps, stride = round(end/dt), round(.2/dt)
    history = []
    for step in range(steps+1):
        if step % stride == 0 or step == steps:
            e = node_energy(q, p, g*a*a*shape, dx)
            field = float(e.sum())
            trapped = region_energy(e, cut)
            core = region_energy(e, core_cut)
            kinetic = .5*mass*v*v
            restoring = .5*spring*(a-1)**2
            gate = kinetic+restoring
            total = field+gate
            max_drift = max(max_drift, abs(total-total0)/scale)
            max_field_residual = max(max_field_residual, abs(field-field0-work)/scale)
            max_gate_residual = max(max_gate_residual, abs(gate-gate0+work)/scale)
            max_trap_residual = max(max_trap_residual, abs(trapped-trap0+integrated_flux-trap_work)/scale)
            max_tail = max(max_tail, float(e[x>domain-10].sum())/scale)
            history.append(dict(t=step*dt, a=float(a), velocity=float(v), height=float(g*a*a),
                                field=field, trapped=trapped, core=core, barrier=trapped-core,
                                gate=gate, gate_kinetic=kinetic, gate_restoring=restoring,
                                total=total, work_on_field=work, work_positive=positive_work,
                                work_negative=negative_work, trap_work=trap_work,
                                outward_flux_integral=integrated_flux))
        if step==steps:
            break
        qn = q+dt*p+.5*dt*dt*f
        an = a+dt*v+.5*dt*dt*av
        fn, avn, intensityn = forces(qn, an)
        pn = p+.5*dt*(f+fn)
        vn = v+.5*dt*(av+avn)
        powern = g*an*vn*intensityn
        trap_powern = g*an*vn*dx*float(bt@abs(qn[active])**2)
        fluxn = cut_flux(qn, pn, cut, dx)
        dw = .5*dt*(power+powern)
        work += dw
        positive_work += max(dw, 0.)
        negative_work += min(dw, 0.)
        trap_work += .5*dt*(trap_power+trap_powern)
        integrated_flux += .5*dt*(flux+fluxn)
        q, p, a, v = qn, pn, an, vn
        f, av, intensity = fn, avn, intensityn
        power, trap_power, flux = powern, trap_powern, fluxn
    late = [r for r in history if r['t']>=max(0., end-40.)]
    summary = dict(final={key:history[-1][key] for key in
                         ['t','trapped','core','barrier','field','gate','total','height','a','work_on_field']},
                   late_window=[late[0]['t'],late[-1]['t']],
                   late_trapped_min=min(r['trapped'] for r in late),
                   late_trapped_max=max(r['trapped'] for r in late),
                   late_trapped_sample_mean=float(np.mean([r['trapped'] for r in late])),
                   late_gate_sample_mean=float(np.mean([r['gate'] for r in late])),
                   min_height=min(r['height'] for r in history),
                   max_height=max(r['height'] for r in history))
    row = dict(parameters=dict(g=g,mass=mass,spring=spring,carrier=carrier,coupled=coupled,
                               energy=energy,dx=dx,dt=dt,domain=domain,end=end,center=center,
                               sigma=sigma,phase=phase), initial_field_energy=field0,
               initial_gate_energy=gate0, initial_total_energy=total0,
               energy_drift=max_drift, field_work_residual=max_field_residual,
               gate_work_residual=max_gate_residual, trap_budget_residual=max_trap_residual,
               max_distant_tail=max_tail, summary=summary, history=history)
    return row, (q,p,float(a),float(v)), start_state


def state_error(actual, reference, g, mass, spring, dx, shape):
    q,p,a,v = actual
    qr,pr,ar,vr = reference
    # A comparison norm, not the difference of two physical Hamiltonians.
    field = node_energy(q-qr,p-pr,g*ar*ar*shape,dx).sum()
    return math.sqrt(field+.5*mass*(v-vr)**2+.5*spring*(a-ar)**2)


def calibrate():
    cfg = dict(g=16.,mass=.1,spring=.1,carrier=math.pi/4,center=12.,sigma=2.,domain=40.,end=16.)
    coarse, fc, initial = evolve(**cfg,dt=.005)
    fine, ff, _ = evolve(**cfg,dt=.0025)
    dx=.1
    _,shape,_ = build_grid(1.,1.,dx,40.)
    n=len(initial[0])
    b=shape[1:-1]

    def rhs(_, y):
        q,p = y[:n],y[n:2*n]
        a,v = float(y[2*n].real),float(y[2*n+1].real)
        f=-(2/dx**2+16*a*a*b)*q
        f[1:]+=q[:-1]/dx**2
        f[:-1]+=q[1:]/dx**2
        intensity=dx*float(b@abs(q)**2)
        av=-(.1*(a-1)+16*a*intensity)/.1
        return np.concatenate((p,f,[v,av,16*a*v*intensity]))

    y0=np.concatenate((initial[0],initial[1],[initial[2],initial[3],0j]))
    sol=solve_ivp(rhs,(0.,16.),y0,method='DOP853',rtol=2e-11,atol=2e-13)
    if not sol.success:
        raise RuntimeError(sol.message)
    reference=(sol.y[:n,-1],sol.y[n:2*n,-1],float(sol.y[2*n,-1].real),float(sol.y[2*n+1,-1].real))
    errors=[state_error(f,reference,16.,.1,.1,dx,shape) for f in [fc,ff]]
    work_ref=float(sol.y[-1,-1].real)
    work_errors=[abs(r['history'][-1]['work_on_field']-work_ref) for r in [coarse,fine]]
    verify('independent coupled ODE state convergence',errors[1]<errors[0] and errors[1]<.005,
           coarse_error=errors[0],fine_error=errors[1],ode_evaluations=sol.nfev)
    verify('independent work integral convergence',work_errors[1]<work_errors[0] and work_errors[1]<.001,
           coarse_error=work_errors[0],fine_error=work_errors[1],reference_work=work_ref)
    verify('Verlet physical energy drift decreases on time refinement',fine['energy_drift']<coarse['energy_drift'],
           coarse=coarse['energy_drift'],fine=fine['energy_drift'])
    reversed_start=(fc[0],-fc[1],fc[2],-fc[3])
    reverse, returned, _=evolve(**cfg,dt=.005,initial=reversed_start)
    target=(initial[0],-initial[1],initial[2],-initial[3])
    reversal_error=state_error(returned,target,16.,.1,.1,dx,shape)
    verify('coupled trajectory reverses without loss',reversal_error<1e-8,error=reversal_error)
    return dict(coarse=coarse,fine=fine,reverse=reverse,state_errors=errors,
                work_errors=work_errors,reference_work=work_ref,reversal_error=reversal_error)


def curve_error(a,b,key='trapped'):
    if not np.allclose([r['t'] for r in a['history']],[r['t'] for r in b['history']]):
        raise ValueError('Sampling times differ')
    scale=a['initial_total_energy'] or 1.
    return max(abs(x[key]-y[key])/scale for x,y in zip(a['history'],b['history']))


def main():
    started=time.monotonic()
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    attempt=OUT/'attempts'/stamp
    attempt.mkdir(parents=True)
    sources=[Path(__file__).resolve(),Path(__file__).with_name('run.py').resolve(),OUT/'protocol.md']
    for p in sources:
        shutil.copy2(p,attempt/p.name)
    data=dict(scope='Candidate Hamiltonian gate; no full foam dynamics or derived particle mass',
              created_utc=stamp,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__),
              cases={},checks=CHECKS)
    cases=data['cases']

    def save():
        (attempt/'results.json').write_text(json.dumps(data,indent=2)+'\n')

    def run_case(name,cfg):
        row,_,_=evolve(**cfg)
        cases[name]=row
        last=row['summary']['final']
        print(f'EVOLVED {name}: field_trap={last["trapped"]:.6f} gate={last["gate"]:.6f} drift={row["energy_drift"]:.2g}',flush=True)
        save()

    data['calibration']=calibrate()
    save()
    carriers={'low':math.pi/8,'middle':math.pi/4,'high':math.pi/2}
    base_names={}
    for label,k in carriers.items():
        names=[]
        for g,m,s in itertools.product([4.,16.],[.1,1.,10.],[.1,1.,10.]):
            name=f'{label}-g{g:g}-M{m:g}-K{s:g}'
            run_case(name,dict(g=g,mass=m,spring=s,carrier=k))
            names.append(name)
        base_names[label]=names
        for g in [0.,4.,16.]:
            run_case(f'{label}-fixed-g{g:g}',dict(g=g,carrier=k,coupled=False))
    reference='middle-g16-M1-K1'
    for e in [.25,4.]:
        run_case(f'reference-energy{e:g}',dict(energy=e))
    run_case('reference-phase',dict(phase=1.234))
    run_case('reference-domain',dict(domain=280.))
    refine_pairs=[]
    for base in ['middle-g4-M1-K1','middle-g16-M0.1-K0.1']:
        cfg=cases[base]['parameters'].copy()
        cfg.update(dx=.05,dt=.0025)
        name=f'refined-{base}'
        run_case(name,cfg)
        refine_pairs.append((base,name))
    selected={}
    for label,names in base_names.items():
        base=max(names,key=lambda name:cases[name]['summary']['final']['trapped'])
        selected[label]=base
        cfg=cases[base]['parameters'].copy()
        cfg.update(dx=.05,dt=.0025)
        name=f'selected-refined-{label}'
        run_case(name,cfg)
        refine_pairs.append((base,name))
        cfg=cases[base]['parameters'].copy()
        cfg.update(domain=560.,end=480.)
        run_case(f'selected-long-{label}',cfg)
    run_case('vacuum',dict(energy=0.,end=16.))
    data['selected_by_field_retention']=selected
    data['refinement_pairs']=refine_pairs
    data['base_names']=base_names
    all_runs=list(cases.values())+[data['calibration'][key] for key in ['coarse','fine','reverse']]
    for key in ['energy_drift','field_work_residual','gate_work_residual','trap_budget_residual']:
        value=max(r[key] for r in all_runs)
        verify(f'{key} within registered tolerance',value<.001,max_residual=value)
    tail=max(r['max_distant_tail'] for r in all_runs)
    verify('distant boundary zone remains negligible',tail<1e-8,max_tail=tail)
    refinement=[]
    for base,refined in refine_pairs:
        errors={key:curve_error(cases[base],cases[refined],key) for key in ['trapped','gate','height']}
        refinement.append(dict(base=base,refined=refined,errors=errors))
    verify('all designated and selected trapped curves refine',max(r['errors']['trapped'] for r in refinement)<.03,
           comparisons=refinement)
    pe=max(curve_error(cases[reference],cases['reference-phase'],key) for key in ['trapped','gate','total'])
    de=max(curve_error(cases[reference],cases['reference-domain'],key) for key in ['trapped','gate','total'])
    verify('global phase invariance',pe<1e-8,max_observable_error=pe)
    verify('dynamic larger-domain invariance',de<1e-8,max_observable_error=de)
    vac=max(abs(r[key]) for r in cases['vacuum']['history'] for key in ['field','gate','velocity'])
    vac=max(vac,max(abs(r['a']-1) for r in cases['vacuum']['history']))
    verify('vacuum remains at zero-energy equilibrium',vac<1e-12,max_deviation=vac)
    old=json.loads((ROOT/'docs/condensate_energy/capture-results.json').read_text())
    # The previous file's dictionary layout is read explicitly below at run time.
    old_case=old['cases']['h4']
    new_hist=[r for r in cases['middle-fixed-g4']['history'] if r['t']<=80.]
    static_error=max(abs(x['trapped']-y['trapped']) for x,y in zip(new_hist,old_case['history'],strict=True))
    verify('fixed barrier agrees with prior independent midpoint integrator',static_error<.001,
           max_trapped_curve_error=static_error)
    verify('all registered variants executed',len(cases)==76,variants=len(cases))
    data['elapsed_seconds']=time.monotonic()-started
    data['all_checks_passed']=all(r['passed'] for r in CHECKS)
    save()
    (attempt/'checks.json').write_text(json.dumps(CHECKS,indent=2)+'\n')
    (OUT/'latest-attempt.json').write_text(json.dumps(dict(attempt=str(attempt.relative_to(ROOT)),all_checks_passed=data['all_checks_passed']),indent=2)+'\n')
    if data['all_checks_passed']:
        shutil.copy2(attempt/'results.json',OUT/'results.json')
        shutil.copy2(attempt/'checks.json',OUT/'checks.json')
    print(f'Attempt {attempt}; elapsed {data["elapsed_seconds"]:.1f}s',flush=True)
    if not data['all_checks_passed']:
        raise SystemExit('Registered numerical check failed; preserved attempt requires qualification.')


if __name__=='__main__':
    main()
