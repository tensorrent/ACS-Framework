#!/usr/bin/env python3
"""Verify provenance and render the gauge-branch evidence without hiding failures."""
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from gauge_completion import ROOT, OUT


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize_gauge_evidence():
    datasets = {}
    for name in ['results', 'finite-volume-results', 'carrier-contract', 'fission-results', 'parameter-contract', 'carrier-countermodels']:
        data = json.loads((OUT / f'{name}.json').read_text())
        for source, expected in data['source_sha256'].items():
            assert digest(ROOT / source) == expected, source
        assert data['all_checks_passed'], name
        datasets[name] = data
    prior = {}
    for name in ['self_binding', 'charge_audit', 'charge_leakage']:
        path = OUT.parent / name / 'receipt.json'
        rec = json.loads(path.read_text())
        for source, expected in rec['artifact_sha256'].items():
            assert digest(ROOT / source) == expected, source
        prior[str(path.relative_to(ROOT))] = digest(path)
    survey = datasets['results']
    cases = survey['cases']
    fig, axs = plt.subplots(2, 2, figsize=(12.4, 8.2), layout='constrained')
    colors = ['#246B8E', '#A44A3F', '#4E7662']
    for charge, color in zip([300., 1000., 3000.], colors):
        rows = sorted([r for k, r in cases.items() if r['charge'] == charge and not k.endswith(('domain', 'tolerance'))], key=lambda r: r['coupling'])
        converged = [r for r in rows if r['success']]
        for ax, metric in zip(axs[0], ['energy_per_charge', 'omega']):
            x = [r['coupling'] for r in converged]
            y = [r[metric] for r in converged]
            ax.plot(x, y, '-', color=color, lw=1.3, alpha=.7)
            good = [r for r in converged if r['localized_candidate']]
            other = [r for r in converged if not r['localized_candidate']]
            ax.scatter([r['coupling'] for r in good], [r[metric] for r in good], s=23, color=color, label=f'Q={charge:g}')
            ax.scatter([r['coupling'] for r in other], [r[metric] for r in other], s=23, facecolors='white', edgecolors=color)
    for ax in axs[0]:
        ax.axhline(1., color='.25', ls='--', lw=1)
        ax.set_xlabel('Electric coupling e (dimensionless)')
        ax.set_xlim(-.005, .255)
        ax.grid(alpha=.18)
        ax.legend(frameon=False, fontsize=9)
    axs[0, 0].set_title('A  Total energy against the free-scalar threshold', loc='left', fontsize=11)
    axs[0, 0].set_ylabel('E / Q (exterior scalar mass = 1)')
    axs[0, 0].set_ylim(.73, 1.34)
    axs[0, 1].set_title('B  Infinity frequency checks localization', loc='left', fontsize=11)
    axs[0, 1].set_ylabel('omega (exterior scalar mass = 1)')
    axs[0, 1].set_ylim(.67, 1.6)
    for e, color in zip([0., .08, .12], colors):
        row = cases[f'Q1000-e{e:g}']
        r = np.array(row['profile']['r'])
        mask = r <= 20
        axs[1, 0].plot(r[mask], np.array(row['profile']['Omega'])[mask], color=color, label=f'e={e:g}')
        axs[1, 0].axhline(row['omega'], color=color, ls=':', lw=.9)
    axs[1, 0].set_title('C  Local frequency and its infinity limit, Q=1000', loc='left', fontsize=11)
    axs[1, 0].set_xlabel('Radius (inverse exterior scalar mass)')
    axs[1, 0].set_ylabel('Omega(r) (exterior scalar mass = 1)')
    axs[1, 0].legend(frameon=False, fontsize=9)
    axs[1, 0].grid(alpha=.18)
    es = [0., .04, .08, .12]
    bases = np.zeros(len(es))
    terms = [('gradient_energy', 'Field gradients', '#246B8E'), ('potential_energy', 'Potential', '#B1B6BC'),
             ('rotation_energy', 'Scalar rotation', '#4E7662'), ('electric_inside', 'Electric inside R=40', '#C29659'),
             ('electric_outside', 'Electric outside R=40', '#A44A3F')]
    for field, label, color in terms:
        values = np.array([cases[f'Q1000-e{e:g}'][field] / 1000 for e in es])
        axs[1, 1].bar(np.arange(len(es)), values, bottom=bases, label=label, color=color, width=.65)
        bases += values
    axs[1, 1].axhline(1., color='.25', ls='--', lw=1)
    axs[1, 1].set_xticks(np.arange(len(es)), [f'{e:g}' for e in es])
    axs[1, 1].set_xlabel('Electric coupling e (dimensionless)')
    axs[1, 1].set_ylabel('Energy / Q (exterior scalar mass = 1)')
    axs[1, 1].set_title('D  Every energy term included, Q=1000', loc='left', fontsize=11)
    axs[1, 1].legend(frameon=False, fontsize=8, loc='upper left', bbox_to_anchor=(1.01, 1.))
    fig.suptitle('Selected classical gauge model: binding is a restricted energy comparison', fontsize=14)
    fig.supxlabel('Source: preserved NumPy/SciPy stationary solves. Hollow points fail the registered localization gate; six unconverged solves omitted from curves but retained in JSON.\nNo full-field dynamical or physical-particle stability claim. All charge values are classical model charges.', fontsize=9)
    fig.savefig(OUT / 'gauge-evidence.png', dpi=170)
    fig.savefig(OUT / 'gauge-evidence.svg')
    plt.close(fig)
    check_count = sum(len(d['checks']) for d in datasets.values())
    failures = {k: dict(message=v['message'], omega=v['omega'], energy_per_charge=v['energy_per_charge']) for k, v in cases.items() if not v['success']}
    assessment = dict(status='qualified selected gauge branch; ACS particle identification remains underdetermined',
        checks_passed=check_count, continuum_runs=len(cases) + len(survey['continuations']) + len(datasets['fission-results']['cases']),
        independent_finite_volume_runs=len(datasets['finite-volume-results']['cases']),
        preserved_solver_failures=failures,
        references={f'e{e:g}': {k: cases[f'Q1000-e{e:g}'][k] for k in ['energy', 'energy_per_charge', 'omega', 'electric_inside', 'electric_outside', 'radius90']} for e in [0., .04, .08, .12]},
        full_field_boundary=dict(selected_vacuum_massless_gauge_modes=18, charged_vector_charge_per_q='2/3', physical_flat_scalar_modes=4,
                                 conventional_vacuum_massless_modes=9, neutral_Delta_electric_charge=0),
        parameter_nonuniqueness='Same 2/3 Yukawa ratio yields opposite pair thresholds; permitted norm potentials have binding and no-binding regions; dimensional rescaling leaves Q fixed.',
        limitations=['Not a full non-Abelian decay trajectory or quantum lifetime.', 'No physical ACS vacuum, complete coefficient map or carrier spectrum selected.',
                     'No all-branches nonexistence or all-partitions fission proof.', 'No source manuscripts or previous evidence edited.'],
        prior_receipts_verified=prior)
    (OUT / 'assessment.json').write_text(json.dumps(assessment, indent=2) + '\n')
    paths = [p for p in OUT.rglob('*') if p.is_file() and p.name != 'receipt.json']
    paths += [Path(__file__).resolve(), ROOT / 'code/condensate_energy/gauge_completion.py',
              ROOT / 'code/condensate_energy/gauge_finite_volume.py', ROOT / 'code/condensate_energy/gauge_carrier_contract.py',
              ROOT / 'code/condensate_energy/gauge_fission.py', ROOT / 'code/condensate_energy/parameter_identifiability.py',
              ROOT / 'code/condensate_energy/carrier_threshold_countermodels.py', OUT.parent / 'investigation-conclusion.md']
    receipt = dict(status=assessment['status'], checks_passed=check_count,
                   prior_receipts_verified=prior,
                   artifact_sha256={str(p.relative_to(ROOT)): digest(p) for p in sorted(set(paths))})
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=check_count, artifacts=len(receipt['artifact_sha256']),
                         continuum_runs=assessment['continuum_runs'], independent_runs=assessment['independent_finite_volume_runs'],
                         preserved_solver_failures=len(failures)), indent=2))


if __name__ == '__main__':
    summarize_gauge_evidence()
