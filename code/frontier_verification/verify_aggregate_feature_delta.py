"""Replay actual finite-feature collisions, independent existence proofs and ACS history."""
import hashlib,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_feature_proposal as proposal
import dedekind_feature_certificate as certificate
import dedekind_feature_audit as audit
import dedekind_feature_export_audit as exports
import dedekind_feature_adversary as adversary
import dedekind_feature_observable_boundary as boundary
import check_feature_contraction_lean as lean
from verify_aggregate_classification_delta_v2 import same,canonical,quiet

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-14-aggregate-feature-delta';PRIOR=ROOT/'docs/frontier/2026-09-14-aggregate-equal-population-delta'
CLASS=ROOT/'docs/frontier/2026-09-14-aggregate-classification-delta';PAIR=ROOT/'docs/frontier/2026-09-13-biquadratic-delta'
ADVANCED=['R12','R13','R14','R15','K04']
FAILURES=['audit-original-local-export','feature-contraction-lean','feature-contraction-lean-after-acquisition','overextended-feature-slice-proposal']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def stage(s):print(s,file=sys.stderr,flush=True)
def without_clocks(x):
    if isinstance(x,dict):return {k:without_clocks(v) for k,v in x.items() if k not in ['recorded_utc','elapsed_seconds']}
    if isinstance(x,list):return [without_clocks(v) for v in x]
    return x
def summarize(cert,small,checked,adv,extra,formal):
    return {'released_features':17,'preselected_population_per_field':22,'source_cutoff':'39/2','gaussian_a':'1/25',
            'actual_common_feature_radius':cert['radius'],'full_point_list_threshold_lower':cert['full_point_list_threshold_lower'],'strict_radius_gap_below_lower':cert['strict_improvement_below_lower'],
            'critical_split_epsilon':cert['critical_split_epsilon'],'earlier_critical_split_epsilon':small['critical_split_epsilon'],
            'critical_split_amplification':int(F(cert['critical_split_epsilon'])/F(small['critical_split_epsilon'])),'correction_box_radius':cert['correction_box_radius'],
            'uniform_source_root_box_checks':len(cert['coordinate_audit']),'independent_scalar_coordinate_inequalities':checked['independent_certificate_audit']['exact_scalar_inclusion_inequalities'],
            'primary_contraction_precisions':[x['precision_bits'] for x in cert['contraction_checks']],'independent_complex_Taylor_precision':640,
            'modular_preconditioner_determinant_prime':65537,'modular_determinant':checked['independent_certificate_audit']['modular_preconditioner_nonsingularity']['determinant_mod_prime'],
            'polynomial_factorizations_per_audit':checked['independent_polynomial_factorizations'],'coefficient_comparisons_per_audit':checked['coefficient_comparisons'],
            'fixed_common_feature_coefficients':checked['fixed_coefficients'],'ambiguous_common_feature_coefficients':checked['ambiguous_coefficients'],'differing_targets':checked['differing_targets'],
            'mutations_rejected':adv['mutations_rejected'],'exact_zero_margin_controls':len(adv['exact_zero_margin_controls']),
            'witness_interior_counts':[extra['interior_count']['A_count_envelope'][0],extra['interior_count']['B_count']],
            'additional_observables_distinguishing_this_witness':[x['observable'] for x in extra['cases'][0]['omitted_observables']],
            'kernel_checked_lemmas':len(formal['theorems']),'new_source_roots_computed':0,'optimal_feature_threshold_established':False,
            'moments_or_unknown_tails_included_in_release':False}
def replay_exploration(tmp):
    mirror=tmp/'exploration';work=mirror/'feature-only-audit';source=mirror/'aggregate-equal-population-audit';work.mkdir(parents=True);source.mkdir()
    (source/'Equal_Population_Decoder.json').write_bytes((PRIOR/'Equal_Population_Decoder.json').read_bytes());(source/'inputs').mkdir()
    with zipfile.ZipFile(PRIOR/'Equal_Population_Inputs.zip') as z:
        for n in z.namelist():(source/'inputs'/n).write_bytes(z.read(n))
    names=['propose_feature_collision.py','propose_local_slice.py','propose_local_slice_v2.py','certify_local_slice.py']
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        for n in names:(work/n).write_bytes(z.read('exploration/'+n))
    outputs=['Feature_Collision_Proposals.json','Local_Slice_Proposal.json','Local_Slice_Proposal_v2.json','Local_Slice_Contraction.json']
    for n,o in zip(names,outputs):
        p=subprocess.run([sys.executable,str(work/n)],cwd=ROOT,capture_output=True,text=True)
        assert p.returncode==0,p.stdout+p.stderr
        same(without_clocks(read(work/o)),without_clocks(read(OUT/o)))
        # Preserve the fresh replay, then restore the original clock-bearing input bytes
        # for the next frozen program's recorded dependency hashes.
        (work/o).rename(work/(o+'.fresh-replay'))
        (work/o).write_bytes((OUT/o).read_bytes())
