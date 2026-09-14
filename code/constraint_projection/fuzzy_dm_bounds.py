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


# ---------------------------------------------------------------------------
# SECTION 2 -- the published bounds table.
#
# EVERY ROW HERE IS *CITED* LITERATURE. Nothing in BOUNDS was measured by this
# script or by its author. Each row carries the source, the confidence level
# the source states, and the caveat the source states about itself. The
# arithmetic that compares these numbers to the Section 1 bracket IS done here
# and is tagged T1 in the report.
#
# kind:
#   "lower"  -- a lower limit: masses BELOW value_eV are excluded
#   "upper"  -- an upper limit: masses ABOVE value_eV are excluded
#   "band"   -- an exclusion interval (lo, hi): masses inside are excluded
#   "pref"   -- a preferred/central value, NOT a limit; never used for verdicts
# ---------------------------------------------------------------------------

BOUNDS = [
    # ---- Lyman-alpha forest -------------------------------------------------
    dict(key="rogers_peiris_2021", probe="lyman-alpha", kind="lower",
         value_eV=2.0e-20, cl="95% credible",
         source="Rogers & Peiris 2021, PRL 126 071302 (arXiv:2007.12705v3)",
         quote="log(m_a[eV]) > -19.64, which equates to m_a > 2 x 10^-20 eV",
         caveat="quantum pressure modelled only via modified initial conditions at z=99; "
                "bounds weaken if ULAs are not all of the DM; prior is uniform in "
                "log(m_a) on [-22,-19] so the CPF bracket lies below the sampled range",
         provenance="CITED"),
    dict(key="rogers_peiris_2021_kmax008", probe="lyman-alpha", kind="lower",
         value_eV=10 ** -20.64, cl="95% credible",
         source="Rogers & Peiris 2021, footnote 4",
         quote="for k_max = 0.08 s km^-1, log(m_a[eV]) > -20.64",
         caveat="the authors' own weakened variant, restricting to the k-range of "
                "previous-generation analyses; shows a decade of the headline bound "
                "lives in the smallest-scale bins",
         provenance="CITED"),
    dict(key="irsic_2017_combined", probe="lyman-alpha", kind="lower",
         value_eV=20.0e-22, cl="2 sigma (95%)",
         source="Irsic+ 2017, PRL 119 031302 (arXiv:1703.04683v2)",
         quote="m_FDM > 20 x 10^-22 eV (2 sigma C.L.), XQ-100 + HIRES/MIKE, T_0 per z-bin",
         caveat="the paper's own 'most conservative' case, allowing IGM temperature "
                "jumps of 5000 K which it calls 'not physically plausible'; no quantum "
                "pressure term in the hydrodynamics",
         provenance="CITED"),
    dict(key="irsic_2017_reference", probe="lyman-alpha", kind="lower",
         value_eV=37.5e-22, cl="2 sigma (95%)",
         source="Irsic+ 2017, Table I 'ref.' column",
         quote="combined 37.5 x 10^-22 eV under a power-law thermal history",
         caveat="assumes smooth power-law T_0(z); roughly doubles the conservative limit",
         provenance="CITED"),
    dict(key="irsic_2017_xq100_planck", probe="lyman-alpha", kind="lower",
         value_eV=2.7e-22, cl="2 sigma (95%)",
         source="Irsic+ 2017, Table I, XQ-100 alone with Planck priors",
         quote="XQ-100 2.7 x 10^-22 eV with Planck priors",
         caveat="WEAKEST single published Lyman-alpha entry located in this survey; "
                "one dataset only, quoted by nobody as a headline result. Carried "
                "deliberately as the adversarial-to-exclusion case",
         provenance="CITED"),
    dict(key="armengaud_2017_sdss", probe="lyman-alpha", kind="lower",
         value_eV=2.3e-21, cl="95% CL",
         source="Armengaud+ 2017, MNRAS 471 4606 (arXiv:1703.09126v2)",
         quote="we exclude FDM masses in the range 10^-22 < m_a < 2.3 x 10^-21 eV at 95% CL",
         caveat="neglects the quantum force in the Madelung equation; the paper states "
                "that for m_a <~ 1e-22 eV the quantum term may impact the non-linear "
                "P(k) and should be included -- i.e. below the CPF bracket's ceiling",
         provenance="CITED"),
    dict(key="armengaud_2017_highres", probe="lyman-alpha", kind="lower",
         value_eV=2.9e-21, cl="95% CL",
         source="Armengaud+ 2017, SDSS + XQ-100 + HIRES/MIKE",
         quote="extends the exclusion range up to m_a = 2.9 x 10^-21 eV",
         caveat="same quantum-force approximation; patchy reionization not modelled",
         provenance="CITED"),
    dict(key="armengaud_2017_planck", probe="lyman-alpha", kind="lower",
         value_eV=1.3e-21, cl="95% CL",
         source="Armengaud+ 2017, SDSS alone with Planck priors",
         quote="the looser bound m_a > 1.3 x 10^-21 eV if one includes Planck",
         caveat="the paper's own loosest variant; n_s from Lyman-alpha alone (0.94) is "
                "in slight tension with the CMB value (0.97)",
         provenance="CITED"),

    # ---- dwarf spheroidal / ultra-faint dwarf kinematics --------------------
    dict(key="dalal_kravtsov_2022", probe="dwarf-heating", kind="lower",
         value_eV=3.0e-19, cl="99% confidence",
         source="Dalal & Kravtsov 2022, PRD (arXiv:2203.05750v2)",
         quote="m_FDM > 3 x 10^-19 eV at 99% confidence (Segue 1 + Segue 2)",
         caveat="stated by the authors as conservative: soliton heating neglected, "
                "initial anisotropy neglected, binaries inflate the measured dispersion, "
                "prior p ~ m^-2 favours light masses. Open questions they name: whether "
                "Segue 2 is a galaxy or a star cluster, and tidal stripping; they also "
                "record an unresolved disagreement with a rival 18-UFD soliton analysis",
         provenance="CITED"),
    dict(key="dalal_kravtsov_2022_other_ufds", probe="dwarf-heating", kind="lower",
         value_eV=1.0e-20, cl="stated fallback (no C.L. attached)",
         source="Dalal & Kravtsov 2022, discussion section",
         quote="even if we removed the constraints from Segue 1 and 2, FDM with "
               "m < 10^-20 eV would remain excluded by these other UFDs",
         caveat="an order-of-magnitude argument from Boeetes I / Leo IV / Carina, not a "
                "full likelihood; carried as the Segue-independent fallback",
         provenance="CITED"),
    dict(key="gonzalez_morales_2017", probe="dwarf-core", kind="upper",
         value_eV=0.4e-22, cl="97.5% C.L.",
         source="Gonzalez-Morales, Marsh, Penarrubia & Urena-Lopez 2017, MNRAS "
                "(arXiv:1609.05856v2)",
         quote="m_a < 0.4 x 10^-22 eV at 97.5% confidence (Fornax + Sculptor, "
               "<sigma^2_los>-fit)",
         caveat="THE SOURCE REPORTS ITS OWN BOUND AS IN CONFLICT WITH STRUCTURE COUNTS: "
                "'m_22 < 0.4 cannot even give the eight classical dSphs' and it is "
                "'inconsistent with a conservative bound of m_a > 1 x 10^-22 eV from "
                "cosmology'; they name the situation a Catch-22",
         provenance="CITED"),
    dict(key="marsh_pop_2015", probe="dwarf-core", kind="upper",
         value_eV=1.1e-22, cl="95% C.L.",
         source="Marsh & Pop 2015, as quoted by Gonzalez-Morales+ 2017",
         quote="limits m_a < 1.1 x 10^-22 eV at a 95% confidence level",
         caveat="uses the WP11 virial mass estimator; GM+17 find this method slightly "
                "biased toward larger axion masses",
         provenance="CITED"),
    dict(key="gonzalez_morales_2017_fornax", probe="dwarf-core", kind="upper",
         value_eV=0.48e-22, cl="97.5% C.L.",
         source="Gonzalez-Morales+ 2017, Fornax alone",
         quote="m_22 < 0.48 for Fornax",
         caveat="single galaxy; same Catch-22 caveat as the joint bound",
         provenance="CITED"),
    dict(key="gonzalez_morales_2017_sculptor", probe="dwarf-core", kind="upper",
         value_eV=0.79e-22, cl="97.5% C.L.",
         source="Gonzalez-Morales+ 2017, Sculptor alone",
         quote="m_22 < 0.79 for Sculptor",
         caveat="single galaxy; same Catch-22 caveat as the joint bound",
         provenance="CITED"),

    # ---- black hole superradiance ------------------------------------------
    dict(key="davoudiasl_denton_2019_scalar", probe="superradiance", kind="band",
         value_eV=(2.9e-21, 4.6e-21), cl="1 sigma",
         source="Davoudiasl & Denton 2019, PRL (arXiv:1904.09242v1)",
         quote="2.9 x 10^-21 eV < mu_S < 4.6 x 10^-21 eV (M87*, M = 6.5e9 Msun)",
         caveat="scalar case, the one that applies to CPF section 6's field; assumes "
                "negligible self-coupling; the scalar constraint exists only for "
                "|a*| > 0.55 and EHT itself supports only |a*| >~ 0.5, the fiducial "
                "a* = 0.9 +- 0.1 coming from a separate analysis",
         provenance="CITED"),
    dict(key="davoudiasl_denton_2019_vector", probe="superradiance", kind="band",
         value_eV=(8.5e-22, 4.6e-21), cl="1 sigma",
         source="Davoudiasl & Denton 2019",
         quote="8.5 x 10^-22 eV < mu_V < 4.6 x 10^-21 eV",
         caveat="VECTOR bosons only -- NOT applicable to CPF section 6, whose field is "
                "a scalar psi = R exp(iS/hbar). Listed for completeness",
         provenance="CITED"),
    dict(key="stott_marsh_2018_smbh", probe="superradiance", kind="band",
         value_eV=(7.0e-20, 1.0e-16), cl="95% C.L.",
         source="Stott & Marsh 2018 (arXiv:1805.02016v2)",
         quote="7 x 10^-20 eV < mu_ax/eV < 1 x 10^-16 at the 95% C.L. (supermassive BHs)",
         caveat="zero self-coupling, valid for f_a >~ 1e14 GeV; sparse SMBH data makes "
                "the exclusion probability oscillatory and driven by individual BHs; "
                "BH spin systematics are the dominant error and are worst for spin-0",
         provenance="CITED"),
    dict(key="stott_marsh_2018_stellar", probe="superradiance", kind="band",
         value_eV=(7.0e-14, 2.0e-11), cl="95% C.L.",
         source="Stott & Marsh 2018",
         quote="7 x 10^-14 eV < mu_ax/eV < 2 x 10^-11 at the 95% C.L. (stellar-mass BHs)",
         caveat="zero self-coupling; ten decades above anything relevant here, listed "
                "to show the full reach of the probe",
         provenance="CITED"),

    # ---- preferences, NOT limits -------------------------------------------
    dict(key="schive_2014_fornax", probe="dwarf-core", kind="pref",
         value_eV=8.1e-23, cl="+1.6/-1.7 e-23 (quoted uncertainty)",
         source="Schive+ 2014a Fornax Jeans analysis, as quoted by "
                "Gonzalez-Morales+ 2017",
         quote="m_a = 8.1 (+1.6/-1.7) x 10^-23 eV",
         caveat="a detection claim, not a limit; GM+17 report it as >~2 sigma discrepant "
                "with their own bound and argue Jeans analysis is biased by the "
                "mass-anisotropy degeneracy",
         provenance="CITED"),
    dict(key="gonzalez_morales_2017_jeans", probe="dwarf-core", kind="pref",
         value_eV=2.44e-22, cl="+1.3/-0.6 e-22",
         source="Gonzalez-Morales+ 2017, joint Jeans analysis of 8 classical dSphs",
         quote="m_a = 2.44 (+1.3/-0.6) x 10^-22 eV",
         caveat="the same paper argues this number is biased by the beta-degeneracy and "
                "should not be read at face value",
         provenance="CITED"),
    dict(key="calabrese_spergel_2016", probe="dwarf-core", kind="pref",
         value_eV=4.65e-22, cl="range 3.7-5.6 e-22",
         source="Calabrese & Spergel 2016, as quoted by Gonzalez-Morales+ 2017",
         quote="explaining the half-light mass in ultra-faint dwarfs requires "
               "m_a ~ 3.7 - 5.6 x 10^-22 eV",
         caveat="in tension with GM+17's own upper limit; quoted by GM+17 as such",
         provenance="CITED"),
]


