"""Verify retained coupled-recovery identities and certificate transcript links."""
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,re,subprocess,sys,zipfile
from pathlib import Path
from flint import arb,ctx

CODE=Path(__file__).absolute().parent
ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-coupled-delta'
PRIOR=ROOT/'docs/frontier/2026-09-13-recovery-delta'
ADVANCED=['P05','R12','R13','R14','K04']


def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def read(path):return json.loads(path.read_text())
def ball(value):return arb(arb(tuple(value['mid'])),arb(tuple(value['rad'])))


def main():
    ctx.prec=256
    previous=subprocess.run([sys.executable,str(CODE/'verify_recovery_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    manifest=read(OUT/'Manifest.json')
    for path,v in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==v['bytes'] and sha(raw)==v['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        source_hashes={sha(z.read(n)) for n in z.namelist() if n.endswith('.py')}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert sha(z.read(kind+'/'+path))==digest==sha((ROOT/path).read_bytes())
    raw_results={}
    for archive in ['Measurements.zip','Coupled_Audits.zip','Dual_Audits.zip']:
        with zipfile.ZipFile(OUT/archive) as z:
            for name in z.namelist():raw_results[name]=z.read(name)
    data={name:json.loads(raw) for name,raw in raw_results.items()}
    measurements=data['Measurements.json'];assert len(measurements['measurements'])==455 and len(measurements['roots'])==7602
    assert measurements['prior_archive_sha256']==sha((PRIOR/'Recovery_Audits.zip').read_bytes())
    for row in measurements['measurements']:assert not {'candidates','models','expected','coefficient'}.intersection(row)
    report=read(OUT/'Exact_Audit.json')
    assert report['status']=='passed' and report['source_sha256']==sha((CODE/'dedekind_coupled_audit.py').read_bytes())
    assert report['input_sha256']==sha(raw_results['Measurements.json'])
    assert report['results_sha256']=={n:sha(raw_results[n]) for n in ['Coupled_160.json','Coupled_224.json','Uncertainty_Grid.json','Dual_224.json','Dual_Refined.json']}
    total=0;linked={}
    for name in ['Coupled_160.json','Coupled_224.json','Uncertainty_Grid.json']:
        result=data[name];assert result['source_sha256']==sha((CODE/'dedekind_coupled_recovery.py').read_bytes())
        for case in result['cases']:
            assert case['status']=='passed' and len(case['measurements'])==91 and len(case['domains'])==604
            domains=[list(range(5)) for _ in case['domains']];checked=0
            for r in case['rounds']:
                assert r['prior_domains_sha256']==sha(canonical(domains))
                for w in r['removals']:
                    assert ball(w['strict_gap'])>0 and w['candidate'] in domains[w['column']]
                    assert case['domains'][w['column']]['n']==w['n']
                    assert case['measurements'][w['measurement_index']]['n']==w['measurement_target']
                    domains[w['column']].remove(w['candidate']);checked+=1
                assert all(domains) and r['remaining_domains_sha256']==sha(canonical(domains))
            assert domains==[r['candidates'] for r in case['domains']]
            assert case['unique_target_coefficients']==sum(len(r['candidates'])==1 for r in case['domains'] if r['n']<=361)
            linked[name,case['settings']['top'],case['additional_radius']]=(checked,sha(canonical(domains)))
            total+=checked
    for r in report['interval_replays']:
        assert linked[r['file'],r['height'],r['delta']]==(r['exclusions_replayed'],r['domains_sha256'])
        assert r['all_604_true_coefficients_retained']
    assert total==report['exclusions_replayed']==8601 and len(report['interval_replays'])==24
    for a,b in zip(data['Coupled_160.json']['cases'],data['Coupled_224.json']['cases']):assert a['domains']==b['domains']
    assert [c['unique_target_coefficients'] for c in data['Coupled_224.json']['cases']]==[78,91,91,91,91]
    dual=data['Dual_224.json'];refined=data['Dual_Refined.json'];certificates=0
    assert dual['source_sha256']==sha((CODE/'dedekind_coupled_dual.py').read_bytes())
    assert refined['source_sha256']==sha((CODE/'dedekind_coupled_dual_refine.py').read_bytes())
    assert refined['initial_dual_sha256']==sha(raw_results['Dual_224.json'])
    assert [c['unique_targets'] for c in dual['cases']]==[76,90,91,91,91]
    assert [c['unique_targets'] for c in refined['cases']]==[89,91,91,91,91]
    for first,last,exact in zip(dual['cases'],refined['cases'],report['dual_replays']):
        domains=[list(range(5)) for _ in last['domains']]
        for t,x in zip(first['targets'],exact['initial_bounds']):
            assert t['n']==x['n'] and t['candidates']==x['candidates']
            assert t['candidates']==[c for c in range(5) if -c<=F(x['bounds'][0]) and c<=F(x['bounds'][1])]
            domains[t['column']]=t['candidates'];certificates+=2
            assert all(F(v)>=0 for p in t['certificates'] for j,v in p['multipliers'])
        exact_changes=iter(exact['refinements'])
        for r in last['rounds']:
            assert r['prior_domains_sha256']==sha(canonical(domains))
            for c in r['changes']:
                x=next(exact_changes);assert c['n']==x['n'] and r['round']==x['round']
                assert c['after']==x['candidates']==[v for v in c['before'] if -v<=F(x['bounds'][0]) and v<=F(x['bounds'][1])]
                assert domains[c['column']]==c['before'];domains[c['column']]=c['after'];certificates+=2
            assert r['remaining_domains_sha256']==sha(canonical(domains))
        assert domains==[r['candidates'] for r in last['domains']] and sha(canonical(domains))==exact['final_domains_sha256']
    assert certificates==report['exact_dual_certificates']==970
    branch=read(OUT/'Target_Branches.json');witness=read(OUT/'Integer_Witnesses.json');ba=read(OUT/'Branch_Audit.json')
    assert branch['refined_sha256']==witness['refined_sha256']==sha(raw_results['Dual_Refined.json'])
    assert witness['branches_sha256']==sha((OUT/'Target_Branches.json').read_bytes())
    assert ba['source_sha256']==sha((CODE/'dedekind_coupled_branch_audit.py').read_bytes())
    assert len(branch['branches'])==8 and sum(b['excluded'] for b in branch['branches'])==6
    assert len(witness['proposals'])==len(ba['feasible_models'])==2
    for b,exact in zip(branch['branches'],ba['separations']):
        assert b['target_assignment']==exact['assignment'] and b['excluded']==exact['excluded']==(F(exact['exact_gap_lower_bound'])>0)
    for p,exact in zip(witness['proposals'],ba['feasible_models']):
        assert p['verified_feasible'] and len(p['coefficients'])==604 and len(p['checks'])==91
        assert all(c['strict_inclusion'] and ball(c['lower_gap'])>0 and ball(c['upper_gap'])>0 for c in p['checks'])
        assert p['assignment']==exact['assignment'] and F(exact['smallest_margin_lower_bound'])>0
        assert sha(canonical(p['coefficients']))==exact['coefficient_vector_sha256']
    assert [p['assignment'] for p in witness['proposals']]==[{'359':0,'361':4},{'359':1,'361':1}]
    local=read(OUT/'Local_Bridge.json')
    assert local['source_sha256']==sha((CODE/'dedekind_coupled_local_bridge.py').read_bytes())
    assert local['retained_partitions']==[[2,2]] and local['surviving_target_pairs']==[{'359':0,'361':4}]
    assert local['unique_target_coefficients_with_added_local_information']==91
    assert len(report['relaxation_ambiguity']['noncertified_trials'])==7
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==11 and all(r['returncode']==0 for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
            assert set(r['input_sources_sha256'].values())<=source_hashes
    ledger=(OUT/'Branch_Events.jsonl').read_bytes();old=(PRIOR/'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(old) and len(old.splitlines())==355
    previous='0'*64
    for i,line in enumerate(ledger.splitlines(),1):
        event=json.loads(line);digest=event.pop('event_sha256')
        assert event['sequence']==i and event['previous_event_sha256']==previous and sha(canonical(event))==digest
        previous=digest
    assert i==360
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']}
    queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert len(after)==116 and set(after)==set(before) and queue['new_branches']==[] and queue['global_exhaustion_claimed'] is False
    for bid,b in after.items():
        old_b=before[bid];assert b['prior_delta_evidence']==old_b.get('prior_delta_evidence',[])+old_b['new_evidence']
        if bid not in ADVANCED:
            assert b['latest_scoped_result']==old_b['latest_scoped_result'] and b['continuation_condition']==old_b['continuation_condition']
            assert b['assessment_this_pass']=='carried_forward_not_newly_audited'
        for p in b['new_evidence']:assert (ROOT/p).exists()
    links=0
    for p in [OUT/'README.md',OUT.parent/'README.md',CODE/'COUPLED_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (p.parent/link.split('#')[0]).exists(),(p,link)
                links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Retained source identities and transcript consistency; numerical optimizers, quadrature and root certification are not rerun.',
        'preceding_checkpoint_integrity':'passed','manifest_files':len(manifest['files']),
        'coupled_cases':24,'integer_exclusions_replayed_in_recorded_audit':8601,'dual_certificates_replayed_in_recorded_audit':970,
        'target_pair_branches':8,'excluded_pairs':6,'verified_feasible_relaxed_models':2,
        'targets_without_local_relations_at_600':91,'targets_with_added_local_relation_at_220':91,
        'receipts':11,'research_branches':116,'ledger_events':360,'preserved_event_prefix':355,
        'ledger_head_sha256':previous,'local_links':links},indent=2))


if __name__=='__main__':main()
