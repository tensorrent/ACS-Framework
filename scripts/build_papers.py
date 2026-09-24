#!/usr/bin/env python3
"""Build the complete canonical LaTeX corpus without changing source directories."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def compile_paper(source, output, executable, update):
    destination = output / source.relative_to(ROOT).parent
    destination.mkdir(parents=True, exist_ok=True)
    process = subprocess.run(
        [executable, '--untrusted', '--keep-logs', '--outdir', str(destination), source.name],
        cwd=source.parent, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=240,
    )
    log = destination / (source.stem + '.log')
    diagnostic = process.stdout + ('\n' + log.read_text(errors='replace') if log.exists() else '')
    (destination / (source.stem + '.console.txt')).write_text(process.stdout)
    fatal = re.findall(r'[^\n]*(?:undefined references|undefined citations|Citation .* undefined|Reference .* undefined|Missing character)[^\n]*', diagnostic, re.I)
    overfull = re.findall(r'Overfull \\[hv]box \(([^)]*)\)', diagnostic)
    pdf = destination / source.with_suffix('.pdf').name
    passed = process.returncode == 0 and pdf.exists() and not fatal
    if passed and update:
        shutil.copy2(pdf, source.with_suffix('.pdf'))
    return dict(source=str(source.relative_to(ROOT)), passed=passed,
                returncode=process.returncode, fatal_diagnostics=sorted(set(fatal)),
                overfull_boxes=sorted(set(overfull)), pdf=str(pdf.relative_to(output)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'build/publication')
    parser.add_argument('--tectonic', default='tectonic')
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--update-pdfs', action='store_true')
    parser.add_argument('--paper', action='append', help='Repository-relative source; default all papers')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    sources = [ROOT / x for x in args.paper] if args.paper else sorted((ROOT / 'papers').rglob('*.tex'))
    sources = [p for p in sources if '\\documentclass' in p.read_text()]
    results = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(compile_paper, p, output, args.tectonic, args.update_pdfs): p for p in sources}
        for future in as_completed(futures):
            try:
                row = future.result()
            except Exception as error:
                row = dict(source=str(futures[future].relative_to(ROOT)), passed=False, error=str(error))
            results.append(row)
            print(('PASS ' if row['passed'] else 'FAIL ') + row['source'], flush=True)
    report = dict(total=len(results), passed=sum(r['passed'] for r in results),
                  papers=sorted(results, key=lambda r: r['source']))
    (output / 'build-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'papers'}))
    return 0 if report['total'] == report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
