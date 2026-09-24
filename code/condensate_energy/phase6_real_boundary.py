#!/usr/bin/env python3
"""Independently solve all real roots of the source's four-quartic proxy."""
import ast
import json
from pathlib import Path
import sympy as s
from scipy.optimize import root
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/endpoint_audit'


def solve_phase6_real_boundary():
    x,y,z,w=s.symbols('x y z w',real=True);gg=s.Rational(16,9)
    vars=[x,y,z,w]
    env=dict(L1=gg*x,L2_s=gg*y,L3_s=gg*z,L4_s=gg*w,g_sq=gg,Rational=s.Rational)
    src=OUT/'source-snapshots/phase6_dynamics.py'
    tree=ast.parse(src.read_text());names=['beta_L1','beta_L2','beta_L3','beta_L4']
    nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets)]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),env)
    equations=[s.expand(env[n]/gg**2) for n in names]
    checks=[]
    def check(name,ok,evidence=None):checks.append(dict(name=name,passed=bool(ok),evidence=evidence))
    check('source beta4 factorization',s.factor(equations[3])==4*w*(x+y-3))
    check('nonzero w branch impossible over reals',s.expand(equations[1].subs(x,3-y))==2*z*z+2*w*w+3)
    check('remaining beta3 factorization',s.factor(equations[2])==4*z*(x+y+2*z-3))
    branches=[]
    for label,zvalue in [('zero',s.Integer(0)),('nonzero',(3-x-y)/2)]:
        pair=[s.expand(eq.subs({w:0,z:zvalue})) for eq in equations[:2]]
        gb=s.groebner(pair,y,x)
        univariate=next(p.as_expr() for p in gb.polys if not p.as_expr().has(y))
        linear=next(p.as_expr() for p in gb.polys if s.degree(p.as_expr(),y)==1)
        yvalue=s.solve(linear,y)[0]
        residuals=[s.rem(s.together(p.subs(y,yvalue)).as_numer_denom()[0],univariate,x) for p in pair]
        check(label+' elimination reconstructs both original equations exactly',all(q==0 for q in residuals))
        pol=s.Poly(univariate,x);intervals=s.polys.polytools.intervals(pol,eps=s.Rational(1,10**20))
        check(label+' all real roots isolated by exact Sturm count',sum(mult for interval,mult in intervals)==pol.count_roots(-s.oo,s.oo))
        roots=[]
        for interval,mult in intervals:
            center=(interval[0]+interval[1])/2
            xv=float(center);yv=float(yvalue.subs(x,center));zv=float(zvalue.subs({x:center,y:yvalue.subs(x,center)}));point=np.array([xv,yv,zv,0.])
            fn=s.lambdify(vars,equations,'numpy')
            error=float(np.linalg.norm(fn(*point),ord=np.inf))
            check(label+' original residual '+str(len(roots)),error<1e-10,error)
            independently=root(lambda a:np.array(fn(*a),float),point+np.array([1e-5,-2e-5,1e-5,1e-5]),tol=1e-11)
            check(label+' independent numerical root '+str(len(roots)),independently.success and np.linalg.norm(independently.x-point)<1e-8)
            roots.append(dict(interval=[str(q) for q in interval],multiplicity=mult,scaled_quartics=point.tolist(),quartics=(float(gg)*point).tolist(),residual=error))
        candidate=s.sqrt(3)/24
        check(label+' proposed Higgs number is not a proxy root',s.simplify(univariate.subs(x,candidate))!=0)
        branches.append(dict(label=label,univariate=str(univariate),y_of_x=str(yvalue),z_of_x_y=str(zvalue),real_roots=roots))
    data=dict(checks_total=len(checks),checks_passed=sum(c['passed'] for c in checks),checks=checks,source_equations=[str(e) for e in equations],
              branches=branches,scope='Exact all-real solution set of the printed fixed-gauge four-quartic proxy, not a fixed point of the complete running ACS action')
    (OUT/'phase6-real-roots.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
    if data['checks_passed']!=len(checks):raise SystemExit(1)


if __name__=='__main__':solve_phase6_real_boundary()
