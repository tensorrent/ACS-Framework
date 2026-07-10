#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
F_N STATIONARITY AT N=200 ZEROS
Scale the variance test from N=25 to N=200.
"""
from mpmath import mp, zetazero, cos, log, sqrt, mpf, fsum, pi
import numpy as np
import time

mp.dps = 25  # 25 digits sufficient for this

print("=" * 70)
print("F_N STATIONARITY TEST: N = 25, 50, 100, 150, 200")
print("=" * 70)

# Pre-compute zeros
print("\nComputing Riemann zeros...")
t0 = time.time()

N_max = 200
zeros = []
for k in range(1, N_max + 1):
    if k % 50 == 0:
        print(f"  Zero {k}/{N_max}...")
    z = zetazero(k)
    zeros.append(float(z.imag))

print(f"  {N_max} zeros computed in {time.time()-t0:.1f}s")
print(f"  γ_1 = {zeros[0]:.6f}, γ_{N_max} = {zeros[-1]:.6f}")

# Compute F_N variance over [X, 2X] segments
def F_N_values(zeros_list, sigma, x_points):
    """Compute F_N(x) = Σ A_k x^{σ-1/2} cos(γ_k log x) at given points."""
    vals = np.zeros(len(x_points))
    for gamma in zeros_list:
        A_k = 1.0 / (sigma**2 + gamma**2)
        for i, x in enumerate(x_points):
            vals[i] += A_k * x**(sigma - 0.5) * np.cos(gamma * np.log(x))
    return vals

def variance_over_segment(zeros_list, sigma, X, n_pts=500):
    """Compute Var[F_N] over [X, 2X]."""
    x_pts = np.linspace(X, 2*X, n_pts)
    F_vals = F_N_values(zeros_list, sigma, x_pts)
    return np.var(F_vals)

# Test stationarity: variance should be BOUNDED for σ=1/2 (on-line)
# and GROWING for σ≠1/2 (off-line)

print(f"\n── Stationarity Test ──\n")

N_tests = [25, 50, 100, 150, 200]
X_tests = [100, 1000, 10000]

print(f"  {'N':<6}", end="")
for X in X_tests:
    print(f"  {'Var(σ=.5)':<14} {'Var(σ=.6)':<14} {'Ratio':<10}", end="")
print()
print(f"  {'-'*80}")

for N in N_tests:
    z_N = zeros[:N]
    print(f"  {N:<6}", end="")
    for X in X_tests:
        var_on = variance_over_segment(z_N, 0.5, X, n_pts=200)
        var_off = variance_over_segment(z_N, 0.6, X, n_pts=200)
        ratio = var_off / max(var_on, 1e-30)
        print(f"  {var_on:<14.6f} {var_off:<14.6f} {ratio:<10.1f}", end="")
    print()

print(f"""
  INTERPRETATION:
  - σ = 0.5 (on critical line): variance stays BOUNDED as X grows
  - σ = 0.6 (off critical line): variance GROWS as X^{{0.2}} 
  - Ratio (off/on) should increase with X if RH is true
  
  If ratio grows consistently across all N values, this confirms
  that stationarity holds for N up to 200 zeros.
""")

# Final variance growth test
print("── Variance Growth Rate ──\n")
X_range = [100, 300, 1000, 3000, 10000, 30000]

print(f"  N=200 zeros, σ=0.5 vs σ=0.6:\n")
print(f"  {'X':<10} {'Var(σ=.5)':<14} {'Var(σ=.6)':<14} {'Ratio':<10} {'log₁₀(Ratio)':<14}")
print(f"  {'-'*62}")

for X in X_range:
    v5 = variance_over_segment(zeros[:200], 0.5, X, n_pts=200)
    v6 = variance_over_segment(zeros[:200], 0.6, X, n_pts=200)
    r = v6 / max(v5, 1e-30)
    lr = np.log10(max(r, 1e-30))
    print(f"  {X:<10} {v5:<14.6f} {v6:<14.6f} {r:<10.1f} {lr:<14.2f}")

print(f"\n  If stationarity holds: Var(σ=0.5) bounded, Var(σ=0.6) ~ X^0.2")
print(f"  → Ratio grows as X^0.2 → log₁₀(Ratio) ~ 0.2 log₁₀(X)")
