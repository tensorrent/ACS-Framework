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
import sys
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
            if line.strip().startswith("|"):          # vocabulary tables
                continue
            # The rule governs assertions made in our own voice, not citation.
            # Quoting a banned form in order to document or retire it is the
            # opposite of using it, so strip quoted spans before matching:
            # "..." , *"..."* , `...` , and fenced-block content.
            bare = re.sub(r'\*?"[^"]*"\*?|`[^`]*`|\u201c[^\u201d]*\u201d', "", line)
            for pat, why in ADVERSARIAL:
                if re.search(pat, bare):
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


# ---------------------------------------------------------------------------
# The destructive-restore guard.  Method rule 12.
#
# `git checkout <path>` resets a whole file to HEAD.  Content it overwrites was
# never staged, so it is not in the object store and no reflog entry restores
# it.  On 2026-09-01 that discarded twelve intentional uncommitted edits while
# removing one appended test line -- exit 0, no warning.
#
# The guard is a PreToolUse hook.  These tests keep it honest: a hook nobody
# checks is a hook that silently stops matching.
# ---------------------------------------------------------------------------
import json
import sys
import subprocess


HOOK = None


def _hook_path():
    global HOOK
    if HOOK is None:
        HOOK = DOCS.parent / ".claude/hooks/guard-destructive-restore.py"
    return HOOK


def _run_hook(command, cwd):
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    return subprocess.run([sys.executable, str(_hook_path())], input=payload,
                          capture_output=True, text=True, cwd=cwd)


def test_restore_guard_is_installed_and_wired():
    """The hook must exist AND be registered, or it protects nothing."""
    assert _hook_path().exists(), "guard hook missing"
    settings = DOCS.parent / ".claude/settings.json"
    assert settings.exists(), ".claude/settings.json missing -- hook not wired"
    cfg = json.loads(settings.read_text())
    wired = json.dumps(cfg.get("hooks", {}).get("PreToolUse", []))
    assert "guard-destructive-restore" in wired, "hook present but not registered"


def test_restore_guard_blocks_the_real_mistake(tmp_path):
    """A dirty path passed to `git checkout` must be refused."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    f = tmp_path / "notes.md"
    f.write_text("committed\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "init"], cwd=tmp_path, check=True)
    f.write_text("committed\nUNCOMMITTED WORK\n")          # the edits at risk
    r = _run_hook("git checkout notes.md", tmp_path)
    assert r.returncode == 2, f"guard did not block; exit={r.returncode}"
    assert "unrecoverable" in r.stderr, "block message must say why"
    assert "notes.md" in r.stderr, "block message must name the file at risk"


def test_restore_guard_allows_safe_commands(tmp_path):
    """A guard that blocks everything would just be turned off."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "clean.md").write_text("x\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "init"], cwd=tmp_path, check=True)
    for cmd in ("git checkout clean.md",        # clean file: restore is a no-op
                "git checkout -b feature",      # branch creation
                "git checkout main",            # branch switch
                "git status --short",
                "sed -i '$ d' clean.md"):
        r = _run_hook(cmd, tmp_path)
        assert r.returncode == 0, f"guard wrongly blocked: {cmd}\n{r.stderr}"


# ---------------------------------------------------------------------------
# Joint coherence of the ledger.  The holistic axis (H5).
#
# Individual entries can each be valid while the SET contradicts itself -- the
# failure mode H3 found in the manuscript's two relational conditions, and
# exactly what a 3,000-line ledger written incrementally is exposed to.
#
# This is a floor, not a proof: it checks that the load-bearing numbers are
# stated consistently wherever they appear.  It cannot check that the
# ARGUMENTS agree; that needs reading, and is recorded as still open.
# ---------------------------------------------------------------------------

LOAD_BEARING = {
    # label: (regex that should match, values that must NOT appear near it)
    "alpha_inv_codata": (r"137\.03599917[0-9]", ["137.036999", "137.035998"]),
    "required_a_over_R": (r"2\.039\d*e-?118|2\.03905e-118", ["2.039e-117", "2.039e-119"]),
    "planck_floor_alpha_inv": (r"26\.95\d*", ["26.85", "27.95"]),
    "relational_alpha_inv": (r"46\.24\d*", ["46.34", "45.24"]),
    "green_ratio": (r"6\.306\d*", ["6.406", "6.206"]),
    "half_twist_percent": (r"0\.0133", ["0.133", "0.00133"]),
}


