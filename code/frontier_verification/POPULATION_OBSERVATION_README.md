# Population information and a missing-root ambiguity threshold

The [preceding classification](../../docs/frontier/2026-09-14-aggregate-classification-delta/README.md) derives exactly two fields from degree four, signature (0,2) and absolute field discriminant 576. Their certified positive-root populations through height 20 have sizes 23 and 22. This continuation compares preserved populations, one missing root, and window selection after coordinate error.

Under the preserved-population contract, list length identifies the field regardless of coordinate-error magnitude. Under a different contract allowing at most one missing root from each source, a common observation becomes possible. Its exact threshold is half the difference between the fields' second positive ordinates, approximately 0.5732773345123776. The same threshold applies to coordinate noise followed by complete observation of the open window (0,20), with no arbitrary deletion allowance. Rational certificates enclose the value in an interval of width 2e-30. At the certified upper endpoint, explicit lists of 22 rational ordinates are compatible with both actual fields and leave 148 of the 604 tracked coefficients ambiguous.

The [evidence package](../../docs/frontier/2026-09-14-aggregate-cardinality-delta/README.md) preserves the inputs, exact bounds, witnesses, independent checks, failures and continuation gates. These are finite observation results under the contracts below, not claims of equal Dedekind zeta functions or ambiguity of infinite spectra.

## What the preserved population reveals

Let a source list consist of every positive ordinate through T=20, counting multiplicities. Coordinate errors may move its entries and a permutation may reorder them, but no entry is inserted or removed. The observed list has exactly the source length. In the complete metadata class, length 23 selects A=Q(sqrt(2),sqrt(-3)) and length 22 selects B=Q(sqrt(-2),sqrt(-3)). This conclusion does not depend on individual coordinate values or an error radius.

The selector accepts only a population size and an explicit contract: the source population is complete through 20, selected before coordinate error, with zero insertions and deletions. Candidate counts are rebuilt from the three class-derived quadratic factors and zeta. A separate audit counts held-out aggregate lists, verifies their source identity and checks the selected arithmetic by polynomial factorization.

Seventy-two coordinate transformations cover two source populations, two nominal precision inputs, six radii and three shift/reordering patterns. Four additional controls move every source ordinate to 10. Since all true source ordinates lie in (0,20), radius 10 permits this collapse. Each observed coordinate value is now identical, but the lists retain different lengths and still select different fields. The general cardinality result is proved by a Lean list lemma; these finite transformations are controls rather than its proof.

This exposes an information advantage of the complete-class decoder. Earlier Gaussian certificates remain valid for their declared deduction method and uncertainty bounds. They do not establish optimal information limits for a decoder that can use the derived field class and the population count. The cardinality argument itself does not enlarge an explicit-formula certificate or justify post-noise cutoff censoring.

Completeness and preservation must come from external evidence. Contract flags do not authenticate themselves. Deleting one A root and falsely declaring the remaining 22 entries complete and preserved makes the scalar selector choose B. Two such false-premise counterexamples are preserved and independently checked. No count-only procedure can diagnose that forged premise from its scalar input alone. The synthetic source populations used here inherit verified completeness and provenance.

## A different contract: one root may be missing

Now allow at most one deletion from each complete source population through 20, no insertions, and independent absolute error at most delta on every retained ordinate. The source population is selected before deletion and coordinate error. No additional roots enter after crossing a measured cutoff. Reordering is allowed and multiplicities remain entries.

If a common observation has m entries, the deletion budgets require

    0 <= 23-m <= 1,    0 <= 22-m <= 1.

Thus m=22: A loses exactly one entry and B loses none. This is a change in the observation model. It is not a missing qualification silently added to the original preserved-population results.

Let a_0<...<a_22 and b_0<...<b_21 be the actual certified source ordinates. After deleting A index j, let a_i^(j) denote the remaining sorted list. For fixed j, the least common-observation radius is

    delta_j = (1/2) max_i |a_i^(j) - b_i|.

The global threshold is delta_* = min_j delta_j. Two steps justify this formula for arbitrary matching and arbitrary observed coordinates.

