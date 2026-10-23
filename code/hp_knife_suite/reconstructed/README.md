# Reconstructed kill tests

[Code guide](../../README.md) · [Elimination Ledger](../../../docs/Elimination_Ledger.md) · [Reproduction](../../../docs/REPRODUCTION.md)

Eight 2026-06-06 kill-test scripts cited in the [Elimination Ledger](../../../docs/Elimination_Ledger.md)
were run on external session machines and never committed (ledger provenance note, lines 14–21).
Their verdicts rest on logged outputs. This directory holds re-authored versions of three of them,
so the logged numbers can be recomputed from repository content. It does not hold the originals.

## Provenance rule

- **Restored** means the original content survives at its original address, or at an address that
  says it is the same bytes (for example the `*_disp.py` display listings in
  `papers/later_FF06_series/`, which the Process Record calls "the canonical source listings").
- **Reconstructed** means the code was re-authored from a description. Every file here starts with
  `RECONSTRUCTED 2026-10-22 from the ledger's description, NOT the original`, cites the ledger lines
  it was built from, and lists the choices the ledger leaves open.

A reconstruction that agrees with the ledger shows that the recorded numbers can be recomputed by a
method matching the ledger's description. It does not show what the original script computed, and it
does not change the ledger's evidence standard for the original entry. Re-labelling is the owner's call.

All three scripts use seed `20260423`, write nothing, and print to stdout only.

## Selection

The three scripts chosen are the ones whose ledger entries state both the method and the output
numbers most completely, so that a mismatch would carry information:

| Script | Ledger lines | Why chosen |
|---|---|---|
| `q3_scaling_test_reconstructed.py` | 428–456 (plus FF06 paper `The_Elimination_Ledger.tex:485-488` for the zero-finder) | Full table: floors, counts, first zeros; formulas written out |
| `q7_neutrino_reconstructed.py` | 285–303 | Every input and output stated |
| `q5_hp_reconstructed.py` | 207–235 | Data window, unfolding, and four outputs fully determined by the stated method; the L2 and β outputs are under-specified |

## How to run

```sh
python code/hp_knife_suite/reconstructed/q3_scaling_test_reconstructed.py   # ~55 s (mpmath)
python code/hp_knife_suite/reconstructed/q7_neutrino_reconstructed.py       # <1 s
python code/hp_knife_suite/reconstructed/q5_hp_reconstructed.py             # ~3 s
python code/hp_knife_suite/reconstructed/q5_hp_reconstructed.py --scan      # post-hoc L2 convention sweep
```

The 2026-10-22 runs used the pinned environment (`mpmath 1.3.0`, `numpy 2.2.6`, `scipy 1.15.3`).

## Agreement with the ledger, cell by cell (2026-10-22 run)

### Q3 (d,q) scaling law: ledger lines 438–449. 14 of 14 cells agree.

| Cell | Ledger | Reconstruction | Agree |
|---|---|---|---|
| L(χ₋₄) framework floor / standard floor | 4.27 / 4.27 | 4.2699 / 4.2699 | yes |
| L(χ₋₄) N_actual at floor / first zero | 0 / 6.02 | 0 / 6.020949 | yes |
| L(χ₋₃) framework floor / standard floor | 5.69 / 5.69 | 5.6932 / 5.6932 | yes |
| L(χ₋₃) N_actual at floor / first zero | 0 / 8.04 | 0 / 8.039737 | yes |
| Dedekind ζ Q(i) framework / standard floor | 72.93 / 8.54 | 72.9271 / 8.5397 | yes |
| Dedekind ζ Q(i) N_actual at 72.93 | 51 | 51 (18 ζ + 33 L(χ₋₄)) | yes |
| framework count at 72.93 | ≈0 | 0 (prints −0.000000) | yes |
| standard count at 72.93 | ~50 | 49.7865 | yes |
| overshoot factor | ~8.5× | 8.5397 | yes |

