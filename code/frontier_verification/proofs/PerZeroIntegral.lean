import PerZero
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

open Real intervalIntegral

namespace PerZeroIntegral

/-- The real paired kernel has the archived closed form as its integral. -/
theorem real_integral (gamma T eps : ℝ) (he : eps ≠ 0) :
    (∫ u : ℝ in -gamma..T - gamma, 2 * eps / (eps ^ 2 + u ^ 2)) =
      PerZero.contribution gamma T eps := by
  simp_rw [div_eq_mul_inv]
  rw [integral_const_mul, integral_inv_sq_add_sq he]
  simp only [neg_mul, arctan_neg, sub_neg_eq_add, PerZero.contribution, div_eq_mul_inv]
  field_simp

/-- Translation returns the actual 0-to-T parameter interval. -/
theorem translated_integral (gamma T eps : ℝ) (he : eps ≠ 0) :
    (∫ t : ℝ in 0..T, 2 * eps / (eps ^ 2 + (t - gamma) ^ 2)) =
      PerZero.contribution gamma T eps := by
  rw [integral_comp_sub_right (fun u : ℝ => 2 * eps / (eps ^ 2 + u ^ 2)) gamma]
  simpa using real_integral gamma T eps he

/-- The complex paired resolvents cancel pointwise to a real Lorentzian. -/
theorem paired_identity (eps u : ℝ) (he : eps ≠ 0) :
    1 / ((eps : ℂ) + Complex.I * u) - 1 / ((-eps : ℂ) + Complex.I * u) =
      ((2 * eps / (eps ^ 2 + u ^ 2) : ℝ) : ℂ) := by
  have hp : 0 < eps ^ 2 + u ^ 2 := by positivity
  have hpos : (eps : ℂ) + Complex.I * u ≠ 0 := by
    intro h
    have := congrArg Complex.re h
    exact he (by simpa using this)
  have hneg : (-eps : ℂ) + Complex.I * u ≠ 0 := by
    intro h
    have := congrArg Complex.re h
    simp only [Complex.add_re, Complex.neg_re, Complex.ofReal_re, Complex.mul_re,
      Complex.I_re, Complex.ofReal_im, Complex.I_im, zero_mul, mul_zero, sub_self,
      add_zero, Complex.zero_re, neg_eq_zero] at this
    exact he this
  have hc : (eps : ℂ) ^ 2 + (u : ℂ) ^ 2 ≠ 0 := by
    exact_mod_cast (ne_of_gt hp)
  push_cast
  field_simp [hpos, hneg, hc]
  ring_nf
  simp [Complex.I_sq]

/-- Integral of the actual complex paired kernel equals the real contribution. -/
theorem complex_integral (gamma T eps : ℝ) (he : eps ≠ 0) :
    (∫ t : ℝ in 0..T,
      (1 / ((eps : ℂ) + Complex.I * (t - gamma)) -
       1 / ((-eps : ℂ) + Complex.I * (t - gamma)))) =
      (PerZero.contribution gamma T eps : ℂ) := by
  calc
    _ = ∫ t : ℝ in 0..T, ((2 * eps / (eps ^ 2 + (t - gamma) ^ 2) : ℝ) : ℂ) := by
      apply integral_congr
      intro t ht
      simpa only [Complex.ofReal_sub] using paired_identity eps (t - gamma) he
    _ = _ := by rw [integral_ofReal, translated_integral gamma T eps he]

end PerZeroIntegral
