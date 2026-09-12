import PerZero

open Real Filter Topology

namespace PerZeroBoundary

noncomputable def scaled (c eps : ℝ) : ℝ :=
  2 * (arctan (eps⁻¹ - c) + arctan c)

theorem scaled_identity (c eps : ℝ) (he : eps ≠ 0) :
    PerZero.contribution (c * eps) 1 eps = scaled c eps := by
  simp [PerZero.contribution, scaled, sub_div, he, one_div]

theorem scaled_tendsto (c : ℝ) :
    Tendsto (scaled c) (𝓝[>] 0) (𝓝 (2 * (π / 2 + arctan c))) := by
  change Tendsto (fun eps : ℝ => 2 * (arctan (eps⁻¹ - c) + arctan c))
    (𝓝[>] 0) (𝓝 (2 * (π / 2 + arctan c)))
  have hinv : Tendsto (fun eps : ℝ => eps⁻¹) (𝓝[>] (0 : ℝ)) atTop :=
    tendsto_inv_nhdsGT_zero
  have hi : Tendsto (fun eps : ℝ => eps⁻¹ + -c) (𝓝[>] (0 : ℝ)) atTop :=
    tendsto_atTop_add_const_right _ (-c) hinv
  have ha : Tendsto arctan atTop (𝓝 (π / 2)) :=
    tendsto_arctan_atTop.mono_right nhdsWithin_le_nhds
  simpa [scaled, Function.comp, sub_eq_add_neg] using
    (((ha.comp hi).add_const (arctan c)).const_mul 2)

theorem moving_boundary_tendsto (c : ℝ) :
    Tendsto (fun eps : ℝ => PerZero.contribution (c * eps) 1 eps)
      (𝓝[>] 0) (𝓝 (2 * (π / 2 + arctan c))) := by
  apply (scaled_tendsto c).congr'
  filter_upwards [self_mem_nhdsWithin] with eps heps
  exact (scaled_identity c eps (ne_of_gt heps)).symm

theorem boundary_at_one :
    Tendsto (fun eps : ℝ => PerZero.contribution eps 1 eps)
      (𝓝[>] 0) (𝓝 (3 * π / 2)) := by
  have h := moving_boundary_tendsto 1
  have heq : 2 * (π / 2 + π / 4) = 3 * π / 2 := by ring
  simpa [arctan_one, heq] using h

theorem boundary_not_two_pi :
    ¬ Tendsto (fun eps : ℝ => PerZero.contribution eps 1 eps)
      (𝓝[>] 0) (𝓝 (2 * π)) := by
  intro h
  have heq := tendsto_nhds_unique boundary_at_one h
  have hp := pi_pos
  linarith

end PerZeroBoundary
