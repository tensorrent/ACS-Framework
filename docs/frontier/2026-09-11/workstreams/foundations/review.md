# Independent bounded review of the physical workstream

**Outcome:** no material mathematical error was found in the three primary targets: the confined isospectral overlap family, the full-matrix seesaw bound/fixed-spectrum family, and the rectangular-barrier outgoing-pole certificate. I independently recertified the same outgoing disk with a different determinant representation, an explicitly differentiated first derivative, and an all-orders Cauchy remainder. This route shares Arb as its trusted interval-arithmetic backend. Numerical shooting is corroboration only.

All five physical check files and the report were read. The detailed review concentrates on the three targets above. The nuclear input data, external nuclear-data retrieval, finite-difference spectral convergence and all numerical sample grids were not independently regenerated in this review. The last section states the remaining coverage limits.

## 1. Confined isospectral family

The denominator \(w=1+tI(x)\) is strictly positive on the closed interval for every finite \(t>-1\), since \(0\le I\le1\). Thus the displayed potential is smooth and local for each allowed parameter. This argument does not require a uniform bound as \(t\to\infty\), and the report does not claim one.

For a base eigenfunction \(v\), the Wronskian identity used by the symbolic check has the correct sign:

\[
\frac{d}{dx}(u'v-uv')=(\mu-\lambda)uv.
\]

The integration constant is zero at the common Dirichlet endpoint. The transformed excited function and transformed ground function therefore satisfy the claimed differential equations. Both endpoint values vanish.

The complete-spectrum claim is stronger than testing finitely many eigenvalues, but its analytic justification is valid. For fixed allowed \(t\),

\[
(T_tv)(x)=v(x)-\frac{tu(x)}{1+tI(x)}\int_0^x u(y)v(y)\,dy
\]

is identity plus a bounded Volterra operator on the finite interval and is invertible. It maps the complete sine basis to eigenfunctions with the same eigenvalues; its image basis is complete. The ground image differs from the normalized ground state only by a nonzero scalar. Since the new regular Dirichlet operator is self-adjoint with discrete spectrum, there is no orthogonal missing eigenspace or extra eigenvalue. The explicit inverse parameter \(-t/(1+t)\), together with \(I_t=(1+t)I/(1+tI)\), supplies another way to check reversibility.

Normalization and overlap follow directly by \(z=I(x)\):

\[
\int_0^\pi u_t^2dx=\int_0^1\frac{1+t}{(1+tz)^2}dz=1,
\quad
\langle u,u_t\rangle=\sqrt{1+t}\frac{\log(1+t)}t.
\]

The continuous \(t=0\) value is 1; the squared overlap tends to zero as \(t\to\infty\). Positivity of the transformed ground state preserves its zero-node label; the usual ordered node counts follow from the regular Sturm operator and unchanged ordered simple spectrum.

The weak-concentration statement for every fixed \(L^2\) trial is also valid: outside any fixed endpoint neighborhood the transformed ground-state probability tends to zero; inside that neighborhood Cauchy–Schwarz bounds the overlap by the trial's arbitrarily small local \(L^2\) norm. This is a confined overlap obstruction. The report correctly does **not** assert preservation of outgoing scattering poles or of all nuclear observables.

## 2. Full seesaw bound and fixed-spectrum family

The number of designated light columns is essential: it equals the number of active rows, so \(A\) is square. From the active-block identity and unitarity,

\[
AdA^T=-BDB^T,\qquad AA^\dagger=I-BB^\dagger.
\]

When \(\eta=\|B\|_2^2<1\), multiplication by the invertible matrices \(A\) and \(A^T\) gives

\[
\|AdA^T\|_*
\ge\sigma_{\min}(A)^2\|d\|_*
=(1-\eta)\sum_i m_i.
\]

The transpose, rather than adjoint, causes no error: a complex matrix and its transpose have the same singular values. For each heavy column \(b_I\), \(\|b_Ib_I^T\|_*=\|b_I\|^2\), so the triangle inequality supplies the stated upper bound. If \(\eta=1\), the lower side is zero and the inequality remains valid. If \(t<1\), using \(\eta\le t\) and rearranging yields \(t\ge S/(M_{\max}+S)\); if \(t\ge1\), that weaker bound is automatic.

The fixed-spectrum example is exact linear algebra. Its row probabilities are nonnegative on the stated interval and sum to 1. Their signed mass average is

\[
m(1-t)+M q_+-M q_-=0.
\]

Orthogonal completion preserves signed eigenvalues \((m,M,-M)\); the negative eigenvalue is converted to a positive Takagi mass by a column phase. Hence the singular mass list remains \((m,M,M)\), the active-active entry vanishes, and heavy mixing is \(q_++q_-=t\). The polynomial light projector is correct whenever \(m^2\ne M^2\). This construction saturates the total-mixing lower bound at its left endpoint. It says nothing about a separate lower bound for each heavy state, which the report correctly disclaims.

A minor clarification was sent to the physical author: explicitly write \(0<m<M\) for this light/heavy construction, which also guarantees the nonzero projector denominator. The executed examples already satisfy it. The separate complex-orthogonal boost calculation is correctly labeled an effective coefficient construction, not an exact large-mixing spectrum.

## 3. Outgoing pole: analytic and interval review

The source transfer formula agrees with the fundamental solution initialized by \(u(0)=0,u'(0)=1\). Its final determinant is \(D(E)=u'(2)-i\sqrt E\,u(2)\), the outgoing condition.

