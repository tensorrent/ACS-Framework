#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Issue #7: Section 9 exact (no IEEE float) kill test.

Float-free analogue of the TFIM cone-leakage diagnostic.

Model (classical 1D Ising + discrete local influence):
  Energy E[σ] = -J * sum_i σ_i σ_{i+1} - h * sum_i σ_i ,  σ_i ∈ {±1}
  Boltzmann weight w(σ) = B**(-E) with integer B ≥ 2  (exact integer weights)

Observables (all over Z / Q via Fraction):
  - gap: integer classical excitation gap E1 - E0
  - cluster_weight: sum_r r * |C(r)|  with C connected ZZ correlators (Fraction)
  - outside_cone_affect: max Fraction of configs where flipping site 0
    changes site r after t steps of a local majority update, for r > t + margin

Decision rule (exact, no float):
  Support requires sign(cov(gap, cluster_weight)) < 0 AND
                 sign(cov(gap, outside_cone_affect)) < 0
  over the parameter sweep, using Fraction covariance (sign only).

No IEEE float on the decision path. Printing may convert Fraction→str for display.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from pathlib import Path
import json


def spins_from_bits(bits: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(1 if b else -1 for b in bits)


def energy(spins: tuple[int, ...], j: int, h: int) -> int:
    n = len(spins)
    e = 0
    for i in range(n - 1):
        e -= j * spins[i] * spins[i + 1]
    for s in spins:
        e -= h * s
    return e


def all_configs(n: int) -> list[tuple[int, ...]]:
    return [spins_from_bits(bits) for bits in product((0, 1), repeat=n)]


def Boltzmann_weights(configs: list[tuple[int, ...]], j: int, h: int, b: int) -> list[int]:
    # w = B**(-E) = B**(Emax - E) / B**Emax  — use relative integers B**(-E)
    # Store unnormalized weight as B**(-E); keep as int via B**(Emax-E)
    energies = [energy(cfg, j, h) for cfg in configs]
    emax = max(energies)
    return [b ** (emax - e) for e in energies]


def exact_gap(configs: list[tuple[int, ...]], j: int, h: int) -> int:
    energies = sorted({energy(cfg, j, h) for cfg in configs})
    if len(energies) < 2:
        return 0
    return energies[1] - energies[0]


def connected_correlators(
    configs: list[tuple[int, ...]], weights: list[int], n: int
) -> list[Fraction]:
    z = sum(weights)
    # <σ0>, <σr>, <σ0 σr>
    exp0 = Fraction(sum(w * cfg[0] for cfg, w in zip(configs, weights)), z)
    out: list[Fraction] = []
    for r in range(1, n):
        expr = Fraction(sum(w * cfg[r] for cfg, w in zip(configs, weights)), z)
        exp0r = Fraction(sum(w * cfg[0] * cfg[r] for cfg, w in zip(configs, weights)), z)
        out.append(abs(exp0r - exp0 * expr))
    return out


def cluster_weight(corrs: list[Fraction]) -> Fraction:
    return sum((r + 1) * c for r, c in enumerate(corrs))


def majority_update(spins: tuple[int, ...]) -> tuple[int, ...]:
    """Synchronous local majority with open boundaries (deterministic, exact)."""
    n = len(spins)
    nxt = []
    for i in range(n):
        left = spins[i - 1] if i > 0 else spins[i]
        right = spins[i + 1] if i + 1 < n else spins[i]
        s = left + spins[i] + right
        nxt.append(1 if s > 0 else -1 if s < 0 else spins[i])
    return tuple(nxt)


def evolve(spins: tuple[int, ...], steps: int) -> tuple[int, ...]:
    cur = spins
    for _ in range(steps):
        cur = majority_update(cur)
    return cur


def outside_cone_affect(
    configs: list[tuple[int, ...]], n: int, t_max: int, margin: int = 0
) -> Fraction:
    """
    Exact influence: Fraction of configs where flipping site 0 changes some
    site r with r > t + margin after exactly t steps, maximized over t.
    """
    total = len(configs)
    worst = Fraction(0)
    for t in range(0, t_max + 1):
        affected = 0
        for cfg in configs:
            flipped = (-cfg[0],) + cfg[1:]
            a = evolve(cfg, t)
            b = evolve(flipped, t)
            for r in range(n):
                if r > t + margin and a[r] != b[r]:
                    affected += 1
                    break
        frac = Fraction(affected, total)
        if frac > worst:
            worst = frac
    return worst


def cov_sign(xs: list[int] | list[Fraction], ys: list[Fraction] | list[int]) -> int:
    """Return -1, 0, +1 for sign of Fraction covariance. No float."""
    n = len(xs)
    assert n == len(ys) and n >= 2
    xf = [Fraction(x) for x in xs]
    yf = [Fraction(y) for y in ys]
    mx = sum(xf) / n
    my = sum(yf) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xf, yf)) / n
    if cov > 0:
        return 1
    if cov < 0:
        return -1
    return 0


