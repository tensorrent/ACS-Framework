/-
  Co-governed and enforced under the Sovereign Integrity Protocol License (SIP v1.1):
  https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

  # The per-zero 2π contribution in Section 7 of the Constraint Projection Framework

  The audit's exact evaluation of the manuscript's defining integral rests on one
  step, stated in `cpf_triple_check.py` X3 and in the ledger (2026-08-30) as:

      for real α,  ∫ du/(α + iu) = arctan(u/α) − (i/2) ln(α² + u²)
      so a zero at β = 1/2 sees α = +ε and α = −ε, the IMAGINARY parts (which
      depend on α²) CANCEL identically, the REAL parts ADD, and

          contribution = 2[ arctan((T−γ)/ε) + arctan(γ/ε) ]  →  2π

      for any zero strictly inside 0 < γ < T.  That IS the residue count,
      derived without invoking the residue theorem.

  This file machine-checks that step.  Three separable claims, and the file is
  deliberate about which is which:

    * `imag_cancels`            the imaginary parts cancel EXACTLY, for every ε.
                                Pure evenness in α — no analysis needed.
    * `real_doubles`            the real parts combine to exactly
                                2[arctan((T−γ)/ε) + arctan(γ/ε)].
                                Pure oddness of arctan.
    * `contribution_lt_two_pi`  that quantity is STRICTLY below 2π for every ε.
    * `contribution_tendsto`    and tends to 2π as ε → 0⁺, for 0 < γ < T.

  The last two together are the honest form of the claim.  Writing "= 2π" would
  be wrong: at any finite ε the contribution is strictly less, and 2π is a
  supremum approached in the limit, not a value attained.  The audit's prose
  said "→ 2π", and that is what is proved here.

  WHAT IS NOT PROVED HERE.  That the closed form above IS the integral — i.e.
  the evaluation of ∫ du/(α+iu) itself — is not formalised; it is standard
  calculus and is taken as the definition of `realPart` / `imagPart`.  What is
  proved is everything the audit's argument does WITH that closed form: the
  cancellation, the doubling, the bound, and the limit.  That boundary is the
  point of the file and is not hidden.

  MATHLIB REQUIRED.  Unlike `../LFBound.lean` and `../AxiomIII.lean`, which check
  with a bare `lean` binary in under a second, this file needs ℝ, `arctan` and
  filter limits — all outside Lean core.  That raises a reader's verification
  cost from a 30-second install to a multi-gigabyte one, which is a real cost and
  is why the Mathlib-dependent proof lives in its own directory.

      cd code/constraint_projection/lean/withMathlib
      lake exe cache get        # ~5 GB, once
      lake env lean PerZero.lean    # exit 0 = verified

  Companion Python: cpf_triple_check.py check X3 (exact closed form over
  Odlyzko's 100k zeros, ratio to 2πN(T)/T = 0.999994 at T = 74,000).
  Ledger: docs/Elimination_Ledger.md, 2026-08-30.
-/

import Mathlib.Analysis.SpecialFunctions.Trigonometric.Arctan
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Topology.Algebra.Order.Field
import Mathlib.Order.Filter.AtTopBot.Field

open Real Filter Topology

namespace PerZero

/-- Real part of the closed form for `∫₀^T dt / (α + i(t − γ))`, with the
    substitution `u = t − γ` already made. -/
noncomputable def realPart (gamma T alpha : ℝ) : ℝ :=
  arctan ((T - gamma) / alpha) - arctan ((-gamma) / alpha)

/-- Imaginary part of the same.  Note `α` enters **only** through `α²` — this is
    the whole reason the imaginary parts cancel between the two lines. -/
noncomputable def imagPart (gamma T alpha : ℝ) : ℝ :=
  -(1 / 2) * (Real.log (alpha ^ 2 + (T - gamma) ^ 2) - Real.log (alpha ^ 2 + gamma ^ 2))

/-- The per-zero contribution: the `+ε` line minus the `−ε` line. -/
noncomputable def contribution (gamma T eps : ℝ) : ℝ :=
  2 * (arctan ((T - gamma) / eps) + arctan (gamma / eps))

/-! ## The imaginary parts cancel -/

/-- **The imaginary parts cancel exactly**, for every `ε` — no positivity or
    interior hypothesis needed.  `α` appears only as `α²`, so the two lines carry
    identical imaginary parts and the difference is identically zero. -/
theorem imag_cancels (gamma T eps : ℝ) :
    imagPart gamma T eps - imagPart gamma T (-eps) = 0 := by
  simp [imagPart]

/-! ## The real parts double -/

/-- **The real parts combine to exactly `2[arctan((T−γ)/ε) + arctan(γ/ε)]`**,
    because `arctan` is odd.  Again no hypothesis on `ε`: at `ε = 0` both sides
    are `0` under Lean's division convention, so the identity is unconditional. -/
theorem real_doubles (gamma T eps : ℝ) :
    realPart gamma T eps - realPart gamma T (-eps) = contribution gamma T eps := by
  simp only [realPart, contribution, div_neg, neg_div, neg_neg, arctan_neg]
  ring

/-! ## The bound and the limit -/

/-- **The contribution is STRICTLY below `2π`** for every `ε`, since
    `arctan < π/2` everywhere.  So `2π` is never attained at finite `ε`. -/
theorem contribution_lt_two_pi (gamma T eps : ℝ) : contribution gamma T eps < 2 * π := by
  have h1 := arctan_lt_pi_div_two ((T - gamma) / eps)
  have h2 := arctan_lt_pi_div_two (gamma / eps)
  simp only [contribution]
  linarith

/-- **…and it tends to `2π` as `ε → 0⁺`**, for a zero strictly inside `0 < γ < T`.
    Both arguments run to `+∞` because their numerators are positive, and
    `arctan → π/2` at `atTop`.  This is the sense in which each interior zero
    contributes `2π`: a supremum approached, not a value reached. -/
theorem contribution_tendsto (gamma T : ℝ) (hg : 0 < gamma) (hgT : gamma < T) :
    Tendsto (contribution gamma T) (𝓝[>] 0) (𝓝 (2 * π)) := by
  have hinv : Tendsto (fun eps : ℝ => eps⁻¹) (𝓝[>] (0 : ℝ)) atTop := tendsto_inv_nhdsGT_zero
  have h1 : Tendsto (fun eps : ℝ => (T - gamma) / eps) (𝓝[>] (0 : ℝ)) atTop := by
    simpa [div_eq_mul_inv] using Tendsto.const_mul_atTop (by linarith : (0:ℝ) < T - gamma) hinv
  have h2 : Tendsto (fun eps : ℝ => gamma / eps) (𝓝[>] (0 : ℝ)) atTop := by
    simpa [div_eq_mul_inv] using Tendsto.const_mul_atTop hg hinv
  have ha : Tendsto arctan atTop (𝓝 (π / 2)) :=
    tendsto_arctan_atTop.mono_right nhdsWithin_le_nhds
  have key : Tendsto (fun eps : ℝ => 2 * (arctan ((T - gamma) / eps) + arctan (gamma / eps)))
      (𝓝[>] 0) (𝓝 (2 * π)) := by
    simpa [Function.comp] using (((ha.comp h1).add (ha.comp h2)).const_mul 2)
  exact key

/-! ## The package -/

/-- **The per-zero `2π` contribution, in full.**

    For a zero at `β = 1/2` with `0 < γ < T`:
    1. the imaginary parts of the two lines cancel identically;
    2. the real parts combine to `2[arctan((T−γ)/ε) + arctan(γ/ε)]`;
    3. that is strictly below `2π` at every finite `ε`;
    4. and tends to `2π` as `ε → 0⁺`.

    Summing over the `N(T)` interior zeros gives `2π·N(T)`, which is the residue
    count — obtained here without invoking the residue theorem. -/
theorem per_zero_two_pi (gamma T : ℝ) (hg : 0 < gamma) (hgT : gamma < T) :
    (∀ eps : ℝ, imagPart gamma T eps - imagPart gamma T (-eps) = 0) ∧
    (∀ eps : ℝ, realPart gamma T eps - realPart gamma T (-eps) = contribution gamma T eps) ∧
    (∀ eps : ℝ, contribution gamma T eps < 2 * π) ∧
    Tendsto (contribution gamma T) (𝓝[>] 0) (𝓝 (2 * π)) :=
  ⟨imag_cancels gamma T, real_doubles gamma T, contribution_lt_two_pi gamma T,
   contribution_tendsto gamma T hg hgT⟩

end PerZero
