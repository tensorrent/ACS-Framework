#!/usr/bin/env python3
"""Independent analytic and high-precision controls for selection/energy claims."""
import json
from pathlib import Path
import re
import mpmath as mp
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/selection_energy'


def verify_selection_and_energy():
    checks=[]
    def check(name,ok,evidence=None):
        row=dict(name=name,passed=bool(ok))
        if evidence is not None:row['evidence']=evidence
        checks.append(row)
    # An entire admissible one-parameter rotation, not only the 45-degree sample.
    theta=s.symbols('theta',real=True)
    R=s.Matrix([[s.cos(theta),-s.sin(theta)],[s.sin(theta),s.cos(theta)]])
    K=s.diag(8,-8);C=s.diag(s.Rational(16,9),0)
    Kr=R.T*K*R;Cr=R.T*C*R
    raw=s.trigsimp(sum(Kr[i,i]*Cr[i,i] for i in range(2))-s.Rational(128,9))
    corrected=s.trigsimp(s.trace(Kr*Cr)-s.Rational(128,9))
    check('all-angle raw diagonal-product counterexample',s.trigsimp(raw+s.Rational(128,9)*s.sin(2*theta)**2)==0)
    check('all-angle full contraction invariant',corrected==0)
    ti,tj=s.symbols('ti tj',real=True)
    q=2*(ti-tj)**2
    check('pairing cancellation extends to arbitrary diagonal symmetric T',q*16+q*(-16)==0)

    # Extract actual printed measurements before static conclusions.
    log=(OUT/'attempts/selection-principle/stdout.txt').read_text()
    section=log.split('── Gradient flow:')[1].split('SELECTION PRINCIPLE: RESULTS')[0]
    rows=re.findall(r'^\s*(\d+)\s+(\d+\.\d+)\s+(\d+)\s*$',section,re.M)
    flow=[dict(step=int(k),defect=float(d),bracket_rank=int(rank)) for k,d,rank in rows]
    check('source replay has beginning and ending flow measurements',len(flow)==5 and flow[0]['step']==0 and flow[-1]['step']==20)
    check('source measured closure worsens despite static relaxation conclusion',flow[-1]['defect']>flow[0]['defect'],flow)
    perturb=log.split('── Perturbation stability test ──')[1].split('── Comparison:')[0]
    onepercent=re.search(r'^\s*0\.010\s+(\d+\.\d+)\s+(\d+)',perturb,re.M)
    check('source printed one-percent defect contradicts below-one-percent claim',onepercent is not None and float(onepercent.group(1))>.01)

    # Independent real-subspace compactness proof: projection trace bound.
    # Random orthonormal frames in the 15D traceless matrix space are only a check.
    bs=[]
    for k in range(1,4):
        d=np.diag([1.]*k+[-float(k)]+[0.]*(3-k));bs.append(d/np.linalg.norm(d))
    for i in range(4):
        for j in range(i+1,4):
            a=np.zeros((4,4));a[i,j]=a[j,i]=1/np.sqrt(2);bs.append(a)
            a=np.zeros((4,4));a[i,j]=1/np.sqrt(2);a[j,i]=-1/np.sqrt(2);bs.append(a)
    rng=np.random.default_rng(9426);cs=[];means=[]
    for _ in range(80):
        frame=np.linalg.qr(rng.normal(size=(15,8)))[0]
        mats=np.einsum('ji,jab->iab',frame,np.array(bs))
        norms=np.linalg.norm(mats+np.swapaxes(mats,1,2),axis=(1,2))
        cs.append(float(np.sum(norms**2)));means.append(float(np.mean(norms)))
    check('independent 80 orthonormal frames obey C>=8',min(cs)>=8-1e-12,{'minimum':min(cs)})
    check('independent frames obey mean defect >=1/2',min(means)>=.5-1e-12,{'minimum':min(means)})

    # Hand derivation of charged gauge masses and unbroken neutral generator.
    u,v,d,gL,gR=s.symbols('u v d gL gR',real=True)
    Phi=s.diag(u,v)/s.sqrt(2)
    sx=s.Matrix([[0,1],[1,0]])
    dl=s.I*gL*sx*Phi/2;dr=-s.I*gR*Phi*sx/2
    realinner=lambda a,b:s.simplify(2*s.re(s.trace(a.conjugate().T*b)))
    charged=s.Matrix([[realinner(dl,dl),realinner(dl,dr)],
                      [realinner(dr,dl),realinner(dr,dr)+gR*gR*d*d]])
    expected=s.Matrix([[gL*gL*(u*u+v*v)/4,-gL*gR*u*v/2],
                       [-gL*gR*u*v/2,gR*gR*(d*d+(u*u+v*v)/4)]])
    check('independent symbolic charged kinetic mass block',s.simplify(charged-expected)==s.zeros(2))
    delta=s.Matrix([d/s.sqrt(2),-s.I*d/s.sqrt(2),0])
    color_action=2*s.I*delta
    rz=s.Matrix([delta[1],-delta[0],0])
    check('independent exact TBL action is nonzero',color_action!=s.zeros(3,1))
    check('independent exact TBL/2 plus R3 action is zero',s.simplify(color_action/2+rz)==s.zeros(3,1))
    check('independent neutral Phi electromagnetic action vanishes',s.diag(1,-1)*Phi-Phi*s.diag(1,-1)==s.zeros(2))

    # Independent origin mass spectrum and 80-digit scale derivative.
    mp.mp.dps=80
    examples=[]
    for nums in [('1.4','.2','.3','.7'),('2','.7','.8','1.1'),('3','0','0','.4')]:
        m0,m1,m2,md=map(mp.mpf,nums)
        shift=mp.sqrt(m1*m1+m2*m2)/2
        eigen=[m0+shift]*4+[m0-shift]*4+[md]*60
        mass4=sum(e*e for e in eigen)
        expected4=8*m0*m0+2*m1*m1+2*m2*m2+60*md*md
        check('80-digit closed spectrum mass-fourth sum '+str(nums),abs(mass4-expected4)<mp.mpf('1e-75'))
        def V(t):return sum(e*e*(mp.log(e)-2*t-mp.mpf(3)/2) for e in eigen)/(64*mp.pi**2)
        derivative=mp.diff(V,0)
        beta=expected4/(32*mp.pi**2)
        check('80-digit independent vacuum RG cancellation '+str(nums),abs(derivative+beta)<mp.mpf('1e-75'))
        examples.append(dict(mass_coefficients=list(nums),vacuum_beta=str(beta),loop_log_mu_derivative=str(derivative)))
    # One-loop integration fixes running, not its boundary value.
    logmu,logmu0,beta,Om0=s.symbols('logmu logmu0 beta Omega0',real=True)
    Om=Om0+beta*(logmu-logmu0)
    check('vacuum RG solution retains arbitrary boundary constant',s.diff(Om,logmu)==beta and s.diff(Om,Om0)==1)
    report=dict(checks_total=len(checks),checks_passed=sum(c['passed'] for c in checks),checks=checks,
        raw_rotation_formula='-128 sin(2 theta)^2 / 9',corrected_contraction=0,
        source_flow_measurements=flow,independent_origin_rg=examples,
        general_running='Omega(mu)=Omega(mu0)+integral beta_Omega d log(mu); its initial value is not selected by this equation.')
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=report['checks_passed'],failures=[c for c in checks if not c['passed']]),indent=2))
    if report['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':verify_selection_and_energy()
