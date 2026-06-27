#!/usr/bin/env python3
"""
PHASE 51: COLEMAN-WEINBERG ANALYSIS OF tan β
=============================================

Question: does β_c uniquely fix tan β at one-loop, or is there a
residual flat direction?

If β_c alone determines tan β, the free parameter count drops from
4 to 3, and the total input count drops from 6 to 5. That would be a
major strengthening of Branch A.

Approach:
  1. Write V_tree(κ_1, κ_2, v_R) including β_c term explicitly.
  2. Identify the flat direction at tree level (when β_c=0).
  3. Compute the Coleman-Weinberg correction from heavy fields.
  4. Extremize V_eff = V_tree + ΔV_CW with respect to tan β.
  5. Check: is tan β determined uniquely, or degenerate?
"""
import numpy as np
from sympy import symbols, sqrt, Rational, simplify, diff, solve, expand
from sympy import Symbol, cos, sin, atan2, pi, log as symlog
from sympy import Matrix, zeros, eye, I as sym_I, re, im

print("=" * 72)
print("PHASE 51: ONE-LOOP EFFECTIVE POTENTIAL AND tan β DETERMINATION")
print("=" * 72)

# ============================================================
# STEP 1: TREE-LEVEL POTENTIAL WITH β_c
# ============================================================

print(r"""
TREE-LEVEL POTENTIAL (with β_c, α_2 = 0 from Phase 50):

  V_tree = -μ²_Φ Tr(Φ†Φ) + λ_Φ [Tr(Φ†Φ)]²
         - μ²_Δ Tr(Δ_R†Δ_R) + ρ_1 [Tr(Δ_R†Δ_R)]² + ρ_2 Tr[(Δ_R†Δ_R)²]
         + α_1 Tr(Φ†Φ) Tr(Δ_R†Δ_R)
         + [β_c Tr(Φ† Φ̃ Δ_R† Δ_R) + h.c.]

where Φ̃ = τ_2 Φ* τ_2 is the charge-conjugate bi-doublet.

At the VEV Φ = diag(κ_1, κ_2) with real κ_1, κ_2:
  Tr(Φ†Φ)       = κ_1² + κ_2²
  Tr(Φ† Φ̃)      = κ_1 κ_2 + κ_1 κ_2 = 2 κ_1 κ_2    [for real VEVs]
  Tr(Δ_R†Δ_R)   = v_R²  (rank-1 VEV)

So the β_c term at real VEV:
  β_c Tr(Φ† Φ̃ Δ_R† Δ_R) + h.c. = 2 Re(β_c) · 2 κ_1 κ_2 · v_R²
                                 = 4 Re(β_c) κ_1 κ_2 v_R²

For the magnitude analysis, treat β_c as real (the phase part is
irrelevant to the CP-conserving vacuum structure).
""")

# Work in terms of (v², tan β, v_R²)
# κ_1 = v cos β, κ_2 = v sin β, so:
#   κ_1² + κ_2² = v²
#   κ_1 κ_2 = (v²/2) sin(2β)

v, v_R, beta, mu_phi_sq, mu_del_sq = symbols('v v_R beta mu_Phi^2 mu_Delta^2', 
                                               positive=True, real=True)
lam_phi = Rational(2) * sqrt(3) / 27
rho1 = symbols('rho_1', real=True, positive=True)
rho2 = Rational(16, 9) - 2 * rho1
alpha1 = symbols('alpha_1', real=True)
beta_c = symbols('beta_c', real=True)

# Tree potential at VEV
phi_sq = v**2
del_sq = v_R**2
phi_phi_tilde = v**2 * sin(2*beta) / 2  # Tr(Φ† Φ̃) evaluated at VEV

V_tree = (-mu_phi_sq * phi_sq 
          + lam_phi * phi_sq**2
          - mu_del_sq * del_sq
          + (rho1 + rho2) * del_sq**2
          + alpha1 * phi_sq * del_sq
          + 4 * beta_c * phi_phi_tilde * del_sq / 2)  # factor: 2·β_c·(phi_phi_tilde)·v_R²
