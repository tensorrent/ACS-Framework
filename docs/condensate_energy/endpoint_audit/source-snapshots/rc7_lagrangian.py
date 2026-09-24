"""
Finite-Temperature Two-Field Mixing: The Loop Calculation
v1.0.0

THE QUESTION:
    Do off-diagonal (mixing) thermal corrections scale differently
    from diagonal (self-energy) corrections as a function of
    chemical potential and temperature?

THE MODEL:
    Two complex scalar fields φ₁, φ₂ with:
    - Masses m₁, m₂
    - Self-coupling λ₁₁|φ₁|⁴, λ₂₂|φ₂|⁴
    - Mixing coupling λ₁₂|φ₁|²|φ₂|²
    - Chemical potential μ for φ₁ (particle), -μ for φ₂ (antiparticle)

    L = |∂φ₁|² - m₁²|φ₁|² + |∂φ₂|² - m₂²|φ₂|²
        - λ₁₁|φ₁|⁴ - λ₂₂|φ₂|⁴ - λ₁₂|φ₁|²|φ₂|²

    At finite T, the one-loop effective potential generates
    thermal corrections to the mass matrix:

    M²_eff = ( m₁² + δm₁²(T,μ)     δm₁₂²(T,μ)    )
             ( δm₁₂²(T,μ)           m₂² + δm₂²(T,μ) )

    The thermal corrections come from:
    
    DIAGONAL (self-energy from self-coupling):
        δm₁²(T,μ) = λ₁₁ · I(m₁, T, +μ) + (λ₁₂/2) · I(m₂, T, -μ)
    
    where I(m, T, μ) = ∫ d³p/(2π)³ · n_B(E_p - μ)/(E_p)
    is the standard thermal integral with E_p = √(p² + m²).
    
    OFF-DIAGONAL (mixing from λ₁₂ vertex):
        δm₁₂²(T,μ) = λ₁₂ · J(m₁, m₂, T, μ)
    
    where J involves BOTH field propagators:
        J(m₁,m₂,T,μ) = ∫ d³p/(2π)³ · [n_B(E₁-μ) + n_B(E₂+μ)] / (E₁+E₂)
    
    (This is the sunset/bubble diagram contribution at one loop.)

    The KEY question: how do I and J scale with μ at fixed T?

NOTE ON STATISTICS:
    For bosons: n_B(x) = 1/(e^x - 1), requires μ < m for stability
    For fermions: n_F(x) = 1/(e^x + 1), μ can exceed m
    
    We compute BOTH cases.
"""

import numpy as np
import math
import time
from scipy import integrate


# ═══════════════════════════════════════════════════════════════
# THERMAL INTEGRALS
# ═══════════════════════════════════════════════════════════════

def n_bose(x):
    """Bose-Einstein distribution."""
    if x > 50: return 0.0
    if x < 0.001: return 1.0/x  # classical limit
    return 1.0 / (math.exp(x) - 1.0)


def n_fermi(x):
    """Fermi-Dirac distribution."""
    if x > 50: return 0.0
    if x < -50: return 1.0
    return 1.0 / (math.exp(x) + 1.0)


def thermal_integral_diagonal(m, T, mu, stat="fermi"):
    """
    I(m, T, μ) = ∫₀^∞ dp p² / (2π²) · n(E-μ) / E
    
    where E = √(p² + m²)
    
    This is the standard one-loop thermal correction to the
    diagonal mass term (self-energy tadpole).
    """
    if T < 1e-15:
        return 0.0
    
    n_func = n_fermi if stat == "fermi" else n_bose
    
    def integrand(p):
        E = math.sqrt(p**2 + m**2)
        arg = (E - mu) / T
        if stat == "bose" and arg < 0.001:
            return 0.0  # skip Bose condensation regime
        try:
            return p**2 / (2 * math.pi**2) * n_func(arg) / E
        except (OverflowError, ZeroDivisionError):
            return 0.0
    
    result, _ = integrate.quad(integrand, 0, 100*T + 10*m, 
                                limit=200, epsabs=1e-12)
    return result


