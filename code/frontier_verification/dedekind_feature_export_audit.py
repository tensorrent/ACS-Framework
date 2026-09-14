"""Independently reconstruct exported Newton data via complex exponential derivatives."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json
from flint import arb,acb,ctx

def enc(x):return {'mid':list(map(int,x.mid().man_exp())),'rad':list(map(int,x.rad().man_exp()))}
def av(x):x=Q(x);return arb(x.numerator)/arb(x.denominator)
def run(proposal,source):
    p=json.loads(proposal.read_text());data=json.loads(source.read_text());m=next(c for c in data['matching_cases'] if c['precision_bits']==224)
    assert p['common_rational_coordinates']==m['common_observation'] and p['critical_index']==1 and p['gaussian_a']=='1/25'
    assert p['centers']==[2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31]
    ctx.prec=640;alpha=arb(1)/25;A=list(map(Q,p['common_rational_coordinates']));B=list(A);eps=Q(p['critical_split_epsilon'])
    A[1]+=eps;B[1]-=eps;variables=p['selected_A_variable_indices'];assert len(variables)==len(set(variables))==17 and 1 not in variables
    for j,i in enumerate(variables):A[i]+=Q(p['corrections'][j])
    F=[];J=[]
    for n in p['centers']:
        u=arb(n).log()
        def exponential(x):return acb(-alpha*av(x)**2,u*av(x)).exp()
        F.append(2*(sum((exponential(x) for x in A),acb(0))-sum((exponential(x) for x in B),acb(0))).real)
        J.append([2*(acb(-2*alpha*av(A[i]),u)*exponential(A[i])).real for i in variables])
    R=[[av(x) for x in row] for row in p['preconditioner']];defects=[]
    for i in range(17):
        row=sum((abs(arb(int(i==j))-sum((R[i][k]*J[k][j] for k in range(17)),arb(0))) for j in range(17)),arb(0));defects.append(row)
    norm=F[0].abs_upper()
    for x in F[1:]:norm=norm.max(x.abs_upper())
    residual_consistent=bool(abs(av(p['max_residual'])-norm)<av('1e-100'))
    inverse_consistent=all(bool(x<av('1e-90')) for x in defects)
    return {'status':'passed' if residual_consistent and inverse_consistent else 'failed','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'inputs_sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [proposal,source]},
            'precision_bits':640,'complex_exponential_F':[enc(x) for x in F],'exported_center_residual_upper':enc(norm),'reported_residual':p['max_residual'],'residual_report_consistent_with_exported_center':residual_consistent,
            'inverse_defect_row_sums':[enc(x) for x in defects],'preconditioner_consistent_with_exported_center':inverse_consistent,
            'scope':'A complex-exponential implementation independently reconstructs F and J at the rational exported correction center, applying the correction once. Tiny decimal-export effects are allowed by stated1e-100/1e-90 tolerances. This audits numerical exports; an existence proof additionally requires a closed-box interval self-map certificate.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--proposal',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.proposal,a.source);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','residual_report_consistent_with_exported_center','preconditioner_consistent_with_exported_center']}));raise SystemExit(0 if r['status']=='passed' else 1)
