#!/usr/bin/env python3
"""
The Feynman path integral run against the CPF entry and the Klein-Foam reading.

The path integral is the natural home for a "no particles, only histories at
finite resolution" ontology -- that IS Feynman's formulation, and a finite
resolution IS lattice regularisation.  So this is a fair test of the ontology
on its own ground, not an imported objection.

Six checks:

    P0  what the path integral GIVES the ontology (the positive result)
    P1  loop counting: alpha is the expansion parameter, so no tree-level
        quantity can fix it.  Where does hbar actually enter?
    P2  the derivation, redone symbolically WITHOUT substituting R
    P3  the fermion measure: Spin vs Pin structures on a non-orientable M
    P4  one-loop running from the vacuum polarisation -- recheck our own
        "sign opposite" verdict rather than reusing it
    P5  the Landau pole, and the coupling at the required resolution
    P6  UV completeness: fixed points, and finite resolution as an ipso-facto
        cutoff theory
    P7  the empirical kill: alpha is MEASURED to run

Every number is computed here.  Nothing is carried over as an assertion.
"""
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

mp.mp.dps = 50
ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78


def head(tag, title):
    print(f"\n{RULE}\n{tag}. {title}\n{RULE}")


# ---------------------------------------------------------------- constants
# CODATA 2022 / PDG, SI.
c     = mp.mpf("299792458")
hbar  = mp.mpf("1.054571817e-34")
e_ch  = mp.mpf("1.602176634e-19")
eps0  = mp.mpf("8.8541878128e-12")
m_e   = mp.mpf("9.1093837015e-31")
G_N   = mp.mpf("6.67430e-11")
ALPHA_INV_CODATA = mp.mpf("137.035999177")
ALPHA_INV_MZ     = mp.mpf("128.947")          # PDG, alpha(M_Z) effective
M_Z_over_m_e     = mp.mpf("91.1876e9") / mp.mpf("0.51099895e6")

lambda_bar_C = hbar / (m_e * c)               # reduced Compton wavelength
r_e          = e_ch**2 / (4 * mp.pi * eps0 * m_e * c**2)   # classical radius
l_Planck     = mp.sqrt(hbar * G_N / c**3)


def p0_what_it_gives():
    head("P0", "What the path integral GIVES the ontology")
    print("""  The Klein-Foam reading is not foreign to this formalism -- it is the
  formalism.  Three things transfer exactly:

    1. "No particles, only histories."  That is Feynman's own statement of
       the path integral.  A particle is not an object in the sum; it is a
       label on boundary conditions.

    2. "Finite resolution of the throat."  A path integral with a shortest
       length IS a lattice regularisation.  This is the most successful
       NON-PERTURBATIVE definition of quantum field theory we have -- lattice
       QCD computes hadron masses from it to percent accuracy.

    3. Joint-scaling invariance (K1).  A lattice theory's physics depends on
       dimensionless ratios (correlation length / spacing), never on the bare
       spacing alone.  That is precisely the invariance verified in K1.

  So the ontology is WELL-FORMED as a lattice path integral.  The checks
  below ask what such a path integral can and cannot determine.""")
    return {"ontology_is_well_formed_as_lattice_path_integral": True,
            "verdict": "the reading maps onto the formalism exactly"}


