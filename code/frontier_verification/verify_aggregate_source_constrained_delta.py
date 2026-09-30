"""Replay source-strip/mixed-pair evidence, rejected trials and the full ACS chain."""
import hashlib,importlib.metadata,json,os,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_source_strip_certificate as strip_certificate
import dedekind_mixed_noise_certificate as mixed_certificate
import dedekind_source_constrained_audit as audit
import dedekind_source_constrained_adversary as adversary
import check_source_constrained_lean as lean
from verify_aggregate_classification_delta_v2 import same,canonical,quiet

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-14-aggregate-source-constrained-delta';PRIOR=ROOT/'docs/frontier/2026-09-14-aggregate-signed-corner-delta'
ADVANCED=['R12','R13','R14','R15','K04'];FAILURES=['corner-pair-exploration'];HASH_LIMITATIONS=['corner-pair-diagnostic']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def stage(s):print(s,file=sys.stderr,flush=True)
def summarize(strip,mixed,checked,adv,formal,diagnostic):
    assert all(x['status']=='passed' for x in [strip,mixed,checked,adv,formal])
    rejected=diagnostic['cases'];assert len(rejected)==3 and all(x['numerically_converged'] and x['rational_center_source_constraints_all_pass'] and not x['inside_cube'] and F(x['minimum_cube_margin'])<0 for x in rejected)
    low=F(strip['uniform_identification_strictly_below']);high=F(mixed['best_certified_tau_upper']);assert F(checked['upper_to_guarantee_ratio'])==high/low
    return {'feature_dimension':22,'source_population':22,'source_cutoff':'39/2','original_coordinate_cube_radius':'1/100','root_coordinate_error_radius':strip['contract']['root_coordinate_error_radius'],
        'bootstrap_feature_budget_cap':strip['bootstrap_feature_budget_cap'],'critical_difference_cap':strip['critical_difference_cap'],
        'conditional_critical_curve_interval':strip['critical_column_curve_interval'],'critical_strip_half_width_display':strip['critical_strip_half_width_display'],
        'conditional_secant_inverse_bound':strip['conditional_secant_inverse_bound'],'inverse_bound_display':strip['inverse_bound_display'],
        'uniform_identification_strictly_below':str(low),'lower_display':float(low),'previous_uniform_guarantee':strip['previous_uniform_guarantee'],
        'best_certified_tau_upper':str(high),'upper_display':float(high),'previous_upper_endpoint':mixed['previous_upper_endpoint'],
        'upper_to_guarantee_ratio':str(high/low),'ratio_display':float(high/low),'relative_threshold_gap_display':float(high/low-1),
        'mixed_pair_count':2,'critical_epsilon':mixed['critical_epsilon'],'variable_radius':'1e-120','tau_scale':'1e-10',
        'pairs':[{'case_id':x['case_id'],'free_A_indices':x['free_A_indices'],'free_B_indices':x['free_B_indices'],'tau_interval':x['tau_interval'],'minimum_cube_margin':x['minimum_cube_margin']} for x in checked['mixed_pair_checks']],
        'rejected_naive_pair_count':3,'rejected_cube_escape_displays':[-float(F(x['minimum_cube_margin'])) for x in rejected],
        'scalar_source_inequalities':352,'polynomial_factorizations':1128,'coefficient_comparisons':1208,'fixed_coefficients':456,'ambiguous_coefficients':148,
        'lower_primary_precision_bits':[1024,1536],'lower_independent_Cramer_precision_bits':[896,1152],
        'mixed_primary_precision_bits':[768,1024],'mixed_independent_complex_precision_bits':[896,1152],
        'mutations_rejected':adv['mutations_rejected'],'exact_controls':len(adv['exact_controls']),'Lean_lemmas':len(formal['theorems']),
        'original_observation_contract_preserved':True,'new_source_roots':0,'entire_concrete_bridge_Lean_formalized':False,'sharp_source_feasible_threshold_proved':False,'arbitrary_report_decoder_implemented':False}

