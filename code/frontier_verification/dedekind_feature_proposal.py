"""Propose finite Gaussian feature collisions on a seventeen-variable local slice."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.linalg import qr

CENTERS=[2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def propose(m,epsilon,dps):
    assert dps>=160;mp.mp.dps=dps
    def number(x):q=F(x);return mp.mpf(q.numerator)/q.denominator
    c=[number(x) for x in m['common_observation']];eps=F(epsilon);assert 0<eps<F(m['radius_lower'])
    a=mp.mpf(1)/25;u=[mp.log(n) for n in CENTERS]
    def fun(x,t):return 2*mp.exp(-a*x*x)*mp.cos(t*x)
    def deriv(x,t):return 2*mp.exp(-a*x*x)*(-2*a*x*mp.cos(t*x)-t*mp.sin(t*x))
    allowed=[i for i in range(22) if i!=1]
    _,_,pivots=qr(np.array([[float(deriv(c[i],t)) for i in allowed] for t in u]),pivoting=True,mode='economic')
    selected=[allowed[int(i)] for i in pivots[:17]]
    A=list(c);B=list(c);A[1]+=number(eps);B[1]-=number(eps);w=mp.matrix([0]*17);history=[]
    def evaluate(values):
        Aobs=list(A)
        for j,i in enumerate(selected):Aobs[i]+=values[j]
        residual=mp.matrix([sum(fun(x,t) for x in Aobs)-sum(fun(x,t) for x in B) for t in u])
        jac=mp.matrix([[deriv(Aobs[i],t) for i in selected] for t in u])
        return Aobs,residual,jac
    for iteration in range(30):
        Aobs,residual,jac=evaluate(w);norm=max(abs(x) for x in residual)
        history.append({'iteration':iteration,'maximum_residual':mp.nstr(norm,140),'maximum_correction':mp.nstr(max(abs(x) for x in w),140)})
        if norm<mp.mpf('1e-130'):break
        w-=mp.lu_solve(jac,residual)
    Aobs,residual,jac=evaluate(w);R=jac**-1;norm=max(abs(x) for x in residual)
    return {'status':'numerical_proposal_not_certified','centers':CENTERS,'gaussian_a':'1/25','critical_index':1,
            'critical_split_epsilon':str(eps),'common_rational_coordinates':m['common_observation'],'selected_A_variable_indices':selected,
            'radius':str(F(m['radius_upper'])-eps),'source_threshold_lower':m['radius_lower'],'proposed_radius_below_L':F(m['radius_upper'])-eps<F(m['radius_lower']),
            'mpmath_dps':dps,'export_significant_digits':140,'iterations':history,'numerically_converged':norm<mp.mpf('1e-130'),
            'corrections':[mp.nstr(x,140) for x in w],'preconditioner':[[mp.nstr(R[i,j],140) for j in range(17)] for i in range(17)],
            'max_residual':mp.nstr(norm,140),'max_correction':mp.nstr(max(abs(x) for x in w),140),
            'scope':'High-precision Newton and QR only propose a slice center and rational preconditioner. They do not certify root existence, acquisition feasibility or an optimal feature threshold. Coordinate and fixed-point audits are required.'}
def run(source,epsilon,dps):
    data=json.loads(source.read_text());assert data['status']=='passed';m=next(c for c in data['matching_cases'] if c['precision_bits']==224)
    p=propose(m,epsilon,dps);p.update(source_sha256=sha(Path(__file__)),input_sha256=sha(source));return p
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--epsilon',required=True);p.add_argument('--dps',type=int,default=180);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.source,a.epsilon,a.dps);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','critical_split_epsilon','numerically_converged','max_residual','max_correction']}))
