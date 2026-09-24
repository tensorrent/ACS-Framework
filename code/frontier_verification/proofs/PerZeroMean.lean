import PerZeroSums

open Real Filter Topology
open scoped BigOperators

namespace PerZeroMean

noncomputable def indicator (gamma T eps L : ℝ) : ℝ :=
  if min gamma (T - gamma) ≤ L * eps then 1 else 0

theorem indicator_nonneg (gamma T eps L : ℝ) : 0 ≤ indicator gamma T eps L := by
  unfold indicator
  split_ifs <;> norm_num

theorem deficit_lt_two_pi (gamma T eps : ℝ) (hg : 0 < gamma)
    (ht : gamma < T) (he : 0 < eps) : PerZeroError.deficit gamma T eps < 2 * π := by
  have h1 := arctan_pos.mpr (div_pos (sub_pos.mpr ht) he)
  have h2 := arctan_pos.mpr (div_pos hg he)
  unfold PerZeroError.deficit PerZero.contribution
  linarith

/-- A point inside the resolution layer gives a definite deficit; outside it,
    reciprocal-distance control gives the upper bound 4/L. -/
theorem point_bounds (gamma T eps L : ℝ) (hg : 0 < gamma)
    (ht : gamma < T) (he : 0 < eps) (hL : 0 < L) :
    2 * arctan (1 / L) * indicator gamma T eps L ≤ PerZeroError.deficit gamma T eps ∧
    PerZeroError.deficit gamma T eps ≤ 2 * π * indicator gamma T eps L + 4 / L := by
  have hd := PerZeroError.deficit_identity gamma T eps hg ht he
  have hpos := PerZeroError.deficit_positive gamma T eps hg ht he
  have h1 := arctan_nonneg.mpr (div_pos he hg).le
  have h2 := arctan_nonneg.mpr (div_pos he (sub_pos.mpr ht)).le
  by_cases hnear : min gamma (T - gamma) ≤ L * eps
  · simp only [indicator, if_pos hnear, mul_one]
    constructor
    · rcases min_le_iff.mp hnear with h | h
      · have hr : 1 / L ≤ eps / gamma := (div_le_div_iff₀ hL hg).2 (by nlinarith)
        have ha := arctan_strictMono.monotone hr
        linarith
      · have hr : 1 / L ≤ eps / (T - gamma) :=
          (div_le_div_iff₀ hL (sub_pos.mpr ht)).2 (by nlinarith)
        have ha := arctan_strictMono.monotone hr
        linarith
    · have h := deficit_lt_two_pi gamma T eps hg ht he
      have hdiv : 0 < (4 : ℝ) / L := div_pos (by norm_num) hL
      linarith
  · simp only [indicator, if_neg hnear, mul_zero, zero_add]
    constructor
    · exact hpos.le
    · have hfar := lt_min_iff.mp (lt_of_not_ge hnear)
      have hr1 : eps / gamma ≤ 1 / L :=
        (div_le_div_iff₀ hg hL).2 (by nlinarith [hfar.1])
      have hr2 : eps / (T - gamma) ≤ 1 / L :=
        (div_le_div_iff₀ (sub_pos.mpr ht) hL).2 (by nlinarith [hfar.2])
      have hbound := (PerZeroError.deficit_bounds gamma T eps hg ht he).2
      have heq : (4 : ℝ) / L = 4 * (1 / L) := by ring
      rw [heq]
      linarith

noncomputable def fraction {ι : Type*} (s : Finset ι) (gamma : ι → ℝ) (T eps L : ℝ) : ℝ :=
  (∑ k ∈ s, indicator (gamma k) T eps L) / s.card

noncomputable def mean {ι : Type*} (s : Finset ι) (gamma : ι → ℝ) (T eps : ℝ) : ℝ :=
  (∑ k ∈ s, PerZeroError.deficit (gamma k) T eps) / s.card

