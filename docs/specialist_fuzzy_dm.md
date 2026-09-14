# Specialist report — CPF §6's ultralight scalar against the observational bounds

STATUS: complete — sections 1-6 written; instrument runs at exit 0; test gate NOT run, nothing committed

Wave-2 specialist. Mission: take the mass that CPF §6's quantum-pressure rotation-curve
mechanism *requires* and test it against published ultralight/fuzzy dark matter bounds.
The audit's existing result (`Constraint_Projection_Framework_Audit.tex`, §"(iii) The scale.")
is internal/structural (T2). This report attempts the escalation to T3 (measured against
external data) or T4 (falsified).

Instrument: `code/constraint_projection/fuzzy_dm_bounds.py`

## Tier conventions used here
- T0 machine-CHECKED, T1 machine (an instrument ran and printed it), T2 proved,
  T3 measured (against external data), T4 falsified. Tiers never promote.
- **Published bounds quoted below are CITED literature values (T3 data from others), not
  measurements made by me.** Every such number is tagged `[CITED]` with its source.
- Numbers computed by my instrument in this session are tagged `[T1 this run]`.

## Sections
1. Re-derivation of the mass §6 requires — **done**
2. Lyman-alpha forest bounds — **done**
3. Dwarf spheroidal kinematics — **done**
4. Black hole superradiance — **done**
5. Honest synthesis — **done**
6. What I did not do / assumptions not lifted — **done**

---

## 1. Re-derivation of the mass §6 requires

Instrument: `code/constraint_projection/fuzzy_dm_bounds.py`, Section 1. Run this session.
Inputs from the audit's own fiducial: `v = 200 km/s`, `L = 1 kpc`. Constants: CODATA 2018,
IAU-2015 parsec. Nothing inherited from the audit; the audit's numbers are regenerated as a
cross-check, not copied.

### 1.1 The four set-ups

| route | relation | m (kg) | m (eV/c²) |
|---|---|---|---|
| (a) standard de Broglie | `λ = h/(mv) = L` | 1.0737e-58 | **6.0229e-23** |
| (b) reduced de Broglie | `ƛ = ħ/(mv) = L` | 1.7088e-59 | **9.5858e-24** |
| (c) soliton core, natural units | `r_c = (mv)⁻¹`, i.e. `ħ/(mv)` | 1.7088e-59 | 9.5858e-24 |
| (d) Schive+2014 core–halo, inverted | `r_c = 1.6 kpc (m/1e-22)⁻¹(M_h/1e9 M_⊙)^(-1/3)` | — | 1.600e-23 (MW-like, r_c=1 kpc) |

All `[T1 this run]` except the *functional form and coefficient* of (d), which is `[CITED]`
(Schive, Chiueh & Broadhurst 2014); the inversion arithmetic is mine.

### 1.2 Finding 1A — the mission's "soliton-core relation" is not an independent check

`r_c ~ (m v)⁻¹` in ħ=c=1 units restores to `r_c = ħ/(m v)`, which is **the same equation** as
route (b). The instrument asserts this (`|m_sol − m_red|/m_red < 1e-12`, passes). So the brief's
items "λ_dB = h/(mv)" and "the soliton-core relation r_c ~ (mv)⁻¹" are one constraint, not two.
The genuinely independent soliton route is (d), the empirical core–halo relation, and it is
reported separately above.

### 1.3 Finding 1B — the audit's `9.6e-24 eV` is the *reduced* de Broglie wavelength

`m_standard / m_reduced = 6.283185…`, asserted equal to 2π to 1e-9. The audit note
(`Constraint_Projection_Framework_Audit.tex`, §"(iii) The scale.") writes "the de Broglie
wavelength" and gives `1.7e-59 kg = 9.6e-24 eV`. That number is reproduced here by the
**reduced** convention `ƛ = ħ/(mv)` (1.7088e-59 kg, 9.5858e-24 eV), not by the standard
convention `λ = h/(mv)` (1.0737e-58 kg, 6.0229e-23 eV).

This is a naming convention, not an arithmetic slip, and the audit is internally consistent in
it — two further checks confirm the same convention is used throughout that paragraph:

- The audit's electron figure, `λ_dB = 5.8e-10 m`: reduced gives 5.788e-10 m ✓; standard gives
  3.637e-09 m ✗.
- The audit's "29 decades": `log10(kpc / 5.788e-10 m) = 28.73` ✓.

So the audit's paragraph is arithmetically sound under its own (unstated) convention. The
correction available is one of labelling: under the standard textbook definition of the
de Broglie wavelength the required mass is **6.0e-23 eV**, a factor 2π heavier than stated.
Recorded because the two numbers straddle the literature's quoted fuzzy-DM window
(1e-23 – 1e-22 eV) differently, and because §6's required mass is about to be compared against
published bounds where a factor 2π is not negligible.

**Both values are carried forward.** The bracket taken to data below is

    m_required ∈ [9.6e-24, 6.0e-23] eV/c²      (convention bracket, v=200 km/s, L=1 kpc)

and the manuscript's own stated `m ~ 1e-23 eV` (CPF L88) sits at the bottom of it.

### 1.4 Finding 1C — sensitivity is mild; this is a robust, not a fragile, requirement

`m = ħ/(vL)` is exactly inverse-linear in both inputs, so `dlog10(m)/dlog10(L) = −1` and
likewise for v. A factor 2 in L moves the mass **0.30 decades**, not two. Over the full grid
`L ∈ [0.5, 10] kpc × v ∈ [100, 300] km/s` the mass spans

    6.391e-25 … 3.834e-23 eV      (1.78 decades)  [T1 this run]

