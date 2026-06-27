"""Final figure showing disentangled conductor vs class number effects."""
import math, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

OUTDIR = "/home/claude/disentangled"
os.makedirs(OUTDIR, exist_ok=True)

# Full data set with NEW h=2 fields
fields = [
    # name, h, cond, split, inert, ratio, N
    ("Q(√-3)",    1,  3, 0.320, 0.041, 7.85, 114),
    ("Q(i)",      1,  4, 0.323, 0.057, 5.69, 122),
    ("Q(√5)",     1,  5, 0.320, 0.058, 5.50, 113),
    ("Q(√-15)",   2, 15, 0.271, 0.068, 3.96, 164),
    ("Q(√-5)",    2, 20, 0.260, 0.077, 3.39, 174),
    ("Q(√-6)",    2, 24, 0.304, 0.097, 3.13, 128),
    ("Q(√-35)",   2, 35, 0.320, 0.106, 3.03,  65),  # NEW
    ("Q(√-91)",   2, 91, 0.268, 0.206, 1.30,  55),  # NEW - decisive
    ("Q(√-23)",   3, 23, 0.412, 0.146, 2.82,  42),
    ("Q(√-31)",   3, 31, 0.300, 0.134, 2.23,  64),
    ("Q(√-39)",   4, 39, 0.279, 0.141, 1.98,  66),
    ("Q(√-47)",   5, 47, 0.279, 0.155, 1.80,  69),
    ("Q(√-87)",   6, 87, 0.341, 0.118, 2.89,  77),
    ("Q(√-26)",   6,104, 0.353, 0.132, 2.67,  67),
]

H_COLORS = {1:'#22ddff', 2:'#ffaa44', 3:'#ff4444', 4:'#aa44ff', 5:'#ff77ff', 6:'#888888'}

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

# Panel A: h=2 specifically — varying conductor
ax = fig.add_subplot(gs[0, 0])
h2_data = [(c, r, n) for nm,h,c,_,_,r,n in fields if h == 2]
for c, r, n in h2_data:
    ax.scatter(c, r, s=180, color='#ffaa44', edgecolor='white', linewidth=1.5, zorder=5)
ax.set_xlim(0, 100); ax.set_ylim(0, 5)
style(ax, "h=2 FIXED, CONDUCTOR VARYING\n5 fields spanning 6× conductor range",
       "conductor", "split/inert ratio")
ax.grid(alpha=0.2)
ax.text(0.05, 0.95, "Conductors 15-35: cluster 3.0-4.0\nConductor 91: drops to 1.30",
        transform=ax.transAxes, color='white', fontsize=10, va='top',
        bbox=dict(boxstyle='round', facecolor='#1a1a2e', edgecolor='#555'))

# Panel B: all data, color by h, x = conductor
ax = fig.add_subplot(gs[0, 1])
for name, h, c, _, _, r, n in fields:
    ax.scatter(c, r, s=140, color=H_COLORS[h], edgecolor='white', linewidth=1, zorder=5)
    ax.annotate(name.replace("Q(√","").replace(")",""), (c, r), xytext=(5, 5),
               textcoords='offset points', fontsize=7, color=H_COLORS[h])
for h in range(1, 7):
    ax.scatter([], [], color=H_COLORS[h], s=140, edgecolor='white', linewidth=1, label=f'h={h}')
ax.set_xlim(0, 110); ax.set_ylim(0, 9)
style(ax, "All fields: ratio vs conductor (color = class number)",
       "conductor", "split/inert ratio")
ax.legend(facecolor='black', edgecolor='#555', labelcolor='white', fontsize=9, loc='upper right')
ax.grid(alpha=0.2)

# Panel C: split and inert MEANS - check what's changing
ax = fig.add_subplot(gs[1, 0])
for name, h, c, s, i, r, n in fields:
    ax.scatter(c, s, s=80, color='#22ff44', edgecolor='white', linewidth=0.4, alpha=0.85)
    ax.scatter(c, i, s=80, color='#ff3333', edgecolor='white', linewidth=0.4, alpha=0.85, marker='X')
ax.scatter([], [], color='#22ff44', s=100, label='split mean')
ax.scatter([], [], color='#ff3333', s=100, marker='X', label='inert mean')
ax.set_xlim(0, 110); ax.set_ylim(0, 0.5)
style(ax, "Split mean (~constant) vs Inert mean (grows with conductor)",
       "conductor", "mean |F_K| at log(p)")
ax.legend(facecolor='black', edgecolor='#555', labelcolor='white', fontsize=9)
ax.grid(alpha=0.2)

# Panel D: ratio vs h with new points - law is broken
ax = fig.add_subplot(gs[1, 1])
for name, h, c, _, _, r, n in fields:
    jitter = np.random.uniform(-0.1, 0.1)
    ax.scatter(h + jitter, r, s=180, color=H_COLORS[h], edgecolor='white', linewidth=1, zorder=5, alpha=0.85)
# Show "naive" fit
h_curve = np.linspace(0.5, 6.5, 200)
ax.plot(h_curve, 0.52 + 5.82/h_curve, '--', color='#ffff88', linewidth=1.5, alpha=0.6,
        label='Naive fit 0.52 + 5.82/h\n(now clearly inadequate)')
# Annotate Q(√-91) 
for name, h, c, _, _, r, n in fields:
    if name == "Q(√-91)":
        ax.annotate('Q(√-91)\ncond=91, h=2\nratio=1.30', (h, r),
                   xytext=(40, 30), textcoords='offset points',
                   arrowprops=dict(arrowstyle='->', color='#ffaa44', linewidth=1.5),
                   fontsize=10, color='#ffaa44',
                   bbox=dict(boxstyle='round', facecolor='#1a1a2e', edgecolor='#ffaa44'))
