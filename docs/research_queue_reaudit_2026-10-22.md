# Research-queue re-audit against the 24 September record, 22 October 2026

[Repository home](../README.md) · [Documentation](README.md) · [Queue checkpoint](frontier/2026-09-12-source-delta/README.md) · [24 September record](publication/2026-09-24/README.md) · [Endpoint audit](condensate_energy/endpoint_audit/README.md)

The 12 September queue (`docs/frontier/2026-09-12-source-delta/Research_Queue.json`, 114 branches)
marks 108 branches `carried_forward_not_newly_audited`. Their `current_status` values were copied
from earlier checkpoints, not re-examined. This page sets each of the 108 against the 24 September
record and asks one question: **does that record change the branch?**

The record, for this page, means these files:

- `docs/publication/2026-09-24/amendments.json`: the 33 manuscript amendments.
- `docs/condensate_energy/endpoint_audit/README.md`, `completion-audit.json` and `assessment.json`:
  the endpoint audit.

`Research_Queue.json` is not edited. It is a dated frontier artefact; it is not in the publication
manifest (`grep -c` = 0), but a re-audit belongs in a new page, not in a rewritten checkpoint.

## Labels

- **closed-by-record**: the record states a result that discharges the branch's continuation
  condition, or answers its question, within the branch's own scope.
- **superseded-by-record**: the record states a newer result on the branch's own question that the
  branch text does not carry. The branch's `latest_scoped_result` is stale, but its continuation
  condition is not discharged.
- **still-open-unchanged**: the record leaves the branch's status and continuation condition as they
  were. The label is literal for open statuses. For a branch already at `exact_result`,
  `superseded` and so on, it means "status stands, continuation still open". This class has two
  touch values:
  - `silent`: a topic regex returns 0 hits on the record.
  - `restates`: the record says what the branch already says, sometimes reached by another method.

## Method and checks

- Each row was decided by hand. A read-only checker script then checked every decision. The
  script was run from the session scratch directory and is not committed, but every row can be
  re-checked with `grep -F` (quotes) or `grep -ciE` (regexes) on the named file. It checked:
  - Every quoted record passage must be a verbatim substring of the named record file (whitespace
    collapsed).
  - Every `silent` row's regex must return 0 hits across all four record files.
  - The id set must equal the 108 carried-forward ids exactly.
  - Result: 0 quote failures and 0 regex failures. The first run caught one false `silent` (the
    pattern `Gauss` matched "Gaussian"); the pattern was tightened to `\bGauss\b`.
- A second check used a different method: a content-word overlap scan. For each
  branch (question plus latest result) it found the record sentence sharing the most content words
  of 5 or more letters.
  - At 4 or more shared words, 0 of the 68 `silent` rows are flagged.
  - At 3 shared words, 15 are flagged: A09, I06, F05, C05, D03, K03, S08, S10, F06, N08, P08, S17,
    M07, S23 and NS03. Each was read; every one shares only generic words ("complete", "theorem",
    "scalar", "heavy/light"). For example, A09 matches the colour-singlet withdrawal ("color",
    "triplet"), not generation counting. None was relabelled.

## Counts

| record effect | branches | of which open status¹ |
|---|---|---|
| superseded-by-record | 7 | 3 (S04, S07, M02) |
| still-open-unchanged | 101 | 29 |
|   — touch `restates` | 33 | |
|   — touch `silent` | 68 | |
| closed-by-record | 0 | 0 |
| **total** | **108** | **32** |

¹ The open statuses are `needs_definition` 11, `open_theorem` 8, `needs_data` 6, `open_computation` 5
and `needs_source` 2. That makes 32, the same count the queue itself carries for these statuses.
7 + 101 + 0 = 108, and 33 + 68 = 101.

**What this shows.** The 24 September record closes none of the 108 carried-forward branches.

Seven branch entries are stale, because the record holds newer results on their own questions:

- S02: the neutral-restriction stable/flat/unstable counterfamily.
- S04: higher loops do not supply a selector.
- S06: the λcanonical = 4c₄/Z² identity and the complete-action dilation family.
- S07: finite one-loop matching on a declared stable branch.
- F01: the rank-one square-root texture is not a CKM prediction.
- F02: the second strong-CP failure, [A,A] = 0 does not imply Tr(F∧F) = 0.
- M02: g = 1 for a uniform charge-to-mass ratio, and α⁻¹ = L/2.

For the other 101, the record does not move the inherited status.

**What it does not show.** This page does not re-verify any branch's own evidence. The record is a
condensate and carrier audit plus 33 editorial amendments. It never addresses the information-flow
(I), MHD (M03–M10), Navier–Stokes (NS), nuclear-pole (N05–N09) or most algebra (A) branches, so
`silent` there is expected and is not a check of those results. The 101 statuses are therefore
"unchanged by the record", not "re-confirmed".

Other post-12-September material was not consulted for this table: the two update papers, the
selection-energy audit, and the 22 October cards. A future queue checkpoint should carry the seven
superseded entries forward with the record's text.

## Table

`where` names the record file (amendments by index and target paper). For `silent` rows, the
deciding quote is the branch's own continuation condition, which the record leaves standing.


