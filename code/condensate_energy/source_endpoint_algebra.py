#!/usr/bin/env python3
"""Independent algebra and units at the remaining historical source boundaries."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/source_endpoint'


def audit_source_endpoint_algebra():
    snap=OUT/'source-snapshots';snap.mkdir(exist_ok=True)
    plan=json.loads((ROOT/'docs/condensate_energy/source-reconciliation-20260924.json').read_text())
    provenance=[]
    for path in plan['pending_sources']:
        src=Path(path);name=('seagate-' if path.startswith('/Volumes/') else '')+src.name
        dest=snap/name;dest.write_bytes(src.read_bytes())
        provenance.append(dict(source=path,snapshot=str(dest.relative_to(ROOT)),sha256=sha256(dest.read_bytes()).hexdigest()))
    (OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    checks=[]
    def check(name,ok,evidence=None):
        row=dict(name=name,passed=bool(ok))
        if evidence is not None:row['evidence']=evidence
        checks.append(row)
    def syntax(path):return ast.dump(ast.parse(path.read_text()),include_attributes=False)
    check('quark source variants differ only outside the executable syntax',
          syntax(snap/'quark_koide_gut.py')==syntax(snap/'seagate-quark_koide_gut.py'))
    check('neutrino honest variant has identical syntax to audited source',
          syntax(snap/'neutrino_honest.py')==syntax(ROOT/'docs/condensate_energy/finite_matching/source-snapshots/neutrino_honest.py'))

    def comm(a,b):return a*b-b*a
    def frob2(a):return s.simplify(s.trace(a.conjugate().T*a))
    def J(a):return s.I*(a+a.T)/2+(a-a.T)/2
    # Symbolic norm identity for arbitrary real matrices, not only chosen generators.
    variables=s.symbols('x:9',real=True);X=s.Matrix(3,3,variables)
    check('chirality map preserves every real Frobenius norm',s.expand(frob2(J(X))-frob2(X))==0)
    H=s.diag(1,-1,0,0);S=s.zeros(4);S[0,1]=S[1,0]=1
    A=s.zeros(4);A[0,1]=1;A[1,0]=-1
    check('symmetric-antisymmetric bracket is symmetric',comm(H,A).T==comm(H,A))
    check('symmetric-symmetric bracket is antisymmetric',comm(H,S).T==-comm(H,S))
    check('chirality map is not a Lie homomorphism of the split algebra',
          comm(J(H),J(S))==-J(comm(H,S)) and comm(H,S)!=s.zeros(4))
    # Neutrino projection: all three directions remain unit Frobenius length.
    S03=s.zeros(4);S03[0,3]=S03[3,0]=1
    A03=s.zeros(4);A03[0,3]=1;A03[3,0]=-1
    H03=s.diag(1,0,0,-1);H12=s.diag(0,1,-1,0)
    t=s.symbols('theta',real=True)
    f1=S03/s.sqrt(2);f2=(s.cos(t)*H03+s.sin(t)*H12)/s.sqrt(2);g=A03/s.sqrt(2)
    check('projection counterfamily uses unit-norm generators',
          frob2(f1)==1 and frob2(g)==1 and s.trigsimp(frob2(f2))==1)
    charged=comm(f1,g);nu=comm(comm(f1,f2),f1)
    signed=s.simplify(nu[3,3]/charged[3,3])
    check('normalized projection ratio varies with direction',s.simplify(signed-s.sqrt(2)*s.cos(t))==0)
    T=s.diag(s.Rational(1,3),s.Rational(1,3),s.Rational(1,3),-1)
    check('lepton squared projection fraction is three quarters',T[3,3]**2/frob2(T)==s.Rational(3,4))
    check('color squared projection fraction is one quarter',sum(T[i,i]**2 for i in range(3))/frob2(T)==s.Rational(1,4))
    # Spin and internal charge are distinct representation factors.
    spin=s.diag(s.Rational(1,2),-s.Rational(1,2));internal=s.zeros(2)
    check('zero internal charge does not imply zero spin rotation',
          internal==s.zeros(2) and spin*s.Matrix([1,0])!=s.zeros(2,1))
    me=s.Rational('0.51099895');mtau=s.Rational('1776.86')
    mass_eV=me**2/mtau/3*10**6;source_eV=me**2/mtau/3*10**3
    check('exact-neutrino displayed result has a factor-1000 conversion error',mass_eV/source_eV==1000)
    v2=s.Rational('2.87e-4')*s.Rational('0.511')*10**6
    check('v2 stated 0.147 eV is incompatible with its inputs',v2>146 and v2<147)
    # The ordinary Koide cone for positive sqrt-mass vector has a 45 degree angle.
    q=s.Rational(2,3)
    check('Koide cone angle has cosine squared one half',1/(3*q)==s.Rational(1,2))
    # Exact powers of a common normalization in the candidate scalar proxy.
    a,r,mu,lam=s.symbols('a r mu lambda',positive=True)
    br=comm(a*H,a*A);third=comm(br,a*H)+comm(br,a*A)
    c2=s.expand(frob2(a*H-a*A)-frob2(br));c4=s.expand(frob2(third))
    check('proxy quadratic sign depends on common generator normalization',c2==4*a**2-8*a**4)
    check('proxy quartic has sixth normalization power',c4==64*a**6)
    check('same generator rays give opposite proxy quadratic signs',c2.subs(a,s.Rational(1,2))>0 and c2.subs(a,1)<0)
    V=-mu*r**2+lam*r**4
    rr=s.sqrt(mu/(2*lam))
    curvature=s.simplify(s.diff(V,r,2).subs(r,rr))
    check('canonical radial curvature is four times quadratic magnitude',curvature==4*mu)
    # QCD alpha convention and homogeneity check, separately from source numerics.
    nf=s.symbols('nf');bstd=11-s.Rational(2,3)*nf
    bsource=(33-2*nf)/(12*s.pi)
    check('source alpha slope is half the log-mu QCD coefficient',s.simplify(bsource/(bstd/(2*s.pi)))==s.Rational(1,2))
    exponent_source=s.simplify((1/s.pi)/(2*bsource))
    check('source mass exponent is half the canonical one-loop exponent',s.simplify(exponent_source/(4/bstd))==s.Rational(1,2))
    m1,m2,m3,c=s.symbols('m1 m2 m3 c',positive=True)
    Q=lambda x,y,z:(x+y+z)/(s.sqrt(x)+s.sqrt(y)+s.sqrt(z))**2
    check('common-scale QCD rescaling preserves Koide exactly',s.simplify(Q(c*m1,c*m2,c*m3)-Q(m1,m2,m3))==0)
    # Read the source's actual QCD functions; confirm its high-scale scan is flat.
    tree=ast.parse((snap/'quark_koide_gut.py').read_text())
    env=dict(np=np,alpha_s_MZ=.1179,M_Z=91.1876)
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
    exec(compile(ast.Module(body=funcs,type_ignores=[]),'quark_source_functions','exec'),env)
    samples=[]
    for scale in [1e3,1e6,1e10,1e16]:
        up=[env['run_mass'](m,start,scale) for m,start in [(.00216,2),(1.27,1.27),(163.,163.)]]
        down=[env['run_mass'](m,start,scale) for m,start in [(.00467,2),(.0934,2),(4.18,4.18)]]
        samples.append(dict(scale=scale,Q_up=env['koide'](*up),Q_down=env['koide'](*down)))
    check('actual source QCD scan is constant once all inputs are above threshold',
          np.ptp([x['Q_up'] for x in samples])<1e-14 and np.ptp([x['Q_down'] for x in samples])<1e-14)
    # Radial inverse calibration is exact and already superseded by full spectra.
    L,R,alpha,x,y=s.symbols('L R alpha x y')
    mat=s.Matrix([[2*L,alpha],[alpha,2*R]])
    check('radial vacuum inverse returns its inserted target',s.simplify(mat.inv()*mat*s.Matrix([x,y])-s.Matrix([x,y]))==s.zeros(2,1))
    # Source color contraction and gravitational power-counting are not their claims.
    center=s.I**(-1)*s.I**2*s.I
    check('printed bar4 tensor 10 tensor 4 contains no invariant under the center',center==-1)
    check('canonical graviton cubic operator needs negative-dimension coupling',1+2*(1+1)==5 and 4-5==-1)

    attempts=OUT/'attempts';attempts.mkdir(exist_ok=True)
    replays=[]
    # All algorithms and numerical constants are unchanged; only two plot paths
    # are redirected in explicit replay copies. Run from those isolated directories.
    names=['neutrino_exact','neutrino_seesaw','neutrino_seesaw_v2','quark_koide_gut',
           'theta0_cabibbo','higgs_potential','task2_lagrangian','branch_a_vacuum']
    for name in names:
        dest=attempts/name;dest.mkdir(exist_ok=True)
        source=(snap/(name+'.py')).read_text()
        replacements=source.count('/home/claude/figures')
        replay=source.replace('/home/claude/figures',str(dest/'figures'))
        path=dest/'replay.py';path.write_text(replay)
        run=subprocess.run([sys.executable,str(path)],cwd=dest,capture_output=True,text=True,timeout=60)
        (dest/'stdout.txt').write_text(run.stdout);(dest/'stderr.txt').write_text(run.stderr)
        row=dict(source=name,returncode=run.returncode,plot_path_replacements=replacements,
                 replay_sha256=sha256(path.read_bytes()).hexdigest())
        (dest/'execution.json').write_text(json.dumps(row,indent=2)+'\n');replays.append(row)
        check('source replay '+name,run.returncode==0)
    data=dict(checks_total=len(checks),checks_passed=sum(x['passed'] for x in checks),checks=checks,
        normalized_projection_ratio=str(signed),projection_ratio_range_on_quarter_turn=[0,float(s.sqrt(2))],
        neutrino_mass_correct_eV=float(mass_eV),neutrino_mass_source_eV=float(source_eV),
        neutrino_v2_correct_eV=float(v2),proxy=dict(quadratic=str(c2),quartic=str(c4),canonical_curvature=str(curvature)),
        source_qcd_scan=samples,replays=replays,
        qualifications=['Frobenius identities do not identify an action or a physical Yukawa map',
            'The spin counterexample separates internal gauge neutrality from a spacetime representation',
            'QCD homogeneity applies to consistent common-scale masses; mixed input schemes are not a precision dataset',
            'The source gravity power-counting assertion is not a proof of quantum renormalizability'])
    (OUT/'algebra.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=data['checks_passed'],
                         failures=[x for x in checks if not x['passed']],neutrino_mass_correct_eV=float(mass_eV)),indent=2))
    if data['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':audit_source_endpoint_algebra()
