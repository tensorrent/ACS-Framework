"""Quadratic relaxation proposals, validated with the exact squared-displacement relation."""
import argparse,json,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from flint import arb,ctx
import dedekind_coupled_recovery as core
import dedekind_quadratic_ordinate as quad


def run(prior,bits,time_limit,max_rounds):
    data,powers,rows,seeds,source,provenance=quad.load(prior,bits);ctx.prec=bits
    basis,metadata=quad.prepare(data,rows,bits);N=len(basis[0]['J'])
    W=np.array([[float(w) for w in r['weights']] for r in rows])
    J=np.array([[float(v) for v in b['J']] for b in basis]);K=np.array([[float(v) for v in b['K']] for b in basis])
    plus=sparse.hstack([sparse.csr_matrix(W),sparse.csr_matrix(J),sparse.csr_matrix(K)],format='csr')
    matrix=sparse.vstack([plus,-plus],format='csr')
    rhs=np.array([float((b['center']+b['quadratic_error']).upper()) for b in basis]+
        [float((-b['center']+b['quadratic_error']+r['B']).upper()) for r,b in zip(rows,basis)])
    domains=[list(d) for d in seeds];rounds=[];combinations={};all_proposals=[];start=time.monotonic()
    for number in range(1,max_rounds+1):
        old=[list(d) for d in domains];checks=[]
        for column,(n,p,k) in enumerate(powers):
            if n>361 or len(old[column])==1:continue
            remaining=list(old[column]);certificates=[]
            for sign in ([1,-1] if old[column][0]==0 else [-1,1]):
                skipped=len(remaining)==1;proposal=None;alpha=[F(0)]*len(rows)
                if not skipped:
                    objective=np.zeros(len(powers)+2*N);objective[column]=-sign
                    proposal=linprog(objective,A_ub=matrix,b_ub=rhs,
                        bounds=[(d[0],d[-1]) for d in old]+[(-1,1)]*N+[(0,1)]*N,method='highs-ipm',
                        options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9,'time_limit':time_limit})
                    marginals=getattr(getattr(proposal,'ineqlin',None),'marginals',None)
                    if marginals is not None and len(marginals)==2*len(rows) and np.isfinite(marginals).all():
                        lambdas=[F(round(max(0.,-float(v))*10**9),10**9) for v in marginals]
                        alpha=[lambdas[i]-lambdas[len(rows)+i] for i in range(len(rows))]
                multipliers=[[i,str(v)] for i,v in enumerate(alpha) if v];key=core.sha(core.canonical(multipliers))
                if key not in combinations:combinations[key]=quad.combine(rows,basis,alpha)
                proof=quad.objective(combinations[key],column,sign,old,'quadratic')
                certificate={'column':column,'n':n,'sign':sign,'multipliers':multipliers,'combination_sha256':key,
                    'solver_status':int(proposal.status) if proposal is not None else None,
                    'solver_skipped_after_singleton':skipped,'solver_message':proposal.message if proposal is not None else 'Existing opposite box bound',
                    'solver_objective':float(proposal.fun) if proposal is not None and proposal.fun is not None else None,**proof}
                certificates.append(certificate);all_proposals.append({k:certificate[k] for k in ['column','n','sign','multipliers','combination_sha256']})
                remaining=[v for v in remaining if not arb(sign*v)>core.decode(proof['objective_upper_bound']).upper()]
                assert remaining,('Certified quadratic bounds have no candidate',number,n)
            checks.append({'column':column,'n':n,'before':old[column],'after':remaining,'certificates':certificates});domains[column]=remaining
            print(json.dumps({'event':'quadratic_target','round':number,'n':n,'before':old[column],'after':remaining,
                'solver_statuses':[c['solver_status'] for c in certificates],'elapsed_seconds':time.monotonic()-start}),flush=True)
        changes=sum(a!=b for a,b in zip(old,domains))
        rounds.append({'round':number,'prior_domains_sha256':core.sha(core.canonical(old)),'checks':checks,
            'changed_targets':changes,'remaining_domains_sha256':core.sha(core.canonical(domains))})
        if not changes:break
    controls=[]
    for mode in ['linear','independent_quadratic','quadratic']:
        control=[list(d) for d in seeds];steps=[]
        for number in range(1,4*91+2):
            old=[list(d) for d in control];checks=[]
            for p in all_proposals:
                column=p['column']
                if len(old[column])==1:continue
                proof=quad.objective(combinations[p['combination_sha256']],column,p['sign'],old,mode)
                after=[v for v in control[column] if not arb(p['sign']*v)>core.decode(proof['objective_upper_bound']).upper()]
                assert after
                checks.append({**p,'before':list(control[column]),'after':after,**proof});control[column]=after
            changes=sum(a!=b for a,b in zip(old,control))
            steps.append({'round':number,'prior_domains_sha256':core.sha(core.canonical(old)),'checks':checks,
                'changed_targets':changes,'remaining_domains_sha256':core.sha(core.canonical(control))})
            if not changes:break
        else:raise AssertionError('Finite certificate closure failed to stabilize')
        controls.append({'mode':mode,'rounds':steps,'domains':[{'n':n,'prime':p,'power':k,'candidates':d} for (n,p,k),d in zip(powers,control)],
            'unique_targets':sum(len(d)==1 for (n,p,k),d in zip(powers,control) if n<=361)})
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'basis_source_sha256':core.sha(Path(quad.__file__).read_bytes()),
        'precision_bits':bits,'height':2000,'additional_radius':'5e-3','solver_method':'highs-ipm','solver_time_limit_seconds':time_limit,
        'max_rounds':max_rounds,'provenance':provenance,'basis':metadata,'rounds':rounds,
        'domains':[{'n':n,'prime':p,'power':k,'candidates':d} for (n,p,k),d in zip(powers,domains)],
        'unique_targets':sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361),'stabilized':rounds[-1]['changed_targets']==0,
        'combinations':{k:v['metadata'] for k,v in combinations.items()},'controls':controls,'elapsed_solver_seconds':time.monotonic()-start,
        'scope':'LP proposals relax each squared displacement to a separate [0,1] coordinate. Certified scalar quadratic support restores the exact square relation. All controls reapply the complete proposal collection independently from the same 81 previously certified domains. Solver output never certifies feasibility or optimality.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prior',type=Path,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True);p.add_argument('--time-limit',type=float,default=15)
    p.add_argument('--max-rounds',type=int,default=4);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.prior,a.precision,a.time_limit,a.max_rounds);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'unique_targets':r['unique_targets'],'controls':{c['mode']:c['unique_targets'] for c in r['controls']}}))
