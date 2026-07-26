> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Visualizations

## `mobius_screw_framing_transformer.html`

Interactive walkthrough of the framing transformer — companion to
[`../papers/notes/Framing_Transformer_Spin_Parity.tex`](../papers/notes/Framing_Transformer_Spin_Parity.tex).
Open it directly in a browser.

Five plates, one per stage of the chain `γ → U → Sl = Tw + Wr → F: S¹→SO(3) → q: S¹→SU(2)`:

1. **The shape** — the (2,1) torus curve with its ribbon, drag to rotate. The two
   ribbon faces are coloured separately so the strip's two-sidedness is visible;
   the moving triad shows T, U, and T×U. The **Throat** button sweeps a/R → 1,
   carrying the donut continuously into the funnel-with-a-throat of the tornado
   reading (Appendix A of the Möbius-screw note) — the closest approach to the
   axis is `ρ_min = R − a`, so the throat closes as a → R.
2. **Călugăreanu** — drag the aspect ratio and watch `Tw` and `Wr` trade against
   each other while `Tw + Wr` stays pinned at −2, all the way from a fat-hole
   donut to a closed funnel. This is the point that only the sum is a topological
   invariant — and that donut and vortex are the same framed loop.
3. **The lift** — the quaternion components across one circuit, landing on −1.
4. **The parity law** — step the framing twists `n` on a round circle and watch σ
   flip on every increment. The `n = 0` row is the one that kills `Sl = 2 ↔ g = 2`.
5. **Verdict** — what is falsified (T4) and what survives.

**Self-contained**: no CDN, no webfonts, no network requests of any kind. Every
number is computed in-browser from the same formulas as
[`../code/framed_unknot/framing_transformer.py`](../code/framed_unknot/framing_transformer.py)
and agrees with it to six decimals (twist −1.033761, writhe −0.966239, sum
−2.000000, and the full σ parity column). The writhe is a live Gauss double
integral over 300 samples, not a lookup — the invariance you see is computed, not
asserted.

## `acs_q_plane_confinement_simulator.html`

Interactive 3D visualiser for the Q-plane confinement picture. Open it directly
in a browser — no build step.

**Requires network access.** The page loads `three.js` 0.128 and `OrbitControls`
from `unpkg.com` via an import map (lines 8–11 and 225). Offline, or behind a
content-security policy that blocks third-party scripts, it renders blank. To
make it self-contained, vendor `three.module.js` and `OrbitControls.js` next to
the HTML and rewrite the import map to relative paths.

This is an illustrative visualiser, not a verification artifact: nothing in
[`../MANIFEST.md`](../MANIFEST.md) depends on it, and it computes no tiered
claim.
