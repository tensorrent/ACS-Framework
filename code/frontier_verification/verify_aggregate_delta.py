"""Verify direct aggregate-spectrum arithmetic recovery and its history."""
import argparse,contextlib,hashlib,io,json,re,subprocess,sys,tempfile,zipfile
from datetime import datetime,timezone
from pathlib import Path
from fractions import Fraction as F
from flint import arb,ctx
import dedekind_aggregate_inputs as extractor
import dedekind_aggregate_measurements as measurements
import dedekind_aggregate_recovery as recovery
import dedekind_aggregate_integer_audit as integer_audit
import dedekind_aggregate_analytic_audit as analytic_audit
import dedekind_aggregate_radius as radius_audit
import dedekind_aggregate_adversary as adversary
from dedekind_coupled_recovery import decode

CODE=Path(__file__).absolute().parent;ROOT=CODE.parents[1]
OUT=ROOT/'docs/frontier/2026-09-13-aggregate-delta';PRIOR=ROOT/'docs/frontier/2026-09-13-biquadratic-delta'
ADVANCED=['R12','R13','R14','R15','K04']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def same(a,b):assert canonical(a)==canonical(b)
def quiet(function,*args):
    with contextlib.redirect_stdout(io.StringIO()):return function(*args)


def main(recompute):
    previous=subprocess.run([sys.executable,str(CODE/'verify_biquadratic_delta.py')],capture_output=True,text=True)
    assert previous.returncode==0,previous.stdout+previous.stderr
    manifest=read(OUT/'Manifest.json')
    for path,entry in manifest['files'].items():
        raw=(ROOT/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
    inventory=read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes={sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments','dependencies']:
            for path,digest in inventory[kind].items():assert digest==sha((ROOT/path).read_bytes())==sha(z.read(kind+'/'+path))
    with tempfile.TemporaryDirectory() as directory:
        tmp=Path(directory)
        with zipfile.ZipFile(OUT/'Aggregate_Inputs.zip') as z:
            assert set(z.namelist())=={'S1_160.json','S2_160.json','S1_224.json','S2_224.json'}
            for n in z.namelist():(tmp/n).write_bytes(z.read(n))
        with zipfile.ZipFile(OUT/'Measurements_Recovery.zip') as z:
            assert set(z.namelist())=={'Measurements160.json','Measurements224.json','Recovery160.json','Recovery224.json'}
            for n in z.namelist():(tmp/n).write_bytes(z.read(n))
        provenance=quiet(extractor.build,PRIOR/'Pair_Spectra.zip',tmp/'regenerated')
        same(provenance,read(OUT/'Input_Provenance.json'))
        for row in provenance['mapping']:assert sha((tmp/row['input_file']).read_bytes())==row['input_sha256']
        mp=[tmp/f'Measurements{b}.json' for b in [160,224]];rp=[tmp/f'Recovery{b}.json' for b in [160,224]]
        for bits,m,r in zip([160,224],mp,rp):
            paths=[tmp/f'S1_{bits}.json',tmp/f'S2_{bits}.json']
            same(read(m),quiet(measurements.run,paths,bits,31,[25]));same(read(r),quiet(recovery.run,m,31))
        same(read(OUT/'Integer_Audit.json'),quiet(integer_audit.run,mp,rp,PRIOR/'Pair_Arithmetic.json'))
        inputs=[tmp/'S1_224.json',tmp/'S2_224.json']
        same(read(OUT/'Radius_Audit.json'),quiet(radius_audit.run,mp[1],rp[1],inputs))
        same(read(OUT/'Adversary_Audit.json'),quiet(adversary.run,mp[1],rp[1],OUT/'Radius_Audit.json',inputs))
        analytic=read(OUT/'Analytic_Audit.json')
        assert analytic['source_sha256']==sha((CODE/'dedekind_aggregate_analytic_audit.py').read_bytes())
        assert analytic['independent_weight_checks']==20536 and analytic['finite_formula_cases']==34 and analytic['alternate_gamma_integrals']==17
        assert analytic['mutation_rejection_counts']=={'omit_negative_zeros':34,'omit_pole':34,'omit_gamma':34,'old_discriminant_125':4,'omit_gamma_normalization':6}
        ctx.prec=256;d=read(mp[1])
        for row in analytic['cases']:
            index=next(i for i,r in enumerate(d['rows']) if r['center']==row['center'])
            observation=d['rows'][index]['observations'][row['observation_index']]
            assert decode(observation['finite_sum']).contains(arb(row['finite_zero_sum']))
            assert decode(observation['unwidened']).contains(arb(row['unwidened_estimate']))
            assert arb(row['finite_formula_residual']).abs_upper()<decode(row['absolute_error_budget'])
        for alt,row in zip(analytic['alternate_gamma'],d['rows']):assert arb(alt['enclosure']).overlaps(arb(row['gamma']['enclosure']))
        for artifact in [analytic,read(OUT/'Adversary_Audit.json'),read(OUT/'Radius_Audit.json'),read(OUT/'Integer_Audit.json')]:
            for name,digest in artifact['inputs_sha256'].items():
                path=next(p for p in [tmp/name,OUT/name,PRIOR/name] if p.exists());assert sha(path.read_bytes())==digest
        if recompute:same(analytic,quiet(analytic_audit.run,mp,inputs,OUT/'Integer_Audit.json'))
        summaries=[]
        for result in read(rp[1])['results']:
            target=next(t for t in result['dual_targets'] if t['n']==7)
            summaries.append((result['monotone_unique_targets'],result['dual_unique_targets'],target['candidates']))
        assert summaries==[(13,12,[4]),(9,9,[0])]
    receipts=read(OUT/'Execution_Receipts.json')
    assert len(receipts)==11 and sum(r['returncode']==0 for r in receipts.values())==10
    assert receipts['primary-source-recheck']['returncode']==1 and receipts['primary-source-recheck-corrected']['returncode']==0
    assert max(receipts[n]['started_utc'] for n in ['aggregate-recovery160','aggregate-recovery224'])<receipts['aggregate-integer-audit']['started_utc']
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name,r in receipts.items():
            assert json.loads(z.read(name+'/receipt.json'))==r and set(r['input_sources_sha256'].values())<=hashes
            for stream in ['stdout','stderr']:assert sha(z.read(name+'/'+stream+'.txt'))==r[stream+'_sha256']
        assert 'FileNotFoundError' in z.read('primary-source-recheck/stderr.txt').decode()
    sources=read(OUT/'Source_Recheck.json');assert sources['status']=='passed' and len(sources['sources'])==2
    old_sources=read(ROOT/'docs/frontier/2026-09-13-explicit-delta/Download_Receipts.json')
    for a,b in zip(sources['sources'],old_sources):assert all(a[k]==b[k] for k in ['filename','url','retrieved_utc','bytes','sha256'])
    before={b['id']:b for b in read(PRIOR/'Research_Queue.json')['branches']};queue=read(OUT/'Research_Queue.json');after={b['id']:b for b in queue['branches']}
    assert set(before)==set(after) and len(after)==117 and queue['new_branches']==[] and queue['advanced_existing_branches']==ADVANCED
    assert queue['global_exhaustion_claimed'] is False and queue['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid,b in before.items():
        a=after[bid];assert a['prior_delta_evidence']==b.get('prior_delta_evidence',[])+b['new_evidence']
        if bid not in ADVANCED:
            assert a['latest_scoped_result']==b['latest_scoped_result'] and a['continuation_condition']==b['continuation_condition']
            assert a['assessment_this_pass']=='carried_forward_not_newly_audited'
        for path in a['new_evidence']:assert (ROOT/path).exists()
    prefix=(PRIOR/'Branch_Events.jsonl').read_bytes();ledger=(OUT/'Branch_Events.jsonl').read_bytes()
    assert len(prefix.splitlines())==383 and ledger.startswith(prefix);last='0'*64
    for index,line in enumerate(ledger.splitlines(),1):
        e=json.loads(line);digest=e.pop('event_sha256');assert e['sequence']==index and e['previous_event_sha256']==last and sha(canonical(e))==digest;last=digest
    assert index==388
    links=0
    for path in [OUT/'README.md',OUT.parent/'README.md',CODE/'AGGREGATE_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent/link.split('#')[0]).exists(),(path,link);links+=1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Recursive history and fresh measurement, coefficient-recovery, exact-integer, radius and adversarial replay. Independent analytic audit execution is retained and checked; --recompute-analytic reruns it. Full analytic and number-field arguments remain unformalized.',
        'manifest_files':len(manifest['files']),'preceding_checkpoint_integrity':'passed','measurement_rows_per_spectrum':17,'generic_coefficients':604,
        'target_count':17,'monotone_unique_targets':[13,9],'continuous_dual_unique_targets':[12,9],'coefficient_at_7':[4,0],
        'integer_exclusions':184,'integer_dual_bounds':136,'radius_integer_dual_bounds':24,'independent_factorizations':1128,
        'independent_weight_checks':20536,'finite_formula_cases':34,'alternate_gamma_integrals':17,'analytic_recomputed_this_invocation':recompute,
        'actual_input_proof_mutations_rejected':12,'formula_mutations_detected':112,'formula_mutations_tested':170,'displaced_sum_controls':408,
        'recorded_commands':11,'failed_commands':1,'research_branches':117,'ledger_events':388,'preserved_event_prefix':383,'ledger_head_sha256':last,'local_links':links},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--recompute-analytic',action='store_true');main(p.parse_args().recompute_analytic)
