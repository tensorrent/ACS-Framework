# Specialist report: stressing the fixed-point classification

**STATUS: in progress**

**Mission.** Try to break the corpus's own fixed-point classification, logged at
`docs/Elimination_Ledger.md` L3263-3266:

> A free action forces periodicity globally and the result is locally unobservable. A
> fixed-point action forces it locally and the result is a physical scale.

A classification that has only ever been confirmed has not been tested. This report attempts
falsification on cases that had no part in building the table.

**Instrument.** `code/constraint_projection/gauge_stress.py` (asserts + `sys.exit`).

**Tiers.** T0 machine-CHECKED / T1 machine / T2 proved / T3 measured / T4 falsified.
Literature facts are cited as literature, not labelled measurement.

---

## 0. What exactly is being tested

The ledger sentence (L3263-3266) bundles two conditionals:

| | antecedent | mechanism | consequent |
|---|---|---|---|
| **R-free** | the action is free | periodicity forced **globally** (topology) | the result is **locally unobservable** |
| **R-fix** | the action has a fixed point | periodicity forced **locally** (smoothness at the fixed point) | the result is a **physical scale** |

Three things are left unstated by the prose, and every one of them is a place the
classification can be attacked:

- **A1 — which space?** "Free" is a property of an action *on a space*, and the four worked
  rows do not use the same kind of space. Mobius: a deck action on a surface. Spinor: `{±I}`
  on the state sphere `S^3`. Zeta: `s -> 1-conj(s)` on `C`. Schwarzschild: Euclidean time
  translation on the Euclidean manifold. The spinor row is the sharpest illustration of why
  this matters: `{±I}` is **free on states** and **trivial on rays** — the same group, the same
  system, opposite ends of the classification depending on which space you name. The table
  names no space.
- **A2 — "forced" is load-bearing and unenforced.** R-free's antecedent is not "free action"
  alone but "free action *that forces* a periodicity." An imposed-but-not-forced period on a
  free action (a compactification radius, a chosen temperature) is a free action with a
  perfectly observable dimensionful period. If "forced" is dropped, R-free fails immediately;
  so the word has to be carried, and the prose carries it only in passing.
- **A3 — "physical scale" vs "pure number."** In Schwarzschild the forced period `beta = 8*pi*M`
  carries a dimension. In the spinor row the forced period `4*pi` does not. The table reads as
  though the fixed point is what supplies the dimension, but `8*pi*M = 8*pi` (a pure number
  from the smoothness condition) times `M` (an input already present in the metric). The pure
  number is what the topology/smoothness supplies in *both* rows. What actually differs is
  **whether the period is a function of local data at all.**

### Falsification shapes accepted in advance

- **F1** a free action whose forced periodicity yields a local dimensionful observable
  → breaks R-free. (Candidate: theta-vacua.)
- **F2** a fixed-point action whose periodicity yields only a sign / pure number and no scale
  → breaks R-fix. (Candidate: conical intersection.)
- **F3** a periodic structure where "free vs fixed point" is not well defined, or where the
  answer flips with the choice of space → the table has no content there (boundary).
- **F4** a scale-producing non-free action with no periodicity at all → R-fix's converse
  is unsupported. (Candidate: Gribov.)

### The sharpened criterion this report will test instead

Because of A3 the report also carries a second, mechanical statement of the same intuition,
which is what the instrument actually measures:

> **C** — a periodicity is *fixed-point type* iff the period is a function of local data at
> the fixed point, and *free type* iff the period is independent of all local data.

`C` is checkable by differentiation: vary the local data, watch the period. Wherever the prose
table and `C` disagree, that disagreement is reported, because the disagreement is the finding.

## 1. theta-vacua / instantons

**Instrument.** `code/constraint_projection/gauge_stress.py::g1_theta_vacua`.
**Tier.** T1 machine (the band computation) + T2 proved (the structural argument).
The QCD numbers quoted at the end are **literature**, cited as literature, and are not
inputs to any assertion here.

### The model is not an analogy, it is the standard map

Jackiw; Callan-Dashen-Gross; Coleman (*The uses of instantons*) map QCD's vacuum structure
onto a one-dimensional periodic potential exactly:

