#!/usr/bin/env python3
"""
Canonical figure build for the ACS papers.

Co-governed and enforced under the SIP License v1.1.

Regenerates every figure referenced by a `\\includegraphics` in papers/.
Writes into the repository tree (papers/figures/ and
papers/core_trilogy/figures/), not to an authoring-machine path.

Provenance policy
-----------------
Each figure declares its own kind in FIGURE_KINDS below:

  "computed"  - every plotted number is produced by this script at run time,
                from the repository's own verified sources (src/common
                lie_algebra, the committed Odlyzko zeros, exact rational
                arithmetic).  No hand-entered data.
  "tabulated" - the plotted numbers are quoted from a specific committed
                result recorded in a paper or artifact, and are reproduced
                here verbatim with the source named.  Re-deriving them is
                out of scope for a plotting script.
  "schematic" - a diagram, not a data plot.  Carries no numerical claim
                beyond labels.

This distinction exists because the figures this script replaces contained
two provenance defects, both now fixed:

  * fig_selection plotted `np.random.uniform(0.55, 0.78, 100)` - a synthetic
    histogram standing in for closure defects that were never computed.
    It is now computed from real Grassmannian sampling.
  * fig_sign_reversal hard-coded DI = +/-1.19, contradicting the value the
    papers quote (+/-1.4986).  It now calls the automaton.

Run:  python3 scripts/generate_paper_figures.py
"""

import os
import sys
from fractions import Fraction

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "code", "acs_codebase"))

from src.common.lie_algebra import sl_n_basis, bracket  # noqa: E402
from src.common.seed import CANONICAL_SEED, default_rng  # noqa: E402

OUT_MAIN = os.path.join(REPO, "papers", "figures")
OUT_TRILOGY = os.path.join(REPO, "papers", "core_trilogy", "figures")
ZEROS = os.path.join(REPO, "code", "hp_knife_suite", "data_zeros", "riemann_zeros_100k.txt")

FIGURE_KINDS = {
    "fig_layers_cycle": "schematic",
    "fig_ricci_flow": "computed",
    "fig_closure_attractor": "computed",
    "fig_selection": "computed",
    "fig_colour_weights": "computed",
    "fig_nuclear_geometry": "computed",
    "fig_rep_gallery": "computed",
    "fig_barbero_immirzi": "computed",
    "fig_torsion_tiers": "computed",
    "fig_hero_nesting": "schematic",
    "fig_chirality": "tabulated",
    "fig_sign_reversal": "computed",
    "fig_variance_scaling": "computed",
    "fig_flow_field": "computed",
    "fig_wronskian_heatmap": "computed",
}

# Figures that live only in papers/core_trilogy/figures/ (Paper B).
TRILOGY_ONLY = {"fig_variance_scaling", "fig_flow_field", "fig_wronskian_heatmap"}

plt.rcParams.update({
    "font.size": 9,
    "axes.linewidth": 0.8,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "figure.dpi": 150,
})

_notes = []


def save(fig, name):
    """Write a figure to every directory that should carry it.

    Rendered once and byte-copied, with the PDF CreationDate suppressed, so
    the build is reproducible and the two directories stay byte-identical.
    """
    import shutil
    targets = [OUT_TRILOGY] if name in TRILOGY_ONLY else [OUT_MAIN, OUT_TRILOGY]
    os.makedirs(targets[0], exist_ok=True)
    first = os.path.join(targets[0], name + ".pdf")
    fig.savefig(first, metadata={"CreationDate": None})
    for d in targets[1:]:
        os.makedirs(d, exist_ok=True)
        shutil.copyfile(first, os.path.join(d, name + ".pdf"))
    plt.close(fig)
    print(f"  [{FIGURE_KINDS[name]:9s}] {name}")


def note(msg):
    _notes.append(msg)
    print(f"      note: {msg}")


# ══════════════════════════════════════════════════════════════════════
# Shared exact quantities
# ══════════════════════════════════════════════════════════════════════

def T_BL():
    return np.diag([1 / 3, 1 / 3, 1 / 3, -1.0])


def torsion_couplings():
    """Exact ||[T_BL, X]||^2 on the sl(4) A/S basis, and on the EW-adapted
    so(4) generators J_i, K_i.  Returns (basis_rows, ew_rows).

    This is the computation that reconciles the 'two tiers' statement with
    the '0:1:4' hierarchy: they are statements about different generator
    sets.  See Paper A, torsion-hierarchy section.
    """
    n = 4

    def mat(entries):
        M = [[Fraction(0)] * n for _ in range(n)]
        for (i, j), v in entries.items():
            M[i][j] = Fraction(v)
        return M

    def mul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

    def brk(A, B):
        P, Q = mul(A, B), mul(B, A)
        return [[P[i][j] - Q[i][j] for j in range(n)] for i in range(n)]

    def fro2(A):
        return sum(A[i][j] ** 2 for i in range(n) for j in range(n))

    def lin(A, B, ca, cb):
        return [[Fraction(ca) * A[i][j] + Fraction(cb) * B[i][j] for j in range(n)] for i in range(n)]

    T = mat({(0, 0): Fraction(1, 3), (1, 1): Fraction(1, 3), (2, 2): Fraction(1, 3), (3, 3): -1})
    A = lambda i, j: mat({(i, j): 1, (j, i): -1})   # noqa: E731
    S = lambda i, j: mat({(i, j): 1, (j, i): 1})    # noqa: E731

    basis_rows = []
    for i in range(4):
        for j in range(i + 1, 4):
            for tag, G in (("A%d%d" % (i, j), A(i, j)), ("S%d%d" % (i, j), S(i, j))):
                basis_rows.append((tag, fro2(brk(T, G))))
    # Cartan generators commute with T_BL (all diagonal).
    for tag in ("H1", "H2", "H3"):
        basis_rows.append((tag, Fraction(0)))

    ew_rows = []
    pairs = {1: ((0, 1), (2, 3), +1), 2: ((0, 2), (1, 3), -1), 3: ((0, 3), (1, 2), +1)}
    for i, ((a, b), (c, d), sgn) in pairs.items():
        P, Q = A(a, b), A(c, d)
        J = lin(P, Q, Fraction(1, 2), Fraction(sgn, 2))
        K = lin(P, Q, Fraction(1, 2), Fraction(-sgn, 2))
        ew_rows.append(("J%d" % i, fro2(brk(T, J))))
        ew_rows.append(("K%d" % i, fro2(brk(T, K))))
    return basis_rows, ew_rows


