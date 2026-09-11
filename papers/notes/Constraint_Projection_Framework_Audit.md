> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Audit of the Constraint Projection Framework

**Flag Condensate Collaboration** · Sovereign-Stack ACS Research Program · August 29, 2026
Readable mirror of `Constraint_Projection_Framework_Audit.tex` — **the `.tex` is authoritative.**
Target manuscript: `Constraint_Projection_Framework.tex` (archived as submitted).

---

## Abstract

The CPF manuscript claims a zero-free-parameter topological derivation of α, g, s, the
dark-matter density, cosmological flatness (via RH) and the Hubble radius from a single
non-orientable surface. **One displayed number survives its own computation**, and it is
CHSH. The rest fails on four independent grounds: an algebraic error a note already in
this repository had corrected; a scale parameter asserted to be fixed but required to
take four mutually exclusive values spanning 117 decades; an axiom with no model; and two
claims falsified in this repository's Elimination Ledger on 2026-07-26 and restated here
without reference.

**Revised 2026-08-29 (second pass).** A full verification run recomputed every step the
first pass had settled by structural argument. Two verdicts moved, both *against* the
manuscript, and both are corrected in place below with the earlier reading stated:
§5 — the Local Friendliness bound on the manuscript's sum is **4**, not 2, so S = 2√2
violates no LF inequality at all; and §7 — the *defining integral*, which the first pass
never evaluated, equals 2πN(T)/T → log(T/2πe) → +∞.

Instruments: `code/constraint_projection/cpf_audit.py` (first pass) and
`code/constraint_projection/cpf_full_verification.py` (full pass, V1–V9; `--deep`
recomputes the §7 contour integrals) · Artifacts:
`docs/constraint_projection_audit.json`,
`docs/constraint_projection_full_verification.json` · Ledger:
`docs/Elimination_Ledger.md`, 2026-08-29.

---

## Claim ledger

| Claim | Tier | Mechanism of failure |
|---|---|---|
| α⁻¹ = ln(8R/a)+1 | **T4** | factor of 2 dropped from the manuscript's own self-energy match |
| zero free parameters | **T4** | a/R fitted per section; four incompatible values, 117 decades apart |
| Axiom III (φ\* parabolic) | **T4** | M is forced to be the Klein bottle; MCG(K) = Z/2 ⊕ Z/2 is finite |
| g = Sl = 2, s = Sl/4 | **T4** | already killed 2026-07-26; Sl carries one parity bit, and g = 1 for every closed curve |
| k = 0 ⟺ RH ⟺ Ω_k = 0 | **T4** | the defining integral equals 2πN(T)/T → log(T/2πe) → +∞, not the claimed sum; and the claimed sum is invariant under β → 1−β |
| L_IR = R²/a ≈ 1.3×10²⁶ m | **T4** | 19–79 decades off, depending on which a is used |
| ρ_DM = (ħ²/2m)\|∇ψ\|² | **T4** | contains ½ρv²; needs m ~ 10⁻²³ eV |
| Axiom I (non-amenable B) | **T4** | every abelian group is amenable |
| S_LF = 2√2 | **T3** | **arithmetically correct** |
| that sum violates LF / falsifies AOE | **T4** | the LF bound on it is **4** (LP-verified); 2√2 < 4, so no LF violation, and Tsirelson forbids one |

Tiers never promote.

---

## §3 — the fine-structure constant: a dropped factor of two

The manuscript supplies three inputs and one conclusion:

```
C_M = 2π ε₀ R / L,   L ≡ ln(8R/a) + 1
(e/2)² / (2 C_M) = m_e c²
R = ħ / (2 m_e c)
                                        ⟹  claimed:  α⁻¹ = L
```

**Proposition.** Those three inputs imply `L·α = 2`, i.e.

> **α⁻¹ = ½ ( ln(8R/a) + 1 )**

*Proof.* `E_self = (e²/4)·L/(4πε₀R) = e²L/(16πε₀R)`. Setting this to `m_e c²` and using
`1/R = 2m_e c/ħ` gives `e²L/(8πε₀ħ) = c`, i.e. `L·α/2 = 1`. Verified symbolically
(check C1). ∎

