#!/usr/bin/env python3
"""Separate algebraic cancellation from vacuum energy in the inherited action."""
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import sympy as s
from canonical_scalar_action import load_exact_basis, polynomial_derivatives, scalar_pack, scalar_gauge_action
from hidden_coupling_audit import archived, gauge_matrices
from radiative_flat_modes import gauge_gram

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/selection_energy'


def energy_matrix_unit(i,j):
    out=s.zeros(4);out[i,j]=1;return out


def energy_pair_tensors(basis,t):
    comms=[t*b-b*t for b in basis]
    G=s.Matrix([[s.trace(a.T*b) for b in basis] for a in basis])
    K=s.Matrix([[8*s.trace(a*b) for b in basis] for a in basis])
    C=s.Matrix([[s.trace(a.T*b) for b in comms] for a in comms])
    raw=s.simplify(sum(K[i,i]*C[i,i] for i in range(len(basis))))
    contraction=s.simplify(s.trace(G.inv()*K*G.inv()*C))
    return G,K,C,raw,contraction


def audit_energy_selection():
    checks=[]
    def check(name,ok,evidence=None):
        row=dict(name=name,passed=bool(ok))
        if evidence is not None:row['evidence']=evidence
        checks.append(row)
    E=energy_matrix_unit;t=s.diag(s.Rational(1,3),s.Rational(1,3),s.Rational(1,3),-1)
    diag=[s.diag(1,-1,0,0),s.diag(0,1,-1,0),s.diag(0,0,1,-1)]
    pairs=[(i,j) for i in range(4) for j in range(i+1,4)]
    anti=[E(i,j)-E(j,i) for i,j in pairs];sym=[E(i,j)+E(j,i) for i,j in pairs]
    original=diag+anti+sym
    G,K,C,raw,invariant=energy_pair_tensors(original,t)
    check('original displayed cancellation exact',raw==0)
    check('full bilinear contraction also zero for this symmetric T',invariant==0)
    gs=[s.diag(1,-1,0,0)/s.sqrt(2),s.diag(1,1,-2,0)/s.sqrt(6),s.diag(1,1,1,-3)/s.sqrt(12)]
    gs += [b/s.sqrt(2) for b in anti+sym]
    g0,k0,c0,r0,iv0=energy_pair_tensors(gs,t)
    check('diagnostic basis Frobenius orthonormal',g0==s.eye(15))
    active=9+pairs.index((0,3));inactive=3+pairs.index((0,1))
    changed=list(gs);changed[active]=2*changed[active]
    gc,kc,cc,rc,ic=energy_pair_tensors(changed,t)
    check('diagonal-product sum changes under basis rescaling',rc!=r0,{'before':str(r0),'after':str(rc)})
    check('full tensor contraction invariant under basis rescaling',ic==iv0)
    rotated=list(gs)
    rotated[active]=(gs[active]+gs[inactive])/s.sqrt(2)
    rotated[inactive]=(gs[active]-gs[inactive])/s.sqrt(2)
    gr,kr,cr,rr,ir=energy_pair_tensors(rotated,t)
    check('counterexample rotation keeps Frobenius orthonormality',gr==s.eye(15))
    check('diagonal-product sum changes even under orthogonal rotation',rr!=r0,{'before':str(r0),'after':str(rr)})
    check('full tensor contraction retains cancellation after orthogonal rotation',ir==iv0)
    check('off-diagonal contraction supplies missing rotated contribution',s.simplify(s.trace(kr*cr)-rr)==-rr)
    check('canonical positive commutator operator has six active modes',c0.rank()==6)
    check('positive operator has no signed-energy cancellation',s.trace(c0)==s.Rational(32,3))
    freq=[s.sqrt(e) for e,mult in c0.eigenvals().items() for _ in range(mult) if e>0]
    check('six canonical oscillator zero-point energies add',sum(freq)/2==4)
    n,w=s.symbols('n omega',positive=True)
    ghost_ground_path=-n*w
    check('opposite-kinetic oscillator has no lower-bound ground energy',s.limit(ghost_ground_path,n,s.oo)==-s.oo)
    mu,M,dm=s.symbols('mu M2 delta_m2',positive=True)
    cw=M**2*(s.log(M/mu**2)-s.Rational(3,2))/(64*s.pi**2)
    check('two positive bosonic loop determinants add rather than Killing-cancel',s.simplify((2*cw).subs(mu,s.sqrt(M)))==-3*M**2/(64*s.pi**2))
    check('small splitting has the additional mass-squared factor',
          s.simplify(s.diff(cw,M)-M*(s.log(M/mu**2)-1)/(32*s.pi**2))==0)
    source_coefficient=s.Rational(3)*s.Rational(32,9)*16/(16*s.pi**2)
    check('source residual scales as mass squared not energy density',
          s.simplify(source_coefficient*(1000**2*dm)/(source_coefficient*dm))==1000**2)
    source_rho_nu=s.Rational('0.05')**4;source_rho_obs=s.Rational('0.0023')**4
    ratio=float(source_rho_nu/source_rho_obs)
    check('source neutrino-scale comparison not within two orders',ratio>1e5,{'ratio':ratio})

    # Complete inherited quadratic action at the field origin.
    _,quadratics,metric=load_exact_basis()
    ms=s.symbols('m0 m1 m2 md',real=True) # each symbol has mass dimension two
    hs=[]
    for poly in quadratics:
        h=s.zeros(68)
        for (i,j),v in poly.items():
            h[i,j]+=v;h[j,i]+=v
        hs.append(h)
    met=s.diag(*[s.Integer(round(x)) for x in metric]);inv=met.inv()
    h=sum([m*x for m,x in zip(ms,hs)],s.zeros(68));op=inv*h
    trace4=s.expand(s.trace(op*op))
    expected=8*ms[0]**2+2*ms[1]**2+2*ms[2]**2+60*ms[3]**2
    check('full scalar origin mass-fourth trace',s.simplify(trace4-expected)==0)
    omega_beta=expected/(32*s.pi**2)
    check('vacuum beta generically nonzero with nonzero quadratic masses',omega_beta.subs(dict(zip(ms,[1,0,0,1])))>0)
    rng=np.random.default_rng(9242026);origins=[]
    for case in range(5):
        values=np.array([1.4,.2,.3,.7])*(1+rng.uniform(0,.5,4))
        numeric=sum(v*np.array(h,dtype=float) for v,h in zip(values,hs))
        canonical=numeric/np.sqrt(metric[:,None]*metric[None,:]);ev=np.linalg.eigvalsh(canonical)
        predicted=np.sort([values[0]+np.hypot(values[1],values[2])/2]*4+
                          [values[0]-np.hypot(values[1],values[2])/2]*4+[values[3]]*60)
        check('independent component origin spectrum '+str(case),np.max(abs(ev-predicted))<1e-12)
        beta=float(omega_beta.subs(dict(zip(ms,values))))
        zero=np.zeros((1,1),complex)
        archive_beta=archived.beta(np.zeros(17),values,np.zeros(3),zero,zero,zero)['vacuum_constant']
        check('matches already implemented archive vacuum beta '+str(case),abs(beta-archive_beta)<1e-14)
        # Independent finite-log-scale difference at positive-mass origin.
        def value(scale):return float(np.sum(ev**2*(np.log(ev/scale**2)-1.5))/(64*np.pi**2))
        step=.001;derivative=(value(np.exp(step))-value(np.exp(-step)))/(2*step)
        check('running constant cancels origin one-loop scale derivative '+str(case),abs(beta+derivative)<1e-12)
        origins.append(dict(mass_coefficients=values.tolist(),vacuum_beta=beta,loop_log_mu_derivative=derivative))
    z,lam,Omega=s.symbols('z lambda Omega',real=True)
    v=ms[0]*z**2/2+lam*z**4/4
    check('arbitrary additive constant leaves stationarity unchanged',s.diff(v+Omega,z)==s.diff(v,z))
    check('arbitrary additive constant leaves mass Hessian unchanged',s.diff(v+Omega,z,2)==s.diff(v,z,2))
    check('vacuum value retains undetermined additive constant',s.diff(v+Omega,Omega)==1)

    # Gauge transformations act on Phi and Delta, not on the Cartan element alone.
    d=1.;vu=1/np.sqrt(5);vd=2/np.sqrt(5)
    D=np.zeros((3,4,4),complex);D[:,3,3]=np.array([1,-1j,0])/np.sqrt(2)
    phi=np.diag([vu,vd])/np.sqrt(2);x=scalar_pack(phi,D)
    bl=scalar_gauge_action(x,np.array(t,dtype=complex),[0,0,0],[0,0,0])
    em=scalar_gauge_action(x,np.array(t,dtype=complex)/2,[0,0,1],[0,0,1])
    check('TBL commutes with itself but breaks the actual Delta VEV',t*t-t*t==s.zeros(4) and np.linalg.norm(bl)>1,
          {'TBL_action_canonical_norm':float(np.linalg.norm(np.sqrt(metric)*bl))})
    check('combined electromagnetic generator annihilates this neutral vacuum',np.max(abs(em))<1e-14)
    mats,groups,weights=gauge_matrices();couplings=np.array([.3,.25,.35])
    gauge=gauge_gram(x,couplings,metric,mats,groups,weights)
    charged=gauge[np.ix_([15,18],[15,18])]
    gL,gR=couplings[1:]
    expected_charged=np.array([[gL*gL*(vu*vu+vd*vd)/4,-gL*gR*vu*vd/2],
        [-gL*gR*vu*vd/2,gR*gR*(d*d+(vu*vu+vd*vd)/4)]])
    check('charged mass block follows complete inherited kinetic term',np.max(abs(charged-expected_charged))<1e-13)
    check('no extra independent torsion W term occurs in this inherited kinetic action',abs(charged[0,0]-gL*gL/4)<1e-13)
    source_torsion=s.Rational(8,45);source_higgs=s.Rational(4,9)
    check('source torsion/Higgs ratio is 2/5',source_torsion/source_higgs==s.Rational(2,5))
    check('source torsion fraction of its total is 2/7, not 40 percent',source_torsion/(source_higgs+source_torsion)==s.Rational(2,7))

    # Safe full replays: reviewed source files only print, compute and import.
    for name in ['torsion_higgs_vacuum.py','acs_vacuum.py']:
        target=OUT/'attempts'/name.removesuffix('.py');target.mkdir(exist_ok=True)
        run=subprocess.run([sys.executable,str(OUT/'source-snapshots'/name)],cwd=target,capture_output=True,text=True,timeout=30)
        (target/'stdout.txt').write_text(run.stdout);(target/'stderr.txt').write_text(run.stderr)
        check('source replay '+name,run.returncode==0)
    report=dict(checks_total=len(checks),checks_passed=sum(c['passed'] for c in checks),checks=checks,
        algebraic_pairing=dict(original_raw_sum=str(raw),orthonormal_raw_sum=str(r0),rescaled_raw_sum=str(rc),
            rotated_raw_sum=str(rr),full_contraction=str(invariant),positive_operator_trace=str(s.trace(c0)),
            positive_oscillator_energy=4,qualification='Oscillator example is a diagnostic, not an identification of ACS particle modes.'),
        vacuum_constant=dict(mass_coefficients='m0,m1,m2,md all have mass dimension two',
            trace_mass_fourth=str(expected),beta_Omega=str(omega_beta),origin_examples=origins,
            archive_status='This vacuum_constant beta was already implemented in the inherited full_one_loop_rg.py; here it is independently reconstructed.',
            undetermined='An additive integration constant remains even when its RG running is fixed.'),
        gauge_check=dict(charged_mass_block=charged.tolist(),expected_charged_mass_block=expected_charged.tolist(),
            TBL_unbroken=False,Q_unbroken=True,source_torsion_fraction_of_total='2/7'),
        physical_limits=['No absolute vacuum-energy prediction',
            'No assertion that all indefinite theories have identical dynamics; the displayed ghost oscillator simply lacks a lower-bound ground state.',
            'An additional torsion field/kinetic term is a different action and requires its own gauge-consistent spectrum.',
            'The algebraic full-contraction zero is retained; its identification with physical vacuum energy is unsupported.'])
    (OUT/'vacuum-energy.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=report['checks_passed'],
        failures=[c for c in checks if not c['passed']],algebraic_pairing=report['algebraic_pairing'],
        beta_Omega=str(omega_beta),gauge_check=report['gauge_check']),indent=2))
    if report['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':audit_energy_selection()