def thermal_integral_mixing(m1, m2, T, mu, stat="fermi"):
    """
    J(m₁, m₂, T, μ) = ∫₀^∞ dp p² / (2π²) · [n(E₁-μ) + n(E₂+μ)] / (E₁+E₂)
    
    This is the one-loop thermal correction to the off-diagonal
    (mixing) mass term.
    
    Note the asymmetry: field 1 has chemical potential +μ,
    field 2 has chemical potential -μ (antiparticle convention).
    
    The mixing involves propagators of BOTH fields, so both
    occupation numbers contribute.
    """
    if T < 1e-15:
        return 0.0
    
    n_func = n_fermi if stat == "fermi" else n_bose
    
    def integrand(p):
        E1 = math.sqrt(p**2 + m1**2)
        E2 = math.sqrt(p**2 + m2**2)
        arg1 = (E1 - mu) / T
        arg2 = (E2 + mu) / T  # note: +μ for antiparticle
        
        if stat == "bose" and (arg1 < 0.001 or arg2 < 0.001):
            return 0.0
        try:
            n1 = n_func(arg1)
            n2 = n_func(arg2)
            return p**2 / (2 * math.pi**2) * (n1 + n2) / (E1 + E2)
        except (OverflowError, ZeroDivisionError):
            return 0.0
    
    result, _ = integrate.quad(integrand, 0, 100*T + 10*max(m1,m2),
                                limit=200, epsabs=1e-12)
    return result


# ═══════════════════════════════════════════════════════════════
# EFFECTIVE MASS MATRIX
# ═══════════════════════════════════════════════════════════════

def compute_mass_matrix(m1, m2, lam11, lam22, lam12, T, mu, stat="fermi"):
    """
    Compute the thermally corrected mass matrix at one loop.
    
    M²_eff = ( m₁² + δm₁²    δm₁₂²     )
             ( δm₁₂²          m₂² + δm₂² )
    
    where:
        δm₁² = λ₁₁·I(m₁,T,+μ) + (λ₁₂/2)·I(m₂,T,-μ)
        δm₂² = λ₂₂·I(m₂,T,-μ) + (λ₁₂/2)·I(m₁,T,+μ)
        δm₁₂² = λ₁₂·J(m₁,m₂,T,μ)
    """
    # Diagonal corrections
    I1_plus = thermal_integral_diagonal(m1, T, mu, stat)    # field 1 at +μ
    I2_minus = thermal_integral_diagonal(m2, T, -mu, stat)  # field 2 at -μ
    I1_minus = thermal_integral_diagonal(m1, T, -mu, stat)  # for δm₂²
    I2_plus = thermal_integral_diagonal(m2, T, mu, stat)    # for δm₂²
    
    dm1_sq = lam11 * I1_plus + (lam12/2) * I2_minus
    dm2_sq = lam22 * I2_minus + (lam12/2) * I1_plus
    
    # Off-diagonal correction
    J = thermal_integral_mixing(m1, m2, T, mu, stat)
    dm12_sq = lam12 * J
    
    M = np.array([
        [m1**2 + dm1_sq, dm12_sq],
        [dm12_sq, m2**2 + dm2_sq]
    ])
    
    return {
        "M": M,
        "dm1_sq": dm1_sq,
        "dm2_sq": dm2_sq,
        "dm12_sq": dm12_sq,
        "I1_plus": I1_plus,
        "I2_minus": I2_minus,
        "J": J,
        "det": np.linalg.det(M),
        "eigenvalues": np.linalg.eigvalsh(M),
        "diag_correction": dm1_sq,
        "offdiag_correction": dm12_sq,
    }


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 1: μ-SCALING OF DIAGONAL VS OFF-DIAGONAL
# ═══════════════════════════════════════════════════════════════

