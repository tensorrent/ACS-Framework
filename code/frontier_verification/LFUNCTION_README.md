# Reproducing finite L-function zero certificates

The [L-function checkpoint](../../docs/frontier/2026-09-13-lfunction-delta/README.md) records the eight supplied L-function tables, corrected ordinates, separate conjugate spectra, complete interval transcripts, failed attempts and downstream replays. Install the pinned packages in [source_requirements.txt](source_requirements.txt). The recorded interval runtime is python-flint 0.9.0 with FLINT 3.6.0.

From this directory, a fresh certificate and a higher-precision replay can be produced with:

```sh
python lfunction_zero_certificate.py --character chi7 --output /path/to/new-certificates/chi7.json
python lfunction_certificate_replay.py /path/to/new-certificates/chi7.json --output /path/to/new-replays/chi7.json
```

For the faster audited mod-91 route, use `python lfunction_functional_backend.py certify --character chi_m91 --output /path/to/new-certificates/chi_m91.json`, then `python lfunction_functional_backend.py replay --character chi_m91 --certificate /path/to/new-certificates/chi_m91.json --output /path/to/new-replays/chi_m91.json`. It evaluates the left side through the primitive functional equation and retains direct-evaluation controls.

Repeat the direct commands for `chi5`, `chi5bar`, `chi7bar`, `chi_m35`, `chi_m91`, and `chi_m104`. The specified height cutoffs are 220 for the four complex characters, 80 for discriminant -35, 60 for -91, and 70 for -104. Computation can take several minutes per character. The original producer works at 160 bits; the replay uses 224 bits and may subdivide the contour further. Higher working precision can change interval overestimation and does not necessarily tighten an image for the same input interval.

For an offline reproduction using retained certificates, extract `Certificates.zip` and `Replays.zip` from the checkpoint. Extract the earlier source checkpoint's `Source_Snapshot.zip` only if reconstructing historical implementations; the audit below can read that ZIP directly.

```sh
python lfunction_data_audit.py --certificates /path/to/certificates --baseline ../../docs/frontier/2026-09-12-source-delta/Source_Snapshot.zip --output /path/to/data-audit.json
python lfunction_table_export.py --certificates /path/to/certificates --output-root /path/to/new-data
python lfunction_observable_delta.py --baseline ../../docs/frontier/2026-09-12-source-delta/Source_Snapshot.zip --data-root /path/to/new-data --output /path/to/observables.json
python verify_lfunction_delta.py
```

The exporter is deterministic and does not independently establish the validity of an arbitrary input certificate. Replay the certificate and verify its provenance before relying on exported data. Its manifest contains character IDs, certified rational intervals, height cutoffs and the 5e-21 absolute rounding bound. That bound describes the decimal text; loading it into float64 introduces further rounding. Use the intervals or decimal strings for shrinking-resolution calculations.

## Why the count establishes finite completeness

The intended characters are verified over every residue against independent cyclic-generator conventions or Kronecker symbols. All seven are primitive, odd and nonprincipal. Nonprincipal Dirichlet L-functions are entire; the Hurwitz representation and functional equation are given in [DLMF 25.15](https://dlmf.nist.gov/25.15). FLINT's [Dirichlet implementation](https://flintlib.org/doc/acb_dirichlet.html) defines the normalized Hardy Z function, which is real for real height and has the same critical-line zeros as L. The installed library version is recorded separately from the current online documentation.

1. A scan at spacing 1/10 proposes sign-change brackets. Each is refined to width below 1e-25 with strict, interval-certified opposite Hardy Z signs. The intermediate value theorem gives a critical-line zero in each disjoint bracket. A scan alone does not prove completeness.
2. The counterclockwise rectangle has real bounds -1/4 and 5/4 and height bounds -1/2 and T. For every accepted straight contour segment, an Arb rectangle encloses the image of the **whole segment** under L and excludes zero. Such a convex image rectangle lies in an open half-plane not containing zero, so the image path has a continuous argument with variation between endpoints in (-pi, pi).
3. The endpoint quotient has strictly positive real part. Its principal argument therefore agrees with that continuous argument increment and has magnitude less than pi/2. Summing enclosing argument intervals and dividing by 2*pi gives an interval containing a unique integer. The argument principle identifies that integer with the number of zeros inside the rectangle, counting multiplicity; there are no poles.
4. The count equals the number of disjoint sign-change brackets. Consequently every bracket contains exactly one simple zero, and there are no other zeros anywhere inside that finite rectangle. No assertion about unbounded height follows. The rectangle also excludes any extra real or slightly negative-height roots in its interior by the same count comparison.

The replay checks the exact rational contour coverage and orientation, recomputes every whole-segment image, and repeats all root signs and the total count. Its refined transcript stores interval midpoints and radii as exact dyadic mantissa/exponent pairs. The producer's decimal ball displays can widen on formatting and are informational; replay uses rational input segments. Both interval passes trust FLINT/Arb. The 65-digit mpmath checks use independently built character values and a separate Hurwitz-zeta implementation for selected roots; they do not independently certify completeness. This argument is documented and executable, but is not formalized in Lean.

## Precision and conjugation corrections

A nonzero L-value at a printed decimal is normal for an approximate root. The data audit instead checks its entire displayed rounding cell, compares it with certified root intervals, and bounds its positional error. A cell whose interval L-image excludes zero cannot contain a root; an image containing zero is inconclusive unless the root bracket establishes existence. The complete list supplies another way to exclude a cell.

Absolute tolerances on the completed L-function are unsuitable as a sole root-location stopping rule because its gamma factor becomes very small at large height. Strict sign brackets and positional width avoid that failure. The old extension script also could miss roots when scanning only Im(L); its output count was never a completeness certificate. The replacement generation entry point uses the certified method and requires an explicit output directory.

For a complex character, conjugation gives L(s, conjugate(chi)) = conjugate(L(conjugate(s), chi)). Thus positive zeros of the conjugate correspond to negative zeros of the original. The positive lists differ. A positive-height Dedekind witness must include both distinct lists under the same cutoff and weighting; doubling one list requires a separate argument and fails as a literal spectral identity. The historical synthesis's doubled-character numerical approximation is withdrawn pending a full recomputation of all factors.
