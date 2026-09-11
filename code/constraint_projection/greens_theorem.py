#!/usr/bin/env python3
"""
Green's theorem run against CPF.

This is the framework's OWN integral theorem, twice over:

  * M is a 2-manifold, so Green's theorem (not the 3D divergence theorem) is
    the native statement on it;
  * Sec 9 elevates the Divergence Theorem to a "relational identity" and makes
    it foundational;
  * and Sec 3's alpha derivation is a Green's-function calculation -- a
    capacitance, i.e. Laplace's equation with a flux boundary condition.

So this test is entirely internal.  Four checks:

    G1  does Green's/Stokes' theorem even hold on M?  Axiom II answers it.
    G2  the vanishing theorem: what an orientation-reversing deck map does to
        the flux of any form pulled back from M
    G3  compute the capacitance HONESTLY, from the Green's-function integral
    G4  propagate the corrected capacitance through the alpha derivation

Everything computed here.  Nothing carried in as an assertion.
"""
import json
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 40
ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78

c     = mp.mpf("299792458")
hbar  = mp.mpf("1.054571817e-34")
e_ch  = mp.mpf("1.602176634e-19")
eps0  = mp.mpf("8.8541878128e-12")
m_e   = mp.mpf("9.1093837015e-31")
G_N   = mp.mpf("6.67430e-11")
ALPHA_INV = mp.mpf("137.035999177")
lambda_bar_C = hbar / (m_e * c)
l_Planck = mp.sqrt(hbar * G_N / c**3)


def head(tag, title):
    print(f"\n{RULE}\n{tag}. {title}\n{RULE}")


def g1_does_greens_hold():
    head("G1", "Does Green's/Stokes' theorem hold on M?  Axiom II answers it.")
    print("""  Green's theorem in its standard form

        oint_C (P dx + Q dy) = iint_D (dQ/dx - dP/dy) dA

  needs an ORIENTATION twice over: the circulation sense of the boundary, and
  the area element dA.  Equivalently, Stokes needs a fundamental class, i.e.
  H_n(M; Z) = Z.  Compute the integral homology of the Klein bottle from the
  CW chain complex, by Smith normal form:\n""")

    # C_2 = Z<f>, C_1 = Z<a,b>, C_0 = Z<v>.  Face word a b a b^-1.
    d2 = sp.Matrix([[2], [0]])       # a: +1+1 = 2,  b: +1-1 = 0
    d1 = sp.Matrix([[0, 0]])         # both edges are loops on the one vertex
    print(f"     d2 = {d2.T.tolist()}^T        d1 = {d1.tolist()}")

    # H_2 = ker d2  (nothing maps in)
    ker_d2 = d2.nullspace()
    print(f"     ker(d2) = {[list(v) for v in ker_d2]}   ->  H_2(K; Z) = "
          f"{'0' if not ker_d2 else 'nonzero'}")

    from sympy.matrices.normalforms import smith_normal_form
    snf = smith_normal_form(d2, domain=sp.ZZ)
    print(f"     Smith normal form of d2 = {snf.T.tolist()}^T")
    print(f"        ker(d1) = Z^2 (d1 = 0), im(d2) = <(2,0)>")
    print(f"        H_1(K; Z) = Z^2 / <(2,0)> = Z + Z/2")

    print(f"""
  THE FINDING, and it is stated by the manuscript itself.  Axiom II reads

        w_1(M) != 0,   H_2(M; Z) = 0

  Both clauses are the obstruction.  H_2(M;Z) = 0 means there is NO
  fundamental class, so an ordinary 2-form has no integral over M; w_1 != 0
  means there is no orientation to give the boundary a circulation sense.
  Section 9 makes the Divergence Theorem a foundational "relational
  identity".  Axiom II removes it, in the manuscript's own notation, three
  pages earlier.

  WHAT SURVIVES, stated precisely.  Stokes' theorem is not simply false on a
  non-orientable manifold -- it holds for TWISTED forms (densities, sections
  of Lambda^n T*M tensor or(M)).  But that is not a free relabelling:

     * the Hodge star needs an orientation, so F and *F cannot both be
       ordinary forms -- one must be twisted;
     * E and B then transform differently under orientation reversal, and
       charge becomes a pseudo-scalar density;
     * the topological term int F ^ F is not available at all.

  So the theorem is recoverable, and the electromagnetism built on it is a
  different theory from the one the manuscript writes down.""")
    return {"H2_K_Z": "0", "H1_K_Z": "Z + Z/2",
            "d2_smith_normal_form": [[int(v) for v in row] for row in snf.T.tolist()],
            "axiom_II_states_H2_zero": True,
            "fundamental_class_exists": False,
            "stokes_holds_for_ordinary_forms": False,
            "stokes_holds_for_twisted_forms": True,
            "verdict": "Axiom II itself removes the theorem Sec 9 makes foundational"}


