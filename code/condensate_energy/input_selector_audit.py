#!/usr/bin/env python3
"""Exact/source-specific tests of archived ACS input-selection proposals."""
import ast
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.linalg import eigvalsh
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy/input_closure'
SNAP = OUT / 'source-snapshots'


def bracket_selector(a, b):
    return a*b - b*a


def inner_selector(a, b):
    return s.trace(a.T*b)


def array_selector(a):
    return np.array(a, dtype=float)


def basis_selector():
    out = [s.diag(1,-1,0,0), s.diag(0,1,-1,0), s.diag(1,1,-1,-1)]
    for sign in [1, -1]:
        for i in range(4):
            for j in range(i+1, 4):
                b = s.zeros(4); b[i,j] = 1; b[j,i] = sign; out.append(b)
    return out


def invariant_selector(f, g):
    c = bracket_selector(f, g)
    d = bracket_selector(c, f) + bracket_selector(c, g)
    return inner_selector(f,f)-inner_selector(c,c)+inner_selector(d,d)


def derivatives_selector(f, g, basis):
    c = bracket_selector(f,g)
    d = bracket_selector(c,f)+bracket_selector(c,g)
    ci = [bracket_selector(b,g) for b in basis]
    di = [bracket_selector(x,f)+bracket_selector(c,b)+bracket_selector(x,g)
          for x,b in zip(ci,basis)]
    grad = s.Matrix([2*inner_selector(f,b)-2*inner_selector(c,x)+2*inner_selector(d,y)
                     for b,x,y in zip(basis,ci,di)])
    hess = s.Matrix(len(basis),len(basis),lambda i,j:
        2*inner_selector(basis[i],basis[j])-2*inner_selector(ci[i],ci[j])
        +2*inner_selector(di[i],di[j])+2*inner_selector(d,
            bracket_selector(ci[i],basis[j])+bracket_selector(ci[j],basis[i])))
    return invariant_selector(f,g), grad, hess


def extracted_selector_functions(path, names):
    """Only named, reviewed function bodies; no source top-level search or disk write."""
    tree = ast.parse(path.read_text())
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in body} == set(names)
    ns = {'np': np}
    exec(compile(ast.Module(body=body,type_ignores=[]),str(path),'exec'),ns)
    return ns


