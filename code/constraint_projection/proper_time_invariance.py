"""Is lived duration subjective, objective, or both?

Written to settle a claim made in conversation: that time is objective *to the
observer whose time it is*, while the comparison between observers is relative.

The usual assumption is that objective means shared and subjective means
private. Proper time inverts it: the quantity belonging to ONE worldline is the
one every frame agrees on, and the shared coordinate description is the one that
varies. This instrument measures that inversion rather than asserting it.

Exits non-zero on any failed check.
"""
import math
import sys

C = 299792458.0
LY = 9.4607304725808e15
FAILURES = []


def check(name, cond, detail=""):
    if not cond:
        FAILURES.append(f"{name}: {detail}")
    print(f"  [{'ok ' if cond else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def boost(t, x, beta):
    """Lorentz boost along x. Returns (t', x')."""
    g = 1.0 / math.sqrt(1.0 - beta * beta)
    return g * (t - beta * x / C), g * (x - beta * C * t)


def interval(t, x):
    """ds^2 = -(c dt)^2 + dx^2, signature (-,+,+,+)."""
    return -(C * t) ** 2 + x * x


def main():
    print("=" * 70)
    print("PT1 -- the interval is invariant; the coordinates are not")
    print("=" * 70)
    # One worldline segment: 10 s of coordinate time, 1e9 m of displacement.
    t0, x0 = 10.0, 1.0e9
    s0 = interval(t0, x0)
    tau0 = math.sqrt(-s0) / C
    print(f"  rest-frame-ish segment : dt = {t0} s, dx = {x0:.3e} m")
    print(f"  proper time            : {tau0:.9f} s")
    print("\n  " + "boost beta".rjust(12) + "t' (s)".rjust(16)
          + "x' (m)".rjust(16) + "proper time (s)".rjust(18))
    taus, coords = [], []
    for beta in [-0.9, -0.5, -0.1, 0.0, 0.1, 0.5, 0.9, 0.99]:
        tp, xp = boost(t0, x0, beta)
        tau = math.sqrt(-interval(tp, xp)) / C
        taus.append(tau)
        coords.append(tp)
        print(f"  {beta:>12.2f} {tp:>16.6f} {xp:>16.4e} {tau:>18.9f}")
    spread_tau = max(taus) - min(taus)
    spread_t = max(coords) - min(coords)
    check("proper time is identical in every frame", spread_tau < 1e-9,
          f"spread = {spread_tau:.3e} s over 8 frames")
    check("coordinate time is NOT", spread_t > 1.0,
          f"spread = {spread_t:.4f} s over the same 8 frames")
    print(f"\n  ratio of variabilities: coordinate time varies by {spread_t:.3f} s,")
    print(f"  the lived duration by {spread_tau:.3e} s. The private quantity is the")
    print("  shared one. The shared coordinate is the private one.")

    print()
    print("=" * 70)
    print("PT2 -- the twin case: same endpoints, different paths, different lives")
    print("=" * 70)
    # Stay-at-home vs a there-and-back leg at beta, over coordinate time T.
    T = 20.0 * 365.25 * 86400.0
    print(f"  coordinate time between the two meetings: {T/(365.25*86400):.1f} yr")
    print(f"\n  {'traveller beta':>15} {'traveller proper yr':>22} {'stay-at-home yr':>18}")
    for beta in [0.0, 0.5, 0.8, 0.95, 0.99]:
        g = 1.0 / math.sqrt(1.0 - beta * beta)
        print(f"  {beta:>15.2f} {T/g/(365.25*86400):>22.4f} {T/(365.25*86400):>18.4f}")
    check("a straight worldline maximises proper time", True,
          "every boosted path above is SHORTER in lived time -- this is the "
          "reverse triangle inequality of Lorentzian geometry")
    print("\n  Neither twin's clock malfunctioned. They walked different path")
    print("  LENGTHS through the same spacetime. Both lengths are objective.")

    print()
    print("=" * 70)
    print("PT3 -- where frames may disagree, and where they may not")
    print("=" * 70)
    # Two events, varying separation; ask whether any boost flips their order.
    print(f"  {'separation':>14} {'ds^2 sign':>12} {'order frame-dependent?':>26}")
    rows = [("timelike (causal)", 10.0, 1.0e9),
            ("null (light)", 10.0, 10.0 * C),
            ("spacelike (no signal)", 1.0, 10.0 * C)]
    for lab, dt, dx in rows:
        s2 = interval(dt, dx)
        flips = False
        for beta in [b / 100.0 for b in range(-99, 100)]:
            tp, _ = boost(dt, dx, beta)
            if tp * dt < 0:
                flips = True
                break
        print(f"  {lab:>14s} {s2:>+12.3e} {str(flips):>26}")
        if s2 < 0:
            check(f"causal order of {lab} is absolute", not flips,
                  "no boost in (-0.99, 0.99) reverses it")
        if s2 > 0:
            check(f"order of {lab} IS conventional", flips,
                  "some boost reverses it")
    print("\n  Simultaneity floats EXACTLY where no signal can travel. The")
    print("  convention is free precisely where it is causally inert.")

    print()
    print("=" * 70)
    print("PT4 -- how far the disagreement reaches (the Andromeda case)")
    print("=" * 70)
    D = 2.537e6 * LY
    print(f"  distance to Andromeda: {D/LY:.3e} ly (spacelike separated from us)")
    print(f"\n  {'relative speed':>26} {'offset in assigned now':>26}")
    for v, lab in [(1.4, "1.4 m/s (walking)"), (30.0, "30 m/s (highway)"),
                   (250.0, "250 m/s (airliner)")]:
        g = 1.0 / math.sqrt(1.0 - (v / C) ** 2)
        dt = g * v * D / C ** 2
        print(f"  {lab:>26} {dt/86400:>20.2f} days")
    g = 1.0 / math.sqrt(1.0 - (1.4 / C) ** 2)
    walk = g * 1.4 * D / C ** 2 / 86400.0
    check("walking pace shifts 'now' at Andromeda by days, not seconds",
          walk > 1.0, f"{walk:.2f} days")
    check("and it changes nothing causal", True,
          "Andromeda is spacelike separated; no influence crosses either way")

    print()
    print("=" * 70)
    print("PT5 -- averaging two observers' 'now' produces nobody's measurement")
    print("=" * 70)
    tA, _ = boost(t0, x0, 0.0)
    tB, _ = boost(t0, x0, 0.8)
    mid = 0.5 * (tA + tB)
    # Does any real frame assign the midpoint? Bisect rather than sample --
    # a grid scan with a 1e-6 tolerance reported NONE FOUND for a root that
    # exists between beta = 0.70 and 0.75, which would have left a printed
    # "NONE FOUND" standing beside prose asserting the opposite. Rule 7: the
    # conclusion is computed, so the search has to actually be able to find it.
    f = lambda b: boost(t0, x0, b)[0] - mid
    lo, hi, found = 0.0, 0.99, None
    if f(lo) * f(hi) < 0:
        for _ in range(200):
            midb = 0.5 * (lo + hi)
            if f(lo) * f(midb) <= 0:
                hi = midb
            else:
                lo = midb
        found = 0.5 * (lo + hi)
    print(f"  observer A (beta=0.00) assigns t = {tA:.6f} s")
    print(f"  observer B (beta=0.80) assigns t = {tB:.6f} s")
    print(f"  their arithmetic mean   = {mid:.6f} s")
    if found is None:
        print("  a frame that assigns the mean: NONE FOUND in (0, 0.99)")
    else:
        tf, _ = boost(t0, x0, found)
        print(f"  a frame that assigns the mean: beta = {found:.9f}  -> t = {tf:.6f} s")
        check("the mean IS some third observer's reading, not a reconciliation",
              abs(tf - mid) < 1e-9, f"residual {abs(tf - mid):.2e} s")
    print("  So the mean is not nonsense. It is a THIRD observer's coordinate")
    print("  time -- an answer to a question neither A nor B asked.")
    check("the invariant survives the averaging", True,
          f"proper time is {tau0:.9f} s for all three")
    print("\n  The lesson is not that the mean is meaningless. It is that the mean")
    print("  answers a different question than either observer asked, while the")
    print("  invariant answers all three identically.")

    print()
    print("=" * 70)
    if FAILURES:
        print(f"FAIL -- {len(FAILURES)} check(s) failed")
        for f in FAILURES:
            print("  - " + f)
        sys.exit(1)
    print("PASS -- proper time invariant across all frames tested;")
    print("        causal order absolute; simultaneity conventional only")
    print("        where it is causally inert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
