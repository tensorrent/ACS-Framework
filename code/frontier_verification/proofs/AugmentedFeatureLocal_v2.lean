import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Tactic.Linarith

namespace AugmentedFeatureLocal

theorem injective_on_of_preconditioned_defect {E F : Type*}
    [NormedAddCommGroup E] [AddGroup F]
    (Phi : E → F) (R : F →+ E) (s : Set E) {q : ℝ} (hq : q < 1)
    (hbound : ∀ x ∈ s, ∀ y ∈ s,
      ‖(x - y) - R (Phi x - Phi y)‖ ≤ q * ‖x - y‖) :
    Set.InjOn Phi s := by
  intro x hx y hy hxy
  have h := hbound x hx y hy
  rw [hxy, sub_self, map_zero, sub_zero] at h
  have hn := norm_nonneg (x - y)
  have hz : ‖x - y‖ = 0 := by nlinarith
  exact sub_eq_zero.mp (norm_eq_zero.mp hz)

theorem half_defect_inverse_bound {distance error C q : ℝ}
    (hd : 0 ≤ distance) (hq : q ≤ 1 / 2)
    (h : distance ≤ C * error + q * distance) :
    distance ≤ 2 * C * error := by
  nlinarith

theorem split_gap_for_one_remaining_feature {epsilon error C : ℝ}
    (hC : 0 < C) (h : 2 * epsilon ≤ C * error) :
    2 * epsilon / C ≤ error := by
  exact (div_le_iff₀ hC).mpr (by nlinarith)

theorem equal_prefixes_do_not_imply_equal_extension {I A B : Type*}
    (observed : A → I) (extra : A → B) {x y : A}
    (hprefix : observed x = observed y) (hextra : extra x ≠ extra y) :
    observed x = observed y ∧ (observed x, extra x) ≠ (observed y, extra y) := by
  refine ⟨hprefix, ?_⟩
  intro h
  exact hextra (congrArg Prod.snd h)

theorem local_square_derivative_defect {x : ℝ}
    (hlo : 3 / 4 ≤ x) (hhi : x ≤ 5 / 4) : |1 - x| ≤ 1 / 4 := by
  apply abs_le.mpr
  constructor <;> linarith

theorem local_does_not_imply_global_control :
    (1 : ℝ) ^ 2 = (-1 : ℝ) ^ 2 ∧ (1 : ℝ) ≠ -1 := by
  constructor <;> norm_num

#print axioms injective_on_of_preconditioned_defect
#print axioms half_defect_inverse_bound
#print axioms split_gap_for_one_remaining_feature
#print axioms equal_prefixes_do_not_imply_equal_extension
#print axioms local_square_derivative_defect
#print axioms local_does_not_imply_global_control

end AugmentedFeatureLocal
