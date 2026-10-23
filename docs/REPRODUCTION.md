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
python gue_perturbation_sweep.py --quick
```

The form/function script also accepts `--full` for the dense GUE comparison. The GUE perturbation sweep reconstructs [Three-Layer Decomposition](../papers/later_FF06_series/Three_Layer_Decomposition.tex) §3. The paper does not state the matrix size, distance, diagonal scale or unfolding, so the script's docstring fixes them. `--quick` takes about a second. The default (N = 4000, 40 draws) has not been run; `--n 2000` took 16.5 minutes single-threaded. At N = 2000 no ε moved the spacings toward the zeros, but the §3 table's ε = 0.4 and ε = 0.8 "breaks" rows did not reproduce. Runtime and results depend on the selected sample and configuration. The first 100,000 zero ordinates are in [riemann_zeros_100k.txt](../code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt); read the [source/data audit](frontier/2026-09-12-source-delta/README.md) for provenance and precision limits. Several earlier stochastic studies use seed `20260423`; each experiment's actual recorded configuration is authoritative.

### Companion notes and frontier proofs

Return to the repository root before running:

```sh
python code/notes_verification/test_scaled_invariance.py
```

Use the [frontier verification guide](../code/frontier_verification/README.md) for its separate pinned Python dependencies, Lean versions, dependency locks, kernel checks, and negative controls.

## Find the evidence behind a result

Use the [condensate evidence index](CONDENSATE_EVIDENCE.md), [frontier index](frontier/README.md), and [claim-to-code manifest](../MANIFEST.md). An archived script may require its original environment or source data; the CI entry points above define the portable subset.

## Supporting papers whose instruments live in another repository

The two supporting papers under `docs/` ([surrogate discriminant amendments](surrogate_discriminant_amendments.tex), [instrument floors](instrument_floors.tex)) are reproduced from the public repository [tensorrent/AISO-UI-for-Ai](https://github.com/tensorrent/AISO-UI-for-Ai), not from `code/` here. Each paper's reproduction section names the branch, the pinned commit (at which the instrument files are byte-identical to the generating runs), and the commands, which run from that repository's `frontend/` directory after `npm install`. The committed figure data (`instrument_floors_data.tex`) is the generator's output at that pin, byte-for-byte. Promoting those instruments into `code/` here is an open owner decision recorded in the branch index.


## Records that depend on the authoring machine

*Added 23 October 2026, at commit `6d1647a`.* An inventory of what in this tree cannot be rerun, or cannot be resolved, on a machine other than the one it was authored on, and what each item needs. It is not the repository's policy on absolute paths in published receipts; that is an open owner decision ([decision brief 6](decisions_2026-10-22.md#6-absolute-path-exposure-one-policy-and-the-redaction-branch)). Found with `git grep -lI -e '/Users/' -e '/Volumes/' HEAD` (66 files, 32 of them in the publication manifest; this section adds one more) and by grepping for "local drive", "authoring machine" and `Aiso_build_artifacts`.

**Scripts that read an absolute path when run.** Each copies its sources into tracked snapshots and rewrites a tracked provenance file, so none should be run casually on any machine. Read from the code and not run: off the authoring machine each stops with `FileNotFoundError` at its first absolute path.

| Script | Reads | Needs | In the tree instead |
|---|---|---|---|
| `code/condensate_energy/endpoint_identifiability.py:28-29` | two files on the external drive mounted at `/Volumes/Seagate 4tb/` | that drive | snapshots in `docs/condensate_energy/endpoint_audit/source-snapshots/`, hashes in `endpoint_audit/provenance.json` |
| `code/condensate_energy/colour_singlet_boundary.py:14-16` | a recovered history text in the author's 23 September audit reports folder | that folder | `endpoint_audit/source-snapshots/newton_colour_music-1.py`, `endpoint_audit/colour-provenance.json` |
| `code/condensate_energy/microscopic_selector_boundary.py:27` | `ACS_Relational_Electrodynamics_Paper.md` from the author's `TR-2026-FF06-ACS` checkout | that checkout | `endpoint_audit/source-snapshots/`, `endpoint_audit/microscopic-provenance.json` |
| `code/condensate_energy/source_endpoint_algebra.py:20-22` | every `pending_sources` path in `docs/condensate_energy/source-reconciliation-20260924.json` (12 absolute: 1 on the external drive, 11 in the author's threshold-audit checkout) | the drive and that checkout | `docs/condensate_energy/source_endpoint/source-snapshots/`, `source_endpoint/provenance.json` |

All 21 absolute-source rows in those four provenance files have their snapshot committed, and every snapshot's sha256 matches its recorded hash (21 of 21, recomputed on 23 October 2026). What can be checked without the drive is therefore the bytes; what cannot be done is to re-read the originals.

**Preserved attempts and snapshots with absolute paths inside.** These are records, kept byte-for-byte, not entry points: `docs/condensate_energy/source_endpoint/attempts/higgs_potential/replay.py:35` and `attempts/koide_rg_flow/replay.py:405-406` write their figures to an absolute output folder in the author's checkout (an edit of that one path is needed to run them elsewhere); `docs/condensate_energy/endpoint_audit/attempts/phase6-timeout-60s/driver.py:27` has the same source list as `microscopic_selector_boundary.py`; `docs/condensate_energy/input_closure/source-snapshots/koide_from_vev.py:423` writes its results to the external drive.

**Instruments and trees outside this repository.**

- `code/benchmark_efficiency.py:32-44`: `Aiso_build_artifacts/` is the private AISO build tree, already marked external there and in `docs/EFFICIENCY_BENCHMARK_REPORT.md:81`; the memo root `.cache/` is local (`:15`). In a public checkout the script writes the tracked `docs/efficiency_benchmark_results.json` and `docs/EFFICIENCY_BENCHMARK_REPORT.md`.
- The canvases workspace: `build_canvas.py` under `Aiso_build_artifacts/eigen_path_daw_viz/`, `npm run typecheck` there, and the Canvas README links (`docs/BUGFIX_LOG.md:14, :48, :72-74`). Needs the workspace; already marked.
- FF06e's original form/function suite: `docs/Cross_Repo_Glossary_Extract.md:239` names `Math-grav-shared/scripts/knife_2x2.py`, which is not in this repository. The measurement table of `papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex` (`:81-93`) is rerun by `code/hp_knife_suite/ff06e_headline.py`, but its spacing-mean and counting witnesses are reconstructions, because the paper gives no formula for either; the original definitions need the suite from the author.
- The original Elimination-Ledger kill-test scripts (`/tmp/q3_floor.py`, `/tmp/q6_offdiag.py` and others on the authoring machine) are not committed. Three are re-authored and labelled RECONSTRUCTED in `code/hp_knife_suite/reconstructed/`; for the rest, [its table of what the owner must supply](../code/hp_knife_suite/reconstructed/README.md#not-reconstructed-what-the-owner-must-supply) names each file and what it unlocks.
- The two supporting papers' instruments live in AISO; see [the section above](#supporting-papers-whose-instruments-live-in-another-repository).

**Records whose provenance fields name the authoring machine.** Nothing to rerun; the paths record where the run's scripts and logs sat on the authoring machine, not anything a reader needs.

- `docs/issue7_verification_report.json` (12 paths, all under one checkout prefix; all 12 repo-relative equivalents are committed) and `docs/issue7_logs/{cross_model,exhaustive,long_range}_stdout.txt:5`. The pipeline has been rerun portably on Linux: [issue 7 replication, 22 October 2026](issue7_linux_replication/2026-10-22/README.md).
- Receipts and provenance under `docs/condensate_energy/` and `docs/frontier/2026-09-12-*/`, and `docs/ACS_Antigravity_Feed_Package/verification_report.json`. Sixteen of the receipt references are resolved by [the relocation map](publication/2026-09-24/receipt-relocations.json), which `scripts/verify_publication.py` reads; that file is load-bearing and must keep its absolute keys.