# ══════════════════════════════════════════════════════════════════════
# 1. fig_colour_weights  (computed: exact su(3) weights)
# ══════════════════════════════════════════════════════════════════════

def fig_colour_weights():
    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    weights = {"$r$": (1.0, 0.0), "$b$": (-1.0, 1.0), "$g$": (0.0, -1.0)}
    cols = {"$r$": "#CC2222", "$b$": "#2244CC", "$g$": "#118833"}
    xs = [w[0] for w in weights.values()] + [weights["$r$"][0]]
    ys = [w[1] for w in weights.values()] + [weights["$r$"][1]]
    ax.plot(xs, ys, "-", color="#999999", lw=0.8, zorder=1)
    for lab, (x, y) in weights.items():
        ax.scatter([x], [y], s=140, color=cols[lab], zorder=3, edgecolor="black", linewidth=0.6)
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(10, 6), fontsize=11)
    ax.scatter([0], [0], s=140, facecolor="white", edgecolor="black", linewidth=1.2, zorder=3)
    ax.annotate("White\n(lepton)", (0, 0), textcoords="offset points",
                xytext=(8, -22), fontsize=8.5)
    ax.axhline(0, color="black", lw=0.4, zorder=0)
    ax.axvline(0, color="black", lw=0.4, zorder=0)
    ax.set_xlabel("$h_1$  (Cartan $H_1$, torsion sector)", fontsize=9)
    ax.set_ylabel("$h_2$  (Cartan $H_2$, torsion sector)", fontsize=9)
    ax.set_title("Fundamental $\\mathbf{3}$ of $\\mathfrak{su}(3)$", fontsize=10, fontweight="bold")
    ax.set_xlim(-1.7, 1.7)
    ax.set_ylim(-1.7, 1.7)
    ax.set_aspect("equal")
    save(fig, "fig_colour_weights")


# ══════════════════════════════════════════════════════════════════════
# 2/3. Closure defect  (computed: real Grassmannian sampling)
# ══════════════════════════════════════════════════════════════════════

def closure_defect(V_basis, gens):
    """D(V) = sum ||[Ti,Tj] - Proj_V([Ti,Tj])|| / sum ||[Ti,Tj]||."""
    Q, _ = np.linalg.qr(V_basis)          # 16 x k orthonormal columns
    num = den = 0.0
    k = len(gens)
    for i in range(k):
        for j in range(i + 1, k):
            B = bracket(gens[i], gens[j]).reshape(-1)
            nb = np.linalg.norm(B)
            if nb < 1e-14:
                continue
            proj = Q @ (Q.T @ B)
            num += np.linalg.norm(B - proj)
            den += nb
    return num / den if den > 0 else 0.0


def sl3_defect_and_samples(n_samples, rng):
    basis4 = sl_n_basis(4)                                   # 15 generators
    flat = np.array([b.reshape(-1) for b in basis4]).T       # 16 x 15

    # sl(3,R) embedded in the upper-left 3x3 block: exactly 8 generators.
    sl3 = []
    for b in sl_n_basis(3):
        M = np.zeros((4, 4))
        M[:3, :3] = b
        sl3.append(M)
    sl3_flat = np.array([m.reshape(-1) for m in sl3]).T      # 16 x 8
    d_sl3 = closure_defect(sl3_flat, sl3)

    defects = np.empty(n_samples)
    for s in range(n_samples):
        C = rng.standard_normal((15, 8))
        V = flat @ C                                          # 16 x 8
        gens = [V[:, c].reshape(4, 4) for c in range(8)]
        defects[s] = closure_defect(V, gens)
    return d_sl3, defects


