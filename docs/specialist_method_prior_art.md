# Prior art for the method itself

**STATUS: complete** (wave-2 specialist; table opened 2026-09-11, finished 2026-09-14 after a
session rate-limit interruption)

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
| 1 | "Evaluate the object the target actually defines — not the object it claims that object equals. Solve it symbolically with the substitutions left out and see what is really there." | A. W. Kimball, "Errors of the Third Kind in Statistical Consulting", *J. American Statistical Association* 52(278):133–142, 1957 — the **error of the third kind**, "the error committed by giving the right answer to the wrong problem" (p. 134); Kimball's examples are of an analysis whose stated target and its actual target have quietly diverged. Generalised by I. I. Mitroff & T. R. Featheringham, "On Systemic Problem Solving and the Error of the Third Kind", *Behavioral Science* 19(6):383–393, 1974 — "solving the wrong problem when [one] should have solved the right problem", or "selecting incorrect problem representation when correct representation should be chosen" (p. 383). Modern domain-specific restatement: **ICH E9(R1)**, *Addendum on Estimands and Sensitivity Analyses in Clinical Trials* (adopted 2019) — an **estimand** "defines the target of estimation" through five attributes and must be written down *before* the analysis, precisely because analyses routinely estimate a quantity other than the one the question names. (Kimball, Mitroff–Featheringham and ICH E9(R1) are cited here from the secondary sources fetched this session — the Wikipedia *Type III error* article and the ICH-addendum summaries — not from the primary texts; see search record.) | **BROADER (them) / NARROWER (us)** — Kimball and Mitroff–Featheringham name the general failure (answering a question other than the one posed). Our rule is one operational counter-move for one instance of it: when a document asserts `A = B`, evaluate `A` as defined rather than `B` as asserted. The estimand framework is the same counter-move fixed to a different domain. The technique half — "solve it symbolically with the substitutions left out" — is standard computer-algebra and physics practice; no canonical citation for it was found this session (see search record). |
| 5 | "Search your own corpus before the literature. The sharpest finding is often already in your own files, dated earlier, in those words." | D. R. Swanson, "Undiscovered Public Knowledge", *The Library Quarterly* 56(2):103–118, 1986 (DOI 10.1086/601720): knowledge "can be public, yet undiscovered, if independently created fragments are logically related but never retrieved, brought together, and interpreted"; the "essential incompleteness of search and retrieval therefore makes possible, and plausible, the existence of undiscovered public knowledge." Demonstrated the same year in Swanson, "Fish Oil, Raynaud's Syndrome, and Undiscovered Public Knowledge", *Perspectives in Biology and Medicine* 30(1):7–18, 1986, and mechanised as the ARROWSMITH system. Organisational form of the same failure: J. P. Walsh & G. R. Ungson, "Organizational Memory", *Academy of Management Review* 16(1):57–91, 1991 (DOI 10.5465/amr.1991.4278992) — retention is not the hard part; **retrieval** is, and stored knowledge that is not retrieved is not knowledge the organisation has. | **BROADER (them) / NARROWER (us)** — Swanson's non-interacting fragments sit in the public literature; ours sit in the same authors' own repository, which makes retrieval strictly cheaper. The claim that unretrieved records behave exactly like records that do not exist is Swanson's and Walsh & Ungson's. What our rule adds is only an ordering — own corpus *first*, literature second — which is a cost argument, not a new principle. |
| 11 | "Report correctness, not righteousness." Write **matches / does not match**, **reproduces / does not reproduce**, **holds / does not hold**. Test: *could a thermometer say it?* | Three independent precursors. (a) **E-Prime** — D. D. Bourland Jr., "A Linguistic Note: Writing in E-Prime", *General Semantics Bulletin* 1965, extending A. Korzybski's general semantics (*Science and Sanity*, 1933). Dropping the copula targets exactly the "is of identity" and "is of predication"; Kellogg & Bourland call their misuse a "deity mode of speech", which lets "even the most ignorant … transform their opinions magically into god-like pronouncements on the nature of things." (b) **The GAGAS finding structure** — GAO, *Government Auditing Standards* ("Yellow Book"), 2018 revision / 2021 technical update (GAO-21-368G): a finding is developed and reported as **criteria / condition / cause / effect**, where criteria is "what is required, desired, or achievable" and condition is "the situation that exists; the extent to which the criteria are met". The report states the measured gap between the two; it does not render a verdict on the audited party. (c) **Nonviolent Communication** — M. B. Rosenberg, *Nonviolent Communication: A Language of Life* (PuddleDancer, 1999/2003) — the first component is observation *separated from* evaluation. (GAGAS element definitions taken from the secondary GAO-derived sources fetched this session, not the Yellow Book PDF; Rosenberg cited from memory and not opened this session — an assumption under rule 10.) | **IDENTICAL in substance** — "could a thermometer say it?" is the E-Prime test, and the criteria-vs-condition form of an audit finding is the same move applied to a document under review. Note the asymmetry: rule 6 forbids indicting *people* (Just Culture, already tabled); rule 11 forbids indicting *documents*, which the postmortem literature does not cover. That extension may be ours, but it is a scope extension of an existing rule, not a new one. The etymological argument (*right* ← *righteous*) and the specific substitution table are repo-local vocabulary, not a general claim. |
<!-- TABLE-END -->

