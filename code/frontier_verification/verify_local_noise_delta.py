"""Verify retained local-information/noise evidence and append-only research history."""
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,re,subprocess,sys,zipfile

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-local-noise-delta';PRIOR=ROOT/'docs/frontier/2026-09-13-quadratic-delta'
ADVANCED=['R12','R13','R14','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def read(p):return json.loads(p.read_text())
def key(c):return c['label'],c['delta'],c['top'],c['profile']

def main():
    earlier=subprocess.run([sys.executable,str(CODE/'verify_quadratic_delta.py')],capture_output=True,text=True)
    assert earlier.returncode==0,earlier.stdout+earlier.stderr
    manifest=read(OUT/'Manifest.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    del raw
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        source_hashes={sha(z.read(n)) for n in z.namelist() if n.endswith('.py')}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert sha(z.read(kind+'/'+path))==digest==sha((ROOT/path).read_bytes())
    wide_audit=read(OUT/'Wide_Audit.json');local_audit=read(OUT/'Local_Audit.json')
    for audit,source in [(wide_audit,'dedekind_wide_audit.py'),(local_audit,'dedekind_local_noise_audit.py')]:
        assert audit['status']=='passed' and audit['source_sha256']==sha((CODE/source).read_bytes())
    assert local_audit['producer_sha256']==sha((CODE/'dedekind_local_noise.py').read_bytes())
    assert local_audit['profiles_source_sha256']==sha((CODE/'dedekind_local_profiles.py').read_bytes())
    with zipfile.ZipFile(PRIOR.parent/'2026-09-13-coupled-delta/Measurements.zip') as z:measurement_hash=sha(z.read('Measurements.json'))
    range_summaries={};range_hashes={};phase_count=0;range_exclusions=0
    with zipfile.ZipFile(OUT/'Noise_Producers.zip') as z:
        assert set(z.namelist())=={'Wide_Ranges160.json','Wide_Ranges224.json','Local_Noise160.json','Local_Noise224.json'}
        # Process the large range files separately instead of retaining all
        # raw buffers and parsed interval certificates at once.
        for bits in [160,224]:
            name='Wide_Ranges'+str(bits)+'.json';raw=z.read(name);range_hashes[name]=sha(raw);data=json.loads(raw);del raw
            assert data['status']=='passed' and data['input_sha256']==measurement_hash
            assert data['source_sha256']==sha((CODE/'dedekind_ordinate_ranges.py').read_bytes())
            assert data['core_sha256']==sha((CODE/'dedekind_coupled_recovery.py').read_bytes()) and data['precision_bits']==bits
            assert len(data['cases'])==30 and data['methods']==['stationary']
            phase_count+=sum(len(d['critical_points']) for b in data['bounds'] for d in b['diagnostics'])
            compact={}
            for case in data['cases']:
                case_key=(case['additional_radius'],case['settings']['top'],case['method'],case['policy'])
                replay=next(r for r in wide_audit['interval_replays'] if r['file']==name and tuple(r['case'])==case_key)
                count=sum(len(s['removals']) for s in case['rounds']);range_exclusions+=count
                assert count==replay['exclusions'] and replay['all_604_arithmetic_coefficients_retained']
                domains=[d['candidates'] for d in case['domains']];assert sha(canonical(domains))==replay['domains_sha256']
                compact[case_key]={'domains':case['domains'],'unique':case['unique_target_coefficients']}
            range_summaries[bits]=compact;del data
        assert range_hashes==wide_audit['results_sha256'] and range_exclusions==wide_audit['exclusions_replayed']==10592
        assert phase_count==wide_audit['critical_point_strict_phase_brackets']==560440
        assert range_summaries[160]==range_summaries[224] and wide_audit['precision_domain_comparisons']==30
        assert wide_audit['domain_inclusion_comparisons']==94 and wide_audit['probe_repeat_cases']==0
        assert wide_audit['mpmath_digits']==80 and len(wide_audit['mpmath_extrema_cases'])==12
        assert all(c['inside_certified_extrema_bounds'] for c in wide_audit['mpmath_extrema_cases'])
        local_hashes={};local_counts=0;spectral_counts=0;minima=0;compact_runs={}
        for bits in [160,224]:
            name='Local_Noise'+str(bits)+'.json';raw=z.read(name);local_hashes[name]=sha(raw);data=json.loads(raw);del raw
            assert data['status']=='passed' and data['source_sha256']==local_audit['producer_sha256']
            assert data['profiles_source_sha256']==local_audit['profiles_source_sha256'] and data['measurement_input_sha256']==measurement_hash
            assert data['inputs']['wide']['sha256']==range_hashes['Wide_Ranges'+str(bits)+'.json']
            assert data['catalogue']==local_audit['independent_catalogue'] and len(data['catalogue'])==11
            assert len(data['cases'])==88 and data['fixed_point_scale_bits']==192
            compact={}
            for case in data['cases']:
                replay=next(r for r in local_audit['replays'] if tuple(r['case'])==key(case) and r['precision_bits']==bits)
                domains=[d['candidates'] for d in case['domains']]
                assert replay['domains_sha256']==sha(canonical(domains)) and replay['all_604_arithmetic_coefficients_retained']
                lc=sum(len(ch['before'])-len(ch['after']) for s in case['rounds'] for c in s['local_checks'] for ch in c['changes'])
                sc=sum(len(s['spectral_checks']) for s in case['rounds'])
                assert lc==replay['local_candidates_removed'] and sc==replay['spectral_candidates_removed']
                assert all(int(w['strict_gap_scaled_integer'])>0 for s in case['rounds'] for w in s['spectral_checks'])
                local_counts+=lc;spectral_counts+=sc;minima+=len(case['minimal_quadratic_seed_observations'])
                assert len(replay['minimum_observation_checks'])==len(case['minimal_quadratic_seed_observations'])
                if case['label']=='wide_stationary':
                    origin=range_summaries[bits][case['delta'],case['top'],'stationary','retained_prefix']
                    assert case['seed_domains']==origin['domains'] and case['seed_unique_targets']==origin['unique']
                assert case['unique_target_coefficients']==sum(len(d['candidates'])==1 for d in case['domains'] if d['n']<=361)
                compact[key(case)]={k:case[k] for k in ['domains','local_models','seed_unique_targets','local_only_unique_targets',
                    'unique_target_coefficients','unique_target_prime_local_models','minimal_quadratic_seed_observations']}
            compact_runs[bits]=compact;del data
    assert local_hashes==local_audit['results_sha256']
    assert local_counts==local_audit['local_candidate_exclusions']==133128
    assert spectral_counts==local_audit['spectral_candidate_exclusions']==598
    assert minima==local_audit['minimal_observation_certificates']==64
    assert compact_runs[160]==compact_runs[224] and len(local_audit['replays'])==176
    assert local_audit['precision_domain_comparisons']==88 and local_audit['assumption_inclusion_comparisons']==176
    cases=compact_runs[160];profiles=['degree','degree_discriminant','galois','galois_discriminant']
    for delta,counts in [('1e-2',[53,68,67,91]),('2e-2',[31,36,35,82]),('3e-2',[22,26,26,62])]:
        assert [cases['wide_stationary',delta,2000,p]['unique_target_coefficients'] for p in profiles]==counts
    assert [cases['wide_stationary','1e-2',t,'galois_discriminant']['unique_target_coefficients'] for t in [220,600,1000,1500,2000]]==[75,84,91,91,91]
    for p in profiles:
        assert cases['quadratic','5e-3',2000,p]['unique_target_coefficients']==91
        assert cases['quadratic','5e-3',2000,p]['unique_target_prime_local_models']==24
    controls=local_audit['adversarial_controls'];g=controls['unsupported_galois_premise']
    assert g['polynomial']=='x**4 - x - 1' and g['irreducible_modulus']==2 and g['polynomial_discriminant']==-283
    assert g['unramified_prime']==7 and g['local_model']==[[1,1],[1,3]] and g['first_coefficient']==1 and g['rejected_by_unsupported_galois_condition']
    assert controls['ramification_exponent_in_coefficient']=={'model':[[4,1]],'correct_coefficient':1,'incorrect_multiplicity_weighted_coefficient':4}
    missing=controls['missing_domain_prerequisites']
    assert F(missing['certified_gap_lower_bound'])>0 and missing['full_exact_dyadic_gap_at_least_lower_bound']
    assert int(missing['missing_prerequisite_gap_scaled_integer'])<=0
    assert len(local_audit['symbolic_euler_identities'])==11 and all(r['logarithmic_derivative_identity'] for r in local_audit['symbolic_euler_identities'])
    receipts=read(OUT/'Execution_Receipts.json')
    assert len(receipts)==9 and {n for n,r in receipts.items() if r['returncode']!=0}=={'local-independent-audit','local-independent-audit2'}
    assert receipts['local-independent-audit2']['returncode']==-15
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
            assert set(r['input_sources_sha256'].values())<=source_hashes
        assert '4300 digits' in z.read('local-independent-audit/stderr.txt').decode()
        assert json.loads(z.read('Arithmetic_Interruption.json'))['terminal_returncode']==-15
    adversary=read(OUT/'Local_Adversary.json')
    assert adversary['status']=='passed' and adversary['source_sha256']==sha((CODE/'dedekind_local_adversary.py').read_bytes())
    assert adversary['polynomial_discriminant']==adversary['field_discriminant']==-283
    assert len(adversary['mod2_nondivisibility'])==6 and all(c['remainder_ascending_mod2'] for c in adversary['mod2_nondivisibility'])
    assert len(adversary['cubic_residues_at_0_through_6_mod7'])==7 and all(adversary['cubic_residues_at_0_through_6_mod7'])
    assert adversary['local_residue_degrees']==[1,3] and adversary['coefficient_at_7']==1
    summary=read(OUT/'Local_Noise_Summary.json')
    assert summary['quadratic_seed_degree_only_unique_targets']==91 and summary['original_unresolved_local_factors']==48
    assert summary['larger_radius_galois_discriminant_counts']=={'1e-2':91,'2e-2':82,'3e-2':62}
    ledger=(OUT/'Branch_Events.jsonl').read_bytes();prefix=(PRIOR/'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(prefix) and len(prefix.splitlines())==369;last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        event=json.loads(line);digest=event.pop('event_sha256')
        assert event['sequence']==index and event['previous_event_sha256']==last and sha(canonical(event))==digest
        last=digest
    assert index==373
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']}
    queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert set(before)==set(after) and len(after)==116 and queue['new_branches']==[] and queue['global_exhaustion_claimed'] is False
    assert queue['advanced_existing_branches']==ADVANCED and queue['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in after.items():
        old=before[bid];assert b['prior_delta_evidence']==old.get('prior_delta_evidence',[])+old['new_evidence']
        if bid not in ADVANCED:
            assert b['latest_scoped_result']==old['latest_scoped_result'] and b['continuation_condition']==old['continuation_condition']
            assert b['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in b['new_evidence']:assert (ROOT/path).exists()
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'LOCAL_NOISE_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Retained transcript, source and history checks. Recorded analytic and local-model audits are linked by hashes; their numerical bases are not rerun.',
        'preceding_checkpoint_integrity':'passed','manifest_files':len(manifest['files']),
        'wide_range_exclusions':range_exclusions,'strict_phase_brackets':phase_count,'independent_extrema_sums':12,
        'local_candidate_exclusions':local_counts,'spectral_feedback_exclusions':spectral_counts,
        'minimal_observation_certificates':minima,'local_case_replays':176,'quadratic_seed_degree_only_unique_targets':91,
        'radius_001_galois_discriminant_unique_targets':91,'original_unresolved_local_factors':48,
        'recorded_commands':9,'failed_commands':1,'deliberately_interrupted_commands':1,'research_branches':116,'ledger_events':373,
        'preserved_event_prefix':369,'ledger_head_sha256':last,'local_links':links},indent=2))

if __name__=='__main__':main()
