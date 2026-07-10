# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Paper A §6 — TM1/TM2 PMNS ansaetze fail phenomenology
========================================================
The Palatini bracket has S_3 residual symmetry on the +1/3 eigenspace
of T_BL (permutations of the three quark generations). This S_3 is
COMPATIBLE with TM1, TM2, and TBM mixing ansaetze, but does not pick
any one of them uniquely.

Even granting that nature picks TM1 (first PMNS column = (sqrt(2/3),
-sqrt(1/6), sqrt(1/6))), the predicted theta_12 and theta_23 fail
observation at the 3 - 5 sigma level:

  TM1: theta_12 predicts 35.7 deg (obs 33.4 +/- 0.75 deg)  -> +3 sigma
       theta_23 predicts 44.4 deg (obs 49.2 +/- 1.0 deg)   -> -5 sigma

Conclusion: PMNS angles are genuine fit parameters, not derived.
"""
import numpy as np


def tm1_predictions(theta_13_obs_deg=8.57):
    """
    TM1 ansatz uses theta_13 as input and predicts theta_12, theta_23.

    sin^2(theta_12) = 1 / (3 cos^2(theta_13))
    sin^2(theta_23) = (1 - 2 sin^2(theta_13)) / (2 - 2 sin^2(theta_13))
    """
    s13_sq = np.sin(np.radians(theta_13_obs_deg)) ** 2
    s12_sq = 1.0 / (3.0 * (1.0 - s13_sq))
    s23_sq = (1.0 - 2 * s13_sq) / (2.0 - 2 * s13_sq)
    theta_12 = np.degrees(np.arcsin(np.sqrt(s12_sq)))
    theta_23 = np.degrees(np.arcsin(np.sqrt(s23_sq)))
    return {"theta_12_deg": theta_12, "theta_23_deg": theta_23}


def tm2_predictions(theta_13_obs_deg=8.57):
    """
    TM2 ansatz: sin^2(theta_12) = 1/3 / (1 - sin^2(theta_13))
    theta_23 fixed at 45 degrees independent of theta_13.
    """
    s13_sq = np.sin(np.radians(theta_13_obs_deg)) ** 2
    s12_sq = (1.0 / 3.0) / (1.0 - s13_sq)
    theta_12 = np.degrees(np.arcsin(np.sqrt(s12_sq)))
    theta_23 = 45.0
    return {"theta_12_deg": theta_12, "theta_23_deg": theta_23}


def pull_analysis(theta_12_obs=33.41, theta_12_err=0.75,
                  theta_23_obs=49.2, theta_23_err=1.0,
                  theta_13_obs=8.57):
    """
    Compute pulls for both TM1 and TM2 ansaetze.
    """
    tm1 = tm1_predictions(theta_13_obs)
    tm2 = tm2_predictions(theta_13_obs)
    return {
        "TM1": {
            "theta_12_pred": tm1["theta_12_deg"],
            "theta_23_pred": tm1["theta_23_deg"],
            "theta_12_pull": (tm1["theta_12_deg"] - theta_12_obs) / theta_12_err,
            "theta_23_pull": (tm1["theta_23_deg"] - theta_23_obs) / theta_23_err,
        },
        "TM2": {
            "theta_12_pred": tm2["theta_12_deg"],
            "theta_23_pred": tm2["theta_23_deg"],
            "theta_12_pull": (tm2["theta_12_deg"] - theta_12_obs) / theta_12_err,
            "theta_23_pull": (tm2["theta_23_deg"] - theta_23_obs) / theta_23_err,
        },
        "observed": {
            "theta_12": theta_12_obs,
            "theta_12_err": theta_12_err,
            "theta_23": theta_23_obs,
            "theta_23_err": theta_23_err,
        },
    }


def main():
    print("Paper A §6 — TM1 / TM2 PMNS ansaetze fail phenomenology")
    print("=" * 60)
    r = pull_analysis()
    print(f"\nObserved:")
    print(f"  theta_12 = {r['observed']['theta_12']:.2f} +/- {r['observed']['theta_12_err']:.2f} deg")
    print(f"  theta_23 = {r['observed']['theta_23']:.2f} +/- {r['observed']['theta_23_err']:.2f} deg")
    for ansatz in ["TM1", "TM2"]:
        d = r[ansatz]
        print(f"\n{ansatz}:")
        print(f"  theta_12 prediction: {d['theta_12_pred']:.2f} deg "
              f"(pull {d['theta_12_pull']:+.1f} sigma)")
        print(f"  theta_23 prediction: {d['theta_23_pred']:.2f} deg "
              f"(pull {d['theta_23_pull']:+.1f} sigma)")
    print(f"\nNeither ansatz is selected by Palatini S_3 symmetry, and neither")
    print(f"matches data at the few-sigma level. PMNS angles are fit, not derived.")


if __name__ == "__main__":
    main()
