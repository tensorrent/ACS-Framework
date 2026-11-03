"""Independently audit wider-to-narrower premise transfer and adaptive noisy recovery."""
import argparse,copy,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from dedekind_aggregate_adaptive_audit import audit_budget,canonical
from dedekind_aggregate_integer_audit import integer_rows
from dedekind_aggregate_moment_local_audit import integer_dual,domain_bound,project,digest
from dedekind_aggregate_local_audit import catalog

RADII=['1/10','2/25','3/50','1/20','1/25','3/100']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def check_transfer(proof,source,radius,seed_radius):
    small,big=F(radius),F(seed_radius);assert small>=0 and big-small>=0
    assert proof['source_radius']==seed_radius and proof['destination_radius']==radius and proof['population_preserved'] is True
    roots=source['positive_root_intervals'];assert len(proof['roots'])==len(roots)
    for index,(r,p) in enumerate(zip(roots,proof['roots'])):
        left,right=F(r['lo']),F(r['hi']);a,b=map(F,p['outer_interval']);c,d=map(F,p['inner_interval'])
        assert p['root_index']==index and (a,b)==(left-big,right+big) and (c,d)==(left-small,right+small)
        assert c-a==b-d==big-small and a<=c<=d<=b and F(3,2)<a and b<20

def replay(data,m,prior,budgets,truth,sources):
    assert canonical(data['catalog'])==canonical(catalog()) and data['columns']==m['columns']
    columns=m['columns']; altered=copy.deepcopy(m)
    for r in altered['rows']:
        for obs in [0,1]: r['observations'][obs]['R']=r['observations'][obs]['unwidened']
    rows=[integer_rows(altered,obs) for obs in [0,1]]; replays=[]; used=[]
    assert len(data['cases'])==24 and len(budgets)==len(data['certificates'])
    keys=[(obs,radius,profile) for obs in [0,1] for radius in RADII for profile in ['degree_only','degree_discriminant']]
    assert [(c['observation_index'],c['radius'],c['profile']) for c in data['cases']]==keys
    for case_index,case in enumerate(data['cases']):
        obs=case['observation_index']; seed=prior['cases'][case['prior_case_index']]
        assert seed['radius']=='1/10' and all(seed[k]==case[k] for k in ['observation_index','profile'])
        check_transfer(case['transfer'],sources[obs],case['radius'],seed['radius'])
        domains=copy.deepcopy(seed['final_domains']); assert domains==case['input_domains']; exact_proofs=[]; local_count=0; dual_count=0; extra=[]
        for iteration,step in enumerate(case['rounds'],1):
            assert step['iteration']==iteration and step['before_domains_sha256']==digest(domains)
            after_local,retained,removed=project(columns,domains,case['profile']); local_count+=len(removed)
            assert retained==step['local_models'] and removed==step['local_removals'] and digest(after_local)==step['after_local_sha256']
            expected=[(i,sign) for i,c in enumerate(columns) if c['n']<=31 and len(after_local[i])>1 for sign in [-1,1]]
            assert [(p['column'],p['sign']) for p in step['proposals']]==expected
            by_index={}; eligible=set()
            for p in step['proposals']:
                index=p['certificate_index']; used.append(index); cert=data['certificates'][index]; budget=budgets[index]
                assert p['case_index']==case_index and p['iteration']==iteration and p['premise_domains_sha256']==digest(after_local)
                assert all(p[k]==case[k] for k in ['observation_index','radius','profile'])
                assert all(p[k]==cert[k] for k in ['observation_index','radius','column','n','sign','multipliers'])
                assert cert['n']==columns[cert['column']]['n'] and budget['certificate_sha256']==hashlib.sha256(canonical(cert)).hexdigest()
                upper=domain_bound(integer_dual(rows[obs],cert,len(columns)),after_local,budget['budget_upper'])
                allowed=[v for v in after_local[cert['column']] if cert['sign']*v<=upper]; assert allowed and truth[['A','B'][obs]][cert['column']] in allowed
                by_index[index]=(cert,upper)
                for value in after_local[cert['column']]:
                    if cert['sign']*value>upper: eligible.add((cert['column'],value))
            domains=copy.deepcopy(after_local); seen=set()
            for witness in step['dual_removals']:
                index=witness['certificate_index']; cert,upper=by_index[index]; i=witness['column']; value=witness['candidate']
                assert all(witness[k]==cert[k] for k in ['column','n','sign']) and value in after_local[i] and (i,value) not in seen; seen.add((i,value))
                gap=cert['sign']*value-upper; assert gap>0 and value!=truth[['A','B'][obs]][i]
                domains[i].remove(value); exact_proofs.append({'iteration':iteration,'certificate_index':index,'column':i,'candidate':value,'objective_upper':str(upper),'strict_gap':str(gap)})
            extra.extend({'iteration':iteration,'column':i,'candidate':v} for i,v in sorted(eligible-seen))
            assert all(domains) and digest(domains)==step['after_domains_sha256'] and all(v in d for v,d in zip(truth[['A','B'][obs]],domains)); dual_count+=len(seen)
        assert domains==case['final_domains'] and not case['rounds'][-1]['local_removals'] and not case['rounds'][-1]['dual_removals']
        unique=lambda ds:sum(len(d)==1 for c,d in zip(columns,ds) if c['n']<=31)
        assert unique(domains)==case['adaptive_unique_targets'] and unique(case['input_domains'])==case['initial_unique_targets'] and sum(len(d)==1 for d in domains)==case['adaptive_unique_support']
        replays.append({**{k:case[k] for k in ['observation_index','radius','profile','initial_unique_targets','adaptive_unique_targets','adaptive_unique_support']},
                        'iterations':len(case['rounds']),'local_removals':local_count,'dual_removals':dual_count,'exact_dual_proofs':exact_proofs,
                        'additional_audit_exclusions_not_propagated':extra,'all_604_true_coefficients_retained_each_round':True})
    assert used==list(range(len(data['certificates'])))
    return replays

