#!/usr/bin/env python3
"""Conservative radial evolution and mechanism-removal controls."""
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np

from self_binding import ROOT,OUT,RadialGrid


def node_energies(grid,chi,u,q,p,b):
    e=grid.w*(.5*(u*u+abs(p)**2)+.25*(chi*chi-1)**2+
              .5*chi*chi*abs(q)**2+.25*b*abs(q)**4)
    edge=.5*grid.k*(np.diff(chi)**2+abs(np.diff(q))**2)
    e[:-1]+=edge/2
    e[1:]+=edge/2
    e[-1]+=.5*grid.outer*((chi[-1]-1)**2+abs(q[-1])**2)
    return e


def evolve(reference,perturb=0.,phase=0.,charge_sign=1.,vacuum=False,
           zero_charge=False,frozen_vacuum=False):
    dr=reference['dr']
    dt=.005 if dr==.1 else .0025
    grid=RadialGrid(120.,dr)
    r=grid.r
    b=reference['b']
    chi=np.interp(r,reference['profile']['r'],reference['profile']['chi'],right=1.)
    f=np.interp(r,reference['profile']['r'],reference['profile']['f'],right=0.)
    f*=1+perturb*np.exp(-(r-4)**2/4)
    u=np.zeros_like(r)
    q=f.astype(complex)*np.exp(1j*phase)
    omega=charge_sign*reference['charge']/float(grid.w@abs(q)**2)
    p=1j*omega*q
    if vacuum:
        chi[:]=1.;q[:]=0.;p[:]=0.
    if zero_charge:
        p[:]=0.
    if frozen_vacuum:
        chi[:]=1.

    def force(chi,q):
        fc=-grid.gradient(chi,1.)/grid.w-chi*(chi*chi-1)-chi*abs(q)**2
        fq=-grid.gradient(q,0.)/grid.w-chi*chi*q-b*abs(q)**2*q
        if frozen_vacuum:
            fc[:]=0.
        return fc,fq

    fchi,fq=force(chi,q)
    e0=float(node_energies(grid,chi,u,q,p,b).sum())
    charge0=float(grid.w@np.imag(np.conj(q)*p))
    scale=e0 if e0 else 1.
    charge_scale=max(1.,abs(charge0))
    max_edrift=max_qdrift=max_tail=0.
    history=[]
    steps,stride=round(80/dt),round(.2/dt)
    for step in range(steps+1):
        if step%stride==0 or step==steps:
            e=node_energies(grid,chi,u,q,p,b)
            charge_density=grid.w*np.imag(np.conj(q)*p)
            energy=float(e.sum())
            charge=float(charge_density.sum())
            max_edrift=max(max_edrift,abs(energy-e0)/scale)
            max_qdrift=max(max_qdrift,abs(charge-charge0)/charge_scale)
            max_tail=max(max_tail,float(e[r>110].sum())/scale)
            history.append(dict(t=step*dt,total_energy=energy,total_charge=charge,
                                local_energy=float(e[r<15].sum()),local_charge=float(charge_density[r<15].sum()),
                                chi0=float(chi[0]),q0_amplitude=float(abs(q[0]))))
        if step==steps:
            break
        cn=chi+dt*u+.5*dt*dt*fchi
        qn=q+dt*p+.5*dt*dt*fq
        fchin,fqn=force(cn,qn)
        u+=.5*dt*(fchi+fchin)
        p+=.5*dt*(fq+fqn)
        chi,q,fchi,fq=cn,qn,fchin,fqn
    return dict(parameters=dict(dr=dr,dt=dt,radius=120.,end=80.,b=b,perturb=perturb,
                                 phase=phase,charge_sign=charge_sign,vacuum=vacuum,
                                 zero_charge=zero_charge,frozen_vacuum=frozen_vacuum),
                initial_energy=e0,initial_charge=charge0,energy_drift=max_edrift,
                charge_drift=max_qdrift,max_distant_tail=max_tail,
                final_local_energy_fraction=history[-1]['local_energy']/scale,
                final_local_charge_fraction=history[-1]['local_charge']/charge0 if charge0 else None,
                history=history)


def curve_error(a,b,key):
    assert np.allclose([r['t'] for r in a['history']],[r['t'] for r in b['history']])
    scale=a['initial_energy'] or 1.
    return max(abs(x[key]-y[key])/scale for x,y in zip(a['history'],b['history']))


def main():
    started=time.monotonic()
    stationary=json.loads((OUT/'results.json').read_text())
    assert stationary['all_checks_passed']
    for collection in ['source_sha256','supplement_sha256']:
        for name,digest in stationary[collection].items():
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    sources=[Path(__file__).resolve(),OUT/'dynamic-protocol.md',ROOT/'code/condensate_energy/self_binding.py']
    data=dict(source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              stationary_sha256=hashlib.sha256((OUT/'results.json').read_bytes()).hexdigest(),cases={},checks=[])
    jobs=[('unperturbed','coarse',{}),('perturb2','coarse',dict(perturb=.02)),
          ('perturb5','coarse',dict(perturb=.05)),('refined','fine',{}),
          ('refined-perturb2','fine',dict(perturb=.02)),('opposite-charge','coarse',dict(charge_sign=-1.)),
          ('phase','coarse',dict(phase=1.234)),('vacuum','coarse',dict(vacuum=True)),
          ('zero-charge','coarse',dict(zero_charge=True)),('frozen-vacuum','coarse',dict(frozen_vacuum=True))]
    for name,reference,opts in jobs:
        row=evolve(stationary['reference'][reference],**opts)
        data['cases'][name]=row
        print(f'EVOLVED {name}: E0={row["initial_energy"]:.7f}, energy15={row["final_local_energy_fraction"]:.7f}, Q15={row["final_local_charge_fraction"]}, drift={row["energy_drift"]:.3g}',flush=True)
        (OUT/'dynamic-results.json').write_text(json.dumps(data,indent=2)+'\n')
    for name,limit in [('energy_drift',.001),('charge_drift',1e-8),('max_distant_tail',1e-8)]:
        value=max(r[name] for r in data['cases'].values())
        data['checks'].append(dict(name=name,passed=value<limit,maximum=value,tolerance=limit))
    base=data['cases']['unperturbed']
    errors={name:max(curve_error(base,data['cases'][name],key) for key in ['total_energy','local_energy'])
            for name in ['phase','opposite-charge']}
    data['checks'].append(dict(name='global phase and charge sign leave energy observables unchanged',passed=max(errors.values())<1e-8,errors=errors))
    errors={name:curve_error(data['cases'][name],data['cases'][refined],'local_energy')
            for name,refined in [('unperturbed','refined'),('perturb2','refined-perturb2')]}
    data['checks'].append(dict(name='local energy curves refine',passed=max(errors.values())<.02,errors=errors))
    vac=data['cases']['vacuum']
    data['checks'].append(dict(name='vacuum remains at equilibrium',passed=all(r['total_energy']==0 for r in vac['history'])))
    data['checks'].append(dict(name='all registered dynamic cases completed',passed=len(data['cases'])==10,cases=len(data['cases'])))
    data['elapsed_seconds']=time.monotonic()-started
    data['all_checks_passed']=all(r['passed'] for r in data['checks'])
    (OUT/'dynamic-results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data['checks'],indent=2),flush=True)
    if not data['all_checks_passed']:
        raise SystemExit('Dynamical qualification failed; preserve raw results.')


if __name__=='__main__':
    main()
