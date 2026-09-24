# Reproducing the source and data audit

The retained runtime is Python 3.12.14 with versions in [source_requirements.txt](source_requirements.txt). The [source/data checkpoint](../../docs/frontier/2026-09-12-source-delta/README.md) includes primary table downloads, complete baseline source snapshots, corrected files, command output, dependency versions, and an append-only queue.

Extract `Primary_Tables.zip` into a directory supplied as `--primary`; the ZIP contains `zeros1`, `zeros2`, and `zeros6.gz` at its root. No network access is needed for the checks. From this directory, run:

```sh
python -m pip install -r source_requirements.txt
python dataset_precision_audit.py --primary /path/to/extracted-tables --output /path/to/new-results
python normalization_crosscheck.py
python -m pytest ../acs_codebase/tests -v
python verify_source_delta.py
```

The first audit verifies primary hashes and source identity, compares selected zero ordinates using Arb and mpmath, computes 12 finite error enclosures, certifies four well-separated endpoint counts, and exercises 12 endpoint-precision cases. It carries the provider's stated input uncertainty; it does not prove all supplied ordinates correct. The second audit independently checks the corrected finite normalized sum at 70-digit precision. Pytest covers the canonical appendix and four added overflow regressions. These commands do not execute the exploratory script pool or train a model.

For exact historical reproduction after the live code has changed, extract `Source_Snapshot.zip`, copy the contents of `baseline/` into a fresh working directory, overlay `corrected/`, then overlay `instruments/`. That reconstructs the recorded code and audit instruments with their repository-relative paths. The original source plus the new regression test can be reconstructed by restoring just the baseline `renormalized_stability.py`; two of the four overflow cases should fail. Never overwrite a working checkout to reconstruct a historical run.

The final integrity command uses archived source identities for mutable implementation files. It verifies receipts and all preceding Frontier checkpoints, without rerunning mathematics or downloading sources. Source-map availability checks refer to the recorded revision; their missing-input findings are not permanent claims about later revisions.
