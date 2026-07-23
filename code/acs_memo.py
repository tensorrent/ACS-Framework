#!/usr/bin/env python3
"""
Disk + in-memory memo for ACS harness numerics (BIE capacitance, Gamow/eigen solves).

RC1: cache is a harness convenience — not a claim about physics uniqueness.
Disable with ACS_MEMO=0. Override root with ACS_MEMO_DIR.

Default root: rh_papers_may21/acs-framework/.cache/
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
from pathlib import Path
from typing import Any, Callable, TypeVar

import numpy as np

T = TypeVar("T")

_FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_ROOT = _FRAMEWORK_ROOT / ".cache"
_LOCK = threading.RLock()
_MEM: dict[str, Any] = {}

# Simple hit/miss counters for benchmark reporting (process-local).
STATS: dict[str, int] = {"hits": 0, "misses": 0, "writes": 0}


def memo_enabled() -> bool:
    return os.environ.get("ACS_MEMO", "1").strip().lower() not in (
        "0",
        "false",
        "off",
        "no",
    )


def memo_root() -> Path:
    override = os.environ.get("ACS_MEMO_DIR", "").strip()
    root = Path(override).expanduser() if override else _DEFAULT_ROOT
    root.mkdir(parents=True, exist_ok=True)
    return root


def reset_stats() -> None:
    STATS["hits"] = 0
    STATS["misses"] = 0
    STATS["writes"] = 0


def clear_memory() -> None:
    with _LOCK:
        _MEM.clear()


def clear_namespace(namespace: str, *, disk: bool = True) -> None:
    """Drop memory entries and optionally disk files for a namespace."""
    prefix = f"{namespace}:"
    with _LOCK:
        for k in list(_MEM):
            if k.startswith(prefix):
                del _MEM[k]
    if disk:
        ns_dir = memo_root() / namespace
        if ns_dir.is_dir():
            for p in ns_dir.iterdir():
                if p.is_file():
                    p.unlink(missing_ok=True)


def key_hash(parts: tuple[Any, ...]) -> str:
    payload = json.dumps(parts, sort_keys=False, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:40]


def _mem_key(namespace: str, digest: str) -> str:
    return f"{namespace}:{digest}"


def _path(namespace: str, digest: str, suffix: str) -> Path:
    d = memo_root() / namespace
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{digest}{suffix}"


def get_json(namespace: str, parts: tuple[Any, ...]) -> Any | None:
    if not memo_enabled():
        return None
    digest = key_hash(parts)
    mk = _mem_key(namespace, digest)
    with _LOCK:
        if mk in _MEM:
            STATS["hits"] += 1
            return _MEM[mk]
    path = _path(namespace, digest, ".json")
    if not path.is_file():
        STATS["misses"] += 1
        return None
    try:
        with path.open("r", encoding="utf-8") as fh:
            value = json.load(fh)
    except (OSError, json.JSONDecodeError):
        STATS["misses"] += 1
        return None
    with _LOCK:
        _MEM[mk] = value
    STATS["hits"] += 1
    return value


def put_json(namespace: str, parts: tuple[Any, ...], value: Any) -> None:
    if not memo_enabled():
        return
    digest = key_hash(parts)
    mk = _mem_key(namespace, digest)
    with _LOCK:
        _MEM[mk] = value
    path = _path(namespace, digest, ".json")
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(value, fh, indent=None, separators=(",", ":"))
    tmp.replace(path)
    STATS["writes"] += 1


def get_npz_solve(namespace: str, parts: tuple[Any, ...]) -> dict[str, Any] | None:
    """Load eigen/Gamow solve: V0, E0, r, u, meta."""
    if not memo_enabled():
        return None
    digest = key_hash(parts)
    mk = _mem_key(namespace, digest)
    with _LOCK:
        if mk in _MEM:
            STATS["hits"] += 1
            return _MEM[mk]
    path = _path(namespace, digest, ".npz")
    if not path.is_file():
        STATS["misses"] += 1
        return None
    try:
        data = np.load(path, allow_pickle=False)
        meta_raw = bytes(data["meta_json"]).decode("utf-8")
        value = {
            "V0": float(data["V0"]),
            "E0": float(data["E0"]),
            "r": np.asarray(data["r"], dtype=float),
            "u": np.asarray(data["u"], dtype=float),
            "meta": json.loads(meta_raw),
        }
    except (OSError, KeyError, ValueError, json.JSONDecodeError):
        STATS["misses"] += 1
        return None
    with _LOCK:
        _MEM[mk] = value
    STATS["hits"] += 1
    return value


def put_npz_solve(
    namespace: str,
    parts: tuple[Any, ...],
    *,
    V0: float,
    E0: float,
    r: np.ndarray,
    u: np.ndarray,
    meta: dict[str, Any],
) -> None:
    if not memo_enabled():
        return
    digest = key_hash(parts)
    mk = _mem_key(namespace, digest)
    value = {
        "V0": float(V0),
        "E0": float(E0),
        "r": np.asarray(r, dtype=float),
        "u": np.asarray(u, dtype=float),
        "meta": dict(meta),
    }
    with _LOCK:
        _MEM[mk] = value
    path = _path(namespace, digest, ".npz")
    tmp = path.with_name(path.stem + ".tmp.npz")
    meta_bytes = json.dumps(meta, separators=(",", ":"), default=float).encode("utf-8")
    np.savez_compressed(
        tmp,
        V0=np.float64(V0),
        E0=np.float64(E0),
        r=np.asarray(r, dtype=np.float64),
        u=np.asarray(u, dtype=np.float64),
        meta_json=np.frombuffer(meta_bytes, dtype=np.uint8),
    )
    tmp.replace(path)
    STATS["writes"] += 1


def cached_json(
    namespace: str,
    parts: tuple[Any, ...],
    compute: Callable[[], T],
) -> T:
    hit = get_json(namespace, parts)
    if hit is not None:
        return hit  # type: ignore[return-value]
    value = compute()
    put_json(namespace, parts, value)
    return value


def fmt_float(x: float, ndigits: int = 12) -> str:
    return format(float(x), f".{ndigits}g")
