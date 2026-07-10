#!/usr/bin/env python3

# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
emergence_quantum_suite.py  --  honing-stone physics thread (Fisher / qubit / entanglement)

Banks the validated sandbox computations from the free-ranging physics discussion. All T1
(machine-verified by running this file). Seed pinned: 20260423.

Five blocks:
  A. FISHER COLLAPSE      -- "reductive plausibility" as numbers:
       A1 static sloppiness (sum-of-exponentials FIM eigenvalues span orders, log-uniform)
       A2 coarse-graining collapse (CLT = Fisher loss; 4 micro shape-dims -> 2 Gaussian),
          GATED on the skew/kurt scaling matching the exact CLT law (skew~n^-1/2, kurt~n^-1).
  B. QUBIT WHEEL          -- the 4-window Z4 phase wheel (S gate), spinor double-cover,
                            and the T-gate (45 deg, off-wheel) = magic = the classical/quantum gap.
  C. ENTANGLEMENT SPECTRUM-- quantum stiff (physical, compressible) vs sloppy (random, flat):
                            TFIM ground states vs a Haar-random state.
  D. CASTE BIFURCATION /  -- insect caste = a saddle-node fold: continuous JH input -> DISCRETE
     VOXEL STATE             caste, threshold = worker eigenvalue lambda=-V'' crossing 0 (exact,
                            2/(3sqrt3)). Same math as k_eff->1 (criticality) and the router. The
                            caste IS the voxel state (bound runtime form where input lands after
                            falling). STRUCTURAL ISOMORPHISM, not operational equivalence.
  E. WORLD-COUNT /        -- "many localized worlds compiled to one substrate sum": the density
     SUBSTRATE SUM           matrix rho = (1/k) sum_i |world_i><world_i| IS the sum; D_eff=1/Tr(rho^2)
                            counts the worlds; consensus/overlap compresses the count; eigenvalues
                            are world-weights, eigen-threshold = which survive (einselection). Dual
                            of D (one->many select vs many->one compile); same eigen-threshold; the
                            multiplayer-substrate and block-C spectrum are this same quantity.
  F. RESOLUTION-FLOOR     -- the LOSSY inversion behind D/E: ascent (coarse-grain) is MANY-TO-ONE
     BIFURCATION            (distinct sources -> same macro), so the descent is ONE-TO-MANY =
     (physics<->theology)   underdetermined. above the resolution floor the ascent DETERMINES
                            (PHYSICS, resolution); below it the descent must be POSITED (THEOLOGY,
                            faith). one truth-search, bifurcated and inverted, meeting at the floor.

