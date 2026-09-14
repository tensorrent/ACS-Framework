"""Audit finite-feature collisions by complex Taylor bounds and modular nonsingularity."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
import sympy as s
from flint import arb,acb,ctx
from dedekind_aggregate_integer_audit import arithmetic_vectors

CENTERS=[2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def av(x):q=F(x);return arb(q.numerator)/arb(q.denominator)
def from_ball(x):return arb(arb(tuple(x['mid'])),arb(tuple(x['rad'])))
def modular_determinant(matrix,prime=65537):
    assert prime==65537 and all(prime%d for d in range(2,257))
    a=[[x.numerator%prime*pow(x.denominator,-1,prime)%prime for x in row] for row in matrix];det=1;pivots=[];swaps=[]
    for i in range(17):
        j=next(j for j in range(i,17) if a[j][i])
        if i!=j:a[i],a[j]=a[j],a[i];det=-det;swaps.append([i,j])
        pivot=a[i][i];pivots.append(pivot);det=det*pivot%prime
        for k in range(i+1,17):
            factor=a[k][i]*pow(pivot,-1,prime)%prime
            a[k]=[(x-factor*y)%prime for x,y in zip(a[k],a[i])]
    assert det%prime!=0
    return {'prime':prime,'determinant_mod_prime':det%prime,'nonzero_pivots':pivots,'row_swaps':swaps,'scope':'All rational denominators are invertible modulo this explicitly trial-divided prime. Nonzero modular determinant implies the rational preconditioner is nonsingular.'}
def independent_parameters(proposal,certificate,inputs):
    assert certificate['status']=='passed' and certificate['coordinate_violations']==[]
    contract={'source_cutoff':'39/2','source_population':22,'source_selection':'complete_positive_prefix_before_coordinate_errors','coordinate_errors':'independent_absolute_bounds','entries_and_multiplicity':'preserved','post_noise_window_censoring':False,'released_observable':'seventeen_finite_Gaussian_sums','gaussian_a':'1/25','normalization':2,'centers':CENTERS,'released_raw_coordinates':False,'released_cumulative_counts':False,'released_moment':False,'included_unknown_tail':False}
    assert certificate['contract']==contract and proposal['centers']==CENTERS and proposal['gaussian_a']=='1/25' and proposal['critical_index']==1
    assert sorted(inputs)==['E1_160.json','E1_224.json','E2_160.json','E2_224.json']
    for d in inputs.values():
        assert set(d)=={'degree','discriminant','real_places','complex_places','top','positive_root_intervals'} and d['top']=='39/2'
        assert [d[k] for k in ['degree','discriminant','real_places','complex_places']]==[4,576,0,2] and len(d['positive_root_intervals'])==22
    a,b=[[tuple(F(x[k]) for k in ['lo','hi']) for x in inputs['E'+str(n)+'_224.json']['positive_root_intervals']] for n in [1,2]]
    common=[(min(x[0],y[0])+max(x[1],y[1]))/2 for x,y in zip(a,b)]
    assert common==list(map(F,proposal['common_rational_coordinates']))
    L=(a[1][0]-b[1][1])/2;U=(a[1][1]-b[1][0])/2
    eps,r,rho=map(F,[certificate['critical_split_epsilon'],certificate['radius'],certificate['correction_box_radius']])
    assert eps==F(proposal['critical_split_epsilon'])>0 and rho>0 and r==F(proposal['radius'])==U-eps<L
    assert F(certificate['full_point_list_threshold_lower'])==F(proposal['source_threshold_lower'])==L
    assert F(certificate['strict_improvement_below_lower'])==L-r>0
    selected=proposal['selected_A_variable_indices'];assert selected==certificate['selected_A_variable_indices'] and len(selected)==len(set(selected))==17
    assert all(type(i) is int and 0<=i<22 and i!=1 for i in selected)
    A=list(common);B=list(common);A[1]+=eps;B[1]-=eps
    assert len(proposal['corrections'])==17 and len(proposal['preconditioner'])==17 and all(len(row)==17 for row in proposal['preconditioner'])
    for j,i in enumerate(selected):A[i]+=F(proposal['corrections'][j])
    Ab=[(x-rho,x+rho) if i in selected else (x,x) for i,x in enumerate(A)];Bb=[(x,x) for x in B]
    assert certificate['A_observed_coordinate_boxes']==[list(map(str,x)) for x in Ab] and certificate['B_fixed_observed_coordinates']==list(map(str,B))
    assert A[1]-B[1]==2*eps and all(x[1]<y[0] for boxes in [Ab,Bb] for x,y in zip(boxes,boxes[1:]))
    constraints=[]
    for bits in [160,224]:
        for number,boxes in [(1,Ab),(2,Bb)]:
            name='E'+str(number)+'_'+str(bits)+'.json';roots=inputs[name]['positive_root_intervals']
            for i,(lo,hi) in enumerate(boxes):
                source_lo,source_hi=F(roots[i]['lo']),F(roots[i]['hi']);assert 0<source_lo<source_hi<F(39,2)
                allowed_lo,allowed_hi=source_hi-r,source_lo+r
                assert allowed_lo<=lo<=hi<=allowed_hi
                stored=next(x for x in certificate['coordinate_audit'] if x['precision_bits']==bits and x['input_member']==name and x['source_index']==i)
                margin=min(lo-allowed_lo,allowed_hi-hi)
                assert stored['source_interval']==[str(source_lo),str(source_hi)] and stored['observed_interval']==[str(lo),str(hi)] and stored['within_radius'] is True
                assert F(stored['error_margin'])==margin and F(stored['maximum_uniform_error'])==r-margin
                constraints.append({'input_member':name,'index':i,'left_inclusion_margin':str(lo-allowed_lo),'right_inclusion_margin':str(allowed_hi-hi)})
    assert len(certificate['coordinate_audit'])==len(constraints)==88
    R=[list(map(F,row)) for row in proposal['preconditioner']]
    return A,B,Ab,selected,R,rho,constraints
def complex_taylor(A,B,boxes,selected,R,rho,bits=640):
    ctx.prec=bits;alpha=arb(1)/25;F0=[];J0=[];second=[];target=[]
    for n in CENTERS:
        u=arb(n).log()
        def exponential(x):return acb(-alpha*x*x,u*x).exp()
        def d1(x):return 2*(acb(-2*alpha*x,u)*exponential(x)).real
        def d2(x):return 2*((acb(-2*alpha*x,u)**2-2*alpha)*exponential(x)).real
        fb=2*sum((exponential(av(x)) for x in B),acb(0)).real;target.append(fb)
        F0.append(2*sum((exponential(av(x)) for x in A),acb(0)).real-fb)
        J0.append([d1(av(A[j])) for j in selected])
        second.append([abs(d2(av(A[j])+arb(0,av(rho).upper()))) for j in selected])
    row_checks=[]
    for i in range(17):
        residual=sum((av(R[i][k])*F0[k] for k in range(17)),arb(0))
        center_defect=sum((abs(arb(int(i==j))-sum((av(R[i][k])*J0[k][j] for k in range(17)),arb(0))) for j in range(17)),arb(0))
        hessian_majorant=sum((abs(av(R[i][k]))*sum(second[k],arb(0)) for k in range(17)),arb(0))
        q=center_defect+av(rho)*hessian_majorant;self_map=abs(residual)+av(rho)*q
        assert q<1 and self_map<av(rho)
        row_checks.append({'index':i,'complex_preconditioned_residual':enc(residual),'center_inverse_defect':enc(center_defect),'weighted_second_derivative_majorant':enc(hessian_majorant),'contraction_majorant':enc(q),'self_map_bound':enc(self_map),'strict_margin':enc(av(rho)-self_map)})
    return {'precision_bits':bits,'rows':row_checks,'complex_F_center':[enc(x) for x in F0],'explicit_common_feature_vector':[enc(x) for x in target],'scope':'Complex exponential center derivatives plus second-derivative mean-value bounds control Jacobian variation. Scalar loops and exact rational R differ from the producer real trigonometric interval-Jacobian matrix product. Both still use FLINT ball arithmetic.'}
def audit_data(proposal,certificate,inputs):
    A,B,boxes,selected,R,rho,constraints=independent_parameters(proposal,certificate,inputs)
    determinant=modular_determinant(R);taylor=complex_taylor(A,B,boxes,selected,R,rho)
    x,u,a=s.symbols('x u a',real=True);g=2*s.exp(-a*x*x)*s.cos(u*x)
    first=2*s.exp(-a*x*x)*(-2*a*x*s.cos(u*x)-u*s.sin(u*x))
    second=2*s.exp(-a*x*x)*((4*a*a*x*x-2*a-u*u)*s.cos(u*x)+4*a*u*x*s.sin(u*x))
    assert s.simplify(s.diff(g,x)-first)==0 and s.simplify(s.diff(g,x,2)-second)==0
    assert [c['precision_bits'] for c in certificate['contraction_checks']]==[512,768]
    for c in certificate['contraction_checks']:
        assert len(c['rows'])==len(c['F_at_rational_center'])==len(c['fixed_common_feature_vector'])==17
        for i,row in enumerate(c['rows']):
            assert row['index']==i and from_ball(row['derivative_error_row_sum'])<1 and from_ball(row['self_map_bound'])<av(rho) and from_ball(row['strict_self_map_margin'])>0
            assert from_ball(c['F_at_rational_center'][i]).overlaps(from_ball(taylor['complex_F_center'][i]))
            assert from_ball(c['fixed_common_feature_vector'][i]).overlaps(from_ball(taylor['explicit_common_feature_vector'][i]))
    return {'status':'passed','uniform_coordinate_inclusions':constraints,'exact_scalar_inclusion_inequalities':176,'modular_preconditioner_nonsingularity':determinant,'independent_complex_Taylor_certificate':taylor,'symbolic_first_and_second_derivative_identities':'passed','full_lists_distinct_by_critical_coordinates':True,'scope':'An independent mathematical sufficient condition proves the same closed-box feature collision. The original report is additionally checked for coordinate/feature consistency; exact full producer replay checks its byte-level intermediate records. Shared FLINT arithmetic and inherited spectral premises remain explicit.'}
def run(proposal_path,certificate_path,input_archive,classification_path,arithmetic_path,source_path):
    proposal=json.loads(proposal_path.read_text());cert=json.loads(certificate_path.read_text());cl=json.loads(classification_path.read_text());source=json.loads(source_path.read_text())
    assert cl['status']==source['status']=='passed' and cl['complete_quartic_candidate_count']==2
    assert cert['inputs_sha256']=={p.name:sha(p) for p in [proposal_path,source_path,input_archive]} and proposal['input_sha256']==sha(source_path)
    with zipfile.ZipFile(input_archive) as z:inputs={n:json.loads(z.read(n)) for n in z.namelist()}
    checked=audit_data(proposal,cert,inputs);vectors,factorizations=arithmetic_vectors(arithmetic_path,source['columns']);ar=json.loads(arithmetic_path.read_text())
    labels={m['class_id']:next(k for k,v in ar['fields'].items() if sorted(v['quadratic_discriminants'])==m['quadratic_discriminants']) for m in cl['retained_models']}
    assert set(labels.values())=={'A','B'} and all(source['predictions'][k]==vectors[v] for k,v in labels.items())
    domains=[sorted({v[j] for v in vectors.values()}) for j in range(604)];assert len(factorizations)==1128 and sum(len(d)==1 for d in domains)==456
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [proposal_path,certificate_path,input_archive,classification_path,arithmetic_path,source_path]},
            'independent_certificate_audit':checked,'heldout_class_mapping':labels,'independent_polynomial_factorizations':1128,'polynomial_factorizations':factorizations,'coefficient_comparisons':1208,
            'columns':source['columns'],'exact_common_feature_coefficient_domains':domains,'fixed_coefficients':456,'ambiguous_coefficients':148,'differing_targets':[c['n'] for c,d in zip(source['columns'],domains) if len(d)>1 and c['n']<=31],
            'scope':'Both actual fields realize the certified same finite feature vector; complete metadata classification excludes other fields, so coefficient domains are exact within this class. No moment, tail or infinite-spectrum identity is inferred.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['proposal','certificate','inputs','classification','arithmetic','source','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.proposal,a.certificate,a.inputs,a.classification,a.arithmetic,a.source);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':'passed','coordinate_inclusions':176,'symbolic_derivatives':2,'modular_determinant':r['independent_certificate_audit']['modular_preconditioner_nonsingularity']['determinant_mod_prime'],'factorizations':1128,'fixed_coefficients':456,'ambiguous_coefficients':148}))
