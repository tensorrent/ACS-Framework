"""Independently check square-discriminant target deduction, full witnesses and guard controls."""
import argparse,hashlib,itertools,json,math
from pathlib import Path
import sympy as s
from flint import arb
from dedekind_aggregate_local_audit import catalog,coefficient,partitions,digest
from dedekind_aggregate_primal_model_audit import real_cuts
from dedekind_coupled_recovery import encode

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def independent_groups(columns,domains,meta):
    catalogue=catalog();groups=[];empty=[]
    for prime in sorted({c['prime'] for c in columns}):
        indices=[i for i,c in enumerate(columns) if c['prime']==prime];patterns={}
        for j,model in enumerate(catalogue):
            if any(e!=1 for e,f in model)!=(meta['absolute_discriminant']%prime==0):continue
            # For an unramified degree-four algebra, even cycle types have an even number of factors.
            if meta['absolute_discriminant']%prime and meta['signed_discriminant_is_nonzero_square'] and len(model)%2:continue
            values=tuple(coefficient(model,columns[i]['power']) for i in indices)
            if all(v in domains[i] for i,v in zip(indices,values)):patterns.setdefault(values,[]).append(j)
        if not patterns:empty.append(prime)
        groups.append({'prime':prime,'columns':indices,'patterns':[{'coefficients':list(v),'model_ids':ids} for v,ids in sorted(patterns.items())]})
    return groups,empty

def controls():
    x=s.symbols('x');examples=[]
    for f,prime,expected,cycle in [(x**4-x*x-1,3,-400,[4]),(x**4-x**3-7*x*x+2*x+9,2,163**2,[1,3])]:
        p=s.Poly(f,x);der=p.diff();a=p.all_coeffs();b=der.all_coeffs();matrix=[]
        for j in range(3):matrix.append([0]*j+a+[0]*(2-j))
        for j in range(4):matrix.append([0]*j+b+[0]*(3-j))
        determinant=int(s.Matrix(matrix).det(method='bareiss'));assert determinant==expected==int(s.discriminant(f,x))
        factors=s.factor_list(f,modulus=prime)[1];degrees=sorted(s.degree(v,x) for v,e in factors for k in range(e))
        assert degrees==cycle and all(e==1 for v,e in factors) and expected%prime
        assert p.is_irreducible
        if prime==3:
            assert all(int(p.eval(k))%3 for k in range(3))
            assert all(s.rem(f,x*x+a*x+b,domain=s.GF(3))!=0 for a in range(3) for b in range(3))
            assert p.count_roots(-s.oo,s.oo)==2
        else:
            assert all(p.eval(k)!=0 for k in [-9,-3,-1,1,3,9])
            # Any monic quadratic factorization has bd=9, c=-1-a, a(d-b)=b+2.
            for b in [-9,-3,-1,1,3,9]:
                d=9//b
                assert (d==b and b+2!=0) or (d!=b and (b+2)%(d-b)!=0)
            assert all((k**3+k+1)%2 for k in [0,1])
        examples.append({'polynomial':str(f),'signed_polynomial_discriminant':determinant,'absolute_discriminant_is_square':math.isqrt(abs(determinant))**2==abs(determinant),
                         'prime':prime,'factor_degrees':list(map(int,degrees)),'irreducibility_cross_check':'passed','sylvester_determinant_cross_check':'passed'})
    original=x**4-2*x**3+7*x*x-6*x+3
    a=s.symbols('a');alternate=s.resultant(a*a-a+1,(x-a)**2+8,a)
    D0=int(s.discriminant(original,x));D1=int(s.discriminant(alternate,x))
    assert D0==14400 and D0//576==25 and D1%5 and 576%5
    original_factors=s.factor_list(original,modulus=5)[1];alternate_factors=[(q.as_expr(),e) for q,e in s.Poly(alternate,x,modulus=5).factor_list()[1]]
    assert any(e>1 for f,e in original_factors) and all(e==1 for f,e in alternate_factors)
    return {'polynomial_controls':examples,'square_does_not_imply_V4':True,'absolute_square_without_signature_is_insufficient':True,
            'ramified_model_control':{'model':[[2,2]],'prime':2,'field_discriminant':576,'c_p':0,'c_p_squared':2,'must_not_apply_unramified_cycle_count':True},
            'index_prime_control':{'original_polynomial':str(original),'original_polynomial_discriminant':D0,'field_discriminant':576,'index_squared':25,'prime':5,
                                   'original_reduction_has_repeated_factors':True,'alternate_polynomial':str(alternate),'alternate_discriminant':D1,
                                   'alternate_factor_degrees':sorted(int(s.degree(f,x)) for f,e in alternate_factors),'field_is_unramified':True}}