| QCD | periodic potential |
|---|---|
| winding sector `\|n>` | well `n` of a lattice |
| large gauge transformation `T\|n> = \|n+1>` | translation `x -> x + a` |
| instanton (tunnels `n -> n+1`) | barrier penetration |
| `\|theta> = sum_n e^{i n theta}\|n>` | Bloch state |
| vacuum energy density `eps(theta)` | lowest Bloch band `E0(theta)` |
| topological susceptibility `chi_top` | `d^2 E0 / d theta^2` at `theta = 0` |

So the instrument diagonalises `H(theta) = -1/2 d^2/dx^2 + V0 cos(2 pi x)` in the plane-wave
basis, `H(theta)_{nm} = (theta + 2 pi n)^2/2 delta_{nm} + (V0/2)(delta_{n,m+1}+delta_{n,m-1})`.

**The action is free.** `T` acts on the winding sectors as `Z` translating itself: no fixed
point, quotient a circle. This is the Mobius/spinor column of the table, not the Schwarzschild
column.

### (a) the period is exactly `2 pi`, and it moves with nothing

```
||H|| ~ 3.158e+04   (largest kinetic diagonal, NPW = 40)

      V0    max|E0(th+2pi)-E0(th)|       / ||H||
     0.0                 2.220e-15     7.031e-20
     0.5                 2.000e-11     6.334e-16
     2.0                 3.067e-11     9.710e-16
     8.0                 2.045e-11     6.474e-16
    32.0                 2.716e-11     8.599e-16
   128.0                 1.117e-11     3.537e-16

worst relative period defect over all V0: 9.710e-16
```

*An in-flight correction.* The first run reported the **absolute** defect, `3.067e-11`, and a
tolerance of `1e-8` — which would have passed while hiding whether the number meant anything.
Varying the basis size at fixed `V0 = 2` gave defect `1.1e-12 -> 4.2e-12 -> 3.1e-11 -> 1.7e-10`
for `NPW = 10, 20, 40, 80`: the defect *grows* with basis size. Divided by `||H||` it is flat at
`~1e-15`. It is LAPACK backward error scaling with the matrix norm, not a failure of
periodicity, and the instrument now asserts on the **relative** defect at `1e-13`. The absolute
number alone was uninterpretable.

**Criterion C reads this as FREE type**: the period `2 pi` is independent of `V0`, of the mass,
of everything. And R-free's *mechanism* clause is confirmed — the free action does force the
periodicity, and forces it globally.

### (b) and the position on that circle is an energy

```
      V0           E0(0)          E0(pi)     W = bandwidth
     0.0      0.00000000      4.93480220         4.935e+00
     0.5     -0.00633080      4.68322906         4.690e+00
     2.0     -0.10087036      3.91010764         4.011e+00
     8.0     -1.51949242      0.56878732         2.088e+00
    32.0    -15.67276353    -15.47650941         1.963e-01
   128.0    -93.73900079    -93.73855349         4.473e-04
```

`W > 0` at every finite barrier. The vacuum energy depends on `theta`. In QCD this is precisely
`chi_top`, an **energy density** — intensive, surviving the infinite-volume limit — and through
it `theta` reaches the neutron EDM.

### (c) the control: a knob the antecedent cannot see

```
W(V0 = 0.5)  = 4.689560e+00     theta plainly observable
W(V0 = 128)  = 4.472932e-04     theta effectively unobservable
ratio        = 1.048e+04
```

This is what makes it a falsification rather than an anecdote. The free `Z` action is
**identical** in both rows. The forced period is `2 pi` in both rows. What decides whether the
consequent holds is the barrier height — the instanton action — and **R-free's antecedent
contains no barrier height.**

`V0 -> infinity` is the superselection limit: sectors decouple, the band flattens, `theta`
becomes a label with no consequence. `V0` finite is the tunnelling regime: `theta` is a coupling.

### The mission's question, answered

> *Decide precisely whether that breaks the table or whether `theta` is a superselection label
> rather than a smoothness-forced periodicity.*

