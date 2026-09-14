# Prior art for the method itself

**STATUS: in progress** (wave-2 specialist, 2026-09-11)

## Scope

Target: `.claude/skills/evidence-chain/SKILL.md` (made canon 2026-08-31) — four links
(claim -> instrument -> observation -> provenance), three honest options, twelve rules —
plus the T0–T4 tier ladder and the corpus's own negative benchmark result about the skill.

Question asked of each rule, and only this question: **has this been said before, by whom,
and where?**

Verdict vocabulary:

- **IDENTICAL** — prior art states the same operational rule, for the same reason.
- **NARROWER** — prior art states a special case of our rule, or states it for a narrower domain.
- **BROADER** — prior art states a more general principle of which our rule is an instance.
- **GENUINELY-NOT-FOUND** — searched, recorded what was searched, and did not find it.

Per the brief: a GENUINELY-NOT-FOUND row is only admissible with its search record attached.
Every citation below was fetched this session unless the row says otherwise; a citation not
opened is an assumption (rule 10) and is marked as such.

Rules 9 and 10 are **already settled** in `docs/Elimination_Ledger.md` L3690-3699 (Richard
Schwartz, arXiv:2308.12641) and are carried forward here, not re-derived.

## The table

| # | Our statement | Closest prior art | Verdict |
|---|---|---|---|
| 6 | "Entries record state; they do not indict each other." | Lunney & Lueder, "Postmortem Culture: Learning from Failure", ch. 15 of *Site Reliability Engineering: How Google Runs Production Systems* (O'Reilly, 2016/2017): a postmortem "must focus on identifying the contributing causes of the incident **without indicting** any individual or team"; it "assumes that everyone involved in an incident had good intentions and did the right thing with the information they had." Antecedent: J. Reason, *Managing the Risks of Organizational Accidents* (Ashgate, 1997) — Just Culture; popularised for software by J. Allspaw, "Blameless PostMortems and a Just Culture", Etsy Code as Craft, 2012-05-22. | **IDENTICAL** — the prior art uses the same verb ("indict") for the same prohibition. |
| 7 | "Derive the printed conclusion from the computed result, never alongside it." | R. Gentleman & D. Temple Lang, "Statistical Analyses and Reproducible Research", *J. Computational and Graphical Statistics* 16(1):1–23, 2007 (Bioconductor Working Paper 2, 2004, https://biostats.bepress.com/bioconductor/paper2) — the *compendium* / dynamic document, in which "contents, including figures, tables, etc., can be recalculated each time a view of the document is generated", so narrative numbers are regenerated from code rather than transcribed. Ancestor: D. E. Knuth, "Literate Programming", *The Computer Journal* 27(2):97–111, 1984. | **NARROWER (them) / BROADER (us)** — their mechanism is document regeneration; our rule states the same anti-drift principle and also applies it *inside an instrument's own print statements* (interpolate the computed variable into the conclusion string), which the compendium literature does not address. |
| 2 | "Anchor every series to a number someone else published. Inverting your own series with your own inputs proves only self-consistency." | JCGM 200 (VIM3), def. **2.41 metrological traceability**, fetched from https://jcgm.bipm.org/vim/en/2.41.html: "property of a measurement result whereby the result can be related to a **reference** through a documented **unbroken chain of calibrations**, each contributing to the measurement uncertainty." The reference is external by construction — a realization of a unit or a measurement standard, never the instrument's own output. Software-side analogue: ASME V&V 10 / P. J. Roache, *Verification and Validation in Computational Science and Engineering* (Hermosa, 1998) — *verification* (self-consistency: are the equations solved right) is explicitly not *validation* (against external data). | **IDENTICAL** — our "self-consistency is not evidence" is the verification/validation distinction, and our "someone else's number" is the traceable reference. Metrology states it with more machinery (uncertainty propagation along the chain) than we do. |
| 3 | "An instrument is not trusted until it has been shown capable of failing. Validate against a known answer *before* using it. A test that cannot reject is not evidence." | Two independent precursors. (a) **Positive controls** in experimental science: a sample known to produce a positive result, run to "confirm that the experiment is capable of producing results under the experimental conditions" — standard assay-validity practice (e.g. ELISA protocol controls; if the positive-control signal is absent "the assay is not valid"). (b) **Mutation testing**: R. A. DeMillo, R. J. Lipton, F. G. Sayward, "Hints on Test Data Selection: Help for the Practicing Programmer", *Computer* 11(4):34–41, IEEE, April 1978 — seed a known defect and require the suite to kill it; a suite that cannot kill mutants is not evidence of correctness. (DOI 10.1109/C-M.1978.218136; cited from secondary sources, the primary PDF was paywalled/403 this session — see search record.) | **IDENTICAL** — this rule is the positive control, restated for computational instruments. It is also the operating premise of mutation testing. Nothing here is ours. |
| 4 | "No result is logged as novel until a literature search has been run and recorded. Judgement is not a search." | PRISMA 2020: M. J. Page et al., "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews", *BMJ* 2021;372:n71 (PMC8007028) — and its search extension **PRISMA-S** (Rethlefsen et al., *Systematic Reviews* 2021;10:39), which requires "full search strategies for at least one database, exactly as run". The *recorded-search* requirement — not merely that you searched, but that the search itself is an artifact — is exactly our rule. Prior-art search in patent examination (35 U.S.C. §102/§103 novelty) is the same device for the same purpose: novelty is not asserted, it is searched for and the search is filed. | **NARROWER (them, in scope) / IDENTICAL (in form)** — PRISMA governs the whole review; we apply the identical requirement to a single logged claim. The *recording* requirement is theirs, not ours. |
| 8 | "Run it to exhaustion; leave nothing outside. Any sentence conceding a limitation must be a computed result, an explicitly recorded open item, or removed." | R. P. Feynman, "Cargo Cult Science", Caltech commencement address, June 1974 (printed in *Engineering and Science* 37(7), 1974; text fetched from https://calteches.library.caltech.edu/51/2/CargoCult.htm): "If you're doing an experiment, you should report everything that you think might make it invalid—not only what you think is right about it: other causes that could possibly explain your results; and things you thought of that you've eliminated by some other experiment, and how they worked—to make sure the other fellow can tell they have been eliminated. **Details that could throw doubt on your interpretation must be given, if you know them.**" | **IDENTICAL in substance, BROADER in Feynman** — he requires disclosure of every doubt-throwing detail; we add the operational trichotomy (computed / recorded open item / removed) that tells you what to *do* with each one. The trichotomy appears to be ours; the obligation is not. |
| 12 | "A restore that discards unstaged work is unrecoverable — guard it, don't remember it." (enforced by a PreToolUse hook, not by recall) | **Poka-yoke** (mistake-proofing), Shigeo Shingo, Toyota Production System — Shingo's premise is that people will inadvertently forget, so the safeguard is built into the process rather than into the operator's care, and responsibility for error lies in system design rather than in the person. Interaction-design restatement: D. A. Norman, *The Design of Everyday Things* (Basic Books, 1988/2013) — **forcing functions** (interlock / lock-in / lock-out) and behaviour-shaping constraints. Domain-specific corroboration: Git itself split the overloaded `git checkout` into `git switch` / `git restore` in v2.23 (2019) for this exact hazard. | **IDENTICAL** — "guard it, don't remember it" is a one-line statement of poka-yoke. The *content* (what `git checkout <path>` destroys, and why the reflog does not help) is repo-specific and is not a general claim. |
<!-- TABLE-END -->

## Findings

<!-- appended per finding -->

## Search record

<!-- appended per search -->
