import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

"""
Signed knife (C6/C7) + L-function character-sign test (C8).
Upgrades |S(u)| -> SIGNED F(u)=sum cos(u*gamma), which keeps the explicit-formula sign.

  zeta : F(log p^m) should be NEGATIVE (C6) with magnitude ~ Lambda(p^m)/sqrt(p^m) (C7).
  L(s,chi_d) for quadratic chi: the log-p peak should FLIP with chi(p)=(d/p) Kronecker (C8).
     => sign(F_chi(log p)) should equal sign(F_zeta(log p)) * chi(p).
"""
import numpy as np, os
g = np.loadtxt(_d("riemann_zeros_100k.txt"))[:2000]

def F(gam, uu):                      # SIGNED witness
    return np.cos(np.outer(uu, gam)).sum(axis=1)

# ---------- C6 / C7 on zeta ----------
ns = np.arange(2, 21); u = np.log(ns)
def lam_w(n):
    for p in range(2, n+1):
        if n % p == 0:
            m=n
            while m%p==0: m//=p
            return (np.log(p)/np.sqrt(n)) if m==1 else 0.0
    return 0.0
w = np.array([lam_w(int(n)) for n in ns])
Fz = F(g, u)
print(f"ZETA signed witness (N={len(g)}):   C6 = negative at prime powers,  C7 = magnitude ~ Lambda/sqrt(n)")
print(f"{'n':>3} {'log n':>7} {'F(signed)':>11} {'sign':>5} {'Lam/sqrt(n)':>12}  type")
zeta_sign = {}
for n,uu,f,ww in zip(ns,u,Fz,w):
    s = '-' if f<0 else '+'
    if ww>0: zeta_sign[int(n)] = (-1 if f<0 else 1)
    print(f"{n:>3} {uu:>7.3f} {f:>11.1f} {s:>5} {ww:>12.3f}  {'PRIME-POW' if ww>0 else 'composite'}")
ppmask = w>0
print(f"\nC6 check: fraction of prime-powers with NEGATIVE F = "
      f"{np.mean(Fz[ppmask]<0):.2f}   (want 1.00)")
# C7: correlation of |F| with Lambda/sqrt(n) on prime powers
print(f"C7 check: corr(|F|, Lambda/sqrt(n)) on prime-powers = "
      f"{np.corrcoef(np.abs(Fz[ppmask]), w[ppmask])[0,1]:.2f}")

# ---------- C8: quadratic Dirichlet L-functions ----------
def chi_quad(d, p):                  # Kronecker symbol (d/p), p prime
    if d % p == 0: return 0
    if p == 2:
        r = d % 8
        return 1 if r in (1,7) else -1
    ls = pow(d % p, (p-1)//2, p)
    return 1 if ls == 1 else (-1 if ls == p-1 else 0)

files = {
    -35:  _d("disentangled/zeros_chi_-35.txt"),
    -91:  _d("disentangled/zeros_chi_-91.txt"),
    -104: _d("cyclotomic_and_h6/zeros_chi_-104.txt"),
}
ps = [2,3,5,7,11,13,17,19]
print("\n" + "="*64)
print("C8: does sign(F_chi(log p)) flip with the Kronecker symbol (d/p)?")
print("    expected sign(F_chi) = sign(F_zeta) * chi(p)")
for d, fn in files.items():
    if not os.path.exists(fn):
        print(f"  [missing {fn}]"); continue
    z = np.loadtxt(fn); z = z[np.isfinite(z)]
    Fc = F(z, np.log(ps))
    print(f"\nL(s, chi_{d})   N={len(z)} zeros")
    print(f"{'p':>3} {'F_chi':>9} {'sgn':>4} {'chi(p)':>7} {'zeta sgn':>9} {'predict':>8} {'match':>6}")
    hits=tot=0
    for p, f in zip(ps, Fc):
        c = chi_quad(d, p)
        zs = zeta_sign.get(p, None)
        got = -1 if f < 0 else 1
        if c == 0 or zs is None:
            print(f"{p:>3} {f:>9.2f} {('-' if f<0 else '+'):>4} {c:>7} {str(zs):>9} {'ramified' if c==0 else '-':>8} {'-':>6}")
            continue
        pred = zs * c
        ok = (got == pred); hits += ok; tot += 1
        print(f"{p:>3} {f:>9.2f} {('-' if f<0 else '+'):>4} {c:>+7d} {zs:>+9d} {pred:>+8d} {('YES' if ok else 'no'):>6}")
    print(f"   --> C8 sign match: {hits}/{tot}")
