"""
Reproducibility seed.

Single source of truth for random seed used throughout the codebase.
Set to the date of the project audit (2026-04-23).

Usage:
  from src.common.seed import default_rng
  rng = default_rng()         # canonical RNG
  rng = default_rng(seed=42)  # custom seed
"""
import numpy as np

CANONICAL_SEED = 20260423


def default_rng(seed=None):
    """Return a numpy Generator seeded with the canonical seed by default."""
    if seed is None:
        seed = CANONICAL_SEED
    return np.random.default_rng(seed)
