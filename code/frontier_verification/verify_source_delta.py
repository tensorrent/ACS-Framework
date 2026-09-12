"""Check retained source/data evidence and preceding immutable checkpoints.

Implementation files are checked in archived before/after snapshots so future
canonical fixes can proceed without rewriting this historical evidence.
"""
from datetime import datetime, timezone
from decimal import Decimal
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

CODE = Path(__file__).resolve().parent
ROOT = CODE.parents[1]
OUT = ROOT / 'docs/frontier/2026-09-12-source-delta'
PRIOR = ROOT / 'docs/frontier/2026-09-12-mean-delta'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    previous_check = subprocess.run([sys.executable, str(CODE / 'verify_mean_delta.py')],
                                    text=True, capture_output=True)
    assert previous_check.returncode == 0, previous_check.stdout + previous_check.stderr
    manifest = read(OUT / 'Manifest.json')
    for name, expected in manifest['files'].items():
        data = (ROOT / name).read_bytes()
        assert len(data) == expected['bytes'] and sha(data) == expected['sha256'], name
    inventory = read(OUT / 'Baseline_Inventory.json')
    assert len(inventory['files']) == 325
    assert sum(row['path'].endswith('.py') for row in inventory['files']) == 195
    rows = {row['path']: row for row in inventory['files']}
    corrected = read(OUT / 'Corrected_Sources.json')['files']
    assert len(corrected) == 5
    with zipfile.ZipFile(OUT / 'Source_Snapshot.zip') as sources:
        for row in inventory['files']:
            data = sources.read('baseline/' + row['path'])
            assert sha(data) == row['sha256'] and len(data) == row['bytes'], row['path']
        for name, expected in corrected.items():
            assert sha(sources.read('baseline/' + name)) == expected['before_sha256']
            assert sha(sources.read('corrected/' + name)) == expected['after_sha256']
        for name in ['dataset_precision_audit.py', 'normalization_crosscheck.py', 'source_requirements.txt']:
            assert sources.read('instruments/code/frontier_verification/' + name) == (CODE / name).read_bytes()
        repo_table = sources.read('baseline/code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt')
    identity = read(OUT / 'Source_Identity.json')
    primary = read(OUT / 'Primary_Receipt.json')
    with zipfile.ZipFile(OUT / 'Primary_Tables.zip') as tables:
        assert tables.read('receipt.json') == (OUT / 'Primary_Receipt.json').read_bytes()
        for event in primary['events']:
            data = tables.read(event['path'])
            assert sha(data) == event['sha256'] and len(data) == event['bytes']
        small = tables.read('zeros1')
        extended = gzip.decompress(tables.read('zeros6.gz'))
        assert sha(extended) == primary['decompressed']['sha256'] == identity['larger_table_sha256']
        assert len(extended) == primary['decompressed']['bytes']
        assert small == repo_table + b'\n'
        assert sha(repo_table) == identity['repository_sha256']
        assert small.split() == extended.split()[:100000]
        assert len(small.split()) == 100000 and len(extended.split()) == 2001052
    mapping = read(OUT / 'Source_Map.json')
    assert mapping['baseline_commit'] == inventory['commit']
    tracked_bytes = (OUT / 'Baseline_Tracked_Paths.txt').read_bytes()
    assert sha(tracked_bytes) == mapping['tracked_paths_sha256']
    tracked = set(tracked_bytes.decode().splitlines())
    assert set(rows) <= tracked
    assert len(mapping['areas']) == 8 and len(mapping['missing_training_inputs']) == 7
    for area in mapping['areas']:
        for source in area['sources']:
            assert source['baseline_sha256'] == rows[source['path']]['sha256']
    # Missing-input findings refer to the recorded revision, not the current tree.
    for source in mapping['missing_training_inputs']:
        assert source['exists_at_audited_revision'] is False and source['path'] not in tracked
    data_inventory = read(OUT / 'Data_Inventory.json')
    assert len(data_inventory['files']) == 9
    for data in data_inventory['files']:
        assert data['sha256'] == rows[data['path']]['sha256']
        assert data['strictly_increasing'] and data['all_positive_finite']

    receipts = read(OUT / 'Test_Receipts.json')
    with zipfile.ZipFile(OUT / 'Execution_Artifacts.zip') as archive:
        for name, receipt in receipts.items():
            retained = json.loads(archive.read(name + '/receipt.json'))
            assert all(receipt[key] == value for key, value in retained.items())
            assert sha(archive.read(name + '/stdout.txt')) == receipt['stdout_sha256']
            assert sha(archive.read(name + '/stderr.txt')) == receipt['stderr_sha256']
            assert receipt['returncode'] == (1 if name == 'baseline-regression-sensitivity' else 0)
        baseline_log = archive.read('baseline-tests/stdout.txt').decode()
        corrected_log = archive.read('corrected-tests/stdout.txt').decode()
        failure_log = archive.read('baseline-regression-sensitivity/stdout.txt').decode()
        assert '42 passed' in baseline_log and '46 passed' in corrected_log
        assert '2 failed, 2 passed' in failure_log and 'overflow encountered in exp' in failure_log
        assert archive.read('dataset-results-pinned/result.json') == (OUT / 'Dataset_Audit.json').read_bytes()
        assert archive.read('normalization-run/stdout.txt') == (OUT / 'Normalization_Crosscheck.json').read_bytes()
    audit = read(OUT / 'Dataset_Audit.json')
    assert audit['status'] == 'passed' and audit['arb_precision_bits'] == 160
    assert audit['source_sha256'] == sha((CODE / 'dataset_precision_audit.py').read_bytes())
    assert len(audit['selected_zeros']) == 5
    assert len(audit['finite_configurations']) == len(audit['endpoint_precision_cases']) == 12
    assert {case['N'] for case in audit['finite_configurations']} == {50, 1000, 10000, 100000}
    for case in audit['finite_configurations']:
        assert case['certified_zeta_count'] == str(case['N'])
    witness = next(case for case in audit['endpoint_precision_cases']
                   if case['index'] == 3 and case['epsilon'] == '1e-10')
    assert witness['rounded_table_count'] == 3 and witness['certified_zeta_count'] == 2
    assert witness['actual_last_point_is_interior'] is False
    cross = read(OUT / 'Normalization_Crosscheck.json')
    assert cross['status'] == 'passed' and len(cross['cases']) == 5
    assert cross['source_sha256'] == sha((CODE / 'normalization_crosscheck.py').read_bytes())
    assert cross['corrected_source_sha256'] == corrected['code/acs_codebase/src/paper_b/renormalized_stability.py']['after_sha256']
    assert all(Decimal(case['absolute_difference']) < Decimal('3e-13') for case in cross['cases'])
    overflow = read(OUT / 'Overflow_Reproduction.json')
    assert overflow['finite']['710'] is False and overflow['finite']['1000'] is False

    old = (PRIOR / 'Branch_Events.jsonl').read_bytes()
    ledger = (OUT / 'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(old) and len(old.splitlines()) == 329
    previous = '0' * 64
    for i, line in enumerate(ledger.splitlines(), 1):
        event = json.loads(line)
        digest = event.pop('event_sha256')
        assert event['sequence'] == i and event['previous_event_sha256'] == previous
        assert sha(json.dumps(event, sort_keys=True, separators=(',', ':')).encode()) == digest
        previous = digest
    assert i == 335
    before = {b['id']: b for b in read(PRIOR / 'Research_Queue.json')['branches']}
    queue = read(OUT / 'Research_Queue.json')
    after = {b['id']: b for b in queue['branches']}
    assert len(after) == len(queue['branches']) == 114 and set(after) - set(before) == {'R12'}
    assert queue['global_exhaustion_claimed'] is False
    for bid, branch in after.items():
        if bid in before:
            prior = before[bid]
            assert branch['prior_delta_evidence'] == prior.get('prior_delta_evidence', []) + prior['new_evidence']
            if bid not in ['K05', 'R11', 'R04', 'K02', 'K04']:
                assert branch['continuation_condition'] == prior['continuation_condition']
                assert branch['latest_scoped_result'] == prior['latest_scoped_result']
                assert branch['assessment_this_pass'] == 'carried_forward_not_newly_audited'
        assert set(branch.get('related_branches', [])) <= set(after)
        for evidence in branch['new_evidence']:
            assert (ROOT / evidence).exists(), evidence
    for area in mapping['areas']:
        assert set(area['related_branches']) <= set(after)
    links = 0
    for path in [OUT / 'README.md', CODE / 'SOURCE_README.md', OUT.parent / 'README.md']:
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent / link.split('#')[0]).exists(), (path, link)
                links += 1
    print(json.dumps({'status': 'passed', 'verified_utc': datetime.now(timezone.utc).isoformat(),
                      'scope': 'Retained evidence and integrity; mathematical checks are not rerun.',
                      'preceding_checkpoint_integrity': 'passed', 'manifest_files': len(manifest['files']),
                      'baseline_source_files': 325, 'corrected_source_files': 5,
                      'primary_large_table_rows': 2001052, 'finite_interval_configurations': 12,
                      'certified_endpoint_counterexample': True, 'canonical_baseline_tests_passed': 42,
                      'corrected_tests_passed': 46, 'old_code_regressions_failed_as_expected': 2,
                      'ledger_events': i, 'preserved_event_prefix': 329,
                      'research_branches': 114, 'ledger_head_sha256': previous, 'local_links': links}, indent=2))


if __name__ == '__main__':
    main()