def p1_loop_counting():
    head("P1", "Loop counting: can a tree-level quantity fix alpha?")
    print("""  In the path integral the weight is exp(iS/hbar).  Expanding around a
  saddle, an L-loop term carries hbar^L relative to tree level.  For gauge
  theory alpha IS that expansion parameter: alpha counts loops.

  A classical electrostatic capacitance solves Laplace's equation.  It is
  the SADDLE POINT -- zero loops, O(hbar^0).  So the question is sharp:
  where does hbar enter the CPF derivation?\n""")

    # Symbols.  Note: no hbar yet.
    E, eps, R, a, me, cc, hb, L = sp.symbols("e epsilon_0 R a m_e c hbar L",
                                             positive=True)
    C_M   = 2 * sp.pi * eps * R / L                       # manuscript's capacitance
    E_slf = (E / 2)**2 / (2 * C_M)                        # effective charge e/2
    # Solve E_self = m_e c^2 for L, WITHOUT assuming anything about R.
    L_classical = sp.solve(sp.Eq(E_slf, me * cc**2), L)[0]
    L_classical = sp.simplify(L_classical)
    print(f"     self-energy condition, solved for L, R left free:")
    print(f"        L = {L_classical}")
    has_hbar = hb in L_classical.free_symbols
    print(f"        contains hbar?  {has_hbar}")

    print(f"\n     Now substitute the manuscript's R = hbar/(2 m_e c):")
    L_quantum = sp.simplify(L_classical.subs(R, hb / (2 * me * cc)))
    print(f"        L = {L_quantum}")
    print(f"        contains hbar?  {hb in L_quantum.free_symbols}")

    # Express in terms of alpha.
    alpha_sym = E**2 / (4 * sp.pi * eps * hb * cc)
    ratio = sp.simplify(L_quantum * alpha_sym)
    print(f"\n     L * alpha = {ratio}      ->  L = {ratio} / alpha,  i.e. alpha^-1 = L/{ratio}")

    print(f"""
  THE FINDING.  The electrostatic step is hbar-free: it fixes a RELATION
  between L, R and m_e and says nothing about alpha.  hbar enters at exactly
  one place -- the choice R = hbar/(2 m_e c).  That step is an input, not a
  consequence of the topology, and it is the ONLY carrier of hbar in the
  derivation.

  So alpha is not derived from the geometry.  It is carried in by the
  decision to measure the geometry in Compton units, and a tree-level
  quantity cannot do otherwise: in the path integral alpha is the loop
  counting parameter, and zero loops give zero information about it.""")
    return {"L_classical": str(L_classical), "classical_contains_hbar": bool(has_hbar),
            "L_after_R_substitution": str(L_quantum),
            "L_times_alpha": str(ratio),
            "hbar_enters_only_via": "R = hbar/(2 m_e c)",
            "verdict": "tree-level; alpha is carried in by the R choice, not derived"}


