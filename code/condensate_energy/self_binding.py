#!/usr/bin/env python3
"""3-D radial, fixed-charge two-field binding candidate with provenance."""
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
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp
from scipy.optimize import minimize
from scipy.sparse import bmat, diags
from scipy.sparse.linalg import LinearOperator, eigsh

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/self_binding'
B_SOURCE=2*math.sqrt(3)/27


class RadialGrid:
    def __init__(self,radius=30.,dr=.1):
        self.n=round(radius/dr)
        self.radius=radius
        self.dr=dr
        edges=np.linspace(0,radius,self.n+1)
        self.r=(edges[:-1]+edges[1:])/2
        self.w=4*math.pi/3*np.diff(edges**3)
        self.sw=np.sqrt(self.w)
        self.k=4*math.pi*edges[1:-1]**2/dr
        self.outer=4*math.pi*radius**2/(dr/2)
        diag=np.zeros(self.n)
        diag[:-1]+=self.k
        diag[1:]+=self.k
        diag[-1]+=self.outer
        self.diag=diag
        self.L=diags([-self.k/(self.sw[:-1]*self.sw[1:]),diag/self.w,
                      -self.k/(self.sw[:-1]*self.sw[1:])],[-1,0,1],format='csc')

    def gradient(self,u,boundary):
        dif=np.diff(u)
        grad=np.zeros_like(u)
        grad[:-1]-=self.k*dif
        grad[1:]+=self.k*dif
        grad[-1]+=self.outer*(u[-1]-boundary)
        return grad

    def gradient_energy(self,u,boundary):
        return float(.5*np.dot(self.k,abs(np.diff(u))**2)+.5*self.outer*abs(u[-1]-boundary)**2)


def energy_gradient(z,grid,charge,b):
    n=grid.n
    chi=z[:n]/grid.sw
    f=z[n:]/grid.sw
    inertia=float(grid.w@f**2)
    omega=charge/inertia
    rotation=.5*charge*omega
    potential=.25*(chi**2-1)**2+.5*chi**2*f**2+.25*b*f**4
    energy=rotation+grid.w@potential+grid.gradient_energy(chi,1.)+grid.gradient_energy(f,0.)
    gc=grid.gradient(chi,1.)+grid.w*(chi*(chi**2-1)+chi*f**2)
    gf=grid.gradient(f,0.)+grid.w*((chi**2-omega**2)*f+b*f**3)
    return float(energy),np.concatenate((gc/grid.sw,gf/grid.sw))


def seed(grid,charge,radius):
    chi=.5*(1+np.tanh(grid.r-radius))
    f=np.exp(-.5*(grid.r/radius)**2)
    f*=math.sqrt(charge/(.8*(grid.w@f**2)))
    return np.concatenate((grid.sw*chi,grid.sw*f))


def solve_fixed(charge,b,dr=.1,radius=30.,initial_radius=3.,initial_profile=None):
    grid=RadialGrid(radius,dr)
    if initial_profile is None:
        z=seed(grid,charge,initial_radius)
    else:
        r=np.array(initial_profile['r'])
        chi=np.interp(grid.r,r,initial_profile['chi'],right=1.)
        f=np.interp(grid.r,r,initial_profile['f'],right=0.)
        z=np.concatenate((grid.sw*chi,grid.sw*f))
    bounds=list(zip(np.zeros(grid.n),grid.sw))+[(0.,None)]*grid.n
    sol=minimize(energy_gradient,z,args=(grid,charge,b),jac=True,method='L-BFGS-B',
                 bounds=bounds,options=dict(gtol=1e-8,ftol=1e-14,maxiter=15000,maxls=50,maxcor=20))
    chi,f=sol.x[:grid.n]/grid.sw,sol.x[grid.n:]/grid.sw
    inertia=float(grid.w@f**2)
    omega=charge/inertia
    potential=.25*(chi**2-1)**2+.5*chi**2*f**2+.25*b*f**4
    gradient=grid.gradient_energy(chi,1.)+grid.gradient_energy(f,0.)
    rotation=.5*omega*charge
    volume=float(grid.w@potential)
    fractions=np.cumsum(grid.w*f*f)/inertia
    radius90=float(np.interp(.9,fractions,grid.r))
    outer=float(np.sum((grid.w*f*f)[grid.r>radius-5])/inertia)
    return dict(charge=charge,b=b,dr=dr,radius=radius,initial_radius=initial_radius,
                optimizer_success=bool(sol.success),message=sol.message,iterations=sol.nit,
                gradient_infinity_norm=float(np.max(abs(sol.jac))),energy=float(sol.fun),
                energy_per_charge=float(sol.fun/charge),omega=omega,
                gradient_energy=gradient,potential_energy=volume,rotation_energy=rotation,
                virial_relative=float(abs(gradient+3*volume-3*rotation)/sol.fun),
                charge_tail_fraction=outer,radius90=radius90,
                chi0=float(chi[0]),f0=float(f[0]),
                localized_below_threshold=bool(sol.fun/charge<1 and omega<1 and outer<1e-6),
                profile=dict(r=grid.r.tolist(),chi=chi.tolist(),f=f.tolist()))


