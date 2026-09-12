"""Check retained integral-delta evidence and the preceding checkpoint.

Uses only the Python standard library and performs no mathematical reruns.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

CODE = Path(__file__).resolve().parent
ROOT = CODE.parents[1]
OUT = ROOT / 'docs/frontier/2026-09-12-integral-delta'
PRIOR = ROOT / 'docs/frontier/2026-09-12-delta'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    prior_check = subprocess.run([sys.executable, str(CODE/'verify_delta.py')], text=True, capture_output=True)
    assert prior_check.returncode == 0, prior_check.stderr
    assert json.loads(prior_check.stdout)['status'] == 'passed'
    manifest = read(OUT/'Manifest.json')
    for name, expected in manifest['files'].items():
        data = (ROOT/name).read_bytes()
        assert len(data) == expected['bytes'] and sha(data) == expected['sha256'], name
    previous_bytes = (PRIOR/'Branch_Events.jsonl').read_bytes()
    ledger = (OUT/'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(previous_bytes) and len(previous_bytes.splitlines()) == 319
    previous = '0'*64
    for i, line in enumerate(ledger.splitlines(), 1):
        event = json.loads(line)
        digest = event.pop('event_sha256')
        assert event['sequence'] == i and event['previous_event_sha256'] == previous
        assert sha(json.dumps(event, sort_keys=True, separators=(',', ':')).encode()) == digest
        previous = digest
    assert i == 322
    before = {b['id']: b for b in read(PRIOR/'Research_Queue.json')['branches']}
    queue = read(OUT/'Research_Queue.json')
    after = {b['id']: b for b in queue['branches']}
    assert len(after) == len(queue['branches']) == 112 and before.keys() == after.keys()
    assert queue['global_exhaustion_claimed'] is False
    for branch_id, branch in after.items():
        if branch_id not in ['C05', 'R11', 'K04']:
            assert branch['continuation_condition'] == before[branch_id]['continuation_condition']
        for evidence in branch['new_evidence']:
            assert (ROOT/evidence).exists(), evidence
    sources = read(CODE/'proofs/Integral_Source_Manifest.json')
    for name, expected in sources.items():
        assert sha((CODE/'proofs'/name).read_bytes()) == expected['sha256'], name
    audit = read(OUT/'Formal_Audit.json')
    assert audit['all_passed'] and audit['rejected_mutations'] == 7
    assert audit['verified_modules'] == ['PerZero', 'PerZeroIntegral', 'PerZeroError', 'PerZeroSums']
    assert audit['audit_source_sha256'] == sha((CODE/'audit_integral_lean.py').read_bytes())
    locked = {p['name']: p['rev'] for p in read(CODE/'proofs/lake-manifest.json')['packages']}
    assert audit['package_revisions'] == locked and len(locked) == 9
    axioms = next(e for e in audit['events'] if e['name'] == 'axiom_dependencies')['stdout']
    assert 'sorryAx' not in axioms
    theorem_count = 0
    for module in audit['verified_modules']:
        data = (CODE/'proofs'/(module+'.lean')).read_bytes()
        assert sha(data) == audit['source_hashes'][module]
        names = re.findall(r'^theorem\s+(\w+)', data.decode(), re.M)
        assert all(module+'.'+name in axioms for name in names)
        if module != 'PerZero':
            theorem_count += len(names)
    assert theorem_count == 19
    with zipfile.ZipFile(OUT/'Formal_Audit_Artifacts.zip') as z:
        assert z.read('receipt.json') == (OUT/'Formal_Audit.json').read_bytes()
        for event in audit['events']:
            assert event['passed']
            if event['expected_rejection']:
                assert event['returncode'] != 0 and 'error:' in event['stdout']
                assert not any(t in event['stdout'].lower() for t in ['unknown module', 'unknown package', 'file not found'])
                assert sha(z.read('mutations/'+event['name']+'.lean')) == event['input_sha256']
    attempts = read(OUT/'Development_Attempts.json')
    with zipfile.ZipFile(OUT/'Development_Attempts.zip') as z:
        for attempt in attempts['attempts']:
            receipt = json.loads(z.read(attempt['directory']+'/receipt.json'))
            source_name = receipt['command'][-1]
            assert sha(z.read(attempt['directory']+'/'+source_name)) == attempt['source_sha256']
            assert receipt['returncode'] == attempt['returncode']
    cross_receipt = read(OUT/'Cross_Method_Receipt.json')
    cross = read(OUT/'Cross_Method_Checks.json')
    assert cross_receipt['returncode'] == 0 and cross['status'] == 'passed'
    assert cross_receipt['source_sha256'] == sha((CODE/'integral_crosscheck.py').read_bytes())
    assert cross_receipt['stdout_sha256'] == sha((OUT/'Cross_Method_Checks.json').read_bytes())
    assert len(cross['complex_integral_cases']) == 24 and len(cross['configurations']) == 9
    links = 0
    for path in [OUT/'README.md', CODE/'INTEGRAL_README.md', OUT.parent/'README.md']:
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent/link.split('#')[0]).exists(), (path, link)
                links += 1
    print(json.dumps({'status': 'passed', 'verified_utc': datetime.now(timezone.utc).isoformat(),
                      'scope': 'Integrity and retained evidence; no mathematical reruns.',
                      'preceding_checkpoint_integrity': 'passed', 'manifest_files': len(manifest['files']),
                      'ledger_events': i, 'preserved_event_prefix': 319, 'ledger_head_sha256': previous,
                      'research_branches': 112, 'new_lean_theorems': theorem_count,
                      'lean_modules_checked_including_dependency': 4, 'false_mutations_rejected': 7,
                      'complex_quadrature_cases': 24, 'finite_configurations': 9,
                      'development_attempts_retained': len(attempts['attempts']),
                      'failed_development_attempts_retained': attempts['failed'], 'local_links': links}, indent=2))


if __name__ == '__main__':
    main()
