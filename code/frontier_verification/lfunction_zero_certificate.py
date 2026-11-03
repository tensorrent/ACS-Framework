"""Finite Dirichlet L-zero certificates using interval images and winding numbers.

Requires python-flint 0.9.0 (FLINT 3.6.0) and SymPy 1.14.0. This is an
executable interval certificate, not a Lean proof or a claim of global GRH.
Every accepted contour segment has an entire interval image excluding zero.
See LFUNCTION_README.md for the argument connecting the checks to completeness.
"""
import argparse
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import flint
from flint import acb, arb, ctx, dirichlet_char
from sympy import kronecker_symbol


SPECS = {
    'chi5': (5, 2, 220, None),
    'chi5bar': (5, 3, 220, None),
    'chi7': (7, 3, 220, None),
    'chi7bar': (7, 5, 220, None),
    'chi_m35': (35, 34, 80, -35),
    'chi_m91': (91, 90, 60, -91),
    'chi_m104': (104, 51, 70, -104),
}
BITS = 160
DIGITS = 20


def ball(x):
    return arb(str(x))


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def point(p):
    return acb(ball(p[0]), ball(p[1]))


def segment_box(a, b):
    mid = tuple((x + y) / 2 for x, y in zip(a, b))
    rad = tuple(abs(x - y) / 2 for x, y in zip(a, b))
    return acb(arb(str(mid[0]), str(rad[0])), arb(str(mid[1]), str(rad[1])))


def character_check(name, chi):
    q, number, _, discriminant = SPECS[name]
    assert chi.is_primitive() and not chi.is_principal()
    assert int(chi.conductor()) == q and int(chi.parity()) == 1
    expected_order = 2 if discriminant else q - 1
    assert int(chi.order()) == expected_order
    table = []
    if discriminant:
        for residue in range(q):
            expected = int(kronecker_symbol(discriminant, residue))
            assert chi(residue) == expected, (name, residue)
            table.append({'residue': residue, 'expected_integer': expected,
                          'flint_value': str(chi(residue))})
    else:
        generator = 2 if q == 5 else 3
        direction = -1 if name.endswith('bar') else 1
        logs = {pow(generator, k, q): (direction * k) % (q - 1)
                for k in range(q - 1)}
        assert len(logs) == q - 1 and chi(0) == 0
        for residue in range(1, q):
            assert int(chi.chi_exponent(residue)) == logs[residue]
        table = [{'residue': k, 'expected_root_exponent': logs.get(k),
                  'flint_root_exponent': None if k == 0 else int(chi.chi_exponent(k))}
                 for k in range(q)]
    return {'modulus': q, 'conrey_number': number, 'conductor': q,
            'order': expected_order, 'parity': 1, 'primitive': True,
            'independent_convention': ('Kronecker symbol with discriminant ' + str(discriminant)
                                       if discriminant else 'powers of the specified primitive generator'),
            'all_residues_checked': table}


def hardy(chi, t):
    z = chi.hardy_z(ball(t))
    assert z.imag.contains(0), z
    return z.real


def decimal_midpoint(lo, hi):
    mid = (lo + hi) / 2
    with localcontext() as dc:
        dc.prec = 100
        d = Decimal(mid.numerator) / Decimal(mid.denominator)
        return format(d.quantize(Decimal(1).scaleb(-DIGITS)), 'f')


def refine(chi, lo, hi):
    vlo, vhi = hardy(chi, lo), hardy(chi, hi)
    slo, shi = sign(vlo), sign(vhi)
    assert slo * shi == -1
    while True:
        rounded = decimal_midpoint(lo, hi)
        center, radius = F(rounded), F(1, 2 * 10**DIGITS)
        if hi - lo < F(1, 10**25) and center - radius < lo < hi < center + radius:
            return {'lo': str(lo), 'hi': str(hi), 'lo_Z': vlo.str(55),
                    'hi_Z': vhi.str(55), 'lo_sign': slo, 'hi_sign': shi,
                    'rounded': rounded, 'rounding_cell_radius': str(radius)}
        mid = (lo + hi) / 2
        vmid = hardy(chi, mid)
        smid = sign(vmid)
        if not smid:
            # An exact zero at a midpoint need not have a decidable strict sign.
            # Probe either quarter point while preserving the enclosing bracket.
            mid = (3 * lo + hi) / 4
            vmid = hardy(chi, mid)
            smid = sign(vmid)
            if not smid:
                mid = (lo + 3 * hi) / 4
                vmid = hardy(chi, mid)
                smid = sign(vmid)
            assert smid, 'Increase precision: no quarter point has a definite sign'
        if smid == slo:
            lo, vlo = mid, vmid
        else:
            hi, vhi = mid, vmid


