#!/usr/bin/env python3
"""Assemble the static documentary site under build/site and check it offline.

The site is plain HTML, CSS and ES modules from site/, with three.js and KaTeX vendored in
site/vendor (checked against site/vendor/VENDOR.sha256). Papers are served beside it so the
site links straight to each PDF and its LaTeX source. Rendered assets are listed in
site/assets/manifest.json with their generator and sha256, so a regenerated asset that drifts
fails the build instead of shipping silently. Nothing here touches the network.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
# Development-only parts of site/ that are never published.
SKIP = {'blender', 'tests', 'node_modules', 'package.json', 'package-lock.json'}
REF = re.compile(r'''(?:href|src)\s*=\s*["']([^"'#][^"']*)["']''', re.I)
DATA_KEYS = {'pdf', 'tex', 'source', 'path', 'figure', 'output'}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_vendor():
    problems = []
    listing = SITE / 'vendor' / 'VENDOR.sha256'
    for line in listing.read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        path = SITE / 'vendor' / name
        if not path.exists():
            problems.append(f'vendor file missing: {name}')
        elif sha256(path) != digest:
            problems.append(f'vendor file changed: {name}')
    return problems


def check_manifest():
    """Every rendered asset must exist, match its recorded hash, and name its generator."""
    manifest = SITE / 'assets' / 'manifest.json'
    if not manifest.exists():
        return [], []
    entries = json.loads(manifest.read_text())['assets']
    problems = []
    for entry in entries:
        path = SITE / 'assets' / entry['output']
        generator = SITE / entry['generator']
        if not generator.exists():
            problems.append(f"{entry['id']}: generator {entry['generator']} missing")
        if not path.exists():
            problems.append(f"{entry['id']}: {entry['output']} missing")
        elif sha256(path) != entry['sha256']:
            problems.append(f"{entry['id']}: {entry['output']} does not match its recorded sha256")
    return problems, entries


def copy_tree(output):
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(SITE, output, ignore=lambda d, names: [n for n in names if Path(d) == SITE and n in SKIP])
    for pattern in ('**/*.pdf', '**/*.tex'):
        for path in sorted((ROOT / 'papers').glob(pattern)):
            target = output / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    shutil.copy2(ROOT / 'papers' / 'catalog.json', output / 'data' / 'catalog.json')
    for path in sorted((ROOT / 'visualizations').glob('*.html')):
        target = output / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def data_paths(node):
    """Yield repo-relative paths named by the site's data files (papers, figures, assets)."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in DATA_KEYS and isinstance(value, str) and not re.match(r'[a-z]+:', value):
                yield value
            else:
                yield from data_paths(value)
    elif isinstance(node, list):
        for value in node:
            yield from data_paths(value)


def check_links(output):
    problems, external = [], 0
    for page in sorted(output.rglob('*.html')):
        if page.is_relative_to(output / 'visualizations'):
            continue  # standalone pages, checked by their own suite
        for ref in REF.findall(page.read_text(errors='replace')):
            parts = urlsplit(ref)
            if parts.scheme or ref.startswith('//'):
                external += 1
                continue
            target = (page.parent / unquote(parts.path)).resolve()
            if parts.path and not target.exists():
                problems.append(f'{page.relative_to(output)}: broken link {ref}')
    for data in sorted((output / 'data').glob('*.json')):
        for ref in data_paths(json.loads(data.read_text())):
            if not (output / ref).exists() and not (output / 'assets' / ref).exists():
                problems.append(f'{data.relative_to(output)}: missing target {ref}')
    return problems, external


def check_llm_txt():
    """Verify llm.txt and llms.txt exist and match the canonical structured generator."""
    from generate_llm_txt import build_llm_text
    expected = build_llm_text()
    problems = []
    for rel in ('llm.txt', 'llms.txt', 'site/llm.txt', 'site/llms.txt'):
        path = ROOT / rel
        if not path.exists():
            problems.append(f'missing structured LLM file: {rel}')
        elif path.read_text(encoding='utf-8') != expected:
            problems.append(f'structured LLM file out of date (run scripts/generate_llm_txt.py): {rel}')
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'build/site')
    args = parser.parse_args()
    problems = check_vendor()
    manifest_problems, assets = check_manifest()
    problems += manifest_problems
    problems += check_llm_txt()
    copy_tree(args.output)
    link_problems, external = check_links(args.output)
    problems += link_problems
    report = dict(output=str(args.output), assets=len(assets), external_links_not_fetched=external,
                  problems=problems, passed=not problems)
    (args.output / 'build-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if not problems else 1


if __name__ == '__main__':
    sys.exit(main())
