"""Replay variable-noise midpoint certificates, original searches and ACS history."""
import hashlib,importlib.metadata,json,os,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_variable_noise_certificate as certificate
import dedekind_variable_noise_audit as audit
import dedekind_variable_noise_adversary as adversary
import check_variable_noise_lean as lean
from verify_aggregate_classification_delta_v2 import same,canonical,quiet

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-14-aggregate-variable-noise-delta';PRIOR=ROOT/'docs/frontier/2026-09-14-aggregate-weighted-feature-delta'
ANCHOR=ROOT/'docs/frontier/2026-09-14-aggregate-augmented-feature-delta/Augmented_Proposals_Local.json'
SOURCE=ROOT/'docs/frontier/2026-09-14-aggregate-equal-population-delta';CLASS=ROOT/'docs/frontier/2026-09-14-aggregate-classification-delta';PAIR=ROOT/'docs/frontier/2026-09-13-biquadratic-delta'
ADVANCED=['R12','R13','R14','R15','K04'];FAILURES=['shifted-pair-exploration']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def stage(s):print(s,file=sys.stderr,flush=True)
def summarize(cert,checked,adv,formal,shifted):
    history=shifted['cases'][0]['history'];rejected=[x for x in history if not x['accepted']];assert len(history)==9 and len(rejected)==1
    assert rejected[0]['source_centers_feasible'] and rejected[0]['numerically_converged'] and F(rejected[0]['maximum_center_displacement'])>F(1,100)
    accepted=[x['tau_display'] for x in history if x['accepted']];assert len(accepted)==8 and all(x>y for x,y in zip(accepted,accepted[1:]))
    return {'certified_pair_count':cert['certified_pair_count'],'feature_dimension':22,'source_population':22,'source_cutoff':'39/2','root_coordinate_error_radius':cert['contract']['root_coordinate_error_radius'],
        'standard_coordinate_cube_radius':'1/100','root_unknowns':21,'scaled_noise_unknowns':1,'variable_cube_radius':'1e-120','tau_scale':'1e-10','critical_epsilon':cert['critical_epsilon'],
        'cases':[{'case_id':x['case_id'],'tau_interval':x['tau_interval'],'tau_upper_display':x['tau_upper_display'],'minimum_cube_margin':x['minimum_cube_margin'],
            'midpoint_component_0_difference_display':x['direct_checks'][0]['midpoint_component_0_difference_display']} for x in cert['cases']],
        'uniform_identification_below':cert['uniform_identification_below'],'best_certified_tau_upper':cert['best_certified_tau_upper'],'convenient_feature_budget':cert['convenient_feature_budget'],
        'upper_to_guarantee_ratio':cert['upper_to_guarantee_ratio'],'ratio_display':cert['ratio_display'],'earlier_upper_bound':cert['earlier_upper_bound'],
        'direct_interval_precisions':[768,1024],'independent_complex_precisions':[896,1152],'scalar_source_inequalities':checked['scalar_coordinate_inequalities'],
        'independent_polynomial_factorizations':checked['factorization_count'],'coefficient_comparisons':checked['coefficient_comparisons'],'fixed_coefficients':checked['fixed_coefficients'],'ambiguous_coefficients':checked['ambiguous_coefficients'],
        'optimizer_trials':9,'accepted_optimizer_steps':8,'rejected_trial_cube_escape':str(F(rejected[0]['maximum_center_displacement'])-F(1,100)),
        'mutations_rejected':adv['mutations_rejected'],'Lean_lemmas':len(formal['theorems']),'new_source_roots_computed':0,'global_injectivity_established':False,
        'optimal_noise_threshold_established':False,'arbitrary_report_decoder_implemented':False}
def replay_explorations():
    with tempfile.TemporaryDirectory() as directory,zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        tmp=Path(directory);base=tmp/'work/acs-research/noise-threshold-audit';base.mkdir(parents=True);repo=tmp/'work/acs-repo'
        for path in [PRIOR/'Feature_Space_Proposals.json',SOURCE/'Equal_Population_Decoder.json',SOURCE/'Equal_Population_Inputs.zip']:
            target=repo/path.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes())
        (repo/'code').mkdir();(repo/'code/frontier_verification').symlink_to(CODE,target_is_directory=True)
        cases=[('explore_boundary_pairs.py','Boundary_Pair_Proposals.json'),('check_boundary_pairs.py','Boundary_Pair_Checks.json'),('explore_shifted_pairs.py',None),('explore_shifted_pairs_v2.py','Shifted_Pair_Proposals.json'),('check_shifted_pairs.py','Shifted_Pair_Checks.json')]
        for script,report in cases:
            p=base/script;p.write_bytes(z.read('exploration/'+script));result=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
            if report is None:
                assert result.returncode!=0 and "ZeroDivisionError: matrix is numerically singular" in result.stderr and not (base/'Shifted_Pair_Proposals.json').exists()
            else:
                assert result.returncode==0,result.stdout+result.stderr;same(read(base/report),read(OUT/report));assert sha((base/report).read_bytes())==sha((OUT/report).read_bytes()),report
