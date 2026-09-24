# Stationarity refinement after the preserved optimizer stop

The 32-start survey finished. Reference energy/charge is about0.83813, the
independent continuum boundary-value solution converges, and the energy,
domain and virial checks pass. However L-BFGS-B stops on relative energy change
before the reference gradient reaches the registered1e-5 tolerance: coarse and
fine infinity norms are about1.7e-5 and2.1e-5. The original failure is preserved.

Do not alter the model, starting branch, charge, mesh or numerical tolerance.
Polish the three reference discrete solutions (coarse, fine, larger domain)
with their exact fixed-charge Hessian and damped Newton steps. Require the same
1e-5 threshold and aim below1e-8. Recompute energies, virial terms and spectra;
repeat the independent-method and domain comparisons with the polished values.
Keep the 32 survey outcomes unchanged and distinguish approximate survey points
from qualified reference solutions. Only the recorded stationarity failure may
be superseded; any other failure remains blocking for numerical qualification.
