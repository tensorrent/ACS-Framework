# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

r"""
LADDER x CHARACTER TWIST  --  is the critical line ONE object, or a FAMILY?

hp_harmonic_ladder.py showed the zeta arithmetic face carries a repetition ladder
(rung k at frequency k log p) obeying the p^{-k/2} trace-formula weight. If every
Dirichlet L(s,chi) is the SAME object twisted by its character, the explicit formula
fixes exactly how the twist acts on the ladder: the prime-power p^k term carries
chi(p^k) = chi(p)^k. So the twist is chi^k on rung k -- a clean, parameter-free,
falsifiable structural prediction.

PART 1  complex characters (phase demodulation, sharp).
  Complex witness W(u) = sum_k exp(i u gamma_k).  For L(s,chi):
     rung k line at u = k log p  ~  |A| chi(p)^k e^{i phi}.
  Demodulate rung k by chi-bar^m; the resultant R = |mean_p chibar(p)^m W/|W|| peaks
  when m = k and collapses otherwise.  PREDICTION: the 2x2 table R(rung k, demod m) is
  DIAGONAL -- rung 1 aligns under chi^1 not chi^2; rung 2 aligns under chi^2 not chi^1.
  (The chi^2 control already in hp_phase_test.py is exactly the off-diagonal (k=1,m=2).)

PART 2  quadratic characters (sign, real).  chi(p) = +-1  =>  chi(p^2) = +1 always.
  So rung 1 sign FLIPS with chi(p) (the C8 result) but rung 2 is UNTWISTED (chi(p^2)=1):
  F_chi(2 log p) should stay NEGATIVE for every quadratic chi, no flip.  The ladder's
  even rungs are character-blind; its odd rungs carry the character.

If both hold, the object is universal: one geometry, and the L-function is that object
with chi^k painted on rung k.  Data-limited (L-zero files are ~50-70 zeros), so PART 1
leans on phase resultants (robust at low N) and PART 2 on small-prime signs.
Reproducible: seed 20260423.  Proves nothing about RH; tests universality of the object.
"""
import numpy as np
rng = np.random.default_rng(20260423)

# ---------------------------------------------------------------- character builders
def build_chi(q, gen, order):
    units = [a for a in range(1, q) if np.gcd(a, q) == 1]
    dlog = {}; val = 1
    for j in range(len(units)):
        dlog[val % q] = j; val = (val * gen) % q
    omega = np.exp(2j*np.pi/order)
    def chi(p):
        if np.gcd(p, q) > 1: return 0+0j
        return omega**dlog[p % q]
    return chi

