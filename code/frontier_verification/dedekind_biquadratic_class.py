"""Exhaust the V4 quartic candidate class with field discriminant 576."""
import argparse, hashlib, itertools, json, math
from pathlib import Path


def squarefree_part(n):
    out=-1 if n<0 else 1;n=abs(n);p=2
    while p*p<=n:
        exponent=0
        while n%p==0:n//=p;exponent+=1
        if exponent%2:out*=p
        p+=1
    return out*n


def fundamental(d): return d if d%4==1 else 4*d


def run(path):
    inputs=json.loads(path.read_text());radicands=[-6,-3,-2,-1,2,3,6]
    models=[]
    for triple in itertools.combinations(radicands,3):
        if all(squarefree_part(a*b) in triple for a,b in itertools.combinations(triple,2)):
            Ds=sorted(fundamental(d) for d in triple)
            models.append({'radicands':triple,'quadratic_discriminants':Ds,
                           'field_discriminant_by_character_conductors':math.prod(abs(D) for D in Ds),
                           'signature':[4,0] if all(d>0 for d in triple) else [0,2]})
    assert len(models)==7
    keep=[m for m in models if m['field_discriminant_by_character_conductors']==576 and m['signature']==[0,2]]
    assert len(keep)==2
    assert {tuple(m['quadratic_discriminants']) for m in keep}=={tuple(sorted(v['quadratic_discriminants'])) for v in inputs['fields'].values()}
    # Separate enumeration in the character group of (Z/24Z)^*.
    units=[1,5,7,11,13,17,19,23]
    generators=[tuple((-1)**((r-1)//2) for r in units),
                tuple((-1)**((r*r-1)//8) for r in units),
                tuple(1 if r%3==1 else -1 for r in units)]
    characters={}
    for bits in itertools.product([0,1],repeat=3):
        values=tuple(math.prod(g[i]**b for g,b in zip(generators,bits)) for i in range(8))
        conductors=[]
        for m in [1,2,3,4,6,8,12,24]:
            if all(values[i]==values[j] for i in range(8) for j in range(8) if units[i]%m==units[j]%m):conductors.append(m)
        characters[bits]={'values':values,'conductor':min(conductors),'parity':int(values[-1]==-1)}
    assert len({r['values'] for r in characters.values()})==8
    planes=[]
    for triple in itertools.combinations([b for b in characters if any(b)],3):
        if tuple(a^b for a,b in zip(triple[0],triple[1]))!=triple[2]:continue
        d=math.prod(characters[b]['conductor'] for b in triple)
        signature=[0,2] if any(characters[b]['parity'] for b in triple) else [4,0]
        planes.append({'basis_vectors':triple,'conductors':[characters[b]['conductor'] for b in triple],
                       'field_discriminant':d,'signature':signature})
    assert len(planes)==7
    assert sorted((p['field_discriminant'],p['signature']) for p in planes)==sorted((m['field_discriminant_by_character_conductors'],m['signature']) for m in models)
    assert sum(p['field_discriminant']==576 and p['signature']==[0,2] for p in planes)==2
    return {'status':'passed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'arithmetic_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'possible_quadratic_radicands':radicands,'all_biquadratic_models':models,'retained_models':keep,
            'mod24_units':units,'characters':[{'bits':b,**row} for b,row in characters.items()],'character_planes':planes,
            'complete_candidate_count':2,
            'premises':['A quadratic subfield can ramify only at primes ramified in the quartic field.',
                        'The fundamental discriminant of Q(sqrt(d)) is d for d=1 mod 4 and 4d otherwise, with d squarefree.',
                        'A V4 field is determined by its three quadratic subfields.',
                        'The discriminant of an abelian field is the product of the conductors of its characters (Milne CFT V.3.27).'],
            'scope':'Exactly two fields among Galois V4 quartics of signature (0,2) and field discriminant 576. The Galois-group input is explicit; no exhaustion of non-V4 quartics is asserted. This strengthens the earlier two-example contract without editing its frozen producer.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--arithmetic',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.arithmetic);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'candidate_fields':r['complete_candidate_count'],'radical_models':7,'character_planes':7}))
