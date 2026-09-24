#!/usr/bin/env python3
"""Render the action-matching evidence and seal this completed research stage."""
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
OUT = ROOT / 'docs/condensate_energy/action_matching'


def main():
    results = [json.loads((OUT / name).read_text()) for name in ['spectrum.json', 'tree-matching.json', 'orbit-bounds.json']]
    checks = sum(r['checks_passed'] for r in results)
    assert checks == sum(r['checks_total'] for r in results)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.1), layout='constrained')
    labels = ['Old color trace', 'Old spin trace', 'Full-basis example']
    negative, flat, positive = [48, 36, 0], [2, 14, 0], [1, 1, 51]
    positions = np.arange(3)
    axes[0].bar(positions, negative, label='Negative mass squared', color='#b35435')
    axes[0].bar(positions, flat, bottom=negative, label='Physical flat modes', color='#b7b7b7')
    axes[0].bar(positions, positive, bottom=np.array(negative) + flat, label='Positive mass squared', color='#356f87')
    for i, rows in enumerate(zip(negative, flat, positive)):
        base = 0
        for value in rows:
            if value >= 2:
                axes[0].text(i, base + value / 2, str(value), ha='center', va='center', color='white' if value != flat[i] else 'black')
            base += value
    axes[0].set(xticks=positions, xticklabels=labels, ylabel='Physical real Delta modes (count)', ylim=(0, 64),
                title='Neutral-vacuum stability in explicit examples')
    axes[0].legend(frameon=False, loc='upper left', fontsize=8.5)
    axes[0].spines[['right', 'top']].set_visible(False)
    k = np.linspace(0, .6, 250)
    high = 2 * np.sqrt(3) / 27
    axes[1].plot(k, high - k ** 2 / 4, lw=2.5, color='#356f87', label='Matched light quartic')
    axes[1].axhline(high, color='.45', ls='--', label='Assumed high-scale quartic')
    axes[1].set(xlabel=r'Effective portal coupling $k_{\mathrm{eff}}$ (dimensionless)',
                ylabel=r'Quartic coupling $\lambda$ (dimensionless)',
                title='A fixed bracket value does not fix the low-energy quartic')
    axes[1].legend(frameon=False, fontsize=8.5)
    axes[1].grid(alpha=.2)
    fig.suptitle('ACS action-to-spectrum and tree-matching audit', fontsize=16)
    fig.supxlabel('Left: old rho1=1/2, rho2=7/9 versus the stated stable full-basis example; nine gauge modes removed.\n'
                  'Right: conditional illustration, lambda7=1 and lambda_high=2 sqrt(3)/27; no experimental fit or pole-mass prediction.', fontsize=8.5)
    for extension in ['png', 'svg']:
        fig.savefig(OUT / ('action-matching.' + extension), dpi=180)
    plt.close(fig)
    attempts = OUT / 'attempts'
    attempts.mkdir(exist_ok=True)
    for source, dest in [('acs-action-spectrum-qualified.log', 'spectrum-qualified.log'),
                         ('acs-action-tree-matching.log', 'tree-matching.log'),
                         ('acs-action-orbit-bounds.log', 'orbit-bounds.log')]:
        p = Path('/private/tmp') / source
        if p.exists():
            (attempts / dest).write_bytes(p.read_bytes())
    assessment = dict(status='Action-to-spectrum and tree-level matching stage complete; broader goal active',
        checks_passed=checks, failed_initial_attempt='Preserved gauge polynomial symbol-assumption mismatch; qualified result passes.',
        established=['Complete stationary first-stage Delta spectrum, 51 physical modes and nine Goldstones',
          'Exact gauge vector spectrum', 'Both explicit old two-trace positive-rho2 ranges are unstable at the neutral vacuum',
          'Sharp quartic orbit bounds for both two-trace readings', 'A stable full-basis neutral example',
          'Exact tree-level heavy-radial potential matching and light-doublet mass matrix',
          'Canonical-action normalization remains independent of the bracket projection'],
        next_calculable_work=['Radiative lifting of extra flat modes on corrected rho2<0 two-trace boundaries',
          'Finite one-loop matching on stable complete potentials, with explicit scheme and boundary assumptions',
          'Continue targeted recovery and testing of action/kinetic constructions in the research history'],
        unresolved_physical_inputs=['Index-explicit normalized ACS action selecting boundary coefficients',
          'Matching scale and light-field selection', 'Flavor matrices and physical calibrations'],
        forbidden_promotions=['No physical Higgs mass derived', 'No proof of matter origin or exact quantum charge',
          'No exhaustive whole-drive/chat-search claim', 'No claim that all mathematical ACS branches are resolved'])
    (OUT / 'assessment.json').write_text(json.dumps(assessment, indent=2) + '\n')
    previous = ROOT / 'docs/condensate_energy/hidden_couplings/receipt.json'
    previous_receipt = json.loads(previous.read_text())
    for path, digest in previous_receipt['artifact_sha256'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    prior = dict(previous_receipt['prior_receipts_verified'])
    prior[str(previous.relative_to(ROOT))] = sha256(previous.read_bytes()).hexdigest()
    for path, digest in prior.items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    sources = ['action_matching_spectrum.py', 'action_tree_matching.py', 'action_orbit_bounds.py', 'seal_action_matching.py']
    artifacts = [ROOT / 'code/condensate_energy' / name for name in sources]
    artifacts += [p for p in OUT.rglob('*') if p.is_file() and p.name != 'receipt.json' and '__pycache__' not in p.parts]
    receipt = dict(status=assessment['status'], checks_passed=checks, prior_receipts_verified=prior,
        artifact_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(artifacts)})
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=checks, artifact_hashes=len(receipt['artifact_sha256']), prior_receipts=len(prior))))


if __name__ == '__main__':
    main()