def p2_circularity():
    head("P2", "The derivation redone symbolically: what is actually being said")
    E, eps, R, me, cc, hb = sp.symbols("e epsilon_0 R m_e c hbar", positive=True)

    # From P1: L = 16 pi eps0 R m_e c^2 / e^2.  Solve instead for R.
    L = sp.symbols("L", positive=True)
    R_classical = sp.solve(sp.Eq(L, 16 * sp.pi * eps * R * me * cc**2 / E**2), R)[0]
    r_e_sym = E**2 / (4 * sp.pi * eps * me * cc**2)
    R_in_re = sp.simplify(R_classical / r_e_sym)
    print(f"     classical self-energy alone gives   R = ({R_in_re}) * r_e")
    print(f"        where r_e = e^2/(4 pi eps0 m_e c^2) is the CLASSICAL electron radius")

    lam_sym = hb / (me * cc)
    print(f"\n     the manuscript separately SETS       R = lambdabar_C / 2")
    print(f"     equating the two:                    L/4 * r_e = lambdabar_C / 2")
    L_solved = sp.solve(sp.Eq(R_classical, lam_sym / 2), L)[0]
    L_over = sp.simplify(L_solved / (lam_sym / r_e_sym))
    print(f"        =>  L = {L_over} * (lambdabar_C / r_e)")

    print(f"""
  And lambdabar_C / r_e is the DEFINITION of 1/alpha:
        r_e = alpha * lambdabar_C     (standard identity)""")
    lhs = r_e / lambda_bar_C
    print(f"        r_e / lambdabar_C   = {mp.nstr(lhs, 12)}")
    print(f"        alpha (CODATA)      = {mp.nstr(1/ALPHA_INV_CODATA, 12)}")
    print(f"        agreement           = {mp.nstr(abs(lhs*ALPHA_INV_CODATA - 1), 3)} relative")

    print(f"""
  So the whole derivation collapses to
        L = 2 * (lambdabar_C / r_e) = 2 / alpha,
  i.e.  alpha^-1 = L/2  -- which is the identity r_e = alpha lambdabar_C
  rewritten.  It determines L FROM alpha.  To run it the other way and get a
  number out, a/R must be supplied independently.\n""")

    # And it is: check the manuscript's stated a/R against CODATA.
    stated_exponent = mp.mpf("136.035999171")
    codata_minus_one = ALPHA_INV_CODATA - 1
    print(f"     manuscript:  a/R = 8 exp(-136.035999171)")
    print(f"        stated exponent          = {mp.nstr(stated_exponent, 12)}")
    print(f"        CODATA alpha^-1 - 1      = {mp.nstr(codata_minus_one, 12)}")
    print(f"        difference               = {mp.nstr(abs(stated_exponent - codata_minus_one), 3)}")
    print(f"""
  The exponent that fixes a/R IS the measured alpha, minus one, to 6e-9 --
  which is exactly the agreement the manuscript reports.  The input and the
  output are the same number.""")
    return {"R_from_classical_self_energy": f"({R_in_re}) * r_e",
            "L_equals": f"{L_over} * lambdabar_C / r_e = 2/alpha",
            "r_e_over_lambdabar_C": mp.nstr(lhs, 12),
            "identity_holds_to": mp.nstr(abs(lhs*ALPHA_INV_CODATA - 1), 3),
            "stated_exponent": mp.nstr(stated_exponent, 12),
            "codata_alpha_inv_minus_1": mp.nstr(codata_minus_one, 12),
            "difference": mp.nstr(abs(stated_exponent - codata_minus_one), 3),
            "verdict": "collapses to r_e = alpha*lambdabar_C; a/R carries CODATA alpha as input"}


