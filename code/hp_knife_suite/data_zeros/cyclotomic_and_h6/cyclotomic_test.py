"""
Cyclotomic Q(zeta_5) - test framework on complex L-function.

The order-4 character chi mod 5:
  chi(1) = 1 (split completely in Q(ζ_5))
  chi(2) = i (cyclic shift of order 4)
  chi(3) = -i
  chi(4) = -1
  chi(5) = 0 (ramified)

For complex chi, the explicit formula involves COMPLEX coefficients:
  Σ_zeros e^{i ω γ_k} ≈ -2 Σ_n χ(n) Λ(n)/√n × (delta at log n = ω)
  
Since chi(p) is complex, we expect BOTH cos and sin components to encode info.

F_cos(ω) = (1/N) Σ cos(ω γ_k)
F_sin(ω) = (1/N) Σ sin(ω γ_k)

At log(p): F_cos picks up Re(chi(p)) · weight
            F_sin picks up Im(chi(p)) · weight (or similar — with signs)

For p ≡ 1 mod 5: chi(p) = 1, expect F_cos peak, F_sin = 0
For p ≡ 4 mod 5: chi(p) = -1, expect -F_cos peak, F_sin = 0  
For p ≡ 2 mod 5: chi(p) = i, expect F_cos = 0, F_sin peak
For p ≡ 3 mod 5: chi(p) = -i, expect F_cos = 0, -F_sin peak
"""
import math, os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

OUTDIR = "/home/claude/cyclotomic"
zeros = np.loadtxt(f"{OUTDIR}/zeros_chi_5_order4.txt")
print(f"L(s, chi_5^1) order-4 zeros: N = {len(zeros)}")

def chi_5_order4(p):
    """Order-4 character mod 5. Returns complex value."""
    if p % 5 == 0: return 0
    r = p % 5
    # chi(1)=1, chi(2)=i, chi(3)=-i, chi(4)=-1
    if r == 1: return 1 + 0j
    if r == 2: return 0 + 1j
    if r == 3: return 0 - 1j
    if r == 4: return -1 + 0j

def sieve(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2, n+1):
        if s[i]:
            for j in range(i*i, n+1, i): s[j]=False
    return [i for i in range(n+1) if s[i]]
primes = sieve(1000)

# F_cos and F_sin
omega = np.linspace(0.5, 5.0, 2000)
F_cos = np.array([np.sum(np.cos(om * zeros))/len(zeros) for om in omega])
F_sin = np.array([np.sum(np.sin(om * zeros))/len(zeros) for om in omega])

# Test: at log(p), F_cos should track Re(chi(p)), F_sin should track Im(chi(p))
# (with overall sign depending on explicit formula convention)
print("\n--- Behavior at log(p) for each chi class ---")
print("\np    p%5   chi      F_cos(log p)   F_sin(log p)   Re(chi)   Im(chi)")
print("-" * 80)

results = {'p1': [], 'p4': [], 'p2': [], 'p3': []}  # by p mod 5

for p in primes[:25]:
    if p == 5: continue
    lp = math.log(p)
    if lp > 5: break
    chi_p = chi_5_order4(p)
    idx = np.argmin(np.abs(omega - lp))
    fc = F_cos[idx]
    fs = F_sin[idx]
    print(f"{p:<4} {p%5:<6} {chi_p}    {fc:+.4f}        {fs:+.4f}       {chi_p.real:+.0f}     {chi_p.imag:+.0f}")
    key = f'p{p%5}'
    results[key].append((p, fc, fs))

print("\n--- Mean amplitudes by character class ---")
for k in ['p1', 'p2', 'p3', 'p4']:
    if results[k]:
        mean_fc = np.mean([r[1] for r in results[k]])
        mean_fs = np.mean([r[2] for r in results[k]])
        print(f"  p ≡ {k[1]} mod 5: mean F_cos = {mean_fc:+.4f}, mean F_sin = {mean_fs:+.4f}, count {len(results[k])}")

# The actual prediction from explicit formula:
# For complex chi, the relation depends on functional equation phase.
# In our Z(t) setup, we rotated by e^{-i arg(eps)/2}, so the explicit-formula
# coefficient at log(p) gets a phase factor.
#
# The clean test: which character classes produce LARGEST |F_cos| vs |F_sin|?
# This is what reveals the character's complex structure.

print("\n--- Sign/phase analysis ---")
# For p ≡ 1 (chi = +1): we expect a pure real signal (cos peak, sin ~0)
# For p ≡ 4 (chi = -1): pure real signal (cos peak with opposite sign)
# For p ≡ 2 (chi = +i): pure imaginary -> sin peak
# For p ≡ 3 (chi = -i): pure imaginary -> -sin peak

# Total signal at each prime:
mean_real = (np.mean([abs(r[1]) for r in results['p1']]) +
             np.mean([abs(r[1]) for r in results['p4']])) / 2 if results['p1'] and results['p4'] else 0
mean_imag = (np.mean([abs(r[1]) for r in results['p2']]) +
             np.mean([abs(r[1]) for r in results['p3']])) / 2 if results['p2'] and results['p3'] else 0

# Wait - the rotation we used (e^{-i arg eps/2}) means the COSINE channel
# might pick up a MIX of Re and Im of chi. Let's also look at total magnitude
# |F| = sqrt(F_cos^2 + F_sin^2)
F_mag = np.sqrt(F_cos**2 + F_sin**2)
print(f"\n|F| amplitudes at log(p):")
print("p    p%5  chi    |F|")
for p in primes[:25]:
    if p == 5: continue
    lp = math.log(p)
    if lp > 5: break
    chi_p = chi_5_order4(p)
    idx = np.argmin(np.abs(omega - lp))
    print(f"{p:<4} {p%5:<5} {chi_p}    {F_mag[idx]:.4f}")

# Save
np.savez(f"{OUTDIR}/cyclotomic_data.npz",
         zeros=zeros, omega=omega, F_cos=F_cos, F_sin=F_sin, F_mag=F_mag)
print(f"\nData saved.")
