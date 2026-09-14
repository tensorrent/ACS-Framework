"""Replay signed corner evidence, independent formulas, proof failures and ACS history."""
import hashlib,importlib.metadata,json,os,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_signed_corner_certificate as certificate
import dedekind_signed_corner_audit as audit
import dedekind_signed_corner_adversary as adversary
import check_signed_corner_lean as lean
from verify_aggregate_classification_delta_v2 import same,canonical,quiet

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-14-aggregate-signed-corner-delta'
PRIOR=ROOT/'docs/frontier/2026-09-14-aggregate-variable-noise-delta'
ADVANCED=['R12','R13','R14','R15','K04'];FAILURES=['lean-draft-v1','lean-proof-v1']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def stage(s):print(s,file=sys.stderr,flush=True)
def summarize(cert,checked,adv,formal):
    assert cert['status']==checked['status']==adv['status']==formal['status']=='passed'
    return {**{k:cert[k] for k in ['matrix_family','corner_uniform_inverse_bound','corner_bound_display','uniform_identification_strictly_below','guarantee_display','previous_uniform_guarantee','inherited_ambiguity_upper_endpoint','upper_to_guarantee_ratio','ratio_display','relative_guarantee_increase_display']},
        'feature_dimension':22,'source_population':22,'source_cutoff':'39/2','coordinate_cube_radius':'1/100',
        'root_coordinate_error_radius':cert['contract']['root_coordinate_error_radius'],
        'signed_region_bounds':[{k:x[k] for k in ['radius','unresolved_row_sign_indices','signed_uniform_inverse_bound','signed_bound_display','signed_noise_guarantee_strictly_below','signed_guarantee_display']} for x in cert['signed_regions']],
        'uniform_curvature_signs':22,'global_inverse_direction_signs':21,'remaining_direction_coordinate':12,'face_direction_sign':-1,
        'curvature_precision_bits':[896,1152],'direct_corner_precision_bits':[1024,1536],'independent_Cramer_precision_bits':[896,1152],
        'factorizations':checked['factorization_count'],'coefficient_comparisons':checked['coefficient_comparisons'],'fixed_coefficients':456,'ambiguous_coefficients':148,
        'mutations_rejected':adv['mutations_rejected'],'exact_counterexample_controls':len(adv['exact_counterexample_controls']),'Lean_lemmas':len(formal['theorems']),
        'new_source_roots':0,'entire_bridge_Lean_formalized':False,'sharp_source_feasible_threshold_proved':False,'arbitrary_report_decoder_implemented':False}

def replay_explorations():
    with tempfile.TemporaryDirectory() as directory,zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        tmp=Path(directory);base=tmp/'work/acs-research/signed-stability-audit';base.mkdir(parents=True);repo=tmp/'work/acs-repo'
        for relative in [certificate.ANCHOR,certificate.REGION,audit.OWN]:
            target=repo/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/relative).read_bytes())
        (repo/'code').mkdir();(repo/'code/frontier_verification').symlink_to(CODE,target_is_directory=True)
        pairs=[('explore_signed_resolvent.py','Signed_Resolvent_Exploration.json'),('explore_gradient_signs.py','Gradient_Sign_Exploration.json'),('explore_corner_inverse.py','Corner_Inverse_Exploration.json'),('audit_gradient_candidate.py','Independent_Gradient_Candidate_Audit.json')]
        for script,report in pairs:
            p=base/script;p.write_bytes(z.read('exploration/'+script))
            result=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
            assert result.returncode==0,result.stdout+result.stderr;same(read(base/report),read(OUT/report))
            assert sha((base/report).read_bytes())==sha((OUT/report).read_bytes()),report