First, ordered matching minimizes the maximum paired distance on the real line. Suppose a<=a' and b<=b', and crossed pairs satisfy |a-b'|<=R and |a'-b|<=R. The upper bound a-b<=a'-b<=R and lower bound b-a<=b'-a<=R give |a-b|<=R. The same argument gives |a'-b'|<=R. In any permutation with an inversion, exchange the inverted matched values; the bound cannot increase. Repeatedly removing adjacent inversions terminates because the finite inversion count decreases. The resulting order-preserving matching is therefore at least as good. This remains valid with repeated values. The real inequality used in each exchange is Lean-checked; the complete finite inversion-removal argument is written here rather than formalized as an algorithm theorem.

Second, if two source values both lie within delta of one observed value, their distance is at most 2*delta by the triangle inequality. Conversely, their midpoint lies within half their distance of each. Applying this to every ordered pair proves the fixed-j formula; checking all 23 deleted indices proves the global formula. Sorting a common observation and composing its two source correspondences gives a matching between retained source lists, so no unordered observation can evade the lower bound.

## Certified bounds and an actual common observation

For source intervals A_i=[a_lo,a_hi] and B_i=[b_lo,b_hi], define

    lower_i = max(0, a_lo-b_hi, b_lo-a_hi) / 2,
    upper_i = (max(a_hi,b_hi)-min(a_lo,b_lo)) / 2.

The first quantity bounds half the actual source separation from below. The second is a uniform common-point radius: the midpoint of the union hull is within upper_i of every value in both intervals. Taking the maximum over pairs and then the minimum over deletions gives L<=delta_*<=U. This upper construction uses rational interval endpoints, so its recorded common observation works for every choice of actual root values in the certified boxes.

The common ordinate chosen for each pair is

    y_i = (min(a_lo,b_lo)+max(a_hi,b_hi)) / 2.

Both endpoint sequences are strictly increasing; their componentwise minima and maxima also increase strictly. Hence the recorded y_i form a strictly increasing 22-entry list inside (0,20). Every endpoint inclusion is checked, and the interval-center lemma is Lean-checked. The first recorded witness deletes zero-based A index 17, its eighteenth root.

An independent minimax dynamic program uses states (i,j,d_A,d_B): consumed prefixes, with each deletion count at most one. A match advances both prefixes and takes the maximum of the current cost and the new pair cost; a deletion advances one prefix without adding a coordinate cost. Minimize over predecessor states. Prefix length increases at every transition, so induction over i+j proves the recurrence computes the least bottleneck cost for each state. The only terminal deletion counts are (1,0). Separate boolean reachability checks feasibility at each exact bound and infeasibility just below it. This checks all ordered partial matchings without selecting a deleted index in advance.

The audit visits 90 states for each lower/upper matrix at each nominal precision, replays 1,012 stored pair rows, checks 176 source-interval endpoint inclusions and performs eight exact threshold-boundary tests. A further cross-check exhausts 41,796 arbitrary indexed matchings for 543 small sorted-multiset problems, including duplicate and negative coordinates. This finite exhaustion supplements the general uncrossing proof.

## The exact threshold is a particular root gap

The critical-gap audit proves more than L<=delta_*<=U. For each of the six deleted A indices 17 through 22, the second A root remains paired with the second B root, and its A interval lies strictly above its B interval. Every other pair has a uniform upper radius strictly below the critical pair's lower radius. For each of the other seventeen deletions, a certified lower bound is strictly above the critical pair's upper radius.

These strict inequalities hold for every actual source root choice in the certified intervals. Therefore the six listed deletions have exactly the same actual bottleneck, and every other deletion is strictly worse:

    delta_* = (a_1 - b_1) / 2.

The source intervals and doubled rational inequalities independently certify 286 strict comparisons across the two nominal precisions. Midpoints of the actual paired roots give a common observation at this exact symbolic threshold. The stored rational observation is a uniform witness at U. The exact symbolic identity does not replace the ordinates with exact numerical constants: their numerical enclosure still has width 2e-30. Both precision inputs give the same critical interval bounds, so the precision label alone must not be treated as a narrower uncertainty bound.

Below L, no common observation exists under this one-deletion model; at U and every larger radius, the stored observation is compatible with both actual fields. The complete metadata class has only those two fields. Consequently its exact coefficient domains at this observation are the two fields' coefficient values: 456 remain fixed and 148 are ambiguous, including target indices 3,7,19,27,31. This is actual field realization of the finite ambiguity, with independently checked arithmetic, rather than feasibility of a necessary coefficient relaxation.

## Coordinate noise followed by window selection

