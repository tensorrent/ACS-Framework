#!/usr/bin/env python3
# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
Is the 72.648x alpha discrepancy a SCALING RULE or an artifact of one choice?

The decoy test (2026-08-30) found that taking the manuscript's zero-free-parameter
claim seriously -- fixing a/R = 1/2 from the modular condition tau = i a/R = i/2 --
PREDICTS alpha^-1 = 1.886 against an observed 137.036, a factor of 72.648.

A fair hypothesis: that factor may not be noise.  If it is a systematic scaling,
the framework would be right in form and merely missing a power law.  That is a
real possibility and it is testable, because a rule and an artifact make DIFFERENT
predictions:

    a RULE      is a property of the theory -> constant under convention changes,
                and it shows up wherever the theory meets data
    an ARTIFACT is a property of one arbitrary choice -> moves when the choice moves

    S1  convention-invariance   does the factor survive a change of tau?
    S2  closed form (decoys)    is 72.648 a recognisable constant, or is the
                                neighbourhood dense with equally good decoys?
    S3  cross-observable        does the SAME factor explain the manuscript's
                                other failed predictions (L_IR, g)?
    S4  instrument reconciliation  is there ANY (K, p) with alpha^-1 = K*X^p that
                                reconciles the three independent capacitance models?
    S5  degrees of freedom      can a 2-parameter power law even be tested here?

Run:  python3 code/constraint_projection/alpha_scaling_test.py
Deps: mpmath
Artifact: docs/alpha_scaling_test.json
"""

import json
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
mp.mp.dps = 40

ALPHA_INV = mp.mpf("137.035999177")
HBAR, M_E, C_L = mp.mpf("1.054571817e-34"), mp.mpf("9.1093837015e-31"), mp.mpf("299792458")
R_SPIN = HBAR / (2 * M_E * C_L)
RULE = "=" * 78


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


def L_of(r):
    """The manuscript's log factor at aspect ratio r = a/R."""
    return mp.log(8 / r) + 1


def s1_convention():
    head("S1", "Convention-invariance: does the factor survive a change of tau?")
    print("  tau = i a/R is a modelling choice.  A scaling RULE is a property of the")
    print("  theory and cannot move when a convention moves.  Sweep the natural values:\n")
    print(f"  {'tau':>6} {'a/R':>8} {'L':>12} {'pred a^-1':>12} {'RATIO':>12} "
          f"{'exponent p':>12}")
    rows = []
    for name, r in [("i/4", mp.mpf(1) / 4), ("i/3", mp.mpf(1) / 3), ("i/2", mp.mpf(1) / 2),
                    ("i", mp.mpf(1)), ("2i", mp.mpf(2)), ("3i", mp.mpf(3))]:
        L = L_of(r)
        pred = L / 2
        ratio = ALPHA_INV / pred
        p = mp.log(ALPHA_INV) / mp.log(L)
        rows.append({"tau": name, "a_over_R": mp.nstr(r, 6), "L": mp.nstr(L, 8),
                     "pred": mp.nstr(pred, 8), "ratio": mp.nstr(ratio, 8),
                     "exponent": mp.nstr(p, 7)})
        print(f"  {name:>6} {mp.nstr(r,4):>8} {mp.nstr(L,8):>12} {mp.nstr(pred,8):>12} "
              f"{mp.nstr(ratio,8):>12} {mp.nstr(p,7):>12}")
    spread = mp.mpf(rows[-1]["ratio"]) / mp.mpf(rows[0]["ratio"])
    print(f"\n  ratio spans {rows[0]['ratio']} -> {rows[-1]['ratio']}  "
          f"({mp.nstr(spread,4)}x across the sweep)")
    print(f"  exponent spans {rows[0]['exponent']} -> {rows[-1]['exponent']}")
    print("\n  Both move continuously with the convention.  Neither is a constant of the")
    print("  theory.  Note also that the ratio is NOT independent data: it is defined as")
    print("  alpha^-1 / (L/2), so it carries exactly the information alpha^-1 already")
    print("  carries, and nothing more.  S1 FAILS the rule hypothesis.")
    return {"rows": rows, "ratio_spread": mp.nstr(spread, 5),
            "verdict": "moves with convention -> artifact"}


