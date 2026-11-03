"""Challenge moment coupling and the prerequisites of noisy local/dual feedback."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_aggregate_shared_audit import terms_for
from dedekind_aggregate_noise_audit import complex_values
from dedekind_aggregate_moment_audit import rational_moment,moment_interval
from dedekind_aggregate_moment_local_audit import integer_dual,domain_bound,project
from dedekind_aggregate_local_audit import catalog,coefficient
from dedekind_aggregate_integer_audit import integer_rows

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def run(certificate_path,feedback_path,audit_path,measurements,proposals,previous_proposals,inputs,truth_path):
    ctx.prec=384;a=arb(1)/25
    d=json.loads(certificate_path.read_text());feedback=json.loads(feedback_path.read_text());audit=json.loads(audit_path.read_text());m=json.loads(measurements.read_text())
    p=json.loads(proposals.read_text());old=json.loads(previous_proposals.read_text());sources=[json.loads(x.read_text()) for x in inputs];truth=json.loads(truth_path.read_text())['arithmetic_vectors'];controls=[];probes=[]
    def control(name,original,mutate,check,predicate):
        check(original);changed=copy.deepcopy(original);mutate(changed);assert digest(original)!=digest(changed)
        try:check(changed)
        except AssertionError:rejected=True
        else:rejected=False
        assert rejected,name
        controls.append({'name':name,'baseline_passed':True,'mutation_rejected':True,'predicate':predicate,
                         'original_component_sha256':digest(original),'mutated_component_sha256':digest(changed)})
    main=next(c for c in d['cases'] if c['observation_index']==0 and c['radius']=='1/200' and c['n']==7 and c['sign']==-1 and c['multiplier_source']=='joint_adapted')
    root=main['root_bounds'][0];original=sources[0]['positive_root_intervals'][0];center=(F(original['lo'])+F(original['hi']))/2
    exact_m=arb(str(rational_moment(center)))
    def check_moment(x):assert decode(x['base_moment']).contains(exact_m)
    control('remove_pair_normalization_from_known_moment',{'base_moment':root['base_moment']},lambda x:x.update(base_moment=encode(decode(x['base_moment'])/3)),check_moment,
            'The original moment enclosure must contain the independently evaluated rational function 12/(9+4t^2).')
    def check_cover(x):
        last=F(root['lo'])
        for leaf in x:assert F(leaf['lo'])==last and F(leaf['hi'])>last;last=F(leaf['hi'])
        assert last==F(root['hi'])
    control('drop_one_joint_cover_leaf',root['leaves'],lambda x:x.pop(len(x)//2),check_cover,
            'Joint increments require a complete rational cover of every allowed root value.')
    omitted=None
    for case in d['cases']:
        if F(case['radius'])==0 or not case['multipliers']:continue
        obs=case['observation_index'];alpha,sigma,terms=terms_for(m,case)
        kappa=sum((arb(str(v))*decode(row['scale'])*404*(-16+a/4).exp()*(arb(row['center']).log()/2).cosh() for row,v in zip(m['rows'],sigma)),arb(0))
        for ri,root_case in enumerate(case['root_bounds']):
            origin=sources[obs]['positive_root_intervals'][ri];base_point=(F(origin['lo'])+F(origin['hi']))/2;base,_,_=complex_values(arb(str(base_point)),a,terms)
            for leaf in root_case['leaves']:
                middle=(F(leaf['lo'])+F(leaf['hi']))/2;h,_,_=complex_values(arb(str(middle)),a,terms)
                value=-2*(h-base)-kappa*arb(str(rational_moment(middle)-rational_moment(base_point)))
                if not decode(leaf['finite_change']).contains(value):omitted=(case,ri,leaf,value);break
            if omitted:break
        if omitted:break
    probes.append({'name':'finite_only_leaf_substitution','witness_found':omitted is not None})
    if omitted:
        case,ri,leaf,value=omitted
        def check_joint_leaf(x):assert decode(x['joint_change']).contains(value)
        control('replace_joint_leaf_with_finite_only_leaf',leaf,lambda x:x.update(joint_change=x['finite_change']),check_joint_leaf,
                'An independently evaluated joint midpoint change at observation '+str(case['observation_index'])+', target '+str(case['n'])+', root '+str(ri)+' lies outside the finite-only leaf enclosure.')
    # A positive unit row and one displaced inherited root isolate the omitted moment term.
    delta=F(1,200);lo,hi=F(original['lo']),F(original['hi']);interval=arb(str(lo-delta)).union(arb(str(hi+delta)))
    row=m['rows'][0];unit_terms=[(decode(row['scale']),arb(row['center']).log())]
    kappa=decode(row['scale'])*404*(-16+a/4).exp()*(arb(row['center']).log()/2).cosh()
    _,hp,_=complex_values(interval,a,unit_terms);finite_derivative=-2*hp;joint_derivative=finite_derivative-kappa*moment_interval(lo-delta,hi+delta,1)
    assert finite_derivative>0 and joint_derivative>0
    base,_,_=complex_values(arb(str(lo)).union(arb(str(hi))),a,unit_terms)
    end,_,_=complex_values(arb(str(lo+delta)).union(arb(str(hi+delta))),a,unit_terms)
    finite_end=-2*(end-base);joint_end=finite_end-kappa*(moment_interval(lo+delta,hi+delta)-moment_interval(lo,hi))
    gap=joint_end-finite_end.upper();assert gap>0
    def check_endpoint_budget(x):assert not joint_end.lower()>decode(x['upper']).upper()
    control('freeze_known_moment_while_moving_root',{'upper':encode(joint_end.upper())},lambda x:x.update(upper=encode(finite_end.upper())),check_endpoint_budget,
            'Both changes increase across the one-root interval. The joint endpoint exceeds the full finite-only maximum, so freezing the baseline moment omits a strictly positive budget term.')
    counterexample={'observation_index':0,'root_index':0,'row_index':0,'radius':'1/200','finite_derivative':encode(finite_derivative),'joint_derivative':encode(joint_derivative),
                    'finite_endpoint_change':encode(finite_end),'joint_endpoint_change':encode(joint_end),'strict_gap':encode(gap),
                    'scope':'A unit measurement multiplier and uncertainty in one inherited root give a counterexample for the analytic budget expression. Other roots stay fixed. This does not assert that unknown zeros attain the tail bound or construct an alternate number field.'}
    altered=copy.deepcopy(m)
    for row in altered['rows']:
        for obs in [0,1]:row['observations'][obs]['R']=row['observations'][obs]['unwidened']
    rows=[integer_rows(altered,obs) for obs in [0,1]]
    def check_nonnegative(x):integer_dual(rows[0],x,len(m['columns']))
    control('negative_dual_multiplier',{k:main[k] for k in ['column','sign','multipliers']},lambda x:x['multipliers'][0].__setitem__(1,str(-F(x['multipliers'][0][1]))),check_nonnegative,
            'Exact integer weighted inequalities require nonnegative rational multipliers.')
    chosen=None
    for case in feedback['cases']:
        domains=case['input_domains']
        for step in case['rounds']:
            after_local,_,_=project(m['columns'],domains,case['profile'])
            if step['dual_removals']:
                chosen=(case,step['dual_removals'][0],after_local);break
            domains=after_local
        if chosen:break
    assert chosen
    case,witness,domains=chosen;index=witness['audit_case_index'];record=audit['objective_replays'][index]
    candidate=next(c for c in (p if record['multiplier_source']=='joint_adapted' else old)['cases'] if all(c[k]==record[k] for k in ['observation_index','radius','column','sign']))
    prepared=integer_dual(rows[case['observation_index']],candidate,len(m['columns']));budget=record['methods'][case['method']]['budget_upper']
    actual=truth[['A','B'][case['observation_index']]][witness['column']]
    def check_removal(x):assert witness['sign']*x['candidate']>domain_bound(prepared,domains,budget)
    control('remove_held_out_true_coefficient',witness,lambda x:x.update(candidate=actual),check_removal,
            'The strict rational objective gap must fail when the independently established actual coefficient is substituted for the excluded candidate.')
    def check_prerequisites(x):assert witness['sign']*witness['candidate']>domain_bound(prepared,x,budget)
    control('discard_validated_domain_prerequisites',domains,lambda x:x.__setitem__(slice(None),[list(range(5)) for _ in x]),check_prerequisites,
            'The new residual-support exclusion depends on validated coefficient domains; resetting every box to 0..4 destroys its strict gap.')
    noisy=next(c for c in feedback['cases'] if c['observation_index']==0 and c['radius']=='1/10' and c['method']=='coupled' and c['profile']=='degree_discriminant')
    exact=next(c for c in feedback['cases'] if c['observation_index']==0 and c['radius']=='0' and c['method']=='coupled' and c['profile']=='degree_discriminant')
    expected=[list(range(5)) for _ in m['columns']]
    for row in audit['objective_replays']:
        if row['observation_index']==0 and row['radius']=='1/10':expected[row['column']]=sorted(set(expected[row['column']])&set(row['methods']['coupled']['candidates']))
    def check_noise_premise(x):assert x==expected
    control('reuse_zero_noise_domains_at_radius_point_one',noisy['input_domains'],lambda x:x.__setitem__(slice(None),copy.deepcopy(exact['input_domains'])),check_noise_premise,
            'Initial domains must come from certificates for the declared noisy input, not from the zero-radius case.')
    models=catalog()
    def check_catalog(x):assert [tuple(map(tuple,row)) for row in x]==models
    control('drop_generic_local_model',feedback['catalog'],lambda x:x.pop(),check_catalog,
            'The complete model catalogue must match the independent degree-partition enumeration.')
    entry=next(e for e in noisy['rounds'][0]['local_models'] if e['prime']==7)
    indices=[i for i,c in enumerate(m['columns']) if c['prime']==7]
    wrong=next(j for j,model in enumerate(models) if any(e>1 for e,f in model) and all(coefficient(model,m['columns'][i]['power']) in noisy['input_domains'][i] for i in indices))
    expected_ids=[j for j,model in enumerate(models) if all(e==1 for e,f in model) and all(coefficient(model,m['columns'][i]['power']) in noisy['input_domains'][i] for i in indices)]
    def check_ramification(x):assert x['model_ids']==expected_ids
    control('admit_ramified_model_at_seven',entry,lambda x:x['model_ids'].append(wrong),check_ramification,
            'The inserted model matches the noisy coefficient domains but violates the declared discriminant-ramification rule at seven.')
    assert len(controls) in [9,10]
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in [certificate_path,feedback_path,audit_path,measurements,proposals,previous_proposals,truth_path]+inputs},
            'actual_component_mutations_rejected':len(controls),'controls':controls,'search_probes':probes,'frozen_moment_counterexample':counterexample,
            'scope':'Semantic component mutations test moment normalization, continuous covers, moment coupling, nonnegative duals, local/dual prerequisites, noise-radius provenance and local assumptions. The one-root counterexample concerns the analytic error-budget expression, not actual attainment of the unknown-zero bound or global field ambiguity.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['certificate','feedback','audit','measurements','proposals','previous-proposals','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args()
    r=run(a.certificate,a.feedback,a.audit,a.measurements,a.proposals,a.previous_proposals,a.inputs,a.truth);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'mutations_rejected':len(r['controls']),'probes':r['search_probes']}))
