# Projection, constraint closure, and the current Navier–Stokes formalization

This workstream addresses K04 and NS04 and supplies a bounded, independent audit for NS02/NS05. It separates an exact obstruction for a specified finite projection from an audit of selected external proof files. Neither is a kernel verification of a Navier–Stokes theorem.

## 1. An exact projection obstruction for every cutoff

Let \(\{f,g\}=f_xg_y-f_yg_x\) be the Poisson bracket on the two-dimensional torus. Let \(P_N\) retain precisely the Fourier modes with \(|k_x|,|k_y|\le N\), and define the truncated bracket by \([f,g]_N=P_N\{f,g\}\). Choose real, retained functions

\[
f=\cos Nx,\qquad g=\sin Nx,\qquad h=\cos(Nx+y),\qquad N\ge1.
\]

Ordinary differentiation gives

\[
\{g,h\}=-\frac N2[\sin(2Nx+y)+\sin y],\qquad
\{h,f\}=-\frac N2[\cos y-\cos(2Nx+y)],\qquad \{f,g\}=0.
\]

The modes with first coordinate \(2N\) are deleted, so the truncated Jacobi sum is

\[
[f,[g,h]_N]_N+[g,[h,f]_N]_N+[h,[f,g]_N]_N
=\frac{N^2}{2}\sin(Nx+y)\ne0.
\]

The outer modes on the right are retained. The unprojected Jacobi sum is zero. This proves failure for every positive integer cutoff, not just a sampled matrix size. Taking Hamiltonian vector fields transfers the example to divergence-free fields; adding a zero third component embeds it into the three-dimensional torus.

Two independent calculations verify it: sparse Fourier convolution using exact integer mode determinants, and physical-space symbolic differentiation followed by the displayed product-to-sum identities. The symbolic parameter N proves the full family; the checks at N=1,2,3,5,8 are supplemental. Full bracket structure constants and twelve exact multivariate examples additionally check the general identity

\[
J_P(f,g,h)=-P\sum_{\rm cyc}[f,(I-P)[g,h]],\qquad f,g,h\in\operatorname{ran}P.
\]

This identity follows by inserting \(P=I-(I-P)\) into the inner brackets and applying ambient Jacobi. It identifies the discarded interactions whose return to retained modes produces the defect.

**ACS implication.** A projected constraint system inherits the ambient Lie algebra only if this defect vanishes, for example by actual subalgebra closure, or if a different bracket is explicitly constructed and verified. The result does not say that the user's particular restricted ACS algebra fails: that requires its actual carrier and projection. It does not invalidate ordinary energy-stable Galerkin methods. Such methods can preserve energy cancellation without preserving this Lie bracket, and convergence requires additional estimates. It also supplies no counterexample to Navier–Stokes regularity.

K04 therefore advances to an exact obstruction plus an explicit closure test. The intended ACS projection and a continuum-limit estimate remain separate obligations.

## 2. Current external claim: scope before status

The [8 September 2026 announcement](https://openai.com/index/navier-stokes-solution/) links an analytical manuscript and formalization claiming a smooth-forced, positive-viscosity breakdown result. The [manuscript's Theorem 1.1](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf) specifies zero initial data, smooth compactly supported space-time forcing, a solution smooth before time 1 with uniformly bounded kinetic energy, and unbounded velocity approaching time 1. This is a source-reported theorem, not a theorem independently established in this audit.

The [official Clay statement](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf) permits forcing in alternatives C/D; A/B instead ask about zero forcing. A forced construction does not by itself negate an unforced assertion. The force class, smooth initial data, spatial domain, pressure conditions, and energy requirement must remain attached to the claim.

## 3. What the static formalization audit actually verifies

Repository: [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler/tree/f9e8bc5b38b6e212696e8a30e3e91517af887bbd), pinned to commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` (10 September 2026). The recursive tree lists 2,659 Lean files. This release preserves twelve selected statement/configuration/adapter files, their original Git blob hashes, and the Apache-2.0 license. The complete proof dependency graph was not fetched or checked.

The read-only audit independently checks:

1. The bytes of all twelve selected files match the pinned Git blob hashes.
2. The challenge and submission definitions have identical tokens after removing nested comments and whitespace. Both public theorem declaration headers also match.
3. A separate contract inspection confirms the convective term, viscosity, pressure gradient, forcing, initial data, divergence constraint, smooth time half-line, rapid force decay, uniform energy requirement, and periodic pressure condition.
4. The Comparator configuration names both C/D submission theorems, enables the additional kernel checker, and permits only `propext`, `Quot.sound`, and `Classical.choice`.
5. Two `sorry` placeholders occur in the **reference challenge**. They are not solution proofs. No such placeholder occurs in the selected solution/adapter files, and those selected files do not directly import the challenge. This does not establish the status of every transitive dependency.

The repository's [formalization metadata](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/formalization.yaml) labels review **self-assessed**. Its reported zero-sorry/axiom results are assertions in metadata; a configured check and a `#print axioms` command are not fresh execution receipts. The selected [Comparator definitions](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/ComparatorDefinitions.lean) do include nonlinear convection, unlike the separate Croft Adams candidate examined by the Navier–Stokes workstream.

The pinned toolchain is Lean 4.34.0-rc2. A supported-runtime startup failure for that version is already preserved in the inherited evidence; no new kernel, Lake, Comparator, or nanoda run was completed here. Text identity is useful audit evidence but is weaker than definitional equality checked in the kernel. Reading selected adapters is weaker than verifying the full imported proof. The exact open path is a supported, pinned full build followed by Comparator and axiom receipts, plus mathematical statement alignment and review of the analytical proof.

## 4. Verification and remaining branches

Run `python run_check.py truncated_jacobi formalization_static_audit` after installing SymPy 1.14.0. The static audit itself uses only the standard library. Both programs passed and have append-only source snapshots, stdout, stderr, hashes, and receipts.

The two projection derivations share the definition of the sharp Fourier cutoff and the Poisson bracket. The two static audit routes share the same pinned source files; they are not independent formalizations. The inherited runner records an unused historical `source_root` fallback that does not exist in this workstream; neither current check reads it. All actual inputs are local relative to the workstream and identified by hash.

| Item | Completed scoped work | Remaining obligation |
|---|---|---|
| K04 | Explicit projection Jacobi defect and all-cutoff counterexample | Supply the intended ACS operator/carrier and prove closure or bound the defect |
| NS04 | Finite divergence-free truncation obstruction verified by two exact methods | Uniform continuum estimates and a legitimate NS functional bridge |
| NS02/NS05 | Pinned statement, hypothesis, configuration, and selected-adapter audit | Full supported formal replay and independent analytical review |
| Croft identification | Separate candidate analysis is available in the Navier–Stokes report | The exact author/title/link intended by the user remains unconfirmed |
