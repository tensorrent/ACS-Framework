#!/usr/bin/env python3
"""Check maintained navigation links and canonical paper/evidence coverage offline.

This intentionally checks the current navigation surface, not frozen historical
Markdown. External URLs are counted but are not fetched or declared reachable.
"""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "README.md", "papers/README.md", "code/README.md", "docs/README.md",
    "docs/REPRODUCTION.md", "docs/BRANCHES.md", "docs/CONDENSATE_EVIDENCE.md",
)
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")


def heading_ids(text):
    """Resolve ordinary ATX headings used by the maintained navigation pages."""
    seen = {}
    result = set()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        number = seen.get(slug, 0)
        seen[slug] = number + 1
        result.add(slug if number == 0 else f"{slug}-{number}")
    return result


def check(root):
    failures = []
    local_links = external_links = 0
    page_text = {}
    for name in PAGES:
        page = root / name
        if not page.is_file():
            failures.append(f"missing navigation page: {name}")
            continue
        content = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", page.read_text(), flags=re.M | re.S)
        page_text[name] = content
        for destination in LINK.findall(content):
            value = destination.strip().removeprefix("<").removesuffix(">")
            url = urlsplit(value)
            if url.scheme in {"http", "https", "mailto"}:
                external_links += 1
                continue
            if url.scheme or url.netloc or url.path.startswith("/"):
                failures.append(f"nonportable link in {name}: {value}")
                continue
            target = (page.parent / unquote(url.path)).resolve() if url.path else page
            local_links += 1
            if not target.is_relative_to(root) or not target.exists():
                failures.append(f"broken local link in {name}: {value}")
            elif url.fragment and target.suffix == ".md":
                if unquote(url.fragment) not in heading_ids(target.read_text()):
                    failures.append(f"missing heading in {name}: {value}")

    catalog = json.loads((root / "papers/catalog.json").read_text())["papers"]
    sources = [entry["source"] for entry in catalog]
    pdfs = [entry["pdf"] for entry in catalog]
    expected = {
        str(path.relative_to(root)) for path in (root / "papers").rglob("*.tex")
        if "\\documentclass" in path.read_text()
    }
    if set(sources) != expected:
        failures.append(f"catalog coverage differs: missing={sorted(expected-set(sources))}, extra={sorted(set(sources)-expected)}")
    if len(sources) != len(set(sources)) or len(pdfs) != len(set(pdfs)):
        failures.append("duplicate paper source or PDF in catalog")
    for entry in catalog:
        source, pdf = Path(entry["source"]), Path(entry["pdf"])
        if source.with_suffix(".pdf") != pdf:
            failures.append(f"source/PDF mismatch: {source}")
        for target in (source, pdf):
            resolved = (root / target).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                failures.append(f"missing or nonportable catalog path: {target}")
            elif f"]({target.relative_to('papers').as_posix()})" not in page_text.get("papers/README.md", ""):
                failures.append(f"paper missing clickable catalog entry: {target}")
        if not entry.get("label") or not entry.get("group") or not entry.get("summary"):
            failures.append(f"missing navigation description: {source}")

    evidence = sorted((root / "docs/condensate_energy").rglob("README.md"))
    for path in evidence:
        link = path.relative_to(root / "docs").as_posix()
        if f"]({link})" not in page_text.get("docs/CONDENSATE_EVIDENCE.md", ""):
            failures.append(f"unindexed evidence report: {link}")

    report = dict(navigation_pages=len(PAGES), local_links=local_links,
                  external_links_not_fetched=external_links, canonical_papers=len(catalog),
                  evidence_reports=len(evidence), failures=failures)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    report = check(root)
    output = root / "build/publication/navigation-report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
