"""Audit weighted regions using real polynomial jets and positive-series inverse bounds."""
import argparse,hashlib,json,zipfile
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import sympy as s
from flint import arb,ctx
from dedekind_augmented_feature_audit import input_geometry

SPECS=[{'kind':'gaussian','center':n,'a':'1/25'} for n in [2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31]]+[
    {'kind':'rational_moment','numerator':3,'offset':'9/4'},{'kind':'gaussian','center':37,'a':'1/25'},
    {'kind':'gaussian','center':2,'a':'1/24'},{'kind':'gaussian','center':41,'a':'1/25'},{'kind':'gaussian','center':43,'a':'1/25'}]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def av(x):
    q=F(x);return arb(q.numerator)/arb(q.denominator)
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def add(p,q):return [(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q)))]
def scale(p,a):return [a*x for x in p]
def deriv(p):return [i*p[i] for i in range(1,len(p))] or [0]
def evaluate(p,x):
    value=0
    for coefficient in reversed(p):value=value*x+coefficient
    return value
def gaussian_polys(a,u,order):
    P=[[1]];Q=[[0]]
    for n in range(order):
        P.append(add(add(deriv(P[n]),[0]+scale(P[n],-2*a)),scale(Q[n],u)))
        Q.append(add(add(deriv(Q[n]),[0]+scale(Q[n],-2*a)),scale(P[n],-u)))
    return P,Q
def moment_polys(d,order):
    P=[[3]]
    for n in range(order):P.append(add(add(scale(deriv(P[n]),d),[0,0]+deriv(P[n])),[0]+scale(P[n],-2*(n+1))))
    return P
def symbolic():
    x,a,u,d=s.symbols('x a u d',real=True);P,Q=gaussian_polys(a,u,7);M=moment_polys(d,7)
    for n in range(8):
        g=2*s.exp(-a*x*x)*(evaluate(P[n],x)*s.cos(u*x)+evaluate(Q[n],x)*s.sin(u*x))
        assert s.simplify(s.diff(2*s.exp(-a*x*x)*s.cos(u*x),x,n)-g)==0
        assert s.factor(s.diff(3/(d+x*x),x,n)-evaluate(M[n],x)/(d+x*x)**(n+1))==0
    return {'orders':list(range(8)),'Gaussian_real_polynomial_identities':'passed','moment_rational_polynomial_identities':'passed'}
