"""
Cyclotomic Q(zeta_5) — first non-quadratic field test.

The Dedekind zeta factorizes as:
  zeta_K(s) = zeta(s) · L(s, chi^1) · L(s, chi^2) · L(s, chi^3)
where chi is a primitive character of order 4 mod 5:
  chi(1) = 1, chi(2) = i, chi(3) = -i, chi(4) = -1

chi^2 = chi_5 (quadratic character we already have)
chi^3 = chi^(-1) = conjugate of chi^1

This file computes the zeros of L(s, chi^1) — a COMPLEX L-function.

For complex chi, Lambda(s, chi) is not real on critical line. We find zeros via
either: (1) sign changes of Re and Im separately, requiring both to vanish, or
(2) minima of |Lambda|^2 = Lambda · Lambda_bar = |L|^2 × gamma factor product.

L(s, chi̅) = conjugate of L(s, chi) for real s+it. So |L(1/2+it, chi)|^2 is real.
"""
import math, os, time
import numpy as np
from mpmath import mp, mpf, mpc, zeta as mp_zeta, gamma as mp_gamma, pi as mp_pi
mp.dps = 20

OUTDIR = "/home/claude/cyclotomic_5"
os.makedirs(OUTDIR, exist_ok=True)

# Primitive character of order 4 mod 5
# (Z/5Z)* is cyclic of order 4. Generator is 2 (since 2^1=2, 2^2=4, 2^3=3, 2^4=1 mod 5).
# chi(2) = i, chi(2^k) = i^k
i = mpc(0, 1)
chi_list = [
    mpc(0, 0),     # chi(0)
    mpc(1, 0),     # chi(1) = i^0 = 1
    i,             # chi(2) = i
    i**3,          # chi(3) = chi(2^3) = i^3 = -i
    mpc(-1, 0),    # chi(4) = chi(2^2) = i^2 = -1
]
print("chi values mod 5 (order-4 character):")
for n, v in enumerate(chi_list):
    print(f"  chi({n}) = {complex(v)}")

# Verify oddness
print(f"\nchi(-1) = chi(4) = {complex(chi_list[4])} (should be -1 for ODD character)")

# L(s, chi) via Hurwitz zeta
def L_chi(s):
    """L(s, chi) = q^{-s} sum chi(a) zeta(s, a/q), q=5."""
    total = mpc(0)
    for a in range(1, 5):
        total += chi_list[a] * mp_zeta(s, mpf(a)/5)
    return mpf(5)**(-s) * total

# Sanity check at s=1: L(1, chi) for complex character involves Gauss sums
# For chi of order 4 mod 5, L(1, chi) = ?
# L(1, chi) = -(1/q) sum chi(a) ψ(a/q) where ψ is digamma
# For odd character: L(1, chi) = -(iπ/q) sum chi(a) cot(π a/q) / ... 
# Simpler: just compute numerically
test_L1 = L_chi(1)
print(f"\nL(1, chi) = {complex(test_L1)}")

# Completed L-function. Chi is ODD, so gamma factor is Gamma((s+1)/2)
def Lambda_chi(s):
    """Lambda(s, chi) = (q/pi)^(s/2) Gamma((s+1)/2) L(s, chi)"""
    return (mpf(5) / mp_pi) ** (s/2) * mp_gamma((s + 1) / 2) * L_chi(s)

# Test Lambda
for t in [0, 5, 10, 20]:
    s = mpc(0.5, t)
    L = Lambda_chi(s)
    print(f"Lambda(1/2 + {t}i) = {complex(L)}")

# To find zeros: find minima of |Lambda|^2 that touch zero
# Equivalently: find sign changes of Re(Lambda) AND Im(Lambda) simultaneously

# Strategy: scan, find regions where |Lambda|^2 is small, then bisect
print("\nScanning for zeros (this involves searching for minima of |Lambda|^2)...")

T_MAX = 100.0
DT = 0.05
t_vals = np.arange(0.01, T_MAX, DT)
abs_Lambda = np.zeros(len(t_vals))
re_Lambda = np.zeros(len(t_vals))
im_Lambda = np.zeros(len(t_vals))

