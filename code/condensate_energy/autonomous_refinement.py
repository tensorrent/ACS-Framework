#!/usr/bin/env python3
"""Four targeted resolution checks after the original registered sweep."""
import hashlib
import json
from pathlib import Path
import time

from autonomous_gate import OUT, ROOT, curve_error, evolve


def main():
    started=time.monotonic()
    original=json.loads((OUT/'results.json').read_text())
    for name,digest in original['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    assert original['all_checks_passed']
    sources=[Path(__file__).resolve(),OUT/'refinement-protocol.md',
             ROOT/'code/condensate_energy/autonomous_gate.py',ROOT/'code/condensate_energy/run.py']
    result=dict(source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                parent_results_sha256=hashlib.sha256((OUT/'results.json').read_bytes()).hexdigest(),cases={},checks=[])
    jobs=[]
    cfg=original['cases']['middle-g16-M0.1-K0.1']['parameters'].copy()
    cfg.update(dx=.025,dt=.00125)
    jobs.append(('fast-soft-third',cfg))
    for label in ['low','middle','high']:
        cfg=original['cases'][f'selected-long-{label}']['parameters'].copy()
        cfg.update(dx=.05,dt=.0025)
        jobs.append((f'long-refined-{label}',cfg))
    for name,cfg in jobs:
        result['cases'][name],_,_=evolve(**cfg)
        print(f'EVOLVED {name}: {json.dumps(result["cases"][name]["summary"])}',flush=True)
        (OUT/'refinement-results.json').write_text(json.dumps(result,indent=2)+'\n')
    comparisons={}
    for key in ['trapped','height']:
        older=curve_error(original['cases']['middle-g16-M0.1-K0.1'],
                          original['cases']['refined-middle-g16-M0.1-K0.1'],key)
        newer=curve_error(original['cases']['refined-middle-g16-M0.1-K0.1'],
                          result['cases']['fast-soft-third'],key)
        comparisons[key]=dict(previous=older,next=newer)
    result['checks'].append(dict(name='fast soft gate converges at third resolution',
                                  passed=all(r['next']<r['previous'] for r in comparisons.values()),
                                  differences=comparisons))
    for label in ['low','middle','high']:
        old=original['cases'][f'selected-long-{label}']
        new=result['cases'][f'long-refined-{label}']
        error=curve_error(old,new)
        relative=abs(new['history'][-1]['trapped']-old['history'][-1]['trapped'])/old['history'][-1]['trapped']
        result['checks'].append(dict(name=f'long {label} trajectory refines',passed=error<.03 and relative<.05,
                                      max_trapped_curve_error=error,endpoint_relative_difference=relative))
    for key in ['energy_drift','field_work_residual','gate_work_residual','trap_budget_residual','max_distant_tail']:
        value=max(r[key] for r in result['cases'].values())
        threshold=1e-8 if key=='max_distant_tail' else .001
        result['checks'].append(dict(name=key,passed=value<threshold,maximum=value,tolerance=threshold))
    result['all_checks_passed']=all(r['passed'] for r in result['checks'])
    result['elapsed_seconds']=time.monotonic()-started
    (OUT/'refinement-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['checks'],indent=2),flush=True)
    if not result['all_checks_passed']:
        raise SystemExit('A supplemental precision check failed; retain qualification in report.')


if __name__=='__main__':
    main()
