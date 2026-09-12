"""Verify the checkpoint's retained hashes, receipts, ledger and branch coverage.

This is an integrity/receipt check, not a new execution of the mathematics.
Run from any directory with Python 3.12; only the standard library is used.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DELTA = ROOT / 'docs/frontier/2026-09-12-delta'
BASE = ROOT / 'docs/frontier/2026-09-11'
PROOFS = Path(__file__).parent / 'proofs'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    manifest = read(DELTA / 'Delta_Manifest.json')
    for name, expected in manifest['files'].items():
        data = (ROOT / name).read_bytes()
        assert len(data) == expected['bytes'] and sha(data) == expected['sha256'], name

    prior = (BASE / 'Branch_Events.jsonl').read_bytes()
    ledger = (DELTA / 'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(prior) and len(prior.splitlines()) == 315
    previous = '0' * 64
    for i, line in enumerate(ledger.splitlines(), 1):
        row = json.loads(line)
        digest = row.pop('event_sha256')
        assert row['sequence'] == i and row['previous_event_sha256'] == previous
        assert sha(json.dumps(row, sort_keys=True, separators=(',', ':')).encode()) == digest
        previous = digest
    assert i == 319

    queue = read(DELTA / 'Research_Queue.json')
    branches = {b['id']: b for b in queue['branches']}
    baseline = {b['id'] for b in read(BASE / 'Branch_Catalog.json')}
    assert len(branches) == len(queue['branches']) == 112
    assert set(branches) - baseline == {'C06', 'R11'} and baseline <= set(branches)
    assert queue['global_exhaustion_claimed'] is False
    for branch in branches.values():
        assert branch['continuation_condition'] and branch['verification_routes']
        for evidence in branch['new_evidence']:
            assert (ROOT / evidence).exists(), evidence
    tasks = read(BASE / 'Task_Checklist.json')['tasks']
    assert len(tasks) == 50
    for task in tasks:
        branch = branches[task['branch_id']]
        if branch['assessment_this_pass'] == 'carried_forward_not_newly_audited':
            assert branch['continuation_condition'] == task['continuation_condition']

    replay = read(DELTA / 'Replay_Receipt.json')
    assert replay['all_passed'] and len(replay['commands']) == 18
    assert len(replay['chosen_streams']) == 7
    assert all(c['returncode'] == 0 and c['status'] == 'passed' for c in replay['commands'])
    fresh = read(DELTA / 'Fresh_Replay_Delta_Manifest.json')
    assert sha((BASE / 'ACS_Frontier_Evidence.zip').read_bytes()) == fresh['base_evidence_archive_sha256']
    with zipfile.ZipFile(DELTA / 'Fresh_Replay_Delta.zip') as z:
        assert len(z.namelist()) == len(fresh['files']) == 332
        assert set(z.namelist()) == set(fresh['files'])
        for name, expected in fresh['files'].items():
            data = z.read(name)
            assert len(data) == expected['bytes'] and sha(data) == expected['sha256'], name

    source_manifest = read(PROOFS / 'Source_Manifest.json')
    for name, expected in source_manifest.items():
        assert sha((PROOFS / name).read_bytes()) == expected['sha256'], name
    with zipfile.ZipFile(BASE / 'ACS_Frontier_Evidence.zip') as z:
        prefix = 'acs-parallel-frontier-20260911/workstreams/foundations/support/source/code/constraint_projection/lean/'
        for name in ['LFBound.lean', 'AxiomIII.lean', 'PerZero.lean']:
            source = prefix + ('withMathlib/' if name == 'PerZero.lean' else '') + name
            assert z.read(source) == (PROOFS / name).read_bytes(), name

    with zipfile.ZipFile(DELTA / 'Lean_Audit_Artifacts.zip') as z:
        for version, directory, modules, mutations in [
            ('434', 'final-lean-audit-v434-attempt2', 5, 11),
            ('415', 'final-lean-audit-v415', 2, 4)
        ]:
            receipt = read(DELTA / f'Lean_Audit_v{version}.json')
            assert receipt['all_passed'] and len(receipt['verified_modules']) == modules
            assert receipt['rejected_mutations'] == mutations
            assert all(e['passed'] for e in receipt['events'])
            assert z.read(directory + '/receipt.json') == (DELTA / f'Lean_Audit_v{version}.json').read_bytes()
            for module, digest in receipt['source_hashes'].items():
                assert digest == source_manifest[module + '.lean']['sha256']
            axioms = next(e for e in receipt['events'] if e['name'] == 'axiom_dependencies')
            assert 'sorryAx' not in axioms['stdout']
            for event in receipt['events']:
                if event['expected_rejection']:
                    data = z.read(directory + '/mutations/' + event['name'] + '.lean')
                    assert sha(data) == event['input_sha256']
                    assert event['returncode'] != 0 and 'error:' in event['stdout']
                    assert not any(t in event['stdout'].lower() for t in ['unknown module', 'unknown package', 'file not found'])
            if version == '434':
                locked = {p['name']: p['rev'] for p in read(PROOFS / 'lake-manifest.json')['packages']}
                assert receipt['package_revisions'] == locked and len(locked) == 9

    for event in read(DELTA / 'python_delta_receipt.json'):
        assert event['returncode'] == 0
        assert sha((Path(__file__).parent / (event['name'] + '.py')).read_bytes()) == event['source_sha256']
        assert read(DELTA / (event['name'] + '.json'))['status'] == 'passed'

    links_checked = 0
    for path in [DELTA / 'README.md', DELTA / 'DERIVATIONS.md', DELTA.parent / 'README.md', Path(__file__).parent / 'README.md']:
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in link or link.startswith('#'):
                continue
            assert (path.parent / link.split('#')[0]).exists(), (path, link)
            links_checked += 1
    print(json.dumps({
        'status': 'passed', 'verified_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Integrity and retained receipts; mathematical commands were not rerun by this verifier.',
        'manifest_files': len(manifest['files']), 'retained_branch_prefix_events': 315,
        'ledger_events': i, 'ledger_head_sha256': previous, 'branches': 112,
        'registered_replay_commands_passed': 18, 'replay_streams': 7,
        'lean_modules_passed': 5, 'distinct_lean_mutations_rejected': 11,
        'older_runtime_standalone_modules_passed': 2, 'older_runtime_mutations_rejected': 4,
        'original_lean_sources_byte_identical': 3, 'locked_dependency_revisions': 9,
        'new_python_audits_passed': 2, 'replay_delta_files': 332,
        'local_links_checked': links_checked
    }, indent=2))


if __name__ == '__main__':
    main()
