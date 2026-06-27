# extras/ — Heritage exploratory scripts

This directory contains ~100 exploratory scripts produced during the
development of the ACS framework. They are **not** part of the canonical
verification suite.

**Status:** unverified. Some are superseded; some contain results that
were later corrected in `src/`; some explore directions that did not
work out.

## Use these scripts to understand the development trajectory:

- `phase##_*.py` — numbered by phase of investigation; phase number
  approximately tracks chronology
- `acs_*.py` — early ACS framework scripts (often replaced)
- `task_*.py` — work split into tasks, mapping to specific paper sections
- `paper_b_*.py` — Paper B sector explorations
- `core_rope_*.py`, `frenet_*.py` — taxonomy instances
- `er_epr_*.py` — early ER=EPR comparison (superseded by
  `src/paper_c/er_epr_algebraic.py`)

## Do NOT use extras/ for verification.

The canonical, tested computations live in `src/`. Tests in `tests/`
verify only those modules. If you need to re-derive something that
appears only in `extras/`, port it into `src/` with proper test coverage
following the patterns established in the canonical modules.

## Some scripts were corrected in flight:

- `phase50_vacuum.py` — float64 catastrophic cancellation bug
  (corrected version uses Python `decimal`; see
  `src/paper_a/branch_a_vacuum.py`)
- `acs_vs_er_epr_test.py` — the "reconstruction error = 1" finding
  was a theorem, not a bug; superseded by
  `src/paper_c/er_epr_algebraic.py`
- `task1_tm1_redo.py` — symbolic TM1 matrix non-unitary; numerical
  formulas correct in `src/paper_a/tm1_pmns.py`

Reading these in their documented form is the recommended way to
understand the framework's adversarial-compression history. The clean
canonical form lives in `src/`.