**It is not a superselection label, and that is exactly why it breaks R-free.** A superselection
label is what `theta` becomes in the `V0 -> infinity` limit, where the answer is a flat band and
`theta` is unobservable. The physical case is the other limit. In QCD the knob is the light quark
mass: with a massless quark `chi_top = 0` and `theta` is unobservable and rotatable away; with
`m_u, m_d > 0` it is not. Same `pi_3(SU(N)) = Z`, same free action, same `2 pi` — and the
consequent flips on a quark mass.

**The deeper discriminant.** What actually controls R-free's consequent is whether the circle
coordinate is conjugate to a charge that is the **volume integral of a local density with
nonzero susceptibility**. `theta` is conjugate to `Q_top = int d^4x q(x)` with
`chi = int <q(x)q(0)> != 0`, so it reaches local observables. The spinor sign is conjugate to no
such thing. Freeness of the action does not see this distinction at all.

### Verdict — **F1, R-free's consequent fails**

| clause | status |
|---|---|
| antecedent: free action | holds (T2) |
| mechanism: periodicity forced globally, period `2 pi`, no local data | holds (T1, measured) |
| consequent: the result is locally unobservable | **fails** (T1, measured) |

Marked **T4 falsified** for the consequent clause of R-free as stated.
The mechanism clause is untouched and is confirmed here on a case that did not build it.

## 2. Aharonov-Bohm

**Instrument.** `gauge_stress.py::g2_aharonov_bohm`. **Tier.** T1 machine + T2 proved.
`h/e` is computed from CODATA `h` and `e` via `scipy.constants`, not quoted.

**Predicted row:** free, global, locally unobservable, visible only in interference.
**Measured row:** identical. The prediction holds. What AB breaks instead is assumption A3.

### The realisation

Configuration space `R^2` minus a point, `pi_1 = Z`, deck action on the universal cover free.
To get a spectrum, a tight-binding ring of `L` sites threaded by flux:
`E_k(theta) = -2t cos((2 pi k + theta)/L)`, `theta = 2 pi Phi / Phi_0`, `N` spinless fermions
filling the lowest `N`. `theta -> theta + 2 pi` maps `k -> k-1`, a relabelling.

### (a) the period is exact and carries no local datum

```
    L     N      t     max_theta |E(th+2pi)-E(th)|
    6     3   1.00                       2.220e-15
   10     5   1.00                       3.553e-15
   14     7   2.50                       1.421e-14
   22    11   0.30                       8.882e-16
   34    17   1.00                       1.066e-14
worst period defect: 1.421e-14
```

Machine precision, and independent of `L`, `N`, `t`. Criterion C: **free type.** Matches.

### (b) — and it is dimensionful. This is the finding.

```
Phi_0 = h/e = 4.135667697e-15 Wb
h = 6.626070150e-34 J s     e = 1.602176634e-19 C
```

`Phi_0` is built from universal constants and from **no property of the ring** — not radius, not
material, not beam energy. So it is a period that carries a dimension while depending on no local
datum.

That splits two things the prose runs together in A3. **"Free -> a pure number" is false.** The
statement that survives is "free -> a period independent of local data", which `h/e` satisfies
while being dimensionful. So the free/fixed contrast is *not* dimensionless-vs-dimensionful.
**Criterion C survives where the prose reading of A3 does not** — and C was this report's own
sharpening, so this is a correction to Section 0, not only to the ledger.

### (c) what "locally unobservable" actually means, measured

```
    L     N    max-min of E_tot        per site
    6     3        5.358984e-01    8.931640e-02
   14     7        2.253459e-01    1.609613e-02
   34    17        9.246558e-02    2.719576e-03
   86    43        3.653421e-02    4.248164e-04
fitted exponent:  amplitude ~ L^(-1.0072)
```

The total energy's flux dependence falls as `1/L`; the energy **density**'s falls as `1/L^2` and
vanishes in the thermodynamic limit. So "locally unobservable" does not mean invisible — the
persistent current is measurable — it means **not an intensive bulk property.** That is a
sharper statement than the ledger's, and it is the one that survives Section 1.

