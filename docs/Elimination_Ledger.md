> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Elimination Ledger

**Append-only.** Strip-mine discipline: rank targets by expected-space-collapsed
per unit cost; weight toward kills aimed at our **own** load-bearing claims. A
landed kill credits the survivors by elimination — no proof required. Don't prove
the gold is there; remove everything that isn't.

- Seed convention: `20260423`
- Tiers: **T1** machine-verified / **T2** proven-or-by-inspection / **T3** numerical / **T4** falsified
- Status tags: `QUEUED` / `IN-PROGRESS` / `KILLED` / `SURVIVED` / `SPLIT` / `BLOCKED`

> **Provenance note (2026-08-07).** Several kill-test scripts below are cited at
> ephemeral paths (`/tmp/…`) or without a path; those scripts were run on external
> session machines and were **not committed to this repository**. For the affected
> entries the recorded verdict rests on the logged outputs quoted in this ledger, not
> on a rerunnable artifact — i.e. the practical reproducibility standard is (b)
> structural/logged rather than (a) recomputable, in the sense of the tiering note
> above. Entries citing repo-relative paths under `code/` are rerunnable as stated.
> Affected citations are annotated inline.

**Engine kill-criterion (tomographic invariance).** A quantity is a **REFRACTION**
if its value moves under a legitimate change of instrument (representation /
normalization / convention / scale / window). It is an **INVARIANT (candidate)** if
it does not. Precedent kill: "universal 2π inversion" → representation-specific
(sl(4,R) adjoint is hyperbolic, not rotational). The criterion can be applied two
ways: **(a)** numerically, by recomputing under an instrument swap (→ T1), or
**(b)** structurally, by arguing from the quantity's construction when no
recomputable pipeline is reachable (→ T2). Tier honestly; never let (b) wear (a)'s
clothes.

---

## TARGET QUEUE (priority order)

### Swing now — cheap, decisive, high collapse

**Q1-TARGET — Framework constants: invariant or refraction?** `IN-PROGRESS → see KILLS LOGGED 2026-06-06`
*(renamed from "T1-TARGET" to avoid collision with the Tier-1 label; matches "Q1" in the scorecard)*
Kill target: "λ_φ = 2√3/27, h̃/h = 2/3, g₄ = g_L = g_R = 4/3, γ = 0.274 are
representation-independent invariants." Kill test: apply kill-criterion to each.
Kill condition: value moves under a valid representation/normalization/convention/scale
change → refraction. Collapse: any one demotes from the "locked" column of the
parameter ledger. Cost: low.

**Q2-TARGET — BRA speed-superiority.** `BLOCKED (needs kernel signatures + reference op)`
Kill target: "trinity-wasm BRA kernel beats TF-f32 at its matched operation."
Kill test: native rlib bench, real kernel vs TF-f32, matched op, matched N range.
Kill condition: slower across the working N range. Collapse: settles the last open
BRA leg; if killed, kernel value rests on determinism + transparency alone (cleanly
bounded). Cost: low once unblocked.

**Q3-TARGET — T_min height floor (2πe)^d/q as a real invariant.** `QUEUED`
Kill test: vary window / N / taper with the zeros engine. Kill condition: floor moves
with windowing → refraction. Collapse: bounds the status of the LF01 correction.
Cost: low.

### Build the kill test, then swing — highest collapse, needs a testbed

**Q4-TARGET — ΔI = c-function (FF06Σ Link 3).** `QUEUED (needs CFT testbed)`
Kill target: the *identity* ΔI ≡ RG c-function (not analogy). Kill test: a system
where both are independently computable — a known 2D CFT with known c — compute ΔI
there, check it disagrees or fails monotonicity where c is monotone. Kill condition:
divergence where both are defined. Collapse: the largest on the board — the spine of
"one mechanism, many forms." Cost: high (the work is *building* the testbed).

### Continue the strip-mine — empty-tunnel mapping

**Q5-TARGET — Remaining Hilbert–Pólya operator candidates.** `QUEUED (3 already down)`
Kill test: spectrum vs zeros / self-adjointness / density. Kill condition: mismatch or
non-self-adjoint. Collapse: each maps another empty tunnel; survivors gain. Cost: medium.

**Q6-TARGET — Residual prime-orbit off-diagonal mechanisms.** `QUEUED (2 already down)`
Kill test: pre-register candidate, surrogate-test against incommensurable null. Kill
condition: consistent with null. Collapse: narrows off-diagonal space. Cost: low.

**Q7-TARGET — Neutrino seesaw resolution (PS gauge suppression).** `QUEUED`
Kill target: "(M_W/M_{W_R})² suppression brings sin²2θ under the X-ray bound." Kill
test: compute it. Kill condition: doesn't clear the bound. Collapse: resolves a
flagged tension. Cost: medium.

---

## KILLS LOGGED

### 2026-06-06 — Target 1: framework constants invariant-or-refraction — **T2 STRUCTURAL**

**Method note.** The ACS derivation code for these four constants is not reachable in
this environment (`computatioanal_work_ACS` — *sic*, directory name recorded as-is — contains the TENT classifier notes, not
the Koide-projection / Palatini-bracket / Barbero–Immirzi pipelines). So this is the
kill-criterion applied **structurally** (path (b)), not a numerical recomputation
under an instrument swap. Verdicts are T2, argued from each constant's construction
and from the framework's own scope notes. **T1 upgrade path for every entry below:
run the actual ACS derivation under a representation/normalization swap and check
whether the number moves.**

**g₄ = g_L = g_R = 4/3 → REFRACTION (value) / INVARIANT (relation).** `SPLIT`
A bare gauge-coupling *value* is generator-normalization-dependent (e.g. the
conventional Tr(TᵃTᵇ) = ½δᵃᵇ vs unit normalization; GUT-normalization rescalings).
Change the normalization and "4/3" changes. The **equality** g₄ = g_L = g_R, by
contrast, is an equality of three couplings in one shared normalization and survives
any consistent rescaling — that is the predictive content (Pati–Salam coupling
unification at the breaking scale). Hedge: 4/3 could survive *if* ACS pins a canonical
normalization in which it is secretly a ratio to a fixed reference — cannot confirm or
rule out without the derivation. Absent that, the number is a refraction; the
unification equality is the invariant.

**γ = 0.274 → REFRACTION (value).** `KILLED`
The value is counting-prescription-dependent: γ = 0.274 is the unconstrained (Meissner)
value; the physical γ = 0.2375 (Domagala–Lewandowski) requires the SU(2) Gauss
constraint via Chern–Simons projection. The framework already documents both. Value
moves (0.274 → 0.2375) under a change of the state-counting prescription ⇒ kill
condition met. The invariant is structural — "there is a fixed γ once a prescription is
fixed" — not the number 0.274. This kill **formalizes** the framework's own existing
scope note rather than surprising it: promotes a documented ambiguity to an explicit
refraction verdict.

**h̃/h = 2/3 → INVARIANT (candidate).** `SURVIVED`
A dimensionless ratio (multiplicative normalization cancels) that is additionally
claimed to be an RG invariant (scale-protected — this is the same property that makes
the tan β protection argument work). A normalization-cancelling, scale-invariant
dimensionless ratio is the strongest invariant candidate of the four; it survives both
the normalization swap and the scale swap on structural grounds. Tier note: "candidate"
because the RG-invariance claim itself should be machine-checked — **T1 upgrade =
integrate the RGEs and confirm d/d(lnμ)(h̃/h) ≈ 0 numerically.**

**λ_φ = 2√3/27 ≈ 0.1283 → SPLIT (geometry invariant / physics-identification scale-relative).** `SPLIT`
Two distinct claims hide in one symbol. (i) **2√3/27 as a number of the Koide
projection geometry** is a fixed mathematical constant of the construction — it does
not move under representation change → INVARIANT. (ii) The **identification** "the
physical Higgs quartic *is* 2√3/27" is scale-conditioned: the quartic runs, and
λ_ACS = 0.1283 crosses the experimental running quartic only at μ ~ 132 GeV. So the
number is special at one scale, not universally → the *identification* is scale-relative
(a refraction w.r.t. renormalization scale). The geometric origin is the candidate
invariant; the bare-number-equals-observable reading is not.

**Net verdict (Target 1).** Of four "locked" constants, two bare values (g₄, γ) demote
to refraction; one ratio (h̃/h) survives as the strongest invariant candidate; one
(λ_φ) splits into an invariant geometric number and a scale-relative physical
identification. **Meta-pattern: the relations survive (the equality g₄=g_L=g_R, the
ratio h̃/h, the Koide-geometric origin of 2√3/27); the bare normalization- or
scale-laden numbers mostly don't.** This is the expected signature of real physics —
observables are relations — and it sharpens the parameter ledger by moving the claims
that were always going to be convention-dependent out of the "fundamental number"
column. All verdicts T2; T1 upgrades require the ACS derivation code under an
instrument swap (g₄, γ, λ_φ) or an RGE integration (h̃/h).

---

### 2026-06-06 — Target Q3: T_min height floor (2πe)^d/q — **SURVIVED (scoped)** · T2 value / T3 empirical

Code: `/tmp/q3_floor.py` (zeta zeros, N=100000). *(script not committed to this repository; run on an external session machine — see the provenance note at the top of this file)*

**Floor value is an analytic invariant, not a refraction.** For d=1,q=1 the floor is
the exact zero of the Riemann–von Mangoldt main term: (T/2π)(log(T/2π)−1) = 0 at
T = 2πe ≈ 17.0795 (machine-zero confirmed; log(2πe/2π)=log e=1). There is no window,
taper, N, or representation freedom anywhere in that identity — the value cannot move
under any instrument choice. Decoy floors (2πe·φ, (2πe)²/10, 2πe/1.5) are not
privileged: only 2πe gives a vanishing main term. By the pre-registered kill condition
("floor moves under windowing → refraction"), the floor **survives** as an invariant.
Above it, the count error |N_full − N_actual| stays O(1) (0.13–0.59 across sampled
heights, RvM-valid); below it the main term is negative (count asymptotic meaningless).
Tier: value-invariance **T2** (identity by inspection); empirical count-tracking **T3**.

**Honest scope.** This is only the d=1,q=1 point. The actual predictive content of the
claim — the exponential-in-degree, linear-in-conductor scaling (2πe)^d/q — is **UNTESTED**
by anything reachable here. ζ-only zeros are a single (d,q). A real test of the scaling
law needs LMFDB L-function zeros at d>1 and q>1; that evidence currently lives only in
the paper's examples table, not independently reproduced.

**Method honesty.** Two broken statistics caught in my own test before being read as
signal: (1) a band-relative-error "onset" metric that was discreteness-dominated at low
T (sparse zeros → noisy band counts), discarded; (2) a max-deviation line with a
subsample-index bug, discarded. Per-height count-error values stand.

### 2026-06-06 — Target Q6: residual prime-orbit off-diagonal mechanism — **KILLED** · T2 structural / T3 numerical

Code: `/tmp/q6_offdiag.py` (explicit-formula dual periodogram, first 3000 zeros, Hann taper). *(script not committed to this repository; run on an external session machine — see the provenance note at the top of this file)*

**No residual peaked off-diagonal mechanism exists.** Power ratio to local baseline:
fundamentals log2/3/5/7 ≈ 3–4×10⁸; prime-power harmonics 2log2, 3log2, 2log3, 2log5 ≈
5×10⁷–4×10⁸ (real peaks, suppressed 2–4× by the p^{k/2} weight); composites
log6/10/12/15 ≈ 0.3–5.4 (baseline noise, ~10⁻¹² power); decoys ~1. The peaked spectrum
is **exactly** the diagonal prime-power set {k·log p}, at 10⁷–10⁸ contrast.

**Structural reason (T2), not just numerics.** The explicit-formula dual carries weight
only on the von Mangoldt function Λ(n), which is supported on prime powers; composites
n = p·p′ have Λ=0, so a sum-frequency off-diagonal peak at log(pp′) is not merely
unobserved but **forbidden by the support of Λ**. Difference-tone off-diagonal peaks
were falsified in prior work. The two natural peaked off-diagonal families are therefore
both dead; the only remaining off-diagonal content is **smooth** — the Montgomery
pair-correlation term, separately confirmed (0.988→0.993 toward Montgomery). Tunnel
mapped empty. Tier: **T2** (Λ support forbids composite peaks) + **T3** (10⁸-contrast
numerical confirmation, this window).

**Queue status update.** Q3 → SURVIVED (scoped; d,q-law BLOCKED on LMFDB). Q6 → KILLED.
Standing peaked-off-diagonal space for the zeta spectrum is now exhausted: {k log p}
diagonal (forced by Λ), smooth Montgomery off-diagonal (confirmed), no third option.

### 2026-06-06 — Target Q5: Hilbert–Pólya operator candidates — **CLASS KILLS (GOE, GSE) + xp-alone killed-as-sufficient** · T3 numerical / T2 structural

Code: `/tmp/q5_hp.py` (zeta zeros 10000–40000, RvM-smooth unfolding). *(script not committed to this repository; run on an external session machine — see the provenance note at the top of this file)*

Strip-mine done at the **class level** (cannot construct/diagonalize a genuine
self-adjoint operator here — that is the open problem itself). The data forces
discriminating constraints; those constraints kill candidate classes.

**Symmetry class → GUE (unitary).** Unfolded spacing L2 distance: GUE 7.31e-2 ≪
GSE 1.72e-1 < GOE 2.26e-1 ≪ Poisson 6.52e-1; fitted level-repulsion exponent
β = 2.12 ≈ 2; variance 0.1600 (reproduces record 0.1607). Under RMT universality the
HP operator must be unitary-class: complex Hermitian, **broken time-reversal symmetry**.
This **kills**: (i) any real-symmetric / T-invariant candidate (GOE, β=1) — e.g. a naive
real Schrödinger operator; (ii) any symplectic candidate (GSE, β=4). Two tunnels mapped
empty. Tier T3 (decisive numerically; rests on RMT universality, not a theorem for ζ).

**Berry–Keating xp.** Smooth-density necessary condition PASSED: the xp semiclassical
count (T/2π)(log(T/2π)−1) matches the actual staircase to <0.2% (ratios 0.998 / 1.00001
/ 0.99998 at T=10³/10⁴/5·10⁴). But xp has a **continuous** spectrum — no discrete
eigenvalues — and S(T) fluctuations are prime-driven, which bare xp does not encode. So
"xp alone is the HP operator" → **killed as sufficient** (necessary-but-insufficient);
"xp as the smooth skeleton" → survives. Tier T2 structural (continuous-spectrum
insufficiency is known) + T3 (smooth match).

**Net.** No claim to have found or killed *the* operator (open). The data now forces
any survivor to satisfy three conditions simultaneously: unitary class (broken T) +
(T/2π)log(T/2πe) smooth count + primes in the fluctuation spectrum. GOE and GSE classes
are out; bare xp is out as a complete answer. Queue: Q5 → PARTIAL (class kills logged;
full-operator search remains open, BLOCKED on a construction, not on data).

### 2026-06-06 — Target Q4: ΔI ≡ RG c-function (FF06Σ Link 3) — **INSTRUMENT BUILT + STRUCTURAL DAMAGE; numerical kill BLOCKED on ΔI def** · T1 instrument / T2 structural

Testbed: `q4_cfunction_testbed.py` (TFIM = free Majorana, M=14 exact diagonalization). *(script not committed to this repository; run on an external session machine — see the provenance note at the top of this file)*

**Blocker (honest).** The FF06Σ Link-3 statement and the formal ΔI being identified
with c are NOT in the reachable corpus. The only ΔI present is the TENT/CDCL routing
scalar `delta_i()` ∈ [0,1] (0.86 active / 0.00 stricken; "CDCL nearly monotone"). The
"central charge" hits in FF06b are the *gauge* central charge (U(1)_{B−L}→1/3), a
different object from the Zamolodchikov c. So the full numerical kill cannot run until
the ΔI definition is supplied.

**Instrument built and validated (T1).** A provably-monotone reference c-function
(Casini–Huerta entropic c-theorem). Critical TFIM recovers c = 0.508 (local 0.501 vs
exact Ising 1/2, <2%); massive phase flows monotonically c(L): 0.237→0.025→0. This is
the independent "c" side; a ΔI plug-in slot + the four-point kill protocol (fixed-point
value 1/2, IR value 0, monotonicity, stationarity) are pre-registered in the testbed.

**Structural damage already done (T2), no ΔI numerics needed.** c is unbounded above
(free boson c=1; N free bosons c=N; string c=26). Therefore the *universal identity*
ΔI ≡ c is dead unless ΔI is both unbounded and canonically normalized:
 - If ΔI is the routing scalar (∈[0,1]) → **FALSIFIED for every c>1 theory**; survives
   at most restricted to c≤1.
 - If ΔI is unbounded transfer-entropy (≥0, nats) → bound objection void, but identity
   needs a fixed unit (nats→dimensionless); absent it the defensible claim is ΔI ∝ c,
   not ΔI = c.

**Verdict.** Q4 → IN-PROGRESS. Highest-collapse target takes structural damage now: the
*universal identity* requires ΔI unbounded **and** canonically normalized — otherwise
it is already an analogy/proportionality, not an identity. Completing the numerical kill
needs (1) which ΔI is meant, (2) its definition dropped into `delta_I_of_state()`. Note
candidate (b) — a mutual-information c-function I(A:B) — *would* match c by construction
(that is the Casini–Huerta route), so if FF06Σ's ΔI is the MI form the identity could
SURVIVE; if it is transfer-entropy-asymmetry or the routing scalar, it does not. The
disambiguation is now the load-bearing question.

### 2026-06-06 — Target Q4 (cont.): instrument pushed to large L — **PRODUCTION-GRADE, gate-validated** · T1

Code: `/tmp/q4_largeL.py`; folded into `q4_cfunction_testbed.py` (`bdg_S`, `c_function_large`). *(script not committed to this repository; run on an external session machine — see the provenance note at the top of this file)*

Free-fermion BdG method, **validation gate PASS**: reproduces exact diagonalization to
1e-13–1e-15 on the same open chain (M=12, h=1.0/1.3, L=1/3/6) — instrument trusted at
scale. At M=400: critical fit c = 0.4884 (Ising 1/2, ~2%); massive entropic c-function
**monotone 0.5→0** with onset at ξ~1/|h−1| (h=1.02→0.001 by L=156; h=1.3→~0), for every
mass. The "c" side is now production-grade. Kill remains BLOCKED only on the FF06Σ ΔI
definition; once supplied, ΔI is computed from the same BdG Gaussian state and checked
against the four pre-registered conditions at large L. Structural damage (universal
identity dead unless ΔI unbounded & canonically normalized) stands independent of this.

### 2026-06-06 — Target Q7: neutrino seesaw / X-ray tension — **RESOLVED (survives), decoupling caveat** · T3 estimate / T2 structural

Code: `/tmp/q7_neutrino.py`. *(script not committed to this repository; run on an external session machine — see the provenance note at the top of this file)* Inputs: framework's stated naive sin²(2θ)=4×10⁻⁶ and
X-ray bound 10⁻¹⁰; PDG M_W=80.4 GeV; v=246.22; generic seesaw × stated (M_W/M_WR)²
suppression (NOT the full FF06 mechanism — verdict is conditional on this reading).

Required suppression S < 2.5×10⁻⁵ → M_WR ≳ 16 TeV (v_R ≳ 49 TeV). Independent lower
bounds on the PS/W_R scale (LHC ~5–6 TeV; rare decays K_L→μe push v_R to ≳100s TeV)
already exceed this, so the suppression clears the X-ray bound by orders of magnitude
for any realistic v_R. The framework's "tension, not resolved" flag upgrades to: **not
a live tension** — the stated mechanism works comfortably.

**Structural caveat (the real content).** Clearing the bound requires high v_R, hence
high M_R ~ v_R, so the sterile/right-handed neutrino is **not keV-scale dark matter** at
that scale. The resolution is by *decoupling*: the X-ray constraint (a keV-sterile-DM
bound) is evaded by removing the sterile state from the keV-DM role, not by suppressing
a keV-DM mixing in place. Verdict therefore splits on intent — viable as "the X-ray
bound is no obstruction" (SURVIVES); fatal if a keV-sterile-DM candidate was required
(that role does not survive). Not a kill of the framework; a kill of the keV-DM reading.

---

## SESSION SCORECARD (2026-06-06)

| Target | Verdict | Tier |
|--------|---------|------|
| γ = 0.274 | KILLED (prescription-dependent) | T2 |
| Q6 off-diagonal mechanism | KILLED (Λ supported on prime powers) | T2+T3 |
| Q5 GOE/GSE operator classes | KILLED; xp-alone killed-as-sufficient | T3+T2 |
| g₄ = 4/3 | SPLIT (relation invariant, number refraction) | T2 |
| λ_φ = 2√3/27 | SPLIT (geometry invariant, identification scale-relative) | T2 |
| h̃/h = 2/3 | SURVIVED (strongest invariant candidate) | T2 |
| Q3 floor 2πe | SURVIVED, scoped (d,q-law untested) | T2+T3 |
| Q4 ΔI ≡ c | INSTRUMENT BUILT + universal identity structurally damaged | T1+T2 |
| Q7 neutrino X-ray | RESOLVED, decoupling caveat | T3+T2 |

Self-corrections this session: two broken statistics caught before reading as signal
(band-relative-error onset; subsample-index max-dev bug).

## REMAINING — all BLOCKED on inputs/constructions, not on swings

| Target | Needs |
|--------|-------|
| Q2 BRA speed | `bra_*` kernel signatures + the TF op it replaces (native rlib bench) |
| Q3 (d,q) scaling | LMFDB L-function zeros at d>1, q>1 |
| Q4 ΔI ≡ c (finish) | the FF06Σ Link-3 ΔI definition (3 readings → 3 verdicts) |
| Constant T1-upgrades | ACS derivation code under representation swap; RGEs for h̃/h |
| Q5 full HP operator | a candidate construction (open problem) |

---

## OOS01 RESULTS (2026-06-06, Mac via Antigravity) — reviewed & re-tiered

> **External-label key.** *OOS01* = the first out-of-session kill campaign (external run,
> 2026-06-06). *Antigravity* = the external agent/machine session that executed that
> campaign (its verdicts are reviewed and re-tiered here, not accepted as-is). *W2F* = the
> external session's working-to-file log; not committed to this repository. *Category A\** =
> that log's top regression-severity class. *trinity-wasm* = a private codebase whose
> benchmark inputs are not vendored here; the Q2 bench is therefore externally-verified-only.

### Q2 BRA speed — **KILLED (T1, measured)**, with a precision confound noted
Matched op identified: Gabor wave-packet render/energy (`bra_render`/`bra_energy`),
replacing TF `exp(-dt²/2w²)·exp(2πi f dt)` (f32). Measured ns/op (release rlib):
BRA-f64 is **1.37–1.82× SLOWER** than TF-f32 across N=16..1024. The withdrawn "489×
faster" is contradicted by direct measurement — not faster, slower. Speed-superiority KILLED (T1).
**Confound (honest):** the bench is BRA-**f64** vs TF-**f32**; f64 carries ~1.5–2× the
work, so at matched precision (f64-vs-f64) BRA is plausibly ~par, not 489×. So: "faster
than the TF you'd actually run (f32)" → FALSE; "competitive at matched f64" → untested,
plausibly par; "489×" → dead either way. **Real surviving value = determinism: integer
AND f64 paths bit-identical across runs (T1 PASS).** That was always the genuine claim.

### Q4 ΔI ≡ c — **identity falsified as stated (T2); monotonicity-analogy is the survivor** — CORRECTING Antigravity's pin
Definitions found (the unblock): routing `delta_i = 0.4·consistency+0.3·divergence+
0.2·late_error+0.1·recomposition` ∈[0,1] (reading a); **physics ΔI = TE(F→G)−TE(G→F)**,
a transfer-entropy asymmetry (reading b); Link-3 verbatim: "ΔI = c-function."
Antigravity pinned the verdict on reading (a) [bounded → kills c>1]. **That is the wrong
ΔI.** Link-3 lives in the FF06Σ physics context, where ΔI is the transfer-entropy
asymmetry (b). Under (b) the *identity* faces three structural mismatches, none about
boundedness: (1) **sign** — c≥0, but a TE difference is signed; (2) **fixed-point value**
— at a symmetric fixed point TE(F→G)=TE(G→F) ⟹ ΔI=0, while c=central charge≠0 (e.g. 1/2);
(3) **category** — TE is a temporal directed-info-flow quantity; c is static/spatial
(Zamolodchikov / Casini–Huerta). Identity dead as stated (T2). What *survives* is the
**monotonicity analogy**: ΔI decreasing along its flow as c decreases along RG flow —
which is exactly what `dI_monotonicity.py` actually tests. So the defensible content is
ΔI *plays the role of* c (monotone along flow), not ΔI = c numerically. The c-side
instrument stands ready if a static, positive, normalized ΔI is ever defined; the ΔI
that exists is not that.

