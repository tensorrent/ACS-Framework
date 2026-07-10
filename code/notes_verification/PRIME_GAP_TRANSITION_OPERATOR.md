> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# The Prime Gap Dynamical Dynamical Dynamical Dynamical Dynamical Transition Operators over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembles on (Z/mZ)*

### Empirical Kernel Law, Compression Law, and Three Falsified Conjectures

*Bradley Wallace · Koba42 / TensorRent*
*May 2026*

---

## Abstract

We study the empirical second-order Dynamical Dynamical Dynamical Dynamical Dynamical Transition Operators over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembles $T_m$ describing prime-gap dynamics on the multiplicative residue group $(\mathbb{Z}/m\mathbb{Z})^*$. Writing $T_m = T_0 + P_m$ where $T_0$ is the uniform transport respecting residue continuity, we establish two empirical laws verified across moduli $m \in \{6, 10, 12, 14, 15, 18, 20, 24, 30, 42, 60, 66, 84, 90\}$:

**Kernel Law.** $\dim \ker(P_m) = \varphi(m)$ exactly, with kernel equal to the space of state-space functions depending only on the source residue class. The kernel is naturally spanned by Dirichlet characters on $(\mathbb{Z}/m\mathbb{Z})^*$.

**Compression Law.** While the algebraic rank of $P_m$ grows quadratically with $\varphi(m)$, the effective dynamical rank follows $r_\text{eff} \sim \varphi(m)^{1.6}$, so the ratio $r_\text{eff}/r_\text{alg}$ vanishes as $\varphi(m)^{-0.64}$ for large $m$. The active spectrum is heavy-tailed with power-law exponent $\alpha \approx 1.16$.

We also document three conjectures that were tested and falsified during the investigation: uniform spectral contraction $\rho(P_m) < 1$, full character-product block-diagonalization of the active sector, and universal renormalized spectral law $P_m / \rho(P_m)$. These negative results constrain what the surviving structure can mean.

The computational data range covers 50,847,531 primes up to $10^9$ (sieved Rust implementation) for low-modulus statistics, and $1.27 \times 10^6$ primes up to $2 \times 10^7$ for the operator-theoretic analysis.

---

## 1. Setup

Let $m \geq 2$ and let $U_m = (\mathbb{Z}/m\mathbb{Z})^* = \{a \in \{1, \ldots, m-1\} : \gcd(a, m) = 1\}$, with $|U_m| = \varphi(m)$. Define the *transition state space*
$$
\mathcal{S}_m = \{(a, b) : a, b \in U_m\}
$$
with $|\mathcal{S}_m| = \varphi(m)^2$. For each prime gap $p_{i+1} - p_i$ with $p_i, p_{i+1} > m$ and $\gcd(p_i, m) = \gcd(p_{i+1}, m) = 1$, the pair $(p_i \bmod m, p_{i+1} \bmod m) \in \mathcal{S}_m$ is the *transition class*.

Construct the empirical second-order Dynamical Dynamical Dynamical Dynamical Dynamical Transition Operators over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembles $T_m : \mathbb{R}^{\mathcal{S}_m} \to \mathbb{R}^{\mathcal{S}_m}$ by
$$
T_m\bigl[(a,b), (a', b')\bigr] = \frac{N\bigl((a,b) \to (a',b')\bigr)}{\sum_{(c,d)} N\bigl((a,b) \to (c,d)\bigr)}
$$
when $b = a'$, and zero otherwise (residue continuity). $T_m$ is row-stochastic.

The *unbiased reference* $T_0$ assigns uniform $1/\varphi(m)$ probability to each consistent next state. The perturbation is
$$
P_m = T_m - T_0.
$$

By construction, $P_m$ has row sums zero and is supported on the same sparsity pattern as $T_m$.

---

## 2. The Kernel Law

**Empirical Theorem (Kernel Law).** For all tested moduli $m \in \{6, 10, 12, 14, 15, 18, 20, 24, 30, 42, 60, 66, 84, 90\}$:
$$
\dim \ker(P_m) = \varphi(m).
$$
Moreover, the kernel equals the *left-source sector*:
$$
\ker(P_m) = \bigl\{f \in \mathbb{C}^{\mathcal{S}_m} : f(a, b) = g(a) \text{ for some } g : U_m \to \mathbb{C}\bigr\}.
$$

**Verification.** For $m = 42$ ($\varphi(m) = 12$), we constructed the 12 Dirichlet characters $\chi_1, \ldots, \chi_{12}$ on $U_{42}$ and tested left-extension vectors $v_\chi(a, b) = \chi(a)$ and right-extension vectors $w_\chi(a, b) = \chi(b)$.

Result:
- $\|P_{42} v_\chi\| < 10^{-3}$ for **all 12** left-character vectors (numerical zero)
- $\|P_{42} w_\chi\| > 0.05$ for **all 12** right-character vectors (clearly nonzero)

The kernel dimension match across all 14 tested moduli, combined with the explicit annihilation verification at $m = 42$, establishes the law empirically.

