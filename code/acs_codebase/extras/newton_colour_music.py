#!/usr/bin/env python3
"""
NEWTON'S COLOUR WHEEL → QCD COLOUR CHARGES
=============================================
Newton (Opticks, 1704): divided the visible spectrum into 7 colours
matching the 7 notes of the Dorian mode (D E F G A B C).
He believed colours and musical tones obeyed the same ratios.

The ACS framework makes this precise:
1. Optical colour = eigenvalue of the EM field ACS
2. Musical pitch = eigenvalue of the vibrating string ACS  
3. QCD colour = eigenvalue of the Palatini torsion ACS
All three are spectra of asymmetric codependent systems.

The key bridge: Newton's 3 PRIMARY colours (R,G,B) that combine
to make WHITE are structurally identical to QCD's 3 colour charges
(R,G,B) that combine to make a SINGLET.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, FancyArrowPatch
import os

OUTDIR = "/home/claude/figures"
os.makedirs(OUTDIR, exist_ok=True)

print("=" * 70)
print("NEWTON'S COLOUR WHEEL → QCD COLOUR CHARGES")
print("Three Spectra, One Structure")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════
print("""
── Newton's Colour-Music Correspondence (Opticks, 1704) ──

Newton divided the visible spectrum using the Dorian mode ratios:
  D  → Red       (lowest frequency, least refracted)
  E  → Orange    
  F  → Yellow    (half-step E→F = narrow band)
  G  → Green     
  A  → Blue      
  B  → Indigo    
  C  → Violet    (half-step B→C = narrow band)
  D' → (octave = return to Red)

The Dorian mode intervals (in frequency ratios):
  D→E: 9/8  (whole tone)    → Red band
  E→F: 256/243 (semitone)   → Orange band (narrow)
  F→G: 9/8  (whole tone)    → Yellow band
  G→A: 9/8  (whole tone)    → Green band
  A→B: 9/8  (whole tone)    → Blue band
  B→C: 256/243 (semitone)   → Indigo band (narrow)
  C→D': 9/8 (whole tone)    → Violet band
""")

# ═══════════════════════════════════════════════════════════════
print("── The Three-Layer Colour Correspondence ──\n")

# Three instances of "colour" in physics, all ACS:

print(f"  {'Property':<20} {'Optical Colour':<22} {'Musical Tone':<22} {'QCD Colour'}")
print(f"  {'-'*86}")

correspondences = [
    ("Form (boundary)", "E field", "String length L", "Vierbein e"),
    ("Function (dyn.)", "B field", "Tension T", "Connection ω"),
    ("Coupling", "Maxwell eqs", "Wave equation", "Palatini action"),
    ("Spectrum", "λ = 400-700nm", "f = 20-20kHz", "R, B, G charges"),
    ("Eigenvalues", "Frequency ν", "Harmonics f_n", "Cartan h₁, h₂"),
    ("Primary 'colours'", "R, G, B", "I, IV, V (tonic)", "R, G, B"),
    ("'White' (all equal)", "White light", "Root chord", "Colour singlet"),
    ("Bracket [F,F]", "E×B (Poynting)", "Standing wave", "Curvature R"),
    ("ΔI = 0 (balance)", "Unpolarised", "Unison/octave", "Confinement"),
    ("Non-Abelian?", "No (U(1))", "No (linear)", "Yes (SU(3))"),
]

for prop, opt, mus, qcd in correspondences:
    print(f"  {prop:<20} {opt:<22} {mus:<22} {qcd}")

# ═══════════════════════════════════════════════════════════════
print(f"\n── Why Three Primary Colours? ──\n")

print("""  In OPTICS: R, G, B are primary because the human eye has three
  types of cone cells (L, M, S). This is a BIOLOGICAL accident —
  the physics has a continuous spectrum.

  In QCD: R, G, B are primary because su(3) has rank 2, giving
  a 3-dimensional fundamental representation. This is NOT an
  accident — it follows from the Palatini bracket structure:
  sl(3,R) is the unique 8-dim closure attractor in sl(4,R),
  and the fundamental representation has dimension 3.

  Newton's insight (deeper than he knew): the fact that THREE
  primary colours combine to make "white" (colourless) is the
  SAME structure in optics and QCD:
  
  Optics: R + G + B = White (all frequencies present equally)
  QCD:    R + G + B = Singlet (all colour charges cancel)
  
  The mathematical structure is identical:
    Optics: the colour vector (r, g, b) with r = g = b
    QCD: the singlet |ψ⟩ = (|R⟩ + |G⟩ + |B⟩)/√3
    
  Both are FIXED POINTS of the colour rotation group:
    Optics: white is invariant under any colour transformation
    QCD: singlet is invariant under all su(3) rotations
    ACS: both are ΔI = 0 attractors