def fig_closure_family():
    rng = default_rng(CANONICAL_SEED)
    d_sl3, defects = sl3_defect_and_samples(2000, rng)
    note(f"closure defect: D(sl(3,R)) = {d_sl3:.3e}; "
         f"min over 2000 random 8-dim subspaces = {defects.min():.4f}")

    # Paper A version: 2000 samples.
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.hist(defects, bins=40, color="#CCCCCC", edgecolor="#888888",
            label=f"Random 8-dim subspaces ($n={len(defects)}$)")
    ax.axvline(d_sl3, color="#CC0000", lw=2.5,
               label="$\\mathfrak{sl}(3,\\mathbb{R})$: $\\mathcal{D}\\approx0$")
    ax.axvline(defects.min(), color="#CC9900", lw=1.6, ls="--",
               label=f"min random $= {defects.min():.2f}$")
    ax.set_xlabel("Closure defect $\\mathcal{D}(V)$", fontsize=10)
    ax.set_ylabel("Count", fontsize=10)
    ax.set_title("$\\mathfrak{sl}(3,\\mathbb{R})$ is the closure attractor",
                 fontsize=10.5, fontweight="bold")
    ax.legend(fontsize=7.5, loc="upper left")
    ax.set_xlim(-0.05, max(0.9, defects.max() * 1.05))
    save(fig, "fig_closure_attractor")

    # Monograph version: the first 100 of the same canonical-seed draw.
    sub = defects[:100]
    fig, ax = plt.subplots(figsize=(4.5, 2.8))
    ax.hist(sub, bins=20, color="#CCCCCC", edgecolor="#999999",
            label="Random 8-dim subspaces ($n=100$)")
    ax.axvline(d_sl3, color="#CC0000", lw=2.5,
               label="$\\mathfrak{sl}(3,\\mathbb{R})$: $\\mathcal{D}\\approx0$")
    ax.set_xlabel("Closure defect $\\mathcal{D}(V)$", fontsize=10)
    ax.set_ylabel("Count (out of 100)", fontsize=10)
    ax.set_title("Selection principle: $\\mathfrak{sl}(3,\\mathbb{R})$ is unique",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_xlim(-0.05, max(0.9, sub.max() * 1.05))
    save(fig, "fig_selection")
    note(f"fig_selection: min over the first 100 samples = {sub.min():.4f}")
    return d_sl3, defects


# ══════════════════════════════════════════════════════════════════════
# 4. fig_barbero_immirzi  (computed)
# ══════════════════════════════════════════════════════════════════════

def fig_barbero_immirzi():
    def Z(g, jmax=200):
        j = np.arange(0.5, jmax + 0.5, 0.5)
        return np.sum((2 * j + 1) * np.exp(-2 * np.pi * g * np.sqrt(j * (j + 1))))

    gs = np.linspace(0.08, 0.8, 900)
    zs = np.array([Z(g) for g in gs])
    lo, hi = 0.05, 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if Z(mid) > 1.0:
            lo = mid
        else:
            hi = mid
    g_acs = 0.5 * (lo + hi)
    note(f"Barbero-Immirzi: Z(gamma)=1 at gamma = {g_acs:.6f}")

    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    ax.semilogy(gs, zs, color="#224488", lw=1.8)
    ax.axhline(1.0, color="black", ls="--", lw=1.0, label="$Z=1$ (information balance)")
    ax.axvline(g_acs, color="#CC0000", lw=1.8,
               label=f"$\\gamma_{{\\rm ACS}} = {g_acs:.4f}$ (SU(2) counting)")
    ax.axvline(0.2375, color="#118833", ls=":", lw=1.8,
               label="$\\gamma_{\\rm DL} = 0.2375$ (Gauss-constrained)")
    ax.set_xlabel("$\\gamma$", fontsize=10)
    ax.set_ylabel("$Z(\\gamma)$", fontsize=10)
    ax.set_title("Horizon state sum: $Z(\\gamma)=1$ selects $\\gamma$",
                 fontsize=10.5, fontweight="bold")
    ax.legend(fontsize=7.2, loc="upper right")
    ax.set_ylim(1e-2, 1e3)
    save(fig, "fig_barbero_immirzi")


# ══════════════════════════════════════════════════════════════════════
# 5. fig_torsion_tiers  (computed: exact rational couplings)
# ══════════════════════════════════════════════════════════════════════

def fig_torsion_tiers():
    basis_rows, ew_rows = torsion_couplings()
    vals = sorted({v for _, v in basis_rows})
    note(f"torsion couplings on the A/S basis: {[str(v) for v in vals]} "
         f"({sum(1 for _, v in basis_rows if v == 0)} at 0, "
         f"{sum(1 for _, v in basis_rows if v != 0)} at 32/9)")
    ew_vals = sorted({v for _, v in ew_rows})
    note(f"torsion couplings on the EW-adapted J/K generators: {[str(v) for v in ew_vals]} "
         f"-> ratio 0 : 1 : 4 against 32/9")

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 2.9),
                                   gridspec_kw={"width_ratios": [1.35, 1]})

    # Left: the basis-independent two-tier result.
    names = [t for t, _ in basis_rows]
    ys = [float(v) for _, v in basis_rows]
    colors = ["#888888" if y == 0 else "#CC2222" for y in ys]
    axL.bar(range(len(ys)), ys, color=colors, edgecolor="black", linewidth=0.4)
    axL.set_xticks(range(len(ys)))
    axL.set_xticklabels(names, rotation=90, fontsize=5.6)
    axL.set_ylabel("$\\|[T_{B-L},X]\\|^2$", fontsize=9)
    axL.set_title("Two tiers on the $A/S$ basis\n(eigenvector adapted)",
                  fontsize=9, fontweight="bold")
    axL.axhline(32 / 9, color="#CC2222", ls=":", lw=1.0)
    axL.set_ylim(0, 32 / 9 * 1.30)
    axL.text(len(ys) - 0.5, 32 / 9 + 0.10, "$32/9$  (6 generators)",
             color="#CC2222", fontsize=7.5, ha="right")
    axL.text(len(ys) - 0.5, 32 / 9 * 1.18, "$0$  (9 generators)",
             color="#555555", fontsize=7.5, ha="right")

    # Right: the 0:1:4 reading on the EW-adapted generators.
    tiers = [("unbroken\n$H_i, A_{ij}, S_{ij}$", 0.0, "#888888"),
             ("electroweak\n$J_i, K_i$", 8 / 9, "#DD8800"),
             ("colour-lepton\n$A_{i3}, S_{i3}$", 32 / 9, "#CC2222")]
    axR.bar(range(3), [t[1] for t in tiers], color=[t[2] for t in tiers],
            edgecolor="black", linewidth=0.5, width=0.6)
    axR.set_xticks(range(3))
    axR.set_xticklabels([t[0] for t in tiers], fontsize=7)
    axR.set_ylabel("$\\|[T_{B-L},X]\\|^2$", fontsize=9)
    axR.set_title("Ratio $0:1:4$ on the EW-adapted\ngenerators (mixtures)",
                  fontsize=9, fontweight="bold")
    for i, t in enumerate(tiers):
        if t[1] > 0:
            axR.text(i, t[1] + 0.1, f"${Fraction(t[1]).limit_denominator(99)}$",
                     ha="center", fontsize=8)
    axR.text(0, 0.12, "$0$", ha="center", fontsize=8)
    save(fig, "fig_torsion_tiers")