def main():
    stage('Checking signed corner provenance and replaying all four original explorations')
    manifest=read(OUT/'Manifest.json');inventory=read(OUT/'Source_Inventory.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert digest==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
        for kind in ['external_runtime_sources','exploration_sources','packaging_sources']:
            for name,digest in inventory[kind].items():assert sha(z.read(name))==digest
    replay_explorations()
    stage('Fresh signed resolvents, whole-family curvature signs and inverse/determinant corner checks')
    cert=read(OUT/'Signed_Corner_Certificate.json');same(cert,quiet(certificate.run))
    checked=read(OUT/'Independent_Signed_Corner_Audit.json');same(checked,quiet(audit.run,OUT/'Signed_Corner_Certificate.json'))
    adv=read(OUT/'Adversary_Audit.json');same(adv,quiet(adversary.run,OUT/'Signed_Corner_Certificate.json'))
    assert checked['factorization_count']==1128 and checked['coefficient_comparisons']==1208 and adv['mutations_rejected']==28 and len(adv['exact_counterexample_controls'])==9
    stage('Fresh Lean algebra/Cramer/endpoint proofs and reproduction of the failed draft')
    formal=read(OUT/'Lean_Check.json');project=ROOT.parent/'acs-research/lean-audit/withMathlib';binary=ROOT.parent/'acs-research/runtime/lean-4.34.0-rc2-darwin_aarch64/bin'
    with tempfile.TemporaryDirectory() as directory,zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        tmp=Path(directory)
        assert quiet(lean.run,CODE/'proofs/SignedCornerStability.lean',project,binary,tmp/'Fresh_Lean.json',tmp/'versions')==0
        fresh=read(tmp/'Fresh_Lean.json')
        for key in ['status','source_sha256','checker_sha256','returncode','stdout','stderr','olean_sha256','lake_manifest_sha256','theorems']:same(fresh[key],formal[key])
        old=tmp/'SignedCornerStability_v1.lean';old.write_bytes(z.read('exploration/SignedCornerStability_v1.lean'))
        assert quiet(lean.run,old,project,binary,tmp/'Failed_Lean.json',tmp/'versions')!=0
        failed=read(tmp/'Failed_Lean.json');original=read(OUT/'Lean_v1.json')
        assert failed['source_sha256']==original['source_sha256'] and failed['status']=='failed' and 'unknown tactic' in failed['stdout'] and 'synthInstanceFailed' in failed['stdout']
    assert len(formal['theorems'])==8 and 'sorryAx' not in formal['stdout']+formal['stderr']
    with zipfile.ZipFile(OUT/'Lean_Artifacts.zip') as z:
        assert set(z.namelist())=={'Lean_Check.json','Lean_Check.olean','SignedCornerStability.lean'};same(formal,json.loads(z.read('Lean_Check.json')))
        assert sha(z.read('Lean_Check.olean'))==formal['olean_sha256']
        assert sha(z.read('SignedCornerStability.lean'))==formal['source_sha256']==sha((CODE/'proofs/SignedCornerStability.lean').read_bytes())
    acquisition=read(OUT/'Source_Acquisition.json');mathlib=project/'.lake/packages/mathlib';assert acquisition['status']=='passed'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathlib,text=True).strip()==acquisition['mathlib_revision']
    for entry in acquisition['pinned_sources']:
        raw=(mathlib/entry['path']).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'] and entry['matches_pinned_git_object']
        assert subprocess.check_output(['git','show','HEAD:'+entry['path']],cwd=mathlib)==raw
    runtime=read(OUT/'Runtime.json')
    for key,pkg in [('python_flint','python-flint'),('sympy','sympy'),('numpy','numpy'),('scipy','scipy'),('mpmath','mpmath'),('pytest','pytest'),('clarabel','clarabel'),('cffi','cffi'),('pycparser','pycparser')]:assert runtime[key]==importlib.metadata.version(pkg)
    summary=summarize(cert,checked,adv,formal);same(summary,read(OUT/'Signed_Corner_Summary.json')['derived_results'])
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==12 and sorted(n for n,r in receipts.items() if r['returncode'])==FAILURES and all(not r['timed_out'] for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        assert len(z.namelist())==3*len(receipts)
        for name,record in receipts.items():
            same(record,json.loads(z.read(name+'/receipt.json')));assert set(record['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==record[stream+'_sha256']
        assert 'no such file or directory' in z.read('lean-draft-v1/stderr.txt').decode()
    for name,key in [('Inherited_Inputs.json','files_sha256'),('Primary_Sources.json','inherited_source_records_sha256')]:
        for path,digest in read(OUT/name)[key].items():assert sha((ROOT/path).read_bytes())==digest
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};q=read(OUT/'Research_Queue.json');after={b['id']:b for b in q['branches']}
    assert set(before)==set(after) and len(after)==117 and q['new_branches']==[] and q['advanced_existing_branches']==ADVANCED and not q['global_exhaustion_claimed']
    assert q['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==453 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        event=json.loads(line);digest=event.pop('event_sha256');assert event['sequence']==index and event['previous_event_sha256']==last and sha(canonical(event))==digest;last=digest
    assert index==458;links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'SIGNED_CORNER_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    stage('All new checks passed; recursively verifying the preceding ACS evidence chain')
    prior=subprocess.run([sys.executable,str(CODE/'verify_aggregate_variable_noise_delta.py')],capture_output=True,text=True)
    assert prior.returncode==0,prior.stdout+prior.stderr
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'manifest_files':len(manifest['files']),
        'fresh_original_explorations':'passed','fresh_signed_resolvent_and_corner_certificates':'passed','fresh_independent_real_polynomial_and_Cramer_audit':'passed',
        'fresh_adversarial_audit':'passed','fresh_Lean_compilation':'passed','failed_Lean_draft_reproduced':'passed','preceding_checkpoint_integrity':'passed',
        'derived_results':summary,'recorded_commands':12,'successful_commands':10,'failed_commands':2,'research_branches':117,'ledger_events':458,'preserved_event_prefix':453,
        'ledger_head_sha256':last,'local_links':links,'entire_bridge_Lean_formalized':False,
        'scope':'The written convex column-family proof and checked signs yield a stronger uniform finite-difference bound. Independent real polynomials and Cramer determinants confirm the numerical premises. The unchanged local source/error contract has a remaining threshold bracket of about 1.7 percent. Source-constrained sharpness, general decoding, wider regions and all ACS branches remain open.'},indent=2))
if __name__=='__main__':main()