### Q1 framework constants — **T1 UPGRADE (all four predictions machine-confirmed)**
Re-run under representation/normalization swaps (matches the engine kill-criterion):
- g₄ = 4/3 → **2/3** under Tr(TᵃTᵇ)=½δ vs δ rescaling → REFRACTION, **T1** (hard before/after). Equality g₄=g_L=g_R remains the invariant.
- γ = 0.274067 (SU(2)/half-integer counting) → **0.190206** (SO(3)/integer counting), |Δ|=0.0839 → REFRACTION, **T1** (hard before/after).
- λ_φ = 2√3/27 → convention-laden, scales with Killing-form normalization → REFRACTION, **T1** (asserted; no explicit before/after pair — softer than g₄/γ).
- h̃/h = 2/3 → scale-invariant algebraic constraint, d/d(lnμ)≈0 → INVARIANT, **T1**.
Meta-pattern now machine-confirmed: **relations/ratios survive (g₄=g_L=g_R, h̃/h); bare
normalization-laden numbers are refractions (g₄'s 4/3, γ's 0.274, λ_φ's 0.1283).**
My session T2 verdicts upgrade to T1; my λ_φ "geometry-number invariant" hedge was
slightly too generous — machine says the value moves under Killing-form normalization.

### Q3 (d,q) scaling — **NOT-FOUND (still blocked)**
Only ζ zeros (d=1,q=1) on disk; no degree-2 or q>1 L-function zeros. Scaling law of
T_min=(2πe)^d/q remains untested, exactly as scoped. Needs an actual LMFDB fetch.

### Q5 AISO regression — **T1 PASS** (logged to W2F record)
Full workspace 842 passed / 0 failed; Step 3 OpenAPI reproduces green; Category A*. No
regression from the #[non_exhaustive] refactor or SIGPIPE fix. (Count grew 343→842 =
wider binary scope, not a regression.)

## SCORECARD UPDATE (post-OOS01)
KILLED: γ (now T1), Q6, Q5-classes, **Q2 BRA speed (T1)**, **Q4 identity-as-stated (T2)**.
SURVIVED/INVARIANT: h̃/h (now T1), Q3 floor (scoped), Q4 monotonicity-analogy, Q7 (decoupling).
REFRACTION (T1): g₄'s 4/3, γ's 0.274, λ_φ's 0.1283. BLOCKED: Q3 (d,q) law, Q5 full HP operator.

### 2026-06-06 — Target Q4 (monotonicity reading) — **RESOLVED; target now fully closed** · T1 numerical / T2 theorem

Code: `/tmp/q4_monotonicity.py` (validated BdG instrument, M=400). *(script not committed to this repository; run on an external session machine — see the provenance note at the top of this file)*

The only surviving reading of ΔI ≡ c was the monotonicity analogy. Tested locally:
the entropic/MI c-function is monotone non-increasing along the mass flow for every
mass (critical 0.52→0.29 plateau decay; h=1.05/1.2/1.5 collapse to 0 past ξ; all YES;
all_mono=True). So "ΔI plays the role of c, monotone along a flow" holds — but only
under the **MI reading (c)**, where it is the Casini–Huerta entropic c-theorem
(monotone by strong subadditivity, a theorem), not a novel conjecture. The framework's
**literal** ΔI = TE(F→G)−TE(G→F) (reading b) cannot furnish it: transfer entropy is
undefined on a static, time-translation-invariant ground state and vanishes by symmetry
on a symmetric bipartition.

**Q4 fully closed.** Every reading accounted for: the conjecture ΔI ≡ c is FALSE/
ill-defined under the framework's own TE-asymmetry definition, or a RESTATEMENT of an
established theorem (Casini–Huerta) under the MI definition. No reading is both novel
and true. Tier: T1 (numerical monotonicity across masses) + T2 (the theorem, and the
TE-undefined-on-static argument). Highest-collapse target retired.

### 2026-06-06 — Target Q3 (d,q) scaling law — **FALSIFIED (T4)** — the degree dependence is wrong
### (LMFDB unreachable from sandbox; zeros COMPUTED directly instead — better: reproducible)

Code: `q3_scaling_test.py` *(script not committed to this repository; run on an external session machine — see the provenance note at the top of this file)* (mpmath Dirichlet L zeros + ζ zeros; genuine degree-2 L-function
built as the Dedekind zeta of Q(i) = ζ·L(χ₋₄), conductor q=4).

Earlier Q3 was SURVIVED-scoped: only the d=1,q=1 point (ζ) was testable, and the floor
2πe was an analytic invariant there. The substantive claim — that T_min scales as
(2πe)^d/q — needed d>1. Now computed and **falsified**:

| L-function | d | q | framework (2πe)^d/q | standard 2πe·q^(−1/d) | N_actual at framework floor |
|---|---|---|---|---|---|
| L(χ₋₄) | 1 | 4 | 4.27 | 4.27 | 0 (first zero 6.02) |
| L(χ₃) | 1 | 3 | 5.69 | 5.69 | 0 (first zero 8.04) |
| **Dedekind ζ Q(i)** | **2** | **4** | **72.93** | **8.54** | **51** |

At d=2 the framework floor (72.9) sits **above 51 actual zeros** — directly contradicting
the framework's own definition of T_min ("the height below which too few zeros exist to
resolve"). The framework count N(T)=(dT/2π)log(qT/(2πe)^d) predicts ≈0 zeros by T=72.9;
the truth is 51, and the standard analytic-conductor count (dT/2π)log(q^{1/d}T/(2πe))
correctly predicts ~50. The two formulas **coincide only at d=1**, which is precisely why
the ζ test survived — it is the degenerate case. **Mechanism:** the floor scales as
2πe·q^{−1/d} (standard), not (2πe)^d/q; the framework over-states the degree dependence,
overshooting the floor by ~8.5× at d=2.

**Verdict.** The floor *value* at d=1,q=1 (2πe) remains an analytic invariant (unchanged).
The *scaling law* T_min=(2πe)^d/q is **FALSIFIED (T4)** in its degree dependence — an
overclaim in LF01's T_min correction, surfaced exactly where the strip-mine predicted the
discriminator would be (d>1). Conductor (q) scaling at d=1 holds. Q3 closed.

---

### 2026-07-17 — EM-as-torsion-annihilator ("electromagnetism is the fundamental degradation") — **KILLED, both forms** · T1 machine / T4 falsified

Conjecture (stated before computation): the electromagnetic direction
Q = J3 + K3 + T_BL/2 is the unique direction in sl(4,R) annihilated by the
Palatini torsion sector — strong form against the full 9-dim sector
T = [Sym0(4), o(4)], weak form against the B−L vacuum direction alone.
Kill test: `code/acs_codebase/extras/test_conjecture_em_torsion_annihilator.py`
(exact rationals, no floats in any decision).

**Strong form KILLED.** T = Sym0(4) exactly (dim 9 = 9, containment verified),
and the centralizer of Sym0(4) in sl(4) is **{0}**: only multiples of the
identity commute with all of Sym0(4), and tracelessness removes those. The
full torsion sector annihilates *nothing* — no direction, EM or otherwise,
is a torsion-null residue of the full sector.

**Weak form KILLED.** Q (in the geometric J3+K3+T_BL/2 embedding) is **not**
in ker(ad_{T_BL}): its J3+K3 component carries the A(0,3) col-lep generator,
which T_BL moves. The kernel itself is the 9-dim sl(3)⊕u(1) block — so even
the diagonal-embedded photon (∝ T_BL) shares "torsion-null" with every colour
direction. Neither embedding gives uniqueness.

**Positive residue (the survivor, machine-verified exact).** The canonical
torsion-coupling operator C = Σ_a ad_{T_a}†ad_{T_a} (orthonormal torsion
basis, Frobenius metric) has **exactly two eigenvalues on sl(4)**:
**4** (multiplicity 9, the symmetric/torsion block) and **6** (multiplicity 6,
the o(4) Lorentz block). C is block-scalar: the only structure torsion
coupling resolves at the algebra level is the Palatini split itself. No
direction inside either block is graded, so **no algebra-level coupling
computation of this form can single out an electromagnetic residue
direction** — any "EM as degradation" mechanism must be sought in the
representation/embedding where charges act, not in the adjoint algebra.
That boundary is the space this kill collapses.

### 2026-07-17 — Condensate-as-collapse ("the slag of the furnace") — **SURVIVED, all four forms** · T1 machine / exact

Clarified conjecture (image/omega-limit dual of the killed F-6 kernel form):
matter/condensate is the COLLAPSED terminal output of the torsion flow, not
the protected base. Kill test:
`code/acs_codebase/extras/test_conjecture_condensate_collapse.py` (exact
rationals; four independently kill-able sub-claims, all stated first).

- **C1 SURVIVED** — ad_{T_BL} is semisimple over Q with exact spectrum
  {−4/3 (×3), 0 (×9), +4/3 (×3)}; every direction outside the exact 12-dim
  exceptional subspace V0⊕V− collapses projectively onto the 3-dim dominant
  sector V+. The terminal form is universal.
- **C2 SURVIVED** — V+ is abelian and nilpotent of order 2 (A·B = 0):
  the collapsed sector is terminal; it cannot regenerate structure.
- **C3 SURVIVED** — in the fermion fundamental 4, V+ consists EXACTLY of the
  three lepton→quark transition operators, and the collapse rate +4/3 equals
  the B−L charge transferred per transition (1/3 − (−1) = 4/3), exactly.
- **C4 SURVIVED** — the flow-invariant (uncollapsed) sector V0 is EXACTLY
  sl(3) ⊕ u(1)_{B−L}: the gauge structure is the furnace; it is never slag.

**Scope boundary (enforced in the script):** these are exact statements about
projective alignment of a linear hyperbolic flow on sl(4,R) and its action on
the fundamental 4. "Collapse" here is NOT decoherence/measurement; nothing is
established about physical spacetime or cosmology. The names correspond
structurally; the physics identification remains conjecture (T3 narrative at
best). What is locked: the flow sorts the algebra into gauge-invariant vs
matter-transitional sectors with the 4/3 = Δ(B−L) identity — machine-verified.

### 2026-07-17 — Hypercone-through-the-slice (projection picture) — **SURVIVED, all three forms** · T1 exact (C1,C2) / T3 measured (C3)

Picture: the 15-dim sl(4) cloud is the object; experience is a slice; a
higher-dimensional cone intersecting the slice is seen as evolving
spheroids/hyperbolae. Kill test:
`code/acs_codebase/extras/test_conjecture_hypercone_projection.py`.

- **C1 SURVIVED (exact)** — real 2-param slice x·D + y·S03 in the fermion
  4-rep has nonzero eigenvalue sheets exactly ±√(x²+y²): a true double cone.
  Any 1-param sub-slice sees the hyperbola 2√(t²+g²) — the cone poking
  through, apex off-slice. Degeneracy codim 2 → β = 1 class.
- **C2 SURVIVED (exact)** — adding the chirality direction z·(i·A03) (the
  same i the J-map sl(3)→su(3) introduces, Prop 9.7) gives sheets exactly
  ±√(x²+y²+z²): degeneracy codim 3 → β = 2 class. The repulsion exponent
  is a DIMENSION COUNTER: β = codim − 1.
- **C3 SURVIVED (measured)** — the repo's 100k Riemann zeros, unfolded,
  give fitted small-spacing exponent **β = 2.019** (Poisson 0 / GOE 1 /
  GUE 2). The shadow carries the imprint of a codimension-3 conical
  structure — the complex/chirality class.

**Scope boundary (enforced in-script):** the cone is in parameter space,
not physical space. Not established: that 3-space is a slice of the cloud,
that the zeros are such an operator's spectrum (open problem #2 stands),
or anything about spacetime/matter. What is locked: β counts hidden cone
dimensions exactly, and the zeros' measured β ≈ 2 selects the chirality
class — consistent with, and giving countable content to, the projection
picture.

---

### 2026-07-26 — Möbius-screw: *Sl = 2* as the geometric origin of *g = 2* — **KILLED** · T2 structural / T1 numerical

**Target.** `papers/notes/Mobius_Screw_Electron.tex` §3.3 identifies the torus-framing
self-linking number of the (2,1) centerline, `Sl = p·q = 2`, with the tree-level Dirac
value `g = 2`, on the stated ground that `Sl = 2` "matches the 4π (two-turn) return of a
spin-½ frame." The note labels this a model identification, not a derivation. The kill
question: does the *value* 2 do any of the work?

**Instrument.** `code/framed_unknot/framing_transformer.py` — evaluates every stage of
the chain `γ → U → (Sl = Tw + Wr) → F: S¹→SO(3) → q: S¹→SU(2)`, and reads off the
holonomy `σ = q(4π)/q(0)`, which is `+1` when the frame lift closes after one circuit
and `−1` when it needs two. Control family: round circles with `n` framing twists
(`Wr = 0`, `|Sl| = n`), which measures the map `Sl → σ` directly rather than assuming it.

**Confirmed (not killed).** The note's geometry is sound. `T·U = 0` to 2.2e-16, so the
torus normal is a genuine framing; `Tw = −1.033761`, `Wr = −0.966239`, `Tw + Wr =
−2.000000`; and independently `Lk(γ, γ + 0.10a·U) = −2.000000`. `|Sl| = pq = 2` as
claimed. (Sign: the embedding as parameterised is left-handed. `Tw` and `Wr` separately
are *not* invariants — they move with `a/R` — only the sum is.)

**Also confirmed.** The frame loop *is* spinorial: `σ = −1`, nontrivial in
`π₁(SO(3)) = ℤ/2`, proved in closed form from the quaternion lift
`q(φ) = [cos(φ/2) + k sin(φ/2)][cos(φ/4) − j sin(φ/4)]`, `q(4π) = (1)(−1) = −1`, and
confirmed numerically three independent ways. The model does land on the spinorial side
of a genuine invariant.

**The kill.** For torus curves the longitude half-angle advances by `πp` and the meridian
half-angle by `πq`, so `σ = (−1)^(p+q)`; with `Sl = pq` and `gcd(p,q) = 1` this is
equivalently `σ = (−1)^(Sl+1)`. The control family reproduces it exactly:

| n | Sl | σ | class |
|---|----|---|-------|
| −2 | +2 | −1 | spinorial |
| −1 | +1 | +1 | trivial |
| 0 | 0 | −1 | **spinorial** |
| 1 | −1 | +1 | trivial |
| 2 | −2 | −1 | spinorial |

**The `Sl = 0` row is the kill.** An ordinary round circle with an untwisted framing is
spinorial in precisely the same sense as the Möbius screw with `|Sl| = 2`. The
spin-relevant content of the self-linking number is one bit — its parity — and `2` and
`0` are the same bit. The value 2 therefore carries no spin information that 0 does not,
and cannot be what produces the double cover. **Mechanism of the error:** matching the
integer 2 across two formalisms in which it arises for unrelated reasons (`pq` on one
side, the order of `π₁(SO(3))` on the other).

**Independent corroboration (literature).** The parity law is not our result — it is
standard. Needham (arXiv:1708.09124 §2.2, Thm 3.7) states that framed-loop space has two
path components distinguished by self-linking parity, via the SU(2)→SO(3) double cover,
and his `h + k` even criterion reproduces our control column exactly at `h = 1`. Gompf &
Stipsicz §5.6–5.7 give the Kirby-calculus form (even framings → bounding spin structure,
odd → non-bounding). Our normalization convention is the standard trap and matches: with
the adapted frame `[T, U, T×U]` and Seifert reference, the 0-framed round unknot *is* the
generator of π₁(SO(3)). **Convention-free statement, which is what should be quoted:**
incrementing the framing by 1 flips the class; framings differing by 2 are equivalent.

**The decisive external point.** Lévy-Leblond, *Nonrelativistic particles and wave
equations*, Comm. Math. Phys. **6** (1967) 286, derives `g = 2` from **linearizing the
Schrödinger equation** — it is a consequence of the spinor representation, neither
relativistic nor topological in origin. A literature sweep found **no** peer-reviewed
derivation of `g = 2` from a framed loop, ribbon, or self-linking structure anywhere in
the mainstream record. The nearby speculative work does not fill the gap: Bilson-Thompson
states outright that his braided-preon model does not explain the origin of spin (twist
encodes charge); Battey-Pratt & Racey (1980) is effectively uncited outside fringe
literature; Schiller's strand model has no independent uptake. Note also that
"half-integer hopfion"/"fractional skyrmion" in the 2024–26 condensed-matter literature
means half-integer *topological index*, not half-integer *angular momentum*, and is not
precedent. The genuine "linking number → fractional spin" result is Wilczek & Zee,
PRL **51** (1983) 2250, which produces a phase and a statistics sector — not a
gyromagnetic ratio.

**Verdict.** `Sl = 2 ↔ g = 2` as a *geometric origin* claim is **FALSIFIED (T4)**. The
surviving statement is narrower and real: the model's double cover comes from the **odd
meridian winding q = 1** — the `φ/2` half-angle in the parameterisation — not from the
product `pq`. That is a ℤ/2 statement and cannot by itself yield a magnitude, so any
successor claiming a value for `g` needs a mechanism this does not supply. Suggested
successor target: compute the current distribution on the ribbon and its magnetic moment
against the angular momentum, which would produce a dimensionful `g` that can then fail.

Full write-up: `papers/notes/Framing_Transformer_Spin_Parity.tex`.
Artifact: `docs/framed_unknot_results.json`.

---

### 2026-07-26 — Successor test: can the framed-loop geometry produce a g-factor? — **KILLED (g = 1)** · T2 structural / T1 numerical

**Target.** The successor proposed when `Sl = 2 ↔ g = 2` was killed: stop matching
integers, compute the shape's magnetic moment against its angular momentum, and get a
dimensionful `g` that can fail. Prompted by the reading of the shape as a **dynamo**.

**Instrument.** `code/framed_unknot/moment_ratio.py` · artifact
`docs/framed_unknot_moment_ratio.json`.

**Result.** For a charge `q` and mass `m` circulating the closed centerline with period
`T`, both moments are proportional to the same vector area `A = ½∮ r × dl`:

```
mu = I·A = (q/T)·A          <L> = (m/T)·∮ r × dr = (2m/T)·A
mu / <L> = q/2m       =>    g = 1   exactly, for every closed curve
```

| curve | A_z / π |
|---|---|
| Möbius screw (2,1), a/R = 0.30 | +2.09000 |
| Möbius screw (2,1), a/R = 0.70 | +2.49000 |
| Möbius screw (2,1), a/R = 0.97 | +2.94090 |
| round circle, one turn | +1.00000 |
| round circle, two turns | +2.00000 |

**The double winding is real and it is useless.** The screw carries 2.09× the vector area
of a single loop — but that factor enters `mu` and `<L>` identically and cancels. This is
the *same failure mode* as the `Sl` kill one entry above: a genuine factor of 2 in the
geometry that carries no information about `g`. Note also that `A_z` is not an invariant
(2.09π → 2.94π across the throat sweep), unlike `Sl`, which does not move.

**Verdict.** **T2 no-go:** no model with charge and mass circulating at uniform `q/m` can
give `g ≠ 1` by geometry — whatever the winding, framing, twist, or throat. Eq. (g=1) is
just the classical orbital g-factor, which is shape-independent. This closes the successor
as posed.

**What it opens.** The requirement is now specific and structural rather than numerical:
**decouple where the charge sits from where the mass sits.** That is a far better-posed
target than hunting a 2 in the geometry. (The Möbius-screw note's own `e/2`-per-sheet
charge assignment is exactly such a knob — though §4.2 of that note already records that
the α estimate built on it does not survive its own revision path.)

**On the dynamo reading.** One part is a theorem, not an analogy: for a thin flux tube of
flux Φ, magnetic helicity `H = ∫A·B = Φ²(Tw + Wr) = Φ²·Sl` (Moffatt 1969; Moffatt & Ricca,
Proc. R. Soc. A **439** (1992) 411). So the Călugăreanu quantity *is* the helicity of this
geometry, and stretch-twist-fold dynamo action is exactly the `Tw ↔ Wr` trade already
plotted. Two things block it as a particle model, neither topological: **(i)** a dynamo
grows — it has a growth rate and consumes kinetic energy from a flow, while a stable
particle is stationary; **(ii)** since `H = Φ²·Sl`, it supplies the same integer we
already had, in units of Φ², adding physical content but no magnitude. The stationary
neighbour is the **force-free / Taylor state** (Woltjer: relaxation at fixed helicity to
∇×B = λB — a spheromak), which is the right dynamical class and whose λ does carry
dimensions of inverse length. It still does not evade the no-go on its own.

Write-up: `papers/notes/Framing_Transformer_Spin_Parity.tex` §§7–8.

---

### 2026-08-29 — Constraint Projection Framework: "zero free parameters, all constants from one non-orientable surface" — **KILLED, every load-bearing claim** · T1 machine / T2 structural / T4 falsified

**Target.** A submitted manuscript, archived as
`papers/notes/Constraint_Projection_Framework.tex`, claiming a zero-free-parameter
topological derivation of `alpha`, `g`, `s`, the dark-matter density, cosmological
flatness (via RH) and the Hubble radius from a single non-orientable surface `M`
with `w_1 != 0`, double cover `T^2`, and `Sl = 2`. The manuscript closes "the ledger
is sealed." It swings directly at this program's own load-bearing claims, two of
which are already entries below, so it is a high-collapse target at low cost.

**Instrument.** `code/constraint_projection/cpf_audit.py` — eight checks (C1–C8),
each written so the manuscript could pass it. Artifact
`docs/constraint_projection_audit.json`. Full write-up:
`papers/notes/Constraint_Projection_Framework_Audit.tex`.

**C1 — the alpha derivation fails its own algebra.** From the manuscript's three
stated inputs — `C_M = 2 pi eps0 R / L` with `L = ln(8R/a)+1`, the match
`(e/2)^2/(2 C_M) = m_e c^2`, and `R = hbar/(2 m_e c)` — sympy returns `L * alpha = 2`,
i.e.

```
alpha^-1 = (1/2)(ln(8R/a) + 1)        NOT   ln(8R/a) + 1
```

**This correction is already in the repository.** It is eq. `(alpha_ann)` of
`papers/notes/Mobius_Ribbon_Capacitance.tex` (2026-07-22), which also records the
CODATA-matching aspect `a/R = 8 exp(1 - 2 alpha^-1) ~ 2.04e-118` — recomputed here at
60 digits as `2.03905e-118`, an exact match. The manuscript reproduces the parent
note's *uncorrected* form and its `137.036`, citing neither the correction nor the
conformal/BIE revisions that returned `alpha^-1 = O(1)` at moderate aspect.

Separately, the step `a/R = 8 exp(-136.035999171)` => `alpha^-1 = 137.035999171` is an
identity — `ln(8/(8 e^-x)) + 1 = x + 1` for any `x`. The target is inserted in the
premise. The asserted mechanism (G-field eigenvalue gap, GQRE renormalization) is
stated with no computation, and the GfE G-field is *algebraically constrained*, so a
discrete UV spectrum does not follow from that action without further input.

**C2 — the kill: one parameter, four incompatible values, 117 decades apart.** The
manuscript's "zero free parameters" rests on "the cutoff `a` is not free." It places
four requirements on `a`, at `R = hbar/(2 m_e c) = 1.9308e-13` m:

| constraint (source) | a/R | alpha^-1 (corrected) | L_IR = R^2/a [m] |
|---|---|---|---|
| `tau = i a/R = i/2` (§3) | 5.00e-1 | 1.886 | 3.9e-13 |
| `a/R = 8 exp(-136.036)` (§3) | 6.66e-59 | 68.518 | 2.9e+45 |
| CODATA match on the corrected relation | 2.04e-118 | 137.035999177 | 9.5e+104 |
| `L_IR = 1.3e26` m (§8) | 1.49e-39 | 46.242 | 1.3e+26 |

§3 contradicts itself internally: `tau = i/2` gives `a/R = 1/2`, five lines before
`a/R = 6.7e-59` — 58 decades apart, and `a/R = 1/2` returns `alpha^-1 = ln 16 + 1 =
3.77`. The alpha leg and the L_IR leg cannot both run: the manuscript's own `a` puts
L_IR 19 decades past the Hubble radius, the corrected `a` puts it 79 decades past, and
forcing L_IR gives `alpha^-1 = 46.24`. **"UV complete" also fails:** the `a` the
corrected relation needs is `3.94e-131` m, i.e. `1e-96` Planck lengths.

**Verdict on the headline: the framework has exactly one free parameter, `a/R`,
fitted separately in §3 and §8.** The Appendix-B parameter table is wrong as stated,
and the comparison to the SM's 19 is not like-for-like — no mass, no mixing angle
and no coupling other than alpha is produced.

**C3 — Axiom III has no model (the structural kill).** Clauses (1)–(2) —
closed, non-orientable, `w_1 != 0`, double cover `T^2` — force `M = Klein bottle
K = T^2/<tau>`, `tau(x,y) = (x+1/2, -y)`, uniquely; that much is correct. Clause (3)
asks for `phi in Diff(M)` with `phi_* = [[1,2],[0,1]]`. Any diffeo of `K` lifts to
`T^2` and must normalise the deck group `{1, tau}`; that group is `Z/2`, so
normalising means commuting. On `H_1(T^2) = Z^2` the linear part of `tau` is
`D = diag(1,-1)`, and exact integer arithmetic gives:

```
[M, D] = 0  =>  M diagonal  =>  centraliser = {diag(+-1, +-1)} ~ Z/2 (+) Z/2, order 4
                                (agrees with Lickorish 1963: MCG(K) = Z/2 (+) Z/2)
phi_*^n = [[1, 2n], [0, 1]]  =>  phi_* is parabolic of INFINITE order
phi_* D phi_*^-1 = [[1, -4], [0, -1]]  !=  D
```

A finite group has no element of infinite order, and `phi_*` does not commute with
`D` in any case. **No such `phi` exists.** The weaker reading fails too: within the
centraliser the available traces are `{+2, -2, 0, 0}` and `+2` is attained *only by
the identity*, which is not a Dehn twist and supplies no self-linking number. So
`Tr(phi_*) = 2 = Sl` has no carrier under either reading, and everything downstream
of it — `tau = i/2` (§3), `g` and `s` (§4), `lambda_UV lambda_IR = 1/R^4` (§8) —
rests on an axiom no surface satisfies.

Second, independent obstruction in §3: the Klein bottle admits **no embedding in
R^3**, only immersions with self-intersection, so the "double-cover annulus" whose
capacitance §3 computes does not exist. `K` is also closed and has no boundary. The
formula actually used is the thin-ring one, whose `ln(8R/a)` is the Kelvin–Maxwell
ring *inductance* log; its additive constant there is `-7/4` or `-2`, never `+1`.