def run(parity_path,branches_path,projection_path,models_path,cut_audit_path,measurements,inputs,truth_path):
    read=lambda p:json.loads(p.read_text())
    data=read(parity_path);branches=read(branches_path);projection=read(projection_path);models=read(models_path);cuts_data=read(cut_audit_path);m=read(measurements);truth=read(truth_path)['arithmetic_vectors']
    assert all(x['status']=='passed' for x in [data,branches,projection,models,cuts_data])
    assert data['inputs_sha256']=={p.name:sha(p) for p in [branches_path,projection_path,models_path,cut_audit_path]+inputs}
    assert data['witness_search_performed'] and len(data['cases'])==len(branches['cases'])==len(projection['cases'])==4
    for p,meta in zip(inputs,data['metadata']):
        value=read(p);assert value['degree']==4 and value['real_places']+2*value['complex_places']==4
        signed=value['discriminant']*(-1 if value['complex_places']%2 else 1)
        assert meta=={'degree':4,'absolute_discriminant':value['discriminant'],'real_places':value['real_places'],'complex_places':value['complex_places'],
                      'signed_discriminant':signed,'signed_discriminant_is_nonzero_square':signed>0 and math.isqrt(signed)**2==signed}
    assert len(data['permutations'])==24 and {tuple(r['permutation']) for r in data['permutations']}==set(itertools.permutations(range(4)))
    for r in data['permutations']:
        permutation=r['permutation'];matrix=s.zeros(4)
        for i,j in enumerate(permutation):matrix[i,j]=1
        order_orbits=[];remaining=set(range(4))
        while remaining:
            start=min(remaining);orbit={start};current=permutation[start]
            while current!=start:orbit.add(current);current=permutation[current]
            remaining-=orbit;order_orbits.append(len(orbit))
        assert sorted(order_orbits)==r['cycles'] and int(matrix.det())==r['sign']==(-1)**(4-len(order_orbits))
        assert r['inversions']==sum(permutation[i]>permutation[j] for i in range(4) for j in range(i+1,4))
    allowed=[list(p) for p in partitions(4) if len(p)%2==0]
    assert allowed==data['allowed_unramified_cycle_types']==[[1,1,1,1],[1,3],[2,2]]
    real=[real_cuts(m,o) for o in cuts_data['observations']];results=[];catalogue=catalog();columns=m['columns']
    for case,old,checked in zip(data['cases'],branches['cases'],projection['cases']):
        assert case['source_case_index']==old['source_case_index']==checked['source_case_index']
        assert case['joint_projection_audit_case_sha256']==digest(checked) and checked['projection_complete_for_retained_relaxation'] and not checked['unresolved_branches']
        assert case['seed_profile']==old['profile'] and case['final_profile']=='degree_discriminant_and_derived_signed_square_parity'
        obs=old['observation_index'];assert case['observation_index']==obs and case['radius']==old['radius']
        parent=models['cases'][case['source_case_index']];expected=[i for i,b in enumerate(old['branches']) if b['status']!='refuted']
        assert [b['branch_index'] for b in case['branches']]==expected
        retained=[];records=[]
        for b in case['branches']:
            source=old['branches'][b['branch_index']];assert b['assignment']==source['assignment']
            domains=[list(d) for d in parent['final_domains']]
            for x in b['assignment']:domains[x['column']]=[x['candidate']]
            groups,empty=independent_groups(columns,domains,data['metadata'][obs]);assert digest(domains)==b['conditional_domains_sha256'] and digest(groups)==b['parity_groups_sha256']
            assert empty==b['incompatible_primes'] and b['retained']==(not empty)
            record={'branch_index':b['branch_index'],'incompatible_primes':empty,'retained':not empty}
            if empty:assert b['witness'] is None
            else:
                retained.append(b['branch_index']);w=b['witness'];assert w['verified_full_pool_feasible'] and w['verified_selected_feasible'] and w['integer_proposal_available']
                values=w['coefficients'];assert len(values)==len(columns) and all(type(v) is int and v in d for v,d in zip(values,domains)) and len(w['local_choices'])==len(groups)
                for g,choice in zip(groups,w['local_choices']):
                    assert choice['prime']==g['prime'];pattern=g['patterns'][choice['pattern_index']];assert choice['model_id'] in pattern['model_ids']
                    assert all(coefficient(catalogue[choice['model_id']],columns[i]['power'])==values[i] for i in g['columns'])
                slacks=[cut['rhs']-sum(a*v for a,v in zip(cut['coefficients'],values)) for cut in cuts_data['observations'][obs]['cuts']]
                assert min(slacks)>=0 and min(slacks)==w['full_pool_minimum_integer_slack']==w['selected_minimum_integer_slack'] and w['violated_full_pool_cut_indices']==[]
                gaps=[bound-sum((a*v for a,v in zip(vector,values)),arb(0)) for vector,bound in real[obs]];assert all(g>0 for g in gaps)
                targets=[{'column':i,'n':c['n'],'candidate':domains[i][0]} for i,c in enumerate(columns) if c['n']<=31 and len(domains[i])==1]
                assert targets==case['unique_targets'] and len(targets)==17 and all(t['candidate']==truth[['A','B'][obs]][t['column']] for t in targets)
                record.update(exact_integer_cut_checks=len(slacks),unrounded_real_cut_checks=len(gaps),all_unrounded_real_cuts_strictly_satisfied=True,
                              smallest_unrounded_real_margin=encode(min(g.lower() for g in gaps)),coefficient_vector_sha256=digest(values),heldout_target_checks=17)
            records.append(record)
        assert retained==[case['retained_branch_index']]
        results.append({'observation_index':obs,'radius':case['radius'],'seed_profile':case['seed_profile'],'unique_targets':17,'branch_replays':records})
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [parity_path,branches_path,projection_path,models_path,cut_audit_path,measurements,truth_path]+inputs},
            'permutation_checks':24,'even_permutations':12,'unramified_cycle_types':allowed,'controls':controls(),'cases':results,
            'scope':'Independent partition/divisor local enumeration, permutation determinants, exact integer witness cuts, fresh unrounded interval checks and held-out targets. Polynomial controls separate signed square from absolute square, A4 from V4, ramified rules and power-basis index primes. The general number-theoretic derivation is written and source-backed, not a Lean kernel proof.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['parity','branches','projection','models','cut-audit','measurements','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.parity,a.branches,a.projection,a.models,a.cut_audit,a.measurements,a.inputs,a.truth);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','cases':len(r['cases']),'permutations':24}))
