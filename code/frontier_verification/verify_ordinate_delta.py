"""Verify retained ordinate-range evidence, integer transcript links and history."""
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,re,subprocess,sys,zipfile
from pathlib import Path
from flint import arb,ctx

CODE=Path(__file__).absolute().parent
ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-uncertainty-delta'
PRIOR=ROOT/'docs/frontier/2026-09-13-coupled-delta'
ADVANCED=['R12','R13','K04']


def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def read(path):return json.loads(path.read_text())
def ball(value):return arb(arb(tuple(value['mid'])),arb(tuple(value['rad'])))
def key(c):return c['additional_radius'],c['settings']['top'],c['method'],c['policy']


def main():
    ctx.prec=256
    previous=subprocess.run([sys.executable,str(CODE/'verify_coupled_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    manifest=read(OUT/'Manifest.json')
    for path,v in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==v['bytes'] and sha(raw)==v['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        source_hashes={sha(z.read(n)) for n in z.namelist() if n.endswith('.py')}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert sha(z.read(kind+'/'+path))==digest==sha((ROOT/path).read_bytes())
    with zipfile.ZipFile(PRIOR/'Measurements.zip') as z:measurement_raw=z.read('Measurements.json')
    measurements=json.loads(measurement_raw)
    assert len(measurements['roots'])==7602 and len(measurements['measurements'])==455
    with zipfile.ZipFile(OUT/'Ordinate_Audits.zip') as z:raws={n:z.read(n) for n in z.namelist()}
    data={n:json.loads(raw) for n,raw in raws.items()}
    assert set(data)=={'Ranges_Probe160.json','Ranges_160.json','Ranges_224.json'}
    audit=read(OUT/'Ordinate_Audit.json');assert audit['status']=='passed'
    assert audit['source_sha256']==sha((CODE/'dedekind_ordinate_audit.py').read_bytes())
    assert audit['results_sha256']=={n:sha(raw) for n,raw in raws.items()}
    assert audit['input_sha256']==sha(measurement_raw)
    linked={};total=0;phases=0
    for name,dataset in data.items():
        assert dataset['status']=='passed' and dataset['source_sha256']==sha((CODE/'dedekind_ordinate_ranges.py').read_bytes())
        assert dataset['core_sha256']==sha((CODE/'dedekind_coupled_recovery.py').read_bytes())
        assert dataset['input_sha256']==sha(measurement_raw)
        bounds={(b['additional_radius'],b['settings']['top']):b for b in dataset['bounds']}
        for b in bounds.values():
            assert len(b['diagnostics'])==91
            for d in b['diagnostics']:
                assert d['critical_edge_boxes']==0
                phases+=len(d['critical_points'])
                for p in d['critical_points']:assert p['k']>=1 and ball(p['point'])>0 and 1<=p['iterations']<=50
        for case in dataset['cases']:
            assert case['status']=='passed' and len(case['domains'])==604
            delta,top,method,policy=key(case)
            heights=[t for t in [220,600,1000,1500,2000] if t<=top] if policy=='retained_prefix' else [top]
            metadata=[m for h in heights for m in bounds[delta,h]['measurements_by_method'][method]]
            assert len(metadata)==case['measurement_count'] and sha(canonical(metadata))==case['measurements_sha256']
            domains=[list(range(5)) for _ in case['domains']];count=0
            for step in case['rounds']:
                assert sha(canonical(domains))==step['prior_domains_sha256']
                for w in step['removals']:
                    assert ball(w['strict_gap'])>0 and w['candidate'] in domains[w['column']]
                    assert case['domains'][w['column']]['n']==w['n'] and metadata[w['measurement_index']]['n']==w['measurement_target']
                    domains[w['column']].remove(w['candidate']);count+=1
                assert all(domains) and sha(canonical(domains))==step['remaining_domains_sha256']
            assert domains==[d['candidates'] for d in case['domains']]
            assert case['unique_target_coefficients']==sum(len(d['candidates'])==1 for d in case['domains'] if d['n']<=361)
            linked[name,key(case)]=count,sha(canonical(domains));total+=count
    assert len(linked)==360 and total==audit['exclusions_replayed']
    assert phases==audit['critical_point_strict_phase_brackets'] and phases>0
    for replay in audit['interval_replays']:
        assert linked[replay['file'],tuple(replay['case'])]==(replay['exclusions'],replay['domains_sha256'])
        assert replay['all_604_arithmetic_coefficients_retained']
    assert len(audit['interval_replays'])==360 and audit['precision_domain_comparisons']==160 and audit['probe_repeat_cases']==40
    low={key(c):c for c in data['Ranges_160.json']['cases']};high={key(c):c for c in data['Ranges_224.json']['cases']}
    assert set(low)==set(high) and all(low[k]['domains']==high[k]['domains'] for k in low)
    assert all(c==low[key(c)] for c in data['Ranges_Probe160.json']['cases'])
    for method in ['derivative','direct','stationary']:
        for top in [600,1000,1500,2000]:
            for policy in ['single_cutoff','retained_prefix']:assert high['5e-4',top,method,policy]['unique_target_coefficients']==91
    assert high['5e-4',2000,'global','single_cutoff']['unique_target_coefficients']==55
    assert high['5e-4',2000,'global','retained_prefix']['unique_target_coefficients']==78
    assert len(audit['mpmath_extrema_cases'])==12 and audit['mpmath_digits']==80
    for c in audit['mpmath_extrema_cases']:
        assert c['inside_certified_extrema_bounds'] and 0<=F(c['lower_bound_slack'])<F('1e-25') and 0<=F(c['upper_bound_slack'])<F('1e-25')
    controls=audit['adversarial_controls']
    assert int(controls['missing_prerequisites']['valid_gap_scaled_integer'])>0>=int(controls['missing_prerequisites']['missing_prerequisite_gap_scaled_integer'])
    assert int(controls['true_coefficient_elimination']['false_exclusion_gap_scaled_integer'])<=0
    assert ball(controls['omitted_critical_point']['strict_gap_beyond_endpoint_hull'])>0
    summary=read(OUT/'Ordinate_Summary.json')
    assert summary['cases']==[{'additional_radius':c['additional_radius'],'height':c['settings']['top'],'method':c['method'],'policy':c['policy'],
      'unique_targets':c['unique_target_coefficients'],'unique_support':c['unique_support_coefficients'],'measurement_count':c['measurement_count'],
      'unresolved_targets':[d for d in c['domains'] if d['n']<=361 and len(d['candidates'])>1]} for c in data['Ranges_224.json']['cases']]
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)>=4
    assert all(r['returncode']==0 for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
            assert set(r['input_sources_sha256'].values())<=source_hashes
    ledger=(OUT/'Branch_Events.jsonl').read_bytes();old=(PRIOR/'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(old) and len(old.splitlines())==360
    previous='0'*64
    for i,line in enumerate(ledger.splitlines(),1):
        event=json.loads(line);digest=event.pop('event_sha256')
        assert event['sequence']==i and event['previous_event_sha256']==previous and sha(canonical(event))==digest
        previous=digest
    assert i==363
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']}
    queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert len(after)==116 and set(after)==set(before) and queue['new_branches']==[] and queue['global_exhaustion_claimed'] is False
    for bid,b in after.items():
        old_b=before[bid];assert b['prior_delta_evidence']==old_b.get('prior_delta_evidence',[])+old_b['new_evidence']
        if bid not in ADVANCED:
            assert b['latest_scoped_result']==old_b['latest_scoped_result'] and b['continuation_condition']==old_b['continuation_condition']
            assert b['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in b['new_evidence']:assert (ROOT/path).exists()
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'ORDINATE_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent/link.split('#')[0]).exists(),(path,link)
                links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
       'scope':'Retained source identities and transcript consistency; interval producers, integer replay and mpmath extrema are not rerun.',
       'preceding_checkpoint_integrity':'passed','manifest_files':len(manifest['files']),'retained_cases':360,
       'integer_exclusions_replayed_in_recorded_audit':total,'critical_points_bracketed_in_recorded_audit':phases,'mpmath_extrema_cases':12,
       'receipts':len(receipts),'research_branches':116,'ledger_events':363,'preserved_event_prefix':360,
       'ledger_head_sha256':previous,'local_links':links},indent=2))


if __name__=='__main__':main()
