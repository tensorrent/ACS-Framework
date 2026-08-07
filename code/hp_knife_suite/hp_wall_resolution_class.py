# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

r"""
THE WALL'S RESOLUTION CLASS  --  the two constraints coexist under an ANTI-commuting
antiunitary; the repulsion exponent counts the cone dimension the real slice hides.

hp_operator_constraint.py measured the Hilbert-Polya wall as two numbers on the zeros:
  A. real witness (|Im W|/|Re W| = 0.0001)  -> naively pulls to beta=1 (commuting antiunitary)
  B. GUE repulsion (beta = 2.00)            -> beta=2 (no commuting antiunitary)
The companion hypercone test (test_conjecture_hypercone_projection.py, branch
claude/torsion-topological-condensation-h6v40k) showed beta = codim - 1: the repulsion
exponent counts the degeneracy cone's codimension, and the chirality direction (the i of
the J-map) is exactly what buys codim 3.

This script establishes, kill-ably, that A and B are NOT mutually exclusive -- the wall is
a class selection, not a contradiction:

  M (exact, sympy). The hypercone's active block H(x,y,z) = x sz + y sx + z sy admits the
     ANTI-commuting antiunitary C = sy o K:  C H* C^{-1} = -H  for all (x,y,z), C^2 = -1.
     Consequences, exact: the spectrum is +-paired for ALL parameters (charpoly even in
     lambda) and the degeneracy locus is x=y=z=0 (codim 3 -> beta=2). Control: imposing a
     COMMUTING antiunitary T = K (T H* T^{-1} = +H) forces z = 0 -- the real slice -- and
     the codimension drops to 2 (beta=1). Commuting antiunitary kills the third direction;
     anti-commuting keeps it while pairing the spectrum.

  E (ensemble discriminator, numpy). Among GOE / GUE / chiral-GUE (H = [[0,A],[A+,0]]):
     only the chiral class passes BOTH wall constraints -- exact +- pairing makes the
     full-spectrum witness W(u) = sum exp(i gamma u) machine-real while the bulk repulsion
     stays beta ~ 2. GOE passes neither-A-and-B (beta~1); GUE passes B but W is complex.

  Reading. The wall's tension dissolves the same way the seam note's reality/GUE puzzle
  did: the AMPLITUDES live on the real slice (z=0, the self-dual locus, Fix(iota)); the
  REPULSION counts the full codimension including the hidden imaginary direction -- the
  phase direction that [iota,T] measures. beta - 1 - (codim of the real slice - 1) = the
  number of hidden directions: measured 2.00 vs the slice's 1 -> exactly one hidden
  imaginary direction. "The line is a slice of the cone," with beta as the dimension count.

SCOPE (first-class): this pins a SYMMETRY-CLASS FAMILY (anti-commuting antiunitary,
chiral/BdG-type), not zeta's Cartan class, and constructs no operator -- the arithmetic
content (orbit lengths log p with weights p^{-k/2}) remains the open problem. The ensemble
realizes the pairing mechanism for the FULL spectrum; the zeros' half-spectrum realness at
prime frequencies additionally uses the real von Mangoldt weights (self-duality). Proves
nothing about RH. Seed 20260423.
"""
import numpy as np
from sympy import Matrix, I, symbols, simplify, zeros as szeros

SEED = 20260423
rng = np.random.default_rng(SEED)

print("=" * 74)
print("THE WALL'S RESOLUTION CLASS -- anti-commuting antiunitary, exact + ensemble")
print("=" * 74)

# ---------------- M: exact miniature ----------------------------------------
x, y, z = symbols("x y z", real=True)
sx = Matrix([[0, 1], [1, 0]])
sy = Matrix([[0, -I], [I, 0]])
sz = Matrix([[1, 0], [0, -1]])
H = x*sz + y*sx + z*sy                      # active block of the hypercone family

anti = simplify(sy * H.conjugate() * sy.inv() + H) == szeros(2, 2)   # C H* C^-1 = -H
Csq = simplify(sy * sy.conjugate())                                   # C^2 = U U-bar
lam = symbols("lam")
cp = H.charpoly(lam).as_expr()
even = simplify(cp - (lam**2 - (x**2 + y**2 + z**2))) == 0            # paired spectrum
comm_forces_real = simplify(H.conjugate() - H) != szeros(2, 2)        # T=K commuting needs z=0
comm_z0 = simplify((H.conjugate() - H).subs(z, 0)) == szeros(2, 2)

print("\n[M] exact miniature H(x,y,z) = x*sz + y*sx + z*sy (hypercone active block)")
print(f"    anti-commuting antiunitary C = sy o K:  C H* C^-1 = -H  : {anti}")
print(f"    C^2 = {Csq.tolist()}  (= -1: BdG-type)")
print(f"    charpoly = lam^2 - (x^2+y^2+z^2)  (spectrum +-paired, all params): {even}")
print("    degeneracy locus x=y=z=0: codim 3  -> beta = 2")
print(f"    control: COMMUTING antiunitary T=K demands H real, i.e. z=0     : "
      f"{comm_forces_real and comm_z0}")
