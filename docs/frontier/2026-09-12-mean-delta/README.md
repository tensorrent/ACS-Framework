# Mean-error continuation — 12 September 2026

This pass adds 23 Lean theorem declarations establishing the mean-error boundary-layer criterion, an explicit counterfamily separating mean from total error, and a failure of testing only one layer. It advances R11 without asserting a result for an actual-zero dataset or the unresolved operator and real-part bridges. Earlier checkpoints, including the [Klein-cover correction](../2026-09-12-topology-delta/README.md), remain unchanged.

## Exact criterion for changing finite configurations

For a nonempty finite indexed configuration, let `N` be its cardinality, let `0 < gamma_k < T`, and let `epsilon > 0`. Repeated ordinate values are allowed. Use the already verified scalar deficit

$$D_k=2\pi-2\left[\arctan\frac{T-\gamma_k}{\epsilon}+\arctan\frac{\gamma_k}{\epsilon}\right]
=2\left[\arctan\frac{\epsilon}{\gamma_k}+\arctan\frac{\epsilon}{T-\gamma_k}\right].$$

Define the mean `M=(sum D_k)/N` and the fraction within an endpoint layer of thickness `L epsilon`, for `L>0`, by

$$p_L=\frac{\#\{k:\min(\gamma_k,T-\gamma_k)\le L\epsilon\}}{N}.$$

[PerZeroMean.lean](../../../code/frontier_verification/proofs/PerZeroMean.lean) proves the finite bounds

$$2\arctan(1/L)\,p_L\le M\le 2\pi p_L+4\arctan(1/L)\le 2\pi p_L+4/L.$$

It also proves, along any filter and with arbitrarily changing finite sets, endpoints, and positive resolutions,

$$M\longrightarrow0\quad\Longleftrightarrow\quad
 p_L\longrightarrow0\ \text{for every fixed }L>0.$$

No growth rate for `N` or separate assumption that `epsilon` tends to zero is needed for this equivalence. Its stated hypotheses require nonempty configurations and interior points at each index. The necessity follows by dividing by the positive lower coefficient. For sufficiency, first choose a large fixed `L` to make `4/L` small, then use convergence of that layer fraction. The argument uses finite inequalities rather than interchanging an unbounded sum and a limit.

The preceding [absolute-error criterion](../2026-09-12-integral-delta/README.md) remains distinct: total deficit tends to zero exactly when

$$\epsilon\sum_k\left(\frac1{\gamma_k}+\frac1{T-\gamma_k}\right)\longrightarrow0.$$

## A fully specified mean-versus-total counterfamily

For integer `N>=2`, take `T=1`, `epsilon=1/N²`, one point at `gamma_0=epsilon`, and the remaining `N-1` indexed points at `1/2`. [PerZeroCounterfamily.lean](../../../code/frontier_verification/proofs/PerZeroCounterfamily.lean) verifies positivity, interiority, the actual finite sum, its identification with the mean definition above, and the limits

$$E_N=\sum_k D_k
=\frac\pi2+2\arctan\frac1{N^2-1}
 +4(N-1)\arctan\frac2{N^2}
\longrightarrow\frac\pi2,\qquad \frac{E_N}{N}\longrightarrow0.$$

Thus vanishing mean deficit does not imply vanishing total deficit, even when the resolution tends to zero. The proof bounds the last term between zero and `8/N`; the nonzero total limit is kernel checked. The repeated midpoint ordinates are allowed by the finite indexed model. This example is not asserted to be a zero configuration of a particular analytic function.

## Why every fixed layer matters

Testing one cutoff is insufficient. For `0<epsilon<1/3`, take a singleton at `gamma=2 epsilon`, `T=1`. The `L=1` layer fraction is exactly zero, while

$$D>2\arctan(1/2)>0.$$

These statements are kernel checked in `single_cutoff_failure`; they apply at every index of any such family with shrinking positive resolution. This guards against replacing the universal quantifier in the criterion with one selected cutoff. Analytically, any finite list of cutoffs has the same limitation: choose `c` larger than every cutoff and set `gamma=c epsilon`, with `epsilon<1/(c+max L)`. Every tested fraction is zero, while `D>2 arctan(1/c)>0`. This finite-list extension follows from the deficit identity; the explicit `c=2, L=1` witness is the one formalized here.

## Evidence and scope

- [Formal audit](Formal_Audit.json) recompiles six modules, including four unchanged dependencies and the two new modules. All public theorem axiom dependencies are printed with no `sorryAx`. Eight altered statements or definitions are rejected; exact altered files and diagnostics are in [Formal_Audit_Artifacts.zip](Formal_Audit_Artifacts.zip).
- [Cross-method checks](Cross_Method_Checks.json) use symbolic limits and a series expansion, exact rational counting in 48 configurations and 240 layer bounds, eight finite counterfamily sizes, six complex quadrature cases, and four single-cutoff counterexamples. The quadrature routine is explicitly shared with the prior integral checkpoint. Numerical quadrature is not interval certification.
- [Development_Attempts.json](Development_Attempts.json) and [the retained attempts](Development_Attempts.zip) include failed Lean attempts, their exact source text, and compiler output. Mutant rejection measures sensitivity of these proof scripts; it is not a completeness claim about the audit.
- [Manifest](Manifest.json), [integrity receipt](Verification.json), [queue](Research_Queue.json), and [event ledger](Branch_Events.jsonl) retain the earlier 326-event prefix and all 113 research branches. Three appended events record this pass; unexamined branches are explicitly carried forward.

The Lean/Mathlib trust base is shared across the formal checks. Symbolic algebra and numerical quadrature provide materially different checks, but numerical samples alone do not prove the asymptotic theorem. Reproduction instructions and pinned source identities are in [MEAN_README.md](../../../code/frontier_verification/MEAN_README.md).

The next input-bearing step is to map the accessible ACS implementation and declared datasets to claims and revisions, then evaluate actual endpoint separations. The natural-operator, independent real-part, geometric-cover, and physical-identification obligations remain open; this scalar error result does not discharge them.
