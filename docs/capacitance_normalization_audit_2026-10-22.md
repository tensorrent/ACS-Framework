# Capacitance normalisation audit, 22 October 2026

Per-model check of the three capacitance models in `code/capacitance_ribbon/ribbon_capacitance.py`
against the numbers printed in `papers/notes/Mobius_Ribbon_Capacitance.tex`. It answers the
note's own amendment (line 254): "This does not identify all three numerical models with that
later formula; it requires each model's normalization to be checked separately before a
physical comparison." It is an audit of conventions and arithmetic, not a physical comparison:
the artifact's own scope line (`capacitance_ribbon_results.json`, `claim_discipline`: "RC1 as-implemented model outputs; not a uniqueness proof of alpha") stands.
Line numbers refer to commit `8b9ba94`. The paper and the committed artifact
`docs/capacitance_ribbon_results.json` are manifest-bound and were not edited.

## How the script was run

```
ACS_OUT_DIR=<scratch>/cap2 ACS_MEMO_DIR=<scratch>/cap2/memo OMP_NUM_THREADS=1 \
  acs-venv/bin/python code/capacitance_ribbon/ribbon_capacitance.py
```

Wall time 19.4 s, exit 0 (Python 3.12.3, numpy 2.2.6, scipy 1.15.3). Both overrides are in the
script at `8b9ba94` (`ACS_OUT_DIR`, lines 675–683; `ACS_MEMO_DIR`, `code/acs_memo.py` line 43), so
the run wrote only `<scratch>/cap2/capacitance_ribbon_results.json` and its BIE memo files;
`git status --short` in the worktree and in the main checkout was empty afterwards. A second run
into `<scratch>/cap` gave a byte-identical JSON. Against the committed JSON the fresh file differs
only in the `comparison_table` BIE columns, by at most `4.4e-16` relative (`alpha_inv_bie`, 16
rows) and `3.3e-16` (`C_bie_F`); the `constants`, `formulas`, `scan_meta`, `demo_point`,
`best_on_grid` and `analytic_codata_match` blocks are equal. The comparison script is
`scratchpad/actionable2/checks/cap_compare.py` (output `cap_compare.out`); the two mesh probes are
`bie_mesh.py` and `bie_extreme.py`. None of them is committed.

## Conventions shared by all three models (from the code)

| Quantity | Held fixed at | Where |
|---|---|---|
| Radius | $R=\hbar/(2m_ec)=1.9307963\times10^{-13}$ m (`R_SPIN`) | line 46 |
| Charge | $Q=e/2$ per double-cover sheet (`Q_SHEET`) | line 49 |
| Self-energy match | $(e/2)^2/(2C)=m_ec^2$, hence $\alpha^{-1}=\pi\epsilon_0R/C$ | `alpha_from_C`, lines 70–85 |
| Units | $C$ in farads; the dimensionless $\hat C=C/(\epsilon_0R)$ gives $\alpha^{-1}=\pi/\hat C$ | note lines 97 and 157–158 |
| Constants | `scipy.constants` float64; $\alpha^{-1}_{\rm ref}=137.03599917759013$ | lines 40–43 |

The $\alpha$ map is the same function for every model, so the per-model question is only what
each model puts into $C$: which radius, which cutoff length, which mesh.

## Per-model normalisation and the numbers (demo point $a/R=0.05$)