**Tally over the ten rules tabled here** (9 and 10 are settled elsewhere and not re-derived):
**IDENTICAL 6** (2, 3, 6, 8, 11, 12) · **NARROWER/IDENTICAL 1** (4) · **NARROWER-us/BROADER-them 3**
(1, 5, 7). **Zero rules came back without prior art.** Every operational rule in
`.claude/skills/evidence-chain/SKILL.md` has been stated before, usually decades earlier, usually
by someone outside software. What is not found in the prior art is small and specific, and is
listed under GENUINELY-NOT-FOUND in the search record: the deferred-substitution *technique* as a
stated rule, the phrase "tiers never promote", and the etymological argument in rule 11. The
file's value is therefore what its own closing section already claims — a written record of a
method so it need not be rediscovered — and not novelty.

## Findings

### Finding 1 — "Tiers never promote": prior art exists, is older, and is more explicit than ours was

**The object, as this corpus currently defines it.** Per `docs/Elimination_Ledger.md` L11–L12
(stated 2026-09-11 by the joint-coherence audit), T1 and T2 are **path markers**, not a strength
ordering. L12 cross-references the engine kill-criterion paragraph at L28–L32, quoted verbatim:
the criterion "can be applied two ways: **(a)** numerically, by recomputing under an instrument
swap (→ T1), or **(b)** structurally, by arguing from the quantity's construction when no
recomputable pipeline is reachable (→ T2). Tier honestly; never let (b) wear (a)'s clothes."
A claim that later becomes recomputable therefore moves T2 → T1 by design. What is forbidden is
re-tiering on the same evidence.

So the prior-art question is: **is there a levels scheme whose categories encode the METHOD of
evaluation rather than the STRENGTH of the result?**

**Yes — the GUM's Type A / Type B split, and the match is close to exact.** Quoted from
JCGM 100:2008 (*Evaluation of measurement data — Guide to the expression of uncertainty in
measurement*), text extracted this session from the BIPM PDF:

- **§0.7, Recommendation INC-1 (1980)**: uncertainty components "may be grouped into two
  categories **according to the way in which their numerical value is estimated**: A. those which
  are evaluated by statistical methods, B. those which are evaluated by other means."
- **§2.3.2** "Type A evaluation (of uncertainty): method of evaluation of uncertainty by the
  statistical analysis of series of observations." **§2.3.3** "Type B evaluation (of
  uncertainty): method of evaluation of uncertainty by means other than the statistical analysis
  of series of observations."
- **§3.3.3**: the categories are formed "based on their method of evaluation"; note —
  "**Categorizing the methods of evaluating uncertainty components rather than the components
  themselves avoids such ambiguity.**"
- **§3.3.4**, the decisive sentence: "The purpose of the Type A and Type B classification is to
  indicate the two different ways of evaluating uncertainty components and **is for convenience
  of discussion only; the classification is not meant to indicate that there is any difference in
  the nature of the components** resulting from the two types of evaluation."

