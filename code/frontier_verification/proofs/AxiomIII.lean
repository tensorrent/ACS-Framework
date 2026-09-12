/-
  Co-governed and enforced under the Sovereign Integrity Protocol License (SIP v1.1):
  https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

  # Axiom III clause (3) of the Constraint Projection Framework has no model

  The manuscript's Axiom III asks for a closed non-orientable surface M with
  w_1 != 0 and orientation double cover T^2 -- which forces M to be the Klein
  bottle K -- together with

      exists phi in Diff(M),  phi_* = [[1,2],[0,1]] in SL(2,Z).

  Everything the manuscript derives downstream of `Tr(phi_*) = 2 = Sl` rests on
  that clause: tau = i/2 in Section 3, g and s in Section 4, and the Dehn-twist
  condition lambda_UV * lambda_IR = 1/R^4 in Section 8.

  The obstruction, formalised here: every diffeomorphism of K = T^2/<tau> lifts to
  T^2 and must normalise the deck group {1, tau}.  That group is Z/2, so
  normalising means COMMUTING.  On H_1(T^2) = Z^2 the linear part of tau is
  D = diag(1,-1).  Hence the image of MCG(K) in GL(2,Z) lies in the centraliser
  of D -- and `phi_*` is not in it.

  WHAT IS PROVED HERE (all machine-checked):
    * `commutes_iff_diagonal`  the centraliser of D is exactly the diagonal matrices
    * `phi_not_commutes`       phi_* is NOT in the centraliser
    * `centraliser_unimodular` the centraliser's unimodular elements are EXACTLY four
    * `phi_infinite_order`     phi_* has infinite order, so it lies in no finite group
    * `axiom_III_clause3_unsatisfiable`  the package

  WHAT IS ASSUMED (cited, not formalised): that a diffeomorphism of K induces a
  matrix on H_1(T^2) commuting with D, and that MCG(K) = Z/2 (+) Z/2 (Lickorish,
  Proc. Camb. Phil. Soc. 59 (1963) 307).  The Lean development establishes the
  ALGEBRAIC obstruction; the topological input is external.  That boundary is
  stated deliberately -- see the closing note.

  No Mathlib.  Check with:
      lean code/constraint_projection/lean/AxiomIII.lean
  (no output, exit 0 = every theorem below is verified by Lean's kernel)

  Companion Python (two independent methods): cpf_triple_check.py check X1.
  Ledger: docs/Elimination_Ledger.md, 2026-08-29 and 2026-08-30.
-/

namespace AxiomIII

/-- A 2x2 integer matrix. -/
structure Mat2 where
  a : Int
  b : Int
  c : Int
  d : Int
deriving DecidableEq, Repr

namespace Mat2

def mul (M N : Mat2) : Mat2 :=
  ⟨M.a * N.a + M.b * N.c, M.a * N.b + M.b * N.d,
   M.c * N.a + M.d * N.c, M.c * N.b + M.d * N.d⟩

def one : Mat2 := ⟨1, 0, 0, 1⟩

def det (M : Mat2) : Int := M.a * M.d - M.b * M.c

def pow (M : Mat2) : Nat → Mat2
  | 0     => one
  | n + 1 => (pow M n).mul M

end Mat2

/-- Linear part of the deck involution `tau(x,y) = (x + 1/2, -y)` acting on
    `H_1(T^2) = Z^2`. -/
def D : Mat2 := ⟨1, 0, 0, -1⟩

/-- The map Axiom III clause (3) demands: a parabolic of trace 2. -/
def phi : Mat2 := ⟨1, 2, 0, 1⟩

/-- `M` lies in the centraliser of the deck involution. -/
def Commutes (M : Mat2) : Prop := M.mul D = D.mul M

/-- `M` is unimodular, i.e. invertible over `Z`. -/
def Unimodular (M : Mat2) : Prop := M.det = 1 ∨ M.det = -1

/-! ## The centraliser is exactly the diagonal matrices -/

theorem commutes_iff_diagonal (M : Mat2) : Commutes M ↔ M.b = 0 ∧ M.c = 0 := by
  constructor
  · intro h
    simp only [Commutes, Mat2.mul, D, Mat2.mk.injEq] at h
    omega
  · rintro ⟨hb, hc⟩
    simp only [Commutes, Mat2.mul, D, Mat2.mk.injEq, hb, hc]
    omega

/-- **`phi_*` is not in the centraliser.**  Its off-diagonal entry is 2, not 0. -/
theorem phi_not_commutes : ¬ Commutes phi := by
  rw [commutes_iff_diagonal]
  simp [phi]

/-- Explicitly: conjugating `D` by `phi_*` gives `[[1,-4],[0,-1]]`, not `D`. -/
theorem phi_conj_D : phi.mul D = ⟨1, -2, 0, -1⟩ ∧ D.mul phi = ⟨1, 2, 0, -1⟩ := by
  constructor <;> simp [Mat2.mul, phi, D]

/-! ## The centraliser has exactly four unimodular elements -/

/-- Over `Z`, a factor of a unit is a unit. -/
private theorem int_unit_left {x y : Int} (h : x * y = 1 ∨ x * y = -1) :
    x = 1 ∨ x = -1 := by
  have hd : x.natAbs ∣ 1 := by
    rcases h with h | h
    · exact ⟨y.natAbs, by rw [← Int.natAbs_mul, h]; rfl⟩
    · exact ⟨y.natAbs, by rw [← Int.natAbs_mul, h]; rfl⟩
  have : x.natAbs = 1 := Nat.dvd_one.mp hd
  omega

/-- **The centraliser of `D` in `GL(2,Z)` is `{diag(±1,±1)}` -- four elements.**
    This is the image of `MCG(K)`; it is `Z/2 ⊕ Z/2`, and in particular FINITE. -/
theorem centraliser_unimodular (M : Mat2) (hc : Commutes M) (hu : Unimodular M) :
    M = ⟨1, 0, 0, 1⟩ ∨ M = ⟨-1, 0, 0, -1⟩ ∨ M = ⟨1, 0, 0, -1⟩ ∨ M = ⟨-1, 0, 0, 1⟩ := by
  obtain ⟨a, b, c, d⟩ := M
  obtain ⟨hb, hc'⟩ := (commutes_iff_diagonal ⟨a, b, c, d⟩).mp hc
  simp only at hb hc'
  subst hb
  subst hc'
  simp only [Unimodular, Mat2.det] at hu
  simp only [Mat2.mk.injEq, true_and, and_true]
  have had : a * d = 1 ∨ a * d = -1 := by omega
  have ha := int_unit_left had
  rcases ha with ha | ha <;> subst ha <;> rcases had with hd | hd <;> omega

/-- Within that centraliser, trace `+2` is attained ONLY by the identity -- so even
    the weaker reading "some mapping class has `Tr(phi_*) = 2`" is carried by the
    trivial class, which is no Dehn twist and supplies no self-linking number. -/
theorem trace_two_only_identity (M : Mat2) (hc : Commutes M) (hu : Unimodular M)
    (ht : M.a + M.d = 2) : M = Mat2.one := by
  rcases centraliser_unimodular M hc hu with h | h | h | h
  · rw [h]; rfl
  · rw [h] at ht; exact absurd ht (by decide)
  · rw [h] at ht; exact absurd ht (by decide)
  · rw [h] at ht; exact absurd ht (by decide)

/-! ## `phi_*` has infinite order -/

theorem phi_pow (n : Nat) : Mat2.pow phi n = ⟨1, 2 * (n : Int), 0, 1⟩ := by
  induction n with
  | zero => simp [Mat2.pow, Mat2.one]
  | succ k ih =>
      show (Mat2.pow phi k).mul phi = _
      rw [ih]
      simp only [Mat2.mul, phi, Mat2.mk.injEq, true_and, and_true]
      omega

/-- **`phi_*` is parabolic of infinite order**, so it cannot lie in ANY finite group
    -- an obstruction independent of the commuting one above. -/
theorem phi_infinite_order (n : Nat) (hn : 1 ≤ n) : Mat2.pow phi n ≠ Mat2.one := by
  rw [phi_pow]
  simp only [Mat2.one, ne_eq, Mat2.mk.injEq, not_and]
  intro _ h
  omega

/-! ## The package -/

/-- **Axiom III clause (3) is unsatisfiable.**

    Three independent statements, each machine-checked:
    1. the centraliser of the deck involution is exactly the diagonal matrices;
    2. `phi_*` is not diagonal, hence not in the centraliser;
    3. `phi_*` has infinite order, hence lies in no finite group -- and the
       centraliser's unimodular part has exactly four elements.

    Given the (external, cited) fact that a diffeomorphism of the Klein bottle
    induces a matrix on `H_1(T^2)` commuting with `D`, no such diffeomorphism
    induces `phi_*`. -/
theorem axiom_III_clause3_unsatisfiable :
    (∀ M : Mat2, Commutes M ↔ M.b = 0 ∧ M.c = 0) ∧
    (¬ Commutes phi) ∧
    (∀ M : Mat2, Commutes M → Unimodular M →
        M = ⟨1, 0, 0, 1⟩ ∨ M = ⟨-1, 0, 0, -1⟩ ∨
        M = ⟨1, 0, 0, -1⟩ ∨ M = ⟨-1, 0, 0, 1⟩) ∧
    (∀ n : Nat, 1 ≤ n → Mat2.pow phi n ≠ Mat2.one) :=
  ⟨commutes_iff_diagonal, phi_not_commutes, centraliser_unimodular, phi_infinite_order⟩

/-!
## Scope

**Proved here.** The algebraic obstruction, in full: the centraliser of
`D = diag(1,-1)` in the integer matrices is the diagonal subgroup; its unimodular
part is exactly the four `diag(±1,±1)`; `phi_* = [[1,2],[0,1]]` is not among them;
and `phi_*` has infinite order.

**Assumed, not proved.** That a diffeomorphism of `K` lifts to `T^2` and induces a
matrix on `H_1` commuting with `D`, and that `MCG(K) = Z/2 ⊕ Z/2` (Lickorish 1963).
Those are the topological inputs. Formalising them would require a development of
surface topology far beyond this file, and they are not in dispute -- the
manuscript's error is algebraic, and that is what is machine-checked here.

**Independent confirmation.** `cpf_triple_check.py` check X1 reaches the same four
matrices by a second route that never mentions the deck transformation: computing
`Out(pi_1(K))` from the presentation `<a,b | b a b^-1 = a^-1>` by symbolic word
algebra, and reading its action on `H_1` of the cover. The two methods share no
machinery.
-/

end AxiomIII
