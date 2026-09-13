"""Challenge exact interval-transfer direction, population and inherited premise identity."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from dedekind_aggregate_nested_audit import check_transfer
from dedekind_aggregate_moment_local_audit import digest

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(value):assert value

def run(nested_path,audit_path,closure_path,inputs,prior_closure,lean_path):
    data=json.loads(nested_path.read_text());audit=json.loads(audit_path.read_text());closure=json.loads(closure_path.read_text());prior=json.loads(prior_closure.read_text());lean=json.loads(lean_path.read_text())
    sources=[json.loads(p.read_text()) for p in inputs]
    assert audit['status']==closure['status']==lean['status']=='passed' and audit['inputs_sha256'][nested_path.name]==sha(nested_path)
    case=next(c for c in data['cases'] if c['observation_index']==0 and c['radius']=='2/25' and c['profile']=='degree_discriminant')
    proof=case['transfer'];source=sources[0];seed=prior['cases'][case['prior_case_index']];controls=[]
    def reject(name,original,changed,predicate,scope):
        predicate(original);caught=False
        try:predicate(changed)
        except (AssertionError,ValueError,IndexError,KeyError):caught=True
        assert caught,name
        controls.append({'name':name,'baseline_passed':True,'mutation_rejected':True,'original_component_sha256':digest(original),
                         'mutated_component_sha256':digest(changed),'predicate':scope})
    def radius_contract(pair):
        p,r=pair;check_transfer(p,source,r,seed['radius'])
    reverse=copy.deepcopy(proof);reverse['destination_radius']='3/25'
    reject('transfer_to_larger_uncertainty',(proof,case['radius']),(reverse,'3/25'),radius_contract,
           'The destination radius must not exceed the radius whose domains were proved.')
    tiny=F(10**20+1,10**21);assert tiny>F('1/10') and float(tiny)==float(F('1/10'))
    equal=next(c['transfer'] for c in data['cases'] if c['observation_index']==0 and c['radius']=='1/10' and c['profile']==case['profile'])
    rounded=copy.deepcopy(equal);rounded['destination_radius']=str(tiny)
    reject('round_away_outward_radius_increase',(equal,'1/10'),(rounded,str(tiny)),radius_contract,
           'Exact rational order rejects an outward increase of 1e-21 even when both radii have the same binary64 value.')
    negative=copy.deepcopy(proof);negative['destination_radius']='-1/100'
    reject('negative_noise_radius',(proof,case['radius']),(negative,'-1/100'),radius_contract,
           'The physical uncertainty contract requires a nonnegative radius.')
    predicate=lambda p:check_transfer(p,source,case['radius'],seed['radius'])
    changed=copy.deepcopy(proof);changed['roots'].pop()
    reject('drop_root_population_member',proof,changed,predicate,'Every inherited root index must be represented in the containment proof.')
    changed=copy.deepcopy(proof);changed['roots'][0],changed['roots'][1]=changed['roots'][1],changed['roots'][0]
    reject('swap_root_correspondence',proof,changed,predicate,'Intervals must correspond to the same original root index.')
    altered=copy.deepcopy(source);altered['positive_root_intervals'][0]['lo']=str(F(altered['positive_root_intervals'][0]['lo'])+F('1/100'))
    altered['positive_root_intervals'][0]['hi']=str(F(altered['positive_root_intervals'][0]['hi'])+F('1/100'))
    reject('change_original_spectral_center',source,altered,lambda s:check_transfer(proof,s,case['radius'],seed['radius']),
           'Containment endpoints are reconstructed from the fixed source intervals, not just from recorded margins.')
    changed=copy.deepcopy(proof);changed['roots'][0]['inner_interval'][0]=str(F(changed['roots'][0]['outer_interval'][0])-F('1/1000000'))
    reject('extend_inner_endpoint_beyond_seed',proof,changed,predicate,'Both sides of every inner interval must stay within the original wider interval.')
    def seed_contract(s):
        check(s['observation_index']==case['observation_index'] and s['profile']==case['profile'] and F(case['radius'])<=F(s['radius']))
        check(s['final_domains']==case['input_domains'])
    wrong=next(c for c in prior['cases'] if c['observation_index']==1 and c['radius']=='1/10' and c['profile']==case['profile'])
    reject('borrow_other_observation_domains',seed,wrong,seed_contract,'The inherited domains must belong to the same observation and local profile.')
    narrow=next(c for c in prior['cases'] if c['observation_index']==0 and c['radius']=='1/50' and c['profile']==case['profile'])
    reject('borrow_smaller_radius_singletons',seed,narrow,seed_contract,'A narrower-radius success cannot seed this wider-radius calculation.')
    reject('replace_seed_by_future_domains',case['input_domains'],case['final_domains'],lambda x:check(x==seed['final_domains']),
           'Initial coefficient domains must exactly match the previously validated seed, before this pass makes deductions.')
    root=source['positive_root_intervals'][0];lo,hi=F(root['lo']),F(root['hi']);small,big=F(case['radius']),F(seed['radius']);point=hi+big
    assert lo-big<=point<=hi+big and point>hi+small
    counterexample={'root_index':0,'source_lo':str(lo),'source_hi':str(hi),'smaller_radius':str(small),'larger_radius':str(big),'point':str(point),
                    'inside_larger_interval':True,'outside_smaller_interval':True,'strict_upper_violation':str(point-hi-small),
                    'predicate_valid_on_smaller_interval':'x <= source_hi + smaller_radius',
                    'scope':'A universal predicate on the smaller box fails at this permitted point of the larger box. This disproves unrestricted reverse certificate transfer; it is not an alternate-field or spectral-realizability witness.'}
    rounding={'inner_radius':str(tiny),'seed_radius':'1/10','same_binary64_value':float(tiny),'exact_outward_increase':str(tiny-F('1/10')),
              'outside_point':str(hi+tiny),'seed_upper_endpoint':str(hi+F('1/10')),
              'scope':'This is the same exact-order mutation counted above, presented as an explicit endpoint witness; it is not an additional independent experiment.'}
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [nested_path,audit_path,closure_path,prior_closure,lean_path]+inputs},
            'actual_component_mutations_rejected':len(controls),'controls':controls,'reverse_transfer_counterexample':counterexample,
            'rounded_radius_counterexample':rounding,'kernel_checked_theorem_names':lean['theorems'],
            'scope':'Ten actual mutations test the new premise-transfer contract. Exact endpoint witnesses expose reverse-direction and binary64-order errors. The four Lean theorems concern box geometry and predicate transport, not the full arithmetic or numerical proof.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['nested','audit','closure','prior-closure','lean','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args();r=run(a.nested,a.audit,a.closure,a.inputs,a.prior_closure,a.lean)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'mutations':r['actual_component_mutations_rejected'],'theorems':len(r['kernel_checked_theorem_names'])}))
