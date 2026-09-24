# Interpretation corrections for retained proof sources

`AxiomIII.lean` is preserved byte-for-byte for provenance and reproducibility. Its matrix theorems pass the kernel, but two comments overstate their topological meaning:

- Line 116 identifies four possible lift matrices with the image of the Klein mapping class group. The canonical orientation-preserving lift has image `{I,-I}` and a nontrivial kernel.
- Lines 131–132 infer the trivial mapping class from the identity matrix. The half-translation gives a nontrivial Dehn-twist class with identity cover homology and trace two.

The parabolic shear obstruction remains valid. Read the [full correction and evidence](../../../docs/frontier/2026-09-12-topology-delta/README.md) and [KleinLiftAudit.lean](KleinLiftAudit.lean) before using the archived comments to interpret the matrix results.
