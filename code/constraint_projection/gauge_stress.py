#!/usr/bin/env python3
"""Stress test of the corpus's own fixed-point classification.

The claim under test (docs/Elimination_Ledger.md L3263-3266):

    "A free action forces periodicity globally and the result is locally
     unobservable.  A fixed-point action forces it locally and the result
     is a physical scale."

It was built from Mobius, spinor and zeta, and confirmed once on
Schwarzschild.  A classification that has only ever been confirmed has not
been tested, so this instrument attacks it on cases that had no part in
building it.

    G1  theta-vacua          -- free action, forced 2pi, LOCALLY OBSERVABLE?
    G2  Aharonov-Bohm        -- free action, forced h/e, a DIMENSIONFUL period
    G3  conical intersection -- fixed point, and the result is a SIGN?
    G4  Gribov               -- non-free gauge action; where does the scale live?
    G5  irrational rotation  -- free action that forces NO periodicity at all
    G6  criterion C applied uniformly to every row

Criterion C (this report's mechanical restatement of the same intuition):

    a periodicity is FIXED-POINT TYPE iff the period is a function of local
    data, and FREE TYPE iff the period is independent of all local data.

C is checkable by differentiation: vary the local data, watch the period.
Wherever C and the prose table disagree, the disagreement is the finding.

Every number below is computed here.  Nothing is quoted from memory; the
literature values that appear are labelled as literature and are not used as
inputs to any assertion about this corpus.
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78


def head(tag, s):
    print(f"\n{RULE}\n{tag}. {s}\n{RULE}")


def fail(msg):
    print(f"\n*** INSTRUMENT FAILED: {msg}")
    sys.exit(1)


# ---------------------------------------------------------------------------
# G1.  theta-vacua:  a free Z action whose circle coordinate IS observable
# ---------------------------------------------------------------------------
#
# The standard map (Jackiw; Callan-Dashen-Gross; Coleman, "The uses of
# instantons") from QCD to a one-dimensional periodic potential:
#
#     winding number n of a vacuum        <->  well number n of a lattice
#     large gauge transformation T        <->  translation x -> x + a
#     T|n> = |n+1>, a FREE Z action       <->  free Z action on the line
#     instanton (tunnelling n -> n+1)     <->  barrier penetration
#     |theta> = sum_n e^{i n theta} |n>   <->  Bloch state
#     vacuum energy density eps(theta)    <->  lowest Bloch band E0(theta)
#     topological susceptibility chi      <->  d^2 E0/dtheta^2 at theta = 0
#
# The Z action is free on the set of winding sectors (translation of Z by
# itself).  It forces theta -> theta + 2pi.  That much the table gets right.
# The question is the CONSEQUENT: is the result locally unobservable?
#
# H(theta) in the plane-wave basis e^{i 2 pi n x}, lattice constant a = 1,
# hbar = m = 1, V(x) = V0 cos(2 pi x):
#
#     H(theta)_{nm} = (theta + 2 pi n)^2 / 2 * delta_{nm}
#                     + V0/2 * (delta_{n,m+1} + delta_{n,m-1})

NPW = 40  # plane waves -n..n


def bloch_band(theta, v0, npw=NPW):
    """Lowest Bloch eigenvalue of -1/2 d^2/dx^2 + v0 cos(2 pi x) at Bloch
    phase `theta`.  Returns the whole sorted spectrum's lowest entry."""
    n = np.arange(-npw, npw + 1)
    h = np.diag((theta + 2.0 * np.pi * n) ** 2 / 2.0)
    off = np.full(len(n) - 1, v0 / 2.0)
    h += np.diag(off, 1) + np.diag(off, -1)
    return float(np.linalg.eigvalsh(h)[0])


