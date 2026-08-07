# Cross-Repository Glossary Extract (historical)

> **Note (2026-08-07).** This document is an extract from a cross-repository
> catalogue and includes vocabulary from codebases that are *not* part of this
> repository. It is preserved for provenance. The canonical, self-contained
> glossary for this repository is [`../GLOSSARY.md`](../GLOSSARY.md).

Coined and specialized vocabulary used in this repository: what each named object is,
its domain and codomain, what it composes with, where it is defined, and whether it is
built or specified.

**This is an extract.** The canonical cross-repo catalogue — covering every tensorrent
repository, with the full status ledger and the coverage/provenance notes — lives at
`dev/docs/GLOSSARY.md`. Section numbers below are that document's numbering, so
cross-references to sections not reproduced here resolve against the canonical copy.

Compiled 2026-07-30 from source and spec files. Every entry cites its defining location.

> Read §1 first. It catalogues the deliberate homonyms (three senses of "scroll", two of
> "well", two of "motif"), the standard terms this program redefines (CDCL, ζ, ring,
> rainbow table), and the genuine cross-repo collisions — including three incompatible
> F369 tables all carrying the EigenCharge name.

---

## 1. Read this first: homonyms, collisions, and contested definitions

The program reuses a small set of nouns at several scales deliberately, and in a few places accidentally. A reviewer who does not know which is which will mis-type objects. This section is the disambiguation table; the detailed entries follow in §3 onward.

### 1.1 Deliberate homonyms — the same word, genuinely different objects

These are intentional. Both senses are load-bearing and are **not** interchangeable.

| Word | Sense A | Sense B | Distinguish by |
|---|---|---|---|
| **well** | *concept well* — a named attractor in router concept space, `{id, keywords[]}` | *reasoning well* — one of 8 thinking archetypes (Deductive, Skeptical, Narrative, Systems, Ethical, Compression, Exploratory, Grounding) | A is data in `wells.json`; B is an enum in `orchestrator.ts` |
| **motif** | *memory motif* — a recurring event window promoted to a name | *color motif* — a 16-hex content address of a byte block | A is in `motif-memory.ts`; B is in `spectral_assembler.ts`. The repo flags the collision explicitly at `aiso/frontend/tools/well-port/PRD.md:198` |
| **scroll** | *reasoning scroll* — append-only decision ledger | *storage scroll* — CRDT event log with frontier root | *codec scroll* — hash-linked chunk chain | All three are append-only and hash-chained; the storage sense adds CRDT merge, the codec sense adds Merkle proofs over 216-byte blocks |
| **vixel** | *AISO routing sense* — signal carrier / Merkle path node | *sovereign_vixel sense* — a 32³ octree encoded as a single 32768-bit Tupper integer | A is active and typed; B is a 49-line aspirational prototype |
| **ring** | *access ring* — R0–R4 visibility level resolved from auth factors | **Not** an algebraic ring | Always the access sense in `rings.ts`; the algebraic sense appears only in the FHE work as `F_P` |
| **rainbow table** | *Vexel rainbow* — precomputed grid coordinates for one Vexel's keywords | **Not** the password-cracking structure | Always the Vexel sense in this codebase |
| **witness** | *independence witness* — a re-implementation used to check the primary one | *epistemic witness* — the distinct source that vouched for a learned well | *spectral witness* — a statistic in the ACS instrument suite | Three unrelated senses in three subsystems |
| **keystone** | *KSM entry* — a CLVM/Chialisp trap with Trap/Fix/Invariant fields | *masterclass keystone* — a source-tiered study artifact from external literature | A is in `.agents/keystone_map_guide.md`; B in `.agents/*_masterclass_keystone.md` |

### 1.2 Redefined standard terms — the word exists in the literature and means something else here

**These are the highest-risk items for an outside reader.**

| Term | Standard meaning | Meaning in this program |
|---|---|---|
| **CDCL** | Conflict-Driven Clause Learning (SAT solving) | **Constraint-Driven Consensus Layer** — a transparent-constraint engine where clauses carry dispositions and provenance. It borrows the backjump idea but is not a SAT solver |
| **EigenCharge** | — (coined) | Two *incompatible* definitions exist; see §1.3 |
| **ζ (zeta)** | The Riemann zeta function | In the RC Stack, ζ is a **Boolean predicate** — a five-gate conjunction certifying a system state. Not a scalar, not a hash, not Riemann's ζ. The prime/FHE arm *does* use Riemann's ζ, so both live in the corpus |
| **Σ-Engine** | — (coined) | A spectral instability estimator; the one component in ζ deliberately allowed to use floating point |
| **holography** | AdS/CFT bulk-boundary correspondence | Used in the strict sense of HR-1/HR-2/HR-3 (boundary encoding + external accessibility + faithfulness); the Ryu–Takayanagi analogy is stated as structural, not derived |
| **tensegrity** | Buckminster Fuller's tension-compression structures | Read as an ACS instance: cables = Form, struts = Function, with a proved lemma that rigidity-matrix zero modes align with gauge freedoms |

### 1.3 Genuine collisions — the same name, different mathematics, in the same program

These are defects rather than design, and a reviewer should treat cross-repo claims about them with care.

**EigenCharge / the F369 table.** At least three distinct constructions carry this name:

| Where | Table size | Trace definition | Hash |
|---|---|---|---|
| `aiso/frontend` (Trinity) | 12,000 entries | positional — byte index rotated by position | FNV-64 |
| `HashCloud-SPE/crates/consensus` | 369 entries, distinct primes | `Σ F369[byte % 369]` | FNV-64 (v1) / SipHash-2-4 keyed on `UBC_ID` (v2) |
| `omniforge-full/python` | 512 entries | closed-form recurrence `t[i] = (i(i−1)/2)·3 − ⌊i/3⌋·6 + ⌊i/9⌋·9` | FNV-1a |

The closed-form recurrence is shared, the table lengths and the reduction are not. **Charges from these three are not comparable**, and the "same word charges bit-identically across runtimes" contract holds only *within* the Trinity family (Rust / WASM / TypeScript), where it is enforced by an equivalence test.

