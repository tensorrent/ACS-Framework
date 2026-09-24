# Autonomous gate: registered model and numerical protocol

2026-09-23, before execution. This is a candidate Hamiltonian completion of the
previous classical 1-D experiment. The cited Klein-foam source sections do not
select these equations or parameters. No claim of full foam or derived mass.

## Hamiltonian and preparation

E = integral (|Phi_t|^2+|Phi_x|^2+g a^2 B(x)|Phi|^2)/2 dx
    + M adot^2/2 + K(a-1)^2/2.

B is the fixed cell-average barrier indicator on [4,5], cavity [0,4].
a is a real coupling coordinate, not a literal aperture radius; a can cross0.
g,M,K are positive. The barrier g a^2 stays nonnegative. The equations are

Phi_tt=Phi_xx-g a^2 B Phi;
M addot=-K(a-1)-g a integral B|Phi|^2 dx.

Start a=1, adot=0, so mechanical kinetic and restoring energies are zero.
The incoming field has a Gaussian envelope centered30, sigma4, and carrier k.
Use the previous left-going initial velocity and normalize actual initial field
energy to E0 once. No external forcing, schedule, damping, absorber or subsequent
normalization. Track field, gate kinetic/restoring, and their combined energy.
The continuum field work rate is g a adot integral B|Phi|^2 dx; the gate receives
its negative. The trap budget includes flux through5 and local work.

At a=1 the initial field force points toward smaller a, hence lower barrier.
The restoring term can later raise it. This is a testable candidate for loading
and closure, not an assumed capture outcome. Even if mechanical energy remains,
it is not counted as field capture or as newly generated particle mass.

## Main sweep, frozen controls and adaptive validation

- Three carriers: pi/8, pi/4, pi/2. All have E0=1.
- g in {4,16}, M in {0.1,1,10}, K in {0.1,1,10}:54 coupled cases.
- At each carrier: permanently fixed a=1 controls for g4,g16 and g0 open:9.
- Domain240, dx0.1, dt0.005, end160; sample every0.2.
- Reference coupled case: g16,M1,K1,k=pi/4. Extra E0=0.25 and4, phase1.234,
  and domain280 controls:4.
- Fixed refinement cases: g4,M1,K1 and g16,M0.1,K0.1, both k=pi/4,
  dx0.05,dt0.0025:2.
- For each carrier, select the coupled case with largest *field* trap energy
  at160; independently refine its space/time grid and extend its coarse-grid
  evolution to480 on domain560:6. This prespecified maximum selection is only
  numerical validation, not an out-of-sample performance claim. Retain every
  nonselected case; do not tune physical parameters after observing outcomes.
- Vacuum at the reference settings, end16:1.

Total76 runs, including the vacuum and selected validation runs even if their
parameters overlap. Report energy fractions, mechanical storage, signed energy
exchange, barrier extrema, and late-time min/max/mean (last40 time units).
Late-time averages distinguish oscillatory residence from one favorable phase.
No threshold prescribes whether retention must improve over fixed barriers.

## Numerical validation

Use velocity Verlet for the coupled Hamiltonian. Unlike the previous quadratic
midpoint solver, it does not conserve the physical energy exactly. Measure its
drift and convergence; never normalize it away. Integrate endpoint work and
flux by trapezoid quadrature independently of energy differences.

- Every run: combined energy drift / E0 <1e-3; field/work and gate/work
  and regional flux/work residuals on the same scale <1e-3. Only the vacuum
  uses1 as its error scale.
- Distant last10 units energy / E0 <1e-8 over sampled trajectories.
- Refined designated and selected cases: trapped-energy curve difference <0.03
  E0. Report gate and barrier differences too, since phase can amplify them.
- Phase and larger-domain reference changes <1e-8 E0.
- Vacuum stays exactly at its equilibrium within1e-12.
- Independent short DOP853 integration: g16,M0.1,K0.1, k=pi/4, center12,
  sigma2, domain40,end16,dx0.1. Compare dt0.005 and0.0025 against rtol2e-11,
  atol2e-13. Error uses final field energy norm plus M dv^2/2+K da^2/2;
  fine error <0.005 and smaller than coarse. Total energy drift and work
  disagreement with independently integrated work must decrease under refinement.
- Reverse the coarse short trajectory's field/gate velocities and evolve for
  the same duration. Recover initial coordinates and reversed velocities to
  absolute energy-norm error <1e-8. This tests time reversibility, not attraction.
- Static g4,k=pi/4 results through80 must agree with the prior midpoint
  capture history to within0.001 E0 on the common grid.

Each attempt copies its sources and this protocol before execution and preserves
raw results plus failed checks. Unexpected nonconvergence remains a numerical
limitation until corrected; physical outcomes do not determine tolerances.

## Scope and analytic checks

Derive equal-and-opposite field/gate work directly from E. Distinguish positive
total energy (bounded motion) from localization, equilibrium binding, and
quantized mass. If a settles to a finite constant, the previous compact-positive
barrier no-bound-mode argument still applies. That argument alone does not
settle persistent time-dependent or nonlinear localized solutions.

The machinery of mutual field/mechanical backreaction is familiar from cavity
optomechanics; no identity with an optical apparatus or established physical
Klein foam is assumed. Transfer ledger entry stays a candidate physical model.
