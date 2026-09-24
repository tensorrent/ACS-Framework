# ACS charge audit: the binding model's missing conservation law

2026-09-23. **Completed scoped audit; no exact ACS charge identified for the
previous neutral scalar binding model.** All 24 recorded checks pass. This is
an exclusion of specific identifications under stated assumptions, not an
exclusion of ACS or all possible binding mechanisms.

The earlier [self-binding result](../self_binding/README.md) remains valid in
its real-plus-complex scalar model. Its applicability to the complete ACS
field content encounters three concrete obstructions:

1. A gauge-allowed holomorphic Delta quartic breaks the candidate continuous
   charge. It was absent from the historical short potential.
2. Even with that quartic set to zero, the surviving classical charge has
   nonzero mixed anomalies with the two weak gauge groups.
3. On the conventional neutral Delta vacuum, the surviving classical global
   combination assigns zero charge to the neutral Delta component. It cannot
   simply be the charged scalar used in the previous experiment.

These findings specify what an ACS completion must address. No interaction
has been deleted or new symmetry imposed in the source action to obtain a
preferred outcome.

## Source and scope

We use the canonical field representations
\(\Phi\sim(1,2,2)\), \(\Delta\sim(\overline{10},1,3)\),
\(\psi_L\sim(4,2,1)\), and physical right-handed
\(\psi_R\sim(4,1,2)\), with three families. For anomaly sums, the
right-handed fields are converted to left-handed conjugates. This avoids a
conjugation mismatch in the historical printed Lagrangian, which sometimes
labels Delta as 10. The canonical manuscript uses bar10, allowing the
contraction of Delta with two physical fundamental right-handed fermions.

The following sources were read and hashed:

- `papers/core_trilogy/Palatini_Gauge_Attractor.tex`, the scalar action around
  lines 2035–2053: field representations and norm cross-couplings.
- `code/acs_codebase/extras/task2_lagrangian.py`, around lines 178–198: both
  direct and conjugate bidoublet Yukawas, Majorana coupling, and the stated
  nonzero conjugate/direct ratio 2/3.
- Frontier branches S01, S08 and S23, and the actual invariant implementations
  recovered from two nested `Prior_Evidence.zip` archives inside
  `docs/frontier/2026-09-11/ACS_Frontier_Evidence.zip`.

The earlier exact completeness count of **4 real quadratics and 17 real
quartics** is inherited evidence. This run independently tests the phase
weights, gauge transformations and a second evaluation of the holomorphic
invariant; it does not rerun the Weyl-character completeness proof. Relevant
source snapshots and their full nesting/hash provenance are saved alongside
this report. Earlier claims that only the short displayed potential is
general are not used.

The audited transformations are continuous internal linear symmetries that
commute with the gauge action and preserve the canonical kinetic metric.
For one complex Delta irrep the connected scalar freedom is its phase; for
the one complex bidoublet, whose gauge representation is real, the two real
copies have connected SO(2) mixing, again the usual phase. Fermion flavor
generators are included. Gauge transformations, nonlinear/emergent symmetries,
spacetime symmetries, and topological charges are different possibilities;
this audit does not classify all of them.

## The exact classical obstruction

Let the family-uniform phase charges of Phi, Delta, left fermions and physical
right fermions be \((p,d,l,r)\). Invariance of the two Dirac Yukawas and the
Majorana term requires

\[
p-l+r=0,\qquad -p-l+r=0,\qquad d+2r=0.
\]

The first two force \(p=0\). Without the holomorphic Delta coupling, the
remaining solution is

\[
X(\Phi,\Delta,\psi_L,\psi_R)=(0,-2,1,1).
\]

Thus the **restricted action does have a classical candidate**. The two
Yukawas do not eliminate every charge: they eliminate the overall Phi phase.
This distinction matters.

However, the complete gauge-allowed scalar basis contains

\[
V_H=\kappa H(\Delta)+\kappa^*H(\Delta)^*,\qquad
H(e^{i\beta}\Delta)=e^{4i\beta}H(\Delta).
\]

Any nonzero complex \(\kappa\) imposes \(4d=0\) on a continuous charge.
The four constraints on \((p,d,l,r)\) have determinant of magnitude **16**
and rank **4**: only the zero continuous phase assignment survives.
Taking \(\kappa\) real does not help; CP invariance and continuous phase
invariance are different conditions. A scale-independent phase of a coupling,
such as the one-loop statement in branch S23, is also not a conserved field
phase charge.