**C4 — §4 restates two kills logged below on 2026-07-26, without reference.**
`g = Sl = 2` was killed by the parity law `sigma = (-1)^(Sl+1)`: the `Sl = 0` round
circle is spinorial in the same sense, so the content of `Sl` is one parity bit and
the value 2 does no work. The magnitude route was then closed by a T2 no-go:
`mu` and `<L>` share the same vector area, so `g = 1` exactly for every closed curve.
The manuscript reproduces the *original mechanism of the error* — matching the
integer 2 across formalisms where it arises for unrelated reasons — and now adds a
third unrelated 2, the trace of a parabolic. Three further errors: the repo's own
computation gives `Tw + Wr = -2.000000`, so `s = Sl/4` would give `s = -1/2`; a
`(p,q)` torus knot with `q = 1` is the **unknot**, as the parent note already
corrects; and the `4` in `s = Sl/4` is nowhere derived — Finkelstein–Rubinstein
yields a `Z/2` sector, not a magnitude, which is exactly the gap that killed the
claim the first time.

**C5 — §7's curvature functional cannot see an off-line zero.** Three independent
failures of `k(eps) = 2 eps SUM_rho 1/((1/2-beta)^2 - eps^2)`:

1. **Blind by construction.** `beta` enters only through `(1/2 - beta)^2` — exactly
   the invariant of the functional equation's involution `beta -> 1 - beta`. Since
   zeta's zero set is symmetric under that involution, every off-line zero arrives
   with a mirror partner contributing identically. Numerically, 50 zeros at
   `eps = 0.1`: `beta = 0.5 + 0.2` and `beta = 0.5 - 0.2` both give `k = +333.33`.
   The functional cannot distinguish RH from its negation.
2. **Inverted sign.** On the critical line every summand is `-1/eps^2`, not 0, so
   `k = -2N/eps` for `N` on-line zeros — divergent as `N -> oo`, zero for no finite
   `eps`. RH makes `k` maximally divergent; the criterion points the wrong way.
3. **Empirical direction.** `Omega_k = 0.0007 +- 0.0019`; no measurement establishes
   an exact zero. A biconditional makes a theorem of arithmetic contingent on CMB
   data, and would let a future curvature detection refute RH.

Repo rule 7 stands: RH is nowhere claimed proved here. §7 claims an *equivalence*,
which is a proof claim in both directions. The corpus's defensible statement remains
Paper B's — RH => stationarity proved by AM–GM, converse conditional on an unproved
minimum-gap bound verified only to N = 200.

**C6 — §5 SURVIVES arithmetically, fails on identification.** `S = 2 sqrt 2 =
2.8284271247` at Tsirelson saturation, confirmed to machine precision (**T3**). This
is the one displayed number in the manuscript that survives its own computation. But
only settings `{2,3}` appear on either wing: the friend setting `x=1 / y=1` enters no
term. With two settings per wing this **is CHSH**, whose local bound is 2 for
CHSH reasons, not observer reasons — so §5 demonstrates ordinary Bell nonlocality
(measured since 1982), not a Local Friendliness violation. Bong et al.'s LF facets
involve the `x=1` row precisely because that is where AOE enters. "Falsifying AOE"
also overstates even a genuine LF violation, which falsifies the **conjunction** of
AOE, Locality and No-Superdeterminism. The `C_6/D_6` axial frame and the
super-observer structure are inert — neither appears in the algebra producing
`2 sqrt 2`.

**C7 — §6's dark matter double counts and needs an exotic scalar.** With
`psi = R e^{iS/hbar}` the split is exact:

```
(hbar^2/2m)|grad psi|^2 = hbar^2 R'^2/(2m)  +  R^2 S'^2/(2m)
                                               ^^^^^^^^^^^^^^ = (1/2) rho v^2
```

The second term is the visible matter's own kinetic energy density, which
`T_00 = rho_vis c^2 + rho_DM c^2` then counts a second time as dark. The `Re/Im`
story is also wrong: `|grad psi|^2` is not a function of `Im(psi)` alone, and the
split is not gauge invariant — a global U(1) phase rotates one into the other; EM
couples through the covariant derivative. **The scale is decisive:** quantum pressure
shapes a rotation curve only when `lambda_dB` is galactic, requiring
`m ~ 1.7e-59 kg = 9.6e-24 eV/c^2` — the fuzzy-dark-matter window, i.e. an ultralight
scalar, which is exactly the "exotic particle" §6 claims to avoid. At `m_e`,
`lambda_dB = 5.8e-10` m, 29 decades too short-ranged. The claim fails either way. No
Jeans solution, rotation curve or dataset appears; "matching observations" is
asserted.

**C8 — Axiom I is false; Axiom II is ill-posed; two citations are wrong.**
`A_Q/Q^x` is malformed (`Q^x` is multiplicative and does not act on the additive
adeles by translation). Both standard readings — `A_Q/Q` and the idele class group
`A_Q^x/Q^x` — are **abelian, hence amenable** (Markov–Kakutani), and `A_Q/Q` is
compact, carrying a translation-invariant Haar *probability* measure. The axiom
asserts no finitely additive translation-invariant probability measure exists; that
is false under every reading, and non-amenability is load-bearing for the "non-amenable
information reservoir" framing. Axiom II maps onto `R^{3,1}` but `delta^(3)` fixes
only three coordinates — nothing supplies the time direction — and a 2-parameter
integral against a 3-dimensional delta is generically distributional, so "Fredholm"
is not established. Citations: `arXiv:2401.12345` is a placeholder (Bianconi,
"Gravity from entropy," is `arXiv:2408.14391`, Phys. Rev. D **111**, 066001 (2025));
"Tiesinga et al., Rev. Mod. Phys. **94**, 035002 (2023)" matches no CODATA article of
record (CODATA 2018 = RMP **93**, 025010 (2021); CODATA 2022 = Mohr, Newell, Taylor &
Tiesinga, RMP **97**, 025002 (2025), `alpha^-1 = 137.035999177(21)`). Proietti 2019
and Finkelstein–Rubinstein 1968 check out.

**Verdict.** **FALSIFIED (T4) on every load-bearing claim.** One displayed number
survives its own computation — `S = 2 sqrt 2` — and it is CHSH. The remainder fails
its own algebra (C1), fits the one parameter it denies having four different ways
(C2), rests on an axiom with no model (C3), restates two logged kills (C4), inverts
its own Riemann criterion while being blind to the functional equation (C5),
double counts (C7), or is false as stated (C8).

**What survives, narrowly.** `M = Klein bottle` from clauses (1)–(2) is correct and
unique — the one piece of topology in the paper that does what it claims; clause (3)
is what fails. `S = 2 sqrt 2` is a correct computation of a known quantity.

**What it opens.** Nothing new: each repair path leads back to a successor question
already on the board. The `g` leg needs the standing successor — *decouple where the
charge sits from where the mass sits* — and no framing, twist or trace-matching
substitutes for it. §7's leg yields one genuinely new structural constraint worth
recording: **a functional that detects off-line zeros must be ODD under
`beta -> 1 - beta`.** Any construction whose `beta`-dependence factors through
`(1/2 - beta)^2` is blind for the same reason, so this bounds a class rather than a
single attempt.

**On the framing.** The manuscript's closing "the ledger is sealed" inverts this
program's discipline. The Elimination Ledger is append-only precisely so that it is
never sealed. A framework declaring zero free parameters while fitting one parameter
four ways, and declaring completeness while restating falsified results, is the
failure mode this corpus names as primary: **overclaiming**.

Full write-up: `papers/notes/Constraint_Projection_Framework_Audit.tex`.
Instrument: `code/constraint_projection/cpf_audit.py`.
Artifact: `docs/constraint_projection_audit.json`.

---

### 2026-08-29 — CPF second pass: full verification — **TWO OF OUR OWN VERDICTS CORRECTED (both understated)** · T1 machine / T2 proved

**Why this entry exists.** The kill logged immediately above settled three of its eight
checks by structural argument rather than computation. Tier honestly: (b) structural
must never wear (a) recomputable's clothes. This pass computed all of them
(`code/constraint_projection/cpf_full_verification.py`, V1–V9, artifact
`docs/constraint_projection_full_verification.json`). Two verdicts moved. Both moved
**against** the manuscript — the earlier readings were too generous, not too harsh —
and both are corrected in place in the audit note with the earlier reading stated.

**CORRECTION 1 (V6) — the EWFS section fails harder than we said.**
The first pass wrote: "no friend setting appears; it is CHSH, whose local bound is 2."
True, but it compares against the wrong polytope. Computing the actual Local
Friendliness bound by linear programming:

```
local (Bell/CHSH) bound      = 2.0000000000
quantum value (Tsirelson)    = 2.8284271247
LOCAL FRIENDLINESS bound     = 4.0000000000   <- all four (a1,b1) branches
no-signalling bound          = 4.0000000000
```

LF (Bong et al.) is `p(ab|xy) = SUM_lam q(lam) p_lam(ab|xy)` with each `p_lam`
no-signalling and `p_lam(a|x=1)`, `p_lam(b|y=1)` deterministic. Maximising a linear
functional over a convex hull = maximising over the generators, so the LF bound is the
max of four LPs. All four return exactly 4.

The structural reason: the manuscript's sum contains no `x=1` or `y=1` term, and **any**
no-signalling behaviour on `{2,3}x{2,3}` extends to a full LF behaviour (take
`a1=b1=+1` and the product form `delta(a,+1) q_B(b|y)` on the mixed rows). So the LF
polytope's projection onto that block is the *full* no-signalling polytope.

**Consequence: `S = 2 sqrt 2 = 2.828 < 4`. The manuscript violates NO Local Friendliness
inequality**, and by Tsirelson no quantum state or measurement could make that
expression do so. Its "`> 2`" is the Bell local bound. So §5 does not merely prove
something weaker than claimed — it proves nothing about AOE at all, and could not.
**T4, strengthened.**

**CORRECTION 2 (V5) — we never evaluated §7's defining integral.**
The first pass tested only the claimed *sum*. The manuscript's actual definition is

```
k(eps) = lim_{T->oo} (1/T) INT_0^T [ zeta'/zeta(1/2+eps+it) - zeta'/zeta(1/2-eps+it) ] dt
```

Residue theorem on the rectangle `1/2-eps .. 1/2+eps, 0 .. iT`: the pole of zeta at
`s=1` is outside for `eps < 1/2`; the poles of `zeta'/zeta` inside are exactly the zeros
with `0 < gamma < T`. The vertical sides give `i I(T)`, so
`i I(T) + INT_bot + INT_top = 2 pi i N(T)`, hence
`I(T) = 2 pi N(T) + i(INT_bot + INT_top)` with `INT_bot` an O(1) real constant and
`INT_top = O(log T)`. Therefore

```
(1/T) I(T)  ->  2 pi N(T)/T  ->  log(T / 2 pi e)  ->  +infinity
```

**real, positive, eps-INDEPENDENT, and divergent.** Confirmed numerically (mpmath,
contour split at the zero ordinates):

| T | eps | N(T) | Re[(1/T)I] | 2 pi N(T)/T | ratio | claimed −2N/eps |
|---|-----|------|-----------|-------------|-------|-----------------|
| 20 | 0.10 | 1  | 0.323180 | 0.314159 | 1.0287 | −20 |
| 20 | 0.25 | 1  | 0.336315 | 0.314159 | 1.0705 | −8 |
| 40 | 0.10 | 6  | 0.946835 | 0.942478 | 1.0046 | −120 |
| 40 | 0.25 | 6  | 0.953112 | 0.942478 | 1.0113 | −48 |
| 60 | 0.10 | 13 | 1.359827 | 1.361357 | 0.9989 | −260 |
| 60 | 0.25 | 13 | 1.357772 | 1.361357 | 0.9974 | −104 |
| 80 | 0.10 | 21 | 1.645536 | 1.649336 | 0.9977 | −420 |
| 80 | 0.25 | 21 | 1.640179 | 1.649336 | 0.9944 | −168 |

Ratio → 1; `Re[(1/T)I]` agrees across `eps` to under 1%; `Im[(1/T)I]` → 0 as the
boundary terms die. At `T=80, eps=0.1` the computed value is **+1.6455** against a
claimed **−420**: opposite sign, factor 255.

**So the Guinand–Weil step is simply wrong, independently of the blindness argument**
(which stands: the claimed summand depends on `beta` only through `(1/2-beta)^2`, the
invariant of the functional equation's involution).

**Worth recording for its own sake:** what the manuscript's integral *actually*
computes is `log(T/2 pi e)` — the **Riemann–von Mangoldt smooth counting term**, which
this repository already reproduces independently
(`src/paper_b/berry_keating_counting.py`, T2(known)). The object is correct and
standard; it is not the object §7 says it is, and it converges to nothing.

**ADDITION (V7) — the dark-matter term is not the quantum potential.**
Not previously checked. The Madelung/Bohm "quantum pressure" that shapes a rotation
curve in every wave-dark-matter model is `Q = -(hbar^2/2m) (grad^2 R)/R`, an energy per
particle that may be negative. The manuscript's `(hbar^2/2m)|grad psi|^2` is a
positive-definite energy *density* built from `R'^2`, not `R''/R`. Different objects:
**§6 does not use the mechanism it names**, on top of double counting `(1/2) rho v^2`
and needing `m ~ 9.6e-24 eV`.

**Everything else held, and is now machine-verified rather than argued:**

- **V1** — Euler-characteristic census (`chi(N_k) = 2-k`, cover genus `h = k-1`, so
  `h=1` only at `k=2`) plus Smith normal form on the CW complex of `K`
  (`H_2 = 0`, `H_1 = Z (+) Z/2`). Clauses (1)–(2) of Axiom III are **correct and
  unique**. Minor: `H_2 = 0` holds for every closed non-orientable surface, so that
  clause is implied by `w_1 != 0` and adds nothing.
- **V2** — exhaustive search over **390,625** integer matrices (`|entries| <= 12`,
  `det = +-1`) confirms the centraliser of `D = diag(1,-1)` has order exactly 4,
  `Z/2 (+) Z/2`, traces `{-2, 0, 0, +2}`, with `+2` attained only by the identity.
  `phi_*` is not in it. **Axiom III unsatisfiable, exhaustively.**
- **V3** — `L * alpha = 2` symbolically; dimensional audit passes (the error is a
  dropped *number*, not a units slip); and a **circularity sweep** shows
  `a/R = 8 exp(-(X-1)) => alpha^-1 = X` for every target tried, including `X = 42`,
  `X = 1000` and `X = -7`. The step carries no information. Provenance: the standard
  thin-ring capacitance is `4 pi^2 eps_0 R / ln(8R/a)` — the manuscript's prefactor
  (`2 pi`) and additive constant (`+1` vs `0`, `-7/4`, `-2`) match nothing, and
  `d(alpha^-1)/d(const) = 1/2` makes the constant a second free knob.
- **V4** — the four-cutoff table reconfirmed at 50 digits, spread **117.4 decades**.
  Added: `Lambda_eff = 1/L_IR^2 = 5.917e-53` vs `Lambda_obs = 1.091e-52` m^-2, ratio
  1.84 — a factor-2 match is automatic for any `L_IR ~ c/H_0`, so it restates the input.
- **V8** — Folner sequences computed on `Z` (`|F_n sym (F_n+g)|/|F_n| -> 0`). Every
  abelian group is amenable; `A_Q/Q` is compact abelian with a Haar probability
  measure; the idele class group is abelian; `A_Q/Q^x` as literally written is
  undefined. **Axiom I false under every reading.**
- **V9** — the prior kills were **re-executed, not cited**:
  `framing_transformer.py` returns `Tw + Wr = -2.000000`, `sigma = -1` three ways, and
  the control row `Sl = 0 -> sigma = -1` (same class as `Sl = 2`);
  `moment_ratio.py` returns `g = 1.000000` exactly. Both artifacts regenerated
  byte-identically (no git drift).

**Verdict unchanged in direction, sharpened in degree: T4 on every load-bearing claim.**
The surviving items are `M = Klein bottle` (V1) and the arithmetic value `S = 2 sqrt 2`
(V6) — the latter now known to be a correct computation of a quantity that cannot bear
the weight §5 puts on it.

**Method note for the ledger.** Both corrections came from computing a step the first
pass had reasoned about instead of running. Both made our own verdict stronger, which
is the less dangerous direction but not a safe one: an audit that understates is still
an audit that was not run. The rule that produced them is worth keeping — **evaluate
the object the target actually defines, not the object it claims that object equals.**

Full write-up: `papers/notes/Constraint_Projection_Framework_Audit.tex` (revised).
Instrument: `code/constraint_projection/cpf_full_verification.py`.
Artifact: `docs/constraint_projection_full_verification.json`.

---

### 2026-08-30 — Successor to the `Sl = 2 <-> g = 2` kill: run Lévy-Leblond, then read the anomaly — **SUCCESSOR CLOSED; NEW EXPERIMENTAL KILL ON CPF COMPLETENESS** · T1 machine / T2(known) / T4 falsified

**Why.** The 2026-07-26 kill closed on Lévy-Leblond (Comm. Math. Phys. **6** (1967) 286)
as "the decisive external point": `g = 2` follows from **linearizing the Schrödinger
equation**, so it is neither relativistic nor topological in origin. The repository has
cited that result for a month without ever running it. Cited-not-run is exactly the
tiering failure this ledger exists to catch. Instrument:
`code/constraint_projection/wave_equation_gfactor.py`, artifact
`docs/wave_equation_gfactor.json`.

**W1–W3 — `g = 2` derived, machine-checked, from `su(2)` alone.**

```
sigma_i sigma_j = delta_ij + i eps_ijk sigma_k          verified, all 9 ordered pairs
[pi_i, pi_j] = i q hbar eps_ijk B_k,  pi = p - qA
(sigma.pi)^2 = pi^2 - q hbar (sigma.B)                  verified with NON-commuting pi
E phi + (sigma.p) chi = 0,  (sigma.p) phi + 2m chi = 0  Levy-Leblond
  => E phi = (sigma.p)^2 phi/(2m) = p^2 phi/(2m)        free Schrodinger
  => minimal coupling + Pauli identity gives spin term -(q hbar/2m)(sigma.B)
  => match  H = -mu.B,  mu = g(q/2m)S,  S = (hbar/2)sigma
  => g = 2
```

**No `c`, no Lorentz transformation, no metric, no light cone** appears anywhere in that
chain. It is a Galilean theory throughout. The whole factor of 2 lives in the single
identity `(sigma.pi)^2 = pi^2 - q hbar (sigma.B)`.

**W4 — `4 pi` periodicity needs a group, not a surface.** `exp(-i(2pi) sigma_z/2) = -I`,
`exp(-i(4pi) sigma_z/2) = +I`: the nontrivial element of `pi_1(SO(3)) = Z/2` acting in the
spinor rep. The CPF manuscript's §4 derives the same `4 pi` from "non-orientability of
`M`" — a longer route to a fact `su(2)` already supplies, and (per the audit) one whose
Axiom III has no model.

**W5 — `g = 2` does not diagnose relativity either.** Squaring the Dirac operator gives
the same Pauli term and the same tree-level 2. Galilean and Lorentzian theories agree
exactly here. What separates frameworks is the **anomaly**.

**W6 — read the data as it lies.**

```
g/2 measured = 1.00115965218059(13)     Fan, Myers, Sukra & Gabrielse, PRL 130, 071801 (2023)
a_e          = 1.15965218059(13) e-3    0.13 ppt
a_e from any 'g = 2 exactly' framework = 0
separation   = 8.92e9 sigma
```

`g = 2` matches to three decimal places and diverges at the fourth.

**W7 — the QED series, and a mistake caught by inverting it.** The first run of this
comparison omitted the **mass-dependent** terms (muon and tau vacuum-polarization
insertions, `A2(m_e/m_mu)`, `A2(m_e/m_tau)`), and separately compared against CODATA's
`alpha`, which is partly determined **by** `a_e` plus QED theory — circular. The omitted
terms total `2.75e-12`, about **20x the experimental uncertainty**, so a comparison
without them is invalid. The error surfaced not by inspection but by **inverting the
series for `alpha^-1`** and checking it against a published anchor:

```
this series + measured a_e  ->  alpha^-1 = 137.03599916622
Fan et al. quote            ->  alpha^-1 = 137.035999166(15)
agreement                   =   0.015 x their quoted uncertainty
```

**W8 — against independently measured `alpha`.** Rb (Morel 2020): residual `3.36e-13`,
**2.1 sigma**. Cs (Parker 2018): residual `-1.02e-12`, **-3.9 sigma**. Rb and Cs disagree
with *each other* at **5.5 sigma**. The dominant discrepancy in this sector is
**experimental**, not a failure of QED. *(Caveat: this uncertainty propagation is cruder
than a full CODATA adjustment; treat the per-source sigmas as indicative. The Cs figure
runs larger than the ~2.4 sigma usually quoted.)*

**W9 — the parameter count, which is the point.**

| framework | inputs | g | matches data to |
|---|---|---|---|
| Lévy-Leblond (Galilean) | `su(2)` + linearization | 2 exactly | 3 decimals |
| Dirac (tree) | `su(2)` + Lorentz | 2 exactly | 3 decimals |
| QED | `alpha` (measured) + loops | 2(1 + a_e) | 12 digits |
| CPF manuscript | Klein bottle + `Sl = 2` | 2 exactly | 3 decimals |

**NEW KILL — the completeness claim, falsified experimentally at 8.92e9 sigma.**
The prior entry killed `Sl = 2 <-> g = 2` as a *geometric origin* claim (the content of
`Sl` is one parity bit). This adds an independent, experimental kill of a *different*
claim: the manuscript's **completeness**. Lévy-Leblond and tree Dirac also stop at 2, and
that is no mark against them — neither claims to be finished, and QED continues the
series with an independently measured `alpha`. The manuscript claims **zero free
parameters, UV/IR completeness, and "all constants."** `Sl` is an **integer** and the
framework contains **no expansion parameter anywhere**, so it has no route to
`1.16e-3` at any order. The stop is therefore terminal, and it is terminal on the
manuscript's own headline observable. **T4.**

**What this closes and what it opens.** The successor question posed on 2026-07-26 —
"can the framed-loop geometry produce a g-factor?" — was answered *no* by the `g = 1`
no-go. This entry answers the complementary question: **what does produce it**, and the
answer is `su(2)` plus linearization, with zero geometric input. That removes the
motivation for the geometric route rather than merely blocking it. The standing successor
(**decouple where the charge sits from where the mass sits**) is unaffected and remains
the only known route past `g = 1`.

**Method note.** Second time in two days that a verdict was corrected by computing rather
than reasoning, and again the correction was found by **anchoring to an independent
published number** (here, inverting for `alpha^-1`) rather than by re-reading the
algebra. Companion to the rule logged 2026-08-29: *evaluate the object the target
actually defines*. Add: **anchor every series to a number someone else published.**

Instrument: `code/constraint_projection/wave_equation_gfactor.py`.
Artifact: `docs/wave_equation_gfactor.json`.

---

### 2026-08-30 — CPF triple-check: every load-bearing claim by ≥2 independent methods — **NO VERDICT MOVED; three had rested on one method** · T1 machine / T2 proved

**Why.** Two passes in two days each corrected a verdict that had been *reasoned about
rather than run*. That is a pattern, not a coincidence. This pass attacks every
load-bearing claim from methods that share no machinery, validates the instruments
before trusting them, and scales past toy sizes. Instrument
`code/constraint_projection/cpf_triple_check.py`, artifact
`docs/constraint_projection_triple_check.json`.

**Standing rule adopted: an instrument is not trusted until it has been shown capable
of FAILING.** X2 below exists because of it.

**X1 — MCG(Klein bottle), two methods sharing no machinery.**
*Method A* (already on record): diffeos lift to `T^2` and must centralise the deck
involution `D = diag(1,-1)`; exhaustive over 390,625 integer matrices → order 4.
*Method B* (new): `K` is aspherical, so `MCG(K) = Out(pi_1(K))`. Computed by symbolic
word algebra on `<a,b | b a b^-1 = a^-1>` in normal form `a^m b^n` — associativity,
identity, inverses and the relation all verified, then Aut enumerated
(`a -> a^e, b -> a^k b^d`, forcing `d` odd), Inn computed
(`conj_a = (1,1,2)`, `conj_b = (-1,1,0)`, so `Inn = {(e,+1,k even)}`), and
`Out = Aut/Inn` indexed by `d` and `k mod 2` → **order 4, `Z/2 (+) Z/2`**.
Its induced action on `H_1` of the cover `<a, b^2>` is exactly `{diag(+-1,+-1)}` —
**the same four matrices Method A found**, with `k` dropping out entirely (inner
automorphisms act trivially on the cover, as they must).

Method A never mentions `pi_1`; Method B never mentions the deck transformation or a
lift. `phi_* = [[1,2],[0,1]]` is absent from both. **Axiom III clause (3) fails under
two independent routes.**

**X2 — the LF instrument, validated before use.** The 2026-08-29 correction rested
entirely on my own construction of the LF polytope, built from the definition rather
than from the source paper. If that construction were too permissive, the correction
was worthless. Three validations, each able to fail:

| test | requirement | result |
|---|---|---|
| V-a | all 64 local deterministic vertices **inside** LF (LF is weaker than local causality) | PASS |
| V-b | a PR box on settings (1,2)×(1,2) **outside** LF (LF ⊊ NS, not vacuous) | PASS, slack 1.0 |
| V-c | **some quantum behaviour outside LF** (Bong et al.'s theorem) | **PASS**, slack `1.19615242` |

V-c is the decisive one. The maximum slack found over 40 Nelder–Mead restarts
(seed `20260423`) is `1.19615242 = 3 sqrt 3 - 4`, attained at the **maximally
entangled** state. So the construction does reproduce a genuine LF violation; it is
not too permissive.

Only then the bound, by **two** methods:
- LP over all four `(a1,b1)` branches → `4.0000000000`
- **exact rational certificate**: an explicit LF behaviour (`a1=b1=+1`, PR box on
  `{2,3}x{2,3}`, product form on the mixed rows) with normalisation, no-signalling,
  AOE-determinism and non-negativity all verified in `Fraction` arithmetic, attaining
  `S = 4` exactly. With `|E| <= 1` giving `S <= 4` trivially, **the maximum is exactly 4
  with no solver involved.**

Bell bound 2 (exhaustive over 64), Tsirelson `2 sqrt 2`. `2 < 2 sqrt 2 < 4`:
**Tsirelson caps any quantum realisation of this expression below the LF bound, so no
LF violation is reachable even in principle.** The 2026-08-29 correction stands, now
on validated instruments and exact arithmetic.

**X3 — Sec 7's integral, second method, 900× the scale.** Method A was mpmath
quadrature, feasible only to `T ~ 100`. Method B is an **exact closed form**: for real
`alpha`, `INT du/(alpha+iu) = arctan(u/alpha) - (i/2)ln(alpha^2+u^2)` with no
branch-cut crossing, so a zero at `beta = 1/2` sees `alpha = +eps` and `-eps`, the
imaginary parts (depending on `alpha^2`) **cancel identically**, and the real parts add:

```
contribution per zero = 2[ arctan((T-gamma)/eps) + arctan(gamma/eps) ]  ->  2 pi
```

for any `0 < gamma < T`. **That is the residue count, derived without invoking the
residue theorem.** Run over Odlyzko's 100,000 zeros:

| T | N(T) | Re[(1/T)I] | 2πN(T)/T | ratio | log(T/2πe) | Im |
|---|---|---|---|---|---|---|
| 100 | 29 | 1.819890 | 1.822124 | 0.998774 | 1.767293 | 8.2e-3 |
| 1000 | 649 | 4.076195 | 4.077787 | 0.999610 | 4.069878 | 1.1e-3 |
| 20000 | 22491 | 7.065708 | 7.065756 | 0.999993 | 7.065610 | 6.8e-5 |
| 74000 | 98625 | 8.373995 | 8.374043 | **0.999994** | 8.373943 | 2.0e-5 |

The ~2e-3 gap against Method A at `T <= 80` was chased down and is **the quadrature's
own error**, not a disagreement: the exact method converges upward and stabilises as
the zero window grows (1.642685 → 1.643660 from window 100 → 74,900).

Component decomposition at `T = 20000`: zero sum `141315.2568` vs `2 pi N(T) =
141315.1207` (edge/tail `0.136`, O(1)); pole term at `s=1` O(1) and non-growing; `psi`
term `O(eps log T)`. **After dividing by `T`, only `2 pi N(T)/T` survives** — the claim
verified piece by piece rather than in aggregate. And `eps`-independence at
`T = 20000`: computed value flat to `~3e-4` across `eps` from 0.02 to 0.40, while the
manuscript's claimed `-2N/eps` varies by 20× and is negative (`-2.2e6` to `-1.1e5`
against a computed `+7.0657`).

**X4 — `g = 2` by three structurally independent routes.**
*Route 1 (Galilean)*: the explicit 4×4 Lévy-Leblond operator
`M = [[E I, sigma.p],[sigma.p, 2m I]]` has `det M = (2Em - p^2)^2` — it squares to the
Schrödinger operator exactly — and rank 2 on shell, so a 2-dimensional kernel: the
spin-½ doublet. *Route 2*: square `sigma.pi` directly, no linearization. *Route 3
(Lorentzian)*: Dirac with the Clifford relations verified, eliminate the small
component. All three give `g = 2` and all bottom out in
`{sigma_i, sigma_j} = 2 delta_ij`. Route 1 uses no relativity, Route 3 no
linearization, Route 2 neither. **None uses a manifold, a framing, or a self-linking
number.**

**X5 — the α factor of 2, three sources.** (1) symbolic solve here → `L*alpha = 2`;
(2) the repository's own published `eq. (alpha_ann)` from July 2026; (3) the repo's
**independent numerical instrument** `code/capacitance_ribbon/ribbon_capacitance.py`
(boundary-integral electrostatics), re-run this session, whose CODATA-matching aspect
`a/R = 2.039050e-118` agrees with my 50-digit value to `1.2e-9` relative, and whose own
recorded note reads *"annulus closed form (ln(8R/a)+1)/2 …not a geometric prediction of
a"*. That instrument also returns `alpha^-1 = O(1)` on its valid aspect window, never
`O(137)`. **Its artifact regenerated byte-identically** (the only diff was a trailing
newline), which independently confirms the repo's reproducibility claim.

**Verdict. No verdict moved on this pass.** That is the finding worth recording: after
two consecutive passes that each corrected something, a third pass built specifically
to break the results did not. But three of these claims had been resting on a **single**
method, and one of them (X2) on a construction I had built myself from a definition
rather than from the source — the single most fragile thing in the whole audit. It now
has three validations and an exact certificate.

**Method rules, now three:**
1. *(2026-08-29)* Evaluate the object the target actually defines, not the object it
   claims that object equals.
2. *(2026-08-30)* Anchor every series to a number someone else published.
3. *(2026-08-30, new)* **An instrument is not trusted until it has been shown capable of
   failing.** Validate that it excludes what it must exclude before believing what it
   includes.

Instrument: `code/constraint_projection/cpf_triple_check.py` (`--full` adds the
T=74,000 sweep and the LF quantum search).
Artifact: `docs/constraint_projection_triple_check.json`.

---

### 2026-08-30 — Method adopted from external work: formal verification. **T0 introduced; our T1 label was overstated** · T0 machine-CHECKED

**Provenance.** Anthropic published *"Learning more about Claude's mathematical
capabilities"* (2026-08-10, `anthropic.com/research/riemann-zeta`): an unreleased model
raised the unconditional lower bound on the fraction of ζ zeros satisfying RH from
**41.6% to 67.2%**. Their own caveat: *"We don't expect that the techniques Claude used
will lead to proving the Riemann hypothesis."* Not peer-reviewed; reviewed internally by
Alpöge and Furman, externally by Conrey and Goldston.

**The result does not bear on this corpus.** Checked: we cite no zero-density bound
anywhere. Paper B's results are conditional-on-RH statements plus the center-manifold
claim; 67.2% is unconditional zero density. **No contradiction and no windfall** — logged
so nobody later mistakes it for either.

**The METHOD is what transfers, and it exposed a real defect in our tiering.**
Their pipeline ends in a **Lean 4 / Mathlib formalization passing a standard checker**.
Ours ends in a Python assertion. Those are categorically different things wearing the
same word:

```
MANIFEST T1: "Machine-verified -- automated test passes, reproducible by running the code"
```

When `cpf_triple_check.py` asserts `det M == (2Em - p^2)^2`, that is **sympy agreeing with
sympy**. It is not a proof. The label is stronger than the thing, which is precisely the
tiering dishonesty this ledger exists to catch — and we had been carrying it since the
bundle was assembled.

**T0 INTRODUCED — machine-CHECKED proof.** Strictly stronger than T1. Kernel-verified by a
proof assistant, with axiom dependencies disclosed. **No existing claim changes tier**:
T0 is a new classification earned by new evidence, not a promotion. Exactly one
proposition holds it so far.

**First T0 result.** `code/constraint_projection/lean/LFBound.lean` — the Local
Friendliness bound on the CPF manuscript's §5 sum is **exactly 4**. This is the
proposition that carried the 2026-08-29 correction to our *own* earlier verdict, which is
why it was chosen first.

```
lean code/constraint_projection/lean/LFBound.lean     0.84 s, exit 0, no Mathlib
```

| theorem | content |
|---|---|
| `S_le_four` | `S <= 4` for any normalised non-negative behaviour |
| `star_is_LF` | the explicit witness is a genuine LF branch |
| `star_S_eq_four` | the witness attains `S = 4` |
| `lf_bound_is_four` | attained **and** bounded ⇒ the LF maximum is 4 |

**Axiom disclosure** (`#print axioms`): `star_is_LF` and `star_S_eq_four` **depend on no
axioms at all** — pure computation. `S_le_four` and `lf_bound_is_four` use only
`propext` and `Quot.sound`. **No `Classical.choice`**, so the development is constructive.
No `sorry`; no `native_decide` (which would trust the compiler rather than the kernel).

**The proof was shown capable of failing** (rule 3, adopted 2026-08-30). Lean rejects the
file under each mutation: attainment `8 -> 9`; bound `<= 8 -> <= 7`; a single PR-box entry
`1 -> 0`. A proof that passed under a corrupted witness would be vacuous.

**Design choice: no Mathlib.** The file checks with a bare `lean` binary in under a
second, so verification costs a reader 30 s of install rather than an hours-long build.
The cost is that `IsGreatest` and set-builder notation are unavailable, so the theorem is
stated as an explicit attained-and-bounded pair. Arithmetic is in **doubled integer
units** (`B x y a b = 2·p(a,b|x,y)`); every probability in play is 0, ½ or 1, so doubling
clears denominators and keeps everything in `Int` where `omega` and `decide` close the
goals.

**Scope — what is NOT formalised.** Nothing here is a statement about quantum mechanics.
Two external facts complete the audit's argument and remain unformalised: Tsirelson caps
any quantum value of this expression at `2 sqrt 2`, and the Bell local bound is 2
(exhaustive over 64 strategies, numerical). Given those, `2 < 2 sqrt 2 < 4`. The upper
bound in Lean also needs only normalisation and non-negativity, **not** the LF
conditions — deliberate, and the honest reading is that all the content sits in
attainment.

**Two other methods from the same source, assessed honestly:**
- **Prior-art search before claiming novelty** (they pulled 54 arXiv papers). **We have
  not done this.** Our one claimed-new result — *a functional detecting off-line zeros
  must be odd under `beta -> 1-beta`* — was asserted novel on judgement alone. **OPEN: it
  needs a literature search before it stands as ours.**
- **Validator/generator role separation** (13 of 60 subagents were validators, separate
  from the 2 developing ideas). We have no structural separation: the same agent builds
  the instrument and checks it. Rule 3 is a self-administered substitute for what role
  separation buys structurally.

**What does not transfer.** The 60-subagent scale is for searching a large *open*
hypothesis space. Auditing a given manuscript has a space fixed by the document; more
agents would not have found anything the triple-check missed. Recorded so the scale is not
cargo-culted.

**Where we were already ahead.** They logged 30 failed subagents and ~650 dead ideas. That
is this ledger, and ours is append-only and older. No change.

Instrument: `code/constraint_projection/lean/LFBound.lean` · `.../lean/README.md`.

---

### 2026-08-30 — Prior-art search (first use of the new method): our one claimed-new result is **NOT NEW — RETIRED** · T4 (novelty claim falsified)

**The claim under test.** Logged 2026-08-29 and repeated in MANIFEST as *"the one
genuinely new output"* of the CPF audit:

> A functional detecting off-line zeros must be **odd** under `beta -> 1-beta`; any
> construction whose `beta`-dependence factors through `(1/2-beta)^2` is blind by the
> functional equation. This bounds a class, not a single attempt.

It was asserted novel **on judgement alone, with no literature search** — flagged as the
gap when we adopted Anthropic's prior-art step (they pulled 54 arXiv papers before
claiming). This is the first run of that step, and it kills our claim immediately.

