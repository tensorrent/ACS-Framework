#!/usr/bin/env python3
"""Render the leakage evidence, retaining the two numerical failures."""
import hashlib
import json
import math
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from self_binding import ROOT

OUT = ROOT / 'docs/condensate_energy/charge_leakage'


def field(row, key):
    return np.array([v[key] for v in row['history']])


def main():
    nonlinear = json.loads((OUT / 'results.json').read_text())
    refined = json.loads((OUT / 'refinement-results.json').read_text())
    radiation_raw = json.loads((OUT / 'radiation-results.json').read_text())
    radiation = json.loads((OUT / 'radiation-qualified.json').read_text())
    assert refined['all_checks_passed'] and radiation['all_checks_passed']
    assert [v['name'] for v in nonlinear['checks'] if not v['passed']] == ['refinement-0.5']
    assert [v['name'] for v in radiation_raw['checks'] if not v['passed']] == ['continuum-solver-residual']
    for data in [nonlinear, refined, radiation_raw, radiation]:
        for name, digest in data['source_sha256'].items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    response = radiation['cases']['real-BVP-R30']
    omega = response['omega']
    b = nonlinear['cases']['ratio-0']['parameters']['b']
    expected_amplitudes = np.abs(np.array(response['boundary_amplitudes']) @ np.array([1, 1j])) / 40
    expected_amplitudes[2] /= math.sqrt(2)
    diagnostic = {}
    for name in ['flux-0.001', 'flux-0.01', 'flux-0.05']:
        row = refined['cases'][name]
        t = field(row, 't')
        keep = t >= 200
        t = t[keep]
        q = (field(row, 'q40_real') + 1j * field(row, 'q40_imag'))[keep]
        chi = field(row, 'chi40')[keep]
        window = np.hanning(len(t))
        epsilon = b * row['parameters']['ratio']
        measured = [abs(np.sum(window * values * np.exp(-1j * frequency * t)) / window.sum()) / epsilon
                    for values, frequency in [(q, -3 * omega), (q, 5 * omega), (chi, 4 * omega)]]
        diagnostic[name] = dict(measured_mode_amplitudes_per_epsilon=measured,
                                predicted_mode_amplitudes_per_epsilon=expected_amplitudes.tolist(),
                                measured_over_predicted=(np.array(measured) / expected_amplitudes).tolist(),
                                mean_total_power_per_epsilon_squared=row['power_per_epsilon_squared'],
                                predicted_steady_power_per_epsilon_squared=response['power_per_epsilon_squared'],
                                block_total_power_per_epsilon_squared=(np.array(row['power_block_means']) / epsilon ** 2).tolist(),
                                method='Hann-weighted complex projection at fixed reference frequencies over t200–400; no fitted frequencies')
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False, 'axes.grid': True, 'grid.alpha': .18,
                         'axes.titleweight': 'bold'})
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 8.8), layout='constrained')
    ax = axes[0, 0]
    for ratio, color in [(0., '#6a747b'), (.1, '#287e88'), (.25, '#b67c35'), (.5, '#825589'), (.9, '#af484b')]:
        row = nonlinear['cases'][f'ratio-{ratio:g}'] if ratio != .5 else refined['cases']['space-0.025']
        label = f'epsilon/b = {ratio:g}' + (' (finest)' if ratio == .5 else '')
        ax.plot(field(row, 't'), 100 * field(row, 'local_energy_fraction'), color=color, label=label)
    ax.axhline(50, color='black', ls=':', lw=1)
    ax.set(title='A  Breaking strength changes core retention', xlabel='Time (dimensionless)',
           ylabel='Energy within radius 15 (% of initial)', ylim=(0, 103))
    ax.legend(fontsize=8)
    ax = axes[0, 1]
    for row, label, color in [(nonlinear['cases']['ratio-0.5'], 'dr 0.1', '#b67c35'),
                              (nonlinear['cases']['refined-0.5'], 'dr 0.05', '#825589'),
                              (refined['cases']['space-0.025'], 'dr 0.025', '#287e88')]:
        ax.plot(field(row, 't'), 100 * field(row, 'local_energy_fraction'), label=label, color=color)
    ax.axhline(50, color='black', ls=':', lw=1)
    ax.set(title='B  Strong-breaking onset converges under refinement', xlabel='Time (dimensionless)',
           ylabel='Energy within radius 15 (% of initial)', xlim=(95, 170), ylim=(30, 75))
    ax.legend(fontsize=8)
    ax = axes[1, 0]
    for name, color in [('flux-0.001', '#287e88'), ('flux-0.01', '#b67c35'), ('flux-0.05', '#825589')]:
        ax.plot([225, 275, 325, 375], diagnostic[name]['block_total_power_per_epsilon_squared'], 'o-',
                label=name.replace('flux-', 'epsilon/b = '), color=color)
    ax.axhline(response['power_per_epsilon_squared'], color='black', ls='--', label='Steady outgoing response')
    ax.set(title='C  Total flux still includes decaying wave components', xlabel='Center of 50-unit averaging window',
           ylabel='Outward power at radius 40 / epsilon²', ylim=(0, None))
    ax.legend(fontsize=8)
    ax = axes[1, 1]
    row = refined['cases']['flux-0.001']
    t = field(row, 't')
    keep = t >= 200
    n = int(keep.sum())
    window = np.hanning(n)
    freq = 2 * math.pi * np.fft.fftshift(np.fft.fftfreq(n, .1))
    for values, label, color in [((field(row, 'q40_real') + 1j * field(row, 'q40_imag'))[keep], 'Complex field q', '#287e88'),
                               (field(row, 'chi40')[keep], 'Condensate chi', '#b67c35')]:
        spectrum = np.abs(np.fft.fftshift(np.fft.fft((values - values.mean()) * window))) / window.sum()
        ax.semilogy(freq, spectrum / (b * .001), color=color, label=label)
    for nu in [-3 * omega, 5 * omega]:
        ax.axvline(nu, color='#287e88', ls=':', lw=1)
    for nu in [-4 * omega, 4 * omega]:
        ax.axvline(nu, color='#b67c35', ls=':', lw=1)
    ax.set(title='D  Predicted harmonics coexist with transient bands', xlabel='Angular frequency (inverse time units)',
           ylabel='Windowed field amplitude / epsilon', xlim=(-4.2, 4.5), ylim=(1e-7, .03))
    ax.legend(fontsize=8)
    fig.suptitle('Charge breaking: localized survival, dispersal, and measurable radiation', fontsize=15)
    for extension in ['png', 'svg']:
        fig.savefig(OUT / f'leakage-evidence.{extension}', dpi=170)
    plt.close(fig)
    report = dict(status='qualified_scoped_charge_breaking_experiment', nonlinear_runs=len(nonlinear['cases']) + len(refined['cases']),
                  exact_embedding_checks=len(nonlinear['contract']['checks']),
                  preserved_failures=[v for v in nonlinear['checks'] + radiation_raw['checks'] if not v['passed']],
                  targeted_refinement_checks=refined['checks'], linear_response_checks=radiation['checks'],
                  finest_strong_case={k: refined['cases']['space-0.025'][k] for k in ['parameters', 'initial_energy',
                                      'final_local_energy_fraction', 'final_total_charge_fraction', 'half_energy_exit']},
                  half_energy_exit_sequence=[nonlinear['cases']['ratio-0.5']['half_energy_exit'], nonlinear['cases']['refined-0.5']['half_energy_exit'],
                                             refined['cases']['space-0.025']['half_energy_exit']],
                  harmonic_comparison=diagnostic, steady_response={k: response[k] for k in ['power_per_epsilon_squared', 'power_channels',
                                      'charge_flux_per_epsilon_squared', 'charge_source_per_epsilon_squared', 'source_flux_identity_relative']},
                  initial_E_over_P_coefficient=radiation['initial_energy_over_power_coefficient'],
                  limitations=['dimensionless selected classical action, not fixed by ACS', 'no universal physical half-life',
                               'steady harmonic power does not equal full transient flux', 'unrestricted gauge/scalar perturbations and quantum emission remain untested',
                               'gauge-compatible ansatz uses a different vacuum and field orientation from the neutral Delta identification'])
    (OUT / 'assessment.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(runs=report['nonlinear_runs'], strong=report['finest_strong_case'], modes=diagnostic,
                          steady_response=report['steady_response']), indent=2))


if __name__ == '__main__':
    main()
