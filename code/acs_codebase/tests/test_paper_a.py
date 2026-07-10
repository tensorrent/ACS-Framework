# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Tests for Paper A phenomenology and parameter pruning.

Negative-result tests (no-go theorems) are first-class.
"""
import numpy as np
import pytest

from src.paper_a.branch_a_parameters import parameter_ledger, stability_ranges
from src.paper_a.branch_a_vacuum import (
    vacuum_analysis, custodial_breaking, lambda_eff_consistency,
)
from src.paper_a.betac_tan_beta import tree_level_extremization
from src.paper_a.yukawa_no_go import yukawa_no_go_test, algebraic_identity_proof
from src.paper_a.theta13_obstruction import discrepancy_analysis
from src.paper_a.tm1_pmns import pull_analysis


# ---------- Branch A parameter ledger ----------

def test_branch_a_parameter_count():
    """Branch A locks at 6 inputs (4 free + 2 calibrations)."""
    ledger = parameter_ledger()
    final = ledger["post_phase_51_52_betac_excluded"]
    assert final["total_inputs"] == 6


def test_alpha1_stability_bound():
    """At rho_1 = 0.5, |alpha_1| < 2 sqrt(lam_phi rho_tot) ~ 0.81."""
    r = stability_ranges()
    bound = r["alpha_1"]["max_alpha1_at_rho1_half"]
    assert 0.80 < bound < 0.82


# ---------- Branch A vacuum (Phase 50) ----------

def test_vacuum_admits_stable_minimum():
    """Reduced potential admits stable vacuum across the alpha_1 range."""
    r = vacuum_analysis()
    # All alpha_1 values within stability bound should give stable vacuum
    stable_count = sum(1 for v in r["vacuum_per_alpha"] if v["stable"])
    assert stable_count >= 7  # at minimum, the inner alpha_1 values


def test_vacuum_recovers_target_VEVs():
    """At each alpha_1 in stability range, recover v^2 ~ 246^2."""
    r = vacuum_analysis()
    for v in r["vacuum_per_alpha"]:
        if v["stable"]:
            assert abs(v["v_squared"] - 246.0**2) / 246.0**2 < 1e-3


def test_custodial_breaking_safe():
    """Delta rho is many orders below experimental bound."""
    r = custodial_breaking()
    assert r["delta_rho_estimate"] < 1e-20
    assert r["safety_factor"] > 1e15


def test_lambda_eff_close_to_SM():
    """ACS lambda_eff = 2 sqrt(3)/27 close to lambda_SM extracted from m_H."""
    r = lambda_eff_consistency()
    assert r["fractional_difference"] < 0.02  # ~1% level


# ---------- beta_c forces tan beta = +/- 1 (Phase 51) ----------

def test_betac_extremization_yields_pi_4():
    """Tree-level critical points of V(beta) are pi/4 and 3 pi/4."""
    from sympy import pi, Rational
    r = tree_level_extremization()
    cps = r["critical_points"]
    expected = {pi / 4, 3 * pi / 4}
    assert set(cps) == expected


# ---------- Yukawa no-go (Phase 52) ----------

def test_yukawa_no_go_matrix_proportional():
    """With h_tilde = (2/3) h and equal VEVs: M_u = M_d, CKM = I."""
    r = yukawa_no_go_test()
    a = r["matrix_proportional"]
    assert a["M_u_minus_M_d_norm"] < 1e-12
    assert a["CKM_deviation_from_I"] < 1e-12


def test_yukawa_no_go_independent_invariant():
    """Independent h, hTilde with norm-ratio 2/3, equal VEVs: M_u = M_d.

    The algebraic identity M_u - M_d = (h - hTilde)(kappa_1 - kappa_2)
    gives 0 whenever kappa_1 = kappa_2, regardless of the specific
    relationship between h and hTilde. So both interpretations of
    hTilde/h = 2/3 yield the same no-go.
    """
    r = yukawa_no_go_test()
    b = r["independent_invariant_ratio"]
    assert b["M_u_minus_M_d_norm"] < 1e-12
    assert b["CKM_deviation_from_I"] < 1e-12


def test_yukawa_algebraic_identity():
    """M_u - M_d = (h - hTilde)(kappa_1 - kappa_2) — symbolic identity."""
    r = algebraic_identity_proof()
    assert r["identity_holds"] is True


# ---------- theta_13 (Phase 49) ----------

def test_theta13_pull_significant():
    """theta_13 prediction is at least 4 sigma from observation."""
    r = discrepancy_analysis()
    assert abs(r["current_pull_sigma"]) > 4.0


def test_theta13_rescue_incompatible_with_proton_decay():
    """v_R needed for cross-coupling rescue conflicts with proton stability."""
    r = discrepancy_analysis()
    assert r["incompatible_with_proton_decay"] is True
    assert r["rescue_to_proton_bound_ratio"] >= 1e10


# ---------- TM1/TM2 fail PMNS (Phase 49) ----------

def test_tm1_fails_phenomenology():
    """TM1 ansatz misses theta_12 by ~3 sigma and theta_23 by ~5 sigma."""
    r = pull_analysis()
    assert abs(r["TM1"]["theta_12_pull"]) > 2.5
    assert abs(r["TM1"]["theta_23_pull"]) > 4.0


def test_tm2_fails_phenomenology():
    """TM2 ansatz also fails theta_23 (predicts 45 deg, obs 49.2 deg)."""
    r = pull_analysis()
    assert abs(r["TM2"]["theta_23_pull"]) > 4.0