Two methods check the counts. The ζ count is 18 by `mpmath.zetazero` and 18 by the committed table
`../data_zeros/riemann_zeros_100k.txt`. The L(χ₋₄) count is 33 by Hardy-Z sign changes and 33.0000 by
the argument principle. The ledger's row "L(χ₃)" is the odd character mod 3 (χ₋₃). Its first zero,
8.039737, confirms that reading.

### Q7 neutrino seesaw / X-ray: ledger line 291. 3 of 3 cells agree.

| Cell | Ledger | Reconstruction | Agree |
|---|---|---|---|
| required suppression S | < 2.5×10⁻⁵ | < 2.5000×10⁻⁵ | yes |
| M_WR | ≳ 16 TeV | > 16.0800 TeV | yes |
| v_R | ≳ 49 TeV | > 49.2440 TeV (assuming v_R = v·M_WR/M_W) | yes |

Two quantitative sentences in the entry (lines 291–293) are **not** supported as written, at the
ledger's own inputs:

- "LHC ~5–6 TeV … already exceed this". The script prints `False` for both 5 and 6 TeV against
  the required 16.08 TeV. Only the rare-decay bound on v_R ("≳100s TeV") could exceed the requirement.
  This directory does not verify that bound.
- "clears the X-ray bound by orders of magnitude for any realistic v_R". The margin is
  (v_R / 49.24 TeV)². It is 4.12× at v_R = 100 TeV, 37.11× at 300 TeV and 412.38× at 1000 TeV.
  Two orders of magnitude needs v_R ≥ 492.44 TeV.

The SURVIVES verdict ("the X-ray bound is no obstruction") therefore rests on v_R ≳ 49 TeV being
established independently. These findings are listed here and the ledger is left unchanged, because
the ledger is append-only and its amendments are the owner's to make.

### Q5 Hilbert–Pólya class test: ledger lines 215–217 and 224–226. 4 of 4 determined cells agree; 5 method-dependent cells approximate.

Reading A (zero indices 10000–40000) is the default. Reading B (heights 10⁴–4×10⁴) is printed alongside.

| Cell | Ledger | Reconstruction | Agree |
|---|---|---|---|
| spacing variance | 0.1600 | 0.1600 (A); 0.1603 (B) | yes (A) |
| xp ratio, T = 10³ | 0.998 | 0.998060 | yes |
| xp ratio, T = 10⁴ | 1.00001 | 1.000009 | yes |
| xp ratio, T = 5×10⁴ | 0.99998 | 0.999983 | yes |
| L2 to GUE | 7.31×10⁻² | 6.382×10⁻² (A, bin 0.05) | **no**: method-dependent, see below |
| L2 to GSE | 1.72×10⁻¹ | 1.692×10⁻¹ | approximately |
| L2 to GOE | 2.26×10⁻¹ | 2.230×10⁻¹ | approximately |
| L2 to Poisson | 6.52×10⁻¹ | 6.507×10⁻¹ | approximately |
| β (repulsion exponent) | 2.12 | 1.996 / 2.006 (A); 2.104 / 1.993 (B) | **no** exact match; all four estimates lie within 0.13 of 2.12 |

The variance matches only reading A, which suggests the window was a range of zero indices. The
ordering GUE ≪ GSE < GOE ≪ Poisson holds in the default output. That ordering is what supports the
class kills.

The `--scan` mode was written after the default output was seen, so it is post hoc. It sweeps 96
histogram conventions: window, bin width 0.02–0.20, range 3–4–5, normalisation, and bin-centre versus
bin-average. GSE, GOE and Poisson each have conventions that contain the ledger value. GUE spans
0.0494–0.0723 across the sweep, so the ledger's 0.0731 sits just above every convention tried. The
closest cell (A, bin 0.02, range 3, density over all spacings, bin centres) gives 0.0722 / 0.1712 /
0.2263 / 0.6517. The original L2 definition remains unknown. The GUE distance is about 2.5× the
GUE-surmise sampling noise floor: the median of 200 draws is 0.0251 for n = 30,000. The residual is
therefore systematic and not sampling noise. This is consistent with the data's variance of 0.1600
sitting below the surmise variance of 0.1781.

