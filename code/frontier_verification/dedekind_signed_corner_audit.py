"""Independent real polynomials, Neumann bounds and determinant-ratio corner audit."""
import argparse, hashlib, json, zipfile
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from flint import arb, arb_mat, fmpq, fmpq_mat, ctx
from dedekind_weighted_region_audit_v2 import SPECS, gaussian_polys, moment_polys, evaluate, positive_series
from dedekind_augmented_feature_audit import input_geometry, modular_det
from dedekind_aggregate_integer_audit import arithmetic_vectors

ROOT=Path(__file__).absolute().parents[2]
ANCHOR='docs/frontier/2026-09-14-aggregate-augmented-feature-delta/Augmented_Proposals_Local.json'
REGION='docs/frontier/2026-09-14-aggregate-weighted-feature-delta/Weighted_Region_Certificate.json'
OWN='docs/frontier/2026-09-14-aggregate-weighted-feature-delta/Independent_Weighted_Region_Audit_v2.json'
UPPER='docs/frontier/2026-09-14-aggregate-variable-noise-delta/Variable_Noise_Certificate.json'
SOURCE='docs/frontier/2026-09-14-aggregate-equal-population-delta'
CLASS='docs/frontier/2026-09-14-aggregate-classification-delta/Full_Quartic_Class.json'
ARITH='docs/frontier/2026-09-13-biquadratic-delta/Pair_Arithmetic.json'
N=22
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def av(x):
    q=F(x);return arb(q.numerator)/arb(q.denominator)
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def endpoints(x):
    assert set(x)=={'mid','rad'} and all(len(x[k])==2 and all(type(t) is int for t in x[k]) for k in x)
    m=F(x['mid'][0])*F(2)**x['mid'][1];r=F(x['rad'][0])*F(2)**x['rad'][1];assert r>=0
    return m-r,m+r
def sign(x):return 1 if x>0 else -1 if x<0 else 0
def interval_sign(lo,hi):return 1 if lo>0 else -1 if hi<0 else 0

