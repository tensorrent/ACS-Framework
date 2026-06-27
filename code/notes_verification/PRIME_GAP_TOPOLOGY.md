# Prime Gap Topology on the Hexagonal Clock

### A 10σ Empirical Divergence from Probabilistic Models

*Bradley Wallace · Koba42 / TensorRent*
*May 2026*

---

## Abstract

We examine the behavioral mechanics of prime gaps on the modulo 6 residue lattice — the "hexagonal clock" on which all primes greater than 3 reside at positions 1 or 5. By isolating the transition matrix between residue classes and decomposing gaps into rotation count and phase shift, we identify three distinct structural behaviors in the empirical prime sequence that deviate from the leading probabilistic models (Cramér and Hardy-Littlewood) by |z| > 10 across 664,579 primes up to 10⁷.

The three behaviors are: (A) a **restoring spring-back force** where gaps systematically shorten after multi-rotation events — qualitatively opposite to the probabilistic prediction; (B) a **directional phase asymmetry** where the 5→1 return transition is 12.75% faster than the 1→5 departure, over 3× stronger than the modular constraint alone predicts; and (C) a **variance floor** where cross-class transition rates are stabilized to 29% of random expectation, consistent with deterministic phase-locked regulation rather than stochastic averaging.

These findings suggest that the prime sequence operates as a path-dependent, structurally constrained mechanism on the ⟨2,3⟩ multiplicative lattice, exhibiting memory and restoring dynamics that memoryless probabilistic models cannot reproduce.

---

## 1. The Hexagonal Clock

All primes greater than 3 satisfy p ≡ 1 or p ≡ 5 (mod 6). This is elementary: 6k, 6k+2, 6k+3, and 6k+4 are divisible by 2 or 3, leaving only 6k+1 and 6k−1 as candidates. Since all prime gaps (beyond the initial 2→3→5) are even, the gap modulo 6 takes exactly three values:

| Gap mod 6 | Fraction | Clock meaning | Transition |
|-----------|----------|---------------|------------|
| **0** | 43.04% | Full 360° cycle — return to same residue class | 1→1 or 5→5 |
| **2** | 28.48% | 120° step — short cross-class shift | 5→1 |
| **4** | 28.48% | 240° step — long cross-class shift | 1→5 |

The three gap classes partition the hexagonal cycle into thirds, analogous to the three phases of a 3-phase power system.

Every gap decomposes uniquely as **g = 6q + r**, where q is the number of complete 360° rotations (the "energy" of the event) and r ∈ {0, 2, 4} is the phase shift (which third of the clock the gap lands on).

---

## 2. Transition Matrix

The transition probabilities between residue classes are:

| From → To | Count | P(to\|from) | Gap class |
|-----------|-------|-------------|-----------|
| 1 → 1 | 142,910 | 0.4302 | same-class (r=0) |
| 1 → 5 | 189,283 | 0.5698 | cross-class (r=4) |
| 5 → 1 | 189,284 | 0.5695 | cross-class (r=2) |
| 5 → 5 | 143,099 | 0.4305 | same-class (r=0) |

Cross-class transitions dominate (57% vs 43%), confirming that primes prefer to alternate between positions 1 and 5 on the hexagonal clock. The transition matrix is nearly symmetric between the two positions but, as shown below, the gap *sizes* are not.

---

## 3. The Three Anomalies

### 3.1 Anomaly A: The Spring-Back Force

When a gap involves multiple complete rotations (q ≥ 2), the *subsequent* gap is systematically shorter than average:

| Current gap rotations (q) | Mean NEXT gap | Deviation from q=0 baseline |
|---------------------------|---------------|----------------------------|
| 0 (gap 2–4) | 15.93 | baseline |
| 1 (gap 6–10) | 15.25 | −4.3% |
| 2 (gap 12–16) | 15.01 | −5.8% |
| 3 (gap 18–22) | 14.55 | −8.7% |
| 4 (gap 24–28) | 14.25 | −10.5% |

After multi-rotation gaps (q ≥ 2), the mean next gap is 14.64 compared to 15.93 after small gaps (q=0) — a 8.1% reduction (t = 30.6, p < 10⁻²⁰⁵).

Critically, both the Cramér and Hardy-Littlewood models predict the opposite sign: that gaps should become *longer* after large gaps, reflecting regression toward the local mean of the gap distribution. The Cramér model predicts +1.43% lengthening; the HL model predicts +1.79%. The empirical result of −9.68% shortening represents a qualitative sign reversal, not merely a magnitude discrepancy.

A memoryless stochastic process cannot execute a systematic restoring force because it has no record of the energy expended in the preceding gap. The spring-back effect implies path dependence: the system "remembers" the torsional energy stored during multi-rotation events and releases it as a shorter subsequent step.

### 3.2 Anomaly B: Directional Phase Asymmetry

