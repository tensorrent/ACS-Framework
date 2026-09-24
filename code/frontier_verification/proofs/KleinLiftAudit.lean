import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import AxiomIII

/- Integer normal forms a^m b^n for b a b^-1 = a^-1.
   The surface/cover interpretation is stated separately from these algebraic
   theorems. In particular, no homology-to-isotopy injectivity is assumed. -/
namespace KleinLiftAudit

abbrev K := ℤ × ℤ

def sign (n : ℤ) : ℤ := if n % 2 = 0 then 1 else -1
def mul (g h : K) : K := (g.1 + sign g.2 * h.1, g.2 + h.2)
def one : K := (0, 0)
def inv (g : K) : K := (-sign g.2 * g.1, -g.2)
def a : K := (1, 0)
def b : K := (0, 1)

theorem sign_add (n m : ℤ) : sign (n + m) = sign n * sign m := by
  unfold sign
  split_ifs <;> omega

theorem sign_neg (n : ℤ) : sign (-n) = sign n := by
  unfold sign
  split_ifs <;> omega

theorem sign_square (n : ℤ) : sign n * sign n = 1 := by
  unfold sign
  split_ifs <;> norm_num

theorem parity_cocycle (n m : ℤ) : (n + m) % 2 = n % 2 + sign n * (m % 2) := by
  unfold sign
  split_ifs <;> omega

theorem mul_assoc (g h k : K) : mul (mul g h) k = mul g (mul h k) := by
  apply Prod.ext
  · simp only [mul, sign_add]
    ring
  · simp [mul, add_assoc]

theorem one_mul (g : K) : mul one g = g := by
  rcases g with ⟨m,n⟩
  simp [mul, one, sign]

theorem mul_one (g : K) : mul g one = g := by
  rcases g with ⟨m,n⟩
  simp [mul, one]

theorem inv_mul (g : K) : mul (inv g) g = one := by
  simp [mul, inv, one, sign_neg]

theorem mul_inv (g : K) : mul g (inv g) = one := by
  apply Prod.ext
  · simp only [mul, inv, one]
    calc
      g.1 + sign g.2 * (-sign g.2 * g.1) = g.1 - (sign g.2 * sign g.2) * g.1 := by ring
      _ = 0 := by rw [sign_square]; ring
  · simp [mul, inv, one]

theorem klein_relation : mul (mul b a) (inv b) = inv a := by
  norm_num [mul, inv, a, b, sign]

/-- Conjugation by the affine half-translation on the universal cover. -/
def twist (g : K) : K := (g.1 + g.2 % 2, g.2)
def untwist (g : K) : K := (g.1 - g.2 % 2, g.2)

theorem twist_mul (g h : K) : twist (mul g h) = mul (twist g) (twist h) := by
  apply Prod.ext
  · simp only [mul, twist, parity_cocycle]
    ring
  · rfl

theorem twist_untwist (g : K) : twist (untwist g) = g := by
  rcases g with ⟨m,n⟩
  simp [twist, untwist]

theorem untwist_twist (g : K) : untwist (twist g) = g := by
  rcases g with ⟨m,n⟩
  simp [twist, untwist]

theorem twist_b : twist b = (1, 1) := by norm_num [twist, b]

theorem inner_b (g : K) : mul (mul g b) (inv g) = (2 * g.1, 1) := by
  apply Prod.ext
  · simp only [mul, b, inv, mul_zero, add_zero]
    rw [sign_add]
    norm_num [sign] at *
    split_ifs <;> ring
  · simp [mul, b, inv]

def IsInner (f : K → K) : Prop := ∃ g, ∀ h, f h = mul (mul g h) (inv g)

/-- The twist is a non-inner automorphism, although it fixes the cover subgroup. -/
theorem twist_not_inner : ¬ IsInner twist := by
  rintro ⟨g, hg⟩
  have h := hg b
  rw [twist_b, inner_b] at h
  have hfirst := congrArg Prod.fst h
  change (1 : ℤ) = 2 * g.1 at hfirst
  omega

theorem twist_fixes_cover (m n : ℤ) : twist (m, 2 * n) = (m, 2 * n) := by
  simp [twist]

theorem twist_square_inner (g : K) : twist (twist g) = mul (mul a g) (inv a) := by
  apply Prod.ext
  · simp [twist, mul, a, inv, sign]
    split_ifs <;> omega
  · simp [twist, mul, a, inv]

/-- The original matrix obstruction remains valid. -/
theorem parabolic_still_excluded : ¬ AxiomIII.Commutes AxiomIII.phi :=
  AxiomIII.phi_not_commutes

/-- Normalizing a two-element deck group forces commuting with its nonidentity element. -/
theorem normalizer_two_commutes {G : Type*} [Group G] (f t : G) (ht : t ≠ 1)
    (hn : f * t * f⁻¹ = 1 ∨ f * t * f⁻¹ = t) : f * t = t * f := by
  rcases hn with h | h
  · have h' := congrArg (fun z => f⁻¹ * z * f) h
    simp [_root_.mul_assoc] at h'
    exact (ht h').elim
  · calc
      f * t = (f * t * f⁻¹) * f := by simp [_root_.mul_assoc]
      _ = t * f := by rw [h]

/-- A canonical orientation-preserving lift can only have I or -I as its matrix. -/
theorem positive_centraliser (M : AxiomIII.Mat2) (hc : AxiomIII.Commutes M)
    (hd : M.det = 1) : M = AxiomIII.Mat2.one ∨ M = ⟨-1, 0, 0, -1⟩ := by
  rcases AxiomIII.centraliser_unimodular M hc (Or.inl hd) with h | h | h | h
  · left; exact h
  · right; exact h
  · rw [h] at hd; norm_num [AxiomIII.Mat2.det] at hd
  · rw [h] at hd; norm_num [AxiomIII.Mat2.det] at hd

end KleinLiftAudit