theorem fraction_nonneg {ι : Type*} (s : Finset ι) (gamma : ι → ℝ) (T eps L : ℝ) :
    0 ≤ fraction s gamma T eps L := by
  exact div_nonneg (Finset.sum_nonneg (fun k hk => indicator_nonneg (gamma k) T eps L)) (Nat.cast_nonneg _)

theorem mean_nonneg {ι : Type*} (s : Finset ι) (gamma : ι → ℝ) (T eps : ℝ)
    (hg : ∀ k ∈ s, 0 < gamma k) (ht : ∀ k ∈ s, gamma k < T) (he : 0 < eps) :
    0 ≤ mean s gamma T eps := by
  exact div_nonneg (Finset.sum_nonneg (fun k hk => (PerZeroError.deficit_positive (gamma k) T eps (hg k hk) (ht k hk) he).le)) (Nat.cast_nonneg _)

theorem mean_bounds {ι : Type*} (s : Finset ι) (hs : s.Nonempty)
    (gamma : ι → ℝ) (T eps L : ℝ) (hg : ∀ k ∈ s, 0 < gamma k)
    (ht : ∀ k ∈ s, gamma k < T) (he : 0 < eps) (hL : 0 < L) :
    2 * arctan (1 / L) * fraction s gamma T eps L ≤ mean s gamma T eps ∧
    mean s gamma T eps ≤ 2 * π * fraction s gamma T eps L + 4 / L := by
  have hn : (0 : ℝ) < s.card := by exact_mod_cast hs.card_pos
  have hlow := Finset.sum_le_sum (fun k hk => (point_bounds (gamma k) T eps L (hg k hk) (ht k hk) he hL).1)
  have hupp := Finset.sum_le_sum (fun k hk => (point_bounds (gamma k) T eps L (hg k hk) (ht k hk) he hL).2)
  simp only [← Finset.mul_sum] at hlow
  simp only [Finset.sum_add_distrib, Finset.sum_const, nsmul_eq_mul, ← Finset.mul_sum] at hupp
  unfold mean fraction
  constructor
  · simpa only [mul_div_assoc] using div_le_div_of_nonneg_right hlow hn.le
  · calc
      _ ≤ (2 * π * (∑ k ∈ s, indicator (gamma k) T eps L) + s.card * (4 / L)) / s.card :=
        div_le_div_of_nonneg_right hupp hn.le
      _ = _ := by field_simp

/-- Vanishing mean deficit is exactly vanishing mass in every fixed resolution layer. -/
theorem mean_tendsto_iff {α ι : Type*} (l : Filter α)
    (s : α → Finset ι) (hs : ∀ j, (s j).Nonempty)
    (gamma : α → ι → ℝ) (T eps : α → ℝ)
    (hg : ∀ j k, k ∈ s j → 0 < gamma j k)
    (ht : ∀ j k, k ∈ s j → gamma j k < T j) (he : ∀ j, 0 < eps j) :
    Tendsto (fun j => mean (s j) (gamma j) (T j) (eps j)) l (𝓝 0) ↔
      ∀ L : ℝ, 0 < L → Tendsto (fun j => fraction (s j) (gamma j) (T j) (eps j) L) l (𝓝 0) := by
  constructor
  · intro h L hL
    have hc : 0 < 2 * arctan (1 / L) :=
      mul_pos (by norm_num) (arctan_pos.mpr (div_pos (by norm_num) hL))
    apply squeeze_zero (fun j => fraction_nonneg (s j) (gamma j) (T j) (eps j) L)
      (fun j => (le_div_iff₀ hc).2 ?_)
      (by simpa using h.div_const (2 * arctan (1 / L)))
    simpa only [mul_comm] using (mean_bounds (s _) (hs _) (gamma _) (T _) (eps _) L (hg _) (ht _) (he _) hL).1
  · intro h
    apply tendsto_order.mpr
    constructor
    · intro a ha
      exact Eventually.of_forall fun j => lt_of_lt_of_le ha (mean_nonneg (s j) (gamma j) (T j) (eps j) (hg j) (ht j) (he j))
    · intro b hb
      let L : ℝ := 8 / b
      have hL : 0 < L := div_pos (by norm_num) hb
      have hlimit : Tendsto (fun j => 2 * π * fraction (s j) (gamma j) (T j) (eps j) L) l (𝓝 0) := by
        simpa using (h L hL).const_mul (2 * π)
      have htail : 4 / L = b / 2 := by dsimp [L]; field_simp; ring
      filter_upwards [hlimit.eventually (eventually_lt_nhds (by linarith : (0 : ℝ) < b / 2))] with j hj
      have hu := (mean_bounds (s j) (hs j) (gamma j) (T j) (eps j) L (hg j) (ht j) (he j) hL).2
      rw [htail] at hu
      linarith