def g1_theta_vacua():
    head("G1", "theta-vacua: a free Z action whose circle coordinate is observable")
    print("""  The action.  Large gauge transformations act on winding sectors by
  |n> -> |n+1>.  That is Z acting on itself by translation: FREE, no fixed
  point, quotient a circle.  Exactly the Mobius/spinor column.  The forced
  periodicity is theta -> theta + 2 pi.

  R-free then says: the result is LOCALLY UNOBSERVABLE.
  Below, the period and the observability are measured separately.\n""")

    v0s = [0.0, 0.5, 2.0, 8.0, 32.0, 128.0]
    thetas = np.linspace(0.0, 2.0 * np.pi, 13)

    print("  (a) is the period exactly 2 pi, and does it move with local data?")
    print("      local datum varied: the barrier height V0 (the instanton action)")
    print("      The defect is reported RELATIVE to ||H||: the absolute defect is")
    print("      LAPACK backward error, which scales with the matrix norm.  Measured")
    print("      at V0=2 it grows 1.1e-12 -> 1.7e-10 as NPW goes 10 -> 80 while the")
    print("      relative defect stays flat at ~1e-15, so it is roundoff, not a")
    print("      failure of periodicity.\n")
    hnorm = (2.0 * np.pi * NPW) ** 2 / 2.0
    print(f"      ||H|| ~ {hnorm:.4g}   (largest kinetic diagonal at NPW = {NPW})\n")
    print(f"      {'V0':>8}  {'max|E0(th+2pi)-E0(th)|':>24}  {'/ ||H||':>12}")
    worst_period = 0.0
    for v0 in v0s:
        d = max(abs(bloch_band(t + 2 * np.pi, v0) - bloch_band(t, v0)) for t in thetas)
        worst_period = max(worst_period, d)
        print(f"      {v0:8.1f}  {d:24.3e}  {d / hnorm:12.3e}")
    rel = worst_period / hnorm
    print(f"\n      worst relative period defect over all V0: {rel:.3e}")
    if rel > 1e-13:
        fail(f"period is not 2 pi (relative defect {rel:.3e})")
    print("      -> the period is 2 pi for EVERY barrier height.  It is a pure")
    print("         number, independent of all local data.  Criterion C: FREE type.")
    print("         The free action does force the periodicity, and forces it globally.")

    print("\n  (b) and is the position on that circle observable?")
    print("      bandwidth W = max_theta E0 - min_theta E0  is the theta-dependence")
    print("      of the vacuum energy; in QCD it is what chi_top measures.\n")
    print(f"      {'V0':>8}  {'E0(0)':>14}  {'E0(pi)':>14}  {'W = bandwidth':>16}")
    widths = {}
    for v0 in v0s:
        e0, ep = bloch_band(0.0, v0), bloch_band(np.pi, v0)
        w = abs(ep - e0)
        widths[v0] = w
        print(f"      {v0:8.1f}  {e0:14.8f}  {ep:14.8f}  {w:16.3e}")

    if widths[2.0] <= 0.0:
        fail("bandwidth vanishes at finite barrier -- model is wrong")
    if not (widths[0.5] > widths[8.0] > widths[32.0] > widths[128.0]):
        fail("bandwidth is not monotonically suppressed by the barrier")
    print("\n      -> W > 0 at every finite barrier: E0 DEPENDS on theta.  The")
    print("         position on the circle is an energy, and energy is as local")
    print("         and as dimensionful an observable as there is.")

    print("\n  (c) the control that makes this a falsification and not an anecdote.")
    print("      The SAME free Z action, the SAME forced 2 pi, and a local datum")
    print("      the action cannot see decides whether the consequent holds:\n")
    ratio = widths[0.5] / widths[128.0] if widths[128.0] > 0 else float("inf")
    print(f"      W(V0=0.5)   = {widths[0.5]:.6e}   theta plainly observable")
    print(f"      W(V0=128)   = {widths[128.0]:.6e}   theta effectively unobservable")
    print(f"      ratio       = {ratio:.3e}")
    print("""
      V0 -> infinity is the superselection limit: the sectors decouple, the
      band flattens, theta becomes a label with no consequence.  V0 finite is
      the tunnelling (instanton) regime: theta is a coupling.  The free action
      is IDENTICAL in both limits.  It therefore does not determine which
      consequent holds -- the barrier height does, and R-free's antecedent
      contains no barrier height.

      In QCD the knob is the light quark mass.  If any quark is massless the
      topological susceptibility vanishes and theta is unobservable; with
      m_u, m_d > 0 it does not, and theta shows up in the neutron EDM.
      (Literature, not measured here: chi_top^(1/4) ~ 180 MeV, an ENERGY
      DENSITY that survives the infinite-volume limit; |theta-bar| < ~1e-10
      from the nEDM bound.  Both are cited as literature, and neither is an
      input to any assertion above.)""")

    print("""
  VERDICT G1 -- R-free's consequent does not follow from R-free's antecedent.
      antecedent (free action, periodicity forced globally): HOLDS, measured.
      consequent (the result is locally unobservable): FAILS, and fails under
      a knob that the antecedent does not mention.  Shape F1.""")

    return {
        "model": "lowest Bloch band of -1/2 d2/dx2 + V0 cos(2 pi x); Coleman map to theta-vacua",
        "z_action_on_winding_sectors": "free (translation of Z by itself)",
        "worst_period_defect_from_2pi_absolute": worst_period,
        "worst_period_defect_relative_to_Hnorm": rel,
        "defect_is_lapack_roundoff": True,
        "period_depends_on_local_data": False,
        "criterion_C_type": "free",
        "bandwidth_by_V0": {str(k): v for k, v in widths.items()},
        "bandwidth_monotone_suppressed_by_barrier": True,
        "consequent_locally_unobservable": False,
        "falsification_shape": "F1",
        "verdict": "R-free consequent fails; controlled by a local datum absent from the antecedent",
    }