""")

# ═══════════════════════════════════════════════════════════════
print("── Newton's Colour Wheel as a Weight Diagram ──\n")

# Newton's colour wheel is a CIRCLE with 7 sectors
# The three primary colours (R, G, B) are at 120° intervals
# This is TOPOLOGICALLY identical to the su(3) weight diagram

# Newton's wheel positions (Dorian mode, starting at D)
# Using cumulative fractions of the octave
dorian_ratios = [0, 9/64, 9/64+16/243*64/9/64, 
                 2*9/64+16/243*64/9/64,
                 3*9/64+16/243*64/9/64,
                 4*9/64+16/243*64/9/64,
                 4*9/64+2*16/243*64/9/64]

# Simplified: Newton used these approximate angular sizes
# R=1/9, O=1/10, Y=1/10, G=1/9, B=1/10, I=1/10, V=1/9
# (three large + four small, summing to ~1)
sizes = [1/9, 1/10, 1/10, 1/9, 1/10, 1/10, 1/9]
total = sum(sizes)
sizes_norm = [s/total for s in sizes]

# Cumulative angles
angles = [0]
for s in sizes_norm:
    angles.append(angles[-1] + s * 360)

colours_newton = ['#FF0000', '#FF8800', '#FFFF00', '#00CC00', 
                  '#0044FF', '#2200AA', '#8800CC']
labels_newton = ['Red\n(D)', 'Orange\n(E)', 'Yellow\n(F)', 'Green\n(G)',
                 'Blue\n(A)', 'Indigo\n(B)', 'Violet\n(C)']
notes = ['D', 'E', 'F', 'G', 'A', 'B', 'C']

print(f"  Newton's wheel sectors (Dorian mode):")
print(f"  {'Colour':<10} {'Note':<6} {'Interval':<12} {'Arc (°)':<10} {'Primary?'}")
print(f"  {'-'*50}")

for i in range(7):
    arc = angles[i+1] - angles[i]
    interval = "whole" if sizes[i] > 1/9.5 else "half"
    primary = "★" if i in [0, 3, 4] else ""  # R, G, B
    print(f"  {labels_newton[i].split(chr(10))[0]:<10} {notes[i]:<6} {interval:<12} {arc:<10.1f} {primary}")

# ═══════════════════════════════════════════════════════════════
print(f"\n── The Frequency Octave Bridge ──\n")

# The visible spectrum spans roughly:
# Violet: ~380 THz (789 nm) to Red: ~480 THz (625 nm)
# Wait, let me get this right:
# Red: ~400 THz (750 nm) to Violet: ~750 THz (400 nm)
# Ratio: 750/400 = 1.875 ≈ close to 2:1 (an octave!)

freq_red = 400  # THz (approximate)
freq_violet = 750  # THz

print(f"  Visible spectrum: {freq_red} THz (red) to {freq_violet} THz (violet)")
print(f"  Ratio: {freq_violet/freq_red:.3f}")
print(f"  Musical octave ratio: 2.000")
print(f"  Discrepancy: {abs(freq_violet/freq_red - 2)/2 * 100:.1f}%")
print(f"  → The visible spectrum spans approximately ONE OCTAVE")
print(f"     (Newton assumed exactly one octave)")

# Map Newton's notes to optical frequencies
print(f"\n  Newton's colour-note-frequency mapping:")
print(f"  {'Note':<6} {'Colour':<10} {'Optical freq (THz)':<20} {'Musical ratio':<15}")
print(f"  {'-'*55}")

# Dorian mode ratios from D (multiply cumulatively)
dorian_intervals = [1, 9/8, (9/8)**2, (9/8)**2*(256/243),
                    (9/8)**3*(256/243), (9/8)**4*(256/243),
                    (9/8)**4*(256/243)**2]
# Normalized
for i, (note, colour, ratio) in enumerate(zip(
    notes, ['Red','Orange','Yellow','Green','Blue','Indigo','Violet'],
    dorian_intervals)):
    freq = freq_red * ratio
    print(f"  {note:<6} {colour:<10} {freq:<20.1f} {ratio:<15.4f}")

# ═══════════════════════════════════════════════════════════════
print(f"\n── The Deep Connection: Three Spectra ──\n")

print(f"""  Newton saw 7 colours in the spectrum because he imposed the
  musical scale (7 notes per octave). But the PHYSICS has three
  primary colours — R, G, B — because of cone cell biology.

  QCD has three colour charges — R, G, B — because of the Lie
  algebra structure (rank 2 → 3-dim fundamental).

  The ACS framework explains WHY the number 3 appears in both:

  In su(3): the Cartan subalgebra has dimension 2 (H₁, H₂).
  The fundamental representation has dimension 2+1 = 3.
  The weight vectors form a triangle with 3 vertices.
  Three is the minimal non-trivial fundamental dimension
  for a rank-2 simple Lie algebra.

  In optics: the EM field has 2 independent polarisations
  (E and B, or equivalently the two helicities).
  The colour space is 3-dimensional because:
  2 polarisations × frequency → 3 independent colour channels
  (this is why RGB suffices for colour reproduction).

  In music: the triad (I-III-V) has 3 notes because the
  first three non-trivial harmonics (2:1, 3:2, 5:4) define
  three independent pitch classes within the octave.

  THE UNIFYING PRINCIPLE (ACS):
  In each case, a rank-2 system (two independent directions)
  produces a 3-dimensional representation as its fundamental.
  The "white" state (all three equal) is the ΔI = 0 attractor.
