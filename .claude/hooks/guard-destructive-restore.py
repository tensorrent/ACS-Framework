#!/usr/bin/env python3
"""PreToolUse guard: block a git restore that would discard uncommitted work.

Why this exists.  On 2026-09-01 a mutation test was undone with

    git checkout docs/Elimination_Ledger.md

to remove one appended line.  The file also carried twelve intentional,
uncommitted edits.  `git checkout <path>` restores the file to HEAD, so all
twelve were discarded silently -- exit code 0, no warning, nothing on stderr.
It was caught only by reading the file afterwards.

`git checkout <path>` is not a targeted undo.  It is a whole-file reset, and
it is unrecoverable: the overwritten content was never staged or committed, so
it is not in the object store and no reflog entry can bring it back.

This hook blocks such a command when the named paths have uncommitted changes,
and names the safe alternatives.  It does not fire when the file is clean --
restoring a clean file is a no-op.

Contract: reads a PreToolUse payload on stdin, exits 0 to allow, 2 to block
with the reason on stderr.
"""
import json
import re
import subprocess
import sys

# `git checkout <paths>` / `git restore <paths>` / `git checkout -- <paths>`.
# Branch operations (-b, -B, checkout <branch>) are not path restores.
RESTORE = re.compile(
    r"\bgit\s+(?:checkout|restore)\b(?P<rest>(?:\s+(?:--|--worktree|--staged|--source=\S+))*"
    r"(?:\s+[^\s;|&]+)+)")
NOT_A_RESTORE = re.compile(r"\bgit\s+(?:checkout|restore)\s+(-b|-B|--orphan|--track|--detach)\b")


def dirty(paths):
    """Return the subset of `paths` git reports as modified."""
    try:
        out = subprocess.run(["git", "status", "--porcelain", "--"] + paths,
                             capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return []
    hits = []
    for line in out.splitlines():
        status, _, name = line[:2], line[2:3], line[3:].strip()
        if status.strip() and not status.startswith("??"):
            hits.append(name)
    return hits


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if payload.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = payload.get("tool_input", {}).get("command", "")
    if not cmd or NOT_A_RESTORE.search(cmd):
        sys.exit(0)

    for m in RESTORE.finditer(cmd):
        toks = [t for t in m.group("rest").split()
                if not t.startswith("-") and t not in ("--",)]
        # A lone ref (no dot, no slash, no extension) is probably a branch.
        paths = [t for t in toks if ("/" in t or "." in t or t == ".")]
        if not paths:
            continue
        lost = dirty(paths)
        if lost:
            print(
                "BLOCKED: `git checkout/restore` on a path with uncommitted changes.\n"
                f"  command: {cmd.strip()[:160]}\n"
                f"  would discard uncommitted edits in: {', '.join(lost)}\n\n"
                "  This is a whole-file reset to HEAD, not a targeted undo, and the\n"
                "  overwritten content is unrecoverable -- it was never staged, so it is\n"
                "  not in the object store and no reflog entry restores it.\n\n"
                "  Safe alternatives:\n"
                "    * undo one appended line ..... sed -i '$ d' <file>\n"
                "    * undo a known edit .......... re-apply the inverse edit\n"
                "    * keep the work, then reset .. git stash push -- <file>\n"
                "    * you really mean it ......... git stash push -- <file> first,\n"
                "                                   so it stays recoverable\n\n"
                "  Origin: docs/Elimination_Ledger.md, 2026-09-01 (rule 12).",
                file=sys.stderr)
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
