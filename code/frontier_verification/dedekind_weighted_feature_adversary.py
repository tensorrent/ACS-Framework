"""Adversarial tests for weighted regions, supersolutions and noisy feature targets."""
import argparse,copy,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from dedekind_weighted_region_audit_v2 import audit_data as region_audit
from dedekind_feature_space_audit import audit_data as feature_audit

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(anchor,exploration,region,feature_proposal,feature_certificate,inputs,prior,diagnosis):
    paths=[anchor,exploration,region,feature_proposal,feature_certificate,inputs,diagnosis]
    a,e,r,p,c,diag=[json.loads(x.read_text()) for x in [anchor,exploration,region,feature_proposal,feature_certificate,diagnosis]]
    with zipfile.ZipFile(inputs) as z:d={n:json.loads(z.read(n)) for n in z.namelist()}
    old={}
    for suffix in ['Enlarged','Small','Local']:
        path=prior/f'Augmented_Certificate_{suffix}_v2.json';paths.append(path);old[suffix]=json.loads(path.read_text())
    assert region_audit(a,e,r,d,old)['status']==feature_audit(p,c,a,r,d)['status']=='passed';mutations=[]
    errors=(AssertionError,ValueError,TypeError,KeyError,IndexError,StopIteration,ZeroDivisionError)
    def region_test(name,change):
        aa,ee,rr,dd=copy.deepcopy((a,e,r,d));change(aa,ee,rr,dd)
        try:region_audit(aa,ee,rr,dd,old)
        except errors as error:mutations.append({'name':name,'surface':'region','status':'rejected','exception':type(error).__name__});return
        raise AssertionError('Accepted region mutation: '+name)
    def feature_test(name,change):
        pp,cc,aa,rr,dd=copy.deepcopy((p,c,a,r,d));change(pp,cc,aa,rr,dd)
        try:feature_audit(pp,cc,aa,rr,dd)
        except errors as error:mutations.append({'name':name,'surface':'feature_space','status':'rejected','exception':type(error).__name__});return
        raise AssertionError('Accepted feature mutation: '+name)
    def weights(e):return next(x for x in e['radius_tests'] if F(x['radius'])==F(3,100) and x['derivative_Taylor_order']==6)['positive_rational_weights']
    region_test('zero weight',lambda a,e,r,d:weights(e).__setitem__(1,'0'))
    region_test('negative weight',lambda a,e,r,d:weights(e).__setitem__(1,'-1'))
    region_test('missing weight',lambda a,e,r,d:weights(e).pop())
    region_test('wrong domain geometry',lambda a,e,r,d:r['regions'][0].update(domain='weighted_ball'))
    region_test('unsupported larger radius',lambda a,e,r,d:r['regions'][0].update(radius='1'))
    region_test('wrong feature dimension',lambda a,e,r,d:r['regions'][0].update(dimension=21))
    region_test('moment removed',lambda a,e,r,d:a['full_rank_proposal']['features'].pop(17))
    region_test('changed kernel center',lambda a,e,r,d:a['full_rank_proposal']['features'][-1].update(center=41))
    region_test('changed center vector',lambda a,e,r,d:a['common_rational_coordinates'].__setitem__(1,'1'))
    region_test('missing full inverse row',lambda a,e,r,d:a['full_rank_proposal']['preconditioner'].pop())
    region_test('wrong Taylor order',lambda a,e,r,d:r['regions'][0].update(derivative_Taylor_order=5))
    region_test('missing point derivative term',lambda a,e,r,d:r['regions'][0]['point_derivative_orders'].pop())
    region_test('wrong remainder derivative',lambda a,e,r,d:r['regions'][0].update(remainder_derivative_order=6))
    region_test('wrong remainder factorial',lambda a,e,r,d:r['regions'][0].update(remainder_factorial=5040))
    region_test('nonpositive majorant entry',lambda a,e,r,d:r['regions'][0]['exact_nonnegative_majorant'][0].__setitem__(0,'-1'))
    region_test('truncated majorant',lambda a,e,r,d:r['regions'][0]['exact_nonnegative_majorant'].pop())
    region_test('wrong exact weighted sum',lambda a,e,r,d:r['regions'][0]['exact_weighted_row_sums'].__setitem__(0,'0'))
    region_test('false row norm',lambda a,e,r,d:r['regions'][0]['exact_preconditioner_row_norms'].__setitem__(1,'0'))
    region_test('undersized critical supersolution',lambda a,e,r,d:r['regions'][0]['exact_componentwise_inverse_bounds'].__setitem__(1,'1'))
    region_test('false critical bound',lambda a,e,r,d:r['regions'][0].update(critical_inverse_bound='1'))
    region_test('wrong critical index',lambda a,e,r,d:r['regions'][0].update(critical_index=0))
    region_test('inflated uniform noise guarantee',lambda a,e,r,d:r['regions'][0].update(uniform_feature_error_identification_guarantee_strictly_below='1'))
    region_test('wrong root noise radius',lambda a,e,r,d:r['regions'][0].update(root_coordinate_error_radius='0'))
    region_test('false source gap',lambda a,e,r,d:r['regions'][0].update(source_critical_separation_lower='1'))
    region_test('incorrect rounding metadata',lambda a,e,r,d:r['regions'][0].update(dyadic_rounding_bits=8))
    region_test('wrong precision coverage',lambda a,e,r,d:r['regions'][0]['checks'].pop())
    region_test('false serialized upper enclosure',lambda a,e,r,d:r['regions'][0]['checks'][0]['majorant_matrix'][0].__setitem__(0,{'mid':[1000000,0],'rad':[0,0]}))
    feature_test('root versus feature error contract changed',lambda p,c,a,r,d:c['contract'].update(additional_feature_errors='relative_errors'))
    feature_test('raw observations released',lambda p,c,a,r,d:c['contract'].update(raw_roots_or_counts_released=True))
    feature_test('unknown tail introduced',lambda p,c,a,r,d:c['contract'].update(unknown_tails_included=True))
    feature_test('post-noise population selection',lambda p,c,a,r,d:c['contract'].update(source_selection='after_noise'))
    feature_test('zero feature direction',lambda p,c,a,r,d:p['feature_direction'].__setitem__(0,0))
    feature_test('incorrect direction sign',lambda p,c,a,r,d:p['feature_direction'].__setitem__(0,-p['feature_direction'][0]))
    feature_test('field signs swapped',lambda p,c,a,r,d:p['cases'][0]['A'].update(field_sign=-1))
    feature_test('negative feature budget',lambda p,c,a,r,d:p['cases'][0].update(feature_error_bound='-1'))
    feature_test('wrong root error radius',lambda p,c,a,r,d:p.update(root_coordinate_error_radius='1'))
    feature_test('missing inverse target',lambda p,c,a,r,d:p['cases'].pop())
    feature_test('zero inverse matrix row',lambda p,c,a,r,d:p['cases'][0]['A']['preconditioner'].__setitem__(0,['0']*22))
    feature_test('off-target root correction',lambda p,c,a,r,d:p['cases'][0]['A']['corrections'].__setitem__(0,'0'))
    feature_test('unjustified observation box',lambda p,c,a,r,d:c['cases'][0]['roots']['A']['observation_boxes'][0].__setitem__(0,'0'))
    feature_test('wrong correction box size',lambda p,c,a,r,d:c['cases'][0]['roots']['A'].update(correction_box_radius='1e-80'))
    feature_test('false local membership',lambda p,c,a,r,d:c['cases'][0]['roots']['A'].update(inside_radius_0p01_cube=False))
    feature_test('missing scalar source check',lambda p,c,a,r,d:c['cases'][0]['coordinate_audit'].pop())
    feature_test('source margin inflated',lambda p,c,a,r,d:c['cases'][0]['coordinate_audit'][0].update(error_margin='1'))
    feature_test('excluded target relabeled feasible',lambda p,c,a,r,d:c['cases'][2].update(status='actual_source_common_noisy_release'))
    feature_test('missing uniform exclusion',lambda p,c,a,r,d:c['cases'][2]['uniform_source_exclusions'].pop())
    feature_test('wrong signed feature difference',lambda p,c,a,r,d:c['cases'][0]['exact_feature_difference_vector'].__setitem__(0,'0'))
    feature_test('wrong pair distance',lambda p,c,a,r,d:c['cases'][0].update(exact_feature_pair_infinity_distance='0'))
    feature_test('false ambiguity upper bound',lambda p,c,a,r,d:c.update(actual_ambiguity_at='1e-12'))
    feature_test('false guarantee ratio',lambda p,c,a,r,d:c.update(upper_to_guarantee_ratio='1'))
    feature_test('truncated source population',lambda p,c,a,r,d:d['E1_224.json']['positive_root_intervals'].pop())
    feature_test('wrong source discriminant',lambda p,c,a,r,d:d['E1_224.json'].update(discriminant=1))
    # Exact polynomial control for missing or mis-scaled Taylor remainders.
    C=F(4096,14197);f=lambda x:x-C*x**7;x=F(3,4);y=F(1)
    assert x!=y and f(x)==f(y) and 7*C>1 and C<F(1,2)
    remainder_control={'map':'x - (4096/14197)*x^7','center':'0','region':['-1','1'],'distinct_equal_image_points':['3/4','1'],
        'common_image':str(f(x)),'correct_derivative_remainder_bound':str(7*C),'bound_if_remainder_omitted':'0','bound_if_divided_by_7_factorial_instead_of_6_factorial':str(C),
        'conclusion':'The omitted or wrong-factorial bound would falsely imply injectivity; the full order-6 remainder prevents that inference.'}
    eta=F(3,100);wsmall=F(1,100);coordinate=eta/2
    assert coordinate<=eta and coordinate/wsmall>eta
    assert diag['endpoint_comparisons']==1936 and diag['exact_rational_endpoint_violations']==[] and len(diag['reconstructed_ball_comparison_failures'])==108
    assert all(F(x['exact_margin'])>=0 and F(x['reconstructed_endpoint_inflation'])>0 for x in diag['reconstructed_ball_comparison_failures'])
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in paths},'mutations_rejected':len(mutations),'mutations':mutations,
        'exact_Taylor_remainder_counterexample':remainder_control,'domain_geometry_control':{'eta':str(eta),'weights':['1/100','1'],'point':[str(coordinate),'0'],'in_standard_cube':True,'in_weighted_ball':False},
        'serialization_control':{'exact_endpoint_checks':1936,'exact_failures':0,'constructor_inflation_false_rejections':108},
        'scope':'Semantic auditor rejection paths and exact mathematical counterexamples test Taylor remainders, weighted geometry, componentwise stability, source feasibility and the distinction between a rejected signed construction and a global impossibility claim.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['anchor','exploration','region','feature-proposal','feature-certificate','inputs','prior','diagnosis','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a.anchor,a.exploration,a.region,a.feature_proposal,a.feature_certificate,a.inputs,a.prior,a.diagnosis);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'mutations_rejected':r['mutations_rejected'],'exact_controls':['Taylor remainder','domain geometry','serialized endpoints']}))
