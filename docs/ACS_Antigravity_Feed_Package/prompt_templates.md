> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Antigravity Agent Prompt Templates

These templates are designed to be copied and pasted directly into your chat or task definitions when invoking an Antigravity agent to work on the ACS codebase.

---

## Template 1: Verify a New Mathematical Conjecture
Use this prompt when you want the agent to formulate and verify a new conjecture.

```markdown
Role: ACS Mathematical Analyst
Context: Load the ACS Framework skill from docs/ACS_FRAMEWORK_SKILL.md and review the parameter ledger in docs/ACS_Antigravity_Feed_Package/key_parameters_ledger.json.

Task:
Formulate a verification script for the following conjecture:
"[INSERT CONJECTURE HERE, e.g., the projection of the sl(4,R) connection onto the SU(2)_R gauge sector under a custom torsion scaling factor epsilon = 0.1]"

Instructions:
1. Adhere strictly to the Adversarial Compression Research Cycle.
2. Build a new test script under code/acs_codebase/extras/ named test_conjecture_*.py.
3. Compute the z-score or numerical error bound.
4. Run the script and capture output.
5. Record your results using the four-tier verification matrix:
   - If exact proof is obtained: Tier 2 (Proved in paper).
   - If numerical-only match: Tier 3 (Numerically verified).
   - If computation shows the claim is false: Tier 4 (Explicitly falsified).
6. Update docs/ACS_Antigravity_Feed_Package/key_parameters_ledger.json and docs/Elimination_Ledger.md if a falsification or new invariant is found.
7. Do not overclaim or promote Tier 3 results to Tier 2.
```

---

## Template 2: Run and Audit the Verification Suite
Use this prompt when you want the agent to perform a complete repository check.

```markdown
Role: ACS Verification Auditor
Context: Load the ACS Framework skill from docs/ACS_FRAMEWORK_SKILL.md.

Task:
Run the consolidated verification suite and standalone extras to audit the state of the repository.

Instructions:
1. Locate the virtual environment at `/Users/coo-koba42/dev/.venv/bin/python`.
2. Run the main pytest suite:
   pytest code/acs_codebase/ -v
3. Execute the key standalone scripts under code/acs_codebase/extras/:
   - barbero_immirzi_correct.py
   - koide_clebsch_gordan.py
   - higgs_mass_ratio.py
4. Execute the Hilbert-Pólya shuffle-knife verification scripts under code/hp_knife_suite/.
5. Generate a structured summary of the results:
   - Total tests run.
   - Any failures or margin deviations.
   - Confirm that all derived constants match the locked values in key_parameters_ledger.json.
```

---

## Template 3: Extend deterministic AI Stack constraints
Use this prompt when you want the agent to develop code using the constraint-attractor loop pattern.

```markdown
Role: Sovereign Stack Engineer
Context: Load the ACS framework skill and review the Paper D (AI Stack PDR) blueprint.

Task:
Implement a new deterministic constraint gate for the AI stack.

Instructions:
1. The new gate must operate strictly in exact integer arithmetic.
2. The gate must enforce a specific mathematical invariant (e.g., matching a trace-determinant EigenCharge triplet).
3. Draft the code in Python using only standard libraries (or numpy) with fixed random seeds (`20260423`).
4. Write a unit test verifying that any out-of-boundary inputs are immediately rejected and trigger information-balance corrections.
```