def experiment_1_mu_scaling():
    """
    THE KEY EXPERIMENT.
    
    Fix T, sweep μ. Compare how diagonal and off-diagonal
    thermal corrections scale.
    
    If off-diagonal grows faster → toy model mechanism is supported.
    If they scale the same → mechanism collapses.
    """
    print("=" * 70)
    print("EXPERIMENT 1: μ-SCALING (Fermions)")
    print("How do diagonal vs off-diagonal corrections scale with μ?")
    print("=" * 70)
    
    m1, m2 = 1.0, 1.0  # equal masses (symmetric case)
    lam11, lam22 = 0.1, 0.1
    lam12 = 0.1  # same coupling strength for fair comparison
    
    T_values = [0.5, 1.0, 2.0, 5.0]
    
    for T in T_values:
        print(f"\n  --- T = {T}, m₁ = m₂ = {m1}, λ = {lam11} ---")
        print(f"  {'μ':>6s} | {'δm₁²':>10s} | {'δm₁₂²':>10s} | "
              f"{'ratio':>8s} | {'I(+μ)':>10s} | {'J':>10s} | {'J/I ratio':>10s}")
        print(f"  {'-'*6}-+-{'-'*10}-+-{'-'*10}-+-"
              f"{'-'*8}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}")
        
        prev_dm1 = None
        prev_dm12 = None
        results = []
        
        for mu in np.linspace(0.0, 3.0, 30):
            r = compute_mass_matrix(m1, m2, lam11, lam22, lam12, T, mu, "fermi")
            
            ratio = r["dm12_sq"] / r["dm1_sq"] if abs(r["dm1_sq"]) > 1e-15 else 0
            ji_ratio = r["J"] / r["I1_plus"] if abs(r["I1_plus"]) > 1e-15 else 0
            
            results.append({
                "mu": mu, "dm1": r["dm1_sq"], "dm12": r["dm12_sq"],
                "I": r["I1_plus"], "J": r["J"], "ratio": ratio,
                "ji_ratio": ji_ratio,
            })
            
            if mu < 0.15 or mu > 2.85 or abs(mu - 1.0) < 0.06 or \
               abs(mu - 2.0) < 0.06 or abs(mu - 0.5) < 0.06:
                print(f"  {mu:6.3f} | {r['dm1_sq']:10.6f} | {r['dm12_sq']:10.6f} | "
                      f"{ratio:8.4f} | {r['I1_plus']:10.6f} | {r['J']:10.6f} | "
                      f"{ji_ratio:10.4f}")
        
        # Fit power law: correction ~ μ^α
        mus = np.array([r["mu"] for r in results if r["mu"] > 0.1])
        dm1s = np.array([abs(r["dm1"]) for r in results if r["mu"] > 0.1])
        dm12s = np.array([abs(r["dm12"]) for r in results if r["mu"] > 0.1])
        
        if len(mus) > 5 and np.min(dm1s) > 0 and np.min(dm12s) > 0:
            from scipy.stats import linregress
            log_mu = np.log(mus)
            
            slope_diag, _, r_diag, _, _ = linregress(log_mu, np.log(dm1s))
            slope_off, _, r_off, _, _ = linregress(log_mu, np.log(dm12s))
            
            print(f"\n  Power law fit (correction ~ μ^α):")
            print(f"    Diagonal:     α = {slope_diag:.4f} (R² = {r_diag**2:.4f})")
            print(f"    Off-diagonal: α = {slope_off:.4f} (R² = {r_off**2:.4f})")
            
            if abs(slope_off - slope_diag) > 0.1:
                print(f"    DIFFERENTIAL SCALING: Δα = {slope_off - slope_diag:+.4f}")
                if slope_off > slope_diag:
                    print(f"    → Off-diagonal grows FASTER with μ")
                    print(f"    → SUPPORTS toy model mechanism")
                else:
                    print(f"    → Diagonal grows FASTER with μ")
                    print(f"    → CONTRADICTS toy model mechanism")
            else:
                print(f"    SAME SCALING: Δα = {slope_off - slope_diag:+.4f}")
                print(f"    → No differential exponent")
                print(f"    → Toy model mechanism NOT supported by this Lagrangian")
        
        # More telling: ratio δm₁₂²/δm₁² as function of μ
        ratios = [r["ji_ratio"] for r in results if r["mu"] > 0.1]
        mus_r = [r["mu"] for r in results if r["mu"] > 0.1]
        
        if len(ratios) > 3:
            slope_ratio, _, r_ratio, _, _ = linregress(mus_r, ratios)
            print(f"\n  J/I ratio trend with μ:")
            print(f"    slope = {slope_ratio:+.6f}, R² = {r_ratio**2:.4f}")
            print(f"    At μ=0: J/I ≈ {ratios[0]:.4f}")
            print(f"    At μ=3: J/I ≈ {ratios[-1]:.4f}")
            if abs(slope_ratio) < 0.001:
                print(f"    → FLAT. Mixing and self-energy scale identically.")
            else:
                print(f"    → {'INCREASING' if slope_ratio > 0 else 'DECREASING'}.")


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 2: T-SCALING
# ═══════════════════════════════════════════════════════════════