ax.set_xlim(0.5, 6.5); ax.set_ylim(0, 9)
ax.set_xticks([1, 2, 3, 4, 5, 6])
style(ax, "Ratio vs h: naive law fails at large conductor",
       "class number h_K", "ratio")
ax.legend(facecolor='black', edgecolor='#555', labelcolor='white', fontsize=9)
ax.grid(alpha=0.2)

# Panel E: Summary table
ax = fig.add_subplot(gs[2, :])
ax.axis('off')
summary = """
DISENTANGLED CONDUCTOR vs CLASS NUMBER — 14 quadratic fields tested

╔════════════════╤═════╤══════════╤═══════════╤═══════════╤═══════════╤══════╗
║ Field          │ h_K │ Conductor│ Split mean│ Inert mean│ Ratio     │ N    ║
╠════════════════╪═════╪══════════╪═══════════╪═══════════╪═══════════╪══════╣
║ Q(√-3)         │  1  │    3     │  0.320    │  0.041    │  7.85×    │ 114  ║
║ Q(i)           │  1  │    4     │  0.323    │  0.057    │  5.69×    │ 122  ║
║ Q(√5)          │  1  │    5     │  0.320    │  0.058    │  5.50×    │ 113  ║
║                │     │          │           │           │           │      ║
║ Q(√-15)        │  2  │   15     │  0.271    │  0.068    │  3.96×    │ 164  ║
║ Q(√-5)         │  2  │   20     │  0.260    │  0.077    │  3.39×    │ 174  ║
║ Q(√-6)         │  2  │   24     │  0.304    │  0.097    │  3.13×    │ 128  ║
║ Q(√-35) NEW    │  2  │   35     │  0.320    │  0.106    │  3.03×    │  65  ║
║ Q(√-91) NEW    │  2  │   91     │  0.268    │  0.206    │  1.30×    │  55  ║
║                │     │          │           │           │           │      ║
║ Q(√-23)        │  3  │   23     │  0.412    │  0.146    │  2.82×    │  42  ║
║ Q(√-31)        │  3  │   31     │  0.300    │  0.134    │  2.23×    │  64  ║
║                │     │          │           │           │           │      ║
║ Q(√-39)        │  4  │   39     │  0.279    │  0.141    │  1.98×    │  66  ║
║ Q(√-47)        │  5  │   47     │  0.279    │  0.155    │  1.80×    │  69  ║
║ Q(√-87)        │  6  │   87     │  0.341    │  0.118    │  2.89×    │  77  ║
║ Q(√-26)        │  6  │  104     │  0.353    │  0.132    │  2.67×    │  67  ║
╚════════════════╧═════╧══════════╧═══════════╧═══════════╧═══════════╧══════╝

PRIMARY FINDING: The fixed-h disentanglement test reveals CONDUCTOR is a major driver
of the ratio variation, NOT just class number.

KEY OBSERVATIONS

  1. h=2 RATIO IS NOT CONDUCTOR-INVARIANT
     Across conductors 15, 20, 24, 35: ratios cluster at 3.0-4.0 (consistent with the
     earlier "class number 2" reading).
     At conductor 91: ratio drops to 1.30 — well below the cluster.
     The factor-6 conductor variation produces factor-3 ratio variation.

  2. INERT MEAN GROWS WITH CONDUCTOR, NOT (PRIMARILY) WITH h
     The split mean stays roughly constant (~0.28-0.32).
     The inert mean systematically grows with conductor:
       conductor 3:   inert 0.041
       conductor 24:  inert 0.097
       conductor 91:  inert 0.206  (5× larger than at cond 3)
     This is the actual mechanism driving the ratio.

  3. THE SIMPLE LAW 0.52 + 5.82/h IS FALSE AS A UNIVERSAL RELATION
     It was an artifact of class-number/conductor correlation in the early sample.
     At fixed h=2 with conductor 91, the law predicts 3.43; observed 1.30.

  4. CLASS NUMBER STILL HAS SOME EFFECT
     Comparing fixed-conductor pairs would help isolate it. The data suggests both 
     class number AND conductor contribute, with conductor possibly dominant at 
     large conductors.

REVISED INTERPRETATION

  The empirical scaling is multivariate in (h, conductor, N). The simple 1-variable
  fit was inadequate. The actual structural observation is:
  
    "Inert prime amplitudes systematically grow with conductor.
     At fixed conductor, higher class number gives some additional inert amplitude.
     The ratio split/inert tracks the inverse of inert amplitude."
  
  The conductor effect is plausibly the noise-floor effect at higher zero density,
  but the systematic growth suggests genuine structural content.

CHARACTER RECOVERY: Still 100% in 14/14 fields. The qualitative pattern is robust.

NEXT EXPERIMENTS

  1. More fixed-h conductor sweeps (h=3 at conductors 23, 31, 59, 83)
  2. Fixed-CONDUCTOR varying-h (harder; few small conductors have multiple h values)
  3. The (h, conductor) → ratio surface mapped systematically
  4. Theoretical: derive inert amplitude as f(N, conductor) from explicit formula
"""
ax.text(0.0, 0.97, summary, transform=ax.transAxes,
        fontsize=8.5, color='white', family='monospace', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#0a0a14', edgecolor='#555'))

plt.suptitle("Disentangled Class Number vs Conductor — 14 Fields",
             color='white', fontsize=14, weight='bold', y=0.995)
plt.savefig(f"{OUTDIR}/disentangled.png", dpi=130, bbox_inches='tight', facecolor='#040408')
print(f"Saved: {OUTDIR}/disentangled.png")
