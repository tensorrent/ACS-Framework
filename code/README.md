# Code guide

[Repository home](../README.md) · [Papers](../papers/README.md) · [Documentation](../docs/README.md) · [Reproduction](../docs/REPRODUCTION.md)

## Checks run by publication CI

- [publication_20260924/verify_science.py](publication_20260924/verify_science.py): 58 scoped action, normalization, RG, exact-root, and carrier checks. Dependencies are pinned in [requirements.txt](publication_20260924/requirements.txt).
- [acs_codebase/tests/](acs_codebase/tests/): the 46-test canonical suite. Its [package guide](acs_codebase/README.md) describes the source organization.
- [../scripts/verify_publication.py](../scripts/verify_publication.py): evidence hashes and manuscript inventory, followed by the portable science checks.
- [../scripts/build_papers.py](../scripts/build_papers.py): all 35 canonical LaTeX manuscripts.
- [../scripts/check_navigation.py](../scripts/check_navigation.py): local navigation links and complete paper-catalog coverage.

These are the portable publication entry points. They do not rerun every archived PDE experiment or prove every claim in the historical corpus.

## Research instruments

- [condensate_energy/](condensate_energy/): the preserved action-to-carrier investigation. Start from the [evidence index](../docs/CONDENSATE_EVIDENCE.md) and [endpoint audit](../docs/condensate_energy/endpoint_audit/README.md) to identify the appropriate model, source snapshot, and receipt. Some archive-recovery scripts require the original local drive.
- [frontier_verification/](frontier_verification/README.md): pinned Python and Lean checks for the frontier deltas published on `main`.
- [hp_knife_suite/](hp_knife_suite/): prime/zero position, spacing, phase, and shuffle experiments. [Data and optional commands](../docs/REPRODUCTION.md#optional-research-suites).
- [notes_verification/](notes_verification/): companion-note checks, including the scaled-invariance test.
- [issue7/](issue7/): Section 9 cone-chain and four-thirds tests; see the [corresponding report](../docs/issue7_paper_section9_and_4over3.md).
- [framed_unknot/](framed_unknot/README.md): framing, SU(2) lift, and moment-ratio checks.
- [capacitance_ribbon/](capacitance_ribbon/): capacitance calculations; read the current carrier-boundary paper before interpreting a numerical match.
- [palpha_overlap/](palpha_overlap/): overlap and Gamow-channel calculations; [audit log](../docs/palpha_audit_log.md).
- [acs_codebase/extras/](acs_codebase/extras/README.md): heritage scripts with mixed status, distinct from the curated test suite.

## Supporting tools

[acs_memo.py](acs_memo.py) and [benchmark_efficiency.py](benchmark_efficiency.py) support memoization and efficiency measurements. [Training harnesses](../harness/training/README.md) and [visualizations](../visualizations/README.md) have their own guides.

The new navigation does not move or rename scientific code. Existing imports, paper citations, and archived hashes keep their original paths.
