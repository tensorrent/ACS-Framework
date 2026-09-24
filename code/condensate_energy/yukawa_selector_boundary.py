#!/usr/bin/env python3
"""Exact boundary of the archived large-tan-beta repair and Yukawa ratio claim."""
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/selection_energy'


def audit_yukawa_selector_boundary():
    checks=[]
    def check(name,ok,evidence=None):
        row=dict(name=name,passed=bool(ok))
        if evidence is not None:row['evidence']=evidence
        checks.append(row)
    t=s.symbols('t',positive=True);r=s.Rational(2,3)
    ratio=(t+r)/(1+r*t)
    check('positive tan-beta ratio derivative positive',s.simplify(s.diff(ratio,t)-(1-r*r)/(1+r*t)**2)==0)
    check('exact lower endpoint two thirds',s.limit(ratio,t,0)==r)
    check('exact upper endpoint three halves',s.limit(ratio,t,s.oo)==1/r)
    check('all positive tan beta below three halves',s.factor(1/r-ratio)==s.Rational(5,2)/(2*t+3))
    check('tan-beta fifty still near 1.5 not forty',ratio.subs(t,50)==s.Rational(152,103))
    # Relax positive relative VEV sign: cancellation can enlarge a scalar ratio.
    z=s.symbols('z',real=True);solution=s.solve(s.Eq((z+r)/(1+r*z),40),z)[0]
    check('ratio forty requires a negative relative VEV in this formula',solution<0)
    check('negative-VEV scalar solution exists but changes source domain',s.simplify((solution+r)/(1+r*solution))==40)
    k1,k2,rr=s.symbols('k1 k2 r',complex=True)
    H=s.MatrixSymbol('H',3,3)
    # Common matrix H implies simultaneous left singular vectors; complex phases
    # can modify only the overall factors, not generate a CKM angle.
    aa=k1+rr*k2;bb=k2+rr*k1
    check('matrix proportionality yields an exact common-flavor factor',s.expand(bb*aa-aa*bb)==0)
    rng=np.random.default_rng(924103);trials=[]
    for i in range(5):
        h=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));u=.3+.2j;v=.8-.1j
        A=(u+float(r)*v)*h;B=(v+float(r)*u)*h
        au=A@A.conj().T;bd=B@B.conj().T
        residual=np.linalg.norm(au@bd-bd@au)/max(1,np.linalg.norm(au)*np.linalg.norm(bd))
        _,svu,_=np.linalg.svd(A);_,svd,_=np.linalg.svd(B);ratios=svu/svd
        check('proportional matrices commute in left mass squares '+str(i),residual<1e-13)
        check('proportional matrices give same mass ratio for every generation '+str(i),np.ptp(ratios)<1e-12)
        trials.append(dict(relative_commutator=float(residual),generation_ratios=ratios.tolist()))
    # Norm-ratio countercontrol: orientation remains a real independent input.
    h=np.diag([1.,2.,4.]);z=np.array([[0.,1.,.3],[.5,0.,.4],[.7,.2,.1]])
    z*=float(r)*np.linalg.norm(h)/np.linalg.norm(z)
    a=h*.3+z*.8;b=h*.8+z*.3
    aa=a@a.T;bb=b@b.T;comm=np.linalg.norm(aa@bb-bb@aa)
    check('independent matrices can obey same norm ratio',abs(np.linalg.norm(z)/np.linalg.norm(h)-float(r))<1e-14)
    check('norm-only ratio does not force aligned flavor',comm>1e-6,{'commutator_norm':float(comm)})
    replay=OUT/'attempts/acs_higgs_wall';replay.mkdir(exist_ok=True)
    run=subprocess.run([sys.executable,str(OUT/'source-snapshots/acs_higgs_wall.py')],cwd=replay,capture_output=True,text=True,timeout=15)
    (replay/'stdout.txt').write_text(run.stdout);(replay/'stderr.txt').write_text(run.stderr)
    check('original Higgs-wall source replays',run.returncode==0)
    report=dict(checks_total=len(checks),checks_passed=sum(c['passed'] for c in checks),checks=checks,
        positive_tan_beta_ratio_range=['2/3','3/2'],source_tan_beta_50_result='152/103',
        negative_relative_vev_for_source_ratio_40=str(solution),proportional_matrix_controls=trials,
        status='Large positive tan beta cannot repair the stated proportional Yukawa hierarchy. Norm-only Yukawa constraints remain a distinct, underdetermined branch.',
        limitations=['The matrix result assumes both Dirac matrices are scalar combinations of the same H.',
            'Degenerate singular-value subspaces admit arbitrary basis choices; that does not supply physical mixing among distinct masses.',
            'A norm constraint on independent matrices is not the proportionality hypothesis.',
            'No new fit to measured quark masses or mixing is performed.'])
    (OUT/'yukawa-boundary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=report['checks_passed'],failures=[c for c in checks if not c['passed']],
        negative_relative_vev_for_ratio40=str(solution)),indent=2))
    if report['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':audit_yukawa_selector_boundary()
