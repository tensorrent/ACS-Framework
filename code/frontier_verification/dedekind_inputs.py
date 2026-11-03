"""Load four certified positive-height factors without guessing missing inputs."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import zipfile

NAMES = ['zeta', 'chi1', 'chi2', 'chi3']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_factors(extra_path, prior_archive):
    container = extra_path.read_bytes()
    if extra_path.suffix.lower() == '.zip':
        with zipfile.ZipFile(extra_path) as archive:
            extra_raw = archive.read('factors-224.json')
    else:
        extra_raw = container
    extra = json.loads(extra_raw)
    assert extra['status'] == 'passed' and extra['top'] == 220
    assert extra['quadratic5']['conrey_number'] == 4
    with zipfile.ZipFile(prior_archive) as archive:
        a_raw, b_raw = archive.read('chi5.json'), archive.read('chi5bar.json')
    a, b = json.loads(a_raw), json.loads(b_raw)
    assert a['status'] == b['status'] == 'passed' and a['top'] == b['top'] == 220
    assert a['character_check']['conrey_number'] == 2 and b['character_check']['conrey_number'] == 3
    factors = {
        'zeta': extra['zeta']['positive_root_intervals'],
        'chi1': a['root_intervals'],
        'chi2': extra['quadratic5']['positive_root_intervals'],
        'chi3': b['root_intervals'],
    }
    all_intervals = []
    for name, rows in factors.items():
        last = F(0)
        for r in rows:
            lo, hi, center = map(F, [r['lo'], r['hi'], r['rounded']])
            radius = F(r['rounding_cell_radius'])
            assert last < lo < hi < 220 and radius == F(1, 2 * 10**20)
            assert center - radius < lo < hi < center + radius
            last = hi
            all_intervals.append((lo, hi, name))
    all_intervals.sort()
    assert all(a[1] < b[0] for a, b in zip(all_intervals, all_intervals[1:]))
    identity = {'extra_certificate_sha256': sha(extra_raw),
                'extra_input_sha256': sha(container),
                'prior_archive_sha256': sha(prior_archive.read_bytes()),
                'chi1_certificate_sha256': sha(a_raw), 'chi3_certificate_sha256': sha(b_raw),
                'loader_sha256': sha(Path(__file__).read_bytes()),
                'counts_at_220': {n: len(rows) for n, rows in factors.items()}}
    return factors, identity


def at_height(factors, top):
    top = F(top)
    assert 0 < top <= 220
    selected = {}
    for name, rows in factors.items():
        assert all(not F(r['lo']) <= top <= F(r['hi']) for r in rows), 'Ambiguous cutoff'
        selected[name] = [r for r in rows if F(r['hi']) < top]
        assert selected[name], 'Normalization requires a nonempty factor'
    return selected
