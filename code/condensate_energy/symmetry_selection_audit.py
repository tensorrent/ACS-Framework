#!/usr/bin/env python3
"""Domain, closure and real-form controls for the archived symmetry selector."""
import ast
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/selection_energy'
SNAP=OUT/'source-snapshots'


def symmetry_matrix_unit(i,j,n=4):
    result=s.zeros(n);result[i,j]=1;return result


def real_symmetry_columns(generators):
    return s.Matrix.hstack(*[s.Matrix([s.re(v) for v in g]+[s.im(v) for v in g]) for g in generators])


def exact_symmetry_structure(generators):
    cols=real_symmetry_columns(generators);gram=cols.T*cols
    left=gram.inv()*cols.T
    ads=[];closed=True;brackets=[]
    for a in generators:
        ad=[]
        for b in generators:
            bracket=a*b-b*a;v=real_symmetry_columns([bracket]);coeff=left*v
            closed=closed and all(s.simplify(x)==0 for x in cols*coeff-v)
            ad.append(coeff);brackets.append(v)
        ads.append(s.Matrix.hstack(*ad))
    killing=s.Matrix([[s.simplify(s.trace(a*b)) for b in ads] for a in ads])
    return dict(closed=closed,dimension=cols.rank(),derived_rank=s.Matrix.hstack(*brackets).rank(),
                killing_rank=killing.rank(),killing=killing,gram=gram)


def load_symmetry_source_functions():
    tree=ast.parse((SNAP/'selection_full.py').read_text())
    ns=dict(np=np,norm=np.linalg.norm,matrix_rank=np.linalg.matrix_rank)
    body=[x for x in tree.body if isinstance(x,ast.FunctionDef)]
    exec(compile(ast.Module(body=body,type_ignores=[]),str(SNAP/'selection_full.py'),'exec'),ns)
    return ns