Exactly two real quartic coordinates, Re H and Im H, break this particular X.
All the other 15 quartics preserve it because Phi has zero X charge. Imposing
independent Phi and Delta phases instead leaves 9 quartics, as in S08, but
those extra symmetries cannot be assumed while retaining arbitrary Yukawas.

The three-family phase system has rank **8** with H and rank **7** without it.
As an additional check, arbitrary Hermitian 3-by-3 left/right flavor generators
were solved at exact rational/complex invertible matrices. Both an aligned
\(\widetilde Y=(2/3)Y\) example and a nonaligned complex example give rank
**20 of 20** with H, and exactly the one X direction without H.
These two matrix examples are tests, not an exhaustive classification of
special flavor textures. The following trace argument is basis independent.

## The quantum obstruction is independent of flavor basis

For arbitrary invertible \(Y,\widetilde Y,F\), their infinitesimal
invariance conditions with Hermitian flavor generators \(T_L,T_R\) are

\[
-T_LY+YT_R+pY=0,\quad
-T_L\widetilde Y+\widetilde YT_R-p\widetilde Y=0,\quad
T_R^TF+FT_R+dF=0.
\]

Multiply by the appropriate inverse and take traces. For three generations,

\[
p=0,\qquad \operatorname{Tr}T_L=\operatorname{Tr}T_R=-\frac32d.
\]

Using the left-handed Weyl convention and \(T(\text{fundamental})=1/2\),
the mixed weak anomaly coefficients are therefore

\[
A_{SU(2)_L^2X}=2\operatorname{Tr}T_L=-3d,\qquad
A_{SU(2)_R^2X}=-2\operatorname{Tr}T_R=3d.
\]

For the normalized candidate \(d=-2\), these are **+6 and -6**. The SU(4),
mixed gravitational and cubic X sums cancel, but both weak coefficients do
not. The two gauge field strengths are independent, so equal gauge couplings
do not cancel these terms as an operator identity. Ordinary unit weak
instantons have X selection rules **+12 and -12** in this convention.

