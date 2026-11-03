"""Certify the missing even quadratic and Riemann factors through height 220.

The even character has an additional trivial zero at s=0 inside the contour.
Its exact Hurwitz value is checked before matching count = positive brackets + 1.
This file reuses the pinned segment/refinement primitives from the prior pass.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import flint
from flint import acb, arb, ctx, dirichlet_char
import mpmath as mp

import lfunction_zero_certificate as core


def dyadic(x):
    m, e = x.man_exp()
    return F(int(m)) * F(2) ** int(e)


def mpf(x):
    x = F(x)
    return mp.mpf(x.numerator) / x.denominator


def certify(bits):
    ctx.prec = bits
    top = 220
    chi = dirichlet_char(5, 4)
    assert chi.is_primitive() and chi.is_real() and not chi.is_principal()
    assert int(chi.conductor()) == 5 and int(chi.parity()) == 0 and int(chi.order()) == 2
    expected = [0, 1, -1, -1, 1]
    assert all(chi(a) == expected[a] for a in range(5))
    # Hurwitz zeta(0,a/5) = 1/2 - a/5, exactly.
    trivial_value = sum(F(expected[a]) * (F(1, 2) - F(a, 5)) for a in range(1, 5))
    assert trivial_value == 0 and chi.l(acb(0)) == 0
    previous = F(0)
    old_sign = core.sign(core.hardy(chi, previous))
    assert old_sign
    brackets = []
    for j in range(1, 10 * top + 1):
        t = F(j, 10)
        sg = core.sign(core.hardy(chi, t))
        assert sg
        if sg != old_sign:
            brackets.append((previous, t))
        previous, old_sign = t, sg
    roots = [core.refine(chi, lo, hi) for lo, hi in brackets]
    assert all(F(a['hi']) < F(b['lo']) for a, b in zip(roots, roots[1:]))
    print(json.dumps({'event': 'quadratic_brackets', 'positive_roots': len(roots), 'precision_bits': bits}), flush=True)
    contour = core.contour_count(chi, top)
    assert contour['zero_count'] == len(roots) + 1
    # At least one zero at 0 plus one in every disjoint positive bracket;
    # equality of total multiplicities proves each is simple and excludes extras.
    qresult = {'modulus': 5, 'conrey_number': 4, 'parity': 0, 'primitive': True,
               'character_values': expected, 'positive_root_intervals': roots, 'contour': contour,
               'additional_trivial_zero': {'point': '0', 'exact_Hurwitz_sum': str(trivial_value)},
               'positive_zeros': len(roots)}

    count = arb(top).zeta_nzeros().unique_fmpz()
    assert count is not None
    count = int(count)
    zroots = []
    computed = list(acb.zeta_zeros(1, count + 1))
    for index, z in enumerate(computed[:count], 1):
        assert z.real == arb('0.5')
        lo, hi = dyadic(z.imag.lower()), dyadic(z.imag.upper())
        assert 0 < lo < hi < top
        rounded = core.decimal_midpoint(lo, hi)
        radius = F(1, 2 * 10**20)
        assert F(rounded) - radius < lo < hi < F(rounded) + radius
        assert not zroots or F(zroots[-1]['hi']) < lo
        zroots.append({'index': index, 'lo': str(lo), 'hi': str(hi),
                       'rounded': rounded, 'rounding_cell_radius': str(radius),
                       'arb_zero': z.str(65)})
    assert computed[-1].imag > top
    zresult = {'positive_zeros': count, 'count_ball': arb(top).zeta_nzeros().str(65),
               'positive_root_intervals': zroots, 'next_zero': computed[-1].str(65)}

    mp.mp.dps = 85
    independent = []
    for name, rows in [('quadratic5', roots), ('zeta', zroots)]:
        for j in [0, len(rows) // 2, len(rows) - 1]:
            r = rows[j]
            if name == 'zeta':
                found = mp.im(mp.zetazero(j + 1))
                residual = abs(mp.zeta(mp.mpc('0.5', found)))
            else:
                def L(t):
                    s = mp.mpc('0.5', t)
                    return mp.power(5, -s) * mp.fsum(expected[a] * mp.zeta(s, mp.mpf(a) / 5)
                                                    for a in range(1, 5))
                center = mp.mpf(r['rounded'])
                derivative = mp.diff(L, center)
                projection = mp.re if abs(mp.re(derivative)) > abs(mp.im(derivative)) else mp.im
                found = mp.findroot(lambda t: projection(L(t)),
                                    (center - mp.mpf('0.0001'), center + mp.mpf('0.0001')),
                                    tol=mp.mpf('1e-78'))
                residual = abs(L(found))
            assert mpf(r['lo']) < found < mpf(r['hi']) and residual < mp.mpf('1e-74')
            independent.append({'factor': name, 'index': j + 1, 'mpmath_root': mp.nstr(found, 62),
                                'absolute_L_residual': mp.nstr(residual, 12), 'inside_interval': True})
    return {'status': 'passed', 'recorded_utc': datetime.now(timezone.utc).isoformat(),
            'precision_bits': bits, 'mpmath_decimal_digits': mp.mp.dps,
            'python_flint': flint.__version__, 'flint': flint.__FLINT_VERSION__,
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'core_source_sha256': hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest(),
            'top': top, 'quadratic5': qresult, 'zeta': zresult, 'independent_checks': independent,
            'scope': 'Positive zeros of the two specified factors through height 220; no global zero theorem.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--precision', type=int, choices=[160, 224], required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = certify(args.precision)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'precision_bits': args.precision,
                      'quadratic_positive': result['quadratic5']['positive_zeros'],
                      'quadratic_contour_count': result['quadratic5']['contour']['zero_count'],
                      'zeta_positive': result['zeta']['positive_zeros'], 'independent_checks': 6}), flush=True)
