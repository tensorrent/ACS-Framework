import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

namespace QuadraticSupport

noncomputable def support (D E : ℝ) : ℝ :=
  if 0 < E ∧ D < 2 * E then D ^ 2 / (4 * E) else D - E

theorem vertex_bound (D E x : ℝ) (hE : 0 < E) :
    D * x - E * x ^ 2 ≤ D ^ 2 / (4 * E) := by
  apply (le_div_iff₀ (by positivity : 0 < 4 * E)).2
  nlinarith [sq_nonneg (2 * E * x - D)]

theorem endpoint_nonpos (D E x : ℝ) (hD : 0 ≤ D) (hE : E ≤ 0)
    (hx0 : 0 ≤ x) (hx1 : x ≤ 1) : D * x - E * x ^ 2 ≤ D - E := by
  have hm : E * (1 + x) ≤ 0 := mul_nonpos_of_nonpos_of_nonneg hE (by linarith)
  have hp := mul_nonneg (sub_nonneg.mpr hx1) (show 0 ≤ D - E * (1 + x) by linarith)
  nlinarith

theorem endpoint_large (D E x : ℝ) (hD : 2 * E ≤ D) (hE : 0 ≤ E)
    (hx0 : 0 ≤ x) (hx1 : x ≤ 1) : D * x - E * x ^ 2 ≤ D - E := by
  have hm := mul_nonneg hE (sub_nonneg.mpr hx1)
  have hp := mul_nonneg (sub_nonneg.mpr hx1) (show 0 ≤ D - E * (1 + x) by nlinarith)
  nlinarith

theorem upper_on_unit_interval (D E x : ℝ) (hD : 0 ≤ D)
    (hx0 : 0 ≤ x) (hx1 : x ≤ 1) : D * x - E * x ^ 2 ≤ support D E := by
  by_cases h : 0 < E ∧ D < 2 * E
  · simpa [support, h] using vertex_bound D E x h.1
  · simp only [support, if_neg h]
    by_cases he : E ≤ 0
    · exact endpoint_nonpos D E x hD he hx0 hx1
    · have hep : 0 < E := lt_of_not_ge he
      have hd : 2 * E ≤ D := le_of_not_gt (fun hd => h ⟨hep, hd⟩)
      exact endpoint_large D E x hd hep.le hx0 hx1

theorem support_nonnegative (D E : ℝ) (hD : 0 ≤ D) : 0 ≤ support D E := by
  simpa using upper_on_unit_interval D E 0 hD (by norm_num) (by norm_num)

theorem signed_reduction (d e D E y : ℝ) (hd : |d| ≤ D) (he : E ≤ e) :
    -d * y - e * y ^ 2 ≤ D * |y| - E * |y| ^ 2 := by
  have hl : -d * y ≤ D * |y| := calc
    -d * y ≤ |-d * y| := le_abs_self _
    _ = |d| * |y| := by rw [abs_mul, abs_neg]
    _ ≤ D * |y| := mul_le_mul_of_nonneg_right hd (abs_nonneg y)
  have hc := mul_le_mul_of_nonneg_right he (sq_nonneg y)
  rw [sq_abs]
  nlinarith

theorem signed_quadratic_bound (d e D E y : ℝ) (hd : |d| ≤ D)
    (he : E ≤ e) (hy : |y| ≤ 1) : -d * y - e * y ^ 2 ≤ support D E := by
  exact (signed_reduction d e D E y hd he).trans
    (upper_on_unit_interval D E |y| ((abs_nonneg d).trans hd) (abs_nonneg y) hy)

theorem support_attained (D E : ℝ) (hD : 0 ≤ D) :
    ∃ x : ℝ, 0 ≤ x ∧ x ≤ 1 ∧ D * x - E * x ^ 2 = support D E := by
  by_cases h : 0 < E ∧ D < 2 * E
  · have hE : 0 < E := h.1
    have h2E : 0 < 2 * E := mul_pos (by norm_num) hE
    refine ⟨D / (2 * E), div_nonneg hD h2E.le, ?_, ?_⟩
    · exact (div_le_one h2E).2 h.2.le
    · simp only [support, if_pos h]
      field_simp [ne_of_gt h.1]
      <;> ring
  · refine ⟨1, by norm_num, by norm_num, ?_⟩
    simp [support, h]

theorem cone_identity (y z : ℝ) :
    (z + 1) ^ 2 - ((2 * y) ^ 2 + (z - 1) ^ 2) = 4 * (z - y ^ 2) := by ring

theorem cone_equivalence (y z : ℝ) :
    (0 ≤ z + 1 ∧ (2 * y) ^ 2 + (z - 1) ^ 2 ≤ (z + 1) ^ 2) ↔ y ^ 2 ≤ z := by
  constructor
  · intro h
    nlinarith [h.2]
  · intro h
    have hz : 0 ≤ z := (sq_nonneg y).trans h
    constructor <;> nlinarith

#print axioms vertex_bound
#print axioms endpoint_nonpos
#print axioms endpoint_large
#print axioms upper_on_unit_interval
#print axioms support_nonnegative
#print axioms signed_reduction
#print axioms signed_quadratic_bound
#print axioms support_attained
#print axioms cone_identity
#print axioms cone_equivalence

end QuadraticSupport
