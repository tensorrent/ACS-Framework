# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

"""
NOT-EVER-FULLY-SYNCED test.
Hold spectral DENSITY fixed (Riemann-von Mangoldt smooth counting), vary only the
fine structure (the 'sync' property). Run the prime-power resonance knife on each.

  real    : never synced  + arithmetic   (positive control)
  GUE     : never synced  + NO arithmetic (Brad's 'never synced' made literal)
  lattice : fully synced  + NO arithmetic (opposite pole)

If 'never synced' were SUFFICIENT, GUE would resonate at u=log(prime power).
"""
import numpy as np
rng = np.random.default_rng(20260423)   # canonical seed

# ---------- load real zeros ----------
g_all = np.loadtxt(_d("riemann_zeros_100k.txt"))
N = 6000
g = g_all[:N].copy()

# ---------- smooth counting N(T) (Riemann-von Mangoldt) and its inverse ----------
def Nsmooth(T):
    return (T/(2*np.pi))*np.log(T/(2*np.pi)) - T/(2*np.pi) + 7/8
w_real = Nsmooth(g)                      # unfolded positions of real zeros (~ k)
# inverse via interpolation on the real (w, gamma) pairs => guarantees identical density
def refold(w):
    return np.interp(w, w_real, g)

# ---------- von Mangoldt ----------
def vonmangoldt(n):
    for p in range(2, n+1):
        if n % p == 0:
            m = n
            while m % p == 0: m //= p
            return np.log(p) if m == 1 else 0.0
    return 0.0
ns   = np.arange(2, 41)
u    = np.log(ns)
Lam  = np.array([vonmangoldt(int(n)) for n in ns])
ispp = Lam > 0

# ---------- witness ----------
def witness(gam, uu):
    return np.abs(np.cos(np.outer(uu, gam)).sum(axis=1))

# ---------- GUE surrogate: true level repulsion, density matched, NO arithmetic ----------
A = (rng.standard_normal((N, N)) + 1j*rng.standard_normal((N, N)))
H = (A + A.conj().T) / 2
ev = np.linalg.eigvalsh(H)               # GUE eigenvalues
ev = ev / ev.std()                       # scale to semicircle radius 2 (var 1)
x  = np.clip(ev/2, -1, 1)
F  = (ev*np.sqrt(np.clip(4-ev**2,0,None))/2 + 2*np.arcsin(x))/(2*np.pi) + 0.5
w_gue = N * F                            # unfolded, unit mean spacing
w_gue = w_gue - w_gue[0] + w_real[0]     # align start
w_gue = np.clip(w_gue, w_real[0], w_real[-1])
g_gue = refold(w_gue)

# ---------- lattice surrogate: perfectly synced, density matched ----------
w_lat = w_real[0] + np.arange(N)*((w_real[-1]-w_real[0])/(N-1))
g_lat = refold(w_lat)

# ---------- run knife ----------
def report(name, gam):
    S = witness(gam, u)
    pp, comp = S[ispp].mean(), S[~ispp].mean()
    return name, S, pp, comp, pp/comp

rows = [report("real   ", g), report("GUE    ", g_gue), report("lattice", g_lat)]

print(f"N = {N} levels;  test frequencies u = log n, n=2..40")
print(f"{'spectrum':>8} {'mean|S| pp':>12} {'mean|S| comp':>13} {'ratio pp/comp':>14}")
for name,S,pp,comp,r in rows:
    print(f"{name:>8} {pp:>12.2f} {comp:>13.2f} {r:>14.3f}")

# spacing-statistics sanity: nearest-neighbour spacing CV (unfolded) -- rigidity check
def cv(w):
    d = np.diff(w); return d.std()/d.mean()
print(f"\nrigidity check  (unfolded NN-spacing coeff. of variation):")
print(f"   real    CV = {cv(w_real):.3f}")
print(f"   GUE     CV = {cv(w_gue):.3f}   (GUE ~0.42 ; Poisson =1 ; lattice =0)")
print(f"   lattice CV = {cv(w_lat):.3f}")

# per-frequency detail for the first primes / prime-powers
print(f"\n{'n':>3} {'log n':>7} {'type':>11} {'real':>9} {'GUE':>9} {'lattice':>9}")
Sr, Sg, Sl = rows[0][1], rows[1][1], rows[2][1]
for i,n in enumerate(ns):
    if n in (2,3,4,5,7,8,9,11,13,6,10,12,15):
        t = 'PRIME-POW' if ispp[i] else 'composite'
        print(f"{n:>3} {u[i]:>7.3f} {t:>11} {Sr[i]:>9.1f} {Sg[i]:>9.1f} {Sl[i]:>9.1f}")
