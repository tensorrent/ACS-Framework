#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
THE EQUATION THAT SOLVES THE RIEMANN CURVATURE TENSOR (Palatini / ACS Layer 2)
==============================================================================
Paper A (Colour from Gravity) treats the vierbein e^a_mu (Form) and the spin
connection omega^{ab}_mu (Function) as INDEPENDENT fields — the first-order
Palatini formulation.  In that language the Riemann curvature tensor is the
*second-order ACS coupling*: the bracket of the connection with itself,

    R^{ab} = d omega^{ab} + omega^a_c ^ omega^{cb}          (curvature 2-form)

This module states, in one place, the equation that actually SOLVES that
tensor, and verifies it end-to-end on the canonical vacuum solution.

THE EQUATION (two field equations of the Palatini action
              S = ∫ eps_{abcd} R^{ab} ^ e^c ^ e^d):

  (1)  CONNECTION equation  (vary S w.r.t. omega):
           D e^a = de^a + omega^a_b ^ e^b = T^a = 0
       Torsion vanishes.  Solving T^a = 0 forces metric compatibility
       ∇_mu g_{alpha beta} = 0 and pins omega to the Levi-Civita value
       omega = omega(e).  In coordinate form this IS the Christoffel symbol:

           Gamma^rho_{mu nu} = 1/2 g^{rho lambda}
                               (∂_mu g_{lambda nu} + ∂_nu g_{lambda mu}
                                - ∂_lambda g_{mu nu})

  (2)  With omega solved, the curvature 2-form becomes the metric Riemann
       tensor in components:

           R^rho_{sigma mu nu} = ∂_mu Gamma^rho_{nu sigma}
                                - ∂_nu Gamma^rho_{mu sigma}
                                + Gamma^rho_{mu lambda} Gamma^lambda_{nu sigma}
                                - Gamma^rho_{nu lambda} Gamma^lambda_{mu sigma}

  (3)  VIERBEIN equation  (vary S w.r.t. e):
           eps_{abcd} R^{ab} ^ e^c = 0   <=>   G_{mu nu} = R_{mu nu} - 1/2 g_{mu nu} R = 0
       In vacuum this is R_{mu nu} = 0 — the Einstein equation.

So "solving the Riemann tensor" = solve (1) for the connection, substitute into
(2) to get R^rho_{sigma mu nu}, and impose (3) for the on-shell (vacuum) field.

VERIFICATION (Schwarzschild, the canonical vacuum solution), all symbolic:
  * ∇g = 0 for the solved connection            (metric compatibility, eq. 1)
  * R_{mu nu} = 0                                (vacuum Einstein, eq. 3)
  * curvature is NOT trivial: Kretschmann scalar K = R_{abcd}R^{abcd} = 48 M^2 / r^6
    (the exact, textbook closed form — proves R itself is nonzero and correctly built)
  * pair + first Bianchi algebraic symmetries of R_{rho sigma mu nu}