def run(nested_path,measurements,inputs,prior_closure,prior_manifest,prior_verification,truth_path):
    data=json.loads(nested_path.read_text());m=json.loads(measurements.read_text());sources=[json.loads(p.read_text()) for p in inputs];prior=json.loads(prior_closure.read_text())
    manifest=json.loads(prior_manifest.read_text());verified=json.loads(prior_verification.read_text());truth=json.loads(truth_path.read_text())['arithmetic_vectors']
    assert data['status']==prior['status']==verified['status']=='passed' and data['radii']==RADII and data['seed_radius']=='1/10'
    assert data['inputs_sha256']=={p.name:sha(p) for p in [measurements,prior_closure,prior_manifest,prior_verification]+inputs}
    assert prior['inputs_sha256'][measurements.name]==sha(measurements) and [sha(p) for p in inputs]==m['input_sha256']
    entry=next(v for p,v in manifest['files'].items() if p.endswith('/'+prior_closure.name));assert entry['sha256']==sha(prior_closure) and entry['bytes']==prior_closure.stat().st_size
    budgets=[]
    for index,c in enumerate(data['certificates']):
        budgets.append(audit_budget(m,sources[c['observation_index']],c))
        if (index+1)%20==0:print(json.dumps({'event':'nested_complex_audit','certificates':index+1}),flush=True)
    replays=replay(data,m,prior,budgets,truth,sources)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [nested_path,measurements,prior_closure,prior_manifest,prior_verification,truth_path]+inputs},
            'fresh_precision_bits':384,'fresh_partitions_per_active_root':96,'budget_replays':budgets,'domain_replays':replays,
            'transported_root_intervals':sum(len(c['transfer']['roots']) for c in data['cases']),
            'stored_midpoints_checked':sum(b['stored_midpoints_checked'] for b in budgets),'fresh_quadratic_interval_leaves':sum(b['fresh_quadratic_interval_leaves'] for b in budgets),
            'independent_displaced_control_count':sum(len(b['independent_displaced_controls']) for b in budgets),
            'exact_domain_objectives':len(budgets),'local_removals':sum(r['local_removals'] for r in replays),'dual_removals':sum(r['dual_removals'] for r in replays),
            'scope':'Exact rational endpoint differences verify every wider-to-narrower seed transfer. Fresh complex quadratic covers and rational moment bounds audit changed vectors, and integer/Fraction replay checks every causal exclusion. The generic local catalogue is independently enumerated. Held-out truth remains a downstream check. Shared FLINT and finite sampled optimization limits remain explicit.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['nested','measurements','prior-closure','prior-manifest','prior-verification','truth','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args();r=run(a.nested,a.measurements,a.inputs,a.prior_closure,a.prior_manifest,a.prior_verification,a.truth)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','transported_root_intervals','stored_midpoints_checked','fresh_quadratic_interval_leaves','exact_domain_objectives','local_removals','dual_removals']}))