def continuum_reference(profile):
    radius,charge,b=profile['radius'],profile['charge'],profile['b']
    r=np.linspace(0,radius,601)
    old=profile['profile']
    chi=np.interp(r,old['r'],old['chi'],right=1.)
    f=np.interp(r,old['r'],old['f'],right=0.)
    omega=profile['omega']
    y=np.stack((chi,np.gradient(chi,r),f,np.gradient(f,r),
                cumulative_trapezoid(4*math.pi*r*r*omega*f*f,r,initial=0.)))
    y[1,0]=y[3,0]=0.

    def rhs(r,y,p):
        c,cp,f,fp,q=y
        return np.array([cp,c*(c*c-1)+c*f*f,fp,(c*c-p[0]**2)*f+b*f**3,
                         4*math.pi*r*r*p[0]*f*f])

    def boundary(left,right,p):
        return np.array([left[1],left[3],left[4],right[0]-1,right[2],right[4]-charge])

    singular=np.diag([0.,-2.,0.,-2.,0.])
    sol=solve_bvp(rhs,boundary,r,y,p=[omega],S=singular,tol=1e-7,max_nodes=30000)
    x=np.linspace(0,radius,12001)
    c,cp,f,fp,q=sol.sol(x)
    omega=float(sol.p[0])
    w=4*math.pi*x*x
    gradient=float(simpson(.5*w*(cp*cp+fp*fp),x=x))
    volume=float(simpson(w*(.25*(c*c-1)**2+.5*c*c*f*f+.25*b*f**4),x=x))
    inertia=float(simpson(w*f*f,x=x))
    rotation=.5*omega**2*inertia
    total=gradient+volume+rotation
    return dict(success=bool(sol.success),message=sol.message,omega=omega,
                max_rms_residual=float(max(sol.rms_residuals)),nodes=len(sol.x),
                energy=total,energy_per_charge=total/charge,charge_integral=omega*inertia,
                virial_relative=abs(gradient+3*volume-3*rotation)/total,
                profile=dict(r=x[::10].tolist(),chi=c[::10].tolist(),f=f[::10].tolist()))


def stability_spectrum(profile):
    grid=RadialGrid(profile['radius'],profile['dr'])
    chi=np.array(profile['profile']['chi'])
    f=np.array(profile['profile']['f'])
    b,omega=profile['b'],profile['omega']
    chi_diag=3*chi*chi-1+f*f
    f_diag=chi*chi+3*b*f*f-omega*omega
    cross=diags(2*chi*f)
    inertia=float(grid.w@f**2)
    vector=np.concatenate((np.zeros(grid.n),grid.sw*f))
    spectra={}
    for ell in [0,1,2]:
        cent=ell*(ell+1)/grid.r**2
        h=bmat([[grid.L+diags(chi_diag+cent),cross],
                [cross,grid.L+diags(f_diag+cent)]],format='csc')
        if ell==0:
            coeff=4*omega**2/inertia
            operator=LinearOperator(h.shape,matvec=lambda z:h@z+coeff*vector*np.dot(vector,z),dtype=float)
        else:
            operator=h
        ev=eigsh(operator,k=4,which='SA',tol=1e-9,maxiter=50000,return_eigenvectors=False)
        spectra[f'amplitude_l{ell}']=sorted(ev.tolist())
    phase=grid.L+diags(chi*chi+b*f*f-omega*omega)
    spectra['phase_l0']=sorted(eigsh(phase,k=4,which='SA',tol=1e-9,maxiter=50000,return_eigenvectors=False).tolist())
    return spectra