**This correction is already in the repository.** It is eq. `(alpha_ann)` of
`Mobius_Ribbon_Capacitance.tex` (2026-07-22), which also records that matching CODATA
then forces `a/R = 8 exp(1 − 2α⁻¹) ≈ 2.04×10⁻¹¹⁸`. The manuscript reproduces the parent
note's *uncorrected* form and its 137.036, citing neither the correction nor the
conformal/BIE revisions that gave α⁻¹ = O(1) at moderate aspect ratio.

**Provenance of the log.** `ln(8R/a)` is the Kelvin–Maxwell thin-ring formula's log term;
in the standard ring inductance `L = μ₀R[ln(8R/a) − 7/4]` the additive constant is −7/4
(or −2). The manuscript's **+1** is neither derived nor attributed — and α⁻¹ depends on it
additively, so it is a second free knob.

**Circularity.** Even granting α⁻¹ = L, the step `a/R = 8e^(−136.035999171) ⟹ α⁻¹ =
137.035999171` is an identity: `ln(8/(8e^−x)) + 1 = x + 1` for any x. The target is
inserted in the premise. The asserted mechanism (G-field eigenvalue gap, GQRE
renormalization) is stated with no computation, and the Gravity-from-Entropy G-field is
*algebraically constrained* rather than obeying an independent wave equation, so the
discrete spectrum the argument needs does not follow from that action.

---

## The cutoff a: four mutually exclusive values

The "zero free parameters" claim rests on "the cutoff a is not free." Four requirements
are placed on it, at R = ħ/(2m_e c) = 1.9308×10⁻¹³ m:

| Constraint (source) | a/R | α⁻¹ (corrected) | L_IR = R²/a [m] |
|---|---|---|---|
| τ = i a/R = i/2 (§3) | 5.00×10⁻¹ | 1.886 | 3.9×10⁻¹³ |
| a/R = 8e^(−136.036) (§3) | 6.66×10⁻⁵⁹ | 68.518 | 2.9×10⁴⁵ |
| CODATA match on the corrected relation | 2.04×10⁻¹¹⁸ | 137.035999177 | 9.5×10¹⁰⁴ |
| L_IR = 1.3×10²⁶ m (§8) | 1.49×10⁻³⁹ | 46.242 | 1.3×10²⁶ |

**They span 117.4 decades.**

- **§3 contradicts itself internally.** `τ = i/2` gives `a/R = 1/2`, five lines before
  `a/R ≈ 6.7×10⁻⁵⁹` — 58 decades apart. On `a/R = 1/2` the manuscript's own formula
  returns `α⁻¹ = ln 16 + 1 = 3.77`.
- **The α leg and the L_IR leg cannot both run.** The manuscript's own a puts L_IR 19
  decades past the Hubble radius; the corrected a puts it 79 decades past; forcing L_IR
  gives α⁻¹ = 46.24.
- **"UV complete" fails too.** The a the corrected relation needs is 3.94×10⁻¹³¹ m, i.e.
  10⁻⁹⁶ Planck lengths.

**Verdict: the framework has exactly one free parameter, a/R, fitted separately in §3 and
§8.** Appendix B's parameter table is wrong as stated, and its comparison to the SM's 19
is not like-for-like — no mass, no mixing angle, and no coupling other than α is produced.

---

## Axiom III has no model

**Lemma.** A closed non-orientable surface with w₁ ≠ 0 whose orientation double cover is
T² is the Klein bottle `K = T²/⟨τ⟩`, `τ(x,y) = (x+½, −y)`. Clauses (1)–(2) therefore
determine M uniquely — and correctly.

**Proposition.** There is no `φ ∈ Diff(K)` with `φ_* = [[1,2],[0,1]]`.

*Proof.* Every diffeomorphism of K lifts to T² and must normalise the deck group {1, τ};
that group is Z/2, so normalising means commuting. On H₁(T²) = Z² the linear part of τ is
`D = diag(1,−1)`. Then:

```
[M, D] = 0  ⟹  M diagonal  ⟹  centraliser = {diag(±1,±1)} ≅ Z/2 ⊕ Z/2, order 4
                               (agrees with Lickorish 1963: MCG(K) = Z/2 ⊕ Z/2)
φ_*^n = [[1, 2n], [0, 1]]   ⟹  φ_* is parabolic of INFINITE order
φ_* D φ_*⁻¹ = [[1, −4], [0, −1]]  ≠  D
```

A finite group has no element of infinite order, and φ\* does not commute with D in any
case. ∎ (Exact integer arithmetic, check C3.)

