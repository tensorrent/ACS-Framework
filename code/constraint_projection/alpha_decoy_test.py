#!/usr/bin/env python3
# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Decoy test on the CPF manuscript's alpha match -- this corpus's own discipline,
applied to the CPF audit for the first time.

The coherence audit of 2026-08-30 found that four CPF instruments (~1,900 lines)
used NONE of this program's own method devices.  The decoy discipline was the one
genuine gap: precedent is the T_min height floor, where decoy floors (2*pi*e*phi,
(2*pi*e)^2/10, 2*pi*e/1.5) were tested and only 2*pi*e gave a vanishing main term,
which is what made 2*pi*e privileged rather than merely fitted.

The manuscript's headline: alpha^-1 = ln(8R/a) + 1 = 137.035999171, "matching
CODATA 2022 to within 6e-9".  The existing kill (cpf_audit.py C1, C2) shows the
step is circular.  This states the same result the corpus's own way -- by asking
whether the match is PRIVILEGED, i.e. whether a decoy family fails where the
manuscript's form succeeds.

    D1  decoy family: do other 'geometric' log-forms hit CODATA equally well?
    D2  information content: how many bits does the match actually carry?
    D3  achievable precision: is 6e-9 impressive, or arithmetic-limited?
    D4  the parameter-free version: what does the theory predict with NO free knob?
    D5  refraction check, in the ledger's own vocabulary

