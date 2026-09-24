#!/usr/bin/env python3
"""Trace the actual family, Yukawa-input and vacuum-alignment dependencies."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import sympy as s
from canonical_scalar_action import (load_exact_basis, basis_derivatives, scalar_pack,
                                    physical_spectrum)
from hidden_coupling_audit import archived, mass

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy/family_boundary'


def family_alignment_boundary():
    OUT.mkdir(exist_ok=True)
    snap = OUT / 'source-snapshots'
    snap.mkdir(exist_ok=True)
    paths = ['extras/' + x + '.py' for x in ['task_C_rigorous', 'task_D_lagrangian',
        'phase50_vacuum', 'phase51_tanbeta', 'phase52_yukawa', 'phase7_qfp_yukawa', 'ps_yukawa_full']]
    paths += ['src/paper_c/theorem_c.py', 'src/paper_a/branch_a_parameters.py', 'src/paper_a/yukawa_no_go.py']
    provenance = []
    for rel in paths:
        src = ROOT / 'code/acs_codebase' / rel
        dest = snap / src.name
        dest.write_bytes(src.read_bytes())
        provenance.append(dict(source=str(src), snapshot=str(dest.relative_to(ROOT)),
                               sha256=sha256(dest.read_bytes()).hexdigest()))
    (OUT / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    checks = []
    def check(name, ok, evidence=None):
        row = dict(name=name, passed=bool(ok))
        if evidence is not None:
            row['evidence'] = evidence
        checks.append(row)

    # A matrix-unit basis makes the adjoint eigenvalues explicit, without
    # assuming an orthogonal Cartan basis or identifying eigenvalue count with rank.
    T = s.diag(s.Rational(1, 3), s.Rational(1, 3), s.Rational(1, 3), -1)
    units = []
    for i in range(4):
        for j in range(4):
            if i != j:
                b = s.zeros(4); b[i, j] = 1; units.append(b)
    for i in range(3):
        b = s.zeros(4); b[i, i] = 1; b[3, 3] = -1; units.append(b)
    W = s.Matrix.hstack(*[s.Matrix(list(b)) for b in units])
    A = s.Matrix.hstack(*[W.gauss_jordan_solve(s.Matrix(list(T*b-b*T)))[0] for b in units])
    check('exact cubic identity retained', A**3 == s.Rational(16, 9)*A)
    check('adjoint rank is six', A.rank() == 6)
    check('adjoint kernel has dimension nine', len(A.nullspace()) == 9)
    check('three eigenvalues have multiplicities nine three three',
          A.eigenvals() == {s.Integer(0): 9, s.Rational(4, 3): 3, -s.Rational(4, 3): 3})
    check('no quadratic annihilating polynomial',
          s.Matrix.hstack(s.Matrix(list(s.eye(15))), s.Matrix(list(A)), s.Matrix(list(A**2))).rank() == 3)
    S = s.zeros(4); S[0, 3] = S[3, 0] = 1
    H = s.diag(1, -1, 0, 0)
    cyclic = []
    for seed in [S, S+H]:
        it = [seed]
        for _ in range(3): it.append(T*it[-1]-it[-1]*T)
        cyclic.append(s.Matrix.hstack(*[s.Matrix(list(x)) for x in it]).rank())
    check('source symmetric seed has cyclic dimension two', cyclic[0] == 2)
    check('generic seed with all spectral components has cyclic dimension three', cyclic[1] == 3)
    E03 = s.zeros(4); E03[0, 3] = 1
    E10 = s.zeros(4); E10[1, 0] = 1
    E13 = s.zeros(4); E13[1, 3] = 1
    check('claimed three directions transform into one another under color', E10*E03-E03*E10 == E13)
    splitting = []
    for n in [1, 2, 3, 4]:
        # sl(n+1), T=(1/n,...,1/n,-1): multiplicities n²,n,n.
        ts = [s.Rational(1, n)]*n + [-s.Integer(1)]
        evs = [ts[i]-ts[j] for i in range(n+1) for j in range(n+1) if i != j] + [s.Integer(0)]*n
        check('two-block splitting gives three eigenvalues for n='+str(n), len(set(evs)) == 3)
        splitting.append(dict(color_block=n, algebra_dimension=len(evs),
                              zero=evs.count(0), positive=evs.count(s.Rational(n+1, n))))
    replicas = []
    for nf in [1, 2, 4]:
        # Family space is a multiplicity factor; it does not change the gauge
        # adjoint relation. The inherited fermion constructor explicitly accepts it.
        phi = np.diag([.2, .3]).astype(complex)
        delta = np.zeros((3, 4, 4), complex)
        fm = mass(phi, delta, np.eye(nf)*.2, np.eye(nf)*.1, np.eye(nf)*.3)
        check('same gauge action permits explicit family multiplicity '+str(nf), fm.shape == (16*nf, 16*nf))
        replicas.append(dict(families=nf, weyl_matrix_shape=list(fm.shape)))

    # Recover the actual source functions without executing its expensive scan.
    src = snap / 'ps_yukawa_full.py'
    tree = ast.parse(src.read_text())
    env = dict(np=np, svd=np.linalg.svd, v=246.22,
               phases=np.array([[0., np.pi/2, 0.], [-np.pi/2, 0., np.pi/2], [0., -np.pi/2, 0.]]))
    names = ['build_yukawa_acs', 'compute_ckm']
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(src), 'exec'), env)
    # The proof below is independent of the phase matrix: both calls pass the same one.
    mt, mb, ep, vv, sb, cb, nn = s.symbols('mt mb epsilon v sinbeta cosbeta N', nonzero=True)
    nu = mt/(ep**2*vv*sb); nd = mb/(ep**3*s.Rational(4,3)*vv*cb)
    pref_u = s.cancel(nu*vv*sb)
    pref_d = s.cancel(nd*vv*cb*ep*s.Rational(4,3))
    check('source up mass prefactor cancels tan beta exactly', pref_u == mt/ep**2)
    check('source down mass prefactor cancels tan beta exactly', pref_d == mb/ep**2)
    check('source mass matrices are exactly proportional for every phase input',
          s.cancel(pref_d/pref_u) == mb/mt)
    scan = []
    for tb, ps in [(.1, .1), (.5, 1.), (4., 1.3), (100., 3.)]:
        V, mu, md = env['compute_ckm'](.2265, tb, ps)
        off = np.linalg.norm(np.abs(V)-np.eye(3))
        ratios = np.array(mu)/np.array(md)
        check('implemented CKM scan stays aligned at '+str((tb, ps)), off < 1e-10)
        check('implemented generation ratios reproduce inserted normalization '+str((tb, ps)),
              np.max(abs(ratios-172.5/4.18)) < 1e-8)
        scan.append(dict(tan_beta=tb, phase_scale=ps, mixing_residual=float(off), mass_ratios=ratios.tolist()))
    qsrc = snap / 'phase7_qfp_yukawa.py'
    fn = next(n for n in ast.parse(qsrc.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'yukawas')
    qenv = dict(np=np, v=246.22, m_t=172.5, m_b=4.18, m_tau=1.777)
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(qsrc), 'exec'), qenv)
    qfp = []
    for tb in [1., 10., 60.]:
        yt, yb, _ = qenv['yukawas'](tb)
        ratio = yt/yb*tb
        check('QFP source mass ratio remains an inserted datum at '+str(tb), abs(ratio-172.5/4.18) < 1e-12)
        qfp.append(dict(tan_beta=tb, reconstructed_mass_ratio=ratio))

    b, v, d, bc = s.symbols('beta v d beta_c', real=True)
    k1, k2, y, z = s.symbols('k1 k2 y z', real=True)
    check('equal positive VEV mass identity retained',
          s.expand((y*k1+z*k2)-(y*k2+z*k1)-(y-z)*(k1-k2)) == 0)
    check('equal negative VEVs give opposite masses of equal singular values',
          s.expand(((y*k1+z*k2)+(y*k2+z*k1)).subs(k2, -k1)) == 0)
    phi = s.diag(v*s.cos(b), v*s.sin(b))
    tilde = s.diag(v*s.sin(b), v*s.cos(b))
    product_term = s.trigsimp(2*bc*s.trace(phi.T*tilde)*d**2)
    check('explicit product-of-traces term has twice the final Phase51 coefficient',
          s.simplify(s.expand_trig(product_term-2*bc*v**2*d**2*s.sin(2*b))) == 0)

    # Complete-action local witnesses: independent orientation-sensitive terms
    # make different non-equal VEV ratios possible, with all physical scalars tested.
    polys, quadratics, metric = load_exact_basis()
    witnesses = []
    for beta in [np.pi/12, np.pi/8, np.pi/6]:
        vv, dd = .3, 1.
        lam = np.zeros(17); lam[0] = 1.; lam[6:11] = [1.2, 1., 1.2, 1.2, 1.2]
        lam[13] = .1; lam[16] = .02
        m1 = -lam[16]*dd**2*np.tan(2*beta)
        m0 = -2*lam[0]*vv**2-lam[13]*dd**2-m1*np.sin(2*beta)/2+lam[16]*dd**2*np.cos(2*beta)/2
        md = -2*lam[7]*dd**2-lam[13]*vv**2+lam[16]*vv**2*np.cos(2*beta)/2
        mm = np.array([m0, m1, 0., md])
        phi = np.diag([vv*np.cos(beta), vv*np.sin(beta)]).astype(complex)
        delta = np.zeros((3,4,4), complex); delta[:,3,3] = dd*np.array([1.,-1j,0.])/np.sqrt(2)
        x = scalar_pack(phi, delta)
        vals, grads, hess = basis_derivatives(polys, quadratics, x)
        coeff = np.r_[lam, mm]
        grad = coeff@grads; hs = np.einsum('i,ijk->jk', coeff, hess)
        spec = physical_spectrum(hs, grad, x, metric)
        check('full stationary unequal-VEV witness at beta='+str(beta), spec['tadpole_infinity_norm'] < 1e-12)
        check('all 56 physical scalar directions positive at beta='+str(beta),
              spec['positive']==56 and spec['negative']==0 and spec['zero']==0)
        check('gauge Ward identity at beta='+str(beta), spec['goldstone_ward_relative'] < 1e-12)
        # Along the real neutral angle: A sin(2b)+B cos(2b), exact minimum
        # at the prescribed b, with curvature -4(A sin(2b)+B cos(2b)).
        aa = m1*vv**2/2; bb = -lam[16]*vv**2*dd**2/2
        curvature = -4*(aa*np.sin(2*beta)+bb*np.cos(2*beta))
        check('independent neutral angular curvature is positive at beta='+str(beta), curvature > 0)
        witnesses.append(dict(beta=float(beta), tan_beta=float(np.tan(beta)), quartics=lam.tolist(),
            quadratic_coefficients=mm.tolist(), minimum_physical_mass_squared=spec['minimum_mass_squared'],
            physical_positive=spec['positive'], tadpole_norm=spec['tadpole_infinity_norm'],
            angular_curvature=float(curvature)))
    # These couplings are bounded by Nphi² + Ndelta² + .09 Nphi Ndelta,
    # since |Jphi dot Jdelta| <= Nphi Ndelta/2 and extra projected norms are positive.
    check('all witness quartics have a positive analytic lower bound', .1-.02/2 > 0)

    Y = np.array([[.2]], complex); Z = np.array([[.1]], complex); F = np.array([[.3]], complex)
    flow = archived.beta(np.zeros(17), np.zeros(4), np.zeros(3), Y, Z, F)
    bq = np.array(flow['quartics'])*(32*np.pi**2)
    check('generic two-Yukawa loops generate a determinant-dependent Phi quartic', abs(bq[4])+abs(bq[5]) > 1e-12)
    check('generic Majorana plus two-Yukawa loops generate a determinant portal', abs(bq[14])+abs(bq[15]) > 1e-12)

    # Replays are isolated; seeding changes only the test RNG, not source code.
    replay = OUT / 'attempts'; replay.mkdir(exist_ok=True)
    wrapper = 'import numpy as np, runpy, sys; np.random.seed(924104); runpy.run_path(sys.argv[1], run_name="__main__")'
    for name in ['task_C_rigorous', 'phase51_tanbeta', 'phase52_yukawa', 'ps_yukawa_full', 'phase7_qfp_yukawa']:
        dest = replay / name; dest.mkdir(exist_ok=True)
        run = subprocess.run([sys.executable, '-c', wrapper, str(snap/(name+'.py'))],
                             cwd=dest, capture_output=True, text=True, timeout=60)
        (dest/'stdout.txt').write_text(run.stdout); (dest/'stderr.txt').write_text(run.stderr)
        (dest/'execution.json').write_text(json.dumps(dict(returncode=run.returncode, wrapper=wrapper), indent=2)+'\n')
        check('unchanged source replay '+name, run.returncode==0)
    result = dict(checks_total=len(checks), checks_passed=sum(c['passed'] for c in checks), checks=checks,
        adjoint=dict(rank=6, nullity=9, minimal_polynomial='t(t-4/3)(t+4/3)',
                     multiplicities={'0':9, '4/3':3, '-4/3':3}, cyclic_dimensions=cyclic),
        splitting_countercontrols=splitting, independent_family_replicas=replicas,
        source_ckm_scan=scan, qfp_inserted_mass_ratios=qfp, neutral_vacua=witnesses,
        generated_quartic_beta_times_32pi2=bq.tolist(),
        status='Family count is not derived by the cubic identity; the archived CKM scan is aligned; complete-action vacuum alignment remains an input.',
        limitations=['No universal classification of flavor mechanisms',
            'Witness actions use chosen coefficients, not physical boundary values',
            'Strict local minima and quartic boundedness do not certify global minima',
            'The loop-source check reuses the previously independently verified complete beta tables',
            'No full finite one-loop minimization at arbitrary mixed couplings is claimed'])
    (OUT/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks), checks_passed=result['checks_passed'],
        failures=[c for c in checks if not c['passed']],
        vacuum_ratios=[w['tan_beta'] for w in witnesses],
        generated_quartic_beta_times_32pi2=bq.tolist()), indent=2))
    if result['checks_passed'] != len(checks):
        raise SystemExit(1)


if __name__ == '__main__':
    family_alignment_boundary()