def verdict(kind, value_eV, m_eV):
    """Is mass m_eV excluded by this bound? Returns 'EXCLUDED' or 'allowed'."""
    if kind == "lower":
        return "EXCLUDED" if m_eV < value_eV else "allowed"
    if kind == "upper":
        return "EXCLUDED" if m_eV > value_eV else "allowed"
    if kind == "band":
        lo, hi = value_eV
        return "EXCLUDED" if lo <= m_eV <= hi else "allowed"
    return "n/a"


# Expected verdicts, recorded so that editing a number in BOUNDS without
# revisiting the report makes this instrument FAIL rather than silently
# print something new. (reduced-convention verdict, standard-convention verdict)
#
# NOTE (added after a negative test of this instrument): verdicts ALONE are not
# enough. Corrupting rogers_peiris_2021 from 2e-20 to 2e-21 -- which is exactly
# the error this report was sent to settle -- leaves every verdict unchanged,
# because both values exclude the bracket. EXPECTED_GAP_DEC below pins the
# magnitude of each bound, not just its sign, so a wrong value fails loudly.
EXPECTED_VERDICTS = {
    "rogers_peiris_2021":            ("EXCLUDED", "EXCLUDED"),
    "rogers_peiris_2021_kmax008":    ("EXCLUDED", "EXCLUDED"),
    "irsic_2017_combined":           ("EXCLUDED", "EXCLUDED"),
    "irsic_2017_reference":          ("EXCLUDED", "EXCLUDED"),
    "irsic_2017_xq100_planck":       ("EXCLUDED", "EXCLUDED"),
    "armengaud_2017_sdss":           ("EXCLUDED", "EXCLUDED"),
    "armengaud_2017_highres":        ("EXCLUDED", "EXCLUDED"),
    "armengaud_2017_planck":         ("EXCLUDED", "EXCLUDED"),
    "dalal_kravtsov_2022":           ("EXCLUDED", "EXCLUDED"),
    "dalal_kravtsov_2022_other_ufds": ("EXCLUDED", "EXCLUDED"),
    "gonzalez_morales_2017":         ("allowed",  "EXCLUDED"),
    "marsh_pop_2015":                ("allowed",  "allowed"),
    "gonzalez_morales_2017_fornax":  ("allowed",  "EXCLUDED"),
    "gonzalez_morales_2017_sculptor": ("allowed", "allowed"),
    "davoudiasl_denton_2019_scalar": ("allowed",  "allowed"),
    "davoudiasl_denton_2019_vector": ("allowed",  "allowed"),
    "stott_marsh_2018_smbh":         ("allowed",  "allowed"),
    "stott_marsh_2018_stellar":      ("allowed",  "allowed"),
}

