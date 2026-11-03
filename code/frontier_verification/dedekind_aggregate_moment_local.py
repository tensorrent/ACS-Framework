"""Project noisy target domains through separately declared generic local models."""
import argparse,hashlib,json
from pathlib import Path
from dedekind_coefficient_recovery import local_models

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def coefficient(model,k):return sum(f for e,f in model if k%f==0)

def run(path):
    data=json.loads(path.read_text());columns=data['columns'];models=sorted(local_models(4,False)+local_models(4,True));assert len(models)==11
    groups={p:[i for i,c in enumerate(columns) if c['prime']==p] for p in sorted({c['prime'] for c in columns})};cases=[]
    for result in data['results']:
        for method in ['separate','coupled']:
            initial=[list(range(5)) for _ in columns]
            for row in result['targets']:initial[row['column']]=row['methods'][method]
            for profile in ['degree_only','degree_discriminant']:
                domains=[list(x) for x in initial];retained=[];removals=[]
                for prime,indices in groups.items():
                    ids=[j for j,model in enumerate(models) if (profile=='degree_only' or any(e>1 for e,f in model)==(data['global_inputs']['discriminant']%prime==0)) and all(coefficient(model,columns[i]['power']) in initial[i] for i in indices)]
                    assert ids;retained.append({'prime':prime,'model_ids':ids})
                    for i in indices:
                        allowed=sorted({coefficient(models[j],columns[i]['power']) for j in ids});assert allowed and set(allowed)<=set(initial[i])
                        for value in sorted(set(initial[i])-set(allowed)):removals.append({'column':i,'n':columns[i]['n'],'candidate':value,'prime':prime})
                        domains[i]=allowed
                removals.sort(key=lambda x:(x['column'],x['candidate']))
                cases.append({'observation_index':result['observation_index'],'radius':result['radius'],'spectral_method':method,'profile':profile,
                    'input_domains':initial,'local_models':retained,'removals':removals,'output_domains':domains,
                    'spectral_unique_targets':sum(len(initial[x['column']])==1 for x in result['targets']),
                    'local_unique_targets':sum(len(domains[x['column']])==1 for x in result['targets']),
                    'local_unique_support':sum(len(x)==1 for x in domains)})
        print(json.dumps({'event':'noisy_local_projection','observation':result['observation_index'],'radius':result['radius'],
                          'unique_targets':[c['local_unique_targets'] for c in cases[-4:]]}),flush=True)
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{path.name:sha(path)},'columns':columns,'catalog':models,'cases':cases,
            'scope':'Each noise radius starts all 604 coefficients in 0..4, intersecting only the newly certified noisy target domains. A complete local projection uses degree alone or degree plus discriminant ramification. No zero-noise monotone domains or old local deductions are reused as noisy premises. These local candidates do not certify joint global realization.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=run(a.certificate);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'cases':len(r['cases'])}))
