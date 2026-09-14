# Specialist report: stressing the fixed-point classification

**STATUS: in progress**

**Mission.** Try to break the corpus's own fixed-point classification, logged at
`docs/Elimination_Ledger.md` L3263-3266:

> A free action forces periodicity globally and the result is locally unobservable. A
> fixed-point action forces it locally and the result is a physical scale.

A classification that has only ever been confirmed has not been tested. This report attempts
falsification on cases that had no part in building the table.

**Instrument.** `code/constraint_projection/gauge_stress.py` (asserts + `sys.exit`).

**Tiers.** T0 machine-CHECKED / T1 machine / T2 proved / T3 measured / T4 falsified.
Literature facts are cited as literature, not labelled measurement.

---

## 0. What exactly is being tested

The ledger sentence (L3263-3266) bundles two conditionals:

| | antecedent | mechanism | consequent |
|---|---|---|---|
| **R-free** | the action is free | periodicity forced **globally** (topology) | the result is **locally unobservable** |
| **R-fix** | the action has a fixed point | periodicity forced **locally** (smoothness at the fixed point) | the result is a **physical scale** |

Three things are left unstated by the prose, and every one of them is a place the
classification can be attacked:

- **A1 — which space?** "Free" is a property of an action *on a space*, and the four worked
  rows do not use the same kind of space. Mobius: a deck action on a surface. Spinor: `{±I}`
  on the state sphere `S^3`. Zeta: `s -> 1-conj(s)` on `C`. Schwarzschild: Euclidean time
  translation on the Euclidean manifold. The spinor row is the sharpest illustration of why
  this matters: `{±I}` is **free on states** and **trivial on rays** — the same group, the same
  system, opposite ends of the classification depending on which space you name. The table
  names no space.
- **A2 — "forced" is load-bearing and unenforced.** R-free's antecedent is not "free action"
  alone but "free action *that forces* a periodicity." An imposed-but-not-forced period on a
  free action (a compactification radius, a chosen temperature) is a free action with a
  perfectly observable dimensionful period. If "forced" is dropped, R-free fails immediately;
  so the word has to be carried, and the prose carries it only in passing.
- **A3 — "physical scale" vs "pure number."** In Schwarzschild the forced period `beta = 8*pi*M`
  carries a dimension. In the spinor row the forced period `4*pi` does not. The table reads as
  though the fixed point is what supplies the dimension, but `8*pi*M = 8*pi` (a pure number
  from the smoothness condition) times `M` (an input already present in the metric). The pure
  number is what the topology/smoothness supplies in *both* rows. What actually differs is
  **whether the period is a function of local data at all.**

### Falsification shapes accepted in advance

- **F1** a free action whose forced periodicity yields a local dimensionful observable
  → breaks R-free. (Candidate: theta-vacua.)
- **F2** a fixed-point action whose periodicity yields only a sign / pure number and no scale
  → breaks R-fix. (Candidate: conical intersection.)
- **F3** a periodic structure where "free vs fixed point" is not well defined, or where the
  answer flips with the choice of space → the table has no content there (boundary).
- **F4** a scale-producing non-free action with no periodicity at all → R-fix's converse
  is unsupported. (Candidate: Gribov.)

### The sharpened criterion this report will test instead

Because of A3 the report also carries a second, mechanical statement of the same intuition,
which is what the instrument actually measures:

> **C** — a periodicity is *fixed-point type* iff the period is a function of local data at
> the fixed point, and *free type* iff the period is independent of all local data.

`C` is checkable by differentiation: vary the local data, watch the period. Wherever the prose
table and `C` disagree, that disagreement is reported, because the disagreement is the finding.

## 1. theta-vacua / instantons

(pending)

## 2. Aharonov-Bohm

(pending)

## 3. Berry phase at a conical intersection

(pending)

## 4. Gribov ambiguity

(pending)

## 5. Case of my own choosing

(pending)

## 6. Verdict

(pending)
