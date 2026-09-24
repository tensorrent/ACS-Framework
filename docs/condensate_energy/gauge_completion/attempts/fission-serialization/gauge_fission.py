#!/usr/bin/env python3
"""Registered product-energy checks; these do not measure fission dynamics."""
import hashlib
import json
from pathlib import Path

from gauge_completion import ROOT, OUT, gauged_bvp


def run_fission_checks():
    paths = [Path(__file__).resolve(), OUT / 'fission-protocol.md', OUT / 'results.json',
             ROOT / 'code/condensate_energy/gauge_completion.py']
    survey = json.loads((OUT / 'results.json').read_text())
    result = dict(source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                  cases={}, comparisons=[], checks=[])
    for e in [0., .08, .12]:
        reference = survey['cases'][f'Q1000-e{e:g}']
        rows = {}
        for q in [600., 500., 400., 999., 1001.]:
            row = gauged_bvp(q, e, reference, tolerance=1e-8)
            rows[q] = row
            result['cases'][f'e{e:g}-Q{q:g}'] = row
            print(e, q, row['success'], row['energy'], row['omega'], flush=True)
        derivative = (rows[1001.]['energy'] - rows[999.]['energy']) / 2
        relative = abs(derivative / reference['omega'] - 1)
        comparison = dict(coupling=e, parent_energy=reference['energy'],
                          derivative_energy=derivative, omega=reference['omega'],
                          derivative_relative=relative, partitions=[])
        for a, b in [(500., 500.), (400., 600.)]:
            total = rows[a]['energy'] + rows[b]['energy']
            comparison['partitions'].append(dict(charges=[a, b], product_energy=total,
                product_minus_parent=total - reference['energy'],
                endpoints_localized=bool(rows[a]['localized_candidate'] and rows[b]['localized_candidate']),
                lower_product_energy=bool(total < reference['energy'])))
        result['comparisons'].append(comparison)
        result['checks'].append(dict(name=f'chemical-potential-e{e:g}', passed=relative < 1e-5))
    result['checks'].append(dict(name='product-solvers-and-identities', passed=all(
        r['success'] and r['max_rms_residual'] < 1e-5 and r['virial_relative'] < 1e-4
        and r['gauss_relative'] < 1e-5 for r in result['cases'].values())))
    result['all_checks_passed'] = all(r['passed'] for r in result['checks'])
    (OUT / 'fission-results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(comparisons=result['comparisons'], checks=result['checks']), indent=2), flush=True)


if __name__ == '__main__':
    run_fission_checks()
