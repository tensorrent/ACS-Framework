# Gaussian explicit formula with controlled tails

This instrument connects the certified Q(zeta_5) zero data to an explicit arithmetic formula for a declared family of smooth test functions. It retains all terms and bounds uncomputed zeros without assuming GRH. It does not identify an operator or establish the historical unsmoothed amplitude claims. The preceding [Dedekind checkpoint](../../docs/frontier/2026-09-13-dedekind-delta/README.md) supplies the four finite factor certificates.

## Normalizations and identity

Let K=Q(zeta_5), with degree 4, discriminant D=125 and no real embeddings. Write

\[
\Lambda_K(s)=125^{s/2}(2\pi)^{-2s}\Gamma(s)^2\zeta_K(s),\qquad
\xi_K(s)=s(s-1)\Lambda_K(s).
\]

The primitive factorization is zeta times the three nonprincipal characters modulo 5. Their parities are 1,0,1. The product of their completed functions and completed Riemann zeta is **20 times** Lambda_K(s), by [gamma duplication](https://dlmf.nist.gov/5.5#E5). The factor 20 is constant and disappears on logarithmic differentiation. The polynomial discriminant of the fifth cyclotomic polynomial is 125; the preceding cyclotomic integer-ring premise identifies it with the field discriminant.

For a>0 and u>=0 choose the Fourier pair

\[
h(t)=e^{-at^2}\cos(ut),\quad
g(x)=\frac{e^{-(x-u)^2/(4a)}+e^{-(x+u)^2/(4a)}}{4\sqrt{\pi a}},\quad
h(t)=\int_{\mathbb R}g(x)e^{itx}\,dx.
\]

The Gaussian g is even, smooth, and decreases faster than any fixed exponential. It meets the bounded-variation and decay requirements of [Belabas–Friedman, Section 2, equations (1)–(2)](https://arxiv.org/pdf/1305.0035). That identity permits complex zero parameters; GRH would assert those parameters are real, and is not assumed here. Substituting this Fourier pair, n=4 and r=0 gives

\[
\sum_\rho h\left(\frac{\rho-1/2}{i}\right)
=P+D_g+G-Q,
\]

where multiplicities and both signs of height are included, and

\[
P=2e^{a/4}\cosh(u/2),\quad D_g=\log(125)g(0),\quad
Q=2\sum_{n\ge2}\frac{\Lambda_K(n)}{\sqrt n}g(\log n),
\]

\[
G=-4(\gamma_E+\log(8\pi))g(0)
+4\int_0^\infty\frac{g(0)-g(x)}{2\sinh(x/2)}\,dx.
\]

The pole term also follows directly from `4*integral g(x)*cosh(x/2) dx = 2*h(i/2)`. For p!=5, Lambda_K(p^k)=4 log(p) if ord_5(p) divides k, otherwise zero. At p=5 it is log(5) for every k>=1. All other n have coefficient zero. These are the exact coefficients audited in the preceding checkpoint.

A second gamma representation is

\[
G=-4\log(2\pi)g(0)
+\frac4\pi\int_0^\infty h(t)\Re\psi(1/2+it)\,dt.
\]

It follows by inserting the digamma integral representation and the Fourier pair. In particular, the constant `-4*log(2*pi)*g(0)` belongs to the gamma contribution. Omitting it in the initial alternate-route implementation was rejected by the zero-frequency case; the failed source and receipt are retained. The corrected route includes it explicitly.

## An unconditional bound for uncomputed zeros

Every nontrivial zero rho=beta+i*gamma has 0<beta<1. The Hadamard product and functional equation imply

\[
M:=\sum_\rho\Re\frac1{2-\rho}
=\frac32+\frac12\log125-2\log(2\pi)+2\psi(2)
+\frac{\zeta'_K}{\zeta_K}(2).
\]

The identity and coefficient bound `0<=Lambda_K(n)<=4*Lambda(n)` appear in [Grenié–Molteni, Section 2, equations (2.1)–(2.7)](https://arxiv.org/pdf/1407.1375). Although that paper's main zero-count theorems assume GRH, these preliminary identities hold unconditionally. We use s=2: every real part in the sum is positive from beta<1 alone, so their conditional positivity argument inside the critical strip is unnecessary.

Let C be the displayed elementary part, approximately 1.083971406029394. Since zeta'_K/zeta_K(2) is negative, M<=C. A finite prime sum gives the stronger bound `M <= C - sum(n<=X) Lambda_K(n)/n^2`. Its missing positive prime sum is at most `4*(log(X)+1)/X` by the integral test, enclosing M from both sides.

Put v=2-beta in (1,2). Then

\[
\frac{v}{v^2+\gamma^2}\ge\frac1{4+\gamma^2},
\]

because the numerator after multiplication by positive denominators is `v*(4-v)+(v-1)*gamma^2 >= 0`. Subtract the known finite moment `M_T=sum(0<gamma<T) 3/(9/4+gamma^2)` from the upper bound for M. Here each positive root appears once across the four factors and the factor 3 accounts for its two signed zeros. Call the resulting positive upper bound U_T.

For any unknown zero, including an off-line one,

\[
\left|h\left(\frac{\rho-1/2}{i}\right)\right|
\le e^{-a\gamma^2+a/4}\cosh(u/2).
\]

If `a*(4+T^2)>=1`, differentiation shows `(4+t^2)*exp(-a*t^2)` decreases for t>=T. Thus the entire signed zero tail is bounded by

\[
E_Z=U_T(4+T^2)e^{-aT^2+a/4}\cosh(u/2).
\]

This bound makes no assumption about the real parts of uncomputed zeros beyond the unconditional strip. Within the certified range, the finite sum is `2*sum h(gamma)` because all four factors have certified critical-line roots and no extra nontrivial zeros. The even-character origin zero is trivial and does not enter this sum. Riemann zeta has no real nontrivial zero: its alternating eta representation is positive for real s>0 and its denominator is negative for 0<s<1. The character certificates already exclude additional real nontrivial zeros in their rectangles.

## Prime and gamma truncations

For X with log(X)>2 and y=log(X)-u-a>0, dominate the omitted prime sum by all integers, using Lambda_K(n)<=4 log(n). The majorant `log(x)*x^(-1/2)*exp(-(log(x)-u)^2/(4a))` decreases for x>=X. Substitution v=log(x), completion of the square and the Gaussian tail inequality give

\[
E_Q\le8\sqrt{a/\pi}\,
e^{u/2+a/4-y^2/(4a)}\left(1+\frac{u+a}{y}\right).
\]

The program sums all eligible prime powers through X, including powers of 5. It does not truncate only the rational primes while silently omitting their eligible powers.

The primary gamma integral is evaluated by Arb over [delta,B], with delta=1e-20 and B=180. Globally `|g''(x)|<=3/(4*a*sqrt(pi*a))=:A`. This follows by differentiating both Gaussians and using `z*exp(-z)<=1` for z>=0. Since g'(0)=0 and `2*sinh(x/2)>=x`, the omitted **four-times integral** below delta is at most `A*delta^2`. Above B, using `0<=g(x)<=g_max=1/(2*sqrt(pi*a))`, its absolute value is at most

\[
8(g(0)+g_{max})\frac{e^{-B/2}}{1-e^{-B}}.
\]

Near zero, the numerator uses expm1 and `cosh(z)-1=2*sinh(z/2)^2` to control cancellation. The two precision runs use different integration partitions. The meromorphic integrand returns non-finite interval values on poles, meeting Arb's analytic-callback contract.

For the alternate digamma integral, [the digamma series](https://dlmf.nist.gov/5.7#E6) gives the positive difference

`Re psi(1/2+it) = psi(1/2) + sum(n>=0) t^2/((n+1/2)*((n+1/2)^2+t^2))`

and a decreasing integral comparison give `|Re psi| <= gamma_E+2*log(2)+2+log(1+4*t^2)/2 < 4+2*t`. Hence the omitted gamma contribution after L is at most `4/pi*exp(-a*L^2)/a*(1+2/L)`. This route integrates the analytic extension `(psi(1/2+it)+psi(1/2-it))/2`, not the nonanalytic real-part function on complex balls.

## Experiments and reproducibility

The fixed grid uses a=1/25,1/100,1/400 and ten frequencies: 0; log of 2,3,5,11,19,139,16,361; and 2.2. Each of the 30 cases has zero cutoffs 60,100,220 and prime-power cutoffs 1000,10000,100000. The logarithms of 16 and 361 test residue-degree powers; 5 tests ramification; zero frequency tests constants. The off-peak point is retained alongside the arithmetic frequencies.

From this directory, with the pinned [requirements](source_requirements.txt):

```sh
python dedekind_explicit_formula.py --extra ../../docs/frontier/2026-09-13-dedekind-delta/Factor_Certificates.zip --prior ../../docs/frontier/2026-09-13-lfunction-delta/Certificates.zip --precision 160 --output /path/to/Gaussian_160.json
python dedekind_explicit_formula.py --extra ../../docs/frontier/2026-09-13-dedekind-delta/Factor_Certificates.zip --prior ../../docs/frontier/2026-09-13-lfunction-delta/Certificates.zip --precision 224 --output /path/to/Gaussian_224.json
python dedekind_explicit_crosscheck.py --audit /path/to/Gaussian_224.json --extra ../../docs/frontier/2026-09-13-dedekind-delta/Factor_Certificates.zip --prior ../../docs/frontier/2026-09-13-lfunction-delta/Certificates.zip --output /path/to/Cross_Method.json
```

The independent route uses mpmath at 60 digits, a separate integer sieve and whole-prime-power residue criterion. It recomputes all 30 zero/prime/gamma/arithmetic values. Nine cases also use the alternate digamma integral with interval quadrature. Deliberate omissions and incorrect conjugation/weights are compared against the same bounded identity; failure to detect a mutation in one case is retained rather than converted into a success. The initial cross-check also exposed an overly rounded comparison string near the edge of a tight prime-sum enclosure. It now compares and retains all 60 computed digits; the certified producer intervals were not widened to make that check pass.

This evidence is numerical verification of a sourced analytic identity with explicit derived bounds, not a new Lean formalization. Both interval precisions share FLINT, and the finite root certificates are inherited. The present error is dominated by their root-bracket widths. Taking a toward zero requires increasing T and controlling root precision relative to frequency; a fixed height-220 dataset cannot establish an unsmoothed limit. Statistical calibration and natural-operator or physical interpretations remain separate obligations.