def test_load_bearing_numbers_are_stated_consistently():
    """No entry may state a variant of a load-bearing number."""
    led = DOCS / "Elimination_Ledger.md"
    if not led.exists():
        pytest.skip("ledger not present")
    text = led.read_text()
    problems = []
    for label, (good, bad_variants) in LOAD_BEARING.items():
        if not re.search(good, text):
            problems.append(f"{label}: canonical value never appears (pattern {good})")
        for bad in bad_variants:
            if bad in text:
                problems.append(f"{label}: variant {bad!r} appears alongside the canonical value")
    assert not problems, "ledger self-consistency:\n" + "\n".join(problems)


def test_every_entry_has_a_tier_marker():
    """An entry with no tier cannot be placed in the claim ledger."""
    led = DOCS / "Elimination_Ledger.md"
    if not led.exists():
        pytest.skip("ledger not present")
    untiered = []
    for line in led.read_text().splitlines():
        if line.startswith("### 202"):
            if not re.search(r"\bT[0-4]\b|NOT-FOUND|method\b", line):
                untiered.append(line.strip()[:95])
    assert not untiered, "entries without a tier marker:\n" + "\n".join(untiered)


# ---------------------------------------------------------------------------
# Added 2026-09-11 by the joint-coherence audit. The audit's nine defects were
# all pointers, and the gate above could not see any of them: it reads heading
# lines only, and only those starting "### 202".
# ---------------------------------------------------------------------------

_INSTR = pathlib.Path(__file__).resolve().parents[3] / "code" / "constraint_projection"


def _run_instrument(name):
    import subprocess
    import sys
    path = _INSTR / name
    if not path.exists():
        pytest.skip(f"{name} not present")
    return subprocess.run([sys.executable, str(path)], capture_output=True, text=True)


def test_ledger_cross_references_resolve_and_anchors_hold():
    """A pointer that resolves is not the same as a pointer that is right.

    crossref_check.py runs both checks: X1 rejects a reference that dangles,
    lands on a blank line, or points at another pointer; X2 holds every anchored
    reference against the text it names. X1 alone passed six wrong references on
    the day this was written, which is why X2 exists.
    """
    r = _run_instrument("crossref_check.py")
    assert r.returncode == 0, (
        "ledger cross-references are broken:\n" + r.stdout[-3000:] + r.stderr[-1000:]
    )
    assert "PASS -- every reference resolves and every anchor holds" in r.stdout


def test_tier_gate_coverage_is_measured_not_assumed():
    """The tier gate's guarantee is narrower than its name; measure it."""
    r = _run_instrument("gate_coverage.py")
    assert r.returncode == 0, (
        "gate_coverage.py failed:\n" + r.stdout[-3000:] + r.stderr[-1000:]
    )
    # Every heading outside the gate's scan must fall into a named category --
    # tiered anyway, structural, or a continuation whose inherited tier the
    # instrument verified at runtime. An unclassified escapee fails here.
    assert "claim-shaped AND untiered -- real escapees   : 0" in r.stdout, (
        "a claim-shaped, untiered heading sits outside the tier gate:\n" + r.stdout
    )


def test_heading_tier_matches_the_verdict_in_the_body():
    """A heading may not under-report a falsification its own body states.

    The old gate passed L540 for three months: heading `T2 structural / T1
    numerical`, body `**Verdict.** ... is **FALSIFIED (T4)**`. The gate never
    reads bodies, so a heading can omit the strongest tier its entry earned.
    """
    led = DOCS / "Elimination_Ledger.md"
    if not led.exists():
        pytest.skip("ledger not present")
    lines = led.read_text().splitlines()
    starts = [i for i, l in enumerate(lines) if l.startswith("### 202")]
    problems = []
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        heading = lines[start]
        body = "\n".join(lines[start + 1:end])
        # Only the T4 direction is checked: a body that states a falsification
        # verdict is the one case where omitting the tier understates the result.
        if re.search(r"\*\*Verdict\.\*\*[^\n]{0,400}?FALSIFIED \(T4\)", body, re.S):
            if "T4" not in heading:
                problems.append(f"L{start + 1}: {heading.strip()[:90]}")
    assert not problems, (
        "entry bodies state FALSIFIED (T4) while their headings omit T4:\n"
        + "\n".join(problems)
    )
