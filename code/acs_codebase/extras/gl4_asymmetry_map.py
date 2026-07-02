#!/usr/bin/env python3
"""
GL(4) Asymmetry Map: What Does [e, ω] Generate?
=================================================
The "~10-page Lie theory computation" from Conjecture 9.6.

Question: For the vierbein e and connection ω on Y^14,
what is the image of the asymmetry map Φ(v) = [e(v), ω(v)]?

Theorem 9.2 showed Im(Φ) = sl(4) for GENERIC (e, ω).
But the physical question is: what happens when (e, ω) are
CONSTRAINED by the Palatini structure?

Specifically:
- e^a_μ is vierbein-compatible (invertible, gives metric)
- ω^{ab}_μ is a Lorentz connection (antisymmetric in ab)
- After vacuum selection: residual O(4) symmetry

This computation determines the CONSTRAINED image.

ALL arithmetic exact: symbolic over Q.
"""

from sympy import (
    Matrix, I, Rational, zeros, eye, simplify, expand,
    symbols, sqrt, pprint, BlockMatrix, Symbol, Trace
)
import itertools

print("=" * 70)
print("GL(4) ASYMMETRY MAP COMPUTATION")
print("What subalgebra does [e, ω] generate?")
print("=" * 70)

# ─── Step 1: Parameterize the vierbein ───────────────────────────────────────

print(f"\n── Step 1: Vierbein structure ──")

# The vierbein e^a_μ is a 4×4 invertible matrix
# At the vacuum: e^a_μ = δ^a_μ (flat spacetime)
# Perturbation: e^a_μ = δ^a_μ + ε h^a_μ
# The perturbation h^a_μ is a general 4×4 matrix (16 components)

# Under O(4) = SU(2)_L × SU(2)_R / Z_2:
# h^a_μ transforms as (2,2) of SU(2)_L × SU(2)_R

# The 16 components of h^a_μ split under O(4) as:
# Symmetric traceless (9) + antisymmetric (6) + trace (1)
# = metric perturbation + Lorentz rotation + conformal factor

print(f"   Vacuum vierbein: e^a_μ = δ^a_μ")
print(f"   Perturbation: h^a_μ has 16 components")
print(f"   Under O(4): 16 = 10 (symmetric) + 6 (antisymmetric)")

# ─── Step 2: Parameterize the connection ─────────────────────────────────────

print(f"\n── Step 2: Connection structure ──")

# The spin connection ω^{ab}_μ is antisymmetric in (a,b)
# So it has 6 × 4 = 24 components (but only 24 independent)
# Actually: ω^{ab}_μ with a<b gives 6 choices, times 4 for μ = 24

# Under O(4): the connection decomposes as
# ω ∈ (3,1) ⊕ (1,3) of SU(2)_L × SU(2)_R

# At the vacuum, ω = 0 (flat space, no curvature)
# Perturbation: ω^{ab}_μ = ε ω̃^{ab}_μ

print(f"   Vacuum connection: ω^{{ab}}_μ = 0")
print(f"   Perturbation: 6 × 4 = 24 components")
print(f"   Under O(4): (3,1) ⊕ (1,3)")

# ─── Step 3: The bracket [e, ω] in GL(4) ────────────────────────────────────

print(f"\n── Step 3: Computing the bracket [e, ω] ──")
print(f"   The bracket lives in gl(4) = End(R⁴)")
print("   [e, omega]^a_b = e^a_mu omega^mu_b - omega^a_mu e^mu_b")

# For a generic vierbein perturbation h and connection perturbation ω̃:
# [h, ω̃]^a_b = h^a_μ ω̃^μ_b - ω̃^a_μ h^μ_b

# Let's work with explicit 4×4 matrices
# h = general 4×4 (vierbein perturbation)
# ω̃ = antisymmetric 4×4 (connection perturbation, for fixed μ)

# The key question: as h ranges over all 4×4 matrices
# and ω̃ ranges over all antisymmetric 4×4 matrices,
# what is the span of [h, ω̃] = h·ω̃ - ω̃·h ?

# Parameterize h with 16 symbols
h_params = symbols('h0:16', real=True)
h = Matrix(4, 4, h_params)

# Parameterize ω̃ antisymmetric: 6 independent parameters
w_params = symbols('w0:6', real=True)
omega = Matrix([
    [0,          w_params[0], w_params[1], w_params[2]],
    [-w_params[0], 0,          w_params[3], w_params[4]],
    [-w_params[1], -w_params[3], 0,          w_params[5]],
    [-w_params[2], -w_params[4], -w_params[5], 0         ]
])

# Compute the commutator
bracket = h * omega - omega * h
bracket = expand(bracket)

print(f"   Bracket computed: 4×4 matrix with 16 entries")
print(f"   Each entry is linear in h-params and w-params")

# ─── Step 4: Determine the image ─────────────────────────────────────────────

print(f"\n── Step 4: Span of [h, ω̃] as h, ω̃ vary ──")

