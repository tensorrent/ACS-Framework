"""Compile elementary population and matching lemmas and preserve exact source attempts."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path

NAMES=['fixed_population_length','unequal_populations_disjoint','uncrossing','common_observation_separation','interval_center']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run(source,project,binary,output,versions):
    source,project,binary,output,versions=[p.absolute() for p in [source,project,binary,output,versions]]
    raw=source.read_bytes();digest=sha(raw);saved=versions/digest;saved.mkdir(parents=True,exist_ok=True);(saved/source.name).write_bytes(raw)
    command=[str(binary/'lake'),'env','lean','-R',str(source.parent),'-o',str(output.with_suffix('.olean')),str(source)]
    result=subprocess.run(command,cwd=project,capture_output=True,text=True,timeout=180,env={**os.environ,'PATH':str(binary)+os.pathsep+os.environ.get('PATH','')})
    assert source.read_bytes()==raw
    report={'status':'passed' if result.returncode==0 else 'failed','source_sha256':digest,'checker_sha256':sha(Path(__file__).read_bytes()),
            'command':command,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr,
            'olean_sha256':sha(output.with_suffix('.olean').read_bytes()) if result.returncode==0 else None,
            'lake_manifest_sha256':sha((project/'lake-manifest.json').read_bytes()),'theorems':NAMES,
            'scope':'Five elementary list/interval lemmas: cardinality under permutation and per-entry noise, disjointness of unequal populations, ordered uncrossing, the common-observation triangle bound, and a uniform interval-center bound. This does not formalize the complete quartic classification, certified zeros, finite inversion-removal algorithm, dynamic-program correctness or global ACS claims.'}
    if result.returncode==0:
        assert 'sorryAx' not in result.stdout+result.stderr and len([s for s in raw.decode().splitlines() if s.startswith('theorem ')])==len(NAMES)
        assert all('PopulationObservation.'+name in result.stdout for name in NAMES)
    output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return result.returncode
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['source','project','binary','output','versions']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();raise SystemExit(run(a.source,a.project,a.binary,a.output,a.versions))