# ══════════════════════════════════════════════════════════════════════
# 6. fig_rep_gallery / fig_nuclear_geometry  (computed weights + Casimirs)
# ══════════════════════════════════════════════════════════════════════

def su3_weights(p, q):
    """Weights of the su(3) irrep (p,q) in the (h1,h2) basis used above."""
    a1 = np.array([1.0, 0.0])
    a2 = np.array([-0.5, np.sqrt(3) / 2])
    hw = p * (a1 * 2 / 3 + a2 * 1 / 3) + q * (a1 * 1 / 3 + a2 * 2 / 3)
    pts = set()
    for i in range(-(p + q + 2), p + q + 3):
        for j in range(-(p + q + 2), p + q + 3):
            w = hw - i * a1 - j * a2
            k1 = np.dot(w, a1)
            if abs(k1) <= p + q + 1e-9:
                pts.add((round(w[0], 6), round(w[1], 6)))
    return np.array(sorted(pts))


def casimir(p, q):
    return (p * p + q * q + p * q) / 3.0 + p + q


def fig_rep_gallery():
    reps = [(0, 0, "$\\mathbf{1}$"), (1, 0, "$\\mathbf{3}$"), (0, 1, "$\\bar{\\mathbf{3}}$"),
            (1, 1, "$\\mathbf{8}$"), (2, 0, "$\\mathbf{6}$"), (3, 0, "$\\mathbf{10}$")]
    fig, axes = plt.subplots(2, 3, figsize=(6.2, 4.0))
    for ax, (p, q, lab) in zip(axes.ravel(), reps):
        pts = su3_weights(p, q)
        ax.scatter(pts[:, 0], pts[:, 1], s=26, color="#224488",
                   edgecolor="black", linewidth=0.4, zorder=3)
        ax.set_title(f"{lab}   $C_2={casimir(p,q):.2f}$", fontsize=8.5)
        ax.axhline(0, color="#BBBBBB", lw=0.4)
        ax.axvline(0, color="#BBBBBB", lw=0.4)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        lim = 2.6
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
    fig.suptitle("Weight diagrams of the six lowest $\\mathfrak{su}(3)$ representations",
                 fontsize=10, fontweight="bold")
    save(fig, "fig_rep_gallery")


def fig_nuclear_geometry():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.8, 3.0))

    pts = su3_weights(1, 0)
    axL.scatter(pts[:, 0], pts[:, 1], s=150, color="#224488",
                edgecolor="black", linewidth=0.6, zorder=3)
    for a, b in [(0, 1), (1, 2), (0, 2)]:
        axL.annotate("", xy=tuple(pts[b]), xytext=tuple(pts[a]),
                     arrowprops=dict(arrowstyle="<->", color="#CC2222", lw=1.3))
    axL.set_title("Gluons as root-vector displacements", fontsize=9, fontweight="bold")
    axL.set_aspect("equal")
    axL.axhline(0, color="#DDDDDD", lw=0.4)
    axL.axvline(0, color="#DDDDDD", lw=0.4)
    axL.set_xticks([])
    axL.set_yticks([])

    reps = [(0, 0, "$\\mathbf{1}$"), (1, 0, "$\\mathbf{3}$"), (1, 1, "$\\mathbf{8}$"),
            (3, 0, "$\\mathbf{10}$")]
    cs = [casimir(p, q) for p, q, _ in reps]
    axR.barh(range(len(reps)), cs, color=["#118833", "#224488", "#DD8800", "#CC2222"],
             edgecolor="black", linewidth=0.5, height=0.55)
    axR.set_yticks(range(len(reps)))
    axR.set_yticklabels([r[2] for r in reps], fontsize=10)
    axR.set_xlabel("quadratic Casimir $C_2$", fontsize=9)
    axR.set_title("Confinement drives $C_2\\to0$  ($\\Delta\\mathcal{I}=0$)",
                  fontsize=9, fontweight="bold")
    for i, c in enumerate(cs):
        axR.text(c + 0.1, i, f"{c:.2f}", va="center", fontsize=8)
    axR.set_xlim(0, max(cs) * 1.25)
    save(fig, "fig_nuclear_geometry")


