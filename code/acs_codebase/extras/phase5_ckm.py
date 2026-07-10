#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
PHASE 5: CKM FROM BI-DOUBLET MISALIGNMENT
===========================================
The Phase 4 negative result showed: if both up and down mass matrices
have the SAME texture, V_CKM = identity.

The fix: in Pati-Salam, the bi-doublet Φ = (1,2,2) has TWO independent 
Yukawa couplings h and h̃, corresponding to Φ and Φ̃ = τ₂Φ*τ₂.

  M_u = h κ₁ + h̃ κ₂    (up-type mass matrix)
  M_d = h κ₂ + h̃ κ₁    (down-type mass matrix)

The KEY: in the ACS bracket structure,
  h  comes from the SYMMETRIC part of [T_{B-L}, g] → SYMMETRIC in gen space
  h̃ comes from the ANTISYMMETRIC part                → ANTISYMMETRIC in gen space

Because h is symmetric and h̃ is antisymmetric, M_u and M_d are 
DIFFERENT non-symmetric matrices. Their SVD diagonalisations differ,
generating CKM mixing.
"""

import numpy as np
from numpy.linalg import norm, svd, det
from scipy.optimize import minimize

def bracket(A, B):
    return A @ B - B @ A

print("=" * 70)
print("PHASE 5: CKM FROM BI-DOUBLET MISALIGNMENT")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# Physical constants
v = 246.22  # Higgs VEV, GeV
eps = 0.22650  # Wolfenstein parameter = BCH coupling

# tan(β) from bracket norms (proved in Phase 4)
tan_beta = 0.5
sin_beta = tan_beta / np.sqrt(1 + tan_beta**2)  # = 1/√5
cos_beta = 1 / np.sqrt(1 + tan_beta**2)         # = 2/√5

kappa1 = v * sin_beta  # up-type VEV
kappa2 = v * cos_beta  # down-type VEV

print(f"\n  tan(β) = {tan_beta} (from bracket norms)")
print(f"  κ₁ = v sin β = {kappa1:.2f} GeV (up-type)")
print(f"  κ₂ = v cos β = {kappa2:.2f} GeV (down-type)")

# ═══════════════════════════════════════════════════════════════
# Step 1: Build h (symmetric) and h̃ (antisymmetric) in generation space
# ═══════════════════════════════════════════════════════════════
print(f"\n── Step 1: Yukawa Matrices h and h̃ ──\n")

# The symmetric Yukawa h comes from the torsion bracket [T_{B-L}, g].
# Its generation-space structure is HIERARCHICAL:
#   h_{33} ~ 1 (heaviest generation, 1st BCH order)
#   h_{22} ~ ε² (2nd generation, 2nd BCH order) 
#   h_{11} ~ ε⁴ (lightest, 3rd BCH order)
#   h_{ij} ~ ε^{|i-j|} × geometric mean (off-diagonal, cross-brackets)
#
# The normalisation is set by m_t = h_{33} × κ₁ for the top quark.

# Physical quark masses at 2 GeV (MeV) for normalisation
m_t = 172500  # MeV
m_c = 1270
m_u_phys = 2.16
m_b = 4180
m_s = 93.4
m_d_phys = 4.67

# h is symmetric, entries ~ √(m_i m_j) / v_u (Fritzsch-like)
# But we use the BCH suppression: h_{ij} = h₀ × ε^{(3-i)+(3-j)} / ((3-i)!(3-j)!)
# Simplified: the EIGENVALUES of h are the up-type Yukawas y_u, y_c, y_t
# and the EIGENVECTORS are close to the identity (nearly diagonal).

# For the symmetric Yukawa, the BEST texture is nearest-neighbour:
# h = [[0, A_12, 0], [A_12, 0, A_23], [0, A_23, h_33]]
# with A_12 = √(m_1 m_2)/κ₁, A_23 = √(m_2 m_3)/κ₁, h_33 = m_3/κ₁

# But we DON'T know which masses to use for h (the Yukawa coupling),
# since the PHYSICAL masses involve both h and h̃.
# Instead, use the bracket norms to set the RELATIVE entries.

# The bracket structure gives:
# h₃₃ : h₂₂ : h₁₁ = 1 : ε² : ε⁴
# h₂₃ = h₃₂ : h₁₂ = h₂₁ = √(h₂₂ h₃₃) : √(h₁₁ h₂₂)
#            = ε : ε³
# h₁₃ = 0 (non-adjacent BCH orders, nearest-neighbour only)

h33 = 1.0
h22 = eps**2
h11 = eps**4
h23 = np.sqrt(h22 * h33)  # = ε
h12 = np.sqrt(h11 * h22)  # = ε³
h13 = 0  # nearest-neighbour

h = np.array([
    [h11,  h12,  h13],
    [h12,  h22,  h23],
    [h13,  h23,  h33]
])

# The antisymmetric Yukawa h̃ comes from the gauge bracket [[f,g],f].
# It is ANTISYMMETRIC in generation space (zero diagonal).
# Its norm relative to h is set by the bracket ratio:
# ||L3_anti|| / ||L3_sym|| = ||[[f,g],f]|| / ||[[f,g],g]||

T_BL = np.diag([1/3, 1/3, 1/3, -1]).astype(float)
A03 = np.zeros((4,4)); A03[0,3]=1; A03[3,0]=-1
A13_g = np.zeros((4,4)); A13_g[1,3]=1; A13_g[3,1]=-1
A23_g = np.zeros((4,4)); A23_g[2,3]=1; A23_g[3,2]=-1
g_CL = (A03 + A13_g + A23_g) / np.sqrt(3)

L2 = bracket(T_BL, g_CL)
L3_anti = bracket(L2, T_BL)
L3_sym = bracket(L2, g_CL)

r_anti_sym = norm(L3_anti) / norm(L3_sym)
print(f"  ||L3_anti||/||L3_sym|| = {r_anti_sym:.6f}")
print(f"  This ratio scales the antisymmetric Yukawa relative to h.")

# h̃ entries: antisymmetric, with the same BCH order suppression
# h̃_{23} = -h̃_{32} = r × ε (same order as h_{23})
# h̃_{12} = -h̃_{21} = r × ε³
# h̃_{13} = -h̃_{31} = r × ε² (this one is NOT zero! 
#   The antisymmetric coupling between non-adjacent orders exists
#   because the GAUGE bracket has different selection rules.)

ht23 = r_anti_sym * eps      # scaled by bracket ratio
ht12 = r_anti_sym * eps**3
ht13 = r_anti_sym * eps**2   # non-zero for antisymmetric!

h_tilde = np.array([
    [0,      ht12,   ht13],
    [-ht12,  0,      ht23],
    [-ht13,  -ht23,  0]
])

print(f"\n  Symmetric Yukawa h:")
for row in h:
    print(f"    [{row[0]:10.6f} {row[1]:10.6f} {row[2]:10.6f}]")

print(f"\n  Antisymmetric Yukawa h̃:")
for row in h_tilde:
    print(f"    [{row[0]:10.6f} {row[1]:10.6f} {row[2]:10.6f}]")

# ═══════════════════════════════════════════════════════════════
# Step 2: Mass matrices M_u = h κ₁ + h̃ κ₂, M_d = h κ₂ + h̃ κ₁
# ═══════════════════════════════════════════════════════════════
print(f"\n── Step 2: Mass Matrices ──\n")

# Include the CP phase α in the down-type VEV
# ⟨Φ⟩ = diag(κ₁, κ₂ e^{iα})
# For now, scan α to find best fit

def compute_ckm_bidoublet(alpha_phase):
    """Compute CKM for given CP phase α in the bi-doublet VEV."""
    k1 = kappa1
    k2 = kappa2 * np.exp(1j * alpha_phase)
    
    M_u = h * k1 + h_tilde * k2
    M_d = h * k2 + h_tilde * k1
    
    # Normalise: scale so that largest singular value of M_u = m_t
    U_u, s_u, Vh_u = svd(M_u)
    scale_u = m_t / (s_u[-1] * 1000)  # convert to GeV in output
    M_u_scaled = M_u * (m_t / s_u[-1])
    
    U_d, s_d, Vh_d = svd(M_d)
    # Scale M_d so that largest singular value = m_b
    M_d_scaled = M_d * (m_b / s_d[-1])
    
    # Re-SVD the scaled matrices
    U_u, s_u, Vh_u = svd(M_u_scaled)
    U_d, s_d, Vh_d = svd(M_d_scaled)
    
    # CKM = V_uL† V_dL (left-handed rotations from SVD)
    V_ckm = U_u.conj().T @ U_d
    
    return V_ckm, sorted(s_u), sorted(s_d)

# Scan α
print(f"  Scanning CP phase α...")
best_chi2 = 1e10
best_alpha = 0

V_obs_dict = {(0,1): 0.2250, (1,2): 0.04182, (0,2): 0.00369}

for alpha in np.linspace(0, 2*np.pi, 1000):
    try:
        V, mu, md = compute_ckm_bidoublet(alpha)
    except:
        continue
    
    chi2 = sum((abs(V[i,j]) - val)**2 / val**2 for (i,j), val in V_obs_dict.items())
    
    if chi2 < best_chi2:
        best_chi2 = chi2
        best_alpha = alpha

print(f"  Best α = {np.degrees(best_alpha):.1f}°")
print(f"  χ² = {best_chi2:.6f}")

V_best, mu_best, md_best = compute_ckm_bidoublet(best_alpha)

print(f"\n  |V_CKM| at α = {np.degrees(best_alpha):.1f}°:")
print(f"  {'':>8} {'d':>10} {'s':>10} {'b':>10}")
labels = ['u', 'c', 't']
for i in range(3):
    print(f"  {labels[i]:>8} {abs(V_best[i,0]):>10.5f} {abs(V_best[i,1]):>10.5f} {abs(V_best[i,2]):>10.5f}")

print(f"\n  Observed (PDG 2024):")
print(f"  {'':>8} {'d':>10} {'s':>10} {'b':>10}")
V_pdg = [[0.97435, 0.22500, 0.00369],
         [0.22486, 0.97349, 0.04182],
         [0.00857, 0.04110, 0.99912]]
for i, lab in enumerate(labels):
    print(f"  {lab:>8} {V_pdg[i][0]:>10.5f} {V_pdg[i][1]:>10.5f} {V_pdg[i][2]:>10.5f}")

V_us = abs(V_best[0,1])
V_cb = abs(V_best[1,2])
V_ub = abs(V_best[0,2])

print(f"\n  Wolfenstein parameters:")
print(f"    |V_us| = {V_us:.4f} (obs: 0.2250, {abs(V_us-0.225)/0.225*100:.1f}%)")
print(f"    |V_cb| = {V_cb:.5f} (obs: 0.04182, {abs(V_cb-0.04182)/0.04182*100:.1f}%)")
print(f"    |V_ub| = {V_ub:.6f} (obs: 0.00369, {abs(V_ub-0.00369)/0.00369*100:.1f}%)")

# Jarlskog invariant
J = np.imag(V_best[0,1] * V_best[1,2] * np.conj(V_best[0,2]) * np.conj(V_best[1,1]))
print(f"    J = {J:.2e} (obs: 3.08e-5)")

# Mass eigenvalues
print(f"\n  Mass eigenvalues:")
print(f"    Up: {mu_best[0]:.2f}, {mu_best[1]:.1f}, {mu_best[2]:.0f} MeV")
print(f"    Down: {md_best[0]:.2f}, {md_best[1]:.1f}, {md_best[2]:.0f} MeV")

# ═══════════════════════════════════════════════════════════════
# Step 3: Try with the antisymmetric coupling ENHANCED
# ═══════════════════════════════════════════════════════════════
print(f"\n── Step 3: Scan over h̃/h ratio ──\n")

# The ratio r_anti_sym = 2/3 from the bracket norms.
# But the EFFECTIVE ratio in the Yukawa sector might be different
# due to the SU(2)_R projection.

best_chi2_2 = 1e10
best_r = 0
best_alpha_2 = 0

for r_try in np.linspace(0.1, 5.0, 100):
    ht23_t = r_try * eps
    ht12_t = r_try * eps**3
    ht13_t = r_try * eps**2
    
    h_tilde_t = np.array([
        [0,         ht12_t,   ht13_t],
        [-ht12_t,   0,        ht23_t],
        [-ht13_t,  -ht23_t,   0]
    ])
    
    for alpha in np.linspace(0, 2*np.pi, 200):
        k1 = kappa1
        k2 = kappa2 * np.exp(1j * alpha)
        
        M_u = h * k1 + h_tilde_t * k2
        M_d = h * k2 + h_tilde_t * k1
        
        try:
            U_u, s_u, Vh_u = svd(M_u)
            U_d, s_d, Vh_d = svd(M_d)
            
            M_u_s = M_u * (m_t / s_u[-1])
            M_d_s = M_d * (m_b / s_d[-1])
            
            U_u, s_u, Vh_u = svd(M_u_s)
            U_d, s_d, Vh_d = svd(M_d_s)
            
            V = U_u.conj().T @ U_d
        except:
            continue
        
        chi2 = sum((abs(V[i,j]) - val)**2 / val**2 for (i,j), val in V_obs_dict.items())
        
        if chi2 < best_chi2_2:
            best_chi2_2 = chi2
            best_r = r_try
            best_alpha_2 = alpha

print(f"  Best h̃/h ratio = {best_r:.4f}")
print(f"  Best α = {np.degrees(best_alpha_2):.1f}°")
print(f"  χ² = {best_chi2_2:.6f}")

# Recompute at best parameters
ht23_b = best_r * eps
ht12_b = best_r * eps**3
ht13_b = best_r * eps**2

h_tilde_b = np.array([
    [0,         ht12_b,   ht13_b],
    [-ht12_b,   0,        ht23_b],
    [-ht13_b,  -ht23_b,   0]
])

k1 = kappa1
k2 = kappa2 * np.exp(1j * best_alpha_2)

M_u_b = h * k1 + h_tilde_b * k2
M_d_b = h * k2 + h_tilde_b * k1

U_u, s_u, _ = svd(M_u_b)
U_d, s_d, _ = svd(M_d_b)

M_u_b *= m_t / s_u[-1]
M_d_b *= m_b / s_d[-1]

U_u, s_u, _ = svd(M_u_b)
U_d, s_d, _ = svd(M_d_b)

V_scan = U_u.conj().T @ U_d

print(f"\n  |V_CKM| at best scan:")
print(f"  {'':>8} {'d':>10} {'s':>10} {'b':>10}")
for i in range(3):
    print(f"  {labels[i]:>8} {abs(V_scan[i,0]):>10.5f} {abs(V_scan[i,1]):>10.5f} {abs(V_scan[i,2]):>10.5f}")

V_us_s = abs(V_scan[0,1])
V_cb_s = abs(V_scan[1,2])
V_ub_s = abs(V_scan[0,2])

J_s = np.imag(V_scan[0,1] * V_scan[1,2] * np.conj(V_scan[0,2]) * np.conj(V_scan[1,1]))

print(f"\n  |V_us| = {V_us_s:.4f} (obs: 0.2250, {abs(V_us_s-0.225)/0.225*100:.1f}%)")
print(f"  |V_cb| = {V_cb_s:.5f} (obs: 0.04182, {abs(V_cb_s-0.04182)/0.04182*100:.1f}%)")
print(f"  |V_ub| = {V_ub_s:.6f} (obs: 0.00369, {abs(V_ub_s-0.00369)/0.00369*100:.1f}%)")
print(f"  J = {J_s:.2e} (obs: 3.08e-5)")

# Check: is the bracket ratio r = ||L3_anti||/||L3_sym|| close to best_r?
print(f"\n  Bracket prediction: r = ||L3_anti||/||L3_sym|| = {r_anti_sym:.4f}")
print(f"  Best-fit r = {best_r:.4f}")
print(f"  Ratio best/bracket = {best_r/r_anti_sym:.3f}")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("PHASE 5 RESULT")
print(f"{'='*70}")
print(f"""
  THE BI-DOUBLET MECHANISM:
  
    M_u = h κ₁ + h̃ κ₂ e^{{iα}}
    M_d = h κ₂ e^{{iα}} + h̃ κ₁
    
  where h is SYMMETRIC (from torsion bracket) and h̃ is 
  ANTISYMMETRIC (from gauge bracket) in generation space.
  
  FIXED PARAMETERS (from ACS):
    tan(β) = κ₁/κ₂ = 1/2 (bracket norm ratio)
    ε = λ_W = 0.2265 (Wolfenstein parameter)
    
  SCANNED PARAMETERS:
    h̃/h ratio (bracket predicts {r_anti_sym:.4f})
    CP phase α
    
  BEST FIT:
    h̃/h = {best_r:.4f}, α = {np.degrees(best_alpha_2):.1f}°
    |V_us| = {V_us_s:.4f} ({abs(V_us_s-0.225)/0.225*100:.1f}% from observed)
    |V_cb| = {V_cb_s:.5f} ({abs(V_cb_s-0.04182)/0.04182*100:.1f}% from observed)
    |V_ub| = {V_ub_s:.6f} ({abs(V_ub_s-0.00369)/0.00369*100:.1f}% from observed)
    J = {J_s:.2e} (obs: 3.08e-5)
    
  THE KEY INSIGHT:
    The CKM mixing arises from the DIFFERENT WEIGHTS of the
    symmetric (h) and antisymmetric (h̃) Yukawa couplings in the
    up-type and down-type mass matrices. The up-type matrix has
    more antisymmetric contribution (weighted by κ₂ > κ₁), while
    the down-type has more symmetric contribution.
    
    The mechanism REQUIRES both h and h̃ to be non-zero, which
    is guaranteed by the bracket structure: the torsion bracket
    generates h (symmetric) and the gauge bracket generates h̃
    (antisymmetric).
""")
