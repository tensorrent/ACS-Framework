# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

r"""
HARMONIC-LADDER LAW  --  does the arithmetic face obey the p^{-k/2} trace-formula weight?

hp_vantage_points.py found the arithmetic witness carries a harmonic ladder: a resonance
at log p (k=1, 'arith') AND at 2 log p (k=2, 'arith2', 41 sigma, independent). For a
Hilbert-Polya operator whose periodic orbits are the primes, arith2 is the k=2 REPETITION
(the p^2 prime-power line), and the Riemann-Weil explicit formula fixes its amplitude:

    |F(log p^k)|  ~  Lambda(p^k) / sqrt(p^k)  =  log(p) / p^{k/2}      (C7)

with F(u) = sum_gamma cos(u gamma)  (the signed witness of hp_signed_lfunction.py).

Since Lambda(p) = Lambda(p^2) = log p, the log p cancels in the ratio and the k=2/k=1
line ratio is a PURE, parameter-free prediction:

    |F(2 log p)| / |F(log p)|  =  p^{-1/2}      (slope -1/2 in log-log vs p)

If the ladder obeys this, the HP constraint "prime orbits appear with all repetitions at
the standard r-fold amplitude" is confirmed, not merely asserted. If not, the k=2 signal
is something other than the prime-power repetition. Test both the RATIO law (slope -1/2)
and the ABSOLUTE weight law (|F(log n)| ~ Lambda(n)/sqrt(n), slope 1) on real zeros.

Reproducible: canonical seed 20260423, Odlyzko's first zeros. Negatives first-class.
"""
import numpy as np

SEED = 20260423
rng = np.random.default_rng(SEED)

g = np.loadtxt(_d("riemann_zeros_100k.txt"))
N = len(g)

def F(uu):                                   # signed witness F(u) = sum_gamma cos(u*gamma)
    uu = np.atleast_1d(np.asarray(uu, float))
    return np.cos(np.outer(uu, g)).sum(axis=1)

# Peak amplitude at frequency u0, with a LOCAL BACKGROUND subtracted so we measure the
# arithmetic spike, not the smooth density term. Background = mean of F at nearby offsets
# that are NOT themselves prime-power log-frequencies.
PRIME_POW_LOGS = np.log([p**k for p in
    [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47] for k in (1,2,3)])
def _is_ppfreq(u, tol=0.02):
    return np.any(np.abs(PRIME_POW_LOGS - u) < tol)

def peak(u0, halfwidth=0.15, nb=12):
    offs = np.linspace(-halfwidth, halfwidth, nb+1)
    bg_us = [u0 + o for o in offs if abs(o) > 0.03 and not _is_ppfreq(u0 + o)]
    vals = F([u0] + bg_us)
    center, bg = vals[0], vals[1:]
    return center - bg.mean()                # signed excess (should be NEGATIVE at p^k)

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

print(f"HARMONIC-LADDER LAW  --  N = {N} zeros, seed {SEED}")
print("=" * 70)
print("Signed excess F at the k=1 (log p) and k=2 (2 log p) prime lines")
print(f"{'p':>4} {'A1=F(log p)':>13} {'A2=F(2log p)':>13} {'|A2/A1|':>9} {'p^-1/2':>9}")

A1, A2, ratio, pm12 = [], [], [], []
for p in PRIMES:
    a1 = peak(np.log(p))
    a2 = peak(2 * np.log(p))
    r = abs(a2) / abs(a1)
    A1.append(a1); A2.append(a2); ratio.append(r); pm12.append(p**-0.5)
    print(f"{p:>4} {a1:>13.1f} {a2:>13.1f} {r:>9.3f} {p**-0.5:>9.3f}")

A1 = np.array(A1); A2 = np.array(A2); ratio = np.array(ratio)

# ---- sign check: both lines should be NEGATIVE (C6) ----
neg1 = np.mean(A1 < 0); neg2 = np.mean(A2 < 0)
print(f"\nC6 sign: fraction NEGATIVE  k=1: {neg1:.2f}   k=2: {neg2:.2f}   (want 1.00)")