**The weaker reading fails too.** Within the centraliser the available traces are
{+2, −2, 0, 0}, and **+2 is attained only by the identity** — which is not a Dehn twist and
supplies no self-linking number. So `Tr(φ_*) = 2 = Sl` has no carrier under either reading.

This is the structural kill: `τ = i/2` (§3), g and s (§4), and
`λ_UV·λ_IR = 1/R⁴` (§8) all rest on an axiom no surface satisfies.

**Second, independent obstruction in §3.** The Klein bottle admits **no embedding in R³**
— only immersions with self-intersection — so there is no conductor to charge. It is also
closed, so it has no boundary and no "double-cover annulus." The formula actually used
describes a different object.

---

## §4 — spin and g restate two logged kills

- **(a) g = Sl was killed by the parity law.** `σ = (−1)^(p+q) = (−1)^(Sl+1)`, measured
  over a control family of framed circles. The Sl = 0 round circle is spinorial in exactly
  the same sense as the |Sl| = 2 screw: the content is **one parity bit**, and 2 and 0 are
  the same bit. The manuscript reproduces the original mechanism of the error — matching
  the integer 2 across formalisms where it arises for unrelated reasons — and adds a third
  unrelated 2, the trace of a parabolic.
- **(b) The magnitude route is closed by a no-go.** μ and ⟨L⟩ are both proportional to the
  same vector area, so `μ/⟨L⟩ = q/2m` and **g = 1 exactly, for every closed curve**.
- **(b′) The data kills the completeness claim outright.** *(Added 2026-08-30,
  `wave_equation_gfactor.py`.)* Measured `a_e = 1.15965218059(13)×10⁻³` (Fan et al., PRL
  **130**, 071801 (2023)), so any framework outputting "g = 2 exactly" sits **8.92×10⁹ σ**
  from the data. Lévy-Leblond and tree Dirac stop at 2 as well — no mark against them,
  since neither claims to be finished and QED continues the series with an independently
  measured α. The manuscript claims zero free parameters, UV/IR completeness and "all
  constants"; `Sl` is an **integer** and the framework has **no expansion parameter**, so
  there is no route to 1.16×10⁻³ at any order. Terminal, and terminal on its own headline
  observable.
- **(b″) The geometry was never needed.** Machine-checked: `g = 2` follows from the su(2)
  algebra plus linearization of the *Schrödinger* equation (Lévy-Leblond 1967) — no `c`,
  no Lorentz, no metric, no surface. The whole factor of 2 lives in
  `(σ·π)² = π² − qħ(σ·B)`. And 4π periodicity is `π₁(SO(3)) = Z/2` in the spinor rep
  (`exp(−i·2π·σ_z/2) = −I`) — a group, not a non-orientable manifold. §4's two headline
  outputs are both free consequences of structure the manuscript already assumes, by a
  route that never touches Axiom III.
- **(c) Three further errors.** The repo's own computation gives `Tw + Wr = −2.000000`, so
  `s = Sl/4` would give s = −½. A (p,q) torus knot with q = 1 is the **unknot** — the
  parent note already carries this correction. And the 4 in `s = Sl/4` is nowhere derived:
  Finkelstein–Rubinstein yields a Z/2 sector, not a magnitude — exactly the gap that
  killed claim (a) the first time.

---

## §7 — the defining integral was never evaluated; it diverges

§7 defines

```
k(ε) = lim_{T→∞} (1/T) ∫₀^T [ ζ'/ζ(½+ε+it) − ζ'/ζ(½−ε+it) ] dt        (*)
```

asserts via Guinand–Weil that this equals `2ε Σ_ρ 1/((½−β)² − ε²)`, and concludes
k = 0 ⟹ RH ⟹ Ω_k = 0.

> **Correction to the first pass.** The first pass tested only the *claimed sum*. It
> did not evaluate (\*). Doing so is decisive on its own.

**Proposition.** For 0 < ε < ½,

```
(1/T) ∫₀^T [...] dt  =  2πN(T)/T + O(log T / T)  →  log(T/2πe)  →  +∞
```

real, positive, **independent of ε**, and **divergent**.

