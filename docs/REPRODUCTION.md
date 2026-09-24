# Reproduction guide

[Repository home](../README.md) · [Documentation](README.md) · [Code guide](../code/README.md) · [Paper catalog](../papers/README.md)

Run commands from the repository root unless a section changes directory. Use a fresh Python 3.12 virtual environment for the portable publication checks.

## Portable publication checks

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r code/publication_20260924/requirements.txt
python scripts/check_navigation.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python scripts/verify_publication.py
python -m pytest -q code/acs_codebase/tests
```

The publication's recorded baseline is 58 fresh scientific checks and 46 canonical tests. The integrity pass validates the 35-paper inventory, 33 amendment markers, and 516 references in the preserved endpoint receipt. Reports are written under the ignored `build/publication/` directory.

For preservation checks without running the science driver:

```sh
python scripts/verify_publication.py --integrity-only
```

The [publication record](publication/2026-09-24/README.md) specifies what was rerun and what was only hash-checked. In particular, the historical Phase-6 full source replay timeout remains recorded; the separate exact-root check does not erase it.

## Build the manuscripts

Install [Tectonic 0.17.0 from its official release](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0) and ensure `tectonic` is on `PATH`.

```sh
python scripts/build_papers.py --jobs 2
```

This builds every canonical document under `papers/`, writes PDFs and logs to `build/publication/`, and fails on compilation errors, missing glyphs, or unresolved references/citations. The first build downloads TeX resources. Width warnings require a separate visual review; build success alone does not verify layout or scientific claims.

For one paper:

```sh
python scripts/build_papers.py --paper papers/updates/ACS_Action_Identifiability.tex
```

`--update-pdfs` replaces the committed PDF copies and is intended for a reviewed publication update. The dated publication manifest binds source and PDF bytes; changing either requires a deliberate new preservation record, not an automatic rewrite of historical hashes.

The [GitHub Actions workflow](../.github/workflows/publication.yml) runs on pushes to `main` and `codex/**`, pull requests, and manual dispatch. It uploads build and scientific reports. The supporting Yang–Mills comparison document in `docs/` is outside this canonical build inventory.

## Optional research suites

These commands are inherited research entry points, not additional passes claimed by the navigation audit. Consult each paper's amendment and the relevant artifact receipt first.

### Core package and heritage scripts

The [core package guide](../code/acs_codebase/README.md) describes `verify_all.sh`, which adds paper-level checks to pytest. [The extras guide](../code/acs_codebase/extras/README.md) distinguishes curated examples from heritage material.

```sh
python code/acs_codebase/extras/barbero_immirzi_correct.py
python code/acs_codebase/extras/koide_clebsch_gordan.py
python code/acs_codebase/extras/higgs_mass_ratio.py
```

Interpret these carefully: the first uses unconstrained state counting; the second reports that the chirality map does not derive the observed angle; the third's close mass-ratio match was selected by a candidate search. A numerical fit is not a derivation.

### Prime and zero instruments

```sh
cd code/hp_knife_suite
python hp_never_synced.py
python hp_xp_test.py
python hp_signed_lfunction.py
python hp_phase_test.py
python hp_form_function_relativity.py
```

The form/function script also accepts `--full` for the dense GUE comparison. Runtime and results depend on the selected sample and configuration. The first 100,000 zero ordinates are in [riemann_zeros_100k.txt](../code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt); read the [source/data audit](frontier/2026-09-12-source-delta/README.md) for provenance and precision limits. Several earlier stochastic studies use seed `20260423`; each experiment's actual recorded configuration is authoritative.

### Companion notes and frontier proofs

Return to the repository root before running:

```sh
python code/notes_verification/test_scaled_invariance.py
```

Use the [frontier verification guide](../code/frontier_verification/README.md) for its separate pinned Python dependencies, Lean versions, dependency locks, kernel checks, and negative controls.

## Find the evidence behind a result

Use the [condensate evidence index](CONDENSATE_EVIDENCE.md), [frontier index](frontier/README.md), and [claim-to-code manifest](../MANIFEST.md). An archived script may require its original environment or source data; the CI entry points above define the portable subset.
