# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
def _d(p): return _os.path.join(_HERE, "data_zeros", p)

r"""
HARDENED CHARACTER TWIST  --  push rung-2 from T3 to T1, and test the k=3 parity law.

hp_ladder_character_twist.py established the chi^k twist on rungs 1-2 but the rung-2 phase
alignment was unresolved with the earlier short tables. The September 2026
replacement uses finite certified lists (146 mod-5 and 157 mod-7 zeros), and this:

  (1) recomputes the rung-1/2 phase-demod resultants at larger N (rung-2 should now clear
      its off-diagonal decisively);
  (2) extends to a 3x3 demod table R(rung k, demod chi^m) for k,m in {1,2,3}, predicted
      DIAGONAL (rung k aligns under chi^k);
  (3) tests the extended parity law for the commutator ||[iota,T]||_k = mean_p|Im chi(p)^k|:
        ||[iota,T]||_k = 0  iff  order(chi) | 2k.
      New rung-3 prediction: order-6 (mod 7) COMMUTES on rung 3 (6|6); order-4 (mod 5) does
      NOT (4 does not divide 6). A clean, falsifiable check the flat picture cannot make.

Reproducible: seed 20260423. Proves nothing about RH; tests the twist structure of the object.
"""
import numpy as np
from math import gcd

def build_chi(q, gen, order):
    units = [a for a in range(1, q) if gcd(a, q) == 1]
    dlog = {}; val = 1
    for j in range(len(units)):
        dlog[val % q] = j; val = (val * gen) % q
    omega = np.exp(2j*np.pi/order)
    def chi(p):
        if gcd(p, q) > 1: return 0+0j
        return omega**dlog[p % q]
    return chi

def Wc(gam, u):
    return np.exp(1j*u*gam).sum()

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

def load_best(ext, orig):
    """Prefer the extended (larger) zero file; fall back to the original."""
    fe, fo = _d(ext), _d(orig)
    if _os.path.exists(fe):
        z = np.loadtxt(fe); z = z[np.isfinite(z)]
        if len(z) >= len(np.loadtxt(fo)):
            return z, "ext"
    z = np.loadtxt(fo); return z[np.isfinite(z)], "orig"

cases = [
    ("mod 5 order 4", "cyclotomic_5/zeros_chi_5_order4_ext.txt",
     "cyclotomic_5/zeros_chi_5_order4.txt", 5, 2, 4),
    ("mod 7 order 6", "cyclotomic_7/zeros_chi_7_order6_ext.txt",
     "cyclotomic_7/zeros_chi_7_order6.txt", 7, 3, 6),
]

for title, ext, orig, q, gen, order in cases:
    gam, src = load_best(ext, orig)
    chi = build_chi(q, gen, order)
    npr = sum(1 for p in PRIMES if chi(int(p)) != 0)
    floor = 1/np.sqrt(npr)
    print("=" * 72)
    print(f"{title}   N={len(gam)} zeros ({src})   demod floor 1/sqrt(#p)={floor:.2f}")

    # 3x3 demod table
    print("  R(rung k, demod chi^m):")
    print(f"  {'':>8} " + " ".join(f"{'chi^'+str(m):>9}" for m in (1, 2, 3)))
    Rtab = {}
    for k in (1, 2, 3):
        phases, chis = [], []
        for p in PRIMES:
            c = chi(int(p))
            if c == 0: continue
            w = Wc(gam, k*np.log(p))
            phases.append(w/abs(w)); chis.append(np.conj(c))
        phases = np.array(phases); chis = np.array(chis)
        row = []
        for m in (1, 2, 3):
            Rtab[(k, m)] = abs(((chis**m) * phases).mean()); row.append(Rtab[(k, m)])
        star = "  <- diag" if np.argmax(row) == k-1 else "  (off-diag peak)"
        print(f"  rung {k:>1} " + " ".join(f"{r:>9.3f}" for r in row) + star)
    diag = all(np.argmax([Rtab[(k, m)] for m in (1, 2, 3)]) == k-1 for k in (1, 2, 3))
    print(f"  3x3 table diagonal (rung k aligns under chi^k): {'YES' if diag else 'partial'}")
    # per-rung resolution: does rung k clear the demod floor under its own power chi^k?
    print("  resolution (R under own power chi^k vs floor):")
    for k in (1, 2, 3):
        r = Rtab[(k, k)]
        status = "RESOLVED" if r > 2 * floor else ("weak" if r > 1.3 * floor else "at floor")
        print(f"    rung {k}: R(chi^{k}) = {r:.3f}  -> {status}")

    # commutator parity law
    print("  commutator ||[iota,T]||_k = mean_p |Im chi(p)^k|   (0 iff order(chi)|2k):")
    for k in (1, 2, 3):
        cn = np.mean([abs((chi(int(p))**k).imag) for p in PRIMES if chi(int(p)) != 0])
        divides = (2*k) % order == 0                        # order(chi) | 2k
        pred = "0 (commutes)" if divides else ">0 (does not)"
        ok = (cn < 1e-9) == divides
        print(f"    k={k}: {cn:.3f}   predict {pred:>14}   order|2k={divides}  {'OK' if ok else 'MISS'}")
    print()

print("=" * 72)
print("""READING:
  The values and resolution labels above are calculated from the loaded tables.
  The 2/sqrt(number of primes) threshold is a heuristic comparison, not a
  calibrated significance test. A finite resultant does not establish an
  infinite explicit formula or a natural spectral operator.
  The displayed parity quantity is computed directly from character values;
  it is an algebraic control and does not depend on the supplied zero list.
  Certified replacement data and before/after results are recorded in
  docs/frontier/2026-09-13-lfunction-delta/.""")