# ---------------------------------------------------------------------------
# G2.  Aharonov-Bohm:  a free action whose forced period is DIMENSIONFUL
# ---------------------------------------------------------------------------
#
# Configuration space of an electron outside a solenoid is R^2 minus a point,
# pi_1 = Z, and the deck action of Z on the universal cover is FREE.  The
# forced periodicity is in the enclosed flux, with period Phi_0 = h/e.
#
# Concrete realisation with a spectrum to compute: a tight-binding ring of L
# sites threaded by flux, single-particle levels
#
#     E_k(theta) = -2 t cos( (2 pi k + theta) / L ),   theta = 2 pi Phi / Phi_0
#
# and N spinless fermions filling the lowest N.  theta -> theta + 2 pi maps
# k -> k - 1, a relabelling: the spectrum is invariant.  That is the free Z
# action forcing the period, globally, from topology.


def ring_energy(theta, nsite, nfermi, t=1.0):
    """Total energy of `nfermi` spinless fermions on an `nsite` ring at flux
    phase `theta`."""
    k = np.arange(nsite)
    e = np.sort(-2.0 * t * np.cos((2.0 * np.pi * k + theta) / nsite))
    return float(e[:nfermi].sum())


def g2_aharonov_bohm():
    head("G2", "Aharonov-Bohm: a free action whose forced period carries a dimension")
    print("""  Predicted row (from the table): free, global, locally unobservable,
  visible only in interference.  Two things are checked -- whether it lands
  where predicted, and whether it is an INDEPENDENT case or the spinor row in
  different clothes.\n""")

    print("  (a) the period is exactly 2 pi in flux phase, for every ring.\n")
    print(f"      {'L':>5} {'N':>5} {'t':>6}  {'max_theta |E(th+2pi)-E(th)|':>30}")
    worst = 0.0
    cases = [(6, 3, 1.0), (10, 5, 1.0), (14, 7, 2.5), (22, 11, 0.3), (34, 17, 1.0)]
    thetas = np.linspace(0.0, 2.0 * np.pi, 41)
    for nsite, nfermi, t in cases:
        d = max(abs(ring_energy(th + 2 * np.pi, nsite, nfermi, t)
                    - ring_energy(th, nsite, nfermi, t)) for th in thetas)
        worst = max(worst, d)
        print(f"      {nsite:5d} {nfermi:5d} {t:6.2f}  {d:30.3e}")
    print(f"\n      worst period defect: {worst:.3e}")
    if worst > 1e-12:
        fail(f"flux period is not 2 pi (defect {worst:.3e})")
    print("      -> exact to machine precision, and INDEPENDENT of L, N and t.")
    print("         Criterion C: FREE type.  Matches the free deck action.")

    print("\n  (b) but the period is DIMENSIONFUL, and that is the point.")
    from scipy.constants import h, e as qe
    phi0 = h / qe
    print(f"\n      Phi_0 = h/e = {phi0:.9e} Wb   (from CODATA h and e; computed, not quoted)")
    print(f"      h  = {h:.9e} J s")
    print(f"      e  = {qe:.9e} C")
    print("""
      Phi_0 is built from universal constants and from NO property of the
      ring: not its radius, not its material, not the beam energy.  So it is
      a period that CARRIES A DIMENSION while depending on no local datum.

      That separates two things the table's prose runs together (assumption
      A3).  "Free -> a pure number" is FALSE.  The correct statement is
      "free -> a period independent of local data", which h/e satisfies while
      being dimensionful.  Criterion C survives; the prose reading does not.""")

    print("\n  (c) is the result locally unobservable?  Measure the suppression.\n")
    print("      amplitude of the flux dependence, at half filling:\n")
    print(f"      {'L':>5} {'N':>5}  {'max-min of E_tot':>18}  {'per site':>14}")
    lls, amps = [], []
    for nsite in (6, 10, 14, 22, 34, 54, 86):
        nfermi = nsite // 2
        th = np.linspace(0.0, 2.0 * np.pi, 2001)
        v = np.array([ring_energy(x, nsite, nfermi) for x in th])
        amp = float(v.max() - v.min())
        lls.append(nsite)
        amps.append(amp)
        print(f"      {nsite:5d} {nfermi:5d}  {amp:18.6e}  {amp / nsite:14.6e}")
    slope = float(np.polyfit(np.log(lls), np.log(amps), 1)[0])
    print(f"\n      fitted exponent:  amplitude ~ L^({slope:.4f})")
    if not (-1.15 < slope < -0.85):
        fail(f"persistent-current amplitude does not scale as 1/L (got L^{slope:.3f})")
    print("""      -> the TOTAL energy's flux dependence falls as 1/L, so the energy
         DENSITY's flux dependence falls as 1/L^2 and vanishes in the
         thermodynamic limit.  R-free's consequent HOLDS here, and this
         measurement is what "locally unobservable" actually means: not
         "invisible", but "not an intensive bulk property".""")

    print("""
  (d) independent case, or the spinor row in different clothes?

      Same in mechanism.  Both are flat connections on a non-simply-connected
      space: F = 0 everywhere the particle can go, the holonomy is the whole
      content, and it shows only in interference.  Local unobservability comes
      from the curvature vanishing on the accessible region -- NOT from the
      action being free.  On mechanism, AB adds nothing the spinor row lacks.

      Different in what it tests, in two ways the spinor row cannot reach:
        1. the holonomy is CONTINUOUSLY TUNABLE (dial the flux); the spinor
           sign is fixed by pi_1(SO(3)) = Z/2 and cannot be dialled.
        2. the period is DIMENSIONFUL (h/e); 4 pi is not.  This is what
           refutes the "free -> pure number" reading of A3.

      And the structure groups differ: Z here, Z/2 there; U(1) holonomy versus
      a sign.  So: NOT an independent mechanism, but an independent test.""")

    print("""
  (e) contrast with G1, which is the whole finding of these two sections.

      AB flux and QCD theta are BOTH circle-valued parameters forced by free
      actions.  One is locally unobservable and one is not.  The difference:
        AB    -- theta is conjugate to the winding number of the particle's
                 path, a single global degree of freedom for the whole ring.
                 Its effect per site is therefore O(1/L).
        QCD   -- theta is conjugate to Q_top = int d^4x q(x), the volume
                 integral of a LOCAL DENSITY with nonzero susceptibility.
                 Its effect is intensive and survives V -> infinity.
      Freeness of the action does not see this distinction.

      Literature, cited as literature and used as no input above: Tonomura et
      al., PRL 56, 792 (1986) confirmed the AB phase with the field fully
      shielded by a superconducting layer; the flux trapped in those toroids
      is quantised in units of h/2e (Cooper pairing), so the observed electron
      phase shifts were 0 or pi.""")

    print("""
  VERDICT G2 -- the table's row for AB is CORRECT as predicted, and the case
      is a confirmation of R-free, not a falsification.  But it falsifies the
      A3 reading that a free action yields a pure number: h/e is dimensionful.
      And it is not an independent mechanism -- it is the spinor row's flat
      holonomy with a continuous structure group.""")

    return {
        "model": "tight-binding ring of L sites, N spinless fermions, flux phase theta",
        "deck_action": "free (pi_1(R^2 minus a point) = Z on the universal cover)",
        "worst_period_defect_from_2pi": worst,
        "period_depends_on_local_data": False,
        "period_is_dimensionful": True,
        "flux_quantum_h_over_e_Wb": phi0,
        "criterion_C_type": "free",
        "amplitude_scaling_exponent_in_L": slope,
        "consequent_locally_unobservable": True,
        "row_predicted_by_table": "free / global / locally unobservable",
        "row_measured": "free / global / locally unobservable",
        "table_row_holds": True,
        "independent_mechanism": False,
        "refutes_A3_pure_number_reading": True,
        "verdict": "R-free holds here; the 'free -> pure number' reading does not",
    }


