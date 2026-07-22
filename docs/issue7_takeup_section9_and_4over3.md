> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Issue 7 takeover: Section 9 toy kill test and 4/3 mechanism test

Companion paper: `papers/methodology/Section9_Cone_Chain_and_Four_Thirds_Kill_Tests.tex` (TR-2026-FF06-I7).

## Scope delivered

Three executable checks were added under `code/issue7/`:

- `section9_toy_kill_test.py`
- `mechanism_4over3_test.py`
- `exhaustive_issue7.py`

Both scripts are designed as kill-style diagnostics, not theorem proofs.

## 1) Section 9 toy kill test

### Objective

Test the dependency direction

`spectral gap -> clustering -> cone sharpness proxy`

in a finite model where all quantities are computable.

### Toy model

- 1D transverse-field Ising chain, open boundary, `N=7`.
- Hamiltonian:
  `H = -J sum Z_i Z_{i+1} - h sum X_i`
- Parameter sweep: `h in {0.5, 0.8, 1.2, 1.5, 2.0}` with `J=1`.

### Measured observables

- Gap: `Delta = E1 - E0` from exact diagonalization.
- Clustering length `xi`: exponential fit of connected `Z0-Zr` ground-state correlator.
- Cone proxy:
  - Compute Heisenberg-evolved `Z0(t)`.
  - Compute leakage curve `||[Z0(t), Zr]||` for distances `r=1..N-1`.
  - Estimate effective cone speed `v_est` from threshold crossing.
  - Measure max leakage outside estimated cone.

### Kill criterion

If larger gap does not co-vary with both:

- smaller `xi`, and
- smaller outside-cone leakage,

then the dependency chain is not supported in this toy model.

### Run result (current execution)

- `corr(gap, xi) = -0.6375` (expected sign)
- `corr(gap, outside_leakage) = +0.9636` (opposite sign)

Status: **chain not supported in this toy run**.

## 2) 4/3 mechanism test

### Objective

Test whether the equality between:

- ACS constant `beta = 4/3`, and
- density exponent form `alpha(d)=1+1/d` at `d=3`,

survives mechanism-level checks.

### Checks

1. **Normalization robustness (K1):**
   if `beta` is rescaled by generator normalization `c`, then
   `d_hat = 1/(c*beta - 1)` should remain stable for a mechanism claim.

2. **Independent-structure check (K2):**
   scan integer pairs `(d,n)` where
   `alpha(d) = 1 + 1/d` and `beta(n) = n/(n-1)`.
   If all equalities are exactly `n=d+1`, this is a bookkeeping identity.

### Run result (current execution)

- K1: inferred `d_hat` varies from undefined to `1.0..3.0`; spread `2.0`.
- K2: all exact matches satisfy `n=d+1`.

Status: **mechanism not established in this test**.

## Exhaustion extension

`exhaustive_issue7.py` extends both checks:

- Section 9 sweep over `n_sites in {6,7,8}`, `h in [0.4,2.4]` (11 points),
  and leakage thresholds `{1e-2, 3e-3, 1e-3, 3e-4}`.
- 4/3 sweep over normalization scale `c in [0.5,1.5]` (101 points),
  integer lattice scan `d,n in [2,100]`, and epsilon perturbation checks.

Current exhaustive result summary:

- Section 9 support rate: `0/12` (no case supported the full chain criterion).
- 4/3 normalization spread in inferred dimension: `74.0`.
- 4/3 exact-hit identity: all exact hits satisfy `n=d+1`.

## Cross-model kill pass

`cross_model_kill_pass.py` adds:

- two model families (`TFIM`, `XXZ+h`) under matched sweep structure,
- two outside-cone leakage summaries (`max`, `mean`) in addition to gap and `xi`.

Current cross-model summary:

- `TFIM` support rate: `0/6`.
- `XXZ` support rate: `1/6`.
- Combined support: `1/12`.

Interpretation (diagnostic scope only):

- The chain criterion is not robust across model family.
- One narrow support cell appears in `XXZ` (`n_sites=7`, threshold `1e-3`);
  this behaves like a contingent pocket, not a stable universal trend.

## Exact (no IEEE float) Section 9 pass

`section9_exact_kill_test.py` is a float-free analogue:

- classical 1D Ising with integer energies and integer Boltzmann base `B`
- connected correlators and influence fractions computed in `Fraction`
- decision rule uses only signs of `Fraction` covariances (no float)

