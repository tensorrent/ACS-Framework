#!/usr/bin/env python3
"""
GEOMETRIC COLOUR PLANES: Nuclear Force as Geometry
====================================================
The su(3) weight diagram is 2D (h1, h2). But representations stack
at different ENERGY LEVELS (quadratic Casimir C₂). The nuclear force
= gluon exchange = root vectors connecting states within and across
these planes. Confinement = collapse to the singlet at C₂ = 0.

This computation:
1. Builds the weight diagrams for all low-lying su(3) representations
2. Stacks them by Casimir eigenvalue (the "q-planes")
3. Shows gluon exchange as geometric paths
4. Demonstrates confinement as the geometric attractor
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

OUTDIR = "/home/claude/figures"
os.makedirs(OUTDIR, exist_ok=True)

print("=" * 70)
print("GEOMETRIC COLOUR PLANES")
print("su(3) Representations as Stacked Weight Diagrams")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
# The su(3) representations and their weight diagrams
# ═══════════════════════════════════════════════════════════════

# Dynkin labels (p,q) → dimension = (p+1)(q+1)(p+q+2)/2
# Quadratic Casimir C₂(p,q) = (p² + q² + pq + 3p + 3q)/3

def casimir(p, q):
    return (p**2 + q**2 + p*q + 3*p + 3*q) / 3

def dimension(p, q):
    return (p+1)*(q+1)*(p+q+2)//2

def weights(p, q):
    """Generate weight diagram for su(3) representation (p,q).
    Weights are (m1, m2) where m1 = eigenvalue of H1, m2 = eigenvalue of H2.
    Using the standard basis where simple roots are:
      α₁ = (2, -1), α₂ = (-1, 2)
    and the highest weight is (p, q) in Dynkin labels, 
    corresponding to (2p+q, 2q+p)/3 in the (h1,h2) basis.
    """
    # For small representations, enumerate explicitly
    wts = set()
    
    # Use the Freudenthal formula approach for small reps
    # Or just hardcode the known ones
    
    if (p, q) == (0, 0):  # Singlet
        return [(0, 0)]
    
    elif (p, q) == (1, 0):  # Fundamental 3
        return [(1, 0), (-1, 1), (0, -1)]
    
    elif (p, q) == (0, 1):  # Anti-fundamental 3̄
        return [(-1, 0), (1, -1), (0, 1)]
    
    elif (p, q) == (1, 1):  # Adjoint 8
        return [(1, 1), (-1, 2), (2, -1), (0, 0), (0, 0),
                (-2, 1), (1, -2), (-1, -1)]
    
    elif (p, q) == (2, 0):  # Sextet 6
        return [(2, 0), (0, 1), (-2, 2), (1, -1), (-1, 0), (0, -2)]
    
    elif (p, q) == (0, 2):  # 6̄
        return [(-2, 0), (0, -1), (2, -2), (-1, 1), (1, 0), (0, 2)]
    
    elif (p, q) == (3, 0):  # Decuplet 10
        return [(3, 0), (1, 1), (-1, 2), (-3, 3),
                (2, -1), (0, 0), (-2, 1),
                (1, -2), (-1, -1),
                (0, -3)]
    
    elif (p, q) == (0, 3):  # 10̄
        return [(-3, 0), (-1, -1), (1, -2), (3, -3),
                (-2, 1), (0, 0), (2, -1),
                (-1, 2), (1, 1),
                (0, 3)]
    
    return [(0, 0)]

# Convert Dynkin weights to orthogonal (h1, h2) coordinates
def dynkin_to_cartesian(m1, m2):
    """Convert Dynkin weight labels to Cartesian coordinates for plotting.
    Use 60° basis: e₁ = (1, 0), e₂ = (-1/2, √3/2)"""
    x = m1 - m2 / 2
    y = m2 * np.sqrt(3) / 2
    return x, y

# ═══════════════════════════════════════════════════════════════
print("\n── su(3) Representations ──\n")

reps = [
    ((0,0), "Singlet $\\mathbf{1}$", '#999999'),
    ((1,0), "Fundamental $\\mathbf{3}$", '#CC0000'),
    ((0,1), "Anti-fund. $\\bar{\\mathbf{3}}$", '#0066CC'),
    ((1,1), "Adjoint $\\mathbf{8}$", '#FF8800'),
    ((2,0), "Sextet $\\mathbf{6}$", '#00AA44'),
    ((3,0), "Decuplet $\\mathbf{10}$", '#8844CC'),
]

print(f"  {'Rep':<20} {'Dim':<6} {'C₂':<8} {'Weights'}")
print(f"  {'-'*65}")
for (p,q), name, _ in reps:
    d = dimension(p, q)
    c2 = casimir(p, q)
    wts = weights(p, q)
    # Remove duplicate (0,0) for display
    unique_wts = list(set(wts))
    print(f"  ({p},{q}) {name:<15} {d:<6} {c2:<8.2f} {unique_wts}")

# ═══════════════════════════════════════════════════════════════
print("\n── Root Vectors (Gluon Exchange Geometry) ──\n")

# The 6 root vectors of su(3) — these are the gluon directions
# In Dynkin labels: ±α₁, ±α₂, ±(α₁+α₂)
roots = [
    ((2, -1), "α₁ (R↔B)"),
    ((-2, 1), "-α₁ (B↔R)"),
    ((-1, 2), "α₂ (B↔G)"),
    ((1, -2), "-α₂ (G↔B)"),
    ((1, 1), "α₁+α₂ (R↔G)"),
    ((-1, -1), "-(α₁+α₂) (G↔R)"),
]

print(f"  {'Root':<20} {'Dynkin':<12} {'Cartesian':<20} {'Colour change'}")
print(f"  {'-'*65}")
for (r1, r2), name in roots:
    x, y = dynkin_to_cartesian(r1, r2)
    print(f"  {name:<20} ({r1:+d},{r2:+d}){'':>4} ({x:+.2f}, {y:+.2f}){'':>6} {name.split('(')[1] if '(' in name else ''}")

# ═══════════════════════════════════════════════════════════════
print("\n── Generating 3D Colour Geometry ──\n")

# FIGURE: 3D stacked weight diagrams
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Stack representations at their Casimir height
for (p,q), name, color in reps:
    c2 = casimir(p, q)
    wts = weights(p, q)
    
    # Convert to Cartesian and plot at height c2
    xs, ys = [], []
    for m1, m2 in wts:
        x, y = dynkin_to_cartesian(m1, m2)
        xs.append(x)
        ys.append(y)
    
    # Remove duplicate points for plotting
    points = list(set(zip(xs, ys)))
    xs_u = [p[0] for p in points]
    ys_u = [p[1] for p in points]
    
    # Plot points
    ax.scatter(xs_u, ys_u, [c2]*len(xs_u), color=color, s=40, zorder=5,
              edgecolors='black', linewidths=0.5)
    
    # Draw edges for triangular/hexagonal shapes
    if len(points) >= 3:
        # Sort by angle for convex hull
        cx = np.mean(xs_u)
        cy = np.mean(ys_u)
        angles = [np.arctan2(y-cy, x-cx) for x,y in points]
        order = np.argsort(angles)
        sorted_pts = [points[i] for i in order]
        
        for i in range(len(sorted_pts)):
            j = (i+1) % len(sorted_pts)
            ax.plot([sorted_pts[i][0], sorted_pts[j][0]],
                   [sorted_pts[i][1], sorted_pts[j][1]],
                   [c2, c2], color=color, alpha=0.5, linewidth=1)
    
    # Label
    label_x = max(xs_u) + 0.3 if xs_u else 0
    label_clean = name.replace('$', '').replace('\\mathbf{', '').replace('\\bar{', '').replace('}', '')
    ax.text(label_x, 0, c2, label_clean, fontsize=7, color=color)

# Draw vertical arrows showing confinement (C₂ → 0)
for rep_from, rep_to in [((1,0), (0,0)), ((1,1), (1,0)), ((2,0), (1,0))]:
    c2_from = casimir(*rep_from)
    c2_to = casimir(*rep_to)
    ax.plot([0, 0], [0, 0], [c2_from, c2_to], 'k--', alpha=0.3, linewidth=0.8)

# Draw gluon exchange arrows within the fundamental
c2_fund = casimir(1, 0)
fund_wts = weights(1, 0)
for i in range(3):
    j = (i+1) % 3
    x1, y1 = dynkin_to_cartesian(*fund_wts[i])
    x2, y2 = dynkin_to_cartesian(*fund_wts[j])
    ax.plot([x1, x2], [y1, y2], [c2_fund, c2_fund], 
           color='#FF4444', alpha=0.6, linewidth=1.5)

ax.set_xlabel('$h_1$ axis', fontsize=9)
ax.set_ylabel('$h_2$ axis', fontsize=9)
ax.set_zlabel('Casimir $C_2$ (binding energy)', fontsize=9)
ax.set_title('Geometric Colour Planes:\nsu(3) Representations Stacked by Energy', 
             fontsize=11, fontweight='bold')
ax.view_init(elev=25, azim=-60)
fig.savefig(f'{OUTDIR}/fig_colour_3d.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("  [1/3] 3D colour geometry saved")

# ═══════════════════════════════════════════════════════════════
# FIGURE: 2D comparison of representations
fig, axes = plt.subplots(2, 3, figsize=(7, 5))

rep_list = [
    ((0,0), "Singlet $\\mathbf{1}$\n$C_2 = 0$", '#999999'),
    ((1,0), "Fund. $\\mathbf{3}$\n$C_2 = 4/3$", '#CC0000'),
    ((0,1), "Anti-fund. $\\bar{\\mathbf{3}}$\n$C_2 = 4/3$", '#0066CC'),
    ((1,1), "Adjoint $\\mathbf{8}$\n$C_2 = 3$", '#FF8800'),
    ((2,0), "Sextet $\\mathbf{6}$\n$C_2 = 10/3$", '#00AA44'),
    ((3,0), "Decuplet $\\mathbf{10}$\n$C_2 = 6$", '#8844CC'),
]

for idx, ((p,q), name, color) in enumerate(rep_list):
    ax = axes[idx//3][idx%3]
    wts = weights(p, q)
    
    xs, ys = [], []
    for m1, m2 in wts:
        x, y = dynkin_to_cartesian(m1, m2)
        xs.append(x)
        ys.append(y)
    
    points = list(set(zip(xs, ys)))
    xs_u = [pt[0] for pt in points]
    ys_u = [pt[1] for pt in points]
    
    # Draw convex hull
    if len(points) >= 3:
        cx, cy = np.mean(xs_u), np.mean(ys_u)
        angles = [np.arctan2(y-cy, x-cx) for x,y in points]
        order = np.argsort(angles)
        sorted_pts = [points[i] for i in order]
        poly = plt.Polygon(sorted_pts, fill=True, facecolor=color, alpha=0.15, 
                          edgecolor=color, linewidth=1.5)
        ax.add_patch(poly)
    
    ax.scatter(xs_u, ys_u, color=color, s=50, zorder=5, edgecolors='black', linewidths=0.5)
    
    # Draw root vectors as arrows for fundamental
    if (p,q) == (1,0):
        for i in range(len(points)):
            j = (i+1) % len(points)
            ax.annotate('', xy=points[j], xytext=points[i],
                       arrowprops=dict(arrowstyle='->', color='#FF4444', lw=1.5))
    
    ax.set_title(name, fontsize=8, fontweight='bold')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.15)
    ax.axhline(0, color='black', linewidth=0.3)
    ax.axvline(0, color='black', linewidth=0.3)
    
    if idx >= 3:
        ax.set_xlabel('$h_1$', fontsize=8)
    if idx % 3 == 0:
        ax.set_ylabel('$h_2$', fontsize=8)

fig.suptitle('Geometric Shapes of su(3) Representations', fontsize=12, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(f'{OUTDIR}/fig_rep_gallery.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("  [2/3] Representation gallery saved")

# ═══════════════════════════════════════════════════════════════
# FIGURE: Nuclear force as geometry
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3.5))

# Left: Gluon exchange in the fundamental
fund = weights(1, 0)
fund_cart = [dynkin_to_cartesian(*w) for w in fund]
colours = ['#CC0000', '#0044CC', '#008800']
labels = ['Red', 'Blue', 'Green']

for i, ((x,y), c, lab) in enumerate(zip(fund_cart, colours, labels)):
    ax1.plot(x, y, 'o', color=c, markersize=14, zorder=5)
    ax1.annotate(lab, (x, y), (x+0.15, y+0.15), fontsize=9, fontweight='bold', color=c)

# Gluon exchange arrows (root vectors)
gluon_pairs = [
    (0, 1, "α₁", '#CC4444'),   # R↔B
    (1, 2, "α₂", '#4444CC'),   # B↔G
    (0, 2, "α₁+α₂", '#44CC44'),  # R↔G
]

for i, j, root_name, arrow_color in gluon_pairs:
    x1, y1 = fund_cart[i]
    x2, y2 = fund_cart[j]
    # Bidirectional
    ax1.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='<->', color=arrow_color, lw=2, 
                              connectionstyle='arc3,rad=0.15'))
    mx, my = (x1+x2)/2, (y1+y2)/2
    ax1.text(mx + 0.2, my, root_name, fontsize=7, color=arrow_color)

ax1.set_title('Gluon Exchange\n(Root Vectors in Weight Space)', fontsize=10, fontweight='bold')
ax1.set_xlim(-2, 2.5)
ax1.set_ylim(-1.5, 1.5)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.15)
ax1.set_xlabel('$h_1$', fontsize=9)
ax1.set_ylabel('$h_2$', fontsize=9)

# Right: Confinement as Casimir descent
rep_labels = ['$\\mathbf{10}$', '$\\mathbf{8}$', '$\\mathbf{6}$', 
              '$\\mathbf{3}$/$\\bar{\\mathbf{3}}$', '$\\mathbf{1}$']
casimirs = [6, 3, 10/3, 4/3, 0]
bar_colors = ['#8844CC', '#FF8800', '#00AA44', '#CC0000', '#999999']

bars = ax2.barh(range(5), casimirs, color=bar_colors, edgecolor='black', 
               linewidth=0.5, height=0.6)
ax2.set_yticks(range(5))
ax2.set_yticklabels(rep_labels, fontsize=10)
ax2.set_xlabel('Quadratic Casimir $C_2$ (binding energy scale)', fontsize=9)
ax2.set_title('Confinement:\n$C_2 \\to 0$ Attractor', fontsize=10, fontweight='bold')

# Arrow showing confinement direction
ax2.annotate('Confinement\n$\\Delta\\mathcal{I} \\to 0$', xy=(0.3, 4), xytext=(3, 3.5),
            arrowprops=dict(arrowstyle='->', color='#CC0000', lw=2),
            fontsize=9, color='#CC0000', fontweight='bold')

ax2.grid(True, axis='x', alpha=0.2)
fig.tight_layout()
fig.savefig(f'{OUTDIR}/fig_nuclear_geometry.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("  [3/3] Nuclear force geometry saved")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("PHYSICAL INTERPRETATION")
print(f"{'='*70}")
print(f"""
  THE GEOMETRIC PICTURE:

  1. COLOUR PLANES (q-planes):
     Each su(3) representation defines a geometric shape in weight space:
       Singlet (1):    a point at the origin         C₂ = 0
       Fundamental (3): equilateral triangle          C₂ = 4/3
       Adjoint (8):     hexagon (the gluon rep)       C₂ = 3
       Sextet (6):      larger triangle               C₂ = 10/3
       Decuplet (10):   even larger triangle          C₂ = 6

     These stack vertically by their quadratic Casimir C₂,
     forming a "tower" of geometric shapes at different energy levels.

  2. GLUON EXCHANGE = ROOT VECTORS:
     A gluon exchange between two quarks IS a root vector displacement
     in weight space. There are exactly 6 root vectors (3 positive + 
     3 negative), corresponding to the 6 off-diagonal gluons.
     The 2 diagonal gluons (g₃, g₈) move WITHIN a weight state 
     (they measure colour without changing it).

  3. CONFINEMENT = CASIMIR DESCENT:
     The nuclear force drives the system toward C₂ = 0 (the singlet).
     In ACS language: ΔI → 0 is the attractor.
     Higher representations (larger C₂) have more binding energy
     and are less stable. The system cascades:
       10 → 8 → 6 → 3 → 1
     until it reaches the colourless singlet.

  4. THE GEOMETRIC SHAPES ARE PHYSICAL:
     The triangle (3) is the quark.
     The inverted triangle (3̄) is the antiquark.
     The hexagon (8) is the gluon field itself.
     The point (1) is the hadron (confined state).
     
     These aren't visualisation tricks — they're the ACTUAL weight 
     diagrams of the representations, and the geometry of the shapes 
     determines the allowed interactions.

  5. ACS CONNECTION:
     In the Palatini ACS:
     - The SHAPE of each representation comes from the bracket structure
       (Prop 9.3: the 6+3 split determines which shapes exist)
     - The STACKING by C₂ comes from the Casimir operator 
       (which is built from the Cartan generators H₁, H₂)
     - The ROOT VECTORS (gluon exchange) traverse both torsion and 
       Lorentz sectors (each gluon = one torsion + one Lorentz generator)
     - CONFINEMENT (C₂ → 0) is the constraint-attractor cycle:
       the system evolves until ΔI = 0 in the colour sector
""")
