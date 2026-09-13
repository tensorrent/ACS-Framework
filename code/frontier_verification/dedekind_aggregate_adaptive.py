"""Re-optimize joint-moment duals after valid local-domain reductions."""
import argparse, hashlib, json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from flint import arb, ctx
from dedekind_coupled_recovery import encode, decode
from dedekind_coupled_dual import inequalities
from dedekind_coefficient_recovery import local_models
from dedekind_aggregate_moment_certificate import certify

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def coefficient(model,k): return sum(f for e,f in model if k%f==0)

def setup(m,source,obs,radius):
    ctx.prec=256; roots=source['positive_root_intervals']; delta=F(radius); a=arb(1)/25
    rows=[{'weights':[decode(w) for w in r['weights']], 'R':decode(r['observations'][obs]['unwidened']), 'B':decode(r['prime_tail'])} for r in m['rows']]
    matrix,rhs=inequalities(rows); A=np.array([[float(v) for v in row] for row in matrix]); b=np.array([float(v) for v in rhs]); J,K=A.shape; N=len(roots)
    mids=np.array([float((F(r['lo'])+F(r['hi']))/2) for r in roots]); positions=mids[:,None]+np.linspace(-float(delta),float(delta),33)[None,:]
    scales=np.array([float(decode(r['scale'])) for r in m['rows']]); u=np.log([r['center'] for r in m['rows']])
    tail=np.array([float(decode(r['scale'])*404*(-16+a/4).exp()*(arb(r['center']).log()/2).cosh()) for r in m['rows']])
    U0=float(decode(m['constant_moment_upper']))-np.sum(3/(2.25+mids*mids)); assert U0>0
    differences=-2*scales[None,None,:]*(np.exp(-.04*positions[:,:,None]**2)*np.cos(positions[:,:,None]*u)-np.exp(-.04*mids[:,None,None]**2)*np.cos(mids[:,None,None]*u))
    changes=3/(2.25+positions*positions)-3/(2.25+mids[:,None]*mids[:,None])
    signed=np.stack([differences,-differences],axis=-1).reshape(N*33,J)-changes.reshape(-1,1)*np.repeat(tail,2)[None,:]
    coefficients=sparse.hstack([-sparse.csr_matrix(A.T),-sparse.eye(K),sparse.csr_matrix((K,N))],format='csr')
    error=sparse.hstack([sparse.csr_matrix(signed),sparse.csr_matrix((N*33,K)),-sparse.kron(sparse.eye(N),np.ones((33,1)),format='csr')],format='csr')
    constraints=sparse.vstack([coefficients,error],format='csr')
    return matrix,rhs,A,b,tail,U0,constraints,N

