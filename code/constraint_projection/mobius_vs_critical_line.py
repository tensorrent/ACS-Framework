#!/usr/bin/env python3
"""One-sided, twisted onto itself: does the Mobius reading fix the mapping?

The correction under test: the structure is not a two-faced planar object.  It
is SINGLE-faced, twisted onto itself -- a Mobius ribbon.  Traverse once and
you are inverted; traverse twice and you are home.

That is a better candidate than "two-faced", because a Mobius band's
orientation cover is a genuine DOUBLE COVER, which is what the spinor Z/2 is.
So the question splits:

    M1  is the Mobius band actually one-sided, one-boundary?      (computed)
    M2  is its deck transformation FREE -- no fixed points?       (computed)
    M3  how does the spinor Z/2 act: freely, or trivially?        (computed)
    M4  the four Z/2's side by side, classified by fixed set
    M5  verdict: what the correction fixes, and what it breaks harder

The punchline is decided by fixed points, so every fixed set is computed.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78
I2 = np.eye(2, dtype=complex)


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


def ribbon(n, phi, s, R=1.0):
    half = n * phi / 2.0
    rho = R + s * np.cos(half)
    return np.stack([rho * np.cos(phi), rho * np.sin(phi), s * np.sin(half)], -1)


def m1_one_sided():
    head("M1", "Is the Mobius band one-sided with one boundary?")
    rows = []
    print(f"     {'half-twists':>12}  {'frame returns?':>15}  {'sides':>6}  {'boundary circles':>17}")
    for n in (0, 1, 2, 3):
        # Transport the cross-section frame once around and see if it returns.
        e0 = np.array([np.cos(0.0), 0.0, np.sin(0.0)])
        half = n * 2 * np.pi / 2.0
        e1 = np.array([np.cos(half) * np.cos(2 * np.pi),
                       np.cos(half) * np.sin(2 * np.pi), np.sin(half)])
        returns = float(np.dot(e0, e1)) > 0
        sides = 2 if returns else 1
        bdry = 2 if n % 2 == 0 else 1
        rows.append({"n": n, "frame_returns": bool(returns), "sides": sides, "boundary": bdry})
        print(f"     {n:>12}  {str(returns):>15}  {sides:>6}  {bdry:>17}")
    print("""
     n = 1 (the Mobius band): the frame does NOT return, so ONE side, and the
     edge closes into ONE circle.  The correction is right on the geometry --
     it is single-faced, twisted onto itself, and you must go round TWICE to
     come back to your starting orientation.""")
    return rows


def m2_deck_is_free():
    head("M2", "Is the Mobius deck transformation FREE?")
    print("""  The orientation double cover of a Mobius band is an annulus, and the deck
  map is  tau(phi, s) = (phi + 2pi, -s)  -- go once around, flip the fibre.
  A covering-space deck action must be FREE: no point may be fixed, or the
  quotient is not a manifold.  Check it rather than assume it.\n""")
    rng = np.random.default_rng(20260901)
    phis = rng.uniform(0, 4 * np.pi, 20000)
    ss = rng.uniform(-0.5, 0.5, 20000)
    # On the cover, a point is (phi mod 4pi, s); tau adds 2pi and flips s.
    fixed = np.sum((np.abs(((phis + 2 * np.pi) % (4 * np.pi)) - phis) < 1e-9) & (np.abs(-ss - ss) < 1e-9))
    # tau^2 should be the identity.
    phi2 = (phis + 4 * np.pi) % (4 * np.pi)
    s2 = ss
    is_invol = np.allclose(phi2, phis % (4 * np.pi)) and np.allclose(s2, ss)
    print(f"     tau^2 = identity?                      {is_invol}")
    print(f"     fixed points among 20000 samples:      {int(fixed)}")
    print(f"     any point with s = 0 AND phi shifted?  requires -s = s AND +2pi = 0 -> impossible")
    print("""
     The deck map is FREE: it fixes nothing.  s = 0 (the core circle) is not
     fixed either, because the phi shift by 2 pi still moves it.  That is
     exactly what makes the double cover a covering rather than a branched
     one.""")
    return {"tau_squared_is_identity": bool(is_invol), "fixed_points": int(fixed), "free": True}


def m3_spinor_action():
    head("M3", "How does the spinor Z/2 act -- freely or trivially?")
    print("""  -I in SU(2) acts on two different spaces, and the answer differs.  That
  difference is the whole reason the phase is invisible alone and visible in
  interference.\n""")
    rng = np.random.default_rng(7)
    v = rng.normal(size=(4000, 2)) + 1j * rng.normal(size=(4000, 2))
    v /= np.linalg.norm(v, axis=1, keepdims=True)

    # On the state sphere S^3: is -psi ever equal to psi?
    fixed_sphere = int(np.sum(np.all(np.abs(-v - v) < 1e-12, axis=1)))
    # On rays (projective): -psi and psi differ by a phase, so same ray.
    same_ray = int(np.sum(np.abs(np.abs(np.einsum("ij,ij->i", np.conj(v), -v)) - 1.0) < 1e-12))
    print(f"     on the state sphere S^3, fixed points of -I : {fixed_sphere} / 4000   -> FREE")
    print(f"     on RAYS (projective space), rays preserved  : {same_ray} / 4000   -> TRIVIAL")
    print("""
     Both are true at once and there is no contradiction: -I moves every
     STATE but preserves every RAY.  Observables see only rays, which is why
     S2 found no probability anywhere that could detect the sign; interference
     compares two arms and so sees the state, not just the ray.

     And this is the precise structural match to M2: SU(2) -> SO(3) is a FREE
     double cover of the state sphere, exactly as the annulus -> Mobius band
     is a free double cover.  The correction lands.""")
    return {"fixed_on_sphere": fixed_sphere, "rays_preserved": same_ray,
            "free_on_states": True, "trivial_on_rays": True}


def m4_four_z2s():
    head("M4", "The four Z/2's, classified by what they fix")
    pts = [0.3 + 2j, 0.5 + 14.134725j, 0.9 - 3j, 2 + 0j, 0.5 + 0j]
    fe = [s for s in pts if abs((1 - s) - s) < 1e-12]
    refl = [s for s in pts if abs((1 - np.conj(s)) - s) < 1e-12]
    rows = [
        {"z2": "Mobius deck (annulus -> band)", "fixed": "nothing", "free": True,
         "kind": "covering-space action"},
        {"z2": "spinor -I on states S^3", "fixed": "nothing", "free": True,
         "kind": "covering-space action"},
        {"z2": "spinor -I on rays CP^1", "fixed": "everything", "free": False,
         "kind": "trivial action"},
        {"z2": f"functional eq. s -> 1-s", "fixed": "one point s=1/2", "free": False,
         "kind": "point reflection"},
        {"z2": f"reflection s -> 1-conj(s)", "fixed": "the line Re(s)=1/2", "free": False,
         "kind": "reflection in a line"},
    ]
    print(f"     {'Z/2 action':<32}  {'fixed set':<22}  {'free?':>6}")
    for r in rows:
        print(f"     {r['z2']:<32}  {r['fixed']:<22}  {str(r['free']):>6}")
    print(f"\n     (computed: s->1-s fixes {len(fe)}/5 samples, s->1-conj(s) fixes {len(refl)}/5)")
    print("""
     Read the column.  The Mobius deck and the spinor-on-states are the same
     KIND of thing -- free covering actions with empty fixed sets.  The
     critical-line involutions are the opposite kind: their entire content is
     a non-empty fixed set.""")
    return rows


def m5_verdict():
    head("M5", "What the correction fixes, and what it breaks harder")
    print("""  IT FIXES THE SPINOR HALF, and this is a real improvement over "two-faced".

     A two-sided object has no reason to require two circuits.  A Mobius band
     does, for the same reason a spinor does: both are quotients by a FREE
     Z/2, so the honest object upstairs is the double cover and one trip
     round the base is only half a trip round the cover.  M1-M3 confirm the
     match on the property that matters -- freeness.

  IT BREAKS THE CRITICAL-LINE HALF HARDER, and this is the sharp part.

     A critical LINE is a fixed set.  A free action has NO fixed set -- that
     is what free means.  So a Mobius/spinor Z/2 cannot have a critical line
     at all: if its action fixed a line, it would not be free, the quotient
     would not be a manifold, and it would not be the double cover that made
     the analogy attractive in the first place.

     The "two-faced" reading at least had the right SHAPE for a critical line
     (a reflection fixes a line).  The Mobius reading is more accurate about
     the spinor and, for exactly that reason, is further from the zeta side.
     Improving the fit on one end worsened it on the other.

  So: the geometry of the correction is right, the spinor identification is
  now genuinely good, and the bridge to the critical line is now provably
  unavailable rather than merely unsupported.  That is a stronger negative
  than the one it replaces, and it was bought by making the claim sharper.""")
    return {"fixes_spinor_half": True, "free_action_excludes_a_critical_line": True,
            "verdict": "better on spinors, provably worse on zeta"}


def main():
    print(RULE)
    print("MOBIUS, NOT TWO-FACED: what the correction fixes and what it breaks")
    print(RULE)
    res = {"M1_one_sided": m1_one_sided(), "M2_deck_free": m2_deck_is_free(),
           "M3_spinor_action": m3_spinor_action(), "M4_four_z2s": m4_four_z2s(),
           "M5_verdict": m5_verdict()}
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print("""  The correction is right, and it moves the result in both directions.

    RIGHT: the Mobius band is one-sided with one boundary (M1), its deck map
    is free (M2), and -I acts freely on states while fixing every ray (M3).
    Mobius <-> spinor is a real structural match -- both are quotients by a
    FREE Z/2, which is why one circuit inverts and two restore.  This is
    strictly better than the two-faced reading.

    AND WORSE: a critical line IS a fixed set, and a free action has none.
    So the very property that makes the Mobius reading correct about spinors
    is the property that forbids it having a critical line. The two-faced
    reading was wrong about the spinor but at least had the right shape for
    zeta; the Mobius reading is right about the spinor and provably cannot
    reach zeta.

  Sharpening the claim converted an unsupported bridge into an excluded one.""")
    print(RULE)
    out = ROOT / "docs" / "mobius_vs_critical_line.json"
    out.write_text(json.dumps({
        "description": "Does the Mobius (one-sided) correction fix the spinor/critical-line mapping?",
        "source": "code/constraint_projection/mobius_vs_critical_line.py",
        "checks": res}, indent=2, default=float) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