*Proof.* Take the rectangle with corners ½±ε and ½±ε+iT. The pole of ζ at s = 1 lies
outside for ε < ½; the poles of ζ'/ζ inside are the zeros with 0 < γ < T. The two
vertical sides contribute i·I(T), so `i·I(T) + ∫_bot + ∫_top = 2πi·N(T)`, giving
`I(T) = 2πN(T) + i(∫_bot + ∫_top)` with ∫_bot an O(1) real constant and ∫_top = O(log T).
Divide by T and apply Riemann–von Mangoldt. ∎

Verified numerically (V5, `--deep`):

| T | ε | N(T) | Re[(1/T)I] | 2πN(T)/T | ratio | claimed −2N/ε |
|---|---|---|---|---|---|---|
| 20 | 0.10 | 1 | 0.323180 | 0.314159 | 1.0287 | −20 |
| 20 | 0.25 | 1 | 0.336315 | 0.314159 | 1.0705 | −8 |
| 40 | 0.10 | 6 | 0.946835 | 0.942478 | 1.0046 | −120 |
| 40 | 0.25 | 6 | 0.953112 | 0.942478 | 1.0113 | −48 |
| 60 | 0.10 | 13 | 1.359827 | 1.361357 | 0.9989 | −260 |
| 60 | 0.25 | 13 | 1.357772 | 1.361357 | 0.9974 | −104 |
| 80 | 0.10 | 21 | 1.645536 | 1.649336 | 0.9977 | −420 |
| 80 | 0.25 | 21 | 1.640179 | 1.649336 | 0.9944 | −168 |

The ratio → 1; Re[(1/T)I] agrees across ε to under 1%; Im[(1/T)I] → 0. At T = 80,
ε = 0.1 the computed value is **+1.6455** and the claimed one is **−420**: opposite in
sign, and off by a factor of 255.

> **What (\*) actually computes** is log(T/2πe) — the Riemann–von Mangoldt *smooth
> counting term*, which this repository already reproduces independently
> (`src/paper_b/berry_keating_counting.py`, T2(known)). So (\*) is a correct and
> standard object; it is simply not the object §7 says it is, and it converges to
> nothing.

Three further failures afflict the claimed sum even on its own terms:

1. **Blind by construction.** β enters only through `(½−β)²` — exactly the invariant of the
   functional equation's involution `β ↦ 1−β`. ζ's zero set is symmetric under that
   involution, so every off-line zero arrives with a mirror partner contributing
   identically. Numerically (50 zeros, ε = 0.1): β = 0.5 + 0.2 and β = 0.5 − 0.2 **both**
   give k = +333.33. The functional cannot distinguish RH from its negation.
2. **Inverted sign.** On the critical line every summand equals −1/ε², not 0. For N
   on-line zeros `k(ε) = −2N/ε`, divergent as N → ∞ and zero for no finite ε. **RH makes k
   maximally divergent**; the criterion points the wrong way.
3. **Empirical direction.** Ω_k is measured as 0.0007 ± 0.0019; no measurement establishes
   an exact zero. A biconditional makes a theorem of arithmetic contingent on CMB data, and
   would let a future curvature detection refute RH.

This repository nowhere claims RH proved and constructs no Hilbert–Pólya operator. §7
claims an *equivalence*, which is a proof claim in both directions. The corpus's
defensible statement remains Paper B's: RH ⇒ stationarity proved by AM–GM, converse
**conditional** on an unproved minimum-gap bound verified only to N = 200.

---

## §5 — the arithmetic is right; the identification is not

With `A(θ) = cos θ σ_z + sin θ σ_x` on |Φ⁺⟩ and the stated angles, the instrument returns
`E(A2,B2) = E(A2,B3) = E(A3,B2) = +1/√2`, `E(A3,B3) = −1/√2`, and

> **S = 2√2 = 2.8284271247…**, saturating the Tsirelson bound to machine precision.
> **Confirmed, T3.**

The identification does not survive — and it fails harder than the first pass recorded.

> **Correction to the first pass.** The first pass concluded "it is CHSH; its local bound
> is 2." True, but it compares against the wrong polytope.

**Proposition.** For S = E(A₂B₂)+E(A₂B₃)+E(A₃B₂)−E(A₃B₃),

```
max over LF = 4 = max over no-signalling,      while     max over local = 2
```

