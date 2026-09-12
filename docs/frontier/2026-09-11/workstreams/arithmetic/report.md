# Arithmetic and infinite-operator continuation

This workstream advances P03, P04, P08, R08, R09 and R10 through explicit operator theorems and one new conditional arithmetic spectral law. R04 and the natural-operator part of R06 remain open. Every conclusion below distinguishes a proved implication, a conjectural arithmetic premise, a finite prime calculation, and a surrogate counterexample. No claim of solving RH or exhausting possible prime laws is made.

The most concrete arithmetic result is this: **if the Lemke Oliver–Soundararajan consecutive-prime conjecture holds for triples at a fixed modulus with \(k=\varphi(m)\ge2\), then**

\[
\frac{P_m(x)}{\log\log x/\log x}\longrightarrow L_k,
\qquad (L_k)_{(b,c),(a,b)}=\frac1{2k}-\frac12\mathbf1_{b=c}.
\]

Consequently \(\rho(P_m(x))/(\log\log x/\log x)\to1/2\), and the manuscript's eigenvalue participation rank tends to **\(k-1\)**. This is a conditional, fixed-modulus prediction derived here; it is not an unconditional prime theorem or a statement about joint limits.

## 1. The exact manuscript convention

The local source `support/Prime_Gap_Transition_Operator.tex`, Setup, defines transition states \((a,b)\), column-stochastic forward transport, and

\[
T[(b,c),(a,b)]=\frac{C(a,b,c)}{\sum_d C(a,b,d)},
\qquad P=T-T_0,
\qquad T_0[(b,c),(a,b)]=1/k.
\]

All other entries vanish. Every denominator must be positive; empty columns require a new convention and are outside the theorem. The source is frozen with a SHA-256 provenance record. Earlier corrections of the source-sector claim are retained: column stochasticity gives a left-null sector, and does not identify the right kernel. Nothing here reverses that correction.

For each middle residue \(b\), define the \(k\times k\) matrix

\[
B_b[c,a]=P[(b,c),(a,b)].
\]

Group input columns as \((a,b)\) with \(b\) first, and output rows as \((b,c)\). Independent row/column permutations turn \(P\) into the block diagonal matrix \(\bigoplus_b B_b\). This is **unitary equivalence for singular values, not similarity for eigenvalues**. It proves

\[
\operatorname{rank}P=\sum_b\operatorname{rank}B_b,\quad
\|P\|_{\rm op}=\max_b\|B_b\|_{\rm op},\quad
\|P\|_{S_p}^p=\sum_b\|B_b\|_{S_p}^p\quad(1\le p<\infty).
\]

Every block has zero column sums, so its rank is at most \(k-1\). Thus the maximal rank \(k(k-1)\) occurs exactly when **every one of the \(k\) blocks has rank \(k-1\)**. For integer counts, multiplying each column by its positive denominator reduces this to exact integer ranks of

\[
M_b[c,a]=kC(a,b,c)-\sum_d C(a,b,d).
\]

This supplies a finite-rank certificate that does not depend on a numerical eigenvalue threshold. It does not prove eventual rank saturation at all primes or all moduli.

Verification uses separately assembled full matrices versus block singular values, and exact denominator-cleared integer ranks on fresh prime counts. The forward action formula \((Pf)(b,c)=\sum_aB_b[c,a]f(a,b)\) independently verifies the decomposition.

## 2. Uniform discrepancy gives quantitative growing-modulus rates

Assume, at the particular prefix and modulus under consideration,

\[
C(a,b,c)=A\,[1+\epsilon_{abc}],\quad A>0,\quad
\delta=\max_{abc}|\epsilon_{abc}|<1.
\]

The common scale \(A\) cancels. Write \(\mu_{ab}=k^{-1}\sum_c\epsilon_{abc}\). Then, exactly,

\[
B_b[c,a]=\frac{\epsilon_{abc}-\mu_{ab}}{k(1+\mu_{ab})}.
\]

For a uniformly selected \(c\), its variance is at most \(\delta^2-\mu_{ab}^2\). The elementary identity

\[
\delta^2(1+\mu)^2-(\delta^2-\mu^2)(1-\delta^2)
=(\delta^2+\mu)^2\ge0
\]

therefore gives

\[
\sum_c|B_b[c,a]|^2
\le\frac{\delta^2}{k(1-\delta^2)}.
\]

