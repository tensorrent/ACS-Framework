"""Challenge adaptive premise lineage and construct a stale-budget counterexample."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_aggregate_integer_audit import integer_rows,endpoint,GRID
from dedekind_aggregate_moment_local_audit import project,integer_dual,domain_bound,digest
from dedekind_aggregate_local_audit import catalog
from dedekind_aggregate_shared_audit import terms_for
from dedekind_aggregate_noise_audit import complex_values
from dedekind_aggregate_adaptive_audit import audit_budget

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(condition):assert condition

def run(adaptive_path,audit_path,closure_path,measurements,inputs,prior_feedback,truth_path):
    ctx.prec=384;d=json.loads(adaptive_path.read_text());audit=json.loads(audit_path.read_text());closure=json.loads(closure_path.read_text())
    m=json.loads(measurements.read_text());sources=[json.loads(p.read_text()) for p in inputs];prior=json.loads(prior_feedback.read_text());truth=json.loads(truth_path.read_text())['arithmetic_vectors']
    assert audit['status']==closure['status']=='passed' and audit['inputs_sha256'][adaptive_path.name]==sha(adaptive_path)
    controls=[]
    def reject(name,original,changed,predicate,scope):
        predicate(original);caught=False
        try:predicate(changed)
        except (AssertionError,ValueError,IndexError,KeyError):caught=True
        assert caught,name
        controls.append({'name':name,'baseline_passed':True,'mutation_rejected':True,'original_component_sha256':digest(original),'mutated_component_sha256':digest(changed),'predicate':scope})
    case=next(c for c in d['cases'] if c['radius']=='1/10' and c['profile']=='degree_discriminant' and c['observation_index']==0)
    seed=prior['cases'][case['prior_case_index']];wrong=next(c for c in prior['cases'] if c['radius']=='0' and c['method']=='coupled' and c['profile']==case['profile'] and c['observation_index']==0)
    reject('borrow_zero_radius_seed',seed,wrong,lambda x:check(x['method']=='coupled' and all(x[k]==case[k] for k in ['observation_index','radius','profile'])),
           'A seed must have the same observation, uncertainty radius and local profile.')
    after,_,_=project(m['columns'],case['input_domains'],case['profile'])
    reject('use_final_domains_as_initial_premises',after,case['final_domains'],lambda x:check(digest(x)==case['rounds'][0]['after_local_sha256']),
           'The premise is reconstructed from the inherited validated state, before this round makes exclusions.')
    p=next(p for p in case['rounds'][0]['proposals'] if p['multipliers']);i=p['certificate_index'];c=d['certificates'][i]
    other=next(b for j,b in enumerate(audit['budget_replays']) if j!=i and b['certificate_sha256']!=digest(c))
    reject('attach_budget_from_different_multiplier',audit['budget_replays'][i],other,lambda b:check(b['certificate_sha256']==digest(c)),
           'The validated analytic budget is bound to the full certificate, including its rational multipliers.')
    changed=copy.deepcopy(p);changed['sign']=-p['sign']
    reject('reverse_target_sign',p,changed,lambda x:check(all(x[k]==c[k] for k in ['observation_index','radius','column','n','sign','multipliers'])),
           'The proposal and certificate must describe the same signed objective.')
    altered=copy.deepcopy(m)
    for r in altered['rows']:
        for obs in [0,1]:r['observations'][obs]['R']=r['observations'][obs]['unwidened']
    rows=integer_rows(altered,0);changed=copy.deepcopy(c);changed['multipliers'][0][1]=str(-abs(F(changed['multipliers'][0][1])))
    reject('negative_dual_multiplier',c,changed,lambda x:integer_dual(rows,x,len(m['columns'])),
           'Integer inequality combination requires distinct row indices and nonnegative rational multipliers.')
    active=next(c for c in d['certificates'] if c['radius']!='0' and any(r['leaves'] for r in c['root_bounds']))
    changed=copy.deepcopy(active);next(r for r in changed['root_bounds'] if r['leaves'])['leaves'].pop()
    reject('drop_continuum_cover_leaf',active,changed,lambda x:audit_budget(m,sources[x['observation_index']],x),
           'The independent audit requires a complete rational partition for every active root interval.')
    changed=copy.deepcopy(active);changed['multipliers'][0][1]=str(2*F(changed['multipliers'][0][1]))
    reject('change_multiplier_after_certification',active,changed,lambda x:audit_budget(m,sources[x['observation_index']],x),
           'Fresh alpha/sigma reconstruction must agree with the stored shared functions and tail multiplier.')
    witness=case['rounds'][0]['dual_removals'][0];cert=d['certificates'][witness['certificate_index']];budget=audit['budget_replays'][witness['certificate_index']]['budget_upper']
    upper=domain_bound(integer_dual(rows,cert,len(m['columns'])),after,budget)
    changed=copy.deepcopy(witness);changed['candidate']=truth['A'][witness['column']]
    reject('remove_heldout_true_value',witness,changed,lambda x:check(x['candidate'] in after[x['column']] and cert['sign']*x['candidate']>upper),
           'A strictly positive independently recomputed gap is required; this predicate does not consult truth.')
    models=catalog();reject('omit_local_catalogue_model',models,models[:-1],lambda x:check(x==catalog()),
           'Generic local possibilities must match independent degree-partition enumeration.')
    # Check the general-box LP support formula on actual integer residuals.
    prepared=integer_dual(rows,c,len(m['columns']));rhs,residual,unit=prepared;support_checks=0;bad=None
    for k,(r,domain) in enumerate(zip(residual,after)):
        exact=max(r*v for v in domain);formula=domain[0]*r+(domain[-1]-domain[0])*max(r,0);assert exact==formula;support_checks+=1
        if r<0 and domain[-1]>domain[0]:bad=(k,r,domain,exact,r*domain[-1])
    assert bad
    k,r,domain,correct,incorrect=bad
    reject('choose_lower_support_for_negative_residual',correct,incorrect,lambda value:check(value>=max(r*v for v in domain)),
           'Maximizing a negative residual uses the smallest domain value; reversing the endpoint understates the support.')
    # A concrete allowed displacement proves that keeping a previous budget after
    # changing multipliers can fail, even before adding any unknown-zero tail.
    selected=None
    for index,candidate in enumerate(d['certificates']):
        if candidate['radius']=='0' or not candidate['multipliers']:continue
        _,_,terms=terms_for(m,candidate);roots=sources[candidate['observation_index']]['positive_root_intervals'];delta=F(candidate['radius']);a=arb(1)/25
        finite=arb(0);points=[]
        for root in roots:
            center=(F(root['lo'])+F(root['hi']))/2;base,_,_=complex_values(arb(str(center)),a,terms);options=[]
            for point in [center-delta,center+delta]:
                h,_,_=complex_values(arb(str(point)),a,terms);options.append((-2*(h-base),point))
            value,point=max(options,key=lambda x:float(x[0].mid()));finite+=value;points.append(str(point))
        if finite>0:
            selected=(index,candidate,finite,points);break
    assert selected
    index,candidate,finite,points=selected;old=F(audit['budget_replays'][index]['budget_upper']);assert arb(str(old))>=finite.upper()
    lower=F(endpoint(encode(finite),False),GRID);factor=max(2,int(2*old/lower)+1)
    changed=copy.deepcopy(candidate);changed['multipliers']=[[j,str(factor*F(v))] for j,v in changed['multipliers']]
    _,_,terms=terms_for(m,changed);actual=arb(0);roots=sources[changed['observation_index']]['positive_root_intervals']
    for root,point in zip(roots,points):
        center=(F(root['lo'])+F(root['hi']))/2;h,_,_=complex_values(arb(point),a,terms);base,_,_=complex_values(arb(str(center)),a,terms);actual+=-2*(h-base)
    assert actual>arb(str(old)) and actual.overlaps(factor*finite) and arb(str(factor*old))>=actual.upper()
    counterexample={'certificate_index':index,'observation_index':candidate['observation_index'],'radius':candidate['radius'],'n':candidate['n'],'sign':candidate['sign'],
                    'multiplier_scale':factor,'allowed_displaced_ordinates':points,'old_valid_budget':str(old),'original_finite_change':encode(finite),
                    'changed_multiplier_finite_change':encode(actual),'strict_excess_over_stale_budget':encode(actual-arb(str(old))),'scaled_valid_budget':str(factor*old),
                    'scope':'Positive scaling changes the measurement combination. These permitted exact displaced ordinates make its finite-sum change exceed the unscaled old total budget. Scaling the old valid budget by the same positive factor repairs this diagnostic. No unknown-tail saturation or alternate number field is claimed.'}
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [adaptive_path,audit_path,closure_path,measurements,prior_feedback,truth_path]+inputs},
            'actual_component_mutations_rejected':len(controls),'controls':controls,'exact_general_domain_support_checks':support_checks,
            'stale_budget_counterexample':counterexample,'scope':'Ten component mutations challenge adaptive lineage, uncertainty coupling, continuum coverage and integer support. A separate interval witness demonstrates why changed multipliers require changed error budgets. This is not a formal proof of software noninterference or a global realization audit.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['adaptive','audit','closure','measurements','prior-feedback','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args();r=run(a.adaptive,a.audit,a.closure,a.measurements,a.inputs,a.prior_feedback,a.truth)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'mutations':r['actual_component_mutations_rejected'],'support_checks':r['exact_general_domain_support_checks'],'counterexample_scale':r['stale_budget_counterexample']['multiplier_scale']}))
