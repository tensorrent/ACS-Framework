"""Verify archived identities, exact transcript consistency and prior checkpoints.

This does not recompute L-functions. Numerical replay commands and receipts are
separate; the retained dyadic transcript is checked without decimal roundtrips.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile
from flint import arb, ctx

CODE = Path(__file__).resolve().parent
ROOT = CODE.parents[1]
OUT = ROOT / 'docs/frontier/2026-09-13-lfunction-delta'
PRIOR = ROOT / 'docs/frontier/2026-09-12-source-delta'
COUNTS = {'chi5': 146, 'chi5bar': 146, 'chi7': 157, 'chi7bar': 158,
          'chi_m35': 65, 'chi_m91': 55, 'chi_m104': 67}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def dyadic(pair):
    return F(int(pair[0])) * F(2) ** int(pair[1])


def bounds(encoded):
    mid, radius = dyadic(encoded['mid']), dyadic(encoded['rad'])
    assert radius >= 0
    return mid - radius, mid + radius


def check_partition(segments, top, values=False):
    ctx.prec = 256
    pi = arb.pi()
    pilo = dyadic(pi.lower().man_exp())
    last = (F(-1, 4), F(-1, 2))
    lengths = [F(0)] * 4
    angle_lo = angle_hi = F(0)
    for row in segments:
        a, b = tuple(map(F, row['a'])), tuple(map(F, row['b']))
        assert a == last and a != b, 'Contour gap'
        assert all(F(-1, 4) <= p[0] <= F(5, 4) and F(-1, 2) <= p[1] <= top for p in [a, b])
        if a[1] == b[1] == F(-1, 2) and a[0] < b[0]:
            edge, length = 0, b[0] - a[0]
        elif a[0] == b[0] == F(5, 4) and a[1] < b[1]:
            edge, length = 1, b[1] - a[1]
        elif a[1] == b[1] == top and a[0] > b[0]:
            edge, length = 2, a[0] - b[0]
        elif a[0] == b[0] == F(-1, 4) and a[1] > b[1]:
            edge, length = 3, a[1] - b[1]
        else:
            raise AssertionError('Wrong contour orientation or boundary')
        lengths[edge] += length
        if values:
            re_lo, re_hi = bounds(row['image_real'])
            im_lo, im_hi = bounds(row['image_imag'])
            assert re_lo > 0 or re_hi < 0 or im_lo > 0 or im_hi < 0, 'Image fails to exclude zero'
            assert bounds(row['ratio_real'])[0] > 0, 'Endpoint quotient is not in the right half-plane'
            lo, hi = bounds(row['angle'])
            assert -pilo / 2 < lo <= hi < pilo / 2
            angle_lo += lo
            angle_hi += hi
        last = b
    assert last == (F(-1, 4), F(-1, 2))
    assert lengths == [F(3, 2), F(top) + F(1, 2), F(3, 2), F(top) + F(1, 2)]
    return angle_lo, angle_hi


def main():
    prior = subprocess.run([sys.executable, str(CODE / 'verify_source_delta.py')], capture_output=True, text=True)
    assert prior.returncode == 0, prior.stdout + prior.stderr
    manifest = read(OUT / 'Manifest.json')
    for name, expected in manifest['files'].items():
        data = (ROOT / name).read_bytes()
        assert len(data) == expected['bytes'] and sha(data) == expected['sha256'], name
    summaries = read(OUT / 'Certificate_Summary.json')['characters']
    assert set(summaries) == set(COUNTS)
    total_segments = total_replay_segments = 0
    with zipfile.ZipFile(OUT / 'Certificates.zip') as certificates, zipfile.ZipFile(OUT / 'Replays.zip') as replays:
        for name, count in COUNTS.items():
            raw = certificates.read(name + '.json')
            cert = json.loads(raw)
            replay_raw = replays.read(name + '.json')
            replay = json.loads(replay_raw)
            summary = summaries[name]
            assert sha(raw) == replay['certificate_sha256'] == summary['certificate_sha256']
            assert sha(replay_raw) == summary['replay_sha256']
            assert cert['status'] == replay['status'] == 'passed'
            assert cert['precision_bits'] == 160 and replay['precision_bits'] == 224
            assert cert['character'] == replay['character'] == name
            assert cert['source_sha256'] == sha((CODE / 'lfunction_zero_certificate.py').read_bytes())
            assert replay['source_sha256'] == sha((CODE / 'lfunction_certificate_replay.py').read_bytes())
            if 'backend_source_sha256' in cert:
                assert cert['backend_source_sha256'] == sha((CODE / 'lfunction_functional_backend.py').read_bytes())
                assert len(cert['direct_functional_controls']) == 4
            if 'backend_source_sha256' in replay:
                assert replay['backend_source_sha256'] == sha((CODE / 'lfunction_functional_backend.py').read_bytes())
                assert len(replay['direct_functional_controls']) == 4
            assert cert['contour']['zero_count'] == len(cert['root_intervals']) == count
            assert replay['root_intervals_recomputed'] == count
            check_partition(cert['contour']['segments'], cert['top'])
            lo, hi = check_partition(replay['segments'], cert['top'], values=True)
            p = arb.pi()
            assert arb(str(lo)) < 2 * count * p < arb(str(hi))
            assert arb(str(lo)) > 2 * (count - 1) * p and arb(str(hi)) < 2 * (count + 1) * p
            last_hi = F(0)
            for root in cert['root_intervals']:
                a, b, d, r = map(F, [root['lo'], root['hi'], root['rounded'], root['rounding_cell_radius']])
                assert last_hi < a < b < cert['top'] and b - a < F(1, 10**25)
                assert r == F(1, 2 * 10**20) and d - r < a < b < d + r
                assert root['lo_sign'] * root['hi_sign'] == -1
                assert arb(root['lo_Z']) * root['lo_sign'] > 0
                assert arb(root['hi_Z']) * root['hi_sign'] > 0
                last_hi = b
            # The deliberately invalid four-corner shortcut gives zero here.
            assert arb(cert['contour']['corner_only_phase_sum']).contains(0)
            total_segments += len(cert['contour']['segments'])
            total_replay_segments += len(replay['segments'])

    audit = read(OUT / 'Data_Audit.json')
    assert audit['status'] == 'passed' and len(audit['tables']) == 8
    assert audit['source_sha256'] == sha((CODE / 'lfunction_data_audit.py').read_bytes())
    with zipfile.ZipFile(OUT / 'Certificates.zip') as certificates:
        for name, expected in audit['certificate_hashes'].items():
            member = 'chi_m91_direct.json' if name == 'chi_m91' else name + '.json'
            assert sha(certificates.read(member)) == expected
        direct = json.loads(certificates.read('chi_m91_direct.json'))
        functional = json.loads(certificates.read('chi_m91.json'))
        assert direct['root_intervals'] == functional['root_intervals']
        assert direct['contour']['zero_count'] == functional['contour']['zero_count'] == 55
    assert len(audit['independent_root_checks']) == 14 and all(r['inside_certified_interval'] for r in audit['independent_root_checks'])
    assert len(audit['conjugation_checks']) == 4
    cells = Counter()
    for table in audit['tables']:
        assert len(table['rows']) == table['original_rows'] and not table['duplicate_nearest_roots']
        cells.update(table['rounding_cell_counts'])
    assert sum(cells.values()) == 654
    assert cells == {'excluded_by_L_ball': 337, 'excluded_by_complete_list': 15, 'certified_root_inside_cell': 302}
    missing = [r for table in audit['tables'] for r in table['missing_roots']]
    assert [r['index'] for r in missing] == [103, 128, 147]
    witness = audit['premature_absolute_tolerance_witness']
    assert F(witness['absolute_L']) > F(1, 10) and F(witness['absolute_completed_L']) < F(1, 10**8)
    observable = read(OUT / 'Observable_Delta.json')
    assert observable['status'] == 'passed' and len(observable['cases']) == 4
    assert observable['source_sha256'] == sha((CODE / 'lfunction_observable_delta.py').read_bytes())
    assert all(len(c['after_R_balls']) == 3 for c in observable['cases'])
    extended7 = next(c for c in observable['cases'] if c['character'] == 'chi7' and c['after_rows'] == 157)
    assert extended7['own_power_exceeds_twice_floor'] == [True, False, True]

    corrections = read(OUT / 'Source_Changes.json')
    with zipfile.ZipFile(OUT / 'Source_Snapshot.zip') as sources:
        for path, item in corrections['files'].items():
            assert sha(sources.read('after/' + path)) == item['after_sha256']
            if item['before_sha256']:
                assert sha(sources.read('before/' + path)) == item['before_sha256']
        for path, expected in corrections['instruments'].items():
            assert sha(sources.read('instruments/' + path)) == expected == sha((ROOT / path).read_bytes())
        data_manifest = json.loads(sources.read('after/code/hp_knife_suite/data_zeros/LFUNCTION_CERTIFICATES.json'))
        assert len(data_manifest['files']) == 10
        for name, item in data_manifest['files'].items():
            raw = sources.read('after/code/hp_knife_suite/data_zeros/' + name)
            assert sha(raw) == item['sha256'] and len(raw.split()) == item['rows']
            assert item['certificate_sha256'] == summaries[item['character']]['certificate_sha256']
            with zipfile.ZipFile(OUT / 'Certificates.zip') as certificates:
                cert = json.loads(certificates.read(item['character'] + '.json'))
            selected = [r for r in cert['root_intervals'] if F(r['hi']) < item['height_cutoff']]
            assert raw == ''.join(r['rounded'] + '\n' for r in selected).encode()
            assert item['root_intervals'] == [{'lo': r['lo'], 'hi': r['hi']} for r in selected]
    receipts = read(OUT / 'Execution_Receipts.json')
    with zipfile.ZipFile(OUT / 'Execution_Artifacts.zip') as runs:
        for name, receipt in receipts.items():
            assert json.loads(runs.read(name + '/receipt.json')) == receipt
            assert sha(runs.read(name + '/stdout.txt')) == receipt['stdout_sha256']
            assert sha(runs.read(name + '/stderr.txt')) == receipt['stderr_sha256']
            expected = 1 if name.startswith('replay-') and not name.startswith(('replay-refined-', 'replay-functional-')) else 0
            if name == 'replay-functional-chi_m91' and receipt['timed_out']:
                expected = 124
            assert receipt['returncode'] == expected, name
        for stage in ['baseline', 'corrected']:
            for script in ['hp_c9_orthogonality', 'hp_phase_test', 'hp_signed_lfunction', 'hp_ladder_character_twist', 'hp_twist_hardened']:
                assert stage + '-' + script in receipts
        assert 'generator-entrypoint' in receipts and 'final-hp_twist_hardened' in receipts
    reproduction = read(OUT / 'Entrypoint_Reproduction.json')
    assert len(reproduction['files']) == 2 and all(x['identical_to_corrected'] for x in reproduction['files'])

    old = (PRIOR / 'Branch_Events.jsonl').read_bytes()
    ledger = (OUT / 'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(old) and len(old.splitlines()) == 335
    previous = '0' * 64
    for i, line in enumerate(ledger.splitlines(), 1):
        event = json.loads(line)
        digest = event.pop('event_sha256')
        assert event['sequence'] == i and event['previous_event_sha256'] == previous
        assert sha(json.dumps(event, sort_keys=True, separators=(',', ':')).encode()) == digest
        previous = digest
    assert i == 341
    before = {b['id']: b for b in read(PRIOR / 'Research_Queue.json')['branches']}
    queue = read(OUT / 'Research_Queue.json')
    after = {b['id']: b for b in queue['branches']}
    assert len(after) == len(queue['branches']) == 115 and set(after) - set(before) == {'R13'}
    assert queue['global_exhaustion_claimed'] is False
    for bid, branch in after.items():
        if bid in before:
            prior_branch = before[bid]
            assert branch['prior_delta_evidence'] == prior_branch.get('prior_delta_evidence', []) + prior_branch['new_evidence']
            if bid not in ['R12', 'P05', 'R07', 'K05', 'K04']:
                assert branch['continuation_condition'] == prior_branch['continuation_condition']
                assert branch['latest_scoped_result'] == prior_branch['latest_scoped_result']
                assert branch['assessment_this_pass'] == 'carried_forward_not_newly_audited'
        for evidence in branch['new_evidence']:
            assert (ROOT / evidence).exists()
    links = 0
    for path in [OUT / 'README.md', OUT.parent / 'README.md', CODE / 'LFUNCTION_README.md',
                 ROOT / 'code/hp_knife_suite/data_zeros/README_LFUNCTION_CERTIFICATES.md']:
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent / link.split('#')[0]).exists(), (path, link)
                links += 1
    print(json.dumps({'status': 'passed', 'verified_utc': datetime.now(timezone.utc).isoformat(),
                      'scope': 'Archived identities and exact transcript consistency; no L-function reevaluation.',
                      'preceding_checkpoint_integrity': 'passed', 'manifest_files': len(manifest['files']),
                      'distinct_certified_zeros': sum(COUNTS.values()), 'characters': 7,
                      'original_contour_segments': total_segments, 'replay_contour_segments': total_replay_segments,
                      'supplied_ordinates_audited': 654, 'outside_displayed_rounding_cells': 352,
                      'missing_mod7_ordinates': 3, 'independent_mpmath_roots': 14,
                      'ledger_events': i, 'preserved_event_prefix': 335, 'research_branches': 115,
                      'ledger_head_sha256': previous, 'local_links': links}, indent=2))


if __name__ == '__main__':
    main()
