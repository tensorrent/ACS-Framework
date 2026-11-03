"""Compile the noise-box transfer theorem and preserve the exact attempted source."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path

NAMES=['interval_member','box_member','certificate_transfer','reverse_inclusion_fails']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run(source,project,binary,output,versions):
    source,project,binary,output,versions=[p.absolute() for p in [source,project,binary,output,versions]]
    raw=source.read_bytes();digest=sha(raw);saved=versions/digest;saved.mkdir(parents=True,exist_ok=True);(saved/source.name).write_bytes(raw)
    compiled=project/source.name;compiled.write_bytes(raw)
    command=[str(binary/'lake'),'env','lean','-o',str(output.with_suffix('.olean')),source.name]
    result=subprocess.run(command,cwd=project,capture_output=True,text=True,timeout=180,env={**os.environ,'PATH':str(binary)+os.pathsep+os.environ.get('PATH','')})
    assert source.read_bytes()==compiled.read_bytes()==raw
    report={'status':'passed' if result.returncode==0 else 'failed','source_sha256':digest,'checker_sha256':sha(Path(__file__).read_bytes()),
            'command':command,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr,
            'olean_sha256':sha(output.with_suffix('.olean').read_bytes()) if result.returncode==0 else None,
            'lake_manifest_sha256':sha((project/'lake-manifest.json').read_bytes()),'theorems':NAMES,
            'scope':'Checks scalar and coordinatewise interval inclusion, transfer of an arbitrary universally valid box predicate to a contained box, and failure of the reverse inclusion. The explicit formula, numerical budgets, arithmetic/local premises and file lineage are not formalized here.'}
    if result.returncode==0:
        assert 'sorryAx' not in result.stdout and len([s for s in raw.decode().splitlines() if s.startswith('theorem ')])==len(NAMES)
        assert all('NoiseBoxTransfer.'+name in result.stdout for name in NAMES)
    output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return result.returncode

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['source','project','binary','output','versions']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();raise SystemExit(run(a.source,a.project,a.binary,a.output,a.versions))
