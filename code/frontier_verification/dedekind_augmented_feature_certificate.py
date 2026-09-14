"""Certify augmented collisions, Jacobian ranks, and a local injectivity neighborhood."""
import argparse, hashlib, json
from fractions import Fraction as F
from pathlib import Path
from flint import arb, arb_mat, ctx
from dedekind_augmented_feature_proposal import FEATURES
from dedekind_feature_certificate import coordinate_audit

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def av(x):
    q=F(x); return arb(q.numerator)/arb(q.denominator)
def enc(x): return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def kernel(spec,x,derivative=False):
    if spec['kind']=='rational_moment':
        d=av(spec['offset'])+x*x
        return -2*spec['numerator']*x/d**2 if derivative else spec['numerator']/d
    a=av(spec['a']);u=arb(spec['center']).log();e=2*(-a*x*x).exp()
    return e*(-2*a*x*(u*x).cos()-u*(u*x).sin()) if derivative else e*(u*x).cos()
def contract(n):
    return {'source_cutoff':'39/2','source_population':22,'source_selection':'complete_positive_prefix_before_coordinate_errors',
            'coordinate_errors':'independent_absolute_bounds','entries_and_multiplicity':'preserved','post_noise_window_censoring':False,
            'released_features':FEATURES[:n],'released_raw_coordinates':False,'released_cumulative_counts':False,'included_unknown_tail':False}
def parameters(p,case,source,rho):
    m=next(x for x in source['matching_cases'] if x['precision_bits']==224);n=case['dimension']
    assert n in [18,19,20,21] and case['features']==FEATURES[:n]
    assert case['status']=='numerical_proposal_not_certified' and case['numerically_converged'] is True
    assert p['common_rational_coordinates']==m['common_observation'] and p['source_threshold_lower']==m['radius_lower'] and p['source_threshold_upper']==m['radius_upper']
    c=list(map(F,p['common_rational_coordinates']));eps=F(case['critical_split_epsilon']);r=F(p['radius']);rho=F(rho)
    assert len(c)==22 and eps>0 and rho>0 and 0<r==F(m['radius_upper'])-eps<F(m['radius_lower'])
    selected=case['selected_A_variable_indices'];assert len(selected)==len(set(selected))==n and all(type(i) is int and i!=1 and 0<=i<22 for i in selected)
    assert len(case['corrections'])==n and len(case['preconditioner'])==n and all(len(row)==n for row in case['preconditioner'])
    A=list(c);B=list(c);A[1]+=eps;B[1]-=eps
    for j,i in enumerate(selected): A[i]+=F(case['corrections'][j])
    Ab=[(x-rho,x+rho) if i in selected else (x,x) for i,x in enumerate(A)];Bb=[(x,x) for x in B]
    assert all(x[1]<y[0] for boxes in [Ab,Bb] for x,y in zip(boxes,boxes[1:]))
    return {'n':n,'A':A,'B':B,'boxes_A':Ab,'boxes_B':Bb,'radius':r,'rho':rho,'epsilon':eps,'selected':selected,'R':[list(map(F,row)) for row in case['preconditioner']]}
def derivative_bound(specs,coordinates,selected,R,radius,bits):
    ctx.prec=bits;n=len(specs);rho=av(radius)
    X=[av(coordinates[i])+arb(0,rho.upper()) for i in selected]
    J=arb_mat([[kernel(s,x,True) for x in X] for s in specs]);rmat=arb_mat([[av(x) for x in row] for row in R])
    defect=arb_mat([[int(i==j) for j in range(n)] for i in range(n)])-rmat*J
    rows=[sum((abs(defect[i,j]) for j in range(n)),arb(0)) for i in range(n)]
    return rows,rmat,J
def collision_case(p,case,source,inputs,rho):
    par=parameters(p,case,source,rho);records=coordinate_audit(par,source,inputs)
    assert all(x['within_radius'] for x in records)
    n=par['n'];checks=[]
    for bits in [640,896]:
        q,R,J=derivative_bound(case['features'],par['A'],par['selected'],par['R'],par['rho'],bits)
        determinant=R.det();assert determinant>0 or determinant<0
        target=[sum((kernel(s,av(x)) for x in par['B']),arb(0)) for s in case['features']]
        residual=arb_mat([[sum((kernel(s,av(x)) for x in par['A']),arb(0))-target[i]] for i,s in enumerate(case['features'])]);pre=R*residual;rows=[]
        for i in range(n):
            self_map=abs(pre[i,0])+av(par['rho'])*q[i]
            assert q[i]<1 and self_map<av(par['rho'])
            rows.append({'index':i,'derivative_defect_row_sum':enc(q[i]),'preconditioned_residual':enc(pre[i,0]),'self_map_bound':enc(self_map),'strict_margin':enc(av(par['rho'])-self_map)})
        checks.append({'precision_bits':bits,'determinant':enc(determinant),'rows':rows,'F_center':[enc(residual[i,0]) for i in range(n)],'fixed_common_feature_vector':[enc(x) for x in target],
                       'maximum_contraction_bound_display':max(float(x.upper()) for x in q)})
    h=F(next(x for x in source['matching_cases'] if x['precision_bits']==224)['rational_height'])
    counts=[sum(hi<h for lo,hi in par['boxes_A']),sum(lo<h for lo,hi in par['boxes_A']),sum(x<h for x in par['B'])];assert counts==[1,1,2]
    return {'status':'passed','dimension':n,'contract':contract(n),'critical_split_epsilon':str(par['epsilon']),'radius':str(par['radius']),
            'strict_improvement_below_L':str(F(p['source_threshold_lower'])-par['radius']),'correction_box_radius':str(par['rho']),
            'selected_A_variable_indices':par['selected'],'A_observed_coordinate_boxes':[list(map(str,x)) for x in par['boxes_A']],
            'B_fixed_observed_coordinates':list(map(str,par['B'])),'coordinate_audit':records,'contraction_checks':checks,
            'interior_counts':{'height':str(h),'A_envelope':counts[:2],'B':counts[2]}}
