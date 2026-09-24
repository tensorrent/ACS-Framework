# Condensate-mediated self-binding: protocol before numerical execution

2026-09-23. Candidate motivated by the quadratic/quartic scalar potentials and
norm cross-coupling in Palatini_Gauge_Attractor.tex (around lines1950 and2040),
and task2_lagrangian.py (Higgs sector). The complete ACS gauge theory does not
automatically select this real-plus-complex scalar reduction or its global U(1).
The historical BCH-norm proxy does not by itself establish a canonically
normalized physical potential. No existing action or ledger is changed.

Established related mechanism: Friedberg-Lee-Sirlin solitons, with a positive
complex-field quartic also tested here. Reference: arXiv:2303.09566v2. This is a
reproduction/extension of a known mechanism, not discovery of a new theory.

## Model and normalization

Write Psi=q/sqrt(2), q complex, chi real. In three spatial dimensions:

E=integral [ (|q_t|^2+|grad q|^2+chi_t^2+|grad chi|^2)/2
            + (chi^2-1)^2/4 + chi^2|q|^2/2 + b|q|^4/4 ] d^3x.
Q=integral Im(conj(q) q_t) d^3x.

The vacuum is chi=1,q=0. The exterior charged-field mass/propagation threshold
is1 in these chosen units. It follows from the cross-coupling and vacuum, rather
than a prescribed spatial barrier. All coefficients and the vacuum scale are
model inputs. Stationary rotating fields q=f(r)exp(i omega t) have
Q=omega I, I=4pi integral r^2 f^2 dr. Minimize
E_Q=gradient energy+potential energy+Q^2/(2I), including BOTH fields' energies.
This constrained numerical search constructs stationary candidates; it is not
a simulation of their physical formation.

## Frozen stationary survey

- b in {0,2sqrt(3)/27,0.5,1.2}; Q in {100,300,1000,3000}:16 settings.
- Two different compact seeds per setting, initial radii3 and7:32 optimizations.
- Spherical finite-volume mesh: radius30, dr0.1, natural regular center,
  chi(R)=1,f(R)=0. Use the exact shell volumes and symmetric gradient energy.
- Compare energy/charge with1, omega with1, core depletion, radius containing
  90% charge, and charge fraction in the outermost5 units.
- Lower energy among the two seeds is the reported candidate, with both attempts
  retained. A diffuse finite-box state is not identified as a soliton.
- b=1.2 is an analytic no-binding control: U-f^2/2 equals
  [(chi^2+f^2-1)^2+(b-1)f^4]/4>=0, implying E>=|Q|.
- b=2sqrt(3)/27 is a numerical reference inspired by the source's scalar value;
  this is not a derivation that its canonical reduced coupling must equal b.

## Independent checks for reference b=2sqrt(3)/27,Q=1000

If this reference is localized and E/Q<1, refine dr to0.05, enlarge radius to40,
and independently solve the radial continuum boundary-value equations with
unknown omega and charge as an extra integrated variable:

chi''+2chi'/r=chi(chi^2-1)+chi f^2;
f''+2f'/r=(chi^2-omega^2)f+b f^3.

Regular derivatives at0, vacuum values atR, and total chargeQ are boundary
conditions. Require BVP convergence/residual <1e-5, continuum virial residual
|G+3V-3T|/E <1e-4, energy agreement across methods/resolutions <0.005 relative,
and domain enlargement effect <1e-4 relative. Require the numerical optimizer's
scaled gradient infinity norm <1e-5 for reference profiles. Nonconvergence is
a solver issue to preserve and repair, not a physical negative.

Compute small eigenvalues of the fixed-charge amplitude Hessian for angular
sectors ell=0,1,2 and the phase operator at ell=0 on both meshes. Include the
rank-one charge term for ell0 amplitude variations only. Report translation/
phase zero-mode discretization errors; negative modes are not suppressed.
This diagnoses linear perturbations in this reduced model, not every nonlinear
or quantum instability. Higher angular sectors add positive centrifugal terms.

## Dynamic follow-up for a qualified reference

Evolve both fields with conservative velocity Verlet, no damping, absorber,
external potential schedule or post-initialization normalization. Use radius120,
end80, dr0.1,dt0.005; refined runs dr0.05,dt0.0025.

- Unperturbed reference from the discrete constrained solution.
- A2% and5% radial shape perturbation of f; initial angular velocity is set once
  to keep Q=1000 and the changed initial energy is reported.
- Refined unperturbed and2% perturbed runs.
- Opposite charge and global phase1.234 controls for the unperturbed state.
- Vacuum q=0,chi=1.

Require relative energy drift <1e-3, charge drift <1e-8, outermost10 units energy
fraction <1e-8, phase/charge-sign invariance in energy observables <1e-8, and
refined local-energy curve changes <0.02 of initial energy. Monitor radius15
energy/charge fractions and chi/f core amplitudes. Do not interpret80 time units
as an infinite-time nonlinear stability proof.

## Evidence boundary

E<Q establishes a barrier to COMPLETE dispersal into free unit-mass charged
waves at conserved Q; it alone does not prove immunity to fission, tunneling or
all perturbations. A stationary object is not yet a formation mechanism from
generic input. The inherited charge is an input and cannot be generated from
zero net charge by these U(1)-symmetric equations. Full ACS embedding, its gauge
constraints and symmetry-breaking terms must be audited separately.

Save protocol/source snapshots and all optimization outcomes. Numerical failures
must be documented before any change or targeted rerun. Keep prior experiments
and source manuscripts frozen.
