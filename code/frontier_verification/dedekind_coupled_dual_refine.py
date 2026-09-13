"""Iterate validated continuous dual bounds with integer box tightening."""
import argparse,json,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from flint import arb
import dedekind_coupled_recovery as core
import dedekind_coupled_dual as dual


def bound_box(matrix,rhs,column,sign,multipliers,domains):
    vector=[arb(0) for _ in matrix[0]];beta=arb(0)
    assert all(v>=0 for v in multipliers)
    for j,value in enumerate(multipliers):
        if value:
            scalar=arb(str(value));beta+=scalar*rhs[j]
            vector=[v+scalar*a for v,a in zip(vector,matrix[j])]
    residual=[(arb(sign) if k==column else arb(0))-v for k,v in enumerate(vector)]
    correction=sum((max((d[0]*v).upper(),(d[-1]*v).upper()) for v,d in zip(residual,domains)),arb(0))
    return {'weighted_rhs':core.encode(beta),'residual_support_bound':core.encode(correction),
            'objective_upper_bound':core.encode(beta+correction),
            'residual_sha256':core.sha(core.canonical([core.encode(v) for v in residual]))}


def run(path,initial_path):
    raw=path.read_bytes();data=json.loads(raw);initial_raw=initial_path.read_bytes();initial=json.loads(initial_raw)
    assert initial['status']=='passed' and initial['input_sha256']==core.sha(raw)
    assert initial['source_sha256']==core.sha(Path(dual.__file__).read_bytes())
    results=[]
    for old_case in initial['cases']:
        top=old_case['settings']['top'];bits=old_case['settings']['precision_bits'];delta=old_case['additional_radius']
        start=time.monotonic();powers,rows,settings=core.prepare(data,top,bits,delta)
        matrix,rhs=dual.inequalities(rows);domains=[list(range(5)) for _ in powers]
        # Recheck the complete initial certificate before importing its bounds.
        for target in old_case['targets']:
            for certificate in target['certificates']:
                lambdas=[F(0) for _ in rhs]
                for j,v in certificate['multipliers']:lambdas[j]=F(v)
                proof=dual.bound(matrix,rhs,target['column'],certificate['sign'],lambdas)
                assert all(proof[k]==certificate[k] for k in proof)
            domains[target['column']]=target['candidates']
        float_matrix=np.array([[float(v) for v in row] for row in matrix]);float_rhs=np.array([float(v) for v in rhs])
        rounds=[]
        for round_number in range(1,4*91+2):
            old=[list(d) for d in domains];changes=[]
            for column,(n,p,k) in enumerate(powers):
                if n>361 or len(old[column])==1:continue
                proofs=[]
                for sign in [-1,1]:
                    objective=np.zeros(len(powers));objective[column]=-sign
                    proposal=linprog(objective,A_ub=float_matrix,b_ub=float_rhs,bounds=[(d[0],d[-1]) for d in old],
                                     method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
                    lambdas=[F(round(max(0.,-float(v))*10**9),10**9) for v in proposal.ineqlin.marginals] if proposal.success else [F(0) for _ in rhs]
                    proof=bound_box(matrix,rhs,column,sign,lambdas,old)
                    proofs.append({'sign':sign,'solver_status':int(proposal.status),
                                   'multipliers':[[j,str(v)] for j,v in enumerate(lambdas) if v],**proof})
                remaining=[c for c in old[column] if all(not arb(proof['sign']*c)>core.decode(proof['objective_upper_bound']).upper() for proof in proofs)]
                assert remaining,('Validated bounds have no integer candidate',top,n)
                if remaining!=old[column]:
                    changes.append({'column':column,'n':n,'before':old[column],'after':remaining,'certificates':proofs})
                    domains[column]=remaining
            if not changes:break
            rounds.append({'round':round_number,'prior_domains_sha256':core.sha(core.canonical(old)),
                           'changes':changes,'remaining_domains_sha256':core.sha(core.canonical(domains))})
        else:raise AssertionError('Finite dual refinement did not stabilize')
        results.append({'settings':settings,'additional_radius':delta,'rounds':rounds,
                        'domains':[{'n':n,'prime':p,'power':k,'candidates':d} for (n,p,k),d in zip(powers,domains)],
                        'unique_targets':sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361)})
        print(json.dumps({'height':top,'unique_targets':results[-1]['unique_targets'],'new_rounds':len(rounds),
                          'elapsed_seconds':time.monotonic()-start}),flush=True)
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'core_sha256':core.sha(Path(core.__file__).read_bytes()),
            'initial_dual_sha256':core.sha(initial_raw),'input_sha256':core.sha(raw),'cases':results,
            'scope':'Initial rational dual certificates are revalidated, then integer box bounds are tightened using new rational dual certificates. No candidate seed from interval propagation or local arithmetic.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['input','initial','output']:p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();r=run(a.input,a.initial);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'cases':len(r['cases'])}))
