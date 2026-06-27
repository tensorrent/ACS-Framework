# Numerical Pitfalls

Documented numerical issues encountered during the framework's verification.
Future contributors should read this before extending the codebase or
modifying scale-dependent computations.

---

## 1. Catastrophic cancellation in scale-separated Cramer's rule

**Where:** `src/paper_a/branch_a_vacuum.py`

**Symptom:** Naive float64 evaluation of the vacuum analysis returns
spurious failures (v² = 0 reported for valid α_1 values).

**Cause:** Cramer's rule inversion of the 2×2 quadratic-form matrix
gives expressions like

```
v² = (2 ρ_tot · μ²_φ − α_1 · μ²_Δ) / (4 λ_φ ρ_tot − α_1²)
```

When the calibrations v ≈ 246 GeV and v_R ≈ 10¹⁵ GeV differ by
13 orders of magnitude, the two terms in the numerator both have
magnitude ~10²⁹ GeV² but differ by only ~10⁴ GeV² (the value of v²).

The 25-order ratio between the dominant terms and the difference
they should produce exceeds float64 precision (~16 decimal digits).
The result is a difference computed as zero, returning v² = 0.

**Resolution:** Use Python's `decimal` module at 50-digit precision
for any computation that touches the v / v_R ratio directly.

```python
from decimal import Decimal, getcontext
getcontext().prec = 50
v_phys = Decimal("246.0")
vR_phys = Decimal("1e15")
# ... arithmetic in Decimal
```

The `branch_a_vacuum.py` module does this throughout. The result at
50-digit precision recovers v² = 60516.0 GeV² and v_R² = 10³⁰ GeV²
exactly across all stable α_1 values.

**Generalization:** any future computation comparing electroweak and
PS scales directly (such as flavor matrix elements with v_R-suppressed
corrections, or one-loop threshold matching) should either:
- use `decimal` arithmetic, or
- work in dimensionless ratios where the suppression appears as a
  small parameter ε = v / v_R rather than as a large quotient.

---

## 2. NumPy boolean type vs Python `bool`

**Where:** every module that returns boolean results from `np.allclose()`,
`np.isclose()`, or `<`/`>` comparisons of numpy arrays.

**Symptom:** `assert result is True` fails in pytest even when the
result evaluates as truthy.

**Cause:** `np.allclose(a, b)` returns `numpy.bool_` (specifically
`np.True_`), which is NOT identical to Python's `True` under `is`.
Identity comparison (`is True`) requires the exact Python singleton.

```python
>>> import numpy as np
>>> r = np.allclose([1.0], [1.0])
>>> type(r)
<class 'numpy.bool_'>
>>> r is True
False
>>> r == True
True
>>> bool(r) is True
True
```

**Resolution:** Wrap all numpy boolean returns in `bool(...)` at the
return site:

```python
return {"verified": bool(np.allclose(a, b))}
```

The codebase does this consistently. Tests use `is True` for safety:
this fails loudly if numpy bools leak through, rather than silently
passing on truthy non-bools.

---

## 3. Bracket-map Jacobian rank at degenerate vs generic points

**Where:** `src/paper_c/orthogonal_complement_probe.py`

**Issue:** the rank of `d(bracket)|_{(X,Y)}` depends on whether
(X, Y) is a generic point in sl(4,ℝ) ⊕ sl(4,ℝ) or a degenerate one.

**Generic point:** rank = n² − 1 = 15, kernel = 15. The bracket map
is locally surjective.

**Degenerate point** (e.g., (H₁, A₀₁) where the bracket lands in a
1-dim subspace): rank = 11, kernel = 19.

**Implication for the paper:** any "ambiguity factor" claim should
specify which point was used. The clean three-number report is:

| Quantity | Value | Meaning |
|---|---|---|
| dim B^⊥ | 14 | passive subspace where (X, Y) must lie |
| Generic Jacobian kernel | 15 | active fiber dimension at generic point |
| Degenerate kernel at (H₁, A₀₁) | 19 | larger fiber at this specific critical point |

Citing only one of these (especially the degenerate one) without
context produces a misleading "ambiguity factor."

---

## 4. SymPy MatrixSymbol arithmetic does not auto-distribute

**Where:** previously in `src/paper_a/yukawa_no_go.py::algebraic_identity_proof`

**Symptom:** `simplify(M_u - M_d - (h - h_tilde)*(k1 - k2)) == 0`
returned `False` even though the identity is mathematically true.

**Cause:** SymPy's `MatrixSymbol` instances do not automatically
distribute scalar coefficients across addition under `simplify`.
The expressions are mathematically equal but symbolically distinct.

**Resolution:** for the algebraic identity test, use commutative
scalar symbols (`symbols(..., commutative=True)`) and explicit
`expand()` on both sides. The matrix-level proof is verified
by the numerical test (`yukawa_no_go_test`) at machine precision.

**Generalization:** for any symbolic verification involving matrix
products and scalar coefficients, prefer:
- expand both sides of the proposed identity, or
- substitute concrete random matrices and verify numerically.

`MatrixSymbol` is best for type checking and shape tracking, not for
algebraic identity manipulation involving distributivity.

---

## 5. Floating-point evaluation of Cayley-Hamilton-like operators

**Where:** `src/paper_c/spectral_taxonomy.py::verify_sl4_hyperbolic`

**Issue:** `expm(2π · ad_{T_BL})` produces matrix elements of order
e^(8π/3) ≈ 4348. This is correct (the operator has real eigenvalues
±4/3, so exponentiation grows by exp(eigenvalue · t)).

**Common confusion:** treating the result as "a numerical bug" because
"holonomy should return to identity." It does not: the spectrum is
real, the flow is hyperbolic, and the 2π loop does NOT close.

**Documentation:** the spectrum classification function explicitly
labels this case:

```python
classify_ad_T_BL()
# {'class': 'hyperbolic', 'real_count': 6, 'imaginary_count': 0, ...}
```

If the test fails (i.e., max element at 2π is small), THAT would
indicate a numerical bug. The current passing test confirms the
hyperbolic flow is computed correctly.

---

## 6. Random seed discipline

**Where:** all modules that sample randomly.

**Convention:** the canonical seed is `20260423`, set in
`src/common/seed.py`. Every module that uses random sampling
either:
- imports `default_rng()` from `src.common.seed`, or
- accepts an explicit `seed` parameter that defaults to canonical.

Tests should be reproducible bit-for-bit on any platform with
identical numpy version. If a test fails due to RNG differences
across numpy versions, that's a known limitation of NumPy's
random API; the workaround is to pin numpy version in
`requirements.txt` if strict reproducibility is required.

---

## 7. Implicit assumption: numpy float64 default

**Status:** all modules implicitly use `np.float64` as the default
real type. This is fine for the verifications in the codebase, but:
- Be aware when porting to GPU or low-precision hardware
- Be aware when working with very small / very large quantities
  (use `decimal` per pitfall #1)

For the spectral computations in Paper B (Riemann zeros), float64 is
sufficient because the zero values are quoted to 6 decimal places and
the verifications operate at residual ~10⁻¹⁰. Higher precision (mpmath)
would only matter for explicit-formula computations to thousands of
zeros, which we do not perform here.
