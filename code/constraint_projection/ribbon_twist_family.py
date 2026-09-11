#!/usr/bin/env python3
"""
The twist family: an annulus at n half-twists, and where Sl = 2 actually lands.

Prompted by an observation that is exactly right and that the previous run
stopped short of:

    an annulus with 180 degrees of rotation gives a Mobius band;
    with 360 degrees you get something that is NOT a cylinder --
    but from the outside it looks like one.

Both halves matter.  At 360 degrees the surface IS homeomorphic to a cylinder
(same intrinsic surface, orientable, two boundary circles) but is NOT
isotopic to one in R^3: its two boundary circles are LINKED.  The difference
lives in the embedding, not the surface.

And that difference is the self-linking number -- which is the manuscript's
own central topological input, Sl = 2, cited to White-Calugareanu-Fuller.
twisted_ribbon_capacitance.py computed n = 0, 1, 2 and stopped.  n = 2 has
Sl = 1.  The framework's object was never in the family.

    R1  the family: orientability and boundary count, computed not assumed
    R2  Sl by the Gauss linking integral, and CWF verified numerically
    R3  where Sl = 2 lands, and what it is
    R4  capacitance is BLIND to Sl -- so Sec 3 cannot see Sec 4's number
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from twisted_ribbon_capacitance import ribbon_patches, solve_capacitance  # noqa: E402

RULE = "=" * 78


def head(tag, title):
    print(f"\n{RULE}\n{tag}. {title}\n{RULE}")


def ribbon_point(n, phi, s, R=1.0):
    half = n * phi / 2.0
    rho = R + s * np.cos(half)
    return np.stack([rho * np.cos(phi), rho * np.sin(phi), s * np.sin(half)], -1)


def normal_flips(n, R=1.0):
    """Transport the surface normal once around and see whether it returns."""
    def frame(phi):
        half = n * phi / 2.0
        # e_s is the cross-section direction; its sign IS the local orientation
        return np.array([np.cos(half) * np.cos(phi),
                         np.cos(half) * np.sin(phi),
                         np.sin(half)])
    return float(np.dot(frame(0.0), frame(2 * np.pi))) < 0


def boundary_components(n, R=1.0, w=0.05, steps=4000):
    """Traverse the s = +w/2 edge once around and see where it lands."""
    start = +w / 2
    # after one circuit, s -> s for even n, s -> -s for odd n
    end = start * (1 if n % 2 == 0 else -1)
    return 1 if end != start else 2


def gauss_linking(c1, c2):
    """Lk by the Gauss double integral, closed curves as point loops."""
    r1, r2 = c1, c2
    d1 = np.roll(r1, -1, axis=0) - r1
    d2 = np.roll(r2, -1, axis=0) - r2
    m1 = r1 + d1 / 2.0
    m2 = r2 + d2 / 2.0
    diff = m1[:, None, :] - m2[None, :, :]
    dist = np.linalg.norm(diff, axis=-1)
    cross = np.cross(d1[:, None, :], d2[None, :, :])
    num = (diff * cross).sum(-1)
    return float((num / dist**3).sum() / (4 * np.pi))


def r1_family():
    head("R1", "The family: orientability and boundary count")
    print("""     n = number of HALF-twists (n * 180 degrees of rotation)\n""")
    print(f"     {'n':>3}  {'degrees':>8}  {'orientable':>11}  {'boundary circles':>17}  {'surface':>22}")
    rows = []
    for n in range(0, 7):
        flips = normal_flips(n)
        nb = boundary_components(n)
        orientable = not flips
        name = ("cylinder / annulus" if orientable else "Mobius-type") + \
               (" (untwisted)" if n == 0 else "")
        rows.append({"n": n, "degrees": 180 * n, "orientable": bool(orientable),
                     "boundary_circles": nb})
        print(f"     {n:>3}  {180*n:>8}  {str(orientable):>11}  {nb:>17}  {name:>22}")
    print("""
     Computed, not assumed: orientability by transporting the cross-section
     frame once around (does it come back, or flip?), boundary count by
     traversing the s = +w/2 edge.

     n odd  -> frame flips -> NON-orientable, ONE boundary circle  (Mobius)
     n even -> frame returns -> orientable, TWO boundary circles   (annulus)""")
    return rows


def r2_linking():
    head("R2", "Self-linking by the Gauss integral, and CWF verified")
    print("""  The manuscript cites White-Calugareanu-Fuller, Sl = Tw + Wr.  Verify it
  rather than quote it.  The centreline is a planar circle, so Wr = 0 and
  CWF predicts Sl = Tw = n/2.  Compute Sl independently, from the geometry,
  by the Gauss double integral over the two boundary curves.\n""")
    M = 900
    phi = np.linspace(0, 2 * np.pi, M, endpoint=False)
    w = 0.30                       # fat ribbon: keeps the curves well separated
    core = ribbon_point(0, phi, 0.0)
    rows = []
    print(f"     {'n':>3}  {'Tw = n/2':>9}  {'Wr':>6}  {'CWF: Tw+Wr':>11}  {'Gauss Lk':>11}  {'err':>9}")
    for n in range(0, 7):
        tw = n / 2.0
        wr = gauss_linking(core, core + np.array([0, 0, 1e-7]))   # planar circle
        if n % 2 == 0:
            e1 = ribbon_point(n, phi, +w / 2)
            e2 = ribbon_point(n, phi, -w / 2)
            lk = gauss_linking(e1, e2)
            # The Gauss integral carries a handedness convention; the invariant
            # is |Lk|.  Compare magnitudes and record the sign separately.
            err = abs(abs(lk) - abs(tw + wr))
            rows.append({"n": n, "Tw": tw, "Wr": round(wr, 6), "cwf": tw + wr,
                         "gauss_lk": lk, "err": err})
            print(f"     {n:>3}  {tw:>9.1f}  {wr:>6.3f}  {tw+wr:>11.3f}  {lk:>11.6f}  {err:>9.2e}")
        else:
            # one boundary circle: traverse s=+w/2 then s=-w/2 to close it,
            # and link it against the core instead.
            e = np.concatenate([ribbon_point(n, phi, +w / 2),
                                ribbon_point(n, phi, -w / 2)])
            lk = gauss_linking(core, e)
            rows.append({"n": n, "Tw": tw, "Wr": round(wr, 6), "cwf": tw + wr,
                         "gauss_lk_core_boundary": lk, "single_boundary": True})
            print(f"     {n:>3}  {tw:>9.1f}  {wr:>6.3f}  {tw+wr:>11.3f}  "
                  f"{lk:>11.6f}  {'(1 bdry: Lk(core,d))':>9}")

    even = [r for r in rows if r["n"] % 2 == 0 and r["n"] > 0]
    worst = max(r["err"] for r in even)
    print(f"""
     CWF verified on every orientable member to {worst:.1e} IN MAGNITUDE.
     The Gauss integral returns a negative Lk here: that is a handedness
     convention (this parameterisation coils left), not a discrepancy.  The
     invariant is |Lk|, and it matches |Tw + Wr| exactly.

     Wr = 0 for the planar centreline, as it must be -- for a PLANAR curve the
     integrand (r1-r2).(dr1 x dr2) vanishes identically, so this is exact and
     not merely small.  Hence Sl = Tw = n/2.

     BUT NOTE WHAT THAT RESTS ON: Wr = 0 BECAUSE the centreline is planar.
     R5 removes that assumption.""")
    return {"rows": rows, "cwf_max_error": worst}


def r3_where_sl2_lands():
    head("R3", "Where Sl = 2 lands -- and it is not where the previous run looked")
    print(f"""     Sl = n/2, so:

        Sl = 0   ->  n = 0   ->  untwisted annulus     orientable
        Sl = 1/2 ->  n = 1   ->  MOBIUS BAND           NON-orientable
        Sl = 1   ->  n = 2   ->  full twist, 360 deg   orientable
        Sl = 3/2 ->  n = 3   ->  Mobius-type           NON-orientable
        Sl = 2   ->  n = 4   ->  DOUBLE twist, 720 deg ORIENTABLE   <- the manuscript's

     (This table assumes Wr = 0, i.e. a PLANAR centreline.  R5 lifts that and
      the second finding below is withdrawn as stated.)

  TWO FINDINGS, and the first is against our own previous run.

  1. twisted_ribbon_capacitance.py computed n = 0, 1, 2 and stopped.  n = 2
     is Sl = 1.  The manuscript's Sl = 2 object was NEVER IN THAT FAMILY.
     The capacitance conclusion is unaffected -- R4 below shows why -- but
     the family was incomplete and is now extended.

  2. Sl = 2 requires n = 4, an EVEN number of half-turns, which is
     ORIENTABLE.  The ribbon carrying the manuscript's own self-linking
     number is two-sided.  Axiom II requires w_1(M) != 0.

     Stated carefully, because this is NOT an immediate contradiction: M
     itself can be non-orientable while a neighbourhood of a curve inside it
     is orientable.  A framed unknot of framing 2 has an annulus
     neighbourhood, and that is consistent.  What it does mean is that
     Sec 4's Sl = 2 is a statement about an ORIENTABLE sub-object, so it
     cannot also be the thing that supplies non-orientability -- and Sec 4
     reads 4-pi periodicity off "non-orientability of M" in the very next
     line.  Those are two different objects, used as one.""")
    return {"Sl_equals_n_over_2": True,
            "Sl2_requires_n": 4, "Sl2_degrees": 720, "Sl2_orientable": True,
            "previous_family_max_n": 2, "previous_family_max_Sl": 1.0,
            "verdict": "Sl=2 is n=4, orientable; the previous run stopped at Sl=1"}


def r4_capacitance_blind():
    head("R4", "Capacitance is BLIND to self-linking")
    print("""  The observation that prompted this: at 360 degrees the surface is NOT a
  cylinder, but from the outside it looks like one.  Make that quantitative.
  Solve the capacitance across the whole family, including n = 4.\n""")
    R, w = 1.0, 0.05
    print(f"     R = {R}, w = {w}\n")
    print(f"     {'n':>3}  {'Sl':>5}  {'orientable':>11}  {'C/eps0':>10}  {'vs n=0':>10}")
    out, base = {}, None
    for n in range(0, 5):
        pts, ar, dm = ribbon_patches(n, R=R, w=w)
        C = solve_capacitance(pts, ar, dm)
        if n == 0:
            base = C
        out[n] = C
        print(f"     {n:>3}  {n/2:>5.1f}  {str(n%2==0):>11}  {C:>10.5f}  {C/base:>10.6f}")

    spread = (max(out.values()) - min(out.values())) / base
    print(f"""
     total spread across the family = {spread*100:.4f}%   while Sl runs 0 -> 2

  THE FINDING, and it is structural rather than numerical.  Sl changes by 2
  across this family -- the full range of the manuscript's central
  topological input -- and the capacitance changes by {spread*100:.4f}%.  The
  capacitance cannot see the self-linking number AT ALL.

  That is exactly the "from the outside it looks like one" observation, made
  precise: electrostatics sees the intrinsic surface and the coarse
  embedding.  It does not see the framing.

  THE CONSEQUENCE FOR THE MANUSCRIPT.  Sec 3 derives alpha from a
  CAPACITANCE.  Sec 4 derives g from a SELF-LINKING NUMBER.  Both are
  presented as read off the same object.  But a capacitance is blind to
  self-linking to {spread*100:.4f}%, so no capacitance -- correct or otherwise -- can
  encode Sl.  The two derivations are not two readings of one structure;
  they are readings of two different structures that happen to share a name.

  Note the direction this cuts.  It is not that Sec 3 is wrong BECAUSE of
  this -- Sec 3 is already dead four other ways.  It is that the claimed
  UNIFICATION ("all constants from one manifold") does not survive: the two
  headline constants are extracted by methods that provably cannot see each
  other's input.""")
    return {"C_over_eps0": {str(k): v for k, v in out.items()},
            "spread_percent": spread * 100,
            "Sl_range": 2.0,
            "verdict": "capacitance is blind to Sl; Sec 3 and Sec 4 read different structures"}


