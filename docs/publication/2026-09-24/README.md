# ACS publication update — 24 September 2026

This release amends all 33 canonical LaTeX manuscripts and adds two research papers, with 35 compiled PDFs. It publishes the scoped action-to-carrier investigation and its preserved evidence. It does not claim that RH, a complete microscopic theory of matter, or every ACS research program has been resolved.

## Read the consolidated results

- [Complete Scalar Actions and Identifiability Boundaries](../../../papers/updates/ACS_Action_Identifiability.pdf) — [LaTeX](../../../papers/updates/ACS_Action_Identifiability.tex). Defines the full scalar basis and kinetic metric, demonstrates hidden transverse instability, distinguishes radiative closure from parameter selection, and proves the conditional action-scale family.
- [Condensate Binding, Charge Protection, and the Boundary of Particle Identification](../../../papers/updates/ACS_Condensate_Carrier_Boundary.pdf) — [LaTeX](../../../papers/updates/ACS_Condensate_Carrier_Boundary.tex). Separates classical binding from physical particle identification and consolidates the charge, gauge-carrier, framing, capacitor, cover-map, state-space, color and torsion tests.
- [Paper-by-paper amendments](amendments.json), [original manuscript inventory](manuscript-baseline.json), and [style and literature review](style-and-research.md).
- [Archived endpoint and remaining inputs](../../condensate_energy/endpoint_audit/README.md). The historical endpoint records 95 passing checks and one incomplete full Phase-6 source replay. The independent exact two-root calculation does not turn that timeout into a successful replay.

## What changed scientifically

The full specified scalar sector has 68 real coordinates, 17 quartic coefficients and four quadratic coefficients. Six quartic directions disappear on the neutral family. Identical neutral observations coexist with stable, flat and unstable transverse spectra. Physical masses require the kinetic metric, and dimensionless structure leaves an overall physical scale undetermined. Finite RG flow retains measurable dependence on boundary data.

The binding calculation remains a conditional result for a specified scalar action. Charge breaking, additional gauge carriers and vacuum choices affect its physical interpretation. The revised corpus withdraws inference of `g=2` from framing, the balanced-triplet/singlet identification, and propagating torsion from the stated algebraic torsion-squared term. The capacitor proposal retains a free cutoff and contains the documented factor-of-two issue. Finite prime/zero statistics do not prove RH.

Every existing paper has a front status notice and a specific dated amendment. Directly contradictory passages in Papers A and C and the framing/Klein-foam abstracts are corrected. Earlier source snapshots and failed computations remain intact. An amendment is not a claim that every historical theorem, external citation or benchmark has received a new independent proof.

## Reproduce the publication checks

Use Python 3.12 with the pinned publication dependencies:

```sh
python -m pip install -r code/publication_20260924/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python scripts/verify_publication.py
python -m pytest -q code/acs_codebase/tests
python scripts/build_papers.py --jobs 2
```

The science driver runs 58 checks: exact restrictions and normalization, the complete stability counterfamily, generalized-coordinate invariance, independent finite differences, action/gauge/complex-flavor scale changes, conditional RG sensitivity, all real roots of the historical quartic proxy, and finite carrier counterexamples with positive controls. The existing canonical suite has 46 tests. These counts are software checks, not independent physical experiments.

The integrity pass verifies 516 hash references in the unchanged endpoint receipt. Sixteen absolute historical references are resolved through an explicit [relocation map](receipt-relocations.json) to byte-identical repository copies. A hash check demonstrates preservation, not the truth of the underlying claim. Original archive-recovery programs may still require the local drive; they are retained as provenance and are not the portable CI entry point.

The neutral-slice check uses the tangent pullback with `x26=d/sqrt(2)` and `x47=-d/sqrt(2)`. A principal five-coordinate block includes a transverse direction and incorrectly fails invariance. That historical failure and its correction were already recorded in [the numerical amendment](../../condensate_energy/canonical_vacuum/numerical-amendment.md); the publication rerun uses the actual four-coordinate tangent.

GitHub Actions has separate scientific-verification and all-manuscript build jobs, also callable manually. It uploads reports and PDFs. Builds fail on compilation errors, missing glyphs and unresolved references/citations. Formatting diagnostics and visual inspection are recorded separately. CI never rewrites archived evidence or commits generated files.

## Provenance and scope

The publication branch starts at reviewed commit `173398ba4e5453f9c2162f52551f925f9a16104a`; remote main was `56f7b2f` at preflight. The five intervening frontier commits retain the integral, mean-error, topology and source corrections. Concurrent later work on other remote branches is not silently merged into this release.

The complete `code/condensate_energy` and `docs/condensate_energy` trees were imported unchanged from the research checkout. Raw chat stores, unrelated projects and the much larger witness-data collection were not imported. The source-only corrections for Paper B and the fibered-line note were reconciled before the new amendments. The [publication manifest](publication-manifest.json) binds the reviewed paper/PDF and evidence files.

Brad Wallace's sole intellectual authorship and the Sovereign Integrity Protocol License v1.1 are preserved. All novel theories, models, and hypotheses represent approximately 5,000–6,000 hours of independent work by the author, who navigates dyslexia and ADHD. An "Analog Mixture-of-Experts" (MoE) AI ensemble (GPT, Claude, Grok, DeepSeek, Gemini, Cursor, Antigravity) was directed by the author strictly via voice-to-text intake, rapid transcription, and adversarial multi-model cross-examination. No external peer review or experimental confirmation is implied.