| Model | Normalisation derived from the code | Paper quotes (lines 181–183) | Script gives | Match |
|---|---|---|---|---|
| Annulus (`annulus_C`, lines 97–118) | $C=2\pi\epsilon_0R/L$, $L=\ln(8R/a)+1$; closed form $\alpha^{-1}=L/2$, i.e. $\hat C=2\pi/L$. Only $R$ and $a$ enter. | $C=1.768\times10^{-24}$ F, $\alpha^{-1}=3.037587$, $\hat C=1.034$ | $1.768098\times10^{-24}$ F, $3.037587$, $1.0342$ | match to every printed digit |
| Conformal, cover 2 (`conformal_annulus_C`, lines 125–157) | strip $L_s=4\pi R$, $W=2a$; $R_m=2R$; $a_{\rm eff}=2R\sinh(a/2R)$; $C=2\pi\epsilon_0R_m/(\ln(8R_m/a_{\rm eff})+1)=4\pi\epsilon_0R/L'$ with $L'=\ln(16R/a_{\rm eff})+1$. The log formula uses $R_m=2R$ but the $\alpha$ map keeps $R$, so $\alpha^{-1}=L'/4$, not $L'/2$. | $3.174\times10^{-24}$ F, $1.692054$, $1.857$ | $3.174101\times10^{-24}$ F, $1.692054$, $1.8567$ | match to every printed digit |
| BIE Möbius (`bie_mobius_C`, lines 290–330; `_bie_mobius_C_uncached`) | lengths nondimensionalised by $R$; constant-panel collocation at unit potential on $X(u,v)=r(u)+v\,n(u)$, $v\in[-a,a]$; $\hat C=Q/V$ at $V=1$; SI $C=\hat C\epsilon_0R$. Mesh is part of the normalisation: demo $48\times6$ panels, scan $40\times5$ (`main`, lines 618 and 620). | $1.441\times10^{-23}$ F, $0.372688$, $8.430$ | $1.441075\times10^{-23}$ F, $0.372691$, $8.4295$ | $C$ and $\hat C$ match as printed; $\alpha^{-1}$ differs in the sixth significant figure (paper $0.372688$; script and committed JSON both $0.3726906505$) |

The closed forms were re-evaluated on all 28 grid rows from the JSON: $\alpha^{-1}_{\rm ann}=L/2$
and $\alpha^{-1}_{\rm conf}=L'/4$ hold to better than $10^{-12}$ relative on every row, and
$\alpha^{-1}_{\rm BIE}=\pi/\hat C$ on all 16 BIE rows (`cap_compare.out`). The paper's ordering
claim (lines 208–216, $\alpha^{-1}_{\rm ann}>\alpha^{-1}_{\rm conf}>\alpha^{-1}_{\rm BIE}$) holds on
every BIE row.

### The sixth digit of the BIE row is below the instrument's own resolution

Mesh sequence at $a/R=0.05$ (`bie_mesh.py`, uncached, one thread):

| panels ($n_u\times n_v$) | $\hat C$ | $\alpha^{-1}$ | time |
|---|---|---|---|
| 72 ($24\times3$) | 8.702334 | 0.361006 | 0.4 s |
| 128 ($32\times4$) | 8.582335 | 0.366053 | 0.7 s |
| 200 ($40\times5$, scan mesh) | 8.494501 | 0.369838 | 1.5 s |
| 288 ($48\times6$, demo mesh) | 8.429491 | 0.372691 | 2.7 s |
| 512 ($64\times8$) | 8.336005 | 0.376870 | 6.3 s |

$\hat C$ falls monotonically with refinement and has not converged: the last step (288 to 512
panels) moves it by 1.1%. The paper's six printed digits for $\alpha^{-1}_{\rm BIE}$ therefore
carry at least a $10^{-2}$ discretisation uncertainty, and the $3\times10^{-6}$ disagreement
between the paper's $0.372688$ and the artifact's $0.372691$ is immaterial beside it. The
committed JSON and this machine agree to $4\times10^{-16}$, so the paper's digit is a
transcription or an earlier-run value, not a platform difference. No Richardson extrapolation
is claimed here; the five-point sequence is too short for one and the panels are not
self-similar across the window.

## The CODATA-matching rows (paper lines 199–205)

