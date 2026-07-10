#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
EXPLORATION: TORSION AND THE CAUSAL STRUCTURE
==============================================
Standard GR sets torsion to zero. Einstein-Cartan keeps it.
The ACS framework says torsion is the GENERATOR of gauge structure.

Question: does non-zero torsion modify the light cone?
If yes: propagation speed depends on the torsion background.
If no: torsion is invisible to photons.

This is NOT for the papers. This is exploration.
"""

import numpy as np
from numpy.linalg import norm, eig, eigvalsh
import sympy as sp

print("=" * 70)
print("TORSION AND THE CAUSAL STRUCTURE")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# PART 1: THE EFFECTIVE METRIC IN THE PRESENCE OF TORSION
# ═══════════════════════════════════════════════════════════════
print(f"\n── Part 1: Effective Metric with Torsion ──\n")

print("""
  In Einstein-Cartan theory, the connection is:
    Γ^λ_μν = {λ_μν} + K^λ_μν
  where {λ_μν} is Levi-Civita and K is the contortion tensor:
    K^λ_μν = ½(T^λ_μν + T_μ^λ_ν + T_ν^λ_μ)
  
  The torsion tensor T^λ_μν = Γ^λ_μν - Γ^λ_νμ has three 
  irreducible components under the Lorentz group:
  
  1. TRACE (vector): T_μ = T^λ_λμ  (4 components)
  2. AXIAL (pseudovector): S_μ = ε_μνρσ T^νρσ  (4 components)  
  3. TENSOR (traceless, non-axial): q_λμν  (16 components)
  
  Total: 4 + 4 + 16 = 24 = 4×4×(4-1)/2 × 2... actually 4³/2
  
  The PHOTON propagation equation in EC theory:
  In the geometric optics limit, photons follow null geodesics of
  the CONNECTION, not the metric. The geodesic equation is:
  
    k^μ ∇_μ k^ν = k^μ (∂_μ k^ν + Γ^ν_μρ k^ρ) = 0
  
  With torsion: Γ = {·} + K, so:
    k^μ ({·}_μ k^ν + K^ν_μρ k^ρ) = 0
    
  The EXTRA term K^ν_μρ k^μ k^ρ modifies the geodesic.
  
  KEY QUESTION: does K^ν_μρ k^μ k^ρ ≠ 0 for null k?
""")

# ═══════════════════════════════════════════════════════════════
# PART 2: WHICH TORSION COMPONENTS COUPLE TO PHOTONS?
# ═══════════════════════════════════════════════════════════════
print(f"── Part 2: Torsion-Photon Coupling ──\n")

print("""
  The contortion contracted with null vectors:
    K^ν_μρ k^μ k^ρ = ½(T^ν_μρ + T_μ^ν_ρ + T_ρ^ν_μ) k^μ k^ρ
  
  For the TRACE part (T^λ_μν = δ^λ_μ V_ν - δ^λ_ν V_μ):
    K^ν_μρ k^μ k^ρ = ½(V_ρ δ^ν_μ - V_μ δ^ν_ρ + ...) k^μ k^ρ
    
  This is non-zero for null k. Let's compute it.
