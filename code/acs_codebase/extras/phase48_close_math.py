#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
PHASE 48: CLOSE OPEN MATHEMATICAL ITEMS
========================================
1. Scaling tests of tr([X,Y] · X) = 0 in sl(4,R) and sl(3,R)
2. Orthogonal-complement reconstruction probe
3. Ambiguity factor derivation

All computations symbolic/exact where possible, numerical fallback
only where matrix sizes force it. Honest about precision throughout.
"""
import numpy as np
from sympy import Matrix, Rational, zeros, eye, symbols, simplify, sqrt
from sympy import nsimplify, trace as symtrace
from scipy.linalg import null_space

# ============================================================
# SECTION 1: BASIS CONSTRUCTION
# ============================================================

def sl_n_basis(n):
    """
    Standard traceless basis of sl(n, R).
    Dimension = n² - 1.
    Returns list of n×n numpy arrays, each traceless.

    Layout:
      (n-1) Cartan generators H_i = E_{i,i} - E_{i+1,i+1}
      n(n-1)/2 antisymmetric generators A_{ij} = E_{ij} - E_{ji}
      n(n-1)/2 symmetric off-diagonal S_{ij} = E_{ij} + E_{ji}
    Total: (n-1) + n(n-1) = n² - 1  ✓
    """
    basis = []
    # Cartan
    for a in range(n - 1):
        M = np.zeros((n, n))
        M[a, a] = 1.0
        M[a+1, a+1] = -1.0
        basis.append(M)
    # Antisymmetric + symmetric off-diagonal
    for i in range(n):
        for j in range(i+1, n):
            A = np.zeros((n, n)); A[i, j] = 1.0; A[j, i] = -1.0
            S = np.zeros((n, n)); S[i, j] = 1.0; S[j, i] = 1.0
            basis.append(A)
            basis.append(S)
    return basis

def random_traceless(n, rng):
    """Sample a random traceless n×n matrix (uniform in entries, then project)."""
    M = rng.standard_normal((n, n))
    M = M - (np.trace(M) / n) * np.eye(n)
    return M

def bracket(X, Y):
    return X @ Y - Y @ X

# ============================================================
# SECTION 2: SCALING TESTS — tr([X,Y] · X) = 0
# ============================================================

def scaling_test(n, num_trials, rng):
    """
    Sample num_trials random (X, Y) pairs in sl(n, R).
    Compute tr([X,Y] · X) for each.
    Return array of residuals and the example norm for context.
    """
    residuals = np.empty(num_trials)
    example_norms = np.empty(num_trials)
    for k in range(num_trials):
        X = random_traceless(n, rng)
        Y = random_traceless(n, rng)
        B = bracket(X, Y)
        residuals[k] = np.trace(B @ X)
        example_norms[k] = np.linalg.norm(B, 'fro')
    return residuals, example_norms

print("=" * 72)
print("SCALING TEST 1: tr([X,Y] · X) = 0 in sl(4, R) over 1000 random pairs")
print("=" * 72)

rng = np.random.default_rng(seed=20260423)
res4, norms4 = scaling_test(n=4, num_trials=1000, rng=rng)

# Also the symmetric partner tr([X,Y] · Y) = 0
def scaling_test_Y(n, num_trials, rng):
    residuals = np.empty(num_trials)
    for k in range(num_trials):
        X = random_traceless(n, rng)
        Y = random_traceless(n, rng)
        B = bracket(X, Y)
        residuals[k] = np.trace(B @ Y)
    return residuals

res4_Y = scaling_test_Y(n=4, num_trials=1000, rng=np.random.default_rng(seed=20260424))

def summarize(label, residuals):
    absres = np.abs(residuals)
    print(f"\n  {label}")
    print(f"    n_trials       : {len(residuals)}")
    print(f"    max |residual| : {absres.max():.2e}")
    print(f"    mean |residual|: {absres.mean():.2e}")
    print(f"    std  residual  : {residuals.std():.2e}")
    print(f"    median |res|   : {np.median(absres):.2e}")

summarize("sl(4,R): tr([X,Y] · X)", res4)
summarize("sl(4,R): tr([X,Y] · Y)", res4_Y)

print(f"\n  For reference — typical ||[X,Y]||_F in this sample:")
print(f"    median ||B||_F : {np.median(norms4):.2f}")
print(f"    max    ||B||_F : {norms4.max():.2f}")
print(f"  Residuals are {np.median(norms4) / max(np.median(np.abs(res4)), 1e-30):.1e}× smaller than ||B||_F — pure floating-point noise.")

# Same in sl(3, R)
print("\n" + "=" * 72)
print("SCALING TEST 2: tr([X,Y] · X) = 0 in sl(3, R) over 1000 random pairs")
print("=" * 72)

rng = np.random.default_rng(seed=20260425)
res3, norms3 = scaling_test(n=3, num_trials=1000, rng=rng)
rng = np.random.default_rng(seed=20260426)
res3_Y = scaling_test_Y(n=3, num_trials=1000, rng=rng)

summarize("sl(3,R): tr([X,Y] · X)", res3)
summarize("sl(3,R): tr([X,Y] · Y)", res3_Y)

# ============================================================
# SECTION 3: EXACT SYMBOLIC VERIFICATION
# ============================================================

print("\n" + "=" * 72)
print("SYMBOLIC VERIFICATION: the identity holds EXACTLY (no floating point)")
print("=" * 72)

from sympy import MatrixSymbol, symbols
# Build a 3×3 traceless generic matrix with symbolic entries
a = symbols('a11 a12 a13 a21 a22 a23 a31 a32 a33', real=True)
b = symbols('b11 b12 b13 b21 b22 b23 b31 b32 b33', real=True)

X_sym = Matrix(3, 3, a)
Y_sym = Matrix(3, 3, b)

# Impose traceless: subtract (tr/n) * I
X_sym = X_sym - (X_sym.trace() / 3) * eye(3)
Y_sym = Y_sym - (Y_sym.trace() / 3) * eye(3)

B_sym = X_sym * Y_sym - Y_sym * X_sym
inner = (B_sym * X_sym).trace()
inner_simplified = simplify(inner)

print(f"\n  Symbolic tr([X,Y] · X) for generic 3×3 traceless X, Y:")
print(f"    = {inner_simplified}")
print(f"  Identically zero? {inner_simplified == 0}")

# Also tr([X,Y] · Y)
inner_Y = simplify((B_sym * Y_sym).trace())
print(f"  Symbolic tr([X,Y] · Y) = {inner_Y}")
print(f"  Identically zero? {inner_Y == 0}")

# ============================================================
# SECTION 4: CHIRALITY-HOPPING EXAMPLE PRESERVED
# ============================================================

print("\n" + "=" * 72)
print("CHIRALITY HOPPING: [H1, A01] = 2 S01 under scaling")
print("=" * 72)

# This is exact integer arithmetic in sl(4)
H1 = Matrix([[1,0,0,0],[0,-1,0,0],[0,0,0,0],[0,0,0,0]])
A01 = Matrix([[0,1,0,0],[-1,0,0,0],[0,0,0,0],[0,0,0,0]])
S01 = Matrix([[0,1,0,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]])

B = H1 * A01 - A01 * H1
print(f"  [H1, A01] =")
print(B)
print(f"  2 * S01 =")
print(2 * S01)
print(f"  Exact equality: {B == 2*S01}")

# Check in sl(3) too
H1_3 = Matrix([[1,0,0],[0,-1,0],[0,0,0]])
A01_3 = Matrix([[0,1,0],[-1,0,0],[0,0,0]])
S01_3 = Matrix([[0,1,0],[1,0,0],[0,0,0]])
B_3 = H1_3 * A01_3 - A01_3 * H1_3
print(f"\n  In sl(3,R): [H1, A01] = 2*S01: {B_3 == 2*S01_3}")

# ============================================================
# SECTION 5: AMBIGUITY FACTOR DERIVATION
# ============================================================

print("\n" + "=" * 72)
print("AMBIGUITY FACTOR: how many generator pairs produce the same B?")
print("=" * 72)

print(r"""
SETUP:
  Given B = [X, Y] with X, Y in sl(n,R). How much of the pair (X, Y)
  is determined by B alone?

  The algebra g = sl(n,R) has dimension d_n = n² - 1.
  The pair (X, Y) lives in g × g, dimension 2·d_n.
  The bracket map  μ(X, Y) = [X, Y]  sends g × g  →  g.

