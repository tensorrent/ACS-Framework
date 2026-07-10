> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# ACS Framework — Reproducible Computational Appendix

Computational appendix for the ACS (Asymmetric Codependent System) trilogy:

- **Paper A** — Pati-Salam phenomenology and parameter pruning
- **Paper B** — Spectral / resolvent reinterpretation of the Riemann explicit formula
- **Paper C** — Algebraic-closure framework, Killing-orthogonality, and inversion-arc taxonomy

This repository reproduces every numerical and symbolic result cited in the trilogy.

---

## Quick start

```bash
# Install
pip install -r requirements.txt

# Run all verifications (single command)
python -m pytest tests/ -v

# Run individual paper sections
python -m src.paper_a.branch_a_vacuum
python -m src.paper_b.resolvent_renormalized
python -m src.paper_c.killing_orthogonality
```

Expected runtime: under 60 seconds on a standard laptop.

---

## What's included

| Module | Result | Paper section |
|---|---|---|
| `paper_a/branch_a_parameters.py` | 5 free Higgs parameters irreducible | Paper A §4 |
| `paper_a/theta13_obstruction.py` | θ₁₃ not fixable by cross-couplings | Paper A §6 |
| `paper_a/branch_a_vacuum.py` | Reduced (α₂=0) potential admits stable vacuum | Paper A §5 |
| `paper_a/betac_tan_beta.py` | β_c forces tan β = ±1 at tree level | Paper A §5 |
| `paper_a/yukawa_no_go.py` | M_u = M_d when κ₁ = κ₂ (no-go theorem) | Paper A §5 |
| `paper_a/tm1_pmns.py` | TM1 ansatz fails phenomenology | Paper A §6 |
| `paper_b/explicit_formula_resolvent.py` | χ(ω) = Σ 1/(ω-γ_k) verified | Paper B §6 |
| `paper_b/wronskian_leibniz.py` | Wronskian fails Leibniz on scalar functions | Paper B §6 |
| `paper_b/renormalized_stability.py` | von Koch boundedness in log coordinates | Paper B §6 |
| `paper_b/berry_keating_counting.py` | BK leading semiclassical counting matches RvM | Paper B §6 |
| `paper_c/theorem_c.py` | ad_T_BL has minimal polynomial t(t-4/3)(t+4/3) | Paper C §3 |
| `paper_c/killing_orthogonality.py` | tr([X,Y]·X) = 0 (theorem + 1000-trial scaling) | Paper C §5.3 |
| `paper_c/orthogonal_complement_probe.py` | dim B⊥ = n²-2 reconstruction algorithm | Paper C §5.4 |
| `paper_c/spectral_taxonomy.py` | Three-class adjoint flow taxonomy | Paper C §5.5 |
| `paper_c/holonomy_representation.py` | 2π inversion is representation-specific | Paper C §5.5 |
| `paper_c/frenet_serret.py` | A³ = -(κ²+χ²)A — elliptic class instance | Paper C §5.5 |
| `paper_c/core_rope_ring.py` | R³ = R — hyperbolic class instance | Paper C §5.5 |

---

## Numerical conventions

**Random seed:** `20260423` is used throughout for reproducibility. Set in `src/common/seed.py` and imported by every script that uses random sampling.

**Precision:** Most computations use `numpy.float64`. The Branch A vacuum analysis uses Python's `decimal` module at 50-digit precision because the scale separation v / v_R ≈ 10⁻¹³ exceeds float64 capacity (catastrophic cancellation in Cramer's rule inversion). See `paper_a/branch_a_vacuum.py` for the documented numerical pitfall.

**Symbolic verification:** Where possible, identities are checked with SymPy returning `0` exactly, not numerical residuals. See `paper_c/killing_orthogonality.py` for an example.

---

## Repository structure

```
acs_codebase/
├── README.md                    # This file
├── requirements.txt             # pip dependencies
├── src/
│   ├── common/                  # Shared utilities (Lie algebra basis, seed, etc.)
│   ├── paper_a/                 # Phenomenology and parameter pruning
│   ├── paper_b/                 # Spectral reinterpretation
│   └── paper_c/                 # Algebraic closure framework
├── tests/                       # pytest-compatible verification tests
│   ├── paper_a/
│   ├── paper_b/
│   └── paper_c/
├── docs/
│   ├── ledger.md                # Full status of every claim
│   ├── numerical_pitfalls.md    # Scale-separation, cancellation, precision notes
│   └── citations.md             # Mapping of results to literature
└── extras/                      # Earlier exploratory scripts (not canonical)
```

---

## Verification ledger

See `docs/ledger.md` for the complete status of every claim:
- Rigorous (proved symbolically and/or numerically)
- Conjectural (flagged in papers as open)
- Disproved (negative results that delimit model space)

Negative results are first-class. Examples:
- Wronskian as Poisson bracket: **disproved** (Leibniz fails by −fgh').
- Equal-VEV alignment with phenomenological CKM: **disproved** (M_u = M_d).
- Universal 2π inversion across spectral classes: **disproved** (representation-specific).

---

## Citation

If you use this codebase, please cite the trilogy. See `docs/citations.md` for BibTeX entries and external references (Zamolodchikov 1986, Komargodski-Schwimmer 2011, von Koch 1901, Berry-Keating 1999, etc.).

---

## License

Released alongside the trilogy under the same license as the manuscripts.
Computations may be freely reproduced and extended; please cite when published.

---

## Known limitations

1. **No FeynRules/UFO model.** Paper A's Lagrangian is specified in standard PS form (see `src/paper_a/lagrangian_specification.md`) but has not been exported to FeynRules. This is Phase D1 of the roadmap — estimated 1-2 months of postdoc work.

2. **No Coleman-Weinberg analysis.** The β_c → tan β analysis is tree-level only. Whether one-loop CW corrections fix tan β uniquely is open. Estimated 2-4 weeks of focused symbolic work.

3. **No Hilbert-Pólya construction.** Paper B presents the trivial diagonal-H resolvent identity as motivation only; constructing a natural self-adjoint operator with exact spectrum {γ_k} remains open (100+ years).

4. **§7 of Paper A (h̃/h = 2/3 interpretation).** Whether this is matrix-level proportionality or invariant-level ratio determines whether `paper_a/yukawa_no_go.py` is an unconditional theorem or a strong indication. The codebase tests both interpretations; see the script docstring.

These limitations are documented honestly because they constrain the strength of specific claims in the papers.