Sum over the \(k\) columns of a block, use its Frobenius bound for operator norm, and then sum the blocks. The resulting uniform theorem is

\[
\boxed{\ \rho(P)\le\|P\|_{\rm op}\le\frac{\delta}{\sqrt{1-\delta^2}},\qquad
\|P\|_{S_2}\le\frac{\sqrt{k}\,\delta}{\sqrt{1-\delta^2}},\qquad
\|P\|_{S_1}\le\frac{k\sqrt{k-1}\,\delta}{\sqrt{1-\delta^2}}.\ }
\]

Here \(S_2\) is Hilbert–Schmidt/Frobenius norm; \(S_1\) is the sum of singular values. The last inequality uses rank at most \(k(k-1)\). These bounds apply to changing \(k\): the old fixed-modulus restriction is unnecessary for convergence to **zero**, provided the displayed discrepancy assumption is proved along the chosen joint sequence. Embed each finite state space isometrically into any common Hilbert space and extend by zero. The bounds then imply respectively

| Topology of convergence to zero | Sufficient arithmetic rate as \(k\to\infty\) |
|---|---|
| Operator norm | \(\delta\to0\) |
| Hilbert–Schmidt norm | \(\sqrt{k}\delta\to0\) |
| Trace norm | \(k^{3/2}\delta\to0\) |

No coherent embedding is needed to compare norms against zero; a **nonzero** limit still requires specified embeddings and compatibility. No theorem proving these discrepancy rates for actual primes was obtained.

A renormalized criterion is also available. If

\[
\epsilon=hC+r,\quad \|C\|_\infty\le M,\quad
\|r\|_\infty\le\eta,\quad \delta\le hM+\eta<1,
\]

and \(L(C)_{(b,c),(a,b)}=(C_{abc}-\bar C_{ab})/k\), the exact quotient gives

\[
\left\|\frac P h-L(C)\right\|_{\rm op}
\le\frac{\eta/h+M\delta}{1-\delta}=:E.
\]

The corresponding \(S_2,S_1\) bounds are \(\sqrt{k}E\) and \(k\sqrt{k-1}E\). To prove this, write each column numerator as the centered version of \(r/h-C\mu_{ab}\); its uncentered entries have magnitude at most \(\eta/h+M\delta\). Its mean-square variance is no larger than the square of that quantity. This theorem makes the required uniform remainder explicit, rather than treating pointwise convergence in a changing dimension as sufficient.

## 3. Exact balanced counterfamilies: the topology matters

Let \(k=2^j\ge4\), let \(H_k\) be the symmetric Sylvester Hadamard matrix, and put

\[
Q=I-\frac1k\mathbf1\mathbf1^T,\qquad
D_k=\frac{k}{k+1}QH_kQ,\qquad
\epsilon_{abc}=\delta D_k[c,a].
\]

Both row and column sums of \(D_k\) vanish, and its entries have magnitude at most one. The counts \(C(a,b,c)=A(1+\delta D_k[c,a])\) thus have **both pair marginals equal to \(Ak\)**. For rational \(\delta\in(0,1)\), choose an integer scale \(A\) clearing denominators. The resulting positive integer edge counts on the directed pair graph have equal in/out degrees and connected support. An Euler circuit realizes them exactly as a cyclic residue word. This removes a possible objection that the surrogate counts cannot come from any consecutive sequence. It does **not** make that sequence a sequence of primes.

Each block is \(B=\delta D_k/k\). The nonzero singular values of \(QH_kQ\) are \(\sqrt{k}\) with multiplicity \(k-2\), and \(1\) once. A proof uses \(H_k^2=kI\): on \(\mathbf1^\perp\\), the square of the compression is \(kI-vv^T\\), where \(\|v\|^2=k-1\). Exact rational identities and independent SVDs confirm this spectrum.

Therefore

\[
\|P\|_{\rm op}=\frac{\delta\sqrt{k}}{k+1},\quad
\|P\|_{S_2}=\frac{\delta\sqrt{k}(k-1)}{k+1},\quad
\|P\|_{S_1}=\frac{\delta k((k-2)\sqrt{k}+1)}{k+1}.
\]

