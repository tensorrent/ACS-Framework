# Reproducing the integral and error delta

This continuation uses the same Lean 4.34.0-rc2 runtime and nine locked dependencies as the [first checkpoint](README.md). The three new files and their unchanged dependency are pinned by [Integral_Source_Manifest.json](proofs/Integral_Source_Manifest.json).

With the matching runtime's `bin` on `PATH`, run this from `proofs/` to acquire the additional integration modules:

```sh
lake exe cache get Mathlib.Analysis.SpecialFunctions.Integrals.Basic Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
```

Follow the first checkpoint's cache instructions as well when preparing a fresh project. `MATHLIB_CACHE_DIR` can select a workspace cache. From this directory, run:

```sh
python audit_integral_lean.py --bin /path/to/lean-4.34.0-rc2/bin --output /path/to/new-integral-audit
python integral_crosscheck.py
python verify_integral_delta.py
```

The first command verifies the source hashes and checked-out dependency revisions, compiles `PerZero` followed by the three new modules, prints all public theorem axiom dependencies, and requires seven false mathematical mutations to fail. It performs no installations. Use a fresh audit directory. These modules require Mathlib; the standalone core-only mode is unsupported.

The second command uses the existing pinned Python requirements. It checks the complex integrand algebra, directly evaluates separate complex integrals and the paired integrand, and exercises finite-configuration estimates. The last command checks the retained package and preceding checkpoint, without rerunning the mathematics or accessing the network.

The dependency library's integration identity is in the pinned `Mathlib/Analysis/SpecialFunctions/Integrals/Basic.lean`; interval-integral comparison and translation are in `Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean`. Their use is visible in the proof source. Cached imported dependencies remain part of the declared trust base.
