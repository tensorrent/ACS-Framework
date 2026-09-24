#!/usr/bin/env python3
"""Render and seal the scoped action-to-carrier completion audit."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import re

os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpmath
import numpy as np
import scipy
import sympy

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/condensate_energy/endpoint_audit'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((OUT / name).read_text())


def render_endpoint_audit():
    rg = read('identifiability.json')['source_RG']
    cutoff = read('microscopic.json')['CPF_cutoffs']
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2), layout='constrained')
    upper = [v['lambda_UV'] for v in rg['alternatives']]
    lower = [v['lambda_IR'] for v in rg['alternatives']]
    axes[0].plot(upper, lower, 'o-', lw=2, ms=7, color='#24647d',
                 label='Three independently integrated boundaries')
    axes[0].axhline(.1294, color='#a45637', ls='--', lw=1.5,
                    label='Historical source comparison input: 0.1294')
    axes[0].set(title='Running retains boundary dependence',
                xlabel='Specified upper-scale quartic λUV',
                ylabel='Calculated lower-scale quartic λIR',
                xlim=(.07, .19), ylim=(.12, .202), xticks=[.08, .10, .12, .14, .16, .18])
    axes[0].text(.075, .197, f'Local sensitivity: {rg["derivative_IR_wrt_UV"]:.6f}',
                 fontsize=10, va='top')
    axes[0].legend(frameon=False, fontsize=8, loc='lower right')
    log_ratio = np.linspace(-130, -45, 400)
    inverse = (np.log(8) - log_ratio*np.log(10) + 1) / 2
    axes[1].plot(log_ratio, inverse, color='#24647d', lw=2)
    chosen = float(cutoff['inserted_inverse_alpha'])
    axes[1].axhline(chosen, color='#a45637', ls='--', lw=1.5,
                    label=f'Inserted target K = {chosen:.6f}')
    xs = np.log10(float(cutoff['source_exponential']))
    xm = np.log10(float(cutoff['self_energy_consistent_exponential']))
    axes[1].scatter([xs, xm], [chosen/2, chosen], s=45,
                    c=['#976932', '#24647d'], zorder=3)
    axes[1].annotate('Source cutoff gives K/2', (xs, chosen/2),
                     xytext=(-110, 65), fontsize=9,
                     arrowprops=dict(arrowstyle='->', color='#976932'))
    axes[1].annotate('Corrected cutoff reproduces K', (xm, chosen),
                     xytext=(-113, 156), fontsize=9,
                     arrowprops=dict(arrowstyle='->', color='#24647d'))
    axes[1].set(title='Self-energy matching still needs a cutoff',
                xlabel='Specified thickness ratio log₁₀(a/R)',
                ylabel='Conditional inverse coupling: [log(8R/a)+1]/2',
                xlim=(-130, -45), ylim=(45, 165), xticks=[-120, -100, -80, -60])
    axes[1].legend(frameon=False, fontsize=8, loc='upper right', bbox_to_anchor=(1, .77))
    for ax in axes:
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=.16)
    fig.suptitle('ACS endpoint: calculations do not remove unselected inputs', fontsize=14)
    fig.supxlabel('Left: source one-loop SM truncation and historical mixed inputs; connecting segments guide the eye.\n'
                  'Right: the recovered capacitor approximation; both marked cutoffs are chosen inputs, not topological predictions.', fontsize=8.5)
    for ext in ['png', 'svg']:
        fig.savefig(OUT / ('endpoint-boundary.' + ext), dpi=180)
    plt.close(fig)
    print('Rendered endpoint-boundary.png and .svg')


def seal_endpoint_audit():
    datasets = {n: read(n) for n in ['identifiability.json', 'microscopic.json',
                                    'phase6-real-roots.json', 'colour-singlet.json']}
    failures = []
    for name, data in datasets.items():
        assert data['checks_total'] == len(data['checks']), name
        assert data['checks_passed'] == sum(bool(c['passed']) for c in data['checks']), name
        failures.extend((name, c['name']) for c in data['checks'] if not c['passed'])
    assert failures == [('microscopic.json', 'Phase6 full source replay completes')], failures
    timeout = read('attempts/phase6_dynamics/execution.json')
    assert not timeout['completed'] and timeout['timeout_seconds'] == 60
    assert datasets['phase6-real-roots.json']['checks_passed'] == 13
    assert read('attempts/mac02_soldering/execution.json')['returncode'] == 0
    provenance = []
    for name in ['provenance.json', 'microscopic-provenance.json',
                 'supplementary-provenance.json', 'colour-provenance.json']:
        for row in read(name):
            source, snapshot = Path(row['source']), ROOT / row['snapshot']
            assert digest(snapshot) == row['sha256'], row['snapshot']
            if 'character_start' in row:
                assert digest(source) == row['source_sha256'], row['source']
                assert source.read_text()[row['character_start']:row['character_end']] == snapshot.read_text()
            else:
                assert digest(source) == row['sha256'], row['source']
            provenance.append(row)
    recovery = read('CPF-recovery.json')
    parent = Path(recovery['source'])
    assert digest(parent) == recovery['source_sha256']
    parent_text = parent.read_text()
    for row in recovery['objects']:
        obj, _ = json.JSONDecoder().raw_decode(parent_text[row['offset']:])
        snapshot = ROOT / row['output']
        assert obj['TargetFile'] == row['target']
        assert obj['CodeContent'] == snapshot.read_text()
        assert len(obj['CodeContent']) == row['characters']
        assert digest(snapshot) == row['sha256']
    last = ROOT / 'docs/condensate_energy/source_endpoint/receipt.json'
    prior = dict(json.loads(last.read_text())['prior_receipts_verified'])
    prior[str(last.relative_to(ROOT))] = digest(last)
    prior_artifacts = {}
    for path, expected in prior.items():
        receipt = ROOT / path
        assert digest(receipt) == expected, path
        for artifact, value in json.loads(receipt.read_text())['artifact_sha256'].items():
            assert digest(ROOT / artifact) == value, artifact
            if artifact in prior_artifacts:
                assert prior_artifacts[artifact] == value, artifact
            prior_artifacts[artifact] = value
    audit = read('completion-audit.json')
    assert len(audit['requirements']) == 7 and len(audit['protocol_items']) == 7
    linked_evidence = {}
    for row in audit['requirements']:
        assert row['resolution'].startswith('achieved'), row['id']
        assert row['finding'] and row['limits'] and row['evidence'], row['id']
        for path in row['evidence']:
            assert (ROOT / path).is_file(), path
            linked_evidence[path] = digest(ROOT / path)
    assert all(not item['is_required_unresolved_mathematical_work'] for item in audit['unresolved_execution'])
    # Existence is only a delivery check; the requirement prose states actual scope.
    for target in re.findall(r'\]\(([^)]+)\)', (OUT / 'README.md').read_text()):
        if '://' in target or target.startswith('#') or target == 'receipt.json':
            continue
        resolved = (OUT / target.split('#')[0]).resolve()
        assert resolved.is_file(), target
        linked_evidence[str(resolved)] = digest(resolved)
    for log in ['acs-endpoint-identifiability.log', 'acs-microscopic-selector-boundary-reconciled.log',
                'acs-phase6-real-boundary.log', 'acs-colour-singlet-boundary.log']:
        (OUT / 'attempts' / log).write_bytes((Path('/private/tmp') / log).read_bytes())
    review = read('visual-review.json')
    assert review['reviewed'] and review['legible']
    assert review['png_sha256'] == digest(OUT / 'endpoint-boundary.png')
    passed = sum(d['checks_passed'] for d in datasets.values())
    assert passed == 95
    assessment = dict(status='Scoped action-to-carrier investigation at evidential endpoint',
        checks_passed=passed, checks_total=passed + len(failures),
        incomplete_source_replays=[dict(dataset=n, check=c) for n, c in failures],
        incomplete_replay_math_resolved_by='phase6-real-roots.json',
        forward_calculation='Complete scalar action and specified conditional matching, binding and leakage',
        established_obstruction='Compatible complete actions have different masses, vacua and carrier thresholds',
        missing_physical_inputs=['Normalized microscopic condensate-to-field map',
                                 'Coefficient, scale and flavor selection law',
                                 'Physical vacuum and quantum carrier identification'],
        discovery_limit='No exhaustive semantic recovery of whole drives, encrypted archives or unexported cloud chats',
        scientific_limit='No completed theory of matter, RH proof or universal no-go theorem for future ACS constructions',
        dependency_versions=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                                 sympy=sympy.__version__, mpmath=mpmath.__version__, matplotlib=matplotlib.__version__),
        requirements_reviewed=len(audit['requirements']), protocol_items_reviewed=len(audit['protocol_items']))
    (OUT / 'assessment.json').write_text(json.dumps(assessment, indent=2) + '\n')
    scripts = ['endpoint_identifiability.py', 'microscopic_selector_boundary.py', 'phase6_real_boundary.py',
               'colour_singlet_boundary.py', 'publish_endpoint_audit.py']
    artifacts = [ROOT / 'code/condensate_energy' / name for name in scripts]
    artifacts += [p for p in OUT.rglob('*') if p.is_file() and p.name != 'receipt.json' and '__pycache__' not in p.parts]
    receipt = dict(status=assessment['status'], checks_passed=passed, incomplete_source_replays=1,
        prior_receipts_verified=prior, prior_artifacts_verified=prior_artifacts,
        linked_evidence_verified=linked_evidence, source_records_verified=len(provenance),
        artifact_sha256={str(p.relative_to(ROOT)): digest(p) for p in sorted(artifacts)})
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(dict(checks_passed=passed, incomplete_source_replays=1,
        artifacts=len(receipt['artifact_sha256']), prior_receipts=len(prior),
        prior_artifacts=len(prior_artifacts), source_records_verified=len(provenance))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--render-only', action='store_true')
    mode.add_argument('--seal', action='store_true')
    args = parser.parse_args()
    if args.render_only:
        render_endpoint_audit()
    else:
        seal_endpoint_audit()
