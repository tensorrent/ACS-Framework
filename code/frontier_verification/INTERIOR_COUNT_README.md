# Equal populations and a sharp interior count gate

The complete metadata class derived in the [classification checkpoint](../../docs/frontier/2026-09-14-aggregate-classification-delta/README.md) contains exactly
`A = Q(sqrt(2), sqrt(-3))` and `B = Q(sqrt(-2), sqrt(-3))`. Both have degree 4, signature (0,2), and absolute discriminant 576. Restricting the inherited complete spectra to height `39/2` gives **22 positive ordinates in each field**, counting multiplicity. Total population no longer distinguishes these fields. An interior count still does, up to the sharp theoretical coordinate-noise threshold.

## Acquisition and inference boundary

Select every positive source ordinate below 19.5 **before** adding noise. Preserve every selected entry and its multiplicity, allow an arbitrary permutation, and independently perturb each coordinate by at most `r`. Retain all selected entries even if a perturbed coordinate leaves the source window. The measured statistic is the number of retained observed coordinates **strictly below** a specified height `H`; it does not additionally filter on positivity. This contract differs from post-noise window censoring and from a feature-only release.

The four anonymous JSON payloads contain only degree, discriminant, signature, rational cutoff, and unlabelled root intervals. Parent filenames, original population sizes, field identities, hashes and cutoff partitions remain in separate provenance. These are known synthetic examples, not a blind experiment. The selector receives only count, height, radius, and the explicit contract; templates are derived from the complete metadata class and the separately certified quadratic-factor spectra. No filename or parent population enters selection. Declared completeness cannot authenticate itself; the supplied examples have inherited finite completeness certificates and new cutoff membership checks.

The new cutoff is a rational string `39/2`. No old integer-cutoff consumer or Gaussian tail/moment budget is silently reused. Source restriction removes A's last recorded entry from the benchmark definition; no entry is deleted from the resulting 22-entry populations during observation.

## General finite-list theorem

Let `a_0 <= ... <= a_(n-1)` and `b_0 <= ... <= b_(n-1)` be sorted real lists, with multiplicities. Set

`D = max_i |a_i - b_i| / 2`.

If `D > 0`, choose an index `k` attaining it and exchange the two names if necessary so `a_k > b_k`. Let `h_* = (a_k+b_k)/2`.

For `0 <= r < D`, every perturbed A entry originating at index `i >= k` satisfies

`y_i >= a_i-r >= a_k-r > h_*`.

Consequently the cumulative A count below `h_*` is at most `k`. Every perturbed B entry originating at index `i <= k` satisfies

`z_i <= b_i+r <= b_k+r < h_*`,

so its count is at least `k+1`. Permuting observations does not change either count. Thus the two full observation sets are disjoint below `D`, and a **single suitably chosen cumulative count** already separates them. This lower-bound proof does not require a decoder to recover an ordered matching.

At `r=D`, the common list `((a_i+b_i)/2)_i` is within radius `D` of both source lists. It is an actual common observation, so no statistic of the full list can distinguish the two sources uniformly there. This proves the exact full-list ambiguity threshold and the sharp threshold of an optimally placed count statistic simultaneously. If `D=0`, the source multisets already coincide. These statements concern a known binary class, equal finite population, independent absolute errors and preserved entries; they do not assert a universal one-count decoder for larger classes or other noise models.

The [canonical Lean source](proofs/InteriorCount_v3.lean) checks eight constituent lemmas: two scalar midpoint inequalities, their interval-gate forms, prefix/suffix filter bounds, strict count separation and permutation invariance. The written argument connects sorted source ranks and noise hypotheses to those lemmas. The entire source arithmetic, zero certificates and general matching theory are not claimed as a single fully formalized Lean theorem. Exhaustive small tests cover 1,741 equal-length multiset pairs, 32,016 literal indexed permutations, and 1,672 positive-gap count gates, including repeated and negative coordinates.

## Application to the actual fields

Write `a_i,b_i` for the 22 true source ordinates in the new prefixes, using zero-based indices. Independent exact inequalities show that the second-root pair (`i=1`) uniquely dominates every other ordered pair. Therefore

`delta_* = (a_1-b_1)/2`, approximately `0.5732773345123776`.

The numerical enclosure has width **2e-30**; the exact symbolic identity does not collapse that interval. With certified root intervals `[Alo,Ahi]` and `[Blo,Bhi]` for this pair, define

