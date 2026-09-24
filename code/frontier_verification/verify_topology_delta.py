"""Verify retained topology-correction evidence and preceding checkpoint integrity."""
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
OUT = ROOT/'docs/frontier/2026-09-12-topology-delta'
PRIOR = ROOT/'docs/frontier/2026-09-12-integral-delta'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    prior_check = subprocess.run([sys.executable, str(CODE/'verify_integral_delta.py')], text=True, capture_output=True)
    assert prior_check.returncode == 0, prior_check.stderr
    manifest = read(OUT/'Manifest.json')
    for name, expected in manifest['files'].items():
        data = (ROOT/name).read_bytes()
        assert len(data) == expected['bytes'] and sha(data) == expected['sha256'], name
    old = (PRIOR/'Branch_Events.jsonl').read_bytes()
    ledger = (OUT/'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(old) and len(old.splitlines()) == 322
    previous = '0'*64
    for i, line in enumerate(ledger.splitlines(), 1):
        event = json.loads(line); digest = event.pop('event_sha256')
        assert event['sequence'] == i and event['previous_event_sha256'] == previous
        assert sha(json.dumps(event, sort_keys=True, separators=(',', ':')).encode()) == digest
        previous = digest
    assert i == 326
    before = {b['id']: b for b in read(PRIOR/'Research_Queue.json')['branches']}
    queue = read(OUT/'Research_Queue.json'); after = {b['id']: b for b in queue['branches']}
    assert len(after) == len(queue['branches']) == 113 and set(after)-set(before) == {'C07'}
    assert set(before) <= set(after) and queue['global_exhaustion_claimed'] is False
    for bid, branch in after.items():
        if bid not in ['C04', 'C05', 'K04', 'C07']:
            assert branch['continuation_condition'] == before[bid]['continuation_condition']
        for evidence in branch['new_evidence']:
            assert (ROOT/evidence).exists(), evidence
        assert set(branch.get('related_branches', [])) <= set(after), bid
    corrections = read(OUT/'Scope_Corrections.json')
    for correction in corrections['metadata_corrections']:
        assert before[correction['branch']][correction['field']] == correction['before']
        assert after[correction['branch']][correction['field']] == correction['after']
    for source in corrections['sources']:
        if 'archive' in source:
            with zipfile.ZipFile(ROOT/source['archive']) as z: data = z.read(source['member'])
        else:
            data = (ROOT/source['path']).read_bytes()
        assert sha(data) == source['sha256']
    sources = read(CODE/'proofs/Topology_Source_Manifest.json')
    for name, expected in sources.items():
        assert sha((CODE/'proofs'/name).read_bytes()) == expected['sha256']
    audit = read(OUT/'Formal_Audit.json')
    assert audit['all_passed'] and audit['rejected_mutations'] == 6
    assert audit['verified_modules'] == ['AxiomIII', 'KleinLiftAudit']
    assert audit['audit_source_sha256'] == sha((CODE/'audit_topology_lean.py').read_bytes())
    locked = {p['name']:p['rev'] for p in read(CODE/'proofs/lake-manifest.json')['packages']}
    assert audit['package_revisions'] == locked and len(locked) == 9
    axioms = next(e for e in audit['events'] if e['name'] == 'axiom_dependencies')['stdout']
    assert 'sorryAx' not in axioms
    for module in audit['verified_modules']:
        data = (CODE/'proofs'/(module+'.lean')).read_bytes()
        assert sha(data) == audit['source_hashes'][module]
        names = re.findall(r'^theorem\s+(\w+)', data.decode(), re.M)
        assert all(module+'.'+name in axioms for name in names)
        if module == 'KleinLiftAudit': assert len(names) == 21
    with zipfile.ZipFile(OUT/'Formal_Audit_Artifacts.zip') as z:
        assert z.read('receipt.json') == (OUT/'Formal_Audit.json').read_bytes()
        for e in audit['events']:
            assert e['passed']
            if e['expected_rejection']:
                assert e['returncode'] != 0 and 'error:' in e['stdout']
                assert not any(t in e['stdout'].lower() for t in ['unknown module', 'unknown package', 'file not found'])
                assert sha(z.read('mutations/'+e['name']+'.lean')) == e['input_sha256']
    attempts = read(OUT/'Development_Attempts.json')
    with zipfile.ZipFile(OUT/'Development_Attempts.zip') as z:
        for a in attempts['attempts']:
            assert sha(z.read(a['directory']+'/'+a['source_file'])) == a['source_sha256']
            assert json.loads(z.read(a['directory']+'/receipt.json'))['returncode'] == a['returncode']
    cross = read(OUT/'Cross_Method_Checks.json'); receipt = read(OUT/'Cross_Method_Receipt.json')
    assert receipt['returncode'] == 0 and cross['status'] == 'passed'
    assert receipt['source_sha256'] == sha((CODE/'klein_lift_crosscheck.py').read_bytes())
    assert receipt['stdout_sha256'] == sha((OUT/'Cross_Method_Checks.json').read_bytes())
    assert cross['normal_form_pairs'] == 2401 and len(cross['affine_symbolic_parity_cases']) == 4
    assert cross['witness']['cover_homology_matrix'] == [[1,0],[0,1]] and cross['parabolic_obstruction_retained']
    links = 0
    for p in [OUT/'README.md', CODE/'TOPOLOGY_README.md', CODE/'proofs/ERRATA.md', OUT.parent/'README.md']:
        for link in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (p.parent/link.split('#')[0]).exists(), (p, link)
                links += 1
    print(json.dumps({'status':'passed','verified_utc':datetime.now(timezone.utc).isoformat(),
                      'scope':'Retained evidence and integrity; no mathematical reruns.',
                      'preceding_checkpoint_integrity':'passed','manifest_files':len(manifest['files']),
                      'ledger_events':i,'preserved_event_prefix':322,'ledger_head_sha256':previous,
                      'research_branches':113,'new_branch':'C07','new_lean_theorems':21,
                      'false_mutations_rejected':6,'symbolic_parity_cases':4,'normal_form_pairs':2401,
                      'development_attempts_retained':len(attempts['attempts']),
                      'failed_development_attempts_retained':attempts['failed'],'local_links':links},indent=2))


if __name__ == '__main__':
    main()
