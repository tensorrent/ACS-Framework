"""Certify actual finite-feature ambiguity by a rationally specified contraction box."""
import argparse,hashlib,json,zipfile
from fractions import Fraction as F
from pathlib import Path
from flint import arb,arb_mat,ctx

CENTERS=[2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31]
CONTRACT={'source_cutoff':'39/2','source_population':22,'source_selection':'complete_positive_prefix_before_coordinate_errors',
          'coordinate_errors':'independent_absolute_bounds','entries_and_multiplicity':'preserved','post_noise_window_censoring':False,
          'released_observable':'seventeen_finite_Gaussian_sums','gaussian_a':'1/25','normalization':2,'centers':CENTERS,
          'released_raw_coordinates':False,'released_cumulative_counts':False,'released_moment':False,'included_unknown_tail':False}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def av(x):q=F(x);return arb(q.numerator)/arb(q.denominator)
def parameters(p,source,box_radius):
    assert source['status']=='passed';m=next(c for c in source['matching_cases'] if c['precision_bits']==224)
    assert p['centers']==CENTERS and p['gaussian_a']=='1/25' and type(p['critical_index']) is int and p['critical_index']==1
    assert p['common_rational_coordinates']==m['common_observation'] and p['source_threshold_lower']==m['radius_lower']
    c=list(map(F,p['common_rational_coordinates']));assert len(c)==22
    eps,r,rho=map(F,[p['critical_split_epsilon'],p['radius'],box_radius]);assert eps>0 and rho>0 and 0<r==F(m['radius_upper'])-eps<F(m['radius_lower'])
    selected=p['selected_A_variable_indices'];assert len(selected)==len(set(selected))==17 and all(type(i) is int and 0<=i<22 and i!=1 for i in selected)
    corrections=list(map(F,p['corrections']));assert len(corrections)==17
    R=[list(map(F,row)) for row in p['preconditioner']];assert len(R)==17 and all(len(row)==17 for row in R)
    A=list(c);B=list(c);A[1]+=eps;B[1]-=eps
    for j,i in enumerate(selected):A[i]+=corrections[j]
    boxes_A=[(x-rho,x+rho) if i in selected else (x,x) for i,x in enumerate(A)];boxes_B=[(x,x) for x in B]
    assert all(lo<=hi for lo,hi in boxes_A+boxes_B)
    for boxes in [boxes_A,boxes_B]:assert all(x[1]<y[0] for x,y in zip(boxes,boxes[1:]))
    assert A[1]-B[1]==2*eps>0
    return {'m':m,'epsilon':eps,'radius':r,'rho':rho,'selected':selected,'A':A,'B':B,'boxes_A':boxes_A,'boxes_B':boxes_B,'R':R}
def coordinate_audit(parameters,source,input_archive):
    records=[];r=parameters['radius'];metadata={'degree':4,'discriminant':576,'real_places':0,'complex_places':2}
    with zipfile.ZipFile(input_archive) as z:
        expected={'E'+str(i)+'_'+str(b)+'.json' for b in [160,224] for i in [1,2]};assert set(z.namelist())==expected
        for bits in [160,224]:
            m=next(c for c in source['matching_cases'] if c['precision_bits']==bits);assert m['population_sizes']==[22,22] and len(m['pairs'])==22
            for number,label,boxes in [(1,'A',parameters['boxes_A']),(2,'B',parameters['boxes_B'])]:
                name='E'+str(number)+'_'+str(bits)+'.json';raw=z.read(name);data=json.loads(raw)
                assert hashlib.sha256(raw).hexdigest()==source['inputs_sha256'][name]
                assert set(data)==set(metadata)|{'top','positive_root_intervals'} and {k:data[k] for k in metadata}==metadata and data['top']=='39/2'
                roots=data['positive_root_intervals'];assert len(roots)==22
                for i,(observed_lo,observed_hi) in enumerate(boxes):
                    slo,shi=[F(roots[i][k]) for k in ['lo','hi']];assert [slo,shi]==list(map(F,m['pairs'][i][label+'_interval']))
                    assert 0<slo<shi<F(39,2)
                    cost=max(abs(x-y) for x in [slo,shi] for y in [observed_lo,observed_hi]);margin=r-cost
                    records.append({'precision_bits':bits,'input_member':name,'source_index':i,'source_interval':[str(slo),str(shi)],'observed_interval':[str(observed_lo),str(observed_hi)],'maximum_uniform_error':str(cost),'error_margin':str(margin),'within_radius':margin>=0})
    return records
