> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Framed unknot — the framing transformer

Companion code for `papers/notes/Framing_Transformer_Spin_Parity.tex`, which
is itself a companion computation to `papers/notes/Mobius_Screw_Electron.tex`.

## What it computes

The Möbius-screw note models the electron as the framed unknot

```
gamma(phi) = ( (R + a cos(phi/2)) cos phi,
               (R + a cos(phi/2)) sin phi,
                a sin(phi/2) ),        phi in [0, 4 pi)
```

a `(p,q) = (2,1)` curve on the torus of radii `(R, a)`, framed by the torus
surface normal, and asserts `Sl = p*q = 2`.

This script evaluates every stage of the chain that turns that geometry into
a statement about spin:

| Stage | Object | What is checked |
|-------|--------|-----------------|
| framing | `U(phi)` = torus normal | `T . U = 0` identically |
| Călugăreanu–White–Fuller | `Sl = Tw + Wr` | twist and writhe integrals sum to the linking number |
| self-linking | `Lk(gamma, gamma + eps U)` | Gauss linking integral, at two offsets |
| adapted frame | `F = [T, U, T x U] : S^1 -> SO(3)` | proper rotation at every point |
| double-cover lift | `q : S^1 -> SU(2)` | whether the lift closes |

The decisive output is the holonomy `sigma = q(4pi)/q(0)`, which is `+1` when
the frame returns after one circuit and `-1` when it needs two.

## Results

| Quantity | Value |
|----------|-------|
| `Tw` | −1.033761 |
| `Wr` | −0.966239 |
| `Tw + Wr` | −2.000000 |
| `Lk(gamma, gamma + 0.10a U)` | −2.000000 |
| `sigma` (three independent routes) | −1.000000 |

So `|Sl| = 2` as the note claims (the sign records that the embedding as
parameterised is left-handed), and the frame loop is **spinorial** — its class
in `pi_1(SO(3)) = Z/2` is nontrivial.

The control family (round circles with `n` framing twists, `Wr = 0`) measures
the map `Sl -> sigma` directly and yields

```
sigma = (-1)^(Sl + 1)        equivalently   sigma = (-1)^(p+q)  for torus curves
```

which means the spin-relevant content of `Sl` is **its parity, not its
magnitude**: `Sl = 2` and `Sl = 0` lie in the same class. See the note for what
this does to the `Sl = 2 <-> g = 2` identification.

## Run

```bash
python3 code/framed_unknot/framing_transformer.py
```

Requires `numpy` only. Runtime ~1 min (dominated by the O(N²) Gauss double
integrals at N = 2000). Writes `docs/framed_unknot_results.json`.

---

## `moment_ratio.py` — the successor test, run

Asks whether the geometry can produce a g-factor at all. It cannot.

For charge `q` and mass `m` traversing the centerline once per period `T`, both
moments are proportional to the same vector area `A = ½ ∮ r × dl`:

```
mu = I·A = (q/T)·A        <L> = (m/T) ∮ r × dr = (2m/T)·A
mu / <L> = q/2m     =>    g = 1   exactly, for every closed curve
```

| curve | A_z / π |
|---|---|
| Möbius screw (2,1), a/R = 0.30 | +2.09000 |
| Möbius screw (2,1), a/R = 0.70 | +2.49000 |
| Möbius screw (2,1), a/R = 0.97 | +2.94090 |
| round circle, one turn | +1.00000 |
| round circle, two turns | +2.00000 |

The double winding is real — 2.09× a single loop — and useless, because the same
factor sits in `mu` and `<L>` and cancels. Same failure mode as the `Sl` kill: a
genuine 2 in the geometry that carries no information about `g`. Note `A_z` is not
even an invariant (2.09π → 2.94π across the throat sweep) while `Sl` does not move.

**No-go:** no model with charge and mass circulating at uniform `q/m` gives `g ≠ 1`,
whatever the winding, framing, twist, or throat. Obtaining `g ≠ 1` requires
decoupling the charge and mass distributions.

```bash
python3 code/framed_unknot/moment_ratio.py     # writes docs/framed_unknot_moment_ratio.json
```
