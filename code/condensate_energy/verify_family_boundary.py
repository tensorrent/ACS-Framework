#!/usr/bin/env python3
"""Independent controls, including the degeneracy exposed by the full replay."""
import json
from pathlib import Path
import re
import numpy as np
import sympy as s
from canonical_scalar_action import independent_projector, scalar_unpack, scalar_pack
from hidden_coupling_audit import mass

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy/family_boundary'


def verify_family_boundary():
    result = json.loads((OUT/'results.json').read_text())
    checks = []
    def check(name, ok, evidence=None):
        row = dict(name=name, passed=bool(ok))
        if evidence is not None: row['evidence'] = evidence
        checks.append(row)
    eps = s.symbols('epsilon', positive=True)
    w = s.Matrix([eps**3/6, -eps**2/2, eps])
    texture = w*w.T
    check('exact phase-scale-two texture is rank one', texture.rank() == 1)
    check('exact phase-scale-two texture has two massless modes', len(texture.nullspace()) == 2)
    check('nonzero singular value is the vector norm squared',
          s.factor(s.trace(texture)-eps**2*(1+eps**2/4+eps**4/36)) == 0)
    ww = np.array(w.subs(eps, s.Rational(453, 2000)), float).ravel()
    matrix = np.outer(ww, ww)
    U, singular, Vh = np.linalg.svd(matrix)
    null_rotations = []
    for theta in [.0, .04, .3]:
        B = np.eye(3); B[1:,1:] = [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        Ud = U@B
        check('null-subspace rotation preserves the mass matrix '+str(theta),
              np.linalg.norm(Ud@np.diag(singular)@Vh-matrix) < 1e-15)
        ckm = U.conj().T@Ud
        null_rotations.append(dict(angle=theta, apparent_mixing=float(abs(ckm[1,2]))))
    log = (OUT/'attempts/ps_yukawa_full/stdout.txt').read_text()
    ps = float(re.search(r'Best phase scale = ([0-9.]+)', log).group(1))
    check('full source replay best phase scale is the rank-one value', ps == 2.)
    check('full replay reports zero first-two-family masses',
          'Up-type:   0.0000, 0.000,' in log and 'Down-type:  0.0000, 0.0000,' in log)
    qfp = (OUT/'attempts/phase7_qfp_yukawa/stdout.txt').read_text()
    check('QFP replay finds no scanned crossing', 'No crossing found.' in qfp)

    # Derive the fermion box from four color copies of two Dirac masses and
    # one neutral 2x2 Majorana block; no archived beta function is used here.
    a,b,d,y,z,f = s.symbols('a b d y z f', real=True)
    up,down = y*a+z*b, y*b+z*a
    heavy = s.sqrt(2)*f*d
    neutral = s.Matrix([[0,down],[down,-heavy]])
    trace4 = s.expand(8*up**4+6*down**4+s.trace(neutral**4))
    check('closed Weyl fourth trace includes all sixteen entries',
          s.expand(trace4-(8*(up**4+down**4)+8*down**2*f**2*d**2+4*f**4*d**4)) == 0)
    box = s.Poly(-2*trace4,a,b,d)
    mixed = box.coeff_monomial(a*b*d**2)
    check('independent determinant-portal box coefficient', s.factor(mixed+32*y*z*f**2) == 0)
    oddphi = box.coeff_monomial(a**3*b)
    check('independent determinant-Phi box coefficient', s.factor(oddphi+64*y*z*(y**2+z**2)) == 0)
    sub = {y:s.Rational(1,5), z:s.Rational(1,10), f:s.Rational(3,10)}
    beta = result['generated_quartic_beta_times_32pi2']
    check('portal coefficient agrees with full beta result', abs(float(mixed.subs(sub))-beta[14]) < 1e-14)
    check('Phi determinant coefficient agrees with full beta result', abs(float(oddphi.subs(sub))-beta[4]) < 1e-14)
    for aa,bb,dd in [(.2,.3,1.),(.4,-.1,.8),(.11,.05,.6)]:
        phi=np.diag([aa,bb]).astype(complex)
        delta=np.zeros((3,4,4),complex);delta[:,3,3]=dd*np.array([1.,-1j,0.])/np.sqrt(2)
        M=mass(phi,delta,np.array([[.2]]),np.array([[.1]]),np.array([[.3]]))
        mm=M.conj().T@M
        exact=float(trace4.subs(sub|{a:aa,b:bb,d:dd}))
        check('closed fermion trace matches independent component mass at '+str((aa,bb,dd)),
              abs(np.trace(mm@mm).real-exact)<1e-14)

    # Re-evaluate the witness potential with the separately implemented invariant
    # projector, and compare restricted neutral formulas and directional stationarity.
    projector=independent_projector()
    rng=np.random.default_rng(924105)
    evidence=[]
    for j,wit in enumerate(result['neutral_vacua']):
        lam=np.array(wit['quartics']);mm=np.array(wit['quadratic_coefficients'])
        beta0=wit['beta'];vv=.3;dd=1.
        delta=np.zeros((3,4,4),complex);delta[:,3,3]=dd*np.array([1.,-1j,0.])/np.sqrt(2)
        phi=np.diag([vv*np.cos(beta0),vv*np.sin(beta0)]).astype(complex)
        x0=scalar_pack(phi,delta)
        def potential(x):
            p,q=scalar_unpack(x)
            det=np.linalg.det(p)
            quadratic=np.array([np.vdot(p,p).real,det.real,det.imag,np.vdot(q,q).real])
            return float(lam@projector(p,q)[0]+mm@quadratic)
        A=mm[1]*vv**2/2;B=-lam[16]*vv**2*dd**2/2
        angular=lambda theta:A*np.sin(2*theta)+B*np.cos(2*theta)
        h=1e-4
        points=[scalar_pack(np.diag([vv*np.cos(beta0+t),vv*np.sin(beta0+t)]).astype(complex),delta) for t in [-h,0,h]]
        curv=(potential(points[0])-2*potential(points[1])+potential(points[2]))/h**2
        check('independent projector recovers angular curvature '+str(j),
              abs(curv-wit['angular_curvature'])<2e-7)
        checks_at_point=[]
        for k in range(4):
            vdir=rng.normal(size=68);vdir/=np.linalg.norm(vdir)
            step=2e-5
            derivative=(potential(x0+step*vdir)-potential(x0-step*vdir))/(2*step)
            checks_at_point.append(float(derivative))
        check('independent directional tadpoles vanish '+str(j),max(abs(x) for x in checks_at_point)<2e-8)
        check('exact-form angular stationarity '+str(j),abs(2*A*np.cos(2*beta0)-2*B*np.sin(2*beta0))<1e-15)
        evidence.append(dict(tan_beta=wit['tan_beta'],projector_angular_curvature=curv,
                             directional_tadpoles=checks_at_point))
    verified=dict(checks_total=len(checks),checks_passed=sum(x['passed'] for x in checks),checks=checks,
        replay_degeneracy=dict(best_phase_scale=ps,exact_rank=1,zero_masses_per_sector=2,
                              arbitrary_null_rotations=null_rotations),
        independent_loop_coefficients=dict(B_lambda14=str(mixed),B_lambda4=str(oddphi)),
        independent_projector_controls=evidence,
        qualification='Apparent CKM mixing inside a massless degenerate subspace is not a physical mixing prediction.')
    (OUT/'verification.json').write_text(json.dumps(verified,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=verified['checks_passed'],
                         failures=[x for x in checks if not x['passed']]),indent=2))
    if verified['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':
    verify_family_boundary()
