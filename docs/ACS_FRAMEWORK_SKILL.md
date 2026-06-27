# ACS Framework — Research Skill

## Metadata

- **Name:** acs-framework
- **Author:** Bradley Wallace
- **Version:** 1.0 (May 2026)
- **Trigger:** ACS, Palatini bracket, Pati-Salam, grading selection, sl(4), Lie bracket, adjoint representation, Barbero-Immirzi, Coleman-Weinberg, signature selection, "work on the papers", "what's still open", "test this idea"

---

## 1. What This Skill Is

This skill encodes the complete ACS (Asymmetric Codependent Systems) research program: the methodology, the computational toolkit, the current framework state, the document collection, and the honesty standards. It enables continuation of ACS research with full context, or application of the adversarial compression methodology to new problems.

The ACS framework derives the Pati-Salam gauge structure SU(4)\_C × SU(2)\_L × SU(2)\_R from the Palatini bracket [e, ω] on sl(4, ℝ), reducing the Standard Model's 19+ parameters to 6 inputs.

---

## 2. The Adversarial Compression Methodology

Every claim goes through this cycle:

```
CONJECTURE → EXPLICIT COMPUTATION → RESULT
                                      ├── Survives → compress to THEOREM (with proof)
                                      ├── Fails    → record as NEGATIVE RESULT (with computation)
                                      └── Partial  → record as OBSERVATION (with scope boundary)
```

**Rules (never violate these):**
- Never dress a conjecture in theorem language until the proof is complete
- Negative results are first-class outputs, not failures — document the conjecture, the killing computation, the mechanism of failure, and the boundary it establishes
- Every scope boundary must be explicit: what the result DOES and DOES NOT claim
- Overclaiming is the primary failure mode — correct it immediately when found
- When a "115-dimensional subalgebra" turns out to be gl(12) upon proper saturation, say so and explain why the earlier result was wrong

---

## 3. The Four-Tier Verification Hierarchy

| Tier | Standard | Example |
|------|----------|---------|
| **1. Machine-verified** | Automated test passes, reproducible by running code | `verify_n2_signature.py`: 4/4 PASS |
| **2. Proved in paper** | Complete mathematical proof, human-verified | N2 Theorem 1: cluster coherence via bilinearity |
| **3. Numerically verified** | Consistent across tests, not yet theorem-level | Compact → trivial grading (16 cases) |
| **4. Explicitly falsified** | Computation shows claim is false, documented | CW 6→5 reduction: fermion-dominated, boundary min |

When reporting results, always state which tier. Never let Tier 3 pass as Tier 2.

---

## 4. Current Framework State

### 4.1 Document Collection

| ID | Title | Pages |
|----|-------|------:|
| Paper A | Colour from Gravity: Pati-Salam from Palatini Bracket | 44 |
| Paper B | Information Asymmetry and the Riemann Spectral ACS | 15 |
| Paper C | The Inversion Arc: Holographic Resolution in ACS | 14 |
| Note N1 | Pythagorean Arithmetic Structure | 5 |
| Note N2 | Grading Selection from Adjoint Spectral Activity | 9 |

**Total: 87 pages, ~6500 lines TeX. Zero undefined citations across all documents.**

### 4.2 Parameter Ledger (6 Inputs)

**Free parameters (4):**

| Parameter | Range | Controls | Notes |
|-----------|-------|----------|-------|
| ρ₁ | (0, 8/9) | Higgs-triplet self-coupling | |
| α₁ | \|α₁\| < 0.81 | Higgs-triplet portal coupling | |
| tan β | (0, ∞) | Bi-doublet VEV ratio | **Gauge-protected flat direction.** Cannot be fixed perturbatively in minimal bi-doublet sector. PS gauge symmetry forces h̃/h to be RG invariant, two-loop QCD is multiplicative, thresholds are β-independent. Requires Branch B with Σ ~ (15,1,1) or non-perturbative effects. |
| v_R | unconstrained | Right-handed breaking scale | Sets proton decay rate and heavy boson masses |

**Calibrations (2):** v = 246.22 GeV (measured), v_R (to be measured)

**Locked (algebraically fixed):**

| Quantity | Value | Mechanism |
|----------|-------|-----------|
| λ_φ (Higgs quartic) | 2√3/27 ≈ 0.1283 | Koide projection |
| h̃/h (Yukawa ratio) | 2/3 | Koide ratio |
| g₄ = g_L = g_R | 4/3 | Palatini bracket |
| 2ρ₁ + ρ₂ | 16/9 | Palatini pairing |
| α₂ | 0 | Representation theory (Phase 50) |
| β_c (tree) | 0 | Phase 51/52 equal-VEV no-go |
| N_gen | 3 | Jacobi truncation at BCH order 3 |
| γ (Barbero-Immirzi) | 0.274 | Information balance / Meissner counting (confirmed exactly: λ₀ = 1.722013) |

