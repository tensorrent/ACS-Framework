import Mathlib.Topology.MetricSpace.Contracting
import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Linarith

namespace FeatureContraction

theorem uniform_interval_error {lo hi ol oh x y r : ℝ}
    (hxlo : lo ≤ x) (hxhi : x ≤ hi) (hylo : ol ≤ y) (hyhi : y ≤ oh)
    (hleft : hi - r ≤ ol) (hright : oh ≤ lo + r) : |x - y| ≤ r := by
  apply abs_le.mpr
  constructor <;> linarith

theorem self_map_from_center_bound {E : Type*} [MetricSpace E]
    (T : E → E) (c : E) {q eta rho : ℝ} (hq : 0 ≤ q)
    (hcenter : dist (T c) c ≤ eta) (hbudget : eta + q * rho ≤ rho)
    (hlip : ∀ x ∈ Metric.closedBall c rho, dist (T x) (T c) ≤ q * dist x c) :
    Set.MapsTo T (Metric.closedBall c rho) (Metric.closedBall c rho) := by
  intro x hx
  have hx' : dist x c ≤ rho := hx
  have hmul := mul_le_mul_of_nonneg_left hx' hq
  have hstep := hlip x hx
  have htriangle := dist_triangle (T x) (T c) c
  change dist (T x) c ≤ rho
  linarith

theorem preconditioned_fixed_point_zero {E : Type*} [AddGroup E]
    (F : E → E) (R : E →+ E) (hR : Function.Injective R) {x : E}
    (hx : x - R (F x) = x) : F x = 0 := by
  apply hR
  simpa only [map_zero] using (sub_eq_self.mp hx)

theorem contracting_root_on_complete_set {E : Type*} [MetricSpace E] [AddGroup E]
    (F : E → E) (R : E →+ E) (hR : Function.Injective R)
    {s : Set E} (hcomplete : IsComplete s) {x0 : E} (hx0 : x0 ∈ s)
    (hmaps : Set.MapsTo (fun x => x - R (F x)) s s) {q : NNReal}
    (hcon : ContractingWith q (hmaps.restrict (fun x => x - R (F x)) s s)) :
    ∃ x ∈ s, F x = 0 := by
  obtain ⟨x, hxs, hfix, _, _⟩ := hcon.exists_fixedPoint' hcomplete hmaps hx0 (edist_ne_top _ _)
  exact ⟨x, hxs, preconditioned_fixed_point_zero F R hR hfix⟩

theorem strict_radius_improvement {L U epsilon : ℝ} (h : U - L < epsilon) :
    U - epsilon < L := by
  linarith

theorem equal_features_from_zero_difference {E : Type*} [AddGroup E] {a b : E}
    (h : a - b = 0) : a = b := sub_eq_zero.mp h

#print axioms uniform_interval_error
#print axioms self_map_from_center_bound
#print axioms preconditioned_fixed_point_zero
#print axioms contracting_root_on_complete_set
#print axioms strict_radius_improvement
#print axioms equal_features_from_zero_difference

end FeatureContraction
