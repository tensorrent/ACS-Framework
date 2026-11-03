"""Continuous LP proposals, validated by rational multipliers and interval bounds.

The LP solver is not trusted to prove any coefficient bound. Each proposed
nonnegative multiplier vector is rounded to exact rationals, then a direct
weighted-inequality argument bounds the objective including its residual.
"""
import argparse,hashlib,json,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from flint import arb,ctx
import dedekind_coupled_recovery as core


def inequalities(rows):
    matrix=[];rhs=[]
    for row in rows:
        matrix.append([w.lower() for w in row['weights']]);rhs.append(row['R'].upper())
        matrix.append([-w.upper() for w in row['weights']]);rhs.append((-row['R'].lower()+row['B'].upper()).upper())
    return matrix,rhs


def bound(matrix,rhs,column,sign,multipliers):
    assert sign in [-1,1] and all(v>=0 for v in multipliers)
    vector=[arb(0) for _ in matrix[0]];beta=arb(0)
    for j,value in enumerate(multipliers):
        if value:
            scalar=arb(str(value));beta+=scalar*rhs[j]
            vector=[v+scalar*a for v,a in zip(vector,matrix[j])]
    residual=[(arb(sign) if k==column else arb(0))-v for k,v in enumerate(vector)]
    correction=4*sum((max(arb(0),v.upper()) for v in residual),arb(0))
    upper=beta+correction
    return {'weighted_rhs':core.encode(beta),'residual_support_bound':core.encode(correction),
            'objective_upper_bound':core.encode(upper),
            'residual_sha256':core.sha(core.canonical([core.encode(v) for v in residual]))}


def run(path,bits,heights,delta):
    raw=path.read_bytes();data=json.loads(raw);reports=[]
    for top in heights:
        start=time.monotonic();powers,rows,settings=core.prepare(data,top,bits,delta)
        matrix,rhs=inequalities(rows)
        floats=np.array([[float(v) for v in row] for row in matrix]);right=np.array([float(v) for v in rhs])
        targets=[]
        for column,(n,p,k) in enumerate(powers):
            if n>361:continue
            certificates=[]
            for sign in [-1,1]:
                objective=np.zeros(len(powers));objective[column]=-sign
                proposal=linprog(objective,A_ub=floats,b_ub=right,bounds=(0,4),method='highs',
                                 options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
                if proposal.success:
                    lambdas=[F(round(max(0.0,-float(v))*10**9),10**9) for v in proposal.ineqlin.marginals]
                else:lambdas=[F(0) for _ in rhs]
                proof=bound(matrix,rhs,column,sign,lambdas)
                certificates.append({'sign':sign,'solver_status':int(proposal.status),'solver_message':proposal.message,
                                     'solver_objective':float(proposal.fun) if proposal.success else None,
                                     'multipliers':[[j,str(v)] for j,v in enumerate(lambdas) if v],**proof})
            candidates=[c for c in range(5) if all(not arb(cert['sign']*c)>core.decode(cert['objective_upper_bound']).upper() for cert in certificates)]
            assert candidates,('Validated dual bounds contradict coefficient integrality',top,n)
            targets.append({'n':n,'prime':p,'power':k,'column':column,'candidates':candidates,'certificates':certificates})
        reports.append({'settings':settings,'additional_radius':delta,'targets':targets,
                        'unique_targets':sum(len(r['candidates'])==1 for r in targets),
                        'measurement_metadata_sha256':core.sha(core.canonical([r['metadata'] for r in rows]))})
        print(json.dumps({'height':top,'delta':delta,'unique_targets':reports[-1]['unique_targets'],
                          'solver_successes':sum(c['solver_status']==0 for t in targets for c in t['certificates']),
                          'elapsed_seconds':time.monotonic()-start}),flush=True)
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),
            'core_sha256':core.sha(Path(core.__file__).read_bytes()),'input_sha256':core.sha(raw),'cases':reports,
            'scope':'Continuous relaxation with 0..4 bounds only. Rational nonnegative multipliers and interval residual support validate every bound even if a float proposal is inaccurate. Integer candidates are retained conservatively.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True)
    p.add_argument('--heights',type=int,nargs='+',default=[220,600,1000,1500,2000])
    p.add_argument('--delta',default='0');p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=run(a.input,a.precision,a.heights,a.delta)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'cases':len(r['cases'])}))
