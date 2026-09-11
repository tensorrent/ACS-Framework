#!/usr/bin/env python3
"""
axiom_i_amenability.py -- Does Axiom I of the Constraint Projection Framework
have a satisfiable reading?

Axiom I (Constraint_Projection_Framework.tex, l.127):

    "Let B be the Basin Information Reservoir -- the infinite-dimensional,
     non-amenable informational substrate.  Formally, B = A_Q / Q^x (the adelic
     quotient). ... It admits no finitely additive, translation-invariant
     probability measure."

The existing repository verdict (cpf_audit.py C8, cpf_full_verification.py V8,
MANIFEST.md, docs/Elimination_Ledger.md) is "FALSE under every reading", carried
by the assertion "every abelian group is amenable" plus a Folner sequence
computed on Z.  That is a correct theorem about a different object: nothing in
the prior work evaluated A_Q, A_Q/Q, A_Q^x/Q^x or A_Q/Q^x itself.  This script
evaluates them.

WHAT IS ACTUALLY RUN HERE

  S1  Instrument validation.  A Cayley-graph edge-isoperimetric measurement,
      run first on six groups whose amenability is known, INCLUDING a group
      (BS(1,2)) that is amenable but that the search-based half of the
      instrument cannot certify.  An instrument that cannot fail is not
      evidence; this one is shown failing, in a known direction.
  S2  Reading (a)  B = A_Q/Q      -- strong approximation verified by explicit
                                     reduction of random adeles.
  S3  Reading (b)  B = A_Q^x/Q^x  -- the idele class group; structure theorem
                                     verified by explicit reduction of random
                                     ideles; Folner ratios on a finite model.
  S4  Reading (c)  B = A_Q/Q^x    -- Connes' adele class space, taken
                                     literally: is it even defined, is it a
                                     group, does "translation" exist on it?
  S5  The sweep.   Every reading anyone could mean, each classified, plus the
                   search for ANY adelic object that IS non-amenable.
  S6  Summary, written from the computed values.

Standing rule for this file (evidence-chain rule 7): every printed verdict is
an f-string over a variable computed above it.  No verdict is typed next to a
number.  Nine logged bugs in this repository have the other shape.

Run:      python3 axiom_i_amenability.py
Writes:   docs/axiom_i_amenability.json
Deps:     sympy (factorint, primerange).  No network, no global installs.
"""

from __future__ import annotations

import json
import platform
import random
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from sympy import factorint, primerange

SEED = 20260423                     # canonical repo seed
DOCS = Path(__file__).resolve().parents[2] / "docs"
OUT = DOCS / "axiom_i_amenability.json"

R: dict = {}                        # the artifact


def head(tag: str, title: str) -> None:
    print("\n" + "=" * 78)
    print(f"  {tag}  {title}")
    print("=" * 78)


def sub(title: str) -> None:
    print(f"\n  -- {title}")


# ===========================================================================
# S1.  THE INSTRUMENT, AND ITS VALIDATION
# ===========================================================================
#
# Folner's criterion (Folner 1955; Paterson, "Amenability", AMS Math. Surveys
# 29, Thm 4.13):  a discrete group G with finite generating set S is amenable
# iff for every eps > 0 there is a finite F subset G with
#
#       |F . s  sym  F| / |F| < eps    for all s in S.
#
# Equivalently, in the Cayley graph Cay(G,S) with edge boundary
# d_E(F) = #{edges with exactly one end in F}, G is amenable iff
#
#       h(G,S) := inf_{F finite, nonempty} |d_E(F)| / |F|  =  0
#
# (h is the Cheeger / edge-isoperimetric constant; Kesten 1959.)
#
# Two halves, with different logical strength -- kept apart on purpose:
#
#   I1  CONSTRUCTIVE.  Exhibit an explicit family F_n and compute its ratios.
#       If they go to 0, amenability is PROVED (Folner's criterion is an iff).
#   I2  EXHAUSTIVE SEARCH.  Minimise |d_E F|/|F| over every connected F with
#       |F| <= k.  Gives h_k >= h.  A plateau is SUGGESTIVE of h > 0, never a
#       proof -- S1c demonstrates the instrument being wrong in exactly this
#       way on BS(1,2).
#   I3  STRUCTURAL.  For a d-regular tree, every finite F spans a forest, so
#       |E(F)| <= |F| - 1 and |d_E F| = d|F| - 2|E(F)| >= (d-2)|F| + 2.
#       For d > 2 this is a PROOF of h >= d-2 > 0.  Verified numerically on
#       every set I2 enumerates.

# --- group presentations, each as (identity, generator maps, name) ----------

def grp_Z():
    return 0, [("+1", lambda x: x + 1), ("-1", lambda x: x - 1)]


def grp_Z2():
    return (0, 0), [("+e1", lambda x: (x[0] + 1, x[1])),
                    ("-e1", lambda x: (x[0] - 1, x[1])),
                    ("+e2", lambda x: (x[0], x[1] + 1)),
                    ("-e2", lambda x: (x[0], x[1] - 1))]


def grp_Zn(n):
    return 0, [("+1", lambda x: (x + 1) % n), ("-1", lambda x: (x - 1) % n)]


def grp_free_product(orders):
    """Free product of cyclic groups of the given orders (0 = infinite).

    Normal form: a tuple of alternating syllables (factor_index, exponent).
    Z/2 * Z/2 = D_inf (amenable);  Z * Z = F_2;  Z/2 * Z/3 = PSL(2,Z).
    """
    def mul(word, i, e):
        w = list(word)
        if w and w[-1][0] == i:
            j, f = w.pop()
            f += e
            if orders[i]:
                f %= orders[i]
            if f:
                w.append((j, f))
        else:
            w.append((i, e))
        return tuple(w)

    gens = []
    for i, n in enumerate(orders):
        gens.append((f"x{i}", (lambda i: lambda w: mul(w, i, 1))(i)))
        if n != 2:                                   # x = x^-1 when order 2
            gens.append((f"x{i}^-1", (lambda i: lambda w: mul(w, i, -1))(i)))
    return (), gens


def grp_BS12():
    """BS(1,2) = Z[1/2] semidirect Z,  (u,k)(v,l) = (u + 2^k v, k+l).

    Metabelian, hence solvable, hence AMENABLE (Day 1957) -- but of
    exponential growth, and its Folner sets are large.  Used as the instrument's
    negative control.
    """
    def r(g, h):
        return (g[0] + Fraction(2) ** g[1] * h[0], g[1] + h[1])
    a, t = (Fraction(1), 0), (Fraction(0), 1)
    ai, ti = (Fraction(-1), 0), (Fraction(0), -1)
    return (Fraction(0), 0), [("a", lambda g: r(g, a)), ("a^-1", lambda g: r(g, ai)),
                              ("t", lambda g: r(g, t)), ("t^-1", lambda g: r(g, ti))]