def audit_symmetry_selection():
    checks=[]
    def check(name,ok,evidence=None):
        row=dict(name=name,passed=bool(ok))
        if evidence is not None:row['evidence']=evidence
        checks.append(row)
    E=symmetry_matrix_unit
    diag=[s.diag(1,-1,0,0)/s.sqrt(2),s.diag(1,1,-2,0)/s.sqrt(6)]
    syms=[(E(i,j)+E(j,i))/s.sqrt(2) for i,j in [(0,1),(0,2),(1,2)]]
    antis=[(E(i,j)-E(j,i))/s.sqrt(2) for i,j in [(0,1),(0,2),(1,2)]]
    split=diag+syms+antis
    compact=[s.I*g for g in diag+syms]+antis
    upper=diag+[E(i,j) for i in range(4) for j in range(i+1,4)]
    structures={}
    for name,gens in [('split_sl3',split),('upper_solvable8',upper),('compact_su3',compact)]:
        info=exact_symmetry_structure(gens)
        check(name+' has eight independent real directions',info['dimension']==8)
        check(name+' is exactly closed',info['closed'])
        check(name+' basis orthonormal for real Frobenius metric',info['gram']==s.eye(8))
        structures[name]=dict(dimension=int(info['dimension']),derived_rank=int(info['derived_rank']),
            killing_rank=int(info['killing_rank']),killing_eigenvalues={str(k):v for k,v in info['killing'].eigenvals().items()})
    check('distinct closed 8D algebra has degenerate Killing form',structures['upper_solvable8']['killing_rank']<8)
    check('split algebra Killing form nondegenerate',structures['split_sl3']['killing_rank']==8)
    check('compact realization genuinely skew Hermitian',all(g+g.conjugate().T==s.zeros(4) for g in compact))
    check('compact realization is not a real-matrix basis',any(any(s.im(x)!=0 for x in g) for g in compact))
    compact_c=s.simplify(sum(s.trace((g+g.conjugate().T).conjugate().T*(g+g.conjugate().T)) for g in compact))
    transpose_c=s.simplify(sum(s.trace((g+g.T).conjugate().T*(g+g.T)) for g in compact))
    check('Hermitian compactness vanishes on su3',compact_c==0)
    check('archived transpose predicate would reject compact su3 even with complex arrays',transpose_c==20)
    check('split and solvable candidates tie in stated combined score',
        s.simplify(sum(s.trace((g+g.T).T*(g+g.T)) for g in split))==20
        and s.simplify(sum(s.trace((g+g.T).T*(g+g.T)) for g in upper))==20)

    # On R^(4x4), antisymmetric projection has rank 4*3/2=6.
    units=[E(i,j) for i in range(4) for j in range(4)]
    pa=s.Matrix.hstack(*[s.Matrix(list((u-u.T)/2)) for u in units])
    check('antisymmetric projector idempotent',pa*pa==pa)
    check('real antisymmetric space dimension six',pa.rank()==6 and s.trace(pa)==6)
    # For 8 orthonormal columns B, Tr(B^T Pa B)<=rank(Pa)=6.
    # C=4 Tr(B^T (I-Pa)B)>=8. Individual ||g+gT||<=2,
    # so their mean >= C/(2*8)>=1/2, above classifier threshold .15.
    bound=4*(8-6);mean_bound=bound/(2*8)
    check('rank-eight compactness lower bound defeats source threshold',bound==8 and mean_bound>.15)
    all_anti=[(E(i,j)-E(j,i))/s.sqrt(2) for i in range(4) for j in range(i+1,4)]
    saturator=all_anti+diag
    exact_c=s.simplify(sum(s.trace((g+g.T).T*(g+g.T)) for g in saturator))
    check('orthonormal saturator attains compactness lower bound',exact_c==8)
    ns=load_symmetry_source_functions()
    array=lambda gs:[np.array(g,dtype=complex if any(s.im(x)!=0 for x in g) else float) for g in gs]
    check('archived compactness function confirms saturator',abs(ns['compactness_defect'](array(saturator))-8)<1e-12)
    check('archived closure accepts solvable counterexample',ns['closure_defect'](array(upper))<1e-13)
    seeded=[]
    for seed in [3,11,23,47,83,109]:
        rng=np.random.default_rng(seed)
        gs=ns['orthonormalize'](ns['enforce_traceless']([rng.normal(size=(4,4)) for _ in range(8)]))
        cvalues=[];ranks=[];means=[];scores=[];increases=0
        for step in range(21):
            C=ns['compactness_defect'](gs);D=ns['closure_defect'](gs)
            cvalues.append(float(C));ranks.append(len(gs));means.append(float(np.mean([np.linalg.norm(g+g.T) for g in gs])))
            score=D+.05*C
            if scores and score>scores[-1]+1e-12:increases+=1
            scores.append(score)
            if step<20:gs=ns['combined_step'](gs,lr=.008,lam=.05)
        check('source short flow retains real rank-eight domain seed '+str(seed),
              all(n==8 for n in ranks) and all(np.isrealobj(g) for g in gs))
        check('source short flow obeys exact compactness bound seed '+str(seed),min(cvalues)>=8-1e-10 and min(means)>=.5-1e-10)
        seeded.append(dict(seed=seed,steps=20,initial_score=scores[0],final_score=scores[-1],
            score_increasing_steps=increases,min_compactness=min(cvalues),minimum_mean_transpose_defect=min(means),
            final_label=ns['classify'](gs)))
    # For conjugate su(3) realizations, unitary conjugation gives the same closure and positivity.
    U=s.eye(4);U[0,0]=U[3,3]=s.Rational(3,5);U[0,3]=s.Rational(4,5);U[3,0]=-s.Rational(4,5)
    rotated=[U*g*U.T for g in compact]
    rotated_info=exact_symmetry_structure(rotated)
    check('compact color embedding can move under unitary conjugation',rotated!=compact)
    check('conjugate compact embedding retains closure',rotated_info['closed'])
    check('conjugate compact embedding retains negative Killing form',rotated_info['killing']==exact_symmetry_structure(compact)['killing'])
    replay=OUT/'attempts/selection-principle';replay.mkdir(exist_ok=True)
    run=subprocess.run([sys.executable,str(SNAP/'selection_principle.py')],cwd=replay,capture_output=True,text=True,timeout=30)
    (replay/'stdout.txt').write_text(run.stdout);(replay/'stderr.txt').write_text(run.stderr)
    check('original selection-principle script replays',run.returncode==0)
    result=dict(checks_total=len(checks),checks_passed=sum(c['passed'] for c in checks),checks=checks,
        structures=structures,compactness_lower_bound=bound,mean_defect_lower_bound=mean_bound,
        source_su3_threshold=.15,seeded_short_flows=seeded,
        status='Archived real rank-eight search cannot reach its claimed compact su3 target. Exact compact su3 exists in a different, complex representation domain.',
        limits=['Closure plus an inserted dimension and penalty is not an Euler-Lagrange vacuum selector.',
            'The 8D solvable counterexample refutes uniqueness of closure, not a classification of all compact subalgebras.',
            'The corrected complex real form is a different physical choice, not merely a rescaling.',
            'Short flows are diagnostics, not an exhaustive attractor study.'])
    (OUT/'symmetry-selection.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks_total=len(checks),checks_passed=result['checks_passed'],
        failures=[c for c in checks if not c['passed']],structures=structures,flows=seeded),indent=2))
    if result['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':audit_symmetry_selection()