### (d) independent case, or the spinor row in different clothes?

**Same mechanism, different test.** Both are flat connections on a non-simply-connected space:
`F = 0` everywhere the particle can go, the holonomy is the whole content, visible only in
interference. Local unobservability comes from **the curvature vanishing on the accessible
region**, not from the action being free. On mechanism AB adds nothing.

It is an independent *test* in two respects the spinor row cannot reach: the holonomy is
continuously tunable (`pi_1 = Z`, dial the flux) where the spinor sign is pinned by
`pi_1(SO(3)) = Z/2`; and the period is dimensionful where `4 pi` is not.

### (e) G1 against G2 — the discriminant the table does not contain

`theta_QCD` and AB flux are both circle-valued parameters forced by free actions. One is
intensive and one is not:

| | conjugate charge | effect |
|---|---|---|
| AB | winding number of the particle's path — one global d.o.f. per ring | `O(1/L)` per site, measured above |
| QCD | `Q_top = int d^4x q(x)` — volume integral of a **local density** with `chi != 0` | intensive, survives `V -> inf` |

Freeness of the action does not see this distinction. **The variable that controls R-free's
consequent is whether the conjugate charge is a bulk density, and the table's antecedent does not
mention it.**

*Literature, cited as literature, used as no input above:* Tonomura et al., PRL **56**, 792
(1986) confirmed the AB phase with the field fully shielded by a superconducting layer; flux
trapped in those toroids is quantised in units of `h/2e` (Cooper pairing), so the observed
electron phase shifts were `0` or `pi`.

### Verdict — R-free holds; A3's "pure number" reading does not

| clause | status |
|---|---|
| antecedent, mechanism, consequent of R-free | all hold (T1/T2) |
| A3's implicit "free -> pure number" | **fails** — `h/e` is dimensionful (T2) |
| independent mechanism? | **no** — flat holonomy, as in the spinor row (T2) |

## 3. Berry phase at a conical intersection

**Instrument.** `gauge_stress.py::g3_conical_intersection`. **Tier.** T1 machine + T2 proved.

`H(R, phi, Delta) = R cos(phi) sx + R sin(phi) sy + Delta sz`. At `Delta = 0` the levels touch at
`R = 0`. The `SO(2)` rotating the parameter plane **fixes the origin**, so the prose table puts
this in the Schwarzschild column: forced locally, result a physical scale. Berry phase measured
as the gauge-invariant Wilson loop `W = prod_i <psi_-(phi_i)|psi_-(phi_{i+1})>`.

### (a) the phase is exactly `pi`, and depends on nothing

```
         R   nstep    ax    by           |W|             |arg W|
      0.01     400   1.0   1.0    0.98773866    3.14159265358979
      1.00     400   1.0   1.0    0.98773866    3.14159265358979
    100.00     400   1.0   1.0    0.98773866    3.14159265358979
      1.00       6   1.0   1.0    0.42187500    3.14159265358979
      1.00    2000   1.0   1.0    0.99753564    3.14159265358979
      1.00     400   1.0   7.0    0.95690304    3.14159265358979
      1.00     400   3.0   0.2    0.91132099    3.14159265358979

max |arg W| - pi  over every variation: 8.882e-16
```

Loop radius over four decades, a 35x anisotropy, discretisations from 6 steps to 2000 — the
phase is `pi` to 9e-16 in every one. (`|W| < 1` is a discretisation artifact of the **modulus**;
the phase is exact at any `nstep`, which is what quantisation means here.)

**So criterion C reads this case as FREE type** — the period depends on no local datum
whatsoever — **while the prose table reads it as FIXED-POINT type**, because the action fixes
the origin. **The two disagree.** This is the first case where the corpus's two statements of
its own intuition come apart, and C was this report's own sharpening in Section 0, so the
disagreement is internal on both sides.

The resolution is **A1 — which space?** The fixed point is a fixed point in *parameter* space;
the object that is periodic (the electronic eigenstate) lives in *Hilbert* space, where the
relevant `Z/2` holonomy action is free. Same system, two spaces, opposite rows. A1 was logged in
Section 0 as a gap in the prose; here it is the thing that decides the answer.