| Model | What the row means in the code | Paper | Script | Match |
|---|---|---|---|---|
| Annulus | $a/R=8\exp(1-2\alpha^{-1}_{\rm ref})$ (`annulus_a_over_R_for_alpha`, line 118) | $\approx2.039\times10^{-118}$ | $2.0390503\times10^{-118}$ | match |
| Conformal | bisection of $C_{\rm conf}(a/R)=\pi\epsilon_0R/\alpha^{-1}_{\rm ref}$ on $\ln(a/R)\in(\ln10^{-300},\ln0.5)$, 80 steps (`_conformal_match_codata`, lines 543–588) | $\approx3.824\times10^{-237}$ | $3.8238549\times10^{-237}$; closed form $a_{\rm eff}/R=16\exp(1-4\alpha^{-1}_{\rm ref})=3.82386\times10^{-237}$ | match |
| BIE | no row is computed: the scan returns `null` outside $5\times10^{-3}\le a/R\le0.25$ (`scan_aspect_ratios`, lines 442–443; actual BIE rows $0.0070\le a/R\le0.1848$, 16 of 28) | "--- not resolved at that aspect" | see below | consistent |

What the BIE instrument returns if the window is ignored (`bie_extreme.py`, scan mesh $40\times5$,
1.5–1.7 s per point):

| $a/R$ | $\hat C_{\rm BIE}$ | $\alpha^{-1}_{\rm BIE}$ | annulus closed form $L/2$ |
|---|---|---|---|
| $5\times10^{-3}$ | 7.4455 | 0.4219 | 4.19 |
| $10^{-4}$ | 6.9249 | 0.4537 | 6.14 |
| $10^{-10}$ | 5.5741 | 0.5636 | 13.05 |
| $10^{-20}$ | 4.2201 | 0.7444 | 24.57 |
| $10^{-50}$ | 2.4275 | 1.2941 | 59.10 |

The BIE $\alpha^{-1}$ grows roughly like $0.016\,\ln(R/a)$ against the annulus's $0.5\,\ln(R/a)$:
with five panels across a half-width of $10^{-50}R$ the self-panel regularisation, not the
geometry, sets $\hat C$. Reaching $\alpha^{-1}=137$ with this discretisation is not a matter of
a longer scan; it would need a panel aspect ratio of order $10^{118}$, which the constant-panel
scheme does not represent. The paper's "not resolved at that aspect" is therefore the correct
statement, and the sharper form it supports is "not resolvable by this instrument". That
sentence, for the manifest-bound note, is proposal §3 of the condensate block in
[proposed amendments, pass 2](proposed_amendments_2026-10-22_pass2.md).

## The self-energy convention, for the record

The audited script uses $E=Q^2/(2C)$ with $Q=e/2$, hence $\alpha^{-1}=L/2$ for the annulus and
$a/R=8e^{1-2K}=2.03905\times10^{-118}$ at $K=137.035999084$. The two other conventions on record
give $a/R=8e^{1-K}=6.65896\times10^{-59}$ ($E=Q^2/C$, the recovered CPF manuscript; the carrier
audit quotes $6.65896\times10^{-59}$ at $K=137.035999171$, reproduced) and $8e^{1-K/2}=3.80536\times
10^{-29}$ ($Q=e$). All three are inverse insertions (`cap_compare.out`); none is a prediction, as
the note says at lines 119–121.

## Verdict on the two parts of candidate 36

1. **Per-model normalisation.** Checked separately: the three models share $R$, $Q=e/2$ and the
   $Q^2/(2C)$ match; the annulus and conformal models differ only in the length that enters the
   logarithm (the conformal model's $R_m=2R$ against the unchanged $R$ in the $\alpha$ map is why
   its closed form is $L'/4$); the BIE model's normalisation includes its mesh, which is not
   converged at the 1% level. The paper's numbers are reproduced to their printed digits except
   the sixth digit of $\alpha^{-1}_{\rm BIE}$.
2. **BIE at the CODATA aspect.** Not reached and not reachable by this instrument; measured drift
   outside the window is in the table above. The honest table entry is the one the paper has.

## Left out

No mesh beyond 512 panels; no extrapolation; no attempt to refine the mesh below $a/R=5\times
10^{-3}$ (the probe above deliberately used the scan mesh to show what the published window
protects against). Nothing here bears on whether any of the three models is the right conductor
for the ribbon, which is frontier M02's open question.
