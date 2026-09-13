"""Equivalent left-half-plane evaluation for the finite contour instruments.

DLMF 25.15.5, with s=1-z and odd chi, gives
L(z,chi) = q**(-z) Gamma(1-z) (2*pi)**(z-1)
           * (-2*i*sin(pi*(1-z)/2)) G(chi) L(1-z,conjugate(chi)).
This avoids interval overestimation in a direct left-half-plane Hurwitz sum.
It changes the evaluator, not the contour or completeness obligations.
"""
import argparse
import hashlib
import json
from pathlib import Path
from flint import acb, arb, ctx, dirichlet_char as native_character
import lfunction_zero_certificate as producer
import lfunction_certificate_replay as checker


class FunctionalCharacter:
    def __init__(self, q, number):
        self.native = native_character(q, number)
        self.conjugate = native_character(q, pow(number, -1, q))
        self.q = q
        assert self.native.is_primitive() and int(self.native.parity()) == 1
        self.gauss = sum((self.native(a) * acb(0, 2 * arb.pi() * a / q).exp()
                          for a in range(q)), acb(0))
        assert (abs(self.gauss) ** 2).contains(q)

    def __getattr__(self, name):
        return getattr(self.native, name)

    def __call__(self, a):
        return self.native(a)

    def l(self, z):
        if z.real < 0:
            s = 1 - z
            return (acb(self.q) ** (-z) * s.gamma() / acb(2 * arb.pi()) ** s
                    * (-2 * acb(0, 1) * (arb.pi() * s / 2).sin())
                    * self.gauss * self.conjugate.l(s))
        return self.native.l(z)


def control(q, number, top):
    chi = FunctionalCharacter(q, number)
    rows = []
    for t in ['-0.5', '0', '5', str(top)]:
        z = acb(arb('-0.25'), arb(t))
        a, b = chi.native.l(z), chi.l(z)
        assert a.overlaps(b) and abs(a - b) < arb('1e-35')
        rows.append({'real_part': '-0.25', 'height': t,
                     'difference_ball': (a - b).str(60)})
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['certify', 'replay'])
    parser.add_argument('--character', choices=producer.SPECS, required=True)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    q, number, top, _ = producer.SPECS[args.character]
    ctx.prec = producer.BITS if args.mode == 'certify' else 224
    controls = control(q, number, top)
    if args.mode == 'certify':
        producer.dirichlet_char = FunctionalCharacter
        producer.certify(args.character, args.output)
        result = json.loads(args.output.read_text())
    else:
        assert args.certificate is not None
        assert json.loads(args.certificate.read_text())['character'] == args.character
        checker.dirichlet_char = FunctionalCharacter
        result = checker.replay(args.certificate)
    result.update(evaluation_backend='DLMF functional equation for Re(s)<0; direct FLINT elsewhere',
                  backend_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  direct_functional_controls=controls)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ['contour', 'segments', 'root_intervals', 'character_check']}, indent=2))