The instrument asserts this span is under 2 decades (passes). Consequence for the mission: §6's
requirement is **not** the kind of claim that can be rescued by a factor-2 argument about what
"galactic scale" means. To lift the required mass by a decade you must shrink L by a decade, to
100 pc — below the scale on which flat rotation curves are the phenomenon being explained.


---

## 2. Lyman-alpha forest bounds

Three primary sources were fetched and read this session. Every number below is `[CITED]`;
none of it was measured by me. Each is quoted with the confidence level the source states and
the caveat the source itself states, not a caveat I supplied.

### 2.1 Finding 2A — the contested Rogers & Peiris number, settled against the source

The brief I was given asserted Rogers & Peiris give roughly `m > 2e-21 eV`. My predecessor
reported `2e-20 eV`. I fetched the paper. **The predecessor's number is the one the source
states.** Verbatim, from the abstract of arXiv:2007.12705v3 (= Phys. Rev. Lett. 126, 071302):

> "We present a new bound on the ultra-light axion (ULA) dark matter mass m_a, using the
> Lyman-alpha forest to look for suppressed cosmic structure growth: a 95% lower limit
> m_a > 2 x 10^-20 eV."

and from its Results section, the same limit in log form:

> "log(m_a[eV]) > -19.64, which equates to m_a > 2 x 10^-20 eV."

`10^-19.64 = 2.291e-20 eV`, consistent with the rounded `2e-20 eV`. So:

    Rogers & Peiris 2021:  m_a > 2e-20 eV   at 95% credibility   [CITED]

**The brief's `2e-21 eV` was low by a factor of ten, and the error has a traceable
provenance rather than being a typo.** `2e-21 eV` is a real number in that paper — it is the
*previous* Lyman-alpha bound, the one Rogers & Peiris supersede. Their Fig. 2 caption reads:

> "the equivalent previous bound (see main text) from the Lyman-alpha forest excludes
> m_a < 2 x 10^-21 eV [29]. In this work, we exclude m_a < 2 x 10^-20 eV (at 95% credibility)."

Ref. [29] there is Irsic et al. 2017. The brief therefore carried Irsic+ 2017's limit under
Rogers & Peiris's name. Logged as its own finding because the direction matters: the weaker
number is the one that leaves more room for CPF §6's required mass, and the brief was written
to set up a conclusion that the weaker number makes less severe. Checking it moved the bound
*away* from the brief's framing, not toward it.

### 2.2 The three bounds, as stated by their sources

All limits are lower limits on m_a for ULAs constituting **all** of the dark matter.

| source | limit (eV) | C.L. | what it is |
|---|---|---|---|
| Rogers & Peiris 2021 (2007.12705, PRL 126 071302) | **2e-20** | 95% credible | Boera+2019 flux power, z=4.2/4.6/5.0, k_f ≤ 0.2 s/km, GP emulator |
| Irsic+ 2017 (1703.04683, PRL 119 031302) | **2.0e-21** | 2σ (95%) | XQ-100 + HIRES/MIKE combined, T_0 free per z-bin — the paper's own "most conservative" |
| Irsic+ 2017, reference thermal history | 3.75e-21 | 2σ | same data, power-law T_0(z) |
| Irsic+ 2017, XQ-100 alone + Planck priors | 2.7e-22 | 2σ | the weakest single entry in this whole table |
| Armengaud+ 2017 (1703.09126, MNRAS 471 4606) | **2.3e-21** | 95% CL | SDSS/BOSS DR9 alone, via the m_X–m_a scaling |
| Armengaud+ 2017, + XQ-100 + HIRES/MIKE | 2.9e-21 | 95% CL | quoted as their extended exclusion range |
| Armengaud+ 2017, SDSS alone + Planck priors | 1.3e-21 | 95% CL | their own stated loosening under CMB priors |

Irsic+ 2017's full 2σ grid, as tabulated in their Table I (units 1e-22 eV): reference 4.5 /
16.4 / 37.5, covariance x1.3 3.9 / 16.3 / 34.9, Planck priors 2.7 / 16.5 / 32.2, T_0 in
z-bins 7.1 / 14.3 / 20.0, for XQ-100 / HIRES-MIKE / combined respectively. One internal
inconsistency in that source is noted for the record and not resolved here: their running text
gives XQ-100 reference as `4.6e-22 eV` where their Table I gives `4.5e-22`. It does not affect
anything below.

### 2.3 The caveats, as the sources state them

Not paraphrased into something stronger or weaker than the source.

**Rogers & Peiris 2021.**
- Quantum pressure is modelled **only through modified initial conditions at z=99**: "we model
  the effect of ULA quantum pressure only by modified initial conditions, as this is sufficient
  for the current sensitivity of data."
- Mixed dark matter is not covered: "These bounds (including our own) can be weakened when
  considering the case where ULAs do not make up all the dark matter, but we defer analysis of
  these mixed dark matter models to future work."
- They decline to quote beyond 3σ: "for robustness, we do not report bounds at > 99.7%
  credibility, since the tails of the distribution estimated by MCMC sampling can be unreliable."
- The bound is strongly driven by the smallest scales. Their footnote 4: restricting to
  `k_max = 0.126 s/km` gives `log(m_a) > -20.24` (5.75e-21 eV); restricting to `k_max = 0.08
  s/km` — the reach of the previous generation of analyses — gives `log(m_a) > -20.64`
  (2.29e-21 eV). **A decade of the bound's strength lives in the smallest-scale bins.**
