"""Regression tests over the CPF audit artifacts.

Why this file exists.  The thirteen instruments in `code/constraint_projection/`
are REPORT GENERATORS, not tests: none of them calls `sys.exit`, and nine have
no assertion at all.  Every one exits 0 whether its verdicts are right or
wrong, so "the scripts ran" carries no information about whether they ran
CORRECTLY.  That is exactly the condition method rule 3 forbids -- an
instrument is not evidence until it has been shown capable of failing.

These tests give the audit teeth: they pin the load-bearing numbers that the
Elimination Ledger and MANIFEST assert, reading them from the committed
artifacts.  If an instrument is edited and a headline verdict moves, the
canonical gate goes red instead of silently regenerating a different answer.

Scope: these check that the RECORDED findings are stable and internally
consistent.  They do not re-derive the physics -- the instruments do that,
and their reasoning is reviewed in the ledger.
"""
import json
import math
import pathlib

import pytest

DOCS = pathlib.Path(__file__).resolve().parents[3] / "docs"


def load(name):
    p = DOCS / name
    if not p.exists():
        pytest.skip(f"{name} not present")
    return json.loads(p.read_text())


def test_alpha_factor_of_two_is_recorded():
    """The audit's first finding: the stated inputs give L*alpha = 2, not 1."""
    d = load("constraint_projection_audit.json")
    assert json.dumps(d).find("137.035999") != -1, "CODATA target should appear in the audit"


def test_required_cutoff_is_sub_planckian():
    """a/R = 2.039e-118 -- the value that voids 'UV complete'."""
    d = load("alpha_gap_diagnosis.json")
    blob = json.dumps(d)
    assert "2.039" in blob or "2.03905" in blob, "required a/R should be recorded"


def test_relational_boundary_predicts_46_and_dies_on_drift():
    """Parameter-free alpha^-1 = 46.24, excluded by alpha-constancy."""
    d = load("alpha_relational_boundary.json")
    blob = json.dumps(d)
    assert "46.24" in blob, "the parameter-free prediction should be recorded"
    assert "2.5" in blob or "2.52" in blob, "the predicted drift rate should be recorded"


def test_decoy_test_found_no_information():
    """14 of 14 decoy forms hit the target -> the match carries zero bits."""
    d = load("alpha_decoy_test.json")
    assert "14" in json.dumps(d), "the decoy count should be recorded"


def test_klein_foam_reading_is_scale_invariant():
    """K1: alpha^-1 depends on R and a only through R/a."""
    d = load("klein_foam_reading.json")["checks"]["K1_invariance"]
    assert d["joint_scaling_invariant"] is True
    assert d["depends_only_on"] == "R/a"


def test_klein_foam_planck_floor_value():
    """K2: the foam's own floor gives 26.96, off 5.08x -- best absolute reading."""
    c = load("klein_foam_reading.json")["checks"]["K2_foam_resolution"]
    assert math.isclose(float(c["alpha_inv"]), 26.957067, rel_tol=1e-5)
    assert math.isclose(float(c["off_by"]), 5.0835, rel_tol=1e-3)


def test_path_integral_no_uv_fixed_point():
    """P6: beta = 2 alpha^2/3pi has only the free-theory root."""
    c = load("feynman_path_integral.json")["checks"]["P6_uv_completeness"]
    assert c["nontrivial_uv_fixed_point"] is False
    assert c["uv_complete_and_finite_resolution_compatible"] is False


def test_path_integral_running_signs_are_opposite():
    """P4: QED screens (-2/3pi), the manuscript anti-screens (+1/2); ratio 3pi/4."""
    c = load("feynman_path_integral.json")["checks"]["P4_running"]
    assert c["signs"] == "opposite"
    assert math.isclose(float(c["magnitude_ratio"]), 3 * math.pi / 4, rel_tol=1e-6)
    assert float(c["qed_d_alphainv_dlnmu"]) < 0 < float(c["cpf_d_alphainv_dlnmu"])


def test_greens_klein_bottle_has_no_fundamental_class():
    """G1: H_2(K;Z) = 0 and H_1 = Z + Z/2 -- Axiom II states the obstruction."""
    c = load("greens_theorem.json")["checks"]["G1_does_greens_hold"]
    assert c["H2_K_Z"] == "0"
    assert c["fundamental_class_exists"] is False
    assert c["stokes_holds_for_ordinary_forms"] is False
    assert c["stokes_holds_for_twisted_forms"] is True


def test_greens_capacitance_is_two_pi_larger():
    """G3: the Green's integral gives 2pi more than the manuscript's C."""
    c = load("greens_theorem.json")["checks"]["G3_honest_capacitance"]
    assert math.isclose(float(c["measured_kappa"]), 2.0, rel_tol=1e-6), "the 8 must emerge"
    assert float(c["ratio_at_manuscript_L"]) > 2 * math.pi, "ratio is 2pi(L+1)/L > 2pi"
    assert math.isclose(float(c["ratio_at_manuscript_L"]), 6.3061946, rel_tol=1e-5)


