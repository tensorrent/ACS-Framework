"""Propagate the independent adaptive audit's stronger bounds with exact domain support."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb,ctx
from dedekind_coupled_recovery import decode,encode
from dedekind_coupled_dual import inequalities
from dedekind_aggregate_integer_audit import integer_rows
from dedekind_aggregate_moment_local_audit import integer_dual,domain_bound,project,digest

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def infer(data,audit,m):
    ctx.prec=256;columns=m['columns'];altered=copy.deepcopy(m)
    for r in altered['rows']:
        for obs in [0,1]:r['observations'][obs]['R']=r['observations'][obs]['unwidened']
    integer=[integer_rows(altered,obs) for obs in [0,1]];real=[]
    for obs in [0,1]:
        real.append(inequalities([{'weights':[decode(w) for w in r['weights']],'R':decode(r['observations'][obs]['unwidened']),'B':decode(r['prime_tail'])} for r in m['rows']]))
    cases=[]
    for case_index,source in enumerate(data['cases']):
        obs=source['observation_index'];selected=[]
        for step in source['rounds']:
            for proposal in step['proposals']:
                i=proposal['certificate_index'];c=data['certificates'][i];budget=audit['budget_replays'][i];assert budget['certificate_sha256']==digest(c)
                A,b=real[obs];rhs=arb(0);v=[arb(0) for _ in columns]
                for j,value in c['multipliers']:
                    scalar=arb(value);rhs+=scalar*b[j];v=[x+scalar*y for x,y in zip(v,A[j])]
                residual=[(arb(c['sign']) if k==c['column'] else arb(0))-x for k,x in enumerate(v)]
                selected.append((i,c,integer_dual(integer[obs],c,len(columns)),budget['budget_upper'],rhs,residual))
        domains=copy.deepcopy(source['final_domains']);steps=[]
        for iteration in range(1,4*len(columns)+2):
            before=copy.deepcopy(domains);after_local,models,removals=project(columns,domains,source['profile']);removed={}
            for i,c,prepared,budget,rhs,residual in selected:
                column=c['column']
                if len(after_local[column])==1:continue
                upper=domain_bound(prepared,after_local,budget)
                for value in after_local[column]:
                    if (column,value) not in removed and c['sign']*value>upper:
                        interval=rhs+sum((max((r*v).upper() for v in d) for r,d in zip(residual,after_local)),arb(0))+arb(budget)
                        assert arb(c['sign']*value)>interval.upper()
                        removed[column,value]={'column':column,'n':c['n'],'candidate':value,'sign':c['sign'],'certificate_index':i,
                                               'exact_upper':str(upper),'strict_gap':str(c['sign']*value-upper),'interval_upper':encode(interval)}
            domains=copy.deepcopy(after_local)
            for column,value in removed:domains[column].remove(value)
            assert all(domains)
            steps.append({'iteration':iteration,'before_domains_sha256':digest(before),'local_models':models,'local_removals':removals,
                          'after_local_sha256':digest(after_local),'dual_removals':list(removed.values()),'after_domains_sha256':digest(domains)})
            if domains==before:break
        else:raise AssertionError('Finite audit closure did not stabilize')
        cases.append({**{k:source[k] for k in ['observation_index','radius','profile']},'adaptive_case_index':case_index,'input_domains':source['final_domains'],
                      'rounds':steps,'final_domains':domains,'unique_targets':sum(len(d)==1 for c,d in zip(columns,domains) if c['n']<=31),
                      'unique_support':sum(len(d)==1 for d in domains)})
    return cases

def run(adaptive_path,audit_path,measurements,truth_path):
    data=json.loads(adaptive_path.read_text());audit=json.loads(audit_path.read_text());m=json.loads(measurements.read_text())
    assert audit['status']=='passed' and audit['inputs_sha256'][adaptive_path.name]==sha(adaptive_path) and audit['inputs_sha256'][measurements.name]==sha(measurements)
    cases=infer(data,audit,m)
    # Held-out arithmetic enters only after all deductions have been computed.
    truth=json.loads(truth_path.read_text())['arithmetic_vectors']
    for c in cases:assert all(v in d for v,d in zip(truth[['A','B'][c['observation_index']]],c['final_domains']))
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [adaptive_path,audit_path,measurements,truth_path]},
            'cases':cases,'local_removals':sum(len(s['local_removals']) for c in cases for s in c['rounds']),
            'dual_removals':sum(len(s['dual_removals']) for c in cases for s in c['rounds']),'all_604_true_coefficients_retained':True,
            'scope':'Consume the independently stronger budgets using exact support over producer-final domains, then alternate generic local projection and every already validated adaptive vector for that radius/profile. Every new rational exclusion also passes a fresh 256-bit real interval support check. No multipliers are re-optimized in this supplemental closure.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['adaptive','audit','measurements','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.adaptive,a.audit,a.measurements,a.truth);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','local_removals','dual_removals']}))
