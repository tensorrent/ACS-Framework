import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

"""
PHASE TEST for complex Dirichlet characters (strictly sharper than the sign test).
Files are one-sided positive-height zeros of L(s,chi), chi of order 4 (mod 5) / order 6 (mod 7).

Complex witness:  W(p) = sum_k exp(i * log p * gamma_k).
If W(p) ~ |A| * chi(p) * e^{i phi0}, then demodulating by chi-bar aligns every prime to a
common direction.  Resultant length R = | mean_p [ chibar(p) W(p)/|W(p)| ] |.
   R -> 1 : phases carry chi(p)         R -> ~1/sqrt(#p) : no character structure.
Controls: demodulate by trivial char, and by chi^2 (wrong order) -- both should collapse.
"""
import numpy as np
rng = np.random.default_rng(20260423)

def build_chi(q, gen, order):
    units=[a for a in range(1,q) if np.gcd(a,q)==1]
    dlog={}; val=1
    for j in range(len(units)):
        dlog[val%q]=j; val=(val*gen)%q
    omega=np.exp(2j*np.pi/order)
    def chi(p):
        if np.gcd(p,q)>1: return 0+0j
        return omega**dlog[p%q]
    return chi

def W(gam,p):                    # complex witness at u=log p
    return np.exp(1j*np.log(p)*gam).sum()

def noise_floor(gam, ntrial=400):
    us=rng.uniform(0.5,3.6,ntrial)
    mags=np.abs(np.exp(1j*np.outer(us,gam)).sum(axis=1))
    return mags.mean(), np.percentile(mags,95)

cases=[
    ("L(s,chi) mod 5, order 4", _d("cyclotomic_5/zeros_chi_5_order4.txt"), 5, 2, 4),
    ("L(s,chi) mod 7, order 6", _d("cyclotomic_7/zeros_chi_7_order6.txt"), 7, 3, 6),
]
primes=np.array([2,3,5,7,11,13,17,19,23,29,31,37,41,43,47])

for title,fn,q,gen,order in cases:
    gam=np.loadtxt(fn); gam=gam[np.isfinite(gam)]
    chi=build_chi(q,gen,order)
    nf_mean,nf95=noise_floor(gam)
    print("="*68); print(f"{title}   (N={len(gam)} zeros; |W| noise floor mean={nf_mean:.2f}, 95%={nf95:.2f})")
    print(f"{'p':>3} {'p%q':>4} {'|W|':>7} {'argW':>7} {'chi(p)':>14} {'demod angle':>12}")
    units=[]; demod=[]; demod2=[]; trivial=[]
    for p in primes:
        c=chi(int(p))
        if c==0: 
            continue
        w=W(gam,int(p)); mag=abs(w); ph=w/mag
        units.append(p); demod.append(np.conj(c)*ph); trivial.append(ph)
        demod2.append(np.conj(c**2)*ph)
        da=np.angle(np.conj(c)*ph)
        print(f"{p:>3} {p%q:>4} {mag:>7.2f} {np.angle(w):>7.2f} {f'{c.real:+.2f}{c.imag:+.2f}i':>14} {da:>12.2f}")
    demod=np.array(demod); trivial=np.array(trivial); demod2=np.array(demod2)
    R_chi=abs(demod.mean()); R_triv=abs(trivial.mean()); R_chi2=abs(demod2.mean())
    npr=len(demod); floor=1/np.sqrt(npr)
    meanmag=np.mean([abs(W(gam,int(p))) for p in units])
    print(f"\n  unramified primes used: {npr}   random-resultant floor ~ 1/sqrt(n) = {floor:.2f}")
    print(f"  mean |W| at primes        = {meanmag:.2f}   (vs noise floor {nf_mean:.2f}  -> arithmetic present if >)")
    print(f"  R  demod by chi (correct) = {R_chi:.3f}   <-- want HIGH")
    print(f"  R  demod by trivial       = {R_triv:.3f}   (control)")
    print(f"  R  demod by chi^2 (wrong) = {R_chi2:.3f}   (control)")
    verdict = "PHASE CARRIES chi" if (R_chi>2*floor and R_chi>1.6*max(R_triv,R_chi2)) else "not resolved at this N"
    print(f"  --> {verdict}")
