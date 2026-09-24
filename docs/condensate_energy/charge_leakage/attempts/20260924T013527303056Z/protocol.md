# Quartic charge breaking: evolution protocol before execution

2026-09-23. This continues the qualified scalar soliton with the explicit
interaction identified by the complete scalar charge audit. This is a selected
classical action and vacuum, not a claim that ACS fixes these coefficients.
All earlier code, reports and receipts remain frozen.

## Action and field map

Add V_break = epsilon Re(q^4)/4 to the previous potential. The real quartic b
remains 2sqrt(3)/27. For |epsilon|<b the complete quartic in q is nonnegative.
The q equation gains -epsilon conjugate(q)^3. The condensate equation is
unchanged. The exact integrated balance, with no boundary flux, is
Qdot = epsilon integral Im(q^4). Charge oscillation is not by itself decay.

There is an explicit gauge-allowed scalar embedding, to be checked exactly:
Phi=chi I2/2, D1=D2=0, D3=q I4/(2sqrt(2)). The inherited Cartesian Delta
convention gives Nphi=chi^2/2, NDelta=|q|^2/2 and HDelta=3q^4/64. Both kinetic
terms are canonical with the previous 1/2 convention. The selected invariant
potential is (Nphi-1/2)^2 + 2 Nphi NDelta + b NDelta^2
+ kappa HDelta + conjugate(kappa HDelta), with kappa=8epsilon/3.
Gauge currents vanish on this polar, color-isotropic ansatz. Fermions set to
zero solve their classical equations; this removes neither their interactions
nor their possible quantum emission channels from the full theory.

This choice differs from the conventional neutral Delta vacuum: exterior
Phi=I2/2, Delta=0, and a rank-four Delta configuration in the core. It does not
repair the failed neutral-mode identification. Other scalar directions, gauge
perturbations, actual ACS vacuum selection and quantum channels remain to be
assessed separately. The other permitted quartic coefficients are explicitly
set to zero in this selected test action, not derived to vanish.

## Frozen experiments

Start from the already qualified b-reference soliton, Q0=1000, with its original
angular velocity. Turn on the selected epsilon as part of the initial
Hamiltonian; record its actual E0. No switching after initialization, damping,
absorber, external work or normalization during evolution.

- epsilon/b = 0, .001, .01, .05, .1, .25, .5, .9, at initial phase0.
- Additional phases pi/8 and pi/4 at ratio .5.
- Negative epsilon at ratio -.5, phase0, to compare with +.5,phase pi/4.
- Reverse initial charge at +.5,phase0, for conjugation symmetry.
- Vacuum control at +.5.
- Refine space/time for +.1 and +.5,phase0.

Total15 runs. Coarse grid dr=.1, dt=.005; refined dr=.05, dt=.0025.
End time400, radius460. Record core energy/charge inside radius15, total energy
and signed charge, maximum far-zone energy (r>450), center fields and wave
probes near r20,40,60. Save histories every .1 time unit. Integrated charge
source is accumulated every time step using the Verlet kick trapezoid identity.

## Numerical gates and physical outcomes

- Relative total energy drift <1e-3.
- Charge minus integrated source residual <1e-8 relative to max(1,|Q0|).
- Far-zone energy <1e-8 E0; otherwise enlarge domain without changing physics.
- Refined local-energy and total-charge curves within .02 of E0 and |Q0|.
- Negative-coupling/phase equivalence and conjugation controls: energy curves
  agree within1e-8; conjugate charge histories have opposite sign.
- Vacuum remains exactly vacuum. Verify potential-force and Noether-source
  derivatives independently before integrating.

Report first sustained energy-half exit: local E/E0<.5 for at least10 time
units on the sampled history. If absent, report observation right-censored at
400; do not infer an infinite lifetime or fit an unsupported decay law.
Also report charge sign/oscillation and energy radiated independently.

On the original rotating background q=f exp(i omega t), the breaking force
has frequency -3omega. Coupled linear response can also contain q frequency
+5omega and chi frequency4omega. These lie above the reference exterior gaps
for q (1) and chi (sqrt(2)). Analyze probe spectra as diagnostics, without
making a preferred peak, decay or survival a numerical pass criterion.

If results require targeted longer runs or tighter refinement, preserve this
batch and register the next experiment before execution.