Taking \(\delta=k^{-3/2}\) yields operator and Hilbert–Schmidt convergence to zero, but **trace norm tends to one**. Taking \(\delta=k^{-1/2}\) leaves the Hilbert–Schmidt norm tending to one. Along the subsequence \(k=4^j\), both choices are rational and give the exact Euler-realizable integer-count families above. These show that the powers of \(k\) in the uniform \(S_2,S_1\) sufficient conditions cannot be reduced without extra assumptions. A simpler balanced family \(D=vv^T\), \(v_i=\pm1\), \(\sum v_i=0\), has operator norm exactly \(\delta\), showing the operator-norm scale is also optimal in order.

For the Hadamard family the algebraic rank is \(k(k-1)\), but its number of nonzero eigenvalues is \((k-1)^2\); singular values and eigenvalues must not be conflated. Because \(B\) is symmetric, on its tensor eigenbasis \(P\) interchanges the two indices with weight equal to one eigenvalue of \(B\). In particular \(P^2=B\otimes B\). Its eigenvalue participation rank is exactly

\[
r_{\rm eff}(P)=
\frac{((k-2)k^{1/4}+1)^4}{((k-2)\sqrt{k}+1)^2}
\sim k^2.
\]

Thus uniform small discrepancy, full allowable algebraic rank, exact flow balance, and a realizable residue word do **not** force a subquadratic participation rank. Multiplying \(P\) by a scalar never changes this participation rank. This is a counterexample to deriving a universal compression law from these structural assumptions alone, not a counterexample to a sufficiently specific theorem about actual primes.

The initial one-sided candidate \(QH_k\) failed: for \(k=4\), its incoming perturbation marginal is \((3,-1,-1,-1)\), whereas every outgoing perturbation marginal is zero. The rejected source, assertion, output and receipt are retained. Double centering is the correction.

## 4. A concrete conditional prime spectral law

