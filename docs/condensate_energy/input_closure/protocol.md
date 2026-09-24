# Input-selection source audit — 24 September 2026

This stage checks whether recovered proposals select the action's still-independent vacuum, flavor and scale inputs. It does not assume those proposals work, nor treat their failure as failure of every ACS construction.

Before calculation, the tests are:

1. Compute the real trace projection in `koide_from_vev.py` for the entire stated matrix domain. If it vanishes, test the explicitly different imaginary projection and determine its image and remaining freedom.
2. Reproduce `neutrino_mass_derivation.py` locally, then evaluate the exact invariant, gradient and Hessian at its proposed vacuum. Compare its Hessian with the Hessian of the stated squared potential and use a specified kinetic Gram matrix when comparing coordinate systems. Preserve negative eigenvalues.
3. Evaluate the actual block complement and its invertibility, and trace whether that result enters the printed mass. Check whether an unbroken color triplet can supply a singlet's mass-mixing vector without a further symmetry-breaking input.
4. Test the recovered Claude attachment's modular fixed point, spectral gap, convergence-to-cutoff implication and numerical constant substitution. Treat boundary conditions and field bundles as inputs. Compare its displayed action with primary GfE sources before transferring conclusions.
5. Preserve source versions, exact identities, numerical cross-checks, failed attempts, and coverage limits. Existing sealed calculations and source originals stay unchanged.

The repaired projection, Frobenius kinetic model and rectangular spectral examples are diagnostic constructions. They are not silently promoted to the ACS action. Algebraic tests apply to the declared source domains; finite numerical tests only cross-check them.

New standalone audit files have no existing callers. No existing function/class/method is edited. The ACS checkout was not available in the GitNexus index in the preceding stage; source scope is therefore established by explicit snapshots, not a claimed graph impact result.

The older `paper_a` ledger already records a distinct equal-VEV Yukawa no-go and an unresolved theta selector. These source failures must not be presented as discovering that historical uncertainty for the first time.
