#!/usr/bin/env python3
"""
Yang-Mills Mass Gap Construction Comparison Checker.
Compares a target mathematical document (plain text, LaTeX, or PDF)
against the pre-registered predictions (C1-C6, X1-X2) from the sealed document.
"""

import os
import sys
import re
import argparse
from typing import Dict, List, Any, Tuple

# Pre-registered predictions keywords and definitions
PREDICTIONS = {
    "C1": {
        "title": "Casimir Gap (Kinematic Resolution)",
        "desc": "At any finite resolution the gap is kinematic — compactness of the gauge group makes the electric spectrum discrete.",
        "must_have": ["Casimir", "discrete", "compact"],
        "should_have": ["plaquette", "gauge group", "electric spectrum", "kinematic", "spectrum", "Casimir gap"]
    },
    "C2": {
        "title": "Survival Theorem (Refinement Transport)",
        "desc": "The proof is a survival theorem showing the physical gap does not close along the coherent refinement path (volume up, spacing down).",
        "must_have": ["refinement", "survive", "limit"],
        "should_have": ["monotonicity", "coherent refinement", "survival", "does not close", "spacing", "refinement path"]
    },
    "C3": {
        "title": "Massless-Gluon Obstruction Projection",
        "desc": "Masslessness is a gauge-variant propagator artifact; the proof operates inside gauge-invariant algebras, excluding it by construction.",
        "must_have": ["gauge-invariant", "massless", "propagator"],
        "should_have": ["gauge invariant", "artifact", "algebra", "excluding", "by construction", "gluon"]
    },
    "C4": {
        "title": "One-Channel Law (0++ Plaquette)",
        "desc": "The quantitative bound lives in one invariant channel (0++ plaquette correlation length / transfer-matrix).",
        "must_have": ["channel", "correlation"],
        "should_have": ["0++", "plaquette", "transfer-matrix", "transfer matrix", "correlation length", "invariant channel"]
    },
    "C5": {
        "title": "Exchange of Limits (Cutoff Uniformity)",
        "desc": "Exchange of limits (weak coupling vs infinite volume) is resolved via uniform, frame-independent bounds carrying no cutoff dependence.",
        "must_have": ["limits", "cutoff", "uniform"],
        "should_have": ["exchange of limits", "infinite volume", "weak coupling", "bounds", "frame-independent", "dependence"]
    },
    "C6": {
        "title": "Constructive Proof Form",
        "desc": "Constructive proof exhibiting vacuum + gap via reflection positivity + uniform correlation-length estimate (not existence-only).",
        "must_have": ["constructive", "positivity"],
        "should_have": ["reflection positivity", "vacuum", "stability bound", "estimate", "existence-only", "reflection-positivity"]
    },
    "X1": {
        "title": "Wilson-Type Algebras Admissibility",
        "desc": "Refinement transport between nested Wilson-type algebras; admissibility control.",
        "must_have": ["Wilson", "algebra"],
        "should_have": ["Wilson-type", "admissibility", "nested", "refinement transport"]
    },
    "X2": {
        "title": "Observable Algebra Pivot (AQFT)",
        "desc": "Operates inside AQFT or observable algebra representation rather than gauge fields.",
        "must_have": ["AQFT", "observable"],
        "should_have": ["algebra", "representation", "observables"]
    }
}


def install_pypdf():
    print("[*] PDF targeted, checking for pypdf...")
    try:
        import pypdf
        return True
    except ImportError:
        print("[!] pypdf library is missing. Attempting auto-installation...")
        import subprocess
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pypdf"], check=True)
            print("[+] pypdf installed successfully.")
            return True
        except Exception as e:
            print(f"[-] Failed to install pypdf: {e}")
            print("[-] Please install pypdf manually or convert the PDF to text first.")
            return False


def extract_text_from_pdf(pdf_path: str) -> str:
    if not install_pypdf():
        sys.exit(1)
    import pypdf
    print(f"[*] Extracting text from PDF: {pdf_path}")
    text = []
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        total_pages = len(reader.pages)
        print(f"[*] Total pages to parse: {total_pages}")
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                # Insert page marker
                text.append(f"\n--- PAGE {i+1} ---\n{page_text}")
    return "\n".join(text)


def extract_text_from_directory(dir_path: str) -> str:
    print(f"[*] Scanning directory recursively: {dir_path}")
    combined_text = []
    extensions = (".tex", ".txt", ".md", ".json", ".py", ".html", ".pdf")
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith(extensions):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, dir_path)
                if file.lower().endswith(".pdf"):
                    content = extract_text_from_pdf(full_path)
                else:
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                    except Exception as e:
                        print(f"[!] Could not read {full_path}: {e}")
                        continue
                combined_text.append(f"\n=== FILE: {rel_path} ===\n{content}")
    return "\n".join(combined_text)


