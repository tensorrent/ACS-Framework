# ACS Framework (Asymmetric Codependent Systems)

This repository contains the canonical manuscripts, mathematical notes, verification suites, and reproduction harnesses for the Asymmetric Codependent Systems (ACS) theoretical framework. 

---

## Repository Structure

```
.
├── MANIFEST.md                       # Claim-to-code mapping & verification matrix
├── README.md                         # This file
├── LICENSE                           # Sovereign Integrity Protocol License (SIP License v1.1)
├── papers/                           # Research manuscripts and notes
│   ├── core_trilogy/                 # The core three papers of the framework
│   │   ├── Palatini_Gauge_Attractor.tex   # Paper A: SU(3) closure attractor in Palatini gravity
│   │   ├── Riemann_Spectral_ACS_ext.tex # Paper B: Extended spectral Riemann hypothesis form
│   │   ├── Spectral_Witness_Refinement.tex # Paper B': Retitled, tightened witness survival variant
│   │   └── Holographic_Spectral_Inversion.tex         # Paper C: Holographic resolution & ER=EPR correspondence
│   ├── notes/                        # Mathematical companion notes
│   │   ├── Pythagorean_Lattice_Limits.tex # Note N1: Pythagorean structure in minimal PS algebra
│   │   ├── Adjoint_Clifford_Adjoint_Clifford_Adjoint_Clifford_Adjoint_Clifford_Adjoint_Clifford_Signature_Selection.tex   # Note N2: Metric signature from adjoint spectral activity
│   │   └── Prime_Gap_Prime_Gap_Prime_Gap_Prime_Gap_Prime_Gap_Transition_Operator.tex   # Note N3: Prime-gap Dynamical Dynamical Dynamical Dynamical Dynamical Transition Operators over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless
│   ├── methodology/                  # Empirical tools and frameworks
│   │   ├── Spectral_Rigidity_Shuffle_Knife.tex # FF06e: The original shuffle-knife discriminant
│   │   ├── Prime_Carrier_Position_Form_Factor.tex # FF06f: Positive ID of the prime carrier as the position pair correlation (explicit formula, r=0.9975)
│   │   └── Form_Function_Relativity.tex # FF06g: The form/function label is relative to the reference frame (companion to FF06e)
│   ├── later_FF06_series/            # Chronological research thread documents
│   │   ├── Three_Layer_Decomposition.tex # Level decomposition of the Riemann zeros
│   │   ├── The_Geometry_Engine.tex   # Reference engine specification
│   │   ├── When_a_Number_Lies.tex    # Relational limits and domain tests
│   │   ├── The_Reversible_Flattening.tex # Reversible flattening processes
│   │   ├── The_Reversible_Flattening_Monograph.tex
│   │   ├── The_Reversible_Flattening_Process_Record.tex
│   │   ├── The_Elimination_Ledger.tex # Record of falsifications & refractions (K1)
│   │   └── One_Mechanism_Many_Forms_Sigma.tex # Consolidated synthesis (Σ)
│   ├── Form_Function_and_Asymmetry.tex # Consolidated core monograph
│   ├── ACS_Deterministic_AI_Stack_PDR.tex # Paper D: Deterministic AI Stack blueprint
│   └── discrete_geometry_formalism.tex # Dynamical Epistemic Algebra formalization
│
├── code/                             # Scientific verification suites
│   ├── acs_codebase/                 # Core verification package
│   │   ├── src/                      # Source implementations for Papers A, B, and C
│   │   ├── tests/                    # Pytest verification suite (42 passing assertions)
│   │   └── extras/                   # Specialized standalone verification scripts
│   ├── notes_verification/           # Companion scripts for Notes N1, N2, and N3
│   └── hp_knife_suite/               # Hilbert-Pólya shuffle-knife verification suite
│       └── data_zeros/               # Extracted zeros and generation scripts
│
├── docs/                             # Framework documentation
│   ├── ACS_Technical_Whitepaper.md   # Consolidated mathematical/physical whitepaper
│   ├── ACS_Master_Index.md           # Page/line index for all manuscripts
│   ├── ACS_Corpus_Map.md             # Logical map of the theoretical claims
│   ├── Elimination_Ledger.md         # Detailed record of the 8 falsified claims
│   ├── README_verification_suite.md  # Detailed developer guide for the code
│   └── ACS_FRAMEWORK_SKILL.md        # LLM context instruction module
│
├── harness/                          # Execution and telemetry scripts
│   └── training/                     # Unified Phase-1 training and telemetry sweeps
│
├── scripts/                          # Supporting helper scripts
└── visualizations/                   # Interactive visual models
    └── acs_q_plane_confinement_simulator.html # Q-plane confinement visualizer
```

