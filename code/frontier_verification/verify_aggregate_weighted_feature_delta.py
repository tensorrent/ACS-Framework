"""Replay weighted uniqueness regions, two-sided feature-noise bounds and ACS history."""
import hashlib,importlib.metadata,json,os,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_weighted_region_certificate as region_certificate
import dedekind_weighted_region_audit_v2 as region_audit
import dedekind_feature_space_proposal as proposal
import dedekind_feature_space_certificate as certificate
import dedekind_feature_space_audit as audit
import dedekind_weighted_feature_adversary as adversary
import check_weighted_feature_lean as lean
from verify_aggregate_classification_delta_v2 import same,canonical,quiet

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-14-aggregate-weighted-feature-delta';PRIOR=ROOT/'docs/frontier/2026-09-14-aggregate-augmented-feature-delta'
SOURCE=ROOT/'docs/frontier/2026-09-14-aggregate-equal-population-delta';CLASS=ROOT/'docs/frontier/2026-09-14-aggregate-classification-delta';PAIR=ROOT/'docs/frontier/2026-09-13-biquadratic-delta'
ADVANCED=['R12','R13','R14','R15','K04'];FAILURES=['independent-weighted-region']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def stage(s):print(s,file=sys.stderr,flush=True)
def summarize(regions,checked,feature,independent,adv,formal,diagnosis):
    results=[]
    for r,a in zip(regions['regions'],checked['regions']):
        results.append({k:r[k] for k in ['radius','domain','critical_index','critical_inverse_bound','critical_inverse_bound_display','root_coordinate_error_radius','source_critical_separation_lower','uniform_feature_error_identification_guarantee_strictly_below','feature_error_guarantee_display']} | {
            'independent_critical_bound_display':a['independent_critical_bound_display'],'contained_preceding_witnesses':a['contained_preceding_witnesses']})
    return {'regions':results,'feature_dimension':22,'source_population':22,'source_cutoff':'39/2','largest_radius_growth_factor':str(F(results[-1]['radius'])/F('1e-10')),
        'derivative_Taylor_order':6,'remainder_derivative_order':7,'remainder_factorial':720,'uniform_weighted_defect_bound':'1/2',
        'primary_region_precisions':[768,1024],'independent_real_polynomial_precisions':[896,1152],'independent_positive_series_terms':33,
        'exact_inverse_roots_certified':feature['exact_inverse_roots_certified'],'source_feasible_noisy_pairs':feature['source_feasible_noisy_pairs'],
        'excluded_signed_target_pairs':feature['excluded_signed_target_pairs'],'inverse_correction_box_radius':'1e-120',
        'feature_error_cases':[{'tau':c['feature_error_bound'],'status':c['status'],'uniform_source_exclusions':len(c['uniform_source_exclusions'])} for c in feature['cases']],
        'small_region_uniform_identification_below':feature['uniform_identification_below'],'actual_ambiguity_at':feature['actual_ambiguity_at'],
        'upper_to_guarantee_ratio':feature['upper_to_guarantee_ratio'],'ratio_display':feature['ratio_display'],
        'independent_scalar_coordinate_inequalities':independent['scalar_coordinate_inequalities'],
        'independent_polynomial_factorizations':independent['factorization_count'],'coefficient_comparisons':independent['coefficient_comparisons'],
        'fixed_arithmetic_coefficients':independent['fixed_coefficients'],'ambiguous_arithmetic_coefficients':independent['ambiguous_coefficients'],
        'mutations_rejected':adv['mutations_rejected'],'exact_endpoint_comparisons':diagnosis['endpoint_comparisons'],
        'exact_endpoint_violations':len(diagnosis['exact_rational_endpoint_violations']),'reconstructed_ball_false_rejections':len(diagnosis['reconstructed_ball_comparison_failures']),
        'Lean_lemmas':len(formal['theorems']),'new_source_roots_computed':0,'global_injectivity_established':False,
        'optimal_measurement_noise_threshold_established':False,'arbitrary_observation_decoder_implemented':False}

