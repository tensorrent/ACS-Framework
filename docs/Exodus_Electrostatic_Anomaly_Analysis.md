> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Does ACS Explain the Exodus Electrostatic Anomaly?

**Verdict: NO — the proposed bridge is KILLED on three independent structural grounds.**
**Date:** 2026-08-12 · **Tier:** T2 structural (K1–K3) / external experimental evidence (§4)

---

## 0. Scope — what is being tested here

The object under test is **our own conjecture**, not Charles Buhler's experiment.

The conjecture, as posed: *the third-order asymmetry Buhler reports in his QED
treatment of two static charges is the same structure as the ACS third-order
holonomy, and the ACS framework therefore supplies the mechanism for the force he
measures.*

This document kills that conjecture. It does **not** adjudicate whether Buhler's
measured force is real — that is an experimental question belonging to
experimentalists, and §4 reports the external state of evidence only because it
bears on whether there is an explanandum at all. Buhler's own epistemic conduct is
notably careful and is recorded fairly in §5.

Per the ledger's strip-mine discipline, this is a kill aimed at one of **our own**
proposed applications. That is the only reason it belongs in this repository.

---

## 1. The conjecture, and why it looked promising

Two independent structural facts motivated it.

**Ours** (`Palatini_Gauge_Attractor.tex`, `def:nested`): expanding the information
asymmetry ΔI(ε) = α₁ε + α₂ε² + α₃ε³ + …,

- 1st order — direct coupling
- 2nd order — the Lie bracket [f,g]
- 3rd order — the **holonomy** [[f,g],f] + [[f,g],g], *"the residue of the closed
  loop Form → Function → Form that cannot be decomposed into lower-order
  contributions"*

with the framework's definition: *"The **emergent pattern** is defined precisely as
the 3rd-order holonomy."*

**His** (APEC 2025-08-02, *"Exodus and the Third Order"*; Michels interview
2026-03-30): second-order time-independent perturbation theory on two static charges
reproduces Coulomb's law; going to third order yields, in his words,

> *"I was seeing three charges now. So basically, one of the charges was weighed
> twice, multiplied by itself, and then the third order is being multiplied by the
> first charge. **So there's already an asymmetry in the charges. Even with two
> charges.**"*

Schematically the ACS holonomy expands as f²g + fg²; his third-order terms are
Q₁²Q₂ + Q₁Q₂². Two programmes independently locating the novel content at third
order, in a triple product with a built-in asymmetry, is a genuine prima facie
match — and worth the cost of a kill test.

---

## 2. Kill conditions, stated before the evidence was gathered

The conjecture survives only if **all three** hold:

- **K1** — Buhler's "asymmetry" is asymmetry in the ACS sense, i.e. non-commutativity of coupling operators (ACS-2: f ≢ g *as operator types*).
- **K2** — ΔI is defined on the physical system he is modelling.
- **K3** — ACS contains content connecting an information asymmetry to a **net linear force**.

Any single failure kills the bridge. All three failed.

---

## 3. The three kills

### K1 — FAILED. The two "asymmetries" are different objects sharing a word.

Buhler's own statement of the asymmetry (APEC 2025, 00:37:23):

> *"it's a function of Q₁Q₂² or Q₁²Q₂. **So already it's asymmetric just by the
> order.** … If you have two identical particles in the identical field, those
> asymmetries will all cancel. You'll get nothing."*

Q₁ and Q₂ are ordinary charges — commuting c-numbers, [Q₁, Q₂] = 0. His asymmetry
is a **polynomial-degree asymmetry among commuting scalars**.

ACS-2 requires the coupling operators to differ **as operator types** (the corpus's
own worked example is polynomial vs absolute value, `integer_acs.py`). Where the
coupling operators commute:

```
α₂ = ⟨[f,g], ∇log dμ/dν⟩ = 0
α₃ = [[f,g],f] + [[f,g],g] = 0
```

Every ACS term above first order vanishes **identically** on a system of commuting
charges. The formal resemblance f²g + fg² ↔ Q₁²Q₂ + Q₁Q₂² is therefore a shape
match with no shared content. This is the corpus's named **false-fit** failure mode
(Process Record §1): a structural resemblance mistaken for an operational identity.

### K2 — FAILED. ΔI is undefined on the system he models.

Buhler is explicit and repeats it unprompted (Michels clip 00:05:56, 00:08:52):

> *"the QED doing Coulomb's law is a second-order equation, **using time-independent
> perturbation theory**."*

His perturbing operator is **H′ = A_μ J^μ** with **J^μ = (ρ, 0, 0, 0)** for two
static point charges — the spatial current components are zero. He treats this as
the essential feature, having concluded in 2018 that no current is needed:
*"I'm in pure electrostatics mode."*

ΔI = TE(F→G) − TE(G→F) is transfer entropy. This repository's own Q4 kill
(2026-06-06, T1+T2, the highest-collapse target retired) established:

> *"transfer entropy is **undefined on a static, time-translation-invariant ground
> state** and vanishes by symmetry on a symmetric bipartition."*

So ΔI is not small on his object — it is **undefined**, and there is nothing for the
BCH expansion to expand. Invoking ACS here would repeat exactly the category error
that killed ΔI ≡ c-function: a temporal, directed quantity applied to a static,
spatial one.

**A real distinction survives this kill, and it is the useful residue.** Buhler's
*apparatus* is not static. Aurigema's vacuum run shows steady-state leakage of
**0.1–0.2 µA** throughout the thrust measurement (with ~17 µA transients at each
voltage step). That is a driven dissipative non-equilibrium steady state, which does
carry a time series and on which ΔI *is* defined. **His theory models a static
configuration; his apparatus is a current-carrying one.** See §6.

### K3 — FAILED. ACS has no linear-momentum content.

A full-corpus search (`papers/**`, `docs/**`, `.tex` and `.md`) for *momentum
conservation*, *net momentum*, *thrust*, *propulsion*, *reactionless* returns
**zero hits**. Searching the bare word *momentum* returns exactly two kinds of
occurrence: **angular** momentum in the g-factor work
(`Framing_Transformer_Spin_Parity.tex` §6), and the rhetorical nesting chain
*"vibrations → momentum → colour → confinement → mass → gravity"* in three
concluding summaries. Neither is a treatment of momentum conservation.

Momentum conservation — what absorbs the recoil — is the entire crux of a thruster
claim. ACS has never addressed it. Any bridge would have to be **built from
nothing**, not found.

### The nearest genuine connection, and why it does not reach

The framed-unknot no-go (2026-07-26, T2) proves that for **any** closed curve with
charge and mass circulating at uniform q/m, μ/⟨L⟩ = q/2m exactly — the vector area
cancels and g = 1 regardless of winding, framing, twist or throat. The ledger records
what that opens: **decouple where the charge sits from where the mass sits.**

Buhler's device does physically satisfy that condition — charge resides on the
conductive surfaces, mass in the potting epoxy and dielectric. But our no-go is a
statement about a **magnetic moment over an angular momentum**. His claim is a **net
linear thrust**. No derivation connects them, and by K3 the corpus contains nothing
that could supply one. The connection is real at the level of the *question* and
absent at the level of the *mechanism*.

Likewise the 720°/360° winding asymmetry (longitude 4π contributing +1 and nothing;
meridian 2π landing on −1 and carrying the entire spinorial character) has no
counterpart in a DC electrostatic device with no rotation and no second timescale.
And p + q = 3 is a **parity** input — σ = (−1)^{p+q}, one bit; a (4,1) curve gives
the identical σ. Reading magnitude into that 3 would recommit precisely the error
the Sl = 2 ↔ g = 2 kill was logged for.

---

## 4. External state of the evidence (reported, not adjudicated)

Included because it bears on whether an explanandum exists.

**Tajmar, Kößling & Neunzig, *"In-Depth Search for a Coupling between Gravity and
Electromagnetism with Steady Fields"*, TU Dresden (arXiv:2402.15640).** Verified
against the primary PDF. Tested, among others:

| Configuration | Paper's description |
|---|---|
| Asymmetric capacitor | *"a copper disc for the electrode at one side and the tip of our connection wire with 0.64 mm diameter (AWG22) on the other"* |
| Dielectric gradient ∥ E | *"two different (low and high) permittivity inserts in the direction of the electric field"* |
| Dielectric gradient ⊥ E | trapezoidal-shaped dielectric |

Conditions: epoxy-potted articles, fully shielded and remotely controlled,
**10⁻⁷ mbar**, attocube IDS3010 laser interferometer readout, **voice-coil in-situ
calibration** against a known force, up to 40 kV.

Stated result:

> *"All types of capacitors tested (low/high-k core dielectric, dielectric gradient,
> symmetric/asymmetric) did not show any weight change nor did they produce any
> anomalous force along their electric field or perpendicular to their electric
> field."*

Representative row (Table 1): Y5T, εᵣ = 6000, ⌀40 mm × 20 mm, **30 kV → −9.5 ± 13.5 nN**.

Buhler's claim is **~10 mN at 30–40 kV**, i.e. **≈7.4 × 10⁵ ×** Tajmar's uncertainty.

**What this does and does not establish.** Tajmar did not test Buhler's specific
article — Buhler's asymmetry is engineered pressure × area over shaped blade arrays
with Faraday-shielded recessed surfaces, not a disc against a wire tip. That is a
legitimate distinction. But Tajmar *did* test the four parameters Buhler's own patent
(US 11,511,891 B2) names as governing — voltage, permittivity, dielectric gradient,
electrode asymmetry — and found null at the nanonewton scale. Buhler's own best
geometry optimisation claims **~6×** (triangular ground features, optimum ~23). Six
orders of magnitude cannot be recovered from a 6× geometry factor. For the claim to
stand, the effect must depend on essentially none of the parameters his patent
identifies, and the blade geometry alone must supply ~10⁶.

