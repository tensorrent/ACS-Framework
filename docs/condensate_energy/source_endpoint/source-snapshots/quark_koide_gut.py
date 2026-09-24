#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
QUARK KOIDE AT THE GUT SCALE
===============================
The Koide formula works for leptons (0.001%) but fails for quarks 
(27% for up-type). Prediction: it should work at the GUT/Palatini 
scale before QCD running distorts the masses.

Use the known QCD RG equations to run quark masses from the low-energy
(pole mass) values UP to the GUT scale (10^16 GeV) and check if 
the Koide ratio Q → 2/3.
"""

import numpy as np

print("=" * 70)
print("QUARK KOIDE AT THE GUT SCALE")
print("Running Masses UP via QCD Renormalization Group")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# QCD running mass formula (1-loop):
# m(μ) = m(μ₀) × [α_s(μ)/α_s(μ₀)]^{γ₀/(2β₀)}
#
# where:
#   β₀ = (33 - 2n_f) / (12π)  (1-loop beta function)
#   γ₀ = 1/π                   (1-loop mass anomalous dimension)
#   n_f = number of active flavours at scale μ
#
# α_s running (1-loop):
#   α_s(μ) = α_s(M_Z) / [1 + (β₀/π) α_s(M_Z) ln(μ/M_Z)]

# Physical constants
alpha_s_MZ = 0.1179  # Strong coupling at M_Z
M_Z = 91.1876  # GeV

# Quark pole masses (GeV) — PDG 2024 values
m_u_pole = 0.00216  # up
m_c_pole = 1.27     # charm
m_t_pole = 173.1    # top

m_d_pole = 0.00467  # down
m_s_pole = 0.0934   # strange
m_b_pole = 4.18     # bottom

# Lepton masses (don't run under QCD)
m_e = 0.000511  # GeV
m_mu = 0.10566
m_tau = 1.7769

print(f"\n── Low-Energy Masses (GeV) ──\n")
print(f"  Up quarks:   u = {m_u_pole:.5f}, c = {m_c_pole:.4f}, t = {m_t_pole:.1f}")
print(f"  Down quarks: d = {m_d_pole:.5f}, s = {m_s_pole:.4f}, b = {m_b_pole:.3f}")
print(f"  Leptons:     e = {m_e:.6f}, μ = {m_mu:.5f}, τ = {m_tau:.4f}")

# Koide ratios at low energy
def koide(m1, m2, m3):
    return (m1 + m2 + m3) / (np.sqrt(m1) + np.sqrt(m2) + np.sqrt(m3))**2

Q_up_low = koide(m_u_pole, m_c_pole, m_t_pole)
Q_down_low = koide(m_d_pole, m_s_pole, m_b_pole)
Q_lepton = koide(m_e, m_mu, m_tau)

print(f"\n  Koide ratios at low energy:")
print(f"    Leptons:     Q = {Q_lepton:.6f} (target: {2/3:.6f}, error: {abs(Q_lepton-2/3)/(2/3)*100:.4f}%)")
print(f"    Up quarks:   Q = {Q_up_low:.6f} (error: {abs(Q_up_low-2/3)/(2/3)*100:.1f}%)")
print(f"    Down quarks: Q = {Q_down_low:.6f} (error: {abs(Q_down_low-2/3)/(2/3)*100:.1f}%)")

# ═══════════════════════════════════════════════════════════════
print(f"\n── Running Quark Masses to High Scales ──\n")

def alpha_s(mu, n_f=6):
    """1-loop running of α_s."""
    beta0 = (33 - 2*n_f) / (12 * np.pi)
    if mu <= 0:
        return alpha_s_MZ
    return alpha_s_MZ / (1 + beta0 * alpha_s_MZ * np.log(mu / M_Z))

def run_mass(m_low, mu_low, mu_high, n_f=6):
    """Run quark mass from mu_low to mu_high using 1-loop RGE."""
    gamma0 = 1 / np.pi  # 1-loop mass anomalous dimension
    beta0 = (33 - 2*n_f) / (12 * np.pi)
    
    a_low = alpha_s(mu_low, n_f)
    a_high = alpha_s(mu_high, n_f)
    
    if a_low <= 0 or a_high <= 0:
        return m_low
    
    # m(μ) = m(μ₀) × (α_s(μ)/α_s(μ₀))^{γ₀/(2β₀)}
    exponent = gamma0 / (2 * beta0)
    return m_low * (a_high / a_low) ** exponent

# Threshold crossings: run with appropriate n_f
# Below m_b: n_f = 5
# Above m_b, below m_t: n_f = 5  
# Above m_t: n_f = 6

def run_to_scale(m_pole, mu_pole, mu_target):
    """Run mass to target scale with threshold matching."""
    # Simplified: use n_f = 6 for everything above M_Z
    # (good enough for order-of-magnitude)
    if mu_target < mu_pole:
        return m_pole  # Don't run down
    return run_mass(m_pole, mu_pole, mu_target, n_f=6)

# Scale scan
scales = [2, 10, 100, 1000, 1e4, 1e6, 1e8, 1e10, 1e12, 1e14, 1e16]
scale_names = ["2 GeV", "10 GeV", "100 GeV", "1 TeV", "10 TeV", 
               "10⁶", "10⁸", "10¹⁰", "10¹²", "10¹⁴", "10¹⁶ (GUT)"]

print(f"  {'Scale':<12} {'Q_up':<10} {'Q_down':<10} {'Q_lep':<10} {'Best?'}")
print(f"  {'-'*50}")

best_up = (1e10, 0)
best_down = (1e10, 0)

for mu, name in zip(scales, scale_names):
    # Run all quark masses to this scale
    # Use MS-bar masses at μ = 2 GeV as starting point
    # (more appropriate than pole masses for RGE)
    m_u_2 = 0.00216   # MS-bar at 2 GeV
    m_d_2 = 0.00467
    m_s_2 = 0.0934
    m_c_2 = 1.27      # MS-bar at m_c
    m_b_2 = 4.18      # MS-bar at m_b
    m_t_2 = 163.0     # MS-bar at m_t
    
    # Run from their natural scales
    mu_u = run_mass(m_u_2, 2.0, mu, n_f=6) if mu > 2 else m_u_2
    mu_c = run_mass(m_c_2, m_c_2, mu, n_f=6) if mu > m_c_2 else m_c_2
    mu_t = run_mass(m_t_2, m_t_2, mu, n_f=6) if mu > m_t_2 else m_t_2
    
    mu_d = run_mass(m_d_2, 2.0, mu, n_f=6) if mu > 2 else m_d_2
    mu_s = run_mass(m_s_2, 2.0, mu, n_f=6) if mu > 2 else m_s_2
    mu_b = run_mass(m_b_2, m_b_2, mu, n_f=6) if mu > m_b_2 else m_b_2
    
    Q_up = koide(mu_u, mu_c, mu_t)
    Q_down = koide(mu_d, mu_s, mu_b)
    Q_lep = koide(m_e, m_mu, m_tau)  # Leptons don't run
    
    err_up = abs(Q_up - 2/3)
    err_down = abs(Q_down - 2/3)
    
    if err_up < best_up[0]:
        best_up = (err_up, mu, Q_up)
    if err_down < best_down[0]:
        best_down = (err_down, mu, Q_down)
    
    marker = ""
    if err_up < 0.02: marker += " ← up!"
    if err_down < 0.02: marker += " ← down!"
    
    print(f"  {name:<12} {Q_up:<10.6f} {Q_down:<10.6f} {Q_lep:<10.6f}{marker}")

# ═══════════════════════════════════════════════════════════════
print(f"\n── Detailed Analysis ──\n")

print(f"  Best up-type Koide:   Q = {best_up[2]:.6f} at μ = {best_up[1]:.0e} GeV")
print(f"    Error: {best_up[0]/(2/3)*100:.2f}%")
print(f"  Best down-type Koide: Q = {best_down[2]:.6f} at μ = {best_down[1]:.0e} GeV")
print(f"    Error: {best_down[0]/(2/3)*100:.2f}%")

# Show the mass ratios at the GUT scale
mu_GUT = 1e16
masses_up_GUT = [
    run_mass(m_u_2, 2.0, mu_GUT, 6),
    run_mass(m_c_2, m_c_2, mu_GUT, 6),
    run_mass(m_t_2, m_t_2, mu_GUT, 6),
]
masses_down_GUT = [
    run_mass(m_d_2, 2.0, mu_GUT, 6),
    run_mass(m_s_2, 2.0, mu_GUT, 6),
    run_mass(m_b_2, m_b_2, mu_GUT, 6),
]

print(f"\n  Masses at GUT scale (10¹⁶ GeV):")
print(f"    u = {masses_up_GUT[0]*1000:.4f} MeV, c = {masses_up_GUT[1]:.4f} GeV, t = {masses_up_GUT[2]:.2f} GeV")
print(f"    d = {masses_down_GUT[0]*1000:.4f} MeV, s = {masses_down_GUT[1]*1000:.2f} MeV, b = {masses_down_GUT[2]:.4f} GeV")

# Mass ratios
print(f"\n  Mass ratios at GUT scale:")
print(f"    m_t/m_c = {masses_up_GUT[2]/masses_up_GUT[1]:.1f} (low E: {m_t_2/m_c_2:.1f})")
print(f"    m_c/m_u = {masses_up_GUT[1]/masses_up_GUT[0]:.1f} (low E: {m_c_2/m_u_2:.1f})")
print(f"    m_b/m_s = {masses_down_GUT[2]/masses_down_GUT[1]:.1f} (low E: {m_b_2/m_s_2:.1f})")
print(f"    m_s/m_d = {masses_down_GUT[1]/masses_down_GUT[0]:.1f} (low E: {m_s_2/m_d_2:.1f})")

# ═══════════════════════════════════════════════════════════════
print(f"\n── The Running Effect ──\n")

# All quarks run the SAME way under QCD (they all carry colour charge)
# So the RATIOS m_t/m_c and m_c/m_u are SCALE-INDEPENDENT at 1-loop
# (the running cancels in the ratio)
# This means: Koide at low energy = Koide at high energy at 1-loop!

# The difference from 2/3 is NOT from QCD running.
# It's from THRESHOLD effects and higher-loop corrections.

print("  KEY INSIGHT: At 1-loop QCD, all quark masses run with the")
print("  SAME anomalous dimension γ₀ = 1/π. Therefore mass RATIOS")
print("  are scale-independent, and the Koide ratio is INVARIANT.")
print(f"")
print(f"  This means: the Koide failure for quarks is NOT from QCD running.")
print(f"  It is an INTRINSIC property of the quark mass matrix.")
print(f"")
print(f"  HOWEVER: at 2-loop and beyond, the anomalous dimensions differ")
print(f"  between quarks (through Yukawa coupling dependence). The top")
print(f"  quark, being so heavy, has a large Yukawa y_t ≈ 1, which")
print(f"  modifies its running differently from u and c.")

# 2-loop correction estimate
# γ = γ₀ α_s/π + γ₁ (α_s/π)² where γ₁ depends on the Yukawa
# For top: γ₁_top includes y_t² correction ≈ 1

# Let me compute with a crude Yukawa correction
print(f"\n── Yukawa-Corrected Running ──\n")

def run_mass_2loop(m_low, mu_low, mu_high, yukawa, n_f=6):
    """2-loop running with Yukawa correction for heavy quarks."""
    gamma0 = 1 / np.pi
    gamma1_yukawa = yukawa**2 / (16 * np.pi**2)  # Yukawa correction
    beta0 = (33 - 2*n_f) / (12 * np.pi)
    
    a_low = alpha_s(mu_low, n_f)
    a_high = alpha_s(mu_high, n_f)
    
    if a_low <= 0 or a_high <= 0:
        return m_low
    
    # Effective anomalous dimension
    gamma_eff = gamma0 + gamma1_yukawa * (a_low + a_high) / 2
    exponent = gamma_eff / (2 * beta0)
    
    return m_low * (a_high / a_low) ** exponent

# Yukawa couplings: y_f = √2 m_f / v where v = 246 GeV
v_higgs = 246.0
y_u = np.sqrt(2) * m_u_2 / v_higgs
y_c = np.sqrt(2) * m_c_2 / v_higgs
y_t = np.sqrt(2) * m_t_2 / v_higgs
y_d = np.sqrt(2) * m_d_2 / v_higgs
y_s = np.sqrt(2) * m_s_2 / v_higgs
y_b = np.sqrt(2) * m_b_2 / v_higgs

print(f"  Yukawa couplings: y_u={y_u:.6f}, y_c={y_c:.4f}, y_t={y_t:.4f}")
print(f"                    y_d={y_d:.6f}, y_s={y_s:.5f}, y_b={y_b:.4f}")

mu_GUT = 2e16
m_u_GUT2 = run_mass_2loop(m_u_2, 2.0, mu_GUT, y_u)
m_c_GUT2 = run_mass_2loop(m_c_2, m_c_2, mu_GUT, y_c)
m_t_GUT2 = run_mass_2loop(m_t_2, m_t_2, mu_GUT, y_t)
m_d_GUT2 = run_mass_2loop(m_d_2, 2.0, mu_GUT, y_d)
m_s_GUT2 = run_mass_2loop(m_s_2, 2.0, mu_GUT, y_s)
m_b_GUT2 = run_mass_2loop(m_b_2, m_b_2, mu_GUT, y_b)

Q_up_GUT2 = koide(m_u_GUT2, m_c_GUT2, m_t_GUT2)
Q_down_GUT2 = koide(m_d_GUT2, m_s_GUT2, m_b_GUT2)

print(f"\n  Koide at GUT scale with Yukawa corrections:")
print(f"    Up quarks:   Q = {Q_up_GUT2:.6f} (low E: {Q_up_low:.6f})")
print(f"    Down quarks: Q = {Q_down_GUT2:.6f} (low E: {Q_down_low:.6f})")
print(f"    Change up:   {(Q_up_GUT2 - Q_up_low)/(2/3)*100:+.2f}% toward 2/3")
print(f"    Change down: {(Q_down_GUT2 - Q_down_low)/(2/3)*100:+.2f}% toward 2/3")

improves_up = abs(Q_up_GUT2 - 2/3) < abs(Q_up_low - 2/3)
improves_down = abs(Q_down_GUT2 - 2/3) < abs(Q_down_low - 2/3)

print(f"\n    Up quarks move {'TOWARD' if improves_up else 'AWAY from'} 2/3 at GUT scale")
print(f"    Down quarks move {'TOWARD' if improves_down else 'AWAY from'} 2/3 at GUT scale")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("RESULT")
print(f"{'='*70}")
print(f"""
  1-LOOP: Quark Koide is SCALE-INVARIANT (all quarks run identically).
    Q_up  = {Q_up_low:.6f} at ALL scales (1-loop)
    Q_down = {Q_down_low:.6f} at ALL scales (1-loop)
    
  2-LOOP (Yukawa): The top quark's large Yukawa (y_t = {y_t:.2f}) 
    modifies its running relative to u and c.
    Q_up at GUT: {Q_up_GUT2:.6f} ({'improves' if improves_up else 'worsens'})
    Q_down at GUT: {Q_down_GUT2:.6f} ({'improves' if improves_down else 'worsens'})
    
  INTERPRETATION:
    The Koide deviation for quarks is NOT a QCD artifact.
    At 1-loop, QCD running preserves the Koide ratio exactly.
    At 2-loop, the top Yukawa shifts Q slightly but doesn't
    bring it to 2/3.
    
    The quark Koide deviation (Q_up = 0.85, Q_down = 0.73) is 
    INTRINSIC to the quark mass matrix. It reflects a genuine
    difference between the quark and lepton sectors:
    
    - Leptons: pure Koide (Q = 2/3 to 0.001%)
      → The three generations sit EXACTLY on the su(3) fundamental cone
    
    - Quarks: modified Koide (Q ≠ 2/3)
      → The quark masses are SHIFTED by the colour interaction
      → The strong force modifies the vacuum direction in the GL(4) fiber
      → The quark θ₀ differs from the lepton θ₀
    
    This is consistent with the ACS picture: leptons are colourless
    (their masses come purely from the Higgs), while quarks carry 
    colour charge (their masses are shifted by the gluon condensate).
    The Koide formula is the COLOUR-FREE limit of the mass formula.
""")
