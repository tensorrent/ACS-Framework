"""Q(sqrt(-26)) second h=6 test. disc=-104, conductor=104."""
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

def chi_m104_prime(p):
    if p == 2 or p == 13: return None
    neg1 = -1 if p % 4 == 3 else 1
    two = 1 if p % 8 in [1, 7] else -1
    thirteen = legendre(p, 13)
    return neg1 * two * thirteen

def sieve(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2, n+1):
        if s[i]:
            for j in range(i*i, n+1, i): s[j]=False
    return [i for i in range(n+1) if s[i]]
small_primes = sieve(200)

chi_list = [0]*104
for n in range(1, 104):
    if gcd(n, 104) > 1: continue
    m = n; val = 1
    for p in small_primes:
        if p > n: break
        while m % p == 0:
            cp = chi_m104_prime(p)
            if cp is None: val = None; break
            val *= cp; m //= p
        if val is None: break
    chi_list[n] = val if val is not None else 0

print(f"chi(-1) = chi(103) = {chi_list[103]} (should be -1)", flush=True)
predicted_L1 = (2 * math.pi * 6) / (2 * math.sqrt(104))
print(f"L(1) predicted (h=6): {predicted_L1:.6f}", flush=True)

def L_chi(s):
    total = mpc(0)
    for a in range(1, 104):
        if chi_list[a] != 0:
            total += chi_list[a] * mp_zeta(s, mpf(a)/104)
    return mpf(104)**(-s) * total

def Lambda_chi(t):
    s = mpc(0.5, t)
    return float(((mpf(104)/mp_pi)**(s/2) * mp_gamma((s+1)/2) * L_chi(s)).real)

t0 = time.time()
val = Lambda_chi(10.0)
elapsed = time.time() - t0
print(f"Lambda(10) = {val:.5f} in {elapsed:.2f}s", flush=True)

T_MAX = 70.0
DT = 0.08
t_vals = np.arange(0.01, T_MAX, DT)
print(f"Scanning {len(t_vals)} points...", flush=True)

t0 = time.time()
Lambda_vals = np.zeros(len(t_vals))
for i, t in enumerate(t_vals):
    if i % 100 == 0 and i > 0:
        e = time.time() - t0
        print(f"  {i}/{len(t_vals)}  rate={i/e:.1f}/s", flush=True)
    Lambda_vals[i] = Lambda_chi(float(t))
print(f"Done in {time.time()-t0:.1f}s", flush=True)

sign_changes = np.where(np.diff(np.sign(Lambda_vals)) != 0)[0]
print(f"Sign changes: {len(sign_changes)}", flush=True)

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
print(f"Zeros: {len(zeros)}, range [{zeros[0]:.2f}, {zeros[-1]:.2f}]", flush=True)
np.savetxt("/home/claude/more_fields/zeros_chi_-104.txt", zeros, fmt='%.10f')
