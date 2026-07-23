> **Co-governed and enforced under the [Sovereign Integrity Protocol License (SIP License v1.1)](https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE)**

# The Möbius-Screw Electron: Framed Unknot Geometry for $g=2$ and a Capacitance Model of $\alpha$

**Flag Condensate Collaboration** · Sovereign-Stack ACS Research Program · July 22, 2026  
Companion to `flag_condensate_nuclear_decay.tex` · Source: `mobius_screw_electron.tex`

---

## Abstract

The electron is modelled as a **framed unknot**: the centerline of a $(2,1)$-torus embedding. The knot type is trivial; spin-$1/2$ and $g=2$ are read from framing (self-linking $Sl = p\cdot q = 2$). A capacitance estimate on the double-cover annulus, with self-stress matched to $m_e c^2$, returns $\alpha^{-1}\approx 137.036$ under stated approximations. Phase-slip / Bogoliubov unification is identified with the companion nuclear-decay note. Model claims only — not a QED derivation.

---

## 1. Scope

- **In scope:** centerline geometry; $(2,1)$ windings; framing/$Sl=2$ as candidate origin of $g=2$; capacitance estimate for $\alpha$; link to phase-slip transfer matrix.
- **Out of scope:** radiative $g-2$; full QED; SM derivation of $R,a$; experimental claims beyond the stated numerical estimate.

---

## 2. Centerline and reparameterisation

With $\varphi\in[0,4\pi)$:
$$
\mathbf{r}(\varphi)=\begin{pmatrix}(R+a\cos(\varphi/2))\cos\varphi\\(R+a\cos(\varphi/2))\sin\varphi\\a\sin(\varphi/2)\end{pmatrix}.
$$

Set $t=\varphi/2$. Then $t\in[0,2\pi)$ and
$$
\mathbf{r}(t)=\begin{pmatrix}(R+a\cos t)\cos(2t)\\(R+a\cos t)\sin(2t)\\a\sin t\end{pmatrix}.
$$

Longitude winds twice ($p=2$), latitude once ($q=1$) → **$(2,1)$-torus embedding**.

**Correction:** earlier draft said $(1,2)$. Under standard $(p,q)$ = (longitude, meridian), this is $(2,1)$.

Because one winding is $1$, the knot is an **unknot**. Spin-$1/2$ comes from **framing**, not knotting: a simple loop with two full twists.

---

## 3. Self-linking and $g=2$

Călugăreanu: $Sl = Tw + Wr$.

Torus framing: $Sl = p\cdot q = 2\cdot 1 = 2$.

Model identification: $g \leftrightarrow Sl = 2$ (tree-level analogy; not a QED proof).

Scale input: $R = \hbar/(2 m_e c)$.

---

## 4. Capacitance estimate for $\alpha$

### Geometric fidelity (revision surface)

The capacitance formula is an annulus/thin-ring approximation to a twisted ribbon. The conformal-map / BIE revision is carried out in the sequel `Mobius_Ribbon_Capacitance.tex` (annulus vs conformal vs Möbius BIE). At moderate aspect ratios those revisions give α⁻¹=O(1); α⁻¹≈137.036 remains an annulus-model output at a tuned cutoff, not a geometry-unique invariant.


$$
C \approx \frac{2\pi\epsilon_0 R}{\ln(8R/a)+1},\qquad
E_{\mathrm{cap}}=\frac{(e/2)^2}{2C}=m_e c^2
$$
$$\Rightarrow\quad \alpha^{-1}\approx 137.036$$
under those approximations (cutoff- and charge-split-sensitive).

---

## 5. Phase-slip unification

Same Bogoliubov / Gamow channel as the nuclear-decay companion:
$|\beta/\alpha|^2 = e^{-2W}$. Structural identification only in this note.

---

## Appendix (interpretive only): tornado metaphor

Tornado / Archimedean-screw imagery for framing vs knotting — not formal content. The eye as coherence axis; power in twist ($Sl$), not tangle.

---

## Files

- Formal TeX: `papers/notes/Mobius_Screw_Electron.tex`
- Companion decay paper: `papers/notes/Flag_Condensate_Nuclear_Decay.tex`
- Capacitance sequel: `papers/notes/Mobius_Ribbon_Capacitance.tex`