**Prior art found.**

1. **Davenport–Heilbronn (1936)** is the classical witness for exactly this. Their
   function satisfies a Riemann-type functional equation — hence the full
   `beta <-> 1-beta` symmetry — yet **has zeros off the critical line** (it is a linear
   combination of two Dirichlet L-functions mod 5, and lacks an Euler product). So
   functional-equation symmetry alone **cannot** locate zeros, and DH is the standard
   counterexample making that precise. See *"Zeros of the Davenport–Heilbronn
   counterexample"*, Math. Comp. **76** (2007) 2045.
2. **Weil's positivity criterion** supplies the constructive complement we said was
   needed. Weil's explicit formula defines a Hermitian/quadratic form whose positive
   semidefiniteness is **equivalent to RH**, and off-line zeros appear as **negative
   eigenvalues** — for finitely many off-line zeros the number of negative eigenvalues is
   exactly half the number of zeros violating RH. That is precisely a functional that is
   *not* blind, and its sensitivity is the **sign/definiteness structure** our
   `(1/2-beta)^2` functional lacks. (AIM RH resource, `aimath.org/WWN/rh/articles/html/75a/`.)

**Verdict.** The statement is **true but not ours**. It is the elementary direction of
classical material: DH is the standard demonstration that the involution is not enough,
and Weil positivity is the standard construction that beats it. **RETIRED as a novel
result (T4 on the novelty claim).** The underlying observation stands as a correct reading
of the CPF manuscript's §7 — it is simply not a contribution.

**Note.** The Anthropic Riemann-zeta result logged above works in exactly this framework
— *"a quadratic form induced by Weil, and positive- (respectively negative-)definite
subspaces arising from zeros on (respectively off) the line."* Our "boundary" was a
weaker, negative-side restatement of the frame that work is built on. Had we searched
before claiming, we would have found it in one query.

**Method note.** The prior-art step paid for itself on first use, and it cost one search.
It is now standing practice: **no result is logged as novel until a literature search has
been run and recorded.**

---

### 2026-08-30 — Coherence audit: the CPF work used **none** of this repo's own methods · T1 measured

**Measurement.** Grep across all four CPF audit instruments for every method device this
program invented:

```
                              refraction | invariant(candidate) | shuffle | surrogate
                              | decoy | vantage | effective rank
cpf_audit.py                  0 hits
cpf_full_verification.py      0 hits
cpf_triple_check.py           0 hits
wave_equation_gfactor.py      0 hits
```

Four instruments, ~1,900 lines, **zero** uses or citations of the repo's own methodology.
The audit was competent and reached correct verdicts, but it was built as though the
corpus had no methods of its own.

**What was available and what actually applies — assessed honestly, not padded:**

| device | applies to the CPF audit? | verdict |
|---|---|---|
| **Tomographic invariance** (REFRACTION vs INVARIANT under instrument swap) | **YES — and we ran it without naming it** | coherence gap |
| **Decoy discipline** (test a "privileged" value against decoys) | **YES — and we did NOT run it** | real gap |
| **Vantage-point census / effective rank** | partially — as framing, not new computation | minor |
| **Shuffle knife / marginal-matched surrogate** | **NO** | correctly not applicable |

**The one real gap: decoys.** The manuscript's headline is that `alpha^-1 = 137.035999171`
matches CODATA to `6e-9`. We killed it as circular (`ln(8/(8e^-x)) + 1 = x + 1` for any
`x`, demonstrated across targets 42, 1000, −7). The **repo-native** form of that kill is
sharper and was never run: a two-parameter log formula `A ln(B/r) + C` with one parameter
free will hit *any* target to machine precision, so the decoy family is the whole family —
the match carries **zero** bits. The existing kill is correct; the decoy framing states
the strength of the result rather than only its failure mode.

**The coherence gap: refraction.** The four-cutoff table and the annulus/conformal/BIE
comparison **are** a tomographic-invariance test — `alpha^-1` moves under model swap (to
`O(1)`) and under the additive constant (`+1 -> -7/4` shifts it by exactly `11/8`). By
this ledger's own criterion, the manuscript's `alpha^-1` is a **REFRACTION**, not an
invariant, and that is the corpus's own vocabulary for precisely this. The audit
re-derived the device instead of citing it.

**Where the shuffle knife genuinely does not apply — recorded so it is not cargo-culted.**
The CPF audit is **deductive**: exact integer arithmetic, finite group theory, exact
rational certificates, symbolic algebra, and now a kernel-checked proof. Marginal-matched
surrogates test *statistical* claims against a matched null. There is no distribution to
permute in "does `phi_* = [[1,2],[0,1]]` lie in a group of order 4." Not a gap.

**Standing correction to practice.** An audit in this corpus should state, up front, which
of the program's own devices it applies and which it does not and why. Four instruments
went by without that.

