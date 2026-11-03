"""Conic proposals for the convex hull of each squared ordinate displacement."""
import argparse,importlib.metadata,json,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy import sparse
import clarabel
from flint import arb,ctx
import dedekind_coupled_recovery as core
import dedekind_quadratic_ordinate as quad


def cone_rows(N,columns):
    # b-Ax = (z+1, 2y, z-1). Membership in the Lorentz cone is
    # equivalent to z>=y^2; adding z<=1 gives the convex hull.
    rr=[];cc=[];vv=[]
    for j in range(N):
        rr.extend([3*j,3*j+1,3*j+2]);cc.extend([columns+N+j,columns+j,columns+N+j]);vv.extend([-1.,-2.,-1.])
    return sparse.csc_matrix((vv,(rr,cc)),shape=(3*N,columns+2*N)),np.tile([1.,0.,-1.],N)


def settings(limit):
    s=clarabel.DefaultSettings();s.verbose=False;s.time_limit=limit;s.max_threads=2
    s.tol_gap_abs=1e-9;s.tol_gap_rel=1e-9;s.tol_feas=1e-9
    return s


def geometry_check():
    soc,b=cone_rows(1,0)
    A=sparse.vstack([sparse.csc_matrix([[1.,0.]]),sparse.csc_matrix([[0.,1.]]),soc],format='csc')
    rhs=np.r_[.5,1.,b]
    solver=clarabel.DefaultSolver(sparse.csc_matrix((2,2)),np.array([0.,1.]),A,rhs,
        [clarabel.ZeroConeT(1),clarabel.NonnegativeConeT(1),clarabel.SecondOrderConeT(3)],settings(5))
    r=solver.solve();assert str(r.status)=='Solved' and abs(r.x[0]-.5)<1e-7 and abs(r.x[1]-.25)<1e-7
    return {'fixed_displacement':.5,'exact_minimum_square':'1/4','solver_coordinates':r.x,'solver_status':str(r.status),
        'scope':'Floating interface/encoding check; the cone equivalence is elementary algebra, not inferred from this test.'}