# Extract the 16 entries of the bracket as linear forms in the 22 parameters
all_params = list(h_params) + list(w_params)

# Build the coefficient matrix: each row is one (h,w) parameter pair,
# each column is one entry of the bracket
# Actually: the bracket entries are BILINEAR in (h, w)
# So we need to look at all products h_i * w_j

# The image of the map (h, ω̃) → [h, ω̃] is a linear subspace of gl(4)
# whose dimension we want to find.

# Since the map is bilinear, the image is spanned by all
# [E_{ij}, A_{kl}] where E_{ij} = basis matrix, A_{kl} = basis antisymmetric

# Basis for 4×4: E_{ij} has 1 at (i,j), 0 elsewhere
# Basis for antisymmetric: A_{kl} = E_{kl} - E_{lk} for k < l

print(f"   Computing all basis brackets [E_{{ij}}, A_{{kl}}]...")

image_vectors = []

for i in range(4):
    for j in range(4):
        # Basis vierbein perturbation E_{ij}
        E = zeros(4)
        E[i, j] = 1
        
        for k in range(4):
            for l in range(k+1, 4):
                # Basis antisymmetric A_{kl}
                A = zeros(4)
                A[k, l] = 1
                A[l, k] = -1
                
                # Commutator
                comm = E * A - A * E
                
                # Flatten to 16-vector
                vec = [comm[r, c] for r in range(4) for c in range(4)]
                
                if any(v != 0 for v in vec):
                    image_vectors.append(vec)

print(f"   Total non-zero basis brackets: {len(image_vectors)}")

# Find rank of the image (= dimension of generated subalgebra)
from sympy import Matrix as SympyMatrix

if image_vectors:
    M = SympyMatrix(image_vectors)
    rank = M.rank()
    print(f"   Rank of image matrix: {rank}")
    print(f"   dim(gl(4)) = 16, dim(sl(4)) = 15")
    print(f"   Image dimension: {rank}")

# ─── Step 5: Check if image is contained in sl(4) ───────────────────────────

print(f"\n── Step 5: Is the image traceless? ──")

all_traceless = True
for vec in image_vectors:
    # Trace = sum of diagonal entries: vec[0] + vec[5] + vec[10] + vec[15]
    tr = vec[0] + vec[5] + vec[10] + vec[15]
    if tr != 0:
        all_traceless = False
        break

print(f"   All brackets traceless: {all_traceless}")
if all_traceless:
    print(f"   ✓ Image ⊆ sl(4)")
    if rank == 15:
        print(f"   ✓ Image = sl(4) (dimension 15 = dim(sl(4)))")
    elif rank < 15:
        print(f"   Image is PROPER SUBALGEBRA of sl(4), dimension {rank}")

# ─── Step 6: Now constrain to PHYSICAL vierbein ─────────────────────────────

print(f"\n── Step 6: Physical constraint — symmetric vierbein perturbation ──")
print(f"   In Palatini gravity, the vierbein gives metric:")
print("   g_uv = eta_ab e^a_u e^b_v")
print(f"   Perturbation of metric: δg ~ h + h^T (symmetric part)")
print(f"   The antisymmetric part of h is a local Lorentz transformation")
print(f"   ")
print(f"   Physical DOF: h_(ab) = 10 (symmetric) — metric perturbation")
print("   Gauge DOF: h_[ab] = 6 (antisymmetric) -- Lorentz rotation")

# Constrain h to be SYMMETRIC (physical metric perturbation only)
image_symmetric = []

for i in range(4):
    for j in range(i, 4):  # Only i ≤ j (symmetric)
        # Symmetric basis: E_{ij} + E_{ji} (or just E_{ii} for diagonal)
        E = zeros(4)
        if i == j:
            E[i, j] = 1
        else:
            E[i, j] = 1
            E[j, i] = 1
        
        for k in range(4):
            for l in range(k+1, 4):
                A = zeros(4)
                A[k, l] = 1
                A[l, k] = -1
                
                comm = E * A - A * E
                vec = [comm[r, c] for r in range(4) for c in range(4)]
                
                if any(v != 0 for v in vec):
                    image_symmetric.append(vec)

M_sym = SympyMatrix(image_symmetric)
rank_sym = M_sym.rank()
print(f"\n   With symmetric h only:")
print(f"   Non-zero brackets: {len(image_symmetric)}")
print(f"   Rank: {rank_sym}")

# ─── Step 7: Constrain to ANTISYMMETRIC h (Lorentz transformations) ──────────

print(f"\n── Step 7: Gauge constraint — antisymmetric h (Lorentz rotations) ──")

image_antisym = []

for i in range(4):
    for j in range(i+1, 4):  # Only i < j (antisymmetric)
        E = zeros(4)
        E[i, j] = 1
        E[j, i] = -1
        
        for k in range(4):
            for l in range(k+1, 4):
                A = zeros(4)
                A[k, l] = 1
                A[l, k] = -1
                
                comm = E * A - A * E
                vec = [comm[r, c] for r in range(4) for c in range(4)]
                
                if any(v != 0 for v in vec):
                    image_antisym.append(vec)

