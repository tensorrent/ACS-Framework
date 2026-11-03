"""Verify coupled moment uncertainty, noisy target feedback and preserved research history."""
import contextlib,hashlib,io,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_aggregate_moment_proposals as proposals
import dedekind_aggregate_moment_certificate as certificate
import dedekind_aggregate_moment_local as local
import dedekind_aggregate_moment_audit as audit
import dedekind_aggregate_moment_feedback as feedback
import dedekind_aggregate_moment_local_audit as local_audit
import dedekind_aggregate_moment_adversary as adversary
from dedekind_aggregate_integer_audit import endpoint,GRID

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-aggregate-moment-delta';PRIOR=ROOT/'docs/frontier/2026-09-13-aggregate-optimized-delta';BASELINE=ROOT/'docs/frontier/2026-09-13-aggregate-delta'
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

def summarize(c,l,f,a,la):
    local_fields=['observation_index','radius','spectral_method','profile','spectral_unique_targets','local_unique_targets','local_unique_support']
    feedback_fields=['observation_index','radius','method','profile','spectral_unique_targets','first_local_unique_targets','feedback_unique_targets','feedback_unique_support']
    feedback_summary=[]
    for row in f['cases']:
        feedback_summary.append({**{k:row[k] for k in feedback_fields},'iterations':len(row['rounds']),
            'remaining_target_domains':[{'n':col['n'],'candidates':domain} for col,domain in zip(f['columns'],row['final_domains']) if col['n']<=31 and len(domain)>1]})
    selected=[r for r in c['cases'] if r['joint_selected']];gains=[]
    for row in selected:
        s=F(endpoint(row['methods']['separate']['total_zero_and_input_budget'],True),GRID)
        j=F(endpoint(row['methods']['coupled']['total_zero_and_input_budget'],True),GRID)
        if s>0:gains.append(((s-j)/s,row))
    largest,row=max(gains,key=lambda x:x[0])
    differences=[{**{k:r[k] for k in ['observation_index','radius','n','sign','multiplier_source']},'separate':r['methods']['separate']['candidates'],'coupled':r['methods']['coupled']['candidates']} for r in c['cases'] if r['methods']['separate']['candidates']!=r['methods']['coupled']['candidates']]
    return {'raw_spectral_results':c['results'],'one_pass_local_results':[{k:r[k] for k in local_fields} for r in l['cases']],
            'feedback_results':feedback_summary,'joint_budget_selected_cases':len(selected),'joint_budget_selected_by_radius':{radius:sum(r['radius']==radius for r in selected) for radius in c['radii']},
            'largest_relative_budget_reduction':{'ratio':str(largest),**{k:row[k] for k in ['observation_index','radius','n','sign','multiplier_source']}},
            'producer_candidate_differences_between_budget_methods':differences,'independent_candidate_improvements':a['independent_candidate_improvements'],
            'one_pass_local_removals':la['one_pass_local_removals'],'feedback_local_removals':la['feedback_local_removals'],'feedback_dual_removals':la['feedback_dual_removals']}

