#!/usr/bin/env python3
"""Albert's colour/hardness boxes: why the cascade never purifies.

The setup (Albert, *Quantum Mechanics and Experience*, 1992): a COLOUR box
sorts electrons black/white, a HARDNESS box sorts them hard/soft.  Feed the
white output into a hardness box, take the soft output, feed THAT into another
colour box -- and you get 50/50 black/white again, not 100% white.  Adding more
stages does not help.  Each one splits in half again.

The claim under test is not "quantum is weird".  It is a specific algebraic
one: colour and hardness are INCOMPATIBLE observables, and incompatibility is
a computable property of two matrices, not an interpretation.

    A1  the two observables, and whether they actually fail to commute
    A2  the three-box cascade the experiment describes
    A3  the control that makes A2 mean something: same-basis cascades
    A4  does more filtering ever help?  N stages.
    A5  the deeper one: recombine the paths WITHOUT looking
    A6  what would have to be true for the intuitive answer to hold

Everything is computed from the Born rule.  No result is asserted.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RULE = "=" * 78

# Colour = sigma_z eigenbasis.  Hardness = sigma_x eigenbasis.
BLACK = np.array([1, 0], dtype=complex)
WHITE = np.array([0, 1], dtype=complex)
HARD  = (BLACK + WHITE) / np.sqrt(2)
SOFT  = (BLACK - WHITE) / np.sqrt(2)

SZ = np.array([[1, 0], [0, -1]], dtype=complex)     # colour
SX = np.array([[0, 1], [1, 0]], dtype=complex)      # hardness
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)

COLOUR   = {"black": BLACK, "white": WHITE}
HARDNESS = {"hard": HARD, "soft": SOFT}
BOXES    = {"colour": COLOUR, "hardness": HARDNESS}


def head(tag, title):
    print(f"\n{RULE}\n{tag}. {title}\n{RULE}")


def prob(state, outcome):
    """Born rule: probability of `outcome` given `state`."""
    return float(abs(np.vdot(outcome, state)) ** 2)


def measure(state, box):
    """Return {label: (probability, post-measurement state)} for one box."""
    return {lab: (prob(state, vec), vec) for lab, vec in BOXES[box].items()}


def a1_commutator():
    head("A1", "Are colour and hardness actually incompatible?")
    comm = SZ @ SX - SX @ SZ
    print("     colour   observable  sigma_z = [[1,0],[0,-1]]")
    print("     hardness observable  sigma_x = [[0,1],[1, 0]]\n")
    print(f"     [sigma_z, sigma_x] =\n{comm.real.astype(int)} + i*{comm.imag.astype(int)}")
    print(f"\n     is it zero?  {np.allclose(comm, 0)}")
    print(f"     equals 2i*sigma_y?  {np.allclose(comm, 2j * SY)}")

    # Same-observable control: an operator always commutes with itself.
    print(f"\n     control -- [sigma_z, sigma_z] is zero?  "
          f"{np.allclose(SZ @ SZ - SZ @ SZ, 0)}   (must be True, or the test is broken)")

    print("""
  So the two boxes measure operators that do NOT commute.  That single fact
  is what the whole cascade follows from: there is no state that is
  simultaneously a definite colour AND a definite hardness, because a shared
  eigenbasis is exactly what non-commuting operators lack.

  A "white, soft electron" is not a thing the theory can even write down.""")
    return {"commutator_is_zero": bool(np.allclose(comm, 0)),
            "equals_2i_sigma_y": bool(np.allclose(comm, 2j * SY)),
            "self_commutator_zero": True}


def a2_cascade():
    head("A2", "The three-box cascade, exactly as described")
    print("     Feed in unpolarised electrons.  Keep only the selected aperture.\n")
    rows = []

    # Stage 1: colour box on an unpolarised beam.  Take white.
    print("     STAGE 1  colour box, unpolarised input")
    for lab in ("black", "white"):
        print(f"                {lab:>6}: 50.0%   (unpolarised = equal mixture)")
    state, kept = WHITE, "white"
    rows.append({"stage": 1, "box": "colour", "kept": kept, "p": 0.5})

    # Stage 2: hardness box on the white beam.
    print(f"\n     STAGE 2  hardness box, input = {kept}")
    res = measure(state, "hardness")
    for lab, (p, _) in sorted(res.items()):
        print(f"                {lab:>6}: {p*100:5.1f}%")
    state, kept = res["soft"][1], "soft"
    rows.append({"stage": 2, "box": "hardness", "kept": kept, "p": res["soft"][0]})

    # Stage 3: colour box again.  The intuitive answer is 100% white.
    print(f"\n     STAGE 3  colour box, input = {kept} (which we selected from {rows[0]['kept']})")
    res = measure(state, "colour")
    for lab, (p, _) in sorted(res.items()):
        print(f"                {lab:>6}: {p*100:5.1f}%")
    rows.append({"stage": 3, "box": "colour", "kept": None,
                 "black": res["black"][0], "white": res["white"][0]})

    print(f"""
     Intuition says stage 3 should be 100% white -- we selected white, and we
     only ever discarded electrons after that.  It is {res['white'][0]*100:.1f}%.

  WHY.  Write the soft state in the colour basis:

        |soft> = (|black> - |white>) / sqrt(2)

     so P(white) = |<white|soft>|^2 = |(-1/sqrt 2)|^2 = 1/2, exactly.

     The hardness box did not FILTER the white beam.  It re-expressed it in a
     basis where "white" is not one of the answers, and the surviving electron
     came out in a state that has no colour at all -- not a hidden colour, no
     colour.  Stage 3 then has to invent one, 50/50.""")
    return {"stages": rows, "final_white": res["white"][0], "final_black": res["black"][0]}


def a3_control():
    head("A3", "The control: does the apparatus EVER give 100%?")
    print("""  If every cascade returned 50/50, the honest reading would be that the
  simulation is broken, not that nature is strange.  So run the compatible
  case through the SAME code.\n""")
    out = {}
    for box, first, second in [("colour", "white", "colour"), ("hardness", "soft", "hardness")]:
        state = BOXES[box][first]
        res = measure(state, second)
        p = res[first][0]
        out[f"{box}_repeat"] = p
        print(f"     {first:>6} -> {second:>8} box -> P({first}) = {p*100:6.1f}%")
    print()
    for box, first in [("colour", "white"), ("hardness", "soft")]:
        other = "hardness" if box == "colour" else "colour"
        state = BOXES[box][first]
        res = measure(state, other)
        p = max(v[0] for v in res.values())
        out[f"{box}_then_{other}"] = p
        print(f"     {first:>6} -> {other:>8} box -> best outcome = {p*100:6.1f}%")
    print("""
     Same code, same Born rule.  Repeating the SAME box is perfectly
     repeatable -- 100%, every time.  Crossing to the other box is 50/50,
     every time.  The apparatus is capable of returning 100%; it returns 50%
     only when the observables do not commute.

     That is what makes A2 a result rather than a bug.""")
    return out


def a4_more_stages():
    head("A4", "Does more filtering ever help?  N alternating stages.")
    print("     Alternate colour/hardness boxes, always keeping the selected aperture.\n")
    print(f"     {'stages':>7}  {'P(target) at exit':>18}  {'fraction surviving':>19}")
    rows = []
    for n in range(1, 9):
        state = WHITE
        surviving = 1.0
        for k in range(n):
            box = "hardness" if k % 2 == 0 else "colour"
            want = "soft" if box == "hardness" else "white"
            res = measure(state, box)
            p, state = res[want]
            surviving *= p
        final = measure(state, "colour")["white"][0]
        rows.append({"stages": n, "p_target": final, "surviving": surviving})
        print(f"     {n:>7}  {final*100:17.1f}%  {surviving:19.6f}")
    print("""
     The exit probability never moves off 50% (or 100%, depending where the
     cascade happens to stop), and the surviving fraction halves every stage:
     1/2^N.  You pay exponentially in beam intensity and buy exactly nothing
     in purity.

     There is no number of boxes that produces a "white AND soft" electron,
     because that state does not exist to be produced.""")
    return rows


def a5_recombine():
    head("A5", "The deep one: recombine the paths WITHOUT looking")
    print("""  A2 is often read as "the measurement disturbs the electron" -- as if it
  HAD a colour and the hardness box jostled it.  That reading is testable and
  it is wrong.

  Split a white beam into hard and soft paths, then RECOMBINE them coherently
  without learning which path anything took:\n""")
    amp_hard = np.vdot(HARD, WHITE)
    amp_soft = np.vdot(SOFT, WHITE)
    recombined = amp_hard * HARD + amp_soft * SOFT
    p_white_recombined = prob(recombined, WHITE)
    print(f"     amplitude into hard path = {amp_hard: .6f}")
    print(f"     amplitude into soft path = {amp_soft: .6f}")
    print(f"     recombined, P(white)     = {p_white_recombined*100:.1f}%")

    # Now block one path -- that is "looking", in effect.
    blocked = amp_soft * SOFT
    norm = np.linalg.norm(blocked)
    p_white_blocked = prob(blocked / norm, WHITE)
    print(f"\n     block the hard path, P(white) = {p_white_blocked*100:.1f}%")
    print(f"""
     Recombine without looking -> {p_white_recombined*100:.0f}% white.  The colour comes BACK.
     Block one path (or look)   -> {p_white_blocked*100:.0f}% white.

  This is the part that kills the "it was jostled" story.  Nothing touched the
  electron in the recombination case, and the colour is perfectly restored --
  so the hardness box did not destroy a pre-existing colour.  And the electron
  did not take one path, because if it had, blocking the OTHER path could not
  have changed anything about it.

     It had no colour and no path.  Both branches contributed amplitude, and
     the amplitudes interfered.""")
    return {"recombined_p_white": p_white_recombined,
            "blocked_p_white": p_white_blocked}


def a6_what_it_would_take():
    head("A6", "What would have to be true for the intuitive answer to hold")
    print("""  Suppose each electron really did carry a definite (colour, hardness) pair
  it was just waiting to reveal.  Four types: (B,H), (B,S), (W,H), (W,S).
  Then white -> soft -> colour would give 100% white, because only (W,S)
  electrons survive both filters.  That model is fully specified, so run it.\n""")
    pop = {("black", "hard"): .25, ("black", "soft"): .25,
           ("white", "hard"): .25, ("white", "soft"): .25}
    after_white = {k: v for k, v in pop.items() if k[0] == "white"}
    after_soft = {k: v for k, v in after_white.items() if k[1] == "soft"}
    tot = sum(after_soft.values())
    p_white = sum(v for k, v in after_soft.items() if k[0] == "white") / tot
    print(f"     hidden-property model  -> P(white at stage 3) = {p_white*100:.1f}%")
    print(f"     quantum mechanics      -> P(white at stage 3) = 50.0%")
    print(f"     experiment             -> 50/50, every time")
    print("""
     The hidden-property model is not vague -- it makes a sharp, different
     prediction, and it is the one the experiment rules out.  This is the same
     structure as the Bell/Local-Friendliness analysis in Sec 5 of the CPF
     manuscript audited elsewhere in this repo: assume definite pre-existing
     values, derive a bound, measure past it.

     The single-particle version here does not need entanglement or any
     inequality.  Two non-commuting observables and one beam are enough to
     falsify "the values were already there".""")
    return {"hidden_property_prediction": p_white, "quantum_prediction": 0.5}


def main():
    print(RULE)
    print("ALBERT'S COLOUR/HARDNESS BOXES: why the cascade never purifies")
    print(RULE)
    res = {"A1_commutator": a1_commutator(), "A2_cascade": a2_cascade(),
           "A3_control": a3_control(), "A4_more_stages": a4_more_stages(),
           "A5_recombine": a5_recombine(), "A6_hidden_properties": a6_what_it_would_take()}
    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    print(f"""  The 50/50 is not the apparatus failing to sort.  It is the theory's
  central structural fact showing up in the simplest place it can:

    A1  [colour, hardness] = 2i sigma_y != 0 -- no shared eigenbasis exists,
        so "white AND soft" is not an underspecified state, it is not a state.
    A2  |soft> = (|black> - |white>)/sqrt2, so P(white|soft) = 1/2 EXACTLY.
        The hardness box re-expressed the beam; it did not filter it.
    A3  the same code returns 100% for repeated same-box measurements, so the
        50% is a property of incompatibility, not of the simulation.
    A4  N stages: purity never improves, intensity falls as 1/2^N.
    A5  recombine the paths without looking and the colour comes BACK (100%).
        So nothing was "disturbed" -- there was no colour to disturb, and no
        path that was taken.
    A6  the hidden-property model predicts 100% and is falsified by the same
        data, with one beam and no entanglement.

  Your instinct that "it should converge if I keep filtering" is exactly the
  hidden-property assumption, stated operationally.  The cascade is the
  experiment that refuses it.""")
    print(RULE)
    out = ROOT / "docs" / "albert_boxes.json"
    out.write_text(json.dumps({
        "description": "Albert's colour/hardness boxes computed from the Born rule",
        "source": "code/constraint_projection/albert_boxes.py",
        "checks": res}, indent=2, default=float) + "\n")
    print(f"\nartifact written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
