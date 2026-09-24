# Follow-up: discrete fission comparisons and chemical potential

Recorded after the primary gauge survey and before these follow-up solves.
The survey gives omega greater than E/Q at Q=1000,e=.12. This motivates a
direct comparison; it is not itself proof that splitting into two chosen
charges lowers energy.

At e=0,.08,.12 compute isolated Q=500,400,600 branches, using the Q=1000
solution as continuation seed. Compare E(1000) with 2E(500) and E(400)+E(600),
with the same potential, coupling, vacuum and infinity convention. Also
solve Q=999 and 1001 to check dE/dQ=omega by a centered difference.

Use the same continuum equations, R=40 and tolerance1e-8. Energy differences
describe infinitely separated products: positive mutual Coulomb energy
vanishes only as their separation tends to infinity. Even a lower final
energy does not compute a fission path, barrier, rate or instability.
Require each product solution to pass solver, virial and localization
checks before treating its energy as a localized endpoint. A failure to
find a cheaper endpoint in these two partitions proves nothing about all
partitions or nonradial stability.

Check the centered chemical-potential identity to relative tolerance 1e-5.
Save all outcomes. Record analytical vacuum Hessian and parameter-scaling
checks separately from numerical branch results.
