# Blocked and long-horizon items: what is missing, and from whom (22 October 2026 list, pass 2)

This page covers twelve items from the 22 October candidate list. Each is either blocked
on an input that is not in this repository, or is a long-horizon addition. For each item
it records:

- the item in its source's words, with file and line;
- what the repository already holds toward it;
- exactly what is missing, who has it, and in what form it should arrive;
- what becomes possible when it arrives.

Nothing here closes an item. Where a check could be run today without the missing input,
it was run, and the result is labelled *measured* with its command. Everything else is
cited, not re-measured.

**Line numbers.** acs-framework line numbers refer to commit `4f3f28d`. AISO-UI-for-Ai
line numbers refer to `76f5983`.

**Concurrent work.** While this page was being written, `f7e688c` added two things. One
is "Records that depend on the authoring machine" in [REPRODUCTION](REPRODUCTION.md),
which overlaps items 30(c) and 67 below. The other is the FF06e block in
[pass-2 amendments](proposed_amendments_2026-10-22_pass2.md), which overlaps item 116.
Where they agree, this page cites them rather than repeating them.

**How the runs were done.** Every run used the pinned environment (Python 3.12, numpy,
scipy) with single-threaded BLAS. Runs used scratch copies of the files outside the
repository, or instruments that print only to stdout. `git status --short` was empty
after every run. No manifest-bound file was edited. Of the files this page names, all 70
files under `code/condensate_energy/` are manifest-bound, as are `papers/**` and
`docs/publication/2026-09-24/provenance/archive-coverage.json`. That is why several
"ports" below are owner decisions rather than edits.

## Summary

| idx | Item | What is missing | From whom | Changed by this pass |
|---|---|---|---|---|
| 30 | Archived PDE runs, large-N slopes, drive-bound programs | (a) nothing external: compute time and a comparison rule; (b) the original α(N) regression program; (c) owner approval to repoint 4 manifest-bound programs to in-repo snapshots | (a) anyone; (b), (c) the author/owner | (a) one PDE program rerun from a scratch copy reproduces its record (measured) |
| 31 | Two encrypted zip members | the password, or the two plaintext files | the author | none |
| 32 | Cloud-chat recovery | a complete provider export of the cloud conversations and attachments | the account holder (the author) | none |
| 33 | OCR pass and large-TAR screening | the 54 PDFs, or the drive; the two ≥200 MB TAR members; the per-file path list | the author (drive holder) | none. The per-file list is confirmed absent from the repository |
| 67 | Throat/Refined run logs, DAW canvas, primary CPF sources | the original July run logs (provenance only); two `.tsx` canvases; a ruling on which CPF text is primary | the author | the Throat and Refined computations reproduce from scratch copies (measured) |
| 98 | K02 training corpus and run identities; the "Croft" source | 7 named files (verified absent) plus run manifests; a citation for "Croft" | the author | none |
| 106 | Q2 matched-f64 bench | the OOS01 bench harness and log, TensorFlow in a pinned environment, and the kernel revision that was benchmarked | the author; environment | the kernel source is found in AISO-UI-for-Ai (`trinity-wasm/`) |
| 107 | Sealed Yang–Mills set never scored | the external construction itself | its author, via the owner | the checker's defects are re-measured, and a fourth defect is found |
| 115 | computational-tensegrity `paper/` | nothing: the files are in the remote's history at the parent commit | the owner decides whether to restore | **reclassified: owner decision, not blocked** |
| 116 | Counting-deviation witness definition | the author's formula and the table's rounding rule | the author (FF06e source) | the reconstructed reading is measured; the printed value does not exclude it |
| 24 | FeynRules/UFO export | long-horizon work, plus fixed coefficients that the record says do not exist | maintainer work; coefficients are an open problem | scoped, not started |
| 72 | Coleman–Weinberg analysis | long-horizon work; "6 → 5" is superseded as posed | maintainer work | scoped, not started |

---

## 1. Archived PDE runs and large-N slopes not rerun; recovery programs need the local drive (idx 30)

**Source.**

- `docs/publication/2026-09-24/science-report.json:2` (also
  `code/publication_20260924/verify_science.py:140`): "archived PDE runs are
  integrity-checked, not rerun."
- `papers/core_trilogy/Riemann_Spectral_Critical_Line.tex:1654-1655`: "No historical
  large-$N$ slope or physical experiment was recomputed for this revision."
- `docs/publication/2026-09-24/README.md:33`: "Original archive-recovery programs may still
  require the local drive; they are retained as provenance and are not the portable CI
  entry point."
- `papers/updates/ACS_Action_Identifiability.tex:325-326`: "archive recovery programs
  requiring the original local drives are not advertised as portable."
- `docs/REPRODUCTION.md:89`: "An archived script may require its original environment or
  source data; the CI entry points above define the portable subset."