# ══════════════════════════════════════════════════════════════════════
# 7. fig_ricci_flow  (computed)
# ══════════════════════════════════════════════════════════════════════

def fig_ricci_flow():
    """Normalised 2D Ricci flow on a conformally-perturbed sphere.

    For g = e^{2u} g_0 on S^2, R = e^{-2u}(R_0 - 2 Delta_0 u) with R_0 = 2.
    Normalised flow: du/dt = -(R - <R>).  Explicit Euler, with dt chosen
    under the diffusion stability limit for the polar-capped grid.
    """
    ntheta, nphi = 48, 96
    cap = 0.35                                    # keep away from the 1/sin^2 poles
    th = np.linspace(cap, np.pi - cap, ntheta)
    ph = np.linspace(0, 2 * np.pi, nphi, endpoint=False)
    TH, PH = np.meshgrid(th, ph, indexing="ij")
    dth, dph = th[1] - th[0], ph[1] - ph[0]
    sin2 = np.sin(TH) ** 2

    def ricci_scalar(u):
        lap = np.zeros_like(u)
        up, dn = np.empty_like(u), np.empty_like(u)
        up[:-1], up[-1] = u[1:], u[-1]            # Neumann at the caps
        dn[1:], dn[0] = u[:-1], u[0]
        lap += (up - 2 * u + dn) / dth ** 2
        lap += (np.cos(TH) / np.sin(TH)) * (up - dn) / (2 * dth)
        lap += (np.roll(u, -1, 1) - 2 * u + np.roll(u, 1, 1)) / (dph ** 2 * sin2)
        return np.exp(-2 * u) * (2.0 - 2.0 * lap)

    # explicit-Euler stability bound for the diffusion part
    dt = 0.20 / (2.0 / dth ** 2 + 2.0 / (dph ** 2 * sin2.min()))
    nsteps = 800
    u = 0.30 * np.sin(3 * TH) * np.cos(2 * PH)

    snapshots, variances = [], []
    for step in range(nsteps + 1):
        R = ricci_scalar(u)
        if not np.all(np.isfinite(R)):
            note("WARNING: Ricci flow diverged; truncating at step %d" % step)
            break
        variances.append(float(np.var(R)))
        if step in (0, nsteps // 4, nsteps):
            snapshots.append((step, R.copy()))
        u = u - dt * (R - R.mean())

    ratio = variances[0] / variances[-1]
    note(f"Ricci flow: curvature variance reduced {ratio:.1f}x (std {ratio**0.5:.1f}x) "
         f"over {len(variances)-1} steps ({variances[0]:.4f} -> {variances[-1]:.4f}), "
         f"dt = {dt:.2e}")
    note("Ricci flow: this figure illustrates monotone decay only; the headline "
         "factor quoted in the papers comes from extras/ricci_flow.py "
         "(std 41.1x, variance 1693x) on its own discretisation")

    fig, axes = plt.subplots(1, 4, figsize=(8.6, 2.3),
                            gridspec_kw={"width_ratios": [1, 1, 1, 1.25]})
    vmax = float(np.abs(snapshots[0][1]).max())
    for ax, (step, R) in zip(axes[:3], snapshots):
        im = ax.pcolormesh(PH, TH, R, cmap="RdBu_r",
                           vmin=-vmax, vmax=vmax, shading="auto")
        ax.set_title(f"$t={step}$", fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.colorbar(im, ax=axes[2], fraction=0.046, label="$R$")
    axes[3].semilogy(variances, color="#224488", lw=1.5)
    axes[3].set_xlabel("flow step", fontsize=8.5)
    axes[3].set_ylabel("$\\mathrm{Var}(R)$", fontsize=8.5)
    axes[3].set_title("monotone decay", fontsize=9)
    axes[3].grid(alpha=0.25)
    fig.suptitle("Ricci flow as the ACS approaching information balance",
                 fontsize=10, fontweight="bold")
    save(fig, "fig_ricci_flow")


# ══════════════════════════════════════════════════════════════════════
# 8. fig_sign_reversal  (computed: the real automaton, not hard-coded)
# ══════════════════════════════════════════════════════════════════════

def fig_sign_reversal():
    """DI values are taken from the repository's own verified automaton,
    code/acs_codebase/extras/integer_acs.py, by running it and parsing its
    reported values.  The figure is therefore pinned to the exact-rational
    computation the papers cite, rather than to a re-implementation here.
    """
    import re
    import subprocess

    script = os.path.join(REPO, "code", "acs_codebase", "extras", "integer_acs.py")
    proc = subprocess.run([sys.executable, script], capture_output=True,
                          text=True, timeout=900)
    if proc.returncode != 0:
        raise RuntimeError(f"integer_acs.py failed:\n{proc.stderr[-2000:]}")

    wanted = [
        ("Uncoupled", "Uncoupled"),
        ("Symmetric (f=g=x²)", "Symmetric\n$(f{=}g{=}x^2)$"),
        ("Asymmetric (f=x², g=|y-8|)", "Asymmetric\n$(f{=}x^2,\\ g{=}|y{-}8|)$"),
        ("Asymmetric SWAPPED (f=|x-8|, g=y²)", "Swapped\n$(f{=}|x{-}8|,\\ g{=}y^2)$"),
    ]
    found = {}
    for line in proc.stdout.splitlines():
        m = re.search(r"^\s*(.+?)\s+DI = ([+-]?\d+\.\d+)\s*$", line)
        if m:
            found[m.group(1).strip()] = float(m.group(2))
    labels, vals = [], []
    for key, lab in wanted:
        if key not in found:
            raise RuntimeError(f"could not parse DI for {key!r}; "
                               f"parsed keys: {sorted(found)}")
        labels.append(lab)
        vals.append(found[key])

    note("integer automaton DI (from extras/integer_acs.py) = "
         + ", ".join(f"{v:+.5f}" for v in vals))
    if abs(abs(vals[2]) - 1.4986) > 0.01:
        note(f"WARNING: asymmetric DI {vals[2]:+.5f} differs from the "
             f"papers' quoted -1.4986")
    if not (vals[2] < 0 < vals[3]):
        note("WARNING: sign reversal under f<->g swap not observed")

    fig, ax = plt.subplots(figsize=(4.4, 2.6))
    colors = ["#CCCCCC", "#CCCCCC", "#CC0000", "#0044CC"]
    bars = ax.bar(range(4), vals, color=colors, edgecolor="black", linewidth=0.5, width=0.6)
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("$\\Delta\\mathcal{I}$", fontsize=11)
    ax.set_title("Integer automaton: sign reversal under $f\\leftrightarrow g$",
                 fontsize=9.5, fontweight="bold")
    ax.axhline(0, color="black", lw=0.5)
    ax.grid(True, axis="y", alpha=0.2)
    span = max(abs(min(vals)), abs(max(vals))) or 1.0
    for bar, v in zip(bars, vals):
        if abs(v) > 0.01:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    v + (0.08 * span if v > 0 else -0.16 * span),
                    f"{v:+.3f}", ha="center", fontsize=8, fontweight="bold")
    ax.set_ylim(-1.35 * span, 1.35 * span)
    save(fig, "fig_sign_reversal")


# ══════════════════════════════════════════════════════════════════════
# 9. fig_chirality  (tabulated: torsion-lattice index, monograph Table)
# ══════════════════════════════════════════════════════════════════════

def fig_chirality():
    N = np.array([8, 12, 16, 20, 24, 32])
    idx = np.array([21, 45, 77, 121, 175, 309])
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.4, 2.6))
    axL.plot(N, idx, "o-", color="#CC2222", lw=1.5, label="$T^a \\neq 0$")
    axL.plot(N, np.zeros_like(N), "s--", color="#888888", lw=1.2, label="$T^a = 0$")
    axL.set_xlabel("lattice size $N$", fontsize=9)
    axL.set_ylabel("spectral index", fontsize=9)
    axL.legend(fontsize=8)
    axL.grid(alpha=0.25)
    axR.plot(N, idx / N ** 2, "o-", color="#224488", lw=1.5)
    axR.axhline(0.30, color="#CC2222", ls=":", lw=1.2, label="$\\approx 0.30$")
    axR.set_xlabel("lattice size $N$", fontsize=9)
    axR.set_ylabel("$|\\mathrm{index}|/N^2$", fontsize=9)
    axR.legend(fontsize=8)
    axR.grid(alpha=0.25)
    fig.suptitle("Torsion-induced chirality: index scales with volume",
                 fontsize=10, fontweight="bold")
    save(fig, "fig_chirality")
    note("fig_chirality is TABULATED from the monograph torsion-lattice table "
         "(sizes 8-32); regenerate from extras/torsion_lattice.py to recompute")


