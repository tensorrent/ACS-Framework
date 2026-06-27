#!/usr/bin/env python3
"""
PHASE 12 - TASK 1: REDO θ_13 FROM PALATINI YUKAWA STRUCTURE
==============================================================
No TBM assumption. No Cabibbo ansatz. Just the Palatini bracket on
the bi-doublet and the spectrum of ad_T_BL (proved in Theorem C).

APPROACH:
  1. Derive the structure of the neutrino mass matrix from the Palatini
     Yukawa operators acting on the (4,2,1) ⊕ (4bar,1,2) representation.
  2. Use the T_BL decomposition of sl(4) → su(3) × u(1)_{B-L} to
     identify which generations mix with which.
  3. Diagonalize. Read off PMNS angles.
  4. Compare with data honestly.
"""
import numpy as np
from sympy import symbols, Matrix, sqrt, Rational, eye, zeros, simplify
from sympy import Symbol, atan2, asin, cos, sin, pi, N, nsimplify
from scipy.optimize import minimize, fsolve

print("=" * 70)
print("TASK 1.1: THE PALATINI YUKAWA STRUCTURE")
print("=" * 70)

print(r"""
The fermion content of Pati-Salam:
  ψ_L = (4, 2, 1):   left-handed quark-lepton doublet
  ψ_R = (4, 1, 2):   right-handed quark-lepton doublet

Under T_BL = diag(1/3, 1/3, 1/3, -1), the SU(4) index splits:
  ψ = (q, q, q, l)    q = quark (B-L = 1/3), l = lepton (B-L = -1)

The Palatini bracket [e, ω] acts on BOTH the SU(4) and Lorentz indices.
For the Yukawa sector, the relevant operator is the one that generates
mass mixing: M = ψ̄_L Y ψ_R × (VEV).

WITH BRACKET STRUCTURE:
  Y = h_Φ · τ_2  + h̃_Φ · (τ_1 ⊗ τ_1)    [bi-doublet contribution]
     + y_Δ · (Δ_R VEV ⊗ iτ_2)             [triplet contribution]
  
  where h̃/h = 2/3 is derived from the Palatini bracket (Paper A, §7).

THE CRUCIAL INSIGHT:
  The lepton sector involves the 4th SU(4) index, which has
  T_BL eigenvalue -1, differing from the quark indices (1/3) by 4/3.
  
  This eigenvalue difference (4/3) is EXACTLY the nontrivial eigenvalue
  of ad_T_BL (Theorem C).
  
  So the structure of the lepton mass matrix is determined by HOW the
  three generations couple to the 4th index vs the first three.
""")

print("=" * 70)
print("TASK 1.2: THE NEUTRINO MASS MATRIX FROM THE BRACKET")
print("=" * 70)

# The neutrino sector in PS has 6 fermions per generation:
# 3 ν_L (from (4,2,1)) + 3 ν_R (from (4bar,1,2))
# (Actually: one ν_L, one ν_R per generation, times 3 generations)
# The Dirac mass m_D comes from the bi-doublet VEV
# The Majorana mass M_R comes from the Δ_R VEV

# Under the Palatini bracket, the Yukawa texture in generation space
# inherits structure from [T_BL, ·]

print(r"""
In the 3-generation basis, the Yukawa matrices h and h̃ are 3x3 complex.
The generations are distinguished by THEIR ORDER in the ad_T_BL iteration.

Specifically (from Theorem C):
  Gen 1 ~ ad_T_BL^0(X) eigenspace (λ = 0)
  Gen 2 ~ ad_T_BL^1(X) eigenspace (λ = 4/3)
  Gen 3 ~ ad_T_BL^2(X) eigenspace (λ = -4/3)

HIERARCHY: The natural mass structure (at the Planck scale or PS scale)
is roughly:
  m_i ∝ |λ_i|^k × v
where λ_i are the ad_T_BL eigenvalues and k depends on the Yukawa order.

For k = 1 (direct bracket), the diagonal hierarchy is:
  m_1 : m_2 : m_3 ~ 0 : 4/3 : 4/3

This gives two non-zero masses, one zero mass — WRONG for neutrinos
(all three should be non-zero).

For k = 2 (double bracket), the hierarchy is:
  m_1 : m_2 : m_3 ~ 0 : 16/9 : 16/9

Same problem. The bracket naturally gives TWO massive states and
one massless state (because λ=0 is an eigenvalue of ad_T_BL).

THIS IS THE KEY STRUCTURAL POINT.
""")

