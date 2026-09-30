# Source constraints sharpen the local noise bracket

The [source-strip certificate](../../docs/frontier/2026-09-14-aggregate-source-constrained-delta/Source_Strip_Certificate.json) strengthens the strict uniform identification guarantee to approximately **1.8196470598929473e-10**. The [mixed observation certificate](../../docs/frontier/2026-09-14-aggregate-source-constrained-delta/Mixed_Noise_Certificate.json) constructs two exact ambiguous pairs; the strongest noise upper endpoint is approximately **1.8313917311990002e-10**. The ratio is approximately **1.0064543677534608**, leaving a gap of about **0.65%**. Exact rational endpoints govern every claim. The source-feasible threshold remains open.

The [independent audit](../../docs/frontier/2026-09-14-aggregate-source-constrained-delta/Independent_Source_Constrained_Audit.json) uses real-polynomial Cramer calculations for the lower bound and complex scalar derivatives for the upper constructions. The [preceding proof](SIGNED_CORNER_README.md) establishes the uniform secant matrix-family framework inherited here.

## Original contract and source endpoint direction

The complete inherited metadata class consists of two quartic fields with signature (0,2) and absolute discriminant 576. Their complete positive source prefixes below 39/2 have 22 entries each. Selection precedes independent absolute coordinate errors, retaining every entry and multiplicity. Let r=U-1e-8<L, where [L,U] is the inherited critical source half-separation enclosure and U-L=2e-30. Observations remain in the same radius-1/100 standard coordinate cube about the rational center c. The ordered 22 finite additive features and their absolute component-error units are unchanged; there are no raw roots, counts, infinite moments or unknown tails in the release.

Indices are zero based. Coordinate1 separates the sources. If the unknown source root lies in [slo,shi] and |observed-root|<=r, then necessarily

    slo-r <= observed <= shi+r.

For a construction to satisfy the error budget for every root in its certified interval, the sufficient condition is instead

    shi-r <= observed <= slo+r.

These endpoints have different purposes. The lower proof uses necessary outer bounds, while the upper construction uses the stronger sufficient inner bounds. Both implications are compiled in Lean. They cannot be interchanged merely because source interval widths are small.

## Critical-strip bootstrap

Write Kold for checkpoint31's exact uniform critical inverse bound, approximately 55.5210906442615. Fix T to checkpoint30's exact certified actual ambiguity upper endpoint, approximately 1.831989439894397e-10. T is an inherited budget cap, not a newly guessed threshold.

Suppose two different-source observations A,B share a report z with ||Phi(A)-z||_infinity and ||Phi(B)-z||_infinity at most tau, and tau<=T. Relabel the pair according to its source class if needed. The common-report triangle inequality and the inherited uniform secant bound imply

    0 < A1-B1 <= Kold*||Phi(A)-Phi(B)||_infinity
                <= 2*Kold*tau <= Dcap := 2*Kold*T.

From the 224-bit source enclosures define a=source_A_lo-r and b=source_B_hi+r. The exact source geometry gives a-b=2(L-r)>0. Necessarily A1>=a and B1<=b, so

    A1 in [a,b+Dcap],      B1 in [a-Dcap,b].

Every critical coordinate along the segment from B to A therefore lies in I*=[a-Dcap,b+Dcap]. Its half-width is approximately 1.0342810350341335e-8, strictly inside the original radius .01 interval. All other coordinate intervals remain the original ones.

The 22 scalar kernels are smooth and Phi is additive across coordinates. Each finite difference is M(A-B), where each column of M is the integral of its derivative curve along the corresponding coordinate segment. Those columns lie in the closed convex hulls of the derivative curves. The critical column now lies in the hull for I*. The resulting product family H* is a subset of checkpoint31's full nonsingular convex column family H; this is a restriction deduced for candidate common-report pairs, not a changed user observation contract.

## Restricted-family corner proof

Every weighted-defect, critical inverse-row sign, uniform curvature sign and 21 resolved inverse-direction sign established on H remains valid on H*. Coordinate1 has positive endpoint direction, so replace it by g'(upper(I*)) instead of the previous radius .01 upper endpoint. Apply the same nondecreasing finite column replacements to the other 20 globally resolved coordinates. Each replacement stays within H*.

After these 21 replacements only column12 is free. At the reference with column12=g'(c12), interval inversion at 1024/1536 bits proves (M^-1 v)_12<0. The independent audit verifies this with real-polynomial Cramer numerator/denominator ratios at 896/1152 bits. Cramer's numerator is independent of column12 on this face and the determinant retains its nonzero sign. Therefore the negative direction holds across the whole face. The inherited negative curvature factor selects its lower endpoint.

The resulting corner bounds the critical inverse-row norm throughout H*, by the finite inverse-difference and closed-hull endpoint argument proved in checkpoint31. The new corner norm is at most an exact100-bit dyadic rational K*, approximately 54.955712129078016. Every row sign agrees with the inherited v. Independent real Cramer ratios verify all 22 critical inverse-row entries and the same upper bound. This yields

    |A1-B1| <= K* ||Phi(A)-Phi(B)||_infinity

for candidate common-report pairs with tau<=T. It does not claim that every arbitrary pair in the original cube has its critical roots in I* or satisfies this stronger secant bound.

