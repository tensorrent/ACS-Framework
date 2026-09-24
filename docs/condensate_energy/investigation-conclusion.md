# ACS condensate/binding investigation — conclusion at the evidence boundary

**The tested mechanism can bind classical fields, but the present ACS source
work does not yet select a stable physical particle from it.** We have
reproducible bound profiles, charge-breaking radiation and dispersal, a
consistent selected gauge embedding, and explicit reasons that none of these
alone supplies the missing particle identification. The remaining boundary
is the complete canonically normalized action, selected physical vacuum and
carrier spectrum; additional runs of the same reduced model cannot determine
those inputs.

This closes the requested investigation to the extent supported by the
current action and data. It does not close all ACS mathematics, solve a
Millennium problem, or establish matter as a Klein-foam condensate. Those
broader identifications have not been derived by these experiments.

## Established within explicit scope

1. **Self-consistent scalar binding exists in the tested model.** At Q=1000,
   b=2sqrt(3)/27, energy is 838.163096 against a free-q threshold of 1000.
   The exterior propagation gap and conserved charge evade the earlier
   massless-exterior/static-real-field obstructions. Independent stationary
   methods, tail and virial checks, linear scalar modes and finite-time
   evolution qualify the reference. Formation tests involve prepared charged
   packets, not spontaneous creation from vacuum.
   [Full binding evidence](self_binding/README.md).

2. **The obvious global-charge assignments do not furnish exact generic ACS
   protection.** Both generic bidoublet Yukawa terms force zero overall Phi
   charge. The gauge-allowed holomorphic Delta quartic breaks the remaining
   classical uniform X phase; without that quartic, X has nonzero mixed weak
   anomalies. The exact audit includes flavor generators and the neutral
   vacuum trap. It does not exclude every rank-deficient texture or a newly
   specified model with extra fields/symmetries.
   [24-check charge audit](charge_audit/README.md).

3. **Approximate charge produces measurable leakage, not a binary answer.**
   Twenty nonlinear runs restore epsilon Re(q^4)/4 in a selected gauge-allowed
   scalar realization and verify its exact source balance. At epsilon/b=.5,
   the finest run retains 27.13% of initial energy inside radius15 at time400;
   the sustained half-energy exit converges toward about133–135 model-time
   units on the two finest meshes. This is an operational finite-time measure,
   not a physical particle half-life. Weak cases retain most core energy over
   the same observation interval.
   [Evolution and preserved failures](charge_leakage/README.md).

4. **Weak-breaking radiation has an independently predicted mechanism.**
   Outgoing linear response predicts P=1.077996267 epsilon² to leading order,
   with q frequencies -3omega,+5omega and condensate frequencies ±4omega.
   A second discretization converges to that result, and the weakest nonlinear
   run shows the predicted harmonic amplitudes within about4%. Total measured
   flux is larger because additional decaying preparation waves remain; no
   asymptotic total-flux equality or physical lifetime is inferred.
   [Radiation comparison](charge_leakage/README.md).

5. **Adding Gauss law and electric energy does not immediately eliminate the
   reduced branch.** At Q=1000,e=.12, E/Q=.96420948 and omega=.96932000,
   with 119.381751 units of electric energy included. Two numerical methods
   agree. Sixty continuum solves, six independent variational minimizations,
   exact field/mass/charge contracts and preserved failed cases distinguish
   successful reference solutions from finite-box artifacts. The two tested
   fission partitions cost more energy; they do not prove general stability.
   [Gauge experiment and 45 qualification checks](gauge_completion/README.md).

## What prevents a particle conclusion

The viable selected gauge slice uses Delta's existing T15 charge with
e=sqrt(3/2)g4. It avoids introducing an anomalous new gauge U(1), but its
exterior Delta=0 leaves SU(4) unbroken. The complete vacuum gauge Gram has
18 massless modes, including vector fields with T15 charge 2/3 of the
chosen scalar's. Its scalar Hessian also has four uneaten flat directions.
Thus the scalar-only threshold is not the full-theory threshold. This is
an obstruction to the stability inference, not a calculated gauge decay rate.