def experiment_2_T_scaling():
    """
    Fix μ, sweep T. Compare scaling.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: T-SCALING (Fermions)")
    print("How do corrections scale with temperature?")
    print("=" * 70)
    
    m1, m2 = 1.0, 1.0
    lam11, lam22, lam12 = 0.1, 0.1, 0.1
    
    for mu in [0.0, 0.5, 1.0, 2.0]:
        print(f"\n  --- μ = {mu} ---")
        print(f"  {'T':>6s} | {'δm₁²':>10s} | {'δm₁₂²':>10s} | {'J/I':>8s}")
        
        for T in np.concatenate([np.linspace(0.1, 2.0, 15), 
                                  np.linspace(2.0, 10.0, 10)]):
            r = compute_mass_matrix(m1, m2, lam11, lam22, lam12, T, mu, "fermi")
            ji = r["J"]/r["I1_plus"] if abs(r["I1_plus"]) > 1e-15 else 0
            print(f"  {T:6.2f} | {r['dm1_sq']:10.6f} | {r['dm12_sq']:10.6f} | {ji:8.4f}")


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 3: MASS ASYMMETRY
# ═══════════════════════════════════════════════════════════════

def experiment_3_mass_asymmetry():
    """
    What if m₁ ≠ m₂? This is more physical — particle and
    antiparticle have different effective masses in medium.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 3: MASS ASYMMETRY (m₁ ≠ m₂)")
    print("=" * 70)
    
    lam11, lam22, lam12 = 0.1, 0.1, 0.1
    T = 1.0
    
    for m1, m2 in [(1.0, 1.0), (1.0, 1.5), (1.0, 2.0), (0.5, 2.0)]:
        print(f"\n  --- m₁={m1}, m₂={m2}, T={T} ---")
        print(f"  {'μ':>6s} | {'δm₁²':>10s} | {'δm₂²':>10s} | {'δm₁₂²':>10s} | "
              f"{'det(M)':>10s} | {'λ_min':>10s}")
        
        for mu in np.linspace(0, 3, 20):
            r = compute_mass_matrix(m1, m2, lam11, lam22, lam12, T, mu, "fermi")
            lam_min = r["eigenvalues"][0]
            print(f"  {mu:6.3f} | {r['dm1_sq']:10.6f} | {r['dm2_sq']:10.6f} | "
                  f"{r['dm12_sq']:10.6f} | {r['det']:10.4f} | {lam_min:10.6f}")
            
            if lam_min < 0:
                print(f"  *** TACHYONIC INSTABILITY at μ={mu:.3f} ***")


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 4: DETERMINANT PHASE BOUNDARY
# ═══════════════════════════════════════════════════════════════

