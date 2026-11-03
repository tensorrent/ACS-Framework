"""Derive unramified even splitting from signed square discriminant and audit target tuples."""
import argparse,hashlib,itertools,json,math
from pathlib import Path
from dedekind_coefficient_recovery import local_models
from dedekind_aggregate_primal_models import coefficient,numeric_system,witness,digest

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def metadata(value):
    n,D,r1,r2=[value[k] for k in ['degree','discriminant','real_places','complex_places']]
    assert all(type(x) is int for x in [n,D,r1,r2]) and n==4 and D>0 and r1>=0 and r2>=0 and r1+2*r2==n
    signed=(-1)**r2*D
    return {'degree':n,'absolute_discriminant':D,'real_places':r1,'complex_places':r2,'signed_discriminant':signed,
            'signed_discriminant_is_nonzero_square':signed>0 and math.isqrt(signed)**2==signed}

def cycles(p):
    seen=set();sizes=[]
    for i in range(len(p)):
        if i in seen:continue
        k=i;size=0
        while k not in seen:seen.add(k);size+=1;k=p[k]
        sizes.append(size)
    return sorted(sizes)

def permitted(model,prime,meta):
    ramified=any(e>1 for e,f in model)
    if ramified!=(meta['absolute_discriminant']%prime==0):return False
    if ramified or not meta['signed_discriminant_is_nonzero_square']:return True
    return (meta['degree']-len(model))%2==0

def groups_for(columns,domains,meta):
    catalogue=sorted(local_models(4,False)+local_models(4,True));groups=[];empty=[]
    for prime in sorted({c['prime'] for c in columns}):
        indices=[i for i,c in enumerate(columns) if c['prime']==prime];patterns={}
        for index,model in enumerate(catalogue):
            if not permitted(model,prime,meta):continue
            values=tuple(coefficient(model,columns[i]['power']) for i in indices)
            if all(v in domains[i] for i,v in zip(indices,values)):patterns.setdefault(values,[]).append(index)
        if not patterns:empty.append(prime)
        groups.append({'prime':prime,'columns':indices,'patterns':[{'coefficients':list(v),'model_ids':ids} for v,ids in sorted(patterns.items())]})
    return groups,empty

def run(branches_path,projection_path,models_path,cut_audit_path,inputs,search_witnesses=True):
    branches=json.loads(branches_path.read_text());projection=json.loads(projection_path.read_text());models=json.loads(models_path.read_text());audit=json.loads(cut_audit_path.read_text())
    assert all(d['status']=='passed' for d in [branches,projection,models,audit])
    assert projection['inputs_sha256'][branches_path.name]==sha(branches_path) and projection['inputs_sha256'][models_path.name]==sha(models_path)
    assert branches['inputs_sha256'][cut_audit_path.name]==sha(cut_audit_path)
    metas=[metadata(json.loads(p.read_text())) for p in inputs]
    assert all(m['signed_discriminant']==576 and m['signed_discriminant_is_nonzero_square'] for m in metas)
    permutations=[]
    for p in itertools.permutations(range(4)):
        inversions=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        permutations.append({'permutation':p,'inversions':inversions,'sign':(-1)**inversions,'cycles':cycles(p)})
    columns=audit['columns'];cases=[]
    for case,checked in zip(branches['cases'],projection['cases']):
        assert case['source_case_index']==checked['source_case_index'] and checked['projection_complete_for_retained_relaxation'] and checked['unresolved_branches']==0
        parent=models['cases'][case['source_case_index']];obs=case['observation_index'];cuts=audit['observations'][obs]['cuts'];records=[];retained=[]
        for index,b in enumerate(case['branches']):
            if b['status']=='refuted':continue
            assert b['status']=='feasible_integer_witness'
            forced=[list(d) for d in parent['final_domains']]
            for x in b['assignment']:forced[x['column']]=[x['candidate']]
            groups,empty=groups_for(columns,forced,metas[obs]);record={'branch_index':index,'assignment':b['assignment'],'conditional_domains_sha256':digest(forced),'parity_groups_sha256':digest(groups),'incompatible_primes':empty,'retained':not empty,'witness':None}
            if not empty:
                retained.append((index,forced))
                if search_witnesses:
                    selected=list(range(len(cuts)));system=numeric_system(cuts,selected,groups,len(columns))
                    record['witness']=witness(cuts,selected,groups,system,forced,None,None)
            records.append(record)
        assert len(retained)==1
        index,forced=retained[0];targets=[{'column':i,'n':c['n'],'candidate':forced[i][0]} for i,c in enumerate(columns) if c['n']<=31 and len(forced[i])==1]
        assert len(targets)==17
        cases.append({'source_case_index':case['source_case_index'],'observation_index':obs,'radius':case['radius'],'seed_profile':case['profile'],
                      'final_profile':'degree_discriminant_and_derived_signed_square_parity','joint_projection_audit_case_sha256':digest(checked),'branches':records,'retained_branch_index':index,'unique_targets':targets})
        print(json.dumps({'event':'signed_discriminant_projection','observation':obs,'seed_profile':case['profile'],'parity_refuted':sum(not b['retained'] for b in records),'unique_targets':len(targets),'full_parity_witness':next(b for b in records if b['retained'])['witness']['verified_full_pool_feasible'] if search_witnesses else None}),flush=True)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [branches_path,projection_path,models_path,cut_audit_path]+inputs},
            'metadata':metas,'permutations':permutations,'allowed_unramified_cycle_types':sorted({tuple(p['cycles']) for p in permutations if p['sign']==1}),
            'cases':cases,'witness_search_performed':search_witnesses,
            'scope':'A necessary local rule follows from supplied signed discriminant, with the mathematical derivation in the accompanying report. No Galois-group label or field candidate catalogue is read. Both old seed profiles now use discriminant and its square consequence. Refuting all but one previously exhaustively covered target tuple proves necessary target uniqueness; optional integer witnesses establish only consistency of the strengthened finite relaxation.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['branches','projection','models','cut-audit','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.branches,a.projection,a.models,a.cut_audit,a.inputs);a.output.write_text(json.dumps(r,indent=2)+'\n')