def main():
    started=time.monotonic()
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    attempt=OUT/'attempts'/stamp
    attempt.mkdir(parents=True)
    sources=[Path(__file__).resolve(),OUT/'protocol.md']
    for p in sources:
        shutil.copy2(p,attempt/p.name)
    payload=dict(scope='Conditional three-dimensional two-field binding; no completed ACS embedding',
                 source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                 versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__),
                 optimizations={},selected={},checks=[])

    def save():
        (attempt/'results.json').write_text(json.dumps(payload,indent=2)+'\n')

    def check(name,passed,**details):
        payload['checks'].append(dict(name=name,passed=bool(passed),**details))
        print(f'{"PASS" if passed else "FAIL"}: {name}',flush=True)

    grid=RadialGrid(30.,.1)
    z=seed(grid,1000.,3.)
    rng=np.random.default_rng(23)
    direction=rng.normal(size=len(z));direction/=np.linalg.norm(direction)
    e,gradient=energy_gradient(z,grid,1000.,B_SOURCE)
    numerical=(energy_gradient(z+1e-5*direction,grid,1000.,B_SOURCE)[0]-
               energy_gradient(z-1e-5*direction,grid,1000.,B_SOURCE)[0])/2e-5
    error=abs(numerical-gradient@direction)/max(1,abs(numerical))
    check('fixed-charge gradient matches independent directional difference',error<1e-6,relative_error=error)
    for label,b in [('zero',0.),('source',B_SOURCE),('half',.5),('control',1.2)]:
        for charge in [100.,300.,1000.,3000.]:
            keys=[]
            for radius in [3.,7.]:
                key=f'{label}-Q{charge:g}-seed{radius:g}'
                row=solve_fixed(charge,b,initial_radius=radius)
                payload['optimizations'][key]=row
                keys.append(key)
                print(f'SOLVED {key}: E/Q={row["energy_per_charge"]:.7f}, omega={row["omega"]:.6f}, tail={row["charge_tail_fraction"]:.2g}, grad={row["gradient_infinity_norm"]:.2g}',flush=True)
                save()
            chosen=min(keys,key=lambda key:payload['optimizations'][key]['energy'])
            payload['selected'][f'{label}-Q{charge:g}']=chosen
    ref=payload['optimizations'][payload['selected']['source-Q1000']]
    payload['reference']={'coarse':ref}
    check('reference is localized and below free-charge threshold',ref['localized_below_threshold'],
          E_over_Q=ref['energy_per_charge'],omega=ref['omega'],tail=ref['charge_tail_fraction'])
    if not ref['localized_below_threshold']:
        save()
        raise SystemExit('Reference did not bind; no automatic change of physical parameters.')
    for name,dr,radius in [('fine',.05,30.),('domain',.1,40.)]:
        row=solve_fixed(1000.,B_SOURCE,dr=dr,radius=radius,initial_profile=ref['profile'])
        payload['reference'][name]=row
        print(f'REFERENCE {name}: E/Q={row["energy_per_charge"]:.8f} gradient={row["gradient_infinity_norm"]:.3g}',flush=True)
        save()
    continuum=continuum_reference(payload['reference']['fine'])
    payload['reference']['continuum']=continuum
    check('independent continuum boundary-value solution',continuum['success'] and continuum['max_rms_residual']<1e-5,
          residual=continuum['max_rms_residual'],message=continuum['message'])
    check('continuum fixed-charge virial balance',continuum['virial_relative']<1e-4,
          residual=continuum['virial_relative'])
    errors={name:abs(row['energy']/continuum['energy']-1) for name,row in payload['reference'].items() if name!='continuum'}
    check('independent methods and grid resolution agree in energy',max(errors.values())<.005,relative_errors=errors)
    domain_error=abs(payload['reference']['domain']['energy']/ref['energy']-1)
    check('larger radius does not create reference binding',domain_error<1e-4,relative_energy_change=domain_error)
    grads={name:row['gradient_infinity_norm'] for name,row in payload['reference'].items() if name!='continuum'}
    check('reference optimizations meet stationarity tolerance',max(grads.values())<1e-5,gradient_norms=grads)
    controls=[row['energy_per_charge'] for key,row in payload['optimizations'].items() if key.startswith('control-')]
    check('analytic no-binding control respects E >= Q',min(controls)>=1-1e-8,minimum_E_over_Q=min(controls))
    check('all frozen stationary starts executed',len(payload['optimizations'])==32,starts=len(payload['optimizations']))
    payload['spectra']={}
    for name in ['coarse','fine']:
        payload['spectra'][name]=stability_spectrum(payload['reference'][name])
        print('SPECTRA',name,json.dumps(payload['spectra'][name]),flush=True)
        save()
    payload['elapsed_seconds']=time.monotonic()-started
    payload['all_checks_passed']=all(r['passed'] for r in payload['checks'])
    save()
    (OUT/'latest-attempt.json').write_text(json.dumps(dict(attempt=str(attempt.relative_to(ROOT)),all_checks_passed=payload['all_checks_passed']),indent=2)+'\n')
    if payload['all_checks_passed']:
        shutil.copy2(attempt/'results.json',OUT/'results.json')
    print(f'Attempt {attempt}; elapsed {payload["elapsed_seconds"]:.1f}s',flush=True)
    if not payload['all_checks_passed']:
        raise SystemExit('Stationary numerical qualification failed; preserve and diagnose.')


if __name__=='__main__':
    main()
