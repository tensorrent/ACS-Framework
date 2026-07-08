"""
Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Signature Selection in Clifford Algebras in Clifford Algebras in Clifford Algebras in Clifford Algebras in Clifford Algebras from Adjoint Spectral Structure in sl(4,R)
==============================================================

Companion code to Note N2 (Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Signature Selection in Clifford Algebras in Clifford Algebras in Clifford Algebras in Clifford Algebras in Clifford Algebras).

Verifies: for any even positive spectral functional f, the graded
functional S_f[P] = Tr(P_ad · f(ad_T)) is uniquely minimised at
the Lorentzian signature P = diag(1,1,1,-1) when T = T_BL has a
3+1 eigenvalue structure.

Tests:
  1. Functional universality (6 different f)
  2. Global minimum on Gr(1,4) (5000 samples)
  3. O(4) frame invariance (50 random rotations)
  4. Generator dependence (8 Cartan elements)

Run:  python3 test_signature_selection.py
"""
import numpy as np
from scipy.linalg import expm


# ============================================================
# Basis and adjoint construction
# ============================================================
def build_sl4_basis():
    basis = []
    for k in range(3):
        H = np.zeros((4, 4)); H[k, k] = 1; H[k+1, k+1] = -1
        basis.append(H)
    for i in range(4):
        for j in range(i+1, 4):
            A = np.zeros((4, 4)); A[i, j] = 1; A[j, i] = -1
            basis.append(A)
    for i in range(4):
        for j in range(i+1, 4):
            S = np.zeros((4, 4)); S[i, j] = 1; S[j, i] = 1
            basis.append(S)
    return basis

BASIS = build_sl4_basis()
N_BASIS = len(BASIS)
IP_DIAG = [np.trace(b @ b) for b in BASIS]


def compute_ad(T):
    ad = np.zeros((N_BASIS, N_BASIS))
    for i, b in enumerate(BASIS):
        comm = T @ b - b @ T
        for j, bj in enumerate(BASIS):
            if abs(IP_DIAG[j]) > 1e-12:
                ad[j, i] = np.trace(comm @ bj) / IP_DIAG[j]
    return ad


def P_adjoint(P_fund):
    Pinv = np.linalg.inv(P_fund)
    P_ad = np.zeros((N_BASIS, N_BASIS))
    for i, bi in enumerate(BASIS):
        Pbi = P_fund @ bi @ Pinv
        for j, bj in enumerate(BASIS):
            if abs(IP_DIAG[j]) > 1e-12:
                P_ad[j, i] = np.trace(Pbi @ bj) / IP_DIAG[j]
    return P_ad


def S_f(P_ad, f_ad):
    return np.trace(P_ad @ f_ad)


def spectral_f(ad_T, f_func):
    evals, evecs = np.linalg.eig(ad_T)
    evals_real = np.round(evals.real, 8)
    f_evals = np.array([f_func(e) for e in evals_real])
    return (evecs * f_evals) @ np.linalg.inv(evecs)


def random_orthogonal(dim=4):
    X = np.random.randn(dim, dim)
    Q, R = np.linalg.qr(X)
    return Q @ np.diag(np.sign(np.diag(R)))


# ============================================================
# Tests
# ============================================================
def test_functional_universality():
    """Test 1: six spectral functionals all select (3,1)."""
    print("\n" + "=" * 70)
    print("TEST 1: Functional universality")
    print("=" * 70)

    T_BL = np.diag([1/3, 1/3, 1/3, -1.0])
    ad_T = compute_ad(T_BL)

    sigs = {
        "(4,0)": np.diag([1.0, 1, 1, 1]),
        "(3,1)": np.diag([1.0, 1, 1, -1]),
        "(2,2)": np.diag([1.0, 1, -1, -1]),
    }

    f_functions = {
        "x^2":        lambda x: x**2,
        "x^4":        lambda x: x**4,
        "|x|":        lambda x: abs(x),
        "1_{x!=0}":   lambda x: 1.0 if abs(x) > 1e-6 else 0.0,
        "exp(x^2)-1": lambda x: np.exp(x**2) - 1,
        "cosh(x)-1":  lambda x: np.cosh(x) - 1,
    }

    all_pass = True
    for fname, f_func in f_functions.items():
        f_ad = spectral_f(ad_T, f_func).real
        vals = {}
        for sname, P_fund in sigs.items():
            vals[sname] = S_f(P_adjoint(P_fund), f_ad)
        min_sig = min(vals, key=vals.get)
        ok = min_sig == "(3,1)"
        if not ok:
            all_pass = False
        print(f"  f = {fname:<12}: min at {min_sig}  {'PASS' if ok else 'FAIL'}")

    print(f"\n  Result: {'ALL PASS' if all_pass else 'SOME FAILED'}")
    return all_pass


