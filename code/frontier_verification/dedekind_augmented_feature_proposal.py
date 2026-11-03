"""Propose augmented finite-feature collisions and square Jacobian inverses."""
import argparse, hashlib, json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.linalg import qr

CENTERS = [2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31]
FEATURES = [{'kind':'gaussian','center':n,'a':'1/25'} for n in CENTERS] + [
    {'kind':'rational_moment','numerator':3,'offset':'9/4'},
    {'kind':'gaussian','center':37,'a':'1/25'},
    {'kind':'gaussian','center':2,'a':'1/24'},
    {'kind':'gaussian','center':41,'a':'1/25'},
    {'kind':'gaussian','center':43,'a':'1/25'}]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def number(value):
    q=F(value); return mp.mpf(q.numerator)/q.denominator
def kernel(spec,x,derivative=False):
    if spec['kind']=='rational_moment':
        d=number(spec['offset'])+x*x
        return -2*spec['numerator']*x/d**2 if derivative else spec['numerator']/d
    a=number(spec['a']); u=mp.log(spec['center']); e=2*mp.exp(-a*x*x)
    return e*(-2*a*x*mp.cos(u*x)-u*mp.sin(u*x)) if derivative else e*mp.cos(u*x)
def exported(matrix): return [[mp.nstr(matrix[i,j],170) for j in range(matrix.cols)] for i in range(matrix.rows)]
def propose_case(common,specs,epsilon):
    n=len(specs); allowed=[i for i in range(22) if i!=1]
    Jall=mp.matrix([[kernel(s,x,True) for x in common] for s in specs])
    _,_,pivots=qr(np.array([[float(Jall[k,i]) for i in allowed] for k in range(n)]),pivoting=True,mode='economic')
    selected=[allowed[int(i)] for i in pivots[:n]]
    J0=mp.matrix([[Jall[k,i] for i in selected] for k in range(n)]); R0=J0**-1
    tangent=2*R0*mp.matrix([Jall[k,1] for k in range(n)])
    A=list(common); B=list(common); A[1]+=number(epsilon); B[1]-=number(epsilon); w=mp.matrix([0]*n); history=[]
    def evaluate(values):
        obs=list(A)
        for j,i in enumerate(selected): obs[i]+=values[j]
        residual=mp.matrix([sum(kernel(s,x) for x in obs)-sum(kernel(s,x) for x in B) for s in specs])
        jac=mp.matrix([[kernel(s,obs[i],True) for i in selected] for s in specs])
        return obs,residual,jac
    result={'dimension':n,'features':specs,'selected_A_variable_indices':selected,
            'center_preconditioner':exported(R0),'linear_split_sensitivity':[mp.nstr(x,170) for x in tangent],
            'maximum_linear_split_sensitivity':mp.nstr(max(abs(x) for x in tangent),170),'critical_split_epsilon':str(F(epsilon))}
    try:
        for iteration in range(35):
            obs,residual,jac=evaluate(w); norm=max(abs(x) for x in residual)
            history.append({'iteration':iteration,'maximum_residual':mp.nstr(norm,170),'maximum_correction':mp.nstr(max(abs(x) for x in w),170)})
            if norm<mp.mpf('1e-160'): break
            w-=mp.lu_solve(jac,residual)
        obs,residual,jac=evaluate(w); R=jac**-1; norm=max(abs(x) for x in residual)
        result.update(status='numerical_proposal_not_certified',numerically_converged=norm<mp.mpf('1e-160'),
            corrections=[mp.nstr(x,170) for x in w],preconditioner=exported(R),max_residual=mp.nstr(norm,170),
            max_correction=mp.nstr(max(abs(x) for x in w),170),iterations=history)
    except (ZeroDivisionError,ValueError,OverflowError) as error:
        result.update(status='numerical_attempt_failed',error_type=type(error).__name__,error=str(error),iterations=history)
    return result
def run(source,epsilon,dps=220):
    assert dps>=200; mp.mp.dps=dps
    data=json.loads(source.read_text()); assert data['status']=='passed'
    m=next(x for x in data['matching_cases'] if x['precision_bits']==224)
    c=[number(x) for x in m['common_observation']]
    cases=[propose_case(c,FEATURES[:n],epsilon) for n in [18,19,20,21]]
    full=mp.matrix([[kernel(s,x,True) for x in c] for s in FEATURES]); inverse=full**-1
    return {'status':'numerical_proposals_not_certified','source_sha256':sha(Path(__file__)),'input_sha256':sha(source),
            'mpmath_dps':dps,'export_significant_digits':170,'common_rational_coordinates':m['common_observation'],
            'source_threshold_lower':m['radius_lower'],'source_threshold_upper':m['radius_upper'],
            'radius':str(F(m['radius_upper'])-F(epsilon)),'cases':cases,
            'full_rank_proposal':{'dimension':22,'features':FEATURES,'preconditioner':exported(inverse),
                'maximum_inverse_row_sum':mp.nstr(max(sum(abs(inverse[i,j]) for j in range(22)) for i in range(22)),170)},
            'scope':'Newton, QR and approximate inverses are proposals only. Neither rank, exact collisions, coordinate feasibility nor local/global identification follows without separate certification.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--source',type=Path,required=True); p.add_argument('--epsilon',required=True); p.add_argument('--dps',type=int,default=220); p.add_argument('--output',type=Path,required=True); a=p.parse_args()
    r=run(a.source,a.epsilon,a.dps); a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'cases':[{k:c.get(k) for k in ['dimension','status','numerically_converged','max_correction','maximum_linear_split_sensitivity','error']} for c in r['cases']],'full_inverse_row_sum':r['full_rank_proposal']['maximum_inverse_row_sum']}))
