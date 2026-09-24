#!/usr/bin/env python3
"""Publish the input-selector diagnostics and independently verify older seals."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR','/private/tmp/acs-condensate-energy-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigvalsh
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/condensate_energy/input_closure'


def render_selector_evidence():
    result=json.loads((OUT/'selector-results.json').read_text())
    fallback=json.loads((OUT/'fallback-resolution.json').read_text())
    curvature=result['curvature']
    bounds=[1]+[x['basis_scale_bound'] for x in curvature['basis_variations']]
    raw=[curvature['original_raw_mass_ratio']]+[x['raw_abs_curvature_mass_ratio'] for x in curvature['basis_variations']]
    H=np.array([[float(sp.Rational(v)) for v in row] for row in curvature['hessian_I']])
    G=np.array([[float(sp.Rational(v)) for v in row] for row in curvature['kinetic_Gram']])
    ev=eigvalsh(H,G); diagnostic=np.sqrt(max(abs(ev))/min(abs(ev)))
    fig,axes=plt.subplots(1,2,figsize=(12.4,5.2),layout='constrained')
    axes[0].plot(bounds,raw,'o-',lw=2.2,color='#b56745',label='Archived raw-eigenvalue ratio')
    axes[0].axhline(diagnostic,color='#286785',lw=2.2,label='Include stipulated kinetic Gram matrix')
    axes[0].set(xlabel='Basis rescaling bound (same matrices F and G)',ylabel='Absolute-curvature mass-ratio diagnostic',
                title='A coordinate choice changes the archived “scale”',xticks=bounds)
    axes[0].legend(frameon=False,fontsize=8.2)
    beta=np.geomspace(1e-3,1,1000)
    yy=np.sort(np.array([np.ones_like(beta),2*beta,4*beta*np.sqrt(1+beta*beta)]),axis=0)
    gap=np.min(yy[1:]/yy[:-1],axis=0)
    axes[1].semilogx(beta,gap,lw=2.2,color='#286785',label='Smaller adjacent amplitude ratio')
    axes[1].axhline(2*np.sqrt(2),ls='--',color='#b56745',label='Exact uniform upper bound')
    axes[1].axhline(min(fallback['comparison_adjacent_amplitude_ratios']),ls=':',color='#487d63',lw=2,
                   label='Smaller required lepton ratio')
    axes[1].set(xlabel='Normalized transverse-field coefficient |b|',ylabel='Amplitude ratio (square root of mass ratio)',
                title='Restored fallback cannot reach the full hierarchy',ylim=(.7,4.7))
    axes[1].legend(frameon=False,fontsize=8.2,loc='center left',bbox_to_anchor=(.01,.63))
    for ax in axes:
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.suptitle('ACS input selection: test what fixes the number',fontsize=15)
    fig.supxlabel('Left: neither curve is a physical mass spectrum; the source point is not stationary. '
        'Right: exact obstruction applies to the source’s normalized TT fallback.\n'
        'Source equations, independent checks, comparison inputs and alternative hypotheses are stated in the report.',fontsize=8.4)
    for ext in ['png','svg']:fig.savefig(OUT/('input-selection.'+ext),dpi=180)
    plt.close(fig)
    print('Rendered input-selection.png and .svg')


def seal_selector_evidence():
    names=['selector-results.json','independent-verification.json','fallback-resolution.json']
    results=[json.loads((OUT/n).read_text()) for n in names]
    assert all(x['checks_total']==x['checks_passed'] for x in results)
    assert all(c['passed'] for x in results for c in x['checks'])
    total=sum(x['checks_total'] for x in results)
    prior_path=ROOT/'docs/condensate_energy/finite_matching/receipt.json'
    previous=json.loads(prior_path.read_text())
    prior=dict(previous['prior_receipts_verified'])
    prior[str(prior_path.relative_to(ROOT))]=sha256(prior_path.read_bytes()).hexdigest()
    prior_artifacts={}
    for name,h in prior.items():
        p=ROOT/name;assert sha256(p.read_bytes()).hexdigest()==h,name
        for path,digest in json.loads(p.read_text()).get('artifact_sha256',{}).items():
            assert sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
            prior_artifacts[path]=digest
    # Freeze successful command outputs, not only counters.
    for log in ['acs-input-selector.log','acs-verify-input-selectors.log','acs-fallback-selector.log']:
        (OUT/'attempts'/log).write_bytes((Path('/private/tmp')/log).read_bytes())
    assessment=dict(status='Source-selector stage complete; full ACS goal active',
        previous_turn_classification='progress',checks_passed=total,
        established=['Real VEV projection vanishes on its full stated domain',
            'Imaginary repair has rank three and leaves VEV direction free',
            'Proposed trough is nonstationary; raw Hessian ratio depends on coordinates',
            'Computed block complement is zero and unused by printed neutrino prediction',
            'Unbroken color forbids a singlet-triplet invariant mass mixing vector',
            'Historical blanket annihilation claim fails for the implemented fallback',
            'Normalized fallback still cannot yield the two charged-lepton hierarchy ratios',
            'Recovered GfE cutoff derivation fails its fixed point and selection steps',
            'Recovered project correlation test inserts constants and depends on units'],
        retained=['Correct commutator identities',
            'Forward projection and generalized curvature tools with explicitly stated inputs',
            'Prior conditional full-action spectra and restricted finite matching'],
        remaining=json.loads((OUT/'source-coverage.json').read_text())['remaining'],
        limits=['No claim of exhaustive live-chat or whole-drive recovery',
            'No new physical constant, particle mass, RH proof or universal no-go theorem',
            'The restored source fallback and the changed imaginary projection are distinct hypotheses'])
    (OUT/'assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    scripts=['input_selector_audit.py','verify_input_selectors.py','fallback_selector_resolution.py','publish_input_closure.py']
    artifacts=[ROOT/'code/condensate_energy'/x for x in scripts]
    artifacts.extend(p for p in OUT.rglob('*') if p.is_file() and p.name!='receipt.json' and '__pycache__' not in p.parts)
    receipt=dict(status=assessment['status'],checks_passed=total,prior_receipts_verified=prior,
        prior_artifacts_verified=prior_artifacts,
        artifact_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(artifacts)})
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(checks_passed=total,artifacts=len(receipt['artifact_sha256']),
        prior_receipts=len(prior),prior_artifacts=len(prior_artifacts))))


if __name__=='__main__':
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--render-only',action='store_true');group.add_argument('--seal',action='store_true')
    args=parser.parse_args()
    if args.render_only:render_selector_evidence()
    else:seal_selector_evidence()