def rank_and_injectivity(p):
    c=list(map(F,p['common_rational_coordinates']));ranks=[]
    for case in p['cases']:
        n=case['dimension'];R=[list(map(F,row)) for row in case['center_preconditioner']]
        assert len(R)==n and all(len(row)==n for row in R)
        qs,_,_=derivative_bound(FEATURES[:n],c,case['selected_A_variable_indices'],R,F(0),896)
        assert all(q<1 for q in qs)
        ranks.append({'dimension':n,'selected_columns':case['selected_A_variable_indices'],'defect_row_sums':[enc(q) for q in qs],'square_minor_invertible':True})
    full=p['full_rank_proposal'];assert full['dimension']==22 and full['features']==FEATURES
    R=[list(map(F,row)) for row in full['preconditioner']];assert len(R)==22 and all(len(row)==22 for row in R)
    Rnorm=max(sum(abs(x) for x in row) for row in R);tests=[]
    for radius in ['1e-12','1e-11','1e-10','1e-9','1e-8','1e-7']:
        checks=[]
        for bits in [640,896]:
            qs,_,_=derivative_bound(FEATURES,c,list(range(22)),R,F(radius),bits)
            checks.append({'precision_bits':bits,'defect_row_sums':[enc(q) for q in qs],
                           'all_rows_below_half':all(q<F(1,2) for q in qs),'all_rows_below_one':all(q<1 for q in qs),
                           'maximum_defect_display':max(float(q.upper()) for q in qs)})
        tests.append({'coordinate_box_radius':str(F(radius)),'checks':checks})
    chosen=next(x for x in reversed(tests) if all(c['all_rows_below_half'] for c in x['checks']))
    return {'status':'passed','rank_minor_checks':ranks,'features':FEATURES,'full_dimension':22,'neighborhood_center':list(map(str,c)),
            'radius_tests':tests,'certified_neighborhood_radius':chosen['coordinate_box_radius'],'uniform_derivative_defect_bound':'1/2',
            'exact_preconditioner_infinity_norm':str(Rnorm),'inverse_Lipschitz_bound':str(2*Rnorm),
            'scope':'For any x,y in this convex closed coordinate box, the componentwise mean-value/integral argument gives ||(x-y)-R(Phi(x)-Phi(y))||_infinity <= (1/2)||x-y||_infinity. Hence Phi is injective there and ||x-y||_infinity <= 2||R||_infinity ||Phi(x)-Phi(y)||_infinity. This is local, not global identification over all admissible observations.'}
def run(proposal,source,inputs,rho='1e-120'):
    p=json.loads(proposal.read_text());s=json.loads(source.read_text());assert s['status']=='passed' and p['input_sha256']==sha(source)
    assert [x['dimension'] for x in p['cases']]==[18,19,20,21]
    collisions=[collision_case(p,c,s,inputs,rho) for c in p['cases']];local=rank_and_injectivity(p)
    c=list(map(F,p['common_rational_coordinates']));eta=F(local['certified_neighborhood_radius'])
    for case in collisions:
        distance=max([abs(F(x)-c[i]) for i,b in enumerate(case['A_observed_coordinate_boxes']) for x in b]+[abs(F(x)-c[i]) for i,x in enumerate(case['B_fixed_observed_coordinates'])])
        case['maximum_distance_from_local_center']=str(distance);case['both_observations_inside_injective_22_feature_neighborhood']=distance<=eta
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in [proposal,source,inputs]},
            'collisions':collisions,'rank_and_local_injectivity':local,
            'scope':'Actual source-feasible collisions for 18 through 21 nested finite observables, with complete populations selected before noise, plus a separately certified local 22-observable injectivity neighborhood. No optimal radius, global injectivity or equality involving unknown tails is claimed.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['proposal','source','inputs','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--box-radius',default='1e-120');a=p.parse_args();r=run(a.proposal,a.source,a.inputs,a.box_radius);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'collision_dimensions':[x['dimension'] for x in r['collisions']],'local_neighborhood_radius':r['rank_and_local_injectivity']['certified_neighborhood_radius'],'local_membership':[x['both_observations_inside_injective_22_feature_neighborhood'] for x in r['collisions']], 'radius_tests':[{ 'radius':x['coordinate_box_radius'],'q_display':x['checks'][0]['maximum_defect_display']} for x in r['rank_and_local_injectivity']['radius_tests']]}))
