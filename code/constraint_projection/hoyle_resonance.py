#!/usr/bin/env python3
"""The Hoyle resonance as a control on the coherence/accuracy framework.

H4 concluded that "it matches the measured value" can carry zero information
when a parameter was free enough to be tuned -- 14 of 14 decoy forms hit
CODATA alpha, so the hit conveyed 0 bits.

The Hoyle state is the sharpest available counter-case, and it is a control
rather than an analogy.  Hoyle (1953) reasoned BACKWARDS FROM THE ANSWER --
carbon exists, therefore the triple-alpha process must be resonant, therefore
a 0+ state must sit near 7.7 MeV -- the same surface form as "alpha is
137.036, therefore a/R is 8 exp(-136.036)".  One of these carries information
and one does not, and the difference is measurable.

    N1  the energetics, computed from nuclear masses
    N2  how NARROW was the prediction?
    N3  bits carried -- Hoyle vs the a/R fit
    N4  the discriminator: could it have failed?
    N5  what this does and does not license
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78

U_MEV = 931.49410242          # CODATA: 1 u in MeV/c^2
M_HE4 = 4.00260325413         # AME2020 atomic mass, u
M_BE8 = 8.005305102           # AME2020
M_C12 = 12.0                  # exact by definition
E_HOYLE = 7.6542              # measured excitation of the 0+_2 state, MeV
# Published values to anchor against (rule 2: do not check our arithmetic
# against our own arithmetic).
PUB_Q_2ALPHA_KEV = 91.84      # Be-8 -> 2 alpha
PUB_THRESHOLD_MEV = 7.2747    # 3 alpha threshold above the C-12 ground state
PUB_E_RES_KEV = 379.5         # Hoyle state above the 3-alpha threshold


def head(t, s):
    print(f"\n{RULE}\n{t}. {s}\n{RULE}")


def n1_energetics():
    head("N1", "The energetics, from nuclear masses")
    q_2a = (M_BE8 - 2 * M_HE4) * U_MEV
    thr_3a = (3 * M_HE4 - M_C12) * U_MEV
    e_res = E_HOYLE - thr_3a
    print(f"     1 u = {U_MEV} MeV/c^2\n")
    print(f"     Be-8 - 2 He-4      = {M_BE8 - 2*M_HE4:+.6f} u = {q_2a:+.4f} MeV")
    print(f"        -> Be-8 is UNBOUND by {q_2a*1000:.0f} keV; it exists only as a fleeting resonance")
    print(f"     3 He-4 - C-12      = {3*M_HE4 - M_C12:+.6f} u = {thr_3a:+.4f} MeV")
    print(f"        -> the 3-alpha threshold sits {thr_3a:.4f} MeV above the C-12 ground state")
    print(f"\n     measured Hoyle state          = {E_HOYLE:.4f} MeV excitation")
    print(f"     above the 3-alpha threshold   = {e_res:.4f} MeV = {e_res*1000:.0f} keV")
    print(f"\n     ANCHORED to published values, not to our own arithmetic:")
    for nm, got, pub, unit in [("Q(Be-8 -> 2a)", q_2a*1000, PUB_Q_2ALPHA_KEV, "keV"),
                               ("3-alpha threshold", thr_3a, PUB_THRESHOLD_MEV, "MeV"),
                               ("resonance energy", e_res*1000, PUB_E_RES_KEV, "keV")]:
        print(f"        {nm:<20} computed {got:>9.4f} {unit}   published {pub:>9.4f} {unit}"
              f"   diff {abs(got-pub):.4f}")
    print(f"""
     That {e_res*1000:.0f} keV is the whole story.  Be-8 falls apart in ~1e-16 s, so
     carbon can only form if a third alpha arrives while it is still there AND
     lands on a state that is nearly energy-matched.  A resonance a few hundred
     keV above threshold is the only way the rate is not negligible.""")
    return {"Q_2alpha_MeV": q_2a, "threshold_3alpha_MeV": thr_3a,
            "hoyle_excitation_MeV": E_HOYLE, "resonance_above_threshold_MeV": e_res,
            "published_Q_2alpha_keV": PUB_Q_2ALPHA_KEV,
            "published_threshold_MeV": PUB_THRESHOLD_MEV,
            "published_E_res_keV": PUB_E_RES_KEV,
            "max_deviation_from_published_keV": max(
                abs(q_2a*1000 - PUB_Q_2ALPHA_KEV),
                abs(thr_3a - PUB_THRESHOLD_MEV)*1000,
                abs(e_res*1000 - PUB_E_RES_KEV))}


def n2_how_narrow():
    head("N2", "How narrow was the prediction?")
    thr_3a = (3 * M_HE4 - M_C12) * U_MEV
    e_res = E_HOYLE - thr_3a
    kT = 8.617333e-2 * 1.0        # kT in MeV at T = 1e9 K; helium burning ~1-2e8 K
    kT_he = kT * 0.15             # ~1.5e8 K
    print(f"     helium burning runs near T ~ 1.5e8 K, so kT ~ {kT_he*1000:.1f} keV.")
    print(f"     a resonance is useful only if it sits within roughly a few x kT")
    print(f"     to a few hundred keV of threshold -- too low and it is below the")
    print(f"     entrance channel, too high and the Boltzmann factor kills it.\n")
    lo, hi = 0.0, 0.8             # MeV above threshold: the usable window
    window = hi - lo
    plausible_lo, plausible_hi = 0.0, 20.0   # any 0+ excitation in C-12, MeV
    plausible = plausible_hi - plausible_lo
    print(f"     usable window above threshold ....... {lo:.1f} - {hi:.1f} MeV  (width {window:.1f} MeV)")
    print(f"     prior range for a 0+ excitation ..... {plausible_lo:.0f} - {plausible_hi:.0f} MeV  (width {plausible:.0f} MeV)")
    print(f"     as absolute excitation energy ....... {thr_3a+lo:.2f} - {thr_3a+hi:.2f} MeV")
    print(f"     where the state actually is ......... {E_HOYLE:.4f} MeV  ({e_res*1000:.0f} keV above threshold)")
    inside = lo <= e_res <= hi
    print(f"     inside the predicted window?  {inside}")
    return {"kT_MeV": kT_he, "window_MeV": window, "prior_range_MeV": plausible,
            "predicted_lo": thr_3a + lo, "predicted_hi": thr_3a + hi,
            "actual": E_HOYLE, "inside": bool(inside)}


def n3_bits(n2):
    head("N3", "Bits carried -- Hoyle vs the a/R fit")
    p_hoyle = n2["window_MeV"] / n2["prior_range_MeV"]
    bits_hoyle = -math.log2(p_hoyle)
    p_fit, bits_fit = 14 / 14, 0.0
    print(f"     HOYLE 1953")
    print(f"        prediction window / prior range = {n2['window_MeV']:.1f} / {n2['prior_range_MeV']:.0f} = {p_hoyle:.3f}")
    print(f"        information if confirmed = -log2({p_hoyle:.3f}) = {bits_hoyle:.2f} bits")
    print(f"        and it WAS confirmed: Dunbar/Wenzel/Whaling 1953, then Cook/Fowler/")
    print(f"        Lauritsen/Lauritsen 1957 for the 0+ assignment and the alpha decay.")
    print(f"\n     CPF a/R")
    print(f"        14 of 14 unrelated functional forms hit CODATA alpha")
    print(f"        P(hit | fitted) = {p_fit:.2f}")
    print(f"        information if confirmed = -log2({p_fit:.2f}) = {bits_fit:.2f} bits")
    print(f"""
     Same surface form -- reason from the known answer to a required value --
     and {bits_hoyle:.1f} bits versus {bits_fit:.0f}.  The difference is not rhetorical.  Hoyle's
     inference pinned a number inside a narrow window of a wide prior, so
     confirming it excluded most of the space.  The a/R construction pins
     nothing, because every form tested reaches the target.""")
    return {"hoyle_p": p_hoyle, "hoyle_bits": bits_hoyle,
            "fit_p": p_fit, "fit_bits": bits_fit}


def n4_could_it_have_failed():
    head("N4", "The discriminator: could it have failed?")
    print("""  This is the whole test, and it is answerable in both directions.

     HOYLE -- yes, and in several ways at once.
        * no 0+ state in the window            -> the argument is dead
        * a state there with the WRONG spin/parity (2+, 1-, ...) -> dead;
          the entrance channel is 3 spin-0 alphas, so only 0+ couples
        * a state that does not alpha-decay back -> dead
        Each was a separate way to lose, and each was checked by experiment.
        Cook et al. 1957 specifically confirmed the 0+ assignment and the
        alpha decay -- i.e. they tested the parts that could have killed it.

     CPF a/R -- no, and this is structural rather than a matter of care.
        a/R is DEFINED as 8 exp(-136.035999171), and that exponent is CODATA
        alpha^-1 minus one.  There is no measurement whose outcome could
        contradict it, because the measurement is its input.  The decoy test
        makes this concrete: 14 of 14 alternative forms also hit, so "it hits"
        was never evidence about which form is right.

  A prediction that cannot fail is not a weak prediction.  It is not a
  prediction -- it is a restatement of its own input in another notation.""")
    return {"hoyle_falsifiable": True,
            "hoyle_failure_modes": ["no state in window", "wrong spin-parity",
                                    "no alpha decay branch"],
            "cpf_falsifiable": False,
            "reason": "a/R is defined from the measured alpha it purports to predict"}


def n5_scope():
    head("N5", "What this licenses, and what it does not")
    print("""  LICENSED.  Reasoning backwards from an observed outcome is legitimate and
  can be highly informative.  The form of the argument is not what
  disqualifies the CPF construction -- Hoyle used the same form and it worked.
  What matters is whether the inference NARROWS the space and exposes itself
  to a measurement that could come out otherwise.

  NOT LICENSED, and worth stating because the Hoyle case is routinely
  over-read:

     * That anthropic reasoning is generally predictive.  This is ONE success,
       and its force comes from the narrowness computed in N2, not from the
       anthropic framing.  A wide-window anthropic argument carries little
       regardless of how compelling it sounds.
     * That Hoyle's own reasoning was anthropic in the modern sense.  Kragh
       (2010, "An Anthropic Myth") argues the anthropic telling is largely
       retrospective and that Hoyle's route ran more through nucleosynthesis
       rates than through "we exist".  We have not adjudicated that
       historiography here, and the physics result above does not depend on
       which account is correct -- the bits come from the window either way.
     * That a confirmed prediction validates the whole framework it came
       from.  Hoyle's success bears on the triple-alpha mechanism.  It does
       not transfer to unrelated claims by the same author.

  The transferable statement is narrow: THE VALUE OF A PREDICTION IS THE
  FRACTION OF THE SPACE IT EXCLUDES, not the elegance of its derivation and
  not the number of digits it matches.""")
    return {"licensed": "backwards reasoning can be informative if it narrows the space",
            "not_licensed": ["anthropic reasoning is generally predictive",
                             "Hoyle's reasoning was anthropic in the modern sense",
                             "a confirmed prediction validates its whole framework"],
            "historiography_note": "Kragh 2010 disputes the anthropic telling; not adjudicated here"}


def main():
    print(RULE)
    print("THE HOYLE RESONANCE AS A CONTROL ON COHERENCE vs ACCURACY")
    print(RULE)
    n1 = n1_energetics()
    n2 = n2_how_narrow()
    n3 = n3_bits(n2)
    res = {"N1_energetics": n1, "N2_narrowness": n2, "N3_bits": n3,
           "N4_falsifiability": n4_could_it_have_failed(), "N5_scope": n5_scope()}
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print(f"""  Hoyle and the CPF's a/R share a surface form -- reason from the known
  answer to a required value -- and could not be further apart in content.

    N1  computed from masses: Be-8 is unbound by {n1['Q_2alpha_MeV']*1000:.0f} keV and the 3-alpha
        threshold is {n1['threshold_3alpha_MeV']:.4f} MeV, so the Hoyle state sits {n1['resonance_above_threshold_MeV']*1000:.0f} keV above it.
    N2  that puts it inside a ~{n2['window_MeV']:.1f} MeV usable window out of a ~{n2['prior_range_MeV']:.0f} MeV prior.
    N3  so confirmation carried {n3['hoyle_bits']:.1f} bits.  The a/R construction carries {n3['fit_bits']:.0f},
        because 14 of 14 decoy forms also hit the target.
    N4  and Hoyle's could have failed three separate ways -- no state, wrong
        spin-parity, no alpha branch -- each checked by experiment.  a/R cannot
        fail, because the measurement it would be tested against is its input.

  A prediction that cannot fail is not a weak prediction; it is a restatement
  of its own input.  And the lesson is not "avoid backwards reasoning" -- it is
  that the value of a prediction is the fraction of the space it EXCLUDES.""")
    print(RULE)
    out = ROOT / "docs" / "hoyle_resonance.json"
    out.write_text(json.dumps({
        "description": "The Hoyle resonance as a control on the coherence/accuracy framework",
        "source": "code/constraint_projection/hoyle_resonance.py",
        "checks": res}, indent=2, default=str) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
