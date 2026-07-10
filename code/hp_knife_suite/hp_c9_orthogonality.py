# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

"""
C9 -- Selberg orthogonality across the panel.
Each L-function's witness phase v_i(p)=W_i(p)/|W_i(p)| ~ chi_i(p)*e^{i phi0_i}.
Cross-correlation from ZEROS:   M_zero[i,j] = | mean_p  v_i(p) conj(v_j(p)) |
Character truth:                M_true[i,j] = | mean_p  chi_i(p) conj(chi_j(p)) |
Selberg: diagonal ~1, off-diagonal -> 0 (bounded; here at the finite-prime floor).
Real test: does M_zero reproduce M_true pair-by-pair (not just both small)?
"""
import numpy as np
g_riem = np.loadtxt(_d("riemann_zeros_100k.txt"))[:2000]

def chi_quad(d,p):
    if d%p==0: return 0
    if p==2:
        r=d%8; return 1 if r in (1,7) else -1
    ls=pow(d%p,(p-1)//2,p); return 1 if ls==1 else (-1 if ls==p-1 else 0)
def build_chi(q,gen,order):
    units=[a for a in range(1,q) if np.gcd(a,q)==1]; dlog={}; val=1
    for j in range(len(units)): dlog[val%q]=j; val=(val*gen)%q
    om=np.exp(2j*np.pi/order)
    return lambda p:0j if np.gcd(p,q)>1 else om**dlog[p%q]

# (label, zeros, character)
L=[]
L.append(("zeta", g_riem, lambda p:1.0+0j))
L.append(("chi35", np.loadtxt(_d("disentangled/zeros_chi_-35.txt")),  lambda p:complex(chi_quad(-35,p))))
L.append(("chi91", np.loadtxt(_d("disentangled/zeros_chi_-91.txt")),  lambda p:complex(chi_quad(-91,p))))
L.append(("chi104",np.loadtxt(_d("cyclotomic_and_h6/zeros_chi_-104.txt")), lambda p:complex(chi_quad(-104,p))))
L.append(("chi5^4",np.loadtxt(_d("cyclotomic_5/zeros_chi_5_order4.txt")), build_chi(5,2,4)))
L.append(("chi7^6",np.loadtxt(_d("cyclotomic_7/zeros_chi_7_order6.txt")), build_chi(7,3,6)))
for k in range(len(L)):
    z=L[k][1]; L[k]=(L[k][0], z[np.isfinite(z)], L[k][2])

primes=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
def vphase(gam,p): w=np.exp(1j*np.log(p)*gam).sum(); return w/abs(w)

n=len(L)
Mz=np.zeros((n,n)); Mt=np.zeros((n,n)); npair=np.zeros((n,n),int)
for i in range(n):
    for j in range(n):
        zi,zj=[],[]; ci,cj=[],[]
        for p in primes:
            a=L[i][2](p); b=L[j][2](p)
            if a==0 or b==0: continue
            zi.append(vphase(L[i][1],p)); zj.append(vphase(L[j][1],p))
            ci.append(a/abs(a)); cj.append(b/abs(b))
        zi,zj,ci,cj=map(np.array,(zi,zj,ci,cj))
        Mz[i,j]=abs(np.mean(zi*np.conj(zj)))
        Mt[i,j]=abs(np.mean(ci*np.conj(cj)))
        npair[i,j]=len(zi)

labels=[x[0] for x in L]
def show(M,name):
    print(f"\n{name}")
    print("        "+"".join(f"{l:>8}" for l in labels))
    for i in range(n):
        print(f"{labels[i]:>7} "+"".join(f"{M[i,j]:>8.2f}" for j in range(n)))
show(Mz,"M_zero  (from L-function ZEROS)")
show(Mt,"M_true  (from characters)")

off=~np.eye(n,dtype=bool)
floor=1/np.sqrt(npair[off].mean())
print(f"\nshared-prime count (typical) ~ {int(npair[off].mean())},  random floor 1/sqrt(n) = {floor:.2f}")
print(f"diagonal:           M_zero mean = {np.diag(Mz).mean():.2f}   M_true mean = {np.diag(Mt).mean():.2f}")
print(f"OFF-diagonal:       M_zero mean = {Mz[off].mean():.2f}   max = {Mz[off].max():.2f}")
print(f"                    M_true mean = {Mt[off].mean():.2f}   max = {Mt[off].max():.2f}")
print(f"zeros reproduce truth: corr(M_zero_off, M_true_off) = {np.corrcoef(Mz[off],Mt[off])[0,1]:.3f}")
print(f"                       mean |M_zero - M_true| off-diag = {np.abs(Mz-Mt)[off].mean():.3f}")
