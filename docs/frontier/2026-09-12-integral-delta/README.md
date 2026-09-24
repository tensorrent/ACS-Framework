# Integral and absolute-error formalization — 12 September 2026

This pass advances C05 and R11 from the [preceding checkpoint](../2026-09-12-delta/README.md). Three new Lean files contain 19 theorem declarations. The actual complex paired integral, the finite-resolution inequalities, and the absolute-error convergence criterion now have successful kernel checks. The 112 research branches remain active records with explicit continuation conditions.

## The integral is now identified

For real `gamma`, `T`, and nonzero `eps`, [PerZeroIntegral.lean](../../../code/frontier_verification/proofs/PerZeroIntegral.lean) proves

$$\int_0^T\left(\frac{1}{\varepsilon+i(t-\gamma)}-\frac{1}{-\varepsilon+i(t-\gamma)}\right)\,dt
=2\left[\arctan\frac{T-\gamma}{\varepsilon}+\arctan\frac{\gamma}{\varepsilon}\right].$$

The right side is embedded in the complex numbers. The proof first checks the pointwise complex identity, then evaluates the real interval integral and translates its endpoints. The theorem allows both signs of nonzero resolution and oriented intervals; the physical interior limit uses positive resolution. This supplies the explicit integral bridge that the unchanged archived `PerZero.lean` identified as unformalized.

## Quantitative error and summation

For positive resolution and an interior point, put `D = 2*pi - contribution`, `x = eps/gamma`, and `y = eps/(T-gamma)`. [PerZeroError.lean](../../../code/frontier_verification/proofs/PerZeroError.lean) proves

$$D=2(\arctan x+\arctan y)>0,$$
$$2\left(\frac{x}{1+x^2}+\frac{y}{1+y^2}\right)\leq D\leq2(x+y),$$
$$0\leq2(x+y)-D\leq\frac23(x^3+y^3).$$

The elementary arctangent inequalities are proved using ordered interval integrals. The statements use dimensionless endpoint ratios; algebraic substitution gives the equivalent bounds displayed in the previous derivation.

[PerZeroSums.lean](../../../code/frontier_verification/proofs/PerZeroSums.lean) then proves the exact criterion for arbitrary changing finite configurations:

$$\sum_k D_{j,k}\to0\quad\Longleftrightarrow\quad
\varepsilon_j\sum_k\left(\frac1{\gamma_{j,k}}+\frac1{T_j-\gamma_{j,k}}\right)\to0.$$

Its formal statement uses an arbitrary filter, changing finite index sets, and explicitly positive resolutions and interior ordinates. Cardinality is unrestricted. The necessity proof shows that sufficiently small total error forces every endpoint ratio below one; the resulting uniform estimate controls the entire finite sum. No unsupported interchange of a growing sum and a limit is used.

## Cross-checks and retained evidence

- [Kernel receipt](Formal_Audit.json): the archived dependency and all three new modules pass, all public theorem axiom dependencies are printed, and seven false mutations are rejected. The mutations change the integral coefficient, resolvent sign, arctangent bound, cubic coefficient, deficit factor, small-error threshold, and endpoint weight.
- [Exact audit inputs and events](Formal_Audit_Artifacts.zip) retain the mutated sources and command outputs. All nine checked-out package revisions match the existing lock. The printed theorem dependencies contain no `sorryAx`.
- [Independent computation](Cross_Method_Checks.json) directly integrates both complex resolvents separately and their difference in 24 cases. It covers interior, endpoint, and exterior ordinates, both resolution signs, and reversed integration orientation. At 70-digit working precision, the checked discrepancies are below `1e-50`. These are numerical checks, not interval enclosures.
- The same computation checks nine changing finite configurations, including vanishing total error, a resolution-scale endpoint defect, and a subresolution endpoint defect. It also checks the previously derived boundary-layer inequalities at four cutoffs.
- [Development attempts](Development_Attempts.zip) and their [index](Development_Attempts.json) preserve failed and successful compiler inputs and diagnostics. Fixes concern algebraic normalization, an explicit measure, integrability arguments, and namespace disambiguation; failed attempts are retained separately from the final successful audit.
- [Integrity receipt](Verification.json), [manifest](Manifest.json), [extended ledger](Branch_Events.jsonl), and [research queue](Research_Queue.json) preserve the preceding checkpoint and its 319-event byte prefix.

Reproduction instructions are in [INTEGRAL_README.md](../../../code/frontier_verification/INTEGRAL_README.md).

## Remaining questions

The boundary-layer criterion for **average** error and its explicit asymptotic counterfamily remain analytical derivations with computational checks; they are not yet Lean convergence theorems. The current absolute-error criterion does not claim that mean error controls total error.

Applying these results to a particular zero dataset requires declared endpoint separations and counting assumptions. The real-part identification and natural-operator obligations remain separate. The topological lifting bridge in `AxiomIII.lean` and the production-source mapping also remain in the queue. Formal verification here retains the ordinary Lean trust base and the pinned Mathlib cache; numerical quadrature provides a separate route for its explicitly sampled scope.