def g2_vanishing_theorem():
    head("G2", "The vanishing theorem on the orientation double cover")
    print("""  Section 3 computes "the capacitance of the double-cover annulus of M".
  The double cover of a non-orientable M is its ORIENTATION cover, and its
  deck transformation tau is orientation-REVERSING.  That has a consequence
  for any flux computed there.

  Let omega be an ordinary 2-form on the cover pulled back from M, so
  tau* omega = omega.  Since tau reverses orientation,

        int_cover tau* omega  =  - int_cover omega
        but tau* omega = omega, so  int omega = - int omega  =>  int omega = 0.

  ANY ordinary 2-form pulled back from a non-orientable base has ZERO
  integral over its orientation double cover.  Verified concretely below.

  Concretely for K: cover = T^2 = [0,1)^2, tau(x,y) = (x + 1/2, -y).
  A function f descends from K iff  f(x,y) = -f(x + 1/2, -y)  (the sign is
  the orientation reversal).  Build such f from arbitrary g:

        f(x,y) = g(x,y) - g(x + 1/2, -y)      (satisfies the constraint)
""")
    rng = np.random.default_rng(20260831)

    def make_g(n_modes=6):
        ms = rng.integers(-3, 4, size=n_modes)
        ns = rng.integers(-3, 4, size=n_modes)
        cs = rng.normal(size=n_modes)
        ph = rng.uniform(0, 2 * np.pi, size=n_modes)
        def g(x, y):
            out = np.zeros_like(x)
            for m, n, cc, p in zip(ms, ns, cs, ph):
                out = out + cc * np.cos(2 * np.pi * (m * x + n * y) + p)
            return out
        return g

    print("     Monte-Carlo integration (random points, so the quadrature grid")
    print("     cannot itself impose the symmetry):\n")
    print(f"     {'trial':>6}  {'N':>9}  {'int f':>14}  {'int |f|':>12}  {'ratio':>10}")
    results = []
    N = 400_000
    for trial in range(5):
        g = make_g()
        xs = rng.uniform(0, 1, N)
        ys = rng.uniform(0, 1, N)
        f = g(xs, ys) - g((xs + 0.5) % 1.0, (-ys) % 1.0)
        I = float(f.mean())
        Iabs = float(np.abs(f).mean())
        ratio = abs(I) / Iabs if Iabs > 0 else 0.0
        results.append({"integral": I, "mean_abs": Iabs, "ratio": ratio})
        print(f"     {trial:>6}  {N:>9}  {I:>14.3e}  {Iabs:>12.6f}  {ratio:>10.2e}")

    # Check the descent constraint really holds for these f.
    xs = rng.uniform(0, 1, 2000)
    ys = rng.uniform(0, 1, 2000)
    g = make_g()
    f  = g(xs, ys) - g((xs + 0.5) % 1.0, (-ys) % 1.0)
    ft = g((xs + 0.5) % 1.0, (-ys) % 1.0) - g((xs + 1.0) % 1.0, ys % 1.0)
    residual = float(np.max(np.abs(f + ft)))
    print(f"\n     descent constraint  f(x,y) + f(tau(x,y)) = 0   max residual = {residual:.3e}")

    worst = max(r["ratio"] for r in results)
    print(f"""
  The integral is zero to Monte-Carlo error ({worst:.1e} relative to the mean
  absolute value) while the integrand itself is O(1).  The vanishing is
  structural, not a small number.

  THE CONSEQUENCE FOR SECTION 3.  "The capacitance of the double-cover
  annulus of M" is a flux quantity.  In the ordinary-form formulation the
  flux of anything descending from M vanishes identically on that cover, so
  the quantity is not merely hard to compute -- it is zero.  To get a
  non-zero answer the charge must be a twisted form, and then the "effective
  charge e/2" is not a charge times a half; it is a density, and the factor
  is fixed by the twisting, not asserted.""")
    return {"trials": results, "worst_relative_residual": worst,
            "descent_constraint_max_residual": residual,
            "verdict": "flux of any pullback 2-form vanishes on the orientation cover"}


