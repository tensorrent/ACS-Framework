import PerZeroError

open Real Filter Topology
open scoped BigOperators

namespace PerZeroSums

theorem half_le_arctan (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1) : x / 2 ≤ arctan x := by
  have hsq : x ^ 2 ≤ 1 := by
    nlinarith [mul_nonneg hx (sub_nonneg.mpr hx1)]
  have h : x / 2 ≤ x / (1 + x ^ 2) := by
    apply (div_le_div_iff₀ (by norm_num) (by positivity)).2
    exact mul_le_mul_of_nonneg_left (by linarith : 1 + x ^ 2 ≤ 2) hx
  exact h.trans (PerZeroError.arctan_lower x hx)

theorem sum_upper {ι : Type*} (s : Finset ι) (x : ι → ℝ)
    (hx : ∀ k ∈ s, 0 ≤ x k) :
    2 * ∑ k ∈ s, arctan (x k) ≤ 2 * ∑ k ∈ s, x k := by
  exact mul_le_mul_of_nonneg_left
    (Finset.sum_le_sum fun k hk => PerZeroError.arctan_upper (x k) (hx k hk)) (by norm_num)

/-- Small total error forces every ratio into the same bounded interval. -/
theorem sum_lower_when_small {ι : Type*} (s : Finset ι) (x : ι → ℝ)
    (hx : ∀ k ∈ s, 0 ≤ x k) (hs : 2 * ∑ k ∈ s, arctan (x k) < π / 2) :
    (∑ k ∈ s, x k) ≤ 2 * ∑ k ∈ s, arctan (x k) := by
  calc
    _ ≤ ∑ k ∈ s, 2 * arctan (x k) := by
      apply Finset.sum_le_sum
      intro k hk
      have hsingle : arctan (x k) ≤ ∑ j ∈ s, arctan (x j) :=
        Finset.single_le_sum (fun j hj => arctan_nonneg.mpr (hx j hj)) hk
      have ha : arctan (x k) < arctan 1 := by rw [arctan_one]; linarith
      have hone : x k ≤ 1 := (arctan_strictMono.lt_iff_lt.mp ha).le
      linarith [half_le_arctan (x k) (hx k hk) hone]
    _ = _ := by rw [Finset.mul_sum]

/-- Cardinality may change arbitrarily. No sum/limit interchange is assumed. -/
theorem total_tendsto_iff {α ι : Type*} (l : Filter α)
    (s : α → Finset ι) (x : α → ι → ℝ) (hx : ∀ j k, k ∈ s j → 0 ≤ x j k) :
    Tendsto (fun j => 2 * ∑ k ∈ s j, arctan (x j k)) l (𝓝 0) ↔
      Tendsto (fun j => ∑ k ∈ s j, x j k) l (𝓝 0) := by
  constructor
  · intro h
    apply squeeze_zero' (Eventually.of_forall (fun j => Finset.sum_nonneg (hx j))) ?_ h
    filter_upwards [h.eventually (eventually_lt_nhds (by positivity : (0 : ℝ) < π / 2))] with j hj
    exact sum_lower_when_small (s j) (x j) (hx j) hj
  · intro h
    apply squeeze_zero (fun j => mul_nonneg (by norm_num)
      (Finset.sum_nonneg fun k hk => arctan_nonneg.mpr (hx j k hk)))
      (fun j => sum_upper (s j) (x j) (hx j))
    simpa using h.const_mul 2

noncomputable def endpointRatio {ι : Type*} (gamma : ι → ℝ) (T eps : ℝ) (p : ι × Bool) : ℝ :=
  if p.2 then eps / gamma p.1 else eps / (T - gamma p.1)

theorem endpoint_sum_identity {ι : Type*} (s : Finset ι) (gamma : ι → ℝ) (T eps : ℝ)
    (hg : ∀ k ∈ s, 0 < gamma k) (ht : ∀ k ∈ s, gamma k < T) (he : 0 < eps) :
    (∑ k ∈ s, PerZeroError.deficit (gamma k) T eps) =
      2 * ∑ p ∈ s.product Finset.univ, arctan (endpointRatio gamma T eps p) := by
  classical
  calc
    _ = ∑ k ∈ s, 2 * (arctan (eps / gamma k) + arctan (eps / (T - gamma k))) := by
      apply Finset.sum_congr rfl
      intro k hk
      exact PerZeroError.deficit_identity (gamma k) T eps (hg k hk) (ht k hk) he
    _ = _ := by simp [endpointRatio, Finset.sum_product, Finset.mul_sum]

theorem endpoint_ratio_sum {ι : Type*} (s : Finset ι) (gamma : ι → ℝ) (T eps : ℝ) :
    (∑ p ∈ s.product Finset.univ, endpointRatio gamma T eps p) =
      eps * ∑ k ∈ s, (1 / gamma k + 1 / (T - gamma k)) := by
  classical
  simp [endpointRatio, Finset.sum_product, Finset.mul_sum, mul_add, div_eq_mul_inv]

/-- The exact absolute-error criterion for arbitrary moving finite configurations. -/
theorem deficit_sum_tendsto_iff {α ι : Type*} (l : Filter α)
    (s : α → Finset ι) (gamma : α → ι → ℝ) (T eps : α → ℝ)
    (hg : ∀ j k, k ∈ s j → 0 < gamma j k)
    (ht : ∀ j k, k ∈ s j → gamma j k < T j) (he : ∀ j, 0 < eps j) :
    Tendsto (fun j => ∑ k ∈ s j, PerZeroError.deficit (gamma j k) (T j) (eps j)) l (𝓝 0) ↔
      Tendsto (fun j => eps j * ∑ k ∈ s j, (1 / gamma j k + 1 / (T j - gamma j k))) l (𝓝 0) := by
  have hn : ∀ j p, p ∈ (s j).product (Finset.univ : Finset Bool) →
      0 ≤ endpointRatio (gamma j) (T j) (eps j) p := by
    intro j p hp
    have hk := (Finset.mem_product.mp hp).1
    unfold endpointRatio
    split
    · exact (div_pos (he j) (hg j p.1 hk)).le
    · exact (div_pos (he j) (sub_pos.mpr (ht j p.1 hk))).le
  have h := total_tendsto_iff l (fun j => (s j).product Finset.univ)
    (fun j => endpointRatio (gamma j) (T j) (eps j)) hn
  simp_rw [← endpoint_sum_identity (s _) (gamma _) (T _) (eps _) (hg _) (ht _) (he _),
    endpoint_ratio_sum] at h
  exact h

end PerZeroSums
