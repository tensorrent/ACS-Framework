#!/usr/bin/env python3
"""Larger-domain qualification of the preserved bound-mode control failure."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/condensate_energy/capture_stability'


def matching(omega):
    return omega/math.tan(4*omega)+math.sqrt(max(0., 4-omega**2))


def main():
    roots = [brentq(matching, (j+.5)*math.pi/4+1e-12,
                    min((j+1)*math.pi/4-1e-12, 2.), xtol=1e-14) for j in range(3)]
    exact = np.array(roots)**2
    grids = {}
    for domain in [40., 60.]:
        for dx in [.1, .05]:
            x = np.arange(round(domain/dx)+1)*dx
            potential = 4*np.clip((x+dx/2-4)/dx, 0., 1.)
            diagonal = 2/dx**2+potential[1:-1]
            ev = eigh_tridiagonal(diagonal, np.full(len(diagonal)-1, -1/dx**2),
                                  select='i', select_range=(0, 2), eigvals_only=True)
            grids[f'D{domain:g}-dx{dx:g}'] = ev.tolist()
    coarse = float(max(abs(np.array(grids['D60-dx0.1'])-exact)))
    fine = float(max(abs(np.array(grids['D60-dx0.05'])-exact)))
    domain_errors = [float(max(abs(np.array(grids[f'D60-dx{dx:g}'])-
                                  np.array(grids[f'D40-dx{dx:g}'])))) for dx in [.1, .05]]
    residual = max(abs(matching(r)) for r in roots)
    checks = [dict(name='analytic bound-mode matching', passed=residual<1e-9, residual=residual),
              dict(name='expanded-domain bound-mode spatial convergence',
                   passed=fine<coarse and fine<.005, coarse_error=coarse, fine_error=fine),
              dict(name='expanded-domain bound-mode remote wall independence',
                   passed=max(domain_errors)<1e-5, domain_errors=domain_errors)]
    sources = [Path(__file__).resolve(), OUT/'domain-amendment.md']
    payload = dict(scope='Supplement replaces failed D20 versus D40 boundary qualification only',
                   source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in sources},
                   omega=roots, eigenvalues=exact.tolist(), finite_grid_eigenvalues=grids,
                   decay_rates=[math.sqrt(4-r*r) for r in roots], checks=checks,
                   all_checks_passed=all(c['passed'] for c in checks))
    (OUT/'bound-domain-results.json').write_text(json.dumps(payload, indent=2)+'\n')
    print(json.dumps(payload, indent=2))
    if not payload['all_checks_passed']:
        raise SystemExit('Expanded domain failed unchanged tolerance.')


if __name__ == '__main__':
    main()
