"""Independently audit augmented collisions and local injectivity with complex Taylor bounds."""
import argparse, hashlib, json, zipfile
from fractions import Fraction as F
from pathlib import Path
import sympy as s
from flint import arb, acb, ctx
from dedekind_aggregate_integer_audit import arithmetic_vectors

SPECS=[{'kind':'gaussian','center':n,'a':'1/25'} for n in [2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31]]+[
    {'kind':'rational_moment','numerator':3,'offset':'9/4'}, {'kind':'gaussian','center':37,'a':'1/25'},
    {'kind':'gaussian','center':2,'a':'1/24'}, {'kind':'gaussian','center':41,'a':'1/25'}, {'kind':'gaussian','center':43,'a':'1/25'}]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def av(x):
    q=F(x);return arb(q.numerator)/arb(q.denominator)
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def ball(x):return arb(arb(tuple(x['mid'])),arb(tuple(x['rad'])))
def modular_det(R):
    prime=65537;assert all(prime%d for d in range(2,257));n=len(R)
    assert all(len(row)==n for row in R)
    a=[[x.numerator%prime*pow(x.denominator,-1,prime)%prime for x in row] for row in R];det=1;pivots=[]
    for i in range(n):
        j=next(j for j in range(i,n) if a[j][i])
        if i!=j:a[i],a[j]=a[j],a[i];det=-det
        pivot=a[i][i];pivots.append(pivot);det=det*pivot%prime
        for k in range(i+1,n):
            factor=a[k][i]*pow(pivot,-1,prime)%prime
            a[k]=[(x-factor*y)%prime for x,y in zip(a[k],a[i])]
    assert det%prime
    return {'prime':prime,'dimension':n,'determinant_mod_prime':det%prime,'pivots':pivots}
def jets(spec,x):
    if spec['kind']=='rational_moment':
        d=av('9/4')+x*x
        return 3/d,-6*x/d**2,6*(3*x*x-av('9/4'))/d**3
    a=av(spec['a']);u=arb(spec['center']).log();z=acb(-a*x*x,u*x).exp();v=acb(-2*a*x,u)
    return 2*z.real,2*(v*z).real,2*((v*v-2*a)*z).real
def taylor(specs,A,B,selected,R,rho,bits=768):
    ctx.prec=bits;n=len(specs);F0=[];J0=[];M=[];target=[]
    for spec in specs:
        target.append(sum((jets(spec,av(x))[0] for x in B),arb(0)))
        F0.append(sum((jets(spec,av(x))[0] for x in A),arb(0))-target[-1])
        J0.append([jets(spec,av(A[j]))[1] for j in selected])
        M.append([abs(jets(spec,av(A[j])+arb(0,av(rho).upper()))[2]) for j in selected])
    rows=[]
    for i in range(n):
        e=sum((av(R[i][k])*F0[k] for k in range(n)),arb(0))
        defect=sum((abs(arb(int(i==j))-sum((av(R[i][k])*J0[k][j] for k in range(n)),arb(0))) for j in range(n)),arb(0))
        weighted=sum((abs(av(R[i][k]))*sum(M[k],arb(0)) for k in range(n)),arb(0))
        q=defect+av(rho)*weighted;budget=abs(e)+av(rho)*q
        rows.append({'index':i,'center_inverse_defect':enc(defect),'weighted_second_derivative_bound':enc(weighted),'contraction_bound':enc(q),
                     'preconditioned_residual':enc(e),'self_map_bound':enc(budget),'strict_self_map_margin':enc(av(rho)-budget)})
    return {'precision_bits':bits,'rows':rows,'F_center':[enc(x) for x in F0],'target':[enc(x) for x in target]}
