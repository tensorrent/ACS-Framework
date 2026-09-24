# Targeted refinement supplement

Registered after the completed 76-case sweep, before these four runs.
All original15 numerical checks passed. Two remaining precision limits warrant
targeted checks: the fast/soft g16,M0.1,K0.1 gate changed its height trajectory by
2.7424 model units under refinement, and the selected trajectories were extended
to480 only on the coarse grid.

Keep the Hamiltonian, input pulses, parameters and all original results fixed.

1. Run the middle-carrier g16,M0.1,K0.1 case on dx0.025,dt0.00125, domain240,
   end160. Compare with dx0.05,dt0.0025. Both trapped-energy and height trajectory
   differences must be smaller than the preceding refinement differences.
2. Run the three selected long cases on dx0.05,dt0.0025, domain560,end480.
   Require full trapped-energy curve changes <0.03 E0 and endpoint relative
   differences <5% against each corresponding coarse result. The latter adds
   protection against a small late signal being hidden by a generous E0 scale.
3. In all four runs retain the original energy/work/flux tolerance1e-3 and remote
   boundary-zone tolerance1e-8. Report actual residuals and differences.

Do not retune physical parameters to preserve a retention result. A failure
would limit quantitative claims and remain in the record; the analytic exclusion
of stationary harmonic bound fields is independent of these trajectories.