# ---- RATIO law: log|A2/A1| vs log p  ->  slope should be -0.5 ----
x = np.log(PRIMES)
y = np.log(ratio)
slope, intercept = np.polyfit(x, y, 1)
yhat = slope * x + intercept
ss_res = np.sum((y - yhat)**2); ss_tot = np.sum((y - y.mean())**2)
R2 = 1 - ss_res/ss_tot
print("\n" + "=" * 70)
print("RATIO LAW   |F(2log p)| / |F(log p)|  =  p^{-1/2}")
print(f"  log-log fit slope = {slope:+.3f}   (trace-formula prediction: -0.500)")
print(f"  intercept         = {intercept:+.3f}   (prediction: 0.000)")
print(f"  R^2               = {R2:.3f}")

# ---- ABSOLUTE weight law: |F(log n)| ~ Lambda(n)/sqrt(n) across BOTH harmonics ----
weights = ([np.log(p)/np.sqrt(p) for p in PRIMES]        # k=1
           + [np.log(p)/p for p in PRIMES])              # k=2
amps = list(np.abs(A1)) + list(np.abs(A2))
lw, la = np.log(weights), np.log(amps)
wslope, wint = np.polyfit(lw, la, 1)
wcorr = np.corrcoef(lw, la)[0, 1]
print("\nABSOLUTE WEIGHT LAW   |F(log n)|  ~  Lambda(n)/sqrt(n)")
print(f"  log-log fit slope = {wslope:+.3f}   (prediction: +1.000)")
print(f"  corr(log|F|, log Lambda/sqrt(n)) = {wcorr:.3f}   (want ~1)")

# ---- null control: same ratio on a GUE-marginal surrogate (should be structureless) ----
def surrogate():
    def Nsmooth(T): return (T/(2*np.pi))*np.log(T/(2*np.pi)) - T/(2*np.pi) + 7/8
    w = Nsmooth(g); s = np.diff(w); s = rng.permutation(s)
    ws = np.concatenate([[w[0]], w[0] + np.cumsum(s)])
    return np.interp(ws, w, g)
g_surr = surrogate()
def Fs(uu):
    uu = np.atleast_1d(np.asarray(uu, float))
    return np.cos(np.outer(uu, g_surr)).sum(axis=1)
# reuse peak() machinery on the surrogate by swapping the module-level g
_g_real = g
def peak_on(arr, u0, halfwidth=0.15, nb=12):
    offs = np.linspace(-halfwidth, halfwidth, nb+1)
    bg_us = [u0 + o for o in offs if abs(o) > 0.03 and not _is_ppfreq(u0 + o)]
    us = np.array([u0] + bg_us)
    vals = np.cos(np.outer(us, arr)).sum(axis=1)
    return vals[0] - vals[1:].mean()
sr = np.array([abs(peak_on(g_surr, 2*np.log(p))) / (abs(peak_on(g_surr, np.log(p)))+1e-9)
               for p in PRIMES])
s_slope = np.polyfit(np.log(PRIMES), np.log(sr + 1e-12), 1)[0]
print(f"\nNULL CONTROL (GUE-marginal surrogate): ratio-law slope = {s_slope:+.3f}")
print("  (no prime structure -> no p^{-1/2} law; slope should NOT sit near -0.5)")

print("\n" + "=" * 70)
ok_ratio = abs(slope + 0.5) < 0.12
ok_weight = abs(wslope - 1.0) < 0.25 and wcorr > 0.9
print("VERDICT")
print(f"  ratio law slope {slope:+.3f} vs -0.5 : {'CONFIRMED' if ok_ratio else 'off'}")
print(f"  absolute weight slope {wslope:+.3f} vs +1.0, corr {wcorr:.2f} : "
      f"{'CONFIRMED' if ok_weight else 'off'}")
print(f"""  => The arithmetic face's harmonic ladder {'obeys' if ok_ratio else 'does NOT obey'} the
     p^-k/2 trace-formula weight. This is the r-fold repetition amplitude of the
     prime periodic orbits: a Hilbert-Polya operator matching the zeros must carry
     the primes as orbit lengths WITH their repetitions at exactly this weighting.
     (A necessary spectral condition on H -- it does not construct H, and proves
     nothing about RH.)""")
