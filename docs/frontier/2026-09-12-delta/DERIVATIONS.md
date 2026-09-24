# Derivations and verification boundaries — 12 September 2026

This continuation extends the declared mathematical objects in the [11 September snapshot](../2026-09-11/README.md). It does not identify an arbitrary scalar kernel, probability model, or constructed spectrum with the full ACS dynamics.

## C06: arbitrary real probabilities

The original `LFBound.lean` uses integer-valued doubled probabilities. Its theorem quantifies over that carrier. The extension [LFReal.lean](../../../code/frontier_verification/proofs/LFReal.lean) instead uses a function from two three-valued settings and two binary outcomes to the reals, with nonnegative entries and total probability one at each setting pair.

For any pair of settings, write

$$E=p_{++}-p_{+-}-p_{-+}+p_{--}.$$

Nonnegativity and normalization give $-1\leq E\leq1$. Therefore

$$S=E_{22}+E_{23}+E_{32}-E_{33}\leq4.$$

The formal proof establishes this upper bound on all such real-valued probability behaviors. It separately constructs a witness in the explicitly defined no-signalling branch with deterministic positive friend outcomes and proves $S=4$. Thus the upper bound is attained on that branch. The source statements remain explicit about which probability model is represented.

The independent [LP audit](../../../code/frontier_verification/lf_real_audit.py) optimizes over 36 real probability variables in each of the four deterministic friend branches. A separate exact-rational witness and dual certificate establish the same optimum without relying on the LP solver's numerical answer. The dual is the sum of four normalization constraints: its coefficient vector dominates the objective componentwise and its right-hand side is exactly four.

A mixture with one-third of the PR witness and two-thirds of a product behavior gives probabilities including one-sixth and has $S=4/3$. It is a valid point outside the original integer-half-unit carrier. The original witness and the upper bound are preserved; the new proof broadens the quantified carrier. Neither this extension nor the LP certificate formalizes a quantum realization or Tsirelson's theorem.

## R11: finite resolution and a moving boundary

For $T>0$, $\varepsilon>0$, define the source's scalar contribution

$$C(\gamma,T,\varepsilon)=2\left[\arctan\frac{T-\gamma}{\varepsilon}+\arctan\frac{\gamma}{\varepsilon}\right].$$

For fixed $0<\gamma<T$, the archived `PerZero.lean` proves that this tends to $2\pi$ as $\varepsilon\downarrow0$. A fixed interior point and a point approaching an endpoint require different limits.

### Exact integral and finite-resolution error

For real $u$ and $\varepsilon>0$, direct algebra gives

$$\frac1{\varepsilon+iu}-\frac1{-\varepsilon+iu}=\frac{2\varepsilon}{\varepsilon^2+u^2}.$$

Differentiating $2\arctan(u/\varepsilon)$ gives the right-hand side. Integrating from $u=-\gamma$ to $u=T-\gamma$ therefore recovers $C$. The [Python audit](../../../code/frontier_verification/per_zero_boundary_audit.py) checks both identities symbolically and compares the closed form with separately evaluated quadrature. This calculus argument has not yet been formalized as an integral theorem in Lean.

For an interior point, its deficit is exactly

$$D=2\pi-C=2\left[\arctan\frac{\varepsilon}{\gamma}+\arctan\frac{\varepsilon}{T-\gamma}\right]>0.$$

The elementary integral representation $\arctan x=\int_0^x(1+t^2)^{-1}\,dt$ yields, for $x\geq0$,

$$\frac{x}{1+x^2}\leq\arctan x\leq x,\qquad 0\leq x-\arctan x\leq\frac{x^3}{3}.$$

Consequently,

$$2\varepsilon\left[\frac{\gamma}{\gamma^2+\varepsilon^2}+\frac{T-\gamma}{(T-\gamma)^2+\varepsilon^2}\right]\leq D\leq2\varepsilon\left[\frac1\gamma+\frac1{T-\gamma}\right],$$

and the error in the linear approximation satisfies

