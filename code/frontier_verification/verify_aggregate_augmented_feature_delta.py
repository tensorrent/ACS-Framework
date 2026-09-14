"""Replay joint-feature collisions, local injectivity, noisy releases and ACS history."""
import hashlib,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_augmented_feature_proposal as proposal
import dedekind_augmented_feature_certificate_v2 as certificate
import dedekind_augmented_feature_audit as audit
import dedekind_augmented_feature_noise as noise
import dedekind_augmented_feature_adversary as adversary
import check_augmented_feature_lean as lean
from verify_aggregate_classification_delta_v2 import same,canonical,quiet

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-14-aggregate-augmented-feature-delta';PRIOR=ROOT/'docs/frontier/2026-09-14-aggregate-feature-delta'
SOURCE=ROOT/'docs/frontier/2026-09-14-aggregate-equal-population-delta';CLASS=ROOT/'docs/frontier/2026-09-14-aggregate-classification-delta';PAIR=ROOT/'docs/frontier/2026-09-13-biquadratic-delta'
ADVANCED=['R12','R13','R14','R15','K04'];FAILURES=['augmented-certificate-enlarged','augmented-feature-lean']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def stage(s):print(s,file=sys.stderr,flush=True)
def summarize(certs,checked,feature_noise,adv,formal):
    large=certs['Enlarged']['collisions'][-1];local=certs['Local'];inj=local['rank_and_local_injectivity']
    return {'collision_dimensions':[18,19,20,21],'critical_splits':['1e-8','1e-12','1e-18'],'certified_collision_count':12,
        'complete_source_population':22,'source_cutoff':'39/2','largest_split_root_error_radius':large['radius'],
        'largest_split_strict_improvement_below_L':large['strict_improvement_below_L'],'correction_box_radius':large['correction_box_radius'],
        'uniform_source_root_box_checks':sum(len(c['coordinate_audit']) for cert in certs.values() for c in cert['collisions']),
        'independent_scalar_coordinate_inequalities':checked['total_scalar_coordinate_inequalities'],
        'direct_interval_precisions':[640,896],'independent_complex_Taylor_precision':768,'local_injective_feature_dimension':22,
        'local_neighborhood_radius':inj['certified_neighborhood_radius'],'local_derivative_defect_bound':inj['uniform_derivative_defect_bound'],
        'inverse_Lipschitz_bound':inj['inverse_Lipschitz_bound'],'local_collision_membership':checked['cases']['Local']['local_memberships'],
        'full_preconditioner_modular_determinant':checked['cases']['Local']['full_preconditioner_modular_determinant']['determinant_mod_prime'],
        'center_43_feature_differences_display':{k:v['center_43_difference_display'] for k,v in checked['cases'].items()},
        'noisy_22_feature_error_bound':feature_noise['feature_release_error_bound'],'explicit_last_feature_offset':feature_noise['final_feature_offset_from_B'],
        'independent_polynomial_factorizations':checked['factorizations_count'],'coefficient_comparisons':checked['coefficient_comparisons'],
        'fixed_arithmetic_coefficients':checked['fixed_coefficients'],'ambiguous_arithmetic_coefficients':checked['ambiguous_coefficients'],
        'mutations_rejected':adv['mutations_rejected'],'exact_zero_margin_controls':len(adv['exact_zero_margin_controls']),
        'binary64_false_negative_margins':sum(x['binary64_margin']<0 for x in adv['exact_zero_margin_controls']),
        'Lean_lemmas':len(formal['theorems']),'new_source_roots_computed':0,'global_injectivity_established':False,'optimal_measurement_noise_threshold_established':False}
