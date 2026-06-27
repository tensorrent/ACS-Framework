#!/usr/bin/env python3
"""
2-QUBIT QUANTUM ACS: Non-trivial steady state version
The key: use ASYMMETRIC dissipation rates + non-commuting Lindblad ops
so the steady state has genuine correlations and asymmetric info flow.
"""
import numpy as np
from numpy.linalg import norm, eigvalsh
from scipy.linalg import expm
import os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTDIR = "/home/claude/figures"
os.makedirs(OUTDIR, exist_ok=True)

I2 = np.eye(2, dtype=complex)
sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)
sp = np.array([[0,1],[0,0]], dtype=complex)  # raising
sm = np.array([[0,0],[1,0]], dtype=complex)  # lowering

print("=" * 70)
print("2-QUBIT QUANTUM ACS")
print("=" * 70)

# Asymmetric coupling operators
V_f = np.kron(sz, sx) + 0.3 * np.kron(sy, sz)
V_g = np.kron(sx, sz) + 0.5 * np.kron(sz, sy)
bracket = V_f @ V_g - V_g @ V_f
print(f"  ||[V_f, V_g]|| = {norm(bracket):.4f} (non-zero ✓)")

# Asymmetric Lindblad: A decays faster than B, with DIFFERENT channels
# This breaks the symmetry and creates a non-maximally-mixed steady state
L_ops = [
    0.5 * np.kron(sm, I2),         # A decays (strong)
    0.15 * np.kron(I2, sm),        # B decays (weak)
    0.2 * np.kron(sp, sm),         # A excites when B decays (correlation)
    0.1 * np.kron(sz, sx),         # entangling dephasing
]

def lindblad_evolve(H, rho, dt=0.005, n_steps=8000):
    for _ in range(n_steps):
        drho = -1j * (H @ rho - rho @ H)
        for L in L_ops:
            Ld = L.conj().T
            drho += L @ rho @ Ld - 0.5*(Ld@L@rho + rho@Ld@L)
        rho = rho + dt * drho
        rho = (rho + rho.conj().T) / 2
        rho /= np.trace(rho).real
    return rho

def ptr_B(rho):
    r = np.zeros((2,2), dtype=complex)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                r[i,j] += rho[i*2+k, j*2+k]
    return r

def ptr_A(rho):
    r = np.zeros((2,2), dtype=complex)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                r[i,j] += rho[k*2+i, k*2+j]
    return r

def S(rho):
    ev = eigvalsh(rho); ev = ev[ev > 1e-15]
    return -np.sum(ev * np.log2(ev))

def MI(rho):
    return S(ptr_B(rho)) + S(ptr_A(rho)) - S(rho)

# Compute quantum ΔI via DIRECTIONAL information flow
# Method: measure how much subsystem B learns about A vs vice versa
# by comparing the state after A-driven vs B-driven evolution

H_0 = 0.5*(np.kron(sz, I2) + np.kron(I2, sz))

epsilons = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]
DI_vals = []
purity_vals = []

print(f"\n  {'eps':<6} {'Purity':<8} {'S_A':<8} {'S_B':<8} {'MI':<8} {'DI_Q':<10}")
print(f"  {'-'*52}")