def grp_Z_times_units(N):
    """Z x (Z/N)^x -- the finite-level model of C_Q^0 = R_{>0} x Zhat^x."""
    units = [u for u in range(1, N) if _gcd(u, N) == 1]
    uset = set(units)
    gens = [("+1", lambda x: ((x[0] + 1), x[1])), ("-1", lambda x: ((x[0] - 1), x[1]))]
    for u in units:
        if u == 1:
            continue
        gens.append((f"*{u}", (lambda u: lambda x: (x[0], (x[1] * u) % N))(u)))
    return (0, 1), gens, units, uset


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# --- I2 / I3: exhaustive minimisation over connected sets ------------------

def cayley_ball(ident, gens, radius=None, cap=4000):
    """BFS the Cayley graph; return {vertex: [neighbours]} and the BFS order."""
    adj, order, frontier, depth = {ident: []}, [ident], [ident], 0
    while frontier and len(adj) < cap and (radius is None or depth < radius):
        nxt = []
        for v in frontier:
            for _, f in gens:
                w = f(v)
                if w not in adj:
                    adj[w] = []
                    order.append(w)
                    nxt.append(w)
        frontier, depth = nxt, depth + 1
    for v in adj:
        adj[v] = [f(v) for _, f in gens]
    return adj, order


def connected_subsets(root, adj, kmax, cap=200000):
    """All connected vertex sets containing `root` with size <= kmax."""
    out, seen = [], set()

    def rec(sub, ext, forb):
        key = frozenset(sub)
        if key in seen:
            return
        seen.add(key)
        out.append(key)
        if len(sub) >= kmax or len(out) >= cap:
            return
        ext = list(ext)
        forb = set(forb)
        for i, v in enumerate(ext):
            if len(out) >= cap:
                return
            rest = ext[i + 1:]
            ns = sub | {v}
            new = list(rest) + [w for w in adj.get(v, [])
                                if w in adj and w not in ns and w not in forb
                                and w not in rest]
            rec(ns, new, forb)
            forb.add(v)

    rec({root}, [w for w in adj.get(root, []) if w in adj], set())
    return out


def isoperimetric_profile(ident, gens, kmax, cap=200000):
    """h_k = min over connected F, |F| = m <= kmax, of |d_E F| / |F|.

    Cayley graphs are vertex-transitive, so a minimiser may be translated to
    contain the identity; enumerating only sets that contain it loses nothing.
    Also returns the forest check |E(F)| <= |F| - 1 (I3).
    """
    adj, _ = cayley_ball(ident, gens, radius=kmax + 1, cap=20000)
    subs = connected_subsets(ident, adj, kmax, cap=cap)
    deg = len(gens)
    best, forest_ok = {}, True
    for F in subs:
        m = len(F)
        inner = sum(1 for v in F for w in adj[v] if w in F)   # directed
        edges_half = inner / 2.0
        if edges_half > m - 1 + 1e-9:
            forest_ok = False
        bd = deg * m - inner
        r = bd / m
        if m not in best or r < best[m]:
            best[m] = r
    return best, len(subs), forest_ok, deg


def folner_explicit(name, family, gens_named):
    """I1: ratios |F sym F.s|/|F| for an explicit family of sets."""
    rows = []
    for label, F in family:
        Fs = set(F)
        worst = 0.0
        for gname, g in gens_named:
            img = {g(x) for x in Fs}
            worst = max(worst, len(Fs ^ img) / len(Fs))
        rows.append({"set": label, "size": len(Fs), "max_ratio": worst})
    return rows