def analyze_matches(text: str) -> Dict[str, Any]:
    results = {}
    
    # Pre-process text to remove extra whitespace and lowercase it for matching
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text_lower = cleaned_text.lower()
    
    # We will search using sliding windows of ~150 words to detect co-occurrence of terms
    words = cleaned_text.split(' ')
    window_size = 150
    step_size = 50
    
    for key, spec in PREDICTIONS.items():
        best_score = 0
        best_snippet = "No matching context found."
        best_location = "N/A"
        
        must_terms = [t.lower() for t in spec["must_have"]]
        should_terms = [t.lower() for t in spec["should_have"]]
        
        # Scan sliding windows
        for idx in range(0, max(1, len(words) - window_size), step_size):
            window_words = words[idx:idx + window_size]
            window_text = " ".join(window_words)
            window_text_lower = window_text.lower()
            
            # Check must-have terms
            must_hits = sum(1 for term in must_terms if term in window_text_lower)
            # Check should-have terms
            should_hits = sum(1 for term in should_terms if term in window_text_lower)
            
            if must_hits >= 1:
                # Calculate a density score
                score = (must_hits / len(must_terms)) * 0.6 + (should_hits / len(should_terms)) * 0.4
                if score > best_score:
                    best_score = score
                    best_snippet = f"... {window_text[:300]} ..."
                    
                    # Try to locate page/file markers in preceding text
                    preceding_text = " ".join(words[max(0, idx-500):idx])
                    file_markers = re.findall(r'=== FILE: (.*?) ===', preceding_text)
                    page_markers = re.findall(r'--- PAGE (\d+) ---', preceding_text)
                    
                    file_loc = file_markers[-1] if file_markers else "Unknown File"
                    page_loc = f"Page {page_markers[-1]}" if page_markers else ""
                    best_location = f"{file_loc} {page_loc}".strip()

        # Classify verdict
        if best_score >= 0.7:
            verdict = "MATCH"
        elif best_score >= 0.25:
            verdict = "PARTIAL"
        else:
            verdict = "MISS"
            
        results[key] = {
            "title": spec["title"],
            "desc": spec["desc"],
            "verdict": verdict,
            "score": best_score,
            "location": best_location,
            "snippet": best_snippet
        }
        
    return results


def generate_report(results: Dict[str, Any], output_path: str):
    report_md = []
    report_md.append("# Yang-Mills Construction Comparison Report")
    report_md.append("Generated automatically by `ym_comparison_checker.py`.\n")
    
    report_md.append("## 1. Summary Scorecard\n")
    report_md.append("| ID | Prediction Title | Verdict | Confidence | Location |")
    report_md.append("|---|---|---|---|---|")
    
    match_count = 0
    partial_count = 0
    miss_count = 0
    
    for key, val in results.items():
        color_verdict = f"**{val['verdict']}**"
        if val['verdict'] == "MATCH":
            match_count += 1
        elif val['verdict'] == "PARTIAL":
            partial_count += 1
        else:
            miss_count += 1
        report_md.append(f"| {key} | {val['title']} | {color_verdict} | {val['score']*100:.1f}% | {val['location']} |")
        
    report_md.append(f"\n**Totals**: {match_count} MATCHES, {partial_count} PARTIALS, {miss_count} MISSES.\n")
    
    report_md.append("## 2. Detailed Findings\n")
    for key, val in results.items():
        report_md.append(f"### {key}: {val['title']}")
        report_md.append(f"* **Pre-registered Spec**: {val['desc']}")
        report_md.append(f"* **Verdict**: **{val['verdict']}** (Confidence: {val['score']*100:.1f}%)")
        report_md.append(f"* **Location**: `{val['location']}`")
        report_md.append(f"* **Matched Passage**:")
        report_md.append(f"  ```\n  {val['snippet']}\n  ```\n")
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_md))
    print(f"[+] Detailed comparison report written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Yang-Mills Construction Comparison Checker")
    parser.add_argument("target", help="Path to Graviton's work (directory, .tex, .txt, or .pdf)")
    parser.add_argument("--sealed_spec", default=None, help="Path to sealed predictions document")
    parser.add_argument("--output", default="docs/YM_COMPARISON_REPORT.md", help="Output path for the comparison report")
    args = parser.parse_args()
    
    print("=== YANG-MILLS COMPARISON CHECKER ===")
    
    if not os.path.exists(args.target):
        print(f"[-] Target path does not exist: {args.target}")
        sys.exit(1)
        
    # Extract text from target
    if os.path.isdir(args.target):
        text = extract_text_from_directory(args.target)
    elif args.target.lower().endswith(".pdf"):
        text = extract_text_from_pdf(args.target)
    else:
        try:
            with open(args.target, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            print(f"[-] Error reading file: {e}")
            sys.exit(1)
            
    print(f"[+] Loaded {len(text)} characters of text from target.")
    
    # Run analysis
    print("[*] Running semantic prediction matcher...")
    results = analyze_matches(text)
    
    # Output console summary
    print("\n" + "="*50)
    print("COMPARISON RESULTS SUMMARY")
    print("="*50)
    for key, val in results.items():
        print(f"[{val['verdict']:<7}] {key}: {val['title']} ({val['score']*100:.1f}%)")
    print("="*50 + "\n")
    
    # Generate markdown report
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    generate_report(results, args.output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