**Our own novel methods, for the record** (none of them externally sourced):
`shuffle knife` (marginal-matched surrogate; FORM/FUNCTION split, self-calibrating because
the surrogate inherits the object's own distribution) · `tomographic invariance`
(refraction vs invariant under instrument swap, with both numerical (a) and structural (b)
paths and an explicit rule never to let (b) wear (a)'s clothes) · `vantage-point census`
(effective rank of witnesses — independent sightings or one reading refracted?) ·
`decoy discipline` · `strip-mine targeting` (rank by expected-space-collapsed per unit
cost, weighted toward the program's *own* load-bearing claims) · `append-only elimination
ledger` · `tiers never promote`.

---

### 2026-08-30 — Decoy test on the CPF alpha match, and the second T0 · T1 measured / T0 machine-checked

Both items closed the two gaps named in the coherence audit above.

**(A) DECOY TEST — the corpus's own discipline, applied to the CPF audit for the first
time.** Precedent: the T_min height floor (2026-06-06), where decoy floors
(`2πe·φ`, `(2πe)²/10`, `2πe/1.5`) were tested and **only** `2πe` gave a vanishing main
term — that separation is what made `2πe` privileged rather than merely fitted.

Instrument `code/constraint_projection/alpha_decoy_test.py`, artifact
`docs/alpha_decoy_test.json`. Fourteen "geometric-looking" log-forms of the same species
as the manuscript's, each solved for the cutoff `a/R` reproducing CODATA
`alpha^-1 = 137.035999177`:

```
manuscript, as written:  ln(8/r) + 1          a/R = 6.65896e-59     residual 0.0
manuscript, corrected:  (ln(8/r) + 1)/2       a/R = 2.03905e-118    residual 1.99e-59
Kelvin-Maxwell ring:    (ln(8/r) - 7/4)/2     a/R = 1.30352e-119
thin-ring capacitance:   ln(8/r)              a/R = 2.44969e-59
different log argument:  ln(4/r) + 1          a/R = 3.32948e-59
pi-flavoured:            ln(8/r) + pi/2       a/R = 1.17842e-58
quadratic in the log:    sqrt(ln(8/r)^2 + 1)  a/R = 2.45865e-59
power form:              (8/r)^(1/60)         a/R = 4.93185e-128
   ... 14 of 14 reproduce CODATA to < 1e-25 (100% of the family)
```

**The decoy test does NOT separate.** Every form hits the target once allowed its own free
cutoff. Where the T_min test isolated `2πe`, this isolates nothing. Two supporting
measurements: **bits carried = 0** (one parameter fitted to one datum, residual DOF 0 —
the model reproduces *every* target in its range, e.g. `alpha^-1 = 42` at
`a/R = 1.25e-17`); and the quoted `6e-9` agreement **tracks the working precision**, not
the physics — it is the manuscript's rounding of its own cutoff, improvable without limit
by quoting more digits.

**The parameter-free reading.** The one place the manuscript fixes `a/R` independently of
`alpha` is `tau = i a/R = i/2`. Take the zero-free-parameter claim seriously and
`alpha^-1` is then **predicted**: `1.886294361`, wrong by a factor of **72.6**. The
137.036 is obtained by abandoning that condition and fitting instead. Both appear in §3,
five lines apart.

**Kill-criterion verdict, in this ledger's own vocabulary: REFRACTION.** The value moves
~8x across legitimate models of the same geometry (annulus 3.037587 / conformal 1.692054 /
BIE 0.372688 at `a/R = 0.05` — our recomputation reproduces the repo's recorded annulus
value exactly), and `d(alpha^-1)/d(additive constant) = 1/2` exactly, so `+1 -> -7/4`
shifts it by `11/8`. Not an invariant candidate.

The existing circularity kill (C1/C2) was correct. **The decoy framing states its strength
rather than only its failure mode:** the match is not merely circular, it is
*uninformative* — no member of a 14-form family fails where the manuscript's form succeeds.

**(B) SECOND T0 — Axiom III clause (3) machine-checked.**
`code/constraint_projection/lean/AxiomIII.lean`, `lean` exit 0 in 0.93 s, no Mathlib.

| theorem | content |
|---|---|
| `commutes_iff_diagonal` | the centraliser of `D = diag(1,-1)` is **exactly** the diagonal matrices |
| `phi_not_commutes` | `phi_*` is not in it |
| `phi_conj_D` | `phi_* D = [[1,-2],[0,-1]]` vs `D phi_* = [[1,2],[0,-1]]` |
| `centraliser_unimodular` | its unimodular elements are **exactly the four** `diag(+-1,+-1)` |
| `trace_two_only_identity` | trace `+2` in that group is attained **only by the identity** |
| `phi_infinite_order` | `phi_*^n = [[1,2n],[0,1]] != I` for `n >= 1` |

**Axioms disclosed:** `propext`, `Classical.choice`, `Quot.sound`. **Unlike `LFBound.lean`
this development is NOT constructive** — `Classical.choice` enters through the automation.
Recorded rather than hidden; the first file's constructivity was reported, so the second
file's loss of it must be too.

**Shown capable of failing:** Lean rejects the file under each of — `phi` made diagonal (so
it *should* commute), `D` made the identity, one of the four centraliser elements dropped,
and the power formula corrupted `2n -> 3n`.

**Scope, stated deliberately.** Proved: the algebraic obstruction, in full. **Assumed and
cited, not formalised:** that a diffeomorphism of `K` lifts to `T^2` and induces a matrix
commuting with `D`, and that `MCG(K) = Z/2 (+) Z/2` (Lickorish 1963). Formalising surface
topology is far beyond this file, and those facts are not in dispute — **the manuscript's
error is algebraic, and the algebra is what is machine-checked.** Independent
confirmation of the same four matrices by `Out(pi_1(K))` word algebra remains in
`cpf_triple_check.py` X1, which shares no machinery with either.

---

### 2026-08-30 — Is the 72.648x alpha gap a scaling rule? — **ARTIFACT, on five independent grounds** · T1 machine / T2 structural

**The hypothesis, and why it was testable.** The decoy test above found that taking
the zero-free-parameter claim seriously — fixing `a/R = 1/2` from `tau = i a/R = i/2` —
*predicts* `alpha^-1 = 1.886` against an observed `137.036`, a factor of **72.648**. A
fair reading: that factor might not be noise. If it were systematic, the framework would
be right in form and merely missing a power law. Worth testing, and testable, because a
rule and an artifact make different predictions:

> a **RULE** is a property of the theory — constant under convention changes, and
> present wherever the theory meets data.
> an **ARTIFACT** is a property of one arbitrary choice — it moves when the choice moves.

Instrument `code/constraint_projection/alpha_scaling_test.py`, artifact
`docs/alpha_scaling_test.json`.

**S1 — the factor moves with the convention.** `tau` is a modelling choice, so sweep it:

| tau | a/R | L | pred alpha^-1 | RATIO | exponent p |
|---|---|---|---|---|---|
| i/4 | 1/4 | 4.4657 | 2.2329 | **61.372** | 3.288 |
| i/3 | 1/3 | 4.1781 | 2.0890 | **65.598** | 3.441 |
| i/2 | 1/2 | 3.7726 | 1.8863 | **72.648** | 3.706 |
| i | 1 | 3.0794 | 1.5397 | **89.001** | 4.375 |
| 2i | 2 | 2.3863 | 1.1931 | **114.85** | 5.657 |
| 3i | 3 | 1.9808 | 0.9904 | **138.36** | 7.198 |

The ratio runs 61 → 138 (2.25x) and the exponent 3.29 → 7.20. Neither is a constant of
the theory. **And the ratio is not independent data**: it is *defined* as
`alpha^-1 / (L/2)`, so it carries exactly the information `alpha^-1` already carries.
Asking whether 72.648 is meaningful is asking whether `137.036 = 72.648 x 1.886`, which
is true by construction.

**S2 — the neighbourhood is dense.** Of 11 short closed forms tried, **2** land within
1e-3 of 72.648: `e^(30/7)` (8.5e-5) and `sqrt(5277)` (7.3e-5). The second is
transparently meaningless, which is the point — near any 3-digit target the space of
short closed forms is dense, so "it looks like a constant" carries no information. Same
failure mode the alpha decoy family exhibited.

**S3 — it does not transfer (decisive).** A missing power law is a property of the
theory, so it must appear wherever the theory meets data:

| observable | predicted | observed | ratio | = 72.648^k |
|---|---|---|---|---|
| alpha^-1 | 1.88629 | 137.036 | 72.6483 | **k = 1.0** |
| L_IR [m] | 3.86159e-13 | 1.3e26 | 3.36649e+38 | **k = 20.7** |
| g-factor | 2.0 | 2.00232 | 1.00116 | **k = 0.00027** |

One rule requires ONE exponent. These are five orders of magnitude apart. And the alpha
row reads `k = 1.0` **by construction** — 72.648 was *defined* as that ratio, so that row
is the definition, not a confirmation.

**S4 — no non-zero power reconciles the instruments (the strongest form, and the fairest
test).** The repo has three independent electrostatic models of the *same* geometry at
`a/R = 0.05`: annulus 3.037587, conformal 1.692054, BIE 0.372688. Under
`alpha^-1 = K X^p`, all three describe one physical geometry so all must map to the same
observed 137.036. But `K X1^p = K X2^p` with `X1 != X2` **forces `p = 0`**, and then
`K = 137.036` — the answer itself. The only power law that reconciles the instruments is
the one that **discards the geometry entirely**. That is not a correction to the theory;
it is the removal of the theory.

**S5 — underdetermined anyway.** Fitting `alpha^-1 = K L^p` needs at least two
independent (input, output) pairs. The manuscript supplies **one** measured observable it
claims to derive (`alpha`) against **two** parameters: residual DOF **−1**. Every `(K,p)`
on the curve `K L^p = 137.036` fits perfectly — `p=1, K=36.32`; `p=2, K=9.628`;
`p=4, K=0.6765`; `p=-1, K=516.98` — none preferred. *(The table's `p = 3.70567 →
K = 1.0000006` row is not a near-miss: that exponent was derived from the requirement
`K = 1`, and the residual is truncation in the 7 digits shown. Circular, and recorded as
such so it is not read as a finding.)* The "natural" exponent `ln(137.036)/ln(L) =
3.7056685` is not an integer, half-integer, or any recognisable index.

**Verdict: ARTIFACT.** Five independent grounds, no verdict change to anything already
logged — the alpha kill stands where it stood.

**The hypothesis could have come out otherwise, and that is why it was worth running.**
Had the ratio held near 72.648 across the `tau` sweep **and** reproduced the `L_IR` gap,
that would have been genuine evidence of a missing power and would have reopened the
alpha leg. It does neither. Recorded as a live alternative that was tested and failed,
not as one dismissed.

Instrument: `code/constraint_projection/alpha_scaling_test.py`.
Artifact: `docs/alpha_scaling_test.json`.

---

### 2026-08-30 — Third T0: the per-zero 2π contribution machine-checked · T0

`code/constraint_projection/lean/withMathlib/PerZero.lean`, `lake env lean` exit 0 in
~4 s. Completes formal verification of the deductive core of the CPF audit.

**Target.** The audit's exact evaluation of §7's defining integral (2026-08-30, X3) rests
on one step: for real `alpha`, `INT du/(alpha+iu) = arctan(u/alpha) - (i/2)ln(alpha^2+u^2)`,
so a zero at `beta = 1/2` sees `alpha = +eps` and `alpha = -eps`, the imaginary parts
(depending on `alpha^2`) cancel, the real parts add, and the contribution is
`2[arctan((T-gamma)/eps) + arctan(gamma/eps)] -> 2 pi`. That is the residue count derived
without the residue theorem, and it was carrying the whole X3 result on Python plus a
hand argument.

| theorem | content |
|---|---|
| `imag_cancels` | the imaginary parts cancel **exactly**, for every `eps` — no hypothesis |
| `real_doubles` | the real parts combine to exactly `2[arctan((T-g)/eps) + arctan(g/eps)]` |
| `contribution_lt_two_pi` | that is **strictly below** `2 pi` at every finite `eps` |
| `contribution_tendsto` | and **tends to** `2 pi` as `eps -> 0+`, for `0 < gamma < T` |
| `per_zero_two_pi` | the package |

**A correction to our own prose, forced by the formalisation.** The ledger and the audit
both wrote the contribution "`-> 2 pi`", but `cpf_triple_check.py` X3's inline comment
reads "`-> 2 pi` for any zero strictly inside", which invites reading it as an attained
value. It is not: `arctan < pi/2` strictly, so at every finite `eps` the contribution is
**strictly below** `2 pi`, and `2 pi` is a supremum approached in the limit. Formalising
made the distinction unavoidable, and both statements are now in the file
(`contribution_lt_two_pi` and `contribution_tendsto`) rather than one loose arrow. The
numerics were never affected — X3's ratios approach 1 from both sides — but the wording
was looser than the mathematics.

**Axioms disclosed:** `propext`, `Classical.choice`, `Quot.sound`. Non-constructive, as
Mathlib's real analysis is. No `sorry`; no `native_decide`.

**Shown capable of failing:** Lean rejects the file under each of — contribution
coefficient `2 -> 3`; limit `2 pi -> 3 pi`; bound `2 pi -> pi`; `imagPart` made **odd** in
`alpha` (`alpha^2 -> alpha`, so the cancellation must fail); `realPart` sign flipped.
The fourth is the important one: it targets the exact structural fact the argument turns
on.

**Scope.** That the closed form **is** the integral — the evaluation of `INT du/(alpha+iu)`
itself — is not formalised; it is standard calculus and is taken as the *definition* of
`realPart`/`imagPart`. What is proved is everything the audit does **with** it. Summing
over the `N(T)` interior zeros gives `2 pi N(T)`.

**Cost, recorded honestly.** This is the first proof here needing Mathlib: ℝ, `arctan` and
filter limits are all outside Lean core. `LFBound` and `AxiomIII` check with a bare `lean`
binary in under a second; this one needs a ~5 GB cache. That raises a reader's
verification cost by orders of magnitude, which is why it sits in its own
`withMathlib/` directory with its own `lakefile.toml` — the dependency boundary is visible
in the tree rather than buried in an import line.

**Formal-verification status after three T0 results.** The deductive core of the CPF audit
is now machine-checked end to end: the LF bound (§5), Axiom III clause (3), and the
per-zero contribution (§7). What remains outside the kernel is, in every case, either
measured data or standard textbook results cited by name — never a step of our own
reasoning.

---

### 2026-08-30 — What the alpha gap actually is, and whether it can be corrected — **NOT CORRECTABLE; three routes closed** · T1 machine / T2 structural

**Why this entry.** The scaling test above ruled out a missing power law, which rules out
a *species* of correction and therefore narrows the question rather than closing it. The
open question was: if not a power law, what **is** it? Instrument
`code/constraint_projection/alpha_gap_diagnosis.py`, artifact
`docs/alpha_gap_diagnosis.json`.

**G1 — the gap is ADDITIVE IN THE LOG, not multiplicative.** `alpha^-1 = (1/2)(ln(8R/a)+1)
= L/2` is linear in a logarithm, so the honest variable is `L`:

```
L from tau = i/2      =   3.7726
L needed for CODATA   = 274.0720
ADDITIVE gap in L     = 270.2994   ->  a/R must shrink by 10^117.4
```

**This is why no power law fit.** A power law is `alpha^-1 ~ L^p`; the actual requirement
is `L -> L + 270`. The scaling test was testing the wrong shape — and its failure was
informative precisely because it identified that.

**G2 — "72.6x" was never a property of the theory.** Every defensible physical scale:

| cutoff `a` | `a/R` | `L` | `alpha^-1` | off by |
|---|---|---|---|---|
| Planck length | 8.37e-23 | 53.91 | **26.96** | 5.08x |
| classical electron radius | 1.46e-2 | 7.31 | 3.65 | 37.5x |
| proton charge radius | 4.35e-3 | 8.52 | 4.26 | 32.2x |
| `a = R` | 1.0 | 3.08 | 1.54 | 89.0x |
| `tau = i/2` | 0.5 | 3.77 | 1.89 | 72.6x |
| CODATA-matching | 2.04e-118 | 274.07 | 137.036 | 1.0x |

The Planck cutoff — the most defensible choice available — gives **26.96**, off by 5.08x,
not 72.6x. Same finding as the `tau` sweep, now in physical rather than modular language.
And the CODATA-matching cutoff is **2.4e-96 Planck lengths**: not a cutoff, an unphysical
number. A "UV completion" 96 decades below the Planck scale is not a regulator.

**G3 — the prefactor cannot be repaired.** Redoing the self-energy match with both
normalisations free (charge `q = eta e`, capacitance `C = kappa eps0 R/L`):

```
alpha^-1 = (4 pi eta^2 / kappa) * L      [check: kappa=2pi, eta=1/2 -> 1/2  OK]
```

At the Planck cutoff, matching CODATA needs `4 pi eta^2/kappa = 2.5418`:

| `kappa` | required `eta^2` | required `eta` | natural? |
|---|---|---|---|
| `2 pi` (manuscript) | 1.2709 | 1.1273 | no |
| `4 pi^2` (thin ring) | 7.9851 | 2.8258 | no |
| `4 pi` | 2.5418 | 1.5943 | no |
| `1` | 0.2023 | 0.4497 | no |

Natural charge fractions are `1, 1/2, 1/3, 2/3, 2`. **None.** Route closed.

**G4 — the shape IS RG running, with the wrong coefficient and the wrong sign.** A
relation linear in `ln(scale)` is exactly the form of a running coupling, so the
manuscript has the right functional form for the wrong reason. One-loop QED, one Dirac
fermion of unit charge:

```
QED:         d(alpha^-1)/d ln(mu)  = -2/(3 pi) = -0.2122
manuscript:  d(alpha^-1)/d ln(R/a) = +1/2      = +0.5000
             magnitude ratio 2.3562,  signs OPPOSITE
```

*(The ratio equals `3 pi/4` exactly, but that is just the arithmetic of the two
coefficients — recorded so it is not misread as a finding. Same trap as `sqrt(5277)`.)*

**The sign is fatal.** QED **screens**: `alpha^-1` decreases toward short distance,
because vacuum polarisation shields the bare charge. The manuscript's relation
*increases* — anti-screening in a `U(1)` theory, which is backwards. Asymptotic freedom
is non-abelian.

**G5 — the general statement, and its PRIOR ART (searched BEFORE claiming, rule 4).**
The formula admits two readings and both are closed:

- **(a) self-energy with a fixed cutoff** — CAN produce a number, but only once the cutoff
  is fixed independently. The framework's own fixing gives `1.886`; G2 shows every other
  defensible scale gives `1.5` to `27`.
- **(b) RG running** — CANNOT derive `alpha` at all: running relates `alpha` at two scales
  and requires a renormalisation condition at one of them. It never produces `alpha` from
  nothing.

**The general no-go is STANDARD, not ours.** Dimensional transmutation is the established
name for trading a dimensionless coupling for a scale (Coleman–Weinberg; `Lambda_QCD`);
RG renormalisation conditions as required boundary data are textbook; and the mainstream
position is that dimensionless constants must be **measured**, not derived. The whole
genre has a survey: *"Attempts at a determination of the fine-structure constant from
first principles: A brief historical overview"* (arXiv:1411.4673), covering Eddington
(136, then 137) and Wyler (137.03608).

**The sharpest point in that literature, and a correction made in-flight.** The first
draft of this instrument asserted that Wyler's match was *better* than the manuscript's.
It is not — checked, and the direction is the opposite:

```
Wyler 1970:      alpha^-1 = 137.03608       rel err 5.9e-7
this manuscript: alpha^-1 = 137.035999171   rel err 4.38e-11
                 the manuscript is 13,471x CLOSER
```

Wyler's agreement was good enough to attract serious attention in 1971 and was still
debunked. **This one is four orders of magnitude better and carries zero bits** (decoy
test, 14 of 14 forms). That is the decoy lesson as history rather than arithmetic:
**closer agreement is not better evidence** — more digits of agreement only means more
digits were fitted, when the construction can hit any target.

**ANSWER TO "HOW DO WE CORRECT THE GAP": you do not.** All three routes are closed, and
the correct move is not repair but reporting: **the framework, taken with its own
scale-fixing, predicts `alpha^-1 = 1.886` and is falsified.** That IS the corrected
result. Anything that closes the gap adds physics not in the manuscript, at which point
it is a different theory and must be tested as one.

**Rule 4 worked as intended, and earlier in the cycle than last time.** The prior-art
search was run *before* the claim was logged rather than after. It retired the general
no-go as standard while confirming the specific diagnosis as ours. Second consecutive
entry where the search changed what we were entitled to say.

Instrument: `code/constraint_projection/alpha_gap_diagnosis.py`.
Artifact: `docs/alpha_gap_diagnosis.json`.

---

### 2026-08-30 — Can a RELATIVE boundary condition fix alpha? — **the condition is relational and the framework contains one; alpha still does not follow** · T1 machine / T2 structural

**The question.** The gap diagnosis ended on: a log-in-scale relation derives `alpha` only
if the scale ratio is fixed from outside, and RG running cannot supply that because it
needs a boundary condition. The natural follow-on: what if the condition is not a single
absolute value but a **relation** between scales? That is a real idea — gauge unification,
dimensional transmutation and fixed points all work that way, and none fixes a coupling
absolutely. Instrument `code/constraint_projection/alpha_relational_boundary.py`.

**B1 — the framework already HAS one, and it is a genuine parameter-free prediction.**
§8 states `lambda_UV * lambda_IR = 1/R^4`, i.e.

```
a * L_IR = R^2          <- a RELATION between UV cutoff and IR scale
```

Substituting `a = R^2/L_IR` into the corrected relation collapses the free parameter
entirely:

```
alpha^-1 = (1/2)( ln(8 R/a) + 1 ) = (1/2)( ln(8 L_IR / R) + 1 )
```

`alpha` is now fixed by the **ratio of cosmological to electron scale** — Dirac's
large-number structure. With `L_IR` taken from observation, nothing is left free:

```
L_IR / R          = 6.73297e38     <- the Dirac large number
alpha^-1 PREDICTED = 46.242346
alpha^-1 observed  = 137.0359992
off by             = 2.9634x
```

**This is a measurable improvement.** 2.96x beats the 72.6x of `tau = i/2`
and the 5.08x of a Planck cutoff, and unlike both it is **parameter-free**. Reaching
137.036 would need `L_IR/R = 4.90e117` against a measured `6.73e38` — off by `10^78.9`.

**B2 — the decisive kill: a relational alpha must DRIFT.** If `alpha` is set by `L_IR/R`
and `L_IR` grows with expansion, `alpha` is not constant. That is measurable:

```
d(alpha^-1)/dt ~ H_0/2 = 3.45e-11 /yr
|alpha_dot/alpha|      = 2.52e-13 /yr
```

| bound on `|alpha_dot/alpha|` [/yr] | value | exceeded by |
|---|---|---|
| atomic clocks, Al+/Hg+, Yb+ | 2e-17 | **12,575x** |
| Oklo natural reactor (2 Gyr) | 1.2e-17 | **20,958x** |
| quasar absorption systems | 1e-16 | 2,515x |

**Excluded by ~10^4 against every independent bound.** The relational reading does not
merely mispredict `alpha`'s *value* — it predicts `alpha` **varies**, and that is ruled
out on its own, independently of the 2.96x normalisation gap.

*Prior art, searched before claiming (rule 4): using alpha-constancy to constrain
varying-alpha models is a standard, well-developed method, and the Oklo and atomic-clock
bounds quoted are the field's own. Nothing in the method is ours — only its application
here. Likewise the Dirac large-number framing is classical, and is where such hypotheses
normally die.*

**B3 — and the deep point: TWO relational conditions that disagree.**

| condition | source | `a/R` | `alpha^-1` |
|---|---|---|---|
| `tau = i a/R = i/2` | §3 | 0.5 | **1.886294** |
| `a L_IR = R^2`, `L_IR` observed | §8 | 1.485e-39 | **46.24235** |

Neither gives 137.036, and **they disagree with each other by 24.5x**.

**A relative boundary condition does not rescue the framework — it makes it
OVER-DETERMINED AND INCONSISTENT, which is strictly worse than under-determined.**
Under-determination is a missing input you can go and find. Over-determination with
disagreement means the framework's own conditions contradict each other and there is **no
free parameter left to absorb the difference**. Supplying the boundary condition removes
the last place the discrepancy could have hidden.

**Verdict.** Both antecedents hold — the condition is relational, and the framework contains
one — and supplying it moves the framework from under-determined to over-determined. Logged as
a route that genuinely improved the prediction (72.6x → 2.96x, and parameter-free) and was
killed anyway, by a test it could have passed: had the predicted drift come in below
1e-17/yr, the relational reading would have survived as a live option with only a
normalisation gap to explain.

Instrument: `code/constraint_projection/alpha_relational_boundary.py`.
Artifact: `docs/alpha_relational_boundary.json`.

---

### 2026-08-31 — The Kelvin/Klein-Foam reading: "there are no particles, only the finite-resolution throat" — **THE READING IS STRUCTURALLY RIGHT; THE CORPUS CARRIES TWO SCOPES FOR `a/R`** · T2 structural / T1 machine / T1 (corpus fact)

**The proposal, in the author's words.** `a` in `alpha^-1 = (1/2)(ln(8R/a)+1)` is not a
particle cutoff. There are no particles. `a` is the *finite resolution of the throat* —
the scale below which the foam has no more structure to resolve. This is not a
re-parameterisation; it is a different ontology, and it was read against the
programme's own prior note rather than against my summary of it.

Read: `papers/notes/Klein_Foam_Monad.tex`, `papers/notes/Mobius_Ribbon_Capacitance.tex`.
Instrument: `code/constraint_projection/klein_foam_reading.py`.
Artifact: `docs/klein_foam_reading.json`.

**K1 — the reading is STRUCTURALLY CORRECT, and this is a real result.** Verified
symbolically, not asserted: under a joint rescaling `(R, a) -> (lambda R, lambda a)`,

```
alpha^-1(lambda R, lambda a) - alpha^-1(R, a) = 0     (sympy, exact)
```

`alpha^-1` depends on `R` and `a` **only through the ratio `R/a`**. It carries no absolute
length. That is exactly the signature a no-particles, resolution-relative ontology
predicts: the formula does not know how big anything is, only how many resolution elements
fit across it. A cutoff reading would have no reason to produce that invariance; the
resolution reading requires it. **The ontology is doing real work here.**

This is also the same invariant this repo already isolated in FF06h — the physical content
is `width/delta`, never a bare length — reached independently and from the other direction.

**K2 — and it gives the best absolute prediction of any reading tested.** The Klein-Foam
note supplies its own resolution floor; §`sec:scales` reads *"Micro (Planck / voxel):
turbulent foam, phase-slip statistics"*. Taking the foam at its word:

```
a = l_Planck = 1.616255e-35 m,   R = R_e = 2.8179403e-15 m
a/R      = 8.37092e-23
alpha^-1 = 26.957067
observed = 137.0359992          ->  off by 5.0835x
```

| reading | `a/R` | `alpha^-1` | off by |
|---|---|---|---|
| §3's `tau = i a/R = i/2` | 0.5 | 1.886 | 72.6x |
| `a = R` | 1 | 1.540 | 89x |
| §8 relational, `a L_IR = R^2` | 1.49e-39 | 46.24 | 2.96x (**parameter-free**) |
| **Klein-Foam Planck floor** | **8.37e-23** | **26.96** | **5.08x** |
| required by CODATA | 2.039e-118 | 137.036 | — |

**Best absolute reading on the board.** Only the §8 relational condition beats it, and that
one died on alpha-drift (12,575x past atomic clocks). Supplying a *principled* resolution
moves the answer 14x closer than the manuscript's own `tau = i/2`.

**K3 — the kill becomes INTERNAL, which is sharper than what we had.** The manuscript's
`alpha` requires

```
a = 3.93699e-131 m  =  2.43587e-96 Planck lengths
                    =  95.6 DECADES BELOW the foam's own declared floor
```

Before this reading, the objection was external: *a sub-Planckian cutoff is unphysical* —
an appeal to outside physics the manuscript could in principle dispute. Under the
Klein-Foam reading it is a **contradiction between two documents of the same programme**:
the foam declares its resolution Planck-scale, and the manuscript's `alpha` needs one 96
decades finer. The framework now refutes itself without help.

**And the renaming does not move the arithmetic.** Cutoff or resolution, `alpha^-1 =
(1/2)(ln(8R/a)+1)` still demands `a/R = 2.039e-118`. The ontological move may well be
right; it is simply **orthogonal to the falsifiable content**. Same shape as CPF §9's
relational-measurement material: a reframe that leaves the numbers untouched. A better
name for `a` is not a different value of `a`.

**K4 — the finding I did not expect: the corpus already contains the resolution.** Two
entries state a scope for `a/R`. The statements differ. Quoted from the files, not
paraphrased:

> **Klein_Foam_Monad.tex:** *"Absolute uniqueness and ``no free parameters'' claims are not asserted."*
>
> **Klein_Foam_Monad.tex:** *"as-implemented, not as a uniqueness theorem for $\alpha$."*
>
> **Klein_Foam_Monad.tex:** *"Free-parameter count depends on which quantities are treated as inputs ($R$, $a/R$, charge split); absolute ``zero free parameters'' is not claimed."*

against

> **CPF manuscript:** *"The framework contains zero free parameters and is both UV and IR complete."*
>
> **CPF manuscript:** *"CPF + GfE | 0 | All constants"*

`Klein_Foam_Monad.tex` **names `a/R` explicitly** as one of the inputs whose treatment
determines the free-parameter count, and records the count as input-dependent. The CPF
entry records that same `a/R` as not free.

**This is a corpus fact, not a verdict on either entry.** Both are entries. Each records a
state of the work at its date. Neither is graded here, and neither is retracted — the
ledger is append-only and that applies to the entries being read, not only to the ones
being written. What the ledger records is which scope the arithmetic supports, and K3
answers that: `a/R` is carrying a fitted value, so the earlier scope is the one the numbers
match.

**What it changes is WHERE the resolution lives.** This audit's central finding —
*"zero free parameters does not hold; `a/R` is fitted"* — was already in the corpus, in
those words, dated a month earlier. The audit did not have to supply it. It had to find it.
An external instrument was built to establish something the corpus had already established
internally, which is a fact about **how this audit was run**, not about either document.

**Verdict.** Four things established, none of them a judgement:
1. The reading is structurally correct — joint-scaling invariance, verified symbolically (K1).
2. It gives the best absolute prediction of any reading tested — 26.96, off 5.08× (K2).
3. The required resolution sits 96 decades below the foam's declared floor, so the `alpha`
   discrepancy is **internal to the corpus** and needs no external appeal (K3).
4. The corpus holds two scope declarations for `a/R`; the arithmetic matches the earlier
   one (K4).

One thing not established: any movement in `alpha`. The renaming is orthogonal to the
number.

*Method note (rule 4).* Nothing here is a new technique. Reading a claim against the
programme's own prior scoped statement of it is just source-checking; the joint-scaling
test is dimensional analysis done symbolically. The only reason it produced anything is
that it was pointed at our own corpus instead of at the literature — the coherence audit
of 2026-08-30 flagged exactly that gap, and this is the first entry to close it.

*Dead end logged as a win.* The instruction stands: success is documented failure as well.
This route did not save `alpha` and was never going to — but it established that the
ontology and the CPF entry are **not the same claim**, and that the corpus states the
scope for `a/R` in two places that do not agree. That is a fact about the corpus, and it
was not visible before the reading; no amount of further arithmetic on the CPF entry alone
would have surfaced it.

*A framing correction, made after this entry first landed in `bdcb530`.* The first draft of
this entry read the scope difference as a fault — "regressed", "stripped off", "the better
document". That imports a judgement the arithmetic does not carry and that this ledger's
own discipline forbids: **entries record state; they do not indict each other.** A
manuscript is a ledger entry. It has a date, a scope, and a set of claims that the numbers
either match or do not. Reading it as a defendant is a category error against the method,
and it also degrades the finding — "two scopes, arithmetic matches the earlier" is checkable
and reusable; "the manuscript overclaimed" is neither. The instrument, this entry, MANIFEST
and the PR were rewritten to the factual form. `bdcb530` stays in history as written.

---

### 2026-08-31 — The Feynman path integral run against CPF and the Klein-Foam reading — **THE ONTOLOGY PASSES ON ITS OWN GROUND; THE α DERIVATION IS AN IDENTITY** · T2 proved / T1 machine / T3 measured

**Why this test is fair rather than imported.** The path integral is not an outside
standard being applied to a foreign object. *"No particles, only histories"* is Feynman's
own statement of it, and *"finite resolution of the throat"* is lattice regularisation.
Running the path integral against the Klein-Foam reading is running it on **home ground**.

Instrument: `code/constraint_projection/feynman_path_integral.py`.
Artifact: `docs/feynman_path_integral.json`. Every number computed in-instrument; the
2026-08-30 running verdict was **re-derived rather than reused**.

**P0 — what the formalism gives the ontology.** Three things transfer exactly: the
no-particles reading is the formalism's own; a shortest length is lattice regularisation,
the most successful non-perturbative definition of QFT we have; and K1's joint-scaling
invariance is precisely the property a lattice theory has (physics depends on
`correlation length / spacing`, never the bare spacing). **The ontology is well-formed as
a lattice path integral.** Nothing below touches that.

**P1 — loop counting: ħ enters at exactly one place, and it is an input.** Solved
symbolically, `R` left free:

```
self-energy condition E_self = m_e c^2, solved for L:
    L = 16 pi eps0 R m_e c^2 / e^2          contains hbar?  FALSE
substituting the manuscript's R = hbar/(2 m_e c):
    L = 8 pi eps0 hbar c / e^2              contains hbar?  TRUE
    L * alpha = 2                    ->  alpha^-1 = L/2
```

The electrostatic step is **ħ-free** — it is a saddle point, zero loops, `O(ħ⁰)`. In the
path integral `α` **is** the loop-counting parameter. A tree-level quantity therefore
carries no information about it, and indeed `α` appears only after `R = ħ/(2m_ec)` is
imposed. That substitution is the sole carrier of ħ in the derivation.

*(This also re-derives the factor of 2 independently: `L·α = 2` was the audit's first
finding, obtained by arithmetic. Here it drops out of the symbolic solve.)*

**P2 — what the derivation actually says.** Solving the same relation for `R` instead:

```
classical self-energy alone:   R = (L/4) * r_e         r_e = e^2/(4 pi eps0 m_e c^2)
the manuscript separately SETS: R = lambdabar_C / 2
equating:                       L = 2 * (lambdabar_C / r_e)
```

And `λ̄_C/r_e` is `α⁻¹` **by the standard identity `r_e = α λ̄_C`** — verified numerically
here, not assumed:

```
r_e / lambdabar_C  = 0.00729735257375
alpha   (CODATA)   = 0.00729735256433      agreement 1.29e-9
```

**So the derivation collapses to `r_e = α λ̄_C` rewritten.** It determines `L` *from* `α`.
Getting a number out the other way requires `a/R` supplied independently — and the
manuscript supplies it:

```
manuscript:            a/R = 8 exp(-136.035999171)
stated exponent          = 136.035999171
CODATA alpha^-1 - 1      = 136.035999177
difference               = 6.0e-9
```

**The exponent that fixes `a/R` is the measured `α⁻¹`, minus one, to 6e-9** — which is
precisely the agreement the entry reports. Input and output are the same number, and the
6e-9 is the round-trip error, not a prediction's residual.

**P3 — the measure: `w₁ ≠ 0` is exactly what forbids a spin structure.** §4 reads 4π
spinor periodicity off non-orientability. In the path integral a spinor is not a reading —
it is a **choice of measure**, and that measure needs a spin structure. Computed from the
CW complex over GF(2), not quoted:

```
CW: 1 vertex, 2 edges, 1 face      ->  chi(K) = 0
over GF(2): rank d1 = 0, rank d2 = 0
            dim H_1(K; Z/2) = 2    ->  |H^1(K; Z/2)| = 4
Wu on a closed surface: w2 = w1^2, <w2,[K]> = chi mod 2 = 0

    Spin  (needs w1 = 0)         0 structures   <- Axiom II SETS w1 != 0
    Pin+  (needs w2 = 0)         4 structures
    Pin-  (needs w2 + w1^2 = 0)  4 structures
                                 8 fermionic measures, 3 bits, none specified
```

**Axiom II's `w₁ ≠ 0` is the precise condition under which no spin structure exists.** The
property the framework relies on for its spinor claim is the property that removes the
spin measure. What remains is a **Pin** theory — perfectly well-defined, but requiring a
choice of Pin⁺/Pin⁻ and one of four structures. Pin⁺ and Pin⁻ are physically different
theories. Three bits of discrete data are unspecified, so the parameter count fails **in
the measure**, before any coupling is computed.

*Note what this is not:* it is **not** "fermions are impossible on `M`". They are fine.
The data is simply real, physical and unstated.

**P4 — our own earlier verdict, re-derived instead of reused.** From the one-loop vacuum
polarisation, differentiating with respect to the RG scale `μ` (the variable that makes
the question well-posed):

```
QED   d(alpha^-1)/d ln mu = -2/(3 pi) = -0.21220659   alpha^-1 falls with energy (screening)
CPF   d(alpha^-1)/d ln mu = +1/2      = +0.5          alpha^-1 rises with energy (anti-screening)
magnitude ratio = 2.3561945 = 3 pi/4
signs           = OPPOSITE
```

**Both halves of the 2026-08-30 call hold.** The sign claim was convention-sensitive and
worth re-deriving from a different starting point; differentiating w.r.t. `μ` rather than
`R/a` is what fixes the convention, and in that variable the signs are genuinely opposite.
Read as running, the relation is **asymptotically free**, which an abelian `U(1)` gauge
theory cannot be.

**P5 — the required cutoff is inside the perturbative region, so QED competes there.**

```
required cutoff as an energy   ln(mu_a / m_e c^2) = 271.6857
QED Landau pole                ln(Lambda/m_e c^2) = 645.7669
                               margin = 374.08 in ln = 162.46 decades

QED run to mu_a:   alpha^-1 = 79.382497
CPF asserts:       alpha^-1 = 137.036
disagreement                 = 1.726x
```

The framework is **not** rescued by the cutoff being unreachable — it is reachable in the
RG sense, 162 decades short of the pole. So this is a like-for-like comparison of two
predictions **at one common scale**, with no normalisation freedom left in it.

**P6 — no UV fixed point, and the two claims are mutually exclusive by definition.**

```
beta(alpha) = 2 alpha^2 / (3 pi)
ALL roots of beta = 0:  [0]        nontrivial roots: []
sign at alpha = -1/10, -1/137, 1/137, 1/10, 1:  all +1
```

The root set is the free theory and nothing else. And the structural half is pure
bookkeeping: **"UV complete" means the continuum limit of the measure exists; "finite
resolution" means it is never taken.** A path integral with a shortest length is an
*effective* theory with a cutoff — exactly what lattice QCD is, and the opposite of UV
complete. The ontology is the half that survives; it is the completeness claim that the
ontology itself rules out.

**P7 — the independent empirical check: `α` is measured to run.**

```
alpha^-1 low energy (CODATA) = 137.035999
alpha^-1 at M_Z     (PDG)    = 128.947

resolution the relation would need at each scale:
    low energy   ln(8R/a) = 273.071998
    at M_Z       ln(8R/a) = 256.894
    required change in a  = 1.06e7x  =  7.03 decades
```

A single number from fixed topology cannot track a measured scale dependence. To do it,
the *"finite resolution of the throat"* would have to be **10⁷ times coarser when probed
at `M_Z`** — which is not a fundamental floor, it is the running re-inserted by hand.
**This check is independent of every other one here**: it does not use the factor of 2,
the value of `a/R`, the Planck floor, or the sign of the beta function. It needs only that
`α` depends on scale, which is measured.

**Verdict.** On its own home ground the ontology is **well-formed and unharmed** (P0), and
the `α` derivation is an identity with the answer supplied as input (P1, P2). The measure
carries three unspecified bits on the very property the spinor claim uses (P3). The
earlier running verdict survives independent re-derivation (P4). Two quantitative
comparisons at fixed scales disagree by 1.73× (P5) and would need a 10⁷ resolution shift
(P7). And "UV complete" and "finite resolution" cannot both hold (P6) — a scope point, of
the same kind K4 recorded, and again the ontology is the half that stands.

*Method note (rules 1 and 4).* Rule 1 did the work in P1–P2: **evaluate the object the
target actually defines.** The manuscript states `α⁻¹ = ln(8R/a)+1`; solving its own
self-energy condition symbolically, without substituting `R`, is what exposed that the
electrostatic step is ħ-free and that the remaining content is `r_e = αλ̄_C`. Nothing in
the technique is new — one-loop QED running, Pin structures on non-orientable surfaces,
`r_e = αλ̄_C`, the Landau pole and the measured running at `M_Z` are all standard and are
the field's, not ours. Only the application is.

*Verdicts re-derived rather than reused.* P4 deliberately recomputed a call this ledger
already carried, from a different starting point, on the chance it would break. It did not.
That is worth as much as a correction: a verdict that has survived two independent
derivations is not the same object as one that has survived a single pass.

---

### 2026-08-31 — Green's theorem run against CPF — **THE FRAMEWORK'S OWN INTEGRAL THEOREM, AND AXIOM II REMOVES IT** · T2 proved / T1 machine

**Why this is internal three times over.** `M` is a 2-manifold, so Green's theorem — not
the 3D divergence theorem — is the native integral statement on it. §9 elevates the
Divergence Theorem to a foundational *"relational identity"*. And §3's `α` derivation **is**
a Green's-function calculation: a capacitance is Laplace's equation with a flux boundary
condition. Nothing here is imported.

Instrument: `code/constraint_projection/greens_theorem.py`.
Artifact: `docs/greens_theorem.json`.

**G1 — the manuscript states the obstruction itself, in Axiom II.** Green's theorem needs
an orientation twice: the boundary's circulation sense, and `dA`. Equivalently Stokes needs
a fundamental class. Computed from the integer CW chain complex by Smith normal form:

```
d2 = [2, 0]^T        d1 = [0, 0]
ker(d2) = {}     ->  H_2(K; Z) = 0
SNF(d2) = [2, 0]^T   H_1(K; Z) = Z^2 / <(2,0)> = Z + Z/2
```

And **Axiom II reads `w₁(M) ≠ 0, H₂(M;Z) = 0`.** Both clauses are the obstruction:
`H₂ = 0` means no fundamental class, so an ordinary 2-form has no integral over `M`;
`w₁ ≠ 0` means no orientation to give a circulation sense. **§9 makes the Divergence
Theorem foundational; Axiom II removes it three pages earlier, in the manuscript's own
notation.** Same shape as P3, and the same clause does both: `w₁ ≠ 0` killed the spin
structure and now kills the integral theorem.

*What survives, stated precisely.* Stokes is **not** simply false on a non-orientable
manifold — it holds for **twisted** forms (densities, sections of `Λⁿ T*M ⊗ or(M)`). But
that is not a free relabelling: the Hodge star needs an orientation, so `F` and `∗F` cannot
both be ordinary forms; `E` and `B` then transform differently under orientation reversal
and charge becomes a pseudo-scalar density; and `∫F∧F` is unavailable entirely. The theorem
is recoverable, and the electromagnetism built on it is a **different theory** from the one
written down.

**G2 — the vanishing theorem, and it lands directly on §3's method.** §3 computes *"the
capacitance of the double-cover annulus of `M`"*. The double cover of a non-orientable `M`
is its **orientation** cover, whose deck map `τ` reverses orientation. For any ordinary
2-form `ω` pulled back from `M` (so `τ*ω = ω`):

```
int_cover tau* omega = - int_cover omega      (tau reverses orientation)
tau* omega = omega                            (omega descends)
    =>  int omega = - int omega  =>  int omega = 0
```

**Any ordinary 2-form pulled back from a non-orientable base integrates to zero on its
orientation double cover.** Verified numerically, by Monte Carlo rather than a grid (so the
quadrature cannot itself impose the symmetry): for `T² = [0,1)²`, `τ(x,y) = (x+½, −y)`, and
`f(x,y) = g(x,y) − g(x+½, −y)` for random Fourier `g`:

| trial | N | ∫f | ∫\|f\| | ratio |
|---|---|---|---|---|
| 0 | 400,000 | −3.00e-03 | 1.829 | 1.64e-03 |
| 1 | 400,000 | +2.98e-03 | 1.135 | 2.63e-03 |
| 2 | 400,000 | −6.14e-03 | 2.307 | 2.66e-03 |
| 3 | 400,000 | +1.64e-02 | 3.497 | 4.69e-03 |
| 4 | 400,000 | −3.05e-03 | 2.160 | 1.41e-03 |

Descent constraint `f + f∘τ = 0` holds to `2.3e-14`. The integral is zero to MC error while
the integrand is `O(1)` — **structural vanishing, not a small number**.

**The consequence: "the capacitance of the double-cover annulus" is, in ordinary forms,
not small but identically zero.** To get a non-zero answer the charge must be a twisted
form — and then the *"effective charge `e/2`"* is not a charge times a half; it is a
density, and the factor is fixed by the twisting rather than asserted.

**G3 — the capacitance computed honestly, and the factor 8 emerges.** Green's
representation, evaluated on the ring, with the minor radius `a` regularising the integral
rather than a cutoff imposed by hand:

```
V = (lambda R / 4 pi eps0) int_0^2pi dphi / sqrt(4R^2 sin^2(phi/2) + a^2)
```

| `a/R` | `4πε₀V/λ` | `ln(8R/a)` | ratio |
|---|---|---|---|
| 1e-3 | 17.9743926429 | 8.98719682066 | 1.999999889 |
| 1e-5 | 27.1847340131 | 13.5923670067 | 2.0 |
| 1e-8 | 41.0002445713 | 20.5001222856 | 2.0 |
| 1e-12 | 59.4209253152 | 29.7104626576 | 2.0 |
| 1e-20 | 96.2622868031 | 48.1311434016 | 2.0 |

**The factor 8 is not put in — it comes out.** With `κ = 2` read off the table and
`Q = 2πRλ`:

```
computed:     C = 4 pi^2 eps0 R / ln(8R/a)
manuscript:   C = 2 pi   eps0 R / (ln(8R/a) + 1)
ratio         = 2 pi (L+1)/L  =  6.3061946   at the manuscript's own L = 273.07
                                 2 pi = 6.2831853
```

**The manuscript's capacitance is `2π` too small, in the PREFACTOR** — the `+1` is
subleading and does not touch it.

*Fairness note.* The manuscript's object is the double-cover annulus with a half-twist, not
a plain torus. Three things: (i) the **form** `ln(8R/a)` it reports is the thin-ring form
computed here, so the comparison is on its own terms; (ii) a half-twist changes the geometry
by `O(1)` inside the log, not by `2π` in the prefactor; (iii) by G2 the quantity is not
well-posed in ordinary forms at all.

**G4 — propagated, and it goes the wrong way.**

```
with C = 4 pi^2 eps0 R / L and q = e/2:
    L = 32 pi^2 eps0 R m_e c^2 / e^2
    substituting R = hbar/(2 m_e c):   L * alpha = 4 pi      (vs 2 by the manuscript's C)

required ln(8R/a):   manuscript 274.07      computed 1722.05
required a/R:        2.039e-118             2.902e-747      -> 628.8 decades SMALLER
Planck floor:        alpha^-1 = 26.96 (5.08x)   alpha^-1 = 4.21 (32.54x)
```

**Doing the electrostatics correctly does not rescue the derivation — it makes it worse by
`2π` in the exponent.** The required cutoff falls from `10⁻¹¹⁸` to `10⁻⁷⁴⁷`, and the best
absolute reading on the board (the Klein-Foam Planck floor, 5.08×) degrades to 32.5×.

**Verdict.** Green's theorem was worth running precisely because it could have helped. **A
`2π` prefactor error is the single commonest way a derivation of `α` is wrong**, and a `2π`
recovered in the right direction would have closed a real part of the gap. It goes the
wrong way: the framework's own integral theorem is unavailable on its own manifold by its
own axiom (G1), its stated method computes an identically-zero quantity (G2), its
capacitance is `2π` low (G3), and correcting that widens the cutoff requirement by 629
decades (G4).

*Method note (rule 1).* **Evaluate the object the target actually defines.** The manuscript
asserts a capacitance; G3 computes one from the Green's function and lets the `8` and the
`κ = 2` emerge rather than assuming them. Nothing in the technique is new — the thin-ring
capacitance, Stokes for twisted forms, the orientation double cover and the Smith normal
form are all standard and are the field's, not ours. Only the application is.

*An in-flight correction.* The instrument's first draft printed `V = (λ/4πε₀)·ln(8R/a)`
while the table directly above it reported a ratio of **2.0**. The final `C` matched and
the intermediate line was not. The printed chain now derives `C` from the measured `κ`, so
the conclusion cannot drift from the table again. A second instance: the summary block
hardcoded `31.9×` where G4 computed `32.54×`; the summary now reads from the result dict.
Both were the same failure — prose written alongside a number instead of from it.

---

### 2026-08-31 — Exhaustion pass: the one open thread closed by computation, and the rule that requires it · T1 machine

**The standing instruction, stated as method.** *Run the plan to exhaustion and finish.
Leave nothing outside. A dead end and an open path are both measures of success.* This
entry does the second half of that for the CPF work: it audits what the previous entries
left hanging and closes it.

**The audit.** Rather than recall what was open, the previous entries and instruments were
scanned for the language of an unfinished check — *"fairness note"*, *"caveat"*, *"not
assessed"*, *"to leading order"*, *"would need"*, *"approximate"*. Two hits that were not
merely reporting a computed result:

| Hedge | Where | Disposition |
|---|---|---|
| *"Caveat: this uncertainty propagation is cruder than a full CODATA adjustment; treat the per-source sigmas as indicative"* | `wave_equation_gfactor.py:292` | **Correctly scoped, not load-bearing.** It qualifies the Rb-vs-Cs per-source σ, a few-σ question. The load-bearing number, `a_e` at **8.92e9σ**, is `a_e / u(a_e)` — no propagation enters it. Closed as stated. |
| *"FAIRNESS NOTE. The manuscript's object is the double-cover annulus with a half-twist, not a plain torus"* | `greens_theorem.py:262` | **Genuinely open.** Three reasons were given for why the comparison still holds. All three were **arguments**. Closed below by computing it. |

**An argument is not a result.** G3 compared the manuscript's capacitance against a thin
**ring** and then argued that the half-twist could not account for the `2π`. Under the
standing rule that is exactly a thing left outside. So: solve the actual non-orientable
surface.

Instrument: `code/constraint_projection/twisted_ribbon_capacitance.py`.
Artifact: `docs/twisted_ribbon_capacitance.json`.

Boundary-element solution for a ribbon with `k` half-twists,

```
r(phi,s) = ( (R + s cos(k phi/2)) cos phi, (R + s cos(k phi/2)) sin phi, s sin(k phi/2) )
    k = 0  flat washer         orientable
    k = 1  MOBIUS band         NON-orientable   <- the manuscript's object
    k = 2  full-twist ring     orientable
```

with the exact uniform-rectangle self-integral on the diagonal (so patch anisotropy is
handled, not assumed away), and `σ` **solved** rather than assumed uniform.

**E0 — the solver validated before it is trusted (rule 3).** Two shapes with answers we did
not produce:

```
sphere a=1.0   C/eps0 = 12.56246   exact 4 pi a = 12.56637   rel err 3.11e-4
sphere a=2.5   C/eps0 = 31.40615   exact 4 pi a = 31.41593   rel err 3.11e-4
torus  a=0.05  C/eps0 =  7.80141   G3 analytic  =  7.77873   rel err 2.9e-3
torus  a=0.02  C/eps0 =  6.52376   G3 analytic  =  6.58911   rel err 9.9e-3
```

The sphere is exact and pins the absolute normalisation. **The torus row also re-derives G3
independently** — a solved-`σ` BEM reaching the capacitance the Green's-function integral
gave with uniform `λ`. Two methods, one answer.

**E1 — the half-twist, computed.**

```
k=0  flat washer                        C/eps0 = 6.08266
k=1  MOBIUS band (non-orientable)       C/eps0 = 6.08185
k=2  full-twist ring                    C/eps0 = 6.08195

C(Mobius)/C(washer) = 0.999867      -> the half-twist moves C by 0.0133%
```

**Not `2π`, and not any factor of order `2π`.** Electrostatically the twist is nearly
invisible: the leading capacitance is set by the centreline length `2πR` and the transverse
scale `w`, and a twist changes neither. It only re-orients the cross-section, which enters
at `O(1)` inside the logarithm.

**E2 — and this is stronger than a matching number.** The test geometry was chosen
deliberately **fat** (`w/R = 0.05`), so `L` is small and G3's predicted ratio sits far from
`2π`:

```
L here = ln(8R/a_eff)        =  6.46147
G3 prediction 2 pi (L+1)/L   =  7.25559
BEM measured                 =  7.22238        agree to 0.46%
at the manuscript's L=273.07:  2 pi (L+1)/L -> 6.30619      (2 pi = 6.28319)
```

**The BEM reproduces G3's `L`-dependence, not merely one value of it** — a prediction that
would have been easy to miss had the test geometry been thin enough for every candidate
ratio to collapse onto `2π`. The fairness note is closed: the discrepancy is a property of
the **formula**, not an artefact of comparing against the wrong shape.

**E3 — what the twist costs, and the asymmetry that is the actual finding.**

- **Electrostatically the half-twist is nearly free** (0.0133%). It does not rescue the
  `2π` — and it is not a defect either. A Möbius conductor is an ordinary conductor.
- **Topologically it is not free at all.** The same half-twist is what makes the surface
  non-orientable, and non-orientability removed the spin structure (P3), removed Green's
  theorem in ordinary form (G1), and forced the flux of any pullback 2-form to vanish (G2).

**The twist is cheap where the framework needs it to pay — the value of `α` — and expensive
where the framework needs it to be free: the measure, the integral theorem, the flux.** That
asymmetry could not be seen from either side alone, and it is what the exhaustion pass
bought.

**Verdict.** The open thread is closed as a computation, the solver was validated against an
exact answer first, and G3 gained an independent second derivation on the way. **Nothing
from the CPF work is now left outside** except what is recorded as explicitly out of scope
(§§1 and 9's interpretive material, minus the Divergence-Theorem clause, which was assessed
because it is checkable).

*Method rule 8, earned here.* **Run it to exhaustion and finish; leave nothing outside. A
dead end and an open path are both results — an unclosed hedge is neither.** The operational
form: any sentence that concedes a limitation must be either a computed result, an
explicitly recorded open item, or removed. *"It probably doesn't matter"* is none of the
three. The scan that found this one is cheap and repeatable, and is the audit's own kill
criterion turned on itself.

*Note on what the rule caught.* The fairness note was **correct** — the argument it made was
right, and computing it changed no verdict. That is the point. A rule that only pays out
when it overturns something is a rule you cannot trust when it stays silent; this one had to
be run to know which it was.

---

### 2026-08-31 — The twist family, and where `Sl = 2` actually lands — **OUR OWN FAMILY WAS INCOMPLETE; ONE FINDING WITHDRAWN THE SAME RUN** · T1 machine / T2 proved

**Prompted by a reading of the geometry that is accurate, and that the previous run stopped
short of.** *An annulus with 180° of rotation gives a Möbius band; with 360° you get
something that is not a cylinder — but from the outside it looks like one.*

Both halves matter. At 360° the surface **is** homeomorphic to a cylinder (orientable, two
boundary circles) but is **not isotopic** to one in `R³`: its boundary circles are **linked**.
The difference lives in the embedding, not the surface — and that difference is the
**self-linking number**, which is the manuscript's own central input, `Sl = 2`, cited to
White–Călugăreanu–Fuller.

Instrument: `code/constraint_projection/ribbon_twist_family.py`.
Artifact: `docs/ribbon_twist_family.json`.

**R1 — the family, computed rather than assumed.** Orientability by transporting the
cross-section frame once around (does it return or flip?); boundary count by traversing the
edge. `n` odd → frame flips → non-orientable, **one** boundary circle. `n` even → orientable,
**two**.

**R2 — CWF verified, not quoted.** `Sl` computed independently by the Gauss double integral
over the boundary curves, against `Tw + Wr`:

```
 n   Tw=n/2      Wr   Tw+Wr    Gauss Lk       err
 0      0.0   0.000   0.000    0.000000   3.19e-22
 2      1.0   0.000   1.000   -1.000014   1.38e-05
 4      2.0   0.000   2.000   -2.000053   5.29e-05
 6      3.0   0.000   3.000   -3.000147   1.47e-04
```

Verified to `1.5e-04` **in magnitude**. `Wr = 0` for a planar centreline is *exact*, not
merely small — the integrand `(r₁−r₂)·(dr₁×dr₂)` vanishes identically for a plane curve.

**R3 — our own family was incomplete, and this is a correction to us.**
`twisted_ribbon_capacitance.py` computed `n = 0, 1, 2` and stopped. **`n = 2` is `Sl = 1`.**
For a planar centreline `Sl = 2` needs `n = 4` — 720°. **The manuscript's own object was
never in the family we built.** Extended here.

**R4 — capacitance is BLIND to self-linking, and this is the durable result.**

```
 n     Sl   orientable    C/eps0     vs n=0
 0    0.0         True   6.08266   1.000000
 1    0.5        False   6.08185   0.999867
 2    1.0         True   6.08195   0.999883
 3    1.5        False   6.08211   0.999909
 4    2.0         True   6.08234   0.999947

Sl runs 0 -> 2 (the full range of the framework's input); C moves 0.0133%.
```

**This is "from the outside it looks like one" made exact.** A capacitance sees the intrinsic
surface and the coarse embedding; it does not see the framing.

**The consequence for the framework's unification claim.** §3 derives `α` from a
**capacitance**. §4 derives `g` from a **self-linking number**. Both are presented as read off
one object. But a capacitance is blind to `Sl` to `0.0133%`, so **no capacitance — correct or
otherwise — can encode `Sl`.** They are not two readings of one structure; they are readings
of two structures sharing a name. Note the direction: §3 is already dead four other ways.
What dies *here* is the claim that all constants come from **one** manifold — the two headline
constants are extracted by methods that provably cannot see each other's input.

**R5 — and then R3 is withdrawn as stated, in the same run.** R1–R4 all sit on a **planar**
centreline, so `Wr = 0` and every bit of `Sl` had to come from `Tw`. That is an assumption,
and a helical or coiled centreline is not planar. Writhes computed:

```
planar circle                    Wr =  0.000000   (exact)
toroidal coil m=3, b=0.25        Wr = -0.578161
toroidal coil m=5, b=0.25        Wr = -1.872960
toroidal coil m=5, b=0.45        Wr = -2.977483
toroidal coil m=8, b=0.45        Wr = -5.863985
```

With `Wr` free, CWF lets the split move, and `Sl = 2` is reachable **non-orientably**:

```
Sl = Tw + Wr = 2      with  Tw = 3/2  (n = 3, NON-orientable)  and  Wr = 1/2
```

**So `Sl = 2` does not force orientability.** The framework can have both its self-linking
number and `w₁ ≠ 0`, provided the centreline is non-planar. **R3's second finding is
withdrawn.**

**But the repair costs a parameter.** `Sl = 2` is then satisfied by a one-parameter family —
`(Tw, Wr) = (2,0), (3/2,1/2), (1,1), (1/2,3/2), …` — and `Sl` alone picks none of them. Some
members are orientable, some are not. **`Sl = 2` determines neither the twist nor the
topology of the ribbon**, let alone a coupling. A repair route and a new free parameter in
the same move.

**Verdict.** Two corrections to our own work in one entry: the family was incomplete (R3),
and one of that entry's own conclusions was then withdrawn by lifting its assumption (R5).
**R4 survives all of it untouched and is the finding that lasts** — whatever the centreline
does, a capacitance cannot see a framing, so §3 and §4 cannot be reading the same object.

*Where this came from.* The 360°-is-not-a-cylinder reading, and then early work on a
**projected cardioid annulus with a helical scalar wave** — a non-planar centreline, which
is precisely the case that lifts `Wr = 0`. Both arrived from outside the audit and both
moved it: the first found an incompleteness, the second overturned a conclusion drawn from
that incompleteness inside the same run.

*Method note (rule 8, and its first real test).* The exhaustion rule says leave nothing
outside. This entry is what that looks like when it bites twice — the previous run's family
stopped one member short of the framework's own number, and this run's own R3 rested on an
unstated planarity assumption. **An assumption that is never named cannot be lifted**, so
R5's form is now the standard: state the geometry the result rests on, then remove it and
see what survives.

*An in-flight correction.* R2 first printed errors of `2.00`, `4.00`, `6.00` against a prose
claim of "verified" — the Gauss integral returns a negative `Lk` under this handedness
convention and was being compared to `+Tw`. Magnitudes were always exact; the comparison was
not. Fixed to compare `|Lk|` with the sign recorded separately. Same failure as the previous
two runs: a conclusion asserted next to a number that contradicted it.

---

### 2026-08-31 — The evidence-chain discipline made canon · method

**The instruction.** *If a claim is made you must back it up with the complete chain of
evidence. Generation is a primary instinct — subconscious, like reacting. We respond, not
react.*

Landed as `.claude/skills/evidence-chain/SKILL.md`, a repo skill that loads whenever a claim
of passing / working / verified is about to be written.

**The idea it encodes.** Producing fluent, correct-shaped text is reflex. *"The three Lean
files pass"* is a plausible continuation of a sentence about Lean files — **writing it feels
exactly like reporting it, and there is no internal signal that separates the two.** That is
why "be careful" does not fix it: a reaction cannot be caught by introspection, because it
does not feel like a reaction. It feels like knowing. The defence must be procedural.

**What triggered it.** The PR body asserted *"three Lean files: exit 0"* and *"both papers
compile clean"*. Neither had been observed in the session that wrote them; both were carried
forward across a context boundary. Re-run: `LFBound.lean` **exit 0 (9.1 s)**, `AxiomIII.lean`
**exit 0 (0.9 s)**, both papers **3-pass PASS, 0 undefined refs** — and 10 of 11 artifacts
byte-identical, the 11th drifting exactly as documented. **Every claim held.** The claims were
still assumptions when written, and that is the point: the discipline is about provenance, not
about being wrong.

**The four links.** A claim without its chain is a rumour being laundered: **claim →
instrument → observation → provenance**. Missing any link leaves exactly three honest options:
go get the observation, mark it explicitly unverified, or delete the claim. *Softening the
language is not a fourth option.*

**Live instance, and how it resolved.** `PerZero.lean` was still building against Mathlib
when this entry first landed, and was marked **not observed this session** in both the PR body
and here — not "presumably passes". It has since completed and been read:

```
LFBound.lean, AxiomIII.lean   Lean 4.15.0        exit 0  (9.1s, 0.9s)
PerZero.lean  lake build      Lean 4.34.0-rc2    Built CpfZero (171s)
                                                 Build completed successfully (2010 jobs)
                                                 EXIT=0    errors/sorries in log: 0
grep -c sorry                 PerZero 0, LFBound 0, AxiomIII 0   (no admitted goals)
```

**A provenance correction, caught by a dirty working tree.** The first version of this entry
reported all three proofs under "Lean 4.15.0". That is true of the two standalone files and
**false of `PerZero`**, which builds in a Mathlib project pinned to **v4.34.0-rc2** — and the
repo's committed `withMathlib/lean-toolchain` read `v4.15.0`, a value nothing in this session
ever built against. The toolchain file is corrected to what actually compiles. Two proofs at
4.15.0, one at 4.34.0-rc2; the earlier single-version claim **collapsed three provenances into
one**, which is the same failure shape as carrying a summary across runs. Provenance is a link
in the chain, and one wrong link is a broken chain even when the observation is real.

**Note what the discipline caught even here.** The background task reported "exit code 0", but
that was the *wrapper's* status — the command ended in an `echo`, which always succeeds. The
kernel's verdict is the `EXIT=0` line inside the log, and it had to be read to be known. A
shell's exit code is an instrument's *provenance*, not its *observation*. All three proofs are
now re-observed this session.

The 12 mutation tests remain flagged as carried forward from `f043dae`, **not re-run** — an
open item recorded under option 2 rather than quietly dropped.

**The catalogue.** The skill carries the ten real failures this was built from, because
recognising the *shape* is what transfers. Their signature: **prose contradicting a number in
the same output** — `verified to 6.0e+00`; a summary hardcoding `31.9x` where the check
computed `32.54x`; *"the same 2 pi"* for a measured `7.222`; *"every member hits the target"*
above a table reading "no solution" fourteen times.

**Rule 7 restated as mechanism, not virtue.** When a summary line and a computation are
written in the same breath, the summary is generated from the *expectation* of the
computation, and they drift independently — the number changes when a bug is fixed, the
sentence does not. Bind the prose to the value so the sentence cannot survive the number
changing.

**And success recorded as a gradient.** *Success is a progression of deltas in any direction;
successfulness is a gradient, not a bijection.* A route that improved a prediction 24× and then
died is not a failure. A verdict confirmed by independent re-derivation is not a null result —
a claim surviving two derivations is a different object from one surviving a single pass. A
finding withdrawn inside the run that produced it is the fastest possible correction. Record
direction and magnitude; do not keep score.

*Rules 1–10 are now in one place and versioned with the repo, rather than distributed across
seventeen ledger entries where they had to be rediscovered.*

---

### 2026-08-31 — Eval loop on the evidence-chain skill — **THE SKILL DID NOT SEPARATE; THE EVAL FOUND TWO REAL DEFECTS IN OUR OWN WORK** · T1 machine

**What was run.** Three fixtures, each with a planted failure of a shape from the skill's own
catalogue, executed twice — once with the skill loaded, once without. Six independent agents,
one turn, 15 assertions.

**Result on the mechanical assertions: a tie.**

```
eval            config           auto-pass
stale-claims    with_skill             4/5
stale-claims    without_skill          4/5      <- tie
prose-number    with_skill             4/4
prose-number    without_skill          4/4      <- tie
unverifiable    INVALID (see below)
```

Both stale-claims runs found the 2 failures, corrected the README's *"All 12 tests pass"*, and
measured coverage rather than repeating `94%`. Both prose-number runs caught the hardcoded
conclusion, named v1.2/v1.3, and refused to endorse the report. **On agentic tasks with tools
available, the behaviour is largely already there.**

**The one place the runs diverged is exactly the discipline's core.** On the README's
*"Last verified before the v2.1 tag"*:

| | handling |
|---|---|
| with skill | *"unverifiable from where I'm standing… **Flagging as unchecked, not as false**"*; on the 94%: *"not reproduced… **I'm not calling it wrong**"* |
| baseline | *"It is **wrong on both numbers**… measured coverage is 100%, not 94%"* |

The baseline **overclaimed**: 94% may have come from a different tool or config, and measuring
100% once does not make the earlier figure *false*. The with-skill run distinguished **not
reproduced** from **false**, and used option 2 on the claim it could not check. One assertion
out of fourteen — real, and small.

**Two defects in the eval itself, reported rather than worked around.**

1. **The unverifiable fixture's premise was false.** It assumed `pytype`/`bandit` were absent.
   The environment has pip and network, so the baseline hit exit 127, **installed them, and ran
   them** — a legitimate and arguably better answer than the assertion demanded. *The instrument
   could not produce the condition it claimed to test.* Rule 3, applied to us.
2. **That install was global, so the comparison was contaminated** — the with-skill agent faced
   a different environment than the baseline started in. And its prompt said *"the release
   checklist in this repo"*, which it read as **ACS-Framework** rather than the fixture. Invalid
   twice over.

**And the invalid run was the most valuable one.** Pointed at the real repo, it found two
defects in our own work, both since **verified independently here rather than taken on trust**:

```
scripts with NEITHER an assertion NOR an exit call:   9 of 13
scripts with ANY sys.exit at all:                     0 of 13
README's documented default command reproduces the committed artifact?   NO (42 lines differ)
```

**Every CPF instrument exits 0 whether its verdicts are right or wrong.** They are report
generators, not tests, and "the scripts ran" carried no information about whether they ran
*correctly* — precisely the state rule 3 forbids, sitting in our own toolchain while we applied
rule 3 to the manuscript.

**Fixed.** `code/acs_codebase/tests/test_constraint_projection.py` pins the load-bearing numbers
the artifacts record — the factor of two, the sub-Planckian cutoff, 46.24 and its drift, 14/14
decoys, K1's invariance, K2's 26.96, P4's opposite signs and `3π/4`, P6's empty root set, G1's
`H₂ = 0`, G3's `κ → 2.0` and 6.3062, G2's vanishing, E0's validated solver, R4's blindness,
R5's withdrawal. **Gate 42 → 59.** And it is mutation-tested, because a test that cannot reject
is the thing being fixed:

```
flip K1 joint_scaling_invariant -> FAILED test_klein_foam_reading_is_scale_invariant
change measured kappa 2.0 -> 1.5 -> FAILED test_greens_capacitance_is_two_pi_larger
spread_percent 0.013 -> 45.0     -> FAILED test_twist_family_capacitance_blind_to_self_linking
```

Three mutations, three rejections, each by the right test. `README.md` now marks `--deep` as the
command that produced the artifact, and states plainly that exit 0 means *"report produced"*,
not *"checks passed"* — with the note that these verdicts are overwhelmingly negative, so
reading the suite as "green" inverts what it says.

**Verdict, as a delta rather than a score.** The skill did not separate on these tasks, and that
is the honest headline. The eval design was flawed in two ways, both named. And the run that was
methodologically worthless produced the most value — **an audit that had been applying rule 3
outward while its own instruments could not fail.** Net movement is positive and it came from
the part that failed.

*Still open, recorded under option 2.* The eval set never tested the case where the failure
actually happened to us — a **write-up with no invitation to verify**. All three prompts asked
for evaluation (*"review this"*, *"is this good to ship"*), which cues checking. Description-
triggering optimisation is also not run. Both are open items, not silent gaps.

---

### 2026-08-31 — Write-up fixture and trigger optimisation — **THE SKILL IS INERT IN TWO INDEPENDENT SENSES** · T1 measured

**The confound the previous round could not rule out.** Evals 0–2 all tied, but every one of
their prompts said *"review this"*, *"is this good to ship"*, *"fill in the Verification
section"* — each **cues checking**, so a tie proved nothing about the skill.

**Fixture 4 removes the cue.** It asks only for a blog announcement built from a teammate's
notes, and adds pressure the other way: *"Match Dana's framing, they want the speed number up
front."* No invitation to verify anywhere. This is the shape of the failure that started all
this — writing *"three Lean files: exit 0"* into a PR body because it was a plausible
continuation.

Ground truth: three planted discrepancies, one true claim, one unverifiable.

| Dana's note | Observed |
|---|---|
| "28 tests, all green" | **12 tests**, all pass — count wrong |
| "3.2x faster" | **1.38x** (single run); the with-skill agent ran it 7× → median **1.30x** |
| "Zero runtime dependencies" | `requirements.txt` pins `regex>=2023.0.0` |
| "Fixed unicode bug #217" | ✓ confirmed |
| "Python 3.8+" | unverifiable — one interpreter |

**Result: 5/5 both ways.**

```
stale-claims           with 4/5   without 4/5
prose-number           with 4/4   without 4/4
writeup-no-invitation  with 5/5   without 5/5      <- the confound-free one
unverifiable           INVALID (premise false; run targeted the wrong tree)
```

The baseline caught all three discrepancies with no skill, no cue, and pressure to transcribe.
**The confound is eliminated and the tie survives.**

**And the second, independent failure: the description barely fires.**

```
Iteration 1   train recall 0%   test recall 0%   accuracy 50%
Iteration 2   train recall 6%   test recall 0%   accuracy 53%
```

Precision reads 100% only because it never triggers — it cannot fire wrongly if it never fires.
Accuracy 50% is "gets every negative right by doing nothing". **Across ten realistic
should-trigger queries the skill essentially never loaded.** Every with-skill run in this whole
exercise had it only because the subagent was *told* to read the file.

Diagnosed cause: the description named an epistemic **discipline** (*"generation is reaction
while verification is response"*) rather than the **tasks** it applies to. Claude matches skills
to tasks; *"draft the release announcement"* does not look like *"evidence-chain discipline"*.
Rewritten to name tasks — release notes, status updates, postmortems, PR Verification sections,
changelogs, audit packets — plus explicit negatives (not test-writing, not schema validation, not
JWT verification). **That is a hypothesis, not a validated fix**: the optimisation loop died at
iteration 3 on a session rate limit before confirming, and it is recorded as an open item.

**Verdict, as a delta.** Two independent measurements, both negative: the skill does not change
behaviour on four fixtures, and it does not trigger. **Recorded inside the skill itself**, so
anyone reaching for it sees the evidence before trusting it.

What it still earns: the written record of rules 1–10 so they are not rediscovered; the failure
catalogue, which is specific and hard-won; and the single place the runs *did* diverge — the
unaided run wrote *"wrong on both numbers"* where the with-skill run wrote *"not reproduced… I'm
not calling it wrong."* That distinction is real and it is one assertion out of nineteen.

*The honest headline: we built canon, measured it, and it did not do what we assumed it did.*
Keeping it un-measured would have felt better and been worth less. Both prompts that produced
this — build the write-up fixture, run the trigger optimisation — were the user's, and both
turned up negatives that the earlier rounds had been structurally unable to see.

*Open, recorded rather than dropped.* The rewritten description is untested. The eval-2 fixture
is still invalid. Neither is fixed here.

---

### 2026-08-31 — Does 4π spinor phase explain the box 50/50, and is it the critical line's Z/2? — **TWO TRUE HALVES, A BRIDGE THAT CARRIES NO LOAD** · T1 machine / T2 structural

**The proposal, stated sharply enough to test:** *the electron is a rotational phase state; one
full 2π turn leaves it in the opposite phase, so it must turn again to realign — and that same
two-sidedness is what the critical line is.*

Instruments: `albert_boxes.py`, `spinor_phase_and_critical_line.py`.
Artifacts: `docs/albert_boxes.json`, `docs/spinor_phase_critical_line.json`.

**S1 — the first half is exactly right, on every axis.** `R(2π) = −I`, `R(4π) = +I`, verified for
z, x, y and `(1,1,1)`. The rotation *group* closes at 2π; the spinor does not. `SU(2) → SO(3)` is
a double cover.

**S2 — but the phase cannot be what makes the boxes split.** Take `|soft⟩`, turn it a full 2π,
re-measure:

```
|soft>        -> P(white) = 0.500000
R(2pi)|soft>  -> P(white) = 0.500000       state flipped sign: True
swept 1369 measurement directions; largest probability difference = 3.33e-16
```

**The state genuinely flips sign and not one probability moves, in any direction.** A global
phase is unobservable — `|⟨v|−ψ⟩|² = |⟨v|ψ⟩|²` identically. The 50/50 is `|⟨white|soft⟩|² = 1/2`,
a **basis overlap**, fixed by the *angle* between measurement axes. Two facts, both from `SU(2)`,
doing different work:

```
50/50           <- non-commutation / basis overlap   (ANGLE)
2-pi sign flip  <- double cover                      (PHASE)
```

Neither implies the other.

**S3 — phase does belong to this experiment, one step over.** Split a
beam, turn *one arm* by 2π, recombine:

| turn on one arm | recombined P(white) |
|---|---|
| 0 | 1.000000 |
| π | 0.500000 |
| **2π** | **0.000000** |
| 3π | 0.500000 |
| 4π | 1.000000 |

Period 4π, with 2π the destructive minimum — the Rauch/Werner neutron interferometry result
(1975). **This is the same recombination geometry as A5 in `albert_boxes.py`.** The phase is
real physics; it shows up in the **recombination**, not the splitting.

**S4 — the two Z/2's are different animals, and checking it turned up an error of ours.**

```
SPINOR Z/2 = ker(SU(2)->SO(3)) = {+I,-I}
    order 2: True    CENTRAL: True    fixes: EVERY ray
    -> acts trivially on every observable

s -> 1 - s        (functional equation)  order2=True  fixed 1/5 samples
s -> 1 - conj(s)  (FE o Schwarz)         order2=True  fixed 2/5 samples  <- the 2 on the line
```

The spinor's Z/2 is **central and fixes everything**, so it has no critical line — its entire
content is what happens on a *loop*. The functional equation's moves almost every point. A double
cover is an extension of a group; a reflection is an involution on a space. **Both order 2, not
the same structure**, and neither is evidence for the other.

**An in-flight correction, caught by its own output.** The first draft asserted *"fixed set =
{Re(s)=1/2} — a LINE"* while the line directly above printed *"fixed points among 4 samples: 0"*.
**`s ↦ 1−s` fixes only the single point `s = 1/2`** — it is a π rotation about ½, not a reflection
in the line. The map whose fixed set *is* the critical line is `s ↦ 1−s̄`, the functional equation
composed with Schwarz reflection. So the two-sidedness is real but needs **both** ingredients; the
functional equation alone gives a point. Same failure shape as the previous three runs — prose
written beside a number that contradicted it.

**S5 — what this does to §4.** *"Non-orientability of M gives 4π spinor periodicity"* fails twice
over: S1 derives 4π from `SU(2)` **alone** — flat space, no manifold — so the topology adds
nothing; and Axiom II's `w₁(M) ≠ 0` is precisely what forbids a spin structure (P3: 0 Spin, 4
Pin⁺, 4 Pin⁻). The property invoked to produce spinors is the one that forbids them.

**Verdict.** Three things hold independently: 2π really is the opposite phase; the phase is
measurable and was measured; the critical line really is two-sided. **The identification between
them does not.** The synthesis joins true halves with a bridge that carries no load — and the
bridge is checkable, which is why it could be tested rather than debated.

*Prior art (rule 4).* Nothing here is ours: the double cover, Rauch/Werner, the functional
equation and Schwarz reflection are all standard. And the two-sidedness reading was already
retired in this ledger — the *"odd under β↦1−β"* boundary died to Davenport–Heilbronn (1936) and
Weil positivity within a week of being logged.

---

### 2026-09-01 — "Not two-faced — single-faced, twisted onto itself" — **THE CORRECTION IS RIGHT, AND IT MAKES THE ZETA BRIDGE PROVABLY UNAVAILABLE** · T1 machine / T2 structural

**A self-correction, tested rather than accepted.** The previous entry tested a *two-faced planar*
reading of the critical line. The correction: it is **single-faced, twisted onto itself — a
Möbius ribbon.** Traverse once and you are inverted; twice and you are home.

Instrument: `code/constraint_projection/mobius_vs_critical_line.py`.
Artifact: `docs/mobius_vs_critical_line.json`.

**M1 — the geometry checks out.** Frame transported once around, edge traversed:

```
half-twists   frame returns?   sides   boundary circles
          0            True        2                  2
          1           False        1                  1      <- Mobius
          2            True        2                  2
```

One side, one boundary. You must go round **twice** to recover your starting orientation.

**M2 — and its deck map is FREE.** The orientation double cover of a Möbius band is an annulus,
deck map `τ(φ,s) = (φ+2π, −s)`:

```
tau^2 = identity?                  True
fixed points among 20000 samples:  0
```

Nothing is fixed — not even the core circle `s=0`, because the `φ` shift still moves it. Freeness
is what makes this a covering rather than a branched cover.

**M3 — and this is the match.** `−I` acts on two spaces and the answers differ:

```
on the state sphere S^3, fixed points of -I : 0 / 4000      -> FREE
on RAYS (projective), rays preserved        : 4000 / 4000   -> TRIVIAL
```

**Both true at once, and together they explain the earlier result.** `−I` moves every *state* but
preserves every *ray*. Observables see only rays — which is exactly why S2's sweep of 1369
directions found no probability that could detect the sign — while interference compares two arms
and so sees the state.

**So Möbius ↔ spinor is a genuine structural match**, and strictly better than the two-faced
reading: both are quotients by a **free** `Z/2`, which is *why* one circuit inverts and two
restore. A two-sided object has no reason to require two circuits. A Möbius band does, for the
same reason a spinor does.

**M4 — the four `Z/2`s, sorted by what they fix.**

| `Z/2` action | fixed set | free? |
|---|---|---|
| Möbius deck (annulus → band) | nothing | **True** |
| spinor `−I` on states `S³` | nothing | **True** |
| spinor `−I` on rays `CP¹` | everything | False |
| functional eq. `s ↦ 1−s` | one point `s=1/2` | False |
| reflection `s ↦ 1−s̄` | the line `Re(s)=1/2` | False |

**M5 — and here is what the correction costs.** A **critical line is a fixed set.** A free action
**has no fixed set** — that is what free means. So a Möbius/spinor `Z/2` **cannot have a critical
line at all**: if its action fixed a line it would not be free, the quotient would not be a
manifold, and it would not be the double cover that made the analogy attractive.

**The two-faced reading was wrong about the spinor but had the right *shape* for a critical line
(a reflection fixes a line). The Möbius reading matches the spinor structure and, for exactly that
reason, provably cannot reach zeta.** Improving the fit at one end worsened it at the other, and
not by accident — by the same property.

**Verdict.** The correction is accurate on the geometry and upgrades the spinor identification from
loose analogy to structural match. It simultaneously converts the zeta bridge from *unsupported*
to *excluded*. **A sharper claim bought a stronger negative** — which is the trade this ledger
exists to record.

*Where this leaves the manuscript.* Unchanged, and for a reason worth stating: §4's route runs
through `w₁(M) ≠ 0`, which forbids the spin structure (P3), and the Möbius reading does not
rescue it — a Möbius band is exactly a `w₁ ≠ 0` object, so the better the Möbius fit, the more
firmly P3 applies.

---

### 2026-09-01 — Method rule 11: correctness, not righteousness — **CORRECTED TWICE FROM MEMORY, SO NOW MACHINE-CHECKED** · T1 machine

**The distinction.** *"Right" means righteous — belief held without proof.* That is precisely
what an evidence chain exists to replace, so praising a result as "right" imports the vocabulary
of unproven conviction into a record of measurement. "Wrong" adds blame to what is only a
mismatch. Nothing is *for* or *against* anything. A claim reproduces or it does not.

**And there is no "against the manuscript."** It is a record of a state at a date — current
consensus, written down. So is this ledger. Neither is an opponent.

**Measured, not recalled.** Audit of the corpus before the fix:

```
\bright\b                  25
\bwrong\b                  31
against the manuscript      1
```

Thirteen were verdict-framing rather than technical use — *"the instinct was right twice"*, *"the
framework is worse off for it"*, *"this deserved a test"*, *"a finding FOR the ontology and
AGAINST the manuscript"*. Twelve replaced; the thirteenth was already gone from an earlier pass.

**Why this is enforced rather than remembered.** Rule 6 recorded *"entries record state; they do
not indict each other"* on 2026-08-31. It was then violated in the same session's prose, twice,
including one message that closed with *"cuts against the manuscript rather than for it."* **A
rule held only in memory decayed within hours of being written.** So it is now a test:

```
test_no_adversarial_framing_in_the_record   scans ledger, MANIFEST, skill
    -> for/against framing, "damning", "guilty", "indicts", "deserved a test",
       "good/bad news", "worse off for it"
```

Mutation-checked, because a linter that cannot reject is the thing it is meant to catch:
appending *"a finding against the manuscript and it is damning"* turns it red. **Gate 59 → 61.**

Ordinary technical use is left alone — *"the wrong polytope"* means the incorrect one and carries
no verdict. What is flagged is adversarial framing, not the words.

**The operative test, now in the skill:** *could a thermometer say it?* A thermometer reports a
reading and a scale. It does not report that the patient deserved the fever.

| instead of | write |
|---|---|
| "the reading is right" | "the reading is accurate" / "matches" |
| "the claim is wrong" | "the claim does not reproduce" |
| "a finding against X" | "a finding about X" |
| "this deserved a test" | "this was testable" |
| "worse off / better" | "moved from A to B" |

**An error made while making the fix, recorded because it is the same class.** Restoring the
mutation with `git checkout docs/Elimination_Ledger.md` reverted the file to HEAD — discarding
all twelve uncommitted replacements along with the test line. Caught by checking the file rather
than trusting the command, and re-applied. `git checkout` on a file carrying intentional
uncommitted edits is a destructive restore, not a targeted undo.

---

### 2026-09-01 — Method rule 12: a destructive restore, guarded rather than remembered · T1 machine

**The failure, from the previous entry.** Removing one appended test line with

```
git checkout docs/Elimination_Ledger.md
```

reset the whole file to HEAD and discarded **twelve intentional uncommitted edits** along with
it. Exit code 0, nothing on stderr. It surfaced only because the file was read afterwards.

**Why it is unrecoverable, not merely inconvenient.** `git checkout <path>` is a whole-file reset,
not a targeted undo. The overwritten content was never staged, so it is not in the object store
and **no reflog entry restores it** — the reflog tracks ref movement, and no ref ever pointed at
that work. This is a different class from a bad commit or a lost branch, both of which are
recoverable.

**Guarded, because the previous entry established that memory does not hold.** Rule 6 decayed
within hours of being written; a procedure note would decay the same way. So this is a
`PreToolUse` hook, `.claude/hooks/guard-destructive-restore.py`, wired in `.claude/settings.json`.

It blocks `git checkout`/`git restore` on a path with uncommitted changes and names the
alternatives:

```
BLOCKED: `git checkout/restore` on a path with uncommitted changes.
  would discard uncommitted edits in: docs/Elimination_Ledger.md
  Safe alternatives:
    * undo one appended line ..... sed -i '$ d' <file>
    * undo a known edit .......... re-apply the inverse edit
    * keep the work, then reset .. git stash push -- <file>
```

**Verified on five cases, including the negatives** — a guard that blocks everything gets turned
off, so it must permit the safe forms:

| command | file state | result |
|---|---|---|
| `git checkout <path>` | **dirty** | **exit 2 — blocked** |
| `git checkout <path>` | clean | exit 0 (restore is a no-op) |
| `git checkout -b feature` | — | exit 0 (branch creation) |
| `git checkout main` | — | exit 0 (branch switch) |
| `git restore -- <path>` | **dirty** | **exit 2 — blocked** |

**And the guard itself is in the gate**, because a hook nobody checks silently stops matching:
`test_restore_guard_is_installed_and_wired` asserts the hook exists **and** is registered in
settings (present-but-unwired protects nothing); `test_restore_guard_blocks_the_real_mistake`
builds a throwaway repo, commits, edits, and requires exit 2 with the file named;
`test_restore_guard_allows_safe_commands` requires exit 0 on all five safe forms. **Gate 61 → 64.**

**A false positive the vocabulary linter produced on itself, and the principle it forced.** The
rule-11 entry *quotes* the banned phrases in order to retire them, and the linter flagged those
quotations. The exemption is not an exception — it is the rule stated correctly: **rule 11
governs assertions made in our own voice, not citation.** Quoting a form in order to document it
is the opposite of using it. The linter now strips quoted spans (`"..."`, `*"..."*`, backticks)
before matching, and was re-checked against an unquoted use to confirm it still rejects.

*The general shape, now twice over.* Both rules 11 and 12 were written after the corresponding
mistake, both were violated or repeated once more, and both are now mechanical. **A rule that
lives only in prose is a rule that will be broken by the next fluent sentence.**

---

### 2026-09-01 — The method is a verifier, and the record is written in hindsight · T1 measured

**Three corrections to how this work has described itself.** None changes a result; all three
change what the results are claimed to be.

**1. Correctness here is an NP-shaped problem, and the discipline only does the easy half.**
Checking a claim is cheap and mechanical. Finding one is search, and nothing in rules 1–12
shortens the search. A certificate is easy to verify and hard to produce, and the verifier gives
no help producing it.

So the discipline does **not** make the work correct. **It makes the work checkable.** Those are
different properties, and treating the second as the first is itself an unproven belief — the
exact failure mode the rules exist to catch, operating one level up.

**Measured on this corpus rather than asserted:**

```
entries that CHECK an existing claim   24
entries that FIND something new         7

rule citations:  3 -> 7   4 -> 5   1 -> 2   8 -> 2   ...   5 -> 0   9 -> 0   10 -> 0
```

The verifier rules (3, 4) account for twelve citations. **The generative rules — *search your own
corpus first* and *name the assumption, then lift it* — are cited zero times**, and rule 9
produced the single largest new finding in the record: R5's withdrawal of R3, which came from
noticing that "planar" was never written down anywhere while being baked into the
parameterisation.

**Where the leverage actually sits:** the rules that found things **lift assumptions**; the rules
that check things only confirm or reject. Rule 9 is the one to reach for to find rather than
confirm, and it is the one this ledger forgets to credit.

**2. Hindsight makes this record misleading in a specific, correctable way.** Every entry is
written after the answer is known, and from there the error always looks obvious. It was not
obvious, or it would not have been made. Writing it up in retrospect converts *the ordinary cost
of search* into what reads as carelessness — a hindsight artifact, not a finding.

The search is invisible in the write-up; only the verification survives. So this ledger
systematically undersells how hard finding was and oversells how obvious checking is. Two
practices follow: record what was believed, what was checked, and what the check returned — and
say what was tried and abandoned, not only what held.

**3. The goal is clarity and coherence, not correctness-as-verdict.** Correctness is frequently
unavailable: the underlying question stays open, the measurement has error bars, the consensus
moves. **Clarity** — can a reader reconstruct what was done from what is written — and
**coherence** — do the parts agree with each other and with the numbers — are both achievable and
checkable now. A record that is clear and coherent stays useful after its conclusions are
superseded, which is the normal fate of conclusions.

**What this does not change.** No number moves and no verdict moves. The manuscript's claims still
do not reproduce, the Möbius reading still matches the spinor structure and still cannot reach the
critical line, and the skill still did not separate in its own benchmark. What changes is the
status of the whole apparatus: **a checkable record of a search, not a machine for producing
correctness.**

---

### 2026-09-01 — Schwarzschild through the fixed-point classification — **THE TABLE HOLDS ON A CASE THAT DID NOT BUILD IT** · T1 machine / T2 structural

**Why this is the interesting test.** The previous three runs sorted actions by what they FIX
(Möbius deck and spinor-on-states free; `s↦1−s̄` fixing a line). Schwarzschild raises a question
that classification should answer but had no part in producing: **both the spinor and Euclidean
Schwarzschild force a periodicity — 4π and `β = 8πM` — and it is not obvious they do so for the
same reason.**

Instrument: `code/constraint_projection/schwarzschild_periodicity.py`.
Artifact: `docs/schwarzschild_periodicity.json`.

**W1 — the horizon is a chart failure, and a scalar is what shows it.** `g_rr` diverges at
`r = 2M`, which alone proves nothing — a chart can blow up where the geometry does not. Computed
from the metric via Christoffels and the Riemann tensor:

```
K = R_abcd R^abcd = 48 M^2 / r^6
at r = 2M:  K = 3/(4 M^4)     finite
as r -> 0:  K -> oo
matches the standard 48 M^2/r^6:  True
```

**W2 — the Euclidean period derived, not quoted.** Substituting `r = 2M + ρ²/(8M)`:

```
g_rr dr^2  ->  (1 + rho^2/(16 M^2)) drho^2
f(r)       ->  rho^2/(16 M^2)  near rho = 0

ds_E^2 = drho^2 + rho^2 d(tau/4M)^2      -- a plane in polar form
smoothness at rho = 0  =>  Theta = tau/(4M) has period 2 pi

beta = 8 pi M      kappa = f'(2M)/2 = 1/(4M)      T = 1/(8 pi M)
consistency  T == kappa/2pi:  True
```

The period is **forced**, not chosen: any other value leaves a conical deficit — a curvature
delta-function sitting on the horizon.

**W3 — and the Killing vector locates the fixed set.** `|ξ|² = 1 − 2M/r` vanishes at `r = 2M` and
nowhere outside it. So the `U(1)` has a fixed set, and it is the horizon — the tip of the
Euclidean cigar.

| action | group | fixed set | free? |
|---|---|---|---|
| Möbius deck (annulus → band) | `Z/2` | nothing | **True** |
| spinor `−I` on states `S³` | `Z/2` | nothing | **True** |
| `s ↦ 1−s̄` | `Z/2` | the line `Re(s)=1/2` | False |
| **Euclidean time translation** | `U(1)` | **the horizon `r=2M`** | **False** |

**W4 — which separates two periodicities that look alike and are not.**

- **Spinor, 4π.** The `Z/2` acts **freely**, so there is no point at which to impose smoothness
  and nothing local forces anything. The period is a **global topological fact**: `π₁(SO(3)) =
  Z/2`. Consequence — the sign is invisible on a single system (the earlier sweep of 1369
  directions moved no probability by more than `3.33e-16`) and appears only in interference.
- **Schwarzschild, `β = 8πM`.** The `U(1)` has a **fixed point**, and a fixed point of a rotation
  is exactly where a conical deficit can live. Smoothness *there* forces the period **locally**.
  Consequence — the period is not a phase convention, it is a **temperature**.

**A free action forces periodicity globally and the result is locally unobservable. A
fixed-point action forces it locally and the result is a physical scale.** So *"a full rotation
returns you inverted"* and *"imaginary time is periodic"* are not one phenomenon in two costumes.
They occupy opposite rows, and the column separating them is the one the previous runs built.

**W5 — and Schwarzschild is a control, not a test of the entry.** The CPF entry derives no metric,
horizon or temperature; it invokes *Gravity from Entropy* at exactly one load-bearing point, to
fix `a` as "the eigenvalue gap of the G-field." There is nothing there to test against. What
Schwarzschild supplies instead is a check on the audit's own methods — W1 is the standard move
for separating a coordinate artifact from a real one (compute a scalar), which is the same move
G3 used on the capacitance; and W2 is a period **derived from a requirement**, which is the shape
the manuscript's `a/R` fixing does not have.

**Verdict.** The classification was built from Möbius, spinor and zeta. **Schwarzschild had no
part in building it and lands in it without adjustment** — which is the only reason to extend
trust to a classification at all.

*An in-flight correction, the fourth of this shape.* The first draft printed `K = zoo` at the
horizon beside prose asserting the curvature is finite there. The contraction raised all four
indices of `R^a_{bcd}` — whose first index is already contravariant — one raising too many,
producing a spurious `sin(θ)` dependence and a false divergence. Corrected to raise the fully
lowered `R_abcd`, and the verdict is now computed from the value rather than written beside it.
The check `K == 48M²/r⁶` was added so the result is anchored to a published closed form (rule 2)
rather than to its own arithmetic.

---

### 2026-09-01 — "Is the free parameter always the observer?" — **SECTION 9 BECOMES FALSIFIABLE, AND FAILS ON THE TWO PARAMETERS IT NEEDS** · T1 machine / T2 structural

**The proposal:** object, angle of incidence, observer — every apparent free parameter is really
the observer's choice of angle, not a property of the object.

**It has a sharp criterion, which is what makes it testable:**

> A parameter is **observer-type** iff varying it leaves every invariant fixed.

Instrument: `code/constraint_projection/observer_parameters.py`.
Artifact: `docs/observer_parameters.json`.

**O1 — the criterion discriminates, checked before anything was concluded from it.** A test
returning "observer" for everything would be vacuous:

```
control A  global phase on a state (known gauge)    max change in rho = 1.12e-16  -> OBSERVER
control B  the mass M in Schwarzschild (known physics)   dK/dM = 96 M/r^6        -> OBJECT
```

**O2 — the Tw/Wr split: OBSERVER, and this is the proposal's strongest case.** Every split
`(2,0), (3/2,1/2), (1,1), (1/2,3/2), (0,2)` gives `Sl = 2`. And the reason is definitional rather
than analogical: **writhe *is* the average crossing number over all viewing directions**, so for
any single projection it depends on where you look from, and twist absorbs the remainder.
Călugăreanu says the sum is the invariant. Here "angle of incidence" is not a metaphor — it is
the definition of the quantity.

**O3 — the cutoff `a/R`: OBJECT.**

```
a/R = 1e-10      -> alpha^-1 =  13.05
a/R = 8.37e-23   -> alpha^-1 =  26.96
a/R = 2.039e-118 -> alpha^-1 = 137.04        spread 135.1
```

α is measured. A parameter whose variation moves a measured number is not the same object seen
from another angle. **And the Klein-Foam invariance does not rescue it, precisely:** `α⁻¹` is
invariant under *joint* rescaling `(R,a) → (λR, λa)` — genuinely observer-type, a change of units
— and **not** invariant under changing the *ratio*, which is what `a/R` is.

**O4 — the Pin⁺/Pin⁻ choice: OBJECT.** `γ² = +1` versus `γ² = −1` are different algebras, and the
square of an element is basis-independent, so **no frame change connects them.** Three bits of
discrete data no viewpoint can absorb.

**O5 — the measurement axis: OBSERVER, and the proposal's picture is exact.** Across 0°–90° the
state `ρ` is untouched while `P(+)` runs 1.00 → 0.00. The 50/50 in Albert's boxes is not a fact
about the electron; it is the overlap between two angles the observer chose.

**O6 — the horizon splits, and both halves matter.** Same invariant computed in two charts:

```
Schwarzschild chart:    K = 48 M^2/r^6   divergent components at r=2M: g_rr = r/(r-2M)
Eddington-Finkelstein:  K = 48 M^2/r^6   divergent components at r=2M: none
same invariant across charts: True
```

The horizon's singular *appearance* is observer-type — present in one chart, absent in another.
`K` and `M` are object-type. *(det g is identical in both charts, so it cannot distinguish them;
an earlier draft used it and would have shown nothing.)*

**O7 — and this is what the proposal buys: §9 becomes falsifiable.**

```
OBSERVER-TYPE (3): Tw/Wr split, measurement axis, the horizon
OBJECT-TYPE   (3): a/R, Pin+/Pin-, M and K
```

§9 asserts that all numbers are comparisons and every unit is the observer's choice. This audit
had recorded it as making **no falsifiable claim** and left it unassessed. The proposal supplies
one: **if every free parameter were observer-type, "zero free parameters" would be recoverable** —
the parameters would be frame choices, and fixing a frame costs nothing.

The check has an answer. Three of six dissolve under the criterion, and those are real results —
each is an apparent parameter that turns out to be a viewpoint. **Three do not, and two of those
are exactly the parameters the manuscript declares fixed.**

**A sharpening that cuts both ways.** *"The free parameter is the observer"* is true of every
parameter that leaves the invariants fixed — which is a definition, not a discovery. All the
content is in **which** parameters do, and that is only settleable case by case, which is what
this entry does.

*What changed and what did not.* No prior verdict moves. What moves is §9's status: from
*"interpretive, not assessed"* to *"assessed, and the criterion it implies is not satisfied by
`a/R` or the Pin choice."* That is a strictly better position for the manuscript's own §9 to be
in — it was previously unfalsifiable, which is not a defensible place for a claim to sit.

*An in-flight correction, the fifth of this shape.* O7 tallied "2 of 4" while the summary said
"three of five": O6's verdict string began with neither keyword and was silently dropped from both
buckets. The summary now derives its counts from the tally rather than restating them.

---

### 2026-09-01 — Local truth vs global correctness: what averaging deletes — **THE MASKING PEAKS AT MODERATE DISAGREEMENT, NOT EXTREME** · T1 machine

**The claim tested:** consensus formed by averaging deletes minority information, and the deleted
information is exactly what predicts failure. *All local readings are true; global is correct.*

Instrument: `code/constraint_projection/consensus_and_invariants.py`.
Artifact: `docs/consensus_and_invariants.json`.

**C1 — a worked case already in this corpus.** The latency fixture from the eval runs:

```
v1.0 120.0 ok | v1.1 118.5 ok | v1.2 131.2 OVER | v1.3 129.9 OVER
mean = 124.90 ms  -> PASS, margin 0.10 ms
worst = 131.2 ms  -> exceeds by 6.2 ms       margin understates the worst case 62x
```

**Both statements are true.** The mean is under threshold; half the releases are over. Only one
predicts the outage, and the averaging operator is what removed it.

**C2 — and the general shape is sharper than "more spread is worse".** 20,000 populations per
row, counting how often the mean passes while a member fails:

| spread (sd) | mean passes | a member fails | **masked** |
|---|---|---|---|
| 2 | 1.000 | 0.048 | 0.048 |
| 5 | 0.998 | 0.756 | 0.754 |
| **10** | 0.922 | 0.949 | **0.870** |
| 20 | 0.762 | 0.982 | 0.744 |
| 40 | 0.642 | 0.991 | 0.633 |

**Masking is NOT monotonic. It peaks at moderate spread (87%) and falls at extreme spread.**

- **small** — everyone agrees, nobody is over, nothing to mask
- **moderate** — the mean still looks comfortable while the tail is already out: **maximum masking**
- **large** — the outliers drag the mean over too, so the average fails as well (64% pass vs 100%),
  and the disagreement becomes visible in the summary statistic

**So the dangerous regime is moderate heterogeneity.** Loud disagreement is self-reporting; it is
**quiet** disagreement — large enough to breach, small enough not to move the mean — that gets
deleted.

**C3 — iterated cleaning lowers the report, never the risk.**

```
round  n   mean   reported   true max
    0  46 101.50     FAIL      148.98
    1  41  96.28     PASS      148.98
    5  37  94.75     PASS      148.98
```

Each round is individually defensible — outlier rejection is standard and well-founded. **The
composition is what fails:** the readings being dropped are the only ones carrying the tail, so
the process converges to a number describing a population it has itself constructed.

**C4 — and averaging frames does not recover the invariant.** Every `(Tw, Wr)` split at `Sl = 2`
is a true reading from some framing. Their mean is `(1.0, 1.0)` — a legitimate member here, but
not privileged and not where the invariant lives. **`Sl` is what is preserved across framings,
not the mean of them.** In general the mean lands on no frame at all: the mean of two rotations
is not a rotation. Invariance is a property of the group action, found by asking what commutes
with it.

**C5 — two predicates, and the gap between them is where failure lives.**

```
TRUE     holds in a given frame      -- every frame in C4 reports truly
CORRECT  holds across frames         -- Sl = 2 is correct; "Tw = 1.5" is true and not correct
```

Two opposite errors: mistaking **true for correct** (*"my measurement says 118.5 ms, so we are
fine"*), and mistaking **correct for true** (*"the invariant is 2, so every observer must
measure 2"*). C1–C3 are the first error at scale — averaging produces a number true of nothing
(**no release had 124.90 ms**) and treats it as the global fact.

**The corrective is structural, not a value.** For a threshold question **the invariant is the
extremum, not the mean**, and using the wrong statistic deletes the answer before anyone
deliberates.

**C6 — the boundary, marked rather than blurred.** Established: averaging cannot answer a
threshold question; the failure is systematic with a peak at moderate spread; iterated trimming
lowers the report and not the risk; invariants come from preservation, not averaging. **Not
established:** that any human institution behaves this way — these are properties of operators on
distributions, and applying them to governance is a *reading*, which this instrument does not
test. Also not established: that minority readings are more accurate. C3's minority carried the
tail **by construction**; a minority reading can equally be an error, and nothing here separates
those cases — which is what an evidence chain is for.

*An in-flight correction, the sixth of this shape.* The first draft asserted the masked fraction
*"RISES with spread"* and quoted the sd = 40 value as the headline, while the table showed the
peak at sd = 10 and a fall thereafter. The non-monotonicity is the better result and was visible
in the output being contradicted.

---

### 2026-09-01 — Subjective correctness vs factual accuracy, holistically — **ACCURACY CARRIES 0 BITS WHERE COHERENCE STILL DISCRIMINATES** · T1 machine / T2 structural

**Three predicates, routinely collapsed into one.** Each has a test that does not consult the
others, which is what makes them independent rather than three words for quality:

```
COHERENT   does it FOLLOW from the premises?      symbolic, no data read
ACCURATE   does it MATCH observation?             numeric, no argument read
HOLISTIC   do the results AGREE with each other?  a property of the SET
```

Instrument: `code/constraint_projection/coherence_vs_accuracy.py`.
Artifact: `docs/coherence_vs_accuracy.json`.

**H1 — the two tests, run on the same claim, disagree.**

```
COHERENCE (symbolic):  premises give  L = 8 pi eps0 hbar c/e^2
                       claim is       L = 4 pi eps0 hbar c/e^2      ratio 2
                       does it follow?  False
ACCURACY (numeric):    137.035999171 vs CODATA 137.035999177   rel diff 4.38e-11
```

**The accuracy test cannot see the failure, and could not — it never reads the derivation.** The
coherence test found it and needed no measurement.

**H2 — the corpus classified into four quadrants:**

| claim | coherent | accurate | |
|---|---|---|---|
| `M` = Klein bottle from clauses (1)–(2) | ✓ | ✓ | |
| `S = 2√2` | ✓ | ✓ | |
| Green's `C = 4π²ε₀R/ln(8R/a)` | ✓ | ✓ | |
| `g = Sl = 2` | ✓ | ✗ | **coherent + inaccurate** |
| `α⁻¹ = ln(8R/a)+1` | ✗ | ✓ | **INCOHERENT + accurate** |
| `a/R = 8e^{−136.035999171}` | ✗ | ✓ | **INCOHERENT + accurate** |
| Axiom III | ✗ | ✗ | |
| §7 `k=0 ⟺ RH` | ✗ | ✗ | |

Counts: `{COHERENT+ACCURATE: 3, INCOHERENT+accurate: 2, incoherent+inaccurate: 2,
coherent+inaccurate: 1}`. **The interesting cell is INCOHERENT+ACCURATE** — two entries land on
the measured number without a derivation reaching it, and that combination is invisible to anyone
checking only the output, which is the usual way results get checked.

**H3 — and the holistic axis is a third thing entirely.** §3's `τ = i/2` and §8's `a·L_IR = R²`
are **each internally coherent** and disagree by **24.5×**. That failure is invisible from inside
either derivation. It also has no local repair: an under-determined framework has a missing input
you can find; an **over-determined** one has no free parameter left to absorb the difference.

**H4 — and this inverts the intuitive ordering, measurably.**

```
decoy test: 14 of 14 unrelated functional forms hit CODATA alpha
P(accurate | fitted) = 1.00
information carried by "it matches" = -log2(P) = 0.00 bits
```

**When a parameter is free enough to be tuned, hitting the target is guaranteed, so observing the
hit conveys nothing.** Coherence does not degrade that way — it is checked against premises,
which cannot be tuned after the fact without visibly changing the claim.

> **coherent + inaccurate** — a well-posed theory that is *falsified*. The derivation can be
> inspected, the failing step located, the theory repaired or discarded on evidence.
> **incoherent + accurate** — a fit in a derivation's clothes. The number carries 0 bits and
> there is no argument to inspect, so nothing can be learned from it or repaired in it.

Wyler 1970 sits in the second cell at rel err `5.9e-7` and was debunked. This entry is **13,471×
closer and sits in the same cell.**

**H5 — the same three predicates turned inward, and one comes back unverified.** Coherence:
enforced by rule 7 after **eight** bugs of the shape *prose written beside a number that
contradicted it*, six of them in the last ten entries. Accuracy: 64 gate tests, mutation-checked,
three Lean proofs re-observed. **Holistic: the entries had never been checked against each other
at scale** — precisely the exposure H3 identifies, in a 3,000-line ledger written incrementally.

**Partly closed rather than only recorded.** Two tests added, both mutation-checked:

```
test_load_bearing_numbers_are_stated_consistently   6 canonical values; a planted
                                                    variant produces 7 detections
test_every_entry_has_a_tier_marker                  a planted untiered entry fails
```

**Gate 64 → 66.** This is a **floor, not a proof**: it checks that the load-bearing *numbers* are
stated consistently wherever they appear. It cannot check that the *arguments* agree — that needs
reading the corpus as a whole, and remains open.

*The transferable statement.* Subjective correctness and factual accuracy are orthogonal, and
holistic consistency is a third axis neither implies. A result can be true in its frame,
inaccurate against measurement, and still more valuable than a fit that matches to eleven digits —
because only one of the two can be inspected, located, and corrected.

---

### 2026-09-01 — The Hoyle resonance as a control on coherence vs accuracy — **SAME ARGUMENT FORM, 4.6 BITS vs 0** · T1 machine / T3 measured

**Why this is a control and not an analogy.** H4 established that *"it matches the measured
value"* can carry zero information when a parameter was free enough to be tuned. The Hoyle state
is the sharpest available counter-case, because **Hoyle used the same argument form**: reason
backwards from a known outcome to a required value. Carbon exists → triple-alpha must be resonant
→ a `0⁺` state must sit near 7.7 MeV. Structurally identical to *α is 137.036 → therefore
`a/R = 8e^{−136.036}`*. One carries information; one does not.

Instrument: `code/constraint_projection/hoyle_resonance.py`.
Artifact: `docs/hoyle_resonance.json`.

**N1 — the energetics, computed from AME2020 masses and anchored to published values** (rule 2 —
do not check our arithmetic against our own arithmetic):

| quantity | computed | published | diff |
|---|---|---|---|
| `Q(Be-8 → 2α)` | 91.8395 keV | 91.8400 keV | 0.0005 |
| 3α threshold | 7.2747 MeV | 7.2747 MeV | 0.0000 |
| resonance energy | 379.4524 keV | 379.5 keV | 0.048 |

**Be-8 is unbound by ~92 keV** — it exists only as a fleeting resonance, decaying in ~10⁻¹⁶ s. So
carbon forms only if a third alpha arrives while Be-8 is still there **and** lands on a state that
is nearly energy-matched. The Hoyle state sits **379 keV** above the 3α threshold.

**N2 — how narrow the prediction was.** At helium-burning temperatures (`T ~ 1.5×10⁸ K`,
`kT ~ 13 keV`), a resonance is useful only within roughly 0–0.8 MeV of threshold: below it the
entrance channel is closed, above it the Boltzmann factor kills the rate. Against a prior range of
~0–20 MeV for a `0⁺` excitation in C-12, that is a **0.8 MeV window in a 20 MeV space**, i.e.
absolute excitation **7.27–8.07 MeV**. Measured: **7.6542 MeV** — inside.

**N3 — and that is the whole difference.**

```
HOYLE 1953    window/prior = 0.8/20 = 0.040   ->  -log2(0.040) = 4.64 bits   CONFIRMED
CPF a/R       14 of 14 decoy forms hit        ->  -log2(1.00)  = 0.00 bits
```

Confirmed by Dunbar/Wenzel/Whaling (1953), then Cook/Fowler/Lauritsen/Lauritsen (1957) for the
`0⁺` assignment and the alpha-decay branch.

**N4 — the discriminator, answerable in both directions.** Hoyle's inference **could have failed
three separate ways**: no `0⁺` state in the window; a state there with wrong spin-parity (the
entrance channel is three spin-0 alphas, so only `0⁺` couples); or a state that does not
alpha-decay back. Each was a distinct way to lose, and Cook et al. specifically tested the
assignments that could have killed it.

`a/R` **cannot fail, structurally rather than through carelessness**: it is *defined* as
`8 exp(−136.035999171)`, and that exponent is CODATA `α⁻¹ − 1`. No measurement could contradict
it, because the measurement is its input.

> **A prediction that cannot fail is not a weak prediction. It is not a prediction — it is a
> restatement of its own input in another notation.**

**N5 — and the scope, because the Hoyle case is routinely over-read.**

*Licensed:* reasoning backwards from an observed outcome is legitimate and can be highly
informative. **The argument form is not what disqualifies the CPF construction** — Hoyle used the
same form. What matters is whether the inference narrows the space and exposes itself to a
measurement that could come out otherwise.

*Not licensed:* that anthropic reasoning is generally predictive — this is **one** success, and
its force comes from the narrowness in N2, not from the anthropic framing. That Hoyle's own
reasoning was anthropic in the modern sense — **Kragh (2010, "An Anthropic Myth") argues the
anthropic telling is largely retrospective**, and this entry does not adjudicate that
historiography; the bits come from the window either way. And that a confirmed prediction
validates the framework it came from — Hoyle's success bears on the triple-alpha mechanism, not
on unrelated claims by the same author.

**The transferable statement:** the value of a prediction is **the fraction of the space it
excludes** — not the elegance of its derivation, and not the number of digits it matches.

*In-flight correction.* The first draft used a rounded He-4 mass (4.002602 u) and produced
`Q(Be-8) = 94 keV` against a published 91.84 and a threshold of 7.2712 against 7.2747. Replaced
with AME2020 values and an explicit published-value comparison, so the arithmetic is checked
against someone else's numbers rather than its own.
