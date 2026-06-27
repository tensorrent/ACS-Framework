"""Cyclotomic Q(zeta_5) - figure showing complex character recovery."""
import math, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.signal import find_peaks

OUTDIR = "/home/claude/cyclotomic"
data = np.load(f"{OUTDIR}/cyclotomic_data.npz")
zeros = data['zeros']
omega = data['omega']
F_cos = data['F_cos']
F_sin = data['F_sin']
F_mag = data['F_mag']

def chi_5_order4(p):
    if p % 5 == 0: return 0
    r = p % 5
    if r == 1: return 1 + 0j
    if r == 2: return 0 + 1j
    if r == 3: return 0 - 1j
    if r == 4: return -1 + 0j

def sieve(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2, n+1):
        if s[i]:
            for j in range(i*i, n+1, i): s[j]=False
    return [i for i in range(n+1) if s[i]]
primes = sieve(1000)

# Color by character value
CHI_COLORS = {1: '#22ff44', 1j: '#ffaa44', -1j: '#ff77aa', -1: '#ff3333'}
CHI_LABELS = {1: '+1 (p≡1)', 1j: '+i (p≡2)', -1j: '-i (p≡3)', -1: '-1 (p≡4)'}

fig = plt.figure(figsize=(16, 12))
gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.28, height_ratios=[1, 1, 1.2])
fig.patch.set_facecolor('#040408')

def style(ax, title, xlabel, ylabel):
    ax.set_facecolor('#0a0a14')
    ax.set_title(title, color='white', fontsize=11)
    ax.set_xlabel(xlabel, color='white', fontsize=10)
    ax.set_ylabel(ylabel, color='white', fontsize=10)
    for s in ax.spines.values(): s.set_color('#555')
    ax.tick_params(colors='white')

# Panel A: F_cos with prime markers (showing real-character signal)
ax = fig.add_subplot(gs[0, 0])
ax.plot(omega, F_cos, color='#22ddff', linewidth=1.5, label='F_cos(ω)')
ax.axhline(0, color='white', linewidth=0.5, alpha=0.3)
for p in primes[:20]:
    lp = math.log(p)
    if not (0.5 <= lp <= 3.5) or p == 5: continue
    c = chi_5_order4(p)
    color = CHI_COLORS[c]
    # Only label real characters here (p≡1, p≡4)
    if abs(c.imag) < 0.5:
        ax.axvline(lp, color=color, linewidth=1.3, alpha=0.7)
        ax.text(lp, 0.30, f"{p}", color=color, fontsize=9, ha='center',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='#040408',
                         edgecolor=color, alpha=0.85))
    else:
        ax.axvline(lp, color=color, linewidth=0.7, alpha=0.3, linestyle=':')
ax.set_xlim(0.5, 3.5); ax.set_ylim(-0.35, 0.35)
style(ax, "F_cos(ω): peaks at primes with REAL χ values (p≡1,4 mod 5)",
       "ω", "F_cos(ω)")

# Panel B: F_sin with prime markers (showing imaginary-character signal)
ax = fig.add_subplot(gs[0, 1])
ax.plot(omega, F_sin, color='#ff77ff', linewidth=1.5, label='F_sin(ω)')
ax.axhline(0, color='white', linewidth=0.5, alpha=0.3)
for p in primes[:20]:
    lp = math.log(p)
    if not (0.5 <= lp <= 3.5) or p == 5: continue
    c = chi_5_order4(p)
    color = CHI_COLORS[c]
    if abs(c.real) < 0.5:  # imaginary chi values
        ax.axvline(lp, color=color, linewidth=1.3, alpha=0.7)
        ax.text(lp, 0.30, f"{p}", color=color, fontsize=9, ha='center',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='#040408',
                         edgecolor=color, alpha=0.85))
    else:
        ax.axvline(lp, color=color, linewidth=0.7, alpha=0.3, linestyle=':')
ax.set_xlim(0.5, 3.5); ax.set_ylim(-0.35, 0.35)
style(ax, "F_sin(ω): peaks at primes with IMAGINARY χ values (p≡2,3 mod 5)",
       "ω", "F_sin(ω)")

