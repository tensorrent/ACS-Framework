---
name: evidence-chain
description: The evidence-chain discipline — every claim must carry the complete chain that produced it, and generation is reaction while verification is response. Use this whenever you are about to state that something passes, works, was verified, was checked, was run, is true, or holds; whenever you write a verification/status/summary section, a PR body, a test report, a commit message, or a research finding; whenever you carry a result forward from earlier context rather than re-observing it; and whenever you are auditing your own or someone else's claims. Load it BEFORE writing the claim, not after — the whole point is that a fluent claim and a verified claim feel identical from the inside, so the check has to be procedural rather than a matter of trying harder.
---

# The Evidence Chain

## The one idea

**Generation is reaction. Verification is response.**

Producing fluent, correct-shaped text is reflex — it happens the way a knee jerks. "The three
Lean files pass" is a *plausible continuation* of a sentence about Lean files. Writing it feels
exactly like reporting it. There is no internal signal that distinguishes the two.

That is the whole problem, and it is why "be careful" does not fix it. A reaction cannot be
caught by introspection because it does not feel like a reaction. It feels like knowing.

**Respond, don't react.** A response has something interposed between the prompt and the
output: an observation. The discipline below is that interposition, made procedural.

## The test

Before any claim leaves your hands:

> **Did you see it? Did you do it?**
> **If no — you are assuming.**

Not "is it probably true." Not "did I verify this at some point." *Did you observe it, in this
session, with a chain you can produce on demand.*

## What a complete chain is

A claim without its chain is a rumour you are laundering. A complete chain has four links, and
you must be able to produce all four:

| Link | Question | Failure if missing |
|---|---|---|
| **Claim** | What exactly is asserted? | Vague claims can't be falsified |
| **Instrument** | What command/code produced it? | "I checked" is not an instrument |
| **Observation** | What output was actually returned? | Paraphrase drifts from result |
| **Provenance** | When, in what environment, by whom? | Stale results masquerade as fresh |

Write the chain down where the claim lives. In a PR body that means the command and the
observed output, not the word "passing." In a ledger entry it means the numbers as printed. In
a commit message it means the gate result.

**If you cannot produce all four links, you have three honest options** — and exactly three:

1. **Go get the observation.** Usually cheapest. Run the thing.
2. **Mark it explicitly unverified.** "Carried forward from `<commit>`; not re-observed this
   session." A flagged gap is information. A silent one is a lie with good posture.
3. **Delete the claim.**

Softening the language is not a fourth option. "Should pass", "passes cleanly", and "I believe
passes" are all the same assertion wearing different clothes.

## The tell

You are reacting, not responding, when:

- The claim arrived **fully formed and felt obvious**. Verified facts come with friction — you
  remember running the thing. Reflexes arrive frictionless.
- You are writing a **summary** and the numbers are coming from memory of the run rather than
  from the run's output. Summaries are where reaction hides, because the reader can't see the
  gap between the section and the data.
- You are **carrying something forward** across a context boundary, a session, or a container.
  Environments change. `/tmp` gets cleared. A result observed two hours ago in another container
  is a claim, not an observation.
- The prose says one thing and **a number next to it says another.** This is the single most
  common form. See the catalogue below.
- You are writing **"verified", "confirmed", "clean", "all passing"** as an adjective rather
  than as a report of a specific observed output.

## Derive the conclusion from the result — never alongside it

This deserves its own section because it is the failure mode that recurs most, and it is
mechanical rather than moral.

When you write a summary line and a computation in the same breath, the summary is generated
from your *expectation* of the computation. They then drift independently. The number changes
when you fix a bug; the sentence does not.

**Bind the prose to the value.** In code, that means the conclusion string interpolates the
computed variable — never a literal you typed while looking at an earlier run. In prose, it
means quoting the output rather than characterising it.

```python
# reaction: the sentence and the number are independent
print("  ratio matches 2 pi")
print(f"  ratio = {ratio}")

# response: the sentence cannot survive the number changing
print(f"  ratio = {ratio:.4f}   vs 2 pi = {2*math.pi:.4f}   ({abs(ratio/(2*math.pi)-1)*100:.2f}%)")
```

## Real failures this discipline was built from

These are not hypotheticals. Each shipped, then had to be corrected. They are here because
recognising the *shape* is what transfers.

