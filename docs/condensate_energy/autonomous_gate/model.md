# Candidate action, energy exchange and stationary-state obstruction

This document defines an added model, not an action extracted from the
Klein-foam manuscripts. Its purpose is to isolate whether autonomous backreaction
is enough to supply the missing capture/binding mechanism in the existing toy.

## Explicit Hamiltonian

Let B(x) be the indicator of [4,5] on the half-line, with Phi(0,t)=0. The field
is complex and classical, and a is one real mechanical coupling coordinate.
Set g,M,K>0 and

\[
E=\frac12\int_0^\infty\left(|\Phi_t|^2+|\Phi_x|^2+ga^2B|\Phi|^2\right)dx
 +\frac12 M\dot a^2+\frac12 K(a-1)^2.
\]

The equations derived from kinetic minus potential energy are

\[
\Phi_{tt}=\Phi_{xx}-ga^2B\Phi,\qquad
M\ddot a=-K(a-1)-ga I,\quad I=\int B|\Phi|^2dx.
\]

The gate begins at a=1, adot=0. Its mechanical energy initially vanishes;
the incoming field's full energy, including interaction with the gate, is
normalized once. The coordinate may cross zero; it is not identified with a
physical aperture radius. The potential ga² remains nonnegative. A single
coordinate responds to the integrated field across the barrier, an assumption
of this reduced mechanical model, not a derivation of relativistic foam dynamics.

When the wave first meets a=1, its added force is -gI and initially lowers a.
The restoring force can reverse that motion. No closure time or phase detector
is prescribed. The restoring strength and inertia are independent inputs.

## Exact continuum budget

With J=-Re(conj(Phi_t) Phi_x), the field satisfies

\[
\partial_t e+\partial_xJ=ga\dot a B|\Phi|^2,\qquad
\frac{dE_{\rm gate}}{dt}=\dot a\{M\ddot a+K(a-1)\}=-ga\dot a I.
\]

Consequently d(E_field+E_gate)/dt=0 when there is no boundary flux at infinity.
For the finite simulation box the Dirichlet endpoints likewise carry no flux;
large-domain and remote-tail checks avoid confusing wall return with confinement.
The local trap budget includes both flux through x=5 and the work density above.
Gate energy and trapped field energy are distinct observables.

The energy is nonnegative. For total initial energy E0,
|a-1|<=sqrt(2E0/K) and |adot|<=sqrt(2E0/M). These bounds prevent unbounded gate
motion; they do not imply localization of the field. Gate energy remaining after
a pulse is excitation of a degree of freedom that was supplied in the model.

## Exact obstruction to a stationary localized harmonic state

Suppose a=a_star is constant and Phi(x,t)=u(x) exp(-i omega t), with real omega
and nonzero u in L2. Because |Phi|² is constant in time, equilibrium requires

\[
a_* = \frac{K}{K+gI},\qquad 0<a_*\le1.
\]

The spatial equation is

\[
\left(-\frac{d^2}{dx^2}+g a_*^2 B\right)u=\omega^2u.
\]

This is precisely the compact nonnegative barrier operator excluded by the
[previous half-line argument](../capture_stability/README.md): an oscillatory
exterior at positive squared frequency cannot be square-integrable; the zero
case is affine outside and also forced to vanish; nonnegativity excludes negative
eigenvalues. ODE uniqueness completes the argument. Thus **no nonzero localized
harmonic field with a stationary gate exists for any g,M,K>0 in this model**.

This is an analytic statement under explicit assumptions, not an extrapolation
of the numerical sweep. It does not exclude every time-dependent joint field/gate
solution. A long-lived oscillating trajectory must be assessed separately;
finite-time numerical residence is not a proof of an infinite-time breather.
The zero-field equilibrium and mechanical oscillations with vanishing field are
not counterexamples to the claim about a nonzero localized field.

## Eliminating a in equilibrium does not hide an attractive well

At fixed I, minimizing the interaction plus restoring potential gives

\[
V_{\rm eff}(I)=\frac{KgI}{2(K+gI)},\qquad
\frac{dV_{\rm eff}}{dI}=\frac{g}{2}\left(\frac{K}{K+gI}\right)^2>0.
\]

The barrier softens as the field increases. It never becomes an exterior gap
or a negative potential. This equilibrium elimination is not the exact transient
dynamics at finite M; it diagnoses the stationary claim only.

## Transfer record and ACS consequence

Mechanism: mutual field/geometry energy exchange. Related established machinery:
Hamiltonian field/mechanical backreaction, as surveyed in
[Aspelmeyer, Kippenberg and Marquardt, *Cavity Optomechanics*](https://arxiv.org/abs/1303.0733).
The equations here are an independently specified toy, not their optical model
and not experimental evidence for Klein foam. The physical transfer remains a
candidate; reproducible numerical checks qualify only its implementation.

Adding a reciprocal gate force closes the external-work accounting gap but
does not close the stationary-binding gap. To obtain a stationary localized field,
an ACS completion must alter at least one premise of this obstruction—such as
the open massless exterior, the compact nonnegative barrier operator, or the
stationary single-frequency ansatz—and specify the physical reason. Changing
premises by choice is not itself a derivation of those changes or of particle mass.

No inference from this toy has been promoted into manuscripts or standing rules.
