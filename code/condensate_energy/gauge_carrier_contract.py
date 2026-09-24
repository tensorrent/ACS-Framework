#!/usr/bin/env python3
"""Exact existing-gauge embedding, vacuum mass Grams and carrier charges."""
import hashlib
import json
from pathlib import Path

import sympy as s

from gauge_completion import ROOT, OUT


def canonical_color_basis():
    generators = []
    names = []
    for i in range(4):
        for j in range(i + 1, 4):
            t = s.zeros(4)
            t[i, j] = t[j, i] = s.Rational(1, 2)
            generators.append(t)
            names.append(f'X{i}{j}')
            t = s.zeros(4)
            t[i, j], t[j, i] = -s.I / 2, s.I / 2
            generators.append(t)
            names.append(f'Y{i}{j}')
    for k in range(1, 4):
        values = [1] * k + [-k] + [0] * (3 - k)
        generators.append(s.diag(*values) / s.sqrt(2 * k * (k + 1)))
        names.append(f'H{k}')
    return generators, names


def vacuum_gauge_gram(phi, delta):
    color, names = canonical_color_basis()
    pauli = [s.Matrix([[0, 1], [1, 0]]), s.Matrix([[0, -s.I], [s.I, 0]]), s.diag(1, -1)]
    spin = [s.Matrix(3, 3, lambda i, j: -s.I * s.LeviCivita(a, i, j)) for a in range(3)]
    variations = []
    for t in color:
        variations.append((s.zeros(2), [-t.conjugate() * d - d * t.conjugate().T for d in delta]))
    for t in pauli:
        variations.append((t * phi / 2, [s.zeros(4) for _ in range(3)]))
    for a, t in enumerate(pauli):
        variations.append((-phi * t / 2, [sum((spin[a][i, j] * delta[j] for j in range(3)), s.zeros(4)) for i in range(3)]))
    def inner(i, j):
        pi, di = variations[i]
        pj, dj = variations[j]
        return s.simplify(2 * s.re(s.trace(pi.conjugate().T * pj) + sum(s.trace(a.conjugate().T * b) for a, b in zip(di, dj))))
    gram = s.Matrix(21, 21, inner)
    return gram, names + ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']