*Proof.* LF (Bong et al.) states p(ab|xy) = Σ_λ q(λ) p_λ(ab|xy) with every p_λ
no-signalling and p_λ(a|x=1), p_λ(b|y=1) deterministic, where x=1 is "open the lab and
read the friend's already-recorded outcome." Maximising a linear functional over a convex
hull equals maximising over the generators, so the LF bound is the largest of four LPs,
one per (a₁,b₁) ∈ {±1}². All four return **4.000000000** (V6).

Structurally: S contains no term with x=1 or y=1. Given *any* no-signalling behaviour q on
{2,3}×{2,3}, set a₁ = b₁ = +1 and define the mixed rows by the product form δ(a,+1)·q_B(b|y)
and q_A(a|x)·δ(b,+1); every no-signalling constraint is met, so q extends. The LF
polytope's projection onto the {2,3} block is therefore the **full no-signalling
polytope**, with CHSH maximum 4. ∎

**Corollary.** S = 2√2 ≈ 2.828 < 4. The manuscript's value **violates no Local
Friendliness inequality**, and by Tsirelson no quantum state or measurement could make
this expression do so. The "> 2" in §5 is the Bell local bound.

So:

- §5 demonstrates ordinary Bell nonlocality, established since 1982. It says nothing about
  AOE, because the expression it evaluates is insensitive to AOE by construction — the LF
  assumption constrains only the rows containing setting 1, and those rows do not appear.
  Bong et al.'s LF facets involve the x=1 row for exactly this reason.
- Even a genuine LF violation would not "falsify AOE": the LF theorem falsifies the
  **conjunction** of AOE, Locality and No-Superdeterminism, and the cited source says so.
- The C₆/D₆ axial frame, the projection onto it, and the super-observer structure are
  **inert** — none appears anywhere in the algebra that produces 2√2.

---

## §6 — the dark-matter term double counts, and needs an exotic scalar

With ψ = Re^(iS/ħ), the split is exact:

```
(ħ²/2m)|∇ψ|²  =  ħ²R′²/(2m)   +   R²S′²/(2m)
                                   ^^^^^^^^^^ = ½ ρ v²,   ρ = R², v = S′/m
```

- **(i) Double counting.** The second term is the visible matter's own kinetic energy
  density. `T₀₀ = ρ_vis c² + ρ_DM c²` then counts it a second time, as dark.
- **(i′) It is not the quantum potential.** The Madelung/Bohm "quantum pressure" — the
  term that actually shapes a rotation curve in every wave-dark-matter model — is
  `Q = −(ħ²/2m)∇²R/R`, an energy *per particle* that may be negative. The manuscript's
  expression is a positive-definite energy *density* built from R′², not R″/R. Different
  objects: §6 does not use the mechanism it names. *(Added on the second pass.)*
- **(ii) The Re/Im story is wrong.** `|∇ψ|²` is not a function of Im ψ alone, and the
  Re/Im split is not gauge invariant — a global U(1) phase rotates one into the other.
  EM coupling enters through the covariant derivative.
- **(iii) The scale.** Quantum pressure shapes a rotation curve only when λ_dB is galactic.
  At v = 200 km/s and L = 1 kpc the required mass is 1.7×10⁻⁵⁹ kg = **9.6×10⁻²⁴ eV/c²** —
  the fuzzy-dark-matter window, i.e. an ultralight scalar, which is exactly the "exotic
  particle" §6 claims to avoid. At m_e, λ_dB = 5.8×10⁻¹⁰ m, 29 decades too short-ranged.
  **The claim fails either way.**

No Jeans solution, rotation curve or dataset appears in §6; "matching observations" is
asserted, not shown.

---

## Axioms I–II and the bibliography

**Axiom I is false under every reading.** `A_Q/Q^×` is malformed — Q^× is multiplicative
and does not act on the additive adeles by translation. The two standard objects, `A_Q/Q`
(compact, additive) and the idele class group `A_Q^×/Q^×`, are both **abelian, hence
amenable** (Markov–Kakutani); the first is compact and carries a translation-invariant
Haar *probability* measure. The axiom asserts no finitely additive translation-invariant
probability measure exists. Non-amenability is load-bearing for the manuscript's framing
and is unavailable here.

**Axiom II is ill-posed.** The kernel maps onto R^{3,1}, but δ⁽³⁾ fixes only three
coordinates — nothing supplies the time direction — and a 2-parameter integral against a
3-dimensional delta is generically distributional, so "Fredholm" is not established.