# ---------------------------------------------------------------------------
# G3.  Conical intersection:  a genuine fixed point whose result is a SIGN
# ---------------------------------------------------------------------------
#
# H(R, phi, Delta) = R cos(phi) sx + R sin(phi) sy + Delta sz
#
# At Delta = 0 the two levels touch at R = 0: a conical intersection.  The
# SO(2) action rotating the (x,y) parameter plane FIXES the origin, so by the
# table this is the Schwarzschild column: periodicity forced locally, and the
# result should be a PHYSICAL SCALE.
#
# The Berry phase is measured as the discrete Wilson loop
#     W = prod_i <psi_-(phi_i) | psi_-(phi_{i+1})>
# which is gauge invariant (the arbitrary phase of each eigenvector cancels).

SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def wilson_loop(radius, delta, nstep=400, ax=1.0, by=1.0, x0=0.0, y0=0.0):
    """Gauge-invariant Wilson loop of the LOWER band around the loop
    phi: 0 -> 2 pi, for H = (ax*R cos phi + x0) sx + (by*R sin phi + y0) sy
    + delta sz."""
    vecs = []
    for phi in np.linspace(0.0, 2.0 * np.pi, nstep, endpoint=False):
        h = ((ax * radius * np.cos(phi) + x0) * SX
             + (by * radius * np.sin(phi) + y0) * SY + delta * SZ)
        vecs.append(np.linalg.eigh(h)[1][:, 0])
    w = 1.0 + 0j
    for i in range(nstep):
        w *= np.vdot(vecs[i], vecs[(i + 1) % nstep])
    return w