def _gf2_rank(rows, ncols):
    """Rank of a GF(2) matrix given as a list of integer bitmasks."""
    rows = [r for r in rows]
    rank = 0
    for col in range(ncols):
        piv = None
        for i in range(rank, len(rows)):
            if (rows[i] >> col) & 1:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def p3_measure():
    head("P3", "The fermion measure: Spin vs Pin structures on M")
    print("""  Section 4 of the manuscript reads 4-pi spinor periodicity off the
  non-orientability of M.  In the path integral, "spinor" is not a reading --
  it is a choice of MEASURE for the fermionic integral, and that measure needs
  a spin structure.  On a non-orientable manifold no spin structure exists.
  What exists is a Pin structure, and there is more than one.\n""")

    # CW complex for the Klein bottle: 1 vertex, edges a,b, one 2-cell abab^-1.
    V, Eg, F = 1, 2, 1
    chi = V - Eg + F
    print(f"     CW complex: {V} vertex, {Eg} edges, {F} face   ->  chi(K) = {chi}")

    # Chain complex over GF(2).  Both edges are loops => d1 = 0.
    d1_rows = [0b00]                    # 1x2, both columns zero
    # d2: word a b a b^-1 -> exponent sums (a:2, b:0) -> zero mod 2.
    d2_rows = [0b0, 0b0]                # 2x1, zero mod 2
    rank_d1 = _gf2_rank(list(d1_rows), 2)
    rank_d2 = _gf2_rank(list(d2_rows), 1)
    dim_H1 = (2 - rank_d1) - rank_d2    # ker d1 - im d2, over GF(2)
    order_H1 = 2 ** dim_H1
    print(f"     over GF(2):  rank d1 = {rank_d1}, rank d2 = {rank_d2}")
    print(f"                  dim H_1(K; Z/2) = {dim_H1}   ->  |H^1(K; Z/2)| = {order_H1}")

    # Wu: on a closed surface w2 = w1^2, and <w2,[M]> = chi mod 2.
    w2_eval = chi % 2
    print(f"\n     Wu formula on a closed surface:  w2 = w1^2,  <w2,[K]> = chi mod 2 = {w2_eval}")
    spin_exists = False                       # w1 != 0 by Axiom II
    pin_plus  = (w2_eval == 0)                # needs w2 = 0
    pin_minus = ((w2_eval + w2_eval) % 2 == 0)  # needs w2 + w1^2 = 2 w1^2 = 0
    print(f"        Spin  (needs w1 = 0):            {spin_exists}   <- Axiom II SETS w1 != 0")
    print(f"        Pin+  (needs w2 = 0):            {pin_plus}")
    print(f"        Pin-  (needs w2 + w1^2 = 0):     {pin_minus}")

    n_spin = 0
    n_pin_each = order_H1
    total = (int(pin_plus) + int(pin_minus)) * n_pin_each
    print(f"""
     count of structures (a torsor over H^1(M; Z/2) when non-empty):
        Spin structures  = {n_spin}
        Pin+ structures  = {n_pin_each}
        Pin- structures  = {n_pin_each}
        total fermionic measures to choose from = {total}

  THE FINDING.  The manuscript's Axiom II sets w1(M) != 0.  That is precisely
  the condition under which NO spin structure exists.  A fermionic path
  integral on M is therefore not a spin theory; it is a Pin theory, and
  writing it down requires choosing Pin+ or Pin- and then one of {n_pin_each}
  structures -- {total} discrete options, log2({total}) = {mp.nstr(mp.log(total)/mp.log(2),3)} bits.

  The manuscript specifies none of them.  So "zero free parameters" fails in
  the MEASURE, before any coupling is computed, and it fails on the same
  property (w1 != 0) that the framework relies on for its spinor claim.

  Note what this is NOT.  It is not "fermions are impossible on M" -- Pin
  structures exist and are perfectly good.  It is that the discrete data is
  real, unspecified, and physical: Pin+ and Pin- give different theories.""")
    return {"chi": chi, "dim_H1_Z2": dim_H1, "order_H1_Z2": order_H1,
            "w2_evaluated": w2_eval, "spin_structures": n_spin,
            "pin_plus_exists": bool(pin_plus), "pin_minus_exists": bool(pin_minus),
            "pin_structures_each": n_pin_each, "total_fermionic_measures": total,
            "bits_unspecified": mp.nstr(mp.log(total)/mp.log(2), 3),
            "verdict": "Axiom II's w1 != 0 forbids Spin; 8 Pin measures unspecified"}