## Not reconstructed: what the owner must supply

Each "needs" line states what is missing, who holds it, in what form, and what it unlocks.

| Original | Ledger lines | Needs |
|---|---|---|
| `/tmp/q3_floor.py` | 157–181 | From the owner, the original file, or failing that the list of "sampled heights" and the `N_full` formula behind "0.13–0.59". Unlocks recomputing the T3 count-tracking cell from the committed 100k table. The 2πe identity is T2 and needs no script. |
| `/tmp/q6_offdiag.py` | 183–205 | From the owner, the original file, or the definition of "local baseline", the x-grid, and the Hann-taper argument. Unlocks recomputing the 3–4×10⁸ fundamental ratios and the 0.3–5.4 composite ratios from the first 3000 committed zeros. |
| `q4_cfunction_testbed.py` | 237–270 | From the owner, the original file: the c-function definition, the h values and L points behind "0.237→0.025→0", and the fit window for c = 0.508 (local 0.501). The ΔI side also needs the FF06Σ Link-3 ΔI definition (ledger line 330). |
| `/tmp/q4_largeL.py` | 272–283 | From the owner, the M = 400 fit window for c = 0.4884 and the L grid behind "h=1.02→0.001 by L=156". The validation gate (M=12, h=1.0/1.3, L=1/3/6, open chain) is fully stated and is the next reconstruction candidate without owner input. |
| `/tmp/q4_monotonicity.py` | 408–426 | From the owner, the MI/entropic c-function definition and L grid behind "critical 0.52→0.29", and the `all_mono` criterion (strict or not, tolerance). Shares the BdG instrument with `q4_largeL`. |

### FF06 series artifacts

These are cited in `papers/later_FF06_series/The_Reversible_Flattening_Process_Record.tex:600-615`
and `The_Geometry_Engine.tex:276-283`.

| Artifact | Needs |
|---|---|
| `verify_ledger.py` (14/14) | From the owner, confirmation that `verify_ledger_disp.py` and `shape_engine_disp.py` are the runnable originals, or the originals to diff against. In a scratch copy, renaming `shape_engine_disp.py` to `shape_engine.py` and running `verify_ledger_disp.py` printed `LEDGER: 14 EXACT, 0 FAIL`, so the count is executable from committed listings today. |
| `predictive_test.py` (30-domain) | The same confirmation for `predictive_test_disp.py`. A scratch run printed `PASS: 28/30 original, 30/30 corrected`. Whether its ground-truth column is computed or asserted was not checked. |
| Rust `shape_engine` crate (`cargo test` 8/8) and `verify.sh` (503-record diff) | From the owner, the crate source (`Cargo.toml`, `src/`, tests), `verify.sh`, and its 503-record reference file. Note that `The_Geometry_Engine.tex:276-278` says "no unverified Rust was produced" in its environment, whereas `Process_Record.tex:354` reports `cargo test 8/8`. The owner should say which engine and run each statement refers to. |
| `motif_test_suite.py`, `check2_gcd_overlap.py` | From the owner, both files and the fixed seeds "recorded with each result" (Process Record lines 601-602). AISO's `frontend/src/motif-memory.ts` cites `motif_test_suite.py --live`, and that file exists in neither repository. |
| Geometry-engine kill rounds (Mersenne-as-prime, single-deletion-as-primality, geometry-beats-division) | From the owner, the pre-registered test-round run artifacts that `The_Geometry_Engine.tex:282-283` says "predate this bundle and are not committed here". Unlocks recomputing three falsifications that are currently recorded only in prose. |