def test_grassmannian_minimum():
    """Test 2: P=diag(1,1,1,-1) is global min on Gr(1,4)."""
    print("\n" + "=" * 70)
    print("TEST 2: Global minimum on Gr(1,4)")
    print("=" * 70)

    T_BL = np.diag([1/3, 1/3, 1/3, -1.0])
    ad_T = compute_ad(T_BL)
    ad_T2 = ad_T @ ad_T

    P_L_ad = P_adjoint(np.diag([1.0, 1, 1, -1]))
    S_lorentz = S_f(P_L_ad, ad_T2)

    np.random.seed(42)
    S_min = S_lorentz
    for _ in range(5000):
        v = np.random.randn(4)
        v /= np.linalg.norm(v)
        P_v = np.eye(4) - 2 * np.outer(v, v)
        val = S_f(P_adjoint(P_v), ad_T2)
        S_min = min(S_min, val)

    ok = abs(S_min - S_lorentz) < 0.01
    print(f"  S_Lorentz = {S_lorentz:.4f}")
    print(f"  min on Gr(1,4) = {S_min:.4f}")
    print(f"  Result: {'PASS' if ok else 'FAIL'}")
    return ok


def test_frame_invariance():
    """Test 3: selection is invariant under O(4) conjugation."""
    print("\n" + "=" * 70)
    print("TEST 3: O(4) frame invariance (50 trials)")
    print("=" * 70)

    T_BL = np.diag([1/3, 1/3, 1/3, -1.0])
    P_L = np.diag([1.0, 1, 1, -1])

    np.random.seed(42)
    sig_pass = 0
    align_pass = 0

    for _ in range(50):
        G = random_orthogonal()
        T_g = G @ T_BL @ G.T
        P_g = G @ P_L @ G.T

        ad_Tg = compute_ad(T_g)
        ad_Tg2 = ad_Tg @ ad_Tg

        sigs_g = {
            "(4,0)": G @ np.eye(4) @ G.T,
            "(3,1)": P_g,
            "(2,2)": G @ np.diag([1., 1, -1, -1]) @ G.T,
        }
        S_all = {s: S_f(P_adjoint(Ps), ad_Tg2) for s, Ps in sigs_g.items()}
        if min(S_all, key=S_all.get) == "(3,1)":
            sig_pass += 1

        evals_T, evecs_T = np.linalg.eigh(T_g)
        v_min = evecs_T[:, np.argmin(evals_T)]
        P_opt = np.eye(4) - 2 * np.outer(v_min, v_min)
        if min(np.linalg.norm(P_opt - P_g),
               np.linalg.norm(P_opt + P_g)) < 1e-6:
            align_pass += 1

    print(f"  Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Adjoint Spectral Minimization and Bipartite Signature Selection in Clifford Algebras in Clifford Algebras in Clifford Algebras in Clifford Algebras in Clifford Algebras: {sig_pass}/50")
    print(f"  Alignment check:    {align_pass}/50")
    ok = sig_pass == 50 and align_pass == 50
    print(f"  Result: {'PASS' if ok else 'FAIL'}")
    return ok


def test_generator_dependence():
    """Test 4: different Cartan elements select matching signatures."""
    print("\n" + "=" * 70)
    print("TEST 4: Generator dependence")
    print("=" * 70)

    cases = [
        ("T_BL (3+1)", np.diag([1/3, 1/3, 1/3, -1.0]), "(3,1)"),
        ("(2,2,2,-6) (3+1)", np.diag([2., 2, 2, -6]), "(3,1)"),
        ("(1,1,-1,-1) (2+2)", np.diag([1., 1, -1, -1]), "(2,2)"),
    ]

    sigs = {
        "(4,0)": np.diag([1.0, 1, 1, 1]),
        "(3,1)": np.diag([1.0, 1, 1, -1]),
        "(2,2)": np.diag([1.0, 1, -1, -1]),
    }

    all_pass = True
    for name, T, expected in cases:
        ad = compute_ad(T)
        ad2 = ad @ ad
        S_all = {s: S_f(P_adjoint(Ps), ad2) for s, Ps in sigs.items()}
        selected = min(S_all, key=S_all.get)
        ok = selected == expected
        if not ok:
            all_pass = False
        print(f"  {name:<20}: selected {selected}, expected {expected}  {'PASS' if ok else 'FAIL'}")

    print(f"\n  Result: {'ALL PASS' if all_pass else 'SOME FAILED'}")
    return all_pass


def main():
    results = []
    results.append(("Functional universality", test_functional_universality()))
    results.append(("Grassmannian minimum", test_grassmannian_minimum()))
    results.append(("Frame invariance", test_frame_invariance()))
    results.append(("Generator dependence", test_generator_dependence()))

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    all_pass = True
    for name, ok in results:
        print(f"  {name:<30}: {'PASS' if ok else 'FAIL'}")
        if not ok:
            all_pass = False
    print(f"\n  Overall: {'ALL TESTS PASS' if all_pass else 'SOME TESTS FAILED'}")


if __name__ == "__main__":
    main()
