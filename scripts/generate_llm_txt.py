#!/usr/bin/env python3
"""Generate deterministic llm.txt and llms.txt structured corpus files for AI/LLM ingestion.

Combines the canonical 35-paper catalog (papers/catalog.json), the audited T1-T4 claim and
elimination ledger (site/data/claims.json), the 5-phase research timeline (site/data/timeline.json),
the F-1..F-23 falsification register, the Q1..Q7 strip-mine results, the 8 structural invariables,
and the full machine-parseable JSON payload into:
  - llm.txt (repository root)
  - site/llm.txt (published at /llm.txt on GitHub Pages)
  - site/llms.txt (published at /llms.txt on GitHub Pages for standard llms.txt crawlers)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://tensorrent.github.io/ACS-Framework"
REPO_URL = "https://github.com/tensorrent/ACS-Framework"

INVARIABLES = [
    {
        "id": "INV-1",
        "name": "Net Transfer Entropy Primitive (ΔI)",
        "statement": "Any two mutually-constraining fields — Form (structural information) and Function (dynamic information) — generate net transfer entropy ΔI = T_{Y->X} - T_{X->Y}; its sign defines directional governance and ΔI = 0 defines the attractor."
    },
    {
        "id": "INV-2",
        "name": "BCH–TE Morphism",
        "statement": "The second-order Taylor coefficient of net transfer entropy ΔI(ε) under flow composition equals the Lie bracket [f, g]: ΔI(ε) = ε⟨f-g, ∇log(dμ/dν)⟩ + 2ε²⟨[f,g], ∇log(dμ/dν)⟩ + O(ε³) (Tier T2 finite-dim proof; T1 machine-verified)."
    },
    {
        "id": "INV-3",
        "name": "Form / Function Ontology",
        "statement": "Across substrates (gravity, Riemann zeros, condensates, attention), Form encodes marginal/structural constraints while Function encodes exact relational/positional dynamics."
    },
    {
        "id": "INV-4",
        "name": "Operator-Type Ladder",
        "statement": "bracket(Function, Function) -> Form; holonomy(bracket, Function) -> irreducible Form."
    },
    {
        "id": "INV-5",
        "name": "Inversion Arc",
        "statement": "A system that solves a constraint becomes the next constraint; role exchange f <-> g flips the sign of ΔI at 1st and 2nd order, and Killing orthogonality tr([X,Y]X) = 0 enforces algebraic non-traversability."
    },
    {
        "id": "INV-6",
        "name": "Tensegrity & Zero-Mode Gauge Freedom",
        "statement": "Rigidity-matrix zero modes correspond to gauge freedoms; in the 68-coordinate scalar action, 6 of 17 quartic directions vanish identically on the neutral slice."
    },
    {
        "id": "INV-7",
        "name": "Four-Tier Epistemic Discipline (T1-T4)",
        "statement": "Every claim is classified T1 (Machine-Verified), T2 (Proved in Paper), T3 (Numerically Verified), or T4 (Explicitly Falsified). Tiers never promote automatically; T4 falsifications are preserved permanently in the append-only Elimination Ledger."
    },
    {
        "id": "INV-8",
        "name": "Local Validity vs Global Overreach",
        "statement": "Each operator lens is valid within its explicit domain boundary and fails when universalized without checking representation or normalization invariance (REFRACTION vs INVARIANT)."
    }
]

FALSIFICATIONS_REGISTER = [
    {"id": "F-1", "claim": "ad^3 = 2*ad for integer eigenvalues", "mechanism": "Requires eigenvalue lambda = 1/sqrt(2); actual sl(4,R) B-L generator satisfies ad^3 = (16/9)*ad."},
    {"id": "F-2", "claim": "Universal 2pi holonomy inversion across all ACS domains", "mechanism": "sl(4,R) adjoint spectrum {0(x9), +-4/3(x3)} is real/hyperbolic, so ||exp(2pi ad)|| approx e^{8pi/3} approx 4348.5 != 1. 2pi spinor closure is representation-specific to SU(2)."},
    {"id": "F-3", "claim": "Wronskian W[f,g] = f'g - g'f is a canonical Poisson bracket", "mechanism": "Fails the Leibniz rule by an exact remainder: W[fg,h] - (fW[g,h] + gW[f,h]) = -fgh', refuting the early plasma-Hamiltonian reading."},
    {"id": "F-4", "claim": "IR Pythagorean lattice imprint on PDG particle masses (N1)", "mechanism": "Monte Carlo z-scores z in [-0.7, +0.3] vs PDG masses — clean statistical null."},
    {"id": "F-5", "claim": "Intrinsic algebraic chirality without physical unitarity input", "mechanism": "Chirality bias vanishes under covariant conjugation; unitarity enters via complexification J(T) = i*sym(T) + anti(T)."},
    {"id": "F-6", "claim": "Killing form alone selects Lorentzian (3,1) signature / EM as torsion annihilator", "mechanism": "Cartan involution != parity involution; torsion sector Sym_0(4) has centralizer {0} in sl(4,R)."},
    {"id": "F-7", "claim": "Holonomy stability selects spacetime signature (Route C)", "mechanism": "All signatures produce equal holonomy norms under the tested functional."},
    {"id": "F-8", "claim": "Bi-doublet quartic coupling alpha_2 is an optional free parameter", "mechanism": "Forbidden by representation theory: Phi ~ (1,2,2) is an SU(4) singlet so T^A Phi = 0 => alpha_2 = 0 identically."},
    {"id": "F-9", "claim": "Tree-level beta_c explains fermion mass hierarchy", "mechanism": "Tree-level equal-VEV no-go forces tan(beta) = +-1 and degenerate up/down mass matrices."},
    {"id": "F-10", "claim": "Tree-level Yukawa rescue of tan(beta)", "mechanism": "Identity M_u - M_d = (h - h_tilde)(kappa_1 - kappa_2) forces M_u = M_d and |V_CKM| = I at equal VEVs."},
    {"id": "F-11", "claim": "Coleman-Weinberg 1-loop 6->5 parameter reduction fixing tan(beta)", "mechanism": "Fermion-dominated 1-loop potential drives minimum to boundary; tan(beta) remains a gauge-protected flat direction in the 6-input Branch A ledger."},
    {"id": "F-12", "claim": "115-dimensional exceptional subalgebra closure", "mechanism": "Proper Lie bracket saturation shows the generated algebra is all of gl(12) (dim 144)."},
    {"id": "F-13", "claim": "N3 uniform-X prime-gap transition conjecture", "mechanism": "Falsified numerically in the tested prime-gap range."},
    {"id": "F-14", "claim": "Assembly order selects distinct packing outcomes ('acid-to-water')", "mechanism": "Greedy packing jams near ~5.5 regardless of assembly order."},
    {"id": "F-15", "claim": "Order-asymmetry acts as a stable signed lever at large N", "mechanism": "Sign oscillates and amplitude decays with N."},
    {"id": "F-16", "claim": "Shell-commensuration of asymmetry at centered-hexagonal numbers", "mechanism": "Zero crossings do not align with centered-hexagonal numbers."},
    {"id": "F-17", "claim": "Sound and light are two octaves of one electromagnetic medium", "mechanism": "4/4 pre-registered scaling tests fail."},
    {"id": "F-18", "claim": "Particle/wave duality is infinite Mandelbrot self-similarity", "mechanism": "Generative models exhibit a characteristic cutoff scale."},
    {"id": "F-19", "claim": "Central-number residual equals the Higgs quartic residual ('same gap')", "mechanism": "Confuses angle-independent charge cancellation with scale-dependent coupling magnitude."},
    {"id": "F-20", "claim": "Higgs quartic residual is a UV Planck-scale boundary condition", "mechanism": "SM RG running of lambda crosses lambda_ACS = 2*sqrt(3)/27 once near the electroweak scale (~130-180 GeV) and runs down."},
    {"id": "F-21", "claim": "Hilbert-Polya operator H built from balanced symmetrized duality involution", "mechanism": "Balanced involutions force beta = 1 (GOE) and break GUE level repulsion (beta = 2)."},
    {"id": "F-22", "claim": "Hilbert-Polya operator via arithmetic diagonal perturbation of GUE", "mechanism": "Cosmetic when weak, destroys GUE spacing when strong; no intermediate selection regime exists."},
    {"id": "F-23", "claim": "Lag-1 spacing autocorrelation is a beyond-GUE arithmetic invariant", "mechanism": "Observed 0.050 gap sits inside the 0.08 finite-sample apparatus band; vanishes under bare permuted spacings."}
]

OPEN_PROBLEMS = [
    {"id": "O-1", "title": "Arithmetic realization of the Hilbert-Polya operator in the pinned chiral class", "status": "Symmetry class pinned (anti-commuting antiunitary C H* C^-1 = -H, C^2 = -1, beta = codim - 1 = 2); explicit arithmetic operator construction remains open."},
    {"id": "O-2", "title": "FeynRules / UFO collider model export for the 68-coordinate scalar & Pati-Salam sector", "status": "Open engineering & phenomenology export."},
    {"id": "O-3", "title": "First-principles action principle for the dual gravitational functional S_tilde_g", "status": "Open continuum variational problem."},
    {"id": "O-4", "title": "High-degree L-function zero-height floor verification (d > 1, q > 1)", "status": "d=1 value 2*pi*e survives; (2*pi*e)^d/q falsified at d=2 by Dedekind zeta_Q(i); full LMFDB sweep open."},
    {"id": "O-5", "title": "Complete Standard Model fermion & gauge embedding from the GL(4,R) frame bundle", "status": "Condensate carrier boundary (24 Sept 2026) separates classical scalar binding from full SM quantum numbers."},
    {"id": "O-6", "title": "Full bulk-boundary ER=EPR holographic dictionary from Killing orthogonality", "status": "Algebraic non-traversability tr([X,Y]X) = 0 proved (T2); dynamical bulk geometry remains open."},
    {"id": "O-7", "title": "Global singlet projection for the Barbero-Immirzi parameter (0.274067 vs 0.2375)", "status": "Local representation swap refracts gamma_BI (Q1); global projection open."},
    {"id": "O-8", "title": "Right-handed neutrino X-ray bound tension", "status": "Resolved via decoupling (M_WR >= 16 TeV, v_R >= 49 TeV), which kills the keV sterile-neutrino dark-matter reading."}
]


def build_llm_text() -> str:
    catalog = json.loads((ROOT / "papers" / "catalog.json").read_text())["papers"]
    claims_doc = json.loads((ROOT / "site" / "data" / "claims.json").read_text())
    timeline = json.loads((ROOT / "site" / "data" / "timeline.json").read_text())["events"]

    lines = [
        "# ACS Framework (Asymptotic Compatibility Synthesis / Asymmetric Codependent Systems)",
        "",
        "> Self-contained structured reference (`llm.txt` / `llms.txt`) for AI systems, LLM agents, and automated scientific auditors.",
        "> Author: Bradley Wallace (Independent Researcher, TensoRrent)",
        f"> Live Documentary Site: {SITE_URL}/",
        f"> Canonical GitHub Repository: {REPO_URL}",
        "> Release Anchor: 24 September 2026 Consolidated Publication + 30 October 2026 Documentary & Provenance Release",
        "> License: Sovereign Integrity Protocol (SIP) License v1.1 (Free for personal, academic, and verification use; commercial/revenue use requires a prior written license)",
        "",
        "---",
        "",
        "## 1. Machine-Readable Endpoints & Structured Data Files",
        "",
        f"- **Full LLM Structured Corpus (`llm.txt`)**: `{SITE_URL}/llm.txt` (mirror: `{SITE_URL}/llms.txt`)",
        f"- **Canonical 35-Paper Catalog (`catalog.json`)**: `{SITE_URL}/data/catalog.json`",
        f"- **Audited T1–T4 Claim & Elimination Ledger (`claims.json`)**: `{SITE_URL}/data/claims.json`",
        f"- **Program Chronology & Verification Timeline (`timeline.json`)**: `{SITE_URL}/data/timeline.json`",
        f"- **Deterministic Scene Asset SHA-256 Manifest (`manifest.json`)**: `{SITE_URL}/assets/manifest.json`",
        f"- **Offline Build & Link Integrity Report (`build-report.json`)**: `{SITE_URL}/build-report.json`",
        f"- **Interactive Möbius Screw Framing Simulator**: `{SITE_URL}/visualizations/mobius_screw_framing_transformer.html`",
        f"- **Interactive q-Plane Confinement Simulator**: `{SITE_URL}/visualizations/acs_q_plane_confinement_simulator.html`",
        "",
        "---",
        "",
        "## 2. Executive Summary & Epistemic Governance Rules for AI Systems",
        "",
        "The ACS Framework investigates how two mutually-constraining fields — **Form** (structural information) and **Function** (dynamic information) — generate net transfer entropy `ΔI`, whose second-order Taylor coefficient under flow composition is the Lie bracket `[f, g]` (**the BCH–TE morphism**). Applied to the Palatini frame-connection pair `(e, ω)`, the bracket image spans `sl(4,R)` (dim 15 = 9 torsion + 6 Lorentz), inside which `sl(3,R)` (5 torsion + 3 Lorentz) emerges as a numerical closure attractor (Tier T3). Applied to prime distributions and Riemann zeta zeros via the Weil–Guinand explicit formula, it separates marginal spacing statistics (`FORM`) from exact level-position arithmetic (`FUNCTION`).",
        "",
        "### Non-Negotiable Citation & Reasoning Rules for AI Agents",
        "",
        "1. **Always State the Verification Tier (`T1`, `T2`, `T3`, `T4`)**:",
        "   - **T1 (Machine-Verified)**: Automated deterministic test passes in the repository verification suite (seed `20260423`).",
        "   - **T2 (Proved in Paper)**: Complete analytical derivation or mathematical proof in the canonical `.tex` manuscript.",
        "   - **T3 (Numerically Verified)**: Consistent across seeded numerical ensembles/sweeps, **not** an unconditional analytical theorem.",
        "   - **T4 (Explicitly Falsified)**: Refuted by symbolic proof, counterexample, or numerical kill test. Recorded permanently in the append-only Elimination Ledger.",
        "   - **Rule**: Tiers never promote automatically. Never present a `T3` numerical observation as a `T2` theorem.",
        "2. **Explicit Non-Claims (Never Overclaim)**:",
        "   - **Riemann Hypothesis**: The ACS Framework **does not prove the Riemann Hypothesis** and **constructs no Hilbert–Pólya operator**. Paper B proves `RH => stationarity` (T2), while the converse depends on a minimum-gap bound checked only to `N = 200`.",
        "   - **`sl(3,R)` Selection**: The selection of `sl(3,R)` inside `sl(4,R)` (`D(sl(3,R)) = 1.4e-16` vs `>= 0.49` across 50,000 random `Gr(8,15)` subspaces) is **T3 numerical**, not an analytical uniqueness proof. Pure rank-2 signature selection (`N2`) has an explicit counterexample in the exceptional Lie algebra `G_2` (dim 14).",
        "   - **24 September 2026 Consolidations & Withdrawals**:",
        "     - The complete scalar action has **68 real coordinates** and **17 quartics**, of which **6 vanish on the neutral slice** (`ACS_Action_Identifiability.pdf`, T1). Physical masses require the kinetic metric.",
        "     - Classical condensate binding is strictly separated from physical Standard Model particle identification (`ACS_Condensate_Carrier_Boundary.pdf`, T1). Earlier inferences equating self-linking `|Sl| = 2` with the electron `g = 2` factor, singlet color confinement from classical framing alone, and propagating algebraic Palatini torsion are **withdrawn / falsified (T4)**.",
        "   - **Five Mandatory Caveats**:",
        "     1. *Coleman–Mandula*: The `(3,1)` grading is an **internal** algebra grading, not spacetime signature; bridging to Lorentzian geometry requires soldering/pre-geometry.",
        "     2. *Exceptional Algebra Boundary*: Grading selection (`N2`) fails for `G_2`.",
        "     3. *Barbero–Immirzi Refraction*: `γ_BI = 0.274067` (`SU(2)`) refracts to `0.190206` (`SO(3)`) under instrument swap (`Q1`) and sits above the Domagala–Lewandowski value `0.2375`.",
        "     4. *Neutrino Decoupling*: Clearing the X-ray bound requires `M_WR >= 16 TeV` (`v_R >= 49 TeV`), which **kills the keV sterile-neutrino dark-matter reading** (`Q7`).",
        "     5. *`tan β` Gauge Protection*: `tan β` is a gauge-protected flat direction at tree level, and 1-loop Coleman–Weinberg `6 -> 5` parameter reduction fails (`T4`, `F-11`).",
        "",
        "---",
        "",
        "## 3. Eight Structural Invariables (`INV-1` … `INV-8`)",
        "",
    ]

    for inv in INVARIABLES:
        lines.append(f"- **{inv['id']} ({inv['name']})**: {inv['statement']}")

    lines += [
        "",
        "---",
        "",
        "## 4. Audited T1–T4 Claim & Elimination Ledger (20 Core Entries)",
        "",
    ]

    for c in claims_doc["claims"]:
        lines += [
            f"### [{c['id']}] {c['claim']}",
            f"- **Tier**: `{c['tier']}` ({c['axis']}) | **Domain**: {c['domain']}",
            f"- **Metric / Identity**: `{c['metric']}`",
            f"- **Scope & Boundary**: {c['scope']}",
            f"- **Verification Script**: `{c['script']}`",
            f"- **Canonical PDF**: `{SITE_URL}/{c['pdf']}`",
            f"- **LaTeX Source**: `{SITE_URL}/{c['tex']}`",
            "",
        ]

    lines += [
        "---",
        "",
        "## 5. Complete Falsification Register (`F-1` … `F-23`) & Open Problems (`O-1` … `O-8`)",
        "",
        "### Falsified Conjectures (`F-1` … `F-23`, Tier T4)",
        "",
    ]

    for f in FALSIFICATIONS_REGISTER:
        lines.append(f"- **{f['id']} — {f['claim']}**: {f['mechanism']}")

    lines += [
        "",
        "### Open Problems (`O-1` … `O-8`)",
        "",
    ]

    for op in OPEN_PROBLEMS:
        lines.append(f"- **{op['id']} — {op['title']}**: {op['status']}")

    lines += [
        "",
        "---",
        "",
        "## 6. Complete 35-Manuscript Canonical Catalog",
        "",
    ]

    for idx, p in enumerate(catalog, start=1):
        lines += [
            f"{idx}. **{p['label']}** (`{p['group']}`)",
            f"   - Summary: {p['summary']}",
            f"   - PDF: `{SITE_URL}/{p['pdf']}`",
            f"   - LaTeX: `{SITE_URL}/{p['source']}`",
        ]

    lines += [
        "",
        "---",
        "",
        "## 7. Chronological Research & Verification Timeline",
        "",
    ]

    for ev in timeline:
        lines += [
            f"- **{ev['date']} · {ev['phase']} — {ev['title']}**",
            f"  - Detail: {ev['detail']}",
            f"  - Primary PDF: `{SITE_URL}/{ev['pdf']}` | LaTeX: `{SITE_URL}/{ev['tex']}`",
        ]

    lines += [
        "",
        "---",
        "",
        "## 8. Author Provenance & Analog Mixture-of-Experts (Analog MoE) Disclosure",
        "",
        "- **Sole Human Author**: Bradley Wallace (Independent Researcher, TensoRrent), 5,000–6,000 hours of solo theoretical and computational research.",
        "- **Accessibility & Neurodiversity Context**: Developed using a voice-directed cognitive-accessibility workflow accommodating dyslexia, ADHD, and dysgraphia/writing constraints.",
        "- **Analog Mixture-of-Experts (Analog MoE) Workflow**: Frontier language models and symbolic/numerical compute harnesses are used strictly as an assistive transcription and adversarial falsification layer. Every candidate claim is subjected to deterministic scripts and strip-mine kill tests (`Q1`–`Q7`, `F-1`–`F-23`); refuted claims are preserved permanently in the Tier T4 Elimination Ledger.",
        "",
        "---",
        "",
        "## 9. Machine-Parseable Consolidated JSON Payload",
        "",
        "```json",
    ]

    consolidated_payload = {
        "schema_version": 1,
        "framework": "Asymptotic Compatibility Synthesis (ACS) Framework",
        "author": {
            "name": "Bradley Wallace",
            "organization": "TensoRrent",
            "role": "Independent Researcher",
            "methodology": "Voice-directed Analog Mixture-of-Experts (Analog MoE) adversarial verification workflow"
        },
        "urls": {
            "site": f"{SITE_URL}/",
            "repository": REPO_URL,
            "llm_txt": f"{SITE_URL}/llm.txt",
            "llms_txt": f"{SITE_URL}/llms.txt",
            "catalog_json": f"{SITE_URL}/data/catalog.json",
            "claims_json": f"{SITE_URL}/data/claims.json",
            "timeline_json": f"{SITE_URL}/data/timeline.json",
            "assets_manifest_json": f"{SITE_URL}/assets/manifest.json"
        },
        "verification_metrics": {
            "canonical_manuscripts": len(catalog),
            "publication_science_checks": 58,
            "canonical_pytest_modules": 46,
            "verified_receipt_hashes": 516,
            "canonical_seed": 20260423,
            "pdg_v_gev": 246.22,
            "odlyzko_zeros_tested": 100000
        },
        "non_claims": [
            "Does NOT prove the Riemann Hypothesis.",
            "Constructs NO self-adjoint Hilbert-Polya operator.",
            "sl(3,R) inside sl(4,R) closure selection is Tier T3 numerical (50,000 Grassmannian samples), NOT an analytical uniqueness proof.",
            "Framing self-linking |Sl|=2 does NOT generate electron g=2 (falsified Tier T4; uniform closed loops yield g=1 identically).",
            "Transfer-entropy asymmetry Delta I is NOT identical to the Zamolodchikov / Casini-Huerta RG c-function (falsified Tier T4, Q4).",
            "Degree-d height floor formula (2*pi*e)^d/q is falsified at d=2 by 51 actual zeros of Dedekind zeta_Q(i) (Tier T4, Q3)."
        ],
        "invariables": INVARIABLES,
        "tiers": claims_doc["tiers"],
        "claims": claims_doc["claims"],
        "falsifications_f1_f23": FALSIFICATIONS_REGISTER,
        "open_problems": OPEN_PROBLEMS,
        "timeline": timeline,
        "papers_catalog": catalog
    }

    lines.append(json.dumps(consolidated_payload, indent=2, ensure_ascii=False))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main():
    content = build_llm_text()
    targets = (
        ROOT / "llm.txt",
        ROOT / "llms.txt",
        ROOT / "site" / "llm.txt",
        ROOT / "site" / "llms.txt",
    )
    for target in targets:
        target.write_text(content, encoding="utf-8")
        print(f"Wrote {target.relative_to(ROOT)} ({len(content.splitlines())} lines, {len(content.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
