"""Exhaust the eight remaining target pairs with validated separation certificates."""
import argparse,itertools,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from flint import arb
import dedekind_coupled_recovery as core
import dedekind_coupled_dual as dual


def separation(matrix,rhs,multipliers,domains):
    assert all(v>=0 for v in multipliers)
    vector=[arb(0) for _ in matrix[0]];beta=arb(0)
    for j,value in enumerate(multipliers):
        if value:
            scalar=arb(str(value));beta+=scalar*rhs[j]
            vector=[v+scalar*a for v,a in zip(vector,matrix[j])]
    lower=sum((min((v*d[0]).lower(),(v*d[-1]).lower()) for v,d in zip(vector,domains)),arb(0))
    return {'weighted_rhs':core.encode(beta),'box_minimum_lower_bound':core.encode(lower),
            'strict_separation_gap':core.encode(lower-beta),'excluded':lower>beta}


def run(path,refined_path):
    raw=path.read_bytes();data=json.loads(raw);refined_raw=refined_path.read_bytes();refined=json.loads(refined_raw)
    assert refined['status']=='passed' and refined['input_sha256']==core.sha(raw)
    case=next(c for c in refined['cases'] if c['settings']['top']==220)
    powers,rows,settings=core.prepare(data,220,224,'0');matrix,rhs=dual.inequalities(rows)
    initial=[r['candidates'] for r in case['domains']]
    unknown=[i for i,((n,p,k),domain) in enumerate(zip(powers,initial)) if n<=361 and len(domain)>1]
    assert [powers[i][0] for i in unknown]==[359,361]
    floats=np.array([[float(v) for v in r] for r in matrix]);right=np.array([float(v) for v in rhs])
    extended=np.column_stack([floats,-np.ones(len(rhs))]);objective=np.zeros(len(powers)+1);objective[-1]=1
    reports=[]
    for values in itertools.product(*(initial[i] for i in unknown)):
        domains=[list(d) for d in initial]
        for i,v in zip(unknown,values):domains[i]=[v]
        proposal=linprog(objective,A_ub=extended,b_ub=right,bounds=[(d[0],d[-1]) for d in domains]+[(0,None)],
                         method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
        multipliers=[F(round(max(0.,-float(v))*10**9),10**9) for v in proposal.ineqlin.marginals] if proposal.success else [F(0) for _ in rhs]
        proof=separation(matrix,rhs,multipliers,domains)
        reports.append({'target_assignment':dict(zip(map(str,[powers[i][0] for i in unknown]),values)),
                        'domains_sha256':core.sha(core.canonical(domains)),
                        'solver_status':int(proposal.status),'proposed_uniform_violation':float(proposal.fun) if proposal.success else None,
                        'multipliers':[[j,str(v)] for j,v in enumerate(multipliers) if v],**proof})
        print(json.dumps({'assignment':reports[-1]['target_assignment'],'excluded':proof['excluded'],
                          'gap':core.decode(proof['strict_separation_gap']).str(20)}),flush=True)
    survivors=[r['target_assignment'] for r in reports if not r['excluded']]
    assert survivors
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'input_sha256':core.sha(raw),
            'refined_sha256':core.sha(refined_raw),'settings':settings,'branches':reports,'surviving_assignments':survivors,
            'scope':'All eight remaining target pairs enumerated. A strictly positive rational-multiplier separation gap proves the entire candidate box infeasible. A non-excluded branch is not certified feasible by the float solver.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['input','refined','output']:p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();r=run(a.input,a.refined);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'survivors':r['surviving_assignments']}))
