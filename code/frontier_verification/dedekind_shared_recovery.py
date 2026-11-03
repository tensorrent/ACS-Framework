"""Bounded shared-error LP proposals with complete interval dual validation."""
import argparse,json,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from flint import arb,ctx
import dedekind_coupled_recovery as core
import dedekind_shared_ordinate as shared


def run(prior,bits,limit,max_rounds):
    data,powers,rows,seeds,provenance=shared.load(prior,2000,bits,'5e-3');ctx.prec=bits
    basis,basis_metadata=shared.shared_basis(data,rows,2000,bits,'5e-3')
    W=np.array([[float(w) for w in row['weights']] for row in rows])
    J=np.array([[float(j) for j in b['J']] for b in basis])
    plus=sparse.hstack([sparse.csr_matrix(W),sparse.csr_matrix(J)],format='csr')
    matrix=sparse.vstack([plus,-plus],format='csr')
    rhs=np.array([float((b['center']+b['error']).upper()) for b in basis]+
                 [float((-b['center']+b['error']+r['B']).upper()) for b,r in zip(basis,rows)])
    domains=[list(d) for d in seeds];rounds=[];start=time.monotonic()
    for round_number in range(1,max_rounds+1):
        old=[list(d) for d in domains];checks=[];changes=0
        for column,(n,p,k) in enumerate(powers):
            if n>361 or len(old[column])==1:continue
            remaining=list(old[column]);certificates=[]
            # This uses only the existing candidate domain, never an expected
            # answer. A singleton needs no second optimization: a zero dual
            # supplies the already established opposite box bound.
            order=[1,-1] if old[column][0]==0 else [-1,1]
            for sign in order:
                skipped=len(remaining)==1;proposal=None;alpha=[F(0)]*len(rows)
                if not skipped:
                    objective=np.zeros(len(powers)+len(basis[0]['J']));objective[column]=-sign
                    proposal=linprog(objective,A_ub=matrix,b_ub=rhs,
                        bounds=[(d[0],d[-1]) for d in old]+[(-1,1)]*len(basis[0]['J']),method='highs-ipm',
                        options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9,'time_limit':limit})
                    marginals=getattr(getattr(proposal,'ineqlin',None),'marginals',None)
                    if marginals is not None and len(marginals)==2*len(rows) and np.isfinite(marginals).all():
                        lambdas=[F(round(max(0.,-float(v))*10**9),10**9) for v in marginals]
                        alpha=[lambdas[i]-lambdas[len(rows)+i] for i in range(len(rows))]
                proof=shared.shared_bound(rows,basis,column,sign,alpha,old)
                certificate={'sign':sign,'solver_skipped_after_singleton':skipped,
                  'solver_status':int(proposal.status) if proposal is not None else None,
                  'solver_message':proposal.message if proposal is not None else 'Opposite bound already supplied by coefficient box',
                  'solver_objective':float(proposal.fun) if proposal is not None and proposal.fun is not None else None,
                  'multipliers':[[i,str(v)] for i,v in enumerate(alpha) if v],**proof}
                certificates.append(certificate)
                remaining=[v for v in remaining if not arb(sign*v)>core.decode(proof['objective_upper_bound']).upper()]
                assert remaining,('Validated shared bounds have no candidate',round_number,n)
            checks.append({'column':column,'n':n,'before':old[column],'after':remaining,'certificates':certificates})
            if remaining!=old[column]:domains[column]=remaining;changes+=1
            print(json.dumps({'event':'shared_target','round':round_number,'n':n,'before':old[column],'after':remaining,
                'solver_statuses':[c['solver_status'] for c in certificates],'elapsed_seconds':time.monotonic()-start}),flush=True)
        rounds.append({'round':round_number,'prior_domains_sha256':core.sha(core.canonical(old)),
           'checks':checks,'changed_targets':changes,'remaining_domains_sha256':core.sha(core.canonical(domains))})
        if not changes:break
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),
       'basis_source_sha256':core.sha(Path(shared.__file__).read_bytes()),'precision_bits':bits,'height':2000,'additional_radius':'5e-3',
       'solver_method':'highs-ipm','solver_time_limit_seconds':limit,'max_rounds':max_rounds,'provenance':provenance,'shared_basis':basis_metadata,
       'measurement_metadata_sha256':core.sha(core.canonical([r['metadata'] for r in rows])),
       'rounds':rounds,'domains':[{'n':n,'prime':p,'power':k,'candidates':d} for (n,p,k),d in zip(powers,domains)],
       'unique_targets':sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361),
       'stabilized':rounds[-1]['changed_targets']==0,'elapsed_solver_seconds':time.monotonic()-start,
       'scope':'Full 7602 common ordinate variables and all 455 retained measurements. Float solvers, including limited or incomplete proposals, never certify a result; every rational signed combination receives full interval residual, common-error and tail bounds. Singleton cases use the old opposite box bound without an unnecessary solve.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prior',type=Path,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True);p.add_argument('--time-limit',type=float,default=15)
    p.add_argument('--max-rounds',type=int,default=8);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.prior,a.precision,a.time_limit,a.max_rounds);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'unique_targets':r['unique_targets'],'rounds':len(r['rounds']),'stabilized':r['stabilized']}))
