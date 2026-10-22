# Proposal E10: output-directory override for the sealed condensate_energy publishers

**Status:** proposal only. Nothing below has been applied.
**Date:** 2026-10-22

The eight `code/condensate_energy/publish_*.py` / `seal_*.py` entry points, and the two
helper modules two of them take `OUT` from, are listed in
`docs/publication/2026-09-24/publication-manifest.json` (lines 79–91 and the two helpers).
A manifest-bound file is not edited by an agent; the edit is proposed here, paste-ready,
for the owner to apply (or not) and then re-seal. The same override was applied directly
to the non-manifest instruments in this change set (`code/issue7/*`, `code/framed_unknot/*`,
`code/palpha_overlap/*`, `code/capacitance_ribbon/*`, `code/benchmark_efficiency.py`), so
the convention below is the one already in the tree.

## The convention

`ACS_OUT_DIR` is a stand-in for the repository's `docs/` root. Unset, every script writes
exactly where it writes today (default reproduces the current path byte-for-byte). Set,
`docs/` is replaced by `$ACS_OUT_DIR` and the rest of the path is kept, so a scratch run of
`publish_endpoint_audit.py` lands in `$ACS_OUT_DIR/condensate_energy/endpoint_audit/`.
Scripts that already use `argparse` also take `--out-dir`, which wins over the variable.

## One complication these scripts have that the issue7 ones do not

Every publisher **reads and writes the same directory**. It reads the committed inputs
(`results.json`, `provenance.json`, `visual-review.json`, `README.md`, …), renders a
figure into that directory, copies attempt logs in, then runs `OUT.rglob('*')` to census
the artifacts the receipt attests to, and finally writes `assessment.json` and
`receipt.json`. Redirecting `OUT` wholesale would therefore break the reads.

The proposal splits the two roles:

- `SRC` — the committed directory under `ROOT / 'docs'`. All reads stay here. Unchanged.
- `OUT` — where this run writes. Defaults to `SRC` (so nothing changes by default);
  under the override it is the same relative path under `$ACS_OUT_DIR`.

Two sites are genuinely ambiguous under an override and are the owner's decision, so the
proposal below leaves both **reading `SRC`** (the conservative choice: a receipt attests to
the committed tree, not to a scratch copy):

1. the `png_sha256` check (`publish_endpoint_audit.py:152`, `publish_source_endpoint.py:83`)
   compares `visual-review.json` against the PNG; a `--render-only` scratch run writes the
   PNG to `OUT`, a later `--seal` scratch run would check `SRC`. If the intent is to check
   the freshly rendered file, change that one `SRC` to `OUT`.
2. the artifact census (`OUT.rglob('*')` in every script) enumerates what the receipt
   hashes. Reading `SRC` keeps the receipt about the committed tree; reading `OUT` would
   make a scratch receipt about a scratch tree. The proposal reads `SRC`.

Also note every publisher copies attempt logs from `/private/tmp/<log>`, a macOS path; that
is independent of this proposal and is left alone.

## Paste-ready edits

Each block replaces the two-line `ROOT`/`OUT` header shown and adds the `--out-dir` flag
where the script has a parser. Line numbers are as of commit `badb0b7`. The style
(spaces vs. compact) matches each file.

### `code/condensate_energy/publish_endpoint_audit.py`

Replace lines 20–21:

```python
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy/endpoint_audit'
```

with:

```python
ROOT = Path(__file__).resolve().parents[2]
# SRC is the committed directory every read comes from. OUT is where this run
# writes; it is SRC unless ACS_OUT_DIR (or --out-dir) redirects it to a scratch
# tree, so a rerun never overwrites the sealed receipt.
SRC = ROOT / 'docs/condensate_energy/endpoint_audit'


def out_dir(override=None):
    override = (override or os.environ.get('ACS_OUT_DIR', '')).strip()
    if not override:
        return SRC
    return Path(override).expanduser() / SRC.relative_to(ROOT / 'docs')


OUT = out_dir()
```

Then change the reads to `SRC` — lines 29, 141, 144, 152 and 173 (`OUT / name`,
`OUT / 'README.md'`, `OUT / target...`, `digest(OUT / 'endpoint-boundary.png')`,
`OUT.rglob('*')`) — and leave the writes on `OUT` (lines 77, 149, 169, 178). Before the
first write in each of `render_endpoint_audit` and `seal_endpoint_audit` add
`OUT.mkdir(parents=True, exist_ok=True)` (and `(OUT / 'attempts').mkdir(...)` before
line 149). In `__main__` (lines 185–189) add the flag and rebind:

```python
    parser = argparse.ArgumentParser()
    parser.add_argument('--out-dir', default=None,
                        help='write artifacts under this directory instead of docs/ '
                             '(overrides ACS_OUT_DIR); default: docs/')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--render-only', action='store_true')
    mode.add_argument('--seal', action='store_true')
    args = parser.parse_args()
    if args.out_dir:
        OUT = out_dir(args.out_dir)
```

### `code/condensate_energy/publish_selection_energy.py`

