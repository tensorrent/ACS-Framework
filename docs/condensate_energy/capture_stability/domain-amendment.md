# Supplemental domain check — registered after the first boundary failure

The initial analytic bound-mode control has three modes. The third has
exterior decay rate kappa=0.2063120570, an amplitude decay length of about4.85.
At dx0.05 the domain20 versus domain40 eigenvalue difference is
0.0001161001233, exceeding the original 1e-5 boundary tolerance. The coarse/fine
convergence to the analytic continuum roots and the independent dynamic ODE
checks passed. This is a finite-box sensitivity, not evidence against the
analytic exponential bound-state solution.

Keep the initial source, protocol, raw failed check and all dynamic cases.
Run a separate spectral check on domains40 and60 at both original resolutions.
Require the same 1e-5 boundary tolerance. Also require the same analytic matching
residual <1e-9 and fine-grid eigenvalue error <0.005 with decreasing error.
No threshold is relaxed. No dynamic case is changed or rerun by this supplement.

The final report must distinguish the original failed check from its expanded
domain replacement. The original experiment script remains reproducible under
its original protocol; this supplement completes its boundary qualification.
