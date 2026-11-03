"""Certify variable-noise feature pairs with a freely moving common midpoint."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,arb_mat,ctx
from dedekind_augmented_feature_proposal import FEATURES
from dedekind_augmented_feature_certificate_v2 import kernel
from dedekind_feature_certificate import coordinate_audit

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def av(x):
    q=F(x);return arb(q.numerator)/arb(q.denominator)
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def parameters(case,c,v,epsilon):
    free=case['free_A_indices'];assert free==[i for i in range(22) if i!=1] and all(type(x) is int for x in free)
    assert case['numerically_converged'] is True and len(case['A_coordinate_corrections'])==21 and case['feature_difference_direction']==v
    A=list(c);A[1]=F(case['fixed_A_critical_coordinate']);B=list(map(F,case['fixed_B_coordinates']));assert len(B)==22 and A[1]==c[1]+epsilon and B[1]==c[1]-epsilon
    for i,x in zip(free,case['A_coordinate_corrections']):A[i]+=F(x)
    alpha=F(case['scaled_tau']);scale=F(case['tau_scale']);rho=F('1e-120');assert scale==F('1e-10') and alpha>rho
    R=[list(map(F,row)) for row in case['preconditioner']];assert len(R)==22 and all(len(row)==22 for row in R)
    boxes=[(x-rho,x+rho) if i in free else (x,x) for i,x in enumerate(A)];tau=(scale*(alpha-rho),scale*(alpha+rho))
    distance=max(abs(x-z) for box,z in zip(boxes,c) for x in box);b_distance=max(abs(x-z) for x,z in zip(B,c));assert max(distance,b_distance)<F(1,100)
    assert boxes[0][0]>0 and B[0]>0 and all(x[1]<y[0] for x,y in zip(boxes,boxes[1:])) and all(x<y for x,y in zip(B,B[1:]))
    return A,B,free,alpha,scale,rho,R,boxes,tau,distance,b_distance
def contraction(A,B,c,free,alpha,scale,rho,R,v,bits):
    ctx.prec=bits;RR=arb_mat([[av(x) for x in row] for row in R]);det=RR.det();assert det>0 or det<0
    X=[av(A[i])+arb(0,av(rho).upper()) for i in free]
    J=arb_mat([[kernel(spec,x,True) for x in X]+[-2*av(scale)*v[k]] for k,spec in enumerate(FEATURES)])
    E=arb_mat([[int(i==j) for j in range(22)] for i in range(22)])-RR*J
    Bfeatures=[sum((kernel(spec,av(x)) for x in B),arb(0)) for spec in FEATURES]
    f=arb_mat([[sum((kernel(spec,av(x)) for x in A),arb(0))-Bfeatures[k]-2*av(scale)*av(alpha)*v[k]] for k,spec in enumerate(FEATURES)]);rf=RR*f;rows=[]
    for i in range(22):
        q=sum((abs(E[i,j]) for j in range(22)),arb(0));budget=abs(rf[i,0])+av(rho)*q;assert q<1 and budget<av(rho)
        rows.append({'index':i,'derivative_defect':enc(q),'preconditioned_residual':enc(rf[i,0]),'self_map_bound':enc(budget),'strict_margin':enc(av(rho)-budget)})
    observed=[av(x)+(arb(0,av(rho).upper()) if i in free else arb(0)) for i,x in enumerate(A)]
    midpoint=[(sum((kernel(spec,x) for x in observed),arb(0))+Bfeatures[k])/2 for k,spec in enumerate(FEATURES)]
    difference=[midpoint[k]-sum((kernel(spec,av(x)) for x in c),arb(0)) for k,spec in enumerate(FEATURES)]
    assert difference[0]>0 or difference[0]<0
    return {'precision_bits':bits,'determinant':enc(det),'F_at_rational_center':[enc(f[i,0]) for i in range(22)],'rows':rows,
        'common_midpoint_feature_enclosures':[enc(x) for x in midpoint],'midpoint_minus_Phi_c_enclosures':[enc(x) for x in difference],
        'midpoint_component_0_differs_from_Phi_c':True,'midpoint_component_0_difference_display':float(difference[0].mid())}
def run(boundary,shifted,anchor,source,inputs,region):
    p,q,a,s,reg=[json.loads(x.read_text()) for x in [boundary,shifted,anchor,source,region]];assert s['status']==reg['status']=='passed'
    m=next(x for x in s['matching_cases'] if x['precision_bits']==224);c=list(map(F,m['common_observation']));L,U=map(F,[m['radius_lower'],m['radius_upper']]);r=U-F('1e-8');epsilon=F('1e-8')+F('1e-16')
    assert len(c)==22 and list(map(F,a['common_rational_coordinates']))==c and a['full_rank_proposal']['features']==FEATURES
    assert F(a['source_threshold_lower'])==L and F(a['source_threshold_upper'])==U and U-L==F('2e-30') and r<L
    v=[1 if F(x)>0 else -1 if F(x)<0 else 0 for x in a['full_rank_proposal']['preconditioner'][1]];assert len(v)==22 and all(abs(x)==1 for x in v)
    assert len(p['cases'])==3 and len(q['cases'])==1 and q['inputs_sha256'][boundary.name]==sha(boundary)
    for d in [p,q]:
        assert F(d['critical_epsilon'])==epsilon and F(d['root_coordinate_error_radius'])==r and d['mpmath_dps']==220 and d['export_significant_digits']==170
        for path in [source,inputs]:assert d['inputs_sha256'][path.name]==sha(path)
    local=next(x for x in reg['regions'] if F(x['radius'])==F(1,100));guarantee=F(local['uniform_feature_error_identification_guarantee_strictly_below']);assert local['status']=='passed' and F(local['root_coordinate_error_radius'])==r
    cases=[]
    for proposed in p['cases']+q['cases']:
        A,B,free,alpha,scale,rho,R,boxes,tau,dist,bdist=parameters(proposed,c,v,epsilon)
        coordinates=coordinate_audit({'radius':r,'boxes_A':boxes,'boxes_B':[(x,x) for x in B]},s,inputs);assert all(x['within_radius'] for x in coordinates)
        checks=[contraction(A,B,c,free,alpha,scale,rho,R,v,bits) for bits in [768,1024]]
        cases.append({'status':'actual_source_variable_noise_pair','case_id':proposed['B_correction_scale'],'variable_dimension':22,'root_variable_indices':free,'root_variable_count':21,'noise_variable_index':21,
            'noise_variable_definition':'alpha=tau/scale','tau_scale':str(scale),'noise_jacobian_column':[str(-2*scale*x) for x in v],'noise_column_derivative_variation':'0',
            'variable_center':[str(F(x)) for x in proposed['A_coordinate_corrections']]+[str(alpha)],'variable_box_radius':str(rho),
            'fixed_A_critical_coordinate':str(A[1]),'A_observation_boxes':[list(map(str,x)) for x in boxes],'fixed_B_coordinates':list(map(str,B)),
            'tau_interval':list(map(str,tau)),'tau_upper_display':float(tau[1]),'minimum_cube_margin':str(F(1,100)-max(dist,bdist)),
            'exact_critical_root_gap':str(A[1]-B[1]),'coordinate_audit':coordinates,'direct_checks':checks,'signed_difference_coefficients':[2*x for x in v],
            'common_release':'(Phi(A)+Phi(B))/2','feature_error_for_exact_pair':'tau','budget_guaranteed_for_pair':str(tau[1]),
            'midpoint_is_Phi_c':False,'interpretation':'A strict contraction yields an exact A/alpha solution with rational fixed B. Its positive tau is enclosed, and the free feature midpoint has component errors exactly tau. This bounds a restricted ambiguity threshold, without global optimality.'})
    best=min(F(x['tau_interval'][1]) for x in cases);budget=F('1.832e-10');assert guarantee<best<budget<F('2e-10')
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in [boundary,shifted,anchor,source,inputs,region]},
        'contract':{'source_cutoff':'39/2','source_population':22,'source_selection':'complete_positive_prefix_before_coordinate_errors','root_entries_and_multiplicity':'preserved','root_coordinate_error_radius':str(r),
            'observed_root_region_radius':'1/100','region_geometry':'standard_coordinate_cube_centered_at_c','features':FEATURES,'additional_feature_errors':'independent_absolute_component_bounds',
            'raw_roots_or_counts_released':False,'unknown_tails_included':False,'common_release_type':'free_feature_midpoint'},
        'common_root_center':list(map(str,c)),'critical_epsilon':str(epsilon),'feature_direction':v,'cases':cases,'certified_pair_count':4,
        'uniform_identification_below':str(guarantee),'best_certified_tau_upper':str(best),'convenient_feature_budget':str(budget),'upper_to_guarantee_ratio':str(best/guarantee),
        'convenient_budget_to_guarantee_ratio':str(budget/guarantee),'ratio_display':float(best/guarantee),'earlier_upper_bound':'1/5000000000',
        'scope':'Four source-feasible noisy pairs in the same radius-0.01 region and fixed root-error contract improve the ambiguity upper bound. The uniform lower bound is inherited and independently checked. A moving feature midpoint avoids the prior fixed-report restriction. Optimal thresholds, arbitrary-data decoding and global recovery remain open.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['boundary','shifted','anchor','source','inputs','region','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a.boundary,a.shifted,a.anchor,a.source,a.inputs,a.region);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'pairs':r['certified_pair_count'],'tau_upper':float(F(r['best_certified_tau_upper'])),'ratio':r['ratio_display']}))
