#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
SCALED INVARIANCE OF INFINITY AND ZERO -- the counting unit is the reference frame.

Verifies the four machine-checkable claims of the companion note
(papers/notes/Scaled_Invariance_Infinity_Zero.tex), using EXACT rational
arithmetic (fractions) so every count is an exact integer, seed 20260423.

  N_delta[a,b]      = #(delta*Z cap [a,b]) = floor(b/delta) - ceil(a/delta) + 1  (clamped >=0)
  N_delta_open(a,b) = #(delta*Z cap (a,b))                                       (open interval)

  A. unit-relativity: the interior of the single interval (1,2) reads 0,9,99,999,9999
     at delta = 1, 1/10, 1/100, 1/1000, 1/10000.
  B. joint-scaling invariance: N_delta[a,b] = N_{lambda*delta}[lambda*a, lambda*b] exactly.
  C. interval-only scaling breaks it: 0, 9, 99, 999 for (1,2)->(10,20)->(100,200)->(1000,2000).
  D. the invariant is dimensionless: depends only on a/delta, b/delta.

Exits nonzero on any mismatch. Nothing here touches set cardinality (Cantor untouched);
this is resolution-relative counting on the lattice delta*Z only.
"""
import sys
import random
from fractions import Fraction
from math import floor, ceil

SEED = 20260423
random.seed(SEED)

def ceil_div(p, q):      # exact ceil of Fraction p/q via integer arithmetic through Fraction
    return int(ceil(p / q))

def N_closed(a, b, delta):
    """#(delta*Z cap [a,b]) with exact rationals; clamped at 0."""
    if b < a:
        return 0
    hi = floor(Fraction(b) / Fraction(delta))
    lo = ceil(Fraction(a) / Fraction(delta))
    return max(0, hi - lo + 1)

def N_open(a, b, delta):
    """#(delta*Z cap (a,b)) -- strict interior."""
    if b <= a:
        return 0
    fb = Fraction(b) / Fraction(delta)
    fa = Fraction(a) / Fraction(delta)
    # strictly greater than a/delta and strictly less than b/delta
    hi = int(fb) - 1 if fb == int(fb) else floor(fb)      # largest integer < b/delta
    lo = int(fa) + 1 if fa == int(fa) else ceil(fa)       # smallest integer > a/delta
    return max(0, hi - lo + 1)

def rand_frac(maxnum=1000, maxden=1000):
    return Fraction(random.randint(1, maxnum), random.randint(1, maxden))

fail = 0

# ---------------------------------------------------------------- A. unit-relativity
print("=" * 66)
print("A. Interior of the single interval (1,2), read at shrinking units")
print(f"   {'delta':>10} {'N_open(1,2)':>14}")
expected_A = {1: 0, 10: 9, 100: 99, 1000: 999, 10000: 9999}
for k, exp in expected_A.items():
    delta = Fraction(1, k)
    got = N_open(1, 2, delta)
    ok = (got == exp)
    fail += not ok
    print(f"   {('1/'+str(k)) if k>1 else '1':>10} {got:>14}   {'' if ok else '<-- MISMATCH'}")
print(f"   staircase 0,9,99,999,9999 : {'OK' if fail==0 else 'FAIL'}")

# ---------------------------------------------------------------- B. joint-scaling invariance
print("\n" + "=" * 66)
print("B. Joint-scaling invariance  N_delta[a,b] = N_{lam*delta}[lam*a, lam*b]")
TRIALS_B = 200_000
mismatch_B = 0
largest = 0
for _ in range(TRIALS_B):
    a = rand_frac(); b = a + rand_frac()
    delta = rand_frac(maxnum=50, maxden=200)
    lam = rand_frac(maxnum=50, maxden=50)
    n1 = N_closed(a, b, delta)
    n2 = N_closed(lam * a, lam * b, lam * delta)
    largest = max(largest, n1)
    if n1 != n2:
        mismatch_B += 1
fail += (mismatch_B != 0)
print(f"   {TRIALS_B:,} random rational configs")
print(f"   mismatches : {mismatch_B}   (want 0)")
print(f"   largest count encountered : {largest:,}")

# ---------------------------------------------------------------- C. interval-only scaling breaks it
print("\n" + "=" * 66)
print("C. Interval-only scaling (delta=1 fixed) -- the label slides, as it must")
expected_C = [((1, 2), 0), ((10, 20), 9), ((100, 200), 99), ((1000, 2000), 999)]
for (a, b), exp in expected_C:
    got = N_open(a, b, Fraction(1))
    ok = (got == exp)
    fail += not ok
    print(f"   N_open({a},{b}) at delta=1 = {got:>5}   (expect {exp}) {'' if ok else '<-- MISMATCH'}")

# ---------------------------------------------------------------- D. dimensionless invariant
print("\n" + "=" * 66)
print("D. The invariant is dimensionless: N depends only on a/delta, b/delta")
TRIALS_D = 50_000
ok_D = 0
for _ in range(TRIALS_D):
    a = rand_frac(); b = a + rand_frac()
    delta = rand_frac(maxnum=50, maxden=200)
    lam = rand_frac(maxnum=80, maxden=80)
    if N_closed(a, b, delta) == N_closed(lam * a, lam * b, lam * delta):
        ok_D += 1
fail += (ok_D != TRIALS_D)
print(f"   ratio-preserving reparametrizations matching : {ok_D:,}/{TRIALS_D:,}")

# ---------------------------------------------------------------- verdict
print("\n" + "=" * 66)
if fail == 0:
    print("ALL EXACT (T1): unit-relativity staircase, joint-scaling invariance (0 mismatches),")
    print("interval-only break, dimensionless invariant. Cantor untouched: this is counting on")
    print("the lattice delta*Z, not set cardinality.")
    sys.exit(0)
else:
    print(f"FAILURES: {fail} block(s) mismatched.")
    sys.exit(1)