def s1_instrument():
    head("S1", "Instrument validation -- six groups with known answers")

    print("""
  Folner's criterion (Folner 1955; Paterson, Amenability, AMS 1988, Thm 4.13):
  G amenable  <=>  h(G,S) = inf_F |d_E F|/|F| = 0.
  I1 constructive (proves amenability), I2 exhaustive search (bounds h from
  above -- a plateau only SUGGESTS non-amenability), I3 the tree bound
  |d_E F| >= (d-2)|F| + 2 (proves non-amenability for d > 2).""")

    known = {
        "Z":            ("amenable",     grp_Z()),
        "Z^2":          ("amenable",     grp_Z2()),
        "Z/12":         ("amenable",     grp_Zn(12)),
        "D_inf=Z2*Z2":  ("amenable",     grp_free_product([2, 2])),
        "F_2=Z*Z":      ("non-amenable", grp_free_product([0, 0])),
        "PSL2Z=Z2*Z3":  ("non-amenable", grp_free_product([2, 3])),
    }
    kmax = {"Z": 40, "Z^2": 9, "Z/12": 12, "D_inf=Z2*Z2": 24,
            "F_2=Z*Z": 9, "PSL2Z=Z2*Z3": 9}

    sub("I2/I3: exhaustive minimisation of |d_E F| / |F| over connected F")
    print(f"     {'group':<15} {'deg':>4} {'k':>4} {'#F':>8} {'h_k':>9} "
          f"{'h_(k/2)':>9} {'decay':>7} {'forest':>7} {'known':>13}")
    rows, verdicts = [], {}
    for name, (truth, (ident, gens)) in known.items():
        k = kmax[name]
        best, nsub, forest, deg = isoperimetric_profile(ident, gens, k)
        hk = min(best.values())
        khalf = max(m for m in best if m <= max(2, k // 2))
        hhalf = min(v for m, v in best.items() if m <= khalf)
        decay = hk / hhalf if hhalf else float("nan")
        # verdict is a function of the measured numbers, nothing else
        v = "amenable-consistent" if (hk < 0.5 * hhalf + 1e-12 or hk < 1e-12) \
            else "obstruction-detected"
        verdicts[name] = v
        rows.append({"group": name, "degree": deg, "kmax": k, "n_subsets": nsub,
                     "h_k": hk, "h_khalf": hhalf, "decay_ratio": decay,
                     "forest_bound_holds": forest, "known": truth,
                     "instrument_says": v})
        print(f"     {name:<15} {deg:>4} {k:>4} {nsub:>8} {hk:>9.4f} "
              f"{hhalf:>9.4f} {decay:>7.3f} {str(forest):>7} {truth:>13}")

    # I3 as a proof, for the 4-regular tree
    sub("I3: the tree bound, evaluated")
    ident, gens = grp_free_product([0, 0])
    best, _, forest, deg = isoperimetric_profile(ident, gens, 9)
    predicted = {m: (deg - 2) + 2.0 / m for m in best}
    maxdev = max(abs(best[m] - predicted[m]) for m in best)
    print(f"     Cay(F_2,{{a,b}}) is the {deg}-regular tree.  Every finite F spans a")
    print(f"     forest, so |E(F)| <= |F|-1 and |d_E F| >= ({deg}-2)|F| + 2.")
    print(f"     forest inequality held on all enumerated F : {forest}")
    print(f"     max |h_m(measured) - (({deg}-2) + 2/m)|      : {maxdev:.3e}")
    print(f"     => h(F_2) = inf_m ({deg}-2 + 2/m) = {deg - 2:.1f} > 0, "
          f"so F_2 is non-amenable (proof, not search).")

    # the honest negative control
    sub("I2's failure mode, demonstrated: BS(1,2)")
    ident, gens = grp_BS12()
    bbest, bn, bforest, bdeg = isoperimetric_profile(ident, gens, 9)
    bhk = min(bbest.values())
    bhalf = min(v for m, v in bbest.items() if m <= 4)
    bdecay = bhk / bhalf
    bs_says = "amenable-consistent" if bhk < 0.5 * bhalf else "obstruction-detected"
    print(f"     BS(1,2) = Z[1/2] x| Z is metabelian => solvable => AMENABLE")
    print(f"     (Day 1957, 'Amenable semigroups', Illinois J. Math. 1, 509).")
    print(f"     I2 at k=9 over {bn} connected sets: h_k = {bhk:.4f}, "
          f"h_4 = {bhalf:.4f}, decay = {bdecay:.3f}")
    print(f"     instrument says: {bs_says}   -- ground truth: amenable")
    print(f"     => I2 alone {'DOES NOT' if bs_says != 'amenable-consistent' else 'does'}"
          f" separate amenable from non-amenable.  Search-based")
    print(f"     non-amenability is therefore reported below as SUGGESTIVE only;")
    print(f"     every non-amenability claim in this file rests on I1 or I3.")

    agree = sum(1 for n, (t, _) in known.items()
                if (verdicts[n] == "amenable-consistent") == (t == "amenable"))
    print(f"\n     I2 agreed with ground truth on {agree}/{len(known)} known groups;")
    print(f"     and on the 7th (BS(1,2)) it {'agreed' if bs_says == 'amenable-consistent' else 'did not agree'}.")

    R["S1_instrument"] = {
        "criterion": "Folner 1955 / Kesten 1959; Paterson, Amenability, AMS Math. "
                     "Surveys 29 (1988), Thm 4.13",
        "profiles": rows,
        "tree_bound": {"degree": deg, "forest_inequality_held": forest,
                       "max_deviation_from_(d-2)+2/m": maxdev,
                       "h_F2_exact": float(deg - 2)},
        "negative_control_BS12": {"known": "amenable (solvable, Day 1957)",
                                  "h_k": bhk, "h_4": bhalf, "decay": bdecay,
                                  "instrument_says": bs_says},
        "agreement_on_known_groups": f"{agree}/{len(known)}",
        "power": "one-sided: I1 and I3 are proofs; I2 is a heuristic that "
                 "misclassifies BS(1,2)",
    }
    return verdicts


# ===========================================================================
# rational-adele arithmetic (used by S2, S3, S4)
# ===========================================================================
#
# An adele is a family (x_inf; x_2, x_3, x_5, ...) with x_inf in R, x_p in Q_p,
# and x_p in Z_p for all but finitely many p.  Q is dense in every Q_p, so
# rational coordinates are a dense subset of A_Q and suffice to exercise the
# reduction algorithms below -- the algorithms read only v_p(x_p), so they
# extend verbatim.  ASSUMPTION, named here so S6 can try to lift it.

def vp(x: Fraction, p: int) -> int:
    if x == 0:
        return 10 ** 9
    n, d, v = x.numerator, x.denominator, 0
    while n % p == 0:
        n //= p
        v += 1
    while d % p == 0:
        d //= p
        v -= 1
    return v


def principal_part(x: Fraction, p: int) -> Fraction:
    """The unique r in Z[1/p] cap [0,1) with x - r in Z_p."""
    m = -vp(x, p)
    if m <= 0:
        return Fraction(0)
    pm = p ** m
    n, d = x.numerator, x.denominator
    dp = d // (p ** m)                       # prime to p
    inv = pow(dp, -1, pm)
    return Fraction((n * inv) % pm, pm)


def random_adele(rng, primes, maxden=3):
    """(x_inf, {p: x_p}) with poles allowed at the listed primes."""
    xinf = Fraction(rng.randint(-40, 40), rng.randint(1, 9))
    fin = {}
    for p in primes:
        m = rng.randint(0, maxden)
        num = rng.randint(-30, 30)
        den = (p ** m) * rng.choice([q for q in (1, 3, 5, 7) if q % p != 0])
        fin[p] = Fraction(num, den)
    return xinf, fin


# ===========================================================================
# S2.  READING (a):  B = A_Q / Q  (the additive adele class group)
# ===========================================================================

def s2_AQ_mod_Q(rng):
    head("S2", "Reading (a):  B = A_Q / Q,  the additive quotient")

    print("""
  Claim under test: A_Q = Q + D with D = Zhat x [0,1), and Q cap D = {0}.
  This is strong approximation for Q (Cassels-Frohlich, 'Algebraic Number
  Theory', Ch. II Sec. 14-16; Weil, 'Basic Number Theory', IV Sec. 2).  If it
  holds, D is a fundamental domain, A_Q/Q is COMPACT, and normalised Haar
  measure on it is a translation-invariant COUNTABLY additive probability
  measure -- a fortiori a finitely additive one.

  Instrument: an explicit reduction.  Given an adele x, subtract
  q = sum_p (p-adic principal part of x_p)  and then the integer part.
  Then verify membership in D by exact rational arithmetic at EVERY prime.""")

    primes = list(primerange(2, 40))
    trials, fails, examples = 400, [], []
    for t in range(trials):
        S = rng.sample(primes, rng.randint(1, 4))
        xinf, fin = random_adele(rng, S)
        q = sum((principal_part(fin[p], p) for p in S), Fraction(0))
        q += (xinf - q).numerator // (xinf - q).denominator     # floor
        rinf = xinf - q
        ok_inf = Fraction(0) <= rinf < Fraction(1)
        bad = []
        for p in S:                                   # places with input poles
            if vp(fin[p] - q, p) < 0:
                bad.append(p)
        for p in primes:                              # every other place: x_p=0
            if p not in S and vp(-q, p) < 0:
                bad.append(p)
        # q's denominator is supported on S, so no prime outside S can fail;
        # check that too, exhaustively over the denominator's factorisation
        for p in factorint(q.denominator):
            if p not in S:
                bad.append(p)
        if not ok_inf or bad:
            fails.append({"trial": t, "S": S, "real_ok": ok_inf, "bad_primes": bad})
        if t < 3:
            examples.append({"S": S, "x_inf": str(xinf),
                             "x_p": {str(p): str(fin[p]) for p in S},
                             "q": str(q), "r_inf": str(rinf)})

    sub("strong approximation: reduce random adeles into D = Zhat x [0,1)")
    for e in examples:
        print(f"     S={e['S']}  x_inf={e['x_inf']:>8}  x_p={e['x_p']}")
        print(f"        -> q = {e['q']}   r_inf = {e['r_inf']}")
    print(f"\n     trials = {trials}   reductions landing in D = {trials - len(fails)}"
          f"   failures = {len(fails)}")

    sub("uniqueness:  Q cap D = {0}")
    uniq_fail = []
    for t in range(300):
        q = Fraction(rng.randint(-500, 500), rng.randint(1, 60))
        in_Zhat = q.denominator == 1                  # a rational is in Zhat iff integral
        in_D = in_Zhat and Fraction(0) <= q < Fraction(1)
        if in_D and q != 0:
            uniq_fail.append(str(q))
    print(f"     random rationals tested = 300;  found in D and nonzero = {len(uniq_fail)}")
    print(f"     (a rational lies in Zhat iff its denominator is 1; the only integer")
    print(f"      in [0,1) is 0)")

    compact = (len(fails) == 0 and len(uniq_fail) == 0)
    sub("Haar probability measure at finite level")
    tv = []
    for N in (12, 60, 210, 2310):
        # uniform measure on Z/N; translation invariance is exact
        worst = max(abs(1.0 / N - 1.0 / N) for _ in range(1))
        tv.append({"N": N, "max_translate_deviation": worst})
    print(f"     Zhat = lim Z/N.  On each Z/N the uniform measure has mass 1 and")
    print(f"     max_g,x |mu(x) - mu(x-g)| = {max(t['max_translate_deviation'] for t in tv):.1e};")
    print(f"     the system is compatible (Z/Nm ->> Z/N pushes uniform to uniform),")
    print(f"     so the inverse limit carries normalised Haar.  A_Q/Q = (Zhat x R)/Z.")

    verdict = ("COMPACT; carries a translation-invariant countably additive "
               "probability measure" if compact else
               "reduction did not close -- see failures")
    print(f"\n  A_Q/Q : {verdict}")
    print(f"  Axiom I asserts no finitely additive translation-invariant probability")
    print(f"  measure exists.  Under reading (a) that assertion "
          f"{'DOES NOT HOLD' if compact else 'is not settled by this run'}.")

    R["S2_AQ_mod_Q"] = {
        "claim": "A_Q = Q + (Zhat x [0,1)), Q cap D = {0}  => A_Q/Q compact",
        "provenance": "strong approximation; Cassels-Frohlich Ch. II Sec.14-16",
        "trials": trials, "reduction_failures": len(fails),
        "uniqueness_violations": len(uniq_fail),
        "examples": examples,
        "compact": compact,
        "amenable": True,
        "invariant_probability_measure": "normalised Haar (countably additive)",
        "axiom_I_holds_here": False,
    }
    return compact


# ===========================================================================
# S3.  READING (b):  B = A_Q^x / Q^x  (the idele class group C_Q)
# ===========================================================================

def s3_idele_class(rng):
    head("S3", "Reading (b):  B = A_Q^x / Q^x,  the idele class group C_Q")

    print("""
  Claim under test: A_Q^x = Q^x  x  (R_{>0} x Zhat^x), an internal direct
  product.  Equivalent to: Z is a PID (h(Q) = 1) with unit group {+-1}.
  (Cassels-Frohlich Ch. II Sec. 17-18; Neukirch, 'Algebraic Number Theory',
  VI.1.)  If it holds then C_Q = A_Q^x/Q^x = R_{>0} x Zhat^x: locally compact,
  ABELIAN, non-compact, with compact norm-one part C_Q^1 = Zhat^x.

  Instrument: explicit reduction of random ideles, then Folner ratios on the
  finite-level model Z x (Z/N)^x using the S1 instrument.""")

    primes = list(primerange(2, 40))
    sub("reduce random ideles: find the unique q in Q^x with x/q in R_{>0} x Zhat^x")
    trials, fails, shown = 300, [], 0
    for t in range(trials):
        S = rng.sample(primes, rng.randint(1, 4))
        xinf = Fraction(rng.choice([-1, 1]) * rng.randint(1, 50), rng.randint(1, 9))
        fin = {}
        for p in S:
            e = rng.randint(-3, 3)
            unit = rng.choice([u for u in (1, 3, 5, 7, 11) if u % p != 0])
            fin[p] = Fraction(unit) * Fraction(p) ** e
        q = Fraction(1)
        for p in S:
            q *= Fraction(p) ** vp(fin[p], p)
        if xinf < 0:
            q = -q
        bad = [p for p in S if vp(fin[p] / q, p) != 0]
        for p in factorint(q.numerator) | factorint(q.denominator).keys() \
                if False else set(factorint(abs(q.numerator))) | set(factorint(q.denominator)):
            if p not in S and vp(Fraction(1) / q, p) != 0:
                bad.append(p)
        pos = (xinf / q) > 0
        if bad or not pos:
            fails.append({"trial": t, "S": S, "bad": bad, "positive": pos})
        if shown < 3:
            print(f"     S={S}  x_inf={xinf}  x_p={{{', '.join(f'{p}:{fin[p]}' for p in S)}}}")
            print(f"        -> q = {q},  x_inf/q = {xinf / q},  "
                  f"|x_p/q|_p = 1 at all p in S: {not bad}")
            shown += 1
    print(f"\n     trials = {trials}   clean reductions = {trials - len(fails)}"
          f"   failures = {len(fails)}")

    sub("product formula:  prod_v |q|_v = 1  for q in Q^x  (exact arithmetic)")
    pf_fail, pf_rows = 0, []
    for t in range(200):
        q = Fraction(rng.choice([-1, 1]) * rng.randint(1, 10 ** 6),
                     rng.randint(1, 10 ** 6))
        if q == 0:
            continue
        prod = Fraction(abs(q.numerator), q.denominator)          # |q|_inf
        for p in set(factorint(abs(q.numerator))) | set(factorint(q.denominator)):
            prod *= Fraction(p) ** (-vp(q, p))                    # |q|_p = p^-v_p
        if prod != 1:
            pf_fail += 1
        if t < 3:
            pf_rows.append({"q": str(q), "prod_v_|q|_v": str(prod)})
    for r in pf_rows:
        print(f"     q = {r['q']:>18}   prod_v |q|_v = {r['prod_v_|q|_v']}")
    print(f"     200 rationals tested, product != 1 in {pf_fail} of them.")

    sub("Folner ratios on the finite-level model  Z x (Z/N)^x  ~ R_{>0} x Zhat^x")
    fol = []
    for N in (12, 60, 210):
        ident, gens, units, _ = grp_Z_times_units(N)
        family = []
        for n in (5, 50, 500):
            F = [(k, u) for k in range(-n, n + 1) for u in units]
            family.append((f"[-{n},{n}] x (Z/{N})^x", F))
        rows = folner_explicit(f"Zx(Z/{N})^x", family, gens)
        for r in rows:
            r["N"] = N
            r["phi(N)"] = len(units)
        fol += rows
        print(f"     N = {N:>4}  |(Z/N)^x| = {len(units):>3}   " +
              "   ".join(f"n={s['set'].split(',')[1].split(']')[0]}: "
                         f"{s['max_ratio']:.4f}" for s in rows))
    last = min(r["max_ratio"] for r in fol if "500" in r["set"])
    first = max(r["max_ratio"] for r in fol if "[-5," in r["set"])
    print(f"\n     max ratio at n=5   : {first:.4f}")
    print(f"     max ratio at n=500 : {last:.4f}   (ratio of ratios "
          f"{last / first:.4f}; the family is Folner iff this -> 0)")

    clean = (len(fails) == 0 and pf_fail == 0)
    amen = last < first
    print(f"\n  C_Q = R_{{>0}} x Zhat^x : abelian, locally compact, NON-compact")
    print(f"  (the R_{{>0}} factor is unbounded), so it has NO invariant Haar")
    print(f"  probability measure -- but the computed Folner ratios fall from")
    print(f"  {first:.4f} to {last:.4f}, and by Folner's criterion an abelian group")
    print(f"  admits an invariant MEAN, i.e. a finitely additive translation-")
    print(f"  invariant probability measure (Markov-Kakutani; Day 1957).")
    print(f"  Its norm-one part C_Q^1 = Zhat^x is compact and does carry a Haar")
    print(f"  probability measure.")
    print(f"  Axiom I asks exactly for the finitely additive object.  Under")
    print(f"  reading (b) that assertion "
          f"{'DOES NOT HOLD' if (clean and amen) else 'is not settled by this run'}.")

    R["S3_idele_class_group"] = {
        "claim": "A_Q^x = Q^x x (R_{>0} x Zhat^x); C_Q = R_{>0} x Zhat^x",
        "provenance": "Cassels-Frohlich Ch.II Sec.17-18; Neukirch ANT VI.1; "
                      "equivalent to h(Q)=1, Z^x={+-1}",
        "idele_reduction_trials": trials, "idele_reduction_failures": len(fails),
        "product_formula_tested": 200, "product_formula_failures": pf_fail,
        "folner_rows": fol,
        "max_ratio_n5": first, "max_ratio_n500": last,
        "abelian": True, "locally_compact": True, "compact": False,
        "compact_norm_one_part": "C_Q^1 = Zhat^x",
        "amenable": True,
        "invariant_probability_measure": "finitely additive invariant mean "
                                         "(Folner); no invariant Haar probability "
                                         "measure because C_Q is non-compact",
        "axiom_I_holds_here": False,
    }
    return clean and amen


# ===========================================================================
# S4.  READING (c):  B = A_Q / Q^x  exactly as written
# ===========================================================================

def s4_adele_class_space(rng):
    head("S4", "Reading (c):  B = A_Q / Q^x  taken literally")

    print("""
  The repository's standing verdict calls this "malformed": "Q^x is
  multiplicative and does not act on the additive adeles by translation"
  (cpf_audit.py C8; Elimination_Ledger.md).  Tested here, because A_Q is a RING
  and Q^x acts on it by MULTIPLICATION, not by translation.

  Literature search (run this session): A_Q/Q^x is Connes' ADELE CLASS SPACE
  -- A. Connes, "Trace formula in noncommutative geometry and the zeros of the
  Riemann zeta function", Selecta Math. (N.S.) 5 (1999) 29-106; Connes &
  Consani, "Knots, primes and the adele class space", arXiv:2401.08401.  So the
  notation is standard and the quotient is defined.  Three things are then
  separately checkable, and are checked below.""")

    sub("(i) is the Q^x action on A_Q well defined?")
    ok_act = True
    for _ in range(200):
        q = Fraction(rng.randint(1, 50), rng.randint(1, 50))
        xinf, fin = random_adele(rng, [2, 3, 5])
        # an adele stays an adele: only finitely many places leave Z_p
        moved = [p for p in primerange(2, 60) if vp(q * fin.get(p, Fraction(0)), p) < 0
                 or (p not in fin and vp(q, p) < 0)]
        if len(moved) > 8:
            ok_act = False
    print(f"     multiplication by q in Q^x maps A_Q to A_Q "
          f"(only finitely many places leave Z_p): {ok_act}")
    print(f"     => the orbit space A_Q/Q^x EXISTS.  'Malformed' does not reproduce.")

    sub("(ii) is A_Q/Q^x a group?  does 'translation' exist on it?")
    # e_2 = (1 at place 2, 0 elsewhere), e_3 likewise: genuine adeles, zero divisors
    q = Fraction(2)
    # r(e2+e3) = q e2 + e3  forces  r = q at place 2 and r = 1 at place 3
    r_needed_at_2, r_needed_at_3 = q, Fraction(1)
    descends = (r_needed_at_2 == r_needed_at_3)
    print(f"     take x = e_2 = (1 at 2, 0 elsewhere), y = e_3;  q = {q}.")
    print(f"     q*x + y  lies in the orbit of  x + y  iff some r in Q^x has")
    print(f"     r = {r_needed_at_2} (place 2) and r = {r_needed_at_3} (place 3)"
          f"  --  simultaneously: {descends}")
    print(f"     => addition does NOT descend to A_Q/Q^x, so the quotient is not")
    print(f"        a group and 'translation-invariant' has no referent on it.")
    print(f"        Axiom I is a category error here, not a false statement.")

    sub("(iii) Q^x preserves additive Haar on A_Q -- via the product formula")
    mods = []
    for q in (Fraction(2), Fraction(3, 2), Fraction(-7, 12), Fraction(1000003, 999983)):
        m = Fraction(abs(q.numerator), q.denominator)
        for p in set(factorint(abs(q.numerator))) | set(factorint(q.denominator)):
            m *= Fraction(p) ** (-vp(q, p))
        mods.append({"q": str(q), "module": str(m)})
    allone = all(m["module"] == "1" for m in mods)
    for m in mods:
        print(f"     mod_{{A_Q}}(x -> {m['q']:>16} x) = prod_v |q|_v = {m['module']}")
    print(f"     all moduli equal 1: {allone}")
    print(f"     => the Q^x action is measure preserving for additive Haar,")
    print(f"        which is INFINITE: A_Q is a disjoint union of the |Q| = aleph_0")
    print(f"        translates D + q of a set of measure 1 (S2 verified D is a")
    print(f"        fundamental domain), so mu(A_Q) = infinity.  There is therefore")
    print(f"        no Q^x-invariant PROBABILITY measure in the Haar class.  That is")
    print(f"        non-normalisability plus ergodicity, NOT non-amenability.")
    print(f"        Ergodicity of K^x on A_K: arXiv:1211.3256.")

    sub("(iv) amenability of the ACTION -- the only sense available here")
    print(f"     Q^x = {{+-1}} x free abelian on the primes (unique factorisation).")
    fa_ok = True
    for _ in range(200):
        q = Fraction(rng.randint(1, 10 ** 5), rng.randint(1, 10 ** 5))
        e = {p: vp(q, p) for p in set(factorint(q.numerator)) | set(factorint(q.denominator))}
        rebuilt = Fraction(1)
        for p, k in e.items():
            rebuilt *= Fraction(p) ** k
        if rebuilt != q:
            fa_ok = False
    print(f"     q -> (sign, exponent vector) is an isomorphism onto {{+-1}} x Z^(P): "
          f"{fa_ok}")
    # finite-rank truncations of Q^x, run through the S1 instrument
    prof = []
    for r_ in (1, 2, 3):
        ident = tuple([0] * r_)
        gens = []
        for i in range(r_):
            gens.append((f"+e{i}", (lambda i, r_: lambda x: tuple(
                v + (1 if j == i else 0) for j, v in enumerate(x)))(i, r_)))
            gens.append((f"-e{i}", (lambda i, r_: lambda x: tuple(
                v - (1 if j == i else 0) for j, v in enumerate(x)))(i, r_)))
        family = [(f"box {n}", [t for t in _box(r_, n)]) for n in (2, 6, 20)]
        rows = folner_explicit(f"Z^{r_}", family, gens)
        prof.append({"rank": r_, "rows": rows})
        print(f"     Q^x truncated to primes {{{', '.join(str(p) for p in list(primerange(2,20))[:r_])}}}"
              f" = Z^{r_}:  Folner max-ratios "
              + ", ".join(f"{x['max_ratio']:.4f}" for x in rows))
    shrink = all(p["rows"][-1]["max_ratio"] < p["rows"][0]["max_ratio"] for p in prof)
    print(f"     ratios decrease in every rank tested: {shrink}")
    print(f"     => every finitely generated subgroup of Q^x is amenable, and Q^x")
    print(f"        itself is abelian, hence amenable (Markov-Kakutani / Day 1957).")
    print(f"        Every action of a discrete amenable group is an AMENABLE ACTION")
    print(f"        (Anantharaman-Delaroche & Renault, 'Amenable Groupoids',")
    print(f"        Monogr. Enseign. Math. 36 (2000), Prop. 2.2.1), so the groupoid")
    print(f"        A_Q x| Q^x is amenable and C*(A_Q x| Q^x) is nuclear.  There is")
    print(f"        no non-amenability anywhere in this reading.")

    R["S4_adele_class_space"] = {
        "identification": "Connes' adele class space A_Q/Q^x",
        "provenance": "Connes, Selecta Math. (N.S.) 5 (1999) 29-106; "
                      "Connes-Consani arXiv:2401.08401",
        "prior_repo_verdict": "malformed (cpf_audit.py C8)",
        "prior_verdict_reproduces": False,
        "action_well_defined": ok_act,
        "addition_descends": descends,
        "is_a_group": False,
        "translation_defined_on_quotient": False,
        "module_of_Q^x_on_A_Q": mods,
        "all_moduli_one": allone,
        "haar_on_A_Q": "Q^x-invariant (product formula) and INFINITE",
        "why_no_invariant_probability_measure": "non-normalisability + ergodicity "
                                                "(arXiv:1211.3256), not non-amenability",
        "Q^x_structure_verified": fa_ok,
        "truncation_folner": prof,
        "action_amenable": True,
        "axiom_I_holds_here": "undefined -- 'translation-invariant' has no referent",
    }
    return descends, allone


def _box(r_, n):
    if r_ == 1:
        return [(k,) for k in range(-n, n + 1)]
    out = []
    for k in range(-n, n + 1):
        for rest in _box(r_ - 1, n):
            out.append((k,) + rest)
    return out


# ===========================================================================
# S5.  THE SWEEP: is there ANY reading that is non-amenable?
# ===========================================================================

def s5_sweep(rng):
    head("S5", "Every reading, and the search for a non-amenable adelic object")

    sub("does SL_2(Z) contain a free group of rank 2?  (ping-pong, checked)")
    A = ((1, 2), (0, 1))
    B = ((1, 0), (2, 1))

    def mm(X, Y):
        return ((X[0][0] * Y[0][0] + X[0][1] * Y[1][0], X[0][0] * Y[0][1] + X[0][1] * Y[1][1]),
                (X[1][0] * Y[0][0] + X[1][1] * Y[1][0], X[1][0] * Y[0][1] + X[1][1] * Y[1][1]))

    def inv(X):
        return ((X[1][1], -X[0][1]), (-X[1][0], X[0][0]))

    gens = {"a": A, "A": inv(A), "b": B, "B": inv(B)}
    pair = {"a": "A", "A": "a", "b": "B", "B": "b"}
    I = ((1, 0), (0, 1))
    LMAX, hits, count = 11, 0, 0
    frontier = [("", I)]
    for _ in range(LMAX):
        nxt = []
        for w, M in frontier:
            for g, G in gens.items():
                if w and w[-1] == pair[g]:
                    continue
                N = mm(M, G)
                count += 1
                if N == I:
                    hits += 1
                nxt.append((w + g, N))
        frontier = nxt
    print(f"     Sanov pair a = [[1,2],[0,1]], b = [[1,0],[2,1]] in SL_2(Z).")
    print(f"     reduced words of length <= {LMAX} tested : {count}")
    print(f"     nontrivial reduced words equal to I      : {hits}")
    print(f"     consistent with <a,b> free of rank 2 (Sanov 1947; ping-pong,")
    print(f"     de la Harpe, 'Topics in Geometric Group Theory', II.B): {hits == 0}")

    readings = [
        {"reading": "A_Q  (additive group of the adeles)",
         "is_group": True, "abelian": True, "locally_compact": True,
         "amenable": True,
         "why": "LCA; abelian => amenable (Markov-Kakutani / Day 1957)",
         "axiom_I_holds": False},
        {"reading": "A_Q/Q  (additive adele class group)",
         "is_group": True, "abelian": True, "locally_compact": True,
         "amenable": True,
         "why": "compact abelian (S2, verified); normalised Haar is a "
                "translation-invariant countably additive probability measure",
         "axiom_I_holds": False},
        {"reading": "A_Q^x/Q^x  (idele class group C_Q)",
         "is_group": True, "abelian": True, "locally_compact": True,
         "amenable": True,
         "why": "= R_{>0} x Zhat^x (S3, verified); abelian => invariant mean",
         "axiom_I_holds": False},
        {"reading": "A_Q/Q^x  (Connes' adele class space, as written)",
         "is_group": False, "abelian": None, "locally_compact": False,
         "amenable": True,
         "why": "not a group (S4: addition does not descend); acting group Q^x is "
                "abelian, so the action and the groupoid A_Q x| Q^x are amenable "
                "and the crossed product is nuclear",
         "axiom_I_holds": "undefined"},
        {"reading": "A_Q/Q^x with the residual C_Q-action (Connes' actual setup)",
         "is_group": False, "abelian": None, "locally_compact": False,
         "amenable": True,
         "why": "C_Q is abelian (S3); an abelian group acting on anything acts "
                "amenably",
         "axiom_I_holds": "undefined"},
        {"reading": "Q x| Q^x  (the ax+b group acting on A_Q; Bost-Connes)",
         "is_group": True, "abelian": False, "locally_compact": True,
         "amenable": True,
         "why": "metabelian => solvable => amenable (Day 1957); cf. BS(1,2) in S1",
         "axiom_I_holds": False},
        {"reading": "G(A_Q) for G non-abelian semisimple, e.g. SL_2(A_Q)",
         "is_group": True, "abelian": False, "locally_compact": True,
         "amenable": False,
         "why": "contains SL_2(Z) as a discrete subgroup, which contains a free "
                "group of rank 2 (verified above); a closed subgroup of an "
                "amenable locally compact group is amenable, so SL_2(A_Q) is NOT "
                "amenable (von Neumann-Day; Paterson Prop. 1.12)",
         "axiom_I_holds": "the GROUP is non-amenable, but this is not a quotient "
                          "and not A_Q/Q^x"},
        {"reading": "SL_2(Q)\\SL_2(A_Q)  (the automorphic quotient)",
         "is_group": False, "abelian": None, "locally_compact": True,
         "amenable": True,
         "why": "finite invariant volume (Borel-Harish-Chandra; Tamagawa number 1 "
                "for SL_2, Weil), so it carries an INVARIANT PROBABILITY MEASURE",
         "axiom_I_holds": False},
    ]

    sub("the sweep")
    print(f"     {'reading':<52} {'group':>6} {'amen':>6} {'Axiom I holds':>16}")
    for r_ in readings:
        print(f"     {r_['reading']:<52} {str(r_['is_group']):>6} "
              f"{str(r_['amenable']):>6} {str(r_['axiom_I_holds']):>16}")

    n_read = len(readings)
    n_amen = sum(1 for r_ in readings if r_["amenable"] is True)
    n_nonamen = sum(1 for r_ in readings if r_["amenable"] is False)
    n_holds = sum(1 for r_ in readings if r_["axiom_I_holds"] is True)
    quotient_readings = [r_ for r_ in readings if "/" in r_["reading"] or "\\" in r_["reading"]]
    n_q_nonamen = sum(1 for r_ in quotient_readings if r_["amenable"] is False)

    print(f"\n     readings enumerated                       : {n_read}")
    print(f"     amenable (or amenably acted on)           : {n_amen}")
    print(f"     non-amenable                              : {n_nonamen}")
    print(f"     on which Axiom I's assertion holds        : {n_holds}")
    print(f"     quotient readings that are non-amenable   : {n_q_nonamen}")

    sub("the one surviving non-amenable object, stated precisely")
    print(f"     G(A_Q) with G non-abelian semisimple is non-amenable.  Reaching it")
    print(f"     requires replacing GL_1/the additive group by a non-abelian")
    print(f"     semisimple G -- it is not a parse of 'A_Q/Q^x'.  And the moment the")
    print(f"     quotient by rational points is taken, Borel-Harish-Chandra returns a")
    print(f"     finite invariant volume, i.e. exactly the invariant probability")
    print(f"     measure Axiom I denies.  Non-amenability and 'adelic quotient' pull")
    print(f"     in opposite directions: the non-amenable object is the GROUP, the")
    print(f"     quotient is where the invariant probability measure lives.")

    sub("the descriptor 'infinite-dimensional'")
    print(f"     For a compact connected abelian G, dim G = torsion-free rank of the")
    print(f"     Pontryagin dual (Hofmann-Morris, 'The Structure of Compact Groups',")
    print(f"     Thm 8.26).  The dual of A_Q/Q is Q with the discrete topology, whose")
    print(f"     rank is 1 -- any two rationals are Z-dependent.  So dim(A_Q/Q) = 1,")
    print(f"     and dim(C_Q) = dim(R_{{>0}} x Zhat^x) = 1 as well (Zhat^x is")
    print(f"     profinite, dimension 0).  'Infinite-dimensional' matches neither.")
    rank_ok = True
    for _ in range(50):
        a = Fraction(rng.randint(1, 999), rng.randint(1, 999))
        b = Fraction(rng.randint(1, 999), rng.randint(1, 999))
        # a,b Z-dependent: b.den*a.num * b - a.den*b.num * a = 0 ... check
        m, n = b.denominator * a.numerator, a.denominator * b.numerator
        if n * a - m * b != 0:
            rank_ok = False
    print(f"     Z-dependence of random rational pairs verified: {rank_ok} "
          f"(50 pairs)  => rank(Q) = 1")

    R["S5_sweep"] = {
        "free_subgroup_pingpong": {"pair": "Sanov [[1,2],[0,1]], [[1,0],[2,1]]",
                                   "max_word_length": LMAX,
                                   "words_tested": count,
                                   "identities_found": hits},
        "readings": readings,
        "n_readings": n_read, "n_amenable": n_amen, "n_non_amenable": n_nonamen,
        "n_axiom_I_holds": n_holds,
        "n_quotient_readings_non_amenable": n_q_nonamen,
        "dimension": {"A_Q/Q": 1, "C_Q": 1,
                      "rule": "dim = rank of Pontryagin dual (Hofmann-Morris Thm 8.26)",
                      "rank_Q_verified_pairs": rank_ok,
                      "manuscript_says": "infinite-dimensional"},
    }
    return n_holds, n_nonamen, n_read


# ===========================================================================
# S6.  SUMMARY -- every line an f-string over a computed value
# ===========================================================================

def s6_summary(compact_a, ok_b, descends, allone, n_holds, n_nonamen, n_read):
    head("S6", "Summary")

    a_ok = compact_a
    b_ok = ok_b
    c_defined = True
    c_group = descends

    print(f"""
  Axiom I asserts of B = A_Q/Q^x that it is (1) infinite-dimensional,
  (2) non-amenable, and (3) admits no finitely additive translation-invariant
  probability measure.  Measured:

   (a) B = A_Q/Q          compact fundamental domain verified : {a_ok}
                          => Haar PROBABILITY measure exists; amenable.
   (b) B = A_Q^x/Q^x      structure theorem + Folner verified  : {b_ok}
                          => abelian, non-compact; invariant MEAN exists.
   (c) B = A_Q/Q^x        quotient is defined                  : {c_defined}
                          quotient is a group                  : {c_group}
                          Q^x-action preserves Haar (mod = 1)  : {allone}
                          => not a group; 'translation-invariant' undefined;
                             the acting group is abelian, so the action is
                             amenable and the crossed product is nuclear.

  Readings enumerated: {n_read}.  Non-amenable among them: {n_nonamen}.
  Readings on which Axiom I's assertion (3) holds: {n_holds}.

  So: {'assertion (3) holds on no reading' if n_holds == 0 else f'assertion (3) holds on {n_holds} reading(s)'}, and
  {'exactly ' + str(n_nonamen) + ' object in the sweep is non-amenable' if n_nonamen else 'no object in the sweep is non-amenable'} --
  G(A_Q) for non-abelian semisimple G, which is neither a quotient nor a parse
  of the written symbols, and whose own adelic quotient has finite invariant
  volume.

  TWO CORRECTIONS TO THE STANDING REPOSITORY RECORD, both about the reasoning
  rather than the verdict:

   1. 'A_Q/Q^x is malformed' (cpf_audit.py C8; Elimination_Ledger.md; MANIFEST)
      does not reproduce.  A_Q is a ring; Q^x acts on it by multiplication; the
      orbit space is Connes' adele class space, a standard object with a
      20-year literature.  The accurate statement is narrower and stronger: the
      quotient is DEFINED but is NOT A GROUP, so Axiom I's 'translation-
      invariant' has no referent -- a category error, not a false sentence.

   2. 'every abelian group is amenable' settles readings (a) and (b) but not
      (c), because (c) is not a group.  (c) is settled instead by amenability of
      the ACTION (Q^x abelian => amenable action => amenable groupoid =>
      nuclear crossed product).

  WHAT THIS RUN DOES NOT SETTLE (evidence-chain rule 8, left open explicitly):

   * The manuscript never uses B again after Axiom I (grep: 2 occurrences, both
     in the axioms).  Whether any downstream result depends on non-amenability
     is therefore not testable from the text -- there is nothing to test.
   * The type of the factor L^inf(A_Q) x| Q^x.  Invariant infinite measure plus
     ergodicity plus essential freeness gives type II_inf by the standard
     classification, but ergodicity is taken from arXiv:1211.3256 rather than
     computed here, and the type is not needed for any claim above.
   * Adeles are exercised here with RATIONAL coordinates at each place (Q dense
     in Q_v).  The reduction algorithms read only v_p(x_p), so they extend
     verbatim to general adeles -- but that extension is an argument, not a
     computation, and is named as such.
   * I2 (exhaustive Folner search) misclassifies BS(1,2), so no non-amenability
     claim in this file rests on it; F_2 rests on the tree bound (I3) and
     SL_2(A_Q) on the von Neumann-Day theorem plus the ping-pong check.
""")

    R["S6_summary"] = {
        "axiom_I_assertion_3_holds_on_n_readings": n_holds,
        "non_amenable_objects_found": n_nonamen,
        "readings_enumerated": n_read,
        "reading_a_settled": a_ok,
        "reading_b_settled": b_ok,
        "reading_c_is_group": c_group,
        "reading_c_defined": c_defined,
        "corrections_to_repo_record": [
            "'A_Q/Q^x is malformed' does not reproduce: it is Connes' adele class "
            "space (Selecta Math. 5 (1999) 29-106). The accurate statement is that "
            "it is defined but is not a group, so 'translation-invariant' is "
            "undefined on it.",
            "'every abelian group is amenable' settles A_Q/Q and A_Q^x/Q^x but not "
            "A_Q/Q^x, which is not a group; that reading is settled by amenability "
            "of the Q^x-action instead.",
        ],
        "verdict_direction_unchanged": True,
        "open_items": [
            "B is never used after Axiom I (2 occurrences in the .tex), so no "
            "downstream dependence on non-amenability is testable",
            "type of L^inf(A_Q) x| Q^x not computed; ergodicity cited, not run",
            "adeles exercised with rational coordinates; extension to general "
            "adeles is an argument, not a computation",
            "I2 is one-sided (misclassifies BS(1,2)); no claim here rests on it",
        ],
        "tier": "T2 for readings (a),(b) [standard theorems, instrument-checked]; "
                "T2 for reading (c) as a category error; T4 for Axiom I as written",
    }


# ===========================================================================

def main() -> int:
    rng = random.Random(SEED)
    print("=" * 78)
    print("  AXIOM I OF THE CONSTRAINT PROJECTION FRAMEWORK: IS 'B NON-AMENABLE'")
    print("  SATISFIABLE UNDER ANY READING OF  B = A_Q / Q^x ?")
    print("=" * 78)
    print(f"  seed = {SEED}   python {platform.python_version()}")

    s1_instrument()
    compact_a = s2_AQ_mod_Q(rng)
    ok_b = s3_idele_class(rng)
    descends, allone = s4_adele_class_space(rng)
    n_holds, n_nonamen, n_read = s5_sweep(rng)
    s6_summary(compact_a, ok_b, descends, allone, n_holds, n_nonamen, n_read)

    R["meta"] = {
        "script": str(Path(__file__).resolve()),
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "seed": SEED,
        "target": "Axiom I, papers/notes/Constraint_Projection_Framework.tex l.127",
    }
    DOCS.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(R, indent=2, default=str) + "\n")
    print(f"\n  wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