def validate_exact(cert,anchor,region,upper):
    """Validate proof-premise bookkeeping without trusting displayed decimals."""
    assert cert['status']=='passed' and cert['matrix_family']=='product_of_closed_convex_hulls_of_coordinate_derivative_curves' and cert['secants_in_family'] is True
    assert cert['entire_bridge_Lean_formalized'] is False and cert['optimal_source_feasible_threshold_proved'] is False
    assert cert['contract']=={k:v for k,v in upper['contract'].items() if k!='common_release_type'}
    assert cert['contract']['features']==SPECS and cert['critical_index']==1
    c=list(map(F,anchor['common_rational_coordinates']));R=[list(map(F,r)) for r in anchor['full_rank_proposal']['preconditioner']]
    assert len(c)==len(R)==N and all(len(row)==N for row in R)
    assert cert['common_root_center']==list(map(str,c)) and anchor['full_rank_proposal']['features']==SPECS
    v=list(map(sign,R[1]));assert cert['critical_sign_vector']==v and all(abs(s)==1 for s in v)
    assert cert['modular_preconditioner']==modular_det(R)
    gap=F(anchor['source_threshold_lower'])-F(upper['contract']['root_coordinate_error_radius']);assert gap>0
    assert len(cert['signed_regions'])==2 and len(region['regions'])==2
    for record,reg in zip(cert['signed_regions'],region['regions']):
        assert record['radius']==reg['radius'];B=[list(map(F,r)) for r in reg['exact_nonnegative_majorant']];w=list(map(F,reg['positive_rational_weights']))
        assert all(x>=0 for r in B for x in r) and all(x>0 for x in w)
        assert all(sum(B[i][j]*w[j] for j in range(N))<w[i]/2 for i in range(N))
        row=list(map(F,record['positive_resolvent_critical_row']));d=list(map(F,record['resolvent_minus_identity_row']));h=list(map(F,record['signed_vector_supersolution']))
        assert len(row)==len(d)==len(h)==N and d==[row[i]-int(i==1) for i in range(N)] and all(x>=0 for x in d) and all(x>0 for x in h)
        assert all(sum(row[i]*(int(i==j)-B[i][j]) for i in range(N))==int(j==1) for j in range(N))
        u0=[sum(R[i][k]*v[k] for k in range(N)) for i in range(N)]
        assert record['signed_R_times_v']==list(map(str,u0))
        assert all(h[i]-sum(B[i][j]*h[j] for j in range(N))==abs(u0[i]) for i in range(N))
        deviations=[sum(d[i]*abs(R[i][k]) for i in range(N)) for k in range(N)]
        margins=[abs(R[1][k])-deviations[k] for k in range(N)]
        assert record['critical_inverse_row_deviation_bounds']==list(map(str,deviations)) and record['critical_inverse_row_sign_margins']==list(map(str,margins))
        assert record['unresolved_row_sign_indices']==[i for i,x in enumerate(margins) if x<=0]
        intervals=[(u0[i]-(h[i]-abs(u0[i])),u0[i]+(h[i]-abs(u0[i]))) for i in range(N)]
        assert record['inverse_direction_intervals']==[list(map(str,x)) for x in intervals]
        penalty=2*sum(max(F(0),-x) for x in margins);K=h[1]+penalty
        assert F(record['sign_flip_penalty'])==penalty and F(record['signed_uniform_inverse_bound'])==K
        assert K<F(record['previous_inverse_bound'])==F(reg['critical_inverse_bound'])
        assert F(record['signed_noise_guarantee_strictly_below'])==gap/K
    assert cert['signed_regions'][0]['unresolved_row_sign_indices']==[]
    assert cert['curvature_Taylor_orders']==list(range(2,8)) and cert['curvature_remainder_derivative_order']==8
    assert cert['curvature_remainder_power']==6 and cert['curvature_remainder_factorial']==720
    assert cert['first_replacement_order']==[i for i in range(N) if i!=12]
    assert cert['last_replacement_coordinate']==12 and cert['last_replacement_direction']==-1
    assert cert['last_direction_scope']=='face_with_other_21_columns_at_certified_endpoints'
    assert [x['precision_bits'] for x in cert['uniform_curvature_checks']]==[896,1152]
    all_directions=[]
    for check in cert['uniform_curvature_checks']:
        assert len(check['columns'])==N;directions=[]
        for j,col in enumerate(check['columns']):
            a=interval_sign(*endpoints(col['curvature_factor_interval']));assert a!=0 and col['curvature_sign']==a and col['coordinate']==j
            u=interval_sign(*map(F,cert['signed_regions'][0]['inverse_direction_intervals'][j]));assert col['inverse_direction_sign']==u
            assert col['endpoint_direction']==-a*u;directions.append(-a*u)
        assert [j for j,x in enumerate(directions) if x==0]==[12] and check['columns'][12]['curvature_sign']==-1
        all_directions.append(directions)
    assert all_directions[0]==all_directions[1];directions=all_directions[0]
    ref=[x+F(1,100)*s for x,s in zip(c,directions)];corner=list(ref);corner[12]=c[12]-F(1,100)
    assert [x['precision_bits'] for x in cert['corner_checks']]==[1024,1536]
    for check in cert['corner_checks']:
        assert check['face_reference_coordinates']==list(map(str,ref)) and check['corner_coordinates']==list(map(str,corner))
        assert endpoints(check['reference_direction_12'])[1]<0
        ds=interval_sign(*endpoints(check['reference_determinant']));assert ds!=0 and ds==interval_sign(*endpoints(check['corner_determinant']))
        assert len(check['corner_critical_inverse_row'])==N
        assert [interval_sign(*endpoints(x)) for x in check['corner_critical_inverse_row']]==v
        assert 0<endpoints(check['corner_norm'])[0]<=endpoints(check['corner_norm'])[1]<F(check['corner_norm_upper'])
    K=max(F(x['corner_norm_upper']) for x in cert['corner_checks']);assert F(cert['corner_uniform_inverse_bound'])==K<F(cert['signed_regions'][0]['signed_uniform_inverse_bound'])
    low=gap/K;high=F(upper['best_certified_tau_upper'])
    assert F(cert['uniform_identification_strictly_below'])==low and F(cert['inherited_ambiguity_upper_endpoint'])==high
    assert F(cert['previous_uniform_guarantee'])==F(upper['uniform_identification_below'])<low<high
    assert F(cert['upper_to_guarantee_ratio'])==high/low
    return c,R,v

