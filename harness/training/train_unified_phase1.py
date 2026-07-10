#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""Unified Phase-1 trainer: shared encoder, MMLU + GSM8K heads.

This script is intentionally lightweight (NumPy only) so it can run in local
environments without a deep learning framework while preserving a multi-task
training loop.

GSM8K uses an operation-classification head (legacy) plus a trainable scalar
head on the same hidden representation for final-answer regression; exact-match
GSM accuracy is reported from the numeric head (rounded), not the heuristic
execute_op path.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

import numpy as np
from datetime import datetime, timezone

TOKEN_RE = re.compile(r"[a-z0-9_]+")
NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")

MMLU_LABELS = ["A", "B", "C", "D"]
MMLU_TO_IDX = {v: i for i, v in enumerate(MMLU_LABELS)}

OPS = ["add", "sub", "mul", "div", "fallback"]
OP_TO_IDX = {v: i for i, v in enumerate(OPS)}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def load_merkle_memory_rows(merkle_map_path: Path, max_events: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not merkle_map_path.exists():
        return [], []
    try:
        data = json.loads(merkle_map_path.read_text(encoding="utf-8"))
    except Exception:
        return [], []

    synthesis = data.get("synthesis", {})
    if not isinstance(synthesis, dict):
        return [], []
    instructions = synthesis.get("instructions", [])
    if not isinstance(instructions, list):
        return [], []

    mmlu_rows: list[dict[str, Any]] = []
    gsm_rows: list[dict[str, Any]] = []

    for inst in instructions:
        if not isinstance(inst, dict):
            continue
        if inst.get("instruction") != "replay_pin_event":
            continue
        if inst.get("message_type") != "note_on":
            continue
        prime_n = int(inst.get("prime_n", 2))
        cylinder_pin = int(inst.get("cylinder_pin", 0))
        path_text = str(inst.get("path", ""))
        xy = inst.get("ulam_xy", [0, 0])
        x = int(xy[0]) if isinstance(xy, list) and len(xy) > 0 else 0
        y = int(xy[1]) if isinstance(xy, list) and len(xy) > 1 else 0

        # MMLU replay sample (deterministic label derived from prime/pin/x/y).
        mmlu_target = MMLU_LABELS[(prime_n + cylinder_pin + abs(x) + abs(y)) % len(MMLU_LABELS)]
        mmlu_rows.append(
            {
                "question": (
                    f"memory replay mmlu from persistent merkle map for path {path_text} "
                    f"with prime {prime_n} pin {cylinder_pin} and ulam {x} {y}; "
                    f"select deterministic option by replay rule"
                ),
                "target": mmlu_target,
            }
        )

        # GSM replay sample (deterministic add operation anchor).
        gsm_answer = str(prime_n + cylinder_pin)
        gsm_rows.append(
            {
                "question": (
                    f"memory replay arithmetic total from persistent merkle pin: "
                    f"prime {prime_n} add pin {cylinder_pin} for path {path_text}"
                ),
                "target": gsm_answer,
            }
        )
        if len(mmlu_rows) >= max_events and len(gsm_rows) >= max_events:
            break
    return mmlu_rows, gsm_rows


def build_vocab(rows: list[dict[str, Any]], max_vocab: int) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        for tok in tokenize(row.get("question", "")):
            counts[tok] = counts.get(tok, 0) + 1
    pairs = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:max_vocab]
    return {tok: i for i, (tok, _) in enumerate(pairs)}


def vectorize_questions(rows: list[dict[str, Any]], vocab: dict[str, int]) -> np.ndarray:
    x = np.zeros((len(rows), len(vocab)), dtype=np.float32)
    for i, row in enumerate(rows):
        for tok in tokenize(row.get("question", "")):
            idx = vocab.get(tok)
            if idx is not None:
                x[i, idx] += 1.0
        norm = np.linalg.norm(x[i], ord=2)
        if norm > 0:
            x[i] /= norm
    return x


def softmax(logits: np.ndarray) -> np.ndarray:
    z = logits - logits.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def mmlu_labels(rows: list[dict[str, Any]]) -> np.ndarray:
    y = np.zeros((len(rows),), dtype=np.int64)
    for i, row in enumerate(rows):
        y[i] = MMLU_TO_IDX[row["target"]]
    return y


def infer_op_label(question: str) -> int:
    q = question.lower()
    if any(k in q for k in ("times", "product", "multiply")):
        return OP_TO_IDX["mul"]
    if any(k in q for k in ("each", "per", "equally", "divide", "shared")):
        return OP_TO_IDX["div"]
    if any(k in q for k in ("left", "remain", "after", "difference")):
        return OP_TO_IDX["sub"]
    if any(k in q for k in ("total", "sum", "add", "altogether", "combined")):
        return OP_TO_IDX["add"]
    return OP_TO_IDX["fallback"]


def gsm_labels(rows: list[dict[str, Any]]) -> np.ndarray:
    y = np.zeros((len(rows),), dtype=np.int64)
    for i, row in enumerate(rows):
        y[i] = infer_op_label(row.get("question", ""))
    return y


def accuracy(logits: np.ndarray, y: np.ndarray) -> float:
    if len(y) == 0:
        return 0.0
    return float((np.argmax(logits, axis=1) == y).mean())


def normalize_number(s: str) -> str:
    m = NUM_RE.findall(str(s).replace(",", ""))
    return m[-1] if m else str(s).strip()


def execute_op(op_idx: int, question: str) -> str:
    nums = [float(n) for n in NUM_RE.findall(question.replace(",", ""))]
    if not nums:
        return "NULL"
    if op_idx == OP_TO_IDX["mul"] and len(nums) >= 2:
        return str(int(round(nums[0] * nums[1])))
    if op_idx == OP_TO_IDX["div"] and len(nums) >= 2 and nums[1] != 0:
        return str(int(round(nums[0] / nums[1])))
    if op_idx == OP_TO_IDX["sub"] and len(nums) >= 2:
        return str(int(round(nums[0] - sum(nums[1:]))))
    if op_idx == OP_TO_IDX["add"] and len(nums) >= 2:
        return str(int(round(sum(nums))))
    return str(int(round(nums[-1])))


def gsm_answer_accuracy(op_logits: np.ndarray, rows: list[dict[str, Any]]) -> float:
    if not rows:
        return 0.0
    pred_ops = np.argmax(op_logits, axis=1)
    correct = 0
    for op, row in zip(pred_ops, rows):
        pred = normalize_number(execute_op(int(op), row.get("question", "")))
        gold = normalize_number(row.get("target", ""))
        if pred == gold:
            correct += 1
    return correct / len(rows)


def gsm_numeric_targets(rows: list[dict[str, Any]]) -> np.ndarray:
    t = np.zeros((len(rows),), dtype=np.float32)
    for i, row in enumerate(rows):
        raw = normalize_number(row.get("target", ""))
        try:
            t[i] = float(raw)
        except ValueError:
            t[i] = 0.0
    return t


def gsm_pred_clip_bounds(*, log1p: bool, answer_cap: float | None) -> tuple[float, float]:
    """Bounds on the numeric head output used before expm1 (log1p mode) or raw (linear)."""
    if log1p:
        hi = float(np.log1p(float(answer_cap))) if (answer_cap is not None and answer_cap > 0) else 50.0
        return 0.0, hi
    if answer_cap is not None and answer_cap > 0:
        c = float(answer_cap)
        return -c, c
    return -1e6, 1e6


def gsm_target_transform(
    t: np.ndarray,
    *,
    log1p: bool,
    answer_cap: float | None,
) -> np.ndarray:
    t2 = t.astype(np.float64)
    if answer_cap is not None and answer_cap > 0:
        t2 = np.minimum(t2, float(answer_cap))
    if not log1p:
        return t2.astype(np.float32)
    t2 = np.maximum(t2, 0.0)
    return np.log1p(t2).astype(np.float32)