def replay_explorations():
    with tempfile.TemporaryDirectory() as directory,zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        tmp=Path(directory);base=tmp/'work/acs-research/local-injectivity-audit';base.mkdir(parents=True)
        repo=tmp/'work/acs-repo';anchor=repo/PRIOR.relative_to(ROOT)/'Augmented_Proposals_Local.json';anchor.parent.mkdir(parents=True)
        anchor.write_bytes((PRIOR/anchor.name).read_bytes());(repo/'code').mkdir();(repo/'code/frontier_verification').symlink_to(CODE,target_is_directory=True)
        cases=[('explore_preconditioned_taylor.py','Preconditioned_Taylor_Exploration.json'),('explore_weighted_taylor.py','Weighted_Taylor_Exploration.json'),('audit_weighted_candidate.py','Independent_Weighted_Candidate_Audit.json'),('diagnose_serialized_endpoints.py','Serialized_Endpoint_Diagnosis.json')]
        (base/'Weighted_Region_Certificate.json').write_bytes((OUT/'Weighted_Region_Certificate.json').read_bytes())
        for script,report in cases:
            p=base/script;p.write_bytes(z.read('exploration/'+script))
            result=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
            assert result.returncode==0,result.stdout+result.stderr
            same(read(base/report),read(OUT/report))
            assert sha((base/report).read_bytes())==sha((OUT/report).read_bytes()),report

