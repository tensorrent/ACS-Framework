"""Freshly verify simultaneous cuts, exhaustive projection and signed-discriminant recovery."""
import copy,gc,hashlib,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from pathlib import Path
import dedekind_aggregate_primal_pool as pool
import dedekind_aggregate_primal_audit as cut_audit
import dedekind_aggregate_primal_models as models
import dedekind_aggregate_primal_model_audit as model_audit
import dedekind_aggregate_primal_branch_audit as branch_audit
import dedekind_aggregate_discriminant_parity as parity
import dedekind_aggregate_parity_audit_v2 as parity_audit
import dedekind_aggregate_primal_adversary as adversary
from verify_aggregate_moment_delta import quiet,same,canonical,unpack

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-14-aggregate-primal-delta';PRIOR=ROOT/'docs/frontier/2026-09-13-aggregate-nested-delta';BASELINE=ROOT/'docs/frontier/2026-09-13-aggregate-delta'
ADVANCED=['R12','R13','R14','R15','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def stage(s):print(s,file=sys.stderr,flush=True)
def summarize(ca,ma,ja,pa,adv):
    return {'directions_by_observation':[len(o['cuts']) for o in ca['observations']],
            **{k:ca[k] for k in ['exact_global_cuts','stored_midpoints_checked','fresh_quadratic_interval_leaves','independent_displaced_controls']},
            **{k:ma[k] for k in ['exact_model_hull_objectives','local_removals','dual_removals','verified_selected_witnesses','verified_full_pool_witnesses']},
            **{k:ja[k] for k in ['joint_assignments','refuted_branches','feasible_branches','unresolved_branches']},
            'joint_relaxation_unique_targets':[c['final_unique_targets_after_branch_refutations'] for c in ja['cases']],
            'parity_results':[{k:c[k] for k in ['observation_index','radius','seed_profile','unique_targets']} for c in pa['cases']],
            'permutation_checks':pa['permutation_checks'],'even_permutations':pa['even_permutations'],
            'parity_integer_witnesses':sum(b['retained'] for c in pa['cases'] for b in c['branch_replays']),
            'parity_refuted_relaxed_tuples':sum(not b['retained'] for c in pa['cases'] for b in c['branch_replays']),
            'actual_component_mutations_rejected':adv['actual_component_mutations_rejected'],'optimal_but_infeasible_proposals':len(adv['optimal_but_infeasible_proposals'])}

def main():
    stage('Verifying all preceding checkpoints recursively')
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_nested_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    manifest=read(OUT/'Manifest.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,d in inventory[kind].items():assert d==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory)
        unpack(BASELINE/'Aggregate_Inputs.zip',tmp,['S1_160.json','S2_160.json','S1_224.json','S2_224.json'])
        unpack(BASELINE/'Measurements_Recovery.zip',tmp,['Measurements160.json','Measurements224.json','Recovery160.json','Recovery224.json'])
        unpack(ROOT/'docs/frontier/2026-09-13-aggregate-adaptive-delta/Adaptive_Feedback.zip',tmp,['Adaptive_Feedback.json'])
        unpack(PRIOR/'Nested_Feedback.zip',tmp,['Nested_Feedback.json'])
        for n in ['Pool_A','Pool_B']:unpack(OUT/(n+'.zip'),tmp,[n+'.json'])
        m=tmp/'Measurements224.json';inputs=[tmp/'S1_224.json',tmp/'S2_224.json'];truth=BASELINE/'Integer_Audit.json'
        pp=[tmp/'Pool_A.json',tmp/'Pool_B.json'];cp=OUT/'Global_Cut_Audit.json';mp=OUT/'Model_Hull_Witnesses.json';mapath=OUT/'Model_Witness_Audit.json'
        bp=OUT/'Joint_Target_Branches.json';jp=OUT/'Joint_Projection_Audit.json';dp=OUT/'Discriminant_Parity.json';pap=OUT/'Parity_Audit.json';ap=OUT/'Adversary_Audit.json'
        stage('Freshly regenerating 351 real continuum certificates')
        fresh=quiet(pool.run,m,inputs,tmp/'Recovery224.json',ROOT/'docs/frontier/2026-09-13-aggregate-optimized-delta/Proposals.json',ROOT/'docs/frontier/2026-09-13-aggregate-moment-delta/Moment_Proposals.json',tmp/'Adaptive_Feedback.json',tmp/'Nested_Feedback.json')
        for p,d in zip(pp,fresh):same(read(p),d)
        del fresh;gc.collect()
        stage('Freshly replaying complex quadratic intervals, rational moments and all global cuts')
        ca=read(cp);same(ca,quiet(cut_audit.run,pp,m,inputs,truth))
        stage('Fresh model-hull LP deductions; independent stored-point and complete branch replay')
        recorded=read(mp);fresh=quiet(models.run,cp,PRIOR/'Nested_Closure.json',PRIOR/'Manifest.json',PRIOR/'Verification.json',False)
        stripped=copy.deepcopy(recorded);stripped['witness_search_performed']=False
        for c in stripped['cases']:c['witness_proposals']=[]
        same(stripped,fresh);del stripped,fresh;gc.collect()
        ma=read(mapath);same(ma,quiet(model_audit.run,mp,cp,PRIOR/'Nested_Closure.json',m,truth))
        ja=read(jp);same(ja,quiet(branch_audit.run,bp,mp,mapath,cp,m,truth))
        assert (ja['joint_assignments'],ja['refuted_branches'],ja['feasible_branches'],ja['unresolved_branches'])==(99,91,8,0)
        assert all(b['all_unrounded_real_cuts_strictly_satisfied'] for c in ja['cases'] for b in c['branch_replays'] if b['status']=='feasible_integer_witness')
        stage('Fresh discriminant projection, independent parity witnesses and semantic mutations')
        pd=read(dp);fresh=quiet(parity.run,bp,jp,mp,cp,inputs,False);stripped=copy.deepcopy(pd);stripped['witness_search_performed']=False
        for c in stripped['cases']:
            for b in c['branches']:b['witness']=None
        same(stripped,fresh)
        pa=read(pap);same(pa,quiet(parity_audit.run,dp,bp,jp,mp,cp,m,inputs,truth))
        adv=read(ap);same(adv,quiet(adversary.run,bp,jp,mp,mapath,cp,dp,m,inputs,truth))
        summary=summarize(ca,ma,ja,pa,adv);same(summary,read(OUT/'Primal_Summary.json')['derived_results'])
        assert summary['directions_by_observation']==[163,188] and summary['exact_global_cuts']==351
        assert (summary['stored_midpoints_checked'],summary['fresh_quadratic_interval_leaves'],summary['independent_displaced_controls'])==(378480,756960,1404)
        assert (summary['exact_model_hull_objectives'],summary['local_removals'],summary['dual_removals'])==(52,0,0)
        assert (summary['verified_selected_witnesses'],summary['verified_full_pool_witnesses'])==(66,37)
        assert len(pa['cases'])==4 and all(c['unique_targets']==17 for c in pa['cases'])
        assert summary['parity_integer_witnesses']==summary['parity_refuted_relaxed_tuples']==4 and adv['actual_component_mutations_rejected']==10
        assert len(adv['optimal_but_infeasible_proposals'])==12
    stage('Checking frozen sources, command receipts and append-only research history')
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==12
    assert {k for k,r in receipts.items() if r['returncode']!=0}=={'primary-source-acquisition','independent-parity-audit'}
    assert all(not r['timed_out'] for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r and set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
        source_record=read(OUT/'Primary_Sources.json');same(json.loads(z.read('primary-source-acquisition-browser-header/stdout.txt')),source_record)
    assert source_record['status']=='passed' and source_record['new_downloads']==len(source_record['sources'])==2
    for src in source_record['sources']:assert src['url'].startswith('https://www.jmilne.org/') and src['bytes']>1000000 and len(src['sha256'])==64 and not src['redistributed_in_repository']
    for path,d in read(OUT/'Inherited_Inputs.json')['files_sha256'].items():assert sha((ROOT/path).read_bytes())==d
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert set(before)==set(after) and len(after)==117 and queue['new_branches']==[] and queue['advanced_existing_branches']==ADVANCED
    assert queue['global_exhaustion_claimed'] is False and queue['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==413 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);d=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==d;last=d
    assert index==418
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'AGGREGATE_PRIMAL_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'manifest_files':len(manifest['files']),
        'preceding_checkpoint_integrity':'passed','derived_results':summary,'fresh_real_and_complex_interval_replay':'passed','fresh_model_hull_LP_replay':'passed',
        'complete_joint_projection_and_exact_separation_replay':'passed','fresh_parity_deduction_and_witness_audit':'passed',
        'new_MILP_search_repeated_in_final_verifier':False,'joint_branch_LP_search_repeated_in_final_verifier':False,
        'new_number_theory_formalized_in_Lean':False,'recorded_commands':12,'successful_commands':10,'failed_commands':2,
        'research_branches':117,'ledger_events':418,'preserved_event_prefix':413,'ledger_head_sha256':last,'local_links':links,
        'scope':'Fresh continuum and LP deduction replay, independent exact finite projection and all stored witnesses, derived signed-discriminant parity and semantic controls. General arithmetic derivation is source-backed written mathematics. Success certifies necessary target recovery under the declared data contract; it does not classify all fields or prove optimal noise thresholds. Ongoing research remains active.'},indent=2))

if __name__=='__main__':main()