- IGM priors are informative by design: a Gaussian prior on T_0 with σ = 3000 K is imposed "in
  order to disfavor very cold IGMs which are hard to motivate physically", and τ_0 carries a
  Gaussian prior of mean 1, σ = 0.05.
- **Prior range**: "Our prior is uniform in the logarithm of the ULA mass:
  log(m_a[eV]) ∈ [-22, -19]." See §2.4.

**Irsic+ 2017.**
- Their headline `20e-22 eV` combined limit is the one obtained "with conservative assumptions
  for the thermal history of the IGM that allow for jumps in the temperature of up to 5000 K",
  and they say of that case: "We regard this result as the most conservative, since sudden jumps
  of temperature are not physically plausible in this redshift range." The number roughly
  doubles under a smooth power-law thermal history.
- No quantum-pressure term in the hydrodynamics; they justify this by the FDM Jeans scale at
  `m = 1e-22 eV, z = 5.4` being `64.7 h/Mpc`, well beyond their `k_max = 12.7 h/Mpc`.
- They show the customary WDM→FDM mapping via `k_1/2` "is not a good approximation" at the
  higher masses, and that `k_0.75` maps better.

**Armengaud+ 2017.**
- Same structural approximation, stated plainly: "This approach is an approximation which
  neglects the 'quantum force' present in the Madelung equation."
- And, critically for this report, the range over which they are willing to defend it: "we find
  indications that for m_a ≲ 1e-22 eV the quantum term may impact the non-linear predictions for
  P(k), and should therefore be included in the simulations in order to provide more reliable
  predictions."
- Their `n_s = 0.94` from Lyman-alpha alone is "in slight tension with the CMB-derived value
  n_s = 0.97"; imposing Planck priors loosens the bound to 1.3e-21 eV.
- Patchy/inhomogeneous reionization is not modelled.

### 2.4 Finding 2B — the CPF bracket lies *below* the mass range these analyses simulate

This is the caveat that actually bites, and it is one the sources themselves raise rather than
one I am importing. CPF §6's required mass, from Section 1 above, is

    m_required ∈ [9.6e-24, 6.0e-23] eV/c²

Compare that with what the three analyses actually cover:

- Rogers & Peiris sample `log(m_a[eV]) ∈ [-22, -19]`, i.e. `m_a ∈ [1e-22, 1e-19] eV`. **The
  entire CPF bracket is below their prior's lower edge** — by a factor 1.7 at the top of the
  bracket and a factor 10.4 at the bottom. Their posterior never visits the CPF mass.
- Irsic+ 2017 simulate `m_FDM ∈ {1, 4, 5.7, 15.7, 30} x 1e-22 eV`. The CPF bracket is below
  their lightest simulated model.
- Armengaud+ 2017 simulate `m_a ∈ {3.4, 7.9, 18, 41} x 1e-22 eV`, and explicitly decline to
  vouch for their approximation below 1e-22 eV.

So the exclusion of the CPF mass by these papers is **an extrapolation of a monotone bound
below the mass range that was simulated**, not a direct measurement at that mass. The
extrapolation is in the safe direction — lighter ULAs suppress small-scale power *more*, so a
95% lower limit at 2e-20 eV entails exclusion of everything lighter, and every one of these
analyses reports the likelihood falling away monotonically toward small m_a — but it is an
entailment, not an observation, and it is recorded here as such under Rule 10. What the sources
directly measured was at masses 1.7x to 10x heavier than what CPF §6 needs.

The independent probe that *does* sit at the CPF mass is the CMB, which Rogers & Peiris cite
(their Fig. 2, from Hlozek+ 2015/2018): "ULA dark matter with masses 1e-33 eV ≤ m_a ≤ 1e-24 eV
are excluded by Planck cosmic microwave background data", and in their introduction: "Current
bounds from the early Universe exclude ULAs being more than half of the dark matter with masses
m_a ≤ 1e-23 eV." The lower half of the CPF bracket falls inside that second statement. The
upper half (up to 6.0e-23 eV) does not.

### 2.5 Finding 2C — the exclusion does not depend on which Lyman-alpha paper you pick

Against the **strongest** bound in the table (Rogers & Peiris, 2e-20 eV):

    m_required = 9.5858e-24 eV  ->  2086x below the bound  (3.32 decades)   [T1 this run]
    m_required = 6.0229e-23 eV  ->   332x below the bound  (2.52 decades)   [T1 this run]

Against the **weakest single entry anywhere in the table** — Irsic+ 2017 XQ-100 alone with
Planck priors, 2.7e-22 eV, a limit nobody quotes as a headline result:

    m_required = 9.5858e-24 eV  ->  28.2x below the bound  (1.45 decades)   [T1 this run]
    m_required = 6.0229e-23 eV  ->   4.5x below the bound  (0.65 decades)   [T1 this run]

Combining with Finding 1C (the `L × v` grid spans only 1.78 decades): even the weakest published
Lyman-alpha limit sits above the top of the CPF convention bracket, and the strongest sits
2.5–3.3 decades above it. The gap is not closable by choosing a different paper, a different
thermal-history assumption, a different de Broglie convention, or a different fiducial galactic
scale. That is the whole point of running the weakest case as well as the strongest.


---

## 3. Dwarf spheroidal kinematics

The mission brief expected this section to pull *opposite* to Lyman-alpha — dSph cores
historically prefer `m ~ 1e-22 eV` or lighter, which would leave room for CPF §6. That
expectation is half right and half out of date, and the split is the finding.

### 3.1 Finding 3A — "dwarf kinematics" is two incompatible constraints, not one