def input_geometry(inputs):
    assert sorted(inputs)==['E1_160.json','E1_224.json','E2_160.json','E2_224.json']
    for d in inputs.values():
        assert set(d)=={'degree','discriminant','real_places','complex_places','top','positive_root_intervals'}
        assert [d[k] for k in ['degree','discriminant','real_places','complex_places']]==[4,576,0,2] and d['top']=='39/2' and len(d['positive_root_intervals'])==22
        roots=[tuple(F(x[k]) for k in ['lo','hi']) for x in d['positive_root_intervals']]
        assert all(0<lo<hi<F(39,2) for lo,hi in roots) and all(x[1]<y[0] for x,y in zip(roots,roots[1:]))
    a,b=[[tuple(F(x[k]) for k in ['lo','hi']) for x in inputs[f'E{i}_224.json']['positive_root_intervals']] for i in [1,2]]
    c=[(min(x[0],y[0])+max(x[1],y[1]))/2 for x,y in zip(a,b)]
    return c,(a[1][0]-b[1][1])/2,(a[1][1]-b[1][0])/2
def audit_pair(p,cert,inputs):
    common,L,U=input_geometry(inputs);assert cert['status']=='passed'
    assert list(map(F,p['common_rational_coordinates']))==common and F(p['source_threshold_lower'])==L and F(p['source_threshold_upper'])==U
    assert [c['dimension'] for c in p['cases']]==[18,19,20,21]==[c['dimension'] for c in cert['collisions']]
    audits=[]
    for proposed,record in zip(p['cases'],cert['collisions']):
        n=proposed['dimension'];assert type(n) is int and record['status']=='passed' and proposed['features']==SPECS[:n]
        contract={'source_cutoff':'39/2','source_population':22,'source_selection':'complete_positive_prefix_before_coordinate_errors','coordinate_errors':'independent_absolute_bounds','entries_and_multiplicity':'preserved','post_noise_window_censoring':False,'released_features':SPECS[:n],'released_raw_coordinates':False,'released_cumulative_counts':False,'included_unknown_tail':False}
        assert record['contract']==contract
        eps=F(proposed['critical_split_epsilon']);rho=F(record['correction_box_radius']);r=F(record['radius'])
        assert eps==F(record['critical_split_epsilon'])>0 and rho>0 and 0<r==F(p['radius'])==U-eps<L and F(record['strict_improvement_below_L'])==L-r
        selected=proposed['selected_A_variable_indices'];assert selected==record['selected_A_variable_indices'] and len(selected)==len(set(selected))==n and all(type(i) is int and i!=1 and 0<=i<22 for i in selected)
        assert len(proposed['corrections'])==n
        A=list(common);B=list(common);A[1]+=eps;B[1]-=eps
        for j,i in enumerate(selected):A[i]+=F(proposed['corrections'][j])
        boxes=[(x-rho,x+rho) if i in selected else (x,x) for i,x in enumerate(A)]
        assert record['A_observed_coordinate_boxes']==[list(map(str,x)) for x in boxes] and list(map(F,record['B_fixed_observed_coordinates']))==B
        assert all(x[1]<y[0] for x,y in zip(boxes,boxes[1:])) and all(x<y for x,y in zip(B,B[1:])) and A[1]-B[1]==2*eps
        inclusions=[]
        for bits in [160,224]:
            for field,observed in [(1,boxes),(2,[(x,x) for x in B])]:
                name=f'E{field}_{bits}.json'
                for i,(lo,hi) in enumerate(observed):
                    slo,shi=[F(inputs[name]['positive_root_intervals'][i][k]) for k in ['lo','hi']]
                    assert shi-r<=lo<=hi<=slo+r
                    old=next(x for x in record['coordinate_audit'] if x['input_member']==name and x['source_index']==i)
                    assert old['precision_bits']==bits and old['within_radius'] is True and old['source_interval']==[str(slo),str(shi)] and old['observed_interval']==[str(lo),str(hi)]
                    margin=min(lo-shi+r,slo+r-hi);assert F(old['error_margin'])==margin and F(old['maximum_uniform_error'])==r-margin
                    inclusions.append({'member':name,'index':i,'left_margin':str(lo-shi+r),'right_margin':str(slo+r-hi)})
        assert len(record['coordinate_audit'])==len(inclusions)==88
        R=[list(map(F,row)) for row in proposed['preconditioner']];assert len(R)==n and all(len(row)==n for row in R)
        determinant=modular_det(R);checked=taylor(SPECS[:n],A,B,selected,R,rho)
        assert all(ball(row['contraction_bound'])<1 and ball(row['strict_self_map_margin'])>0 for row in checked['rows'])
        assert [c['precision_bits'] for c in record['contraction_checks']]==[640,896]
        for c in record['contraction_checks']:
            assert len(c['rows'])==len(c['F_center'])==len(c['fixed_common_feature_vector'])==n
            for i,row in enumerate(c['rows']):
                assert row['index']==i and ball(row['derivative_defect_row_sum'])<1 and ball(row['self_map_bound'])<av(rho) and ball(row['strict_margin'])>0
                assert ball(c['F_center'][i]).overlaps(ball(checked['F_center'][i])) and ball(c['fixed_common_feature_vector'][i]).overlaps(ball(checked['target'][i]))
        h=common[1];assert record['interior_counts']=={'height':str(h),'A_envelope':[1,1],'B':2}
        assert sum(hi<h for lo,hi in boxes)==sum(lo<h for lo,hi in boxes)==1 and sum(x<h for x in B)==2
        audits.append({'dimension':n,'coordinate_inclusions':inclusions,'scalar_inequalities':176,'modular_preconditioner':determinant,'complex_Taylor':checked})
    local=cert['rank_and_local_injectivity'];assert local['status']=='passed' and local['full_dimension']==22 and local['features']==SPECS
    assert list(map(F,local['neighborhood_center']))==common and local['uniform_derivative_defect_bound']=='1/2'
    eta=F(local['certified_neighborhood_radius']);assert eta>0 and all(x+eta<y-eta for x,y in zip(common,common[1:])) and common[0]>eta
    assert p['full_rank_proposal']['dimension']==22 and p['full_rank_proposal']['features']==SPECS
    R=[list(map(F,row)) for row in p['full_rank_proposal']['preconditioner']];assert len(R)==22 and all(len(row)==22 for row in R)
    full_det=modular_det(R);full=taylor(SPECS,common,common,list(range(22)),R,eta)
    assert all(ball(row['contraction_bound'])<av('1/2') for row in full['rows'])
    norm=max(sum(abs(x) for x in row) for row in R);assert F(local['exact_preconditioner_infinity_norm'])==norm and F(local['inverse_Lipschitz_bound'])==2*norm
    ranks=[]
    assert len(local['rank_minor_checks'])==4
    for case,record in zip(p['cases'],local['rank_minor_checks']):
        n=case['dimension'];selected=case['selected_A_variable_indices'];Q=[list(map(F,row)) for row in case['center_preconditioner']]
        assert len(Q)==n and all(len(row)==n for row in Q) and record['dimension']==n and record['selected_columns']==selected and record['square_minor_invertible'] is True
        check=taylor(SPECS[:n],common,common,selected,Q,F(0));assert all(ball(x['center_inverse_defect'])<1 for x in check['rows'])
        assert len(record['defect_row_sums'])==n and all(ball(x)<1 for x in record['defect_row_sums'])
        ranks.append({'dimension':n,'modular_inverse':modular_det(Q),'center_defects':[x['center_inverse_defect'] for x in check['rows']]})
    memberships=[]
    for record in cert['collisions']:
        distance=max([abs(F(x)-common[i]) for i,b in enumerate(record['A_observed_coordinate_boxes']) for x in b]+[abs(F(x)-common[i]) for i,x in enumerate(record['B_fixed_observed_coordinates'])])
        assert F(record['maximum_distance_from_local_center'])==distance and record['both_observations_inside_injective_22_feature_neighborhood']==(distance<=eta)
        memberships.append(distance<=eta)
    record=cert['collisions'][-1];AA=[av(lo).union(av(hi)) for lo,hi in record['A_observed_coordinate_boxes']];BB=list(map(av,record['B_fixed_observed_coordinates']))
    difference=sum((jets(SPECS[-1],x)[0] for x in AA),arb(0))-sum((jets(SPECS[-1],x)[0] for x in BB),arb(0))
    assert difference>0 or difference<0
    conditional_lower=F(record['critical_split_epsilon'])/norm if memberships[-1] else None
    if conditional_lower is not None:assert abs(difference)>av(conditional_lower)
    return {'status':'passed','collision_audits':audits,'total_scalar_coordinate_inequalities':704,'independent_rank_minors':ranks,
            'full_preconditioner_modular_determinant':full_det,'local_complex_Taylor':full,'certified_neighborhood_radius':str(eta),
            'local_memberships':memberships,'center_43_difference_for_21_feature_witness':enc(difference),'center_43_difference_display':float(difference.mid()),
            'conditional_center_43_gap_from_local_inverse_bound':str(conditional_lower) if conditional_lower is not None else None,
            'scope':'Complex exponential jets and rational moment derivatives prove contraction and local injectivity independently of the real interval Jacobian product. Scalar inclusions are reconstructed directly from anonymous source boxes. Both formulations still share FLINT. The inverse-bound gap applies only when both observations belong to the certified local neighborhood.'}
