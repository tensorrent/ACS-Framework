#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
CONJECTURE: "ELECTROMAGNETISM IS THE FUNDAMENTAL DEGRADATION"
=============================================================
Precise form under test (Adversarial Compression Cycle — stated BEFORE
computing, read as it lies afterward):

  STRONG FORM: The electromagnetic direction
      Q = J3 + K3 + (1/2) T_BL          (= T3L + T3R + (B-L)/2)
  is the UNIQUE direction in sl(4,R) annihilated by the full 9-dim
  Palatini torsion sector  T = [Sym0(4), o(4)].
  ("EM is the terminal torsion-null residue of the gauge structure.")

  WEAK FORM: Q is the unique gauge direction annihilated by the B-L
  vacuum direction T_BL alone (the direction behind the locked 0:1:4
  coupling ratio in torsion_hierarchy.py).

All arithmetic exact over Q (sympy Rational). No floats in any decision.
Provenance: torsion sector construction follows su3_torsion_intersection.py;
generator conventions follow torsion_hierarchy.py.
"""
from sympy import Matrix, Rational, zeros, eye

print("=" * 72)
print("EM-AS-TORSION-ANNIHILATOR — EXACT COMPUTATION")
print("=" * 72)


def E(i, j):
    m = zeros(4)
    m[i, j] = 1
    return m


def bracket(X, Y):
    return X * Y - Y * X


def vec(M):
    return Matrix([M[i, j] for i in range(4) for j in range(4)])


# --- sl(4) basis (15-dim) ----------------------------------------------------
sl4_basis = []
for i in range(4):
    for j in range(4):
        if i != j:
            sl4_basis.append(E(i, j))
for k in range(3):
    d = zeros(4)
    d[k, k], d[k + 1, k + 1] = 1, -1
    sl4_basis.append(d)
assert Matrix.hstack(*[vec(B) for B in sl4_basis]).rank() == 15

# --- Torsion sector T = [Sym0(4), o(4)] --------------------------------------
sym_basis = [E(i, j) + E(j, i) for i in range(4) for j in range(i + 1, 4)]
for k in range(3):
    d = zeros(4)
    d[k, k], d[k + 1, k + 1] = 1, -1
    sym_basis.append(d)
o4_basis = [E(i, j) - E(j, i) for i in range(4) for j in range(i + 1, 4)]

torsion_vecs = []
for S in sym_basis:
    for A in o4_basis:
        C = bracket(S, A)
        if any(x != 0 for x in C):
            torsion_vecs.append(vec(C))
T_span = Matrix.hstack(*torsion_vecs)
dim_T = T_span.rank()
print(f"\n[1] Torsion sector T = [Sym0(4), o(4)] : dim = {dim_T}")

# Identify T with Sym0(4) (both should be 9-dim, T subset Sym0)
sym0_span = Matrix.hstack(*[vec(S) for S in sym_basis])
joint = Matrix.hstack(T_span, sym0_span)
print(f"    dim(Sym0(4)) = {sym0_span.rank()},  dim(T + Sym0) = {joint.rank()}")
T_equals_sym0 = (dim_T == 9 and joint.rank() == 9)
print(f"    T == Sym0(4) exactly : {T_equals_sym0}")

# Orthogonal-ish basis for T: use sym_basis if T == Sym0 (exact, convenient)
T_basis = sym_basis if T_equals_sym0 else None
assert T_basis is not None, "unexpected torsion sector; conjecture test invalid"

# --- The electromagnetic direction ------------------------------------------
J3 = (E(0, 3) - E(3, 0) + E(1, 2) - E(2, 1)) / 2      # self-dual
K3 = (E(0, 3) - E(3, 0) - E(1, 2) + E(2, 1)) / 2      # anti-self-dual
T_BL = Matrix.diag(Rational(1, 3), Rational(1, 3), Rational(1, 3), -1)
Q = J3 + K3 + T_BL / 2
print("\n[2] EM direction Q = J3 + K3 + T_BL/2 (T3L + T3R + (B-L)/2)")
print(f"    Q traceless: {Q.trace() == 0}")

# --- STRONG FORM: centralizer of the full torsion sector ---------------------
# Solve [X, T_a] = 0 for all a, X in sl(4): nullspace of stacked ad-maps.
rows = []
for Ta in T_basis:
    rows.append(Matrix.hstack(*[vec(bracket(B, Ta)) for B in sl4_basis]))
big = Matrix.vstack(*rows)
null = big.nullspace()
dim_centralizer = len(null)
print("\n[3] STRONG FORM — centralizer of full torsion sector in sl(4)")
print(f"    dim {{X in sl(4) : [X,T]=0 for ALL T in torsion sector}} = {dim_centralizer}")

# --- Exact spectrum of the coupling operator on sl(4) ------------------------
# C = sum_a ad_{T_a}^dagger ad_{T_a} w.r.t. the Frobenius metric, torsion basis
# orthonormalized exactly. Eigenvalues grade sl(4) by torsion activity.
on_T = []
for S in sym_basis:
    v = vec(S)
    for u in on_T:
        v = v - (u.dot(v)) * u
    n2 = v.dot(v)
    on_T.append(v / n2**Rational(1, 2))
on_T_mats = [Matrix(4, 4, list(v)) for v in on_T]

on_sl4 = []
for B in sl4_basis:
    v = vec(B)
    for u in on_sl4:
        v = v - (u.dot(v)) * u
    n2 = v.dot(v)
    on_sl4.append(v / n2**Rational(1, 2))
on_sl4_mats = [Matrix(4, 4, list(v)) for v in on_sl4]

# --- Total torsion coupling C(X) = sum_a ||[T_a, X]||^2 ----------------------
# T_a run over an exactly ORTHONORMALIZED (Frobenius) basis of the torsion
# sector, so C is the canonical Casimir-type form; exact rationals throughout.
def total_coupling(X):
    tot = Rational(0)
    for Ta in on_T_mats:
        C = bracket(Ta, X)
        tot += sum(x * x for x in C)
    return tot

named = {
    "Q (photon)": Q,
    "J3 (SU2_L)": J3,
    "K3 (SU2_R)": K3,
    "T_BL (B-L)": T_BL,
    "H1 (colour)": Matrix.diag(1, -1, 0, 0),
    "A01 (colour, antisym)": E(0, 1) - E(1, 0),
    "A03 (col-lep)": E(0, 3) - E(3, 0),
    "S12 (torsion)": E(1, 2) + E(2, 1),
}
print("\n[4] Total torsion coupling C(X) = sum_a ||[T_a,X]||^2 (exact)")
for name, X in named.items():
    k2 = sum(x * x for x in X)          # normalise per unit norm^2
    print(f"    C({name:<22}) = {total_coupling(X)}   (per ||X||^2={k2}: {total_coupling(X)/k2})")

Cop = zeros(15)
for i, Bi in enumerate(on_sl4_mats):
    for j, Bj in enumerate(on_sl4_mats):
        acc = Rational(0)
        for Ta in on_T_mats:
            acc += vec(bracket(Ta, Bi)).dot(vec(bracket(Ta, Bj)))
        Cop[i, j] = acc
eigs = Cop.eigenvals()
print("\n[4b] EXACT spectrum of the torsion-coupling operator on sl(4):")
for lam, mult in sorted(eigs.items(), key=lambda kv: kv[0]):
    print(f"     eigenvalue {lam}  (multiplicity {mult})")

# --- WEAK FORM: kernel of ad_{T_BL} ------------------------------------------
M_bl = Matrix.hstack(*[vec(bracket(B, T_BL)) for B in sl4_basis])
null_bl = M_bl.nullspace()
dim_z_bl = len(null_bl)
Q_coords = Matrix.hstack(*[vec(B) for B in sl4_basis]).solve_least_squares(vec(Q))
in_kernel = all(x == 0 for x in (M_bl * Q_coords))
print("\n[5] WEAK FORM — centralizer of T_BL alone")
print(f"    dim {{X : [X, T_BL] = 0}} = {dim_z_bl}   (sl(3) + u(1): 8 + 1 = 9)")
print(f"    Q lies in this kernel : {in_kernel}")
print(f"    Q unique in this kernel : {dim_z_bl == 1}")

# --- VERDICT -----------------------------------------------------------------
print("\n" + "=" * 72)
print("VERDICT — read as it lies")
print("=" * 72)
strong_holds = (dim_centralizer == 1)
if dim_centralizer == 0:
    print("STRONG FORM: FALSIFIED (T4).")
    print("  The full torsion sector annihilates NOTHING: its centralizer in")
    print("  sl(4) is {0}. Q is not a torsion-null residue of the full sector —")
    print("  no direction is. Mechanism: T = Sym0(4), and only multiples of the")
    print("  identity commute with all of Sym0(4); tracelessness kills those.")
elif strong_holds:
    print("STRONG FORM: SURVIVES — centralizer is exactly 1-dimensional.")
else:
    print(f"STRONG FORM: FALSIFIED as stated — centralizer is {dim_centralizer}-dim, not 1.")

print()
sorted_eigs = sorted(eigs.items(), key=lambda kv: kv[0])
if len(sorted_eigs) == 2 and [m for _, m in sorted_eigs] == [9, 6]:
    lo, hi = sorted_eigs[0][0], sorted_eigs[1][0]
    print("POSITIVE RESIDUE (machine-verified, exact):")
    print(f"  The torsion-coupling operator on sl(4) has EXACTLY two eigenvalues:")
    print(f"    {lo} on the 9-dim symmetric (torsion) block")
    print(f"    {hi} on the 6-dim antisymmetric o(4) (Lorentz) block")
    print("  It is block-scalar: the ONLY structure torsion coupling can see at")
    print("  the algebra level is the Palatini split itself. No direction inside")
    print("  either block is graded — so no algebra-level computation of this")
    print("  form can single out an electromagnetic residue direction. Any 'EM")
    print("  as degradation' claim must live in the representation/embedding")
    print("  (where charges sit), not in the adjoint algebra. That is the")
    print("  boundary this test establishes.")

print()
if in_kernel and dim_z_bl > 1:
    print("WEAK FORM: PARTIAL (T3 observation, scope-bounded).")
    print(f"  Q IS annihilated by the vacuum direction T_BL, but so is the whole")
    print(f"  {dim_z_bl}-dim sl(3)+u(1) block. 'Torsion-null' is a property Q shares")
    print("  with every colour direction; Q's zero in the 0:1:4 ratio is real but")
    print("  NOT unique to Q at the level of the algebra. Uniqueness claims must")
    print("  live at the level of the physical boson embedding, not the algebra.")
elif in_kernel and dim_z_bl == 1:
    print("WEAK FORM: SURVIVES — Q is the unique T_BL-null direction.")
else:
    print("WEAK FORM: FALSIFIED — Q is not annihilated by T_BL.")