Same shape as above (this file uses the spaced style). Replace lines 15–16 with the
`SRC` / `out_dir()` / `OUT` block, substituting `'docs/condensate_energy/selection_energy'`.
Reads to `SRC`: lines 56, 71, 76, 99. Writes stay on `OUT`: lines 49, 75, 95, 103. Add
the `--out-dir` flag to the parser at lines 109–113 and the `if args.out_dir:` rebind
after `parse_args()`.

### `code/condensate_energy/publish_family_boundary.py` (compact style)

Replace lines 14–15:

```python
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/family_boundary'
```

with:

```python
ROOT=Path(__file__).resolve().parents[2]
# SRC: committed inputs (reads). OUT: this run's writes; SRC unless ACS_OUT_DIR or
# --out-dir points at a scratch tree, so a rerun never overwrites the sealed receipt.
SRC=ROOT/'docs/condensate_energy/family_boundary'
def out_dir(override=None):
    override=(override or os.environ.get('ACS_OUT_DIR','')).strip()
    return Path(override).expanduser()/SRC.relative_to(ROOT/'docs') if override else SRC
OUT=out_dir()
```

Reads to `SRC`: lines 19, 50, 63, 67, 84. Writes stay on `OUT`: lines 44, 66, 81, 88.
Parser (lines 94–96):

```python
    parser=argparse.ArgumentParser();mode=parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('--out-dir',default=None,help='write under this directory instead of docs/ (overrides ACS_OUT_DIR)')
    mode.add_argument('--render-only',action='store_true');mode.add_argument('--seal',action='store_true')
    args=parser.parse_args()
    if args.out_dir:OUT=out_dir(args.out_dir)
```

### `code/condensate_energy/publish_input_closure.py` (compact style)

As `publish_family_boundary.py`, with `'docs/condensate_energy/input_closure'` at lines
17–18. Reads to `SRC`: lines 22, 23, 59, 90, 97. Writes stay on `OUT`: lines 52, 75, 94,
101. Parser at lines 107–109 (the group variable is named `group` here, not `mode`).

### `code/condensate_energy/publish_source_endpoint.py` (compact style)

As `publish_family_boundary.py`, with `'docs/condensate_energy/source_endpoint'` at lines
14–15. Reads to `SRC`: lines 19, 45, 47, 81, 83, 98. Writes stay on `OUT`: lines 39, 69,
80, 95, 102. Parser at lines 108–110.

### `code/condensate_energy/seal_action_matching.py` (no parser → env var only)

Replace lines 14–15 with the spaced-style `SRC` / `out_dir()` / `OUT` block, substituting
`'docs/condensate_energy/action_matching'`. Reads to `SRC`: lines 19, 87. Writes stay on
`OUT`: lines 52, 54 (`attempts = OUT / 'attempts'` — add `parents=True` to the `mkdir`
on line 55), 76, 90.

### `code/condensate_energy/seal_finite_matching.py` and `code/condensate_energy/finite_light_matching.py`

`seal_finite_matching.py` imports `ROOT, OUT` from `finite_light_matching.py` (line 15),
so the override belongs in the helper. In `finite_light_matching.py` replace line 20
(`OUT = ROOT / 'docs/condensate_energy/finite_matching'`) with the spaced-style
`SRC` / `out_dir()` / `OUT` block (its own `main` already does
`OUT.mkdir(parents=True, exist_ok=True)` at line 219 and writes `matching.json` at 314,
both of which should stay on `OUT`). Then in `seal_finite_matching.py` import `SRC` too
(line 15) and move the reads to it: lines 20 and 92. Writes stay on `OUT`: lines 28, 54,
56 (`attempts`; `parents=True` on its `mkdir`), 88, 96.

### `code/condensate_energy/seal_radiative_flat_modes.py` and `code/condensate_energy/radiative_flat_modes.py`

Same pattern: `seal_radiative_flat_modes.py` imports `ROOT, OUT` from
`radiative_flat_modes.py` (line 18). In the helper replace line 22
(`OUT = ROOT / 'docs/condensate_energy/radiative_flat_modes'`) with the block; its own
`main` (`mkdir` at 197, `results.json` at 405) stays on `OUT`. In the seal script import
`SRC` and move the reads: lines 22 and 103. Writes stay on `OUT`: lines 60, 62
(`attempts`; `parents=True`), 99, 109.

## What this does not change

- No computation. The figures, assessments and receipts are produced by the same code;
  only the directory the writes land in is parameterised.
- Default behaviour is byte-identical: with the variable unset and no flag, `OUT is SRC`
  and every path resolves exactly as before, so the sealed receipts and the manifest
  hashes of the *docs* are unaffected. The manifest hashes of the *scripts* change, which
  is why this is a proposal: the owner re-seals.

## How to check it after applying

```sh
# default location unchanged: both print the committed docs/ path
cd code/condensate_energy && python -c "import publish_endpoint_audit as m; print(m.OUT)"
python -c "import finite_light_matching as m; print(m.OUT)"
# override: both print under the scratch tree
ACS_OUT_DIR=/tmp/scratch python -c "import publish_endpoint_audit as m; print(m.OUT)"
# and afterwards
git status --short   # must list only the files you edited
```
