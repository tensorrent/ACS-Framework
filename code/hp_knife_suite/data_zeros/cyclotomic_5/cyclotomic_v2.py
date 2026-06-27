"""
Find zeros of L(s, chi_quartic mod 5) via |L|² on critical line.
|L(1/2+it, chi)|² is real, non-negative, and zero exactly at zeros of L.
No gamma-factor decay to confuse the search.
"""
import math, os, time
import numpy as np
from mpmath import mp, mpf, mpc, zeta as mp_zeta
mp.dps = 20

OUTDIR = "/home/claude/cyclotomic_5"
os.makedirs(OUTDIR, exist_ok=True)

i = mpc(0, 1)
chi_list = [mpc(0,0), mpc(1,0), i, i**3, mpc(-1,0)]
print("chi values:", [complex(c) for c in chi_list])

def L_chi(s):
    """L(s, chi_quartic) via Hurwitz."""
    total = mpc(0)
    for a in range(1, 5):
        total += chi_list[a] * mp_zeta(s, mpf(a)/5)
    return mpf(5)**(-s) * total

def absL_sq(t):
    """|L(1/2+it, chi)|^2 = L · conjugate(L), real."""
    L = L_chi(mpc(0.5, t))
    return float(L.real**2 + L.imag**2)

# Scan
T_MAX = 100.0
DT = 0.05
t_vals = np.arange(0.01, T_MAX, DT)
print(f"Scanning {len(t_vals)} points...")
abs_sq = np.zeros(len(t_vals))
t0 = time.time()
for k, t in enumerate(t_vals):
    if k % 500 == 0 and k > 0:
        print(f"  {k}/{len(t_vals)}  rate={k/(time.time()-t0):.0f}/s")
    abs_sq[k] = absL_sq(float(t))
print(f"Scan done in {time.time()-t0:.1f}s")

# Find local minima
mins = []
for k in range(1, len(abs_sq)-1):
    if abs_sq[k] < abs_sq[k-1] and abs_sq[k] < abs_sq[k+1]:
        mins.append(k)

# Genuine zeros: local minima where |L|² is small (no exp decay so we can use absolute threshold)
print(f"Total local minima: {len(mins)}")
threshold = 0.5  # heuristic for "close to zero" of |L|^2
candidate_zeros = [k for k in mins if abs_sq[k] < threshold]
print(f"Candidate zeros (|L|² < {threshold}): {len(candidate_zeros)}")

# Refine each candidate
def find_zero_near(t_guess, dt=0.05):
    """Refine zero of |L|² near t_guess using fine bisection."""
    t_best = t_guess
    val_best = absL_sq(t_best)
    # Try a few iterations of golden-section-like reduction
    for _ in range(50):
        h = max(dt/10, 1e-8)
        v_plus = absL_sq(t_best + h)
        v_minus = absL_sq(t_best - h)
        if v_plus < val_best and v_plus < v_minus:
            t_best += h
            val_best = v_plus
        elif v_minus < val_best:
            t_best -= h
            val_best = v_minus
        else:
            dt = dt / 2
            if dt < 1e-10: break
    return t_best, val_best

zeros = []
for k in candidate_zeros:
    t_guess = float(t_vals[k])
    t_zero, val = find_zero_near(t_guess, DT)
    if val < 1e-3:  # actual zero (sqrt of |L|^2 < 0.03)
        zeros.append(t_zero)

# Dedupe close ones
zeros = np.array(sorted(zeros))
if len(zeros) > 1:
    diffs = np.diff(zeros)
    zeros = zeros[np.concatenate([[True], diffs > 0.05])]

print(f"\nRefined zeros: {len(zeros)}")
print(f"First 15: {[f'{z:.4f}' for z in zeros[:15]]}")
print(f"Last 5: {[f'{z:.4f}' for z in zeros[-5:]]}")

# Verify
print("\nVerification (|L|² at zeros):")
for z in zeros[:10]:
    val = absL_sq(z)
    print(f"  t={z:.4f}  |L|²={val:.2e}  |L|={math.sqrt(val):.2e}")

# Predicted count (Riemann-von Mangoldt for L of conductor q)
predicted = (T_MAX/(2*math.pi)) * math.log(5*T_MAX/(2*math.pi)) - T_MAX/(2*math.pi)
print(f"\nPredicted count: ~{predicted:.0f}")
print(f"Observed: {len(zeros)}")

np.savetxt(f"{OUTDIR}/zeros_chi_5_order4.txt", zeros, fmt='%.10f')