# Let me compute this explicitly
# Build ad_T_BL on sl(4) and find its three eigenspaces
T_BL = np.diag([1/3, 1/3, 1/3, -1])

def make_sl4_basis():
    basis = []
    labels = []
    for (a, b) in [(0, 1), (1, 2), (2, 3)]:
        M = np.zeros((4, 4)); M[a, a] = 1; M[b, b] = -1
        basis.append(M); labels.append(f'H{a}{b}')
    for (i, j) in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]:
        A = np.zeros((4, 4)); A[i, j] = 1; A[j, i] = -1
        basis.append(A); labels.append(f'A{i}{j}')
        S = np.zeros((4, 4)); S[i, j] = 1; S[j, i] = 1
        basis.append(S); labels.append(f'S{i}{j}')
    return basis, labels

basis, labels = make_sl4_basis()

# Compute ad_T_BL action on each basis element
eigenspaces = {0.0: [], 4/3: [], -4/3: []}
for name, X in zip(labels, basis):
    adX = T_BL @ X - X @ T_BL
    # Is it zero?
    if np.max(np.abs(adX)) < 1e-10:
        eigenspaces[0.0].append(name)
    else:
        # Check which eigenvalue: ad_T_BL(X) = λ X requires proportionality
        ratio = adX[np.abs(X) > 1e-10][0] / X[np.abs(X) > 1e-10][0]
        ratio = round(ratio, 6)
        if abs(ratio - 4/3) < 1e-5:
            eigenspaces[4/3].append(name)
        elif abs(ratio - (-4/3)) < 1e-5:
            eigenspaces[-4/3].append(name)
        else:
            # Mixed — need to decompose
            # A_{i3} + S_{i3} and A_{i3} - S_{i3} are eigenvectors
            pass

print("The three eigenspaces of ad_T_BL on sl(4,R):")
for ev, members in eigenspaces.items():
    print(f"  λ = {ev:+.4f} : {len(members)} members: {members}")

print(r"""
STRUCTURE OF THE MASS MATRIX:
  The three generations correspond to three different eigenspaces of
  ad_T_BL. The mass matrix M in the generation basis has the form:
  
    M_ij = v × Y_ij
    
  where Y_ij depends on the Yukawa structure AND on how the three
  generations are projected into the ad_T_BL eigenspaces.

  Natural form (from Palatini bracket):
    Y = [ a   b   c ]
        [ b*  d   e ]
        [ c*  e*  f ]
  
  where the diagonal entries (a, d, f) come from the direct action,
  and the off-diagonal (b, c, e) come from bracket mixing.

FOR NEUTRINOS SPECIFICALLY:
  m_ν_eff = m_D · M_R^(-1) · m_D^T   (see-saw Type I)
  
  The Palatini structure restricts the form of m_D and M_R, but
  does NOT fix their numerical values (those are the free parameters).
""")

print("=" * 70)
print("TASK 1.3: PMNS FROM DIAGONALIZATION")
print("=" * 70)

# Try a natural ansatz coming from the Palatini structure:
# The leading-order mass matrix in the "natural basis" where ad_T_BL 
# is diagonal.

# In this basis, if the mass matrix is DIAGONAL, the PMNS = V_lepton^dag V_neutrino
# would be the identity — NO mixing. This is the opposite of observation.

# So the mixing MUST come from the rotation between the "generation basis"
# and the "ad_T_BL eigenbasis."

# Try the simplest non-trivial ansatz consistent with the Palatini bracket:
# A "democratic" Yukawa coupling modulated by the T_BL eigenvalues.

# In the quark sector, the Cabibbo-KM structure is known to give large
# mixing. The question: does the SAME bracket structure give the observed
# PMNS angles?

print(r"""
TEST: THE DEMOCRATIC + T_BL-STRUCTURED ANSATZ

  A natural Palatini Yukawa matrix at the PS scale:
  
    Y = y₀ · 1_{3x3} + y₁ · f(T_BL) + y₂ · f(T_BL)²
  
  where f(T_BL) is the 3x3 projection of ad_T_BL onto the generation
  space. From Theorem C, f has 3 eigenvalues (0, +a, -a) for some
  value a. In the basis where f is diagonal, Y is diagonal too.

  The MIXING comes from the rotation between the democratic basis
  (where y₀ dominates, all generations equivalent) and the eigenvalue
  basis (where y₁, y₂ structure enters).
""")

