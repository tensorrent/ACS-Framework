"""Q(zeta_5) cyclotomic test - corrected."""
import math, os, time
import numpy as np
from mpmath import mp, mpf, mpc, zeta as mp_zeta, gamma as mp_gamma, pi as mp_pi, exp as mp_exp
mp.dps = 20

OUTDIR = "/home/claude/cyclotomic"
os.makedirs(OUTDIR, exist_ok=True)

# Order-4 character mod 5
chi_vals = [mpc(0), mpc(1), mpc(0, 1), mpc(0, -1), mpc(-1)]

def gauss_sum():
    total = mpc(0)
    for a in range(1, 5):
        total += chi_vals[a] * mp_exp(2 * mp_pi * mpc(0, 1) * a / 5)
    return total

tau = gauss_sum()
epsilon = tau / (mpc(0, 1) * mpf(5)**mpf('0.5'))
arg_eps = math.atan2(float(epsilon.imag), float(epsilon.real))
print(f"arg(eps) = {arg_eps:.5f} rad ({math.degrees(arg_eps):.2f}°)")

# Use Hurwitz zeta for L(s, chi) — works for Re(s) >= 1/2 except at s=1
def L_chi(s):
    total = mpc(0)
    for a in range(1, 5):
        if abs(chi_vals[a]) > 1e-10:
            total += chi_vals[a] * mp_zeta(s, mpf(a)/5)
    return mpf(5)**(-s) * total

# Lambda function
def Lambda_chi_complex(t):
    s = mpc(0.5, t)
    factor1 = (mpf(5) / mp_pi) ** (s/2)
    factor2 = mp_gamma((s + 1) / 2)
    return factor1 * factor2 * L_chi(s)

# Z function — should be real
phase_factor = mp_exp(mpc(0, -arg_eps/2))
def Z(t):
    lam = Lambda_chi_complex(t)
    rotated = phase_factor * lam
    return float(rotated.real)

# Verify Z is real
print("\nVerify Z(t) is real:")
for t_test in [0.5, 1.0, 5.0, 10.0, 20.0, 50.0]:
    lam = Lambda_chi_complex(t_test)
    rotated = phase_factor * lam
    re = float(rotated.real)
    im = float(rotated.imag)
    print(f"  t={t_test:5.1f}: Z = {re:+.5f}, imag = {im:+.2e}")

# Time
t0 = time.time()
val = Z(10.0)
elapsed = time.time() - t0
print(f"\nOne Z eval: {elapsed:.3f}s, rate {1/elapsed:.0f}/s")

# Scan
T_MAX = 100.0
DT = 0.1
t_vals = np.arange(0.01, T_MAX, DT)
print(f"Scanning {len(t_vals)} points for Z(t) zeros...")

Z_vals = np.zeros(len(t_vals))
t0 = time.time()
for i, t in enumerate(t_vals):
    if i % 200 == 0 and i > 0:
        e = time.time() - t0
        print(f"  {i}/{len(t_vals)}  rate={i/e:.0f}/s")
    Z_vals[i] = Z(float(t))
print(f"Done in {time.time()-t0:.1f}s")

sign_changes = np.where(np.diff(np.sign(Z_vals)) != 0)[0]
print(f"Sign changes: {len(sign_changes)}")

def bisect(t_lo, t_hi):
    f_lo = Z(t_lo); f_hi = Z(t_hi)
    if f_lo * f_hi >= 0: return None
    for _ in range(40):
        t_mid = (t_lo + t_hi) / 2
        f_mid = Z(t_mid)
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
print(f"\nZeros found: {len(zeros)}, range [{zeros[0]:.2f}, {zeros[-1]:.2f}]")
print(f"First 15: {zeros[:15]}")

# Density check for complex L: same as Dirichlet — N(T) ≈ (T/2π) log(qT/(2πe))
T_test = zeros[-1]
predicted = (T_test/(2*math.pi)) * math.log(5*T_test/(2*math.pi)) - T_test/(2*math.pi)
print(f"Predicted zero count at T={T_test:.1f}: {predicted:.1f}, observed: {len(zeros)}")

np.savetxt(f"{OUTDIR}/zeros_chi_5_order4.txt", zeros, fmt='%.10f')
