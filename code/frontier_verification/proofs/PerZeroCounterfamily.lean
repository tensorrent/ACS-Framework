import PerZeroMean

open Real Filter Topology
open scoped BigOperators

namespace PerZeroCounterfamily

noncomputable def value (r : ℝ) : ℝ :=
  π / 2 + 2 * arctan (1 / (r ^ 2 - 1)) + 4 * (r - 1) * arctan (2 / r ^ 2)

theorem remainder_bounds (r : ℝ) (hr : 2 ≤ r) :
    0 ≤ 4 * (r - 1) * arctan (2 / r ^ 2) ∧
    4 * (r - 1) * arctan (2 / r ^ 2) ≤ 8 / r := by
  have hp : 0 < r := by linarith
  have hq : 0 ≤ (2 : ℝ) / r ^ 2 := by positivity
  have ha := arctan_nonneg.mpr hq
  constructor
  · exact mul_nonneg (by linarith) ha
  · calc
      _ ≤ (4 * r) * (2 / r ^ 2) :=
        mul_le_mul (by linarith) (PerZeroError.arctan_upper _ hq) ha (by linarith)
      _ = _ := by field_simp; ring

theorem value_tendsto : Tendsto value atTop (𝓝 (π / 2)) := by
  have hi : Tendsto (fun r : ℝ => (r ^ 2 - 1)⁻¹) atTop (𝓝 0) :=
    tendsto_inv_atTop_zero.comp
      (by simpa [sub_eq_add_neg] using (tendsto_atTop_add_const_right atTop (-1 : ℝ)
        (tendsto_pow_atTop (by decide : 2 ≠ 0))))
  have ha : Tendsto (fun r : ℝ => arctan (1 / (r ^ 2 - 1))) atTop (𝓝 0) := by
    simpa [Function.comp_def, arctan_zero, one_div] using (continuous_arctan.tendsto 0).comp hi
  have htail : Tendsto (fun r : ℝ => 4 * (r - 1) * arctan (2 / r ^ 2)) atTop (𝓝 0) := by
    apply squeeze_zero' ?_ ?_
      (by simpa [div_eq_mul_inv] using (tendsto_inv_atTop_zero : Tendsto (fun r : ℝ => r⁻¹) atTop (𝓝 0)).const_mul 8)
    · filter_upwards [eventually_ge_atTop (2 : ℝ)] with r hr
      exact (remainder_bounds r hr).1
    · filter_upwards [eventually_ge_atTop (2 : ℝ)] with r hr
      exact (remainder_bounds r hr).2
  change Tendsto (fun r : ℝ => π / 2 + 2 * arctan (1 / (r ^ 2 - 1)) + 4 * (r - 1) * arctan (2 / r ^ 2)) atTop (𝓝 (π / 2))
  simpa only [one_div, mul_zero, add_zero] using (((tendsto_const_nhds : Tendsto (fun _ : ℝ => π / 2) atTop (𝓝 (π / 2))).add (ha.const_mul 2)).add htail)

theorem value_div_tendsto : Tendsto (fun r : ℝ => value r / r) atTop (𝓝 0) := by
  simpa [div_eq_mul_inv] using value_tendsto.mul
    (tendsto_inv_atTop_zero : Tendsto (fun r : ℝ => r⁻¹) atTop (𝓝 0))

noncomputable def resolution (N : ℕ) : ℝ := 1 / (N : ℝ) ^ 2
noncomputable def ordinate (N k : ℕ) : ℝ := if k = 0 then resolution N else 1 / 2
noncomputable def total (N : ℕ) : ℝ :=
  ∑ k ∈ Finset.range N, PerZeroError.deficit (ordinate N k) 1 (resolution N)

theorem resolution_bounds (N : ℕ) (hN : 2 ≤ N) : 0 < resolution N ∧ resolution N < 1 := by
  have hn : (2 : ℝ) ≤ N := by exact_mod_cast hN
  unfold resolution
  constructor
  · positivity
  · apply (div_lt_one (by positivity : (0 : ℝ) < (N : ℝ)^2)).2
    nlinarith

theorem ordinate_interior (N k : ℕ) (hN : 2 ≤ N) : 0 < ordinate N k ∧ ordinate N k < 1 := by
  unfold ordinate
  split_ifs
  · exact resolution_bounds N hN
  · norm_num

