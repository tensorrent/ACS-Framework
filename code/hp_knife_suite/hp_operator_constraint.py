# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

r"""
THE HILBERT-POLYA WALL, MADE QUANTITATIVE  --  the two constraints, and why they conflict.

We do NOT construct an operator (the problem is open). We state, as measured numbers, the two
properties any self-adjoint H with spectrum {gamma_k} must carry SIMULTANEOUSLY, and show they
pull toward opposite symmetry classes -- which is exactly why no natural candidate is known.

  CONSTRAINT A (from the arithmetic face): the periodic-orbit amplitudes are REAL.
    The complex prime witness W(p) = sum_k exp(i gamma_k log p) is real (cosine-only): its
    imaginary part vanishes relative to its real part. Real, gamma<->-gamma-even amplitudes are
    the hallmark of a TIME-REVERSAL-INVARIANT (orthogonal, beta=1) system.

  CONSTRAINT B (from the local-order face): the level repulsion is GUE (beta=2).
    The nearest-neighbour spacing distribution repels as P(s) ~ s^beta at small s. GUE gives
    beta=2 (count(<s) ~ s^3); GOE gives beta=1 (count(<s) ~ s^2). We fit beta from the zeros.

A beta=1 (real-symmetric / time-reversal-invariant) operator matches A but FAILS B; a generic
beta=2 operator matches B but has complex orbit amplitudes, failing A. The Riemann dynamics must
be time-reversal-BROKEN (beta=2) yet carry REAL orbit amplitudes -- the Berry-Keating tension.
That two-sided constraint is the wall. Measuring both pins it down; it constructs nothing and
proves nothing about RH. Negatives (here, the non-existence of a matching naive operator) first-class.
"""
import numpy as np

g = np.loadtxt(_d("riemann_zeros_100k.txt"))
N = len(g)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

print(f"THE HILBERT-POLYA WALL  --  N = {N} zeros")
print("=" * 72)

# ---------- CONSTRAINT A: real orbit amplitudes ----------
print("CONSTRAINT A -- periodic-orbit amplitudes are REAL (time-reversal-even)")
print(f"  {'p':>4} {'|Re W|':>12} {'|Im W|':>12} {'|Im|/|Re|':>11}")
im_re = []
for p in PRIMES[:8]:
    w = np.exp(1j * np.log(p) * g).sum()
    r = abs(w.real); im = abs(w.imag)
    im_re.append(im / r)
    print(f"  {p:>4} {r:>12.1f} {im:>12.1f} {im/r:>11.4f}")
print(f"  mean |Im|/|Re| over primes = {np.mean(im_re):.4f}   (0 => real amplitudes, T-even)")
realness = np.mean(im_re)

# ---------- CONSTRAINT B: GUE repulsion exponent beta ----------
# Unfold to unit mean spacing, then fit count(spacing < s) ~ s^{beta+1} at small s.
def Nsmooth(T):
    return (T/(2*np.pi))*np.log(T/(2*np.pi)) - T/(2*np.pi) + 7/8
w = Nsmooth(g)
s = np.diff(w)
s = s / s.mean()

print("\nCONSTRAINT B -- level repulsion exponent beta  (GUE=2, GOE=1, Poisson=0)")
# cumulative count of small spacings; slope of log C(s) vs log s is beta+1
svals = np.linspace(0.02, 0.30, 25)
counts = np.array([np.sum(s < sv) for sv in svals], dtype=float)
good = counts > 30
slope, intc = np.polyfit(np.log(svals[good]), np.log(counts[good]), 1)
beta = slope - 1.0
print(f"  small-spacing scaling  count(s'<s) ~ s^(beta+1):  slope = {slope:.3f}")
print(f"  => beta = {beta:.2f}   (GUE prediction 2.00; GOE 1.00)")
# corroborate with fraction of very small spacings vs GUE/GOE/Poisson expectation
frac_small = np.mean(s < 0.30)
print(f"  fraction of spacings < 0.30 = {frac_small:.4f}")
print(f"    GUE ~ {32/np.pi**2*0.30**3/3:.4f}   GOE ~ {np.pi/4*0.30**2:.4f}   Poisson ~ {1-np.exp(-0.30):.4f}")

# ---------- the wall ----------
print("\n" + "=" * 72)
print("THE WALL")
print(f"  A: orbit amplitudes real (|Im|/|Re| = {realness:.3f} ~ 0)  -> pulls to beta=1 (T-even)")
print(f"  B: measured repulsion beta = {beta:.2f} ~ 2               -> beta=2 (T-broken)")
print("""  A real-symmetric (beta=1) operator satisfies A and fails B; a generic complex-Hermitian
  (beta=2) operator satisfies B with complex amplitudes and fails A. The Riemann operator must
  be time-reversal-BROKEN yet carry REAL orbit amplitudes -- realised in physics only by special
  systems (e.g. a T-breaking with an antiunitary symmetry whose square is +1). No natural
  differential/dynamical operator with this exact signature is known; that gap is the open
  Hilbert-Polya problem, here stated as two measured numbers rather than a slogan.
  Constructs no operator; proves nothing about RH.""")
