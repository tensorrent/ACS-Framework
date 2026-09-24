import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import LFBound

/- The original LFBound carrier has integer doubled probabilities. This extension
   proves the bound on arbitrary real probabilities for the explicitly defined
   no-signalling, deterministic-friend branch. Quantum and topological claims are
   outside the statement. -/
namespace LFReal

abbrev Setting := LFBound.Setting
abbrev Outcome := LFBound.Outcome
abbrev Behaviour := Setting → Setting → Outcome → Outcome → ℝ

def total (B : Behaviour) (x y : Setting) : ℝ :=
  B x y .plus .plus + B x y .plus .minus + B x y .minus .plus + B x y .minus .minus
def corr (B : Behaviour) (x y : Setting) : ℝ :=
  B x y .plus .plus - B x y .plus .minus - B x y .minus .plus + B x y .minus .minus
def S (B : Behaviour) : ℝ :=
  corr B .s2 .s2 + corr B .s2 .s3 + corr B .s3 .s2 - corr B .s3 .s3
def NonNeg (B : Behaviour) : Prop := ∀ x y a b, 0 ≤ B x y a b
def Normalised (B : Behaviour) : Prop := ∀ x y, total B x y = 1
def margA (B : Behaviour) (x y : Setting) (a : Outcome) : ℝ :=
  B x y a .plus + B x y a .minus
def margB (B : Behaviour) (x y : Setting) (b : Outcome) : ℝ :=
  B x y .plus b + B x y .minus b
def NoSignalling (B : Behaviour) : Prop :=
  (∀ x a y y', margA B x y a = margA B x y' a) ∧
  (∀ y b x x', margB B x y b = margB B x' y b)
def AOEDeterministic (B : Behaviour) : Prop :=
  (∀ y, margA B .s1 y .plus = 1) ∧ (∀ x, margB B x .s1 .plus = 1)
def LFBranch (B : Behaviour) : Prop :=
  NonNeg B ∧ Normalised B ∧ NoSignalling B ∧ AOEDeterministic B

theorem corr_bounds (B : Behaviour) (hn : NonNeg B) (hs : Normalised B)
    (x y : Setting) : -1 ≤ corr B x y ∧ corr B x y ≤ 1 := by
  have h := hs x y
  have h1 := hn x y .plus .plus
  have h2 := hn x y .plus .minus
  have h3 := hn x y .minus .plus
  have h4 := hn x y .minus .minus
  simp only [total] at h
  simp only [corr]
  constructor <;> linarith

theorem S_le_four (B : Behaviour) (hn : NonNeg B) (hs : Normalised B) : S B ≤ 4 := by
  have a := (corr_bounds B hn hs .s2 .s2).2
  have b := (corr_bounds B hn hs .s2 .s3).2
  have c := (corr_bounds B hn hs .s3 .s2).2
  have d := (corr_bounds B hn hs .s3 .s3).1
  simp only [S]
  linarith

def star (x y : Setting) (a b : Outcome) : ℝ := (LFBound.star x y a b : ℝ) / 2

theorem star_nonneg : NonNeg star := by
  intro x y a b
  cases x <;> cases y <;> cases a <;> cases b <;> norm_num [star, LFBound.star]

theorem star_normalised : Normalised star := by
  intro x y
  cases x <;> cases y <;> norm_num [total, star, LFBound.star]

theorem star_nosignalling : NoSignalling star := by
  constructor
  · intro x a y y'
    cases x <;> cases a <;> cases y <;> cases y' <;>
      norm_num [margA, star, LFBound.star]
  · intro y b x x'
    cases y <;> cases b <;> cases x <;> cases x' <;>
      norm_num [margB, star, LFBound.star]

theorem star_aoe : AOEDeterministic star := by
  constructor
  · intro y; cases y <;> norm_num [margA, star, LFBound.star]
  · intro x; cases x <;> norm_num [margB, star, LFBound.star]

theorem star_is_LF : LFBranch star :=
  ⟨star_nonneg, star_normalised, star_nosignalling, star_aoe⟩

theorem star_attains_four : S star = 4 := by
  norm_num [S, corr, star, LFBound.star]

theorem lf_real_bound_is_four :
    (∃ B : Behaviour, LFBranch B ∧ S B = 4) ∧
    (∀ B : Behaviour, LFBranch B → S B ≤ 4) := by
  constructor
  · exact ⟨star, star_is_LF, star_attains_four⟩
  · intro B h
    exact S_le_four B h.1 h.2.1

end LFReal