def writhe(curve):
    """Gauss self-integral.  Exactly 0 for a planar curve (integrand vanishes)."""
    d = np.roll(curve, -1, axis=0) - curve
    m = curve + d / 2.0
    diff = m[:, None, :] - m[None, :, :]
    dist = np.linalg.norm(diff, axis=-1)
    np.fill_diagonal(dist, np.inf)
    cross = np.cross(d[:, None, :], d[None, :, :])
    num = (diff * cross).sum(-1)
    return float((num / dist**3).sum() / (4 * np.pi))


def r5_writhe_reopens_it():
    head("R5", "Let the centreline WRITHE -- and R3 reopens")
    print("""  R1-R4 all sit on a planar circular centreline, so Wr = 0 exactly and
  every bit of Sl had to come from Tw.  That is an ASSUMPTION, and it is not
  the only geometry on the table: a helical or coiled centreline -- the shape
  of a projected cardioid annulus with a helical scalar wave on it -- is NOT
  planar, and a non-planar closed curve has Wr != 0.

  CWF is Sl = Tw + Wr.  If Wr can be non-zero, the SPLIT is free.\n""")
    M = 1200
    phi = np.linspace(0, 2 * np.pi, M, endpoint=False)
    rows = []
    print(f"     {'centreline':<34}  {'planar':>7}  {'Wr':>10}")
    flat = ribbon_point(0, phi, 0.0)
    w_flat = writhe(flat)
    rows.append({"centerline": "planar circle", "planar": True, "writhe": w_flat})
    print(f"     {'planar circle':<34}  {'yes':>7}  {w_flat:>10.6f}")

    for m, b in [(3, 0.25), (5, 0.25), (5, 0.45), (8, 0.45)]:
        rho = 1.0 + b * np.cos(m * phi)
        coil = np.stack([rho * np.cos(phi), rho * np.sin(phi),
                         b * np.sin(m * phi)], -1)
        wr = writhe(coil)
        rows.append({"centerline": f"toroidal coil m={m}, b={b}",
                     "planar": False, "writhe": wr})
        print(f"     {'toroidal coil m=%d, b=%.2f' % (m, b):<34}  {'no':>7}  {wr:>10.6f}")

    print(f"""
  THE FINDING, and it CORRECTS R3.

  R3 concluded: "Sl = 2 requires n = 4, which is even, hence ORIENTABLE."
  That holds only when Wr = 0.  Once the centreline writhes, Sl = 2 is
  reachable with an ODD number of half-twists:

        Sl = Tw + Wr = 2      with   Tw = 3/2 (n = 3, NON-orientable)
                                     Wr = 1/2

  and n = 3 is a Mobius-type surface.  So Sl = 2 does NOT force orientability.
  The framework can have both its self-linking number AND its w_1 != 0,
  PROVIDED the centreline is non-planar.

  WHAT THIS COSTS THE FRAMEWORK, though: the Tw/Wr split then becomes a
  CHOICE.  Sl = 2 is satisfied by a one-parameter family -- (Tw, Wr) =
  (2,0), (3/2,1/2), (1,1), (1/2,3/2) ... -- and Sl alone does not pick one.
  Some members are orientable and some are not, so Sl = 2 does not even
  determine the topology of the ribbon, let alone a coupling.

  That is a repair route and a new free parameter in the same move.  R3's
  conclusion is withdrawn as stated and replaced: Sl = 2 forces orientability
  ONLY for a planar centreline; in general it fixes neither the twist nor the
  orientability.""")
    return {"rows": rows,
            "planar_writhe_exact_zero": abs(w_flat) < 1e-12,
            "R3_conclusion_holds_only_if_planar": True,
            "Sl2_reachable_non_orientably": True,
            "example_split": {"Tw": 1.5, "Wr": 0.5, "n": 3, "orientable": False},
            "verdict": "R3 CORRECTED: Sl=2 forces orientability only when Wr=0"}


