"""Reproduce preserved-population identification and actual one-deletion ambiguity."""
import hashlib,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import dedekind_population_decoder as decoder
import dedekind_population_matching as matching
import dedekind_population_audit as audit
import dedekind_population_adversary as adversary
import dedekind_population_critical_gap as critical
import dedekind_population_window as window
import check_population_observation_lean as lean
import check_population_window_lean as window_lean
from verify_aggregate_classification_delta_v2 import same,canonical,quiet

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-14-aggregate-cardinality-delta';PRIOR=ROOT/'docs/frontier/2026-09-14-aggregate-classification-delta'
BASELINE=ROOT/'docs/frontier/2026-09-13-aggregate-delta';PAIR=ROOT/'docs/frontier/2026-09-13-biquadratic-delta'
ADVANCED=['R12','R13','R14','R15','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def stage(s):print(s,file=sys.stderr,flush=True)
def domains(population,matched,windowed):
    source_cases=population['cases'];out=[]
    for case in matched['cases']:
        bits=case['precision_bits'];records=[next(c for c in source_cases if c['input_member']=='S'+str(i)+'_'+str(bits)+'.json') for i in [1,2]]
        values=[sorted({r['predicted_coefficients'][j] for r in records}) for j in range(len(population['columns']))]
        assert sum(len(v)==1 for v in values)==456 and sum(len(v)==2 for v in values)==148
        w=next(c for c in windowed['cases'] if c['precision_bits']==bits)
        assert w['common_observation_compatible_actual_classes']==case['distinct_actual_field_classes']
        out.append({'precision_bits':bits,'common_observation_radius':case['constructive_common_observation_radius'],'compatible_actual_classes':case['distinct_actual_field_classes'],
                    'one_deletion_common_observation':case['common_observation'],'window_common_observation':w['common_observation'],
                    'coefficient_domains':values,'fixed_coefficients':456,'ambiguous_coefficients':148})
    return {'columns':population['columns'],'cases':out,'scope':'Exact coefficient domains for the stored one-deletion and post-noise-window common observations within the completely classified metadata class. Both actual fields are compatible and no other field belongs to this class; the 456 shared values remain fixed while 148 differ.'}
def summarize(pop,matched,checked,adv,gap,windowed,formal,window_formal):
    return {'preserved_population_sizes':[23,22],'fixed_population_field_selection_independent_of_coordinate_radius':True,
            'coordinate_transformations':pop['coordinate_transformations_checked'],'collapsed_geometry_controls':pop['collapsed_geometry_controls'],
            'false_completeness_or_preservation_counterexamples':len(pop['false_population_contract_counterexamples']),
            'polynomial_factorizations':checked['population_audit']['independent_polynomial_factorizations'],
            'unique_field_coefficient_comparisons':checked['population_audit']['unique_field_coefficient_comparisons'],
            'observation_coefficient_comparisons':checked['population_audit']['observation_coefficient_comparisons'],
            'common_observation_population':22,'required_source_deletions':[1,0],'common_observation_fixed_coefficients':456,'common_observation_ambiguous_coefficients':148,
            'differing_targets':[3,7,19,27,31],'numerical_radius_bracket':[matched['cases'][0]['true_ambiguity_threshold_lower'],matched['cases'][0]['constructive_common_observation_radius']],
            'numerical_radius_bracket_width':gap['numerical_threshold_bracket_width'],'exact_symbolic_threshold':gap['exact_symbolic_threshold'],
            'optimal_deletion_indices_zero_based':gap['cases'][0]['optimal_deletion_indices_zero_based'],
            'matching_pair_rows':checked['matching_audit']['total_pair_rows_replayed'],'endpoint_inclusions':checked['matching_audit']['total_endpoint_inclusions'],
            'threshold_boundary_checks':checked['matching_audit']['total_threshold_boundary_checks'],
            'strict_critical_gap_inequalities':gap['independent_source_interval_audit']['total_strict_inequalities'],
            'post_noise_window_arbitrary_deletions':windowed['allowed_arbitrary_deletions'],
            'post_noise_window_visible_populations':windowed['cases'][0]['visible_population_after_window_selection'],
            'post_noise_window_exact_inequalities':windowed['independent_interval_audit']['total_exact_inequalities'],
            'arbitrary_finite_matching_problems':adv['finite_arbitrary_matching_crosscheck']['sorted_multiset_problems'],
            'literal_finite_matchings':adv['finite_arbitrary_matching_crosscheck']['arbitrary_indexed_matchings_enumerated'],
            'mutations_rejected':adv['actual_component_mutations_rejected']+len(gap['mutations'])+len(windowed['mutations']),
            'kernel_checked_observation_lemmas':len(formal['theorems'])+len(window_formal['theorems']),'new_roots_computed':0}
def replay_exploration(tmp):
    mirror=tmp/'exploratory/work';research=mirror/'acs-research/aggregate-cardinality-audit';repo=mirror/'acs-repo'
    research.mkdir(parents=True);repo.mkdir(parents=True)
    for source in [BASELINE/'Aggregate_Inputs.zip',PRIOR/'Full_Quartic_Class.json']:
        dst=repo/source.relative_to(ROOT);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(source.read_bytes())
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        for name in ['propose_population_observation.py','audit_population_proposal_v2.py']:(research/name).write_bytes(z.read('exploration/'+name))
    for name in ['propose_population_observation.py','audit_population_proposal_v2.py']:
        p=subprocess.run([sys.executable,str(research/name)],cwd=repo,capture_output=True,text=True)
        assert p.returncode==0,p.stdout+p.stderr
    for name in ['Population_Observation_Proposal.json','Population_Proposal_Audit.json']:same(read(research/name),read(OUT/name))
def main():
    stage('Checking manifests, immutable source versions and fresh observation science')
    manifest=read(OUT/'Manifest.json')
    for path,e in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==e['bytes'] and sha(raw)==e['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert digest==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
    cp=PRIOR/'Full_Quartic_Class.json';cap=PRIOR/'Full_Class_Audit.json';ia=BASELINE/'Aggregate_Inputs.zip';sa=PAIR/'Pair_Spectra.zip'
    ar=PAIR/'Pair_Arithmetic.json';me=BASELINE/'Measurements_Recovery.zip';pp=OUT/'Population_Decoder.json';mp=OUT/'Population_Matching.json';op=OUT/'Population_Observation_Proposal.json'
    pop=read(pp);same(pop,quiet(decoder.run,cp,cap,ia,sa))
    matched=read(mp);same(matched,quiet(matching.run,ia,pp,op))
    checked=read(OUT/'Population_Audit.json');same(checked,quiet(audit.run,pp,mp,cp,ia,sa,ar,me,op))
    stage('Fresh adversarial matching and critical-root-gap replay')
    adv=read(OUT/'Adversary_Audit.json');same(adv,quiet(adversary.run,pp,mp,cp,ia,sa,ar,me))
    gap=read(OUT/'Critical_Gap_Audit.json');same(gap,quiet(critical.run,mp,ia))
    windowed=read(OUT/'Population_Window_Audit.json');same(windowed,quiet(window.run,mp,OUT/'Critical_Gap_Audit.json',ia))
    same(domains(pop,matched,windowed),read(OUT/'Common_Observation_Domains.json'))
    formal=read(OUT/'Lean_Check.json');window_formal=read(OUT/'Window_Lean_Check.json')
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory)
        stage('Fresh replay of frozen exploratory successes and Lean compilation')
        replay_exploration(tmp)
        project=ROOT.parent/'acs-research/lean-audit/withMathlib';binary=ROOT.parent/'acs-research/runtime/lean-4.34.0-rc2-darwin_aarch64/bin'
        assert quiet(lean.run,CODE/'proofs/PopulationObservation.lean',project,binary,tmp/'Fresh_Lean.json',tmp/'lean-versions')==0
        fresh=read(tmp/'Fresh_Lean.json')
        for k in ['status','source_sha256','checker_sha256','returncode','stdout','stderr','olean_sha256','lake_manifest_sha256','theorems']:same(formal[k],fresh[k])
        assert formal['status']=='passed' and len(formal['theorems'])==5
        assert quiet(window_lean.run,CODE/'proofs/WindowCensoring.lean',project,binary,tmp/'Fresh_Window_Lean.json',tmp/'window-lean-versions')==0
        fresh_window=read(tmp/'Fresh_Window_Lean.json')
        for k in ['status','source_sha256','checker_sha256','returncode','stdout','stderr','olean_sha256','lake_manifest_sha256','theorems']:same(window_formal[k],fresh_window[k])
        assert window_formal['status']=='passed' and len(window_formal['theorems'])==3
    with zipfile.ZipFile(OUT/'Lean_Artifacts.zip') as z:
        assert set(z.namelist())=={'Lean_Check.json','Lean_Check.olean','PopulationObservation.lean','Population_Lean_Audit.json','Window_Lean_Check.json','Window_Lean_Check.olean','WindowCensoring.lean'}
        same(json.loads(z.read('Lean_Check.json')),formal)
        assert sha(z.read('Lean_Check.olean'))==formal['olean_sha256'] and sha(z.read('PopulationObservation.lean'))==formal['source_sha256']
        old=json.loads(z.read('Population_Lean_Audit.json'));assert old['status']=='passed' and old['artifact_sha256']==formal['olean_sha256'] and old['source_sha256']==formal['source_sha256']
        assert old['driver_sha256'] in hashes and old['lake_manifest_sha256']==formal['lake_manifest_sha256'] and old['theorems']==formal['theorems'] and old['stdout']==formal['stdout']
        same(json.loads(z.read('Window_Lean_Check.json')),window_formal)
        assert sha(z.read('Window_Lean_Check.olean'))==window_formal['olean_sha256'] and sha(z.read('WindowCensoring.lean'))==window_formal['source_sha256']
    result=summarize(pop,matched,checked,adv,gap,windowed,formal,window_formal);same(result,read(OUT/'Population_Summary.json')['derived_results'])
    assert result['coordinate_transformations']==72 and result['common_observation_ambiguous_coefficients']==148 and result['mutations_rejected']==34
    assert result['post_noise_window_arbitrary_deletions']==0 and result['post_noise_window_exact_inequalities']==198 and result['kernel_checked_observation_lemmas']==8
    assert result['matching_pair_rows']==1012 and result['strict_critical_gap_inequalities']==286 and result['literal_finite_matchings']==41796
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==13
    failures=sorted(n for n,r in receipts.items() if r['returncode']!=0)
    assert failures==['independent-population-proposal','population-lean-lemmas'] and all(not r['timed_out'] for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            same(json.loads(z.read(name+'/receipt.json')),r);assert set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
        assert 'upper-lower<F(1,10**30)' in z.read('independent-population-proposal/stderr.txt').decode()
        assert 'must be contained in root directory' in z.read('population-lean-lemmas/stdout.txt').decode()
    for path,digest in read(OUT/'Inherited_Inputs.json')['files_sha256'].items():assert sha((ROOT/path).read_bytes())==digest
    sources=read(OUT/'Primary_Sources.json');assert sources['new_downloads']==0
    for path,digest in sources['inherited_source_records_sha256'].items():assert sha((ROOT/path).read_bytes())==digest
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};q=read(OUT/'Research_Queue.json');after={b['id']:b for b in q['branches']}
    assert set(before)==set(after) and len(after)==117 and q['new_branches']==[] and q['advanced_existing_branches']==ADVANCED and not q['global_exhaustion_claimed']
    assert q['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==423 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==428;links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'POPULATION_OBSERVATION_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    stage('All new checks passed; verifying preceding checkpoints recursively')
    previous=subprocess.run([sys.executable,str(CODE/'verify_aggregate_classification_delta_v2.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'manifest_files':len(manifest['files']),'preceding_checkpoint_integrity':'passed',
        'derived_results':result,'fresh_population_and_actual_matching':'passed','fresh_independent_arithmetic_DP_and_critical_gap':'passed','fresh_exploratory_success_replay':'passed',
        'fresh_lean_compilation':'passed','general_arithmetic_and_full_matching_proof_formalized_in_Lean':False,
        'recorded_commands':13,'successful_commands':11,'failed_commands':2,'research_branches':117,'ledger_events':428,'preserved_event_prefix':423,'ledger_head_sha256':last,'local_links':links,
        'scope':'Preserved cardinality identifies this completely classified field pair independently of coordinate errors. Under one deletion, or coordinate noise followed by complete window selection with no arbitrary deletions, actual fields admit a common observation at a threshold given exactly by half their second-root gap, with a2e-30 numerical bracket. Fresh independent arithmetic, matching, adversarial, interval and eight elementary Lean checks support the written proof. The wider ACS goal remains active.'},indent=2))
if __name__=='__main__':main()