def replay_explorations():
    with tempfile.TemporaryDirectory() as directory,zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        tmp=Path(directory);base=tmp/'work/acs-research/source-constrained-audit';base.mkdir(parents=True);repo=tmp/'work/acs-repo'
        relatives=[audit.PRIOR,audit.ANCHOR,audit.REGION,audit.UPPER,audit.SOURCE+'/Equal_Population_Inputs.zip',audit.SOURCE+'/Equal_Population_Decoder.json']
        for relative in relatives:
            target=repo/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/relative).read_bytes())
        (repo/'code').mkdir();(repo/'code/frontier_verification').symlink_to(CODE,target_is_directory=True)
        cases=[('explore_critical_strip.py','Critical_Strip_Exploration.json'),('audit_critical_strip.py','Independent_Critical_Strip_Audit.json'),
            ('explore_corner_pairs.py',None),('explore_corner_pairs_v2.py','Corner_Pair_Diagnostic.json'),('explore_complementary_pairs.py','Complementary_Pair_Proposals.json'),('check_complementary_pairs.py','Complementary_Pair_Checks.json')]
        for script,report in cases:
            p=base/script;p.write_bytes(z.read('exploration/'+script));result=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
            if report is None:assert result.returncode!=0 and 'AssertionError' in result.stderr and not (base/'Corner_Pair_Proposals.json').exists()
            else:
                assert result.returncode==0,result.stdout+result.stderr;same(read(base/report),read(OUT/report));assert sha((base/report).read_bytes())==sha((OUT/report).read_bytes()),report

