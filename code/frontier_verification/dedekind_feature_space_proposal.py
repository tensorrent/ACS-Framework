"""Propose two actual-source observations around a common 22-feature release."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
from dedekind_augmented_feature_proposal import FEATURES,kernel,number

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def solve(c,R,signs,tau,field_sign):
    n=22;t=number(tau);v=mp.matrix(signs);w=field_sign*t*mp.matrix([[number(x) for x in row] for row in R])*v
    target=mp.matrix([sum(kernel(spec,x) for x in c)+field_sign*t*signs[i] for i,spec in enumerate(FEATURES)])
    history=[]
    def evaluate(w):
        y=[x+w[i] for i,x in enumerate(c)];f=mp.matrix([sum(kernel(spec,x) for x in y)-target[i] for i,spec in enumerate(FEATURES)])
        J=mp.matrix([[kernel(spec,x,True) for x in y] for spec in FEATURES]);return y,f,J
    for iteration in range(30):
        y,f,J=evaluate(w);res=max(abs(x) for x in f);history.append({'iteration':iteration,'maximum_residual':mp.nstr(res,170)})
        if res<mp.mpf('1e-160'):break
        w-=mp.lu_solve(J,f)
    y,f,J=evaluate(w);inverse=J**-1
    return {'field_sign':field_sign,'numerically_converged':max(abs(x) for x in f)<mp.mpf('1e-160'),
        'corrections':[mp.nstr(x,170) for x in w],'preconditioner':[[mp.nstr(inverse[i,j],170) for j in range(n)] for i in range(n)],
        'iterations':history,'maximum_residual':mp.nstr(max(abs(x) for x in f),170),
        'maximum_displacement':mp.nstr(max(abs(x) for x in w),170),'critical_coordinate_margin_proposal':mp.nstr(field_sign*w[1]-mp.mpf('1e-8'),170)}
def run(source):
    mp.mp.dps=220;p=json.loads(source.read_text());assert p['full_rank_proposal']['features']==FEATURES
    c=list(map(number,p['common_rational_coordinates']));R=[list(map(F,row)) for row in p['full_rank_proposal']['preconditioner']]
    signs=[1 if x>0 else -1 if x<0 else 0 for x in R[1]];assert all(abs(x)==1 for x in signs)
    cases=[]
    for tau in ['2.1e-10','2e-10','1.98e-10','1.97e-10']:
        cases.append({'feature_error_bound':str(F(tau)),'A':solve(c,R,signs,tau,1),'B':solve(c,R,signs,tau,-1)})
    return {'status':'numerical_proposals_not_certified','source_sha256':sha(Path(__file__)),'input_sha256':sha(source),'mpmath_dps':220,'export_significant_digits':170,
        'features':FEATURES,'common_root_center':p['common_rational_coordinates'],'common_feature_release':'The exact 22-feature vector Phi(c) of the given rational center c.',
        'feature_direction':signs,'root_coordinate_error_radius':str(F(p['source_threshold_upper'])-F('1e-8')),
        'source_threshold_lower':p['source_threshold_lower'],'critical_required_shift':'1/100000000','cases':cases,
        'scope':'Full 22-variable Newton solves propose Phi(y_A)=Phi(c)+tau*v and Phi(y_B)=Phi(c)-tau*v. Rational source-to-observation feasibility, exact feature equalities and neighborhood containment require separate certificates. The signs are a direction proposal, not a global optimality proof.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.source);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'cases':[{'tau':c['feature_error_bound'],'A_critical_margin':c['A']['critical_coordinate_margin_proposal'],'B_critical_margin':c['B']['critical_coordinate_margin_proposal'],'max_displacement':max(float(c[f]['maximum_displacement']) for f in ['A','B'])} for c in r['cases']]},indent=2))
