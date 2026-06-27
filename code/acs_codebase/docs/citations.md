# Citations and External References

The ACS trilogy rests on standard mathematical and physical results
from the literature. This document records the key citations to be
included in each paper.

---

## Paper A — Pati-Salam phenomenology

### Pati-Salam model
- J. C. Pati and A. Salam, "Lepton Number as the Fourth Color,"
  Phys. Rev. D 10 (1974) 275.

### Standard Model parameter count
- Particle Data Group, *Review of Particle Physics*, latest edition.
  19+ free parameters in the SM, used as the comparison baseline.

### PMNS data and θ₁₃
- T2K Collaboration, "Observation of electron neutrino appearance,"
  Phys. Rev. Lett. 112 (2014) 061802.
- NOvA, T2K, JUNO recent measurements; values used in
  `src/paper_a/theta13_obstruction.py` reflect 2024 PDG averages.

### Proton decay bounds
- Super-Kamiokande Collaboration, recent τ_p > 10³⁴ years bounds
  imply v_R > 10¹⁵ GeV in Pati-Salam-like settings.

### TBM, TM1, TM2 ansaetze
- P. F. Harrison, D. H. Perkins, W. G. Scott, "Tri-bimaximal mixing
  and the neutrino oscillation data," Phys. Lett. B 530 (2002) 167.
- C. H. Albright, W. Rodejohann, "Comparing trimaximal mixing and
  its variants with deviations from tri-bimaximal mixing,"
  Eur. Phys. J. C 62 (2009) 599.

### Yukawa hierarchy and FeynRules
- A. Alloul et al., "FeynRules 2.0 — A complete toolbox for tree-level
  phenomenology," Comput. Phys. Commun. 185 (2014) 2250.

---

## Paper B — Spectral / resolvent framework

### Riemann hypothesis and the explicit formula
- B. Riemann, "Über die Anzahl der Primzahlen unter einer gegebenen
  Grösse," Monatsber. Berliner Akad. (1859).

### Boundedness of the prime-counting error under RH (CRITICAL CITATION)
- **H. von Koch, "Sur la distribution des nombres premiers,"
  Acta Mathematica 24 (1901) 159–182.**

  This is the source of the bound ψ(x) − x = O(√x log²x) under RH,
  which Paper B reframes in logarithmic coordinates as the
  renormalized stability statement. The framing is new; the
  underlying inequality is von Koch's.

### Hilbert-Pólya conjecture
- D. Hilbert and G. Pólya, independent suggestions ca. 1914.
  No published primary source; the conjecture is cited as folklore
  attributed to both. See:
  - A. Odlyzko, "Primes, quantum chaos, and computers,"
    in *Number Theory: Proceedings* (1990).

### Berry-Keating Hamiltonian H ~ xp
- M. V. Berry and J. P. Keating, "H = xp and the Riemann zeros,"
  in *Supersymmetry and Trace Formulae*, eds. I. V. Lerner et al.,
  NATO ASI Series Vol. 370 (Plenum, 1999), 355–367.

### Riemann-von Mangoldt counting
- E. C. Titchmarsh, *The Theory of the Riemann Zeta-Function*,
  2nd ed., revised by D. R. Heath-Brown (Oxford University Press, 1986).

### Riemann zero data
- A. M. Odlyzko, "Tables of zeros of the Riemann zeta function."
  http://www.dtc.umn.edu/~odlyzko/zeta_tables/
  First 50 zeros used in `src/paper_b/explicit_formula_resolvent.py`.

### Connes' spectral approach (alternative to Hilbert-Pólya)
- A. Connes, "Trace formula in noncommutative geometry and the zeros
  of the Riemann zeta function," Selecta Math. 5 (1999) 29.

---

## Paper C — Algebraic-closure framework

### c-theorem (2D)
- A. B. Zamolodchikov, "Irreversibility of the flux of the
  renormalization group in a 2D field theory," JETP Lett. 43 (1986) 730.

### a-theorem (4D)
- Z. Komargodski and A. Schwimmer, "On renormalization group flows
  in four dimensions," JHEP 12 (2011) 099.

### Jordan-Chevalley decomposition (spectral taxonomy basis)
- C. Chevalley, *Théorie des groupes de Lie*, Tome III (Hermann, 1955).
- N. Jacobson, *Lie Algebras* (Dover, 1979), Chapter III.

