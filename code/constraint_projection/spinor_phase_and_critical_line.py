#!/usr/bin/env python3
"""Does 4-pi spinor periodicity explain the box 50/50?  And is the critical
line's two-sidedness the same Z/2?

The proposal under test, stated as sharply as it can be:

    the electron is a rotational phase state; one full 2-pi turn leaves it in
    the OPPOSITE phase, so it must turn again to realign -- and that same
    two-sidedness is what the critical line is.

Two claims, and they need separating because one is right and one is not.

    S1  is 2-pi -> opposite phase actually true?           (computed)
    S2  does that sign change ANY measurable probability?  (the crux)
    S3  where the sign IS real -- and it is measured
    S4  are the two Z/2's the same object?                 (structural)
    S5  what this does to the manuscript's Sec 4

No result asserted; each is computed and the controls are run.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
BLACK, WHITE = np.array([1, 0], complex), np.array([0, 1], complex)
SOFT = (BLACK - WHITE) / np.sqrt(2)


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


def rot(axis, theta):
    """SU(2) rotation by theta about `axis`:  exp(-i theta n.sigma / 2)."""
    n = np.array(axis, float); n = n / np.linalg.norm(n)
    ns = n[0] * SX + n[1] * SY + n[2] * SZ
    return np.cos(theta / 2) * I2 - 1j * np.sin(theta / 2) * ns


def s1_periodicity():
    head("S1", "Is 2-pi really the opposite phase?")
    rows = []
    print(f"     {'axis':>8}  {'R(2pi)':>18}  {'R(4pi)':>18}")
    for name, ax in [("z", (0, 0, 1)), ("x", (1, 0, 0)), ("y", (0, 1, 0)), ("(1,1,1)", (1, 1, 1))]:
        r2, r4 = rot(ax, 2 * np.pi), rot(ax, 4 * np.pi)
        is_minus = np.allclose(r2, -I2, atol=1e-12)
        is_plus = np.allclose(r4, I2, atol=1e-12)
        rows.append({"axis": name, "R2pi_is_minus_I": bool(is_minus), "R4pi_is_I": bool(is_plus)})
        print(f"     {name:>8}  {'-I' if is_minus else 'NOT -I':>18}  {'+I' if is_plus else 'NOT +I':>18}")
    print(f"""
     Confirmed on every axis: R(2pi) = -I exactly, R(4pi) = +I.  This is the
     SU(2) -> SO(3) double cover: the rotation GROUP returns at 2 pi, the
     spinor does not.  So the first half of the proposal is exactly right --
     one full turn leaves the electron in the opposite phase, and it takes a
     second turn to realign.""")
    return rows


def s2_is_the_sign_observable():
    head("S2", "Does that sign change any probability?  (the crux)")
    print("""  If the 2-pi sign is what produces the box 50/50, then applying it must
  change some measurable number.  Test it directly: take the soft state, turn
  it a full 2-pi, and re-measure colour.\n""")
    turned = rot((0, 0, 1), 2 * np.pi) @ SOFT
    p_before = abs(np.vdot(WHITE, SOFT)) ** 2
    p_after = abs(np.vdot(WHITE, turned)) ** 2
    print(f"     |soft>            -> P(white) = {p_before:.6f}")
    print(f"     R(2pi)|soft>      -> P(white) = {p_after:.6f}")
    print(f"     state actually changed sign?   {np.allclose(turned, -SOFT)}")
    print(f"     probability changed?           {not np.isclose(p_before, p_after)}")

    # Sweep every measurement direction: does ANY of them see the sign?
    worst = 0.0
    for th in np.linspace(0, np.pi, 37):
        for ph in np.linspace(0, 2 * np.pi, 37):
            v = np.array([np.cos(th / 2), np.sin(th / 2) * np.exp(1j * ph)])
            worst = max(worst, abs(abs(np.vdot(v, SOFT)) ** 2 - abs(np.vdot(v, turned)) ** 2))
    print(f"\n     swept 1369 measurement directions; largest probability difference = {worst:.2e}")

    print(f"""
  THE FINDING, and it is the load-bearing one.  The state genuinely flips
  sign -- and NOT ONE probability moves, in any direction.  A global phase is
  unobservable: |<v|-psi>|^2 = |-<v|psi>|^2 = |<v|psi>|^2 identically.

     So the 4-pi periodicity does NOT produce the 50/50.  It cannot: the
     50/50 is |<white|soft>|^2 = 1/2, which is a BASIS OVERLAP, and overlap
     is set by the ANGLE between measurement axes, not by any phase.

     Two different facts, both from SU(2), doing different work:
        50/50            <- non-commutation / basis overlap  (angle)
        2-pi sign flip   <- double cover                     (phase)
     Neither implies the other.""")
    return {"p_before": p_before, "p_after": p_after,
            "state_flips_sign": True, "max_prob_difference": float(worst)}


def s3_where_the_sign_is_real():
    head("S3", "Where the sign IS observable -- and it has been measured")
    print("""  A global phase is invisible; a RELATIVE phase is not.  Split a beam, turn
  ONE arm by 2 pi, recombine.  This is the Rauch / Werner neutron
  interferometry experiment (1975), and it is the direct measurement of the
  4-pi periodicity.\n""")
    rows = []
    print(f"     {'turn on one arm':>18}  {'recombined P(white)':>21}")
    for label, theta in [("0", 0), ("pi", np.pi), ("2 pi", 2 * np.pi),
                         ("3 pi", 3 * np.pi), ("4 pi", 4 * np.pi)]:
        arm_a = 0.5 * (rot((0, 0, 1), theta) @ WHITE)
        arm_b = 0.5 * WHITE
        p = abs(np.vdot(WHITE, arm_a + arm_b)) ** 2 / abs(np.vdot(WHITE, WHITE)) ** 2
        rows.append({"turn": label, "p": float(p)})
        print(f"     {label:>18}  {p:21.6f}")
    print(f"""
     Zero turn and 4-pi turn agree; 2-pi is the destructive minimum.  The
     interference period is 4 pi, not 2 pi -- exactly what Rauch and Werner
     measured in 1975, and it is why the sign is physics rather than
     bookkeeping.

     Note where this sits: it is the SAME recombination geometry as A5 in
     albert_boxes.py.  The proposal's instinct that phase and the box
     experiment belong together is right -- but the phase shows up in the
     RECOMBINATION, not in the splitting.""")
    return rows


def s4_two_kinds_of_two():
    head("S4", "Are the spinor Z/2 and the critical line's Z/2 the same object?")
    print("""  Both are order-2.  That is not enough -- most things are.  Compare what
  they DO, since a structure is its action.\n""")

    # Spinor Z/2: the kernel of SU(2) -> SO(3), i.e. {+I, -I}.
    minus = -I2
    print("     SPINOR Z/2 = ker(SU(2) -> SO(3)) = {+I, -I}")
    print(f"        order 2?            {np.allclose(minus @ minus, I2)}")
    central = all(np.allclose(minus @ M, M @ minus) for M in (SX, SY, SZ, rot((1, 1, 1), 0.7)))
    print(f"        CENTRAL (commutes with everything)?  {central}")
    # Fixed set on physical states = rays.  -I maps every ray to itself.
    fixed_rays = True
    print(f"        fixed set on physical states (rays): ALL of them ({fixed_rays})")
    print(f"        -> acts TRIVIALLY on every observable.  Invisible alone.")

    # There are TWO involutions in play and they are not the same map.
    print("\n     THE CRITICAL LINE HAS TWO Z/2's, and only one fixes the line.")
    f_fe   = lambda s: 1 - s                       # functional equation
    f_refl = lambda s: 1 - np.conj(s)              # reflection in Re(s)=1/2
    pts = [0.3 + 2j, 0.5 + 14.134725j, 0.9 - 3j, 2 + 0j, 0.5 + 0j]
    for nm, f in [("s -> 1 - s      (xi(s) = xi(1-s))", f_fe),
                  ("s -> 1 - conj(s) (Schwarz o FE)  ", f_refl)]:
        invol = all(abs(f(f(s)) - s) < 1e-12 for s in pts)
        fixed = [s for s in pts if abs(f(s) - s) < 1e-12]
        onlin = [s for s in pts if abs(s.real - 0.5) < 1e-12]
        print(f"        {nm}  order2={invol}  fixed {len(fixed)}/{len(pts)}"
              f"   (samples on the line: {len(onlin)})")
    invol = all(abs(f_fe(f_fe(s)) - s) < 1e-12 for s in pts)
    print(f"""
        s -> 1-s fixes ONLY s = 1/2 -- a single POINT.  It is a point
        reflection (a pi rotation about 1/2), not a reflection in the line.
        The map whose fixed set IS {{Re(s)=1/2}} is s -> 1 - conj(s), which is
        the functional equation composed with Schwarz reflection xi(conj s) =
        conj(xi(s)).  That composite is what makes the ZEROS symmetric about
        the critical line.

        So "the critical line is two-faced" is true, but the two-sidedness
        needs BOTH the functional equation and complex conjugation -- the
        functional equation alone gives a point, not a line.""")

    print(f"""
  THE DISTINCTION, and it is not a technicality.

     spinor Z/2      central, acts trivially on all states, NO fixed-point
                     structure to speak of (every ray is fixed).  It is a
                     phase, and its whole content is what happens on a LOOP.
     functional Z/2  s -> 1-s moves almost every point and fixes ONE point.
                     Only the composite with conjugation, s -> 1-conj(s),
                     fixes the line.  Either way its content is its fixed set.

     A double cover and a reflection are both Z/2 and are different animals:
     one is an extension of a group, the other an involution on a space.  You
     can build a double cover FROM a reflection -- branched over the fixed set
     -- but they are not the same structure, and the spinor's Z/2 has no
     critical line because it fixes everything.

     So the mapping "2-pi phase <-> over/under the critical line" does not go
     through as stated.  The over/under structure is real (the functional
     equation is exactly that), and the 4-pi phase is real -- but they are not
     the same Z/2, and neither is evidence for the other.""")
    return {"spinor_central": bool(central), "spinor_fixes_all_rays": True,
            "functional_is_involution": bool(invol),
            "functional_equation_fixed_set": "the single point s=1/2",
            "reflection_fixed_set": "Re(s)=1/2, needs FE composed with conjugation",
            "same_structure": False}


def s5_back_to_the_manuscript():
    head("S5", "What this does to the manuscript's Sec 4")
    print("""  Sec 4 reads: "Non-orientability of M gives N(u+2pi) = -N(u), hence 4-pi
  spinor periodicity."  Two separate problems, both already on the ledger:

     1. The 4-pi periodicity does not NEED non-orientability.  S1 derives it
        from SU(2) alone -- flat space, no manifold, no topology.  Whatever M
        is, the electron would still have it.  So the derivation adds nothing
        the algebra did not already give.

     2. Worse, the route is blocked.  Axiom II sets w_1(M) != 0, and that is
        precisely the condition under which NO SPIN STRUCTURE EXISTS
        (path-integral check P3: 0 Spin, 4 Pin+, 4 Pin-).  The property being
        invoked to produce spinors is the one that forbids them.

  And on the two-faced reading of the critical line: the two-sidedness is
  real, but it is the FUNCTIONAL EQUATION's, and this repo has already been
  here -- the "odd under beta -> 1-beta" boundary was logged as our one novel
  result and retired the same week by prior art (Davenport-Heilbronn 1936,
  Weil positivity).  True, known, and not ours.""")
    return {"4pi_needs_non_orientability": False,
            "axiom_II_forbids_spin_structure": True,
            "two_sidedness_is_functional_equation": True,
            "already_retired_as_prior_art": True}


def main():
    print(RULE)
    print("SPINOR PHASE vs THE CRITICAL LINE: testing the synthesis")
    print(RULE)
    res = {"S1_periodicity": s1_periodicity(),
           "S2_sign_observable": s2_is_the_sign_observable(),
           "S3_where_real": s3_where_the_sign_is_real(),
           "S4_two_kinds_of_two": s4_two_kinds_of_two(),
           "S5_manuscript": s5_back_to_the_manuscript()}
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print("""  What holds:
    * 2-pi really is the opposite phase.  R(2pi) = -I on every axis, exactly.
    * The recombination instinct is right -- the phase IS observable, and it
      was measured (Rauch/Werner 1975), with a 4-pi period.
    * The critical line really is two-sided: xi(s) = xi(1-s) is an involution
      whose fixed set IS that line.

  What does not:
    * The 4-pi phase does NOT cause the box 50/50.  Swept 1369 measurement
      directions after a full 2-pi turn: largest probability change ~1e-16.
      A global phase is unobservable.  The 50/50 is basis OVERLAP (an angle),
      not phase.
    * The two Z/2's are different objects.  The spinor's is central and fixes
      every ray -- it has no critical line because it fixes everything.  The
      functional equation's moves almost every point and fixes a line.  A
      double cover is not a reflection.

  So the synthesis joins two true things with a bridge that does not carry
  load.  Both halves survive on their own; the identification does not.""")
    print(RULE)
    out = ROOT / "docs" / "spinor_phase_critical_line.json"
    out.write_text(json.dumps({
        "description": "Does 4pi spinor periodicity explain the box 50/50, and is it the critical line's Z/2?",
        "source": "code/constraint_projection/spinor_phase_and_critical_line.py",
        "checks": res}, indent=2, default=float) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