def own_resolvent(R,B,w):
    assert all(x>=0 for r in B for x in r) and all(x>0 for x in w)
    assert all(sum(B[i][j]*w[j] for j in range(N))<w[i]/2 for i in range(N))
    C=fmpq_mat([[fmpq(str(F(int(i==j))-B[i][j])) for j in range(N)] for i in range(N)]).inv()
    row=[F(str(C[1,i])) for i in range(N)];d=[row[i]-int(i==1) for i in range(N)];assert all(x>=0 for x in d)
    assert all(sum(row[i]*(int(i==j)-B[i][j]) for i in range(N))==int(j==1) for j in range(N))
    v=list(map(sign,R[1]));u0=[sum(R[i][k]*v[k] for k in range(N)) for i in range(N)]
    h=positive_series(B,list(map(abs,u0)),w)
    assert all(h[i]>=abs(u0[i])+sum(B[i][j]*h[j] for j in range(N)) for i in range(N))
    margins=[abs(R[1][k])-sum(d[i]*abs(R[i][k]) for i in range(N)) for k in range(N)]
    intervals=[(u0[i]-(h[i]-abs(u0[i])),u0[i]+(h[i]-abs(u0[i]))) for i in range(N)]
    return row,d,h,margins,intervals

def real_functions():
    functions=[]
    for spec in SPECS:
        if spec['kind']=='rational_moment':
            polys=moment_polys(F(9,4),8)
            def fn(x,polys=polys):return [evaluate([av(t) for t in polys[n]],x)/(av('9/4')+x*x)**(n+1) for n in range(9)]
        else:
            a=av(spec['a']);u=arb(spec['center']).log();P,Q=gaussian_polys(a,u,8)
            def fn(x,a=a,u=u,P=P,Q=Q):return [2*(-a*x*x).exp()*(evaluate(P[n],x)*(u*x).cos()+evaluate(Q[n],x)*(u*x).sin()) for n in range(9)]
        functions.append(fn)
    return functions

def real_curvature(c,R,d,intervals,functions,expected):
    eta=av('1/100');point=[[fn(av(x)) for x in c] for fn in functions]
    high=[[abs(fn(av(x)+arb(0,eta.upper()))[8]) for x in c] for fn in functions];columns=[]
    for j in range(N):
        b0=[];rad=[]
        for i in range(N):
            co=[sum((av(R[i][k])*point[k][j][t+2] for k in range(N)),arb(0)) for t in range(6)]
            b0.append(co[0]);rad.append(sum((abs(co[t])*eta**t/factorial(t) for t in range(1,6)),arb(0))+eta**6/factorial(6)*sum((abs(av(R[i][k]))*high[k][j] for k in range(N)),arb(0)))
        perturb=sum((av(d[i])*(abs(b0[i])+rad[i]) for i in range(N)),arb(0))
        bound=b0[1]+arb(0,(rad[1]+perturb).upper());a=sign(bound);u=interval_sign(*intervals[j])
        assert a==expected[j]['curvature_sign']!=0 and u==expected[j]['inverse_direction_sign']
        columns.append({'coordinate':j,'real_curvature_factor':enc(bound),'curvature_sign':a,'inverse_direction_sign':u,'endpoint_direction':-a*u})
    return columns

def determinant_ratio(J, column, rhs):
    denominator=J.det();assert sign(denominator)!=0
    numerator=arb_mat([[rhs[i] if j==column else J[i,j] for j in range(N)] for i in range(N)]).det()
    return numerator/denominator,numerator,denominator

