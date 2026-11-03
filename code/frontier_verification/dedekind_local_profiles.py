"""Finite degree-four local Euler profiles, without a field-specific splitting rule."""
import itertools
DEGREE=4
PROFILES=['degree','degree_discriminant','galois','galois_discriminant']

def catalogue():
    pairs=[(e,f) for e in range(1,5) for f in range(1,5) if e*f<=4]
    result=[]
    def visit(remaining,start,model):
        if remaining==0:result.append(tuple(model));return
        for i in range(start,len(pairs)):
            e,f=pairs[i]
            if e*f<=remaining:visit(remaining-e*f,i,model+[pairs[i]])
    visit(4,0,[])
    return sorted(result)

def coefficient(model,k):return sum(f for e,f in model if k%f==0)
MODELS=catalogue()

def eligible(prime,profile):
    assert profile in PROFILES
    return [i for i,m in enumerate(MODELS)
        if ('galois' not in profile or len(set(m))==1)
        and ('discriminant' not in profile or any(e>1 for e,f in m)==(125%prime==0))]

def groups(powers):
    return {p:[i for i,(n,q,k) in enumerate(powers) if q==p] for p in sorted({p for n,p,k in powers})}

def retained(powers,domains,columns,profile):
    p=powers[columns[0]][1]
    return [i for i in eligible(p,profile) if all(coefficient(MODELS[i],powers[j][2]) in domains[j] for j in columns)]

def local_pass(powers,domains,profile):
    out=[list(d) for d in domains];checks=[]
    for p,columns in groups(powers).items():
        initial=eligible(p,profile);keep=retained(powers,domains,columns,profile);assert keep,('No local profile',p,profile)
        changes=[]
        for j in columns:
            after=sorted({coefficient(MODELS[i],powers[j][2]) for i in keep})
            assert set(after)<=set(domains[j])
            if after!=domains[j]:changes.append({'column':j,'n':powers[j][0],'before':domains[j],'after':after});out[j]=after
        if changes:
            rejected=[{'model_id':i,'witness_column':next(j for j in columns if coefficient(MODELS[i],powers[j][2]) not in domains[j])}
                      for i in initial if i not in keep]
            checks.append({'prime':p,'eligible_model_ids':initial,'retained_model_ids':keep,'rejected_models':rejected,'changes':changes})
    return out,checks

def minimal_observations(powers,domains,column,profile,answer):
    columns=groups(powers)[powers[column][1]];initial=eligible(powers[column][1],profile);trials=0
    for size in range(len(columns)+1):
        matches=[]
        for subset in itertools.combinations(columns,size):
            trials+=1
            keep=[i for i in initial if all(coefficient(MODELS[i],powers[j][2]) in domains[j] for j in subset)]
            values=sorted({coefficient(MODELS[i],powers[column][2]) for i in keep})
            if values==[answer]:matches.append((subset,keep))
        if matches:
            subset,keep=matches[0]
            return {'column':column,'n':powers[column][0],'answer':answer,'minimum_observation_count':size,
                'witness_columns':list(subset),'witness_prime_powers':[powers[j][0] for j in subset],
                'retained_model_ids':keep,'minimum_size_witness_sets':len(matches),'subsets_checked_through_minimum_size':trials}
    raise AssertionError('No sufficient observation subset')