def ball(x):return arb(arb(tuple(x['mid'])),arb(tuple(x['rad'])))
def upper48(x):
    m,e=map(int,x.upper().man_exp());q=F(m)*F(2)**e*2**48
    return F(-(-q.numerator//q.denominator),2**48)
def real_majorant(c,R,radius,bits):
    ctx.prec=bits;point=[];highest=[]
    for spec in SPECS:
        if spec['kind']=='rational_moment':
            M=moment_polys(F(9,4),7)
            def jets(x):return [evaluate([av(t) for t in M[n]],x)/(av('9/4')+x*x)**(n+1) for n in range(8)]
        else:
            a=av(spec['a']);u=arb(spec['center']).log();P,Q=gaussian_polys(a,u,7)
            def jets(x):return [2*(-a*x*x).exp()*(evaluate(P[n],x)*(u*x).cos()+evaluate(Q[n],x)*(u*x).sin()) for n in range(8)]
        point.append([jets(av(x)) for x in c]);highest.append([abs(jets(av(x)+arb(0,av(radius).upper()))[7]) for x in c])
    B=[]
    for i in range(22):
        row=[]
        for j in range(22):
            value=abs(arb(int(i==j))-sum((av(R[i][k])*point[k][j][1] for k in range(22)),arb(0)))
            for t in range(1,6):value+=av(radius)**t/factorial(t)*abs(sum((av(R[i][k])*point[k][j][t+1] for k in range(22)),arb(0)))
            value+=av(radius)**6/factorial(6)*sum((abs(av(R[i][k]))*highest[k][j] for k in range(22)),arb(0))
            row.append(value)
        B.append(row)
    return B
def positive_series(B,r,w):
    # A positive Neumann partial sum plus a weighted geometric tail; no linear solver.
    term=list(r);h=list(r);M=max(x/y for x,y in zip(r,w))
    for _ in range(32):
        term=[sum(B[i][j]*term[j] for j in range(22)) for i in range(22)];h=[x+y for x,y in zip(h,term)]
    h=[x+M*y/F(2)**32 for x,y in zip(h,w)]
    assert all(x>0 for x in h) and all(h[i]>=r[i]+sum(B[i][j]*h[j] for j in range(22)) for i in range(22))
    return h
def audit_data(p,exploration,certificate,inputs,prior_certificates):
    c,L,U=input_geometry(inputs);assert certificate['status']=='passed' and p['full_rank_proposal']['dimension']==22 and p['full_rank_proposal']['features']==SPECS
    assert list(map(F,p['common_rational_coordinates']))==list(map(F,certificate['common_rational_coordinates']))==c and F(p['source_threshold_lower'])==L and F(p['source_threshold_upper'])==U
    R=[list(map(F,row)) for row in p['full_rank_proposal']['preconditioner']];assert len(R)==22 and all(len(row)==22 for row in R)
    candidate=next(x for x in exploration['radius_tests'] if F(x['radius'])==F(3,100) and x['derivative_Taylor_order']==6);w=list(map(F,candidate['positive_rational_weights']))
    assert len(w)==22 and all(x>0 for x in w);rownorms=[sum(abs(x) for x in row) for row in R]
    assert [x['radius'] for x in certificate['regions']]==['1/100','3/100'];results=[]
    for region in certificate['regions']:
        eta=F(region['radius']);assert region['status']=='passed' and region['domain']=='standard_coordinate_cube_centered_at_c' and region['features']==SPECS and region['dimension']==22
        assert region['derivative_Taylor_order']==6 and region['point_derivative_orders']==list(range(1,7)) and region['remainder_derivative_order']==7 and region['remainder_factorial']==720
        assert region['positive_rational_weights']==list(map(str,w)) and region['uniform_weighted_defect_bound']=='1/2' and region['dyadic_rounding_bits']==40
        assert c[0]>eta and all(x+eta<y-eta for x,y in zip(c,c[1:]))
        Bstored=[list(map(F,row)) for row in region['exact_nonnegative_majorant']];hstored=list(map(F,region['exact_componentwise_inverse_bounds']))
        assert len(Bstored)==len(hstored)==22 and all(len(row)==22 and all(x>=0 for x in row) for row in Bstored)
        assert list(map(F,region['exact_preconditioner_row_norms']))==rownorms and all(x>0 for x in hstored)
        qs=[sum(Bstored[i][j]*w[j] for j in range(22))/w[i] for i in range(22)]
        assert max(qs)<F(1,2) and list(map(F,region['exact_weighted_row_sums']))==qs
        assert all(hstored[i]-sum(Bstored[i][j]*hstored[j] for j in range(22))==rownorms[i] for i in range(22))
        assert region['critical_index']==1 and F(region['critical_inverse_bound'])==hstored[1] and F(region['standard_infinity_inverse_bound'])==max(hstored)
        assert F(region['coarser_weighted_norm_inverse_bound'])==2*max(w)*max(rownorms[i]/w[i] for i in range(22))
        r=U-F('1e-8');assert F(region['root_coordinate_error_radius'])==r and F(region['source_threshold_lower'])==L and F(region['source_critical_separation_lower'])==2*(L-r)>0
        assert F(region['uniform_feature_error_identification_guarantee_strictly_below'])==(L-r)/hstored[1]
        assert [x['precision_bits'] for x in region['checks']]==[768,1024]
        for check in region['checks']:
            assert len(check['weighted_defect_rows'])==22 and all(ball(x)<arb(1)/2 for x in check['weighted_defect_rows'])
            assert len(check['majorant_matrix'])==22 and all(len(row)==22 for row in check['majorant_matrix'])
            assert all(av(Bstored[i][j])>=ball(check['majorant_matrix'][i][j]) for i in range(22) for j in range(22))
        independent=[];matrices=[]
        for bits in [896,1152]:
            B=real_majorant(c,R,eta,bits);q=[sum((B[i][j]*av(w[j]) for j in range(22)),arb(0))/av(w[i]) for i in range(22)]
            assert all(x<arb(1)/2 for x in q);matrices.append(B)
            independent.append({'precision_bits':bits,'weighted_rows':[enc(x) for x in q],'maximum_bound_display':max(float(x.upper()) for x in q)})
        Bown=[[max(upper48(B[i][j]) for B in matrices) for j in range(22)] for i in range(22)]
        assert all(x>=0 for row in Bown for x in row) and all(sum(Bown[i][j]*w[j] for j in range(22))<w[i]/2 for i in range(22))
        hown=positive_series(Bown,rownorms,w);assert hown[1]<=hstored[1]
        containment=[]
        for suffix,old in prior_certificates.items():
            assert old['status']=='passed'
            for case in old['collisions']:
                distance=max([abs(F(x)-c[i]) for i,box in enumerate(case['A_observed_coordinate_boxes']) for x in box]+[abs(F(x)-c[i]) for i,x in enumerate(case['B_fixed_observed_coordinates'])])
                containment.append({'source_case':suffix,'dimension':case['dimension'],'maximum_distance':str(distance),'inside_region':distance<=eta})
        assert len(containment)==12
        if eta==F(3,100):assert all(x['inside_region'] for x in containment)
        results.append({'radius':str(eta),'independent_real_polynomial_bounds':independent,'independent_48_bit_majorant':[[str(x) for x in row] for row in Bown],
            'positive_series_terms':33,'geometric_tail_bound':'M*w/2^32','independent_componentwise_supersolution':list(map(str,hown)),
            'independent_critical_bound_no_larger_than_claimed':True,'independent_critical_bound_display':float(hown[1]),
            'preceding_witness_containment':containment,'contained_preceding_witnesses':sum(x['inside_region'] for x in containment)})
    return {'status':'passed','symbolic_derivative_identities':symbolic(),'regions':results,
        'scope':'Real derivative polynomials, scalar Taylor estimates and a positive Neumann series with an exact geometric tail independently support the regions and claimed critical-coordinate bounds. Exact rational inequalities reconstruct source gaps and witness containment. Shared FLINT and the stated finite-source/class premises remain explicit.'}
def run(anchor,exploration,certificate,inputs,prior):
    p=json.loads(anchor.read_text());e=json.loads(exploration.read_text());cert=json.loads(certificate.read_text());assert e['inputs_sha256'][anchor.name]==sha(anchor) and cert['inputs_sha256']=={x.name:sha(x) for x in [anchor,exploration]}
    with zipfile.ZipFile(inputs) as z:data={n:json.loads(z.read(n)) for n in z.namelist()}
    paths=[anchor,exploration,certificate,inputs];old={}
    for suffix in ['Enlarged','Small','Local']:
        path=prior/f'Augmented_Certificate_{suffix}_v2.json';paths.append(path);old[suffix]=json.loads(path.read_text())
    result=audit_data(p,e,cert,data,old);result.update(source_sha256=sha(Path(__file__)),inputs_sha256={x.name:sha(x) for x in paths});return result
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['anchor','exploration','certificate','inputs','prior','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a.anchor,a.exploration,a.certificate,a.inputs,a.prior);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'regions':[{k:x[k] for k in ['radius','independent_critical_bound_display','contained_preceding_witnesses']} for x in r['regions']]}))
