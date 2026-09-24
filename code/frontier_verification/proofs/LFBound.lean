/-
  Co-governed and enforced under the Sovereign Integrity Protocol License (SIP v1.1):
  https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

  # The Local Friendliness bound on the Constraint Projection Framework's Section 5 sum

  Formalises the proposition that carried the 2026-08-29 correction to this audit's
  own earlier verdict:

      max over the Local Friendliness polytope of
          S = E(A2,B2) + E(A2,B3) + E(A3,B2) - E(A3,B3)
      is exactly 4.

  The CPF manuscript reports S = 2*sqrt 2 ~ 2.828 and calls it a Local Friendliness
  violation because 2*sqrt 2 > 2.  But 2 is the *Bell* local bound.  The LF bound on
  this expression is 4, so the value violates no LF inequality -- and since Tsirelson
  caps any quantum realisation at 2*sqrt 2 < 4, none is reachable even in principle.

  Two halves, both proved here:
    * `S_le_four`      -- S <= 4 for ANY normalised non-negative behaviour.
    * `star_S_eq_four` -- an explicit LF behaviour attains S = 4, so the bound is tight.
  `lf_bound_is_four` packages them as `IsGreatest`.

  Note on the upper bound: it needs only normalisation and non-negativity, NOT the LF
  conditions.  That is honest and is the point -- the content is entirely in
  attainment, i.e. that a *bona fide LF* behaviour reaches 4.

  ARITHMETIC.  Everything is done in doubled integer units: `B x y a b` denotes
  2 * p(a,b | x,y).  Every probability in play is 0, 1/2 or 1, so doubling clears all
  denominators and keeps the development inside `Int`.  This deliberately avoids any
  Mathlib dependency: the file checks with a bare `lean` binary in seconds.

  Check with:   lean code/constraint_projection/lean/LFBound.lean
  (no output and exit code 0 means every theorem below is machine-verified)

  Companion Python (exact rationals, same certificate):
    code/constraint_projection/cpf_triple_check.py, check X2
  Ledger: docs/Elimination_Ledger.md, 2026-08-29 and 2026-08-30.
-/

namespace LFBound

/-- Measurement settings.  `s1` is the *friend* setting: "open the lab and read the
    friend's already-recorded outcome".  `s2`, `s3` are superobserver settings. -/
inductive Setting | s1 | s2 | s3
  deriving DecidableEq, Repr

/-- Binary outcomes, valued +1 and -1. -/
inductive Outcome | plus | minus
  deriving DecidableEq, Repr

/-- The value (either 1 or minus 1) carried by an outcome. -/
def Outcome.val : Outcome → Int
  | .plus  =>  1
  | .minus => -1

/-- A behaviour in doubled units: `B x y a b = 2 * p(a,b | x,y)`. -/
abbrev Behaviour := Setting → Setting → Outcome → Outcome → Int

variable (B : Behaviour)

/-- Total weight on a setting pair (doubled, so a normalised behaviour gives 2). -/
def total (x y : Setting) : Int :=
  B x y .plus .plus + B x y .plus .minus + B x y .minus .plus + B x y .minus .minus

/-- Alice's marginal (doubled). -/
def margA (x y : Setting) (a : Outcome) : Int := B x y a .plus + B x y a .minus

/-- Bob's marginal (doubled). -/
def margB (x y : Setting) (b : Outcome) : Int := B x y .plus b + B x y .minus b

/-- The correlator, doubled: `corr2 B x y = 2 * E(x,y)`. -/
def corr2 (x y : Setting) : Int :=
  Outcome.val .plus  * Outcome.val .plus  * B x y .plus  .plus  +
  Outcome.val .plus  * Outcome.val .minus * B x y .plus  .minus +
  Outcome.val .minus * Outcome.val .plus  * B x y .minus .plus  +
  Outcome.val .minus * Outcome.val .minus * B x y .minus .minus

/-- The manuscript's sum, doubled: `S2 B = 2 * S`. -/
def S2 : Int :=
  corr2 B .s2 .s2 + corr2 B .s2 .s3 + corr2 B .s3 .s2 - corr2 B .s3 .s3

/-- Probabilities are non-negative. -/
def NonNeg : Prop := ∀ x y a b, 0 ≤ B x y a b

/-- Probabilities sum to one on every setting pair. -/
def Normalised : Prop := ∀ x y, total B x y = 2

/-- No-signalling: neither wing's marginal depends on the other wing's setting. -/
def NoSignalling : Prop :=
  (∀ x a y y', margA B x y a = margA B x y' a) ∧
  (∀ y b x x', margB B x y b = margB B x' y b)

/-- Absoluteness of Observed Events, at the level of one hidden-variable branch:
    conditioned on the branch, the friend-setting outcomes are *deterministic*.
    Here the branch is `a1 = b1 = plus`. -/
def AOEDeterministic : Prop :=
  (∀ y, margA B .s1 y .plus = 2) ∧ (∀ x, margB B x .s1 .plus = 2)

/-- A Local Friendliness branch: a no-signalling behaviour whose friend-setting
    marginals are deterministic.  The LF polytope is the convex hull of these, so
    maximising a linear functional over LF = maximising over these generators. -/
def LFBranch : Prop :=
  NonNeg B ∧ Normalised B ∧ NoSignalling B ∧ AOEDeterministic B

/-! ## Upper bound -/