No physical input beyond the metric; standard GR, exact, seed-independent.
"""

import sympy as sp


def _simp(x):
    """Robust reduction: plain simplify leaves some trig residuals (e.g.
    sin(2th)tan(th)+cos(2th)-1), so fold in expand_trig + trigsimp."""
    return sp.simplify(sp.trigsimp(sp.expand_trig(sp.simplify(x))))


def _iszero(x):
    return _simp(x) == 0


# ═══════════════════════════════════════════════════════════════════
# Generic solver: takes a metric g_{mu nu}(x), returns the objects in
# equations (1)-(3) above.  This is the "equation to solve the Riemann
# tensor" made executable.
# ═══════════════════════════════════════════════════════════════════

def christoffel(g, coords):
    """Eq. (1) solved: Levi-Civita connection Gamma^rho_{mu nu} from the metric."""
    n = len(coords)
    ginv = g.inv()
    Gamma = [[[sp.Integer(0)] * n for _ in range(n)] for _ in range(n)]
    for rho in range(n):
        for mu in range(n):
            for nu in range(n):
                s = sp.Integer(0)
                for lam in range(n):
                    s += ginv[rho, lam] * (
                        sp.diff(g[lam, nu], coords[mu])
                        + sp.diff(g[lam, mu], coords[nu])
                        - sp.diff(g[mu, nu], coords[lam])
                    )
                Gamma[rho][mu][nu] = _simp(s / 2)
    return Gamma


def riemann(Gamma, coords):
    """Eq. (2): R^rho_{sigma mu nu} = ∂_mu G^rho_{nu sig} - ∂_nu G^rho_{mu sig}
                                      + G^rho_{mu lam} G^lam_{nu sig}
                                      - G^rho_{nu lam} G^lam_{mu sig}."""
    n = len(coords)
    R = [[[[sp.Integer(0)] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for rho in range(n):
        for sig in range(n):
            for mu in range(n):
                for nu in range(n):
                    term = (sp.diff(Gamma[rho][nu][sig], coords[mu])
                            - sp.diff(Gamma[rho][mu][sig], coords[nu]))
                    for lam in range(n):
                        term += (Gamma[rho][mu][lam] * Gamma[lam][nu][sig]
                                 - Gamma[rho][nu][lam] * Gamma[lam][mu][sig])
                    R[rho][sig][mu][nu] = _simp(term)
    return R


def ricci(R, coords):
    """Contraction R_{sigma nu} = R^rho_{sigma rho nu}."""
    n = len(coords)
    Ric = sp.zeros(n, n)
    for sig in range(n):
        for nu in range(n):
            Ric[sig, nu] = _simp(sum(R[rho][sig][rho][nu] for rho in range(n)))
    return Ric


def lower_first(R, g, coords):
    """R_{rho sigma mu nu} = g_{rho lambda} R^lambda_{sigma mu nu}."""
    n = len(coords)
    Rl = [[[[sp.Integer(0)] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for rho in range(n):
        for sig in range(n):
            for mu in range(n):
                for nu in range(n):
                    Rl[rho][sig][mu][nu] = _simp(
                        sum(g[rho, lam] * R[lam][sig][mu][nu] for lam in range(n)))
    return Rl


def covariant_derivative_metric(g, Gamma, coords):
    """∇_mu g_{alpha beta} — must vanish (metric compatibility, eq. 1)."""
    n = len(coords)
    out = [[[sp.Integer(0)] * n for _ in range(n)] for _ in range(n)]
    for mu in range(n):
        for a in range(n):
            for b in range(n):
                s = sp.diff(g[a, b], coords[mu])
                for lam in range(n):
                    s -= Gamma[lam][mu][a] * g[lam, b]
                    s -= Gamma[lam][mu][b] * g[a, lam]
                out[mu][a][b] = _simp(s)
    return out


def kretschmann(Rlow, g, coords):
    """K = R_{abcd} R^{abcd}, the coordinate-invariant curvature norm."""
    n = len(coords)
    ginv = g.inv()

    # Raise all four indices of R to form R^{abcd}.
    def raise_all(a, b, c, d):
        val = sp.Integer(0)
        for p in range(n):
            for q in range(n):
                for r in range(n):
                    for s in range(n):
                        val += (ginv[a, p] * ginv[b, q] * ginv[c, r] * ginv[d, s]
                                * Rlow[p][q][r][s])
        return val

    K = sp.Integer(0)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    Rl = Rlow[a][b][c][d]
                    if Rl == 0:
                        continue
                    K += Rl * raise_all(a, b, c, d)
    return _simp(K)


# ═══════════════════════════════════════════════════════════════════
# Verification on Schwarzschild — the canonical vacuum solution.
# ═══════════════════════════════════════════════════════════════════

def main():
    print("=" * 74)
    print("SOLVING THE RIEMANN CURVATURE TENSOR — Palatini / ACS Layer 2")
    print("=" * 74)
    print("""
  R^{ab} = d omega^{ab} + omega^a_c ^ omega^{cb}          (curvature 2-form)

  (1) connection eq.  D e^a = T^a = 0  =>  omega = omega(e) = Christoffel Gamma
  (2) components      R^rho_{sig mu nu} = ∂_mu G^rho_{nu sig} - ∂_nu G^rho_{mu sig}
                                        + G^rho_{mu lam} G^lam_{nu sig}
                                        - G^rho_{nu lam} G^lam_{mu sig}
  (3) vierbein eq.    eps_{abcd} R^{ab} ^ e^c = 0  =>  R_mu_nu = 0  (vacuum)
