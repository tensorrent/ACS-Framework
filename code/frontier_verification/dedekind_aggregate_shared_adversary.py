"""Mutate actual shared-root and local-closure proof components and recheck predicates."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_aggregate_shared_audit import terms_for,complex_derivative
from dedekind_aggregate_local_audit import catalog,coefficient
from dedekind_aggregate_integer_audit import integer_rows,exclusion_gap

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def run(shared_path,local_path,measurement_path,inputs,truth_path):
    ctx.prec=384;a=arb(1)/25
    shared=json.loads(shared_path.read_text());local=json.loads(local_path.read_text());m=json.loads(measurement_path.read_text())
    sources=[json.loads(p.read_text()) for p in inputs];truth=json.loads(truth_path.read_text())['arithmetic_vectors'];controls=[]
    def control(name,original,mutate,check,reason):
        check(original)
        altered=copy.deepcopy(original);mutate(altered)
        assert digest(original)!=digest(altered)
        try:check(altered)
        except AssertionError:rejected=True
        else:rejected=False
        assert rejected,name
        controls.append({'name':name,'baseline_passed':True,'mutation_rejected':True,'predicate':reason,
                         'original_component_sha256':digest(original),'mutated_component_sha256':digest(altered)})
    case=next(c for c in shared['cases'] if c['observation_index']==0 and c['sign']==-1 and c['radius']=='1/100000')
    alpha,sigma,terms=terms_for(m,case)
    def check_terms(packet):
        assert [x['alpha'] for x in packet]==list(map(str,alpha))
        assert [x['sigma'] for x in packet]==list(map(str,sigma))
    active=next(i for i,x in enumerate(alpha) if x)
    control('reverse_one_signed_multiplier',case['terms'],lambda x:x[active].update(alpha=str(-alpha[active])),check_terms,
            'The signed row coefficient must equal lambda_upper minus lambda_lower.')
    roots=sources[0]['positive_root_intervals'];delta=F(case['radius'])
    enlarged=[arb(str(F(x['lo'])-delta)).union(arb(str(F(x['hi'])+delta))) for x in roots]
    U=decode(m['constant_moment_upper'])-sum((3/(arb('9/4')+x*x) for x in enlarged),arb(0))
    tail=sum((arb(str(v))*decode(row['scale'])*U*404*(-16+a/4).exp()*(arb(row['center']).log()/2).cosh()
              for v,row in zip(sigma,m['rows'])),arb(0));assert tail>0
    def check_tail(x):assert decode(x['zero_tail']).overlaps(tail)
    control('omit_unknown_zero_tail',{'zero_tail':case['zero_tail']},lambda x:x.update(zero_tail=encode(arb(0))),check_tail,
            'A fresh moment and nonnegative sigma-weighted tail remain necessary after finite-root cancellation.')
    population=[{'root_index':r['root_index'],'lo':r['lo'],'hi':r['hi']} for r in case['root_bounds']]
    def check_population(packet):
        assert len(packet)==len(roots)
        for i,(r,original) in enumerate(zip(packet,roots)):
            assert r['root_index']==i and F(r['lo'])==F(original['lo'])-delta and F(r['hi'])==F(original['hi'])+delta
    control('drop_one_finite_root',population,lambda x:x.pop(),check_population,
            'Finite root count, multiplicity indices and all widened intervals must match the inherited population.')
    root=case['root_bounds'][0]
    def check_cover(packet):
        last=F(root['lo'])
        for leaf in packet:
            assert F(leaf['lo'])==last and F(leaf['hi'])>last;last=F(leaf['hi'])
        assert last==F(root['hi'])
    control('drop_one_cover_leaf',root['leaves'],lambda x:x.pop(len(x)//2),check_cover,
            'Consecutive rational leaf endpoints must cover the entire widened root interval without a gap.')
    leaf=root['leaves'][0]
    value,_=complex_derivative(arb(str((F(leaf['lo'])+F(leaf['hi']))/2)),a,terms);assert not value.contains(0)
    def check_derivative(packet):assert decode(packet['combined_derivative']).contains(value)
    control('forge_zero_derivative_enclosure',leaf,lambda x:x.update(combined_derivative=encode(arb(0))),check_derivative,
            'Complex-exponential evaluation at the actual leaf midpoint must lie in the submitted derivative enclosure.')
    empty=next(c for c in shared['cases'] if c['observation_index']==0 and c['sign']==1 and c['radius']=='1/100000')
    assert empty['multipliers']==[]
    def check_residual(packet):
        assert decode(packet['weighted_rhs'])==0 and decode(packet['residual_support_bound'])==4
        assert decode(packet['objective_upper_bound'])==4
    control('omit_box_residual_support',empty['nominal_bound'],lambda x:x.update(residual_support_bound=encode(arb(0)),objective_upper_bound=encode(arb(0))),check_residual,
            'With no multipliers, the positive coefficient objective still has box support four; the zero certificate is invalid.')
    independent=catalog()
    def check_catalog(packet):assert [tuple(map(tuple,x)) for x in packet]==independent
    control('drop_one_generic_local_model',local['catalog'],lambda x:x.pop(),check_catalog,
            'Independent integer partitions of degree four and divisor pairs must reproduce the complete eleven-model catalogue.')
    columns=local['columns'];wrong=None
    for c in local['cases']:
        if c['profile']!='degree_discriminant':continue
        for entry in c['rounds'][0]['local_models']:
            p=entry['prime']
            if 576%p==0:continue
            indices=[i for i,x in enumerate(columns) if x['prime']==p]
            for j,model in enumerate(independent):
                if any(e>1 for e,f in model) and all(coefficient(model,columns[i]['power']) in c['input_domains'][i] for i in indices):
                    wrong=(c,entry,j,indices);break
            if wrong:break
        if wrong:break
    assert wrong
    c,entry,j,indices=wrong
    expected=[k for k,model in enumerate(independent) if all(e==1 for e,f in model) and all(coefficient(model,columns[i]['power']) in c['input_domains'][i] for i in indices)]
    def check_ramification(packet):assert packet['model_ids']==expected
    control('admit_ramified_model_at_unramified_prime',entry,lambda x:x['model_ids'].append(j),check_ramification,
            'At prime '+str(entry['prime'])+', which does not divide 576, all ramification indices must be one; the inserted model otherwise fits input coefficient domains.')
    chosen=None
    for c in local['cases']:
        rows=integer_rows(m,c['observation_index'])
        for w in c['rounds'][0]['linear_removals']:
            i,v,j=w['column'],w['candidate'],w['measurement_index']
            if exclusion_gap(rows[j],c['input_domains'],i,v,w['side'])<=0:
                chosen=(c,w,rows[j]);break
        if chosen:break
    assert chosen
    c,w,row=chosen;i=w['column'];actual=truth[['A','B'][c['observation_index']]][i]
    def check_candidate(packet):assert exclusion_gap(row,c['first_local_domains'],i,packet['candidate'],w['side'])>0
    control('eliminate_held_out_true_coefficient',w,lambda x:x.update(candidate=actual),check_candidate,
            'The exact integer strict-gap predicate must reject elimination of the independently established true coefficient.')
    def check_prerequisites(packet):assert exclusion_gap(row,packet,i,w['candidate'],w['side'])>0
    control('discard_local_prerequisites_for_spectral_step',c['first_local_domains'],lambda x:x.__setitem__(slice(None),copy.deepcopy(c['input_domains'])),check_prerequisites,
            'The recorded new spectral exclusion needs the preceding local-domain reductions; reverting to baseline domains destroys its strict gap.')
    assert len(controls)==10
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [shared_path,local_path,measurement_path,truth_path]+inputs},
            'actual_component_mutations_rejected':len(controls),'controls':controls,
            'scope':'Each control alters an actual proof component, first passes its intact component through a semantic predicate, and then requires rejection of the mutation. These targeted predicates supplement the full independent audit; they are not exhaustive fuzzing or a claim that every mutation changes a final recovered coefficient.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['shared','local','measurements','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.shared,a.local,a.measurements,a.inputs,a.truth);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'actual_component_mutations_rejected':len(r['controls'])}))
