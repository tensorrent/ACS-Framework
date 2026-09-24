#!/usr/bin/env python3
"""Verify the publication's inventory and frozen evidence, then rerun its scoped checks."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT/'docs/publication/2026-09-24'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    failures=[]
    manifest=json.loads((RECORD/'publication-manifest.json').read_text())
    for name,expected in manifest['sha256'].items():
        p=ROOT/name
        if not p.is_file() or digest(p)!=expected: failures.append('manifest mismatch: '+name)
    sources=sorted(str(p.relative_to(ROOT)) for p in (ROOT/'papers').rglob('*.tex') if '\\documentclass' in p.read_text())
    if sources!=sorted(manifest['manuscripts']): failures.append('manuscript inventory changed')
    amended=json.loads((RECORD/'amendments.json').read_text())
    for entry in amended:
        source=(ROOT/entry['path']).read_text()
        if source.count('% Publication amendment: 2026-09-24')!=1: failures.append('missing/duplicate amendment: '+entry['path'])
        if not (ROOT/entry['path']).with_suffix('.pdf').is_file(): failures.append('missing PDF: '+entry['path'])
    receipt=json.loads((ROOT/'docs/condensate_energy/endpoint_audit/receipt.json').read_text())
    verified=0; relocated=0; external=[]
    relocations=json.loads((RECORD/'receipt-relocations.json').read_text())
    for section in ['prior_receipts_verified','prior_artifacts_verified','linked_evidence_verified','artifact_sha256']:
        for name,expected in receipt[section].items():
            p=Path(relocations.get(name,name))
            if name in relocations: relocated+=1
            if p.is_absolute() or not (ROOT/p).is_file():
                external.append(dict(section=section,path=name,sha256=expected))
                continue
            if digest(ROOT/p)!=expected: failures.append('archived receipt mismatch: '+name)
            else: verified+=1
    # Missing archive-only links are explicitly inventoried, never silently promoted to passes.
    if external!=manifest['external_receipt_references']: failures.append('external reference inventory changed')
    result=dict(manuscripts=len(sources),amended=len(amended),manifest_files=len(manifest['sha256']),
                receipt_references_verified=verified,relocated_references=relocated,archive_only_references=len(external),failures=failures)
    output=ROOT/'build/publication';output.mkdir(parents=True,exist_ok=True)
    (output/'integrity-report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    return not failures


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only',action='store_true')
    args=parser.parse_args()
    if not verify(): return 1
    if not args.integrity_only:
        subprocess.run([sys.executable,str(ROOT/'code/publication_20260924/verify_science.py')],cwd=ROOT,check=True)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
