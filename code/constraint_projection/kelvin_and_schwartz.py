#!/usr/bin/env python3
"""Two external checks on the ribbon/vortex ontology: Schwartz 2023, Kelvin 1867.

Both are prior art the corpus never searched (rule 4), and both bear directly
on the Mobius ribbon work.

  SCHWARTZ (Annals of Mathematics 2025, arXiv:2308.12641) settled the
  Halpern-Weaver conjecture: a flat Moebius band admitting a smooth ISOMETRIC
  embedding in R^3 has aspect ratio > sqrt(3).  Sharp, since bands of ratio
  sqrt(3)+eps exist.

  KELVIN (1867) proposed atoms ARE knotted vortex tubes -- the original
  "matter is topology" programme, and the reason Tait built the first knot
  tables.  It is the closest historical precursor to a Klein-foam/framed-knot
  ontology, and it was abandoned.  Why it was abandoned is the useful part.

    S1  do our ribbons satisfy the Schwartz bound?  (and does it even apply?)
    S2  where does OUR parameterisation actually self-intersect?
    S3  Schwartz's own three-year error -- prior art for rule 10
    K1  Kelvin's vortex atoms: what the programme claimed
    K2  Kelvin-Helmholtz: is a vortex ribbon even stable?
    K3  what killed it, and whether the same kill transfers
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78
SQRT3 = np.sqrt(3.0)


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


def ribbon(n, phi, s, R=1.0):
    half = n * phi / 2.0
    rho = R + s * np.cos(half)
    return np.stack([rho * np.cos(phi), rho * np.sin(phi), s * np.sin(half)], -1)


def s1_schwartz_bound():
    head("S1", "Do our ribbons satisfy the Schwartz bound -- and does it apply?")
    print(f"""  Schwartz: a flat Moebius band with a smooth ISOMETRIC embedding in R^3
  has aspect ratio (length/width) > sqrt(3) = {SQRT3:.6f}.  Sharp.

  The word ISOMETRIC is load-bearing and is the first thing to check, not the
  last: it means PAPER -- bending without stretching.  Our ribbons are ruled
  surfaces built by rotating a segment, which is NOT an isometry of a flat
  strip.  So the bound may not bind on us at all.  Test that rather than
  assume it either way.\n""")
    rows = []
    print(f"     {'w/R used':>10}  {'length 2piR':>12}  {'aspect':>10}  {'> sqrt3?':>9}  where")
    for w, where in [(0.05, "twisted_ribbon_capacitance, ribbon_twist_family"),
                     (0.30, "ribbon_twist_family R2 linking"),
                     (0.05 / 4, "a_eff = w/4, the field-equivalent radius")]:
        aspect = 2 * np.pi * 1.0 / w
        rows.append({"w_over_R": w, "aspect": aspect, "exceeds_sqrt3": bool(aspect > SQRT3),
                     "where": where})
        print(f"     {w:>10.4f}  {2*np.pi:>12.4f}  {aspect:>10.2f}  {str(aspect > SQRT3):>9}  {where}")
    worst = min(r["aspect"] for r in rows)
    print(f"""
     Every ribbon we used has aspect >= {worst:.1f}, versus a bound of {SQRT3:.3f}.  So the
     question never became live -- we were {worst/SQRT3:.0f}x clear of it.

     But note WHY that is not merely lucky: the bound constrains SHORT, WIDE
     bands, and every use here was a thin ring where the capacitance log
     ln(8R/a) needs w << R.  The physics we were computing forced us into the
     regime where the geometric constraint is slack.

     AND THE BOUND DOES NOT STRICTLY APPLY ANYWAY.  Our surface stretches --
     the |dr/dphi| metric factor varies with s -- so it is not a paper band.
     A non-isometric Moebius embedding can have any aspect ratio; the standard
     parameterisation self-intersects long before sqrt(3), which S2 measures.""")
    return {"sqrt3": float(SQRT3), "rows": rows, "min_aspect_used": float(worst),
            "bound_applies_to_our_surfaces": False,
            "reason": "our ribbons are ruled, not isometric embeddings of a flat strip"}


def s2_self_intersection():
    head("S2", "Where does OUR parameterisation actually break?")
    print("""  The relevant constraint on a non-isometric ribbon is embeddedness: at what
  width does the surface pass through itself?  Measure it.\n""")
    n_f, n_s = 400, 9
    phi = np.linspace(0, 2 * np.pi, n_f, endpoint=False)
    ss = np.linspace(-0.5, 0.5, n_s)
    print(f"     {'w/R':>8}  {'min |rho| (dist to axis)':>25}  {'min pair dist':>14}  {'degenerate?':>12}")
    rows = []
    for w in (0.05, 0.5, 1.0, 1.5, 1.9, 2.0, 2.2, 3.0):
        F, S = np.meshgrid(phi, ss * w, indexing="ij")
        rho = 1.0 + S * np.cos(1 * F / 2.0)          # the radial coordinate itself
        min_rho = float(np.abs(rho).min())
        signed_min = float(rho.min())
        P = ribbon(1, F, S).reshape(-1, 3)
        d = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=-1)
        idx = np.arange(P.shape[0]); fi = idx // n_s
        dphi = np.abs(fi[:, None] - fi[None, :]); dphi = np.minimum(dphi, n_f - dphi)
        d[dphi < 12] = np.inf
        m = float(d.min())
        # Degenerate when rho passes through 0: the surface reaches the axis
        # and folds through it.  That is what actually breaks, not a pairwise
        # near-miss between distant patches.
        degen = signed_min <= 0.0
        rows.append({"w_over_R": w, "min_abs_rho": min_rho, "signed_min_rho": signed_min,
                     "min_pair_distance": m, "degenerate": bool(degen)})
        print(f"     {w:>8.2f}  {min_rho:>25.5f}  {m:>14.5f}  {str(degen):>12}")
    first_bad = next((r["w_over_R"] for r in rows if r["degenerate"]), None)
    print(f"""
     The pairwise distance NEVER reaches zero -- it flattens near 0.085 and
     stays there, so distant-patch collision is not what limits this family.
     What breaks is the radial coordinate: rho = R + s cos(n phi/2) passes
     through ZERO once |s| reaches R, i.e. at w/R = 2, and the surface folds
     through its own axis.  First degenerate width measured: w/R = {first_bad}.

     So the working constraint is w/R < 2, from rho -> 0, and it is a
     coordinate degeneracy rather than a self-intersection.  Limiting aspect
     2 pi R / 2R = pi = {np.pi:.4f}, against Schwartz's {SQRT3:.3f} -- numerically
     adjacent, and not the same statement about the same object.""")
    return {"rows": rows, "our_constraint": "w/R < 2 (rho -> 0 at s = -R)",
            "first_degenerate_w_over_R": first_bad,
            "pairwise_distance_ever_zero": False,
            "our_limiting_aspect": float(np.pi),
            "schwartz_bound": float(SQRT3),
            "same_statement": False}


def s3_schwartz_method():
    head("S3", "Schwartz's own three-year error -- prior art for rule 10")
    print("""  The methodological content of this result is not the theorem, and it is
  documented in his own account of the work.

     2020  Schwartz attacks the conjecture ASSUMING the cut-open band is a
           PARALLELOGRAM.  The calculation does not give sqrt(3).  Stuck.
     2023  He cuts a paper Moebius band open and LOOKS at it.  It is a
           TRAPEZOID, not a parallelogram.  He reruns the same calculation
           with the corrected shape and the minimum falls out immediately.

  Three years separated the two, and the gap was one unexamined assumption
  about a shape he could have cut out at any point.

  THIS IS RULE 10 IN THE LITERATURE, and it is better prior art than anything
  the corpus has cited for it: "did you see it?  did you do it?  if no, you
  are assuming."  Schwartz assumed for three years, then looked.

  It is also rule 9 -- NAME the assumption, then lift it.  "Parallelogram" was
  never written down as an assumption; it was baked into the setup, which is
  exactly how "planar" was baked into our R1-R4 before R5 lifted it.

  Recorded as prior art.  Rules 9 and 10 are not ours.""")
    return {"year_stuck": 2020, "year_solved": 2023,
            "wrong_assumption": "cut-open band is a parallelogram",
            "actual": "trapezoid",
            "resolution": "cut one open and looked",
            "prior_art_for": ["rule 9 (name the assumption)", "rule 10 (did you see it)"]}


def k1_vortex_atoms():
    head("K1", "Kelvin 1867: the original 'matter is topology' programme")
    print("""  Kelvin proposed that atoms ARE knotted vortex tubes in the aether.  The
  motivation was Helmholtz's theorems (1858): in an ideal incompressible
  inviscid fluid, vortex lines are material lines and their TOPOLOGY IS
  CONSERVED FOR ALL TIME.  A knot, once tied, cannot untie.

  That gave exactly what a theory of matter wants:
     * discrete species          -- distinct knot types
     * absolute stability        -- topology cannot change under the dynamics
     * spectra                   -- vibrational modes of the tube
     * no free parameters        -- the knot table is what it is

  Tait built the first knot tables (1877-1885) FOR this programme.  Modern
  knot theory is its surviving output.

  This is the closest historical precursor to a framed-knot / Klein-foam
  ontology, and the corpus had not cited it.  Rule 4 and rule 5 both missed
  it: it is prior art, and it is prior art for the ONTOLOGY rather than for
  any single claim.""")
    return {"proposer": "Kelvin (W. Thomson), 1867",
            "basis": "Helmholtz 1858 vortex theorems: topology conserved in ideal fluid",
            "offered": ["discrete species", "absolute stability", "spectra",
                        "no free parameters"],
            "surviving_output": "knot theory (Tait tables, 1877-1885)"}


def k2_kelvin_helmholtz():
    head("K2", "Kelvin-Helmholtz: is a vortex ribbon even stable?")
    print("""  The stability question is answerable in closed form, and the answer is the
  reason the programme needed an IDEAL fluid.

  For a vortex sheet with velocity jump dU across it, inviscid and without
  surface tension, the linear growth rate of a perturbation of wavenumber k is

        sigma = k * dU / 2          -- growth, for EVERY k

  There is no stabilising term, so every wavelength grows, and shorter
  wavelengths grow FASTER.  The perturbation with the smallest resolvable
  wavelength dominates.\n""")
    dU = 1.0
    print(f"     {'wavelength':>12}  {'k = 2pi/lambda':>15}  {'growth sigma':>13}  {'e-fold time':>12}")
    rows = []
    for lam in (1.0, 0.1, 0.01, 1e-3, 1e-6):
        k = 2 * np.pi / lam
        sig = k * dU / 2
        rows.append({"wavelength": lam, "k": k, "sigma": sig, "efold": 1 / sig})
        print(f"     {lam:>12.0e}  {k:>15.3e}  {sig:>13.3e}  {1/sig:>12.3e}")
    print(f"""
     Growth is UNBOUNDED as lambda -> 0.  A bare vortex sheet has no shortest
     unstable wavelength, so it does not merely destabilise -- it does so
     infinitely fast in the ideal limit.

     THE CONSEQUENCE FOR THE ONTOLOGY.  Helmholtz's theorems give topological
     stability, and Kelvin-Helmholtz gives dynamical instability, in the SAME
     ideal fluid.  The topology of a vortex knot is conserved while its
     geometry is torn apart, and both statements are theorems about the same
     equations.

     A regulator is therefore not optional: viscosity, surface tension, or a
     finite core radius is required, and each one BREAKS the exact topological
     conservation that motivated the programme.  Reconnection at finite
     viscosity changes knot type.

     This is the same shape as the finite-resolution result already in the
     corpus: introducing a cutoff to make the object well-defined removes the
     exactness that made it attractive.""")
    return {"growth_rate": "sigma = k dU / 2, unbounded as k -> infinity",
            "rows": rows, "stabilising_term": None,
            "regulator_required": ["viscosity", "surface tension", "finite core"],
            "cost": "any regulator breaks exact topological conservation"}


def k3_what_killed_it():
    head("K3", "What killed it, and whether the same kill transfers")
    print("""  Kelvin's programme was abandoned for reasons worth separating, because
  only some of them transfer.

     1. THE AETHER WENT.  Michelson-Morley (1887) and then special relativity
        removed the medium the vortices were vortices IN.  This is a
        contingent, empirical kill and it is SPECIFIC to Kelvin -- a modern
        topological ontology need not posit a mechanical aether.
        -> does NOT transfer automatically.

     2. NO QUANTITATIVE SPECTRA.  The programme never produced the observed
        atomic spectral lines from knot invariants.  It had the right SHAPE
        (discrete species, discrete modes) and never delivered a number that
        matched.  In this corpus's terms: coherent, and inaccurate.
        -> TRANSFERS DIRECTLY.  It is the same cell the CPF alpha claim would
           occupy if its derivation held, and the same standard applies.

     3. STABILITY REQUIRED AN IDEALISATION THAT COULD NOT BE MAINTAINED (K2).
        -> TRANSFERS to any ontology whose stability argument runs through
           exact topological conservation.

     4. THE KNOT TABLE WAS NOT PREDICTIVE.  Which knot is which atom was
        never derivable; the assignment would have been fitted after the fact.
        -> TRANSFERS, and is the sharpest one.  It is exactly the a/R
           situation: a structure rich enough to accommodate any assignment
           makes no prediction, and the decoy test measured that as 0 bits.

  So three of four transfer, and the one that does not (the aether) is the one
  usually given as the reason.  The programme's real difficulty was that
  topological richness bought accommodation rather than prediction -- which is
  a live standard, not a historical curiosity.""")
    return {"reasons": [
        {"reason": "aether removed by Michelson-Morley/SR", "transfers": False},
        {"reason": "never produced quantitative spectra", "transfers": True},
        {"reason": "stability needed an unmaintainable idealisation", "transfers": True},
        {"reason": "knot-to-atom assignment was fitted, not derived", "transfers": True}],
        "sharpest": "topological richness bought accommodation, not prediction"}


def main():
    print(RULE)
    print("SCHWARTZ 2023 AND KELVIN 1867: TWO EXTERNAL CHECKS ON THE RIBBON ONTOLOGY")
    print(RULE)
    res = {"S1_schwartz_bound": s1_schwartz_bound(),
           "S2_self_intersection": s2_self_intersection(),
           "S3_schwartz_method": s3_schwartz_method(),
           "K1_vortex_atoms": k1_vortex_atoms(),
           "K2_kelvin_helmholtz": k2_kelvin_helmholtz(),
           "K3_what_killed_it": k3_what_killed_it()}
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print(f"""  S1  Schwartz's sqrt(3) bound is on ISOMETRIC (paper) bands.  Ours are ruled
      surfaces and stretch, so it does not strictly apply -- and every ribbon
      we used had aspect >= {res['S1_schwartz_bound']['min_aspect_used']:.0f}, {res['S1_schwartz_bound']['min_aspect_used']/SQRT3:.0f}x clear of it regardless.
  S2  our real constraint is w/R < 2, where rho -> 0 at the inner edge.  The
      limiting aspect is pi = {np.pi:.3f} against Schwartz's {SQRT3:.3f}: numerically close,
      not the same statement.
  S3  and the useful part is his METHOD.  Three years stuck on an unexamined
      assumption (parallelogram), resolved by cutting one open and LOOKING --
      trapezoid.  That is rule 10 in the literature, and better prior art for
      rules 9 and 10 than anything the corpus had cited.  They are not ours.
  K1  Kelvin 1867 is the original "matter is topology" programme and the
      corpus had never cited it.  Prior art for the ONTOLOGY, not a claim.
  K2  and Helmholtz gives topological conservation while Kelvin-Helmholtz
      gives sigma = k dU/2, unbounded as k -> 0 wavelength, in the SAME ideal
      fluid.  Any regulator that fixes the instability breaks the exact
      conservation that motivated the programme.
  K3  three of the four reasons it was abandoned transfer.  The one that does
      not is the aether -- the one usually cited.  The sharpest transferring
      reason: topological richness bought accommodation, not prediction.""")
    print(RULE)
    out = ROOT / "docs" / "kelvin_and_schwartz.json"
    out.write_text(json.dumps({
        "description": "Schwartz 2023 Moebius bound and Kelvin 1867 vortex atoms as external checks",
        "source": "code/constraint_projection/kelvin_and_schwartz.py",
        "checks": res}, indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
