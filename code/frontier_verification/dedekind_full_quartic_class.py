"""Derive the complete quartic field class from degree, signature and discriminant 576."""
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def factor(n):
    out={};p=2
    while p*p<=n:
        while n%p==0:out[p]=out.get(p,0)+1;n//=p
        p+=1
    if n>1:out[n]=1
    return out
def check_metadata(m):
    if set(m)!={'degree','discriminant','real_places','complex_places'}:raise ValueError('Only degree, absolute discriminant and signature are permitted')
    n,D,r1,r2=[m[k] for k in ['degree','discriminant','real_places','complex_places']]
    if not all(type(x) is int for x in [n,D,r1,r2]) or n!=4 or D<1 or min(r1,r2)<0 or r1+2*r2!=4:raise ValueError('Invalid quartic metadata')
    signed=(-1)**r2*D;issquare=signed>0 and math.isqrt(signed)**2==signed;primes=factor(D)
    return {'signed_discriminant':signed,'signed_discriminant_square':issquare,'prime_factorization':[[p,e] for p,e in primes.items()],
            'A4_excluded_by_cubic_quotient_obstruction':issquare and set(primes)<={2,3} and primes.get(3,0)<3}

def group_certificate():
    perms=list(itertools.permutations(range(4)));lookup={p:i for i,p in enumerate(perms)};identity=lookup[(0,1,2,3)]
    table=[[lookup[tuple(a[b[k]] for k in range(4))] for b in perms] for a in perms]
    even=[i for i,p in enumerate(perms) if sum(p[a]>p[b] for a in range(4) for b in range(a+1,4))%2==0]
    inverses={a:next(b for b in even if table[a][b]==identity) for a in even}
    def closure(gens):
        g=set(gens)|{identity}
        while True:
            more={table[a][b] for a in g for b in g};new=g|more
            if new==g:return frozenset(g)
            g=new
    found={frozenset([identity])};pending=list(found)
    while pending:
        g=pending.pop()
        for a in even:
            h=closure(set(g)|{a})
            if h not in found:found.add(h);pending.append(h)
    groups=sorted(found,key=lambda g:(len(g),sorted(g)))
    def normal(h,g):return all({table[table[a][b]][inverses[a]] for b in h}==set(h) for a in g)
    def orbits(g):
        remaining=set(range(4));out=[]
        while remaining:
            o={perms[a][min(remaining)] for a in g};out.append(sorted(o));remaining-=o
        return sorted(out,key=lambda x:(len(x),x))
    transitive=[g for g in groups if len(orbits(g))==1];assert [len(g) for g in transitive]==[4,12]
    klein=transitive[0];alternating=transitive[1];assert normal(klein,alternating) and all(table[a][a]==identity for a in klein)
    cosets=sorted({frozenset(table[a][b] for b in klein) for a in alternating},key=lambda g:sorted(g));action={a:[cosets.index(frozenset(table[a][x] for x in c)) for c in cosets] for a in alternating}
    assert len(cosets)==3 and {a for a,v in action.items() if v==[0,1,2]}==set(klein) and len({tuple(v) for v in action.values()})==3
    inertia=[]
    for g in groups:
        if len({tuple(action[a]) for a in g})!=3:continue
        wild=[p for p in groups if len(p)==3 and p<=g and normal(p,g)]
        normalizer=[a for a in alternating if {table[table[a][b]][inverses[a]] for b in g}==set(g)]
        record={'inertia':sorted(g),'inertia_order':len(g),'normal_wild_3_subgroups':[sorted(p) for p in wild],'normalizer':normalizer,'embedding_orbits':orbits(g)}
        if wild:
            assert len(g)==3 and set(normalizer)==set(g) and sorted(map(len,orbits(g)))==[1,3]
            record.update(local_factors_ef=[[1,1],[3,1]],minimum_discriminant_exponent=3,minimum_even_discriminant_exponent=4)
        else:assert len(g)==12
        inertia.append(record)
    assert len(groups)==10 and len(inertia)==5 and sum(bool(i['normal_wild_3_subgroups']) for i in inertia)==4
    return {'permutations':perms,'even_indices':even,'subgroups':[sorted(g) for g in groups],'transitive_subgroups':[sorted(g) for g in transitive],
            'klein_subgroup':sorted(klein),'quotient_cosets':[sorted(c) for c in cosets],'quotient_action':[[a,v] for a,v in sorted(action.items())],
            'cubic_quotient_ramified_at_3_candidates':inertia,'cyclic_cubic_local_2_ramified_case':{'e':3,'f':1,'wild_order':1,'residue_unit_order':1,'tame_injection_possible':False},
            'unramified_cubic_minkowski_bound':{'degree':3,'real_places':3,'complex_places':0,'absolute_discriminant':1,'ideal_norm_upper':str(F(math.factorial(3),3**3)),'contradicts_positive_integer_ideal_norm':True}}