/-- Every correlator lies in [-1,1]; doubled, in [-2,2]. -/
theorem corr2_le_two (hn : NonNeg B) (hs : Normalised B) (x y : Setting) :
    corr2 B x y ≤ 2 := by
  have h := hs x y
  have h1 := hn x y .plus .plus
  have h2 := hn x y .plus .minus
  have h3 := hn x y .minus .plus
  have h4 := hn x y .minus .minus
  simp only [total] at h
  simp only [corr2, Outcome.val]
  omega

theorem neg_two_le_corr2 (hn : NonNeg B) (hs : Normalised B) (x y : Setting) :
    -2 ≤ corr2 B x y := by
  have h := hs x y
  have h1 := hn x y .plus .plus
  have h2 := hn x y .plus .minus
  have h3 := hn x y .minus .plus
  have h4 := hn x y .minus .minus
  simp only [total] at h
  simp only [corr2, Outcome.val]
  omega

/-- **S ≤ 4** for any normalised non-negative behaviour.  Note this does not even
    need the LF conditions -- it holds on the whole no-signalling polytope, and
    indeed on all behaviours. -/
theorem S_le_four (hn : NonNeg B) (hs : Normalised B) : S2 B ≤ 8 := by
  have a := corr2_le_two B hn hs .s2 .s2
  have b := corr2_le_two B hn hs .s2 .s3
  have c := corr2_le_two B hn hs .s3 .s2
  have d := neg_two_le_corr2 B hn hs .s3 .s3
  simp only [S2]
  omega

/-! ## Attainment: an explicit LF behaviour reaching S = 4 -/

/-- The witness.  Branch `a1 = b1 = plus`; a PR box on the superobserver settings
    `{s2,s3}`; product form on the mixed rows.  In ordinary probabilities the
    entries are 0, 1/2 and 1; doubled they are 0, 1 and 2. -/
def star : Behaviour
  -- friend/friend: the recorded outcomes, deterministic
  | .s1, .s1, .plus,  .plus  => 2
  | .s1, .s1, _,      _      => 0
  -- friend on Alice's side, superobserver on Bob's: Alice fixed, Bob uniform
  | .s1, _,   .plus,  _      => 1
  | .s1, _,   .minus, _      => 0
  -- superobserver on Alice's side, friend on Bob's: Bob fixed, Alice uniform
  | _,   .s1, _,      .plus  => 1
  | _,   .s1, _,      .minus => 0
  -- PR box on {s2,s3} x {s2,s3}: outcomes agree except at (s3,s3)
  | .s3, .s3, .plus,  .minus => 1
  | .s3, .s3, .minus, .plus  => 1
  | .s3, .s3, _,      _      => 0
  | _,   _,   .plus,  .plus  => 1
  | _,   _,   .minus, .minus => 1
  | _,   _,   _,      _      => 0

theorem star_nonneg : NonNeg star := by
  intro x y a b; cases x <;> cases y <;> cases a <;> cases b <;> decide

theorem star_normalised : Normalised star := by
  intro x y; cases x <;> cases y <;> decide

theorem star_nosignalling : NoSignalling star := by
  constructor
  · intro x a y y'; cases x <;> cases a <;> cases y <;> cases y' <;> decide
  · intro y b x x'; cases y <;> cases b <;> cases x <;> cases x' <;> decide

theorem star_aoe : AOEDeterministic star := by
  constructor
  · intro y; cases y <;> decide
  · intro x; cases x <;> decide

/-- The witness is a genuine Local Friendliness branch. -/
theorem star_is_LF : LFBranch star :=
  ⟨star_nonneg, star_normalised, star_nosignalling, star_aoe⟩

/-- …and it attains `S = 4` (doubled: 8). -/
theorem star_S_eq_four : S2 star = 8 := by decide

/-! ## The bound -/

/-- **The Local Friendliness bound on the manuscript's sum is exactly 4.**

    Stated as: the value 8 (= 2*S with S = 4) is ATTAINED by an LF branch, and is an
    UPPER BOUND over all LF branches.  Since LF branches generate the LF polytope and
    `S2` is linear, its maximum over the convex hull equals its maximum over the
    generators, so this is the LF maximum. -/
theorem lf_bound_is_four :
    (∃ B : Behaviour, LFBranch B ∧ S2 B = 8) ∧
    (∀ B : Behaviour, LFBranch B → S2 B ≤ 8) := by
  refine ⟨⟨star, star_is_LF, star_S_eq_four⟩, ?_⟩
  rintro B ⟨hn, hs, -, -⟩
  exact S_le_four B hn hs

/-!
## What this does and does not establish

**Does.**  `S <= 4` on every normalised non-negative behaviour, and `S = 4` is
attained by an explicit behaviour that is no-signalling and has deterministic
friend-setting marginals.  So 4 is the exact LF maximum.

**Does not.**  Nothing here is a statement about quantum mechanics.  The relevant
external facts, used in the audit but NOT formalised here, are:
  * Tsirelson's bound caps any quantum value of this expression at 2*sqrt 2;
  * the Bell local bound on it is 2 (exhaustive over 64 deterministic strategies,
    checked numerically in cpf_triple_check.py, not here).
Given those, 2 < 2*sqrt 2 < 4 places the manuscript's value strictly inside the LF
polytope, which is the audit's conclusion.

**Scope of "LF" here.**  `LFBranch` encodes one branch of the LF decomposition.
The LF polytope is the convex hull of such branches over the four choices of
(a1,b1); `star` uses the branch a1 = b1 = plus.  Because `S2` is linear, the maximum
over the hull equals the maximum over branches, so exhibiting one branch attaining 8
together with the universal upper bound settles the maximum.  That the *other* three
branches also attain 8 is checked numerically (four LPs, all returning 4.0) but is
not needed for this theorem and is not claimed here.
-/

end LFBound