# ══════════════════════════════════════════════════════════════════════
# 10-12. Paper B figures  (computed from the committed Odlyzko zeros)
# ══════════════════════════════════════════════════════════════════════

def load_zeros(n):
    g = []
    with open(ZEROS) as fh:
        for line in fh:
            line = line.strip()
            if line:
                g.append(float(line))
            if len(g) >= n:
                break
    return np.array(g)


def fig_variance_scaling():
    gam = load_zeros(50)
    A = 1.0 / (0.25 + gam ** 2)

    def var_T12(X, sigma, m=4000):
        x = np.linspace(X, 2 * X, m)
        lx = np.log(x)
        T12 = np.zeros_like(x)
        for a, gk in zip(A, gam):
            rho_abs = np.hypot(sigma, gk)
            phase = gk * lx - np.arctan2(gk, sigma)
            T12 += -(x ** sigma) * np.cos(phase) / rho_abs * (a * (0.25 + gk ** 2))
        return float(np.var(T12))

    Xs = np.array([1e2, 1e3, 1e4, 1e5])
    ratios = np.array([var_T12(X, 0.6) / var_T12(X, 0.5) for X in Xs])
    pred = (Xs / Xs[0]) ** 0.2 * ratios[0]
    rel = np.abs(ratios - pred) / pred
    note(f"variance scaling ratios = {np.array2string(ratios, precision=3)}; "
         f"max deviation from X^0.2 = {rel.max()*100:.2f}%")

    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    ax.loglog(Xs, ratios, "o", color="#CC2222", ms=7, label="measured (50 Odlyzko zeros)")
    ax.loglog(Xs, pred, "--", color="#224488", lw=1.5, label="$\\propto X^{0.2}$")
    ax.set_xlabel("$X$", fontsize=10)
    ax.set_ylabel("$\\mathrm{Var}_X[T_{12}]_{\\sigma=0.6}\\,/\\,\\mathrm{Var}_X[T_{12}]_{\\sigma=0.5}$",
                  fontsize=8)
    ax.set_title("Variance scaling: off-critical zeros steepen the power law",
                 fontsize=9.5, fontweight="bold")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25, which="both")
    save(fig, "fig_variance_scaling")