# Decade gap between each bound and the REDUCED-convention required mass,
# recorded to 2 dp as printed this run. Signed: positive means the bound sits
# above the required mass. Pins each bound's magnitude.
EXPECTED_GAP_DEC = {
    "rogers_peiris_2021":             3.32,
    "rogers_peiris_2021_kmax008":     2.38,
    "irsic_2017_combined":            2.32,
    "irsic_2017_reference":           2.59,
    "irsic_2017_xq100_planck":        1.45,
    "armengaud_2017_sdss":            2.38,
    "armengaud_2017_highres":         2.48,
    "armengaud_2017_planck":          2.13,
    "dalal_kravtsov_2022":            4.50,
    "dalal_kravtsov_2022_other_ufds": 3.02,
    "gonzalez_morales_2017":         -0.62,
    "marsh_pop_2015":                -1.06,
    "gonzalez_morales_2017_fornax":  -0.70,
    "gonzalez_morales_2017_sculptor": -0.92,
    "davoudiasl_denton_2019_scalar":  2.48,
    "davoudiasl_denton_2019_vector":  1.95,
    "stott_marsh_2018_smbh":          3.86,
    "stott_marsh_2018_stellar":       9.86,
}


def section2_bounds_table():
    print("=" * 74)
    print("SECTION 2 -- published bounds [CITED literature, NOT measured here]")
    print("=" * 74)
    required = ("key", "probe", "kind", "value_eV", "cl", "source", "quote",
                "caveat", "provenance")
    for b in BOUNDS:
        for f in required:
            check(f"BOUNDS[{b.get('key','?')}] has field '{f}'",
                  bool(b.get(f)), "" if b.get(f) else "missing or empty")
        check(f"BOUNDS[{b['key']}] is tagged CITED",
              b.get("provenance") == "CITED", str(b.get("provenance")))
    keys = [b["key"] for b in BOUNDS]
    check("BOUNDS keys are unique", len(keys) == len(set(keys)))

    by_probe = {}
    for b in BOUNDS:
        by_probe.setdefault(b["probe"], []).append(b)
    for probe in ("lyman-alpha", "dwarf-heating", "dwarf-core", "superradiance"):
        print(f"\n  -- {probe} --")
        for b in by_probe.get(probe, []):
            if b["kind"] == "band":
                lo, hi = b["value_eV"]
                val = f"{lo:.3e} .. {hi:.3e} eV excluded"
            else:
                arrow = ">" if b["kind"] == "lower" else "<"
                val = f"m {arrow} {b['value_eV']:.3e} eV"
                if b["kind"] == "pref":
                    val = f"m ~ {b['value_eV']:.3e} eV (preference, not a limit)"
            print(f"     {b['key']:32s} {val:40s} [{b['cl']}]")
    print()


