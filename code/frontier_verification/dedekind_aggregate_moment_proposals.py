"""Propose all seventeen target duals with jointly sampled finite and moment changes."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from flint import arb,ctx
from dedekind_coupled_recovery import decode
from dedekind_coupled_dual import inequalities

RADII=['0','1/200','1/50','1/10']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run(measurements,inputs):
    ctx.prec=256;d=json.loads(measurements.read_text());cases=[];a=arb(1)/25
    assert d['global_inputs']=={'degree':4,'discriminant':576,'real_places':0,'complex_places':2,'top':20} and all(r['denominator']==25 for r in d['rows'])
    targets=[i for i,c in enumerate(d['columns']) if c['n']<=31];assert len(targets)==17
    for obs,path in enumerate(inputs):
        assert sha(path)==d['input_sha256'][obs]
        roots=json.loads(path.read_text())['positive_root_intervals'];N=len(roots)
        centers=[(F(x['lo'])+F(x['hi']))/2 for x in roots];mids=np.array([float(v) for v in centers])
        rows=[{'weights':[decode(w) for w in r['weights']],'R':decode(r['observations'][obs]['unwidened']),'B':decode(r['prime_tail'])} for r in d['rows']]
        matrix,rhs=inequalities(rows);A=np.array([[float(v) for v in row] for row in matrix]);b=np.array([float(v) for v in rhs]);J=len(b);K=A.shape[1]
        scales=np.array([float(decode(r['scale'])) for r in d['rows']]);u=np.log([r['center'] for r in d['rows']])
        tail_coeff=np.array([float(decode(r['scale'])*404*(-16+a/4).exp()*(arb(r['center']).log()/2).cosh()) for r in d['rows']])
        U0=float(decode(d['constant_moment_upper']))-np.sum(3/(2.25+mids*mids));assert U0>0
        coefficient_rows=sparse.hstack([-sparse.csr_matrix(A.T),-sparse.eye(K),sparse.csr_matrix((K,N))],format='csr')
        for radius in RADII:
            delta=F(radius);assert all(F(x['lo'])-delta>0 and F(x['hi'])+delta<20 for x in roots)
            positions=mids[:,None]+np.linspace(-float(delta),float(delta),33)[None,:]
            differences=-2*scales[None,None,:]*(np.exp(-.04*positions[:,:,None]**2)*np.cos(positions[:,:,None]*u)-np.exp(-.04*mids[:,None,None]**2)*np.cos(mids[:,None,None]*u))
            moment_changes=3/(2.25+positions*positions)-3/(2.25+mids[:,None]*mids[:,None])
            signed=np.stack([differences,-differences],axis=-1).reshape(N*33,J)-moment_changes.reshape(-1,1)*np.repeat(tail_coeff,2)[None,:]
            root_rows=sparse.hstack([sparse.csr_matrix(signed),sparse.csr_matrix((N*33,K)),-sparse.kron(sparse.eye(N),np.ones((33,1)),format='csr')],format='csr')
            constraints=sparse.vstack([coefficient_rows,root_rows],format='csr');objective=np.r_[b+np.repeat(tail_coeff*U0,2),np.full(K,4.),np.ones(N)]
            for column in targets:
                for sign in [-1,1]:
                    right=np.zeros(K+N*33);right[column]=-sign
                    proposed=linprog(objective,A_ub=constraints,b_ub=right,bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
                    values=proposed.x[:J] if proposed.success else np.zeros(J)
                    multipliers=[[i,str(F(round(max(0.,float(v))*10**9),10**9))] for i,v in enumerate(values) if round(max(0.,float(v))*10**9)]
                    cases.append({'observation_index':obs,'radius':radius,'column':column,'n':d['columns'][column]['n'],'sign':sign,'multipliers':multipliers,
                        'solver_status':int(proposed.status),'solver_message':proposed.message,'sampled_surrogate_score':float(proposed.fun) if proposed.success else None})
            print(json.dumps({'event':'joint_moment_proposals','observation':obs,'radius':radius,'target_count':17}),flush=True)
    return {'status':'proposed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [measurements]+inputs},'radii':RADII,'target_count':17,
            'sample_offsets_per_root':33,'rational_multiplier_grid':10**9,'cases':cases,
            'scope':'Floating sampled joint changes of the finite Gaussian sum and the known-zero moment propose rational duals for all seventeen targets. A baseline moment tail plus per-root increments is used. Scores are not continuum or optimality certificates; no local model, field list or held-out truth is supplied.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args();r=run(a.measurements,a.inputs)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'cases':len(r['cases'])}))