Consider all positive nontrivial zero ordinates, with multiplicities. Every entry receives an independent displacement of absolute size at most delta>=0, and the observer records every transformed entry lying in the open window (0,20). There are no arbitrary insertions or deletions. This is an ideal complete window-observation model, not an assertion that a physical detector meets those assumptions.

The first two source roots of both fields have certified margins from zero and from height 20 exceeding U. They therefore stay inside the window under every allowed error of radius at most U. Any further retained source root has a larger original ordinate, even if it entered from above 20. Thus the first two ranks of each retained source list are fixed. If the two windowed observations were identical at delta<delta_*, their source correspondences would give a matching at pair distance at most 2*delta. Uncrossing would then force the second source roots to be that close, contradicting their gap. Unknown tail entries cannot change those first two retained source ranks, so this lower bound does not require enumerating the tail.

For the upper construction, pair A's first 22 source roots with B's 22 recorded roots, using their actual midpoints. Deleting zero-based A index 22 was one of the six optimal finite matchings, so these pair errors are at most delta_* and their midpoints lie inside the window. The last recorded A root is sufficiently close to 20 to move outside it within a strictly smaller error. If a_lo is that root's certified lower endpoint, set

    eta = (L - (20-a_lo)) / 2 > 0,
    transformed_last_A_root = 20 + eta.

This exit point is outside the window and its error for every allowed true value of the root is strictly below L. Leave every originally unrecorded positive ordinate unchanged. Inherited completeness through 20 puts each such entry at or above 20, so it stays outside the open window. This defines a complete noise map on both source families: all their entries remain, one recorded A entry exits the displayed window, and the two visible lists have 22 identical entries. No new zeros need to be computed for this construction or the protected-prefix lower bound.

The rational union-hull midpoints for A deletion index 22 give the recorded uniform window witness at U. The actual-root midpoints prove existence at the exact symbolic threshold. The window audit checks 198 exact inequalities, verifies the protected prefixes, bounds the exit error and covers the unchanged tail. Three additional Lean lemmas prove the local window protection, uniform exit and unchanged-tail exclusion steps. The full retained-rank and matching argument remains the written proof above.

The window JSON's source-population sizes 23/22 refer to the tracked entries originally through height 20; those entries still exist after noise. Its visible population is 22/22. It does not assert that the full source families contain only 23 or 22 roots. The complete metadata class still has two fields, so both common-observation constructions have the same 456 fixed and 148 ambiguous coefficient domains.

## Checks, failures and remaining scope

Eight elementary Lean lemmas cover preserved length, unequal-population disjointness, uncrossing, the two-source triangle bound, interval centers and the three window steps. Portable checkers compile both modules. The full number-theoretic classification, source zero certificates, inversion-removal proof, dynamic-program correctness and retained-rank argument are not claimed as complete Lean formalizations.

Twenty-five semantic mutations challenge contract stages, completeness declarations, insertion/deletion budgets, integer types, leaked coordinates, multiplicity loss, candidate coverage, arithmetic values, matching indices, interval endpoints, incomplete witnesses and false threshold claims. Four further mutations challenge the critical pair, optimal deletions, strict margins and unresolved numerical width; five challenge window exits, protected prefixes, tail handling and visible counts. A literal zip-only endpoint loop accepts a shortened 21-entry witness even though it would require two deletions from A; the complete auditor rejects it. This preserves a concrete false acceptance and its missing population check.

Two development failures remain intact. An early audit incorrectly required the exported threshold interval to be narrower than 1e-30; the exact width is 2e-30, so a separate version reports that width. An initial Lean driver omitted the package-root option needed for an external source file; a separate driver adds the documented option. Neither correction changes the numerical proposal or theorem source. Thirteen recorded scientific/development commands comprise eleven successes and two preserved failures; packaging and final recursive verification are separate.

Run the inherited pinned environment with:

    python code/frontier_verification/verify_aggregate_cardinality_delta.py

The verifier freshly replays the decoder, exact matching, independent arithmetic and dynamic program, adversarial controls, critical-gap and window proof components, and both Lean compilations, then verifies the preceding checkpoint chain. It also checks source snapshots, receipts, inherited inputs and append-only history.

Next, examine other edit budgets, source cutoffs and error norms, construct equal-population benchmarks where cardinality does not identify the field, and extend formalization. The window result relies on complete observation and bounded independent coordinate errors; other acquisition processes need their own contracts. Natural operators, infinite arithmetic, topology, physical interpretation and private-input questions remain active. No global completion or exhaustion is claimed.