def section3_verdicts():
    print("=" * 74)
    print("SECTION 3 -- the Section 1 bracket placed against every bound")
    print("=" * 74)
    m_red = globals()["M_REQ_REDUCED_EV"]
    m_std = globals()["M_REQ_STANDARD_EV"]
    print(f"  bracket: reduced  m = {m_red:.4e} eV   (audit's stated 9.6e-24)")
    print(f"           standard m = {m_std:.4e} eV   (x 2*pi)")
    print()
    print(f"  {'bound':34s} {'reduced':>10s} {'standard':>10s}   gap(dec) red/std")
    n_excl_both = 0
    for b in BOUNDS:
        if b["kind"] == "pref":
            continue
        vr = verdict(b["kind"], b["value_eV"], m_red)
        vs = verdict(b["kind"], b["value_eV"], m_std)
        exp = EXPECTED_VERDICTS.get(b["key"])
        check(f"verdict matches recorded expectation for {b['key']}",
              exp == (vr, vs), f"computed {(vr, vs)}, recorded {exp}")
        if b["kind"] == "lower":
            gr = math.log10(b["value_eV"] / m_red)
            gs = math.log10(b["value_eV"] / m_std)
            gap = f"{gr:6.2f} {gs:6.2f}"
        elif b["kind"] == "upper":
            gr = math.log10(m_red / b["value_eV"])
            gs = math.log10(m_std / b["value_eV"])
            gap = f"{gr:6.2f} {gs:6.2f}"
        else:
            lo, _ = b["value_eV"]
            gr = math.log10(lo / m_red)
            gs = math.log10(lo / m_std)
            gap = f"{gr:6.2f} {gs:6.2f}"
        print(f"  {b['key']:34s} {vr:>10s} {vs:>10s}   {gap}")
        exp_gap = EXPECTED_GAP_DEC.get(b["key"])
        check(f"decade gap matches recorded value for {b['key']}",
              exp_gap is not None and abs(gr - exp_gap) <= 0.01,
              f"computed {gr:.4f}, recorded {exp_gap}")
        if (vr, vs) == ("EXCLUDED", "EXCLUDED"):
            n_excl_both += 1

    print()
    # The headline arithmetic, recomputed rather than quoted.
    rp = [b for b in BOUNDS if b["key"] == "rogers_peiris_2021"][0]["value_eV"]
    weakest_lya = min(b["value_eV"] for b in BOUNDS
                      if b["probe"] == "lyman-alpha" and b["kind"] == "lower")
    dk = [b for b in BOUNDS if b["key"] == "dalal_kravtsov_2022"][0]["value_eV"]
    gm = [b for b in BOUNDS if b["key"] == "gonzalez_morales_2017"][0]["value_eV"]
    print(f"  strongest Lyman-alpha  ({rp:.1e} eV): reduced {math.log10(rp/m_red):.2f} dec, "
          f"standard {math.log10(rp/m_std):.2f} dec below")
    print(f"  weakest   Lyman-alpha  ({weakest_lya:.1e} eV): reduced "
          f"{math.log10(weakest_lya/m_red):.2f} dec, standard "
          f"{math.log10(weakest_lya/m_std):.2f} dec below")
    print(f"  UFD heating            ({dk:.1e} eV): reduced {math.log10(dk/m_red):.2f} dec, "
          f"standard {math.log10(dk/m_std):.2f} dec below")
    print(f"  dSph core upper limit  ({gm:.1e} eV): reduced ratio "
          f"{m_red/gm:.3f} (allowed), standard ratio {m_std/gm:.3f} (excluded)")

    # Rogers & Peiris state the SAME limit twice, as log(m_a) > -19.64 and as
    # m_a > 2e-20 eV. Check the stored value against the paper's own log form.
    rp_log = 10 ** -19.64
    print(f"  Rogers & Peiris internal consistency: 10^-19.64 = {rp_log:.4e} eV "
          f"vs stored {rp:.3e} eV  (ratio {rp_log/rp:.4f})")
    check("stored Rogers & Peiris value reproduces the paper's own log form",
          abs(math.log10(rp_log / rp)) < 0.10,
          f"10^-19.64={rp_log:.4e} vs stored={rp:.3e}")

    check("weakest Lyman-alpha limit still excludes BOTH ends of the bracket",
          weakest_lya > m_std, f"weakest={weakest_lya:.3e}, m_std={m_std:.3e}")
    check("the reduced-convention mass is ALLOWED by the dSph-core upper limit",
          m_red < gm, f"m_red={m_red:.4e}, gm={gm:.3e}")
    check("the standard-convention mass is EXCLUDED by the dSph-core upper limit",
          m_std > gm, f"m_std={m_std:.4e}, gm={gm:.3e}")
    _all_lower_exclude = all(verdict("lower", b["value_eV"], m_std) == "EXCLUDED"
                             for b in BOUNDS if b["kind"] == "lower")
    check("every Lyman-alpha and dwarf-heating lower limit excludes both ends",
          _all_lower_exclude,
          "" if _all_lower_exclude
          else "some lower limit does not exclude the standard-convention mass")
    check("no superradiance band contains either end of the bracket",
          all(verdict("band", b["value_eV"], m) == "allowed"
              for b in BOUNDS if b["kind"] == "band" for m in (m_red, m_std)))
    print(f"  bounds excluding BOTH ends: {n_excl_both}")
    check("at least 10 published limits exclude both ends of the bracket",
          n_excl_both >= 10, f"n={n_excl_both}")

    # Cross-check of the 2*pi convention against an external primary source.
    # Dalal & Kravtsov 2022 state: m = 1e-22 eV, v = 200 km/s -> lambda ~ 600 pc.
    m_dk = eV_to_kg(1e-22)
    lam_std_pc = H_PLANCK / (m_dk * 200e3) / KPC * 1000.0
    lam_red_pc = HBAR / (m_dk * 200e3) / KPC * 1000.0
    print()
    print(f"  cross-check vs Dalal & Kravtsov 2022's stated 'lambda ~ 600 pc':")
    print(f"      standard h/(mv) = {lam_std_pc:.1f} pc ; reduced hbar/(mv) = "
          f"{lam_red_pc:.1f} pc")
    check("D&K's quoted 600 pc is the STANDARD convention",
          abs(lam_std_pc - 600.0) / 600.0 < 0.05, f"{lam_std_pc:.1f} pc")
    check("D&K's quoted 600 pc is NOT the reduced convention",
          abs(lam_red_pc - 600.0) / 600.0 > 0.5, f"{lam_red_pc:.1f} pc")
    print()