Reading the primary sources, dwarf-galaxy stellar kinematics yields two families of limits
that point in opposite directions by roughly four decades, because they use two different
physical effects:

**(i) Soliton core size.** A cored density profile of radius `r_c` implies an *upper* limit on
`m`, since lighter bosons make bigger cores. All `[CITED]`, González-Morales, Marsh, Peñarrubia
& Ureña-López 2017 (arXiv:1609.05856, MNRAS):

| analysis | result | note |
|---|---|---|
| Schive+ 2014a, Fornax Jeans | `m_a = 8.1 (+1.6/−1.7) e-23 eV` | a *detection*, not a limit |
| joint Jeans, 8 classical dSphs (GM+17) | `m_a = 2.44 (+1.3/−0.6) e-22 eV` | GM+17 argue this is biased |
| Marsh & Pop 2015, virial estimator | `m_a < 1.1e-22 eV` (95% C.L.) | upper limit |
| **GM+17 `⟨σ²_los⟩`-fit, Fornax+Sculptor** | **`m_a < 0.4e-22 eV` (97.5% C.L.)** | their headline, claimed unbiased |
| GM+17, Fornax alone | `m_22 < 0.48` i.e. `< 4.8e-23 eV` | |
| GM+17, Sculptor alone | `m_22 < 0.79` i.e. `< 7.9e-23 eV` | |
| Calabrese & Spergel 2016, UFD half-light masses | `m_a ~ 3.7 – 5.6e-22 eV` | pulls the other way |
| Lora+ 2012, Ursa Minor clump / Fornax GCs | `m_a ~ 0.3 – 1e-22 eV` | |

**(ii) Wave-interference dynamical heating.** Density granules of coherence length `ħ/(mv)`
heat stellar orbits; observed cold, compact ultra-faint dwarfs therefore imply a *lower* limit,
and lighter bosons heat harder. `[CITED]` Dalal & Kravtsov 2022 (arXiv:2203.05750, PRD):

    m_FDM > 3e-19 eV at 99% confidence  (Segue 1 + Segue 2, marginalized over halo v_1/2)

with their Table I giving, in units of 1e-19 eV and for three prior choices on `v_1/2`:
1σ 5.87 / 6.52 / 6.16, 2σ 4.15 / 4.54 / 4.57, 3σ 2.86 / 3.22 / 3.35.

These two families are not reconcilable by averaging and this report does not attempt it.
`4e-23 eV` (an upper limit) and `3e-19 eV` (a lower limit) with no overlap is a contradiction
somewhere in the modelling, and the sources say as much about each other.

### 3.2 Finding 3B — the CPF bracket straddles the dSph-core upper limit

This is the one place in the whole report where part of CPF §6's required mass **survives**,
and it survives only under one of the two de Broglie conventions from Section 1:

    GM+17 upper limit:  m_a < 4.0e-23 eV (97.5% C.L.)  [CITED]

    m_required = 9.5858e-24 eV  (reduced conv.)   ->  0.240 x the limit  -> ALLOWED  [T1 this run]
    m_required = 6.0229e-23 eV  (standard conv.)  ->  1.506 x the limit  -> EXCLUDED [T1 this run]

So the factor 2π of Finding 1B is decisive here and nowhere else: the audit's own stated
`9.6e-24 eV` sits comfortably inside the mass range that Fornax and Sculptor's cores prefer,
while the standard-convention `6.0e-23 eV` sits above it by a factor 1.5. The manuscript's own
`m ~ 1e-23 eV` is also inside. A specialist who fixed the convention "correction" of Finding 1B
without carrying both values forward would have lost this.

The honest reading, though, has to include what GM+17 say about their own bound in the same
paper. They state it is in conflict with structure counts:

> "m_22 < 0.4 cannot even give the eight classical dSphs, never mind passing a more realistic
> bound such as n_sub ≳ 66"

and they describe the resulting position explicitly as a Catch-22:

> "ULAs, like WDM, may suffer from a Catch 22 in that 'if you want large cores, you don't get
> enough dwarfs; if you want enough dwarfs, you don't get big enough cores'."

and they name their own bound as inconsistent with the cosmological floor:

> "The constraint from this method, m_a < 0.4 x 10^-22 eV, produces too few subhalos and is
> inconsistent with a conservative bound of m_a > 1 x 10^-22 eV from cosmology."

So the region in which CPF §6's reduced-convention mass survives is a region the source that
defines it says cannot be the dark matter. The survival is real and is recorded as real; it is
survival against one observable, inside a window its own authors report as closed by others.

### 3.3 Finding 3C — the CPF bracket versus the heating bound

Against the other family, there is no survival and no convention-dependence:

    Dalal & Kravtsov 2022:  m_FDM > 3e-19 eV at 99% confidence  [CITED]

    m_required = 9.5858e-24 eV  ->  3.13e4 x below the bound  (4.50 decades)  [T1 this run]
    m_required = 6.0229e-23 eV  ->  4.98e3 x below the bound  (3.70 decades)  [T1 this run]