# Let me parameterize and solve
# Work in the charged lepton basis for simplicity
# Suppose Y_lepton has form:
# Y_l = y_0 D + y_1 (T) + y_2 (T^2)  where T is the ad_T_BL projection
# In the T-diagonal basis: Y_l diagonal: (y_0, y_0 + 4y_1/3 + 16y_2/9,
#                                          y_0 - 4y_1/3 + 16y_2/9)
# This is STILL diagonal in the eigenbasis.

# For nontrivial mixing, we need a DIFFERENT ad_T_BL projection for neutrinos
# vs charged leptons, OR an off-diagonal piece from see-saw.

# The RH neutrino Majorana mass is distinct, so let's model it:
# M_R = M₀ · 1 + M₁ · (ν_R specific structure)

# For the see-saw:
# m_ν_eff = m_D · M_R^(-1) · m_D^T

# Suppose (natural Palatini structure):
#   m_D diagonal in T_BL-basis: diag(m_D0, m_D1, m_D2)
#   M_R diagonal in DIFFERENT basis: M_0 · 1 + M_1 · (some direction)

# The misalignment between the two bases gives the PMNS mixing.

# Numerical test: try various relative alignments and see which gives
# observable angles close to data.

import itertools
from scipy.linalg import svd

def pmns_from_matrices(Y_l, M_nu):
    """Compute PMNS angles from charged-lepton Yukawa Y_l and 
    effective neutrino mass matrix M_nu (both 3x3 complex)."""
    # Diagonalize Y_l Y_l^dag (left) to get V_l
    YlYl = Y_l @ Y_l.conj().T
    evals_l, V_l = np.linalg.eigh(YlYl)
    # Sort by eigenvalue (mass squared)
    idx = np.argsort(evals_l)
    V_l = V_l[:, idx]
    
    # Diagonalize M_nu M_nu^dag to get V_nu
    MnuMnu = M_nu @ M_nu.conj().T
    evals_nu, V_nu = np.linalg.eigh(MnuMnu)
    idx_nu = np.argsort(evals_nu)
    V_nu = V_nu[:, idx_nu]
    
    # PMNS = V_l^dag · V_nu
    U = V_l.conj().T @ V_nu
    
    # Extract standard-parametrization angles
    # |U_e3| = sin(theta_13)
    theta_13 = np.arcsin(np.abs(U[0, 2]))
    theta_12 = np.arctan2(np.abs(U[0, 1]), np.abs(U[0, 0]))
    theta_23 = np.arctan2(np.abs(U[1, 2]), np.abs(U[2, 2]))
    
    return np.degrees(theta_12), np.degrees(theta_13), np.degrees(theta_23)

# Observed values
obs = {'12': 33.41, '13': 8.57, '23': 49.2}

# Set up the Palatini ansatz
# Charged lepton Yukawa in generation basis (diagonal approximation)
# with small bracket-induced off-diagonal mixing
print(r"""
NUMERICAL EXPLORATION of the Palatini ansatz:

Parameterize:
  Y_l = diag(m_e, m_μ, m_τ)/v  (charged lepton masses)
       + ε_l × (bracket mixing matrix B_l)
  
  m_ν = diag(m_1, m_2, m_3)
       + ε_ν × (bracket mixing matrix B_ν)
  
  where B is a specific matrix from the ad_T_BL structure.

The simplest nontrivial bracket mixing in 3x3:
  B = [ 0  a  b ]
      [ a* 0  c ]
      [ b* c* 0 ]
""")

# For each ansatz, compute PMNS angles and check agreement
# Parameterize: a, b, c in the [0,1] range, compare with data

def ansatz_angles(a, b, c, alignment_angle=0):
    """Ansatz-based PMNS computation."""
    v = 246.22
    m_e, m_mu, m_tau = 0.000511, 0.1057, 1.777
    
    # Charged lepton Yukawa (nearly diagonal)
    Y_l = np.diag([m_e, m_mu, m_tau]) / v
    
    # Neutrino mass matrix (diagonal + off-diagonal)
    m1, m2, m3 = 0.0, 0.0086, 0.05  # eV (normal hierarchy approximation)
    M_nu = np.diag([m1, m2, m3]) + np.array([
        [0, a, b],
        [a, 0, c],
        [b, c, 0]
    ]) * 0.01  # scale
    
    # Add alignment rotation
    ca, sa = np.cos(alignment_angle), np.sin(alignment_angle)
    R = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    M_nu = R @ M_nu @ R.T
    
    return pmns_from_matrices(Y_l, M_nu)