def main():
    stage('Checking immutable variable-noise evidence and replaying original searches, checks and failure')
    manifest=read(OUT/'Manifest.json');inventory=read(OUT/'Source_Inventory.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(name)) for name in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert digest==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
        for kind in ['external_runtime_sources','exploration_sources','packaging_sources']:
            for name,digest in inventory[kind].items():assert sha(z.read(name))==digest
    replay_explorations()
    p=OUT/'Boundary_Pair_Proposals.json';q=OUT/'Shifted_Pair_Proposals.json';cc=OUT/'Variable_Noise_Certificate.json';sp=SOURCE/'Equal_Population_Decoder.json';ia=SOURCE/'Equal_Population_Inputs.zip';region=PRIOR/'Weighted_Region_Certificate.json';ra=PRIOR/'Independent_Weighted_Region_Audit_v2.json'
    stage('Regenerating all four variable-noise contraction certificates and independent audits')
    cert=read(cc);same(cert,quiet(certificate.run,p,q,ANCHOR,sp,ia,region))
    checked=read(OUT/'Independent_Variable_Noise_Audit.json');same(checked,quiet(audit.run,p,q,cc,ANCHOR,region,ra,ia,CLASS/'Full_Quartic_Class.json',PAIR/'Pair_Arithmetic.json',sp))
    adv=read(OUT/'Adversary_Audit.json');same(adv,quiet(adversary.run,p,q,cc,ANCHOR,region,ia));assert adv['mutations_rejected']==64 and checked['certified_pair_count']==4 and checked['scalar_coordinate_inequalities']==704
    stage('Fresh Lean scaling, midpoint-error and scope proofs')
    formal=read(OUT/'Lean_Check.json');project=ROOT.parent/'acs-research/lean-audit/withMathlib';binary=ROOT.parent/'acs-research/runtime/lean-4.34.0-rc2-darwin_aarch64/bin'
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory);assert quiet(lean.run,CODE/'proofs/VariableNoiseMidpoint.lean',project,binary,tmp/'Fresh_Lean.json',tmp/'versions')==0;fresh=read(tmp/'Fresh_Lean.json')
        for key in ['status','source_sha256','checker_sha256','returncode','stdout','stderr','olean_sha256','lake_manifest_sha256','theorems']:same(fresh[key],formal[key])
    assert formal['status']=='passed' and len(formal['theorems'])==6 and 'sorryAx' not in formal['stdout']
    with zipfile.ZipFile(OUT/'Lean_Artifacts.zip') as z:
        assert set(z.namelist())=={'Lean_Check.json','Lean_Check.olean','VariableNoiseMidpoint.lean'};same(formal,json.loads(z.read('Lean_Check.json')))
        assert sha(z.read('Lean_Check.olean'))==formal['olean_sha256'] and sha(z.read('VariableNoiseMidpoint.lean'))==formal['source_sha256']==sha((CODE/'proofs/VariableNoiseMidpoint.lean').read_bytes())
    source=read(OUT/'Source_Acquisition.json');mathlib=project/'.lake/packages/mathlib';assert source['status']=='passed'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathlib,text=True).strip()==source['mathlib_revision']
    for entry in source['pinned_sources']:
        raw=(mathlib/entry['path']).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'] and entry['matches_pinned_git_object'] is True
        assert subprocess.check_output(['git','show','HEAD:'+entry['path']],cwd=mathlib)==raw
    runtime=read(OUT/'Runtime.json')
    for key,pkg in [('python_flint','python-flint'),('sympy','sympy'),('numpy','numpy'),('scipy','scipy'),('mpmath','mpmath'),('pytest','pytest'),('clarabel','clarabel'),('cffi','cffi'),('pycparser','pycparser')]:assert runtime[key]==importlib.metadata.version(pkg)
    summary=summarize(cert,checked,adv,formal,read(q));same(summary,read(OUT/'Variable_Noise_Summary.json')['derived_results'])
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==10 and sorted(name for name,r in receipts.items() if r['returncode'])==FAILURES and all(not r['timed_out'] for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        assert len(z.namelist())==3*len(receipts)
        for name,record in receipts.items():
            same(record,json.loads(z.read(name+'/receipt.json')));assert set(record['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==record[stream+'_sha256']
        assert 'ZeroDivisionError: matrix is numerically singular' in z.read('shifted-pair-exploration/stderr.txt').decode()
    for name,key in [('Inherited_Inputs.json','files_sha256'),('Primary_Sources.json','inherited_source_records_sha256')]:
        for path,digest in read(OUT/name)[key].items():assert sha((ROOT/path).read_bytes())==digest
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};qdata=read(OUT/'Research_Queue.json');after={b['id']:b for b in qdata['branches']}
    assert set(before)==set(after) and len(after)==117 and qdata['new_branches']==[] and qdata['advanced_existing_branches']==ADVANCED and not qdata['global_exhaustion_claimed']
    assert qdata['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==448 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==453;links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'VARIABLE_NOISE_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    stage('All new checks passed; recursively verifying preceding ACS checkpoints')
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_weighted_feature_delta_v2.py')],capture_output=True,text=True);assert previous.returncode==0,previous.stdout+previous.stderr
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'manifest_files':len(manifest['files']),
        'fresh_original_searches_and_interval_checks':'passed','preserved_singular_Newton_failure_reproduced':'passed','fresh_four_variable_noise_certificates':'passed',
        'fresh_independent_complex_source_and_arithmetic_audits':'passed','fresh_adversarial_audit':'passed','fresh_Lean_compilation':'passed','preceding_checkpoint_integrity':'passed',
        'derived_results':summary,'recorded_commands':10,'successful_commands':9,'failed_commands':1,'research_branches':117,'ledger_events':453,'preserved_event_prefix':448,
        'ledger_head_sha256':last,'local_links':links,'entire_calculus_arithmetic_spectral_bridge_Lean_formalized':False,
        'scope':'Four exact variable-noise constructions with free feature midpoints improve the local ambiguity upper bound under the unchanged source, region and root/feature error contract. A roughly 3.6 percent gap to the inherited uniform lower guarantee remains; global recovery, arbitrary-report decoding and the wider ACS program stay open.'},indent=2))
if __name__=='__main__':main()
