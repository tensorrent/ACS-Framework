#!/usr/bin/env python3
"""Schwarzschild through the fixed-point classification.

The last three runs sorted Z/2 and U(1) actions by what they FIX:

    Mobius deck, spinor -I on states .... free, fix nothing
    spinor -I on rays ................... fixes everything (trivial)
    s -> 1 - conj(s) .................... fixes a LINE (the critical line)

Schwarzschild belongs in that table, and putting it there answers a question
the spinor work raised but did not settle: BOTH systems force a periodicity --
4 pi for the spinor, beta = 8 pi M for Euclidean Schwarzschild -- and it is
not obvious they do it for the same reason.

    W1  is the horizon a real singularity, or a coordinate artifact?
    W2  Euclidean continuation: derive the period, do not quote it
    W3  what does the Killing flow FIX?  -> where Schwarzschild sits
    W4  the two mechanisms of periodicity, side by side
    W5  what the manuscript actually uses gravity for

Every tensor is computed from the metric.  Nothing is quoted from memory.
"""
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


t, r, th, ph, M, eps = sp.symbols("t r theta phi M epsilon", positive=True)
X = [t, r, th, ph]
f = 1 - 2 * M / r
G = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th) ** 2)


def christoffel(g, x):
    gi = g.inv()
    n = len(x)
    return [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b])
                                          - sp.diff(g[b, c], x[d])) for d in range(n)) / 2)
              for c in range(n)] for b in range(n)] for a in range(n)]


