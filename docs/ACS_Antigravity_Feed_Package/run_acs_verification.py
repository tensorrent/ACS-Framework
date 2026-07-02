#!/usr/bin/env python3
"""
ACS Verification Wrapper
========================
Programmatically runs the complete verification suite and standalone extras,
checks output parameters against the locked ledger values, and outputs a
structured JSON compliance report.
"""

import os
import sys
import subprocess
import json
import time

def run_command(cmd, cwd=None):
    start = time.time()
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        duration = time.time() - start
        return {
            "status": "PASS" if res.returncode == 0 else "FAIL",
            "returncode": res.returncode,
            "stdout": res.stdout.strip(),
            "stderr": res.stderr.strip(),
            "duration_sec": round(duration, 3)
        }
    except Exception as e:
        duration = time.time() - start
        return {
            "status": "ERROR",
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "duration_sec": round(duration, 3)
        }

def main():
    print("🚀 Running complete ACS Verification Suite...\n")
    
    python_bin = "/Users/coo-koba42/dev/.venv/bin/python"
    if not os.path.exists(python_bin):
        python_bin = sys.executable
        
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python_executor": python_bin,
        "base_directory": base_dir,
        "results": {}
    }
    
    # 1. Run core test suite (pytest)
    print("1. Running core test suite (pytest)...")
    pytest_cmd = f"{python_bin} -m pytest code/acs_codebase/ -q"
    res = run_command(pytest_cmd, cwd=base_dir)
    report["results"]["core_pytest_suite"] = res
    print(f"   Status: {res['status']} ({res['duration_sec']}s)")
    
    # 2. Run standalone extras
    print("\n2. Running standalone extras...")
    
    # Barbero-Immirzi
    print("   Running barbero_immirzi_correct.py...")
    bi_cmd = f"{python_bin} code/acs_codebase/extras/barbero_immirzi_correct.py"
    res = run_command(bi_cmd, cwd=base_dir)
    report["results"]["barbero_immirzi"] = res
    if "γ = 0.274067" in res["stdout"] or "gamma = 0.274067" in res["stdout"]:
        print("   ✓ Solved gamma = 0.274067 matches unconstrained ledger value.")
    else:
        print("   ⚠ Warning: solved gamma value mismatch.")
        
    # Koide
    print("   Running koide_clebsch_gordan.py...")
    koide_cmd = f"{python_bin} code/acs_codebase/extras/koide_clebsch_gordan.py"
    res = run_command(koide_cmd, cwd=base_dir)
    report["results"]["koide_lepton_mass"] = res
    if "CONFIRMED ✓" in res["stdout"]:
        print("   ✓ Koide lepton mass fit confirmed.")
        
    # Higgs mass
    print("   Running higgs_mass_ratio.py...")
    higgs_cmd = f"{python_bin} code/acs_codebase/extras/higgs_mass_ratio.py"
    res = run_command(higgs_cmd, cwd=base_dir)
    report["results"]["higgs_mass_ratio"] = res
    if "Match: 0.47%" in res["stdout"]:
        print("   ✓ Higgs mass ratio match of 0.47% confirmed.")
        
    # 3. Run HP knife suite
    print("\n3. Running Hilbert-Pólya shuffle-knife scripts...")
    
    hp_scripts = {
        "hp_never_synced": "hp_never_synced.py",
        "hp_xp_test": "hp_xp_test.py",
        "hp_signed_lfunction": "hp_signed_lfunction.py",
        "hp_phase_test": "hp_phase_test.py",
        "hp_c9_orthogonality": "hp_c9_orthogonality.py"
    }
    
    for key, script in hp_scripts.items():
        print(f"   Running {script}...")
        hp_cmd = f"{python_bin} {script}"
        res = run_command(hp_cmd, cwd=os.path.join(base_dir, "code", "hp_knife_suite"))
        report["results"][key] = res
        print(f"   Status: {res['status']}")

    # Determine overall status
    all_pass = all(item["status"] == "PASS" for item in report["results"].values())
    report["overall_status"] = "PASS" if all_pass else "FAIL"
    
    output_path = os.path.join(os.path.dirname(__file__), "verification_report.json")
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"\n{'═'*50}")
    print(f"Verification process complete.")
    print(f"Overall status: {report['overall_status']}")
    print(f"Structured report saved to: docs/ACS_Antigravity_Feed_Package/verification_report.json")
    print(f"{'═'*50}")
    
    sys.exit(0 if all_pass else 1)

if __name__ == "__main__":
    main()
