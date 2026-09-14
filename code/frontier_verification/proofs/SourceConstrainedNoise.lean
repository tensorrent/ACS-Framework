import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

set_option autoImplicit false

namespace SourceConstrainedNoise

theorem source_radius_necessity {lo hi root observed radius : ℝ}
    (hl : lo ≤ root) (hh : root ≤ hi) (he : |observed - root| ≤ radius) :
    lo - radius ≤ observed ∧ observed ≤ hi + radius := by
  obtain ⟨he₁, he₂⟩ := abs_le.mp he
  constructor <;> linarith

theorem source_radius_sufficiency {lo hi root observed radius : ℝ}
    (hl : lo ≤ root) (hh : root ≤ hi)
    (ho₁ : hi - radius ≤ observed) (ho₂ : observed ≤ lo + radius) :
    |observed - root| ≤ radius := by
  apply abs_le.mpr
  constructor <;> linarith

theorem critical_source_strip {a b A B cap : ℝ}
    (ha : a ≤ A) (hb : B ≤ b) (hd : A - B ≤ cap) :
    (a ≤ A ∧ A ≤ b + cap) ∧ (a - cap ≤ B ∧ B ≤ b) := by
  constructor <;> constructor <;> linarith

theorem scalar_segment_stays_in_strip {lo hi x y t : ℝ}
    (hx₁ : lo ≤ x) (hx₂ : x ≤ hi) (hy₁ : lo ≤ y) (hy₂ : y ≤ hi)
    (ht₁ : 0 ≤ t) (ht₂ : t ≤ 1) :
    lo ≤ (1-t)*x+t*y ∧ (1-t)*x+t*y ≤ hi := by
  have ht : 0 ≤ 1-t := by linarith
  have h₁ := mul_le_mul_of_nonneg_left hx₁ ht
  have h₂ := mul_le_mul_of_nonneg_left hy₁ ht₁
  have h₃ := mul_le_mul_of_nonneg_left hx₂ ht
  have h₄ := mul_le_mul_of_nonneg_left hy₂ ht₁
  constructor <;> nlinarith

theorem common_budget_difference_cap {K T tau d featureDistance : ℝ}
    (hK : 0 ≤ K) (ht : tau ≤ T) (hd : d ≤ K * featureDistance)
    (hf : featureDistance ≤ 2*tau) : d ≤ 2*T*K := by
  calc
    d ≤ K * featureDistance := hd
    _ ≤ K * (2*tau) := mul_le_mul_of_nonneg_left hf hK
    _ ≤ K * (2*T) := mul_le_mul_of_nonneg_left (by linarith) hK
    _ = 2*T*K := by ring

theorem bootstrap_excludes_subthreshold {gap K T tau : ℝ}
    (hK : 0 < K) (hcap : gap/K ≤ T)
    (hseparation : tau ≤ T → gap ≤ K*tau) (ht : tau < gap/K) : False := by
  have htcap : tau ≤ T := le_trans (le_of_lt ht) hcap
  have hs := hseparation htcap
  have hstrict : tau*K < gap := (lt_div_iff₀ hK).mp ht
  nlinarith

theorem mixed_kernel_derivative (isA : Bool) (g : ℝ → ℝ) (x slope fixed : ℝ)
    (hg : HasDerivAt g slope x) :
    HasDerivAt (fun t => if isA then g t - fixed else fixed - g t)
      (if isA then slope else -slope) x := by
  cases isA
  · simpa using HasDerivAt.const_sub fixed hg
  · simpa using hg.sub_const fixed

#print axioms source_radius_necessity
#print axioms source_radius_sufficiency
#print axioms critical_source_strip
#print axioms scalar_segment_stays_in_strip
#print axioms common_budget_difference_cap
#print axioms bootstrap_excludes_subthreshold
#print axioms mixed_kernel_derivative

end SourceConstrainedNoise
