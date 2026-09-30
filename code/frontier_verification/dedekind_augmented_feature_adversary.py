"""Challenge augmented-feature certificates and their observation/scope boundaries."""
import argparse,copy,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from dedekind_augmented_feature_audit import audit_pair,ball,av

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(proposal,certificate,inputs,noise):
    p=json.loads(proposal.read_text());c=json.loads(certificate.read_text());n=json.loads(noise.read_text())
    with zipfile.ZipFile(inputs) as z:d={name:json.loads(z.read(name)) for name in z.namelist()}
    assert audit_pair(p,c,d)['status']=='passed';mutations=[]
    def attempt(name,change):
        pp,cc,dd=copy.deepcopy((p,c,d));change(pp,cc,dd)
        try:audit_pair(pp,cc,dd)
        except (AssertionError,ValueError,TypeError,IndexError,KeyError,StopIteration,ZeroDivisionError) as e:
            mutations.append({'name':name,'status':'rejected','exception':type(e).__name__});return
        raise AssertionError('Mutation accepted: '+name)
    attempt('missing joint moment',lambda p,c,d:p['cases'][0]['features'].pop())
    attempt('wrong moment offset',lambda p,c,d:p['cases'][0]['features'][17].update(offset='1'))
    attempt('wrong moment numerator',lambda p,c,d:p['cases'][0]['features'][17].update(numerator=6))
    attempt('wrong Gaussian width',lambda p,c,d:p['cases'][2]['features'][-1].update(a='1/25'))
    attempt('wrong center 41',lambda p,c,d:p['cases'][3]['features'][-1].update(center=43))
    attempt('missing collision dimension',lambda p,c,d:p['cases'].pop())
    attempt('wrong reported dimension',lambda p,c,d:c['collisions'][0].update(dimension=17))
    attempt('critical variable adjusted',lambda p,c,d:p['cases'][0]['selected_A_variable_indices'].__setitem__(0,1))
    attempt('duplicate variables',lambda p,c,d:p['cases'][0]['selected_A_variable_indices'].__setitem__(0,p['cases'][0]['selected_A_variable_indices'][1]))
    attempt('zero split',lambda p,c,d:p['cases'][0].update(critical_split_epsilon='0'))
    attempt('stale radius',lambda p,c,d:p.update(radius=p['source_threshold_upper']))
    attempt('false strict threshold improvement',lambda p,c,d:c['collisions'][0].update(strict_improvement_below_L='1'))
    attempt('changed common coordinate',lambda p,c,d:p['common_rational_coordinates'].__setitem__(0,'1'))
    attempt('missing correction',lambda p,c,d:p['cases'][0]['corrections'].pop())
    attempt('off-root correction',lambda p,c,d:p['cases'][0]['corrections'].__setitem__(0,'1'))
    attempt('inconsistent A interval',lambda p,c,d:c['collisions'][0]['A_observed_coordinate_boxes'][0].__setitem__(0,'0'))
    attempt('changed fixed B',lambda p,c,d:c['collisions'][0]['B_fixed_observed_coordinates'].__setitem__(1,'0'))
    attempt('oversized correction box',lambda p,c,d:c['collisions'][0].update(correction_box_radius='1'))
    attempt('truncated coordinate witness',lambda p,c,d:c['collisions'][0]['coordinate_audit'].pop())
    attempt('inflated coordinate margin',lambda p,c,d:c['collisions'][0]['coordinate_audit'][0].update(error_margin='1'))
    attempt('singular slice preconditioner',lambda p,c,d:p['cases'][0]['preconditioner'].__setitem__(0,['0']*18))
    attempt('identity slice preconditioner',lambda p,c,d:p['cases'][0].update(preconditioner=[[str(int(i==j)) for j in range(18)] for i in range(18)]))
    attempt('claimed noncontraction',lambda p,c,d:c['collisions'][0]['contraction_checks'][0]['rows'][0].update(derivative_defect_row_sum={'mid':[1,0],'rad':[0,0]}))
    attempt('negative self-map margin',lambda p,c,d:c['collisions'][0]['contraction_checks'][0]['rows'][0].update(strict_margin={'mid':[-1,0],'rad':[0,0]}))
    attempt('missing feature enclosure',lambda p,c,d:c['collisions'][0]['contraction_checks'][0]['F_center'].pop())
    attempt('false feature residual',lambda p,c,d:c['collisions'][0]['contraction_checks'][0]['F_center'].__setitem__(0,{'mid':[1,0],'rad':[0,0]}))
    attempt('raw coordinates released',lambda p,c,d:c['collisions'][0]['contract'].update(released_raw_coordinates=True))
    attempt('count profile released',lambda p,c,d:c['collisions'][0]['contract'].update(released_cumulative_counts=True))
    attempt('unknown tail included',lambda p,c,d:c['collisions'][0]['contract'].update(included_unknown_tail=True))
    attempt('post-noise censoring',lambda p,c,d:c['collisions'][0]['contract'].update(post_noise_window_censoring=True))
    attempt('source loses multiplicity',lambda p,c,d:d['E1_224.json']['positive_root_intervals'].pop())
    attempt('field identity leaked into input',lambda p,c,d:d['E1_224.json'].update(field='A'))
    attempt('wrong source metadata',lambda p,c,d:d['E1_224.json'].update(discriminant=1))
    attempt('false interior count',lambda p,c,d:c['collisions'][0]['interior_counts'].update(B=1))
    attempt('false local membership',lambda p,c,d:c['collisions'][0].update(both_observations_inside_injective_22_feature_neighborhood=False))
    attempt('local region expanded without proof',lambda p,c,d:c['rank_and_local_injectivity'].update(certified_neighborhood_radius='1'))
    attempt('wrong local center',lambda p,c,d:c['rank_and_local_injectivity']['neighborhood_center'].__setitem__(0,'0'))
    attempt('understated inverse stability constant',lambda p,c,d:c['rank_and_local_injectivity'].update(inverse_Lipschitz_bound='1'))
    attempt('understated matrix norm',lambda p,c,d:c['rank_and_local_injectivity'].update(exact_preconditioner_infinity_norm='1'))
    attempt('false zero local defect',lambda p,c,d:c['rank_and_local_injectivity'].update(uniform_derivative_defect_bound='0'))
    attempt('singular full preconditioner',lambda p,c,d:p['full_rank_proposal']['preconditioner'].__setitem__(0,['0']*22))
    attempt('full features omit final center',lambda p,c,d:p['full_rank_proposal']['features'].pop())
    attempt('missing rank minor',lambda p,c,d:c['rank_and_local_injectivity']['rank_minor_checks'].pop())
    attempt('rank flag contradicts claim',lambda p,c,d:c['rank_and_local_injectivity']['rank_minor_checks'][0].update(square_minor_invertible=False))
    attempt('noncontracting rank defect',lambda p,c,d:c['rank_and_local_injectivity']['rank_minor_checks'][0]['defect_row_sums'].__setitem__(0,{'mid':[1,0],'rad':[0,0]}))
    zero_controls=[]
    for case in c['collisions']:
        for row in case['coordinate_audit']:
            if F(row['error_margin'])==0:
                computed=float(F(case['radius']))-max(abs(float(F(x))-float(F(y))) for x in row['source_interval'] for y in row['observed_interval'])
                zero_controls.append({'dimension':case['dimension'],'input':row['input_member'],'index':row['source_index'],'exact_margin':'0','binary64_margin':computed})
    assert len(zero_controls)==16
    # Explicit local square-map control: the derivative defect is <= 1/4 on [3/4,5/4], yet +/-1 collide globally.
    assert max(abs(1-x) for x in [F(3,4),F(5,4)])==F(1,4) and F(1)**2==F(-1)**2 and F(1)!=F(-1)
    assert n['status']=='passed' and F(n['feature_release_error_bound'])==F('5e-18') and F(n['final_feature_offset_from_B'])==F('-4.5e-18')
    for row in n['checks']:
        gap=ball(row['exact_feature_difference']);assert abs(gap)>av('2e-18')
        assert abs(ball(row['A_final_feature_error']))<av('5e-18') and abs(ball(row['B_final_feature_error']))<av('5e-18')
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in [proposal,certificate,inputs,noise]},
            'mutations_rejected':len(mutations),'mutations':mutations,'exact_zero_margin_controls':zero_controls,
            'local_to_global_counterexample':{'map':'x^2','region':['3/4','5/4'],'preconditioner':'1/2','derivative_defect_bound':'1/4','outside_region_collision':['-1','1']},
            'noise_boundary_control':{'tau_5e_minus_18_common_release':'certified','tau_1e_minus_18_common_release_for_this_witness':'excluded because its last-feature separation exceeds 2*tau',
                                       'scope':'This excludes the smaller error only for the constructed local witness, not all possible witnesses.'},
            'scope':'Actual independent-auditor rejection paths test source, feature, coordinate, contraction, rank and local-region semantics. Exact counterexamples separate local from global and exact from noisy observation contracts.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['proposal','certificate','inputs','noise','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a.proposal,a.certificate,a.inputs,a.noise);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'mutations_rejected':r['mutations_rejected'],'zero_margin_controls':len(r['exact_zero_margin_controls'])}))