The caveats D&K state about their own result all run in the conservative direction — they
list them as such: soliton heating neglected ("inclusion of soliton effects ... significantly
worsens the fit"), initial velocity anisotropy neglected, binary contamination inflating the
measured dispersion, and a prior `p ∝ m_FDM^-2` deliberately chosen to favour light masses.
The caveats that could weaken it are also stated by them: whether Segue 2 is a galaxy or a star
cluster at all, and whether tidal stripping down to the soliton could suppress the interference
that drives the heating (they argue not, from Gaia pericentre positions and tidal radii). They
also record an outright disagreement with another UFD analysis (their Ref. [11], which claims
soliton detections in 18 UFDs) and do not resolve it.

Their own fallback ladder matters for robustness, because it does not depend on Segue 1 or
Segue 2 at all: DDO 168 gives `m ≳ 1e-21 eV`, Carina `m ≳ 5e-21 eV`, Boötes I `m > 1e-20 eV`,
Leo IV `m > 3e-20 eV`, and they conclude "even if we removed the constraints from Segue 1 and 2,
FDM with m < 1e-20 eV would remain excluded by these other UFDs." The whole CPF bracket is below
`1e-20 eV`.

### 3.4 Finding 3D — the FDM literature uses *both* conventions, and says which is which

An unplanned external check on Finding 1B, found while reading Dalal & Kravtsov. Their
introduction states, of the de Broglie wavelength:

> "the de Broglie wavelength of DM particles, λ = h/mv, can be large enough to produce
> observable wave effects on galactic scales. For example, a mass of m = 10^-22 eV and a DM
> velocity dispersion of v = 200 km/s would give λ ∼ 600 pc."

Reproducing that from CODATA constants this run: `h/(mv)` at `m = 1e-22 eV`, `v = 200 km/s`
gives **602.3 pc** `[T1 this run]` — the quoted figure to 0.4%. The reduced form gives 95.9 pc,
which is not what they quote. So D&K use the **standard** convention for "the de Broglie
wavelength".

But two paragraphs later, for the physically relevant granule size, they write:

> "fluctuations in the local density and gravitational potential throughout FDM halos with
> contrast of order unity, δρ ∼ ρ, and coherence lengths r ≈ λ/2π = ℏ/mv"

and use `r = ℏ/(mσ_dm)` throughout their derivation. So the same primary source uses `h/(mv)`
for the named wavelength and `ħ/(mv)` for the length that actually sets the physics.

This confirms Finding 1B from outside the corpus and sharpens it: the audit's `9.6e-24 eV` is
not a slip, and it is not even an idiosyncratic convention — it is the **coherence-length**
convention that the FDM literature uses when it computes the scale on which wave effects act.
The correction available to the audit is therefore smaller than Finding 1B stated: not "the
required mass is a factor 2π heavier", but "the length being set to 1 kpc should be named the
coherence length `ħ/(mv)`, not the de Broglie wavelength `h/(mv)`". Both numbers still travel
forward as a bracket, because CPF §6's own text does not say which length it means.


---

## 4. Black hole superradiance

Superradiance is the one probe in this report that returns a **null** result on CPF §6: it
does not constrain the required mass, and it cannot be made to, because no black hole heavy
enough exists. Recorded in full because a measured dead end is a deliverable.

### 4.1 Which black hole population bounds which boson mass

Superradiance needs the boson's Compton wavelength comparable to the BH gravitational radius,
i.e. the dimensionless coupling `α = G M_BH μ / (ħ c³)` of order a few tenths. Since `α ∝ M_BH μ`,
**heavier black holes probe lighter bosons**, and the probed boson mass runs inversely with the
BH mass. From the constants (`[T1 this run]`):

    ħ c³ / (G M_sun) = 1.33600e-10 eV        so   μ(α=1) = 1.336e-10 eV x (M_sun / M_BH)

Stott & Marsh 2018 (arXiv:1805.02016) state the observational span and its consequence
directly `[CITED]`:

> "The current lower and upper bounds on BH masses from X-ray spectroscopy and emission data
> covers the approximate region 5 M_⊙ ≲ M_BH ≲ 5 x 10^8 M_⊙, which defines the relevant axion
> mass window as, 10^-20 eV ≲ μ_ax ≲ 10^-11 eV."

and their two exclusion bands, both at 95% C.L. and both for a **single** field with negligible
self-interaction (`f_a ≳ 1e14 GeV`):

| BH population | excluded boson mass band | C.L. |
|---|---|---|
| stellar-mass BHs (X-ray binaries, BBH) | `7e-14 eV < μ < 2e-11 eV` | 95% |
| supermassive BHs (AGN X-ray reflection) | `7e-20 eV < μ < 1e-16 eV` | 95% |

They also say in their own words what this means for fuzzy dark matter:

> "'Fuzzy dark matter (DM)' with μ_ax ≈ 10^-22 eV ... is too light to make predictions about the
> spin distribution of SMBHs with M_BH < 10^9 M_⊙."

The single heaviest-BH extension of this is Davoudiasl & Denton 2019 (arXiv:1904.09242), using
EHT's M87* (`M_BH = (6.5 ± 0.7)e9 M_⊙`, fiducial spin `a* = 0.9 ± 0.1` from Tamburini+ 2019,
`τ_BH = 1e9 yr`) `[CITED]`:

    scalar:  2.9e-21 eV < μ_S < 4.6e-21 eV     (1σ, M87*)
    vector:  8.5e-22 eV < μ_V < 4.6e-21 eV     (1σ, M87*)

CPF §6's field is a **scalar** (`ψ = R exp(iS/ħ)`, CPF L205–219), so the scalar row is the one
that applies; the vector band reaches roughly 3.4x lighter and is not available to this model.

### 4.2 Finding 4A — the bracket falls *out* of every superradiance band, on the light side

    m_required = 9.5858e-24 eV  ->  302x below M87*'s scalar band (2.48 decades)  [T1 this run]
    m_required = 6.0229e-23 eV  ->   48x below M87*'s scalar band (1.68 decades)  [T1 this run]

and against the broader SMBH band of Stott & Marsh, 3.86 and 3.07 decades below respectively.
No superradiance measurement excludes any part of the CPF bracket. **Superradiance returns no
verdict on CPF §6, in either direction.**

