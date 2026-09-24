#!/usr/bin/env python3
"""Validate recorded evidence, render figures and assemble an amended receipt."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from run import ROOT, plt

OUT = ROOT/'docs/condensate_energy/capture_stability'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def series(case, key):
    return [r[key] for r in case['history']]


def main():
    latest = json.loads((OUT/'latest-attempt.json').read_text())
    attempt = ROOT/latest['attempt']
    evidence = json.loads((attempt/'results.json').read_text())
    supplement = json.loads((OUT/'bound-domain-results.json').read_text())
    failed = [r for r in evidence['checks'] if not r['passed']]
    expected_failure = 'bound-mode control is insensitive to remote wall'
    if len(failed)!=1 or failed[0]['name']!=expected_failure:
        raise RuntimeError('Only the documented spectral domain failure can be superseded.')
    if not supplement['all_checks_passed'] or not all(r['passed'] for r in supplement['checks']):
        raise RuntimeError('Supplemental checks did not pass.')
    for payload in [evidence, supplement]:
        for name, digest in payload['source_sha256'].items():
            if sha(ROOT/name)!=digest:
                raise RuntimeError(f'Source changed since recorded execution: {name}')
    prior_receipt = json.loads((OUT.parent/'receipt.json').read_text())
    for name, digest in prior_receipt['artifact_sha256'].items():
        if sha(ROOT/name)!=digest:
            raise RuntimeError(f'Frozen parent artifact changed: {name}')
    cases = evidence['cases']
    if len(cases)!=23:
        raise RuntimeError('Incomplete frozen sweep')

    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10,
                         'axes.spines.top':False, 'axes.spines.right':False,
                         'axes.titleweight':'bold', 'axes.grid':True,
                         'grid.alpha':.18, 'figure.facecolor':'white',
                         'savefig.facecolor':'white'})
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.2), layout='constrained')
    times = [16, 20, 24, 28, 32, 36]
    colors = plt.cm.viridis(np.linspace(.08, .92, len(times)))
    ax = axes[0, 0]
    for t, color in zip(times, colors):
        c = cases[f'close-h16-t{t}']
        ax.plot(series(c, 't'), series(c, 'trapped'), color=color, label=f'Close at {t}')
    c = cases['static-h16']
    ax.plot(series(c, 't'), series(c, 'trapped'), 'k--', label='Always raised')
    ax.set(title='A  Timing changes retention', xlabel='Time (model units)',
           ylabel='Cavity + barrier energy / incoming energy', xlim=(0, 160))
    ax.legend(ncol=2, fontsize=8, loc='upper right')
    ax = axes[0, 1]
    for h, color in [(4, '#3274a1'), (16, '#d17b26')]:
        values = [cases[f'close-h{h}-t{t}']['summary']['at_160']['trapped'] for t in times]
        ax.plot(times, values, 'o-', color=color, label=f'Final barrier height {h}')
        ax.axhline(cases[f'static-h{h}']['summary']['at_160']['trapped'], color=color,
                   ls=':', label=f'Always raised, height {h}')
    ax.set(title='B  Every registered closing time', xlabel='Closure start time',
           ylabel='Retained energy at t = 160 / incoming energy', xticks=times)
    ax.legend(fontsize=8)
    ax = axes[1, 0]
    c = cases['close-h16-t28']
    t = series(c, 't')
    ax.plot(t, series(c, 'total'), color='#a33b38', label='Total field energy')
    ax.plot(t, 1+np.array(series(c, 'work')), 'k--', label='Initial energy + gate work')
    ax.plot(t, series(c, 'trapped'), color='#3274a1', label='Cavity + barrier energy')
    ax.plot(t, series(c, 'work'), color='#d17b26', label='Work supplied by gate')
    ax.axvspan(28, 32, color='gray', alpha=.13)
    ax.set(title='C  Closure supplies energy', xlabel='Time (model units)',
           ylabel='Energy / incoming energy', xlim=(15, 160))
    ax.legend(fontsize=8, loc='center right')
    ax = axes[1, 1]
    for name, label, color in [('close-h16-t28', 'Gate remains raised', '#3274a1'),
                                ('reopen-h16-t28', 'Reopen from t = 60 to 64', '#a33b38')]:
        c = cases[name]
        ax.plot(series(c, 't'), series(c, 'trapped'), label=label, color=color)
    ax.axvspan(60, 64, color='gray', alpha=.15)
    ax.set(title='D  Opening the gate releases storage', xlabel='Time (model units)',
           ylabel='Cavity + barrier energy / incoming energy', xlim=(20, 100))
    ax.legend(fontsize=8)
    fig.suptitle('Timed capture in a specified 1-D wave model', fontsize=17)
    for extension in ['png', 'svg']:
        fig.savefig(OUT/f'gated-capture.{extension}', dpi=170)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.7), layout='constrained')
    x = np.linspace(0, 22, 1500)
    for j, (omega, kappa) in enumerate(zip(supplement['omega'], supplement['decay_rates'])):
        u = np.where(x<=4, np.sin(omega*x), np.sin(4*omega)*np.exp(-kappa*(x-4)))
        norm2 = 2-math.sin(8*omega)/(4*omega)+math.sin(4*omega)**2/(2*kappa)
        axes[0].plot(x, u/math.sqrt(norm2), label=f'Mode {j+1}: omega = {omega:.5f}')
    axes[0].axvline(4, color='gray', ls=':')
    axes[0].set(title='A  Three analytic localized modes', xlabel='Position (model units)',
                ylabel='L2-normalized mode amplitude')
    axes[0].legend(fontsize=8)
    exact = np.array(supplement['eigenvalues'])
    for dx, color in [(.1, '#d17b26'), (.05, '#3274a1')]:
        errors = abs(np.array(supplement['finite_grid_eigenvalues'][f'D60-dx{dx:g}'])-exact)
        axes[1].semilogy([1, 2, 3], errors, 'o-', label=f'Grid spacing {dx}', color=color)
    axes[1].set(title='B  Independent grid eigenvalues converge', xlabel='Mode', xticks=[1, 2, 3],
                ylabel='Absolute error in squared frequency')
    axes[1].legend()
    fig.suptitle('Binding control: an explicitly supplied exterior threshold U = 4', fontsize=15)
    for extension in ['png', 'svg']:
        fig.savefig(OUT/f'bound-mode-control.{extension}', dpi=170)
    plt.close(fig)

    named_cases = {name: row['summary'] for name, row in cases.items()}
    assessment = dict(status='qualified_with_documented_domain_amendment',
                      original_attempt=str(attempt.relative_to(ROOT)),
                      original_passed_checks=sum(c['passed'] for c in evidence['checks']),
                      original_failed_checks=failed,
                      superseding_supplement='bound-domain-results.json',
                      supplement_passed_checks=len(supplement['checks']),
                      dynamic_variants=23, source_and_parent_hashes_verified=True,
                      physical_conclusions=dict(
                          controlled_finite_time_retention='demonstrated for specified pulse and controls',
                          compact_positive_barrier_L2_bound_mode='excluded by continuum argument in README',
                          supplied_exterior_threshold_bound_modes='three analytic modes, independently checked',
                          autonomous_capture='not implemented',
                          elementary_particle_mass='not derived',
                          full_klein_foam='not tested'),
                      cases=named_cases)
    (OUT/'assessment.json').write_text(json.dumps(assessment, indent=2)+'\n')
    paths = [Path(__file__).resolve(), ROOT/'code/condensate_energy/capture_stability.py',
             ROOT/'code/condensate_energy/bound_domain_check.py',
             attempt/'results.json', attempt/'checks.json', attempt/'capture_stability.py',
             attempt/'run.py', attempt/'protocol.md']
    paths += sorted(p for p in OUT.iterdir() if p.is_file() and p.name!='receipt.json')
    receipt = dict(status=assessment['status'], dynamic_variants=23,
                   original_passed=12, original_failed=1, supplemental_passed=3,
                   unresolved_numerical_checks=0,
                   artifact_sha256={str(p.relative_to(ROOT)):sha(p) for p in paths})
    (OUT/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({k:v for k,v in assessment.items() if k!='cases'}, indent=2))


if __name__ == '__main__':
    main()