def symbolic_audit():
    x,a,u,d=s.symbols('x a u d',real=True);g=2*s.exp(-a*x*x)*s.cos(u*x);m=3/(d+x*x)
    assert s.simplify(s.diff(g,x)-2*s.exp(-a*x*x)*(-2*a*x*s.cos(u*x)-u*s.sin(u*x)))==0
    assert s.simplify(s.diff(g,x,2)-2*s.exp(-a*x*x)*((4*a*a*x*x-2*a-u*u)*s.cos(u*x)+4*a*u*x*s.sin(u*x)))==0
    assert s.simplify(s.diff(m,x)+6*x/(d+x*x)**2)==0
    assert s.simplify(s.diff(m,x,2)-6*(3*x*x-d)/(d+x*x)**3)==0
    return {'Gaussian_first_and_second':'passed','rational_moment_first_and_second':'passed'}
def run(evidence,source,inputs,classification,arithmetic):
    paths=[source,inputs,classification,arithmetic];source_data=json.loads(source.read_text());cl=json.loads(classification.read_text());assert source_data['status']==cl['status']=='passed' and cl['complete_quartic_candidate_count']==2
    with zipfile.ZipFile(inputs) as z:data={n:json.loads(z.read(n)) for n in z.namelist()}
    cases={}
    for suffix in ['Enlarged','Small','Local']:
        pp=evidence/f'Augmented_Proposals_{suffix}.json';cp=evidence/f'Augmented_Certificate_{suffix}_v2.json';paths.extend([pp,cp]);p=json.loads(pp.read_text());c=json.loads(cp.read_text())
        assert p['input_sha256']==sha(source) and c['inputs_sha256']=={x.name:sha(x) for x in [pp,source,inputs]}
        cases[suffix]=audit_pair(p,c,data)
    vectors,factors=arithmetic_vectors(arithmetic,source_data['columns']);ar=json.loads(arithmetic.read_text())
    labels={m['class_id']:next(k for k,v in ar['fields'].items() if sorted(v['quadratic_discriminants'])==m['quadratic_discriminants']) for m in cl['retained_models']}
    assert set(labels.values())=={'A','B'} and all(source_data['predictions'][k]==vectors[v] for k,v in labels.items())
    domains=[sorted({v[j] for v in vectors.values()}) for j in range(604)];assert len(factors)==1128 and sum(len(x)==1 for x in domains)==456
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in paths},'cases':cases,'symbolic_derivatives':symbolic_audit(),
            'total_collision_certificates':12,'total_scalar_coordinate_inequalities':2112,'polynomial_factorizations':factors,'factorizations_count':1128,'coefficient_comparisons':1208,
            'class_mapping':labels,'columns':source_data['columns'],'coefficient_domains':domains,'fixed_coefficients':456,'ambiguous_coefficients':148,
            'scope':'The arithmetic domains remain exact within the complete inherited two-field class for all certified collisions, including the joint finite moment. Local 22-feature injectivity does not prove global recovery over the full feasible observation region.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['evidence','source','inputs','classification','arithmetic','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.evidence,a.source,a.inputs,a.classification,a.arithmetic);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'collisions':12,'scalar_inequalities':2112,'fixed_coefficients':456,'ambiguous_coefficients':148,
                      'center_43_differences':{k:v['center_43_difference_display'] for k,v in r['cases'].items()},'local_memberships':r['cases']['Local']['local_memberships']}))