def chi_quad(d, p):                     # Kronecker (d/p)
    if d % p == 0: return 0
    if p == 2:
        r = d % 8; return 1 if r in (1, 7) else -1
    ls = pow(d % p, (p-1)//2, p)
    return 1 if ls == 1 else (-1 if ls == p-1 else 0)

def Wc(gam, u):                         # complex witness at frequency u
    return np.exp(1j*u*gam).sum()

def Fr(gam, u):                         # signed real witness at frequency u
    return np.cos(u*gam).sum()

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# =====================================================================================
print("="*72)
print("PART 1  --  COMPLEX CHARACTERS: does rung k carry chi^k ?  (phase demod)")
print("="*72)
complex_cases = [
    ("L(s,chi) mod 5, order 4", _d("cyclotomic_5/zeros_chi_5_order4.txt"), 5, 2, 4),
    ("L(s,chi) mod 7, order 6", _d("cyclotomic_7/zeros_chi_7_order6.txt"), 7, 3, 6),
]
for title, fn, q, gen, order in complex_cases:
    gam = np.loadtxt(fn); gam = gam[np.isfinite(gam)]
    chi = build_chi(q, gen, order)
    # noise floor for |W| at a random (non-arithmetic) frequency
    us = rng.uniform(0.5, 7.2, 400)
    nf = np.abs(np.exp(1j*np.outer(us, gam)).sum(axis=1)).mean()
    print(f"\n{title}   N={len(gam)} zeros   |W| noise floor ~ {nf:.2f}")
    # 2x2 resultant table R(rung k, demod power m)
    R = {}
    magk = {}
    for k in (1, 2):
        phases = []; mags = []
        chi_pk_conj = []
        prime_used = []
        for p in PRIMES:
            c = chi(int(p))
            if c == 0:
                continue
            w = Wc(gam, k*np.log(p)); m = abs(w)
            phases.append(w/m); mags.append(m); prime_used.append(p)
            chi_pk_conj.append(np.conj(c))
        phases = np.array(phases); chi1 = np.array(chi_pk_conj)
        magk[k] = np.mean(mags)
        for m_pow in (1, 2):
            demod = (chi1**m_pow) * phases           # demodulate by chi-bar^m
            R[(k, m_pow)] = abs(demod.mean())
    floor = 1/np.sqrt(sum(1 for p in PRIMES if chi(int(p)) != 0))
    print(f"  random-resultant floor ~ 1/sqrt(#primes) = {floor:.2f}")
    print(f"  mean |W|:  rung1 = {magk[1]:.2f}   rung2 = {magk[2]:.2f}   (vs floor {nf:.2f})")
    print(f"  {'':>10}   demod chi^1   demod chi^2   -> aligns under")
    for k in (1, 2):
        r1, r2 = R[(k, 1)], R[(k, 2)]
        winner = "chi^1" if r1 > r2 else "chi^2"
        exp = f"chi^{k}"
        ok = winner == exp
        print(f"  rung k={k} :   {r1:>10.3f}   {r2:>10.3f}   -> {winner:>5}"
              f"  (predict {exp}) {'OK' if ok else 'MISS'}")
    diag_ok = (R[(1,1)] > R[(1,2)]) and (R[(2,2)] > R[(2,1)])
    print(f"  DIAGONAL twist (rung k aligns under chi^k): {'CONFIRMED' if diag_ok else 'not resolved'}")

# =====================================================================================
print("\n" + "="*72)
print("PART 2  --  QUADRATIC CHARACTERS: rung1 flips with chi(p), rung2 stays fixed")
print("="*72)
# zeta signs for reference (rung1 and rung2 both negative at prime powers, C6)
gz = np.loadtxt(_d("riemann_zeros_100k.txt"))[:2000]
zeta_sign1 = {p: (-1 if Fr(gz, np.log(p)) < 0 else 1) for p in PRIMES}

quad_cases = [
    (-35,  _d("disentangled/zeros_chi_-35.txt")),
    (-91,  _d("disentangled/zeros_chi_-91.txt")),
    (-104, _d("cyclotomic_and_h6/zeros_chi_-104.txt")),
]
small = [2, 3, 5, 7, 11, 13]                 # rung-2 signal only readable at small p (few zeros)
for d, fn in quad_cases:
    if not _os.path.exists(fn):
        print(f"  [missing {fn}]"); continue
    gam = np.loadtxt(fn); gam = gam[np.isfinite(gam)]
    print(f"\nL(s,chi_{d})   N={len(gam)} zeros")
    print(f"  {'p':>3} {'chi(p)':>7} {'rung1 sign':>11} {'pred(flip)':>11} "
          f"{'rung2 sign':>11} {'pred(fixed)':>12}")
    hit1 = tot1 = hit2 = tot2 = 0
    for p in small:
        c = chi_quad(d, p)
        if c == 0:
            continue
        f1 = Fr(gam, np.log(p)); f2 = Fr(gam, 2*np.log(p))
        s1 = -1 if f1 < 0 else 1
        s2 = -1 if f2 < 0 else 1
        pred1 = zeta_sign1[p] * c            # rung1 twists by chi(p)
        pred2 = -1                           # rung2: zeta neg * chi(p^2)=+1 -> negative
        ok1 = (s1 == pred1); ok2 = (s2 == pred2)
        hit1 += ok1; tot1 += 1; hit2 += ok2; tot2 += 1
        print(f"  {p:>3} {c:>+7d} {('-' if s1<0 else '+'):>11} "
              f"{('-' if pred1<0 else '+'):>11} {('-' if s2<0 else '+'):>11} "
              f"{'-  (neg)':>12}  {'OK' if ok1 and ok2 else ''}")
    print(f"  rung1 flip-with-chi match : {hit1}/{tot1}")
    print(f"  rung2 stays-negative match: {hit2}/{tot2}")

# =====================================================================================
print("\n" + "="*72)
print("PART 3  --  COMMUTATOR LEDGER: reality = [iota, T] = 0 = self-dual")
print("="*72)
# The functional equation is the involution iota: chi -> chi-bar. The twist T paints
# chi(p)^k on rung k (verified in Parts 1-2). Their commutator on a fiber is the failure
# of the arithmetic face to be real: || [iota,T] ||_k = mean_p | Im chi(p)^k |. It is
# zero exactly when chi(p)^k is real for all k, i.e. chi real, i.e. chi in Fix(iota).
# This is the ORDER PARAMETER of the family, read off the twist the zeros confirmed above.
print("  ||[iota,T]||_k = mean_p |Im chi(p)^k|   (0 <=> face real <=> self-dual)")
print(f"  {'fiber':>22} {'k=1':>8} {'k=2':>8}   {'locus':>14}")
def commutator_norm(chi, k, primes):
    vals = [abs((chi(int(p))**k).imag) for p in primes if chi(int(p)) != 0]
    return float(np.mean(vals))
# quadratic (self-dual) fibers: chi real -> defect 0 on every rung
for d, _ in quad_cases:
    chi = lambda p, d=d: chi_quad(d, p) + 0j
    c1 = commutator_norm(chi, 1, PRIMES); c2 = commutator_norm(chi, 2, PRIMES)
    locus = "Fix(iota)" if (c1 < 1e-9 and c2 < 1e-9) else "off-locus"
    print(f"  {'chi_'+str(d)+' (quadratic)':>22} {c1:>8.3f} {c2:>8.3f}   {locus:>14}")
# complex fibers: chi not real -> defect > 0, and rung parity differs
for title, fn, q, gen, order in complex_cases:
    chi = build_chi(q, gen, order)
    c1 = commutator_norm(chi, 1, PRIMES); c2 = commutator_norm(chi, 2, PRIMES)
    locus = "Fix(iota)" if (c1 < 1e-9 and c2 < 1e-9) else "off-locus"
    tag = f"chi mod {q} ord {order}"
    print(f"  {tag:>22} {c1:>8.3f} {c2:>8.3f}   {locus:>14}")
print("  => self-dual fibers commute ([iota,T]=0, real face); complex fibers do not.")
print("     The commutator IS the phase the zeros carry -- the family's order parameter.")

print("\n" + "="*72)
print("""READING:
  PART 1 -- if the 2x2 phase table is diagonal, the L-function ladder carries chi^k on
    rung k: the object is the SAME as zeta's, with the character painted frequency by
    frequency. Rung 1 sees chi, rung 2 sees chi^2 -- a genuine, twist-specific fingerprint.
  PART 2 -- for real chi, chi^2 = trivial, so the even rungs go character-BLIND: rung 2
    stays negative for every quadratic L while rung 1 flips. The ladder's parity encodes
    the character's order.
  Together: 'the flattened object' is universal. Each L-function is one geometry with
    chi^k on rung k; zeta is the chi = trivial member. Data-limited (~50-70 L-zeros);
    phase resultants carry PART 1, small-prime signs carry PART 2. Proves nothing about
    RH -- it tests whether the object is one or many.""")
