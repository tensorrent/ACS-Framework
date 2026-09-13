"""Independently enumerate local models and replay the joint closure with integers."""
import argparse,hashlib,itertools,json
from pathlib import Path
from dedekind_aggregate_integer_audit import integer_rows,exclusion_gap

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def partitions(n,least=1):
    if n==0:yield ()
    for k in range(least,n+1):
        for tail in partitions(n-k,k):yield (k,)+tail
def catalog():
    out=set()
    for partition in partitions(4):
        choices=[[(e,size//e) for e in range(1,size+1) if size%e==0] for size in partition]
        out.update(tuple(sorted(model)) for model in itertools.product(*choices))
    return sorted(out)
def coefficient(model,k):return sum(f for e,f in model if k%f==0)


def run(local_paths,measurement_paths,recovery_paths,truth_path,shared_path):
    independent=catalog();assert len(independent)==11
    datasets=[json.loads(p.read_text()) for p in local_paths];truth=json.loads(truth_path.read_text())['arithmetic_vectors'];replays=[]
    local_exclusions=linear_exclusions=0
    for local_path,m_path,r_path,data in zip(local_paths,measurement_paths,recovery_paths,datasets):
        m=json.loads(m_path.read_text());recovery=json.loads(r_path.read_text())
        assert data['inputs_sha256']=={m_path.name:sha(m_path),r_path.name:sha(r_path)}
        models=[tuple(map(tuple,model)) for model in data['catalog']];assert models==independent
        columns=data['columns'];groups={p:[i for i,c in enumerate(columns) if c['prime']==p] for p in sorted({c['prime'] for c in columns})}
        for case in data['cases']:
            obs=case['observation_index'];baseline=[list(r['candidates']) for r in recovery['results'][obs]['monotone_exclusion']['domains']]
            for r in recovery['results'][obs]['dual_targets']:baseline[r['column']]=sorted(set(baseline[r['column']])&set(r['candidates']))
            assert baseline==case['input_domains'];domains=[list(x) for x in baseline];rows=integer_rows(m,obs);lc=sc=0
            for step in case['rounds']:
                assert step['before_domains_sha256']==digest(domains);before=[list(x) for x in domains]
                expected_models=[];removed=[]
                for p,indices in groups.items():
                    ids=[j for j,model in enumerate(independent) if (case['profile']=='degree_only' or any(e>1 for e,f in model)==(576%p==0)) and all(coefficient(model,columns[i]['power']) in before[i] for i in indices)]
                    assert ids;expected_models.append({'prime':p,'model_ids':ids})
                    for i in indices:
                        allowed=sorted({coefficient(independent[j],columns[i]['power']) for j in ids})
                        for v in sorted(set(before[i])-set(allowed)):removed.append({'column':i,'n':columns[i]['n'],'candidate':v,'prime':p})
                        domains[i]=allowed
                removed.sort(key=lambda r:(r['column'],r['candidate']))
                assert expected_models==step['local_models'] and removed==step['local_removals']
                assert digest(domains)==step['after_local_sha256'];after_local=[list(x) for x in domains]
                if step['iteration']==1:assert domains==case['first_local_domains']
                for w in step['linear_removals']:
                    i,c,j=w['column'],w['candidate'],w['measurement_index']
                    assert c in after_local[i] and columns[i]['n']==w['n']
                    assert exclusion_gap(rows[j],after_local,i,c,w['side'])>0
                    domains[i].remove(c)
                assert all(domains) and digest(domains)==step['after_domains_sha256']
                assert all(v in domain for v,domain in zip(truth[['A','B'][obs]],domains))
                lc+=len(removed);sc+=len(step['linear_removals'])
            assert domains==case['final_domains'] and not case['rounds'][-1]['local_removals'] and not case['rounds'][-1]['linear_removals']
            targets=sum(len(x)==1 for c,x in zip(columns,domains) if c['n']<=31);support=sum(len(x)==1 for x in domains)
            assert targets==case['joint_unique_targets']==17 and support==case['joint_unique_support']
            replays.append({'source_file':local_path.name,'observation_index':obs,'profile':case['profile'],'iterations':len(case['rounds']),
                            'local_exclusions':lc,'linear_exclusions':sc,'unique_targets':targets,'unique_support':support,'all_604_true_coefficients_retained':True})
            local_exclusions+=lc;linear_exclusions+=sc
    for a,b in zip(datasets[0]['cases'],datasets[1]['cases']):assert a['final_domains']==b['final_domains']
    shared=json.loads(shared_path.read_text());unramified_values=sorted({coefficient(model,1) for model in independent if all(e==1 for e,f in model)})
    assert unramified_values==[0,1,2,4]
    supplemented=[{'observation_index':r['observation_index'],'radius':r['radius'],
                   'input_candidates':r['methods']['shared_roots'],'degree_discriminant_candidates':sorted(set(r['methods']['shared_roots'])&set(unramified_values))} for r in shared['results']]
    assert next(r['degree_discriminant_candidates'] for r in supplemented if r['observation_index']==0 and r['radius']=='1/200')==[4]
    return {'status':'passed','source_sha256':sha(Path(__file__)),'inputs_sha256':{p.name:sha(p) for p in local_paths+measurement_paths+recovery_paths+[truth_path,shared_path]},
            'independent_catalog':independent,'joint_replays':replays,'local_exclusions':local_exclusions,'linear_exclusions':linear_exclusions,
            'unramified_prime_coefficient_values':unramified_values,'shared_radius_with_generic_local_rule':supplemented,
            'scope':'Partitions of degree four and divisor pairs independently exhaust local models. Exact integer row gaps replay every spectral elimination between local steps. Held-out arithmetic is used only for validation. Adding the generic unramified-prime rule excludes coefficient three at seven; it does not use a Galois group or a field candidate list.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['local','measurements','recoveries']:p.add_argument('--'+n,type=Path,nargs=2,required=True)
    for n in ['truth','shared','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=run(a.local,a.measurements,a.recoveries,a.truth,a.shared);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'local_exclusions':r['local_exclusions'],'linear_exclusions':r['linear_exclusions'],'joint_replays':len(r['joint_replays'])}))
