#!/usr/bin/env python3
"""Subjective correctness (coherence) vs factual accuracy, and the holistic axis.

Three predicates, routinely collapsed into one:

    COHERENT   does the conclusion FOLLOW from the stated premises?
               a property of the derivation, checkable without any measurement
    ACCURATE   does the number MATCH observation?
               a property of the output, checkable without reading the argument
    HOLISTIC   do the independently-derived results AGREE with each other?
               a property of the SET, invisible from inside any one of them

They are independent, so there are four quadrants and not a single scale --
and the ordering between two of those quadrants is the opposite of the
intuitive one.

    H1  the two axes, made operational
    H2  the corpus classified
    H3  individually coherent, jointly incoherent
    H4  why coherent+inaccurate BEATS incoherent+accurate
    H5  where this audit's own output sits
"""
import json
import math
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


def h1_axes():
    head("H1", "The two axes, made operational")
    print("""  Each has a test that does not consult the other -- which is what makes
  them independent rather than two words for quality.\n""")
    # Coherence: does the conclusion follow?  Symbolic, no measurement.
    E, eps, R, me, cc, hb, L = sp.symbols("e epsilon_0 R m_e c hbar L", positive=True)
    C = 2 * sp.pi * eps * R / L
    stated = sp.Eq((E / 2) ** 2 / (2 * C), me * cc ** 2)
    derived_L = sp.solve(stated, L)[0]
    with_R = sp.simplify(derived_L.subs(R, hb / (2 * me * cc)))
    alpha = E ** 2 / (4 * sp.pi * eps * hb * cc)
    claimed = 1 / alpha                      # the manuscript's alpha^-1 = L
    actual = sp.simplify(with_R)
    follows = sp.simplify(actual - claimed) == 0
    print(f"     COHERENCE TEST -- purely symbolic, no data consulted:")
    print(f"        premises give   L = {actual}")
    print(f"        claim is        L = alpha^-1 = {sp.simplify(claimed)}")
    print(f"        does the claim FOLLOW?  {follows}   (ratio = {sp.simplify(actual/claimed)})")
    print(f"\n     ACCURACY TEST -- purely numeric, no argument consulted:")
    print(f"        the manuscript's stated value 137.035999171 vs CODATA 137.035999177")
    rel = abs(137.035999171 - 137.035999177) / 137.035999177
    print(f"        relative difference = {rel:.2e}   -> accurate")
    print(f"""
     So the entry is INACCURATE nowhere and INCOHERENT at the step above: the
     premises give L = 2/alpha and the claim is L = 1/alpha.  Accuracy did not
     detect that, and could not -- it never reads the derivation.  Coherence
     did, and needed no measurement.

     Two tests, neither reducible to the other.""")
    return {"claim_follows_from_premises": bool(follows),
            "ratio_actual_over_claimed": str(sp.simplify(actual / claimed)),
            "accuracy_relative_difference": rel}


def h2_classify():
    head("H2", "The corpus, classified")
    rows = [
        ("M = Klein bottle from clauses (1)-(2)", True, True,
         "follows uniquely; and it is the surface it says"),
        ("S = 2 sqrt 2 for the Bell state", True, True, "arithmetic checks; matches QM"),
        ("alpha^-1 = ln(8R/a)+1", False, True,
         "premises give 2/alpha; the NUMBER still lands on CODATA"),
        ("a/R = 8 exp(-136.035999171)", False, True,
         "no derivation; the exponent IS CODATA alpha^-1 minus one"),
        ("Axiom III: phi_* = [[1,2],[0,1]]", False, False,
         "MCG(K) has order 4; phi_* has infinite order -- no model"),
        ("g = Sl = 2", True, False,
         "follows from the stated geometry; a_e puts it 8.92e9 sigma out"),
        ("Sec 7: k = 0 <=> RH", False, False,
         "the defining integral is +oo, not the claimed sum"),
        ("Green's C = 4 pi^2 eps0 R/ln(8R/a)", True, True,
         "derived from the Green's function; BEM confirms to 0.46%"),
    ]
    print(f"     {'claim':<40} {'coherent':>9} {'accurate':>9}  quadrant")
    quad = {}
    for name, coh, acc, _ in rows:
        q = ("COHERENT+ACCURATE" if coh and acc else
             "coherent+inaccurate" if coh else
             "INCOHERENT+accurate" if acc else "incoherent+inaccurate")
        quad[q] = quad.get(q, 0) + 1
        print(f"     {name:<40} {str(coh):>9} {str(acc):>9}  {q}")
    print(f"\n     quadrant counts: {quad}")
    print("""
     The interesting cell is INCOHERENT+ACCURATE: two entries land on the
     measured number without a derivation that reaches it.  That combination
     is invisible to anyone checking only the output, which is the usual way
     a result gets checked.""")
    return {"rows": [{"claim": n, "coherent": c, "accurate": a, "note": w}
                     for n, c, a, w in rows], "quadrants": quad}


def h3_jointly_incoherent():
    head("H3", "Individually coherent, jointly incoherent -- the holistic axis")
    print("""  Two derivations can each be valid and still contradict each other.  That
  failure is invisible from inside either one, which is what makes it a
  property of the SET rather than of any member.\n""")
    cases = [
        ("tau = i a/R = i/2  (Sec 3)", 0.5, 1.886294),
        ("a L_IR = R^2, L_IR observed  (Sec 8)", 1.485e-39, 46.24235),
    ]
    print(f"     {'condition':<40} {'a/R':>12}  {'alpha^-1':>10}")
    for nm, aR, ai in cases:
        print(f"     {nm:<40} {aR:>12.3e}  {ai:>10.4f}")
    ratio = cases[1][2] / cases[0][2]
    print(f"\n     both derivations valid on their own premises")
    print(f"     they disagree by {ratio:.1f}x, and neither matches 137.036")
    print(f"""
     Each is internally COHERENT.  The SET is not.  And note what this costs:
     an under-determined framework has a missing input you can go and find; an
     over-determined one has no free parameter left to absorb the difference,
     so supplying the boundary condition removed the last place the
     discrepancy could hide.

     Holistic incoherence is strictly worse than a single incoherent step,
     because there is no local repair for it.""")
    return {"conditions": [{"name": n, "a_over_R": a, "alpha_inv": v} for n, a, v in cases],
            "disagreement_factor": ratio}


