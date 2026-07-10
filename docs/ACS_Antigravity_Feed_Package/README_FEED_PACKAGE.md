> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# ACS Antigravity Feed Package

This directory contains the structured artifacts and prompt templates designed to integrate the Asymmetric Codependent Systems (ACS) framework directly into Google's Antigravity agentic platform.

## Contents

1. **`key_parameters_ledger.json`**: Machine-readable JSON index of derived constants, locked parameters, proved theorems, explicitly falsified claims, and open research questions.
2. **`run_acs_verification.py`**: A master python wrapper that runs the entire verification suite (pytest assertions + standalone extras) and outputs a structured JSON compliance report.
3. **`prompt_templates.md`**: Contextual prompt templates optimized for Antigravity agents to research, verify, or extend the ACS framework.

## Usage in Antigravity

1. Upload the `ACS-Framework` repository or this `ACS_Antigravity_Feed_Package` folder into your Antigravity workspace.
2. Direct the agent to initialize the ACS context by pointing it to the master skill module:
   ```
   Load the ACS Framework skill from docs/ACS_FRAMEWORK_SKILL.md.
   ```
3. Use the JSON ledger (`key_parameters_ledger.json`) as the ground truth constraint set for any code generation or mathematical derivations.
4. Run `run_acs_verification.py` to verify that the local codebase is in a fully passing and compliant state.
