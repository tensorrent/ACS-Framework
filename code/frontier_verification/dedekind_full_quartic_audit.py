"""Audit the quartic classification by exhaustive subsets, local group constraints and characters."""
import argparse,hashlib,itertools,json,math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import sympy as s

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cycles(p):
    remaining=set(range(4));out=[]
    while remaining:
        a=min(remaining);seen=[]
        while a not in seen:seen.append(a);a=p[a]
        remaining-=set(seen);out.append(seen)
    return out
def audit_groups(data):
    permutations=list(itertools.permutations(range(4)));lookup={p:i for i,p in enumerate(permutations)}
    assert list(map(list,permutations))==data['permutations']
    # Opposite multiplication to the producer, and cycle parity rather than inversions.
    table=[[lookup[tuple(b[a[k]] for k in range(4))] for b in permutations] for a in permutations]
    identity=lookup[(0,1,2,3)];even=[i for i,p in enumerate(permutations) if (4-len(cycles(p)))%2==0]
    assert even==data['even_indices'] and len(even)==12
    remainder=[i for i in even if i!=identity];groups=[]
    for mask in range(1<<len(remainder)):
        g={identity}|{v for j,v in enumerate(remainder) if mask>>j&1}
        if all(table[a][b] in g for a in g for b in g):groups.append(frozenset(g))
    groups.sort(key=lambda g:(len(g),sorted(g)));assert [sorted(g) for g in groups]==data['subgroups']
    inverses={a:next(b for b in even if table[a][b]==identity) for a in even}
    def conjugate(a,g):return {table[table[a][b]][inverses[a]] for b in g}
    def normal(h,g):return all(conjugate(a,h)==set(h) for a in g)
    def orbits(g):
        unused=set(range(4));result=[]
        while unused:
            seen={min(unused)};queue=list(seen)
            while queue:
                i=queue.pop()
                for a in g:
                    j=permutations[a][i]
                    if j not in seen:seen.add(j);queue.append(j)
            unused-=seen;result.append(sorted(seen))
        return sorted(result,key=lambda x:(len(x),x))
    transitive=[g for g in groups if len(orbits(g))==1];assert [sorted(g) for g in transitive]==data['transitive_subgroups'] and [len(g) for g in transitive]==[4,12]
    klein={identity}|{i for i in even if sorted(map(len,cycles(permutations[i])))==[2,2]};assert sorted(klein)==data['klein_subgroup'] and normal(klein,set(even))
    cosets=sorted({frozenset(table[a][b] for a in klein) for b in even},key=lambda g:sorted(g));assert [sorted(g) for g in cosets]==data['quotient_cosets'] and len(cosets)==3
    action={a:[cosets.index(frozenset(table[x][a] for x in c)) for c in cosets] for a in even}
    assert [[a,v] for a,v in sorted(action.items())]==data['quotient_action']
    assert {tuple(v) for v in action.values()}=={(0,1,2),(1,2,0),(2,0,1)}
    candidates=[g for g in groups if not g<=klein];assert len(candidates)==5
    replay=[]
    for g,row in zip(candidates,data['cubic_quotient_ramified_at_3_candidates']):
        assert sorted(g)==row['inertia'] and len(g)==row['inertia_order']
        wild=[h for h in groups if h<=g and len(h)==3 and normal(h,g)];assert [sorted(h) for h in wild]==row['normal_wild_3_subgroups']
        norm={a for a in even if conjugate(a,g)==set(g)};assert norm==set(row['normalizer']) and orbits(g)==row['embedding_orbits']
        decomposition=[h for h in groups if g<=h and normal(g,h)]
        if wild:
            assert decomposition==[g] and len(g)==3 and sorted(map(len,orbits(g)))==[1,3]
            assert row['local_factors_ef']==[[1,1],[3,1]]
            lower=sum((e if e%3==0 else e-1)*f for e,f in row['local_factors_ef'])
            assert lower==row['minimum_discriminant_exponent']==3 and 2*math.ceil(F(lower,2))==row['minimum_even_discriminant_exponent']==4
        else:assert len(g)==12
        replay.append({'inertia_order':len(g),'normal_wild_3_subgroups':len(wild),'allowed_decomposition_orders':[len(h) for h in decomposition],
                       'survives_wild_filtration':bool(wild),'embedding_orbit_sizes':sorted(map(len,orbits(g)))})
    local=data['cyclic_cubic_local_2_ramified_case'];assert local=={'e':3,'f':1,'wild_order':1,'residue_unit_order':1,'tame_injection_possible':False}
    assert (2**local['f']-1)%local['e']!=0
    bound=data['unramified_cubic_minkowski_bound'];assert bound['degree']==3 and bound['real_places']==3 and bound['complex_places']==0 and bound['absolute_discriminant']==1
    assert F(bound['ideal_norm_upper'])==F(2,9)<1 and bound['contradicts_positive_integer_ideal_norm']
    return {'exhausted_identity_containing_A4_subsets':2048,'subgroup_order_counts':dict(sorted(Counter(map(len,groups)).items())),
            'transitive_group_orders':[4,12],'inertia_replays':replay,'cubic_minkowski_upper':'2/9'}