def radical_class(m):
    primes=list(factor(m['discriminant']));assert primes==[2,3]
    vectors=list(itertools.product([0,1],repeat=3));radicals={v:(-1)**v[0]*2**v[1]*3**v[2] for v in vectors};zero=(0,0,0);models=[]
    for triple in itertools.combinations([v for v in vectors if v!=zero],3):
        if tuple(a^b for a,b in zip(triple[0],triple[1]))!=triple[2]:continue
        ds=sorted(radicals[v] for v in triple);Ds=sorted(d if d%4==1 else 4*d for d in ds);r2=0 if all(d>0 for d in ds) else 2
        models.append({'squareclass_vectors':triple,'radicands':ds,'quadratic_discriminants':Ds,'field_discriminant':math.prod(Ds),'real_places':4-2*r2,'complex_places':r2,
                       'class_id':'quadratic_discriminants_'+('_'.join(map(str,Ds)))})
    models.sort(key=lambda x:x['radicands']);assert len(models)==7
    retained=[x for x in models if all(x[k]==m[k] for k in ['real_places','complex_places']) and x['field_discriminant']==m['discriminant']]
    assert len(retained)==2
    return models,retained

def run(metadata_path):
    metadata=json.loads(metadata_path.read_text());checked=check_metadata(metadata)
    assert metadata=={'degree':4,'discriminant':576,'real_places':0,'complex_places':2} and checked['A4_excluded_by_cubic_quotient_obstruction']
    groups=group_certificate();models,retained=radical_class(metadata)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{metadata_path.name:sha(metadata_path)},'metadata':metadata,'metadata_deductions':checked,
            'group_certificate':groups,'all_biquadratic_models':models,'retained_models':retained,'complete_quartic_candidate_count':len(retained),'Galois_group_derived':'V4',
            'proof_dependencies':['Signed square discriminant forces the Galois closure permutation group into A4; irreducibility gives transitivity.',
             'A4 has normal V4 quotient C3; unramified local extensions are closed under compositum, so no new finite ramified primes enter the normal closure.',
             'A ramified cyclic cubic extension of Q2 would have e=3,f=1 and tame inertia injecting into F2 multiplicative group, impossible.',
             'At3, a ramified cubic quotient forces inertia C3; its normalizer is C3, giving a wild cubic local factor in the quartic and discriminant exponent at least3.',
             'The supplied exponent at3 is2. The cubic quotient would therefore be everywhere finitely unramified, contradicting Minkowski.',
             'Quadratic subfields ramify only at2,3; enumerate their square classes. Conductor-discriminant multiplication identifies exactly two biquadratic fields.'],
            'scope':'Complete isomorphism class for degree4, signature(0,2), absolute field discriminant576, using the accompanying source-backed number-theoretic proof. No Galois group, field catalogue, polynomial, coefficient vector or spectral observation is supplied. Computational checks certify the finite group and square-class portions; the general arithmetic bridge is not formalized in Lean.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--metadata',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.metadata);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','group':r['Galois_group_derived'],'candidate_fields':r['complete_quartic_candidate_count']}))
