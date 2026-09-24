# Capture and stability continuation — protocol before execution

2026-09-23. Scope: the explicitly added classical 1-D complex wave model from
the parent experiment. This is not the full Klein-foam dynamics. Original
source, results and source hashes remain frozen.

## Questions and distinctions

1. Can a finite, compact, nonnegative barrier on a massless half-line have an
   L2 stationary eigenfunction? Give a continuum argument, not an inference
   from a finite-time simulation or a finite Dirichlet box spectrum.
2. Does admitting a pulse and then raising the barrier improve finite-time
   retention? What work does the prescribed gate do on the field?
3. What explicit alternative admits actual localized oscillatory modes?
   Use a positive exterior threshold as a control, not as a derived mass.

## Dynamic model and exact discrete budget

Phi_tt=Phi_xx-U(x,t)Phi, U(x,t)=h(t) B(x), B the same cell-average
unit rectangular barrier [4,5]. The cavity is [0,4], x=0 is Dirichlet.
Energy and outward flux are the parent definitions. In the continuum:

  dE/dt = integral (U_t |Phi|^2 / 2) dx;
  dE_region/dt + J_right = integral_region (U_t |Phi|^2 / 2) dx.

Use implicit midpoint with H_mid=(H_old+H_new)/2. The exact discrete work
for each step is dx/4 sum (U_new-U_old)(|q_new|^2+|q_old|^2).
The midpoint flux plus this local work must close each regional budget.
Also accumulate continuum midpoint work dx dt/2 sum U_t(t_mid)|q_mid|^2;
its difference from endpoint work should shrink under time refinement.
Positive and negative work are reported separately. No subtraction of work
from regional energy is presented as an attribution to the incoming pulse.

The gate uses a C1 cosine ramp from h=0 to h=H over duration 4. Both its
timing and height are external controls; no autonomous feedback is claimed.
Initial Gaussian: center30, sigma4, carrier pi/4, left-going velocity as in
the previous capture experiment. Normalize actual initial energy to1, once.
No damping, absorber or later normalization.

## Frozen sweep and controls

- Domain240, end160, dx0.1, dt0.005, sampling every0.2.
- Always-open control and always-raised H=4,16 controls.
- Close starting at t=16,20,24,28,32,36 for each H=4,16: all12 cases.
- H16 start28 reopening at60 over4 time units.
- H16 start24 and28 with dx0.05,dt0.0025.
- H16 start28 with dx0.1,dt0.0025 (time-only refinement).
- H16 start28 with domain280 (boundary control).
- H16 start28 with global phase1.234 (representation control).
- H16 start28 with duration2 and8 (physical changes, not invariances).

Total23 long dynamic variants. Report all timings, not just the largest.
Compare retained energy at80 and160, core versus barrier energy, total energy,
work, integrated signed outward flux and maxima over sampled trajectories.
The maximum over this finite sweep is exploratory, not an optimized policy.
Retention at160 does not establish infinite-time stability.

Independent calibration: DOP853 integrates the first-order semi-discrete
equations plus continuum work on domain40, pulse center10, end12, H16 closure
start6 duration2, dx0.1. Compare midpoint dt0.005 and0.0025 to that reference.
Check state error in the final Hamiltonian energy norm <0.005 at the fine step
and decreasing on refinement. Continuum work disagreement <0.005 and decreasing.

Numerical gates: energy/work and regional flux/work residuals <1e-8;
last10 units' energy fraction <1e-8 throughout sampled histories;
combined grid refinement changes trapped curve <0.03 of incoming energy;
larger domain and global phase changes <1e-8; midpoint versus endpoint work
difference decreases on time refinement. No outcome thresholds are imposed on
retention, sign of advantage, or monotonicity with closing time.

## Genuine bound-mode control

Change the physical model explicitly: U=0 on [0,4], U=mu^2 on (4,infinity),
mu=2, Dirichlet at0. A stable localized mode has 0<omega<mu and obeys
omega cot(4 omega)=-sqrt(mu^2-omega^2). Solve every branch below threshold
with a bracketed root method. Independently diagonalize the finite-difference
Hamiltonian on domains20 and40, dx0.1 and0.05. Check matching residual <1e-9,
domain eigenvalue difference <1e-5 and fine-grid eigenvalue error <0.005 and
decreasing. Use the analytic exponential tail to establish localization;
finite-box eigenvectors alone are not evidence for a bound state.

Static bound-mode existence does not show capture from continuum scattering
states. The time-independent linear spectral subspaces do not exchange
population. Any proposed capture mechanism must address that separately.

## Failure handling

Save each run's source/protocol copies, raw results and checks under attempts/.
If a check fails, preserve it and state any protocol or code amendment before
rerunning. Numerical calibration can change; a physical negative result cannot
be relabeled a solver failure. No manuscript or standing-rule changes.