**Interpretation.** The kernel consists precisely of state-space functions that ignore the destination coordinate. The Dirichlet characters on $U_m$ provide a natural orthonormal basis for this $\varphi(m)$-dimensional kernel.

**Mechanism (conjectural).** $T_0$ preserves any function of the source coordinate alone because uniform forward transport averages over all destinations. The empirical perturbation $P_m$ encodes arithmetic corrections that act through *destination bias* (which residue class is preferred next), not source structure. Hence functions depending only on the source automatically lie in $\ker(P_m)$.

---

## 3. The Compression Law

**Definitions.** The *algebraic rank* is $r_\text{alg}(m) = \mathrm{rank}(P_m) = \varphi(m)^2 - \varphi(m)$. The *effective dynamical rank* (participation ratio) is
$$
r_\text{eff}(m) = \frac{\bigl(\sum_i |\lambda_i|\bigr)^2}{\sum_i |\lambda_i|^2}
$$
where the sum runs over the nonzero eigenvalues of $P_m$.

**Empirical Scaling.** Across the tested range:

| $m$ | $\varphi(m)$ | $r_\text{alg}$ | $r_\text{eff}$ | $r_\text{eff} / r_\text{alg}$ |
|---|---|---|---|---|
| 6 | 2 | 2 | 1.53 | 0.767 |
| 12 | 4 | 12 | 7.07 | 0.589 |
| 30 | 8 | 56 | 15.3 | 0.274 |
| 42 | 12 | 132 | 36.5 | 0.277 |
| 60 | 16 | 240 | 43.0 | 0.179 |
| 90 | 24 | 552 | 100.5 | 0.182 |

Log-log fits yield:
$$
r_\text{eff}(m) \approx 0.59 \cdot \varphi(m)^{1.61}, \qquad \frac{r_\text{eff}(m)}{r_\text{alg}(m)} \approx 1.23 \cdot \varphi(m)^{-0.64}.
$$

In particular, $r_\text{eff}/r_\text{alg} \to 0$ as $\varphi(m) \to \infty$ in the tested regime. The active sector becomes increasingly compressible as arithmetic complexity grows.

---

## 4. The Heavy-Tailed Spectrum

The distribution of nonzero eigenvalue magnitudes $|\lambda|$ of $P_m$ is heavy-tailed. Combining data from $m \in \{42, 60, 90\}$ (924 nonzero eigenvalues total):

| Quantile | $|\lambda|$ |
|---|---|
| 50% | 0.015 |
| 75% | 0.025 |
| 90% | 0.055 |
| 95% | 0.124 |
| 99% | 0.323 |

A power-law fit on the top 30% of eigenvalues gives
$$
P(|\lambda| > x) \sim x^{-1.16}.
$$
The 99th percentile is approximately 20× the median. A small number of dominant modes carry most of the dynamical mass; the bulk of the spectrum is negligible.

---

## 5. Three Falsified Conjectures

The investigation proposed and explicitly tested three conjectures that did not survive the data.

### 5.1 Uniform spectral contraction — FALSIFIED

**Conjecture:** $\rho(P_m) < 1$ uniformly in $m$, with $P_m$ behaving as a quasi-nilpotent contraction (the "gear-clock" picture from low-modulus data).

**Falsification:**

| $m$ | $\varphi(m)$ | $\rho(P_m)$ |
|---|---|---|
| 6 | 2 | 0.145 |
| 30 | 8 | 0.341 |
| 60 | 16 | 0.586 |
| 90 | 24 | 0.745 |

Power-law fit: $\rho(P_m) \approx 0.07 \cdot \varphi(m)^{0.75}$. The fit predicts $\rho(P_m) = 1$ near $\varphi(m) \approx 50$. The contraction principle is a low-modulus artifact.

### 5.2 Character-product block-diagonalization — FALSIFIED

**Conjecture:** $P_m$ acts block-diagonally in the basis $\{\chi_i(a) \overline{\chi_j(b)}\}$ of $\varphi(m)^2$ character products on the state space, with off-diagonal entries (mixing different $\chi_i$) vanishing.

**Falsification:** Define the *left-preserved norm fraction* as the ratio of $\|P_m\|_F$ contributions from entries with $i_1 = i_2$ (left-character preserved) to the total $\|P_m\|_F$:

| $m$ | Left-preserved fraction |
|---|---|
| 6 | 71% |
| 12 | 53% |
| 30 | 36% |
| 42 | 29% |

The fraction *decreases* with $\varphi(m)$. At $m = 42$, only 29% of the perturbation norm respects the left-character block structure. The character structure is exact at the kernel boundary (Section 2) but does not extend to global block-diagonalization of the active sector.

### 5.3 Universal renormalized spectral law — FALSIFIED

**Conjecture:** The normalized operator $P_m / \rho(P_m)$ has a universal spectral distribution as $m \to \infty$.

**Falsification:** The mean of $|\lambda|/\rho(P_m)$ over the nonzero spectrum:

| $m$ | $\varphi(m)$ | Mean $|\lambda|/\rho$ |
|---|---|---|
| 6 | 2 | 0.645 |
| 12 | 4 | 0.402 |
| 30 | 8 | 0.126 |
| 60 | 16 | 0.054 |
| 90 | 24 | 0.040 |

The normalized mean decreases monotonically by a factor of 16 across the tested range. No universal renormalized law exists in this normalization. The spectrum becomes more concentrated on a small number of dominant modes as $\varphi(m)$ grows, consistent with the heavy-tail observation.

---

## 6. What This Means for Low-Modulus Statistics

The strong low-modulus anomalies that motivated this study — the prime-gap spring-back, directional asymmetry, and variance suppression on the mod-6 hexagonal clock — are now seen as manifestations of the *dominant low-frequency modes* of $P_m$.

At $m = 6$, $r_\text{eff} \approx 1.5$ out of $r_\text{alg} = 2$: essentially the entire active sector is dominated by one or two modes. These modes correspond to the Chebyshev bias (driven by $L(s, \chi_3)$) and the alternating "hunting tooth" structure (lag-1 anti-correlation).

At larger moduli, these modes persist but are joined by a high-dimensional bulk of weakly active modes. The dominant modes still carry most of the variance, but the algebraic state space is much richer. The mod-6 "gear-clock" picture captures the dominant transport but not the asymptotic structure.

---

## 7. Open Problems

1. **Derive the Kernel Law.** The empirical exactness of $\dim \ker(P_m) = \varphi(m)$ across all tested moduli strongly suggests an algebraic theorem. The likely route: show that admissible residue-class transition constraints together with stationarity under source averaging force left-source-only functions into the nullspace of any arithmetic perturbation of $T_0$.

2. **Derive the Compression Law.** Whether $r_\text{eff} \sim \varphi(m)^{1.6}$ is a fundamental scaling or an intermediate asymptotic regime remains open. Pushing to $\varphi(m) > 100$ would test extrapolation.

3. **Connection to L-functions.** The dominant low-modulus mode at $m = 6$ has eigenvalue 0.152, attenuation rate $\sim 1/\log(x)$, and is structurally consistent with the $L(s, \chi_3)$ explicit formula contribution to the Chebyshev bias. A rigorous derivation of mode eigenvalues from L-function zero spectra remains open.

4. **Asymptotic spectral law.** The heavy-tailed distribution with exponent $\alpha \approx 1.16$ may or may not be universal. The tail exponent should be measured at larger $m$ to distinguish a fixed limiting law from a slowly varying one.

---

## 8. Honest Scope Boundary

This note establishes empirical regularities of an operator constructed from prime-gap data. It does not constitute a proof of any number-theoretic theorem about primes. The Kernel Law is verified across 14 moduli and explicitly mechanism-tested at $m = 42$; it is presented as an empirical theorem awaiting rigorous proof. The Compression Law is a fitted scaling law; the underlying mechanism is open. The falsified conjectures are documented to constrain what the surviving structure can mean.

The conjectures that did *not* survive — uniform contraction, character-product block-diagonalization, and universal renormalized law — were tested and explicitly killed. Their failure modes are documented because negative results constrain the theoretical interpretation of the positive results.

---

## 9. Data and Reproducibility

All computations use primes generated by the Sieve of Eratosthenes implemented in Python (up to $2 \times 10^7$) and Rust (up to $10^9$ for the low-modulus statistics). The Rust sieve is segmented and parallelized via Rayon; the Python implementation is single-threaded and suffices for the operator-theoretic range.

Code repository: `hex_clock_sieve` (Rust) and `acs-framework/code/` (Python).

The operator construction, kernel verification, and scaling-law extraction are deterministic and reproducible from the source primes. No random sampling enters the analysis except in the explicit Cramér and Hardy-Littlewood comparisons reported separately.

---

## 10. Summary

The empirical prime-gap Dynamical Dynamical Dynamical Dynamical Dynamical Transition Operators over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembless over Prime Gap Ensembles $P_m = T_m - T_0$ on the multiplicative residue group $(\mathbb{Z}/m\mathbb{Z})^*$ admits the following structure, verified across moduli with $\varphi(m) \leq 24$:

**Surviving Tier-1 result:** The kernel is exactly $\varphi(m)$-dimensional and consists of source-residue-only functions.

**Surviving Tier-3 results:** The effective dynamical rank scales as $\varphi(m)^{1.6}$, sub-quadratically in the algebraic rank, so the active sector is increasingly compressible. The spectrum is heavy-tailed with power-law exponent $\approx 1.16$.

**Falsified Tier-4 conjectures:** Uniform spectral contraction (replaced by growing $\rho \sim \varphi^{0.75}$), character-product block-diagonalization (replaced by kernel-only character invariance), and universal renormalized spectral law (replaced by progressive concentration on dominant modes).

The structure that survives three rounds of explicit falsification is real, falsifiable, and reproducible.
