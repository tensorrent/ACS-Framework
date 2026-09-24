#!/usr/bin/env python3
"""Render and seal the radiative-flat-mode experiment and all follow-up checks."""
from hashlib import sha256
import json
import os
from pathlib import Path
import platform

os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpmath
import numpy as np
import scipy
import sympy

from radiative_flat_modes import ROOT, OUT, analytic_curvature


def main():
    results = [json.loads((OUT / name).read_text()) for name in
               ['results.json', 'vacuum-search.json', 'competing-vacua.json', 'search-audit.json']]
    total = sum(r['checks_total'] for r in results)
    assert total == sum(r['checks_passed'] for r in results)
    assert all(c['passed'] for r in results for c in r['checks'])
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.5), layout='constrained')
    f = np.linspace(.01, .6, 250)
    for kind, color, label in [('spin', '#286785', 'Charged singlet (2 real modes)'),
                               ('color', '#af5836', 'Color sextet (12 real modes)')]:
        values = [1e3 * analytic_curvature(kind, .3, .35, [value])['total'] for value in f]
        axes[0].plot(f, values, color=color, lw=2.4, label=label)
    axes[0].axhline(0, color='.4', lw=1)
    axes[0].set(xlabel='One Majorana singular value f (dimensionless)',
                ylabel=r'Local angular curvature $m^2/d^2$ ($\times 10^{-3}$)',
                title='Fermion loops can reverse the local sign')
    axes[0].legend(frameon=False, fontsize=8.5)
    labels = ['Gauge only', 'One family: f = 0.3', 'One family: f = 0.5', 'Three families: f = 0.3 each']
    colors = ['#7e8d94', '#48846a', '#af5836', '#286785']
    for row, label, color in zip(results[2]['examples'], labels, colors):
        axes[1].plot(row['path_grid'], 1e4 * np.array(row['energy_grid']), label=label,
                     color=color, lw=2.5 if len(row['Majorana_singular']) == 3 else 1.6)
    axes[1].axhline(0, color='.4', lw=1)
    row = results[2]['examples'][-1]
    axes[1].plot([row['path_peak_u']], [1e4 * row['path_peak_energy']], 'o', color=colors[-1])
    axes[1].annotate('Locally positive,\nlower at the endpoint', xy=(1, 1e4 * row['closed_energy_difference']['total']),
                     xytext=(.47, -3.5), fontsize=9, color=colors[-1],
                     arrowprops=dict(arrowstyle='->', color=colors[-1]))
    axes[1].set(xlabel='Position u on the stated tree-minimum path',
                ylabel=r'$(V_1(u)-V_1(0))/d^4$ ($\times 10^{-4}$)',
                title='A competing configuration survives the full test')
    axes[1].legend(frameon=False, fontsize=8, loc='lower left')
    for axis in axes:
        axis.spines[['top', 'right']].set_visible(False)
        axis.grid(alpha=.15)
    fig.suptitle('ACS: finite loop corrections and competing vacuum orientations', fontsize=15)
    fig.supxlabel('Conditional Landau-gauge MS-bar calculation: g4 = 0.3, gR = 0.35, d = boundary scale = 1; flat boundary differences zero.\n'
                  'Right: spin-Gram model, neutral rank-one color to equal rank-four color / real spin; no global-minimum or lifetime certificate.', fontsize=8.5)
    for ext in ['png', 'svg']:
        fig.savefig(OUT / ('radiative-flat-modes.' + ext), dpi=180)
    plt.close(fig)
    attempts = OUT / 'attempts'
    attempts.mkdir(exist_ok=True)
    for stem in ['flat-modes', 'vacuum-search', 'competing-vacua', 'search-audit']:
        source = Path('/private/tmp/acs-radiative-' + stem + '.log')
        if source.exists():
            (attempts / (stem + '.log')).write_bytes(source.read_bytes())
    previous = ROOT / 'docs/condensate_energy/action_matching/receipt.json'
    prior = dict(json.loads(previous.read_text())['prior_receipts_verified'])
    prior[str(previous.relative_to(ROOT))] = sha256(previous.read_bytes()).hexdigest()
    verified_artifacts = {}
    for path, expected in prior.items():
        p = ROOT / path
        assert sha256(p.read_bytes()).hexdigest() == expected, path
        receipt = json.loads(p.read_text())
        for artifact, digest in receipt.get('artifact_sha256', {}).items():
            actual = sha256((ROOT / artifact).read_bytes()).hexdigest()
            assert actual == digest, artifact
            verified_artifacts[artifact] = actual
    search = results[1]
    runs = [run for case in search['searches'] for support in case['supports']
            for batch in ['initial', 'repeated'] for run in support[batch]['runs']]
    assessment = dict(status='Conditional one-loop flat-direction stage complete; broader ACS goal remains active',
        checks_passed=total, search_attempts=len(runs), abnormal_search_stops=sum(not r['success'] for r in runs),
        independent_retries=results[3]['retries_total'],
        established=['Exact gauge spectra on the two diagnostic orbits',
            'Scalar symmetry and stationary-orbit invariance',
            'Analytic finite one-loop curvatures for all fourteen physical tree-flat modes',
            'Exact one-loop cancellation of renormalization-scale dependence at fixed matching boundary',
            'Full tree-minimum family parameterization and component-verified mass spectra',
            'Explicit locally positive but lower competing configuration at the stated three-family boundary'],
        numerical_evidence=['Multistart candidate minima across all four color support caps',
            'Independent Powell qualification of all abnormal L-BFGS-B stops'],
        not_established=['A uniquely selected ACS boundary, scale or vacuum',
            'A rigorous global-minimum certificate from numerical searches',
            'Full one-loop light-doublet matching, pole masses, tunneling lifetimes or higher-loop robustness'],
        next_calculable_work=['Finite one-loop matching on stable full-basis potentials with a declared light doublet',
            'Continue targeted action/kinetic-source recovery and complete the derivability/underdetermination audit'])
    (OUT / 'assessment.json').write_text(json.dumps(assessment, indent=2) + '\n')
    sources = ['radiative_flat_modes.py', 'radiative_vacuum_search.py', 'radiative_competing_vacua.py',
               'radiative_search_audit.py', 'seal_radiative_flat_modes.py']
    artifacts = [ROOT / 'code/condensate_energy' / name for name in sources]
    artifacts += [p for p in OUT.rglob('*') if p.is_file() and p.name != 'receipt.json' and '__pycache__' not in p.parts]
    receipt = dict(status=assessment['status'], checks_passed=total,
        versions=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
            sympy=sympy.__version__, mpmath=mpmath.__version__, matplotlib=matplotlib.__version__),
        prior_receipts_verified=prior, prior_artifacts_verified=verified_artifacts,
        artifact_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(artifacts)})
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=total, artifact_hashes=len(receipt['artifact_sha256']),
        prior_receipts=len(prior), prior_artifacts=len(verified_artifacts), search_attempts=len(runs),
        abnormal_search_stops=assessment['abnormal_search_stops'], independent_retries=results[3]['retries_total'])))


if __name__ == '__main__':
    main()
