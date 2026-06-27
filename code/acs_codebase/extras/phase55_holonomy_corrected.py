#!/usr/bin/env python3
"""
PHASE 55 (CORRECTED): DOES THE THREE-STEP HOLONOMY GENERALIZE?
================================================================
First attempt treated ad_{T_BL} as a rotation generator. Numerics
showed ||U - I|| growing to 2174 at t = 2π — a red flag that
revealed my setup was wrong.

The correct statement: ad_{T_BL} has REAL eigenvalues (0, ±4/3),
so exp(t · ad) is hyperbolic (exponential growth/decay on the ±4/3
eigenspaces), NOT rotational.

The "three-step 2π inversion" from SU(2) quaternions does NOT
generalize to the sl(4,R) Palatini structure. What generalizes is
Cayley-Hamilton saturation at degree 3, but the geometric content
is different in each case.
"""
import numpy as np

print("=" * 72)
print("PHASE 55: HOLONOMY IN sl(4,R) — CORRECTED ANALYSIS")
print("=" * 72)

T_BL = np.diag([1/3, 1/3, 1/3, -1.0])

# Find correct eigenvectors
# Upper-triangular E_{i,3} has eigenvalue +4/3 under ad_{T_BL}
# Lower-triangular E_{3,i} has eigenvalue -4/3

E_03_up = np.zeros((4,4)); E_03_up[0,3] = 1
E_13_up = np.zeros((4,4)); E_13_up[1,3] = 1
E_23_up = np.zeros((4,4)); E_23_up[2,3] = 1
E_30_down = np.zeros((4,4)); E_30_down[3,0] = 1
E_31_down = np.zeros((4,4)); E_31_down[3,1] = 1
E_32_down = np.zeros((4,4)); E_32_down[3,2] = 1

def bracket(X, Y):
    return X @ Y - Y @ X

print("\nEigenvectors of ad_{T_BL} (verified):")
for M, label, expected in [
    (E_03_up, "E_{03}", 4/3),
    (E_13_up, "E_{13}", 4/3),
    (E_23_up, "E_{23}", 4/3),
    (E_30_down, "E_{30}", -4/3),
    (E_31_down, "E_{31}", -4/3),
    (E_32_down, "E_{32}", -4/3),
]:
    result = bracket(T_BL, M)
    ratio = result[result.nonzero()][0] / M[M.nonzero()][0] if M.any() else 0
    print(f"  [T_BL, {label}] = ({ratio:.4f}) · {label}  (expected {expected:+.4f})")

print(r"""

KEY STRUCTURAL FACT:

  ad_{T_BL} has REAL eigenvalues {0, +4/3, -4/3}.
  
  Therefore exp(t · ad_{T_BL}) acts as:
    - identity on the λ=0 eigenspace (9-dim)
    - exp(+4t/3) on the λ=+4/3 eigenspace (3-dim) — EXPONENTIAL GROWTH
    - exp(-4t/3) on the λ=-4/3 eigenspace (3-dim) — EXPONENTIAL DECAY
  
  This is HYPERBOLIC evolution (like a Lorentz boost), NOT rotational.
  
  At t = 2π:
    exp(8π/3) ≈ 4348   ← upper eigenspace grows by 4348×
    exp(-8π/3) ≈ 0.00023  ← lower eigenspace decays to ~0
    
  So "exp(t · ad_{T_BL}) at t = 2π" does NOT return anywhere close
  to the identity. There is no geometric "2π loop" in the sense of 
  the SU(2) quaternion case.
""")

# Verify with explicit computation
for t_test in [np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]:
    scale_up = np.exp(4*t_test/3)
    scale_dn = np.exp(-4*t_test/3)
    print(f"  At t = {t_test/np.pi:.2f}π:")
    print(f"    Upper eigenspace: × {scale_up:.2e}")
    print(f"    Lower eigenspace: × {scale_dn:.2e}")

print(r"""

COMPARISON WITH SU(2) QUATERNION CASE:

  In SU(2), the generators of rotations are iσ_k (Hermitian, real
  eigenvalues of σ_k but IMAGINARY eigenvalues of iσ_k).
  
  exp(i·t·σ_3/2) is a genuine rotation on spinor space because iσ_3
  has eigenvalues ±i (purely imaginary).
  
  For ad_{T_BL}: eigenvalues are ±4/3 (purely real).
  So "exp(t·ad_{T_BL})" is boost-like, not rotation-like.

  TO GET A ROTATION in the Palatini algebra, we would need to use
  i·ad_{T_BL} (multiply by i). Then:
    i·ad has eigenvalues {0, ±4i/3}
    exp(t · i·ad) on ±4i/3 eigenspace = exp(±4it/3)  — rotation
    
  At t = 3π/2: exp(±i·2π) = 1  (full return)
  At t = 3π/4: exp(±i·π) = -1  (sign flip)

  But the factor of i is NOT natural in the Palatini bracket context,
  where all fields are real. This is the mathematical obstruction.

WHAT THIS MEANS:

  The SU(2) quaternion "three 120° rotations compose to 2π" picture
  is a feature of the COMPLEX / IMAGINARY exponentiation, not of the
  number 3 itself.

  In sl(4,R) with T_BL having real eigenvalues, the analogous
  "three-step" structure is NOT a geometric rotation but an
  ALGEBRAIC closure: ad^3 = (16/9) ad by Cayley-Hamilton.

  Paper C's "2π inversion after three steps" is specific to the
  SU(2) representation where the adjoint generates rotations. It
  does not transfer to the full sl(4,R) Palatini algebra.
""")

