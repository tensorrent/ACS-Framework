#!/usr/bin/env python3
"""Carrier thresholds remain free even on the proposed 2/3 Yukawa ratio."""
import hashlib
import json
from pathlib import Path

import sympy as s

from gauge_completion import ROOT, OUT


def compare_allowed_carriers():
    data = json.loads((OUT / 'results.json').read_text())
    row = data['cases']['Q1000-e0.08']
    scalar_weight = s.sqrt(s.Rational(3, 2))
    t15 = s.diag(1, 1, 1, -3) / (2 * s.sqrt(6))
    fundamental = [t15[i, i] for i in range(4)]
    # Weyl description: two 4s from left doublets; two anti-4s from
    # charge-conjugated right doublets per family. Mixed weak traces vanish.
    checks = dict(gauged_T15_cubic_anomaly_cancels=s.simplify(2 * sum(t ** 3 for t in fundamental) + 2 * sum((-t) ** 3 for t in fundamental)) == 0,
                  mixed_weak_trace_zero=sum(fundamental) == 0,
                  weak_Witten_doublet_count_even=(3 * 4) % 2 == 0,
                  two_antilepton_weights_equal_Delta=s.simplify(-2 * t15[3, 3] - scalar_weight) == 0)
    cases = []
    for label, y in [('light-carrier', s.Rational(1, 10)), ('heavy-carrier', s.Integer(1))]:
        Y = y * s.eye(3)
        Z = s.Rational(2, 3) * Y
        mass = (Y + Z) / 2
        m = mass[0, 0]
        pair = 2 * m
        cases.append(dict(label=label, Y_eigenvalue=str(y), Z_over_Y='2/3',
                          fermion_mass=str(m), pair_threshold=str(pair),
                          infinitesimal_pair_emission_kinematically_open=bool(float(pair) < row['omega']),
                          complete_dispersal_to_free_pairs_energetically_open=bool(float(pair) < row['energy_per_charge'])))
        checks[f'{label}_mass_map'] = mass == s.Rational(5, 6) * Y
    checks['same_Yukawa_ratio_allows_opposite_threshold_outcomes'] = cases[0]['infinitesimal_pair_emission_kinematically_open'] and not cases[1]['infinitesimal_pair_emission_kinematically_open']
    checks['same_Yukawa_ratio_allows_opposite_total_energy_outcomes'] = cases[0]['complete_dispersal_to_free_pairs_energetically_open'] and not cases[1]['complete_dispersal_to_free_pairs_energetically_open']
    result = dict(checks=checks, cases=cases, reference=dict(charge=1000, coupling=.08, omega=row['omega'], energy_per_charge=row['energy_per_charge']),
        assumptions=['Canonical selected vacuum Phi=I2/2, Delta=0, with source-convention Dirac mass (Y+Z)/2.',
                     'A nonzero Majorana-type interaction F Delta R R permits the appropriate antilepton pair; F is an additional selected nonzero coefficient.',
                     'The m_R=0 Delta component couples the two weak components of the lepton pair; both have equal Dirac mass in this chosen equal-VEV vacuum.',
                     'These are tree-level kinematic comparisons. Fermion occupation, Pauli blocking, transition matrix elements, loop corrections, and actual rates are not calculated.',
                     'Neither absolute Y value is asserted to be the physical ACS choice. The comparison proves that the 2/3 ratio plus gauge content cannot alone select the threshold.'],
        conclusion='Existing gauge charge avoids the global-X anomaly obstruction but does not assign carrier masses or protect scalar q-number.')
    paths = [Path(__file__).resolve(), OUT / 'results.json', OUT / 'carrier-contract.json',
             ROOT / 'docs/frontier/2026-09-11/workstreams/rg/report.md']
    result['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    result['all_checks_passed'] = all(checks.values())
    (OUT / 'carrier-countermodels.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    assert result['all_checks_passed']


if __name__ == '__main__':
    compare_allowed_carriers()
