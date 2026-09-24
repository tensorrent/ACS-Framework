#!/usr/bin/env python3
"""Full-action scale family and final source-normalization diagnostics."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from canonical_scalar_action import (ROOT, load_exact_basis, basis_derivatives,
    scalar_pack, scalar_unpack, canonical_gauge_orbit)
from hidden_coupling_audit import mass
from radiative_flat_modes import cw_sum

OUT=ROOT/'docs/condensate_energy/endpoint_audit'


def run_endpoint_identifiability():
    checks=[]
    def check(name,ok,evidence=None):
        checks.append(dict(name=name,passed=bool(ok),evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL',flush=True)
    snap=OUT/'source-snapshots';snap.mkdir(exist_ok=True)
    sources=[ROOT/'code/acs_codebase/extras/four_computations.py',
             ROOT/'code/acs_codebase/extras/seven_tests.py',
             Path('/Volumes/Seagate 4tb/rc7_lagrangian.py'),
             Path('/Volumes/Seagate 4tb/tensorrent_tent_io_publish/tent_io/harness/tools/palatini_colour_charges.py')]
    provenance=[]
    for src in sources:
        p=snap/src.name;p.write_bytes(src.read_bytes())
        provenance.append(dict(source=str(src),snapshot=str(p.relative_to(ROOT)),sha256=sha256(p.read_bytes()).hexdigest()))
    (OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')

    z,c,r,h,k=s.symbols('Z c r h k',positive=True)
    check('canonical field map fixes kinetic coefficient',s.simplify(z*(1/s.sqrt(z))**2)==1)
    check('canonical quartic invariant under consistent field reparameterization',
          s.simplify(4*(c*k**4)/(z*k**2)**2-4*c/z**2)==0)
    check('common action prefactor remains in physical quartic',
          s.simplify(4*(k*c)/(k*z)**2-4*c/(k*z**2))==0)
    # General homogeneous polynomials, not a neutral restriction.
    polys,quadratics,metric=load_exact_basis()
    check('all 17 invariants are homogeneous quartics',len(polys)==17 and all(len(m)==4 for p in polys for m in p))
    check('all four mass polynomials are homogeneous quadratics',len(quadratics)==4 and all(len(m)==2 for p in quadratics for m in p))
    rng=np.random.default_rng(20260924)
    x=rng.normal(size=68)/5;coeff=np.r_[rng.normal(size=17),rng.normal(size=4)]
    vals,grads,hess=basis_derivatives(polys,quadratics,x)
    V=coeff@vals;gradient=coeff@grads;H=np.einsum('i,ijk->jk',coeff,hess)
    orbit=canonical_gauge_orbit(x,metric);gauges=np.repeat([.31,.27,.35],[15,3,3])
    gram=(orbit*gauges).T@(orbit*gauges)
    Y=(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))/7
    Z=(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))/7
    F=(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))/7;F=(F+F.T)/2
    check('flavor witness is complex and noncommuting',np.linalg.norm(Y@Z-Z@Y)>.01 and np.linalg.norm(Y.imag)>.01)
    fm=mass(*scalar_unpack(x),Y,Z,F)
    def rel(a,b):return float(np.linalg.norm(a-b)/max(1.,np.linalg.norm(b)))
    scaling=[]
    for scale in [.4,2.3]:
        changed=np.r_[coeff[:17],scale**2*coeff[17:]]
        sv,sg,sh=basis_derivatives(polys,quadratics,scale*x)
        errors=dict(potential=rel(changed@sv,scale**4*V),
            gradient=rel(changed@sg,scale**3*gradient),
            hessian=rel(np.einsum('i,ijk->jk',changed,sh),scale**2*H))
        orb=canonical_gauge_orbit(scale*x,metric)
        errors['gauge_gram']=rel((orb*gauges).T@(orb*gauges),scale**2*gram)
        ff=mass(*scalar_unpack(scale*x),Y,Z,F)
        errors['fermion_mass']=rel(ff,scale*fm)
        errors['fermion_squared_singular_values']=rel(np.linalg.svd(ff,compute_uv=False)**2,
            scale**2*np.linalg.svd(fm,compute_uv=False)**2)
        for name,error in errors.items():check(name+' dilation '+str(scale),error<1e-10,error)
        scaling.append(dict(scale=scale,residuals=errors))
    # Stable neutral witness already independently qualified in family_boundary.
    witness=json.loads((ROOT/'docs/condensate_energy/family_boundary/results.json').read_text())['neutral_vacua'][0]
    beta=witness['beta'];vv=.3;dd=1.
    lam=np.zeros(17);lam[0]=1.;lam[6:11]=[1.2,1.,1.2,1.2,1.2];lam[13]=.1;lam[16]=.02
    mm=np.array(witness['quadratic_coefficients'])
    phi=np.diag([vv*np.cos(beta),vv*np.sin(beta)]).astype(complex)
    delta=np.zeros((3,4,4),complex);delta[:,3,3]=dd*np.array([1.,-1j,0.])/np.sqrt(2)
    xv=scalar_pack(phi,delta)
    va,gr,he=basis_derivatives(polys,quadratics,xv);co=np.r_[lam,mm]
    hc=np.einsum('i,ijk->jk',co,he)/np.sqrt(metric[:,None]*metric[None,:])
    scalar2=np.linalg.eigvalsh(hc)
    check('CW scale witness retains scalar stability',np.min(scalar2)>-1e-10 and np.sum(scalar2>1e-8)==56)
    orb=canonical_gauge_orbit(xv,metric)*gauges
    vector2=np.linalg.eigvalsh(orb.T@orb)
    fermion2=np.linalg.svd(mass(phi,delta,Y,Z,F),compute_uv=False)**2
    mu=.8
    cw=(cw_sum(scalar2,1.5,mu)+3*cw_sum(vector2,5/6,mu)-2*cw_sum(fermion2,1.5,mu))/(64*np.pi**2)
    for scale in [.4,2.3]:
        moved=(cw_sum(scale**2*scalar2,1.5,scale*mu)+3*cw_sum(scale**2*vector2,5/6,scale*mu)
               -2*cw_sum(scale**2*fermion2,1.5,scale*mu))/(64*np.pi**2)
        check('one-loop potential including complex flavor scales to fourth power '+str(scale),rel(moved,scale**4*cw)<1e-9)
    a,M,mu_s,c_s=s.symbols('a M mu c',positive=True)
    check('CW logarithm is exactly invariant under simultaneous scale change',
        s.simplify(s.log(a**2*M/(a*mu_s)**2)-s.log(M/mu_s**2))==0)
    check('one-loop dimensional transmutation still needs its integration scale',
        s.diff(mu_s*s.exp(-1/(2*c_s*a)),mu_s)==s.exp(-1/(2*c_s*a)))

    # Conditional source flow and its dependence on the upper quartic boundary.
    source=(snap/'four_computations.py').read_text();tree=ast.parse(source)
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='sm_rge']
    env=dict(np=np);exec(compile(ast.Module(body=funcs,type_ignores=[]),'source_sm_rge','exec'),env)
    rhs=env['sm_rge'];MZ=91.1876;MP=1.22e19;end=np.log(MP/MZ)
    initial=np.array([.4615,.6517,1.218,.935,.1294])
    up=solve_ivp(rhs,[0,end],initial,method='DOP853',rtol=2e-12,atol=1e-14)
    check('source upward RG reaches endpoint',up.success and abs(up.t[-1]-end)<1e-12)
    quartic=2*np.sqrt(3)/27;uv=up.y[:,-1].copy();uv[4]=quartic
    def sensitivity_rhs(t,state):
        g1,g2,g3,yt,ll=state[:5]
        derivative=(48*ll+12*yt**2-3*(3*g2**2+.6*g1**2))/(16*np.pi**2)
        return np.r_[rhs(t,state[:5]),derivative*state[5]]
    down=solve_ivp(sensitivity_rhs,[end,0],np.r_[uv,1.],method='DOP853',rtol=2e-12,atol=1e-14)
    other=solve_ivp(rhs,[end,0],uv,method='RK45',rtol=2e-11,atol=1e-14,max_step=.1)
    check('two RG endpoint methods agree',down.success and other.success and rel(down.y[:5,-1],other.y[:,-1])<1e-8)
    ends=[]
    for shift in [-1e-5,1e-5]:
        perturbed=uv.copy();perturbed[4]+=shift
        sol=solve_ivp(rhs,[end,0],perturbed,method='DOP853',rtol=2e-12,atol=1e-14)
        check('perturbed boundary reaches endpoint '+str(shift),sol.success and sol.t[-1]==0)
        ends.append(sol.y[4,-1])
    numerical=(ends[1]-ends[0])/2e-5;analytic=down.y[5,-1]
    check('RG variational sensitivity agrees with boundary differences',abs(numerical/analytic-1)<1e-5,
          dict(variational=float(analytic),difference=float(numerical)))
    check('finite RG flow retains nonzero boundary sensitivity',analytic>0)
    trajectories=[]
    for boundary in [.08,quartic,.18]:
        yy=uv.copy();yy[4]=boundary
        sol=solve_ivp(rhs,[end,0],yy,method='DOP853',rtol=2e-12,atol=1e-14)
        check('alternate boundary reaches endpoint '+str(boundary),sol.success and sol.t[-1]==0)
        trajectories.append(dict(lambda_UV=float(boundary),lambda_IR=float(sol.y[4,-1])))
    check('different source quartics do not become identical',np.ptp([q['lambda_IR'] for q in trajectories])>.01)
    alpha=.1179;target=(4/3)**2/(4*np.pi)
    relative=np.exp(2*np.pi/7*(1/target-1/alpha));crossing=MZ*relative
    check('source QCD crossing exactly reproduces inserted target',abs(alpha/(1+alpha*7/(2*np.pi)*np.log(relative))-target)<1e-14)
    g2cross=initial[1]/np.sqrt(1-(-19/6)*initial[1]**2*np.log(relative)/(8*np.pi**2))
    check('one-coupling crossing does not give simultaneous gauge equality',abs(g2cross-4/3)>.5)
    # Additional claims printed in the same full replay, with exact counterexamples.
    u,v,w=s.symbols('u v w',positive=True);vvv=s.Matrix([u,v,w]);rankone=vvv*vvv.T
    check('printed square-root texture is rank one',rankone.rank()==1)
    T=s.diag(s.Rational(1,2),-s.Rational(1,2))
    check('commuting curvature can have nonzero wedge-square trace',T*T-T*T==s.zeros(2) and 2*s.trace(T*T)==1)
    check('real Yukawa matrices need not have positive determinant',s.det(s.diag(-1,1,1)*s.eye(3))==-1)
    # A norm portal and diagonal chemical potentials preserve two independent phases.
    x1,y1,x2,y2,m1,m2,l1,l2,l12=s.symbols('x1 y1 x2 y2 m1 m2 l1 l2 l12',real=True)
    n1=x1*x1+y1*y1;n2=x2*x2+y2*y2
    potential=m1*n1+m2*n2+l1*n1*n1+l2*n2*n2+l12*n1*n2
    check('thermal-source norm portal preserves both independent phases',
        s.expand(-y1*s.diff(potential,x1)+x1*s.diff(potential,y1))==0 and
        s.expand(-y2*s.diff(potential,x2)+x2*s.diff(potential,y2))==0)
    zero={x1:0,y1:0,x2:0,y2:0}
    check('norm portal has no off-diagonal quadratic term in unbroken phase',
          all(s.diff(potential,p,q).subs(zero)==0 for p in [x1,y1] for q in [x2,y2]))

    attempts=OUT/'attempts';attempts.mkdir(exist_ok=True)
    replays=[]
    for name,body,scope in [('four_computations',source,'entire program'),
          ('seven_tests_kinetic','import numpy as np\n'+''.join((snap/'seven_tests.py').read_text().splitlines(True)[357:472]),
           'only normalization section: source lines 358-472')]:
        dest=attempts/name;dest.mkdir(exist_ok=True);p=dest/'replay.py';p.write_text(body)
        run=subprocess.run([sys.executable,str(p)],cwd=dest,capture_output=True,text=True,timeout=60)
        (dest/'stdout.txt').write_text(run.stdout);(dest/'stderr.txt').write_text(run.stderr)
        row=dict(source=name,scope=scope,returncode=run.returncode,replay_sha256=sha256(p.read_bytes()).hexdigest())
        (dest/'execution.json').write_text(json.dumps(row,indent=2)+'\n');replays.append(row)
        check('source replay '+name,run.returncode==0)
    result=dict(checks_total=len(checks),checks_passed=sum(c['passed'] for c in checks),checks=checks,
        general_action_scaling=scaling,complex_flavor_CW=dict(value=float(cw),mu=mu),
        source_RG=dict(upward_lambda=float(up.y[4,-1]),downward_lambda=float(down.y[4,-1]),
            derivative_IR_wrt_UV=float(analytic),tree_mass_proxy_GeV=float(np.sqrt(2*down.y[4,-1])*246.22),
            alternatives=trajectories,QCD_crossing_GeV=float(crossing),g2_at_crossing=float(g2cross)),
        replays=replays,limitations=['Dilation compares different flat-space actions, not a symmetry at fixed dimensional inputs',
            'One-loop potential scaling is not general complex-flavor finite EFT matching',
            'Historical SM running uses source inputs and truncations; mass output is a tree proxy, not a pole prediction',
            'Thermal selection rule assumes an unbroken phase and no added bilinear, condensate or charge-breaking interaction',
            'No full microscopic foam action or empirical particle identification is supplied by these diagnostics'])
    (OUT/'identifiability.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=result['checks_passed'],source_RG=result['source_RG']),indent=2))
    if result['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':run_endpoint_identifiability()