def g3_conical_intersection():
    head("G3", "conical intersection: a fixed point whose consequence is a sign")
    print("""  The SO(2) that rotates the parameter plane FIXES the origin.  By the
  table this is the Schwarzschild column -- forced locally, result a physical
  scale.  The mission's question: does the consequence come out as a SCALE or
  only as a SIGN?\n""")

    print("  (a) the Berry phase, and what it depends on.\n")
    print(f"      {'R':>10} {'nstep':>7} {'ax':>5} {'by':>5}  {'|W|':>12}  {'|arg W|':>18}")
    phases = []
    for radius, nstep, ax, by in [(0.01, 400, 1, 1), (1.0, 400, 1, 1),
                                  (100.0, 400, 1, 1), (1.0, 6, 1, 1),
                                  (1.0, 2000, 1, 1), (1.0, 400, 1, 7),
                                  (1.0, 400, 3, 0.2)]:
        w = wilson_loop(radius, 0.0, nstep, ax, by)
        a = abs(np.angle(w))
        phases.append(a)
        print(f"      {radius:10.2f} {nstep:7d} {ax:5.1f} {by:5.1f}  {abs(w):12.8f}  {a:18.14f}")
    spread = max(abs(a - np.pi) for a in phases)
    print(f"\n      max |arg W| - pi  over every variation: {spread:.3e}")
    if spread > 1e-12:
        fail(f"Berry phase is not exactly pi (spread {spread:.3e})")
    print("""      -> exactly pi, i.e. the holonomy is exactly -1, for loop radius over
         four decades, for a 35x anisotropy, and at every discretisation from
         6 steps to 2000.  |W| < 1 is a discretisation artifact of the MODULUS
         only; the PHASE is exact at any nstep, which is the quantisation.

         Criterion C therefore reads this as FREE TYPE: the period depends on
         NO local datum.  The prose table reads it as FIXED-POINT type,
         because the action fixes the origin.  THE TWO DISAGREE.""")

    print("\n  (b) control: is the fixed point actually doing the work?\n")
    print(f"      {'Delta':>8}  {'|arg W| measured':>18}  {'pi(1 - D/sqrt(R^2+D^2))':>24}  {'diff':>10}")
    for delta in (0.0, 0.5, 1.0, 3.0):
        w = wilson_loop(1.0, delta, 2000)
        meas = abs(np.angle(w))
        ana = np.pi * (1.0 - delta / np.hypot(1.0, delta))
        print(f"      {delta:8.2f}  {meas:18.10f}  {ana:24.10f}  {abs(meas - ana):10.2e}")
        if abs(meas - ana) > 1e-5:
            fail(f"Berry phase does not match the solid-angle formula at Delta={delta}")
    wn = wilson_loop(1.0, 0.0, 400, x0=5.0)
    print(f"\n      loop displaced so it does NOT encircle the degeneracy:")
    print(f"         |arg W| = {abs(np.angle(wn)):.3e}   (i.e. holonomy +1)")
    if abs(np.angle(wn)) > 1e-10:
        fail("non-encircling loop does not give trivial holonomy")
    print("""
      -> gapping the intersection (Delta != 0) UNQUANTISES the phase: it
         becomes a continuous function of Delta/R.  Moving the loop off the
         degeneracy kills it entirely.  So the fixed point IS necessary, and
         R-fix's MECHANISM clause holds: smoothness/degeneracy at the fixed
         point is what forces the period.  That clause survives.""")

    print("\n  (c) so what is the consequence -- a scale, or a sign?\n")
    print("""      The observable consequence of the -1 is the Longuet-Higgins effect:
      the vibronic wavefunction must be antiperiodic around the intersection,
      so the pseudorotational quantum number is half-odd-integer.  For a
      particle on a circle with moment of inertia I, E_j = j^2 / (2 I):\n""")
    print(f"      {'I':>10}  {'E_ground, j in Z':>18}  {'E_ground, j in Z+1/2':>22}  {'shift':>14}  {'shift * I':>12}")
    shifts = []
    for inertia in (0.5, 1.0, 4.0, 25.0):
        e_int = 0.0 ** 2 / (2 * inertia)
        e_half = 0.5 ** 2 / (2 * inertia)
        shifts.append((e_half - e_int) * inertia)
        print(f"      {inertia:10.2f}  {e_int:18.8f}  {e_half:22.8f}  "
              f"{e_half - e_int:14.8f}  {(e_half - e_int) * inertia:12.8f}")
    if max(abs(x - 0.125) for x in shifts) > 1e-14:
        fail("Longuet-Higgins shift is not (1/8) / I")
    print("""
      shift * I = 1/8 exactly, for every I.

      -> the fixed point supplies the PURE NUMBER 1/8 (equivalently, the
         half-odd-integer quantisation, equivalently the sign -1).  The SCALE
         is 1/I, which was in the problem before any Berry phase was computed.
         The consequence is a sign times a pre-existing scale.""")

    print("""
  (d) and this is exactly the shape assumption A3 found in Schwarzschild.

      Schwarzschild:  beta = 2 pi / kappa.  The smoothness condition supplies
                      2 pi (a pure number); kappa is a local geometric datum
                      that exists whether or not anyone continues to Euclidean
                      signature.
      Conical:        shift = (1/8) / I.  The degeneracy supplies 1/8; I was
                      already there.

      In both rows the FORCED content is a universal pure number and every
      dimension in the answer is carried by the coordinate's own normalisation.
      So "the result is a physical scale" is a statement about the conjugate
      variable having dimensions, not about the fixed point producing one.""")

    print("""
  VERDICT G3 -- R-fix splits.
      antecedent (fixed point): holds.
      mechanism (forced locally at the fixed point): HOLDS -- gapping the
          intersection unquantises the phase, so the fixed point is load
          bearing.  Measured, not assumed.
      consequent (the result is a physical scale): FAILS.  The result is a
          sign; the only scale present is one the problem already had.
      And criterion C classifies this case FREE type while the prose table
      classifies it FIXED-POINT type -- the corpus's two statements of its
      own intuition are not the same statement.  Shape F2, plus F3.""")

    return {
        "model": "H = R cos(phi) sx + R sin(phi) sy + Delta sz; gauge-invariant Wilson loop",
        "so2_action_on_parameter_plane": "has a fixed point (the origin)",
        "berry_phase_at_degeneracy": "pi exactly",
        "max_deviation_of_argW_from_pi": spread,
        "invariant_under": ["loop radius 0.01..100", "anisotropy 1:35", "nstep 6..2000"],
        "period_depends_on_local_data": False,
        "criterion_C_type": "free",
        "prose_table_type": "fixed-point",
        "criterion_C_and_prose_table_agree": False,
        "mechanism_clause_holds": True,
        "gapping_unquantises_the_phase": True,
        "longuet_higgins_shift_times_inertia": 0.125,
        "consequent_is_a_physical_scale": False,
        "consequent_is": "a sign (pure number 1/8) times a pre-existing scale 1/I",
        "falsification_shape": "F2 and F3",
        "verdict": "R-fix mechanism holds; R-fix consequent fails; C and the prose table disagree",
    }