### 4.3 Finding 4B — what it would take, and why it is not available

Calibrating the efficient-superradiance window empirically from M87* itself — Davoudiasl &
Denton's own scalar band edges correspond to `α = 0.141` and `α = 0.224` at `M_BH = 6.5e9 M_⊙`
(`[T1 this run]`, their numbers as inputs) — the BH mass needed to place the CPF bracket inside
an exclusion band is

| target boson mass | required M_BH (α = 0.141 … 0.224) |
|---|---|
| 6.0229e-23 eV (standard conv.) | 3.13e11 … 4.97e11 M_⊙ |
| 1.0e-23 eV (CPF's stated value) | 1.88e12 … 2.99e12 M_⊙ |
| 9.5858e-24 eV (reduced conv.) | 1.97e12 … 3.12e12 M_⊙ |

The heaviest black holes with any mass estimate at all are of order `4–7e10 M_⊙`. So probing
CPF §6's mass by superradiance needs a black hole roughly **5 to 50 times heavier than the
heaviest one known**, with a measured spin. Davoudiasl & Denton say the same thing from the
other side:

> "The largest SMBHs are more than an order of magnitude more massive than M87*, but are
> significantly farther away making them difficult targets for the EHT or other probes that
> could provide good spin measurements. Still, this means that it is, in principle, possible to
> probe the entire fuzzy DM parameter [space] using this technique"

— but "the entire fuzzy DM parameter space" there means the `~1e-22 – 1e-21 eV` canonical
window, which is already one to two decades above the CPF bracket. Even the aspirational version
of this probe does not reach `1e-23 eV`.

### 4.4 Caveats the superradiance sources state about themselves

- Both bands are quoted for **zero self-coupling**; Stott & Marsh: "These limits apply strictly
  in the regime of zero self-coupling. Assuming a self-coupling derived from a standard instanton
  potential, they apply for axions with decay constants f_a ≳ 10^14 GeV." A scalar with stronger
  self-interaction shuts superradiance off entirely. CPF §6 does not specify a self-coupling, so
  this caveat cannot be lifted here either way.
- Spin systematics dominate. Stott & Marsh: "the main sources of error for catalogued BHs comes
  from the systematic errors when modelling the emission of the accreting disc", and "the
  potentially large systematic errors in BH spin measurements could act as a current restriction
  to this approach for spin-0 fields" — spin-0 being exactly CPF's case.
- The M87* result is spin-driven: Davoudiasl & Denton's Fig. 2 shows the scalar constraint exists
  only for `|a*| > 0.55`, and EHT itself supports only `|a*| ≳ 0.5` with "no analysis made of any
  spins 0 < |a*| < 0.5". The fiducial `a* = 0.9 ± 0.1` comes from a separate analysis, not EHT.
- The SMBH exclusion band is sparse-data driven: "The sparseness of the data leads to oscillatory
  features in the exclusion probability ... with the exclusions being driven by individual BHs."

None of these caveats change Finding 4A, because the gap is 1.7–3.9 decades and every caveat
moves the band by less than that. The null is robust.


---

## 5. Honest synthesis

Written from the instrument's printed output (`python3 code/constraint_projection/fuzzy_dm_bounds.py`,
exit 0, run this session), not alongside it. All 18 limit rows and their verdicts are in
Sections 2 and 3 of that output.

### 5.1 Scope check — does CPF §6 claim the scalar *is* the dark matter?

Yes, and this matters, because every bound in Section 2 is quoted for ULAs constituting **all**
of the dark matter. `Constraint_Projection_Framework.tex` §6 is titled "Dark Matter as Kinetic
Potential" and writes `ρ_DM = (ħ²/2m)|∇ψ|²`, `T_00 = ρ_vis c² + ρ_DM c²` — the field's kinetic
potential is the whole dark-matter term, not a subcomponent. So the "100% of the DM" assumption
the bounds carry is matched by the manuscript's own framing, and the mixed-dark-matter escape
that Rogers & Peiris explicitly defer is not available to §6 as written.

A provenance correction to my own Section 1 while I am here: §6's text names **no mass at all**.
The `m ~ 1e-23 eV` figure is at `Constraint_Projection_Framework.tex` L88, which is inside the
audit-summary `tcolorbox` embedded in that file, and at `Constraint_Projection_Framework_Audit.tex`
L108; the audit's derivation is at Audit L568. Section 1 of this report cites it as "the
manuscript's own stated m ~ 1e-23 eV (CPF L88)" — the file and line are right, but it is the
audit speaking inside the manuscript file, not §6. §6's required mass is **entirely inferred**
from its mechanism, first by the audit and independently here. There is no manuscript-stated
number for a bound to contradict.

### 5.2 The verdict, by probe family

`[T1 this run]` for every verdict; `[CITED]` for every bound feeding it.

| probe family | rows | reduced 9.59e-24 eV | standard 6.02e-23 eV |
|---|---|---|---|
| Lyman-alpha forest | 8 | **excluded** by all 8 | **excluded** by all 8 |
| UFD wave-interference heating | 2 | **excluded** by both | **excluded** by both |
| dSph soliton core size | 4 | **allowed** by all 4 | excluded by 2 of 4 |
| BH superradiance | 4 | no verdict | no verdict |

**10 published limits exclude both ends of the bracket** (instrument asserts `n ≥ 10`, passes).
The decade gaps, reduced / standard:

    strongest Lyman-alpha (Rogers & Peiris 2e-20 eV)   3.32 / 2.52
    weakest   Lyman-alpha (Irsic XQ-100+Planck 2.7e-22) 1.45 / 0.65
    UFD heating (Dalal & Kravtsov 3e-19 eV)            4.50 / 3.70
    Segue-independent UFD fallback (1e-20 eV)          3.02 / 2.22