**SPE.** Canonically **Symbolic Pointer Engine**. The expansion "Storage Proof Engine" appears once, in `koba42-prime-thread-scroll/docs/HASHCLOUD_PRIME_SCROLL_INTEGRATION.md`, and is a mis-expansion.

**Ephemeral mask discipline.** The papers assert masks drawn uniformly and used once. Three implementations use a **constant mask `r = 1`** instead — `prime-field-bigint.ts:41`, `homomorphic-prime-fhe.ts:26`, `multi-key-threshold-fhe.ts:42` — and the H-PSI alert token hard-codes `alertMask = 0xabcdef123456n`. These do not satisfy the information-theoretic secrecy argument the papers state. Only `interactive-client-assisted-fhe.ts`, `multi-ring-shift-cipher.ts`, `homomorphic-csam-psi-matcher.ts`, and `unified-private-ai-platform.ts` take a caller-supplied uniform mask.

**Blinded evaluation handle `H_mult`.** Asserted as Theorem 2 / Theorem 4 in the ePrint and PETS manuscripts and in the README; **refuted in the source**, where `generateBlindedEvalHandle` and `serverMultiplyBlinded` are marked `@deprecated` with a regression test pinning the impossibility. This is a live documentation/code divergence, not a resolved one.

### 1.4 Contested acronyms

Two central names have no single canonical expansion in the corpus.

**TENT** — dominant usage (roughly 15 of 25 occurrences) is *Tensor Entanglement Network Technology*. Also found: *Thermodynamic Engine for Natural Topology*, *Topology of Evolving Neural Terrain*, *The Entropy-Nullifying Transceiver*, *Truth Encoded in Nested Topology*, *TensorRent Intent-Topology*, *Tensor Engineering & Networking Toolkit*, *Test-first Enforcement Network Technology*. One file hedges openly: "Tentative Emergent Neural Topology? – based on the code context."

**SEGGCI** — the README's own subtitle gives *Self-Improving, Ethically Grounded, Geometrically Coherent Intelligence*. Also found: *Sovereign Epistemic Governance & Graph Constraint Integration* (one doc flags this as possibly unsourced), *Stability Emergence Geometric Coherent Intelligence*, *Self-Evolving Generalized Governance & Cognitive Intelligence*.

**AKPP** — appears in "AKPP Underdetermination Bound (Theorem 5)" and is **never expanded anywhere in either repo**; the theorem is a one-line assertion with `∎` and no proof body.

### 1.5 Non-injective vocabularies

The **mobioud** prime-triad lexicon reuses triples across versions with different meanings: `(101,103,107)` is *Resonance/Insight/Flow* in v2, *Systemic Acceptance* in v3, and *Master Symmetry* in v5; `(191,193,197)` is *Invariant Clarity* in v4 and *Total Recall* in v5. Later versions overwrite rather than extend, so the map `ℙ³ ⇀ ConceptLabel` is partial and version-dependent.

---


## 11. The formal mathematics — ACS / FF06 (Wallace 2026)

Canonical paths: `TR-2026-FF06-ACS/` (see §2 on mirrors). This is the most type-disciplined part of the corpus and the part most likely to be what a mathematical reviewer is reading.

### Asymmetric Codependent System (ACS)
**Kind** object/structure · **Status** active
The central object; every domain result is an instantiation. A pair of smooth fields `(𝓕, 𝓖)` on a manifold M satisfying three axioms. **(ACS-1) codependence**: `𝓕̇ = F(𝓕,𝓖,𝓖̇)` and `𝓖̇ = G(𝓖,𝓕,𝓕̇)`, neither field derivable from the other. **(ACS-2) structural asymmetry**: the coupling operators `f ≢ g` differ in **operator type** — functional form, e.g. polynomial vs absolute value — not merely in parameter values. **(ACS-3) mutual constraint**: the equilibrium set of one field constrains the reachable configurations of the other, so no admissible state is reached by varying one field alone.
- **Type**: `(𝓕,𝓖) ∈ Γ(E₁) × Γ(E₂)` over M, with coupling pair `(f,g)` in a Lie algebra of operators
- **At**: `papers/Form_Function_and_Asymmetry.tex:262-290` (Def 2.2)

### Form field / Function field (INV-3)
**Kind** object/structure · **Status** active
Within an ACS, **Form** carries *structural* information — boundary conditions, equilibrium geometry, the space of admissible states; **Function** carries *dynamic* information — the generator of change between states. The distinction is load-bearing, not labelling: Form constrains what Functions are realisable, Function determines which Forms are stable. Canonical assignments: (vierbein e, connection ω), (primes {p_n}, zeros {γ_k}), (cables, struts), (UV couplings, IR flow).
- **At**: `papers/Form_Function_and_Asymmetry.tex:292-304` (Def 2.3); operational re-definition by surrogate survival at `papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex:59`

### Information Asymmetry ΔI (INV-1)
**Kind** invariant/metric · **Status** active
The declared primitive of the program. The net transfer entropy between the two fields: `ΔI(𝓕→𝓖) = TE(𝓕→𝓖) − TE(𝓖→𝓕)`, with `TE_ℓ(X→Y) = Σ p(y_{t+ℓ},y_t,x_t) log₂ [p(y_{t+ℓ}|y_t,x_t) / p(y_{t+ℓ}|y_t)]`. Sign is the generator: `ΔI > 0` = Form drives Function; `ΔI < 0` = Function drives Form; `ΔI = 0` = the symmetric/Abelian case, an attractor and equilibrium.
- **Type**: `ΔI : Γ(E₁) × Γ(E₂) × ℝ≥0^(ε) → ℝ` (bits), computed w.r.t. the ACS invariant measure μ
- **At**: `papers/Form_Function_and_Asymmetry.tex:306-322` (Def 2.4)

