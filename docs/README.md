# Documentation index

[Repository home](../README.md) · [Papers](../papers/README.md) · [Code](../code/README.md) · [Branches](BRANCHES.md)

## Current findings and checks

- [24 September 2026 publication](publication/2026-09-24/README.md): the current consolidated results, corrections, limits, and reproducibility scope.
- [Reproduction guide](REPRODUCTION.md): portable checks, manuscript builds, and optional research suites.
- [Publication amendments](publication/2026-09-24/amendments.json): a specific update for each of the 33 earlier manuscripts.
- [Publication manifest](publication/2026-09-24/publication-manifest.json): file hashes for the published papers and evidence.
- [Style and literature review](publication/2026-09-24/style-and-research.md): primary references and manuscript conventions.
- [Branch index](BRANCHES.md): work published on `main`, open research PRs, and unmerged branches.

## Explore by research question

### Actions, condensates, and particle identification

Start with the [action-identifiability paper](../papers/updates/ACS_Action_Identifiability.pdf) and [carrier-boundary paper](../papers/updates/ACS_Condensate_Carrier_Boundary.pdf), then follow their source receipts.

- [Endpoint audit](condensate_energy/endpoint_audit/README.md): consolidated disposition and remaining inputs.
- [Condensate evidence guide](CONDENSATE_EVIDENCE.md): every retained experiment's README, indexed without changing its archived bytes.
- [Original energy investigation](condensate_energy/README.md): the initial retention, entry, and escape experiments; this is the beginning of the sequence, not its endpoint.
- [Publication checks](../code/publication_20260924/verify_science.py): the portable subset rerun in CI.

### Primes, zeta zeros, topology, and observation

- [Frontier continuation index](frontier/README.md): dated deltas, corrections, and the current queue published on `main`.
- [11 September snapshot](frontier/2026-09-11/README.md): the imported 50-task investigation and original evidence archive.
- [12 September source and data audit](frontier/2026-09-12-source-delta/README.md): provenance, precision, and finite-sum implementation corrections.
- [Frontier verification guide](../code/frontier_verification/README.md): Python and Lean reproduction with explicit trust boundaries.
- [Unmerged frontier work](BRANCHES.md#open-research-prs): later experiments remain on their research branch until reviewed and integrated.

### Historical claims, falsifications, and editorial work

- [Claim-to-code manifest](../MANIFEST.md) and [glossary](../GLOSSARY.md): read with current publication amendments.
- [Elimination ledger](Elimination_Ledger.md): retained falsifications and counterexamples.
- [Technical whitepaper](ACS_Technical_Whitepaper.md): consolidated background with its current status notice.
- [Corpus map](ACS_Corpus_Map.md): historical claim map; its numerical/status summaries predate the latest audit.
- [May 2026 master index](ACS_Master_Index.md): historical page and line references, retained for old citations.
- [August editorial audit](Editorial_Audit_2026-08-07.md) and [bug-fix log](BUGFIX_LOG.md): earlier review records.
- [Paper A changes](PaperA_changelog.md), [Paper B changes](PaperB_changelog_extended.md), and [Paper C changes](PaperC_changelog.md).

## Other supporting material

- [Section 9 and four-thirds tests](issue7_paper_section9_and_4over3.md) and [Linux replication](issue7_linux_replication/README.md).
- [Alpha-decay overlap audit](palpha_audit_log.md) and [overlap artifacts](palpha_overlap/).
- [Torsion and condensation analysis](Torsion_Topological_Condensation_Analysis.md).
- [Yang–Mills comparison methodology PDF](ym_comparison_methodology_paper.pdf) and [LaTeX source](ym_comparison_methodology_paper.tex). This supporting document lives outside the 35-paper canonical publication inventory and its build job.
- [Historical verification guide](README_verification_suite.md), [efficiency report](EFFICIENCY_BENCHMARK_REPORT.md), and [historical cross-repository glossary](Cross_Repo_Glossary_Extract.md).

The publication's frozen evidence is preserved in place. New indexes point into it; they do not rewrite original receipts, failures, or source snapshots.
