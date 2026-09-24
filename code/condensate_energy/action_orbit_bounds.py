#!/usr/bin/env python3
"""Sharp orbit bounds for both explicit historical Delta trace potentials."""
import json
import sympy as s
from canonical_scalar_action import ROOT

OUT = ROOT / 'docs/condensate_energy/action_matching'


def main():
    checks, models = [], {}

    def check(name, ok, evidence=None):
        checks.append(dict(name=name, passed=bool(ok), evidence=evidence))
        print(name, 'PASS' if ok else 'FAIL', flush=True)

    rho1, rho2, mass, N = s.symbols('rho1 rho2 mDelta N', real=True)
    for name, size in [('color_gram', 4), ('spin_gram', 3)]:
        eigenvalues = s.symbols('e0:' + str(size), nonnegative=True)
        trace = sum(eigenvalues)
        trace2 = sum(v ** 2 for v in eigenvalues)
        pair_differences = sum((eigenvalues[i] - eigenvalues[j]) ** 2 for i in range(size) for j in range(i + 1, size))
        pair_products = 2 * sum(eigenvalues[i] * eigenvalues[j] for i in range(size) for j in range(i + 1, size))
        check(name + '-sharp-lower-bound-identity', s.expand(size * trace2 - trace ** 2 - pair_differences) == 0)
        check(name + '-sharp-upper-bound-identity', s.expand(trace ** 2 - trace2 - pair_products) == 0)
        if name == 'color_gram':
            fields = [s.eye(4), s.zeros(4), s.zeros(4)]
            gram = sum((d.conjugate().T * d for d in fields), s.zeros(4))
        else:
            fields = [s.diag(*[int(i == a) for i in range(4)]) for a in range(3)]
            gram = s.Matrix([[s.trace(a.conjugate().T * b) for b in fields] for a in fields])
        check(name + '-lower-bound-attained-by-actual-Delta-fields', s.trace(gram * gram) / s.trace(gram) ** 2 == s.Rational(1, size))
        rankone = s.diag(0, 0, 0, 1)
        fields = [rankone / s.sqrt(2), -s.I * rankone / s.sqrt(2), s.zeros(4)]
        if name == 'color_gram':
            gram = sum((d.conjugate().T * d for d in fields), s.zeros(4))
        else:
            gram = s.Matrix([[s.trace(a.conjugate().T * b) for b in fields] for a in fields])
        check(name + '-neutral-vacuum-attains-upper-bound', s.trace(gram * gram) == s.trace(gram) ** 2 == 1)
        neutral_coefficient = rho1 + rho2
        spread_coefficient = rho1 + rho2 / size
        source_neutral = s.expand(neutral_coefficient.subs(rho2, s.Rational(16, 9) - 2 * rho1))
        source_spread = s.expand(spread_coefficient.subs(rho2, s.Rational(16, 9) - 2 * rho1))
        check(name + '-negative-rho2-favors-neutral-rankone', s.expand(neutral_coefficient - spread_coefficient - (1 - s.Rational(1, size)) * rho2) == 0)
        # At rho1=1/2, mDelta=-2( rho1+rho2 ), the neutral stationary norm is one.
        point = {rho1: s.Rational(1, 2), rho2: s.Rational(7, 9)}
        md = -2 * neutral_coefficient.subs(point)
        neutral_energy = -md ** 2 / (4 * neutral_coefficient.subs(point))
        spread_energy = -md ** 2 / (4 * spread_coefficient.subs(point))
        check(name + '-lower-energy-nonneutral-vacuum-at-fixed-action', spread_energy < neutral_energy,
              dict(mDelta=str(md), neutral_energy=str(neutral_energy), other_energy=str(spread_energy)))
        models[name] = dict(ratio_range=[str(s.Rational(1, size)), '1'],
            coercive_quartic_conditions=['rho1+rho2>0', f'rho1+rho2/{size}>0'],
            source_neutral_coefficient=str(source_neutral), source_spread_coefficient=str(source_spread),
            source_coercive_range=('-8/9<rho1<16/9' if size == 4 else '-16/9<rho1<16/9'),
            neutral_favored_range_under_source_relation='8/9<rho1<16/9 (rho2<0); necessary orientation sign, with additional exact tree-level flat modes)',
            lower_bound_witness=('D1=I4,D2=D3=0' if size == 4 else 'D1=E11,D2=E22,D3=E33'),
            negative_mass_counterexample=dict(mDelta=str(md), neutral_energy=str(neutral_energy), competing_energy=str(spread_energy)))
    output = dict(checks=checks, checks_passed=sum(c['passed'] for c in checks), checks_total=len(checks), models=models,
        proof='Each Gram is positive semidefinite; its eigenvalues are nonnegative. Cauchy-Schwarz and pairwise-product identities bound Tr(Gram^2)/(Tr Gram)^2 between 1/n and 1. Explicit Delta matrices attain both endpoints. A linear function of this ratio is positive everywhere iff it is positive at both endpoints.',
        limitations='Coercivity of the quartic and minimization within the pure-Delta two-trace models only. At a zero quartic endpoint, a negative quadratic can make the full potential unbounded. This does not replace boundedness tests for the full 17-quartic action.')
    (OUT / 'orbit-bounds.json').write_text(json.dumps(output, indent=2) + '\n')
    assert all(c['passed'] for c in checks), 'Failures retained in orbit-bounds.json'


if __name__ == '__main__':
    main()
