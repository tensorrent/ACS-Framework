"""Certify inverse feature observations, source feasibility, and explicit noisy releases."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,arb_mat,ctx
from dedekind_augmented_feature_certificate_v2 import kernel
from dedekind_augmented_feature_proposal import FEATURES
from dedekind_feature_certificate import coordinate_audit

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def av(x):
    q=F(x);return arb(q.numerator)/arb(q.denominator)
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def inverse_root(common,signs,tau,proposed,rho):
    assert proposed['field_sign'] in [1,-1] and proposed['numerically_converged'] is True
    assert len(proposed['corrections'])==22 and len(proposed['preconditioner'])==22 and all(len(x)==22 for x in proposed['preconditioner'])
    y=[x+F(v) for x,v in zip(common,proposed['corrections'])];boxes=[(x-rho,x+rho) for x in y]
    assert all(x[1]<z[0] for x,z in zip(boxes,boxes[1:]))
    matrix=[list(map(F,row)) for row in proposed['preconditioner']];checks=[]
    for bits in [768,1024]:
        ctx.prec=bits;R=arb_mat([[av(x) for x in row] for row in matrix]);det=R.det();assert det>0 or det<0
        X=[av(x)+arb(0,av(rho).upper()) for x in y]
        J=arb_mat([[kernel(spec,x,True) for x in X] for spec in FEATURES]);E=arb_mat([[int(i==j) for j in range(22)] for i in range(22)])-R*J
        common_features=[sum((kernel(spec,av(x)) for x in common),arb(0)) for spec in FEATURES]
        f=arb_mat([[sum((kernel(spec,av(x)) for x in y),arb(0))-common_features[i]-proposed['field_sign']*av(tau)*signs[i]] for i,spec in enumerate(FEATURES)])
        pre=R*f;rows=[]
        for i in range(22):
            q=sum((abs(E[i,j]) for j in range(22)),arb(0));budget=abs(pre[i,0])+av(rho)*q;assert q<1 and budget<av(rho)
            rows.append({'index':i,'derivative_defect_bound':enc(q),'preconditioned_residual':enc(pre[i,0]),'self_map_bound':enc(budget),'strict_margin':enc(av(rho)-budget)})
        checks.append({'precision_bits':bits,'determinant':enc(det),'rows':rows,'F_at_rational_center':[enc(f[i,0]) for i in range(22)],'common_exact_feature_enclosures':[enc(x) for x in common_features]})
    distance=max(abs(x-z) for box,z in zip(boxes,common) for x in box)
    return {'status':'exact_target_root_exists','field_sign':proposed['field_sign'],'observation_boxes':[list(map(str,x)) for x in boxes],
        'correction_box_radius':str(rho),'maximum_distance_from_common_center':str(distance),'inside_radius_0p01_cube':distance<=F(1,100),'contraction_checks':checks}
def run(proposal,anchor,source,inputs,region):
    p=json.loads(proposal.read_text());a=json.loads(anchor.read_text());s=json.loads(source.read_text());regions=json.loads(region.read_text())
    assert p['input_sha256']==sha(anchor) and regions['status']=='passed' and regions['inputs_sha256'][anchor.name]==sha(anchor)
    assert p['features']==FEATURES and a['full_rank_proposal']['features']==FEATURES and s['status']=='passed'
    m=next(x for x in s['matching_cases'] if x['precision_bits']==224);common=list(map(F,m['common_observation']));assert list(map(F,p['common_root_center']))==common==list(map(F,a['common_rational_coordinates']))
    r=F(p['root_coordinate_error_radius']);L=F(m['radius_lower']);U=F(m['radius_upper']);assert r==U-F('1e-8')<L and p['source_threshold_lower']==m['radius_lower'] and F(p['critical_required_shift'])==F('1e-8')
    signs=p['feature_direction'];assert len(signs)==22 and all(type(x) is int and abs(x)==1 for x in signs)
    assert signs==[1 if F(x)>0 else -1 if F(x)<0 else 0 for x in a['full_rank_proposal']['preconditioner'][1]]
    local=next(x for x in regions['regions'] if F(x['radius'])==F(1,100));assert local['status']=='passed' and F(local['root_coordinate_error_radius'])==r
    cases=[];rho=F('1e-120')
    for proposed in p['cases']:
        tau=F(proposed['feature_error_bound']);assert tau>0
        roots={field:inverse_root(common,signs,tau,proposed[field],rho) for field in ['A','B']}
        assert roots['A']['field_sign']==1 and roots['B']['field_sign']==-1 and all(x['inside_radius_0p01_cube'] for x in roots.values())
        par={'radius':r,'boxes_A':[tuple(map(F,x)) for x in roots['A']['observation_boxes']],'boxes_B':[tuple(map(F,x)) for x in roots['B']['observation_boxes']]}
        records=coordinate_audit(par,s,inputs);violations=[x for x in records if not x['within_radius']];exclusions=[]
        for x in violations:
            slo,shi=map(F,x['source_interval']);olo,ohi=map(F,x['observed_interval']);margin=max(slo-ohi,olo-shi,F(0))-r
            if margin>0:exclusions.append({'input_member':x['input_member'],'source_index':x['source_index'],'all_source_and_observation_points_violate_by_at_least':str(margin)})
        assert not violations or exclusions
        cases.append({'status':'actual_source_common_noisy_release' if not violations else 'signed_target_pair_excluded_in_local_cube','feature_error_bound':str(tau),
            'roots':roots,'coordinate_audit':records,'coordinate_violation_count':len(violations),'uniform_source_exclusions':exclusions,
            'common_release':'Phi(c), the exact 22-feature vector of the recorded rational center. The A feature error is -tau*v; the B feature error is +tau*v.',
            'exact_feature_difference_vector':[str(2*tau*v) for v in signs],'exact_feature_pair_infinity_distance':str(2*tau),
            'interpretation':'When source-feasible, tau is the sharp independent component-error threshold for this exact pair by midpoint sufficiency and the triangle inequality. A rejected signed target pair does not exclude other common releases, directions or observation pairs.'})
    accepted=[x for x in cases if x['status']=='actual_source_common_noisy_release'];assert accepted
    guarantee=F(local['uniform_feature_error_identification_guarantee_strictly_below']);upper=min(F(x['feature_error_bound']) for x in accepted);assert 0<guarantee<upper
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in [proposal,anchor,source,inputs,region]},
        'contract':{'source_cutoff':'39/2','source_population':22,'source_selection':'complete_positive_prefix_before_coordinate_errors','root_entries_and_multiplicity':'preserved',
            'root_coordinate_error_radius':str(r),'observed_root_region_radius':'1/100','region_geometry':'standard_coordinate_cube_centered_at_c','features':FEATURES,
            'additional_feature_errors':'independent_absolute_component_bounds','raw_roots_or_counts_released':False,'unknown_tails_included':False},
        'feature_direction':signs,'cases':cases,'exact_inverse_roots_certified':2*len(cases),'source_feasible_noisy_pairs':len(accepted),
        'excluded_signed_target_pairs':len(cases)-len(accepted),'uniform_identification_below':str(guarantee),'actual_ambiguity_at':str(upper),
        'upper_to_guarantee_ratio':str(upper/guarantee),'guarantee_display':float(guarantee),'ambiguity_display':float(upper),'ratio_display':float(upper/guarantee),
        'scope':'Two-sided bounds concern the complete inherited two-field class, fixed root error r=U-1e-8, the radius-0.01 observed-root cube, and the exact stated finite feature units. All errors and region restrictions are explicit. No exact optimal threshold, global identification outside the cube, physical precision model or unknown-tail equality is claimed.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['proposal','anchor','source','inputs','region','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a.proposal,a.anchor,a.source,a.inputs,a.region);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'cases':[{k:x[k] for k in ['status','feature_error_bound','coordinate_violation_count']} for x in r['cases']],
        'guaranteed_below':r['guarantee_display'],'ambiguity_at':r['ambiguity_display'],'ratio':r['ratio_display']}))
