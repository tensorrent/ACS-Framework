"""Verify the full metadata field class, actual A4 controls and count-only arithmetic decoding."""
import hashlib,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from pathlib import Path
import dedekind_full_quartic_class as classification
import dedekind_full_quartic_audit as audit
import dedekind_quartic_class_controls as controls
import dedekind_class_count_decode as decode
import dedekind_class_count_audit as count_audit
import dedekind_full_class_adversary as adversary
from verify_aggregate_moment_delta import quiet,canonical,unpack

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-14-aggregate-classification-delta';PRIOR=ROOT/'docs/frontier/2026-09-14-aggregate-primal-delta'
BASELINE=ROOT/'docs/frontier/2026-09-13-aggregate-delta';PAIR=ROOT/'docs/frontier/2026-09-13-biquadratic-delta'
ADVANCED=['R12','R13','R14','R15','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def stage(s):print(s,file=sys.stderr,flush=True)
def unique_object(pairs):
    keys=[k for k,v in pairs];assert len(keys)==len(set(keys)), 'JSON key collision'
    return dict(pairs)
def normalized(value):
    return json.loads(json.dumps(value),object_pairs_hook=unique_object)
def same(a,b):assert canonical(normalized(a))==canonical(normalized(b))
def comparison_controls():
    same({'counts':{'1':1,'12':1,'2':3}}, {'counts':{1:1,2:3,12:1}})
    same({'pairs':[[1,2]]},{'pairs':[(1,2)]})
    try:same({'counts':{'3':4}},{'counts':{3:3}})
    except AssertionError:pass
    else:raise AssertionError('Changed count accepted')
    try:normalized({1:'a','1':'b'})
    except AssertionError:pass
    else:raise AssertionError('Colliding JSON keys accepted')
    return 4
def summarize(c,a,co,d,ca,adv):
    return {'Galois_group_derived':c['Galois_group_derived'],'complete_quartic_candidate_count':c['complete_quartic_candidate_count'],
            'candidate_quadratic_discriminants':[m['quadratic_discriminants'] for m in c['retained_models']],
            'exhausted_A4_subsets':a['independent_group_audit']['exhausted_identity_containing_A4_subsets'],
            'sign_functions_tested':a['independent_character_audit']['sign_functions_tested'],'quadratic_characters':8,'character_planes':7,
            'actual_A4_control_discriminants':[f['field_discriminant'] for f in co['fields']],
            'projective_maximality_checks':co['projective_maximality_checks'],'nonzero_residue_cosets_covered':co['nonzero_residue_cosets_covered'],
            'count_decoding_cases':len(d['cases']),'uniquely_decoded_cases':sum(c['field_unique_for_every_admissible_count'] for c in d['cases']),
            **{k:ca[k] for k in ['metadata_only_unique_coefficients','coefficients_resolved_by_distinguishing_count','differing_targets','independent_polynomial_factorizations','coefficient_comparisons','exact_complete_T20_counts']},
            'robust_count_gate':d['robust_count_gate'],'half_radius_ambiguity_controls':len(ca['radius_half_count_ambiguity_witnesses']),
            'actual_component_mutations_rejected':adv['actual_component_mutations_rejected']}

def main():
    assert comparison_controls()==4
    manifest=read(OUT/'Manifest.json')
    for path,e in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==e['bytes'] and sha(raw)==e['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,d in inventory[kind].items():assert d==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
    stage('Fresh full-class enumeration, independent group/character audit and actual-field maximality controls')
    metadata=OUT/'Metadata.json';cp=OUT/'Full_Quartic_Class.json';ap=OUT/'Full_Class_Audit.json';cop=OUT/'A4_Field_Controls.json'
    dp=OUT/'Complete_Class_Count_Decode.json';cap=OUT/'Complete_Count_Audit.json';advp=OUT/'Adversary_Audit.json'
    c=read(cp);same(c,quiet(classification.run,metadata))
    a=read(ap);same(a,quiet(audit.run,cp,metadata,PAIR/'Pair_Candidate_Class.json'))
    co=read(cop);same(co,quiet(controls.run))
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory)
        unpack(BASELINE/'Aggregate_Inputs.zip',tmp,['S1_160.json','S2_160.json','S1_224.json','S2_224.json'])
        unpack(BASELINE/'Measurements_Recovery.zip',tmp,['Measurements160.json','Measurements224.json','Recovery160.json','Recovery224.json'])
        unpack(PAIR/'Pair_Spectra.zip',tmp,['Pair_Spectrum160.json','Pair_Spectrum224.json','Pair_Spectral_Audit.json'])
        spectra=[tmp/'Pair_Spectrum160.json',tmp/'Pair_Spectrum224.json'];observations=[tmp/'S1_224.json',tmp/'S2_224.json'];m=tmp/'Measurements224.json'
        arithmetic=PAIR/'Pair_Arithmetic.json';old=PAIR/'Pair_Decoding.json'
        stage('Fresh count decoding, independent attainable sets and 1128 local polynomial factorizations')
        d=read(dp);same(d,quiet(decode.run,cp,ap,spectra,observations))
        ca=read(cap);same(ca,quiet(count_audit.run,dp,cp,ap,spectra,observations,arithmetic,old,m))
        stage('Fresh semantic adversary and provenance replay')
        adv=read(advp);same(adv,quiet(adversary.run,cp,metadata,cop,dp,ap,spectra,observations,arithmetic,old,m))
        sources=read(OUT/'Primary_Sources.json');assert sources['metadata_sha256']==sha(metadata.read_bytes())
        assert sources['metadata_source_sha256']=={p.name:sha(p.read_bytes()) for p in observations}
        for p in observations:assert {k:read(p)[k] for k in read(metadata)}==read(metadata)
        paths={p.name:p for p in [cp,ap,cop,dp,cap,advp,metadata,m,arithmetic,old,PAIR/'Pair_Candidate_Class.json']+spectra+observations}
        for document in [c,a,d,ca,adv]:
            for name,digest in document['inputs_sha256'].items():assert sha(paths[name].read_bytes())==digest
    result=summarize(c,a,co,d,ca,adv);same(result,read(OUT/'Classification_Summary.json')['derived_results'])
    assert result['Galois_group_derived']=='V4' and result['complete_quartic_candidate_count']==2 and result['exhausted_A4_subsets']==2048
    assert result['actual_A4_control_discriminants']==[3136,5184] and (result['projective_maximality_checks'],result['nonzero_residue_cosets_covered'])==(470,2510)
    assert (result['count_decoding_cases'],result['uniquely_decoded_cases'])==(20,16)
    assert (result['metadata_only_unique_coefficients'],result['coefficients_resolved_by_distinguishing_count'])==(456,148)
    assert result['differing_targets']==[3,7,19,27,31] and result['independent_polynomial_factorizations']==1128 and result['coefficient_comparisons']==1208
    assert result['exact_complete_T20_counts']==[23,22] and result['half_radius_ambiguity_controls']==8 and result['actual_component_mutations_rejected']==13
    receipts=read(OUT/'Execution_Receipts.json');assert len(receipts)==7 and all(r['returncode']==0 and not r['timed_out'] for r in receipts.values())
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r and set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
        same(json.loads(z.read('classification-input-acquisition/stdout.txt')),sources)
    assert sources['new_downloads']==1 and sources['reused_local_primary_PDFs']==1 and len(sources['sources'])==2
    assert sources['inherited_sources']['sha256']==sha((ROOT/sources['inherited_sources']['record']).read_bytes())
    for source in sources['sources']:assert len(source['sha256'])==64 and source['bytes']>100000 and not source['redistributed_in_repository']
    for path,digest in read(OUT/'Inherited_Inputs.json')['files_sha256'].items():assert sha((ROOT/path).read_bytes())==digest
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};q=read(OUT/'Research_Queue.json');after={b['id']:b for b in q['branches']}
    assert set(before)==set(after) and len(after)==117 and q['new_branches']==[] and q['advanced_existing_branches']==ADVANCED and not q['global_exhaustion_claimed']
    assert q['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition'] and a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes();assert len(prefix.splitlines())==418 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==423;links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'FULL_QUARTIC_CLASS_README_v2.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    attempts=read(OUT/'Verification_Attempts.json')
    assert set(attempts)=={'final-recursive-verification','verification-diagnosis'}
    assert attempts['final-recursive-verification']['returncode']==1 and attempts['verification-diagnosis']['returncode']==0
    with zipfile.ZipFile(OUT/'Verification_Attempt_Artifacts.zip') as z:
        for name,r in attempts.items():
            same(json.loads(z.read(name+'/receipt.json')),r)
            assert set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
        same(json.loads(z.read('verification-diagnosis/stdout.txt')),read(OUT/'Verification_Diagnosis.json'))
    with zipfile.ZipFile(OUT/'Packaging_Attempt_v1.zip') as z:
        old_manifest=json.loads(z.read(str((OUT/'Manifest.json').relative_to(ROOT))))
        for name,e in old_manifest['files'].items():
            raw=z.read(name);assert sha(raw)==e['sha256'] and len(raw)==e['bytes']
        old_receipts=json.loads(z.read(str((OUT/'Execution_Receipts.json').relative_to(ROOT))))
        same(old_receipts,receipts)
        for name in ['Metadata.json','Full_Quartic_Class.json','Full_Class_Audit.json','A4_Field_Controls.json','Complete_Class_Count_Decode.json','Complete_Count_Audit.json','Adversary_Audit.json','Primary_Sources.json','Branch_Events.jsonl','Research_Queue.json']:
            assert z.read(str((OUT/name).relative_to(ROOT)))==(OUT/name).read_bytes()
    stage('All new scientific/provenance checks passed; verifying prior checkpoints recursively')
    prior=subprocess.run([sys.executable,str(CODE/'verify_aggregate_primal_delta.py')],capture_output=True,text=True)
    assert prior.returncode==0,prior.stdout+prior.stderr
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),'manifest_files':len(manifest['files']),'preceding_checkpoint_integrity':'passed',
        'derived_results':result,'fresh_full_class_and_independent_enumeration':'passed','fresh_actual_A4_maximality_controls':'passed','fresh_count_decoding_and_polynomial_audit':'passed',
        'number_theoretic_proof_formalized_in_Lean':False,'new_roots_computed':0,'recorded_commands':7,'successful_commands':7,'failed_commands':0,'preserved_failed_verification_attempts':1,'verification_diagnosis':'passed','JSON_comparison_controls':4,
        'research_branches':117,'ledger_events':423,'preserved_event_prefix':418,'ledger_head_sha256':last,'local_links':links,
        'scope':'Fresh computational replay supports the written metadata-only quartic classification and count-based arithmetic selection, with actual A4 hypothesis controls and thirteen mutations. General number theory is source-backed written mathematics, not a Lean proof. Complete classification is scoped to the stated invariants; the wider ACS investigation remains active.'},indent=2))

if __name__=='__main__':main()