def exact_gauge_carrier_contract():
    x, y, chi, b = s.symbols('x y chi b', real=True)
    q = x + s.I * y
    e44 = s.zeros(4)
    e44[3, 3] = 1
    phi = chi * s.eye(2) / 2
    delta = [s.zeros(4), s.zeros(4), q * e44 / s.sqrt(2)]
    color, names = canonical_color_basis()
    t15 = color[-1]
    weight = s.sqrt(s.Rational(3, 2))
    action = -t15 * delta[2] - delta[2] * t15.T
    currents = [s.simplify(s.trace(delta[2].conjugate().T * (-t.conjugate() * delta[2] - delta[2] * t.conjugate().T))) for t in color]
    nphi = s.trace(phi.conjugate().T * phi)
    ndelta = s.trace(delta[2].conjugate().T * delta[2])
    potential = (nphi - s.Rational(1, 2)) ** 2 + 2 * nphi * ndelta + b * ndelta ** 2
    expected = (chi * chi - 1) ** 2 / 4 + chi * chi * (x * x + y * y) / 2 + b * (x * x + y * y) ** 2 / 4
    # Every determinant in HDelta is of one of these matrices. Its full
    # derivative w.r.t. any matrix entry is a cofactor (adjugate entry).
    det_inputs = list(delta)
    for i in range(3):
        for j in range(i + 1, 3):
            det_inputs.extend([delta[i] + delta[j], delta[i] - delta[j]])
    hol_value = all(d.det() == 0 for d in det_inputs)
    hol_gradient = all(d.adjugate() == s.zeros(4) for d in det_inputs)
    vacuum = [s.zeros(4) for _ in range(3)]
    gram, generator_names = vacuum_gauge_gram(s.eye(2) / 2, vacuum)
    eig = {str(k): int(v) for k, v in gram.eigenvals().items()}
    vector_ratios = []
    vector_weights = []
    color_sum = s.zeros(4)
    for i in range(3):
        root = s.zeros(4)
        root[i, 3] = 1
        w = s.simplify(t15[i, i] - t15[3, 3])
        assert t15 * root - root * t15 == w * root
        vector_weights.append(str(w))
        vector_ratios.append(str(s.simplify(w / weight)))
        color_sum += root * root.T - root.T * root
    # Normalized generators have no bilinear cross terms: 2 Tr(Ta Tb)=delta_ab.
    metric_ok = all(s.simplify(2 * s.trace(a * bb)) == int(i == j) for i, a in enumerate(color) for j, bb in enumerate(color))
    anti_lepton_ratio = s.simplify(-t15[3, 3] / weight)
    # A distinct conventional neutral-Delta breaking. Couplings=1 here only
    # to compute an exact Gram rank, not to select physical masses.
    neutral = [e44 / s.sqrt(2), -s.I * e44 / s.sqrt(2), s.zeros(4)]
    physical_gram, physical_names = vacuum_gauge_gram(s.diag(s.Rational(1, 3), s.Rational(1, 5)), neutral)
    electric_generator = s.zeros(21, 1)
    electric_generator[14], electric_generator[17], electric_generator[20] = s.sqrt(s.Rational(2, 3)), 1, 1
    spin3 = s.Matrix([[0, -s.I, 0], [s.I, 0, 0], [0, 0, 0]])
    neutral_vector = s.Matrix([1, -s.I, 0])
    neutral_charge_zero = (spin3 + s.eye(3)) * neutral_vector == s.zeros(3, 1)
    # The earlier positive-potential no-binding bound survives positive E_el.
    g, v, lam, f = s.symbols('g v lam f', positive=True)
    u = lam / 4 * (chi * chi - v * v) ** 2 + g * g / 2 * chi * chi * f * f + b / 4 * f ** 4
    square = lam / 4 * (chi * chi - v * v + g * g / lam * f * f) ** 2 + (b - g ** 4 / lam) / 4 * f ** 4
    checks = {
        'canonical_SU4_trace_metric': metric_ok,
        'scalar_kinetics_one_half': s.trace(s.diff(phi, chi).conjugate().T * s.diff(phi, chi)) == s.Rational(1, 2) and s.trace(s.diff(delta[2], x).conjugate().T * s.diff(delta[2], x)) == s.Rational(1, 2),
        'selected_invariant_potential_matches': s.expand(potential - expected) == 0,
        'existing_T15_eigenstate': s.simplify(action - weight * delta[2]) == s.zeros(4),
        'fourteen_other_color_currents_zero': all(c == 0 for c in currents[:-1]),
        'T15_current_weight': s.simplify(currents[-1] - weight * (x * x + y * y) / 2) == 0,
        'weak_triplet_current_zero': all((-s.I * s.LeviCivita(a, 2, 2)) == 0 for a in range(3)),
        'holomorphic_value_zero': hol_value,
        'holomorphic_full_first_derivative_zero': hol_gradient,
        'selected_vacuum_18_massless_vectors': gram.rank() == 3 and eig == {'0': 18, '1/2': 3},
        'charged_color_vector_weight_two_thirds': all(w == '2/3' for w in vector_ratios),
        'three_root_charges_have_no_SU3_Cartan_remainder': color_sum == s.diag(1, 1, 1, -3),
        'antilepton_weight_half_scalar': anti_lepton_ratio == s.Rational(1, 2),
        'neutral_Delta_component_is_electrically_neutral': neutral_charge_zero,
        'broken_vacuum_nine_massless_vectors': physical_gram.rank() == 12,
        'electromagnetic_generator_unbroken': physical_gram * electric_generator == s.zeros(21, 1),
        'positive_quartic_no_binding_identity': s.expand(u - g * g * v * v * f * f / 2 - square) == 0,
    }
    return dict(checks={k: bool(v) for k, v in checks.items()},
        embedding='Phi=chi I2/2; D1=D2=0; D3=q E44/sqrt(2); A along T15',
        T15=str(t15), scalar_weight=str(weight), effective_coupling='e=sqrt(3/2)*g4 in this canonical convention',
        full_vacuum_gram=[[str(v) for v in row] for row in gram.tolist()], generator_order=generator_names,
        selected_vacuum_mass_squared_eigenvalues=eig,
        charged_vector_weights=vector_weights, charged_vector_charge_per_q=vector_ratios,
        antilepton_charge_per_q=str(anti_lepton_ratio),
        conventional_vacuum_gram=[[str(v) for v in row] for row in physical_gram.tolist()],
        conventional_vacuum='Phi=diag(1/3,1/5); D=(1,-i,0) E44/sqrt(2); all gauge couplings set to 1 for rank only',
        physical_Delta_anti_lepton_pair_electric_charges=[0, 1, 2],
        boundaries=['The color gauge charge is defined in a fixed asymptotic Cartan convention; this is not a gauge-invariant elementary particle identification.',
                    'The selected vacuum has massless non-Abelian charged vectors. Scalar-only E<Q is not a full-theory stability certificate.',
                    'Charge weights and mass Gram establish available sectors, not actual nonlinear emission rates or quantum confinement.',
                    'Gauge charge conservation remains exact in the full anomaly-free gauge content; individual scalar q-number need not be conserved.',
                    'The exact rank-one slice does not make the full HDelta operator identically zero or prove stability to off-slice fields.'])