### (b) control — the fixed point is genuinely load-bearing

```
   Delta    |arg W| measured   pi(1 - D/sqrt(R^2+D^2))        diff
    0.00        3.1415926536              3.1415926536    8.88e-16
    0.50        1.7366287830              1.7366297074    9.24e-07
    1.00        0.9201502710              0.9201511845    9.14e-07
    3.00        0.1612159287              0.1612161739    2.45e-07

loop displaced so it does NOT encircle the degeneracy:
   |arg W| = 1.215e-16     (holonomy +1)
```

Gapping the intersection **unquantises** the phase — it becomes a continuous function of
`Delta/R`, matching the solid-angle formula to 1e-6. Moving the loop off the degeneracy kills it
entirely. So **R-fix's mechanism clause holds and is measured**: the fixed point is what forces
the period locally. This is a confirmation, and it is reported as one.

### (c) the mission's question — scale, or sign?

The observable consequence is the Longuet-Higgins effect: antiperiodic vibronic wavefunction,
half-odd-integer pseudorotational quantum number, `E_j = j^2/(2I)`.

```
         I    E_ground, j in Z    E_ground, j in Z+1/2           shift     shift * I
      0.50          0.00000000              0.25000000      0.25000000    0.12500000
      1.00          0.00000000              0.12500000      0.12500000    0.12500000
      4.00          0.00000000              0.03125000      0.03125000    0.12500000
     25.00          0.00000000              0.00500000      0.00500000    0.12500000
```

`shift * I = 1/8` exactly, for every `I`. **Only a sign.** The fixed point supplies the pure
number `1/8`; the scale `1/I` was in the problem before any Berry phase was computed.

### (d) — and that is A3's shape, now general

| row | forced content | where the dimension comes from |
|---|---|---|
| Schwarzschild | `2 pi` (no conical deficit) | `kappa`, a local geometric datum already in the metric |
| conical intersection | `1/8` (half-odd-integer `j`) | `1/I`, already in the vibrational problem |
| spinor | `4 pi` | nothing to multiply — angle is dimensionless |
| AB | `1` flux quantum | `h/e`, universal constants |
| theta-QCD | `2 pi` | nothing — `theta` is dimensionless |

In **every** row the forced content is a universal pure number, and any dimension in the period
is carried by the conjugate coordinate's own normalisation. `beta = 2 pi / kappa` is not the
fixed point producing a temperature; it is the fixed point producing `2 pi` and Euclidean time
already having dimensions. **"The result is a physical scale" is a statement about the conjugate
variable, not about the fixed point.**

### Verdict — **F2 (+F3), R-fix's consequent fails**

| clause | status |
|---|---|
| antecedent: fixed-point action | holds |
| mechanism: forced locally at the fixed point | **holds**, measured by gapping (T1) |
| consequent: the result is a physical scale | **fails** — a sign times a pre-existing scale (T1) |
| criterion C vs the prose table | **disagree** on this case (T1) |

Marked **T4 falsified** for the consequent clause of R-fix as stated.

## 4. Gribov ambiguity

**Instrument.** `gauge_stress.py::g4_gribov`. **Tier.** T1 machine (the toy) + T2 proved
(the transfer to Yang-Mills). Gribov/Singer/Zwanziger are cited as literature.

### The two non-freenesses have to be separated first

The mission's framing — *"the gauge action is NOT free (reducible connections have stabilizers),
so the table predicts a local physical scale"* — has a true premise. But two different things are
called non-freeness in this problem and they are not the same locus:

| | condition | property of |
|---|---|---|
| **stabiliser** | `D_mu[A] w = 0` (covariantly constant gauge parameter) | the **action** |
| **Gribov zero mode** | `d.D[A] w = 0` (Faddeev-Popov) | the **section** |

The second is strictly weaker. In the standard Christ-Lee toy the two loci coincide and the
distinction cannot be seen, so the instrument uses a model where they are deliberately separated:
`SO(2)` rotating `(x,y)` in `R^3` with `z` inert, and a **curved** section
`f = y - eps*z*(x^2 - y^2)`, i.e. `f/r = sin(th) - beta cos(2 th)` with `beta = eps*z*r`.

