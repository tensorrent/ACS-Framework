# Gauged branch and competing carriers — prospective protocol

Recorded before the runs in this directory. This is a selected classical
action and vacuum, not a derivation of the ACS vacuum or its coefficients.
Prior records remain unchanged. Every solver outcome, including failures and
delocalized finite-domain solutions, is retained.

## Questions

1. Does the previous scalar bound branch survive adding its complete radial
   electric field and the Gauss constraint?
2. Can that charge be an existing ACS gauge generator, without gauging the
   anomalous global X or dropping a gauge-required interaction?
3. Does binding relative to the selected scalar's free waves imply binding
   relative to all fields in that vacuum? Compute charges and vacuum masses
   before drawing that conclusion.
4. Which parameters and conversion to physical units remain unselected by
   the source action? An allowed counterexample is sufficient to disprove
   a universal conclusion from representation content alone.

## Model and boundary conditions

Use the earlier canonical model with b=2 sqrt(3)/27, replacing ordinary
q derivatives by D_mu=partial_mu-i e A_mu and adding -F_mu_nu F^mu_nu/4.
For q=f(r) exp(i omega t), Omega=omega-e A0, solve

    chi''+2chi'/r = chi(chi^2-1)+chi f^2
    f''+2f'/r = (chi^2-Omega^2)f+b f^3
    Omega''+2Omega'/r = e^2 f^2 Omega
    Q'(r) = 4 pi r^2 Omega f^2.

At the center impose zero radial derivatives and Q(0)=0. At radius R impose
chi=1, f=0 and Q(R)=Q_target. Reconstruct the infinity frequency as
omega=Omega(R)+R Omega'(R). The omitted exterior is a vacuum Coulomb
field; include its energy e^2 Q^2/(8 pi R), using the independently measured
Gauss flux for the primary energy evaluation. A hard finite-domain f=0 is
only an approximation, checked by increasing R and inspecting tails.

Independently check Gauss flux, T+E_electric=omega Q/2 and
G+3V-3T-E_electric=0, including the exterior field. E<Q tests binding
only against unit-mass free q waves. Require omega<1, small tails, and
domain convergence before calling a profile localized.

## Survey and qualification

Continue Q=1000 from the existing e=0 reference at e=0,.02,.04,.06,.08,
.10,.12,.14,.16,.18,.20,.25. Repeat at Q=300 and 3000 using intermediate
charge continuations at e=0 as needed. Failed or nonlocalized cases do not
prove nonexistence of other branches. Charge/coupling scan values are test
inputs, not physical fitted parameters.

Baseline R=40, BVP tolerance 1e-7, maximum 20,000 nodes. For each solution
record the numerical solver status and actual residual, all energy terms,
Gauss and virial residuals, frequency, tail and radius enclosing 90% of Q.
Keep finite-domain results even when the frequency fails localization.

Reference qualification at Q=1000, e=0,.04,.08: successful solve, maximum
BVP residual <1e-5, relative Gauss and charge errors <1e-5, integrated
energy identity and virial residual <1e-4. Compare e=.08 and .12 to R=60
and a tighter R=40 solve: energy/frequency differences <1e-3 and outermost
five-unit charge fraction <1e-6 are required for a localization claim.
If .12 is not localized, retain it without such a claim.

Independent finite-volume fixed-charge energy minimization uses exact
linear elimination of the electrostatic potential at each trial profile,
with the Coulomb boundary energy included. Compare e=0,.08,.12 at dr=.1
and .05, R=40. Require weighted-gradient infinity norm <1e-5 and fine-grid
energy relative difference <1e-3 to the BVP. Differences should decrease
under refinement. Verify analytic gradient and Hessian with finite
differences before trusting the minimization. If Newton minimization fails
for a non-minimum branch, preserve that finding rather than change gates.

## Field and carrier contract

Candidate selected classical embedding: Phi=chi I2/2, D1=D2=0,
D3=q E44/sqrt(2), A0 along canonical T15=diag(1,1,1,-3)/(2sqrt(6)).
Verify normalized kinetic terms, T15 weight, other gauge current
projections and the selected invariant norm potential. Effective e is the
product of g4 with the representation weight, not an independently gauged
global X. Check the holomorphic Delta quartic and its full first derivative
on this rank-one slice. Its vanishing value alone is insufficient.

Compute the full 21-generator scalar vacuum gauge-mass Gram at
(Phi=I2/2, Delta=0). Compute charges of omitted vector and fermion
components under T15. A free channel is only a kinematic threshold,
not an emission rate or a demonstrated nonlinear instability. A massless
charged omitted sector invalidates using E<Q as a full-theory stability
certificate. Quantum confinement is outside this classical calculation.

For massive candidate fermion carriers report both total-dispersal and
infinitesimal-emission thresholds, with all normalization factors stated.
Do not assign masses, Yukawas or a physical time scale absent source
selection. Do not identify this vacuum with conventional neutral Delta
breaking, or the T15 charge with physical electromagnetic charge.

## Scope controls

No full nonlinear gauge evolution, nonradial proof, quantum emission rate,
or physical particle identification is claimed. Additional scalar couplings
are selected, not proved absent. The allowed full action may change the
vacuum, scalar masses and branch. The final assessment must distinguish
the reduced result, the full-field carrier obstruction and missing input.