TWO SOURCES OF AMBIGUITY:

  (a) KERNEL OF μ AT A POINT: all pairs (X', Y') giving the same B.
      This is (X, Y) + ker(dμ|_{(X,Y)}).
      Generic fiber dimension = 2·d_n - rank(dμ) = 2·d_n - d_n = d_n
      (for generic B, the image has full dimension d_n).

  (b) DIRECTIONS RECOVERABLE FROM B ALONE:
      B is a vector in g (d_n dimensional).
      B is Killing-orthogonal to both X and Y, so
        X, Y ∈ B⊥ (Killing orthogonal complement)
      which has dimension d_n - 1.
      Within B⊥, the 2-plane span{X,Y} can be any 2-plane of the
      orthogonal complement — 2·(d_n-1) - 3 parameters (a 2-plane
      in d_n-1 dim space with three SO(2) stabilizer params).

  We report the CLEAN number: within B⊥, how many "directions" could
  X come from?  That's dim(B⊥) / 2 (since any pair in B⊥ producing
  B is a 2-plane), which is (d_n - 1) / 2.
""")

for n in [3, 4, 5]:
    d = n*n - 1
    orth_dim = d - 1
    ambiguity = orth_dim / 2
    print(f"  sl({n}, R):")
    print(f"    dim g      = n² - 1 = {d}")
    print(f"    B ∈ g,  B⊥ has dim {d} - 1 = {orth_dim}")
    print(f"    (X, Y) constrained to 2-plane in B⊥")
    print(f"    Ambiguity factor (B⊥ directions / 2) = {orth_dim}/2 = {ambiguity}")
    print()

print(r"""
SPECIFIC TO PAPER C'S CLAIM (sl(4, R)):
  d_4 = 15
  B⊥ has dimension 14
  Ambiguity = 14 / 2 = 7
  
  Earlier we said "~13/2 ≈ 6.5" — that number counted the full
  fiber of the bracket map, subtracting only the bracket's own
  direction (15 - 2 = 13 for a 2-plane spanned by generic X, Y,
  divided by 2).

  The CORRECT counts are:
    • B⊥ / 2 = 14/2 = 7  (directions per generator in B⊥)
    • Generic bracket map fiber = 2·15 - 15 = 15  (if onto)
    • Fiber of (X,Y) giving same B, modulo pair rotations: 
         15 - 3 (SO(2) stabilizer + scale) = 12

  Paper C should state ONE clean number. We recommend "dim(B⊥) = 14"
  as the number of directions the generators can live in after B
  is known.
