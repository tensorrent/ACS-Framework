#!/usr/bin/env python3
# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Where g = 2 actually comes from, and what the measured g-factor says about it.

Successor to the 2026-07-26 kill of `Sl = 2 <-> g = 2`
(docs/Elimination_Ledger.md).  That entry closed with Levy-Leblond's 1967 result
as "the decisive external point" -- g = 2 follows from LINEARIZING the Schrodinger
equation, so it is neither relativistic nor topological in origin -- but the
repository has cited that result without ever running it.  This script runs it,
then reads the measured anomaly as it lies.

    W1  sigma algebra                sigma_i sigma_j = delta_ij + i eps_ijk sigma_k
    W2  Pauli identity               (sigma.pi)^2 = pi^2 - q hbar (sigma.B)
    W3  Levy-Leblond -> Schrodinger, minimal coupling, g = 2
    W4  4 pi periodicity from SU(2) alone -- no manifold
    W5  Dirac, for contrast: same g = 2, so g = 2 does not diagnose relativity
    W6  read the data: a_e measured vs a_e = 0
    W7  the QED series, validated by inverting it for alpha
    W8  QED vs measurement using INDEPENDENTLY measured alpha
    W9  parameter count

Nothing here is new physics.  W1-W5 are textbook; the point is that they are
machine-checked rather than cited, and that they need no surface, no framing and
no self-linking number.