def p4_running():
    head("P4", "One-loop running from the vacuum polarisation (rechecking our own verdict)")
    print("""  Derived here rather than quoted.  The one-loop photon self-energy from
  the path integral, one Dirac fermion:

        Pi(q^2) ~ (alpha/3pi) ln(Lambda^2/m^2)   ->   mu d(alpha)/d(mu) = 2 alpha^2 / (3 pi)

  so, differentiating alpha^-1,\n""")
    beta_alpha_inv = -2 / (3 * mp.pi)
    print(f"        d(alpha^-1)/d ln mu  =  -2/(3 pi)  =  {mp.nstr(beta_alpha_inv, 8)}")
    print(f"        alpha^-1 DECREASES with mu  ->  coupling grows at short distance")
    print(f"        this is SCREENING, the sign every U(1) gauge theory has.\n")

    # CPF read as running.  mu ~ 1/a, so ln a = -ln mu.
    a_s, R_s, mu = sp.symbols("a R mu", positive=True)
    cpf = sp.Rational(1, 2) * (sp.log(8 * R_s / a_s) + 1)
    cpf_mu = cpf.subs(a_s, 1 / mu)
    slope = sp.simplify(sp.diff(cpf_mu, sp.log(mu)) if False else sp.diff(cpf_mu, mu) * mu)
    print(f"     CPF: alpha^-1 = (1/2)(ln(8R/a)+1).  Set the RG scale mu ~ 1/a:")
    print(f"        d(alpha^-1)/d ln mu  =  {slope}")
    cpf_slope = mp.mpf(float(slope))
    print(f"                             =  {mp.nstr(cpf_slope, 8)}")

    print(f"""
     QED      {mp.nstr(beta_alpha_inv, 8)}      alpha^-1 falls with energy   (screening)
     CPF      {mp.nstr(cpf_slope, 8)}      alpha^-1 RISES with energy   (anti-screening)

     magnitude ratio |CPF/QED| = {mp.nstr(abs(cpf_slope/beta_alpha_inv), 8)}  =  3 pi/4 = {mp.nstr(3*mp.pi/4, 8)}
     signs                     = OPPOSITE

  VERDICT ON OUR OWN EARLIER CALL.  The 2026-08-30 gap diagnosis recorded
  "coefficient off by 3pi/4, sign opposite".  Re-derived here from the
  vacuum polarisation rather than reused: BOTH HOLD.  The sign statement is
  convention-sensitive, so it was worth re-deriving -- differentiating with
  respect to the RG scale mu (not with respect to R/a) is what makes it
  well-posed, and in that variable the signs are genuinely opposite.

  Physically: read as running, the manuscript's relation is ASYMPTOTICALLY
  FREE.  An abelian U(1) gauge theory cannot be.""")
    return {"qed_d_alphainv_dlnmu": mp.nstr(beta_alpha_inv, 8),
            "cpf_d_alphainv_dlnmu": mp.nstr(cpf_slope, 8),
            "magnitude_ratio": mp.nstr(abs(cpf_slope/beta_alpha_inv), 8),
            "equals_3pi_over_4": mp.nstr(3*mp.pi/4, 8),
            "signs": "opposite",
            "earlier_verdict_rederived": True,
            "verdict": "our 2026-08-30 call CONFIRMED by independent derivation"}


def p5_landau():
    head("P5", "The Landau pole, and the coupling at the required resolution")
    a_over_R = mp.mpf("2.039e-118")
    # mu ~ hbar c / a, and R = lambdabar_C / 2, so mu_a / (m_e c^2) = 2/(a/R).
    mu_a_over_me = 2 / a_over_R
    ln_mu_a = mp.log(mu_a_over_me)
    ln_landau = 3 * mp.pi * ALPHA_INV_CODATA / 2
    print(f"     required cutoff       a/R = {mp.nstr(a_over_R, 6)}")
    print(f"     as an energy      mu_a/m_e c^2 = {mp.nstr(mu_a_over_me, 6)},  ln = {mp.nstr(ln_mu_a, 7)}")
    print(f"     QED Landau pole   ln(Lambda/m_e c^2) = 3 pi/(2 alpha) = {mp.nstr(ln_landau, 7)}")
    inside = ln_mu_a < ln_landau
    print(f"\n     is the required cutoff BELOW the Landau pole?   {inside}")
    print(f"        margin in ln = {mp.nstr(ln_landau - ln_mu_a, 7)}  ({mp.nstr((ln_landau-ln_mu_a)/mp.log(10),6)} decades)")

    alpha_inv_at_a = ALPHA_INV_CODATA - (2 / (3 * mp.pi)) * ln_mu_a
    print(f"""
     So QED remains perturbatively defined there, and it makes a PREDICTION
     for the coupling at that scale that can be compared directly:

        QED, run to mu_a:   alpha^-1 = {mp.nstr(alpha_inv_at_a, 8)}
        CPF asserts there:  alpha^-1 = {mp.nstr(ALPHA_INV_CODATA, 8)}
        disagreement                  = {mp.nstr(ALPHA_INV_CODATA/alpha_inv_at_a, 6)}x

  This is a like-for-like comparison at ONE scale -- no normalisation freedom
  left in it.  Note the direction: the framework is not saved by the cutoff
  being unreachable.  It is reachable in the RG sense, and the two answers
  disagree by {mp.nstr(ALPHA_INV_CODATA/alpha_inv_at_a, 4)}x.""")
    return {"a_over_R": mp.nstr(a_over_R, 6),
            "ln_mu_a_over_me": mp.nstr(ln_mu_a, 7),
            "ln_landau_pole": mp.nstr(ln_landau, 7),
            "cutoff_below_landau_pole": bool(inside),
            "qed_alpha_inv_at_cutoff": mp.nstr(alpha_inv_at_a, 8),
            "cpf_alpha_inv": mp.nstr(ALPHA_INV_CODATA, 8),
            "disagreement": mp.nstr(ALPHA_INV_CODATA/alpha_inv_at_a, 6),
            "verdict": "cutoff is inside the perturbative region; the two disagree 1.7x there"}


