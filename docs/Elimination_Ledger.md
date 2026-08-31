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

`g = 2` is right to three decimal places and wrong at the fourth.

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

**The hypothesis, and why it deserved a test.** The decoy test above found that taking
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

### 2026-08-30 — Can a RELATIVE boundary condition fix alpha? — **the instinct was right twice and still does not save it** · T1 machine / T2 structural

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

**This is a real improvement and deserved the test.** 2.96x beats the 72.6x of `tau = i/2`
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

**Verdict.** The instinct was right twice — the condition should be relative, and the
framework does contain one — and the framework is worse off for it, not better. Logged as
a route that genuinely improved the prediction (72.6x → 2.96x, and parameter-free) and was
killed anyway, by a test it could have passed: had the predicted drift come in below
1e-17/yr, the relational reading would have survived as a live option with only a
normalisation gap to explain.

Instrument: `code/constraint_projection/alpha_relational_boundary.py`.
Artifact: `docs/alpha_relational_boundary.json`.
