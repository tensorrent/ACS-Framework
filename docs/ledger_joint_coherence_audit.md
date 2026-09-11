# Elimination Ledger — joint coherence audit

STATUS: in progress

Scope: `docs/Elimination_Ledger.md` (3,967 lines, 57 entries). Audit of whether the
ledger is internally coherent when read as a joint record: withdrawals recorded at
both ends, direct contradictions between entries, tier discipline, inventory.

Method: entries addressed by line range via a precomputed index; every finding below
quotes the actual text with line numbers. A refinement that was properly recorded at
both ends is not a defect and is reported as such.

---
