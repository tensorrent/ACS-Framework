#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Issue #7 end-to-end verification pipeline.

Runs all issue scripts, captures stdout logs, computes checksums, validates
artifact consistency, and emits a machine-readable verification report.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
LOGS = DOCS / "issue7_logs"


@dataclass
class RunSpec:
    name: str
    script_rel: str
    stdout_rel: str


RUN_SPECS = [
    RunSpec(
        name="section9",
        script_rel="code/issue7/section9_toy_kill_test.py",
        stdout_rel="docs/issue7_logs/section9_stdout.txt",
    ),
    RunSpec(
        name="mechanism_4over3",
        script_rel="code/issue7/mechanism_4over3_test.py",
        stdout_rel="docs/issue7_logs/mechanism_4over3_stdout.txt",
    ),
    RunSpec(
        name="exhaustive",
        script_rel="code/issue7/exhaustive_issue7.py",
        stdout_rel="docs/issue7_logs/exhaustive_stdout.txt",
    ),
    RunSpec(
        name="cross_model",
        script_rel="code/issue7/cross_model_kill_pass.py",
        stdout_rel="docs/issue7_logs/cross_model_stdout.txt",
    ),
    RunSpec(
        name="long_range",
        script_rel="code/issue7/long_range_kill_pass.py",
        stdout_rel="docs/issue7_logs/long_range_stdout.txt",
    ),
    RunSpec(
        name="section9_exact",
        script_rel="code/issue7/section9_exact_kill_test.py",
        stdout_rel="docs/issue7_logs/section9_exact_stdout.txt",
    ),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def run_one(spec: RunSpec) -> dict[str, Any]:
    script = ROOT / spec.script_rel
    out = ROOT / spec.stdout_rel
    out.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    out.write_text(proc.stdout, encoding="utf-8")
    return {
        "name": spec.name,
        "script": str(script),
        "stdout_file": str(out),
        "exit_code": proc.returncode,
        "stdout_sha256": sha256_file(out),
        "stdout_lines": len(proc.stdout.splitlines()),
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_exhaustive_consistency(stdout_text: str, data: dict[str, Any]) -> list[str]:
    errs = []
    support_rate = data["section9_exhaustive"]["summary"]["support_rate"]
    spread = data["mechanism_4over3_exhaustive"]["normalization_robustness"]["finite_d_spread"]
    identity = data["mechanism_4over3_exhaustive"]["identity_check"]["all_hits_match_n_eq_d_plus_1"]
    if f"section9 support rate: {support_rate:.4f}" not in stdout_text:
        errs.append("exhaustive stdout support_rate mismatch")
    if f"4/3 inferred-d spread under scaling: {spread:.6f}" not in stdout_text:
        errs.append("exhaustive stdout spread mismatch")
    if f"4/3 exact-hit identity only (n=d+1): {identity}" not in stdout_text:
        errs.append("exhaustive stdout identity mismatch")
    return errs


def check_cross_model_consistency(stdout_text: str, data: dict[str, Any]) -> list[str]:
    errs = []
    tfim_rate = data["tfim"]["summary"]["support_rate"]
    xxz_rate = data["xxz"]["summary"]["support_rate"]
    sup = data["meta"]["combined_support_cases"]
    total = data["meta"]["combined_total_cases"]
    if f"TFIM support rate: {tfim_rate:.4f}" not in stdout_text:
        errs.append("cross-model stdout TFIM rate mismatch")
    if f"XXZ support rate:  {xxz_rate:.4f}" not in stdout_text:
        errs.append("cross-model stdout XXZ rate mismatch")
    if f"Combined support:  {sup}/{total}" not in stdout_text:
        errs.append("cross-model stdout combined mismatch")
    return errs


def check_long_range_consistency(stdout_text: str, data: dict[str, Any]) -> list[str]:
    errs = []
    for key, sweep in data["sweeps"].items():
        rate = sweep["summary"]["support_rate"]
        if f"{key} support rate: {rate:.4f}" not in stdout_text:
            errs.append(f"long-range stdout {key} rate mismatch")
    sup = data["meta"]["combined_support_cases"]
    total = data["meta"]["combined_total_cases"]
    if f"Combined support:  {sup}/{total}" not in stdout_text:
        errs.append("long-range stdout combined mismatch")
    return errs


def check_section9_exact_consistency(stdout_text: str, data: dict[str, Any]) -> list[str]:
    errs = []
    supports = data["summary"]["supports_chain"]
    sign_cw = data["summary"]["sign_cov_gap_cluster"]
    sign_leak = data["summary"]["sign_cov_gap_outside_affect"]
    if f"sign cov(gap, cluster_weight) = {sign_cw:+d}" not in stdout_text:
        errs.append("section9_exact stdout cluster cov sign mismatch")
    if f"sign cov(gap, outside_affect) = {sign_leak:+d}" not in stdout_text:
        errs.append("section9_exact stdout outside cov sign mismatch")
    expected = (
        "RESULT: exact data supports the chain direction."
        if supports
        else "RESULT: exact data does not support a robust monotone chain."
    )
    if expected not in stdout_text:
        errs.append("section9_exact stdout result line mismatch")
    if data.get("float_free") is not True:
        errs.append("section9_exact artifact missing float_free=true")
    return errs


def check_doc_hash_mentions(doc_text: str, hashes: dict[str, str]) -> list[str]:
    errs = []
    for rel, digest in hashes.items():
        if digest not in doc_text:
            errs.append(f"missing hash in doc for {rel}")
    return errs


def main() -> None:
    results = [run_one(spec) for spec in RUN_SPECS]
    run_failures = [r for r in results if r["exit_code"] != 0]

    exhaustive_json = DOCS / "issue7_exhaustive_results.json"
    cross_json = DOCS / "issue7_cross_model_results.json"
    long_range_json = DOCS / "issue7_long_range_results.json"
    exact_json = DOCS / "issue7_section9_exact_results.json"
    ex_data = load_json(exhaustive_json)
    cross_data = load_json(cross_json)
    long_range_data = load_json(long_range_json)
    exact_data = load_json(exact_json)

    stdout_map = {r["name"]: Path(r["stdout_file"]).read_text(encoding="utf-8") for r in results}

    consistency_errors = []
    consistency_errors.extend(check_exhaustive_consistency(stdout_map["exhaustive"], ex_data))
    consistency_errors.extend(check_cross_model_consistency(stdout_map["cross_model"], cross_data))
    consistency_errors.extend(check_long_range_consistency(stdout_map["long_range"], long_range_data))
    consistency_errors.extend(
        check_section9_exact_consistency(stdout_map["section9_exact"], exact_data)
    )

    hash_map = {
        "docs/issue7_exhaustive_results.json": sha256_file(exhaustive_json),
        "docs/issue7_cross_model_results.json": sha256_file(cross_json),
        "docs/issue7_long_range_results.json": sha256_file(long_range_json),
        "docs/issue7_section9_exact_results.json": sha256_file(exact_json),
        "docs/issue7_logs/long_range_stdout.txt": sha256_file(LOGS / "long_range_stdout.txt"),
        "docs/issue7_logs/section9_exact_stdout.txt": sha256_file(
            LOGS / "section9_exact_stdout.txt"
        ),
        "docs/issue7_logs/section9_stdout.txt": sha256_file(LOGS / "section9_stdout.txt"),
        "docs/issue7_logs/mechanism_4over3_stdout.txt": sha256_file(
            LOGS / "mechanism_4over3_stdout.txt"
        ),
        "docs/issue7_logs/exhaustive_stdout.txt": sha256_file(LOGS / "exhaustive_stdout.txt"),
        "docs/issue7_logs/cross_model_stdout.txt": sha256_file(LOGS / "cross_model_stdout.txt"),
    }
    docs_to_check = [
        DOCS / "issue7_takeup_section9_and_4over3.md",
        DOCS / "issue7_paper_section9_and_4over3.md",
    ]
    doc_errors = []
    for doc_path in docs_to_check:
        doc_text = doc_path.read_text(encoding="utf-8")
        missing = check_doc_hash_mentions(doc_text, hash_map)
        doc_errors.extend([f"{doc_path.name}: {item}" for item in missing])

    report = {
        "status": "PASS_WITH_CAUTION"
        if not run_failures and not consistency_errors and not doc_errors
        else "NEEDS_WORK",
        "runs": results,
        "consistency_errors": consistency_errors,
        "doc_errors": doc_errors,
        "hashes": hash_map,
        "warnings": [
            "Float NumPy Section 9 scripts remain single-platform anchored.",
            "Exact Section 9 kill test (Fraction/integer decision path) retires cross-machine drift for that diagnostic.",
            "Results are finite-model diagnostics, not universal no-go proofs.",
        ],
    }

    out_report = DOCS / "issue7_verification_report.json"
    out_report.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("Issue #7 verification pipeline complete")
    print(f"status: {report['status']}")
    print(f"runs_ok: {len(run_failures) == 0}")
    print(f"consistency_errors: {len(consistency_errors)}")
    print(f"doc_errors: {len(doc_errors)}")
    print(f"report: {out_report}")


if __name__ == "__main__":
    main()
