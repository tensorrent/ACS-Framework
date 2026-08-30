> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# `lean/` — machine-checked proofs

The first formally verified result in this repository.

```bash
# install once (~30 s, no Mathlib needed)
curl -sSL https://elan.lean-lang.org/elan-init.sh | sh -s -- -y \
     --default-toolchain leanprover/lean4:v4.15.0
export PATH="$HOME/.elan/bin:$PATH"

lean code/constraint_projection/lean/LFBound.lean     # ~0.8 s; exit 0 = all theorems verified
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