def p6_uv_completeness():
    head("P6", "UV completeness: fixed points, and what a finite resolution implies")
    al = sp.symbols("alpha", real=True)          # unconstrained: let 0 be findable
    beta = 2 * al**2 / (3 * sp.pi)
    fixed = sp.solve(sp.Eq(beta, 0), al)
    nontrivial = [f for f in fixed if f != 0]
    # Sample the sign rather than asking solve() for an inequality's truth value.
    probes = [sp.Rational(-1, 10), sp.Rational(-1, 137), sp.Rational(1, 137),
              sp.Rational(1, 10), sp.Integer(1)]
    signs = [sp.sign(beta.subs(al, x)) for x in probes]
    all_positive = all(sg == 1 for sg in signs)
    print(f"     one-loop QED beta function:  beta(alpha) = {beta}")
    print(f"     ALL solutions of beta = 0:   {fixed}")
    print(f"     solutions with alpha != 0:   {nontrivial}")
    print(f"     sign of beta at alpha in {[str(x) for x in probes]}:")
    print(f"                                  {[int(sg) for sg in signs]}  -> all positive: {all_positive}")
    print(f"        The root set is {fixed} -- the free theory and nothing else.")
    print(f"        No UV fixed point at alpha != 0, and beta > 0 for every alpha != 0,")
    print(f"        so the coupling runs UP without bound: no asymptotic freedom and")
    print(f"        no asymptotic safety at this order.")
    print(f"""
     And the structural point, which is pure path-integral bookkeeping:

        "UV complete"     = the continuum limit of the measure EXISTS
        "finite resolution a" = the continuum limit is never taken

     These are mutually exclusive by definition.  A path integral with a
     shortest length is an EFFECTIVE theory with a cutoff.  That is a
     perfectly respectable object -- it is what lattice QCD is -- but it is
     the opposite of UV complete.

  THE FINDING, and note where it lands.  The manuscript's abstract claims
  "UV and IR complete".  The Klein-Foam reading says there is a finite
  resolution.  Both cannot hold.  The ontology is the half that survives:
  a finite-resolution path integral is well-defined and useful.  It is the
  completeness claim that the ontology itself rules out.""")
    return {"beta": str(beta), "fixed_points": [str(f) for f in fixed],
            "nontrivial_fixed_points": [str(f) for f in nontrivial],
            "nontrivial_uv_fixed_point": bool(nontrivial),
            "uv_complete_and_finite_resolution_compatible": False,
            "verdict": "no UV fixed point; and finite resolution EXCLUDES UV completeness"}