### ACS measure
**Kind** object/structure · **Status** active
The canonical invariant measure μ equipping a deterministic ACS phase flow so that transfer entropy — a stochastic object — is well-defined on it; this closes the stochastic/deterministic bridge. Multi-attractor systems are analysed per ergodic component. Domain instances are pinned: primes carry `μ = Σ_n δ(x − log p_n)` (ergodic by PNT / Vinogradov equidistribution), zeros carry the Montgomery–Odlyzko GUE pair-correlation measure, gauge fields carry the Liouville measure on the constraint surface.
- **Type**: `μ ∈ 𝒫(X×Y)`, Φ_t-invariant
- **At**: `papers/Form_Function_and_Asymmetry.tex:233-258` (Def 2.1)

### Nested Coupling Orders / Emergent Pattern
**Kind** method/principle · **Status** active
Expand `ΔI(ε) = α₁ε + α₂ε² + α₃ε³ + ⋯`. 1st order = direct coupling; 2nd order = the Lie bracket `[f,g]`; 3rd order = the **holonomy term** `[[f,g],f] + [[f,g],g]`. **The emergent pattern is defined precisely as the 3rd-order holonomy** — the component of ΔI irreducible to direct or bracketed coupling. This is the BCH series, valid for `‖ε‖ < r_BCH = π` for matrix Lie algebras. In the Abelian case `[f,g] = 0` all higher α_n vanish, so there is no emergence beyond direct coupling — exactly U(1).
- **Type**: `α_n = 𝔼_μ[β_n(f,g)]`, β_n the n-th BCH generator
- **At**: `papers/Form_Function_and_Asymmetry.tex:324-351` (Def 2.5)

### Layered Resolution Structure — the strict typing rule (INV-4)
**Kind** method/principle · **Status** active
The BCH expansion induces a strict resolution hierarchy: **Layer 0** base Forms `𝓕₀` (states, no dynamics); **Layer 1** Functions `𝓖₁ : 𝓕₀ → 𝓕₀` (torsion `T^a`); **Layer 2** bracket `𝓗₂ : 𝓖₁ × 𝓖₁ → 𝓕₁` (curvature `R^{ab} = [g₁,g₂]`); **Layer 3** holonomy `𝓙₃ : 𝓗₂ × 𝓖₁ → 𝓕₂` (Bianchi `D_{[μ}F_{νρ]} = 0`).

**Strict typing rule**: a Function at layer n acts only on objects from layers < n, and always produces a Form, never a Function. Claimed consequence: self-reference (Gödelian fixed points) is *structurally blocked*, because encoding a Function requires a Form of layer ≥ 1, which layer-1 Functions cannot act on. Verified by cumulative rank growth 2 → 3 → 5 in 𝔰𝔩(4).
- **At**: `papers/Form_Function_and_Asymmetry.tex:353-396` (Remark 2.6)

### BCH–Transfer-Entropy morphism (Link 2, INV-2)
**Kind** theorem/result · **Status** active (T2)
The lemma establishing that the Lie-algebraic BCH expansion and transfer entropy coincide order by order; in particular the Lie bracket **is** the exact second-order Taylor coefficient of ΔI. This is the link that lets an information-theoretic asymmetry generate algebra: applied to the vierbein–connection pair it produces 𝔰𝔩(4), from which the gauge/gravity chain follows. Key identities symbolically verified over generic polynomial fields.
- **Type**: `∂²_ε ΔI |₀ = 𝔼_μ[[f,g]]`
- **At**: `papers/Form_Function_and_Asymmetry.tex:459-466`, exact verification in Appendix `app:exact:2211`

### T1 — ACS generates non-zero information asymmetry
**Kind** theorem/result · **Status** active
For an ACS with `f ≢ g` and ε inside the BCH radius, for generic `(f,g)` (outside a Lebesgue-null set in the C² topology), `ΔI(ε) ≠ 0` for all but finitely many `ε > 0`, with sign set by the dominant BCH order of `[f,g]` at the late-time attractor. The proof splits on `[f,g] = 0` (then `α₁ = 𝔼_μ[f−g] ≠ 0` generically) versus `[f,g] ≠ 0` (then `α₃ = 0` forces the codimension-1 locus `f − g = λ[f,g]` in the centraliser).
- **At**: `papers/Form_Function_and_Asymmetry.tex:413-457`

### Computational tensegrity
**Kind** object/structure · **Status** active
A tensegrity network — nodes, edges split into cables (tension) and struts (compression), energy `H = Σ_cables k V₊ + Σ_struts k V₋` — read as an ACS: Form = cable network (pulls to equilibrium), Function = strut network (maintains separation), coupling = shared node positions, asymmetry = `V₊ ≠ V₋` as structurally different nonlinear potentials, emergent pattern = the equilibrium configuration, which minimises neither cables nor struts alone. **There is no standalone `computational-tensegrity` directory locally** (§2).
- **Type**: `H : (ℝⁿ)^V → ℝ`; rigidity matrix `K = RRᵀ`
- **At**: `papers/Form_Function_and_Asymmetry.tex:898-934` (§5); `papers/core_trilogy/Holographic_Spectral_Inversion.tex:224-260`

### Zero modes are gauge freedoms
**Kind** theorem/result · **Status** active
The zero eigenvalues of the tensegrity rigidity matrix `K = RRᵀ` are zero-energy deformations, and under the ACS correspondence they align with the gauge redundancies of the lattice gauge theory on the same graph — directions in configuration space where `ΔI = 0`. Numerical witness: the icosahedral tensegrity (12 bulk nodes, 6 struts) yields exactly 6 zero modes = `dim SO(3) + dim(translations)`.
- **Type**: `ker K ≅` gauge orbit directions; `dim ker K = 6`
- **At**: `papers/Form_Function_and_Asymmetry.tex:912-923`

### Tensegrity atom
**Kind** object/structure · **Status** active (quarantined to an interpretive appendix in the FF06b build)
The minimal ACS unit in which a compression element (Form) and a tension element (Function) balance, governed by the dimensionless ratio `ρ = αγ/βκ` — stable when `ρ < 1`, unstable when `ρ > 1`. The prime–zero system is written in this form: Form `𝓡(x) = ψ(x) = Σ_{p^k ≤ x} log p` (rigid boundary/instrument), Function `𝓘(x) = −Σ_ρ x^ρ/ρ` (resonant modes), with the coupling equation `𝓡(x) + 𝓘(x) = x − log 2π − ½log(1 − x⁻²)` as the ACS mutual constraint: **Form + Function = total state**.
- **At**: `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:576`, ratio at `:354`