def audit_characters(data):
    units=[i for i in range(24) if math.gcd(i,24)==1];index={u:i for i,u in enumerate(units)};chars=[]
    for values in itertools.product([-1,1],repeat=len(units)):
        if all(values[index[a*b%24]]==values[index[a]]*values[index[b]] for a in units for b in units):chars.append(values)
    assert len(chars)==8
    descriptors={}
    for v in chars:
        conductor=next(m for m in s.divisors(24) if all(v[i]==v[j] for i in range(8) for j in range(8) if units[i]%m==units[j]%m))
        D=conductor*v[index[23]];descriptors[v]=int(D)
        assert v==tuple(int(s.kronecker_symbol(D,u)) for u in units)
    nontrivial=[v for v in chars if any(x==-1 for x in v)];planes=[]
    for triple in itertools.combinations(nontrivial,3):
        if all(tuple(a*b for a,b in zip(u,v)) in triple for u,v in itertools.combinations(triple,2)):
            Ds=sorted(descriptors[v] for v in triple);r2=2 if any(D<0 for D in Ds) else 0
            planes.append({'quadratic_discriminants':Ds,'field_discriminant':math.prod(Ds),'real_places':4-2*r2,'complex_places':r2})
    assert len(planes)==7
    expected=[{k:m[k] for k in ['quadratic_discriminants','field_discriminant','real_places','complex_places']} for m in data['all_biquadratic_models']]
    assert sorted(planes,key=lambda p:p['quadratic_discriminants'])==sorted(expected,key=lambda p:p['quadratic_discriminants'])
    for m in data['all_biquadratic_models']:
        ds=m['radicands'];assert len(ds)==3 and all(d!=1 and abs(d) in s.divisors(6) for d in ds)
        assert sorted(d if d%4==1 else 4*d for d in ds)==m['quadratic_discriminants']
        for a,b in itertools.combinations(ds,2):
            product=a*b;sf=(-1 if product<0 else 1)*math.prod(int(p) for p,e in s.factorint(abs(product)).items() if e%2)
            assert sf in ds
    selected=[p for p in planes if p['field_discriminant']==576 and p['complex_places']==2]
    assert len(selected)==2 and sorted(p['quadratic_discriminants'] for p in selected)==sorted(p['quadratic_discriminants'] for p in data['retained_models'])
    return {'sign_functions_tested':256,'quadratic_characters':8,'character_planes':7,'complete_quartic_candidate_count':2,'selected_quadratic_discriminants':sorted(p['quadratic_discriminants'] for p in selected)}

def run(class_path,metadata_path,old_class_path):
    data=json.loads(class_path.read_text());m=json.loads(metadata_path.read_text());old=json.loads(old_class_path.read_text())
    assert data['status']=='passed' and data['inputs_sha256']=={metadata_path.name:sha(metadata_path)} and data['metadata']==m
    assert set(m)=={'degree','discriminant','real_places','complex_places'} and m=={'degree':4,'discriminant':576,'real_places':0,'complex_places':2}
    md=data['metadata_deductions'];assert md=={'signed_discriminant':576,'signed_discriminant_square':True,'prime_factorization':[[2,6],[3,2]],'A4_excluded_by_cubic_quotient_obstruction':True}
    groups=audit_groups(data['group_certificate']);chars=audit_characters(data)
    assert data['Galois_group_derived']=='V4' and data['complete_quartic_candidate_count']==2
    assert chars['selected_quadratic_discriminants']==sorted(p['quadratic_discriminants'] for p in old['retained_models'])
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [class_path,metadata_path,old_class_path]},
            'independent_group_audit':groups,'independent_character_audit':chars,'old_V4_conditional_candidate_set_retained':True,
            'new_scope':'The source-backed cubic-quotient obstruction derives V4 from the metadata, making the two-field enumeration exhaustive among all quartic fields with the specified invariants. The computational audit independently verifies the finite group, local-order and character portions; it does not formalize general algebraic number theory in Lean.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['classification','metadata','old-class','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.classification,a.metadata,a.old_class);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','subsets':2048,'sign_functions':256,'candidate_fields':2}))