### Killing form and skew-symmetry of ad
- N. Bourbaki, *Lie Groups and Lie Algebras*, Chapters 1-3.
  Standard result that ad_X is skew-symmetric w.r.t. the Killing form.

### ER=EPR conjecture (for comparison purposes)
- J. Maldacena and L. Susskind, "Cool horizons for entangled black holes,"
  Fortsch. Phys. 61 (2013) 781.

### Ryu-Takayanagi formula
- S. Ryu and T. Takayanagi, "Holographic derivation of entanglement
  entropy from AdS/CFT," Phys. Rev. Lett. 96 (2006) 181602.

### AdS/CFT
- J. Maldacena, "The large N limit of superconformal field theories
  and supergravity," Adv. Theor. Math. Phys. 2 (1998) 231.

### Van Raamsdonk: spacetime from entanglement
- M. Van Raamsdonk, "Building up spacetime with quantum entanglement,"
  Gen. Rel. Grav. 42 (2010) 2323.

### Frenet-Serret formulas
- Standard differential geometry; see e.g., M. P. do Carmo,
  *Differential Geometry of Curves and Surfaces* (Prentice-Hall, 1976).

### AGC / core rope memory (architectural correspondence)
- E. C. Hall, *Journey to the Moon: The History of the Apollo
  Guidance Computer* (AIAA, 1996).

---

## Methodological references

### Adversarial compression / proofs and refutations
- I. Lakatos, *Proofs and Refutations* (Cambridge University Press, 1976).
  Standard reference for the conjecture-test-refine cycle that
  this codebase's verification methodology follows.

### Falsifiability
- K. Popper, *The Logic of Scientific Discovery* (Hutchinson, 1959).

---

## Software dependencies

- NumPy: T. E. Oliphant et al., "Array programming with NumPy,"
  Nature 585 (2020) 357.
- SciPy: P. Virtanen et al., "SciPy 1.0," Nat. Methods 17 (2020) 261.
- SymPy: A. Meurer et al., "SymPy: symbolic computing in Python,"
  PeerJ Computer Science 3 (2017) e103.
- Pytest: H. Krekel et al., pytest documentation, https://docs.pytest.org

---

## BibTeX template

For convenience, BibTeX entries for the most-cited references:

```bibtex
@article{vonKoch1901,
  author  = {von Koch, Helge},
  title   = {Sur la distribution des nombres premiers},
  journal = {Acta Mathematica},
  volume  = {24},
  pages   = {159--182},
  year    = {1901}
}

@article{Zamolodchikov1986,
  author  = {Zamolodchikov, A. B.},
  title   = {Irreversibility of the flux of the renormalization group
             in a 2D field theory},
  journal = {JETP Letters},
  volume  = {43},
  pages   = {730},
  year    = {1986}
}

@article{KomargodskiSchwimmer2011,
  author  = {Komargodski, Zohar and Schwimmer, Adam},
  title   = {On renormalization group flows in four dimensions},
  journal = {JHEP},
  volume  = {12},
  pages   = {099},
  year    = {2011}
}

@article{PatiSalam1974,
  author  = {Pati, J. C. and Salam, A.},
  title   = {Lepton number as the fourth color},
  journal = {Phys. Rev. D},
  volume  = {10},
  pages   = {275},
  year    = {1974}
}

@inproceedings{BerryKeating1999,
  author    = {Berry, M. V. and Keating, J. P.},
  title     = {H = xp and the Riemann zeros},
  booktitle = {Supersymmetry and Trace Formulae},
  editor    = {Lerner, I. V. and others},
  series    = {NATO ASI Series},
  volume    = {370},
  publisher = {Plenum Press},
  pages     = {355--367},
  year      = {1999}
}

@article{MaldacenaSusskind2013,
  author  = {Maldacena, Juan and Susskind, Leonard},
  title   = {Cool horizons for entangled black holes},
  journal = {Fortsch. Phys.},
  volume  = {61},
  pages   = {781},
  year    = {2013}
}

@article{RyuTakayanagi2006,
  author  = {Ryu, Shinsei and Takayanagi, Tadashi},
  title   = {Holographic derivation of entanglement entropy from AdS/CFT},
  journal = {Phys. Rev. Lett.},
  volume  = {96},
  pages   = {181602},
  year    = {2006}
}

@book{Lakatos1976,
  author    = {Lakatos, Imre},
  title     = {Proofs and Refutations},
  publisher = {Cambridge University Press},
  year      = {1976}
}
```
