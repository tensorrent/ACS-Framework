"""Certify weighted Taylor regions and exact componentwise inverse bounds."""
import argparse,hashlib,json
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from flint import arb,acb,arb_mat,ctx
from dedekind_augmented_feature_audit import SPECS

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def av(x):
    q=F(x);return arb(q.numerator)/arb(q.denominator)
def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def derivatives(spec,x,order):
    if spec['kind']=='rational_moment':
        z=acb(arb(3)/2,x);return [2*(acb(0,-1)**n*factorial(n)/z**(n+1)).real for n in range(order+1)]
    a=av(spec['a']);u=arb(spec['center']).log();v=acb(-2*a*x,u);e=acb(-a*x*x,u*x).exp();poly=[acb(1),v]
    for n in range(1,order):poly.append(v*poly[n]-2*a*n*poly[n-1])
    return [2*(p*e).real for p in poly[:order+1]]
def parameters(p,exploration):
    assert p['full_rank_proposal']['dimension']==22 and p['full_rank_proposal']['features']==SPECS
    c=list(map(F,p['common_rational_coordinates']));R=[list(map(F,row)) for row in p['full_rank_proposal']['preconditioner']]
    assert len(c)==len(R)==22 and all(len(row)==22 for row in R)
    candidate=next(x for x in exploration['radius_tests'] if F(x['radius'])==F(3,100) and x['derivative_Taylor_order']==6)
    w=list(map(F,candidate['positive_rational_weights']));assert len(w)==22 and all(x>0 for x in w)
    return c,R,w
def majorant(c,R,radius,bits):
    ctx.prec=bits;eta=av(radius);n=22;rmat=arb_mat([[av(x) for x in row] for row in R]);absR=arb_mat([[abs(rmat[i,j]) for j in range(n)] for i in range(n)])
    point=[[derivatives(spec,av(x),7) for x in c] for spec in SPECS]
    boxes=[av(x)+arb(0,eta.upper()) for x in c];highest=arb_mat([[abs(derivatives(spec,x,7)[7]) for x in boxes] for spec in SPECS])
    terms=[]
    for t in range(6):
        mat=rmat*arb_mat([[point[k][j][t+1] for j in range(n)] for k in range(n)])
        if t==0:mat=arb_mat([[int(i==j) for j in range(n)] for i in range(n)])-mat
        terms.append(arb_mat([[abs(mat[i,j]) for j in range(n)] for i in range(n)]))
    remainder=absR*highest*eta**6/factorial(6)
    B=terms[0]+sum((terms[t]*eta**t/factorial(t) for t in range(1,6)),arb_mat(n,n))+remainder
    return B,terms,remainder