def main():
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_optimized_delta.py')],capture_output=True,text=True)
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
        unpack(OUT/'Moment_Certificates.zip',tmp,['Moment_Certificate.json'])
        unpack(OUT/'Local_Feedback.zip',tmp,['Moment_Local.json','Moment_Feedback.json'])
        m=tmp/'Measurements224.json';inputs=[tmp/'S1_224.json',tmp/'S2_224.json'];pp=OUT/'Moment_Proposals.json';old=PRIOR/'Proposals.json'
        cp=tmp/'Moment_Certificate.json';lp=tmp/'Moment_Local.json';fp=tmp/'Moment_Feedback.json';ap=OUT/'Moment_Audit.json';lap=OUT/'Moment_Local_Audit.json';truth=BASELINE/'Integer_Audit.json'
        proposed=read(pp);same(proposed,quiet(proposals.run,m,inputs));assert len(proposed['cases'])==272 and all(c['solver_status']==0 for c in proposed['cases'])
        same(read(cp),quiet(certificate.run,m,pp,old,inputs))
        same(read(lp),quiet(local.run,cp))
        same(read(ap),quiet(audit.run,cp,m,pp,old,inputs,truth))
        same(read(fp),quiet(feedback.run,m,pp,old,ap))
        same(read(lap),quiet(local_audit.run,lp,fp,cp,ap,m,pp,old,truth))
        same(read(OUT/'Adversary_Audit.json'),quiet(adversary.run,cp,fp,ap,m,pp,old,inputs,truth))
        datasets=[proposed,read(cp),read(lp),read(ap),read(fp),read(lap),read(OUT/'Adversary_Audit.json')]
        for data in datasets:
            for name,digest in data['inputs_sha256'].items():
                path=next(p for p in [tmp/name,OUT/name,PRIOR/name,BASELINE/name] if p.exists());assert sha(path.read_bytes())==digest
        c,l,a,f,la=datasets[1:6];summary=summarize(c,l,f,a,la);same(summary,read(OUT/'Moment_Summary.json')['derived_results'])
        assert len(c['cases'])==288 and len(l['cases'])==len(f['cases'])==32
        assert a['stored_midpoints_checked']==104592 and a['fresh_quadratic_interval_leaves']==209184 and a['exact_objective_bounds']==576
        assert a['symbolic_moment_derivative_checks']==3 and len(a['independent_displaced_controls'])==528
        assert summary['joint_budget_selected_cases']==97 and summary['joint_budget_selected_by_radius']=={'0':0,'1/200':35,'1/50':34,'1/10':28}
        assert summary['producer_candidate_differences_between_budget_methods']==[] and len(a['independent_candidate_improvements'])==2
        assert (la['one_pass_local_removals'],la['feedback_local_removals'],la['feedback_dual_removals'])==(12326,12396,56)
        assert datasets[-1]['actual_component_mutations_rejected']==10 and datasets[-1]['search_probes']==[{'name':'finite_only_leaf_substitution','witness_found':True}]
        matrix=[]
        for radius in ['0','1/200','1/50','1/10']:
            matrix.append([next(r['feedback_unique_targets'] for r in f['cases'] if r['observation_index']==obs and r['radius']==radius and r['method']=='coupled' and r['profile']=='degree_discriminant') for obs in [0,1]])
        assert matrix==[[14,13],[13,13],[13,13],[13,10]]
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==7 and all(r['returncode']==0 and not r['timed_out'] for r in receipts.values())
    assert receipts['joint-moment-proposals']['started_utc']<receipts['joint-moment-certificate']['started_utc']<receipts['independent-moment-audit']['started_utc']
    assert receipts['noisy-dual-local-feedback']['started_utc']<receipts['independent-noisy-local-audit']['started_utc']
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
            assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition']
            assert a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==398 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==403
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'AGGREGATE_MOMENT_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Fresh joint-moment proposals, continuum bounds, local projections, frozen-dual feedback, complex/rational/integer audits and semantic controls. Prior history verified recursively. Shared FLINT backend and unformalized analytic premises remain explicit; neither surviving domains nor frozen-family fixed points prove optimality or global ambiguity.',
        'manifest_files':len(manifest['files']),'preceding_checkpoint_integrity':'passed','target_count':17,'measurement_rows':17,'generic_coefficients':604,
        'radii':['0','1/200','1/50','1/10'],'degree_discriminant_feedback_unique_targets':matrix,'proposal_count':272,'validated_multiplier_cases':288,
        'joint_budget_selected_cases':97,'new_producer_integer_domains_from_joint_budget':0,'stored_midpoints_checked':104592,'fresh_quadratic_interval_leaves':209184,
        'exact_objective_bounds':576,'symbolic_moment_derivative_checks':3,'independent_displaced_controls':528,'independent_candidate_improvements':2,
        'one_pass_local_removals':12326,'feedback_local_removals':12396,'feedback_dual_removals':56,'actual_component_mutations_rejected':10,
        'recorded_commands':7,'failed_commands':0,'research_branches':117,'ledger_events':403,'preserved_event_prefix':398,'ledger_head_sha256':last,'local_links':links},indent=2))

if __name__=='__main__':main()
