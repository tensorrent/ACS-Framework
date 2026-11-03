"""Re-evaluate a recorded zero certificate at higher precision.

This checker independently checks the rational contour partition, recomputes
every interval image, sums its phase increments, and checks every root bracket.
It shares FLINT/Arb with the producer; it is not an independent interval kernel.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time
from flint import acb, arb, ctx, dirichlet_char


def replay(path):
    data = json.loads(path.read_text())
    ctx.prec = 224
    spec = data['character_check']
    chi = dirichlet_char(spec['modulus'], spec['conrey_number'])
    assert chi.is_primitive() and not chi.is_principal()
    assert int(chi.parity()) == 1
    top = F(data['top'])
    corners = [(F(-1, 4), F(-1, 2)), (F(5, 4), F(-1, 2)),
               (F(5, 4), top), (F(-1, 4), top)]
    assert data['contour']['corners'] == [list(map(str, p)) for p in corners]
    start = time.monotonic()
    last = corners[0]
    edge_lengths = [F(0)] * 4
    angle_sum = arb(0)
    cache, leaves = {}, []

    def encode(x):
        return {'mid': [str(x.mid().man_exp()[0]), int(x.mid().man_exp()[1])],
                'rad': [str(x.rad().man_exp()[0]), int(x.rad().man_exp()[1])]}

    def L(p):
        if p not in cache:
            cache[p] = chi.l(acb(arb(str(p[0])), arb(str(p[1]))))
        return cache[p]

    def increment(a, b, depth=0):
        # More working precision can change the L-evaluation algorithm and
        # increase dependency overestimation for wide input balls. Subdivide
        # the same geometrical segment; never substitute endpoint-only checks.
        re = arb(str((a[0] + b[0]) / 2), str(abs(a[0] - b[0]) / 2))
        im = arb(str((a[1] + b[1]) / 2), str(abs(a[1] - b[1]) / 2))
        image = chi.l(acb(re, im))
        if not image.contains(0):
            ratio = L(b) / L(a)
            if ratio.real > 0:
                angle = ratio.arg()
                leaves.append({'a': list(map(str, a)), 'b': list(map(str, b)),
                               'image_real': encode(image.real), 'image_imag': encode(image.imag),
                               'ratio_real': encode(ratio.real), 'angle': encode(angle)})
                return angle
        assert depth < 12, ('Refinement failed', a, b)
        m = tuple((x + y) / 2 for x, y in zip(a, b))
        return increment(a, m, depth + 1) + increment(m, b, depth + 1)

    for segment in data['contour']['segments']:
        a, b = tuple(map(F, segment['a'])), tuple(map(F, segment['b']))
        assert a == last and a != b, 'Contour gap or zero-length segment'
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
            raise AssertionError('Segment is not on the oriented rectangle boundary')
        edge_lengths[edge] += length
        angle_sum += increment(a, b)
        last = b
    assert last == corners[0]
    assert edge_lengths == [F(3, 2), top + F(1, 2), F(3, 2), top + F(1, 2)]
    winding = angle_sum / (2 * arb.pi())
    count = winding.unique_fmpz()
    assert count is not None and int(count) == data['contour']['zero_count']
    assert int(count) == len(data['root_intervals'])
    last_hi = F(0)
    for root in data['root_intervals']:
        lo, hi, d, r = map(F, [root['lo'], root['hi'], root['rounded'], root['rounding_cell_radius']])
        assert last_hi < lo < hi < top
        assert r == F(1, 2 * 10**20) and d - r < lo < hi < d + r
        left, right = chi.hardy_z(arb(str(lo))), chi.hardy_z(arb(str(hi)))
        assert left.imag.contains(0) and right.imag.contains(0)
        assert (left.real > 0 and right.real < 0) or (left.real < 0 and right.real > 0)
        last_hi = hi
    return {'status': 'passed', 'character': data['character'], 'precision_bits': ctx.prec,
            'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'original_segments_recomputed': len(data['contour']['segments']),
            'segments_recomputed': len(leaves), 'segments': leaves,
            'root_intervals_recomputed': int(count), 'winding_ball': winding.str(75),
            'seconds': time.monotonic() - start}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = replay(args.certificate)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'segments'}, indent=2))
