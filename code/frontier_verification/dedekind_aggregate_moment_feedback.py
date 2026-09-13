"""Alternate noisy local domains with frozen-dual residual supports."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import encode,decode
from dedekind_coupled_dual import inequalities
from dedekind_coefficient_recovery import local_models

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def coefficient(model,k):return sum(f for e,f in model if k%f==0)

def run(measurements,proposals,previous_proposals,audit_path):
    ctx.prec=256;m=json.loads(measurements.read_text());p=json.loads(proposals.read_text());old=json.loads(previous_proposals.read_text());audit=json.loads(audit_path.read_text())
    assert audit['status']=='passed'
    for path in [measurements,proposals,previous_proposals]:assert audit['inputs_sha256'][path.name]==sha(path)
    columns=m['columns'];models=sorted(local_models(4,False)+local_models(4,True));groups={prime:[i for i,c in enumerate(columns) if c['prime']==prime] for prime in sorted({c['prime'] for c in columns})}
    matrices=[]
    for obs in range(2):
        rows=[{'weights':[decode(w) for w in r['weights']],'R':decode(r['observations'][obs]['unwidened']),'B':decode(r['prime_tail'])} for r in m['rows']]
        matrices.append(inequalities(rows))
    prepared=[]
    for index,row in enumerate(audit['objective_replays']):
        candidate=next(c for c in (p if row['multiplier_source']=='joint_adapted' else old)['cases'] if all(c[k]==row[k] for k in ['observation_index','radius','column','sign']))
        A,b=matrices[row['observation_index']];vector=[arb(0) for _ in columns];beta=arb(0)
        for j,value in candidate['multipliers']:
            scalar=arb(value);assert F(value)>=0;beta+=scalar*b[j];vector=[v+scalar*a for v,a in zip(vector,A[j])]
        residual=[(arb(row['sign']) if k==row['column'] else arb(0))-v for k,v in enumerate(vector)]
        prepared.append({'index':index,'row':row,'weighted_rhs':beta,'residual':residual})
    cases=[]
    for obs in range(2):
        for radius in p['radii']:
            selected=[c for c in prepared if c['row']['observation_index']==obs and c['row']['radius']==radius]
            for method in ['separate','coupled']:
                initial=[list(range(5)) for _ in columns]
                for c in selected:
                    i=c['row']['column'];initial[i]=sorted(set(initial[i])&set(c['row']['methods'][method]['candidates']))
                assert all(initial)
                for profile in ['degree_only','degree_discriminant']:
                    domains=[list(x) for x in initial];steps=[];first_local=None
                    for iteration in range(1,4*len(columns)+2):
                        before=[list(x) for x in domains];retained=[];local_removed=[]
                        for prime,indices in groups.items():
                            ids=[j for j,model in enumerate(models) if (profile=='degree_only' or any(e>1 for e,f in model)==(m['global_inputs']['discriminant']%prime==0)) and all(coefficient(model,columns[i]['power']) in before[i] for i in indices)]
                            assert ids;retained.append({'prime':prime,'model_ids':ids})
                            for i in indices:
                                values=sorted({coefficient(models[j],columns[i]['power']) for j in ids})
                                for v in sorted(set(before[i])-set(values)):local_removed.append({'column':i,'n':columns[i]['n'],'candidate':v,'prime':prime})
                                domains[i]=values
                        local_removed.sort(key=lambda r:(r['column'],r['candidate']));after_local=[list(x) for x in domains]
                        if first_local is None:first_local=[list(x) for x in domains]
                        removed={}
                        for c in selected:
                            row=c['row'];i=row['column']
                            if len(after_local[i])==1:continue
                            support=sum((max((r*v).upper() for v in d) for r,d in zip(c['residual'],after_local)),arb(0))
                            upper=c['weighted_rhs']+support+arb(row['methods'][method]['budget_upper'])
                            for value in after_local[i]:
                                if (i,value) not in removed and arb(row['sign']*value)>upper.upper():
                                    removed[i,value]={'column':i,'n':columns[i]['n'],'candidate':value,'audit_case_index':c['index'],'sign':row['sign'],
                                                      'weighted_rhs':encode(c['weighted_rhs']),'residual_support_bound':encode(support),'objective_upper_bound':encode(upper)}
                        for i,value in removed:domains[i].remove(value)
                        assert all(domains)
                        steps.append({'iteration':iteration,'before_domains_sha256':digest(before),'local_models':retained,'local_removals':local_removed,
                            'after_local_sha256':digest(after_local),'dual_removals':list(removed.values()),'after_domains_sha256':digest(domains)})
                        if domains==before:break
                    else:raise AssertionError('Finite feedback domains did not stabilize')
                    def unique(ds,limit=31):return sum(len(d)==1 for c,d in zip(columns,ds) if c['n']<=limit)
                    cases.append({'observation_index':obs,'radius':radius,'method':method,'profile':profile,'input_domains':initial,'first_local_domains':first_local,
                                  'rounds':steps,'final_domains':domains,'spectral_unique_targets':unique(initial),'first_local_unique_targets':unique(first_local),
                                  'feedback_unique_targets':unique(domains),'feedback_unique_support':unique(domains,4096)})
            print(json.dumps({'event':'noisy_dual_local_feedback','observation':obs,'radius':radius,'targets':[c['feedback_unique_targets'] for c in cases[-4:]]}),flush=True)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{path.name:sha(path) for path in [measurements,proposals,previous_proposals,audit_path]},
            'precision_bits':256,'columns':columns,'catalog':models,'cases':cases,
            'scope':'Each radius starts with the independently audited noisy target domains. Generic local projection alternates with the same frozen duals, replacing the 0..4 residual support by the exact support over current domains. The validated analytic error budgets are unchanged. No zero-noise domains, new multipliers, field templates or arithmetic coefficients are read. A fixed point is not global realizability.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','proposals','previous-proposals','audit','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.measurements,a.proposals,a.previous_proposals,a.audit);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'cases':len(r['cases'])}))
