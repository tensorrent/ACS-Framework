import Mathlib.Basic.Real.Basic
import Mathlib.Data.List.Permutation
import Mathlib.Tactic.Linarith
import Lean.Elab.Tactic.Omega

namespace InteriorCount

theorem suffix_point_above {a b x y r : ℝ} (hxa : a ≤ x)
    (herr : |x - y| ≤ r) (hr : r < (a - b) / 2) : (a + b) / 2 < y := by
  obtain ⟨hl, hu⟩ := abs_le.mp herr
  linarith

theorem prefix_point_below {a b x y r : ℝ} (hxb : x ≤ b)
    (herr : |x - y| ≤ r) (hr : r < (a - b) / 2) : y < (a + b) / 2 := by
  obtain ⟨hl, hu⟩ := abs_le.mp herr
  linarith

theorem interval_gate_above {alo bhi x y r : ℝ} (hlo : alo ≤ x)
    (herr : |x - y| ≤ r) (hr : r < (alo - bhi) / 2) : (alo + bhi) / 2 < y := by
  exact suffix_point_above hlo herr hr

theorem interval_gate_below {alo bhi x y r : ℝ} (hhi : x ≤ bhi)
    (herr : |x - y| ≤ r) (hr : r < (alo - bhi) / 2) : y < (alo + bhi) / 2 := by
  exact prefix_point_below hhi herr hr

theorem suffix_filter_bound {α : Type*} (p : α → Bool) (pre suffix : List α)
    (h : ∀ x ∈ suffix, p x = false) : ((pre ++ suffix).filter p).length ≤ pre.length := by
  have hs : suffix.filter p = [] := List.filter_eq_nil_iff.mpr (by
    intro x hx
    simp [h x hx])
  simpa [List.filter_append, hs] using List.length_filter_le p pre

theorem prefix_filter_bound {α : Type*} (p : α → Bool) (pre suffix : List α)
    (h : ∀ x ∈ pre, p x = true) : pre.length ≤ ((pre ++ suffix).filter p).length := by
  have hp : pre.filter p = pre := List.filter_eq_self.mpr h
  simp only [List.filter_append, hp, List.length_append]
  omega

theorem count_separation {α : Type*} (p : α → Bool)
    (ap asuf bp bsuf : List α) (ha : ∀ x ∈ asuf, p x = false)
    (hb : ∀ x ∈ bp, p x = true) (hlen : ap.length < bp.length) :
    ((ap ++ asuf).filter p).length < ((bp ++ bsuf).filter p).length := by
  have h₁ := suffix_filter_bound p ap asuf ha
  have h₂ := prefix_filter_bound p bp bsuf hb
  omega

theorem count_permutation {α : Type*} (p : α → Bool) {a b : List α}
    (h : a.Perm b) : (a.filter p).length = (b.filter p).length := by
  exact (h.filter p).length_eq

#print axioms suffix_point_above
#print axioms prefix_point_below
#print axioms interval_gate_above
#print axioms interval_gate_below
#print axioms suffix_filter_bound
#print axioms prefix_filter_bound
#print axioms count_separation
#print axioms count_permutation

end InteriorCount