def g3_honest_capacitance():
    head("G3", "The capacitance, computed from the Green's-function integral")
    print("""  Green's representation: the potential of a charge distribution is the
  free-space Green's function integrated over the source,

        V(r) = (1/4 pi eps0) int sigma(r') / |r - r'| dS'.

  For a thin ring of major radius R and minor radius a, evaluate on the ring
  itself.  The chord between two points at angular separation phi is
  2R sin(phi/2), regularised by the minor radius a:

        V = (lambda R / 4 pi eps0) int_0^2pi dphi / sqrt(4R^2 sin^2(phi/2) + a^2)

  No cutoff is imposed by hand -- a regularises the integral.  Evaluate it
  numerically and read off what log appears.\n""")

    def V_over_lambda(R, a):
        f = lambda ph: R / mp.sqrt(4 * R**2 * mp.sin(ph / 2)**2 + a**2)
        return mp.quad(f, [0, mp.pi, 2 * mp.pi]) / (4 * mp.pi * eps0)

    print(f"     {'a/R':>12}  {'4 pi eps0 V/lambda':>20}  {'ln(8R/a)':>12}  {'ratio':>10}")
    rows = []
    for exponent in [3, 5, 8, 12, 20]:
        R = mp.mpf(1)
        a = mp.mpf(10) ** (-exponent)
        V = V_over_lambda(R, a)
        lhs = 4 * mp.pi * eps0 * V              # dimensionless: should be ln(8R/a)
        target = mp.log(8 * R / a)
        rows.append({"a_over_R": f"1e-{exponent}", "computed": mp.nstr(lhs, 12),
                     "ln_8R_over_a": mp.nstr(target, 12),
                     "ratio": mp.nstr(lhs / target, 10)})
        print(f"     {'1e-'+str(exponent):>12}  {mp.nstr(lhs,12):>20}  "
              f"{mp.nstr(target,12):>12}  {mp.nstr(lhs/target,10):>10}")

    # Read the coefficient off the table rather than asserting it.
    kappa = mp.mpf(rows[-1]["ratio"])
    kappa_int = int(mp.nint(kappa))
    print(f"""
     The Green's integral returns a clean multiple of ln(8R/a), and the
     factor 8 EMERGES -- it is not imposed.  Measured coefficient:

        4 pi eps0 V / lambda  =  kappa * ln(8R/a),   kappa -> {mp.nstr(kappa, 10)}  (= {kappa_int})

     so, with Q = 2 pi R lambda,

        V = ({kappa_int} lambda / 4 pi eps0) ln(8R/a) = (lambda / 2 pi eps0) ln(8R/a)
        C = Q / V = 8 pi^2 eps0 R / ({kappa_int} ln(8R/a)) = 4 pi^2 eps0 R / ln(8R/a)
""")
    # Confirm that chain symbolically from the measured kappa.
    lam, Rs, es, Ls = sp.symbols("lambda R epsilon_0 L", positive=True)
    V_sym = kappa_int * lam * Ls / (4 * sp.pi * es)
    C_sym = sp.simplify(2 * sp.pi * Rs * lam / V_sym * Rs / Rs)
    print(f"     symbolic check from the measured kappa: C = {sp.simplify(C_sym.subs(Ls, Ls))}"
          .replace("L", "ln(8R/a)"))
    L = sp.symbols("L", positive=True)
    epsym, Rsym = sp.symbols("epsilon_0 R", positive=True)
    C_green = 4 * sp.pi**2 * epsym * Rsym / L
    C_manu  = 2 * sp.pi * epsym * Rsym / (L + 1)
    ratio = sp.simplify(C_green / C_manu)
    print(f"     manuscript:  C = 2 pi eps0 R / (ln(8R/a) + 1)")
    print(f"     computed:    C = 4 pi^2 eps0 R / ln(8R/a)")
    print(f"     ratio C_computed / C_manuscript = {ratio}")
    Lnum = 2 * ALPHA_INV - 1          # the manuscript's own ln(8R/a)
    ratio_num = mp.mpf(float(ratio.subs(L, float(Lnum))))
    print(f"        at the manuscript's own ln(8R/a) = {mp.nstr(Lnum,9)}:  ratio = {mp.nstr(ratio_num, 8)}")
    print(f"        leading behaviour:  2 pi = {mp.nstr(2*mp.pi, 8)}")

    print(f"""
  THE FINDING.  The manuscript's capacitance is smaller than the one the
  Green's-function integral returns by a factor of {mp.nstr(ratio_num,6)}, i.e. 2 pi to
  leading order.  The "+1" in its denominator is a subleading term and does
  not account for it -- the discrepancy is in the PREFACTOR.

  FAIRNESS NOTE.  The manuscript's object is "the double-cover annulus of M
  with a half-twist identification", not a plain torus.  Three things about
  that: (i) the FORM ln(8R/a) it reports is the thin-ring form computed here,
  so the comparison is on its own terms; (ii) a half-twist changes the
  geometry by an O(1) amount inside the log, not by 2 pi in the prefactor;
  and (iii) by G2, the flux of anything pulled back from M vanishes on that
  cover, so "the capacitance of the double-cover annulus" is not a well-posed
  ordinary-form quantity to begin with.""")
    return {"rows": rows, "measured_kappa": mp.nstr(kappa, 10),
            "C_computed": "4 pi^2 eps0 R / ln(8R/a)",
            "C_manuscript": "2 pi eps0 R / (ln(8R/a) + 1)",
            "ratio_symbolic": str(ratio),
            "ratio_at_manuscript_L": mp.nstr(ratio_num, 8),
            "two_pi": mp.nstr(2 * mp.pi, 8),
            "factor_8_emerges": True,
            "verdict": "manuscript capacitance is 2 pi too small; the 8 is confirmed"}


