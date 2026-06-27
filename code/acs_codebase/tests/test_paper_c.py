"""
Tests for Paper C foundation theorems.

These verify the rigorous claims that the trilogy depends on.
A failure here invalidates downstream papers.
"""
import numpy as np
import pytest

from src.paper_c.theorem_c import verify_theorem_c
from src.paper_c.killing_orthogonality import (
    symbolic_verification,
    numerical_scaling_test,
    chirality_hopping_example,
)
from src.paper_c.orthogonal_complement_probe import (
    verify_probe_at_H1_A01,
    verify_probe_at_generic,
)
from src.paper_c.spectral_taxonomy import (
    classify_ad_T_BL,
    verify_su2_elliptic_2pi,
    verify_sl4_hyperbolic,
    verify_core_rope_hyperbolic,
    verify_frenet_serret_elliptic,
)
from src.paper_c.er_epr_algebraic import (
    bell_state_local_commutativity,
    bracket_killing_orthogonality,
    projection_returns_zero,
)


# ---------- Theorem C ----------

def test_theorem_c_residual_machine_zero():
    """ad^3 = (16/9) ad must hold to machine precision."""
    r = verify_theorem_c()
    assert r["theorem_c_residual"] < 1e-12
    assert r["verified"] is True


def test_theorem_c_eigenvalues_correct():
    """Eigenvalues must be {0, +/- 4/3} with multiplicities (9, 3, 3)."""
    r = verify_theorem_c()
    assert r["multiplicities"][0.0] == 9
    assert r["multiplicities"][round(4/3, 8)] == 3
    assert r["multiplicities"][round(-4/3, 8)] == 3


# ---------- Killing-orthogonality ----------

def test_killing_orthogonality_symbolic():
    """tr([X, Y] X) = 0 must hold IDENTICALLY in SymPy."""
    inner_X, inner_Y = symbolic_verification()
    assert inner_X == 0
    assert inner_Y == 0


def test_killing_orthogonality_sl3_scaling():
    """1000 random pairs in sl(3) — residuals at machine precision."""
    r = numerical_scaling_test(n=3, num_trials=1000)
    assert r["max_residual_X"] < 1e-12
    assert r["max_residual_Y"] < 1e-12
    assert r["verified"] is True


def test_killing_orthogonality_sl4_scaling():
    """1000 random pairs in sl(4) — residuals at machine precision."""
    r = numerical_scaling_test(n=4, num_trials=1000)
    assert r["max_residual_X"] < 1e-12
    assert r["max_residual_Y"] < 1e-12
    assert r["verified"] is True


def test_chirality_hopping_exact():
    """[H_1, A_01] = 2 S_01 — exact integer match."""
    r = chirality_hopping_example(n=4)
    assert r["exact_match"] is True


# ---------- Orthogonal-complement probe ----------

def test_probe_dimension_matches_theory():
    """dim B^perp = n^2 - 2 = 14 for sl(4, R)."""
    r = verify_probe_at_H1_A01()
    assert r["dim_B_perp"] == 14


def test_generators_lie_in_B_perp():
    """X, Y must lie in B^perp by Killing orthogonality."""
    r = verify_probe_at_H1_A01()
    assert r["H1_in_B_perp_residual"] < 1e-12
    assert r["A01_in_B_perp_residual"] < 1e-12


def test_generic_jacobian_rank():
    """Generic (X, Y) gives rank-15 Jacobian (full bracket-map image)."""
    r = verify_probe_at_generic(num_trials=20)
    assert r["all_rank_15"] is True
    assert r["all_kernel_15"] is True


def test_degenerate_kernel_at_H1_A01():
    """At the specific point (H_1, A_01), Jacobian rank drops to 11."""
    r = verify_probe_at_H1_A01()
    assert r["jacobian_rank_degenerate"] == 11
    assert r["jacobian_kernel_dim_degenerate"] == 19


# ---------- Spectral taxonomy ----------

def test_ad_T_BL_is_hyperbolic():
    """ad_{T_BL} has real eigenvalues — hyperbolic class."""
    cls = classify_ad_T_BL()
    assert cls["class"] == "hyperbolic"
    assert cls["zero_count"] == 9
    assert cls["real_count"] == 6
    assert cls["imaginary_count"] == 0


def test_su2_quaternion_elliptic_2pi():
    """Three 2pi/3 rotations in SU(2) compose to -I."""
    r = verify_su2_elliptic_2pi()
    assert r["is_minus_I"] is True
    assert r["deviation_from_minus_I"] < 1e-12


def test_sl4_hyperbolic_no_2pi_loop():
    """exp(2pi * ad_{T_BL}) is NOT close to I — confirms hyperbolic flow."""
    r = verify_sl4_hyperbolic()
    assert r["is_bounded_loop"] is False
    assert r["max_element_at_2pi"] > 100


def test_core_rope_R_cubed_equals_R():
    """Core rope ring satisfies R^3 = R (hyperbolic, real spectrum {-1, 0, +1})."""
    r = verify_core_rope_hyperbolic()
    assert r["R_cubed_equals_R"] is True
    assert sorted(r["eigenvalues"]) == [-1.0, 0.0, 1.0]
    assert r["spectrum_classification"]["class"] == "hyperbolic"


def test_frenet_serret_elliptic():
    """Frenet-Serret operator has imaginary eigenvalues — elliptic class."""
    r = verify_frenet_serret_elliptic(kappa=1.0, chi=0.5)
    assert r["A_cubed_residual"] < 1e-12
    assert r["spectrum_classification"]["class"] == "elliptic"


# ---------- ER=EPR algebraic ----------

def test_bell_state_local_ops_commute():
    """[A_Alice, B_Bob] = 0 on a Bell state by tensor-product structure."""
    r = bell_state_local_commutativity()
    assert r["commute"] is True


def test_bracket_killing_orthogonal_to_inputs():
    """tr([X, Y] X) = tr([X, Y] Y) = 0 — algebraic non-traversability."""
    r = bracket_killing_orthogonality()
    assert r["both_zero"] is True


def test_direct_projection_returns_zero():
    """pi_X([X, Y]) is zero to machine precision (theorem)."""
    r = projection_returns_zero()
    assert r["zero_to_machine_precision"] is True