### (a) the horizon, from the exact roots

```
 beta = eps z r   copies   min |FP det| over roots
         0.9000        2                2.39639300
         0.9999        2                2.59787414
         1.0000        3                0.00000000
         1.0001        4                0.02449551
         1.5000        4                1.96045516
FP determinant at beta = 1 exactly: 1.837e-16
```

Copies jump `2 -> 4` exactly at `beta = 1`, and the FP determinant vanishes there. The new pair
is born as a tangency, which is why. (An in-flight note: a sign-change root scan reported
`min|FP| = 2.598` at the horizon and missed it entirely — a tangential double root produces no
sign change. The instrument uses the exact roots of the quadratic in `sin(th)` instead.)

### (b) the horizon is not where the fixed points are

```
    eps       z   horizon r_h = 1/(eps z)     fixed locus
   0.50    1.00                  2.000000           r = 0
   2.00    1.00                  0.500000           r = 0
   2.00    4.00                  0.125000           r = 0
   8.00    4.00                  0.031250           r = 0
```

Two measured facts:

1. **The horizon and the fixed locus are disjoint.** The horizon sits at `r_h > 0`, where every
   orbit is a full circle and every stabiliser is **trivial**. The horizon is not made of fixed
   points.
2. **The horizon moves with `eps` and the fixed locus does not.** `eps` is a parameter of the
   *gauge condition*. So the horizon does supply a scale — and that scale is a property of the
   **section**, not of the action and not of the space. Set `eps = 0` (a linear section) and the
   scale runs to infinity and the copies vanish altogether.

### (c) what the genuine fixed point supplies: nothing

In Yang-Mills the honest fixed points of the honest gauge action are the reducible connections —
`A = 0` above all, stabiliser the global colour group `G`. That is a bona fide fixed point of a
bona fide gauge action, and it **forces no periodicity** (there is no circle near it) and
**supplies no scale** (a stabiliser is a group; groups are dimensionless). R-fix read as
"fixed point ⟹ physical scale" returns nothing on the flagship infinite-dimensional gauge action.

### (d) — and R-fix's mechanism is vacuous here

R-fix's mechanism clause is "periodicity forced locally by smoothness at the fixed point." There
is **no periodicity in the Gribov problem at all.** The antecedent is satisfied, the mechanism has
nothing to act on, so whatever scale turns up cannot have arrived through R-fix.

*Literature, cited as literature, used as no input above:* Gribov, Nucl. Phys. **B139**, 1 (1978);
Singer, Commun. Math. Phys. **60**, 7 (1978) — no global gauge fixing exists, the gauge orbit
bundle being non-trivial; Zwanziger's horizon condition. The Gribov mass in the restricted gluon
propagator is defined in Landau or Coulomb gauge and is a **gauge-dependent** quantity — the same
conclusion the toy reaches independently, that the scale belongs to the section.

### Verdict — **F4, R-fix's converse unsupported**

| clause | status |
|---|---|
| antecedent: action not free | holds |
| mechanism: periodicity forced locally | **vacuous** — no periodicity exists |
| consequent: a local physical scale | delivered, but **by the section, not the fixed points** |

The finding is stronger than "R-fix's converse fails." It is that **satisfying R-fix's consequent
is not evidence for R-fix**, because a quantity with no invariant meaning — one that moves when
you change a gauge condition — can satisfy it.

## 5. Case of my own choosing — the irrational rotation

**Instrument.** `gauge_stress.py::g5_irrational_rotation`. **Tier.** T1 machine + T2 proved.

### The assumption, named and then lifted (Rule 9)

The four rows that built the table are actions on well-behaved spaces with **closed orbits**,
whose quotients are manifolds or orbifolds. Hold the group (`Z`), the space (`S^1`) and the kind
of map (a rotation) fixed, and lift only "well-behaved":

> `Z` acting on `S^1` by `x -> x + alpha` (mod 1).