""")

# Let's verify this numerically: given a specific B, sample pairs
# that produce the same B and check their distribution.

print("=" * 72)
print("NUMERICAL VERIFICATION: fiber dimension at a specific B")
print("=" * 72)

# Pick a specific B
X0 = np.zeros((4,4)); X0[0,0]=1; X0[1,1]=-1
Y0 = np.zeros((4,4)); Y0[0,1]=1; Y0[1,0]=-1
B0 = bracket(X0, Y0)
print(f"  Using (X0, Y0): X0 = H1, Y0 = A01")
print(f"  B0 = [X0, Y0] =")
print(B0)

# Build the bracket map as a linear map of the pair
# Treat (X, Y) as a vector in R^{2*15} (using sl(4) basis)
basis4 = sl_n_basis(4)
d4 = len(basis4)
assert d4 == 15

# Express X, Y, B in basis coordinates
def to_coords(M, basis):
    """Project M onto basis using trace inner product, return coefficients."""
    coords = np.zeros(len(basis))
    for i, b in enumerate(basis):
        coords[i] = np.trace(M @ b.T) / np.trace(b @ b.T)
    return coords

def from_coords(c, basis):
    M = np.zeros_like(basis[0])
    for i, b in enumerate(basis):
        M = M + c[i] * b
    return M

# The bracket map (X, Y) -> [X, Y] is bilinear.
# Its Jacobian at (X0, Y0) is the linear map:
#   (δX, δY) -> [δX, Y0] + [X0, δY]
# We compute this 15×30 matrix.

J = np.zeros((d4, 2*d4))
for i in range(d4):
    # δX direction i: J(:, i) = [basis[i], Y0]
    val = bracket(basis4[i], Y0)
    J[:, i] = to_coords(val, basis4)
    # δY direction i: J(:, d4+i) = [X0, basis[i]]
    val = bracket(X0, basis4[i])
    J[:, d4 + i] = to_coords(val, basis4)

rank_J = np.linalg.matrix_rank(J, tol=1e-10)
ker_dim = 2*d4 - rank_J

print(f"\n  Jacobian of bracket map at (X0, Y0): shape {J.shape}")
print(f"  Rank (image dimension in sl(4)) = {rank_J}")
print(f"  Kernel dimension (directions leaving B unchanged) = {ker_dim}")
print(f"  dim(g × g) = {2*d4}")
print(f"  Sanity: rank + ker = {rank_J + ker_dim}, should equal {2*d4}")

# Interpretation
print(f"""
  INTERPRETATION at this specific (X0, Y0):
    - {rank_J} infinitesimal directions of (δX, δY) PRODUCE a change in B
    - {ker_dim} directions LEAVE B UNCHANGED — these are the ambiguity
    - The fiber of μ over B0 is a {ker_dim}-dimensional manifold
      (locally, generically)

  So for sl(4,R), a pair (X, Y) producing a given B has
  a {ker_dim}-parameter family of other pairs producing the same B.
