import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

"""
Berry-Keating xp through the knife.

  xp-honest : E_k = N_smooth^{-1}(k)   -- the PROVEN part of Berry-Keating
                                          (semiclassical density of xp = smooth zero count).
                                          xp has NO periodic orbits -> NO fluctuations -> NO arithmetic, by construction.
  xp+orbits : same levels, displaced by the prime periodic-orbit fluctuation (trace formula).
                                          This INSERTS the primes by hand -> CIRCULAR. Shows the trap & the duality.

Compare against: real zeros (positive, ~240) and the GUE null (~0.98, from hp_never_synced.py).
"""
import numpy as np
rng = np.random.default_rng(20260423)

g_all = np.loadtxt(_d("riemann_zeros_100k.txt"))
N = 6000
g = g_all[:N].copy()

# ---- von Mangoldt test frequencies ----
def vonmangoldt(n):
    for p in range(2, n+1):
        if n % p == 0:
            m=n
            while m%p==0: m//=p
            return np.log(p) if m==1 else 0.0
    return 0.0
ns=np.arange(2,41); u=np.log(ns)
Lam=np.array([vonmangoldt(int(n)) for n in ns]); ispp=Lam>0

def witness(gam,uu): return np.abs(np.cos(np.outer(uu,gam)).sum(axis=1))
def knife(gam):
    S=witness(gam,u); pp=S[ispp].mean(); comp=S[~ispp].mean(); return S,pp,comp,pp/comp

# ---- smooth counting and its inverse (Berry-Keating density) ----
def Nsm(E): return (E/(2*np.pi))*(np.log(E/(2*np.pi))-1)+7/8
Egrid=np.linspace(5.0,9000.0,600000); Ngrid=Nsm(Egrid)
invN=lambda kk: np.interp(kk,Ngrid,Egrid)
k=np.arange(1,N+1)
E_xp = invN(k-0.5)                       # Berry-Keating semiclassical spectrum (honest)

# ---- prime periodic-orbit fluctuation (trace formula) -> CIRCULAR injection ----
def sieve(P):
    s=np.ones(P+1,bool); s[:2]=False
    for i in range(2,int(P**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
primes=sieve(3000)
rho_sm=lambda E:(1/(2*np.pi))*np.log(E/(2*np.pi))
def Nfl(E):
    tot=np.zeros_like(E)
    for p in primes:
        lp=np.log(p)
        for m in (1,2,3):
            amp=p**(-m/2)
            if amp<1e-7: break
            tot += (1.0/m)*amp*np.sin(m*lp*E)
    return -(1/np.pi)*tot
E_circ = E_xp - Nfl(E_xp)/rho_sm(E_xp)   # zeros reconstructed FROM primes (first order)

# ---- run ----
res = {
  "real            ": knife(g),
  "xp-honest       ": knife(E_xp),
  "xp+orbits(CIRC) ": knife(E_circ),
}
print(f"N = {N};  GUE null (prior run) = 0.98\n")
print(f"{'spectrum':>17} {'mean|S| pp':>11} {'mean|S| comp':>12} {'ratio':>8}")
for name,(S,pp,comp,r) in res.items():
    print(f"{name:>17} {pp:>11.2f} {comp:>12.2f} {r:>8.2f}")

print(f"\n{'n':>3} {'log n':>7} {'type':>10} {'real':>8} {'xp-honest':>10} {'xp+CIRC':>9}")
Sr=res['real            '][0]; Sx=res['xp-honest       '][0]; Sc=res['xp+orbits(CIRC) '][0]
for i,n in enumerate(ns):
    if n in (2,3,5,7,4,9,6,8,10,11,13):
        t='PRIME-POW' if ispp[i] else 'composite'
        print(f"{n:>3} {u[i]:>7.3f} {t:>10} {Sr[i]:>8.0f} {Sx[i]:>10.1f} {Sc[i]:>9.0f}")

# how close did the circular reconstruction get to the actual zeros?
err=np.abs(E_circ-g)
print(f"\ncircular reconstruction vs true zeros: median |E_circ - gamma| = {np.median(err):.3f}")
print("(primes were used to MAKE these levels -> any prime resonance is inserted, not derived)")