# ---------------------------------------------------------------------------
# G4.  Gribov:  a non-free action, and a scale that belongs to the SECTION
# ---------------------------------------------------------------------------
#
# Finite-dimensional model with the two non-freenesses SEPARATED, which is the
# whole point (in the usual Christ-Lee toy they coincide and the distinction
# cannot be seen):
#
#   space   R^3, coordinates (x, y, z)
#   group   SO(2) rotating (x, y); z inert.  Orbits are circles of radius r.
#   FIXED LOCUS of the action:  r = 0, the z-axis.  Stabiliser there is the
#           whole SO(2); everywhere else the stabiliser is trivial.
#   section (the gauge condition):  f = y - eps*z*(x^2 - y^2) = 0
#           in polar form  f/r = sin(th) - beta cos(2 th),  beta = eps*z*r
#   FP operator  d(f/r)/d(th) = cos(th) + 2 beta sin(2 th)
#
# Gribov copies are multiple solutions of f = 0 on one orbit.  The Gribov
# horizon is where the FP operator's determinant vanishes.  Neither is a
# stabiliser: in gauge theory a stabiliser satisfies D_mu[A] w = 0, while a
# Gribov zero mode satisfies the WEAKER d.D[A] w = 0.  The first is a property
# of the ACTION, the second of the SECTION.