**Bibliography.**
- `[Bianconi2024]` `arXiv:2401.12345` is a placeholder. The paper is G. Bianconi, "Gravity
  from entropy," **arXiv:2408.14391**, Phys. Rev. D **111**, 066001 (2025).
- `[CODATA2022]` "E. Tiesinga et al., Rev. Mod. Phys. **94**, 035002 (2023)" matches no
  CODATA article of record. CODATA 2018 = Tiesinga, Mohr, Newell & Taylor, RMP **93**,
  025010 (2021); CODATA 2022 = Mohr, Newell, Taylor & Tiesinga, RMP **97**, 025002 (2025),
  α⁻¹ = 137.035999177(21).
- `[Proietti2019]` and `[Finkelstein1968]` check out as cited.

---

## What survives, and what repair would take

**Survives.**

1. **S = 2√2** under the stated operators and state (T3) — a correct computation of a
   known quantity.
2. **M = Klein bottle** from clauses (1)–(2) is correct and unique — confirmed by an
   Euler-characteristic census (χ(N_k) = 2−k, cover genus h = k−1, so h = 1 only at k = 2)
   and by computing H_*(K;Z) from the CW complex via Smith normal form. The one piece of
   topology in the paper that does what it claims. Clause (3) is what fails. *(Minor: H₂ = 0
   holds for every closed non-orientable surface, so that clause is implied by w₁ ≠ 0.)*
3. `ln(8R/a)` is the right functional form for a thin-ring self-energy, inherited correctly
   from the parent note; the prefactor, the additive constant, and the cutoff are wrong.

**Repair, leg by leg.**

- **α** — adopt the corrected relation, then *derive* a/R from something that is not α, and
  accept whatever number comes out. The repository's conformal and BIE revisions give O(1)
  at moderate aspect, so the honest current state is that this route does not reach 137.
- **Axiom III** — either drop clause (3), or use a surface whose mapping class group does
  contain an infinite-order parabolic — but then the T² double cover, and with it the whole
  modular-parameter argument, is gone.
- **g** — the ledger's standing successor applies unchanged: **decouple where the charge
  sits from where the mass sits.** No framing, twist or trace-matching substitutes for it.
- **§7** — two repairs. (a) Redo the Guinand–Weil step: the defining integral is 2πN(T)/T,
  so any claim about it must survive the Proposition above. (b) A functional detecting
  off-line zeros must be **odd** under β ↦ 1−β; any construction whose β-dependence factors
  through (½−β)² is blind for the same reason. *(b) is the one genuinely new structural
  boundary the audit produces: it bounds a class, not a single attempt.*
- **§5** — an LF test must contain the x=1 / y=1 rows; by the Proposition above an
  expression without them cannot violate LF at any quantum value. Take an actual LF facet
  from Bong et al. and evaluate it.
- **§6** — accepting the ultralight mass makes this fuzzy dark matter: real and testable,
  but a proposal *with* an exotic particle, inheriting that literature's constraints.

**On the framing.** The manuscript's closing "the ledger is sealed" inverts this program's
discipline. The Elimination Ledger is append-only precisely so that it is never sealed; its
entries are kills aimed at the program's own load-bearing claims, kept because they bound
the space. Two of the claims this manuscript advances as derivations are entries in that
ledger. A framework declaring zero free parameters while fitting one parameter four ways,
and declaring completeness while restating falsified results, is describing the failure
mode this corpus names as primary: **overclaiming**.

---

## Files

- Manuscript (as submitted): `papers/notes/Constraint_Projection_Framework.tex`
- Formal TeX (authoritative): `papers/notes/Constraint_Projection_Framework_Audit.tex`
- Instruments: `code/constraint_projection/cpf_audit.py` (first pass),
  `code/constraint_projection/cpf_full_verification.py` (full pass, V1–V9),
  `code/constraint_projection/wave_equation_gfactor.py` (origin of g = 2, W1–W9)
- Artifacts: `docs/constraint_projection_audit.json`,
  `docs/constraint_projection_full_verification.json`, `docs/wave_equation_gfactor.json`
- Ledger entry: `docs/Elimination_Ledger.md`, 2026-08-29
- Prior repo results relied on: `papers/notes/Mobius_Ribbon_Capacitance.tex`,
  `papers/notes/Framing_Transformer_Spin_Parity.tex`, `code/framed_unknot/`
