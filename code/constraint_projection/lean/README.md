> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# `lean/` — machine-checked proofs

The first formally verified result in this repository.

```bash
# install once (~30 s, no Mathlib needed)
curl -sSL https://elan.lean-lang.org/elan-init.sh | sh -s -- -y \
     --default-toolchain leanprover/lean4:v4.15.0
export PATH="$HOME/.elan/bin:$PATH"

lean code/constraint_projection/lean/LFBound.lean     # ~0.8 s; exit 0 = all theorems verified
lean code/constraint_projection/lean/AxiomIII.lean    # ~0.9 s

# PerZero.lean needs Mathlib (real analysis is outside Lean core):
cd code/constraint_projection/lean/withMathlib
lake exe cache get          # ~5 GB, once
lake env lean PerZero.lean  # ~4 s; exit 0 = verified
```

## Why this exists

**`T1` in this repository has always meant "an automated test passes, reproducible by
running the code."** That is a Python assertion — sympy agreeing with sympy. It is not a
proof, and the label is stronger than the thing. A Lean kernel-checked proof is
categorically different, so it gets its own tier (**T0**) rather than being folded into T1.

Method adopted from Anthropic's Riemann-zeta pipeline (2026-08-10), which ends in a Lean 4
/ Mathlib formalization passing a standard checker. See `docs/Elimination_Ledger.md`,
2026-08-30.

## `LFBound.lean`

Formalises the proposition that carried the 2026-08-29 correction to this audit's *own*
earlier verdict: the Local Friendliness bound on the CPF manuscript's §5 sum
`S = E(A2,B2) + E(A2,B3) + E(A3,B2) − E(A3,B3)` is **exactly 4** — not 2, which is the
*Bell* bound the manuscript compares against.

| Theorem | Content |
|---|---|
| `corr2_le_two`, `neg_two_le_corr2` | every correlator lies in [−1,1] |
| `S_le_four` | `S ≤ 4` for any normalised non-negative behaviour |
| `star_is_LF` | the explicit witness is a genuine LF branch (non-negative, normalised, no-signalling, AOE-deterministic) |
| `star_S_eq_four` | the witness attains `S = 4` |
| `lf_bound_is_four` | attained **and** an upper bound ⇒ the LF maximum is 4 |

**Axiom dependencies** (`#print axioms`):

```
star_is_LF          does not depend on any axioms
star_S_eq_four      does not depend on any axioms
S_le_four           [propext, Quot.sound]
lf_bound_is_four    [propext, Quot.sound]
```

No `Classical.choice`, so the development is constructive. No `sorry`, no `native_decide`
(which would trust the compiler rather than the kernel).

## Design notes

- **No Mathlib.** Checks with a bare `lean` binary in under a second, so anyone can verify
  it without an hours-long build. Cost: `IsGreatest` and set-builder notation are
  unavailable, so `lf_bound_is_four` is stated as an explicit attained-and-bounded pair.
- **Doubled integer units.** `B x y a b` denotes `2 · p(a,b|x,y)`. Every probability in
  play is 0, ½ or 1, so doubling clears denominators and keeps everything in `Int`, where
  `omega` and `decide` close the goals.
- **The upper bound needs only normalisation and non-negativity**, not the LF conditions.
  That is deliberate and honest: it holds on all behaviours, so all the content is in
  *attainment* — that a bona fide LF behaviour reaches 4.

## Mutation tests

The proof has been shown capable of failing (repo rule: an instrument is not trusted until
it can fail). Lean **rejects** the file under each of:

| mutation | result |
|---|---|
| `S2 star = 8` → `= 9` | REJECTED |
| `S2 B ≤ 8` → `≤ 7` | REJECTED |
| one PR-box entry `1` → `0` | REJECTED |

## Scope — what is *not* formalised here

`LFBound.lean` says nothing about quantum mechanics. Two external facts, used in the audit
but **not** proved here, complete the argument: Tsirelson caps any quantum realisation of
this expression at `2√2`, and the Bell local bound is 2 (exhaustive over 64 deterministic
strategies, checked numerically in `cpf_triple_check.py`). Given those,
`2 < 2√2 < 4` puts the manuscript's value strictly inside the LF polytope.

Next candidates for formalisation: **Axiom III unsatisfiable** (finite group theory — the
centraliser of `diag(1,−1)` in `GL(2,ℤ)` and the order of a parabolic) and the **per-zero
`2π` contribution** in §7.


## `AxiomIII.lean` — Axiom III clause (3) has no model