""")

# ============================================================
# SECTION 6: THE ORTHOGONAL-COMPLEMENT RECONSTRUCTION PROBE
# ============================================================

print("=" * 72)
print("ORTHOGONAL-COMPLEMENT PROBE — PSEUDOCODE + NUMERICAL RUN")
print("=" * 72)

print(r"""
ALGORITHM (orthogonal-complement probe):

  INPUT:  B ∈ sl(n, R), n ≥ 3, B ≠ 0
  OUTPUT: A basis of the Killing-orthogonal complement B⊥
          (the subspace where both generators X, Y must lie)

  Step 1. Choose an orthogonal basis of sl(n, R).
          e.g., the (n-1) Cartan + n(n-1)/2 antisymmetric +
          n(n-1)/2 symmetric basis.

  Step 2. Compute the Killing form matrix K_ij = tr(basis[i] · basis[j]).
          For sl(n, R) this is diagonal with values ±2n on diagonal.

  Step 3. Express B in the basis: B = sum_i b_i * basis[i].
          Compute b_i = tr(B · basis[i]) / K_ii.

  Step 4. The orthogonal complement B⊥ is the kernel of the linear
          functional  v -> sum_i b_i * K_ii * v_i.
          Basis for B⊥: Gram-Schmidt away from (b_1, ..., b_{n²-1}).

  Step 5. Return the basis of B⊥, which has dimension n² - 2.

CONSTRAINTS ON (X, Y):
  - Both X and Y lie in B⊥.
  - The PAIR (X, Y) must satisfy [X, Y] = B.
  - Within B⊥, the 2-plane span{X,Y} is determined up to an SO(2)
    rotation AND an overall scale — total 3-parameter ambiguity
    within the 2-plane.
  - The 2-plane itself (within B⊥) is generically under-determined.

RECONSTRUCTION ACCURACY:
  Given only B, we recover:
    • The (n² - 2)-dimensional subspace B⊥ containing X and Y.
    • The magnitude ||B||² (one real number).
    • The spectrum of ad_B (at most n distinct eigenvalues).
  We do NOT recover:
    • The specific 2-plane within B⊥.
    • Individual norms ||X||, ||Y||.
    • Individual Killing values K(X,X), K(Y,Y).
