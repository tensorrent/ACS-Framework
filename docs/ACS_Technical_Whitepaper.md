> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Asymmetric Codependent Systems (ACS) — Technical Whitepaper

**Status amendment, 24 September 2026.** This is a historical overview. The [publication update](publication/2026-09-24/README.md) governs its physical interpretation: the complete scalar action retains undetermined coefficients, vacuum and physical scale. Framing does not derive `g=2`; balanced triplet expectation is not a singlet; the stated torsion-squared term is algebraic. The two new papers give the forward calculations, counterexamples and remaining inputs. The overview's cross-domain equations require their stated domains and maps; they are not universal identities between unlike objects.

This document provides a consolidated mathematical and physical specification of the Asymmetric Codependent Systems (ACS) framework. It outlines the algebraic foundations of the gauge sector, the spectral positional duality of L-functions, the holographic boundary conditions of the inversion arc, and the deterministic AI stack governance model.

---

## 1. Core Mathematical Axioms

### 1.1 The Primitive: Asymmetric Transfer Entropy
In a coupled nonlinear system with two state spaces $X$ and $Y$ governed by codependent evolution dynamics, the net transfer entropy $\Delta I$ measures the direction and magnitude of information flow:

$$\Delta I = T_{Y \to X} - T_{X \to Y}$$

The sign of $\Delta I$ defines the governance relation:
- $\Delta I > 0$: $Y$ acts as a driver/constraint on $X$ (Form governs Function).
- $\Delta I < 0$: $X$ acts as a driver/constraint on $Y$ (Function governs Form).
- $\Delta I = 0$: Stable information-balance (attractor state).

### 1.2 The BCH–Transfer-Entropy Morphism
For two mutually-constraining fields represented by local algebra generators $f, g$, the net transfer entropy $\Delta I$ under a short-time evolution step $\tau$ is mapped to the Lie bracket through a second-order Taylor expansion:

$$\Delta I(\tau) = \tau^2 [f, g] + \mathcal{O}(\tau^3)$$

This relation establishes a direct morphism between information dynamics and Lie algebras, ensuring that stable information flow corresponds to algebraic closure.

---

## 2. The Gauge Sector (Paper A)

### 2.1 The Palatini Bracket
Applying the BCH-TE morphism to the vierbein $e^a{}_\mu$ and connection $\omega^{ab}{}_\mu$ in Palatini gravity, the Lie bracket generates the split real Lie algebra $\mathfrak{sl}(4, \mathbb{R})$ (dimension 15, rank 3):

$$[e, \omega] \in \mathfrak{sl}(4, \mathbb{R})$$

The Palatini decomposition splits $\mathfrak{sl}(4, \mathbb{R})$ into two sectors:
1. **Lorentz Sector (6-dimensional):** $\mathfrak{so}(3,1)$, representing local Lorentz transformations.
2. **Torsion Sector (9-dimensional):** The remaining generators, representing spacetime torsion.