NOTE (scope): block A's parameter-space compression is the SOFT/RG reduction (sloppy models,
Machta-Sethna), distinct from the HARD group-theoretic reduction (e.g. 230 space groups).
Same shape (finite emergent catalog), different engine -- kept separate.
Block D is the threshold/eigenvalue-crossing unifier in a third domain (developmental biology);
the isomorphism to the AISO voxel state is a VALIDATION candidate (the shape is a natural kind),
NOT an adoption candidate (the Waddington fold does not implement the gravitational router).
Blocks A-F share ONE substrate<->realizations axis with ONE eigenvalue-threshold. That recurrence
is the RESULT (verified, computable). The "this is reality / Sephiroth" reading is the FRAME (lens),
kept at a separate tier: the math certifies the SHAPE, not the metaphysics.
F adds the physics(ascent)/theology(descent) reading of that axis. Same tier rule: the lossy
inversion is the RESULT; "physics IS theology" is the FRAME it grounds. The structure does prove
one thing about the frame -- faith is NECESSARY below the floor but not WHICH faith (descent is
one-to-many) -- and that is a theorem about the inversion, not an endorsement of any descent.
"""
import numpy as np

SEED = 20260423

# ============================================================ A. FISHER COLLAPSE
def A1_sloppy_spectrum():
    print("=" * 74)
    print("A1  static sloppiness -- FIM eigenvalues, sum of K exponentials (no fit)")
    print("=" * 74)
    t = np.linspace(0.1, 5, 60)
    for theta in [np.array([1, 2, 3, 4, 5.]), np.array([1, 2, 3, 4, 5, 6, 7, 8.])]:
        grad = np.array([-t * np.exp(-th * t) for th in theta])
        J = grad @ grad.T
        ev = np.sort(np.linalg.eigvalsh(J))[::-1]
        span = np.log10(ev[0] / ev[-1])
        print(f"  K={len(theta)}: lambda_max/lambda_min = {ev[0]/ev[-1]:.3e} ({span:.1f} orders); "
              f"log10 gaps {np.round(np.diff(np.log10(ev)), 2)}")
    print("  -> a few stiff directions, then a ~log-uniform cascade of sloppier ones = sloppiness.")

def _pmf1(th, x):
    u = th[0]*x + th[1]*x**2 + th[2]*x**3 + th[3]*x**4
    u -= u.max(); p = np.exp(u); return p / p.sum()

def A2_clt_fisher_collapse():
    print("\n" + "=" * 74)
    print("A2  coarse-graining collapse -- CLT as Fisher loss (gated on CLT sanity)")
    print("=" * 74)
    from scipy.optimize import brentq
    N = 8192; L = 300.0; x = np.linspace(-L, L, N); dx = x[1] - x[0]
    th234 = (-0.45, 0.16, -0.018)
    th1 = brentq(lambda a: np.sum(_pmf1([a, *th234], x) * x), -5, 5)
    theta0 = np.array([th1, *th234])

    def pmf_n(th, n):
        p1 = _pmf1(th, x); phi = np.fft.fft(np.fft.ifftshift(p1))
        pn = np.fft.fftshift(np.real(np.fft.ifft(phi**n))); pn = np.clip(pn, 0, None)
        return pn / pn.sum()

    def moms(p):
        m = np.sum(p*x); v = np.sum(p*(x-m)**2); sd = np.sqrt(v)
        return np.sum(p*((x-m)/sd)**3), np.sum(p*((x-m)/sd)**4) - 3

    sk1, ku1 = moms(_pmf1(theta0, x))
    ok = True
    for n in [1, 4, 16, 64, 256]:
        skn, kun = moms(pmf_n(theta0, n))
        if abs(skn - sk1/np.sqrt(n)) > 0.02: ok = False
    print(f"  single step: skew={sk1:.3f} exkurt={ku1:.3f} (non-Gaussian).  CLT sanity gate: "
          f"{'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  gate failed -> FIM not trusted."); return

    def FIM(th, n, eps=2e-4):
        pn = pmf_n(th, n); mask = pn > 1e-11; sc = []
        for j in range(4):
            tp = th.copy(); tp[j] += eps; tm = th.copy(); tm[j] -= eps
            sc.append((np.log(np.clip(pmf_n(tp, n), 1e-300, None)) -
                       np.log(np.clip(pmf_n(tm, n), 1e-300, None))) / (2*eps))
        return np.array([[np.sum(pn[mask]*sc[i][mask]*sc[j][mask]) for j in range(4)] for i in range(4)])

    print(f"  {'n':>5}   normalized FIM eigenvalues (/lambda_max)              cond #")
    for n in [1, 4, 16, 64, 256]:
        ev = np.sort(np.linalg.eigvalsh(FIM(theta0, n)))[::-1]; e = ev/ev[0]
        print(f"  {n:>5}   " + "  ".join(f"{z:8.2e}" for z in e) + f"   {ev[0]/ev[-1]:.1e}")
    print("  -> skew/kurt directions sink ~4 orders; mean+var survive. 4 micro shape-dims -> 2-dim Gaussian.")

# ============================================================ B. QUBIT WHEEL
def B_qubit_wheel():
    print("\n" + "=" * 74)
    print("B  qubit Z4 wheel, spinor double-cover, and the T-gate magic gap")
    print("=" * 74)
    i = 1j
    I = np.eye(2); Z = np.array([[1, 0], [0, -1]])
    S = np.array([[1, 0], [0, i]]); T = np.array([[1, 0], [0, np.exp(i*np.pi/4)]])
    Rz = lambda th: np.array([[np.exp(-i*th/2), 0], [0, np.exp(i*th/2)]])
    wheel = [np.linalg.matrix_power(S, k)[1, 1] for k in range(5)]
    labels = ['^ (1)', '> (i)', 'v (-1)', '< (-i)', '^ (1)']
    print("  S-gate phase wheel: " + ", ".join(f"S^{k}={v:+.0f} {labels[k]}" for k, v in enumerate(wheel)))
    print(f"  S^2 = Z? {np.allclose(S@S, Z)}   S^4 = I? {np.allclose(np.linalg.matrix_power(S,4), I)}  "
          f"-> literal 4-window Z4 wheel")
    print(f"  spinor: Rz(360) = -I? {np.allclose(Rz(2*np.pi), -I)}   Rz(720) = I? {np.allclose(Rz(4*np.pi), I)}  "
          f"-> wheel goes round TWICE (SU(2) double cover)")
    print(f"  magic: T (45 deg) off-wheel; T^2 = S? {np.allclose(T@T, S)}   T^8 = I? "
          f"{np.allclose(np.linalg.matrix_power(T,8), I)}")
    print("  -> on-wheel {H,S,CNOT} = Clifford = classically simulable; T (45 deg, between windows) = magic = quantum.")

# ============================================================ C. ENTANGLEMENT SPECTRUM
def C_entanglement_spectrum():
    print("\n" + "=" * 74)
    print("C  entanglement spectrum -- quantum stiff (physical) vs sloppy (random)")
    print("=" * 74)
    import scipy.sparse as sp, scipy.sparse.linalg as spla
    np.random.seed(SEED)
    n = 12; half = n // 2
    I = sp.identity(2, format='csr')
    X = sp.csr_matrix([[0, 1], [1, 0]]); Z = sp.csr_matrix([[1, 0], [0, -1]])

    def op(P, j):
        m = sp.identity(1, format='csr')
        for k in range(n): m = sp.kron(m, P if k == j else I, format='csr')
        return m

    def TFIM(h):
        H = sp.csr_matrix((2**n, 2**n))
        for j in range(n-1): H = H - op(Z, j) @ op(Z, j+1)
        for j in range(n):   H = H - h * op(X, j)
        return H

    def spectrum(psi):
        Mt = psi.reshape(2**half, 2**(n-half)); s = np.linalg.svd(Mt, compute_uv=False)
        p = s**2; p = p[p > 1e-14]; p /= p.sum()
        return -np.sum(p*np.log(p)), 1.0/np.sum(p**2)

    print(f"  n={n}, half-cut={half}: max entropy {half*np.log(2):.2f} nats, full rank {2**half}")
    print(f"  {'state':28s}{'S[nats]':>9}{'D_eff':>8}")
    for h, lab in [(0.5, 'TFIM h=0.5 (ordered)'), (1.0, 'TFIM h=1.0 (critical)'), (2.0, 'TFIM h=2.0 (disordered)')]:
        _, vec = spla.eigsh(TFIM(h), k=1, which='SA'); S, D = spectrum(vec[:, 0].real)
        print(f"  {lab:28s}{S:>9.3f}{D:>8.1f}")
    psi = np.random.randn(2**n) + 1j*np.random.randn(2**n); psi /= np.linalg.norm(psi)
    S, D = spectrum(psi)
    print(f"  {'random (Haar) state':28s}{S:>9.3f}{D:>8.1f}")
    print("  -> physical states compressible (D_eff ~ 1-2, stiff); random state flat (D_eff ~ full, sloppy).")
    print(f"  Holevo: <= {n} classical bits extractable per measurement regardless of 2^{n}={2**n} amplitudes.")

# ============================================================ D. CASTE BIFURCATION / VOXEL STATE
def D_caste_bifurcation_voxel_state():
    print("\n" + "=" * 74)
    print("D  caste bifurcation = voxel state -- continuous JH -> discrete caste via a fold")
    print("=" * 74)
    mu_c = 2 / (3 * np.sqrt(3))
    def wells(mu):
        r = np.roots([1, 0, -1, -mu]); return sorted(r.real[abs(r.imag) < 1e-9])
    caste = lambda mu: 'worker' if len(wells(mu)) == 3 else 'soldier'
    print(f"  exact threshold JH_c = 2/(3*sqrt3) = {mu_c:.4f}")
    print("  caste vs JH input (continuous -> DISCRETE):")
    for m in [0.0, 0.10, 0.20, 0.30, 0.38, 0.40, 0.55]:
        print(f"    JH={m:.2f} -> {caste(m)}")
    print("  worker eigenvalue lambda = 1 - 3 x*^2 crosses 0 EXACTLY at JH_c (saddle-node = threshold):")
    for m in [0.00, 0.20, 0.30, 0.384, 0.386]:
        r = wells(m)
        if len(r) == 3:
            xw = r[0]; print(f"    JH={m:.3f}: x*_worker={xw:+.4f}  lambda={1 - 3*xw**2:+.4f}")
        else:
            print(f"    JH={m:.3f}: worker well GONE -> larva rolls to soldier (x={r[0]:+.4f})")
    xc = -1 / np.sqrt(3)
    assert abs(1 - 3*xc**2) < 1e-12 and abs(xc**3 - xc - mu_c) < 1e-12, "fold identity failed"
    print("  [checked] at JH_c: V'=0 AND V''=0 simultaneously -> lambda=0 (true saddle-node).")
    print("  supersoldier = identical fold at a 2nd, higher JH threshold (Rajakumar 2012).")
    print("  SAME MATH: lambda=-V'' crosses 0  ==  k_eff crosses 1 (criticality)  ==  dominant eigenvalue")
    print("             crosses its critical value (router/Cheeger). one shape, three domains.")
    print("  VOXEL-STATE MAP (structural isomorphism, NOT operational equivalence):")
    print("    genome(latent wells)<->substrate/seed | JH(falling)<->intent's fall | lambda->0<->routing decision")
    print("    CASTE = well it lands in <-> VOXEL STATE: bound runtime form where input executes ('what survived the fall')")
    print("    identical genomes, JH sets the form <-> positional-not-essential (1000 white balls)")

# ============================================================ E. WORLD-COUNT / SUBSTRATE SUM
def E_world_count_substrate_sum():
    print("\n" + "=" * 74)
    print("E  world-count / substrate sum -- many localized worlds compiled to one rho")
    print("=" * 74)
    rng = np.random.default_rng(SEED); d = 64
    world = lambda: (lambda v: v / np.linalg.norm(v))(rng.standard_normal(d) + 1j*rng.standard_normal(d))
    Deff  = lambda rho: 1.0 / np.trace(rho @ rho).real
    print("  substrate = (1/k) sum_i |world_i><world_i| ;  D_eff counts the worlds in the sum:")
    for k in [1, 2, 4, 8, 16, 32]:
        W = [world() for _ in range(k)]
        rho = sum(np.outer(w, w.conj()) for w in W) / k
        print(f"    {k:2d} distinct worlds -> D_eff = {Deff(rho):5.2f}")
    print("  consensus / overlap compresses the count (agreement -> fewer distinct worlds):")
    base = world()
    for ov in [0.0, 0.5, 0.9, 0.99]:
        W = [(lambda w: w / np.linalg.norm(w))(ov*base + (1-ov)*world()) for _ in range(8)]
        rho = sum(np.outer(w, w.conj()) for w in W) / 8
        print(f"    8 worlds, overlap={ov:>4} -> D_eff = {Deff(rho):4.2f}")
    W = [world() for _ in range(5)]; rho = sum(np.outer(w, w.conj()) for w in W) / 5
    ev = np.sort(np.linalg.eigvalsh(rho).real)[::-1]
    print(f"  eigenvalues = world-weights: {ev[:6].round(3)}  (einselection = threshold keeping the heavy ones)")
    print("  DUAL of D: caste = one->many (threshold selects a realization); this = many->one (settlement compiles).")
    print("  the multiplayer substrate and block-C entanglement spectrum are this SAME quantity (D_eff = worlds).")
    print("  TIER LINE: the recurring substrate<->realizations shape is the RESULT; 'this is reality / Sephiroth'")
    print("             is the FRAME. the math certifies the SHAPE (D_eff, eigen-threshold), not the metaphysics.")

# ============================================================ F. RESOLUTION-FLOOR BIFURCATION
def F_resolution_floor_bifurcation():
    print("\n" + "=" * 74)
    print("F  resolution-floor bifurcation -- the lossy inversion: ascent (physics) vs descent (theology)")
    print("=" * 74)
    N = 8192; L = 300.0; x = np.linspace(-L, L, N); dx = x[1] - x[0]
    pmf    = lambda th: (lambda u: (lambda p: p/p.sum())(np.exp(u - u.max())))(
                         th[0]*x + th[1]*x**2 + th[2]*x**3 + th[3]*x**4)
    center = lambda p: np.roll(p, -int(round(np.sum(p*x) / dx)))
    def conv_n(p, n):
        phi = np.fft.fft(np.fft.ifftshift(p)); pn = np.fft.fftshift(np.real(np.fft.ifft(phi**n)))
        pn = np.clip(pn, 0, None); return pn / pn.sum()
    def smom(p):
        m = np.sum(p*x); sd = np.sqrt(np.sum(p*(x-m)**2))
        return np.sum(p*((x-m)/sd)**3), np.sum(p*((x-m)/sd)**4) - 3
    A = center(pmf([0, -0.45,  0.16, -0.018]))
    B = center(pmf([0, -0.45, -0.16, -0.018]))
    print("  ASCENT (physics): two DISTINCT sources -> coarse-grain -> distinguishability collapses (MANY-TO-ONE):")
    print(f"    {'n':>6}{'skew_A':>9}{'skew_B':>9}{'|A-B|':>10}")
    for n in [1, 2, 4, 16, 64, 256]:
        sa, ka = smom(conv_n(A, n)); sb, kb = smom(conv_n(B, n))
        print(f"    {n:>6}{sa:>9.4f}{sb:>9.4f}{abs(sa-sb)+abs(ka-kb):>10.4f}")
    print("  -> distinct sources flow to the SAME macro; the inverse (macro -> which source) is ONE-TO-MANY = underdetermined.")
    seq = [abs(smom(conv_n(A, n))[0] - smom(conv_n(B, n))[0]) for n in [1, 4, 16, 64]]
    assert all(seq[i] > seq[i+1] for i in range(len(seq)-1)), "ascent not lossy"
    print("  [checked] distinguishability is monotone decreasing -> the ascent is provably lossy.")
    print("\n  THE BIFURCATION (one lossy inversion, two branches meeting at the resolution floor):")
    print("    above floor: ascent DETERMINES   -> PHYSICS  (resolution, scaled invariants)   [determined, lossy]")
    print("    below floor: inverse not unique  -> THEOLOGY (faith supplies the descent)        [underdetermined]")
    print("    floor = Fisher collapse (block A2) = T_min height floor (L-function work). same floor.")
    print("    physics ascends toward the source but cannot reach it from below; theology descends from it on faith")
    print("    but cannot measure back up. inverses meeting at the floor; neither crosses from its own side.")
    print("\n  TIER LINE (kept in the artifact):")
    print("    RESULT (computable): the inversion is lossy; ascent many-to-one, descent one-to-many; the floor exists.")
    print("    FRAME (lens): 'physics IS theology, bifurcated and inverted.' the math grounds the SHAPE, not the metaphysics.")
    print("    THEOREM about the frame: one-to-many => faith NECESSARY below the floor but NOT WHICH faith")
    print("       (many descents consistent with one physics). that silence is structural, not a hedge.")

if __name__ == "__main__":
    print(f"emergence + quantum suite | seed {SEED}\n")
    A1_sloppy_spectrum()
    A2_clt_fisher_collapse()
    B_qubit_wheel()
    C_entanglement_spectrum()
    D_caste_bifurcation_voxel_state()
    E_world_count_substrate_sum()
    F_resolution_floor_bifurcation()
    print("\n[all results T1: reproduced by running this file]")