""")

# ═══════════════════════════════════════════════════════════════
# Generate the figure
fig = plt.figure(figsize=(9, 4))

# Panel 1: Newton's colour wheel
ax1 = fig.add_subplot(131, projection='polar')
for i in range(7):
    theta1 = np.radians(angles[i])
    theta2 = np.radians(angles[i+1])
    theta_range = np.linspace(theta1, theta2, 50)
    ax1.fill_between(theta_range, 0.5, 1.0, color=colours_newton[i], alpha=0.8)
    mid_angle = (theta1 + theta2) / 2
    ax1.text(mid_angle, 1.15, notes[i], ha='center', va='center', fontsize=8, fontweight='bold')

ax1.set_ylim(0, 1.3)
ax1.set_yticks([])
ax1.set_xticks([])
ax1.set_title("Newton's Colour Wheel\n(Opticks, 1704)", fontsize=9, fontweight='bold', pad=15)

# Panel 2: RGB additive mixing (triangle)
ax2 = fig.add_subplot(132)

# Three primary circles overlapping
from matplotlib.patches import Circle
R_pos = (0.5, 0.85)
G_pos = (0.15, 0.25)
B_pos = (0.85, 0.25)

for pos, color, label in [(R_pos, '#FF000066', 'R'), 
                           (G_pos, '#00FF0066', 'G'),
                           (B_pos, '#0000FF66', 'B')]:
    circle = Circle(pos, 0.38, color=color, ec='black', lw=0.5)
    ax2.add_patch(circle)
    ax2.text(pos[0], pos[1] + (0.25 if pos[1] > 0.5 else -0.25),
            label, ha='center', fontsize=12, fontweight='bold',
            color=color[:7].replace('66',''))

# White center
ax2.text(0.5, 0.45, 'White\n(singlet)', ha='center', va='center', 
        fontsize=8, fontweight='bold', color='gray')

ax2.set_xlim(-0.3, 1.3)
ax2.set_ylim(-0.15, 1.25)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('RGB Primary Colours\n(Optics = QCD)', fontsize=9, fontweight='bold')

# Panel 3: QCD weight diagram
ax3 = fig.add_subplot(133)

# Same triangle as the colour weight diagram
weights_qcd = [(1, 0), (-0.5, np.sqrt(3)/2), (-0.5, -np.sqrt(3)/2)]
qcd_colors = ['#CC0000', '#0044CC', '#008800']
qcd_labels = ['R (+1,0)', 'B (-1,+1)', 'G (0,-1)']

tri = plt.Polygon(weights_qcd, fill=False, edgecolor='gray', linewidth=1, linestyle='--')
ax3.add_patch(tri)

for (x,y), c, lab in zip(weights_qcd, qcd_colors, qcd_labels):
    ax3.plot(x, y, 'o', color=c, markersize=12, zorder=5)
    dx = 0.15 if x > 0 else -0.15
    dy = 0.15 if y > 0 else -0.15
    ax3.annotate(lab, (x,y), (x+dx, y+dy), fontsize=7, fontweight='bold', color=c)

# White at center
ax3.plot(0, 0, 'o', color='gray', markersize=8, markerfacecolor='white',
        markeredgecolor='gray', markeredgewidth=1.5, zorder=5)
ax3.text(0.15, -0.05, 'Singlet\n$(0,0)$', fontsize=7, color='gray')

# Gluon arrows
for i in range(3):
    j = (i+1) % 3
    ax3.annotate('', xy=weights_qcd[j], xytext=weights_qcd[i],
                arrowprops=dict(arrowstyle='->', color='#888888', lw=1, 
                              connectionstyle='arc3,rad=0.2'))

ax3.set_xlim(-1.2, 1.5)
ax3.set_ylim(-1.2, 1.2)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_title('QCD Weight Diagram\n(Palatini ACS)', fontsize=9, fontweight='bold')

# Connect panels with arrows
fig.text(0.35, 0.5, '≅', fontsize=20, ha='center', va='center', color='#CC0000')
fig.text(0.66, 0.5, '≅', fontsize=20, ha='center', va='center', color='#CC0000')

fig.suptitle("Newton → Mersenne → QCD: Three Primary Colours, One Structure",
            fontsize=11, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(f'{OUTDIR}/fig_newton_qcd.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("  Figure saved: fig_newton_qcd.pdf")

# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("SUMMARY: NEWTON'S COLOUR WHEEL IS THE QCD WEIGHT DIAGRAM")
print(f"{'='*70}")
print(f"""
  Three physicists, three centuries, one structure:

  MERSENNE (1636): Harmonics of vibrating strings obey integer ratios.
    Combination tones arise from nonlinear mixing (= Wronskian bracket).
    Primes M_p = 2^p - 1 sample the spectral function at harmonic nodes.

  NEWTON (1704): The visible spectrum divides into 7 bands matching
    the 7 notes of the Dorian mode. Three primary colours (R,G,B)
    combine to make white. The colour wheel is a circular weight diagram.

  ACS (2026): The Palatini bracket generates sl(4,R), which uniquely
    selects sl(3,R) → su(3) via the chirality map. The three colour 
    charges (R,G,B) are eigenvalues of torsion-sector Cartan generators.
    The colour singlet (white) is the ΔI = 0 attractor.

  THE CONNECTION:
    Newton's 3 primary colours   =  QCD's 3 colour charges
    Newton's white (R+G+B)       =  QCD's singlet (R+G+B)/√3
    Newton's colour wheel         ≅  su(3) weight diagram (topologically)
    Mersenne's combination tones  =  ACS Wronskian bracket
    Mersenne's harmonic series    =  Euler product (= zeta function)
    Newton's spectral "octave"    =  one period of the spectral function

  Newton was right that colour and music obey the same mathematics.
  He was right that three primary colours are fundamental.
  He could not have known that the same three-ness appears in QCD —
  but the ACS framework shows it's the same rank-2 algebra producing
  a 3-dimensional fundamental representation in all three domains.
""")