### Spectral function `F_N(x)`
**Kind** operator/map · **Status** active
The explicit-formula oscillatory sum, truncated to the first N zeros and stripped of the √x growth envelope: `F_N(x) = Σ_{k=1}^N A_k φ_k(x)` with `A_k = (¼ + γ_k²)⁻¹` and `φ_k(x) = ½cos(γ_k x) + γ_k sin(γ_k x)`, evaluated at `x = ln p`. The asymmetric weight `A_k ∼ γ_k⁻²` is exact **only at σ = 1/2** — this is the structural asymmetry of the prime–zero ACS.
- **Type**: `F_N : ℝ_{>0} → ℝ`
- **At**: `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:209-226`; reference implementation `zero_variance/src/main.rs:26-38`

### Stationarity measure 𝒮(N,X) and T4′
**Kind** invariant/metric + theorem/result · **Status** T4 proved; **the T4′ converse is conditional** on an unproved minimum-gap bound `δ_N > 0` for all N
`𝒮(N,X) = Var_{x∈[X,2X]}[F_N(x)] / Σ_{k=1}^N |A_k|²`. `F_N` is *uniformly stationary* if `sup_{X>2} 𝒮(N,X) < ∞` for all N. **T4′** asserts the equivalence RH ⟺ `F_N` uniformly stationary ⟺ `lim_{X→∞} 𝒮(N,X) < ∞`, with quantitative failure `𝒮(N,X) ≥ c·X^{2(σ₀−1/2)}` if some zero has `σ₀ > 1/2`.
- **At**: `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:631-641`; forward direction T4 at `:227`

### Zero-variance experiment
**Kind** artifact/format (executable witness) · **Status** active
The Rust experiment measuring the variance-scaling exponent α of `F_N(x)` over x-windows, on-line versus with an injected off-critical perturbation. It is the machine witness for T4/T4′: unperturbed zeros give `α ≈ 0.00126` at `N = 2×10⁶` (statistically flat = stationary), while an injected fake zero at σ produces `α ≈ σ − 1/2` **exactly** (−0.197 at σ = 0.4; +0.199 at σ = 0.6) — the predicted `X^{2(σ₀−1/2)}` blow-up recovered numerically, separation −0.198 at `N = 2×10⁶`.
- **At**: `zero_variance/src/main.rs` (433 lines); results `zero_variance/summary.txt`, `variance_scaling_results.csv`

### Spectral stability ratio ρ_spec
**Kind** invariant/metric · **Status** active
`ρ_spec = max_k [|A_k| X^{|σ_k − 1/2|}] / [δ_N⁻¹ Σ_j |A_j|]`, with X the observation scale and δ_N the minimum zero gap. Under RH (`σ_k ≡ 1/2`) `ρ_spec = 0` ⇒ stable ⇒ `F_N` stationary; an off-critical zero sends `ρ_spec → ∞` as `X → ∞` ⇒ unstable ⇒ non-stationary. Explicitly the spectral analogue of the tensegrity-atom ratio: both systems stable iff `ρ < 1`.
- **At**: `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:337-356`

### Renormalised stability
**Kind** theorem/result · **Status** active — stated by the authors as a *reframing*, not a new theorem
With `u = log x` and `Δ_norm(u) = (ψ(e^u) − e^u)/e^{u/2} ∼ −Σ_ρ e^{(ρ−1/2)u}/ρ`: under RH each exponent is purely imaginary, so `Δ_norm` is bounded; conversely a zero with `Re ρ₀ > 1/2` makes it unbounded. This recasts RH as "the prime–zero ACS sits exactly at the boundary between bounded oscillation and exponential divergence" — a **phase boundary** in ACS stability language.
- **At**: `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:405-450`

### Resolvent susceptibility χ(ω)
**Kind** operator/map · **Status** active
Rephrasing of the explicit formula as a linear-response object: `χ(ω) = Σ_ρ 1/(ω − γ_ρ) = Tr[(ωI − H)⁻¹]` for any operator H with spectrum `{γ_k}`. Meromorphic with simple unit-residue poles. It recasts the prime–zero correspondence as linear response — primes = discrete sources, zeros = resonant poles — so the Hilbert–Pólya problem becomes "construct a *natural* self-adjoint H without inputting the γ_k."
- **At**: `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:372-404`

