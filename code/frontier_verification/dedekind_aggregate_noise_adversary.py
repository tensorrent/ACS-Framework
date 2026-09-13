"""Reject semantic corruptions of adapted nonlinear-error proof components."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import decode,encode
from dedekind_aggregate_shared_audit import terms_for
from dedekind_aggregate_integer_audit import integer_rows,objective_bound
from dedekind_aggregate_noise_audit import complex_values

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def run(certificate_path,audit_path,measurements,inputs):
    ctx.prec=384;a=arb(1)/25
    d=json.loads(certificate_path.read_text());audit=json.loads(audit_path.read_text());m=json.loads(measurements.read_text())
    sources=[json.loads(p.read_text()) for p in inputs];controls=[]
    def control(name,original,mutate,check,predicate):
        check(original);altered=copy.deepcopy(original);mutate(altered);assert digest(altered)!=digest(original)
        try:check(altered)
        except AssertionError:rejected=True
        else:rejected=False
        assert rejected,name
        controls.append({'name':name,'baseline_passed':True,'mutation_rejected':True,'predicate':predicate,
                         'original_component_sha256':digest(original),'mutated_component_sha256':digest(altered)})
    case=next(c for c in d['cases'] if c['observation_index']==0 and c['radius']=='3/50' and c['sign']==-1 and c['multiplier_source']=='noise_adapted')
    alpha,sigma,terms=terms_for(m,case);altered=copy.deepcopy(m)
    for row in altered['rows']:row['observations'][0]['R']=row['observations'][0]['unwidened']
    rows=integer_rows(altered,0)
    def check_multipliers(x):objective_bound(rows,case['column'],x,len(m['columns']))
    control('negative_inequality_multiplier',{'sign':case['sign'],'multipliers':case['multipliers']},lambda x:x['multipliers'][0].__setitem__(1,str(-F(x['multipliers'][0][1]))),check_multipliers,
            'Exact integer objective replay requires every inequality multiplier to be nonnegative.')
    active=next(i for i,v in enumerate(alpha) if v)
    def check_terms(x):assert [r['alpha'] for r in x]==list(map(str,alpha)) and [r['sigma'] for r in x]==list(map(str,sigma))
    control('reverse_one_signed_root_weight',case['terms'],lambda x:x[active].update(alpha=str(-alpha[active])),check_terms,
            'The signed finite-root coefficient and the nonnegative unknown-tail coefficient must match the actual dual multipliers.')
    roots=sources[0]['positive_root_intervals'];delta=F(case['radius'])
    wide=[arb(str(F(x['lo'])-delta)).union(arb(str(F(x['hi'])+delta))) for x in roots]
    U=decode(m['constant_moment_upper'])-sum((3/(arb('9/4')+x*x) for x in wide),arb(0))
    tail=sum((arb(str(v))*decode(row['scale'])*U*404*(-16+a/4).exp()*(arb(row['center']).log()/2).cosh() for row,v in zip(m['rows'],sigma)),arb(0));assert tail>0
    def check_tail(x):assert decode(x['zero_tail']).overlaps(tail)
    control('omit_unknown_zero_budget',{'zero_tail':case['zero_tail']},lambda x:x.update(zero_tail=encode(arb(0))),check_tail,
            'Fresh moment inflation and sigma-weighted unknown-zero budgets remain positive after finite-error optimization.')
    empty=next(c for c in d['cases'] if c['observation_index']==0 and c['sign']==1 and c['radius']=='3/50' and c['multiplier_source']=='frozen')
    assert not empty['multipliers']
    def check_residual(x):assert decode(x['residual_support_bound'])==4 and decode(x['objective_upper_bound'])==4
    control('omit_full_box_residual',empty['nominal_bound'],lambda x:x.update(residual_support_bound=encode(arb(0)),objective_upper_bound=encode(arb(0))),check_residual,
            'The positive coefficient objective retains support four when its multiplier vector is empty.')
    root=case['root_bounds'][0]
    def check_cover(x):
        last=F(root['lo'])
        for leaf in x:assert F(leaf['lo'])==last and F(leaf['hi'])>last;last=F(leaf['hi'])
        assert last==F(root['hi'])
    control('drop_one_continuum_cover_leaf',root['leaves'],lambda x:x.pop(len(x)//2),check_cover,
            'The rational leaf boundaries must cover every allowed ordinate value without gaps.')
    leaf=root['leaves'][0];base,_,_=complex_values(arb(str((F(roots[0]['lo'])+F(roots[0]['hi']))/2)),a,terms)
    endpoint,_,_=complex_values(arb(leaf['lo']),a,terms);change=-2*(endpoint-base)
    def check_variation(x):assert decode(x['change']).contains(change)
    control('replace_leaf_range_with_its_midpoint_value',leaf,lambda x:x.update(change=x['midpoint_change']),check_variation,
            'A fresh complex evaluation at the leaf endpoint is covered by the full enclosure and falls outside the substituted midpoint-only interval.')
    for witness in audit['certified_off_grid_counterexamples']:
        obs=witness['observation_index'];radius=witness['radius'];index=witness['root_index']
        c=next(x for x in d['cases'] if x['observation_index']==obs and x['radius']==radius and x['multiplier_source']=='noise_adapted' and x['multipliers'])
        value=decode(witness['off_grid_error_interval']);sampled=max(decode(x).upper() for x in witness['sampled_error_intervals'])
        assert value>sampled
        def check_sample(x):assert not value>x['upper']
        # Keep the packet serializable while comparing exact dyadic enclosures.
        def check_encoded(x):check_sample({'upper':decode(x['upper'])})
        control('use_sampled_maximum_as_continuum_bound_'+str(obs),{'upper':c['root_bounds'][index]['direct_error_upper']},lambda x:x.update(upper=encode(sampled)),check_encoded,
                'The audited off-grid error exceeds every one of the 33 sampled values but remains below the certified continuous root bound.')
    assert len(controls)==8
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [certificate_path,audit_path,measurements]+inputs},
            'actual_component_mutations_rejected':len(controls),'controls':controls,
            'scope':'Eight targeted semantic mutations of actual proof components, including the two independently certified off-grid witnesses. Each original component passes before its mutation is required to fail. These are not exhaustive fuzzing, and the off-grid tests overlap the two witnesses already reported by the independent audit.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['certificate','audit','measurements','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.certificate,a.audit,a.measurements,a.inputs);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'mutations_rejected':len(r['controls'])}))
