> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Elimination Ledger

**Append-only.** Strip-mine discipline: rank targets by expected-space-collapsed
per unit cost; weight toward kills aimed at our **own** load-bearing claims. A
landed kill credits the survivors by elimination — no proof required. Don't prove
the gold is there; remove everything that isn't.

- Seed convention: `20260423`
- Tiers: **T1** machine-verified / **T2** proven-or-by-inspection / **T3** numerical / **T4** falsified
- Status tags: `QUEUED` / `IN-PROGRESS` / `KILLED` / `SURVIVED` / `SPLIT` / `BLOCKED`

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

**T1-TARGET — Framework constants: invariant or refraction?** `IN-PROGRESS → see KILLS LOGGED 2026-06-06`
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
this environment (`computatioanal_work_ACS` contains the TENT classifier notes, not
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

Code: `/tmp/q3_floor.py` (zeta zeros, N=100000).

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

Code: `/tmp/q6_offdiag.py` (explicit-formula dual periodogram, first 3000 zeros, Hann taper).

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

Code: `/tmp/q5_hp.py` (zeta zeros 10000–40000, RvM-smooth unfolding).

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

Testbed: `q4_cfunction_testbed.py` (TFIM = free Majorana, M=14 exact diagonalization).

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

Code: `/tmp/q4_largeL.py`; folded into `q4_cfunction_testbed.py` (`bdg_S`, `c_function_large`).

Free-fermion BdG method, **validation gate PASS**: reproduces exact diagonalization to
1e-13–1e-15 on the same open chain (M=12, h=1.0/1.3, L=1/3/6) — instrument trusted at
scale. At M=400: critical fit c = 0.4884 (Ising 1/2, ~2%); massive entropic c-function
**monotone 0.5→0** with onset at ξ~1/|h−1| (h=1.02→0.001 by L=156; h=1.3→~0), for every
mass. The "c" side is now production-grade. Kill remains BLOCKED only on the FF06Σ ΔI
definition; once supplied, ΔI is computed from the same BdG Gaussian state and checked
against the four pre-registered conditions at large L. Structural damage (universal
identity dead unless ΔI unbounded & canonically normalized) stands independent of this.

### 2026-06-06 — Target Q7: neutrino seesaw / X-ray tension — **RESOLVED (survives), decoupling caveat** · T3 estimate / T2 structural

Code: `/tmp/q7_neutrino.py`. Inputs: framework's stated naive sin²(2θ)=4×10⁻⁶ and
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

### Q2 BRA speed — **KILLED (T1, measured)**, with a precision confound noted
Matched op identified at last: Gabor wave-packet render/energy (`bra_render`/`bra_energy`),
replacing TF `exp(-dt²/2w²)·exp(2πi f dt)` (f32). Measured ns/op (release rlib):
BRA-f64 is **1.37–1.82× SLOWER** than TF-f32 across N=16..1024. The withdrawn "489×
faster" is obliterated — not faster, slower. Speed-superiority KILLED (T1).
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

Code: `/tmp/q4_monotonicity.py` (validated BdG instrument, M=400).

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

Code: `q3_scaling_test.py` (mpmath Dirichlet L zeros + ζ zeros; genuine degree-2 L-function
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

## KILLS LOGGED (2026-07-17)

### EM-as-torsion-annihilator ("electromagnetism is the fundamental degradation") — **KILLED, both forms** · T1 machine / T4 falsified

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

### Condensate-as-collapse ("the slag of the furnace") — **SURVIVED, all four forms** · T1 machine / exact

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
