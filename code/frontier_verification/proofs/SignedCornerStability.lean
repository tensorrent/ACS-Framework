import Mathlib.Basic.Real.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

set_option autoImplicit false

namespace SignedCornerStability
open Matrix

theorem inverse_difference {T : Type*} [Ring T] (A B X Y : T)
    (hXA : X * A = 1) (hBY : B * Y = 1) :
    X - Y = X * (B - A) * Y := by
  calc
    X - Y = X * (B * Y) - (X * A) * Y := by rw [hBY, hXA, mul_one, one_mul]
    _ = X * (B - A) * Y := by simp only [mul_sub, sub_mul, mul_assoc]

theorem column_action {n : Type*} [Fintype n] [DecidableEq n]
    (X : Matrix n n ℝ) (d v : n → ℝ) (j r : n) :
    (X *ᵥ ((fun i k => if k = j then d i else 0) *ᵥ v)) r =
      (X *ᵥ d) r * v j := by
  simp [Matrix.mulVec, dotProduct, ite_mul, Finset.sum_mul, mul_assoc]

theorem inverse_column_replacement {n : Type*} [Fintype n] [DecidableEq n]
    (A B X Y : Matrix n n ℝ) (d v : n → ℝ) (j r : n)
    (hXA : X * A = 1) (hBY : B * Y = 1)
    (hd : B - A = fun i k => if k = j then d i else 0) :
    (X *ᵥ v) r - (Y *ᵥ v) r = (X *ᵥ d) r * (Y *ᵥ v) j := by
  have h := congrArg (fun M : Matrix n n ℝ => (M *ᵥ v) r)
    (inverse_difference A B X Y hXA hBY)
  rw [Matrix.sub_mulVec, ← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, hd] at h
  simpa using h.trans (column_action X d (Y *ᵥ v) j r)

theorem cramer_column_numerator_invariant {n : Type*} [Fintype n] [DecidableEq n]
    (A : Matrix n n ℝ) (z v : n → ℝ) (j : n) :
    Matrix.cramer (A.updateCol j z) v j = Matrix.cramer A v j := by
  simp only [Matrix.cramer_apply]
  congr 1
  ext i k
  by_cases h : k = j
  · subst k; simp
  · simp [Matrix.updateCol_ne h]

theorem negative_quotient_transfer {numerator d₀ d : ℝ}
    (h₀ : numerator / d₀ < 0) (hs : d₀ * d > 0) : numerator / d < 0 := by
  apply div_neg_iff.mpr
  rcases div_neg_iff.mp h₀ with ⟨hn, hd⟩ | ⟨hn, hd⟩
  · exact Or.inl ⟨hn, by nlinarith⟩
  · exact Or.inr ⟨hn, by nlinarith⟩

theorem endpoint_step_nonnegative {old new first second : ℝ}
    (h : new - old = -first * second) (hs : first * second ≤ 0) : old ≤ new := by
  nlinarith

theorem convex_combination_upper {n : Type*} [Fintype n]
    (weights values : n → ℝ) (bound : ℝ)
    (hw : ∀ i, 0 ≤ weights i) (hs : ∑ i, weights i = 1)
    (hv : ∀ i, values i ≤ bound) : ∑ i, weights i * values i ≤ bound := by
  calc
    ∑ i, weights i * values i ≤ ∑ i, weights i * bound :=
      Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_left (hv i) (hw i)
    _ = bound := by rw [← Finset.sum_mul, hs, one_mul]

theorem replacement_chain (K : ℕ → ℝ) (m : ℕ)
    (h : ∀ i < m, K i ≤ K (i+1)) : K 0 ≤ K m := by
  induction m with
  | zero => exact le_rfl
  | succ m ih => exact le_trans (ih fun i hi => h i (Nat.lt_succ_of_lt hi)) (h m (Nat.lt_succ_self m))

#print axioms inverse_difference
#print axioms column_action
#print axioms inverse_column_replacement
#print axioms cramer_column_numerator_invariant
#print axioms negative_quotient_transfer
#print axioms endpoint_step_nonnegative
#print axioms convex_combination_upper
#print axioms replacement_chain

end SignedCornerStability
