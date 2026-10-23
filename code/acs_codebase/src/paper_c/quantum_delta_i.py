# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

"""
Paper C / monograph §"Quantum definition of ΔI" — 2-qubit ΔI_Q toy model
=========================================================================
Port of ``extras/quantum_acs_2qubit.py`` (SCRIPT 54/76 in the heritage
bundle ``extras/ACS_all_76_scripts.py``).  The extras copy is untouched;
this module is the canonical, tested form.

What the quantity is
--------------------
The monograph (``papers/Form_Function_and_Asymmetry.tex``, §"Extensions
and Open Problems" → §"Quantum definition of ΔI") proposes the quantum
analogue of the ACS information asymmetry ΔI: the classical attractor
(SRB measure) becomes the steady state ρ_∞ of a Lindblad equation in
which subsystems A (Form) and B (Function) are each other's dissipative
environment, and ΔI_Q is a transfer-entropy asymmetry built from
conditional von Neumann entropies and evaluated at ρ_∞.  The same
passage states that "the explicit computation for finite-dimensional toy
models (e.g. a 2-qubit ACS) is tractable (~2 pages)".  Link 1 of
``papers/later_FF06_series/One_Mechanism_Many_Forms_Sigma.tex`` fixes
ΔI as the transfer-entropy asymmetry by definition, and
``papers/core_trilogy/Holographic_Spectral_Inversion.tex`` (§ on the
Wheeler–DeWitt conjecture) reads the quantum attractor as ΔI_Q = 0.

What the script computes (and what it does not)
-----------------------------------------------
The heritage script does *not* evaluate the conditional-entropy
definition.  It computes a directional entropy-flow proxy:

  1. Integrate the Lindblad equation with H(ε) = H_0 + ε V_f + 0.6 ε V_g
     from the maximally mixed state for 8000 forward-Euler steps of
     dt = 0.005 (T = 40) and call the result the steady state ρ_ss.
  2. Probe the two channels separately for a short time τ = 0.15 with
     pure unitary evolution: the Form→Function channel H_0 + ε V_f and
     the Function→Form channel H_0 + 0.6 ε V_g.
  3. ΔI_Q := [S(ρ_B) after the A-drive − S(ρ_B) at ρ_ss]
           − [S(ρ_A) after the B-drive − S(ρ_A) at ρ_ss].

This is a port, not a derivation: the proxy is carried as-is, the gap
between it and the monograph's definition is left on the frontier, and
the tests pin the script's current outputs.  Two facts the port makes
measurable rather than assumed:

  * The "steady state" is the Euler state at T = 40, not a converged
    fixed point: ``lindbladian_residual`` is ~2e-3 at ε = 0 (the weak
    B-decay channel, rate 0.15² ≈ 0.02, has relaxation time ≈ 44).
  * At ε = 0 both probe Hamiltonians reduce to the local H_0, which
    cannot move reduced-state spectra, so ΔI_Q(0) = 0 in exact
    arithmetic (the script returns 0.0) — a structural property, not a
    numerical coincidence.

Structural properties (tested):
  - ΔI_Q vanishes for any state when both drives are local.
  - ΔI_Q is odd under exchanging the roles of Form and Function
    (swap the qubits and exchange the two drive Hamiltonians).
  - Mutual information vanishes on product states and is 2 bits on a
    Bell state; partial traces recover the factors of a product state.

No random sampling is used in the sweep itself; the structural tests
draw their generic state from the canonical seed (``src.common.seed``).
"""
import numpy as np
from numpy.linalg import eigvalsh
from scipy.linalg import expm
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.common import bracket, default_rng

# ---------- Single-qubit operators ----------

I2 = np.eye(2, dtype=complex)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)
SIGMA_PLUS = np.array([[0, 1], [0, 0]], dtype=complex)   # raising
SIGMA_MINUS = np.array([[0, 0], [1, 0]], dtype=complex)  # lowering

# ---------- The heritage model, constants verbatim from the script ----------

