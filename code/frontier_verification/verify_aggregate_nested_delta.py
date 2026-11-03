"""Verify nested noise domains, fresh numerical recovery and a kernel-checked transfer rule."""
import hashlib,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_aggregate_nested as nested
import dedekind_aggregate_nested_audit as audit
import dedekind_aggregate_adaptive_closure as closure
import dedekind_aggregate_nested_adversary as adversary
import check_noise_box_lean as lean
from verify_aggregate_moment_delta import quiet,same,unpack,canonical
from verify_aggregate_adaptive_delta import summarize as adaptive_summary

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-aggregate-nested-delta';PRIOR=ROOT/'docs/frontier/2026-09-13-aggregate-adaptive-delta';BASELINE=ROOT/'docs/frontier/2026-09-13-aggregate-delta'
ADVANCED=['R12','R13','R14','R15','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())

def summarize(data,checked,closed):
    result=adaptive_summary(data,checked,closed);gates=[]
    for obs in [0,1]:
        for profile in ['degree_only','degree_discriminant']:
            selected=[c for c in closed['cases'] if c['observation_index']==obs and c['profile']==profile]
            best=max(F(c['radius']) for c in selected if c['unique_targets']==17)
            next_radius=min(F(c['radius']) for c in selected if F(c['radius'])>best and c['unique_targets']<17)
            gates.append({'observation_index':obs,'profile':profile,'largest_tested_all_target_radius':str(best),'next_tested_nonclosure_radius':str(next_radius),
                          'scope':'The smaller endpoint is a sufficient recovery certificate and transfers to contained smaller boxes. The larger endpoint is a stalled tested update, not an impossibility or optimality bound.'})
    result['noise_test_gates']=gates;result['transported_root_intervals']=checked['transported_root_intervals']
    return result

def main():
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_adaptive_delta.py')],capture_output=True,text=True)
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
        unpack(BASELINE/'Aggregate_Inputs.zip',tmp,['S1_160.json','S2_160.json','S1_224.json','S2_224.json'])
        unpack(BASELINE/'Measurements_Recovery.zip',tmp,['Measurements160.json','Measurements224.json','Recovery160.json','Recovery224.json'])
        unpack(OUT/'Nested_Feedback.zip',tmp,['Nested_Feedback.json'])
        m=tmp/'Measurements224.json';inputs=[tmp/'S1_224.json',tmp/'S2_224.json'];seed=PRIOR/'Audit_Closure.json';pm=PRIOR/'Manifest.json';pv=PRIOR/'Verification.json'
        dp=tmp/'Nested_Feedback.json';ap=OUT/'Nested_Audit.json';cp=OUT/'Nested_Closure.json';lp=OUT/'Lean_Check.json';truth=BASELINE/'Integer_Audit.json'
        data=read(dp);same(data,quiet(nested.run,m,inputs,seed,pm,pv))
        checked=read(ap);same(checked,quiet(audit.run,dp,m,inputs,seed,pm,pv,truth))
        closed=read(cp);same(closed,quiet(closure.run,dp,ap,m,truth))
        attacked=read(OUT/'Adversary_Audit.json');same(attacked,quiet(adversary.run,dp,ap,cp,inputs,seed,lp))
        # Prior Manifest/Verification names intentionally map to the prior package.
        paths={p.name:p for p in [m,dp,ap,cp,lp,truth,seed,pm,pv]+inputs}
        for document in [data,checked,closed,attacked]:
            for name,digest in document['inputs_sha256'].items():assert sha(paths[name].read_bytes())==digest
        summary=summarize(data,checked,closed);same(summary,read(OUT/'Nested_Summary.json')['derived_results'])
        assert len(data['cases'])==24 and len(data['certificates'])==470 and summary['all_sampled_lp_statuses_success']
        assert (checked['transported_root_intervals'],checked['stored_midpoints_checked'],checked['fresh_quadratic_interval_leaves'],checked['exact_domain_objectives'],checked['independent_displaced_control_count'])==(540,110832,221664,470,412)
        assert (checked['local_removals'],checked['dual_removals'],closed['local_removals'],closed['dual_removals'])==(100,132,0,0)
        assert summary['additional_audit_exclusions_across_rounds']==4
        matrix=[]
        for radius in nested.RADII:
            matrix.append([next(c['unique_targets'] for c in closed['cases'] if c['radius']==radius and c['observation_index']==obs and c['profile']=='degree_discriminant') for obs in [0,1]])
        assert matrix==[[15,11],[17,13],[17,13],[17,17],[17,17],[17,17]]
        assert attacked['actual_component_mutations_rejected']==10
        witness=attacked['rounded_radius_counterexample'];assert F(witness['exact_outward_increase'])==F(1,10**21)
        assert float(F(witness['inner_radius']))==float(F(witness['seed_radius']))
        recorded=read(lp);project=ROOT.parent/'acs-research/lean-audit/withMathlib';binary=ROOT.parent/'acs-research/runtime/lean-4.34.0-rc2-darwin_aarch64/bin'
        assert quiet(lean.run,CODE/'proofs/NoiseBoxTransfer.lean',project,binary,tmp/'Fresh_Lean.json',tmp/'lean-versions')==0
        fresh=read(tmp/'Fresh_Lean.json')
        for key in recorded:
            if key!='command':same(recorded[key],fresh[key])
        with zipfile.ZipFile(OUT/'Lean_Artifacts.zip') as z:
            assert set(z.namelist())=={'Lean_Check.json','Lean_Check.olean','NoiseBoxTransfer.lean'}
            same(json.loads(z.read('Lean_Check.json')),recorded)
            assert sha(z.read('Lean_Check.olean'))==recorded['olean_sha256'] and sha(z.read('NoiseBoxTransfer.lean'))==recorded['source_sha256']
        assert len(recorded['theorems'])==4 and 'sorryAx' not in recorded['stdout']
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==5 and all(r['returncode']==0 and not r['timed_out'] for r in receipts.values())
    ordered=['nested-radius-feedback','independent-nested-audit','nested-audit-closure','nested-transfer-adversary']
    assert [receipts[k]['started_utc'] for k in ordered]==sorted(receipts[k]['started_utc'] for k in ordered)
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r and set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
    for path,digest in read(OUT/'Inherited_Inputs.json')['files_sha256'].items():assert sha((ROOT/path).read_bytes())==digest
    sources=read(OUT/'Primary_Sources.json');assert sources['new_downloads']==0 and sources['inherited_record_sha256']==sha((BASELINE/'Primary_Sources.json').read_bytes())
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert set(before)==set(after) and len(after)==117 and queue['new_branches']==[] and queue['advanced_existing_branches']==ADVANCED
    assert queue['global_exhaustion_claimed'] is False and queue['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:
            assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==408 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==413
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'AGGREGATE_NESTED_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Fresh nested-domain proposals and real certificates, independent complex/rational/integer audits, exact supplemental closure, ten transfer mutations and fresh Lean compilation. Prior checkpoints verified recursively. The transfer theorem concerns box geometry; the full arithmetic proof is unformalized, and tested nonclosure is not an impossibility bound.',
        'manifest_files':len(manifest['files']),'preceding_checkpoint_integrity':'passed','target_count':17,'measurement_rows':17,'generic_coefficients':604,
        'radii':nested.RADII,'degree_discriminant_final_unique_targets':matrix,'local_profiles':2,'nested_cases':24,'new_multiplier_cases':470,
        'transported_root_intervals':540,'stored_midpoints_checked':110832,'fresh_quadratic_interval_leaves':221664,'exact_domain_objectives':470,'independent_displaced_controls':412,
        'local_removals':100,'dual_removals':132,'supplemental_local_removals':0,'supplemental_dual_removals':0,'actual_component_mutations_rejected':10,
        'kernel_checked_transfer_theorems':4,'fresh_lean_compilation':'passed','recorded_commands':5,'failed_commands':0,
        'research_branches':117,'ledger_events':413,'preserved_event_prefix':408,'ledger_head_sha256':last,'local_links':links},indent=2))

if __name__=='__main__':main()
