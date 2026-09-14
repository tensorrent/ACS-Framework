"""Compile source-error, critical-strip, budget-bootstrap and mixed-derivative lemmas."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path

NAMES=['source_radius_necessity','source_radius_sufficiency','critical_source_strip','scalar_segment_stays_in_strip','common_budget_difference_cap','bootstrap_excludes_subthreshold','mixed_kernel_derivative']
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
            'scope':'Seven generic lemmas: necessary and sufficient source-error bounds, critical-coordinate strip, segment containment, common-report difference cap, noncircular subthreshold bootstrap and the actual derivative sign for a free A versus B kernel. The complete concrete secant-family and contraction theorem remains partly written or computational; inherited Lean lemmas retain their scopes.'}
    if result.returncode==0:
        assert 'sorryAx' not in result.stdout+result.stderr and len([s for s in raw.decode().splitlines() if s.startswith('theorem ')])==len(NAMES)
        assert all('SourceConstrainedNoise.'+name in result.stdout for name in NAMES)
    output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return result.returncode
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['source','project','binary','output','versions']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();raise SystemExit(run(a.source,a.project,a.binary,a.output,a.versions))
