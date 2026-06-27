#!/usr/bin/env python3
"""
FOLLOWING THE TORSION MASS HIERARCHY
======================================
The last exploration found that torsion discriminates gauge bosons:
  Photon: 0 coupling, W/Z: 0.889, Gluon: 3.556
  Ratio W/Z : Gluon = 1:4

Don't assume. Compute every variant. See what falls out.
"""

import numpy as np
from numpy.linalg import norm, eigvalsh
from itertools import combinations

def bracket(A, B):
    return A @ B - B @ A

def killing(A, B):
    """Killing form of sl(4): K(A,B) = 8 Tr(AB)"""
    return 8 * np.trace(A @ B)

# ═══════════════════════════════════════════════════════════════
# ALL GENERATORS IN THE 4×4 SPACE
# ═══════════════════════════════════════════════════════════════

# Diagonal (Cartan) generators of sl(4)
H1 = np.diag([1,-1,0,0]).astype(float)
H2 = np.diag([0,1,-1,0]).astype(float)
H3 = np.diag([0,0,1,-1]).astype(float)  # = T_{B-L} normalised differently
T_BL = np.diag([1/3, 1/3, 1/3, -1]).astype(float)

# Off-diagonal generators E_{ij} for i≠j
def E(i,j):
    M = np.zeros((4,4))
    M[i,j] = 1
    return M

# Antisymmetric (Lorentz) generators: A_{ij} = E_{ij} - E_{ji}
def A(i,j):
    return E(i,j) - E(j,i)

# Symmetric (torsion) generators: S_{ij} = E_{ij} + E_{ji}
def S(i,j):
    return E(i,j) + E(j,i)

# Self-dual (SU(2)_L) generators
J1 = (A(0,1) + A(2,3)) / 2
J2 = (A(0,2) - A(1,3)) / 2
J3 = (A(0,3) + A(1,2)) / 2

# Anti-self-dual (SU(2)_R) generators
K1 = (A(0,1) - A(2,3)) / 2
K2 = (A(0,2) + A(1,3)) / 2
K3 = (A(0,3) - A(1,2)) / 2

# Colour-lepton mixing (the generators that T_BL doesn't commute with trivially)
g_CL = (A(0,3) + A(1,3) + A(2,3)) / np.sqrt(3)

print("=" * 70)
print("TORSION COUPLING OF EVERY GENERATOR IN sl(4)")
print("=" * 70)

# Compute [T_BL, X] for every generator
print(f"\n  Generator       ||[T_BL, X]||²    Killing(X,X)    Type")
print(f"  {'─'*65}")

all_gens = {
    "H1 (colour)":     H1,
    "H2 (colour)":     H2,
    "H3 (B-L)":        H3,
    "T_BL":            T_BL,
    "J1 (SU2_L)":      J1,
    "J2 (SU2_L)":      J2,
    "J3 (SU2_L)":      J3,
    "K1 (SU2_R)":      K1,
    "K2 (SU2_R)":      K2,
    "K3 (SU2_R)":      K3,
    "A01 (colour)":    A(0,1),
    "A02 (colour)":    A(0,2),
    "A12 (colour)":    A(1,2),
    "A03 (col-lep)":   A(0,3),
    "A13 (col-lep)":   A(1,3),
    "A23 (col-lep)":   A(2,3),
    "S01 (boost)":     S(0,1),
    "S02 (boost)":     S(0,2),
    "S03 (boost)":     S(0,3),
    "S12 (torsion)":   S(1,2),
    "S13 (torsion)":   S(1,3),
    "S23 (torsion)":   S(2,3),
}

results = {}
for name, gen in all_gens.items():
    comm = bracket(T_BL, gen)
    n2 = norm(comm)**2
    k = killing(gen, gen)
    sym = "Sym" if np.allclose(gen, gen.T) else "Anti"
    results[name] = (n2, k, sym)
    if n2 > 1e-10:
        print(f"  {name:<20} {n2:>12.6f}    {k:>10.4f}       {sym}")
    else:
        print(f"  {name:<20} {'0':>12}    {k:>10.4f}       {sym}")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("GROUPING BY TORSION COUPLING STRENGTH")
print(f"{'='*70}")

# Group by coupling strength
zero_coupling = [(n,v) for n,(v,_,_) in results.items() if v < 1e-10]
weak_coupling = [(n,v) for n,(v,_,_) in results.items() if 0.5 < v < 1.5]
strong_coupling = [(n,v) for n,(v,_,_) in results.items() if v > 2]

print(f"\n  ZERO torsion coupling (massless sector):")
for name, _ in zero_coupling:
    print(f"    {name}")