def experiment_4_phase_boundary():
    """
    Find where det(M²_eff) = 0 in (T, μ) space.
    This is where the effective mass matrix becomes singular
    — the analog of the toy model phase boundary.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 4: PHASE BOUNDARY det(M²_eff) = 0")
    print("=" * 70)
    
    m1, m2 = 1.0, 1.0
    lam11, lam22, lam12 = 0.1, 0.1, 0.1
    
    # Scan (T, μ) space
    T_vals = np.linspace(0.1, 5.0, 40)
    mu_vals = np.linspace(0.0, 5.0, 40)
    
    det_map = np.zeros((len(T_vals), len(mu_vals)))
    lmin_map = np.zeros((len(T_vals), len(mu_vals)))
    
    print(f"\n  Computing {len(T_vals)}×{len(mu_vals)} phase diagram...")
    
    for i, T in enumerate(T_vals):
        for j, mu in enumerate(mu_vals):
            r = compute_mass_matrix(m1, m2, lam11, lam22, lam12, T, mu, "fermi")
            det_map[i, j] = r["det"]
            lmin_map[i, j] = r["eigenvalues"][0]
    
    # Find minimum eigenvalue
    min_lam = np.min(lmin_map)
    min_idx = np.unravel_index(np.argmin(lmin_map), lmin_map.shape)
    
    print(f"\n  Minimum eigenvalue: {min_lam:.6f}")
    print(f"    at T = {T_vals[min_idx[0]]:.2f}, μ = {mu_vals[min_idx[1]]:.2f}")
    
    if min_lam > 0:
        print(f"\n  Mass matrix is POSITIVE DEFINITE everywhere.")
        print(f"  No tachyonic instability in this parameter range.")
        print(f"  → This Lagrangian does NOT produce a phase transition")
        print(f"     with these coupling values.")
    else:
        # Find phase boundary
        print(f"\n  TACHYONIC REGION EXISTS!")
        tachyonic = lmin_map < 0
        print(f"  Fraction tachyonic: {np.mean(tachyonic):.1%}")
    
    # Now try stronger coupling
    print(f"\n  --- Trying stronger coupling λ₁₂ = 1.0 ---")
    lam12_strong = 1.0
    
    for i, T in enumerate(T_vals):
        for j, mu in enumerate(mu_vals):
            r = compute_mass_matrix(m1, m2, lam11, lam22, lam12_strong, T, mu, "fermi")
            det_map[i, j] = r["det"]
            lmin_map[i, j] = r["eigenvalues"][0]
    
    min_lam = np.min(lmin_map)
    min_idx = np.unravel_index(np.argmin(lmin_map), lmin_map.shape)
    
    print(f"  Minimum eigenvalue: {min_lam:.6f}")
    print(f"    at T = {T_vals[min_idx[0]]:.2f}, μ = {mu_vals[min_idx[1]]:.2f}")
    
    if min_lam > 0:
        print(f"  Still positive definite.")
    else:
        tachyonic = lmin_map < 0
        print(f"  TACHYONIC REGION EXISTS!")
        print(f"  Fraction tachyonic: {np.mean(tachyonic):.1%}")


# ═══════════════════════════════════════════════════════════════
# EXPERIMENT 5: THE ACTUAL SCALING COMPARISON
# ═══════════════════════════════════════════════════════════════

def experiment_5_raw_integral_comparison():
    """
    Strip away the coupling constants.
    Compare the RAW integrals I and J directly.
    
    If J/I is constant in μ → same scaling → toy fails.
    If J/I grows with μ → differential scaling → toy supported.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 5: RAW INTEGRAL COMPARISON I vs J")
    print("This is the definitive test.")
    print("=" * 70)
    
    m1, m2 = 1.0, 1.0
    
    for T in [0.5, 1.0, 2.0, 5.0]:
        print(f"\n  --- T = {T}, m₁ = m₂ = 1.0 (Fermions) ---")
        print(f"  {'μ':>6s} | {'I(m,T,+μ)':>12s} | {'I(m,T,-μ)':>12s} | "
              f"{'J(T,μ)':>12s} | {'J/I(+μ)':>8s} | {'I(+μ)/I(-μ)':>12s}")
        print(f"  {'-'*6}-+-{'-'*12}-+-{'-'*12}-+-{'-'*12}-+-{'-'*8}-+-{'-'*12}")
        
        I_plus_vals = []
        J_vals = []
        mus = []
        
        for mu in np.linspace(0, 4, 40):
            I_plus = thermal_integral_diagonal(m1, T, mu, "fermi")
            I_minus = thermal_integral_diagonal(m1, T, -mu, "fermi")
            J = thermal_integral_mixing(m1, m2, T, mu, "fermi")
            
            ji = J / I_plus if I_plus > 1e-15 else 0
            ii = I_plus / I_minus if I_minus > 1e-15 else float('inf')
            
            mus.append(mu)
            I_plus_vals.append(I_plus)
            J_vals.append(J)
            
            if mu < 0.15 or mu > 3.8 or abs(mu - 1.0) < 0.12 or \
               abs(mu - 2.0) < 0.12 or abs(mu - 3.0) < 0.12:
                print(f"  {mu:6.3f} | {I_plus:12.8f} | {I_minus:12.8f} | "
                      f"{J:12.8f} | {ji:8.4f} | {ii:12.4f}")
        
        # Fit log-log scaling
        mus_fit = np.array([m for m in mus if m > 0.2])
        I_fit = np.array([I_plus_vals[i] for i, m in enumerate(mus) if m > 0.2])
        J_fit = np.array([J_vals[i] for i, m in enumerate(mus) if m > 0.2])
        
        if len(mus_fit) > 5 and np.min(I_fit) > 0 and np.min(J_fit) > 0:
            from scipy.stats import linregress
            
            # Fit in high-μ regime (μ > m)
            high_mu = mus_fit > 1.5
            if np.sum(high_mu) > 3:
                sl_I, _, r_I, _, _ = linregress(np.log(mus_fit[high_mu]), 
                                                  np.log(I_fit[high_mu]))
                sl_J, _, r_J, _, _ = linregress(np.log(mus_fit[high_mu]), 
                                                  np.log(J_fit[high_mu]))
                
                print(f"\n  High-μ scaling (μ > 1.5):")
                print(f"    I(+μ) ~ μ^{sl_I:.4f} (R² = {r_I**2:.4f})")
                print(f"    J(μ)  ~ μ^{sl_J:.4f} (R² = {r_J**2:.4f})")
                print(f"    Δ(exponent) = {sl_J - sl_I:+.4f}")
                
                if abs(sl_J - sl_I) < 0.05:
                    print(f"    → SAME SCALING")
                elif sl_J > sl_I:
                    print(f"    → OFF-DIAGONAL GROWS FASTER")
                else:
                    print(f"    → DIAGONAL GROWS FASTER")
        
        # Also: J/I ratio trend
        ji_ratios = [J_vals[i]/I_plus_vals[i] if I_plus_vals[i] > 1e-15 else 0 
                     for i in range(len(mus))]
        valid = [(mus[i], ji_ratios[i]) for i in range(len(mus)) 
                 if mus[i] > 0.2 and ji_ratios[i] > 0]
        if len(valid) > 5:
            vm, vr = zip(*valid)
            sl, _, rr, _, _ = linregress(vm, vr)
            print(f"\n  J/I ratio vs μ:")
            print(f"    slope = {sl:+.6f}")
            print(f"    J/I at μ=0.5: {vr[0]:.4f}")
            print(f"    J/I at μ=max: {vr[-1]:.4f}")
            print(f"    {'CONSTANT (same scaling)' if abs(sl) < 0.005 else 'VARIES (differential scaling)'}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    t0 = time.time()
    
    print("=" * 70)
    print("FINITE-TEMPERATURE TWO-FIELD MIXING: THE LOOP CALCULATION")
    print("=" * 70)
    print()
    print("Question: Do off-diagonal thermal corrections scale")
    print("differently from diagonal corrections with μ?")
    print()
    print("If yes → toy model mechanism has QFT support")
    print("If no  → toy model mechanism is an artifact of chosen exponents")
    print()
    
    experiment_1_mu_scaling()
    experiment_2_T_scaling()
    experiment_3_mass_asymmetry()
    experiment_4_phase_boundary()
    experiment_5_raw_integral_comparison()
    
    # ─── VERDICT ─────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")
    print("""
The one-loop thermal integrals I (diagonal) and J (off-diagonal)
have been computed numerically for the minimal two-scalar Lagrangian.

The results above show whether off-diagonal corrections scale
differently from diagonal corrections as a function of chemical
potential μ.

If J/I is constant → corrections scale identically.
    The toy model's differential exponent is NOT produced
    by this Lagrangian. The mechanism is an artifact of the
    polynomial ansatz, not a QFT prediction.

If J/I varies → there IS differential scaling.
    The specific direction (increasing or decreasing) determines
    whether the toy model's phase boundary is physically supported.
""")
    
    print(f"Total time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