The mapping onto the ledger's own (a)/(b) criterion is one-to-one: **T1 ↔ Type A** (a numerical
recomputation was reachable), **T2 ↔ Type B** (evaluated by other means — argued from
construction). Neither dominates the other; the label records the route. **Verdict: IDENTICAL**,
and the prior art is from 1980 (INC-1), 28 years before the GUM edition quoted and 46 years before
our 2026-09-11 statement of it. Metrology also states it more strongly than we do: the GUM
volunteers that the classification carries *no* difference in nature, which is a claim our ledger
has not made in writing.

**Second, weaker precedent — ACM Artifact Review and Badging v1.1** (acm.org, fetched this
session via search summary): **Results Reproduced** = "the main results of the paper have been
obtained in a subsequent study by a person or team other than the authors, **using, in part,
artifacts provided by the author**"; **Results Replicated** = the same "**without the use of
author-supplied artifacts**". The two badges are distinguished purely by which route was
available, exactly as T1/T2 are. **Verdict: NARROWER** — the ACM pair encodes route but carries an
implied strength ordering (independent reimplementation is treated as the stronger badge), which
the GUM pair and our (a)/(b) pair do not.

**The contrast cases confirm the property is unusual, not unprecedented.**

- **GRADE** is the explicit opposite on the promotion question. Randomised trials start high and
  observational studies start low — i.e. the *starting* tier is set by method — but the rating is
  then moved by strength considerations, and moved **up**: Guyatt et al., "GRADE guidelines: 9.
  Rating up the quality of evidence", *J. Clinical Epidemiology* 2011;64(12):1311–1316
  (PMID 21802902) — rate up one level for a large effect (≥2-fold), two levels for ≥5-fold, and
  also for a dose–response gradient or for plausible confounders that would only shrink the
  observed effect. GRADE deliberately mixes the method axis and the strength axis on one scale and
  permits promotion. Ours, as of L11–L12, does not permit re-tiering on the same evidence.
- **Oxford CEBM Levels of Evidence (2011)** assigns a level by study design and then allows the
  level to be graded down (and, for large effects, up) — same mixed-axis construction as GRADE.
  (Cited from the GRADE/CEBM secondary literature, not fetched directly — see search record.)
- **IPCC AR5 uncertainty guidance** (Mastrandrea et al., *Guidance Note for Lead Authors of the
  IPCC Fifth Assessment Report on Consistent Treatment of Uncertainties*, 2010; summarised in
  *Climatic Change* 2011, DOI 10.1007/s10584-011-0178-6) is the closest in *shape* to a
  two-axis scheme: evidence (type, amount, quality, consistency) and agreement are evaluated
  **separately**, with confidence a deliberately flexible function of the 3×3 grid rather than a
  computed one. But **both axes are strength axes.** Neither records which route produced the
  finding. **Verdict: not the property we were looking for** — it separates two dimensions of
  strength, not strength from method.

**A finding about our own scheme, recorded because it is checkable.** `docs/Elimination_Ledger.md`
states both readings two lines apart. L11 defines T0 as "machine-CHECKED (kernel-verified by a
proof assistant, axiom dependencies disclosed; added 2026-08-30, **strictly stronger than T1**)";
L12 then states that the ladder means "the PATH marker, **not a strength ordering**". T0 vs T1 is
asserted as an ordering in the same list that denies the ladder is one. By the GUM's own §3.3.4
standard this is the mixed-axis construction GRADE chose on purpose and metrology avoided on
purpose: T1/T2 are method markers, T4 (falsified) is a verdict marker, and T0 is asserted as a
strength marker, all on one axis. This is an observation about the text as it stands on
2026-09-14, not a proposal — the reconciliation, if one is wanted, is the Elimination Ledger's to
append.

**Does "tiers never promote" as a *phrase* have prior art?** Not found as a phrase. The nearest
principle is the append-only / immutable-record discipline already tabled under rule 6, plus the
metrological convention that a measurement result is inseparable from the conditions under which
it was obtained (VIM 2.20 *measurement result*; GUM §7.2.7 on reporting). The phrase itself is
ours; the property it names is not.


