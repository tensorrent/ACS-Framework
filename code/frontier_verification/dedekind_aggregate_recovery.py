"""Recover integer Euler coefficients from Gaussian inequalities without fields."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from flint import arb,ctx
import dedekind_coupled_recovery as core
from dedekind_coupled_dual import inequalities,bound


def rows_for(data,observation):
    return [{'weights':[core.decode(w) for w in row['weights']],
             'R':core.decode(row['observations'][observation]['R']),'B':core.decode(row['prime_tail']),
             'metadata':{'n':row['center']}} for row in data['rows']]


def run(path,limit):
    raw=path.read_bytes();data=json.loads(raw);ctx.prec=224
    assert data['status']=='passed' and data['global_inputs']['degree']==4
    powers=[(r['n'],r['prime'],r['power']) for r in data['columns']];results=[]
    for observation in range(len(data['input_sha256'])):
        rows=rows_for(data,observation);fixed=core.eliminate(powers,rows);assert fixed['status']=='passed'
        matrix,rhs=inequalities(rows)
        floats=np.array([[float(x) for x in row] for row in matrix]);right=np.array([float(x) for x in rhs])
        targets=[]
        for column,(n,p,k) in enumerate(powers):
            if n>limit:continue
            certificates=[]
            for sign in [-1,1]:
                objective=np.zeros(len(powers));objective[column]=-sign
                proposal=linprog(objective,A_ub=floats,b_ub=right,bounds=(0,4),method='highs',
                    options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
                multipliers=[F(round(max(0.0,-float(v))*10**9),10**9) for v in proposal.ineqlin.marginals] if proposal.success else [F(0)]*len(rhs)
                proof=bound(matrix,rhs,column,sign,multipliers)
                certificates.append({'sign':sign,'multipliers':[[j,str(v)] for j,v in enumerate(multipliers) if v],
                    'solver_status':int(proposal.status),'solver_message':proposal.message,**proof})
            candidates=[c for c in range(5) if all(not arb(cert['sign']*c)>core.decode(cert['objective_upper_bound']).upper() for cert in certificates)]
            assert candidates,(observation,n)
            targets.append({'n':n,'prime':p,'power':k,'column':column,'candidates':candidates,'certificates':certificates})
        results.append({'observation_index':observation,'input_sha256':data['input_sha256'][observation],
                        'monotone_exclusion':fixed,'dual_targets':targets,
                        'monotone_unique_targets':sum(len(r['candidates'])==1 for r in fixed['domains'] if r['n']<=limit),
                        'dual_unique_targets':sum(len(r['candidates'])==1 for r in targets)})
        print(json.dumps({'event':'recovered','observation':observation,'monotone':results[-1]['monotone_unique_targets'],
                          'dual':results[-1]['dual_unique_targets'],'c7':next(r['candidates'] for r in targets if r['n']==7)}),flush=True)
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'measurement_sha256':hashlib.sha256(raw).hexdigest(),'target_limit':limit,'results':results,
            'scope':'Every coefficient starts in {0,1,2,3,4}. Monotone row exclusions and independent continuous dual proposals use only the supplied explicit-formula inequalities. Rounded nonnegative rational multipliers and full residual support validate all solver bounds. No local-power relations, Galois-group restrictions, field candidates or arithmetic coefficients are read.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--measurements',type=Path,required=True);p.add_argument('--target-limit',type=int,default=31);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.measurements,a.target_limit);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'observations':len(r['results'])}))