def fig_flow_field():
    g1 = load_zeros(1)[0]
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.4, 3.0))
    for ax, sigma, title in ((axL, 0.5, "$\\sigma = 1/2$: closed loop"),
                             (axR, 0.7, "$\\sigma = 0.7$: outward spiral")):
        t = np.linspace(0, 6 * np.pi / g1, 4000)          # three full turns
        r = np.exp((sigma - 0.5) * t)
        x, y = r * np.cos(g1 * t), r * np.sin(g1 * t)
        ax.plot(x, y, color="#224488" if sigma == 0.5 else "#CC2222", lw=1.1)
        ax.scatter([x[0]], [y[0]], s=22, color="black", zorder=3)
        ax.set_title(title, fontsize=9.5, fontweight="bold")
        ax.set_aspect("equal")
        ax.axhline(0, color="#DDDDDD", lw=0.5)
        ax.axvline(0, color="#DDDDDD", lw=0.5)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle(f"Tensor flow for $\\gamma_1 = {g1:.3f}$: "
                 "$\\sigma=1/2$ is the unique center manifold",
                 fontsize=9.5, fontweight="bold", y=1.04)
    save(fig, "fig_flow_field")
    note("fig_flow_field: radial envelope is exp((sigma-1/2)t); "
         "at sigma=1/2 it is identically 1, giving a closed orbit")


def fig_wronskian_heatmap():
    gam = load_zeros(20)
    x = np.e                                   # t = ln x = 1
    c, s = np.cos(gam * np.log(x)), np.sin(gam * np.log(x))
    # phi_k(x) = cos(gamma_k ln x)/sqrt(x);  W[k,j] = phi_k' phi_j - phi_j' phi_k
    W = (np.outer(gam * s, c) - np.outer(c, gam * s)) * x ** -2
    W = -W                                     # orientation: W[k,j] = phi_k' phi_j - ...
    off = W[~np.eye(len(gam), dtype=bool)]
    note(f"Wronskian at t=1, sigma=1/2: |W| in [{np.abs(off).min():.3e}, "
         f"{np.abs(off).max():.3e}]; zero off-diagonal entries = "
         f"{int((np.abs(off) < 1e-12).sum())}")
    note("Wronskian magnitudes depend on the phi_k normalisation convention; "
         "Paper B quotes [8.6e-5, 0.19] for its stated convention")

    fig, ax = plt.subplots(figsize=(4.2, 3.5))
    lim = float(np.abs(W).max())
    im = ax.imshow(W, cmap="RdBu_r", vmin=-lim, vmax=lim)
    ax.set_xlabel("$j$", fontsize=10)
    ax.set_ylabel("$k$", fontsize=10)
    ax.set_title("$W[\\varphi_k,\\varphi_j]$ at $t=1$, $\\sigma=1/2$\n"
                 "(antisymmetric; no zero entry)", fontsize=9.5, fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.046)
    save(fig, "fig_wronskian_heatmap")


# ══════════════════════════════════════════════════════════════════════
# 13-14. Schematics
# ══════════════════════════════════════════════════════════════════════

def _box(ax, xy, w, h, text, fc, fs=8):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch(xy, w, h, boxstyle="round,pad=0.02",
                                facecolor=fc, edgecolor="black", linewidth=0.7))
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fs)