def contour_count(chi, top):
    corners = [(F(-1, 4), F(-1, 2)), (F(5, 4), F(-1, 2)),
               (F(5, 4), F(top)), (F(-1, 4), F(top))]
    cache, accepted = {}, []
    start = time.monotonic()

    def value(p):
        if p not in cache:
            cache[p] = chi.l(point(p))
        return cache[p]

    def segment(a, b, depth=0):
        image = chi.l(segment_box(a, b))
        if not image.contains(0):
            ratio = value(b) / value(a)
            if ratio.real > 0:
                angle = ratio.arg()
                accepted.append({'a': list(map(str, a)), 'b': list(map(str, b)),
                                 'image': image.str(55), 'ratio': ratio.str(55),
                                 'angle': angle.str(55), 'depth': depth})
                return angle
        assert depth < 26, ('Unable to exclude a contour zero', a, b, image)
        mid = tuple((x + y) / 2 for x, y in zip(a, b))
        return segment(a, mid, depth + 1) + segment(mid, b, depth + 1)

    total = arb(0)
    for i in range(4):
        total += segment(corners[i], corners[(i + 1) % 4])
        print(json.dumps({'event': 'contour_edge', 'edge': i,
                          'segments': len(accepted), 'seconds': time.monotonic() - start}), flush=True)
    winding = total / (2 * arb.pi())
    integer = winding.unique_fmpz()
    assert integer is not None and integer >= 0
    # Deliberately invalid shortcut retained as an adversarial comparison.
    corner_only = sum((value(corners[(i + 1) % 4]) / value(corners[i])).arg()
                      for i in range(4)) / (2 * arb.pi())
    return {'orientation': 'counterclockwise', 'corners': [list(map(str, p)) for p in corners],
            'segments': accepted, 'winding_ball': winding.str(55), 'zero_count': int(integer),
            'corner_only_phase_sum': corner_only.str(55),
            'corner_only_is_not_a_certificate': True, 'seconds': time.monotonic() - start}


def certify(name, output):
    ctx.prec = BITS
    q, number, top, _ = SPECS[name]
    chi = dirichlet_char(q, number)
    convention = character_check(name, chi)
    brackets, lo = [], F(0)
    slo = sign(hardy(chi, lo))
    assert slo
    for j in range(1, 10 * top + 1):
        hi = F(j, 10)
        shi = sign(hardy(chi, hi))
        assert shi, ('Scan endpoint needs special handling', hi)
        if shi != slo:
            brackets.append((lo, hi))
        lo, slo = hi, shi
    print(json.dumps({'event': 'scan', 'character': name, 'brackets': len(brackets)}), flush=True)
    roots = [refine(chi, lo, hi) for lo, hi in brackets]
    assert all(F(a['hi']) < F(b['lo']) for a, b in zip(roots, roots[1:]))
    print(json.dumps({'event': 'refined', 'character': name, 'roots': len(roots)}), flush=True)
    contour = contour_count(chi, top)
    assert contour['zero_count'] == len(roots), 'Scan is incomplete or count includes other zeros'
    result = {'status': 'passed', 'character': name, 'top': top,
              'recorded_utc': datetime.now(timezone.utc).isoformat(),
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'precision_bits': BITS, 'python_flint': flint.__version__,
              'flint': flint.__FLINT_VERSION__, 'character_check': convention,
              'scan_step': '1/10', 'rounding_decimal_places': DIGITS,
              'root_intervals': roots, 'contour': contour,
              'scope': 'Exactly these simple zeros in the declared finite rectangle; no global GRH claim.'}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'event': 'certificate', 'character': name, 'zeros': len(roots),
                      'path': str(output), 'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--character', choices=SPECS, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    certify(args.character, args.output)