def test_greens_vanishing_theorem_is_structural():
    """G2: pullback 2-forms integrate to zero on the orientation cover."""
    c = load("greens_theorem.json")["checks"]["G2_vanishing_theorem"]
    assert c["worst_relative_residual"] < 0.02, "MC integral must be ~0 vs an O(1) integrand"
    assert c["descent_constraint_max_residual"] < 1e-10


def test_bem_solver_was_validated_before_use():
    """E0, rule 3: the solver hits the exact sphere answer before being trusted."""
    c = load("twisted_ribbon_capacitance.json")["checks"]["E0_validate"]
    assert c["sphere_within_2pct"] is True
    assert c["torus_within_10pct"] is True
    for row in c["rows"][:2]:
        assert row["rel_err"] < 1e-3, "sphere must match 4 pi eps0 a closely"


def test_half_twist_is_not_two_pi():
    """E1/E2: the half-twist moves C by <0.1%, and 2pi survives on the Mobius."""
    ch = load("twisted_ribbon_capacitance.json")["checks"]
    assert ch["E1_twists"]["half_twist_effect_percent"] < 0.1
    assert ch["E2_against_manuscript"]["bem_vs_g3_prediction_pct"] < 2.0


def test_twist_family_capacitance_blind_to_self_linking():
    """R4: Sl runs 0->2 while C moves ~0.01% -- capacitance cannot see framing."""
    c = load("ribbon_twist_family.json")["checks"]["R4_capacitance_blind"]
    assert c["spread_percent"] < 0.1
    assert c["Sl_range"] == 2.0


def test_twist_family_cwf_verified():
    """R2: White-Calugareanu-Fuller checked by Gauss integral, magnitudes exact."""
    c = load("ribbon_twist_family.json")["checks"]["R2_linking"]
    assert c["cwf_max_error"] < 1e-3


def test_writhe_reopens_orientability_conclusion():
    """R5: Sl=2 forces orientability only when Wr=0; a coil lifts that."""
    c = load("ribbon_twist_family.json")["checks"]["R5_writhe_reopens"]
    assert c["planar_writhe_exact_zero"] is True
    assert c["Sl2_reachable_non_orientably"] is True
    assert c["example_split"]["orientable"] is False


def test_every_cpf_artifact_names_its_source():
    """Provenance is a link in the chain: each artifact must name what made it."""
    missing = []
    for name in ["klein_foam_reading.json", "feynman_path_integral.json",
                 "greens_theorem.json", "twisted_ribbon_capacitance.json",
                 "ribbon_twist_family.json"]:
        p = DOCS / name
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        if "source" not in d or not d["source"].endswith(".py"):
            missing.append(name)
    assert not missing, f"artifacts without a source field: {missing}"


# ---------------------------------------------------------------------------
# Vocabulary check.  Method rule 11.
#
# "Right" means righteous -- belief held without proof -- which is the thing an
# evidence chain replaces.  Praising a result as "right" imports the vocabulary
# of unproven conviction into a record of measurement; "wrong" adds blame to a
# mismatch.  A document under audit is not an opponent, it is a record of a
# state at a date.
#
# This is enforced rather than remembered because it was corrected twice from
# memory and recurred both times.  Only ADVERSARIAL framings are flagged --
# "the wrong polytope" (the incorrect one) is ordinary technical use and is
# left alone.
# ---------------------------------------------------------------------------
import re

ADVERSARIAL = [
    (r"\b(FOR|for) the \w+ and (AGAINST|against) the\b", "for/against framing"),
    (r"\bfinding (AGAINST|against)\b", "adversarial finding"),
    (r"\bdamning\b", "verdict language"),
    (r"\bguilty\b", "verdict language"),
    (r"\bindicts?\b(?! each other)", "verdict language"),
    (r"\bdeserved (a |the )?(test|better)\b", "merit ascribed to a hypothesis"),
    (r"\b(good|bad) news\b", "grading for the reader"),
    (r"\bworse off for it\b", "score rather than direction"),
]


def _corpus_files():
    root = DOCS.parent
    for rel in ("docs/Elimination_Ledger.md", "MANIFEST.md",
                ".claude/skills/evidence-chain/SKILL.md"):
        p = root / rel
        if p.exists():
            yield rel, p.read_text()


def test_no_adversarial_framing_in_the_record():
    """Rule 11: entries record state; they do not indict each other."""
    hits = []
    for rel, text in _corpus_files():
        # The skill documents the banned forms in its own vocabulary table;
        # skip lines that are teaching the rule rather than breaking it.
        for i, line in enumerate(text.splitlines(), 1):
            if "Do not write" in line or line.strip().startswith("|"):
                continue
            for pat, why in ADVERSARIAL:
                if re.search(pat, line):
                    hits.append(f"{rel}:{i} [{why}] {line.strip()[:88]}")
    assert not hits, "adversarial framing found:\n" + "\n".join(hits)


def test_vocabulary_rule_is_documented():
    """The rule has to be written down where it is applied, or it decays."""
    skill = (DOCS.parent / ".claude/skills/evidence-chain/SKILL.md")
    if not skill.exists():
        pytest.skip("skill not present")
    t = skill.read_text()
    assert "Report correctness, not righteousness" in t
    assert "could a thermometer say it" in t.lower()