This is an anomaly of the proposed **global current**, not a claim that the
underlying gauge theory is inconsistent. Its implication is failure of exact
quantum X conservation. It does **not** determine a decay rate: such effects
can be strongly suppressed, and a lifetime needs couplings, a state and an
actual calculation. The anomaly machinery and zero-mode selection-rule
interpretation follow the standard derivation in
[Tong's gauge-theory notes, chapter 3](https://davidtong.org/pdfs/teaching/gauge-theory/gauge3.pdf).
The coefficients and trace obstruction above were computed in this audit.

Rank-deficient Yukawa matrices fall outside the inverse-matrix proof. A
protected exceptional texture would have to be explicitly derived and tested.
For example, removing both H and the Majorana coupling permits a Delta-only
phase with neutral fermions, avoiding this fermion anomaly. It also changes
the displayed Majorana/seesaw sector and is a different model assumption.

## Why the neutral vacuum hides the breaking interaction

Write Delta as three complex symmetric color matrices \(D_a\), a Cartesian
SU(2) triplet. One normalization of the invariant is

\[
H(D)=\sum_a\det D_a+
\frac12\sum_{a<b}\big[\det(D_a+D_b)+\det(D_a-D_b)\big].
\]

Equivalently, \(H=\mathbb E\det(\sum_a z_aD_a)\) for a real standard
Gaussian three-vector z. The determinant congruence law establishes SU(4)
invariance; rotational invariance of z establishes the SU(2) triplet part.
This also supplies an independent fourth-moment numerical evaluation.

For the neutral highest-weight rank-one direction, consider the explicit
transverse slice

\[
D_1=\operatorname{diag}(a,b,c,v),\quad
D_2=\operatorname{diag}(0,0,0,iv),\quad D_3=0.
\]

The exact result is **\(H=3vabc\)**. At \(a=b=c=0\), the value, first
derivatives and Hessian vanish, yet
\(\partial_a\partial_b\partial_cH=3v\ne0\). More generally, expanding
a determinant around a rank-one color matrix requires at least three
perturbation columns, explaining why this term is invisible to the quadratic
vacuum analysis. Restricting forever to that neutral direction would hide a
real interaction in the complete field space.

For the X-current convention used above, the classical source from this term is

\[
\partial_\mu j_X^\mu=-16\operatorname{Im}(\kappa H),
\]

in addition to the quantum anomaly contributions. This is a concrete example
of a constraint missed by a restricted observation: a higher-order coupling
can break conservation even when a quadratic stability calculation is clean.
It does not establish a general holonomy theory.

## Vacuum alignment and the charge carried by the actual mode

In the branch \(\kappa=0\), temporarily neglecting the anomaly, the neutral
Delta VEV has \(X=-2\) and gauged \(B-L=+2\). The vacuum-preserving
combination is

\[
B=\frac{X+(B-L)}4.
\]

It assigns **1/3 to quarks and 0 to leptons**. The Delta color components have
charges **-2/3 for the color-sextet pair, -1/3 for the mixed color/lepton
component, and 0 for the lepton/lepton neutral component**. All are derived
from the same bar10 weight convention. The holomorphic quartic carries
\(B=-2\), consistent with its charge-breaking role.

Consequently the conventional neutral condensate does not carry the
independent unbroken global charge. Its phase participates in gauge symmetry
breaking; it cannot be identified with the previous model's independent
global-charge rotor by simply freezing gauge fields. Colored scalar modes,
fermionic states or a genuine gauged soliton are separate candidate mechanisms
whose full energies and constraints would need calculation.

An exact Smith-normal-form check also tracks the finite remnants. The generic
classical family-uniform phase constraints give 16 field transformations;
8 are gauge-center actions, leaving a quotient of order 2. Imposing the
ordinary weak-instanton selection rules leaves precisely those 8 gauge-center
actions. This is a statement about the transformations of the listed local
fields, not a classification of all gauge bundles, line operators, generalized
symmetries or discrete anomalies. In any case, a finite remnant does not
supply the continuous fixed-Q functional of the prior soliton calculation.

## What this changes in the binding assessment

The earlier energy comparison, 838.16 versus 1000 at Q=1000, applies to the
specified scalar model with its exact U(1). It cannot yet be promoted to a
full-ACS stability statement. Once fermions and gauge fields participate,
the relevant threshold is the lowest admissible final-state energy carrying
the complete set of conserved charges. It need not equal the scalar-only
\(m_\infty|Q|\) threshold. Emission into other charge carriers and gauge
constraints must be included; their rates and spectrum have not been computed.

The direct neutral-Higgs/Delta interpretation is now a **specific failed
identification under the audited assumptions**. The finite-time scalar
retention data are unchanged. Productive continuations require one of the
following concrete inputs:

- A derived ACS symmetry/texture or additional field content that survives
  all interactions and anomaly checks, with a charged physical mode.
- A fully specified gauged or baryonic configuration, including gauge fields,
  fermionic channels and the appropriate energy threshold.
- An approximate-charge model with justified breaking coefficients, followed
  by measured leakage and a lifetime calculation.

None is selected automatically by a clean fit or by setting a troublesome
coupling to zero. This audit narrows the missing requirement instead of
expanding the previous reduced model into a claim it cannot support.

## Checks and reproduction

The record contains 24 passing checks: exact constraint ranks, exact flavor
examples, a basis-independent trace identity, anomaly sums, finite group
enumeration, vacuum charges, an exact cubic witness and numerical transform
checks. For 24 generic field samples, 72 phase-pair transforms and 24 gauge
transforms, the maximum relative discrepancies are approximately
\(3.02\times10^{-15}\) for gauge invariance,
\(4.43\times10^{-16}\) for phase covariance and
\(7.97\times10^{-17}\) for the independent invariant evaluations.

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/condensate_energy/charge_audit.py
```

Dependencies: NumPy and SymPy. The recorded run used NumPy 2.5.0 and SymPy
1.14.0. The script verifies the prior self-binding receipt before proceeding.
`protocol.md` was written before executing the audit. `results.json` contains
all outcomes and source digests; `archive-provenance.json` identifies the
nested source members; `receipt.json` seals this report and its evidence.
No manuscripts, standing rules, or prior experimental artifacts were modified.