The external arithmetic premise is the **Main Conjecture**, not a theorem, in [Lemke Oliver and Soundararajan, *Unexpected biases in the distribution of consecutive primes*, version 4](https://arxiv.org/html/1603.03720v4). For fixed modulus and \(r=3\), it supplies a count expansion with leading relative correction

\[
h\,c_1(a,b,c),\qquad h=\frac{\log\log x}{\log x},\qquad
c_1=1-\frac{k}{2}(\mathbf1_{a=b}+\mathbf1_{b=c}),
\]

plus terms \(O_m(1/\log x)=o_m(h)\). The subleading constants and error are not asserted uniform in \(m\). The conjecture counts by the first prime; requiring the third prime to lie below \(x\) changes at most two endpoint triples, and omitting primes below \(m\) changes finitely many more for fixed \(m\).

The derivation here is exact. Averaging \(c_1\) over \(c\) gives

\[
\bar c_1(a,b)=\frac12-\frac{k}{2}\mathbf1_{a=b}.
\]

Subtracting this average in the conditional-frequency quotient cancels all dependence on \(a=b\), leaving

\[
L_{(b,c),(a,b)}=\frac{c_1-\bar c_1}{k}
=\frac1{2k}-\frac12\mathbf1_{b=c}.
\]

For an independent spectral derivation, let

\[
(Sf)_b=\sum_a f(a,b),\qquad
(Vx)_{b,c}=\left(\frac1{2k}-\frac12\mathbf1_{b=c}\right)x_b.
\]

Then \(L=VS\), while \(SV=-Q/2\). Sylvester's determinant identity, or direct elimination of the kernel of \(S\), gives

\[
\det(tI-L)=t^{k^2-k+1}(t+1/2)^{k-1}.
\]

Direct exact characteristic polynomials for \(k=2,3,4,5\) verify this second route. The rank of \(L\) is \(k\), and \(L^3=-L^2/2\); a zero Jordan block explains why rank is not the number of nonzero eigenvalues. The nonzero eigenvalues are \(-1/2\), repeated \(k-1\) times. Fixed-dimensional polynomial root continuity now proves

\[
\rho(P)/h\to1/2,\qquad
\frac{(\sum_j|\lambda_j(P)|)^2}{\sum_j|\lambda_j(P)|^2}\to k-1.
\]

This conditional result is compatible with maximal finite algebraic rank: many finite nonzero eigenvalues may vanish faster than \(h\). It also leaves the order of limits essential. The observed exponent near 1.6 across a small modulus range does not follow from the fixed-modulus limit.

The independent finite instrument sieved primes through 2,000,000, with prefixes 20,000 and 200,000, and moduli 3, 4, 6, 10, 12, 30. Vectorized counts and a direct loop agree at every shortest prefix; every recorded column is populated. Exact block ranks certify maximal algebraic rank for every one of the 18 recorded operators. Representative final-prefix results are:

| Modulus | \(k\) | Exact algebraic rank | Observed \(\rho(P)/h\) | Observed participation rank | Conditional fixed-\(m\) limit of participation rank |
|---|---:|---:|---:|---:|---:|
| 3 | 2 | 2 | 0.881 | 1.541 | 1 |
| 4 | 2 | 2 | 0.804 | 1.557 | 1 |
| 10 | 4 | 12 | 0.987 | 7.544 | 3 |
| 12 | 4 | 12 | 0.889 | 6.597 | 3 |
| 30 | 8 | 56 | 2.073 | 16.222 | 7 |

These values are not close enough to certify the asymptotic prediction, and the finite calculations are not used to prove it. Their purpose is reproducible instrumentation, exact finite rank certification, and an honest record of the current scale.

## 5. R09/R10 continuation: an actual trace-class observable

Take the explicitly declared positive ordinates \(\gamma\) of all nontrivial zeta zeros, with multiplicity, and define \(H\) on \(\ell^2\) of the paired ordinates by multiplication by \(\pm\gamma\), with domain

\[
\mathcal D(H)=\{v:\sum_{\gamma,\pm}\gamma^2|v_{\pm\gamma}|^2<\infty\}.
\]

This is a self-adjoint **constructed ordinate operator**; naturalness and spectral identification are not established. The positive minimum ordinate makes \(H^{-1}\) bounded. It is Hilbert–Schmidt, but not trace class. For \(z\) outside the spectrum, however,

\[
A(z)=(H-zI)^{-1}-H^{-1}
=z(H-zI)^{-1}H^{-1}
\]

is trace class. The proof is either the product of two Hilbert–Schmidt diagonal factors, or direct absolute summation of \(z/[\lambda(\lambda-z)]\). Its trace equals the already defined paired scalar observable

\[
\operatorname{Tr}A(z)=\sum_{\gamma>0}\frac{2z}{\gamma^2-z^2}.
\]

This is a precisely changed observable; it does not retroactively turn the unpaired resolvent into a trace-class operator. The manuscript writes \(\omega I-H\), while this work and retained R08–R10 use \(H-zI\); converting conventions changes the sign of the trace.

Let \(H_{\rm tail}(T)\) be the established inverse-square bound from R10:

\[
H_{\rm tail}(T)=\frac{\log(T/(2\pi))+1}{2\pi T}
+\frac{a(2\log T+1/2)+b(2\log\log T+1/(2\log T))+2c}{T^2},
\]

with \((a,b,c)=(0.10076,0.24460,8.08344)\). The accepted external input remains Theorem 1.1 of [Bellotti and Wong, version 2](https://arxiv.org/html/2412.15470v2). No new zero-counting theorem is claimed.

For \(|z|\le K<T\), omit the finitely many low poles from the domain and truncate at ordinates \(\gamma\le T\). Then

\[
\|A(z)-A_T(z)\|_{S_1}
\le\frac{2K}{1-K/T}H_{\rm tail}(T),
\]

\[
\|A'(z)-A_T'(z)\|_{S_1}
\le\frac{2}{(1-K/T)^2}H_{\rm tail}(T).
\]

This supplies a trace-norm, rather than merely scalar cancellation, certificate. More generally, the \(r\ge1\) derivative tail is bounded by

\[
\frac{2r!\,T^{1-r}}{(1-K/T)^{r+1}}H_{\rm tail}(T).
\]

For an independent analytic route, define the canonical product

\[
D(z)=\prod_{\gamma>0}(1-z^2/\gamma^2).
\]

Uniform convergence on compact sets follows from the same inverse-square summability, and \(-D'/D=\operatorname{Tr}A\) away from zeros. If \(D_T\) is its finite product,

\[
\left|\frac{D(z)}{D_T(z)}-1\right|
\le\exp\left(\frac{K^2}{1-K^2/T^2}H_{\rm tail}(T)\right)-1.
\]

The ratio has its removable extension at shared finite-product zeros. This follows by expanding each tail logarithm with \(|\log(1-w)|\le |w|/(1-|w|)\), then exponentiating. On the integer-spectrum instrument, \(D(z)=\sin(\pi z)/(\pi z)\\) and the trace is \(1/z-\pi\cot(\pi z)\); these closed forms independently check product, trace and derivative truncations.

The following decimal bounds are rounded upward from high-precision evaluations; unlike retained R10, this new workstream does not attach fresh Arb enclosures to these decimal evaluations. The analytic inequalities are the certificates.

| \(T\), \(K=10\) | Trace-norm tail of \(A\) | Trace-norm tail of \(A'\) | Relative canonical-product error |
|---|---:|---:|---:|
| 100 | 0.173061 | 0.0192290 | 1.196004 |
| 1,000 | 0.0198914 | 0.00200924 | 0.103484 |
| 1,000,000 | 0.0000413100 | 0.00000413104 | 0.000206569 |

## 6. The exact RH and identification boundary

R04 requires an unconditional bound on \((\psi(e^u)-e^u)/(e^{u/2}(1+u^2))\). Its retained classical equivalence is unchanged. Neither inverse-square ordinate counts nor the constructed trace-class operator above controls the real parts of zeros or this prime-counting error.

There is a concrete information-loss obstruction. For any \(\gamma>0\) and \(0<\alpha<1/2\), the central multiset containing each \(1/2\pm i\gamma\) twice and the off-line quartet

\[
1/2\pm\alpha\pm i\gamma
\]

have identical positive-ordinate multisets. Every ordinate-only operator, paired resolvent and \(D(z)\) above is identical for the two. Yet the products retaining the full shifted-zero coordinates differ: with

\[
F(z)=\left(1-\frac{z^2}{(\gamma+i\alpha)^2}\right)
\left(1-\frac{z^2}{(\gamma-i\alpha)^2}\right),\qquad
G(z)=(1-z^2/\gamma^2)^2,
\]

the coefficient of \(z^2\) in \(F-G\) is

\[
\frac{2\alpha^2(3\gamma^2+\alpha^2)}{\gamma^2(\gamma^2+\alpha^2)^2}>0.
\]

Direct multiset comparison and the independently expanded product coefficient verify the obstruction. These are abstract symmetry-compatible multisets, not asserted alternative zeros of the zeta function. The result establishes that ordinate information alone cannot do the required identification. A natural operator whose spectral parameter is proved to equal \(-i(\rho-1/2)\), or an independently justified full trace formula implying that identification, remains necessary for this approach to RH.

## 7. Assigned-branch disposition

| Prior branch | New constructive advance or exact boundary | Disposition |
|---|---|---|
| P03 | Exact block-rank criterion; 18 fresh denominator-cleared prime-rank certificates | Finite evidence extended; all-prefix law open |
| P04 | Conditional fixed-modulus participation limit \(k-1\); balanced full-rank quadratic counterfamily for structural assumptions | Universal/joint-limit prime law open |
| P08 | Dimension-uniform operator estimate and explicit \(S_2,S_1\) joint-rate criteria; explicit conditional LOS coefficient | Conditional branch sharpened; arithmetic premise unproved |
| R04 | Explicit ordinate-information obstruction; corrected classical bound retained | RH bound open |
| R06 | Trace-class subtraction and domain for the constructed operator; exact missing real-part identification | Natural-operator branch open |
| R08 | Scalar paired observable realized as a trace of a specified trace-class subtraction | Observable subpath complete under declared spectrum |
| R09 | Sharp-in-order growing-dimension Schatten criteria; exact balanced failures of stronger convergence | General sufficient-condition branch advanced |
| R10 | Uniform trace-norm, derivative and canonical-product truncation bounds using retained \(H_{\rm tail}\) | Tail-control subpaths advanced; no RH consequence |

## 8. Verification, failures, and replay

`run_checks.py` executes snapshots in unique timestamped attempt directories, preserving source, stdout, stderr, SHA-256 hashes and receipts. Defaults run the three successful mathematical checks; the rejected `naive_hadamard_balance.py` is intentionally excluded. Old attempts are never rewritten. The first batch also retained three dependency failures: the default runtime lacked SymPy and mpmath. The same code passed after making already installed dependencies visible; requirements are declared for portable replay. Later adding exact finite-prime ranks produced a new successful LOS attempt, preserving its earlier successful source and output too.

Run `python run_checks.py` in an environment with the declared requirements. No check imports an old workspace path or depends on the frozen support copies at execution time. Those copies provide audit provenance. The two primary external arithmetic statements are explicit premises, not machine-verified lemmas. There is no proof-assistant kernel pass, no certified exhaustive prime-tail search, and no claim that numerical agreement proves the universal statements.