# Local level splitting on both qubits.  Local, so it preserves the
# spectra of both reduced states — this is why ΔI_Q(0) = 0 exactly.
H_0 = 0.5 * (np.kron(SIGMA_Z, I2) + np.kron(I2, SIGMA_Z))

# Asymmetric, non-commuting coupling operators: V_FORM is the A→B
# (Form→Function) drive, V_FUNCTION the B→A (Function→Form) drive.
V_FORM = np.kron(SIGMA_Z, SIGMA_X) + 0.3 * np.kron(SIGMA_Y, SIGMA_Z)
V_FUNCTION = np.kron(SIGMA_X, SIGMA_Z) + 0.5 * np.kron(SIGMA_Z, SIGMA_Y)

# The script weights the function channel by 0.6 relative to the form
# channel, both in the full Hamiltonian and in the probe.
FUNCTION_WEIGHT = 0.6

# Asymmetric dissipation: A decays faster than B through different
# channels, so the steady state is neither maximally mixed nor symmetric.
LINDBLAD_OPS = [
    0.5 * np.kron(SIGMA_MINUS, I2),            # A decays (strong)
    0.15 * np.kron(I2, SIGMA_MINUS),           # B decays (weak)
    0.2 * np.kron(SIGMA_PLUS, SIGMA_MINUS),    # A excites when B decays
    0.1 * np.kron(SIGMA_Z, SIGMA_X),           # entangling dephasing
]

DT = 0.005          # forward-Euler step
N_STEPS = 8000      # T = 40
PROBE_TIME = 0.15   # unitary probe duration for each channel

EPSILONS = (0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0)

# Eigenvalues below this are dropped from the entropy sum (script's cut).
ENTROPY_EIGEN_CUT = 1e-15


# ---------- Bipartite helpers ----------

def partial_trace_b(rho):
    """
    Trace out qubit B (the second tensor factor); returns ρ_A.

    Index convention: rho[(i, k), (j, l)] with (i, j) on A and (k, l)
    on B, i.e. row index i*2 + k.
    """
    r = rho.reshape(2, 2, 2, 2)
    return np.einsum("ikjk->ij", r)


def partial_trace_a(rho):
    """Trace out qubit A (the first tensor factor); returns ρ_B."""
    r = rho.reshape(2, 2, 2, 2)
    return np.einsum("kikj->ij", r)


def von_neumann_entropy(rho):
    """
    S(ρ) = -Σ λ log2 λ over eigenvalues λ > ENTROPY_EIGEN_CUT, in bits.

    The cut reproduces the script: eigenvalues at or below 1e-15 are
    treated as exact zeros rather than contributing 0·log 0 noise.
    """
    ev = eigvalsh(rho)
    ev = ev[ev > ENTROPY_EIGEN_CUT]
    return float(-np.sum(ev * np.log2(ev)))


def mutual_information(rho):
    """I(A:B) = S(ρ_A) + S(ρ_B) − S(ρ_AB), in bits."""
    return (von_neumann_entropy(partial_trace_b(rho))
            + von_neumann_entropy(partial_trace_a(rho))
            - von_neumann_entropy(rho))


def purity(rho):
    """Tr(ρ²); 1 for pure states, 1/4 for the maximally mixed 2-qubit state."""
    return float(np.real(np.trace(rho @ rho)))


def random_density_matrix(dim=4, rng=None):
    """
    Generic full-rank density matrix ρ = G G† / Tr(G G†) with G a
    complex Ginibre matrix drawn from the canonical RNG by default.
    Used by the structural tests, not by the sweep.
    """
    if rng is None:
        rng = default_rng()
    G = rng.standard_normal((dim, dim)) + 1j * rng.standard_normal((dim, dim))
    rho = G @ G.conj().T
    return rho / np.trace(rho).real


# ---------- Lindblad dynamics ----------

def lindbladian(H, rho, lindblad_ops=LINDBLAD_OPS):
    """
    Right-hand side of the Lindblad master equation:
      L(ρ) = -i[H, ρ] + Σ_k ( L_k ρ L_k† − ½ {L_k† L_k, ρ} ).

    Term order matches the script so the Euler trajectory is bitwise
    reproducible.
    """
    drho = -1j * (H @ rho - rho @ H)
    for L in lindblad_ops:
        Ld = L.conj().T
        drho += L @ rho @ Ld - 0.5 * (Ld @ L @ rho + rho @ Ld @ L)
    return drho


