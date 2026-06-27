"""
Q(zeta_5) Dedekind structure test.

ζ_{Q(ζ_5)}(s) = ζ(s) · L(s, χ¹) · L(s, χ²) · L(s, χ³)
              = ζ(s) · L(s, χ¹) · L(s, chi_5_quad) · L(s, χ̄¹)

where χ is order-4 character mod 5.

For F_K analysis: combine zeros of all four L-functions.
For L(s, χ³) = L(s, χ̄¹): zeros are reflections of L(s, χ¹) zeros.
Specifically, if 1/2 + iγ is a zero of L(s, χ), then 1/2 - iγ is a zero of L(s, χ̄).
For computing F at omega > 0, we use cos(omega·γ) which is symmetric in γ → -γ.
So L(s, χ) and L(s, χ̄) contribute identically to F at positive omega.

Splitting pattern for primes p coprime to 5:
- p ≡ 1 mod 5: ord_p(5) = 1 (split completely into 4 prime ideals of norm p)
- p ≡ 4 mod 5: ord_p(5) = 2 (split into 2 prime ideals of norm p²)
- p ≡ 2, 3 mod 5: ord_p(5) = 4 (inert, single prime ideal of norm p⁴)
- p = 5: totally ramified
"""
import math, os
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

OUTDIR = "/home/claude/cyclotomic_5"

# Load all four L-function zero sets
zeta_zeros = np.loadtxt("/mnt/project/The_first_100_000_zeros_of_the_Riemann_zeta_function__accurate_to_within_3_10__-9_")
zeros_chi2 = np.loadtxt("/home/claude/Qsqrt5/zeros_chi5.txt")  # quadratic chi_5 character
zeros_chi1 = np.loadtxt(f"{OUTDIR}/zeros_chi_5_order4.txt")  # order-4 chi
# χ³ = χ̄¹ has zeros = reflections of χ¹ zeros under γ → -γ
# For our cos(omega·γ) Fourier transform, this is symmetric — so |F_chi3(omega)| = |F_chi1(omega)|
# But they're DIFFERENT sets of zeros. Use chi1_zeros doubled (same gamma but different identities).
# Actually for F(omega) = Σ cos(omega γ): if χ³ has zeros at -γ for each γ of χ¹, then
# Σ_{χ¹} cos(omega γ) = Σ_{χ³} cos(omega γ) since cos(-x) = cos(x). So contribute equally.

print(f"Loaded L-function zeros:")
print(f"  ζ(s):     up to {zeta_zeros[-1]:.0f} ({len(zeta_zeros)} zeros)")
print(f"  L(s, χ²): {len(zeros_chi2)} zeros (range {zeros_chi2[0]:.2f}-{zeros_chi2[-1]:.2f})")
print(f"  L(s, χ¹): {len(zeros_chi1)} zeros (range {zeros_chi1[0]:.2f}-{zeros_chi1[-1]:.2f})")
print(f"  L(s, χ³): same |gamma| as χ¹ (54 zeros)")

# Match T ranges
T_max_chi1 = zeros_chi1[-1]
T_max_chi2 = zeros_chi2[-1]
T_max = min(T_max_chi1, T_max_chi2, 100)
print(f"\nUsing T ≤ {T_max:.1f}")

zeta_sub = zeta_zeros[zeta_zeros < T_max]
chi2_sub = zeros_chi2[zeros_chi2 < T_max]
chi1_sub = zeros_chi1[zeros_chi1 < T_max]

print(f"\nFinal zero counts (T < {T_max}):")
print(f"  ζ:    {len(zeta_sub)}")
print(f"  χ²:   {len(chi2_sub)}")
print(f"  χ¹:   {len(chi1_sub)}")
print(f"  χ³:   {len(chi1_sub)} (same as χ¹)")

# Fourier transforms
omega = np.linspace(0.5, 5.0, 2000)
F_zeta = np.array([np.sum(np.cos(om*zeta_sub))/len(zeta_sub) for om in omega])
F_chi2 = np.array([np.sum(np.cos(om*chi2_sub))/len(chi2_sub) for om in omega])
F_chi1 = np.array([np.sum(np.cos(om*chi1_sub))/len(chi1_sub) for om in omega])

