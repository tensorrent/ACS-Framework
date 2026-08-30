> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# `constraint_projection/` — audit instrument for the CPF manuscript

Companion computation to `papers/notes/Constraint_Projection_Framework_Audit.tex`.
Target: `papers/notes/Constraint_Projection_Framework.tex` (archived as submitted).

```bash
python3 code/constraint_projection/cpf_audit.py              # first pass, C1-C8, ~2 s
python3 code/constraint_projection/cpf_full_verification.py  # full pass, V1-V9, ~30 s
python3 code/constraint_projection/cpf_full_verification.py --deep   # + contour integrals, ~4 min
python3 code/constraint_projection/wave_equation_gfactor.py  # where g=2 comes from, ~5 s
```

Deps: `numpy`, `sympy`, `mpmath` (60-digit precision for the cutoff arithmetic).
Runtime ~2 s. Writes `docs/constraint_projection_audit.json`.

## What it checks

Each check is written so the manuscript could pass it; no verdict is assumed.

| Check | Question | Verdict |
|-------|----------|---------|
| **C1** | Do the manuscript's own inputs give $\alpha^{-1}=\ln(8R/a)+1$? | **No** — sympy returns $L\alpha=2$, so $\alpha^{-1}=\tfrac12(\ln(8R/a)+1)$. Factor of 2 dropped |
| **C2** | How many values must the "not free" cutoff $a$ take? | **Four**, spanning 117.4 decades. One free parameter, fitted per section |
| **C3** | Does Axiom III's Dehn twist exist? | **No** — $\mathcal{M}$ is forced to be the Klein bottle, $\mathrm{MCG}(K)=\mathbb{Z}/2\oplus\mathbb{Z}/2$ is finite, $\phi_*$ is parabolic of infinite order. Exact integer arithmetic |
| **C4** | Do $g=Sl=2$ and $s=Sl/4$ hold? | **No** — both killed 2026-07-26; re-stated against the ledger |
| **C5** | Can $k(\varepsilon)$ see an off-line zero? | **No** — invariant under $\beta\mapsto1-\beta$; and on-line zeros give $k\to-\infty$ |
| **C6** | Is $S=2\sqrt2$, and is it a Local Friendliness sum? | **Yes / No** — arithmetic confirmed to machine precision; but no friend setting appears, so it is CHSH |
| **C7** | What mass does the quantum-pressure term need? | $9.6\times10^{-24}$ eV — an ultralight scalar. Also double counts $\tfrac12\rho v^2$ |
| **C8** | Axioms I–II and the bibliography | Axiom I false (abelian ⇒ amenable), Axiom II ill-posed, two citations wrong |

## Notes

- **C2 reproduces a repository result independently.** The CODATA-matching aspect
  it computes, $a/R = 2.03905\times10^{-118}$, matches the $\approx2.039\times10^{-118}$
  already published in `papers/notes/Mobius_Ribbon_Capacitance.tex` — which is also
  where the C1 correction was first recorded, in July 2026.
- **C3 is exact.** No floating point enters: the centraliser computation, the
  conjugation $\phi_*D\phi_*^{-1}$, and the order of $\phi_*$ are integer matrix
  arithmetic in sympy.
- **C6 is the one pass.** Recorded as such; the repository's discipline is that a
  correct step inside a failed argument is still reported correct.
- The script only ever writes `docs/constraint_projection_audit.json`; it does not
  touch any other tracked artifact.


## Second pass — `cpf_full_verification.py`

The first pass settled three of its eight checks by structural argument rather than
computation. This one computes all of them. **Two verdicts moved, both against the
manuscript.**

| Check | Question | Result |
|-------|----------|--------|
| **V1** | Which closed surface has double cover $T^2$? | Klein bottle, uniquely — Euler census + Smith normal form |
| **V2** | Does Axiom III's $\phi$ exist? | No — exhaustive search over 390,625 integer matrices; centraliser has order 4 |
| **V3** | Is the $\alpha$ step a derivation? | No — $L\alpha=2$, and the cutoff step returns *any* target ($42$, $1000$, $-7$) |
| **V4** | How many cutoffs? | Four, 117.4 decades apart; plus $\Lambda_{\rm eff}$ vs Planck |
| **V5** | What does §7's **integral** equal? | $2\pi N(T)/T \to \log(T/2\pi e) \to +\infty$ — **not** the claimed sum |
| **V6** | What is the **LF** bound on §5's sum? | **4** (LP) — so $2\sqrt2$ violates no LF inequality |
| **V7** | Is it the Bohm quantum potential? | No — $Q=-\frac{\hbar^2}{2m}\nabla^2R/R$, not $\lvert\nabla\psi\rvert^2$ |
| **V8** | Is the reservoir non-amenable? | No — Følner sequences; every abelian group is amenable |
| **V9** | Do the prior kills reproduce? | Yes — `framed_unknot/` re-executed, byte-identical |

`--deep` recomputes V5's contour integrals with `mpmath` (contour split at the zero
ordinates); without it the recorded values are reported and the residue argument is
still derived symbolically.

> **Note on the committed artifact.** `docs/constraint_projection_full_verification.json`
> was produced by a `--deep` run, so its V5 numerics are genuinely recomputed
> (`deep_mode: true`). A default run reproduces the same table from the recorded values
> and writes `deep_mode: false` — expect that one-field diff if you re-run without the
> flag.


## `wave_equation_gfactor.py` — where $g=2$ actually comes from

Successor to the 2026-07-26 `Sl = 2 ↔ g = 2` kill, which closed on Lévy-Leblond as its
decisive citation without ever running it.

| Check | Result |
|-------|--------|
| **W1** | $\sigma$ algebra verified, all 9 pairs |
| **W2** | $(\sigma\cdot\pi)^2 = \pi^2 - q\hbar(\sigma\cdot B)$, symbolic, non-commuting $\pi_i$ |
| **W3** | Lévy-Leblond → free Schrödinger → **$g = 2$**. No $c$, no Lorentz, no metric |
| **W4** | $4\pi$ periodicity from $\pi_1(SO(3))$ — a group, not a surface |
| **W5** | Tree Dirac gives 2 as well: $g=2$ diagnoses neither relativity nor topology |
| **W6** | $a_e = 1.15965218059(13)\times10^{-3}$; "$g=2$" is $8.92\times10^9\sigma$ away |
| **W7** | QED series, **validated by inverting for $\alpha^{-1}$** against Fan et al. |
| **W8** | vs independent $\alpha$: Rb 2.1σ, Cs −3.9σ, Rb-vs-Cs 5.5σ |
| **W9** | parameter count: topology buys nothing $su(2)$ didn't give free |

> **Two traps this script exists to document.** (1) The mass-dependent QED terms
> ($A_2(m_e/m_\mu)$, $A_2(m_e/m_\tau)$) contribute $2.75\times10^{-12}$ — roughly 20× the
> experimental uncertainty. Omit them and any comparison is invalid. (2) CODATA's $\alpha$
> is partly determined *by* $a_e$ plus QED theory, so using it to "predict" $a_e$ is
> circular; use the atom-recoil determinations. Both traps were hit on the first run and
> caught by the W7 inversion.
