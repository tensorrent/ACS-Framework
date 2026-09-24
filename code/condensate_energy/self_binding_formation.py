#!/usr/bin/env python3
"""Unprepared condensate, charged Gaussian input; no external gate schedule."""
import hashlib
import json
from pathlib import Path
import numpy as np

from self_binding import ROOT,OUT,B_SOURCE,RadialGrid
from self_binding_dynamics import evolve,curve_error


def packet(sigma,dr):
    grid=RadialGrid(120.,dr)
    f=np.exp(-.5*(grid.r/sigma)**2)
    f*=np.sqrt(1000./float(grid.w@f**2))
    return dict(dr=dr,b=B_SOURCE,charge=1000.,
                profile=dict(r=grid.r.tolist(),chi=np.ones(grid.n).tolist(),f=f.tolist()))


def main():
    sources=[Path(__file__).resolve(),ROOT/'code/condensate_energy/self_binding_dynamics.py',
             ROOT/'code/condensate_energy/self_binding.py',OUT/'formation-protocol.md']
    data=dict(source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              cases={},checks=[])
    for name,sigma,dr,frozen in [('sigma3',3.,.1,False),('sigma6',6.,.1,False),
                                 ('sigma9',9.,.1,False),('refined-sigma6',6.,.05,False),
                                 ('frozen-sigma6',6.,.1,True)]:
        row=evolve(packet(sigma,dr),frozen_vacuum=frozen)
        row['packet_sigma']=sigma
        data['cases'][name]=row
        print('FORMED',name,json.dumps({k:v for k,v in row.items() if k!='history'}),flush=True)
        (OUT/'formation-results.json').write_text(json.dumps(data,indent=2)+'\n')
    for key,threshold in [('energy_drift',.001),('charge_drift',1e-8),('max_distant_tail',1e-8)]:
        value=max(r[key] for r in data['cases'].values())
        data['checks'].append(dict(name=key,passed=value<threshold,maximum=value,tolerance=threshold))
    error=curve_error(data['cases']['sigma6'],data['cases']['refined-sigma6'],'local_energy')
    data['checks'].append(dict(name='central formation local energy refines',passed=error<.02,max_curve_difference=error))
    difference=abs(data['cases']['sigma6']['initial_energy']-data['cases']['frozen-sigma6']['initial_energy'])
    data['checks'].append(dict(name='matched response control has identical initial energy',passed=difference<1e-10,difference=difference))
    data['all_checks_passed']=all(r['passed'] for r in data['checks'])
    (OUT/'formation-results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data['checks'],indent=2))
    if not data['all_checks_passed']:
        raise SystemExit('Formation precision check failed; preserve the outcome.')


if __name__=='__main__':
    main()