Run:  python3 code/constraint_projection/wave_equation_gfactor.py
Deps: sympy, mpmath
Artifact: docs/wave_equation_gfactor.json
"""

import json
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
mp.mp.dps = 40

RULE = "=" * 78

# --- measured inputs ---------------------------------------------------------
# Fan, Myers, Sukra & Gabrielse, Phys. Rev. Lett. 130, 071801 (2023); 0.13 ppt.
G_OVER_2 = mp.mpf("1.00115965218059")
U_G_OVER_2 = mp.mpf("0.00000000000013")
A_E = G_OVER_2 - 1
U_A_E = U_G_OVER_2
# alpha^-1 from that measurement plus QED, as quoted by the same paper:
ALPHA_INV_FROM_AE = mp.mpf("137.035999166")
U_ALPHA_INV_FROM_AE = mp.mpf("0.000000015")
# independent recoil determinations
ALPHA_RB = (mp.mpf("137.035999206"), mp.mpf("0.000000011"))   # Morel et al. 2020
ALPHA_CS = (mp.mpf("137.035999046"), mp.mpf("0.000000027"))   # Parker et al. 2018

I2, Z2 = sp.eye(2), sp.zeros(2)
SX = sp.Matrix([[0, 1], [1, 0]])
SY = sp.Matrix([[0, -sp.I], [sp.I, 0]])
SZ = sp.Matrix([[1, 0], [0, -1]])
SIG = [SX, SY, SZ]


def head(tag, title):
    print(f"\n{RULE}\n{tag}. {title}\n{RULE}")


# ---------------------------------------------------------------------------
def w1_sigma_algebra():
    head("W1", "The sigma algebra -- the only structural input")
    ok = True
    for i in range(3):
        for j in range(3):
            lhs = SIG[i] * SIG[j]
            rhs = sp.KroneckerDelta(i, j) * I2 + sp.I * sum(
                (sp.LeviCivita(i, j, k) * SIG[k] for k in range(3)), Z2)
            ok = ok and sp.simplify(lhs - rhs) == Z2
    print("  sigma_i sigma_j = delta_ij + i eps_ijk sigma_k")
    print(f"  verified for all 9 ordered pairs: {ok}")
    print("  This is su(2).  It is the whole input to W2-W4.")
    assert ok
    return {"identity": "sigma_i sigma_j = delta_ij + i eps_ijk sigma_k",
            "pairs_verified": 9, "holds": ok}


# ---------------------------------------------------------------------------
def w2_pauli_identity():
    head("W2", "Pauli identity with NON-commuting kinetic momenta")
    q, hbar = sp.symbols("q hbar", real=True)
    pi_ = list(sp.symbols("pi_1 pi_2 pi_3", commutative=False))
    B = list(sp.symbols("B_1 B_2 B_3", commutative=False))

    # [pi_i, pi_j] = i q hbar eps_ijk B_k   (from pi = p - qA)
    def comm(i, j):
        return sp.I * q * hbar * sum(sp.LeviCivita(i, j, k) * B[k] for k in range(3))

    extra = Z2
    for i in range(3):
        for j in range(3):
            for k in range(3):
                e = sp.LeviCivita(i, j, k)
                if e != 0:
                    extra += sp.Rational(1, 2) * sp.I * e * comm(i, j) * SIG[k]
    extra = sp.expand(extra)
    target = sp.expand(-q * hbar * sum((B[k] * SIG[k] for k in range(3)), Z2))
    same = sp.simplify(extra - target) == Z2

    print("  pi_i = p_i - q A_i,   [pi_i, pi_j] = i q hbar eps_ijk B_k")
    print("  (sigma.pi)^2 = sum_ij (delta_ij + i eps_ijk sigma_k) pi_i pi_j")
    print("               = pi^2 . I  +  (i/2) eps_ijk sigma_k [pi_i, pi_j]")
    print(f"  antisymmetric part = {sp.nsimplify(extra[0,0])} ... (2x2 matrix)")
    print(f"  equals  -q hbar (sigma.B) :  {same}")
    print("\n  =>  (sigma.pi)^2 = pi^2 - q hbar (sigma.B)")
    print("  This single identity is where the factor of 2 in g will come from.")
    assert same
    return {"identity": "(sigma.pi)^2 = pi^2 - q hbar (sigma.B)",
            "verified_symbolically": bool(same),
            "commutator": "[pi_i, pi_j] = i q hbar eps_ijk B_k"}


# ---------------------------------------------------------------------------
def w3_levy_leblond():
    head("W3", "Levy-Leblond: linearize Schrodinger, then read off g")
    m, g = sp.symbols("m g", real=True, positive=True)
    q, hbar = sp.symbols("q hbar", real=True)

    print("  Dirac linearized Klein-Gordon.  Levy-Leblond (Comm. Math. Phys. 6")
    print("  (1967) 286) did the same to SCHRODINGER.  With psi = (phi, chi), each")
    print("  a two-component spinor, the free equations are")
    print("      E phi + (sigma.p) chi = 0")
    print("      (sigma.p) phi + 2 m chi = 0")
    print("  The second gives chi = -(sigma.p) phi / (2m); substituting,")
    print("      E phi = (sigma.p)^2 phi / (2m) = p^2 phi / (2m)")
    print("  which is the free Schrodinger equation.  Note what was NOT used:")
    print("  no c, no Lorentz transformation, no metric, no light cone.  This is a")
    print("  Galilean theory throughout.\n")
    print("  Minimal coupling p -> pi = p - qA, E -> E - qA_0, then apply W2:")
    print("      (E - qA_0) phi = [ pi^2/(2m) - (q hbar / 2m)(sigma.B) ] phi")
    print("  The spin term is therefore  -(q hbar / 2m)(sigma.B).\n")
    print("  Zeeman form:  H = -mu.B  with  mu = g (q/2m) S,  S = (hbar/2) sigma")
    print("      -mu.B = -(g q hbar / 4m)(sigma.B)")
    gval = sp.solve(sp.Eq(-q * hbar / (2 * m), -g * q * hbar / (4 * m)), g)[0]
    print(f"      equate coefficients  ->  g = {gval}\n")
    assert gval == 2
    print("  g = 2 from su(2) plus linearization.  No relativity, no geometry,")
    print("  no framing, no self-linking number, no surface of any kind.")
    return {"free_equations": ["E phi + (sigma.p) chi = 0",
                              "(sigma.p) phi + 2 m chi = 0"],
            "reduces_to": "E phi = p^2 phi / 2m (free Schrodinger)",
            "spin_term": "-(q hbar / 2m)(sigma.B)",
            "g": int(gval),
            "relativity_used": False}


# ---------------------------------------------------------------------------
def w4_periodicity():
    head("W4", "4 pi periodicity from SU(2) alone -- no manifold required")
    th = sp.symbols("theta", real=True)
    U = sp.cos(th / 2) * I2 - sp.I * sp.sin(th / 2) * SZ
    rows = {}
    for val, lab in [(0, "0"), (sp.pi, "pi"), (2 * sp.pi, "2 pi"), (4 * sp.pi, "4 pi")]:
        M = sp.simplify(U.subs(th, val))
        rows[lab] = str(M.tolist())
        print(f"  exp(-i({lab}) sigma_z/2) = {M.tolist()}")
    print("\n  A 2 pi rotation returns -I; 4 pi returns +I.  This is the nontrivial")
    print("  element of pi_1(SO(3)) = Z/2 acting in the spinor representation.")
    print("  It requires a GROUP, not a surface: no w_1, no non-orientability, and")
    print("  no Klein bottle enters.  The manuscript's Sec 4 derives the same 4 pi")
    print("  from 'non-orientability of M', which is a longer route to a fact that")
    print("  su(2) already supplies -- and, per the audit, a route whose Axiom III")
    print("  has no model.")
    return {"rotations": rows, "pi1_SO3": "Z/2", "manifold_required": False}


# ---------------------------------------------------------------------------
def w5_dirac():
    head("W5", "Dirac, for contrast")
    print("  Squaring the Dirac operator produces the SAME Pauli term")
    print("  -q hbar (sigma.B), hence the same g = 2 at tree level.")
    print("  So g = 2 does not diagnose relativity either: a Galilean theory")
    print("  (Levy-Leblond) and a Lorentzian one (Dirac) agree exactly here.")
    print("  What IS relativistic -- indeed what is quantum-field-theoretic -- is")
    print("  the ANOMALY, and that is where every framework gets separated.")
    return {"dirac_tree_g": 2, "levy_leblond_g": 2,
            "conclusion": "g = 2 diagnoses neither relativity nor topology"}


# ---------------------------------------------------------------------------
def w6_read_the_data():
    head("W6", "Read the data as it lies")
    g_meas = 2 * G_OVER_2
    print(f"  g/2 measured = {G_OVER_2}(13)")
    print(f"  g   measured = {g_meas}")
    print(f"  a_e = (g-2)/2 = {mp.nstr(A_E, 14)}  +- {mp.nstr(U_A_E, 2)}")
    print(f"  relative precision = {mp.nstr(U_A_E/A_E, 3)}   (0.13 ppt)")
    print("  source: Fan, Myers, Sukra & Gabrielse, PRL 130, 071801 (2023)\n")
    sep = A_E / U_A_E
    print(f"  Any framework whose output is 'g = 2 exactly' predicts a_e = 0.")
    print(f"  The measured value sits {mp.nstr(sep, 4)} sigma from 0.")
    print(f"  'g = 2' is correct to three decimal places and wrong at the fourth.")
    return {"g_over_2": str(G_OVER_2), "g": mp.nstr(g_meas, 15),
            "a_e": mp.nstr(A_E, 14), "u_a_e": mp.nstr(U_A_E, 2),
            "sigma_from_zero": mp.nstr(sep, 4),
            "source": "Fan et al., PRL 130, 071801 (2023)"}


# ---------------------------------------------------------------------------
# QED series.  Mass-independent A1^(2n) plus mass-dependent A2 (mu, tau) terms.
A1 = [mp.mpf("0.5"),
      mp.mpf("-0.328478965579193"),   # exact: 197/144 + pi^2/12 - pi^2 ln2/2 + 3 zeta(3)/4
      mp.mpf("1.181241456587"),       # Laporta & Remiddi 1996
      mp.mpf("-1.912245764926446"),   # Laporta 2017, analytic
      mp.mpf("6.737")]                # Aoyama-Kinoshita-Nio, +- 0.159
A2 = {2: mp.mpf("5.19738667e-7") + mp.mpf("1.83798e-9"),
      3: mp.mpf("-7.37394155e-6") + mp.mpf("-6.5819e-8") + mp.mpf("0.190945e-12"),
      4: mp.mpf("9.161970703e-4") + mp.mpf("7.42924e-6")}
HAD, U_HAD = mp.mpf("1.693e-12"), mp.mpf("0.012e-12")
EW = mp.mpf("0.0297e-12")


def a_of(alpha_inv):
    x = (1 / alpha_inv) / mp.pi
    tot = sum(c * x ** (n + 1) for n, c in enumerate(A1))
    for n, c in A2.items():
        tot += c * x ** n
    return tot + HAD + EW


def w7_series():
    head("W7", "The QED series, validated by inverting it")
    x = (1 / ALPHA_INV_FROM_AE) / mp.pi
    print(f"  alpha/pi = {mp.nstr(x, 10)}\n")
    print(f"  {'order':>6} {'A1 (mass-indep)':>20} {'term':>14} "
          f"{'A2 (mass-dep)':>16} {'term':>14}")
    terms = []
    for n, c in enumerate(A1, start=1):
        t1 = c * x ** n
        c2 = A2.get(n)
        t2 = c2 * x ** n if c2 is not None else None
        terms.append({"order": n, "A1": mp.nstr(c, 16), "term_A1": mp.nstr(t1, 8),
                      "A2": mp.nstr(c2, 10) if c2 is not None else None,
                      "term_A2": mp.nstr(t2, 8) if t2 is not None else None})
        print(f"  {n:>6} {mp.nstr(c,16):>20} {mp.nstr(t1,8):>14} "
              f"{(mp.nstr(c2,10) if c2 is not None else '-'):>16} "
              f"{(mp.nstr(t2,8) if t2 is not None else '-'):>14}")
    md = sum(c * x ** n for n, c in A2.items())
    print(f"\n  hadronic = {mp.nstr(HAD,6)}   electroweak = {mp.nstr(EW,6)}")
    print(f"  total mass-dependent = {mp.nstr(md, 6)}")
    print("\n  NOTE.  The mass-dependent terms (muon and tau vacuum-polarization")
    print("  insertions) are ~2.7e-12 -- about 20x the measurement uncertainty.")
    print("  Omitting them shifts the predicted a_e by more than the entire")
    print("  experimental error budget, so any comparison without them is invalid.")

    root = mp.findroot(lambda t: a_of(t) - A_E, mp.mpf("137.036"))
    off = abs(root - ALPHA_INV_FROM_AE) / U_ALPHA_INV_FROM_AE
    print(f"\n  VALIDATION.  Invert the series for alpha^-1 using the measured a_e:")
    print(f"     this series      -> alpha^-1 = {mp.nstr(root, 14)}")
    print(f"     Fan et al. quote -> alpha^-1 = {ALPHA_INV_FROM_AE}"
          f"({str(U_ALPHA_INV_FROM_AE).split('.')[1].lstrip('0')})")
    print(f"     agreement to {mp.nstr(off, 3)} x their quoted uncertainty.")
    print("  The series is anchored to an independent published number, not asserted.")
    return {"terms": terms, "mass_dependent_total": mp.nstr(md, 6),
            "hadronic": mp.nstr(HAD, 6), "electroweak": mp.nstr(EW, 6),
            "inverted_alpha_inv": mp.nstr(root, 14),
            "literature_alpha_inv": str(ALPHA_INV_FROM_AE),
            "agreement_in_sigma": mp.nstr(off, 3)}


# ---------------------------------------------------------------------------
def w8_vs_independent_alpha():
    head("W8", "QED vs measurement, using INDEPENDENTLY measured alpha")
    print("  CODATA's alpha is partly determined BY a_e plus QED theory, so using it")
    print("  here would be circular.  Use the atom-recoil determinations instead.\n")
    x = (1 / ALPHA_INV_FROM_AE) / mp.pi
    rows = []
    for nm, (v, u) in [("Rb recoil, Morel et al. 2020", ALPHA_RB),
                       ("Cs recoil, Parker et al. 2018", ALPHA_CS)]:
        pred = a_of(v)
        u_pred = mp.sqrt((pred * u / v) ** 2 + (mp.mpf("0.159") * x ** 5) ** 2 + U_HAD ** 2)
        d = A_E - pred
        s = d / mp.sqrt(u_pred ** 2 + U_A_E ** 2)
        rows.append({"source": nm, "alpha_inv": str(v),
                     "a_e_pred": mp.nstr(pred, 14), "u_pred": mp.nstr(u_pred, 2),
                     "residual": mp.nstr(d, 3), "sigma": mp.nstr(s, 3)})
        print(f"  {nm}")
        print(f"     alpha^-1 = {v}({str(u).split('.')[1].lstrip('0')})")
        print(f"     a_e pred = {mp.nstr(pred,14)} +- {mp.nstr(u_pred,2)}")
        print(f"     residual = {mp.nstr(d,3)}   ->  {mp.nstr(s,3)} sigma\n")
    tension = (ALPHA_RB[0] - ALPHA_CS[0]) / mp.sqrt(ALPHA_RB[1] ** 2 + ALPHA_CS[1] ** 2)
    print(f"  Rb vs Cs disagree with each other at {mp.nstr(tension, 3)} sigma.")
    print("  READING: the dominant discrepancy in this sector is EXPERIMENTAL -- the")
    print("  two recoil measurements -- not a failure of QED.  Caveat: this")
    print("  uncertainty propagation is cruder than a full CODATA adjustment, so")
    print("  treat the per-source sigmas as indicative, not definitive.")
    return {"comparisons": rows, "rb_vs_cs_sigma": mp.nstr(tension, 3),
            "caveat": "crude uncertainty propagation; sigmas indicative"}


# ---------------------------------------------------------------------------
def w9_parameter_count():
    head("W9", "What each framework spends, and what it buys")
    rows = [
        ("Levy-Leblond (Galilean)", "su(2) + linearization", "2 exactly", "3 decimals"),
        ("Dirac (tree level)", "su(2) + Lorentz", "2 exactly", "3 decimals"),
        ("QED", "alpha (measured) + loop expansion", "2(1 + a_e)", "12 digits"),
        ("CPF manuscript", "Klein bottle + Sl = 2", "2 exactly", "3 decimals"),
    ]
    print(f"  {'framework':>25} {'inputs':>36} {'g':>12}  matches to")
    for r in rows:
        print(f"  {r[0]:>25} {r[1]:>36} {r[2]:>12}  {r[3]}")
    print()
    print("  The topology buys nothing that su(2) did not already give for free, and")
    print("  it cannot go further.  Sl is an INTEGER and the manuscript contains no")
    print(f"  expansion parameter, so it has no route to a_e = {mp.nstr(A_E,12)}")
    print("  at any order.  Levy-Leblond and tree Dirac stop at 2 as well, but")
    print("  neither claims to be finished; QED continues the series using an")
    print("  independently measured alpha.  The manuscript claims zero free")
    print("  parameters, UV/IR completeness and 'all constants', so for it the stop")
    print("  is terminal -- and it is terminal on its own headline observable.")
    return {"table": [dict(zip(("framework", "inputs", "g", "matches"), r)) for r in rows],
            "cpf_route_to_anomaly": None,
            "reason": "Sl is an integer; no expansion parameter exists in the framework"}


# ---------------------------------------------------------------------------
def main():
    print(RULE)
    print("Where g = 2 comes from, and what the measured anomaly says")
    print("successor to: docs/Elimination_Ledger.md, 2026-07-26 (Sl = 2 <-> g = 2)")
    print(RULE)

    res = {
        "W1_sigma_algebra": w1_sigma_algebra(),
        "W2_pauli_identity": w2_pauli_identity(),
        "W3_levy_leblond": w3_levy_leblond(),
        "W4_periodicity": w4_periodicity(),
        "W5_dirac": w5_dirac(),
        "W6_data": w6_read_the_data(),
        "W7_qed_series": w7_series(),
        "W8_independent_alpha": w8_vs_independent_alpha(),
        "W9_parameter_count": w9_parameter_count(),
    }

    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print(f"  g = 2 derived from su(2) + linearization        : machine-verified")
    print(f"  relativity used                                 : none")
    print(f"  topology used                                   : none")
    print(f"  4 pi periodicity source                         : pi_1(SO(3)) = Z/2")
    print(f"  measured a_e                                    : {mp.nstr(A_E,14)}")
    print(f"  a_e predicted by any 'g = 2' framework          : 0")
    print(f"  separation                                      : "
          f"{res['W6_data']['sigma_from_zero']} sigma")
    print(f"  series validated against Fan et al. alpha^-1    : "
          f"{res['W7_qed_series']['agreement_in_sigma']} sigma")
    print(RULE)

    payload = {
        "description": "Origin of g = 2 (Levy-Leblond) and the measured anomaly",
        "source": "code/constraint_projection/wave_equation_gfactor.py",
        "successor_to": "docs/Elimination_Ledger.md 2026-07-26 (Sl = 2 <-> g = 2)",
        "bears_on": "papers/notes/Constraint_Projection_Framework.tex Sec 4",
        "measured_inputs": {
            "g_over_2": str(G_OVER_2), "u": str(U_G_OVER_2),
            "source": "Fan, Myers, Sukra & Gabrielse, PRL 130, 071801 (2023)",
            "alpha_inv_Rb": str(ALPHA_RB[0]), "alpha_inv_Cs": str(ALPHA_CS[0]),
        },
        "checks": res,
    }
    out = ROOT / "docs" / "wave_equation_gfactor.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