### Finding 2 — The negative benchmark: methodology interventions that fail to separate are a well-populated literature, and our result sits inside it

**Our observation, read off `.claude/skills/evidence-chain/SKILL.md` L271–L288 this session, not
recalled:**

```
stale-claims           with 4/5   without 4/5
prose-number           with 4/4   without 4/4
writeup-no-invitation  with 5/5   without 5/5
unverifiable           INVALID (fixture premise false; run targeted the wrong tree)
```

plus "measured recall 0% at iteration 1, 6% at iteration 2, across ten realistic should-trigger
queries" for the skill's description.

**An arithmetic observation about that table, derived from the numbers above.** Summing the three
valid fixtures: both arms scored **13 of 14**. The skill arm's available headroom was therefore
**1 point out of 14 (7.1%)**, and two of the three fixtures were already at ceiling in the
baseline arm. The design could have detected large *harm* (the baseline arm had 13 points to
lose) but could detect at most a 7.1% *benefit*. **"It did not separate" is, on these numbers,
only weakly distinguishable from "it could not have separated upward."** That is a statement
about the instrument, and per rule 3 it is the statement that has to be made before the null is
read as evidence of anything. It does not overturn the skill file's conclusion; it bounds it.

**Is there prior art for methodology/checklist interventions failing to show measurable effect?
Abundantly — this is one of the better-documented null literatures in existence.**

*Surgical and clinical checklists, after the positive flagship trial.*

- A. B. Haynes et al., "A Surgical Safety Checklist to Reduce Morbidity and Mortality in a Global
  Population", *NEJM* 2009;360:491–499 — the positive result that made checklists canon.
- **D. R. Urbach, A. Govindarajan, R. Saskin, A. S. Wilton, N. N. Baxter, "Introduction of
  Surgical Safety Checklists in Ontario, Canada", *NEJM* 2014;370:1029–1038** (PMID 24620866) —
  over 100 hospitals; any-complication rate moved 3.86% → 3.82% and 30-day mortality 0.71% →
  0.65%, **neither significant**, with no significant change in readmissions or ED visits — and
  self-reported checklist compliance above 90% at almost every participating hospital. High
  adherence, no measurable effect.
- **J. Bion et al., "'Matching Michigan': a 2-year stepped interventional programme to minimise
  central venous catheter-blood stream infections in intensive care units in England", *BMJ
  Quality & Safety* 2013;22(2):110–123** — infection rates fell significantly in **both** control
  and intervention arms, consistent with a secular trend; the intervention showed no effect beyond
  it. The paper's own conclusion is that ethnographic work is needed to explain success or failure
  of such programmes, because the outcome numbers do not.
- C. L. Bosk, M. Dixon-Woods, C. A. Goeschel, P. J. Pronovost, "Reality check for checklists",
  *The Lancet* 2009;374(9688):444–445 — written by people on the successful Keystone project,
  cautioning that compliance with a checklist is not the mechanism and should not be read as one.
- Popular-science synthesis with the trial list: E. Anthes, "Hospital checklists are meant to save
  lives — so why do they often fail?", *Nature* 523:516–518, 2015 (PMID 26223609).

*Training people in an explicit debiasing method.*

- **J. Sherbino, K. Kulasegaram, E. Howey, G. Norman, "Ineffectiveness of cognitive forcing
  strategies to reduce biases in diagnostic reasoning: a controlled trial", *CJEM*
  2014;16(1):34–40** (PMID 24423999) — n = 191 students, 4-week EM rotation, allocated to
  cognitive-forcing-strategy training or control: "the educational interventions employed in this
  study to teach CFS failed to show any reduction in diagnostic error by novices." Earlier
  exploratory study by the same group (Sherbino et al., *Teach Learn Med* 2011;23(1):78–84,
  PMID 21240788) reached the same place.

*Interventions aimed at getting people to follow a reporting checklist at all — the closest
analogue to our description-recall result.*