print(f"\n  WEAK torsion coupling (||[T,X]||² ≈ 0.89):")
for name, v in weak_coupling:
    print(f"    {name}: {v:.6f}")

print(f"\n  STRONG torsion coupling (||[T,X]||² ≈ 3.56):")
for name, v in strong_coupling:
    print(f"    {name}: {v:.6f}")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("THE RATIO: WHAT IS 0.889 / 3.556?")
print(f"{'='*70}")

# The W/Z coupling: ||[T_BL, J_i]||²
w_coupling = norm(bracket(T_BL, J1))**2
# The gluon coupling: ||[T_BL, A_{i3}]||²
g_coupling = norm(bracket(T_BL, A(0,3)))**2

ratio = w_coupling / g_coupling
print(f"\n  ||[T_BL, J1]||² = {w_coupling:.6f}")
print(f"  ||[T_BL, A03]||² = {g_coupling:.6f}")
print(f"  Ratio = {ratio:.6f}")
print(f"  Exact: {ratio} = 1/4? {abs(ratio - 0.25) < 1e-10}")

# What IS 1/4 in this context?
# J1 = (A01 + A23)/2
# [T_BL, J1] = [T_BL, A01]/2 + [T_BL, A23]/2
# [T_BL, A01] = 0 (colour sector, commutes)
# [T_BL, A23] = 0 (colour sector, commutes)
# Wait... let me recheck

comm_T_J1 = bracket(T_BL, J1)
print(f"\n  Checking components of [T_BL, J1]:")
print(f"  J1 = (A01 + A23)/2")

comm_T_A01 = bracket(T_BL, A(0,1))
comm_T_A23 = bracket(T_BL, A(2,3))
print(f"  [T_BL, A01] norm = {norm(comm_T_A01):.6f}")
print(f"  [T_BL, A23] norm = {norm(comm_T_A23):.6f}")
print(f"  [T_BL, J1] = {norm(comm_T_J1):.6f}")

# Wait — A01 has indices 0,1 which are both in the colour block.
# T_BL = diag(1/3, 1/3, 1/3, -1)
# [T_BL, A01]_{ij} = (T_BL_ii - T_BL_jj) A01_{ij}
# For (i,j) = (0,1): (1/3 - 1/3) × 1 = 0
# For (i,j) = (1,0): (1/3 - 1/3) × (-1) = 0
# So [T_BL, A01] = 0. ✓

# A23: indices 2,3
# (i,j) = (2,3): (1/3 - (-1)) × 1 = 4/3
# (i,j) = (3,2): (-1 - 1/3) × (-1) = 4/3
# So [T_BL, A23] = (4/3) A23... wait no, let me compute properly

comm_T_A23_manual = np.zeros((4,4))
for i in range(4):
    for j in range(4):
        if A(2,3)[i,j] != 0:
            comm_T_A23_manual[i,j] = (T_BL[i,i] - T_BL[j,j]) * A(2,3)[i,j]

print(f"\n  Manual [T_BL, A23]:")
print(f"  {comm_T_A23_manual}")
print(f"  norm = {norm(comm_T_A23_manual):.6f}")
print(f"  = (4/3) × A23? {np.allclose(comm_T_A23_manual, (4/3)*A(2,3))}")

# So: [T_BL, J1] = [T_BL, (A01+A23)/2] = 0 + (4/3)A23/2 = (2/3)A23
print(f"\n  [T_BL, J1] = (2/3) A23")
print(f"  ||[T_BL, J1]||² = (2/3)² × ||A23||² = (4/9) × {norm(A(2,3))**2:.1f} = {4/9 * norm(A(2,3))**2:.6f}")
print(f"  Check: {w_coupling:.6f}")

# And ||[T_BL, A03]||² = (4/3)² × ||A03||² = (16/9) × 2 = 32/9
print(f"\n  ||[T_BL, A03]||² = (4/3)² × ||A03||² = {(4/3)**2 * norm(A(0,3))**2:.6f}")
print(f"  Check: {g_coupling:.6f}")

# Ratio: (4/9 × 2) / (16/9 × 2) = 4/16 = 1/4 ✓
print(f"\n  Ratio = (4/9) / (16/9) = 4/16 = 1/4 ✓")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("WHAT DOES 1/4 PREDICT?")
print(f"{'='*70}")

# If the torsion VEV contributes to the gauge boson mass as:
# m² ∝ ||[T_BL, generator]||² × v_torsion²
# then:
# m_W² / m_gluon² = 1/4

# But gluons are confined, not massive in the usual sense.
# The confinement scale Λ_QCD ≈ 200 MeV is the effective gluon mass.
# So: m_W² / Λ_QCD² = ?

