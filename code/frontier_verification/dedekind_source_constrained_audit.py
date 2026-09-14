"""Independent source endpoints, real Cramer lower bounds and complex mixed systems."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from flint import arb,arb_mat,ctx
from dedekind_signed_corner_audit import validate_exact,real_functions,determinant_ratio,endpoints,interval_sign
from dedekind_augmented_feature_audit import SPECS,input_geometry,jets,modular_det
from dedekind_aggregate_integer_audit import arithmetic_vectors

ROOT=Path(__file__).absolute().parents[2]
PRIOR='docs/frontier/2026-09-14-aggregate-signed-corner-delta/Signed_Corner_Certificate.json'
ANCHOR='docs/frontier/2026-09-14-aggregate-augmented-feature-delta/Augmented_Proposals_Local.json'
REGION='docs/frontier/2026-09-14-aggregate-weighted-feature-delta/Weighted_Region_Certificate.json'
UPPER='docs/frontier/2026-09-14-aggregate-variable-noise-delta/Variable_Noise_Certificate.json'
SOURCE='docs/frontier/2026-09-14-aggregate-equal-population-delta'
CLASS='docs/frontier/2026-09-14-aggregate-classification-delta/Full_Quartic_Class.json'
ARITH='docs/frontier/2026-09-13-biquadratic-delta/Pair_Arithmetic.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def av(x):
    q=F(x);return arb(q.numerator)/arb(q.denominator)
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def overlaps(x,y):
    a,b=endpoints(x);c,d=endpoints(y);return max(a,c)<=min(b,d)

def strip_data(strip,prior,anchor,region,upper,data):
    c,R,v=validate_exact(prior,anchor,region,upper);cc,L,U=input_geometry(data);assert cc==c
    r=U-F('1e-8');gap=L-r;assert gap>0
    assert strip['status']=='passed' and strip['contract']==prior['contract'] and strip['common_root_center']==list(map(str,c)) and strip['critical_index']==1
    assert strip['family']=='product_of_closed_column_hulls_with_only_coordinate_1_interval_restricted'
    assert strip['family_scope']=='all_common_report_pairs_with_feature_budget_at_most_bootstrap_cap'
    assert strip['other_coordinate_radius']=='1/100' and strip['original_observation_contract_preserved'] is True and strip['entire_bridge_Lean_formalized'] is False
    assert F(strip['source_threshold_lower'])==L and F(strip['source_threshold_upper'])==U and F(strip['critical_source_gap_lower'])==2*gap
    aa=data['E1_224.json']['positive_root_intervals'][1];bb=data['E2_224.json']['positive_root_intervals'][1]
    assert strip['source_A_critical_interval']==[aa['lo'],aa['hi']] and strip['source_B_critical_interval']==[bb['lo'],bb['hi']]
    a=F(aa['lo'])-r;b=F(bb['hi'])+r;assert a-b==2*gap
    T=F(upper['best_certified_tau_upper']);Kold=F(prior['corner_uniform_inverse_bound']);D=2*T*Kold
    assert F(strip['necessary_A_critical_lower'])==a and F(strip['necessary_B_critical_upper'])==b
    assert F(strip['bootstrap_feature_budget_cap'])==T and F(strip['inherited_uniform_critical_inverse_bound'])==Kold and F(strip['critical_difference_cap'])==D
    assert strip['conditional_A_critical_interval']==list(map(str,[a,b+D])) and strip['conditional_B_critical_interval']==list(map(str,[a-D,b]))
    lo,hi=a-D,b+D;assert c[1]-F(1,100)<lo<=b<a<=hi<c[1]+F(1,100)
    assert strip['critical_column_curve_interval']==list(map(str,[lo,hi]))
    assert strip['first_replacement_order']==[i for i in range(22) if i!=12] and strip['last_replacement_coordinate']==12 and strip['last_replacement_direction']==-1
    dirs=[x['endpoint_direction'] for x in prior['uniform_curvature_checks'][0]['columns']];assert dirs[1]==1 and dirs[12]==0
    ref=[x+F(1,100)*s for x,s in zip(c,dirs)];ref[1]=hi;corner=list(ref);corner[12]=c[12]-F(1,100)
    assert strip['face_reference_coordinates']==list(map(str,ref)) and strip['corner_coordinates']==list(map(str,corner))
    assert [x['precision_bits'] for x in strip['checks']]==[1024,1536] and strip['dyadic_rounding_bits']==100
    for check in strip['checks']:
        assert endpoints(check['face_direction_12'])[1]<0
        ds=interval_sign(*endpoints(check['face_reference_determinant']));assert ds!=0 and ds==interval_sign(*endpoints(check['corner_determinant']))
        assert [interval_sign(*endpoints(x)) for x in check['corner_critical_inverse_row']]==v
        assert 0<endpoints(check['corner_norm'])[0]<=endpoints(check['corner_norm'])[1]<F(check['corner_norm_upper'])
    K=max(F(x['corner_norm_upper']) for x in strip['checks']);lower=gap/K
    assert F(strip['conditional_secant_inverse_bound'])==K<Kold and F(strip['uniform_identification_strictly_below'])==lower
    assert F(strip['previous_uniform_guarantee'])==F(prior['uniform_identification_strictly_below'])<lower<T and strip['new_lower_is_below_bootstrap_cap'] is True
    return c,L,U,v,ref,corner,K,lower

def independent_strip(ref,corner,v,K):
    checks=[]
    for bits in [896,1152]:
        ctx.prec=bits;functions=real_functions()
        J=arb_mat([[fn(av(x))[1] for x in ref] for fn in functions]);u,num,det=determinant_ratio(J,12,v);assert u<0
        J=arb_mat([[fn(av(x))[1] for x in corner] for fn in functions]);row=[];numerators=[]
        for k in range(22):
            value,n,d=determinant_ratio(J,1,[int(i==k) for i in range(22)]);assert value>0 if v[k]>0 else value<0
            row.append(value);numerators.append(enc(n))
        norm=sum(map(abs,row),arb(0));assert norm<av(K) and ((det>0 and d>0) or (det<0 and d<0))
        checks.append({'precision_bits':bits,'face_Cramer_numerator':enc(num),'face_determinant':enc(det),'face_direction_12':enc(u),
            'corner_Cramer_numerators':numerators,'corner_determinant':enc(d),'critical_inverse_row':[enc(x) for x in row],'corner_norm':enc(norm),'claimed_bound_verified':True})
    return checks

def complex_system(A,B,c,free,sides,w,scale,rho,R,v,bits):
    ctx.prec=bits;F0=[];J0=[];H=[];midpoints=[]
    freeA={i for i,s in zip(free,sides) if s=='A'};freeB=set(free)-freeA
    for k,spec in enumerate(SPECS):
        F0.append(sum((jets(spec,av(x))[0] for x in A),arb(0))-sum((jets(spec,av(x))[0] for x in B),arb(0))-2*av(scale)*av(w[21])*v[k])
        J0.append([(1 if s=='A' else -1)*jets(spec,av((A if s=='A' else B)[i]))[1] for i,s in zip(free,sides)]+[-2*av(scale)*v[k]])
        H.append([abs(jets(spec,av((A if s=='A' else B)[i])+arb(0,av(rho).upper()))[2]) for i,s in zip(free,sides)]+[arb(0)])
        midpoints.append((sum((jets(spec,av(x)+(arb(0,av(rho).upper()) if i in freeA else arb(0)))[0] for i,x in enumerate(A)),arb(0))+
                          sum((jets(spec,av(x)+(arb(0,av(rho).upper()) if i in freeB else arb(0)))[0] for i,x in enumerate(B)),arb(0)))/2)
    rows=[]
    for i in range(22):
        res=sum((av(R[i][k])*F0[k] for k in range(22)),arb(0))
        center=sum((abs(arb(int(i==j))-sum((av(R[i][k])*J0[k][j] for k in range(22)),arb(0))) for j in range(22)),arb(0))
        variation=av(rho)*sum((abs(av(R[i][k]))*sum(H[k],arb(0)) for k in range(22)),arb(0));q=center+variation;budget=abs(res)+av(rho)*q
        assert q<1 and budget<av(rho);rows.append({'index':i,'complex_residual':enc(res),'center_defect':enc(center),'variation_bound':enc(variation),'contraction_bound':enc(q),'self_map_bound':enc(budget)})
    differences=[midpoints[k]-sum((jets(spec,av(x))[0] for x in c),arb(0)) for k,spec in enumerate(SPECS)];assert differences[0]>0 or differences[0]<0
    return {'precision_bits':bits,'rows':rows,'F_at_center':[enc(x) for x in F0],'midpoint_enclosures':[enc(x) for x in midpoints],'midpoint_minus_Phi_c':[enc(x) for x in differences]}

def audit_pairs(proposal,cert,prior,c,L,U,v,data):
    r=U-F('1e-8');epsilon=F('1e-8')+F('1e-24');rho=F('1e-120')
    assert cert['status']=='passed' and cert['contract']==prior['contract'] and cert['contract']['features']==SPECS
    assert cert['common_root_center']==list(map(str,c)) and F(cert['critical_epsilon'])==epsilon and F(proposal['critical_epsilon'])==epsilon
    assert F(proposal['root_coordinate_error_radius'])==r and cert['feature_direction']==proposal['feature_direction']==v
    assert len(cert['cases'])==len(proposal['cases'])==cert['certified_pair_count']==2
    assert [F(x['margin']) for x in proposal['cases']]==[F('1e-6'),F('1e-10')]
    results=[]
    for p,record in zip(proposal['cases'],cert['cases']):
        assert p['status']=='feasible_numerical_candidate' and p['numerically_converged'] is True and p['source_centers_pass'] is True
        assert record['status']=='actual_source_mixed_variable_noise_pair' and record['case_id']==p['margin']
        free=p['free_indices'];sides=p['free_coordinate_sides'];assert free==[i for i in range(22) if i!=1] and all(type(i) is int for i in free) and len(sides)==21 and set(sides)=={'A','B'}
        assert record['root_variable_indices']==free and record['root_variable_sides']==sides and record['root_jacobian_column_signs']==[1 if s=='A' else -1 for s in sides]
        assert record['variable_dimension']==22 and record['root_variable_count']==21 and record['noise_variable_index']==21
        assert record['noise_variable_definition']=='alpha=tau/scale' and F(record['variable_radius'])==rho and record['noise_column_derivative_variation']=='0'
        A=list(map(F,p['fixed_A_coordinates']));B=list(map(F,p['fixed_B_coordinates']));w=list(map(F,p['variable_center']));assert len(A)==len(B)==len(w)==22
        for k,(i,side) in enumerate(zip(free,sides)):(A if side=='A' else B)[i]=w[k]
        assert A==list(map(F,p['rational_A_coordinates'])) and B==list(map(F,p['rational_B_coordinates'])) and record['variable_center']==list(map(str,w))
        assert A[1]==c[1]+epsilon and B[1]==c[1]-epsilon and F(record['critical_root_gap'])==2*epsilon>2*(L-r)
        scale=F(p['tau_scale']);assert scale==F(record['tau_scale'])==F('1e-10') and w[21]>rho
        assert record['noise_jacobian_column']==[str(-2*scale*s) for s in v] and record['signed_feature_difference_coefficients']==[2*s for s in v]
        assert record['common_release']=='(Phi(A)+Phi(B))/2' and record['component_error_at_exact_solution']=='tau'
        labels={i:s for i,s in zip(free,sides)};boxes={side:[(x-rho,x+rho) if labels.get(i)==side else (x,x) for i,x in enumerate(coords)] for side,coords in [('A',A),('B',B)]}
        assert record['A_observation_boxes']==[list(map(str,x)) for x in boxes['A']] and record['B_observation_boxes']==[list(map(str,x)) for x in boxes['B']]
        for value in boxes.values():assert value[0][0]>0 and all(x[1]<y[0] for x,y in zip(value,value[1:]))
        margin=F(1,100)-max(abs(x-z) for value in boxes.values() for pair,z in zip(value,c) for x in pair)
        assert F(record['minimum_cube_margin'])==margin>0
        tau=(scale*(w[21]-rho),scale*(w[21]+rho));assert record['tau_interval']==list(map(str,tau)) and F(record['budget_guaranteed_for_pair'])==tau[1]
        R=[list(map(F,row)) for row in p['preconditioner']];assert len(R)==22 and all(len(row)==22 for row in R);mod=modular_det(R)
        independent=[complex_system(A,B,c,free,sides,w,scale,rho,R,v,bits) for bits in [896,1152]]
        assert [x['precision_bits'] for x in record['direct_checks']]==[768,1024]
        for check in record['direct_checks']:
            assert interval_sign(*endpoints(check['preconditioner_determinant']))!=0
            assert len(check['rows'])==len(check['F_at_center'])==len(check['common_midpoint_enclosures'])==len(check['midpoint_minus_Phi_c'])==22
            for i,row in enumerate(check['rows']):
                assert row['index']==i and endpoints(row['derivative_defect'])[1]<1 and endpoints(row['self_map_bound'])[1]<rho and endpoints(row['strict_margin'])[0]>0
                assert all(overlaps(check['F_at_center'][i],x['F_at_center'][i]) and overlaps(check['common_midpoint_enclosures'][i],x['midpoint_enclosures'][i]) and overlaps(check['midpoint_minus_Phi_c'][i],x['midpoint_minus_Phi_c'][i]) for x in independent)
            assert interval_sign(*endpoints(check['midpoint_minus_Phi_c'][0]))!=0
        stored={(x['input_member'],x['source_index']):x for x in record['coordinate_audit']};assert len(stored)==len(record['coordinate_audit'])==88;constraints=[]
        for bits in [160,224]:
            for number,side in [(1,'A'),(2,'B')]:
                member=f'E{number}_{bits}.json'
                for i,(lo,hi) in enumerate(boxes[side]):
                    slo,shi=[F(data[member]['positive_root_intervals'][i][k]) for k in ['lo','hi']]
                    left=lo-(shi-r);right=(slo+r)-hi;assert left>=0 and right>=0
                    q=stored[(member,i)];assert q['precision_bits']==bits and q['within_radius'] is True and F(q['error_margin'])==min(left,right)
                    assert q['source_interval']==list(map(str,[slo,shi])) and q['observed_interval']==list(map(str,[lo,hi])) and F(q['maximum_uniform_error'])==r-min(left,right)
                    constraints.append({'input_member':member,'coordinate':i,'observation_side':side,'lower_source_margin':str(left),'upper_source_margin':str(right)})
        results.append({'case_id':record['case_id'],'modular_preconditioner':mod,'independent_complex_checks':independent,'direct_source_constraints':constraints,'scalar_source_inequalities':176,'tau_interval':list(map(str,tau)),
            'free_A_indices':[i for i,s in zip(free,sides) if s=='A'],'free_B_indices':[i for i,s in zip(free,sides) if s=='B'],'minimum_cube_margin':str(margin)})
    best=min(F(x['tau_interval'][1]) for x in results)
    assert F(cert['best_certified_tau_upper'])==best<F(cert['previous_upper_endpoint'])==F(prior['inherited_ambiguity_upper_endpoint'])
    return results

def run(strip,mixed,proposal,root=ROOT):
    inherited=[root/p for p in [PRIOR,ANCHOR,REGION,UPPER,SOURCE+'/Equal_Population_Inputs.zip',SOURCE+'/Equal_Population_Decoder.json',CLASS,ARITH]]
    prior,a,reg,upper=map(read,inherited[:4]);sc,mc,p=map(read,[strip,mixed,proposal])
    with zipfile.ZipFile(inherited[4]) as z:data={n:json.loads(z.read(n)) for n in z.namelist()}
    assert sc['inputs_sha256']=={x.name:sha(x) for x in inherited[:5]}
    assert mc['inputs_sha256']=={x.name:sha(x) for x in [inherited[0],inherited[5],inherited[4],proposal]}
    for x in [inherited[0],inherited[5],inherited[4]]:assert p['inputs_sha256'][x.name]==sha(x)
    c,L,U,v,ref,corner,K,lower=strip_data(sc,prior,a,reg,upper,data)
    strip_checks=independent_strip(ref,corner,v,K);cases=audit_pairs(p,mc,prior,c,L,U,v,data)
    best=min(F(x['tau_interval'][1]) for x in cases);assert lower<best<F(sc['bootstrap_feature_budget_cap'])
    src,cl,ar=map(read,inherited[5:]);assert src['status']==cl['status']=='passed' and cl['complete_quartic_candidate_count']==2
    vectors,factors=arithmetic_vectors(inherited[7],src['columns'])
    labels={m['class_id']:next(k for k,val in ar['fields'].items() if sorted(val['quadratic_discriminants'])==m['quadratic_discriminants']) for m in cl['retained_models']}
    assert set(labels.values())=={'A','B'} and all(src['predictions'][k]==vectors[val] for k,val in labels.items())
    domains=[sorted({val[j] for val in vectors.values()}) for j in range(604)];assert len(factors)==1128 and sum(len(x)==1 for x in domains)==456
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in inherited+[strip,mixed,proposal]},
        'independent_source_strip_checks':strip_checks,'mixed_pair_checks':cases,'certified_pair_count':2,'scalar_source_inequalities':352,
        'uniform_identification_strictly_below':str(lower),'best_certified_tau_upper':str(best),'upper_to_guarantee_ratio':str(best/lower),'ratio_display':float(best/lower),
        'factorization_count':1128,'polynomial_factorizations':factors,'coefficient_comparisons':1208,'class_mapping':labels,'fixed_coefficients':456,'ambiguous_coefficients':148,
        'scope':'Independent source endpoints and real-polynomial Cramer ratios verify the strip lower premises; complex scalar Jacobians and second derivatives audit both mixed A/B systems. All 352 scalar source inequalities are rebuilt directly. Polynomial arithmetic confirms the inherited finite coefficient consequences. Numerical routes share FLINT and inherited source/classification premises. Full analytic assembly and source-feasible sharpness remain open.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['strip','mixed','proposal','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.strip,a.mixed,a.proposal);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','certified_pair_count','scalar_source_inequalities','ratio_display']}))
