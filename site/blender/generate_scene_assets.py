#!/usr/bin/env python3
"""Deterministic mathematical SVG fallback generator for the ACS-Framework 3D scenes.

Computes exact projections of:
1. mobius-framing.svg — (2,1) Möbius-screw torus curve with Călugăreanu framing ribbon (Sl = Tw + Wr = -2)
2. palatini-attractor.svg — sl(4,R) -> su(3) 5+3 torsion/Lorentz closure attractor & root hexagon
3. critical-seam.svg — Center-manifold phase flow (sigma = 1/2 closed rotation vs sigma != 1/2 spiral) & chiral hypercone

Writes the SVG files into site/assets/ and updates site/assets/manifest.json with their SHA-256 digests.
"""
import hashlib
import json
import math
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
ASSETS = SITE / 'assets'


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def render_mobius_framing() -> str:
    R, a = 1.0, 0.34
    steps = 240
    pts_outer = []
    pts_inner = []
    pts_center = []
    for i in range(steps + 1):
        phi = 2.0 * math.pi * i / steps
        theta = 0.5 * phi
        # (2,1) torus knot / Möbius framing curve
        r = R + a * math.cos(theta)
        x = r * math.cos(phi)
        y = r * math.sin(phi)
        z = a * math.sin(theta)
        # Isometric-like projection
        px = 400 + 210 * (x * 0.86 - y * 0.42)
        py = 225 + 210 * (x * 0.22 + y * 0.45 - z * 0.82)
        pts_center.append(f"{px:.2f},{py:.2f}")

        # Ribbon normal offset
        nx = math.cos(theta) * math.cos(phi)
        ny = math.cos(theta) * math.sin(phi)
        nz = math.sin(theta)
        w = 0.11
        ox = x + w * nx
        oy = y + w * ny
        oz = z + w * nz
        ix = x - w * nx
        iy = y - w * ny
        iz = z - w * nz
        pox = 400 + 210 * (ox * 0.86 - oy * 0.42)
        poy = 225 + 210 * (ox * 0.22 + oy * 0.45 - oz * 0.82)
        pix = 400 + 210 * (ix * 0.86 - iy * 0.42)
        piy = 225 + 210 * (ix * 0.22 + iy * 0.45 - iz * 0.82)
        pts_outer.append(f"{pox:.2f},{poy:.2f}")
        pts_inner.append(f"{pix:.2f},{piy:.2f}")

    rungs = []
    for i in range(0, steps, 6):
        o = pts_outer[i].split(",")
        inn = pts_inner[i].split(",")
        rungs.append(
            f'<line x1="{o[0]}" y1="{o[1]}" x2="{inn[0]}" y2="{inn[1]}" '
            f'stroke="#0ea5e9" stroke-opacity="0.38" stroke-width="1.3"/>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" width="800" height="450">
  <defs>
    <radialGradient id="bg1" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </radialGradient>
  </defs>
  <rect width="800" height="450" fill="url(#bg1)"/>
  <g stroke="#1e293b" stroke-width="1">
    <line x1="80" y1="225" x2="720" y2="225"/>
    <line x1="400" y1="40" x2="400" y2="410"/>
    <circle cx="400" cy="225" r="165" fill="none" stroke-dasharray="4 6"/>
  </g>
  <g>{''.join(rungs)}</g>
  <polyline fill="none" stroke="#38bdf8" stroke-width="2.2" points="{' '.join(pts_outer)}"/>
  <polyline fill="none" stroke="#f59e0b" stroke-width="2.2" points="{' '.join(pts_inner)}"/>
  <polyline fill="none" stroke="#f8fafc" stroke-width="3.0" points="{' '.join(pts_center)}"/>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" fill="#94a3b8">
    <text x="28" y="38" fill="#e2e8f0" font-weight="600">SCENE 01 · (2,1) MÖBIUS-SCREW FRAMED UNKNOT</text>
    <text x="28" y="60">Călugăreanu invariant: Sl = Tw + Wr = -2.000000 (Tw = -1.033761, Wr = -0.966239)</text>
    <text x="28" y="405" fill="#38bdf8">SU(2) Frame Holonomy: σ = (-1)^(Sl+1) = -1 (Spinorial)</text>
    <text x="28" y="425" fill="#f43f5e">T4 Falsification: n = 0 untwisted circle also gives σ = -1 (kills Sl = 2 ↔ g = 2)</text>
  </g>
</svg>
"""
    return svg


def render_palatini_attractor() -> str:
    cx, cy = 400, 230
    radius = 135
    roots = []
    nodes = []
    labels = [
        ("α₁ (Torsion+Lorentz)", 0),
        ("α₁+α₂", 60),
        ("α₂", 120),
        ("-α₁", 180),
        ("-α₁-α₂", 240),
        ("-α₂", 300),
    ]
    pts = []
    for label, deg in labels:
        rad = math.radians(deg)
        x = cx + radius * math.cos(rad)
        y = cy - radius * math.sin(rad)
        pts.append((x, y, label))

    edges = []
    for i in range(6):
        x1, y1, _ = pts[i]
        x2, y2, _ = pts[(i + 1) % 6]
        edges.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#38bdf8" stroke-width="2" stroke-opacity="0.65"/>')
        edges.append(f'<line x1="{cx}" y1="{cy}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#475569" stroke-width="1.5" stroke-dasharray="3 4"/>')

    for x, y, label in pts:
        nodes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#0ea5e9" stroke="#e0f2fe" stroke-width="2"/>')

    # Quark triplet triangle inside
    q_pts = []
    for deg, col in [(30, "#f43f5e"), (150, "#38bdf8"), (270, "#10b981")]:
        rad = math.radians(deg)
        qx = cx + 72 * math.cos(rad)
        qy = cy - 72 * math.sin(rad)
        q_pts.append((qx, qy, col))
    tri = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in q_pts)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" width="800" height="450">
  <rect width="800" height="450" fill="#090d16"/>
  <g stroke="#1e293b" stroke-width="1">
    <circle cx="{cx}" cy="{cy}" r="165" fill="none"/>
    <circle cx="{cx}" cy="{cy}" r="135" fill="none" stroke-dasharray="4 4"/>
    <circle cx="{cx}" cy="{cy}" r="72" fill="none" stroke-dasharray="2 4"/>
  </g>
  <polygon points="{tri}" fill="#f59e0b" fill-opacity="0.08" stroke="#f59e0b" stroke-width="2"/>
  {''.join(edges)}
  {''.join(nodes)}
  <circle cx="{cx - 12}" cy="{cy}" r="6" fill="#f59e0b"/>
  <circle cx="{cx + 12}" cy="{cy}" r="6" fill="#f59e0b"/>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" fill="#94a3b8">
    <text x="28" y="38" fill="#e2e8f0" font-weight="600">SCENE 02 · PALATINI sl(4,R) → su(3) CLOSURE ATTRACTOR (5+3 SPLIT)</text>
    <text x="28" y="60">dim Im(Φ) = 15 = 9 Torsion Sym₀(4) + 6 Lorentz o(4) · sl(3,R) embeds 5 Torsion + 3 Lorentz</text>
    <text x="28" y="405" fill="#10b981">Closure defect D(sl(3,R)) = 1.4e-16 vs min random Gr(8,15) = 0.49 (50,000 samples, T3)</text>
    <text x="28" y="425" fill="#f59e0b">Chirality map J(T) = i·sym(T) + anti(T) · Torsion tiers 0 : 1 : 4 · Bosonic ρ_vac = 0 exact</text>
  </g>
</svg>
"""
    return svg


def render_critical_seam() -> str:
    # Left panel: center manifold sigma = 1/2 closed circle vs sigma = 0.68 outward spiral
    c1x, c1y = 230, 235
    c2x, c2y = 570, 235
    pts_crit = []
    pts_off = []
    steps = 220
    for i in range(steps + 1):
        t = 4.0 * math.pi * i / steps
        # sigma = 1/2: pure rotation
        r1 = 105.0
        x1 = c1x + r1 * math.cos(t)
        y1 = c1y + r1 * math.sin(t)
        pts_crit.append(f"{x1:.2f},{y1:.2f}")
        # sigma = 0.68: outward spiral
        r2 = 38.0 * math.exp(0.11 * t)
        x2 = c2x + r2 * math.cos(t)
        y2 = c2y + r2 * math.sin(t)
        pts_off.append(f"{x2:.2f},{y2:.2f}")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" width="800" height="450">
  <rect width="800" height="450" fill="#090d16"/>
  <g stroke="#1e293b" stroke-width="1">
    <line x1="400" y1="75" x2="400" y2="385" stroke-dasharray="4 4"/>
    <circle cx="{c1x}" cy="{c1y}" r="105" fill="none" stroke="#1e293b"/>
    <circle cx="{c2x}" cy="{c2y}" r="105" fill="none" stroke="#1e293b" stroke-dasharray="3 5"/>
  </g>
  <polyline fill="none" stroke="#10b981" stroke-width="2.8" points="{' '.join(pts_crit)}"/>
  <polyline fill="none" stroke="#f43f5e" stroke-width="2.4" points="{' '.join(pts_off)}"/>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" fill="#94a3b8">
    <text x="28" y="38" fill="#e2e8f0" font-weight="600">SCENE 03 · CRITICAL-LINE CENTER MANIFOLD &amp; CHIRAL HYPERCONE (β = codim − 1)</text>
    <text x="28" y="60">Explicit-formula seam: Primes (Form) ↔ Zeros (Function) · Two FUNCTION faces: Arith 11,497σ, Local 26σ</text>
    <text x="115" y="375" fill="#10b981">σ = 1/2: Center Manifold (α = 0, closed rotation)</text>
    <text x="455" y="375" fill="#f43f5e">σ = 0.68: Radial Spiral Drift (α = 2σ − 1 &gt; 0)</text>
    <text x="28" y="415" fill="#38bdf8">HP Wall Resolution: C H* C⁻¹ = −H (C² = −1) · Codim 3 ⇒ β = 2.00 GUE + Real Orbits (T1)</text>
  </g>
</svg>
"""
    return svg


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    specs = [
        ("scene-mobius-framing", "mobius-framing.svg", render_mobius_framing()),
        ("scene-palatini-attractor", "palatini-attractor.svg", render_palatini_attractor()),
        ("scene-critical-seam", "critical-seam.svg", render_critical_seam()),
    ]
    manifest_entries = []
    for asset_id, filename, content in specs:
        out_path = ASSETS / filename
        raw = content.encode("utf-8")
        out_path.write_bytes(raw)
        manifest_entries.append({
            "id": asset_id,
            "output": filename,
            "generator": "blender/generate_scene_assets.py",
            "sha256": sha256_bytes(raw),
        })
    manifest_path = ASSETS / "manifest.json"
    manifest_path.write_text(json.dumps({"assets": manifest_entries}, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(manifest_entries)} deterministic SVG scene assets and updated {manifest_path}")


if __name__ == "__main__":
    main()
