"""Independently audit common feature releases and local two-sided identification bounds."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_augmented_feature_audit import jets,modular_det,input_geometry
from dedekind_weighted_region_audit_v2 import SPECS
from dedekind_aggregate_integer_audit import arithmetic_vectors

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def av(x):
    q=F(x);return arb(q.numerator)/arb(q.denominator)
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def ball(x):return arb(arb(tuple(x['mid'])),arb(tuple(x['rad'])))
def audit_root(c,v,tau,proposed,record):
    assert proposed['field_sign']==record['field_sign'] and proposed['field_sign'] in [-1,1] and proposed['numerically_converged'] is True and record['status']=='exact_target_root_exists'
    rho=F(record['correction_box_radius']);assert rho==F('1e-120') and len(proposed['corrections'])==22
    y=[x+F(w) for x,w in zip(c,proposed['corrections'])];boxes=[(x-rho,x+rho) for x in y];assert record['observation_boxes']==[list(map(str,x)) for x in boxes]
    distance=max(abs(x-z) for box,z in zip(boxes,c) for x in box);assert F(record['maximum_distance_from_common_center'])==distance<=F(1,100) and record['inside_radius_0p01_cube'] is True
    assert all(x[1]<z[0] for x,z in zip(boxes,boxes[1:]))
    R=[list(map(F,row)) for row in proposed['preconditioner']];assert len(R)==22 and all(len(row)==22 for row in R)
    determinant=modular_det(R);ctx.prec=896;F0=[];J=[];M=[];target=[]
    for k,spec in enumerate(SPECS):
        target.append(sum((jets(spec,av(x))[0] for x in c),arb(0)))
        F0.append(sum((jets(spec,av(x))[0] for x in y),arb(0))-target[-1]-proposed['field_sign']*av(tau)*v[k])
        J.append([jets(spec,av(x))[1] for x in y]);M.append([abs(jets(spec,av(x)+arb(0,av(rho).upper()))[2]) for x in y])
    rows=[]
    for i in range(22):
        residual=sum((av(R[i][k])*F0[k] for k in range(22)),arb(0))
        center=sum((abs(arb(int(i==j))-sum((av(R[i][k])*J[k][j] for k in range(22)),arb(0))) for j in range(22)),arb(0))
        variation=av(rho)*sum((abs(av(R[i][k]))*sum(M[k],arb(0)) for k in range(22)),arb(0))
        q=center+variation;budget=abs(residual)+av(rho)*q;assert q<1 and budget<av(rho)
        rows.append({'index':i,'complex_residual':enc(residual),'center_inverse_defect':enc(center),'second_derivative_variation_bound':enc(variation),'contraction_bound':enc(q),'self_map_bound':enc(budget)})
    assert [x['precision_bits'] for x in record['contraction_checks']]==[768,1024]
    for check in record['contraction_checks']:
        assert len(check['rows'])==len(check['F_at_rational_center'])==len(check['common_exact_feature_enclosures'])==22
        for i,row in enumerate(check['rows']):
            assert row['index']==i and ball(row['derivative_defect_bound'])<1 and ball(row['self_map_bound'])<av(rho) and ball(row['strict_margin'])>0
            assert ball(check['F_at_rational_center'][i]).overlaps(F0[i]) and ball(check['common_exact_feature_enclosures'][i]).overlaps(target[i])
    return {'status':'passed','modular_nonsingularity':determinant,'precision_bits':896,'complex_Taylor_rows':rows},boxes
def audit_data(p,certificate,anchor,region,inputs):
    c,L,U=input_geometry(inputs);assert certificate['status']=='passed' and p['features']==anchor['full_rank_proposal']['features']==SPECS
    assert list(map(F,p['common_root_center']))==list(map(F,anchor['common_rational_coordinates']))==c
    r=U-F('1e-8');assert F(p['root_coordinate_error_radius'])==r<L and F(p['source_threshold_lower'])==L and F(p['critical_required_shift'])==F('1e-8')
    expected={'source_cutoff':'39/2','source_population':22,'source_selection':'complete_positive_prefix_before_coordinate_errors','root_entries_and_multiplicity':'preserved',
        'root_coordinate_error_radius':str(r),'observed_root_region_radius':'1/100','region_geometry':'standard_coordinate_cube_centered_at_c','features':SPECS,
        'additional_feature_errors':'independent_absolute_component_bounds','raw_roots_or_counts_released':False,'unknown_tails_included':False}
    assert certificate['contract']==expected and region['status']=='passed'
    local=next(x for x in region['regions'] if F(x['radius'])==F(1,100));h=list(map(F,local['exact_componentwise_inverse_bounds']));guarantee=(L-r)/h[1]
    assert F(local['uniform_feature_error_identification_guarantee_strictly_below'])==guarantee and F(certificate['uniform_identification_below'])==guarantee
    v=p['feature_direction'];assert v==certificate['feature_direction']==[1 if F(x)>0 else -1 if F(x)<0 else 0 for x in anchor['full_rank_proposal']['preconditioner'][1]]
    assert len(v)==22 and all(type(x) is int and abs(x)==1 for x in v)
    assert len(p['cases'])==len(certificate['cases'])==4;results=[];accepted=[]
    for proposed,case in zip(p['cases'],certificate['cases']):
        tau=F(proposed['feature_error_bound']);assert tau==F(case['feature_error_bound'])>0
        audits={};boxes={}
        for label in ['A','B']:audits[label],boxes[label]=audit_root(c,v,tau,proposed[label],case['roots'][label])
        assert proposed['A']['field_sign']==1 and proposed['B']['field_sign']==-1
        constraints=[];exclusions=[];violations=0
        for bits in [160,224]:
            for number,label in [(1,'A'),(2,'B')]:
                name=f'E{number}_{bits}.json'
                for i,(lo,hi) in enumerate(boxes[label]):
                    slo,shi=[F(inputs[name]['positive_root_intervals'][i][k]) for k in ['lo','hi']]
                    left=lo-(shi-r);right=(slo+r)-hi;inside=left>=0 and right>=0
                    stored=next(x for x in case['coordinate_audit'] if x['input_member']==name and x['source_index']==i)
                    assert stored['precision_bits']==bits and stored['within_radius']==inside and F(stored['error_margin'])==min(left,right)
                    assert stored['source_interval']==[str(slo),str(shi)] and stored['observed_interval']==[str(lo),str(hi)]
                    assert F(stored['maximum_uniform_error'])==r-min(left,right)
                    margin=max(slo-hi,lo-shi,F(0))-r
                    if not inside:violations+=1
                    if margin>0:exclusions.append({'input_member':name,'source_index':i,'all_source_and_observation_points_violate_by_at_least':str(margin)})
                    constraints.append({'input_member':name,'index':i,'left_inclusion_margin':str(left),'right_inclusion_margin':str(right),'inside':inside})
        assert len(case['coordinate_audit'])==len(constraints)==88 and case['coordinate_violation_count']==violations and case['uniform_source_exclusions']==exclusions
        if violations:
            assert exclusions and case['status']=='signed_target_pair_excluded_in_local_cube'
        else:
            assert case['status']=='actual_source_common_noisy_release';accepted.append(tau)
            # The critical source-box gap is uniformly positive for every pair in the two root boxes.
            assert boxes['A'][1][0]-boxes['B'][1][1]>=2*(L-r)>0
        assert case['exact_feature_difference_vector']==[str(2*tau*x) for x in v] and F(case['exact_feature_pair_infinity_distance'])==2*tau
        results.append({'tau':str(tau),'status':case['status'],'root_audits':audits,'scalar_source_constraints':constraints,'scalar_inequalities':176,'uniform_source_exclusions':exclusions})
    upper=min(accepted);assert len(accepted)==certificate['source_feasible_noisy_pairs']==2 and certificate['excluded_signed_target_pairs']==2 and certificate['exact_inverse_roots_certified']==8
    assert F(certificate['actual_ambiguity_at'])==upper and F(certificate['upper_to_guarantee_ratio'])==upper/guarantee and guarantee<upper
    return {'status':'passed','cases':results,'exact_inverse_root_count':8,'scalar_coordinate_inequalities':704,'source_feasible_common_releases':2,'excluded_signed_target_pairs':2,
        'uniform_identification_below':str(guarantee),'actual_ambiguity_at':str(upper),'upper_to_lower_ratio':str(upper/guarantee),
        'scope':'Complex second-derivative contraction bounds and modular inverses independently certify all eight exact targets. Rational source inequalities prove feasible common releases or uniform exclusion of the specified signed target pair. The local uniqueness theorem excludes alternative local roots for those exact targets, not other target choices. Uniform identification is a separation theorem, not an implemented decoder for arbitrary observations.'}
def run(proposal,certificate,anchor,region,region_audit,inputs,classification,arithmetic,source):
    paths=[proposal,certificate,anchor,region,region_audit,inputs,classification,arithmetic,source];p=json.loads(proposal.read_text());cert=json.loads(certificate.read_text());a=json.loads(anchor.read_text());reg=json.loads(region.read_text());ra=json.loads(region_audit.read_text());cl=json.loads(classification.read_text());src=json.loads(source.read_text())
    assert cert['inputs_sha256']=={x.name:sha(x) for x in [proposal,anchor,source,inputs,region]} and p['input_sha256']==sha(anchor)
    assert ra['status']=='passed' and ra['inputs_sha256'][region.name]==sha(region) and all(x['independent_critical_bound_no_larger_than_claimed'] for x in ra['regions'])
    assert cl['status']==src['status']=='passed' and cl['complete_quartic_candidate_count']==2
    with zipfile.ZipFile(inputs) as z:data={name:json.loads(z.read(name)) for name in z.namelist()}
    result=audit_data(p,cert,a,reg,data);vectors,factors=arithmetic_vectors(arithmetic,src['columns']);ar=json.loads(arithmetic.read_text())
    labels={m['class_id']:next(k for k,v in ar['fields'].items() if sorted(v['quadratic_discriminants'])==m['quadratic_discriminants']) for m in cl['retained_models']}
    assert set(labels.values())=={'A','B'} and all(src['predictions'][k]==vectors[v] for k,v in labels.items())
    domains=[sorted({v[j] for v in vectors.values()}) for j in range(604)];assert len(factors)==1128 and sum(len(x)==1 for x in domains)==456
    result.update(source_sha256=sha(Path(__file__)),inputs_sha256={x.name:sha(x) for x in paths},class_mapping=labels,polynomial_factorizations=factors,factorization_count=1128,coefficient_comparisons=1208,columns=src['columns'],common_release_coefficient_domains=domains,fixed_coefficients=456,ambiguous_coefficients=148)
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['proposal','certificate','anchor','region','region-audit','inputs','classification','arithmetic','source','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a.proposal,a.certificate,a.anchor,a.region,a.region_audit,a.inputs,a.classification,a.arithmetic,a.source);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'roots':r['exact_inverse_root_count'],'inequalities':r['scalar_coordinate_inequalities'],'feasible_pairs':r['source_feasible_common_releases'],'excluded_signed_targets':r['excluded_signed_target_pairs'],'fixed_coefficients':456,'ambiguous_coefficients':148}))
