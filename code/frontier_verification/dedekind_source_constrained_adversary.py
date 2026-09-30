"""Attack source-strip hypotheses, mixed-coordinate signs and serialized proof premises."""
import argparse,copy,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from dedekind_source_constrained_audit import strip_data,audit_pairs,ROOT,PRIOR,ANCHOR,REGION,UPPER,SOURCE
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def put(d,path,value):
    for k in path[:-1]:d=d[k]
    d[path[-1]]=value
def run(strip,mixed,proposal,root=ROOT):
    paths=[root/p for p in [PRIOR,ANCHOR,REGION,UPPER,SOURCE+'/Equal_Population_Inputs.zip']]
    prior,a,reg,upper=map(read,paths[:4]);sc,mc,p=map(read,[strip,mixed,proposal])
    with zipfile.ZipFile(paths[4]) as z:data={n:json.loads(z.read(n)) for n in z.namelist()}
    c,L,U,v,*_=strip_data(sc,prior,a,reg,upper,data);assert len(audit_pairs(p,mc,prior,c,L,U,v,data))==2
    mutations=[
        ('unconditional_strip_claim','strip',['family_scope'],'all_observations_in_Q'),
        ('externally_narrowed_root_contract','strip',['original_observation_contract_preserved'],False),
        ('overstated_formalization','strip',['entire_bridge_Lean_formalized'],True),
        ('necessary_bound_uses_source_upper','strip',['necessary_A_critical_lower'],str(F(sc['source_A_critical_interval'][1])-(U-F('1e-8')))),
        ('necessary_bound_uses_source_lower','strip',['necessary_B_critical_upper'],str(F(sc['source_B_critical_interval'][0])+(U-F('1e-8')))),
        ('common_report_factor_two_omitted','strip',['critical_difference_cap'],str(F(sc['critical_difference_cap'])/2)),
        ('bootstrap_cap_replaced','strip',['bootstrap_feature_budget_cap'],'1e-12'),
        ('wrong_old_secant_constant','strip',['inherited_uniform_critical_inverse_bound'],'1'),
        ('A_interval_upper_understated','strip',['conditional_A_critical_interval',1],sc['conditional_A_critical_interval'][0]),
        ('B_interval_lower_overstated','strip',['conditional_B_critical_interval',0],sc['conditional_B_critical_interval'][1]),
        ('incorrect_column_curve_lower','strip',['critical_column_curve_interval',0],'0'),
        ('wrong_critical_endpoint','strip',['face_reference_coordinates',1],sc['critical_column_curve_interval'][0]),
        ('coordinate12_replaced_before_face','strip',['first_replacement_order'],list(range(21))),
        ('wrong_final_endpoint','strip',['last_replacement_direction'],1),
        ('nonnegative_face_quotient','strip',['checks',0,'face_direction_12'],{'mid':[1,0],'rad':[0,0]}),
        ('singular_face_determinant','strip',['checks',0,'face_reference_determinant'],{'mid':[0,0],'rad':[1,0]}),
        ('undersized_inverse_bound','strip',['conditional_secant_inverse_bound'],'54'),
        ('unsupported_lower_budget','strip',['uniform_identification_strictly_below'],'2e-10'),
        ('dropped_non_circularity_check','strip',['new_lower_is_below_bootstrap_cap'],False),
        ('changed_feature_units','mixed',['contract','additional_feature_errors'],'relative'),
        ('post_noise_selection','mixed',['contract','source_selection'],'after_coordinate_noise'),
        ('missing_mixed_pair','mixed',['certified_pair_count'],1),
        ('critical_safety_increment_changed','mixed',['critical_epsilon'],'1e-8'),
        ('mixed_root_count_changed','mixed',['cases',0,'root_variable_count'],22),
        ('noise_index_moved','mixed',['cases',0,'noise_variable_index'],1),
        ('free_side_flipped','mixed',['cases',0,'root_variable_sides',0],'A' if mc['cases'][0]['root_variable_sides'][0]=='B' else 'B'),
        ('root_Jacobian_sign_flipped','mixed',['cases',0,'root_jacobian_column_signs',0],-mc['cases'][0]['root_jacobian_column_signs'][0]),
        ('unscaled_alpha','mixed',['cases',0,'noise_variable_definition'],'alpha=tau'),
        ('wrong_noise_scale','mixed',['cases',0,'tau_scale'],'1'),
        ('wrong_noise_column','mixed',['cases',0,'noise_jacobian_column',0],'0'),
        ('incorrect_variable_radius','mixed',['cases',0,'variable_radius'],'1e-80'),
        ('fixed_critical_box_varied','mixed',['cases',0,'A_observation_boxes',1,0],str(F(mc['cases'][0]['A_observation_boxes'][1][0])-F('1e-120'))),
        ('transferred_root_box','mixed',['cases',0,'B_observation_boxes',0,0],'0'),
        ('inflated_cube_margin','mixed',['cases',0,'minimum_cube_margin'],'1'),
        ('undersized_upper_endpoint','mixed',['cases',0,'tau_interval',1],'1e-12'),
        ('common_midpoint_replaced','mixed',['cases',0,'common_release'],'Phi(c)'),
        ('feature_error_erased','mixed',['cases',0,'component_error_at_exact_solution'],'0'),
        ('unproved_best_upper','mixed',['best_certified_tau_upper'],'1e-12'),
        ('numerical_rejection_relabelled','proposal',['cases',0,'status'],'rejected_numerical_trial'),
        ('boolean_coordinate_index','proposal',['cases',0,'free_indices',0],False),
        ('uncertified_root_side','proposal',['cases',0,'free_coordinate_sides',0],'C'),
        ('missing_source_entry','data',['E1_224.json','positive_root_intervals'],data['E1_224.json']['positive_root_intervals'][:-1]),
        ('changed_source_cutoff','data',['E2_160.json','top'],'20'),
        ('source_margin_inflated','mixed',['cases',0,'coordinate_audit',0,'error_margin'],'1'),
        ('false_contraction','mixed',['cases',0,'direct_checks',0,'rows',0,'derivative_defect'],{'mid':[2,0],'rad':[0,0]}),
        ('false_midpoint_enclosure','mixed',['cases',0,'direct_checks',0,'common_midpoint_enclosures',0],{'mid':[100,0],'rad':[0,0]}),
    ]
    results=[]
    for name,target,path,value in mutations:
        payload=copy.deepcopy({'strip':sc,'mixed':mc,'proposal':p,'data':data});put(payload[target],path,value)
        try:
            cc,ll,uu,vv,*_=strip_data(payload['strip'],prior,a,reg,upper,payload['data'])
            audit_pairs(payload['proposal'],payload['mixed'],prior,cc,ll,uu,vv,payload['data'])
        except (AssertionError,ValueError,KeyError,TypeError,IndexError,StopIteration,ZeroDivisionError) as e:results.append({'mutation':name,'rejected':True,'exception':type(e).__name__})
        else:raise AssertionError('accepted invalid mutation '+name)
    lo,hi,r,observed=map(F,[0,2,1,-1]);assert lo-r<=observed<=hi+r and abs(observed-lo)<=r and abs(observed-hi)>r
    a,b,cap=F(2),F(0),F(3);A,B=F(3),F(0);assert A>=a and B<=b and A-B<=cap and A<=b+cap and B>=a-cap
    assert not (F(2)<=F(1)) and F(2)<F(3) # A feasible budget above a cap is not excluded by below-cap evidence.
    x,h,fixed=F(3),F(1,10),F(4);oldA=x*x-fixed;newA=(x+h)**2-fixed;oldB=fixed-x*x;newB=fixed-(x+h)**2
    assert newA-oldA==2*x*h+h*h and newB-oldB==-(2*x*h+h*h)
    scale,alpha,rho=F(1,10),F(2),F(1,100);assert scale*(alpha+rho)-scale*(alpha-rho)==2*scale*rho
    controls=[{'name':'necessary_outer_interval_is_not_uniform_source_sufficiency','source_interval':['0','2'],'radius':'1','observation':'-1','error_at_low_root':'1','error_at_high_root':'3'},
        {'name':'source_strip_endpoint_direction','a':'2','b':'0','difference_cap':'3','admissible_A':'3','admissible_B':'0','A_upper':'3','B_lower':'-1'},
        {'name':'below_cap_exclusion_does_not_cover_larger_claim','budget_cap':'1','unsupported_lower':'3','possible_ambiguity_budget':'2'},
        {'name':'free_B_kernel_has_opposite_derivative','kernel':'x^2','x':str(x),'step':str(h),'A_residual_increment':str(newA-oldA),'B_residual_increment':str(newB-oldB)},
        {'name':'scaled_noise_interval_width','scale':str(scale),'alpha':str(alpha),'variable_radius':str(rho),'tau_width':str(2*scale*rho)}]
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in paths+[strip,mixed,proposal]},'mutations_rejected':len(results),'mutations':results,'exact_controls':controls,
        'scope':'Forty-six mutations and five exact controls check conditional strip scope, necessary versus sufficient source endpoints, mixed A/B assignment and derivative signs, variable/error scales and numerical proof premises. This is not an exhaustive audit or proof of the sharp source-feasible threshold.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['strip','mixed','proposal','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.strip,a.mixed,a.proposal);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'mutations_rejected':r['mutations_rejected'],'exact_controls':len(r['exact_controls'])}))
