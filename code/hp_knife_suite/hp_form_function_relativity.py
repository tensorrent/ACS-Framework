# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

r"""
FORM/FUNCTION RELATIVITY  --  "one witness's form is another witness's function."

The shuffle-knife (hp_knife.py, and Spectral_Witness_Refinement.tex sec.15) labels a
spectral witness FUNCTION if its value on the real zeros deviates from a *surrogate*
ensemble, and FORM if it does not.  The label is therefore NOT a property of the
witness alone: it is a property of the pair (witness, reference measure nu).  The
reference nu is the "perspective" -- literally the reference measure d mu / d nu that
already appears in the BCH-TE lemma of Form_Function_and_Asymmetry.tex (Lemma 2.9),
where the information asymmetry is measured against a *chosen* nu.

This script makes the relativity operational.  It evaluates the SAME witnesses against
a LADDER of reference frames ordered by how much structure each preserves:

    Poisson   <   GUE-marginal (gap-shuffle)   <   GUE-full (bulk)   <   zeta itself
    (no repulsion)   (NN-spacing law only)      (full RMT 2-pt)        (arithmetic)

A witness is FUNCTION relative to a frame iff it reads structure the frame does NOT
preserve.  As the frame is refined (left to right), witnesses fall from FUNCTION to
FORM one class at a time -- a staircase.  The arithmetic witness is the last to fall:
it is FUNCTION relative to every frame coarser than zeta itself.

Reproducible: canonical seed 20260423, Odlyzko's first zeros.  Negatives first-class.
"""
import sys
import numpy as np
import time

SEED = 20260423
rng = np.random.default_rng(SEED)

# The GUE-full frame diagonalises dense N x N Hermitian matrices and is slow
# (~7 min at N=4000, 40 draws).  It is OFF by default; pass --full to include it.
# The two exact frames (Poisson, GUE-marginal) are ~2 s and already carry the thesis.
WITH_FULL = "--full" in sys.argv

# ---------- load real zeros ----------
g_all = np.loadtxt(_d("riemann_zeros_100k.txt"))
N = 4000
g = g_all[:N].copy()

# Riemann-von Mangoldt smooth counting -> unfolded positions (unit mean spacing)
def Nsmooth(T):
    return (T/(2*np.pi))*np.log(T/(2*np.pi)) - T/(2*np.pi) + 7/8
w_real = Nsmooth(g)
s_real = np.diff(w_real)
def refold(w):                              # map unfolded positions back to real density
    return np.interp(w, w_real, g)

# =====================================================================================
#  WITNESSES  (each a single scalar, ordered by how much structure it reads)
# =====================================================================================
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def W_repulsion(s):        # reads: NN-spacing law only  (level repulsion depth)
    s = s / s.mean()
    return np.mean(s < 0.5)                  # fraction of small gaps; Poisson~0.39, GUE~0.16

def W_shape(s):            # reads: NN-spacing law only  (L2 distance to GUE Wigner surmise)
    s = s / s.mean()
    edges = np.linspace(0, 4, 41); ctr = 0.5*(edges[:-1]+edges[1:])
    h, _ = np.histogram(s, bins=edges, density=True)
    wig = (32/np.pi**2) * ctr**2 * np.exp(-4*ctr**2/np.pi)
    return np.sqrt(np.mean((h - wig)**2))

def W_lag1(s):             # reads: local serial ORDER (beyond the marginal)
    s = s - s.mean()
    return np.sum(s[:-1]*s[1:]) / np.sum(s*s)

def W_rigidity(w):         # reads: long-range 2-point correlation (number variance)
    L = 15.0; a, b = w.min(), w.max()
    starts = np.arange(a, b - L, L)
    cnt = np.array([np.sum((w >= s0) & (w < s0 + L)) for s0 in starts])
    return cnt.var()

def W_arith(gam):          # reads: zeta ARITHMETIC (prime resonance power)
    return sum(np.mean(np.cos(gam*np.log(p)))**2 for p in PRIMES)

WITNESSES = ["repulsion", "shape", "lag1", "rigidity", "arith"]
def evaluate(gam):
    w = Nsmooth(gam); s = np.diff(w)
    return {"repulsion": W_repulsion(s), "shape": W_shape(s),
            "lag1": W_lag1(s), "rigidity": W_rigidity(w), "arith": W_arith(gam)}