theorem fraction_eq_count {ι : Type*} (s : Finset ι) (gamma : ι → ℝ) (T eps L : ℝ) :
    fraction s gamma T eps L =
      ((s.filter (fun k => min (gamma k) (T - gamma k) ≤ L * eps)).card : ℝ) / s.card := by
  classical
  simp [fraction, indicator, Finset.sum_boole]

theorem point_bounds_sharp (gamma T eps L : ℝ) (hg : 0 < gamma)
    (ht : gamma < T) (he : 0 < eps) (hL : 0 < L) :
    2 * arctan (1 / L) * indicator gamma T eps L ≤ PerZeroError.deficit gamma T eps ∧
    PerZeroError.deficit gamma T eps ≤ 2 * π * indicator gamma T eps L + 4 * arctan (1 / L) := by
  constructor
  · exact (point_bounds gamma T eps L hg ht he hL).1
  · by_cases hnear : min gamma (T - gamma) ≤ L * eps
    · simp only [indicator, if_pos hnear, mul_one]
      have hd := deficit_lt_two_pi gamma T eps hg ht he
      have ha := arctan_pos.mpr (div_pos (by norm_num : (0 : ℝ) < 1) hL)
      linarith
    · simp only [indicator, if_neg hnear, mul_zero, zero_add]
      have hfar := lt_min_iff.mp (lt_of_not_ge hnear)
      have hr1 : eps / gamma ≤ 1 / L := (div_le_div_iff₀ hg hL).2 (by nlinarith [hfar.1])
      have hr2 : eps / (T - gamma) ≤ 1 / L :=
        (div_le_div_iff₀ (sub_pos.mpr ht) hL).2 (by nlinarith [hfar.2])
      have h1 := arctan_strictMono.monotone hr1
      have h2 := arctan_strictMono.monotone hr2
      rw [PerZeroError.deficit_identity gamma T eps hg ht he]
      linarith

theorem mean_bounds_sharp {ι : Type*} (s : Finset ι) (hs : s.Nonempty)
    (gamma : ι → ℝ) (T eps L : ℝ) (hg : ∀ k ∈ s, 0 < gamma k)
    (ht : ∀ k ∈ s, gamma k < T) (he : 0 < eps) (hL : 0 < L) :
    2 * arctan (1 / L) * fraction s gamma T eps L ≤ mean s gamma T eps ∧
    mean s gamma T eps ≤ 2 * π * fraction s gamma T eps L + 4 * arctan (1 / L) := by
  constructor
  · exact (mean_bounds s hs gamma T eps L hg ht he hL).1
  · have hn : (0 : ℝ) < s.card := by exact_mod_cast hs.card_pos
    have hupp := Finset.sum_le_sum (fun k hk => (point_bounds_sharp (gamma k) T eps L (hg k hk) (ht k hk) he hL).2)
    simp only [Finset.sum_add_distrib, Finset.sum_const, nsmul_eq_mul, ← Finset.mul_sum] at hupp
    unfold mean fraction
    calc
      _ ≤ (2 * π * (∑ k ∈ s, indicator (gamma k) T eps L) + s.card * (4 * arctan (1 / L))) / s.card :=
        div_le_div_of_nonneg_right hupp hn.le
      _ = _ := by field_simp

end PerZeroMean
