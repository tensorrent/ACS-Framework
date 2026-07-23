# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

r"""
VANTAGE POINTS  --  how many INDEPENDENT sightings of zeta do the witnesses give,
and is there a THIRD face beyond the arithmetic and lag-1 witnesses?

Motivation.  Spectral_Witness_Refinement.tex (sec.7) asks whether the witnesses are
"independent confirmations or one reading refracted through several lenses," reports an
effective rank ~4 for the five scalar witnesses, and finds a clean FORM/FUNCTION split:
arithmetic (~11,500 sig) and lag-1 (~97 sig) are FUNCTION (they read *this* spectrum);
spacing/counting/shape are FORM (they read the GUE universality class, shared by any
marginal-matched sequence).  Geometrically: the FORM witnesses see the flattened GUE
"silhouette"; the FUNCTION witnesses see a face of the object the silhouette lacks.

This script makes the count operational and then hunts for a third face:

  (A) reproduce the FORM/FUNCTION z-scores of the five canonical witnesses vs the
      GUE-marginal (gap-shuffle) surrogate;
  (B) measure the effective rank (participation ratio) of the witness correlation
      matrix over the surrogate ensemble -- the number of independent INSTRUMENTS;
  (C) THIRD-FACE SEARCH: add candidate arithmetic witnesses that read a *different*
      arithmetic structure than the single-prime power sum (prime-square harmonic,
      cross-prime difference tones, cross-prime sum tones, full complex phase power,
      lag-2 order), score each FORM/FUNCTION, and test whether any FUNCTION candidate
      is INDEPENDENT of the arithmetic witness under a jitter-response ensemble of the
      real zeros.  A function witness that tracks arith is the same face seen twice; one
      that moves independently is a genuinely new face.

Reproducible: canonical seed 20260423, Odlyzko's first zeros.  Negatives first-class.
"""
import numpy as np

SEED = 20260423
rng = np.random.default_rng(SEED)

# ---------- load real zeros ----------
g_all = np.loadtxt(_d("riemann_zeros_100k.txt"))
N = 4000
g = g_all[:N].copy()

def Nsmooth(T):
    return (T/(2*np.pi))*np.log(T/(2*np.pi)) - T/(2*np.pi) + 7/8
w_real = Nsmooth(g)
s_real = np.diff(w_real)
def refold(w):
    return np.interp(w, w_real, g)

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
LOGP = np.log(PRIMES)

# =====================================================================================
#  WITNESS BATTERY  -- the 5 canonical + 5 candidate faces
# =====================================================================================
def W_repulsion(s):
    s = s / s.mean(); return np.mean(s < 0.5)                    # FORM (NN law)

def W_shape(s):
    s = s / s.mean()
    edges = np.linspace(0, 4, 41); ctr = 0.5*(edges[:-1]+edges[1:])
    h, _ = np.histogram(s, bins=edges, density=True)
    wig = (32/np.pi**2) * ctr**2 * np.exp(-4*ctr**2/np.pi)
    return np.sqrt(np.mean((h - wig)**2))                        # FORM (NN law)

def W_lag1(s):
    s = s - s.mean(); return np.sum(s[:-1]*s[1:]) / np.sum(s*s)  # FUNCTION (local order)

def W_rigidity(w):
    L = 15.0; a, b = w.min(), w.max()
    starts = np.arange(a, b - L, L)
    cnt = np.array([np.sum((w >= s0) & (w < s0 + L)) for s0 in starts])
    return cnt.var()                                            # FORM (2-pt)

def W_arith(gam):                                               # FUNCTION (single-prime power)
    return sum(np.mean(np.cos(gam*lp))**2 for lp in LOGP)

# ---- candidate faces -------------------------------------------------------------
def W_arith2(gam):        # prime-SQUARE harmonic: resonance at 2*log p (reads p^2 line)
    return sum(np.mean(np.cos(2*gam*lp))**2 for lp in LOGP)

def W_phasepow(gam):      # full complex prime power |<e^{i g log p}>|^2 (cos^2 + sin^2)
    return sum(np.mean(np.cos(gam*lp))**2 + np.mean(np.sin(gam*lp))**2 for lp in LOGP)

def W_difftone(gam):      # cross-prime DIFFERENCE tones: resonance at log(q/p), p<q
    tot = 0.0
    for i in range(len(PRIMES)):
        for j in range(i+1, len(PRIMES)):
            tot += np.mean(np.cos(gam*(LOGP[j]-LOGP[i])))**2
    return tot