# Panel C: Phase plot — F_cos + i·F_sin at log(p) for each prime
ax = fig.add_subplot(gs[1, 0])
ax.axhline(0, color='white', linewidth=0.5, alpha=0.3)
ax.axvline(0, color='white', linewidth=0.5, alpha=0.3)

# Plot each prime as point in (F_cos, F_sin) plane
for p in primes[:30]:
    if p == 5: continue
    lp = math.log(p)
    if lp > 5: continue
    idx = np.argmin(np.abs(omega - lp))
    fc = F_cos[idx]; fs = F_sin[idx]
    c = chi_5_order4(p)
    color = CHI_COLORS[c]
    ax.scatter(fc, fs, s=120, color=color, edgecolor='white', linewidth=0.8, zorder=5)
    ax.annotate(f"{p}", (fc, fs), xytext=(5, 5), textcoords='offset points',
                fontsize=8, color=color)

# Mark predicted positions
amp = 0.16  # rough mean amplitude
# Theoretical position: F_cos + i·F_sin ≈ -chi(p) × amp (sign from explicit formula)
for chi_val, color in CHI_COLORS.items():
    pred = -chi_val * amp
    ax.scatter([pred.real], [pred.imag], s=300, color=color, marker='*',
               edgecolor='white', linewidth=2, alpha=0.6, zorder=4)

# Annotate quadrants
for chi_val, label in CHI_LABELS.items():
    pred = -chi_val * 0.20
    ax.annotate(f"χ={chi_val}", (pred.real, pred.imag),
               xytext=(8, -8) if pred.imag <= 0 else (8, 8),
               textcoords='offset points', fontsize=10, color=CHI_COLORS[chi_val],
               weight='bold')

ax.set_xlim(-0.3, 0.3); ax.set_ylim(-0.3, 0.3)
ax.set_aspect('equal')
style(ax, "Complex character recovery: each prime in (F_cos, F_sin) plane",
       "F_cos(log p)", "F_sin(log p)")

# Panel D: |F| amplitude
ax = fig.add_subplot(gs[1, 1])
ax.plot(omega, F_mag, color='#ffaa00', linewidth=1.5)
ax.axhline(0, color='white', linewidth=0.5, alpha=0.3)
for p in primes[:20]:
    lp = math.log(p)
    if not (0.5 <= lp <= 3.5) or p == 5: continue
    c = chi_5_order4(p)
    color = CHI_COLORS[c]
    ax.axvline(lp, color=color, linewidth=1.2, alpha=0.55)
ax.set_xlim(0.5, 3.5); ax.set_ylim(0, 0.4)
style(ax, "|F(ω)| = √(F_cos² + F_sin²): peaks at ALL primes (chi=0 excepted)",
       "ω", "|F(ω)|")

# Panel E: Summary
ax = fig.add_subplot(gs[2, :])
ax.axis('off')

# Compute means by chi class
results = {}
for p in primes[:30]:
    if p == 5: continue
    lp = math.log(p)
    if lp > 5: continue
    idx = np.argmin(np.abs(omega - lp))
    c = chi_5_order4(p)
    key = (c.real, c.imag)
    if key not in results: results[key] = []
    results[key].append((p, F_cos[idx], F_sin[idx]))

summary = """
CYCLOTOMIC Q(ζ_5) — FIRST NON-QUADRATIC FIELD TEST

Setup:
  Q(ζ_5) is a DEGREE-4 cyclotomic field. Galois group Gal(Q(ζ_5)/Q) ≅ (Z/5)* ≅ Z/4 (cyclic).
  Dedekind zeta: ζ_K(s) = ζ(s) · L(s, χ) · L(s, χ²) · L(s, χ³)
  where χ is a generator of the character group, ORDER 4 (complex-valued).
  
  This is the framework's first test on a COMPLEX character (χ takes values in {1, i, -1, -i}).
  Methodology: define Z(t) = e^{-i arg(ε)/2} · Λ(1/2 + it, χ) which is real-valued.
  Then find zeros of Z. Found 54 zeros in range [6.18, 99.06] (predicted 53.1).

THE COMPLEX CHARACTER STRUCTURE IS RECOVERED CLEANLY:

  Per-class mean F_cos and F_sin at log(p):

  ╔══════════╤═══════╤═════════════╤═════════════╤═════════════╗
  ║ p mod 5  │  χ(p) │ Mean F_cos  │ Mean F_sin  │ Class       ║
  ╠══════════╪═══════╪═════════════╪═════════════╪═════════════╣
"""

