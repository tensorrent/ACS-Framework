"""Does the tier-marker gate actually look at the whole ledger?

`test_every_entry_has_a_tier_marker` asserts that every ledger entry carries a
tier. This instrument measures what that test's own regex can and cannot see.
It was written because the ledger index surfaced entries with no tier marker
that the gate nevertheless passes -- and the gate passes them because of
exceptions this author wrote into the test after the fact.

A gate that is satisfied by its own escape hatches is not measuring anything.
This instrument reports coverage as a number so the claim "every entry has a
tier" can be read as "every entry the gate looks at", which is a weaker claim.

Exit code is non-zero if any finding below is unmeasurable, so the file cannot
pass by printing prose.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "Elimination_Ledger.md"
GATE = ROOT / "code" / "acs_codebase" / "tests" / "test_constraint_projection.py"

# The predicate the gate applies, copied verbatim from the test so this
# instrument measures the deployed regex and not a paraphrase of it.
GATE_SCANS = lambda line: line.startswith("### 202")
GATE_ACCEPTS = lambda line: bool(re.search(r"\bT[0-4]\b|NOT-FOUND|method\b", line))

# Headings that are document structure, not claims. Enumerated explicitly so
# that "structural" is a decision on the record rather than a regex accident.
#
# CORRECTION, same session, by the joint-coherence specialist: the first version of
# this file classified L413 as a "claim-shaped and untiered real escapee". It is not.
# L412 directly above it is `### 2026-06-06 -- Target Q3 (d,q) scaling law --
# **FALSIFIED (T4)**`, and L413 is that entry's continuation sub-heading. The tier is
# on the line above. The regex was right that L413 carries no tier of its own; the
# prose calling it an escapee was written from the regex output without reading the
# adjacent line -- the tenth instance in this corpus of prose composed beside a
# computation rather than from the object it describes. Continuation sub-headings are
# now a named category rather than an unhandled remainder.
STRUCTURAL = {
    "## TARGET QUEUE (priority order)",
    "## KILLS LOGGED",
    "## SESSION SCORECARD (2026-06-06)",
    "## REMAINING — all BLOCKED on inputs/constructions, not on swings",
    "## OOS01 RESULTS (2026-06-06, Mac via Antigravity) — reviewed & re-tiered",
    "## SCORECARD UPDATE (post-OOS01)",
    "### Swing now — cheap, decisive, high collapse",
    "### Build the kill test, then swing — highest collapse, needs a testbed",
    "### Continue the strip-mine — empty-tunnel mapping",
}

# Sub-headings that continue the entry immediately above them and inherit its tier.
# Membership is verified at runtime: the preceding heading must itself carry a tier,
# or the instrument exits rather than granting the inheritance on trust.
CONTINUATION = {
    "### (LMFDB unreachable from sandbox; zeros COMPUTED directly instead — better: reproducible)",
}


def verify_gate_regex_is_current() -> None:
    """The copied predicate must still match what the test file deploys."""
    src = GATE.read_text()
    if r'r"\bT[0-4]\b|NOT-FOUND|method\b"' not in src:
        sys.exit(
            "GATE DRIFT: test_constraint_projection.py no longer contains the "
            "regex this instrument measures. Update both together."
        )


def main() -> int:
    if not LEDGER.exists():
        sys.exit("ledger not found: " + str(LEDGER))
    verify_gate_regex_is_current()

    lines = LEDGER.read_text().splitlines()
    heads = [(i, l) for i, l in enumerate(lines, 1) if re.match(r"^#{2,3} ", l)]
    scanned = [(i, l) for i, l in heads if GATE_SCANS(l)]
    skipped = [(i, l) for i, l in heads if not GATE_SCANS(l)]

    print("=" * 72)
    print("GC1 -- how much of the ledger the tier gate looks at")
    print("=" * 72)
    print(f"  headings in the ledger (## or ###) : {len(heads)}")
    print(f"  headings the gate scans            : {len(scanned)}")
    print(f"  headings the gate never reads      : {len(skipped)}")
    cov = len(scanned) / len(heads)
    print(f"  coverage                           : {cov:.1%}")
    print()
    print("  The gate's claim is not 'every entry has a tier'. It is")
    print(f"  'every entry matching ### 202* has a tier' -- {len(skipped)} headings are")
    print("  outside the assertion entirely.")

    print()
    print("=" * 72)
    print("GC2 -- what is in the blind spot")
    print("=" * 72)
    blind_tiered, blind_structural, blind_cont, blind_untiered = [], [], [], []
    heading_lines = {i: l for i, l in heads}
    for i, l in skipped:
        if l.strip() in STRUCTURAL:
            blind_structural.append((i, l))
        elif l.strip() in CONTINUATION:
            # Do not take the inheritance on trust: find the nearest heading above
            # and require that IT carries a tier.
            prev = [(j, h) for j, h in heads if j < i]
            if not prev or not GATE_ACCEPTS(prev[-1][1]):
                sys.exit(
                    f"L{i} is listed as a continuation sub-heading, but the heading "
                    f"above it carries no tier to inherit. The exemption is unearned."
                )
            blind_cont.append((i, l, prev[-1][0]))
        elif GATE_ACCEPTS(l):
            blind_tiered.append((i, l))
        else:
            blind_untiered.append((i, l))
    print(f"  carry a tier anyway (gate would pass them)   : {len(blind_tiered)}")
    print(f"  document structure, not claims               : {len(blind_structural)}")
    print(f"  continuation sub-headings (tier is above)    : {len(blind_cont)}")
    for i, l, src in blind_cont:
        print(f"      L{i} inherits from L{src}: {heading_lines[src][:70]}")
    print(f"  claim-shaped AND untiered -- real escapees   : {len(blind_untiered)}")
    for i, l in blind_untiered:
        print(f"      L{i}: {l[:88]}")
    if not blind_untiered:
        print("      (none)")

    print()
    print("=" * 72)
    print("GC3 -- which of the gate's own exceptions have ever fired")
    print("=" * 72)
    counts = {"T0-T4": 0, "NOT-FOUND": 0, "method": 0, "REJECTED": 0}
    only_method, only_notfound = [], []
    for i, l in scanned:
        t = bool(re.search(r"\bT[0-4]\b", l))
        nf = bool(re.search(r"NOT-FOUND", l))
        me = bool(re.search(r"method\b", l))
        if t:
            counts["T0-T4"] += 1
        if nf:
            counts["NOT-FOUND"] += 1
        if me:
            counts["method"] += 1
        if not (t or nf or me):
            counts["REJECTED"] += 1
        if me and not (t or nf):
            only_method.append((i, l))
        if nf and not (t or me):
            only_notfound.append((i, l))
    for k, v in counts.items():
        print(f"  {k:<12}: {v}")
    print()
    print(f"  entries passing ONLY via the 'method' escape    : {len(only_method)}")
    for i, l in only_method:
        print(f"      L{i}: {l[:88]}")
    print(f"  entries passing ONLY via the 'NOT-FOUND' escape : {len(only_notfound)}")
    for i, l in only_notfound:
        print(f"      L{i}: {l[:88]}")
    if not only_notfound:
        print("      (none -- this branch of the gate has never fired on a")
        print("       scanned heading. It is unexercised surface in a test whose")
        print("       whole purpose is to be exercised.)")

    print()
    print("=" * 72)
    print("GC4 -- the gate reads headings only, never bodies")
    print("=" * 72)
    print("  A tier stated in an entry's body but absent from its heading FAILS")
    print("  the gate; a tier mentioned in a heading about someone else's claim")
    print("  PASSES it. The gate tests heading hygiene, not claim tiering.")
    print("  This is a scope statement, not a defect -- recorded so the test's")
    print("  name is not read as a stronger guarantee than it makes.")

    print()
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  coverage {cov:.1%}; {len(blind_untiered)} claim-shaped untiered heading(s) outside")
    print(f"  the assertion; {len(only_notfound)} entries have ever used the NOT-FOUND branch;")
    print(f"  {len(only_method)} entry passes only because an exception was added after it")
    print("  was written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
