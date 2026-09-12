import PerZeroIntegral

open Real intervalIntegral MeasureTheory

namespace PerZeroError

theorem kernel_continuous : Continuous (fun t : ℝ => 1 / (1 + t ^ 2)) :=
  continuous_const.div (by fun_prop) (fun t => by positivity)

theorem arctan_upper (x : ℝ) (hx : 0 ≤ x) : arctan x ≤ x := by
  have h := integral_mono_on (μ := volume) hx ((kernel_continuous.intervalIntegrable 0 x))
    (continuous_const.intervalIntegrable (a := 0) (b := x))
    (fun t (_ : t ∈ Set.Icc 0 x) => show 1 / (1 + t ^ 2) ≤ (1 : ℝ) by
      apply (div_le_iff₀ (by positivity)).2
      nlinarith [sq_nonneg t])
  simpa using h

theorem arctan_lower (x : ℝ) (hx : 0 ≤ x) : x / (1 + x ^ 2) ≤ arctan x := by
  have h := integral_mono_on (μ := volume) hx
    (continuous_const.intervalIntegrable (a := 0) (b := x)) (kernel_continuous.intervalIntegrable 0 x)
    (fun t (ht : t ∈ Set.Icc 0 x) => show 1 / (1 + x ^ 2) ≤ 1 / (1 + t ^ 2) by
      apply (div_le_div_iff₀ (by positivity) (by positivity)).2
      nlinarith [mul_nonneg (sub_nonneg.mpr ht.2) (add_nonneg hx ht.1)])
  simpa [div_eq_mul_inv, mul_comm] using h

theorem arctan_cubic (x : ℝ) (hx : 0 ≤ x) :
    0 ≤ x - arctan x ∧ x - arctan x ≤ x ^ 3 / 3 := by
  constructor
  · exact sub_nonneg.mpr (arctan_upper x hx)
  have h := integral_mono_on (μ := volume) hx
    ((continuous_const.sub (continuous_id.pow 2)).intervalIntegrable 0 x)
    (kernel_continuous.intervalIntegrable 0 x)
    (fun t (_ : t ∈ Set.Icc 0 x) => show 1 - t ^ 2 ≤ 1 / (1 + t ^ 2) by
      apply (le_div_iff₀ (by positivity)).2
      nlinarith [sq_nonneg (t ^ 2)])
  change (∫ t : ℝ in 0..x, 1 - t ^ 2) ≤ (∫ t : ℝ in 0..x, 1 / (1 + t ^ 2)) at h
  have hconst : IntervalIntegrable (fun _ : ℝ => (1 : ℝ)) volume 0 x := continuous_const.intervalIntegrable 0 x
  have hpow : IntervalIntegrable (fun t : ℝ => t ^ 2) volume 0 x := (by fun_prop : Continuous (fun t : ℝ => t ^ 2)).intervalIntegrable 0 x
  rw [integral_sub hconst hpow] at h
  simp only [intervalIntegral.integral_const, sub_zero, smul_eq_mul, mul_one, integral_pow,
    Nat.reduceAdd, zero_pow (by decide : 3 ≠ 0), zero_sub,
    integral_one_div_one_add_sq, arctan_zero] at h
  norm_num at h
  linarith

noncomputable def deficit (gamma T eps : ℝ) : ℝ :=
  2 * π - PerZero.contribution gamma T eps

theorem deficit_identity (gamma T eps : ℝ) (hg : 0 < gamma)
    (ht : gamma < T) (he : 0 < eps) :
    deficit gamma T eps =
      2 * (arctan (eps / gamma) + arctan (eps / (T - gamma))) := by
  have h1 := arctan_inv_of_pos (div_pos hg he)
  have h2 := arctan_inv_of_pos (div_pos (sub_pos.mpr ht) he)
  simp only [inv_div] at h1 h2
  unfold deficit PerZero.contribution
  linarith

theorem deficit_positive (gamma T eps : ℝ) (hg : 0 < gamma)
    (ht : gamma < T) (he : 0 < eps) : 0 < deficit gamma T eps := by
  rw [deficit_identity gamma T eps hg ht he]
  have h1 := arctan_pos.mpr (div_pos he hg)
  have h2 := arctan_pos.mpr (div_pos he (sub_pos.mpr ht))
  linarith

theorem deficit_bounds (gamma T eps : ℝ) (hg : 0 < gamma)
    (ht : gamma < T) (he : 0 < eps) :
    2 * ((eps / gamma) / (1 + (eps / gamma) ^ 2) +
      (eps / (T - gamma)) / (1 + (eps / (T - gamma)) ^ 2)) ≤ deficit gamma T eps ∧
    deficit gamma T eps ≤ 2 * (eps / gamma + eps / (T - gamma)) := by
  rw [deficit_identity gamma T eps hg ht he]
  have h1 := arctan_lower (eps / gamma) (le_of_lt (div_pos he hg))
  have h2 := arctan_lower (eps / (T - gamma)) (le_of_lt (div_pos he (sub_pos.mpr ht)))
  have h3 := arctan_upper (eps / gamma) (le_of_lt (div_pos he hg))
  have h4 := arctan_upper (eps / (T - gamma)) (le_of_lt (div_pos he (sub_pos.mpr ht)))
  constructor <;> linarith

theorem deficit_cubic (gamma T eps : ℝ) (hg : 0 < gamma)
    (ht : gamma < T) (he : 0 < eps) :
    0 ≤ 2 * (eps / gamma + eps / (T - gamma)) - deficit gamma T eps ∧
    2 * (eps / gamma + eps / (T - gamma)) - deficit gamma T eps ≤
      2 / 3 * ((eps / gamma) ^ 3 + (eps / (T - gamma)) ^ 3) := by
  rw [deficit_identity gamma T eps hg ht he]
  have h1 := arctan_cubic (eps / gamma) (le_of_lt (div_pos he hg))
  have h2 := arctan_cubic (eps / (T - gamma)) (le_of_lt (div_pos he (sub_pos.mpr ht)))
  constructor <;> linarith

end PerZeroError