| id | current_status (12 Sept) | question | record effect | record touch | where | deciding quote |
|---|---|---|---|---|---|---|
| A01 | `exact_result` | Restricted cubic and adjoint exponential | **still-open-unchanged** | silent | record silent: `/minimal polynomial\|adjoint exponential\|X\^3\|TBL adjoint/i` → 0 hits | Branch continuation stands: "A different carrier or generator requires a fresh minimal polynomial." |
| A02 | `exact_obstruction` | Generic BCH truncation from Jacobi | **still-open-unchanged** | silent | record silent: `/BCH\|nested commutator\|nilpoten\|Jacobi/i` → 0 hits | Branch continuation stands: "Specify nilpotency or a restricted operator class before truncating." |
| A03 | `exact_result` | Global sl(n) grading minimization | **still-open-unchanged** | restates | amendments.json[15] (Adjoint_Clifford_Signature_Selection.tex) | "A signature or grading selection within an algebraic construction is distinct from deriving a physical spacetime metric." |
| A04 | `exact_result` | Defining-eigenvalue cluster coherence | **still-open-unchanged** | silent | record silent: `/eigenvalue cluster\|defining-eigenvalue\|defining representation/i` → 0 hits | Branch continuation stands: "Preserve defining-representation clusters in the statement." |
| A05 | `exact_obstruction` | General uniqueness with distinct weights | **still-open-unchanged** | silent | record silent: `/edge weight\|optimal cut\|tied/i` → 0 hits | Branch continuation stands: "Exclude equal sums of cut weights, not merely equal edges." |
| A06 | `exact_result` | Cartan-fixed gradings in other root systems | **still-open-unchanged** | silent | record silent: `/root-lattice\|root system\|sign character\|Cartan-fixed/i` → 0 hits | Branch continuation stands: "Broader involution classes need a separately stated classification." |
| A07 | `exact_obstruction` | Adjoint-eigenvalue cluster interpretation | **still-open-unchanged** | silent | record silent: `/adjoint-eigenvalue\|adjoint eigenvalue\|eigenvalue partition/i` → 0 hits | Branch continuation stands: "Retain the distinction between defining and adjoint eigenvalue partitions." |
| A08 | `exact_result` | Compact quadratic grading selection | **still-open-unchanged** | restates | amendments.json[15] (Adjoint_Clifford_Signature_Selection.tex) | "A signature or grading selection within an algebraic construction is distinct from deriving a physical spacetime metric." |
| A09 | `exact_obstruction` | Three directions imply three generations | **still-open-unchanged** | silent | record silent: `/generation\|family multiplicity\|three famil/i` → 0 hits | Branch continuation stands: "Supply a generation-counting mechanism independent of color dimension." |
| A10 | `exact_obstruction` | Non-symmetric grading domain | **still-open-unchanged** | silent | record silent: `/involution\|non-symmetric\|mixed-signature/i` → 0 hits | Branch continuation stands: "Retain orthogonality/symmetry or formulate a different constrained optimization." |
| I01 | `needs_definition` | BCH displacement to information | **still-open-unchanged** | silent | record silent: `/transfer entropy\|\bTE\b\|information flow\|information balance\|mutual information\|halting\|Lyapunov\|c-function\|Ito \|diffusion\|history/i` → 0 hits | Branch continuation stands: "Specify the complete ACS transition law, source/target observations, lag and conditioning, fixed reference measure and valid smooth perturbation hypotheses. The torus split is not asserted to satisfy every informal ACS condition." |
| I02 | `exact_obstruction` | Universal stochastic bracket-score TE bridge | **still-open-unchanged** | silent | record silent: `/transfer entropy\|\bTE\b\|information flow\|information balance\|mutual information\|halting\|Lyapunov\|c-function\|Ito \|diffusion\|history/i` → 0 hits | Branch continuation stands: "If extra ACS constraints exclude it, prove a bridge under those precise constraints." |
| I03 | `exact_obstruction` | Invariant measure determines information flow | **still-open-unchanged** | silent | record silent: `/transfer entropy\|\bTE\b\|information flow\|information balance\|mutual information\|halting\|Lyapunov\|c-function\|Ito \|diffusion\|history/i` → 0 hits | Branch continuation stands: "Provide the transition kernel and observation history." |
| I04 | `exact_obstruction` | Information balance implies convergence | **still-open-unchanged** | silent | record silent: `/transfer entropy\|\bTE\b\|information flow\|information balance\|mutual information\|halting\|Lyapunov\|c-function\|Ito \|diffusion\|history/i` → 0 hits | Branch continuation stands: "State a Lyapunov, contraction, compactness and invariance argument." |
| I05 | `needs_definition` | A concrete convergent coupled model | **still-open-unchanged** | silent | record silent: `/transfer entropy\|\bTE\b\|information flow\|information balance\|mutual information\|halting\|Lyapunov\|c-function\|Ito \|diffusion\|history/i` → 0 hits | Branch continuation stands: "Derive a complete-space contraction or coercive Lyapunov condition from the actual ACS update map and name the limit and norm." |
| I06 | `superseded` | Delta I equals a c-function | **still-open-unchanged** | silent | record silent: `/transfer entropy\|\bTE\b\|information flow\|information balance\|mutual information\|halting\|Lyapunov\|c-function\|Ito \|diffusion\|history/i` → 0 hits | Branch continuation stands: "A newly defined observable would create a new branch." |
| I07 | `needs_definition` | Full-history information instrument | **still-open-unchanged** | silent | record silent: `/transfer entropy\|\bTE\b\|information flow\|information balance\|mutual information\|halting\|Lyapunov\|c-function\|Ito \|diffusion\|history/i` → 0 hits | Branch continuation stands: "Supply both source/target history sigma-algebras, lag, transition law and observation noise before identifying the ACS observable." |
| I08 | `exact_result` | Noise compatibility with hard constraints | **still-open-unchanged** | silent | record silent: `/transfer entropy\|\bTE\b\|information flow\|information balance\|mutual information\|halting\|Lyapunov\|c-function\|Ito \|diffusion\|history/i` → 0 hits | Branch continuation stands: "Specify whether ACS-3 imposes this constraint and provide its actual diffusion." |
| S01 | `exact_result` | Complete gauge-only scalar invariant basis | **still-open-unchanged** | restates | endpoint_audit/README.md | "68 real scalar coordinates, 17 real quartic coefficients, four quadratic coefficients and the kinetic metric." |
| S02 | `exact_obstruction` | Endpoint vacuum forced by gauge symmetry | **superseded-by-record** | new | endpoint_audit/README.md | "Symmetry alone permits different stable local alignments and both stable/unstable transverse spectra at the same restricted neutral data. A unique physical vacuum is demonstrably underdetermined." + "The action audit also disproves uniqueness from a neutral restriction by a stable/flat/unstable counterfamily." (amendments.json[25] (The_Elimination_Ledger.tex)) |
| S03 | `exact_obstruction` | Gauge protection of the angular flat direction | **still-open-unchanged** | restates | endpoint_audit/README.md | "restores the relevant couplings; the old reduced potential is generally not closed under running." |
| S04 | `open_computation` | Complete coupled scalar and Yukawa RG selection | **superseded-by-record** | new | endpoint_audit/README.md | "Completing all higher-loop terms would be further conditional theory development, not a missing evaluation of the printed proxy or a supplied physical selector." + "A beta function without a boundary condition does not select Λ in physical units." (endpoint_audit/README.md) |
| S05 | `exact_result` | Approximate phase6 fixed-point branches | **still-open-unchanged** | restates | endpoint_audit/README.md | "Exact elimination and Sturm root counts give just two real solutions, both on x₃=x₄=0" |
| S06 | `exact_obstruction` | Gauge and scalar normalization | **superseded-by-record** | new | endpoint_audit/README.md | "The correct radial identity is h=√Z r and λcanonical=4c₄/Z² for the convention V=c₄r⁴=λcanonical h⁴/4. Consistent coordinate changes preserve this result; an undetermined common action prefactor remains physically relevant." + "This is a family of physically different actions, **not** a coordinate symmetry of one action with fixed dimensional inputs." (endpoint_audit/README.md) |
| S07 | `needs_definition` | Gauge one-loop running | **superseded-by-record** | new | endpoint_audit/README.md | "The latter includes mixed heavy/light effects, light-field subtraction, finite kinetic normalization and independent 80-digit limits. It assumes a particular light doublet, portal structure and real diagonal flavor." + "No unique global physical vacuum is asserted" (endpoint_audit/completion-audit.json) |
| S08 | `exact_result` | CP and phase invariant subspaces | **still-open-unchanged** | silent | record silent: `/CP action\|invariant subspace\|holomorphic\|current coupling\|13 quartics\|independent .{0,20}phases/i` → 0 hits | Branch continuation stands: "Select and justify a physical symmetry before excluding coefficients." |
| S09 | `exact_result` | Complete bidoublet scalar-loop RG | **still-open-unchanged** | silent | record silent: `/bidoublet\|Phi-only\|tensor-check/i` → 0 hits | Branch continuation stands: "Full gauge, Delta and Yukawa contributions require the enlarged system." |
| S10 | `exact_result` | Pure scalar fixed quartic obstruction | **still-open-unchanged** | silent | record silent: `/Gaussian one-loop\|sum-of-squares\|pure-scalar\|pure scalar/i` → 0 hits | Branch continuation stands: "Gauge, Yukawa or different-dimensional theories require their own analysis." |
| S11 | `closed_scoped_result` | Coupled 68-real-field norm sector | **still-open-unchanged** | restates | endpoint_audit/README.md | "Six quartic directions are invisible to the restricted neutral potential but change physical stability." |
| S12 | `exact_result` | All seventeen scalar quartic beta functions | **still-open-unchanged** | silent | record silent: `/quartic beta\|153 coupling\|148660155\|beta functions/i` → 0 hits | Branch continuation stands: "Add Yukawa contributions and matching for a full interacting model." |
| S13 | `exact_result` | Full gauge terms in seventeen quartic coordinates | **still-open-unchanged** | restates | endpoint_audit/README.md | "restores the relevant couplings; the old reduced potential is generally not closed under running." |
| S14 | `exact_result` | Four quadratic beta functions and vacuum counterterm | **still-open-unchanged** | silent | record silent: `/quadratic beta\|tadpole\|counterterm/i` → 0 hits | Branch continuation stands: "Include Yukawa and threshold corrections." |
| S15 | `exact_result` | Nonnegative quartic cone under forward RG | **still-open-unchanged** | silent | record silent: `/nonnegative quartic\|forward RG\|positivity\|quartic cone/i` → 0 hits | Branch continuation stands: "Yukawa terms, finite-scale blowup and vacuum selection are separate questions." |
| S16 | `exact_result` | Symmetry subspaces, holomorphic phase and current coupling | **still-open-unchanged** | silent | record silent: `/CP action\|invariant subspace\|holomorphic\|current coupling\|13 quartics\|independent .{0,20}phases/i` → 0 hits | Branch continuation stands: "Check which conclusions survive a declared Yukawa sector." |
| S17 | `closed_scoped_result` | Gauge running for a declared family content | **still-open-unchanged** | silent | record silent: `/two-loop\|two loops\|family count\|arbitrary family/i` → 0 hits | Branch continuation stands: "Threshold-specific running requires selected masses and effective-theory content." |
| S18 | `open_computation` | General minimal-model Yukawa matrix running | **still-open-unchanged** | restates | endpoint_audit/README.md | "General mixed-quartic, noncommuting-flavor finite EFT matching is not claimed." |
| S19 | `open_computation` | All Yukawa corrections to seventeen quartics and four masses | **still-open-unchanged** | restates | endpoint_audit/README.md | "General quantum foam dynamics, all-orders RG, general finite EFT matching, non-Abelian decay trajectories and physical pole masses are not claimed." |
| S20 | `closed_scoped_obstruction` | Constant aligned Yukawa ratio 2/3 | **still-open-unchanged** | silent | record silent: `/\b2/3\b\|aligned Yukawa\|alignment defect\|cubic alignment/i` → 0 hits | Branch continuation stands: "Different leading relation, extra mechanism or finite-coupling cancellation requires a separately specified calculation." |
| S21 | `open_computation` | Full dimensionless one-loop fixed-point classification | **still-open-unchanged** | restates | endpoint_audit/README.md | "These are roots of a fixed-gauge four-quartic proxy; they are not fixed points of the complete running action." |
| S22 | `closed_scoped_result` | Extending quartic positivity preservation to fermions | **still-open-unchanged** | silent | record silent: `/positivity\|forward invariant\|contact margin/i` → 0 hits | Branch continuation stands: "Maximal positivity region, higher-loop persistence and physical vacuum selection." |
| S23 | `open_computation` | Yukawa effects on scalar symmetry subspaces | **still-open-unchanged** | silent | record silent: `/Yukawa effects\|symmetry subspace\|Delta phase\|spurion/i` → 0 hits | Branch continuation stands: "Compute full two-loop quartic sources and Im[(lambda11-i lambda12)(beta11+i beta12)] with generic flavor spurions." |
| F01 | `exact_obstruction` | Yukawa ratio and CKM structure | **superseded-by-record** | new | endpoint_audit/README.md | "The script's square-root mass texture is rank one, leaving degenerate zero-mass subspaces; its eigensolver mixing is not a nondegenerate CKM prediction." |
| F02 | `exact_obstruction` | Strong CP from a real bracket | **superseded-by-record** | new | endpoint_audit/README.md | "Its strong-CP argument also fails: [A,A]=0 does not imply Tr(F∧F)=0, and real matrices need not have positive determinant. The bare theta coefficient remains a separate action datum" |
| F03 | `exact_result` | TM1 neutrino instrument | **still-open-unchanged** | silent | record silent: `/TM1\|solar\|neutrino\|PMNS\|atmospheric/i` → 0 hits | Branch continuation stands: "Use current likelihoods only after fixing the exact mixing hypothesis." |
| F04 | `needs_definition` | Koide and flavor-angle interpretation | **still-open-unchanged** | silent | record silent: `/Koide/i` → 0 hits | Branch continuation stands: "Predictive mass texture, scale and matching prescription remain required; prior S20 exclusion unchanged." |
| F05 | `needs_definition` | Seesaw suppression and physical constraints | **still-open-unchanged** | silent | record silent: `/seesaw\|Takagi\|heavy scale\|inverse-seesaw/i` → 0 hits | Branch continuation stands: "Full textures, observed mixing constraints, decay channels, abundance history and current likelihood." |
| F06 | `exact_result` | Exact seesaw identifiability | **still-open-unchanged** | silent | record silent: `/seesaw\|Takagi\|heavy scale\|inverse-seesaw/i` → 0 hits | Branch continuation stands: "Provide the intended mass texture and physical observable model." |
| F07 | `exact_result` | TM1 atmospheric/CP relation | **still-open-unchanged** | silent | record silent: `/TM1\|solar\|neutrino\|PMNS\|atmospheric/i` → 0 hits | Branch continuation stands: "A texture mechanism and data likelihood are separate inputs." |
| G01 | `exact_result` | Finite Gauss and H123 constraints | **still-open-unchanged** | silent | record silent: `/\bGauss\b\|H123\|spin-half\|joint kernel/i` → 0 hits | Branch continuation stands: "State the intended physical Hamiltonian and continuum limit." |
| G02 | `exact_obstruction` | Torsion equilibrium implies attraction | **still-open-unchanged** | silent | record silent: `/equilibri\|attract/i` → 0 hits | Branch continuation stands: "Derive the actual evolution and its stability estimate." |
| G03 | `exact_obstruction` | Connection propagation from T squared | **still-open-unchanged** | restates | endpoint_audit/README.md | "T² and K∧K are algebraic in K. They provide no independent contortion wave operator. Our component check retains all 24 contortion components." |
| G04 | `needs_definition` | Barbero-Immirzi counting roots | **still-open-unchanged** | silent | record silent: `/Immirzi\|Barbero\|puncture\|degeneracy/i` → 0 hits | Branch continuation stands: "Derive the physical counting prescription and its temporal information process. Integer-spin exclusion requires an additional rule beyond sum m_i=0." |
| G05 | `needs_definition` | Spacetime, masses and gravity from internal grading | **still-open-unchanged** | restates | endpoint_audit/README.md | "This is a conditional construction, not the missing action-to-parameter derivation." |
| G06 | `exact_result` | Holst internal-map invertibility | **still-open-unchanged** | silent | record silent: `/Holst\|Immirzi\|gamma-inverse/i` → 0 hits | Branch continuation stands: "Derive the complete spacetime action, source terms and actual evolution." |
| G07 | `exact_result` | All finite site counts for the fixed H123 | **still-open-unchanged** | silent | record silent: `/\bGauss\b\|H123\|spin-half\|joint kernel/i` → 0 hits | Branch continuation stands: "Constraints on every triple or a continuum Hamiltonian define another problem." |
| N01 | `exact_result` | Coulomb action and printed nuclear table | **still-open-unchanged** | restates | amendments.json[9] (Flag_Condensate_Nuclear_Decay.tex) | "The reported 14-isotope slope comparison uses measured decay inputs and does not predict preformation from first principles." |
| N02 | `needs_data` | Extended isotope input provenance | **still-open-unchanged** | restates | amendments.json[16] (Flag_Condensate_Palpha_Throat_Overlap.tex) | "This amendment adds no new isotope observations." |
| N03 | `needs_data` | Geometric overlap adds predictive value | **still-open-unchanged** | restates | amendments.json[18] (Flag_Condensate_Palpha_Overlap.tex) | "Isospectral alternatives can change channel overlap, so the spectrum alone does not identify preformation." |
| N04 | `needs_data` | Nuclear radius and energy sensitivity | **still-open-unchanged** | restates | amendments.json[11] (Flag_Condensate_Palpha_Refined.tex) | "Tuning a potential to a measured energy supplies that energy as input, and isospectral data need not determine a channel overlap." |
| N05 | `exact_result` | Real Robin boundary versus outgoing width | **still-open-unchanged** | silent | record silent: `/Robin\|outgoing\|self-adjoint\|flux/i` → 0 hits | Branch continuation stands: "Use an outgoing complex boundary for decay widths." |
| N06 | `closed_scoped_certificate` | Complex resonance instrument | **still-open-unchanged** | silent | record silent: `/resonance\|\bArb\b\|pole enclosure\|certified disk/i` → 0 hits | Branch continuation stands: "Separate validated pole enclosures for a specified physical nuclear potential and channel." |
| N07 | `needs_data` | Outgoing nuclear potential poles | **still-open-unchanged** | silent | record silent: `/potential pole\|branch fraction\|Pauli\|capacity inequalit\|within-alpha/i` → 0 hits | Branch continuation stands: "Physical Pauli/state prescription, independently constrained potential, preformation, branch fractions and channel angular momenta." |
| N08 | `needs_data` | Higher radial nuclear pole branches | **still-open-unchanged** | silent | record silent: `/radial node\|node configuration\|node count\|Pauli\|branch fraction/i` → 0 hits | Branch continuation stands: "Supply the physical Pauli/node prescription and branch-specific energy/intensity/angular momentum." |
| N09 | `needs_data` | Potential sensitivity at eleven nodes | **still-open-unchanged** | silent | record silent: `/212Po\|214Po\|minimax\|eleven nodes/i` → 0 hits | Branch continuation stands: "Independently constrain potential and errors, rather than select them using the same decay width." |
| P01 | `exact_result` | Prime transport structural kernel | **still-open-unchanged** | restates | amendments.json[17] (Prime_Gap_Transition_Operator.tex) | "exact saturation is an observation on the tested moduli" |
| P02 | `exact_obstruction` | Strict contraction from transport structure | **still-open-unchanged** | silent | record silent: `/strict contraction\|spectral radius\|totient\|eigenvalue above one/i` → 0 hits | Branch continuation stands: "Any prime-specific contraction theorem must use arithmetic assumptions." |
| P03 | `open_theorem` | Finite prime rank and spectral data | **still-open-unchanged** | restates | amendments.json[17] (Prime_Gap_Transition_Operator.tex) | "The effective-rank exponent is pre-asymptotic and depends on the rank convention." |
| P04 | `open_theorem` | Prime compression, tails and universal spectral law | **still-open-unchanged** | restates | amendments.json[17] (Prime_Gap_Transition_Operator.tex) | "Neither the transition kernel nor an octave or geometric representation establishes a universal physical prime generator." |
| P05 | `exact_result` | Residue characters and L-function extension | **still-open-unchanged** | silent | record silent: `/ramified\|Euler factor\|L-function\|residue character\|Dirichlet/i` → 0 hits | Branch continuation stands: "Supply ramified factors and a proof linking the empirical operator to the L-function." |
| P06 | `exact_result` | Positions, ordered gaps and prime carriers | **still-open-unchanged** | restates | amendments.json[7] (Spectral_Rigidity_Shuffle_Knife.tex) | "Shuffle controls isolate sensitivity to the information that a particular shuffle removes. They do not exhaust all arithmetic alternatives" |
| P07 | `exact_result` | Every binary stochastic transport | **still-open-unchanged** | silent | record silent: `/binary\|spectral radius\|stochastic transport/i` → 0 hits | Branch continuation stands: "Larger alphabets and prime-specific arithmetic remain separate." |
| P08 | `open_theorem` | Conditional fixed-modulus arithmetic limit | **still-open-unchanged** | silent | record silent: `/discrepancy\|fixed-modulus\|renormali[sz]ed error/i` → 0 hits | Branch continuation stands: "Establish the actual-prime discrepancy uniformly along the selected joint sequence, and specify embeddings for a nonzero limit. A prime-specific input beyond structural compatibility, small discrepancy and rank saturation is needed to force subquadratic compression. Prove an unconditional consecutive-prime expansion or provide explicit uniform-in-modulus remainders." |
| R01 | `exact_result` | Wronskian Lie algebra and Poisson lift | **still-open-unchanged** | silent | record silent: `/Wronskian\|Poisson\|cotangent\|Hamiltonian realization/i` → 0 hits | Branch continuation stands: "Specify a Hamiltonian, measure and prime-zero dynamics; the lift alone does not provide them." |
| R02 | `exact_result` | Finite spectral growth and stationarity | **still-open-unchanged** | restates | amendments.json[22] (Riemann_Spectral_Critical_Line.tex) | "All infinite-sum or long-time conclusions require the relevant convergence and exchange-of-limit argument." |
| R03 | `exact_obstruction` | Printed spectral stability ratio | **still-open-unchanged** | silent | record silent: `/stability ratio\|spectral stability/i` → 0 hits | Branch continuation stands: "Choose and justify the intended stability diagnostic." |
| R05 | `exact_obstruction` | Infinite zero sums and resolvent trace | **still-open-unchanged** | restates | endpoint_audit/README.md | "This does not justify interchanging an infinite zero sum and a limit." |
| R06 | `open_theorem` | Hilbert-Polya operator and ensemble exclusions | **still-open-unchanged** | restates | amendments.json[22] (Riemann_Spectral_Critical_Line.tex) | "A diagonal operator assembled only from real ordinates loses the real-part displacement" |
| R07 | `superseded` | Degree/conductor height-floor law | **still-open-unchanged** | silent | record silent: `/conductor\|height-floor\|height floor\|degree-dependent/i` → 0 hits | Branch continuation stands: "Any claimed finite uniformity threshold needs an independent error theorem." |
| R08 | `closed_scoped_result` | Uniform paired-resolvent tails | **still-open-unchanged** | restates | amendments.json[22] (Riemann_Spectral_Critical_Line.tex) | "A diagonal operator assembled only from real ordinates loses the real-part displacement" |
| R09 | `closed_scoped_result` | Common-space finite-section criterion | **still-open-unchanged** | restates | amendments.json[22] (Riemann_Spectral_Critical_Line.tex) | "A diagonal operator assembled only from real ordinates loses the real-part displacement" |
| R10 | `closed_scoped_result` | Explicit zeta-ordinate paired-resolvent tail | **still-open-unchanged** | restates | amendments.json[22] (Riemann_Spectral_Critical_Line.tex) | "A diagonal operator assembled only from real ordinates loses the real-part displacement" |
| C01 | `superseded` | CPF critical reflection and even detectors | **still-open-unchanged** | restates | amendments.json[19] (Critical_Line_As_Fibered_Object.tex) | "fixes the entire line" |
| C02 | `exact_result` | CPF contour instrument and strip limits | **still-open-unchanged** | restates | endpoint_audit/README.md | "This does not justify interchanging an infinite zero sum and a limit." |
| C03 | `exact_result` | Local Friendliness versus Bell bound | **still-open-unchanged** | restates | endpoint_audit/README.md | "The Bell identity survives within its actual assumptions." |
| C04 | `parabolic_obstruction_retained_weaker_trace_reading_corrected` | Klein-cover shear obstruction | **still-open-unchanged** | restates | endpoint_audit/README.md | "Its proposed M=[[1,2],[0,1]] instead has MD−DM=[[0,−4],[0,0]]. The map is not the claimed quotient diffeomorphism. Its trace 2 cannot fix a framing or a magnetic moment." |
| C05 | `scalar_mean_asymptotics_verified_geometric_bridge_open` | Independent Lean kernel verification | **still-open-unchanged** | silent | record silent: `/\bLean\b\|sorryAx\|theorem declaration/i` → 0 hits | Branch continuation stands: "Continue the source-to-claim and geometric bridge audit. The scalar mean/total distinction is now formalized; the orientation-cover and induced homology/isotopy functor remain separate obligations." |
| C06 | `scoped_real_bound_kernel_checked` | Real-probability extension of the declared LF branch | **still-open-unchanged** | silent | record silent: `/Friendliness\|no-signall?ing\|superobserver\|\bLPs?\b/i` → 0 hits | Branch continuation stands: "Map the declared branch assumptions to the intended ACS and experimental semantics. Derive any quantum-realization restrictions separately; broader carrier coverage does not supply that bridge." |
| C07 | `nonfaithful_cover_action_counterexample_verified` | Does identity torus-cover homology force a trivial Klein-bottle mapping class? | **still-open-unchanged** | silent | record silent: `/mapping class\|half-translation\|Klein-bottle\|Klein bottle/i` → 0 hits | Branch continuation stands: "Formalize the full geometric bridge and audit any remaining identification of a matrix trace with isotopy, self-linking or physical quantities." |
| M01 | `exact_result` | Ribbon immersion and self-intersection | **still-open-unchanged** | silent | record silent: `/immers\|self-intersection\|half-twist\|half twist/i` → 0 hits | Branch continuation stands: "Other twist counts require their own global intersection classification." |
| M02 | `needs_definition` | Framing, g-factor and capacitance prediction | **superseded-by-record** | new | amendments.json[8] (Framing_Transformer_Spin_Parity.tex) | "uniform classical charge-to-mass density gives $g=1$ for every closed curve, while varying the densities can change the moment without changing the framing." + "Setting E=mc² therefore gives α⁻¹=L/2, not L." (endpoint_audit/README.md) |
| M03 | `open_theorem` | Ideal magnetic shear stabilization | **still-open-unchanged** | silent | record silent: `/MHD\|magnetic shear\|Kelvin\|tanh\|plasma\|instability band/i` → 0 hits | Branch continuation stands: "Higher-norm continuation, nonlinear vortex persistence, unequal-density interfaces and observed plasma parameters remain separate open tasks" |
| M04 | `conditional_certificate` | Smooth-layer Kelvin-Helmholtz growth | **still-open-unchanged** | silent | record silent: `/MHD\|magnetic shear\|Kelvin\|tanh\|plasma\|instability band/i` → 0 hits | Branch continuation stands: "A second complete operator proof/kernel certificate is distinct from numerical validation. Nonlinear evolution, other profiles and physical plasma parameters need additional analysis." |
| M05 | `exact_result` | All integer twists of the standard ribbon | **still-open-unchanged** | silent | record silent: `/immers\|self-intersection\|half-twist\|half twist\|integer twist/i` → 0 hits | Branch continuation stands: "Other geometry constraints, charge models or material dynamics are distinct." |
| M06 | `exact_result` | Complete tanh instability band | **still-open-unchanged** | silent | record silent: `/MHD\|magnetic shear\|Kelvin\|tanh\|plasma\|instability band/i` → 0 hits | Branch continuation stands: "Spectral multiplicities and nonlinear three-dimensional persistence remain open." |
| M07 | `open_theorem` | Weighted whole-line tanh spectrum and unstable multiplicity | **still-open-unchanged** | silent | record silent: `/MHD\|magnetic shear\|Kelvin\|tanh\|plasma\|instability band/i` → 0 hits | Branch continuation stands: "A second complete operator proof/kernel certificate is distinct from numerical validation. Nonlinear evolution, other profiles and physical plasma parameters need additional analysis." |
| M08 | `conditional_certificate` | Tanh growth stationary maximum | **still-open-unchanged** | silent | record silent: `/MHD\|magnetic shear\|Kelvin\|tanh\|plasma\|instability band/i` → 0 hits | Branch continuation stands: "A second complete operator proof/kernel certificate is distinct from numerical validation. Nonlinear evolution, other profiles and physical plasma parameters need additional analysis." |
| M09 | `exact_result` | Upper endpoint slope and existence of a global growth maximum | **still-open-unchanged** | silent | record silent: `/MHD\|magnetic shear\|Kelvin\|tanh\|plasma\|instability band/i` → 0 hits | Branch continuation stands: "The maximizing location and uniqueness require a further quantitative certificate." |
| M10 | `conditional_certificate` | Certified global tanh growth height | **still-open-unchanged** | silent | record silent: `/MHD\|magnetic shear\|Kelvin\|tanh\|plasma\|instability band/i` → 0 hits | Branch continuation stands: "A second complete operator proof/kernel certificate is distinct from numerical validation. Nonlinear evolution, other profiles and physical plasma parameters need additional analysis." |
| D01 | `exact_result` | Reversible arithmetic and order-preserving encodings | **still-open-unchanged** | restates | amendments.json[31] (The_Reversible_Flattening.tex) | "Reversibility requires an injective encoding on the stated domain and a defined inverse on its image." |
| D02 | `exact_result` | Lattice phase and scaled counts | **still-open-unchanged** | restates | amendments.json[5] (Scaled_Invariance_of_Infinity_and_Zero.tex) | "A finite-resolution count and its joint-scaling ratio are properties of a specified observation protocol." |
| D03 | `needs_definition` | Variance as noncommutativity and geometric ontology | **still-open-unchanged** | silent | record silent: `/noncommutativ\|sheaf\|order defect\|O\(4\)/i` → 0 hits | Branch continuation stands: "Choose source/target typing for order defects, a faithful observable and probability law; if using sheaf language specify topology, restrictions and gluing. The optional completion is not identified with an unstated physical ontology." |
| K01 | `needs_definition` | Transparent constraints and deterministic arithmetic | **still-open-unchanged** | restates | amendments.json[2] (ACS_Deterministic_AI_Stack_PDR.tex) | "Deterministic replay and provenance are engineering properties of a specified implementation." |
| K03 | `needs_source` | External Yang-Mills comparison | **still-open-unchanged** | silent | record silent: `/Yang-Mills\|Yang--Mills\|sealed_spec\|checker/i` → 0 hits | Branch continuation stands: "Supply the full external proof, theorem statement, hypotheses and dependencies. Keyword scores cannot establish its truth, and these checker findings cannot refute it." |
| NS01 | `needs_source` | Identify Croft reference | **still-open-unchanged** | silent | record silent: `/Navier\|Croft\|enstrophy\|vortic\|solenoidal\|PDE/i` → 0 hits | Branch continuation stands: "Provide the author, title, link or passage intended by Croft; cross-reference remains an alternative transcription." |
| NS02 | `evidence_review_only` | Latest primary Navier-Stokes advances | **still-open-unchanged** | silent | record silent: `/Navier\|Croft\|enstrophy\|vortic\|solenoidal\|PDE/i` → 0 hits | Branch continuation stands: "Independent full analytical and proof-kernel review of newly released claims; retain precise equations and hypotheses." |
| NS03 | `open_theorem` | ACS-to-PDE continuation criterion | **still-open-unchanged** | silent | record silent: `/Navier\|Croft\|enstrophy\|vortic\|solenoidal\|PDE/i` → 0 hits | Branch continuation stands: "Define an ACS functional and prove a cutoff-uniform bridge to a sufficient strain or critical-velocity continuation bound." |
| NS04 | `closed_scoped_obstruction` | Finite projection and bracket identities | **still-open-unchanged** | silent | record silent: `/Navier\|Croft\|enstrophy\|vortic\|solenoidal\|PDE/i` → 0 hits | Branch continuation stands: "Specify the actual ACS projection/carrier, prove closure or bound the discarded-mode defect, and establish continuum estimates." |
| NS05 | `open_theorem` | Unforced 3D smooth finite-energy problem | **still-open-unchanged** | silent | record silent: `/Navier\|Croft\|enstrophy\|vortic\|solenoidal\|PDE/i` → 0 hits | Branch continuation stands: "Prove or independently verify the claimed theorem with its exact equation, data, domain, force, energy and regularity class." |

