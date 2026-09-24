#!/usr/bin/env python3
"""Render exact diagnostic formulas and seal the qualified selection audit."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy/selection_energy'


def render_selection_diagnostics():
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.8), layout='constrained')
    axes[0].bar(['Classifier\nrequires <', 'All allowed\nframes obey ≥'], [.15, .5],
                color=['#b56745', '#286785'], width=.6)
    axes[0].set(title='The real-matrix target is unreachable',
                ylabel='Mean transpose defect', ylim=(0, .65))
    axes[0].text(0, .18, '0.15', ha='center')
    axes[0].text(1, .53, '0.50', ha='center')
    deg = np.linspace(0, 90, 361)
    axes[1].plot(deg, -128/9*np.sin(2*np.deg2rad(deg))**2,
                 color='#b56745', lw=2.2, label='Source diagonal product')
    axes[1].axhline(0, color='#286785', lw=2.2, label='Full tensor contraction')
    axes[1].set(title='A basis rotation exposes the artifact', xlabel='Basis rotation (degrees)',
                ylabel='Algebraic diagnostic', xticks=[0, 45, 90], ylim=(-16, 3))
    axes[1].legend(frameon=False, fontsize=8, loc='lower left')
    t = np.geomspace(.01, 1000, 700)
    axes[2].semilogx(t, (t+2/3)/(1+2*t/3), color='#286785', lw=2.2)
    axes[2].axhline(1.5, color='#b56745', ls='--', label='Exact upper bound: 1.5')
    axes[2].scatter([50], [152/103], color='#286785')
    axes[2].text(.02, 1.32, 'Source target 40 is outside\nthe entire positive domain.', fontsize=9)
    axes[2].set(title='Positive tan β cannot fix the ratio', xlabel='tan β > 0',
                ylabel='(tan β + 2/3) / (1 + 2 tan β / 3)', ylim=(.6, 1.7))
    axes[2].legend(frameon=False, fontsize=8, loc='lower right')
    for ax in axes:
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=.15)
    fig.suptitle('ACS selection audit: exact constraints before numerical searches', fontsize=15)
    fig.supxlabel('These are diagnostics of the archived formulas. The retained tensor cancellation is not a vacuum-energy prediction.\n'
                  'Physical spectra require the specified action and kinetic metric; independent Yukawa matrices remain a different hypothesis.', fontsize=8.5)
    for ext in ['png', 'svg']:
        fig.savefig(OUT / ('selection-energy.' + ext), dpi=180)
    plt.close(fig)
    print('Rendered selection-energy.png and .svg')


def seal_selection_diagnostics():
    names = ['symmetry-selection.json', 'vacuum-energy.json', 'verification.json', 'yukawa-boundary.json']
    results = [json.loads((OUT / n).read_text()) for n in names]
    assert all(x['checks_total'] == x['checks_passed'] for x in results)
    assert all(c['passed'] for x in results for c in x['checks'])
    total = sum(x['checks_total'] for x in results)
    prior_path = ROOT / 'docs/condensate_energy/input_closure/receipt.json'
    previous = json.loads(prior_path.read_text())
    prior = dict(previous['prior_receipts_verified'])
    prior[str(prior_path.relative_to(ROOT))] = sha256(prior_path.read_bytes()).hexdigest()
    prior_artifacts = {}
    for name, digest in prior.items():
        p = ROOT / name
        assert sha256(p.read_bytes()).hexdigest() == digest, name
        for path, h in json.loads(p.read_text()).get('artifact_sha256', {}).items():
            assert sha256((ROOT / path).read_bytes()).hexdigest() == h, path
            prior_artifacts[path] = h
    for row in json.loads((OUT / 'provenance.json').read_text()):
        assert sha256((ROOT / row['snapshot']).read_bytes()).hexdigest() == row['sha256']
    for log in ['acs-symmetry-selection.log', 'acs-vacuum-energy.log',
                'acs-verify-selection-energy.log', 'acs-yukawa-selector-boundary.log']:
        (OUT / 'attempts' / log).write_bytes((Path('/private/tmp') / log).read_bytes())
    review = json.loads((OUT / 'visual-review.json').read_text())
    assert review['reviewed'] and review['legible']
    assessment = dict(status='Selection and energy stage complete; full ACS goal active',
        checks_passed=total,
        established=['Real eight-frame search excludes its compactness target',
            'Eight-dimensional closure does not uniquely select split sl3',
            'Source diagonal Killing pairing depends on the basis',
            'Correct full contraction still vanishes but is not a determinant calculation',
            'The inherited vacuum beta is independently confirmed; its integration constant remains free',
            'The full gauge action preserves Q rather than TBL alone',
            'Positive tan beta cannot repair the stated proportional Yukawa formula'],
        retained=['Valid compact su3 forward construction with the appropriate real form',
            'Prior conditional spectra and finite matching',
            'Independent norm-constrained Yukawa matrices are not excluded'],
        remaining=['Reconcile source inventory and original goal scope',
            'Inspect surviving action-level input and scale derivations before closure'],
        limits=['No absolute vacuum-energy or new particle-mass prediction',
            'No universal no-go theorem for independently specified ACS actions',
            'Short selector flows do not classify all attractors'])
    (OUT / 'assessment.json').write_text(json.dumps(assessment, indent=2) + '\n')
    scripts = ['symmetry_selection_audit.py', 'vacuum_energy_audit.py',
               'verify_selection_energy.py', 'yukawa_selector_boundary.py', 'publish_selection_energy.py']
    artifacts = [ROOT / 'code/condensate_energy' / x for x in scripts]
    artifacts.extend(p for p in OUT.rglob('*') if p.is_file() and p.name != 'receipt.json' and '__pycache__' not in p.parts)
    receipt = dict(status=assessment['status'], checks_passed=total,
        prior_receipts_verified=prior, prior_artifacts_verified=prior_artifacts,
        artifact_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(artifacts)})
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=total, artifacts=len(receipt['artifact_sha256']),
                         prior_receipts=len(prior), prior_artifacts=len(prior_artifacts))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--render-only', action='store_true')
    mode.add_argument('--seal', action='store_true')
    args = parser.parse_args()
    if args.render_only:
        render_selection_diagnostics()
    else:
        seal_selection_diagnostics()
