import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

namespace NoiseBoxTransfer

theorem interval_member (lo hi small big x : ℝ) (h : small ≤ big)
    (hx : lo - small ≤ x ∧ x ≤ hi + small) :
    lo - big ≤ x ∧ x ≤ hi + big := by
  constructor <;> linarith [hx.1, hx.2]

def InBox {ι : Type*} (lo hi : ι → ℝ) (radius : ℝ) (x : ι → ℝ) : Prop :=
  ∀ i, lo i - radius ≤ x i ∧ x i ≤ hi i + radius

theorem box_member {ι : Type*} (lo hi : ι → ℝ) (small big : ℝ)
    (h : small ≤ big) (x : ι → ℝ) (hx : InBox lo hi small x) :
    InBox lo hi big x := by
  intro i
  exact interval_member (lo i) (hi i) small big (x i) h (hx i)

theorem certificate_transfer {ι : Type*} (lo hi : ι → ℝ) (small big : ℝ)
    (h : small ≤ big) (P : (ι → ℝ) → Prop)
    (cert : ∀ x, InBox lo hi big x → P x) :
    ∀ x, InBox lo hi small x → P x := by
  intro x hx
  exact cert x (box_member lo hi small big h x hx)

theorem reverse_inclusion_fails :
    ¬ (∀ x : ℝ, (-1 ≤ x ∧ x ≤ 1) → (0 ≤ x ∧ x ≤ 0)) := by
  intro h
  have hx := h 1 (by constructor <;> norm_num)
  norm_num at hx

#print axioms interval_member
#print axioms box_member
#print axioms certificate_transfer
#print axioms reverse_inclusion_fails

end NoiseBoxTransfer
