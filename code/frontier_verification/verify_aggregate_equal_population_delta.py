"""Fresh equal-population science, immutable evidence and preceding ACS checkpoints."""
import hashlib,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from pathlib import Path
import dedekind_equal_population_inputs as inputs
import dedekind_equal_population_decode as decode
import dedekind_equal_population_audit as audit
import dedekind_equal_population_adversary as adversary
import dedekind_equal_population_plateau as plateau
import check_interior_count_lean as lean
from verify_aggregate_classification_delta_v2 import same,canonical,quiet

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-14-aggregate-equal-population-delta'
PRIOR=ROOT/'docs/frontier/2026-09-14-aggregate-cardinality-delta'
CLASS=ROOT/'docs/frontier/2026-09-14-aggregate-classification-delta'
BASELINE=ROOT/'docs/frontier/2026-09-13-aggregate-delta';PAIR=ROOT/'docs/frontier/2026-09-13-biquadratic-delta'
ADVANCED=['R12','R13','R14','R15','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def stage(s):print(s,file=sys.stderr,flush=True)
def summarize(provenance,decoded,checked,adv,cutoffs,formal):
    d=checked['decode_audit'];m=decoded['matching_cases'][0]
    return {'source_cutoff':'39/2','equal_populations':[22,22],'anonymous_input_files':len(provenance['cases']),
            'parent_intervals_partitioned':checked['cutoff_audit']['partitioned_source_intervals'],'retained_intervals':88,
            'metadata_and_total_population_fixed_coefficients':456,'interior_count_cases':len(d['count_cases']),'uniformly_unique_count_cases':d['uniformly_unique_count_cases'],
            'coefficients_fixed_by_unique_count':604,'common_observation_fixed_coefficients':456,'common_observation_ambiguous_coefficients':148,'differing_targets':d['differing_targets'],
            'exact_symbolic_threshold':m['exact_symbolic_threshold'],'rational_height':m['rational_height'],'threshold_bracket':[m['radius_lower'],m['radius_upper']],
            'threshold_bracket_width':m['bracket_width'],'rational_gate_guarantee':'0 <= r < L','actual_common_observation_at_U':True,'actual_ambiguity_at_L_claimed':False,
            'independent_polynomial_factorizations':checked['independent_polynomial_factorizations'],'polynomial_coefficient_comparisons':d['polynomial_coefficient_comparisons'],
            'common_observation_endpoint_checks':d['common_observation_endpoint_checks'],'strict_noncritical_pair_comparisons':d['strict_noncritical_comparisons'],
            'all_bipartite_pair_cost_entries':d['all_pair_cost_entries'],'bipartite_boundary_checks':len(d['bipartite_boundary_checks']),
            'finite_multiset_pairs':adv['finite_crosscheck']['equal_length_multiset_pairs'],'literal_indexed_matchings':adv['finite_crosscheck']['literal_indexed_matchings'],
            'finite_positive_gap_count_gates':adv['finite_crosscheck']['positive_gap_count_gates'],'mutations_rejected':adv['mutations_rejected']+len(cutoffs['mutations']),
            'cutoff_plateau':[cutoffs['cases'][0]['cutoff_lower'],cutoffs['cases'][0]['cutoff_upper']],'cutoff_plateau_exact_checks':cutoffs['independent_exact_checks'],
            'kernel_checked_lemmas':len(formal['theorems']),'new_roots_computed':0,'new_Gaussian_measurements':0}
def main():
    stage('Verifying immutable sources and fresh equal-population science')
    manifest=read(OUT/'Manifest.json')
    for path,e in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==e['bytes'] and sha(raw)==e['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,d in inventory[kind].items():assert d==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
    cp=CLASS/'Full_Quartic_Class.json';ca=CLASS/'Full_Class_Audit.json';parent=BASELINE/'Aggregate_Inputs.zip';spectra=PAIR/'Pair_Spectra.zip';ar=PAIR/'Pair_Arithmetic.json'
    pp=OUT/'Input_Provenance.json';dp=OUT/'Equal_Population_Decoder.json'
    provenance=read(pp);decoded=read(dp);checked=read(OUT/'Equal_Population_Audit.json');adv=read(OUT/'Adversary_Audit.json');cuts=read(OUT/'Cutoff_Plateau.json');formal=read(OUT/'Lean_Check_v3.json')
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory);fresh_inputs=tmp/'inputs'
        same(provenance,quiet(inputs.run,parent,'39/2',fresh_inputs))
        with zipfile.ZipFile(OUT/'Equal_Population_Inputs.zip') as z:
            assert set(z.namelist())=={c['input_member'] for c in provenance['cases']}
            for name in z.namelist():assert z.read(name)==(fresh_inputs/name).read_bytes()
        same(decoded,quiet(decode.run,cp,ca,fresh_inputs,spectra))
        same(checked,quiet(audit.run,dp,pp,cp,fresh_inputs,parent,spectra,ar))
        stage('Fresh adversarial, cutoff-continuum and Lean checks')
        same(adv,quiet(adversary.run,dp,pp,cp,fresh_inputs,parent,spectra,ar))
        same(cuts,quiet(plateau.run,parent,spectra))
        project=ROOT.parent/'acs-research/lean-audit/withMathlib';binary=ROOT.parent/'acs-research/runtime/lean-4.34.0-rc2-darwin_aarch64/bin'
        assert quiet(lean.run,CODE/'proofs/InteriorCount_v3.lean',project,binary,tmp/'Fresh_Lean.json',tmp/'lean-versions')==0
        fresh=read(tmp/'Fresh_Lean.json')
        for k in ['status','source_sha256','checker_sha256','returncode','stdout','stderr','olean_sha256','lake_manifest_sha256','theorems']:same(fresh[k],formal[k])
        assert formal['status']=='passed' and len(formal['theorems'])==8 and 'sorryAx' not in formal['stdout']
    with zipfile.ZipFile(OUT/'Lean_Artifacts.zip') as z:
        expected={'Lean_Check.json','Lean_Check_v2.json','Lean_Check_v3.json','Lean_Check_v3.olean','InteriorCount.lean','InteriorCount_v2.lean','InteriorCount_v3.lean'}
        assert set(z.namelist())==expected and sha(z.read('Lean_Check_v3.olean'))==formal['olean_sha256']
        for suffix in ['','_v2','_v3']:
            name='Lean_Check'+suffix+'.json';record=read(OUT/name);same(record,json.loads(z.read(name)))
            assert record['source_sha256']==sha(z.read('InteriorCount'+suffix+'.lean'))==sha((CODE/('proofs/InteriorCount'+suffix+'.lean')).read_bytes())
            assert record['status']==('passed' if suffix=='_v3' else 'failed')
        assert 'Mathlib/Tactic/Omega.olean' in read(OUT/'Lean_Check.json')['stdout']
        assert "unexpected token 'prefix'" in read(OUT/'Lean_Check_v2.json')['stdout']
    summary=summarize(provenance,decoded,checked,adv,cuts,formal);same(summary,read(OUT/'Equal_Population_Summary.json')['derived_results'])
    assert summary['parent_intervals_partitioned']==90 and summary['mutations_rejected']==36 and summary['literal_indexed_matchings']==32016
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==8
    assert sorted(n for n,r in receipts.items() if r['returncode'])==['interior-count-lean','interior-count-lean-v2']
    assert all(not r['timed_out'] for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        assert set(z.namelist())=={n+'/'+f for n in receipts for f in ['receipt.json','stdout.txt','stderr.txt']}
        for n,r in receipts.items():
            same(r,json.loads(z.read(n+'/receipt.json')));assert set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(n+'/'+stream+'.txt'))==r[stream+'_sha256']
    for path,d in read(OUT/'Inherited_Inputs.json')['files_sha256'].items():assert sha((ROOT/path).read_bytes())==d
    sources=read(OUT/'Primary_Sources.json');assert sources['new_downloads']==0
    for path,d in sources['inherited_source_records_sha256'].items():assert sha((ROOT/path).read_bytes())==d
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};q=read(OUT/'Research_Queue.json');after={b['id']:b for b in q['branches']}
    assert set(before)==set(after) and len(after)==117 and q['new_branches']==[] and q['advanced_existing_branches']==ADVANCED and not q['global_exhaustion_claimed']
    assert q['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==428 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);d=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==d;last=d
    assert index==433;links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'INTERIOR_COUNT_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    stage('All new checks passed; recursively replaying preceding checkpoints')
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_cardinality_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'manifest_files':len(manifest['files']),
        'preceding_checkpoint_integrity':'passed','fresh_input_restriction':'passed','fresh_count_and_actual_witness_science':'passed',
        'fresh_independent_arithmetic_counts_and_bipartite_matching':'passed','fresh_adversaries_and_cutoff_continuum':'passed','fresh_lean_compilation':'passed',
        'derived_results':summary,'recorded_commands':8,'successful_commands':6,'failed_commands':2,'research_branches':117,'ledger_events':433,'preserved_event_prefix':428,'ledger_head_sha256':last,'local_links':links,
        'complete_arithmetic_and_full_matching_formalized_in_Lean':False,
        'scope':'The certified equal-population benchmark removes total-count identification. A sharp theoretical interior count still separates the actual binary field class below half the second-root gap; a rational gate certifies r<L and a shared actual observation is constructed at U. Closed-box ambiguity at L is not promoted to actual-field ambiguity. All prior ACS branches and the ongoing delta objective remain active.'},indent=2))
if __name__=='__main__':main()
