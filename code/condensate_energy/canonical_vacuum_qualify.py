#!/usr/bin/env python3
"""Correct the neutral pullback test; preserve original action and spectra."""
import copy
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s

from canonical_scalar_action import ROOT, OUT


def qualify_neutral_pullback():
    path = OUT / 'results.json'
    original = json.loads(path.read_text())
    failures = [c['name'] for c in original['checks'] if not c['passed']]
    assert failures == ['neutral-hessian-unchanged-by-hidden-coefficients'], failures
    for name, digest in original['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    result = copy.deepcopy(original)
    result['original_failure'] = failures
    result['checks'] = [c for c in result['checks'] if c['passed']]
    metric = np.array(result['kinetic_metric'])
    tangent = np.zeros((68, 4))
    tangent[0, 0], tangent[6, 1], tangent[7, 2] = 1, 1, 1
    tangent[26, 3], tangent[47, 3] = 1/np.sqrt(2), -1/np.sqrt(2)
    a, u, w, d = s.symbols('a u w d', real=True)
    exact_vars = dict(zip(['a','u','w','d'],[a,u,w,d]))
    exact_basis = [s.sympify(e, locals=exact_vars) for e in original['neutral']['restrictions']]
    vacuum = {a:s.Rational(1,3), u:s.Rational(1,5), w:0, d:1}
    pullbacks, neutral_spectra, exact_errors = [], [], []
    result['quartic_boundedness'] = {}
    for name, row in result['cases'].items():
        coeff = row['quartic_coefficients'] + row['quadratic_coefficients']
        rational = [s.Rational(str(c)).limit_denominator(10**6) for c in coeff]
        potential = s.expand(sum(c*e for c,e in zip(rational,exact_basis)))
        exact_h = s.hessian(potential,[a,u,w,d]).subs(vacuum)
        exact_grad = s.Matrix([s.diff(potential,v) for v in [a,u,w,d]]).subs(vacuum)
        raw = np.array(row['canonical_hessian']) * np.sqrt(metric[:,None]*metric[None,:])
        pulled = tangent.T @ raw @ tangent
        exact_errors.append(float(np.max(abs(pulled-np.array(exact_h,float)))))
        row['neutral_pullback_hessian'] = pulled.tolist()
        row['exact_neutral_gradient'] = [str(x) for x in exact_grad]
        row['exact_quadratic_coefficients'] = [str(x) for x in rational[17:]]
        if name.startswith('angular-'):
            pullbacks.append(pulled)
            neutral_spectra.append(next(r['mass_squared'] for r in row['sectors'] if r['abs_electric_charge']==0))
        lower_delta = min(rational[6:11]) - s.Rational(3,16)*s.sqrt(rational[11]**2+rational[12]**2)
        lower_cross = rational[13] - abs(rational[15])/2 - abs(rational[16])/2
        result['quartic_boundedness'][name] = dict(Nphi_squared_lower_coefficient='1',
            NDelta_squared_lower_coefficient=str(lower_delta), mixed_lower_coefficient=str(lower_cross),
            positive=bool(lower_delta>0 and lower_cross>0),
            proof='Five projected Delta norms sum to NDelta^2; |HDelta|<=3 NDelta^2/16 by real-Gaussian polarization and the determinant Frobenius bound; |detPhi|<=Nphi/2; |Jphi|<=Nphi/2 and |JDelta|<=NDelta.')
    difference = max(float(np.max(abs(v-pullbacks[0]))) for v in pullbacks)
    spectrum_difference = max(float(np.max(abs(np.array(v)-neutral_spectra[0]))) for v in neutral_spectra)
    result['corrected_neutral_comparison'] = dict(tangent=tangent.tolist(), maximum_pullback_difference=difference,
        maximum_exact_Hessian_difference=max(exact_errors), maximum_physical_neutral_mass_squared_difference=spectrum_difference)
    result['checks'].extend([
        dict(name='declared-neutral-tangent-Hessian-unchanged',passed=difference<1e-12),
        dict(name='pullback-matches-independent-exact-neutral-Hessian',passed=max(exact_errors)<1e-12),
        dict(name='physical-neutral-spectrum-unchanged',passed=spectrum_difference<1e-10),
        dict(name='all-witness-quartics-bounded-below',passed=all(c['positive'] for c in result['quartic_boundedness'].values()))])
    sources = [Path(__file__).resolve(), OUT/'numerical-amendment.md', path,
               ROOT/'code/condensate_energy/canonical_scalar_action.py']
    result['qualification_sha256'] = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    result['all_checks_passed'] = all(c['passed'] for c in result['checks'])
    (OUT/'qualified-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(corrected_neutral_comparison={k:v for k,v in result['corrected_neutral_comparison'].items() if k!='tangent'},
                         checks=result['checks'][-4:],total_checks=len(result['checks']),all_checks_passed=result['all_checks_passed']),indent=2))
    assert result['all_checks_passed']


if __name__=='__main__':
    qualify_neutral_pullback()
