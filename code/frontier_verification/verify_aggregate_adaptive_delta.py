"""Verify adaptive multiplier recovery, audit closure, adversaries and append-only history."""
import hashlib,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_aggregate_adaptive as adaptive
import dedekind_aggregate_adaptive_audit as audit
import dedekind_aggregate_adaptive_closure as closure
import dedekind_aggregate_adaptive_adversary as adversary
from verify_aggregate_moment_delta import quiet,same,unpack,canonical
from dedekind_aggregate_integer_audit import endpoint,GRID

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-aggregate-adaptive-delta';PRIOR=ROOT/'docs/frontier/2026-09-13-aggregate-moment-delta';BASELINE=ROOT/'docs/frontier/2026-09-13-aggregate-delta'
ADVANCED=['R12','R13','R14','R15','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())

def summarize(data,checked,closed):
    results=[]
    for source,final in zip(data['cases'],closed['cases']):
        results.append({**{k:source[k] for k in ['observation_index','radius','profile','initial_unique_targets','adaptive_unique_targets','adaptive_unique_support']},
                        'adaptive_iterations':len(source['rounds']),'closure_iterations':len(final['rounds']),'final_unique_targets':final['unique_targets'],'final_unique_support':final['unique_support'],
                        'remaining_target_domains':[{'n':c['n'],'candidates':d} for c,d in zip(data['columns'],final['final_domains']) if c['n']<=31 and len(d)>1]})
    return {'results':results,'new_multiplier_cases':len(data['certificates']),
            'all_sampled_lp_statuses_success':all(p['solver_status']==0 for c in data['cases'] for s in c['rounds'] for p in s['proposals']),
            'adaptive_local_removals':checked['local_removals'],'adaptive_dual_removals':checked['dual_removals'],
            'additional_audit_exclusions_across_rounds':sum(len(r['additional_audit_exclusions_not_propagated']) for r in checked['domain_replays']),
            'supplemental_local_removals':closed['local_removals'],'supplemental_dual_removals':closed['dual_removals']}

def main():
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_moment_delta.py')],capture_output=True,text=True)
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
        unpack(PRIOR/'Local_Feedback.zip',tmp,['Moment_Local.json','Moment_Feedback.json'])
        unpack(OUT/'Adaptive_Feedback.zip',tmp,['Adaptive_Feedback.json'])
        m=tmp/'Measurements224.json';inputs=[tmp/'S1_224.json',tmp/'S2_224.json'];fp=tmp/'Moment_Feedback.json';pa=PRIOR/'Moment_Local_Audit.json'
        dp=tmp/'Adaptive_Feedback.json';ap=OUT/'Adaptive_Audit.json';cp=OUT/'Audit_Closure.json';truth=BASELINE/'Integer_Audit.json'
        data=read(dp);same(data,quiet(adaptive.run,m,inputs,fp,pa))
        checked=read(ap);same(checked,quiet(audit.run,dp,m,inputs,fp,pa,truth))
        closed=read(cp);same(closed,quiet(closure.run,dp,ap,m,truth))
        attacked=read(OUT/'Adversary_Audit.json');same(attacked,quiet(adversary.run,dp,ap,cp,m,inputs,fp,truth))
        for document in [data,checked,closed,attacked]:
            for name,digest in document['inputs_sha256'].items():
                path=next(p for p in [tmp/name,OUT/name,PRIOR/name,BASELINE/name] if p.exists());assert sha(path.read_bytes())==digest
        summary=summarize(data,checked,closed);same(summary,read(OUT/'Adaptive_Summary.json')['derived_results'])
        assert len(data['cases'])==16 and len(data['certificates'])==288 and summary['all_sampled_lp_statuses_success']
        assert (checked['stored_midpoints_checked'],checked['fresh_quadratic_interval_leaves'],checked['exact_domain_objectives'],checked['independent_displaced_control_count'])==(80976,161952,288,356)
        assert (checked['local_removals'],checked['dual_removals'],closed['local_removals'],closed['dual_removals'])==(87,109,0,2)
        assert summary['additional_audit_exclusions_across_rounds']==8
        matrix=[]
        for radius in ['0','1/200','1/50','1/10']:
            matrix.append([next(c['unique_targets'] for c in closed['cases'] if c['radius']==radius and c['observation_index']==obs and c['profile']=='degree_discriminant') for obs in [0,1]])
        assert matrix==[[17,17],[17,17],[17,17],[15,11]]
        assert attacked['actual_component_mutations_rejected']==10 and attacked['exact_general_domain_support_checks']==604
        witness=attacked['stale_budget_counterexample'];assert witness['multiplier_scale']==9 and F(endpoint(witness['strict_excess_over_stale_budget'],False),GRID)>F('0.383')
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==4 and all(r['returncode']==0 and not r['timed_out'] for r in receipts.values())
    ordered=['adaptive-dual-feedback','independent-adaptive-audit','audit-strengthened-closure','adaptive-lineage-adversary']
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
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==403 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==408
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'AGGREGATE_ADAPTIVE_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Fresh adaptive sampled proposals and real interval certificates, independent complex/rational/integer audits, supplemental exact closure and semantic controls. All preceding checkpoints verified recursively. This is a scoped recovery delta; surviving domains do not establish global feasibility or ambiguity, and a stalled sampled update does not prove optimality.',
        'manifest_files':len(manifest['files']),'preceding_checkpoint_integrity':'passed','target_count':17,'measurement_rows':17,'generic_coefficients':604,
        'radii':['0','1/200','1/50','1/10'],'degree_discriminant_final_unique_targets':matrix,'local_profiles':2,'adaptive_cases':16,'new_multiplier_cases':288,
        'stored_midpoints_checked':80976,'fresh_quadratic_interval_leaves':161952,'exact_domain_objectives':288,'independent_displaced_controls':356,
        'adaptive_local_removals':87,'adaptive_dual_removals':109,'supplemental_local_removals':0,'supplemental_dual_removals':2,
        'actual_component_mutations_rejected':10,'exact_general_domain_support_checks':604,'stale_budget_counterexample_multiplier_scale':9,
        'recorded_commands':4,'failed_commands':0,'research_branches':117,'ledger_events':408,'preserved_event_prefix':403,'ledger_head_sha256':last,'local_links':links},indent=2))

if __name__=='__main__':main()