Run:  python3 code/constraint_projection/alpha_decoy_test.py
Deps: mpmath
Artifact: docs/alpha_decoy_test.json
"""

import json
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
mp.mp.dps = 60

ALPHA_INV = mp.mpf("137.035999177")          # CODATA 2022
HBAR, M_E, C_L = mp.mpf("1.054571817e-34"), mp.mpf("9.1093837015e-31"), mp.mpf("299792458")
R_SPIN = HBAR / (2 * M_E * C_L)
RULE = "=" * 78


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


# --- the decoy family -------------------------------------------------------
# Each entry: (label, alpha_inv as a function of r = a/R, solved cutoff r*).
# All are "geometric-looking" capacitance/inductance forms of the same species as
# the manuscript's.  A privileged form would be one where only IT can hit the target.
FAMILY = [
    ("manuscript, as written:  ln(8/r) + 1",         lambda r: mp.log(8 / r) + 1),
    ("manuscript, corrected:  (ln(8/r) + 1)/2",      lambda r: (mp.log(8 / r) + 1) / 2),
    ("Kelvin-Maxwell ring:    (ln(8/r) - 7/4)/2",    lambda r: (mp.log(8 / r) - mp.mpf(7) / 4) / 2),
    ("external-inductance:    (ln(8/r) - 2)/2",      lambda r: (mp.log(8 / r) - 2) / 2),
    ("thin-ring capacitance:  ln(8/r)",              lambda r: mp.log(8 / r)),
    ("no additive constant:   ln(8/r)/2",            lambda r: mp.log(8 / r) / 2),
    ("different log argument: ln(4/r) + 1",          lambda r: mp.log(4 / r) + 1),
    ("different log argument: ln(16/r) + 1",         lambda r: mp.log(16 / r) + 1),
    ("bare ratio:             ln(1/r)",              lambda r: mp.log(1 / r)),
    ("pi-flavoured:           ln(8/r) + pi/2",       lambda r: mp.log(8 / r) + mp.pi / 2),
    ("Euler-flavoured:        ln(8/r) + euler",      lambda r: mp.log(8 / r) + mp.euler),
    ("quadratic in the log:   sqrt(ln(8/r)^2 + 1)",  lambda r: mp.sqrt(mp.log(8 / r) ** 2 + 1)),
    ("log-of-log correction:  ln(8/r) + ln(ln(8/r))",
     lambda r: mp.log(8 / r) + mp.log(mp.log(8 / r))),
    ("power form:             (8/r)^(1/60)",         lambda r: (8 / r) ** (mp.mpf(1) / 60)),
]


def solve_cutoff(f, target=None):
    """Find r = a/R reproducing the target exactly.

    Solutions sit at r ~ 1e-59 to 1e-300, so root-finding in r is hopelessly
    ill-conditioned.  Substitute r = exp(-t) and bisect in t, where every form in
    the family is smooth and monotone over t in [0, 2000].  Bisection needs only a
    sign change, so it cannot be defeated by scale.
    """
    tgt = ALPHA_INV if target is None else target
    g = lambda t: f(mp.e ** (-t)) - tgt
    lo, hi = mp.mpf("1e-6"), mp.mpf(2000)
    try:
        glo, ghi = g(lo), g(hi)
    except Exception:
        return None
    if glo * ghi > 0:
        return None                      # no sign change -> genuinely unreachable
    for _ in range(400):
        mid = (lo + hi) / 2
        try:
            gm = g(mid)
        except Exception:
            return None
        if glo * gm <= 0:
            hi, ghi = mid, gm
        else:
            lo, glo = mid, gm
    return mp.e ** (-(lo + hi) / 2)


def d1_decoys():
    head("D1", "Decoy family: is the manuscript's form privileged?")
    print("  For each candidate, solve for the cutoff r = a/R that reproduces CODATA")
    print("  alpha^-1 = 137.035999177 EXACTLY.  A privileged form is one where only it")
    print("  can hit the target; a fitted form is one where everything can.\n")
    print(f"  {'form':<42} {'solved a/R':>16} {'|residual|':>12}")
    rows, hits = [], 0
    for label, f in FAMILY:
        r = solve_cutoff(f)
        if r is None or r <= 0:
            rows.append({"form": label, "cutoff": None, "residual": None, "hits": False})
            print(f"  {label:<42} {'no solution':>16} {'-':>12}")
            continue
        res = abs(f(r) - ALPHA_INV)
        ok = res < mp.mpf("1e-25")
        hits += ok
        rows.append({"form": label, "cutoff": mp.nstr(r, 8),
                     "residual": mp.nstr(res, 3), "hits": bool(ok)})
        print(f"  {label:<42} {mp.nstr(r,6):>16} {mp.nstr(res,3):>12}")
    frac = hits / len(FAMILY)
    print(f"\n  {hits} of {len(FAMILY)} forms reproduce CODATA to < 1e-25 "
          f"({100*frac:.0f}% of the family).")
    if hits <= 1:
        print(f"  The manuscript's form IS privileged -- the decoys fail where it succeeds.")
    else:
        print(f"  The manuscript's form is NOT privileged: {hits} distinct forms hit the")
        print(f"  same target once each is allowed its own free cutoff.  Contrast the")
        print(f"  T_min precedent, where only 2*pi*e gave a vanishing main term and the")
        print(f"  decoys did not -- there the decoy test SEPARATED, here it does not.")
    return {"rows": rows, "hits": hits, "family_size": len(FAMILY),
            "privileged": hits <= 1}


def d2_bits():
    head("D2", "Information content of the match")
    print("  A match is evidence only if it could have failed.  Here the model is")
    print("      alpha^-1 = F(a/R)   with a/R FREE and F continuous and monotone.")
    print("  For any such F, r |-> F(r) is a bijection onto its range, so a solution")
    print("  exists for EVERY target in that range.  The set of targets the model can")
    print("  reproduce is therefore the whole range -- it excludes nothing.\n")
    f = FAMILY[0][1]
    print(f"  {'arbitrary target':>20} {'solved a/R':>18} {'F(r*) recovered':>20}")
    for tgt in ["137.035999177", "42", "1", "1000"]:
        t = mp.mpf(tgt)
        r = solve_cutoff(f, t)
        if r is None:
            print(f"  {tgt:>20} {'unreachable':>18} {'-':>20}")
        else:
            print(f"  {tgt:>20} {mp.nstr(r,6):>18} {mp.nstr(f(r),12):>20}")
    print(f"\n  parameters fitted : 1  (the cutoff a/R)")
    print(f"  targets matched   : 1  (alpha^-1)")
    print(f"  residual DOF      : 0")
    print(f"  bits carried      : 0   -- a 1-parameter fit to 1 datum is an identity,")
    print(f"                          not a prediction.  Nothing was risked.")
    return {"parameters": 1, "targets": 1, "residual_dof": 0, "bits": 0}


def d3_precision():
    head("D3", "Is 6e-9 impressive, or arithmetic-limited?")
    print("  The manuscript reports agreement 'to within 6e-9' as though the precision")
    print("  were a result.  But the cutoff is solved for, so the achievable agreement")
    print("  is limited only by the arithmetic used.\n")
    f = FAMILY[0][1]
    print(f"  {'working precision':>18} {'|alpha^-1(fit) - CODATA|':>28}")
    rows = []
    for dps in [15, 30, 50, 80]:
        old = mp.mp.dps
        mp.mp.dps = dps
        r = 8 * mp.e ** (1 - ALPHA_INV)      # closed form for the manuscript's F
        got = abs((mp.log(8 / r) + 1) - ALPHA_INV)
        mp.mp.dps = old
        rows.append({"dps": dps, "residual": mp.nstr(got, 3)})
        print(f"  {str(dps)+' digits':>18} {mp.nstr(got,3):>28}")
    print(f"\n  The residual tracks the working precision, not the physics.  6e-9 is")
    print(f"  the manuscript's rounding of its own quoted cutoff, not a measurement of")
    print(f"  agreement.  Quoting more digits of a/R would 'improve' it without limit.")
    return {"rows": rows}


def d4_parameter_free():
    head("D4", "What does the theory predict with NO free knob?")
    print("  The manuscript claims ZERO free parameters.  Take that seriously: the only")
    print("  place it fixes a/R independently of alpha is the modular condition")
    print("  tau = i*a/R = i/2, i.e. a/R = 1/2.  Then alpha^-1 is PREDICTED:\n")
    r = mp.mpf(1) / 2
    ms, corr = mp.log(8 / r) + 1, (mp.log(8 / r) + 1) / 2
    print(f"     a/R = 1/2  ->  alpha^-1 (manuscript's relation) = {mp.nstr(ms,10)}")
    print(f"                ->  alpha^-1 (corrected relation)    = {mp.nstr(corr,10)}")
    print(f"     observed                                        = {mp.nstr(ALPHA_INV,12)}")
    print(f"     ratio observed/predicted (corrected)            = {mp.nstr(ALPHA_INV/corr,6)}x")
    print(f"\n  So the ONLY parameter-free version of the theory predicts alpha^-1 = "
          f"{mp.nstr(corr,6)},")
    print(f"  wrong by a factor of {mp.nstr(ALPHA_INV/corr,4)}.  The 137.036 is obtained by")
    print(f"  abandoning that condition and fitting the cutoff instead.  Those are the")
    print(f"  two options and the manuscript reports both, five lines apart.")
    return {"a_over_R": "1/2", "predicted_manuscript": mp.nstr(ms, 10),
            "predicted_corrected": mp.nstr(corr, 10),
            "observed": mp.nstr(ALPHA_INV, 12),
            "factor_off": mp.nstr(ALPHA_INV / corr, 6)}


def d5_refraction():
    head("D5", "Refraction test, in this ledger's own vocabulary")
    print("  Kill-criterion (Elimination Ledger, engine section): a quantity is a")
    print("  REFRACTION if its value moves under a legitimate change of instrument")
    print("  (representation / normalization / convention / scale / window); it is an")
    print("  INVARIANT (candidate) if it does not.\n")
    r = mp.mpf("0.05")
    print(f"  Instrument swap at fixed geometry a/R = {r} (repo's recorded demo run):")
    print(f"     annulus model      alpha^-1 = 3.037587")
    print(f"     conformal model    alpha^-1 = 1.692054")
    print(f"     BIE (Moebius)      alpha^-1 = 0.372688")
    print(f"     -> value moves by ~8x across legitimate models of the SAME geometry")
    print(f"\n  Convention swap at fixed model (the additive constant):")
    base = (mp.log(8 / r) + 1) / 2
    for c, name in [(1, "+1 (manuscript)"), (mp.mpf(-7) / 4, "-7/4 (Kelvin-Maxwell)"),
                    (-2, "-2 (external L)"), (0, "0 (thin-ring C)")]:
        v = (mp.log(8 / r) + c) / 2
        print(f"     constant {name:<24} alpha^-1 = {mp.nstr(v,8)}")
    print(f"     -> d(alpha^-1)/d(constant) = 1/2 exactly; +1 -> -7/4 shifts it by 11/8")
    print(f"\n  VERDICT: the manuscript's alpha^-1 is a REFRACTION, not an invariant.")
    print(f"  This is the corpus's own vocabulary for precisely this situation, and the")
    print(f"  CPF audit re-derived the device (C2's four-cutoff table) without citing it.")
    return {"model_swap_spread": "~8x at a/R = 0.05",
            "d_alpha_d_constant": "1/2 exactly",
            "verdict": "REFRACTION"}


def main():
    print(RULE)
    print("DECOY TEST on the CPF manuscript's alpha match")
    print("first application of this corpus's decoy discipline to the CPF audit")
    print(RULE)
    res = {"D1_decoy_family": d1_decoys(), "D2_information": d2_bits(),
           "D3_precision": d3_precision(), "D4_parameter_free": d4_parameter_free(),
           "D5_refraction": d5_refraction()}
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print(f"  decoy forms also hitting CODATA : "
          f"{res['D1_decoy_family']['hits']} of {res['D1_decoy_family']['family_size']}")
    print(f"  form privileged?                : {res['D1_decoy_family']['privileged']}")
    print(f"  bits carried by the match       : 0")
    print(f"  parameter-free prediction       : alpha^-1 = "
          f"{res['D4_parameter_free']['predicted_corrected']} "
          f"({res['D4_parameter_free']['factor_off']}x off)")
    print(f"  kill-criterion verdict          : {res['D5_refraction']['verdict']}")
    print(f"\n  The existing circularity kill (C1/C2) was correct.  The decoy framing")
    print(f"  states its STRENGTH rather than only its failure mode: the match is not")
    print(f"  merely circular, it is uninformative -- no member of a 14-form decoy")
    print(f"  family fails where the manuscript's form succeeds.")
    print(RULE)
    out = ROOT / "docs" / "alpha_decoy_test.json"
    out.write_text(json.dumps({
        "description": "Decoy test on the CPF alpha match (repo-native discipline)",
        "source": "code/constraint_projection/alpha_decoy_test.py",
        "precedent": "docs/Elimination_Ledger.md 2026-06-06, T_min height floor decoys",
        "checks": res}, indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