def euler_steady_state(H, rho0=None, dt=DT, n_steps=N_STEPS,
                       lindblad_ops=LINDBLAD_OPS):
    """
    Forward-Euler integration of the Lindblad equation from rho0
    (default: maximally mixed), re-hermitising and re-normalising each
    step exactly as the script does.

    This is the script's "steady state".  It is the state at
    T = dt * n_steps, not a solved fixed point; see
    ``lindbladian_residual`` for how far from stationary it is.
    """
    if rho0 is None:
        rho0 = np.eye(4, dtype=complex) / 4
    rho = rho0
    for _ in range(n_steps):
        rho = rho + dt * lindbladian(H, rho, lindblad_ops)
        rho = (rho + rho.conj().T) / 2
        rho /= np.trace(rho).real
    return rho


def lindbladian_residual(H, rho, lindblad_ops=LINDBLAD_OPS):
    """Frobenius norm ‖L(ρ)‖ — zero iff ρ is a true stationary state."""
    return float(np.linalg.norm(lindbladian(H, rho, lindblad_ops)))


def full_hamiltonian(eps):
    """H(ε) = H_0 + ε V_f + 0.6 ε V_g — the Hamiltonian that sets ρ_ss."""
    return H_0 + eps * V_FORM + eps * FUNCTION_WEIGHT * V_FUNCTION


def form_channel_hamiltonian(eps):
    """Form→Function probe: H_0 + ε V_f (A drives B)."""
    return H_0 + eps * V_FORM


def function_channel_hamiltonian(eps):
    """Function→Form probe: H_0 + 0.6 ε V_g (B drives A)."""
    return H_0 + eps * FUNCTION_WEIGHT * V_FUNCTION


# ---------- The quantity ----------

def _unitary_probe(H, rho, probe_time):
    """ρ ↦ e^{-iHτ} ρ e^{iHτ}, re-hermitised and re-normalised as the script does."""
    U = expm(-1j * H * probe_time)
    out = U @ rho @ U.conj().T
    out = (out + out.conj().T) / 2
    return out / np.trace(out).real


def delta_i_q(rho, h_form, h_function, probe_time=PROBE_TIME):
    """
    Directional entropy-flow asymmetry of the heritage script.

      dS_B_from_A = S(ρ_B | after h_form probe)     − S(ρ_B | ρ)
      dS_A_from_B = S(ρ_A | after h_function probe) − S(ρ_A | ρ)
      ΔI_Q        = dS_B_from_A − dS_A_from_B

    Parameters
    ----------
    rho : (4, 4) density matrix (the state probed; ρ_ss in the sweep)
    h_form : (4, 4) Hermitian — the Form→Function channel Hamiltonian
    h_function : (4, 4) Hermitian — the Function→Form channel Hamiltonian
    probe_time : float — duration τ of each unitary probe

    Returns
    -------
    dict with the two entropy changes and their difference.
    """
    s_a = von_neumann_entropy(partial_trace_b(rho))
    s_b = von_neumann_entropy(partial_trace_a(rho))
    rho_fg = _unitary_probe(h_form, rho, probe_time)
    rho_gf = _unitary_probe(h_function, rho, probe_time)
    dS_B_from_A = von_neumann_entropy(partial_trace_a(rho_fg)) - s_b
    dS_A_from_B = von_neumann_entropy(partial_trace_b(rho_gf)) - s_a
    return {
        "dS_B_from_A": dS_B_from_A,
        "dS_A_from_B": dS_A_from_B,
        "delta_i_q": dS_B_from_A - dS_A_from_B,
    }


SWAP = np.array([[1, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1]], dtype=complex)