def main():
    stage('Checking immutable weighted-feature evidence and replaying original explorations')
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
    anchor=PRIOR/'Augmented_Proposals_Local.json';exploration=OUT/'Weighted_Taylor_Exploration.json';region=OUT/'Weighted_Region_Certificate.json'
    sp=SOURCE/'Equal_Population_Decoder.json';ia=SOURCE/'Equal_Population_Inputs.zip';cp=CLASS/'Full_Quartic_Class.json';ar=PAIR/'Pair_Arithmetic.json'
    pp=OUT/'Feature_Space_Proposals.json';cc=OUT/'Feature_Space_Certificate.json';ra=OUT/'Independent_Weighted_Region_Audit_v2.json'
    stage('Regenerating weighted Taylor certificates and eight feature-space inverse roots')
    regions=read(region);same(regions,quiet(region_certificate.run,anchor,exploration))
    same(read(pp),quiet(proposal.run,sp));feature=read(cc);same(feature,quiet(certificate.run,pp,anchor,sp,ia,region))
    stage('Independent real-polynomial/positive-series and complex/arithmetic audits')
    checked=read(ra);same(checked,quiet(region_audit.run,anchor,exploration,region,ia,PRIOR))
    independent=read(OUT/'Independent_Feature_Space_Audit.json');same(independent,quiet(audit.run,pp,cc,anchor,region,ra,ia,cp,ar,sp))
    adv=read(OUT/'Adversary_Audit.json');diagnosis=read(OUT/'Serialized_Endpoint_Diagnosis.json')
    same(adv,quiet(adversary.run,anchor,exploration,region,pp,cc,ia,PRIOR,OUT/'Serialized_Endpoint_Diagnosis.json'))
    assert adv['mutations_rejected']==52 and independent['exact_inverse_root_count']==8 and independent['scalar_coordinate_inequalities']==704
    assert diagnosis['endpoint_comparisons']==1936 and len(diagnosis['reconstructed_ball_comparison_failures'])==108 and diagnosis['exact_rational_endpoint_violations']==[]
    stage('Fresh Lean compilation and reproduction of the preserved endpoint-audit failure')
    formal=read(OUT/'Lean_Check.json');project=ROOT.parent/'acs-research/lean-audit/withMathlib';binary=ROOT.parent/'acs-research/runtime/lean-4.34.0-rc2-darwin_aarch64/bin'
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory);assert quiet(lean.run,CODE/'proofs/WeightedFeatureStability.lean',project,binary,tmp/'Fresh_Lean.json',tmp/'versions')==0
        fresh=read(tmp/'Fresh_Lean.json')
        for key in ['status','source_sha256','checker_sha256','returncode','stdout','stderr','olean_sha256','lake_manifest_sha256','theorems']:same(fresh[key],formal[key])
        failed=subprocess.run([sys.executable,str(CODE/'dedekind_weighted_region_audit.py'),'--anchor',str(anchor),'--exploration',str(exploration),'--certificate',str(region),'--inputs',str(ia),'--prior',str(PRIOR),'--output',str(tmp/'Rejected.json')],capture_output=True,text=True)
        assert failed.returncode!=0 and 'AssertionError' in failed.stderr and "av(Bstored[i][j])>=ball(check['majorant_matrix'][i][j])" in failed.stderr and not (tmp/'Rejected.json').exists(),failed.stderr
    assert formal['status']=='passed' and len(formal['theorems'])==6 and 'sorryAx' not in formal['stdout']
    with zipfile.ZipFile(OUT/'Lean_Artifacts.zip') as z:
        assert set(z.namelist())=={'Lean_Check.json','Lean_Check.olean','WeightedFeatureStability.lean'}
        same(formal,json.loads(z.read('Lean_Check.json')));assert sha(z.read('Lean_Check.olean'))==formal['olean_sha256']
        assert sha(z.read('WeightedFeatureStability.lean'))==formal['source_sha256']==sha((CODE/'proofs/WeightedFeatureStability.lean').read_bytes())
    old=(CODE/'dedekind_weighted_region_audit.py').read_text();new=(CODE/'dedekind_weighted_region_audit_v2.py').read_text()
    addition="def exact_upper_endpoint(x):\n    m,e=x['mid'];r,t=x['rad'];return F(m)*F(2)**e+F(r)*F(2)**t\n"
    assert new.replace(addition,'').replace("Bstored[i][j]>=exact_upper_endpoint(check['majorant_matrix'][i][j])","av(Bstored[i][j])>=ball(check['majorant_matrix'][i][j])")==old
    source=read(OUT/'Source_Acquisition.json');mathlib=project/'.lake/packages/mathlib';assert source['status']=='passed'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathlib,text=True).strip()==source['mathlib_revision']
    for entry in source['pinned_sources']:
        raw=(mathlib/entry['path']).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'] and entry['matches_pinned_git_object'] is True
        assert subprocess.check_output(['git','show','HEAD:'+entry['path']],cwd=mathlib)==raw
    runtime=read(OUT/'Runtime.json')
    for key,pkg in [('python_flint','python-flint'),('sympy','sympy'),('numpy','numpy'),('scipy','scipy'),('mpmath','mpmath'),('pytest','pytest'),('clarabel','clarabel'),('cffi','cffi'),('pycparser','pycparser')]:assert runtime[key]==importlib.metadata.version(pkg)
    summary=summarize(regions,checked,feature,independent,adv,formal,diagnosis);same(summary,read(OUT/'Weighted_Feature_Summary.json')['derived_results'])
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==13 and sorted(name for name,r in receipts.items() if r['returncode'])==FAILURES and all(not r['timed_out'] for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        assert len(z.namelist())==3*len(receipts)
        for name,record in receipts.items():
            same(record,json.loads(z.read(name+'/receipt.json')));assert set(record['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==record[stream+'_sha256']
        assert 'AssertionError' in z.read('independent-weighted-region/stderr.txt').decode()
    for name,key in [('Inherited_Inputs.json','files_sha256'),('Primary_Sources.json','inherited_source_records_sha256')]:
        for path,digest in read(OUT/name)[key].items():assert sha((ROOT/path).read_bytes())==digest
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};q=read(OUT/'Research_Queue.json');after={b['id']:b for b in q['branches']}
    assert set(before)==set(after) and len(after)==117 and q['new_branches']==[] and q['advanced_existing_branches']==ADVANCED and not q['global_exhaustion_claimed']
    assert q['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==443 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==448;links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'WEIGHTED_FEATURE_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    stage('All new checks passed; recursively verifying preceding ACS checkpoints')
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_augmented_feature_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'manifest_files':len(manifest['files']),
        'fresh_original_explorations_and_endpoint_diagnosis':'passed','fresh_weighted_Taylor_and_componentwise_certificates':'passed',
        'fresh_eight_exact_inverse_roots':'passed','fresh_independent_real_polynomial_positive_series_complex_and_arithmetic_audits':'passed',
        'fresh_adversarial_audit':'passed','fresh_Lean_compilation':'passed','preserved_endpoint_audit_failure_reproduced':'passed',
        'preceding_checkpoint_integrity':'passed','derived_results':summary,'recorded_commands':13,'successful_commands':12,'failed_commands':1,
        'research_branches':117,'ledger_events':448,'preserved_event_prefix':443,'ledger_head_sha256':last,'local_links':links,
        'entire_calculus_arithmetic_spectral_bridge_Lean_formalized':False,
        'scope':'The selected 22-feature map is injective on certified standard coordinate cubes, with componentwise stability and conditional uniform noise-identification guarantees. Exact inverse roots give actual noisy ambiguity under the same smaller-region contract and a two-sided threshold bracket. The sharp threshold, bounded-error decoder, global injectivity and wider ACS branches remain open.'},indent=2))
if __name__=='__main__':main()