---

## Claims and Verification Matrix

Every mathematical or numerical claim in the papers is tracked under a strict four-tier verification hierarchy in [MANIFEST.md](MANIFEST.md). Tiers never promote; numerical approximations (T3) are explicitly distinguished from exact mathematical proofs (T2).

### Core Theoretical Focus

1. **Gauge Group Selection (Paper A):** Derivation of Pati-Salam $\mathfrak{su}(4) \times \mathfrak{su}(2)_L \times \mathfrak{su}(2)_R$ and the emergence of the compact real form $\mathfrak{su}(3)$ of the strong force as a geometric closure attractor.
2. **Spectral Positional Duality (Paper B):** Numerical proof that the arithmetic information of the Riemann zeros is encoded strictly in their level locations (governed by the explicit formula) rather than their local spacing distributions (which are universally GUE and arithmetic-blind).
3. **Algebraic Holography (Paper C):** Formalization of Killing-orthogonality and three-class spectral taxonomies mapping algebraic structures to holographic boundary conditions.

---

## Replication and Test Execution

### 1. Curated Core Test Suite (42 Assertions)
To run the automated verification suite for the core trilogy (requires `numpy`, `scipy`, `sympy`, and `pytest`):

```bash
cd code/acs_codebase
pip install -r requirements.txt
python -m pytest -v
```

### 2. Standalone Verification Scripts
The individual claims and physical parameters are calculated by standalone python modules in `code/acs_codebase/extras/`:

*   **Barbero-Immirzi Parameter ($\gamma \approx 0.274$):**
    ```bash
    python code/acs_codebase/extras/barbero_immirzi_correct.py
    ```
*   **Koide Lepton Mass Relation ($0.001\%$ fit):**
    ```bash
    python code/acs_codebase/extras/koide_clebsch_gordan.py
    ```
*   **Higgs Mass Ratio ($m_H/v \approx 0.506$ vs. physical $0.508$):**
    ```bash
    python code/acs_codebase/extras/higgs_mass_ratio.py
    ```

### 3. Hilbert-Pólya Shuffle-Knife Verification
To reproduce the level-decomposition and spacing universality metrics:

```bash
cd code/hp_knife_suite
python hp_never_synced.py      # Verifies spacing properties (zeros vs GUE vs lattice)
python hp_xp_test.py           # Verifies Berry-Keating xp-operator limits
python hp_signed_lfunction.py  # Checks zeta weights and quadratic L-function signs
python hp_phase_test.py        # Validates complex character phases (demodulation R = 0.99)
python hp_form_function_relativity.py         # Form/function label is frame-relative (2 exact frames, ~2s)
python hp_form_function_relativity.py --full  # adds the GUE-full(bulk) rung (dense diagonalisation, ~7 min)
```

---

## Scientific Scope & Guidelines

> **This repository documents an active research program, not a completed theory.** All results are tiered T1–T4 (machine-verified / proved / numerically verified / explicitly falsified); tiers never promote. Open problems remain — including the Hilbert-Pólya operator construction and the L-functions extension — and **the Riemann Hypothesis is nowhere concluded or claimed proved** by this framework. Parameter-count claims (7 inputs, 2.7× reduction) are specific to Branch A (minimal bi-doublet); alternative Higgs sectors change the count. The Barbero-Immirzi parameter γ = 0.274 is the unconstrained information-balance value, pending Chern-Simons state-counting verification. Falsified claims are documented openly in the [Elimination Ledger](docs/Elimination_Ledger.md), not hidden.

*   **Replication Seed:** The stochastic portions of the codebase use the canonical seed `20260423`.
*   **Zero Dataset:** Zeros used are Odlyzko's first 100,000 Riemann zeros, located under `code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt`.
*   **Dirichlet L-Function Zeros:** Zeros are calculated directly from $L(s, \chi)$ using Hurwitz zeta functions without inserting prime values, ensuring non-circularity in character readouts.
*   **Falsifications:** Rather than being hidden, explicitly falsified claims (such as the standard $2\pi$ loop inversion or standard Wronskian-Poisson equivalence) are detailed in [docs/Elimination_Ledger.md](docs/Elimination_Ledger.md).
