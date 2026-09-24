#!/usr/bin/env python3
"""Qualify all abnormal multistart stops using a different optimization method."""
import json
import math
import numpy as np
from scipy.optimize import minimize

from radiative_flat_modes import OUT
from radiative_vacuum_search import effective_potential, probabilities


def main():
    source = json.loads((OUT / 'vacuum-search.json').read_text())
    checks, reviews = [], []
    for case in source['searches']:
        singular = case['Majorana_singular']
        base = effective_potential([1, 0, 0, 0], 0., singular)
        rows = []
        for support in case['supports']:
            rank = support['rank']
            bounds = [(0., math.pi / 4)] + [(0., math.pi / 2)] * (rank - 1)
            for batch in ['initial', 'repeated']:
                for index, run in enumerate(support[batch]['runs']):
                    if run['success']:
                        continue

                    def objective(values):
                        return 1e4 * (effective_potential(probabilities(values[1:]), values[0], singular) - base)

                    # Independent derivative-free solve from the original start.
                    result = minimize(objective, run['start'], method='Powell', bounds=bounds,
                                      options=dict(xtol=1e-10, ftol=1e-11, maxiter=1000))
                    rows.append(dict(rank=rank, batch=batch, original_run=index,
                        original_message=run['message'], original_energy=run['energy_relative'],
                        success=bool(result.success), message=str(result.message),
                        energy_relative=float(result.fun / 1e4), theta=float(result.x[0]),
                        q=probabilities(result.x[1:]).tolist()))
        if rows:
            for name, ok in [('all-independent-retries-successful', all(r['success'] for r in rows)),
                             ('no-retry-undercuts-selected-candidate', all(r['energy_relative'] >= case['best']['energy_relative'] - 1e-9 for r in rows)),
                             ('all-retries-return-neutral-energy', all(abs(r['energy_relative']) < 1e-9 for r in rows))]:
                checks.append(dict(name=str(singular) + '-' + name, passed=bool(ok)))
                print(checks[-1]['name'], 'PASS' if ok else 'FAIL', flush=True)
        reviews.append(dict(Majorana_singular=singular, retries=rows))
    result = dict(checks=checks, checks_passed=sum(c['passed'] for c in checks), checks_total=len(checks),
        reviews=reviews, retries_total=sum(len(r['retries']) for r in reviews),
        qualification='Original abnormal L-BFGS-B stops remain in vacuum-search.json. Powell retries use original starts. '
        'These checks qualify optimizer stops, not a mathematical global-minimum certificate.')
    (OUT / 'search-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=result['checks_passed'], retries_total=result['retries_total'])))
    assert all(c['passed'] for c in checks), 'Failures retained in search-audit.json'


if __name__ == '__main__':
    main()
