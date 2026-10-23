# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
RECONSTRUCTED 2026-10-22 from the ledger's description, NOT the original.

Original: `q3_scaling_test.py`, run 2026-06-06 on an external session machine and never
committed (docs/Elimination_Ledger.md:431, provenance note :14-21). This file was
re-authored from the ledger's prose and table only (docs/Elimination_Ledger.md:428-456,
"Target Q3 (d,q) scaling law -- FALSIFIED (T4)"). It is not a copy, it cannot certify
what the original computed, and agreement with the ledger's numbers is agreement with
the *recorded outputs*, not proof that the original was correct.

What the ledger states (and this file implements):
  * zeros computed directly with mpmath (ledger :431-432): zeta zeros + Dirichlet L zeros;
  * the degree-2 test object is the Dedekind zeta of Q(i) = zeta(s) * L(s, chi_-4),
    conductor q = 4 (ledger :432), so its zeros are the union of the two zero sets;
  * framework floor (2*pi*e)^d / q, standard floor 2*pi*e * q^(-1/d) (table, :438-442);
  * framework count N(T) = (dT/2pi) log(qT/(2pi e)^d) vs standard analytic-conductor
    count (dT/2pi) log(q^(1/d) T/(2pi e)) (ledger :445-447).

The FF06 paper adds the zero-finding method (papers/later_FF06_series/
The_Elimination_Ledger.tex:485-488): "mpmath Dirichlet-L zeros via Hurwitz-zeta
construction and Hardy-Z sign changes; zeta zeros from the first 10^5". Implemented as:
sign changes of the real Hardy function Z(t) = exp(i*theta(t)) L(1/2+it, chi), with
L from mpmath.dirichlet (a Hurwitz-zeta sum), on a 0.025 grid, refined by bisection.

Choices made here that neither source states (so a mismatch may be ours):
  * grid step 0.025 and bisection depth 40;
  * the sign-change count is checked by a DIFFERENT method, the argument principle
    N(T) = theta(T)/pi + S(T), S(T) = arg L(1/2+iT)/pi by continuous variation along
    2 -> 2+iT -> 1/2+iT (valid because Lambda(s) = Lambda(1-s) and Lambda is real on
    the real axis for a real primitive character);
  * the zeta count is taken from mpmath.zetazero and cross-checked against the
    committed table code/hp_knife_suite/data_zeros/riemann_zeros_100k.txt.

