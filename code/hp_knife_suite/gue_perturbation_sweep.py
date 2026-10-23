# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
# The sweep is hundreds of mid-sized dense eigvalsh calls.  A multithreaded BLAS on a
# shared machine oversubscribes (one N=1000 complex eigvalsh: 7.2 s threaded vs 0.49 s
# single-threaded, measured under load) and lets thread scheduling touch the last bits.
# An explicit caller setting still wins.
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    _os.environ.setdefault(_v, "1")
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

r"""
GUE PERTURBATION SWEEP  --  Three_Layer_Decomposition.tex sec. 3,
"Spacings are pure GUE, arithmetic-blind (T3)".

The paper: take a GUE core H0 = (A + A^dagger)/2, add a prime-log diagonal at strength
eps, and compare the spacing-histogram distance to the true zeros against the noise band
of pure-GUE draws.  It reports eps=0: 0.0455 (in band); eps=0.05-0.2: 0.044-0.047
(cosmetic); eps=0.4: 0.073 (+2.1 sigma, breaks toward Poisson); eps=0.8: 0.312
(+18.7 sigma).  Claim under test: there is NO SELECTION REGIME (no eps moves the spacing
law toward the zeros).

RECONSTRUCTED.  No script or record of the original run survives in the tree.  The
paper does not state N, the draw count, the binning, the distance, how the diagonal is
scaled against the core, or the unfolding.  They are fixed here, before the first full
run, from house precedent where one exists:

  eps grid    0, 0.05, 0.1, 0.2, 0.4, 0.8   (0.1 is assumed inside the paper's "0.05-0.2")
  core        H0 = (A + A^dagger)/2, A complex Ginibre N x N  (hp_form_function_relativity.py,
              draw_gue_full); the SAME A at every eps (common random numbers)
  N, draws    4000, 40 by default -- that script's dense-GUE frame (not stated in the paper)
  diagonal    Lambda = diag(log p_1 .. log p_N), the first N primes; the order is irrelevant
              because H0 is unitarily invariant
  --scale     core (default): H = H0 + eps*sqrt(N)*Lambda -- eps in units where the core is a
                              radius-2 semicircle (H0/sqrt(N)); the diagonal's spread matches
                              the core's width 4 near eps ~ 0.4 at N = 4000
              raw:            H = H0 + eps*Lambda -- the literal reading of the sentence; the
                              diagonal is then O(1) against a spectrum of radius 2*sqrt(N)
  bulk        middle 80% of levels (draw_gue_full's 10-90% quantile window)
  unfolding   semicircle: centred, standardised, semicircle CDF -- draw_gue_full's unfolding
                          (centring added: the diagonal shifts the spectral mean)
              local:      each spacing / mean of its 2K+1 neighbours, K = 20 -- does not
                          assume the density, so it separates a changed spacing law from
                          a mis-unfolded changed density (the second, distinct method)
  reference   spacings of the first 10^5 zeros: Riemann-von Mangoldt unfolding (semicircle
              column), the same local unfolding (local column)
  distance    sqrt(mean over 40 bins on [0,4] of (h - h_zeros)^2), spacings scaled to unit
              mean -- W_shape's form, with the zeros' histogram in place of the surmise
  band        mean and sd over draws of the eps=0 distance; z(eps) = (mean_eps - mean_0)/sd_0
  verdict     z < 2: in band;  z >= 2: breaks;  z <= -2: SELECTION (closer to zeros than GUE)
  kill rule   "no selection regime" fails at this scale if any eps has z <= -2 under either
              unfolding
  direction   P(s < 0.5), the small-gap fraction (W_repulsion): rising toward Poisson's
              1 - e^{-1/2} = 0.393 is "toward Poisson"

Reproducible: canonical seed 20260423, Odlyzko's first 10^5 zeros.  Negatives kept
first-class.  Writes nothing unless --out is given, and refuses an --out inside the repo.
"""
import sys
import time
import json
import argparse
import numpy as np