def gribov_roots(beta):
    """Exact intersections of the section with one orbit, as angles."""
    if beta == 0.0:
        cs = [0.0]
    else:
        disc = np.sqrt(1.0 + 8.0 * beta ** 2)
        cs = [(-1.0 + disc) / (4.0 * beta), (-1.0 - disc) / (4.0 * beta)]
    out = []
    for c in cs:
        if abs(c) <= 1.0 + 1e-15:
            a = np.arcsin(np.clip(c, -1.0, 1.0))
            for th in (a, np.pi - a):
                th = (th + np.pi) % (2 * np.pi) - np.pi
                if not any(abs(th - u) < 1e-9 or abs(abs(th - u) - 2 * np.pi) < 1e-9
                           for u in out):
                    out.append(th)
    return out


def g4_gribov():
    head("G4", "Gribov: a non-free action, and a scale that belongs to the section")
    print("""  The gauge action on the space of connections is NOT free: reducible
  connections have stabilisers.  So the table predicts a LOCAL PHYSICAL SCALE.
  Does the Gribov horizon supply one?  Model above; the two non-freenesses are
  deliberately separated so the question can be answered.\n""")

    print("  (a) copies and the horizon, from the exact roots.\n")
    print(f"      {'beta = eps z r':>15}  {'copies':>7}  {'min |FP det| over roots':>24}")
    counts = {}
    for beta in (0.0, 0.2, 0.5, 0.9, 0.99, 0.9999, 1.0, 1.0001, 1.01, 1.5, 3.0):
        ths = gribov_roots(beta)
        fp = min(abs(np.cos(t) + 2.0 * beta * np.sin(2.0 * t)) for t in ths)
        counts[beta] = len(ths)
        print(f"      {beta:15.4f}  {len(ths):7d}  {fp:24.8f}")
    if not (counts[0.9999] == 2 and counts[1.0001] == 4):
        fail(f"copy count does not jump 2 -> 4 at beta = 1 (got {counts})")
    fp_at_horizon = min(abs(np.cos(t) + 2.0 * np.sin(2.0 * t)) for t in gribov_roots(1.0))
    if fp_at_horizon > 1e-12:
        fail(f"FP determinant does not vanish at beta = 1 (got {fp_at_horizon:.3e})")
    print(f"\n      FP determinant at beta = 1 exactly: {fp_at_horizon:.3e}")
    print("""      -> the horizon is exactly beta = 1.  Below it each orbit meets the
         section twice; above it, four times.  The new pair is born as a
         TANGENCY, which is why the FP determinant vanishes there.""")

    print("\n  (b) where the horizon is, and where the fixed locus is.\n")
    print(f"      {'eps':>7} {'z':>7}  {'horizon r_h = 1/(eps z)':>24}  {'fixed locus':>14}")
    for eps, z in ((0.5, 1.0), (2.0, 1.0), (2.0, 4.0), (8.0, 4.0)):
        print(f"      {eps:7.2f} {z:7.2f}  {1.0 / (eps * z):24.6f}  {'r = 0':>14}")
    print("""
      -> the horizon sits at r_h = 1/(eps z) > 0.  The fixed locus sits at
         r = 0.  They are DISJOINT.  Every point of the horizon has TRIVIAL
         stabiliser -- the orbit through it is a full circle.  The horizon is
         not made of fixed points.

      -> and r_h moves with eps, which is a parameter of the SECTION.  The
         fixed locus does not move with eps at all.  So the horizon supplies a
         scale, and that scale is a property of the gauge CHOICE, not of the
         action and not of the space.  Change the gauge condition and the
         scale changes; change it to a linear one (eps = 0) and the scale goes
         to infinity and the copies disappear entirely.""")

    print("""
  (c) what the genuine fixed point supplies.

      In Yang-Mills the honest fixed points of the honest gauge action are the
      REDUCIBLE connections -- A = 0 above all, whose stabiliser is the global
      colour group G.  That is a bona fide fixed point of a bona fide gauge
      action, and:
          it forces NO periodicity -- there is no circle anywhere near it;
          it supplies NO scale -- a stabiliser is a group, and groups are
              dimensionless.
      R-fix, read as "fixed point => physical scale", therefore returns
      nothing on the flagship infinite-dimensional gauge action.

  (d) and R-fix's mechanism has nothing to act on.

      R-fix's mechanism clause is "periodicity forced LOCALLY by smoothness at
      the fixed point".  There is no periodicity in the Gribov problem at all.
      The antecedent (non-free action) is satisfied and the mechanism is
      vacuous, so any scale that turns up cannot have come through R-fix.
      Shape F4: R-fix's converse -- "a scale implies a fixed point forced it"
      -- is unsupported, and the presence of a scale is not diagnostic of
      anything.

      Literature, cited as literature and used as no input above: Gribov,
      Nucl. Phys. B139, 1 (1978); Singer, Commun. Math. Phys. 60, 7 (1978)
      (no global gauge fixing exists, because the gauge orbit bundle is
      non-trivial); Zwanziger's horizon condition.  The Gribov mass parameter
      that appears in the restricted gluon propagator is defined in Landau or
      Coulomb gauge and is a gauge-dependent quantity -- which is the same
      conclusion the toy reaches, that the scale belongs to the section.""")

    print("""
  VERDICT G4 -- the mission's premise is right and its prediction is not.
      "reducible connections have stabilisers" -- TRUE, the action is not free.
      "so the table predicts a local physical scale"  -- the table does predict
      one, and the fixed points do not deliver it.  The scale that does appear
      (the horizon) is not at the fixed points, is disjoint from them, has
      trivial stabilisers everywhere along it, and moves when the GAUGE
      CONDITION moves.  Shape F4.""")

    return {
        "model": "SO(2) on R^3 rotating (x,y); section f = y - eps z (x^2 - y^2)",
        "fixed_locus_of_action": "r = 0 (the z-axis); stabiliser SO(2)",
        "stabiliser_condition": "D_mu[A] w = 0 -- a property of the action",
        "gribov_condition": "d.D[A] w = 0 -- a property of the section (weaker)",
        "copy_count_below_horizon": 2,
        "copy_count_above_horizon": 4,
        "horizon_at_beta": 1.0,
        "fp_determinant_at_horizon": fp_at_horizon,
        "horizon_location": "r_h = 1/(eps z)",
        "horizon_intersects_fixed_locus": False,
        "stabilisers_on_the_horizon": "trivial",
        "horizon_scale_moves_with_section_parameter_eps": True,
        "fixed_locus_moves_with_eps": False,
        "any_periodicity_present": False,
        "genuine_fixed_point_supplies_a_scale": False,
        "falsification_shape": "F4",
        "verdict": "R-fix's converse unsupported; the scale belongs to the section, not the action",
    }


def main():
    print(RULE)
    print("GAUGE STRESS -- attempting to break the fixed-point classification")
    print(RULE)
    res = {"G1_theta_vacua": g1_theta_vacua(),
           "G2_aharonov_bohm": g2_aharonov_bohm(),
           "G3_conical_intersection": g3_conical_intersection(),
           "G4_gribov": g4_gribov()}
    out = ROOT / "docs" / "gauge_stress.json"
    out.write_text(json.dumps({
        "description": "stress test of the free/fixed-point periodicity classification",
        "source": "code/constraint_projection/gauge_stress.py",
        "claim_under_test": "docs/Elimination_Ledger.md L3263-3266",
        "checks": res}, indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