"No verdict" for superradiance means **unconstrained, not endorsed** — the bracket falls below
every excluded band because no black hole heavy enough exists (Section 4). It is not evidence
for §6.

### 5.3 What survives, and how much of it

The split the mission asked for, stated as a split:

**Survives:** the reduced-convention mass `9.59e-24 eV` against the dSph soliton-core upper
limits — all four of them, most tightly `m_a < 4.0e-23 eV` (97.5% C.L., González-Morales+ 2017),
which it clears by a factor 4.2. This is the audit's own number and the only place in this
report where any part of the bracket is admitted by data.

**Does not survive:** everything else. Both ends fail all eight Lyman-alpha limits including the
weakest single entry anywhere in the literature, and both fail both UFD-heating limits including
the Segue-independent fallback.

**The surviving window is one the source that defines it reports as closed.** González-Morales+
2017 state of their own `m_22 < 0.4` bound that it "produces too few subhalos and is inconsistent
with a conservative bound of m_a > 1 x 10^-22 eV from cosmology", and name the situation a
Catch-22. So the honest statement is: CPF §6's mass survives the observable that *prefers* light
bosons, and that observable is reported by its own authors to be in conflict with the ones that
do not. There is no mass in the whole bracket that satisfies both families simultaneously — the
dSph-core family caps at `4.0e-23 eV` and the Lyman-alpha family floors at `2.7e-22 eV`, leaving
a gap of 0.83 decades with nothing in it.

### 5.4 Tier recommendation

I record this as **T3 (measured against external data)** and I do not claim T4 myself. Reasoning,
stated so it can be overturned:

- The measurements are not mine. Every bound is `[CITED]`; my contribution is the re-derivation
  of the required mass from constants (T1) and the comparison arithmetic (T1). A T3 entry is the
  honest tier for "the audit's T2 structural requirement has now been placed against external
  data and does not fit."
- The reservation against T4 is **Finding 2B**, and it is real: the Lyman-alpha bounds are
  extrapolations of a monotone likelihood *below* the mass range that was simulated. Rogers &
  Peiris's prior floor is `1e-22 eV`; Irsic+'s lightest simulated model is `1e-22 eV`;
  Armengaud+ decline to vouch for their approximation below `1e-22 eV`. The top of the CPF
  bracket is `6.0e-23 eV`, a factor 1.7 below all three. The direction of the extrapolation is
  safe (lighter bosons suppress more) but it is an entailment, not an observation at that mass.
- Dalal & Kravtsov 2022 partly repairs this: their mechanism is a direct simulation of wave
  interference at the relevant masses, not a transfer-function extrapolation, and their
  `m > 3e-19 eV` leaves the bracket 3.70–4.50 decades outside. If a later specialist judges that
  sufficient, T4 for the specific claim "§6's ultralight scalar, at the mass its own mechanism
  requires, can be the dark matter" is defensible. I am leaving that judgement to the ledger with
  the measurement in hand rather than taking it on the strength of one paper.

**What does not depend on the tier call:** the audit's §6 result stands and is strengthened. The
audit's structural finding was that §6 needs `m ~ 1e-23 eV`, "an exotic ultralight scalar." This
report measures how exotic: 0.65 to 4.50 decades outside every published limit except one whose
authors report it as inconsistent with structure counts. The audit did not overstate it.

### 5.5 Correcting the brief that commissioned this run

Recorded as a finding in its own right, per the mission's instruction. The brief asserted
Rogers & Peiris give `m > 2e-21 eV`. The source states `m_a > 2 x 10^-20 eV` at 95% credibility
(Section 2.1). The brief was low by a factor of ten, and `2e-21 eV` turns out to be the
*previous* Lyman-alpha bound (Irsic+ 2017) that Rogers & Peiris supersede and cite by that value
in their own Fig. 2 caption.

The direction is the part worth logging. The weaker number leaves more room for §6's required
mass, so the error ran toward the conclusion the brief was setting up. Checking it against the
source moved the bound a decade *away* from that framing. My predecessor's `2e-20 eV` was
correct and is confirmed here from the primary source; neither number was inherited.


---

## 6. What I did not do / assumptions not lifted

Rule 10: *did you see it? did you do it?* Everything below is something I did **not** observe
this run. Listed so a later specialist knows exactly where the floor is.

### 6.1 Numbers I read from a primary source this session

Fetched and read directly, and quoted verbatim above: Rogers & Peiris 2021 (arXiv:2007.12705v3),
Irsic+ 2017 (arXiv:1703.04683v2), Armengaud+ 2017 (arXiv:1703.09126v2), González-Morales+ 2017
(arXiv:1609.05856v2), Dalal & Kravtsov 2022 (arXiv:2203.05750v2), Stott & Marsh 2018
(arXiv:1805.02016v2), Davoudiasl & Denton 2019 (arXiv:1904.09242v1). Seven papers.

### 6.2 Numbers I relayed second-hand and did NOT verify against their own source

These are in the report and in `BOUNDS`, and each is quoted *as relayed by* a paper I did read.
That is weaker provenance and is flagged as such:

