"""Independently audit variable-tau equations, source boxes and free midpoint releases."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_augmented_feature_audit import jets,modular_det,input_geometry
from dedekind_aggregate_integer_audit import arithmetic_vectors

SPECS=[{'kind':'gaussian','center':n,'a':'1/25'} for n in [2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31]]+[
    {'kind':'rational_moment','numerator':3,'offset':'9/4'},{'kind':'gaussian','center':37,'a':'1/25'},
    {'kind':'gaussian','center':2,'a':'1/24'},{'kind':'gaussian','center':41,'a':'1/25'},{'kind':'gaussian','center':43,'a':'1/25'}]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def av(x):
    q=F(x);return arb(q.numerator)/arb(q.denominator)
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def ball(x):
    assert set(x)=={'mid','rad'} and all(len(x[k])==2 and all(type(a) is int for a in x[k]) for k in x) and x['rad'][0]>=0
    return arb(arb(tuple(x['mid'])),arb(tuple(x['rad'])))
def independent_root(A,B,c,free,R,alpha,scale,rho,v,bits):
    ctx.prec=bits;F0=[];J0=[];M=[];midpoints=[];differences=[]
    for k,spec in enumerate(SPECS):
        fA=sum((jets(spec,av(x))[0] for x in A),arb(0));fB=sum((jets(spec,av(x))[0] for x in B),arb(0))
        F0.append(fA-fB-2*av(scale)*av(alpha)*v[k]);J0.append([jets(spec,av(A[i]))[1] for i in free]+[-2*av(scale)*v[k]])
        M.append([abs(jets(spec,av(A[i])+arb(0,av(rho).upper()))[2]) for i in free]+[arb(0)])
        intervalA=sum((jets(spec,av(x)+(arb(0,av(rho).upper()) if i in free else arb(0)))[0] for i,x in enumerate(A)),arb(0))
        midpoints.append((intervalA+fB)/2);differences.append(midpoints[-1]-sum((jets(spec,av(x))[0] for x in c),arb(0)))
    rows=[]
    for i in range(22):
        residual=sum((av(R[i][k])*F0[k] for k in range(22)),arb(0))
        center=sum((abs(arb(int(i==j))-sum((av(R[i][k])*J0[k][j] for k in range(22)),arb(0))) for j in range(22)),arb(0))
        variation=av(rho)*sum((abs(av(R[i][k]))*sum(M[k],arb(0)) for k in range(22)),arb(0));q=center+variation;budget=abs(residual)+av(rho)*q
        assert q<1 and budget<av(rho)
        rows.append({'index':i,'complex_residual':enc(residual),'center_inverse_defect':enc(center),'second_derivative_variation':enc(variation),'contraction_bound':enc(q),'self_map_bound':enc(budget)})
    assert differences[0]>0 or differences[0]<0
    return {'precision_bits':bits,'rows':rows,'F_at_rational_center':[enc(x) for x in F0],'common_midpoint_enclosures':[enc(x) for x in midpoints],
        'midpoint_minus_Phi_c_enclosures':[enc(x) for x in differences],'midpoint_component_0_difference_display':float(differences[0].mid())}
def audit_data(boundary,shifted,certificate,anchor,region,inputs):
    c,L,U=input_geometry(inputs);r=U-F('1e-8');epsilon=F('1e-8')+F('1e-16');assert r<L and U-L==F('2e-30')
    assert certificate['status']=='passed' and region['status']=='passed' and anchor['full_rank_proposal']['features']==SPECS
    assert list(map(F,anchor['common_rational_coordinates']))==list(map(F,certificate['common_root_center']))==c
    assert F(anchor['source_threshold_lower'])==L and F(anchor['source_threshold_upper'])==U and F(certificate['critical_epsilon'])==epsilon
    for p in [boundary,shifted]:assert F(p['root_coordinate_error_radius'])==r and F(p['critical_epsilon'])==epsilon and p['mpmath_dps']==220 and p['export_significant_digits']==170
    expected={'source_cutoff':'39/2','source_population':22,'source_selection':'complete_positive_prefix_before_coordinate_errors','root_entries_and_multiplicity':'preserved','root_coordinate_error_radius':str(r),
        'observed_root_region_radius':'1/100','region_geometry':'standard_coordinate_cube_centered_at_c','features':SPECS,'additional_feature_errors':'independent_absolute_component_bounds',
        'raw_roots_or_counts_released':False,'unknown_tails_included':False,'common_release_type':'free_feature_midpoint'}
    assert certificate['contract']==expected
    v=[1 if F(x)>0 else -1 if F(x)<0 else 0 for x in anchor['full_rank_proposal']['preconditioner'][1]]
    assert len(v)==22 and all(type(x) is int and abs(x)==1 for x in v) and certificate['feature_direction']==v
    local=next(x for x in region['regions'] if F(x['radius'])==F(1,100));h=F(local['critical_inverse_bound']);assert h>0 and F(local['root_coordinate_error_radius'])==r
    guarantee=(L-r)/h;assert F(local['uniform_feature_error_identification_guarantee_strictly_below'])==F(certificate['uniform_identification_below'])==guarantee
    assert len(boundary['cases'])==3 and len(shifted['cases'])==1 and len(certificate['cases'])==certificate['certified_pair_count']==4
    proposed=boundary['cases']+shifted['cases'];assert [x['B_correction_scale'] for x in proposed]==['1/2','1','3/2','optimized_common_shift_from_3/2'];results=[];uppers=[]
    for p,record in zip(proposed,certificate['cases']):
        free=p['free_A_indices'];assert free==record['root_variable_indices']==[i for i in range(22) if i!=1] and all(type(x) is int for x in free)
        assert p['numerically_converged'] is True and len(p['A_coordinate_corrections'])==21 and p['feature_difference_direction']==v
        assert record['case_id']==p['B_correction_scale'] and record['status']=='actual_source_variable_noise_pair' and record['variable_dimension']==22 and record['root_variable_count']==21 and record['noise_variable_index']==21
        assert record['noise_variable_definition']=='alpha=tau/scale' and record['noise_column_derivative_variation']=='0'
        A=list(c);A[1]=F(p['fixed_A_critical_coordinate']);B=list(map(F,p['fixed_B_coordinates']));assert len(B)==22 and A[1]==c[1]+epsilon and B[1]==c[1]-epsilon
        for i,w in zip(free,p['A_coordinate_corrections']):A[i]+=F(w)
        scale=F(p['tau_scale']);alpha=F(p['scaled_tau']);rho=F(record['variable_box_radius']);assert scale==F(record['tau_scale'])==F('1e-10') and rho==F('1e-120') and alpha>rho
        assert record['variable_center']==[str(F(x)) for x in p['A_coordinate_corrections']]+[str(alpha)] and record['noise_jacobian_column']==[str(-2*scale*x) for x in v]
        R=[list(map(F,row)) for row in p['preconditioner']];assert len(R)==22 and all(len(row)==22 for row in R);determinant=modular_det(R)
        boxes=[(x-rho,x+rho) if i in free else (x,x) for i,x in enumerate(A)];assert record['A_observation_boxes']==[list(map(str,x)) for x in boxes] and record['fixed_B_coordinates']==list(map(str,B)) and F(record['fixed_A_critical_coordinate'])==A[1]
        assert boxes[0][0]>0 and B[0]>0 and all(x[1]<y[0] for x,y in zip(boxes,boxes[1:])) and all(x<y for x,y in zip(B,B[1:]))
        max_distance=max([abs(x-z) for box,z in zip(boxes,c) for x in box]+[abs(x-z) for x,z in zip(B,c)])
        assert F(record['minimum_cube_margin'])==F(1,100)-max_distance>0 and F(record['exact_critical_root_gap'])==A[1]-B[1]==2*epsilon>2*(L-r)
        tau=(scale*(alpha-rho),scale*(alpha+rho));assert record['tau_interval']==list(map(str,tau)) and 0<tau[0]<tau[1] and F(record['budget_guaranteed_for_pair'])==tau[1]
        assert record['common_release']=='(Phi(A)+Phi(B))/2' and record['feature_error_for_exact_pair']=='tau' and record['midpoint_is_Phi_c'] is False and record['signed_difference_coefficients']==[2*x for x in v]
        independent=[independent_root(A,B,c,free,R,alpha,scale,rho,v,bits) for bits in [896,1152]]
        assert [x['precision_bits'] for x in record['direct_checks']]==[768,1024]
        for check in record['direct_checks']:
            assert len(check['rows'])==len(check['F_at_rational_center'])==len(check['common_midpoint_feature_enclosures'])==len(check['midpoint_minus_Phi_c_enclosures'])==22
            det=ball(check['determinant']);assert det>0 or det<0
            for i,row in enumerate(check['rows']):
                assert row['index']==i and ball(row['derivative_defect'])<1 and ball(row['self_map_bound'])<av(rho) and ball(row['strict_margin'])>0
                assert all(ball(check['F_at_rational_center'][i]).overlaps(ball(a['F_at_rational_center'][i])) for a in independent)
                assert all(ball(check['common_midpoint_feature_enclosures'][i]).overlaps(ball(a['common_midpoint_enclosures'][i])) for a in independent)
                assert all(ball(check['midpoint_minus_Phi_c_enclosures'][i]).overlaps(ball(a['midpoint_minus_Phi_c_enclosures'][i])) for a in independent)
            d=ball(check['midpoint_minus_Phi_c_enclosures'][0]);assert check['midpoint_component_0_differs_from_Phi_c'] is True and (d>0 or d<0)
        constraints=[];stored={(x['input_member'],x['source_index']):x for x in record['coordinate_audit']};assert len(stored)==len(record['coordinate_audit'])==88
        for bits in [160,224]:
            for number,observed in [(1,boxes),(2,[(x,x) for x in B])]:
                name=f'E{number}_{bits}.json'
                for i,(lo,hi) in enumerate(observed):
                    slo,shi=[F(inputs[name]['positive_root_intervals'][i][k]) for k in ['lo','hi']];left=lo-(shi-r);right=(slo+r)-hi;assert left>=0 and right>=0
                    entry=stored[(name,i)];assert entry['precision_bits']==bits and entry['within_radius'] is True and F(entry['error_margin'])==min(left,right)
                    assert entry['source_interval']==[str(slo),str(shi)] and entry['observed_interval']==[str(lo),str(hi)] and F(entry['maximum_uniform_error'])==r-min(left,right)
                    constraints.append({'input_member':name,'index':i,'left_inclusion_margin':str(left),'right_inclusion_margin':str(right)})
        uppers.append(tau[1]);results.append({'case_id':record['case_id'],'modular_preconditioner':determinant,'independent_complex_checks':independent,'source_constraints':constraints,'scalar_inequalities':176,
            'minimum_cube_margin':record['minimum_cube_margin'],'tau_interval':list(map(str,tau)),'free_midpoint_certifiably_differs_from_Phi_c':True})
    best=min(uppers);budget=F(certificate['convenient_feature_budget']);assert guarantee<best<budget==F('1.832e-10')<F(certificate['earlier_upper_bound'])==F('2e-10')
    assert F(certificate['best_certified_tau_upper'])==best and F(certificate['upper_to_guarantee_ratio'])==best/guarantee and F(certificate['convenient_budget_to_guarantee_ratio'])==budget/guarantee
    return {'status':'passed','cases':results,'certified_pair_count':4,'scalar_coordinate_inequalities':704,'uniform_identification_below':str(guarantee),'best_certified_tau_upper':str(best),'convenient_feature_budget':str(budget),
        'upper_to_guarantee_ratio':str(best/guarantee),'scope':'Independent complex second derivatives, exact constant noise-column arithmetic, modular inverses and direct source inequalities certify all four variable-noise pairs. The common midpoint moves away from Phi(c); the prior fixed-target exclusions do not establish global impossibility. The lower guarantee remains conditional on the inherited class and region.'}
def run(boundary,shifted,certificate,anchor,region,region_audit,inputs,classification,arithmetic,source):
    paths=[boundary,shifted,certificate,anchor,region,region_audit,inputs,classification,arithmetic,source]
    p,q,cert,a,reg,ra,cl,src=[json.loads(x.read_text()) for x in [boundary,shifted,certificate,anchor,region,region_audit,classification,source]]
    assert cert['inputs_sha256']=={x.name:sha(x) for x in [boundary,shifted,anchor,source,inputs,region]} and q['inputs_sha256'][boundary.name]==sha(boundary)
    assert ra['status']=='passed' and ra['inputs_sha256'][region.name]==sha(region) and all(x['independent_critical_bound_no_larger_than_claimed'] for x in ra['regions'])
    assert cl['status']==src['status']=='passed' and cl['complete_quartic_candidate_count']==2
    with zipfile.ZipFile(inputs) as z:data={name:json.loads(z.read(name)) for name in z.namelist()}
    result=audit_data(p,q,cert,a,reg,data);vectors,factors=arithmetic_vectors(arithmetic,src['columns']);ar=json.loads(arithmetic.read_text())
    labels={m['class_id']:next(k for k,v in ar['fields'].items() if sorted(v['quadratic_discriminants'])==m['quadratic_discriminants']) for m in cl['retained_models']}
    assert set(labels.values())=={'A','B'} and all(src['predictions'][k]==vectors[v] for k,v in labels.items())
    domains=[sorted({v[j] for v in vectors.values()}) for j in range(604)];assert len(factors)==1128 and sum(len(x)==1 for x in domains)==456
    result.update(source_sha256=sha(Path(__file__)),inputs_sha256={x.name:sha(x) for x in paths},class_mapping=labels,polynomial_factorizations=factors,factorization_count=1128,coefficient_comparisons=1208,columns=src['columns'],common_release_coefficient_domains=domains,fixed_coefficients=456,ambiguous_coefficients=148)
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['boundary','shifted','certificate','anchor','region','region-audit','inputs','classification','arithmetic','source','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a.boundary,a.shifted,a.certificate,a.anchor,a.region,a.region_audit,a.inputs,a.classification,a.arithmetic,a.source);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'pairs':r['certified_pair_count'],'scalar_inequalities':r['scalar_coordinate_inequalities'],'factorizations':r['factorization_count']}))