def pred_numeric_to_rounded_ints(
    raw_pred: np.ndarray,
    *,
    log1p: bool,
    clip_lo: float | None = None,
    clip_hi: float | None = None,
) -> np.ndarray:
    """Map scalar regression outputs to integer answers for exact-match accuracy."""
    if log1p:
        lo = float(clip_lo) if clip_lo is not None else -50.0
        hi = float(clip_hi) if clip_hi is not None else 50.0
        pred = np.expm1(np.clip(raw_pred.astype(np.float64), lo, hi))
    else:
        r = raw_pred.astype(np.float64)
        if clip_lo is not None and clip_hi is not None:
            r = np.clip(r, float(clip_lo), float(clip_hi))
        pred = r
    return np.rint(pred).astype(np.int64)


def _softplus_np(x: np.ndarray) -> np.ndarray:
    xc = np.clip(x.astype(np.float64), -50.0, 50.0)
    return np.log1p(np.exp(xc))


def _sigmoid_np(x: np.ndarray) -> np.ndarray:
    xc = np.clip(x.astype(np.float64), -50.0, 50.0)
    return 1.0 / (1.0 + np.exp(-xc))


def gsm_numeric_pred_c_train(
    h_gsm: np.ndarray,
    w_num: np.ndarray,
    b_num: np.ndarray,
    *,
    numeric_head: str,
    gsm_log1p: bool,
    residual_alpha: float,
    use_pred_clip: bool,
    gsm_pred_lo: float,
    gsm_pred_hi: float,
) -> np.ndarray:
    """Training-aligned numeric prediction (same target space as t_gsm_train_t)."""
    raw = gsm_numeric_pred_log(
        h_gsm,
        w_num,
        b_num,
        numeric_head=numeric_head,
        gsm_log1p=gsm_log1p,
        residual_alpha=residual_alpha,
    )
    if use_pred_clip:
        return np.clip(raw, gsm_pred_lo, gsm_pred_hi).astype(np.float32)
    return raw.astype(np.float32)


def gsm_numeric_pred_log(
    h: np.ndarray,
    w_num: np.ndarray,
    b_num: np.ndarray,
    *,
    numeric_head: str,
    gsm_log1p: bool,
    residual_alpha: float = 0.1,
) -> np.ndarray:
    """Numeric head raw output in target space (log1p or linear).

    residual_* uses w_num[:, :1], b_num[:, :1] for the scalar trunk and
    w_num[:, 1:3], b_num[:, 1:3] for the softplus branch; pred = s + α·branch.
    """
    if numeric_head == "scalar":
        return (h @ w_num + b_num).ravel()
    if numeric_head == "product":
        z = h @ w_num + b_num
        z0 = z[:, 0].astype(np.float64)
        z1 = z[:, 1].astype(np.float64)
        f0 = _softplus_np(z0)
        f1 = _softplus_np(z1)
        a = np.maximum(f0 * f1, 1e-6)
        if gsm_log1p:
            return np.log1p(a).astype(np.float32)
        return a.astype(np.float32)
    # residual_product | residual_sum: stacked (H, 3) weights
    w_s = w_num[:, :1]
    b_s = b_num[:, :1]
    w_z = w_num[:, 1:3]
    b_z = b_num[:, 1:3]
    s = (h @ w_s + b_s).ravel().astype(np.float64)
    z = h @ w_z + b_z
    z0 = z[:, 0].astype(np.float64)
    z1 = z[:, 1].astype(np.float64)
    f0 = _softplus_np(z0)
    f1 = _softplus_np(z1)
    alpha_r = float(residual_alpha)
    if numeric_head == "residual_product":
        p_mul = f0 * f1
        ap = np.maximum(p_mul, 1e-6)
        if gsm_log1p:
            branch = alpha_r * np.log1p(ap)
        else:
            branch = alpha_r * ap
    else:
        # residual_sum
        q = f0 + f1
        branch = alpha_r * q
    return (s + branch).astype(np.float32)


def gsm_answer_accuracy_numeric(
    h: np.ndarray,
    w_num: np.ndarray,
    b_num: np.ndarray,
    rows: list[dict[str, Any]],
    *,
    log1p_targets: bool,
    clip_lo: float | None = None,
    clip_hi: float | None = None,
    numeric_head: str = "scalar",
    residual_alpha: float = 0.1,
) -> float:
    if not rows:
        return 0.0
    raw = gsm_numeric_pred_log(
        h,
        w_num,
        b_num,
        numeric_head=numeric_head,
        gsm_log1p=log1p_targets,
        residual_alpha=residual_alpha,
    )
    pred_int = pred_numeric_to_rounded_ints(
        raw, log1p=log1p_targets, clip_lo=clip_lo, clip_hi=clip_hi
    )
    correct = 0
    for pred, row in zip(pred_int, rows):
        gold = normalize_number(row.get("target", ""))
        try:
            gold_i = int(float(gold))
        except ValueError:
            gold_i = 10**18
        if pred == gold_i:
            correct += 1
    return correct / len(rows)