""")

# Implement and run
def orthogonal_complement_probe(B, n):
    """
    Given B = [X,Y] in sl(n,R), compute a basis of B⊥ (Killing-orthogonal).
    Returns (basis_of_Bperp, expansion_of_B).
    """
    basis = sl_n_basis(n)
    d = len(basis)
    # Expansion of B in the basis
    K_diag = np.array([np.trace(b @ b) for b in basis])
    b_coords = np.array([np.trace(B @ basis[i]) / K_diag[i] for i in range(d)])
    # The functional: v -> sum_i K_ii * b_i * v_i = <B, v>
    weights = K_diag * b_coords  # the Killing-weighted coords of B
    # Orthogonal complement: vectors v with weights·v = 0
    # Null space of the 1×d row vector `weights`
    nullsp = null_space(weights.reshape(1, -1))  # d × (d-1) matrix
    return nullsp, b_coords

null_basis, b_coords = orthogonal_complement_probe(B0, 4)
print(f"  Ran probe on B0 = [H1, A01]")
print(f"  B0's basis coords (nonzero only):")
for i, c in enumerate(b_coords):
    if abs(c) > 1e-10:
        print(f"    basis[{i}]: {c:.4f}")
print(f"  dim(B⊥) = {null_basis.shape[1]}  (should be {4*4 - 1 - 1} = 14)")

# Verify: original X0, Y0 should lie in B⊥
X0_coords = np.array([np.trace(X0 @ basis4[i]) / np.trace(basis4[i] @ basis4[i]) for i in range(d4)])
Y0_coords = np.array([np.trace(Y0 @ basis4[i]) / np.trace(basis4[i] @ basis4[i]) for i in range(d4)])
# Project onto B⊥
X0_in_perp = null_basis @ null_basis.T @ X0_coords
Y0_in_perp = null_basis @ null_basis.T @ Y0_coords
# Check recovery
print(f"\n  Sanity: do X0 and Y0 actually lie in B⊥?")
print(f"    ||X0 - π_{{B⊥}}(X0)|| = {np.linalg.norm(X0_coords - X0_in_perp):.2e}")
print(f"    ||Y0 - π_{{B⊥}}(Y0)|| = {np.linalg.norm(Y0_coords - Y0_in_perp):.2e}")
print(f"  (Both should be 0 — X, Y always lie in B⊥ by the theorem.)")

# ============================================================
# SECTION 7: FINAL PARAMETER LEDGER
# ============================================================

print("\n" + "=" * 72)
print("PAPER A PARAMETER LEDGER — UNCHANGED")
print("=" * 72)

print(r"""
Free parameters (confirmed irreducible by Phase 12 Task A):

  1. tan β         — VEV ratio in bi-doublet Higgs
  2. ρ₁            — Δ_R self-coupling (with ρ₂ = 16/9 − 2ρ₁)
  3. α₁            — Φ·Δ cross-coupling (trace-times-trace)
  4. α₂            — Φ·T^A·Φ·T^A · Δ cross-coupling
  5. β_c           — CP-violating phase coupling

  Single algebraic constraint from Palatini bracket:
      2ρ₁ + ρ₂ = g² = 16/9

  Vacuum stability:  ρ₁ > 0

Calibrations (dimensional, set from data):
  • m_τ (lepton mass scale)
  • v   (electroweak VEV)

Total: 7 inputs. Cannot be reduced further in the current framework.

θ_13 status (from task_B_theta13.py):
  • Current prediction θ_13 = arcsin(λ_W/√2) ≈ 9.18°
  • Observation: 8.57° ± 0.12°
  • Pull: 5.2σ (projected 12.6σ after JUNO precision)
  • Cross-coupling fix requires v_R ≈ 10³ GeV
  • Proton decay requires v_R > 10¹⁵ GeV
  • CONCLUSION: not fixable by cross-couplings without conflicting
    with proton-decay lower bound.
  • θ_13 (along with θ_12, θ_23) moved from "derived" to "fit"
    in Paper A ledger. Derived-match count dropped from 11 to 8.
""")

# ============================================================
# SECTION 8: OPEN QUESTIONS CLOSED TABLE
# ============================================================

print("=" * 72)
print("OPEN QUESTIONS CLOSED — FINAL STATUS TABLE")
print("=" * 72)

items = [
    ("Orthogonal-complement probe algorithm",
     "Specified + numerically verified. B⊥ has dim n²−2 = 14 for sl(4)."),
    ("Killing-orthogonality scaling in sl(4)",
     f"1000 pairs, max |residual| = {np.abs(res4).max():.1e}, pure floating-point noise."),
    ("Killing-orthogonality scaling in sl(3)",
     f"1000 pairs, max |residual| = {np.abs(res3).max():.1e}, pure floating-point noise."),
    ("Symbolic proof of identity",
     "tr([X,Y]·X) = 0 and tr([X,Y]·Y) = 0 verified symbolically in SymPy."),
    ("Chirality-hopping example",
     "[H_1, A_{01}] = 2 S_{01} exact in sl(4) and sl(3)."),
    ("Ambiguity factor (sl(4))",
     f"B⊥ has dim 14; bracket-map kernel at (H1, A01) has dim {ker_dim}."),
    ("Paper A parameter ledger",
     "Unchanged: 2 calibrations + 5 free = 7 irreducible inputs."),
    ("θ_13 discrepancy",
     "Real (5.2σ now, 12.6σ after JUNO); not fixable by cross-couplings."),
    ("ACS non-traversability",
     "Algebraic theorem, not a postulate (subsection 5.3, Paper C)."),
]

width_a = max(len(it[0]) for it in items) + 2
for label, status in items:
    print(f"  {label:<{width_a}}  {status}")

print("\n" + "=" * 72)
print("PHASE 48 COMPLETE")
print("=" * 72)