Let G=(L-r)/K*, approximately 1.8196470598929473e-10. Exact arithmetic verifies the old strict guarantee < G < T. If a common report existed at tau<G, then tau<T supplies the budget hypothesis used to derive H*. Source separation and the conditional secant estimate would give 2(L-r)<=2*K* tau, contradicting tau<G. Thus the improved strict identification guarantee applies under the **original** cube and error contract. This noncircular implication is compiled as a generic Lean lemma. Equality at G and sharpness over source-feasible pairs remain unsettled.

## Mixed A/B upper constructions

A naive construction fixed all B coordinates near the selected corner and solved21A roots plus noise. Its numerical equations and source-center checks passed, but the resulting A left the cube by about 0.000287–0.000288. The failed original search and a separate diagnostic preserving all three region violations are archived. These trials are rejected and do not establish an ambiguity endpoint or an impossibility theorem.

The successful construction fixes one observation per noncritical coordinate and solves the other. For each coordinate j!=1, the report specifies whether A_j or B_j is free. The opposite observation is pinned to its selected cube endpoint with an interior margin. This choice is part of the proposal, not an assumption that all A coordinates are free. Two cases use margins1e-6 and1e-10.

Both critical coordinates are fixed as A1=c1+epsilon and B1=c1-epsilon, with epsilon=1e-8+1e-24. The root-error radius r is unchanged. The smaller safety increment is explicit and checked against every source interval; no correction-box uncertainty is assigned to these fixed coordinates.

The unknown vector contains the 21 actual free root coordinates and alpha=tau/s, where s=1e-10. Define

    F(w)=Phi(A(w))-Phi(B(w))-2*s*alpha*v.

Each free A coordinate has Jacobian column +g'(A_j); each free B coordinate has column -g'(B_j). The noise column is exactly -2*s*v and has zero derivative variation. The [primary derivative documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/Calculus/Deriv/Add.html) supplies the subtraction rules used in the compiled mixed-kernel derivative lemma. Pinned local sources are archived separately from current documentation.

Newton proposals at220 decimal digits are exported to170 significant digits. Exact rational centers and preconditioners are then used in a variable cube of radius rho=1e-120. Radius rho belongs to each chosen free A or B root and alpha; all other observation coordinates are singletons. The noise interval is s*[alpha-rho,alpha+rho], so its radius is s*rho=1e-130.

For the real interval Jacobian J(w), the primary checker bounds E=I-RJ throughout this cube. For every row i it proves q_i=sum_j |E_ij|<1 and |(R F(center))_i|+rho*q_i<rho. The map w -> w-RF(w) is therefore a strict contraction mapping the closed cube into itself. Its exact fixed point exists; nonsingular R, checked by a determinant enclosure and independently modulo65537, implies F(w)=0 there. This provides actual mixed A/B observation pairs, not just small numerical residuals.

The independent complex route rebuilds signed center Jacobians and absolute second-derivative variation by scalar sums at 896/1152 bits. The primary interval matrix route uses768/1024 bits. Both prove contraction and self-mapping. Direct source inequalities require each observed box [lo,hi] to lie inside [source_hi-r,source_lo+r], for each A/B field, each coordinate and both 160/224-bit source files. All 352 scalar inequalities pass across the two cases. The boxes also preserve positivity, ordering and strict membership in the original coordinate cube.

At each exact solution Phi(A)-Phi(B)=2*tau*v, with tau>0 and every v component equal to +/-1. The common release (Phi(A)+Phi(B))/2 has absolute feature error exactly tau from either observation, by the inherited midpoint lemmas. The two exact upper endpoints are approximately 1.8314064434518525e-10 and1.8313917311990002e-10. Their midpoint reports are certifiably different from Phi(c). Their exact critical gap exceeds2(L-r), as required.

## Audits, provenance and remaining questions

The independent audit repeats 1128 polynomial factorizations and 1208 coefficient comparisons. Under the complete inherited two-field class, identification below G fixes the tracked 604-column vector. At either new common report456 coefficient domains are fixed and 148 ambiguous. This is not full infinite arithmetic recovery or an arbitrary-report decoder.

Seven new Lean lemmas establish necessary and sufficient source-error bounds, critical strip endpoints, segment containment, the common-budget difference cap, noncircular subthreshold exclusion and the actual mixed-kernel derivative sign. Inherited matrix, contraction and midpoint results retain their original scopes. The whole concrete analytic and spectral/arithmetic assembly remains partly written or computational. Independent numerical routes share FLINT and inherited source premises.

Forty-six premise mutations and five exact controls test source endpoint direction, conditional scope, mixed A/B assignment, derivative signs, scales and serialized evidence. The written proof audit is by the implementing investigator, not a separate agent or human review.

One exploratory diagnostic receipt has an empty automatic source-hash map because the original runner resolved relative arguments against its own launch directory instead of the child cwd. The actual receipt is retained unchanged. Its report records the exact source hash; the source snapshot preserves that version, and the full verifier replays it byte for byte. This limitation is explicit rather than retroactively rewriting the receipt.

Run `code/frontier_verification/verify_aggregate_source_constrained_delta.py` with the repository's pinned Python runtime. It replays all six original scripts, including the failed naive search, regenerates the canonical certificates and independent/adversarial audits, recompiles Lean, checks hashes/receipts/ledger history, and recursively verifies checkpoint31 and its preceding chain. No new runtime package or source roots were acquired.

Next: tighten the remaining source-feasible gap, validate useful parameter families, implement bounded-error inverse sets for arbitrary reports, test larger/global domains and formalize the remaining analytic bridges. All 117 ACS branches, natural operator/infinite arithmetic/real-part/topology questions and private-input gates remain active. No global completion or exhaustion is claimed.
