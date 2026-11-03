"""Verify shared-error certificates, generic local feedback, and append-only history."""
import contextlib,hashlib,io,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from pathlib import Path
import dedekind_aggregate_shared as shared
import dedekind_aggregate_local as local
import dedekind_aggregate_shared_audit as shared_audit
import dedekind_aggregate_local_audit as local_audit
import dedekind_aggregate_shared_adversary as adversary

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-aggregate-shared-delta';PRIOR=ROOT/'docs/frontier/2026-09-13-aggregate-delta'
ADVANCED=['R12','R13','R14','R15','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def same(a,b):assert canonical(a)==canonical(b)
def quiet(fn,*args):
    with contextlib.redirect_stdout(io.StringIO()):return fn(*args)
def unpack(path,tmp,names):
    with zipfile.ZipFile(path) as z:
        assert set(z.namelist())==set(names)
        for name in names:(tmp/name).write_bytes(z.read(name))

def main():
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    manifest=read(OUT/'Manifest.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert digest==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory)
        unpack(PRIOR/'Aggregate_Inputs.zip',tmp,['S1_160.json','S2_160.json','S1_224.json','S2_224.json'])
        unpack(PRIOR/'Measurements_Recovery.zip',tmp,['Measurements160.json','Measurements224.json','Recovery160.json','Recovery224.json'])
        unpack(OUT/'Shared_Local_Certificates.zip',tmp,['Shared224.json','Shared320.json','Local160.json','Local224.json'])
        mp=[tmp/f'Measurements{b}.json' for b in [160,224]];rp=[tmp/f'Recovery{b}.json' for b in [160,224]]
        sp=[tmp/f'Shared{b}.json' for b in [224,320]];lp=[tmp/f'Local{b}.json' for b in [160,224]]
        inputs=[tmp/'S1_224.json',tmp/'S2_224.json']
        for bits,path in zip([224,320],sp):same(read(path),quiet(shared.run,mp[1],rp[1],inputs,bits))
        for path,m,r in zip(lp,mp,rp):same(read(path),quiet(local.run,m,r))
        sa=read(OUT/'Shared_Audit.json');la=read(OUT/'Local_Audit.json');aa=read(OUT/'Adversary_Audit.json')
        same(sa,quiet(shared_audit.run,sp,mp[1],rp[1],inputs,PRIOR/'Radius_Audit.json'))
        same(la,quiet(local_audit.run,lp,mp,rp,PRIOR/'Integer_Audit.json',sp[1]))
        same(aa,quiet(adversary.run,sp[1],lp[1],mp[1],inputs,PRIOR/'Integer_Audit.json'))
        for data in [read(p) for p in sp+lp]+[sa,la,aa]:
            for name,digest in data['inputs_sha256'].items():
                path=next(p for p in [tmp/name,OUT/name,PRIOR/name] if p.exists());assert sha(path.read_bytes())==digest
        assert sa['stored_leaf_midpoints_checked']==39600 and sa['fresh_complex_interval_leaves']==47520 and sa['exact_objective_bounds']==144
        assert len(sa['independent_displaced_controls'])==96 and len(sa['common_error_premise_controls'])==2
        assert la['local_exclusions']==3162 and la['linear_exclusions']==190 and len(la['joint_replays'])==8
        assert aa['actual_component_mutations_rejected']==10
        summary=read(OUT/'Aggregate_Shared_Summary.json');d=read(sp[1]);l=read(lp[1])
        same(summary['radius_results'],d['results']);same(summary['generic_unramified_radius_results'],la['shared_radius_with_generic_local_rule'])
        fields=['observation_index','profile','baseline_unique_targets','first_local_unique_targets','joint_unique_targets','joint_unique_support']
        same(summary['local_feedback_results'],[{k:c[k] for k in fields} for c in l['cases']])
        assert [c['joint_unique_targets'] for c in l['cases']]==[17]*4
        assert [c['joint_unique_support'] for c in l['cases']]==[45,45,37,38]
    receipts=read(OUT/'Execution_Receipts.json')
    assert len(receipts)==7 and all(r['returncode']==0 and not r['timed_out'] for r in receipts.values())
    assert max(receipts[n]['started_utc'] for n in ['shared-error224','shared-error320'])<receipts['independent-shared-replay']['started_utc']
    assert max(receipts[n]['started_utc'] for n in ['local-spectral160','local-spectral224'])<receipts['independent-local-replay']['started_utc']
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r and set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
    for path,digest in read(OUT/'Inherited_Inputs.json')['files_sha256'].items():assert sha((ROOT/path).read_bytes())==digest
    source=read(OUT/'Primary_Sources.json');assert source['new_downloads']==0
    assert source['inherited_record_sha256']==sha((PRIOR/'Primary_Sources.json').read_bytes())
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert set(before)==set(after) and len(after)==117 and queue['new_branches']==[] and queue['advanced_existing_branches']==ADVANCED
    assert queue['global_exhaustion_claimed'] is False and queue['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:
            assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition']
            assert a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes()
    assert len(prefix.splitlines())==388 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==393
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'AGGREGATE_SHARED_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Recursive preceding-checkpoint verification, fresh two-precision shared bounds and local feedback, complex interval and exact integer replay, displaced controls, and ten semantic proof-component mutations. Shared interval routes both use FLINT; the full analytic argument is not formalized.',
        'manifest_files':len(manifest['files']),'preceding_checkpoint_integrity':'passed','measurement_rows_per_spectrum':17,'generic_coefficients':604,
        'joint_unique_targets':[17,17],'joint_unique_support_degree_only':[45,37],'joint_unique_support_degree_discriminant':[45,38],
        'largest_tested_shared_box_radii':['1/500','1/20'],'largest_tested_shared_unramified_radii':['1/200','1/20'],
        'stored_leaf_midpoints_checked':39600,'fresh_complex_interval_leaves':47520,'exact_objective_bounds':144,
        'local_exclusions':3162,'linear_exclusions':190,'independent_displaced_controls':96,'common_error_premise_controls':2,
        'actual_component_mutations_rejected':10,'recorded_commands':7,'failed_commands':0,
        'research_branches':117,'ledger_events':393,'preserved_event_prefix':388,'ledger_head_sha256':last,'local_links':links},indent=2))

if __name__=='__main__':main()
