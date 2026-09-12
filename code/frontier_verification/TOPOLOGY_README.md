# Reproducing the Klein-cover correction

Use the same Lean 4.34.0-rc2 runtime, pinned Mathlib lock and Python requirements as the [first checkpoint](README.md). This audit adds [KleinLiftAudit.lean](proofs/KleinLiftAudit.lean) and retains [AxiomIII.lean](proofs/AxiomIII.lean) byte-for-byte. Hashes are in [Topology_Source_Manifest.json](proofs/Topology_Source_Manifest.json).

The proof needs `Mathlib.Tactic.Linarith`, `Mathlib.Tactic.NormNum`, and `Mathlib.Tactic.Ring`, already obtained by the preceding checkpoint's cache instructions. It does not require the aggregate `Mathlib.Tactic` module.

From this directory, run:

```sh
python audit_topology_lean.py --bin /path/to/lean-4.34.0-rc2/bin --output /path/to/new-topology-audit
python klein_lift_crosscheck.py
python verify_topology_delta.py
```

The formal audit uses a fresh output directory, verifies sources and nine dependency revisions, compiles the two modules, prints public theorem axiom dependencies, and rejects six false variants. It performs no downloads. The Python check uses exact integer/rational arithmetic and symbolic affine matrices. The final command verifies retained evidence and earlier checkpoint integrity; it does not rerun mathematics.

The resulting distinction is between a matrix invariant and the underlying mapping class. The Lean proof establishes a non-inner automorphism fixing the entire declared cover subgroup; the accompanying geometric construction connects it to the Klein-bottle diffeomorphism. No theorem here identifies homology action with isotopy class.
