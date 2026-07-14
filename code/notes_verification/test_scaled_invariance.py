# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Scaled invariance of "infinity" and "zero" as counting labels
=============================================================

Companion to the note *Scaled Invariance of Infinity and Zero* (FF06h),
in the family of Form/Function Relativity (FF06g) and When a Number Lies.

Thesis under test (the user's observation, made precise):

    "There are infinite numbers between 1 and 2 in decimals, but if the
     constraint unit is a minimum of 1 (whole numbers) it is irrelevant."

Restated operationally: the number of representable points inside an
interval is not a property of the interval. It is a reading of the PAIR
(interval, resolution-unit delta). The labels "infinite" (delta -> 0) and
"zero interior" (delta = interval width) are two readings of the SAME
interval at two units related by a scale. The only frame-invariant content
is the DIMENSIONLESS ratio  width / delta  (the interior count), which is
preserved exactly when the interval and the unit are rescaled together.

This script establishes four machine-verified (T1) facts:

  A. UNIT-RELATIVITY OF THE LABEL. The interior count of delta*Z strictly
     inside (1, 2) is 0 at delta = 1 and diverges as delta -> 0
     (0, 9, 99, 999, 9999, ...). Same interval, opposite labels, only the
     unit changed.

  B. JOINT-SCALING INVARIANCE (the "scaled invariance"). For every interval
     [a,b], unit delta, and scale lambda,
         #( (delta)Z    cap [a, b] )  ==  #( (lambda*delta)Z cap [lambda*a, lambda*b] ).
     Verified EXACTLY (rational arithmetic, no floating error) over a large
     random ensemble. Infinity/zero is invariant under joint rescaling.

  C. INTERVAL-ONLY SCALING BREAKS IT (why the label is "relative"). Holding
     the unit fixed and stretching the interval by k multiplies the interior
     count by ~k: [1,2] has 0 interior integers, its x10 image [10,20] has 9.
     The label moves precisely because the unit did NOT scale with it.

  D. THE INVARIANT IS DIMENSIONLESS. The closed-interval count
     floor(b/delta) - ceil(a/delta) + 1 depends only on the ratios
     a/delta, b/delta; equal-ratio pairs give equal counts.

Result: all four PASS. The observation is a correct, classical statement
about resolution-relative counting -- NOT a claim about set cardinality
(see the scope note in the .tex; Cantor is untouched).

Run:
    python3 test_scaled_invariance.py

Dependencies: standard library only (fractions, random). Seed 20260423.
"""

from fractions import Fraction
import random

SEED = 20260423


# ============================================================
# Exact lattice-point counting (no floating error)
# ============================================================
def count_closed(a, b, delta):
    """#{ x in delta*Z : a <= x <= b }, exact for Fraction inputs.

    x = m*delta with integer m, and a <= m*delta <= b  <=>
    ceil(a/delta) <= m <= floor(b/delta).
    """
    if delta <= 0:
        raise ValueError("delta must be positive")
    if b < a:
        return 0
    lo = a / delta
    hi = b / delta
    m_lo = _ceil_frac(lo)
    m_hi = _floor_frac(hi)
    return max(0, m_hi - m_lo + 1)


def count_open(a, b, delta):
    """#{ x in delta*Z : a < x < b }, exact (strict interior)."""
    if delta <= 0:
        raise ValueError("delta must be positive")
    if b <= a:
        return 0
    m_lo = _floor_frac(a / delta) + 1          # first integer strictly > a/delta
    m_hi = _ceil_frac(b / delta) - 1           # last integer strictly < b/delta
    return max(0, m_hi - m_lo + 1)


def _floor_frac(x):
    return x.numerator // x.denominator


def _ceil_frac(x):
    return -((-x.numerator) // x.denominator)


# ============================================================
# A. Unit-relativity of the label
# ============================================================
def test_unit_relativity():
    print("=" * 78)
    print("  A. UNIT-RELATIVITY OF THE LABEL   (interior of the open interval (1,2))")
    print("=" * 78)
    print(f"  {'unit delta':>14} {'interior count of (1,2)':>26}   {'label':>10}")
    print(f"  {'-'*70}")
    expected = {1: 0, 10: 9, 100: 99, 1000: 999, 10000: 9999}
    ok = True
    for k in [1, 10, 100, 1000, 10000]:
        delta = Fraction(1, k)
        c = count_open(Fraction(1), Fraction(2), delta)
        label = "0 (empty)" if c == 0 else ("-> infinity" if k >= 1000 else "growing")
        flag = "OK" if c == expected[k] else "FAIL"
        ok = ok and (c == expected[k])
        print(f"  {'1/'+str(k):>14} {c:>26} {label:>13}  [{flag}]")
    print()
    print("  The SAME interval (1,2): 0 interior points at unit=1, diverging as unit->0.")
    print("  'Infinite decimals between 1 and 2' and 'nothing between 1 and 2' are the")
    print("  same interval read at two units. The label is not carried by the interval.")
    print()
    assert ok, "unit-relativity counts did not match closed form"
    return ok


# ============================================================
# B. Joint-scaling invariance (exact, randomized)
# ============================================================
def test_joint_scaling_invariance(n_trials=200000):
    print("=" * 78)
    print("  B. JOINT-SCALING INVARIANCE   (exact rational arithmetic)")
    print("=" * 78)
    print("  Claim:  #(deltaZ cap [a,b])  ==  #((lambda*delta)Z cap [lambda*a, lambda*b])")
    print(f"  Random ensemble: {n_trials} trials, seed {SEED}.")
    rng = random.Random(SEED)
    mismatches = 0
    max_count = 0
    for _ in range(n_trials):
        a = Fraction(rng.randint(-500, 500), rng.randint(1, 12))
        width = Fraction(rng.randint(0, 1000), rng.randint(1, 12))
        b = a + width
        delta = Fraction(rng.randint(1, 50), rng.randint(1, 50))
        lam = Fraction(rng.randint(1, 40), rng.randint(1, 40))
        left = count_closed(a, b, delta)
        right = count_closed(lam * a, lam * b, lam * delta)
        max_count = max(max_count, left)
        if left != right:
            mismatches += 1
    flag = "OK" if mismatches == 0 else "FAIL"
    print(f"  mismatches: {mismatches} / {n_trials}   (max count seen: {max_count})   [{flag}]")
    print("  The counting label is EXACTLY invariant under scaling interval and unit together.")
    print("  This is the 'scaled invariance': infinity and zero move only when the unit")
    print("  is held while the interval scales (or vice versa) -- never under joint scaling.")
    print()
    assert mismatches == 0, f"{mismatches} joint-scaling mismatches"
    return mismatches == 0


# ============================================================
# C. Interval-only scaling breaks the label
# ============================================================
def test_interval_only_scaling():
    print("=" * 78)
    print("  C. INTERVAL-ONLY SCALING BREAKS IT   (unit held at 1)")
    print("=" * 78)
    print(f"  {'interval':>16} {'unit':>8} {'interior integers':>20}")
    print(f"  {'-'*54}")
    unit = Fraction(1)
    rows = [
        ((Fraction(1), Fraction(2)), 0),
        ((Fraction(10), Fraction(20)), 9),
        ((Fraction(100), Fraction(200)), 99),
        ((Fraction(1000), Fraction(2000)), 999),
    ]
    ok = True
    for (a, b), exp in rows:
        c = count_open(a, b, unit)
        flag = "OK" if c == exp else "FAIL"
        ok = ok and (c == exp)
        print(f"  {'['+str(a)+','+str(b)+']':>16} {str(unit):>8} {c:>20}  [{flag}]")
    print()
    print("  [1,2] scaled x10 -> [10,20] gains 9 interior points at the SAME unit.")
    print("  The interval [1,2] is 'adjacent' (0 between) only because it equals one unit.")
    print("  Adjacency of 1 and 2 is a fact about the unit, not about 1 and 2.")
    print()
    assert ok, "interval-only scaling counts did not match"
    return ok


# ============================================================
# D. The invariant is the dimensionless ratio
# ============================================================
def test_dimensionless_invariant(n_trials=50000):
    print("=" * 78)
    print("  D. THE INVARIANT IS DIMENSIONLESS   (count depends only on a/delta, b/delta)")
    print("=" * 78)
    rng = random.Random(SEED + 1)
    mismatches = 0
    for _ in range(n_trials):
        a = Fraction(rng.randint(-300, 300), rng.randint(1, 9))
        b = a + Fraction(rng.randint(0, 600), rng.randint(1, 9))
        delta = Fraction(rng.randint(1, 30), rng.randint(1, 30))
        # any lambda reproduces the same count because a/delta and b/delta are fixed
        lam = Fraction(rng.randint(1, 25), rng.randint(1, 25))
        c1 = count_closed(a, b, delta)
        c2 = count_closed(lam * a, lam * b, lam * delta)  # same ratios a/delta, b/delta
        if c1 != c2:
            mismatches += 1
    flag = "OK" if mismatches == 0 else "FAIL"
    print(f"  ratio-preserving reparametrizations agree: {n_trials - mismatches}/{n_trials}  [{flag}]")
    print("  count = floor(b/delta) - ceil(a/delta) + 1  is a function of the ratios alone.")
    print("  Only  width/delta  is physical; the raw width and raw unit are gauge.")
    print()
    assert mismatches == 0, f"{mismatches} dimensionless-invariant mismatches"
    return mismatches == 0


def main():
    print()
    results = [
        ("A unit-relativity",         test_unit_relativity()),
        ("B joint-scaling invariance", test_joint_scaling_invariance()),
        ("C interval-only break",     test_interval_only_scaling()),
        ("D dimensionless invariant", test_dimensionless_invariant()),
    ]
    print("=" * 78)
    print("  SUMMARY")
    print("=" * 78)
    for name, ok in results:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")
    all_ok = all(ok for _, ok in results)
    print()
    print("  " + ("ALL PASS -- " if all_ok else "FAILURE -- "), end="")
    print("infinity and zero are resolution-relative counting labels;")
    print("  the dimensionless ratio width/delta is the joint-scaling invariant.")
    print()
    print("  SCOPE: this concerns the count of REPRESENTABLE points under a unit,")
    print("  not set cardinality. |R|, |Q|, |Z| remain distinct and frame-free;")
    print("  Cantor is untouched. See the .tex scope section.")
    print()
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
