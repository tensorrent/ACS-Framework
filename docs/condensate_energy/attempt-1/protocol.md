# Condensate retained-energy audit: protocol

2026-09-23. Fixed before the new simulations. Source: Klein_Foam_Monad.tex,
especially the flag-field/throat postulates and the mass ansatz in lines 227–239;
Flag_Condensate_Nuclear_Decay.tex, transfer matrices in lines 126–159; later
frontier branches N01–N09 and M02. No source manuscript or standing ledger changes.

## Questions and scope

1. Does the barrier transmission factor also determine energy retained in a
   confined field? Compare flux, regional energy, WKB exponential and exact T.
2. Does the printed |beta/alpha|² identification agree with the spatial transfer
   matrix under an explicitly declared scattering convention?
3. Are the observed localization and changes stable under resolution, domain,
   initial-phase, small initial-state, and barrier-shape changes?

The complete nonlinear Klein-foam action, wall dynamics, and gluing rules are
not specified in the cited sections. This experiment therefore adds a clearly
labeled **linear one-dimensional wave completion**, not a full foam simulation:

    Phi_tt = Phi_xx - U(x) Phi,
    e = (|Phi_t|² + |Phi_x|² + U |Phi|²)/2,
    J = -Re(conj(Phi_t) Phi_x),   e_t + J_x = 0.

Units c=1; all coordinates, frequencies and energies are dimensionless. U>=0 is
an externally prescribed barrier. Phi is a classical complex amplitude here;
its velocity is an independent variable and is NOT identified with the paper's
imaginary component pi. This choice agrees with the paper's stationary allowed/
forbidden transfer equation but adds a time evolution and positive Hamiltonian.
It does not quantize the field or derive a particle mass or an autonomous soliton.

## Instruments

- Stationary scattering: six frequencies [0.3,0.6,1,1.7,2.5,3.5], six barrier
  heights [0,0.5,1,4,9,16], five widths [0.25,0.5,1,2,3]: 180 cases.
  Cross-check analytic propagation against independent DOP853 integration and
  boundary matching. Include exact threshold, zero-width and zero-barrier cases.
  Define the traveling-wave basis explicitly: alpha=B22, beta=B21. Then test
  the flux relations rather than assigning names by analogy to particle creation.
- Time evolution: cavity [0,4], right barrier [4,4+b], exterior to D=120, fixed
  Dirichlet endpoints. No absorber or renormalization during evolution. Stop at
  t=80, before physical reflection from the distant endpoint can return. Audit
  the exterior tail and a larger-domain repeat rather than assuming this works.
- Prepared field: sin(pi*x/4) in the cavity, zero outside; initial velocity
  -i*(pi/4)*Phi. Normalize its actual discrete Hamiltonian energy to one. This is
  finite-energy broadband initial data after truncation, NOT a monochromatic
  steady scattering state. Record that distinction when comparing with T(omega).
- Sweep U0 in [1,4,9] and b in [0.5,1,2], plus one barrier-free case. Measure
  cavity, barrier and exterior energy, integrated net outward energy flux, and
  total energy. Report t=8,24,48,80 and full sampled trajectories.
- Solve with implicit midpoint on the symmetric finite-difference Hamiltonian,
  dx=0.1, dt=0.02, sampled every 0.2. Use the exact corresponding discrete edge
  energy current for the local conservation check. Repeat three diagonal sweep
  cases at dx=0.05, dt=0.01; repeat the central case at dx=0.05,dt=0.02 to separate
  spatial and temporal effects, and at D=160 to test the exterior boundary.
- At U0=4,b=1, test a global phase rotation of 0.73, a second-mode admixture of
  0.01i, and a smooth barrier edge with tanh width 0.15. A changed physical barrier
  is a sensitivity test, not numerical error. Also evolve the initial difference
  field to distinguish positive-energy stability from local retention changes.
- Independent time-solver check: small-domain DOP853 evolution before an exterior
  return, versus midpoint at two time steps. Closed cavity eigenmode: verify
  energy conservation and the midpoint phase against its independently known
  discrete frequency. A sealed boundary cannot certify outward decay.

## Acceptance and interpretation

Instrument gates: stationary T error <1e-8; R+T error <1e-7; midpoint total and
regional integrated-flux residual <1e-8 of initial energy; global phase invariance
<1e-10; selected refined retained-energy curves differ by <0.02 absolute fraction;
larger-domain difference <1e-6; final distant-tail energy <1e-8. Independent time
solver: reducing dt must reduce error and fine relative state error <0.005.
Failures are reported and corrected or left unresolved, never silently relaxed.

Do not require a favorable physical hypothesis outcome. Compare the exponential,
reflection, transmission and measured retention without fitting a scale to make
them match. A failed equality rejects that equality for the stated preparation,
region and time, not all nonlinear condensate theories. Finite-time localization
and bounded perturbations do not prove an eternal bound state. Dividing measured
energy by c² is an energy-equivalent proxy, not an independent derivation of rest
mass, inertia, spin, charge or self-confinement. Lossless transmission into a
region and subsequent trapping there are different processes; the latter could
require a specified capture channel, changing boundaries or dissipation.

External reference: [MIT, resonance and the S-matrix](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2013/resources/lecture-14/).