def run(certificate,root=ROOT):
    paths=[root/p for p in [ANCHOR,REGION,OWN,UPPER,SOURCE+'/Equal_Population_Inputs.zip',SOURCE+'/Equal_Population_Decoder.json',CLASS,ARITH]]
    cert=read(certificate);a,reg,own,upper=map(read,paths[:4]);c,R,v=validate_exact(cert,a,reg,upper)
    assert cert['inputs_sha256']=={p.name:sha(p) for p in [paths[0],paths[1],paths[3],paths[4]]}
    with zipfile.ZipFile(paths[4]) as z:data={n:json.loads(z.read(n)) for n in z.namelist()}
    cc,L,U=input_geometry(data);assert cc==c and L==F(a['source_threshold_lower']) and U==F(a['source_threshold_upper'])
    assert own['status']=='passed' and own['inputs_sha256'][paths[1].name]==sha(paths[1]);records=[];resolved=[]
    for i in range(2):
        assert own['regions'][i]['radius']==reg['regions'][i]['radius']
        B=[list(map(F,r)) for r in own['regions'][i]['independent_48_bit_majorant']];w=list(map(F,reg['regions'][i]['positive_rational_weights']))
        row,d,h,margins,intervals=own_resolvent(R,B,w);K=h[1]+2*sum(max(F(0),-x) for x in margins)
        assert K<=F(cert['signed_regions'][i]['signed_uniform_inverse_bound'])
        if i==0:assert all(x>0 for x in margins)
        records.append({'radius':reg['regions'][i]['radius'],'own_resolvent_row':list(map(str,row)),
            'positive_series_supersolution':list(map(str,h)),'own_sign_margins':list(map(str,margins)),
            'inverse_direction_intervals':[list(map(str,x)) for x in intervals],
            'own_signed_bound':str(K),'own_signed_bound_no_larger_than_claimed':True})
        resolved.append((d,intervals))
    checks=[]
    for bits in [896,1152]:
        ctx.prec=bits;fn=real_functions();d,intervals=resolved[0]
        cols=real_curvature(c,R,d,intervals,fn,cert['uniform_curvature_checks'][0]['columns'])
        y=list(map(F,cert['corner_checks'][0]['face_reference_coordinates']))
        J=arb_mat([[f(av(x))[1] for x in y] for f in fn]);u12,num,det=determinant_ratio(J,12,v);assert u12<0
        y[12]=c[12]-F(1,100);J=arb_mat([[f(av(x))[1] for x in y] for f in fn]);row=[];numerators=[]
        for k in range(N):
            # Solve J*x=e_k by replacing column 1. This yields inverse entry (1,k).
            x,numerator,denominator=determinant_ratio(J,1,[int(i==k) for i in range(N)])
            assert sign(x)==v[k];row.append(x);numerators.append(enc(numerator))
        K=sum(map(abs,row),arb(0));assert 0<K<av(cert['corner_uniform_inverse_bound']) and sign(det)==sign(denominator)
        checks.append({'precision_bits':bits,'columns':cols,'face_cramer_numerator':enc(num),'face_determinant':enc(det),
            'face_direction_12':enc(u12),'corner_cramer_numerators':numerators,'corner_determinant':enc(denominator),
            'corner_critical_inverse_row':[enc(x) for x in row],'corner_norm':enc(K),'corner_norm_display':float(K.mid()),
            'corner_bound_independently_verified':True})
    source,classification,arith=map(read,paths[5:]);assert source['status']==classification['status']=='passed' and classification['complete_quartic_candidate_count']==2
    vectors,factors=arithmetic_vectors(paths[7],source['columns'])
    labels={m['class_id']:next(k for k,v in arith['fields'].items() if sorted(v['quadratic_discriminants'])==m['quadratic_discriminants']) for m in classification['retained_models']}
    assert set(labels.values())=={'A','B'} and all(source['predictions'][k]==vectors[v] for k,v in labels.items())
    domains=[sorted({v[j] for v in vectors.values()}) for j in range(604)];assert len(factors)==1128 and sum(len(x)==1 for x in domains)==456
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in paths+[certificate]},
        'independent_signed_regions':records,'checks':checks,'arithmetic_class_mapping':labels,'polynomial_factorizations':factors,
        'factorization_count':1128,'coefficient_comparisons':1208,'fixed_coefficients':456,'ambiguous_coefficients':148,
        'uniform_identification_strictly_below':cert['uniform_identification_strictly_below'],
        'scope':'Real derivative polynomials through order 8 and an independently certified 48-bit majorant support the same column-family signs. Exact FLINT rational inversion plus finite positive-series bounds differ from primary rational elimination. Cramer determinant ratios independently verify the face sign and all 22 corner inverse-row entries; no interval matrix inverse is used for those point checks. Both routes share FLINT and inherited source premises. The full convex/analytic bridge remains a written proof with separately compiled generic lemmas.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.certificate);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'factorizations':r['factorization_count'],'corner_norms':[x['corner_norm_display'] for x in r['checks']]}))