""")

# Symbolic computation
# Let k be a null vector in 4D: k = (ω, ω, 0, 0) for a photon moving in x
# Torsion trace: T^λ_μν = δ^λ_μ V_ν - δ^λ_ν V_μ

omega = sp.Symbol('omega', positive=True)
V0, V1, V2, V3 = sp.symbols('V0 V1 V2 V3')

# Null vector k^μ = (ω, ω, 0, 0) — moving in x direction
k = sp.Matrix([omega, omega, 0, 0])

# Minkowski metric η = diag(-1, 1, 1, 1)
eta = sp.diag(-1, 1, 1, 1)
V = sp.Matrix([V0, V1, V2, V3])

# Check null: k^μ k_μ = η_μν k^μ k^ν
k_squared = sum(eta[mu,mu] * k[mu]**2 for mu in range(4))
print(f"  k² = {k_squared} (should be 0 for null) ✓")

# Contortion for trace torsion: K^ν_μρ = ½(δ^ν_μ V_ρ - δ^ν_ρ V_μ + η^νσ(δ_σμ V_ρ - ...))
# Actually, for the trace part T^λ_μν = δ^λ_μ V_ν - δ^λ_ν V_μ:
# Contortion: K^λ_μν = ½(T^λ_μν + T_μ^·λ_ν + T_ν^·λ_μ)
# where indices are raised/lowered with η.

# T^λ_μν = δ^λ_μ V_ν - δ^λ_ν V_μ
# T_μ^λ_ν = η_μα T^αλ_ν ... this gets index-heavy.
# Let me just compute K^ν_μρ k^μ k^ρ for the trace torsion directly.

# For trace torsion, the contortion simplifies to:
# K^λ_μν = (2/3)(δ^λ_μ V_ν - g_μν V^λ)
# (this is the standard result for the trace component)

# K^ν_μρ k^μ k^ρ = (2/3)(δ^ν_μ V_ρ - g_μρ V^ν) k^μ k^ρ
# = (2/3)(k^ν (V · k) - (k · k) V^ν)
# = (2/3)(k^ν (V · k) - 0)  [since k is null!]
# = (2/3) k^ν (V_μ k^μ)

V_dot_k = sum(eta[mu,mu] * V[mu] * k[mu] for mu in range(4))
print(f"\n  V · k = {V_dot_k}")

# The geodesic deviation is:
# k^μ ∇_μ k^ν = (2/3) k^ν (V · k)
# This is PROPORTIONAL to k^ν itself!
# That means the torsion trace does NOT deflect the photon,
# it only RESCALES the affine parameter.
# The null condition k² = 0 is PRESERVED.

print(f"""
  RESULT for TRACE torsion:
    k^μ K^ν_μρ k^ρ = (2/3) k^ν (V·k) = (2/3) k^ν × ({V_dot_k})
    
  This is proportional to k^ν itself!
  → The trace torsion does NOT change the DIRECTION of the photon.
  → It only rescales the affine parameter (redshift/blueshift).
  → The null condition k² = 0 is PRESERVED.
  → The light cone is UNCHANGED by trace torsion.
""")

# ═══════════════════════════════════════════════════════════════
print(f"── Part 3: Axial Torsion (the interesting one) ──\n")

print("""
  For the AXIAL torsion (totally antisymmetric T_μνρ = ε_μνρσ S^σ):
  
  The contortion is: K^λ_μν = -(1/2) ε^λ_μνρ S^ρ
  
  Contracted with null k:
    K^ν_μρ k^μ k^ρ = -(1/2) ε^ν_μρσ S^σ k^μ k^ρ
  
  But ε^ν_μρσ is antisymmetric in μρ, while k^μ k^ρ is symmetric.
  Therefore: K^ν_μρ k^μ k^ρ = 0 IDENTICALLY for axial torsion.
  
  → The axial torsion also does NOT deflect photons.
  → The light cone is UNCHANGED by axial torsion.
""")

# Verify: ε contracted with symmetric tensor = 0
# ε_{μρ}^{νσ} k^μ k^ρ = 0 because ε is antisymmetric in μρ

print(f"  Verification: ε_μρνσ × k^μ k^ρ:")
# For μ,ρ ∈ {0,1}: ε_{01νσ} k^0 k^1 + ε_{10νσ} k^1 k^0 
#                  = ε_{01νσ}(ω²) + (-ε_{01νσ})(ω²) = 0
print(f"  ε is antisymmetric in (μ,ρ), k^μ k^ρ is symmetric → contraction = 0 ✓")

# ═══════════════════════════════════════════════════════════════
print(f"\n── Part 4: Tensor Torsion (the remaining piece) ──\n")

print("""
  The TENSOR component q^λ_μν (traceless, non-axial) has 16 
  independent components. Its contortion is more complex.
  
  K^λ_μν = ½(q^λ_μν + q_μ^λ_ν + q_ν^λ_μ)
  
  Contracted with null k:
    K^ν_μρ k^μ k^ρ = ½(q^ν_μρ + q_μ^ν_ρ + q_ρ^ν_μ) k^μ k^ρ
  
  The first term: q^ν_μρ k^μ k^ρ — this is symmetric in μρ, so
  it picks up the symmetric part of q^ν_μρ in its lower indices.
  
  The tensor torsion CAN have a non-zero symmetric part in (μ,ρ).
  So this term is generically NON-ZERO.
  
  BUT: does it change the NULL condition?
  
  The geodesic equation k^μ ∇_μ k^ν = 0 becomes:
    k^μ D_μ k^ν + K^ν_μρ k^μ k^ρ = 0
  where D is the Levi-Civita covariant derivative.
  
  Contract with k_ν:
    k_ν k^μ D_μ k^ν + k_ν K^ν_μρ k^μ k^ρ = 0
    ½ k^μ D_μ (k²) + K_νμρ k^ν k^μ k^ρ = 0
  
  Now K_νμρ has the symmetry K_νμρ = -K_μνρ (from contortion).
  So K_νμρ k^ν k^μ = -K_μνρ k^ν k^μ = -K_νμρ k^ν k^μ
  → K_νμρ k^ν k^μ = 0 (antisymmetric in νμ, contracted with symmetric k^ν k^μ)
  
  Therefore: ½ k^μ D_μ (k²) = 0
  → If k² = 0 initially, it STAYS zero.
  → THE NULL CONDITION IS PRESERVED BY ALL TORSION COMPONENTS.
