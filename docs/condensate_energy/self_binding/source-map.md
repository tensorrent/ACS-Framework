# Source-to-model map and the remaining ACS condition

The polynomial ingredients are present in the work. Their identification with
the reduced model's fields and charge has not been derived.

1. `papers/core_trilogy/Palatini_Gauge_Attractor.tex`, near lines2040–2053,
   contains symmetry-breaking scalar terms and the norm cross-coupling
   alpha1 Tr(Phi†Phi) Tr(Delta†Delta). These motivate testing a condensate that
   changes another field's propagation threshold. They do not fix the reduced
   model's parameters g=lambda_chi=v=1, nor identify a specific radial field
   component with either chi or q.
2. `code/acs_codebase/extras/task2_lagrangian.py`, Higgs sector near lines129–164,
   supplies the kinetic/potential structure; fermion terms near lines178–188
   include both Phi and its conjugate bidoublet. These terms matter for charge.
3. `docs/frontier/2026-09-11/Branch_Catalog.json`, branches S01 and S08, records
   a larger scalar invariant space than the older restricted potential and
   explicitly says extra phase symmetries must be selected and justified.
   The new test therefore cannot silently drop every phase-breaking term.

## A specific obstruction to a too-easy identification

Under an overall Phi phase with charge q_Phi, Phi-tilde has charge -q_Phi.
Let the left/right fermions have charges q_L,q_R. Invariance of both displayed
Yukawa terms requires

  -q_L + q_Phi + q_R = 0,
  -q_L - q_Phi + q_R = 0.

Subtracting forces q_Phi=0. Thus the required nonzero conserved q-number cannot
simply be called the Higgs bidoublet's overall phase while retaining both generic
nonzero Yukawa terms. This does not rule out a different collective charge,
component assignment, gauge completion or protected sector. Any such proposal
must give its actual transformation law and interactions.

For the tested model Q=integral(x y_t-y x_t), where q=x+iy. A phase-invariant
potential gives zero integrated charge source. Adding epsilon(x²-y²)/2 yields
Q_t=integral2 epsilon x y, absent boundary flux. It breaks the conservation law
used in the binding-energy argument. A surviving framing parity or a geometric
loop is not automatically this continuous Noether charge.

## The vacuum scale is still an input

The older `higgs_potential.py` proposes a norm proxy with quadratic coefficient
||F-G||²-||[F,G]||². With F=diag(1,-1,0,0) and G the01 antisymmetric generator,
common rescaling by a gives4a²-8a⁴. Its sign changes unless coefficient and
kinetic normalization are supplied consistently. This observation does not
prove physical symmetry breaking impossible. It prevents treating the proxy
alone as a normalization-independent derivation of the chosen physical vacuum.
The canonical manuscript itself notes incomplete kinetic matching near lines2020.

## What is now concrete

The three-dimensional mechanism has an explicit positive Hamiltonian, no
prescribed spatial well, a dynamically adjustable condensate, and a conserved
charge. A reference localized solution has total energy below free charged
waves after including the condensate deformation energy. The mathematical
obstruction from the earlier massless open-exterior model no longer applies:
the exterior vacuum gives a nonzero propagation threshold.

The remaining ACS identification is a precise condition: find the action's
protected charge and the field/coupling map, or explicitly study the lifetime
when its proposed charge is only approximate. The current evidence is a valid
reduced-model mechanism, not a derivation of the full gauge theory's particles.
No source manuscripts or standing rules have been changed.
