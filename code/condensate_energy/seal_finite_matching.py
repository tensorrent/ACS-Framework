#!/usr/bin/env python3
"""Render finite matching, preserve evidence and verify the receipt chain."""
from dataclasses import asdict, replace
from hashlib import sha256
import json
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from finite_light_matching import ROOT, OUT, Parameters, threshold


def main():
    names = ['matching.json', 'verification.json', 'exact-RG.json', 'archive-inputs.json']
    results = [json.loads((OUT / name).read_text()) for name in names]
    total = sum(r['checks_total'] for r in results)
    assert all(r['checks_passed'] == r['checks_total'] for r in results)
    assert all(c['passed'] for r in results for c in r['checks'])
    base = Parameters()
    assumed = replace(base, lambda0=2 * np.sqrt(3) / 27)
    assumption_result = dict(parameters=asdict(assumed), threshold=threshold(assumed),
        qualification='The proposed bracket value is inserted as an assumption. It is not selected or fitted by this calculation.')
    (OUT / 'assumed-bracket-example.json').write_text(json.dumps(assumption_result, indent=2) + '\n')
    portals = np.linspace(0, .4, 201)
    tree = [replace(assumed, portal=k).light for k in portals]
    matched = [threshold(replace(assumed, portal=k))['canonical_quartic'] for k in portals]
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.2), layout='constrained')
    axes[0].axhline(assumed.lambda0, color='.45', ls='--', label=r'Assumed $\lambda_0=2\sqrt{3}/27$')
    axes[0].plot(portals, tree, lw=2.2, color='#b26845', label='After tree matching')
    axes[0].plot(portals, matched, lw=2.2, color='#286785', label='After canonical one-loop matching')
    axes[0].set(xlabel='Independent norm portal k', ylabel='Light-doublet quartic coupling',
                title='One proposed input does not fix the light coupling')
    axes[0].legend(frameon=False, fontsize=8.4)
    th = results[0]['examples'][0]['threshold']
    values = np.array([th['potential_quartic_threshold'], th['kinetic_quartic_threshold'], th['total_quartic_threshold']]) * 1e3
    axes[1].bar(['Potential', 'Kinetic', 'Total'], values, color=['#b26845', '#286785', '#48846a'], width=.6)
    axes[1].axhline(0, color='.5', lw=1)
    for i, value in enumerate(values):
        axes[1].text(i, value + (.04 if value > 0 else -.04), f'{value:+.6f}', ha='center', va='bottom' if value > 0 else 'top', fontsize=9)
    axes[1].set(ylabel=r'One-loop quartic shift ($\times 10^{-3}$)', ylim=(-.8, 1.4),
                title='Kinetic matching reverses the correction in this example')
    for axis in axes:
        axis.spines[['top', 'right']].set_visible(False)
        axis.grid(axis='y', alpha=.15)
    fig.suptitle('ACS action to light-field coupling: finite one-loop matching', fontsize=15)
    fig.supxlabel('Conditional Landau-gauge MS-bar branch: d = mu = 1, lambda7 = 0.5; remaining inputs and the selected light doublet are stated in the report.\n'
                  'Left: assumed bracket boundary. Right: representative lambda0 = 0.2, k = 0.2. Neither panel is a Higgs pole-mass prediction.', fontsize=8.4)
    for ext in ['png', 'svg']:
        fig.savefig(OUT / ('finite-matching.' + ext), dpi=180)
    plt.close(fig)
    attempts = OUT / 'attempts'
    for source, name in [('acs-finite-light-matching.log', 'matching-qualified.log'),
                         ('acs-verify-finite-matching.log', 'verification.log'),
                         ('acs-exact-matching-rg.log', 'exact-RG.log'),
                         ('acs-archive-matching-inputs.log', 'archive-qualified.log')]:
        p = Path('/private/tmp') / source
        if p.exists():
            (attempts / name).write_bytes(p.read_bytes())
    prior_path = ROOT / 'docs/condensate_energy/radiative_flat_modes/receipt.json'
    prior = dict(json.loads(prior_path.read_text())['prior_receipts_verified'])
    prior[str(prior_path.relative_to(ROOT))] = sha256(prior_path.read_bytes()).hexdigest()
    old_artifacts = {}
    for name, expected in prior.items():
        p = ROOT / name
        assert sha256(p.read_bytes()).hexdigest() == expected, name
        for artifact, digest in json.loads(p.read_text()).get('artifact_sha256', {}).items():
            assert sha256((ROOT / artifact).read_bytes()).hexdigest() == digest, artifact
            old_artifacts[artifact] = digest
    assessment = dict(status='Conditional dimension-four finite-matching stage complete; full ACS investigation active',
        previous_turn_classification='progress', checks_passed=total,
        established=['Heavy scalar/vector/Weyl spectra and eigenvalue jets on the declared stable branch',
            'Finite mass, quartic and kinetic thresholds with mixed heavy/light effects',
            '80-digit light-field subtraction limits and independent component checks',
            'Exact symbolic mass and canonical-quartic RG matching identities',
            'Archived vacuum-selection operator has rank at most two; third eigvalsh magnitude is spurious',
            'Archived Majorana scale is inverse inference from an inserted target, with a separate factor-1000 unit inconsistency'],
        remaining=['General mixed-quartic and noncommuting-flavor matching if required by a surviving proposed action',
            'Source construction selecting normalized action coefficients, vacuum/matching scale and flavor inputs',
            'Original-scope recovery/completion audit; no exhaustive whole-drive/chat claim yet'],
        physical_limits=['No selected physical scale or pole mass', 'No complete dimension-six EFT',
            'Stable tree branch does not itself select the boundary parameters',
            'Source-specific failed proposals do not falsify unrelated constructions'])
    (OUT / 'assessment.json').write_text(json.dumps(assessment, indent=2) + '\n')
    scripts = ['finite_light_matching.py', 'verify_finite_matching.py', 'exact_matching_rg.py',
               'archive_matching_inputs.py', 'seal_finite_matching.py']
    artifacts = [ROOT / 'code/condensate_energy' / name for name in scripts]
    artifacts += [p for p in OUT.rglob('*') if p.is_file() and p.name != 'receipt.json' and '__pycache__' not in p.parts]
    receipt = dict(status=assessment['status'], checks_passed=total, prior_receipts_verified=prior,
        prior_artifacts_verified=old_artifacts,
        artifact_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(artifacts)})
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=total, artifact_hashes=len(receipt['artifact_sha256']),
        prior_receipts=len(prior), prior_artifacts=len(old_artifacts))))


if __name__ == '__main__':
    main()