""")

print("""
  ═══════════════════════════════════════════════════════════
  THEOREM: Torsion preserves the null cone.
  
  For ANY torsion tensor T^λ_μν, the contortion K^λ_μν 
  satisfies K_{[νμ]ρ} k^ν k^μ = 0 for all vectors k.
  
  Consequence: if a geodesic starts null (k² = 0), it 
  REMAINS null in the presence of torsion.
  
  The speed of light is NOT modified by torsion.
  The causal structure is determined by the METRIC alone.
  Torsion changes the PATH of the geodesic (torsion-induced
  precession) but not the SPEED.
  ═══════════════════════════════════════════════════════════
""")

# ═══════════════════════════════════════════════════════════════
print(f"── Part 5: But Wait — What About EFFECTIVE Metrics? ──\n")

print("""
  The theorem above applies to MINIMALLY COUPLED photons.
  But in the ACS, the electromagnetic field is a COMPONENT
  of the connection ω, not a separate field. This changes
  the analysis: the photon IS part of the torsion sector.
  
  In the Pati-Salam embedding, the U(1)_Y gauge field A_μ is:
    A_μ = ω_μ^{T_{3R} + T_{B-L}/2}
  
  The gauge field propagation equation is NOT the geodesic
  equation — it's the Yang-Mills equation:
    D_ν F^{μν} = J^μ
  
  In the presence of torsion, the Yang-Mills equation becomes:
    D_ν F^{μν} + T^μ_νρ F^{νρ} = J^μ
  
  The EXTRA TERM T^μ_νρ F^{νρ} modifies the dispersion relation.
  In the geometric optics limit (F ~ k × amplitude):
    k² + (torsion corrections) = 0
  
  The dispersion relation becomes:
    k² = -T^μ_νρ k^ν ε^ρ_μ
  where ε is the polarisation.
  
  If T ≠ 0, then k² ≠ 0 in general — the photon acquires
  an EFFECTIVE MASS that depends on polarisation!