# Let me re-derive: β_c Tr(Φ†Φ̃Δ†Δ) + h.c. = 2·Re(β_c)·Tr(Φ†Φ̃)·Tr(Δ†Δ)
# = 2·β_c·(v²/2)·sin(2β)·v_R² = β_c·v²·sin(2β)·v_R²
V_tree = (-mu_phi_sq * v**2 
          + lam_phi * v**4
          - mu_del_sq * v_R**2
          + (rho1 + rho2) * v_R**4
          + alpha1 * v**2 * v_R**2
          + beta_c * v**2 * sin(2*beta) * v_R**2)

print(f"V_tree(v, β, v_R) after reparameterization:")
print(f"  V_tree = −μ²_φ v² + λ_φ v⁴")
print(f"         − μ²_Δ v_R² + (ρ_1 + ρ_2) v_R⁴")
print(f"         + α_1 v² v_R²")
print(f"         + β_c v² sin(2β) v_R²")

# Key observation: tan β only appears through sin(2β) in the β_c term
print(r"""
KEY OBSERVATION:
  The only tan-β dependence in V_tree is through sin(2β) in the β_c term.
  
  dV_tree/dβ = 2 β_c v² v_R² cos(2β)
  
  Setting this to zero gives:
    cos(2β) = 0    (if β_c ≠ 0 and v, v_R ≠ 0)
    2β = π/2 + n·π
    β = π/4 + n·π/2  →  tan β = ±1 (all four critical points)
  
  So AT TREE LEVEL, β_c selects tan β = ±1 (when β_c ≠ 0).
  
  Second derivative test: 
    d²V/dβ² = -4 β_c v² v_R² sin(2β)
  
  At β = π/4: sin(2β) = 1, so d²V/dβ² = -4 β_c v² v_R²
    This is a MAX if β_c > 0, MIN if β_c < 0.
  At β = 3π/4: sin(2β) = -1, flipped sign.
  
  So for EITHER sign of β_c, one of {π/4, 3π/4} is a minimum → tan β = ±1.
""")

# ============================================================
# STEP 2: CHECK THE TREE-LEVEL RESULT EXPLICITLY
# ============================================================

dV_dbeta = diff(V_tree, beta)
print(f"\n∂V_tree/∂β = {simplify(dV_dbeta)}")

d2V_dbeta2 = diff(V_tree, beta, 2)
print(f"∂²V_tree/∂β² = {simplify(d2V_dbeta2)}")

print(r"""
TREE-LEVEL RESULT:
  β_c ≠ 0 forces tan β = ±1 (i.e., κ_1 = ±κ_2) at TREE LEVEL.

But this is a problem:
  tan β ≈ 60 is needed phenomenologically to get the top-bottom mass 
  hierarchy (m_t/m_b ≈ 40, with Palatini ratio h̃/h = 2/3).

So tree-level β_c cannot give the right tan β.
The β_c term as written is INCONSISTENT with large tan β.

This is a GENUINE TENSION that Phase 51 must resolve.
""")

# ============================================================
# STEP 3: WHAT DOES THIS TENSION MEAN?
# ============================================================

print("=" * 72)
print("ANALYSIS OF THE TENSION")
print("=" * 72)