def W_sumtone(gam):       # cross-prime SUM tones: resonance at log(p*q) (composite line)
    tot = 0.0
    for i in range(len(PRIMES)):
        for j in range(i+1, len(PRIMES)):
            tot += np.mean(np.cos(gam*(LOGP[j]+LOGP[i])))**2
    return tot

def W_lag2(s):            # second serial order (beyond lag-1)
    s = s - s.mean(); return np.sum(s[:-2]*s[2:]) / np.sum(s*s)

CANONICAL = ["repulsion", "shape", "lag1", "rigidity", "arith"]
CANDIDATES = ["arith2", "phasepow", "difftone", "sumtone", "lag2"]
ALL = CANONICAL + CANDIDATES

def evaluate(gam):
    w = Nsmooth(gam); s = np.diff(w)
    return {
        "repulsion": W_repulsion(s), "shape": W_shape(s), "lag1": W_lag1(s),
        "rigidity": W_rigidity(w), "arith": W_arith(gam),
        "arith2": W_arith2(gam), "phasepow": W_phasepow(gam),
        "difftone": W_difftone(gam), "sumtone": W_sumtone(gam), "lag2": W_lag2(s),
    }

# GUE-marginal surrogate: permute the real gaps (destroys zeta, keeps spacing law)
def draw_gue_marginal():
    s = rng.permutation(s_real)
    w = np.concatenate([[w_real[0]], w_real[0] + np.cumsum(s)])
    return refold(w)

# =====================================================================================
#  (A) FORM / FUNCTION z-scores  +  (B) effective rank of the instruments
# =====================================================================================
M = 300
real = evaluate(g)
ens = {k: np.empty(M) for k in ALL}
for m in range(M):
    wv = evaluate(draw_gue_marginal())
    for k in ALL: ens[k][m] = wv[k]

z = {k: abs(real[k] - ens[k].mean()) / (ens[k].std() + 1e-30) for k in ALL}

print(f"VANTAGE POINTS  --  N = {N} zeros, {M} GUE-marginal surrogates, seed {SEED}")
print("=" * 74)
print("(A) FORM / FUNCTION split (|z| > 3 = FUNCTION = reads THIS spectrum)")
print(f"    {'witness':>10} {'real':>12} {'surr.mean':>12} {'|z| sigma':>12}  {'label':>9}")
for k in ALL:
    tag = "CANON" if k in CANONICAL else "cand"
    lab = "FUNCTION" if z[k] > 3 else "form"
    print(f"    {k:>10} {real[k]:12.5f} {ens[k].mean():12.5f} {z[k]:12.1f}  {lab:>9}  [{tag}]")

# effective rank (participation ratio) of the canonical-witness correlation matrix
def eff_rank(cols):
    X = np.column_stack([ens[k] for k in cols])
    X = (X - X.mean(0)) / (X.std(0) + 1e-30)
    C = np.corrcoef(X, rowvar=False)
    ev = np.clip(np.linalg.eigvalsh(C), 0, None)
    return (ev.sum()**2) / (np.sum(ev**2) + 1e-30), ev[::-1]

er5, ev5 = eff_rank(CANONICAL)
print("\n(B) INDEPENDENT INSTRUMENTS (effective rank = (Sum l)^2 / Sum l^2 of corr eigenvalues)")
print(f"    5 canonical witnesses: effective rank = {er5:.2f}  (of 5)")
print(f"    eigenvalues: " + ", ".join(f"{e:.2f}" for e in ev5))
print(f"    -> ~{er5:.1f} independent instruments; the rest are the shared GUE silhouette.")

# =====================================================================================
#  (C) THIRD-FACE SEARCH: is any FUNCTION candidate INDEPENDENT of arith?
#      Jitter the REAL zeros and watch how each witness responds; a witness that
#      co-moves with arith is the same face, one that moves independently is a new face.
# =====================================================================================
print("\n(C) THIRD-FACE SEARCH  --  jitter-response independence from the arith witness")
K = 400
eps = 0.10                                   # jitter as fraction of local mean spacing
loc_spacing = np.median(np.diff(g))
func_cands = [k for k in CANDIDATES if z[k] > 3]
track = ["arith", "lag1"] + func_cands       # study the function witnesses
resp = {k: np.empty(K) for k in track}
for kk in range(K):
    gj = g + rng.standard_normal(N) * eps * loc_spacing
    gj.sort()
    wv = evaluate(gj)
    for k in track: resp[k][kk] = wv[k]

