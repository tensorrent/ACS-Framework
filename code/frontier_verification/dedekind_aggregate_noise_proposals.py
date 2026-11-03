"""Propose rational duals using a floating sampled common-root error objective."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from flint import arb,ctx
from dedekind_coupled_recovery import decode
from dedekind_coupled_dual import inequalities

RADII=['0','1/500','1/200','1/100','1/50','1/20','3/50','7/100','1/10','13/100','7/50','1/5']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run(measurements,inputs):
    ctx.prec=256;d=json.loads(measurements.read_text());cases=[];a=arb(1)/25
    assert d['global_inputs']=={'degree':4,'discriminant':576,'real_places':0,'complex_places':2,'top':20}
    assert all(r['denominator']==25 for r in d['rows'])
    for obs,path in enumerate(inputs):
        assert sha(path)==d['input_sha256'][obs]
        roots=json.loads(path.read_text())['positive_root_intervals'];N=len(roots)
        mids=np.array([float(arb(str((F(x['lo'])+F(x['hi']))/2))) for x in roots])
        rows=[{'weights':[decode(w) for w in r['weights']],'R':decode(r['observations'][obs]['unwidened']),'B':decode(r['prime_tail'])} for r in d['rows']]
        matrix,rhs=inequalities(rows);A=np.array([[float(v) for v in row] for row in matrix]);b=np.array([float(v) for v in rhs]);J=len(b);K=A.shape[1]
        scales=np.array([float(decode(r['scale'])) for r in d['rows']]);u=np.log([r['center'] for r in d['rows']])
        column=next(i for i,x in enumerate(d['columns']) if x['n']==7)
        coefficient_rows=sparse.hstack([-sparse.csr_matrix(A.T),-sparse.eye(K),sparse.csr_matrix((K,N))],format='csr')
        for radius in RADII:
            delta=F(radius);wide=[arb(str(F(x['lo'])-delta)).union(arb(str(F(x['hi'])+delta))) for x in roots]
            assert all(x>0 and x<20 for x in wide)
            U=decode(d['constant_moment_upper'])-sum((3/(arb('9/4')+x*x) for x in wide),arb(0));assert U>0
            tails=np.array([float((decode(r['scale'])*U*404*(-16+a/4).exp()*(arb(r['center']).log()/2).cosh()).upper()) for r in d['rows']])
            offsets=np.linspace(-float(delta),float(delta),33);positions=mids[:,None]+offsets[None,:]
            differences=-2*scales[None,None,:]*(np.exp(-.04*positions[:,:,None]**2)*np.cos(positions[:,:,None]*u)-np.exp(-.04*mids[:,None,None]**2)*np.cos(mids[:,None,None]*u))
            signed=np.stack([differences,-differences],axis=-1).reshape(N*33,J)
            root_rows=sparse.hstack([sparse.csr_matrix(signed),sparse.csr_matrix((N*33,K)),-sparse.kron(sparse.eye(N),np.ones((33,1)),format='csr')],format='csr')
            constraints=sparse.vstack([coefficient_rows,root_rows],format='csr');objective=np.r_[b+np.repeat(tails,2),np.full(K,4.),np.ones(N)]
            for sign in [-1,1]:
                right=np.zeros(K+N*33);right[column]=-sign
                proposal=linprog(objective,A_ub=constraints,b_ub=right,bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
                values=proposal.x[:J] if proposal.success else np.zeros(J)
                multipliers=[[i,str(F(round(max(0.,float(v))*10**9),10**9))] for i,v in enumerate(values) if round(max(0.,float(v))*10**9)]
                cases.append({'observation_index':obs,'radius':radius,'sign':sign,'column':column,'multipliers':multipliers,
                    'solver_status':int(proposal.status),'solver_message':proposal.message,'sampled_surrogate_score':float(proposal.fun) if proposal.success else None})
            print(json.dumps({'event':'proposals','observation':obs,'radius':radius,'statuses':[x['solver_status'] for x in cases[-2:]]}),flush=True)
    return {'status':'proposed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [measurements]+inputs},
            'radii':RADII,'sample_offsets_per_root':33,'rational_multiplier_grid':10**9,'cases':cases,
            'scope':'Floating sampled-error minimization proposes nonnegative rational duals. The sampled score is not a bound for continuous ordinate uncertainty, not a certified relaxation optimum, and not a coefficient certificate. Every proposal requires separate interval validation, including all coefficient residuals and unconditional tails. No local model, field catalogue or arithmetic truth is used.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--measurements',type=Path,required=True);p.add_argument('--inputs',type=Path,nargs=2,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=run(a.measurements,a.inputs);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'cases':len(r['cases'])}))
