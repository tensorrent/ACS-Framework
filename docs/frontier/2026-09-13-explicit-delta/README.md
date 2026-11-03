# Gaussian explicit-formula delta

The certified finite Q(zeta_5) spectra now agree with a declared explicit formula that includes pole, discriminant, gamma and prime-power terms, with separate bounds on every omitted tail. All 30 cases agree at both working precisions. The unknown-zero bound allows zeros off the critical line and does not assume GRH. This advances the bridge from finite observations to arithmetic while leaving unsmoothed limits, statistical calibration and operator identification open.

The [derivation and reproduction instructions](../../../code/frontier_verification/EXPLICIT_README.md) specify `h(t)=exp(-a*t^2)*cos(u*t)` and its Gaussian Fourier partner. They specialize [Belabas–Friedman's stated Weil–Poitou identity](https://arxiv.org/pdf/1305.0035) and derive the truncation bounds. The full zero sum equals pole plus discriminant plus gamma minus the prime-power sum. Both signs of zero height and the correct primitive Euler coefficients are included.

## What was checked

The [two-precision archive](Gaussian_Audits.zip) contains every integration segment, eligible prime-power contribution, finite factor sum and error bound. The fixed grid has three widths a=1/25,1/100,1/400 and ten frequencies: 0; log of 2,3,5,11,19,139,16,361; and 2.2. Each case retains zero cutoffs 60,100,220 and prime-power cutoffs 1000,10000,100000. There are 2,436 nonzero prime-power coefficients through the final cutoff. The 160-bit and 224-bit runs use different gamma-integration partitions.

The [cross-method audit](Cross_Method.json) recomputes all 30 zero, prime, gamma and arithmetic values with mpmath at 60 digits. It generates prime powers by a separate sieve and tests the residue of the entire power, independently of the producer's residue-degree stepping. Nine cases also evaluate a different gamma integral, using the digamma function in the zero-frequency variable with interval quadrature. All comparisons pass.

The [algebra audit](Algebra_Audit.json) checks six exact polynomial/calculus identities, the cyclotomic discriminant 125, six gamma-duplication controls and nine digamma-bound controls. The product of the four primitive completed factors is 20 times the chosen completed Dedekind function; that constant cancels on logarithmic differentiation. These checks support the written argument and do not replace its analytic premises.

## The unconditional tail argument

At s=2, the logarithmic-derivative identity gives the positive moment `M=sum Re(1/(2-rho))`. Its elementary upper bound is approximately 1.083971406029394. Subtracting a finite positive prime sum and the certified finite zero moment gives an upper bound of approximately 0.050037848535216 for the remaining moment beyond height 220. The underlying Hadamard-product identity is [Grenié–Molteni, equations (2.1)–(2.7)](https://arxiv.org/pdf/1407.1375); unlike their subsequent critical-strip estimates, its use here at s=2 is unconditional.

For 0<beta<1, the inequality `Re(1/(2-rho)) >= 1/(4+gamma^2)` and a Gaussian envelope bound control all unknown zeros, including off-line ones. Separate integral comparisons bound the prime tail and both omitted ends of the gamma integral. The largest final zero-tail bound across the 30 cases is below 6.6e-49. Every final residual enclosure contains zero and lies inside ±7e-24. Root-location uncertainty from the inherited brackets dominates that error; agreement of the two arithmetic precision runs cannot reduce it.

## A concrete correction to peak interpretation

At a=1/400 and u=log(2), the local Euler coefficient for 2 is zero and the entire smoothed prime contribution is only about 1.40e-36. Nevertheless, the certified signed zero sum is about **-0.736822760644**. The pole term is about 2.122646583181 and the gamma term about -2.859469343825; the discriminant contribution is tiny. Thus a nonzero raw zero amplitude does not imply a nonzero local prime coefficient.

At the residue-degree frequency log(16), the smoothed prime contribution is about 3.910677237125 while the zero sum is about -0.191877355194, after the pole and gamma terms are included. These finite examples demonstrate the need to subtract the specified background and control smoothing leakage. They are not new universal ratios or statistical significance claims. The [compact summary](Gaussian_Summary.json) retains all 30 decompositions, including ramified, nonsplit and off-peak cases.

## Adversarial checks and retained failures

Ten deliberate variants are tested over the same 30 cases: omitting negative zeros, doubling one positive conjugate list, separately normalizing factors, omitting pole/gamma/discriminant/gamma-normalization/ramified terms, omitting the residue-degree multiplier, and reversing the prime sign. All ten are rejected in at least one case; 252 of the 300 individual comparisons reject their variant. The remaining 48 are retained as inconclusive at that case's error scale. Altered zero weights receive their own conservative unknown-tail allowances.

The [execution archive](Execution_Artifacts.zip) preserves five successful recorded commands and four unsuccessful commands. The initial alternate gamma implementation omitted its elementary `-4*log(2*pi)*g(0)` normalization, which the zero-frequency test rejected. Two subsequent failures exposed the comparison string being rounded too aggressively near an enclosure edge; the final check uses all 60 computed digits without widening the producer certificate. A malformed local command failed before running mathematics. Development probes also retain the python-flint real-power edge case for a ball straddling zero and its multiplication-based correction. The [development notes](Development_Notes.json) distinguish these cases.

## Evidence and next gates

[Execution receipts](Execution_Receipts.json), [source inventory](Source_Inventory.json), [source snapshot](Source_Snapshot.zip), [runtime](Runtime.json), [primary-source references](Primary_Sources.json), and [download identities](Download_Receipts.json) identify the inputs and methods. Primary papers remain linked at their sources; only their identities and retrieval receipts are packaged. The [manifest](Manifest.json) and [verification result](Verification.json) check retained evidence and reported-computation consistency, recursively preserving prior checkpoints. They do not rerun quadrature or formalize the analytic proof.

The [queue](Research_Queue.json) advances P05, R12, R13 and K04, retaining all 115 branches. The [ledger](Branch_Events.jsonl) extends the unchanged 346-event prefix to 350 events. Next: recover individual arithmetic coefficients with explicit smoothing-leakage bounds and joint height/width/root-precision budgets; separately specify the statistical comparison. Taking a toward zero with fixed height 220 is not justified. Natural operators, independent real-part arguments, geometric topology, physical identifications and private benchmark inputs retain their prior gates. The ongoing investigation has no global completion or exhaustion claim.