### Wronskian–Lie identification, and the Wronskian-is-not-Poisson obstruction
**Kind** theorem/result · **Status** the identification is active; **the Poisson reading is legacy/falsified** (claim #23 in the master ledger)
On `𝒞¹((0,∞))` the operation `[f,g](x) = f'(x)g(x) − g'(x)f(x)` is a genuine Lie bracket (bilinear, antisymmetric, Jacobi verified by direct expansion). The **retained negative result**: it fails the Leibniz rule `{fg,h} = f{g,h} + g{f,h}` by the exact computable correction `−fgh'`, hence it is *not* a Poisson bracket — so Hamiltonian readings of the Wronskian-as-bracket do not transfer.
- **At**: `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:283-336`; code `src/paper_b/wronskian_leibniz.py`

### Holographic Resolution (HR-1 / HR-2 / HR-3)
**Kind** method/principle · **Status** active
A system S solving a constraint C by reducing ΔI achieves *holographic resolution* if **HR-1** S encodes the full information content of C on its own boundary ∂S; **HR-2** the interior of C is accessible from outside via ∂S without passing through C's interface; **HR-3** the encoding is faithful — no information in C is inaccessible via ∂S. Presented as structurally analogous to Ryu–Takayanagi; the analogy is stated as structural, not derived.
- **At**: `papers/Form_Function_and_Asymmetry.tex:943-957`

### Self-Resolving Structure
**Kind** object/structure · **Status** active
A structure S is *self-resolving* if it carries an intrinsic measure `μ(t)` such that whenever S begins to invert its information asymmetry (`ΔI → −ΔI`), `μ(t)` becomes nonzero and is legible **within S's own record**, not merely detectable by an external observer. Prototype: the Bianchi identity — any deviation from gauge-covariant curvature is encoded in the field equations themselves.
- **At**: `papers/Form_Function_and_Asymmetry.tex:959-974`

### Inversion Arc — "the key becomes the lock" (INV-5)
**Kind** theorem/result · **Status** active (proof given as sketch; the RG instances are the hard anchor)
Let S solve constraint C₀ with `ΔI > 0` (Form drives Function: open, outward-flowing). As S becomes the dominant access structure, new actors enter only through S; at that point `S = C₁` is the new constraint and the sign flips: `ΔI(S as solution) > 0 ⟶ ΔI(S as constraint) < 0`. The flip follows from the Form/Function role reversal as S's dominance rises; inversion rate `τ⁻¹` scales with adoption rate. Anchored by two **proved** instances: the Zamolodchikov c-theorem (2D) and the Komargodski–Schwimmer a-theorem (4D).
- **At**: `papers/Form_Function_and_Asymmetry.tex:978-1026` (+ instance table)

### Constraint–Attractor Cycle
**Kind** method/principle · **Status** active
The dynamical reading of the inversion arc: the Palatini field equations drive the system to `T^a = 0` (torsion-free), which is simultaneously the *attractor* of the ACS flow and the *constraint* on subsequent evolution. Breaking it runs the cycle `T^a = 0 → T^a ≠ 0 (torsion activates) → chiral modes → spinor bundle → 𝔰𝔲(3) (complexify) → confinement → new constraint`. At each stage `[f,g]` measures the asymmetry driving the transition: zero at the attractor, non-zero while being driven to the next. The quantum version: Wheeler–DeWitt `Ĥ|Ψ⟩ = 0` is the quantum attractor where `ΔI_Q = 0`, and breaking it (ℏ corrections) yields the arrow of time.
- **At**: `papers/Form_Function_and_Asymmetry.tex:1028-1069`

### Closure Attractor / closure defect functional 𝒟(V)
**Kind** invariant/metric + theorem/result · **Status** active (T3 — a 50k-sample numerical result, **explicitly not a uniqueness theorem**)
For a k-dimensional subspace `V ⊂ 𝔰𝔩(4,ℝ)` with basis `{T_i}` and orthogonal projector `Π_V`: `𝒟(V) = Σ_{i<j} ‖[T_i,T_j] − Π_V([T_i,T_j])‖ / Σ_{i<j} ‖[T_i,T_j]‖`. Result: `𝒟(𝔰𝔩(3,ℝ)) = 0` exactly, while 100 random 8-dimensional subspaces all give `𝒟 > 0.54` and none reach 0.1; stable under perturbation (`𝒟 < 0.03` for `ε ≤ 0.01`). Hence 𝔰𝔲(3) is the **unique 8-dimensional closure attractor of the Palatini bracket** — "colour from gravity."
- **Type**: `𝒟 : Gr(k, 𝔰𝔩(4,ℝ)) → [0,1]`
- **At**: `papers/Form_Function_and_Asymmetry.tex:1516-1556`; tier at `Math-grav-shared/MANIFEST.md`

### Killing-orthogonality and algebraic non-traversability
**Kind** theorem/result · **Status** active (T2)
*Killing-orthogonality*: for any matrix Lie algebra and any X, Y, `tr([X,Y]X) = 0` and `tr([X,Y]Y) = 0` — the bracket output is trace-orthogonal to both inputs. *Algebraic non-traversability* (corollary): with `π_X(M) = [tr(MX)/tr(X²)]X`, the bracket output `B = [X,Y]` satisfies `π_X(B) = 0` identically, so no information from B traverses back to X by scalar inner-product reconstruction. Offered as the ACS rereading of ER = EPR: non-traversability derived from bracket algebra alone, **no bulk geometry invoked**. Verified at `|c| < 10⁻¹⁶` in 𝔰𝔩(4,ℝ). Note the consistency with the Layered Resolution Structure: a bracket output is a Form, opaque to its inputs.
- **At**: `papers/core_trilogy/Holographic_Spectral_Inversion.tex:467-480, 650-685`

### Three-class spectral taxonomy — elliptic / hyperbolic / parabolic
**Kind** theorem/result · **Status** active (T2); corrected from an earlier four-class version
Any finite-dimensional real linear ACS operator X admits a Jordan–Chevalley decomposition `X = X_s + X_n`; the semisimple part partitions adjoint flows into **elliptic** (imaginary eigenvalues; rotational/periodic), **hyperbolic** (real eigenvalues; exponential, *no 2π loop closure*), **parabolic** (`X_s = 0, X_n ≠ 0`; polynomial). Its job is an **obstruction**: it kills the earlier "universal 2π inversion at three steps" reading of `ad³ = (16/9)ad` in 𝔰𝔩(4,ℝ) — that is Cayley–Hamilton saturation in a *hyperbolic* algebra (`spec(ad_{T_{B−L}}) = {0, ±4/3}`), not rotational closure.
- **At**: `papers/core_trilogy/Holographic_Spectral_Inversion.tex:547-600`

### Shuffle knife (K1) — the form/function discriminant
**Kind** operator/map (methodological instrument) · **Status** active
The operator deciding whether a spectral witness reads the *universality class* or the *object*: replace the object by a **marginal-matched surrogate** (its own unfolded spacing distribution, re-randomised so object-specific correlations are destroyed but the distribution class is preserved) and ask whether each witness's value survives. Survives ⇒ **form**; collapses ⇒ **function**, with the collapse size in surrogate-σ units measuring true object-specific influence. On the first 10⁵ Riemann zeros with 60 surrogate seeds: arithmetic prime-resonance ≈11,497σ and lag-1 correlation ≈97σ = FUNCTION; spacing, counting, Wigner-shape 0.4–1.0σ = FORM. The function signal *amplifies* with N (3030σ at 2×10⁴ → 11,497σ at 10⁵).
- **Type**: witness verdict `z = |W_real − W̄_shuf| / σ_shuf`
- **At**: `papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex:53-68`; implementation `Math-grav-shared/scripts/knife_2x2.py`

### Five-instrument suite and the two-knife taxonomy
**Kind** protocol · **Status** active
A grid of destructions and reflections, each isolating one property. **K1** destroys *ordering* (marginal-matched permutation). **K2** the class knife destroys *arithmetic* (null = GUE draws via Dumitriu–Edelman β=2: carries rigidity, lacks primes). **R** coherent refinement destroys nothing and enlarges the window (N: 12.5k → 100k) — objective signals sharpen, artifacts evaporate. **M** the mirror test compares ψ from primes to ψ from axis-placed zeros. **O** the octave test fits a per-tone Gabor envelope slope `β_j`, where `β_j = 0` ⟺ tone j grows at `x^{1/2}` (the on-line prediction). The **two-knife taxonomy** is the K1×K2 verdict grid; the silent-K1/fires-K2 cell was relabelled **ARITHMETIC FINITE-HEIGHT DEVIATION** (a Bogomolny–Keating signature) after a matched-height CUE control closed only 44% of the variance gap.
- **At**: `Math-grav-shared/docs/graviton_note_five_instruments_20260702.md`; scripts `Math-grav-shared/scripts/`

### Transport obstruction — the three-number diagnostic
**Kind** invariant/metric · **Status** active (T2)
Build a transport holonomy `D = U₁U₂⁻¹` from two refinement-path orderings of a connection with genuine curvature, then diagnose with three numbers: `‖D − I‖` (path-dependent?), `‖D − (Tr D/n)I‖` (scalar/central?), `mean ‖[D,H]‖` over Hermitian probes (commuting?). Verdict: abelian arm ⇒ the obstruction is a *scalar*; non-abelian arm ⇒ a *conjugacy class*. Forced result: over 2000 random Palatini connections the curvature `[e,ω]` has central component `8.88×10⁻¹⁶` (machine zero), because 𝔰𝔩(4) is simple and `[e,ω]` traceless — a scalar holonomy is **algebraically impossible**, so the obstruction is necessarily a conjugacy class.
- **At**: `papers/core_trilogy/Spectral_Witness_Refinement.tex:187-256`

### Prime-Gap Transition Operator P_m and the Kernel Law
**Kind** operator/map + theorem/result · **Status** active
On the transition state space `𝒮_m = {(a,b) : a,b ∈ U_m}`, `U_m = (ℤ/mℤ)^*`, build the empirical column-stochastic second-order transition operator `T_m` subject to residue continuity `b = a'`, with unbiased reference `T₀ = 1/φ(m)` and perturbation `P_m = T_m − T₀`. **Kernel Law** (empirical, T1/T3): `dim ker(P_m) = φ(m)` for all tested moduli, and `ker(P_m)` **is** the *source sector* `{f(a,b) = g(a)}` — Dirichlet characters are a canonical basis but the sector is the structural object. Kernel = Form sector; perturbation carries the Function content. **Fresh-eyes caveat recorded in the paper**: the eigenvalues are bounded dynamical modes (`|λ| ≈ 0.01–0.3`), *not* the Riemann zeros.
- **Type**: `P_m : ℂ^{𝒮_m} → ℂ^{𝒮_m}`, `|𝒮_m| = φ(m)²`
- **At**: `papers/notes/Prime_Gap_Transition_Operator.tex:53-110`

### Grading selection functional
**Kind** invariant/metric + theorem/result · **Status** active (T2)
For a distinguished generator T and a symmetric involution `P = diag(ε_i)`, define `S̃_g[P] = Tr(σ_P · g(ad_T))` with g applied spectrally. The theorem: the metric signature / Clifford grading minimising adjoint spectral activity is selected by a binary index-partition, reducing to **max-cut on a complete bipartite graph**; universality holds across six functionals, with frame invariance under O(4). Two routes are **retained as closed negatives**: signature selection from the Killing form (Route A) and from stability (Route C). A G₂ counterexample bounds it — cluster coherence fails for multi-length root clusters.
- **At**: `papers/notes/Adjoint_Clifford_Signature_Selection.tex:114, 226`

### Shape (relational representation of an integer)
**Kind** object/structure · **Status** active
A *shape* encodes a positive integer's multiplicative structure as a finite map `{p_i : e_i}` from prime "sides" to positive exponents, with volume `Π p_i^{e_i}`. Multiplicative questions become geometric: multiply = merge, divisibility = containment, gcd/lcm = common/enclosing box, primality = atomic box. The reference engine is 91 lines; all twelve operations verified exact against integer ground truth. The single boundary is addition, handled by an explicit flagged exit to value-space.
- **Type**: `ρ : ℤ_{>0} → ⊕_p ℕ` (an isomorphism onto its image for ×)
- **At**: `papers/later_FF06_series/When_a_Number_Lies.tex:71-82`

### Reversible flattening, the homomorphism criterion, and the seam
**Kind** method/principle + theorem/result · **Status** active
A *flattening* `π : R → s` to a scalar/symbol string is **reversible** if there is a relational representation `ρ(R)` and an exact recovery such that operations of interest are computed on `ρ(R)` without ever forming s. **Criterion**: the flattening of ⋆ is reversible exactly when ⋆ is a homomorphism `(objects, ⋆) → (stored structure, ⊕)`, i.e. `ρ(a ⋆ b) = ρ(a) ⊕ ρ(b)`. Multiplication passes (FTA: `(ℤ_{>0},×) ≅ (⊕_p ℕ, +)`); addition fails — and this non-homomorphic boundary is **the seam**.

Keystone theorem: *the seam is convolution* — Euler's `Σ_n p(n)x^n = Π_k (1−x^k)⁻¹` crosses it, and convolution is additive in the index and multiplicative in the value. Corollary, "density, not identity": convolution yields *how many*, never *which one* — which is why the explicit formula gives a statistical prime/zero relation and never an address.
- **At**: `papers/later_FF06_series/The_Reversible_Flattening.tex:79-101, 169-199`

### Boundary law; scalar abstraction is impossible under cycles
**Kind** theorem/result · **Status** active (stated as an empirical-structural characterization, not a proof-theoretic theorem)
*Boundary law*: relational representation strictly improves on scalar abstraction iff (i) an exact underlying relation exists, (ii) it is a product, ratio, or non-transitive graph rather than a sum, and (iii) the scalar projection breaks (overflow, underflow, catastrophic cancellation, or nonexistence) or the question is exact and the scalar destroys needed structure. *Impossibility instance*: if the pairwise majority relation contains a cycle `A ≻ B ≻ C ≻ A`, every total order contradicts at least one majority verdict (exhaustive check: minimum contradicted edges is one, not zero) — the same transitivity obstruction that forbids encoding rock-paper-scissors as box containment. Measured cycle rates ≈7%, 43%, 78%, 99% for 3, 5, 7, 10 candidates, persisting at 1001 voters.
- **At**: `papers/later_FF06_series/When_a_Number_Lies.tex:144-181`

### Invariant vs refraction classification
**Kind** method/principle · **Status** active (all verdicts T1)
Turning the program's own instrument inward: recompute each "algebraically locked" framework constant under a legitimate change of representation or counting convention. A quantity that moves is a **refraction** (an artifact of instrument or normalisation); one that survives is an **invariant**. Verdicts: `g₄ = 4/3 → 2/3` under `Tr(T^aT^b) = ½δ` vs `δ` = refraction (though the *equality* `g₄ = g_L = g_R` is invariant); Barbero–Immirzi `γ = 0.274067 → 0.190206` under SU(2)→SO(3) counting = refraction; `λ_φ = 2√3/27` scales with Killing-form norm = refraction; Yukawa ratio `h̃/h = 2/3` = **invariant** (normalisation cancels; RG-protected). Pattern: **the relations survive, the bare numbers do not.**
- **At**: `papers/later_FF06_series/The_Elimination_Ledger.tex:121-175`

### Elimination Ledger
**Kind** artifact/format · **Status** active
The standing register of explicitly falsified claims, retained as boundary results rather than deleted. Contents include: `ad³ = 2·ad` for integer matrices (impossible: requires `λ = 1/√2`); universal 2π inversion at three steps (𝔰𝔩(4) is hyperbolic); Wronskian as Poisson bracket (Leibniz fails by `−fgh'`); IR ⟨2,3⟩ lattice imprint (z-scores null vs PDG); intrinsic algebra chirality; signature selection from the Killing form (Route A) and from stability (Route C); the Coleman–Weinberg 6→5 input reduction (fermion-dominated, boundary minimum, tanβ gauge-protected); the height-floor scaling law `T_min = (2πe)^d/q` (correct floor `2πe·q^{−1/d}`).
- **At**: `papers/later_FF06_series/The_Elimination_Ledger.tex`; `docs/Elimination_Ledger.md`; `Math-grav-shared/MANIFEST.md`

### Mode collapse law
**Kind** theorem/result · **Status** active
For N coupled Duffing nodes on a symmetric graph Laplacian, `ẍ + γẋ + kx + Lx + βx^{∘3} = F(t)`, in the eigenbasis `Lφ_j = λ_jφ_j`, `ω_j = √(k+λ_j)`: multiple-scale analysis gives the nonlinear frequency shift `Δω_nl = (3βΓ_m/8ω_m)a_m²` with **eigenvector fourth moment** `Γ_m = Σ_i φ_m(i)⁴`. Collapse occurs when `Δω_nl ≈ Δω_m` (nearest spectral gap), giving the universal law

> **β_c a_m² = (8ω_m)/(3Γ_m) · Δω_m**

Mechanism: parametric instability from four-wave mixing between the driven mode and its nearest spectral neighbour — self-detuning against the spectral gap. Verified within 6% across ring, Erdős–Rényi, Barabási–Albert, and grid graphs.
- **At**: `claude-archive/archive/projects/unified-field-theory/knowledge/unified-stability-epistemic-limits-nonlinear-mode.md:323-361`, derivation `:443-479`

### Phase boundary primitive
**Kind** method/principle · **Status** active
The unifying claim: stability certification, perturbation budget, epistemic detectability, load redistribution, and mode collapse are all governed by the *same* primitive — two scalings compete under a control parameter, and their crossing marks a qualitative change. Per layer: RC6 = eigenvalue vs quadratic root; RC7 = perturbation magnitude vs stability margin; RC8 = Lyapunov divergence vs geometric sampling density; load redistribution = convex cost vs amplitude concentration; mode collapse = nonlinear frequency shift vs spectral gap. Stated framing: "This is not mysticism but eigenvalue geometry under perturbation."
- **At**: `…/unified-stability-epistemic-limits-nonlinear-mode.md:59-77, 386-408`

### Epistemic horizon (RC8)
**Kind** theorem/result · **Status** active
A **detectability limit, not a physical instability**: determinism is inferable from finite noisy data only when `σ < C·A·λ^α·N^{−β/D₂}` with structural exponents `α = ½`, `β = 1` (N sample size, λ largest Lyapunov exponent, D₂ correlation dimension, A amplitude scale, σ observational noise). Derived by balancing deterministic divergence `δ₀e^{λt}` against noise diffusion `σ√t` at Lyapunov time, with geometric resolution `δ₀ ∼ AN^{−1/D₂}`. Empirical calibration `α ≈ 0.46`, `β ≈ 1.07`. Companions: **RC6** spectral certification (margin `B = min_k dist(λ_k, roots of Q)`, certified iff `B > 0`) and **RC7** perturbation budget (`ε < B` ⇒ still certified without recomputing eigenvalues, by Weyl).
- **At**: `…/unified-stability-epistemic-limits-nonlinear-mode.md:141-169, 98-121, 122-139`

### Participation ratio collapse diagnostic
**Kind** invariant/metric · **Status** active
Threshold-free detector of modal collapse: `PR(t) = (Σ_k q_k²)² / Σ_k q_k⁴` over modal energies. `PR = 1` for a pure single mode, dropping toward `1/N` as energy spreads. Used in place of arbitrary thresholds.
- **At**: `…/unified-stability-epistemic-limits-nonlinear-mode.md:363-374`

### Load redistribution theorem
**Kind** theorem/result · **Status** active
With convex cost `S_p(x) = (1/N)Σ_i|x_i|^p` (p > 2) and modal equalization efficiency `η_m² = (1/N)(Σ_i|φ_m(i)|)²` (= 1 iff the mode is flat), the AC (modal) response is bounded away from the DC (localized) response: `[S_p(x^DC) − S_p(x^AC)]/S_p(x^DC) ≥ (1 − N^{1−p/2})·η_global^{p/2}`. In words: **convex cost reduction under modal forcing is bounded by a spectral average of eigenvector flatness.**
- **At**: `…/unified-stability-epistemic-limits-nonlinear-mode.md:275-321`

### Trust holonomy
**Kind** theorem/result · **Status** active (T2/T3 in-model; the mapping to the shipped ring layer is T3)
The variational problem for path-dependent trust, on the free step-3 nilpotent group on 2 generators (Hall basis `{X, Y, Z=[X,Y], U=[X,Z], V=[Y,Z]}`, BCH exact at step 3; interactions = unit horizontal steps). **Line-null**: any constant-direction path has `log g = L·W` exactly, commutator components stay 0 — "no amount of repeated same-type interaction purchases commutator-class trust." **Reachability**: by Chow–Rashevskii, `{X,Y}` bracket-generate, so every trust state is reachable. **Semicircle optimum**: with free endpoint, `Z_max = L²/2π`, achieved by the semicircular maneuver — twice the closed-loop isoperimetric bound `1/4π`. Doctrine line: *form is bought on straight paths; function is bought only with curvature.* Two pre-registered predictions were overturned and struck with provenance.
- **At**: `Math-grav-shared/docs/NOTE_trust_holonomy_variational_20260703.md`; script `scripts/trust_holonomy.py`

### ACS Deterministic AI Stack and the Coherence Obstruction Tensor
**Kind** subsystem · **Status** the formalism is active; the engineering realisation is **aspirational** (phased plan, Phase 0 → Phase 3)
The system is specified as `(𝒜, 𝒮, {ℛ_α}_{α∈𝒮}, Φ)`: a state space 𝒜 of O(4)-valued matrix fields on a finite grid (**no continuum manifold assumed**); a **rewrite semigroup** of scheme-indexed nonlinear endomorphisms that explicitly do *not* compose coherently (`ℛ_α ∘ ℛ_β ≠ ℛ_{αβ}` — not a category or groupoid); and a deliberately lossy **observation functor** `Φ : 𝒜 → ℝ^m`. The **Coherence Obstruction Tensor** is `[ℛ_α, ℛ_β](A)`, pushed forward to the **scheme dispersion metric** `Δ_scheme(A) = Var_{α∈𝒮}[Φ(ℛ_α^k(A))]` — which measures non-commutativity of *measurement orderings*, not geometric curvature.
- **At**: `papers/discrete_geometry_formalism.tex:24-83`; PDR `papers/ACS_Deterministic_AI_Stack_PDR.tex:325, 384, 458, 526, 623, 688`

### Orbit Sheaf and de-sublimation of geometry
**Kind** object/structure · **Status** active
Because the rewrite system lacks global functoriality, invariants do not exist as intrinsic geometric objects; the primitive output is instead the ensemble of *all* measurement histories under the finite atlas of rewrite rules, `Spec_𝒮(A) = {Φ(ℛ_{α_k} ∘ ⋯ ∘ ℛ_{α_1}(A))}`. All physics-like quantities are recast as secondary statistics on this ensemble — **de-sublimation**: curvature = measurable commutator defect of local update operators after projection; RG flow = drift of the induced measure on Φ-space under iterated composition; fixed points = ordinary attractors of the observable dynamics; holonomy = loop compositions in the action semigroup at discrete vertices. Open frontier: the minimal generating scheme set `𝒮_min`, and sufficiency of Φ for classifying rewrite-history equivalence classes.
- **Type**: `Spec_𝒮 : 𝒜 → 𝒫(ℝ^m)`
- **At**: `papers/discrete_geometry_formalism.tex:52-66`

### One Mechanism, Many Forms — the identity chain
**Kind** method/principle · **Status** Links 1–2 active; **Link 3 aspirational/conjectural**
The corpus's meta-claim, stated ontologically rather than epistemically: the form/function asymmetry is *one mechanism expressed in many substrates*, not a family of analogues. What makes that more than a slogan is a three-link identity chain. **Link 1** (definitional): ΔI is the transfer-entropy asymmetry. **Link 2** (proven, T2): the Lie bracket is the exact second-order Taylor coefficient of ΔI. **Link 3** (the load-bearing *open* identification): ΔI *is* the RG c-function (Zamolodchikov) / a-function (Komargodski–Schwimmer), with form = UV couplings, function = IR couplings, β-function = the coupling, c-theorem = monotonicity of ΔI.

The papers state the stakes explicitly: **if Link 3 fails, cross-domain sameness collapses from identity back to analogy.**
- **At**: `papers/later_FF06_series/One_Mechanism_Many_Forms_Sigma.tex:81-135`

### WQRF — Wallace Quantum Resonance Framework
**Kind** method/principle · **Status** **legacy** — a separate, earlier line
An earlier research line under `research_papers`: a claimed 5D topological model with the **Wallace Transform** `W_φ(x) = α log^φ(x+ε) + β` and claims of `O(n²) → O(n^{1.44})` complexity reduction and golden-ratio correlations across 23+ disciplines. It shares an author with the FF06/ACS line but **none of its definitions, tiering discipline, or objects**; it is not cited by the formal papers, and the FF06 corpus's own Elimination-Ledger discipline is in explicit tension with its claim style. Listed here only as the historical antecedent — and because the degenerate `prime_banding` artifacts (§10) are generated by it.
- **At**: `research_papers/WQRF_BIBLIOGRAPHY.md:1-30`

---

