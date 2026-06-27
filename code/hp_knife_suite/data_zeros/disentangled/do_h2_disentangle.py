"""
Fixed-h varying-conductor: Q(sqrt(-35)) and Q(sqrt(-91)) both h=2.

Test if ratio stays ~3.1-4.0 across factor-6 conductor variation.

Q(sqrt(-35)): disc -35 (since -35 ≡ 1 mod 4), conductor 35, h=2
  Character: (-35|p) for prime p coprime to 35
    = (-1|p)(5|p)(7|p)
    Using reciprocity:
    = (p|5)(p|7) for odd p coprime to 35
    chi(2) = (-35|2) = -1 since -35 ≡ 5 mod 8
  
Q(sqrt(-91)): disc -91 (since -91 ≡ 1 mod 4), conductor 91, h=2
  Character: chi(p) = (p|7)(p|13) for odd p coprime to 91
  chi(2) = (-91|2) = -1 since -91 ≡ 5 mod 8
"""
import math, os, time
import numpy as np
from mpmath import mp, mpf, mpc, zeta as mp_zeta, gamma as mp_gamma, pi as mp_pi
from math import gcd
mp.dps = 15

def legendre(a, p):
    a = a % p
    if a == 0: return 0
    val = pow(a, (p-1)//2, p)
    return -1 if val == p-1 else val

def sieve(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2, n+1):
        if s[i]:
            for j in range(i*i, n+1, i): s[j]=False
    return [i for i in range(n+1) if s[i]]
small_primes = sieve(200)

def compute_field_zeros(disc_neg, conductor, h_K, chi_prime_fn, T_MAX=80.0, DT=0.08):
    """Compute zeros of L(s, chi_disc_neg) where conductor = |disc_neg|."""
    name = f"Q(sqrt({disc_neg}))"
    print(f"\n{'='*70}\n{name}: disc={disc_neg}, conductor={conductor}, h_K={h_K}\n{'='*70}")
    
    # Build character mod conductor
    chi_list = [0]*conductor
    for n in range(1, conductor):
        if gcd(n, conductor) > 1: continue
        m = n; val = 1
        for p in small_primes:
            if p > n: break
            while m % p == 0:
                cp = chi_prime_fn(p)
                if cp is None: val = None; break
                val *= cp; m //= p
            if val is None: break
        chi_list[n] = val if val is not None else 0
    
    # Verify oddness
    print(f"chi(-1) = chi({conductor-1}) = {chi_list[conductor-1]} (should be -1 for imaginary)")
    
    # Verify class number formula
    predicted_L1 = (2 * math.pi * h_K) / (2 * math.sqrt(abs(disc_neg)))
    print(f"L(1) predicted (h={h_K}): {predicted_L1:.6f}")
    
    def L_chi(s):
        total = mpc(0)
        for a in range(1, conductor):
            if chi_list[a] != 0:
                total += chi_list[a] * mp_zeta(s, mpf(a)/conductor)
        return mpf(conductor)**(-s) * total
    
    def Lambda_chi(t):
        s = mpc(0.5, t)
        return float(((mpf(conductor)/mp_pi)**(s/2) * mp_gamma((s+1)/2) * L_chi(s)).real)
    
    # Time check
    t0 = time.time()
    val = Lambda_chi(10.0)
    rate = 1/(time.time() - t0)
    print(f"Lambda(10) = {val:.5f}, rate {rate:.0f}/s")
    
    # Scan
    t_vals = np.arange(0.01, T_MAX, DT)
    print(f"Scanning {len(t_vals)} points...")
    
    t0 = time.time()
    Lambda_vals = np.zeros(len(t_vals))
    for i, t in enumerate(t_vals):
        if i % 200 == 0 and i > 0:
            e = time.time() - t0
            print(f"  {i}/{len(t_vals)}  rate={i/e:.0f}/s")
        Lambda_vals[i] = Lambda_chi(float(t))
    print(f"Done in {time.time()-t0:.1f}s")
    
    sign_changes = np.where(np.diff(np.sign(Lambda_vals)) != 0)[0]
    print(f"Sign changes: {len(sign_changes)}")
    
    def bisect(t_lo, t_hi):
        f_lo = Lambda_chi(t_lo); f_hi = Lambda_chi(t_hi)
        if f_lo * f_hi >= 0: return None
        for _ in range(40):
            t_mid = (t_lo + t_hi) / 2
            f_mid = Lambda_chi(t_mid)
            if abs(f_mid) < 1e-8 or (t_hi-t_lo) < 1e-8: return t_mid
            if f_lo * f_mid < 0: t_hi = t_mid; f_hi = f_mid
            else: t_lo = t_mid; f_lo = f_mid
        return (t_lo + t_hi) / 2
    
    zeros = []
    for idx in sign_changes:
        z = bisect(t_vals[idx], t_vals[idx+1])
        if z is not None: zeros.append(z)
    zeros = np.array(sorted(zeros))
    diffs = np.diff(zeros)
    zeros = zeros[np.concatenate([[True], diffs > 0.1])]
    print(f"Zeros: {len(zeros)}, range [{zeros[0]:.2f}, {zeros[-1]:.2f}]")
    return zeros, chi_list

# Q(sqrt(-35)): chi(2) = -1, chi(odd p coprime to 35) = (p|5)(p|7)
def chi_m35_prime(p):
    if p == 5 or p == 7: return None
    if p == 2: return -1  # -35 ≡ 5 mod 8
    return legendre(p, 5) * legendre(p, 7)

zeros_m35, chi35 = compute_field_zeros(-35, 35, 2, chi_m35_prime, T_MAX=80.0)

# Q(sqrt(-91)): chi(2) = -1, chi(odd p coprime to 91) = (p|7)(p|13)
def chi_m91_prime(p):
    if p == 7 or p == 13: return None
    if p == 2: return -1  # -91 ≡ 5 mod 8
    return legendre(p, 7) * legendre(p, 13)

zeros_m91, chi91 = compute_field_zeros(-91, 91, 2, chi_m91_prime, T_MAX=60.0)

os.makedirs("/home/claude/more_fields", exist_ok=True)
np.savetxt("/home/claude/more_fields/zeros_chi_-35.txt", zeros_m35, fmt='%.10f')
np.savetxt("/home/claude/more_fields/zeros_chi_-91.txt", zeros_m91, fmt='%.10f')
print(f"\nSaved both zero files.")
