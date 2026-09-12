"""Verify retained mean-error evidence and all preceding checkpoint integrity."""
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
OUT = ROOT / 'docs/frontier/2026-09-12-mean-delta'
PRIOR = ROOT / 'docs/frontier/2026-09-12-topology-delta'
MODULES = ['PerZero', 'PerZeroIntegral', 'PerZeroError', 'PerZeroSums', 'PerZeroMean', 'PerZeroCounterfamily']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    earlier = subprocess.run([sys.executable, str(CODE / 'verify_topology_delta.py')],
                             text=True, capture_output=True)
    assert earlier.returncode == 0, earlier.stdout + earlier.stderr
    manifest = read(OUT / 'Manifest.json')
    for name, expected in manifest['files'].items():
        data = (ROOT / name).read_bytes()
        assert len(data) == expected['bytes'] and sha(data) == expected['sha256'], name
    old = (PRIOR / 'Branch_Events.jsonl').read_bytes()
    ledger = (OUT / 'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(old) and len(old.splitlines()) == 326
    previous = '0' * 64
    for i, line in enumerate(ledger.splitlines(), 1):
        event = json.loads(line)
        digest = event.pop('event_sha256')
        assert event['sequence'] == i and event['previous_event_sha256'] == previous
        assert sha(json.dumps(event, sort_keys=True, separators=(',', ':')).encode()) == digest
        previous = digest
    assert i == 329
    before = {b['id']: b for b in read(PRIOR / 'Research_Queue.json')['branches']}
    queue = read(OUT / 'Research_Queue.json')
    after = {b['id']: b for b in queue['branches']}
    assert len(after) == len(queue['branches']) == 113 and set(after) == set(before)
    assert queue['global_exhaustion_claimed'] is False and queue['new_branches'] == []
    for bid, branch in after.items():
        prior = before[bid]
        assert branch['prior_delta_evidence'] == prior.get('prior_delta_evidence', []) + prior['new_evidence']
        if bid not in ['R11', 'C05', 'K04']:
            assert branch['continuation_condition'] == prior['continuation_condition']
            assert branch['latest_scoped_result'] == prior['latest_scoped_result']
            assert branch['assessment_this_pass'] == 'carried_forward_not_newly_audited'
        assert branch.get('related_branches', []) == prior.get('related_branches', [])
        for evidence in branch['new_evidence']:
            assert (ROOT / evidence).exists(), evidence
        assert set(branch.get('related_branches', [])) <= set(after), bid

    sources = read(CODE / 'proofs/Mean_Source_Manifest.json')
    for name, expected in sources.items():
        assert sha((CODE / 'proofs' / name).read_bytes()) == expected['sha256']
    audit = read(OUT / 'Formal_Audit.json')
    assert audit['all_passed'] and audit['rejected_mutations'] == 8
    assert audit['verified_modules'] == MODULES
    assert audit['audit_source_sha256'] == sha((CODE / 'audit_mean_lean.py').read_bytes())
    locked = {p['name']: p['rev'] for p in read(CODE / 'proofs/lake-manifest.json')['packages']}
    assert audit['package_revisions'] == locked and len(locked) == 9
    axioms = next(e for e in audit['events'] if e['name'] == 'axiom_dependencies')['stdout']
    assert 'sorryAx' not in axioms
    new_theorems = 0
    for module in MODULES:
        data = (CODE / 'proofs' / (module + '.lean')).read_bytes()
        assert sha(data) == audit['source_hashes'][module]
        names = re.findall(r'^theorem\s+(\w+)', data.decode(), re.M)
        assert all(module + '.' + name in axioms for name in names)
        if module in ['PerZeroMean', 'PerZeroCounterfamily']:
            new_theorems += len(names)
    assert new_theorems == 23
    with zipfile.ZipFile(OUT / 'Formal_Audit_Artifacts.zip') as z:
        assert z.read('receipt.json') == (OUT / 'Formal_Audit.json').read_bytes()
        assert sum(e['expected_rejection'] for e in audit['events']) == 8
        for event in audit['events']:
            assert event['passed']
            if event['expected_rejection']:
                assert event['returncode'] != 0 and 'error:' in event['stdout']
                assert not any(t in event['stdout'].lower() for t in ['unknown module', 'unknown package', 'file not found'])
                data = z.read('mutations/' + event['name'] + '.lean')
            elif event['name'] == 'axiom_dependencies':
                data = z.read('AuditAxioms.lean')
                assert event['returncode'] == 0
            else:
                data = (CODE / 'proofs' / (event['name'] + '.lean')).read_bytes()
                assert event['returncode'] == 0
            assert sha(data) == event['input_sha256']
    attempts = read(OUT / 'Development_Attempts.json')
    assert attempts['failed'] == sum(a['returncode'] != 0 for a in attempts['attempts']) == 4
    with zipfile.ZipFile(OUT / 'Development_Attempts.zip') as z:
        for attempt in attempts['attempts']:
            assert sha(z.read(attempt['directory'] + '/' + attempt['source_file'])) == attempt['source_sha256']
            receipt = json.loads(z.read(attempt['directory'] + '/receipt.json'))
            assert receipt['returncode'] == attempt['returncode']
            assert receipt['source_sha256'] == attempt['source_sha256']
    cross = read(OUT / 'Cross_Method_Checks.json')
    receipt = read(OUT / 'Cross_Method_Receipt.json')
    assert receipt['returncode'] == 0 and cross['status'] == 'passed'
    assert receipt['source_sha256'] == sha((CODE / 'mean_crosscheck.py').read_bytes())
    assert receipt['shared_quadrature_source_sha256'] == sha((CODE / 'integral_crosscheck.py').read_bytes())
    assert receipt['stdout_sha256'] == sha((OUT / 'Cross_Method_Checks.json').read_bytes())
    assert cross['symbolic']['total_limit'] == 'pi/2' and cross['symbolic']['mean_limit'] == '0'
    assert len(cross['finite_configurations']) == 48 and cross['layer_inequalities_checked'] == 240
    assert len(cross['counterfamily']) == 8 and len(cross['complex_quadrature_cases']) == 6
    assert len(cross['single_cutoff_counterexamples']) == 4
    links = 0
    for path in [OUT / 'README.md', CODE / 'MEAN_README.md', OUT.parent / 'README.md']:
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent / link.split('#')[0]).exists(), (path, link)
                links += 1
    print(json.dumps({'status': 'passed', 'verified_utc': datetime.now(timezone.utc).isoformat(),
                      'scope': 'Retained evidence and integrity; no mathematical reruns.',
                      'preceding_checkpoint_integrity': 'passed', 'manifest_files': len(manifest['files']),
                      'ledger_events': i, 'preserved_event_prefix': 326, 'ledger_head_sha256': previous,
                      'research_branches': 113, 'new_lean_theorems': new_theorems,
                      'false_mutations_rejected': 8, 'finite_configurations': 48, 'layer_inequalities': 240,
                      'complex_quadrature_cases': 6, 'development_attempts_retained': len(attempts['attempts']),
                      'failed_development_attempts_retained': attempts['failed'], 'local_links': links}, indent=2))


if __name__ == '__main__':
    main()