- **D. Blanco, D. G. Altman, D. Moher, I. Boutron, J. J. Kirkham, E. Cobo, "Scoping review on
  interventions to improve adherence to reporting guidelines in health research", *BMJ Open*
  2019;9(5):e026589** (PMC6527996) — maps the intervention landscape and finds the evaluated
  evidence thin, with training on the use of reporting guidelines specifically **unevaluated**,
  concluding that additional research is needed to assess effectiveness. Our own "the description
  barely triggered" is the same failure one layer down: an instrument nobody retrieves cannot be
  measured, however good it is.

*Nulls for written instructions given to an already-capable model — the nearest analogue in our
own medium.*

- **M. Zheng, J. Pei, L. Logeswaran, M. Lee, D. Jurgens, "When 'A Helpful Assistant' Is Not Really
  Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models",
  *Findings of EMNLP 2024*** (arXiv:2311.10054) — 162 roles, 4 model families, 2,410 factual
  questions: adding a persona to the system prompt does not improve performance. The structural
  match to our result is close: a text-level intervention on a capable model, measured against a
  no-intervention baseline, with no separation.
- **J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu et al., "Large Language Models Cannot
  Self-Correct Reasoning Yet", *ICLR 2024*** (arXiv:2310.01798) — **intrinsic** self-correction,
  without external feedback, does not improve and often degrades reasoning performance. Read
  against our SKILL.md's own closing claim — "everything above is a verifier. None of it is a
  generator" — this is the sharper statement of the same limit: a verifier with no external
  observation to check against is not a verifier, it is another generation pass.

**Verdict on the negative benchmark: IDENTICAL in kind, and our result falls inside the
distribution the prior art reports.** A written methodology handed to a capable operator, measured against that operator
without it, failing to separate, is the modal outcome in three independent literatures (surgical
safety, cognitive debiasing, system-prompt engineering). The honest reading is not that the
measurement was unlucky; it is that **this is what these measurements usually return.**

**And the honest reading of our canon's evidential status.** With three fixtures at or near
ceiling, one fixture invalid, a single-digit headroom, and n = 4, the corpus's own evaluation
does not establish that the evidence-chain skill changes behaviour, and does not establish that it
does not. **The canon is unevidenced** — not falsified, unevidenced. Per the exhaustion principle
that is a complete result and belongs on the record as one. It also matches what the prior art
predicts for an intervention of this shape, which makes the measurement *concordant* rather than
anomalous, and removes the motive to re-run it expecting a different number.

**What the prior art suggests would actually be measurable**, offered as an open item and not as a
result: Urbach's 90%-compliance-no-effect and Bion's both-arms-declined are both cases where the
*outcome* measure was saturated or trending independently. The one place SKILL.md reports the runs
did diverge — "distinguishing **not reproduced** from **false**, where the unaided run
overclaimed" — is a non-ceiling discriminator. A benchmark built only from items of that shape has
headroom; the present one does not.

## Search record

Recorded because rule 4 requires it and because a GENUINELY-NOT-FOUND verdict is inadmissible
without it. Session date **2026-09-14**. "Fetched" = the page or PDF was retrieved and read this
session. "Search summary" = the search engine's extracted text was read, the source page was not
opened. Tool: `WebSearch` / `WebFetch` through the session proxy.

### Queries run this session (wave-2 resume)