def main():
    stage('Checking immutable feature evidence and fresh existence certificates')
    manifest=read(OUT/'Manifest.json')
    for path,e in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==e['bytes'] and sha(raw)==e['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,d in inventory[kind].items():assert d==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
    sp=PRIOR/'Equal_Population_Decoder.json';ia=PRIOR/'Equal_Population_Inputs.zip';cp=CLASS/'Full_Quartic_Class.json';ar=PAIR/'Pair_Arithmetic.json'
    pp=OUT/'Enlarged_Slice_Proposal.json';ep=OUT/'Enlarged_Slice_Certificate.json';sm=OUT/'Local_Slice_Proposal_v2.json';sc=OUT/'Small_Slice_Certificate.json'
    same(read(pp),quiet(proposal.run,sp,'1/1000000',180))
    cert=read(ep);small=read(sc);same(cert,quiet(certificate.run,pp,sp,ia,'1e-100'));same(small,quiet(certificate.run,sm,sp,ia,'1e-80'))
    stage('Independent complex Taylor, modular determinant and polynomial arithmetic')
    checked=read(OUT/'Independent_Feature_Audit.json');same(checked,quiet(audit.run,pp,ep,ia,cp,ar,sp))
    same(read(OUT/'Small_Independent_Audit.json'),quiet(audit.run,sm,sc,ia,cp,ar,sp))
    original=read(OUT/'Original_Export_Audit.json');corrected=read(OUT/'Corrected_Export_Audit.json')
    same(original,quiet(exports.run,OUT/'Local_Slice_Proposal.json',sp));same(corrected,quiet(exports.run,sm,sp))
    assert original['status']=='failed' and corrected['status']=='passed'
    adv=read(OUT/'Adversary_Audit.json');same(adv,quiet(adversary.run,pp,ep,ia,sp,OUT/'Original_Export_Audit.json',OUT/'Corrected_Export_Audit.json'))
    extra=read(OUT/'Observable_Boundary.json');same(extra,quiet(boundary.run,ep,sp))
    formal=read(OUT/'Lean_Check_v2.json');project=ROOT.parent/'acs-research/lean-audit/withMathlib';binary=ROOT.parent/'acs-research/runtime/lean-4.34.0-rc2-darwin_aarch64/bin'
    module=project/'.lake/packages/mathlib/Mathlib/Topology/MetricSpace/Contracting.lean';module_olean=project/'.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Topology/MetricSpace/Contracting.olean'
    acquisition=read(OUT/'Runtime_Acquisition.json');sources=read(OUT/'Source_Acquisition.json')
    assert acquisition['status']=='passed' and acquisition['module_source_sha256']==sources['module_source_sha256']==sha(module.read_bytes())
    assert acquisition['module_olean_sha256']==sha(module_olean.read_bytes()) and acquisition['lake_manifest_sha256']==sha((project/'lake-manifest.json').read_bytes())
    mathlib=project/'.lake/packages/mathlib';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathlib,text=True).strip()==sources['mathlib_revision']
    assert subprocess.check_output(['git','show','HEAD:Mathlib/Topology/MetricSpace/Contracting.lean'],cwd=mathlib)==module.read_bytes()
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:assert z.read('external/Mathlib/Topology/MetricSpace/Contracting.lean')==module.read_bytes()
    stage('Fresh Lean root-existence proof and preserved exploratory replay')
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory);replay_exploration(tmp)
        assert quiet(lean.run,CODE/'proofs/FeatureContraction_v2.lean',project,binary,tmp/'Fresh_Lean.json',tmp/'versions')==0
        fresh=read(tmp/'Fresh_Lean.json')
        for k in ['status','source_sha256','checker_sha256','returncode','stdout','stderr','olean_sha256','lake_manifest_sha256','theorems']:same(fresh[k],formal[k])
        assert formal['status']=='passed' and len(formal['theorems'])==6 and 'sorryAx' not in formal['stdout']
    with zipfile.ZipFile(OUT/'Lean_Artifacts.zip') as z:
        expected={'Lean_Check.json','Lean_Check_after_acquisition.json','Lean_Check_v2.json','Lean_Check_v2.olean','FeatureContraction.lean','FeatureContraction_v2.lean'}
        assert set(z.namelist())==expected and sha(z.read('Lean_Check_v2.olean'))==formal['olean_sha256']
        for name,source in [('Lean_Check.json','FeatureContraction.lean'),('Lean_Check_after_acquisition.json','FeatureContraction.lean'),('Lean_Check_v2.json','FeatureContraction_v2.lean')]:
            record=read(OUT/name);same(record,json.loads(z.read(name)));assert record['source_sha256']==sha(z.read(source))==sha((CODE/'proofs'/source).read_bytes())
            assert record['status']==('passed' if name=='Lean_Check_v2.json' else 'failed')
        assert 'Contracting.olean' in read(OUT/'Lean_Check.json')['stdout'] and 'LE Type' in read(OUT/'Lean_Check_after_acquisition.json')['stdout']
    summary=summarize(cert,small,checked,adv,extra,formal);same(summary,read(OUT/'Feature_Collision_Summary.json')['derived_results'])
    assert summary['mutations_rejected']==35 and summary['critical_split_amplification']==1000000 and summary['witness_interior_counts']==[1,2]
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==18 and sorted(n for n,r in receipts.items() if r['returncode'])==FAILURES
    assert all(not r['timed_out'] for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for n,r in receipts.items():
            same(r,json.loads(z.read(n+'/receipt.json')));assert set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(n+'/'+stream+'.txt'))==r[stream+'_sha256']
        assert 'matrix is numerically singular' in z.read('overextended-feature-slice-proposal/stderr.txt').decode()
        launch=read(OUT/'Launch_Failure.json');same(launch,json.loads(z.read('unreceipted-launch/Launch_Failure.json')))
        assert launch['status']=='launch_failed_before_scientific_program' and 'not a runner-generated receipt' in launch['record_provenance']
        assert z.read('unreceipted-launch/stdout.txt')==z.read('unreceipted-launch/stderr.txt')==b''
    for path,d in read(OUT/'Inherited_Inputs.json')['files_sha256'].items():assert sha((ROOT/path).read_bytes())==d
    primary=read(OUT/'Primary_Sources.json')
    for path,d in primary['inherited_source_records_sha256'].items():assert sha((ROOT/path).read_bytes())==d
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};q=read(OUT/'Research_Queue.json');after={b['id']:b for b in q['branches']}
    assert set(before)==set(after) and len(after)==117 and q['new_branches']==[] and q['advanced_existing_branches']==ADVANCED and not q['global_exhaustion_claimed']
    assert q['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==433 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);d=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==d;last=d
    assert index==438;links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'FEATURE_COLLISION_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    stage('All new checks passed; recursively verifying preceding ACS checkpoints')
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_equal_population_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'manifest_files':len(manifest['files']),'preceding_checkpoint_integrity':'passed',
        'fresh_numerical_proposal_and_both_contraction_certificates':'passed','fresh_independent_complex_Taylor_modular_and_arithmetic_audits':'passed',
        'fresh_omitted_observable_boundaries_and_adversaries':'passed','fresh_original_export_bug_rejection':'passed','fresh_exploratory_replay':'passed','fresh_Lean_compilation':'passed',
        'derived_results':summary,'recorded_commands':18,'successful_commands':14,'failed_commands':4,'separately_recorded_launch_failures':1,
        'research_branches':117,'ledger_events':438,'preserved_event_prefix':433,'ledger_head_sha256':last,'local_links':links,
        'full_calculus_arithmetic_and_spectral_bridge_formalized_in_Lean':False,
        'scope':'Two actual fields share exactly17finite Gaussian features at a radius strictly below the full-point-list ambiguity bound. Independent interval existence routes and rational coordinate checks replace a mere small-residual claim. The constructed witness has different interior counts and omitted moments/kernels; optimal augmented-feature identifiability and the wider ACS program remain open.'},indent=2))
if __name__=='__main__':main()