""")

    t, r, th, ph, M = sp.symbols('t r theta phi M', positive=True)
    coords = [t, r, th, ph]
    f = 1 - 2 * M / r
    g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)

    print("=" * 74)
    print("VERIFICATION — Schwarzschild metric g = diag(-(1-2M/r), 1/(1-2M/r), r^2, r^2 sin^2 th)")
    print("=" * 74)

    Gamma = christoffel(g, coords)
    print("  [eq.1] Levi-Civita connection Gamma solved from the metric.")

    # (1) metric compatibility: the solved connection annihilates the metric
    dg = covariant_derivative_metric(g, Gamma, coords)
    metric_compat = all(_iszero(dg[m][a][b])
                        for m in range(4) for a in range(4) for b in range(4))
    print(f"  [eq.1] metric compatibility  ∇_mu g_ab = 0 (torsion-free) : {metric_compat}")
    assert metric_compat, "connection is not metric-compatible"

    R = riemann(Gamma, coords)
    print("  [eq.2] Riemann tensor R^rho_{sigma mu nu} assembled from Gamma.")

    # (3) vacuum Einstein equation: Ricci must vanish
    Ric = ricci(R, coords)
    vacuum = all(_iszero(Ric[i, j]) for i in range(4) for j in range(4))
    print(f"  [eq.3] vacuum Einstein eq.   R_mu_nu = 0                   : {vacuum}")
    assert vacuum, f"Ricci tensor did not vanish:\n{Ric}"

    # curvature is genuinely nonzero — the invariant closed form is exact
    Rlow = lower_first(R, g, coords)
    K = kretschmann(Rlow, g, coords)
    K_expected = 48 * M**2 / r**6
    K_ok = _iszero(K - K_expected)
    print(f"  [R != 0] Kretschmann K = R_abcd R^abcd = {K}")
    print(f"           matches exact closed form 48 M^2 / r^6            : {K_ok}")
    assert K_ok, f"Kretschmann scalar {K} != 48 M^2/r^6"

    # algebraic symmetries of the lowered Riemann tensor
    antisym_12 = all(_iszero(Rlow[a][b][c][d] + Rlow[b][a][c][d])
                     for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    antisym_34 = all(_iszero(Rlow[a][b][c][d] + Rlow[a][b][d][c])
                     for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    pair_sym = all(_iszero(Rlow[a][b][c][d] - Rlow[c][d][a][b])
                   for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    first_bianchi = all(
        _iszero(Rlow[a][b][c][d] + Rlow[a][c][d][b] + Rlow[a][d][b][c])
        for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    print(f"  [sym] R_{{ab.}} = -R_{{ba.}}   : {antisym_12}")
    print(f"  [sym] R_{{.cd}} = -R_{{.dc}}   : {antisym_34}")
    print(f"  [sym] R_{{abcd}} =  R_{{cdab}}  : {pair_sym}")
    print(f"  [sym] first Bianchi  R_{{a[bcd]}} = 0 : {first_bianchi}")
    assert antisym_12 and antisym_34 and pair_sym and first_bianchi

    print("=" * 74)
    print("RESULT: the Palatini connection equation solves omega -> Gamma, the")
    print("curvature 2-form gives R^rho_{sigma mu nu}, and the vierbein equation")
    print("puts it on shell (R_mu_nu = 0).  All checks pass on Schwarzschild:")
    print("  metric-compatible, Ricci-flat, K = 48 M^2/r^6, full algebraic symmetry.")
    print("=" * 74)


if __name__ == "__main__":
    main()
