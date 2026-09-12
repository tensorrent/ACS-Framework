# ACS Frontier verification instruments

These checks accompany the [12 September research delta](../../docs/frontier/2026-09-12-delta/README.md). The original three Lean files and dependency lock are copied unchanged from the Frontier evidence archive; `LFReal.lean` and `PerZeroBoundary.lean` are new formalizations. [Source_Manifest.json](proofs/Source_Manifest.json) distinguishes their provenance and fixes their hashes.

## Python checks

Use Python 3.12 and the pinned [requirements](requirements.txt) in an isolated environment. Run:

```sh
python lf_real_audit.py
python per_zero_boundary_audit.py
```

The first uses real-valued linear programming and a separate exact-rational primal/dual certificate. The second checks exact symbolic integrand identities, 70-digit numerical quadrature, finite-resolution error bounds, and moving-boundary counterexamples. JSON results are printed to standard output.

## Lean checks

The full project is pinned to [Lean 4.34.0-rc2](https://github.com/leanprover/lean4/releases/tag/v4.34.0-rc2) and the nine package revisions in [lake-manifest.json](proofs/lake-manifest.json). The two original standalone files also check under [Lean 4.15.0](https://github.com/leanprover/lean4/releases/tag/v4.15.0). Use the official binary for the desired platform; keep its `bin` directory on `PATH` when calling Lake.

From `proofs/`, obtain just the required modules with the locked project:

```sh
lake exe cache get Mathlib.Analysis.SpecialFunctions.Trigonometric.Arctan Mathlib.Analysis.SpecialFunctions.Log.Basic Mathlib.Topology.Algebra.Order.Field Mathlib.Order.Filter.AtTopBot.Field Mathlib.Tactic.Linarith Mathlib.Tactic.NormNum Mathlib.Basic.Real.Basic
```

`MATHLIB_CACHE_DIR` may point to a chosen workspace cache directory. Cache acquisition downloads dependencies; `audit_lean.py` itself performs no installations and verifies every checked-out revision against the lock.

From this directory, run the audit with a fresh output directory:

```sh
python audit_lean.py --bin /path/to/lean-4.34.0-rc2/bin --output /path/to/new-audit-directory
```

The audit checks five files, prints the public theorem axiom dependencies, rejects any `sorryAx` dependency in that output, and requires rejection of eleven altered mathematical statements. Each command and its output is recorded in an append-only event file. It verifies sources and the dependency lock before checking proofs. Source files are never altered; generated `.olean` files live under the ignored `.lake/` directory.

For the two original standalone proofs under the older runtime, use a separate output directory:

```sh
python audit_lean.py --bin /path/to/lean-4.15.0/bin --output /path/to/new-core-audit-directory --core-only
```

This checks those two proofs and four mutations without Mathlib. Version agreement is cross-version reproducibility, not a second independent implementation of Lean's kernel. Cached upstream dependencies remain part of the proof's declared trust base.

## Scope

Run `python verify_delta.py` to check the retained checkpoint's file hashes, evidence archives, event chain, branch coverage, receipts, and links. This integrity check performs no downloads and does not rerun the mathematical commands.

`LFReal.lean` proves the bound over arbitrary real probabilities and attainment in the explicitly defined positive-friend branch. It does not claim quantum realizability. `PerZeroBoundary.lean` proves a limit for the declared scalar formula along a moving ordinate; it does not establish zeta real-part identification or a natural spectral operator. The wider error bounds in the accompanying derivation remain analytical results with computational checks, rather than Lean integral/summation theorems.
