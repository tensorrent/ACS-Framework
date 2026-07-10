#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
THE SU(3) QUESTION: Does the torsion sector contain colour?
============================================================
The Palatini decomposition gives:
  sl(4) = o(4) [6-dim, Lorentz] ⊕ torsion [9-dim, (3,3)]

su(3) lives inside sl(4) via Pati-Salam [8-dim].

QUESTION: dim(torsion_sector ∩ su(3)) = ?

If 8: torsion CONTAINS su(3) → colour from geometry
If 0: colour requires extra structure (KK, spinor bundle, etc.)
If between: partial overlap → interesting constraints

ALL arithmetic exact over Q[i, √3].
"""

from sympy import (
    Matrix, I, Rational, zeros, eye, simplify, sqrt, 
    pprint, GramSchmidt
)

print("=" * 70)
print("THE SU(3) QUESTION")
print("Does the 9-dim torsion sector contain the 8-dim colour algebra?")
print("=" * 70)

# ─── Step 1: Construct the 9-dim torsion sector basis ────────────────────────

print("\n── Step 1: Torsion sector basis ──")
print("   [Sym₀(4), o(4)] — computed from basis brackets")

def E(i, j, n=4):
    m = zeros(n)
    m[i, j] = 1
    return m

def comm(A, B):
    return A * B - B * A

# Basis for Sym₀(4): traceless symmetric 4×4
sym_basis = []
sym_labels = []

# Off-diagonal symmetric
for i in range(4):
    for j in range(i+1, 4):
        sym_basis.append(E(i,j) + E(j,i))
        sym_labels.append(f"S_{i}{j}")

# Traceless diagonal
for i in range(3):
    d = zeros(4)
    d[i,i] = 1
    d[3,3] = -1
    sym_basis.append(d)
    sym_labels.append(f"D_{i}")

# Basis for o(4): antisymmetric 4×4
anti_basis = []
anti_labels = []
for i in range(4):
    for j in range(i+1, 4):
        anti_basis.append(E(i,j) - E(j,i))
        anti_labels.append(f"A_{i}{j}")

print(f"   Sym₀(4) basis: {len(sym_basis)} elements")
print(f"   o(4) basis: {len(anti_basis)} elements")

# Compute all brackets [S, A] and collect the image vectors
torsion_vectors = []
for S in sym_basis:
    for A in anti_basis:
        bracket = comm(S, A)
        # Flatten to 16-vector
        vec = []
        for r in range(4):
            for c in range(4):
                vec.append(simplify(bracket[r, c]))
        if any(v != 0 for v in vec):
            torsion_vectors.append(vec)

print(f"   Non-zero brackets: {len(torsion_vectors)}")

# Find basis for the torsion subspace
torsion_matrix = Matrix(torsion_vectors)
torsion_rank = torsion_matrix.rank()
print(f"   Torsion sector dimension: {torsion_rank}")

# Get a basis via row reduction
torsion_rref, torsion_pivots = torsion_matrix.rref()
torsion_basis_vectors = [torsion_matrix.row(p) for p in range(len(torsion_vectors)) 
                         if any(torsion_rref[i, :] != zeros(1, 16) for i in range(torsion_matrix.rows))]

# Actually, let's use the RREF rows directly
torsion_space_basis = []
for i in range(torsion_rref.rows):
    row = torsion_rref.row(i)
    if any(row[j] != 0 for j in range(16)):
        torsion_space_basis.append(list(row))
    if len(torsion_space_basis) == torsion_rank:
        break

print(f"   Basis vectors extracted: {len(torsion_space_basis)}")

# ─── Step 2: Construct su(3) inside sl(4) ────────────────────────────────────

print("\n── Step 2: su(3) generators inside sl(4) ──")

half = Rational(1, 2)

# Gell-Mann matrices λ_a in 4×4 (upper-left 3×3 block)
# T_a = λ_a / 2, then su(4) element is i*T_a (skew-Hermitian)
# But we're working in sl(4,R), so we need the REAL form

# The real form of su(3) in sl(4,R) has 8 generators.
# These are the matrices i*T_a expressed as real 4×4.
# For real sl(4): generators are traceless real 4×4.
# su(3) ⊂ sl(4,C), but we need su(3) ∩ sl(4,R).

# Actually, su(3) as a REAL Lie algebra has dimension 8.
# Its generators in the fundamental rep are i*λ_a/2.
# These are 3×3 skew-Hermitian matrices.
# Embedded in 4×4, they're still skew-Hermitian.

# As REAL matrices, a skew-Hermitian matrix X satisfies X = -X^†.
# Writing X = A + iB where A is real and B is real:
# A + iB = -(A^T - iB^T) = -A^T + iB^T
# So A = -A^T (antisymmetric) and B = B^T (symmetric).

# The REAL and IMAGINARY parts of the su(3) generators:
# λ₁ = [[0,1,0],[1,0,0],[0,0,0]] → real symmetric
# i*λ₁/2 has real part 0, imaginary part λ₁/2 → as a complex matrix
# But in REAL sl(4), we represent complex matrices as 2n×2n real... 

# Wait. Let me reconsider. sl(4,R) is the algebra of REAL traceless 4×4.
# su(3) as embedded in sl(4,C) uses COMPLEX matrices.
# The intersection su(3) ∩ sl(4,R) is a real form.

# The standard real form: su(3) has a compact real form (itself) and
# a split real form sl(3,R). 
# sl(3,R) ⊂ sl(4,R) embeds naturally (upper-left 3×3 block, traceless).
# dim(sl(3,R)) = 8.

# So the right question is: does the torsion sector contain sl(3,R)?

# Generators of sl(3,R) in sl(4,R):
# 8 generators: 3 diagonal (traceless in 3×3, extended to 4×4) + 
# 6 off-diagonal (E_{ij} for i≠j, i,j ∈ {0,1,2})
# But traceless in sl(4) means trace over 4×4 = 0.

# Upper-left 3×3 traceless: E_{ij} for i≠j (6 matrices) +
# diagonal: d₁ = diag(1,-1,0,0), d₂ = diag(0,1,-1,0) (2 matrices)
# Total: 8 = dim(sl(3,R)) ✓

# But these need to also be traceless in 4×4.
# E_{ij} for i,j ∈ {0,1,2}: already traceless. ✓
# d₁ = diag(1,-1,0,0): Tr = 0. ✓
# d₂ = diag(0,1,-1,0): Tr = 0. ✓

sl3_generators = []
sl3_labels = []

# Off-diagonal: E_{ij} for i,j ∈ {0,1,2}, i ≠ j
for i in range(3):
    for j in range(3):
        if i != j:
            gen = E(i, j)
            sl3_generators.append(gen)
            sl3_labels.append(f"E_{i}{j}")

# Diagonal: two independent traceless diagonals
d1 = Matrix([[1,0,0,0],[0,-1,0,0],[0,0,0,0],[0,0,0,0]])
d2 = Matrix([[0,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,0]])
sl3_generators.append(d1)
sl3_labels.append("d1=diag(1,-1,0,0)")
sl3_generators.append(d2)
sl3_labels.append("d2=diag(0,1,-1,0)")

print(f"   sl(3,R) generators: {len(sl3_generators)}")
for label, gen in zip(sl3_labels, sl3_generators):
    print(f"     {label}: Tr={simplify(gen.trace())}, in upper-left 3×3: {all(gen[i,3]==0 and gen[3,i]==0 for i in range(4))}")

# Verify closure
print("\n   Verifying sl(3,R) closes under commutation...")
closure_ok = True
for a in range(8):
    for b in range(a+1, 8):
        bracket = comm(sl3_generators[a], sl3_generators[b])
        # Check bracket is in span of generators
        is_upper_3x3 = all(simplify(bracket[i,3]) == 0 and simplify(bracket[3,i]) == 0 for i in range(4))
        is_traceless = simplify(bracket.trace()) == 0
        if not is_upper_3x3 or not is_traceless:
            closure_ok = False
            print(f"   FAIL: [{sl3_labels[a]}, {sl3_labels[b]}] escapes")
            break
print(f"   sl(3,R) closes: {closure_ok}")

# Flatten sl(3) generators to 16-vectors
sl3_vectors = []
for gen in sl3_generators:
    vec = [gen[r,c] for r in range(4) for c in range(4)]
    sl3_vectors.append(vec)

sl3_matrix = Matrix(sl3_vectors)
sl3_rank = sl3_matrix.rank()
print(f"   sl(3,R) dimension in sl(4,R): {sl3_rank}")

# ─── Step 3: THE DECISIVE COMPUTATION — intersection ─────────────────────────

print("\n── Step 3: INTERSECTION ──")
print("   Computing dim(torsion_sector ∩ sl(3,R))...")

# Stack torsion basis and sl(3) basis, find the dimension of their intersection.
# Intersection dimension = dim(torsion) + dim(sl3) - dim(torsion + sl3)

# Build combined matrix
combined_vectors = torsion_space_basis + sl3_vectors
combined_matrix = Matrix(combined_vectors)
combined_rank = combined_matrix.rank()

intersection_dim = torsion_rank + sl3_rank - combined_rank

print(f"   dim(torsion) = {torsion_rank}")
print(f"   dim(sl(3,R)) = {sl3_rank}")
print(f"   dim(torsion + sl(3,R)) = {combined_rank}")
print(f"   dim(torsion ∩ sl(3,R)) = {intersection_dim}")

# ─── Step 4: Interpret the result ────────────────────────────────────────────

print(f"\n── Step 4: Interpretation ──")

if intersection_dim == 8:
    print("   ★ TORSION CONTAINS ALL OF sl(3,R)")
    print("   The 9-dim torsion sector contains the entire colour algebra!")
    print("   The extra 1 dimension is the u(1) hypercharge direction.")
    print("   COLOUR CHARGE ARISES FROM GEOMETRIC TORSION.")
elif intersection_dim == 0:
    print("   ✗ ZERO OVERLAP")  
    print("   The torsion sector and colour algebra are complementary.")
    print("   SU(3) definitively requires extra structure beyond Palatini.")
elif intersection_dim > 0:
    print(f"   ~ PARTIAL OVERLAP: {intersection_dim} dimensions")
    print(f"   {intersection_dim} of 8 colour generators lie in the torsion sector.")
    print(f"   The remaining {8 - intersection_dim} require other sources.")
    
    # Identify WHICH generators are in the intersection
    print(f"\n   Identifying which sl(3) generators are in torsion sector...")
    for idx, (label, vec) in enumerate(zip(sl3_labels, sl3_vectors)):
        # Check if this vector is in the torsion subspace
        # Add it to torsion basis and check if rank increases
        test_matrix = Matrix(torsion_space_basis + [vec])
        test_rank = test_matrix.rank()
        in_torsion = (test_rank == torsion_rank)  # Rank doesn't increase = vector is in span
        status = "IN torsion" if in_torsion else "NOT in torsion"
        print(f"     {label}: {status}")

# ─── Step 5: Check the FULL Pati-Salam subalgebra ────────────────────────────

print(f"\n── Step 5: What about su(3) ⊕ u(1)_{{B-L}}? ──")

# Add the hypercharge generator
Y = Matrix([[Rational(1,3),0,0,0],[0,Rational(1,3),0,0],
            [0,0,Rational(1,3),0],[0,0,0,-1]])
Y_vec = [Y[r,c] for r in range(4) for c in range(4)]

ps_vectors = sl3_vectors + [Y_vec]
ps_matrix = Matrix(ps_vectors)
ps_rank = ps_matrix.rank()

combined_ps = Matrix(torsion_space_basis + ps_vectors)
combined_ps_rank = combined_ps.rank()

ps_intersection = torsion_rank + ps_rank - combined_ps_rank

print(f"   dim(su(3) ⊕ u(1)_{{B-L}}) = {ps_rank}")
print(f"   dim(torsion ∩ (su(3) ⊕ u(1))) = {ps_intersection}")

# ─── Step 6: Decomposition under Lorentz ─────────────────────────────────────

print(f"\n── Step 6: How does sl(3,R) decompose under o(4)? ──")

# Check which sl(3) generators are symmetric vs antisymmetric
print("   Symmetric/antisymmetric decomposition of sl(3,R) generators:")
n_sym = 0
n_anti = 0
n_neither = 0
for label, gen in zip(sl3_labels, sl3_generators):
    is_sym = (gen == gen.T)
    is_anti = (gen == -gen.T)
    if is_sym:
        kind = "SYMMETRIC"
        n_sym += 1
    elif is_anti:
        kind = "ANTISYMMETRIC"
        n_anti += 1
    else:
        kind = "NEITHER"
        n_neither += 1
    print(f"     {label}: {kind}")

print(f"\n   Symmetric (→ torsion sector candidate): {n_sym}")
print(f"   Antisymmetric (→ Lorentz sector candidate): {n_anti}")
print(f"   Neither: {n_neither}")

# The symmetric generators of sl(3) are in Sym₀(4)
# The antisymmetric generators of sl(3) are in o(4)
# But the TORSION SECTOR is [Sym₀(4), o(4)], not Sym₀(4) itself!
# So symmetric sl(3) generators are in Sym₀(4) but may or may not
# be in the IMAGE of the bracket map.

print(f"\n" + "=" * 70)
print("FINAL ANSWER")
print("=" * 70)
print(f"dim(torsion ∩ sl(3,R)) = {intersection_dim} out of 8")
if intersection_dim >= 1:
    print(f"dim(torsion ∩ (sl(3) ⊕ u(1))) = {ps_intersection} out of 9")
