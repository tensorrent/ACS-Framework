#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
CONJECTURE: "QUANTUM CONDENSATE = COLLAPSED FORM (THE SLAG OF THE FURNACE)"
===========================================================================
Clarified form (stated BEFORE computing, read as it lies afterward):

  The uncollapsed, non-condensed substrate is fundamental; matter (the
  quantum condensate) is the COLLAPSED, terminal output of the torsion
  flow — the slag, not the base. This is an IMAGE/omega-limit claim, the
  dual of the (already killed, F-6) kernel/annihilator claim.

Precise kill-able sub-claims, in the sl(4,R) Palatini structure and the
fermion fundamental 4 (conventions: fermion_reps_full.py, torsion flow:
phase55_holonomy_corrected.py / torsion_condensation_holonomy.py):

  C1 (universal collapse): under exp(t ad_{T_BL}), every direction outside
     an exact, identifiable exceptional set collapses projectively onto
     the dominant eigenspace V+ (lambda = +4/3). The terminal form is
     universal; the exceptional set is precisely the invariant sector.
  C2 (slag is terminal): V+ is abelian and nilpotent of order 2 — the
     collapsed operators square to zero and cannot regenerate structure.
  C3 (slag is matter-shaped): in the fermion 4, V+ consists EXACTLY of
     the lepton -> quark transition operators, and the collapse rate
     +4/3 EQUALS the B-L charge transferred per transition
     (Delta(B-L) = 1/3 - (-1) = 4/3).
  C4 (uncollapsed sector is the gauge furnace): the flow-invariant
     (non-collapsing) sector is exactly sl(3) + u(1)_{B-L} — the colour
     and B-L gauge structure keeps burning; it is never part of the slag.

