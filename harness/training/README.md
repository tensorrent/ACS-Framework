> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# `harness/training/` — Phase-1 unified trainer

This directory holds the NumPy-only Phase-1 training harness used to produce the
MMLU + GSM8K telemetry numbers quoted elsewhere in the ACS corpus. It is a
**self-contained training/analysis utility**, not part of the mathematical
verification suite under `code/` — nothing in `papers/` depends on it.

Everything below is run from the repository root, and every path is
repo-relative. All four files in this directory are listed; there are no others.

## What is here

| File | What it does |
|---|---|
| `train_unified_phase1.py` | The trainer: shared encoder with an MMLU head (4-way multiple choice) and a GSM8K head (operation classification plus a scalar numeric head for final-answer regression). NumPy only. |
| `scrape_telemetry_metrics.py` | Reads `report.json` files produced by trainer runs and prints a telemetry table (`telemetry_row_frac`, `telemetry_aux_mean_abs`, `telemetry_aux_to_base_ratio`). |
| `run_phase1_tune_batch.sh` | Multi-seed stability barrage over the trainer: fixed hyperparameters, `residual_product` numeric head, auto LR decay. Tunable through environment variables documented in the script header. |
| `run_phase1_phase_d_telemetry_sweep.sh` | Phase-D sweep: calls `run_phase1_tune_batch.sh` once per telemetry auxiliary weight (`0.03`, `0.05`, `0.1`). |

## Data is not shipped

The trainer's default input paths are `harness/fixtures/training/*.jsonl`
(`mmlu_train`, `mmlu_test`, `gsm8k_train`, `gsm8k_test`) and its default output
directory is `harness/reports/training/`. **Neither directory is included in this
repository** — the corpora and the recorded run artifacts live outside it. To use
the trainer you must supply your own JSONL corpora and point the flags at them:

```bash
python3 harness/training/train_unified_phase1.py \
  --mmlu-train-jsonl /path/to/mmlu_train.jsonl \
  --mmlu-test-jsonl  /path/to/mmlu_test.jsonl \
  --save-dir         /path/to/run_artifacts \
  --epochs 20
```

Each JSONL row is one example. If the GSM8K files are absent the trainer still
trains and evaluates the MMLU head alone.

Deterministic Merkle-memory replay is on by default and reads
`harness/reports/upg/upg_merkle_tensor_scroll.current.json` (also not shipped).
Without that file, pass:

```bash
python3 harness/training/train_unified_phase1.py --disable-merkle-memory
```

Override the default save directory globally with the `TENT_TRAINING_SAVE_DIR`
environment variable, or per run with `--save-dir`.

`python3 harness/training/train_unified_phase1.py --help` lists the full flag set
(numeric-head variant, LR decay schedule, alignment/boundary/directional loss
terms, telemetry auxiliary weight, RNG seed).

## Run artifacts

Each run writes into `<save-dir>/unified_phase1_<run_id>/`:

- `model_weights.npz` — NumPy weights
- `vocab.json` — token map
- `report.json` — config, per-epoch logs, final metrics

## Telemetry table

Point the scraper at any directory tree containing run `report.json` files; it
recurses:

```bash
python3 harness/training/scrape_telemetry_metrics.py /path/to/run_artifacts
python3 harness/training/scrape_telemetry_metrics.py /path/to/run_artifacts --sort ratio
```

## Batch and sweep drivers

```bash
bash harness/training/run_phase1_tune_batch.sh
bash harness/training/run_phase1_phase_d_telemetry_sweep.sh
```

Both derive the repository root from their own location, so they work from any
working directory. Read the comment header of `run_phase1_tune_batch.sh` for the
environment-variable knobs (`SEEDS`, `EPOCHS`, `HIDDEN_DIM`, `BASE_LR`,
`MIN_EPOCH`, `PATIENCE`, `HEAD_DECAY_MULT`, `LR_DECAY_GAMMA`,
`FREEZE_AFTER_EPOCH`, `SAVE_DIR`, `SAVE_DIR_SUFFIX`, `RUN_LABEL`,
`SKIP_COMPARE`, `COMPARE_REPORTS_DIR`, `EXTRA_ARGS`).

Two caveats, both structural:

- `run_phase1_tune_batch.sh` invokes `harness/training/compare_runs.py` for its
  leaderboard step. **That script is not included in this repository.** Set
  `SKIP_COMPARE=1` to train without it.
- `run_phase1_phase_d_telemetry_sweep.sh` requires
  `harness/reports/training/gsm_merged_telemetry_x50.jsonl`, which is likewise not
  shipped; the script exits with a clear error if it is missing.