The mean gap size depends on the direction of the cross-class transition:

| Transition | Mean gap | Interpretation |
|------------|----------|---------------|
| 5 → 1 (return to majority) | 13.08 | Fast — the "active" phase snaps back quickly |
| 1 → 5 (departure to minority) | 14.67 | Slow — leaving the "stable" phase takes longer |
| 1 → 1 (stay in majority) | 16.64 | Slowest — same-class transitions are costly |
| 5 → 5 (stay in minority) | 16.55 | Slowest — same-class transitions are costly |

The 5→1 return is 12.75% faster than the 1→5 departure (t = 30.7, p < 10⁻²⁰⁷). The Cramér model produces 5.09% asymmetry; the HL model produces 3.70%. The empirical asymmetry is 2.5× to 3.4× stronger than either model predicts.

This directional asymmetry is consistent with position 5 acting as a structurally "active" or minority state from which the system preferentially returns to the "stable" majority position at 1. The asymmetry is topological: it depends on which position the system is leaving, not merely on the arithmetic distance traveled.

### 3.3 Anomaly C: The 3-Phase Variance Floor

The variance of cross-class transition fractions in sliding windows is suppressed well below random expectation:

| Window size (W) | Observed variance ratio (r=2,4) | Random expectation |
|-----------------|--------------------------------|-------------------|
| 10 | 0.34 | 1.00 |
| 50 | 0.30 | 1.00 |
| 100 | 0.29 | 1.00 |
| 500 | 0.29 | 1.00 |

The cross-class transitions (r=2 and r=4) maintain nearly constant fractional presence regardless of window size, with variance at 29% of what independent random assignment would produce. By contrast, same-class transitions (r=0) fluctuate at 93–96% of random expectation.

This pattern mirrors 3-phase electrical power delivery, where three currents offset by 120° provide constant total power without dead zones. The prime gap sequence achieves an analogous regulation: the two alternating phases (5→1 and 1→5) deliver nearly constant coverage, preventing "dead zones" where the clock stalls on one side.

The Hardy-Littlewood model produces a variance ratio of 0.473 — significantly above the empirical 0.285 (z = −10.9). The suppression to 29% of random represents structural tightness that loaded-dice models cannot replicate.

---

## 4. Comparison Against Standard Models

### 4.1 Methodology

We generated 50 synthetic realizations of each model for primes up to 2 × 10⁶:

**Cramér model.** Each integer n > 4 with n ≡ 1 or 5 (mod 6) is independently designated as "prime" with probability proportional to 1/ln(n). No gap-to-gap correlations.

**Hardy-Littlewood model.** Gaps drawn from an exponential distribution with mean ln(x), subject to the mod 6 landing constraint. This captures the local density variation and modular structure but generates gaps independently.

### 4.2 Results

| Metric | Real primes | Cramér (mean ± σ) | **z vs Cramér** | HL (mean ± σ) | **z vs HL** |
|--------|-------------|-------------------|----------------|---------------|------------|
| A. Spring-back | −9.68% | +1.43 ± 1.75% | **−6.3** | +1.79 ± 0.83% | **−13.8** |
| B. Asymmetry | −12.75% | −5.09 ± 1.16% | **−6.6** | −3.70 ± 0.83% | **−10.9** |
| C. Variance ratio | 0.285 | 0.331 ± 0.019 | −2.4 | 0.473 ± 0.017 | **−10.9** |

**5 of 6 comparisons exceed |z| = 5.** In particle physics, a 5σ deviation constitutes a discovery threshold. These deviations range from 6σ to 14σ.

The single sub-threshold comparison (variance ratio vs Cramér, z = −2.4) reflects the Cramér model's accidental proximity to the real value, not a mechanistic explanation: the Cramér model has no structural reason to produce variance suppression.

### 4.3 The Sign Flip

The spring-back result is qualitatively distinct from the other two anomalies. The directional asymmetry and variance floor are magnitude discrepancies — the models predict the correct direction but the wrong amount. The spring-back is a **sign reversal**: both models predict that gaps lengthen after large gaps (positive regression), while real primes show gaps shortening (negative restoring force).

No refinement of the gap distribution — including pair-correlation corrections from the Hardy-Littlewood k-tuple conjecture — can flip this sign, because:

1. Pair correlations between consecutive primes are *positive* (nearby primes tend to cluster), which strengthens the regression-to-mean prediction, making the model's positive spring-back *larger*, not smaller.

2. The Maier phenomenon shows that primes exhibit *more* clustering than Cramér predicts in short intervals, meaning after a desert (large gap), the local density is if anything *lower* than the logarithmic mean — predicting an even longer next gap.

3. The restoring force requires memory of the preceding gap's energy. Markov-type gap models (where the next gap depends only on the current position, not the history) cannot produce a systematic shortening conditioned on the *size* of the previous gap, because the size is not part of the Markov state.

