#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Generate additional zeros of Dirichlet L(s,chi) on the critical line, non-circularly:
L(s,chi) = q^{-s} sum_{a=1..q} chi(a) * zeta(s, a/q)   (Hurwitz zeta; primes NEVER inserted),
matching the construction of the bundle's existing L-zero files.

Zero finder (no root number needed): at a simple zero t* on the line, L(1/2+it) ~ c*(t-t*),
so BOTH Re L and Im L change sign at t*. Bracket sign changes of Im L, refine, and accept
only where |L| collapses (a true common zero), rejecting points where Im L alone vanishes.

Writes t (imaginary parts) one per line, ascending. Seed-free (deterministic scan).
"""
import sys
from math import gcd
import mpmath as mp

mp.mp.dps = 20

def make_chi(q, gen, order):
    units = [a for a in range(1, q) if gcd(a, q) == 1]
    dlog = {}; val = 1
    for j in range(len(units)):
        dlog[val % q] = j; val = (val * gen) % q
    w = mp.e**(2j*mp.pi/order)
    def chi(a):
        a %= q
        if gcd(a, q) != 1:
            return mp.mpc(0)
        return w**dlog[a]
    return chi, units

def L_on_line(t, q, chi):
    s = mp.mpf(1)/2 + 1j*t
    tot = mp.mpc(0)
    for a in range(1, q+1):
        c = chi(a)
        if gcd(a, q) == 1:
            tot += c * mp.zeta(s, mp.mpf(a)/q)
    return q**(-s) * tot

def find_zeros(q, chi, t_max, step=mp.mpf('0.04'), tol=mp.mpf('1e-6')):
    zeros = []
    t = mp.mpf('0.5')
    Lprev = L_on_line(t, q, chi)
    while t < t_max:
        t2 = t + step
        L2 = L_on_line(t2, q, chi)
        if mp.im(Lprev) * mp.im(L2) < 0:            # Im L sign change -> bracket
            try:
                tz = mp.findroot(lambda x: mp.im(L_on_line(x, q, chi)), (t, t2), solver='anderson')
                if abs(L_on_line(tz, q, chi)) < tol and (not zeros or abs(tz - zeros[-1]) > 1e-3):
                    zeros.append(mp.mpf(tz))
            except Exception:
                pass
        t, Lprev = t2, L2
    return zeros

CASES = [
    ("cyclotomic_5/zeros_chi_5_order4_ext.txt", 5, 2, 4),
    ("cyclotomic_7/zeros_chi_7_order6_ext.txt", 7, 3, 6),
]

if __name__ == "__main__":
    t_max = mp.mpf(sys.argv[1]) if len(sys.argv) > 1 else mp.mpf('160')
    import os
    HERE = os.path.dirname(os.path.abspath(__file__))
    for fname, q, gen, order in CASES:
        chi, units = make_chi(q, gen, order)
        # validate: first zero should match the existing file to ~5 digits
        zs = find_zeros(q, chi, t_max)
        out = os.path.join(HERE, fname)
        with open(out, "w") as f:
            for z in zs:
                f.write(mp.nstr(z, 11) + "\n")
        print(f"{fname}: {len(zs)} zeros up to t={t_max}; first three: "
              f"{[mp.nstr(z,8) for z in zs[:3]]}")
