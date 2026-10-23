# Co-governed and enforced under the Sovereign Integrity Protocol License (SIP License v1.1):
# https://github.com/tensorrent/ACS-Framework/blob/main/LICENSE
"""
RECONSTRUCTED 2026-10-22 from the ledger's description, NOT the original.

Original: `/tmp/q7_neutrino.py`, run 2026-06-06 on an external session machine and never
committed (docs/Elimination_Ledger.md:287, provenance note :14-21). Re-authored from the
ledger entry "Target Q7: neutrino seesaw / X-ray tension" (docs/Elimination_Ledger.md:285-303)
only. Agreement below is agreement with the recorded outputs, not a certificate of the
original script or of the physics reading.

Inputs exactly as the ledger states them (:287-289):
  naive sin^2(2 theta) = 4e-6 (the framework's stated value), X-ray bound 1e-10,
  PDG M_W = 80.4 GeV, v = 246.22 GeV, and a generic seesaw times the stated (M_W/M_WR)^2
  suppression -- "NOT the full FF06 mechanism -- verdict is conditional on this reading".

One relation the ledger does not write out: v_R from M_WR. The recorded pair
(M_WR >~ 16 TeV, v_R >~ 49 TeV) is reproduced by M_WR = g v_R / 2 with g = 2 M_W / v,
i.e. v_R = v * M_WR / M_W (equal left/right gauge couplings). That is the assumption here.

The ledger also says independent bounds (LHC ~5-6 TeV; K_L -> mu e pushing v_R to
>~ 100s of TeV) "already exceed" the requirement and that the suppression clears the
bound "by orders of magnitude for any realistic v_R" (:291-293). Those two sentences are
quantitative, so the margins are printed below rather than restated.

Seed convention 20260423 (nothing below is stochastic). Writes nothing; stdout only.
"""
import math

import numpy as np

np.random.default_rng(20260423)  # house seed; no stochastic step in this script

SIN2_NAIVE = 4e-6
XRAY_BOUND = 1e-10
M_W = 80.4      # GeV, PDG value as stated in the ledger
V_EW = 246.22   # GeV


def main():
    print("Q7 neutrino seesaw / X-ray -- RECONSTRUCTION (not the 2026-06-06 original)")
    print("=" * 78)
    s_req = XRAY_BOUND / SIN2_NAIVE
    m_wr_min = M_W / math.sqrt(s_req)            # GeV
    v_r_min = V_EW * m_wr_min / M_W              # GeV
    print(f"required suppression S < {s_req:.4e}")
    print(f"=> M_WR > M_W / sqrt(S) = {m_wr_min / 1e3:.4f} TeV")
    print(f"=> v_R  > v * M_WR / M_W = {v_r_min / 1e3:.4f} TeV")
    print()

    print("independent bounds vs the requirement (ledger :291-293):")
    for label, m_wr in [("LHC M_WR ~5 TeV", 5e3), ("LHC M_WR ~6 TeV", 6e3)]:
        print(f"  {label:<26} >= required M_WR {m_wr_min / 1e3:.2f} TeV ? {m_wr >= m_wr_min}")
    print()

    print("margin below the X-ray bound as a function of v_R (bound / predicted mixing):")
    print(f"  {'v_R [TeV]':>10}{'M_WR [TeV]':>12}{'S=(M_W/M_WR)^2':>17}{'sin^2(2th)':>13}{'margin':>10}")
    for v_r_tev in [49.24, 100, 300, 1000]:
        m_wr = M_W * v_r_tev * 1e3 / V_EW
        s = (M_W / m_wr) ** 2
        mix = SIN2_NAIVE * s
        print(f"  {v_r_tev:>10.2f}{m_wr / 1e3:>12.3f}{s:>17.3e}{mix:>13.3e}{XRAY_BOUND / mix:>10.2f}")
    print()
    print("Ledger cells (docs/Elimination_Ledger.md:291) for comparison:")
    print("  S < 2.5e-5;  M_WR >~ 16 TeV;  v_R >~ 49 TeV")


if __name__ == "__main__":
    main()
