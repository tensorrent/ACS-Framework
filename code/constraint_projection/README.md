> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# `constraint_projection/` — audit instrument for the CPF manuscript

Companion computation to `papers/notes/Constraint_Projection_Framework_Audit.tex`.
Target: `papers/notes/Constraint_Projection_Framework.tex` (archived as submitted).

```bash
python3 code/constraint_projection/cpf_audit.py
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
