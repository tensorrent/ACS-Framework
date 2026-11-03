"""Rational dual certificates retaining common ordinate errors across measurements."""
import argparse,json,time,zipfile
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
from flint import arb,ctx
import dedekind_coupled_recovery as core
import dedekind_coupled_dual as dual
from dedekind_coupled_dual_refine import bound_box


def load(prior,top,bits,delta):
    with zipfile.ZipFile(prior.parent/'2026-09-13-coupled-delta'/'Measurements.zip') as z:raw=z.read('Measurements.json')
    with zipfile.ZipFile(prior/'Ordinate_Audits.zip') as z:ranges_raw=z.read('Ranges_224.json')
    data=json.loads(raw);ranges=json.loads(ranges_raw)
    audit=json.loads((prior/'Ordinate_Audit.json').read_text())
    assert audit['status']=='passed' and audit['input_sha256']==core.sha(raw)
    assert audit['results_sha256']['Ranges_224.json']==core.sha(ranges_raw)
    case=next(c for c in ranges['cases'] if c['additional_radius']==delta and c['settings']['top']==top
              and c['method']=='stationary' and c['policy']=='retained_prefix')
    rows=[]
    for height in [220,600,1000,1500,2000]:
        if height>top:continue
        powers,base,settings=core.prepare(data,height,bits,delta)
        bound=next(b for b in ranges['bounds'] if b['additional_radius']==delta and b['settings']['top']==height)
        metadata=bound['measurements_by_method']['stationary']
        for row,old in zip(base,metadata):
            assert row['metadata']['n']==old['n'] and row['metadata']['denominator']==old['denominator']
            row['R']=core.decode(old['R']);row['metadata']['R']=core.encode(row['R']);row['metadata']['range_method']='stationary'
            rows.append(row)
    domains=[r['candidates'] for r in case['domains']]
    assert len(domains)==len(powers)==604 and len(rows)==case['measurement_count']
    return data,powers,rows,domains,{'measurement_input_sha256':core.sha(raw),'prior_ranges_sha256':core.sha(ranges_raw),
       'prior_audit_sha256':core.sha((prior/'Ordinate_Audit.json').read_bytes()),'seed_case':case,
       'seed_domains_sha256':core.sha(core.canonical(domains))}


def hp(a,u,t):return (-a*t*t).exp()*(-2*a*t*(u*t).cos()-u*(u*t).sin())
def hpp(a,u,t):return (-a*t*t).exp()*((4*a*a*t*t-2*a-u*u)*(u*t).cos()+4*a*u*t*(u*t).sin())


def shared_basis(data,rows,top,bits,delta):
    ctx.prec=bits;radius=arb(delta)
    selected=[r for r in data['roots'] if F(r['hi'])<top]
    boxes=[arb(r['lo']).union(arb(r['hi']))+arb(0,radius.upper()) for r in selected]
    centers=[b.mid() for b in boxes];radii=[b.rad() for b in boxes]
    assert all(b.lower()>0 and b.upper()<top for b in boxes)
    basis=[];start=time.monotonic()
    for index,row in enumerate(rows):
        m=row['metadata'];height=m['height'];a=arb(1)/m['denominator'];u=arb(m['n']).log();A=core.decode(m['scale'])
        coefficients=[];finite=arb(0);remainder=arb(0);used=0
        for source,box,t,r in zip(selected,boxes,centers,radii):
            if F(source['hi'])>=height:coefficients.append(arb(0));continue
            assert box.upper()<height
            finite+=2*(-a*t*t).exp()*(u*t).cos()
            coefficients.append(2*A*r*hp(a,u,t))
            remainder+=A*r*r*hpp(a,u,box).abs_upper();used+=1
        center=A*(arb(m['pole'])+arb(m['discriminant_term'])+arb(m['gamma'])-finite)
        zero=core.decode(m['zero_error']);error=zero+remainder
        item={'center':center,'error':error,'remainder':remainder,'zero_error':zero,'J':coefficients}
        item['metadata']={'measurement_index':index,'height':height,'n':m['n'],'denominator':m['denominator'],
           'roots_used':used,'center':core.encode(center),'zero_error':core.encode(zero),'taylor_remainder':core.encode(remainder),
           'linear_error':core.encode(error),'J_sha256':core.sha(core.canonical([core.encode(v) for v in coefficients]))}
        basis.append(item)
        if (index+1)%91==0:print(json.dumps({'event':'shared_basis','rows':index+1,'roots':len(boxes),'elapsed_seconds':time.monotonic()-start}),flush=True)
    return basis,{'root_boxes_sha256':core.sha(core.canonical([core.encode(b) for b in boxes])),
       'roots':len(boxes),'basis':[b['metadata'] for b in basis]}


def shared_bound(rows,basis,column,sign,alpha,domains):
    assert sign in [-1,1]
    vector=[arb(0) for _ in domains];noise=[arb(0) for _ in basis[0]['J']]
    center=arb(0);tail=arb(0);individual_noise=arb(0)
    for index,value in enumerate(alpha):
        if not value:continue
        scalar=arb(str(value));absolute=abs(scalar);b=basis[index];row=rows[index]
        center+=scalar*b['center'];tail+=absolute*b['error']
        if value<0:tail+=(-scalar)*row['B']
        vector=[v+scalar*w for v,w in zip(vector,row['weights'])]
        noise=[v+scalar*j for v,j in zip(noise,b['J'])]
        individual_noise+=absolute*sum((j.abs_upper() for j in b['J']),arb(0))
    shared_error=sum((v.abs_upper() for v in noise),arb(0))
    residual=[(arb(sign) if k==column else arb(0))-v for k,v in enumerate(vector)]
    support=sum((max((d[0]*v).upper(),(d[-1]*v).upper()) for v,d in zip(residual,domains)),arb(0))
    upper=center+tail+shared_error+support
    return {'weighted_center':core.encode(center),'zero_taylor_prime_allowance':core.encode(tail),
       'shared_ordinate_allowance':core.encode(shared_error),'separate_ordinate_allowance':core.encode(individual_noise),
       'residual_support_bound':core.encode(support),'objective_upper_bound':core.encode(upper),
       'coefficient_vector_sha256':core.sha(core.canonical([core.encode(v) for v in vector])),
       'shared_noise_vector_sha256':core.sha(core.canonical([core.encode(v) for v in noise]))}