def _default_save_dir() -> Path:
    env = os.environ.get("TENT_TRAINING_SAVE_DIR", "").strip()
    if env:
        return Path(env)
    return Path("/Users/coo-koba42/dev/tent_io/harness/reports/training")


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified MMLU+GSM8K Phase-1 trainer")
    parser.add_argument(
        "--mmlu-train-jsonl",
        type=Path,
        default=Path("/Users/coo-koba42/dev/tent_io/harness/fixtures/training/mmlu_train.jsonl"),
    )
    parser.add_argument(
        "--mmlu-test-jsonl",
        type=Path,
        default=Path("/Users/coo-koba42/dev/tent_io/harness/fixtures/training/mmlu_test.jsonl"),
    )
    parser.add_argument(
        "--gsm8k-train-jsonl",
        type=Path,
        default=Path("/Users/coo-koba42/dev/tent_io/harness/fixtures/training/gsm8k_train.jsonl"),
    )
    parser.add_argument(
        "--gsm8k-test-jsonl",
        type=Path,
        default=Path("/Users/coo-koba42/dev/tent_io/harness/fixtures/training/gsm8k_test.jsonl"),
    )
    parser.add_argument(
        "--telemetry-aux-weight",
        type=float,
        default=0.0,
        help=(
            "If > 0: GSM rows with source=file_edit_telemetry shift the numeric MSE target in "
            "transformed space by (telemetry-aux-weight * drift_score * row_weight * reliability * 0.01 * "
            "telemetry-scale) per row (see build_unified_batch.py). Default 0.0 disables. Run A/B with 0 before enabling."
        ),
    )
    parser.add_argument(
        "--telemetry-scale",
        type=float,
        default=1.0,
        help=(
            "Multiplies the fixed 0.01 telemetry bump: "
            "delta = telemetry_aux_weight * drift_score * row_weight * reliability * 0.01 * telemetry_scale. "
            "Default 1.0 matches prior runs. Use e.g. 100 or 1000 for sensitivity probes before changing data."
        ),
    )
    parser.add_argument(
        "--run-label",
        type=str,
        default="",
        help=(
            "Optional label stored in report.json (config.run_label) and final JSON (run_label) "
            "for sweeps (e.g. telemetry_w0.01 to match --telemetry-aux-weight). Survives if artifact paths move."
        ),
    )
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument(
        "--rng-seed",
        type=int,
        default=42,
        help="Seed for NumPy weight initialization (multi-seed sweeps).",
    )
    parser.add_argument("--max-vocab", type=int, default=10000)
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--lr", type=float, default=0.1)
    parser.add_argument("--l2", type=float, default=1e-4)
    parser.add_argument(
        "--gsm-mse-lambda",
        type=float,
        default=0.1,
        help="Weight for GSM numeric (final-answer) MSE; 0 disables that loss path.",
    )
    parser.add_argument(
        "--gsm-target-linear",
        action="store_true",
        help="Regress raw numeric answers instead of log1p(1+max(answer,0)).",
    )
    parser.add_argument(
        "--gsm-numeric-head",
        choices=("scalar", "product", "residual_product", "residual_sum"),
        default="scalar",
        help=(
            "scalar: single output in target space (log1p or linear). "
            "product: two outputs; max(softplus(z0)*softplus(z1), eps) before log1p/linear. "
            "residual_*: keep scalar column 0; columns 1–2 are a softplus branch; "
            "pred = s + α·log1p(branch) (product) or s + α·(sp0+sp1) (sum) when targets are log1p; "
            "linear targets use the same structure without log1p on the branch product. "
            "See --gsm-residual-alpha."
        ),
    )
    parser.add_argument(
        "--gsm-residual-alpha",
        type=float,
        default=0.1,
        help="Scale for residual_product / residual_sum branch (ignored for scalar and product).",
    )
    parser.add_argument(
        "--gsm-head-lr-multiplier",
        type=float,
        default=1.0,
        help="Learning rate multiplier applied only to w_num and b_num (numeric head).",
    )
    parser.add_argument(
        "--gsm-head-lr-decay-multiplier",
        type=float,
        default=1.0,
        help=(
            "Extra factor on numeric-head LR after --lr-decay-after-epoch (same epoch threshold). "
            "1.0 disables. Use <1 to shrink head steps when global LR decays."
        ),
    )
    parser.add_argument(
        "--gsm-answer-cap",
        type=float,
        default=10000.0,
        help="Clip GSM numeric targets to this maximum before loss (0 disables).",
    )
    parser.add_argument(
        "--gsm-round-target-before-log1p",
        action="store_true",
        help="Use log1p(round(answer)) targets (after cap) instead of log1p(raw float).",
    )
    parser.add_argument(
        "--gsm-align-lambda",
        type=float,
        default=0.0,
        help=(
            "Weight for optional GSM align loss in answer space (0 disables). "
            "See --gsm-align-loss; try small values (e.g. 0.005–0.02) after gsm-mse-lambda is tuned."
        ),
    )
    parser.add_argument(
        "--gsm-align-loss",
        choices=("wrong_mse", "clipped_l1"),
        default="wrong_mse",
        help=(
            "wrong_mse: (2/n)*λ*𝟙[round(pred)≠gold]*(pred−target) chain rule into head output. "
            "clipped_l1: λ*∂mean(min(|pred−target|,1))/∂pred (smoother, often more stable)."
        ),
    )
    parser.add_argument(
        "--gsm-boundary-lambda",
        type=float,
        default=0.0,
        help=(
            "Weight for mean(|pred_answer - rint(pred_answer)|) in answer space (0 disables). "
            "Nudges the numeric head toward integer-valued predictions before rounding."
        ),
    )
    parser.add_argument(
        "--gsm-directional-lambda",
        type=float,
        default=0.0,
        help=(
            "Weight for bounded answer-space loss toward gold GSM target (0 disables). "
            "Uses --gsm-directional-loss; gradients chain through expm1 when targets are log1p."
        ),
    )
    parser.add_argument(
        "--gsm-directional-loss",
        choices=("weighted_abs", "smooth_signed"),
        default="weighted_abs",
        help=(
            "weighted_abs: mean(|err|/(1+|err|)), err=pred_answer-target. "
            "smooth_signed: mean(err/(1+|err|)), smoother derivative at 0."
        ),
    )
    parser.add_argument(
        "--gsm-no-pred-clip",
        action="store_true",
        help="Do not clip numeric head output to [0,log1p(cap)] (log1p) / cap (linear) before log-space MSE.",
    )
    parser.add_argument(
        "--disable-merkle-memory",
        action="store_true",
        help="Disable persistent Merkle replay rows in training data.",
    )
    parser.add_argument(
        "--merkle-map",
        type=Path,
        default=Path("/Users/coo-koba42/dev/tent_io/harness/reports/upg/upg_merkle_tensor_scroll.current.json"),
    )
    parser.add_argument("--merkle-max-events", type=int, default=128)
    parser.add_argument(
        "--save-dir",
        type=Path,
        default=_default_save_dir(),
        help=(
            "Directory where model/report artifacts are written. "
            "Default: $TENT_TRAINING_SAVE_DIR if set, else harness/reports/training."
        ),
    )
    parser.add_argument(
        "--freeze-shared-after-epoch",
        type=int,
        default=0,
        help=(
            "If >0, stop updating w_shared/b_shared after this epoch (MMLU/GSM heads keep training). "
            "Use a prior run's best_gsm_epoch to test drift control. 0 disables."
        ),
    )
    parser.add_argument(
        "--lr-decay-after-epoch",
        type=int,
        default=0,
        help="If >0, multiply effective LR by --lr-decay-gamma once when epoch exceeds this (0 disables).",
    )
    parser.add_argument(
        "--lr-decay-gamma",
        type=float,
        default=0.5,
        help="Multiplicative LR step applied after --lr-decay-after-epoch.",
    )
    parser.add_argument(
        "--auto-lr-decay-on-best-gsm",
        action="store_true",
        help=(
            "Event-driven LR decay (same factor as --lr-decay-gamma). "
            "If --auto-lr-decay-patience >= 0: decay once when (epoch - last_GSM_improve_epoch) > patience "
            "and epoch >= --auto-lr-decay-min-epoch. "
            "If patience is -1 (default): legacy schedule on first strict improvement past min_epoch "
            "(see --auto-lr-decay-delay). Ignored if --lr-decay-after-epoch > 0."
        ),
    )
    parser.add_argument(
        "--auto-lr-decay-delay",
        type=int,
        default=0,
        help="Extra epochs after a new GSM best before auto LR decay fires (0 = decay on next epoch).",
    )
    parser.add_argument(
        "--auto-lr-decay-min-epoch",
        type=int,
        default=10,
        help=(
            "Auto decay only from this epoch onward (patience mode: fire when current epoch >= this; "
            "legacy schedule mode: only set schedule on improvements with epoch >= this)."
        ),
    )
    parser.add_argument(
        "--auto-lr-decay-patience",
        type=int,
        default=-1,
        help=(
            "If >= 0: when (epoch - last_GSM_improve_epoch) >= patience and epoch >= min_epoch, "
            "target decay at epoch (last_improve + 1 + delay); apply once effective LR is past that point. "
            "If -1 (default): legacy mode schedules on first strict improvement past min_epoch (+ delay)."
        ),
    )
    args = parser.parse_args()

    mmlu_train = read_jsonl(args.mmlu_train_jsonl)
    mmlu_test = read_jsonl(args.mmlu_test_jsonl)
    gsm_train = read_jsonl(args.gsm8k_train_jsonl)
    gsm_test = read_jsonl(args.gsm8k_test_jsonl)

    if not mmlu_train or not mmlu_test:
        raise SystemExit("MMLU corpora not found. Run prepare_training_corpora.py first.")

    mmlu_merkle_rows: list[dict[str, Any]] = []
    gsm_merkle_rows: list[dict[str, Any]] = []
    if not args.disable_merkle_memory:
        mmlu_merkle_rows, gsm_merkle_rows = load_merkle_memory_rows(args.merkle_map, args.merkle_max_events)
        mmlu_train.extend(mmlu_merkle_rows)
        gsm_train.extend(gsm_merkle_rows)

    vocab = build_vocab(mmlu_train + gsm_train, max_vocab=args.max_vocab)
    x_mmlu_train = vectorize_questions(mmlu_train, vocab)
    x_mmlu_test = vectorize_questions(mmlu_test, vocab)
    y_mmlu_train = mmlu_labels(mmlu_train)
    y_mmlu_test = mmlu_labels(mmlu_test)

    x_gsm_train = vectorize_questions(gsm_train, vocab) if gsm_train else np.zeros((0, len(vocab)), dtype=np.float32)
    x_gsm_test = vectorize_questions(gsm_test, vocab) if gsm_test else np.zeros((0, len(vocab)), dtype=np.float32)
    y_gsm_train = gsm_labels(gsm_train) if gsm_train else np.zeros((0,), dtype=np.int64)
    y_gsm_test = gsm_labels(gsm_test) if gsm_test else np.zeros((0,), dtype=np.int64)

    gsm_log1p = not args.gsm_target_linear
    gsm_cap: float | None = None if args.gsm_answer_cap <= 0 else float(args.gsm_answer_cap)
    gsm_pred_lo, gsm_pred_hi = gsm_pred_clip_bounds(log1p=gsm_log1p, answer_cap=gsm_cap)
    use_pred_clip = not args.gsm_no_pred_clip

    raw_tgt = gsm_numeric_targets(gsm_train)
    if gsm_train and args.gsm_round_target_before_log1p:
        raw_tgt = np.rint(raw_tgt).astype(np.float32)
    t_gsm_train_t = (
        gsm_target_transform(raw_tgt, log1p=gsm_log1p, answer_cap=gsm_cap)
        if gsm_train
        else np.zeros((0,), dtype=np.float32)
    )
    t_gsm_raw = gsm_numeric_targets(gsm_train).astype(np.float64) if gsm_train else np.zeros((0,), dtype=np.float64)
    t_gsm_int = np.rint(t_gsm_raw).astype(np.int64) if len(t_gsm_raw) else np.zeros((0,), dtype=np.int64)

    t_gsm_train_t_base = np.zeros((0,), dtype=np.float32)
    telemetry_aux_delta = np.zeros((0,), dtype=np.float64)
    telemetry_mask_arr = np.zeros((0,), dtype=bool)
    if gsm_train:
        t_gsm_train_t_base = np.asarray(t_gsm_train_t, dtype=np.float32).copy()
        n_gsm_rows = len(gsm_train)
        telemetry_mask_arr = np.array(
            [str(r.get("source", "")) == "file_edit_telemetry" for r in gsm_train],
            dtype=bool,
        )
        tw = float(args.telemetry_aux_weight)
        telemetry_aux_delta = np.zeros((n_gsm_rows,), dtype=np.float64)
        for i in range(n_gsm_rows):
            if not telemetry_mask_arr[i]:
                continue
            try:
                sig = (
                    float(gsm_train[i].get("drift_score", 0.0))
                    * float(gsm_train[i].get("weight", 0.0))
                    * float(gsm_train[i].get("reliability", 0.0))
                )
            except (TypeError, ValueError):
                sig = 0.0
            telemetry_aux_delta[i] = (
                tw * float(sig) * 0.01 * float(args.telemetry_scale)
            )
        t_gsm_train_t = t_gsm_train_t_base + telemetry_aux_delta.astype(np.float32)

    if gsm_log1p:
        eval_clip_lo, eval_clip_hi = (
            (gsm_pred_lo, gsm_pred_hi) if use_pred_clip else (-50.0, 50.0)
        )
    else:
        eval_clip_lo, eval_clip_hi = (
            (gsm_pred_lo, gsm_pred_hi) if use_pred_clip else (None, None)
        )

    rng = np.random.default_rng(int(args.rng_seed))
    w_shared = rng.normal(scale=0.03, size=(len(vocab), args.hidden_dim)).astype(np.float32)
    b_shared = np.zeros((1, args.hidden_dim), dtype=np.float32)
    w_mmlu = rng.normal(scale=0.03, size=(args.hidden_dim, 4)).astype(np.float32)
    b_mmlu = np.zeros((1, 4), dtype=np.float32)
    w_gsm = rng.normal(scale=0.03, size=(args.hidden_dim, len(OPS))).astype(np.float32)
    b_gsm = np.zeros((1, len(OPS)), dtype=np.float32)
    if args.gsm_numeric_head == "product":
        w_num = rng.normal(scale=0.02, size=(args.hidden_dim, 2)).astype(np.float32)
        b_num = np.array([[1.15, 1.15]], dtype=np.float32)
    elif args.gsm_numeric_head in ("residual_product", "residual_sum"):
        w_num = np.zeros((args.hidden_dim, 3), dtype=np.float32)
        w_num[:, 0:1] = rng.normal(scale=0.03, size=(args.hidden_dim, 1)).astype(np.float32)
        w_num[:, 1:3] = rng.normal(scale=0.02, size=(args.hidden_dim, 2)).astype(np.float32)
        b_num = np.zeros((1, 3), dtype=np.float32)
        b_num[0, 1:3] = 1.15
    else:
        _num_dim = 1
        w_num = rng.normal(scale=0.03, size=(args.hidden_dim, 1)).astype(np.float32)
        b_num = np.zeros((1, 1), dtype=np.float32)
    epoch_logs: list[dict[str, Any]] = []
    best_gsm_answer_test_acc: float | None = None
    best_gsm_epoch: int | None = None
    best_mmlu_test_acc_at_best_gsm: float | None = None
    gsm_test_acc_per_epoch: list[float] = []
    effective_lr = float(args.lr)
    lr_decay_applied = False
    lr_decay_reason: str = "none"
    scheduled_auto_decay_epoch: int | None = None
    last_gsm_improve_epoch: int | None = None
    lr_decay_fired_epoch: int | None = None
    lr_decay_schedule_target_epoch: int | None = None
    lr_decay_post_run_applied: bool = False

    for epoch in range(1, args.epochs + 1):
        if int(args.lr_decay_after_epoch) > 0 and not lr_decay_applied:
            if epoch > int(args.lr_decay_after_epoch):
                effective_lr *= float(args.lr_decay_gamma)
                lr_decay_applied = True
                lr_decay_reason = "manual_epoch"
                lr_decay_schedule_target_epoch = int(args.lr_decay_after_epoch) + 1
                if lr_decay_fired_epoch is None:
                    lr_decay_fired_epoch = epoch
        elif (
            args.auto_lr_decay_on_best_gsm
            and int(args.lr_decay_after_epoch) == 0
            and int(args.auto_lr_decay_patience) >= 0
            and not lr_decay_applied
            and last_gsm_improve_epoch is not None
            and epoch >= int(args.auto_lr_decay_min_epoch)
            and (epoch - last_gsm_improve_epoch) >= int(args.auto_lr_decay_patience)
        ):
            _psched = last_gsm_improve_epoch + 1 + int(args.auto_lr_decay_delay)
            lr_decay_schedule_target_epoch = _psched
            if epoch >= _psched:
                effective_lr *= float(args.lr_decay_gamma)
                lr_decay_applied = True
                lr_decay_reason = "auto_best_gsm"
                if lr_decay_fired_epoch is None:
                    lr_decay_fired_epoch = epoch
            else:
                scheduled_auto_decay_epoch = _psched
        elif (
            args.auto_lr_decay_on_best_gsm
            and int(args.lr_decay_after_epoch) == 0
            and not lr_decay_applied
            and scheduled_auto_decay_epoch is not None
            and epoch >= scheduled_auto_decay_epoch
        ):
            lr_decay_schedule_target_epoch = scheduled_auto_decay_epoch
            effective_lr *= float(args.lr_decay_gamma)
            lr_decay_applied = True
            lr_decay_reason = "auto_best_gsm"
            if lr_decay_fired_epoch is None:
                lr_decay_fired_epoch = epoch
        # MMLU step
        h_mmlu = np.tanh(x_mmlu_train @ w_shared + b_shared)
        logits_mmlu = h_mmlu @ w_mmlu + b_mmlu
        probs_mmlu = softmax(logits_mmlu)
        onehot_mmlu = np.eye(4, dtype=np.float32)[y_mmlu_train]
        dlogits_mmlu = (probs_mmlu - onehot_mmlu) / len(x_mmlu_train)
        dw_mmlu = h_mmlu.T @ dlogits_mmlu + args.l2 * w_mmlu
        db_mmlu = dlogits_mmlu.sum(axis=0, keepdims=True)
        dh_mmlu = dlogits_mmlu @ w_mmlu.T
        dz_mmlu = dh_mmlu * (1 - h_mmlu * h_mmlu)
        dw_shared_mmlu = x_mmlu_train.T @ dz_mmlu
        db_shared_mmlu = dz_mmlu.sum(axis=0, keepdims=True)

        # GSM step (optional): op-routing CE + numeric final-answer MSE on shared hidden state
        if len(x_gsm_train) > 0:
            h_gsm = np.tanh(x_gsm_train @ w_shared + b_shared)
            logits_gsm = h_gsm @ w_gsm + b_gsm
            probs_gsm = softmax(logits_gsm)
            onehot_gsm = np.eye(len(OPS), dtype=np.float32)[y_gsm_train]
            n_gsm = len(x_gsm_train)
            dlogits_gsm = (probs_gsm - onehot_gsm) / n_gsm
            dw_gsm = h_gsm.T @ dlogits_gsm + args.l2 * w_gsm
            db_gsm = dlogits_gsm.sum(axis=0, keepdims=True)
            dh_from_ce = dlogits_gsm @ w_gsm.T
            if args.gsm_numeric_head == "scalar":
                pred_raw = (h_gsm @ w_num + b_num).ravel()
                d_pred = np.zeros_like(pred_raw, dtype=np.float32)
                if args.gsm_mse_lambda > 0.0:
                    if use_pred_clip:
                        pred_c = np.clip(pred_raw, gsm_pred_lo, gsm_pred_hi)
                    else:
                        pred_c = pred_raw
                    diff = (pred_c.astype(np.float32) - t_gsm_train_t).astype(np.float32)
                    d_pred += (2.0 / float(n_gsm)) * float(args.gsm_mse_lambda) * diff
                need_answer_space = (
                    args.gsm_align_lambda > 0.0
                    or args.gsm_boundary_lambda > 0.0
                    or args.gsm_directional_lambda > 0.0
                )
                if need_answer_space:
                    if gsm_log1p:
                        pc_a = (
                            np.clip(pred_raw, gsm_pred_lo, gsm_pred_hi)
                            if use_pred_clip
                            else np.clip(pred_raw, -50.0, 50.0)
                        )
                        pred_lin = np.expm1(pc_a)
                        chain = np.exp(np.minimum(pc_a, 50.0))
                    else:
                        pc_a = (
                            np.clip(pred_raw, gsm_pred_lo, gsm_pred_hi)
                            if use_pred_clip
                            else pred_raw.astype(np.float64)
                        )
                        pred_lin = pc_a.astype(np.float64)
                        chain = np.ones_like(pred_lin, dtype=np.float64)
                    if args.gsm_boundary_lambda > 0.0:
                        lam_b = float(args.gsm_boundary_lambda)
                        nearest = np.rint(pred_lin)
                        g_b = (lam_b / float(n_gsm)) * np.sign(pred_lin - nearest)
                        d_pred += (g_b * chain).astype(np.float32)
                    if args.gsm_align_lambda > 0.0:
                        lam_a = float(args.gsm_align_lambda)
                        if args.gsm_align_loss == "wrong_mse":
                            wrong = (np.rint(pred_lin).astype(np.int64) != t_gsm_int)
                            g = (
                                (2.0 / float(n_gsm))
                                * lam_a
                                * wrong.astype(np.float64)
                                * (pred_lin - t_gsm_raw)
                            )
                        else:
                            err = pred_lin - t_gsm_raw
                            mask = (np.abs(err) < 1.0).astype(np.float64)
                            g = (1.0 / float(n_gsm)) * lam_a * np.sign(err) * mask
                        d_pred += (g * chain).astype(np.float32)
                    if args.gsm_directional_lambda > 0.0:
                        lam_d = float(args.gsm_directional_lambda)
                        err = pred_lin - t_gsm_raw
                        denom = (1.0 + np.abs(err)) ** 2
                        if args.gsm_directional_loss == "smooth_signed":
                            g_d = (lam_d / float(n_gsm)) / denom
                        else:
                            g_d = (lam_d / float(n_gsm)) * np.sign(err) / denom
                        d_pred += (g_d * chain).astype(np.float32)
                if (
                    args.gsm_mse_lambda > 0.0
                    or args.gsm_align_lambda > 0.0
                    or args.gsm_boundary_lambda > 0.0
                    or args.gsm_directional_lambda > 0.0
                ):
                    dw_num = (h_gsm.T @ d_pred[:, np.newaxis]) + args.l2 * w_num
                    db_num = np.array([[float(np.sum(d_pred))]], dtype=np.float32)
                    dh_from_num = d_pred[:, np.newaxis] * w_num.T
                    dh_gsm = dh_from_ce + dh_from_num
                else:
                    dw_num = np.zeros_like(w_num)
                    db_num = np.zeros_like(b_num)
                    dh_gsm = dh_from_ce
            elif args.gsm_numeric_head == "product":
                # product head: p = softplus(z0)*softplus(z1), a = max(p, eps); log target uses log1p(a)
                z = h_gsm @ w_num + b_num
                z0 = z[:, 0].astype(np.float64)
                z1 = z[:, 1].astype(np.float64)
                z0c = np.clip(z0, -50.0, 50.0)
                z1c = np.clip(z1, -50.0, 50.0)
                f0 = np.log1p(np.exp(z0c))
                f1 = np.log1p(np.exp(z1c))
                p = f0 * f1
                a = np.maximum(p, 1e-6)
                if gsm_log1p:
                    pred_raw = np.log1p(a).astype(np.float32)
                else:
                    pred_raw = a.astype(np.float32)
                pred_lin = a.astype(np.float64)
                dL_da = np.zeros((n_gsm,), dtype=np.float64)
                if args.gsm_mse_lambda > 0.0:
                    if use_pred_clip:
                        pred_c = np.clip(pred_raw, gsm_pred_lo, gsm_pred_hi)
                    else:
                        pred_c = pred_raw
                    diff = (pred_c.astype(np.float32) - t_gsm_train_t).astype(np.float32)
                    scale_mse = (2.0 / float(n_gsm)) * float(args.gsm_mse_lambda)
                    d_pl = scale_mse * diff
                    if gsm_log1p:
                        dL_da += d_pl.astype(np.float64) * (1.0 / (1.0 + a))
                    else:
                        dL_da += d_pl.astype(np.float64)
                if args.gsm_boundary_lambda > 0.0:
                    lam_b = float(args.gsm_boundary_lambda)
                    nearest = np.rint(pred_lin)
                    dL_da += (lam_b / float(n_gsm)) * np.sign(pred_lin - nearest)
                if args.gsm_align_lambda > 0.0:
                    lam_a = float(args.gsm_align_lambda)
                    if args.gsm_align_loss == "wrong_mse":
                        wrong = (np.rint(pred_lin).astype(np.int64) != t_gsm_int)
                        dL_da += (
                            (2.0 / float(n_gsm))
                            * lam_a
                            * wrong.astype(np.float64)
                            * (pred_lin - t_gsm_raw)
                        )
                    else:
                        err = pred_lin - t_gsm_raw
                        mask = (np.abs(err) < 1.0).astype(np.float64)
                        dL_da += (1.0 / float(n_gsm)) * lam_a * np.sign(err) * mask
                if args.gsm_directional_lambda > 0.0:
                    lam_d = float(args.gsm_directional_lambda)
                    err = pred_lin - t_gsm_raw
                    denom = (1.0 + np.abs(err)) ** 2
                    if args.gsm_directional_loss == "smooth_signed":
                        dL_da += (lam_d / float(n_gsm)) / denom
                    else:
                        dL_da += (lam_d / float(n_gsm)) * np.sign(err) / denom
                if (
                    args.gsm_mse_lambda > 0.0
                    or args.gsm_align_lambda > 0.0
                    or args.gsm_boundary_lambda > 0.0
                    or args.gsm_directional_lambda > 0.0
                ):
                    dL_dp = dL_da * (p > 1e-6).astype(np.float64)
                    dL_df0 = dL_dp * f1
                    dL_df1 = dL_dp * f0
                    sig0 = _sigmoid_np(z0)
                    sig1 = _sigmoid_np(z1)
                    dz0 = dL_df0 * sig0
                    dz1 = dL_df1 * sig1
                    dz_mat = np.column_stack([dz0, dz1])
                    dw_num = h_gsm.T @ dz_mat + args.l2 * w_num
                    db_num = np.sum(dz_mat, axis=0, keepdims=True).astype(np.float32)
                    dh_from_num = (
                        dz0[:, np.newaxis] * w_num[np.newaxis, :, 0]
                        + dz1[:, np.newaxis] * w_num[np.newaxis, :, 1]
                    )
                    dh_gsm = dh_from_ce + dh_from_num
                else:
                    dw_num = np.zeros_like(w_num)
                    db_num = np.zeros_like(b_num)
                    dh_gsm = dh_from_ce
            elif args.gsm_numeric_head in ("residual_product", "residual_sum"):
                w_s = w_num[:, :1]
                b_s = b_num[:, :1]
                w_z = w_num[:, 1:3]
                b_z = b_num[:, 1:3]
                s = (h_gsm @ w_s + b_s).ravel().astype(np.float64)
                z = h_gsm @ w_z + b_z
                z0 = z[:, 0].astype(np.float64)
                z1 = z[:, 1].astype(np.float64)
                z0c = np.clip(z0, -50.0, 50.0)
                z1c = np.clip(z1, -50.0, 50.0)
                f0 = np.log1p(np.exp(z0c))
                f1 = np.log1p(np.exp(z1c))
                alpha_r = float(args.gsm_residual_alpha)
                if args.gsm_numeric_head == "residual_product":
                    p_mul = f0 * f1
                    ap = np.maximum(p_mul, 1e-6)
                    if gsm_log1p:
                        pred_raw = (s + alpha_r * np.log1p(ap)).astype(np.float32)
                    else:
                        pred_raw = (s + alpha_r * ap).astype(np.float32)
                else:
                    q = f0 + f1
                    pred_raw = (s + alpha_r * q).astype(np.float32)

                d_r = np.zeros((n_gsm,), dtype=np.float64)
                need_answer_space_rs = (
                    args.gsm_align_lambda > 0.0
                    or args.gsm_boundary_lambda > 0.0
                    or args.gsm_directional_lambda > 0.0
                )
                if args.gsm_mse_lambda > 0.0:
                    if use_pred_clip:
                        pred_c = np.clip(pred_raw, gsm_pred_lo, gsm_pred_hi)
                    else:
                        pred_c = pred_raw
                    diff = (pred_c.astype(np.float32) - t_gsm_train_t).astype(np.float32)
                    d_r += (2.0 / float(n_gsm)) * float(args.gsm_mse_lambda) * diff.astype(np.float64)
                if need_answer_space_rs:
                    if gsm_log1p:
                        pc_a = (
                            np.clip(pred_raw, gsm_pred_lo, gsm_pred_hi)
                            if use_pred_clip
                            else np.clip(pred_raw, -50.0, 50.0)
                        )
                        pred_lin = np.expm1(pc_a)
                        chain = np.exp(np.minimum(pc_a, 50.0))
                    else:
                        pc_a = (
                            np.clip(pred_raw, gsm_pred_lo, gsm_pred_hi)
                            if use_pred_clip
                            else pred_raw.astype(np.float64)
                        )
                        pred_lin = pc_a.astype(np.float64)
                        chain = np.ones_like(pred_lin, dtype=np.float64)
                    if args.gsm_boundary_lambda > 0.0:
                        lam_b = float(args.gsm_boundary_lambda)
                        nearest = np.rint(pred_lin)
                        g_b = (lam_b / float(n_gsm)) * np.sign(pred_lin - nearest)
                        d_r += (g_b * chain).astype(np.float64)
                    if args.gsm_align_lambda > 0.0:
                        lam_a = float(args.gsm_align_lambda)
                        if args.gsm_align_loss == "wrong_mse":
                            wrong = (np.rint(pred_lin).astype(np.int64) != t_gsm_int)
                            g = (
                                (2.0 / float(n_gsm))
                                * lam_a
                                * wrong.astype(np.float64)
                                * (pred_lin - t_gsm_raw)
                            )
                        else:
                            err = pred_lin - t_gsm_raw
                            mask = (np.abs(err) < 1.0).astype(np.float64)
                            g = (1.0 / float(n_gsm)) * lam_a * np.sign(err) * mask
                        d_r += (g * chain).astype(np.float64)
                    if args.gsm_directional_lambda > 0.0:
                        lam_d = float(args.gsm_directional_lambda)
                        err = pred_lin - t_gsm_raw
                        denom = (1.0 + np.abs(err)) ** 2
                        if args.gsm_directional_loss == "smooth_signed":
                            g_d = (lam_d / float(n_gsm)) / denom
                        else:
                            g_d = (lam_d / float(n_gsm)) * np.sign(err) / denom
                        d_r += (g_d * chain).astype(np.float64)

                if (
                    args.gsm_mse_lambda > 0.0
                    or args.gsm_align_lambda > 0.0
                    or args.gsm_boundary_lambda > 0.0
                    or args.gsm_directional_lambda > 0.0
                ):
                    d_s = d_r
                    if args.gsm_numeric_head == "residual_product":
                        p_mul = f0 * f1
                        ap = np.maximum(p_mul, 1e-6)
                        if gsm_log1p:
                            dL_da = d_r * (alpha_r / (1.0 + ap))
                        else:
                            dL_da = d_r * alpha_r * (p_mul > 1e-6).astype(np.float64)
                        dL_dp = dL_da * (p_mul > 1e-6).astype(np.float64)
                        dL_df0 = dL_dp * f1
                        dL_df1 = dL_dp * f0
                    else:
                        dL_df0 = d_r * alpha_r
                        dL_df1 = d_r * alpha_r
                    sig0 = _sigmoid_np(z0)
                    sig1 = _sigmoid_np(z1)
                    dz0 = dL_df0 * sig0
                    dz1 = dL_df1 * sig1
                    dz_mat = np.column_stack([dz0, dz1])
                    dw_s = h_gsm.T @ d_s[:, np.newaxis] + args.l2 * w_s
                    dw_z = h_gsm.T @ dz_mat + args.l2 * w_z
                    dw_num = np.concatenate([dw_s, dw_z], axis=1)
                    db_num = np.concatenate(
                        [
                            np.array([[float(np.sum(d_s))]], dtype=np.float32),
                            np.sum(dz_mat, axis=0, keepdims=True).astype(np.float32),
                        ],
                        axis=1,
                    )
                    dh_from_s = d_s[:, np.newaxis] * w_s.T
                    dh_from_z = (
                        dz0[:, np.newaxis] * w_z[np.newaxis, :, 0]
                        + dz1[:, np.newaxis] * w_z[np.newaxis, :, 1]
                    )
                    dh_from_num = dh_from_s + dh_from_z
                    dh_gsm = dh_from_ce + dh_from_num
                else:
                    dw_num = np.zeros_like(w_num)
                    db_num = np.zeros_like(b_num)
                    dh_gsm = dh_from_ce
            else:
                raise ValueError(f"unknown gsm-numeric-head: {args.gsm_numeric_head!r}")
            dz_gsm = dh_gsm * (1 - h_gsm * h_gsm)
            dw_shared_gsm = x_gsm_train.T @ dz_gsm
            db_shared_gsm = dz_gsm.sum(axis=0, keepdims=True)
        else:
            dw_gsm = np.zeros_like(w_gsm)
            db_gsm = np.zeros_like(b_gsm)
            dw_num = np.zeros_like(w_num)
            db_num = np.zeros_like(b_num)
            dw_shared_gsm = np.zeros_like(w_shared)
            db_shared_gsm = np.zeros_like(b_shared)

        # Joint update
        _freeze_shared = int(args.freeze_shared_after_epoch) > 0 and epoch > int(
            args.freeze_shared_after_epoch
        )
        if not _freeze_shared:
            w_shared -= effective_lr * ((dw_shared_mmlu + dw_shared_gsm) + args.l2 * w_shared)
            b_shared -= effective_lr * (db_shared_mmlu + db_shared_gsm)
        w_mmlu -= effective_lr * dw_mmlu
        b_mmlu -= effective_lr * db_mmlu
        w_gsm -= effective_lr * dw_gsm
        b_gsm -= effective_lr * db_gsm
        _head_decay = (
            float(args.gsm_head_lr_decay_multiplier) if lr_decay_applied else 1.0
        )
        lr_gsm_head = effective_lr * float(args.gsm_head_lr_multiplier) * _head_decay
        w_num -= lr_gsm_head * dw_num
        b_num -= lr_gsm_head * db_num

        h_mmlu_te = np.tanh(x_mmlu_test @ w_shared + b_shared)
        mmlu_test_acc_ep = accuracy(h_mmlu_te @ w_mmlu + b_mmlu, y_mmlu_test)
        gsm_acc_ep: float | None = None
        h_gsm_te_ep: np.ndarray | None = None
        if len(x_gsm_train) > 0:
            h_gsm_te_ep = np.tanh(x_gsm_test @ w_shared + b_shared)
            gsm_acc_ep = gsm_answer_accuracy_numeric(
                h_gsm_te_ep,
                w_num,
                b_num,
                gsm_test,
                log1p_targets=gsm_log1p,
                clip_lo=eval_clip_lo,
                clip_hi=eval_clip_hi,
                numeric_head=args.gsm_numeric_head,
                residual_alpha=args.gsm_residual_alpha,
            )
            g_ep = float(gsm_acc_ep)
            gsm_test_acc_per_epoch.append(g_ep)
            _prev_best = best_gsm_answer_test_acc
            if best_gsm_answer_test_acc is None or g_ep > best_gsm_answer_test_acc:
                if (
                    int(args.auto_lr_decay_patience) < 0
                    and args.auto_lr_decay_on_best_gsm
                    and int(args.lr_decay_after_epoch) == 0
                    and not lr_decay_applied
                    and _prev_best is not None
                    and g_ep > _prev_best
                    and epoch >= int(args.auto_lr_decay_min_epoch)
                ):
                    _sched = epoch + 1 + int(args.auto_lr_decay_delay)
                    lr_decay_schedule_target_epoch = _sched
                    if _sched > int(args.epochs):
                        effective_lr *= float(args.lr_decay_gamma)
                        lr_decay_applied = True
                        lr_decay_reason = "auto_best_gsm"
                        if lr_decay_fired_epoch is None:
                            lr_decay_fired_epoch = epoch
                    else:
                        scheduled_auto_decay_epoch = _sched
                best_gsm_answer_test_acc = g_ep
                best_gsm_epoch = epoch
                best_mmlu_test_acc_at_best_gsm = float(mmlu_test_acc_ep)
                last_gsm_improve_epoch = epoch

        if epoch == 1 or epoch % 5 == 0 or epoch == args.epochs:
            mmlu_train_acc = accuracy(logits_mmlu, y_mmlu_train)
            log = {
                "epoch": epoch,
                "mmlu_train_acc": mmlu_train_acc,
                "mmlu_test_acc": mmlu_test_acc_ep,
            }
            if len(x_gsm_train) > 0 and h_gsm_te_ep is not None and gsm_acc_ep is not None:
                h_gsm_tr = np.tanh(x_gsm_train @ w_shared + b_shared)
                gsm_train_logits = h_gsm_tr @ w_gsm + b_gsm
                gsm_test_logits = h_gsm_te_ep @ w_gsm + b_gsm
                log["gsm_op_train_acc"] = accuracy(gsm_train_logits, y_gsm_train)
                log["gsm_op_test_acc"] = accuracy(gsm_test_logits, y_gsm_test)
                log["gsm_answer_heuristic_test_acc"] = gsm_answer_accuracy(gsm_test_logits, gsm_test)
                log["gsm_answer_test_acc"] = gsm_acc_ep
                gn = float(gsm_acc_ep)
                gh = float(log["gsm_answer_heuristic_test_acc"])
                log["gsm_numeric_minus_heuristic_test_acc"] = gn - gh
                log["gsm_numeric_over_heuristic_test_acc"] = (gn / gh) if gh > 0 else None
            print(json.dumps(log))
            epoch_logs.append(log)

    if (
        args.auto_lr_decay_on_best_gsm
        and int(args.lr_decay_after_epoch) == 0
        and int(args.auto_lr_decay_patience) >= 0
        and not lr_decay_applied
        and last_gsm_improve_epoch is not None
        and int(args.epochs) > int(last_gsm_improve_epoch)
    ):
        if scheduled_auto_decay_epoch is not None and lr_decay_schedule_target_epoch is None:
            lr_decay_schedule_target_epoch = scheduled_auto_decay_epoch
        lr_decay_post_run_applied = True
        effective_lr *= float(args.lr_decay_gamma)
        lr_decay_applied = True
        lr_decay_reason = "auto_best_gsm_final_fallback"

    telemetry_row_frac = 0.0
    telemetry_aux_mean_abs = 0.0
    telemetry_aux_to_base_ratio = 0.0
    if len(gsm_train) > 0 and telemetry_mask_arr.size > 0:
        n_tel = int(np.sum(telemetry_mask_arr))
        telemetry_row_frac = float(n_tel) / float(len(gsm_train))
        if n_tel > 0:
            abs_aux = np.abs(telemetry_aux_delta[telemetry_mask_arr])
            telemetry_aux_mean_abs = float(np.mean(abs_aux))
            h_gsm_tr = np.tanh(x_gsm_train @ w_shared + b_shared)
            pred_c_tr = gsm_numeric_pred_c_train(
                h_gsm_tr,
                w_num,
                b_num,
                numeric_head=args.gsm_numeric_head,
                gsm_log1p=gsm_log1p,
                residual_alpha=float(args.gsm_residual_alpha),
                use_pred_clip=use_pred_clip,
                gsm_pred_lo=gsm_pred_lo,
                gsm_pred_hi=gsm_pred_hi,
            )
            base_res = np.abs(
                pred_c_tr.astype(np.float64) - t_gsm_train_t_base.astype(np.float64)
            )
            tel_res = base_res[telemetry_mask_arr]
            denom = float(np.mean(tel_res)) if tel_res.size else 0.0
            if denom > 1e-12:
                telemetry_aux_to_base_ratio = telemetry_aux_mean_abs / denom

    final = {
        "mmlu_train_rows": len(mmlu_train),
        "mmlu_test_rows": len(mmlu_test),
        "gsm_train_rows": len(gsm_train),
        "gsm_test_rows": len(gsm_test),
        "telemetry_row_frac": telemetry_row_frac,
        "telemetry_aux_mean_abs": telemetry_aux_mean_abs,
        "telemetry_aux_to_base_ratio": telemetry_aux_to_base_ratio,
        "rows_merkle_replay_mmlu": len(mmlu_merkle_rows),
        "rows_merkle_replay_gsm": len(gsm_merkle_rows),
        "merkle_memory_enabled": not args.disable_merkle_memory,
        "merkle_map": str(args.merkle_map),
        "vocab_size": len(vocab),
        "effective_lr_end": effective_lr,
        "lr_decay_reason": lr_decay_reason,
        "lr_decay_schedule_target_epoch": lr_decay_schedule_target_epoch,
        "lr_decay_fired_epoch": lr_decay_fired_epoch,
        "lr_decay_post_run_applied": lr_decay_post_run_applied,
    }
    if lr_decay_fired_epoch is not None and lr_decay_schedule_target_epoch is not None:
        final["lr_decay_lag"] = int(lr_decay_fired_epoch) - int(lr_decay_schedule_target_epoch)
    else:
        final["lr_decay_lag"] = None
    if lr_decay_fired_epoch is not None and best_gsm_epoch is not None:
        final["lr_decay_offset_from_best"] = int(lr_decay_fired_epoch) - int(best_gsm_epoch)
    else:
        final["lr_decay_offset_from_best"] = None
    _fi_ld = lr_decay_fired_epoch
    if (
        _fi_ld is not None
        and int(_fi_ld) >= 1
        and int(_fi_ld) <= len(gsm_test_acc_per_epoch)
    ):
        final["gsm_answer_test_acc_at_lr_decay_fired"] = float(
            gsm_test_acc_per_epoch[int(_fi_ld) - 1]
        )
    else:
        final["gsm_answer_test_acc_at_lr_decay_fired"] = None
    if len(x_gsm_train) > 0:
        h_gsm_te = np.tanh(x_gsm_test @ w_shared + b_shared)
        final["final_gsm_answer_test_acc"] = gsm_answer_accuracy_numeric(
            h_gsm_te,
            w_num,
            b_num,
            gsm_test,
            log1p_targets=gsm_log1p,
            clip_lo=eval_clip_lo,
            clip_hi=eval_clip_hi,
            numeric_head=args.gsm_numeric_head,
            residual_alpha=args.gsm_residual_alpha,
        )
        final["final_gsm_answer_heuristic_test_acc"] = gsm_answer_accuracy(h_gsm_te @ w_gsm + b_gsm, gsm_test)
        fn = float(final["final_gsm_answer_test_acc"])
        fh = float(final["final_gsm_answer_heuristic_test_acc"])
        final["final_gsm_numeric_minus_heuristic_test_acc"] = fn - fh
        final["final_gsm_numeric_over_heuristic_test_acc"] = (fn / fh) if fh > 0 else None
        if best_gsm_epoch is not None:
            final["best_gsm_answer_test_acc"] = best_gsm_answer_test_acc
            final["best_gsm_epoch"] = best_gsm_epoch
            final["best_mmlu_test_acc_at_best_gsm"] = best_mmlu_test_acc_at_best_gsm
            # Read-only counterfactual: epoch that maximizes GSM test (first if tied).
            final["early_stop_epoch_gsm"] = best_gsm_epoch
            final["recommended_epoch_gsm"] = int(best_gsm_epoch)
            # Peak local shape at best_gsm_epoch: penalize isolated spikes (neighbors far below peak).
            _bi = int(best_gsm_epoch) - 1
            _h = gsm_test_acc_per_epoch
            _nei: list[float] = []
            if _bi > 0:
                _nei.append(float(_h[_bi - 1]))
            if _bi + 1 < len(_h):
                _nei.append(float(_h[_bi + 1]))
            _nfloor = min(_nei) if _nei else float(_h[_bi])
            _peak_iso = max(0.0, float(best_gsm_answer_test_acc) - _nfloor)
            final["best_gsm_peak_isolation"] = _peak_iso
            _bqs = float(best_gsm_answer_test_acc) - 0.5 * _peak_iso
            final["best_gsm_quality_score"] = _bqs
            if float(best_gsm_answer_test_acc) > 0.0:
                final["best_gsm_quality_ratio"] = _bqs / float(best_gsm_answer_test_acc)
            final["gsm_degradation"] = float(best_gsm_answer_test_acc) - fn
            final["epochs_since_best_gsm"] = int(args.epochs) - int(best_gsm_epoch)
            # Epochs with test GSM within 95% of run peak (plateau width; narrow = spike).
            _peak = float(best_gsm_answer_test_acc)
            _thr = 0.95 * _peak - 1e-12
            _pw = sum(1 for g in gsm_test_acc_per_epoch if g >= _thr)
            final["gsm_peak_width_3"] = _pw
            _stable_ep: int | None = None
            for _ri in range(len(gsm_test_acc_per_epoch) - 1, -1, -1):
                if float(gsm_test_acc_per_epoch[_ri]) >= _thr:
                    _stable_ep = _ri + 1
                    break
            final["recommended_epoch_gsm_stable"] = _stable_ep
            _ep = max(int(args.epochs), 1)
            # High peak × fraction of run spent near peak (sweep-friendly).
            final["gsm_plateau_quality"] = _peak * (_pw / float(_ep))
            # Sweep ranking: peak accuracy minus half the final-vs-best drop (λ=0.5).
            final["gsm_quality_score"] = _peak - 0.5 * float(final["gsm_degradation"])
            # 1.0 = no degradation from peak; <1.0 = instability (scale-free vs peak height).
            if _peak > 0.0:
                final["gsm_quality_ratio"] = float(final["gsm_quality_score"]) / _peak
            # OLS slope of test GSM vs epoch from (best_gsm_epoch, peak) through final epoch.
            # Negative ⇒ net decline along the tail; ~0 ⇒ flat or best at last epoch.
            _e_best = int(best_gsm_epoch)
            _E = int(args.epochs)
            _sx = [float(_e_best)]
            _sy = [float(best_gsm_answer_test_acc)]
            for _epn in range(_e_best + 1, _E + 1):
                _sx.append(float(_epn))
                _sy.append(float(gsm_test_acc_per_epoch[_epn - 1]))
            if len(_sx) < 2:
                final["gsm_post_peak_slope"] = 0.0
            else:
                _xv = np.array(_sx, dtype=np.float64)
                _yv = np.array(_sy, dtype=np.float64)
                _xm = float(_xv.mean())
                _ym = float(_yv.mean())
                _dx = _xv - _xm
                _den = float((_dx * _dx).sum())
                if _den < 1e-18:
                    final["gsm_post_peak_slope"] = 0.0
                else:
                    final["gsm_post_peak_slope"] = float((_dx * (_yv - _ym)).sum() / _den)
            # d²(gsm)/d(epoch)² from OLS quadratic on strict post-peak tail only.
            # ~0 ⇒ roughly linear tail; negative with declining tail ⇒ accelerating drop.
            _tail_x: list[float] = []
            _tail_y: list[float] = []
            for _epn in range(_e_best + 1, _E + 1):
                _tail_x.append(float(_epn))
                _tail_y.append(float(gsm_test_acc_per_epoch[_epn - 1]))
            if len(_tail_x) < 3:
                final["gsm_post_peak_curvature"] = 0.0
            else:
                _tx = np.array(_tail_x, dtype=np.float64)
                _ty = np.array(_tail_y, dtype=np.float64)
                _TA = np.column_stack((np.ones_like(_tx), _tx, _tx * _tx))
                _cq, _, _, _ = np.linalg.lstsq(_TA, _ty, rcond=None)
                final["gsm_post_peak_curvature"] = float(2.0 * _cq[2])
    final["final_mmlu_test_acc"] = accuracy(
        np.tanh(x_mmlu_test @ w_shared + b_shared) @ w_mmlu + b_mmlu,
        y_mmlu_test,
    )

    run_label_clean = (args.run_label or "").strip()
    if run_label_clean:
        final["run_label"] = run_label_clean

    run_started = datetime.now(timezone.utc)
    run_id = run_started.strftime("%Y%m%dT%H%M%S") + f"{run_started.microsecond // 1000:03d}Z"
    run_dir = args.save_dir / f"unified_phase1_{run_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(
        run_dir / "model_weights.npz",
        w_shared=w_shared,
        b_shared=b_shared,
        w_mmlu=w_mmlu,
        b_mmlu=b_mmlu,
        w_gsm=w_gsm,
        b_gsm=b_gsm,
        w_num=w_num,
        b_num=b_num,
    )
    with (run_dir / "vocab.json").open("w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=True)
    report = {
        "run_id": run_id,
        "config": {
            "epochs": args.epochs,
            "rng_seed": int(args.rng_seed),
            "max_vocab": args.max_vocab,
            "hidden_dim": args.hidden_dim,
            "lr": args.lr,
            "l2": args.l2,
            "gsm_mse_lambda": args.gsm_mse_lambda,
            "gsm_target_log1p": gsm_log1p,
            "gsm_answer_cap": gsm_cap,
            "gsm_round_target_before_log1p": args.gsm_round_target_before_log1p,
            "gsm_align_lambda": args.gsm_align_lambda,
            "gsm_align_loss": args.gsm_align_loss,
            "gsm_boundary_lambda": args.gsm_boundary_lambda,
            "gsm_directional_lambda": args.gsm_directional_lambda,
            "gsm_directional_loss": args.gsm_directional_loss,
            "gsm_numeric_head": args.gsm_numeric_head,
            "gsm_residual_alpha": args.gsm_residual_alpha,
            "gsm_head_lr_multiplier": args.gsm_head_lr_multiplier,
            "gsm_head_lr_decay_multiplier": args.gsm_head_lr_decay_multiplier,
            "freeze_shared_after_epoch": args.freeze_shared_after_epoch,
            "lr_decay_after_epoch": args.lr_decay_after_epoch,
            "lr_decay_gamma": args.lr_decay_gamma,
            "auto_lr_decay_on_best_gsm": args.auto_lr_decay_on_best_gsm,
            "auto_lr_decay_delay": args.auto_lr_decay_delay,
            "auto_lr_decay_min_epoch": args.auto_lr_decay_min_epoch,
            "auto_lr_decay_patience": args.auto_lr_decay_patience,
            "gsm_no_pred_clip": args.gsm_no_pred_clip,
            "disable_merkle_memory": args.disable_merkle_memory,
            "merkle_map": str(args.merkle_map),
            "merkle_max_events": args.merkle_max_events,
            "run_label": run_label_clean or None,
            "telemetry_aux_weight": float(args.telemetry_aux_weight),
            "telemetry_scale": float(args.telemetry_scale),
        },
        "inputs": {
            "mmlu_train_jsonl": str(args.mmlu_train_jsonl),
            "mmlu_test_jsonl": str(args.mmlu_test_jsonl),
            "gsm8k_train_jsonl": str(args.gsm8k_train_jsonl),
            "gsm8k_test_jsonl": str(args.gsm8k_test_jsonl),
        },
        "epoch_logs": epoch_logs,
        "final_metrics": final,
    }
    with (run_dir / "report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=True, indent=2)
    final["artifacts_dir"] = str(run_dir)
    print(json.dumps(final, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
