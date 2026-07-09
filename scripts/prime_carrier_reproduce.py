#!/usr/bin/env python3
"""
prime_carrier_reproduce.py
Reproduces every table in papers/methodology/Prime_Carrier_Position_Form_Factor.tex (FF06f).

Claim under test: the zeta prime-resonance functional
    P(f) = (1/N) | sum_j exp(-i f gamma_j) |^2 ,   measured at f = log p,
is a linear functional of the VALUE-SPACE PAIR CORRELATION of the zero POSITIONS,
i.e. the single-realisation spectral form factor. It is a two-point statistic --- of
the positions, not the spacings. Reconstructing P from that pair correlation recovers
100% exactly; spacing/index two-point surrogates recover ~7%; and the form-factor peaks
sit at prime-power frequencies with heights ~ (Lambda(n)/sqrt n)^2 (the explicit formula).

Data: code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt (shipped in this repo).
Canonical seed 20260423. prime_peak_power reused verbatim from the shuffle-knife suite.
No external deps beyond numpy. Run from anywhere inside the repo:  python3 scripts/prime_carrier_reproduce.py
"""
import os
import numpy as np

rng = np.random.default_rng(20260423)

# --- locate the shipped zeros file relative to the repo root, independent of cwd ---
def find_zeros():
    here = os.path.dirname(os.path.abspath(__file__))
    d = here
    for _ in range(6):
        cand = os.path.join(d, "code", "hp_knife_suite", "data_zeros", "riemann_zeros_100k.txt")
        if os.path.exists(cand):
            return cand
        d = os.path.dirname(d)
    raise FileNotFoundError("riemann_zeros_100k.txt not found under repo code/hp_knife_suite/data_zeros/")

Z = np.loadtxt(find_zeros())

FREQS6 = np.array([np.log(p) for p in [2, 3, 5, 7, 11, 13]])

def prime_peak_power(x, freqs=FREQS6):
    """Shuffle-knife prime-resonance witness: (1/N) sum_f |sum_j exp(-i f x_j)|^2."""
    return sum(abs(np.sum(np.exp(-1j * f * x)))**2 for f in freqs) / len(x)

def positions_from_spacings(s, x0):
    x = np.empty(len(s) + 1); x[0] = x0; x[1:] = x0 + np.cumsum(s)
    return x

def phase_random(a):
    """Surrogate preserving a power spectrum (== a two-point autocovariance), phases destroyed."""
    m = a.mean(); F = np.fft.rfft(a - m)
    ph = rng.uniform(0, 2*np.pi, len(F)); ph[0] = 0.0
    if len(a) % 2 == 0: ph[-1] = 0.0
    return np.fft.irfft(np.abs(F) * np.exp(1j*ph), n=len(a)) + m

def vonmangoldt(n):
    if n < 2: return 0.0
    m, p, primes = n, 2, []
    while p*p <= m:
        if m % p == 0:
            primes.append(p)
            while m % p == 0: m //= p
        p += 1
    if m > 1: primes.append(m)
    return np.log(primes[0]) if len(primes) == 1 else 0.0   # prime power <=> single distinct prime

def hr(t): print("\n" + "=" * 70 + "\n" + t + "\n" + "=" * 70)

# Each table re-seeds so its numbers are reproducible independent of run order.
def reseed():
    global rng
    rng = np.random.default_rng(20260423)