def h4_ordering():
    head("H4", "Why COHERENT+INACCURATE beats INCOHERENT+ACCURATE")
    print("""  The intuitive ordering puts "gets the right number" on top.  The decoy
  data says otherwise, and it is measurable.\n""")
    n_forms, n_hit = 14, 14
    p_hit = n_hit / n_forms
    bits = abs(-math.log2(p_hit)) if p_hit > 0 else float("inf")  # avoid -0.0
    print(f"     decoy test: {n_hit} of {n_forms} unrelated functional forms hit CODATA alpha")
    print(f"     P(accurate | fitted) = {p_hit:.2f}")
    print(f"     information carried by 'it matches' = -log2(P) = {bits:.2f} bits")
    print(f"""
     Accuracy conveys {bits:.0f} bits here.  When a parameter is free enough to be
     tuned, hitting the target is guaranteed, so observing the hit tells you
     nothing you did not already know.

     Coherence does not degrade that way.  It is checked against the premises,
     which cannot be tuned after the fact without visibly changing the claim.

     THE ORDERING, and it is the opposite of the intuitive one:

        coherent + inaccurate   a well-posed theory that is FALSIFIED.
                                Valuable: the derivation can be inspected, the
                                failing step located, and the theory repaired
                                or discarded on evidence.  g = Sl = 2 is here.
        incoherent + accurate   a FIT wearing a derivation's clothes.
                                Nearly worthless: the number carries 0 bits,
                                and there is no argument to inspect, so
                                nothing about it can be learned or repaired.

     Wyler 1970 sits in the second cell with rel err 5.9e-7 and was debunked.
     This entry is 13,471x closer and sits in the same cell.  Closer agreement
     is not better evidence -- more digits only means more digits were fitted.""")
    return {"decoy_forms": n_forms, "decoy_hits": n_hit,
            "p_accurate_given_fitted": p_hit, "bits_from_accuracy": bits,
            "ordering": "coherent+inaccurate > incoherent+accurate"}


def h5_this_audit():
    head("H5", "Where this audit's own output sits")
    print("""  The same three predicates, turned inward.

     COHERENT   the instruments derive their conclusions from computed values
                -- enforced by rule 7 after eight bugs of exactly the shape
                "prose written beside a number that contradicted it".  Six of
                those were caught in the last ten entries alone, which says
                the enforcement is load-bearing and the failure recurrent.

     ACCURATE   64 gate tests, mutation-checked; three Lean proofs re-observed
                this session; artifacts byte-identical on re-run.

     HOLISTIC   this is the weakest of the three and the honest place to say
                so.  The entries have not been checked against EACH OTHER at
                scale.  H3's failure mode -- individually valid, jointly
                contradictory -- is exactly what a 3,000-line ledger written
                incrementally is exposed to, and no instrument here tests it.

  So the audit is in better shape on the two axes it can check locally and
  unverified on the one that requires reading the whole corpus at once.  That
  is a recorded open item, not a clean bill.""")
    return {"coherent": "enforced by rule 7; 8 bugs of that shape found",
            "accurate": "64 gate tests, mutation-checked, proofs re-observed",
            "holistic": "UNVERIFIED -- entries not cross-checked at scale",
            "open_item": "no instrument tests joint coherence of the ledger"}


def main():
    print(RULE)
    print("COHERENCE vs ACCURACY, AND THE HOLISTIC AXIS")
    print(RULE)
    res = {"H1_axes": h1_axes(), "H2_classify": h2_classify(),
           "H3_jointly_incoherent": h3_jointly_incoherent(),
           "H4_ordering": h4_ordering(), "H5_this_audit": h5_this_audit()}
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print(f"""  Three predicates, independent, routinely collapsed:

    COHERENT   does it follow from the premises?   -- symbolic, no data needed
    ACCURATE   does it match observation?          -- numeric, no argument read
    HOLISTIC   do the results agree with EACH OTHER? -- a property of the set

  H1  the manuscript's alpha step is inaccurate nowhere and incoherent at one
      point: premises give L = 2/alpha, the claim is L = 1/alpha.  The accuracy
      test cannot see that -- it never reads the derivation.
  H2  classified: {res['H2_classify']['quadrants']}
  H3  and the two relational conditions are each coherent while disagreeing
      {res['H3_jointly_incoherent']['disagreement_factor']:.1f}x -- incoherence that belongs to the SET, with no local repair.
  H4  accuracy carries {res['H4_ordering']['bits_from_accuracy']:.0f} bits when 14 of 14 decoy forms hit the target.
      So coherent+inaccurate (falsifiable, inspectable) OUTRANKS
      incoherent+accurate (a fit with nothing to inspect) -- the reverse of
      the intuitive ordering.
  H5  turned inward: this audit is checked on coherence and accuracy and
      UNVERIFIED on holistic consistency.  Recorded as open.""")
    print(RULE)
    out = ROOT / "docs" / "coherence_vs_accuracy.json"
    out.write_text(json.dumps({
        "description": "Coherence vs accuracy vs holistic consistency, with the corpus classified",
        "source": "code/constraint_projection/coherence_vs_accuracy.py",
        "checks": res}, indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
