#!/usr/bin/env python3
"""Newton polish of a preserved L-BFGS energy-stop precision limitation."""
import copy
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import solve
from scipy.sparse import bmat,diags

from self_binding import ROOT,OUT,RadialGrid,energy_gradient,stability_spectrum


def hessian(z,grid,charge,b):
    c,f=z[:grid.n]/grid.sw,z[grid.n:]/grid.sw
    inertia=float(grid.w@f**2)
    omega=charge/inertia
    cross=diags(2*c*f)
    h=bmat([[grid.L+diags(3*c*c-1+f*f),cross],
            [cross,grid.L+diags(c*c+3*b*f*f-omega**2)]],format='csc').toarray()
    h[grid.n:,grid.n:]+=4*omega**2/inertia*np.outer(grid.sw*f,grid.sw*f)
    return h


def polish(row):
    result=copy.deepcopy(row)
    grid=RadialGrid(row['radius'],row['dr'])
    q,b=row['charge'],row['b']
    z=np.concatenate((grid.sw*np.array(row['profile']['chi']),grid.sw*np.array(row['profile']['f'])))
    norms=[]
    for iteration in range(12):
        e,g=energy_gradient(z,grid,q,b)
        norm=float(max(abs(g)))
        norms.append(norm)
        if norm<1e-9:
            break
        step=solve(hessian(z,grid,q,b),-g,assume_a='pos')
        for power in range(20):
            trial=z+step*2**(-power)
            et,gt=energy_gradient(trial,grid,q,b)
            if et<=e+1e-10 and max(abs(gt))<norm:
                z=trial
                break
        else:
            raise RuntimeError('Newton polish could not improve residual without increasing energy.')
    e,g=energy_gradient(z,grid,q,b)
    c,f=z[:grid.n]/grid.sw,z[grid.n:]/grid.sw
    inertia=float(grid.w@f**2)
    omega=q/inertia
    gradient=grid.gradient_energy(c,1.)+grid.gradient_energy(f,0.)
    potential=float(grid.w@(.25*(c*c-1)**2+.5*c*c*f*f+.25*b*f**4))
    rotation=.5*omega*q
    tail=float(np.sum((grid.w*f*f)[grid.r>row['radius']-5])/inertia)
    result.update(gradient_infinity_norm=float(max(abs(g))),energy=e,energy_per_charge=e/q,
                  omega=omega,gradient_energy=gradient,potential_energy=potential,rotation_energy=rotation,
                  virial_relative=abs(gradient+3*potential-3*rotation)/e,charge_tail_fraction=tail,
                  radius90=float(np.interp(.9,np.cumsum(grid.w*f*f)/inertia,grid.r)),
                  chi0=float(c[0]),f0=float(f[0]),
                  localized_below_threshold=bool(e/q<1 and omega<1 and tail<1e-6),
                  profile=dict(r=grid.r.tolist(),chi=c.tolist(),f=f.tolist()),
                  polish_gradient_history=norms,polish_iterations=len(norms)-1,
                  energy_change_from_original=e-row['energy'])
    return result


def main():
    latest=json.loads((OUT/'latest-attempt.json').read_text())
    raw_path=ROOT/latest['attempt']/'results.json'
    original=json.loads(raw_path.read_text())
    failures=[r for r in original['checks'] if not r['passed']]
    expected='reference optimizations meet stationarity tolerance'
    assert len(failures)==1 and failures[0]['name']==expected,failures
    for name,digest in original['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    result=copy.deepcopy(original)
    result['original_attempt']=str(raw_path.relative_to(ROOT))
    result['original_failures']=failures
    result['checks']=[r for r in result['checks'] if r['passed']]
    result['supplement_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in [Path(__file__).resolve(),OUT/'numerical-amendment.md']}
    for name in ['coarse','fine','domain']:
        row=polish(original['reference'][name])
        result['reference'][name]=row
        print('POLISHED',name,row['gradient_infinity_norm'],row['energy_change_from_original'],flush=True)
    continuum=result['reference']['continuum']
    grads={name:result['reference'][name]['gradient_infinity_norm'] for name in ['coarse','fine','domain']}
    result['checks'].append(dict(name='Newton-polished references meet unchanged stationarity tolerance',
                                  passed=max(grads.values())<1e-5,gradient_norms=grads))
    errors={name:abs(result['reference'][name]['energy']/continuum['energy']-1) for name in grads}
    result['checks'].append(dict(name='polished energies agree with independent continuum method',
                                  passed=max(errors.values())<.005,relative_errors=errors))
    de=abs(result['reference']['domain']['energy']/result['reference']['coarse']['energy']-1)
    result['checks'].append(dict(name='polished domain comparison',passed=de<1e-4,relative_energy_change=de))
    result['spectra']={name:stability_spectrum(result['reference'][name]) for name in ['coarse','fine']}
    result['all_checks_passed']=all(r['passed'] for r in result['checks'])
    result['qualification']='original gradient stop preserved; unchanged-tolerance Newton refinement passed'
    (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],spectra=result['spectra']),indent=2))
    if not result['all_checks_passed']:
        raise SystemExit('Polished qualification failed.')


if __name__=='__main__':
    main()
