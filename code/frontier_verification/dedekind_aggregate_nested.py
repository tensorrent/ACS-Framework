"""Transfer wider-radius domains by exact inclusion and re-optimize within the smaller boxes."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from flint import arb
from dedekind_coupled_recovery import encode
from dedekind_coefficient_recovery import local_models
from dedekind_aggregate_adaptive import setup,propose,domain_objective,coefficient,digest
from dedekind_aggregate_moment_certificate import certify

RADII=['1/10','2/25','3/50','1/20','1/25','3/100']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def transfer(source,radius,seed):
    small,big=F(radius),F(seed['radius']);assert 0<=small<=big
    roots=[]
    for i,r in enumerate(source['positive_root_intervals']):
        lo,hi=F(r['lo']),F(r['hi']);outer=[lo-big,hi+big];inner=[lo-small,hi+small]
        assert F(3,2)<outer[0]<=inner[0]<=inner[1]<=outer[1]<20
        roots.append({'root_index':i,'outer_interval':list(map(str,outer)),'inner_interval':list(map(str,inner))})
    return {'source_radius':seed['radius'],'destination_radius':radius,'roots':roots,'population_preserved':True,
            'scope':'Every new ordinate interval is contained in the previously certified wider interval, with unchanged root indexing, metadata, measurement rows and local profile. Wider-radius coefficient exclusions therefore remain valid.'}

def run(measurements,inputs,prior_closure,prior_manifest,prior_verification):
    m=json.loads(measurements.read_text());sources=[json.loads(p.read_text()) for p in inputs];old=json.loads(prior_closure.read_text())
    manifest=json.loads(prior_manifest.read_text());verified=json.loads(prior_verification.read_text())
    assert old['status']==verified['status']=='passed' and old['inputs_sha256'][measurements.name]==sha(measurements)
    entry=next(v for p,v in manifest['files'].items() if p.endswith('/'+prior_closure.name));assert entry['sha256']==sha(prior_closure) and entry['bytes']==prior_closure.stat().st_size
    assert [sha(p) for p in inputs]==m['input_sha256']
    assert m['global_inputs']=={'degree':4,'discriminant':576,'real_places':0,'complex_places':2,'top':20}
    columns=m['columns'];models=sorted(local_models(4,False)+local_models(4,True))
    groups={p:[i for i,c in enumerate(columns) if c['prime']==p] for p in sorted({c['prime'] for c in columns})}
    cases=[];certificates=[]
    plan=[(obs,radius,profile) for obs in [0,1] for radius in RADII for profile in ['degree_only','degree_discriminant']]
    for obs,radius,profile in plan:
        matches=[(i,s) for i,s in enumerate(old['cases']) if s['observation_index']==obs and s['radius']=='1/10' and s['profile']==profile];assert len(matches)==1
        seed_index,seed=matches[0];transport=transfer(sources[obs],radius,seed);prepared=setup(m,sources[obs],obs,radius)
        domains=[list(d) for d in seed['final_domains']];assert len(domains)==len(columns);initial=[list(d) for d in domains];steps=[]
        for iteration in range(1,4*len(columns)+2):
            before=[list(d) for d in domains]; retained=[]; local_removed=[]
            for prime,indices in groups.items():
                ids=[j for j,model in enumerate(models) if (profile=='degree_only' or any(e>1 for e,f in model)==(576%prime==0)) and all(coefficient(model,columns[i]['power']) in before[i] for i in indices)]
                assert ids; retained.append({'prime':prime,'model_ids':ids})
                for i in indices:
                    values=sorted({coefficient(models[j],columns[i]['power']) for j in ids})
                    for v in sorted(set(before[i])-set(values)): local_removed.append({'column':i,'n':columns[i]['n'],'candidate':v,'prime':prime})
                    domains[i]=values
            local_removed.sort(key=lambda r:(r['column'],r['candidate'])); after_local=[list(d) for d in domains]
            proposals=[]; removed={}
            for column,c in enumerate(columns):
                if c['n']>31 or len(after_local[column])==1: continue
                for sign in [-1,1]:
                    proposal={**propose(prepared,after_local,column,sign),'observation_index':obs,'radius':radius,'profile':profile,'column':column,'n':c['n'],'sign':sign,
                              'case_index':len(cases),'iteration':iteration,'premise_domains_sha256':digest(after_local),'certificate_index':len(certificates)}
                    proof=certify(m,sources[obs],proposal); certificates.append(proof)
                    upper=domain_objective(prepared,proposal,after_local,proof['methods']['coupled']['total_zero_and_input_budget'])
                    proposal['domain_objective_upper_bound']=encode(upper); proposals.append(proposal)
                    for value in after_local[column]:
                        if (column,value) not in removed and arb(sign*value)>upper.upper():
                            removed[column,value]={'column':column,'n':c['n'],'candidate':value,'sign':sign,'certificate_index':proposal['certificate_index']}
            for column,value in removed: domains[column].remove(value)
            assert all(domains)
            steps.append({'iteration':iteration,'before_domains_sha256':digest(before),'local_models':retained,'local_removals':local_removed,
                          'after_local_sha256':digest(after_local),'proposals':proposals,'dual_removals':list(removed.values()),'after_domains_sha256':digest(domains)})
            print(json.dumps({'event':'adaptive_round','observation':obs,'radius':radius,'profile':profile,'iteration':iteration,'proposals':len(proposals),
                              'local_removals':len(local_removed),'dual_removals':len(removed),'unique_targets':sum(len(d)==1 for c,d in zip(columns,domains) if c['n']<=31)}),flush=True)
            if domains==before: break
        else: raise AssertionError('Finite domain iteration did not stabilize')
        cases.append({'observation_index':obs,'radius':radius,'profile':profile,'prior_case_index':seed_index,'transfer':transport,'input_domains':initial,'rounds':steps,'final_domains':domains,
                      'initial_unique_targets':sum(len(d)==1 for c,d in zip(columns,initial) if c['n']<=31),
                      'adaptive_unique_targets':sum(len(d)==1 for c,d in zip(columns,domains) if c['n']<=31),'adaptive_unique_support':sum(len(d)==1 for d in domains)})
    assert len(cases)==24
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in [measurements,prior_closure,prior_manifest,prior_verification]+inputs},
            'columns':columns,'catalog':models,'radii':RADII,'seed_radius':'1/10','sample_offsets_per_root':33,'rational_multiplier_grid':10**9,'cases':cases,'certificates':certificates,
            'scope':'Each new radius/profile starts from the final independently strengthened radius-0.1 domains, transported by explicit interval inclusion. Adaptive sampled vectors receive fresh real continuum certificates before every deduction. No smaller-radius domain seeds a larger radius, and no arithmetic coefficients or field catalogue enter inference. Stalling this particular update does not prove optimality or ambiguity.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','prior-closure','prior-manifest','prior-verification','output']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--inputs',type=Path,nargs=2,required=True);a=p.parse_args();r=run(a.measurements,a.inputs,a.prior_closure,a.prior_manifest,a.prior_verification)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'cases':len(r['cases']),'certificates':len(r['certificates'])}))
