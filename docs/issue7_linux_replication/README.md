# Issue 7 float-suite second-platform replication (Linux)

**Date:** 2026-08-07
**Environment:** Linux x86_64 (glibc 2.39), Python 3.11.15, NumPy 2.4.6
(reference environment for the committed anchors: macOS 15.3.2 arm64, Python 3.14.6, NumPy 2.5.0)

The Section 9 / 4-over-3 kill suite was rerun on this second platform to address the
single-platform-anchoring limitation recorded in
`papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex` (Limitations).

## Results

- **Exact-arithmetic scripts** (`section9_exact_kill_test.py`): output artifact is
  **byte-identical** to the committed macOS artifact
  (`docs/issue7_section9_exact_results.json`), as expected for integer/`Fraction`
  decision paths.
- **Float NumPy scripts** (`section9_toy_kill_test.py`, `mechanism_4over3_test.py`,
  `cross_model_kill_pass.py`, `long_range_kill_pass.py`): every decision-level output
  (`supports_chain` booleans, support rates, RESULT lines) **matches the committed
  macOS artifacts exactly**; floating-point values agree to ~1e-12 or better (IEEE
  last-bit drift only). The Linux artifacts committed alongside this note:
  - `issue7_cross_model_results.json` (verdicts identical; XXZ support 0.1667, combined 1/12)
  - `issue7_long_range_results.json` (verdicts identical; alpha_2 support 0.5000, combined 5/12)

  The exact-arithmetic artifact is not duplicated here because it is byte-identical
  to the committed `docs/issue7_section9_exact_results.json`.

## Reading

The committed SHA-256 anchors remain macOS-specific (byte-identical hashes do not
transfer across platforms for float outputs); this replication establishes the
**tolerance-based** cross-platform anchor the paper's Limitations section called for:
the falsification verdicts are platform-independent at the decision level.
`verify_issue7_pipeline.py` (the full re-run wrapper) was not exercised to completion
on this platform (wall-clock bound); the individual kill scripts above were.
