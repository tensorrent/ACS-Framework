"""Attack variable-noise scaling, fixed coordinates, midpoint claims and source feasibility."""
import argparse,copy,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from dedekind_variable_noise_audit import audit_data

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(boundary,shifted,certificate,anchor,region,inputs):
    paths=[boundary,shifted,certificate,anchor,region,inputs];p,q,c,a,r=[json.loads(x.read_text()) for x in paths[:-1]]
    with zipfile.ZipFile(inputs) as z:d={n:json.loads(z.read(n)) for n in z.namelist()}
    assert audit_data(p,q,c,a,r,d)['status']=='passed';mutations=[]
    def test(name,change):
        pp,qq,cc,aa,rr,dd=copy.deepcopy((p,q,c,a,r,d));change(pp,qq,cc,aa,rr,dd)
        try:audit_data(pp,qq,cc,aa,rr,dd)
        except (AssertionError,ValueError,TypeError,KeyError,IndexError,StopIteration,ZeroDivisionError) as error:
            mutations.append({'name':name,'status':'rejected','exception':type(error).__name__});return
        raise AssertionError('Accepted mutation: '+name)
    test('post-noise population selection',lambda p,q,c,a,r,d:c['contract'].update(source_selection='after_noise'))
    test('relative feature errors',lambda p,q,c,a,r,d:c['contract'].update(additional_feature_errors='relative'))
    test('raw roots released',lambda p,q,c,a,r,d:c['contract'].update(raw_roots_or_counts_released=True))
    test('unknown tail introduced',lambda p,q,c,a,r,d:c['contract'].update(unknown_tails_included=True))
    test('weighted ball substituted for coordinate cube',lambda p,q,c,a,r,d:c['contract'].update(region_geometry='weighted_ball'))
    test('expanded region without certificate',lambda p,q,c,a,r,d:c['contract'].update(observed_root_region_radius='1'))
    test('fixed feature report contract',lambda p,q,c,a,r,d:c['contract'].update(common_release_type='fixed_Phi_c'))
    test('wrong source discriminant',lambda p,q,c,a,r,d:d['E1_224.json'].update(discriminant=1))
    test('missing source root',lambda p,q,c,a,r,d:d['E2_160.json']['positive_root_intervals'].pop())
    test('missing source precision',lambda p,q,c,a,r,d:d.pop('E1_160.json'))
    test('wrong source cutoff',lambda p,q,c,a,r,d:d['E1_224.json'].update(top='20'))
    test('wrong feature kernel',lambda p,q,c,a,r,d:a['full_rank_proposal']['features'][0].update(center=3))
    test('infinite moment substituted',lambda p,q,c,a,r,d:a['full_rank_proposal']['features'][17].update(kind='infinite_moment'))
    test('wrong midpoint root center',lambda p,q,c,a,r,d:c['common_root_center'].__setitem__(1,'1'))
    test('wrong root noise radius',lambda p,q,c,a,r,d:q.update(root_coordinate_error_radius='1'))
    test('removed critical safety margin',lambda p,q,c,a,r,d:q.update(critical_epsilon='1e-8'))
    test('missing boundary pair',lambda p,q,c,a,r,d:p['cases'].pop())
    test('missing shifted pair',lambda p,q,c,a,r,d:q['cases'].pop())
    test('wrong pair count',lambda p,q,c,a,r,d:c.update(certified_pair_count=3))
    test('zero direction component',lambda p,q,c,a,r,d:c['feature_direction'].__setitem__(0,0))
    test('wrong signed direction',lambda p,q,c,a,r,d:p['cases'][0]['feature_difference_direction'].__setitem__(0,1))
    test('critical root included as variable',lambda p,q,c,a,r,d:p['cases'][0]['free_A_indices'].__setitem__(0,1))
    test('boolean root index',lambda p,q,c,a,r,d:p['cases'][0]['free_A_indices'].__setitem__(0,False))
    test('missing root correction',lambda p,q,c,a,r,d:p['cases'][0]['A_coordinate_corrections'].pop())
    test('numerical failure relabeled a solution',lambda p,q,c,a,r,d:p['cases'][0].update(numerically_converged=False))
    test('22 root unknowns claimed',lambda p,q,c,a,r,d:c['cases'][0].update(root_variable_count=22))
    test('wrong system dimension',lambda p,q,c,a,r,d:c['cases'][0].update(variable_dimension=21))
    test('wrong noise variable index',lambda p,q,c,a,r,d:c['cases'][0].update(noise_variable_index=1))
    test('unscaled noise variable definition',lambda p,q,c,a,r,d:c['cases'][0].update(noise_variable_definition='alpha=tau'))
    test('missing tau scale',lambda p,q,c,a,r,d:p['cases'][0].update(tau_scale='1'))
    test('negative tau scale',lambda p,q,c,a,r,d:p['cases'][0].update(tau_scale='-1e-10'))
    test('nonpositive alpha',lambda p,q,c,a,r,d:p['cases'][0].update(scaled_tau='0'))
    test('incorrect constant noise column',lambda p,q,c,a,r,d:c['cases'][0]['noise_jacobian_column'].__setitem__(0,'0'))
    test('invented noise-column variation',lambda p,q,c,a,r,d:c['cases'][0].update(noise_column_derivative_variation='1'))
    test('changed variable center',lambda p,q,c,a,r,d:c['cases'][0]['variable_center'].__setitem__(21,'1'))
    test('wrong variable box radius',lambda p,q,c,a,r,d:c['cases'][0].update(variable_box_radius='1e-80'))
    test('fixed A critical coordinate erased',lambda p,q,c,a,r,d:p['cases'][0].update(fixed_A_critical_coordinate='0'))
    test('fixed B critical coordinate erased',lambda p,q,c,a,r,d:p['cases'][0]['fixed_B_coordinates'].__setitem__(1,'0'))
    test('altered shifted B root',lambda p,q,c,a,r,d:q['cases'][0]['fixed_B_coordinates'].__setitem__(0,'1'))
    test('zero inverse row',lambda p,q,c,a,r,d:p['cases'][0]['preconditioner'].__setitem__(0,['0']*22))
    test('missing inverse row',lambda p,q,c,a,r,d:p['cases'][0]['preconditioner'].pop())
    test('off-equation A correction',lambda p,q,c,a,r,d:p['cases'][0]['A_coordinate_corrections'].__setitem__(0,'0'))
    test('source observation box changed',lambda p,q,c,a,r,d:c['cases'][0]['A_observation_boxes'][0].__setitem__(0,'0'))
    test('inflated cube margin',lambda p,q,c,a,r,d:c['cases'][0].update(minimum_cube_margin='1'))
    test('erased critical gap',lambda p,q,c,a,r,d:c['cases'][0].update(exact_critical_root_gap='0'))
    test('undersized tau upper endpoint',lambda p,q,c,a,r,d:c['cases'][0]['tau_interval'].__setitem__(1,'1e-12'))
    test('undersized pair budget',lambda p,q,c,a,r,d:c['cases'][0].update(budget_guaranteed_for_pair='1e-12'))
    test('wrong exact feature difference factor',lambda p,q,c,a,r,d:c['cases'][0]['signed_difference_coefficients'].__setitem__(0,-1))
    test('midpoint reported as Phi(c)',lambda p,q,c,a,r,d:c['cases'][0].update(common_release='Phi(c)'))
    test('midpoint-equality flag reversed',lambda p,q,c,a,r,d:c['cases'][0].update(midpoint_is_Phi_c=True))
    test('zero feature error falsely claimed',lambda p,q,c,a,r,d:c['cases'][0].update(feature_error_for_exact_pair='0'))
    test('missing direct precision',lambda p,q,c,a,r,d:c['cases'][0]['direct_checks'].pop())
    test('noncontractive direct bound',lambda p,q,c,a,r,d:c['cases'][0]['direct_checks'][0]['rows'][0].update(derivative_defect={'mid':[2,0],'rad':[0,0]}))
    test('zero strict self-map margin',lambda p,q,c,a,r,d:c['cases'][0]['direct_checks'][0]['rows'][0].update(strict_margin={'mid':[0,0],'rad':[0,0]}))
    test('corrupt serialized equation residual',lambda p,q,c,a,r,d:c['cases'][0]['direct_checks'][0]['F_at_rational_center'].__setitem__(0,{'mid':[1,0],'rad':[0,0]}))
    test('false midpoint enclosure',lambda p,q,c,a,r,d:c['cases'][0]['direct_checks'][0]['common_midpoint_feature_enclosures'].__setitem__(0,{'mid':[100,0],'rad':[0,0]}))
    test('false midpoint displacement enclosure',lambda p,q,c,a,r,d:c['cases'][0]['direct_checks'][0]['midpoint_minus_Phi_c_enclosures'].__setitem__(0,{'mid':[0,0],'rad':[0,0]}))
    test('negative serialized radius',lambda p,q,c,a,r,d:c['cases'][0]['direct_checks'][0]['rows'][0]['derivative_defect'].update(rad=[-1,0]))
    test('missing source inequality',lambda p,q,c,a,r,d:c['cases'][0]['coordinate_audit'].pop())
    test('inflated source margin',lambda p,q,c,a,r,d:c['cases'][0]['coordinate_audit'][0].update(error_margin='1'))
    test('false best upper bound',lambda p,q,c,a,r,d:c.update(best_certified_tau_upper='1e-12'))
    test('undersized convenient budget',lambda p,q,c,a,r,d:c.update(convenient_feature_budget='1e-12'))
    test('inflated uniform guarantee',lambda p,q,c,a,r,d:c.update(uniform_identification_below='1e-9'))
    test('false threshold ratio',lambda p,q,c,a,r,d:c.update(upper_to_guarantee_ratio='1'))
    # Exact controls separate the algorithm/representation from the mathematical question.
    a,b,z0,z1,budget=map(F,[2,4,0,3,1]);assert abs(z0-a)>budget and abs(z0-b)>budget and abs(z1-a)==abs(z1-b)==budget
    f=lambda x:x*x-1;assert f(F(-1))==f(F(1))==0 and f(F(0))==-1 and 2*F(0)==0
    scale,alpha,rho=F(1,10),F(2),F(1,100);lo,hi=scale*(alpha-rho),scale*(alpha+rho);assert (lo,hi)==(F(199,1000),F(201,1000)) and hi-lo==2*scale*rho
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in paths},'mutations_rejected':len(mutations),'mutations':mutations,
        'fixed_report_scope_control':{'feature_values':['2','4'],'rejected_report':'0','feasible_midpoint_report':'3','component_budget':'1','conclusion':'Failure at one fixed report does not exclude another common report.'},
        'Newton_failure_control':{'polynomial':'x^2-1','failed_start':'0','derivative_at_start':'0','actual_roots':['-1','1'],'conclusion':'A singular Newton step is compatible with exact roots elsewhere.'},
        'scaled_noise_control':{'scale':str(scale),'alpha':str(alpha),'variable_radius':str(rho),'tau_interval':[str(lo),str(hi)],'constant_noise_column':'-1/5','noise_column_variation':'0'},
        'scope':'Independent-auditor mutation paths and exact arithmetic controls test scaling, root/noise dimensions, fixed coordinates, source constraints, moving midpoints and the distinction between search failures and impossibility. They do not certify global optimality.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['boundary','shifted','certificate','anchor','region','inputs','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a.boundary,a.shifted,a.certificate,a.anchor,a.region,a.inputs);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'mutations_rejected':r['mutations_rejected']}))