def contraction(parameters,bits):
    ctx.prec=bits;alpha=arb(1)/25;us=[arb(n).log() for n in CENTERS];rho=parameters['rho'];A,B=parameters['A'],parameters['B'];selected=parameters['selected']
    def feature(x,u):return 2*(-alpha*x*x).exp()*(u*x).cos()
    def derivative(x,u):return 2*(-alpha*x*x).exp()*(-2*alpha*x*(u*x).cos()-u*(u*x).sin())
    target=[sum((feature(av(x),u) for x in B),arb(0)) for u in us]
    F0=arb_mat([[sum((feature(av(x),u) for x in A),arb(0))-target[i]] for i,u in enumerate(us)])
    X=[av(A[i])+arb(0,av(rho).upper()) for i in selected]
    J=arb_mat([[derivative(x,u) for x in X] for u in us]);R=arb_mat([[av(x) for x in row] for row in parameters['R']])
    determinant=R.det();assert determinant>0 or determinant<0
    E=arb_mat([[int(i==j) for j in range(17)] for i in range(17)])-R*J;Fbar=R*F0;rows=[]
    for i in range(17):
        row_sum=sum((abs(E[i,j]) for j in range(17)),arb(0));bound=abs(Fbar[i,0])+av(rho)*row_sum
        assert row_sum<1 and bound<av(rho)
        rows.append({'index':i,'preconditioned_residual':enc(Fbar[i,0]),'derivative_error_row_sum':enc(row_sum),'self_map_bound':enc(bound),'strict_self_map_margin':enc(av(rho)-bound)})
    return {'precision_bits':bits,'preconditioner_determinant':enc(determinant),'F_at_rational_center':[enc(F0[i,0]) for i in range(17)],'fixed_common_feature_vector':[enc(x) for x in target],'rows':rows,
            'contraction_bound_approx_display':max(float(sum((abs(E[i,j]) for j in range(17)),arb(0)).upper()) for i in range(17))}
def run(proposal_path,source_path,input_archive,box_radius):
    p=json.loads(proposal_path.read_text());source=json.loads(source_path.read_text());assert p['input_sha256']==sha(source_path)
    par=parameters(p,source,box_radius);coordinates=coordinate_audit(par,source,input_archive)
    violations=[x for x in coordinates if not x['within_radius']]
    result={'status':'rejected_coordinate_bounds' if violations else 'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in [proposal_path,source_path,input_archive]},
            'contract':CONTRACT,'radius':str(par['radius']),'full_point_list_threshold_lower':par['m']['radius_lower'],'strict_improvement_below_lower':str(F(par['m']['radius_lower'])-par['radius']),
            'critical_split_epsilon':str(par['epsilon']),'correction_box_radius':str(par['rho']),'selected_A_variable_indices':par['selected'],
            'A_observed_coordinate_boxes':[list(map(str,x)) for x in par['boxes_A']],'B_fixed_observed_coordinates':list(map(str,par['B'])),
            'coordinate_audit':coordinates,'coordinate_violations':violations,'contraction_checks':[],
            'scope':'Exact rational source-to-observation bounds and real Arb derivative enclosures. A passed result proves existence within the stated finite-feature contract by the documented contraction argument; independent methods and source premises are audited separately. It does not identify an optimal feature threshold or assert equality of moments, unknown tails or infinite explicit-formula measurements.'}
    if not violations:result['contraction_checks']=[contraction(par,bits) for bits in [512,768]]
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['proposal','source','inputs','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--box-radius',default='1e-100');a=p.parse_args();r=run(a.proposal,a.source,a.inputs,a.box_radius);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'coordinate_violations':len(r['coordinate_violations']),'strict_improvement':r['strict_improvement_below_lower'],'contraction_bounds':[x['contraction_bound_approx_display'] for x in r['contraction_checks']]}));raise SystemExit(0 if r['status']=='passed' else 1)