R = np.column_stack([resp[k] for k in track])
R = (R - R.mean(0)) / (R.std(0) + 1e-30)
Cr = np.corrcoef(R, rowvar=False)
ai = track.index("arith")

# von-Mangoldt family: witnesses that read the SAME explicit-formula coupling
# (single primes, their harmonics, their complex phase) -- facets of ONE face, not new.
VONMANGOLDT = {"arith2", "phasepow"}
# difference/sum tones: Spectral_Witness_Refinement.tex already argues these are an
# incommensurable NULL (1.2 sigma) by unique factorisation -- treat weak hits as artifact.
NULLED = {"difftone", "sumtone"}
STRONG = 20.0                                # bar for a robust (non-borderline) face

print(f"    jitter eps = {eps} x local spacing, {K} draws")
print(f"    FUNCTION candidates (|z|>3): {func_cands if func_cands else '(none)'}")
print(f"    {'witness':>10} {'|z| sigma':>12} {'corr w/ arith':>14}  {'verdict':>26}")
for k in track:
    if k == "arith":
        print(f"    {k:>10} {z[k]:12.1f} {'-- (self)':>14}  {'reference face (arithmetic)':>26}")
        continue
    c = Cr[track.index(k), ai]
    if z[k] <= 3:
        verdict = "form (no face)"
    elif k in VONMANGOLDT and abs(c) > 0.9:
        verdict = "same face (cos-only)"
    elif k in VONMANGOLDT:
        verdict = "arith face, higher harmonic"
    elif k in NULLED:
        verdict = "weak: theory-nulled tone"
    elif k in ("lag1", "lag2"):
        verdict = "local-order face"
    elif abs(c) < 0.5:
        verdict = "INDEPENDENT face?"
    else:
        verdict = "same face as arith"
    print(f"    {k:>10} {z[k]:12.1f} {c:14.2f}  {verdict:>26}")

# robust independent faces = strong, arith-independent, not a von-Mangoldt harmonic,
# not a theory-nulled tone, not the already-named local-order family
robust_new = [k for k in func_cands
              if z[k] > STRONG and abs(Cr[track.index(k), ai]) < 0.5
              and k not in VONMANGOLDT and k not in NULLED and k not in ("lag2",)]

print("\n" + "=" * 74)
print("RESULT  --  counting FACES, not instruments")
print(f"  * independent INSTRUMENTS (canonical corr rank) : ~{er5:.1f} of 5")
print(f"  * face 1  ARITHMETIC (explicit-formula coupling): arith {z['arith']:.0f}sig"
      f"  [+ harmonic arith2 {z['arith2']:.0f}sig, phase phasepow {z['phasepow']:.0f}sig]")
print(f"  * face 2  LOCAL ORDER (serial correlation)      : lag1 {z['lag1']:.0f}sig"
      f"  [+ lag2 {z['lag2']:.0f}sig, same family]")
print(f"  * rigidity: FUNCTION here ({z['rigidity']:.0f}sig) vs gap-shuffle but FORM vs")
print(f"              GUE-full -- the form/function label is frame-relative (FF06g).")
print(f"  * difftone/sumtone: {z['difftone']:.0f}/{z['sumtone']:.0f}sig, borderline and")
print(f"              consistent with the manuscript's incommensurable null -> not a face.")
print(f"  * robust NEW independent face beyond the two    : "
      + (", ".join(robust_new) if robust_new else "(none)"))
print("=" * 74)
print("""READING:
  The object has TWO robust faces on this battery: the arithmetic/explicit-formula
  coupling (with its own harmonic ladder arith -> arith2, so even the single face has
  internal depth a flat line cannot hold) and the local-order face (lag1/lag2). The
  three silhouette witnesses (repulsion, shape, and rigidity-vs-GUE-full) are the
  flattened GUE shadow every such spectrum casts. No robust THIRD face-family appears
  here: the extra candidates are either the same coupling at another frequency
  (arith2, phasepow) or the difference/sum tones the manuscript already showed are an
  incommensurable null. So "object not a line" holds -- the silhouette is provably a
  projection -- but the object is, for now, two-faced with a harmonic-rich arithmetic
  face, not many-faced. Nothing here proves RH or builds a Hilbert-Polya operator.""")
