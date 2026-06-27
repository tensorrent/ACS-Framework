"""
Tests for Paper B spectral / resolvent reinterpretation.

Includes the negative result that the Wronskian fails Leibniz.
"""
import numpy as np
import pytest

from src.paper_b.explicit_formula_resolvent import (
    chi, trace_resolvent, verify_resolvent_identity, pole_structure_check,
    RIEMANN_ZEROS,
)
from src.paper_b.wronskian_leibniz import (
    symbolic_leibniz_check, numerical_leibniz_check,
)
from src.paper_b.renormalized_stability import (
    delta_norm, boundedness_check, divergence_test_off_critical,
)
from src.paper_b.berry_keating_counting import (
    riemann_von_mangoldt_count, berry_keating_count, comparison_table,
)


# ---------- Resolvent identity ----------

def test_resolvent_identity_at_omega_50():
    """Tr[(omega - H)^-1] = chi(omega) for trivial diagonal H."""
    r = verify_resolvent_identity(omega_test=50.0)
    assert r["match"] is True


def test_chi_diverges_near_zeros():
    """|chi(omega)| spikes near each gamma_k (simple pole)."""
    pts = pole_structure_check()
    assert all(p["diverges_at_pole"] for p in pts)


# ---------- Wronskian Leibniz failure ----------

def test_leibniz_failure_symbolic():
    """W(fg, h) - [f W(g,h) + g W(f,h)] = -f g h' identically."""
    r = symbolic_leibniz_check()
    assert r["matches_minus_fgh_prime"] is True


def test_leibniz_failure_numerical():
    """Numerical Leibniz check matches the symbolic correction term."""
    r = numerical_leibniz_check()
    assert r["matches_within_1pct"] is True


def test_leibniz_difference_nonzero():
    """The correction term -f g h' is genuinely nonzero — Wronskian
    is not a Poisson bracket."""
    r = numerical_leibniz_check()
    assert abs(r["expected_minus_fgh_prime"]) > 1e-3


# ---------- Renormalized stability ----------

def test_delta_norm_bounded_under_RH():
    """Delta_norm is bounded in u in [5, 20] under RH (50 zeros)."""
    r = boundedness_check()
    assert r["consistent_with_boundedness"] is True
    # Slope of running max should be small
    assert abs(r["running_max_slope"]) < 0.05


def test_off_critical_zero_diverges_faster():
    """A hypothetical zero at sigma > 1/2 diverges faster than RH spectrum."""
    r = divergence_test_off_critical(sigma_off=0.7)
    assert r["off_zero_diverges_faster"] is True


# ---------- Berry-Keating leading-order counting ----------

def test_BK_matches_within_two_zeros_through_T_143():
    """BK semiclassical counting matches RvM within ~2 zeros for T < 143."""
    rows = comparison_table(T_values=(50, 75, 100, 125, 143))
    for r in rows:
        assert abs(r["diff"]) <= 2.0


def test_BK_leading_form():
    """BK formula evaluates correctly at T = 100."""
    bk_100 = berry_keating_count(100.0)
    expected = (100.0 / (2 * np.pi)) * (np.log(100.0 / (2 * np.pi)) - 1)
    assert np.isclose(bk_100, expected)


def test_riemann_count_at_known_value():
    """At T = 50, exactly 10 zeros are below T (gamma_10 = 49.77)."""
    assert riemann_von_mangoldt_count(50.0) == 10
