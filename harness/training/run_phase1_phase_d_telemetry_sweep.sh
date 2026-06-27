#!/usr/bin/env bash
# Phase D: telemetry auxiliary weight sweep (0.03, 0.05, 0.1) with x50 merged GSM train.
# Matches Phase C: same SEEDS/EPOCHS/hparams as run_phase1_tune_batch.sh defaults; gsm_merged_telemetry_x50.jsonl.
# Run from repo root:
#   bash tent_io/harness/training/run_phase1_phase_d_telemetry_sweep.sh
# Background:
#   nohup bash tent_io/harness/training/run_phase1_phase_d_telemetry_sweep.sh > tent_io/harness/reports/training/sweep_phase_d_nohup.log 2>&1 &
set -euo pipefail
_HERE="$(cd "$(dirname "$0")" && pwd)"
# Repo root = parent of harness/ (works for dev/tent_io/harness/training and release TR-*/harness/training).
REPO_ROOT="$(cd "${_HERE}/../.." && pwd)"
# Optional: PHASE_D_BASE_SAVE=/path/to/sweep_phase_d_<stamp> to append more weights without a new stamp.
# Optional: PHASE_D_WEIGHTS="0.05 0.1" to resume a partial sweep.
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
if [[ -n "${PHASE_D_BASE_SAVE:-}" ]]; then
  BASE_SAVE="${PHASE_D_BASE_SAVE}"
else
  BASE_SAVE="${REPO_ROOT}/harness/reports/training/sweep_phase_d_${STAMP}"
fi
GSM_X50="${REPO_ROOT}/harness/reports/training/gsm_merged_telemetry_x50.jsonl"

if [[ ! -f "${GSM_X50}" ]]; then
  echo "run_phase1_phase_d_telemetry_sweep.sh: missing ${GSM_X50} (build with build_unified_batch.py / merge pipeline)" >&2
  exit 1
fi

if [[ -n "${PHASE_D_WEIGHTS:-}" ]]; then
  read -r -a WEIGHTS <<< "${PHASE_D_WEIGHTS}"
else
  WEIGHTS=(0.03 0.05 0.1)
fi
echo "=== Phase D telemetry sweep base=${BASE_SAVE} gsm_train=${GSM_X50} weights=${WEIGHTS[*]} ==="

for w in "${WEIGHTS[@]}"; do
  # SAVE_DIR_SUFFIX must be set with SAVE_DIR (see run_phase1_tune_batch.sh).
  export SAVE_DIR="${BASE_SAVE}"
  export SAVE_DIR_SUFFIX="_telemetry_w${w}"
  export RUN_LABEL="telemetry_w${w}"
  export EXTRA_ARGS="--telemetry-aux-weight ${w} --gsm8k-train-jsonl ${GSM_X50}"
  echo ""
  echo ">>> weight=${w} SAVE_DIR=${SAVE_DIR}${SAVE_DIR_SUFFIX}"
  # shellcheck disable=SC1091
  bash "${_HERE}/run_phase1_tune_batch.sh"
done

echo ""
echo "=== Phase D sweep complete. Artifacts under ${BASE_SAVE}_telemetry_w* ==="
echo "Telemetry table: python3 ${REPO_ROOT}/harness/training/scrape_telemetry_metrics.py ${REPO_ROOT}/harness/reports/training"