def p7_measured_running():
    head("P7", "The empirical kill: alpha is MEASURED to run")
    print("""  The CPF relation returns ONE number from fixed topology.  But alpha is
  not one number -- its scale dependence is measured directly.\n""")
    print(f"     alpha^-1 at low energy (CODATA)  = {mp.nstr(ALPHA_INV_CODATA, 9)}")
    print(f"     alpha^-1 at M_Z        (PDG)     = {mp.nstr(ALPHA_INV_MZ, 9)}")
    print(f"     measured change                  = {mp.nstr(ALPHA_INV_CODATA - ALPHA_INV_MZ, 6)}")

    # What a/R would be needed at M_Z, with R fixed by m_e?
    # alpha^-1 = (1/2)(ln(8R/a)+1)  ->  ln(8R/a) = 2 alpha^-1 - 1
    ln_low = 2 * ALPHA_INV_CODATA - 1
    ln_mz  = 2 * ALPHA_INV_MZ - 1
    factor = mp.e ** (ln_low - ln_mz)
    print(f"""
     Inverting the CPF relation for the resolution it would need at each scale:
        at low energy:  ln(8R/a) = {mp.nstr(ln_low, 9)}
        at M_Z:         ln(8R/a) = {mp.nstr(ln_mz, 9)}
        required change in a     = {mp.nstr(factor, 6)}x   ({mp.nstr(mp.log(factor)/mp.log(10), 5)} decades)

  THE FINDING.  To track the measured running, the "finite resolution of the
  throat" would have to be {mp.nstr(factor, 4)} times COARSER when probed at M_Z than at
  low energy.  A resolution that changes by 7 decades with the probe is not a
  fundamental floor -- it is a restatement of the running, with the running
  put in by hand.

  This kill is independent of every other one here.  It does not care about
  the factor of 2, the value of a/R, the Planck floor, or the sign of the
  beta function.  It only needs alpha to depend on scale, which is measured.""")
    return {"alpha_inv_low": mp.nstr(ALPHA_INV_CODATA, 9),
            "alpha_inv_MZ": mp.nstr(ALPHA_INV_MZ, 9),
            "required_resolution_change": mp.nstr(factor, 6),
            "decades": mp.nstr(mp.log(factor)/mp.log(10), 5),
            "verdict": "a fixed-topology single number cannot track a measured running"}


def main():
    print(RULE)
    print("THE FEYNMAN PATH INTEGRAL RUN AGAINST CPF AND THE KLEIN-FOAM READING")
    print(RULE)
    res = {
        "P0_what_it_gives":    p0_what_it_gives(),
        "P1_loop_counting":    p1_loop_counting(),
        "P2_circularity":      p2_circularity(),
        "P3_measure":          p3_measure(),
        "P4_running":          p4_running(),
        "P5_landau":           p5_landau(),
        "P6_uv_completeness":  p6_uv_completeness(),
        "P7_measured_running": p7_measured_running(),
    }
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print("""  The ontology passes its own test (P0): "no particles, only histories at
  finite resolution" IS the path integral, and a finite resolution IS lattice
  regularisation.  Nothing about the reading is ill-formed.

  What the path integral then says about the CPF entry:

    P1  the electrostatic step is hbar-free -- tree level, zero loops.  hbar
        enters at exactly one point, the choice R = hbar/(2 m_e c).  alpha is
        the loop-counting parameter, so no tree-level quantity can fix it.
    P2  the derivation collapses to r_e = alpha * lambdabar_C, an identity;
        and a/R is defined by an exponent equal to CODATA alpha^-1 minus one,
        to 6e-9.  Input and output are the same number.
    P3  Axiom II sets w1 != 0, which is exactly the condition under which NO
        spin structure exists.  8 Pin measures, none specified.
    P4  our own "3pi/4, sign opposite" call, re-derived from the vacuum
        polarisation instead of reused: CONFIRMED.
    P5  the required cutoff sits INSIDE the perturbative region (Landau pole
        is 162 decades further out), so QED makes a competing prediction
        there: 79.4 vs 137.0, disagreeing 1.7x at one common scale.
    P6  no UV fixed point; and "finite resolution" excludes "UV complete" by
        definition.  The ontology is the half that survives.
    P7  alpha is MEASURED to run.  A single number from fixed topology would
        need the throat resolution to change by 7 decades between low energy
        and M_Z.

  The path integral is the ontology's home ground, and on that ground the
  ontology is fine and the alpha derivation is not.""")
    print(RULE)
    out = ROOT / "docs" / "feynman_path_integral.json"
    out.write_text(json.dumps({
        "description": "The Feynman path integral run against CPF and the Klein-Foam reading",
        "source": "code/constraint_projection/feynman_path_integral.py",
        "checks": res}, indent=2) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