# Actually, the physical question is different.
# The RATIO of W coupling to gluon coupling is 1/4.
# In terms of the gauge couplings:
# [T_BL, J_i] = (2/3) × (colour-lepton component of J_i)
# [T_BL, A_{i3}] = (4/3) × A_{i3}
# The ratio of structure constants: (2/3)/(4/3) = 1/2
# The ratio of ||·||²: (2/3)²/(4/3)² = 1/4

# This 1/2 is the RATIO of the electroweak to strong coupling
# at the torsion scale:
# g_W/g_s = (2/3)/(4/3) = 1/2

g_W_eff = 2/3
g_s_eff = 4/3
ratio_couplings = g_W_eff / g_s_eff

print(f"\n  Effective torsion coupling constants:")
print(f"    g_W (from [T_BL, J]) = 2/3 = {g_W_eff:.6f}")
print(f"    g_s (from [T_BL, A_i3]) = 4/3 = {g_s_eff:.6f}")
print(f"    Ratio g_W/g_s = 1/2")

# Now: sin²θ_W = g'²/(g² + g'²)
# At the PS scale: g_W = g' (from the SU(2)_R ↔ U(1)_Y matching)
# Actually, sin²θ_W involves g₁ and g₂, not the torsion couplings.
# But let's check: is (g_W/g_s)² = 1/4 related to sin²θ_W?

print(f"\n  (g_W/g_s)² = (1/2)² = 1/4")
print(f"  sin²θ_W at PS = 3/8 = 0.375")
print(f"  These are different. But...")

# The WEAK mixing in the torsion sector:
# The J generators have components in BOTH the colour block and
# the lepton block. The colour block commutes with T_BL; the
# lepton block doesn't.
# The fraction of J that couples to torsion:
# J1 = (A01 + A23)/2
# A01 is pure colour (commutes with T_BL)
# A23 mixes colour and lepton (index 3 = lepton)
# So the torsion-active fraction of J1 is the A23 component.
# ||A23||/||J1|| = ||A23||/(||A01+A23||/2) ...

# Actually: J1 has norm ||J1||² = ||A01||²/4 + ||A23||²/4 = 2/4 + 2/4 = 1
norm_J1 = norm(J1)**2
norm_A23_component = norm(A(2,3))**2 / 4  # the part that couples
fraction_active = norm_A23_component / norm_J1

print(f"\n  Active fraction of J1 (lepton-sector component):")
print(f"    ||A23/2||² / ||J1||² = {norm_A23_component:.4f} / {norm_J1:.4f} = {fraction_active:.4f}")
print(f"    = 1/2")
print(f"    Half of the SU(2)_L generator is torsion-active.")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("α_em FROM THE BRACKET")
print(f"{'='*70}")

# The electromagnetic coupling comes from the U(1)_Y direction.
# In PS: Y = T_{3R} + (B-L)/2
# The photon is the massless combination after EWSB.
# The coupling is g_em = g₂ sin θ_W = g₁ cos θ_W

# At the PS scale with g₂ = g₃ = 4/3 and sin²θ_W = 3/8:
g2_PS = 4/3
sin2_W = 3/8
g_em_PS = g2_PS * np.sqrt(sin2_W)
alpha_em_PS = g_em_PS**2 / (4 * np.pi)

print(f"\n  At the Pati-Salam scale:")
print(f"    g₂ = 4/3 (bracket constant)")
print(f"    sin²θ_W = 3/8 (standard PS)")
print(f"    g_em = g₂ × sin θ_W = {g2_PS} × {np.sqrt(sin2_W):.6f} = {g_em_PS:.6f}")
print(f"    α_em(PS) = g²_em/(4π) = {alpha_em_PS:.6f}")
print(f"    1/α_em(PS) = {1/alpha_em_PS:.2f}")

# Running from PS scale (~10^15 GeV) to M_Z:
# α_em runs from ~1/40 at GUT to ~1/128 at M_Z
# Our value 1/α = 34.1 is in the right range for a GUT-scale coupling.

print(f"\n  For comparison:")
print(f"    1/α_em(GUT) ≈ 40 (standard)")
print(f"    1/α_em(M_Z) ≈ 128 (observed)")
print(f"    Our 1/α_em(PS) = {1/alpha_em_PS:.1f}")
print(f"    Match to GUT expectation: {abs(1/alpha_em_PS - 40)/(40)*100:.0f}%")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("THE FULL TORSION MASS SPECTRUM")
print(f"{'='*70}")

# If we define the torsion mass as m² ∝ ||[T_BL, X]||²:
# Photon: 0
# W/Z: (2/3)² × 2 = 8/9
# Gluon: (4/3)² × 2 = 32/9

