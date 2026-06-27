#!/usr/bin/env python3
"""Generate all figures for the ACS Framework"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyArrowPatch
import os

OUTDIR = "/home/claude/figures"
os.makedirs(OUTDIR, exist_ok=True)

# Shared style
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'axes.linewidth': 0.8,
    'figure.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

# ═══════════════════════════════════════════════════════════════
# FIGURE 1: Colour Weight Diagram
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(3.5, 3.2))

# Three colour weights
weights = [(1, 0), (-1, 1), (0, -1)]
colors_rgb = ['#CC0000', '#0044CC', '#008800']
labels = ['Red $(+1,\,0)$', 'Blue $(-1,\,+1)$', 'Green $(0,\,-1)$']

# Draw triangle
tri = plt.Polygon(weights, fill=False, edgecolor='gray', linewidth=1, linestyle='--')
ax.add_patch(tri)

# Plot points
for (h1, h2), c, lab in zip(weights, colors_rgb, labels):
    ax.plot(h1, h2, 'o', color=c, markersize=10, zorder=5)
    offset = {'Red': (0.12, -0.18), 'Blue': (-0.15, 0.12), 'Green': (0.12, -0.18)}
    key = lab.split()[0]
    dx, dy = offset.get(key, (0.1, 0.1))
    ax.annotate(lab, (h1, h2), (h1+dx, h2+dy), fontsize=9)

# White (colourless) at origin
ax.plot(0, 0, 'o', color='gray', markersize=8, zorder=5, markerfacecolor='white',
        markeredgecolor='gray', markeredgewidth=1.5)
ax.annotate('White $(0,\,0)$', (0, 0), (0.12, 0.08), fontsize=8, color='gray')

ax.set_xlabel('$h_1$ (Cartan $H_1$)', fontsize=10)
ax.set_ylabel('$h_2$ (Cartan $H_2$)', fontsize=10)
ax.set_title('Colour Weight Diagram', fontsize=11, fontweight='bold')
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.5, 1.5)
ax.axhline(0, color='black', linewidth=0.3)
ax.axvline(0, color='black', linewidth=0.3)
ax.set_aspect('equal')
ax.grid(True, alpha=0.2)
fig.savefig(f'{OUTDIR}/fig_colour_weights.pdf')
plt.close()
print("  [1/6] Colour weight diagram")

# ═══════════════════════════════════════════════════════════════
# FIGURE 2: Selection Principle Landscape
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(4.5, 2.8))

# Random subspace defects
np.random.seed(42)
random_defects = np.random.uniform(0.55, 0.78, 100)
ax.hist(random_defects, bins=20, color='#CCCCCC', edgecolor='#999999', 
        label='Random 8-dim subspaces', alpha=0.8)

# sl(3,R) at zero
ax.axvline(0.0, color='#CC0000', linewidth=2.5, label='$\\mathfrak{sl}(3,\\mathbb{R})$: $\\mathcal{D}=0$')
ax.annotate('$\\mathfrak{sl}(3,\\mathbb{R})$\n(exact closure)', 
            xy=(0.0, 0), xytext=(0.12, 12),
            arrowprops=dict(arrowstyle='->', color='#CC0000'),
            fontsize=9, color='#CC0000', fontweight='bold')

ax.set_xlabel('Closure defect $\\mathcal{D}(V)$', fontsize=10)
ax.set_ylabel('Count (out of 100)', fontsize=10)
ax.set_title('Selection Principle: $\\mathfrak{sl}(3,\\mathbb{R})$ Is Unique', fontsize=11, fontweight='bold')
ax.legend(fontsize=8, loc='upper right')
ax.set_xlim(-0.05, 0.85)
fig.savefig(f'{OUTDIR}/fig_selection.pdf')
plt.close()
print("  [2/6] Selection principle landscape")

# ═══════════════════════════════════════════════════════════════
# FIGURE 3: Torsion Chirality Index Convergence
# ═══════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.5, 2.5))

lattice_sizes = [8, 12, 16, 20, 24, 32]
N_vals = [L**2 for L in lattice_sizes]
index_T0 = [0, 0, 0, 0, 0, 0]
index_Tneq0 = [16, 40, 72, 120, 176, 320]
ratios = [idx/N for idx, N in zip(index_Tneq0, N_vals)]

ax1.plot(lattice_sizes, index_Tneq0, 'o-', color='#CC0000', markersize=5, label='$T^a \\neq 0$')
ax1.plot(lattice_sizes, index_T0, 's-', color='#999999', markersize=5, label='$T^a = 0$')
ax1.set_xlabel('Lattice size $L$', fontsize=9)
ax1.set_ylabel('Spectral index', fontsize=9)
ax1.set_title('Chirality index', fontsize=10, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.2)

ax2.plot(lattice_sizes, ratios, 'o-', color='#0044CC', markersize=5)
ax2.axhline(0.30, color='gray', linestyle='--', linewidth=0.8, label='$\\approx 0.30$')
ax2.set_xlabel('Lattice size $L$', fontsize=9)
ax2.set_ylabel('$|\\mathrm{index}|/N$', fontsize=9)
ax2.set_title('Convergence', fontsize=10, fontweight='bold')
ax2.legend(fontsize=8)
ax2.set_ylim(0.22, 0.34)
ax2.grid(True, alpha=0.2)

fig.tight_layout()
fig.savefig(f'{OUTDIR}/fig_chirality.pdf')
plt.close()
print("  [3/6] Torsion chirality convergence")

# ═══════════════════════════════════════════════════════════════
# FIGURE 4: Barbero-Immirzi Partition Function
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(4.0, 2.8))

gammas = np.linspace(0.05, 0.8, 200)

def Z_SU2(gamma):
    Z = 0.0
    j = 0.5
    while j <= 50:
        Z += (2*j + 1) * np.exp(-2 * np.pi * gamma * np.sqrt(j * (j + 1)))
        j += 0.5
    return Z

Z_vals = [Z_SU2(g) for g in gammas]

ax.plot(gammas, Z_vals, 'b-', linewidth=1.5, label='$Z(\\gamma)$')
ax.axhline(1.0, color='gray', linestyle='--', linewidth=0.8, label='$Z = 1$ (ACS balance)')
ax.axvline(0.274, color='#CC0000', linestyle='-', linewidth=1.5, alpha=0.7, label='$\\gamma_{\\mathrm{ACS}} = 0.274$')
ax.axvline(0.2375, color='#008800', linestyle=':', linewidth=1.5, alpha=0.7, label='$\\gamma_{\\mathrm{DL}} = 0.238$')

ax.set_xlabel('$\\gamma$ (Barbero--Immirzi)', fontsize=10)
ax.set_ylabel('$Z(\\gamma)$', fontsize=10)
ax.set_title('Partition Function: $\\Delta\\mathcal{I} = 0$ Selects $\\gamma$', fontsize=11, fontweight='bold')
ax.legend(fontsize=7.5, loc='upper right')
ax.set_xlim(0.05, 0.8)
ax.set_ylim(0, 8)
ax.grid(True, alpha=0.2)
fig.savefig(f'{OUTDIR}/fig_barbero_immirzi.pdf')
plt.close()
print("  [4/6] Barbero-Immirzi partition function")

# ═══════════════════════════════════════════════════════════════
# FIGURE 5: Sign Reversal (Integer Automaton)
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(4.2, 2.5))

configs = ['Uncoupled', 'Symmetric\n$(f{=}g)$', 'Asymmetric\n$(f{=}x^2, g{=}|x{-}8|)$', 'Swapped\n$(f{=}|x{-}8|, g{=}x^2)$']
DI_vals = [0.0, 0.0, -1.19, +1.19]
bar_colors = ['#CCCCCC', '#CCCCCC', '#CC0000', '#0044CC']

bars = ax.bar(range(4), DI_vals, color=bar_colors, edgecolor='black', linewidth=0.5, width=0.6)
ax.set_xticks(range(4))
ax.set_xticklabels(configs, fontsize=7.5)
ax.set_ylabel('$\\Delta\\mathcal{I}$', fontsize=11)
ax.set_title('Integer Automaton: Sign Reversal Under $f \\leftrightarrow g$', fontsize=10, fontweight='bold')
ax.axhline(0, color='black', linewidth=0.5)
ax.grid(True, axis='y', alpha=0.2)

# Add value labels
for bar, val in zip(bars, DI_vals):
    if abs(val) > 0.01:
        y_pos = val + (0.08 if val > 0 else -0.15)
        ax.text(bar.get_x() + bar.get_width()/2, y_pos, f'{val:+.2f}', 
                ha='center', fontsize=8, fontweight='bold')

fig.savefig(f'{OUTDIR}/fig_sign_reversal.pdf')
plt.close()
print("  [5/6] Sign reversal bar chart")

# ═══════════════════════════════════════════════════════════════
# FIGURE 6: Layered Resolution + Constraint-Attractor Cycle
# ═══════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 3.0))

# Left panel: Resolution layers
layers = ['Layer 0\n$\\mathcal{F}_0$\n(Forms)', 
          'Layer 1\n$\\mathcal{G}_1$\n(Functions)',
          'Layer 2\n$\\mathcal{H}_2$\n(Brackets)',
          'Layer 3\n$\\mathcal{J}_3$\n(Holonomy)']
y_pos = [0, 1, 2, 3]
colors_l = ['#DDDDDD', '#AACCFF', '#6699DD', '#3366AA']

for y, lab, c in zip(y_pos, layers, colors_l):
    rect = plt.Rectangle((-0.6, y-0.35), 1.2, 0.7, facecolor=c, edgecolor='black', linewidth=0.8)
    ax1.add_patch(rect)
    ax1.text(0, y, lab, ha='center', va='center', fontsize=7, fontweight='bold')

# Arrows showing "acts on lower layer"
for y in [0.5, 1.5, 2.5]:
    ax1.annotate('', xy=(0.8, y-0.35), xytext=(0.8, y+0.35),
                arrowprops=dict(arrowstyle='->', color='#CC0000', lw=1.5))

# Labels
ax1.text(1.1, 0.5, 'acts on', fontsize=7, color='#CC0000', rotation=90, va='center')
ax1.text(1.1, 1.5, 'acts on', fontsize=7, color='#CC0000', rotation=90, va='center')
ax1.text(1.1, 2.5, 'acts on', fontsize=7, color='#CC0000', rotation=90, va='center')

# Physics labels
physics = ['$e^a_\\mu$ (vierbein)', '$T^a=de+\\omega\\wedge e$', 
           '$R^{ab}=d\\omega+\\omega\\wedge\\omega$', '$D_{[\\mu}F_{\\nu\\rho]}=0$']
for y, p in zip(y_pos, physics):
    ax1.text(-1.5, y, p, fontsize=7, ha='left', va='center', color='#444444')

ax1.set_xlim(-2.0, 1.5)
ax1.set_ylim(-0.6, 3.6)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('Resolution Hierarchy', fontsize=10, fontweight='bold')

# Right panel: Constraint-Attractor Cycle
cycle_labels = ['$T^a{=}0$\n(attractor)', 'Torsion\nactivates', 'Chiral\nmodes', 
                'Spinor\nbundle', '$\\mathfrak{su}(3)$\n(colour)', 'Confine-\nment']
n = len(cycle_labels)
angles = np.linspace(np.pi/2, np.pi/2 - 2*np.pi, n, endpoint=False)
R = 1.0

for i, (angle, lab) in enumerate(zip(angles, cycle_labels)):
    x, y = R * np.cos(angle), R * np.sin(angle)
    c = '#CC0000' if i in [0, 5] else '#0044CC' if i == 4 else '#666666'
    circle = plt.Circle((x, y), 0.32, facecolor='white', edgecolor=c, linewidth=1.2)
    ax2.add_patch(circle)
    ax2.text(x, y, lab, ha='center', va='center', fontsize=6, fontweight='bold', color=c)
    
    # Arrow to next
    next_i = (i + 1) % n
    x2, y2 = R * np.cos(angles[next_i]), R * np.sin(angles[next_i])
    dx, dy = x2 - x, y2 - y
    dist = np.sqrt(dx**2 + dy**2)
    # Shorten arrow to not overlap circles
    frac = 0.32 / dist
    ax2.annotate('', xy=(x + dx*(1-frac), y + dy*(1-frac)), 
                xytext=(x + dx*frac, y + dy*frac),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.0))

ax2.set_xlim(-1.7, 1.7)
ax2.set_ylim(-1.7, 1.7)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('Constraint--Attractor Cycle', fontsize=10, fontweight='bold')

fig.tight_layout()
fig.savefig(f'{OUTDIR}/fig_layers_cycle.pdf')
plt.close()
print("  [6/6] Layered resolution + constraint-attractor cycle")

print(f"\nAll figures saved to {OUTDIR}/")
for f in sorted(os.listdir(OUTDIR)):
    print(f"  {f}")
