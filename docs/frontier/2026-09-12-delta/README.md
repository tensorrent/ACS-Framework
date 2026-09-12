# ACS research delta — 12 September 2026

This pass advances the [Frontier snapshot](../2026-09-11/README.md) through fresh execution, formal verification, and two new scoped derivations. It carries forward all 110 existing branches and adds C06 and R11. Ongoing research and new questions remain the objective.

## What moved forward

- **Fresh reproducibility:** all 18 registered replay commands passed across all seven workstreams in a fresh extraction, using Python 3.12 and the exact five dependency versions. The replay completed in about 185 seconds. This checks the registered programs; it does not independently re-prove every catalog claim.
- **C05 — the runtime gate is passed for the three archived files:** `LFBound.lean`, `AxiomIII.lean`, and `PerZero.lean` now have fresh successful kernel checks. Their combined 24 theorem declarations are in unchanged sources. All nine Mathlib package revisions match the retained lock. Topological lifting assumptions and the identification of a closed form with an actual integral remain separate obligations.
- **C06 — a broader probability carrier:** the new `LFReal.lean` proves the bound on arbitrary real probabilities and attainment in the declared deterministic-friend branch. Four independently constructed LP problems and exact primal/dual certificates agree on the value four.
- **R11 — control of finite resolution and moving endpoints:** a new Lean proof gives the limit along `gamma = c * epsilon`. At `c = 1`, the value tends to `3*pi/2`, not `2*pi`. Analytical error bounds and a counterfamily distinguish vanishing average error from vanishing total error.

Read the [derivations](DERIVATIONS.md) for the exact statements, proofs, and remaining boundaries. [Research_Queue.json](Research_Queue.json) records all 112 branches without relabeling untouched branches as newly audited.

## Verification and evidence

- [Replay receipt](Replay_Receipt.json), [new replay artifacts](Fresh_Replay_Delta.zip), and their [manifest](Fresh_Replay_Delta_Manifest.json). The ZIP contains 332 changed or newly produced files; unchanged source remains in the original Frontier archive.
- [Full Lean audit](Lean_Audit_v434.json): the three original files and two new files pass; eleven distinct mathematical mutations are rejected, and public theorem axiom dependencies are printed.
- [Lean audit artifacts](Lean_Audit_Artifacts.zip) retain the exact mutated sources, printed-axiom inputs, and command events from both final runs.
- [Lean 4.15 audit](Lean_Audit_v415.json): both original standalone proofs pass, with four rejected mutations. This is a version comparison, not an independent kernel implementation.
- [Real-probability certificates](lf_real_audit.json) and [per-zero numerical/symbolic checks](per_zero_boundary_audit.json).
- [Reproduction code and instructions](../../../code/frontier_verification/README.md).
- [Extended branch-event ledger](Branch_Events.jsonl): the original 315-event byte prefix is retained, with four new events appended.
- [Package verification](Delta_Verification.json) checks source and archive hashes, branch coverage, the complete event chain, retained receipts, and local documentation links against the [file manifest](Delta_Manifest.json).

The version comparison matters: several `LFBound` witness facts have no axioms in Lean 4.15, while Lean 4.34 reports `propext` for the same source. The documentation's old axiom list is reproduced under its documented runtime; it should not be silently generalized across versions. The new real-analysis proofs report `propext`, `Classical.choice`, and `Quot.sound`; no printed theorem dependency contains `sorryAx`.

The Lean artifact checks use the pinned official runtime and matching cached Mathlib dependencies. The external library cache and ordinary Lean trust base are retained assumptions. The separate LP, exact rational certificates, symbolic identities, and quadrature supply different verification routes for the specific claims they cover.

## Attempts retained

The [setup record](Setup_Attempts.json) preserves the initial wrong cache-path syntax, missing module, virtual-environment interpreter mistake, and a missing source in the temporary audit project. The [attempts directory](attempts/) retains the Python import failures and the first versions of the two new Lean proofs. Those Lean attempts failed on a required `noncomputable` annotation and an unfolding step; corrected versions subsequently pass. These are development outcomes, not failed evidence silently discarded.

## Next deltas

The immediate continuation is to formalize the integral identification and quantitative error/summation criteria, and to audit the external topological bridge separately from its integer-matrix obstruction. The existing two-loop RG, nonlinear/continuum, prime-discrepancy, physical-data, and production-source gates remain in the queue. Source-dependent questions, including the intended “Croft” reference, retain their need for an exact source.

This pass verifies scoped propositions and records new counterexamples. It does not establish RH, a natural Hilbert–Pólya operator, general unforced Navier–Stokes regularity, or missing physical and production-model assumptions.
