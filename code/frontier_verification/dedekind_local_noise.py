"""Alternate exact local-profile filtering and certified positive spectral inequalities."""
import argparse,json,time,zipfile
from pathlib import Path
from flint import ctx
import dedekind_coupled_recovery as core
from dedekind_coupled_audit import integers
import dedekind_local_profiles as local

HEIGHTS=[220,600,1000,1500,2000]
def read(path):return json.loads(path.read_text())
def archived(path,name):
    with zipfile.ZipFile(path) as z:raw=z.read(name)
    return json.loads(raw),core.sha(raw)

def load_inputs(directory,prior,bits):
    data_raw=(directory/'Measurements.json').read_bytes();data=json.loads(data_raw);inputs={};cases=[];rows_by={}
    base=prior.parent
    narrow,narrow_hash=archived(base/'2026-09-13-uncertainty-delta/Ordinate_Audits.zip','Ranges_'+str(bits)+'.json')
    wide_path=directory/('Wide_Ranges'+str(bits)+'.json');wide_raw=wide_path.read_bytes();wide=json.loads(wide_raw)
    for label,dataset,digest in [('narrow',narrow,narrow_hash),('wide',wide,core.sha(wide_raw))]:
        assert dataset['status']=='passed' and dataset['input_sha256']==core.sha(data_raw)
        inputs[label]={'sha256':digest,'precision_bits':bits}
        for bound in dataset['bounds']:
            delta=bound['additional_radius']
            if label=='narrow' and delta!='5e-3':continue
            top=bound['settings']['top'];powers,rows,settings=core.prepare(data,top,bits,delta)
            assert settings==bound['settings']
            metadata=bound['measurements_by_method']['stationary']
            built=[]
            for original,m in zip(rows,metadata):
                assert {k:v for k,v in m.items() if k not in ['R','range_method']}=={k:v for k,v in original['metadata'].items() if k!='R'}
                built.append({'weights':original['weights'],'R':core.decode(m['R']),'B':original['B'],'metadata':m})
            rows_by[delta,top]=built
        for case in dataset['cases']:
            if case['method']!='stationary' or case['policy']!='retained_prefix':continue
            delta=case['additional_radius']
            if label=='narrow' and delta!='5e-3':continue
            top=case['settings']['top'];rows=[r for t in HEIGHTS if t<=top for r in rows_by[delta,t]]
            assert core.sha(core.canonical([r['metadata'] for r in rows]))==case['measurements_sha256']
            cases.append({'label':label+'_stationary','delta':delta,'top':top,'seed_domains':case['domains'],'rows':rows,
                'source_sha256':digest,'seed_domain_hash':core.sha(core.canonical(case['domains']))})
    shared,shared_hash=archived(base/'2026-09-13-shared-delta/Shared_Audits.zip','Shared_160.json')
    quadratic,quadratic_hash=archived(prior/'Quadratic_Audits.zip','Quadratic_Union160.json')
    qcase=next(c for c in quadratic['cases'] if c['mode']=='quadratic')
    for label,source,digest in [('shared',shared,shared_hash),('quadratic',qcase,quadratic_hash)]:
        rows=[r for t in HEIGHTS for r in rows_by['5e-3',t]]
        cases.append({'label':label,'delta':'5e-3','top':2000,'seed_domains':source['domains'],'rows':rows,
            'source_sha256':digest,'seed_domain_hash':core.sha(core.canonical(source['domains']))})
        inputs[label]={'sha256':digest,'seed_precision_bits':160,'audit_replay_precisions':[160,224]}
    return data,powers,cases,inputs,core.sha(data_raw)

def spectral_pass(powers,rows,domains):
    removals={}
    for index,row in enumerate(rows):
        lower=sum(w*d[0] for w,d in zip(row['lo'],domains))
        upper=sum(w*d[-1] for w,d in zip(row['hi'],domains))+row['tail']
        assert lower<=row['rhi'] and row['rlo']<=upper,('Row inconsistent',index)
        for i,d in enumerate(domains):
            if len(d)==1:continue
            for candidate in d:
                if (i,candidate) in removals:continue
                low=lower+row['lo'][i]*(candidate-d[0]);high=upper+row['hi'][i]*(candidate-d[-1])
                if low>row['rhi']:side='candidate_minimum_above_observation';gap=low-row['rhi']
                elif high<row['rlo']:side='candidate_maximum_below_observation';gap=row['rlo']-high
                else:continue
                removals[i,candidate]={'column':i,'n':powers[i][0],'candidate':candidate,'measurement_index':index,
                    'side':side,'strict_gap_scaled_integer':str(gap)}
    out=[list(d) for d in domains]
    for i,c in removals:out[i].remove(c)
    assert all(out)
    return out,list(removals.values())

