#!/usr/bin/env python3
"""Exact obstructions and retained identities in the recovered CPF/action routes."""
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import mpmath as mp
import numpy as np
import sympy as s
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/endpoint_audit'


def audit_microscopic_selectors():
    checks=[]
    def check(name,ok,evidence=None):
        checks.append(dict(name=name,passed=bool(ok),evidence=evidence))
        print(name,'PASS' if ok else 'FAIL',flush=True)
    snapshots=OUT/'source-snapshots'
    sources=[ROOT/'code/acs_codebase/extras/phase6_dynamics.py',
        ROOT/'papers/core_trilogy/Palatini_Gauge_Attractor.tex',
        ROOT/'papers/notes/Klein_Foam_Monad.tex',
        Path('/Users/coo-koba42/dev/TR-2026-FF06-ACS/docs/ACS_Relational_Electrodynamics_Paper.md')]
    provenance=[]
    for src in sources:
        dest=snapshots/src.name;dest.write_bytes(src.read_bytes())
        provenance.append(dict(source=str(src),snapshot=str(dest.relative_to(ROOT)),sha256=sha256(dest.read_bytes()).hexdigest()))
    (OUT/'microscopic-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    recovery=json.loads((OUT/'CPF-recovery.json').read_text())
    check('two recovered CPF payloads have identical bytes',len(recovery['objects'])==2 and len({r['sha256'] for r in recovery['objects']})==1)
    for r in recovery['objects']:
        check('recovered CPF payload hash '+str(r['offset']),sha256((ROOT/r['output']).read_bytes()).hexdigest()==r['sha256'])
    # Orientation-cover deck transformation on H1. A lifted base diffeomorphism
    # must conjugate the unique nontrivial deck map to itself.
    M=s.Matrix([[1,2],[0,1]]);D=s.diag(1,-1)
    comm=M*D-D*M
    check('proposed cover automorphism fails required deck commutation',comm==s.Matrix([[0,-4],[0,0]]))
    a,b,c,d=s.symbols('a b c d',integer=True);N=s.Matrix([[a,b],[c,d]])
    check('cover descent forces both homological off-diagonal entries to zero',N*D-D*N==s.Matrix([[0,-2*b],[2*c,0]]))
    check('unipotent trace cannot determine a unique twist',s.trace(s.Matrix([[1,2*a],[0,1]]))==2)
    # Exact source self-energy algebra, independent of its cutoff assertion.
    ee,eps,hbar,light,mass,L,R=s.symbols('e eps hbar c m L R',positive=True)
    cap=2*s.pi*eps*R/L;energy=ee**2/(8*cap);alpha=ee**2/(4*s.pi*eps*hbar*light)
    ratio=s.simplify((energy/(mass*light**2)).subs(R,hbar/(2*mass*light)))
    check('source capacitance and radius imply E over mc2 equals alpha L over two',s.simplify(ratio-alpha*L/2)==0)
    aa,xx=s.symbols('alpha x',positive=True)
    solved=s.solve(s.Eq(aa*L/2,1),1/aa)
    check('self-energy matching requires inverse alpha L over two',solved==[L/2])
    cutoff=8*s.exp(-(xx-1))
    check('CPF cutoff is inverse insertion of any desired number',s.simplify(s.log(8/cutoff)+1-xx)==0)
    mp.mp.dps=70;K=mp.mpf('137.035999171')
    source_cutoff=8*mp.exp(-(K-1));matched_cutoff=8*mp.exp(-(2*K-1))
    check('CPF displayed approximate cutoff also disagrees numerically',abs(source_cutoff/mp.mpf('2.039496e-59')-1)>.1)
    # Local surface-delta kernel is distribution-valued, absent a thickness rule.
    z,w=s.symbols('z w',real=True,positive=True)
    norm2=s.integrate(s.exp(-z*z/w**2)/(2*s.pi*w**2),(z,-s.oo,s.oo))
    check('normal Gaussian surface regulator has inverse-width squared norm',s.simplify(norm2-1/(2*s.sqrt(s.pi)*w))==0)
    check('surface kernel is not an ordinary L2 volume state in zero-width limit',s.limit(norm2,w,0,dir='+')==s.oo)
    # The printed metric itself can descend; do not reject a valid metric identity.
    u,rr,pitch=s.symbols('u R pitch',real=True)
    metric=s.Matrix([[rr**2+pitch**2/(4*s.pi**2),pitch*s.sin(u/2)/(2*s.pi)],
                     [pitch*s.sin(u/2)/(2*s.pi),1]])
    check('printed metric respects the glide pullback',s.simplify(D.T*metric.subs(u,u+2*s.pi)*D-metric)==s.zeros(2))
    check('metric determinant retains an unfixed positive radius and pitch',
          s.trigsimp(metric.det()-rr**2-pitch**2*s.cos(u/2)**2/(4*s.pi**2))==0)
    # Exact Bell calculation is valid conditional on the supplied state/operators.
    th,ph=s.symbols('theta phi',real=True)
    def op(t):return s.Matrix([[s.cos(t),s.sin(t)],[s.sin(t),-s.cos(t)]])
    bell=s.Matrix([1,0,0,1])/s.sqrt(2)
    expectation=(bell.T*s.kronecker_product(op(th),op(ph))*bell)[0]
    check('Bell correlator equals the printed cosine',s.trigsimp(expectation-s.cos(th-ph))==0)
    angles=[(0,s.pi/4,1),(0,-s.pi/4,1),(s.pi/2,s.pi/4,1),(s.pi/2,-s.pi/4,-1)]
    bell_sum=s.simplify(sum(sign*expectation.subs({th:t,ph:p}) for t,p,sign in angles))
    product=s.Matrix([1,0,0,0]);product_sum=s.simplify(sum(sign*(product.T*s.kronecker_product(op(t),op(p))*product)[0] for t,p,sign in angles))
    check('chosen Bell settings give two root two',bell_sum==2*s.sqrt(2))
    check('same operators with product state do not give same Bell value',product_sum==s.sqrt(2))
    transform=s.Matrix([[s.sqrt(3)/3,-s.Rational(1,3)],[0,s.Rational(2,3)],[-s.sqrt(3)/3,-s.Rational(1,3)]])
    check('hexagonal coordinates are rank two with a linear constraint',transform.rank()==2 and s.ones(1,3)*transform==s.zeros(1,2))
    # Gauge phase does not distinguish electromagnetically dark and bright copies.
    ax,ay,q,A,dx,dy=s.symbols('x y q A dx dy',real=True)
    covnorm=(dx+q*A*ay)**2+(dy-q*A*ax)**2
    phase_rotated=covnorm.subs({ax:-ay,ay:ax,dx:-dy,dy:dx},simultaneous=True)
    check('pi over two phase rotation preserves covariant kinetic density',s.expand(phase_rotated-covnorm)==0)
    check('claimed real-imaginary orthogonality fails for constant pi over four phase',s.sin(s.pi/4)*s.cos(s.pi/4)==s.Rational(1,2))
    rad,G,Mv,hh,mm,cc=s.symbols('r G M hbar m c',positive=True)
    speed2=G*Mv/rad+hh**2/(2*mm**2*rad**2)
    check('printed finite-visible-mass rotation speed tends to zero',s.limit(speed2,rad,s.oo)==0)
    # Immediate internal contradiction in the claimed RH/flatness formula.
    epsilon,beta=s.symbols('epsilon beta',positive=True)
    term=2*epsilon/((s.Rational(1,2)-beta)**2-epsilon**2)
    check('printed curvature summand on the critical line is nonzero',term.subs(beta,s.Rational(1,2))==-2/epsilon)
    time,gamma=s.symbols('T gamma',positive=True)
    critical_average=2/time*(s.atan((time-gamma)/epsilon)+s.atan(gamma/epsilon))
    check('actual finite critical-line summand time average vanishes',s.limit(critical_average,time,s.oo)==0)
    averages=[]
    # Independent quadrature for finite sums. This is not an all-zero interchange.
    for beta_f in [.5,.73]:
        e=.07;ga=1.3;ap=.5+e-beta_f;am=.5-e-beta_f
        for stop in [20.,200.]:
            def primitive(a,t):return np.arctan((t-ga)/a)-.5j*np.log(a*a+(t-ga)**2)
            exact=((primitive(ap,stop)-primitive(ap,0))-(primitive(am,stop)-primitive(am,0)))/stop
            def integrand(t):return 1/(ap+1j*(t-ga))-1/(am+1j*(t-ga))
            numeric=(quad(lambda t:integrand(t).real,0,stop,points=[ga],epsabs=1e-10)[0]
                     +1j*quad(lambda t:integrand(t).imag,0,stop,points=[ga],epsabs=1e-10)[0])/stop
            check('finite-summand primitive independently checked '+str((beta_f,stop)),abs(numeric-exact)<1e-10)
            averages.append(dict(beta=beta_f,T=stop,real=float(exact.real),imag=float(exact.imag),
                                 printed_value=float(2*e/((.5-beta_f)**2-e**2))))
    # Independent Lorentz connection has 24 algebraic contortion components.
    # In an orthonormal frame, T^a_mn = K^a_(n,m)-K^a_(m,n).
    pairs=list(combinations(range(4),2));ks=s.symbols('k:24');vel=s.symbols('kd:24')
    eta=[-1,1,1,1]
    def cont(a,b,mu):
        if a==b:return s.Integer(0)
        sign=1 if a<b else -1
        return eta[a]*sign*ks[4*pairs.index(tuple(sorted((a,b))))+mu]
    tors=[cont(a,n,mu)-cont(a,mu,n) for a in range(4) for mu,n in pairs]
    mapT=s.Matrix(tors).jacobian(ks)
    check('torsion-contortion map has full 24-component rank',mapT.rank()==24)
    torsion_norm=sum(eta[a]*eta[mu]*eta[n]*tors[6*a+j]**2 for a in range(4) for j,(mu,n) in enumerate(pairs))
    check('quadratic torsion term has no connection velocity kinetic matrix',
          s.hessian(torsion_norm,vel)==s.zeros(24))
    check('quadratic torsion term is algebraic degree two in contortion',s.Poly(torsion_norm,*ks).total_degree()==2)
    # The Palatini D0 K term is a boundary term because D0(e wedge e)=0.
    tt=s.symbols('t');field=s.Function('K')(tt);coef=s.symbols('C')
    boundary=coef*s.diff(field,tt)
    euler=s.diff(boundary,field)-s.diff(s.diff(boundary,s.diff(field,tt)),tt)
    check('covariantly constant Palatini coefficient leaves derivative term as boundary',euler==0)
    checks_path=OUT/'attempts/phase6_dynamics';checks_path.mkdir(exist_ok=True)
    run=subprocess.run([sys.executable,str(snapshots/'phase6_dynamics.py')],cwd=checks_path,capture_output=True,text=True,timeout=60)
    (checks_path/'stdout.txt').write_text(run.stdout);(checks_path/'stderr.txt').write_text(run.stderr)
    (checks_path/'execution.json').write_text(json.dumps(dict(returncode=run.returncode,source='source-snapshots/phase6_dynamics.py',scope='full unchanged source replay'),indent=2)+'\n')
    check('Phase6 full source replay completes',run.returncode==0)
    data=dict(checks_total=len(checks),checks_passed=sum(c['passed'] for c in checks),checks=checks,
        CPF_cutoffs=dict(inserted_inverse_alpha=str(K),source_exponential=str(source_cutoff),self_energy_consistent_exponential=str(matched_cutoff)),
        finite_curvature_averages=averages,
        qualifications=['Finite-summand averages do not justify swapping an infinite zero sum with a limit',
            'No actual zeta zero is located or excluded by the internal contradiction',
            'Torsion conclusion is for a smooth nondegenerate tetrad, independent metric-compatible connection and stated Palatini plus T-squared bulk action',
            'Extra curvature-derivative terms, singular defects or constrained teleparallel models require their own action and mode analysis',
            'Bell identity assumes the quantum state and observables; it does not derive their physics from coordinate topology',
            'Empirical claims in the CPF bibliography have not been independently authenticated by this algebra audit'])
    (OUT/'microscopic.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=data['checks_passed'],CPF_cutoffs=data['CPF_cutoffs']),indent=2))
    if data['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':audit_microscopic_selectors()
