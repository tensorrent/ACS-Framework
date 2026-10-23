# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
RECONSTRUCTED 2026-10-22 from the ledger's description, NOT the original.

Original: `/tmp/q5_hp.py`, run 2026-06-06 on an external session machine and never
committed (docs/Elimination_Ledger.md:209, provenance note :14-21). Re-authored from the
ledger entry "Target Q5: Hilbert-Polya operator candidates" (docs/Elimination_Ledger.md:
207-235) only. Agreement below is agreement with the recorded outputs; it does not certify
the original script, and it does not upgrade the ledger's RMT-universality caveat (:220).

What the ledger states (and this file implements):
  * data: "zeta zeros 10000-40000", "RvM-smooth unfolding" (:209);
  * outputs: unfolded-spacing L2 distance to GUE / GSE / GOE / Poisson
    (7.31e-2 / 1.72e-1 / 2.26e-1 / 6.52e-1), fitted repulsion exponent beta = 2.12,
    spacing variance 0.1600 ("reproduces record 0.1607") (:215-217);
  * xp smooth count (T/2pi)(log(T/2pi) - 1) vs the actual staircase: ratios
    0.998 / 1.00001 / 0.99998 at T = 1e3 / 1e4 / 5e4 (:224-226).

What the ledger does NOT state, so both readings / several choices are printed:
  * whether "10000-40000" means zero INDICES or HEIGHTS -> both windows are run;
  * whether unfolded spacings were renormalised to mean 1 -> raw and renormalised;
  * the L2 definition -> histogram density on [0,4] vs the Wigner surmises, with
    L2 = sqrt(sum (h - p)^2 ds), at two bin widths; a GUE-surmise sampling noise floor
    (seed 20260423) is printed so a residual can be read against sampling error;
  * the beta estimator -> (i) the suite's committed convention
    (code/hp_knife_suite/hp_operator_constraint.py:51-65, count(s'<s) ~ s^(beta+1) on
    s in [0.02, 0.30]); (ii) a log-log fit of the histogram density on small s.
Data: the committed table code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt
(first 100,000 zeros). Writes nothing; stdout only. `--scan` prints a POST HOC sweep of L2
conventions (see convention_scan) instead of the default report.
"""
import os
import sys

import numpy as np

SEED = 20260423
HERE = os.path.dirname(os.path.abspath(__file__))
ZEROS_FILE = os.path.join(HERE, "..", "data_zeros", "riemann_zeros_100k.txt")


def n_smooth(t):
    """Riemann-von Mangoldt smooth count, including the 7/8 constant."""
    return (t / (2 * np.pi)) * np.log(t / (2 * np.pi)) - t / (2 * np.pi) + 7 / 8


def n_xp(t):
    """Berry-Keating xp semiclassical count, as the ledger writes it (:223)."""
    return (t / (2 * np.pi)) * (np.log(t / (2 * np.pi)) - 1)


SURMISE = {
    "GUE": lambda s: (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi),
    "GSE": lambda s: (2**18 / (3**6 * np.pi**3)) * s**4 * np.exp(-64 * s**2 / (9 * np.pi)),
    "GOE": lambda s: (np.pi / 2) * s * np.exp(-np.pi * s**2 / 4),
    "Poisson": lambda s: np.exp(-s),
}


def l2_to(spacings, pdf, width, smax=4.0):
    edges = np.arange(0.0, smax + width / 2, width)
    h, _ = np.histogram(spacings, bins=edges, density=False)
    h = h / (len(spacings) * width)  # density normalised to ALL spacings, not just those < smax
    c = 0.5 * (edges[:-1] + edges[1:])
    return float(np.sqrt(np.sum((h - pdf(c)) ** 2) * width))


def beta_suite(s):
    """Committed suite convention (hp_operator_constraint.py:61-65)."""
    svals = np.linspace(0.02, 0.30, 25)
    counts = np.array([np.sum(s < sv) for sv in svals], dtype=float)
    good = counts > 30
    slope, _ = np.polyfit(np.log(svals[good]), np.log(counts[good]), 1)
    return slope - 1.0, int(good.sum())


def beta_density(s, smax=0.5, width=0.05):
    edges = np.arange(0.0, smax + width / 2, width)
    h, _ = np.histogram(s, bins=edges)
    c = 0.5 * (edges[:-1] + edges[1:])
    ok = h > 0
    slope, _ = np.polyfit(np.log(c[ok]), np.log(h[ok] / (len(s) * width)), 1)
    return slope


def gue_surmise_sample(rng, n):
    grid = np.linspace(0.0, 6.0, 60001)
    cdf = np.cumsum(SURMISE["GUE"](grid))
    cdf /= cdf[-1]
    return np.interp(rng.random(n), cdf, grid)


def window_report(label, g, rng):
    w = n_smooth(g)
    raw = np.diff(w)
    ren = raw / raw.mean()
    print(f"[{label}]  zeros {len(g)}  heights {g[0]:.3f} .. {g[-1]:.3f}  spacings {len(raw)}")
    print(f"  mean unfolded spacing (raw RvM)       = {raw.mean():.6f}")
    print(f"  variance, raw RvM-unfolded            = {raw.var():.4f}")
    print(f"  variance, renormalised to mean 1      = {ren.var():.4f}")
    for width in (0.05, 0.10):
        cells = "  ".join(f"{k} {l2_to(ren, f, width):.3e}" for k, f in SURMISE.items())
        print(f"  L2 (bin {width:.2f}, renormalised): {cells}")
    noise = [l2_to(gue_surmise_sample(rng, len(ren)), SURMISE["GUE"], 0.05) for _ in range(200)]
    print(f"  GUE-surmise sampling noise floor (bin 0.05, n={len(ren)}, 200 draws): "
          f"median {np.median(noise):.3e}, 95th pct {np.percentile(noise, 95):.3e}")
    b1, npts = beta_suite(ren)
    b2 = beta_density(ren)
    print(f"  beta, suite convention (count ~ s^(beta+1), {npts} pts)  = {b1:.3f}")
    print(f"  beta, log-log density fit on s < 0.5                = {b2:.3f}")
    print()


def convention_scan(g):
    """POST HOC (--scan): which histogram conventions land near the ledger's L2 cells?

    Chosen after seeing the default output, so it locates the ledger's numbers inside a
    space of conventions; it does not identify the original's method.
    """
    target = np.array([7.31e-2, 1.72e-1, 2.26e-1, 6.52e-1])
    cells = []
    for lab, gg in (("A", g[9999:40000]), ("B", g[(g >= 1e4) & (g <= 4e4)])):
        s = np.diff(n_smooth(gg))
        s = s / s.mean()
        for width in (0.02, 0.05, 0.10, 0.20):
            for smax in (3.0, 4.0, 5.0):
                for norm in ("all", "in-range"):
                    for ev in ("centre", "bin-average"):
                        e = np.arange(0.0, smax + width / 2, width)
                        h, _ = np.histogram(s, bins=e)
                        h = h / ((len(s) if norm == "all" else h.sum()) * width)
                        c = 0.5 * (e[:-1] + e[1:])
                        fine = np.linspace(0.0, 1.0, 41)
                        row = []
                        for f in SURMISE.values():
                            if ev == "centre":
                                p = f(c)
                            else:  # mean of the pdf over each bin, 41-point trapezoid
                                p = np.array([np.trapezoid(f(a + width * fine), fine) for a in e[:-1]])
                            row.append(np.sqrt(np.sum((h - p) ** 2) * width))
                        cells.append(((lab, width, smax, norm, ev), np.array(row)))
    arr = np.array([r for _, r in cells])
    print(f"POST HOC convention scan: {len(cells)} cells "
          "(window A/B x bin 0.02/0.05/0.10/0.20 x range 3/4/5 x norm x evaluation)")
    for i, k in enumerate(SURMISE):
        print(f"  {k:<8} min {arr[:, i].min():.4f}  max {arr[:, i].max():.4f}  ledger {target[i]:.4f}")
    best = int(np.argmin(np.sum((arr - target) ** 2, axis=1)))
    print(f"  closest cell to the ledger: {cells[best][0]} -> "
          + "  ".join(f"{v:.4f}" for v in cells[best][1]))
    print()


def main():
    rng = np.random.default_rng(SEED)
    g = np.loadtxt(ZEROS_FILE)
    if "--scan" in sys.argv[1:]:
        convention_scan(g)
        return
    print("Q5 Hilbert-Polya class test -- RECONSTRUCTION (not the 2026-06-06 original)")
    print("=" * 78)
    print(f"table: {len(g)} zeros, max height {g[-1]:.3f}")
    print()
    window_report("reading A: zero indices 10000..40000", g[9999:40000], rng)
    window_report("reading B: heights 10000 <= gamma <= 40000", g[(g >= 1e4) & (g <= 4e4)], rng)

    print("xp smooth count vs actual staircase (ratio N_xp(T) / N_actual(T)):")
    for T in (1e3, 1e4, 5e4):
        n_act = int(np.sum(g <= T))
        print(f"  T = {T:>8.0f}: N_xp = {n_xp(T):12.4f}  N_actual = {n_act:6d}  ratio = {n_xp(T) / n_act:.6f}")
    print()
    print("Ledger cells (docs/Elimination_Ledger.md:215-217, :224-226) for comparison:")
    print("  L2 GUE 7.31e-2, GSE 1.72e-1, GOE 2.26e-1, Poisson 6.52e-1; beta 2.12; variance 0.1600")
    print("  xp ratios 0.998 / 1.00001 / 0.99998 at T = 1e3 / 1e4 / 5e4")


if __name__ == "__main__":
    main()
