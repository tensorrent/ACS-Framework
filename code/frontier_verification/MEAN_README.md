# Reproducing the mean-error continuation

Use the Lean 4.34.0-rc2 runtime, pinned Mathlib dependencies, and Python requirements from the [first checkpoint](README.md), with the additional cached imports listed in [INTEGRAL_README.md](INTEGRAL_README.md). This pass adds [PerZeroMean.lean](proofs/PerZeroMean.lean) and [PerZeroCounterfamily.lean](proofs/PerZeroCounterfamily.lean); preceding proofs and their manifests remain unchanged. The complete input hashes are in [Mean_Source_Manifest.json](proofs/Mean_Source_Manifest.json).

From this directory, run:

```sh
python audit_mean_lean.py --bin /path/to/lean-4.34.0-rc2/bin --output /path/to/new-mean-audit
python mean_crosscheck.py
python verify_mean_delta.py
```

The audit verifies the source and project hashes and all nine dependency revisions, compiles six modules in dependency order, prints public theorem axiom dependencies, and rejects eight semantic mutations. It requires a prepared project and makes no downloads. All six `.lean` files must be present if passing a separate `--project` directory.

The Python check independently evaluates symbolic limits and a series, exact rational layer counts, and numerical scalar deficits. It reuses `integral_crosscheck.direct` to evaluate the paired complex resolvents and the difference of separately integrated resolvents. It covers synthetic configurations, including repeated ordinates. Neither these samples nor the finite indexed counterfamily assert a result for an actual-zero dataset.

The final command verifies retained receipts, source hashes, archives, links, queue continuity, the append-only event chain, and all preceding checkpoint manifests. It does not rerun the mathematical checks. The frozen [mean-error checkpoint](../../docs/frontier/2026-09-12-mean-delta/README.md) distinguishes the arbitrary-filter theorem from finite cross-checks and records the remaining gates.
