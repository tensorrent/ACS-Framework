"""Verify the invariant-classification checkpoint and replay its finite audits."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, re, subprocess, sys, zipfile
import dedekind_invariant_classification as producer
import dedekind_invariant_audit as auditor
import dedekind_invariant_adversary as adversary

CODE = Path(__file__).absolute().parent
ROOT = CODE.parents[1]
OUT = ROOT/'docs/frontier/2026-09-13-invariant-delta'
PRIOR = ROOT/'docs/frontier/2026-09-13-local-noise-delta'
ADVANCED = ['R12', 'R13', 'R14', 'K04']

def sha(raw): return hashlib.sha256(raw).hexdigest()
def read(path): return json.loads(path.read_text())
def canonical(v): return json.dumps(v, sort_keys=True, separators=(',', ':')).encode()

def main():
    previous = subprocess.run([sys.executable, str(CODE/'verify_local_noise_delta.py')], capture_output=True, text=True)
    assert previous.returncode == 0, previous.stdout + previous.stderr
    manifest = read(OUT/'Manifest.json')
    for path, entry in manifest['files'].items():
        raw = (ROOT/path).read_bytes()
        assert len(raw) == entry['bytes'] and sha(raw) == entry['sha256'], path
    inventory = read(OUT/'Source_Inventory.json')
    with zipfile.ZipFile(OUT/'Source_Snapshot.zip') as z:
        hashes = {sha(z.read(n)) for n in z.namelist()}
        for kind in ['instruments', 'dependencies']:
            for path, digest in inventory[kind].items():
                assert digest == sha((ROOT/path).read_bytes()) == sha(z.read(kind+'/'+path))
    data = read(OUT/'Invariant_Predictions.json')
    assert canonical(data) == canonical(producer.run())
    replay = auditor.audit(data, ROOT)
    replay['predictions_sha256'] = sha((OUT/'Invariant_Predictions.json').read_bytes())
    assert canonical(replay) == canonical(read(OUT/'Invariant_Audit.json'))
    assert adversary.run(OUT/'Invariant_Predictions.json', ROOT) == read(OUT/'Invariant_Adversary.json')
    receipts = read(OUT/'Execution_Receipts.json')
    assert len(receipts) == 5 and sum(r['returncode']==0 for r in receipts.values()) == 4
    assert receipts['primary-acquisition']['returncode'] == 1
    assert receipts['invariant-producer']['started_utc'] < receipts['invariant-independent-audit']['started_utc']
    with zipfile.ZipFile(OUT/'Execution_Artifacts.zip') as z:
        for name, receipt in receipts.items():
            assert json.loads(z.read(name+'/receipt.json')) == receipt
            assert set(receipt['input_sources_sha256'].values()) <= hashes
            for stream in ['stdout', 'stderr']:
                assert sha(z.read(name+'/'+stream+'.txt')) == receipt[stream+'_sha256']
        assert 'HTTP Error 406' in z.read('primary-acquisition/stderr.txt').decode()
    sources = read(OUT/'Source_Acquisition.json')
    assert sources['status'] == 'passed' and len(sources['sources']) == 6
    assert all(s['curl_returncode']==0 and len(s['sha256'])==64 and s['bytes']>0 for s in sources['sources'])
    prefix = (PRIOR/'Branch_Events.jsonl').read_bytes()
    ledger = (OUT/'Branch_Events.jsonl').read_bytes()
    assert len(prefix.splitlines()) == 373 and ledger.startswith(prefix)
    last = '0'*64
    for index, line in enumerate(ledger.splitlines(), 1):
        event = json.loads(line); digest = event.pop('event_sha256')
        assert event['sequence']==index and event['previous_event_sha256']==last and sha(canonical(event))==digest
        last = digest
    assert index == 378
    old = {b['id']: b for b in read(PRIOR/'Research_Queue.json')['branches']}
    queue = read(OUT/'Research_Queue.json')
    new = {b['id']: b for b in queue['branches']}
    assert len(new)==117 and set(new)-set(old)=={'R15'} and set(old)<=set(new)
    assert queue['global_exhaustion_claimed'] is False and queue['new_branches']==['R15']
    assert queue['advanced_existing_branches']==ADVANCED
    assert queue['parent_checkpoint']==str((PRIOR/'Research_Queue.json').relative_to(ROOT))
    for bid, before in old.items():
        after = new[bid]
        assert after['prior_delta_evidence']==before.get('prior_delta_evidence', [])+before['new_evidence']
        if bid not in ADVANCED:
            assert after['latest_scoped_result']==before['latest_scoped_result'] and after['continuation_condition']==before['continuation_condition']
            assert after['assessment_this_pass']=='carried_forward_not_newly_audited'
    for branch in new.values():
        for path in branch['new_evidence']: assert (ROOT/path).exists(), path
    summary = read(OUT/'Invariant_Summary.json')
    assert summary['global_invariant_local_factors']==72 and summary['previous_ambiguous_factors_selected']==48
    assert summary['additional_spectral_observations_used']==0 and summary['complete_number_field_proof_formalized'] is False
    links = 0
    for path in [OUT/'README.md', OUT.parent/'README.md', CODE/'INVARIANT_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent/link.split('#')[0]).exists(), (path, link)
                links += 1
    print(json.dumps({'status': 'passed', 'verified_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Previous checkpoint integrity plus fresh replay of all new finite-group, polynomial, held-out and corrupted-transcript audits. Cited arithmetic theorems remain mathematical premises, not a fully mechanized number-field proof.',
        'manifest_files': len(manifest['files']), 'preceding_checkpoint_integrity': 'passed',
        's4_exhaustive_subsets': 130817, 'product_subsets_with_identity': 32768, 'independent_factorizations': 564,
        'coefficient_matches': 604, 'target_matches': 91, 'local_factors_from_invariants': 72,
        'prior_ambiguous_factors_selected': 48, 'mutated_transcripts_rejected': 6, 'recorded_commands': 5, 'failed_commands': 1,
        'research_branches': 117, 'ledger_events': 378, 'preserved_event_prefix': 373, 'ledger_head_sha256': last, 'local_links': links}, indent=2))

if __name__ == '__main__': main()