def section4_superradiance_reach():
    print("=" * 74)
    print("SECTION 4 -- superradiance reach: which BH mass probes which boson mass")
    print("=" * 74)
    # alpha = G M mu / (hbar c^3);  mu(alpha=1, M=Msun) = hbar c^3 / (G Msun)
    K_EV = HBAR * C_LIGHT ** 3 / (G_NEWTON * M_SUN) / E_CHARGE
    print(f"  hbar c^3 / (G Msun) = {K_EV:.5e} eV     [T1 this run]")
    check("superradiance scale constant is ~1.34e-10 eV",
          abs(K_EV - 1.336e-10) / 1.336e-10 < 0.01, f"{K_EV:.5e}")

    # Calibrate the efficient-superradiance alpha window from M87* itself,
    # using Davoudiasl & Denton's CITED scalar band edges as inputs.
    M87_MSUN = 6.5e9
    dd = [b for b in BOUNDS if b["key"] == "davoudiasl_denton_2019_scalar"][0]
    lo_eV, hi_eV = dd["value_eV"]
    a_lo = lo_eV * M87_MSUN / K_EV
    a_hi = hi_eV * M87_MSUN / K_EV
    print(f"  M87* (M = {M87_MSUN:.1e} Msun) scalar band -> alpha in "
          f"[{a_lo:.3f}, {a_hi:.3f}]   [T1 this run, D&D numbers as input]")
    check("calibrated alpha window is physical (0 < alpha < 1)",
          0.0 < a_lo < a_hi < 1.0, f"[{a_lo:.3f},{a_hi:.3f}]")

    m_red = globals()["M_REQ_REDUCED_EV"]
    m_std = globals()["M_REQ_STANDARD_EV"]
    LARGEST_KNOWN_SMBH_MSUN = 6.6e10   # CITED order of magnitude (TON 618 class)
    print()
    print("  BH mass that would be needed to place the bracket inside a band:")
    worst = float("inf")
    for label, m in (("standard conv. 6.02e-23 eV", m_std),
                     ("CPF stated    1.00e-23 eV", 1.0e-23),
                     ("reduced conv.  9.59e-24 eV", m_red)):
        M_lo = a_lo * K_EV / m
        M_hi = a_hi * K_EV / m
        worst = min(worst, M_lo)   # weakest case: the smallest BH mass that would suffice
        print(f"      {label:28s}  M_BH = {M_lo:.3e} .. {M_hi:.3e} Msun"
              f"   ({M_lo/LARGEST_KNOWN_SMBH_MSUN:.0f}x the heaviest known)")
    check("every required BH mass exceeds the heaviest known SMBH",
          worst > LARGEST_KNOWN_SMBH_MSUN,
          f"min required {worst:.3e} vs largest known {LARGEST_KNOWN_SMBH_MSUN:.1e}")
    reach = a_lo * K_EV / LARGEST_KNOWN_SMBH_MSUN
    print(f"  lightest boson reachable with the heaviest known SMBH "
          f"({LARGEST_KNOWN_SMBH_MSUN:.1e} Msun): {reach:.3e} eV")
    check("superradiance cannot reach the top of the CPF bracket",
          reach > m_std, f"reach={reach:.3e}, m_std={m_std:.3e}")
    print()


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

    section2_bounds_table()
    section3_verdicts()
    section4_superradiance_reach()

    if FAILURES:
        print("INTERNAL INCONSISTENCIES:")
        for f in FAILURES:
            print("  - " + f)
        sys.exit(1)
    print("All sections internally consistent.")


if __name__ == "__main__":
    main()
