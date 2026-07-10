#!/usr/bin/env bash

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
# Multi-seed stability barrage: residual_product head + auto LR decay + fixed hyperparams.
# Goal: config-level stability via compare_runs --aggregate-by-config (stability_score).
# Run from repo root: bash tent_io/harness/training/run_phase1_tune_batch.sh
# Override: SEEDS, EPOCHS, HIDDEN_DIM, BASE_LR, MIN_EPOCH, PATIENCE, HEAD_DECAY_MULT, LR_DECAY_GAMMA, FREEZE_AFTER_EPOCH (>0 freezes
# w_shared/b_shared after that epoch; heads keep training), SAVE_DIR (--save-dir for artifacts),
# SAVE_DIR_SUFFIX (optional; appended to SAVE_DIR for weight sweeps / variants — requires SAVE_DIR set),
# RUN_LABEL (optional; appended to trainer as --run-label for report.json / stdout JSON, e.g. telemetry_w0.005),
# SKIP_COMPARE=1 (train only), COMPARE_REPORTS_DIR (override directory for compare_runs; defaults to SAVE_DIR if set).
# Locked control stack (post-tuning): MIN_EPOCH=24, PATIENCE=2, HEAD_DECAY_MULT=0.5, FREEZE_AFTER_EPOCH=24.
set -euo pipefail
_HERE="$(cd "$(dirname "$0")" && pwd)"
# Parent of harness/ (tent_io in the dev tree, or release root in TR-* snapshots).
REPO_ROOT="$(cd "${_HERE}/../.." && pwd)"
PY="${PYTHON:-python3}"
TRAIN="${REPO_ROOT}/harness/training/train_unified_phase1.py"
COMPARE="${REPO_ROOT}/harness/training/compare_runs.py"

SEEDS="${SEEDS:-40 41 42 43 44 45 46 47 48 49}"
EPOCHS="${EPOCHS:-40}"
HIDDEN_DIM="${HIDDEN_DIM:-64}"
BASE_LR="${BASE_LR:-0.1}"
MIN_EPOCH="${MIN_EPOCH:-24}"
PATIENCE="${PATIENCE:-2}"
HEAD_DECAY_MULT="${HEAD_DECAY_MULT:-0.5}"
LR_DECAY_GAMMA="${LR_DECAY_GAMMA:-0.5}"
FREEZE_AFTER_EPOCH="${FREEZE_AFTER_EPOCH:-0}"
SAVE_DIR="${SAVE_DIR:-}"
SAVE_DIR_SUFFIX="${SAVE_DIR_SUFFIX:-}"
SKIP_COMPARE="${SKIP_COMPARE:-0}"
COMPARE_REPORTS_DIR="${COMPARE_REPORTS_DIR:-}"
EXTRA_ARGS="${EXTRA_ARGS:-}"
RUN_LABEL="${RUN_LABEL:-}"
if [[ -n "${RUN_LABEL}" ]]; then
  if [[ -n "${EXTRA_ARGS}" ]]; then
    EXTRA_ARGS="${EXTRA_ARGS} --run-label ${RUN_LABEL}"
  else
    EXTRA_ARGS="--run-label ${RUN_LABEL}"
  fi
fi

if [[ -n "${SAVE_DIR_SUFFIX}" ]]; then
  if [[ -z "${SAVE_DIR}" ]]; then
    echo "run_phase1_tune_batch.sh: SAVE_DIR_SUFFIX is set but SAVE_DIR is empty. Set SAVE_DIR to the artifact base path, then e.g. SAVE_DIR_SUFFIX=_telemetry_w0.005" >&2
    exit 1
  fi
  SAVE_DIR="${SAVE_DIR}${SAVE_DIR_SUFFIX}"
fi

FREEZE_ARGS=()
if [[ "${FREEZE_AFTER_EPOCH}" =~ ^[0-9]+$ ]] && (( FREEZE_AFTER_EPOCH > 0 )); then
  FREEZE_ARGS=(--freeze-shared-after-epoch "${FREEZE_AFTER_EPOCH}")
fi

SAVE_ARGS=()
if [[ -n "${SAVE_DIR}" ]]; then
  mkdir -p "${SAVE_DIR}"
  SAVE_ARGS=(--save-dir "${SAVE_DIR}")
fi

for s in ${SEEDS}; do
  echo "=== rng-seed=${s} hidden=${HIDDEN_DIM} lr=${BASE_LR} epochs=${EPOCHS} min_epoch=${MIN_EPOCH} patience=${PATIENCE} head_decay=${HEAD_DECAY_MULT} lr_decay_gamma=${LR_DECAY_GAMMA} freeze=${FREEZE_AFTER_EPOCH}${RUN_LABEL:+ run_label=${RUN_LABEL}} ==="
  # shellcheck disable=SC2086
  "${PY}" "${TRAIN}" \
    --hidden-dim "${HIDDEN_DIM}" \
    --lr "${BASE_LR}" \
    --epochs "${EPOCHS}" \
    --rng-seed "${s}" \
    --gsm-numeric-head residual_product \
    --gsm-mse-lambda 0.05 \
    --gsm-residual-alpha 0.05 \
    --gsm-head-lr-multiplier 2 \
    --auto-lr-decay-on-best-gsm \
    --auto-lr-decay-min-epoch "${MIN_EPOCH}" \
    --auto-lr-decay-patience "${PATIENCE}" \
    --gsm-head-lr-decay-multiplier "${HEAD_DECAY_MULT}" \
    --lr-decay-gamma "${LR_DECAY_GAMMA}" \
    "${SAVE_ARGS[@]+"${SAVE_ARGS[@]}"}" \
    "${FREEZE_ARGS[@]+"${FREEZE_ARGS[@]}"}" \
    ${EXTRA_ARGS}
done

if [[ "${SKIP_COMPARE}" == "1" ]]; then
  echo ""
  _sd="${SAVE_DIR:-}"
  if [[ -n "${_sd}" ]]; then
    echo "SKIP_COMPARE=1: skipping compare_runs (artifacts under ${_sd})"
  else
    echo "SKIP_COMPARE=1: skipping compare_runs (trainer default save-dir)"
  fi
  exit 0
fi

_CRD="${COMPARE_REPORTS_DIR:-}"
if [[ -z "${_CRD}" && -n "${SAVE_DIR}" ]]; then
  _CRD="${SAVE_DIR}"
fi
_COMPARE_OPTS=()
if [[ -n "${_CRD}" ]]; then
  _COMPARE_OPTS=(--reports-dir "${_CRD}")
fi

echo ""
echo "=== Config-level stability [aggregate]; also: --print-best-config for JSON ==="
"${PY}" "${COMPARE}" \
  "${_COMPARE_OPTS[@]}" \
  --aggregate-only \
  --top-k 20

echo ""
if [[ -n "${_CRD}" ]]; then
  echo "Per-run leaderboard [optional]: ${PY} ${COMPARE} --reports-dir ${_CRD} --sort-by gsm_quality --top-k 15"
else
  echo "Per-run leaderboard [optional]: ${PY} ${COMPARE} --sort-by gsm_quality --top-k 15"
fi