def run_sweep(n: int = 8, j: int = 1, b: int = 2) -> dict:
    configs = all_configs(n)
    h_values = list(range(0, 6))
    rows = []
    for h in h_values:
        weights = Boltzmann_weights(configs, j, h, b)
        gap = exact_gap(configs, j, h)
        corrs = connected_correlators(configs, weights, n)
        cw = cluster_weight(corrs)
        leak = outside_cone_affect(configs, n, t_max=n - 1, margin=0)
        rows.append(
            {
                "h": h,
                "gap": gap,
                "cluster_weight": str(cw),
                "cluster_weight_num": cw.numerator,
                "cluster_weight_den": cw.denominator,
                "outside_cone_affect": str(leak),
                "outside_cone_affect_num": leak.numerator,
                "outside_cone_affect_den": leak.denominator,
            }
        )

    gaps = [r["gap"] for r in rows]
    cws = [Fraction(r["cluster_weight_num"], r["cluster_weight_den"]) for r in rows]
    leaks = [
        Fraction(r["outside_cone_affect_num"], r["outside_cone_affect_den"]) for r in rows
    ]
    sign_gap_cw = cov_sign(gaps, cws)
    sign_gap_leak = cov_sign(gaps, leaks)
    supports = sign_gap_cw < 0 and sign_gap_leak < 0

    return {
        "model": "classical_ising_exact_fraction",
        "settings": {"n": n, "j": j, "b": b, "h_values": h_values},
        "rows": rows,
        "summary": {
            "sign_cov_gap_cluster": sign_gap_cw,
            "sign_cov_gap_outside_affect": sign_gap_leak,
            "supports_chain": supports,
        },
        "float_free": True,
        "decision_path": "Fraction covariance signs only",
    }


def main() -> None:
    result = run_sweep()
    out = (
        Path(__file__).resolve().parents[2] / "docs" / "issue7_section9_exact_results.json"
    )
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    s = result["summary"]
    print("Section 9 exact (no IEEE float) kill test")
    print(f"Model: classical Ising N={result['settings']['n']}, B={result['settings']['b']}")
    print("h  gap  cluster_weight  outside_cone_affect")
    for r in result["rows"]:
        print(
            f"{r['h']:>1}  {r['gap']:>3}  {r['cluster_weight']:>16}  {r['outside_cone_affect']:>16}"
        )
    print(
        f"sign cov(gap, cluster_weight) = {s['sign_cov_gap_cluster']:+d}  (expect -1)"
    )
    print(
        f"sign cov(gap, outside_affect) = {s['sign_cov_gap_outside_affect']:+d}  (expect -1)"
    )
    if s["supports_chain"]:
        print("RESULT: exact data supports the chain direction.")
    else:
        print("RESULT: exact data does not support a robust monotone chain.")
    print(f"artifact: docs/issue7_section9_exact_results.json")


if __name__ == "__main__":
    main()
