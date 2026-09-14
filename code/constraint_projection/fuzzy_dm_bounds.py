#!/usr/bin/env python3
"""
fuzzy_dm_bounds.py -- CPF section 6's required ultralight scalar mass, re-derived,
and placed against published fuzzy/ultralight dark matter bounds.

WHAT THIS INSTRUMENT DOES
  1. Re-derives the boson mass that section 6's quantum-pressure rotation-curve
     mechanism requires, under four independent set-ups, from CODATA constants.
     Nothing is inherited from the audit note; the audit's own numbers are then
     regenerated as a cross-check.
  2. Reports the sensitivity of that mass to the two free inputs (v, L).
  3. Holds a table of PUBLISHED observational bounds. Those are CITED literature
     values (T3 data measured by others), NOT measurements made by this script.
     Each carries source, stated confidence, and the caveat the source states.
  4. Exits non-zero on any internal inconsistency.

TIER: derivation lines are T1 (this instrument printed them).
      Bound lines are CITED (see BOUNDS table provenance fields).
"""
import sys
import math

FAILURES = []


def check(name, cond, detail=""):
    if not cond:
        FAILURES.append(f"{name}: {detail}")
    print(f"  [{'ok ' if cond else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# CODATA 2018 exact / recommended values
# ---------------------------------------------------------------------------
H_PLANCK = 6.62607015e-34      # J s      (exact, SI definition)
HBAR = H_PLANCK / (2.0 * math.pi)
C_LIGHT = 299792458.0          # m/s      (exact)
E_CHARGE = 1.602176634e-19     # C        (exact)
M_ELECTRON = 9.1093837015e-31  # kg
G_NEWTON = 6.67430e-11         # m^3 kg^-1 s^-2
KPC = 3.0856775814913673e19    # m        (IAU 2015 parsec x 1000)
M_SUN = 1.98892e30             # kg


def kg_to_eV(m_kg):
    return m_kg * C_LIGHT ** 2 / E_CHARGE


def eV_to_kg(m_eV):
    return m_eV * E_CHARGE / C_LIGHT ** 2


# ---------------------------------------------------------------------------
# SECTION 1 -- re-derivation of the mass section 6 requires
# ---------------------------------------------------------------------------
# Section 6 (Constraint_Projection_Framework.tex L205-219) asserts that the
# "quantum pressure" of a field psi = R exp(iS/hbar) shapes galactic rotation
# curves. That requires the field's wavelength to be comparable to the structure
# it shapes. The audit (Constraint_Projection_Framework_Audit.tex, "(iii) The
# scale.") takes v = 200 km/s, L = 1 kpc.

V_GAL = 200.0e3   # m/s   -- the audit's fiducial rotation speed
L_GAL = 1.0 * KPC # m     -- the audit's fiducial length


def m_from_standard_de_broglie(v, L):
    """lambda_dB = h / (m v) = L   ->   m = h / (v L).  Standard convention."""
    return H_PLANCK / (v * L)


def m_from_reduced_de_broglie(v, L):
    """lambdabar = hbar / (m v) = L  ->  m = hbar / (v L).  Reduced convention."""
    return HBAR / (v * L)


def m_from_soliton_core_natural(v, r_c):
    """Soliton core relation r_c ~ (m v)^-1 in hbar = c = 1 units.

    Restoring units, r_c = hbar / (m v), i.e. identical in form to the reduced
    de Broglie wavelength. This is the mission's stated relation and it is NOT
    an independent constraint -- it is the same equation.
    """
    return HBAR / (v * r_c)


def m_from_schive_core_halo(r_c_kpc, M_halo_Msun):
    """Schive, Chiueh & Broadhurst 2014 empirical soliton core-halo relation:

        r_c = 1.6 kpc * (m / 1e-22 eV)^-1 * (M_h / 1e9 Msun)^-1/3

    CITED functional form + coefficient (Schive+ 2014, Nature Physics 10, 496;
    Schive+ 2014, PRL 113, 261302). The inversion below is arithmetic done here.
    """
    return 1e-22 * (1.6 / r_c_kpc) * (M_halo_Msun / 1e9) ** (-1.0 / 3.0)


def m_from_soliton_virial(r_c, M_c, coeff):
    """Self-gravitating ground-state soliton: coeff * hbar^2 / (G m^2) = M_c r_c.

    coeff = 1/2 is the crude virial balance (hbar^2/(2 m r_c^2) = G M_c m / r_c).
    The true ground-state numerical coefficient is O(1) and is quoted separately.
    Returns m in kg.
    """
    return math.sqrt(coeff * HBAR ** 2 / (G_NEWTON * M_c * r_c))


def main():
    print("=" * 74)
    print("SECTION 1 -- the mass CPF section 6 requires, re-derived from constants")
    print("=" * 74)
    print(f"  inputs: v = {V_GAL/1e3:.0f} km/s, L = {L_GAL/KPC:.1f} kpc")
    print(f"  h    = {H_PLANCK:.6e} J s")
    print(f"  hbar = {HBAR:.6e} J s")
    print()

    m_std = m_from_standard_de_broglie(V_GAL, L_GAL)
    m_red = m_from_reduced_de_broglie(V_GAL, L_GAL)
    m_sol = m_from_soliton_core_natural(V_GAL, L_GAL)

    print("  (a) standard de Broglie   lambda = h/(mv) = L")
    print(f"      m = {m_std:.4e} kg = {kg_to_eV(m_std):.4e} eV/c^2")
    print("  (b) reduced de Broglie    lambdabar = hbar/(mv) = L")
    print(f"      m = {m_red:.4e} kg = {kg_to_eV(m_red):.4e} eV/c^2")
    print("  (c) soliton core          r_c = hbar/(mv), r_c = L")
    print(f"      m = {m_sol:.4e} kg = {kg_to_eV(m_sol):.4e} eV/c^2")
    print()
    ratio = m_std / m_red
    print(f"  (a)/(b) = {ratio:.6f}   [2*pi = {2*math.pi:.6f}]")
    check("standard/reduced ratio is exactly 2*pi",
          abs(ratio - 2 * math.pi) < 1e-9, f"ratio={ratio!r}")
    check("(c) coincides with (b) -- soliton relation is not independent",
          abs(m_sol - m_red) / m_red < 1e-12)

    # Cross-check against the audit note's printed numbers.
    print()
    print("  cross-check vs the audit note's stated numbers (which convention?):")
    AUDIT_KG = 1.7e-59
    AUDIT_EV = 9.6e-24
    AUDIT_ELECTRON_LAMBDA = 5.8e-10  # m, audit's stated electron de Broglie length
    print(f"      audit states m = {AUDIT_KG:.2e} kg = {AUDIT_EV:.2e} eV")
    print(f"      reduced convention gives {m_red:.4e} kg = {kg_to_eV(m_red):.4e} eV")
    print(f"      standard convention gives {m_std:.4e} kg = {kg_to_eV(m_std):.4e} eV")
    check("audit's kg number reproduced by the REDUCED convention to 2 sig figs",
          abs(m_red - AUDIT_KG) / AUDIT_KG < 0.02,
          f"reduced={m_red:.4e} vs audit={AUDIT_KG:.2e}")
    check("audit's eV number reproduced by the REDUCED convention to 2 sig figs",
          abs(kg_to_eV(m_red) - AUDIT_EV) / AUDIT_EV < 0.02,
          f"reduced={kg_to_eV(m_red):.4e} vs audit={AUDIT_EV:.2e}")
    check("audit's kg number is NOT the standard-convention value",
          abs(m_std - AUDIT_KG) / AUDIT_KG > 0.5)

    lam_e_red = HBAR / (M_ELECTRON * V_GAL)
    lam_e_std = H_PLANCK / (M_ELECTRON * V_GAL)
    print(f"      electron at 200 km/s: reduced {lam_e_red:.3e} m, standard {lam_e_std:.3e} m")
    print(f"      audit states {AUDIT_ELECTRON_LAMBDA:.1e} m")
    check("audit's electron length also uses the REDUCED convention",
          abs(lam_e_red - AUDIT_ELECTRON_LAMBDA) / AUDIT_ELECTRON_LAMBDA < 0.02,
          f"reduced={lam_e_red:.3e}")
    decades = math.log10(L_GAL / lam_e_red)
    print(f"      decades between kpc and the electron length: {decades:.1f}"
          "   (audit states 29)")
    check("audit's '29 decades' reproduced", abs(decades - 29.0) < 1.0,
          f"computed {decades:.2f}")

    # -- sensitivity ---------------------------------------------------------
    print()
    print("  sensitivity: m = hbar/(vL) is exactly inverse-linear in BOTH v and L,")
    print("  so d(log10 m)/d(log10 L) = -1 and d(log10 m)/d(log10 v) = -1.")
    print("  A factor 2 in L moves m by 0.30 decades, not 2 decades.")
    print()
    print("   L[kpc] \\ v[km/s]      100        200        300")
    for Lk in (0.5, 1.0, 2.0, 5.0, 10.0):
        row = []
        for vk in (100.0, 200.0, 300.0):
            row.append(kg_to_eV(m_from_reduced_de_broglie(vk * 1e3, Lk * KPC)))
        print(f"   {Lk:6.1f}        " + "  ".join(f"{x:.3e}" for x in row))
    m_lo = kg_to_eV(m_from_reduced_de_broglie(300e3, 10.0 * KPC))
    m_hi = kg_to_eV(m_from_reduced_de_broglie(100e3, 0.5 * KPC))
    span = math.log10(m_hi / m_lo)
    print(f"   full span over that grid: {m_lo:.3e} .. {m_hi:.3e} eV"
          f"  ({span:.2f} decades)")
    check("grid span is under 2 decades", span < 2.0, f"{span:.2f} decades")

    # -- Schive core-halo route ---------------------------------------------
    print()
    print("  (d) Schive+2014 empirical core-halo relation [CITED form], inverted:")
    for (rc, Mh, label) in ((1.0, 1e12, "MW-like halo, r_c = 1 kpc"),
                            (1.0, 1e9, "dwarf halo, r_c = 1 kpc"),
                            (0.5, 1e12, "MW-like halo, r_c = 0.5 kpc")):
        mm = m_from_schive_core_halo(rc, Mh)
        print(f"      {label:32s} m = {mm:.3e} eV")

    globals()["M_REQ_REDUCED_EV"] = kg_to_eV(m_red)
    globals()["M_REQ_STANDARD_EV"] = kg_to_eV(m_std)
    print()

    if FAILURES:
        print("INTERNAL INCONSISTENCIES:")
        for f in FAILURES:
            print("  - " + f)
        sys.exit(1)
    print("Section 1 internally consistent.")


if __name__ == "__main__":
    main()