The candidate list's phrase "port drive-bound recovery programs" does not occur in
`docs/REPRODUCTION.md`. Line 89 is the nearest wording.

### (a) Archived PDE runs

**What "integrity-checked" covers.** `scripts/verify_publication.py:31-46` hashes every
reference in `docs/condensate_energy/endpoint_audit/receipt.json`:

| Receipt section | References |
|---|---|
| `prior_receipts_verified` | 13 |
| `prior_artifacts_verified` | 387 |
| `linked_evidence_verified` | 63 |
| `artifact_sha256` | 53 |
| **Total** | **516** |

Of these, 16 are resolved through `receipt-relocations.json`. None are archive-only
(`docs/publication/2026-09-24/integrity-report.json`).

**Which programs are PDE-style.** A grep for time-stepping markers (`solve_ivp`, `dt =`,
`n_steps`, `np.roll`, Laplacian) finds 11 files in `code/condensate_energy/`. Among them
are `self_binding_dynamics.py` ("Conservative radial evolution and mechanism-removal
controls"), `charge_leakage.py`, `capture.py` and `run.py`.

**Why they were not rerun in place.** They write into tracked paths:

- `self_binding_dynamics.py:115,131` → `docs/condensate_energy/self_binding/dynamic-results.json`
- `charge_radiation.py:16,117` → `docs/condensate_energy/charge_leakage/`
- `run.py:32,41` → `docs/condensate_energy/`

All 70 files under `code/condensate_energy/` are manifest-bound, so an output-redirect
flag cannot be added without the integrity gate.

**Measured today (one program, from a scratch copy).** `self_binding_dynamics.py` was run
from a copy of `code/condensate_energy/` and `docs/condensate_energy/self_binding/` in
`scratchpad/actionable2/bn-pde-rerun/`:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/condensate_energy/self_binding_dynamics.py
```

- **Run.** It completed with rc 0 in 30.9 s wall (the recorded run gives
  `elapsed_seconds` 15.25). All 10 cases evolved, and all 7 checks pass, as recorded.
- **Energy drift.** The maximum is 6.957779941e-06, against 6.957779940e-06 recorded.
- **All floats.** 28,218 floats were compared. Values with |recorded| > 1e-10 (25,356 of
  them) agree to a maximum relative difference of 6.6e-08, at `perturb5/history/chi0`.
  The remaining 2,862 near-zero values differ by at most 1.25e-15 absolute.

That is one PDE program out of 11. The other ten were not run, so their runtimes and
agreement are unknown.

**Missing.** No external input. This sub-item needs:

- compute time;
- a written comparison rule (which tolerance counts as "reproduced") fixed before the
  runs;
- either the scratch-copy method used here, or an owner-approved `ACS_OUT_DIR`-style
  override. The override would change manifest-bound files.

`code/palpha_overlap/palpha_overlap.py:45-51` already has such an override and is the
model for it.

**On arrival.** A dated rerun receipt for each PDE program, saying "reproduced to X" or
"differs at Y". The archived results stay as they are.

### (b) Large-N slopes

The printed values are in `Riemann_Spectral_Critical_Line.tex:1010-1018`: "The earlier
run on the supplied $2{,}001{,}052$-ordinate table reported $\alpha(50)=-0.000200$ […]
and $\alpha(2{,}000{,}000)=0.001259$." The injection slopes are at `:1035-1045`.

**What is present.**

- **The input table.** `docs/frontier/2026-09-12-source-delta/Primary_Tables.zip` holds
  `zeros6.gz` (14,369,780 bytes). Its 2,001,052-row count is asserted by
  `code/frontier_verification/verify_source_delta.py:69` and
  `dataset_precision_audit.py:56`.
- **No program for the printed values.** A grep for the printed values 0.001259,
  0.001247 and 0.001045 over `.py/.md/.json/.tex/.txt` finds only unrelated
  condensate-energy data.
- **The heritage scripts are not that program.**
  `code/acs_codebase/extras/riemann_scaled_final.py:6` uses "100 Odlyzko zeros", and
  `riemann_tensor.py:153-154` uses the first 20 zeros.

**Missing.**

- The original α(N) regression program, with its x-grid, windowing and variance
  estimator, and its run log. Form: the script and the log, with sha256.
- The author's ruling on the injection convention. `:1020-1029` says: "At $\sigma=1/2$ its
  envelope factor is one, not zero. Also, if $x$ denotes logarithmic coordinate, the
  actual explicit-formula envelope is $e^{(\sigma-1/2)x}$, not $x^{\sigma-1/2}$." The open
  problem is mapped in [open problems](open_problems_2026-10-22.md) at `:136`.

Without the program, a rerun would be a RECONSTRUCTED regression, not a recomputation.

**On arrival.** α(N) can be rerun from N = 50 to 2,000,000 on the vendored table, against
the six printed values.

### (c) Drive-bound programs

Eight Python files hard-code `/Volumes/...` or `/Users/...` paths:

- `code/condensate_energy/endpoint_identifiability.py:28-29`
- `code/condensate_energy/colour_singlet_boundary.py:14`
- `code/condensate_energy/microscopic_selector_boundary.py:27`
- `code/condensate_energy/source_endpoint_algebra.py:21`
- `docs/condensate_energy/source_endpoint/attempts/koide_rg_flow/replay.py:405-406`
- `docs/condensate_energy/source_endpoint/attempts/higgs_potential/replay.py:35`
- `docs/condensate_energy/endpoint_audit/attempts/phase6-timeout-60s/driver.py:27`
- `docs/condensate_energy/input_closure/source-snapshots/koide_from_vev.py:423`

**Snapshots exist for the files the drive held.** For the files those programs read from
the drive, `docs/condensate_energy/endpoint_audit/source-snapshots/` holds copies. The
sha256 of each copy appears in the audit's own records (*measured*, `sha256sum` then
grep):

| Snapshot | Recorded in |
|---|---|
| `rc7_lagrangian.py` (`773bee9f…`) | `provenance.json`, `receipt.json` |
| `palatini_colour_charges.py` (`24b117fd…`) | `provenance.json`, `receipt.json` |
| `ACS_Relational_Electrodynamics_Paper.md` (`c0675acb…`) | `microscopic-provenance.json`, `receipt.json` |

**Missing.** Owner approval, through the integrity gate, to repoint the four
manifest-bound `code/condensate_energy` programs at the hash-checked snapshots when the
drive path is absent. No new input is needed for those four. The two
`attempts/*/replay.py` files write figures to `/Users/...`. They are retained failed or
attempt records and should stay byte-identical.

**On arrival.** `endpoint_identifiability.py`, `colour_singlet_boundary.py` and
`microscopic_selector_boundary.py` become runnable from a clone.

**The concurrent inventory agrees and goes further.** The "Records that depend on the
authoring machine" section of [REPRODUCTION](REPRODUCTION.md), added in `f7e688c`, lists
the same four programs. It reports that all 21 absolute-source snapshot hashes match:
"21 of 21, recomputed on 23 October 2026". The three hashes above are a subset of that
check by the same method, not a second method.

---

## 2. Two encrypted archive members unread (idx 31)

**Source.** `docs/publication/2026-09-24/provenance/archive-coverage.json`:

- `:34-35`: "`Sovereign_Monolith_FINAL_20260130_003048.zip!SOVEREIGN_IEEE_REPORT.md`
  … file_size=5751 compress_size=2738> is encrypted, password required for extraction"
- `:38-39`: "`…!sovereign_paper.tex` … file_size=6385 compress_size=3030> is encrypted,
  password required for extraction"
- `:105`: "Two encrypted members of Sovereign_Monolith_FINAL_20260130_003048.zip remain
  unread."

`docs/condensate_energy/endpoint_audit/assessment.json:19` retains the related limit: "No
exhaustive semantic recovery of whole drives, encrypted archives or unexported cloud
chats".

**Missing.** One of the following, from the author:

- the zip password, delivered out of band and never committed;
- the two plaintext files themselves.

The archive is on the author's drive (`/Volumes/Seagate 4tb/Cold_Vault/`).

**Form.** Either the password, or the two files. If the files are sent, they must be 5,751
and 6,385 bytes, matching the sizes the zip's central directory records. Their CRC-32 can
then be checked against that directory, so the plaintext is tied to the archived bytes.

**On arrival.** Extract the two files and check their CRC-32. Record the sha256 values.
Screen them with the four `archive-rescreen.json` patterns and read them. Write the
result as a dated addendum. `archive-coverage.json` is manifest-bound, so the addendum
does not edit it.

The members are small (about 12 kB together), so the work is minutes once the input is
here.

---

## 3. Cloud-chat recovery incomplete (idx 32)

**Source.**

- `archive-coverage.json:108`: "Long cloud chats were not fully paginated; all cloud
  attachments and every cloud-only conversation were not exported or independently
  hashed."
- `docs/condensate_energy/endpoint_audit/README.md:237-239`: "finds 138 matches across
  four named patterns. These are discovery counts, not 138 independently validated
  models. Neither keyword screening nor this audit certifies complete cloud-chat
  recovery."
- `completion-audit.json:20`: "not a semantic audit of every stored or cloud-only
  conversation".

**Measured composition of the 138.** `archive-rescreen.json` holds 138 matches over 3,645
paths, using four patterns. Classified by a substring test on each match's `source`
path, the split is:

| Store | Matches |
|---|---|
| Antigravity | 104 |
| Seagate filesystem | 19 |
| Claude | 10 |
| Cursor | 5 |

This classification is a heuristic of this pass, not a field in the record.

**Missing.** A complete export of the cloud conversations, including long-chat pagination
and every attachment. It must come from the account holder, because only the account
holder can request it.

**Form.** Each provider's official data-export archive, kept outside this repository for
privacy, with its sha256 recorded here.

**On arrival.**

- Hash each conversation and attachment independently.
- Rerun the four-pattern screen and compare it with the 138.
- Run a non-lexical pass, because `archive-coverage.json:102` warns that "Keyword
  screening can miss work that uses unrelated vocabulary".

The result is a coverage addendum. It certifies at most what the export contains.

---

## 4. OCR pass and large-TAR content screening (idx 33)

**Source.** `archive-coverage.json`:

- `:52-56`: `filesystem_pdf_statuses` "text extracted": 164, "no text": 54,
  "duplicate": 62.
- `:103`: "54 filesystem PDFs have no extractable text, mainly figures/icons and unrelated
  documents; no general OCR pass was run."
- `:42-50`: the two archive gaps,
  `acs_codebase.tar.gz!sovereign_sdk/monolith_bench.log` and
  `…!sovereign_sdk/sovereign_training_corpus.jsonl`, each with "TAR member >=200 MB".
- `:105`: "Two TAR members at least 200 MB (a training corpus and a monolith benchmark
  log) were not content-screened".

**The per-file list is not in the repository.** `endpoint_audit/README.md:305` links an
"archive coverage ledger" at `../../../../reports/rh-research-audit-20260923/seagate-extension/coverage.json`.
That path does not exist from a clone (*measured*: `ls` returns "No such file or
directory").

`receipt-relocations.json` maps that absolute path to
`docs/publication/2026-09-24/provenance/archive-coverage.json`. That file is 7,934 bytes
and holds counts only. So the 54 PDFs are counted here, but not named.

**Missing.** From the drive holder:

- the 54 PDFs, or their path list together with drive access;
- `acs_codebase.tar.gz`, or the two members extracted.

**Form.** A file list with sha256, and the files themselves outside the repository.

**On arrival.**

- OCR the 54 PDFs (for example with tesseract), then apply the four-pattern screen.
- Stream-screen the two TAR members. They are at least 200 MB each, so this is
  line-streamed, not loaded whole.
- Record the counts in a dated addendum.

Whether `sovereign_training_corpus.jsonl` relates to the K02 corpora (idx 98 below) is
not established. The names differ.

---

## 5. Missing reproduction artefacts: Throat/Refined P_α run logs, Density_Engine DAW canvas, primary CPF sources (idx 67)

**Source.**

- `papers/notes/Flag_Condensate_Palpha_Throat_Overlap.tex:186` and
  `Flag_Condensate_Palpha_Refined.tex:390`: "(run logs not committed to this
  repository)."
- `papers/notes/Density_Engine_Many_Worlds.tex:390-391`: "The eigen-path DAW visualisation
  (\nolinkurl{Aiso_build_artifacts/eigen_path_daw_viz/}, an external, unpublished build
  artifact --- not committed to this repository)".
- `Density_Engine_Many_Worlds.tex:413`: "\texttt{density-engine.canvas.tsx},
  external/unpublished".
- `docs/BUGFIX_LOG.md:56`: "`eigen-path-daw.canvas.tsx` (canvases workspace on the
  authoring machine, outside this repository)".

### Run logs

**Measured today.** Both instruments were run from scratch copies of `code/palpha_overlap/`
and `code/acs_memo.py` in `scratchpad/actionable2/bn-palpha-rerun/`, with
`ACS_OUT_DIR=<scratch>/out ACS_MEMO=0`:

| Instrument | Wall time | Floats differing from committed JSON | Maximum relative difference | Non-float differences |
|---|---|---|---|---|
| `palpha_overlap_throat.py` | 0.63 s | 77 | 3.4e-13 | 0 |
| `palpha_overlap_refined.py` | 1.13 s | 517 | 1.31e-10 | 1: the `utc` stamp |

For Throat, two further near-zero values differ by at most 6.3e-17 absolute. For Refined,
six differ by at most 3.3e-16 absolute. The committed Refined `utc` stamp is
`2026-07-23T13:25:01.895032+00:00`.

**What a run log is.** Each script writes a run log built from a header and a markdown
table of the same result (`palpha_overlap_throat.py:508-521`). So the computation and its
log can be regenerated by anyone.

**Missing.** Only the original July log files, as provenance. They are on the author's
machine. The `.tex` sentences remain true either way, and they are manifest-bound.

**On arrival, or by decision.** One of:

- commit the original logs under `docs/palpha_overlap/*_logs/`;
- commit today-style rerun logs, labelled as reruns, beside the unchanged JSON.

### DAW canvases

**Missing.** `density-engine.canvas.tsx`, `eigen-path-daw.canvas.tsx`, the
`Aiso_build_artifacts/eigen_path_daw_viz/` tree (including `_canvas_template.tsx` and
`build_canvas.py`, per `BUGFIX_LOG.md:53,72-73`) and the workspace's package lock. They
come from the author's authoring machine.

None of these paths exist under `/home/user` (*measured*: `find`).

**On arrival.** Commit them under `visualizations/`, or publish them and link the URL.
Rerun `npm run typecheck`, which is `BUGFIX_LOG.md:14`'s check.

### Primary CPF sources

`docs/condensate_energy/endpoint_audit/source-snapshots/` holds `CPF-recovered-0.tex`,
`CPF-recovered-1.tex`, `mac02_soldering.py`, `newton_colour_music-1.py` and others. These
are recovered payloads ("Two recovered payloads are byte-identical", `README.md:131-132`),
and their hashes are in `receipt.json`.

**Missing.** The author's ruling on whether the recovered text is the primary source, or
the original file if it is not. This is an author decision, not a computation.

### Appendix B script

This one is present: `code/acs_codebase/extras/lemma29_verify.py`. Its link into
`papers/Form_Function_and_Asymmetry.tex` is already proposed as row 12 of
[proposed amendments](proposed_amendments_2026-10-22.md).

---

## 6. K02 training corpus and run identities; the "Croft" source (idx 98)

**Source.** The candidate cites `docs/frontier/2026-09-12-source-delta/README.md`. That
file says (`:11`): "Training source is present, but the declared corpora, run artifacts,
Merkle-memory file, and comparison script are absent from this revision; exact paths are
recorded in the source map."

The K02 wording is in `Research_Queue.json`:

- `:24`: "K02: acquire declared private training corpus and run identities before
  validating benchmark or deployment claims"
- `:1797-1831`: `current_status` "partial_training_source_mapped_private_claim_inputs_missing".
  Its `continuation_condition` is: "Supply or locate the declared corpus/run manifests and
  corresponding implementation revision, then audit train/test separation and replay the
  actual benchmark. Do not replace those claims with a synthetic training demonstration."

**Measured today.** The seven declared inputs are each ABSENT from this checkout
(`test -e`):

| Path | Declared at |
|---|---|
| `harness/fixtures/training/mmlu_train.jsonl` | `train_unified_phase1.py:406` |
| `harness/fixtures/training/mmlu_test.jsonl` | `:411` |
| `harness/fixtures/training/gsm8k_train.jsonl` | `:416` |
| `harness/fixtures/training/gsm8k_test.jsonl` | `:421` |
| `harness/reports/upg/upg_merkle_tensor_scroll.current.json` | `:577` |
| `harness/reports/training/gsm_merged_telemetry_x50.jsonl` | `run_phase1_phase_d_telemetry_sweep.sh:23` |
| `harness/training/compare_runs.py` | `run_phase1_tune_batch.sh:20` |

**Missing.** From the author:

- the seven files;
- the run manifests (seeds, `report.json` per run);
- the implementation revision that produced the claimed numbers.

**Form.** The files at those paths, or a private store plus a sha256 manifest committed
here, with the train/test provenance of each corpus.

**On arrival.**

- Audit train/test separation (for example, MMLU train/test overlap).
- Replay `run_phase1_tune_batch.sh` and `compare_runs.py`.
- Compare against the claims, as the continuation condition requires.

**"Croft".** The source is `Research_Queue.json:2959-2972` (NS01): "Croft Adams is a
documented candidate; no matching citation occurs in the supplied corpus and user intent
is not established." The continuation condition is: "Provide the author, title, link or
passage intended by Croft". The citation must come from the author.

---

## 7. Q2 matched-f64 benchmark (idx 106)

**Source.** `docs/Elimination_Ledger.md`:

- `:346-347`: "*trinity-wasm* = a private codebase whose benchmark inputs are not vendored
  here; the Q2 bench is therefore externally-verified-only."
- `:354-357`: "the bench is BRA-**f64** vs TF-**f32** […] "competitive at matched f64" →
  untested, plausibly par".
- `:328`: the need, "`bra_*` kernel signatures + the TF op it replaces (native rlib
  bench)".
- `:344-345`: "*W2F* = the external session's working-to-file log; not committed to this
  repository."

**New fact (measured today).** The kernel source is vendored, though not in this
repository. AISO-UI-for-Ai tracks `trinity-wasm/src/lib.rs`, which defines
`pub fn bra_render(...)` at `:148` and `pub fn bra_energy(samples: &[f64])` at `:170`. It
was first committed in `5000747` on 2026-07-24, after the ledger's 2026-06-06 OOS01
entry.

Three caveats about this source:

- Its `Cargo.toml` declares `license = "Proprietary (SIP License v1.1)"`.
- Its release profile is `opt-level = "s"` (size), which matters for timing.
- Its header cites a `tests/determinism.rs` that is not present (`trinity-wasm/` holds
  only `src/lib.rs`).

The TF op it replaces is written out in the ledger (`:351`): "`exp(-dt²/2w²)·exp(2πi f
dt)` (f32)".

**Toolchain check.** `cargo 1.97.0` is present. TensorFlow is not: `import tensorflow`
gives `ModuleNotFoundError` in both the pinned and the system Python.

**Missing.**

1. The OOS01 bench harness and its W2F log, from the author. Without them, a new run
   cannot be compared like-for-like with "1.37–1.82× SLOWER" (`:352-353`).
2. The kernel revision that OOS01 benchmarked, from the author. It may differ from
   `5000747`.
3. TensorFlow, at a pinned version, in a pinned environment. This is setup work, not an
   input.
4. An owner decision on whether a fresh bench with a RECONSTRUCTED harness may move Q2
   off "untested".

**On arrival.** A criterion bench of `bra_render` against the TF op, f64 against f64, at
N = 16…1024 on one machine. It reports the ratio per N.

---

## 8. Sealed Yang–Mills prediction set never scored (idx 107)

**Source.** `docs/PARALLEL_YM_SEALED_20260704.md` is 47 lines long:

- predictions C1–C6 at `:11-34`;
- contaminated X1–X2 at `:37-41`;
- the protocol at `:43-47`: "Map each C1-C6 to his lemma structure; score MATCH / PARTIAL
  / MISS with cites; clean-set score = the landed-same-spot determination; X-set logged
  but excluded."

The file has no result section. The candidate list's quotation "No scoring,
MATCH/PARTIAL/MISS result, or arrival of the external construction is recorded" does not
occur in either repository; it is the candidate list's own summary. `docs/README.md:60`
places the companion methodology paper "outside the 35-paper canonical publication
inventory and its build job."

**What the checker does.** `scripts/ym_comparison_checker.py` is not manifest-bound.

- It holds a keyword table per prediction (`:18-67`): `must_have` and `should_have`
  terms.
- It slides 150-word windows with step 50 over the target text (`:137-138`, loop at
  `:149`), and scores each window as 0.6 × (must fraction) + 0.4 × (should fraction)
  (`:161`).
- It calls a score ≥ 0.7 MATCH and ≥ 0.25 PARTIAL (`:176-179`).
- `--sealed_spec` is parsed (`:237`) and never read.
- The default `--output` is `docs/YM_COMPARISON_REPORT.md` (`:238`), a tracked path.
- A PDF target triggers a `pip install pypdf` at run time (`:70-79`).

**The K03 defect as recorded.** `docs/frontier/2026-09-12-source-delta/Research_Queue.json:1843`:
"The actual unchanged available checker gives MATCH=1.0 to both affirmative and
explicitly negated fixtures for all eight predictions, misses a complete final-window
fixture, and never uses its parsed sealed_spec argument."

**Re-measured today.** The fixtures were written to `scratchpad/actionable2/bn-ym-check/`,
with `--output` set to scratch:

| Fixture | Result |
|---|---|
| affirmative, 125 words | 8 MATCH |
| explicitly negated, 178 words | C1–C6 all MATCH (C3 86.7%, C6 80.0%); X1 PARTIAL 30%; X2 MISS |
| 300 neutral words, then the C4 cluster (317 words) | C4 MISS 0% |
| the C4 cluster, then 300 neutral words | C4 MATCH 100% |

The X2 MISS in the negated case is the final-window defect again, not negation
awareness. For 178 words the window loop visits only index 0, covering words 0–149, and
"AQFT" sits at word 173.

**A fourth defect, not in K03.** The `Totals` line counts X1/X2 together with C1–C6 (the
affirmative report says "8 MATCHES"). The protocol says the X-set is "logged but
excluded" (`:45`).

**Missing.** The external construction itself ("Graviton's construction", `:5`), from its
author through the owner. The form is given by K03's `continuation_condition`: "Supply
the full external proof, theorem statement, hypotheses and dependencies."

**On arrival.** The scoring is a human, lemma-level mapping of C1–C6 with cites. The
checker can at most point to candidate passages. Its four defects mean that a keyword
MATCH says nothing about agreement.

---

## 9. computational-tensegrity `paper/` directory (idx 115): reclassified as an owner decision

**Source.** `/home/user/AISO-UI-for-Ai/docs/research/ACS_PAPER_AMENDMENTS_2026-10-21.md:584-591`:
"The repository contains **no `paper/` directory** — only the macOS AppleDouble stubs
[…] So the CI workflow cannot be passing, and the paper text referenced by the README is
not public. Not amendable from here — it needs the files."

**Correction to the first-pass reading.** The first-pass verdict said the single commit
`6fbbec9` has "no parent". In fact the local clone is shallow:

- `.git/shallow` lists `6fbbec9`;
- `git cat-file -p HEAD` shows `parent f93a195bcf6bdd5b674443e5db5076839678bb15`;
- the local `git rev-list --count HEAD` of 1 is the shallow depth, not the history.

**Measured today, read-only through the GitHub API; nothing was fetched or restored.**

- Commit `6fbbec9` ("Delete paper directory", Brad Wallace, 2026-03-09) removed
  `paper/Computational_Tensegrity_Wallace_2026.tex` (541 lines),
  `paper/Computational_Tensegrity_Wallace_2026.pdf`, and two AppleDouble sidecars.
- At `f93a195`, `paper/` holds the `.tex` (48,827 bytes, blob `f7238442…`) and the `.pdf`
  (854,268 bytes, blob `4145dc84…`).
- `.github/workflows/build-paper.yml` builds `root_file: Computational_Tensegrity_Wallace_2026.tex`
  in `working_directory: paper`. That is the same file name.
- A second copy probably exists. `archive-coverage.json:66,70` lists
  `computational-tensegrity (1).tar.gz!computational-tensegrity/paper/._Computational_Tensegrity_Wallace_2026.pdf`
  sidecars. `:104` says the paired primary documents "were covered by the document pass".

**Missing.** No file is missing. The owner deleted `paper/` deliberately, so restoring it
is the owner's choice.

**The options.**

| Option | Cost | Consequence |
|---|---|---|
| Restore `paper/` from `f93a195` (`git revert 6fbbec9`) | One commit | CI can build again; the paper text becomes visible at HEAD |
| Keep it deleted | One commit | Remove the `cd paper` steps from the workflow and the README's `paper/` promise, so CI stops failing on a missing directory |

Neither option was taken here. Repository visibility was not checked.

**On decision.** The §6 amendment in AISO-UI-for-Ai can then be written against real
text.

---

## 10. The counting-deviation witness definition (idx 116)

**Source.**

- `papers/methodology/Spectral_Rigidity_Shuffle_Knife.tex:79`: "the remaining four are
  computed on unfolded spacings".
- `:89`: "counting deviation & $1\times10^{-5}$ & $1\times10^{-5}$ & $1.0$ & FORM". No
  formula is given anywhere in the paper.
- `GLOSSARY.md:699` names "counting deviation" but does not define it.
- `ACS_PAPER_AMENDMENTS_2026-10-21.md:277-281` (AISO-UI-for-Ai): "it likely belongs in the
  FORM_EXACT tier too. I do not have its definition and am not claiming a discrepancy."

**What changed today.** Commit `4f3f28d` added `code/hp_knife_suite/ff06e_headline.py`.
At `:65-66` it reads the witness as a RECONSTRUCTED `abs(len(gam) - w[-1]) / len(gam)`,
that is |N − N̄(γ_N)| / N.

**Measured today.**

```
python code/hp_knife_suite/ff06e_headline.py --n 100000
```

It ran in 1.97 s, with 60 surrogates and seed 20260423. The counting row gives:

| Quantity | Value |
|---|---|
| W_real | 5.9491e-06 |
| W_shuf | 5.9491e-06 |
| σ | 3.922e-15 |
| Driver's flag | "float floor" |

**What that measurement does and does not show.** Printed at five decimal places,
5.9491e-06 is 0.00001. So the paper's "$1\times10^{-5}$" does not exclude this reading,
and it does not confirm it either. The table prints the spacing-mean row at four places
("0.0000"), so the rounding rule is unknown.

**Missing.** From the author, via the FF06e manuscript source or its generating script:

- the formula;
- which sequence it acts on (raw or unfolded);
- its normalisation;
- the rounding used in the table.

The concurrent FF06e block in
[pass-2 amendments](proposed_amendments_2026-10-22_pass2.md) reports the same 5.9491e-06
and also leaves the witness unclassified. [REPRODUCTION](REPRODUCTION.md) (`f7e688c`)
names the original suite as `Math-grav-shared/scripts/knife_2x2.py`, which is not in this
repository. That file is the concrete form the definition could arrive in.

**On arrival.**

- Replace the RECONSTRUCTED line in `ff06e_headline.py` with the author's formula.
- Tier the witness on the four-tier scheme. Its surrogate σ at the float floor would put
  it in FORM_EXACT.
- Settle whether the dagger note's suspicion holds.

---

## 11. FeynRules/UFO export (idx 24): scope only, not started

**Source.**

- `code/acs_codebase/README.md:122`: "**No FeynRules/UFO model.** Paper A's Lagrangian is
  specified in standard PS form (see `extras/task2_lagrangian.py` and
  `extras/task_D_lagrangian.py`) but has not been exported to FeynRules. This is Phase D1
  of the roadmap — estimated 1-2 months of postdoc work."
- `docs/ACS_Corpus_Map.md:139` (O-2): "FeynRules/UFO export | engineering | LHC-testable
  predictions".
- `docs/ACS_Master_Index.md:151` (item 16).
- `code/acs_codebase/extras/task2_lagrangian.py:306-313`: "I have NOT run FeynRules in
  this session."
- The adjudication is [A-16 and B-O-2](adjudication_2026-10-22.md).

**Inputs in the repository.**

- The Lagrangian, as printed text in `extras/task_D_lagrangian.py` (four sectors: gravity,
  gauge, Higgs, fermion) and `extras/task2_lagrangian.py`. It is a printed string, not a
  machine-readable model.
- The 17-quartic coefficient vector of the complete scalar sector, in
  `code/condensate_energy/radiative_flat_modes.py:38-39` (`lam = [0] * 17`).
- No FeynRules, UFO, SARAH or MadGraph tooling: the five files that mention them are prose.

**The obstruction the record states.** The coefficients are not fixed: "The complete
scalar action and physical vacuum still require coefficients, kinetic normalization and a
selection rule". This is quoted at `ACS_Master_Index.md:171-174`, from `amendments.json`.
So any export is a parametric model, and "LHC-testable predictions" need values the
record does not have.

FeynRules also needs Mathematica, a licensed external tool. Writing UFO's Python files
directly avoids that dependency.

**First milestone.** A machine-readable model spec in a new module beside
`code/acs_codebase/src/paper_a/` (which already holds `betac_tan_beta.py`,
`branch_a_vacuum.py` and others). It would contain:

- the gauge group SU(4)×SU(2)_L×SU(2)_R;
- each field's representation and charges;
- the parameter list, naming the 17 quartics as `radiative_flat_modes.py` does.

It would come with tests that gauge anomalies cancel and that hypercharge reproduces the
Standard Model charges. A UFO export of the gauge and fermion sectors only would follow,
leaving the scalar potential symbolic.

It extends `src/paper_a` and `extras/task_D_lagrangian.py`. The whole effort estimate (1–2
months) is the record's. This pass does not re-estimate it.

---

## 12. Coleman–Weinberg analysis (idx 72): scope only, not started

**Source.**

- `code/acs_codebase/README.md:124`: "**No Coleman-Weinberg analysis.** The β_c → tan β
  analysis is tree-level only. Whether one-loop CW corrections fix tan β uniquely is open.
  Estimated 2-4 weeks of focused symbolic work."
- `docs/PaperA_changelog.md:161-164`.

**Reframing already on record.** `docs/ACS_Master_Index.md:150,157-180` records the
question as posed ("6 → 5") as "**superseded as posed, not open**". At tree level, in the
minimal bi-doublet, tan β is gauge-protected; this is T4 in `MANIFEST.md:63`. The input
count was retired by the 17-quartic record. The live question is narrower: "Whether
radiative corrections select tan β in the complete 17-quartic action is a different
question; the record supplies no selector for it".

**What already exists.**

| File | What it does |
|---|---|
| `code/acs_codebase/src/paper_a/betac_tan_beta.py` (68 lines) | Tree-level extremisation: tan β = ±1 |
| `extras/phase51_tanbeta.py:273` | Prints a "COLEMAN-WEINBERG SKELETON" |
| `code/condensate_energy/radiative_flat_modes.py:106,114,119` | One-loop machinery on flat directions: `cw_sum`, `cw_angular`, `analytic_curvature` |

`radiative_flat_modes.py` writes into `docs/condensate_energy/radiative_flat_modes` (`:22`)
and is manifest-bound. It must be run from a scratch copy, or extended in a new module
that imports it.

**First milestone.** A new module that imports `cw_angular`. It would:

- treat the bi-doublet angle β as a flat direction of the 17-quartic potential;
- supply W_R, Z_R and fermion masses as functions of β;
- report the sign of the one-loop curvature at β = π/4 against the boundary.

The couplings g4 and gR, and the Yukawa inputs, are unfixed, so the deliverable is a scan
with its parameter ranges declared in advance. It is not a selection result. The record's
estimate for the whole is 2–4 weeks.

---

## What this page leaves out

- The other ten PDE-style programs (idx 30a) were not run.
- No TensorFlow install was attempted (idx 106).
- No restoration or fetch was made in computational-tensegrity (idx 115).
- No password guessing or archive cracking was attempted (idx 31).
- No sample UFO export or CW scan was started (idx 24, 72).
- The candidate idx 33 is labelled "work" in the candidate list. It is treated here as
  blocked, because every input is on the author's drive.
