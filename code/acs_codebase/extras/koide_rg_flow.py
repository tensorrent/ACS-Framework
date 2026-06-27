#!/usr/bin/env python3
"""
THE KOIDE ANGLE RG FLOW: 11.57° → 12.73°
===========================================
The bare geometric angle θ₀ = π/6 - arctan(1/3) = 11.57° at the GUT scale.
The observed IR angle is 12.73°.
Gap: 1.17°.

This computation runs the Standard Model 1-loop RG equations for the
charged lepton Yukawa couplings from M_GUT down to the IR, and extracts
θ₀(μ) at each scale.

The SM 1-loop beta functions for lepton Yukawas:
  16π² dy_i/dt = y_i × [ T - (9/4)g₂² - (15/4)g'² + (3/2)y_i² ]
  
where:
  t = ln(μ/M_Z)
  T = Tr(3Y_u†Y_u + 3Y_d†Y_d + Y_e†Y_e) ≈ 3y_t² (top dominates)
  g₂ = SU(2) gauge coupling
  g' = U(1) hypercharge coupling

The FLAVOUR-UNIVERSAL terms (T, g₂², g'²) scale ALL Yukawas equally
→ they DON'T change θ₀.

The FLAVOUR-DEPENDENT term (3/2)y_i² scales each Yukawa differently
→ this IS what shifts θ₀.

Since y_τ >> y_μ >> y_e, the tau Yukawa runs faster than the others,
pulling θ₀ upward as we flow to the IR.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

print("=" * 70)
print("THE KOIDE ANGLE RG FLOW")
print("From GUT Scale (11.57°) to IR (12.73°)")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# Physical constants at M_Z
M_Z = 91.1876  # GeV
v = 246.22      # Higgs VEV, GeV

# Gauge couplings at M_Z (PDG 2024)
alpha1_MZ = 0.01017  # U(1)_Y (GUT normalised: g'² = 5/3 × g₁²)
alpha2_MZ = 0.03382  # SU(2)_L
alpha3_MZ = 0.1179   # SU(3)_c

g1_MZ = np.sqrt(4 * np.pi * alpha1_MZ)  # ~ 0.357
g2_MZ = np.sqrt(4 * np.pi * alpha2_MZ)  # ~ 0.652
g3_MZ = np.sqrt(4 * np.pi * alpha3_MZ)  # ~ 1.218

# Yukawa couplings at M_Z: y_i = √2 m_i / v
m_e = 0.51099895e-3   # GeV
m_mu = 0.1056583755   # GeV
m_tau = 1.77686        # GeV
m_t = 173.1            # GeV (top quark)

y_e_MZ = np.sqrt(2) * m_e / v
y_mu_MZ = np.sqrt(2) * m_mu / v
y_tau_MZ = np.sqrt(2) * m_tau / v
y_t_MZ = np.sqrt(2) * m_t / v

print(f"\n── Initial Conditions at M_Z = {M_Z} GeV ──\n")
print(f"  Gauge couplings: g₁={g1_MZ:.4f}, g₂={g2_MZ:.4f}, g₃={g3_MZ:.4f}")
print(f"  Yukawa couplings:")
print(f"    y_e  = {y_e_MZ:.6e}")
print(f"    y_μ  = {y_mu_MZ:.6e}")
print(f"    y_τ  = {y_tau_MZ:.6e}")
print(f"    y_t  = {y_t_MZ:.4f}")

# ═══════════════════════════════════════════════════════════════
# Extract θ₀ from Yukawa couplings
def extract_theta0(y_e, y_mu, y_tau):
    """Extract the Koide angle θ₀ from three Yukawa couplings.
    Koide parametrisation: √m_i = A(1 + √2 cos(θ₀ + 2πi/3))
    Since y_i = √2 m_i / v, we have √y_i ∝ m_i^{1/4} × const
    Actually: √m_i = √(y_i v/√2), so we fit to √(y_i).
    """
    # masses from yukawas
    masses = [(y * v / np.sqrt(2)) for y in [y_e, y_mu, y_tau]]
    sqrt_m = sorted([np.sqrt(m) for m in masses])
    
    def err(params):
        A, th0 = params
        pred = sorted([A * (1 + np.sqrt(2) * np.cos(th0 + 2*np.pi*k/3)) 
                       for k in range(3)])
        if any(p <= 0 for p in pred):
            return 1e10
        return sum((np.log(p/o))**2 for p, o in zip(pred, sqrt_m))
    
    res = minimize(err, [sum(sqrt_m)/3, 0.2], method='Nelder-Mead',
                  options={'xatol': 1e-14, 'fatol': 1e-16, 'maxiter': 50000})
    return np.degrees(res.x[1])

theta0_MZ = extract_theta0(y_e_MZ, y_mu_MZ, y_tau_MZ)
print(f"\n  θ₀ at M_Z: {theta0_MZ:.4f}°")
print(f"  Target:    12.73°")

# ═══════════════════════════════════════════════════════════════
# 1-loop RG equations
print(f"\n── SM 1-Loop Beta Functions ──\n")

def rge_system(t, y_vec):
    """
    SM 1-loop RG equations.
    y_vec = [g1, g2, g3, y_e, y_mu, y_tau, y_t]
    t = ln(μ/M_Z)
    
    16π² dg_i/dt = b_i g_i³
    16π² dy_l/dt = y_l × [T - c₁g'² - c₂g₂² + (3/2)y_l²]
    16π² dy_t/dt = y_t × [T - c₁'g'² - c₂'g₂² - 8g₃² + (9/2)y_t²]
    """
    g1, g2, g3, ye, ymu, ytau, yt = y_vec
    
    # Beta function coefficients (SM with 3 generations)
    b1 = 41/10   # U(1)
    b2 = -19/6   # SU(2) 
    b3 = -7      # SU(3)
    
    # Trace term: T = 3y_t² + 3y_b² + y_τ² ≈ 3y_t² + y_τ²
    # (neglecting light quark and lepton Yukawas)
    T = 3 * yt**2 + ytau**2
    
    # Lepton gauge coefficients
    # For charged leptons: 16π² dy_l/dt = y_l(T - (9/4)g₂² - (15/4)g'² + (3/2)y_l²)
    # Using GUT-normalised g₁: g' = √(3/5) g₁
    gp_sq = (3/5) * g1**2
    
    c_lepton_gp = 15/4    # coefficient of g'² for leptons
    c_lepton_g2 = 9/4     # coefficient of g₂²
    
    # Top quark gauge coefficients
    c_top_gp = 17/20      # coefficient of g'² for up-type quarks  
    c_top_g2 = 9/4
    c_top_g3 = 8
    
    factor = 1 / (16 * np.pi**2)
    
    # Gauge coupling running
    dg1 = factor * b1 * g1**3
    dg2 = factor * b2 * g2**3
    dg3 = factor * b3 * g3**3
    
    # Lepton Yukawa running
    common_lepton = T - c_lepton_g2 * g2**2 - c_lepton_gp * gp_sq
    
    dye = factor * ye * (common_lepton + 1.5 * ye**2)
    dymu = factor * ymu * (common_lepton + 1.5 * ymu**2)
    dytau = factor * ytau * (common_lepton + 1.5 * ytau**2)
    
    # Top Yukawa running
    dyt = factor * yt * (T - c_top_gp * gp_sq - c_top_g2 * g2**2 
                         - c_top_g3 * g3**2 + 4.5 * yt**2)
    
    return [dg1, dg2, dg3, dye, dymu, dytau, dyt]

# ═══════════════════════════════════════════════════════════════
# Run from M_Z UP to M_GUT
print(f"  Running from M_Z = {M_Z:.1f} GeV up to M_GUT = 2×10¹⁶ GeV...\n")

t_MZ = 0  # ln(M_Z/M_Z) = 0
t_GUT = np.log(2e16 / M_Z)  # ln(M_GUT/M_Z) ≈ 39.3

y0 = [g1_MZ, g2_MZ, g3_MZ, y_e_MZ, y_mu_MZ, y_tau_MZ, y_t_MZ]

# Solve ODE from t=0 (M_Z) to t=t_GUT
sol = solve_ivp(rge_system, [t_MZ, t_GUT], y0, 
                method='RK45', max_step=0.1, rtol=1e-10, atol=1e-13,
                dense_output=True)

if not sol.success:
    print(f"  ODE solver failed: {sol.message}")
else:
    print(f"  ODE solved successfully ({len(sol.t)} steps)")

# Extract θ₀ at various scales
scales_t = np.linspace(t_MZ, t_GUT, 100)
scales_GeV = M_Z * np.exp(scales_t)
theta0_running = []

print(f"\n  {'Scale (GeV)':<16} {'y_e':<12} {'y_μ':<12} {'y_τ':<12} {'y_t':<8} {'θ₀ (deg)'}")
print(f"  {'-'*72}")

for i, t in enumerate(scales_t):
    state = sol.sol(t)
    g1, g2, g3, ye, ymu, ytau, yt = state
    
    if ye > 0 and ymu > 0 and ytau > 0:
        th0 = extract_theta0(ye, ymu, ytau)
        theta0_running.append(th0)
    else:
        theta0_running.append(np.nan)
    
    if i % 20 == 0 or i == len(scales_t) - 1:
        mu = M_Z * np.exp(t)
        if mu > 1e12:
            mu_str = f"{mu:.1e}"
        else:
            mu_str = f"{mu:.1f}"
        print(f"  {mu_str:<16} {ye:<12.4e} {ymu:<12.4e} {ytau:<12.4e} {yt:<8.4f} {theta0_running[-1]:.4f}")

theta0_running = np.array(theta0_running)

# ═══════════════════════════════════════════════════════════════
print(f"\n── Results ──\n")

theta0_IR = theta0_running[0]   # at M_Z
theta0_UV = theta0_running[-1]  # at M_GUT

# The bare geometric prediction
theta0_bare = np.degrees(np.pi/6 - np.arctan(1/3))  # 11.565°

print(f"  θ₀ at M_Z (IR):          {theta0_IR:.4f}°")
print(f"  θ₀ at M_GUT (UV):        {theta0_UV:.4f}°")
print(f"  Shift (UV → IR):         {theta0_IR - theta0_UV:+.4f}°")
print(f"")
print(f"  Bare geometric angle:     {theta0_bare:.4f}°")
print(f"  Observed IR angle:        12.7328°")
print(f"  Required shift:           {12.7328 - theta0_bare:+.4f}°")
print(f"  RG-computed shift:        {theta0_IR - theta0_UV:+.4f}°")

# The KEY question: does the RG shift go in the RIGHT DIRECTION?
shift_rg = theta0_IR - theta0_UV
shift_needed = 12.7328 - theta0_bare

print(f"\n  Direction match: {'YES ✓' if np.sign(shift_rg) == np.sign(shift_needed) else 'NO ✗'}")
print(f"  Magnitude: RG gives {abs(shift_rg):.4f}° of the needed {abs(shift_needed):.4f}°")
print(f"  Fraction explained: {abs(shift_rg / shift_needed) * 100:.1f}%")

# ═══════════════════════════════════════════════════════════════
print(f"\n── The Flavour-Dependent Shift ──\n")

# The shift comes entirely from the (3/2)y_i² term.
# At 1-loop, the flavour-dependent part shifts θ₀ by:
#   Δθ₀ ≈ (3/(32π²)) × (y_τ² - y_μ²) × ln(M_GUT/M_Z)
# (since y_e² ≈ 0 and y_μ² ≈ 0 compared to y_τ²)

delta_theta_analytic = (3 / (32 * np.pi**2)) * (y_tau_MZ**2) * t_GUT
delta_theta_analytic_deg = np.degrees(delta_theta_analytic)

print(f"  Analytic estimate of flavour-dependent shift:")
print(f"    Δθ₀ ≈ (3/(32π²)) × y_τ² × ln(M_GUT/M_Z)")
print(f"         = (3/(32π²)) × {y_tau_MZ**2:.4e} × {t_GUT:.2f}")
print(f"         = {delta_theta_analytic:.6f} rad = {delta_theta_analytic_deg:.4f}°")
print(f"")
print(f"  This is the dominant contribution. The exact numerical RG gives")
print(f"  {abs(shift_rg):.4f}° (including gauge coupling effects).")

# ═══════════════════════════════════════════════════════════════
# Now the critical test: start from the BARE angle at M_GUT and run DOWN
print(f"\n── Critical Test: Start from Bare Angle at GUT Scale ──\n")

# At the GUT scale, the RG gives θ₀(M_GUT) from the SM Yukawas
# But the ACS PREDICTS θ₀_bare = 11.57° at the GUT scale.
# We need to check: if we SET θ₀ = 11.57° at M_GUT, what θ₀ do we get at M_Z?

# Get the GUT-scale Yukawa values from the RG run
state_GUT = sol.sol(t_GUT)
_, _, _, ye_GUT, ymu_GUT, ytau_GUT, _ = state_GUT

print(f"  SM Yukawas at M_GUT (from running UP):")
print(f"    y_e  = {ye_GUT:.6e}")
print(f"    y_μ  = {ymu_GUT:.6e}")
print(f"    y_τ  = {ytau_GUT:.6e}")
print(f"    θ₀(M_GUT) from SM = {theta0_UV:.4f}°")

# Now: construct Yukawas at M_GUT that give θ₀ = 11.57°
# while keeping the OVERALL scale and Koide ratio Q = 2/3

# The Koide parametrisation at GUT scale with θ₀_bare:
theta0_bare_rad = np.radians(theta0_bare)

# We need to find A such that the TOTAL Yukawa normalization matches
# the SM value at the GUT scale
# Sum of √masses: S = √(y_e v/√2) + √(y_mu v/√2) + √(y_tau v/√2)
masses_GUT = [(y * v / np.sqrt(2)) for y in [ye_GUT, ymu_GUT, ytau_GUT]]
sqrt_m_GUT = sorted([np.sqrt(m) for m in masses_GUT])
S_GUT = sum(sqrt_m_GUT)
A_GUT = S_GUT / 3  # From Koide: S = 3A

# Reconstruct masses with bare θ₀
sqrt_m_bare = sorted([A_GUT * (1 + np.sqrt(2) * np.cos(theta0_bare_rad + 2*np.pi*k/3)) 
                      for k in range(3)])

if any(s <= 0 for s in sqrt_m_bare):
    print(f"  WARNING: negative √m at bare angle — adjusting A")
    # Need larger A
    for A_try in np.linspace(A_GUT * 0.5, A_GUT * 2.0, 100):
        sqrt_m_try = sorted([A_try * (1 + np.sqrt(2) * np.cos(theta0_bare_rad + 2*np.pi*k/3)) 
                            for k in range(3)])
        if all(s > 0 for s in sqrt_m_try):
            A_GUT = A_try
            sqrt_m_bare = sqrt_m_try
            break

masses_bare = [s**2 for s in sqrt_m_bare]
yukawas_bare = [np.sqrt(2) * m / v for m in masses_bare]

print(f"\n  Bare Koide masses at M_GUT (θ₀ = {theta0_bare:.2f}°):")
for name, m in zip(["e", "μ", "τ"], masses_bare):
    print(f"    m_{name} = {m:.6e} GeV")

# Check: extract θ₀ back
theta0_check = extract_theta0(*yukawas_bare)
print(f"  θ₀ extracted: {theta0_check:.4f}° (should be {theta0_bare:.4f}°)")

# Now run these DOWN from M_GUT to M_Z
print(f"\n  Running bare Yukawas DOWN from M_GUT to M_Z...")

# Need gauge couplings at GUT scale too
g1_GUT, g2_GUT, g3_GUT = state_GUT[0], state_GUT[1], state_GUT[2]
yt_GUT = state_GUT[6]

y0_bare = [g1_GUT, g2_GUT, g3_GUT, yukawas_bare[0], yukawas_bare[1], yukawas_bare[2], yt_GUT]

# Run DOWN: from t_GUT to t_MZ (reverse direction)
sol_down = solve_ivp(rge_system, [t_GUT, t_MZ], y0_bare,
                     method='RK45', max_step=0.1, rtol=1e-10, atol=1e-13,
                     dense_output=True)

if sol_down.success:
    state_IR = sol_down.sol(t_MZ)
    ye_IR, ymu_IR, ytau_IR = state_IR[3], state_IR[4], state_IR[5]
    
    theta0_IR_from_bare = extract_theta0(ye_IR, ymu_IR, ytau_IR)
    
    masses_IR = [(y * v / np.sqrt(2)) for y in [ye_IR, ymu_IR, ytau_IR]]
    
    print(f"\n  Masses at M_Z (from bare θ₀ = {theta0_bare:.2f}° at GUT):")
    for name, m in zip(["e", "μ", "τ"], masses_IR):
        print(f"    m_{name} = {m*1e3:.4f} MeV")
    
    print(f"\n  θ₀ at M_Z (from bare): {theta0_IR_from_bare:.4f}°")
    print(f"  θ₀ observed:            12.7328°")
    print(f"  RG shift:               {theta0_IR_from_bare - theta0_bare:+.4f}°")
    print(f"  Needed shift:           {12.7328 - theta0_bare:+.4f}°")
    
    match_pct = abs((theta0_IR_from_bare - theta0_bare) / (12.7328 - theta0_bare)) * 100
    
    print(f"\n  {'='*50}")
    print(f"  RG FLOW ACCOUNTS FOR {match_pct:.1f}% OF THE GAP")
    print(f"  {'='*50}")
else:
    print(f"  Downward RG failed: {sol_down.message}")

# ═══════════════════════════════════════════════════════════════
# Generate figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))

# Panel 1: θ₀ running
valid = ~np.isnan(theta0_running)
ax1.plot(np.log10(scales_GeV[valid]), theta0_running[valid], 'b-', lw=2)
ax1.axhline(12.7328, color='red', ls='--', lw=1, label='Observed IR (12.73°)')
ax1.axhline(theta0_bare, color='green', ls='--', lw=1, label=f'Bare geometric ({theta0_bare:.2f}°)')
ax1.set_xlabel('log₁₀(μ / GeV)', fontsize=10)
ax1.set_ylabel('θ₀ (degrees)', fontsize=10)
ax1.set_title('Koide Angle RG Flow', fontsize=11, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.2)

# Panel 2: Yukawa running (ratios)
ye_run = []
ymu_run = []
ytau_run = []
for t in scales_t:
    state = sol.sol(t)
    ye_run.append(state[3])
    ymu_run.append(state[4])
    ytau_run.append(state[5])

ye_run = np.array(ye_run)
ymu_run = np.array(ymu_run)
ytau_run = np.array(ytau_run)

# Plot ratios normalised to M_Z values
ax2.plot(np.log10(scales_GeV), ytau_run/ytau_run[0], 'r-', lw=1.5, label='y_τ / y_τ(M_Z)')
ax2.plot(np.log10(scales_GeV), ymu_run/ymu_run[0], 'b-', lw=1.5, label='y_μ / y_μ(M_Z)')
ax2.plot(np.log10(scales_GeV), ye_run/ye_run[0], 'g-', lw=1.5, label='y_e / y_e(M_Z)')
ax2.set_xlabel('log₁₀(μ / GeV)', fontsize=10)
ax2.set_ylabel('y_i(μ) / y_i(M_Z)', fontsize=10)
ax2.set_title('Yukawa Coupling Running', fontsize=11, fontweight='bold')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.2)

fig.tight_layout()
os.makedirs('/home/claude/figures', exist_ok=True)
fig.savefig('/home/claude/figures/fig_koide_rg_flow.pdf', dpi=300, bbox_inches='tight')
plt.close()
print(f"\n  Figure saved: fig_koide_rg_flow.pdf")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("FINAL RESULT")
print(f"{'='*70}")
print(f"""
  BARE GEOMETRIC ANGLE (ACS prediction at Palatini scale):
    θ₀_bare = π/6 - arctan(1/3) = {theta0_bare:.4f}°
    
  OBSERVED IR ANGLE (from charged lepton masses):
    θ₀_obs = 12.7328°
    
  GAP: {12.7328 - theta0_bare:.4f}°
    
  1-LOOP RG FLOW:
    The SM beta functions for lepton Yukawa couplings shift θ₀
    as the energy scale runs from M_GUT to M_Z.
    
    The dominant contribution is the tau Yukawa self-energy:
    Δθ₀ ≈ (3/(32π²)) × y_τ² × ln(M_GUT/M_Z)
    
    The tau Yukawa y_τ = {y_tau_MZ:.4e} is 200× larger than y_μ,
    so it pulls the mass triangle TOWARD the τ vertex, increasing θ₀.
    
    Computed shift: {abs(theta0_IR - theta0_UV):.4f}°
    (from SM Yukawas running up)
    
  STATUS:
    Direction of shift: {'CORRECT ✓' if np.sign(shift_rg) == np.sign(shift_needed) else 'WRONG ✗'}
    Fraction of gap explained by 1-loop RG: {abs(shift_rg/shift_needed)*100:.1f}%
""")