# ---------------------------------------------------------------- Table 1 (N=200)
reseed()
hr("TABLE 1 — which two-point object carries the signal (N=200, 300 trials)")
N = 200; z = Z[:N]; s = np.diff(z)
base = prime_peak_power(z)
floor = np.mean([prime_peak_power(positions_from_spacings(rng.permutation(s), z[0])) for _ in range(300)])
gap2  = np.mean([prime_peak_power(positions_from_spacings(phase_random(s), z[0])) for _ in range(300)])
j = np.arange(N); trend = np.polyval(np.polyfit(j, z, 5), j); fluct = z - trend
idx2  = np.mean([prime_peak_power(trend + phase_random(fluct)) for _ in range(300)])
pair_exact = sum(np.sum(np.cos(f*(z[:, None]-z[None, :]))) for f in FREQS6) / N
hist, edges = np.histogram((z[:, None]-z[None, :]).ravel(), bins=4000)
centers = 0.5*(edges[:-1]+edges[1:])
pair_bin = sum(np.sum(hist*np.cos(f*centers)) for f in FREQS6) / N
pois = np.mean([prime_peak_power(positions_from_spacings(rng.exponential(s.mean(), N-1), z[0])) for _ in range(300)])
for name, v in [("ordered baseline", base), ("spacing shuffle (1-point)", floor),
                ("gap 2-point (C)", gap2), ("index 2-point (D)", idx2),
                ("value-space pair-corr (E, exact)", pair_exact),
                ("value-space pair-corr (E, 4000-bin)", pair_bin), ("Poisson null (calib)", pois)]:
    print(f"  {name:38} {v:9.3f}  ({100*v/base:5.1f}%)")
print(f"  CALIBRATION: pair-corr reproduces baseline exactly? {'PASS' if abs(pair_exact-base)/base < 1e-9 else 'FAIL'}")

# ---------------------------------------------------------------- Table 2 (explicit formula)
hr("TABLE 2 — form-factor peaks vs explicit-formula weight Lambda(n)/sqrt(n) (N=4000)")
N = 4000; z = Z[:N]
fgrid = np.linspace(0.5, np.log(40)+0.05, 6000)
K = np.array([abs(np.sum(np.exp(-1j*f*z)))**2 for f in fgrid]) / N
meas_pp, pred_pp, comps = [], [], []
print(f"  {'n':>3} {'type':<14} {'height':>8} {'Lambda/sqrt(n)':>14}")
for n in range(2, 34):
    k = np.argmin(np.abs(fgrid - np.log(n)))
    h = K[max(0, k-8):k+9].max()
    lam = vonmangoldt(n)
    if lam > 0:
        meas_pp.append(h); pred_pp.append((lam/np.sqrt(n))**2)
        if n in (4,5,7,8,9,11,13,16,25,27,32):
            print(f"  {n:>3} {'prime power' if not (lam and n in (5,7,11,13)) else 'prime':<14} {h:8.2f} {lam/np.sqrt(n):14.3f}")
    else:
        comps.append(h)
r = np.corrcoef(meas_pp, pred_pp)[0, 1]
print(f"\n  Pearson r(height, (Lambda/sqrt n)^2) = {r:.4f}")
print(f"  mean height  prime-power = {np.mean(meas_pp):.2f}   composite = {np.mean(comps):.2f}")

# ---------------------------------------------------------------- Table 3 (N-robustness)
reseed()
hr("TABLE 3 — robustness in N (baseline vs shuffle floor, 200 trials)")
print(f"  {'N':>6} {'baseline':>10} {'floor':>7} {'separation':>11}")
for N in [200, 500, 1000, 2000, 5000, 10000]:
    z = Z[:N]; s = np.diff(z)
    b = prime_peak_power(z)
    fl = np.mean([prime_peak_power(positions_from_spacings(rng.permutation(s), z[0])) for _ in range(200)])
    print(f"  {N:>6} {b:10.3f} {fl:7.3f} {b/fl:9.1f}x")

# ---------------------------------------------------------------- Table 4 (mechanism)
reseed()
hr("MECHANISM — gap 2-point is preserved yet the primes are lost (N=2000)")
N = 2000; z = Z[:N]; s = np.diff(z); sr = phase_random(s)
acov = lambda a: [float(np.mean((a-a.mean())[:-L]*(a-a.mean())[L:])) for L in (1, 2, 3)]
print(f"  gap autocovariance lag(1,2,3) original : {[round(v,4) for v in acov(s)]}")
print(f"  gap autocovariance lag(1,2,3) surrogate: {[round(v,4) for v in acov(sr)]}  (preserved)")
print(f"  prime power ordered   : {prime_peak_power(z):.3f}")
print(f"  prime power surrogate : {prime_peak_power(positions_from_spacings(sr, z[0])):.3f}  (collapses)")
print("\nDone. See papers/methodology/Prime_Carrier_Position_Form_Factor.tex for interpretation.")
