# ACS Framework — Complete Bundle

**Author:** Bradley Wallace · TensorRent
**Assembled:** 2026-06-27
**Canonical seed (all stochastic code):** `20260423`

This bundle contains the latest ACS (Asymmetric Codependent Systems) papers and the
validation/code that supports the claims in them. Everything here has been run and
checked at assembly time (see `MANIFEST.md` for the per-claim tier table).

---

## What's inside

```
papers/
  core_trilogy/        Papers A, B, C   (B in two current forms — see note below)
  notes/               N1, N2, N3
  methodology/         FF06e — the Form/Function shuffle-knife (the discriminant itself)
  later_FF06_series/   June 2026 methodology/geometry thread (f, g, h, i, J, K, Σ, K1)
code/
  acs_codebase/        curated pytest backbone for Papers A/B/C  (42 tests, 15 modules)
  notes_verification/  N1 lattice null-test, N2 signature-selection test, N3 support
  hp_knife_suite/      the four-knife Riemann/L-function exam built this session
    data_zeros/        Riemann + Dirichlet L zeros, WITH their generation scripts
docs/                  master index, corpus map, framework skill, elimination ledger, changelogs
MANIFEST.md            full inventory + four-tier verification table + claim→evidence map
```

## Reproduce

Codebase (Papers A/B/C):
```
cd code/acs_codebase
pip install -r requirements.txt        # numpy scipy sympy pytest
python -m pytest -q                     # expect: 42 passed
```

HP / L-function exam (Paper B / N3 support):
```
cd code/hp_knife_suite
python hp_never_synced.py      # real zeros 240 vs GUE ~1 vs lattice ~0.7   (C5: arithmetic present)
python hp_xp_test.py           # Berry-Keating xp: density only, no orbits  (negative)
python hp_signed_lfunction.py  # C6 sign + C7 weights on zeta; C8 char-sign 18/18 on quadratics
python hp_phase_test.py        # C8' complex-character phase, demod R = 0.99
python hp_c9_orthogonality.py  # C9 finite-prime orthogonality, zeros-vs-truth corr 0.92
```
All scripts are self-contained (data paths resolve to `data_zeros/` automatically).

---

## Honest scope (read this)

- **Paper B is included in two current forms.** `..._extended` (deepest, longest) and
  `Spectral_Witness_Survival_...` (retitled, tightened). Both are post-May-21; pick the
  canonical one yourself — neither was silently dropped.

- **The HP/L-function suite verifies *known* mathematics.** C5–C9 are the Weil–Guinand
  explicit formula and its Dirichlet generalization: peaks at log pᵐ, weights p^(−m/2),
  negative sign, χ(p) twist, pairwise character orthogonality. These are theorems. The
  suite is a **falsification / calibration instrument** — it confirms that real spectra
  exhibit the explicit formula and that imposters (GUE, Berry-Keating xp) do not. It does
  **not** prove new theorems and does **not** construct a Hilbert–Pólya operator.

- **Non-circularity is checked.** The Dirichlet L-function zeros were computed from
  L(s,χ) via Hurwitz zeta (`data_zeros/cyclotomic_*/*.py`) — no prime ever enters the
  construction. So the witness recovering χ(p) from those zeros is a real readout, not a
  plant. The generation scripts are included so this is auditable.

- **"Selberg orthogonality" (C9) here is a finite-prime proxy** (a ~12-prime resultant),
  consistent with Selberg's asymptotic statement, not the asymptotic statement itself.

- **Tiers do not promote.** T3 (numerical) is labeled T3, never T2. The closure-attractor
  result is T3. The falsified claims live in `docs/...KILL01_Elimination_Ledger.md` as
  first-class results, not hidden.

- **Not included:** the hundreds of loose exploratory scripts across the working
  directory, the AISO engineering stack, and the `.npz`/`.png` caches. The
  `later_FF06_series` papers are included as documents; their individual computational
  artifacts remain in the broader workspace and can be bundled on request.