def swap_roles(rho, h_form, h_function):
    """
    Exchange Form and Function: relabel the qubits (conjugate by SWAP)
    and hand each channel the other's Hamiltonian.  ΔI_Q is odd under
    this map, which is the sign structure a directed asymmetry must have.

    Returns (rho', h_form', h_function') ready for ``delta_i_q``.
    """
    return (SWAP @ rho @ SWAP,
            SWAP @ h_function @ SWAP,
            SWAP @ h_form @ SWAP)


# ---------- The sweep ----------

def sweep(epsilons=EPSILONS):
    """
    Reproduce the script's table: for each ε, integrate to ρ_ss, record
    purity, S_A, S_B, mutual information, ΔI_Q and the stationarity
    residual.

    Returns
    -------
    list of dict, one per ε, in the order given.
    """
    rows = []
    for eps in epsilons:
        H = full_hamiltonian(eps)
        rho_ss = euler_steady_state(H)
        di = delta_i_q(rho_ss,
                       form_channel_hamiltonian(eps),
                       function_channel_hamiltonian(eps))
        rows.append({
            "eps": eps,
            "rho_ss": rho_ss,
            "purity": purity(rho_ss),
            "S_A": von_neumann_entropy(partial_trace_b(rho_ss)),
            "S_B": von_neumann_entropy(partial_trace_a(rho_ss)),
            "MI": mutual_information(rho_ss),
            "delta_i_q": di["delta_i_q"],
            "residual": lindbladian_residual(H, rho_ss),
        })
    return rows


def cubic_fit(rows, eps_min=0.01):
    """
    The script's cubic polyfit of ΔI_Q(ε) over ε > eps_min.

    Returns
    -------
    dict with the three Taylor-like coefficients (alpha1 linear, alpha2
    quadratic, alpha3 cubic) and the constant term the script discards.
    """
    eps_a = np.array([r["eps"] for r in rows], dtype=float)
    di_a = np.array([r["delta_i_q"] for r in rows], dtype=float)
    mask = eps_a > eps_min
    c3, c2, c1, c0 = np.polyfit(eps_a[mask], di_a[mask], 3)
    return {"alpha1": float(c1), "alpha2": float(c2), "alpha3": float(c3),
            "const": float(c0)}


def script_verdicts(rows, fit):
    """
    The five yes/no checks the script prints, as booleans with the
    script's thresholds.
    """
    di = [r["delta_i_q"] for r in rows]
    return {
        "DI_Q_at_zero_vanishes": abs(di[0]) < 0.001,
        "alpha1_nonzero": abs(fit["alpha1"]) > 1e-4,
        "alpha2_nonzero": abs(fit["alpha2"]) > 1e-4,
        "DI_Q_grows_with_eps": abs(di[-1]) > abs(di[1]),
        "steady_state_not_pure": rows[-1]["purity"] < 0.9,
    }


def main():
    print("Paper C / monograph — 2-qubit quantum ΔI_Q toy (port of extras script 54)")
    print("=" * 72)
    print(f"  ||[V_f, V_g]|| = {np.linalg.norm(bracket(V_FORM, V_FUNCTION)):.4f}")
    print(f"\n  {'eps':<6} {'Purity':<8} {'S_A':<8} {'S_B':<8} {'MI':<8} "
          f"{'DI_Q':<11} {'||L(rho)||':<10}")
    print(f"  {'-'*64}")
    rows = sweep()
    for r in rows:
        print(f"  {r['eps']:<6.2f} {r['purity']:<8.4f} {r['S_A']:<8.4f} "
              f"{r['S_B']:<8.4f} {r['MI']:<8.4f} {r['delta_i_q']:<+11.6f} "
              f"{r['residual']:<10.2e}")
    fit = cubic_fit(rows)
    print(f"\n  Fit: DI_Q ≈ {fit['alpha1']:.4f}·ε + {fit['alpha2']:.4f}·ε² "
          f"+ {fit['alpha3']:.4f}·ε³")
    for name, ok in script_verdicts(rows, fit).items():
        print(f"    {name:<26} {'YES' if ok else 'NO'}")
    print("\n  Note: rho_ss is the Euler state at T = 40; the residual column")
    print("  measures how far it is from stationary (not converged at small eps).")


if __name__ == "__main__":
    main()