- **`alpha = p/q` rational:** `n = q` acts trivially, so every point has stabiliser `qZ` — the
  action is **not free**. But no element outside the kernel has **any** fixed point. A period `q`
  is forced; the quotient is `S^1`, a manifold.
- **`alpha` irrational:** the action **is free**. Every orbit is dense, the quotient is
  indiscrete, and **no period is forced at all**.

### (a) freeness, measured

```
       N         golden       xN      Liouville       xN    13/34 (exact)
      10      5.573e-02   0.5573      9.991e-03   0.0999          5.9e-02
     100      5.025e-03   0.5025      1.000e-04   0.0100          0.0e+00
    1000      4.531e-04   0.4531      1.000e-04   0.1000          0.0e+00
  100000      5.961e-06   0.5961      9.000e-06   0.9000          0.0e+00
```

Irrational: never `0`, at any `N` — the action is free. But the value falls as `~c/N`, so no `n`
ever returns the circle to itself: **no period is forced.** Rational `13/34`: **exactly** `0` at
`n = 34` — not free, and a period *is* forced.

Both irrationals are free and their quantitative structure is not alike: the golden ratio sits
near `0.5/N`, the Liouville number lurches between `0.01/N` and `0.9/N`. Freeness is blind to it.

### (b) the quotient is not Hausdorff — measured

```
       N    max gap, golden        x N
      10       1.458980e-01     1.4590
    1000       1.186241e-03     1.1862
   50000       2.525061e-05     1.2625
```

The gap goes to zero: every orbit is **dense**. No two orbits can be separated by disjoint
saturated open sets, so the quotient topology is indiscrete — not Hausdorff, not even `T0`. There
is no smooth structure on which to impose anything and no continuous function on the quotient
except the constants. **R-free's mechanism clause — "forces periodicity globally" — has nothing
to force.**

### (c) the forced period is a nowhere-continuous function of `alpha`

Convergents `p_k/q_k -> golden`; `q_k` *is* the forced period of rotation by `p_k/q_k`:

```
     q_k      |p_k/q_k - golden|
      34               3.869e-04
      55               1.478e-04
      89               5.646e-05
     144               2.157e-05
     610               1.202e-06
```

Arbitrarily small changes in `alpha` send the forced period to `34, 55, 89, 144, ...` without
bound, and to *no period at all* on a dense set of full measure — while **freeness is constant
on each class.** A discrete, wildly discontinuous antecedent is being asked to control a quantity
that is neither.

### (d) the boundary this draws

The table offers two rows. This single one-parameter family already needs four, and lands in the
two that do not exist:

| mode | quotient | period forced? | table row |
|---|---|---|---|
| free **+ proper** | manifold | yes | Möbius, spinor, AB, θ — covered |
| free **but not proper** | non-Hausdorff | **no** | **none** |
| non-free, effective, isolated fixed locus | orbifold | yes, locally | Schwarzschild — covered |
| non-free, **non-effective**, no fixed point anywhere | manifold | yes, by the **kernel** | **none** |

The rational rotation is the sharper of the two gaps. It is not free, so the table routes it to
the fixed-point column and predicts a local physical scale. It has **no fixed points at all** —
the stabiliser is the same subgroup at every point — there is nothing local to impose smoothness
at, and the forced period `q` is a pure integer with no scale anywhere near it.
**"Not free" does not mean "has a fixed point", and the classification treats them as the same
thing.**

### (e) the same failure is what goes wrong in infinite dimensions (T2)

A manifold quotient needs more than freeness: the action must be **proper** and admit slices. The
irrational rotation is the smallest free-but-not-proper example, and its pathology — dense orbits,
indiscrete quotient — is exactly that of free actions of non-compact groups in infinite
dimensions, where orbits need not be closed. **"Free" was standing in for "free and proper"
throughout the table**, and all four constructing cases are proper, so the distinction never had
to be made.

### Verdict — **F3, a boundary**

On one family, with group and space held fixed, **freeness and forced periodicity are exactly
anti-correlated**: free ⟺ irrational ⟺ no period forced. The dichotomy is not exhaustive, "not
free" ≠ "has a fixed point", and "free" was doing the work of "free and proper".

## 6. Verdict

(pending)