def main():
    stage('Checking immutable augmented evidence and regenerating all 12 collision certificates')
    manifest=read(OUT/'Manifest.json');inventory=read(OUT/'Source_Inventory.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(name)) for name in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert digest==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
        for name,digest in inventory['external_runtime_sources'].items():assert sha(z.read(name))==digest
    sp=SOURCE/'Equal_Population_Decoder.json';ia=SOURCE/'Equal_Population_Inputs.zip';cp=CLASS/'Full_Quartic_Class.json';ar=PAIR/'Pair_Arithmetic.json';certs={}
    for suffix,epsilon in [('Enlarged','1e-8'),('Small','1e-12'),('Local','1e-18')]:
        pp=OUT/f'Augmented_Proposals_{suffix}.json';cc=OUT/f'Augmented_Certificate_{suffix}_v2.json'
        same(read(pp),quiet(proposal.run,sp,epsilon,220));certs[suffix]=read(cc);same(certs[suffix],quiet(certificate.run,pp,sp,ia,'1e-120'))
    stage('Independent complex Taylor, arithmetic, feature-noise and adversarial replay')
    checked=read(OUT/'Independent_Augmented_Audit.json');same(checked,quiet(audit.run,OUT,sp,ia,cp,ar))
    feature_noise=read(OUT/'Feature_Noise_Boundary.json');same(feature_noise,quiet(noise.run,OUT/'Augmented_Certificate_Local_v2.json',OUT/'Independent_Augmented_Audit.json'))
    adv=read(OUT/'Adversary_Audit.json');same(adv,quiet(adversary.run,OUT/'Augmented_Proposals_Local.json',OUT/'Augmented_Certificate_Local_v2.json',ia,OUT/'Feature_Noise_Boundary.json'))
    assert adv['mutations_rejected']==45 and checked['total_collision_certificates']==12 and checked['total_scalar_coordinate_inequalities']==2112
    stage('Fresh Lean local-injectivity proofs and failure provenance')
    formal=read(OUT/'Lean_Check_v2.json');project=ROOT.parent/'acs-research/lean-audit/withMathlib';binary=ROOT.parent/'acs-research/runtime/lean-4.34.0-rc2-darwin_aarch64/bin'
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory);assert quiet(lean.run,CODE/'proofs/AugmentedFeatureLocal_v2.lean',project,binary,tmp/'Fresh_Lean.json',tmp/'versions')==0
        fresh=read(tmp/'Fresh_Lean.json')
        for key in ['status','source_sha256','checker_sha256','returncode','stdout','stderr','olean_sha256','lake_manifest_sha256','theorems']:same(fresh[key],formal[key])
        # Reproduce the preserved first certificate failure without altering its source.
        failed=subprocess.run([sys.executable,str(CODE/'dedekind_augmented_feature_certificate.py'),'--proposal',str(OUT/'Augmented_Proposals_Enlarged.json'),'--source',str(sp),'--inputs',str(ia),'--output',str(tmp/'Rejected.json')],capture_output=True,text=True)
        assert failed.returncode!=0 and "not supported between instances of 'flint.types.arb.arb' and 'Fraction'" in failed.stderr and not (tmp/'Rejected.json').exists()
    assert formal['status']=='passed' and len(formal['theorems'])==6 and 'sorryAx' not in formal['stdout']
    with zipfile.ZipFile(OUT/'Lean_Artifacts.zip') as z:
        assert set(z.namelist())=={'Lean_Check.json','Lean_Check_v2.json','Lean_Check_v2.olean','AugmentedFeatureLocal.lean','AugmentedFeatureLocal_v2.lean'}
        assert sha(z.read('Lean_Check_v2.olean'))==formal['olean_sha256']
        for name,src in [('Lean_Check.json','AugmentedFeatureLocal.lean'),('Lean_Check_v2.json','AugmentedFeatureLocal_v2.lean')]:
            record=read(OUT/name);same(record,json.loads(z.read(name)));assert record['source_sha256']==sha(z.read(src))==sha((CODE/'proofs'/src).read_bytes())
        assert read(OUT/'Lean_Check.json')['status']=='failed' and "unexpected token 'prefix'" in read(OUT/'Lean_Check.json')['stdout']
    old=(CODE/'dedekind_augmented_feature_certificate.py').read_text();new=(CODE/'dedekind_augmented_feature_certificate_v2.py').read_text();assert old.replace('q<F(1,2)',"q<av('1/2')")==new
    assert re.sub(r'\bprefix\b','observed',(CODE/'proofs/AugmentedFeatureLocal.lean').read_text())==(CODE/'proofs/AugmentedFeatureLocal_v2.lean').read_text()
    source=read(OUT/'Source_Acquisition.json');mathlib=project/'.lake/packages/mathlib';assert source['status']=='passed'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathlib,text=True).strip()==source['mathlib_revision']
    for entry in source['pinned_sources']:
        raw=(mathlib/entry['path']).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'] and entry['matches_pinned_git_object'] is True
        assert subprocess.check_output(['git','show','HEAD:'+entry['path']],cwd=mathlib)==raw
    summary=summarize(certs,checked,feature_noise,adv,formal);same(summary,read(OUT/'Augmented_Feature_Summary.json')['derived_results'])
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==13 and sorted(name for name,r in receipts.items() if r['returncode'])==FAILURES and all(not r['timed_out'] for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        assert len(z.namelist())==3*len(receipts)
        for name,record in receipts.items():
            same(record,json.loads(z.read(name+'/receipt.json')));assert set(record['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==record[stream+'_sha256']
        assert "not supported between instances of 'flint.types.arb.arb' and 'Fraction'" in z.read('augmented-certificate-enlarged/stderr.txt').decode()
    for path,digest in read(OUT/'Inherited_Inputs.json')['files_sha256'].items():assert sha((ROOT/path).read_bytes())==digest
    for path,digest in read(OUT/'Primary_Sources.json')['inherited_source_records_sha256'].items():assert sha((ROOT/path).read_bytes())==digest
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};q=read(OUT/'Research_Queue.json');after={b['id']:b for b in q['branches']}
    assert set(before)==set(after) and len(after)==117 and q['new_branches']==[] and q['advanced_existing_branches']==ADVANCED and not q['global_exhaustion_claimed']
    assert q['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==438 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==443;links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'AUGMENTED_FEATURE_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    stage('All new checks passed; recursively verifying preceding ACS checkpoints')
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_feature_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'manifest_files':len(manifest['files']),
        'fresh_proposals_and_12_contraction_certificates':'passed','fresh_independent_complex_Taylor_rank_and_arithmetic_audits':'passed',
        'fresh_noisy_22_feature_release':'passed','fresh_adversarial_audit':'passed','fresh_Lean_compilation':'passed','preserved_certificate_failure_reproduced':'passed',
        'preceding_checkpoint_integrity':'passed','derived_results':summary,'recorded_commands':13,'successful_commands':11,'failed_commands':2,
        'research_branches':117,'ledger_events':443,'preserved_event_prefix':438,'ledger_head_sha256':last,'local_links':links,
        'entire_calculus_arithmetic_spectral_bridge_Lean_formalized':False,
        'scope':'Joint finite observables through dimension 21 admit actual-source collisions. The selected 22-feature map is locally injective on a certified neighborhood containing smaller collisions; an explicit bounded feature error restores ambiguity there. Global identification, optimal radii/noise thresholds and the wider ACS program remain open.'},indent=2))
if __name__=='__main__':main()
