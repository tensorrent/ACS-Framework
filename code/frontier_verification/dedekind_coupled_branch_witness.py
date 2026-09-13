"""Seek integer assignments for non-excluded target branches; validate intervals."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from flint import arb
import dedekind_coupled_recovery as core
import dedekind_coupled_dual as dual


def run(path,refined_path,branches_path):
    raw=path.read_bytes();data=json.loads(raw);refined_raw=refined_path.read_bytes();refined=json.loads(refined_raw)
    branches_raw=branches_path.read_bytes();branches=json.loads(branches_raw)
    assert refined['input_sha256']==branches['input_sha256']==core.sha(raw)
    assert branches['refined_sha256']==core.sha(refined_raw)
    case=next(c for c in refined['cases'] if c['settings']['top']==220)
    powers,rows,settings=core.prepare(data,220,224,'0');matrix,rhs=dual.inequalities(rows)
    extended=np.column_stack([np.array([[float(v) for v in r] for r in matrix]),-np.ones(len(rhs))])
    right=np.array([float(v) for v in rhs]);objective=np.zeros(len(powers)+1);objective[-1]=1
    reports=[]
    for assignment in branches['surviving_assignments']:
        domains=[list(r['candidates']) for r in case['domains']]
        for n,v in assignment.items():domains[next(i for i,(m,p,k) in enumerate(powers) if m==int(n))]=[v]
        proposal=linprog(objective,A_ub=extended,b_ub=right,bounds=[(d[0],d[-1]) for d in domains]+[(0,None)],
                         method='highs',integrality=[1]*len(powers)+[0],options={'time_limit':60,'mip_rel_gap':0})
        result={'assignment':assignment,'solver_status':int(proposal.status),'solver_message':proposal.message,
                'proposed_violation':float(proposal.fun) if proposal.fun is not None else None,'verified_feasible':False}
        if proposal.x is not None:
            values=[round(float(v)) for v in proposal.x[:-1]]
            assert all(v in d for v,d in zip(values,domains))
            checks=[];valid=True
            for j,row in enumerate(rows):
                total=sum((w*c for w,c in zip(row['weights'],values)),arb(0))
                lower=total-row['R'].lower();upper=row['R'].upper()-total
                passed=lower>0 and upper>0
                valid=valid and passed
                checks.append({'row':j,'target':row['metadata']['n'],'lower_gap':core.encode(lower),
                               'upper_gap':core.encode(upper),'strict_inclusion':passed})
            result.update(verified_feasible=valid,coefficients=values,checks=checks,tail_assignment='0')
        reports.append(result)
        print(json.dumps({'assignment':assignment,'status':result['solver_status'],'verified_feasible':result['verified_feasible']}),flush=True)
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'input_sha256':core.sha(raw),
            'refined_sha256':core.sha(refined_raw),'branches_sha256':core.sha(branches_raw),'settings':settings,'proposals':reports,
            'scope':'MILP only proposes integer vectors. Strict interval inclusion in every measurement with tail zero is required for feasibility. Such a vector models this finite relaxation, not another number field or a different zero spectrum.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['input','refined','branches','output']:p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();r=run(a.input,a.refined,a.branches);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'verified_assignments':[p['assignment'] for p in r['proposals'] if p['verified_feasible']]}))