`L = (Alo-Bhi)/2`, `U = (Ahi-Blo)/2`, `H = (Alo+Bhi)/2`.

For every `0 <= r < L`, the rational height `H` separates count at most 1 for A from count at least 2 for B. The fixed rational height is not asserted equal to the theoretical true-root midpoint `h_*`. Its critical-rank margin is

`min(a_1-H,H-b_1) = delta_* - |H-h_*|`.

This is a strict-radius guarantee; endpoint behavior also depends on the strict count convention. More precise certified intervals could support a closer rational gate. Both nominal 160/224 inputs are retained, and their labels alone do not establish improved precision.

At `L`, the **closed-box count envelopes** overlap. This expresses uncertainty allowed by the interval certificate; it is not evidence that the actual fields share an observation at `L`. For each root pair, the midpoint of its union hull yields a fixed rational observed coordinate. Every endpoint of both source boxes lies within radius `U` of that point, proving uniform realizability for the true ordinates. All 22 coordinates are present. The critical union-hull midpoint equals `H` because the two critical boxes have equal width. Its strict count is 1; changing `<` to `<=` changes this count to 2. Both fields produce the same full observation at `U`.

The complete metadata class has only these two fields. A unique count selection therefore fixes all 604 tracked prime-power Euler coefficients through 4096. At the common observation, 456 coefficient values agree and remain fixed; 148 are ambiguous, including targets 3, 7, 19, 27, and 31. Fresh local polynomial factorization verifies both 604-value vectors, using 1,128 factorizations away from each chosen order index. These are exact domains within this fully classified finite metadata class, not an infinite-spectrum result.

An independent augmenting-path matching search uses every one of the 22 by 22 possible pair costs. It rejects a perfect matching just below `L` for the lower cost matrix and just below `U` for the uniform-witness cost matrix, and accepts at the respective boundaries. This is distinct from assuming an ordered matching. Eight boundary searches examine 1,936 pair-cost entries across two precisions and two cost models. There are 176 common-witness endpoint checks and 42 strict noncritical-pair comparisons.

## Cutoff stability and adversarial controls

Every cutoff strictly between `max(A_21_hi,B_21_hi)` and `A_22_lo` selects the identical two 22-entry prefixes. The rational bounds are approximately 19.086441660064803 and 19.724015324441552. Exact endpoint inequalities prove this continuum statement; nine interior cutoffs per precision supply additional checks. The endpoints themselves are not asserted certified cutoffs. The count theorem transfers because the finite source lists are unchanged. Post-noise censoring and Gaussian budgets require separate work.

Thirty-two main semantic mutations reject missing/extra/repeated roots, provenance leakage, mismatched contracts, invalid scalar types, wrong counts, false coefficient predictions, truncated witnesses and a false actual-ambiguity claim at `L`. Four additional mutations reject overextended cutoff bounds and false membership claims. Radii `L-10^-100` and `L+10^-100` have the same binary64 representation but different exact closed-box count outcomes, demonstrating why the boundary audit retains rational arithmetic.

Two failed Lean sources and their logs are preserved. The first imported a nonexistent `Mathlib.Tactic.Omega` module; the second used reserved keyword `prefix` as a variable name. The separately versioned third source uses the installed Lean Omega module and a valid name, and compiles with no `sorryAx`. No earlier numerical or theorem source was overwritten.

## Reproduce and continue

The [dated evidence package](../../docs/frontier/2026-09-14-aggregate-equal-population-delta/README.md) includes the input archive, full provenance, decoder, independent audit, adversaries, cutoff certificate, all three Lean attempts, compiled successful artifact, runtime, source snapshot, receipts, manifest and append-only research ledger. Run the canonical verifier from the repository root with the pinned environment:

```sh
../acs-research/.venv/bin/python code/frontier_verification/verify_aggregate_equal_population_delta.py
```

It regenerates the four inputs, repeats all new scientific computations and Lean compilation, verifies immutable receipts/archives/history, then recursively verifies the preceding checkpoints. The broader 117-branch ACS program remains active. A next observation contract can release a finite Gaussian feature vector only; it must define its actual source perturbations, errors and any tail terms explicitly. A numerical small residual would be a proposal, not an existence certificate. Natural operators, infinite arithmetic/real-part information, topology, physical interpretations, fuller formalization and private-input gates also remain open.
