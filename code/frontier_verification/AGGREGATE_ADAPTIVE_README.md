# Adaptive multipliers under validated coefficient domains

This continuation recovers all seventeen target coefficients for both aggregate spectra at tested ordinate radii 0, 0.005 and 0.02, under either generic local profile. At radius 0.1 it recovers 14/11 targets with degree-only local rules and 15/11 with discriminant ramification. The preceding frozen-vector feedback reached 11/10 and 13/10 respectively at radius 0.1. No new zeros, measurements, field templates, Galois-group information or arithmetic seeds are supplied to inference.

The [checkpoint package](../../docs/frontier/2026-09-13-aggregate-adaptive-delta/README.md) retains all domains, rounds, rational multipliers, continuum leaves, independent audits, failures from earlier checkpoints, and exact continuation gates. These are sufficient recovery certificates for a fixed benchmark and input contract. They do not establish an optimal noise radius, realizability of surviving coefficient assignments, or exhaustion of the broader ACS program.

## Adaptive objective and dependency order

Use the same 34 signed inequalities from seventeen Gaussian measurements, with nominal matrix A and right-hand side b. For a signed target s*c_j and nonnegative rational multiplier vector lambda, let r = s*e_j - A^T*lambda. If earlier valid deductions give coefficient domains D_k, then

    s*c_j <= b^T*lambda + sum_k max_{v in D_k}(r_k*v) + E(lambda).

E(lambda) is the newly certified shared finite-root/known-moment budget, including the unconditional unknown-zero remainder and the existing prime remainder in b. The [preceding derivation](AGGREGATE_MOMENT_README.md) gives the joint root function J = -2H - kappa*m, with m(t)=12/(9+4t^2), and the explicit minimum of independently valid separated and joint budgets.

For l_k=min D_k and u_k=max D_k, the exact support identity is

    max_{v in D_k}(r_k*v) = l_k*r_k + (u_k-l_k)*max(r_k,0).

It holds even when the integer domain has holes. Floating LP variables z_k >= max(r_k,0) therefore have cost u_k-l_k. The lambda cost becomes b-A*l plus the baseline moment-tail contribution; s*l_j is a constant added to the reported sampled score. Root increments are sampled at 33 positions only to propose lambda. Neither LP solver status nor its sampled score proves a continuum bound or optimum.

The loop starts separately from each of sixteen previously validated states: two observations, four radii, and two local profiles. Within a round it first applies generic local projection, then freezes that round's domains. It proposes both signs for each unresolved target, rationalizes multipliers on the 1e-9 grid, and recomputes a complete 224-bit, 48-leaf real first-derivative certificate for every vector. Producer exclusions use those fixed premise domains and a 256-bit interval residual support. Exclusions are applied together, then feed the next local round. Premise hashes, case/profile/radius identities and ordered certificate indices prevent a later result from becoming its own premise. The finite stopping test means this sampled update makes no further deduction.

There are 288 proposed and validated vectors across all rounds. Every LP reports success; all scientific source versions were frozen before their recorded executions. The adaptive producer reads the preceding audit's validation status and fingerprint, but no held-out arithmetic vector. Formal noninterference and a blinded experiment are not claimed.

## Independent replay and stronger audit deductions

The independent audit reconstructs every changed H and kappa. It checks 80,976 stored midpoint values/derivatives, then builds 161,952 fresh complex quadratic interval leaves at 384 bits. Rational monotonic moment endpoints above t=3/2 avoid an interval dependency in the rational part. Integer rows and exact Fraction supports replay 288 domain objectives, 109 dual exclusions and 87 consequent local exclusions. Independent degree-partition enumeration checks local model retention. All 604 held-out true coefficients remain after every round. The two transcendental interval routes share FLINT; 356 separate 85-digit mpmath displaced controls are samples, not completeness proofs.

Eight stronger audit findings refer to one value in four rounds under two profiles: candidate 2 for B's coefficient at 31, radius 0.1. A supplemental exact closure consumes the validated budgets and all previously generated vectors. It removes that candidate once per profile, with a fresh 256-bit interval support cross-check for each exclusion. Local projection makes no further removals and the singleton counts do not change. This closure reuses the existing vectors; it does not re-optimize after the stronger audit domain.

Final degree/discriminant target counts at radii 0, 0.005, 0.02 and 0.1 are respectively 17/17, 17/17, 17/17 and 15/11 for A/B. The degree-only counts agree at the first three radii and are 14/11 at radius 0.1. Counts and complete support domains are in the machine-readable summary and closure.

At radius 0.1 under the stronger profile, A retains c29 in {0,1,2} and c31 in {1,2,4}. B retains c17 in {0,1}, c19 in {2,4}, c23 in {0,1,2}, c25 in {0,4}, c29 in {0,1}, and c31 in {0,1}. These sets encode what this deduction method has not ruled out. They are not constructed field alternatives.

The earlier exact-input full-row closure already recovered 17/17 targets and more support coefficients in some profiles. That older result remains intact. The new advance is full recovery at the positive tested radius 0.02 and stronger recovery at 0.1, rather than an improvement in every support-domain statistic at zero noise.

## Adversarial checks and a stale-budget witness

Ten component mutations challenge borrowed zero-radius seeds, future domains used as earlier premises, mismatched budget/vector identities, reversed objectives, negative multipliers, incomplete interval covers, multipliers changed after certification, invalid coefficient removal, omitted local models, and the wrong support endpoint for a negative residual. All 604 actual residual coordinates also satisfy the general-domain support formula by direct enumeration.

A separate concrete diagnostic starts with an A, radius 0.005, positive c23 vector. Choose each exact root center plus or minus that radius and multiply the vector by nine. Fresh complex interval evaluation proves that its finite-sum change exceeds the unscaled old total budget by more than 0.383. Multiplying the old valid budget by nine restores a sufficient bound in this homogeneous diagnostic. This demonstrates why a new vector cannot inherit an unchanged error budget. It does not claim an unknown-zero tail is saturated or construct another number field.

## Reproduction and remaining gates

The fresh recursive verifier extracts exact inputs from the archived baseline, reruns the adaptive producer, independent audit, supplemental closure and adversary, checks all source/input fingerprints and execution streams, regenerates the summary, and verifies the inherited history. Run with the pinned Python environment from the repository root:

    python code/frontier_verification/verify_aggregate_adaptive_delta.py

The complete earlier runtime and source records remain inherited. No new packages, external downloads, roots, Lean modules or formal analytic proofs are claimed. Four scientific commands succeeded; packaging and the final recursive verifier are separate from those receipts.

Next gates are to re-optimize from the audit-strengthened domains, bracket where all-target recovery stops beyond radius 0.02, compare noisy standalone-row propagation under the same contract, and investigate constructive feasibility or global-field obstructions for survivors. Additional matched-invariant fields and the other ACS branches remain open. Each further pass must retain its assumptions, negative outcomes, source versions and dependency history.