print(r"""
Option (i): β_c must be very small (but not zero).
  If β_c ≪ other quartics, the β_c-induced tan β minimization becomes
  soft, and other effects (loop corrections, higher-dimension operators) 
  can dominate and shift tan β to its phenomenological value.
  
  Order-of-magnitude estimate: for the tree-level β_c to be subleading,
  we need β_c v²v_R² ≪ (other terms at minimum). Since other terms 
  scale like λ_φ v⁴ ~ 10⁻¹·(246)⁴ ≈ 4×10⁸ GeV⁴, and β_c v²v_R² 
  = β_c·6×10⁴·10³⁰, we need β_c ≪ 10⁻²⁶. 
  
  This is unnatural — β_c would need extreme fine-tuning to be so small.

Option (ii): the β_c term as written doesn't actually appear at tree level.
  Re-examination: does Tr(Φ† Φ̃ Δ_R† Δ_R) actually come from the 
  Palatini bracket, or is it an assumed additional term?
  
  Check: Φ̃ = τ_2 Φ* τ_2. For a (1,2,2) bi-doublet, Φ̃ is the 
  CP-conjugate. The operator Tr(Φ† Φ̃) transforms as:
    - (1,2,2) × (1,2̄,2̄) → contains SU(2)_L × SU(2)_R singlets
  and so is gauge-invariant.
  
  Multiplied by Tr(Δ_R† Δ_R) gives a total singlet. So YES, this 
  term is allowed by gauge invariance.
  
  But: does the Palatini bracket actually PRODUCE this term? In 
  Paper A's construction, β_c was introduced as a free parameter
  without explicit bracket derivation.

Option (iii): the tree-level "tan β = ±1" is actually a SYMMETRY 
constraint, and phenomenological tan β comes from a DIFFERENT 
mechanism.
  
  If the bi-doublet really has tan β = 1 at the Lagrangian level,
  the m_t/m_b hierarchy must come entirely from the Yukawa matrix 
  eigenvalues, NOT from VEV ratios.
  
  But this is what Paper A's h̃/h = 2/3 already says! The Yukawa 
  ratio is 2/3, giving m_t/m_b = (v_u·y_t)/(v_d·y_b) ≈ 1·y_t/y_b.
  If tan β = 1 (v_u = v_d), then m_t/m_b is entirely from the 
  Yukawa matrix.

PHENOMENOLOGY CHECK:
  m_t ≈ 173 GeV, m_b ≈ 4.18 GeV, m_t/m_b ≈ 41.4
  
  If tan β = 1, we need y_t/y_b ≈ 41.4 directly.
  The Palatini ratio h̃/h = 2/3 says: same bi-doublet couples to 
  BOTH up-type and down-type with a FIXED ratio. So if m_t comes 
  from h·κ_1 and m_b comes from h̃·κ_1 (same κ_1!), then:
    m_t/m_b = h/h̃ = 3/2 = 1.5
  which is very different from 41.4.
  
  OR, if the Yukawa matrix in generation space provides the 
  hierarchy separately from the h/h̃ ratio — then tan β = 1 
  is just one constraint and the Yukawa texture does the rest.
""")

# ============================================================
# STEP 4: THE HONEST CONCLUSION
# ============================================================

print("=" * 72)
print("PHASE 51 VERDICT — THE tan β QUESTION")
print("=" * 72)

print(r"""
STATUS: tan β is NOT uniquely fixed by β_c in a phenomenologically 
viable way. The analysis reveals one of three outcomes:

  (A) Tree-level β_c forces tan β = ±1, but m_t/m_b = 41 requires
      either a different mechanism for the hierarchy, OR β_c is 
      fine-tuned to be negligible.

  (B) The β_c term as written is not actually generated by the 
      Palatini bracket — it's a phenomenological extension. Removing 
      it (β_c = 0 at tree level) leaves tan β as a genuine flat 
      direction, and Coleman-Weinberg corrections would need to lift it.

  (C) The Yukawa ratio h̃/h = 2/3 is incompatible with tan β = 1 if 
      m_t/m_b is generated by VEVs alone — but COMPATIBLE if the 
      hierarchy lives in Yukawa texture (as in flavor-structure models).

HONEST ANSWER: the current Phase 51 analysis does NOT demonstrate that
β_c uniquely fixes tan β to a phenomenologically viable value.
The expected reduction 6 → 5 does NOT materialize at tree level.

This is a genuine finding, not a null result. It tells us:
  • tan β is a free parameter sitting primarily in the Yukawa sector
  • β_c may need to be reinterpreted or removed from the Lagrangian
  • The Phase 50 count of 6 inputs stands; no further reduction here

NEXT STEPS IF PURSUING:
  (1) Work out what happens in the m_t/m_b Yukawa-hierarchy scenario 
      (tan β = 1 FIXED, hierarchy from Yukawa matrices).
      If self-consistent → potential 5-input model, but requires
      different Yukawa analysis than Paper A currently has.
  
  (2) Do full Coleman-Weinberg calculation including heavy W_R, Z_R,
      gauge bosons, and scalar modes. This requires:
        - complete mass spectrum of all fields at the VEV
        - β-function of all couplings at one-loop
        - renormalization group improvement
      Estimated effort: 2-4 weeks of dedicated symbolic + numerical 
      computation.
  
  (3) Accept that tan β is free (6-input model) and proceed.

RECOMMENDATION: 
  The honest paper statement is option (3) for now, with a footnote 
  or appendix explaining that dedicated Coleman-Weinberg analysis 
  might reveal tan β fixation but is beyond the scope of the current 
  derivation.
""")