def run(prior,bits,targets,limit):
    geometry=geometry_check();data,powers,rows,seeds,source,provenance=quad.load(prior,bits);ctx.prec=bits
    basis,metadata=quad.prepare(data,rows,bits);N=len(basis[0]['J']);C=len(powers);D=C+2*N;M=len(rows)
    W=np.array([[float(w) for w in r['weights']] for r in rows])
    J=np.array([[float(v) for v in b['J']] for b in basis]);K=np.array([[float(v) for v in b['K']] for b in basis])
    plus=sparse.hstack([sparse.csc_matrix(W),sparse.csc_matrix(J),sparse.csc_matrix(K)],format='csc')
    observation=sparse.vstack([plus,-plus],format='csc')
    obs_rhs=np.array([float((b['center']+b['quadratic_error']).upper()) for b in basis]+
        [float((-b['center']+b['quadratic_error']+r['B']).upper()) for r,b in zip(rows,basis)])
    identity=sparse.hstack([sparse.eye(C,format='csc'),sparse.csc_matrix((C,2*N))],format='csc')
    squares=sparse.hstack([sparse.csc_matrix((N,C+N)),sparse.eye(N,format='csc')],format='csc')
    linear=sparse.vstack([observation,identity,-identity,squares],format='csc')
    linear_rhs=np.r_[obs_rhs,[d[-1] for d in seeds],[-d[0] for d in seeds],np.ones(N)]
    cone,cone_rhs=cone_rows(N,C);matrix=sparse.vstack([linear,cone],format='csc');rhs=np.r_[linear_rhs,cone_rhs]
    cones=[clarabel.NonnegativeConeT(len(linear_rhs))]+[clarabel.SecondOrderConeT(3) for _ in range(N)]
    model_hash=core.sha(matrix.indptr.tobytes()+matrix.indices.tobytes()+matrix.data.tobytes()+rhs.tobytes())
    reports=[];domains=[list(d) for d in seeds];combinations={};start=time.monotonic()
    for column,(n,p,k) in enumerate(powers):
        if n>361 or len(seeds[column])==1 or (targets and n not in targets):continue
        remaining=list(seeds[column]);certificates=[]
        for sign in ([1,-1] if seeds[column][0]==0 else [-1,1]):
            skipped=len(remaining)==1;alpha=[F(0)]*M;r=None
            if not skipped:
                objective=np.zeros(D);objective[column]=-sign
                solver=clarabel.DefaultSolver(sparse.csc_matrix((D,D)),objective,matrix,rhs,cones,settings(limit))
                r=solver.solve()
                if len(r.z)>=2*M and np.isfinite(r.z[:2*M]).all():
                    lambdas=[F(round(max(0.,float(v))*10**9),10**9) for v in r.z[:2*M]]
                    alpha=[lambdas[i]-lambdas[M+i] for i in range(M)]
            multipliers=[[i,str(v)] for i,v in enumerate(alpha) if v];key=core.sha(core.canonical(multipliers))
            if key not in combinations:combinations[key]=quad.combine(rows,basis,alpha)
            bounds={mode:quad.objective(combinations[key],column,sign,seeds,mode) for mode in ['linear','independent_quadratic','quadratic']}
            certificate={'sign':sign,'multipliers':multipliers,'combination_sha256':key,
                'solver_status':str(r.status) if r is not None else 'SkippedExistingBoxBound',
                'solver_time':float(r.solve_time) if r is not None else 0,
                'solver_primal_coordinates':r.x if r is not None else None,
                'bounds':bounds}
            certificates.append(certificate)
            remaining=[v for v in remaining if not arb(sign*v)>core.decode(bounds['quadratic']['objective_upper_bound']).upper()]
            assert remaining,('Validated conic-proposed bound has no candidate',n)
            print(json.dumps({'event':'conic_sign','n':n,'sign':sign,'status':certificate['solver_status'],
                'remaining':remaining,'elapsed_seconds':time.monotonic()-start}),flush=True)
        controls={mode:[v for v in seeds[column] if all(not arb(c['sign']*v)>core.decode(c['bounds'][mode]['objective_upper_bound']).upper() for c in certificates)]
                  for mode in ['linear','independent_quadratic','quadratic']}
        assert all(controls.values()) and controls['quadratic']==remaining
        reports.append({'column':column,'n':n,'before':seeds[column],'after':remaining,'certificates':certificates,'control_candidates':controls})
        domains[column]=remaining
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'basis_source_sha256':core.sha(Path(quad.__file__).read_bytes()),
        'runtime_additions':{n:importlib.metadata.version(n) for n in ['clarabel','cffi','pycparser']},
        'precision_bits':bits,'height':2000,'additional_radius':'5e-3','requested_targets':targets,'solver_time_limit_seconds':limit,
        'geometry_check':geometry,'provenance':provenance,'basis':metadata,
        'float_model':{'variables':D,'rows':matrix.shape[0],'nonnegative_cone_dimension':len(linear_rhs),'lorentz_cones':N,'sparse_model_sha256':model_hash},
        'checks':reports,'domains':[{'n':n,'prime':p,'power':k,'candidates':d} for (n,p,k),d in zip(powers,domains)],
        'unique_targets':sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361),
        'combinations':{k:v['metadata'] for k,v in combinations.items()},
        'scope':'Conic models enforce y squared <= z <= 1 as a convex relaxation. Any finite proposed row multipliers are rounded and checked with the complete interval quadratic support, cubic remainder and tails. Primal coordinates are unverified proposals; solver status does not establish actual-field or nonlinear spectral feasibility.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prior',type=Path,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True);p.add_argument('--targets',type=int,nargs='*',default=[])
    p.add_argument('--time-limit',type=float,default=30);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.prior,a.precision,a.targets,a.time_limit);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'unique_targets':r['unique_targets']}))