for eps in epsilons:
    H = H_0 + eps * V_f + eps * 0.6 * V_g
    rho0 = np.eye(4, dtype=complex) / 4
    rho_ss = lindblad_evolve(H, rho0)
    
    pur = np.real(np.trace(rho_ss @ rho_ss))
    sa = S(ptr_B(rho_ss))
    sb = S(ptr_A(rho_ss))
    mi = MI(rho_ss)
    purity_vals.append(pur)
    
    # Directional info flow: evolve small time under asymmetric parts
    dt_p = 0.15
    # Form→Function channel only
    H_fg = H_0 + eps * V_f
    rho_fg = expm(-1j*H_fg*dt_p) @ rho_ss @ expm(1j*H_fg*dt_p)
    rho_fg = (rho_fg + rho_fg.conj().T)/2; rho_fg /= np.trace(rho_fg).real
    
    # Function→Form channel only
    H_gf = H_0 + eps * 0.6 * V_g
    rho_gf = expm(-1j*H_gf*dt_p) @ rho_ss @ expm(1j*H_gf*dt_p)
    rho_gf = (rho_gf + rho_gf.conj().T)/2; rho_gf /= np.trace(rho_gf).real
    
    # ΔI = change in B's entropy under A-drive minus change in A's entropy under B-drive
    dS_B_from_A = S(ptr_A(rho_fg)) - sb  # B changes when A drives
    dS_A_from_B = S(ptr_B(rho_gf)) - sa  # A changes when B drives
    DI_Q = dS_B_from_A - dS_A_from_B
    DI_vals.append(DI_Q)
    
    print(f"  {eps:<6.2f} {pur:<8.4f} {sa:<8.4f} {sb:<8.4f} {mi:<8.4f} {DI_Q:<+10.6f}")

# Fit
eps_a = np.array(epsilons)
DI_a = np.array(DI_vals)
mask = eps_a > 0.01
if np.sum(mask) >= 4:
    c = np.polyfit(eps_a[mask], DI_a[mask], 3)
    print(f"\n  Fit: DI_Q ≈ {c[2]:.4f}·ε + {c[1]:.4f}·ε² + {c[0]:.4f}·ε³")
    print(f"  ||[V_f,V_g]|| = {norm(bracket):.4f}")
    
    a1_nz = abs(c[2]) > 1e-4
    a2_nz = abs(c[1]) > 1e-4
    di_grows = abs(DI_vals[-1]) > abs(DI_vals[1]) if len(DI_vals) > 1 else False
    
    print(f"\n  Results:")
    print(f"    DI_Q(0) = 0:        {'YES ✓' if abs(DI_vals[0]) < 0.001 else 'NO'}")
    print(f"    α₁ (1st order) ≠ 0: {'YES ✓' if a1_nz else 'NO ✗'}")
    print(f"    α₂ (2nd order) ≠ 0: {'YES ✓' if a2_nz else 'NO ✗'}")
    print(f"    DI_Q grows with ε:  {'YES ✓' if di_grows else 'NO ✗'}")
    print(f"    Purity < 1:         {'YES ✓' if purity_vals[-1] < 0.9 else 'NO (maximally mixed)'}")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 2.8))
    ax1.plot(epsilons, DI_vals, 'o-', color='#CC0000', markersize=5, lw=1.5, label='Data')
    ef = np.linspace(0, 2, 100)
    ax1.plot(ef, np.polyval(c, ef), '--', color='#0044CC', lw=1, label='Cubic fit')
    ax1.axhline(0, color='gray', lw=0.5, ls='--')
    ax1.set_xlabel('$\\varepsilon$', fontsize=10)
    ax1.set_ylabel('$\\Delta\\mathcal{I}_Q$', fontsize=10)
    ax1.set_title('Quantum $\\Delta\\mathcal{I}$ vs coupling', fontsize=10, fontweight='bold')
    ax1.legend(fontsize=7); ax1.grid(True, alpha=0.2)
    
    ax2.plot(epsilons, purity_vals, 's-', color='#008800', markersize=5, lw=1.5)
    ax2.axhline(0.25, color='gray', lw=0.5, ls='--', label='Max mixed')
    ax2.set_xlabel('$\\varepsilon$', fontsize=10)
    ax2.set_ylabel('Tr$(\\rho^2)$', fontsize=10)
    ax2.set_title('Purity of steady state', fontsize=10, fontweight='bold')
    ax2.legend(fontsize=7); ax2.grid(True, alpha=0.2)
    
    fig.tight_layout()
    fig.savefig(f'{OUTDIR}/fig_quantum_acs.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\n  Figure saved: fig_quantum_acs.pdf")

print(f"\n{'='*70}")