# ============================================================
# STEP 5: ONE-LOOP ADDITIONAL CONSIDERATION
# ============================================================

print("=" * 72)
print("COLEMAN-WEINBERG SKELETON")
print("=" * 72)

print(r"""
Full Coleman-Weinberg correction:

  ΔV_CW(φ) = (1/64π²) Σ_i n_i m_i⁴(φ) [ln(m_i²(φ)/μ²) − C_i]

  where the sum is over all species (bosons +1, fermions -1, n_i
  counts physical degrees of freedom), m_i(φ) is the field-dependent
  mass, μ is the renormalization scale, C_i = 3/2 for scalars and
  fermions, 5/6 for gauge bosons.

FIELDS CONTRIBUTING in PS with Branch A content:
  - Φ bi-doublet: 8 real d.o.f., 4 physical masses after Goldstone eating
  - Δ_R triplet: 10 real d.o.f., 9 physical (one eaten by SU(2)_R breaking)
  - Gauge bosons: SU(4) has 15, SU(2)_L has 3, SU(2)_R has 3 = 21 gauge bosons
  - Fermions: 3 generations × (4,2,1)+(4,1,2) = 3 × 16 = 48 Weyl fermions
               per generation

Each field's mass at the VEV depends on β (via κ_1 = v cos β, κ_2 = v sin β).
The β-dependence of ΔV_CW therefore depends on:

  (a) Which fields have tan-β-dependent masses at tree level?
      → top quark (via y_t κ_1 or y_t κ_2 depending on which bi-doublet 
        component it couples to)
      → bottom quark (similarly, with the conjugate bi-doublet)
      → tau lepton (similarly)
      → W_L mass depends on κ_1² + κ_2² = v² only (not on β) 
      → charged Higgs mass matrix has β-dependence

  (b) Does the net ΔV_CW have a β-dependent piece that shifts the 
      tree-level tan β = ±1 result?
      → If yes: the shift might reach the phenomenological tan β ≈ 60.
      → If no: tan β remains at ±1, incompatible with data.

LEADING CONTRIBUTION AT ONE LOOP:
  The largest tan-β-dependent term is the top-quark loop:
    ΔV_t ≈ -(3/16π²) (y_t κ_u)⁴ ln[(y_t κ_u)²/μ²]
  where κ_u = κ_1 for tan β > 1 convention (or κ_2; convention matters).

  dΔV_t/dβ has a finite, non-trivial β-dependence. In the MSSM, this 
  generates tan β radiatively via the known radiative EWSB mechanism.

EXTRAPOLATION TO PS:
  The radiative-EWSB mechanism is well-known in 2-Higgs-doublet models
  (MSSM is the classic example). In that context, tan β is indeed fixed 
  by the interplay of (tree-level μ²-type terms) and (loop corrections
  from large Yukawas).

  For PS with the ACS constraints:
    - λ_φ = 2√3/27 is FIXED (cannot absorb loop corrections)
    - α_1, β_c are free but tree-level
    - ρ_1 is free
    - Top Yukawa y_t ≈ 1 at EW scale, h̃/h = 2/3 locked

  A FULL CW calculation would determine whether the tree-tan β = ±1 
  drifts to the phenomenological tan β ≈ 60 under radiative corrections,
  OR whether the two are incompatible.

This is a genuine open question. It requires 2-4 weeks of focused 
symbolic work to answer definitively.

INTERIM STATUS: tan β remains a free parameter in the Phase 50 ledger.
Branch A stays at 6 inputs.
""")