def propose(prepared,domains,column,sign):
    matrix,rhs,A,b,tail,U0,constraints,N=prepared; J,K=A.shape
    lo=np.array([d[0] for d in domains],dtype=float); hi=np.array([d[-1] for d in domains],dtype=float)
    # support(r,D) = lo*r + (hi-lo)*max(r,0), also for domains with holes.
    objective=np.r_[b-A@lo+np.repeat(tail*U0,2),hi-lo,np.ones(N)]
    right=np.zeros(K+N*33); right[column]=-sign
    p=linprog(objective,A_ub=constraints,b_ub=right,bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    values=p.x[:J] if p.success else np.zeros(J)
    multipliers=[[i,str(F(round(max(0.,float(v))*10**9),10**9))] for i,v in enumerate(values) if round(max(0.,float(v))*10**9)]
    return {'multipliers':multipliers,'solver_status':int(p.status),'solver_message':p.message,
            'sampled_surrogate_score':float(p.fun+sign*lo[column]) if p.success else None}

def domain_objective(prepared,c,domains,budget):
    ctx.prec=256; matrix,rhs=prepared[:2]; beta=arb(0); vector=[arb(0) for _ in domains]
    for j,value in c['multipliers']:
        v=arb(value); assert F(value)>=0; beta+=v*rhs[j]; vector=[x+v*y for x,y in zip(vector,matrix[j])]
    residual=[(arb(c['sign']) if k==c['column'] else arb(0))-v for k,v in enumerate(vector)]
    support=sum((max((r*v).upper() for v in d) for r,d in zip(residual,domains)),arb(0))
    return beta+support+decode(budget)

def run(measurements,inputs,prior_feedback,prior_audit):
    m=json.loads(measurements.read_text()); sources=[json.loads(x.read_text()) for x in inputs]
    old=json.loads(prior_feedback.read_text()); audit=json.loads(prior_audit.read_text())
    assert old['status']==audit['status']=='passed' and audit['inputs_sha256'][prior_feedback.name]==sha(prior_feedback)
    assert old['inputs_sha256'][measurements.name]==sha(measurements)
    assert [sha(p) for p in inputs]==m['input_sha256']
    assert m['global_inputs']=={'degree':4,'discriminant':576,'real_places':0,'complex_places':2,'top':20}
    columns=m['columns']; assert columns==old['columns']; models=sorted(local_models(4,False)+local_models(4,True))
    groups={p:[i for i,c in enumerate(columns) if c['prime']==p] for p in sorted({c['prime'] for c in columns})}
    cases=[]; certificates=[]
    for seed_index,seed in enumerate(old['cases']):
        if seed['method']!='coupled': continue
        obs=seed['observation_index']; radius=seed['radius']; profile=seed['profile']; prepared=setup(m,sources[obs],obs,radius)
        domains=[list(d) for d in seed['final_domains']]; initial=[list(d) for d in domains]; steps=[]
        for iteration in range(1,4*len(columns)+2):
            before=[list(d) for d in domains]; retained=[]; local_removed=[]
            for prime,indices in groups.items():
                ids=[j for j,model in enumerate(models) if (profile=='degree_only' or any(e>1 for e,f in model)==(576%prime==0)) and all(coefficient(model,columns[i]['power']) in before[i] for i in indices)]
                assert ids; retained.append({'prime':prime,'model_ids':ids})
                for i in indices:
                    values=sorted({coefficient(models[j],columns[i]['power']) for j in ids})
                    for v in sorted(set(before[i])-set(values)): local_removed.append({'column':i,'n':columns[i]['n'],'candidate':v,'prime':prime})
                    domains[i]=values
            local_removed.sort(key=lambda r:(r['column'],r['candidate'])); after_local=[list(d) for d in domains]
            proposals=[]; removed={}
            for column,c in enumerate(columns):
                if c['n']>31 or len(after_local[column])==1: continue
                for sign in [-1,1]:
                    proposal={**propose(prepared,after_local,column,sign),'observation_index':obs,'radius':radius,'profile':profile,'column':column,'n':c['n'],'sign':sign,
                              'case_index':len(cases),'iteration':iteration,'premise_domains_sha256':digest(after_local),'certificate_index':len(certificates)}
                    proof=certify(m,sources[obs],proposal); certificates.append(proof)
                    upper=domain_objective(prepared,proposal,after_local,proof['methods']['coupled']['total_zero_and_input_budget'])
                    proposal['domain_objective_upper_bound']=encode(upper); proposals.append(proposal)
                    for value in after_local[column]:
                        if (column,value) not in removed and arb(sign*value)>upper.upper():
                            removed[column,value]={'column':column,'n':c['n'],'candidate':value,'sign':sign,'certificate_index':proposal['certificate_index']}
            for column,value in removed: domains[column].remove(value)
            assert all(domains)
            steps.append({'iteration':iteration,'before_domains_sha256':digest(before),'local_models':retained,'local_removals':local_removed,
                          'after_local_sha256':digest(after_local),'proposals':proposals,'dual_removals':list(removed.values()),'after_domains_sha256':digest(domains)})
            print(json.dumps({'event':'adaptive_round','observation':obs,'radius':radius,'profile':profile,'iteration':iteration,'proposals':len(proposals),
                              'local_removals':len(local_removed),'dual_removals':len(removed),'unique_targets':sum(len(d)==1 for c,d in zip(columns,domains) if c['n']<=31)}),flush=True)
            if domains==before: break
        else: raise AssertionError('Finite domain iteration did not stabilize')
        cases.append({'observation_index':obs,'radius':radius,'profile':profile,'prior_case_index':seed_index,'input_domains':initial,'rounds':steps,'final_domains':domains,
                      'initial_unique_targets':sum(len(d)==1 for c,d in zip(columns,initial) if c['n']<=31),
                      'adaptive_unique_targets':sum(len(d)==1 for c,d in zip(columns,domains) if c['n']<=31),'adaptive_unique_support':sum(len(d)==1 for d in domains)})
    assert len(cases)==16
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [measurements,prior_feedback,prior_audit]+inputs},
            'columns':columns,'catalog':models,'sample_offsets_per_root':33,'rational_multiplier_grid':10**9,'cases':cases,'certificates':certificates,
            'scope':'At each round, sampled LPs propose new rational multipliers for unresolved targets using only previously justified domains at the same radius/profile. Every new vector receives a fresh real interval uncertainty certificate before producer deductions. No arithmetic coefficients or field catalogue are read. The stopping condition is no further deduction by this specific update, not global optimality or realization.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','prior-feedback','prior-audit','output']: p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True); a=p.parse_args(); r=run(a.measurements,a.inputs,a.prior_feedback,a.prior_audit)
    a.output.write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps({'status':r['status'],'cases':len(r['cases']),'certificates':len(r['certificates'])}))
