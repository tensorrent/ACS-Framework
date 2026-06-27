"""Q(zeta_7) — phase channel recovery for order-6 character.

The 6 character values are 6th roots of unity:
  chi(1) = 1                            phase = 0
  chi(3) = ω = (1+i√3)/2               phase = π/3 (60°)
  chi(2) = ω² = (-1+i√3)/2             phase = 2π/3 (120°)
  chi(6) = ω³ = -1                      phase = π (180°)
  chi(4) = ω⁴ = (-1-i√3)/2             phase = 4π/3 (240°)
  chi(5) = ω⁵ = (1-i√3)/2              phase = 5π/3 (300°)

Predicted F at log(p) = -chi(p) × amplitude
So F should land at phase = π + arg(chi(p)).
"""
import math, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

OUTDIR = "/home/claude/cyclotomic_7"
zeros = np.loadtxt(f"{OUTDIR}/zeros_chi_7_order6.txt")
print(f"L(s, chi_7 order 6) zeros: N = {len(zeros)}")

# Order-6 character mod 7
# 3 is generator, chi(3) = ω = e^{2πi/6}
# Discrete log: chi(n) = ω^{log_3(n) mod 6}
disc_log = {1: 0, 3: 1, 2: 2, 6: 3, 4: 4, 5: 5}

def chi_7_order6(p):
    """Order-6 character mod 7. Returns complex value."""
    r = p % 7
    if r == 0: return 0 + 0j
    k = disc_log[r]
    return complex(math.cos(2*math.pi*k/6), math.sin(2*math.pi*k/6))

def sieve(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2, n+1):
        if s[i]:
            for j in range(i*i, n+1, i): s[j]=False
    return [i for i in range(n+1) if s[i]]
primes = sieve(1000)

# F_cos and F_sin
omega_grid = np.linspace(0.5, 5.0, 2000)
F_cos = np.array([np.sum(np.cos(om * zeros))/len(zeros) for om in omega_grid])
F_sin = np.array([np.sum(np.sin(om * zeros))/len(zeros) for om in omega_grid])

# Now examine each prime
print("\np    p%7  chi(p)               F_cos(log p)  F_sin(log p)  F_mag    expected -chi phase")
print("-" * 110)
results_by_class = {}
for p in primes[:30]:
    if p == 7: continue
    lp = math.log(p)
    if lp > 5: break
    chi_p = chi_7_order6(p)
    idx = np.argmin(np.abs(omega_grid - lp))
    fc = F_cos[idx]
    fs = F_sin[idx]
    fmag = math.sqrt(fc**2 + fs**2)
    # Predicted: -chi(p) × amp, so phase = π + arg(chi_p)
    obs_phase_deg = math.degrees(math.atan2(fs, fc)) if fmag > 0.01 else None
    pred_phase_deg = math.degrees(math.atan2(-chi_p.imag, -chi_p.real))
    p_mod = p % 7
    if p_mod not in results_by_class:
        results_by_class[p_mod] = []
    results_by_class[p_mod].append((p, fc, fs, fmag))
    obs_str = f"{obs_phase_deg:+.0f}°" if obs_phase_deg is not None else "n/a"
    print(f"{p:<4} {p_mod:<4} {chi_p.real:+.3f}{chi_p.imag:+.3f}i    {fc:+.4f}      {fs:+.4f}      {fmag:.4f}  pred {pred_phase_deg:+.0f}° obs {obs_str}")

# Mean per class
print("\n=== Mean F_cos, F_sin per character class ===")
print("p mod 7  chi(p)                Mean F_cos   Mean F_sin   Mean phase (deg)")
print("-" * 90)
class_means = []
for r in [1, 3, 2, 6, 4, 5]:  # ordered by chi power (0, 1, 2, 3, 4, 5)
    if r not in results_by_class: continue
    rows = results_by_class[r]
    mean_fc = np.mean([row[1] for row in rows])
    mean_fs = np.mean([row[2] for row in rows])
    chi_val = chi_7_order6(r)
    pred_phase = math.degrees(math.atan2(-chi_val.imag, -chi_val.real))
    obs_phase = math.degrees(math.atan2(mean_fs, mean_fc))
    class_means.append((r, chi_val, mean_fc, mean_fs, len(rows), pred_phase, obs_phase))
    print(f"  {r}      {chi_val.real:+.3f}{chi_val.imag:+.3f}i      {mean_fc:+.4f}     {mean_fs:+.4f}     pred {pred_phase:+.0f}, obs {obs_phase:+.0f}")

# Compute phase recovery quality
print("\n=== Phase recovery quality ===")
print("class  pred_phase  obs_phase  diff (deg)")
total_diff = 0
for r, chi_val, mfc, mfs, n, pred, obs in class_means:
    diff = abs(obs - pred)
    if diff > 180: diff = 360 - diff
    total_diff += diff
    print(f"  {r}    {pred:+6.1f}°    {obs:+6.1f}°    {diff:5.1f}°")
print(f"Mean absolute phase error: {total_diff/len(class_means):.1f}°")

# Save data
F_mag = np.sqrt(F_cos**2 + F_sin**2)
np.savez(f"{OUTDIR}/cyclotomic_7_data.npz",
         zeros=zeros, omega=omega_grid, F_cos=F_cos, F_sin=F_sin, F_mag=F_mag)
print(f"\nData saved.")
