#!/usr/bin/env python3
"""Fresh portable checks; does not reseal or overwrite archived evidence."""
import ast
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code/condensate_energy'))
sys.path.insert(0, str(ROOT / 'docs/condensate_energy/hidden_couplings/source-snapshots'))
from canonical_scalar_action import (load_exact_basis, scalar_pack, scalar_unpack,
    basis_derivatives, physical_spectrum, canonical_gauge_orbit)
from canonical_vacuum_audit import exact_neutral_restriction, bracket_and_normalization, verify_derivatives
from yukawa_model import mass
import phase6_real_boundary


def run():
    checks = []
    def check(name, passed, evidence=None):
        checks.append(dict(name=name, passed=bool(passed), evidence=evidence))
        print(('PASS ' if passed else 'FAIL ') + name, flush=True)
    def relative(a, b):
        return float(np.linalg.norm(a-b) / max(1., np.linalg.norm(b)))
    polys, quadratics, metric = load_exact_basis()
    check('17 homogeneous quartics', len(polys)==17 and all(len(m)==4 for p in polys for m in p))
    check('4 homogeneous quadratics', len(quadratics)==4 and all(len(m)==2 for p in quadratics for m in p))
    for label, result in [('normalization', bracket_and_normalization()), ('neutral', exact_neutral_restriction(polys, quadratics))]:
        for name, passed in result['checks'].items():
            check(label + ': ' + name, passed)
    phi = np.diag([1/3, 1/5]).astype(complex)
    delta = np.zeros((3,4,4), complex)
    delta[:,3,3] = np.array([1,-1j,0]) / np.sqrt(2)
    x = scalar_pack(phi, delta)
    values, gradients, hessians = basis_derivatives(polys, quadratics, x)
    # Tangent coordinates (a,b,alpha,d) of the neutral family. A raw five-entry
    # principal block incorrectly includes an independent transverse Delta variation.
    tangent = np.zeros((68,4))
    tangent[0,0]=1; tangent[6,1]=1; tangent[7,2]=1/5
    tangent[26,3]=1/np.sqrt(2); tangent[47,3]=-1/np.sqrt(2)
    spectra = []
    for k, expected in [(1/5,(56,0,0)), (0,(44,12,0)), (-1/5,(6,0,50))]:
        c = np.zeros(21)
        c[0:2] = 1
        c[6:11] = 1
        c[[6,8,9,10]] += k
        c[[11,12,13,16]] = [.01,.02,.1,.02]
        c[[17,18,20]] = [-2743/7200,-41/240,-1259/625]
        H = np.einsum('i,ijk->jk', c, hessians)
        row = physical_spectrum(H,c@gradients,x,metric)
        check(f'full stationary spectrum k={k}', (row['positive'],row['zero'],row['negative'])==expected, expected)
        check(f'tadpoles and Goldstones k={k}', row['tadpole_infinity_norm']<1e-10 and row['goldstone_ward_relative']<1e-10 and row['gauge_orbit_rank']==12)
        check(f'coordinate invariance k={k}', row['coordinate_rescaling_spectrum_error']<1e-10)
        spectra.append(tangent.T @ H @ tangent)
    check('identical neutral Hessians across stability counterfamily', max(np.max(abs(h-spectra[0])) for h in spectra)<1e-12)
    rng = np.random.default_rng(20260924)
    x = rng.normal(size=68)/5
    c = rng.normal(size=21)
    values, gradients, hessians = basis_derivatives(polys, quadratics, x)
    V, grad, H = c@values, c@gradients, np.einsum('i,ijk->jk',c,hessians)
    check('independent finite-difference derivatives', verify_derivatives(polys,quadratics,c,x,metric,'generic')['passed'])
    Y = (rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))/7
    Z = (rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))/7
    F = (rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))/7; F=(F+F.T)/2
    check('complex noncommuting flavor witness',np.linalg.norm(Y@Z-Z@Y)>.01)
    fm = mass(*scalar_unpack(x),Y,Z,F)
    orbit = canonical_gauge_orbit(x,metric)
    for a in [.4,2.3]:
        ca = np.r_[c[:17], a*a*c[17:]]
        v,g,h = basis_derivatives(polys,quadratics,a*x)
        check(f'action dilation V, gradient, Hessian a={a}', max(relative(ca@v,a**4*V),relative(ca@g,a**3*grad),relative(np.einsum('i,ijk->jk',ca,h),a*a*H))<1e-10)
        oa = canonical_gauge_orbit(a*x,metric)
        check(f'gauge mass Gram dilation a={a}', relative(oa.T@oa,a*a*(orbit.T@orbit))<1e-10)
        fa = mass(*scalar_unpack(a*x),Y,Z,F)
        check(f'48-Weyl complex flavor dilation a={a}', relative(fa,a*fm)<1e-10 and relative(np.linalg.svd(fa,compute_uv=False)**2,a*a*np.linalg.svd(fm,compute_uv=False)**2)<1e-10)
    a,m,mu = s.symbols('a m mu',positive=True)
    check('one-loop logarithm invariant under simultaneous scale change',s.simplify(s.log(a*a*m/(a*mu)**2)-s.log(m/mu**2))==0)
    source = ROOT/'docs/condensate_energy/endpoint_audit/source-snapshots/four_computations.py'
    tree=ast.parse(source.read_text());fn=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='sm_rge']
    env=dict(np=np);exec(compile(ast.Module(body=fn,type_ignores=[]),str(source),'exec'),env)
    rhs=env['sm_rge'];end=np.log(1.22e19/91.1876)
    up=solve_ivp(rhs,[0,end],[.4615,.6517,1.218,.935,.1294],method='DOP853',rtol=2e-12,atol=1e-14)
    check('conditional source RG reaches UV',up.success and up.t[-1]==end)
    uv=up.y[:,-1].copy();uv[4]=2*np.sqrt(3)/27
    def extended(t,y):
        g1,g2,g3,yt,ll=y[:5]
        derivative=(48*ll+12*yt*yt-3*(3*g2*g2+.6*g1*g1))/(16*np.pi**2)
        return np.r_[rhs(t,y[:5]),derivative*y[5]]
    down=solve_ivp(extended,[end,0],np.r_[uv,1.],method='DOP853',rtol=2e-12,atol=1e-14)
    differences=[]
    for epsilon in [-1e-5,1e-5]:
        u=uv.copy();u[4]+=epsilon
        sol=solve_ivp(rhs,[end,0],u,method='DOP853',rtol=2e-12,atol=1e-14)
        check('perturbed boundary reaches IR '+str(epsilon),sol.success and sol.t[-1]==0)
        differences.append(sol.y[4,-1])
    sensitivity=(differences[1]-differences[0])/2e-5
    check('finite running retains sensitivity',down.success and abs(sensitivity/down.y[5,-1]-1)<1e-5 and abs(sensitivity-.2088898)<1e-6,float(sensitivity))
    # Redirect only the output of the existing exact solver to temporary storage.
    old=phase6_real_boundary.OUT
    with tempfile.TemporaryDirectory() as scratch:
        destination=Path(scratch);(destination/'source-snapshots').mkdir()
        shutil.copy2(old/'source-snapshots/phase6_dynamics.py',destination/'source-snapshots/phase6_dynamics.py')
        try:
            phase6_real_boundary.OUT=destination
            with contextlib.redirect_stdout(io.StringIO()): phase6_real_boundary.solve_phase6_real_boundary()
            roots=json.loads((destination/'phase6-real-roots.json').read_text())
        finally:
            phase6_real_boundary.OUT=old
    for row in roots['checks']: check('phase6: '+row['name'],row['passed'],row.get('evidence'))
    check('exactly two real proxy roots',sum(len(b['real_roots']) for b in roots['branches'])==2)
    D=s.diag(1,-1);M=s.Matrix([[1,2],[0,1]])
    check('cover shear fails necessary deck commutation',M*D-D*M==s.Matrix([[0,-4],[0,0]]))
    alpha,L=s.symbols('alpha L',positive=True)
    check('capacitor factor of two',s.solve(s.Eq(alpha*L/2,1),alpha)==[2/L])
    eps=s.symbols('epsilon',positive=True);beta=s.symbols('beta',real=True)
    check('CPF curvature summand is nonzero on the critical line',(2*eps/((s.Rational(1,2)-beta)**2-eps**2)).subs(beta,s.Rational(1,2))==-2/eps)
    generators=[]
    for i,j in [(0,1),(0,2),(1,2)]:
        real=s.zeros(3);imag=s.zeros(3);real[i,j]=real[j,i]=s.Rational(1,2);imag[i,j]=-s.I/2;imag[j,i]=s.I/2
        generators.extend([real,imag])
    generators.extend([s.diag(1,-1,0)/2,s.diag(1,1,-2)/(2*s.sqrt(3))])
    state=s.ones(3,1)/s.sqrt(3)
    check('balanced triplet has zero means but nonzero variance',all(s.simplify((state.H*t*state)[0])==0 for t in generators[-2:]) and s.simplify(sum((state.H*t*t*state)[0] for t in generators[-2:]))==s.Rational(1,3))
    check('triplet Casimir and no invariant vector',sum((t*t for t in generators),s.zeros(3))==s.Rational(4,3)*s.eye(3) and s.Matrix.vstack(*generators).rank()==3)
    meson=s.Matrix([int(i==j) for i in range(3) for j in range(3)])/s.sqrt(3)
    check('tensor-product singlet positive control',all(s.simplify((s.kronecker_product(t,s.eye(3))-s.kronecker_product(s.eye(3),s.conjugate(t)))*meson)==s.zeros(9,1) for t in generators))
    # Exact square completion in the paper's f, chi and Noether-charge convention.
    f,g,v,lam,b=s.symbols('f g v lam b',positive=True)
    chi=s.symbols('chi',real=True)
    U=lam*(chi**2-v**2)**2/4+g*g*chi*chi*f*f/2+b*f**4/4
    square=lam*((chi**2-v**2)+g*g*f*f/lam)**2/4+(b-g**4/lam)*f**4/4
    check('FLS negative control exact square completion',s.expand(U-g*g*v*v*f*f/2-square)==0)
    return dict(scope='Fresh portable action, normalization, RG, exact-root and carrier-obstruction checks; archived PDE runs are integrity-checked, not rerun.',total=len(checks),passed=sum(c['passed'] for c in checks),checks=checks)


if __name__=='__main__':
    result=run();out=ROOT/'build/publication/science-report.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
    raise SystemExit(0 if result['total']==result['passed'] else 1)
