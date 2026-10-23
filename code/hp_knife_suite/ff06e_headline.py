# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

r"""
FF06e HEADLINE  --  the five-witness shuffle-knife table of
papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex (Sec. 3) as a runnable driver.

The paper reports z at N = 10^5 (and z_arith, z_lag1 at N = 2x10^4) with 60 surrogates,
seed 20260423, and names no script.  hp_vantage_points.py carries the same surrogate and
three of the five witnesses (arith, lag1, shape) but is fixed at N = 4000 with 300
surrogates and reads repulsion/rigidity where the paper reads spacing-mean and counting
deviation; hp_knife.py is a different witness (|sum cos(gamma log n)|, n <= 40) on a
raw-height gap shuffle with no unfolding.  This driver runs the paper's protocol at any N.

Surrogate (paper Sec. 2 + its 2026-07-02 remark): permute the unfolded spacings,
re-accumulate from u0[0], re-interpolate onto the real (u0, gamma) grid, re-unfold.
This is hp_vantage_points.draw_gue_marginal with N as a parameter.

Witnesses.  arith / lag1 / shape are hp_vantage_points.W_arith / W_lag1 / W_shape,
copied verbatim: that module runs its whole 300-surrogate study at import, so it cannot
be imported.  The paper gives no formula for "spacing mean deviation" or "counting
deviation"; the two below are RECONSTRUCTED readings.  Both depend only on the window
endpoints, which the re-interpolation surrogate preserves to rounding, so their
surrogate sigma sits at the float floor and their z is a ratio of rounding noise -- it is
printed, flagged, and must not be read as a measurement.

Reproducible: seed 20260423, one default_rng stream per N, K draws in order.
Prints to stdout only; writes nothing.
"""
import argparse
import time

import numpy as np

SEED = 20260423
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
LOGP = np.log(PRIMES)

def Nsmooth(T):
    return (T/(2*np.pi))*np.log(T/(2*np.pi)) - T/(2*np.pi) + 7/8

# =====================================================================================
#  THE FIVE WITNESSES
# =====================================================================================
def W_arith(gam):                    # prime resonance on ACTUAL heights (= hp_vantage_points)
    return sum(np.mean(np.cos(gam*lp))**2 for lp in LOGP)

def W_lag1(s):                       # serial order (= hp_vantage_points)
    s = s - s.mean(); return np.sum(s[:-1]*s[1:]) / np.sum(s*s)

def W_shape(s):                      # Wigner-surmise L2 (= hp_vantage_points)
    s = s / s.mean()
    edges = np.linspace(0, 4, 41); ctr = 0.5*(edges[:-1]+edges[1:])
    h, _ = np.histogram(s, bins=edges, density=True)
    wig = (32/np.pi**2) * ctr**2 * np.exp(-4*ctr**2/np.pi)
    return np.sqrt(np.mean((h - wig)**2))

def W_spacing_mean(s):               # RECONSTRUCTED: unfolded mean spacing vs 1
    return abs(s.mean() - 1.0)

def W_counting(gam, w):              # RECONSTRUCTED: count N(gamma_N) vs smooth count, relative
    return abs(len(gam) - w[-1]) / len(gam)

WITNESSES = ["arith", "lag1", "spacing_mean", "counting", "shape"]

def evaluate(gam):
    w = Nsmooth(gam); s = np.diff(w)
    return {"arith": W_arith(gam), "lag1": W_lag1(s), "spacing_mean": W_spacing_mean(s),
            "counting": W_counting(gam, w), "shape": W_shape(s)}

# The paper's printed cells, (W_real, W_shuf mean, z); None where it prints nothing.
PAPER = {
    100000: {"arith": (0.0636, 1.0e-5, 11497), "lag1": (-0.357, -1.0e-3, 97),
             "spacing_mean": (0.0000, 0.0000, 1.0), "counting": (1e-5, 1e-5, 1.0),
             "shape": (0.0258, 0.0258, 0.4)},
    20000: {"arith": (0.0922, None, 3030), "lag1": (None, None, 51)},
}

# =====================================================================================
#  THE KNIFE
# =====================================================================================
def knife(g_all, N, K, seed):
    """Real-vs-surrogate table at N; returns {witness: (real, mean, sd, z, float_floor)}."""
    rng = np.random.default_rng(seed)
    g = g_all[:N].copy()
    w_real = Nsmooth(g); s_real = np.diff(w_real)

    def draw():                      # marginal-matched: permute, re-accumulate, re-interpolate
        s = rng.permutation(s_real)
        w = np.concatenate([[w_real[0]], w_real[0] + np.cumsum(s)])
        return np.interp(w, w_real, g)

    real = evaluate(g)
    ens = {k: np.empty(K) for k in WITNESSES}
    for m in range(K):
        wv = evaluate(draw())
        for k in WITNESSES: ens[k][m] = wv[k]

    out = {}
    for k in WITNESSES:
        mu, sd = ens[k].mean(), ens[k].std()
        # sigma at the rounding floor means the witness is surrogate-invariant: its z
        # standardises one rounding error by another and carries no information
        floor = sd <= 1e-12 * max(1.0, abs(mu))
        z = abs(real[k] - mu) / sd if sd > 0 else float("nan")
        out[k] = (real[k], mu, sd, z, floor)
    return out

def show(N, K, seed, res, secs):
    paper = PAPER.get(N, {})
    print(f"\nN = {N} zeros, K = {K} surrogates, seed {seed}, wall {secs:.2f} s")
    print(f"  {'witness':>12} {'W_real':>11} {'W_shuf':>11} {'sigma':>10} {'z':>10}"
          f"  {'category':>11} | {'paper W_real':>12} {'paper z':>8} {'z/z_paper-1':>11}")
    for k in WITNESSES:
        real, mu, sd, z, floor = res[k]
        cat = "float floor" if floor else ("FUNCTION" if z > 3 else "FORM")
        pr, _, pz = paper.get(k, (None, None, None))
        dev = f"{z/pz - 1:+.1%}" if (pz is not None and not floor) else "-"
        print(f"  {k:>12} {real:11.4e} {mu:11.4e} {sd:10.3e} {z:10.1f}  {cat:>11} | "
              f"{('-' if pr is None else f'{pr:.4g}'):>12} {('-' if pz is None else f'{pz:g}'):>8}"
              f" {dev:>11}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="FF06e five-witness shuffle-knife table")
    ap.add_argument("--n", type=int, nargs="+", default=[4000, 20000, 100000])
    ap.add_argument("--surrogates", type=int, default=60)
    ap.add_argument("--seed", type=int, default=SEED)
    a = ap.parse_args()

    g_all = np.loadtxt(_d("riemann_zeros_100k.txt"))
    print(f"FF06e headline -- {len(g_all)} zeros on file; protocol: permute unfolded "
          f"spacings, re-accumulate, re-interpolate")
    for N in a.n:
        if N > len(g_all):
            raise SystemExit(f"N = {N} exceeds the {len(g_all)} zeros on file")
        t0 = time.perf_counter()
        res = knife(g_all, N, a.surrogates, a.seed)
        show(N, a.surrogates, a.seed, res, time.perf_counter() - t0)