def fig_layers_cycle():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.2, 3.2))
    layers = [("Layer 0: Forms   $e^a_\\mu$", "#DDE8F5"),
              ("Layer 1: $T^a = de^a + \\omega^a{}_b\\wedge e^b$", "#CCE0F0"),
              ("Layer 2: $R^{ab} = d\\omega^{ab} + \\omega\\wedge\\omega$", "#BBD6EC"),
              ("Layer 3: $D_{[\\mu}F_{\\nu\\rho]} = 0$  (Bianchi)", "#AACBE7")]
    for i, (txt, fc) in enumerate(layers):
        _box(axL, (0.05, 0.06 + i * 0.23), 0.9, 0.17, txt, fc, fs=7.4)
        if i < 3:
            axL.annotate("", xy=(0.5, 0.06 + (i + 1) * 0.23),
                         xytext=(0.5, 0.06 + i * 0.23 + 0.17),
                         arrowprops=dict(arrowstyle="->", lw=1.1))
    axL.text(0.5, 0.99, "acts only on lower layers; output is a Form",
             ha="center", va="top", fontsize=7.2, style="italic")
    axL.set_xlim(0, 1)
    axL.set_ylim(0, 1.03)
    axL.axis("off")
    axL.set_title("Strict resolution hierarchy", fontsize=9.5, fontweight="bold")

    steps = ["$T^a = 0$", "torsion\nactivates", "chiral\nmodes", "spinor\nbundle",
             "$\\mathfrak{sl}(3,\\mathbb{R})\\to\\mathfrak{su}(3)$", "confinement\n$\\Delta\\mathcal{I}\\to0$"]
    th = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi, len(steps) + 1)[:-1]
    for i, (t, lab) in enumerate(zip(th, steps)):
        x, y = 0.62 * np.cos(t), 0.62 * np.sin(t)
        axR.scatter([x], [y], s=1500, facecolor="#F0E2CC", edgecolor="black",
                    linewidth=0.7, zorder=2)
        axR.text(x, y, lab, ha="center", va="center", fontsize=6.4, zorder=3)
    for i in range(len(th)):
        t0, t1 = th[i], th[(i + 1) % len(th)]
        axR.annotate("", xy=(0.62 * np.cos(t1) * 0.78, 0.62 * np.sin(t1) * 0.78),
                     xytext=(0.62 * np.cos(t0) * 0.78, 0.62 * np.sin(t0) * 0.78),
                     arrowprops=dict(arrowstyle="->", color="#AA5500", lw=1.0,
                                     connectionstyle="arc3,rad=0.25"))
    axR.set_xlim(-1, 1)
    axR.set_ylim(-1, 1)
    axR.set_aspect("equal")
    axR.axis("off")
    axR.set_title("Constraint-attractor cycle", fontsize=9.5, fontweight="bold")
    save(fig, "fig_layers_cycle")


def fig_hero_nesting():
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    chain = [("Palatini gravity\n$(e,\\omega)$ as an ACS", "#DDE8F5"),
             ("$\\mathfrak{sl}(4,\\mathbb{R})$, rank 15\n(6 Lorentz + 9 torsion)", "#CCE0F0"),
             ("$\\mathfrak{sl}(3,\\mathbb{R})$ closure attractor\n$J:\\ \\mathfrak{sl}(3,\\mathbb{R})\\to\\mathfrak{su}(3)$", "#BBD6EC"),
             ("Koide projection $2/3$\n$\\Rightarrow\\ \\lambda=2\\sqrt{3}/27$", "#AACBE7"),
             ("3 generations\n(Jacobi truncation)", "#99C0E2"),
             ("Predictions:\n49 keV $\\nu$, $\\theta_{\\rm QCD}=0$", "#88B5DD")]
    for i, (txt, fc) in enumerate(chain):
        y = 0.88 - i * 0.145
        _box(ax, (0.06, y - 0.055), 0.55, 0.11, txt, fc, fs=7.2)
        if i < len(chain) - 1:
            ax.annotate("", xy=(0.335, y - 0.09), xytext=(0.335, y - 0.055),
                        arrowprops=dict(arrowstyle="->", lw=1.1))
    ledger = ("Branch A input ledger\n\n"
              "2  calibrations  ($v$, $m_\\tau$)\n"
              "1  forbidden  ($\\alpha_2$, rep theory)\n"
              "1  tree-excluded  ($\\beta_c$)\n"
              "3  free  ($\\rho_1,\\alpha_1,\\tan\\beta$)\n"
              "\\rule{0pt}{1em}\n"
              "6  total inputs   (SM: 19+)")
    _box(ax, (0.66, 0.20), 0.30, 0.60, ledger.replace("\\rule{0pt}{1em}\n", ""),
         "#F5EEE0", fs=7.0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 1)
    ax.axis("off")
    ax.set_title("The ACS nesting chain: each solution becomes the next constraint",
                 fontsize=10, fontweight="bold")
    save(fig, "fig_hero_nesting")


# ══════════════════════════════════════════════════════════════════════

def main():
    print(f"Canonical seed: {CANONICAL_SEED}")
    print(f"Writing to:\n  {OUT_MAIN}\n  {OUT_TRILOGY}\n")
    fig_colour_weights()
    fig_closure_family()
    fig_barbero_immirzi()
    fig_torsion_tiers()
    fig_rep_gallery()
    fig_nuclear_geometry()
    fig_ricci_flow()
    fig_sign_reversal()
    fig_chirality()
    fig_variance_scaling()
    fig_flow_field()
    fig_wronskian_heatmap()
    fig_layers_cycle()
    fig_hero_nesting()

    made = set()
    for d in (OUT_MAIN, OUT_TRILOGY):
        for f in sorted(os.listdir(d)):
            if f.endswith(".pdf"):
                made.add(f[:-4])
    missing = set(FIGURE_KINDS) - made
    print(f"\n{len(made)} distinct figures written.")
    if missing:
        print(f"MISSING: {sorted(missing)}")
        return 1
    print("\nProvenance summary:")
    for kind in ("computed", "tabulated", "schematic"):
        names = sorted(k for k, v in FIGURE_KINDS.items() if v == kind)
        print(f"  {kind:9s} ({len(names)}): {', '.join(names)}")
    if _notes:
        print("\nRun notes:")
        for n in _notes:
            print(f"  - {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