## The T3 SU(3) closure attractor at 50,000 and 1,000,000 samples

**The limitation being tested.** `papers/core_trilogy/Palatini_Gauge_Attractor.tex`:2366-2375 reads:
"The suite uses 100 Riemann zeros (Odlyzko tables) and 50{,}000 random subspaces (Grassmannian
sampling). Extension to $10{,}000$ zeros or $10^6$ subspaces would strengthen confidence bounds but is
not expected to change qualitative results".

The claim behind it is Proposition `prop:selection`, :1061-1063: "For 50,000 randomly sampled
8-dimensional subspaces (uniform on $\mathrm{Gr}(8,15)$), $\mathcal{D}(V) > 0.49$ in every case; no
alternative achieves $\mathcal{D} < 0.1$."

**Which code samples it.** The proof (:1080) cites `selection_full.py` and `acs_verify_all.py`.
Neither draws Grassmannian subspaces:

- `selection_full.py` runs random-start gradient flows.
- `acs_verify_all.py`'s only subspace code is an `in_subspace` membership helper.
- `code/acs_codebase/extras/riemann_scaled_final.py`:35 is a `print` of the hard-coded string
  "0/50000 random subspaces below defect 0.01".

The only Gr(8,15) sampler on disk is `scripts/generate_paper_figures.py::sl3_defect_and_samples`
(:222-241). It draws a 15×8 Gaussian `C` with `default_rng(20260423)`, maps it through the `sl_n_basis(4)`
matrix, and evaluates the paper's D(V). The figure uses it at n = 2000.