# Total F_K = sum of normalized F's
# Important: each F_L is normalized by its own N, but they should be weighted EQUALLY
# in the Dedekind decomposition (each L-function contributes equally to the explicit formula).
F_K = F_zeta + F_chi2 + F_chi1 + F_chi1  # F_chi3 = F_chi1 by symmetry

def sieve(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2, n+1):
        if s[i]:
            for j in range(i*i, n+1, i): s[j]=False
    return [i for i in range(n+1) if s[i]]
primes = sieve(1000)

# Classify primes by splitting type in Q(ζ_5)
def split_type(p):
    """Returns (f, g, type_name) for prime p in Q(ζ_5)."""
    if p == 5:
        return (1, 1, 'ramified', 1)  # totally ramified
    r = p % 5
    if r == 1:  # order 1 in (Z/5)*
        return (1, 4, 'split_4', 4)  # 4 primes of norm p
    if r == 4:  # order 2 (since 4² = 16 ≡ 1)
        return (2, 2, 'split_2', 2)  # 2 primes of norm p²
    # r = 2 or 3, order 4 (since 2 generates (Z/5)*, ord(2)=4; ord(3)=4 also)
    return (4, 1, 'inert', 1)

# Test F_K at all relevant prime powers
print("\n" + "="*80)
print("Q(ζ_5) DEDEKIND STRUCTURE TEST")
print("="*80)

amps_split4 = []   # p ≡ 1 mod 5, peak at log(p)
amps_split2 = []   # p ≡ 4 mod 5, peak at log(p²)
amps_inert = []    # p ≡ 2,3 mod 5, peak at log(p⁴)
amps_ramif = []    # p = 5

# For split_4: contribution at log(p) is 4× the basic Λ/√p
# For split_2: contribution at log(p²) but ALSO at log(p) from one of the L-functions
# For inert: contribution at log(p^4)
# For ramified: at log(5)

print("\n{:<6}{:<8}{:<14}{:<10}{:<12}".format("p", "p%5", "type", "f×g", "expected peak position"))
print("-"*80)
for p in primes[:25]:
    if p == 5:
        f, g, name, mult = split_type(p)
        lp = math.log(p)
        idx = np.argmin(np.abs(omega - lp))
        amp = abs(F_K[idx])
        amps_ramif.append((p, amp))
        print(f"{p:<6}{p%5:<8}{name:<14}{f}×{g}        log(p)={lp:.3f}, |F_K|={amp:.4f}")
        continue
    
    f, g, name, mult = split_type(p)
    lp = math.log(p)
    if lp > 5: break
    
    # Primary expected peak position depends on type
    if name == 'split_4':
        # Peak at log(p)
        idx = np.argmin(np.abs(omega - lp))
        amp = abs(F_K[idx])
        amps_split4.append((p, amp, lp))
        print(f"{p:<6}{p%5:<8}{name:<14}{f}×{g}        log(p)={lp:.3f}, |F_K|={amp:.4f}")
    elif name == 'split_2':
        # Peak at log(p²)
        lp2 = 2*lp
        if lp2 > 5:
            print(f"{p:<6}{p%5:<8}{name:<14}{f}×{g}        log(p²)={lp2:.3f} > 5, SKIP")
            continue
        idx = np.argmin(np.abs(omega - lp2))
        amp = abs(F_K[idx])
        amps_split2.append((p, amp, lp2))
        print(f"{p:<6}{p%5:<8}{name:<14}{f}×{g}        log(p²)={lp2:.3f}, |F_K|={amp:.4f}")
        # Also note amplitude at log(p) — should be SUPPRESSED for split_2 type
        idx_p = np.argmin(np.abs(omega - lp))
        amp_p = abs(F_K[idx_p])
        print(f"      {'':<8}{'(at log p)':<14}{'':<10}                   log(p)={lp:.3f}, |F_K|={amp_p:.4f}")
    else:  # inert
        # Peak at log(p^4)
        lp4 = 4*lp
        if lp4 > 5:
            # Just check log(p) which should be suppressed
            idx_p = np.argmin(np.abs(omega - lp))
            amp_p = abs(F_K[idx_p])
            amps_inert.append((p, amp_p, lp))
            print(f"{p:<6}{p%5:<8}{name:<14}{f}×{g}        log(p)={lp:.3f}, |F_K|={amp_p:.4f}  (log(p⁴)={lp4:.2f} > 5)")
        else:
            idx = np.argmin(np.abs(omega - lp4))
            amp = abs(F_K[idx])
            amps_inert.append((p, amp, lp4))
            print(f"{p:<6}{p%5:<8}{name:<14}{f}×{g}        log(p⁴)={lp4:.3f}, |F_K|={amp:.4f}")