M_anti = SympyMatrix(image_antisym)
rank_anti = M_anti.rank()
print(f"   With antisymmetric h only:")
print(f"   Non-zero brackets: {len(image_antisym)}")
print(f"   Rank: {rank_anti}")

# ─── Step 8: O(4) decomposition ─────────────────────────────────────────────

print(f"\n── Step 8: Summary of image dimensions ──")
print(f"   ")
print(f"   Generic h (all 16 DOF) + antisym ω (6 DOF):")
print(f"     → [h, ω̃] spans {rank}-dimensional subspace of gl(4)")
print(f"   ")
print(f"   Symmetric h (10 DOF) + antisym ω (6 DOF):")
print(f"     → [h, ω̃] spans {rank_sym}-dimensional subspace")
print(f"   ")
print(f"   Antisymmetric h (6 DOF) + antisym ω (6 DOF):")
print(f"     → [h, ω̃] spans {rank_anti}-dimensional subspace")
print(f"   ")
print(f"   Physical vierbein = symmetric (metric) + antisymmetric (Lorentz)")
print(f"   Connection = antisymmetric (Lorentz algebra)")
print(f"   ")
print(f"   The antisymmetric-antisymmetric bracket [h_{{[ab]}}, ω_{{[cd]}}]")
print(f"   generates a {rank_anti}-dimensional subalgebra.")
print(f"   This is the LORENTZ SECTOR — should be o(4) = su(2)⊕su(2), dim 6")

# Check: is rank_anti = 6?
if rank_anti == 6:
    print(f"   ✓ CONFIRMED: [o(4), o(4)] = o(4), dimension 6")
    print(f"     This is the self-bracket of the connection.")
elif rank_anti == 3:
    print(f"   Interesting: dimension 3 — might be one su(2) factor")
else:
    print(f"   Dimension {rank_anti} — investigating...")

# The symmetric-antisymmetric bracket [h_{{(ab)}}, ω_{{[cd]}}]
# generates the MIXED sector — this is where new structure lives
image_mixed = []
for i in range(4):
    for j in range(i, 4):
        E = zeros(4)
        if i == j:
            E[i, j] = 1
        else:
            E[i, j] = 1
            E[j, i] = 1
        
        for k in range(4):
            for l in range(k+1, 4):
                A = zeros(4)
                A[k, l] = 1
                A[l, k] = -1
                
                comm = E * A - A * E
                vec = [comm[r, c] for r in range(4) for c in range(4)]
                
                if any(v != 0 for v in vec):
                    image_mixed.append(vec)

# Check what the mixed sector generates BEYOND the Lorentz sector
all_vecs = image_antisym + image_mixed
M_all = SympyMatrix(all_vecs)
rank_all = M_all.rank()

print(f"\n   Mixed sector [h_{{(ab)}}, ω_{{[cd]}}]: spans {rank_sym}-dim space")
print(f"   Combined (Lorentz + mixed): spans {rank_all}-dim space")
print(f"   New directions from metric-connection bracket: {rank_all - rank_anti}")

# ─── Final summary ───────────────────────────────────────────────────────────

print(f"\n" + "=" * 70)
print("RESULTS — GL(4) ASYMMETRY MAP")
print("=" * 70)
print(f"")
print(f"1. UNCONSTRAINED: [gl(4), o(4)] = sl(4), dim {rank}")
print(f"   (Theorem 9.2 confirmed: generic bracket spans all of sl(4))")
print(f"")
print(f"2. LORENTZ SECTOR: [o(4), o(4)] → dim {rank_anti}")
print(f"   (Self-bracket of connection = curvature)")
print(f"")
print(f"3. METRIC SECTOR: [sym(4), o(4)] → dim {rank_sym}")
print(f"   (Vierbein-connection bracket = torsion)")
print(f"")
print(f"4. COMBINED (physical): dim {rank_all}")
print(f"   New directions beyond Lorentz: {rank_all - rank_anti}")
print(f"")
if rank_all == 15:
    print(f"CONCLUSION: Even with Palatini constraints, the bracket")
    print(f"generates ALL of sl(4). The SM cannot be selected by")
    print(f"the bracket alone — vacuum selection is REQUIRED.")
    print(f"This confirms Corollary 9.3.")
    print(f"  StrickenBy{{rule: derived-negative-load-bearing, reason: rank=15 => algebra")
    print(f"    selects NO direction; load-bearing leg of theta0-not-derivable-from-algebra")
    print(f"    (T2 derived negative; see theta0_derivation_suite.py OVERCLAIM LEDGER)}}")
elif rank_all < 15:
    print(f"CONCLUSION: Palatini constraints REDUCE the image!")
    print(f"dim(Im) = {rank_all} < 15 = dim(sl(4))")
    print(f"This is a NEW RESULT — the constrained bracket generates")
    print(f"a PROPER SUBALGEBRA of sl(4).")
    print(f"Identifying this subalgebra is the key question.")