### 4.3 Proved Theorems (10)

| # | Result | Location | Method |
|---|--------|----------|--------|
| 1 | SU(3) closure attractor | Paper A | BCH + computational |
| 2 | λ_φ = 2√3/27 | Paper A | Koide projection |
| 3 | α₂ = 0 | Paper A §5.5.1 | T^A Φ = 0 |
| 4 | β_c = 0 no-go | Paper A §5.5.1 | Mass matrix rank |
| 5 | Killing-orthogonality | Paper C Thm 4.1 | Direct trace |
| 6 | Three-class spectral taxonomy | Paper C Thm 4.2 | Jordan-Chevalley |
| 7 | Wronskian ≠ Poisson | Paper B Rem 2.3 | Leibniz fails by −fgh' |
| 8 | RH ⇒ stationarity | Paper B | Functional analysis |
| 9 | von Koch stability | Paper B Thm 2.4 | Log-coordinate reformulation |
| 10 | **General grading selection** | **N2 Thm 1** | **Bilinearity + weighted max-cut** |

### 4.4 Falsified Claims (8)

| # | Claim | How Killed | Mechanism |
|---|-------|-----------|-----------|
| 1 | ad³ = 2·ad for integers | Requires λ = 1/√2 | Eigenvalue constraint |
| 2 | Universal 2π inversion | sl(4) hyperbolic | Spectral classification |
| 3 | Wronskian Poisson | Leibniz fails by −fgh' | Direct computation |
| 4 | IR lattice imprint | z-scores null vs PDG | Statistical null test |
| 5 | Intrinsic chirality | Bias vanishes under covariant conjugation | Invariance testing |
| 6 | Route A (Killing form) | Cartan ≠ parity involution | Classification |
| 7 | Route C (stability) | All signatures equal holonomy norms | Computation |
| 8 | **CW 6→5** | **Gauge-protected flat direction** | **RG invariance + multiplicative QCD + β-independent thresholds** |

### 4.5 Open Problems (6)

| # | Problem | Requires | Impact |
|---|---------|----------|--------|
| 1 | FeynRules/UFO export | Engineering | LHC-testable predictions |
| 2 | Hilbert-Pólya operator | Different domain | RH connection |
| 3 | Action principle for S̃_g | Variational theory | First-principles derivation |
| 4 | L-functions extension | LMFDB zeros | Paper B generality |
| 5 | SM from GL(4) fiber | Conceptual breakthrough | Full SM derivation |
| 6 | ER=EPR correspondence | Conceptual breakthrough | Holographic interpretation |

---

## 5. Scope Honesty Standards (Must Always Be Stated)

### 5.1 Coleman-Mandula Rule
The N2 grading selection theorem selects a grading of the **internal carrier space**, NOT of physical spacetime. Any discussion connecting the (3,1) grading to Lorentzian signature MUST include the Coleman-Mandula constraint and the three bridging mechanisms (soldering, pre-geometry, CM evasion). This is never optional.

### 5.2 Exceptional Algebra Boundary
Cluster coherence (N2 Theorem 1(i)) holds for classical Lie algebra types (A, B, C, D) where interaction weights factor through eigenvalue clusters. It **fails** for exceptional algebras — G₂ counterexample proved (Proposition in N2). The failure mechanism: eigenvalue clusters in G₂ contain roots of multiple lengths, breaking the bilinear factorization. Always state the factorization condition.

### 5.3 Barbero-Immirzi Gap
γ = 0.274 is the unconstrained (Meissner) value, confirmed exactly. The physical value γ = 0.2375 (Domagala-Lewandowski) requires the SU(2) Gauss constraint via Chern-Simons projection — a **global** singlet projection on the multi-puncture tensor product, NOT a local degeneracy removal. Mechanism identified; exact derivation requires external CS computation.

### 5.4 Neutrino Tension
The naive Type-I see-saw mixing angle sin²(2θ) ≈ 4 × 10⁻⁶ is excluded by X-ray bounds (< 10⁻¹⁰). PS gauge-sector suppression (M_W/M_{W_R})² may resolve this. Tension is flagged, not resolved.

