import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

import numpy as np
rng = np.random.default_rng(20260423)  # canonical seed

# --- load zeros ---
g = np.loadtxt(_d("riemann_zeros_100k.txt"))
N = 30000
g = g[:N]

# --- von Mangoldt: which integers are prime powers ---
def is_prime_power(n):
    m=n; 
    for p in range(2,int(n**0.5)+1):
        if m%p==0:
            while m%p==0: m//=p
            return m==1
    return True  # n prime
def vonmangoldt(n):
    # returns log p if n=p^k else 0
    for p in range(2,n+1):
        if n%p==0:
            m=n
            while m%p==0: m//=p
            return np.log(p) if m==1 else 0.0
    return 0.0

ns = np.arange(2,41)
u  = np.log(ns)                      # test frequencies = log n
Lam= np.array([vonmangoldt(int(n)) for n in ns])
ispp = Lam>0

# --- witness S(u) = sum_k cos(u * gamma_k) ---
def witness(gam, uu):
    return np.abs(np.cos(np.outer(uu, gam)).sum(axis=1))

S_real = witness(g, u)

# --- internal control: prime-powers vs composites on the REAL spectrum ---
print("=== REAL zeros: prime-power frequencies vs composites (internal control) ===")
print(f"{'n':>3} {'log n':>7} {'|S(u)|':>10} {'Lambda':>7}  type")
for n,uu,s,l in zip(ns,u,S_real,Lam):
    print(f"{n:>3} {uu:>7.3f} {s:>10.1f} {l:>7.3f}  {'PRIME-POWER' if l>0 else 'composite'}")
print(f"\nmean |S| at prime-powers : {S_real[ispp].mean():8.1f}")
print(f"mean |S| at composites   : {S_real[~ispp].mean():8.1f}")
print(f"ratio (pp/comp)          : {S_real[ispp].mean()/S_real[~ispp].mean():8.2f}")

# --- shuffle knife: gap-matched surrogate (preserves spacing distribution = FORM) ---
gaps = np.diff(g)
M = 300
S_sur = np.zeros((M, len(u)))
for i in range(M):
    gp = rng.permutation(gaps)
    gs = np.empty(N); gs[0]=g[0]; gs[1:]=g[0]+np.cumsum(gp)
    S_sur[i] = witness(gs, u)

mu = S_sur.mean(axis=0); sd = S_sur.std(axis=0)
z  = (S_real - mu)/sd
print("\n=== SHUFFLE KNIFE: real vs gap-matched surrogate (FORM preserved, order destroyed) ===")
print(f"{'n':>3} {'type':>12} {'z-score':>9}")
for n,zz,pp in zip(ns,z,ispp):
    print(f"{n:>3} {('PRIME-POWER' if pp else 'composite'):>12} {zz:>9.2f}")
print(f"\nmean z at prime-powers : {z[ispp].mean():7.2f}  (FUNCTION present if >> 0)")
print(f"mean z at composites   : {z[~ispp].mean():7.2f}  (should be ~ 0)")
print(f"surrogate self-check: its own pp/comp ratio = {S_sur.mean(axis=0)[ispp].mean()/S_sur.mean(axis=0)[~ispp].mean():.2f} (form carries NO arithmetic if ~1)")
