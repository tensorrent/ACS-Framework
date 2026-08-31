#!/usr/bin/env python3
# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Can a RELATIVE boundary condition fix alpha where an absolute one cannot?

The gap diagnosis (2026-08-30) closed three routes and ended on a structural
point: a log-in-scale relation derives alpha only if the scale ratio is fixed
from outside the relation, and RG running cannot supply that because it needs a
boundary condition.

The natural follow-on: what if the boundary condition is not a single absolute
value but a RELATION between scales?  That is a real idea -- gauge unification,
dimensional transmutation and fixed points all work that way, none of them fixes
a coupling absolutely.  And the manuscript ALREADY CONTAINS one.

    B1  the framework's own relational condition, and what it predicts
    B2  the decisive test: a relational alpha must DRIFT
    B3  how many relational conditions are there, and do they agree?

Run:  python3 code/constraint_projection/alpha_relational_boundary.py
Deps: mpmath
Artifact: docs/alpha_relational_boundary.json
"""

import json
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
mp.mp.dps = 40

ALPHA_INV = mp.mpf("137.035999177")
HBAR, M_E, C_L = mp.mpf("1.054571817e-34"), mp.mpf("9.1093837015e-31"), mp.mpf("299792458")
R_SPIN = HBAR / (2 * M_E * C_L)
L_IR = mp.mpf("1.3e26")
H0 = mp.mpf("67.4") * 1000 / mp.mpf("3.0856775814913673e22")     # s^-1
YEAR = mp.mpf("3.1557e7")
RULE = "=" * 78


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


def b1_relational():
    head("B1", "The framework's OWN relational condition")
    print("  Sec 8 states  lambda_UV * lambda_IR = 1/R^4  with lambda_UV = 1/a^2 and")
    print("  lambda_IR = 1/L_IR^2, i.e.")
    print("\n        a * L_IR = R^2\n")
    print("  That is a RELATION between the UV cutoff and the IR scale -- not an")
    print("  absolute value for either.  Exactly the shape a relative boundary")
    print("  condition should have.  Substituting a = R^2/L_IR into the corrected")
    print("  alpha relation:")
    print("\n        alpha^-1 = (1/2)( ln(8 R/a) + 1 ) = (1/2)( ln(8 L_IR / R) + 1 )\n")
    print("  alpha is now fixed by the RATIO of the cosmological to the electron")
    print("  scale.  No free parameter survives once L_IR is taken from observation.")
    print("  This is Dirac's large-number structure, and it is a genuine prediction.\n")
    ratio = L_IR / R_SPIN
    pred = (mp.log(8 * ratio) + 1) / 2
    print(f"     L_IR (Hubble radius)   = {mp.nstr(L_IR, 6)} m")
    print(f"     R = hbar/(2 m_e c)     = {mp.nstr(R_SPIN, 6)} m")
    print(f"     L_IR / R               = {mp.nstr(ratio, 6)}   <- the Dirac large number")
    print(f"     alpha^-1 PREDICTED     = {mp.nstr(pred, 8)}")
    print(f"     alpha^-1 observed      = {mp.nstr(ALPHA_INV, 10)}")
    print(f"     off by                 = {mp.nstr(ALPHA_INV / pred, 5)}x")
    need = mp.e ** (2 * ALPHA_INV - 1) / 8
    print(f"\n  Better than 72.6x (tau = i/2) and better than 5.08x (Planck cutoff),")
    print(f"  and unlike those it is PARAMETER-FREE.  The relational move genuinely")
    print(f"  improves the situation -- which is why it deserved testing rather than")
    print(f"  dismissal.  But it is still wrong by a factor of {mp.nstr(ALPHA_INV/pred,4)}, and to reach")
    print(f"  137.036 it would need L_IR/R = {mp.nstr(need,6)} against a measured")
    print(f"  {mp.nstr(ratio,6)} -- off by 10^{mp.nstr(mp.log(need/ratio,10),5)}.")
    return {"condition": "a * L_IR = R^2 (Sec 8)",
            "derived_relation": "alpha^-1 = (1/2)(ln(8 L_IR/R) + 1)",
            "L_IR_over_R": mp.nstr(ratio, 6), "predicted": mp.nstr(pred, 8),
            "observed": mp.nstr(ALPHA_INV, 10), "off_by": mp.nstr(ALPHA_INV / pred, 5),
            "needed_ratio": mp.nstr(need, 6),
            "decades_off": mp.nstr(mp.log(need / ratio, 10), 5)}


def b2_drift():
    head("B2", "The decisive test: a relational alpha must DRIFT")
    print("  If alpha is set by L_IR/R and L_IR grows with cosmic expansion, then")
    print("  alpha is not constant.  That is not a philosophical objection -- it is a")
    print("  measurable consequence, and it is how Dirac-type large-number hypotheses")
    print("  are normally killed.\n")
    d_ainv = H0 * YEAR / 2
    drift = d_ainv / ALPHA_INV
    print(f"     H_0                      = {mp.nstr(H0, 6)} /s = {mp.nstr(H0*YEAR, 6)} /yr")
    print(f"     d(alpha^-1)/dt ~ H_0 / 2 = {mp.nstr(d_ainv, 6)} /yr")
    print(f"     |alpha_dot / alpha|      = {mp.nstr(drift, 6)} /yr\n")
    bounds = [("atomic clocks, Al+/Hg+, Yb+", mp.mpf("2e-17")),
              ("Oklo natural reactor (2 Gyr)", mp.mpf("1.2e-17")),
              ("quasar absorption systems", mp.mpf("1e-16"))]
    print(f"  {'observational bound on |alpha_dot/alpha| [/yr]':>46} {'bound':>9} {'exceeded':>11}")
    rows = []
    for n, b in bounds:
        rows.append({"bound": n, "value": mp.nstr(b, 2), "exceeded_by": mp.nstr(drift / b, 5)})
        print(f"  {n:>46} {mp.nstr(b,2):>9} {mp.nstr(drift/b,5):>11}x")
    print(f"\n  EXCLUDED by roughly four orders of magnitude against every independent")
    print(f"  bound.  The relational reading does not merely mispredict alpha's VALUE;")
    print(f"  it predicts alpha VARIES, and that is ruled out on its own.")
    print(f"\n  Prior art (searched before claiming, rule 4): using alpha-constancy to")
    print(f"  constrain varying-alpha models is a standard and well-developed method;")
    print(f"  the Oklo and atomic-clock bounds above are the field's own. Nothing in")
    print(f"  the METHOD is ours -- only its application to this framework.")
    return {"predicted_drift_per_year": mp.nstr(drift, 6),
            "d_alpha_inv_dt_per_year": mp.nstr(d_ainv, 6), "bounds": rows,
            "verdict": "EXCLUDED by ~1e4 against every independent bound",
            "method_is_novel": False}


def b3_count():
    head("B3", "How many relational conditions are there, and do they agree?")
    print("  A relative boundary condition helps only if it imposes MORE constraints")
    print("  than it introduces unknowns.  Count what the manuscript actually has:\n")
    conds = [("tau = i a/R = i/2", "Sec 3", mp.mpf(1) / 2),
             ("a L_IR = R^2, L_IR observed", "Sec 8", R_SPIN / L_IR)]
    print(f"  {'condition':>32} {'source':>8} {'a/R':>14} {'alpha^-1':>10}")
    rows = []
    for nm, src, r in conds:
        ai = (mp.log(8 / r) + 1) / 2
        rows.append({"condition": nm, "source": src, "a_over_R": mp.nstr(r, 6),
                     "alpha_inv": mp.nstr(ai, 7)})
        print(f"  {nm:>32} {src:>8} {mp.nstr(r,6):>14} {mp.nstr(ai,7):>10}")
    a1 = (mp.log(8 / conds[0][2]) + 1) / 2
    a2 = (mp.log(8 / conds[1][2]) + 1) / 2
    print(f"\n  TWO independent relational conditions, in the same manuscript, giving")
    print(f"  {mp.nstr(a1,7)} and {mp.nstr(a2,7)}.  Neither gives 137.036, and they disagree")
    print(f"  with each other by {mp.nstr(a2/a1,5)}x.")
    print(f"\n  THIS IS THE DEEP POINT.  A relative boundary condition does not rescue")
    print(f"  the framework -- it makes it OVER-DETERMINED AND INCONSISTENT, which is")
    print(f"  strictly worse than under-determined.  Under-determination is a missing")
    print(f"  input you can go and find.  Over-determination with disagreement means")
    print(f"  the framework's own conditions contradict each other, and there is no")
    print(f"  free parameter left to absorb the difference.")
    return {"conditions": rows, "disagreement_factor": mp.nstr(a2 / a1, 5),
            "verdict": "over-determined and inconsistent -- worse than under-determined"}


def main():
    print(RULE)
    print("CAN A RELATIVE BOUNDARY CONDITION FIX ALPHA?")
    print(RULE)
    res = {"B1_relational_condition": b1_relational(), "B2_drift_test": b2_drift(),
           "B3_condition_count": b3_count()}
    print(f"\n{RULE}\nANSWER\n{RULE}")
    print("  The instinct was right in TWO ways and still does not save it.")
    print()
    print("  RIGHT (1): the boundary condition should be relative, not absolute.")
    print("             Gauge unification, dimensional transmutation and fixed points")
    print("             all work that way.")
    print("  RIGHT (2): the framework already HAS one -- Sec 8's a * L_IR = R^2 -- and")
    print("             using it removes the free parameter entirely, turning alpha")
    print("             into a genuine prediction: alpha^-1 = 46.24, off by 2.96x.")
    print("             That is a real improvement on 72.6x, and parameter-free.")
    print()
    print("  BUT: (a) 46.24 is still wrong by 3x; (b) the relational reading predicts")
    print("       alpha DRIFTS at 2.5e-13/yr, excluded by ~1e4 against atomic clocks,")
    print("       Oklo and quasars; and (c) the manuscript's TWO relational conditions")
    print("       disagree with each other by 24.5x, leaving it over-determined and")
    print("       inconsistent -- strictly worse than having a free parameter.")
    print(RULE)
    out = ROOT / "docs" / "alpha_relational_boundary.json"
    out.write_text(json.dumps({
        "description": "Can a relative boundary condition fix alpha?",
        "source": "code/constraint_projection/alpha_relational_boundary.py",
        "checks": res}, indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
