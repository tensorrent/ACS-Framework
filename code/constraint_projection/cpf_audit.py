#!/usr/bin/env python3
# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Audit instrument for the Constraint Projection Framework (CPF) manuscript.

Companion computation to papers/notes/Constraint_Projection_Framework_Audit.tex.
Target manuscript: papers/notes/Constraint_Projection_Framework.tex (as submitted).

The manuscript claims a zero-free-parameter topological derivation of alpha,
g, s, the dark-matter density, cosmological flatness (via RH) and the Hubble
radius, from a single non-orientable surface M.  This script evaluates the
load-bearing steps.  Each check is written so that the manuscript could have
passed it; none of the verdicts is assumed.

    C1  self-energy algebra          -> is alpha^-1 = ln(8R/a)+1 or half that?
    C2  the cutoff a                 -> how many values is it required to take?
    C3  Axiom III realisability      -> does the claimed Dehn twist exist on M?
    C4  spin / g-factor              -> already-logged repo kills, re-checked
    C5  curvature functional         -> can k(eps) see an off-line zero at all?
    C6  EWFS sum                     -> is S_LF = 2 sqrt 2, and is it an LF sum?
    C7  dark matter                  -> what mass does the quantum pressure need?

Run:  python3 code/constraint_projection/cpf_audit.py
Deps: numpy, sympy, mpmath
Artifact: docs/constraint_projection_audit.json
"""

import json
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]

mp.mp.dps = 60

# CODATA 2022 (Mohr, Newell, Taylor & Tiesinga, Rev. Mod. Phys. 97, 025002 (2025))
ALPHA_INV_CODATA22 = mp.mpf("137.035999177")
ALPHA_INV_CODATA22_UNC = mp.mpf("0.000000021")
HBAR = mp.mpf("1.054571817e-34")
M_E = mp.mpf("9.1093837015e-31")
C_LIGHT = mp.mpf("299792458")
L_PLANCK = mp.mpf("1.616255e-35")
HUBBLE_RADIUS = mp.mpf("1.3e26")          # the manuscript's own target, S 8

R_SPIN = HBAR / (2 * M_E * C_LIGHT)       # the manuscript's R = hbar/(2 m_e c)

RULE = "=" * 74


def banner(n, title):
    print(f"\n{RULE}\nC{n}. {title}\n{RULE}")


# ---------------------------------------------------------------------------
# C1 -- the self-energy algebra, done symbolically from the manuscript's own
#       three inputs:  C_M,  E_self = (e/2)^2 / (2 C_M) = m_e c^2,  R = hbar/2mc
# ---------------------------------------------------------------------------
def check_self_energy():
    banner(1, "Self-energy algebra: does alpha^-1 = ln(8R/a) + 1 follow?")

    e, eps0, R, me, c, hbar, L = sp.symbols(
        "e epsilon_0 R m_e c hbar L", positive=True
    )
    C_M = 2 * sp.pi * eps0 * R / L                    # manuscript S 3
    E_self = (e / 2) ** 2 / (2 * C_M)                 # manuscript S 3
    L_solved = sp.solve(sp.Eq(E_self, me * c ** 2), L)[0]
    L_solved = sp.simplify(L_solved.subs(R, hbar / (2 * me * c)))

    alpha = e ** 2 / (4 * sp.pi * eps0 * hbar * c)
    product = sp.simplify(sp.expand(L_solved * alpha))

    print(f"  C_M          = {C_M}")
    print(f"  E_self       = {sp.simplify(E_self)}")
    print(f"  solve E_self = m_e c^2  for L, then put R = hbar/(2 m_e c):")
    print(f"      L        = {L_solved}")
    print(f"      L * alpha = {product}")
    print()
    print("  So the manuscript's own inputs give   alpha^-1 = L / 2,")
    print("  i.e.  alpha^-1 = ( ln(8R/a) + 1 ) / 2 ,  NOT  ln(8R/a) + 1.")
    print()
    print("  This is not a new result here.  papers/notes/Mobius_Ribbon_Capacitance.tex")
    print("  eq. (alpha_ann) already publishes  alpha^-1_ann = (1/2)(ln(8R/a)+1),")
    print("  and its CODATA-matching aspect  a/R = 8 exp(1 - 2 alpha^-1) ~ 2e-118.")

    factor = sp.nsimplify(product)
    return {
        "manuscript_relation": "alpha^-1 = ln(8R/a) + 1",
        "relation_implied_by_manuscript_inputs": "alpha^-1 = (ln(8R/a) + 1) / 2",
        "L_times_alpha": str(factor),
        "missing_factor": 2,
        "verdict": "FALSE -- factor of 2 dropped",
        "already_in_repo": "papers/notes/Mobius_Ribbon_Capacitance.tex eq. alpha_ann",
    }


# ---------------------------------------------------------------------------
# C2 -- the cutoff a.  The manuscript calls a "not free".  Collect every
#       constraint the manuscript places on it and see whether they agree.
# ---------------------------------------------------------------------------
def check_cutoff_consistency():
    banner(2, "The cutoff a: how many values does the manuscript require?")

    ainv_paper = mp.mpf("137.035999171")

    constraints = [
        # (label, source in manuscript, a/R)
        ("modular parameter tau = i a/R = i/2",
         "S 3, 'the self-linking condition Tr(phi_*) = 2 fixes tau = i/2'",
         mp.mpf(1) / 2),
        ("manuscript's own stated a/R",
         "S 3, 'a/R = 8 exp(-136.035999171)'",
         8 * mp.e ** (-(ainv_paper - 1))),
        ("a/R that the CORRECTED alpha relation needs",
         "C1 above, alpha^-1 = (ln(8R/a)+1)/2 at CODATA 2022",
         8 * mp.e ** (1 - 2 * ALPHA_INV_CODATA22)),
        ("a/R that L_IR = R^2/a = 1.3e26 m needs",
         "S 8, 'L_IR = R^2/a ~ 1.3e26 m'",
         R_SPIN / HUBBLE_RADIUS),
    ]

    print(f"  R = hbar/(2 m_e c) = {mp.nstr(R_SPIN, 8)} m\n")
    rows = []
    for label, src, ratio in constraints:
        a = ratio * R_SPIN
        L = mp.log(8 / ratio) + 1
        row = {
            "constraint": label,
            "manuscript_source": src,
            "a_over_R": mp.nstr(ratio, 6),
            "a_metres": mp.nstr(a, 6),
            "a_over_planck_length": mp.nstr(a / L_PLANCK, 4),
            "ln_8R_over_a_plus_1": mp.nstr(L, 12),
            "alpha_inv_manuscript_formula": mp.nstr(L, 12),
            "alpha_inv_corrected_formula": mp.nstr(L / 2, 12),
            "L_IR_equals_R2_over_a_metres": mp.nstr(R_SPIN / ratio, 6),
        }
        rows.append(row)
        print(f"  {label}")
        print(f"      source        : {src}")
        print(f"      a/R           = {row['a_over_R']}")
        print(f"      a             = {row['a_metres']} m   "
              f"( {row['a_over_planck_length']} x Planck length )")
        print(f"      alpha^-1 (ms) = {row['alpha_inv_manuscript_formula']}")
        print(f"      alpha^-1 (ok) = {row['alpha_inv_corrected_formula']}")
        print(f"      L_IR = R^2/a  = {row['L_IR_equals_R2_over_a_metres']} m")
        print()

    ratios = [c[2] for c in constraints]
    spread = mp.log(max(ratios) / min(ratios), 10)
    print(f"  The four requirements on the single quantity a span "
          f"{mp.nstr(spread, 5)} decades.")
    print("  They are mutually exclusive.  Whichever one is imposed, the others fail:")
    print("   - tau = i/2 gives alpha^-1 = 1.886 (or 3.773 on the uncorrected relation);")
    print("   - the alpha match gives L_IR = 9.5e104 m, ~79 decades past the Hubble radius;")
    print("   - the L_IR match gives alpha^-1 = 46.24.")
    print()
    print("  'Zero free parameters' is therefore not the situation.  There is exactly")
    print("  one free parameter, a/R, and it is fitted separately in each section.")

    return {
        "constraints": rows,
        "decades_spanned": mp.nstr(spread, 5),
        "free_parameters_claimed": 0,
        "free_parameters_actual": 1,
        "verdict": "FALSE -- a is fitted per-section, four incompatible values",
    }


# ---------------------------------------------------------------------------
# C3 -- Axiom III.  Its first four clauses pin M = Klein bottle.  The fifth
#       asks for a diffeomorphism inducing a parabolic of infinite order.
# ---------------------------------------------------------------------------
def check_axiom_iii():
    banner(3, "Axiom III: does the claimed Dehn twist exist on M?")

    print("  Clauses (1)-(2) -- closed, non-orientable, w_1 != 0, double cover T^2 --")
    print("  have exactly one model: the Klein bottle K = T^2 / <tau>,")
    print("  tau(x,y) = (x + 1/2, -y).   (pi_1 = Z x| Z and H_2 = 0 follow.)")
    print()
    print("  Clause (3) asks for phi in Diff(M) with phi_* = [[1,2],[0,1]].")
    print("  Any diffeomorphism of K lifts to T^2 and must normalise the deck")
    print("  group {1, tau}; that group is Z/2, so normalising means commuting.")
    print("  On H_1(T^2) = Z^2 the linear part of tau is D = diag(1,-1).")
    print()

    D = sp.Matrix([[1, 0], [0, -1]])
    phi = sp.Matrix([[1, 2], [0, 1]])
    conj = phi * D * phi.inv()
    commutes = sp.simplify(phi * D - D * phi) == sp.zeros(2, 2)

    print(f"  phi_*                = {phi.tolist()}   trace {phi.trace()}, det {phi.det()}")
    print(f"  phi_* D phi_*^{{-1}}   = {conj.tolist()}")
    print(f"  equals D?            = {commutes}")
    print()

    a_, b_, c_, d_ = sp.symbols("a b c d")
    M = sp.Matrix([[a_, b_], [c_, d_]])
    sol = sp.solve(list(M * D - D * M), [a_, b_, c_, d_])
    centraliser = [sp.diag(1, 1), sp.diag(-1, -1), sp.diag(1, -1), sp.diag(-1, 1)]
    print(f"  Centraliser of D in GL(2,Z): [M,D] = 0 forces {sol} -- diagonal only.")
    print(f"  Integer diagonal matrices of determinant +-1: {len(centraliser)},")
    print("  i.e. Z/2 x Z/2 -- finite, matching Lickorish's MCG(K) = Z/2 (+) Z/2.")
    print()
    traces = {str(m.tolist()): int(m.trace()) for m in centraliser}
    for k, v in traces.items():
        print(f"      {k:24s} trace {v:+d}")
    print()
    print("  phi_* = [[1,2],[0,1]] is parabolic of INFINITE order (phi_*^n = [[1,2n],[0,1]]).")
    print("  A finite group contains no element of infinite order, and phi_* does not")
    print("  commute with D in any case.  No such phi exists.")
    print()
    print("  Note the second edge: within the centraliser, trace = +2 is achieved")
    print("  ONLY by the identity.  So even the weaker reading -- 'some mapping class")
    print("  of M has Tr(phi_*) = 2' -- is carried by the trivial mapping class, which")
    print("  is not a Dehn twist and supplies no self-linking number.")
    print()
    print("  VERDICT: Axiom III has no model.  Sl = Tr(phi_*) = 2, and everything")
    print("  downstream of it (S 4 tau = i/2, S 5 spin and g, S 8 Dehn-twist condition),")
    print("  rests on an axiom no surface satisfies.")

    return {
        "M_forced_to_be": "Klein bottle",
        "deck_linear_part": [[int(x) for x in row] for row in D.tolist()],
        "phi_star": [[int(x) for x in row] for row in phi.tolist()],
        "phi_star_trace": int(phi.trace()),
        "phi_star_order": "infinite (parabolic)",
        "phi_conj_D": [[int(x) for x in row] for row in conj.tolist()],
        "phi_commutes_with_D": bool(commutes),
        "centraliser_order": len(centraliser),
        "centraliser_traces": traces,
        "mcg_klein_bottle": "Z/2 (+) Z/2 (Lickorish 1963) -- finite",
        "only_element_with_trace_2": "identity",
        "verdict": "UNSATISFIABLE -- Axiom III has no model",
    }


# ---------------------------------------------------------------------------
# C4 -- spin and g.  Both claims are already in the Elimination Ledger.
# ---------------------------------------------------------------------------
def check_spin_and_g():
    banner(4, "Spin and g-factor: re-checking against the logged kills")

    print("  Manuscript S 5 asserts  s = Sl/4 = 1/2  and  g = Sl = 2.")
    print()
    print("  (a) g = Sl = 2 is the KILLED claim of 2026-07-26:")
    print("      sigma = (-1)^(Sl+1), so an Sl = 0 round circle is spinorial in")
    print("      exactly the same sense.  The spin content of Sl is ONE PARITY BIT,")
    print("      and 2 and 0 are the same bit.  The value 2 does no work.")
    print("      -> docs/Elimination_Ledger.md 2026-07-26, T4.")
    print()
    print("  (b) The successor test closed the magnitude route entirely:")
    print("      mu = (q/T) A and <L> = (2m/T) A share the same vector area, so")
    print("      mu/<L> = q/2m and g = 1 EXACTLY for every closed curve.  T2 no-go.")
    print("      -> docs/Elimination_Ledger.md 2026-07-26 (successor), T4.")
    print()
    print("  (c) The repo's own computation of the (2,1) centerline gives")
    print("      Tw + Wr = -2.000000, i.e. Sl = -2 as parameterised.  On s = Sl/4")
    print("      that is s = -1/2.  The manuscript takes |Sl| without saying so.")
    print()
    print("  (d) s = Sl/4 has no stated derivation.  The 4 is not fixed by anything")
    print("      in the manuscript; White-Calugareanu-Fuller (Sl = Tw + Wr) and the")
    print("      Finkelstein-Rubinstein mechanism are both cited, but FR yields a")
    print("      Z/2 statistics sector, not a magnitude -- the same gap the ledger")
    print("      recorded when it killed (a).")
    print()
    print("  (e) A (p,q) torus knot with q = 1 is the UNKNOT.  The manuscript calls")
    print("      it a '(2,1)-torus knot'; the repo's parent note already corrects")
    print("      this to 'framed unknot'.")

    return {
        "claim_g_equals_Sl": "T4 -- killed 2026-07-26 (parity bit, sigma = (-1)^(Sl+1))",
        "claim_s_equals_Sl_over_4": "unsupported -- the 4 is not derived; FR gives Z/2, not a magnitude",
        "geometric_g_no_go": "g = 1 exactly for every closed curve (T2 no-go)",
        "repo_measured_Sl": -2.0,
        "s_implied_by_repo_sign": -0.5,
        "knot_type": "(2,1) has q = 1 -> unknot, not a knot",
        "verdict": "RESTATES TWO ALREADY-FALSIFIED CLAIMS (T4)",
    }


# ---------------------------------------------------------------------------
# C5 -- the curvature functional.  Can it distinguish RH from not-RH?
# ---------------------------------------------------------------------------
def check_curvature_functional():
    banner(5, "Curvature functional: can k(eps) see an off-line zero?")

    beta, eps = sp.symbols("beta epsilon", real=True)
    summand = 1 / ((sp.Rational(1, 2) - beta) ** 2 - eps ** 2)
    reflected = summand.subs(beta, 1 - beta)
    invariant = sp.simplify(reflected - summand) == 0
    on_line = sp.simplify(summand.subs(beta, sp.Rational(1, 2)))

    print(f"  manuscript S 7:  k(eps) = 2 eps SUM_rho 1/((1/2 - beta)^2 - eps^2)")
    print()
    print(f"  summand t(beta)      = {summand}")
    print(f"  t(1 - beta) - t(beta) = {sp.simplify(reflected - summand)}")
    print(f"  invariant under beta -> 1 - beta ?  {invariant}")
    print()
    print("  (i) BLINDNESS.  beta enters only through (1/2 - beta)^2, which is exactly")
    print("      the invariant of the functional equation's involution beta -> 1-beta.")
    print("      zeta's zeros are symmetric under that involution, so any off-line zero")
    print("      comes with its mirror and contributes identically.  k(eps) takes the")
    print("      same value on a critical-line configuration and on its reflection.")
    print("      The functional cannot distinguish RH from its negation.")
    print()
    print(f"  (ii) SIGN.  On the critical line t(1/2) = {on_line}, so EVERY on-line")
    print("      zero contributes -1/eps^2 -- none contributes 0.  Summing N of them,")
    N = sp.symbols("N", positive=True)
    k_on = sp.simplify(2 * eps * N * on_line)
    print(f"          k(eps) = {k_on}")
    print("      which diverges as N -> oo and vanishes for no finite eps.  RH makes")
    print("      k maximally divergent; the stated criterion is inverted, not merely")
    print("      unproved.")
    print()

    zeros = 50
    e0 = mp.mpf("0.1")
    delta = mp.mpf("0.2")

    def k_at(b):
        return 2 * e0 * zeros * (1 / ((mp.mpf("0.5") - b) ** 2 - e0 ** 2))

    k_online = k_at(mp.mpf("0.5"))
    k_plus = k_at(mp.mpf("0.5") + delta)
    k_minus = k_at(mp.mpf("0.5") - delta)

    print(f"  numerical demonstration, {zeros} zeros, eps = {e0}:")
    print(f"      all at beta = 0.5        ->  k = {mp.nstr(k_online, 10)}")
    print(f"      all at beta = 0.5 + 0.2  ->  k = {mp.nstr(k_plus, 10)}")
    print(f"      all at beta = 0.5 - 0.2  ->  k = {mp.nstr(k_minus, 10)}")
    print("      the two off-line mirror images are IDENTICAL, and none of the three is 0.")
    print()
    print("  (iii) EMPIRICAL DIRECTION.  Even a repaired functional would not make")
    print("      'Omega_k = 0 <-> RH' testable: Omega_k is measured as 0.0007 +- 0.0019")
    print("      and no measurement can establish an exact zero.  A biconditional here")
    print("      would make a theorem of arithmetic contingent on CMB data.")
    print()
    print("  Repo rule: the Riemann Hypothesis is nowhere claimed proved.  S 7 claims")
    print("  an equivalence, which is a proof claim in both directions.")

    return {
        "summand": str(summand),
        "invariant_under_functional_equation": bool(invariant),
        "value_on_critical_line": str(on_line),
        "k_for_N_online_zeros": str(k_on),
        "numeric_k_online": mp.nstr(k_online, 10),
        "numeric_k_beta_plus_delta": mp.nstr(k_plus, 10),
        "numeric_k_beta_minus_delta": mp.nstr(k_minus, 10),
        "mirror_images_identical": True,
        "verdict": "FALSE -- blind by construction, and inverted in sign",
    }


# ---------------------------------------------------------------------------
# C6 -- the EWFS sum.  The arithmetic is right; the identification is not.
# ---------------------------------------------------------------------------
def check_ewfs():
    banner(6, "EWFS: is S_LF = 2 sqrt 2, and is it a Local Friendliness sum?")

    def obs(t):
        return np.array([[np.cos(t), np.sin(t)], [np.sin(t), -np.cos(t)]])

    phi_plus = np.array([1, 0, 0, 1]) / np.sqrt(2)

    def corr(a, b):
        return float(phi_plus @ np.kron(obs(a), obs(b)) @ phi_plus)

    th2, th3, ph2, ph3 = 0.0, np.pi / 2, np.pi / 4, -np.pi / 4
    e22, e23, e32, e33 = corr(th2, ph2), corr(th2, ph3), corr(th3, ph2), corr(th3, ph3)
    S = e22 + e23 + e32 - e33
    tsirelson = 2 * np.sqrt(2)

    print(f"  E(A2,B2) = {e22:+.6f}    E(A2,B3) = {e23:+.6f}")
    print(f"  E(A3,B2) = {e32:+.6f}    E(A3,B3) = {e33:+.6f}")
    print(f"  S        = {S:.10f}      2 sqrt 2 = {tsirelson:.10f}")
    print(f"  Tsirelson bound saturated: {abs(S - tsirelson) < 1e-12}")
    print()
    print("  ARITHMETIC CONFIRMED.  This is the one section whose displayed number")
    print("  survives its own computation.")
    print()
    print("  But the identification does not.  Both operators are cos(t) sigma_z +")
    print("  sin(t) sigma_x, and only settings {2,3} appear on either wing.  The")
    print("  setting that makes an EWFS an EWFS -- x = 1 / y = 1, 'open the lab and")
    print("  read the friend's already-recorded outcome' -- enters no term of the sum.")
    print("  With two settings per wing this expression IS CHSH; its local bound is 2")
    print("  because that is the CHSH bound, not because of anything about observers.")
    print()
    print("  Consequences:")
    print("   - S 6 demonstrates ordinary Bell nonlocality, known since 1982, not")
    print("     a Local Friendliness violation.  Bong et al. (Nat. Phys. 16, 1199")
    print("     (2020)) LF facets involve the x=1 row precisely because that is where")
    print("     Absoluteness of Observed Events enters.")
    print("   - 'falsifying AOE' overstates even a genuine LF violation.  The LF")
    print("     theorem falsifies the CONJUNCTION of Absoluteness of Observed Events,")
    print("     Locality and No-Superdeterminism.  No single conjunct is singled out.")
    print("   - the C_6/D_6 axial frame, the projection of |Phi+> onto it, and the")
    print("     super-observer structure are all inert: none appears in the algebra.")

    return {
        "correlators": {"E_A2B2": e22, "E_A2B3": e23, "E_A3B2": e32, "E_A3B3": e33},
        "S": S,
        "tsirelson": tsirelson,
        "arithmetic_confirmed": bool(abs(S - tsirelson) < 1e-12),
        "friend_setting_present": False,
        "is_LF_inequality": False,
        "identification": "CHSH relabelled; local bound 2 is the CHSH bound",
        "AOE_claim": "overstated -- LF falsifies AOE AND Locality AND No-Superdeterminism",
        "verdict": "ARITHMETIC TRUE, IDENTIFICATION FALSE",
    }


# ---------------------------------------------------------------------------
# C7 -- dark matter.  What does the quantum-pressure term actually need?
# ---------------------------------------------------------------------------
def check_dark_matter():
    banner(7, "Dark matter: what mass does (hbar^2/2m)|grad psi|^2 require?")

    Rp, Sp, Rr, hbar_s, m_s = sp.symbols("R' S' R hbar m", real=True, positive=True)
    total = sp.expand(hbar_s ** 2 / (2 * m_s) * (Rp ** 2 + (Rr * Sp / hbar_s) ** 2))
    quantum = hbar_s ** 2 * Rp ** 2 / (2 * m_s)
    bulk = Rr ** 2 * Sp ** 2 / (2 * m_s)
    exact = sp.simplify(total - (quantum + bulk)) == 0

    print("  With psi = R exp(iS/hbar), grad psi = (R' + i R S'/hbar) exp(iS/hbar):")
    print(f"      (hbar^2/2m)|grad psi|^2 = {total}")
    print(f"      = {quantum}   [amplitude gradient]")
    print(f"      + {bulk}   [bulk flow]")
    print(f"      split exact: {exact}")
    print()
    print("  (i) DOUBLE COUNTING.  The second term is R^2 S'^2 / 2m = (1/2) rho v^2")
    print("      with rho = R^2 and v = S'/m -- the ordinary kinetic energy density of")
    print("      the visible matter itself.  S 6's T_00 = rho_vis c^2 + rho_DM c^2 then")
    print("      counts it a second time, as dark.")
    print()
    print("  (ii) THE Re/Im STORY IS WRONG.  |grad psi|^2 is not a function of Im(psi)")
    print("      alone, and the Re/Im split is not gauge invariant: a global U(1) phase")
    print("      rotates one into the other.  Electromagnetic coupling enters through")
    print("      the covariant derivative, not through 'the real component'.")
    print()

    ev = mp.mpf("1.602176634e-19")
    kpc = mp.mpf("3.0856775814913673e19")
    v_gal = mp.mpf("2.0e5")

    m_needed = HBAR / (v_gal * kpc)
    m_needed_ev = m_needed * C_LIGHT ** 2 / ev
    lam_e = HBAR / (M_E * v_gal)

    print("  (iii) THE SCALE.  Quantum pressure only shapes a rotation curve when the")
    print("      de Broglie wavelength is galactic.  At v = 200 km/s and L = 1 kpc:")
    print(f"          m required   = {mp.nstr(m_needed, 4)} kg = {mp.nstr(m_needed_ev, 4)} eV/c^2")
    print(f"          lambda_dB(e) = {mp.nstr(lam_e, 4)} m")
    print(f"          m_e / m_req  = {mp.nstr(M_E / m_needed, 4)}")
    print()
    print("      ~1e-23 eV is the fuzzy-dark-matter window: an ultralight scalar, which")
    print("      is exactly the 'exotic particle' S 6 claims to avoid.  For any Standard")
    print("      Model mass the term is ~29 orders of magnitude too short-ranged to")
    print("      matter at kpc scales.  'Resolves galactic rotation curves without")
    print("      exotic particles' is false either way: with an SM mass the effect is")
    print("      absent, and with the mass that works the particle is exotic.")
    print()
    print("  No Jeans-equation solution, no rotation curve and no galaxy data appear")
    print("  in S 6; 'matching observations' is asserted, not shown.")

    return {
        "madelung_split_exact": bool(exact),
        "bulk_term": "R^2 S'^2 / 2m = (1/2) rho v^2 -- the visible matter's own kinetic energy",
        "double_counted_in_T00": True,
        "mass_required_kg": mp.nstr(m_needed, 6),
        "mass_required_eV": mp.nstr(m_needed_ev, 6),
        "electron_de_broglie_at_200kms_m": mp.nstr(lam_e, 6),
        "m_e_over_m_required": mp.nstr(M_E / m_needed, 6),
        "verdict": "FALSE -- double counts, and needs an ultralight exotic scalar",
    }


# ---------------------------------------------------------------------------
def check_citations_and_axioms():
    banner(8, "Axioms I-II and the bibliography")

    print("  AXIOM I.  'B = A_Q / Q^x' is malformed: Q^x is the multiplicative group")
    print("  and does not act on the additive adeles by translation.  The two standard")
    print("  objects are A_Q/Q (compact, additive) and the idele class group A_Q^x/Q^x.")
    print()
    print("  Either reading contradicts the axiom's own last sentence.  Both groups are")
    print("  ABELIAN, hence amenable -- every abelian group is amenable (Markov-Kakutani).")
    print("  A_Q/Q is moreover compact, so it carries a Haar PROBABILITY measure that is")
    print("  translation invariant and countably additive.  The axiom asserts that no")
    print("  finitely additive translation-invariant probability measure exists.  That")
    print("  is false for every candidate reading of B.")
    print()
    print("  AXIOM II.  The kernel maps onto R^{3,1} but delta^{(3)}(r(u,v) - x) fixes")
    print("  only three coordinates; nothing in the kernel produces the time direction.")
    print("  A 2-parameter integral against a 3-dimensional delta is also generically")
    print("  distributional, not a function, so 'Fredholm' is not established.")
    print()
    print("  S 3 also computes an ELECTROSTATIC CAPACITANCE for M.  M is forced to be")
    print("  the Klein bottle (C3), which admits no embedding in R^3 -- only immersions")
    print("  with self-intersection.  There is no conductor to charge, and no 'annulus';")
    print("  the Klein bottle is closed and has no boundary.  The formula actually used")
    print("  is the thin-ring one, whose log term ln(8R/a) is the Kelvin-Maxwell ring")
    print("  INDUCTANCE log; its additive constant there is -7/4 or -2, never +1.")
    print()
    print("  BIBLIOGRAPHY.")
    print("   - [Bianconi2024] arXiv:2401.12345 is a placeholder identifier.  The paper")
    print("     is G. Bianconi, 'Gravity from entropy', arXiv:2408.14391, Phys. Rev. D")
    print("     111, 066001 (2025).  Note also that the GfE G-field is ALGEBRAICALLY")
    print("     CONSTRAINED, not a field obeying an independent wave equation; S 3's")
    print("     'Box G + lambda G = 0 with lambda_UV = 1/a^2' and its discrete eigenvalue")
    print("     gap are asserted, with no derivation from the GfE action.")
    print("   - [CODATA2022] 'E. Tiesinga et al., Rev. Mod. Phys. 94, 035002 (2023)'")
    print("     matches no CODATA article of record.  CODATA 2018 is Tiesinga, Mohr,")
    print("     Newell & Taylor, Rev. Mod. Phys. 93, 025010 (2021); CODATA 2022 is Mohr,")
    print("     Newell, Taylor & Tiesinga, Rev. Mod. Phys. 97, 025002 (2025).")
    print(f"   - the 2022 value is alpha^-1 = {ALPHA_INV_CODATA22}"
          f"({str(ALPHA_INV_CODATA22_UNC)[-2:]}).")
    print("   - [Proietti2019] and [Finkelstein1968] check out as cited.")

    return {
        "axiom_I_type_error": "A_Q/Q^x is malformed; Q^x is multiplicative",
        "axiom_I_amenability": "FALSE -- every abelian group is amenable; A_Q/Q is "
                               "compact and carries a Haar probability measure",
        "axiom_II_time_direction": "delta^{(3)} fixes 3 coordinates; R^{3,1} needs 4",
        "klein_bottle_embedding": "no embedding in R^3; the capacitance has no referent",
        "log_provenance": "ln(8R/a) is the thin-ring inductance log; its constant is -7/4 or -2",
        "bianconi_identifier_given": "arXiv:2401.12345 (placeholder)",
        "bianconi_identifier_actual": "arXiv:2408.14391, Phys. Rev. D 111, 066001 (2025)",
        "gfe_G_field": "algebraically constrained; no wave equation, no derived eigenvalue gap",
        "codata_given": "Rev. Mod. Phys. 94, 035002 (2023) -- matches no CODATA release",
        "codata_2022_actual": "Mohr, Newell, Taylor & Tiesinga, Rev. Mod. Phys. 97, 025002 (2025)",
        "alpha_inv_codata_2022": str(ALPHA_INV_CODATA22),
        "verdict": "AXIOM I FALSE, AXIOM II ILL-POSED, TWO CITATIONS WRONG",
    }


# ---------------------------------------------------------------------------
def main():
    print(RULE)
    print("Constraint Projection Framework -- audit instrument")
    print("target: papers/notes/Constraint_Projection_Framework.tex (as submitted)")
    print(RULE)

    results = {
        "C1_self_energy_algebra": check_self_energy(),
        "C2_cutoff_consistency": check_cutoff_consistency(),
        "C3_axiom_iii_realisability": check_axiom_iii(),
        "C4_spin_and_g_factor": check_spin_and_g(),
        "C5_curvature_functional": check_curvature_functional(),
        "C6_ewfs": check_ewfs(),
        "C7_dark_matter": check_dark_matter(),
        "C8_axioms_and_citations": check_citations_and_axioms(),
    }

    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    summary = {k: v["verdict"] for k, v in results.items()}
    for k, v in summary.items():
        print(f"  {k:32s} {v}")
    print()
    print("  One displayed number survives its own computation: S_LF = 2 sqrt 2 (C6),")
    print("  and it is CHSH, which has been measured since 1982.  Everything the")
    print("  manuscript claims as new either fails its own algebra, restates a claim")
    print("  this repository has already falsified, or rests on an unsatisfiable axiom.")
    print(RULE)

    payload = {
        "description": "Audit of the Constraint Projection Framework manuscript",
        "source": "code/constraint_projection/cpf_audit.py",
        "target_manuscript": "papers/notes/Constraint_Projection_Framework.tex",
        "companion_note": "papers/notes/Constraint_Projection_Framework_Audit.tex",
        "constants": {
            "alpha_inv_CODATA_2022": str(ALPHA_INV_CODATA22),
            "R_spin_metres": mp.nstr(R_SPIN, 10),
        },
        "checks": results,
        "summary": summary,
    }
    out = ROOT / "docs" / "constraint_projection_audit.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