| What was written | What was true |
|---|---|
| "Three Lean files: exit 0" in a PR body | Not observed in that session — carried forward from earlier context |
| "Both papers compile clean, 3-pass" | Same — asserted, not run |
| `verified to 6.0e+00` printed beside the word "verified" | 6.0 is an enormous error; the comparison used a sign convention wrongly. Magnitudes were exact; the printed check was not |
| Summary said `31.9x` | The check computed `32.54x`; the summary hardcoded a stale value |
| "the same 2 pi" for a measured `7.222` | The prediction at that geometry was `7.256`. The precise statement was the *stronger* result |
| A `V =` line stating one coefficient | The ratio table directly above it printed `2.0` |
| "every member hits the target" | The table below said "no solution" for all 14 |
| `solve()` returned `[]`, prose claimed a root at 0 | The symbol was declared `positive=True`, excluding 0 |
| "re-running flips one field" | It flips one field *and* truncates precision across 42 rows |
| A "fairness note" giving three reasons a factor couldn't matter | Three *arguments*. The computation had not been done. (It agreed — that is the point: you cannot know until you run it) |

Notice how many are **prose contradicting a number in the same output**. That is the signature.

## The rules

Earned in order, each from a specific failure. They are operational, not aspirational.

1. **Evaluate the object the target actually defines** — not the object it claims that object
   equals. Solve it symbolically with the substitutions left out and see what is really there.
2. **Anchor every series to a number someone else published.** Inverting your own series with
   your own inputs proves only self-consistency.
3. **An instrument is not trusted until it has been shown capable of failing.** Validate against
   a known answer *before* using it. A test that cannot reject is not evidence.
4. **No result is logged as novel until a literature search has been run and recorded.**
   Judgement is not a search. One query has retired claims that felt original.
5. **Search your own corpus before the literature.** The sharpest finding is often already in
   your own files, dated earlier, in those words.
6. **Entries record state; they do not indict each other.** Append-only applies to what you
   *read*, not only what you write. State the checkable fact, not the verdict — the factual form
   is also the more useful one.
7. **Derive the printed conclusion from the computed result, never alongside it.**
8. **Run it to exhaustion; leave nothing outside.** An unclosed hedge is neither a dead end nor
   an open path. Any sentence conceding a limitation must be a computed result, an explicitly
   recorded open item, or removed. "It probably doesn't matter" is none of the three.
9. **Name the assumption a result rests on, then lift it.** An assumption never named cannot be
   lifted. If "planar" appears nowhere in your write-up but is baked into your
   parameterisation, no one — including you — can see what the result depends on.
10. **Did you see it? Did you do it? If no, you are assuming.** Apply it to your own
    verification claims first.

## Auditing what you have already written

Rules 8 and 10 are cheap to run and should be run routinely, not only when challenged.

Scan your own output for the language of an unfinished check:

```
"fairness note" | "caveat" | "not assessed" | "to leading order" | "at this order"
"approximate"   | "would need" | "should"    | "presumably"      | "left open"
"clean"         | "all passing" | "verified" | "confirmed"
```

For every hit, ask which of the three honest options applies. Then do that one.

A hit is not automatically a defect. Two of the most useful outcomes are: *"checked, correctly
scoped, not load-bearing"* and *"computed, and the original argument was right."* **A rule that
only pays out when it overturns something cannot be trusted when it stays silent** — you have to
run it to know which case you are in.

## Success is a gradient

Findings are not binary and should not be reported as a scoreboard.

A route that improved a prediction by 24× and then died is not a failure. A verdict confirmed by
independent re-derivation is not a null result — a claim that has survived two derivations is a
different object from one that survived a single pass. A finding withdrawn inside the run that
produced it is not an embarrassment; it is the fastest possible correction.

Record **direction and magnitude**. A dead end walked to the end and written down is permanent:
the next person does not have to walk it. Report what moved, how far, and which way — not
whether you won.

## Applying this

When you are about to make a claim:

1. **Name the claim precisely.** Vague claims cannot be checked, which is often why they are
   vague.
2. **Produce the four links** — or pick one of the three honest options.
3. **Bind the prose to the computed value** so they cannot drift.
4. **Name the assumptions** the result rests on, then try lifting them.
5. **Report the delta**, not a verdict.

The cost is small and pays immediately: a verification section reporting what was *watched* to
pass is worth more than one reporting what someone believes passed, and the gaps you name are
the ones nobody else has to discover.