In the original tiny enclosing box, \(E\) remains in the right half-plane and \(E-20\) remains strictly below the negative-real-axis cut, with imaginary distance about \(0.002208\), enormously larger than \(10^{-30}\). Thus the local square roots used in the jet computation are analytic throughout that box. The second formal-series coefficient is \(D''/2\); bounding it over an enclosing box is sufficient for the complex Taylor remainder on the disk. The original inequality has the correct normalization and direction.

I nevertheless used a distinct analytic certificate to avoid relying on that second-derivative jet. Set \(h=\sqrt{20-E}\), \(k=\sqrt E\), and write

\[
U=\cosh h\,\frac{\sin k}{k}+\frac{\sinh h}{h}\cos k,
\quad
V=h\sinh h\,\frac{\sin k}{k}+\cosh h\cos k,
\quad D=V-ikU.
\]

This is the same barrier transfer, expressed with square-root arguments of positive real part. The review script explicitly verifies that both arguments retain positive real part over an outer enclosing box of radius \(R=10^{-3}\). It differentiates the displayed elementary functions explicitly to enclose \(D'(E_0)\); it does not use a formal-series jet.

If \(|D|\le M\) on the outer circle, Cauchy's estimates bound **all** Taylor coefficients. On the inner circle of radius \(r=10^{-30}\), the entire tail from degree two is bounded by

\[
\sum_{n\ge2}|a_n|r^n
\le\frac{Mr^2}{R(R-r)}.
\]

The independently evaluated Arb bounds are approximately:

| Quantity | Validated value/bound |
|---|---:|
| \(|D(E_0)|\) upper bound | \(1.276474\times10^{-34}\) |
| \(|D'(E_0)|\) lower bound | \(10.64997325885\) |
| Outer-circle \(|D|\) upper bound | \(0.031620244\) |
| All-orders Cauchy tail upper bound | \(3.162025\times10^{-56}\) |
| Rouché left side | \(1.276474\times10^{-34}\) |
| Rouché right side | \(1.064997\times10^{-29}\) |

The strict interval comparison passes at 180 bits. Therefore \(D\) has exactly one zero, counted with multiplicity, inside the same stated disk. Its imaginary part is strictly negative. This is a simple outgoing benchmark resonance. At a zero, \(U\ne0\), since otherwise both final Cauchy data would vanish, contradicting invertible propagation from \((0,1)\). Thus the corresponding incoming determinant \(V+ikU=2ikU\) does not vanish there, so the usual outgoing scattering denominator is not canceled by that numerator.

The independent certificate is in `checks/physical_review_certificate.py`; `run_physical_review.py` appends portable source snapshots, stdout/stderr, result JSON and a hashed receipt. The successful persistent record is `attempts/physical_review_20260911T223212445087Z/`. An immediately preceding direct invocation also passed before the receipt-producing replay. Both analytic certificate constructions share Arb/python-flint as the trusted arithmetic implementation. Neither certifies the separate Woods–Saxon/Coulomb nuclear poles.

## 4. Other checks and review limits

I read the remaining two checks and checked the displayed algebra for branch-width conversion, independently bounded channel feasibility, log-preformation differential, magnetic moments under common rigid rotation, and the capacitance/self-energy scaling. No material algebraic error was found in those formulas under the named positivity, channel-independence and kinematic assumptions.

A second minor wording clarification was sent to the physical author: the saturated design matrix spans arbitrary width vectors only for **unrestricted** nuisance \(\log P_i\). With \(P_i\le1\), the same null direction establishes local nonidentifiability when the varied parameters remain feasible; it does not remove the separate feasibility inequalities. The report's later feasibility section already makes the correct restriction.

This review did not independently establish the accuracy of the inherited nuclear grid, retrieve evaluated branching data, repeat the finite-difference mesh eigenvalues, rerun every random seesaw/linear-program/moment sample, audit the LNHB search receipts, or supply a microscopic nuclear/electron model. Those limits do not affect the exact counterfamilies or the newly rerun rectangular-barrier certificate, but they remain important limits on physical conclusions.

## Reviewed identities

The reviewed physical versions are copied in the persistent review attempt. Their SHA-256 values are:

| Physical file | SHA-256 |
|---|---|
| `report.md` | `5b5fdacbf7c55ac2461003df43f2a09dae8e5a2ad305877fab98bfc8f8064265` |
| `checks/isospectral_overlap.py` | `fc7cb380342c26f4d3175a7688940fd8fa4f192d9cf1a706118158737b83c740` |
| `checks/flavor_boundaries.py` | `c6f3ecee83cca6c0c2910a2a4b7e259b3bfcd3965841fd265663f31f1fce7c11` |
| `checks/outgoing_certificate.py` | `8d2edaf2ad2d458f6a565c979b82ad204bc363d66453f0177cb19fe454e736ce` |
| `checks/nuclear_identifiability.py` | `4ec5603e19b043a27df167649108841470002a4441fd79f2964d4b2e0e3d4a13` |
| `checks/moment_capacitance.py` | `eb70cd7bdca156515a31ed13fe53f012ce7175c55e20cd8a8fec0ae930414c0e` |

The independent review-certificate script has SHA-256 `34eebbf5f691f5624b7b2685495cd7c394bbce8fd318b3c9e45bbb1524a9146f`. This is a bounded review of those versions; later edits need their own identity and scope assessment.
