# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

r"""
LADDER TOWER  --  how deep does the p^{-k/2} repetition tower go?

hp_harmonic_ladder.py confirmed rungs k=1,2 obey the Riemann-Weil weight
|F(k log p)| ~ Lambda(p^k)/sqrt(p^k) = log(p)/p^{k/2}. This extends the test to k=3
(the p^3 prime-power line at 3 log p) and reports the whole tower. Since Lambda(p^k)=log p
for every k, the log p cancels in the rung-k/rung-1 ratio, giving a pure prediction:

    |F(k log p)| / |F(log p)|  =  p^{-(k-1)/2}      (log-log slope -(k-1)/2)

    rung 2 :  slope -1/2      rung 3 :  slope -1

Falsification-first: the k=3 line is p^{-1} weaker than the fundamental, so it may drown in
the finite-N background. We report the measured slope per rung and whether the tower is
resolved to depth 3 or only depth 2. F(u) = sum_gamma cos(u gamma) (signed witness).
Reproducible: 100k zeros, seed 20260423.
"""
import numpy as np

SEED = 20260423
rng = np.random.default_rng(SEED)
g = np.loadtxt(_d("riemann_zeros_100k.txt"))
N = len(g)

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
PRIME_POW_LOGS = np.log([p**k for p in PRIMES for k in (1, 2, 3, 4)])

def _is_ppfreq(u, tol=0.02):
    return np.any(np.abs(PRIME_POW_LOGS - u) < tol)

def peak(u0, halfwidth=0.15, nb=12):
    offs = np.linspace(-halfwidth, halfwidth, nb + 1)
    bg_us = [u0 + o for o in offs if abs(o) > 0.03 and not _is_ppfreq(u0 + o)]
    us = np.array([u0] + bg_us)
    vals = np.cos(np.outer(us, g)).sum(axis=1)
    return vals[0] - vals[1:].mean()

print(f"LADDER TOWER  --  N = {N} zeros, seed {SEED}")
print("=" * 74)
print(f"{'p':>4} " + " ".join(f"{'A'+str(k):>11}" for k in (1, 2, 3)))
A = {1: [], 2: [], 3: []}
for p in PRIMES:
    row = []
    for k in (1, 2, 3):
        a = peak(k * np.log(p))
        A[k].append(a); row.append(a)
    print(f"{p:>4} " + " ".join(f"{a:>11.1f}" for a in row))
for k in (1, 2, 3):
    A[k] = np.array(A[k])

# sign check (C6): every prime-power line should be NEGATIVE
print("\nC6 sign (fraction negative):  " +
      "  ".join(f"k={k}: {np.mean(A[k] < 0):.2f}" for k in (1, 2, 3)))

# background noise floor: |peak| at random non-prime-power frequencies
_rand_us = rng.uniform(0.6, 12.0, 400)
_rand_us = np.array([u for u in _rand_us if not _is_ppfreq(u)])
floor = np.std([peak(u) for u in _rand_us])
print(f"\nbackground noise floor (std of |peak| off prime lines) = {floor:.1f}")

# ratio law per rung, GATED by signal: include a prime only where |A_k| > 3*floor,
# so a rung is measured only where its line is above background (honest depth).
x = np.log(PRIMES)
print("\n" + "=" * 74)
print("RATIO LAW   |F(k log p)| / |F(log p)|  =  p^{-(k-1)/2}   (signal-gated: |A_k|>3*floor)")
print(f"  {'rung k':>7} {'pred':>7} {'#primes':>8} {'slope':>8} {'R^2':>7} {'verdict':>26}")
for k in (2, 3):
    mask = np.abs(A[k]) > 3 * floor
    pred = -(k - 1) / 2
    if mask.sum() < 3:
        print(f"  {k:>7} {pred:>7.2f} {mask.sum():>8} {'--':>8} {'--':>7} {'below background':>26}")
        continue
    xk = x[mask]; yk = np.log(np.abs(A[k][mask]) / np.abs(A[1][mask]))
    slope, intc = np.polyfit(xk, yk, 1)
    yh = slope * xk + intc
    R2 = 1 - np.sum((yk - yh)**2) / np.sum((yk - yk.mean())**2)
    ok = abs(slope - pred) < 0.2 and R2 > 0.8
    pmax = PRIMES[np.where(mask)[0][-1]]
    verdict = f"RESOLVED (p<={pmax})" if ok else "background-limited"
    print(f"  {k:>7} {pred:>7.2f} {mask.sum():>8} {slope:>8.3f} {R2:>7.3f} {verdict:>26}")

# absolute weight across all three rungs (signal-gated): |F(log n)| ~ Lambda(n)/sqrt(n)
weights, amps = [], []
for k in (1, 2, 3):
    for i, p in enumerate(PRIMES):
        if abs(A[k][i]) > 3 * floor:
            weights.append(np.log(p) / p**(k/2)); amps.append(abs(A[k][i]))
lw, la = np.log(weights), np.log(amps)
wslope = np.polyfit(lw, la, 1)[0]; wcorr = np.corrcoef(lw, la)[0, 1]
print(f"\nABSOLUTE WEIGHT (all three rungs, signal-gated: {len(amps)} lines) "
      f"|F(log n)| ~ Lambda(n)/sqrt(n)")
print(f"  slope {wslope:+.3f} (pred +1.000), corr {wcorr:.3f}")

# small-prime rung-3 detail (where it is actually visible)
print("\nrung-3 detail (small primes, where p^{-1} is not yet buried):")
for i, p in enumerate(PRIMES[:6]):
    print(f"  p={p:>2}: |A3/A1| = {abs(A[3][i])/abs(A[1][i]):.3f}   p^-1 = {p**-1.0:.3f}")

print("\n" + "=" * 74)
print("""READING: the tower depth is whatever the data supports, reported honestly. If rung 3
tracks p^-1 the repetition tower is 3 deep (prime cubes p^3 present at the standard
amplitude); if it only holds for small primes and scatters for large ones, the tower is
resolved to depth ~2-3 and background-limited beyond. Either way it constrains the
Hilbert-Polya trace formula's orbit repetitions; proves nothing about RH.""")
