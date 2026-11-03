"""Check the retained Dedekind checkpoint and its complete preceding history.

This checks archive identities, rational partitions, counts and consistency of
reported computations. It does not reevaluate L-functions or regenerate roots.
"""
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
from verify_lfunction_delta import check_partition

CODE = Path(__file__).resolve().parent
ROOT = CODE.parents[1]
OUT = ROOT / 'docs/frontier/2026-09-13-dedekind-delta'
PRIOR = ROOT / 'docs/frontier/2026-09-13-lfunction-delta'
NAMES = ['zeta', 'chi1', 'chi2', 'chi3']
VARIANTS = ['historical_doubled_means', 'separate_factor_means', 'union_mean']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text())


def root_check(rows, top, signs=False):
    last = F(0)
    for r in rows:
        lo, hi, center, radius = map(F, [r['lo'], r['hi'], r['rounded'], r['rounding_cell_radius']])
        assert last < lo < hi < top and radius == F(1, 2 * 10**20)
        assert center - radius < lo < hi < center + radius
        if signs:
            assert r['lo_sign'] * r['hi_sign'] == -1
            assert arb(r['lo_Z']) * r['lo_sign'] > 0 and arb(r['hi_Z']) * r['hi_sign'] > 0
        last = hi


def main():
    ctx.prec = 256
    previous_check = subprocess.run([sys.executable, str(CODE / 'verify_lfunction_delta.py')], capture_output=True, text=True)
    assert previous_check.returncode == 0, previous_check.stdout + previous_check.stderr
    manifest = read(OUT / 'Manifest.json')
    for path, item in manifest['files'].items():
        raw = (ROOT / path).read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256'], path
    certs = {}
    with zipfile.ZipFile(OUT / 'Factor_Certificates.zip') as z:
        for bits in [160, 224]:
            raw = z.read(f'factors-{bits}.json')
            d = json.loads(raw)
            certs[bits] = d
            assert d['status'] == 'passed' and d['precision_bits'] == bits and d['top'] == 220
            assert d['source_sha256'] == sha((CODE / 'dedekind_factor_certificate.py').read_bytes())
            assert d['core_source_sha256'] == sha((CODE / 'lfunction_zero_certificate.py').read_bytes())
            q = d['quadratic5']
            assert q['character_values'] == [0, 1, -1, -1, 1] and q['parity'] == 0
            assert q['positive_zeros'] == len(q['positive_root_intervals']) == 146
            assert q['contour']['zero_count'] == 147 and q['additional_trivial_zero']['point'] == '0'
            assert sum(F(q['character_values'][a]) * (F(1, 2) - F(a, 5)) for a in range(1, 5)) == 0
            check_partition(q['contour']['segments'], 220)
            angles = sum((arb(s['angle']) for s in q['contour']['segments']), arb(0)) / (2 * arb.pi())
            assert angles.unique_fmpz() == 147 and arb(q['contour']['winding_ball']).unique_fmpz() == 147
            root_check(q['positive_root_intervals'], 220, signs=True)
            assert d['zeta']['positive_zeros'] == len(d['zeta']['positive_root_intervals']) == 90
            assert arb(d['zeta']['count_ball']) == 90
            root_check(d['zeta']['positive_root_intervals'], 220)
            assert len(d['independent_checks']) == 6 and all(x['inside_interval'] for x in d['independent_checks'])
    for factor in ['quadratic5', 'zeta']:
        a = certs[160][factor]['positive_root_intervals']
        b = certs[224][factor]['positive_root_intervals']
        assert [r['rounded'] for r in a] == [r['rounded'] for r in b]
        assert all(max(F(x['lo']), F(y['lo'])) < min(F(x['hi']), F(y['hi'])) for x, y in zip(a, b))

    independent = read(OUT / 'Independent_Root_Audit.json')
    assert independent['status'] == 'passed' and len(independent['quadratic_roots']) == 146
    assert len(independent['primary_zeta_comparisons']) == 90
    for row, root in zip(independent['quadratic_roots'], certs[224]['quadratic5']['positive_root_intervals']):
        assert row['inside_certified_interval'] and F(root['lo']) < F(row['mpmath_ordinate']) < F(root['hi'])
        assert F(row['absolute_L_residual']) < F(1, 10**74)
    with zipfile.ZipFile(ROOT / 'docs/frontier/2026-09-12-source-delta/Primary_Tables.zip') as z:
        high_raw = z.read('zeros2')
    assert sha(high_raw) == independent['primary_zeros2_sha256']
    high = [''.join(b.split()) for b in re.split(r'\n\s*\n', high_raw.decode().strip())]
    for root in certs[224]['zeta']['positive_root_intervals']:
        assert F(root['lo']) < F(high[root['index'] - 1]) < F(root['hi'])

    changes = read(OUT / 'Source_Changes.json')
    with zipfile.ZipFile(OUT / 'Source_Snapshot.zip') as z:
        for path, row in changes['files'].items():
            assert sha(z.read('after/' + path)) == row['after_sha256']
            if row['before_sha256']:
                assert sha(z.read('before/' + path)) == row['before_sha256']
        for path, digest in changes['instruments'].items():
            assert sha(z.read('instruments/' + path)) == digest == sha((ROOT / path).read_bytes())
        tables = json.loads(z.read('after/code/hp_knife_suite/data_zeros/DEDEKIND_FACTORS.json'))
        assert {n: d['rows'] for n, d in tables['factors'].items()} == {'zeta': 90, 'chi1': 146, 'chi2': 146, 'chi3': 146}
        for name, d in tables['factors'].items():
            raw = z.read('factor_tables/' + d['path'])
            assert sha(raw) == d['sha256'] and len(raw.split()) == d['rows']
            assert d['absolute_decimal_error_bound'] == '5e-21'
    for path, digest in changes['dependencies'].items():
        assert sha((ROOT / path).read_bytes()) == digest

    euler = read(OUT / 'Euler_Audit.json')
    assert euler['status'] == 'passed' and len(euler['modular_polynomial_factorizations']) == 168
    assert len(euler['unramified_residue_classes']) == 4
    for row in euler['unramified_residue_classes']:
        r, f, g = row['residue'], row['residue_degree_f'], row['prime_ideal_count_g']
        assert g * f == 4 and pow(r, f, 5) == 1
        assert row['first_16_coefficients_divided_by_log_p'] == [4 if k % f == 0 else 0 for k in range(1, 17)]
        assert row['leading_coefficient_is_g_times_f'] == 4
        units = [1, 2, 3, 4]
        expected = [[int(units[i] == r * units[j] % 5) for j in range(4)] for i in range(4)]
        assert row['permutation_matrix'] == expected
    assert euler['ramified']['first_16_coefficients_divided_by_log_5'] == [1] * 16
    for row in euler['normalization_counterexamples']:
        assert row['counts'] == tables['counts_by_cutoff'][str(row['height'])]
        ns = [row['counts'][n] for n in NAMES]
        assert row['common_union_weight'] == str(F(1, sum(ns)))
        # Independently recompute three nonsplit character combinations as
        # rational real/imaginary pairs, without parsing symbolic strings.
        real2, imag2 = F(1, ns[0]) - F(1, ns[2]), F(1, ns[1]) - F(1, ns[3])
        real4 = F(1, ns[0]) - F(1, ns[1]) + F(1, ns[2]) - F(1, ns[3])
        assert (real2 != 0 or imag2 != 0) and real4 != 0
    assert euler['normalization_counterexamples'][-1]['weighted_first_prime_coefficients']['4'] == '14/3285'

    witness = read(OUT / 'Finite_Witness_Audit.json')
    assert witness['status'] == 'passed' and len(witness['configurations']) == 18
    assert len(witness['primes']) == 34 and len(witness['independent_checks']) == 54
    configs = {}
    for c in witness['configurations']:
        configs[(c['height'], c['window'])] = c
        assert c['counts'] == tables['counts_by_cutoff'][str(c['height'])]
        assert len(c['direct_points']) == 102 and len(c['legacy_grid_points']) == 34
        ns = [c['counts'][n] for n in NAMES]
        for row in c['direct_points']:
            z, a, b, d = [arb(row['factor_sums'][n]) for n in NAMES]
            expected = [(z / ns[0] + 2 * a / ns[1] + b / ns[2]) / 4,
                        (z / ns[0] + a / ns[1] + b / ns[2] + d / ns[3]) / 4,
                        (z + a + b + d) / sum(ns)]
            assert all(x.overlaps(arb(row['variants'][v])) for x, v in zip(expected, VARIANTS))
        cohort = set(witness['primes'][:25])
        rows = [r for r in c['direct_points'] if r['power'] == 1 and r['prime'] in cohort and r['prime'] != 5]
        a = [abs(arb(r['variants']['union_mean'])) for r in rows if r['prime'] % 5 == 1]
        b = [abs(arb(r['variants']['union_mean'])) for r in rows if r['prime'] % 5 != 1]
        ratio = (sum(a, arb(0)) / len(a)) / (sum(b, arb(0)) / len(b))
        assert ratio.overlaps(arb(c['metrics']['first_25_primes']['exact_logp']['union_mean']['split4_to_other_ratio']))
    assert len(configs) == 18
    for row in witness['independent_checks']:
        c = configs[(row['height'], row['window'])]
        point = next(p for p in c['direct_points'] if (p['prime'], p['power']) == (row['prime'], row['power']))
        assert arb(point['variants']['union_mean']).contains(arb(row['mpmath_union_mean']))
    with zipfile.ZipFile(OUT / 'Execution_Artifacts.zip') as z:
        receipts = read(OUT / 'Execution_Receipts.json')
        assert len(receipts) == 9
        for name, r in receipts.items():
            assert json.loads(z.read(name + '/receipt.json')) == r and r['returncode'] == 0
            assert sha(z.read(name + '/stdout.txt')) == r['stdout_sha256']
            assert sha(z.read(name + '/stderr.txt')) == r['stderr_sha256']
        assert z.read('results/Entrypoint_Result.json') == (OUT / 'Finite_Witness_Audit.json').read_bytes()
    for name, file in [('Euler_Audit.json', 'dedekind_euler_audit.py'), ('Finite_Witness_Audit.json', 'dedekind_witness_audit.py'), ('Independent_Root_Audit.json', 'dedekind_independent_roots.py')]:
        assert read(OUT / name)['source_sha256'] == sha((CODE / file).read_bytes())

    ledger = (OUT / 'Branch_Events.jsonl').read_bytes()
    old = (PRIOR / 'Branch_Events.jsonl').read_bytes()
    assert ledger.startswith(old) and len(old.splitlines()) == 341
    previous = '0' * 64
    for i, line in enumerate(ledger.splitlines(), 1):
        event = json.loads(line)
        digest = event.pop('event_sha256')
        assert event['sequence'] == i and event['previous_event_sha256'] == previous
        assert sha(json.dumps(event, sort_keys=True, separators=(',', ':')).encode()) == digest
        previous = digest
    assert i == 346
    before = {b['id']: b for b in read(PRIOR / 'Research_Queue.json')['branches']}
    queue = read(OUT / 'Research_Queue.json')
    after = {b['id']: b for b in queue['branches']}
    assert set(before) == set(after) and len(after) == len(queue['branches']) == 115
    assert queue['global_exhaustion_claimed'] is False and queue['new_branches'] == []
    for bid, b in after.items():
        old_b = before[bid]
        assert b['prior_delta_evidence'] == old_b.get('prior_delta_evidence', []) + old_b['new_evidence']
        if bid not in ['P05', 'R12', 'R13', 'K05', 'K04']:
            assert b['latest_scoped_result'] == old_b['latest_scoped_result']
            assert b['continuation_condition'] == old_b['continuation_condition']
            assert b['assessment_this_pass'] == 'carried_forward_not_newly_audited'
        for evidence in b['new_evidence']:
            assert (ROOT / evidence).exists()
    links = 0
    for p in [OUT / 'README.md', OUT.parent / 'README.md', CODE / 'DEDEKIND_README.md']:
        for link in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (p.parent / link.split('#')[0]).exists(), (p, link)
                links += 1
    print(json.dumps({'status': 'passed', 'verified_utc': datetime.now(timezone.utc).isoformat(),
                      'scope': 'Retained evidence and reported-computation consistency; L-functions are not reevaluated.',
                      'preceding_checkpoint_integrity': 'passed', 'manifest_files': len(manifest['files']),
                      'new_quadratic_roots': 146, 'certified_zeta_subset': 90, 'four_factor_union': 528,
                      'quadratic_contour_count_including_origin': 147, 'independent_quadratic_roots': 146,
                      'primary_zeta_literal_comparisons': 90, 'modular_factorizations': 168,
                      'finite_configurations': 18, 'direct_frequency_points': 1836, 'grid_frequency_points': 612,
                      'independent_finite_values': 54, 'portable_entrypoint_byte_identical': True,
                      'research_branches': 115, 'ledger_events': i, 'preserved_event_prefix': 341,
                      'ledger_head_sha256': previous, 'local_links': links}, indent=2))


if __name__ == '__main__':
    main()
