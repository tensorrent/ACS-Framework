# Dynamical qualification and mechanism controls

Registered after the polished stationary solve, before time evolution. Use the
eight cases and numerical tolerances in protocol.md. Reference profiles are
the Newton-qualified coarse/fine solutions; preserving the original optimizer
failure is part of the evidence chain.

Specify the radial perturbation as f -> f[1+epsilon exp(-(r-4)^2/4)]. Recompute
omega=Q/integral f^2 only for initialization so charge is unchanged. Initial
energy changes and must be measured, not renormalized. Track all two-field
gradient, kinetic and potential contributions and signed charge inside radius15.

Two additional mechanism controls, added before running them:

- Set the reference field's initial velocity to zero (Q=0), leaving the prepared
  spatial profiles. Evolve the same equations. A finite-time oscillon is not
  ruled out; do not make immediate dispersal a success condition.
- Fix the condensate at its vacuum value chi=1 throughout, retaining the initial
  charged-field profile and charge. This deliberately different one-field control
  has potential |q|^2/2+b|q|^4/4 and no self-generated well. Its own Hamiltonian
  is conserved. Report its initial energy and residence, without treating it as
  the same physical theory or as an external-work-free formation protocol.

Total10 runs. For Q=0, report absolute charge drift divided by max(1,abs(Q0)).
All physical outcomes are measurements; only numerical errors have pass gates.
