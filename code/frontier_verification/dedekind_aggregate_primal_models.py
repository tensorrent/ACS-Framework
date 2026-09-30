"""Use local-model convex hulls and seek integer witnesses for simultaneous cuts."""
import argparse,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from dedekind_coefficient_recovery import local_models

DUAL_GRID=10**9
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def coefficient(model,k):return sum(f for e,f in model if k%f==0)

def groups_for(columns,domains,profile):
    catalog=sorted(local_models(4,False)+local_models(4,True));groups=[];projected=[list(d) for d in domains];removed=[]
    for prime in sorted({c['prime'] for c in columns}):
        indices=[i for i,c in enumerate(columns) if c['prime']==prime];patterns={}
        for index,model in enumerate(catalog):
            if profile=='degree_discriminant' and any(e>1 for e,f in model)!=(576%prime==0):continue
            values=tuple(coefficient(model,columns[i]['power']) for i in indices)
            if all(v in domains[i] for i,v in zip(indices,values)):patterns.setdefault(values,[]).append(index)
        assert patterns
        groups.append({'prime':prime,'columns':indices,'patterns':[{'coefficients':list(v),'model_ids':ids} for v,ids in sorted(patterns.items())]})
        for k,i in enumerate(indices):
            values=sorted({v[k] for v in patterns})
            for v in sorted(set(domains[i])-set(values)):removed.append({'column':i,'n':columns[i]['n'],'candidate':v,'prime':prime})
            projected[i]=values
    removed.sort(key=lambda r:(r['column'],r['candidate']));return groups,projected,removed

def numeric_system(cuts,selected,groups,column_count):
    descriptors=[];offsets=[]
    for g in groups:
        offsets.append(len(descriptors));descriptors.extend((g,p) for p in g['patterns'])
    exponents={j:max([1,abs(cuts[j]['rhs'])]+[abs(v) for v in cuts[j]['coefficients']]).bit_length() for j in selected}
    C=np.array([[math.ldexp(float(sum(cuts[j]['coefficients'][i]*v for i,v in zip(g['columns'],p['coefficients']))),-exponents[j]) for g,p in descriptors] for j in selected])
    rhs=np.array([math.ldexp(float(cuts[j]['rhs']),-exponents[j]) for j in selected])
    row=[];col=[]
    for k,g in enumerate(groups):
        for i in range(len(g['patterns'])):row.append(k);col.append(offsets[k]+i)
    equality=sparse.csr_matrix((np.ones(len(col)),(row,col)),shape=(len(groups),len(descriptors)))
    def target(column):
        return np.array([p['coefficients'][g['columns'].index(column)] if column in g['columns'] else 0 for g,p in descriptors],dtype=float)
    return C,rhs,equality,target,offsets,len(descriptors),exponents

def group_bound(cuts,multipliers,groups,column,sign,column_count):
    active=[];seen=set()
    for index,value in multipliers:
        assert type(index) is int and index not in seen and 0<=index<len(cuts);seen.add(index)
        numerator=F(value)*DUAL_GRID;assert numerator.denominator==1 and numerator>=0
        if numerator:active.append((index,numerator.numerator))
    exponent=max([cuts[i]['normalization_exponent'] for i,n in active],default=0);unit=DUAL_GRID*(1<<exponent)
    vector=[0]*column_count;rhs=0
    for i,n in active:
        scale=n*(1<<(exponent-cuts[i]['normalization_exponent']));rhs+=scale*cuts[i]['rhs']
        vector=[x+scale*y for x,y in zip(vector,cuts[i]['coefficients'])]
    residual=[(sign*unit if i==column else 0)-x for i,x in enumerate(vector)]
    support=sum(max(sum(residual[i]*v for i,v in zip(g['columns'],p['coefficients'])) for p in g['patterns']) for g in groups)
    return F(rhs+support,unit),digest({'weighted_coefficients':vector,'weighted_rhs':rhs,'unit':unit})