print("=" * 72)
print("WHAT ACTUALLY SURVIVES AS A GENERAL PATTERN")
print("=" * 72)

print(r"""
Collecting all the three-order phenomena we've verified:

  SYSTEM              CAYLEY-HAMILTON RELATION       GEOMETRIC CONTENT
  -----------------   ----------------------------   ----------------------
  SU(2) quaternion    (iσ_3)² = -I,  period 2π      2π rotation = -I
  sl(4,R) Palatini    ad^3 = (16/9) ad              Hyperbolic, no 2π loop
  Core rope ring      R³ = R                        Z/3Z permutation
  Frenet-Serret       A³ = -(κ²+χ²) A               Curvature-torsion rot.
  
COMMON FEATURE: Cayley-Hamilton saturation at low order (2 or 3).

NOT COMMON: "2π geometric inversion" — this only applies where
the generator has IMAGINARY eigenvalues (rotational structure).

PAPER C SHOULD CLAIM:
  (a) Various ACS systems exhibit low-order algebraic closure via
      Cayley-Hamilton on the relevant structural operator.
  (b) The specific degree (2 for SU(2), 3 for sl(4,R), etc.) depends
      on the operator's minimal polynomial.
  (c) In cases where the operator has imaginary eigenvalues (e.g.,
      SU(2) rotations), this closure has geometric content as a
      2π inversion; in cases with real eigenvalues (e.g., sl(4,R) 
      Palatini B-L generator), it is purely algebraic.

PAPER C SHOULD NOT CLAIM:
  "Three-step bracket chains always produce 2π geometric inversions."
  This is false in sl(4,R) and was only ever true in specific 
  representations where the adjoint acts by rotation.

THE "INVERSION ARC" NARRATIVE:
  The forward half (c/a-theorem monotonicity to IR) is rigorous.
  The post-attractor extension remains conjectural.
  The "2π holonomy" framing is REPRESENTATION-DEPENDENT, not
  universal.
""")

print("=" * 72)
print("PHASE 55 FINAL VERDICT")
print("=" * 72)

print(r"""
The three-step quaternion holonomy from SU(2) does NOT generalize
to the sl(4,R) Palatini adjoint action. The two systems share the
integer 3 for DIFFERENT reasons:

  SU(2): three 120° rotations fill 2π (geometric)
  sl(4,R): minimal polynomial of ad_{T_BL} has degree 3 (algebraic)

These are related structurally (Cayley-Hamilton governs both) but
have DIFFERENT geometric content. Paper C's "2π inversion after
three steps" is a feature of the SU(2) representation, not a
universal ACS theorem.

PAPER C REVISION:
  Separate the narrative into:
  
  (a) RIGOROUS: c/a-theorem as proved instance of inversion-arc
      forward half.
      
  (b) ALGEBRAIC: Cayley-Hamilton saturation at finite order across
      multiple ACS systems (SU(2), sl(4,R), core rope, Frenet-Serret).
      Common pattern, different specific mechanisms.
      
  (c) GEOMETRIC "2π inversion": specific to SU(2) and other
      representations with imaginary adjoint eigenvalues. NOT a
      universal ACS feature.
      
  (d) CONJECTURAL: post-attractor ΔI < 0 behavior, "key becomes 
      the lock" narrative. Flagged as interpretive motivation, not
      theorem.

This is the clean, defensible version. It preserves the interesting
structural content (algebraic closure at order 3, cross-system
correspondences) without overclaiming geometric universality.

APPLIED EPISTEMIC DISCIPLINE:
  A promising narrative ("every ACS system inverts at 2π after three
  steps") tested against explicit computation, found to be specific
  rather than universal, downgraded in scope. Same pattern as Paper B's
  Poisson-bracket retreat and Paper A's parameter-count tightening.

No retreat in substance — the Cayley-Hamilton pattern is real and
important. Just correct scope: algebraic saturation, not geometric
2π inversion in all representations.
""")