**Leading artifact candidate: electrostatic coupling to the chamber.** For a device
of ~25 pF self-capacitance at 40 kV, q = CV = 1 µC; at 0.5 m from a grounded wall,
F = q²/4πε₀(2d)² ≈ **9 mN** — the right order of magnitude, DC, non-decaying,
pressure-independent. In Buhler's favour, his grounded ITO Faraday enclosure with
force measured *on the enclosure* is aimed squarely at this artifact. It is the
leading candidate, not a demonstrated one.

**An internal contradiction in his own record.** Buhler states the force persists
after power removal (*"it would accelerate. With the power off."*); Aurigema's own
vacuum data shows thrust tracking voltage down and returning to ~0 within the ~300 s
capacitor drain, with any residual attributed to **charge injection into the
plastic** — i.e. an electret. Resolving that single measurement discriminates
"new force" from "charge-state-dependent electrostatic effect."

---

## 5. Concessions — recorded because the ledger keeps them

- **The ion-wind objection fails here.** At 10⁻⁶ torr the mean free path is ~50 m, and a collisionless ion rocket delivering 10 mN at 30 kV would require ~76 mA and kilowatts against his claimed microamps. Critics leading with ion wind are attacking the wrong mechanism.
- **Buhler's epistemic conduct is careful.** He declines the antigravity framing (*"It's pretentious to say that we're messing with gravity… I don't think I'm bending space-time with my 2,000 volts and plates and wires"*), states his own theory tentatively (*"my math may not be perfect, I'm sure"*), acknowledges the energy-conservation problem rather than hiding it, solicits skeptics, and distinguishes witnesses who have *seen* the effect from those who have *reproduced* it. This is not a fraud profile.
- **The experimental programme is unusually extensive** for this space: ~2,000 test articles, 10⁻⁶ torr, ±20 µN resolution, polarity- and orientation-reversal controls, DC-only operation, and a Bluetooth-actuated untethered spinner that removes the HV feedthrough artifact.
- **David Chester's correction is the sharpest technical point against the premise** and Buhler accepted it: α enters at *classical* level too (the Coulomb tree diagram already carries two vertices), so α appearing in the data is **not** evidence of a quantum origin. Buhler additionally uses √α-per-order and α² interchangeably within one talk; those are not the same claim.
- **The governing integral is unsolved**, by his own account: *"it's 1/k^(7/2) and it's this mess which is a gamma function… that is a nasty integral that I have not been able to solve."* No third-order expression has been published; no paper has appeared, having been promised since 2024.

---

## 6. What survives — the one transferable result

The kill leaves a single well-posed discriminator, and it is independent of whether
Tajmar's null generalises:

> **Does the force require the leakage current?**

His theory says no — J^μ has zero spatial components, and he regards current-freedom
as the essential feature. His apparatus always has 0.1–0.2 µA flowing during
measurement. Nobody has separated the two.

- If the effect **requires** the current, his static-charge theory is modelling the wrong object, and the system is a driven dissipative steady state — the one regime in which ΔI is defined at all.
- If the effect is genuinely **current-independent**, then ACS has nothing to say about it by K2, and the ACS route should be abandoned rather than repaired.

Either outcome is informative, and the test is a single afternoon's work on apparatus
that already exists.

---

## 7. Scope boundary

This document establishes that **the ACS framework does not explain the Exodus
electrostatic anomaly**, and that the proposed bridge fails on three independent
structural grounds, any one of which is sufficient.

It does **not** establish that Buhler's measured force is an artifact; §4 reports
external evidence without adjudicating it. It does **not** evaluate his QED
derivation on its own terms — that would require the third-order expression, which
has not been published. It does **not** claim ACS is incompatible with a
current-dependent electrostatic effect; K2 leaves that specific door open, and §6
states the test that would open or close it.

**Sources.** Primary: APEC 2025-08-02 (`VuOx7n77G78`); Michels interview 2026-03-30
(`mOWwdIuyaQA`, theory from 01:53:28) and clip (`wMm3J-NvH-M`); Aurigema vacuum test
2024-07-05 (`kzCrhtVqXZw`); US 11,511,891 B2. External: Tajmar, Kößling & Neunzig,
arXiv:2402.15640 (verified against the primary PDF). Internal: `def:nested` and
`sec:torsion-hierarchy` in `Palatini_Gauge_Attractor.tex`; Q4 kill and the
2026-07-26 entries in `Elimination_Ledger.md`; `Framing_Transformer_Spin_Parity.tex`
§§6–8.