def dyadic_upper(x,bits=40):
    man,exponent=map(int,x.upper().man_exp());q=F(man)*F(2)**exponent;scaled=q*2**bits
    return F(-(-scaled.numerator//scaled.denominator),2**bits)
def solve_exact(matrix,rhs):
    n=len(rhs);a=[list(row)+[v] for row,v in zip(matrix,rhs)]
    for i in range(n):
        pivot=next(j for j in range(i,n) if a[j][i]);a[i],a[pivot]=a[pivot],a[i]
        value=a[i][i];a[i]=[x/value for x in a[i]]
        for j in range(n):
            if j!=i:
                value=a[j][i];a[j]=[x-value*y for x,y in zip(a[j],a[i])]
    return [row[-1] for row in a]
def certify(p,exploration,radius):
    c,R,w=parameters(p,exploration);radius=F(radius);assert radius in [F(1,100),F(3,100)]
    assert c[0]>radius and all(x+radius<y-radius for x,y in zip(c,c[1:]))
    checks=[];matrices=[]
    for bits in [768,1024]:
        B,terms,remainder=majorant(c,R,radius,bits);rows=[sum((B[i,j]*av(w[j]) for j in range(22)),arb(0))/av(w[i]) for i in range(22)]
        assert all(x<arb(1)/2 for x in rows)
        checks.append({'precision_bits':bits,'majorant_matrix':[[enc(B[i,j]) for j in range(22)] for i in range(22)],
            'weighted_defect_rows':[enc(x) for x in rows],'remainder_matrix':[[enc(remainder[i,j]) for j in range(22)] for i in range(22)],
            'center_coefficient_row_maxima_display':[max(float(sum((abs(M[i,j]) for j in range(22)),arb(0)).upper()) for i in range(22)) for M in terms],
            'maximum_weighted_defect_display':max(float(x.upper()) for x in rows)})
        matrices.append(B)
    upper=[[max(dyadic_upper(B[i,j]) for B in matrices) for j in range(22)] for i in range(22)]
    assert all(x>=0 for row in upper for x in row)
    exact_q=[sum(upper[i][j]*w[j] for j in range(22))/w[i] for i in range(22)];assert max(exact_q)<F(1,2)
    rownorms=[sum(abs(x) for x in row) for row in R]
    h=solve_exact([[F(int(i==j))-upper[i][j] for j in range(22)] for i in range(22)],rownorms)
    assert all(x>0 for x in h) and all(h[i]-sum(upper[i][j]*h[j] for j in range(22))==rownorms[i] for i in range(22))
    L,U=F(p['source_threshold_lower']),F(p['source_threshold_upper']);root_error=U-F('1e-8');assert L-root_error>0
    weightedC=2*max(w)*max(rownorms[i]/w[i] for i in range(22))
    return {'status':'passed','radius':str(radius),'domain':'standard_coordinate_cube_centered_at_c','dimension':22,'features':SPECS,
        'derivative_Taylor_order':6,'point_derivative_orders':list(range(1,7)),'remainder_derivative_order':7,'remainder_factorial':720,
        'positive_rational_weights':list(map(str,w)),'uniform_weighted_defect_bound':'1/2','checks':checks,
        'exact_nonnegative_majorant':[[str(x) for x in row] for row in upper],'dyadic_rounding_bits':40,'exact_weighted_row_sums':list(map(str,exact_q)),
        'exact_preconditioner_row_norms':list(map(str,rownorms)),'exact_componentwise_inverse_bounds':list(map(str,h)),
        'componentwise_supersolution_identity':'h = abs(R)*ones + B_upper*h','critical_index':1,'critical_inverse_bound':str(h[1]),
        'standard_infinity_inverse_bound':str(max(h)),'coarser_weighted_norm_inverse_bound':str(weightedC),
        'source_threshold_lower':str(L),'root_coordinate_error_radius':str(root_error),'source_critical_separation_lower':str(2*(L-root_error)),
        'uniform_feature_error_identification_guarantee_strictly_below':str((L-root_error)/h[1]),
        'critical_inverse_bound_display':float(h[1]),'feature_error_guarantee_display':float((L-root_error)/h[1]),
        'scope':'The weighted Taylor majorant gives injectivity on the stated standard coordinate cube. Exact nonnegative supersolutions give componentwise inverse stability. Within the complete inherited two-field class, root errors at most r<L and both observations in this cube imply feature separation at least 2(L-r)/h[1]; independent feature errors strictly below (L-r)/h[1] cannot erase field identity. No global result outside this cube or optimal noise threshold is claimed.'}
def run(proposal,exploration):
    p=json.loads(proposal.read_text());e=json.loads(exploration.read_text());assert e['inputs_sha256'][proposal.name]==sha(proposal)
    c,R,w=parameters(p,e);regions=[certify(p,e,r) for r in ['1/100','3/100']]
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{x.name:sha(x) for x in [proposal,exploration]},
        'common_rational_coordinates':list(map(str,c)),'regions':regions,'scope':'Validated higher-order weighted bounds and exact componentwise stability supersolutions, with all local and observation-contract premises explicit.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['proposal','exploration','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=run(a.proposal,a.exploration);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'regions':[{k:x[k] for k in ['radius','critical_inverse_bound_display','feature_error_guarantee_display']} for x in r['regions']]}))