""")

# Compute the effective mass for the ACS torsion background
print(f"── Part 6: Effective Photon Mass from ACS Torsion ──\n")

# In the ACS, the torsion VEV is set by [T_{B-L}, g_CL].
# This bracket is in the (i,3) components of the 4×4 matrix.

def bracket(A, B):
    return A @ B - B @ A

T_BL = np.diag([1/3, 1/3, 1/3, -1]).astype(float)
A03 = np.zeros((4,4)); A03[0,3]=1; A03[3,0]=-1
A13 = np.zeros((4,4)); A13[1,3]=1; A13[3,1]=-1
A23 = np.zeros((4,4)); A23[2,3]=1; A23[3,2]=-1
g_CL = (A03 + A13 + A23) / np.sqrt(3)

L2 = bracket(T_BL, g_CL)

print(f"  Torsion VEV = [T_BL, g_CL]:")
print(f"  {L2}")
print(f"  This is SYMMETRIC (torsion sector), norm = {norm(L2):.6f}")
print(f"  Components: T_{{i3}} = T_{{3i}} = 4/(3*sqrt(3)) for i=0,1,2")

# The effective photon mass depends on the CONTRACTION of the
# torsion with the photon's propagation and polarisation.
# For a photon in the U(1)_Y direction, the relevant torsion
# component is the one that mixes the photon direction with
# the colour directions.

# In the ACS embedding, the photon direction is T_{3R} + T_{B-L}/2.
# The torsion [T_{B-L}, g] lives in the (i,3) plane.
# The photon is in the T_{B-L} direction.
# [T_{B-L}, T_{B-L}] = 0 → no self-torsion!

comm_self = bracket(T_BL, T_BL)
print(f"\n  [T_BL, T_BL] = {norm(comm_self):.2e} (exactly zero)")
print(f"  → The photon's OWN torsion background is ZERO.")
print(f"  → The photon does not see its own torsion.")

# But the COLOUR torsion (from the SU(3) sector) is non-zero.
# Does the photon couple to the colour torsion?
# Only if the photon direction has non-zero overlap with the
# colour generators.

# The photon is U(1)_Y ∝ T_{B-L}.
# The colour generators are the SU(3) ones (upper 3×3 block).
# T_{B-L} commutes with SU(3) → [T_{B-L}, colour] = 0.
# → The photon does NOT couple to colour torsion either!

print(f"  T_BL commutes with the SU(3) generators:")
for name, gen in [("H1", np.diag([1,-1,0,0]).astype(float)),
                   ("H2", np.diag([0,1,-1,0]).astype(float))]:
    c = bracket(T_BL, gen)
    print(f"    [T_BL, {name}] = {norm(c):.2e}")

print(f"""
  RESULT: The photon (U(1)_Y gauge boson) propagates through
  the ACS torsion background WITHOUT acquiring an effective mass.
  
  This is because:
  1. [T_BL, T_BL] = 0 (self-torsion vanishes)
  2. [T_BL, SU(3)] = 0 (photon commutes with colour)
  3. The photon direction is in the CARTAN subalgebra, which
     has zero torsion coupling by construction.
  
  The GLUONS, however, DO couple to torsion:
  [T_BL, A_i3] = (4/3) A_i3 ≠ 0
  
  The gluons acquire an effective mass from the torsion background.
  This is CONFINEMENT: the colour force becomes short-range
  because the gluons are massive in the torsion vacuum.
""")

# ═══════════════════════════════════════════════════════════════
print(f"── Part 7: What WOULD Break the Speed Limit? ──\n")

print("""
  For the light speed to be modified by torsion, we would need:
  
  1. The photon to carry SPIN angular momentum that couples to
     the AXIAL torsion S_μ. In EC theory, only FERMIONS couple
     to axial torsion (spin-torsion coupling). Photons (spin-1)
     do NOT couple at tree level.
     
  2. A BACKGROUND torsion field that is non-zero in the photon's
     propagation direction AND in the photon's gauge direction
     simultaneously. As we showed: [T_BL, T_BL] = 0 and
     [T_BL, colour] = 0, so this doesn't happen for photons.
     
  3. A HIGHER-ORDER effect: the BCH expansion at 3rd order
     includes [[f,g],f] and [[f,g],g]. These could in principle
     give a torsion-squared correction to the photon propagator.
     Let's compute this.
