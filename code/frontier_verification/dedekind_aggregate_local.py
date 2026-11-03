"""Alternate generic local-degree models and certified spectral inequalities."""
import argparse,hashlib,json
from pathlib import Path
from flint import arb,ctx
from dedekind_coefficient_recovery import local_models
from dedekind_coupled_recovery import decode,encode

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def coefficient(model,power):return sum(f for e,f in model if power%f==0)


def initial_domains(result):
    domains=[list(row['candidates']) for row in result['monotone_exclusion']['domains']]
    for row in result['dual_targets']:domains[row['column']]=sorted(set(domains[row['column']])&set(row['candidates']))
    assert all(domains)
    return domains


def run(measurements,recovery):
    d=json.loads(measurements.read_text());recovered=json.loads(recovery.read_text());ctx.prec=256
    assert recovered['measurement_sha256']==sha(measurements)
    columns=d['columns'];catalog=sorted(local_models(4,False)+local_models(4,True));assert len(catalog)==11
    groups={p:[i for i,c in enumerate(columns) if c['prime']==p] for p in sorted({c['prime'] for c in columns})}
    cases=[]
    for observation,result in enumerate(recovered['results']):
        baseline=initial_domains(result)
        rows=[{'weights':[decode(w) for w in row['weights']],'R':decode(row['observations'][observation]['R']),'B':decode(row['prime_tail'])} for row in d['rows']]
        for profile in ['degree_only','degree_discriminant']:
            permitted={p:[j for j,m in enumerate(catalog) if profile=='degree_only' or any(e>1 for e,f in m)==(d['global_inputs']['discriminant']%p==0)] for p in groups}
            domains=[list(x) for x in baseline];rounds=[];first_local=None
            for iteration in range(1,4*len(columns)+2):
                before=[list(x) for x in domains];retained=[];local_removed=[]
                for p,indices in groups.items():
                    ids=[j for j in permitted[p] if all(coefficient(catalog[j],columns[i]['power']) in before[i] for i in indices)]
                    assert ids,('No compatible local model',observation,profile,p)
                    retained.append({'prime':p,'model_ids':ids})
                    for i in indices:
                        kept=sorted({coefficient(catalog[j],columns[i]['power']) for j in ids})
                        assert set(kept)<=set(before[i]) and kept
                        for value in set(before[i])-set(kept):local_removed.append({'column':i,'n':columns[i]['n'],'candidate':value,'prime':p})
                        domains[i]=kept
                local_removed.sort(key=lambda r:(r['column'],r['candidate']))
                if first_local is None:first_local=[list(x) for x in domains]
                after_local=[list(x) for x in domains];linear_removed={}
                for j,row in enumerate(rows):
                    low=sum((w*x[0] for w,x in zip(row['weights'],after_local)),arb(0))
                    high=sum((w*x[-1] for w,x in zip(row['weights'],after_local)),arb(0))+row['B']
                    assert not (row['R']<low or row['R']>high),('Inconsistent complete row',observation,profile,iteration,j)
                    for i,(w,old) in enumerate(zip(row['weights'],after_local)):
                        if len(old)==1:continue
                        for value in old:
                            if (i,value) in linear_removed:continue
                            lo=low+w*(value-old[0]);hi=high+w*(value-old[-1])
                            if row['R']<lo:side='candidate_minimum_above_observation';gap=lo-row['R']
                            elif row['R']>hi:side='candidate_maximum_below_observation';gap=row['R']-hi
                            else:continue
                            linear_removed[i,value]={'column':i,'n':columns[i]['n'],'candidate':value,'measurement_index':j,'side':side,'gap':encode(gap)}
                for i,value in linear_removed:domains[i].remove(value)
                assert all(domains)
                rounds.append({'iteration':iteration,'before_domains_sha256':digest(before),'local_models':retained,'local_removals':local_removed,
                               'after_local_sha256':digest(after_local),'linear_removals':list(linear_removed.values()),'after_domains_sha256':digest(domains)})
                if domains==before:break
            else:raise AssertionError('Finite domains failed to stabilize')
            def unique(ds,limit=31):return sum(len(x)==1 for c,x in zip(columns,ds) if c['n']<=limit)
            cases.append({'observation_index':observation,'profile':profile,'input_domains':baseline,'first_local_domains':first_local,'rounds':rounds,'final_domains':domains,
                          'baseline_unique_targets':unique(baseline),'first_local_unique_targets':unique(first_local),'joint_unique_targets':unique(domains),
                          'joint_unique_support':unique(domains,4096)})
            print(json.dumps({k:cases[-1][k] for k in ['observation_index','profile','baseline_unique_targets','first_local_unique_targets','joint_unique_targets','joint_unique_support']}),flush=True)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{measurements.name:sha(measurements),recovery.name:sha(recovery)},
            'columns':columns,'catalog':catalog,'cases':cases,
            'scope':'Generic sum(e*f)=4 local models, optionally with ramification from the discriminant, are alternated with the inherited Gaussian row inequalities. No Galois group, field candidate class or held-out arithmetic is used. One local pass and the joint fixed point are reported separately. Survivors are conservative local/spectral candidates, not proofs of global field realization.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['measurements','recovery','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.measurements,a.recovery);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'cases':len(r['cases'])}))
