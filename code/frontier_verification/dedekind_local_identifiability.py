"""Distinguish recovered finite coefficients from identification of local factors."""
import argparse,hashlib,json
from collections import defaultdict
from pathlib import Path
from dedekind_recovery_audit import ordered_models


def coefficient(model,k):return sum(f for e,f in model if k%f==0)


def run(path):
    raw=path.read_bytes();data=json.loads(raw);assert data['status']=='passed'
    profiles=[]
    for ramified in [False,True]:
        groups=defaultdict(list)
        for model in sorted(ordered_models(ramified)):
            values=tuple(coefficient(model,k) for k in range(1,13))
            c1,c2,c3,c4=values[:4]
            numerators=[c1,c2-c1,c3-c1,c4-c2]
            for f,numerator in enumerate(numerators,1):
                assert numerator%f==0 and numerator//f==sum(g==f for e,g in model)
            assert all(coefficient(model,k)==values[(k-1)%12] for k in range(1,145))
            groups[values].append(model)
        profiles.append({'ramified':ramified,'model_count':sum(map(len,groups.values())),
                         'distinct_full_coefficient_sequences':len(groups),
                         'groups':[{'period_12':list(v),'models':[list(map(list,m)) for m in models]}
                                   for v,models in groups.items()]})
    unresolved=[]
    for p in data['inferences_by_height']['2000']['models']:
        models=p['retained_models']
        if len(models)>1:
            separating=[k for k in range(1,13) if len({coefficient(m,k) for m in models})>1]
            assert separating
            first=min(separating);n=p['prime']**first
            assert n>data['target_limit']
            unresolved.append({'prime':p['prime'],'retained_models':models,'first_distinguishing_exponent':first,
                               'next_prime_power':n,'possible_coefficients':sorted({coefficient(m,first) for m in models})})
    assert len(unresolved)==48 and all(r['first_distinguishing_exponent']==2 for r in unresolved)
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'recovery_sha256':hashlib.sha256(raw).hexdigest(),'profiles':profiles,'unresolved_local_factors':unresolved,
            'unresolved_count':len(unresolved),'range_of_next_powers':[min(r['next_prime_power'] for r in unresolved),max(r['next_prime_power'] for r in unresolved)],
            'inversion':['n1=c1','n2=(c2-c1)/2','n3=(c3-c1)/3','n4=(c4-c2)/4'],
            'scope':'For degree four, four power coefficients determine residue-degree multiplicities. They do not generally determine the individual ramification indices. Periodicity follows because every residue degree divides 12; finite checks support that exact argument.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--recovery',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.recovery)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'unresolved_local_factors':r['unresolved_count'],'next_power_range':r['range_of_next_powers']}))