**What was run.** A stdout-only driver imported that module and called the function unchanged. No
figure was written. Pinned venv, NumPy 2.2.6, seed 20260423:

```
python -I run_closure.py <worktree> 50000
python -I run_closure.py <worktree> 1000000
```

| n | wall time | D(sl(3,R)) | min D | max D | D < 0.01 | D < 0.1 | D < 0.49 | D < 0.5 |
|---|---|---|---|---|---|---|---|---|
| 2,000 | 1.1 s | 3.176e-16 | 0.508295 | 0.819501 | 0 | 0 | 0 | 0 |
| 50,000 | 24.0 s | 3.176e-16 | 0.461262 | 0.825336 | 0 | 0 | 2 | 3 |
| 1,000,000 | 482.4 s | 3.176e-16 | 0.422638 | 0.858106 | 0 | 0 | 35 | 66 |

Wilson 95% intervals for the fraction of draws below each threshold:

| n | D < 0.01 and D < 0.1 (k = 0) | D < 0.49 | D < 0.5 |
|---|---|---|---|
| 50,000 | [0, 7.682e-05] | 2/50,000: [1.097e-05, 1.458e-04] | 3/50,000: [2.041e-05, 1.764e-04] |
| 1,000,000 | [0, 3.841e-06] | 35/10⁶: [2.517e-05, 4.867e-05] | 66/10⁶: [5.188e-05, 8.396e-05] |