Current exact summary:

- `sign cov(gap, cluster_weight) = -1` (expected direction)
- `sign cov(gap, outside_affect) = 0` (outside-cone affect identically `0` under local majority — sharp classical cone)
- joint chain support: **false**

Platform note: because the decision path is exact rational, this diagnostic
does not require a second machine for numeric reproducibility.

`long_range_kill_pass.py` adds a long-range Ising family
`H = -sum_{i<j} J/|i-j|^alpha Z_i Z_j - h sum X_i` with `alpha in {3, 2}`,
using the same sweep structure and dual leakage proxies.

Current long-range summary:

- `alpha=3` support rate: `2/6`.
- `alpha=2` support rate: `3/6`.
- Combined support: `5/12`.

Interpretation (diagnostic scope only):

- Support cells concentrate at the smallest leakage threshold (`1e-3`)
  and are threshold-dependent, not uniform across the grid.
- The long-range family shows more partial support than nearest-neighbor
  families, but the chain criterion still fails in the majority of cells.

## Scope boundary

These results are finite-model diagnostics and kill-test outputs only.
They do not establish a general no-go theorem, nor a universal impossibility
claim beyond the tested model families and parameter windows.

Platform status: float NumPy Section 9 scripts remain single-platform
anchored. The exact Section 9 kill test
(`section9_exact_kill_test.py`) uses integer/`Fraction` on the decision
path, so cross-machine float drift is not a concern for that diagnostic.
Companion exact ACS TE automaton: `TR-2026-FF06-ACS/.../integer_acs.py`.
See the paper footnote in `issue7_paper_section9_and_4over3.md`.

## Repro commands

```bash
python3 code/issue7/section9_toy_kill_test.py
python3 code/issue7/mechanism_4over3_test.py
python3 code/issue7/exhaustive_issue7.py
python3 code/issue7/cross_model_kill_pass.py
python3 code/issue7/long_range_kill_pass.py
python3 code/issue7/section9_exact_kill_test.py
python3 code/issue7/verify_issue7_pipeline.py
```

## Environment and artifact anchors

Observed environment for canonical logs:

- Python: `3.14.6`
- NumPy: `2.5.0`
- Platform: `macOS-15.3.2-arm64-arm-64bit-Mach-O`

Canonical artifact checksums (SHA-256):

- `docs/issue7_exhaustive_results.json`  
  `2ad53a2c84ea9b51fd36c9c4a956451d9910e51fbfb694738873f7902f3c03cb`
- `docs/issue7_logs/section9_stdout.txt`  
  `5e3d49a49ef53fde92fd29855912852c5a90a5a857c2d0010770a1642434f4f9`
- `docs/issue7_logs/mechanism_4over3_stdout.txt`  
  `be1ff08ab3fbb8b8aebaff1ed5e504ff63ac20de661a31fb0d450e36c6ca3146`
- `docs/issue7_logs/exhaustive_stdout.txt`  
  `ec79dc64dedc9aa392dfc0fc5c0d5f4714717028b4e9f65ac470073072e119ac`
- `docs/issue7_cross_model_results.json`  
  `763f5a47d93ed7ec382ffb1445c4427c747311de4c813c16d6258cd60763caba`
- `docs/issue7_logs/cross_model_stdout.txt`  
  `b69406e5f4f980ec9127a355208bb03e28077a9ff77dee36209b3d80c8f515d0`
- `docs/issue7_long_range_results.json`  
  `e0fcab86e6963ee3f5298bc6a9124438bfeeaef5ea457a469703e889e74fbb48`
- `docs/issue7_logs/long_range_stdout.txt`  
  `51924950d9b4c577948f11df2cdeb7390a7124f11c3d9b04480230476298a6c3`
- `docs/issue7_section9_exact_results.json`  
  `3242ffb90440868dbff15db66b35d10e44233325aa7dd35ea2e4ab9031bbc650`
- `docs/issue7_logs/section9_exact_stdout.txt`  
  `08469f911d19dd9bb7934067b1e5503b7e872eb7bd2aeecab1aedcb9673661fc`

Verifier note:

- `verify_issue7_pipeline.py` now checks hash-anchor presence in both
  `issue7_takeup_section9_and_4over3.md` and
  `issue7_paper_section9_and_4over3.md`.
