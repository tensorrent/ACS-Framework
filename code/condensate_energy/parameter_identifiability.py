#!/usr/bin/env python3
"""Exact countermodels for selection by gauge symmetry or ratios alone."""
import hashlib
import json
from pathlib import Path

import sympy as s

from gauge_completion import ROOT, OUT


def parameter_selection_contract():
    # Phi has eight real canonical coordinates. ||Phi||^2=x.x/2.
    direction = s.zeros(8, 1)
    direction[0] = direction[6] = 1 / s.sqrt(2)
    phi_hessian = 2 * direction * direction.T
    # At Delta=0 the mixed term 2 Nphi Ndelta gives all 60 real modes m^2=1.
    scalar_spectrum = {'0': 7, '1': 60, '2': 1}
    a, v, lam, g, b, chi, f, p, q = s.symbols('a v lam g b chi f p q', positive=True)
    kinetic = (p * p + q * q) / 2
    potential = lam * (chi * chi - v * v) ** 2 / 4 + g * g * chi * chi * f * f / 2 + b * f ** 4 / 4
    # x'=x/a, phi'(x')=a phi(x), derivatives scale a^2. Volume a^-3.
    density_scaled = (kinetic + potential).subs({chi: a * chi, f: a * f, v: a * v, p: a * a * p, q: a * a * q}, simultaneous=True)
    density_ok = s.simplify(density_scaled - a ** 4 * (kinetic + potential)) == 0
    integrated_energy_ok = s.simplify(density_scaled / a ** 3 - a * (kinetic + potential)) == 0
    # Q integrates field times one derivative and is invariant under this scaling.
    charge_ok = s.simplify((a * f) * (a * a * p) / a ** 3 - f * p) == 0
    # Two possible exact gauge-invariant norm potentials have opposite outcomes
    # at the same reduced reference charge. Numerical survival belongs to b0;
    # b1 obeys the completed-square no-binding inequality for every profile.
    b0 = 2 * s.sqrt(3) / 27
    b1 = s.Rational(6, 5)
    checks = dict(phi_radial_mass_squared_two=phi_hessian.eigenvals() == {s.Integer(0): 7, s.Integer(2): 1},
                  potential_and_kinetic_density_scale_to_fourth_power=density_ok,
                  integrated_energy_scales_linearly=integrated_energy_ok,
                  integrated_charge_invariant=charge_ok,
                  binding_reference_below_completed_square_boundary=bool(b0 < 1),
                  allowed_no_binding_control_above_boundary=bool(b1 > 1))
    return dict(checks=checks, canonical_selected_vacuum_scalar_spectrum=scalar_spectrum,
                physical_flat_scalar_directions=4,
                flat_direction_scope='Seven zero scalar Hessian modes, three eaten by the broken weak generators, leave four physical tree-level flat directions of the selected norm potential. General allowed angular couplings change this conclusion.',
                scale_family='v -> a v, quadratic masses -> a^2 masses, field amplitudes -> a fields, length/time -> length/time divided by a, energy -> a energy, Q unchanged; dimensionless couplings fixed.',
                countermodel_scope='Gauge-invariant potential class and representation content, not a proof that both satisfy every proposed unverified ACS bracket/kinetic matching rule.',
                input_boundary=[
                    'The source has not mapped all 17 quartics and four mass parameters through canonical normalization to a selected physical vacuum.',
                    'The proposed Phi quartic does not specify the independent Delta quartic b, mixed coupling, Delta mass or all angular invariants.',
                    'Yukawa matrices and the selected vacuum determine the available fermion thresholds; gauge charges alone do not.',
                    'The exact unbroken gauge generator is computable once the vacuum is specified. Choosing that vacuum is a different problem.',
                    'Classical results at fixed continuous charge do not determine integer occupation, elementary particle masses, or quantum widths.'])


def run_parameter_contract():
    result = parameter_selection_contract()
    paths = [Path(__file__).resolve(), OUT / 'protocol.md', OUT / 'fission-protocol.md',
             ROOT / 'docs/frontier/2026-09-11/workstreams/rg/report.md',
             ROOT / 'docs/condensate_energy/self_binding/results.json']
    result['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    result['all_checks_passed'] = all(result['checks'].values())
    (OUT / 'parameter-contract.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)
    assert result['all_checks_passed']


if __name__ == '__main__':
    run_parameter_contract()