def riemann(Ga, x):
    n = len(x)
    return [[[[sp.simplify(sp.diff(Ga[a][b][d], x[c]) - sp.diff(Ga[a][b][c], x[d])
                           + sum(Ga[a][c][e] * Ga[e][b][d] - Ga[a][d][e] * Ga[e][b][c]
                                 for e in range(n)))
               for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]


def w1_horizon_is_a_coordinate_artifact():
    head("W1", "Is the horizon a singularity, or an artifact of the chart?")
    print(f"     metric g_tt = {-f},   g_rr = {1/f}\n")
    print(f"     at r = 2M:  g_tt -> {sp.simplify((-f).subs(r, 2*M))},"
          f"   g_rr -> divergent")
    print("     -- which alone proves nothing.  A chart can blow up where the\n"
          "        geometry does not.  So compute a SCALAR, which no coordinate\n"
          "        change can move.\n")
    Ga = christoffel(G, X)
    Rm = riemann(Ga, X)
    n = 4
    Rl = [[[[sp.simplify(sum(G[a, e] * Rm[e][b][c][d] for e in range(n)))
             for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    gi = G.inv()
    # Rl is FULLY LOWERED (R_abcd).  Raise all four of ITS indices -- an
    # earlier draft raised Rm (whose first index is already contravariant)
    # with four metrics, i.e. one raising too many, and produced a spurious
    # sin(theta) dependence and a divergence at the horizon.
    Ru = [[[[sp.simplify(sum(gi[a, e] * gi[b, ff] * gi[c, g2] * gi[d, h] * Rl[e][ff][g2][h]
                             for e in range(n) for ff in range(n)
                             for g2 in range(n) for h in range(n)))
             for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    K = sp.simplify(sp.expand(sum(Rl[a][b][c][d] * Ru[a][b][c][d]
                                  for a in range(n) for b in range(n)
                                  for c in range(n) for d in range(n))))
    print(f"     Kretschmann  K = R_abcd R^abcd = {K}")
    K_h = sp.simplify(K.subs(r, 2 * M))
    finite = K_h.is_finite is True or (K_h.free_symbols and not K_h.has(sp.zoo, sp.oo))
    print(f"     at r = 2M:   K = {K_h}      finite?  {bool(finite)}")
    print(f"     as r -> 0:   K -> {sp.limit(K, r, 0)}")
    print(f"     matches the standard 48 M^2/r^6?  "
          f"{sp.simplify(K - 48*M**2/r**6) == 0}")
    print("""
     The horizon is a COORDINATE artifact: the invariant curvature is finite
     there and diverges only at r = 0.  So the surface at r = 2M is a place
     where the chart fails, not where the geometry does -- which is exactly
     what makes the next step legitimate.""")
    return {"kretschmann": str(K), "K_at_horizon": str(K_h),
            "finite_at_horizon": bool(finite),
            "matches_48M2_over_r6": bool(sp.simplify(K - 48*M**2/r**6) == 0),
            "diverges_at": "r = 0"}


def w2_euclidean_period():
    head("W2", "Euclidean continuation: derive the period")
    print("""  Set tau = i t.  The Euclidean metric near the horizon is a 2D surface in
  (tau, r); if it is smooth there, the angular coordinate must close at 2 pi,
  and that fixes the period of tau.  Derive it -- do not quote it.\n""")
    rho = sp.symbols("rho", positive=True)
    # r = 2M + rho^2/(8M)  is the substitution that makes g_rr dr^2 -> drho^2.
    sub = 2 * M + rho**2 / (8 * M)
    g_rr = sp.simplify((1 / f).subs(r, sub) * sp.diff(sub, rho) ** 2)
    g_tt = sp.simplify(f.subs(r, sub))
    print(f"     substitute r = 2M + rho^2/(8M):")
    print(f"        g_rr dr^2  ->  ({sp.simplify(g_rr)}) drho^2")
    print(f"        f(r)       ->  {sp.simplify(g_tt)}")
    lead = sp.simplify(sp.series(g_tt, rho, 0, 3).removeO())
    print(f"        f near rho=0 ->  {lead}")
    print(f"\n     so  ds_E^2 = drho^2 + rho^2 d(tau/(4M))^2  -- a PLANE in polar form,")
    print(f"     with angle  Theta = tau/(4M).  Smoothness at rho = 0 needs Theta")
    print(f"     to have period 2 pi, hence:\n")
    beta = sp.simplify(2 * sp.pi * 4 * M)
    kappa = sp.simplify(sp.diff(f, r).subs(r, 2 * M) / 2)
    T = sp.simplify(1 / beta)
    print(f"        period  beta = 8 pi M  = {beta}")
    print(f"        surface gravity kappa = f'(2M)/2 = {kappa}")
    print(f"        temperature T = 1/beta = {T}   = kappa/(2 pi) = {sp.simplify(kappa/(2*sp.pi))}")
    print(f"        consistency  T == kappa/2pi ?  {sp.simplify(T - kappa/(2*sp.pi)) == 0}")
    print("""
     The period is not chosen.  It is FORCED, by demanding the Euclidean
     geometry be smooth at rho = 0.  Any other period leaves a conical deficit
     at the tip -- a curvature delta-function sitting exactly on the horizon.""")
    return {"beta": str(beta), "surface_gravity": str(kappa), "temperature": str(T),
            "T_equals_kappa_over_2pi": bool(sp.simplify(T - kappa / (2 * sp.pi)) == 0)}


def w3_what_the_flow_fixes():
    head("W3", "What does the Killing flow FIX?")
    print("""  The period in W2 belongs to a U(1) action -- translation in Euclidean
  time, generated by the Killing vector xi = d/dt.  Its norm decides the
  fixed set.\n""")
    norm2 = sp.simplify(-G[0, 0])
    print(f"     |xi|^2 = -g_tt = {norm2}")
    for R in (4 * M, 3 * M, 2 * M):
        v = sp.simplify(norm2.subs(r, R))
        print(f"        at r = {R}:  |xi|^2 = {v}    {'FIXED (xi vanishes)' if v == 0 else 'moves'}")
    print(f"""
     The Killing vector VANISHES at r = 2M and nowhere else outside it.  So
     the U(1) has a fixed set, and that fixed set is the horizon -- the tip of
     the Euclidean cigar.

     That places Schwarzschild squarely on one side of the classification:""")
    rows = [
        ("Mobius deck (annulus -> band)", "Z/2", "nothing", True, "no smoothness condition"),
        ("spinor -I on states S^3", "Z/2", "nothing", True, "no smoothness condition"),
        ("s -> 1 - conj(s)", "Z/2", "the line Re(s)=1/2", False, "reflection"),
        ("Euclidean time translation", "U(1)", "the horizon r=2M", False, "CONICAL: period forced"),
    ]
    print(f"\n     {'action':<32} {'group':>5}  {'fixed set':<20} {'free?':>6}")
    for nm, grp, fx, free, _ in rows:
        print(f"     {nm:<32} {grp:>5}  {fx:<20} {str(free):>6}")
    return {"killing_norm2": str(norm2), "vanishes_at": "r = 2M",
            "action_is_free": False, "fixed_set": "the horizon",
            "classification": [{"action": a, "group": g, "fixed": f_, "free": fr}
                               for a, g, f_, fr, _ in rows]}


def w4_two_mechanisms():
    head("W4", "Two periodicities, two different mechanisms")
    print("""  Both the spinor and Schwarzschild force a period.  They do it for
  opposite reasons, and the classification is what separates them.

     SPINOR, period 4 pi
        the Z/2 acts FREELY -- it fixes nothing.
        There is no point at which to impose smoothness, so nothing local
        forces anything.  The period is a GLOBAL topological fact: pi_1(SO(3))
        = Z/2, so a loop must be traversed twice to be contractible.
        Consequence: the sign is invisible on a single system (S2 swept 1369
        directions, max change 3.33e-16) and shows only in interference.

     SCHWARZSCHILD, period beta = 8 pi M
        the U(1) has a FIXED POINT -- the horizon.
        A fixed point of a rotation is exactly where a conical deficit can
        live, so smoothness THERE forces the period locally.  Get it wrong and
        you get a curvature delta-function on the horizon.
        Consequence: the period is not a phase convention, it is a temperature
        -- and it is measurable in principle, as Hawking radiation.

  THE SEPARATION.  A free action forces periodicity globally (topology) and the
  result is unobservable locally.  A fixed-point action forces it locally
  (smoothness at the fixed point) and the result is a physical scale.

  So "a full rotation returns you inverted" and "imaginary time is periodic"
  are NOT the same phenomenon wearing different clothes.  They sit on opposite
  rows of the same table, and the column that separates them is the one built
  in the previous three runs: what does the action fix?""")
    return {"spinor": {"period": "4 pi", "free": True, "forced_by": "global topology",
                       "locally_observable": False},
            "schwarzschild": {"period": "8 pi M", "free": False,
                              "forced_by": "smoothness at the fixed point",
                              "locally_observable": True}}


def w5_manuscript():
    head("W5", "What the manuscript uses gravity for")
    print("""  The CPF entry does not derive a metric, a horizon, or a temperature.  It
  invokes "Gravity from Entropy" at exactly one load-bearing point: to fix the
  cutoff a as "the eigenvalue gap of the G-field" (Sec 3).

  So Schwarzschild is not a test OF the manuscript -- there is nothing there to
  test against.  What it does supply is a CONTROL for the audit's own methods:

     * W1 shows the standard move for telling a coordinate artifact from a real
       one: compute a scalar.  This audit used the same move on the capacitance
       (G3: does the factor 8 EMERGE, or was it imposed?).
     * W2 shows a period DERIVED from a smoothness requirement rather than
       asserted -- the shape the manuscript's a/R fixing does not have, since
       that exponent is CODATA alpha^-1 minus one.
     * W3/W4 extend the fixed-point classification to a U(1), and it still
       sorts cleanly.  A classification that only worked on the cases it was
       built from would be worth little.

  That last point is the useful one: the table was built from Mobius, spinor
  and zeta, and Schwarzschild -- which had no part in building it -- lands in
  it without adjustment.""")
    return {"manuscript_derives_a_metric": False,
            "gfe_used_for": "fixing the cutoff a as an eigenvalue gap",
            "schwarzschild_role": "control for the audit's methods, not a test of the entry"}


def main():
    print(RULE)
    print("SCHWARZSCHILD THROUGH THE FIXED-POINT CLASSIFICATION")
    print(RULE)
    res = {"W1_coordinate_artifact": w1_horizon_is_a_coordinate_artifact(),
           "W2_euclidean_period": w2_euclidean_period(),
           "W3_fixed_set": w3_what_the_flow_fixes(),
           "W4_two_mechanisms": w4_two_mechanisms(),
           "W5_manuscript": w5_manuscript()}
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print("""  W1  Kretschmann computed from the metric: 48 M^2/r^6, finite at r = 2M,
      divergent only at r = 0.  The horizon is a chart failure, not a
      geometric one.
  W2  Euclidean period DERIVED from smoothness at the tip: beta = 8 pi M,
      kappa = 1/(4M), T = kappa/2pi -- checked, not quoted.
  W3  the Killing vector vanishes at r = 2M and nowhere outside it, so the
      U(1) has a FIXED SET and it is the horizon.
  W4  and that is the separation.  The spinor's 4 pi comes from a FREE action
      and is forced by global topology, so it is locally invisible.
      Schwarzschild's beta comes from a FIXED POINT and is forced by local
      smoothness, so it is a temperature.  Same word, opposite mechanisms.

  The classification was built from Mobius, spinor and zeta.  Schwarzschild had
  no part in building it and lands in it without adjustment -- which is the
  only reason to trust a classification at all.""")
    print(RULE)
    out = ROOT / "docs" / "schwarzschild_periodicity.json"
    out.write_text(json.dumps({
        "description": "Schwarzschild through the fixed-point/free-action classification",
        "source": "code/constraint_projection/schwarzschild_periodicity.py",
        "checks": res}, indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