### 5.5 tan β Protection
This is NOT "we couldn't fix it." It IS "the PS gauge structure prevents perturbative fixing in the minimal sector." Three independent arguments: (1) h̃/h is an RG invariant, (2) two-loop QCD is multiplicative, (3) threshold corrections are β-independent. Fixing requires non-minimal Higgs or non-perturbative physics.

---

## 6. Computation Toolkit

### 6.1 Lie Algebra Basis Construction

```python
import numpy as np

def build_sln_basis(n):
    """
    Build basis for sl(n, R): n²-1 traceless n×n real matrices.
    Returns: (n-1) Cartan + n(n-1)/2 antisymmetric + n(n-1)/2 symmetric
    """
    basis = []
    for k in range(n - 1):
        H = np.zeros((n, n)); H[k, k] = 1; H[k+1, k+1] = -1
        basis.append(H)
    for i in range(n):
        for j in range(i + 1, n):
            A = np.zeros((n, n)); A[i, j] = 1; A[j, i] = -1
            basis.append(A)
    for i in range(n):
        for j in range(i + 1, n):
            S = np.zeros((n, n)); S[i, j] = 1; S[j, i] = 1
            basis.append(S)
    return basis
```

### 6.2 Adjoint Representation

```python
def compute_ad(T, basis):
    """ad_T matrix: (ad_T)_{ji} = Tr([T, b_i] · b_j) / Tr(b_j²)"""
    n = len(basis)
    ip = [np.trace(b @ b) for b in basis]
    ad = np.zeros((n, n))
    for i, bi in enumerate(basis):
        comm = T @ bi - bi @ T
        for j, bj in enumerate(basis):
            if abs(ip[j]) > 1e-12:
                ad[j, i] = np.trace(comm @ bj) / ip[j]
    return ad

def P_adjoint(P, basis):
    """Adjoint of involution σ_P: X → PXP⁻¹"""
    n = len(basis)
    ip = [np.trace(b @ b) for b in basis]
    Pinv = np.linalg.inv(P)
    Pa = np.zeros((n, n))
    for i, bi in enumerate(basis):
        Pbi = P @ bi @ Pinv
        for j, bj in enumerate(basis):
            if abs(ip[j]) > 1e-12:
                Pa[j, i] = np.trace(Pbi @ bj) / ip[j]
    return Pa
```

### 6.3 Grading Selection Functional

```python
def spectral_f(ad_T, f_func):
    """f(ad_T) via spectral theorem"""
    evals, evecs = np.linalg.eig(ad_T)
    f_evals = np.array([f_func(e.real) for e in evals])
    return evecs @ np.diag(f_evals) @ np.linalg.inv(evecs)

def grading_functional(P_ad, f_ad):
    """S̃_g[P] = Tr(σ_P · g(ad_T))"""
    return np.trace(P_ad @ f_ad)

def find_optimal_grading(T, n, g_func=lambda x: x**2):
    """Brute-force over 2^{n-1} partitions. Returns (P, value, shape, coherent)."""
    from itertools import product as itprod
    basis = build_sln_basis(n)
    ad_T = compute_ad(T, basis)
    f_ad = spectral_f(ad_T, g_func)
    best_val, best_P = float('inf'), None
    for signs in itprod([-1, 1], repeat=n-1):
        eps = list(signs) + [1]
        P = np.diag(eps)
        Pa = P_adjoint(P, basis)
        val = grading_functional(Pa, f_ad)
        if val < best_val:
            best_val = val; best_P = np.array(eps)
    n_minus = sum(1 for e in best_P if e == -1)
    shape = (n - n_minus, n_minus)
    # Coherence check
    t_diag = np.diag(T)
    coherent = True
    for e in sorted(set(np.round(t_diag, 8))):
        idx = [i for i in range(n) if abs(t_diag[i] - e) < 1e-6]
        if len(set(best_P[i] for i in idx)) > 1: coherent = False
    return best_P, best_val, shape, coherent

# Standard Cartan elements
T_BL = np.diag([1/3, 1/3, 1/3, -1.0])  # B-L generator in sl(4)
```

### 6.4 Root Systems

