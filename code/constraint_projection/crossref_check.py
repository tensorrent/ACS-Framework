"""Do the ledger's internal line references point at what they claim?

The joint-coherence audit found that the dominant defect shape in this corpus is
not a wrong result -- it is a pointer. Five of its nine defects were a missing or
stale cross-reference: an entry corrected downstream with nothing at the original
end saying so, or a pointer naming an unlabelled target.

Inserting the repair markers reproduced the defect immediately: every `L<n>`
reference written into a marker went stale the moment a marker above it shifted
the file. Line numbers are this document's addressing scheme, and an addressing
scheme with no checker drifts on every edit.

This instrument checks two things:

  X1  every `L<n>` reference resolves to a line that exists and is not blank, and
      does not point at another cross-reference marker (a pointer at a pointer is
      drift, not a reference);
  X2  the anchored references -- the ones written by the 2026-09-11 audit repairs,
      where the intended target is known -- still land on their intended text.

Exits non-zero on any failure, so it can be wired into the gate.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs" / "Elimination_Ledger.md"

# (line number, substring that MUST appear on that line). Every pair here was
# read off the file at repair time; if an edit moves the target, this fails
# loudly instead of leaving a silently wrong pointer.
ANCHORS = [
    (370, "Q1 framework constants"),
    (378, "My session T2 verdicts upgrade to T1"),
    (97, "T1 upgrade path for every entry below"),
    (128, "T1 upgrade ="),
    (149, "All verdicts T2"),
    (328, "Constant T1-upgrades"),
    (417, "FALSIFIED (T4)"),
    (1300, "T0 INTRODUCED"),
    (2586, "does not force orientability"),
    (3040, "Method rule 11"),
    (3098, "Method rule 12"),
    (3919, "two unassessed legs"),
    (3824, "CORRECTS K2's mechanism"),
    (3881, "Michalke 1964"),
    # Added with the 2026-09-11 audit entry, whose own references were written
    # from pre-repair greps and were all stale on arrival. X1 passed them because
    # they resolved to real lines -- resolving is not the same as being right.
    (840, "is malformed"),
    (1005, "as literally written is"),
    (1398, "true but not ours"),
    (1401, "stands as a correct"),
    (2622, "made canon"),
    (3731, "A regulator"),
    (540, "Möbius-screw"),
    (390, "SCORECARD UPDATE"),
    (1478, "tiers never promote"),
    (11, "Tiers name the **ROUTE** the evidence took"),
]

MARKER = re.compile(r"^>\s+\*\*(SUPERSEDED|TIER RAISED|PART OF THIS FINDING|DATED SNAPSHOT|On the)")


def main() -> int:
    lines = LEDGER.read_text().splitlines()
    n = len(lines)
    failures = []

    print("=" * 70)
    print("X1 -- every L<n> reference resolves to real, non-empty, non-pointer text")
    print("=" * 70)
    refs = []
    for i, line in enumerate(lines, 1):
        # Two-to-four digits only. Single-digit `L1`..`L9` are the manuscript's
        # LEG labels ("**L2 - the RH leg**") and the Lebesgue norms ("L2
        # distance"), not line references. Excluding them is a real narrowing of
        # this check: a reference to a line below 10 would be missed. There are
        # no such lines to reference -- the file's first 9 lines are the header.
        for m in re.finditer(r"\bL(\d{2,4})(?:[–-](\d{2,4}))?\b", line):
            lo = int(m.group(1))
            hi = int(m.group(2)) if m.group(2) else lo
            refs.append((i, lo, hi))
    print(f"  references found : {len(refs)}")
    dangling = [r for r in refs if r[1] < 1 or r[2] > n or r[1] > r[2]]
    blank = [r for r in refs if 1 <= r[1] <= n and not lines[r[1] - 1].strip()]
    at_marker = [r for r in refs if 1 <= r[1] <= n and MARKER.match(lines[r[1] - 1])]
    print(f"  out of range     : {len(dangling)}")
    print(f"  land on a blank  : {len(blank)}")
    print(f"  point at a marker: {len(at_marker)}")
    for src, lo, hi in dangling:
        failures.append(f"L{src} references L{lo}-{hi}, outside a {n}-line file")
    for src, lo, hi in blank:
        failures.append(f"L{src} references L{lo}, which is blank")
    for src, lo, hi in at_marker:
        failures.append(f"L{src} references L{lo}, which is itself a pointer")

    print()
    print("=" * 70)
    print("X2 -- the audit's anchored references land on their intended text")
    print("=" * 70)
    ok = 0
    for ln, needle in ANCHORS:
        if ln > n:
            failures.append(f"anchor L{ln} is past end of file ({n} lines)")
            print(f"  L{ln:<5} MISSING  (past end of file)")
            continue
        got = lines[ln - 1]
        if needle in got:
            ok += 1
            print(f"  L{ln:<5} ok       {needle!r}")
        else:
            failures.append(f"anchor L{ln} should contain {needle!r}; found {got.strip()[:60]!r}")
            print(f"  L{ln:<5} DRIFTED  expected {needle!r}")
    print(f"\n  {ok}/{len(ANCHORS)} anchors hold")

    print()
    print("=" * 70)
    if failures:
        print(f"FAIL -- {len(failures)} cross-reference defect(s)")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("PASS -- every reference resolves and every anchor holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