The manuscript's Axiom III asks for `φ ∈ Diff(M)` with `φ_* = [[1,2],[0,1]]`, where
clauses (1)–(2) have already forced `M` to be the Klein bottle. Everything downstream of
`Tr(φ_*) = 2 = Sl` rests on it: `τ = i/2` (§3), `g` and `s` (§4), and
`λ_UV·λ_IR = 1/R⁴` (§8).

| Theorem | Content |
|---|---|
| `commutes_iff_diagonal` | the centraliser of `D = diag(1,−1)` is **exactly** the diagonal matrices |
| `phi_not_commutes` | `φ_*` is not in it |
| `phi_conj_D` | explicitly, `φ_*D = [[1,−2],[0,−1]]` while `Dφ_* = [[1,2],[0,−1]]` |
| `centraliser_unimodular` | its unimodular elements are **exactly the four** `diag(±1,±1)` |
| `trace_two_only_identity` | within that group, trace `+2` is attained **only by the identity** |
| `phi_infinite_order` | `φ_*ⁿ = [[1,2n],[0,1]] ≠ I` for `n ≥ 1` — so it lies in no finite group |
| `axiom_III_clause3_unsatisfiable` | the package |

**Axioms:** `propext`, `Classical.choice`, `Quot.sound`. Unlike `LFBound.lean` this
development is **not** constructive — `Classical.choice` enters through the automation.
Disclosed rather than hidden.

### Mutation tests

| mutation | result |
|---|---|
| `φ` made diagonal (so it *should* commute) | REJECTED |
| `D` made the identity (centraliser becomes everything) | REJECTED |
| drop one of the four centraliser elements | REJECTED |
| wrong power formula `2n → 3n` | REJECTED |

### Scope — the boundary, stated deliberately

**Proved:** the algebraic obstruction in full.

**Assumed, cited, not formalised:** that a diffeomorphism of `K` lifts to `T²` and induces
a matrix on `H₁` commuting with `D`, and that `MCG(K) = ℤ/2 ⊕ ℤ/2` (Lickorish, *Proc.
Camb. Phil. Soc.* **59** (1963) 307). Formalising surface topology is far beyond this
file, and those facts are not in dispute — **the manuscript's error is algebraic, and the
algebra is what is machine-checked.**

**Independent confirmation:** `cpf_triple_check.py` X1 reaches the same four matrices by a
route that never mentions the deck transformation — computing `Out(π₁(K))` from
`⟨a,b | bab⁻¹ = a⁻¹⟩` by symbolic word algebra. The two methods share no machinery.


## `withMathlib/PerZero.lean` — the per-zero 2π contribution (§7)

Machine-checks the step the audit's exact evaluation of §7's integral rests on. For a
zero at `β = ½` the two lines carry `α = +ε` and `α = −ε`:

| Theorem | Content |
|---|---|
| `imag_cancels` | the imaginary parts cancel **exactly**, every `ε` — `α` enters only as `α²` |
| `real_doubles` | the real parts combine to exactly `2[arctan((T−γ)/ε) + arctan(γ/ε)]` — `arctan` is odd |
| `contribution_lt_two_pi` | that is **strictly below** `2π` at every finite `ε` |
| `contribution_tendsto` | and **tends to** `2π` as `ε → 0⁺`, for `0 < γ < T` |
| `per_zero_two_pi` | the package |

**Why "→ 2π" and not "= 2π".** At any finite `ε` the contribution is strictly less; `2π`
is a supremum approached, never attained. Stating it as an equality would be wrong, and
the audit's prose said "→", so that is what is proved.

**Axioms:** `propext`, `Classical.choice`, `Quot.sound` — non-constructive, as Mathlib's
real analysis is. No `sorry`, no `native_decide`.

### Mutation tests

| mutation | result |
|---|---|
| contribution coefficient `2 → 3` | REJECTED |
| limit `2π → 3π` | REJECTED |
| bound `2π → π` | REJECTED |
| `imagPart` made **odd** in `α` (`α² → α`) — cancellation must fail | REJECTED |
| `realPart` sign flipped | REJECTED |

### Scope — what is *not* proved

That the closed form **is** the integral — the evaluation of `∫du/(α+iu)` itself — is not
formalised; it is standard calculus, and is taken here as the *definition* of `realPart`
and `imagPart`. What is proved is everything the audit's argument does **with** that
closed form: the cancellation, the doubling, the bound, and the limit. Summing over the
`N(T)` interior zeros then gives `2π·N(T)` — the residue count, without invoking the
residue theorem.

### Cost note

This is the first proof here that needs Mathlib. `LFBound` and `AxiomIII` check with a
bare `lean` binary in under a second; this one needs ℝ, `arctan` and filter limits, all
outside Lean core. That raises a reader's verification cost from a 30-second install to a
multi-gigabyte one — a real cost, and why it lives in its own directory rather than
alongside the self-contained files.