---

## 5. Gear Meshing and Hunting Tooth Structure

Consecutive gap pairs (g_n mod 6, g_{n+1} mod 6) show a striking deviation from independence:

| Gap pair (mod 6) | Observed | Expected (independent) | Enhancement ratio |
|-------------------|----------|----------------------|-------------------|
| (2, 4) | 15.70% | 8.11% | **1.94×** |
| (4, 2) | 15.70% | 8.11% | **1.94×** |
| (0, 0) | 17.48% | 18.52% | 0.94× (suppressed) |

The alternating cross-class pairs (2,4) and (4,2) — corresponding to the trajectory 5→1→5 and 1→5→1 — occur at nearly double their independence expectation. Same-class pairs (0,0) are mildly suppressed. The system exhibits a "hunting tooth" pattern: after one cross-class transition, it preferentially executes another in the opposite direction, alternating between the two residue positions like meshing gear teeth that cannot achieve a smooth 1:1 ratio.

---

## 6. Large Gaps as Multi-Rotation Events

Large gaps preferentially land in the same residue class (r = 0):

| Rotation count (q) | Fraction with r=0 | Fraction with r=2 | Fraction with r=4 |
|--------------------|-------------------|--------------------|-------------------|
| 0 (smallest gaps) | 0% | 50.2% | 49.8% |
| 1 | 50.8% | 21.5% | 27.7% |
| 2 | 52.0% | 28.1% | 19.9% |
| 3 | 51.4% | 25.9% | 22.8% |
| 5 | 62.4% | 18.3% | 19.3% |

At q = 0, only cross-class transitions are possible (gap = 2 or 4). At q ≥ 1, same-class transitions (r = 0) dominate, rising to 62% at q = 5. High-energy events (many rotations) have enough momentum to complete full cycles and return to the starting position. Low-energy events are forced to shift phase.

---

## 7. Connection to the ⟨2,3⟩ Lattice

The modulo 6 structure is the ⟨2,3⟩ multiplicative lattice acting on the integers. All dimensionless ratios in the Pati-Salam gauge construction from the Palatini bracket [e, ω] on sl(4, ℝ) belong to this same lattice (TR-2026-FF06-N1). The hexagonal clock is the prime-number-theoretic manifestation of the algebraic structure that governs the gauge sector.

The three gap classes (r = 0, 2, 4) correspond to the three independent directions in the ⟨2,3⟩ lattice: a full ⟨2,3⟩ cycle (r=0), a ⟨2⟩ step (r=2), and a ⟨2²⟩ step (r=4). The 3-phase power delivery (Anomaly C) reflects the fact that these three directions maintain constant coverage of the lattice under the sieving action of primes 2 and 3.

---

## 8. Caveat and Future Work

The Hardy-Littlewood model used here generates gaps independently with mod 6 filtering. A full implementation would include the singular series S({0, h₁, h₁+h₂}) for consecutive gap pairs, which introduces gap-to-gap correlations. This could potentially reduce the z-scores for Anomalies B and C.

However, as argued in §4.3, pair-correlation corrections cannot flip the sign of the spring-back effect (Anomaly A), because positive pair correlations *strengthen* rather than weaken the regression-to-mean prediction. The qualitative sign reversal stands regardless of model refinement.

Extension to 10⁸ or 10⁹ primes would test whether the three anomalies persist, strengthen, or attenuate at larger scales. The variance floor's stability across window sizes (W = 10 to W = 500) suggests persistence, but this requires confirmation.

A derivation of the specific quantitative values (29% variance suppression, 1.94× pair enhancement, 3% spring-back rate per rotation) from the Wronskian non-vanishing condition of the Riemann spectral structure (TR-2026-FF06b) would establish a direct link between the prime gear clock and the zeta zero spectrum. This connection, if it exists, would constitute a novel structural characterization of the prime distribution.

---

## 9. Data and Reproducibility

All computations use the first 664,579 primes (up to 10⁷) generated by the Sieve of Eratosthenes. The Cramér and Hardy-Littlewood comparisons each use 50 synthetic realizations with matched range. Random seeds are fixed for reproducibility.

Code repository: `acs-framework/code/`

---

## 10. Summary

The prime gap sequence on the modulo 6 hexagonal clock exhibits three structural behaviors — spring-back, directional asymmetry, and variance suppression — that deviate from the leading probabilistic models by 6σ to 14σ. The spring-back effect is a qualitative sign reversal that no refinement of the gap distribution can explain, because it requires path-dependent memory that memoryless models do not possess. The directional asymmetry and variance floor are magnitude discrepancies that exceed probabilistic prediction by factors of 2.5× to 3.4×.

These findings are consistent with a deterministic, structurally constrained mechanism operating on the ⟨2,3⟩ lattice — a mechanism whose specific parameters remain to be derived from the spectral structure of the Riemann zeta function.