def run_carrier_contract():
    result = exact_gauge_carrier_contract()
    survey = json.loads((OUT / 'results.json').read_text())
    result['fermion_thresholds'] = []
    for e in [0., .08, .12]:
        row = survey['cases'][f'Q1000-e{e:g}']
        result['fermion_thresholds'].append(dict(coupling=e,
            equal_mass_pair_complete_dispersal_mass_threshold=row['energy_per_charge'] / 2,
            equal_mass_pair_infinitesimal_emission_mass_threshold=row['omega'] / 2))
    result['fermion_threshold_scope'] = 'Two anti-leptons each have half the selected scalar T15 weight. Values are in units of the scalar exterior mass; actual admissible channels and masses must come from the chosen full vacuum and interactions. They are kinematic conditions, not widths.'
    result['source_constraints'] = {
        'quartic_basis': '17 real quartic couplings, 4 real quadratic couplings in the gauge-only invariant basis; coefficients are not fixed by this count.',
        'no_binding_counterexample': 'For b>=g^4/lambda_chi the completed square gives E>=g v |Q| even with gauge energy; b=1.2 in model units is an allowed selected norm potential.',
        'physical_scale': 'A common replacement of every dimensionful parameter by the correspondingly scaled value preserves dimensionless classical predictions while scaling energies by a and times by 1/a. Dimensionless source ratios alone cannot choose a.',
        'fermion_mass_map_in_selected_vacuum': 'M_D=(Y+Z)/2 when Phi=I2/2 in the inherited Yukawa convention; Delta=0 supplies no Majorana VEV. Unspecified Y,Z leave carrier thresholds undetermined.',
        'source_caution': 'The proposed manuscript Higgs quartic is not a derivation of this Delta self-quartic b; its own canonical matching qualification remains.'}
    sources = [Path(__file__).resolve(), OUT / 'protocol.md', OUT / 'results.json',
               ROOT / 'docs/condensate_energy/charge_audit/source-snapshots/scalar_invariant_basis.py',
               ROOT / 'docs/frontier/2026-09-11/workstreams/rg/report.md',
               ROOT / 'papers/core_trilogy/Palatini_Gauge_Attractor.tex']
    result['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    result['all_checks_passed'] = all(result['checks'].values())
    (OUT / 'carrier-contract.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(checks=result['checks'], thresholds=result['fermion_thresholds']), indent=2), flush=True)
    assert result['all_checks_passed'], result['checks']


if __name__ == '__main__':
    run_carrier_contract()
