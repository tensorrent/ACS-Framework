import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Linarith

namespace WindowCensoring

theorem protected_inside {lo hi x y radius top : ℝ}
    (hlo : radius < lo) (hhi : hi + radius < top)
    (hxlo : lo ≤ x) (hxhi : x ≤ hi) (herror : |y - x| ≤ radius) :
    0 < y ∧ y < top := by
  obtain ⟨hel, heu⟩ := abs_le.mp herror
  constructor <;> linarith

theorem uniform_exit {lo hi x target radius top : ℝ}
    (hxlo : lo ≤ x) (hxhi : x ≤ hi) (horder : hi < target)
    (hexit : top < target) (hbudget : target - lo ≤ radius) :
    top < target ∧ |target - x| ≤ radius := by
  constructor
  · exact hexit
  · apply abs_le.mpr
    constructor <;> linarith

theorem identity_tail_excluded {x top : ℝ} (hx : top ≤ x) :
    ¬ (0 < x ∧ x < top) := by
  intro h
  linarith [h.2]

#print axioms protected_inside
#print axioms uniform_exit
#print axioms identity_tail_excluded

end WindowCensoring