- **Marsh & Pop 2015** `m_a < 1.1e-22 eV` (95%) — read only inside González-Morales+ 2017.
- **Schive+ 2014a Fornax** `m_a = 8.1(+1.6/−1.7)e-23 eV` — read only inside González-Morales+ 2017.
- **Calabrese & Spergel 2016** `m_a ~ 3.7–5.6e-22 eV` — read only inside González-Morales+ 2017.
- **Lora+ 2012** `m_a ~ 0.3–1e-22 eV` — read only inside González-Morales+ 2017 (not in `BOUNDS`).
- **Hložek+ 2015/2018 CMB** `1e-33 ≤ m_a ≤ 1e-24 eV excluded`, and "more than half of the dark
  matter with m_a ≤ 1e-23 eV" — read only inside Rogers & Peiris's Fig. 2 caption and
  introduction. **This one matters**: it is the only probe cited anywhere in this report that
  sits *at* the CPF mass rather than above it, and it would be the natural way to close the
  extrapolation gap of Finding 2B. It is not in `BOUNDS` and it is not verified. **Highest-value
  next step for whoever picks this up.**
- **Sub-halo mass function** `m_a ≲ 2.1e-21 eV excluded` — read only in Rogers & Peiris's Fig. 2
  caption. Not in `BOUNDS`.
- **Schive+ 2014 core–halo relation** (Section 1 route (d)) — inherited from my Section 1, itself
  taken from the coefficient as commonly quoted, not from Nature Physics 10, 496 directly.

### 6.3 Assumptions named but not lifted

- **`6.6e10 M_⊙` as "the heaviest known black hole"** (Section 4.3, and `LARGEST_KNOWN_SMBH_MSUN`
  in the instrument) is an order-of-magnitude figure I did not check against any catalogue this
  run. It is an assumption. The conclusion is insensitive — the required mass is 5x larger even
  for the top of the bracket, and 30x for the bottom — but the number itself is unverified.
- **`α ∈ [0.141, 0.224]` as the efficient-superradiance window** is calibrated by me from
  Davoudiasl & Denton's own M87* scalar band edges. It is a back-inference from one object, not
  a result from superradiance theory, and it inherits their mass, spin and `τ_BH` choices.
- **CPF §6's self-coupling is unspecified**, so the "zero self-coupling / `f_a ≳ 1e14 GeV`"
  condition attached to every superradiance bound can be neither satisfied nor violated here.
  Since superradiance returns no verdict anyway (Section 4.2), this does not change anything.
- **`v = 200 km/s`, `L = 1 kpc`** remain the audit's fiducials. Section 1.4 measured the
  sensitivity over `L ∈ [0.5,10] kpc × v ∈ [100,300] km/s` (1.78 decades) but did not go outside
  that grid.
- **Every bound assumes ULAs are 100% of the dark matter.** §5.1 argues CPF §6's own framing
  matches that, but I did not test a mixed-DM version of §6, and Rogers & Peiris explicitly note
  their bound weakens in that case. Nobody has run the mixed case at `1e-23 eV`.

### 6.4 Lines I did not open at all

- **CMB / Planck ULA bounds as a primary source** — see §6.2, the highest-value gap.
- **21 cm / reionization.** Stott & Marsh 2018 note claims of `m_a ≥ 5–8e-21 eV` from the global
  21 cm signal and say that if that gap closes, "fuzzy DM with no self-interactions will be
  completely excluded." Not pursued; would strengthen the exclusion, not weaken it.
- **Strong-lensing / tidal-stream substructure bounds.** Not pursued.
- **The audit's other §6 objections.** The audit also finds that `(ħ²/2m)|∇ψ|²` contains
  `½ρv²` and so double-counts visible kinetic energy in `T_00`, and that the named mechanism is
  not the Bohm quantum potential `−(ħ²/2m)∇²R/R`. This report tests **only** the mass scale.
  Those two findings stand independently and are untouched here; nothing in this report
  strengthens or weakens them.
- **Irsic+ 2017's internal discrepancy** between `4.6e-22` in their running text and `4.5e-22` in
  their Table I (Section 2.2) is recorded, not resolved. It changes nothing downstream.
- **Dalal & Kravtsov's disagreement with the rival 18-UFD soliton analysis** is recorded as they
  state it, not adjudicated.

### 6.5 What I did not run

Per the mission: **the test gate was not run and nothing was committed.** The instrument
`code/constraint_projection/fuzzy_dm_bounds.py` was run directly and exits 0.

### 6.6 A defect I found in my own instrument, and fixed

Recorded because it is the same failure mode the corpus keeps catching. The first version of the
extended instrument checked only the *verdict* (`EXCLUDED` / `allowed`) for each bound against
the bracket. I negative-tested it by corrupting `rogers_peiris_2021` from `2e-20` back to the
brief's `2e-21` — **the instrument still exited 0**, because both values exclude the bracket, so
no verdict changed. An instrument that cannot detect the exact error it was built to settle is
not a check.

Fixed by pinning magnitude, not just sign: `EXPECTED_GAP_DEC` records the decade gap for all 18
limit rows to 2 dp and asserts it to ±0.01, and a separate check reproduces Rogers & Peiris's
`2e-20 eV` from their own `log(m_a) > −19.64`. Re-run of the negative tests after the fix:

    corrupt Rogers & Peiris 2e-20 -> 2e-21      exit 1, 2 FAILs   [T1 this run]
    corrupt Irsic combined 20e-22 -> 60e-22     exit 1, 1 FAIL    [T1 this run]
    corrupt dSph upper limit 0.4e-22 -> 0.4e-24 exit 1, 2 FAILs   [T1 this run]
    corrupt HBAR = h/2pi -> h/6                 exit 1, 5 FAILs   [T1 this run]
    unmodified                                  exit 0, 0 FAILs   [T1 this run]

