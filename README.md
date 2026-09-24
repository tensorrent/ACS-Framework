# ACS Framework

Asymmetric Codependent Systems: research manuscripts, mathematical notes, computational checks, and preserved experimental records.

## Start here

- **Read the current findings:** [24 September publication](docs/publication/2026-09-24/README.md) — two consolidated papers, amendments to 33 earlier manuscripts, and the verification record.
- **Find a paper:** [complete paper catalog](papers/README.md) — all 35 canonical manuscripts, with direct PDF and LaTeX links, grouped by topic.
- **Explore the evidence:** [documentation index](docs/README.md) — current results, historical records, corrections, and research queues.
- **Run the checks:** [reproduction guide](docs/REPRODUCTION.md) and [code directory guide](code/README.md).
- **Find unfinished work:** [branch index and cleanup audit](docs/BRANCHES.md) — open PRs, unmerged research, and recoverable retired branches.

## Current publication

The [publication merged in PR #17](https://github.com/tensorrent/ACS-Framework/pull/17) includes **35 compiled PDFs**, **58 fresh scientific checks**, **46 canonical tests**, and **516 verified evidence references**. These are scoped software and preservation checks, not independent physical experiments.

The two new papers cover [scalar-action identifiability](papers/updates/ACS_Action_Identifiability.pdf) and [condensate binding and particle-identification limits](papers/updates/ACS_Condensate_Carrier_Boundary.pdf). Read their hypotheses and the dated amendments before relying on earlier claims. The historical full Phase-6 source replay remains incomplete; a passing exact-root calculation does not replace that replay.

[GitHub Actions](https://github.com/tensorrent/ACS-Framework/actions/workflows/publication.yml) checks navigation, evidence integrity, scientific results, and manuscript builds. Its reports and compiled PDFs are downloadable from each successful run. The committed PDFs remain available in the paper catalog.

## Research status

ACS is an active research program. This repository does not establish the Riemann Hypothesis or a complete physical theory. The current publication separates conditional results, fitted or free inputs, counterexamples, and identification limits.

Use the [claim-to-code manifest](MANIFEST.md), [glossary](GLOSSARY.md), and [elimination ledger](docs/Elimination_Ledger.md) alongside the latest amendments. The [historical corpus map](docs/ACS_Corpus_Map.md) and [May 2026 page index](docs/ACS_Master_Index.md) describe earlier snapshots; their counts and status labels are not the current publication inventory.

## Repository map

- [papers/](papers/README.md) — canonical manuscripts and PDFs; Markdown mirrors are secondary.
- [docs/](docs/README.md) — findings, audits, receipts, historical records, and navigation.
- [code/](code/README.md) — portable checks and specialized research instruments.
- [scripts/](scripts/) — manuscript builds, publication verification, navigation checks, and supporting utilities.
- [harness/training/](harness/training/README.md) — training and telemetry experiments.
- [visualizations/](visualizations/README.md) — interactive models.
- [MANIFEST.md](MANIFEST.md) and [GLOSSARY.md](GLOSSARY.md) — claim mapping and terminology.

Existing source and evidence paths are retained so citations and receipt hashes continue to resolve. Active research branches are cataloged separately from the published `main` branch.

## Quick verification

From the repository root, in a Python 3.12 virtual environment:

```sh
python -m pip install -r code/publication_20260924/requirements.txt
python scripts/check_navigation.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python scripts/verify_publication.py
python -m pytest -q code/acs_codebase/tests
```

To rebuild the papers, install Tectonic 0.17.0 and run `python scripts/build_papers.py --jobs 2`. See the [reproduction guide](docs/REPRODUCTION.md) for outputs, archived experiments, and optional suites.

## Citation and license

Authorship and citation metadata are in [CITATION.cff](CITATION.cff). The repository uses the [Sovereign Integrity Protocol License v1.1](LICENSE); see also the [paper licensing note](papers/LICENSE-PAPERS.md). The new consolidations disclose AI-assisted drafting and checking. Publication here does not imply external peer review.