t0 = time.time()
for k, t in enumerate(t_vals):
    if k % 500 == 0 and k > 0:
        elapsed = time.time() - t0
        print(f"  {k}/{len(t_vals)}  rate={k/elapsed:.0f}/s")
    L_val = Lambda_chi(mpc(0.5, t))
    re_Lambda[k] = float(L_val.real)
    im_Lambda[k] = float(L_val.imag)
    abs_Lambda[k] = math.sqrt(re_Lambda[k]**2 + im_Lambda[k]**2)
print(f"Scan done in {time.time()-t0:.1f}s")

# Find local minima of |Lambda|
# A zero is a point where both Re and Im vanish, i.e. |Lambda| → 0
# Look for local minima where |Lambda| is small
min_indices = []
for k in range(1, len(t_vals)-1):
    if abs_Lambda[k] < abs_Lambda[k-1] and abs_Lambda[k] < abs_Lambda[k+1]:
        if abs_Lambda[k] < 0.05:  # threshold for "close to zero"
            min_indices.append(k)
print(f"Found {len(min_indices)} candidate minima")

# Refine each candidate by Newton-like iteration on |Lambda|^2
# Or just check the value is small
def Lambda_at_t(t):
    return Lambda_chi(mpc(0.5, t))

zeros_chi = []
for k in min_indices:
    t_init = t_vals[k]
    # Local search: refine to find precise zero
    # Use simultaneous bisection on Re and Im — find where |Lambda|^2 is minimum
    # Just use minimize via finer grid then check
    fine_t = np.linspace(t_init - DT, t_init + DT, 21)
    fine_abs = [abs(Lambda_at_t(float(t))) for t in fine_t]
    best_idx = np.argmin(fine_abs)
    t_best = float(fine_t[best_idx])
    # Refine further
    for _ in range(30):
        L_val = Lambda_at_t(t_best)
        if abs(L_val) < 1e-10:
            break
        # Newton step on |Lambda|^2 by central diff
        h = 1e-4
        L_plus = Lambda_at_t(t_best + h)
        L_minus = Lambda_at_t(t_best - h)
        deriv_abs_sq = (abs(L_plus)**2 - abs(L_minus)**2) / (2*h)
        if abs(deriv_abs_sq) < 1e-20:
            break
        # Step proportional to current |L|
        step = -float(L_val.real * L_plus.real + L_val.imag * L_plus.imag) / (
            float(L_plus.real**2 + L_plus.imag**2 + 1e-30))
        # Simpler: just take a small step toward smaller |L|
        delta = h * (1 if deriv_abs_sq < 0 else -1) * min(abs(L_val), 1.0)
        t_new = t_best + delta
        L_new = Lambda_at_t(t_new)
        if abs(L_new) < abs(L_val):
            t_best = t_new
        else:
            # binary search
            delta = delta / 2
            if abs(delta) < 1e-12:
                break
    zeros_chi.append(t_best)

zeros_chi = np.array(sorted(zeros_chi))
diffs = np.diff(zeros_chi)
zeros_chi = zeros_chi[np.concatenate([[True], diffs > 0.1])]
print(f"\nRefined zeros: {len(zeros_chi)}")
print(f"First 10: {zeros_chi[:10]}")
print(f"Range: [{zeros_chi[0]:.3f}, {zeros_chi[-1]:.3f}]")

# Verify: |Lambda| at each zero should be near 0
print("\nVerification (|Lambda| at zeros, should be ≈ 0):")
for z in zeros_chi[:10]:
    val = abs(Lambda_at_t(float(z)))
    print(f"  t={z:.4f}  |Lambda|={val:.2e}")

np.savetxt(f"{OUTDIR}/zeros_chi_5_order4.txt", zeros_chi, fmt='%.10f')
print(f"\nSaved to {OUTDIR}/zeros_chi_5_order4.txt")

# Density check for complex L-function:
# N(T) ≈ (T/(2π)) log(qT/(2π e)) + (T/(2π)) log(2) (approximate)
predicted_count = (T_MAX/(2*math.pi)) * math.log(5*T_MAX/(2*math.pi)) - T_MAX/(2*math.pi)
print(f"\nPredicted count to T={T_MAX}: ~{predicted_count:.0f}")
print(f"Observed: {len(zeros_chi)}")
