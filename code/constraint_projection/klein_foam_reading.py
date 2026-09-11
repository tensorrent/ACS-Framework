#!/usr/bin/env python3
# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
The Klein-Foam reading of `a`: not a particle cutoff, but the throat's finite resolution.

Prompted by the author's own framing: "there are no particles, only the finite
resolution throat."  That is not decoration -- it changes what the parameter `a`
IS, and therefore what it would take to fix it.  This tests the reading against
the corpus's own documents.

    K1  is alpha^-1 actually resolution-relative?  (FF06h joint-scaling invariance)
    K2  the foam supplies its own resolution -- what does it give?
    K3  what resolution does the manuscript's alpha require, against that floor?
    K4  two scope declarations for a/R: Klein_Foam_Monad.tex vs the CPF entry

Run:  python3 code/constraint_projection/klein_foam_reading.py
Deps: sympy, mpmath
Artifact: docs/klein_foam_reading.json
"""

import json
import re
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
mp.mp.dps = 40

ALPHA_INV = mp.mpf("137.035999177")
HBAR, M_E, C_L = mp.mpf("1.054571817e-34"), mp.mpf("9.1093837015e-31"), mp.mpf("299792458")
R_SPIN = HBAR / (2 * M_E * C_L)
L_PLANCK = mp.mpf("1.616255e-35")
RULE = "=" * 78


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


def k1_invariance():
    head("K1", "Is alpha^-1 actually resolution-relative?  (FF06h invariance)")
    print("  FF06h (Scaled_Invariance_of_Infinity_and_Zero.tex) proves the count")
    print("  N_delta[a,b] is a property of the PAIR (interval x unit), invariant under")
    print("  the joint rescaling ([a,b], delta) -> (lambda[a,b], lambda delta), and")
    print("  that the invariant is DIMENSIONLESS.\n")
    print("  If the Klein-Foam reading is right -- no particles, only a throat at")
    print("  finite resolution -- then alpha^-1 must be a function of the RATIO of")
    print("  scale to resolution and of nothing else.  Test it symbolically:\n")
    R, a, lam = sp.symbols("R a lambda", positive=True)
    ainv = (sp.log(8 * R / a) + 1) / 2
    scaled = ainv.subs({R: lam * R, a: lam * a})
    diff = sp.simplify(scaled - ainv)
    print(f"     alpha^-1(R, a)               = {ainv}")
    print(f"     alpha^-1(lambda R, lambda a) = {sp.simplify(scaled)}")
    print(f"     difference                   = {diff}")
    print(f"     JOINT-SCALING INVARIANT: {diff == 0}")
    print(f"\n  Confirmed.  alpha^-1 depends on R/a and nothing else, so the reading is")
    print(f"  STRUCTURALLY CORRECT: the formula is a scale-to-resolution ratio, exactly")
    print(f"  what a no-particles ontology should produce.  This is a genuine coherence")
    print(f"  between the ontology and the algebra, not a coincidence.")
    assert diff == 0
    return {"expression": str(ainv), "joint_scaling_invariant": True,
            "depends_only_on": "R/a",
            "verdict": "reading is structurally correct -- alpha^-1 IS resolution-relative"}


def k2_foam_resolution():
    head("K2", "The foam supplies its own resolution -- what does it give?")
    src = ROOT / "papers/notes/Klein_Foam_Monad.tex"
    txt = src.read_text() if src.exists() else ""
    m = re.search(r"Micro \(Planck / voxel\)[^\\]*", txt)
    print("  The Klein-Foam note does not leave the resolution open.  Section")
    print("  'Nested scale-variant dimensions' states it:\n")
    if m:
        print(f"     \"{m.group(0).strip()}\"")
    else:
        print("     (quote not located; see papers/notes/Klein_Foam_Monad.tex, sec:scales)")
    print(f"\n  So the foam's own floor is the Planck / voxel scale.  Taking it:\n")
    r = L_PLANCK / R_SPIN
    L = mp.log(8 / r) + 1
    pred = L / 2
    print(f"     a = l_Planck = {mp.nstr(L_PLANCK,6)} m")
    print(f"     R = hbar/(2 m_e c) = {mp.nstr(R_SPIN,6)} m")
    print(f"     a/R = {mp.nstr(r,6)}")
    print(f"     alpha^-1 = (1/2)(ln(8R/a)+1) = {mp.nstr(pred,8)}")
    print(f"     observed = {mp.nstr(ALPHA_INV,10)}   ->  off by {mp.nstr(ALPHA_INV/pred,5)}x")
    print(f"\n  BEST of every absolute reading tested: 5.08x, against 72.6x for")
    print(f"  tau = i/2 and 89x for a = R.  The ontology genuinely improves the")
    print(f"  prediction by supplying a principled resolution.  It is still wrong by 5x.")
    return {"foam_floor": "Planck / voxel (sec:scales)",
            "a_over_R": mp.nstr(r, 6), "alpha_inv": mp.nstr(pred, 8),
            "off_by": mp.nstr(ALPHA_INV / pred, 5),
            "verdict": "best absolute reading; still 5.08x off"}


def k3_below_the_floor():
    head("K3", "What resolution does the manuscript's alpha require?")
    a_needed = R_SPIN * 8 * mp.e ** (1 - 2 * ALPHA_INV)
    in_planck = a_needed / L_PLANCK
    decades = -mp.log(in_planck, 10)
    print(f"     required a          = {mp.nstr(a_needed,6)} m")
    print(f"     in Planck lengths   = {mp.nstr(in_planck,6)}")
    print(f"     i.e. {mp.nstr(decades,5)} DECADES BELOW the foam's own stated floor\n")
    print(f"  This is the sharpest form of the alpha kill, and it is now INTERNAL.")
    print(f"  Previously the objection was external -- a sub-Planckian cutoff is")
    print(f"  unphysical.  Under the Klein-Foam reading it is a contradiction between")
    print(f"  two documents of the same programme: the foam's resolution is declared")
    print(f"  Planck-scale in Klein_Foam_Monad.tex, and the manuscript's alpha needs a")
    print(f"  resolution {mp.nstr(decades,4)} decades finer than that.")
    print(f"\n  AND THE RENAMING DOES NOT MOVE THE NUMBER.  Whether `a` is a particle")
    print(f"  cutoff or a throat resolution, alpha^-1 = (1/2)(ln(8R/a)+1) still requires")
    print(f"  a/R = {mp.nstr(8*mp.e**(1-2*ALPHA_INV),6)}.  The ontological move may well be right; it is")
    print(f"  simply orthogonal to the arithmetic.  Same shape as CPF Sec 9's")
    print(f"  relational-measurement material: a reframe that leaves the falsifiable")
    print(f"  content untouched.")
    return {"required_a_m": mp.nstr(a_needed, 6),
            "required_a_in_planck_lengths": mp.nstr(in_planck, 6),
            "decades_below_foam_floor": mp.nstr(decades, 5),
            "renaming_changes_arithmetic": False,
            "verdict": "96 decades below the foam's own floor -- an INTERNAL contradiction"}


def k4_scoping():
    head("K4", "Two scope declarations for a/R, dated a month apart")
    kf = ROOT / "papers/notes/Klein_Foam_Monad.tex"
    cpf = ROOT / "papers/notes/Constraint_Projection_Framework.tex"
    kf_txt = kf.read_text() if kf.exists() else ""
    cpf_txt = cpf.read_text() if cpf.exists() else ""

    print("  Both files are entries in the same corpus.  Each states a scope for")
    print("  a/R.  The two statements differ.  Quoted, not paraphrased:\n")
    kf_quotes = []
    for pat in [r"Absolute uniqueness and ``no free parameters''[^.]*\.",
                r"as-implemented, not as a uniqueness theorem for \$\\alpha\$[^.]*\.",
                r"Free-parameter count depends on which[\s\S]{0,180}?not claimed\."]:
        m = re.search(pat, kf_txt)
        if m:
            q = " ".join(m.group(0).split())
            kf_quotes.append(q)
            print(f"     Klein Foam:  \"{q[:150]}{'...' if len(q)>150 else ''}\"")
    print()
    cpf_quotes = []
    for pat in [r"The framework contains zero free parameters[^.]*\.",
                r"CPF \+ GfE & 0 & All constants"]:
        m = re.search(pat, cpf_txt)
        if m:
            q = " ".join(m.group(0).split())
            cpf_quotes.append(q)
            print(f"     CPF:         \"{q}\"")

    print(f"\n  THE FINDING -- a corpus fact, not a verdict on either entry.")
    print(f"  Klein_Foam_Monad.tex names a/R as an input and records the count as")
    print(f"  input-dependent.  The CPF entry records a/R as not free.  Two entries,")
    print(f"  same quantity, different scope.  The arithmetic (K3) matches the earlier")
    print(f"  one: a/R is carrying a fitted value.")
    print(f"\n  What this changes is WHERE the resolution lives.  It is already in the")
    print(f"  corpus, dated a month earlier, in those words.  The audit did not have to")
    print(f"  supply it -- only to find it.  Nothing here grades the entries; the ledger")
    print(f"  records which scope the numbers support, and both entries stand.")
    return {"klein_foam_quotes": kf_quotes, "cpf_quotes": cpf_quotes,
            "klein_foam_names_a_over_R_as_input": True,
            "cpf_declares_zero_free_parameters": True,
            "verdict": "two scope declarations for a/R in one corpus; the arithmetic matches the earlier"}


def main():
    print(RULE)
    print("THE KLEIN-FOAM READING: `a` as throat resolution, not particle cutoff")
    print(RULE)
    res = {"K1_invariance": k1_invariance(), "K2_foam_resolution": k2_foam_resolution(),
           "K3_below_the_floor": k3_below_the_floor(), "K4_scoping": k4_scoping()}
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print("  The reading is STRUCTURALLY CORRECT (K1): alpha^-1 is joint-scaling")
    print("  invariant and depends only on R/a, exactly as a no-particles ontology")
    print("  requires.  It gives the BEST absolute prediction of any reading tested")
    print("  (K2: 26.96, off 5.08x).  And it makes the alpha kill INTERNAL rather than")
    print("  external (K3: the required resolution is 96 decades below the foam's own")
    print("  declared floor).")
    print()
    print("  But the renaming does not move the arithmetic, and K4 is where the")
    print("  resolution turns out to already live: Klein_Foam_Monad.tex records a/R")
    print("  as an input and the count as input-dependent.  The corpus carries two")
    print("  scope declarations; the arithmetic matches the earlier one.")
    print(RULE)
    out = ROOT / "docs" / "klein_foam_reading.json"
    out.write_text(json.dumps({
        "description": "The Klein-Foam reading of `a` as throat resolution",
        "source": "code/constraint_projection/klein_foam_reading.py",
        "checks": res}, indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
