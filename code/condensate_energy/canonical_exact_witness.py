#!/usr/bin/env python3
"""Exact physical transverse instability and limits of vacuum fitting."""
import hashlib
import json
from pathlib import Path

import sympy as s

from canonical_scalar_action import ROOT, OUT, load_exact_basis


def exact_transverse_witness():
    polys, quadratics, metric = load_exact_basis()
    k, t = s.symbols('k t', real=True)
    coords = {0:s.Rational(1,3), 6:s.Rational(1,5), 26:1/s.sqrt(2), 47:-1/s.sqrt(2), 48:t}
    restricted = []
    for j, p in enumerate(polys+quadratics):
        restricted.append(s.expand(sum(s.Rational(c,18 if j<17 else 1)*s.prod(coords[i] for i in m)
                                      for m,c in p.items() if all(i in coords for i in m))))
    coeff = [s.S.Zero]*21
    coeff[0]=coeff[1]=1
    for j in range(6,11):
        coeff[j]=1 if j==7 else 1+k
    coeff[11],coeff[12],coeff[13],coeff[16]=s.Rational(1,100),s.Rational(1,50),s.Rational(1,10),s.Rational(1,50)
    coeff[17],coeff[18],coeff[20]=-s.Rational(2743,7200),-s.Rational(41,240),-s.Rational(1259,625)
    potential=s.expand(sum(c*p for c,p in zip(coeff,restricted)))
    mass2=s.simplify(s.diff(potential,t,2).subs(t,0)/2)
    a,b,c,d=s.symbols('a b c d',real=True)
    d1=s.diag(a,b,c,d/s.sqrt(2));d2=s.diag(0,0,0,-s.I*d/s.sqrt(2));d3=s.zeros(4)
    ds=[d1,d2,d3]
    hol=sum(v.det() for v in ds)
    for i in range(3):
        for j in range(i+1,3):
            hol+=((ds[i]+ds[j]).det()+(ds[i]-ds[j]).det())/2
    hol=s.simplify(hol)
    lam,rho,alpha,x,y=s.symbols('lambda rho alpha x y',real=True)
    matrix=s.Matrix([[2*lam,alpha],[alpha,2*rho]])
    target=s.Matrix([x,y]);masses=matrix*target
    recovered=s.simplify(matrix.inv()*masses)
    # Coordinate 48 is Re(D3_00). An infinitesimal color transformation of
    # D_a proportional to E44 has support only in row/column4. Weak rotations
    # preserve E44. Hence this 00 fluctuation is orthogonal to every gauge
    # tangent and has electric charge -1/3, not a Goldstone direction.
    checks=dict(transverse_canonical_mass_formula=mass2==s.Rational(5,3)*k+s.Rational(4,5625),
                stable_side_positive=bool(mass2.subs(k,s.Rational(1,5))>0),
                unstable_side_negative=bool(mass2.subs(k,-s.Rational(1,5))<0),
                holomorphic_cubic_vertex_survives=hol==3*a*b*c*d/s.sqrt(2),
                holomorphic_third_derivative_nonzero=s.diff(hol,a,b,c)==3*d/s.sqrt(2),
                reverse_fitted_vacuum_is_identity=recovered==target)
    result=dict(checks=checks, transverse_field='Re(D3_00), canonical fluctuation sqrt(2)*Re(D3_00)',
                electric_charge_of_complex_component='-1/3', mass_squared=str(mass2),
                k_positive_mass_squared=str(mass2.subs(k,s.Rational(1,5))),
                k_negative_mass_squared=str(mass2.subs(k,-s.Rational(1,5))),
                exact_transverse_restricted_potential=str(potential),holomorphic_cubic=str(hol),
                phase50_input_mass_map=[str(v) for v in masses],phase50_recovered_targets=[str(v) for v in recovered],
                boundary='The spectrum witness uses the gauge-only canonical potential class, not a claim that these coefficients obey an unprovided complete ACS selection map. The instability is exact for this witness.')
    paths=[Path(__file__).resolve(),OUT/'protocol.md',OUT/'qualified-results.json',ROOT/'code/condensate_energy/canonical_scalar_action.py']
    result['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    result['all_checks_passed']=all(checks.values())
    (OUT/'exact-witness.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert result['all_checks_passed']


if __name__=='__main__':
    exact_transverse_witness()
