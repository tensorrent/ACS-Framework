"""Verify shared-ordinate certificate transcripts, provenance and append-only history."""
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,re,subprocess,sys,zipfile
from pathlib import Path
from flint import arb,ctx

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-shared-delta';PRIOR=ROOT/'docs/frontier/2026-09-13-uncertainty-delta'
ADVANCED=['R12','R13','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def read(p):return json.loads(p.read_text())
def ball(v):return arb(arb(tuple(v['mid'])),arb(tuple(v['rad'])))


def main():
    ctx.prec=256
    earlier=subprocess.run([sys.executable,str(CODE/'verify_ordinate_delta.py')],capture_output=True,text=True)
    assert earlier.returncode==0,earlier.stdout+earlier.stderr
    manifest=read(OUT/'Manifest.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        source_hashes={sha(z.read(n)) for n in z.namelist() if n.endswith('.py')}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert sha(z.read(kind+'/'+path))==digest==sha((ROOT/path).read_bytes())
    with zipfile.ZipFile(OUT/'Shared_Audits.zip') as z:raws={n:z.read(n) for n in z.namelist()}
    assert set(raws)=={'Marginal_224.json','Shared_Probe160.json','Shared_160.json'}
    data={n:json.loads(raw) for n,raw in raws.items()};audit=read(OUT/'Shared_Audit.json')
    assert audit['status']=='passed' and audit['source_sha256']==sha((CODE/'dedekind_shared_audit.py').read_bytes())
    assert audit['basis_source_sha256']==sha((CODE/'dedekind_shared_ordinate.py').read_bytes())
    assert audit['results_sha256']=={n:sha(raw) for n,raw in raws.items()}
    with zipfile.ZipFile(PRIOR/'Ordinate_Audits.zip') as z:old_raw=z.read('Ranges_224.json')
    old=json.loads(old_raw);seed=next(c for c in old['cases'] if c['additional_radius']=='5e-3' and c['settings']['top']==2000
                                     and c['method']=='stationary' and c['policy']=='retained_prefix')
    with zipfile.ZipFile(PRIOR.parent/'2026-09-13-coupled-delta'/'Measurements.zip') as z:measurement_raw=z.read('Measurements.json')
    seed_domains=[d['candidates'] for d in seed['domains']]
    assert seed['unique_target_coefficients']==73
    for name,result in data.items():
        assert result['status']=='passed'
        expected='dedekind_shared_recovery.py' if name=='Shared_160.json' else 'dedekind_shared_ordinate.py'
        assert result['source_sha256']==sha((CODE/expected).read_bytes())
        p=result['provenance'];assert p['seed_case']==seed and p['seed_domains_sha256']==sha(canonical(seed_domains))
        assert p['prior_ranges_sha256']==sha(old_raw) and p['measurement_input_sha256']==sha(measurement_raw)
        assert p['prior_audit_sha256']==sha((PRIOR/'Ordinate_Audit.json').read_bytes())
        if name!='Marginal_224.json':assert result['shared_basis']['roots']==7602 and len(result['shared_basis']['basis'])==455
    marginal=data['Marginal_224.json']['cases'][0]
    assert marginal['unique_targets']==73 and len(marginal['rounds'])==1
    assert len(audit['marginal_replays'])==18 and audit['marginal_certificates']==36
    for check,replay in zip(marginal['rounds'][0]['checks'],audit['marginal_replays']):
        assert check['n']==replay['n'] and check['after']==replay['candidates']==check['before']
        assert replay['candidates']==[v for v in check['before'] if all(c['sign']*v<=F(bound) for c,bound in zip(check['certificates'],replay['bounds']))]
    certificates=0;removed=0
    for name in ['Shared_Probe160.json','Shared_160.json']:
        result=data[name];case=result['cases'][0] if name=='Shared_Probe160.json' else result
        for bits in [160,224]:
            replay=next(r for r in audit['shared_replays'] if r['file']==name and r['precision_bits']==bits)
            exact=iter(replay['certificates']);domains=[list(d) for d in seed_domains]
            for step in case['rounds']:
                assert step['prior_domains_sha256']==sha(canonical(domains));old_domains=[list(d) for d in domains]
                for check in step['checks']:
                    column=check['column'];assert old_domains[column]==check['before'];bounds=[]
                    for certificate in check['certificates']:
                        item=next(exact);certificates+=1
                        assert item['round']==step['round'] and item['n']==check['n'] and item['sign']==certificate['sign']
                        assert item['multipliers_sha256']==sha(canonical(certificate['multipliers']))
                        value=sum(F(item[k]) for k in ['weighted_center_upper','zero_taylor_prime_upper','shared_ordinate_upper','residual_support_upper'])
                        assert value==F(item['objective_upper_bound']);bounds.append(value)
                        assert certificate['sign'] in [-1,1]
                        assert all((F(v)*10**9).denominator==1 for i,v in certificate['multipliers'])
                        assert all(0<=i<455 for i,v in certificate['multipliers'])
                    after=[v for v in check['before'] if all(c['sign']*v<=bound for c,bound in zip(check['certificates'],bounds))]
                    assert after==check['after']
                    assert after==[v for v in check['before'] if all(not arb(c['sign']*v)>ball(c['objective_upper_bound']).upper() for c in check['certificates'])]
                    if bits==160:removed+=len(check['before'])-len(after)
                    domains[column]=after
                assert step['remaining_domains_sha256']==sha(canonical(domains))
            assert list(exact)==[] and domains==[d['candidates'] for d in case['domains']]
            assert replay['domains_sha256']==sha(canonical(domains)) and replay['all_604_arithmetic_coefficients_retained']
    assert certificates==audit['shared_certificates_across_precisions']==120 and removed==audit['candidate_removals_including_probe']==12
    result=data['Shared_160.json'];assert result['unique_targets']==81 and result['stabilized'] and len(result['rounds'])==2
    statuses=[c['solver_status'] for s in result['rounds'] for k in s['checks'] for c in k['certificates']]
    assert statuses.count(0)==48 and statuses.count(None)==8 and len(statuses)==56
    probe=data['Shared_Probe160.json']['cases'][0]
    assert probe['unique_targets']==74
    assert sum(c['solver_status']==1 for s in probe['rounds'] for k in s['checks'] for c in k['certificates'])==2
    unresolved=[d for d in result['domains'] if d['n']<=361 and len(d['candidates'])>1]
    assert [d['n'] for d in unresolved]==[64,81,125,128,243,256,289,343,359,361]
    assert len(audit['derivative_point_checks'])==75 and len(audit['finite_center_checks'])==2 and audit['mpmath_digits']==80
    assert audit['symbolic_second_derivative_identity']
    assert all(c['derivative_enclosed'] and c['second_derivatives_bounded'] for c in audit['derivative_point_checks'])
    assert all(c['inside_certified_center'] and c['roots']==7602 for c in audit['finite_center_checks'])
    controls=audit['adversarial_controls'];assert ball(controls['omitted_taylor_remainder']['strict_excess_without_remainder'])>0
    assert ball(controls['absolute_of_sum_instead_of_sum_of_absolutes']['strict_underestimate'])>0
    dependency=controls['missing_seed_bounds'];assert F(dependency['without_seed_bounds'])>F(dependency['valid_objective_upper_bound'])
    summary=read(OUT/'Shared_Summary.json');assert summary['unresolved_targets']==unresolved and summary['shared_unique_targets']==81
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==4 and all(r['returncode']==0 for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
            assert set(r['input_sources_sha256'].values())<=source_hashes
    ledger=(OUT/'Branch_Events.jsonl').read_bytes();prefix=(PRIOR/'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(prefix) and len(prefix.splitlines())==363;last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        event=json.loads(line);digest=event.pop('event_sha256')
        assert event['sequence']==index and event['previous_event_sha256']==last and sha(canonical(event))==digest
        last=digest
    assert index==366
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']}
    queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert set(before)==set(after) and len(after)==116 and queue['new_branches']==[] and queue['global_exhaustion_claimed'] is False
    for bid,b in after.items():
        old_b=before[bid];assert b['prior_delta_evidence']==old_b.get('prior_delta_evidence',[])+old_b['new_evidence']
        if bid not in ADVANCED:
            assert b['latest_scoped_result']==old_b['latest_scoped_result'] and b['continuation_condition']==old_b['continuation_condition']
            assert b['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in b['new_evidence']:assert (ROOT/path).exists()
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'SHARED_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
       'scope':'Retained source, certificate transcript and history checks; numerical bases, optimizers and the independent arithmetic audit are not rerun.',
       'preceding_checkpoint_integrity':'passed','manifest_files':len(manifest['files']),
       'marginal_certificates_replayed_in_recorded_audit':36,'shared_certificates_across_two_precisions':120,
       'independent_derivative_cases':75,'independent_finite_center_sums':2,'shared_unique_targets':81,'unresolved_targets':10,
       'recorded_commands':4,'limited_probe_solver_trials':2,'research_branches':116,'ledger_events':366,'preserved_event_prefix':363,
       'ledger_head_sha256':last,'local_links':links},indent=2))


if __name__=='__main__':main()