def s2_closed_form():
    head("S2", "Is 72.648 a recognisable constant?  (decoy discipline)")
    tgt = ALPHA_INV / (L_of(mp.mpf(1) / 2) / 2)
    print(f"  target = {mp.nstr(tgt, 12)}\n")
    cands = [
        ("e^(30/7)", mp.e ** (mp.mpf(30) / 7)), ("sqrt(5277)", mp.sqrt(5277)),
        ("pi^2 e^2", mp.pi ** 2 * mp.e ** 2), ("23 pi", 23 * mp.pi),
        ("72", mp.mpf(72)), ("8 pi e", 8 * mp.pi * mp.e),
        ("4 pi e", 4 * mp.pi * mp.e), ("2 pi e^2", 2 * mp.pi * mp.e ** 2),
        ("e^4/2", mp.e ** 4 / 2), ("pi^4 * 0.746", mp.pi ** 4 * mp.mpf("0.746")),
        ("137.036/1.886", ALPHA_INV / mp.mpf("1.886")),
    ]
    print(f"  {'candidate':<18} {'value':>16} {'rel err':>12}")
    hits, rows = 0, []
    for k, v in cands:
        rel = abs(v - tgt) / tgt
        ok = rel < mp.mpf("1e-3")
        hits += ok
        rows.append({"form": k, "value": mp.nstr(v, 10), "rel_err": mp.nstr(rel, 3),
                     "within_1e-3": bool(ok)})
        print(f"  {k:<18} {mp.nstr(v,10):>16} {mp.nstr(rel,3):>12}"
              f"{'   <-- within 1e-3' if ok else ''}")
    print(f"\n  {hits} of {len(cands)} land within 1e-3 -- and `sqrt(5277)` is")
    print(f"  transparently meaningless, which is the point: near any 3-digit target the")
    print(f"  space of short closed forms is DENSE, so 'it looks like a constant' carries")
    print(f"  no information.  Same failure mode as the alpha decoy family.")
    return {"target": mp.nstr(tgt, 12), "rows": rows, "hits": hits,
            "verdict": "neighbourhood is dense -> no evidence"}


def s3_cross_observable():
    head("S3", "Does the SAME factor explain the OTHER failed predictions?")
    print("  A missing power law is a property of the THEORY, so it must appear")
    print("  wherever the theory meets data -- not only in alpha.\n")
    r0 = mp.mpf(1) / 2
    base = ALPHA_INV / (L_of(r0) / 2)
    items = [("alpha^-1", L_of(r0) / 2, ALPHA_INV),
             ("L_IR [m]", R_SPIN / r0, mp.mpf("1.3e26")),
             ("g-factor", mp.mpf(2), mp.mpf("2.00231930436118"))]
    print(f"  {'observable':>10} {'predicted':>14} {'observed':>14} {'ratio':>14} "
          f"{'= 72.648^k':>14}")
    rows = []
    for name, pred, obs in items:
        rr = obs / pred
        k = mp.log(rr) / mp.log(base)
        rows.append({"observable": name, "predicted": mp.nstr(pred, 6),
                     "observed": mp.nstr(obs, 6), "ratio": mp.nstr(rr, 6),
                     "exponent_k": mp.nstr(k, 5)})
        print(f"  {name:>10} {mp.nstr(pred,6):>14} {mp.nstr(obs,6):>14} "
              f"{mp.nstr(rr,6):>14} {mp.nstr(k,5):>14}")
    print(f"\n  A single scaling rule requires ONE exponent everywhere.  These are")
    print(f"  1.0, 20.7 and 0.00027 -- five orders of magnitude apart.  And the alpha")
    print(f"  row reads 1.0 BY CONSTRUCTION, since 72.648 was defined as that ratio;")
    print(f"  it is not a confirmation, it is the definition.  S3 FAILS decisively.")
    return {"rows": rows, "verdict": "exponents disagree by 5 orders -> not a rule"}


def s4_instruments():
    head("S4", "Can ANY power law reconcile the three independent instruments?")
    print("  This is the strongest form of the hypothesis and the fairest test of it.")
    print("  The repo has three independent electrostatic models of the SAME geometry")
    print("  at a/R = 0.05 (code/capacitance_ribbon/ribbon_capacitance.py):\n")
    models = [("annulus", mp.mpf("3.037587")), ("conformal", mp.mpf("1.692054")),
              ("BIE (Moebius)", mp.mpf("0.372688"))]
    for n, v in models:
        print(f"     {n:<16} raw alpha^-1 = {mp.nstr(v, 8)}")
    print(f"\n  Hypothesis: alpha^-1_true = K * X^p for some universal (K, p), where X is")
    print(f"  a model's raw output.  All three describe the same physical geometry, so")
    print(f"  all three must map to the SAME observed 137.036.  But")
    print(f"      K * X1^p = K * X2^p   with X1 != X2   forces   p = 0.")
    x1, x2 = models[0][1], models[1][1]
    p_needed = mp.log(ALPHA_INV / ALPHA_INV) / mp.log(x1 / x2)   # = 0
    print(f"\n     required exponent p = {mp.nstr(p_needed, 6)}")
    print(f"     and then K = {mp.nstr(ALPHA_INV, 12)} -- the answer itself.")
    print(f"\n  So the ONLY power law that reconciles the instruments is the one with")
    print(f"  exponent ZERO: a 'law' that discards the geometry entirely and asserts")
    print(f"  alpha^-1 = 137.036 as a constant.  That is not a correction to the theory,")
    print(f"  it is the removal of the theory.  S4 FAILS.")
    print(f"\n  (Cross-check: fitting p on annulus vs conformal to reach a COMMON target")
    print(f"  is inconsistent for every non-zero p, because the map X -> K X^p is")
    print(f"  injective for p != 0 and the three X values are distinct.)")
    return {"models": [{"name": n, "alpha_inv": mp.nstr(v, 8)} for n, v in models],
            "required_exponent": 0,
            "verdict": "only p = 0 works -> discards the geometry, not a correction"}


