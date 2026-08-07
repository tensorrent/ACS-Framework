#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
CONJECTURE: "THE HYPERCONE POKING THROUGH THE SLICE"
====================================================
Picture under test: the 15-dim sl(4) cloud is the object; 3-dim experience
is a slice; a higher-dimensional cone intersecting the slice is seen as
evolving spheroids. The Hilbert-Polya operator is experienced in projection.

Precise kill-able sub-claims (stated BEFORE computing, read as it lies):

  C1 (exact): In the fermion 4-rep of the sl(4) cloud, a 2-parameter REAL
     slice through the torsion/diagonal directions has eigenvalue sheets
     forming an EXACT double cone at degeneracy; every 1-parameter
     sub-slice sees hyperbolae (avoided crossings) — the cone poking
     through, never the apex. Degeneracy codimension = 2, so repulsion
     exponent beta = codim - 1 = 1 (GOE class).

  C2 (exact): Adding the chirality direction (the i introduced by the
     framework's J-map, sl(3) -> su(3)) raises the degeneracy codimension
     to 3: an exact 3-parameter cone. Repulsion exponent beta = 2 (GUE
     class). The exponent COUNTS the cone's hidden dimensions.

  C3 (measured, T3): The actual Riemann zeros (100k, in-repo) have
     small-spacing repulsion exponent beta ~ 2, NOT 1, NOT 0. If so, the
     shadow is the projection of a codimension-3 conical structure —
     the hidden operator lives in the complex (chirality) class, and the
     slice picture acquires a measured dimension count.

C1/C2 exact over Q (sympy). C3 is a measurement on data; reported as fit.
"""
from sympy import Matrix, Rational, symbols, sqrt, simplify, zeros, factor, I as sI
import numpy as np
import os

print("=" * 72)
print("HYPERCONE-THROUGH-THE-SLICE — EXACT STRUCTURE + MEASURED SHADOW")
print("=" * 72)

x, y, z = symbols("x y z", real=True)


def E(i, j):
    m = zeros(4)
    m[i, j] = 1
    return m


# --- C1: real 2-parameter slice — exact double cone --------------------------
# Slice directions (in-framework): S03 = E03 + E30 (torsion generator, V+/V-
# ladder) and D = diag(1,0,0,-1) (Cartan direction separating lepton/quark_r).
S03 = E(0, 3) + E(3, 0)
D = Matrix.diag(1, 0, 0, -1)
H2 = x * D + y * S03
lam = symbols("lam")
cp = factor(H2.charpoly(lam).as_expr())
print("\n[C1] Real slice H(x,y) = x*D + y*S03 in the fermion 4-rep")
print(f"     char poly: {cp}")
eigs2 = H2.eigenvals()
print(f"     eigenvalues: {sorted([simplify(e) for e in eigs2], key=str)}")
# The active 2x2 block (lepton, q_r) has eigenvalues +-sqrt(x^2+y^2): a cone.
gap2 = simplify(2 * sqrt(x**2 + y**2))
cone_exact = all(simplify(e**2 - (x**2 + y**2)) == 0 for e in eigs2 if simplify(e) != 0)
print(f"     nonzero sheets are +-sqrt(x^2 + y^2) exactly (double cone): {cone_exact}")
print("     1-param sub-slice x = t, y = g (fixed): gap = 2*sqrt(t^2+g^2) —")
print("     a hyperbola: the cone seen from inside the slice, apex off-slice.")
print("     Degeneracy needs x = 0 AND y = 0: codimension 2 -> beta = 1 (GOE).")
c1 = cone_exact

# --- C2: add the chirality (imaginary) direction — codim 3 cone --------------
# The J-map (Prop 9.7) introduces i: the third direction is the antisymmetric
# A03 with imaginary coefficient — Hermitian, not real-symmetric.
A03 = E(0, 3) - E(3, 0)
H3 = x * D + y * S03 + z * (sI * A03)
herm = simplify(H3 - H3.conjugate().T) == zeros(4)
eigs3 = H3.eigenvals()
cone3_exact = all(simplify(e**2 - (x**2 + y**2 + z**2)) == 0
                  for e in eigs3 if simplify(e) != 0)
print("\n[C2] Hermitian slice H(x,y,z) = x*D + y*S03 + z*(i*A03)")
print(f"     Hermitian: {herm}")
print(f"     nonzero sheets are +-sqrt(x^2 + y^2 + z^2) exactly: {cone3_exact}")
print("     Degeneracy needs x = y = z = 0: codimension 3 -> beta = 2 (GUE).")
print("     The chirality i is exactly what buys the third cone dimension.")
c2 = herm and cone3_exact

# --- C3: measure the exponent in the shadow (Riemann zeros) ------------------
print("\n[C3] Measured small-spacing repulsion of the Riemann zeros")
zeros_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "..", "hp_knife_suite", "data_zeros",
                          "riemann_zeros_100k.txt")
t = np.array([float(v) for v in open(zeros_path).read().split()])
t = np.sort(t[t > 0])
print(f"     zeros loaded: {len(t)}")
# Unfold: local mean density rho(T) = log(T/(2*pi)) / (2*pi)
rho = np.log(t[:-1] / (2 * np.pi)) / (2 * np.pi)
s = np.diff(t) * rho
s = s[(s > 0) & np.isfinite(s)]
print(f"     unfolded spacings: n = {len(s)}, mean = {s.mean():.4f} (want ~1)")
# Fit P(s) ~ s^beta on the small-s tail via log-log histogram slope
bins = np.linspace(0.02, 0.5, 25)
hist, edges = np.histogram(s, bins=bins, density=True)
mid = (edges[:-1] + edges[1:]) / 2
mask = hist > 0
beta_fit, _ = np.polyfit(np.log(mid[mask]), np.log(hist[mask]), 1)
print(f"     fitted repulsion exponent beta = {beta_fit:.3f}")
print("     reference: Poisson beta=0 | GOE beta=1 | GUE beta=2")
c3 = abs(beta_fit - 2) < 0.35 and abs(beta_fit - 1) > 0.5
print(f"     consistent with GUE (beta~2), inconsistent with GOE/Poisson: {c3}")

# --- VERDICT -----------------------------------------------------------------
print("\n" + "=" * 72)
print("VERDICT — read as it lies")
print("=" * 72)
for tag, ok, txt in [
    ("C1", c1, "real slice: exact double cone, slices see hyperbolae (codim 2)"),
    ("C2", c2, "chirality direction raises the cone to codim 3 (beta = 2 class)"),
    ("C3", c3, "zeros' measured beta ~ 2: shadow of a codim-3 conical structure"),
]:
    print(f"  {tag}: {'SURVIVES' if ok else 'FALSIFIED'} — {txt}")

if all([c1, c2, c3]):
    print("""
ALL THREE SURVIVE (C1/C2 exact T1; C3 measured T3).

What this DOES establish: the repulsion exponent is a dimension counter.
Level crossings of Hermitian families are conical structures whose apex
lives in more parameters than any 1-dim slice can reach; the slice sees
only hyperbolic near-misses ("spheroids that never quite touch"). The
measured beta ~ 2 of the Riemann zeros says the hidden Hilbert-Polya
object's degeneracy cone is codimension-3 — the complex/chirality class,
the same i the framework's J-map introduces. In that precise sense the
shadow carries a countable imprint of dimensions the slice cannot see.

What this does NOT establish: that physical 3-space is a slice of the
15-dim cloud; that zeros ARE such an operator's spectrum (open problem
#2 stands); anything about spacetime, matter, or 'tearing through'.
The cone is in parameter space, not in physical space. Names correspond
structurally; the physics identification remains at the conjecture layer.""")
else:
    print("\nAt least one sub-claim falsified — record mechanism above (T4).")