All arithmetic exact over Q (sympy Rational). No floats in any decision.
"""
from sympy import Matrix, Rational, zeros

print("=" * 72)
print("CONDENSATE-AS-COLLAPSE (SLAG OF THE FURNACE) — EXACT COMPUTATION")
print("=" * 72)


def E(i, j):
    m = zeros(4)
    m[i, j] = 1
    return m


def bracket(X, Y):
    return X * Y - Y * X


def vec(M):
    return Matrix([M[i, j] for i in range(4) for j in range(4)])


# --- sl(4) basis and the torsion vacuum direction ---------------------------
sl4_basis = []
for i in range(4):
    for j in range(4):
        if i != j:
            sl4_basis.append(E(i, j))
for k in range(3):
    d = zeros(4)
    d[k, k], d[k + 1, k + 1] = 1, -1
    sl4_basis.append(d)
B_span = Matrix.hstack(*[vec(B) for B in sl4_basis])
assert B_span.rank() == 15

T_BL = Matrix.diag(Rational(1, 3), Rational(1, 3), Rational(1, 3), -1)

# --- C1: exact eigenspace decomposition of ad_{T_BL} on sl(4) ----------------
# ad matrix in sl4 coordinates
ad = zeros(15, 15)
cols = []
for B in sl4_basis:
    cols.append(B_span.solve(vec(bracket(T_BL, B))))
ad = Matrix.hstack(*cols)
eig = ad.eigenvals()
print("\n[C1] Exact spectrum of ad_{T_BL} on sl(4):")
for lam, mult in sorted(eig.items(), key=lambda kv: kv[0]):
    print(f"     lambda = {lam}   (multiplicity {mult})")

spec_ok = (eig.get(Rational(4, 3)) == 3 and eig.get(Rational(-4, 3)) == 3
           and eig.get(0) == 9)

# Dominant eigenspace V+ and invariant sector V0, exact bases
Vplus = (ad - Rational(4, 3) * Matrix.eye(15)).nullspace()
Vzero = ad.nullspace()
Vminus = (ad + Rational(4, 3) * Matrix.eye(15)).nullspace()
print(f"     dim V+ = {len(Vplus)},  dim V0 = {len(Vzero)},  dim V- = {len(Vminus)}")

# Universal collapse statement: for X = X0 + X+ + X- (exact, unique split),
# exp(t ad) X = X0 + e^{4t/3} X+ + e^{-4t/3} X-. Projectively, any X with
# X+ != 0 collapses onto V+. Exceptional set = {X : X+ = 0} = V0 + V-,
# an exact 12-dim proper subspace (measure zero). This is a THEOREM of the
# decomposition once the spectrum is verified real and semisimple:
semisimple = (len(Vplus) + len(Vzero) + len(Vminus) == 15)
print(f"     ad_(T_BL) semisimple over Q (eigenbasis spans sl4): {semisimple}")
c1 = spec_ok and semisimple
print(f"     C1 (universal collapse onto V+, exceptional set = V0+V-, 12-dim): {c1}")

# --- C2: the slag is abelian, nilpotent of order 2 ---------------------------
Vplus_mats = [Matrix(4, 4, list(B_span * v)) for v in Vplus]
abelian = all(bracket(A, B).is_zero_matrix for A in Vplus_mats for B in Vplus_mats)
nilpotent2 = all((A * B).is_zero_matrix for A in Vplus_mats for B in Vplus_mats)
print("\n[C2] Structure of the collapsed sector V+:")
print(f"     abelian ([V+,V+]=0): {abelian}")
print(f"     nilpotent order 2 (A*B = 0 for all A,B in V+): {nilpotent2}")
c2 = abelian and nilpotent2

# --- C3: the slag is matter-shaped in the fermion 4 --------------------------
# Fundamental 4 = 3_{1/3} (quarks r,g,b) + 1_{-1} (lepton), fermion_reps_full.
print("\n[C3] Action of V+ on the fermion fundamental 4:")
e = [Matrix([1 if k == i else 0 for k in range(4)]) for i in range(4)]
labels = ["q_r", "q_g", "q_b", "lep"]
lep_to_quark_only = True
for A in Vplus_mats:
    for i in range(4):
        img = A * e[i]
        if not all(x == 0 for x in img):
            src = labels[i]
            tgt = [labels[k] for k in range(4) if img[k] != 0]
            print(f"     {src} -> {tgt}   (operator maps {src} into {'/'.join(tgt)})")
            if src != "lep" or any(t == "lep" for t in tgt):
                lep_to_quark_only = False
# B-L charge transfer per transition = (B-L)_quark - (B-L)_lepton
dBL = Rational(1, 3) - (-1)
rate_matches_charge = (dBL == Rational(4, 3))
print(f"     V+ maps ONLY lepton -> quark: {lep_to_quark_only}")
print(f"     collapse rate +4/3 == Delta(B-L) = 1/3 - (-1) = {dBL}: {rate_matches_charge}")
c3 = lep_to_quark_only and rate_matches_charge

# --- C4: the uncollapsed sector is exactly sl(3) + u(1)_{B-L} ----------------
print("\n[C4] The flow-invariant (uncollapsed) sector V0:")
# sl(3)+u(1) basis: upper-left traceless 3x3 block generators + T_BL
sl3_u1 = []
for i in range(3):
    for j in range(3):
        if i != j:
            sl3_u1.append(E(i, j))
d1 = zeros(4); d1[0, 0], d1[1, 1] = 1, -1
d2 = zeros(4); d2[1, 1], d2[2, 2] = 1, -1
sl3_u1 += [d1, d2, T_BL]
gauge_span = Matrix.hstack(*[vec(M) for M in sl3_u1])
V0_span = Matrix.hstack(*[B_span * v for v in Vzero])
joint = Matrix.hstack(gauge_span, V0_span)
same = (gauge_span.rank() == 9 and V0_span.rank() == 9 and joint.rank() == 9)
print(f"     dim(sl3+u1) = {gauge_span.rank()}, dim V0 = {V0_span.rank()}, "
      f"dim(sum) = {joint.rank()}")
print(f"     V0 == sl(3) + u(1)_(B-L) exactly: {same}")
c4 = same

# --- VERDICT -----------------------------------------------------------------
print("\n" + "=" * 72)
print("VERDICT — read as it lies")
print("=" * 72)
for tag, ok, txt in [
    ("C1", c1, "universal projective collapse onto V+ (exceptional set exact)"),
    ("C2", c2, "collapsed sector abelian + nilpotent^2 (terminal slag)"),
    ("C3", c3, "slag = lepton->quark transitions; rate 4/3 = Delta(B-L)"),
    ("C4", c4, "uncollapsed sector = sl(3)+u(1) gauge furnace"),
]:
    print(f"  {tag}: {'SURVIVES' if ok else 'FALSIFIED'} — {txt}")

if all([c1, c2, c3, c4]):
    print("""
ALL FOUR SUB-CLAIMS SURVIVE (T1 machine-verified, exact arithmetic).

Scope boundary (what this DOES and DOES NOT establish):
  DOES: in the sl(4,R) Palatini structure, the torsion flow generated by
  the B-L vacuum direction sorts the algebra into an invariant gauge
  sector (sl(3)+u(1), never collapses) and a collapsing pair; every
  generic direction lands projectively on a 3-dim terminal sector that
  is nilpotent (order 2), and that terminal sector consists exactly of
  the lepton->quark transition operators, with collapse rate equal to
  the B-L charge transferred (4/3). The 'slag' is matter-shaped, and
  the 'furnace' is the gauge structure. This is consistent with — and
  gives exact content to — the condensate-as-collapsed-form picture.
  DOES NOT: establish any statement about physical spacetime, quantum
  measurement, wavefunction collapse, or cosmology. 'Collapse' here is
  projective alignment of a linear hyperbolic flow, not decoherence.
  The correspondence of names is structural, not demonstrated physics.""")
else:
    print("\nAt least one sub-claim falsified — record mechanism above (T4).")
