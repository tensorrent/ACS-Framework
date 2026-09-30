import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Data.Finset.Max
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

open scoped BigOperators

namespace WeightedFeatureStability

theorem weighted_maximum_principle {I : Type*} [Fintype I] [Nonempty I]
    (B : I → I → ℝ) (w z : I → ℝ) {q : ℝ}
    (hB : ∀ i j, 0 ≤ B i j) (hw : ∀ i, 0 < w i) (hq : q < 1)
    (hrow : ∀ i, ∑ j, B i j * w j ≤ q * w i)
    (hz : ∀ i, z i ≤ ∑ j, B i j * z j) : ∀ i, z i ≤ 0 := by
  classical
  obtain ⟨k, _, hmax⟩ := Finset.exists_max_image (Finset.univ : Finset I)
    (fun i => z i / w i) Finset.univ_nonempty
  intro i
  by_contra hi
  have hip : 0 < z i := lt_of_not_ge hi
  let a := z k / w k
  have hap : 0 < a := lt_of_lt_of_le (div_pos hip (hw i)) (hmax i (Finset.mem_univ i))
  have hzw : ∀ j, z j ≤ a * w j := by
    intro j
    exact (div_le_iff₀ (hw j)).mp (hmax j (Finset.mem_univ j))
  have heq : a * w k = z k := div_mul_cancel₀ _ (ne_of_gt (hw k))
  have hs : (∑ j, B k j * z j) ≤ a * (∑ j, B k j * w j) := by
    calc
      (∑ j, B k j * z j) ≤ ∑ j, B k j * (a * w j) := by
        apply Finset.sum_le_sum
        intro j _
        exact mul_le_mul_of_nonneg_left (hzw j) (hB k j)
      _ = a * (∑ j, B k j * w j) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro j _
        ring
  have hcycle : z k ≤ q * z k := by
    calc
      z k ≤ ∑ j, B k j * z j := hz k
      _ ≤ a * (∑ j, B k j * w j) := hs
      _ ≤ a * (q * w k) := mul_le_mul_of_nonneg_left (hrow k) (le_of_lt hap)
      _ = q * (a * w k) := by ring
      _ = q * z k := by rw [heq]
  have hkp : 0 < z k := by
    have h := mul_pos hap (hw k)
    rwa [heq] at h
  nlinarith

theorem componentwise_supersolution_bound {I : Type*} [Fintype I] [Nonempty I]
    (B : I → I → ℝ) (w d r h : I → ℝ) {q error : ℝ}
    (hB : ∀ i j, 0 ≤ B i j) (hw : ∀ i, 0 < w i) (hq : q < 1)
    (hrow : ∀ i, ∑ j, B i j * w j ≤ q * w i) (he : 0 ≤ error)
    (hd : ∀ i, d i ≤ r i * error + ∑ j, B i j * d j)
    (hh : ∀ i, r i + ∑ j, B i j * h j ≤ h i) :
    ∀ i, d i ≤ h i * error := by
  have hz : ∀ i, d i - h i * error ≤ ∑ j, B i j * (d j - h j * error) := by
    intro i
    have hs : (∑ j, B i j * (d j - h j * error)) =
        (∑ j, B i j * d j) - (∑ j, B i j * h j) * error := by
      simp only [mul_sub, Finset.sum_sub_distrib, Finset.sum_mul, mul_assoc]
    have hm := mul_le_mul_of_nonneg_right (hh i) he
    have hb := hd i
    rw [hs]
    nlinarith
  have result := weighted_maximum_principle B w (fun i => d i - h i * error) hB hw hq hrow hz
  intro i
  have h := result i
  linarith

theorem critical_source_gap {a b yA yB L radius : ℝ}
    (hL : 2 * L = a - b) (hA : a - radius ≤ yA) (hB : yB ≤ b + radius) :
    2 * (L - radius) ≤ yA - yB := by
  linarith

theorem strict_noise_identification {gap distance featureGap K tau : ℝ}
    (hK : 0 < K) (hroot : 2 * gap ≤ distance)
    (hstable : distance ≤ K * featureGap) (hcommon : featureGap ≤ 2 * tau)
    (hsmall : tau < gap / K) : False := by
  have hs := (lt_div_iff₀ hK).mp hsmall
  have hm := mul_le_mul_of_nonneg_left hcommon (le_of_lt hK)
  nlinarith

theorem signed_common_release_error {z tau v : ℝ}
    (htau : 0 ≤ tau) (hv : |v| = 1) : |z - (z + tau * v)| = tau := by
  have h : z - (z + tau * v) = -(tau * v) := by ring
  rw [h, abs_neg, abs_mul, abs_of_nonneg htau, hv, mul_one]

theorem exact_midpoint_radius_upper {x midpoint radius bound : ℝ}
    (hx : |x - midpoint| ≤ radius) (hb : midpoint + radius ≤ bound) : x ≤ bound := by
  have h := (abs_le.mp hx).2
  linarith

#print axioms weighted_maximum_principle
#print axioms componentwise_supersolution_bound
#print axioms critical_source_gap
#print axioms strict_noise_identification
#print axioms signed_common_release_error
#print axioms exact_midpoint_radius_upper

end WeightedFeatureStability