def s5_dof():
    head("S5", "Degrees of freedom: is the hypothesis even testable here?")
    print("  To fit alpha^-1 = K * L^p you need at least two independent (input, output)")
    print("  pairs.  Count what the manuscript actually supplies:\n")
    print(f"     observables it claims to DERIVE and that are measured : 1  (alpha)")
    print(f"     free parameters in the power-law ansatz               : 2  (K, p)")
    print(f"     residual degrees of freedom                           : -1")
    print(f"\n  The system is underdetermined: with one datum, EVERY (K, p) satisfying")
    print(f"  K * L^p = 137.036 fits perfectly -- a one-parameter family of 'rules',")
    print(f"  none preferred.  Demonstrate:\n")
    L = L_of(mp.mpf(1) / 2)
    print(f"  {'p':>8} {'required K':>18} {'K L^p':>18}")
    rows = []
    for p in [mp.mpf(1), mp.mpf(2), mp.mpf("3.705668"), mp.mpf(4), mp.mpf(-1)]:
        K = ALPHA_INV / L ** p
        rows.append({"p": mp.nstr(p, 7), "K": mp.nstr(K, 10),
                     "check": mp.nstr(K * L ** p, 12)})
        print(f"  {mp.nstr(p,6):>8} {mp.nstr(K,10):>18} {mp.nstr(K*L**p,12):>18}")
    print(f"\n  All exact.  The 'natural' exponent -- the one making K = 1 -- is")
    print(f"  p = ln(137.036)/ln(L) = {mp.nstr(mp.log(ALPHA_INV)/mp.log(L), 8)}, which is")
    print(f"  not an integer, half-integer, or any recognisable index.  S5: the")
    print(f"  hypothesis cannot be tested from inside the manuscript; it needs a SECOND")
    print(f"  measured observable the framework derives, and there isn't one.")
    return {"observables": 1, "parameters": 2, "residual_dof": -1, "rows": rows,
            "natural_exponent": mp.nstr(mp.log(ALPHA_INV) / mp.log(L), 8),
            "verdict": "underdetermined -> untestable from within"}


def main():
    print(RULE)
    print("SCALING RULE or ARTIFACT?  Testing the 72.648x alpha discrepancy")
    print(RULE)
    res = {"S1_convention": s1_convention(), "S2_closed_form": s2_closed_form(),
           "S3_cross_observable": s3_cross_observable(), "S4_instruments": s4_instruments(),
           "S5_degrees_of_freedom": s5_dof()}
    print(f"\n{RULE}\nVERDICT\n{RULE}")
    for k, v in res.items():
        print(f"  {k:24s} {v['verdict']}")
    print(f"\n  ARTIFACT, on five independent grounds.  The factor 72.648 is a function")
    print(f"  of the arbitrary choice tau = i/2 (it runs 61 -> 138 across natural")
    print(f"  alternatives), it is not independent data (it is DEFINED as the ratio it")
    print(f"  is claimed to explain), it does not transfer to the framework's other")
    print(f"  failed predictions (exponents 1.0 vs 20.7 vs 0.00027), no non-zero power")
    print(f"  reconciles the three independent instruments, and with one observable and")
    print(f"  two parameters the ansatz is underdetermined anyway.")
    print(f"\n  The hypothesis was worth testing and it could have come out otherwise:")
    print(f"  had the ratio held at 72.648 across the tau sweep AND reproduced the L_IR")
    print(f"  gap, that would have been real evidence of a missing power.  It does not.")
    print(RULE)
    out = ROOT / "docs" / "alpha_scaling_test.json"
    out.write_text(json.dumps({
        "description": "Is the 72.648x alpha discrepancy a scaling rule or an artifact?",
        "source": "code/constraint_projection/alpha_scaling_test.py",
        "checks": res, "verdict": "ARTIFACT on five independent grounds"},
        indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
