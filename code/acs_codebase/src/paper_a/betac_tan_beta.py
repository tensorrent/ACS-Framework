# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Paper A §5 — beta_c term and tan beta selection (Phase 51 result)
==================================================================
Tree-level extremization of the cross-coupling

  V_betac = beta_c Tr(Phi^dagger PhiTilde Delta_R^dagger Delta_R) + h.c.
          = beta_c v^2 sin(2 beta) v_R^2  + h.c.   (real VEVs)

with respect to beta gives

  partial V / partial beta = 2 beta_c v^2 v_R^2 cos(2 beta) = 0

so cos(2 beta) = 0, i.e. tan beta = +/- 1.

Combined with the Phase 52 no-go (M_u = M_d when kappa_1 = kappa_2),
this rules out tree-level beta_c in the minimal bi-doublet:
  beta_c != 0 forces tan beta = +/- 1 -> M_u = M_d -> CKM = I.

Conclusion: beta_c must be ABSENT at tree level, or the Higgs sector
must be extended (Branch B with Sigma ~ (15, 1, 1)).
"""
from sympy import symbols, sin, cos, diff, simplify, solve, Rational, sqrt


def tree_level_extremization():
    """
    Symbolic verification: at tree level with beta_c != 0,
    the only critical points satisfy cos(2 beta) = 0.
    """
    beta = symbols('beta', real=True)
    beta_c = symbols('beta_c', real=True, nonzero=True)
    v = symbols('v', positive=True)
    v_R = symbols('v_R', positive=True)

    # Only the beta_c term has beta-dependence
    V_betac = beta_c * v**2 * sin(2 * beta) * v_R**2
    dV_dbeta = simplify(diff(V_betac, beta))

    # Solve cos(2 beta) = 0
    critical_points = solve(dV_dbeta, beta)

    return {
        "V_betac_term": V_betac,
        "dV_dbeta": dV_dbeta,
        "critical_points": critical_points,
        "implies_tan_beta_pm_1": "cos(2*beta) = 0 -> tan(beta) = +/- 1",
    }


def main():
    print("Paper A §5 — beta_c selection of tan beta")
    print("=" * 60)
    result = tree_level_extremization()
    print(f"\nbeta_c potential term at VEV:")
    print(f"  V_betac = {result['V_betac_term']}")
    print(f"\ndV/dbeta = {result['dV_dbeta']}")
    print(f"\nCritical points: {result['critical_points']}")
    print(f"\nConclusion: {result['implies_tan_beta_pm_1']}")
    print("\n  At beta = pi/4: tan beta = +1")
    print("  At beta = 3 pi/4: tan beta = -1")
    print("  No phenomenologically viable tan beta ~ 60 selectable.")


if __name__ == "__main__":
    main()