# =====================================================================================
#  REFERENCE FRAMES  (nulls), ordered by increasing structure preserved
# =====================================================================================
def draw_poisson():                          # no repulsion, density matched
    s = rng.exponential(1.0, N-1)
    w = np.concatenate([[w_real[0]], w_real[0] + np.cumsum(s)])
    w = (w - w[0])/(w[-1]-w[0])*(w_real[-1]-w_real[0]) + w_real[0]
    return refold(w)

def draw_gue_marginal():                     # exact NN-spacing law, order+arithmetic destroyed
    s = rng.permutation(s_real)
    w = np.concatenate([[w_real[0]], w_real[0] + np.cumsum(s)])
    return refold(w)

def draw_gue_full():                         # full RMT 2-point structure, arithmetic destroyed
    A = rng.standard_normal((N, N)) + 1j*rng.standard_normal((N, N))
    H = (A + A.conj().T) / 2
    ev = np.linalg.eigvalsh(H); ev = ev/ev.std()
    lo, hi = np.quantile(ev, 0.1), np.quantile(ev, 0.9)   # keep the bulk (semicircle edges unfold poorly)
    ev = ev[(ev >= lo) & (ev <= hi)]
    x = np.clip(ev/2, -1, 1)
    F = (ev*np.sqrt(np.clip(4-ev**2, 0, None))/2 + 2*np.arcsin(x))/(2*np.pi) + 0.5
    w = (F - F[0])/(F[-1]-F[0])*(w_real[-1]-w_real[0]) + w_real[0]
    return refold(np.clip(w, w_real[0], w_real[-1]))

FRAMES = [("Poisson", draw_poisson, 200),
          ("GUE-marginal", draw_gue_marginal, 200)]
if WITH_FULL:
    FRAMES.append(("GUE-full(bulk)", draw_gue_full, 40))

# =====================================================================================
#  DRIVER: z-score of each witness against each frame; label FUNCTION if |z| > 3
# =====================================================================================
Z_THRESH = 3.0
real = evaluate(g)

print(f"FORM/FUNCTION RELATIVITY  --  N = {N} zeros, seed {SEED}")
print("A witness is FUNCTION vs a frame iff it reads structure that frame does not preserve.")
if not WITH_FULL:
    print("(fast mode: 2 exact frames.  Pass --full to add GUE-full(bulk), ~7 min.)")
print()

z = {}
for name, draw, M in FRAMES:
    t0 = time.time()
    ens = {k: [] for k in WITNESSES}
    for _ in range(M):
        wv = evaluate(draw())
        for k in WITNESSES: ens[k].append(wv[k])
    for k in WITNESSES:
        arr = np.array(ens[k])
        z[(k, name)] = abs(real[k] - arr.mean()) / (arr.std() + 1e-12)
    print(f"  frame '{name}':  {M} draws, {time.time()-t0:.1f}s")

hdr = f"\n{'witness':>10} | " + " | ".join(f"{n:>20}" for n, _, _ in FRAMES) + " | reads"
print(hdr); print("-"*len(hdr))
reads = {"repulsion":"NN-spacing law", "shape":"NN-spacing law",
         "lag1":"local order", "rigidity":"2-pt correlation", "arith":"zeta arithmetic"}
for k in WITNESSES:
    cells = []
    for name, _, _ in FRAMES:
        lab = "FUNCTION" if z[(k, name)] > Z_THRESH else "FORM"
        cells.append(f"{z[(k,name)]:8.1f}sig {lab:>8}")
    print(f"{k:>10} | " + " | ".join(cells) + f" | {reads[k]}")

print(f"""
READING (threshold |z| > {Z_THRESH:.0f} = FUNCTION):
  * Refining the frame (Poisson -> GUE-marginal -> GUE-full) turns witnesses FORM one
    class at a time -- a staircase.  The label is a coordinate on (witness x frame),
    not a property of the witness: the SAME shape/repulsion witness is FUNCTION in the
    Poisson frame and FORM in a repulsion-matched frame.
  * 'arith' is FUNCTION in every frame short of zeta itself: it is the irreducibly
    zeta-specific content (the explicit-formula coupling), never absorbed into FORM.
  * The terminal frame 'zeta itself' makes every witness FORM (z = 0 against itself),
    including arith -- consistent with, but not a proof of, RH.
  * The reference frame nu is exactly the d mu / d nu of the BCH-TE lemma: form/function
    is measured against a *chosen* perspective, and choosing it differently relabels.
NOTE: GUE-full(bulk) is a finite-N, unfolded ensemble (approximate); the two exact
frames Poisson and GUE-marginal carry the argument.  Negatives kept first-class.
""")