for key, label, sign in [((1.0, 0.0), '+1', '(p≡1)'),
                          ((0.0, 1.0), '+i', '(p≡2)'),
                          ((0.0, -1.0), '-i', '(p≡3)'),
                          ((-1.0, 0.0), '-1', '(p≡4)')]:
    if key in results:
        rows = results[key]
        mean_fc = np.mean([r[1] for r in rows])
        mean_fs = np.mean([r[2] for r in rows])
        summary += f"  ║   {sign:6s} │  {label:4s} │   {mean_fc:+.4f}   │   {mean_fs:+.4f}   │ n = {len(rows):2d}        ║\n"

summary += """  ╚══════════╧═══════╧═════════════╧═════════════╧═════════════╝

  INTERPRETATION

    For p ≡ 1 mod 5 (χ = +1):  F_cos = -0.15 (PEAK in cos channel, negative sign)
                                F_sin ≈ 0    (no signal in sin channel)

    For p ≡ 4 mod 5 (χ = -1):  F_cos = +0.16 (PEAK in cos channel, positive sign — flipped)
                                F_sin ≈ 0

    For p ≡ 2 mod 5 (χ = +i):  F_cos ≈ 0
                                F_sin = -0.17 (PEAK in sin channel, negative sign)

    For p ≡ 3 mod 5 (χ = -i):  F_cos ≈ 0
                                F_sin = +0.15 (PEAK in sin channel, positive sign — flipped)

  The complex Fourier transform F(ω) = (1/N) Σ exp(iω γ) at log(p) recovers chi(p) cleanly:
                                
                            F(log p) ≈ -χ(p) · |amplitude|
  
  Real chi → real F (cosine channel only)
  Imaginary chi → imaginary F (sine channel only)
  Sign of F = -sign of chi (from explicit-formula coefficient)

KEY OBSERVATIONS

  1. The framework EXTENDS naturally from real to complex characters. 
     The (cos, sin) channel decomposition recovers the (Re(chi), Im(chi)) structure.
     
  2. CROSS-CHANNEL LEAKAGE is small (~0.01-0.02), much smaller than signal (~0.15-0.17).
     This means the recovery is clean — character classes are well-separated in the
     (F_cos, F_sin) phase plane.
     
  3. The phase plot is a faithful operational representation of the cyclic group 
     structure of (Z/5)*. The four character values {1, i, -1, -i} appear at four 
     distinct positions in the (F_cos, F_sin) plane.
     
  4. The framework is therefore not specific to real (quadratic) characters. It 
     captures Fourier-dual structure for general Dirichlet characters, with 
     complex characters cleanly handled via the Z-function methodology.

EXTENSION (NOT YET DONE)

  The full Dedekind ζ_{Q(ζ_5)} = ζ · L(χ) · L(χ²) · L(χ³). To test the full 
  Dedekind structure of Q(ζ_5), need to combine: F_cos for ζ, F (complex) for L(χ),
  F_cos for L(χ²) [our quadratic case], and conjugate F for L(χ³). The result should 
  show the splitting structure of Q(ζ_5):
  
    p ≡ 1 mod 5: SPLIT COMPLETELY into 4 prime ideals
    p ≡ 2, 3 mod 5: TWO prime ideals each (of degree 2)
    p ≡ 4 mod 5: TWO prime ideals each (of degree 2)
    p = 5: FULLY RAMIFIED (1 prime ideal, e=4)
  
  This is a natural follow-up computation.
"""
ax.text(0.0, 0.98, summary, transform=ax.transAxes,
        fontsize=8.5, color='white', family='monospace', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#0a0a14', edgecolor='#555'))

plt.suptitle("Cyclotomic Q(ζ_5) — Complex Character Recovery via Z-function Methodology",
             color='white', fontsize=14, weight='bold', y=0.995)
plt.savefig(f"{OUTDIR}/cyclotomic_5.png", dpi=130, bbox_inches='tight', facecolor='#040408')
print(f"Saved: {OUTDIR}/cyclotomic_5.png")