# Summary
print("\n" + "="*60)
print("SUMMARY — amplitude by splitting class")
print("="*60)
if amps_split4:
    mean_s4 = np.mean([a for _,a,_ in amps_split4])
    print(f"split_4 (p≡1 mod 5, at log p):  mean |F_K| = {mean_s4:.4f}  (n={len(amps_split4)})")
if amps_split2:
    mean_s2 = np.mean([a for _,a,_ in amps_split2])
    print(f"split_2 (p≡4 mod 5, at log p²): mean |F_K| = {mean_s2:.4f}  (n={len(amps_split2)})")
if amps_inert:
    mean_in = np.mean([a for _,a,_ in amps_inert])
    print(f"inert   (p≡2,3 mod 5):           mean |F_K| = {mean_in:.4f}  (n={len(amps_inert)})")
if amps_ramif:
    mean_r = np.mean([a for _,a in amps_ramif])
    print(f"ramified (p=5):                  mean |F_K| = {mean_r:.4f}")

# The structural prediction: split_4 should DOMINATE because 4 prime ideals all contribute at log(p)
# split_2 should peak at log(p²) but be suppressed at log(p)
# inert should peak at log(p⁴) which is outside our range for most p

# Compare to quadratic field Q(√5) at log(p) for the same primes
# In Q(√5): p ≡ 1, 4 mod 5 splits, p ≡ 2, 3 inert
# In Q(ζ_5): p ≡ 1 fully splits (×4), p ≡ 4 splits in pairs (×2), p ≡ 2,3 inert
# So p ≡ 1 should have STRONGER peak in Q(ζ_5) than Q(√5)
# p ≡ 4 should have WEAKER peak at log(p) in Q(ζ_5) (the "peak" is at log(p²) not log(p))

print("\n" + "="*60)
print("STRUCTURAL CHECK — does the framework discriminate the 4 classes?")
print("="*60)

# Check: at log(p), which primes peak the most?
print("\n|F_K| at log(p) for p ≡ 1 mod 5 (split_4, should be HIGH):")
for p, amp, lp in sorted(amps_split4, key=lambda x: x[0])[:5]:
    print(f"  p={p:3d}  |F_K|={amp:.4f}")

print("\n|F_K| at log(p) for p ≡ 4 mod 5 (split_2, should be MODERATE — half of split_4):")
# Recompute at log(p) not log(p²)
for p in primes[:30]:
    if p == 5: continue
    if p % 5 == 4:
        lp = math.log(p)
        if lp > 5: break
        idx = np.argmin(np.abs(omega - lp))
        print(f"  p={p:3d}  |F_K|={abs(F_K[idx]):.4f}")

print("\n|F_K| at log(p) for p ≡ 2,3 mod 5 (inert, should be LOW):")
for p in primes[:30]:
    if p == 5: continue
    if p % 5 in [2, 3]:
        lp = math.log(p)
        if lp > 5: break
        idx = np.argmin(np.abs(omega - lp))
        print(f"  p={p:3d}  |F_K|={abs(F_K[idx]):.4f}")

# Save
np.savez(f"{OUTDIR}/Qzeta5_data.npz",
         zeros_chi1=zeros_chi1, zeros_chi2=zeros_chi2,
         omega=omega, F_K=F_K, F_zeta=F_zeta, F_chi1=F_chi1, F_chi2=F_chi2)
print(f"\nData saved to {OUTDIR}/Qzeta5_data.npz")
