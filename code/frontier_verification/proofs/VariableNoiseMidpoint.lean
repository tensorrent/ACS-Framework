import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

namespace VariableNoiseMidpoint

theorem scaled_positive_interval {scale alpha lo hi : ℝ}
    (hs : 0 < scale) (hl : 0 < lo) (ha : lo ≤ alpha) (hb : alpha ≤ hi) :
    0 < scale * alpha ∧ scale * alpha ≤ scale * hi := by
  exact ⟨mul_pos hs (lt_of_lt_of_le hl ha), mul_le_mul_of_nonneg_left hb (le_of_lt hs)⟩

theorem affine_noise_column (base scale alpha step v : ℝ) :
    (base - 2 * scale * (alpha + step) * v) - (base - 2 * scale * alpha * v) =
      (-2 * scale * v) * step := by
  ring

theorem signed_midpoint_errors {a b tau v : ℝ}
    (hd : a - b = 2 * tau * v) (ht : 0 ≤ tau) (hv : |v| = 1) :
    |(a + b) / 2 - a| = tau ∧ |(a + b) / 2 - b| = tau := by
  have hA : (a + b) / 2 - a = -(tau * v) := by linarith
  have hB : (a + b) / 2 - b = tau * v := by linarith
  constructor
  · rw [hA, abs_neg, abs_mul, abs_of_nonneg ht, hv, mul_one]
  · rw [hB, abs_mul, abs_of_nonneg ht, hv, mul_one]

theorem common_release_budget_lower {a b z tau budget : ℝ}
    (hd : |a - b| = 2 * tau) (ha : |z - a| ≤ budget) (hb : |z - b| ≤ budget) :
    tau ≤ budget := by
  obtain ⟨hal, hau⟩ := abs_le.mp ha
  obtain ⟨hbl, hbu⟩ := abs_le.mp hb
  have h : |a - b| ≤ 2 * budget := abs_le.mpr ⟨by linarith, by linarith⟩
  rw [hd] at h
  linarith

theorem fixed_critical_gap {c epsilon a b : ℝ}
    (he : 0 < epsilon) (ha : a = c + epsilon) (hb : b = c - epsilon) :
    a - b = 2 * epsilon ∧ 0 < a - b := by
  constructor <;> linarith

theorem fixed_report_exclusion_is_not_global :
    |(0 : ℝ) - 2| > 1 ∧ |(0 : ℝ) - 4| > 1 ∧
      |(3 : ℝ) - 2| ≤ 1 ∧ |(3 : ℝ) - 4| ≤ 1 := by
  norm_num

#print axioms scaled_positive_interval
#print axioms affine_noise_column
#print axioms signed_midpoint_errors
#print axioms common_release_budget_lower
#print axioms fixed_critical_gap
#print axioms fixed_report_exclusion_is_not_global

end VariableNoiseMidpoint
