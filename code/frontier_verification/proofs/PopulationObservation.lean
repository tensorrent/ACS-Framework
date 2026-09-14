import Mathlib.Basic.Real.Basic
import Mathlib.Data.List.Forall2
import Mathlib.Data.List.Permutation
import Mathlib.Tactic.Linarith

namespace PopulationObservation

def FixedPopulation (source observed : List ℝ) (radius : ℝ) : Prop :=
  ∃ reordered : List ℝ, reordered.Perm source ∧
    List.Forall₂ (fun x y => |x - y| ≤ radius) observed reordered

theorem fixed_population_length {source observed : List ℝ} {radius : ℝ}
    (h : FixedPopulation source observed radius) : observed.length = source.length := by
  obtain ⟨reordered, hp, hn⟩ := h
  exact hn.length_eq.trans hp.length_eq

theorem unequal_populations_disjoint {a b observed : List ℝ} {ra rb : ℝ}
    (hne : a.length ≠ b.length)
    (ha : FixedPopulation a observed ra) (hb : FixedPopulation b observed rb) : False := by
  exact hne ((fixed_population_length ha).symm.trans (fixed_population_length hb))

theorem uncrossing {a a' b b' radius : ℝ} (ha : a ≤ a') (hb : b ≤ b')
    (h₁ : |a - b'| ≤ radius) (h₂ : |a' - b| ≤ radius) :
    |a - b| ≤ radius ∧ |a' - b'| ≤ radius := by
  obtain ⟨h₁l, h₁u⟩ := abs_le.mp h₁
  obtain ⟨h₂l, h₂u⟩ := abs_le.mp h₂
  constructor
  · apply abs_le.mpr
    constructor <;> linarith
  · apply abs_le.mpr
    constructor <;> linarith

theorem common_observation_separation {a b observed radius : ℝ}
    (ha : |a - observed| ≤ radius) (hb : |b - observed| ≤ radius) :
    |a - b| ≤ 2 * radius := by
  obtain ⟨hal, hau⟩ := abs_le.mp ha
  obtain ⟨hbl, hbu⟩ := abs_le.mp hb
  apply abs_le.mpr
  constructor <;> linarith

theorem interval_center {lo hi x : ℝ} (hlo : lo ≤ x) (hhi : x ≤ hi) :
    |x - (lo + hi) / 2| ≤ (hi - lo) / 2 := by
  apply abs_le.mpr
  constructor <;> linarith

#print axioms fixed_population_length
#print axioms unequal_populations_disjoint
#print axioms uncrossing
#print axioms common_observation_separation
#print axioms interval_center

end PopulationObservation