def run(directory,prior,bits):
    start=time.monotonic();data,powers,cases,inputs,measurement_hash=load_inputs(directory,prior,bits);ctx.prec=bits
    reports=[]
    for case in cases:
        integer_rows=integers(case['rows']);seeds=[r['candidates'] for r in case['seed_domains']]
        for profile in local.PROFILES:
            initial,first=local.local_pass(powers,seeds,profile)
            domains=[list(d) for d in seeds];rounds=[]
            for number in range(1,4*len(powers)+2):
                old=[list(d) for d in domains];middle,local_checks=local.local_pass(powers,old,profile)
                domains,spectral_checks=spectral_pass(powers,integer_rows,middle)
                rounds.append({'round':number,'prior_domains_sha256':core.sha(core.canonical(old)),
                    'local_checks':local_checks,'after_local_domains_sha256':core.sha(core.canonical(middle)),
                    'spectral_checks':spectral_checks,'remaining_domains_sha256':core.sha(core.canonical(domains))})
                if domains==old:break
            else:raise AssertionError('Finite monotone iteration did not stabilize')
            final_models=[{'prime':p,'retained_model_ids':local.retained(powers,domains,columns,profile)}
                for p,columns in local.groups(powers).items()]
            minimal=[]
            if case['label']=='quadratic':
                for i,((n,p,k),before,after) in enumerate(zip(powers,seeds,initial)):
                    if n<=361 and len(before)>1 and len(after)==1:
                        minimal.append(local.minimal_observations(powers,seeds,i,profile,after[0]))
            reports.append({k:case[k] for k in ['label','delta','top','source_sha256','seed_domain_hash']} | {
                'profile':profile,'seed_domains':case['seed_domains'],
                'measurements_sha256':core.sha(core.canonical([r['metadata'] for r in case['rows']])),
                'integer_rows_sha256':core.sha(core.canonical(integer_rows)),'measurement_count':len(integer_rows),
                'seed_unique_targets':sum(len(d)==1 for (n,p,k),d in zip(powers,seeds) if n<=361),
                'local_only_unique_targets':sum(len(d)==1 for (n,p,k),d in zip(powers,initial) if n<=361),
                'local_only_domains_sha256':core.sha(core.canonical(initial)),
                'rounds':rounds,'domains':[{'n':n,'prime':p,'power':k,'candidates':d} for (n,p,k),d in zip(powers,domains)],
                'unique_target_coefficients':sum(len(d)==1 for (n,p,k),d in zip(powers,domains) if n<=361),
                'unique_support_coefficients':sum(len(d)==1 for d in domains),'local_models':final_models,
                'unique_target_prime_local_models':sum(len(m['retained_model_ids'])==1 for m in final_models if m['prime']<=361),
                'minimal_quadratic_seed_observations':minimal})
            print(json.dumps({'event':'local_noise','label':case['label'],'delta':case['delta'],'top':case['top'],'profile':profile,
                'seed':reports[-1]['seed_unique_targets'],'local_only':reports[-1]['local_only_unique_targets'],
                'coupled':reports[-1]['unique_target_coefficients'],'rounds':len(rounds),'elapsed_seconds':time.monotonic()-start}),flush=True)
    return {'status':'passed','source_sha256':core.sha(Path(__file__).read_bytes()),'profiles_source_sha256':core.sha(Path(local.__file__).read_bytes()),
        'precision_bits':bits,'measurement_input_sha256':measurement_hash,'inputs':inputs,'catalogue':[list(map(list,m)) for m in local.MODELS],
        'assumption_profiles':{p:{'degree':4,'galois_extension':'galois' in p,'use_discriminant_to_label_ramified_primes':'discriminant' in p} for p in local.PROFILES},
        'fixed_point_scale_bits':192,'cases':reports,'elapsed_seconds':time.monotonic()-start,
        'scope':'General degree-four Euler profiles, optionally restricted by the given discriminant and an explicitly added Galois premise. Alternating local and positive spectral exclusions use all 604 coefficients. No residue-class splitting oracle or held-out field polynomial enters inference. Surviving local models need not be jointly realizable by a number field.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--prior',type=Path,required=True);p.add_argument('--precision',type=int,choices=[160,224],required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();r=run(a.directory,a.prior,a.precision);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'cases':len(r['cases'])}))