| # | Query | Outcome |
|---|---|---|
| 1 | `Kimball 1957 "type III error" giving the right answer to the wrong problem statistics` | Hit. Led to fetch #A. |
| 2 | `ICH E9(R1) estimand addendum "target of estimation" define the quantity to be estimated` | Hit (search summary only; five attributes, pre-specification requirement). |
| 3 | `Swanson 1986 "undiscovered public knowledge" Library Quarterly knowledge already recorded but unretrieved` | Hit; abstract text obtained via search summary. Primary DOI page returned **HTTP 403** on fetch (see fetch #B). |
| 4 | `"organizational memory" knowledge management "reinventing the wheel" prior internal reports searched before external literature` | Hit; led to query #5. |
| 5 | `Walsh Ungson "Organizational Memory" Academy of Management Review 1991 16 57-91` | Citation confirmed (16(1):57–91, DOI 10.5465/amr.1991.4278992) via search summary; article body not fetched. |
| 6 | `E-Prime Bourland general semantics Korzybski eliminate "to be" judgment report observation not evaluation` | Hit. Led to fetch #C. |
| 7 | `GAO Yellow Book GAGAS audit finding elements condition criteria cause effect "not to assign blame"` | **Partial.** Four successive searches returned the criteria/condition/cause/effect element definitions, but **the phrase "not to assign blame" was not located in any GAO source.** Recorded as not found; the row cites only the element definitions, which were located. |
| 8 | `IPCC AR5 uncertainty guidance Mastrandrea 2010 confidence two dimensions evidence and agreement not a strength ladder` | Hit (search summary); two-axis evidence/agreement structure confirmed. |
| 9 | `GRADE approach "rating up" quality of evidence observational studies upgrade downgrade Guyatt 2011` | Hit; *GRADE guidelines: 9* (PMID 21802902) and the rate-up criteria confirmed via search summary. |
| 10 | `ACM "Artifact Review and Badging" "Results Reproduced" versus "Results Replicated" badge different team different experimental setup` | Hit; badge definitions obtained via search summary from acm.org policy page. |
| 11 | `Urbach 2014 NEJM "surgical safety checklists in Ontario" no significant reduction mortality complications` | Hit; the 3.86→3.82% / 0.71→0.65% figures and the >90% compliance note obtained via search summary. |
| 12 | `Sherbino 2014 "cognitive forcing strategies" ineffective reduce diagnostic error debiasing training null result` | Hit; CJEM 2014;16(1):34–40, PMID 24423999, plus the 2011 exploratory study PMID 21240788. |
| 13 | `Blanco 2019 scoping review interventions improve adherence reporting guidelines CONSORT little evidence effectiveness` | Hit; *BMJ Open* 2019, PMC6527996. |
| 14 | `Zheng 2024 "When A Helpful Assistant Is Not Really Helpful" personas system prompts do not improve performance LLM` | Hit; arXiv:2311.10054, Findings of EMNLP 2024; 162 roles / 4 model families / 2,410 questions. |
| 15 | `Bion 2013 "Matching Michigan" BMJ Quality Safety central venous catheter bloodstream infection no additional effect secular trend` | Hit; *BMJ Qual Saf* 2013;22(2):110–123, both-arms-declined result. |
| 16 | `Huang 2024 ICLR "Large Language Models Cannot Self-Correct Reasoning Yet" intrinsic self-correction degrades performance` | Hit; arXiv:2310.01798, ICLR 2024. |
| 17 | `Anthes Nature 2015 "hospital checklists" why do they often fail Bosk 2009 "reality check for checklists" Lancet` | Hit; *Nature* 523:516–518 (PMID 26223609) and *Lancet* 2009;374(9688):444–445. |
| 18 | `"defer substitution" OR "keep it symbolic" computer algebra practice evaluate expression as defined before substituting numerical values` | **Not found as a named principle.** Two rounds of results returned only CAS tool documentation (SymPy `subs`/`evalf`, MATLAB `subs`, Sage, Mathcad) describing the mechanism, and one pedagogy page. No canonical source states "evaluate the defined object before substituting" as a *rule*. See GENUINELY-NOT-FOUND #1. |
| 19 | `"evidence tiers" OR "levels of evidence" "never promote" claim stays at tier it entered immutable` | **Not found, and the opposite was found.** Results returned the ESSA (Every Student Succeeds Act) tiers of evidence and WWC material, which state the reverse: tier ratings "are not static" and change as new evidence on impacts becomes available. See GENUINELY-NOT-FOUND #2. |

### Documents fetched and read this session

| Ref | Source | Result |
|---|---|---|
| A | `https://en.wikipedia.org/wiki/Type_III_error` | Fetched. Kimball's definition quoted ("the right answer to the wrong problem", p. 134) plus Mosteller 1948, Mitroff & Featheringham 1974, Raiffa, Marascuilo & Levin 1970. **The page carries no journal/DOI details**, so the JASA 52(278):133–142 citation in the table is from the search summary, not from a fetched bibliographic record. |
| B | `https://www.journals.uchicago.edu/doi/10.1086/601720` (Swanson 1986) | **HTTP 403 Forbidden.** Abstract text used in the table comes from the search summary of the same DOI. |
| C | `https://en.wikipedia.org/wiki/E-Prime` | Fetched. Bourland 1965 *General Semantics Bulletin* citation and the Kellogg & Bourland "deity mode of speech" quotation confirmed. Korzybski *Science and Sanity* full citation **not** present on the page. |
| D | `https://jcgm.bipm.org/vim/en/2.28.html` (VIM3 Type A evaluation) | Fetched. Definition confirmed; the page's notes do **not** carry the nature-of-components statement, which sent the search to the GUM itself. |
| E | `https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf` (GUM, 1.8 MB) | **Fetched, and text extracted locally** (WebFetch could not read the compressed PDF; extracted with `pypdf`, 384,702 chars, to the session scratchpad). §0.7 / §2.3.2 / §2.3.3 / §3.3.3 / §3.3.4 read directly and quoted verbatim in Finding 1. **This is the only primary source quoted from its own text in this session's additions.** |
| F | `https://physics.nist.gov/Pubs/guidelines/sec3.html` (NIST TN 1297) | **301 redirect** to `nist.gov/pml/pubs/tn1297/index.cfm`; not followed, because fetch #E had already supplied the primary GUM text. |

### GENUINELY-NOT-FOUND

**#1 — "Solve it symbolically with the substitutions left out" (technique half of rule 1).**
Searched: query #18, two rounds. Found: computer-algebra system documentation describing *how* to
defer substitution (SymPy, MATLAB, Sage, Mathcad) and one teaching page on symbolic vs numeric
expressions. Not found: any source stating deferred substitution as a *methodological rule* for
checking a claimed identity. Assessment: this is folk practice with wide tooling support and no
canonical statement. The concept half of rule 1 (evaluate the object actually defined) is covered
by Kimball / Mitroff–Featheringham / ICH E9(R1) and is **not** not-found.

**#2 — "Tiers never promote" as a stated principle of a levels-of-evidence scheme.**
Searched: query #19, plus queries #9 and #10 approaching it from GRADE and from ACM badging.
Found: the opposite, repeatedly and explicitly. GRADE has a dedicated guideline for **rating up**
(Guyatt et al. 2011, *GRADE guidelines: 9*). ESSA tiers are stated to be non-static and to change
with new evidence. ACM badges are awarded per artifact evaluation and are not described as
immutable. Not found: any evidence-levels scheme that forbids re-tiering. Assessment: **the
prohibition appears to be ours.** But note what Finding 1 establishes — the *property* the
prohibition was protecting (tiers encoding method, not strength) is the GUM's Type A/Type B split
from Recommendation INC-1 (1980), stated there more explicitly than in our own ledger. So the
not-found result is narrow: the phrase and the no-re-tiering rule are unprecedented; the idea they
protect is 46 years old.

**#3 — "Not to assign blame" as GAGAS language.**
Searched: query #7, four successive result sets, including attempts at the GAO Yellow Book PDF
listing pages. Found: the criteria/condition/cause/effect element definitions (used in the rule-11
row). Not found: the specific non-attribution language. The rule-11 row therefore rests on the
*structure* of a GAGAS finding, which was located, and not on a blame-prohibition clause, which
was not. Recorded so the row is not read as claiming more than was seen.

### Not searched (declared, per rule 10)

- The Rosenberg *Nonviolent Communication* citation in the rule-11 row was **not opened this
  session**; it is carried from prior knowledge and is an assumption.
- ICH E9(R1), Kimball 1957, Mitroff & Featheringham 1974, Walsh & Ungson 1991, Guyatt et al. 2011,
  Urbach et al. 2014, Bion et al. 2013, Sherbino et al. 2014, Blanco et al. 2019, Zheng et al.
  2024, Huang et al. 2024, Bosk et al. 2009, Anthes 2015, Haynes et al. 2009, the ACM badging
  policy and the IPCC AR5 guidance note were all reached **via search summaries only**; none of
  their full texts was fetched. Their quoted figures and phrasings are second-hand this session.
- Oxford CEBM Levels of Evidence (2011) was **not searched directly**; the characterisation in
  Finding 1 comes from the GRADE/CEBM secondary material returned by query #9 and is flagged there.

