# Local Euler information and ordinate uncertainty

The [quadratic checkpoint](QUADRATIC_README.md) identified 83 of 91 prime-power coefficients through 361 at additional ordinate radius `0.005`. General degree-four local Euler relations now resolve the remaining eight without using the discriminant to label ramified primes and without assuming the field is Galois.

A separate experiment increases the radius to `0.01`, `0.02` and `0.03`. With the Galois premise and ramification information explicitly supplied, alternating local relations and spectral inequalities identifies respectively 91, 82 and 62 targets from retained measurements through height 2000. All 91 are already identified through height 1000 at radius `0.01`. The same wide measurements using only coefficient boxes give 38, 17 and 10 targets. These are conditional sufficient bounds on a tested grid, not optimal noise thresholds.

## General local models and explicit assumptions

For a quartic number field and a rational prime, write the local ramification indices and residue degrees as positive pairs `(e_i,f_i)`. The general relation is `sum_i e_i f_i=4`. For a Galois extension all pairs agree; hence `efg=4`. The field discriminant determines which rational primes ramify. These premises are distinguished in [Milne, Theorems 3.34–3.35](https://www.jmilne.org/math/CourseNotes/ANT.pdf), printed pages 59–60.

The [catalogue](dedekind_local_profiles.py) enumerates every nondecreasing multiset of positive pairs with total degree four. Recursion subtracts a positive product `ef` from the remaining degree, and permits the same pair again. Every multiset has one sorted representation; induction on the remaining degree proves completeness of this finite enumeration. There are eleven profiles: five unramified and six ramified. An independent audit constructs the same set from ordered compositions of four and divisors of their parts, then removes permutations. Galois profiles are independently enumerated from all positive triples satisfying `efg=4`.

Four assumption sets are kept separate:

- `degree`: all eleven degree-four profiles.
- `degree_discriminant`: additionally use the given discriminant 125 to select ramified or unramified profiles at each prime.
- `galois`: additionally assume the extension is Galois, with no local use of the discriminant.
- `galois_discriminant`: use both added restrictions.

The explicit-formula calculation still uses the supplied field invariants in every case. Withholding the discriminant here means withholding its *local ramification labels*, not removing it from the analytic formula. Galois structure is an additional premise in these inference experiments; it is not inferred from the zero ordinates. The known cyclotomic witness has that structure, but no prime residue-class splitting rule or field-polynomial factorization enters the decoder.

## Euler coefficients and auditable exclusions

For a local model, the Euler denominator is

```
P(X) = product_i (1-X^f_i).
```

Its logarithmic derivative gives

```
-X P'(X)/P(X) = sum_i f_i X^f_i/(1-X^f_i)
              = sum_{k>=1} c_(p^k) X^k,
c_(p^k) = sum_{i: f_i divides k} f_i.
```

The ramification indices constrain the degree budget but do not multiply these coefficients. The independent audit checks the rational-function identity symbolically for every catalogue entry. This exact identity explains the full coefficient sequence; the first twelve coefficients are also retained for inspection.

For each prime, keep exactly the profiles whose coefficients belong to every previously certified domain at that prime's observed powers. Every rejected profile has an explicit contradicting observation. Projecting the surviving profiles back to each coefficient gives another valid domain restriction. All 604 coefficient coordinates through 4096 participate, including nuisance coefficients beyond the 91 targets.

The [combined inference instrument](dedekind_local_noise.py) alternates that local filtering with the inherited positive spectral inequalities

```
sum_n W_mn c_n + q_m belongs to R_m,    0 <= q_m <= B_m.
```

All weights, observations and tail bounds are rounded outward to the integer grid `2^-192`. For a proposed value at coordinate `i`, the other coordinates retain their current certified endpoints. A value is removed only when its complete minimum is above the observation or its complete maximum is below it. Each strict integer gap and each prerequisite-domain hash is recorded. Local filtering and spectral filtering are synchronous within their respective stages. Finite monotone domains guarantee termination of this particular closure procedure; a stable domain is not a feasibility certificate.

Both precision runs cover 22 starting cases and four assumption sets: five narrow stationary prefixes, fifteen wider prefixes, and the preceding shared and quadratic results. Each assumption set starts independently from its declared input domains. The local-only result is recorded before spectral feedback, so the contributions can be separated.

## What information resolves the eight targets?

At radius `0.005`, all four assumption sets identify 91 targets from the quadratic seed. Under the weakest set, several conclusions need just one already certified observation:

- `c_4=0` determines `c_64=0` and `c_256=4`.
- `c_9=0` determines `c_81=4`.
- `c_2=0`, `c_3=0` and `c_7=0` respectively determine `c_128=0`, `c_243=0` and `c_343=0`.
- For `c_125=1`, one minimum witness uses the observations at 5 and 125.
- For `c_361=4`, the minimum witness uses the observations at 19 and 361.

The [audit](dedekind_local_noise_audit.py) verifies minimum cardinality by exhaustive hitting sets: every catalogue model giving a different target value must be contradicted by the selected observations. It checks every smaller subset, records the number of minimum-size alternatives, and verifies the displayed witness. These minima concern the available finite observation domains under each stated assumption set, not every possible analytic proof.

From the older 73-target stationary seed at radius `0.005`, the degree-plus-discriminant model identifies 86 targets locally and 91 after spectral feedback. From the older 81-target shared seed, it identifies 90 locally and 91 after feedback. Stronger local information can therefore substitute for some of the more precise error modeling, with that information explicitly charged as a premise.

## Wider uncertainty and remaining arithmetic ambiguity

At retained height 2000, the four assumption sets give the following singleton counts, in the order `degree`, `degree_discriminant`, `galois`, `galois_discriminant`:

- Radius `0.005`, stationary seed: 83, 91, 89, 91.
- Radius `0.01`: 53, 68, 67, 91.
- Radius `0.02`: 31, 36, 35, 82.
- Radius `0.03`: 22, 26, 26, 62.

For `galois_discriminant` at radius `0.01`, counts across retained heights 220, 600, 1000, 1500 and 2000 are 75, 84, 91, 91 and 91. At radius `0.02`, the nine remaining targets are 269, 271, 281, 283, 289, 311, 313, 359 and 361. All remaining domains for every case are retained.

Identifying these coefficients still leaves 48 of the original 72 prime-local factors ambiguous. Even when all 91 target coefficients are singletons, only 24 of those local models are determined. Their next distinguishing powers, outside the target cohort, retain the earlier [local-identifiability gate](dedekind_local_identifiability.py). Surviving local profiles also do not establish simultaneous realization by any number field.

## Independent verification and counterchecks

The [wider-range audit](dedekind_wide_audit.py) replays 10,592 prior-stage exclusions, verifies 560,440 strict phase brackets and independently recomputes twelve full scalar extrema sums with 80-digit mpmath. The 160- and 224-bit runs agree on all 30 wider cases. Original membership at every cutoff remains valid through radius `0.03`; every included and excluded certified root interval is checked against the cutoff.

The independent local audit uses a separately enumerated catalogue, exact dyadic spectral-gap calculations, held-out arithmetic values for all 604 coefficients, and exhaustive minimum-observation witnesses. It checks every local and spectral exclusion, every assumption-inclusion comparison and agreement of the two precision runs. Analytic row reconstruction shares the pinned loader; the distinct wider-range audit checks the new range calculations. No new Lean claim is made for these computational catalogues.

Three controls test material assumptions. The irreducible quartic `x^4-x-1` has polynomial discriminant `-283`; modulo 7 it factors as one linear and one irreducible cubic factor. Since 7 is unramified, its coefficient at 7 is one, and its local type is excluded by an unsupported Galois restriction. A ramified `(e,f)=(4,1)` model has coefficient one, while incorrectly multiplying by `e` gives four. A spectral exclusion also fails when its previously proved domains are reset to unrestricted boxes.

The first local audit stopped while printing an exact rational gap with more than 4,300 digits. Its successor was deliberately stopped after 453 seconds because fraction normalization was too costly. Both attempts and source versions are retained. The successful audit aligns dyadic mantissas at their least exponent and adds shifted signed integers. This computes the same full exact sums without discarding or rounding any term, then compares each gap against its positive fixed-grid lower bound.

An [elementary adversary check](dedekind_local_adversary.py) independently verifies all six possible monic factors of degree one or two over the two-element field, every cubic residue modulo seven, and the discriminant by a Bareiss determinant. It confirms that the counterexample has field discriminant -283 and local degrees 1 and 3 at seven, independently of the symbolic factorization routine.

## Reproduction and continuation

Use the [pinned analytic dependencies](source_requirements.txt). Extract the producer archive from the [checkpoint](../../docs/frontier/2026-09-13-local-noise-delta/README.md) into a scratch directory and copy its inherited `Measurements.json` input from the coupled checkpoint. Exact commands and receipts are retained. Core commands are:

```sh
$PYTHON code/frontier_verification/dedekind_ordinate_ranges.py --input "$AUDIT/Measurements.json" --precision 160 --deltas 1e-2 2e-2 3e-2 --methods stationary --output "$AUDIT/Wide_Ranges160.json"
$PYTHON code/frontier_verification/dedekind_ordinate_ranges.py --input "$AUDIT/Measurements.json" --precision 224 --deltas 1e-2 2e-2 3e-2 --methods stationary --output "$AUDIT/Wide_Ranges224.json"
$PYTHON code/frontier_verification/dedekind_local_noise.py --directory "$AUDIT" --prior docs/frontier/2026-09-13-quadratic-delta --precision 160 --output "$AUDIT/Local_Noise160.json"
$PYTHON code/frontier_verification/dedekind_local_noise.py --directory "$AUDIT" --prior docs/frontier/2026-09-13-quadratic-delta --precision 224 --output "$AUDIT/Local_Noise224.json"
$PYTHON code/frontier_verification/dedekind_wide_audit.py --directory "$AUDIT" --prior docs/frontier/2026-09-13-coupled-delta --output "$AUDIT/Wide_Audit.json"
$PYTHON code/frontier_verification/dedekind_local_noise_audit.py --directory "$AUDIT" --prior docs/frontier/2026-09-13-quadratic-delta --output "$AUDIT/Local_Audit.json"
$PYTHON code/frontier_verification/verify_local_noise_delta.py
```

Measurements selected for the declared noise, linked nonlinear errors and tails, explicit feasible or separating witnesses, and the missing square-power observations remain active next steps. The wider ACS research queue retains its other gates and makes no global completion or exhaustion claim.
