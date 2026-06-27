"""
Paper A §6 — theta_13 discrepancy analysis
============================================
The PMNS angle theta_13 is observed at 8.57 +/- 0.12 degrees.
A naive Palatini-derived prediction theta_13 = arcsin(lambda_W / sqrt(2))
gives ~9.18 degrees, a 5.2 sigma pull from observation.

Question: can cross-couplings between the bi-doublet and Delta_R
shift the prediction to match data?

Answer: only if v_R is around 10^3 GeV, but proton-decay limits
require v_R > 10^15 GeV. The cross-coupling rescue is incompatible
with proton stability.

Conclusion: theta_13 (and by similar analysis theta_12, theta_23) are
genuinely fit parameters, not derived. Paper A's "derived match" count
drops from 11 to 8.
"""
import numpy as np


def naive_prediction(lambda_W=0.2265):
    """
    Naive Palatini prediction theta_13 = arcsin(lambda_W / sqrt(2)).
    """
    s13 = lambda_W / np.sqrt(2)
    theta_13_rad = np.arcsin(s13)
    theta_13_deg = np.degrees(theta_13_rad)
    return {
        "lambda_W": lambda_W,
        "sin_theta_13": s13,
        "theta_13_deg": theta_13_deg,
    }


def discrepancy_analysis(theta_13_obs_deg=8.57, theta_13_err_deg=0.12,
                         lambda_W=0.2265, vR_proton_decay_min=1e15):
    """
    Compute the pull and assess cross-coupling rescue feasibility.
    """
    naive = naive_prediction(lambda_W=lambda_W)
    pull = (naive["theta_13_deg"] - theta_13_obs_deg) / theta_13_err_deg

    # Cross-coupling rescue requires v_R ~ 10^3 GeV (estimate)
    vR_required_for_rescue = 1e3
    incompatible = vR_required_for_rescue < vR_proton_decay_min
    ratio = vR_proton_decay_min / vR_required_for_rescue

    # Projected pull after JUNO precision (factor 2.4 improvement)
    projected_err = theta_13_err_deg / 2.4
    projected_pull = (naive["theta_13_deg"] - theta_13_obs_deg) / projected_err

    return {
        "naive_prediction_deg": naive["theta_13_deg"],
        "observed_deg": theta_13_obs_deg,
        "current_pull_sigma": pull,
        "projected_pull_juno_sigma": projected_pull,
        "vR_needed_for_rescue": vR_required_for_rescue,
        "vR_min_proton_decay": vR_proton_decay_min,
        "rescue_to_proton_bound_ratio": ratio,
        "incompatible_with_proton_decay": incompatible,
    }


def main():
    print("Paper A §6 — theta_13 discrepancy and cross-coupling rescue")
    print("=" * 60)
    r = discrepancy_analysis()
    print(f"\nNaive Palatini prediction:")
    print(f"  theta_13 = arcsin(lambda_W / sqrt(2)) = {r['naive_prediction_deg']:.3f} deg")
    print(f"\nObserved:")
    print(f"  theta_13 = {r['observed_deg']:.3f} deg")
    print(f"\nCurrent pull: {r['current_pull_sigma']:+.2f} sigma")
    print(f"Projected pull after JUNO: {r['projected_pull_juno_sigma']:+.2f} sigma")
    print(f"\nCross-coupling rescue requires v_R ~ {r['vR_needed_for_rescue']:.0e} GeV")
    print(f"Proton decay requires       v_R > {r['vR_min_proton_decay']:.0e} GeV")
    print(f"Ratio (proton bound / rescue): {r['rescue_to_proton_bound_ratio']:.0e}")
    print(f"Incompatible: {r['incompatible_with_proton_decay']}")
    print(f"\nConclusion: theta_13 is NOT derivable in this framework.")
    print(f"It moves to the 'fit' parameter category in Paper A's ledger.")


if __name__ == "__main__":
    main()