The conventional neutral-Delta vacuum has a different unbroken group and
mass spectrum. The exact alternate mass Gram finds SU(3)c×U(1)em, but the
neutral Delta component has zero electric charge. Charged partners exist;
their potentials, masses and lepton emission channels must be computed in
that actual vacuum. Reusing the old profile would silently change the theory.

Even the proposed Yukawa ratio does not settle the carrier threshold. At the
selected equal-VEV vacuum, M_D=(Y+Z)/2. Holding Z/Y=2/3, two explicit choices
Y=.1I and Y=I yield opposite answers for allowed pair emission. Likewise,
the allowed norm-potential class contains both our binding example and an
exact no-binding region b>=g^4/lambda_chi. These are counterexamples to
selection by symmetry or those ratios alone; they do not refute a future
complete derivation supplying additional constraints.

The source [RG threshold report, section5](../frontier/2026-09-11/workstreams/rg/report.md)
explicitly requires selecting the stationary vacuum, canonical scalar Hessian,
gauge Gram, Weyl mass map and light-field projectors before physical matching.
The [canonical manuscript](../../papers/core_trilogy/Palatini_Gauge_Attractor.tex)
also qualifies its incomplete kinetic normalization chain. Counting17 quartics
and four quadratic coefficients does not select their values. A proposed Phi
quartic does not determine the Delta self-coupling used in the experiment.

Finally, an exact classical rescaling preserves dimensionless solutions and
charge while changing energies and lifetimes. Consequently the present model
units cannot be converted to a unique particle mass or lifetime without
additional physical scale selection or an explicitly adopted measured input.

## Requirement-by-requirement disposition

- **Restore omitted charge breaking and measure survival:** completed for the
  stated selected action, with exact source accounting, 20 runs, refinements
  and independent radiation calculations. Full quantum decay rates remain
  outside the claim.
- **Investigate an existing gauge charge and alternatives:** completed by an
  exact T15 embedding, full Gauss/electric stationary tests and a separate
  conventional-vacuum electromagnetic mass-Gram calculation. A generic
  physical charged-particle solution is not thereby established.
- **Include other carriers and thresholds:** completed as mass/charge-sector
  identification and kinematic tests, including exact opposite-threshold
  countermodels. No non-Abelian transition trajectory or quantum width is
  claimed.
- **Determine what source parameters are actually selected:** the invariant
  basis, transformation laws and conditional matching relations are available;
  full canonical coefficients, the physical vacuum, carrier masses and the
  physical scale are not selected by the cited implementation and source
  conclusions. This is supported by explicit countermodels and scaling, not
  merely by a failed search for a file.
- **Preserve failures and verify calculations independently:** satisfied by
  the retained original optimization/response failures, successful repairs
  at unchanged numerical gates, independent discretizations, exact algebraic
  checks, all survey outcomes and content-hash receipts. Successful checks
  do not promote an untested full-theory assertion.
- **Deliver a reproducible integrated assessment:** this report, the four
  linked experiment records, their scripts/raw data/figures and the final
  [gauge receipt](gauge_completion/receipt.json) provide the evidence chain.

## The concrete ACS completion requirement

Further physical identification needs one specified canonically normalized
action and a derived or explicitly selected vacuum, followed by its complete
scalar, gauge and fermion spectrum. That supplies the minimum energy over
all states carrying the relevant exact charges. The localized branch must
then be tested against that threshold and perturbations in every retained
field sector; an approximate charge additionally needs a width calculation.

This is the missing derivation, not a request for another arbitrary parameter
scan. The current code provides reusable conservation, tail, energy, carrier
and provenance checks for that step. It does not supply the missing input by
renaming the reduced solution or by treating its numerical survival as proof.
