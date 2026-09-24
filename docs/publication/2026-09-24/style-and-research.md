# Style and primary-literature review

Reviewed on 24 September 2026. The established corpus retains its article classes and notation. The new papers follow the sequence: problem and scope; definitions and conventions; derivation; checks and controls; limitations; conclusions; reproducibility appendix; references. This avoids imposing an unrelated journal template on historical manuscripts.

## Primary models for flow and methods

- [APS manuscript guidance](https://journals.aps.org/authors/web-submission-guidelines-physical-review) and [REVTeX](https://journals.aps.org/revtex): structural LaTeX markup, explicit sections, readable equations and a separate reproducibility record. REVTeX is a possible submission format, not a requirement for this repository release.
- [Kannike, arXiv:1603.02680](https://arxiv.org/abs/1603.02680), corrected version 3: distinguish potential definitions, orbit restrictions and boundedness conditions. The ACS paper likewise separates boundedness, local stability and global vacuum selection. No stability theorem is imported without its assumptions.
- [Jiang, Craig, Li and Sutherland, arXiv:1811.08878](https://arxiv.org/abs/1811.08878): organize matching around the model and conventions, then corrections and applicability. The ACS finite-matching discussion states its heavy/light, normalization and flavor restrictions.
- [Gherardi, Marzocca and Venturini, arXiv:2003.12525](https://arxiv.org/abs/2003.12525), version 5: place a clearly defined operator/matching problem before detailed coefficients and appendices. The ACS basis and component-code authority are stated before numerical spectra.
- [Heeck and Sokhashvili, arXiv:2303.09566](https://arxiv.org/abs/2303.09566), version 2: specify the scalar model and charge before discussing localized solutions. The ACS carrier paper distinguishes its added quartic and conditional threshold from that reference model.
- [Vashistha, Gannouji and Ganguly, arXiv:2606.09786](https://arxiv.org/abs/2606.09786), version 1: the algebraic contortion sector is the relevant comparison for the torsion correction. The ACS paper gives its own decomposition and does not import the neutron-star phenomenology.

These sources supply context and presentation models, not endorsements of ACS. Their claims are not counted as fresh ACS checks. The new manuscripts use original prose, short descriptive citations and explicit limits.

## Editorial checks

All 33 existing manuscripts receive claim-specific amendments. Front matter points readers to the governing update. The two new abstracts state results and limits; conventions define coefficients, coordinates, metrics and charge thresholds before calculations. Failed inferences remain identifiable, and numerical qualification is distinguished from an exact argument.

Long paths use breakable URL typography; ordinary tables fit the text width; long tables retain pagination; long displays are split. Missing Unicode glyphs are replaced with portable TeX forms. The unresolved Paper-A citation key is corrected to its existing Paper-B bibliography entry. Source and PDF inventories, build diagnostics and visual review accompany this release.

The review is a consolidation and targeted consistency audit. It does not independently re-prove the complete older corpus, rerun every archived simulation, or verify every historical external citation. The declared fresh checks and retained evidence are enumerated in the release README.