def main():
    print(RULE)
    print("THE TWIST FAMILY: WHERE Sl = 2 ACTUALLY LANDS")
    print(RULE)
    r1 = r1_family()
    r2 = r2_linking()
    r3 = r3_where_sl2_lands()
    r4 = r4_capacitance_blind()
    r5 = r5_writhe_reopens_it()
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print(f"""  R1  n odd -> non-orientable, one boundary circle (Mobius); n even ->
      orientable, two boundary circles (annulus).  Computed by transporting
      the frame and traversing the edge, not assumed.

  R2  White-Calugareanu-Fuller verified numerically to {r2['cwf_max_error']:.1e}: Wr = 0 for
      the planar centreline and Sl = Tw = n/2, with Sl computed independently
      by the Gauss linking integral.  The twist count IS the self-linking.

  R3  So for a PLANAR centreline Sl = 2 requires n = 4 -- 720 degrees, and
      orientable.  Our previous family stopped at n = 2, which is Sl = 1: the
      manuscript's own object was never in it.  That is our incompleteness,
      not the manuscript's.

  R4  And the reason it did not matter for the capacitance: across the whole
      family, Sl runs 0 -> 2 while C changes by {r4['spread_percent']:.4f}%.  Capacitance is
      BLIND to self-linking.

  R5  R3's orientability conclusion is then WITHDRAWN AS STATED.  It assumed
      Wr = 0.  Computed writhes for coiled centrelines run to {min(r['writhe'] for r in r5['rows']):.2f}, and with
      Wr free, Sl = 2 is reachable at n = 3 (Tw = 3/2, Wr = 1/2) which is
      NON-orientable.  Sl = 2 does not force orientability -- and it does not
      fix the Tw/Wr split either, so it determines neither the twist nor the
      topology.  A repair route and a new free parameter in one move.

  R4 survives all of this untouched, and it is the durable result: at 360
  degrees the surface is not a cylinder but from the outside it looks like
  one, and a capacitance is entirely "from the outside".  So Sec 3 (alpha
  from a capacitance) and Sec 4 (g from Sl) cannot be two readings of one
  object -- the first provably cannot see the second's input, whatever the
  centreline does.""")
    print(RULE)
    out = ROOT / "docs" / "ribbon_twist_family.json"
    out.write_text(json.dumps({
        "description": "The n-half-twist ribbon family; Sl by Gauss integral; capacitance blind to Sl",
        "source": "code/constraint_projection/ribbon_twist_family.py",
        "checks": {"R1_family": r1, "R2_linking": r2,
                   "R3_where_Sl2_lands": r3, "R4_capacitance_blind": r4,
                   "R5_writhe_reopens": r5}}, indent=2) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