theorem boundary_deficit (eps : ℝ) (he : 0 < eps) (he1 : eps < 1) :
    PerZeroError.deficit eps 1 eps = π / 2 + 2 * arctan (eps / (1 - eps)) := by
  rw [PerZeroError.deficit_identity eps 1 eps he he1 he]
  simp only [div_self he.ne', arctan_one]
  ring

theorem midpoint_deficit (eps : ℝ) (he : 0 < eps) :
    PerZeroError.deficit (1 / 2) 1 eps = 4 * arctan (2 * eps) := by
  rw [PerZeroError.deficit_identity (1 / 2) 1 eps (by norm_num) (by norm_num) he]
  norm_num
  ring

theorem total_eq_value (N : ℕ) (hN : 2 ≤ N) : total N = value N := by
  have hn : (2 : ℝ) ≤ N := by exact_mod_cast hN
  have hn0 : (N : ℝ) ≠ 0 := by linarith
  have hn2 : (N : ℝ)^2 - 1 ≠ 0 := by nlinarith
  have he := resolution_bounds N hN
  have point (k : ℕ) : PerZeroError.deficit (ordinate N k) 1 (resolution N) =
      (if k = 0 then PerZeroError.deficit (resolution N) 1 (resolution N) -
        PerZeroError.deficit (1 / 2) 1 (resolution N) else 0) +
        PerZeroError.deficit (1 / 2) 1 (resolution N) := by
    by_cases hk : k = 0 <;> simp [ordinate, hk]
  unfold total
  simp_rw [point]
  simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_range, nsmul_eq_mul]
  rw [Finset.sum_ite_eq']
  simp only [Finset.mem_range, show 0 < N by omega, ite_true]
  rw [boundary_deficit _ he.1 he.2, midpoint_deficit _ he.1]
  have hr : resolution N / (1 - resolution N) = 1 / ((N : ℝ)^2 - 1) := by
    unfold resolution
    field_simp
  rw [hr]
  unfold value resolution
  simp only [mul_one_div]
  ring

theorem total_tendsto : Tendsto total atTop (𝓝 (π / 2)) := by
  have h : Tendsto (fun N : ℕ => value (N : ℝ)) atTop (𝓝 (π / 2)) :=
    value_tendsto.comp tendsto_natCast_atTop_atTop
  apply h.congr'
  filter_upwards [eventually_ge_atTop (2 : ℕ)] with N hN
  exact (total_eq_value N hN).symm

theorem mean_tendsto : Tendsto (fun N : ℕ => total N / N) atTop (𝓝 0) := by
  have h : Tendsto (fun N : ℕ => value (N : ℝ) / N) atTop (𝓝 0) :=
    value_div_tendsto.comp tendsto_natCast_atTop_atTop
  apply h.congr'
  filter_upwards [eventually_ge_atTop (2 : ℕ)] with N hN
  rw [total_eq_value N hN]

theorem total_not_tendsto_zero : ¬ Tendsto total atTop (𝓝 0) := by
  intro h
  have heq := tendsto_nhds_unique total_tendsto h
  have hp := pi_pos
  linarith

theorem configuration_mean_eq (N : ℕ) :
    PerZeroMean.mean (Finset.range N) (ordinate N) 1 (resolution N) = total N / N := by
  simp only [PerZeroMean.mean, total, Finset.card_range]

/-- Testing one layer misses points just beyond it, even as resolution shrinks. -/
theorem single_cutoff_failure (eps : ℝ) (he : 0 < eps) (he1 : eps < 1 / 3) :
    PerZeroMean.indicator (2 * eps) 1 eps 1 = 0 ∧
    0 < 2 * arctan (1 / 2) ∧
    2 * arctan (1 / 2) < PerZeroError.deficit (2 * eps) 1 eps := by
  have hg : 0 < 2 * eps := by positivity
  have ht : 2 * eps < 1 := by linarith
  have hfar : ¬ min (2 * eps) (1 - 2 * eps) ≤ 1 * eps := by
    apply not_le.mpr
    apply lt_min <;> linarith
  constructor
  · simp only [PerZeroMean.indicator, if_neg hfar]
  constructor
  · exact mul_pos (by norm_num) (arctan_pos.mpr (by norm_num))
  · rw [PerZeroError.deficit_identity (2 * eps) 1 eps hg ht he]
    have hr : eps / (2 * eps) = (1 : ℝ) / 2 := by field_simp
    rw [hr]
    have ha := arctan_pos.mpr (div_pos he (sub_pos.mpr ht))
    linarith

end PerZeroCounterfamily