def main():
    stage('Checking source-constrained provenance and replaying all six original scripts, including the rejected search')
    manifest=read(OUT/'Manifest.json');inventory=read(OUT/'Source_Inventory.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert digest==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
        for kind in ['external_runtime_sources','exploration_sources','packaging_sources']:
            for name,digest in inventory[kind].items():assert sha(z.read(name))==digest
        assert sha(z.read('exploration/explore_corner_pairs_v2.py'))==read(OUT/'Corner_Pair_Diagnostic.json')['source_sha256']
    replay_explorations()
    stage('Fresh source-strip and mixed A/B certificates, independent analytic/source/arithmetic audits and mutations')
    sp=OUT/'Source_Strip_Certificate.json';mp=OUT/'Mixed_Noise_Certificate.json';pp=OUT/'Complementary_Pair_Proposals.json'
    strip=read(sp);mixed=read(mp);same(strip,quiet(strip_certificate.run));same(mixed,quiet(mixed_certificate.run,pp))
    checked=read(OUT/'Independent_Source_Constrained_Audit.json');same(checked,quiet(audit.run,sp,mp,pp))
    adv=read(OUT/'Adversary_Audit.json');same(adv,quiet(adversary.run,sp,mp,pp))
    assert checked['scalar_source_inequalities']==352 and checked['factorization_count']==1128 and adv['mutations_rejected']==46 and len(adv['exact_controls'])==5
    stage('Fresh Lean source-error, strip, budget-bootstrap and mixed-derivative proofs')
    formal=read(OUT/'Lean_Check.json');project=ROOT.parent/'acs-research/lean-audit/withMathlib';binary=ROOT.parent/'acs-research/runtime/lean-4.34.0-rc2-darwin_aarch64/bin'
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory);assert quiet(lean.run,CODE/'proofs/SourceConstrainedNoise.lean',project,binary,tmp/'Fresh_Lean.json',tmp/'versions')==0;fresh=read(tmp/'Fresh_Lean.json')
        for key in ['status','source_sha256','checker_sha256','returncode','stdout','stderr','olean_sha256','lake_manifest_sha256','theorems']:same(fresh[key],formal[key])
    assert len(formal['theorems'])==7 and 'sorryAx' not in formal['stdout']+formal['stderr']
    with zipfile.ZipFile(OUT/'Lean_Artifacts.zip') as z:
        assert set(z.namelist())=={'Lean_Check.json','Lean_Check.olean','SourceConstrainedNoise.lean'};same(formal,json.loads(z.read('Lean_Check.json')))
        assert sha(z.read('Lean_Check.olean'))==formal['olean_sha256'] and sha(z.read('SourceConstrainedNoise.lean'))==formal['source_sha256']==sha((CODE/'proofs/SourceConstrainedNoise.lean').read_bytes())
    acquisition=read(OUT/'Source_Acquisition.json');mathlib=project/'.lake/packages/mathlib';assert acquisition['status']=='passed'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathlib,text=True).strip()==acquisition['mathlib_revision']
    for entry in acquisition['pinned_sources']:
        raw=(mathlib/entry['path']).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'] and entry['matches_pinned_git_object']
        assert subprocess.check_output(['git','show','HEAD:'+entry['path']],cwd=mathlib)==raw
    runtime=read(OUT/'Runtime.json')
    for key,pkg in [('python_flint','python-flint'),('sympy','sympy'),('numpy','numpy'),('scipy','scipy'),('mpmath','mpmath'),('pytest','pytest'),('clarabel','clarabel'),('cffi','cffi'),('pycparser','pycparser')]:assert runtime[key]==importlib.metadata.version(pkg)
    summary=summarize(strip,mixed,checked,adv,formal,read(OUT/'Corner_Pair_Diagnostic.json'));same(summary,read(OUT/'Source_Constrained_Summary.json')['derived_results'])
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==12 and sorted(n for n,r in receipts.items() if r['returncode'])==FAILURES and all(not r['timed_out'] for r in receipts.values())
    assert sorted(n for n,r in receipts.items() if not r['input_sources_sha256'])==HASH_LIMITATIONS
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        assert len(z.namelist())==3*len(receipts)
        for name,record in receipts.items():
            same(record,json.loads(z.read(name+'/receipt.json')));assert set(record['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==record[stream+'_sha256']
        assert 'AssertionError' in z.read('corner-pair-exploration/stderr.txt').decode()
    for name,key in [('Inherited_Inputs.json','files_sha256'),('Primary_Sources.json','inherited_source_records_sha256')]:
        for path,digest in read(OUT/name)[key].items():assert sha((ROOT/path).read_bytes())==digest
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};q=read(OUT/'Research_Queue.json');after={b['id']:b for b in q['branches']}
    assert set(before)==set(after) and len(after)==117 and q['new_branches']==[] and q['advanced_existing_branches']==ADVANCED and not q['global_exhaustion_claimed']
    assert q['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==458 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        event=json.loads(line);digest=event.pop('event_sha256');assert event['sequence']==index and event['previous_event_sha256']==last and sha(canonical(event))==digest;last=digest
    assert index==463;links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'SOURCE_CONSTRAINED_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    stage('All new checks passed; recursively verifying the preceding ACS evidence chain')
    prior=subprocess.run([sys.executable,str(CODE/'verify_aggregate_signed_corner_delta.py')],capture_output=True,text=True);assert prior.returncode==0,prior.stdout+prior.stderr
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'manifest_files':len(manifest['files']),
        'fresh_original_explorations_and_checks':'passed','rejected_naive_pair_failure_reproduced':'passed','fresh_source_strip_and_mixed_pair_certificates':'passed',
        'fresh_independent_real_Cramer_complex_source_and_arithmetic_audits':'passed','fresh_adversarial_audit':'passed','fresh_Lean_compilation':'passed','preceding_checkpoint_integrity':'passed',
        'derived_results':summary,'recorded_commands':12,'successful_commands':11,'failed_commands':1,'source_hash_receipt_limitations':HASH_LIMITATIONS,
        'research_branches':117,'ledger_events':463,'preserved_event_prefix':458,'ledger_head_sha256':last,'local_links':links,'entire_concrete_bridge_Lean_formalized':False,
        'scope':'A conditional source-strip bootstrap strengthens the strict lower guarantee under the original local observation contract. Two mixed A/B contraction constructions improve the actual ambiguity upper endpoint. Independent formulas, direct source checks and seven generic Lean lemmas support a remaining threshold bracket of about 0.65 percent. Source-feasible sharpness, general decoding and all wider ACS branches remain open.'},indent=2))
if __name__=='__main__':main()