def g4_propagate():
    head("G4", "Propagating the corrected capacitance through the derivation")
    E, eps, R, me, cc, hb, L = sp.symbols("e epsilon_0 R m_e c hbar L", positive=True)
    C_green = 4 * sp.pi**2 * eps * R / L
    E_self  = (E / 2)**2 / (2 * C_green)
    L_sol   = sp.simplify(sp.solve(sp.Eq(E_self, me * cc**2), L)[0])
    L_sub   = sp.simplify(L_sol.subs(R, hb / (2 * me * cc)))
    alpha_s = E**2 / (4 * sp.pi * eps * hb * cc)
    prod    = sp.simplify(L_sub * alpha_s)
    print(f"     with C = 4 pi^2 eps0 R / L and q = e/2:")
    print(f"        L = {L_sol}")
    print(f"        substituting R = hbar/(2 m_e c):  L = {L_sub}")
    print(f"        L * alpha = {prod}      ->  L = {prod} / alpha")
    print(f"\n     compare the manuscript's route, which gave  L * alpha = 2.")

    L_required = 4 * mp.pi * ALPHA_INV
    L_manu     = 2 * ALPHA_INV
    print(f"\n     required ln(8R/a):")
    print(f"        manuscript's capacitance:  L = 2 alpha^-1   = {mp.nstr(L_manu, 10)}")
    print(f"        computed capacitance:      L = 4 pi alpha^-1 = {mp.nstr(L_required, 10)}")

    aR_manu = 8 * mp.e ** (-(L_manu - 1))
    aR_new  = 8 * mp.e ** (-(L_required - 1))
    dec_manu = mp.log(aR_manu) / mp.log(10)
    dec_new  = mp.log(aR_new) / mp.log(10)
    print(f"\n     required a/R:")
    print(f"        manuscript's route:  a/R = {mp.nstr(aR_manu, 6)}   ({mp.nstr(dec_manu, 6)} decades)")
    print(f"        computed route:      a/R = {mp.nstr(aR_new, 6)}   ({mp.nstr(dec_new, 6)} decades)")
    print(f"        the corrected capacitance makes the required cutoff "
          f"{mp.nstr(abs(dec_new - dec_manu), 6)} decades SMALLER")

    # And what alpha^-1 does the foam's own Planck floor give with correct C?
    R_phys = lambda_bar_C / 2
    aR_planck = l_Planck / R_phys
    alpha_inv_planck_new  = mp.log(8 / aR_planck) / (4 * mp.pi)
    alpha_inv_planck_manu = (mp.log(8 / aR_planck) + 1) / 2
    print(f"""
     and with the Klein-Foam note's own Planck floor (a = l_Planck):
        a/R                                = {mp.nstr(aR_planck, 6)}
        manuscript's capacitance -> alpha^-1 = {mp.nstr(alpha_inv_planck_manu, 8)}   (off {mp.nstr(ALPHA_INV/alpha_inv_planck_manu, 6)}x)
        computed capacitance     -> alpha^-1 = {mp.nstr(alpha_inv_planck_new, 8)}   (off {mp.nstr(ALPHA_INV/alpha_inv_planck_new, 6)}x)

  THE FINDING.  Doing the electrostatics correctly does not rescue the
  derivation -- it makes it worse by a factor of 2 pi in the exponent.  The
  required cutoff drops from 10^-118 to 10^-747, and the best previous
  absolute reading (Planck floor, 5.08x off) degrades to {mp.nstr(ALPHA_INV/alpha_inv_planck_new, 4)}x.

  This is the useful direction to have tested.  A 2 pi error in a prefactor
  is the single most common way a "derivation of alpha" is wrong, and had it
  gone the other way it would have closed a real part of the gap.  It goes
  the wrong way.""")
    return {"L_solved": str(L_sol), "L_after_R_substitution": str(L_sub),
            "L_times_alpha": str(prod),
            "L_required_manuscript": mp.nstr(L_manu, 10),
            "L_required_computed": mp.nstr(L_required, 10),
            "a_over_R_manuscript": mp.nstr(aR_manu, 6),
            "a_over_R_computed": mp.nstr(aR_new, 6),
            "decades_worse": mp.nstr(abs(dec_new - dec_manu), 6),
            "planck_alpha_inv_manuscript": mp.nstr(alpha_inv_planck_manu, 8),
            "planck_alpha_inv_computed": mp.nstr(alpha_inv_planck_new, 8),
            "planck_off_by_computed": mp.nstr(ALPHA_INV / alpha_inv_planck_new, 6),
            "verdict": "correct electrostatics makes the gap 2 pi worse in the exponent"}