$$0\leq2\varepsilon\left[\frac1\gamma+\frac1{T-\gamma}\right]-D\leq\frac{2\varepsilon^3}{3}\left[\frac1{\gamma^3}+\frac1{(T-\gamma)^3}\right].$$

These are analytical inequalities for the specified scalar kernel. The 16 numerical comparisons exercise them but do not replace the derivation.

### A formalized boundary-scaling law

Set $T=1$ and $\gamma=c\varepsilon$. For $\varepsilon\ne0$,

$$C(c\varepsilon,1,\varepsilon)=2\left[\arctan(\varepsilon^{-1}-c)+\arctan c\right]\longrightarrow\pi+2\arctan c.$$

[PerZeroBoundary.lean](../../../code/frontier_verification/proofs/PerZeroBoundary.lean) kernel-checks the exact identity and this limit for every fixed real $c$. For $c>0$, the point is interior once $\varepsilon$ is sufficiently small. In particular, $c=1$ gives $3\pi/2$, and the proof explicitly rejects convergence to $2\pi$ along that path. Thus the fixed-interior limit cannot be applied uniformly over all interior ordinates.

### Exact criterion for the absolute counting error

Consider any sequence of finite point configurations $0<\gamma_{j,k}<T_j$ with positive resolutions $\varepsilon_j$. Let $E_j$ be the sum of their deficits. Then

$$E_j\to0\quad\Longleftrightarrow\quad\varepsilon_j\sum_k\left[\frac1{\gamma_{j,k}}+\frac1{T_j-\gamma_{j,k}}\right]\to0.$$

Proof: write the individual nonnegative ratios as $x_{j,\ell}$. The exact deficit is $E_j=2\sum_\ell\arctan x_{j,\ell}$. The upper bound proves sufficiency. Conversely, if $E_j\to0$, every arctangent in the finite sum is eventually below $\pi/4$, uniformly in its index, so all ratios are below one. On $[0,1]$, $\arctan x\geq x/2$; hence $\sum_\ell x_{j,\ell}\leq E_j$ eventually. This proves necessity without assuming fixed cardinality or exchanging an uncontrolled sum and limit.

### Mean error has a weaker criterion

Assume $N_j\geq1$ points. Put $d_{j,k}=\min(\gamma_{j,k},T_j-\gamma_{j,k})$, and let $f_j(L)$ be the fraction with $d_{j,k}\leq L\varepsilon_j$. For each fixed $L>0$,

$$2\arctan(1/L)\,f_j(L)\leq E_j/N_j\leq2\pi f_j(L)+4\arctan(1/L).$$

The lower bound uses the nearer endpoint of every point in the boundary layer. Outside that layer, both arctangent arguments are smaller than $1/L$; each remaining point contributes at most $4\arctan(1/L)$. Each point inside contributes less than $2\pi$.

It follows that $E_j/N_j\to0$ if and only if $f_j(L)\to0$ for every fixed finite $L>0$. For sufficiency, first choose $L$ large, then take $j$ large. This is weaker than the absolute-error criterion.

For an explicit counterfamily, take $T=1$, $\varepsilon_N=N^{-2}$, one point at $\gamma=\varepsilon_N$, and the other $N-1$ points at $1/2$, where $N\geq2$. Its total error is

$$E_N=\frac\pi2+2\arctan\frac1{N^2-1}+4(N-1)\arctan\frac2{N^2}\longrightarrow\frac\pi2,$$

while $E_N/N\to0$. The audit evaluates this family at $N=10,100,1000$ and records the nonzero absolute error. Repeated ordinates are allowed in this abstract configuration; the construction makes no assertion about actual zeta zeros.

### Remaining scope

The moving-boundary law is kernel-checked. The integral identification, quantitative inequalities, and configuration criteria above have analytical derivations and computational checks, but are not yet Lean integral or summation theorems. Turning these into bounds for a particular zeta-zero dataset requires its actual endpoint separations and counting assumptions. None of these results supplies the missing real-part identification for RH or a natural Hilbert–Pólya operator.
