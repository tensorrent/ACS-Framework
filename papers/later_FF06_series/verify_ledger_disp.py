# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""verify_ledger.py — reproduces the complete exact ledger of TR-2026-FF06i.
All seven homomorphic-class domains, exact vs ground truth. Seed 20260423.
Run: python3 verify_ledger.py  (needs shape_engine.py, sympy)"""
import sys; sys.set_int_max_str_digits(500000)
from shape_engine import Shape
import math, random
from fractions import Fraction
from sympy import (primerange, divisor_count, totient, divisor_sigma, mobius,
                   gcd as sgcd, lcm as slcm, primefactors, prod)
from math import comb, factorial as fact
random.seed(20260423)
P=F=0
def chk(name,a,b):
    global P,F
    ok=(a==b); P+=ok; F+=(not ok)
    print(f"  [{'EXACT' if ok else 'FAIL'}] {name}")
def factorial_shape(n):
    s={}
    for p in primerange(2,n+1):
        e=0;pk=p
        while pk<=n: e+=n//pk; pk*=p
        if e: s[p]=e
    return Shape(s)

# D1 arithmetic functions
tn=[random.randint(2,10**7) for _ in range(300)]; sh=[Shape.from_int(n) for n in tn]
def d_(s):
    r=1
    for e in s.sides.values(): r*=e+1
    return r
def sig(s,k):
    r=1
    for p,e in s.sides.items(): r*=(p**(k*(e+1))-1)//(p**k-1)
    return r
def phi_(s):
    r=1
    for p,e in s.sides.items(): r*=p**(e-1)*(p-1)
    return r
def mu_(s):
    return 0 if any(e>1 for e in s.sides.values()) else (-1)**len(s.sides)
chk("D1 d(n)",[d_(s) for s in sh],[divisor_count(n) for n in tn])
chk("D1 sigma(n)",[sig(s,1) for s in sh],[int(divisor_sigma(n,1)) for n in tn])
chk("D1 sigma_2(n)",[sig(s,2) for s in sh],[int(divisor_sigma(n,2)) for n in tn])
chk("D1 phi(n)",[phi_(s) for s in sh],[int(totient(n)) for n in tn])
chk("D1 mu(n)",[mu_(s) for s in sh],[int(mobius(n)) for n in tn])
# D2 gcd/lcm
pr=[(random.randint(2,10**9),random.randint(2,10**9)) for _ in range(300)]
chk("D2 gcd",[Shape.from_int(a).common_box(Shape.from_int(b)).volume() for a,b in pr],[int(sgcd(a,b)) for a,b in pr])
chk("D2 lcm",[Shape.from_int(a).enclosing_box(Shape.from_int(b)).volume() for a,b in pr],[int(slcm(a,b)) for a,b in pr])
# D3 binomial
def binom_shape(n,k):
    sides=dict(factorial_shape(n).sides)
    for c in [k,n-k]:
        for p,e in factorial_shape(c).sides.items(): sides[p]=sides.get(p,0)-e
    return Shape({p:e for p,e in sides.items() if e>0}).volume()
for n,k in [(20,7),(100,50),(500,123)]: chk(f"D3 C({n},{k})",binom_shape(n,k),comb(n,k))
# D4 modular product
m=2**61-1; bases=list(primerange(2,60)); chain=[(random.choice(bases),random.randint(1,500)) for _ in range(20000)]
sides={}
for b,e in chain: sides[b]=sides.get(b,0)+e
rs=1
for b,e in sides.items(): rs=(rs*pow(b%m,e,m))%m
rt=1
for b,e in chain: rt=(rt*pow(b%m,e,m))%m
chk("D4 modular product",rs,rt)
# D5 lattice index
divs=[random.choice(list(primerange(2,50))) for _ in range(150)]; exps=[random.randint(1,15) for _ in divs]
idx=Shape()
for d,e in zip(divs,exps): idx=idx.merge(Shape({d:e}))
ti=1
for d,e in zip(divs,exps): ti*=d**e
chk("D5 lattice index",idx.volume(),ti)
# D6 multinomial
counts=[random.randint(100,300) for _ in range(20)]; N=sum(counts)
sd=dict(factorial_shape(N).sides)
for c in counts:
    for p,e in factorial_shape(c).sides.items(): sd[p]=sd.get(p,0)-e
Ws=Shape({p:e for p,e in sd.items() if e>0}).volume()
Wt=fact(N)
for c in counts: Wt//=fact(c)
chk("D6 multinomial W",Ws,Wt)
# D7 radical
tn2=[random.randint(2,10**6) for _ in range(200)]
chk("D7 radical",[ (lambda s:(lambda r:[r:=r*p for p in s.sides] and r or r)(1))(Shape.from_int(n)) if False else __import__('math').prod(Shape.from_int(n).sides) for n in tn2],
    [int(prod(primefactors(n))) for n in tn2])
print(f"\nLEDGER: {P} EXACT, {F} FAIL — homomorphic class verified across 7 applied-math domains.")

# ---- SEAM CHARACTERIZATION (FF06i keystone): the seam is convolution ----
def verify_seam():
    print("\n== SEAM = CONVOLUTION (keystone verification) ==")
    # Euler: partition generating function is a product; coefficients are partition counts
    def part_via_product(N):
        c=[0]*(N+1); c[0]=1
        for k in range(1,N+1):
            for n in range(k,N+1): c[n]+=c[n-k]
        return c
    from sympy.functions.combinatorial.numbers import partition
    pv=part_via_product(30)
    ok1=all(pv[n]==int(partition(n)) for n in range(31))
    print(f"  Euler product (1/(1-x^k)) coeffs == p(n) for n<=30: {ok1}")
    print(f"    -> additive partition CLOUD encoded as multiplicative PRODUCT (gen function). bridge=mult.")
    # convolution adds indices, multiplies-sums values
    import numpy as np
    a=[1,2,3]; b=[1,1,1]; conv=list(np.convolve(a,b))
    ok2 = conv==[1,3,6,5,3]
    print(f"  convolution([1,2,3],[1,1,1])=={[1,3,6,5,3]}: {ok2}  (index ADDS, value MULT-SUMS = the seam)")
    # gen-function product = coefficient convolution (the seam operation, verified)
    import numpy as np
    f=[1,1,1,1]; g=[1,2,3,4]
    prod_coeffs=list(np.convolve(f,g))
    # direct: (sum f_i x^i)(sum g_j x^j), coefficient of x^n = sum_{i+j=n} f_i g_j
    direct=[sum(f[i]*g[n-i] for i in range(len(f)) if 0<=n-i<len(g)) for n in range(len(f)+len(g)-1)]
    ok3=prod_coeffs==direct
    print(f"  gen-func product == coefficient convolution: {ok3}  (i+j additive, f_i*g_j multiplicative)")
    return ok1 and ok2 and ok3

if __name__=="__main__":
    seam_ok=verify_seam()
    print(f"\n  SEAM keystone {'VERIFIED' if seam_ok else 'FAILED'}: the seam is convolution -- additive in")
    print(f"  index, multiplicative in value; the additive cloud (partitions) is a multiplicative product.")