print("    -> commuting antiunitary kills the third direction (codim 2, beta=1);")
print("       anti-commuting keeps it (codim 3, beta=2) while pairing the spectrum.")

# ---------------- E: ensemble discriminator ---------------------------------
def unfolded_spacings(ev):
    """bulk spacings normalized by a running local mean."""
    ev = np.sort(ev)
    n = len(ev)
    ev = ev[int(0.2*n):int(0.8*n)]
    s = np.diff(ev)
    k = 25
    loc = np.convolve(s, np.ones(k)/k, mode="same")
    return s / loc

def beta_fit(spacings):
    """fit count(s < x) ~ x^{beta+1} on the small-s tail."""
    xs = np.linspace(0.08, 0.45, 14)
    cnt = np.array([np.sum(spacings < xv) for xv in xs], dtype=float)
    good = cnt > 20
    slope = np.polyfit(np.log(xs[good]), np.log(cnt[good]), 1)[0]
    return slope - 1.0

def witness_ratio(ev, us=(0.7, 1.3, 2.9)):
    """|Im W| / |W| for W(u) = sum exp(i ev u) over the FULL spectrum."""
    r = []
    for u in us:
        w = np.exp(1j*ev*u).sum()
        r.append(abs(w.imag) / (abs(w) + 1e-300))
    return float(np.mean(r))

DRAWS, N = 8, 800
res = {}
sp, wr, pairdef = [], [], 0.0
for _ in range(DRAWS):                       # GOE
    A = rng.standard_normal((N, N))
    ev = np.linalg.eigvalsh((A + A.T)/2)
    sp.append(unfolded_spacings(ev)); wr.append(witness_ratio(ev))
res["GOE"] = (beta_fit(np.concatenate(sp)), np.mean(wr), None)

sp, wr = [], []
for _ in range(DRAWS):                       # GUE
    A = rng.standard_normal((N, N)) + 1j*rng.standard_normal((N, N))
    ev = np.linalg.eigvalsh((A + A.conj().T)/2)
    sp.append(unfolded_spacings(ev)); wr.append(witness_ratio(ev))
res["GUE"] = (beta_fit(np.concatenate(sp)), np.mean(wr), None)

sp, wr, pd = [], [], []
n = 600
for _ in range(DRAWS):                       # chiral GUE: H = [[0,A],[A+,0]]
    A = (rng.standard_normal((n, n)) + 1j*rng.standard_normal((n, n)))/np.sqrt(2)
    Hc = np.block([[np.zeros((n, n)), A], [A.conj().T, np.zeros((n, n))]])
    ev = np.linalg.eigvalsh(Hc)
    pd.append(np.max(np.abs(np.sort(ev) + np.sort(ev)[::-1])))        # +- pairing defect
    pos = np.sort(ev[ev > 0])
    pos = pos[int(0.05*len(pos)):int(0.95*len(pos))]                  # drop hard/soft edges
    s = np.diff(pos); k = 25
    s = s / np.convolve(s, np.ones(k)/k, mode="same")
    sp.append(s); wr.append(witness_ratio(ev))
res["chGUE"] = (beta_fit(np.concatenate(sp)), np.mean(wr), np.max(pd))

print("\n[E] ensemble discriminator (8 draws each; W over the full spectrum)")
print(f"    {'ensemble':>9} {'beta fit':>9} {'|Im W|/|W|':>12} {'pairing defect':>15}"
      f"  {'passes A (real W)':>18} {'passes B (beta=2)':>18}")
for name, (b, w, p) in res.items():
    pa = w < 1e-10
    pb = abs(b - 2.0) < 0.35
    pstr = f"{p:.1e}" if p is not None else "unpaired"
    print(f"    {name:>9} {b:>9.2f} {w:>12.2e} {pstr:>15}  {str(pa):>18} {str(pb):>18}")
both = [k for k, (b, w, _) in res.items() if w < 1e-10 and abs(b - 2.0) < 0.35]
print(f"    passes BOTH wall constraints: {both}")

# ---------------- data anchor ------------------------------------------------
print("\n[data] zeros (hp_operator_constraint.py): |Im W|/|Re W| = 0.0001, beta = 2.00")
print("       hypercone C3 (companion branch):    beta = 2.019 -> codim-3 shadow")
print("""
VERDICT: the wall is a CLASS SELECTION, not a contradiction. Real witness + beta=2
coexist exactly when the antiunitary symmetry ANTI-commutes (pairs the spectrum,
preserves codim 3); a commuting antiunitary would confine the family to the real
slice (codim 2, beta=1). The amplitudes live on the real slice (Fix(iota)); the
repulsion counts the hidden imaginary direction -- "the line is a slice of the cone,"
with beta as the dimension counter. Constructs no operator; the arithmetic (orbit
lengths log p, weights p^{-k/2}) remains open. Proves nothing about RH.""")
