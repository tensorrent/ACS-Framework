> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# Visualizations

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