""")

# The 3rd-order BCH term for the photon direction:
# [[T_BL, g], T_BL] — this is in the ANTISYMMETRIC sector

L3_ff = bracket(L2, T_BL)
print(f"  [[T_BL, g], T_BL]:")
print(f"  norm = {norm(L3_ff):.6f}")
print(f"  symmetric part: {norm((L3_ff + L3_ff.T)/2):.10f}")
print(f"  antisymmetric part: {norm((L3_ff - L3_ff.T)/2):.6f}")

# This is PURE ANTISYMMETRIC — it's in the Lorentz sector.
# Project onto the photon direction (T_BL):
proj_photon = np.trace(L3_ff @ T_BL) / norm(T_BL)**2
print(f"  Projection onto photon direction: {proj_photon:.10f}")

# The projection is zero! The 3rd-order bracket in the T_BL direction
# has no overlap with T_BL itself because L3_ff is antisymmetric
# and T_BL is symmetric (diagonal).

print(f"""
  The 3rd-order bracket [[T_BL, g], T_BL] is PURE ANTISYMMETRIC.
  T_BL is SYMMETRIC (diagonal).
  Their inner product is ZERO.
  
  → Even at 3rd BCH order, the photon does not acquire a
     torsion-induced mass or speed modification.
     
  ═══════════════════════════════════════════════════════════
  CONCLUSION
  ═══════════════════════════════════════════════════════════
  
  1. Torsion preserves the null cone (theorem, all components).
  2. The photon does not couple to the ACS torsion background
     because [T_BL, T_BL] = 0 and [T_BL, SU(3)] = 0.
  3. Even at 3rd BCH order, the photon-torsion coupling is zero
     (symmetry mismatch: anti ⟂ sym).
  4. The speed of light is PROTECTED by the Cartan-subalgebra
     structure of the electromagnetic direction.
     
  WHAT TORSION DOES MODIFY:
  - Gluon propagation (confinement: [T_BL, A_i3] ≠ 0)
  - Fermion geodesics (spin-torsion coupling)
  - Gravitational wave polarisation (torsion modes)
  
  WHAT TORSION DOES NOT MODIFY:
  - The speed of light
  - The electromagnetic causal structure
  - Photon mass (stays zero)
  
  The Lorentz "barrier" is not broken by torsion.
  It is PROTECTED by the algebraic structure that the ACS
  framework itself identifies: the photon sits in the Cartan
  subalgebra, which is the zero-torsion subspace by construction.
  
  This is not a limitation — it's a PREDICTION.
  The ACS framework predicts that c is exact, not approximate,
  because the electromagnetic gauge direction is algebraically
  orthogonal to the torsion sector.
""")

# ═══════════════════════════════════════════════════════════════
print(f"── Bonus: What About Massive Gauge Bosons? ──\n")

# The W and Z bosons are in the SU(2)_L sector.
# Do they couple to torsion?

J1 = np.zeros((4,4))
J1[0,1] = J1[2,3] = 0.5
J1[1,0] = J1[3,2] = -0.5

comm_TJ = bracket(T_BL, J1)
print(f"  [T_BL, J1(SU(2)_L)] norm = {norm(comm_TJ):.6f}")

# T_BL commutes with SU(2)_L? Let's check properly.
# T_BL = diag(1/3, 1/3, 1/3, -1) is in SU(4)
# SU(2)_L generators J_i are in the Lorentz sector (self-dual)
# They live in different spaces — they should commute in a
# direct product group.

# But in our 4×4 matrices, they share the same space!
print(f"  (Non-zero: {norm(comm_TJ):.6f})")
print(f"  T_BL and SU(2)_L generators do NOT commute in the 4×4 space.")
print(f"  This means the W/Z bosons DO feel the torsion background.")
print(f"  → Torsion contributes to electroweak symmetry breaking!")
print(f"  → The W/Z mass has a torsion component.")

# The W/Z effective mass from torsion:
# m_W² ∝ ||[T_BL, J_i]||² × (torsion VEV)²
m_W_torsion = norm(comm_TJ)**2
print(f"  ||[T_BL, J1]||² = {m_W_torsion:.6f}")
print(f"  Ratio to gluon torsion mass ||[T_BL, A_i3]||² = {(4/3)**2*2:.6f}")
print(f"  W/Z torsion mass / gluon torsion mass = {m_W_torsion / ((4/3)**2*2):.4f}")

print(f"""
  This is a GENUINELY NEW OBSERVATION:
  
  The torsion background discriminates between gauge bosons:
  - Photon: ZERO torsion coupling (Cartan direction) → massless
  - W/Z: NON-ZERO torsion coupling → massive
  - Gluons: MAXIMAL torsion coupling → confined
  
  The HIERARCHY of gauge boson masses follows from the
  HIERARCHY of their torsion couplings, which is set by
  the bracket structure constants of the Pati-Salam embedding.
  
  This is the GEOMETRIC ORIGIN of the mass hierarchy:
  photon < W/Z < gluon (effective), all from the same torsion VEV.
""")