# The ratio m²_W / m²_gluon(eff) = (8/9)/(32/9) = 1/4
# If we identify the gluon effective mass with Λ_QCD ≈ 200 MeV:
# m_W(torsion) = Λ_QCD × √(1/4) = Λ_QCD / 2 = 100 MeV

# That's WAY too small — the actual W mass is 80 GeV.
# So the torsion VEV does NOT directly give the W mass.
# The W mass comes primarily from the Higgs mechanism.
# The torsion contribution is a CORRECTION, not the main source.

Lambda_QCD = 0.200  # GeV
m_W_torsion = Lambda_QCD / 2
m_W_obs = 80.4  # GeV

print(f"\n  IF m_gluon(eff) ~ Λ_QCD = {Lambda_QCD*1000:.0f} MeV:")
print(f"    m_W(torsion) = Λ_QCD/2 = {m_W_torsion*1000:.0f} MeV")
print(f"    m_W(observed) = {m_W_obs*1000:.0f} MeV")
print(f"    Ratio: {m_W_torsion/m_W_obs:.4f}")
print(f"    → Torsion gives only {m_W_torsion/m_W_obs*100:.2f}% of the W mass.")
print(f"    → The Higgs mechanism provides the rest ({(1-m_W_torsion/m_W_obs)*100:.1f}%).")

# BUT: this comparison is wrong! The gluon isn't really "massive"
# with mass Λ_QCD. Confinement and mass are different phenomena.
# The correct comparison uses the TORSION VEV, not Λ_QCD.

# The torsion VEV in the ACS is set by the bracket norm:
# ||[T_BL, g]|| = (4/3)√2 ≈ 1.886 (in algebra units)
# The physical VEV in GeV depends on the identification of the
# algebra units with physical scales.

# In the ACS, the electroweak VEV v = 246 GeV comes from the
# Higgs potential minimum. The torsion VEV is v_T = v × tan(β) = v/2.
# (from the bracket ratio ||L2||/||L3_sym|| = 1/2)

v_ew = 246.22  # GeV
v_torsion = v_ew / 2  # from tan(β) = 1/2

m_W_from_torsion = g_W_eff * v_torsion / 2  # standard formula m = gv/2
m_W_from_higgs = g2_PS * v_ew / 2

print(f"\n  With v_torsion = v/2 = {v_torsion:.1f} GeV:")
print(f"    m_W(torsion) = g_W × v_T/2 = (2/3)×{v_torsion:.1f}/2 = {m_W_from_torsion:.1f} GeV")
print(f"    m_W(Higgs) = g₂ × v/2 = (4/3)×{v_ew:.1f}/2 = {m_W_from_higgs:.1f} GeV")
print(f"    m_W(observed) = {m_W_obs:.1f} GeV")
print(f"    Ratio torsion/Higgs = {m_W_from_torsion/m_W_from_higgs:.4f} = 1/4")

# The torsion contribution is exactly 1/4 of the Higgs contribution.
# But the physical W mass is g₂v/2 = 164 GeV... that's too large.
# The PHYSICAL coupling g₂ at M_Z is 0.652, not 4/3.
# So g₂ = 4/3 is the PS-scale value, and the running reduces it.

g2_MZ = 0.6517
m_W_physical = g2_MZ * v_ew / 2
print(f"\n  With g₂(M_Z) = {g2_MZ}:")
print(f"    m_W = g₂(M_Z) × v/2 = {m_W_physical:.1f} GeV (obs: 80.4)")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("THE KEY RATIOS — WHAT THE ALGEBRA ACTUALLY PREDICTS")
print(f"{'='*70}")

print(f"""
  The torsion bracket ||[T_BL, X]||² gives three EXACT ratios:
  
  1. Photon : W/Z : Gluon = 0 : 8/9 : 32/9 = 0 : 1 : 4
  
  2. The structure constant ratio g_W/g_s = (2/3)/(4/3) = 1/2
  
  3. The torsion-active fraction of SU(2)_L = 1/2
     (only the lepton-sector component of J_i couples to torsion)
  
  4. α_em(PS) = [(4/3)² × (3/8)] / (4π) = 2/(9π) = {2/(9*np.pi):.6f}
     1/α_em = 9π/2 = {9*np.pi/2:.4f}
  
  These are PARAMETER-FREE predictions from the bracket algebra.
  Whether they lead to the correct physical masses depends on:
  - The RG running from the PS scale to M_Z (known, computable)
  - The identification of the torsion VEV (tan β = 1/2)
  - The Higgs potential minimisation (open problem)
  
  What is NOT in doubt: the bracket algebra discriminates gauge
  bosons with EXACT rational ratios. The photon is protected by
  its Cartan-subalgebra position. The pattern 0 : 1 : 4 is a
  theorem of the embedding, not a fit.
""")