```python
def G2_roots():
    """G₂: 12 roots in R³ (the exceptional counterexample)"""
    short = [(1,-1,0),(0,1,-1),(-1,0,1),(-1,1,0),(0,-1,1),(1,0,-1)]
    long = [(2,-1,-1),(-1,2,-1),(-1,-1,2),(-2,1,1),(1,-2,1),(1,1,-2)]
    return [np.array(r, dtype=float) for r in short + long]

def classical_roots(type_letter, rank):
    """Root systems for A_n, B_n, C_n, D_n"""
    if type_letter == 'A':
        n = rank + 1
        return [np.array([1*(i==a) - 1*(i==b) for i in range(n)], dtype=float)
                for a in range(n) for b in range(n) if a != b]
    elif type_letter == 'B':
        n = rank; roots = []
        for i in range(n):
            for j in range(i+1, n):
                for si in [1,-1]:
                    for sj in [1,-1]:
                        r = np.zeros(n); r[i]=si; r[j]=sj; roots.append(r)
            for s in [1,-1]:
                r = np.zeros(n); r[i]=s; roots.append(r)
        return roots
    elif type_letter == 'D':
        n = rank; roots = []
        for i in range(n):
            for j in range(i+1, n):
                for si in [1,-1]:
                    for sj in [1,-1]:
                        r = np.zeros(n); r[i]=si; r[j]=sj; roots.append(r)
        return roots
    elif type_letter == 'C':
        n = rank; roots = []
        for i in range(n):
            for j in range(i+1, n):
                for si in [1,-1]:
                    for sj in [1,-1]:
                        r = np.zeros(n); r[i]=si; r[j]=sj; roots.append(r)
            for s in [1,-1]:
                r = np.zeros(n); r[i]=2*s; roots.append(r)
        return roots
```

### 6.5 Coleman-Weinberg Potential

```python
def V_CW_bidoublet(beta, h=1.0, ht=2/3, lam=2*np.sqrt(3)/27, mu=1.0):
    """One-loop CW for PS bi-doublet. Returns V_fermion + V_scalar."""
    Nc = 3
    mt2 = (h*np.cos(beta) + ht*np.sin(beta))**2
    mb2 = (h*np.sin(beta) + ht*np.cos(beta))**2
    V = 0
    for m2 in [mt2, mb2]:
        if m2 > 1e-20:
            V += -Nc/(16*np.pi**2) * m2**2 * (np.log(m2/mu**2) - 1.5)
    for m2 in [8*lam*np.cos(beta)**2, 8*lam*np.sin(beta)**2]:
        if m2 > 1e-20:
            V += 1/(64*np.pi**2) * m2**2 * (np.log(m2/mu**2) - 1.5)
    return V
# Key: h²/λ ≈ 7.8 → fermion-dominated → boundary minimum → tan β unfixed
```

### 6.6 Spectral Gap for Rewrite Systems

```python
def cyclic_eigenvalue(k, N, w=0.3):
    """Exact: λ_k = (1-w) + w cos(2πk/N) for N-cycle graph"""
    return (1 - w) + w * np.cos(2 * np.pi * k / N)

def graph_contraction_rate(adj_matrix, w=0.3):
    """Second eigenvalue of L = (1-w)I + wP controls all contraction."""
    degrees = adj_matrix.sum(axis=1)
    P = adj_matrix / degrees[:, None]
    L = (1-w) * np.eye(len(adj_matrix)) + w * P
    evals = np.sort(np.linalg.eigvals(L).real)[::-1]
    return abs(evals[1])  # |λ₂| = contraction rate
# Independent of matrix dimension, fiber algebra, nonlinear alignment, initial conditions
```

### 6.7 Wronskian and Spectral Tests (Paper B)

```python
def wronskian_test(zeros, x=1.0):
    """Test W[cos(γ_j x), cos(γ_k x)] ≠ 0 for all pairs."""
    N = len(zeros); n_vanish = 0
    for j in range(N):
        for k in range(j+1, N):
            W = (zeros[j]*np.sin(zeros[j]*x)*np.cos(zeros[k]*x) - 
                 zeros[k]*np.cos(zeros[j]*x)*np.sin(zeros[k]*x))
            if abs(W) < 1e-15: n_vanish += 1
    return N*(N-1)//2, n_vanish  # (total_pairs, vanishing_pairs)

def cross_correlation_bound(zeros, x_max=50, n_pts=1000):
    """Max |C_N|. Paper B requires < 0.29."""
    N = len(zeros); C_max = 0
    for x in np.linspace(0.1, x_max, n_pts):
        C = sum(np.cos((zeros[j]-zeros[k])*x) for j in range(N) for k in range(j+1,N))
        C_max = max(C_max, 2*abs(C)/(N*(N-1)))
    return C_max
# Verified: 19900/19900 pairs at N=200, C_200 = 0.044 << 0.29
```

---

## 7. Document Management

### 7.1 Cross-Reference Network

