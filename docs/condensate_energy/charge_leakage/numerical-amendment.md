# Preserved failures and targeted refinement

The first15 nonlinear runs completed. Energy and charge-source balance,
boundary isolation and symmetry controls pass. The ratio .1 refinement passes.
At ratio .5, dr .1 versus .05 differs by .0200904 of E0 in local energy and
.0435586 of |Q0| in charge, above the unchanged .02 tolerance. Both disperse,
but their half-energy exit times139.9 and134.8 are not yet a qualified precise
lifetime. Keep every original run and the failed check.

Add dr .025,dt .00125 at ratio .5, with a newly Newton-polished stationary
initial condition on that mesh. Compare against dr .05,dt .0025 with the same
.02 curve tolerances. Also evolve dr .05 with dt .00125 to isolate the time
step. Require decreasing errors under spatial refinement; do not relabel the
original coarse-grid failure as a pass. Domain460 and end400 remain unchanged.

The complex outgoing-radiation BVP hit its mesh ceiling, residuals1.02e-5 and
2.40e-5, despite agreement with independently converging finite differences.
Preserve radiation-results.json. Recast the same complex linear equations as
12 real equations, initialize from the recorded approximate solution and
provide an exact Jacobian. Keep the residual gate1e-6 and solver target1e-8.
Do not change the field equations, boundary conditions or power comparison.

Additional diagnostic: run weak ratios .001,.01,.05 with direct discrete
energy flux at radius40. The original batch saved field probes but not that
flux, so it cannot supply a direct flux comparison retrospectively. Compare
mean power over t200–400 to the independent linear epsilon^2 prediction and
report scatter rather than selecting a favorable time interval afterward.
Energy flux is derived from the same finite-volume Hamiltonian: minus edge
stiffness times field difference times the neighboring average velocity,
summed over real condensate and the complex field. Core-energy derivative and
integrated edge flux provide a separate energy-balance check (<1e-3 E0).

Use a new integrator with explicit dr/dt and flux diagnostics, preserving the
original program. Both use the same grid/energy implementation and equivalent
Verlet updates; do not claim their agreement is an independent physics test.