SEED = 20260423
EPS = [0.0, 0.05, 0.1, 0.2, 0.4, 0.8]
PAPER = {0.0: "0.0455 (in band)", 0.05: "0.044-0.047", 0.1: "0.044-0.047",
         0.2: "0.044-0.047", 0.4: "0.073 (+2.1sig)", 0.8: "0.312 (+18.7sig)"}
EDGES = np.linspace(0, 4, 41)
BULK = (0.1, 0.9)
K_LOCAL = 20
Z_BREAK = 2.0
REPO = _os.path.realpath(_os.path.join(_HERE, "..", ".."))

def Nsmooth(T):                             # Riemann-von Mangoldt smooth count
    return (T/(2*np.pi))*np.log(T/(2*np.pi)) - T/(2*np.pi) + 7/8

def first_primes(n):
    # p_n < n (ln n + ln ln n) for n >= 6 (Rosser); 15 covers the first six
    lim = 15 if n < 6 else int(n*(np.log(n) + np.log(np.log(n)))) + 1
    sieve = np.ones(lim + 1, bool); sieve[:2] = False
    for i in range(2, int(lim**0.5) + 1):
        if sieve[i]: sieve[i*i::i] = False
    return np.nonzero(sieve)[0][:n]

# ---------- spacing statistics (house W_shape / W_repulsion forms) ----------
def hist(s):
    h, _ = np.histogram(s / s.mean(), bins=EDGES, density=True)
    return h

def dist(h, h_ref):
    return np.sqrt(np.mean((h - h_ref)**2))

def small_gap(s):
    return np.mean(s / s.mean() < 0.5)

def bin_avg(pdf):                           # bin-averaged density on EDGES, renormalised to [0,4]
    x = np.linspace(0, 4, 40*50 + 1); x = 0.5*(x[:-1] + x[1:])
    h = pdf(x).reshape(40, 50).mean(axis=1)
    return h / (h.sum()*(EDGES[1] - EDGES[0]))

# ---------- unfoldings ----------
def bulk(ev):
    n = len(ev)
    return ev[int(BULK[0]*n):int(BULK[1]*n)]

def unfold_semicircle(ev):
    x = bulk((ev - ev.mean()) / ev.std())
    y = np.clip(x/2, -1, 1)
    F = (x*np.sqrt(np.clip(4 - x**2, 0, None))/2 + 2*np.arcsin(y))/(2*np.pi) + 0.5
    return np.diff(F)

def unfold_local(lev, k=K_LOCAL):
    s = np.diff(lev)
    c = np.concatenate([[0.0], np.cumsum(s)])
    m = (c[2*k + 1:] - c[:-2*k - 1]) / (2*k + 1)    # mean of s[i-k .. i+k]
    return s[k:len(s) - k] / m

UNF = {"semicircle": unfold_semicircle,
       "local": lambda ev: unfold_local(bulk(ev))}

def verdict(z):
    return "SELECTION" if z <= -Z_BREAK else ("breaks" if z >= Z_BREAK else "in band")

