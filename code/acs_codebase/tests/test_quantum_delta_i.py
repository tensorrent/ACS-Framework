# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Tests for the 2-qubit ΔI_Q toy (port of extras/quantum_acs_2qubit.py).

Two kinds of assertion:
  * Pins — the heritage script's current outputs, captured by executing
    the untouched script on 2026-10-23 (numpy 2.2.6, scipy 1.15.3).
    ΔI_Q and purity are pinned to the full-precision values the script
    holds in memory (interval 1e-9); S_A, S_B and MI are pinned to the
    four decimals the script prints (interval 6e-5).
  * Structure — properties the quantity must have independent of the
    integrator: it vanishes for local drives, it is odd under the
    Form/Function role swap, and the entropy helpers behave on product
    and Bell states.
"""
import numpy as np
import pytest

from src.common import default_rng, bracket, FLOAT_TOL
from src.paper_c.quantum_delta_i import (
    I2, H_0, V_FORM, V_FUNCTION, LINDBLAD_OPS, EPSILONS,
    partial_trace_a, partial_trace_b, von_neumann_entropy,
    mutual_information, purity, random_density_matrix,
    lindbladian_residual,
    form_channel_hamiltonian, function_channel_hamiltonian,
    delta_i_q, swap_roles, sweep, cubic_fit, script_verdicts,
)


# Reference values from the untouched extras script (see module docstring).
# Columns: eps, DI_Q (full precision), purity (full precision),
#          S_A, S_B, MI (as printed, 4 decimals).
SCRIPT_ROWS = [
    (0.0,  0.0,                     0.724963848387223,   0.1587, 0.5780, 0.0020),
    (0.05, 0.00022579956185653227,  0.7229247066490159,  0.1643, 0.5810, 0.0054),
    (0.1,  0.0008866717059490825,   0.7161261343004577,  0.1814, 0.5914, 0.0159),
    (0.2,  0.0033361035779112536,   0.681572417393611,   0.2521, 0.6480, 0.0619),
    (0.3,  0.006882482378568422,    0.6170672089350814,  0.3627, 0.7522, 0.1327),
    (0.5,  0.014598593332846077,    0.4886457063825397,  0.5885, 0.9271, 0.2430),
    (0.7,  0.01940038651178433,     0.4247826447910553,  0.7393, 0.9824, 0.2794),
    (1.0,  0.020760398890092624,    0.37894082620583514, 0.8655, 0.9971, 0.2715),
    (1.5,  0.01727151547579997,     0.3338816817755348,  0.9512, 0.9996, 0.2083),
    (2.0,  0.013277430283098246,    0.3066312102260882,  0.9797, 0.9999, 0.1498),
]
SCRIPT_BRACKET_NORM = 2.3323807579381204
SCRIPT_FIT = {"alpha1": 0.05192304374999331,
              "alpha2": -0.03349743361518704,
              "alpha3": 0.005894562817676941}

PIN_FULL = 1e-9    # interval around a full-precision captured value
PIN_PRINTED = 6e-5  # interval around a value captured at 4 printed decimals


@pytest.fixture(scope="module")
def rows():
    """One sweep per test module: ten Euler integrations (~6 s)."""
    return sweep()


# ---------- Pins: the script's current outputs ----------

def test_sweep_grid_matches_script():
    assert tuple(EPSILONS) == tuple(r[0] for r in SCRIPT_ROWS)


def test_bracket_norm_matches_script():
    """||[V_f, V_g]|| = 2.3324 — the drives do not commute."""
    n = float(np.linalg.norm(bracket(V_FORM, V_FUNCTION)))
    assert abs(n - SCRIPT_BRACKET_NORM) <= PIN_FULL
    assert n > 1.0


@pytest.mark.parametrize("idx", range(len(SCRIPT_ROWS)),
                         ids=[f"eps={r[0]}" for r in SCRIPT_ROWS])
def test_row_matches_script(rows, idx):
    eps, di_ref, pur_ref, sa_ref, sb_ref, mi_ref = SCRIPT_ROWS[idx]
    r = rows[idx]
    assert r["eps"] == eps
    assert abs(r["delta_i_q"] - di_ref) <= PIN_FULL
    assert abs(r["purity"] - pur_ref) <= PIN_FULL
    assert abs(r["S_A"] - sa_ref) <= PIN_PRINTED
    assert abs(r["S_B"] - sb_ref) <= PIN_PRINTED
    assert abs(r["MI"] - mi_ref) <= PIN_PRINTED


def test_cubic_fit_matches_script(rows):
    """DI_Q ≈ 0.0519 ε − 0.0335 ε² + 0.0059 ε³ over ε > 0.01."""
    fit = cubic_fit(rows)
    for k, ref in SCRIPT_FIT.items():
        assert abs(fit[k] - ref) <= 1e-7


def test_script_verdicts_all_yes(rows):
    """The five checks the script prints as YES are still YES."""
    v = script_verdicts(rows, cubic_fit(rows))
    assert all(v.values()), v


def test_delta_i_q_sign_and_growth(rows):
    """ΔI_Q > 0 for every ε > 0 on this grid and peaks inside it (ε = 1.0)."""
    di = [r["delta_i_q"] for r in rows]
    assert all(d > 1e-4 for d in di[1:])
    assert max(range(len(di)), key=lambda i: di[i]) == 7


# ---------- Measured, not assumed: what the "steady state" is ----------

@pytest.mark.parametrize("idx", range(len(SCRIPT_ROWS)),
                         ids=[f"eps={r[0]}" for r in SCRIPT_ROWS])
def test_steady_state_is_a_full_rank_density_matrix(rows, idx):
    rho = rows[idx]["rho_ss"]
    assert abs(np.trace(rho).real - 1.0) <= FLOAT_TOL
    assert np.linalg.norm(rho - rho.conj().T) <= FLOAT_TOL
    assert np.linalg.eigvalsh(rho).min() > 1e-4     # full rank, as the monograph requires
    assert 0.25 <= rows[idx]["purity"] <= 1.0


def test_steady_state_residual_is_small_but_not_converged(rows):
    """
    The Euler state at T = 40 is within 3e-3 of stationary at every ε
    (measured 2.1e-3 at ε = 0, 3.4e-4 at ε = 1.0).  Floor on quality:
    the bound may tighten if the integrator is improved; it must not
    loosen.
    """
    for r in rows:
        assert r["residual"] < 3e-3
    # The lower bound is stated so the pin cannot be re-read as a
    # claim of convergence: at ε = 0 the state is not a fixed point.
    assert rows[0]["residual"] > 1e-3


# ---------- Structure: independent of the integrator ----------

def test_delta_i_q_vanishes_for_local_drives():
    """
    A local Hamiltonian cannot change either reduced spectrum, so both
    entropy changes are zero and ΔI_Q = 0 — for any state, not just ρ_ss.
    """
    rng = default_rng()
    rho = random_density_matrix(rng=rng)
    r = delta_i_q(rho, H_0, H_0)
    assert abs(r["dS_B_from_A"]) <= FLOAT_TOL
    assert abs(r["dS_A_from_B"]) <= FLOAT_TOL
    assert abs(r["delta_i_q"]) <= FLOAT_TOL
    # Any other local pair, including a generic one, behaves the same.
    h_a = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    h_b = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
    h_local = np.kron(h_a + h_a.conj().T, I2) + np.kron(I2, h_b + h_b.conj().T)
    r = delta_i_q(rho, h_local, 0.6 * h_local)
    assert abs(r["delta_i_q"]) <= FLOAT_TOL


def test_delta_i_q_odd_under_role_swap():
    """
    Relabelling A↔B and exchanging the two channel Hamiltonians negates
    ΔI_Q (exactly, by construction of the two entropy differences).
    """
    rho = random_density_matrix()
    for eps in (0.3, 1.0, 2.0):
        h_f = form_channel_hamiltonian(eps)
        h_g = function_channel_hamiltonian(eps)
        d = delta_i_q(rho, h_f, h_g)["delta_i_q"]
        d_swapped = delta_i_q(*swap_roles(rho, h_f, h_g))["delta_i_q"]
        assert abs(d + d_swapped) <= FLOAT_TOL
        assert abs(d) > 1e-6  # the test is not vacuous: ΔI_Q ≠ 0 here


def test_partial_traces_recover_product_factors():
    rho_a = np.array([[0.7, 0.2j], [-0.2j, 0.3]], dtype=complex)
    rho_b = np.array([[0.4, 0.1], [0.1, 0.6]], dtype=complex)
    rho = np.kron(rho_a, rho_b)
    assert np.linalg.norm(partial_trace_b(rho) - rho_a) <= FLOAT_TOL
    assert np.linalg.norm(partial_trace_a(rho) - rho_b) <= FLOAT_TOL


def test_mutual_information_vanishes_on_product_state():
    rho_a = np.array([[0.7, 0.2j], [-0.2j, 0.3]], dtype=complex)
    rho_b = np.array([[0.4, 0.1], [0.1, 0.6]], dtype=complex)
    assert abs(mutual_information(np.kron(rho_a, rho_b))) <= FLOAT_TOL


def test_entropy_and_mutual_information_on_reference_states():
    """Pure: S = 0. Maximally mixed 2-qubit: S = 2 bits. Bell: I(A:B) = 2 bits."""
    bell = np.zeros(4, dtype=complex)
    bell[0] = bell[3] = 1 / np.sqrt(2)
    rho_bell = np.outer(bell, bell.conj())
    assert abs(von_neumann_entropy(rho_bell)) <= FLOAT_TOL
    assert abs(mutual_information(rho_bell) - 2.0) <= FLOAT_TOL
    assert abs(purity(rho_bell) - 1.0) <= FLOAT_TOL
    rho_mixed = np.eye(4, dtype=complex) / 4
    assert abs(von_neumann_entropy(rho_mixed) - 2.0) <= FLOAT_TOL
    assert abs(purity(rho_mixed) - 0.25) <= FLOAT_TOL


def test_lindbladian_residual_zero_on_decoupled_ground_state():
    """
    With only the two local decay channels and H_0, the state |1⟩⊗|1⟩
    (both qubits in the σ_z = −1 eigenstate that σ_- lowers into, basis
    index 3) is an exact stationary state: residual zero to machine
    precision.  This checks the residual diagnostic itself, so that the
    non-zero residuals of the sweep are read as measurements.
    """
    ground = np.zeros((4, 4), dtype=complex)
    ground[3, 3] = 1.0
    decay_only = LINDBLAD_OPS[:2]
    assert lindbladian_residual(H_0, ground, decay_only) <= FLOAT_TOL