**What reproduces and what does not.**

- *Reproduces:* "0/50000 below 0.01" and "no alternative achieves D < 0.1", at 50,000 and at 10⁶. At
  10⁶ the 95% upper bound on the fraction of draws below 0.1 is 3.841e-06.
- *Reproduces:* the figure caption's minimum of 0.50 at n = 2000 (0.508295).
- *Does not reproduce:* "$\mathcal{D}(V) > 0.49$ in every case". With this sampler and seed, 2 of the
  first 50,000 draws fall below 0.49 (minimum 0.461262). At 10⁶ the sample minimum falls to 0.422638,
  and 35 draws are below 0.49.
  - The 50,000-sample minimum is a draw statistic that keeps falling as n grows, not a floor.
  - The original 50,000-sample run's code and seed are not on disk, so this page cannot say whether
    that run used a different sampler.

**Scale reached.** 10⁶ samples finished in 482.4 s. A larger n would fit in 20 minutes; linear
extrapolation gives about 2.4×10⁶. That is an extrapolation only; nothing beyond 10⁶ was run.

**What sampling cannot test.** Any 8-dimensional subalgebra has D = 0 exactly, and any continuous
sampler hits a given subalgebra with probability zero. The Wilson bounds therefore bound the fraction
of generic subspaces near closure. They are not evidence of uniqueness.

The record already contains a counterexample to uniqueness.
`docs/condensate_energy/selection_energy/README.md`:17 says: "The six strictly upper triangular
matrix units plus two diagonal traceless generators form a closed, eight-dimensional solvable
algebra." The same `closure_defect` function used above gives D = 0.0 for that algebra
(`solvable_check.py`, stdout only).

The Remark at :1083-1094 says, at :1089, "The only other 8-dimensional subalgebra of $\mathfrak{sl}(4,\mathbb{R})$
is $\mathfrak{su}(3)$ itself". That sentence is therefore contradicted by the record's own audit.

Two further points:

- The sampler is uniform on Gr(8,15) in the coordinates of `sl_n_basis(4)`, not in the Frobenius
  inner product in which D is measured. That basis's Gram matrix has diagonal 2 and off-diagonal
  entries up to 1 in absolute value, measured with the same check script.
- Paper A is manifest-bound and was not edited. The status stays T3 ("numerical, not a uniqueness
  theorem", `docs/ACS_FRAMEWORK_SKILL.md`:110).

**Not done here:** the "10,000 zeros" and Wronskian-Jacobi halves of the same limitation sentence.