def main():
    ap = argparse.ArgumentParser(description="GUE + prime-log diagonal spacing sweep "
                                 "(Three_Layer_Decomposition sec. 3, reconstructed)")
    ap.add_argument("--quick", action="store_true", help="smoke run: N=300, 8 draws")
    ap.add_argument("--n", type=int, help="matrix size (default 4000; --quick 300)")
    ap.add_argument("--draws", type=int, help="draws per eps (default 40; --quick 8)")
    ap.add_argument("--scale", choices=("core", "raw"), default="core",
                    help="diagonal scaling convention (see docstring)")
    ap.add_argument("--out", help="also write the table as JSON here (outside the repo)")
    a = ap.parse_args()
    N = a.n or (300 if a.quick else 4000)
    M = a.draws or (8 if a.quick else 40)
    if a.out:
        out = _os.path.realpath(a.out)
        if _os.path.commonpath([out, REPO]) == REPO:
            sys.exit(f"--out {out} is inside the repository {REPO}; point it at a scratch dir")

    g = np.loadtxt(_d("riemann_zeros_100k.txt"))
    REF = {"semicircle": hist(np.diff(Nsmooth(g))), "local": hist(unfold_local(g))}
    P_zero = {"semicircle": small_gap(np.diff(Nsmooth(g))), "local": small_gap(unfold_local(g))}
    poisson = bin_avg(lambda s: np.exp(-s))
    surmise = bin_avg(lambda s: (32/np.pi**2)*s**2*np.exp(-4*s**2/np.pi))

    rng = np.random.default_rng(SEED)
    lam = np.log(first_primes(N).astype(float))
    amp = np.sqrt(N) if a.scale == "core" else 1.0
    idx = np.arange(N)
    D = {u: np.zeros((M, len(EPS))) for u in UNF}
    P = {u: np.zeros((M, len(EPS))) for u in UNF}
    t0 = time.time()
    for i in range(M):
        A = rng.standard_normal((N, N)) + 1j*rng.standard_normal((N, N))
        H = (A + A.conj().T) / 2; del A
        d0 = H.diagonal().copy()
        for j, e in enumerate(EPS):
            H[idx, idx] = d0 + e*amp*lam
            ev = np.linalg.eigvalsh(H)
            for u, unfold in UNF.items():
                s = unfold(ev)
                D[u][i, j] = dist(hist(s), REF[u]); P[u][i, j] = small_gap(s)
        print(f"  draw {i+1}/{M}  {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
    elapsed = time.time() - t0

    print(f"GUE PERTURBATION SWEEP (reconstructed)  --  N = {N}, {M} draws per eps, "
          f"scale '{a.scale}', seed {SEED}")
    print(f"reference: {len(g)} zeros.  H = H0 + eps*{'sqrt(N)*' if a.scale == 'core' else ''}"
          f"diag(log p_1..log p_{N}),  p_{N} = {int(np.exp(lam[-1]) + 0.5)}")
    rows = []
    for u in UNF:
        mu0, sd0 = D[u][:, 0].mean(), D[u][:, 0].std(ddof=1)
        print(f"\nunfolding '{u}':  zeros P(s<.5) = {P_zero[u]:.4f};  dist(Poisson, zeros) = "
              f"{dist(poisson, REF[u]):.4f}, dist(GUE surmise, zeros) = {dist(surmise, REF[u]):.4f}")
        hdr = f"{'eps':>5} | {'dist mean':>9} {'sd':>7} {'z':>7} | {'P(s<.5)':>7} | {'verdict':>9} | paper"
        print(hdr); print("-"*len(hdr))
        for j, e in enumerate(EPS):
            m, sd = D[u][:, j].mean(), D[u][:, j].std(ddof=1)
            z = (m - mu0) / sd0
            pm = P[u][:, j].mean()
            print(f"{e:>5.2f} | {m:>9.4f} {sd:>7.4f} {z:>+7.1f} | {pm:>7.4f} | {verdict(z):>9} | {PAPER[e]}")
            rows.append({"unfolding": u, "eps": e, "dist_mean": m, "dist_sd": sd, "z": z,
                         "small_gap": pm, "verdict": verdict(z), "paper": PAPER[e]})
    sel = [r for r in rows if r["z"] <= -Z_BREAK]
    print(f"\nkill rule (any eps with z <= -{Z_BREAK:.0f}, either unfolding): "
          + ("FIRED -- " + ", ".join(f"{r['unfolding']} eps={r['eps']}" for r in sel) if sel
             else "not fired -- no selection regime at this scale"))
    print(f"elapsed {elapsed:.0f}s ({M*len(EPS)} eigvalsh of {N}x{N} complex)")
    print("NOTE: N, draws, binning, distance, diagonal scale and unfolding are reconstructed"
          " (see docstring);\n      a disagreement with the paper's digits is a statement about"
          " this configuration, not a refutation.")
    if a.out:
        with open(out, "w") as f:
            json.dump({"N": N, "draws": M, "scale": a.scale, "seed": SEED, "eps": EPS,
                       "k_local": K_LOCAL, "elapsed_s": elapsed, "rows": rows}, f, indent=1)

if __name__ == "__main__":
    main()
