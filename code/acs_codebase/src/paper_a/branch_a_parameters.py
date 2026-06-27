"""
Paper A §4 — Five free Higgs parameters in the pre-pruning model
=================================================================
Before the Phase 50/51/52 pruning, the most general renormalizable
Higgs potential consistent with the gauge symmetries
SU(4)_C x SU(2)_L x SU(2)_R contains FIVE independent quartic
couplings:

  V = -mu_Phi^2 (Phi^dagger Phi) + lambda_Phi (Phi^dagger Phi)^2
      - mu_Delta^2 (Delta_R^dagger Delta_R)
      + rho_1 [Tr(Delta_R^dagger Delta_R)]^2
      + rho_2 Tr[(Delta_R^dagger Delta_R)^2]
      + alpha_1 (Phi^dagger Phi) Tr(Delta_R^dagger Delta_R)
      + alpha_2 Tr(Phi^dagger T^A Phi) Tr(Delta_R^dagger T^A Delta_R)
      + [beta_c Tr(Phi^dagger PhiTilde Delta_R^dagger Delta_R) + h.c.]

Five free quartics: lambda_Phi, rho_1, rho_2, alpha_1, alpha_2, beta_c.
After Palatini constraint 2 rho_1 + rho_2 = 16/9, four remain free.
After Phase 50: alpha_2 = 0 (forbidden by representation theory) -> 3 free.
After Phase 51/52: beta_c = 0 at tree level -> 2 free + tan beta radiative.

This module enumerates the parameters and their constraint relations.
"""


def parameter_ledger():
    """
    Return the parameter accounting at each phase of the pruning.
    """
    return {
        "pre_palatini": {
            "free_params": ["lambda_Phi", "rho_1", "rho_2", "alpha_1", "alpha_2", "beta_c", "tan_beta"],
            "calibrations": ["v", "v_R"],
            "total_inputs": 9,
        },
        "post_palatini_constraints": {
            "locked": {
                "lambda_Phi": "= 2 sqrt(3) / 27 (Koide projection)",
                "2 rho_1 + rho_2": "= 16/9 (Palatini pairing)",
                "g_4 = g_L = g_R": "= 4/3 (Palatini bracket)",
                "hTilde / h": "= 2/3 (Palatini Yukawa)",
                "N_generations": "= 3 (Theorem C)",
            },
            "free_params": ["rho_1", "alpha_1", "alpha_2", "beta_c", "tan_beta"],
            "calibrations": ["v", "v_R"],
            "total_inputs": 7,
        },
        "post_phase_50_alpha2_forbidden": {
            "newly_locked": "alpha_2 = 0 (T^A Phi = 0 for Phi ~ (1,2,2))",
            "free_params": ["rho_1", "alpha_1", "beta_c", "tan_beta"],
            "calibrations": ["v", "v_R"],
            "total_inputs": 6,
        },
        "post_phase_51_52_betac_excluded": {
            "newly_locked": "beta_c = 0 at tree level (else M_u = M_d)",
            "free_params": ["rho_1", "alpha_1", "tan_beta (radiative)"],
            "calibrations": ["v", "v_R"],
            "total_inputs": 6,  # tan beta still effectively free pending CW
            "note": "tan beta becomes radiatively generated rather than tree-level free",
        },
    }


def stability_ranges():
    """
    Return the allowed ranges for each remaining free parameter
    in Branch A.
    """
    import numpy as np
    rho_1_test = 0.5
    rho_2_test = 16/9 - 2 * rho_1_test
    rho_tot_test = rho_1_test + rho_2_test
    lam_phi = 2 * np.sqrt(3) / 27
    max_alpha = 2 * np.sqrt(lam_phi * rho_tot_test)
    return {
        "rho_1": {
            "range": "(0, 8/9)",
            "from": "rho_2 = 16/9 - 2 rho_1 > 0 + stability rho_1 > 0",
        },
        "alpha_1": {
            "range_str": (
                f"|alpha_1| < 2 sqrt(lambda_Phi rho_tot) "
                f"(= {max_alpha:.4f} at rho_1 = 0.5, where rho_tot = rho_1 + rho_2 = {rho_tot_test:.4f})"
            ),
            "lambda_Phi": lam_phi,
            "rho_tot_at_rho1_half": rho_tot_test,
            "max_alpha1_at_rho1_half": max_alpha,
        },
        "tan_beta": {
            "range": "(0, infinity)",
            "from": "radiatively generated, value TBD by Coleman-Weinberg",
        },
    }


def main():
    print("Paper A §4 — Free parameter ledger across pruning phases")
    print("=" * 60)

    ledger = parameter_ledger()
    for phase, info in ledger.items():
        print(f"\n{phase}:")
        for k, v in info.items():
            if k != "locked":
                print(f"  {k}: {v}")
            else:
                print(f"  locked:")
                for lk, lv in v.items():
                    print(f"    {lk}: {lv}")

    print("\nStability ranges for Branch A free parameters:")
    ranges = stability_ranges()
    for k, v in ranges.items():
        print(f"\n  {k}:")
        for kk, vv in v.items():
            print(f"    {kk}: {vv}")


if __name__ == "__main__":
    main()