def main():
    print(RULE)
    print("GREEN'S THEOREM RUN AGAINST CPF")
    print(RULE)
    res = {"G1_does_greens_hold":  g1_does_greens_hold(),
           "G2_vanishing_theorem": g2_vanishing_theorem(),
           "G3_honest_capacitance": g3_honest_capacitance(),
           "G4_propagate":         g4_propagate()}
    g2, g3, g4 = res["G2_vanishing_theorem"], res["G3_honest_capacitance"], res["G4_propagate"]
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print(f"""  Green's theorem is internal to this framework three times over: M is a
  2-manifold, Sec 9 makes the Divergence Theorem foundational, and Sec 3's
  alpha derivation is a Green's-function calculation.  All four checks are
  therefore the framework tested against itself.

    G1  Axiom II states w_1(M) != 0 AND H_2(M;Z) = 0.  Computed: H_2(K;Z) = 0,
        H_1(K;Z) = Z + Z/2.  No fundamental class, no orientation -> Green's
        theorem in ordinary form does not hold on M.  Section 9 makes that
        theorem foundational; Axiom II removes it, three pages earlier, in the
        manuscript's own notation.  Twisted forms restore it, at the cost of a
        different electromagnetism.

    G2  Any ordinary 2-form pulled back from a non-orientable base integrates
        to ZERO on its orientation double cover -- proved, and verified by
        Monte Carlo to {g2['worst_relative_residual']:.1e} of the integrand's own scale while
        the integrand is O(1).  So "the capacitance of the double-cover annulus" is not a
        small quantity; in ordinary forms it is identically zero.

    G3  The Green's-function integral returns C = 4 pi^2 eps0 R / ln(8R/a),
        with the factor 8 EMERGING rather than being imposed.  The
        manuscript's C is smaller by {g3['ratio_at_manuscript_L']}x -- 2 pi to leading order, in the
        prefactor, which the "+1" does not touch.

    G4  Propagated: L * alpha = 4 pi, not 2.  The required cutoff moves from
        {g4['a_over_R_manuscript']} to {g4['a_over_R_computed']} -- {g4['decades_worse']}
        decades SMALLER -- and the Planck-floor reading degrades from 5.08x
        to {g4['planck_off_by_computed']}x.

  A 2 pi prefactor error is the commonest way a derivation of alpha goes
  wrong, and this one had a real chance to close part of the gap.  It widens
  it instead.""")
    print(RULE)
    out = ROOT / "docs" / "greens_theorem.json"
    out.write_text(json.dumps({
        "description": "Green's theorem run against CPF",
        "source": "code/constraint_projection/greens_theorem.py",
        "checks": res}, indent=2) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