def run_selector_audit():
    checks=[]; data={}
    def check(name, passed, evidence=None):
        row=dict(name=name,passed=bool(passed))
        if evidence is not None: row['evidence']=evidence
        checks.append(row)

    bs=basis_selector(); sym=bs[:9]
    f=s.diag(1,-1,0,0); f[0,1]=s.Rational(3,10)
    g=s.Rational(3,10)*s.diag(0,1,-1,0); g[1,2]=1
    l2=bracket_selector(f,g); ls=[f,l2,bracket_selector(l2,f)+bracket_selector(l2,g)]
    # A basis of all real 4x4 matrices and all real symmetric matrices.
    units=[]
    for i in range(4):
        for j in range(4):
            e=s.zeros(4); e[i,j]=1; units.append(e)
    symmetric=sym+[s.eye(4)]
    zero_pairs=[s.re(s.trace((s.I*(l+l.T)/2+(l-l.T)/2)*v))
                for l in units for v in symmetric]
    check('real projection identically zero on full real matrix x symmetric matrix domain',
          all(x==0 for x in zero_pairs), {'basis_pairs':len(zero_pairs)})
    source=extracted_selector_functions(SNAP/'koide_from_vev.py',
        ['bracket','chirality_map','vev_projected_yukawa'])
    rng=np.random.default_rng(20260924)
    random_errors=[]
    for _ in range(100):
        ll=rng.normal(size=(4,4)); v=rng.normal(size=(4,4)); v=(v+v.T)/2
        random_errors.append(abs(source['vev_projected_yukawa'](ll,v)))
    check('archived real projection agrees with exact zero identity',max(random_errors)<2e-14,
          {'trials':100,'max_absolute_roundoff':max(random_errors)})
    # Explicitly different hypothesis: Im Tr(J(L) V), not the source's Re.
    p=s.Matrix([[inner_selector((l+l.T)/2,v) for v in sym] for l in ls])
    check('imaginary repair has rank three',p.rank()==3,{'rank':p.rank(),'nullity':9-p.rank()})
    gram9=s.Matrix([[inner_selector(a,b) for b in sym] for a in sym])
    right=gram9.inv()*p.T*(p*gram9.inv()*p.T).inv()
    check('repaired projection exact right inverse',p*right==s.eye(3))
    examples=[]
    for yy in [(1,2,3),(1,10,100),(5,5,1)]:
        y=s.Matrix(yy); c=right*y; norm2=(c.T*gram9*c)[0]
        normalized=c/s.sqrt(norm2); observed=p*normalized
        check('repair fits ratios '+str(yy), all(s.simplify(observed[i]/observed[0]-y[i]/y[0])==0 for i in range(3)))
        check('repair VEV unit norm '+str(yy), s.simplify((normalized.T*gram9*normalized)[0]-1)==0)
        examples.append(dict(target_ratios=list(yy),observed_ratios=[float(x/observed[0]) for x in observed],
                             raw_vev_norm_squared=str(norm2)))
    data['projection']=dict(exact_real_projection=0,repaired_matrix=[[str(x) for x in row] for row in p.tolist()],
        repaired_rank=int(p.rank()),repaired_nullity=9-p.rank(),examples=examples,
        qualification='Imaginary projection is a changed hypothesis; it fits arbitrary nonzero ratios and still needs a VEV-selection law and a field-representation map.')

    # Exact source point, derivatives in source's 15-dimensional basis.
    gv=s.Rational(61,50)*g
    iv, grad, hi=derivatives_selector(f,gv,bs)
    hv=2*grad*grad.T+2*iv*hi
    metric=s.Matrix([[inner_selector(a,b) for b in bs] for a in bs])
    h=array_selector(hi); hvn=array_selector(hv); gn=array_selector(grad).ravel(); gm=array_selector(metric)
    check('claimed trough is not DeltaI zero',iv!=0,{'DeltaI_exact':str(iv),'DeltaI':float(iv)})
    check('claimed point not stationary for I or I squared',grad!=s.zeros(15,1) and iv!=0,
          {'gradient_I_norm':float(np.linalg.norm(gn)),'gradient_I_squared_norm':float(np.linalg.norm(2*float(iv)*gn))})
    fn=array_selector(f); bsn=np.array([array_selector(b) for b in bs])
    f_cov=np.array([float(inner_selector(f,b)) for b in bs])
    grad_tangent=gn-f_cov*(f_cov@np.linalg.solve(gm,gn))/(f_cov@np.linalg.solve(gm,f_cov))
    check('normalizing Form does not make point stationary',np.linalg.norm(grad_tangent)>1e-8,
          {'tangent_gradient_covector_norm':float(np.linalg.norm(grad_tangent))})
    check('squared potential has a lower point at Form zero',invariant_selector(s.zeros(4),gv)==0 and iv**2>0)
    check('source Hessian differs from squared-potential Hessian',hi!=hv)
    check('source basis has nonidentity positive metric',metric!=s.eye(15) and np.min(eigvalsh(gm))>0)
    q=s.symbols('q',real=True)
    symbolic_direct=[]
    for ix in [0,3,9,14]:
        expr=s.expand(invariant_selector(f+q*bs[ix],gv))
        ok=s.diff(expr,q).subs(q,0)==grad[ix] and s.diff(expr,q,2).subs(q,0)==hi[ix,ix]
        check('independent polynomial derivative '+str(ix),ok)
        check('independent squared polynomial derivative '+str(ix),s.diff(expr**2,q,2).subs(q,0)==hv[ix,ix])
    source_i=extracted_selector_functions(SNAP/'neutrino_mass_derivation.py',['bracket','J_sq','delta_I'])['delta_I']
    gvn=array_selector(gv)
    errors=[]
    for eps in [1e-3,3e-4,1e-4]:
        numeric=np.zeros((15,15))
        for i in range(15):
            for j in range(15):
                bi=eps*bsn[i]; bj=eps*bsn[j]
                numeric[i,j]=(source_i(fn+bi+bj,gvn)-source_i(fn+bi-bj,gvn)
                              -source_i(fn-bi+bj,gvn)+source_i(fn-bi-bj,gvn))/(4*eps**2)
        err=float(np.max(abs(numeric-h))); errors.append(dict(step=eps,max_error=err))
        check('archived finite difference Hessian at step '+str(eps),err<2e-3,errors[-1])
    ev=eigvalsh(h); evv=eigvalsh(hvn)
    signed=lambda vals:dict(negative=int(sum(vals < -1e-8)),zero=int(sum(abs(vals)<=1e-8)),positive=int(sum(vals>1e-8)))
    original_ratio=np.sqrt(max(abs(ev))/min(abs(ev)[abs(ev)>1e-3]))
    canonical=eigvalsh(h,gm); canonical_v=eigvalsh(hvn,gm)
    variations=[]
    for bound in [2.,5.,10.]:
        c=np.diag(np.geomspace(1/bound,bound,15))
        hp=c.T@h@c; gp=c.T@gm@c; raw=eigvalsh(hp)
        rr=float(np.sqrt(max(abs(raw))/min(abs(raw)[abs(raw)>1e-3])))
        err=float(max(abs(eigvalsh(hp,gp)-canonical)))
        check('generalized I Hessian invariant under basis scaling '+str(bound),err<1e-8)
        check('generalized squared Hessian invariant under basis scaling '+str(bound),
              np.max(abs(eigvalsh(c.T@hvn@c,gp)-canonical_v))<1e-7)
        variations.append(dict(basis_scale_bound=bound,raw_abs_curvature_mass_ratio=rr,
                               generalized_eigenvalue_error=err))
    check('source curvature ratio changes under coordinate rescaling',
          max(abs(x['raw_abs_curvature_mass_ratio']/original_ratio-1) for x in variations)>.1)
    check('negative curvature is hidden by source absolute value',np.min(ev)<-1e-6,
          {'I_eigenvalue_signs':signed(ev),'I_squared_eigenvalue_signs':signed(evv)})
    data['curvature']=dict(I_exact=str(iv),I=float(iv),gradient_I=[str(x) for x in grad],
        I_squared=float(iv**2),hessian_I=[[str(x) for x in row] for row in hi.tolist()],
        kinetic_Gram=[[str(x) for x in row] for row in metric.tolist()],
        raw_I_eigenvalues=ev.tolist(),raw_squared_eigenvalues=evv.tolist(),
        generalized_I_eigenvalues=canonical.tolist(),generalized_squared_eigenvalues=canonical_v.tolist(),
        original_raw_mass_ratio=float(original_ratio),basis_variations=variations,finite_difference_errors=errors,
        qualification='A Frobenius kinetic metric is stipulated for coordinate diagnostics; the point is not a vacuum, so none of these eigenvalues is a derived physical mass spectrum.')

    md=bracket_selector(f,gv); mq=md[:3,:3]
    check('quark block singular',mq.det()==0,{'rank':mq.rank()})
    check('lepton block and both mixing blocks are zero',md[3,:]==s.zeros(1,4) and md[:,3]==s.zeros(4,1))
    check('pseudoinverse Schur expression exactly zero',
        md[3,3]-(md[3,:3]*mq.pinv()*md[:3,3])[0]==0)
    # No invariant color-triplet vector can mix with a singlet in the unbroken group.
    ts=[]
    for i in range(3):
        for j in range(i+1,3):
            a=s.zeros(3); a[i,j]=a[j,i]=s.Rational(1,2);ts.append(a)
            a=s.zeros(3); a[i,j]=-s.I/2;a[j,i]=s.I/2;ts.append(a)
    ts.extend([s.diag(1,-1,0)/2,s.diag(1,1,-2)/(2*s.sqrt(3))])
    casimir=sum([t*t for t in ts],s.zeros(3))
    check('SU3 triplet Casimir nonzero on every vector',casimir==s.Rational(4,3)*s.eye(3))
    check('no common invariant color triplet vector',s.Matrix.vstack(*ts).rank()==3)
    symanti=[bracket_selector(x,y) for x in sym for y in bs[9:]]
    check('valid archived symmetric-antisymmetric bracket identity',all(x==x.T for x in symanti))
    tree=ast.parse((SNAP/'neutrino_mass_derivation.py').read_text())
    used=sum(isinstance(n,ast.Name) and n.id=='S_dimless' and isinstance(n.ctx,ast.Load) for n in ast.walk(tree))
    check('computed complement never read by source',used==0,{'load_count':used})
    replay=OUT/'attempts/neutrino-mass-source';replay.mkdir(parents=True,exist_ok=True)
    run=subprocess.run([sys.executable,str(SNAP/'neutrino_mass_derivation.py')],cwd=replay,capture_output=True,text=True,timeout=30)
    (replay/'stdout.txt').write_text(run.stdout);(replay/'stderr.txt').write_text(run.stderr)
    check('archived neutrino source replay exits successfully',run.returncode==0)
    actual=json.loads((replay/'neutrino_mass_results.json').read_text()) if run.returncode==0 else {}
    expected=246*original_ratio
    check('replayed scale equals noncanonical Hessian ratio times inserted 246 GeV',abs(actual.get('Lambda_PS_GeV',0)/expected-1)<2e-5)
    check('replayed neutrino mass uses inserted electron mass',
          abs(actual.get('m_nu_eV',0)-(0.511e6)**2/(actual.get('Lambda_PS_GeV',1)*1e9))<1e-12)
    data['seesaw']=dict(matrix=[[str(x) for x in row] for row in md.tolist()],quark_rank=int(mq.rank()),
        pseudoinverse_complement=0,source_replay=actual,printed_static_claim=dict(Lambda_PS_GeV=3900,m_nu_eV=.067),
        qualification='Singlet-to-triplet mixing requires color-breaking structure. A true color-singlet heavy-neutrino seesaw remains possible, with its own mass/Yukawa inputs.')

    tau=s.symbols('tau'); transform=tau+2
    check('claimed modular fixed point fails',s.simplify(transform.subs(tau,s.I/2)-s.I/2)==2)
    check('parabolic modular action has no finite fixed point',s.solve(s.Eq(transform,tau),tau)==[])
    a,r=s.symbols('a R',positive=True)
    check('two claimed gap equalities incompatible for finite R',s.simplify((1/r**2+1/a**2)-1/a**2)==1/r**2)
    x=s.symbols('x',real=True)
    periodic=s.exp(s.I*x); anti=s.exp(s.I*x/2)
    check('integer mode fails required antiperiodicity',s.simplify(periodic.subs(x,x+2*s.pi)+periodic)!=0)
    check('half-integer mode has required antiperiodicity',s.simplify(anti.subs(x,x+2*s.pi)+anti)==0)
    finite_examples=[]
    for ar in [s.Rational(1,4),s.Rational(1,2),s.Integer(1),s.Integer(2)]:
        # Unit other factor area. A compact T2 factor suffices to refute convergence=>unique ratio.
        lam=1+1/ar**2; volume=4*s.pi**2*ar
        integral=volume/lam
        check('claimed convergence holds at alternate ratio '+str(ar),integral.is_finite is True and integral>0)
        finite_examples.append(dict(a_over_R=str(ar),integral=float(integral),
            periodic_torus_gap=float(min(1,1/ar**2)),one_antiperiodic_cycle_gap=.25,
            source_gap=float(lam)))
    # A concrete Klein quotient: (x,y)~(x+2pi,y)~(-x,y+2pi),
    # orientation cover has y period 4pi. cos(x) is an allowed even scalar.
    klein=s.cos(x)
    check('nonorientability alone does not force every scalar to be antiperiodic',
          s.simplify(klein.subs(x,-x)-klein)==0 and s.simplify(klein.subs(x,x+2*s.pi)-klein)==0)
    k=s.symbols('K',real=True)
    ratio=8*s.exp(-(k-1))
    check('cutoff substitution returns any preselected inverse coupling',s.simplify(s.log(8/ratio)+1-k)==0)
    # Even the attachment's own local matrix integrand gives no wave equation
    # if the two metrics are independent: there are no derivatives of either metric.
    b=s.symbols('b',positive=True)
    density=2*(b-s.log(b)) # 4x4 relative metric b I
    check('displayed matrix action stationary relative metric b=1',s.diff(density,b).subs(b,1)==0)
    check('displayed action is not primary GfE warmup action up to an additive constant',
          s.simplify(s.diff(density-(-4*s.log(b)),b))!=0)
    data['cutoff']=dict(modular_map='tau -> tau + 2',claimed_fixed_point_residual=2,
        gap_equality_residual='1/R^2',alternative_finite_integrals=finite_examples,
        arbitrary_target_identity='log(8 / (8 exp(-(K-1)))) + 1 = K',
        recovered_cutoff=float(8*s.exp(-s.Rational('136.035999171'))),
        fixed_half_ratio_inverse_coupling=float(s.log(16)+1),
        qualification='Boundary conditions, bundle/parity and metric must be specified. No beta function, compactification prescription or boundary datum deriving the exponent is supplied by the recovered attachment.')
    result=dict(checks_total=len(checks),checks_passed=sum(c['passed'] for c in checks),checks=checks,**data)
    (OUT/'selector-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=result['checks_passed'],failures=[c for c in checks if not c['passed']],
        I=float(iv),source_replay=actual,basis_variations=variations),indent=2))
    if result['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':
    run_selector_audit()
