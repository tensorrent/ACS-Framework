"""Shared quadratic ordinate terms with interval cubic remainders and exact support."""
import argparse,json,time,zipfile
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
import dedekind_coupled_recovery as core
import dedekind_shared_ordinate as shared


def load(prior,bits):
    data,powers,rows,_,previous=shared.load(prior.parent/'2026-09-13-uncertainty-delta',2000,bits,'5e-3')
    with zipfile.ZipFile(prior/'Shared_Audits.zip') as z:raw=z.read('Shared_160.json')
    source=json.loads(raw);audit=json.loads((prior/'Shared_Audit.json').read_text())
    assert source['status']=='passed' and audit['status']=='passed'
    assert audit['results_sha256']['Shared_160.json']==core.sha(raw)
    seeds=[d['candidates'] for d in source['domains']]
    assert len(seeds)==604 and source['unique_targets']==81
    provenance={'shared_result_sha256':core.sha(raw),'shared_audit_sha256':core.sha((prior/'Shared_Audit.json').read_bytes()),
       'seed_domains_sha256':core.sha(core.canonical(seeds)),'seed_domains':source['domains'],'earlier_inputs':previous}
    return data,powers,rows,seeds,source,provenance


def third(a,u,t):
    return (-a*t*t).exp()*((-8*a*a*a*t*t*t+12*a*a*t+6*a*u*u*t)*(u*t).cos()
                          +(-12*a*a*u*t*t+6*a*u+u*u*u)*(u*t).sin())


def prepare(data,rows,bits):
    basis,metadata=shared.shared_basis(data,rows,2000,bits,'5e-3')
    radius=arb('5e-3');selected=[r for r in data['roots'] if F(r['hi'])<2000]
    boxes=[arb(r['lo']).union(arb(r['hi']))+arb(0,radius.upper()) for r in selected]
    assert core.sha(core.canonical([core.encode(b) for b in boxes]))==metadata['root_boxes_sha256']
    start=time.monotonic();new_metadata=[]
    for index,(row,b) in enumerate(zip(rows,basis)):
        m=row['metadata'];a=arb(1)/m['denominator'];u=arb(m['n']).log();A=core.decode(m['scale'])
        K=[];cubic=arb(0)
        for source,box in zip(selected,boxes):
            if F(source['hi'])>=m['height']:K.append(arb(0));continue
            t,r=box.mid(),box.rad();K.append(A*r*r*shared.hpp(a,u,t))
            cubic+=A*r*r*r*third(a,u,box).abs_upper()/3
        b['K']=K;b['cubic']=cubic;b['quadratic_error']=b['zero_error']+cubic
        new_metadata.append({**b['metadata'],'cubic_remainder':core.encode(cubic),
            'quadratic_error':core.encode(b['quadratic_error']),'K_sha256':core.sha(core.canonical([core.encode(k) for k in K]))})
        if (index+1)%91==0:print(json.dumps({'event':'quadratic_basis','rows':index+1,'elapsed_seconds':time.monotonic()-start}),flush=True)
    return basis,{**metadata,'basis':new_metadata}


def scalar_support(d,e):
    # Both selected endpoints are exact dyadics. Multiplication by 2 is exact,
    # so equality at D=2E safely falls into the endpoint branch.
    D=d.abs_upper();E=e.lower();assert D.rad()==0 and E.rad()==0
    if E>0 and D<2*E:
        value=D*D/(4*E);kind='interior_vertex'
    else:value=D-E;kind='endpoint'
    assert value>=0
    independent=D+max(arb(0),-E)
    return value,independent,kind


def combine(rows,basis,alpha):
    vector=[arb(0)]*len(rows[0]['weights']);noise=[arb(0)]*len(basis[0]['J']);curve=[arb(0)]*len(noise)
    center=arb(0);linear_tail=arb(0);quadratic_tail=arb(0)
    for i,value in enumerate(alpha):
        if not value:continue
        scalar=arb(str(value));absolute=abs(scalar);b=basis[i]
        center+=scalar*b['center'];linear_tail+=absolute*b['error'];quadratic_tail+=absolute*b['quadratic_error']
        if value<0:
            linear_tail+=(-scalar)*rows[i]['B'];quadratic_tail+=(-scalar)*rows[i]['B']
        vector=[v+scalar*w for v,w in zip(vector,rows[i]['weights'])]
        noise=[v+scalar*j for v,j in zip(noise,b['J'])]
        curve=[v+scalar*k for v,k in zip(curve,b['K'])]
    linear_allowance=sum((j.abs_upper() for j in noise),arb(0))
    allowance=arb(0);independent=arb(0);vertices=0;support_rows=[]
    for d,e in zip(noise,curve):
        value,separate,kind=scalar_support(d,e);allowance+=value;independent+=separate;vertices+=kind=='interior_vertex'
        support_rows.append({'linear':core.encode(d),'quadratic':core.encode(e),'support':core.encode(value),'kind':kind})
    metadata={'weighted_center':core.encode(center),'linear_tail_allowance':core.encode(linear_tail),
       'quadratic_tail_allowance':core.encode(quadratic_tail),'linear_ordinate_allowance':core.encode(linear_allowance),
       'independent_quadratic_allowance':core.encode(independent),'coupled_quadratic_allowance':core.encode(allowance),
       'interior_vertices':vertices,'endpoints':len(noise)-vertices,'root_support_sha256':core.sha(core.canonical(support_rows)),
       'coefficient_vector_sha256':core.sha(core.canonical([core.encode(v) for v in vector]))}
    return {'vector':vector,'noise':noise,'curve':curve,'center':center,'linear_tail':linear_tail,
       'quadratic_tail':quadratic_tail,'linear_allowance':linear_allowance,'independent_allowance':independent,'allowance':allowance,'metadata':metadata}