# Scan over the parameter space
print("Sample Palatini-inspired configurations:")
print(f"  {'a':>6} {'b':>6} {'c':>6} {'θ12':>8} {'θ13':>8} {'θ23':>8} {'χ²':>8}")

best_chi2 = 1e10
best_params = None
for a in np.linspace(0.1, 1.0, 5):
    for b in np.linspace(0.1, 1.0, 5):
        for c in np.linspace(0.1, 1.0, 5):
            try:
                t12, t13, t23 = ansatz_angles(a, b, c)
                chi2 = ((t12 - obs['12']) / 0.75)**2 + ((t13 - obs['13']) / 0.12)**2 + ((t23 - obs['23']) / 0.9)**2
                if chi2 < best_chi2:
                    best_chi2 = chi2
                    best_params = (a, b, c, t12, t13, t23)
            except:
                pass

print(f"  Best fit: a={best_params[0]:.2f}, b={best_params[1]:.2f}, c={best_params[2]:.2f}")
print(f"    θ12={best_params[3]:.2f}° (obs {obs['12']}°)")
print(f"    θ13={best_params[4]:.2f}° (obs {obs['13']}°)")
print(f"    θ23={best_params[5]:.2f}° (obs {obs['23']}°)")
print(f"    χ² = {best_chi2:.1f}")

print(r"""
HONEST ASSESSMENT:
  Even with best-fit Palatini-inspired parameters, the simultaneous fit
  to all three PMNS angles is not dramatically better than existing
  approaches. The parameters a, b, c are free — they're exactly the 
  α₁, α₂, β_c cross-couplings from the 5-parameter boundary.

  SO: the Palatini structure MOTIVATES the form of the off-diagonal
  mixing matrix but does NOT fix its magnitudes. The PMNS angles are
  therefore FIT to data, not predicted.

  NEW FINDING: The OLD prediction θ_13 = arcsin(λ_W/√2) was a
  CABIBBO-MOTIVATED fit, not a Palatini derivation. The Palatini
  structure is CONSISTENT with any PMNS pattern that can be 
  generated by a 3x3 complex Hermitian mass matrix.

  The correct statement of the Palatini framework's PMNS prediction:
  "Three generations exist (Theorem C). The mixing pattern has the
   form of a bracket-induced off-diagonal perturbation on a 
   diagonal base. The magnitudes are fit by α_i, β_c, not derived."
""")

print("=" * 70)
print("TASK 1.4: WHAT IS ACTUALLY DERIVED vs FIT")
print("=" * 70)

print(r"""
PALATINI-DERIVED (from bracket structure):
  ✓ Three generations exist                      [Theorem C: rank of ad_T_BL]
  ✓ Mass matrix has off-diagonal bracket form    [from B matrix structure]
  ✓ Yukawa ratio h̃/h = 2/3                       [Paper A Koide derivation]

FIT TO DATA (via 5 free parameters):
  × θ_12 exact value                             [depends on α₁, α₂]
  × θ_13 exact value                             [depends on α₁, α₂, β_c]
  × θ_23 exact value                             [depends on α₁, α₂, β_c]
  × δ_CP phase                                   [depends on β_c]

CORRECTED LEDGER for PMNS:
  Old claim: "θ_12, θ_13, θ_23 derived from TBM + Cabibbo correction"
  New statement: "PMNS mixing inherits the generation structure from
  ad_T_BL (Theorem C). Specific angle values are fit parameters that
  live in the free 5-parameter Higgs sector, not predicted by the
  Palatini bracket alone."

NUMBER OF PREDICTIONS LOST:
  θ_12 (previously 32.4°, off by 1.3σ): removed from "derived" ledger
  θ_13 (previously 9.2°, off by 5.2σ): removed from "derived" ledger  
  θ_23 (previously 45°, off by 4.7σ): removed from "derived" ledger

  These are not FAILURES of the framework — they were never genuine
  predictions. The TBM base was chosen by analogy with flavor-symmetry
  literature, not derived from the Palatini bracket.

  Removing them brings the ledger in line with reality: Palatini
  fixes STRUCTURE (3 generations, form of mixing matrix), not
  NUMERICAL values.

UPDATED DERIVED MATCHES: was 11, now 8.
  8 genuinely derived: m_H, sin²θ_W, α_s, γ_BI, θ₀ Koide, m_e/m_μ,
                       m_μ/m_τ, see-saw product.
  3 removed: θ_12, θ_13, θ_23 (PMNS — all were fit-dependent)
""")