Seed convention 20260423 (nothing below is stochastic). Writes nothing; stdout only.
"""
import os

import mpmath as mp
import numpy as np

np.random.default_rng(20260423)  # house seed; no stochastic step in this script
mp.mp.dps = 20

HERE = os.path.dirname(os.path.abspath(__file__))
ZEROS_FILE = os.path.join(HERE, "..", "data_zeros", "riemann_zeros_100k.txt")
TWO_PI_E = 2 * mp.pi * mp.e

# Primitive real odd characters (chi(-1) = -1, so the gamma shift a = 1), as value lists
# indexed by n mod q for mpmath.dirichlet.
CHARS = {
    "L(chi_-4)": (4, [0, 1, 0, -1]),
    "L(chi_-3)": (3, [0, 1, -1]),
}
A_SHIFT = 1  # both characters are odd


def theta(t, q):
    """arg of (q/pi)^{s/2+a/2} Gamma((s+a)/2) at s = 1/2+it, continuous from t=0."""
    t = mp.mpf(t)
    return mp.im(1j * t / 2 * mp.log(q / mp.pi) + mp.loggamma((mp.mpf(0.5) + A_SHIFT + 1j * t) / 2))


def hardy_Z(t, q, chi):
    val = mp.exp(1j * theta(t, q)) * mp.dirichlet(mp.mpc(0.5, t), chi)
    return val  # real up to rounding for a real primitive character (root number 1)


def zeros_by_sign_change(q, chi, T, step=0.025):
    ts = np.arange(step, float(T) + step, step)
    vals = [hardy_Z(t, q, chi) for t in ts]
    max_imag = max(abs(mp.im(v)) for v in vals)
    re = [float(mp.re(v)) for v in vals]
    zs = []
    for i in range(len(ts) - 1):
        if re[i] == 0.0 or re[i] * re[i + 1] < 0:
            lo, hi = mp.mpf(ts[i]), mp.mpf(ts[i + 1])
            flo = mp.re(hardy_Z(lo, q, chi))
            for _ in range(40):  # bisection to ~1e-12
                mid = (lo + hi) / 2
                fm = mp.re(hardy_Z(mid, q, chi))
                if flo * fm <= 0:
                    hi = mid
                else:
                    lo, flo = mid, fm
            zs.append(float((lo + hi) / 2))
    return [z for z in zs if z <= T], max_imag


def count_by_argument_principle(q, chi, T, n_vert=400, n_horiz=2000):
    """N(T) = theta(T)/pi + S(T); S(T) = (1/pi) Delta arg L along 2 -> 2+iT -> 1/2+iT."""
    path = [mp.mpc(2, T * k / n_vert) for k in range(n_vert + 1)]
    path += [mp.mpc(2 - 1.5 * k / n_horiz, T) for k in range(1, n_horiz + 1)]
    args = [mp.arg(mp.dirichlet(s, chi)) for s in path]
    total, prev = mp.mpf(0), args[0]
    for a in args[1:]:
        d = a - prev
        d -= 2 * mp.pi * mp.nint(d / (2 * mp.pi))  # unwrap; steps are small vs pi
        total += d
        prev = a
    total += args[0]  # arg L(2) = 0 for these characters; kept for completeness
    return float(theta(T, q) / mp.pi + total / mp.pi)


def zeta_zeros_upto(T):
    out, n = [], 1
    while True:
        g = float(mp.im(mp.zetazero(n)))
        if g > T:
            return out
        out.append(g)
        n += 1


def framework_count(T, d, q):
    return d * T / (2 * mp.pi) * mp.log(q * T / TWO_PI_E**d)


def standard_count(T, d, q):
    return d * T / (2 * mp.pi) * mp.log(mp.mpf(q) ** (mp.mpf(1) / d) * T / TWO_PI_E)


def main():
    print("Q3 (d,q) scaling law -- RECONSTRUCTION (not the 2026-06-06 original)")
    print("=" * 78)
    rows = [("L(chi_-4)", 1, 4), ("L(chi_-3)", 1, 3), ("Dedekind zeta Q(i)", 2, 4)]
    floors = {}
    for name, d, q in rows:
        fw = TWO_PI_E**d / q
        st = TWO_PI_E * mp.mpf(q) ** (-mp.mpf(1) / d)
        floors[name] = (float(fw), float(st))

    T_ded = floors["Dedekind zeta Q(i)"][0]
    # zeros
    zeta_z = zeta_zeros_upto(T_ded)
    table = np.loadtxt(ZEROS_FILE)
    zeta_file_count = int(np.sum(table <= T_ded))
    l4, im4 = zeros_by_sign_change(4, CHARS["L(chi_-4)"][1], T_ded)
    l3, im3 = zeros_by_sign_change(3, CHARS["L(chi_-3)"][1], 10.0)
    ap4 = count_by_argument_principle(4, CHARS["L(chi_-4)"][1], T_ded)

    print(f"max |Im Z(t)| on the grid (should be ~0): chi_-4 {float(im4):.2e}, chi_-3 {float(im3):.2e}")
    print(f"zeta zeros <= {T_ded:.4f}: mpmath.zetazero {len(zeta_z)}, committed table {zeta_file_count}")
    print(f"L(chi_-4) zeros <= {T_ded:.4f}: sign-change {len(l4)}, argument principle {ap4:.4f}")
    print(f"first zero L(chi_-4) = {l4[0]:.6f}; first zero L(chi_-3) = {l3[0]:.6f}")
    print()

    n_actual = {
        "L(chi_-4)": sum(1 for z in l4 if z <= floors["L(chi_-4)"][0]),
        "L(chi_-3)": sum(1 for z in l3 if z <= floors["L(chi_-3)"][0]),
        "Dedekind zeta Q(i)": len(zeta_z) + len(l4),
    }
    first = {"L(chi_-4)": l4[0], "L(chi_-3)": l3[0], "Dedekind zeta Q(i)": min(zeta_z[0], l4[0])}
    print(f"{'L-function':<20}{'d':>3}{'q':>3}{'framework (2pie)^d/q':>22}{'standard 2pie q^-1/d':>22}"
          f"{'N_actual@fw floor':>19}{'first zero':>12}")
    for name, d, q in rows:
        fw, st = floors[name]
        print(f"{name:<20}{d:>3}{q:>3}{fw:>22.4f}{st:>22.4f}{n_actual[name]:>19d}{first[name]:>12.4f}")
    print()
    print(f"at T = {T_ded:.4f} (d=2, q=4):")
    print(f"  framework count  (dT/2pi)log(qT/(2pie)^d)      = {float(framework_count(T_ded, 2, 4)):.6f}")
    print(f"  standard count   (dT/2pi)log(q^(1/d)T/(2pie))  = {float(standard_count(T_ded, 2, 4)):.4f}")
    print(f"  actual zeros (zeta + L(chi_-4))                 = {n_actual['Dedekind zeta Q(i)']}")
    print(f"  framework floor / standard floor               = {T_ded / floors['Dedekind zeta Q(i)'][1]:.4f}")
    print()
    print("Ledger cells (docs/Elimination_Ledger.md:438-449) for comparison:")
    print("  floors 4.27/4.27, 5.69/5.69, 72.93/8.54; N_actual 0, 0, 51; first zeros 6.02, 8.04;")
    print("  framework count ~0, standard ~50, overshoot ~8.5x")


if __name__ == "__main__":
    main()
