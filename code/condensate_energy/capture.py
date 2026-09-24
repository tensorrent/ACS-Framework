#!/usr/bin/env python3
"""Reverse-preparation audit using the frozen, already checked wave instrument."""
import hashlib
import json
import math
import numpy as np
from run import OUT, ROOT, CHECKS, build_grid, node_energy, simulate, curve_error, check


def incoming(height, dx=.1, dt=.005):
    x, potential, _ = build_grid(height, 1., dx, 160.)
    xi, sigma, k = x[1:-1], 4., np.pi/4
    q = np.exp(-.5*((xi-30)/sigma)**2-1j*k*xi)
    p = (-(xi-30)/sigma**2-1j*k)*q
    norm = math.sqrt(node_energy(q,p,potential,dx).sum())
    result, _, _, _ = simulate(height,1.,dx=dx,dt=dt,domain=160.,initial=(q/norm,p/norm))
    peak = max(result['history'],key=lambda r:r['trapped'])
    result['capture_summary'] = dict(initial=result['history'][0]['trapped'],peak=peak['trapped'],
                                     peak_time=peak['t'],at_80=result['history'][-1]['trapped'],
                                     minimum_signed_outward_integral=min(r['outward_flux_integral'] for r in result['history']))
    return result


def main():
    cases={f'h{h:g}':incoming(h) for h in [0.,4.,9.]}
    cases['refined-h4']=incoming(4.,dx=.05,dt=.0025)
    energy=max(c['energy_drift'] for c in cases.values())
    flux=max(max(c['core_flux_balance'],c['trap_flux_balance']) for c in cases.values())
    tail=max(c['distant_tail_fraction'] for c in cases.values())
    refinement=curve_error(cases['h4'],cases['refined-h4'])
    check('incoming preparation conserves field energy',energy<1e-8,max_drift=energy)
    check('signed flux resolves energy entering and leaving the cavity',flux<1e-8,max_residual=flux)
    check('incoming domain endpoint remains unvisited',tail<1e-8,max_tail_fraction=tail)
    check('incoming central preparation converges under refinement',refinement<.02,max_curve_difference=refinement)
    sources=['code/condensate_energy/run.py','code/condensate_energy/capture.py','docs/condensate_energy/capture-protocol.md']
    result=dict(scope='Exploratory reverse-preparation supplement; temporary capture is not permanent mass',
                cases=cases,checks=CHECKS,source_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources})
    (OUT/'capture-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v['capture_summary'] for k,v in cases.items()},indent=2))


if __name__=='__main__':
    main()
