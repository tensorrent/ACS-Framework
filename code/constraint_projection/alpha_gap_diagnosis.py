#!/usr/bin/env python3
# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
If the alpha gap is not a power law, what IS it, and can it be corrected?

The scaling test (2026-08-30) ruled out a missing power law on five grounds.
That rules out a SPECIES of correction, which narrows the question rather than
closing it.  This diagnoses what the gap actually is and tests every route to
closing it.

    G1  the natural variable    the gap is ADDITIVE in the log, not multiplicative
    G2  physical cutoffs        what does each defensible scale actually give?
    G3  the prefactor           can a legitimate (kappa, eta) close it?
    G4  the shape               log-in-scale IS the shape of RG running -- compare
    G5  the general no-go       and its prior art

Run:  python3 code/constraint_projection/alpha_gap_diagnosis.py
Deps: mpmath
Artifact: docs/alpha_gap_diagnosis.json
"""

import json
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
mp.mp.dps = 40

ALPHA_INV = mp.mpf("137.035999177")
HBAR, M_E, C_L = mp.mpf("1.054571817e-34"), mp.mpf("9.1093837015e-31"), mp.mpf("299792458")
R_SPIN = HBAR / (2 * M_E * C_L)
L_PLANCK = mp.mpf("1.616255e-35")
RULE = "=" * 78


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


def L_of(r):
    return mp.log(8 / r) + 1


def g1_natural_variable():
    head("G1", "The gap is ADDITIVE in the log, not multiplicative")
    print("  alpha^-1 = (1/2)(ln(8R/a) + 1) = L/2 is LINEAR IN A LOGARITHM, so the")
    print("  honest variable is L -- not the ratio of alpha^-1 values.\n")
    L_tau, L_need = L_of(mp.mpf(1) / 2), 2 * ALPHA_INV
    gap = L_need - L_tau
    print(f"     L from tau = i/2     = {mp.nstr(L_tau, 10)}")
    print(f"     L needed for CODATA  = {mp.nstr(L_need, 10)}")
    print(f"     ADDITIVE gap in L    = {mp.nstr(gap, 10)}")
    print(f"     -> a/R must shrink by e^{mp.nstr(gap,7)} = "
          f"10^{mp.nstr(gap/mp.log(10),6)}")
    print(f"\n  THIS is why no power law fit.  A power law is alpha^-1 ~ L^p; the actual")
    print(f"  requirement is L -> L + 270.  Wrong species of correction entirely -- the")
    print(f"  scaling test was testing the wrong shape, and said so.")
    return {"L_from_tau": mp.nstr(L_tau, 10), "L_needed": mp.nstr(L_need, 10),
            "additive_gap": mp.nstr(gap, 10), "decades": mp.nstr(gap / mp.log(10), 6),
            "verdict": "additive in log, not multiplicative"}


def g2_physical_cutoffs():
    head("G2", "What does each physically defensible cutoff give?")
    print("  The model needs an independent scale.  Try the ones physics offers:\n")
    print(f"  {'cutoff a':>26} {'a/R':>14} {'L':>10} {'alpha^-1':>10} {'off by':>9}")
    rows = []
    cands = [("Planck length", L_PLANCK),
             ("classical electron radius", mp.mpf("2.8179403262e-15")),
             ("proton charge radius", mp.mpf("8.4e-16")),
             ("R itself (a = R)", R_SPIN),
             ("tau = i/2  (a = R/2)", R_SPIN / 2),
             ("CODATA-matching", R_SPIN * 8 * mp.e ** (1 - 2 * ALPHA_INV))]
    for name, a in cands:
        r = a / R_SPIN
        L = L_of(r)
        ai = L / 2
        rows.append({"cutoff": name, "a_over_R": mp.nstr(r, 5), "L": mp.nstr(L, 6),
                     "alpha_inv": mp.nstr(ai, 6), "off_by": mp.nstr(ALPHA_INV / ai, 4)})
        print(f"  {name:>26} {mp.nstr(r,5):>14} {mp.nstr(L,6):>10} "
              f"{mp.nstr(ai,6):>10} {mp.nstr(ALPHA_INV/ai,4):>9}x")
    planck_ratio = ALPHA_INV / (L_of(L_PLANCK / R_SPIN) / 2)
    print(f"\n  The Planck cutoff -- the most defensible physical choice -- gives")
    print(f"  alpha^-1 = 26.96, off by {mp.nstr(planck_ratio,4)}x, NOT 72.6x.  So '72.6' was")
    print(f"  never a property of the theory; it is a property of choosing a/R = 1/2.")
    print(f"  Same finding as the tau sweep, now in physical rather than modular terms.")
    codata_a = R_SPIN * 8 * mp.e ** (1 - 2 * ALPHA_INV)
    print(f"\n  The CODATA-matching cutoff is {mp.nstr(codata_a/L_PLANCK,4)} Planck lengths.")
    print(f"  That is not a cutoff.  A 'UV completion' 96 decades below the Planck")
    print(f"  scale is not a short-distance regulator, it is an unphysical number.")
    return {"rows": rows, "planck_alpha_inv": mp.nstr(L_of(L_PLANCK / R_SPIN) / 2, 6),
            "planck_off_by": mp.nstr(planck_ratio, 4),
            "codata_cutoff_in_planck_lengths": mp.nstr(codata_a / L_PLANCK, 4),
            "verdict": "the gap is whatever scale you pick"}


def g3_prefactor():
    head("G3", "Can a legitimate prefactor close it?")
    print("  General form: charge q = eta*e, capacitance C = kappa*eps0*R/L.")
    print("  Redoing the self-energy match with both free:\n")
    print("     E = q^2/(2C) = eta^2 e^2 L / (2 kappa eps0 R),  R = hbar/(2 m_e c)")
    print("     => alpha^-1 = (4 pi eta^2 / kappa) * L")
    print(f"     check: kappa = 2 pi, eta = 1/2 -> 4 pi (1/4)/(2 pi) = 1/2   OK\n")
    L_p = L_of(L_PLANCK / R_SPIN)
    need = ALPHA_INV / L_p
    print(f"  At the Planck cutoff (L = {mp.nstr(L_p,6)}), matching CODATA needs")
    print(f"     4 pi eta^2 / kappa = {mp.nstr(need,6)}\n")
    print(f"  {'kappa':>22} {'required eta^2':>16} {'required eta':>14} {'natural?':>10}")
    rows = []
    natural = {mp.mpf(1), mp.mpf(1) / 2, mp.mpf(1) / 3, mp.mpf(2) / 3, mp.mpf(2)}
    for kn, kv in [("2 pi (manuscript)", 2 * mp.pi), ("4 pi^2 (thin ring)", 4 * mp.pi ** 2),
                   ("4 pi", 4 * mp.pi), ("1", mp.mpf(1))]:
        e2 = need * kv / (4 * mp.pi)
        e_ = mp.sqrt(e2)
        ok = any(abs(e_ - n) < mp.mpf("1e-3") for n in natural)
        rows.append({"kappa": kn, "eta2": mp.nstr(e2, 6), "eta": mp.nstr(e_, 6),
                     "natural": bool(ok)})
        print(f"  {kn:>22} {mp.nstr(e2,6):>16} {mp.nstr(e_,6):>14} {str(ok):>10}")
    print(f"\n  Natural charge fractions are 1, 1/2, 1/3, 2/3, 2.  None of the required")
    print(f"  eta values is one of them.  The prefactor cannot be repaired by any")
    print(f"  defensible charge split or capacitance normalisation.  Route CLOSED.")
    return {"required_4pi_eta2_over_kappa": mp.nstr(need, 6), "rows": rows,
            "verdict": "no natural (kappa, eta) closes it"}


def g4_rg_shape():
    head("G4", "What shape IS it?  log-in-scale is the shape of RG running")
    print("  A relation linear in ln(scale) is exactly the form of a running coupling.")
    print("  So the manuscript has the right FUNCTIONAL FORM -- for the wrong reason.")
    print("  Compare the coefficients.  QED one-loop, one Dirac fermion, unit charge:\n")
    beta = 2 / (3 * mp.pi)
    ms = mp.mpf(1) / 2
    print(f"     QED:         d(alpha^-1)/d ln(mu)  = -2/(3 pi) = {mp.nstr(-beta,8)}")
    print(f"     manuscript:  d(alpha^-1)/d ln(R/a) = +1/2      = {mp.nstr(ms,8)}")
    print(f"\n     magnitude ratio = {mp.nstr(ms/beta,7)}")
    print(f"     signs           = OPPOSITE")
    print(f"\n  (The ratio equals 3 pi/4 = {mp.nstr(3*mp.pi/4,7)}, but that is just the")
    print(f"  arithmetic of the two coefficients, not a finding.  Recorded so it is not")
    print(f"  misread -- same trap as sqrt(5277) in the decoy test.)")
    print(f"\n  THE SIGN IS THE FATAL PART.  QED SCREENS: alpha^-1 DECREASES toward short")
    print(f"  distance, because vacuum polarisation shields the bare charge.  The")
    print(f"  manuscript's relation INCREASES -- anti-screening in a U(1) theory, which")
    print(f"  is backwards.  Asymptotic freedom is a non-abelian phenomenon.")
    return {"qed_coefficient": mp.nstr(-beta, 8), "manuscript_coefficient": mp.nstr(ms, 8),
            "magnitude_ratio": mp.nstr(ms / beta, 7), "signs": "opposite",
            "verdict": "right functional form, wrong coefficient, wrong sign"}


def g5_no_go():
    head("G5", "The general no-go -- and its prior art")
    print("  The formula's shape admits exactly two readings, and both are closed:\n")
    print("  (a) A SELF-ENERGY WITH A FIXED CUTOFF.  This CAN produce a number -- but")
    print("      only once the cutoff is fixed independently.  The framework's own")
    print("      independent fixing (tau = i/2) gives alpha^-1 = 1.886.  G2 shows every")
    print("      other defensible scale gives 1.5 to 27.  None gives 137.")
    print("\n  (b) RG RUNNING.  This CANNOT derive alpha at all: running relates alpha at")
    print("      two scales and requires a renormalisation condition -- a boundary")
    print("      value -- at one of them.  It never produces alpha from nothing.")
    print("\n  So the honest statement is not 'the gap needs correcting' but 'a")
    print("  log-in-scale relation derives alpha only if the scale ratio is fixed from")
    print("  OUTSIDE the relation'.  The manuscript fixes it two incompatible ways and")
    print("  reports both, five lines apart.")
    print("\n  PRIOR ART -- searched BEFORE claiming this time (rule 4).  The general")
    print("  statement is STANDARD, not ours:")
    print("   * dimensional transmutation is the established name for trading a")
    print("     dimensionless coupling for a scale (Coleman-Weinberg; Lambda_QCD);")
    print("   * RG renormalisation conditions as required boundary data are textbook;")
    print("   * the position that dimensionless constants must be MEASURED, not")
    print("     derived, is the mainstream one.")
    print("\n  And the whole GENRE has a survey: 'Attempts at a determination of the")
    print("  fine-structure constant from first principles: A brief historical")
    print("  overview' (arXiv:1411.4673).  It covers Eddington (136, then 137) and")
    print("  Wyler (1/137.03608).")
    print("\n  THE SHARPEST POINT IN THAT LITERATURE, for our purposes:")
    wyler = mp.mpf("137.03608")
    manuscript = mp.mpf("137.035999171")
    rw = abs(wyler - ALPHA_INV) / ALPHA_INV
    rm = abs(manuscript - ALPHA_INV) / ALPHA_INV
    print(f"     Wyler 1970:     alpha^-1 = {wyler}      rel err {mp.nstr(rw,3)}")
    print(f"     this manuscript: alpha^-1 = {manuscript}  rel err {mp.nstr(rm,3)}")
    print(f"\n     The manuscript is {mp.nstr(rw/rm,5)}x CLOSER than Wyler.")
    print(f"     Wyler's match was good enough to attract serious attention in 1971,")
    print(f"     and was still debunked.  This one is four orders of magnitude better")
    print(f"     -- and by the decoy result carries ZERO bits.")
    print(f"\n  That is the decoy lesson as history rather than arithmetic: closer")
    print(f"  agreement is not better evidence.  More digits of agreement only means")
    print(f"  more digits were fitted, when the construction can hit any target.")
    return {"reading_a": "self-energy with fixed cutoff -> framework's own fixing gives 1.886",
            "reading_b": "RG running -> cannot derive alpha, needs a boundary condition",
            "general_no_go_is_novel": False,
            "prior_art": ["dimensional transmutation (Coleman-Weinberg)",
                          "RG renormalisation condition as boundary data (textbook)",
                          "arXiv:1411.4673 survey of first-principles alpha attempts",
                          "Wyler 1970: alpha^-1 = 137.03608, closer than this manuscript, debunked"],
            "wyler_rel_err": mp.nstr(abs(mp.mpf("137.03608") - ALPHA_INV) / ALPHA_INV, 3),
            "manuscript_rel_err": mp.nstr(abs(mp.mpf("137.035999171") - ALPHA_INV) / ALPHA_INV, 3),
            "manuscript_closer_than_wyler_by": mp.nstr(
                (abs(mp.mpf("137.03608") - ALPHA_INV)) / (abs(mp.mpf("137.035999171") - ALPHA_INV)), 5),
            "verdict": "diagnosis is ours; the general no-go is standard"}


def main():
    print(RULE)
    print("WHAT THE ALPHA GAP ACTUALLY IS, AND WHETHER IT CAN BE CORRECTED")
    print(RULE)
    res = {"G1_natural_variable": g1_natural_variable(),
           "G2_physical_cutoffs": g2_physical_cutoffs(),
           "G3_prefactor": g3_prefactor(),
           "G4_rg_shape": g4_rg_shape(),
           "G5_no_go": g5_no_go()}
    print(f"\n{RULE}\nANSWER\n{RULE}")
    print("  WHAT IT IS: an additive-in-log discrepancy of 270 in L (10^117 in a/R),")
    print("  not a multiplicative factor.  The '72.6x' was an artifact of choosing")
    print("  a/R = 1/2; the Planck cutoff gives 5.08x and a = R gives 89x.")
    print()
    print("  CAN IT BE CORRECTED:  no, by three closed routes --")
    print("    * move the cutoff  -> needs 2.4e-96 Planck lengths, unphysical")
    print("    * fix the prefactor -> no natural (kappa, eta) works")
    print("    * read it as running -> wrong sign (U(1) screens), wrong coefficient,")
    print("      and running cannot derive alpha at all without a boundary condition")
    print()
    print("  The correct move is not to repair the gap but to report the prediction:")
    print("  the framework, taken with its own scale-fixing, predicts alpha^-1 = 1.886")
    print("  and is falsified.  That IS the corrected result.")
    print(RULE)
    out = ROOT / "docs" / "alpha_gap_diagnosis.json"
    out.write_text(json.dumps({
        "description": "What the alpha gap is, and whether it can be corrected",
        "source": "code/constraint_projection/alpha_gap_diagnosis.py",
        "checks": res}, indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