def run(prior,bits,top,delta,modes,targets,max_rounds):
    data,powers,rows,seeds,provenance=load(prior,top,bits,delta);ctx.prec=bits
    W=np.array([[float(w) for w in row['weights']] for row in rows])
    matrix,rhs=dual.inequalities(rows)
    marginal_matrix=sparse.csr_matrix(np.array([[float(v) for v in r] for r in matrix]))
    marginal_rhs=np.array([float(v) for v in rhs]);basis=None;basis_metadata=None
    if 'shared' in modes:
        basis,basis_metadata=shared_basis(data,rows,top,bits,delta)
        J=np.array([[float(j) for j in b['J']] for b in basis])
        plus=sparse.hstack([sparse.csr_matrix(W),sparse.csr_matrix(J)],format='csr')
        shared_matrix=sparse.vstack([plus,-plus],format='csr')
        shared_rhs=np.array([float((b['center']+b['error']).upper()) for b in basis]+
                            [float((-b['center']+b['error']+r['B']).upper()) for b,r in zip(basis,rows)])
    reports=[]
    for mode in modes:
        domains=[list(d) for d in seeds];rounds=[];start=time.monotonic()
        for round_number in range(1,max_rounds+1):
            old=[list(d) for d in domains];checks=[];changes=[]
            for column,(n,p,k) in enumerate(powers):
                if n>361 or len(old[column])==1 or (targets and n not in targets):continue
                certificates=[]
                for sign in [-1,1]:
                    extra=len(basis[0]['J']) if mode=='shared' else 0
                    objective=np.zeros(len(powers)+extra);objective[column]=-sign
                    proposal=linprog(objective,A_ub=shared_matrix if mode=='shared' else marginal_matrix,
                        b_ub=shared_rhs if mode=='shared' else marginal_rhs,
                        bounds=[(d[0],d[-1]) for d in old]+[(-1,1)]*extra,method='highs',
                        options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9,'time_limit':90})
                    size=2*len(rows);lambdas=[F(round(max(0.,-float(v))*10**9),10**9) for v in proposal.ineqlin.marginals] if proposal.success else [F(0)]*size
                    if mode=='shared':
                        alpha=[lambdas[i]-lambdas[len(rows)+i] for i in range(len(rows))]
                        proof=shared_bound(rows,basis,column,sign,alpha,old)
                        multipliers=[[i,str(v)] for i,v in enumerate(alpha) if v]
                    else:
                        proof=bound_box(matrix,rhs,column,sign,lambdas,old)
                        multipliers=[[i,str(v)] for i,v in enumerate(lambdas) if v]
                    certificates.append({'sign':sign,'solver_status':int(proposal.status),'solver_message':proposal.message,
                         'solver_objective':float(proposal.fun) if proposal.success else None,'multipliers':multipliers,**proof})
                after=[v for v in old[column] if all(not arb(c['sign']*v)>core.decode(c['objective_upper_bound']).upper() for c in certificates)]
                assert after,('Certified objective bounds have no candidate',mode,n)
                checked={'column':column,'n':n,'before':old[column],'after':after,'certificates':certificates};checks.append(checked)
                if after!=old[column]:changes.append(checked);domains[column]=after
                print(json.dumps({'event':'dual_target','mode':mode,'round':round_number,'n':n,'before':old[column],'after':after,
                    'solver_statuses':[c['solver_status'] for c in certificates],'elapsed_seconds':time.monotonic()-start}),flush=True)
            rounds.append({'round':round_number,'prior_domains_sha256':core.sha(core.canonical(old)),
                'checks':checks,'changed_targets':len(changes),'remaining_domains_sha256':core.sha(core.canonical(domains))})
            if not changes:break
        reports.append({'mode':mode,'rounds':rounds,'domains':[{'n':n,'prime':p,'power':k,'candidates':d} for (n,p,k),d in zip(powers,domains)],
           'unique_targets':sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361),
           'stabilized_within_requested_targets':not rounds[-1]['changed_targets'],'elapsed_seconds':time.monotonic()-start})
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'precision_bits':bits,'height':top,
        'additional_radius':delta,'requested_targets':targets,'max_rounds':max_rounds,'modes':modes,'provenance':provenance,
        'measurement_metadata_sha256':core.sha(core.canonical([r['metadata'] for r in rows])),
        'shared_basis':basis_metadata,'cases':reports,
        'scope':'Previously certified stationary-prefix coefficient domains seed both routes. Marginal duals use existing row ranges. Shared duals use common normalized ordinate displacements, per-row interval Taylor remainders and inherited unconditional zero/prime tails. Float LP results only propose rational multipliers; complete interval objectives decide candidate retention.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prior',type=Path,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True);p.add_argument('--top',type=int,default=2000)
    p.add_argument('--delta',default='5e-3');p.add_argument('--modes',nargs='+',choices=['marginal','shared'],default=['marginal','shared'])
    p.add_argument('--targets',nargs='*',type=int,default=[]);p.add_argument('--max-rounds',type=int,default=12)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=run(a.prior,a.precision,a.top,a.delta,a.modes,a.targets,a.max_rounds)
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'counts':{r['mode']:r['unique_targets'] for r in result['cases']}}))