### 2.2 SU(3) Closure and the Chirality Map
Among 50,000 uniformly sampled 8-dimensional subspaces of $\mathfrak{sl}(4, \mathbb{R})$, the split real form $\mathfrak{sl}(3, \mathbb{R})$ is the only subspace found to achieve numerically exact closure under the bracket map (**T3** — a numerical selection result consistent with Dynkin's classification, not a proved uniqueness theorem; see MANIFEST):

$$\mathcal{D}_{\mathfrak{sl}(3, \mathbb{R})} < 10^{-14}, \qquad \mathcal{D}(V) > 0.49 \text{ for every sampled alternative } V$$

To recover the compact $\mathfrak{su}(3)$ strong force gauge group, we define a complex linear chirality map $J$ on the generators:

$$J(T) = i\,\text{sym}(T) + \text{anti}(T)$$

Under $J$, the Cartan classification maps the non-compact generators of $\mathfrak{sl}(3, \mathbb{R})$ to skew-Hermitian generators closing exactly on $\mathfrak{su}(3)$:

$$\mathfrak{sl}(3, \mathbb{R}) \xrightarrow{J} \mathfrak{su}(3)$$

### 2.3 Derived Parameters from Palatini Closure
> **Status note (per the Elimination Ledger, OOS01/Q1, T1 machine-verified):** the *relations* below survive changes of normalisation convention, but the *bare numerical values* are **refractions** — they move under legitimate changes of trace normalisation or state-counting prescription and are therefore prescription-dependent, not invariants.

- **Higgs Quartic Coupling:** from the geometric projection of the holonomy onto the Higgs direction (value scales with the Killing-form norm convention):
  $$\lambda_\phi = \frac{2\sqrt{3}}{27} \approx 0.1283$$
- **Barbero-Immirzi Parameter:** from the information-balance condition ($\Delta I = 0$) over the discrete spin area spectrum (value depends on the SU(2) vs SO(3) counting prescription: $0.274067$ vs $0.190206$):
  $$\sum_j (2j+1)e^{-2\pi\gamma\sqrt{j(j+1)}} = 1 \implies \gamma \approx 0.274067$$

---

## 3. The Spectral Sector (Paper B & Note N3)

### 3.1 Positional Duality
Let $u_1 < u_2 < \dots < u_N$ be the unfolded zeros of the Riemann zeta function $\zeta(s)$. The spectral statistics of the zeros decompose into three structurally independent layers:

1. **Density (Analysis):** Governed by the smooth Riemann–von Mangoldt term, carrying no arithmetic information.
2. **Local Spacings (Universality):** Governed by the Gaussian Unitary Ensemble (GUE) universality class.
3. **Positions (Arithmetic):** Governed by the primes via the Weil-Guinand explicit formula.

$$\langle\cos(\gamma_i \log p)\rangle \propto - \frac{\ln p}{\sqrt{p}}$$

### 3.2 Spacing Universality and the Shuffle Knife
Using the **shuffle knife** operator, we randomly permute the nearest-neighbor spacings $\{s_i\}$ while preserving the one-point spacing distribution class. Testing witnesses on the real vs. permuted sequences reveals:
- **Form (Universality):** Spacing and counting functions remain within $0.4\sigma - 1.0\sigma$ of the surrogate null.
- **Function (Arithmetic):** Prime-resonance collapses under permutation (exhibiting $\sim\!11,500\sigma$ significance on the real sequence).

This supports arithmetic sensitivity of the tested position observables relative to the specified shuffle controls. It does not establish universal arithmetic blindness of all spacing statistics or prove RH.

---

## 4. Holographic Resolution (Paper C)

### 4.1 Killing-Orthogonality
In the boundary mapping of the inversion arc, we define the boundary state space as the orthogonal complement of the bulk gauge orbit under the Lie algebra Killing form $B(\cdot, \cdot)$:

$$\mathfrak{g}_{\text{boundary}} = \mathfrak{g}_{\text{bulk}}^\perp$$

For any bulk generators $X, Y$, the boundary projection satisfies:

$$B([X, Y], Z) = 0 \quad \forall Z \in \mathfrak{g}_{\text{bulk}}$$

This algebraic orthogonality provides an algebraic correspondence consistent with ER=EPR (**T2/T3** per MANIFEST; the full holographic correspondence remains an open problem, corpus map O-6), where bulk Einstein-Rosen wormhole geometries would map to boundary EPR entanglement via the algebra's radical.

---

## 5. Deterministic AI Stack Governance (Paper D = `papers/ACS_Deterministic_AI_Stack_PDR.tex`, with the formal companion `papers/discrete_geometry_formalism.tex`)

### 5.1 The Constraint-Attractor Cycle
The ACS Deterministic AI Stack is governed by a closed constraint-attractor loop that prevents model drift:

```
   ┌───────────┐   Solve    ┌─────────────┐  Promote   ┌───────────┐
   │ Constraint│ ─────────> │  Attractor  │ ─────────> │Constraint │
   │   Set k   │            │    State    │            │  Set k+1  │
   └───────────┘            └─────────────┘            └───────────┘
         ▲                                                    │
         └────────────────── Feedback ────────────────────────┘
```

1. **Solve:** The system solves the current constraint set $C_k$ to locate a stable attractor state.
2. **Promote:** The properties of this attractor state are algebraically locked and promoted to become part of the constraint set $C_{k+1}$ for the next cycle.
3. **Feedback:** Any deviation triggers information-balance corrections ($\Delta I \neq 0$), returning the system to the attractor basin.

---

## 6. Author Provenance, Neurodiversity Context & Analog MoE Assistive Methodology

All novel theories, geometric architectures, physical intuitions, and mathematical hypotheses across the ACS Framework are the independent intellectual creation of the human author, **Bradley Wallace**, developed over approximately **5,000–6,000 hours** of focused solo research.

### Neurodiversity Accommodation & The Human-in-the-Loop "Analog MoE"
The author lives and works with **dyslexia and ADHD**. To overcome the severe cognitive and mechanical friction of conventional linear reading and keyboard text composition, the author developed and directed a **human-in-the-loop "Analog Mixture-of-Experts" (MoE)** ensemble comprising:
- **OpenAI GPT**
- **Anthropic Claude**
- **xAI Grok**
- **DeepSeek**
- **Google Gemini**
- **Cursor**
- **Google DeepMind Antigravity**

The author interacted with these models primarily through **high-bandwidth voice-to-text / speech interfaces** to:
1. Dictate raw conceptual insights, geometric visions, and physical hypotheses in real-time.
2. Intake, audio-synthesize, and analyze dense external mathematical and physical literature.
3. Rapidly iterate, structure, and transcribe spoken formulations into rigorous LaTeX and Markdown manuscripts.
4. Orchestrate **adversarial cross-examination**, where models were pitted against each other to critique derivations, audit code, stress-test conjectures, and eliminate errors.
5. Scaffold, execute, and verify automated numerical and exact symbolic test harnesses.

The AI ensemble did not generate the underlying physical theories or mathematical hypotheses; they functioned as an assistive cognitive prosthesis for transcription, intake, and multi-model cross-examination under the author's direct guidance. The recorded chat histories and session archives serve as the timestamped auditable ledger tracing every core concept to the author's spoken ideation.