def propose_bound(cuts,selected,groups,system,column,sign,column_count):
    C,rhs,equality,target,offsets,count,exponents=system
    result=linprog(-sign*target(column),A_ub=C,b_ub=rhs,A_eq=equality,b_eq=np.ones(len(groups)),bounds=(0,None),method='highs',
                   options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    multipliers=[]
    if result.success:
        for index,value in zip(selected,result.ineqlin.marginals):
            n=round(max(0.,-float(value))*DUAL_GRID)
            shift=cuts[index]['normalization_exponent']-exponents[index];assert shift>=0
            if n:multipliers.append([index,str(F(n*(1<<shift),DUAL_GRID))])
    upper,stream=group_bound(cuts,multipliers,groups,column,sign,column_count)
    return {'column':column,'sign':sign,'multipliers':multipliers,'solver_status':int(result.status),'solver_message':result.message,
            'floating_upper_proposal':float(-result.fun) if result.success else None,'exact_upper':str(upper),'integer_combination_sha256':stream}

def witness(cuts,selected,groups,system,domains,column,value):
    C,rhs,equality,target,offsets,count,exponents=system
    constraints=[LinearConstraint(sparse.hstack([sparse.csr_matrix(C),np.ones((len(selected),1))],format='csc'),-np.inf,rhs),
                 LinearConstraint(sparse.hstack([equality,sparse.csr_matrix((len(groups),1))],format='csc'),np.ones(len(groups)),np.ones(len(groups)))]
    if column is not None:constraints.append(LinearConstraint(np.r_[target(column),0][None,:],[value],[value]))
    result=milp(np.r_[np.zeros(count),-1],integrality=np.r_[np.ones(count,dtype=int),0],
                bounds=Bounds(np.r_[np.zeros(count),-np.inf],np.r_[np.ones(count),1]),constraints=constraints,
                options={'time_limit':10,'mip_rel_gap':0,'presolve':True})
    record={'assignment':None if column is None else {'column':column,'candidate':value},'solver_status':int(result.status),'solver_message':result.message,
            'proposed_minimum_normalized_slack':float(result.x[-1]) if result.x is not None else None,
            'verified_selected_feasible':False,'verified_full_pool_feasible':False,'integer_proposal_available':False}
    if result.x is not None:
        choice=[];coefficients=[0]*len(domains);valid=True
        for g,start in zip(groups,offsets):
            vector=result.x[start:start+len(g['patterns'])];k=int(np.argmax(vector))
            valid=valid and all(abs(float(v)-(1 if j==k else 0))<=1e-6 for j,v in enumerate(vector))
            p=g['patterns'][k];choice.append({'prime':g['prime'],'pattern_index':k,'model_id':p['model_ids'][0]})
            for i,v in zip(g['columns'],p['coefficients']):coefficients[i]=v
        if valid and all(v in d for v,d in zip(coefficients,domains)) and (column is None or coefficients[column]==value):
            slacks=[c['rhs']-sum(a*v for a,v in zip(c['coefficients'],coefficients)) for c in cuts]
            record.update(integer_proposal_available=True,coefficients=coefficients,local_choices=choice,
                          selected_minimum_integer_slack=min(slacks[i] for i in selected),full_pool_minimum_integer_slack=min(slacks),
                          violated_full_pool_cut_indices=[i for i,s in enumerate(slacks) if s<0],
                          verified_selected_feasible=all(slacks[i]>=0 for i in selected),verified_full_pool_feasible=all(s>=0 for s in slacks))
    return record

def run(audit_path,seed_path,seed_manifest,seed_verification,search_witnesses=True):
    audit=json.loads(audit_path.read_text());seed=json.loads(seed_path.read_text());manifest=json.loads(seed_manifest.read_text());verified=json.loads(seed_verification.read_text())
    assert audit['status']==seed['status']==verified['status']=='passed'
    entry=next(v for p,v in manifest['files'].items() if p.endswith('/'+seed_path.name));assert entry['sha256']==sha(seed_path) and entry['bytes']==seed_path.stat().st_size
    columns=audit['columns'];cases=[]
    for obs in audit['observations']:
        for profile in ['degree_only','degree_discriminant']:
            matched=[(i,c) for i,c in enumerate(seed['cases']) if all(c[k]==v for k,v in [('observation_index',obs['observation_index']),('radius',obs['radius']),('profile',profile)])];assert len(matched)==1
            seed_index,source=matched[0]
            for mode in ['unit_rows_from_common_seed','all_directions_from_common_seed']:
                cuts=obs['cuts'];selected=[i for i,c in enumerate(cuts) if mode.startswith('all_') or c['is_unit_row']]
                domains=[list(d) for d in source['final_domains']];initial=[list(d) for d in domains];steps=[]
                for iteration in range(1,4*len(columns)+2):
                    before=[list(d) for d in domains];groups,after_local,removed=groups_for(columns,before,profile)
                    system=numeric_system(cuts,selected,groups,len(columns));proofs=[];excluded={}
                    for column,c in enumerate(columns):
                        if c['n']>31 or len(after_local[column])==1:continue
                        for sign in [-1,1]:
                            proof=propose_bound(cuts,selected,groups,system,column,sign,len(columns));proof['n']=c['n'];proofs.append(proof)
                            for value in after_local[column]:
                                if (column,value) not in excluded and sign*value>F(proof['exact_upper']):
                                    excluded[column,value]={'column':column,'n':c['n'],'candidate':value,'proof_index':len(proofs)-1,'strict_gap':str(sign*value-F(proof['exact_upper']))}
                    domains=[list(d) for d in after_local]
                    for column,value in excluded:domains[column].remove(value)
                    assert all(domains)
                    steps.append({'iteration':iteration,'before_domains_sha256':digest(before),'groups':groups,'local_removals':removed,'after_local_sha256':digest(after_local),
                                  'model_hull_proofs':proofs,'dual_removals':list(excluded.values()),'after_domains_sha256':digest(domains)})
                    print(json.dumps({'event':'local_model_cut_round','observation':obs['observation_index'],'radius':obs['radius'],'profile':profile,'mode':mode,
                                      'iteration':iteration,'local_removals':len(removed),'dual_removals':len(excluded),'unique_targets':sum(len(d)==1 for c,d in zip(columns,domains) if c['n']<=31)}),flush=True)
                    if domains==before:break
                else:raise AssertionError('Finite model-hull deduction did not stabilize')
                groups,final,removed=groups_for(columns,domains,profile);assert final==domains and not removed
                system=numeric_system(cuts,selected,groups,len(columns));assignments=[(None,None)]+[(i,v) for i,c in enumerate(columns) if c['n']<=31 and len(domains[i])>1 for v in domains[i]]
                witnesses=[]
                for column,value in (assignments if search_witnesses else []):
                    w=witness(cuts,selected,groups,system,domains,column,value);witnesses.append(w)
                    print(json.dumps({'event':'local_model_integer_proposal','observation':obs['observation_index'],'profile':profile,'mode':mode,
                                      'assignment':w['assignment'],'solver_status':w['solver_status'],'verified_selected_feasible':w['verified_selected_feasible'],'verified_full_pool_feasible':w['verified_full_pool_feasible']}),flush=True)
                cases.append({'observation_index':obs['observation_index'],'radius':obs['radius'],'profile':profile,'mode':mode,'seed_case_index':seed_index,
                              'selected_cut_indices':selected,'solver_normalization_exponents':{str(i):e for i,e in system[-1].items()},'input_domains':initial,'rounds':steps,'final_domains':domains,'final_groups':groups,'witness_proposals':witnesses,
                              'initial_unique_targets':sum(len(d)==1 for c,d in zip(columns,initial) if c['n']<=31),
                              'final_unique_targets':sum(len(d)==1 for c,d in zip(columns,domains) if c['n']<=31),'final_unique_support':sum(len(d)==1 for d in domains)})
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [audit_path,seed_path,seed_manifest,seed_verification]},
            'columns':columns,'catalog':sorted(local_models(4,False)+local_models(4,True)),'cases':cases,'witness_search_performed':search_witnesses,
            'scope':'Both modes start from the same previously validated domains. Unit-row and full-direction inequalities are combined with the convex hull of complete allowed local coefficient patterns. Floating LPs propose nonnegative multipliers; exact integer group support certifies every exclusion. MILPs propose complete local-model assignments with a ten-second limit per branch, and integer slacks check any returned witness. Solver non-success or missing witnesses do not prove impossibility. No arithmetic vector or field catalogue is read.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['audit','seed','seed-manifest','seed-verification','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.audit,a.seed,a.seed_manifest,a.seed_verification);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'cases':len(r['cases']),'feasible_selected_witnesses':sum(w['verified_selected_feasible'] for c in r['cases'] for w in c['witness_proposals'])}))