def objective(combination,column,sign,domains,mode):
    assert sign in [-1,1]
    residual=[(arb(sign) if i==column else arb(0))-v for i,v in enumerate(combination['vector'])]
    support=sum((max((d[0]*v).upper(),(d[-1]*v).upper()) for v,d in zip(residual,domains)),arb(0))
    tail=combination['linear_tail'] if mode=='linear' else combination['quadratic_tail']
    allowance=combination['linear_allowance'] if mode=='linear' else combination['independent_allowance'] if mode=='independent_quadratic' else combination['allowance']
    upper=combination['center']+tail+allowance+support
    return {'residual_support_bound':core.encode(support),'objective_upper_bound':core.encode(upper)}


def run(prior,bits,modes,max_rounds):
    data,powers,rows,seeds,source,provenance=load(prior,bits);ctx.prec=bits
    basis,metadata=prepare(data,rows,bits);proposals=[];combinations={}
    for step in source['rounds']:
        for check in step['checks']:
            if len(seeds[check['column']])==1:continue
            for certificate in check['certificates']:
                multipliers=certificate['multipliers'];key=core.sha(core.canonical(multipliers))
                if key not in combinations:
                    alpha=[F(0)]*len(rows)
                    for i,v in multipliers:alpha[i]=F(v)
                    combinations[key]=combine(rows,basis,alpha)
                proposals.append({'source_round':step['round'],'n':check['n'],'column':check['column'],
                   'sign':certificate['sign'],'multipliers':multipliers,'combination_sha256':key})
    reports=[]
    for mode in modes:
        domains=[list(d) for d in seeds];rounds=[]
        for number in range(1,max_rounds+1):
            old=[list(d) for d in domains];checks=[]
            for proposal in proposals:
                column=proposal['column']
                if len(old[column])==1:continue
                proof=objective(combinations[proposal['combination_sha256']],column,proposal['sign'],old,mode)
                after=[v for v in domains[column] if not arb(proposal['sign']*v)>core.decode(proof['objective_upper_bound']).upper()]
                assert after,('Validated quadratic bound has no candidate',mode,proposal['n'])
                checks.append({**proposal,'before':list(domains[column]),'after':after,**proof});domains[column]=after
            changes=sum(a!=b for a,b in zip(old,domains))
            rounds.append({'round':number,'prior_domains_sha256':core.sha(core.canonical(old)),'checks':checks,
                'changed_targets':changes,'remaining_domains_sha256':core.sha(core.canonical(domains))})
            if not changes:break
        reports.append({'mode':mode,'rounds':rounds,'domains':[{'n':n,'prime':p,'power':k,'candidates':d} for (n,p,k),d in zip(powers,domains)],
            'unique_targets':sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361),'stabilized':rounds[-1]['changed_targets']==0})
        print(json.dumps({'event':'frozen_multiplier_result','mode':mode,'unique_targets':reports[-1]['unique_targets'],'rounds':len(rounds)}),flush=True)
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'precision_bits':bits,
       'height':2000,'additional_radius':'5e-3','provenance':provenance,'basis':metadata,
       'proposals':proposals,'combinations':{k:v['metadata'] for k,v in combinations.items()},'cases':reports,
       'scope':'Frozen signed multipliers from the preceding shared-error checkpoint; all 81 certified domains seed each control independently. Cubic remainders are interval bounds. Coupled scalar support retains y squared, while an explicit control treats y and y squared independently. Surviving candidates are not certified feasible.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prior',type=Path,required=True)
    p.add_argument('--precision',type=int,choices=[160,224],required=True)
    p.add_argument('--modes',nargs='+',choices=['linear','independent_quadratic','quadratic'],default=['linear','independent_quadratic','quadratic'])
    p.add_argument('--max-rounds',type=int,default=8);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.prior,a.precision,a.modes,a.max_rounds);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'counts':{c['mode']:c['unique_targets'] for c in r['cases']}}))