```
Paper A → Paper B (WallaceB), Paper C (WallaceC), N1 (WallaceN1), N2 (WallaceN2)
Paper B → Paper A (Wallace2026a)
Paper C → Paper A (Wallace2026a), Paper B (Wallace2026b), N2 (WallaceN2)
N1 → Paper A (WallaceA)
N2 → Paper A (WallaceA), N1 (WallaceN1), Coleman-Mandula (1967), HLS (1975)
```

### 7.2 Notation Conventions

| Context | Functional | Involution | Notes |
|---------|-----------|------------|-------|
| N2, g(0)=0 | $\widetilde{\mathcal{S}}_g$ | $\sigma_P$ | The main theorem |
| N2, f(0)>0 | $\mathcal{S}_f$ | $\sigma_P$ | Separate Proposition (zero-mode) |
| Paper A | Expanded $\mathrm{Tr}(...)$ | — | No macros — all explicit |

Never mix S\_f and S̃\_g without specifying which regime.

### 7.3 Compilation and Verification

```bash
# Compile all (3 passes for cross-refs)
for d in papers/core_trilogy/ papers/notes/ papers/methodology/ papers/later_FF06_series/; do
    cd "$d" && pdflatex -interaction=nonstopmode main.tex >/dev/null 2>&1
    pdflatex -interaction=nonstopmode main.tex >/dev/null 2>&1
    pdflatex -interaction=nonstopmode main.tex >/dev/null 2>&1
    rm -f main.aux main.log main.out main.toc && cd ../..
done

# Citation check (should print nothing)
for doc in papers/core_trilogy/*.tex papers/notes/*.tex; do
    cites=$(grep -oP '\\cite\{[^}]+\}' "$doc" | sed 's/\\cite{//;s/}//;s/,/\n/g' | sort -u)
    bibs=$(grep -oP '\\bibitem\{[^}]+\}' "$doc" | sed 's/\\bibitem{//;s/}//' | sort -u)
    for c in $cites; do
        echo "$bibs" | grep -qx "$c" || echo "UNDEFINED in $(dirname $doc): $c"
    done
done

# Run all tests
python3 code/verify_n2_signature.py && python3 code/verify_n1_lattice.py && python3 code/verify_cw_analysis.py
```

### 7.4 After Any Edit

1. Compile the edited paper (3 passes)
2. Check for undefined references
3. If cross-references changed, check ALL five documents
4. Run the relevant test suite
5. Rebuild the tarball

---

## 8. The Palatini → Pati-Salam Pipeline (Quick Reference)

```
[e, ω] on sl(4,ℝ)  ──BCH──→  Order 0: frame + connection (16+24 components)
                               Order 1: Higgs bi-doublet Φ ~ (1,2,2)
                                 └─ quartic λ = 2√3/27, Yukawa h̃/h = 2/3
                               Order 2: gauge bosons
                                 └─ SU(3) closure attractor, 12 PS bosons
                               Order 3: three generations
                                 └─ Jacobi truncation (order 4+ vanishes)

Gauge structure: SU(4)_C × SU(2)_L × SU(2)_R  (Pati-Salam, 1974)
Parameters: 19+ (SM) → 6 (ACS Branch A) = 4 free + 2 calibrations
```

---

## 9. Key Results in One Sentence Each

1. **SU(3) attractor:** The Palatini bracket's BCH expansion converges to SU(3) regardless of starting point.
2. **Higgs quartic:** λ = 2√3/27 ≈ 0.128, matching experiment (0.129) to 0.84%.
3. **Three generations:** Jacobi identity truncates at order 3; no fourth generation.
4. **Grading selection:** Minimizing adjoint spectral activity selects (3,1) grading for T\_{B-L}. Proof: g(0)=0 → bilinear in magnetizations → splitting never helps → weighted max-cut.
5. **CW negative:** tan β is gauge-protected; parameter count stays at 6 in minimal sector.
6. **Wronskian structure:** Zero-mode functions form a Lie algebra but NOT Poisson (Leibniz fails).
7. **Spectral control:** Rewrite system contraction rate = |λ₂| of graph propagator, independent of everything else.
8. **G₂ boundary:** Cluster coherence fails for exceptional algebras (multi-length root clusters).

---

## 10. What To Do When Starting a New Session

1. Read this skill to load the full context
2. Check `references/framework_state.md` for current parameter ledger and open problems
3. Ask the user which cluster of problems to work on
4. Apply adversarial compression: conjecture → test → compress or kill
5. After any paper edit: compile → check refs → run tests → bundle
6. After any new result: classify it (Tier 1-4) and update the relevant paper

---

*Nothing more is assumed. Nothing less is computed.*
